"""Immutable filesystem storage for Kristal artifacts and Runtime Packs.

The store verifies bounded package inventory and payload digests before an
atomic directory rename. It does not decide trust, compatibility, policy, or
activation eligibility; those authorities remain outside this adapter.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping

from ..application import ApplicationError, kristal_state_content_digest

_RUNTIME_ID = re.compile(r"^runtime-pack:[A-Za-z0-9][A-Za-z0-9._:/+-]*$")
_KRISTAL_ID = re.compile(r"^kristal-artifact\.[A-Za-z0-9][A-Za-z0-9._-]*$")
_KRISTAL_STATE_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
_VERSION = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
_DIGEST = re.compile(r"^(sha256:[0-9a-f]{64}|sha384:[0-9a-f]{96}|sha512:[0-9a-f]{128})$")
_RECORD_FORMAT = "koa-kristal-artifact-record/v1"


class ArtifactStoreError(RuntimeError):
    """Base failure for component-owned artifact storage."""


class InvalidArtifactError(ArtifactStoreError, ValueError):
    """The supplied artifact or payload inventory is invalid."""


class ArtifactConflictError(ArtifactStoreError):
    """An immutable artifact reference was reused with different bytes."""


class ArtifactNotFoundError(ArtifactStoreError):
    """The requested artifact is not present in the local store."""


class ArtifactIntegrityError(ArtifactStoreError):
    """Stored bytes no longer match their immutable record."""


class ArtifactStorageUnavailableError(ArtifactStoreError):
    """The owned filesystem store cannot be accessed safely."""


class ArtifactClass(StrEnum):
    RUNTIME_PACK = "runtime_pack"
    KRISTAL_STATE = "kristal_state"
    KRISTAL_ARTIFACT = "kristal_artifact"


@dataclass(frozen=True, slots=True)
class StoredArtifact:
    artifact_ref: str
    artifact_class: ArtifactClass
    artifact_identity: str
    artifact_version: str
    artifact_digest: str
    document_digest: str
    storage_key: str
    byte_length: int
    stored_at: datetime
    manifest_entries: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _Descriptor:
    artifact_class: ArtifactClass
    identity: str
    version: str
    digest: str
    entries: Mapping[str, tuple[str, int, bool]]

    @property
    def artifact_ref(self) -> str:
        return f"{self.identity}@{self.version}#{self.digest}"


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(
            dict(value), ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise InvalidArtifactError("artifact document must contain JSON-compatible values") from exc


def _utc(value: datetime, field: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise InvalidArtifactError(f"{field} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidArtifactError(f"{field} must be a non-empty string")
    return value.strip()


def _safe_relative(value: Any) -> str:
    text = _text(value, "manifest path")
    if len(text) > 1024 or text.startswith("/") or "//" in text or any(ord(ch) < 32 for ch in text):
        raise InvalidArtifactError(f"unsafe manifest path: {text!r}")
    path = PurePosixPath(text)
    if path.is_absolute() or ".." in path.parts or "." in path.parts or not path.parts:
        raise InvalidArtifactError(f"unsafe manifest path: {text!r}")
    return path.as_posix()


def _digest_bytes(data: bytes, claim: str) -> str:
    if not isinstance(claim, str) or not _DIGEST.fullmatch(claim):
        raise InvalidArtifactError(f"unsupported or invalid digest claim: {claim!r}")
    algorithm, expected = claim.split(":", 1)
    actual = hashlib.new(algorithm, data).hexdigest()
    if actual != expected:
        raise InvalidArtifactError(f"payload digest mismatch for {claim}")
    return claim


def _descriptor(document: Mapping[str, Any]) -> _Descriptor:
    artifact_class = document.get("artifact_class")
    if artifact_class == ArtifactClass.RUNTIME_PACK.value:
        identity = _text(document.get("artifact_identity"), "artifact_identity")
        if not _RUNTIME_ID.fullmatch(identity):
            raise InvalidArtifactError("artifact_identity is not a Runtime Pack identity")
        version = _text(document.get("artifact_version"), "artifact_version")
        if not _VERSION.fullmatch(version):
            raise InvalidArtifactError("Runtime Pack artifact_version must be semantic versioning")
        digest = _text(document.get("artifact_digest"), "artifact_digest")
        if not _DIGEST.fullmatch(digest):
            raise InvalidArtifactError("Runtime Pack artifact_digest is invalid")
        if document.get("release_channel") != "knowledge":
            raise InvalidArtifactError("Runtime Packs must use the knowledge release channel")
        if document.get("digest_scope") != "canonical_manifest_and_payload":
            raise InvalidArtifactError("Runtime Pack digest_scope is not supported")
        handling = document.get("content_handling")
        if not isinstance(handling, Mapping):
            raise InvalidArtifactError("Runtime Pack content_handling must be an object")
        if handling.get("unverified_execution_allowed") is not False:
            raise InvalidArtifactError("unverified Runtime Pack execution is prohibited")
        if handling.get("direct_cross_component_mutation_allowed") is not False:
            raise InvalidArtifactError("cross-component mutation is prohibited")
        if handling.get("secret_values_allowed") is not False:
            raise InvalidArtifactError("secret values are prohibited in Runtime Packs")
        manifest = document.get("manifest")
        digest_key = "digest"
        size_key = "size_bytes"
    elif document.get("artifact_type") == ArtifactClass.KRISTAL_STATE.value:
        artifact_class = ArtifactClass.KRISTAL_STATE.value
        identity = _text(document.get("state_id"), "state_id")
        if not _KRISTAL_STATE_ID.fullmatch(identity):
            raise InvalidArtifactError("state_id is not a Kristal v6 sha256 identity")
        version = _text(document.get("schema_version"), "schema_version")
        if version != "6.0":
            raise InvalidArtifactError("Kristal State schema_version must be 6.0")
        content_hash = document.get("content_hash")
        if not isinstance(content_hash, Mapping) or content_hash.get("alg") != "sha256":
            raise InvalidArtifactError("Kristal State content_hash must use sha256")
        raw_digest = _text(content_hash.get("value"), "content_hash.value")
        digest = f"sha256:{raw_digest}"
        if identity != digest or not _KRISTAL_STATE_ID.fullmatch(digest):
            raise InvalidArtifactError("Kristal State identity and content_hash must match")
        try:
            computed = kristal_state_content_digest(document)
        except ApplicationError as exc:
            raise InvalidArtifactError(str(exc)) from exc
        if raw_digest != computed:
            raise InvalidArtifactError("Kristal State content hash does not match RFC 8785 canonical content")
        return _Descriptor(ArtifactClass.KRISTAL_STATE, identity, version, digest, MappingProxyType({}))
    elif artifact_class == ArtifactClass.KRISTAL_ARTIFACT.value:
        identity = _text(document.get("artifact_id"), "artifact_id")
        if not _KRISTAL_ID.fullmatch(identity):
            raise InvalidArtifactError("artifact_id is not a Kristal artifact identity")
        version = _text(document.get("artifact_version"), "artifact_version")
        content_identity = document.get("content_identity")
        if not isinstance(content_identity, Mapping) or content_identity.get("algorithm") != "sha256":
            raise InvalidArtifactError("Kristal content_identity must use sha256")
        raw_digest = _text(content_identity.get("digest"), "content_identity.digest")
        digest = f"sha256:{raw_digest}"
        if not _DIGEST.fullmatch(digest):
            raise InvalidArtifactError("Kristal content identity digest is invalid")
        manifest = document.get("manifest")
        digest_key = "sha256"
        size_key = "size_bytes"
    else:
        raise InvalidArtifactError("unsupported artifact_class")
    if not isinstance(manifest, Mapping):
        raise InvalidArtifactError("manifest must be an object")
    raw_entries = manifest.get("entries")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise InvalidArtifactError("manifest entries must be a non-empty array")
    entries: dict[str, tuple[str, int, bool]] = {}
    for item in raw_entries:
        if not isinstance(item, Mapping):
            raise InvalidArtifactError("manifest entries must be objects")
        path = _safe_relative(item.get("path"))
        if path in entries:
            raise InvalidArtifactError(f"duplicate manifest path: {path}")
        claim = item.get(digest_key)
        if artifact_class == ArtifactClass.KRISTAL_ARTIFACT:
            claim = f"sha256:{_text(claim, f'{path}.sha256')}"
        claim = _text(claim, f"{path}.digest")
        if not _DIGEST.fullmatch(claim):
            raise InvalidArtifactError(f"invalid digest for {path}")
        raw_size = item.get(size_key)
        if raw_size is None and artifact_class == ArtifactClass.KRISTAL_ARTIFACT:
            raw_size = -1
        if not isinstance(raw_size, int) or isinstance(raw_size, bool) or raw_size < -1:
            raise InvalidArtifactError(f"invalid size for {path}")
        required = item.get("required", True)
        if not isinstance(required, bool):
            raise InvalidArtifactError(f"required must be boolean for {path}")
        entries[path] = (claim, raw_size, required)
    return _Descriptor(ArtifactClass(artifact_class), identity, version, digest, MappingProxyType(entries))


class FilesystemArtifactStore:
    """Store immutable artifact documents and payloads beneath one owned root."""

    def __init__(
        self,
        root: str | Path,
        *,
        max_artifact_bytes: int = 512 * 1024 * 1024,
        max_files: int = 20_000,
    ) -> None:
        if max_artifact_bytes <= 0 or max_files <= 0:
            raise ValueError("artifact limits must be positive")
        self._root = Path(root)
        self._objects = self._root / "objects"
        self._tmp = self._root / ".tmp"
        self._max_artifact_bytes = max_artifact_bytes
        self._max_files = max_files
        try:
            self._objects.mkdir(parents=True, exist_ok=True, mode=0o750)
            self._tmp.mkdir(parents=True, exist_ok=True, mode=0o750)
        except OSError as exc:
            raise ArtifactStorageUnavailableError(f"cannot initialize artifact store: {exc}") from exc

    @staticmethod
    def _storage_key(artifact_ref: str) -> str:
        return hashlib.sha256(artifact_ref.encode("utf-8")).hexdigest()

    def _object_dir(self, storage_key: str) -> Path:
        if not re.fullmatch(r"[0-9a-f]{64}", storage_key):
            raise InvalidArtifactError("storage_key is invalid")
        return self._objects / storage_key[:2] / storage_key

    def store(
        self,
        document: Mapping[str, Any],
        payloads: Mapping[str, bytes | bytearray | memoryview],
        *,
        stored_at: datetime,
    ) -> StoredArtifact:
        if not isinstance(document, Mapping) or not isinstance(payloads, Mapping):
            raise TypeError("document and payloads must be mappings")
        descriptor = _descriptor(document)
        normalized: dict[str, bytes] = {}
        total = 0
        if len(payloads) > self._max_files:
            raise InvalidArtifactError("artifact exceeds the configured file-count limit")
        for raw_path, raw_bytes in payloads.items():
            path = _safe_relative(raw_path)
            if path in normalized:
                raise InvalidArtifactError(f"duplicate payload path: {path}")
            if not isinstance(raw_bytes, (bytes, bytearray, memoryview)):
                raise InvalidArtifactError(f"payload {path} must be bytes-like")
            data = bytes(raw_bytes)
            total += len(data)
            if total > self._max_artifact_bytes:
                raise InvalidArtifactError("artifact exceeds the configured size limit")
            normalized[path] = data
        missing = sorted(path for path, (_, _, required) in descriptor.entries.items() if required and path not in normalized)
        extra = sorted(set(normalized) - set(descriptor.entries))
        if missing:
            raise InvalidArtifactError("missing required payloads: " + ", ".join(missing))
        if extra:
            raise InvalidArtifactError("payloads absent from manifest: " + ", ".join(extra))
        for path, data in normalized.items():
            claim, size, _ = descriptor.entries[path]
            if size >= 0 and len(data) != size:
                raise InvalidArtifactError(f"payload size mismatch for {path}")
            _digest_bytes(data, claim)
        document_bytes = _canonical_bytes(document)
        document_digest = "sha256:" + hashlib.sha256(document_bytes).hexdigest()
        storage_key = self._storage_key(descriptor.artifact_ref)
        target = self._object_dir(storage_key)
        when = _utc(stored_at, "stored_at")
        record = {
            "format": _RECORD_FORMAT,
            "artifact_ref": descriptor.artifact_ref,
            "artifact_class": descriptor.artifact_class.value,
            "artifact_identity": descriptor.identity,
            "artifact_version": descriptor.version,
            "artifact_digest": descriptor.digest,
            "document_digest": document_digest,
            "storage_key": storage_key,
            "byte_length": total,
            "stored_at": when.isoformat().replace("+00:00", "Z"),
            "manifest_entries": sorted(descriptor.entries),
        }
        record_bytes = _canonical_bytes(record)
        if target.exists():
            existing = self._read_record_file(target / "record.json")
            if existing != record or (target / "document.json").read_bytes() != document_bytes:
                raise ArtifactConflictError("immutable artifact reference already contains different data")
            self._verify_object(target, existing)
            return self._to_stored(existing)
        parent = target.parent
        parent.mkdir(parents=True, exist_ok=True, mode=0o750)
        temp_dir = Path(tempfile.mkdtemp(prefix=storage_key + ".", dir=self._tmp))
        try:
            (temp_dir / "payload").mkdir(mode=0o750)
            self._atomic_file(temp_dir / "document.json", document_bytes, 0o640)
            for path, data in normalized.items():
                destination = temp_dir / "payload" / Path(*PurePosixPath(path).parts)
                destination.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
                self._atomic_file(destination, data, 0o640)
            self._atomic_file(temp_dir / "record.json", record_bytes, 0o640)
            self._fsync_tree(temp_dir)
            try:
                os.rename(temp_dir, target)
            except FileExistsError:
                existing = self._read_record_file(target / "record.json")
                if existing != record:
                    raise ArtifactConflictError("concurrent immutable artifact conflict")
            self._fsync_directory(parent)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ArtifactStorageUnavailableError(f"cannot persist artifact: {exc}") from exc
        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
        return self.get(descriptor.artifact_ref)

    def get(self, artifact_ref: str) -> StoredArtifact:
        ref = _text(artifact_ref, "artifact_ref")
        target = self._object_dir(self._storage_key(ref))
        try:
            record = self._read_record_file(target / "record.json")
        except FileNotFoundError as exc:
            raise ArtifactNotFoundError(ref) from exc
        if record.get("artifact_ref") != ref:
            raise ArtifactIntegrityError("storage-key collision or record identity mismatch")
        self._verify_object(target, record)
        return self._to_stored(record)

    def read_document(self, artifact_ref: str) -> Mapping[str, Any]:
        stored = self.get(artifact_ref)
        path = self._object_dir(stored.storage_key) / "document.json"
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ArtifactIntegrityError(f"cannot read stored document: {exc}") from exc
        if not isinstance(value, dict):
            raise ArtifactIntegrityError("stored artifact document is not an object")
        return MappingProxyType(value)

    def read_payload(self, artifact_ref: str, relative_path: str) -> bytes:
        stored = self.get(artifact_ref)
        path = _safe_relative(relative_path)
        document = self.read_document(artifact_ref)
        descriptor = _descriptor(document)
        if path not in descriptor.entries:
            raise ArtifactNotFoundError(f"payload not declared: {path}")
        target = self._object_dir(stored.storage_key) / "payload" / Path(*PurePosixPath(path).parts)
        try:
            if target.is_symlink() or not target.is_file():
                raise ArtifactIntegrityError("payload path is not a regular file")
            data = target.read_bytes()
        except OSError as exc:
            raise ArtifactIntegrityError(f"cannot read payload: {exc}") from exc
        claim, size, _ = descriptor.entries[path]
        if size >= 0 and len(data) != size:
            raise ArtifactIntegrityError("stored payload size mismatch")
        try:
            _digest_bytes(data, claim)
        except InvalidArtifactError as exc:
            raise ArtifactIntegrityError(str(exc)) from exc
        return data

    def _verify_object(self, target: Path, record: Mapping[str, Any]) -> None:
        if record.get("format") != _RECORD_FORMAT:
            raise ArtifactIntegrityError("unknown artifact record format")
        if target.is_symlink() or not target.is_dir():
            raise ArtifactIntegrityError("artifact object is not a regular directory")
        try:
            document_bytes = (target / "document.json").read_bytes()
        except OSError as exc:
            raise ArtifactIntegrityError(f"cannot read artifact document: {exc}") from exc
        actual = "sha256:" + hashlib.sha256(document_bytes).hexdigest()
        if actual != record.get("document_digest"):
            raise ArtifactIntegrityError("artifact document digest mismatch")
        try:
            document = json.loads(document_bytes.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ArtifactIntegrityError("stored artifact document is invalid JSON") from exc
        if not isinstance(document, dict):
            raise ArtifactIntegrityError("stored artifact document is not an object")
        descriptor = _descriptor(document)
        if descriptor.artifact_ref != record.get("artifact_ref"):
            raise ArtifactIntegrityError("artifact document identity mismatch")
        for path in record.get("manifest_entries", []):
            self.read_payload_without_record(target, descriptor, path)

    @staticmethod
    def read_payload_without_record(target: Path, descriptor: _Descriptor, path: str) -> None:
        safe = _safe_relative(path)
        if safe not in descriptor.entries:
            raise ArtifactIntegrityError("record contains undeclared manifest entry")
        payload = target / "payload" / Path(*PurePosixPath(safe).parts)
        if not payload.is_file() or payload.is_symlink():
            if descriptor.entries[safe][2]:
                raise ArtifactIntegrityError(f"required stored payload missing: {safe}")
            return
        try:
            data = payload.read_bytes()
            claim, size, _ = descriptor.entries[safe]
            if size >= 0 and len(data) != size:
                raise ArtifactIntegrityError(f"stored payload size mismatch: {safe}")
            _digest_bytes(data, claim)
        except OSError as exc:
            raise ArtifactIntegrityError(f"cannot verify stored payload {safe}: {exc}") from exc
        except InvalidArtifactError as exc:
            raise ArtifactIntegrityError(str(exc)) from exc

    @staticmethod
    def _read_record_file(path: Path) -> dict[str, Any]:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ArtifactIntegrityError("artifact record is not an object")
        return value

    @staticmethod
    def _to_stored(record: Mapping[str, Any]) -> StoredArtifact:
        raw_time = _text(record.get("stored_at"), "stored_at")
        try:
            stored_at = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ArtifactIntegrityError("stored_at is invalid") from exc
        entries = record.get("manifest_entries")
        if not isinstance(entries, list) or not all(isinstance(item, str) for item in entries):
            raise ArtifactIntegrityError("manifest_entries is invalid")
        return StoredArtifact(
            artifact_ref=_text(record.get("artifact_ref"), "artifact_ref"),
            artifact_class=ArtifactClass(record.get("artifact_class")),
            artifact_identity=_text(record.get("artifact_identity"), "artifact_identity"),
            artifact_version=_text(record.get("artifact_version"), "artifact_version"),
            artifact_digest=_text(record.get("artifact_digest"), "artifact_digest"),
            document_digest=_text(record.get("document_digest"), "document_digest"),
            storage_key=_text(record.get("storage_key"), "storage_key"),
            byte_length=int(record.get("byte_length")),
            stored_at=stored_at.astimezone(timezone.utc),
            manifest_entries=tuple(entries),
        )

    @staticmethod
    def _atomic_file(path: Path, data: bytes, mode: int) -> None:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(path, flags, mode)
        try:
            with os.fdopen(fd, "wb", closefd=False) as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        finally:
            os.close(fd)

    @staticmethod
    def _fsync_directory(path: Path) -> None:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    @classmethod
    def _fsync_tree(cls, path: Path) -> None:
        for directory, _, _ in os.walk(path, topdown=False):
            cls._fsync_directory(Path(directory))
