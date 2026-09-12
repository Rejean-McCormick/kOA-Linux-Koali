"""Persistence boundary for external identity federation bindings."""

from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable

from .identity_store import IdentityRecord


@dataclass(frozen=True, slots=True)
class ExternalIdentityBindingRecord:
    binding_id: str
    provider_type: str
    provider_id: str
    issuer: str
    subject: str
    local_identity_id: str
    tenant_ref: str | None
    environment: str
    created_at: datetime
    evidence_refs: tuple[str, ...] = ()


@runtime_checkable
class ExternalIdentityBindingStore(Protocol):
    """Store local identity bindings; it does not own external IdP source records."""

    def transaction(self) -> AbstractContextManager[object]:
        raise NotImplementedError

    def get_identity(self, identity_id: str) -> IdentityRecord | dict[str, object] | None:
        raise NotImplementedError

    def get_external_identity_binding(
        self,
        *,
        provider_id: str,
        issuer: str,
        subject: str,
        tenant_ref: str | None,
        environment: str,
    ) -> ExternalIdentityBindingRecord | dict[str, object] | None:
        raise NotImplementedError

    def put_external_identity_binding(self, record: ExternalIdentityBindingRecord) -> None:
        raise NotImplementedError
