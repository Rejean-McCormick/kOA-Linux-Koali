"""Admit a bounded Kristal artifact candidate without granting runtime authority."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal

from ..ports import ArtifactStore, AuditSink, PolicyEvaluator
from . import (
    ApplicationError,
    ArtifactRef,
    as_mapping,
    canonical_json,
    deterministic_id,
    evaluate_policy_port,
    freeze_mapping,
    record_evidence_port,
    thaw,
    validate_artifact_structure,
)

AdmissionStatus = Literal["admitted", "already_admitted"]


@dataclass(frozen=True, slots=True)
class AdmissionResult:
    status: AdmissionStatus
    artifact: ArtifactRef
    admission_id: str
    evidence_receipt_ref: str
    policy_decision_id: str


class AdmitArtifact:
    def __init__(
        self,
        artifact_store: ArtifactStore,
        policy_evaluator: PolicyEvaluator,
        audit_sink: AuditSink,
    ) -> None:
        self._artifacts = artifact_store
        self._policy = policy_evaluator
        self._audit = audit_sink

    def __call__(
        self,
        artifact: object,
        *,
        actor_context: object,
        request_id: str,
    ) -> AdmissionResult:
        if not request_id.strip():
            raise ApplicationError("invalid_request_id", "request_id is required")
        candidate = as_mapping(artifact, name="artifact")
        actor = as_mapping(actor_context, name="actor_context")
        ref = validate_artifact_structure(candidate)

        decision = evaluate_policy_port(
            self._policy,
            "kristal.artifact.admit",
            actor,
            ref.as_mapping(),
            {
                "request_id": request_id,
                "artifact_class": ref.artifact_class,
                "provenance": thaw(candidate.get("provenance", {})),
            },
        )
        _require_allow(decision.outcome, decision.reason_code, "admission")
        if decision.obligations:
            unsupported = set(decision.obligations) - {"required_classification"}
            if unsupported:
                raise ApplicationError(
                    "unsupported_policy_obligation",
                    "admission policy returned obligations this bundle cannot enforce",
                    details={"obligations": sorted(unsupported)},
                )
            required = decision.obligations.get("required_classification")
            classification = candidate.get("metadata", {})
            actual = classification.get("classification") if isinstance(classification, Mapping) else None
            if required is not None and actual != required:
                raise ApplicationError(
                    "policy_obligation_unsatisfied",
                    "required artifact classification is absent",
                )

        existing = self._artifacts.get_artifact(ref.artifact_id, ref.artifact_version)
        if existing is not None:
            existing_mapping = as_mapping(existing, name="stored artifact")
            existing_ref = validate_artifact_structure(existing_mapping)
            same_document = canonical_json(existing_mapping) == canonical_json(candidate)
            same_content_address = ref.artifact_class == "kristal_state" and existing_ref.content_digest == ref.content_digest
            if existing_ref != ref or not (same_document or same_content_address):
                raise ApplicationError(
                    "artifact_identity_conflict",
                    "the artifact identity and version already contain different content",
                )
            receipt = self._record_evidence(
                "already_admitted", request_id, ref, actor, "existing", decision.decision_id
            )
            return AdmissionResult(
                "already_admitted",
                ref,
                deterministic_id("admission", request_id, ref.as_mapping()),
                receipt,
                decision.decision_id,
            )

        same_digest = self._artifacts.find_by_content_digest(ref.content_digest)
        if same_digest is not None:
            digest_ref = validate_artifact_structure(as_mapping(same_digest, name="digest match"))
            if digest_ref.artifact_id != ref.artifact_id:
                raise ApplicationError(
                    "content_identity_alias_conflict",
                    "canonical content is already registered under another artifact identity",
                    details={"registered_artifact_id": digest_ref.artifact_id},
                )

        admission_id = deterministic_id(
            "admission", request_id, ref.as_mapping(), {"decision": decision.decision_id}
        )
        event = {
            "event_id": admission_id,
            "event_type": "kristal.artifact.admission",
            "outcome": "admitted",
            "request_id": request_id,
            "artifact": thaw(ref.as_mapping()),
            "actor_id": actor.get("actor_id") or actor.get("subject_id"),
            "policy_decision_id": decision.decision_id,
            "policy_receipt_ref": decision.receipt_ref,
        }
        receipt = record_evidence_port(self._audit, event, "admission")
        record = freeze_mapping(
            {
                "admission_id": admission_id,
                "request_id": request_id,
                "artifact": thaw(ref.as_mapping()),
                "policy_decision_id": decision.decision_id,
                "policy_receipt_ref": decision.receipt_ref,
                "evidence_receipt_ref": receipt,
                "status": "candidate",
            }
        )
        outcome = self._artifacts.admit_artifact(thaw(candidate), thaw(record))
        if outcome not in {"created", "existing"}:
            raise ApplicationError("store_protocol_error", "artifact store returned an unknown outcome")
        return AdmissionResult(
            "admitted" if outcome == "created" else "already_admitted",
            ref,
            admission_id,
            receipt,
            decision.decision_id,
        )

    def _record_evidence(
        self,
        outcome: str,
        request_id: str,
        ref: ArtifactRef,
        actor: Mapping[str, Any],
        status: str,
        policy_decision_id: str | None,
    ) -> str:
        receipt = record_evidence_port(
            self._audit,
            {
                "event_id": deterministic_id("admission-event", request_id, ref.as_mapping(), outcome),
                "event_type": "kristal.artifact.admission",
                "outcome": outcome,
                "request_id": request_id,
                "artifact": thaw(ref.as_mapping()),
                "actor_id": actor.get("actor_id") or actor.get("subject_id"),
                "status": status,
                "policy_decision_id": policy_decision_id,
            },
            "admission",
        )
        return receipt


def _require_allow(outcome: str, reason_code: str | None, operation: str) -> None:
    if outcome == "allow":
        return
    if outcome == "deny":
        raise ApplicationError(
            "policy_denied", f"{operation} was denied", details={"reason_code": reason_code}
        )
    if outcome == "blocked":
        raise ApplicationError(
            "policy_unavailable", f"{operation} policy was unavailable", details={"reason_code": reason_code}
        )
    raise ApplicationError("policy_protocol_error", "policy returned an unknown outcome")
