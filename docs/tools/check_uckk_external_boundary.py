#!/usr/bin/env python3
"""Validate directional interchange between the private kOA and online UCKK Mediatheques.

The check rejects UCKK-as-internal models, merged authority or storage, implicit
bidirectional synchronization, publication without Publication Gateway authority,
and import without quarantine and explicit local acceptance.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

TOOL_ID = "check_uckk_external_boundary"
TOOL_VERSION = "2.0.0"
META_RE = re.compile(
    r"\A<!-- KOA:DOC-META:BEGIN GENERATED\n(?P<payload>.*?)\nKOA:DOC-META:END -->",
    re.DOTALL,
)
INACTIVE = {"superseded", "retired", "deprecated", "archived"}
REQUIRED = (
    "contracts/components/koa-mediatheque.component.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/artifact-contracts/koa-media-record.schema.json",
    "contracts/artifact-contracts/uckk-publication-package.schema.json",
    "contracts/artifact-contracts/uckk-publication-receipt.schema.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "02-system/12-koa-mediatheque-system-boundary.md",
    "04-components/koa-mediatheque.md",
    "04-components/uckk-publication-bridge.md",
    "04-components/uckk-import-bridge.md",
)
PROHIBITED_ACTIVE_PATHS = (
    "contracts/subsystems/uckk.subsystem.json",
    "contracts/components/uckk-dimension-gateway.component.json",
    "contracts/artifact-contracts/uckk-media-reference.schema.json",
    "02-system/12-uckk-system-boundary.md",
    "04-components/subsystems/uckk.md",
    "04-components/subsystems/uckk-mediatheque.md",
    "04-components/uckk-dimension-gateway.md",
    "11-recipes/user-lightweight/uckk-mediatheque-local.md",
)
PROHIBITED_IDENTIFIERS = {
    "uckk_platform",
    "uckk-platform",
    "uckk_dimension_gateway",
    "uckk-dimension-gateway",
}
PROHIBITED_REFERENCES = {
    "contracts/subsystems/uckk.subsystem.json",
    "contracts/components/uckk-dimension-gateway.component.json",
    "contracts/artifact-contracts/uckk-media-reference.schema.json",
    "subsystems/uckk",
    "docs/subsystems/uckk",
}
PROHIBITED_PROSE = (
    re.compile(r"\bthe\s+(?:koa\s+)?mediatheque\s+is\s+native\s+to\s+uckk\b", re.I),
    re.compile(r"\buckk\s+is\s+an?\s+internal\s+(?:koa-linux\s+)?subsystem\b", re.I),
    re.compile(r"\buckk\s+platform\s+is\s+part\s+of\s+the\s+koa(?:-linux)?\s+runtime\b", re.I),
    re.compile(r"\buckk\s+owns\s+(?:the\s+)?local\s+koa\s+(?:media|files?)\b", re.I),
    re.compile(r"\b(?:automatic|implicit|background)\s+bidirectional\s+synchroni[sz]ation\s+(?:is\s+)?(?:enabled|required|the\s+default)\b", re.I),
    re.compile(r"\bshared\s+(?:authoritative\s+)?(?:database|storage)\s+between\s+(?:the\s+)?(?:koa|uckk)\s+mediatheques\b", re.I),
    re.compile(r"\bremote\s+uckk\s+(?:changes?|versions?)\s+automatically\s+overwrite\s+local\b", re.I),
)


@dataclass(frozen=True)
class Finding:
    path: str
    code: str
    message: str


def parse_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_metadata(path: Path) -> dict[str, Any] | None:
    match = META_RE.match(path.read_text(encoding="utf-8"))
    if not match:
        return None
    try:
        value = json.loads(match.group("payload"))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def active(path: Path) -> bool:
    if path.suffix.lower() == ".json":
        try:
            value = parse_json(path)
        except Exception:
            return True
        if isinstance(value, dict):
            return str(value.get("status", "active")).lower() not in INACTIVE
        return True
    if path.suffix.lower() == ".md":
        metadata = markdown_metadata(path)
        if metadata is None:
            return True
        return str(metadata.get("status", "active")).lower() not in INACTIVE
    return True


def walk_strings(value: Any, path: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


NEGATIVE_JSON_KEYS = {
    "deprecated_aliases",
    "forbidden_aliases",
    "prohibited_active_identifiers",
    "prohibited_identifiers",
    "prohibited_references",
    "prohibited_claims",
    "prohibited_assumptions",
    "non_responsibilities",
}


def walk_active_strings(value: Any, path: str = "$") -> Iterable[tuple[str, str]]:
    """Yield strings from active assertions, excluding retired and negative-policy objects."""
    if isinstance(value, dict):
        if str(value.get("status", "active")).lower() in INACTIVE:
            return
        for key, child in value.items():
            if key in NEGATIVE_JSON_KEYS:
                continue
            yield from walk_active_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_active_strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


def check_required(root: Path, findings: list[Finding]) -> None:
    for rel in REQUIRED:
        if not (root / rel).is_file():
            findings.append(Finding(rel, "REQUIRED_FILE_MISSING", "Required corrected-boundary source is missing."))


def check_prohibited_paths(root: Path, findings: list[Finding]) -> None:
    for rel in PROHIBITED_ACTIVE_PATHS:
        path = root / rel
        if path.exists() and active(path):
            findings.append(Finding(rel, "PROHIBITED_ACTIVE_SOURCE", "Obsolete UCKK-internal source remains active."))


def check_json_sources(root: Path, findings: list[Finding]) -> None:
    for path in sorted(root.rglob("*.json"), key=lambda p: p.as_posix().casefold()):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(("generated/", "finalization-reports/", "KOALI_MAJOR_UPDATE_SPEC_2026-09/")):
            continue
        try:
            value = parse_json(path)
        except Exception as exc:
            findings.append(Finding(rel, "JSON_INVALID", str(exc)))
            continue
        if not active(path):
            continue
        for json_path, text in walk_active_strings(value):
            if text in PROHIBITED_IDENTIFIERS:
                findings.append(Finding(rel, "PROHIBITED_INTERNAL_IDENTIFIER", f"{json_path} contains {text!r}."))
            normalized = text.replace("\\", "/").rstrip("/")
            if normalized in PROHIBITED_REFERENCES:
                findings.append(Finding(rel, "PROHIBITED_INTERNAL_REFERENCE", f"{json_path} contains {text!r}."))


NEGATIVE_CONTEXT_MARKERS = (
    "shall not", "must not", "does not", "do not", "cannot", "may not",
    "prohibited", "forbidden", "invalid", "incorrect", "reject", "rejected",
    "must reject", "validator", "detection pattern", "non-responsibil",
)
NEGATIVE_SECTION_MARKERS = (
    "prohibited", "forbidden", "invalid", "incorrect", "negative example",
    "non-responsibil", "rejected claim", "validation fixture", "detection",
)


def prose_claim_lines(text: str) -> Iterable[tuple[int, str]]:
    """Yield active prose lines while excluding code and explicit negative examples."""
    in_fence = False
    section = ""
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("#"):
            section = stripped.lstrip("#").strip().casefold()
            continue
        if not stripped or stripped.startswith("<!--") or stripped.startswith(">"):
            continue
        # Remove inline-code examples before prose matching.
        candidate = re.sub(r"`[^`]*`", "", raw)
        context = f"{section} {candidate}".casefold()
        if any(marker in context for marker in NEGATIVE_SECTION_MARKERS):
            continue
        if any(marker in candidate.casefold() for marker in NEGATIVE_CONTEXT_MARKERS):
            continue
        yield number, candidate


def check_markdown_sources(root: Path, findings: list[Finding]) -> None:
    for path in sorted(root.rglob("*.md"), key=lambda p: p.as_posix().casefold()):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(("generated/", "finalization-reports/", "KOALI_MAJOR_UPDATE_SPEC_2026-09/")):
            continue
        if not active(path):
            continue
        text = path.read_text(encoding="utf-8")
        metadata = markdown_metadata(path)
        if metadata:
            for json_path, value in walk_strings(metadata):
                if value in PROHIBITED_IDENTIFIERS:
                    findings.append(Finding(rel, "PROHIBITED_METADATA_IDENTIFIER", f"{json_path} contains {value!r}."))
                normalized = value.replace("\\", "/").rstrip("/")
                if normalized in PROHIBITED_REFERENCES:
                    findings.append(Finding(rel, "PROHIBITED_METADATA_REFERENCE", f"{json_path} contains {value!r}."))
        for line_number, line in prose_claim_lines(text):
            for pattern in PROHIBITED_PROSE:
                match = pattern.search(line)
                if match:
                    findings.append(Finding(rel, "PROHIBITED_OWNERSHIP_CLAIM", f"line {line_number}: {match.group(0)!r}"))


def check_corrected_contracts(root: Path, findings: list[Finding]) -> None:
    component_path = root / "contracts/components/koa-mediatheque.component.json"
    if component_path.is_file():
        try:
            component = parse_json(component_path)
            if component.get("component_id") != "koa_mediatheque":
                findings.append(Finding(component_path.relative_to(root).as_posix(), "COMPONENT_ID_INVALID", "component_id must be koa_mediatheque."))
            prohibited = " ".join(str(x) for x in component.get("non_responsibilities", []))
            if "Operating or administering UCKK" not in prohibited:
                findings.append(Finding(component_path.relative_to(root).as_posix(), "EXTERNAL_BOUNDARY_NOT_EXPLICIT", "Contract must explicitly exclude operating UCKK."))
        except Exception as exc:
            findings.append(Finding(component_path.relative_to(root).as_posix(), "COMPONENT_CONTRACT_INVALID", str(exc)))

    integration_path = root / "contracts/integrations/uckk-publication.integration.json"
    if integration_path.is_file():
        try:
            integration = parse_json(integration_path)
            external = integration.get("external_system", {})
            boundary = integration.get("boundary", {})
            expected = {
                "integration_id": integration.get("integration_id") == "uckk-publication",
                "authority": integration.get("authority") == "non_authoritative",
                "inside_koa_linux": external.get("inside_koa_linux") is False,
                "owns_local_koa_media": external.get("owns_local_koa_media") is False,
                "shared_database": boundary.get("shared_database") is False,
                "direct_database_write": boundary.get("direct_database_write") is False,
                "implicit_bidirectional_sync": boundary.get("implicit_bidirectional_sync") is False,
                "source_authority_preserved": boundary.get("source_authority_preserved") is True,
            }
            for field, ok in expected.items():
                if not ok:
                    findings.append(Finding(integration_path.relative_to(root).as_posix(), "INTEGRATION_BOUNDARY_INVALID", f"Required boundary assertion failed: {field}."))
        except Exception as exc:
            findings.append(Finding(integration_path.relative_to(root).as_posix(), "INTEGRATION_CONTRACT_INVALID", str(exc)))

    import_path = root / "contracts/integrations/uckk-import.integration.json"
    if import_path.is_file():
        try:
            integration = parse_json(import_path)
            external = integration.get("external_system", {})
            boundary = integration.get("boundary", {})
            model = integration.get("import_model", {})
            expected = {
                "integration_id": integration.get("integration_id") == "uckk-import",
                "direction": integration.get("direction") == "inbound_import",
                "authority": integration.get("authority") == "non_authoritative",
                "inside_koa_linux": external.get("inside_koa_linux") is False,
                "owns_local_koa_media": external.get("owns_local_koa_media") is False,
                "shared_database": boundary.get("shared_database") is False,
                "direct_database_write": boundary.get("direct_database_write") is False,
                "implicit_bidirectional_sync": boundary.get("implicit_bidirectional_sync") is False,
                "remote_overwrite": boundary.get("remote_change_implies_local_overwrite") is False,
                "source_authority_preserved": boundary.get("source_authority_preserved") is True,
                "local_copy_authority_separate": boundary.get("local_copy_authority_separate") is True,
                "quarantine": model.get("quarantine") == "required before local acceptance",
            }
            for field, ok in expected.items():
                if not ok:
                    findings.append(Finding(import_path.relative_to(root).as_posix(), "IMPORT_BOUNDARY_INVALID", f"Required boundary assertion failed: {field}."))
        except Exception as exc:
            findings.append(Finding(import_path.relative_to(root).as_posix(), "IMPORT_CONTRACT_INVALID", str(exc)))

    frame_path = root / "contracts/artifact-contracts/shared-mediatheque-frame.schema.json"
    if frame_path.is_file():
        try:
            frame = parse_json(frame_path)
            props = frame.get("properties", {})
            if props.get("frame_id", {}).get("const") != "koa-uckk-shared-mediatheque-frame":
                findings.append(Finding(frame_path.relative_to(root).as_posix(), "SHARED_FRAME_INVALID", "frame_id constant is missing or incorrect."))
            required = set(frame.get("required", []))
            for field in {"object_identity", "version_identity", "integrity", "media", "rights", "provenance", "lifecycle"}:
                if field not in required:
                    findings.append(Finding(frame_path.relative_to(root).as_posix(), "SHARED_FRAME_INVALID", f"Required shared-frame field is missing: {field}."))
        except Exception as exc:
            findings.append(Finding(frame_path.relative_to(root).as_posix(), "SHARED_FRAME_INVALID", str(exc)))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the kOA and UCKK Mediatheque directional interchange boundary")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", help="Emit a JSON result")
    args = parser.parse_args()
    root = args.root.resolve()
    findings: list[Finding] = []

    check_required(root, findings)
    check_prohibited_paths(root, findings)
    check_json_sources(root, findings)
    check_markdown_sources(root, findings)
    check_corrected_contracts(root, findings)

    if args.json:
        print(json.dumps({
            "tool_id": TOOL_ID,
            "tool_version": TOOL_VERSION,
            "root": root.as_posix(),
            "outcome": "fail" if findings else "pass",
            "findings": [asdict(f) for f in findings],
        }, indent=2))
    else:
        for finding in findings:
            print(f"FAIL: {finding.path}: {finding.code}: {finding.message}")
        print(f"{TOOL_ID}: {'fail' if findings else 'pass'}; findings={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
