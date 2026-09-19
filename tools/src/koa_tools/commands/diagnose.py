"""Report repository and pipeline readiness without changing repository state."""
from __future__ import annotations

import argparse
import hashlib
import json
import tomllib
from pathlib import Path
from typing import Any, Mapping, Sequence

from koa_tools.checks import repository_root
from . import CANONICAL_PROFILES
from .validate import execute

REGISTRIES = (
    ".koa/repository.json",
    ".koa/path-ownership.json",
    ".koa/dependency-rules.json",
    ".koa/generated-paths.json",
    ".koa/file-architecture.lock.json",
)

_REQUIRED_PLAN_KEYS = (
    "profile_id",
    "plan_id",
    "source_digests",
    "services",
    "networks",
    "volumes",
    "packages",
    "files",
    "offline",
    "backup",
)


def configure_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--pipeline",
        action="store_true",
        help="inspect profile-to-release pipeline readiness without producing artifacts",
    )
    parser.add_argument(
        "--profile",
        choices=CANONICAL_PROFILES,
        help="canonical profile to inspect with --pipeline",
    )
    return parser


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> argparse.ArgumentParser:
    parser = configure_parser(subparsers.add_parser("diagnose", help=__doc__))
    parser.set_defaults(handler=run, func=run)
    return parser


add_parser = register


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("document root must be an object")
    return value


def _load_toml(path: Path) -> Mapping[str, Any]:
    value = tomllib.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("document root must be a table")
    return value


def _stage(stage: str) -> dict[str, Any]:
    return {"stage": stage, "status": "pass", "reason_codes": [], "details": []}


def _block(
    stage: dict[str, Any],
    blockers: list[dict[str, str]],
    code: str,
    detail: str,
    *,
    path: str | None = None,
) -> None:
    stage["status"] = "blocked"
    if code not in stage["reason_codes"]:
        stage["reason_codes"].append(code)
    finding = {"code": code, "stage": str(stage["stage"]), "detail": detail}
    if path is not None:
        finding["path"] = path
    blockers.append(finding)
    stage["details"].append(finding)


def _profile_contract(base: Path, profile: str) -> tuple[dict[str, Any], Mapping[str, Any] | None]:
    stage = _stage("profile_contract")
    blockers: list[dict[str, str]] = []
    relative = f"docs/contracts/profiles/{profile}.profile.json"
    path = base / relative
    if not path.is_file():
        _block(stage, blockers, "pipeline_profile_invalid", "canonical profile contract is missing", path=relative)
        return {"stage": stage, "blockers": blockers}, None
    try:
        contract = _load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        _block(stage, blockers, "pipeline_profile_invalid", f"profile contract is unreadable: {exc}", path=relative)
        return {"stage": stage, "blockers": blockers}, None

    expected_id = profile.replace("-", "_")
    if contract.get("profile_id") != expected_id or contract.get("profile_kind") != "primary_profile":
        _block(
            stage,
            blockers,
            "pipeline_profile_invalid",
            "pipeline diagnosis requires a matching canonical primary profile contract",
            path=relative,
        )
    return {"stage": stage, "blockers": blockers}, contract


def _effective_profile(base: Path, profile: str) -> tuple[dict[str, Any], Mapping[str, Any] | None]:
    stage = _stage("effective_profile")
    blockers: list[dict[str, str]] = []
    profile_id = profile.replace("-", "_")
    relative = f"generated/profiles/{profile_id}/effective-profile.json"
    path = base / relative
    if not path.is_file():
        _block(stage, blockers, "pipeline_effective_profile_missing", "effective-profile projection is absent", path=relative)
        return {"stage": stage, "blockers": blockers}, None
    try:
        declaration = _load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        _block(stage, blockers, "pipeline_effective_profile_stale", f"effective-profile projection is invalid: {exc}", path=relative)
        return {"stage": stage, "blockers": blockers}, None

    primary_profile = declaration.get("primary_profile")
    declared_primary_profile_id = (
        primary_profile.get("profile_id") if isinstance(primary_profile, dict) else None
    )
    if (
        declaration.get("format") != "koa.effective-profile"
        or declaration.get("authority") != "derived_projection"
        or declaration.get("manual_edits") != "prohibited"
        or declared_primary_profile_id != profile_id
        or declaration.get("result") != "pass"
    ):
        _block(stage, blockers, "pipeline_effective_profile_stale", "effective-profile identity or derived-authority markers do not match", path=relative)

    source_digests = declaration.get("source_digests")
    if not isinstance(source_digests, dict) or not source_digests:
        _block(stage, blockers, "pipeline_effective_profile_stale", "effective-profile source digests are absent", path=relative)
    else:
        for source, expected in sorted(source_digests.items()):
            if not isinstance(source, str) or not isinstance(expected, str):
                _block(stage, blockers, "pipeline_effective_profile_stale", "effective-profile source digest entry is malformed", path=relative)
                continue
            source_path = base / source
            if not source_path.is_file() or _sha256(source_path) != expected.removeprefix("sha256:"):
                _block(stage, blockers, "pipeline_effective_profile_stale", f"effective-profile source digest does not match {source}", path=source)

    return {"stage": stage, "blockers": blockers}, declaration


def _required_members(contract: Mapping[str, Any] | None) -> tuple[str, ...]:
    if contract is None:
        return ()
    components = contract.get("components")
    if not isinstance(components, dict):
        return ()
    return tuple(
        sorted(
            component_id
            for component_id, entry in components.items()
            if isinstance(component_id, str)
            and isinstance(entry, dict)
            and entry.get("state") == "required"
        )
    )


def _native_component_ids(base: Path) -> set[str]:
    path = base / "docs/generated/component-catalog.json"
    if not path.is_file():
        return set()
    try:
        catalog = _load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
        return set()
    records = catalog.get("records")
    if not isinstance(records, list):
        return set()
    return {
        str(item["id"])
        for item in records
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _component_bundles(base: Path, contract: Mapping[str, Any] | None) -> dict[str, Any]:
    stage = _stage("component_bundles")
    blockers: list[dict[str, str]] = []
    native_ids = _native_component_ids(base)
    for component_id in _required_members(contract):
        if component_id not in native_ids:
            continue
        slug = component_id.replace("_", "-")
        manifest_ref = f"packaging/components/{slug}.toml"
        manifest_path = base / manifest_ref
        if not manifest_path.is_file():
            _block(stage, blockers, "pipeline_component_bundle_missing", f"packaging manifest for required component {component_id} is missing", path=manifest_ref)
            continue
        try:
            manifest = _load_toml(manifest_path)
        except (OSError, UnicodeError, tomllib.TOMLDecodeError, ValueError) as exc:
            _block(stage, blockers, "pipeline_component_bundle_invalid", f"component packaging manifest is invalid: {exc}", path=manifest_ref)
            continue
        upstream = manifest.get("upstream_bundle")
        output = upstream.get("output") if isinstance(upstream, dict) else None
        source_bundle = manifest.get("source_bundle")
        if not isinstance(output, str) or not output:
            _block(stage, blockers, "pipeline_component_bundle_invalid", f"required component {component_id} has no declared upstream bundle output", path=manifest_ref)
            continue
        bundle_ref = f"{output.rstrip('/')}/bundle.json"
        bundle_path = base / bundle_ref
        if not bundle_path.is_file():
            label = f" ({source_bundle})" if isinstance(source_bundle, str) else ""
            _block(stage, blockers, "pipeline_component_bundle_missing", f"required component bundle{label} for {component_id} is absent", path=bundle_ref)
            continue
        try:
            _load_json(bundle_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            _block(stage, blockers, "pipeline_component_bundle_invalid", f"component bundle is invalid: {exc}", path=bundle_ref)
    return {"stage": stage, "blockers": blockers}


def _source_lock_resolved(lock: Mapping[str, Any]) -> bool:
    negative = {"blocked", "unresolved", "blocked_missing_authoritative_source", "blocked_missing_authoritative_source_metadata"}
    for key in ("pin_state", "lock_status", "status"):
        value = lock.get(key)
        if isinstance(value, str) and (value in negative or value.startswith("blocked") or "unresolved" in value):
            return False
    activation = lock.get("activation")
    if isinstance(activation, dict) and activation.get("allowed") is False:
        return False
    if lock.get("activation_allowed") is False or lock.get("admission_enabled") is False:
        return False
    return True


def _subsystem_sources(base: Path, contract: Mapping[str, Any] | None) -> dict[str, Any]:
    stage = _stage("subsystem_sources")
    blockers: list[dict[str, str]] = []
    native_ids = _native_component_ids(base)
    for subsystem_id in _required_members(contract):
        if subsystem_id in native_ids:
            continue
        slug = subsystem_id.replace("_", "-")
        manifest_ref = f"packaging/subsystems/{slug}.toml"
        manifest_path = base / manifest_ref
        if not manifest_path.is_file():
            _block(stage, blockers, "pipeline_subsystem_bundle_missing", f"required subsystem {subsystem_id} has no packaging declaration", path=manifest_ref)
            continue
        try:
            manifest = _load_toml(manifest_path)
        except (OSError, UnicodeError, tomllib.TOMLDecodeError, ValueError) as exc:
            _block(stage, blockers, "pipeline_subsystem_bundle_missing", f"subsystem packaging declaration is invalid: {exc}", path=manifest_ref)
            continue
        source = manifest.get("source")
        lock_ref = source.get("lock_path") if isinstance(source, dict) else None
        if not isinstance(lock_ref, str) or not lock_ref:
            _block(stage, blockers, "pipeline_subsystem_source_unresolved", f"required subsystem {subsystem_id} has no declared source lock", path=manifest_ref)
            continue
        lock_path = base / lock_ref
        if not lock_path.is_file():
            _block(stage, blockers, "pipeline_subsystem_source_unresolved", f"required subsystem {subsystem_id} source lock is missing", path=lock_ref)
            continue
        try:
            lock = _load_json(lock_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            _block(stage, blockers, "pipeline_subsystem_source_unresolved", f"subsystem source lock is invalid: {exc}", path=lock_ref)
            continue
        if not _source_lock_resolved(lock):
            _block(stage, blockers, "pipeline_subsystem_source_unresolved", f"required subsystem {subsystem_id} source authority remains unresolved", path=lock_ref)
    return {"stage": stage, "blockers": blockers}


def _package_resolution(base: Path, profile: str) -> dict[str, Any]:
    stage = _stage("package_resolution")
    blockers: list[dict[str, str]] = []
    candidates = tuple(sorted(base.glob("generated/**/package-resolution.json")))
    if not candidates:
        _block(stage, blockers, "pipeline_package_resolution_missing", "no materialized package-resolution.json exists under generated/")
        return {"stage": stage, "blockers": blockers}

    profile_id = profile.replace("-", "_")
    matching: list[tuple[Path, Mapping[str, Any]]] = []
    for path in candidates:
        try:
            resolution = _load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
            continue
        if (
            resolution.get("profile_id") == profile_id
            and resolution.get("package_set_id") == "koa.host.base-packages"
        ):
            matching.append((path, resolution))

    if not matching:
        _block(
            stage,
            blockers,
            "pipeline_package_resolution_missing",
            "no package resolution under generated/ matches the selected profile and base package set",
        )
        return {"stage": stage, "blockers": blockers}
    if len(matching) != 1:
        refs = ", ".join(path.relative_to(base).as_posix() for path, _ in matching)
        _block(
            stage,
            blockers,
            "pipeline_package_resolution_invalid",
            f"multiple package resolutions claim the selected profile/base package identity: {refs}",
        )
    return {"stage": stage, "blockers": blockers}


def _resolved_plan(base: Path, profile: str) -> dict[str, Any]:
    stage = _stage("resolved_plan")
    blockers: list[dict[str, str]] = []
    profile_id = profile.replace("-", "_")
    relative = f"generated/profiles/{profile_id}/resolved-plan.json"
    path = base / relative
    if not path.is_file():
        _block(stage, blockers, "pipeline_resolved_plan_missing", "authority-derived resolved deployment plan is absent", path=relative)
        return {"stage": stage, "blockers": blockers}
    try:
        plan = _load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        _block(stage, blockers, "pipeline_resolved_plan_invalid", f"resolved deployment plan is invalid: {exc}", path=relative)
        return {"stage": stage, "blockers": blockers}
    missing = [key for key in _REQUIRED_PLAN_KEYS if key not in plan]
    if missing or plan.get("profile_id") not in {profile, profile_id}:
        detail = "resolved deployment plan is not closed"
        if missing:
            detail += "; missing=" + ",".join(missing)
        _block(stage, blockers, "pipeline_resolved_plan_invalid", detail, path=relative)
    return {"stage": stage, "blockers": blockers}


def _eligible_release_set(base: Path) -> tuple[str | None, Mapping[str, Any] | None]:
    root = base / "generated/release"
    if not root.is_dir():
        return None, None
    for path in sorted(root.rglob("*.json")):
        try:
            candidate = _load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
            continue
        if candidate.get("artifact_class") != "release_set" or not isinstance(candidate.get("release_set_id"), str):
            continue
        channels = candidate.get("channels")
        compatibility = candidate.get("compatibility")
        activation = candidate.get("activation")
        signature = candidate.get("signature")
        if (
            isinstance(channels, dict)
            and set(channels) == {"system", "services", "governance", "knowledge"}
            and isinstance(compatibility, dict)
            and compatibility.get("status") in {"compatible", "pass", "passed"}
            and isinstance(activation, dict)
            and activation.get("eligibility") in {"eligible", "ready"}
            and isinstance(signature, dict)
            and signature.get("verification_status") in {"verified", "pass", "passed"}
        ):
            return path.relative_to(base).as_posix(), candidate
    return None, None


def _image_and_release(base: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    image_stage = _stage("b0092_and_image")
    release_stage = _stage("release_prerequisites")
    image_blockers: list[dict[str, str]] = []
    release_blockers: list[dict[str, str]] = []
    settings_ref = "packaging/system/image.toml"
    settings_path = base / settings_ref
    if not settings_path.is_file():
        _block(image_stage, image_blockers, "pipeline_image_inputs_missing", "system image packaging settings are missing", path=settings_ref)
        _block(release_stage, release_blockers, "pipeline_release_evidence_missing", "release eligibility cannot be established without system image packaging authority", path=settings_ref)
        return {"stage": image_stage, "blockers": image_blockers}, {"stage": release_stage, "blockers": release_blockers}
    try:
        settings = _load_toml(settings_path)
    except (OSError, UnicodeError, tomllib.TOMLDecodeError, ValueError) as exc:
        _block(image_stage, image_blockers, "pipeline_image_inputs_missing", f"system image packaging settings are invalid: {exc}", path=settings_ref)
        _block(release_stage, release_blockers, "pipeline_release_evidence_missing", "release eligibility cannot be established from invalid system image packaging authority", path=settings_ref)
        return {"stage": image_stage, "blockers": image_blockers}, {"stage": release_stage, "blockers": release_blockers}

    bundle_ref = settings.get("assembly_plan_bundle_source")
    if not isinstance(bundle_ref, str) or not bundle_ref:
        _block(image_stage, image_blockers, "pipeline_b0092_not_renderable", "B-0092 output path is not declared by system image packaging", path=settings_ref)
    else:
        bundle_path = base / bundle_ref
        if not bundle_path.is_file():
            _block(image_stage, image_blockers, "pipeline_b0092_not_renderable", "B-0092 assembly bundle is absent", path=bundle_ref)
        else:
            try:
                _load_json(bundle_path)
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
                _block(image_stage, image_blockers, "pipeline_b0092_stale", f"B-0092 assembly bundle is invalid: {exc}", path=bundle_ref)

    status = settings.get("status")
    if isinstance(status, str) and status.startswith("blocked"):
        _block(image_stage, image_blockers, "pipeline_image_inputs_missing", f"system image packaging remains {status}", path=settings_ref)

    identity = settings.get("identity")
    complete_release_set_required = isinstance(identity, dict) and identity.get("complete_release_set_required") is True
    if complete_release_set_required:
        release_ref, _ = _eligible_release_set(base)
        if release_ref is None:
            _block(
                release_stage,
                release_blockers,
                "pipeline_release_evidence_missing",
                "no generated Release Set has four-channel closure, compatible status, activation eligibility, and verified signature",
            )
        else:
            release_stage["release_set_ref"] = release_ref
    return {"stage": image_stage, "blockers": image_blockers}, {"stage": release_stage, "blockers": release_blockers}


def collect_pipeline(base: Path, profile: str | None) -> dict[str, Any]:
    if profile is None:
        stage = _stage("profile_contract")
        blockers: list[dict[str, str]] = []
        _block(stage, blockers, "pipeline_profile_invalid", "--profile is required with --pipeline")
        return {"profile": None, "readiness": "blocked", "stages": [stage], "blockers": blockers}

    profile_result, contract = _profile_contract(base, profile)
    effective_result, _ = _effective_profile(base, profile)
    stages = [
        profile_result["stage"],
        effective_result["stage"],
        _component_bundles(base, contract)["stage"],
        _subsystem_sources(base, contract)["stage"],
        _package_resolution(base, profile)["stage"],
        _resolved_plan(base, profile)["stage"],
    ]
    image_result, release_result = _image_and_release(base)
    stages.extend((image_result["stage"], release_result["stage"]))
    blockers = [
        detail
        for stage in stages
        for detail in stage["details"]
        if isinstance(detail, dict) and "code" in detail
    ]
    return {
        "profile": profile,
        "readiness": "ready" if not blockers else "blocked",
        "stages": stages,
        "blockers": blockers,
    }


def collect(
    root: str | Path,
    *,
    pipeline: bool = False,
    profile: str | None = None,
) -> dict[str, Any]:
    base = repository_root(root)
    results = execute(base)
    registry_status = {path: (base / path).is_file() for path in REGISTRIES}
    architecture_ready = all(registry_status.values()) and all(result.ok for result in results)
    payload: dict[str, Any] = {
        "command": "diagnose",
        "root": base.as_posix(),
        "readiness": "ready" if architecture_ready else "blocked",
        "registries": registry_status,
        "checks": [result.to_dict() for result in results],
    }
    if pipeline:
        pipeline_result = collect_pipeline(base, profile)
        payload["architecture_readiness"] = payload["readiness"]
        payload["pipeline"] = pipeline_result
        payload["readiness"] = "ready" if architecture_ready and pipeline_result["readiness"] == "ready" else "blocked"
    return payload


def run(args: argparse.Namespace) -> int:
    payload = collect(
        args.root,
        pipeline=bool(getattr(args, "pipeline", False)),
        profile=getattr(args, "profile", None),
    )
    if getattr(args, "json", False):
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"repository: {payload['root']}")
        print(f"readiness: {payload['readiness']}")
        for path, present in payload["registries"].items():
            print(f"registry {'present' if present else 'missing'}: {path}")
        for result in payload["checks"]:
            counts = result["counts"]
            print(f"{result['check_id']}: {result['status']} ({counts['errors']} error(s), {counts['warnings']} warning(s))")
        pipeline = payload.get("pipeline")
        if isinstance(pipeline, dict):
            print(f"pipeline[{pipeline['profile'] or '-'}]: {pipeline['readiness']}")
            for stage in pipeline["stages"]:
                codes = ",".join(stage["reason_codes"]) or "-"
                print(f"pipeline {stage['stage']}: {stage['status']} ({codes})")
    return 0 if payload["readiness"] == "ready" else 1


def main(
    argv: Sequence[str] | None = None,
    *,
    repository_root: str | Path | None = None,
) -> int:
    parser = configure_parser(argparse.ArgumentParser(prog="koa diagnose", description=__doc__))
    args = parser.parse_args(argv)
    if repository_root is not None:
        args.root = Path(repository_root).expanduser().resolve()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
