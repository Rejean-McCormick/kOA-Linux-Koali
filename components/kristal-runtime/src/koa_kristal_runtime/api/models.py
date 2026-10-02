"""Transport-neutral public models for Kristal Runtime.

The module performs boundary validation only. Artifact trust, digest calculation,
compatibility decisions, persistence, policy evaluation, resource admission, and
atomic state transitions remain responsibilities of the service supplied by the
preceding bundles.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dataclass_field
from types import MappingProxyType
from typing import Any, Mapping, Sequence
import re

API_VERSION = "1.0.0"
COMPONENT_ID = "kristal_runtime"
COMPONENT_CONTRACT = "contracts/components/kristal-runtime.component.json"
RUNTIME_PACK_SCHEMA = "docs/contracts/artifact-contracts/runtime-pack.schema.json"
KRISTAL_STATE_SCHEMA = "docs/contracts/artifact-contracts/kristal-state.schema.json"
KRISTAL_READER_POLICY_SCHEMA = "docs/contracts/artifact-contracts/kristal-reader-policy.schema.json"
KRISTAL_ARTIFACT_SCHEMA = "docs/contracts/artifact-contracts/kristal-artifact.schema.json"  # legacy
KRISTAL_STANDARD_VERSION = "6.0.0"
KRISTAL_CANONICALIZATION_PROFILE = "kristal.v6:jcs-rfc8785"
KNOWLEDGE_RELEASE_CHANNEL = "knowledge"

INTERFACE_IDS = (
    "kristal_identity_resolution",
    "runtime_pack_validation",
    "runtime_pack_activation",
    "runtime_pack_rollback",
    "runtime_status_query",
)

RUNTIME_STATES = (
    "inactive",
    "verification_pending",
    "verified",
    "active",
    "blocked",
    "degraded",
    "rollback_in_progress",
    "failed",
)
VERIFICATION_CHECKS = (
    "schema_validation",
    "identity_validation",
    "digest_validation",
    "trust_validation_when_required",
    "compatibility_validation",
    "release_channel_validation",
    "downgrade_and_substitution_policy_validation",
)
RECEIPT_CLASSES = (
    "verification_receipt",
    "transition_receipt",
    "recovery_receipt",
)
RECEIPT_TRANSITIONS = (
    "runtime_pack_validation",
    "runtime_pack_activation",
    "runtime_pack_rollback",
    "runtime_pack_failure",
)
RECEIPT_OUTCOMES = (
    "verified",
    "activated",
    "rolled_back",
    "blocked",
    "failed",
    "forward_repair_required",
)
DIGEST_RE = re.compile(r"^(?:sha256:[0-9a-f]{64}|sha384:[0-9a-f]{96}|sha512:[0-9a-f]{128})$")
RUNTIME_PACK_ID_RE = re.compile(r"^runtime-pack:[A-Za-z0-9][A-Za-z0-9._:/+-]*$")
KRISTAL_ID_RE = re.compile(r"^(?:sha256:[0-9a-f]{64}|kristal(?:-artifact)?[.:/][A-Za-z0-9][A-Za-z0-9._:/@+-]*)$")
SENSITIVE_KEY_RE = re.compile(
    r"(?:^|[_-])(password|passwd|secret|private[_-]?key|access[_-]?token|refresh[_-]?token|api[_-]?key)(?:$|[_-])",
    re.IGNORECASE,
)


class ModelValidationError(ValueError):
    """A public request or response violates the closed API contract."""

    def __init__(self, field_name: str, code: str, message: str) -> None:
        super().__init__(message)
        self.field_name = field_name
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class ApiError:
    code: str
    message: str
    field: str | None = None
    details: Mapping[str, str] = dataclass_field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _require_token(self.code, "error.code"))
        object.__setattr__(self, "message", _require_string(self.message, "error.message", max_length=512))
        if self.field is not None:
            object.__setattr__(self, "field", _require_string(self.field, "error.field", max_length=256))
        object.__setattr__(self, "details", _string_mapping(self.details, "error.details"))

    def to_mapping(self) -> dict[str, Any]:
        result: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.field is not None:
            result["field"] = self.field
        if self.details:
            result["details"] = dict(self.details)
        return result


@dataclass(frozen=True, slots=True)
class ApiRequest:
    interface_id: str
    request_id: str
    correlation_id: str
    payload: Mapping[str, Any]
    version: str = API_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "interface_id", _require_token(self.interface_id, "interface_id"))
        object.__setattr__(self, "request_id", _require_reference(self.request_id, "request_id"))
        object.__setattr__(self, "correlation_id", _require_reference(self.correlation_id, "correlation_id"))
        if self.version != API_VERSION:
            raise ModelValidationError("version", "unsupported_version", f"version must be {API_VERSION}")
        object.__setattr__(self, "payload", _mapping(self.payload, "payload"))

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ApiRequest":
        data = _mapping(value, "request")
        _reject_unknown(data, {"interface_id", "request_id", "correlation_id", "payload", "version"}, "request")
        return cls(
            interface_id=_require_string(data.get("interface_id"), "interface_id"),
            request_id=_require_string(data.get("request_id"), "request_id"),
            correlation_id=_require_string(data.get("correlation_id"), "correlation_id"),
            payload=_mapping(data.get("payload", {}), "payload"),
            version=_require_string(data.get("version", API_VERSION), "version"),
        )


@dataclass(frozen=True, slots=True)
class ApiResponse:
    interface_id: str
    request_id: str
    correlation_id: str
    status: str
    result: Mapping[str, Any] | None = None
    error: ApiError | None = None
    version: str = API_VERSION

    def __post_init__(self) -> None:
        if self.status not in {"succeeded", "rejected", "failed"}:
            raise ModelValidationError("status", "invalid_response_status", "response status is not registered")
        if self.version != API_VERSION:
            raise ModelValidationError("version", "unsupported_version", f"version must be {API_VERSION}")
        if self.status == "succeeded":
            if self.result is None or self.error is not None:
                raise ModelValidationError("result", "invalid_success_response", "successful responses require only a result")
            object.__setattr__(self, "result", _mapping(self.result, "result"))
        else:
            if self.error is None or self.result is not None:
                raise ModelValidationError("error", "invalid_error_response", "rejected and failed responses require only an error")

    @classmethod
    def success(cls, request: ApiRequest, result: object) -> "ApiResponse":
        return cls(request.interface_id, request.request_id, request.correlation_id, "succeeded", _public_mapping(result))

    @classmethod
    def rejected(cls, request: ApiRequest, error: ApiError) -> "ApiResponse":
        return cls(request.interface_id, request.request_id, request.correlation_id, "rejected", error=error)

    @classmethod
    def failed(cls, request: ApiRequest, error: ApiError) -> "ApiResponse":
        return cls(request.interface_id, request.request_id, request.correlation_id, "failed", error=error)

    def to_mapping(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "interface_id": self.interface_id,
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "version": self.version,
            "status": self.status,
        }
        if self.result is not None:
            result["result"] = dict(self.result)
        if self.error is not None:
            result["error"] = self.error.to_mapping()
        return result


@dataclass(frozen=True, slots=True)
class Receipt:
    receipt_id: str
    receipt_class: str
    transition: str
    outcome: str
    correlation_id: str
    subject_ref: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "receipt_id", _require_reference(self.receipt_id, "receipt_id"))
        if self.receipt_class not in RECEIPT_CLASSES:
            raise ModelValidationError("receipt_class", "invalid_receipt_class", "receipt class is not registered")
        if self.transition not in RECEIPT_TRANSITIONS:
            raise ModelValidationError("transition", "invalid_receipt_transition", "receipt transition is not registered")
        if self.outcome not in RECEIPT_OUTCOMES:
            raise ModelValidationError("outcome", "invalid_receipt_outcome", "receipt outcome is not registered")
        object.__setattr__(self, "correlation_id", _require_reference(self.correlation_id, "correlation_id"))
        object.__setattr__(self, "subject_ref", _require_reference(self.subject_ref, "subject_ref"))
        object.__setattr__(self, "evidence_refs", _string_sequence(self.evidence_refs, "evidence_refs"))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "receipt_class": self.receipt_class,
            "transition": self.transition,
            "outcome": self.outcome,
            "correlation_id": self.correlation_id,
            "subject_ref": self.subject_ref,
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class KristalIdentityResolutionRequest:
    request_id: str
    correlation_id: str
    content_identity_claim: str | None = None
    canonical_content_reference: str | None = None
    content_digest: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _require_reference(self.request_id, "request_id"))
        object.__setattr__(self, "correlation_id", _require_reference(self.correlation_id, "correlation_id"))
        if self.content_identity_claim is not None:
            object.__setattr__(self, "content_identity_claim", _require_reference(self.content_identity_claim, "content_identity_claim"))
        if self.canonical_content_reference is not None:
            object.__setattr__(self, "canonical_content_reference", _require_reference(self.canonical_content_reference, "canonical_content_reference"))
        if self.content_digest is not None:
            object.__setattr__(self, "content_digest", _require_digest(self.content_digest, "content_digest"))
        if not any((self.content_identity_claim, self.canonical_content_reference, self.content_digest)):
            raise ModelValidationError("payload", "identity_input_missing", "identity resolution requires a claim, canonical reference, or digest")

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], request: ApiRequest) -> "KristalIdentityResolutionRequest":
        data = _mapping(payload, "payload")
        _reject_unknown(data, {"content_identity_claim", "canonical_content_reference", "content_digest"}, "payload")
        return cls(
            request.request_id,
            request.correlation_id,
            _optional_string(data.get("content_identity_claim"), "content_identity_claim"),
            _optional_string(data.get("canonical_content_reference"), "canonical_content_reference"),
            _optional_string(data.get("content_digest"), "content_digest"),
        )


@dataclass(frozen=True, slots=True)
class KristalIdentityResolutionResponse:
    outcome: str
    verification_outcome: str
    resolved_kristal_identity: str | None = None
    content_digest: str | None = None

    def __post_init__(self) -> None:
        if self.outcome not in {"resolved", "identity_unresolved", "content_digest_invalid", "canonical_content_unavailable"}:
            raise ModelValidationError("outcome", "invalid_identity_outcome", "identity outcome is not registered")
        if self.verification_outcome not in {"verified", "unresolved", "failed", "blocked"}:
            raise ModelValidationError("verification_outcome", "invalid_verification_outcome", "verification outcome is not registered")
        if self.resolved_kristal_identity is not None:
            identity = _require_reference(self.resolved_kristal_identity, "resolved_kristal_identity")
            if not KRISTAL_ID_RE.fullmatch(identity):
                raise ModelValidationError("resolved_kristal_identity", "invalid_kristal_identity", "resolved identity is not a Kristal identity")
            object.__setattr__(self, "resolved_kristal_identity", identity)
        if self.content_digest is not None:
            object.__setattr__(self, "content_digest", _require_digest(self.content_digest, "content_digest"))
        if self.outcome == "resolved" and (self.resolved_kristal_identity is None or self.verification_outcome != "verified"):
            raise ModelValidationError("outcome", "incomplete_identity_resolution", "resolved outcomes require a verified Kristal identity")
        if self.outcome != "resolved" and self.resolved_kristal_identity is not None:
            raise ModelValidationError("resolved_kristal_identity", "identity_on_failure", "failed identity resolution cannot expose a resolved identity")

    def to_mapping(self) -> dict[str, Any]:
        result: dict[str, Any] = {"outcome": self.outcome, "verification_outcome": self.verification_outcome}
        if self.resolved_kristal_identity is not None:
            result["resolved_kristal_identity"] = self.resolved_kristal_identity
        if self.content_digest is not None:
            result["content_digest"] = self.content_digest
        return result


@dataclass(frozen=True, slots=True)
class RuntimePackValidationRequest:
    request_id: str
    correlation_id: str
    runtime_pack: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _require_reference(self.request_id, "request_id"))
        object.__setattr__(self, "correlation_id", _require_reference(self.correlation_id, "correlation_id"))
        pack = _mapping(self.runtime_pack, "runtime_pack")
        _validate_runtime_pack_boundary(pack)
        object.__setattr__(self, "runtime_pack", pack)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], request: ApiRequest) -> "RuntimePackValidationRequest":
        data = _mapping(payload, "payload")
        _reject_unknown(data, {"runtime_pack"}, "payload")
        return cls(request.request_id, request.correlation_id, _mapping(data.get("runtime_pack"), "runtime_pack"))

    @property
    def artifact_identity(self) -> str:
        return str(self.runtime_pack["artifact_identity"])

    @property
    def artifact_version(self) -> str:
        return str(self.runtime_pack["artifact_version"])

    @property
    def artifact_digest(self) -> str:
        return str(self.runtime_pack["artifact_digest"])


@dataclass(frozen=True, slots=True)
class RuntimePackVerificationResult:
    outcome: str
    activation_eligible: bool
    verification_record_ref: str
    artifact_identity: str
    artifact_version: str
    artifact_digest: str
    checks: Mapping[str, str]
    receipt: Receipt

    def __post_init__(self) -> None:
        if self.outcome not in {"verified", "blocked", "failed"}:
            raise ModelValidationError("outcome", "invalid_validation_outcome", "validation outcome is not registered")
        if not isinstance(self.activation_eligible, bool):
            raise ModelValidationError("activation_eligible", "invalid_boolean", "activation_eligible must be boolean")
        object.__setattr__(self, "verification_record_ref", _require_reference(self.verification_record_ref, "verification_record_ref"))
        identity = _require_string(self.artifact_identity, "artifact_identity")
        if not RUNTIME_PACK_ID_RE.fullmatch(identity):
            raise ModelValidationError("artifact_identity", "invalid_runtime_pack_identity", "artifact identity is not a Runtime Pack identity")
        object.__setattr__(self, "artifact_identity", identity)
        object.__setattr__(self, "artifact_version", _require_string(self.artifact_version, "artifact_version"))
        object.__setattr__(self, "artifact_digest", _require_digest(self.artifact_digest, "artifact_digest"))
        checks = _string_mapping(self.checks, "checks")
        unknown = set(checks) - set(VERIFICATION_CHECKS)
        if unknown:
            raise ModelValidationError("checks", "unknown_verification_check", f"unknown checks: {', '.join(sorted(unknown))}")
        if any(value not in {"pass", "fail", "blocked", "not_required"} for value in checks.values()):
            raise ModelValidationError("checks", "invalid_check_outcome", "check outcomes must be pass, fail, blocked, or not_required")
        object.__setattr__(self, "checks", checks)
        if self.outcome == "verified":
            if not self.activation_eligible or any(checks.get(name) not in {"pass", "not_required"} for name in VERIFICATION_CHECKS):
                raise ModelValidationError("activation_eligible", "inconsistent_verification", "verified result requires eligible status and successful checks")
        elif self.activation_eligible:
            raise ModelValidationError("activation_eligible", "eligible_nonverified_pack", "nonverified Runtime Packs cannot be activation eligible")
        if self.receipt.transition != "runtime_pack_validation" or self.receipt.outcome != self.outcome:
            raise ModelValidationError("receipt", "mismatched_verification_receipt", "verification receipt does not match the result")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome,
            "activation_eligible": self.activation_eligible,
            "verification_record_ref": self.verification_record_ref,
            "artifact_identity": self.artifact_identity,
            "artifact_version": self.artifact_version,
            "artifact_digest": self.artifact_digest,
            "checks": dict(self.checks),
            "receipt": self.receipt.to_mapping(),
        }


@dataclass(frozen=True, slots=True)
class RuntimePackActivationRequest:
    request_id: str
    correlation_id: str
    activation_request_id: str
    verified_runtime_pack_ref: str
    authorization_ref: str
    resource_grant_ref: str

    def __post_init__(self) -> None:
        for name in ("request_id", "correlation_id", "activation_request_id", "verified_runtime_pack_ref", "authorization_ref", "resource_grant_ref"):
            object.__setattr__(self, name, _require_reference(getattr(self, name), name))

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], request: ApiRequest) -> "RuntimePackActivationRequest":
        data = _mapping(payload, "payload")
        required = {"activation_request_id", "verified_runtime_pack_ref", "authorization_ref", "resource_grant_ref"}
        _reject_unknown(data, required, "payload")
        return cls(
            request.request_id,
            request.correlation_id,
            _require_string(data.get("activation_request_id"), "activation_request_id"),
            _require_string(data.get("verified_runtime_pack_ref"), "verified_runtime_pack_ref"),
            _require_string(data.get("authorization_ref"), "authorization_ref"),
            _require_string(data.get("resource_grant_ref"), "resource_grant_ref"),
        )


@dataclass(frozen=True, slots=True)
class RuntimePackRollbackRequest:
    request_id: str
    correlation_id: str
    rollback_request_id: str
    target_last_valid_runtime_ref: str
    authorization_ref: str

    def __post_init__(self) -> None:
        for name in ("request_id", "correlation_id", "rollback_request_id", "target_last_valid_runtime_ref", "authorization_ref"):
            object.__setattr__(self, name, _require_reference(getattr(self, name), name))

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], request: ApiRequest) -> "RuntimePackRollbackRequest":
        data = _mapping(payload, "payload")
        _reject_unknown(data, {"rollback_request_id", "target_last_valid_runtime_ref", "authorization_ref"}, "payload")
        return cls(
            request.request_id,
            request.correlation_id,
            _require_string(data.get("rollback_request_id"), "rollback_request_id"),
            _require_string(data.get("target_last_valid_runtime_ref"), "target_last_valid_runtime_ref"),
            _require_string(data.get("authorization_ref"), "authorization_ref"),
        )


@dataclass(frozen=True, slots=True)
class RuntimePackTransitionResult:
    transition: str
    outcome: str
    active_runtime_identity: str | None
    last_valid_state_preserved: bool
    receipt: Receipt

    def __post_init__(self) -> None:
        if self.transition not in {"runtime_pack_activation", "runtime_pack_rollback"}:
            raise ModelValidationError("transition", "invalid_transition", "transition result is not registered")
        allowed = (
            {"activated", "blocked", "failed"}
            if self.transition == "runtime_pack_activation"
            else {"rolled_back", "blocked", "failed", "forward_repair_required"}
        )
        if self.outcome not in allowed:
            raise ModelValidationError("outcome", "invalid_transition_outcome", "transition outcome is not registered")
        if not isinstance(self.last_valid_state_preserved, bool):
            raise ModelValidationError("last_valid_state_preserved", "invalid_boolean", "last_valid_state_preserved must be boolean")
        if self.active_runtime_identity is not None:
            identity = _require_string(self.active_runtime_identity, "active_runtime_identity")
            if not RUNTIME_PACK_ID_RE.fullmatch(identity):
                raise ModelValidationError("active_runtime_identity", "invalid_runtime_pack_identity", "active identity is not a Runtime Pack identity")
            object.__setattr__(self, "active_runtime_identity", identity)
        success = self.outcome in {"activated", "rolled_back"}
        if success and self.active_runtime_identity is None:
            raise ModelValidationError("active_runtime_identity", "missing_active_runtime", "successful transition requires an active Runtime Pack identity")
        if not success and not self.last_valid_state_preserved:
            raise ModelValidationError(
                "last_valid_state_preserved",
                "unsafe_transition_failure",
                "failed or blocked transition must preserve the last valid state",
            )
        expected_receipt_outcome = self.outcome
        if self.receipt.transition != self.transition or self.receipt.outcome != expected_receipt_outcome:
            raise ModelValidationError("receipt", "mismatched_transition_receipt", "transition receipt does not match the result")

    def to_mapping(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "transition": self.transition,
            "outcome": self.outcome,
            "last_valid_state_preserved": self.last_valid_state_preserved,
            "receipt": self.receipt.to_mapping(),
        }
        if self.active_runtime_identity is not None:
            result["active_runtime_identity"] = self.active_runtime_identity
        return result


@dataclass(frozen=True, slots=True)
class RuntimeStatusRequest:
    request_id: str
    correlation_id: str
    authorized_status_scope: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _require_reference(self.request_id, "request_id"))
        object.__setattr__(self, "correlation_id", _require_reference(self.correlation_id, "correlation_id"))
        object.__setattr__(self, "authorized_status_scope", _require_reference(self.authorized_status_scope, "authorized_status_scope"))

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], request: ApiRequest) -> "RuntimeStatusRequest":
        data = _mapping(payload, "payload")
        _reject_unknown(data, {"authorized_status_scope"}, "payload")
        return cls(request.request_id, request.correlation_id, _require_string(data.get("authorized_status_scope"), "authorized_status_scope"))


@dataclass(frozen=True, slots=True)
class HealthVector:
    state: str
    process_alive: bool
    startup_complete: bool
    contract_ready: bool
    read_ready: bool
    write_ready: bool
    activation_ready: bool
    degraded_capabilities: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.state not in RUNTIME_STATES:
            raise ModelValidationError("state", "invalid_runtime_state", "runtime state is not registered")
        for name in ("process_alive", "startup_complete", "contract_ready", "read_ready", "write_ready", "activation_ready"):
            if not isinstance(getattr(self, name), bool):
                raise ModelValidationError(name, "invalid_boolean", f"{name} must be boolean")
        object.__setattr__(self, "degraded_capabilities", _string_sequence(self.degraded_capabilities, "degraded_capabilities"))
        object.__setattr__(self, "blockers", _string_sequence(self.blockers, "blockers"))
        if not self.process_alive and any((self.startup_complete, self.contract_ready, self.read_ready, self.write_ready, self.activation_ready)):
            raise ModelValidationError("process_alive", "inconsistent_health", "an unavailable process cannot report readiness")
        if self.activation_ready and not (self.contract_ready and self.write_ready):
            raise ModelValidationError("activation_ready", "inconsistent_activation_readiness", "activation readiness requires contract and write readiness")
        if self.state == "active" and not self.read_ready:
            raise ModelValidationError("read_ready", "inconsistent_active_state", "an active runtime must be readable")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "process_alive": self.process_alive,
            "startup_complete": self.startup_complete,
            "contract_ready": self.contract_ready,
            "read_ready": self.read_ready,
            "write_ready": self.write_ready,
            "activation_ready": self.activation_ready,
            "degraded_capabilities": list(self.degraded_capabilities),
            "blockers": list(self.blockers),
        }


@dataclass(frozen=True, slots=True)
class RuntimeStatusResponse:
    active_runtime_identity: str | None
    verification_state: str
    activation_state: str
    health_state: HealthVector
    verification_record_ref: str | None = None
    activation_record_ref: str | None = None

    def __post_init__(self) -> None:
        if self.active_runtime_identity is not None:
            identity = _require_string(self.active_runtime_identity, "active_runtime_identity")
            if not RUNTIME_PACK_ID_RE.fullmatch(identity):
                raise ModelValidationError("active_runtime_identity", "invalid_runtime_pack_identity", "active identity is not a Runtime Pack identity")
            object.__setattr__(self, "active_runtime_identity", identity)
        if self.verification_state not in RUNTIME_STATES:
            raise ModelValidationError("verification_state", "invalid_runtime_state", "verification state is not registered")
        if self.activation_state not in RUNTIME_STATES:
            raise ModelValidationError("activation_state", "invalid_runtime_state", "activation state is not registered")
        if self.verification_record_ref is not None:
            object.__setattr__(self, "verification_record_ref", _require_reference(self.verification_record_ref, "verification_record_ref"))
        if self.activation_record_ref is not None:
            object.__setattr__(self, "activation_record_ref", _require_reference(self.activation_record_ref, "activation_record_ref"))
        if self.activation_state == "active" and self.active_runtime_identity is None:
            raise ModelValidationError("active_runtime_identity", "missing_active_runtime", "active state requires an active Runtime Pack identity")

    def to_mapping(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "verification_state": self.verification_state,
            "activation_state": self.activation_state,
            "health_state": self.health_state.to_mapping(),
        }
        if self.active_runtime_identity is not None:
            result["active_runtime_identity"] = self.active_runtime_identity
        if self.verification_record_ref is not None:
            result["verification_record_ref"] = self.verification_record_ref
        if self.activation_record_ref is not None:
            result["activation_record_ref"] = self.activation_record_ref
        return result


def _validate_runtime_pack_boundary(pack: Mapping[str, Any]) -> None:
    required = {
        "schema_version",
        "artifact_class",
        "artifact_identity",
        "artifact_version",
        "release_channel",
        "lifecycle",
        "created_at",
        "artifact_digest",
        "digest_scope",
        "provenance",
        "compatibility_constraints",
        "manifest",
        "verification",
        "activation_contract",
        "replacement_policy",
        "content_handling",
        "disclosure",
    }
    missing = sorted(required - set(pack))
    if missing:
        raise ModelValidationError("runtime_pack", "runtime_pack_fields_missing", f"missing fields: {', '.join(missing)}")
    if pack.get("schema_version") != "1.0.0":
        raise ModelValidationError("runtime_pack.schema_version", "invalid_schema_version", "Runtime Pack schema_version must be 1.0.0")
    if pack.get("artifact_class") != "runtime_pack":
        raise ModelValidationError("runtime_pack.artifact_class", "invalid_artifact_class", "artifact_class must be runtime_pack")
    identity = _require_string(pack.get("artifact_identity"), "runtime_pack.artifact_identity")
    if not RUNTIME_PACK_ID_RE.fullmatch(identity):
        raise ModelValidationError("runtime_pack.artifact_identity", "invalid_runtime_pack_identity", "artifact_identity is not a Runtime Pack identity")
    _require_string(pack.get("artifact_version"), "runtime_pack.artifact_version")
    if pack.get("release_channel") != KNOWLEDGE_RELEASE_CHANNEL:
        raise ModelValidationError("runtime_pack.release_channel", "wrong_release_channel", "Runtime Packs must use the knowledge release channel")
    if pack.get("digest_scope") != "canonical_manifest_and_payload":
        raise ModelValidationError("runtime_pack.digest_scope", "invalid_digest_scope", "Runtime Pack digest scope is not canonical")
    _require_digest(pack.get("artifact_digest"), "runtime_pack.artifact_digest")
    compatibility = _mapping(pack.get("compatibility_constraints"), "runtime_pack.compatibility_constraints")
    if (
        compatibility.get("target_component") != COMPONENT_ID
        or compatibility.get("target_component_contract_ref") != COMPONENT_CONTRACT
    ):
        raise ModelValidationError(
            "runtime_pack.compatibility_constraints",
            "wrong_target_component",
            "Runtime Pack does not target the active Kristal Runtime contract",
        )
    verification = _mapping(pack.get("verification"), "runtime_pack.verification")
    if tuple(verification.get("required_checks", ())) != VERIFICATION_CHECKS:
        raise ModelValidationError(
            "runtime_pack.verification.required_checks",
            "invalid_verification_checks",
            "verification checks do not match the Runtime Pack contract",
        )
    if (
        verification.get("quarantine_on_nonverified_outcome") is not True
        or verification.get("reverify_after_integrity_scope_change") is not True
    ):
        raise ModelValidationError(
            "runtime_pack.verification",
            "unsafe_verification_policy",
            "nonverified or changed artifacts must be quarantined and reverified",
        )
    activation = _mapping(pack.get("activation_contract"), "runtime_pack.activation_contract")
    expected_activation = {
        "owner_component": COMPONENT_ID,
        "component_contract_ref": COMPONENT_CONTRACT,
        "interface_id": "runtime_pack_activation",
        "activation_boundary": "active_runtime_pack_record",
        "activation_mode": "atomic_pointer_switch",
        "partial_authoritative_activation_allowed": False,
        "last_valid_state_retained_until_success": True,
        "verification_receipt_required": True,
        "authorization_required": True,
        "resource_grant_required": True,
    }
    for key, expected in expected_activation.items():
        if activation.get(key) != expected:
            raise ModelValidationError(
                f"runtime_pack.activation_contract.{key}",
                "unsafe_activation_contract",
                f"{key} does not match the canonical activation contract",
            )
    replacement = _mapping(pack.get("replacement_policy"), "runtime_pack.replacement_policy")
    for key, expected in {
        "implicit_downgrade_allowed": False,
        "implicit_substitution_allowed": False,
        "authorization_required": True,
        "compatibility_validation_required": True,
    }.items():
        if replacement.get(key) != expected:
            raise ModelValidationError(
                f"runtime_pack.replacement_policy.{key}",
                "unsafe_replacement_policy",
                f"{key} does not match the canonical replacement policy",
            )
    handling = _mapping(pack.get("content_handling"), "runtime_pack.content_handling")
    for key, expected in {
        "immutable_after_publication": True,
        "unverified_execution_allowed": False,
        "direct_cross_component_mutation_allowed": False,
        "secret_values_allowed": False,
    }.items():
        if handling.get(key) != expected:
            raise ModelValidationError(
                f"runtime_pack.content_handling.{key}",
                "unsafe_content_handling",
                f"{key} does not match the canonical content policy",
            )
    disclosure = _mapping(pack.get("disclosure"), "runtime_pack.disclosure")
    if disclosure.get("contains_secret_values") is not False:
        raise ModelValidationError("runtime_pack.disclosure.contains_secret_values", "secret_values_forbidden", "Runtime Packs cannot contain secret values")
    _reject_sensitive_keys(pack, "runtime_pack")


def _reject_sensitive_keys(value: object, field_name: str) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str) and SENSITIVE_KEY_RE.search(key) and item is not False:
                raise ModelValidationError(field_name, "sensitive_field_forbidden", f"sensitive field is forbidden: {key}")
            _reject_sensitive_keys(item, field_name)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            _reject_sensitive_keys(item, field_name)


def _mapping(value: object, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ModelValidationError(field_name, "invalid_mapping", f"{field_name} must be an object")
    result: dict[str, Any] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise ModelValidationError(field_name, "invalid_mapping_key", f"{field_name} keys must be strings")
        result[key] = item
    return MappingProxyType(result)


def _string_mapping(value: object, field_name: str) -> Mapping[str, str]:
    data = _mapping(value, field_name)
    return MappingProxyType({key: _require_string(item, f"{field_name}.{key}") for key, item in data.items()})


def _require_string(value: object, field_name: str, *, max_length: int = 2048) -> str:
    if not isinstance(value, str):
        raise ModelValidationError(field_name, "invalid_string", f"{field_name} must be a string")
    result = value.strip()
    if not result:
        raise ModelValidationError(field_name, "empty_string", f"{field_name} must not be empty")
    if len(result) > max_length:
        raise ModelValidationError(field_name, "string_too_long", f"{field_name} exceeds {max_length} characters")
    if any(ord(char) < 32 for char in result):
        raise ModelValidationError(field_name, "control_character", f"{field_name} contains a control character")
    return result


def _optional_string(value: object, field_name: str) -> str | None:
    return None if value is None else _require_string(value, field_name)


def _require_token(value: object, field_name: str) -> str:
    result = _require_string(value, field_name, max_length=128)
    if not re.fullmatch(r"[a-z][a-z0-9_]*", result):
        raise ModelValidationError(field_name, "invalid_token", f"{field_name} must be a lower snake-case token")
    return result


def _require_reference(value: object, field_name: str) -> str:
    result = _require_string(value, field_name, max_length=2048)
    if result.startswith("/") or "../" in result or result == "..":
        raise ModelValidationError(field_name, "unsafe_reference", f"{field_name} is not a safe canonical reference")
    return result


def _require_digest(value: object, field_name: str) -> str:
    result = _require_string(value, field_name, max_length=160)
    if not DIGEST_RE.fullmatch(result):
        raise ModelValidationError(field_name, "invalid_digest", f"{field_name} must be a supported canonical digest")
    return result


def _string_sequence(value: object, field_name: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise ModelValidationError(field_name, "invalid_sequence", f"{field_name} must be an array of strings")
    result = tuple(_require_reference(item, field_name) for item in value)
    if len(set(result)) != len(result):
        raise ModelValidationError(field_name, "duplicate_value", f"{field_name} must contain unique values")
    return result


def _reject_unknown(data: Mapping[str, Any], allowed: set[str], field_name: str) -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ModelValidationError(field_name, "unknown_field", f"unknown fields: {', '.join(unknown)}")


def _public_mapping(value: object) -> Mapping[str, Any]:
    method = getattr(value, "to_mapping", None)
    if not callable(method):
        raise ModelValidationError("result", "invalid_service_result", "service result is not a public API model")
    return _mapping(method(), "result")
