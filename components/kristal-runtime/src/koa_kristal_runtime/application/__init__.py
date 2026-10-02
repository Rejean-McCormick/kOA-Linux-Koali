"""Application boundary for Kristal Runtime.

The application layer accepts JSON-compatible mappings so that the concrete
B-0045 domain objects and B-0017 interface bindings can be connected without
this bundle importing or recreating them.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import asdict, dataclass, is_dataclass
from hashlib import sha256
import json
import math
import re
from types import MappingProxyType
from typing import Any, Final

_JSON_SCALAR = str | int | float | bool | None
JsonValue = _JSON_SCALAR | list["JsonValue"] | dict[str, "JsonValue"]
JsonMapping = Mapping[str, JsonValue]

ACCEPTED_ARTIFACT_CLASSES: Final[frozenset[str]] = frozenset(
    {"kristal_state", "kristal_artifact", "runtime_pack"}
)
TERMINAL_LIFECYCLE_STATES: Final[frozenset[str]] = frozenset(
    {"revoked", "retired"}
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SHA256_URI_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
KRISTAL_V6_STANDARD_VERSION: Final[str] = "6.0.0"
KRISTAL_V6_SCHEMA_VERSION: Final[str] = "6.0"
KRISTAL_V6_CANONICALIZATION_PROFILE: Final[str] = "kristal.v6:jcs-rfc8785"
KRISTAL_V6_CANONICALIZATION_VERSION: Final[str] = "1"
_KRISTAL_V6_HASH_EXCLUSIONS: Final[frozenset[str]] = frozenset({"state_id", "content_hash", "signatures"})
_KRISTAL_V6_VALUE_STATES: Final[frozenset[str]] = frozenset({"known", "unknown", "not_applicable", "indeterminate", "not_measured"})
_KRISTAL_V6_VALUE_SEMANTICS: Final[frozenset[str]] = frozenset({"boolean", "categorical", "set", "ordinal", "scalar", "interval", "probability", "distribution", "vector", "partial_order", "state", "temporal"})
_KRISTAL_V6_RECORD_ROLES: Final[frozenset[str]] = frozenset({"authoritative_constraint", "observed_state", "organizational_rule", "derived_state", "decision", "action", "reference_knowledge", "structural"})
_KRISTAL_V6_ACTIONABILITY_MODES: Final[frozenset[str]] = frozenset({"automatic", "human_review", "human_decision", "manual", "prohibited", "insufficient_information", "not_applicable"})
_KRISTAL_V5_FIELDS: Final[frozenset[str]] = frozenset({"certainty_level", "uncertainty", "qualifiers", "scope"})
_MAX_IJSON_INTEGER: Final[int] = 9007199254740991
_RUNTIME_DIGEST_RE = re.compile(r"^sha(?:256|384|512):[0-9a-f]+$")


class ApplicationError(RuntimeError):
    """Closed, machine-readable application failure."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: Mapping[str, JsonValue] | None = None,
    ) -> None:
        if not code or not re.fullmatch(r"[a-z][a-z0-9_]*", code):
            raise ValueError("application error codes must be lower snake case")
        super().__init__(message)
        self.code = code
        self.details = freeze_mapping(details or {})


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    """Stable reference to an admitted artifact."""

    artifact_class: str
    artifact_id: str
    artifact_version: str
    content_digest: str

    def as_mapping(self) -> Mapping[str, JsonValue]:
        return freeze_mapping(
            {
                "artifact_class": self.artifact_class,
                "artifact_id": self.artifact_id,
                "artifact_version": self.artifact_version,
                "content_digest": self.content_digest,
            }
        )


def as_mapping(value: object, *, name: str) -> Mapping[str, JsonValue]:
    """Convert a mapping, dataclass, or public ``to_mapping`` object safely."""

    candidate: object
    if isinstance(value, Mapping):
        candidate = value
    elif is_dataclass(value) and not isinstance(value, type):
        candidate = asdict(value)
    else:
        converter = getattr(value, "to_mapping", None)
        if not callable(converter):
            raise ApplicationError(
                "invalid_input",
                f"{name} must be a mapping or expose to_mapping()",
            )
        candidate = converter()
    if not isinstance(candidate, Mapping):
        raise ApplicationError("invalid_input", f"{name} did not resolve to a mapping")
    return freeze_mapping(candidate)


def freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, JsonValue]:
    """Return an immutable, detached, JSON-compatible mapping."""

    try:
        detached = json.loads(
            json.dumps(thaw(value), ensure_ascii=False, allow_nan=False, sort_keys=True)
        )
    except (TypeError, ValueError) as exc:
        raise ApplicationError(
            "non_json_value",
            "application inputs and port results must be JSON-compatible",
        ) from exc
    if not isinstance(detached, dict):
        raise ApplicationError("invalid_mapping", "expected a JSON object")
    return _deep_freeze(detached)


def thaw(value: JsonValue | Mapping[str, JsonValue] | Sequence[JsonValue]) -> JsonValue:
    """Return a detached mutable JSON value for a port invocation."""

    if isinstance(value, Mapping):
        return {str(k): thaw(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [thaw(v) for v in value]
    if isinstance(value, list):
        return [thaw(v) for v in value]
    return deepcopy(value)


def _deep_freeze(value: JsonValue) -> JsonValue:
    if isinstance(value, dict):
        return MappingProxyType({k: _deep_freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(v) for v in value)  # type: ignore[return-value]
    return value


def _jcs_validate_string(value: str) -> None:
    for character in value:
        if 0xD800 <= ord(character) <= 0xDFFF:
            raise ApplicationError("non_json_value", "lone surrogate is not valid I-JSON")


def _jcs_string(value: str) -> str:
    _jcs_validate_string(value)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _jcs_utf16_sort_key(value: str) -> bytes:
    _jcs_validate_string(value)
    return value.encode("utf-16-be")


def _jcs_number(value: int | float) -> str:
    if isinstance(value, bool):
        raise ApplicationError("non_json_value", "boolean is not a JCS number")
    if isinstance(value, int):
        if abs(value) > _MAX_IJSON_INTEGER:
            raise ApplicationError("non_json_value", "integer is outside the interoperable I-JSON range")
        return str(value)
    if not math.isfinite(value):
        raise ApplicationError("non_json_value", "non-finite number is not valid I-JSON")
    if value == 0.0:
        return "0"
    negative = value < 0
    number = -value if negative else value
    raw = repr(number).lower()
    if "e" in raw:
        mantissa, exponent_text = raw.split("e", 1)
        exponent = int(exponent_text)
    else:
        mantissa, exponent = raw, 0
    if "." in mantissa:
        before, after = mantissa.split(".", 1)
        digits = before + after
        decimal_pos = len(before) + exponent
    else:
        digits = mantissa
        decimal_pos = len(mantissa) + exponent
    while len(digits) > 1 and digits[0] == "0":
        digits = digits[1:]
        decimal_pos -= 1
    while len(digits) > 1 and digits[-1] == "0":
        digits = digits[:-1]
    scientific_exponent = decimal_pos - 1
    if 1e-6 <= number < 1e21:
        if decimal_pos <= 0:
            rendered = "0." + ("0" * (-decimal_pos)) + digits
        elif decimal_pos >= len(digits):
            rendered = digits + ("0" * (decimal_pos - len(digits)))
        else:
            rendered = digits[:decimal_pos] + "." + digits[decimal_pos:]
    else:
        rendered_mantissa = digits if len(digits) == 1 else digits[0] + "." + digits[1:]
        sign = "+" if scientific_exponent >= 0 else ""
        rendered = f"{rendered_mantissa}e{sign}{scientific_exponent}"
    return "-" + rendered if negative else rendered


def _jcs_render(value: object) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return _jcs_string(value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return _jcs_number(value)
    if isinstance(value, Mapping):
        for key in value:
            if not isinstance(key, str):
                raise ApplicationError("non_json_value", "JSON object keys must be strings")
        keys = sorted(value, key=_jcs_utf16_sort_key)
        return "{" + ",".join(_jcs_string(key) + ":" + _jcs_render(value[key]) for key in keys) + "}"
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return "[" + ",".join(_jcs_render(item) for item in value) + "]"
    raise ApplicationError("non_json_value", f"unsupported JSON value type: {type(value).__name__}")


def canonical_json(value: object) -> bytes:
    """Return RFC 8785 JCS bytes for JSON-compatible content."""

    return _jcs_render(value).encode("utf-8")


def kristal_state_content_digest(artifact: Mapping[str, Any]) -> str:
    """Return the Kristal v6 content hash after the declared top-level exclusions."""

    policy = artifact.get("hash_target_policy")
    if not isinstance(policy, Mapping):
        raise ApplicationError("kristal_v6_hash_policy_invalid", "hash_target_policy is required")
    exclusions = policy.get("exclude_fields")
    if not isinstance(exclusions, (list, tuple)) or isinstance(exclusions, (str, bytes)):
        raise ApplicationError("kristal_v6_hash_policy_invalid", "exclude_fields must be an array")
    if set(exclusions) != _KRISTAL_V6_HASH_EXCLUSIONS or len(exclusions) != len(set(exclusions)):
        raise ApplicationError(
            "kristal_v6_hash_policy_invalid",
            "Kristal v6 identity must exclude exactly state_id, content_hash, and signatures",
        )
    target = {str(key): thaw(value) for key, value in artifact.items() if key not in _KRISTAL_V6_HASH_EXCLUSIONS}
    return sha256(canonical_json(target)).hexdigest()


def deterministic_id(prefix: str, *values: object) -> str:
    digest = sha256()
    for value in values:
        if isinstance(value, Mapping):
            digest.update(canonical_json(value))
        else:
            digest.update(str(value).encode("utf-8"))
        digest.update(b"\x00")
    return f"{prefix}:{digest.hexdigest()}"


def require_non_empty_string(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ApplicationError("artifact_invalid", f"{key} must be a non-empty string")
    return value.strip()


def require_mapping(mapping: Mapping[str, Any], key: str) -> Mapping[str, JsonValue]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise ApplicationError("artifact_invalid", f"{key} must be an object")
    return freeze_mapping(value)


def require_sequence(mapping: Mapping[str, Any], key: str) -> tuple[JsonValue, ...]:
    value = mapping.get(key)
    if not isinstance(value, (list, tuple)) or isinstance(value, (str, bytes)):
        raise ApplicationError("artifact_invalid", f"{key} must be an array")
    return tuple(value)


def artifact_ref_from(artifact: Mapping[str, JsonValue]) -> ArtifactRef:
    if artifact.get("artifact_type") == "kristal_state":
        state_id = require_non_empty_string(artifact, "state_id")
        schema_version = require_non_empty_string(artifact, "schema_version")
        if schema_version != KRISTAL_V6_SCHEMA_VERSION or not _SHA256_URI_RE.fullmatch(state_id):
            raise ApplicationError("content_identity_invalid", "Kristal State must use v6 sha256 content identity")
        digest = kristal_state_content_digest(artifact)
        if state_id != f"sha256:{digest}":
            raise ApplicationError("content_identity_invalid", "Kristal State state_id does not match RFC 8785 content")
        content_hash = require_mapping(artifact, "content_hash")
        if content_hash.get("alg") != "sha256" or content_hash.get("value") != digest:
            raise ApplicationError("content_identity_invalid", "Kristal State content_hash does not match canonical content")
        return ArtifactRef("kristal_state", state_id, schema_version, state_id)

    artifact_class = require_non_empty_string(artifact, "artifact_class")
    if artifact_class not in ACCEPTED_ARTIFACT_CLASSES:
        raise ApplicationError(
            "unsupported_artifact_class",
            f"unsupported artifact class: {artifact_class}",
        )
    if artifact_class == "kristal_artifact":
        artifact_id = require_non_empty_string(artifact, "artifact_id")
        artifact_version = require_non_empty_string(artifact, "artifact_version")
        identity = require_mapping(artifact, "content_identity")
        algorithm = require_non_empty_string(identity, "algorithm")
        digest = require_non_empty_string(identity, "digest")
        if algorithm != "sha256" or not _SHA256_RE.fullmatch(digest):
            raise ApplicationError(
                "content_identity_invalid",
                "Kristal content identity must be a lowercase sha256 digest",
            )
        return ArtifactRef(artifact_class, artifact_id, artifact_version, f"sha256:{digest}")

    artifact_id = require_non_empty_string(artifact, "artifact_identity")
    artifact_version = require_non_empty_string(artifact, "artifact_version")
    digest = require_non_empty_string(artifact, "artifact_digest")
    if not artifact_id.startswith("runtime-pack:") or not _RUNTIME_DIGEST_RE.fullmatch(digest):
        raise ApplicationError(
            "content_identity_invalid",
            "Runtime Pack identity or digest is invalid",
        )
    return ArtifactRef(artifact_class, artifact_id, artifact_version, digest)


def _reject_v5_fields(value: Mapping[str, Any], path: str) -> None:
    forbidden = _KRISTAL_V5_FIELDS.intersection(value)
    if forbidden:
        names = ", ".join(sorted(forbidden))
        raise ApplicationError("kristal_v5_field_forbidden", f"Kristal v6 forbids legacy field(s) {names} at {path}")


def _validate_kristal_state_v6(artifact: Mapping[str, JsonValue]) -> None:
    if artifact.get("schema_version") != KRISTAL_V6_SCHEMA_VERSION:
        raise ApplicationError("kristal_v6_schema_invalid", "schema_version must be 6.0")
    if artifact.get("canonicalization_profile") != KRISTAL_V6_CANONICALIZATION_PROFILE:
        raise ApplicationError("kristal_v6_canonicalization_invalid", "Kristal v6 requires kristal.v6:jcs-rfc8785")
    if artifact.get("canonicalization_version") != KRISTAL_V6_CANONICALIZATION_VERSION:
        raise ApplicationError("kristal_v6_canonicalization_invalid", "Kristal v6 canonicalization_version must be 1")
    _reject_v5_fields(artifact, "$")
    require_non_empty_string(artifact, "artifact_status")
    require_non_empty_string(artifact, "created_at")
    require_mapping(artifact, "created_by")
    state_applicability = require_mapping(artifact, "applicability")
    require_non_empty_string(state_applicability, "domain")
    assertions = require_sequence(artifact, "assertions")
    if not assertions:
        raise ApplicationError("kristal_v6_assertions_invalid", "Kristal State assertions cannot be empty")
    provenance = require_sequence(artifact, "provenance")
    for item in provenance:
        if not isinstance(item, Mapping):
            raise ApplicationError("missing_provenance", "Kristal v6 provenance entries must be objects")
        require_non_empty_string(item, "provenance_id")
        require_non_empty_string(item, "event_type")
        require_non_empty_string(item, "created_at")
    for assertion in assertions:
        if not isinstance(assertion, Mapping):
            raise ApplicationError("kristal_v6_assertions_invalid", "assertions must contain objects")
        _reject_v5_fields(assertion, "$.assertions[]")
        assertion_id = require_non_empty_string(assertion, "assertion_id")
        if not _SHA256_URI_RE.fullmatch(assertion_id):
            raise ApplicationError("kristal_v6_assertions_invalid", "assertion_id must be a sha256 URI")
        require_non_empty_string(assertion, "assertion_status")
        statement = require_mapping(assertion, "statement")
        _reject_v5_fields(statement, "$.assertions[].statement")
        for field in ("subject", "predicate", "object"):
            if field not in statement:
                raise ApplicationError("kristal_v6_assertions_invalid", f"statement.{field} is required")
        assertion_applicability = require_mapping(assertion, "applicability")
        require_non_empty_string(assertion_applicability, "domain")
        valuations = require_sequence(assertion, "valuations")
        if not valuations:
            raise ApplicationError("kristal_v6_valuation_invalid", "valuations cannot be empty")
        for valuation in valuations:
            if not isinstance(valuation, Mapping):
                raise ApplicationError("kristal_v6_valuation_invalid", "valuation entries must be objects")
            require_non_empty_string(valuation, "dimension")
            semantics = require_non_empty_string(valuation, "value_semantics")
            state = require_non_empty_string(valuation, "value_state")
            if semantics not in _KRISTAL_V6_VALUE_SEMANTICS or state not in _KRISTAL_V6_VALUE_STATES:
                raise ApplicationError("kristal_v6_valuation_invalid", "valuation semantics or state is not registered")
            if state == "known" and "value" not in valuation:
                raise ApplicationError("kristal_v6_valuation_invalid", "known valuations require value")
            if state != "known" and "value" in valuation:
                raise ApplicationError("kristal_v6_valuation_invalid", "non-known valuations must not contain value")
        role = assertion.get("record_role")
        if role is not None and role not in _KRISTAL_V6_RECORD_ROLES:
            raise ApplicationError("kristal_v6_record_role_invalid", "record_role is not registered")
        actionability = assertion.get("actionability")
        if actionability is not None:
            if not isinstance(actionability, Mapping):
                raise ApplicationError("kristal_v6_actionability_invalid", "actionability must be an object")
            mode = actionability.get("mode")
            if mode not in _KRISTAL_V6_ACTIONABILITY_MODES:
                raise ApplicationError("kristal_v6_actionability_invalid", "actionability.mode is not registered")
    # Identity verification deliberately occurs after semantic checks.  Automatic
    # actionability is data, never a grant of execution authority.
    artifact_ref_from(artifact)


def validate_artifact_structure(artifact: Mapping[str, JsonValue]) -> ArtifactRef:
    """Validate contract-critical invariants without replacing schema validation."""

    if artifact.get("artifact_type") == "kristal_state":
        _validate_kristal_state_v6(artifact)
        return artifact_ref_from(artifact)

    ref = artifact_ref_from(artifact)
    manifest = require_mapping(artifact, "manifest")
    entries = require_sequence(manifest, "entries")
    if not entries:
        raise ApplicationError("manifest_invalid", "manifest entries cannot be empty")
    seen_paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, Mapping):
            raise ApplicationError("manifest_invalid", "manifest entries must be objects")
        path = require_non_empty_string(entry, "path")
        if path.startswith("/") or ".." in path.split("/") or "\\" in path:
            raise ApplicationError("unsafe_manifest_path", f"unsafe manifest path: {path}")
        if path in seen_paths:
            raise ApplicationError("manifest_invalid", f"duplicate manifest path: {path}")
        seen_paths.add(path)
        digest = entry.get("sha256") or entry.get("digest")
        if not isinstance(digest, str) or not digest:
            raise ApplicationError("manifest_invalid", f"manifest digest missing for {path}")

    provenance = require_mapping(artifact, "provenance")
    producer = provenance.get("producer")
    if isinstance(producer, Mapping):
        producer_id = producer.get("producer_id") or producer.get("id")
        if not isinstance(producer_id, str) or not producer_id.strip():
            raise ApplicationError("missing_provenance", "provenance producer identity is required")
    elif not isinstance(producer, str) or not producer.strip():
        raise ApplicationError("missing_provenance", "provenance producer is required")

    if ref.artifact_class == "runtime_pack":
        if artifact.get("release_channel") != "knowledge":
            raise ApplicationError(
                "release_channel_invalid",
                "Runtime Packs must use the knowledge release channel",
            )
        lifecycle = require_mapping(artifact, "lifecycle")
        status = require_non_empty_string(lifecycle, "status")
        if status in TERMINAL_LIFECYCLE_STATES:
            raise ApplicationError(
                "artifact_not_admissible",
                f"a {status} Runtime Pack cannot be admitted",
            )
        handling = require_mapping(artifact, "content_handling")
        if handling.get("secret_values_allowed") is not False:
            raise ApplicationError(
                "secret_content_forbidden",
                "Runtime Packs cannot permit secret values",
            )
    else:
        require_mapping(artifact, "rights")
        require_mapping(artifact, "compatibility")
    return ref



def evaluate_policy_port(
    evaluator: object,
    action: str,
    actor_context: Mapping[str, Any],
    resource: Mapping[str, Any],
    context: Mapping[str, Any],
) -> Any:
    """Invoke the policy authority and convert transport failure to blocked."""

    method = getattr(evaluator, "evaluate", None)
    if not callable(method):
        raise ApplicationError("policy_protocol_error", "policy evaluator has no evaluate method")
    try:
        decision = method(action, thaw(actor_context), thaw(resource), thaw(context))
    except ApplicationError:
        raise
    except Exception as exc:
        raise ApplicationError(
            "policy_unavailable",
            f"policy evaluation is unavailable for {action}",
        ) from exc
    outcome = getattr(decision, "outcome", None)
    if outcome not in {"allow", "deny", "blocked"}:
        raise ApplicationError("policy_protocol_error", "policy returned an unknown outcome")
    for field in ("decision_id", "policy_ref", "receipt_ref"):
        value = getattr(decision, field, None)
        if not isinstance(value, str) or not value:
            raise ApplicationError("policy_protocol_error", f"policy decision lacks {field}")
    obligations = getattr(decision, "obligations", None)
    if not isinstance(obligations, Mapping):
        raise ApplicationError("policy_protocol_error", "policy obligations must be an object")
    return decision


def record_evidence_port(audit_sink: object, event: Mapping[str, Any], operation: str) -> str:
    """Secure a durable evidence receipt or fail the operation explicitly."""

    method = getattr(audit_sink, "record", None)
    if not callable(method):
        raise ApplicationError("audit_unavailable", "audit sink has no record method")
    try:
        receipt = method(thaw(event))
    except ApplicationError:
        raise
    except Exception as exc:
        raise ApplicationError("audit_unavailable", f"{operation} evidence is unavailable") from exc
    if not isinstance(receipt, str) or not receipt:
        raise ApplicationError("audit_unavailable", f"{operation} evidence was not secured")
    return receipt



from .admit_artifact import AdmitArtifact, AdmissionResult
from .execute_query import ExecuteQuery, QueryResult
from .render_artifact import RenderArtifact, RenderResult
from .revoke_artifact import RevokeArtifact, RevocationResult
from .verify_artifact import VerifyArtifact, VerificationResult

__all__ = [
    "AdmitArtifact",
    "AdmissionResult",
    "ApplicationError",
    "ArtifactRef",
    "KRISTAL_V6_CANONICALIZATION_PROFILE",
    "KRISTAL_V6_STANDARD_VERSION",
    "ExecuteQuery",
    "QueryResult",
    "RenderArtifact",
    "RenderResult",
    "RevokeArtifact",
    "RevocationResult",
    "VerificationResult",
    "VerifyArtifact",
    "canonical_json",
    "kristal_state_content_digest",
    "validate_artifact_structure",
]
