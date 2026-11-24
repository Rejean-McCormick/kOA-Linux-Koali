from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
INVENTORY_DOCS = [
    "docs/02-system/code-and-filesystem-architecture/24-repository-root-and-documentation.md",
    "docs/02-system/code-and-filesystem-architecture/25-internal-components-node-trust-governance.md",
    "docs/02-system/code-and-filesystem-architecture/26-internal-components-data-publication-and-knowledge.md",
    "docs/02-system/code-and-filesystem-architecture/27-independent-subsystem-integrations.md",
    "docs/02-system/code-and-filesystem-architecture/28-uckk-external-services-and-transport-interfaces.md",
    "docs/02-system/code-and-filesystem-architecture/29-host-platform-files.md",
    "docs/02-system/code-and-filesystem-architecture/30-assembly-profiles-packaging-and-release.md",
    "docs/02-system/code-and-filesystem-architecture/31-operations-tests-tools-development-and-ci.md",
]


def inventory_paths(repository: Path) -> list[str]:
    paths: list[str] = []
    for relative in INVENTORY_DOCS:
        document = repository / relative
        in_fence = False
        for line in document.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            is_path = ("/" in stripped or stripped.startswith(".") or re.fullmatch(r"[A-Za-z0-9_.-]+\.[A-Za-z0-9_.-]+", stripped))
            if (
                in_fence
                and stripped
                and " " not in stripped
                and not stripped.endswith("/")
                and not any(char in stripped for char in "├└│")
                and is_path
            ):
                paths.append(stripped)
    return paths


def _lock_paths(value: Any, key: str = "") -> set[str]:
    result: set[str] = set()
    if isinstance(value, dict):
        for child_key, child in value.items():
            result.update(_lock_paths(child, str(child_key)))
    elif isinstance(value, list):
        for child in value:
            result.update(_lock_paths(child, key))
    elif isinstance(value, str) and key.lower() in {"path", "file", "relative_path"}:
        result.add(value.strip("/"))
    return result


def test_frozen_inventory_contains_1145_unique_paths() -> None:
    paths = inventory_paths(ROOT)
    assert len(paths) == 1145
    assert len(set(paths)) == len(paths)


def test_inventory_contains_all_ten_tests_from_this_bundle() -> None:
    paths = set(inventory_paths(ROOT))
    expected = {
        "tests/boundaries/test_generated_roots.py",
        "tests/boundaries/test_no_cross_database_writes.py",
        "tests/boundaries/test_no_private_component_imports.py",
        "tests/boundaries/test_no_vendored_subsystems.py",
        "tests/boundaries/test_path_ownership.py",
        "tests/boundaries/test_ui_has_no_privileged_access.py",
        "tests/conformance/test_filesystem_architecture.py",
        "tests/conformance/test_profile_claims.py",
        "tests/conformance/test_release_evidence.py",
        "tests/conformance/test_requirement_traceability.py",
    }
    assert expected <= paths


def test_machine_lock_matches_normative_inventory() -> None:
    lock = ROOT / ".koa" / "file-architecture.lock.json"
    if not lock.is_file():
        pytest.skip("B-0010 file-architecture lock is not present")
    data = json.loads(lock.read_text(encoding="utf-8"))
    locked = _lock_paths(data)
    if isinstance(data, dict) and isinstance(data.get("paths"), list):
        locked.update(item for item in data["paths"] if isinstance(item, str))
    assert locked == set(inventory_paths(ROOT))


def test_duplicate_inventory_entry_is_detectable(tmp_path: Path) -> None:
    relative = INVENTORY_DOCS[0]
    document = tmp_path / relative
    document.parent.mkdir(parents=True)
    document.write_text("```text\na/b.py\na/b.py\n```\n", encoding="utf-8")
    for other in INVENTORY_DOCS[1:]:
        path = tmp_path / other
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
    paths = inventory_paths(tmp_path)
    assert len(paths) != len(set(paths))
