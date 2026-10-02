"""Execute a declared bounded deterministic query against a verified artifact."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
from typing import Any

from ..ports import ArtifactStore, AuditSink, IndexStore, PolicyEvaluator
from . import (
    ApplicationError,
    ArtifactRef,
    JsonValue,
    as_mapping,
    canonical_json,
    deterministic_id,
    evaluate_policy_port,
    freeze_mapping,
    record_evidence_port,
    thaw,
    validate_artifact_structure,
)


@dataclass(frozen=True, slots=True)
class QueryResult:
    artifact: ArtifactRef
    query_contract_id: str
    query_contract_version: str
    query_class: str
    items: tuple[Mapping[str, JsonValue], ...]
    next_cursor: str | None
    total_count: int | None
    result_digest: str
    evidence_receipt_ref: str
    status: str
    provenance: Mapping[str, JsonValue]


class ExecuteQuery:
    def __init__(
        self,
        artifact_store: ArtifactStore,
        index_store: IndexStore,
        policy_evaluator: PolicyEvaluator,
        audit_sink: AuditSink,
    ) -> None:
        self._artifacts = artifact_store
        self._index = index_store
        self._policy = policy_evaluator
        self._audit = audit_sink

    def __call__(
        self,
        artifact_id: str,
        artifact_version: str,
        *,
        query_contract: object,
        query_class: str,
        parameters: object,
        actor_context: object,
        request_id: str,
        limit: int,
        cursor: str | None = None,
    ) -> QueryResult:
        for value, field in (
            (artifact_id, "artifact_id"),
            (artifact_version, "artifact_version"),
            (query_class, "query_class"),
            (request_id, "request_id"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ApplicationError("invalid_input", f"{field} is required")
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise ApplicationError("query_limit_invalid", "limit must be a positive integer")
        if cursor is not None and (not isinstance(cursor, str) or not cursor):
            raise ApplicationError("cursor_invalid", "cursor must be a non-empty opaque string")

        actor = as_mapping(actor_context, name="actor_context")
        params = as_mapping(parameters, name="parameters")
        contract = as_mapping(query_contract, name="query_contract")
        artifact = self._load_verified(artifact_id, artifact_version)
        ref = validate_artifact_structure(artifact)
        contract_id, contract_version, query_spec = _resolve_query_spec(contract, query_class)
        allowed_parameters = query_spec.get("allowed_parameter_keys", ())
        if allowed_parameters:
            extras = set(params) - set(allowed_parameters)
            if extras:
                raise ApplicationError(
                    "unsupported_query_parameter",
                    "query contains parameters outside the declared contract",
                    details={"parameters": sorted(extras)},
                )
        maximum = query_spec.get("max_items")
        if not isinstance(maximum, int) or maximum < 1:
            raise ApplicationError("query_contract_invalid", "max_items must be positive")
        effective_limit = min(limit, maximum)
        timeout_ms = query_spec.get("timeout_ms")
        if not isinstance(timeout_ms, int) or timeout_ms < 1:
            raise ApplicationError("query_contract_invalid", "timeout_ms must be positive")

        decision = evaluate_policy_port(
            self._policy,
            "kristal.query.execute",
            actor,
            {
                **thaw(ref.as_mapping()),
                "query_contract_id": contract_id,
                "query_class": query_class,
            },
            {"request_id": request_id, "parameters": thaw(params), "limit": limit},
        )
        _require_allow(decision.outcome, decision.reason_code)
        effective_limit, allowed_fields, redacted_fields = _apply_obligations(
            decision.obligations, effective_limit, query_spec
        )

        try:
            page = self._index.query(
                ref.artifact_id,
                ref.artifact_version,
                query_class,
                thaw(params),
                limit=effective_limit,
                cursor=cursor,
                timeout_ms=timeout_ms,
            )
        except ApplicationError:
            raise
        except Exception as exc:
            self._record_failure(request_id, ref, query_class, "index_unavailable")
            raise ApplicationError(
                "index_unavailable",
                "the local derived index is unavailable; no remote or AI fallback is permitted",
            ) from exc

        if len(page.items) > effective_limit:
            raise ApplicationError("index_protocol_error", "index returned more items than permitted")
        sort_fields = query_spec.get("sort_fields")
        tie_breaker = query_spec.get("tie_breaker")
        if not isinstance(sort_fields, (list, tuple)) or not sort_fields:
            raise ApplicationError("query_contract_invalid", "sort_fields are required")
        if not isinstance(tie_breaker, str) or not tie_breaker:
            raise ApplicationError("query_contract_invalid", "tie_breaker is required")
        source_items = [as_mapping(item, name="query item") for item in page.items]
        ordered_sources = sorted(
            source_items,
            key=lambda item: tuple(
                _sortable(_read_path(item, field)) for field in (*sort_fields, tie_breaker)
            ),
        )
        ordered = tuple(
            _project_item(item, allowed_fields, redacted_fields) for item in ordered_sources
        )
        digest = "sha256:" + sha256(canonical_json({"items": [thaw(x) for x in ordered]})).hexdigest()
        lifecycle_status = _artifact_status(artifact)
        provenance_raw = artifact.get("provenance", {})
        if isinstance(provenance_raw, (list, tuple)):
            provenance = freeze_mapping({"records": thaw(provenance_raw)})
        else:
            provenance = as_mapping(provenance_raw, name="provenance")
        event = {
            "event_id": deterministic_id("query", request_id, ref.as_mapping(), {"digest": digest}),
            "event_type": "kristal.query.completed",
            "outcome": "succeeded",
            "request_id": request_id,
            "artifact": thaw(ref.as_mapping()),
            "query_contract_id": contract_id,
            "query_contract_version": contract_version,
            "query_class": query_class,
            "result_digest": digest,
            "result_count": len(ordered),
            "policy_decision_id": decision.decision_id,
            "policy_receipt_ref": decision.receipt_ref,
        }
        receipt = record_evidence_port(self._audit, event, "query")
        return QueryResult(
            ref,
            contract_id,
            contract_version,
            query_class,
            ordered,
            page.next_cursor,
            page.total_count,
            digest,
            receipt,
            lifecycle_status,
            provenance,
        )

    def _load_verified(self, artifact_id: str, artifact_version: str) -> Mapping[str, JsonValue]:
        artifact = self._artifacts.get_artifact(artifact_id, artifact_version)
        if artifact is None:
            raise ApplicationError("artifact_not_found", "artifact is not admitted")
        if self._artifacts.get_revocation(artifact_id, artifact_version) is not None:
            raise ApplicationError("artifact_revoked", "revoked artifacts cannot be queried")
        verification = self._artifacts.get_verification(artifact_id, artifact_version)
        if verification is None or verification.get("outcome") != "verified":
            raise ApplicationError("artifact_not_verified", "artifact has no successful verification")
        return as_mapping(artifact, name="stored artifact")

    def _record_failure(self, request_id: str, ref: ArtifactRef, query_class: str, code: str) -> None:
        try:
            record_evidence_port(
                self._audit,
                {
                "event_id": deterministic_id("query-failure", request_id, ref.as_mapping(), code),
                "event_type": "kristal.query.failed",
                "outcome": "failed",
                "request_id": request_id,
                "artifact": thaw(ref.as_mapping()),
                "query_class": query_class,
                    "reason_code": code,
                },
                "query failure",
            )
        except ApplicationError:
            return


def _resolve_query_spec(
    contract: Mapping[str, JsonValue], query_class: str
) -> tuple[str, str, Mapping[str, JsonValue]]:
    contract_id = contract.get("contract_id")
    version = contract.get("version")
    classes = contract.get("query_classes")
    if not isinstance(contract_id, str) or not contract_id:
        raise ApplicationError("query_contract_invalid", "contract_id is required")
    if not isinstance(version, str) or not version:
        raise ApplicationError("query_contract_invalid", "query contract version is required")
    if not isinstance(classes, Mapping):
        raise ApplicationError("query_contract_invalid", "query_classes must be an object")
    spec = classes.get(query_class)
    if not isinstance(spec, Mapping):
        raise ApplicationError("unsupported_query_class", "query class is not declared")
    unsupported = contract.get("unsupported_operations", ())
    if query_class in unsupported:
        raise ApplicationError("unsupported_query_class", "query class is explicitly unsupported")
    return contract_id, version, as_mapping(spec, name="query specification")


def _apply_obligations(
    obligations: Mapping[str, Any],
    current_limit: int,
    query_spec: Mapping[str, JsonValue],
) -> tuple[int, frozenset[str] | None, frozenset[str]]:
    supported = {"max_items", "allowed_fields", "redact_fields"}
    unknown = set(obligations) - supported
    if unknown:
        raise ApplicationError(
            "unsupported_policy_obligation",
            "query policy returned obligations this runtime cannot enforce",
            details={"obligations": sorted(unknown)},
        )
    policy_limit = obligations.get("max_items", current_limit)
    if not isinstance(policy_limit, int) or isinstance(policy_limit, bool) or policy_limit < 1:
        raise ApplicationError("policy_protocol_error", "max_items obligation is invalid")
    effective_limit = min(current_limit, policy_limit)
    contract_fields = query_spec.get("result_fields")
    allowed: frozenset[str] | None = None
    if contract_fields is not None:
        if not isinstance(contract_fields, (list, tuple)):
            raise ApplicationError("query_contract_invalid", "result_fields must be an array")
        allowed = frozenset(str(x) for x in contract_fields)
    policy_fields = obligations.get("allowed_fields")
    if policy_fields is not None:
        if not isinstance(policy_fields, (list, tuple)):
            raise ApplicationError("policy_protocol_error", "allowed_fields must be an array")
        policy_set = frozenset(str(x) for x in policy_fields)
        if allowed is not None and not policy_set.issubset(allowed):
            raise ApplicationError("policy_scope_expansion", "policy attempted to expose undeclared fields")
        allowed = policy_set if allowed is None else allowed & policy_set
    redacted_raw = obligations.get("redact_fields", ())
    if not isinstance(redacted_raw, (list, tuple)):
        raise ApplicationError("policy_protocol_error", "redact_fields must be an array")
    redacted = frozenset(str(x) for x in redacted_raw)
    return effective_limit, allowed, redacted


def _project_item(
    item: Mapping[str, Any],
    allowed_fields: frozenset[str] | None,
    redacted_fields: frozenset[str],
) -> Mapping[str, JsonValue]:
    source = as_mapping(item, name="query item")
    result: dict[str, Any] = {}
    for key, value in source.items():
        if allowed_fields is not None and key not in allowed_fields:
            continue
        result[key] = "[REDACTED]" if key in redacted_fields else thaw(value)
    return freeze_mapping(result)


def _read_path(mapping: Mapping[str, Any], path: object) -> Any:
    if not isinstance(path, str) or not path:
        raise ApplicationError("query_contract_invalid", "sort field names must be strings")
    current: Any = mapping
    for part in path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            raise ApplicationError("index_protocol_error", f"sort field is missing: {path}")
        current = current[part]
    return current


def _sortable(value: Any) -> tuple[int, Any]:
    if value is None:
        return 0, ""
    if isinstance(value, bool):
        return 1, int(value)
    if isinstance(value, (int, float)):
        return 2, float(value)
    if isinstance(value, str):
        return 3, value
    raise ApplicationError("index_protocol_error", "sort values must be scalar")


def _artifact_status(artifact: Mapping[str, Any]) -> str:
    artifact_status = artifact.get("artifact_status")
    if isinstance(artifact_status, str):
        return artifact_status
    lifecycle = artifact.get("lifecycle")
    if isinstance(lifecycle, Mapping):
        status = lifecycle.get("status")
        if isinstance(status, str):
            return status
    metadata = artifact.get("metadata")
    if isinstance(metadata, Mapping):
        status = metadata.get("status")
        if isinstance(status, str):
            return status
    return "verified"


def _require_allow(outcome: str, reason: str | None) -> None:
    if outcome == "allow":
        return
    if outcome == "deny":
        raise ApplicationError("policy_denied", "query was denied", details={"reason_code": reason})
    if outcome == "blocked":
        raise ApplicationError("policy_unavailable", "query policy is unavailable", details={"reason_code": reason})
    raise ApplicationError("policy_protocol_error", "policy returned an unknown outcome")
