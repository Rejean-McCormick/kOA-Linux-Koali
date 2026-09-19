#!/usr/bin/env python3
"""Run the offline operation CI gate and emit deterministic candidate evidence."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_scope import partition, is_qemu

SUITE_ID = "offline"
TEST_TYPE = "offline_operation"
EVIDENCE_TYPE = "offline_operation_test"
QEMU_TEST_PATH = "tests/offline/test_qemu_offline_navigation.py"
QEMU_SUPPORT_PATHS = [
    QEMU_TEST_PATH,
    "tests/system/qemu_harness.py",
    "tests/system/qemu-machine.toml",
]
DEFAULT_PATHS: list[str] = []
DEFAULT_COMMANDS: list[list[str]] = []
DEFAULT_POLICY = "ci/policies/offline-gates.json"
COMMAND_TIMEOUT_SECONDS = 1800


def _git(root: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
        timeout=30,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _command_record(argv: list[str], code: int) -> dict[str, Any]:
    displayed = [
        "{python}" if index == 0 and item == sys.executable else item
        for index, item in enumerate(argv)
    ]
    return {"argv": displayed, "exit_code": code, "outcome": "passed" if code == 0 else "failed"}


def _normalise_command(command: list[str]) -> list[str]:
    return [sys.executable if item == "{python}" else item for item in command]


def _load_policy(
    path: Path, suite: str
) -> tuple[list[dict[str, Any]], dict[str, str], list[str], str]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(document, dict)
        or document.get("status") != "active"
        or document.get("default_decision") != "block"
    ):
        raise ValueError("policy must be active and deny by default")
    gates = document.get("gates")
    if not isinstance(gates, list):
        raise ValueError("policy gates must be an array")
    selected = [gate for gate in gates if isinstance(gate, dict) and gate.get("suite") == suite]
    if not selected:
        raise ValueError(f"policy has no gate for suite {suite}")
    env: dict[str, str] = {}
    for gate in selected:
        for key, value in gate.get("environment", {}).items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError("gate environment must contain strings")
            env[key] = value
    inventory = document.get("expected_inventory", [])
    if isinstance(inventory, dict):
        inventory = inventory.get(suite, [])
    if not isinstance(inventory, list) or not all(
        isinstance(item, str) and item for item in inventory
    ):
        raise ValueError("expected_inventory must be a string array or a suite mapping")
    return selected, env, sorted(set(inventory)), _digest(path)


def _build_commands(
    root: Path, policy: Path | None
) -> tuple[list[list[str]], list[str], dict[str, str], str | None]:
    commands: list[list[str]] = []
    required: list[str] = []
    env: dict[str, str] = {}
    policy_digest: str | None = None
    if policy:
        gates, env, inventory, policy_digest = _load_policy(policy, SUITE_ID)
        required.extend(inventory)
        for gate in gates:
            required.extend(gate.get("required_paths", []))
            for command in gate.get("commands", []):
                if (
                    not isinstance(command, list)
                    or not command
                    or not all(isinstance(item, str) and item for item in command)
                ):
                    raise ValueError("policy command must be a non-empty string array")
                commands.append(_normalise_command(command))
            pytest_paths = gate.get("pytest_paths", [])
            if pytest_paths:
                arguments = gate.get("pytest_arguments", ["-q", "-p", "no:cacheprovider"])
                if not all(isinstance(item, str) and item for item in pytest_paths + arguments):
                    raise ValueError("pytest paths and arguments must be strings")
                commands.append([sys.executable, "-m", "pytest", *arguments, *pytest_paths])
    else:
        required.extend(DEFAULT_PATHS)
        commands.extend(_normalise_command(command) for command in DEFAULT_COMMANDS)
        if DEFAULT_PATHS:
            commands.append(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q",
                    "--disable-warnings",
                    "-p",
                    "no:cacheprovider",
                    *DEFAULT_PATHS,
                ]
            )
    return commands, sorted(set(required)), env, policy_digest


def _commands_include_qemu(root: Path, commands: list[list[str]]) -> bool:
    if not (root / QEMU_TEST_PATH).is_file():
        return False
    for command in commands:
        for item in command:
            if item == QEMU_TEST_PATH or item.rstrip("/") == "tests/offline":
                return True
    return False


def _load_qemu_harness(root: Path):
    path = root / "tests/system/qemu_harness.py"
    spec = importlib.util.spec_from_file_location("koa_qemu_harness_offline_ci", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load tests/system/qemu_harness.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _qemu_runtime_environment(
    root: Path, args: argparse.Namespace
) -> tuple[dict[str, str], list[str]]:
    environment: dict[str, str] = {"KOA_QEMU_NETWORK": "off"}
    blocked: list[str] = []

    def configured(name: str, argument: str | None) -> str:
        value = (argument or os.environ.get(name, "")).strip()
        if value:
            environment[name] = value
        return value

    image_value = configured("KOA_QEMU_IMAGE", args.qemu_image)
    profile_value = configured("KOA_QEMU_ACTIVE_PROFILE", args.qemu_active_profile)
    configured("KOA_QEMU_NAVIGATION_SURFACE_ID", args.qemu_navigation_surface_id)
    configured("KOA_QEMU_NAVIGATION_READY_REGEX", args.qemu_navigation_ready_regex)
    configured("KOA_QEMU_NAVIGATION_RESULT_REGEX", args.qemu_navigation_result_regex)
    configured("KOA_QEMU_NAVIGATION_KEYS", args.qemu_navigation_keys)
    mediatheque_selection = configured(
        "KOA_QEMU_MEDIATHEQUE_SELECTION", args.qemu_mediatheque_selection
    )
    release_set_value = configured("KOA_QEMU_ACTIVE_RELEASE_SET", args.qemu_active_release_set)
    configured("KOA_QEMU_MEDIATHEQUE_ARTIFACT_REF", args.qemu_mediatheque_artifact_ref)
    configured("KOA_QEMU_MEDIATHEQUE_OFFLINE_REGEX", args.qemu_mediatheque_offline_regex)
    environment["KOA_QEMU_IMAGE_FORMAT"] = args.qemu_image_format or os.environ.get(
        "KOA_QEMU_IMAGE_FORMAT", "raw"
    )

    required = (
        "KOA_QEMU_IMAGE",
        "KOA_QEMU_ACTIVE_PROFILE",
        "KOA_QEMU_NAVIGATION_SURFACE_ID",
        "KOA_QEMU_NAVIGATION_READY_REGEX",
        "KOA_QEMU_NAVIGATION_RESULT_REGEX",
        "KOA_QEMU_NAVIGATION_KEYS",
        "KOA_QEMU_MEDIATHEQUE_SELECTION",
    )
    for name in required:
        if not environment.get(name):
            blocked.append(f"{name} is required for offline QEMU validation")

    if environment["KOA_QEMU_IMAGE_FORMAT"] not in {"raw", "qcow2"}:
        blocked.append("KOA_QEMU_IMAGE_FORMAT must be 'raw' or 'qcow2'")
    if mediatheque_selection and mediatheque_selection not in {"selected", "not_selected"}:
        blocked.append("KOA_QEMU_MEDIATHEQUE_SELECTION must be 'selected' or 'not_selected'")
    if mediatheque_selection == "selected":
        for name in (
            "KOA_QEMU_ACTIVE_RELEASE_SET",
            "KOA_QEMU_MEDIATHEQUE_ARTIFACT_REF",
            "KOA_QEMU_MEDIATHEQUE_OFFLINE_REGEX",
        ):
            if not environment.get(name):
                blocked.append(f"{name} is required when kOA Mediatheque is selected")

    for name in (
        "KOA_QEMU_NAVIGATION_READY_REGEX",
        "KOA_QEMU_NAVIGATION_RESULT_REGEX",
        "KOA_QEMU_MEDIATHEQUE_OFFLINE_REGEX",
    ):
        value = environment.get(name)
        if value:
            try:
                re.compile(value)
            except re.error as exc:
                raise ValueError(f"{name} is not a valid regular expression: {exc}") from exc

    qcodes = environment.get("KOA_QEMU_NAVIGATION_KEYS", "")
    if qcodes:
        values = [item.strip().lower() for item in qcodes.split(",") if item.strip()]
        if (
            not values
            or len(values) > 8
            or any(re.fullmatch(r"[a-z0-9-]+", item) is None for item in values)
        ):
            raise ValueError(
                "KOA_QEMU_NAVIGATION_KEYS must contain one to eight comma-separated QEMU qcodes"
            )

    for name, value in (
        ("KOA_QEMU_ACTIVE_PROFILE", profile_value),
        (
            "KOA_QEMU_ACTIVE_RELEASE_SET",
            release_set_value if mediatheque_selection == "selected" else "",
        ),
    ):
        if value:
            path = Path(value).expanduser()
            if not path.is_file() or path.is_symlink():
                blocked.append(f"{name} must reference a regular file: {path}")

    if not blocked and image_value:
        harness_module = _load_qemu_harness(root)
        harness = harness_module.QemuHarness.from_file(root / "tests/system/qemu-machine.toml")
        try:
            harness.preflight(Path(image_value).expanduser())
        except harness_module.QemuBlockedError as exc:
            blocked.append(str(exc))
    return environment, blocked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument("--check-config", action="store_true")
    parser.add_argument("--scope", choices=("all", "local", "qemu"), default=os.environ.get("KOA_TEST_SCOPE", "all"))
    parser.add_argument("--qemu-image")
    parser.add_argument("--qemu-image-format", choices=("raw", "qcow2"))
    parser.add_argument("--qemu-active-profile")
    parser.add_argument("--qemu-navigation-surface-id")
    parser.add_argument("--qemu-navigation-ready-regex")
    parser.add_argument("--qemu-navigation-result-regex")
    parser.add_argument("--qemu-navigation-keys")
    parser.add_argument("--qemu-mediatheque-selection", choices=("selected", "not_selected"))
    parser.add_argument("--qemu-active-release-set")
    parser.add_argument("--qemu-mediatheque-artifact-ref")
    parser.add_argument("--qemu-mediatheque-offline-regex")
    args = parser.parse_args()

    root = args.repo_root.resolve()
    policy_value = args.policy or (Path(DEFAULT_POLICY) if DEFAULT_POLICY else None)
    policy = (
        None
        if policy_value is None
        else (policy_value if policy_value.is_absolute() else root / policy_value)
    )
    if policy and not policy.is_file():
        print(f"{SUITE_ID}: required policy is missing: {policy}", file=sys.stderr)
        return 2
    try:
        commands, required, policy_env, policy_digest = _build_commands(root, policy)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"{SUITE_ID}: invalid gate configuration: {exc}", file=sys.stderr)
        return 2

    commands, required, omitted = partition(root, commands, required, args.scope)
    qemu_required = any(is_qemu(command) for command in commands)
    if qemu_required:
        required = sorted(set([*required, *QEMU_SUPPORT_PATHS]))
    missing = sorted(path for path in required if not (root / path).exists())
    if args.check_config:
        print(
            json.dumps(
                {
                    "suite_id": SUITE_ID, "scope": args.scope, "omitted_commands": omitted, "full_gate": args.scope == "all",
                    "commands": commands,
                    "required_paths": required,
                    "missing_paths": missing,
                    "policy_digest": policy_digest,
                    "qemu_machine_validation": qemu_required,
                    "qemu_network": "disabled",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1 if missing else 0

    revision = os.environ.get("GITHUB_SHA") or _git(root, "rev-parse", "HEAD") or "unversioned"
    commit_time = (
        _git(root, "show", "-s", "--format=%cI", revision)
        if revision != "unversioned"
        else None
    )
    clean = (_git(root, "status", "--porcelain=v1", "--untracked-files=all") or "") == ""
    evidence_dir = args.evidence_dir or (
        Path(os.environ.get("KOA_CI_EVIDENCE_DIR", "/tmp/koa-ci-evidence")) / SUITE_ID
    )
    evidence_dir = evidence_dir.resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    qemu_environment: dict[str, str] = {}
    blocked_reasons: list[str] = []
    if qemu_required:
        try:
            qemu_environment, blocked_reasons = _qemu_runtime_environment(root, args)
        except (OSError, RuntimeError, ValueError) as exc:
            print(f"{SUITE_ID}: invalid QEMU validation configuration: {exc}", file=sys.stderr)
            blocked_reasons = [str(exc)]

    outcome = "blocked" if missing or blocked_reasons or not commands else "passed"
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            "PYTHONHASHSEED": environment.get("PYTHONHASHSEED", "0"),
            "PYTEST_ADDOPTS": " ".join(
                filter(None, [environment.get("PYTEST_ADDOPTS", ""), "-p no:cacheprovider"])
            ),
        }
    )
    environment.update(policy_env)
    environment.update(qemu_environment)

    if not [p for p in missing if p not in QEMU_SUPPORT_PATHS and not Path(p).name.startswith("test_qemu_")]:
        for argv in commands:
            if (blocked_reasons or missing) and is_qemu(argv):
                records.append({"argv": argv, "exit_code": None, "outcome": "blocked", "reasons": blocked_reasons})
                continue
            print(f"[{SUITE_ID}] $ {' '.join(argv)}", flush=True)
            try:
                result = subprocess.run(
                    argv,
                    cwd=root,
                    env=environment,
                    check=False,
                    timeout=COMMAND_TIMEOUT_SECONDS,
                )
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
            records.append(_command_record(argv, code))
            if code != 0:
                outcome = "failed"

    core = {
        "format_version": "1.0.0",
        "report_kind": "ci_gate_candidate_evidence",
        "authoritative": False,
        "suite_id": SUITE_ID, "scope": args.scope, "omitted_commands": omitted, "full_gate": args.scope == "all",
        "test_type": TEST_TYPE,
        "evidence_type": EVIDENCE_TYPE,
        "source_revision": revision,
        "source_recorded_at": commit_time,
        "repository_clean_before": clean,
        "policy_digest": policy_digest,
        "required_paths": required,
        "missing_paths": missing,
        "blocked_reasons": blocked_reasons,
        "commands": records,
        "outcome": outcome,
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.system().lower(),
            "machine": platform.machine().lower(),
            "qemu_network": "disabled" if qemu_required else "not_applicable",
        },
        "notes": [
            "This report is candidate CI evidence only.",
            "Offline QEMU validation always disables the VM network device.",
            "It does not authorize merge, release, signing, publication, or activation.",
        ],
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report_id = hashlib.sha256(canonical).hexdigest()
    report = {**core, "report_id": f"sha256:{report_id}"}
    output = evidence_dir / f"{SUITE_ID}-gate-report.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{SUITE_ID}: {outcome}; report={output}")
    return {"passed": 0, "failed": 1, "blocked": 2}[outcome]


if __name__ == "__main__":
    raise SystemExit(main())
