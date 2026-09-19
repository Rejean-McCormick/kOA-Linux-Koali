"""Validation of the frozen repository file architecture."""
from __future__ import annotations

import fnmatch
import subprocess
from pathlib import Path
from typing import Any, Iterable, Mapping

from . import (
    CheckResult,
    Finding,
    first_mapping,
    first_sequence,
    iter_repository_files,
    load_json_object,
    normalize_repository_path,
    repository_root,
)
from .dependencies import check_dependencies
from .generated_content import check_generated_content
from .path_ownership import check_path_ownership


DEFAULT_TOP_LEVEL_ROOTS = frozenset(
    {
        ".github",
        ".koa",
        "LICENSES",
        "assembly",
        "ci",
        "components",
        "dev",
        "docs",
        "generated",
        "host",
        "integrations",
        "interfaces",
        "operations",
        "packaging",
        "profiles",
        "release",
        "tests",
        "tools",
    }
)
DEFAULT_ROOT_FILES = frozenset(
    {
        ".editorconfig",
        ".gitattributes",
        ".gitignore",
        ".pre-commit-config.yaml",
        ".python-version",
        ".rustfmt.toml",
        "Cargo.lock",
        "Cargo.toml",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "NOTICE.md",
        "README.md",
        "REUSE.toml",
        "SECURITY.md",
        "pyproject.toml",
        "rust-toolchain.toml",
        "uv.lock",
    }
)


def _path_values(data: Mapping[str, Any]) -> tuple[list[str], list[Finding]]:
    findings: list[Finding] = []
    raw = first_sequence(data, ("paths", "files", "inventory", "entries"))
    values: list[str] = []
    if raw is not None:
        for index, item in enumerate(raw):
            if isinstance(item, str):
                value = item
            elif isinstance(item, dict):
                value = item.get("path") or item.get("file")
            else:
                value = None
            if not isinstance(value, str) or not value:
                findings.append(Finding("FILE_LOCK_ENTRY", f"entry {index} has no path", ".koa/file-architecture.lock.json"))
                continue
            try:
                values.append(normalize_repository_path(value))
            except ValueError as exc:
                findings.append(Finding("FILE_LOCK_PATH", f"entry {index}: {exc}", ".koa/file-architecture.lock.json"))
    else:
        mapping = first_mapping(data, ("path_metadata", "file_metadata"))
        if mapping is not None:
            for value in mapping:
                try:
                    values.append(normalize_repository_path(value))
                except ValueError as exc:
                    findings.append(Finding("FILE_LOCK_PATH", str(exc), ".koa/file-architecture.lock.json"))
        else:
            findings.append(Finding("FILE_LOCK_SHAPE", "lock must contain paths/files/inventory/entries or path_metadata", ".koa/file-architecture.lock.json"))
    duplicates = sorted({path for path in values if values.count(path) > 1})
    for path in duplicates:
        findings.append(Finding("FILE_LOCK_DUPLICATE", "path appears more than once in architecture lock", path))
    return sorted(set(values), key=str.casefold), findings


def _repository_allowlist(data: Mapping[str, Any] | None) -> tuple[set[str], set[str]]:
    if data is None:
        return set(DEFAULT_TOP_LEVEL_ROOTS), set(DEFAULT_ROOT_FILES)
    entries = data.get("allowed_top_level_entries")
    if isinstance(entries, list) and all(isinstance(item, str) for item in entries):
        allowed = set(entries)
        return allowed, allowed
    root_values = data.get("allowed_top_level_roots") or data.get("top_level_roots") or data.get("roots")
    file_values = data.get("allowed_root_files") or data.get("root_files")
    roots = set(root_values) if isinstance(root_values, list) and all(isinstance(item, str) for item in root_values) else set(DEFAULT_TOP_LEVEL_ROOTS)
    files = set(file_values) if isinstance(file_values, list) and all(isinstance(item, str) for item in file_values) else set(DEFAULT_ROOT_FILES)
    return roots, files


def _ignored_patterns(data: Mapping[str, Any]) -> tuple[str, ...]:
    values = data.get("ignored_paths") or data.get("ignore") or []
    if not isinstance(values, list):
        return ()
    result: list[str] = []
    for value in values:
        if isinstance(value, str):
            try:
                result.append(normalize_repository_path(value))
            except ValueError:
                continue
    return tuple(sorted(set(result)))


def _is_ignored(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) or path.startswith(pattern + "/") for pattern in patterns)




def _gitignore_pattern_matches(path: str, pattern: str) -> bool:
    """Best-effort Git-ignore matching used only when git check-ignore is unavailable."""

    directory_only = pattern.endswith("/")
    normalized = pattern.strip("/")
    if not normalized:
        return False

    path_parts = path.split("/")
    pattern_parts = normalized.split("/")

    if len(pattern_parts) == 1:
        candidates = path_parts[:-1] if directory_only else path_parts
        return any(fnmatch.fnmatchcase(part, normalized) for part in candidates)

    def match_parts(candidate: tuple[str, ...], wanted: tuple[str, ...]) -> bool:
        if not wanted:
            return not candidate
        if wanted[0] == "**":
            return match_parts(candidate, wanted[1:]) or (
                bool(candidate) and match_parts(candidate[1:], wanted)
            )
        return bool(candidate) and fnmatch.fnmatchcase(candidate[0], wanted[0]) and match_parts(
            candidate[1:], wanted[1:]
        )

    max_prefix = len(path_parts) - 1 if directory_only else len(path_parts)
    wanted = tuple(pattern_parts)
    return any(match_parts(tuple(path_parts[:size]), wanted) for size in range(1, max_prefix + 1))


def _fallback_gitignored_paths(base: Path, paths: Iterable[str]) -> set[str]:
    ignore_file = base / ".gitignore"
    try:
        lines = ignore_file.read_text(encoding="utf-8").splitlines()
    except OSError:
        return set()

    rules: list[tuple[str, bool]] = []
    for raw in lines:
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        negated = value.startswith("!")
        if negated:
            value = value[1:]
        if value:
            rules.append((value, negated))

    ignored: set[str] = set()
    for path in paths:
        state = False
        for pattern, negated in rules:
            if _gitignore_pattern_matches(path, pattern):
                state = not negated
        if state:
            ignored.add(path)
    return ignored


def _gitignored_paths(base: Path, paths: Iterable[str]) -> set[str]:
    """Return workspace paths excluded by the repository's .gitignore rules.

    ``git check-ignore --no-index`` evaluates ignore rules without using tracked-state
    cleanliness as a diagnostic gate. A small parser fallback keeps isolated unit tests
    deterministic when the temporary directory is not a Git repository.
    """

    candidates = tuple(sorted(set(paths), key=str.casefold))
    if not candidates or not (base / ".gitignore").is_file():
        return set()

    payload = b"\0".join(path.encode("utf-8") for path in candidates) + b"\0"
    try:
        result = subprocess.run(
            ["git", "-C", str(base), "check-ignore", "--no-index", "-z", "--stdin"],
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return _fallback_gitignored_paths(base, candidates)

    if result.returncode in (0, 1):
        return {
            normalize_repository_path(item.decode("utf-8"))
            for item in result.stdout.split(b"\0")
            if item
        }
    return _fallback_gitignored_paths(base, candidates)


def _check_symlink(base: Path, relative: str) -> Finding | None:
    path = base / relative
    if not path.is_symlink():
        return None
    try:
        resolved = path.resolve(strict=False)
        resolved.relative_to(base)
    except (OSError, ValueError):
        return Finding("FILE_SYMLINK_ESCAPE", "symbolic link escapes the repository root", relative)
    return None


def check_file_architecture(
    root: str | Path | None = None,
    *,
    include_related: bool = True,
    paths: Iterable[str] | None = None,
) -> CheckResult:
    """Compare committed paths with the frozen lock and enforce root structure."""

    base = repository_root(root)
    lock_data, findings = load_json_object(base / ".koa" / "file-architecture.lock.json", code_prefix="FILE_LOCK")
    repository_data, repository_findings = load_json_object(base / ".koa" / "repository.json", code_prefix="REPOSITORY_REGISTRY")
    findings.extend(repository_findings)
    if lock_data is None:
        return CheckResult.build("file-architecture", findings, {"actual_paths": 0, "expected_paths": 0})

    expected, lock_findings = _path_values(lock_data)
    findings.extend(lock_findings)
    ignored = _ignored_patterns(lock_data)
    expected_set = set(expected)
    discovered = {
        normalize_repository_path(path)
        for path in (paths if paths is not None else iter_repository_files(base))
    }
    gitignored = _gitignored_paths(base, discovered)
    actual = sorted(
        {
            path
            for path in discovered
            if path in expected_set or (path not in gitignored and not _is_ignored(path, ignored))
        },
        key=str.casefold,
    )
    actual_set = set(actual)
    for path in sorted(actual_set - expected_set, key=str.casefold):
        findings.append(Finding("FILE_UNKNOWN", "committed path is not present in the frozen architecture lock", path))
    for path in sorted(expected_set - actual_set, key=str.casefold):
        findings.append(Finding("FILE_MISSING", "path declared by the frozen architecture lock is missing", path))

    allowed_roots, allowed_root_files = _repository_allowlist(repository_data)
    for path in actual:
        root_name = path.split("/", 1)[0]
        if "/" in path:
            if root_name not in allowed_roots:
                findings.append(Finding("FILE_TOP_LEVEL_ROOT", f"unknown top-level root: {root_name}", path))
        elif path not in allowed_root_files:
            findings.append(Finding("FILE_ROOT_ENTRY", "unknown file at repository root", path))
        symlink_finding = _check_symlink(base, path)
        if symlink_finding:
            findings.append(symlink_finding)

    if include_related:
        related = (
            check_path_ownership(base, paths=actual),
            check_dependencies(base, paths=actual),
            # Generated documentation/build roots are intentionally outside the frozen
            # structural inventory. Validate them against the complete discovered tree
            # rather than the lock-filtered path set.
            check_generated_content(base, paths=discovered),
        )
        for result in related:
            findings.extend(result.findings)

    return CheckResult.build(
        "file-architecture",
        findings,
        {
            "actual_paths": len(actual),
            "expected_paths": len(expected),
            "related_checks": include_related,
        },
    )


check = check_file_architecture


__all__ = ["check", "check_file_architecture"]
