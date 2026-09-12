"""Bind and resolve externally verified OIDC subjects to local identities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from . import Conflict, InvalidRequest, require_text, require_utc, stable_ref
from ..ports import AuditEvent, AuditSink, Clock, ExternalIdentityBindingRecord, ExternalIdentityBindingStore

_ALLOWED_LOCAL_SUBJECT_TYPES = frozenset({"human", "recovery_operator"})


def _field(record: object, name: str):
    if isinstance(record, dict):
        return record.get(name)
    return getattr(record, name)


@dataclass(frozen=True, slots=True)
class BindExternalIdentityCommand:
    request_id: str
    provider_id: str
    issuer: str
    subject: str
    local_identity_id: str
    tenant_ref: str | None
    environment: str
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class BindExternalIdentityResult:
    request_id: str
    binding_ref: str
    identity_ref: str
    status: str
    reason_code: str
    authorizes_business_action: bool = False


class BindExternalIdentity:
    """Persist one exact OIDC issuer+subject binding after external verification."""

    operation_id = "bind_external_identity"

    def __init__(self, store: ExternalIdentityBindingStore, clock: Clock, audit: AuditSink) -> None:
        self._store = store
        self._clock = clock
        self._audit = audit

    def execute(self, command: BindExternalIdentityCommand) -> BindExternalIdentityResult:
        request_id = require_text(command.request_id, "request_id")
        provider_id = require_text(command.provider_id, "provider_id")
        issuer = require_text(command.issuer, "issuer")
        subject = require_text(command.subject, "subject")
        local_identity_id = require_text(command.local_identity_id, "local_identity_id")
        tenant_ref = require_text(command.tenant_ref, "tenant_ref") if command.tenant_ref is not None else None
        environment = require_text(command.environment, "environment")
        evidence_refs = tuple(dict.fromkeys(require_text(v, "evidence_ref") for v in command.evidence_refs))
        now = require_utc(self._clock.now(), "clock.now")

        identity = self._store.get_identity(local_identity_id)
        if identity is None:
            raise InvalidRequest("local identity does not exist", reason_code="identity_not_established")
        if _field(identity, "status") != "active":
            raise InvalidRequest("local identity is not active", reason_code="identity_not_established")
        if _field(identity, "subject_type") not in _ALLOWED_LOCAL_SUBJECT_TYPES:
            raise InvalidRequest("OIDC human SSO may bind only human or recovery_operator identities")
        if _field(identity, "tenant_ref") != tenant_ref or _field(identity, "environment") != environment:
            raise InvalidRequest("binding scope does not match local identity", reason_code="trust_scope_mismatch")

        existing = self._store.get_external_identity_binding(
            provider_id=provider_id,
            issuer=issuer,
            subject=subject,
            tenant_ref=tenant_ref,
            environment=environment,
        )
        if existing is not None:
            if _field(existing, "local_identity_id") != local_identity_id:
                raise Conflict(
                    "external subject is already bound to another local identity",
                    reason_code="state_conflict",
                )
            return BindExternalIdentityResult(
                request_id=request_id,
                binding_ref=str(_field(existing, "binding_id")),
                identity_ref=local_identity_id,
                status="active",
                reason_code="external_identity_already_bound",
            )

        binding_ref = stable_ref(
            "external-identity-binding",
            provider_id,
            issuer,
            subject,
            tenant_ref or "-",
            environment,
        )
        record = ExternalIdentityBindingRecord(
            binding_id=binding_ref,
            provider_type="oidc",
            provider_id=provider_id,
            issuer=issuer,
            subject=subject,
            local_identity_id=local_identity_id,
            tenant_ref=tenant_ref,
            environment=environment,
            created_at=now,
            evidence_refs=evidence_refs,
        )
        event = AuditEvent(
            event_id=stable_ref("event", self.operation_id, request_id, binding_ref),
            operation_id=self.operation_id,
            request_id=request_id,
            event_type="external_identity_bound",
            outcome="committed",
            occurred_at=now,
            subject_refs=(local_identity_id, binding_ref),
            reason_code="external_identity_bound",
            evidence_refs=evidence_refs,
            details={"provider_id": provider_id, "authorizes_business_action": "false"},
        )
        self._audit.ensure_available(critical=True)
        with self._store.transaction():
            self._store.put_external_identity_binding(record)
            self._audit.publish(event)
        return BindExternalIdentityResult(
            request_id=request_id,
            binding_ref=binding_ref,
            identity_ref=local_identity_id,
            status="active",
            reason_code="external_identity_bound",
        )


@dataclass(frozen=True, slots=True)
class ResolveExternalIdentityCommand:
    provider_id: str
    issuer: str
    subject: str
    tenant_ref: str | None
    environment: str


@dataclass(frozen=True, slots=True)
class ResolveExternalIdentityResult:
    identity_result: str
    identity_ref: str | None
    reason_code: str
    authorizes_business_action: bool = False


class ResolveExternalIdentity:
    """Resolve an exact issuer+subject pair to an active local identity."""

    def __init__(self, store: ExternalIdentityBindingStore) -> None:
        self._store = store

    def execute(self, command: ResolveExternalIdentityCommand) -> ResolveExternalIdentityResult:
        provider_id = require_text(command.provider_id, "provider_id")
        issuer = require_text(command.issuer, "issuer")
        subject = require_text(command.subject, "subject")
        tenant_ref = require_text(command.tenant_ref, "tenant_ref") if command.tenant_ref is not None else None
        environment = require_text(command.environment, "environment")
        binding = self._store.get_external_identity_binding(
            provider_id=provider_id,
            issuer=issuer,
            subject=subject,
            tenant_ref=tenant_ref,
            environment=environment,
        )
        if binding is None:
            return ResolveExternalIdentityResult("not_established", None, "external_identity_not_bound")
        identity_ref = str(_field(binding, "local_identity_id"))
        identity = self._store.get_identity(identity_ref)
        if identity is None or _field(identity, "status") != "active":
            return ResolveExternalIdentityResult("not_established", identity_ref, "identity_not_established")
        return ResolveExternalIdentityResult("established", identity_ref, "external_identity_resolved")
