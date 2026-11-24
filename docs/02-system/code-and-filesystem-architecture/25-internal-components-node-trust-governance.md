<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-025",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/ai-navigation.contract.json",
    "02-system/02-logical-architecture.md",
    "02-system/04-component-boundaries.md",
    "02-system/07-cross-component-communication.md",
    "02-system/19-release-and-artifact-identity.md",
    "04-components/04-subsystem-documentation-boundaries.md",
    "05-development/00-development-model.md",
    "06-lifecycle/02-release-model.md",
    "07-security/05-privilege-boundaries.md",
    "08-operations/00-operating-model.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/23-code-and-filesystem-architecture.md",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-002",
    "LOCK-CODE-FS-004",
    "LOCK-CODE-FS-008",
    "LOCK-CODE-FS-009"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-COMP-011",
    "DOC-COMP-IDT-001",
    "DOC-COMP-RG-001",
    "DOC-COMP-GOV-POL-001"
  ],
  "tags": [
    "internal-components",
    "node-agent",
    "identity",
    "resource-governor",
    "governance"
  ]
}
KOA:DOC-META:END -->

# Internal Components: Node, Trust, Resources, and Governance

## 1. Scope

This file freezes the baseline source inventory for four kOA-owned internal components. Each component owns its private domain and application code. Other components may import only its declared public client or generated interface bindings, never its private `src` modules.

## 2. kOA Node Agent

```text
components/koa-node-agent/README.md
components/koa-node-agent/component.toml
components/koa-node-agent/Cargo.toml
components/koa-node-agent/build.rs
components/koa-node-agent/src/lib.rs
components/koa-node-agent/src/main.rs
components/koa-node-agent/src/config.rs
components/koa-node-agent/src/health.rs
components/koa-node-agent/src/receipts.rs
components/koa-node-agent/src/domain/mod.rs
components/koa-node-agent/src/domain/command.rs
components/koa-node-agent/src/domain/request.rs
components/koa-node-agent/src/domain/authorization.rs
components/koa-node-agent/src/domain/safe_path.rs
components/koa-node-agent/src/application/mod.rs
components/koa-node-agent/src/application/dispatch.rs
components/koa-node-agent/src/application/validate_request.rs
components/koa-node-agent/src/application/execute_operation.rs
components/koa-node-agent/src/ports/mod.rs
components/koa-node-agent/src/ports/policy_client.rs
components/koa-node-agent/src/ports/receipt_store.rs
components/koa-node-agent/src/ports/system_backend.rs
components/koa-node-agent/src/ports/clock.rs
components/koa-node-agent/src/adapters/mod.rs
components/koa-node-agent/src/adapters/unix_socket.rs
components/koa-node-agent/src/adapters/filesystem_receipt_store.rs
components/koa-node-agent/src/adapters/systemd_backend.rs
components/koa-node-agent/src/adapters/mount_backend.rs
components/koa-node-agent/src/adapters/network_backend.rs
components/koa-node-agent/src/adapters/clock.rs
components/koa-node-agent/src/broker/mod.rs
components/koa-node-agent/src/broker/catalog.rs
components/koa-node-agent/src/broker/operations.rs
components/koa-node-agent/src/broker/sandbox.rs
components/koa-node-agent/src/bin/koa-node-agent.rs
components/koa-node-agent/src/bin/koa-privileged-broker.rs
components/koa-node-agent/src/bin/koa-node-agentctl.rs
components/koa-node-agent/packaging/payload.toml
components/koa-node-agent/tests/unit_command.rs
components/koa-node-agent/tests/unit_safe_path.rs
components/koa-node-agent/tests/contract_socket.rs
components/koa-node-agent/tests/integration_systemd.rs
components/koa-node-agent/tests/security_catalog.rs
components/koa-node-agent/tests/security_path_traversal.rs
```

The privileged broker is part of the Node Agent security boundary. It is not a shared utility package. Its operation catalog is closed and it never accepts an arbitrary shell command, unrestricted path, unit name, network rule, or capability request.

## 3. Identity and Trust

```text
components/identity-and-trust/README.md
components/identity-and-trust/component.toml
components/identity-and-trust/pyproject.toml
components/identity-and-trust/src/koa_identity_and_trust/__init__.py
components/identity-and-trust/src/koa_identity_and_trust/__main__.py
components/identity-and-trust/src/koa_identity_and_trust/bootstrap.py
components/identity-and-trust/src/koa_identity_and_trust/config.py
components/identity-and-trust/src/koa_identity_and_trust/health.py
components/identity-and-trust/src/koa_identity_and_trust/receipts.py
components/identity-and-trust/src/koa_identity_and_trust/domain/__init__.py
components/identity-and-trust/src/koa_identity_and_trust/domain/identity.py
components/identity-and-trust/src/koa_identity_and_trust/domain/credential.py
components/identity-and-trust/src/koa_identity_and_trust/domain/trust_root.py
components/identity-and-trust/src/koa_identity_and_trust/domain/role_binding.py
components/identity-and-trust/src/koa_identity_and_trust/domain/session_context.py
components/identity-and-trust/src/koa_identity_and_trust/application/__init__.py
components/identity-and-trust/src/koa_identity_and_trust/application/issue_local_identity.py
components/identity-and-trust/src/koa_identity_and_trust/application/verify_credential.py
components/identity-and-trust/src/koa_identity_and_trust/application/resolve_session.py
components/identity-and-trust/src/koa_identity_and_trust/application/rotate_trust_root.py
components/identity-and-trust/src/koa_identity_and_trust/application/revoke_credential.py
components/identity-and-trust/src/koa_identity_and_trust/ports/__init__.py
components/identity-and-trust/src/koa_identity_and_trust/ports/identity_store.py
components/identity-and-trust/src/koa_identity_and_trust/ports/key_store.py
components/identity-and-trust/src/koa_identity_and_trust/ports/clock.py
components/identity-and-trust/src/koa_identity_and_trust/ports/audit_sink.py
components/identity-and-trust/src/koa_identity_and_trust/adapters/__init__.py
components/identity-and-trust/src/koa_identity_and_trust/adapters/sqlite_identity_store.py
components/identity-and-trust/src/koa_identity_and_trust/adapters/filesystem_key_store.py
components/identity-and-trust/src/koa_identity_and_trust/adapters/tpm_key_store.py
components/identity-and-trust/src/koa_identity_and_trust/adapters/audit_client.py
components/identity-and-trust/src/koa_identity_and_trust/adapters/system_clock.py
components/identity-and-trust/src/koa_identity_and_trust/api/__init__.py
components/identity-and-trust/src/koa_identity_and_trust/api/models.py
components/identity-and-trust/src/koa_identity_and_trust/api/routes.py
components/identity-and-trust/migrations/README.md
components/identity-and-trust/migrations/0001_initial.sql
components/identity-and-trust/packaging/payload.toml
components/identity-and-trust/tests/conftest.py
components/identity-and-trust/tests/_support.py
components/identity-and-trust/tests/unit/test_domain.py
components/identity-and-trust/tests/unit/test_application.py
components/identity-and-trust/tests/contract/test_contracts.py
components/identity-and-trust/tests/integration/test_service.py
components/identity-and-trust/tests/failure/test_safe_degradation.py
```
## 4. Resource Governor

```text
components/resource-governor/README.md
components/resource-governor/component.toml
components/resource-governor/pyproject.toml
components/resource-governor/src/koa_resource_governor/__init__.py
components/resource-governor/src/koa_resource_governor/__main__.py
components/resource-governor/src/koa_resource_governor/bootstrap.py
components/resource-governor/src/koa_resource_governor/config.py
components/resource-governor/src/koa_resource_governor/health.py
components/resource-governor/src/koa_resource_governor/receipts.py
components/resource-governor/src/koa_resource_governor/domain/__init__.py
components/resource-governor/src/koa_resource_governor/domain/resource_envelope.py
components/resource-governor/src/koa_resource_governor/domain/resource_claim.py
components/resource-governor/src/koa_resource_governor/domain/admission_decision.py
components/resource-governor/src/koa_resource_governor/domain/degradation_state.py
components/resource-governor/src/koa_resource_governor/application/__init__.py
components/resource-governor/src/koa_resource_governor/application/admit_workload.py
components/resource-governor/src/koa_resource_governor/application/apply_envelope.py
components/resource-governor/src/koa_resource_governor/application/reconcile_usage.py
components/resource-governor/src/koa_resource_governor/application/degrade_workload.py
components/resource-governor/src/koa_resource_governor/application/restore_workload.py
components/resource-governor/src/koa_resource_governor/ports/__init__.py
components/resource-governor/src/koa_resource_governor/ports/usage_probe.py
components/resource-governor/src/koa_resource_governor/ports/node_agent.py
components/resource-governor/src/koa_resource_governor/ports/profile_provider.py
components/resource-governor/src/koa_resource_governor/ports/audit_sink.py
components/resource-governor/src/koa_resource_governor/ports/clock.py
components/resource-governor/src/koa_resource_governor/adapters/__init__.py
components/resource-governor/src/koa_resource_governor/adapters/proc_usage_probe.py
components/resource-governor/src/koa_resource_governor/adapters/systemd_usage_probe.py
components/resource-governor/src/koa_resource_governor/adapters/node_agent_client.py
components/resource-governor/src/koa_resource_governor/adapters/profile_file_provider.py
components/resource-governor/src/koa_resource_governor/adapters/audit_client.py
components/resource-governor/src/koa_resource_governor/adapters/system_clock.py
components/resource-governor/src/koa_resource_governor/api/__init__.py
components/resource-governor/src/koa_resource_governor/api/models.py
components/resource-governor/src/koa_resource_governor/api/routes.py
components/resource-governor/migrations/README.md
components/resource-governor/packaging/payload.toml
components/resource-governor/tests/conftest.py
components/resource-governor/tests/_support.py
components/resource-governor/tests/unit/test_domain.py
components/resource-governor/tests/unit/test_application.py
components/resource-governor/tests/contract/test_contracts.py
components/resource-governor/tests/integration/test_service.py
components/resource-governor/tests/failure/test_safe_degradation.py
```
## 5. Governance Policy Runtime

```text
components/governance-policy-runtime/README.md
components/governance-policy-runtime/component.toml
components/governance-policy-runtime/pyproject.toml
components/governance-policy-runtime/src/koa_governance_policy_runtime/__init__.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/__main__.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/bootstrap.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/config.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/health.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/receipts.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/domain/__init__.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/domain/policy_bundle.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/domain/policy_rule.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/domain/decision.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/domain/evaluation_context.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/application/__init__.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/application/load_bundle.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/application/activate_bundle.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/application/evaluate_policy.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/application/revoke_bundle.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/ports/__init__.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/ports/bundle_store.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/ports/signature_verifier.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/ports/decision_receipt_store.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/ports/audit_sink.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/ports/clock.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/adapters/__init__.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/adapters/filesystem_bundle_store.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/adapters/identity_signature_verifier.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/adapters/filesystem_receipt_store.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/adapters/audit_client.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/adapters/system_clock.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/api/__init__.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/api/models.py
components/governance-policy-runtime/src/koa_governance_policy_runtime/api/routes.py
components/governance-policy-runtime/migrations/README.md
components/governance-policy-runtime/packaging/payload.toml
components/governance-policy-runtime/tests/conftest.py
components/governance-policy-runtime/tests/unit/test_domain.py
components/governance-policy-runtime/tests/unit/test_application.py
components/governance-policy-runtime/tests/contract/test_contracts.py
components/governance-policy-runtime/tests/integration/test_service.py
components/governance-policy-runtime/tests/failure/test_safe_degradation.py
```

## 6. Component-Local File Rules

- `component.toml` declares the component identity, entrypoints, public interfaces, owned state roots, health endpoints, package outputs, and allowed dependencies.
- `domain/` contains deterministic state and invariants and SHALL NOT import adapters.
- `application/` contains use cases and imports only domain types and ports.
- `ports/` contains interfaces required by the component.
- `adapters/` contains filesystem, database, system, and remote-interface implementations.
- `api/` exposes the admitted service interface but never performs authorization by UI visibility.
- `migrations/` is owned only by the component whose state is migrated.
- `packaging/` contains component package inputs, not release policy.
- tests SHALL address domain behavior, contract compatibility, service integration, and safe degradation separately.

## November 2026 inventory reconciliation — registered additions

The following implementation paths were already registered in the non-authoritative `.koa/file-architecture.lock.json` projection and are present in this checkout. They are recorded here to restore the correspondence between the normative source inventory and its machine projection. This registration does not authorize a release, privileged execution, or a change of ownership.

```text
components/identity-and-trust/migrations/0002_external_identity_bindings.sql
components/identity-and-trust/src/koa_identity_and_trust/application/external_identity.py
components/identity-and-trust/src/koa_identity_and_trust/domain/external_identity.py
components/identity-and-trust/src/koa_identity_and_trust/ports/external_identity_store.py
components/identity-and-trust/tests/integration/test_external_identity_store.py
components/identity-and-trust/tests/unit/test_external_identity_binding.py
```
