"""Immutable Kristal and Runtime Pack artifact values.

The domain types in this module model only Kristal Runtime-owned facts.  Tenant
workflow, interface state, caches and deployment topology are deliberately
absent from content identity.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from hashlib import sha256
import math
import re
from typing import Iterable, Mapping, TypeAlias


class DomainValidationError(ValueError):
    """Raised when a Kristal domain value violates a declared invariant."""


JsonScalar: TypeAlias = None | bool | int | float | str


@dataclass(frozen=True, slots=True)
class FrozenObject:
    """Deterministically ordered immutable representation of a JSON object."""

    items: tuple[tuple[str, "FrozenJson"], ...]


FrozenJson: TypeAlias = JsonScalar | tuple["FrozenJson", ...] | FrozenObject

_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
_KRISTAL_ARTIFACT_ID = re.compile(r"^kristal-artifact\.[A-Za-z0-9][A-Za-z0-9._-]*$")
_RUNTIME_PACK_ID = re.compile(r"^runtime-pack:[A-Za-z0-9][A-Za-z0-9._:/+-]*$")
_CANONICAL_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_DIGEST = re.compile(r"^(?:sha256:[0-9a-f]{64}|sha384:[0-9a-f]{96}|sha512:[0-9a-f]{128})$")
_MEDIA_TYPE = re.compile(
    r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+"
    r"(?:\s*;\s*[A-Za-z0-9!#$&^_.+-]+=[A-Za-z0-9!#$&^_.+:/-]+)*$"
)
_SNAKE_ID = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
_VERSION_CONSTRAINT = re.compile(r"^[0-9A-Za-z.*<>=!~^|,\-+ ]+$")


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise DomainValidationError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise DomainValidationError(f"{field_name} must not be empty")
    if any(ord(character) < 32 for character in normalized):
        raise DomainValidationError(f"{field_name} must not contain control characters")
    return normalized


def _matching_text(value: str, field_name: str, pattern: re.Pattern[str]) -> str:
    normalized = _required_text(value, field_name)
    if pattern.fullmatch(normalized) is None:
        raise DomainValidationError(f"{field_name} has an invalid format")
    return normalized


def _semantic_version(value: str, field_name: str) -> str:
    return _matching_text(value, field_name, _SEMVER)


def _aware_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise DomainValidationError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise DomainValidationError(f"{field_name} must include a timezone")
    return value


def _safe_relative_path(value: str, field_name: str) -> str:
    normalized = _required_text(value, field_name)
    if normalized.startswith("/") or "//" in normalized:
        raise DomainValidationError(f"{field_name} must be a normalized relative path")
    parts = normalized.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise DomainValidationError(f"{field_name} contains an unsafe path segment")
    return normalized


def _unique_texts(
    values: Iterable[str],
    field_name: str,
    *,
    required: bool = False,
    pattern: re.Pattern[str] | None = None,
    preserve_order: bool = False,
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise DomainValidationError(f"{field_name} must be an iterable of strings")
    normalized = tuple(
        _matching_text(value, field_name, pattern)
        if pattern is not None
        else _required_text(value, field_name)
        for value in values
    )
    if required and not normalized:
        raise DomainValidationError(f"{field_name} must contain at least one value")
    if len(set(normalized)) != len(normalized):
        raise DomainValidationError(f"{field_name} must not contain duplicates")
    return normalized if preserve_order else tuple(sorted(normalized))


def _freeze_json(value: object, field_name: str = "value") -> FrozenJson:
    if isinstance(value, FrozenObject):
        return value
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise DomainValidationError(f"{field_name} must not contain non-finite numbers")
        return value
    if isinstance(value, datetime):
        return _aware_datetime(value, field_name).isoformat()
    if isinstance(value, Mapping):
        items: list[tuple[str, FrozenJson]] = []
        for key, nested in value.items():
            normalized_key = _required_text(key, f"{field_name} key")
            items.append((normalized_key, _freeze_json(nested, field_name)))
        keys = [key for key, _ in items]
        if len(set(keys)) != len(keys):
            raise DomainValidationError(f"{field_name} must not contain duplicate keys")
        return FrozenObject(tuple(sorted(items, key=lambda item: item[0])))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field_name) for item in value)
    if isinstance(value, (set, frozenset)):
        frozen = tuple(_freeze_json(item, field_name) for item in value)
        return tuple(sorted(frozen, key=repr))
    raise DomainValidationError(f"{field_name} must be JSON-compatible")


def _thaw_json(value: FrozenJson) -> object:
    if isinstance(value, FrozenObject):
        return {key: _thaw_json(nested) for key, nested in value.items}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


class ArtifactClass(StrEnum):
    """Artifact classes admitted by Kristal Runtime."""

    KRISTAL_STATE = "kristal_state"
    KRISTAL_ARTIFACT = "kristal_artifact"
    RUNTIME_PACK = "runtime_pack"


class RuntimePackLifecycle(StrEnum):
    """Lifecycle values owned by the Runtime Pack artifact contract."""

    CANDIDATE = "candidate"
    VERIFIED = "verified"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    REVOKED = "revoked"
    RETIRED = "retired"


class DisclosureVisibility(StrEnum):
    """Runtime Pack disclosure classes."""

    PUBLIC = "public"
    AUTHORIZED_INTERNAL = "authorized_internal"
    RESTRICTED = "restricted"


@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """Content-derived Kristal identity independent from operational context."""

    digest: str
    algorithm: str = "sha256"

    def __post_init__(self) -> None:
        if self.algorithm != "sha256":
            raise DomainValidationError("content identity algorithm must be sha256")
        object.__setattr__(self, "digest", _matching_text(self.digest, "digest", _SHA256))

    @classmethod
    def from_canonical_content(cls, content: bytes) -> "ContentIdentity":
        if not isinstance(content, bytes):
            raise DomainValidationError("canonical content must be bytes")
        return cls(sha256(content).hexdigest())

    def verifies(self, canonical_content: bytes) -> bool:
        return self == self.from_canonical_content(canonical_content)


@dataclass(frozen=True, slots=True)
class KristalManifestEntry:
    """One immutable file in a portable Kristal artifact."""

    path: str
    sha256: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", _safe_relative_path(self.path, "path"))
        object.__setattr__(self, "sha256", _matching_text(self.sha256, "sha256", _SHA256))


@dataclass(frozen=True, slots=True)
class ArtifactProvenance:
    """Minimum provenance required by the Kristal artifact contract."""

    source_refs: tuple[str, ...]
    producer: str
    build_receipt_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_refs", _unique_texts(self.source_refs, "source_refs", required=True))
        object.__setattr__(self, "producer", _required_text(self.producer, "producer"))
        if self.build_receipt_ref is not None:
            object.__setattr__(
                self,
                "build_receipt_ref",
                _required_text(self.build_receipt_ref, "build_receipt_ref"),
            )


@dataclass(frozen=True, slots=True)
class ArtifactRights:
    """Rights and audience declarations that travel with an artifact."""

    license: str
    audiences: tuple[str, ...] = ()
    restrictions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "license", _required_text(self.license, "license"))
        object.__setattr__(self, "audiences", _unique_texts(self.audiences, "audiences"))
        object.__setattr__(self, "restrictions", _unique_texts(self.restrictions, "restrictions"))


@dataclass(frozen=True, slots=True)
class ArtifactCompatibility:
    """Compatibility claims carried by a Kristal artifact."""

    kristal_runtime: str
    schema_versions: tuple[str, ...] = ()
    profile_constraints: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "kristal_runtime",
            _required_text(self.kristal_runtime, "kristal_runtime"),
        )
        object.__setattr__(
            self,
            "schema_versions",
            _unique_texts(self.schema_versions, "schema_versions"),
        )
        object.__setattr__(
            self,
            "profile_constraints",
            _unique_texts(self.profile_constraints, "profile_constraints"),
        )


@dataclass(frozen=True, slots=True)
class KristalArtifact:
    """Portable content-derived epistemic artifact."""

    artifact_id: str
    artifact_version: str
    content_identity: ContentIdentity
    manifest_entries: tuple[KristalManifestEntry, ...]
    provenance: ArtifactProvenance
    rights: ArtifactRights
    compatibility: ArtifactCompatibility
    query_contract_refs: tuple[str, ...] = ()
    signature_refs: tuple[str, ...] = ()
    metadata: FrozenJson = FrozenObject(())
    artifact_class: ArtifactClass = ArtifactClass.KRISTAL_ARTIFACT

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "artifact_id",
            _matching_text(self.artifact_id, "artifact_id", _KRISTAL_ARTIFACT_ID),
        )
        object.__setattr__(
            self,
            "artifact_version",
            _required_text(self.artifact_version, "artifact_version"),
        )
        if self.artifact_class is not ArtifactClass.KRISTAL_ARTIFACT:
            raise DomainValidationError("artifact_class must be kristal_artifact")
        if not self.manifest_entries:
            raise DomainValidationError("manifest_entries must contain at least one entry")
        paths = [entry.path for entry in self.manifest_entries]
        if len(set(paths)) != len(paths):
            raise DomainValidationError("manifest entry paths must be unique")
        object.__setattr__(
            self,
            "manifest_entries",
            tuple(sorted(self.manifest_entries, key=lambda entry: entry.path)),
        )
        object.__setattr__(
            self,
            "query_contract_refs",
            _unique_texts(self.query_contract_refs, "query_contract_refs"),
        )
        object.__setattr__(
            self,
            "signature_refs",
            _unique_texts(self.signature_refs, "signature_refs"),
        )
        object.__setattr__(self, "metadata", _freeze_json(self.metadata, "metadata"))

    def verifies_content(self, canonical_content: bytes) -> bool:
        """Verify content identity without considering tenant or UI state."""

        return self.content_identity.verifies(canonical_content)

    def as_dict(self) -> dict[str, object]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_version": self.artifact_version,
            "artifact_class": self.artifact_class.value,
            "content_identity": {
                "algorithm": self.content_identity.algorithm,
                "digest": self.content_identity.digest,
            },
            "manifest": {
                "entries": [
                    {"path": entry.path, "sha256": entry.sha256}
                    for entry in self.manifest_entries
                ],
                "query_contract_refs": list(self.query_contract_refs),
            },
            "provenance": {
                "source_refs": list(self.provenance.source_refs),
                "producer": self.provenance.producer,
                **(
                    {"build_receipt_ref": self.provenance.build_receipt_ref}
                    if self.provenance.build_receipt_ref is not None
                    else {}
                ),
            },
            "rights": {
                "license": self.rights.license,
                "audiences": list(self.rights.audiences),
                "restrictions": list(self.rights.restrictions),
            },
            "compatibility": {
                "kristal_runtime": self.compatibility.kristal_runtime,
                "schema_versions": list(self.compatibility.schema_versions),
                "profile_constraints": list(self.compatibility.profile_constraints),
            },
            "signatures": list(self.signature_refs),
            "metadata": _thaw_json(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class ArtifactLocator:
    """Stable locator for a Runtime Pack or related artifact."""

    artifact_identity: str
    artifact_version: str
    artifact_digest: str
    artifact_class: str = "runtime_pack"
    release_channel: str = "knowledge"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "artifact_identity",
            _matching_text(self.artifact_identity, "artifact_identity", _CANONICAL_ID),
        )
        object.__setattr__(
            self,
            "artifact_version",
            _required_text(self.artifact_version, "artifact_version"),
        )
        object.__setattr__(
            self,
            "artifact_digest",
            _matching_text(self.artifact_digest, "artifact_digest", _DIGEST),
        )
        object.__setattr__(self, "artifact_class", _matching_text(self.artifact_class, "artifact_class", _SNAKE_ID))
        if self.release_channel != "knowledge":
            raise DomainValidationError("Kristal artifacts must use the knowledge release channel")


@dataclass(frozen=True, slots=True)
class RuntimePackManifestEntry:
    """One bounded payload entry in a Runtime Pack manifest."""

    path: str
    role: str
    media_type: str
    digest: str
    size_bytes: int
    required: bool
    content_identity: str | None = None
    depends_on_paths: tuple[str, ...] = ()
    load_order: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", _safe_relative_path(self.path, "path"))
        object.__setattr__(self, "role", _matching_text(self.role, "role", _SNAKE_ID))
        object.__setattr__(self, "media_type", _matching_text(self.media_type, "media_type", _MEDIA_TYPE))
        object.__setattr__(self, "digest", _matching_text(self.digest, "digest", _DIGEST))
        if isinstance(self.size_bytes, bool) or not isinstance(self.size_bytes, int) or self.size_bytes < 0:
            raise DomainValidationError("size_bytes must be a non-negative integer")
        if not isinstance(self.required, bool):
            raise DomainValidationError("required must be a boolean")
        if self.content_identity is not None:
            object.__setattr__(
                self,
                "content_identity",
                _matching_text(self.content_identity, "content_identity", _CANONICAL_ID),
            )
        dependencies = tuple(
            _safe_relative_path(path, "depends_on_paths") for path in self.depends_on_paths
        )
        if len(set(dependencies)) != len(dependencies):
            raise DomainValidationError("depends_on_paths must not contain duplicates")
        if self.path in dependencies:
            raise DomainValidationError("manifest entry must not depend on itself")
        object.__setattr__(self, "depends_on_paths", tuple(sorted(dependencies)))
        if isinstance(self.load_order, bool) or not isinstance(self.load_order, int) or self.load_order < 0:
            raise DomainValidationError("load_order must be a non-negative integer")


@dataclass(frozen=True, slots=True)
class RuntimePackManifest:
    """Complete, uniquely addressed Runtime Pack inventory."""

    manifest_version: str
    manifest_digest: str
    entries: tuple[RuntimePackManifestEntry, ...]
    total_uncompressed_size_bytes: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "manifest_version", _semantic_version(self.manifest_version, "manifest_version"))
        object.__setattr__(self, "manifest_digest", _matching_text(self.manifest_digest, "manifest_digest", _DIGEST))
        if not self.entries:
            raise DomainValidationError("entries must contain at least one manifest entry")
        paths = [entry.path for entry in self.entries]
        if len(set(paths)) != len(paths):
            raise DomainValidationError("manifest entry paths must be unique")
        known_paths = set(paths)
        for entry in self.entries:
            missing = set(entry.depends_on_paths) - known_paths
            if missing:
                raise DomainValidationError(
                    f"manifest dependency paths are missing: {sorted(missing)!r}"
                )
        object.__setattr__(
            self,
            "entries",
            tuple(sorted(self.entries, key=lambda entry: (entry.load_order, entry.path))),
        )
        computed_size = sum(entry.size_bytes for entry in self.entries)
        if self.total_uncompressed_size_bytes is None:
            object.__setattr__(self, "total_uncompressed_size_bytes", computed_size)
        elif (
            isinstance(self.total_uncompressed_size_bytes, bool)
            or not isinstance(self.total_uncompressed_size_bytes, int)
            or self.total_uncompressed_size_bytes < computed_size
        ):
            raise DomainValidationError(
                "total_uncompressed_size_bytes must cover every manifest entry"
            )


@dataclass(frozen=True, slots=True)
class RuntimePackCompatibility:
    """Compatibility evidence required before activation eligibility."""

    runtime_api_version: str
    pack_format_version: str
    compatibility_evidence_refs: tuple[str, ...]
    supported_profile_ids: tuple[str, ...] = ()
    required_overlay_ids: tuple[str, ...] = ()
    prohibited_overlay_ids: tuple[str, ...] = ()
    target_component: str = "kristal_runtime"
    target_component_contract_ref: str = "contracts/components/kristal-runtime.component.json"

    def __post_init__(self) -> None:
        if self.target_component != "kristal_runtime":
            raise DomainValidationError("target_component must be kristal_runtime")
        if self.target_component_contract_ref != "contracts/components/kristal-runtime.component.json":
            raise DomainValidationError("target_component_contract_ref is not canonical")
        object.__setattr__(
            self,
            "runtime_api_version",
            _matching_text(self.runtime_api_version, "runtime_api_version", _VERSION_CONSTRAINT),
        )
        object.__setattr__(
            self,
            "pack_format_version",
            _semantic_version(self.pack_format_version, "pack_format_version"),
        )
        object.__setattr__(
            self,
            "compatibility_evidence_refs",
            _unique_texts(
                self.compatibility_evidence_refs,
                "compatibility_evidence_refs",
                required=True,
            ),
        )
        for field_name in (
            "supported_profile_ids",
            "required_overlay_ids",
            "prohibited_overlay_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _unique_texts(getattr(self, field_name), field_name, pattern=_SNAKE_ID),
            )
        overlap = set(self.required_overlay_ids) & set(self.prohibited_overlay_ids)
        if overlap:
            raise DomainValidationError(
                f"overlays cannot be both required and prohibited: {sorted(overlap)!r}"
            )


@dataclass(frozen=True, slots=True)
class RuntimePack:
    """Immutable Runtime Pack candidate or published artifact descriptor."""

    artifact_identity: str
    artifact_version: str
    lifecycle: RuntimePackLifecycle
    created_at: datetime
    artifact_digest: str
    provenance_refs: tuple[str, ...]
    compatibility: RuntimePackCompatibility
    manifest: RuntimePackManifest
    query_contract_refs: tuple[str, ...]
    reader_policy_refs: tuple[str, ...]
    visibility: DisclosureVisibility
    contains_personal_data: bool
    contains_restricted_content: bool
    signature_refs: tuple[str, ...] = ()
    supersedes: ArtifactLocator | None = None
    schema_version: str = "1.0.0"
    artifact_class: ArtifactClass = ArtifactClass.RUNTIME_PACK
    release_channel: str = "knowledge"
    digest_scope: str = "canonical_manifest_and_payload"

    def __post_init__(self) -> None:
        if self.schema_version != "1.0.0":
            raise DomainValidationError("schema_version must be 1.0.0")
        if self.artifact_class is not ArtifactClass.RUNTIME_PACK:
            raise DomainValidationError("artifact_class must be runtime_pack")
        object.__setattr__(
            self,
            "artifact_identity",
            _matching_text(self.artifact_identity, "artifact_identity", _RUNTIME_PACK_ID),
        )
        object.__setattr__(
            self,
            "artifact_version",
            _semantic_version(self.artifact_version, "artifact_version"),
        )
        try:
            lifecycle = RuntimePackLifecycle(self.lifecycle)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("lifecycle is not registered") from exc
        object.__setattr__(self, "lifecycle", lifecycle)
        object.__setattr__(self, "created_at", _aware_datetime(self.created_at, "created_at"))
        object.__setattr__(
            self,
            "artifact_digest",
            _matching_text(self.artifact_digest, "artifact_digest", _DIGEST),
        )
        if self.release_channel != "knowledge":
            raise DomainValidationError("Runtime Packs must use the knowledge release channel")
        if self.digest_scope != "canonical_manifest_and_payload":
            raise DomainValidationError("digest_scope must cover canonical manifest and payload")
        object.__setattr__(
            self,
            "provenance_refs",
            _unique_texts(self.provenance_refs, "provenance_refs", required=True),
        )
        object.__setattr__(
            self,
            "query_contract_refs",
            _unique_texts(self.query_contract_refs, "query_contract_refs", required=True),
        )
        object.__setattr__(
            self,
            "reader_policy_refs",
            _unique_texts(self.reader_policy_refs, "reader_policy_refs", required=True),
        )
        try:
            visibility = DisclosureVisibility(self.visibility)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("visibility is not registered") from exc
        object.__setattr__(self, "visibility", visibility)
        if not isinstance(self.contains_personal_data, bool):
            raise DomainValidationError("contains_personal_data must be a boolean")
        if not isinstance(self.contains_restricted_content, bool):
            raise DomainValidationError("contains_restricted_content must be a boolean")
        object.__setattr__(
            self,
            "signature_refs",
            _unique_texts(self.signature_refs, "signature_refs"),
        )
        if lifecycle in {
            RuntimePackLifecycle.PUBLISHED,
            RuntimePackLifecycle.DEPRECATED,
            RuntimePackLifecycle.SUPERSEDED,
            RuntimePackLifecycle.REVOKED,
            RuntimePackLifecycle.RETIRED,
        } and not self.signature_refs:
            raise DomainValidationError("published lifecycle states require signatures")
        if self.contains_restricted_content and visibility is DisclosureVisibility.PUBLIC:
            raise DomainValidationError("restricted content cannot be declared public")

    @property
    def locator(self) -> ArtifactLocator:
        return ArtifactLocator(
            artifact_identity=self.artifact_identity,
            artifact_version=self.artifact_version,
            artifact_digest=self.artifact_digest,
        )
