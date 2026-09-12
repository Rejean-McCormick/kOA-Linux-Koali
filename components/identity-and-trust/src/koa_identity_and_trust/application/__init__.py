"""Application-layer primitives for Identity and Trust.

The application layer establishes identity and trust outcomes.  It deliberately
never grants business, governance, publication, resource, release, or host
mutation authority.
"""

from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
import json
from typing import NoReturn


class IdentityAndTrustApplicationError(RuntimeError):
    """Base class for explicit application failures."""

    reason_code = "identity_and_trust_application_error"

    def __init__(self, message: str, *, reason_code: str | None = None) -> None:
        super().__init__(message)
        if reason_code is not None:
            self.reason_code = reason_code


class InvalidRequest(IdentityAndTrustApplicationError, ValueError):
    """The caller supplied a malformed, unsupported, or ambiguous request."""

    reason_code = "invalid_request"


class NotFound(IdentityAndTrustApplicationError, LookupError):
    """A required identity-and-trust object does not exist."""

    reason_code = "not_found"


class Conflict(IdentityAndTrustApplicationError):
    """The requested transition conflicts with authoritative current state."""

    reason_code = "state_conflict"


class DependencyUnavailable(IdentityAndTrustApplicationError):
    """A required protected store, key provider, or evidence path is unavailable."""

    reason_code = "dependency_unavailable"


def require_text(value: str, field: str) -> str:
    """Return a stripped non-empty value or reject the request."""

    if not isinstance(value, str):
        raise InvalidRequest(f"{field} must be a string")
    normalized = value.strip()
    if not normalized:
        raise InvalidRequest(f"{field} must not be empty")
    if any(ord(character) < 32 for character in normalized):
        raise InvalidRequest(f"{field} contains control characters")
    return normalized


def require_utc(value: datetime, field: str) -> datetime:
    """Require an aware UTC timestamp and normalize it to UTC."""

    if not isinstance(value, datetime):
        raise InvalidRequest(f"{field} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise InvalidRequest(f"{field} must be timezone-aware")
    return value.astimezone(UTC)


def stable_ref(kind: str, *parts: str) -> str:
    """Create a deterministic opaque reference from non-secret request metadata."""

    normalized_kind = require_text(kind, "kind").lower().replace("_", "-")
    material = "\x1f".join(require_text(part, "reference part") for part in parts)
    digest = sha256(material.encode("utf-8")).hexdigest()
    return f"{normalized_kind}-{digest[:32]}"


def canonical_json(value: object) -> str:
    """Serialize an application result deterministically for idempotency storage."""

    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def unreachable(message: str) -> NoReturn:
    """Raise an explicit internal-state error instead of returning a false success."""

    raise IdentityAndTrustApplicationError(message, reason_code="invalid_internal_state")


from .external_identity import (  # noqa: E402
    BindExternalIdentity,
    BindExternalIdentityCommand,
    BindExternalIdentityResult,
    ResolveExternalIdentity,
    ResolveExternalIdentityCommand,
    ResolveExternalIdentityResult,
)
from .issue_local_identity import (  # noqa: E402
    IssueLocalIdentity,
    IssueLocalIdentityCommand,
    IssueLocalIdentityResult,
)
from .resolve_session import ResolveSession, ResolveSessionCommand, ResolveSessionResult  # noqa: E402
from .revoke_credential import (  # noqa: E402
    RevokeCredential,
    RevokeCredentialCommand,
    RevokeCredentialResult,
)
from .rotate_trust_root import (  # noqa: E402
    RotateTrustRoot,
    RotateTrustRootCommand,
    RotateTrustRootResult,
)
from .verify_credential import (  # noqa: E402
    VerifyCredential,
    VerifyCredentialCommand,
    VerifyCredentialResult,
)

__all__ = [
    "BindExternalIdentity",
    "BindExternalIdentityCommand",
    "BindExternalIdentityResult",
    "Conflict",
    "DependencyUnavailable",
    "IdentityAndTrustApplicationError",
    "InvalidRequest",
    "IssueLocalIdentity",
    "IssueLocalIdentityCommand",
    "IssueLocalIdentityResult",
    "NotFound",
    "ResolveExternalIdentity",
    "ResolveExternalIdentityCommand",
    "ResolveExternalIdentityResult",
    "ResolveSession",
    "ResolveSessionCommand",
    "ResolveSessionResult",
    "RevokeCredential",
    "RevokeCredentialCommand",
    "RevokeCredentialResult",
    "RotateTrustRoot",
    "RotateTrustRootCommand",
    "RotateTrustRootResult",
    "VerifyCredential",
    "VerifyCredentialCommand",
    "VerifyCredentialResult",
]
