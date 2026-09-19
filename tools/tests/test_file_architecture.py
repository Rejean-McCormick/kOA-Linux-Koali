from __future__ import annotations

import hashlib
import json
from pathlib import Path

from koa_tools.checks.dependencies import check_dependencies
from koa_tools.checks.file_architecture import check_file_architecture
from koa_tools.checks.generated_content import check_generated_content
from koa_tools.commands import diagnose, validate, verify


def write_json(root: Path, relative: str, value: object) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


def touch(root: Path, relative: str, content: str = "") -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def architecture_registries(root: Path, paths: list[str]) -> None:
    all_paths = sorted(set(paths + [
        ".koa/repository.json",
        ".koa/path-ownership.json",
        ".koa/dependency-rules.json",
        ".koa/generated-paths.json",
        ".koa/file-architecture.lock.json",
    ]))
    write_json(root, ".koa/repository.json", {"allowed_top_level_roots": [".koa", "docs", "generated", "components", "interfaces"]})
    write_json(root, ".koa/path-ownership.json", {"rules": [
        {"owner": "repository", "path": ".koa"},
        {"owner": "documentation", "path": "docs"},
        {"owner": "generators", "path": "generated"},
        {"owner": "components", "path": "components"},
        {"owner": "interfaces", "path": "interfaces"},
    ]})
    write_json(root, ".koa/dependency-rules.json", {"rules": []})
    write_json(root, ".koa/generated-paths.json", {"entries": []})
    write_json(root, ".koa/file-architecture.lock.json", {"paths": all_paths})


def test_file_architecture_accepts_exact_deterministic_inventory(tmp_path: Path) -> None:
    touch(tmp_path, "docs/README.md", "# docs\n")
    architecture_registries(tmp_path, ["docs/README.md"])

    result = check_file_architecture(tmp_path)

    assert result.ok, result.to_dict()
    assert result.metadata["actual_paths"] == result.metadata["expected_paths"]




def test_file_architecture_ignores_gitignored_workspace_artifacts(tmp_path: Path) -> None:
    touch(tmp_path, ".gitignore", "build/\n*.egg-info/\nGitSink.bat\n")
    touch(tmp_path, "docs/README.md", "# docs\n")
    touch(tmp_path, "components/example/build/lib/generated.py")
    touch(tmp_path, "components/example/src/example.egg-info/PKG-INFO")
    touch(tmp_path, "GitSink.bat")
    architecture_registries(tmp_path, [".gitignore", "docs/README.md"])

    result = check_file_architecture(tmp_path, include_related=False)

    assert result.ok, result.to_dict()
    assert result.metadata["actual_paths"] == result.metadata["expected_paths"]


def test_file_architecture_reports_unknown_missing_and_unknown_root(tmp_path: Path) -> None:
    touch(tmp_path, "docs/README.md")
    touch(tmp_path, "surprise/value.txt")
    architecture_registries(tmp_path, ["docs/README.md", "docs/MISSING.md"])

    result = check_file_architecture(tmp_path, include_related=False)

    assert not result.ok
    found = {(finding.code, finding.path) for finding in result.findings}
    assert ("FILE_UNKNOWN", "surprise/value.txt") in found
    assert ("FILE_MISSING", "docs/MISSING.md") in found
    assert ("FILE_TOP_LEVEL_ROOT", "surprise/value.txt") in found


def test_generated_content_checks_declaration_source_and_digest(tmp_path: Path) -> None:
    touch(tmp_path, "docs/source.json", "{}")
    touch(tmp_path, "generated/view.json", '{"generated":true}')
    digest = hashlib.sha256((tmp_path / "generated/view.json").read_bytes()).hexdigest()
    write_json(tmp_path, ".koa/generated-paths.json", {"entries": [{
        "path": "generated/view.json",
        "source": "docs/source.json",
        "renderer": "example-v1",
        "sha256": digest,
    }]})

    assert check_generated_content(tmp_path).ok

    touch(tmp_path, "generated/view.json", '{"generated":false}')
    stale = check_generated_content(tmp_path)
    assert not stale.ok
    assert any(item.code == "GENERATED_CONTENT_STALE" for item in stale.findings)


def test_generated_content_rejects_undeclared_generated_file(tmp_path: Path) -> None:
    touch(tmp_path, "generated/unregistered.json", "{}")
    write_json(tmp_path, ".koa/generated-paths.json", {"entries": []})

    result = check_generated_content(tmp_path)

    assert not result.ok
    assert any(item.code == "GENERATED_PATH_UNDECLARED" for item in result.findings)


def test_dependencies_reject_private_cross_component_import(tmp_path: Path) -> None:
    touch(tmp_path, "components/a/src/koa_a/domain/model.py", "from koa_b.domain import secret\n")
    touch(tmp_path, "components/b/src/koa_b/domain/secret.py", "VALUE = 1\n")
    write_json(tmp_path, ".koa/dependency-rules.json", {"rules": []})

    result = check_dependencies(tmp_path)

    assert not result.ok
    assert any(item.code == "DEPENDENCY_PROHIBITED" for item in result.findings)


def test_dependencies_accept_public_interface_import(tmp_path: Path) -> None:
    touch(tmp_path, "components/a/src/koa_a/domain/model.py", "from koa_interfaces import Receipt\n")
    touch(tmp_path, "interfaces/python/koa_interfaces/__init__.py", "class Receipt: ...\n")
    write_json(tmp_path, ".koa/dependency-rules.json", {"rules": []})

    result = check_dependencies(tmp_path)

    assert result.ok, result.to_dict()


def test_validate_verify_and_diagnose_commands_expose_same_checks(tmp_path: Path, capsys) -> None:
    touch(tmp_path, "docs/README.md", "# docs\n")
    architecture_registries(tmp_path, ["docs/README.md"])

    assert validate.main(["--root", str(tmp_path)]) == 0
    validate_output = capsys.readouterr().out
    assert "architecture-checks: pass" in validate_output

    assert verify.main(["--root", str(tmp_path)]) == 0
    verify_output = capsys.readouterr().out
    assert "architecture-checks: pass" in verify_output

    assert diagnose.main(["--root", str(tmp_path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["readiness"] == "ready"
    assert [item["check_id"] for item in payload["checks"]] == [
        "file-architecture",
        "path-ownership",
        "dependencies",
        "generated-content",
    ]


def _pipeline_fixture(root: Path, *, ready: bool) -> None:
    profile_ref = "docs/contracts/profiles/sovereign-linux-node.profile.json"
    profile = {
        "profile_id": "sovereign_linux_node",
        "profile_kind": "primary_profile",
        "components": {
            "identity_and_trust": {"state": "required"},
            "ariane": {"state": "required"},
        },
    }
    write_json(root, profile_ref, profile)
    write_json(
        root,
        "docs/generated/component-catalog.json",
        {"generated": True, "records": [{"id": "identity_and_trust"}]},
    )
    touch(
        root,
        "packaging/components/identity-and-trust.toml",
        "\n".join(
            [
                'source_bundle = "B-0023"',
                "",
                "[upstream_bundle]",
                'output = "generated/component-bundles/identity-and-trust"',
            ]
        )
        + "\n",
    )
    touch(
        root,
        "packaging/subsystems/ariane.toml",
        "\n".join(
            [
                "[source]",
                'lock_path = "integrations/ariane/source.lock.json"',
            ]
        )
        + "\n",
    )
    write_json(
        root,
        "integrations/ariane/source.lock.json",
        {"pin_state": "pinned" if ready else "unresolved", "activation": {"allowed": ready}},
    )
    touch(
        root,
        "packaging/system/image.toml",
        "\n".join(
            [
                f'status = "{"ready" if ready else "blocked_missing_inputs"}"',
                'assembly_plan_bundle_source = "generated/assembly/B-0092/bundle.json"',
                "activation_ready = false",
                "",
                "[identity]",
                "complete_release_set_required = true",
            ]
        )
        + "\n",
    )

    if not ready:
        touch(root, "generated/profiles/sovereign_linux_node/resolved-plan.json", "{}\n")
        return

    profile_digest = hashlib.sha256((root / profile_ref).read_bytes()).hexdigest()
    write_json(
        root,
        "generated/profiles/sovereign_linux_node/effective-profile.json",
        {
            "format": "koa.effective-profile",
            "authority": "derived_projection",
            "manual_edits": "prohibited",
            "primary_profile": {"profile_id": "sovereign_linux_node", "version": "1.0.0"},
            "result": "pass",
            "source_digests": {profile_ref: profile_digest},
        },
    )
    write_json(root, "generated/component-bundles/identity-and-trust/bundle.json", {"bundle_id": "B-0023"})
    write_json(
        root,
        "generated/rootfs/package-resolution.json",
        {"package_set_id": "koa.host.base-packages", "profile_id": "sovereign_linux_node"},
    )
    write_json(
        root,
        "generated/profiles/sovereign_linux_node/resolved-plan.json",
        {
            "profile_id": "sovereign_linux_node",
            "plan_id": "test-plan",
            "source_digests": {profile_ref: profile_digest},
            "services": [],
            "networks": [],
            "volumes": [],
            "packages": [],
            "files": [],
            "offline": {},
            "backup": {},
        },
    )
    write_json(root, "generated/assembly/B-0092/bundle.json", {"bundle_id": "B-0092"})
    write_json(
        root,
        "generated/release/candidates/test-release-set.json",
        {
            "artifact_class": "release_set",
            "release_set_id": "test.release-set",
            "channels": {
                "system": {},
                "services": {},
                "governance": {},
                "knowledge": {},
            },
            "compatibility": {"status": "compatible"},
            "activation": {"eligibility": "eligible"},
            "signature": {"verification_status": "verified"},
        },
    )


def test_pipeline_diagnose_reports_authority_blockers_without_writing(tmp_path: Path) -> None:
    _pipeline_fixture(tmp_path, ready=False)
    before = {
        path.relative_to(tmp_path).as_posix(): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    payload = diagnose.collect_pipeline(tmp_path, "sovereign-linux-node")

    after = {
        path.relative_to(tmp_path).as_posix(): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    codes = {item["code"] for item in payload["blockers"]}
    assert payload["readiness"] == "blocked"
    assert {
        "pipeline_effective_profile_missing",
        "pipeline_component_bundle_missing",
        "pipeline_subsystem_source_unresolved",
        "pipeline_package_resolution_missing",
        "pipeline_resolved_plan_invalid",
        "pipeline_b0092_not_renderable",
        "pipeline_image_inputs_missing",
        "pipeline_release_evidence_missing",
    } <= codes
    assert before == after


def test_pipeline_diagnose_passes_only_when_observed_chain_is_closed(tmp_path: Path) -> None:
    _pipeline_fixture(tmp_path, ready=True)

    payload = diagnose.collect_pipeline(tmp_path, "sovereign-linux-node")

    assert payload["readiness"] == "ready"
    assert payload["blockers"] == []
    assert all(stage["status"] == "pass" for stage in payload["stages"])


def test_pipeline_diagnose_rejects_legacy_root_primary_profile_id(tmp_path: Path) -> None:
    _pipeline_fixture(tmp_path, ready=True)
    path = tmp_path / "generated/profiles/sovereign_linux_node/effective-profile.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.pop("primary_profile", None)
    payload["primary_profile_id"] = "sovereign_linux_node"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    result = diagnose.collect_pipeline(tmp_path, "sovereign-linux-node")

    assert result["readiness"] == "blocked"
    assert "pipeline_effective_profile_stale" in {item["code"] for item in result["blockers"]}
