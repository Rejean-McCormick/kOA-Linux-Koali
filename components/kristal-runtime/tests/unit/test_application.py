from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from typing import Any

import pytest
from jsonschema import Draft202012Validator

SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from koa_kristal_runtime.application import (  # noqa: E402
    AdmitArtifact,
    ApplicationError,
    ExecuteQuery,
    RenderArtifact,
    RevokeArtifact,
    VerifyArtifact,
    canonical_json,
    kristal_state_content_digest,
)
from koa_kristal_runtime.ports import (  # noqa: E402
    IndexQueryPage,
    PolicyDecision,
    SignatureVerification,
)


DIGEST_A = "a" * 64
DIGEST_B = "b" * 64


def artifact(*, artifact_id: str = "kristal-artifact.example", digest: str = DIGEST_A) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "artifact_version": "1.0.0",
        "artifact_class": "kristal_artifact",
        "content_identity": {"algorithm": "sha256", "digest": digest},
        "manifest": {
            "entries": [{"path": "records.json", "sha256": digest}],
            "query_contract_refs": ["query.example@1.0.0"],
        },
        "provenance": {"source_refs": ["source:example"], "producer": "producer.example"},
        "rights": {"license": "CC-BY-4.0", "audiences": ["public"]},
        "compatibility": {
            "kristal_runtime": "*",
            "profile_constraints": ["sovereign_linux_node"],
        },
        "signatures": [],
        "metadata": {
            "status": "recognized",
            "title": "Example Kristal",
            "summary": "A bounded example",
            "secret_note": "never disclose",
        },
    }


def runtime_pack(*, channel: str = "knowledge") -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "artifact_class": "runtime_pack",
        "artifact_identity": "runtime-pack:example",
        "artifact_version": "1.0.0",
        "release_channel": channel,
        "lifecycle": {"status": "published", "published_at": "2026-08-06T12:00:00Z"},
        "created_at": "2026-08-06T12:00:00Z",
        "artifact_digest": "sha256:" + DIGEST_A,
        "digest_scope": "canonical_manifest_and_payload",
        "provenance": {
            "producer": {
                "producer_id": "producer.example",
                "producer_type": "component",
                "component_id": "kristal_runtime",
                "contract_ref": "docs/contracts/components/kristal-runtime.component.json",
                "software_version": "1.0.0",
            },
            "build_id": "build.example",
            "built_at": "2026-08-06T12:00:00Z",
            "source_materials": [{
                "material_id": "source.example",
                "digest": "sha256:" + DIGEST_B,
                "source_ref": "docs/contracts/artifact-contracts/kristal-artifact.schema.json",
            }],
            "reproducible_build": True,
        },
        "compatibility_constraints": {
            "target_component": "kristal_runtime",
            "target_component_contract_ref": "contracts/components/kristal-runtime.component.json",
            "runtime_api_version": "^1.0.0",
            "pack_format_version": "1.0.0",
            "supported_profile_ids": ["sovereign_linux_node"],
            "required_overlay_ids": [],
            "prohibited_overlay_ids": ["unsafe_overlay"],
            "compatibility_evidence_refs": ["evidence:compatibility"],
        },
        "manifest": {
            "manifest_version": "1.0.0",
            "manifest_digest": "sha256:" + DIGEST_B,
            "entries": [{
                "path": "records.json",
                "role": "knowledge_records",
                "media_type": "application/json",
                "digest": "sha256:" + DIGEST_B,
                "size_bytes": 128,
                "required": True,
            }],
        },
        "verification": {
            "required_checks": [
                "schema_validation",
                "identity_validation",
                "digest_validation",
                "trust_validation_when_required",
                "compatibility_validation",
                "release_channel_validation",
                "downgrade_and_substitution_policy_validation",
            ],
            "quarantine_on_nonverified_outcome": True,
            "reverify_after_integrity_scope_change": True,
            "verification_receipt_schema_ref": "contracts/artifact-contracts/decision-receipt.schema.json",
        },
        "activation_contract": {
            "owner_component": "kristal_runtime",
            "component_contract_ref": "contracts/components/kristal-runtime.component.json",
            "interface_id": "runtime_pack_activation",
            "activation_boundary": "active_runtime_pack_record",
            "activation_mode": "atomic_pointer_switch",
            "partial_authoritative_activation_allowed": False,
            "last_valid_state_retained_until_success": True,
            "verification_receipt_required": True,
            "authorization_required": True,
            "resource_grant_required": True,
            "recovery": {
                "rollback_supported": True,
                "last_valid_predecessor_required": True,
                "forward_repair_supported": False,
            },
        },
        "replacement_policy": {
            "implicit_downgrade_allowed": False,
            "implicit_substitution_allowed": False,
            "authorization_required": True,
            "compatibility_validation_required": True,
        },
        "content_handling": {
            "immutable_after_publication": True,
            "unverified_execution_allowed": False,
            "direct_cross_component_mutation_allowed": False,
            "secret_values_allowed": False,
        },
        "disclosure": {
            "visibility": "authorized_internal",
            "contains_secret_values": False,
            "contains_personal_data": False,
            "contains_restricted_content": False,
        },
        "signatures": [{
            "kid": "signer.example",
            "algorithm": "Ed25519",
            "value": "AAAAAAAAAAAAAAAAAAAAAA==",
            "signed_digest": "sha256:" + DIGEST_A,
            "signed_at": "2026-08-06T12:00:00Z",
        }],
    }



def kristal_state() -> dict[str, Any]:
    state: dict[str, Any] = {
        "schema_version": "6.0",
        "artifact_type": "kristal_state",
        "state_id": "sha256:" + ("0" * 64),
        "artifact_status": "recognized",
        "created_at": "2026-10-01T12:00:00Z",
        "created_by": {"agent_id": "system:koa-linux", "agent_type": "system"},
        "canonicalization_profile": "kristal.v6:jcs-rfc8785",
        "canonicalization_version": "1",
        "content_hash": {"alg": "sha256", "value": "0" * 64},
        "hash_target_policy": {
            "exclude_fields": ["state_id", "content_hash", "signatures"]
        },
        "applicability": {"domain": "technology", "environment": "test", "language": "en"},
        "assertions": [{
            "assertion_id": "sha256:" + ("c" * 64),
            "statement": {
                "subject": {"label": "kOA Linux"},
                "predicate": {"label": "kristal.alignment"},
                "object": {"kind": "string", "value": "v6"},
                "coordinates": [{
                    "predicate": {"label": "platform"},
                    "object": {"kind": "string", "value": "linux"}
                }],
            },
            "assertion_status": "hypothesis",
            "applicability": {"domain": "technology"},
            "valuations": [{
                "dimension": "assertion_support",
                "value_semantics": "ordinal",
                "value_state": "known",
                "value": "supported",
                "scale_ref": "kristal.ordinal.support.v1"
            }],
            "record_role": "reference_knowledge",
            "actionability": {"mode": "automatic"},
        }],
        "provenance": [{
            "provenance_id": "prov:koa-linux:v6",
            "event_type": "validated",
            "created_at": "2026-10-01T12:00:01Z",
            "agent": {"agent_id": "system:koa-linux", "agent_type": "system"}
        }],
        "signatures": [],
    }
    digest = kristal_state_content_digest(state)
    state["state_id"] = "sha256:" + digest
    state["content_hash"]["value"] = digest
    return state

def test_contract_fixtures_validate_against_canonical_schemas():
    repository_root = Path(__file__).resolve().parents[4]
    cases = (
        (artifact(), repository_root / "docs/contracts/artifact-contracts/kristal-artifact.schema.json"),
        (kristal_state(), repository_root / "docs/contracts/artifact-contracts/kristal-state.schema.json"),
        (runtime_pack(), repository_root / "docs/contracts/artifact-contracts/runtime-pack.schema.json"),
    )
    for instance, schema_path in cases:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(instance)


class MemoryArtifactStore:
    def __init__(self) -> None:
        self.artifacts: dict[tuple[str, str], dict[str, Any]] = {}
        self.verifications: dict[tuple[str, str], dict[str, Any]] = {}
        self.revocations: dict[tuple[str, str], dict[str, Any]] = {}

    def get_artifact(self, artifact_id: str, artifact_version: str):
        value = self.artifacts.get((artifact_id, artifact_version))
        return deepcopy(value) if value else None

    def find_by_content_digest(self, content_digest: str):
        for value in self.artifacts.values():
            digest = value.get("artifact_digest")
            if value.get("artifact_type") == "kristal_state":
                digest = value["state_id"]
            elif value.get("artifact_class") == "kristal_artifact":
                digest = "sha256:" + value["content_identity"]["digest"]
            if digest == content_digest:
                return deepcopy(value)
        return None

    def admit_artifact(self, artifact_value, admission_record):
        if artifact_value.get("artifact_type") == "kristal_state":
            key = (artifact_value["state_id"], artifact_value["schema_version"])
        elif artifact_value["artifact_class"] == "runtime_pack":
            key = (artifact_value["artifact_identity"], artifact_value["artifact_version"])
        else:
            key = (artifact_value["artifact_id"], artifact_value["artifact_version"])
        if key in self.artifacts:
            return "existing"
        self.artifacts[key] = deepcopy(dict(artifact_value))
        return "created"

    def get_verification(self, artifact_id: str, artifact_version: str):
        value = self.verifications.get((artifact_id, artifact_version))
        return deepcopy(value) if value else None

    def record_verification(self, record):
        key = (record["artifact_id"], record["artifact_version"])
        if key in self.verifications:
            return "existing"
        self.verifications[key] = deepcopy(dict(record))
        return "created"

    def get_revocation(self, artifact_id: str, artifact_version: str):
        value = self.revocations.get((artifact_id, artifact_version))
        return deepcopy(value) if value else None

    def record_revocation(self, record):
        key = (record["artifact_id"], record["artifact_version"])
        if key in self.revocations:
            return "existing"
        self.revocations[key] = deepcopy(dict(record))
        return "created"


class AllowPolicy:
    def __init__(self, *, outcome: str = "allow", obligations: dict[str, Any] | None = None) -> None:
        self.outcome = outcome
        self.obligations = obligations or {}
        self.calls: list[tuple[str, dict[str, Any], dict[str, Any], dict[str, Any]]] = []

    def evaluate(self, action, actor_context, resource, context):
        self.calls.append((action, dict(actor_context), dict(resource), dict(context)))
        return PolicyDecision(
            self.outcome,
            "decision:1",
            "policy:1",
            "receipt:policy:1",
            self.obligations,
            "POLICY_BLOCKED" if self.outcome != "allow" else None,
        )


class MemoryAudit:
    def __init__(self, *, available: bool = True) -> None:
        self.available = available
        self.events: list[dict[str, Any]] = []

    def record(self, event):
        self.events.append(deepcopy(dict(event)))
        return f"receipt:audit:{len(self.events)}" if self.available else ""


class RaisingPolicy:
    def evaluate(self, action, actor_context, resource, context):
        raise OSError("policy transport unavailable")


class RaisingAudit:
    def record(self, event):
        raise OSError("audit transport unavailable")


class Verifier:
    def __init__(self, **overrides: Any) -> None:
        values = {
            "identity_valid": True,
            "digest_valid": True,
            "provenance_valid": True,
            "trust_required": False,
            "trusted": True,
            "signatures_valid": True,
            "verifier_ref": "verifier:test",
            "reason_code": None,
        }
        values.update(overrides)
        self.result = SignatureVerification(**values)

    def verify(self, artifact_value, signatures):
        return self.result


class MemoryIndex:
    def __init__(self) -> None:
        self.items: list[dict[str, Any]] = [
            {"id": "b", "rank": 2, "title": "Second", "private": "p2"},
            {"id": "a", "rank": 1, "title": "First", "private": "p1"},
        ]
        self.fail_query = False
        self.fail_withdraw = False
        self.withdrawals: list[tuple[str, str, str]] = []
        self.last_limit: int | None = None

    def query(self, artifact_id, artifact_version, query_class, parameters, *, limit, cursor, timeout_ms):
        if self.fail_query:
            raise OSError("index unavailable")
        self.last_limit = limit
        return IndexQueryPage(deepcopy(self.items[:limit]), "cursor:next", len(self.items))

    def withdraw(self, artifact_id, artifact_version, scope):
        if self.fail_withdraw:
            raise OSError("withdraw failed")
        self.withdrawals.append((artifact_id, artifact_version, scope))


@pytest.fixture
def actor() -> dict[str, Any]:
    return {"actor_id": "actor:test", "audiences": ["public"]}


@pytest.fixture
def runtime_context() -> dict[str, Any]:
    return {
        "kristal_runtime_version": "1.2.0",
        "profile_id": "sovereign_linux_node",
        "overlay_ids": [],
    }


def admit(store: MemoryArtifactStore, actor: dict[str, Any], value: dict[str, Any] | None = None):
    return AdmitArtifact(store, AllowPolicy(), MemoryAudit())(
        value or artifact(), actor_context=actor, request_id="request:admit"
    )


def verify(store: MemoryArtifactStore, actor: dict[str, Any], runtime_context: dict[str, Any]):
    return VerifyArtifact(store, Verifier(), AllowPolicy(), MemoryAudit())(
        "kristal-artifact.example",
        "1.0.0",
        actor_context=actor,
        runtime_context=runtime_context,
        request_id="request:verify",
    )


def query_contract() -> dict[str, Any]:
    return {
        "contract_id": "query.example",
        "version": "1.0.0",
        "query_classes": {
            "lookup": {
                "allowed_parameter_keys": ["term"],
                "result_fields": ["id", "rank", "title"],
                "max_items": 10,
                "timeout_ms": 250,
                "sort_fields": ["rank"],
                "tie_breaker": "id",
            }
        },
        "unsupported_operations": ["arbitrary_sparql"],
    }


def test_admission_is_idempotent_and_does_not_grant_active_status(actor):
    store = MemoryArtifactStore()
    audit = MemoryAudit()
    use_case = AdmitArtifact(store, AllowPolicy(), audit)
    first = use_case(artifact(), actor_context=actor, request_id="request:1")
    second = use_case(artifact(), actor_context=actor, request_id="request:2")
    assert first.status == "admitted"
    assert second.status == "already_admitted"
    assert len(store.artifacts) == 1
    assert store.artifacts[("kristal-artifact.example", "1.0.0")]["metadata"]["status"] == "recognized"
    assert [event["outcome"] for event in audit.events] == ["admitted", "already_admitted"]


def test_admission_rejects_same_identity_with_different_content(actor):
    store = MemoryArtifactStore()
    admit(store, actor)
    changed = artifact()
    changed["metadata"]["title"] = "Changed"
    with pytest.raises(ApplicationError) as exc:
        AdmitArtifact(store, AllowPolicy(), MemoryAudit())(
            changed, actor_context=actor, request_id="request:changed"
        )
    assert exc.value.code == "artifact_identity_conflict"


def test_admission_rejects_content_alias_and_unsafe_paths(actor):
    store = MemoryArtifactStore()
    admit(store, actor)
    alias = artifact(artifact_id="kristal-artifact.alias")
    with pytest.raises(ApplicationError) as exc:
        AdmitArtifact(store, AllowPolicy(), MemoryAudit())(
            alias, actor_context=actor, request_id="request:alias"
        )
    assert exc.value.code == "content_identity_alias_conflict"
    unsafe = artifact(digest=DIGEST_B)
    unsafe["manifest"]["entries"][0]["path"] = "../escape"
    with pytest.raises(ApplicationError) as unsafe_exc:
        AdmitArtifact(MemoryArtifactStore(), AllowPolicy(), MemoryAudit())(
            unsafe, actor_context=actor, request_id="request:unsafe"
        )
    assert unsafe_exc.value.code == "unsafe_manifest_path"


def test_admission_fails_closed_for_policy_and_audit(actor):
    with pytest.raises(ApplicationError) as denied:
        AdmitArtifact(MemoryArtifactStore(), AllowPolicy(outcome="deny"), MemoryAudit())(
            artifact(), actor_context=actor, request_id="request:deny"
        )
    assert denied.value.code == "policy_denied"
    store = MemoryArtifactStore()
    with pytest.raises(ApplicationError) as unavailable:
        AdmitArtifact(store, AllowPolicy(), MemoryAudit(available=False))(
            artifact(), actor_context=actor, request_id="request:audit"
        )
    assert unavailable.value.code == "audit_unavailable"
    assert store.artifacts == {}


def test_runtime_pack_requires_knowledge_channel(actor):
    with pytest.raises(ApplicationError) as exc:
        AdmitArtifact(MemoryArtifactStore(), AllowPolicy(), MemoryAudit())(
            runtime_pack(channel="services"), actor_context=actor, request_id="request:pack"
        )
    assert exc.value.code == "release_channel_invalid"


def test_verification_records_closed_success_and_is_idempotent(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    audit = MemoryAudit()
    use_case = VerifyArtifact(store, Verifier(), AllowPolicy(), audit)
    first = use_case(
        "kristal-artifact.example",
        "1.0.0",
        actor_context=actor,
        runtime_context=runtime_context,
        request_id="request:verify",
    )
    second = use_case(
        "kristal-artifact.example",
        "1.0.0",
        actor_context=actor,
        runtime_context=runtime_context,
        request_id="request:verify:again",
    )
    assert first.outcome == "verified"
    assert first.activation_eligible is False
    assert second.outcome == "already_verified"
    assert len(store.verifications) == 1


def test_verification_rejects_invalid_trust_and_incompatibility(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    with pytest.raises(ApplicationError) as trust:
        VerifyArtifact(store, Verifier(trusted=False, trust_required=True), AllowPolicy(), MemoryAudit())(
            "kristal-artifact.example",
            "1.0.0",
            actor_context=actor,
            runtime_context=runtime_context,
            request_id="request:trust",
        )
    assert trust.value.code == "artifact_untrusted"
    incompatible = artifact(digest=DIGEST_B)
    incompatible["compatibility"]["kristal_runtime"] = "^2.0.0"
    other = MemoryArtifactStore()
    admit(other, actor, incompatible)
    with pytest.raises(ApplicationError) as compatibility:
        VerifyArtifact(other, Verifier(), AllowPolicy(), MemoryAudit())(
            "kristal-artifact.example",
            "1.0.0",
            actor_context=actor,
            runtime_context=runtime_context,
            request_id="request:compatibility",
        )
    assert compatibility.value.code == "artifact_incompatible"


def test_runtime_pack_verification_can_be_activation_eligible(actor, runtime_context):
    store = MemoryArtifactStore()
    AdmitArtifact(store, AllowPolicy(), MemoryAudit())(
        runtime_pack(), actor_context=actor, request_id="request:pack:admit"
    )
    result = VerifyArtifact(store, Verifier(), AllowPolicy(), MemoryAudit())(
        "runtime-pack:example",
        "1.0.0",
        actor_context=actor,
        runtime_context=runtime_context,
        request_id="request:pack:verify",
    )
    assert result.activation_eligible is True


def test_query_is_bounded_sorted_projected_and_redacted(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    verify(store, actor, runtime_context)
    index = MemoryIndex()
    policy = AllowPolicy(obligations={"max_items": 2, "allowed_fields": ["id", "title"], "redact_fields": ["title"]})
    result = ExecuteQuery(store, index, policy, MemoryAudit())(
        "kristal-artifact.example",
        "1.0.0",
        query_contract=query_contract(),
        query_class="lookup",
        parameters={"term": "example"},
        actor_context=actor,
        request_id="request:query",
        limit=8,
    )
    assert index.last_limit == 2
    assert [item["id"] for item in result.items] == ["a", "b"]
    assert all(item["title"] == "[REDACTED]" for item in result.items)
    assert all("private" not in item and "rank" not in item for item in result.items)
    assert result.status == "recognized"
    assert result.result_digest.startswith("sha256:")


def test_query_rejects_unsupported_parameters_and_unverified_or_revoked_artifacts(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    use_case = ExecuteQuery(store, MemoryIndex(), AllowPolicy(), MemoryAudit())
    with pytest.raises(ApplicationError) as unverified:
        use_case(
            "kristal-artifact.example", "1.0.0", query_contract=query_contract(), query_class="lookup",
            parameters={}, actor_context=actor, request_id="request:unverified", limit=1
        )
    assert unverified.value.code == "artifact_not_verified"
    verify(store, actor, runtime_context)
    with pytest.raises(ApplicationError) as parameter:
        use_case(
            "kristal-artifact.example", "1.0.0", query_contract=query_contract(), query_class="lookup",
            parameters={"unknown": True}, actor_context=actor, request_id="request:parameter", limit=1
        )
    assert parameter.value.code == "unsupported_query_parameter"
    store.revocations[("kristal-artifact.example", "1.0.0")] = {"status": "revoked"}
    with pytest.raises(ApplicationError) as revoked:
        use_case(
            "kristal-artifact.example", "1.0.0", query_contract=query_contract(), query_class="lookup",
            parameters={}, actor_context=actor, request_id="request:revoked", limit=1
        )
    assert revoked.value.code == "artifact_revoked"


def test_query_has_no_remote_or_ai_fallback(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    verify(store, actor, runtime_context)
    index = MemoryIndex()
    index.fail_query = True
    audit = MemoryAudit()
    with pytest.raises(ApplicationError) as exc:
        ExecuteQuery(store, index, AllowPolicy(), audit)(
            "kristal-artifact.example", "1.0.0", query_contract=query_contract(), query_class="lookup",
            parameters={}, actor_context=actor, request_id="request:index-failure", limit=1
        )
    assert exc.value.code == "index_unavailable"
    assert audit.events[-1]["event_type"] == "kristal.query.failed"


def test_query_rejects_policy_scope_expansion(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    verify(store, actor, runtime_context)
    policy = AllowPolicy(obligations={"allowed_fields": ["id", "private"]})
    with pytest.raises(ApplicationError) as exc:
        ExecuteQuery(store, MemoryIndex(), policy, MemoryAudit())(
            "kristal-artifact.example", "1.0.0", query_contract=query_contract(), query_class="lookup",
            parameters={}, actor_context=actor, request_id="request:scope", limit=1
        )
    assert exc.value.code == "policy_scope_expansion"


def test_render_is_a_deterministic_audience_bound_projection(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    verify(store, actor, runtime_context)
    view = {
        "view_id": "view.public-summary",
        "version": "1.0.0",
        "media_type": "application/json",
        "required_audience": "public",
        "fields": ["artifact_id", "metadata.title", "metadata.summary"],
    }
    policy = AllowPolicy(obligations={"allowed_fields": ["artifact_id", "metadata.title"], "redact_fields": ["metadata.title"]})
    result = RenderArtifact(store, policy, MemoryAudit())(
        "kristal-artifact.example", "1.0.0", view_contract=view, actor_context=actor,
        request_id="request:render"
    )
    assert result.payload["artifact_id"] == "kristal-artifact.example"
    assert result.payload["metadata"]["title"] == "[REDACTED]"
    assert "summary" not in result.payload["metadata"]
    assert result.payload_digest.startswith("sha256:")


def test_render_rejects_missing_audience_and_policy_expansion(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    verify(store, actor, runtime_context)
    no_audience = {**actor, "audiences": []}
    view = {
        "view_id": "view.public", "version": "1", "media_type": "application/json",
        "required_audience": "public", "fields": ["artifact_id"]
    }
    with pytest.raises(ApplicationError) as audience:
        RenderArtifact(store, AllowPolicy(), MemoryAudit())(
            "kristal-artifact.example", "1.0.0", view_contract=view,
            actor_context=no_audience, request_id="request:audience"
        )
    assert audience.value.code == "audience_denied"
    with pytest.raises(ApplicationError) as expansion:
        RenderArtifact(store, AllowPolicy(obligations={"allowed_fields": ["metadata.secret_note"]}), MemoryAudit())(
            "kristal-artifact.example", "1.0.0", view_contract=view,
            actor_context=actor, request_id="request:expansion"
        )
    assert expansion.value.code == "policy_scope_expansion"


def test_revocation_is_authoritative_before_index_withdrawal(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    verify(store, actor, runtime_context)
    index = MemoryIndex()
    use_case = RevokeArtifact(store, index, AllowPolicy(), MemoryAudit())
    result = use_case(
        "kristal-artifact.example", "1.0.0", actor_context=actor,
        request_id="request:revoke", reason_code="RIGHTS_WITHDRAWN", scope="all"
    )
    again = use_case(
        "kristal-artifact.example", "1.0.0", actor_context=actor,
        request_id="request:revoke", reason_code="RIGHTS_WITHDRAWN", scope="all"
    )
    assert result.outcome == "revoked"
    assert again.outcome == "already_revoked"
    assert store.revocations[("kristal-artifact.example", "1.0.0")]["status"] == "revoked"
    assert len(index.withdrawals) == 2


def test_revocation_conflict_and_cleanup_failure_are_explicit(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    verify(store, actor, runtime_context)
    index = MemoryIndex()
    use_case = RevokeArtifact(store, index, AllowPolicy(), MemoryAudit())
    use_case(
        "kristal-artifact.example", "1.0.0", actor_context=actor,
        request_id="request:first", reason_code="COMPROMISED", scope="query"
    )
    with pytest.raises(ApplicationError) as conflict:
        use_case(
            "kristal-artifact.example", "1.0.0", actor_context=actor,
            request_id="request:second", reason_code="OTHER", scope="query"
        )
    assert conflict.value.code == "revocation_conflict"

    other = MemoryArtifactStore()
    admit(other, actor)
    verify(other, actor, runtime_context)
    failed_index = MemoryIndex()
    failed_index.fail_withdraw = True
    with pytest.raises(ApplicationError) as cleanup:
        RevokeArtifact(other, failed_index, AllowPolicy(), MemoryAudit())(
            "kristal-artifact.example", "1.0.0", actor_context=actor,
            request_id="request:cleanup", reason_code="COMPROMISED", scope="query"
        )
    assert cleanup.value.code == "revocation_cleanup_failed"
    assert other.revocations[("kristal-artifact.example", "1.0.0")]["status"] == "revoked"


def test_policy_unavailability_blocks_all_governed_operations(actor, runtime_context):
    blocked = AllowPolicy(outcome="blocked")
    with pytest.raises(ApplicationError) as admission:
        AdmitArtifact(MemoryArtifactStore(), blocked, MemoryAudit())(
            artifact(), actor_context=actor, request_id="request:blocked"
        )
    assert admission.value.code == "policy_unavailable"

    store = MemoryArtifactStore()
    admit(store, actor)
    with pytest.raises(ApplicationError) as verification:
        VerifyArtifact(store, Verifier(), blocked, MemoryAudit())(
            "kristal-artifact.example", "1.0.0", actor_context=actor,
            runtime_context=runtime_context, request_id="request:verify:blocked"
        )
    assert verification.value.code == "policy_unavailable"


def test_idempotent_retries_still_require_current_authority(actor, runtime_context):
    store = MemoryArtifactStore()
    admit(store, actor)
    verify(store, actor, runtime_context)
    index = MemoryIndex()
    RevokeArtifact(store, index, AllowPolicy(), MemoryAudit())(
        "kristal-artifact.example", "1.0.0", actor_context=actor,
        request_id="request:revoke:auth", reason_code="WITHDRAWN", scope="query"
    )

    blocked = AllowPolicy(outcome="blocked")
    with pytest.raises(ApplicationError) as admission_retry:
        AdmitArtifact(store, blocked, MemoryAudit())(
            artifact(), actor_context=actor, request_id="request:admit:retry"
        )
    assert admission_retry.value.code == "policy_unavailable"

    with pytest.raises(ApplicationError) as verification_retry:
        VerifyArtifact(store, Verifier(), blocked, MemoryAudit())(
            "kristal-artifact.example", "1.0.0", actor_context=actor,
            runtime_context=runtime_context, request_id="request:verify:retry"
        )
    assert verification_retry.value.code == "artifact_revoked"

    with pytest.raises(ApplicationError) as revocation_retry:
        RevokeArtifact(store, index, blocked, MemoryAudit())(
            "kristal-artifact.example", "1.0.0", actor_context=actor,
            request_id="request:revoke:auth", reason_code="WITHDRAWN", scope="query"
        )
    assert revocation_retry.value.code == "policy_unavailable"


def test_policy_and_audit_transport_failures_are_closed(actor):
    with pytest.raises(ApplicationError) as policy_failure:
        AdmitArtifact(MemoryArtifactStore(), RaisingPolicy(), MemoryAudit())(
            artifact(), actor_context=actor, request_id="request:policy:transport"
        )
    assert policy_failure.value.code == "policy_unavailable"

    with pytest.raises(ApplicationError) as audit_failure:
        AdmitArtifact(MemoryArtifactStore(), AllowPolicy(), RaisingAudit())(
            artifact(), actor_context=actor, request_id="request:audit:transport"
        )
    assert audit_failure.value.code == "audit_unavailable"


def test_kristal_v6_jcs_matches_normative_vectors():
    assert canonical_json({}) == b"{}"
    value = {"z": "last", "a": {"b": 2, "a": 1}, "m": [{"y": True, "x": False}, None, "text"]}
    expected = b'{"a":{"a":1,"b":2},"m":[{"x":false,"y":true},null,"text"],"z":"last"}'
    assert canonical_json(value) == expected
    assert __import__("hashlib").sha256(expected).hexdigest() == "f45ed16183caf10d3a60b77fe6b2db8cae797c847bd81391b43887abd68fe7c2"


def test_kristal_v6_state_admission_is_content_addressed(actor):
    state = kristal_state()
    store = MemoryArtifactStore()
    result = AdmitArtifact(store, AllowPolicy(), MemoryAudit())(
        state, actor_context=actor, request_id="request:v6:admit"
    )
    assert result.artifact.artifact_class == "kristal_state"
    assert result.artifact.artifact_id == state["state_id"]
    assert result.artifact.artifact_version == "6.0"
    assert result.artifact.content_digest == state["state_id"]


def test_kristal_v6_rejects_mutation_without_rehash(actor):
    state = kristal_state()
    state["assertions"][0]["valuations"][0]["value"] = "changed"
    with pytest.raises(ApplicationError) as exc:
        AdmitArtifact(MemoryArtifactStore(), AllowPolicy(), MemoryAudit())(
            state, actor_context=actor, request_id="request:v6:tamper"
        )
    assert exc.value.code == "content_identity_invalid"


def test_kristal_v6_rejects_legacy_semantics_and_invalid_unknown_value(actor):
    legacy = kristal_state()
    legacy["assertions"][0]["uncertainty"] = 0.2
    digest = kristal_state_content_digest(legacy)
    legacy["state_id"] = "sha256:" + digest
    legacy["content_hash"]["value"] = digest
    with pytest.raises(ApplicationError) as exc:
        AdmitArtifact(MemoryArtifactStore(), AllowPolicy(), MemoryAudit())(
            legacy, actor_context=actor, request_id="request:v6:legacy"
        )
    assert exc.value.code == "kristal_v5_field_forbidden"

    invalid = kristal_state()
    valuation = invalid["assertions"][0]["valuations"][0]
    valuation["value_state"] = "unknown"
    digest = kristal_state_content_digest(invalid)
    invalid["state_id"] = "sha256:" + digest
    invalid["content_hash"]["value"] = digest
    with pytest.raises(ApplicationError) as exc2:
        AdmitArtifact(MemoryArtifactStore(), AllowPolicy(), MemoryAudit())(
            invalid, actor_context=actor, request_id="request:v6:valuation"
        )
    assert exc2.value.code == "kristal_v6_valuation_invalid"


def test_kristal_v6_automatic_actionability_never_grants_activation(actor, runtime_context):
    state = kristal_state()
    store = MemoryArtifactStore()
    AdmitArtifact(store, AllowPolicy(), MemoryAudit())(state, actor_context=actor, request_id="request:v6:admit")
    result = VerifyArtifact(store, Verifier(), AllowPolicy(), MemoryAudit())(
        state["state_id"], "6.0", actor_context=actor, runtime_context=runtime_context, request_id="request:v6:verify"
    )
    assert result.activation_eligible is False


def test_kristal_v6_filesystem_store_accepts_document_only_state(tmp_path):
    from koa_kristal_runtime.adapters.filesystem_artifact_store import FilesystemArtifactStore
    from datetime import datetime, timezone
    state = kristal_state()
    store = FilesystemArtifactStore(tmp_path / "artifacts")
    stored = store.store(state, {}, stored_at=datetime(2026, 10, 1, tzinfo=timezone.utc))
    assert stored.artifact_class.value == "kristal_state"
    assert stored.artifact_identity == state["state_id"]
    assert stored.manifest_entries == ()
    assert dict(store.read_document(stored.artifact_ref))["artifact_type"] == "kristal_state"
