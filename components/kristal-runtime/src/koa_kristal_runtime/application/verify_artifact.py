"""Verify an admitted artifact without making it active or authoritative elsewhere."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from ..ports import ArtifactStore, AuditSink, PolicyEvaluator, SignatureVerifier
from . import (
    ApplicationError,
    ArtifactRef,
    as_mapping,
    deterministic_id,
    evaluate_policy_port,
    freeze_mapping,
    record_evidence_port,
    require_mapping,
    thaw,
    validate_artifact_structure,
)

VerificationOutcome = Literal["verified", "already_verified"]


@dataclass(frozen=True, slots=True)
class VerificationResult:
    outcome: VerificationOutcome
    artifact: ArtifactRef
    verification_id: str
    evidence_receipt_ref: str
    verifier_ref: str
    activation_eligible: bool


class VerifyArtifact:
    def __init__(
        self,
        artifact_store: ArtifactStore,
        signature_verifier: SignatureVerifier,
        policy_evaluator: PolicyEvaluator,
        audit_sink: AuditSink,
    ) -> None:
        self._artifacts = artifact_store
        self._signatures = signature_verifier
        self._policy = policy_evaluator
        self._audit = audit_sink

    def __call__(
        self,
        artifact_id: str,
        artifact_version: str,
        *,
        actor_context: object,
        runtime_context: object,
        request_id: str,
    ) -> VerificationResult:
        _require_text(artifact_id, "artifact_id")
        _require_text(artifact_version, "artifact_version")
        _require_text(request_id, "request_id")
        actor = as_mapping(actor_context, name="actor_context")
        runtime = as_mapping(runtime_context, name="runtime_context")
        stored = self._artifacts.get_artifact(artifact_id, artifact_version)
        if stored is None:
            raise ApplicationError("artifact_not_found", "artifact is not admitted")
        artifact = as_mapping(stored, name="stored artifact")
        ref = validate_artifact_structure(artifact)
        if ref.artifact_id != artifact_id or ref.artifact_version != artifact_version:
            raise ApplicationError("store_integrity_error", "stored artifact reference does not match lookup")
        if self._artifacts.get_revocation(artifact_id, artifact_version) is not None:
            raise ApplicationError("artifact_revoked", "revoked artifacts cannot be verified")

        decision = evaluate_policy_port(
            self._policy,
            "kristal.artifact.verify",
            actor,
            ref.as_mapping(),
            {"request_id": request_id, "runtime_context": thaw(runtime)},
        )
        _require_allow(decision.outcome, decision.reason_code)
        if decision.obligations:
            unsupported = set(decision.obligations) - {"trust_required"}
            if unsupported:
                raise ApplicationError(
                    "unsupported_policy_obligation",
                    "verification policy returned unenforceable obligations",
                    details={"obligations": sorted(unsupported)},
                )

        existing = self._artifacts.get_verification(artifact_id, artifact_version)
        if existing is not None:
            record = as_mapping(existing, name="verification record")
            if record.get("content_digest") == ref.content_digest and record.get("outcome") == "verified":
                receipt = _require_text_value(record.get("evidence_receipt_ref"), "evidence_receipt_ref")
                verifier = _require_text_value(record.get("verifier_ref"), "verifier_ref")
                return VerificationResult(
                    "already_verified",
                    ref,
                    _require_text_value(record.get("verification_id"), "verification_id"),
                    receipt,
                    verifier,
                    bool(record.get("activation_eligible", False)),
                )
            raise ApplicationError(
                "verification_conflict",
                "a non-matching verification record already exists",
            )

        signatures_raw = artifact.get("signatures", ())
        if not isinstance(signatures_raw, (list, tuple)):
            raise ApplicationError("artifact_invalid", "signatures must be an array")
        signatures: list[Mapping[str, Any]] = []
        for signature in signatures_raw:
            if not isinstance(signature, Mapping):
                raise ApplicationError("artifact_invalid", "signature entries must be objects")
            signatures.append(thaw(as_mapping(signature, name="signature")))
        verification = self._signatures.verify(thaw(artifact), signatures)
        trust_required = bool(decision.obligations.get("trust_required", verification.trust_required))
        if not verification.identity_valid:
            raise ApplicationError("unknown_artifact_identity", "artifact identity verification failed")
        if not verification.digest_valid:
            raise ApplicationError("invalid_artifact_digest", "artifact digest verification failed")
        if not verification.provenance_valid:
            raise ApplicationError("missing_provenance", "artifact provenance verification failed")
        if not verification.signatures_valid:
            raise ApplicationError("artifact_untrusted", "artifact signatures are invalid")
        if trust_required and not verification.trusted:
            raise ApplicationError("artifact_untrusted", "required artifact trust is unavailable")

        activation_eligible = _validate_compatibility(artifact, runtime)
        verification_id = deterministic_id(
            "verification", request_id, ref.as_mapping(), {"verifier": verification.verifier_ref}
        )
        event = {
            "event_id": verification_id,
            "event_type": "kristal.artifact.verification",
            "outcome": "verified",
            "request_id": request_id,
            "artifact": thaw(ref.as_mapping()),
            "policy_decision_id": decision.decision_id,
            "policy_receipt_ref": decision.receipt_ref,
            "verifier_ref": verification.verifier_ref,
            "activation_eligible": activation_eligible,
        }
        receipt = record_evidence_port(self._audit, event, "verification")
        record = freeze_mapping(
            {
                "verification_id": verification_id,
                "request_id": request_id,
                "artifact_id": ref.artifact_id,
                "artifact_version": ref.artifact_version,
                "artifact_class": ref.artifact_class,
                "content_digest": ref.content_digest,
                "outcome": "verified",
                "activation_eligible": activation_eligible,
                "verifier_ref": verification.verifier_ref,
                "policy_decision_id": decision.decision_id,
                "policy_receipt_ref": decision.receipt_ref,
                "evidence_receipt_ref": receipt,
            }
        )
        outcome = self._artifacts.record_verification(thaw(record))
        if outcome not in {"created", "existing"}:
            raise ApplicationError("store_protocol_error", "artifact store returned an unknown outcome")
        return VerificationResult(
            "verified" if outcome == "created" else "already_verified",
            ref,
            verification_id,
            receipt,
            verification.verifier_ref,
            activation_eligible,
        )


def _validate_compatibility(
    artifact: Mapping[str, Any], runtime: Mapping[str, Any]
) -> bool:
    runtime_version = runtime.get("kristal_runtime_version")
    profile_id = runtime.get("profile_id")
    if not isinstance(runtime_version, str) or not runtime_version:
        raise ApplicationError("runtime_context_invalid", "kristal_runtime_version is required")
    if not isinstance(profile_id, str) or not profile_id:
        raise ApplicationError("runtime_context_invalid", "profile_id is required")
    if artifact.get("artifact_type") == "kristal_state":
        # record_role/actionability describe the record; neither grants runtime authority.
        return False
    if artifact.get("artifact_class") == "kristal_artifact":
        compatibility = require_mapping(artifact, "compatibility")
        constraint = compatibility.get("kristal_runtime")
        if not isinstance(constraint, str) or not _version_matches(runtime_version, constraint):
            raise ApplicationError("artifact_incompatible", "Kristal Runtime version is incompatible")
        profiles = compatibility.get("profile_constraints", ())
        if profiles and profile_id not in profiles:
            raise ApplicationError("artifact_incompatible", "active profile is incompatible")
        return False

    compatibility = require_mapping(artifact, "compatibility_constraints")
    if compatibility.get("target_component") != "kristal_runtime":
        raise ApplicationError("artifact_incompatible", "Runtime Pack targets another component")
    if compatibility.get("target_component_contract_ref") != "contracts/components/kristal-runtime.component.json":
        raise ApplicationError("artifact_incompatible", "Runtime Pack targets another contract")
    constraint = compatibility.get("runtime_api_version")
    if not isinstance(constraint, str) or not _version_matches(runtime_version, constraint):
        raise ApplicationError("artifact_incompatible", "runtime API version is incompatible")
    supported = compatibility.get("supported_profile_ids", ())
    if supported and profile_id not in supported:
        raise ApplicationError("artifact_incompatible", "active profile is not supported")
    prohibited = compatibility.get("prohibited_overlay_ids", ())
    overlays = runtime.get("overlay_ids", ())
    if any(item in overlays for item in prohibited):
        raise ApplicationError("artifact_incompatible", "a prohibited overlay is active")
    replacement = require_mapping(artifact, "replacement_policy")
    if replacement.get("implicit_downgrade_allowed") is not False or replacement.get("implicit_substitution_allowed") is not False:
        raise ApplicationError("downgrade_or_substitution_denied", "implicit replacement is forbidden")
    return True


def _version_matches(version: str, constraint: str) -> bool:
    clean = constraint.strip()
    if clean in {"*", version, f"=={version}"}:
        return True
    if clean.startswith("^"):
        return version.split(".", 1)[0] == clean[1:].split(".", 1)[0]
    if clean.endswith(".*"):
        return version.startswith(clean[:-1])
    return False


def _require_allow(outcome: str, reason: str | None) -> None:
    if outcome == "allow":
        return
    if outcome == "deny":
        raise ApplicationError("policy_denied", "verification was denied", details={"reason_code": reason})
    if outcome == "blocked":
        raise ApplicationError("policy_unavailable", "verification policy is unavailable", details={"reason_code": reason})
    raise ApplicationError("policy_protocol_error", "policy returned an unknown outcome")


def _require_text(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ApplicationError("invalid_input", f"{field} is required")


def _require_text_value(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ApplicationError("store_integrity_error", f"stored {field} is invalid")
    return value
