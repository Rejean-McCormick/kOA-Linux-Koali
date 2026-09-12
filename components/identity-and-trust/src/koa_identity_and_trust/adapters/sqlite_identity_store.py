"""Component-owned SQLite persistence for Identity and Trust."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from dataclasses import asdict, is_dataclass
from collections.abc import Iterable, Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class IdentityStoreError(RuntimeError):
    """Raised for invalid or unsafe identity-store operations."""


class ConcurrentUpdateError(IdentityStoreError):
    """Raised when optimistic revision checks detect stale application state."""


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _mapping(record: Mapping[str, Any] | object) -> dict[str, Any]:
    if isinstance(record, Mapping):
        return dict(record)
    if hasattr(record, "to_record"):
        converted = record.to_record()  # type: ignore[attr-defined]
        if isinstance(converted, Mapping):
            return dict(converted)
    if is_dataclass(record):
        return asdict(record)
    if hasattr(record, "__dict__"):
        return dict(vars(record))
    raise TypeError("record must be a mapping or expose to_record()")


class SQLiteIdentityStore:
    """Persist only Identity and Trust authoritative records in one SQLite file."""

    def __init__(
        self,
        database: str | Path,
        *,
        migration: str | Path | None = None,
        timeout: float = 5.0,
    ) -> None:
        self.database = Path(database).expanduser().resolve()
        self.timeout = timeout
        self.migration = Path(migration).expanduser().resolve() if migration is not None else None
        self.migrations_dir = Path(__file__).resolve().parents[3] / "migrations"

    def initialize(self) -> None:
        self.database.parent.mkdir(parents=True, exist_ok=True)
        migrations = [self.migration] if self.migration is not None else sorted(self.migrations_dir.glob("*.sql"))
        with self._connect() as connection:
            for migration in migrations:
                connection.executescript(migration.read_text(encoding="utf-8"))
        try:
            self.database.chmod(0o600)
        except OSError as exc:
            raise IdentityStoreError("cannot enforce identity-store permissions") from exc

    @contextmanager
    def transaction(self, *, immediate: bool = True) -> Iterator[sqlite3.Connection]:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
            try:
                yield connection
            except BaseException:
                connection.rollback()
                raise
            else:
                connection.commit()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database,
            timeout=self.timeout,
            isolation_level=None,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")
        connection.execute("PRAGMA trusted_schema = OFF")
        return connection

    def put_identity(self, record: Mapping[str, Any] | object, *, expected_revision: int | None = None) -> int:
        data = _mapping(record)
        fields = {
            "identity_id": data["identity_id"],
            "subject_type": data["subject_type"],
            "display_name": data["display_name"],
            "owner_ref": data.get("owner_ref"),
            "tenant_ref": data.get("tenant_ref"),
            "environment": data["environment"],
            "status": data["status"],
            "created_at": data["created_at"],
            "activated_at": data.get("activated_at"),
            "expires_at": data.get("expires_at"),
            "revoked_at": data.get("revoked_at"),
            "retired_at": data.get("retired_at"),
            "credential_refs_json": _json(data.get("credential_refs", [])),
            "evidence_refs_json": _json(data.get("evidence_refs", [])),
            "public_attributes_json": _json(data.get("public_attributes", {})),
        }
        return self._upsert_revisioned("identities", "identity_id", fields, expected_revision)

    def get_identity(self, identity_id: str) -> dict[str, Any] | None:
        return self._fetch_one("identities", "identity_id", identity_id, {
            "credential_refs_json": "credential_refs",
            "evidence_refs_json": "evidence_refs",
            "public_attributes_json": "public_attributes",
        })


    def put_external_identity_binding(self, record: Mapping[str, Any] | object) -> None:
        data = _mapping(record)
        fields = {
            "binding_id": data["binding_id"],
            "provider_type": data.get("provider_type", "oidc"),
            "provider_id": data["provider_id"],
            "issuer": data["issuer"],
            "subject": data["subject"],
            "local_identity_id": data["local_identity_id"],
            "tenant_ref": data.get("tenant_ref") or "",
            "environment": data["environment"],
            "created_at": data["created_at"],
            "evidence_refs_json": _json(data.get("evidence_refs", [])),
        }
        self._insert("external_identity_bindings", fields)

    def get_external_identity_binding(
        self,
        *,
        provider_id: str,
        issuer: str,
        subject: str,
        tenant_ref: str | None,
        environment: str,
    ) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT * FROM external_identity_bindings
                   WHERE provider_id = ? AND issuer = ? AND subject = ?
                     AND tenant_ref = ? AND environment = ?
                   LIMIT 1""",
                (provider_id, issuer, subject, tenant_ref or "", environment),
            ).fetchone()
        if row is None:
            return None
        result = self._decode(dict(row), {"evidence_refs_json": "evidence_refs"})
        result["tenant_ref"] = result["tenant_ref"] or None
        return result

    def put_credential(self, record: Mapping[str, Any] | object, *, expected_revision: int | None = None) -> int:
        data = _mapping(record)
        fields = {
            "credential_id": data["credential_id"],
            "subject_identity_id": data["subject_identity_id"],
            "credential_type": data["credential_type"],
            "issuer_ref": data["issuer_ref"],
            "scope_json": _json(data["scope"]),
            "issued_at": data["issued_at"],
            "not_before": data["not_before"],
            "expires_at": data.get("expires_at"),
            "status": data["status"],
            "key_or_material_reference": data["key_or_material_reference"],
            "revocation_reference": data["revocation_reference"],
            "evidence_refs_json": _json(data.get("evidence_refs", [])),
        }
        return self._upsert_revisioned("credentials", "credential_id", fields, expected_revision)

    def get_credential(self, credential_id: str) -> dict[str, Any] | None:
        return self._fetch_one("credentials", "credential_id", credential_id, {
            "scope_json": "scope", "evidence_refs_json": "evidence_refs"
        })

    def put_trust_root(self, record: Mapping[str, Any] | object, *, expected_revision: int | None = None) -> int:
        data = _mapping(record)
        scope = data["scope"]
        fields = {
            "trust_root_id": data["trust_root_id"],
            "root_type": data["root_type"],
            "public_material_ref": data["public_material_ref"],
            "scope_json": _json(scope),
            "scope_fingerprint": self.scope_fingerprint(scope),
            "owner_ref": data["owner_ref"],
            "status": data["status"],
            "activated_at": data.get("activated_at"),
            "expires_at": data.get("expires_at"),
            "revoked_at": data.get("revoked_at"),
            "supersedes_ref": data.get("supersedes_ref"),
            "evidence_refs_json": _json(data.get("evidence_refs", [])),
        }
        return self._upsert_revisioned("trust_roots", "trust_root_id", fields, expected_revision)

    def get_trust_root(self, trust_root_id: str) -> dict[str, Any] | None:
        return self._fetch_one("trust_roots", "trust_root_id", trust_root_id, {
            "scope_json": "scope", "evidence_refs_json": "evidence_refs"
        })

    def active_trust_roots(self, scope: Mapping[str, object]) -> list[dict[str, Any]]:
        fingerprint = self.scope_fingerprint(scope)
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM trust_roots WHERE scope_fingerprint = ? AND status = 'active' ORDER BY trust_root_id",
                (fingerprint,),
            ).fetchall()
        return [self._decode(dict(row), {"scope_json": "scope", "evidence_refs_json": "evidence_refs"}) for row in rows]

    def record_revocation(self, record: Mapping[str, Any] | object) -> None:
        data = _mapping(record)
        columns = {
            "revocation_id": data["revocation_id"],
            "target_ref": data["target_ref"],
            "target_type": data["target_type"],
            "scope_json": _json(data["scope"]),
            "reason_code": data["reason_code"],
            "authority_ref": data["authority_ref"],
            "effective_at": data["effective_at"],
            "recorded_at": data["recorded_at"],
            "evidence_refs_json": _json(data.get("evidence_refs", [])),
        }
        self._insert("revocations", columns)

    def is_revoked(self, target_ref: str, target_type: str, *, at: str) -> bool:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM revocations WHERE target_ref = ? AND target_type = ? AND effective_at <= ? LIMIT 1",
                (target_ref, target_type, at),
            ).fetchone()
        return row is not None

    def record_verification(self, record: Mapping[str, Any] | object) -> None:
        data = _mapping(record)
        columns = {
            "verification_id": data["verification_id"],
            "result": data["result"],
            "resolved_identity_ref": data.get("resolved_identity_ref"),
            "resolved_trust_root_ref": data.get("resolved_trust_root_ref"),
            "validated_scope_json": _json(data.get("validated_scope", {})),
            "algorithm": data.get("algorithm"),
            "credential_or_artifact_ref": data["credential_or_artifact_ref"],
            "verified_at": data["verified_at"],
            "reason_code": data["reason_code"],
            "evidence_refs_json": _json(data.get("evidence_refs", [])),
        }
        self._insert("verification_results", columns)

    def apply_trust_update(
        self,
        *,
        scope: Mapping[str, object],
        expected_sequence: int,
        new_sequence: int,
        package_ref: str,
        applied_at: str,
        receipt_ref: str,
        revocations: Iterable[Mapping[str, Any]] = (),
    ) -> None:
        """Atomically advance one exact trust scope and apply its revocations."""

        if new_sequence <= expected_sequence:
            raise IdentityStoreError("offline trust update must advance monotonically")
        fingerprint = self.scope_fingerprint(scope)
        with self.transaction() as connection:
            current = connection.execute(
                "SELECT active_sequence FROM trust_update_state WHERE scope_fingerprint = ?",
                (fingerprint,),
            ).fetchone()
            actual = int(current[0]) if current is not None else 0
            if actual != expected_sequence:
                raise ConcurrentUpdateError(
                    f"trust update sequence changed: expected {expected_sequence}, found {actual}"
                )
            for record in revocations:
                data = dict(record)
                connection.execute(
                    """INSERT INTO revocations(
                        revocation_id,target_ref,target_type,scope_json,reason_code,
                        authority_ref,effective_at,recorded_at,evidence_refs_json
                    ) VALUES (?,?,?,?,?,?,?,?,?)""",
                    (
                        data["revocation_id"], data["target_ref"], data["target_type"],
                        _json(data.get("scope", scope)), data["reason_code"],
                        data["authority_ref"], data["effective_at"], data["recorded_at"],
                        _json(data.get("evidence_refs", [])),
                    ),
                )
            connection.execute(
                """INSERT INTO trust_update_state(scope_fingerprint,active_sequence,package_ref,applied_at,receipt_ref)
                   VALUES (?,?,?,?,?)
                   ON CONFLICT(scope_fingerprint) DO UPDATE SET
                     active_sequence=excluded.active_sequence,
                     package_ref=excluded.package_ref,
                     applied_at=excluded.applied_at,
                     receipt_ref=excluded.receipt_ref""",
                (fingerprint, new_sequence, package_ref, applied_at, receipt_ref),
            )

    def backup_to(self, destination: str | Path, *, replace: bool = False) -> Path:
        """Create a consistent component-owned SQLite backup, excluding key bytes."""

        candidate = Path(destination).expanduser()
        if candidate.is_symlink():
            raise IdentityStoreError("backup destination must not be a symbolic link")
        target = candidate.resolve()
        if target == self.database:
            raise IdentityStoreError("backup destination must differ from the active store")
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not replace:
            raise FileExistsError(f"backup destination already exists: {target}")
        temporary = target.with_name(f".{target.name}.partial")
        temporary.unlink(missing_ok=True)
        try:
            with self._connect() as source, sqlite3.connect(temporary) as backup:
                source.backup(backup)
                result = backup.execute("PRAGMA integrity_check").fetchone()
                if result is None or result[0] != "ok":
                    raise IdentityStoreError("SQLite backup integrity check failed")
            temporary.chmod(0o600)
            os.replace(temporary, target)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
        return target

    @staticmethod
    def scope_fingerprint(scope: Mapping[str, object]) -> str:
        if not scope:
            raise ValueError("trust scope must be explicit and non-empty")
        return hashlib.sha256(_json(scope).encode("utf-8")).hexdigest()

    def _insert(self, table: str, fields: Mapping[str, object]) -> None:
        columns = ",".join(fields)
        placeholders = ",".join("?" for _ in fields)
        with self.transaction() as connection:
            connection.execute(
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                tuple(fields.values()),
            )

    def _upsert_revisioned(
        self,
        table: str,
        key_name: str,
        fields: Mapping[str, object],
        expected_revision: int | None,
    ) -> int:
        key = fields[key_name]
        with self.transaction() as connection:
            current = connection.execute(
                f"SELECT revision FROM {table} WHERE {key_name} = ?", (key,)
            ).fetchone()
            if current is None:
                if expected_revision not in (None, 0):
                    raise ConcurrentUpdateError(f"{table} record does not exist")
                columns = [*fields, "revision"]
                connection.execute(
                    f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)})",
                    (*fields.values(), 0),
                )
                return 0
            actual = int(current[0])
            if expected_revision is None or expected_revision != actual:
                raise ConcurrentUpdateError(
                    f"{table} revision changed: expected {expected_revision}, found {actual}"
                )
            new_revision = actual + 1
            assignments = ",".join(f"{column} = ?" for column in fields if column != key_name)
            values = [fields[column] for column in fields if column != key_name]
            cursor = connection.execute(
                f"UPDATE {table} SET {assignments}, revision = ? WHERE {key_name} = ? AND revision = ?",
                (*values, new_revision, key, actual),
            )
            if cursor.rowcount != 1:
                raise ConcurrentUpdateError(f"concurrent update detected for {table}")
            return new_revision

    def _fetch_one(
        self,
        table: str,
        key_name: str,
        key: str,
        json_fields: Mapping[str, str],
    ) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                f"SELECT * FROM {table} WHERE {key_name} = ?", (key,)
            ).fetchone()
        return None if row is None else self._decode(dict(row), json_fields)

    @staticmethod
    def _decode(record: dict[str, Any], json_fields: Mapping[str, str]) -> dict[str, Any]:
        for stored, public in json_fields.items():
            record[public] = json.loads(record.pop(stored))
        return record
