"""SQLite persistence for Kristal Runtime owned indexes and transitions."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterator, Mapping, Sequence


class IndexStoreError(RuntimeError):
    """Base error for Kristal Runtime index persistence."""


class InvalidIndexRecord(IndexStoreError, ValueError):
    """A supplied record violates a local storage invariant."""


class IndexConflictError(IndexStoreError):
    """An idempotency or immutable identity conflict occurred."""


class IndexRecordNotFound(IndexStoreError):
    """A requested local record does not exist."""


class IndexStorageUnavailable(IndexStoreError):
    """SQLite storage could not complete safely."""


class ArtifactDisposition(StrEnum):
    STAGED = "staged"
    QUARANTINED = "quarantined"
    VERIFIED = "verified"
    REJECTED = "rejected"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"


class VerificationOutcome(StrEnum):
    VERIFIED = "verified"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    FAILED = "failed"


class TransitionOutcome(StrEnum):
    ACTIVATED = "activated"
    ROLLED_BACK = "rolled_back"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ArtifactIndexRecord:
    artifact_ref: str
    artifact_class: str
    artifact_identity: str
    artifact_version: str
    artifact_digest: str
    document_digest: str
    storage_key: str
    byte_length: int
    disposition: ArtifactDisposition
    verification_id: str | None
    registered_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class VerificationRecord:
    verification_id: str
    request_id: str
    correlation_id: str
    artifact_ref: str
    outcome: VerificationOutcome
    activation_eligible: bool
    checks: Mapping[str, Any]
    reason_codes: tuple[str, ...]
    identity_receipt_ref: str | None
    policy_receipt_ref: str | None
    receipt_ref: str
    recorded_at: datetime


@dataclass(frozen=True, slots=True)
class ActivationRecord:
    transition_id: str
    request_id: str
    correlation_id: str
    operation: str
    outcome: TransitionOutcome
    candidate_artifact_ref: str | None
    previous_artifact_ref: str | None
    resulting_artifact_ref: str | None
    verification_id: str | None
    authorization_ref: str | None
    resource_grant_ref: str | None
    receipt_ref: str
    reason_codes: tuple[str, ...]
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class RuntimeState:
    active_artifact_ref: str | None
    previous_artifact_ref: str | None
    revision: int
    last_transition_id: str | None
    updated_at: datetime | None


def _text(value: Any, field: str, *, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str) or not value.strip():
        raise InvalidIndexRecord(f"{field} must be a non-empty string")
    return value.strip()


def _utc(value: datetime, field: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise InvalidIndexRecord(f"{field} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _timestamp(value: datetime, field: str) -> str:
    return _utc(value, field).isoformat().replace("+00:00", "Z")


def _parse_time(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise IndexStorageUnavailable("stored timestamp is invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise IndexStorageUnavailable("stored timestamp lacks timezone")
    return parsed.astimezone(timezone.utc)


def _canonical(value: Mapping[str, Any]) -> tuple[str, str]:
    try:
        raw = json.dumps(dict(value), ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise InvalidIndexRecord("record must contain JSON-compatible values") from exc
    return raw, "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _reason_codes(values: Sequence[str]) -> tuple[str, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise InvalidIndexRecord("reason_codes must be an array")
    result = tuple(_text(item, "reason_code") for item in values)
    if len(result) != len(set(result)):
        raise InvalidIndexRecord("reason_codes must not contain duplicates")
    return result  # type: ignore[return-value]


class SQLiteIndexStore:
    """Persist only Kristal Runtime authoritative state and rebuildable indexes."""

    def __init__(self, database_path: str | Path, *, busy_timeout_ms: int = 5000) -> None:
        if busy_timeout_ms <= 0:
            raise ValueError("busy_timeout_ms must be positive")
        self._path = Path(database_path)
        self._busy_timeout_ms = busy_timeout_ms
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
        except OSError as exc:
            raise IndexStorageUnavailable(f"cannot create database directory: {exc}") from exc

    def initialize(self, migration_path: str | Path) -> None:
        try:
            script = Path(migration_path).read_text(encoding="utf-8")
            connection = self._connect()
            try:
                connection.executescript(script)
            except sqlite3.Error:
                if connection.in_transaction:
                    connection.rollback()
                raise
            finally:
                connection.close()
        except (OSError, UnicodeError, sqlite3.Error) as exc:
            raise IndexStorageUnavailable(f"cannot initialize index store: {exc}") from exc

    def register_artifact(
        self,
        *,
        artifact_ref: str,
        artifact_class: str,
        artifact_identity: str,
        artifact_version: str,
        artifact_digest: str,
        document_digest: str,
        storage_key: str,
        byte_length: int,
        registered_at: datetime,
        disposition: ArtifactDisposition = ArtifactDisposition.STAGED,
    ) -> ArtifactIndexRecord:
        if artifact_class not in {"runtime_pack", "kristal_state", "kristal_artifact"}:
            raise InvalidIndexRecord("unsupported artifact_class")
        if not isinstance(byte_length, int) or isinstance(byte_length, bool) or byte_length < 0:
            raise InvalidIndexRecord("byte_length must be a non-negative integer")
        when = _timestamp(registered_at, "registered_at")
        values = (
            _text(artifact_ref, "artifact_ref"), artifact_class,
            _text(artifact_identity, "artifact_identity"), _text(artifact_version, "artifact_version"),
            _text(artifact_digest, "artifact_digest"), _text(document_digest, "document_digest"),
            _text(storage_key, "storage_key"), byte_length, ArtifactDisposition(disposition).value, when, when,
        )
        with self._transaction() as connection:
            existing = connection.execute("SELECT * FROM artifacts WHERE artifact_ref = ?", (values[0],)).fetchone()
            if existing is not None:
                immutable = (existing["artifact_class"], existing["artifact_identity"], existing["artifact_version"], existing["artifact_digest"], existing["document_digest"], existing["storage_key"], existing["byte_length"])
                supplied = (values[1], values[2], values[3], values[4], values[5], values[6], values[7])
                if immutable != supplied:
                    raise IndexConflictError("artifact_ref was reused with different immutable metadata")
                return self._artifact(existing)
            try:
                connection.execute(
                    """INSERT INTO artifacts(
                        artifact_ref, artifact_class, artifact_identity, artifact_version,
                        artifact_digest, document_digest, storage_key, byte_length,
                        disposition, registered_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", values,
                )
            except sqlite3.IntegrityError as exc:
                raise IndexConflictError(f"artifact identity conflict: {exc}") from exc
            row = connection.execute("SELECT * FROM artifacts WHERE artifact_ref = ?", (values[0],)).fetchone()
            return self._artifact(row)

    def get_artifact(self, artifact_ref: str) -> ArtifactIndexRecord:
        with self._read() as connection:
            row = connection.execute("SELECT * FROM artifacts WHERE artifact_ref = ?", (_text(artifact_ref, "artifact_ref"),)).fetchone()
            if row is None:
                raise IndexRecordNotFound(str(artifact_ref))
            return self._artifact(row)

    def record_verification(
        self,
        *,
        verification_id: str,
        request_id: str,
        correlation_id: str,
        artifact_ref: str,
        outcome: VerificationOutcome,
        activation_eligible: bool,
        checks: Mapping[str, Any],
        reason_codes: Sequence[str],
        receipt_ref: str,
        recorded_at: datetime,
        identity_receipt_ref: str | None = None,
        policy_receipt_ref: str | None = None,
    ) -> VerificationRecord:
        result = VerificationOutcome(outcome)
        if not isinstance(activation_eligible, bool):
            raise InvalidIndexRecord("activation_eligible must be boolean")
        if result is not VerificationOutcome.VERIFIED and activation_eligible:
            raise InvalidIndexRecord("only verified artifacts can be activation eligible")
        if not isinstance(checks, Mapping) or not checks:
            raise InvalidIndexRecord("checks must be a non-empty object")
        reasons = _reason_codes(reason_codes)
        if result is not VerificationOutcome.VERIFIED and not reasons:
            raise InvalidIndexRecord("non-verified outcomes require reason_codes")
        checks_json, _ = _canonical(checks)
        payload = {
            "verification_id": _text(verification_id, "verification_id"),
            "request_id": _text(request_id, "request_id"),
            "correlation_id": _text(correlation_id, "correlation_id"),
            "artifact_ref": _text(artifact_ref, "artifact_ref"),
            "outcome": result.value,
            "activation_eligible": activation_eligible,
            "checks": dict(checks),
            "reason_codes": list(reasons),
            "identity_receipt_ref": _text(identity_receipt_ref, "identity_receipt_ref", optional=True),
            "policy_receipt_ref": _text(policy_receipt_ref, "policy_receipt_ref", optional=True),
            "receipt_ref": _text(receipt_ref, "receipt_ref"),
            "recorded_at": _timestamp(recorded_at, "recorded_at"),
        }
        _, canonical_digest = _canonical(payload)
        with self._transaction() as connection:
            artifact = connection.execute("SELECT * FROM artifacts WHERE artifact_ref = ?", (payload["artifact_ref"],)).fetchone()
            if artifact is None:
                raise IndexRecordNotFound(str(payload["artifact_ref"]))
            existing = connection.execute("SELECT * FROM verification_records WHERE request_id = ?", (payload["request_id"],)).fetchone()
            if existing is not None:
                if existing["canonical_digest"] != canonical_digest:
                    raise IndexConflictError("verification request_id was reused with different semantics")
                return self._verification(existing)
            connection.execute(
                """INSERT INTO verification_records(
                    verification_id, request_id, correlation_id, artifact_ref, outcome,
                    activation_eligible, checks_json, reason_codes_json, identity_receipt_ref,
                    policy_receipt_ref, receipt_ref, recorded_at, canonical_digest
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    payload["verification_id"], payload["request_id"], payload["correlation_id"],
                    payload["artifact_ref"], payload["outcome"], int(activation_eligible), checks_json,
                    json.dumps(list(reasons), separators=(",", ":")), payload["identity_receipt_ref"],
                    payload["policy_receipt_ref"], payload["receipt_ref"], payload["recorded_at"], canonical_digest,
                ),
            )
            disposition = ArtifactDisposition.VERIFIED.value if result is VerificationOutcome.VERIFIED else (
                ArtifactDisposition.REJECTED.value if result is VerificationOutcome.REJECTED else ArtifactDisposition.QUARANTINED.value
            )
            connection.execute(
                "UPDATE artifacts SET disposition = ?, verification_id = ?, updated_at = ? WHERE artifact_ref = ?",
                (disposition, payload["verification_id"], payload["recorded_at"], payload["artifact_ref"]),
            )
            row = connection.execute("SELECT * FROM verification_records WHERE verification_id = ?", (payload["verification_id"],)).fetchone()
            return self._verification(row)

    def get_verification(self, verification_id: str) -> VerificationRecord:
        with self._read() as connection:
            row = connection.execute("SELECT * FROM verification_records WHERE verification_id = ?", (_text(verification_id, "verification_id"),)).fetchone()
            if row is None:
                raise IndexRecordNotFound(str(verification_id))
            return self._verification(row)

    def activate(
        self,
        *,
        transition_id: str,
        request_id: str,
        correlation_id: str,
        artifact_ref: str,
        verification_id: str,
        authorization_ref: str,
        resource_grant_ref: str,
        receipt_ref: str,
        occurred_at: datetime,
    ) -> ActivationRecord:
        return self._switch(
            operation="activate", expected_outcome=TransitionOutcome.ACTIVATED,
            transition_id=transition_id, request_id=request_id, correlation_id=correlation_id,
            target_ref=artifact_ref, verification_id=verification_id,
            authorization_ref=authorization_ref, resource_grant_ref=resource_grant_ref,
            receipt_ref=receipt_ref, occurred_at=occurred_at,
        )

    def rollback(
        self,
        *,
        transition_id: str,
        request_id: str,
        correlation_id: str,
        target_artifact_ref: str,
        verification_id: str,
        authorization_ref: str,
        receipt_ref: str,
        occurred_at: datetime,
    ) -> ActivationRecord:
        return self._switch(
            operation="rollback", expected_outcome=TransitionOutcome.ROLLED_BACK,
            transition_id=transition_id, request_id=request_id, correlation_id=correlation_id,
            target_ref=target_artifact_ref, verification_id=verification_id,
            authorization_ref=authorization_ref, resource_grant_ref=None,
            receipt_ref=receipt_ref, occurred_at=occurred_at,
        )

    def _switch(
        self, *, operation: str, expected_outcome: TransitionOutcome, transition_id: str,
        request_id: str, correlation_id: str, target_ref: str, verification_id: str,
        authorization_ref: str, resource_grant_ref: str | None, receipt_ref: str,
        occurred_at: datetime,
    ) -> ActivationRecord:
        payload = {
            "transition_id": _text(transition_id, "transition_id"),
            "request_id": _text(request_id, "request_id"),
            "correlation_id": _text(correlation_id, "correlation_id"),
            "operation": operation,
            "target_ref": _text(target_ref, "target_ref"),
            "verification_id": _text(verification_id, "verification_id"),
            "authorization_ref": _text(authorization_ref, "authorization_ref"),
            "resource_grant_ref": _text(resource_grant_ref, "resource_grant_ref", optional=True),
            "receipt_ref": _text(receipt_ref, "receipt_ref"),
            "occurred_at": _timestamp(occurred_at, "occurred_at"),
        }
        _, canonical_digest = _canonical(payload)
        with self._transaction() as connection:
            existing = connection.execute("SELECT * FROM activation_records WHERE request_id = ?", (payload["request_id"],)).fetchone()
            if existing is not None:
                if existing["canonical_digest"] != canonical_digest:
                    raise IndexConflictError("transition request_id was reused with different semantics")
                return self._activation(existing)
            state = connection.execute("SELECT * FROM runtime_state WHERE singleton_id = 1").fetchone()
            target = connection.execute("SELECT * FROM artifacts WHERE artifact_ref = ?", (payload["target_ref"],)).fetchone()
            if target is None:
                raise IndexRecordNotFound(str(payload["target_ref"]))
            if target["artifact_class"] != "runtime_pack" or target["disposition"] != ArtifactDisposition.VERIFIED.value:
                raise InvalidIndexRecord("only a verified Runtime Pack can become active")
            verification = connection.execute("SELECT * FROM verification_records WHERE verification_id = ?", (payload["verification_id"],)).fetchone()
            if verification is None or verification["artifact_ref"] != payload["target_ref"] or verification["outcome"] != VerificationOutcome.VERIFIED.value or not verification["activation_eligible"]:
                raise InvalidIndexRecord("activation requires the matching eligible verification record")
            current = state["active_artifact_ref"]
            previous = state["previous_artifact_ref"]
            if operation == "activate":
                if current == payload["target_ref"]:
                    raise IndexConflictError("Runtime Pack is already active")
                next_previous = current
            elif operation == "rollback":
                if previous is None or previous != payload["target_ref"]:
                    raise InvalidIndexRecord("rollback target must be the declared previous Runtime Pack")
                next_previous = current
            else:
                raise InvalidIndexRecord("unsupported transition operation")
            connection.execute(
                """INSERT INTO activation_records(
                    transition_id, request_id, correlation_id, operation, outcome,
                    candidate_artifact_ref, previous_artifact_ref, resulting_artifact_ref,
                    verification_id, authorization_ref, resource_grant_ref, receipt_ref,
                    reason_codes_json, occurred_at, canonical_digest
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '[]', ?, ?)""",
                (
                    payload["transition_id"], payload["request_id"], payload["correlation_id"], operation,
                    expected_outcome.value, payload["target_ref"], current, payload["target_ref"],
                    payload["verification_id"], payload["authorization_ref"], payload["resource_grant_ref"],
                    payload["receipt_ref"], payload["occurred_at"], canonical_digest,
                ),
            )
            connection.execute(
                """UPDATE runtime_state SET active_artifact_ref = ?, previous_artifact_ref = ?,
                    revision = revision + 1, last_transition_id = ?, updated_at = ? WHERE singleton_id = 1""",
                (payload["target_ref"], next_previous, payload["transition_id"], payload["occurred_at"]),
            )
            row = connection.execute("SELECT * FROM activation_records WHERE transition_id = ?", (payload["transition_id"],)).fetchone()
            return self._activation(row)

    def record_unsuccessful_transition(
        self, *, transition_id: str, request_id: str, correlation_id: str,
        operation: str, outcome: TransitionOutcome, candidate_artifact_ref: str | None,
        verification_id: str | None, authorization_ref: str | None,
        resource_grant_ref: str | None, receipt_ref: str, reason_codes: Sequence[str],
        occurred_at: datetime,
    ) -> ActivationRecord:
        result = TransitionOutcome(outcome)
        if result not in {TransitionOutcome.BLOCKED, TransitionOutcome.FAILED}:
            raise InvalidIndexRecord("unsuccessful transition outcome must be blocked or failed")
        if operation not in {"activate", "rollback"}:
            raise InvalidIndexRecord("operation must be activate or rollback")
        reasons = _reason_codes(reason_codes)
        if not reasons:
            raise InvalidIndexRecord("unsuccessful transitions require reason_codes")
        payload = {
            "transition_id": _text(transition_id, "transition_id"), "request_id": _text(request_id, "request_id"),
            "correlation_id": _text(correlation_id, "correlation_id"), "operation": operation,
            "outcome": result.value, "candidate_artifact_ref": _text(candidate_artifact_ref, "candidate_artifact_ref", optional=True),
            "verification_id": _text(verification_id, "verification_id", optional=True),
            "authorization_ref": _text(authorization_ref, "authorization_ref", optional=True),
            "resource_grant_ref": _text(resource_grant_ref, "resource_grant_ref", optional=True),
            "receipt_ref": _text(receipt_ref, "receipt_ref"), "reason_codes": list(reasons),
            "occurred_at": _timestamp(occurred_at, "occurred_at"),
        }
        _, canonical_digest = _canonical(payload)
        with self._transaction() as connection:
            existing = connection.execute("SELECT * FROM activation_records WHERE request_id = ?", (payload["request_id"],)).fetchone()
            if existing is not None:
                if existing["canonical_digest"] != canonical_digest:
                    raise IndexConflictError("transition request_id was reused with different semantics")
                return self._activation(existing)
            state = connection.execute("SELECT * FROM runtime_state WHERE singleton_id = 1").fetchone()
            connection.execute(
                """INSERT INTO activation_records(
                    transition_id, request_id, correlation_id, operation, outcome,
                    candidate_artifact_ref, previous_artifact_ref, resulting_artifact_ref,
                    verification_id, authorization_ref, resource_grant_ref, receipt_ref,
                    reason_codes_json, occurred_at, canonical_digest
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    payload["transition_id"], payload["request_id"], payload["correlation_id"], operation,
                    result.value, payload["candidate_artifact_ref"], state["active_artifact_ref"],
                    state["active_artifact_ref"], payload["verification_id"], payload["authorization_ref"],
                    payload["resource_grant_ref"], payload["receipt_ref"],
                    json.dumps(list(reasons), separators=(",", ":")), payload["occurred_at"], canonical_digest,
                ),
            )
            row = connection.execute("SELECT * FROM activation_records WHERE transition_id = ?", (payload["transition_id"],)).fetchone()
            return self._activation(row)

    def runtime_state(self) -> RuntimeState:
        with self._read() as connection:
            row = connection.execute("SELECT * FROM runtime_state WHERE singleton_id = 1").fetchone()
            if row is None:
                raise IndexStorageUnavailable("runtime_state singleton is missing")
            return RuntimeState(row["active_artifact_ref"], row["previous_artifact_ref"], row["revision"], row["last_transition_id"], _parse_time(row["updated_at"]))

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path, timeout=self._busy_timeout_ms / 1000, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(f"PRAGMA busy_timeout = {self._busy_timeout_ms}")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except (sqlite3.Error, InvalidIndexRecord, IndexConflictError, IndexRecordNotFound):
            if connection.in_transaction:
                connection.rollback()
            raise
        except Exception as exc:
            if connection.in_transaction:
                connection.rollback()
            raise IndexStorageUnavailable(f"index transaction failed: {exc}") from exc
        finally:
            connection.close()

    @contextmanager
    def _read(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            yield connection
        except sqlite3.Error as exc:
            raise IndexStorageUnavailable(f"index read failed: {exc}") from exc
        finally:
            connection.close()

    @staticmethod
    def _artifact(row: sqlite3.Row) -> ArtifactIndexRecord:
        return ArtifactIndexRecord(
            row["artifact_ref"], row["artifact_class"], row["artifact_identity"], row["artifact_version"],
            row["artifact_digest"], row["document_digest"], row["storage_key"], row["byte_length"],
            ArtifactDisposition(row["disposition"]), row["verification_id"],
            _parse_time(row["registered_at"]), _parse_time(row["updated_at"]),
        )  # type: ignore[arg-type]

    @staticmethod
    def _verification(row: sqlite3.Row) -> VerificationRecord:
        checks = json.loads(row["checks_json"])
        reasons = json.loads(row["reason_codes_json"])
        if not isinstance(checks, dict) or not isinstance(reasons, list):
            raise IndexStorageUnavailable("stored verification JSON is invalid")
        return VerificationRecord(
            row["verification_id"], row["request_id"], row["correlation_id"], row["artifact_ref"],
            VerificationOutcome(row["outcome"]), bool(row["activation_eligible"]), MappingProxyType(checks),
            tuple(reasons), row["identity_receipt_ref"], row["policy_receipt_ref"], row["receipt_ref"],
            _parse_time(row["recorded_at"]),
        )  # type: ignore[arg-type]

    @staticmethod
    def _activation(row: sqlite3.Row) -> ActivationRecord:
        reasons = json.loads(row["reason_codes_json"])
        if not isinstance(reasons, list):
            raise IndexStorageUnavailable("stored transition reason_codes are invalid")
        return ActivationRecord(
            row["transition_id"], row["request_id"], row["correlation_id"], row["operation"],
            TransitionOutcome(row["outcome"]), row["candidate_artifact_ref"], row["previous_artifact_ref"],
            row["resulting_artifact_ref"], row["verification_id"], row["authorization_ref"],
            row["resource_grant_ref"], row["receipt_ref"], tuple(reasons), _parse_time(row["occurred_at"]),
        )  # type: ignore[arg-type]
