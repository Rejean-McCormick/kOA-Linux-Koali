"""External identity bindings for optional federation.

The binding maps an externally verified subject to a stable local kOA identity.
It is identity evidence only and never grants business authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class ExternalIdentityProviderType(str, Enum):
    OIDC = "oidc"


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _instant(name: str, value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class ExternalIdentityBinding:
    """Exact provider subject -> local identity mapping.

    `issuer` and `subject` are preserved exactly after surrounding whitespace is
    removed. Email, display name and other profile attributes are not identity keys.
    """

    binding_id: str
    provider_type: ExternalIdentityProviderType
    provider_id: str
    issuer: str
    subject: str
    local_identity_id: str
    tenant_ref: str | None
    environment: str
    created_at: datetime
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "binding_id", _required("binding_id", self.binding_id))
        object.__setattr__(self, "provider_type", ExternalIdentityProviderType(self.provider_type))
        object.__setattr__(self, "provider_id", _required("provider_id", self.provider_id))
        object.__setattr__(self, "issuer", _required("issuer", self.issuer))
        object.__setattr__(self, "subject", _required("subject", self.subject))
        object.__setattr__(self, "local_identity_id", _required("local_identity_id", self.local_identity_id))
        if self.tenant_ref is not None:
            object.__setattr__(self, "tenant_ref", _required("tenant_ref", self.tenant_ref))
        object.__setattr__(self, "environment", _required("environment", self.environment))
        object.__setattr__(self, "created_at", _instant("created_at", self.created_at))
        object.__setattr__(
            self,
            "evidence_refs",
            tuple(sorted({_required("evidence_ref", value) for value in self.evidence_refs})),
        )

    @property
    def federated_subject_key(self) -> tuple[str, str]:
        return (self.issuer, self.subject)
