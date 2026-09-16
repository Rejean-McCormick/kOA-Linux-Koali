<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-011",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "koa_node_agent"
  ],
  "canonical_refs": [
    "contracts/components/koa-node-agent.component.json",
    "generated/component-catalog.json#/components/koa_node_agent",
    "contracts/system.contract.json#/global_boundaries/privilege",
    "contracts/system.contract.json#/critical_transitions",
    "contracts/system.contract.json#/release_and_artifact_identity",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-COMP-NODE-001",
    "REQ-COMP-NODE-002",
    "REQ-COMP-NODE-003",
    "REQ-COMP-NODE-004",
    "REQ-COMP-NODE-005",
    "REQ-COMP-NODE-006",
    "REQ-COMP-NODE-007",
    "REQ-COMP-NODE-008",
    "REQ-COMP-NODE-009",
    "REQ-COMP-NODE-010",
    "REQ-COMP-NODE-011",
    "REQ-COMP-NODE-012",
    "REQ-COMP-NODE-013",
    "REQ-COMP-NODE-014",
    "REQ-COMP-NODE-015",
    "REQ-COMP-NODE-016",
    "REQ-COMP-NODE-017",
    "REQ-COMP-NODE-018",
    "REQ-COMP-NODE-019",
    "REQ-COMP-NODE-020",
    "REQ-COMP-NODE-021",
    "REQ-COMP-NODE-022",
    "REQ-COMP-NODE-023",
    "REQ-COMP-NODE-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-AI-001",
    "LOCK-AI-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-COMP-005"
  ],
  "tags": [
    "koa_node_agent",
    "node_lifecycle",
    "privileged_broker",
    "closed_operations",
    "atomic_activation",
    "idempotency",
    "receipts",
    "rollback",
    "recovery",
    "offline_import",
    "non_ai"
  ]
}
KOA:DOC-META:END -->

# kOA Node Agent

## 1. Purpose

The kOA Node Agent is the node-local lifecycle and narrow privileged-operation component for kOA deployments.

It exposes fixed high-level operations rather than a generic administrative command surface. It performs final node-local validation, stages and activates verified artifacts, manages declared node resources, executes recovery, enforces idempotency, and emits machine-readable receipts.

The Node Agent does not become a universal system administrator, policy engine, release authority, component-data owner, container orchestrator, package manager, file-transfer service, or remote shell.

The canonical contract is `contracts/components/koa-node-agent.component.json`.

## 2. Scope

This document applies to:

- node-local lifecycle requests;
- sensitive host mutations;
- system, services, governance, and knowledge artifact staging and activation;
- rollback, revert, restore, forward repair, and recovery-target transitions;
- verified offline-bundle import;
- declared encrypted-volume operations;
- bounded allowlisted service-group operations;
- node-scoped key rotation;
- node-evidence export;
- idempotency, replay protection, receipts, health, backup, and recovery;
- requests from local components, operators, recovery workflows, or a control plane.

This document does not define:

- application business operations or authoritative application data;
- governance policy content;
- identity or trust-root ownership;
- release content or compatibility;
- artifact-class structure;
- profile membership;
- a required service manager, container runtime, operating-system layout, or orchestration platform;
- arbitrary host administration.

A systemd service, SELinux domain, rootless container layout, or local Unix socket may implement profile requirements, but an implementation recipe is not the component contract.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/components/koa-node-agent.component.json` | Node Agent responsibilities, operations, authority, interfaces, security, lifecycle, receipts, failures, and conformance |
| `generated/component-catalog.json#/components/koa_node_agent` | Component identity and registry membership |
| `contracts/system.contract.json#/global_boundaries/privilege` | Sensitive-host-mutation authority and narrow privilege path |
| `contracts/system.contract.json#/critical_transitions` | Critical transitions requiring machine-readable receipts |
| `contracts/system.contract.json#/release_and_artifact_identity` | Release compatibility, non-partial activation, and recovery behavior |
| `generated/profile-catalog.json` | Profile and overlay membership |
| `contracts/release-channels.contract.json` | System, services, governance, and knowledge channel identity |
| `contracts/artifact-classes.contract.json` | Artifact and receipt activation, recovery, integrity, signing, and retention rules |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | System, component, data, lifecycle, profile, implementation, and AI invariants |
| `generated/traceability.json` | Links among operations, decisions, requirements, profiles, tests, and evidence |
| `generated/test-catalog.json` | Registered Node Agent tests |
| `generated/evidence-catalog.json` | Registered evidence supporting Node Agent claims |

## 4. Model and Responsibilities

### 4.1 Component identity

The canonical identifier is `koa_node_agent`. The component class is `node_local_lifecycle_and_privileged_operation_broker`.

The Node Agent is a narrow broker. It accepts one registered operation, validates all required authority and state, performs one bounded node-local transition, and records the outcome.

### 4.2 Authority boundary

The Node Agent owns its request, idempotency, staging, execution, recovery, health, and receipt state.

Authority remains elsewhere for:

- application operations and data;
- policy and break-glass decisions;
- identity and trust;
- profile permission;
- release compatibility;
- artifact class and manifest meaning;
- resource allocation;
- audit disclosure;
- publication.

A control plane coordinates desired state. The target Node Agent performs final validation. Root, administrator, cluster administrator, or container-runtime control does not substitute for application or governance authority.

### 4.3 Operation classes

<!-- GENERATED:BEGIN
source=contracts/components/koa-node-agent.component.json#/operation_model/operation_classes
renderer=canonical-table-v1
-->
| Operation | Purpose | Authorization class | Host mutation | Idempotency | Receipt |
| --- | --- | --- | ---: | --- | --- |
| `inspect_node_state` | Return bounded node identity, active profile, booted release, active Release Set, health, readiness, and recovery state. | `node_inspection` | No | `repeatable_read` | `optional_unless_profile_or_security_policy_requires` |
| `stage_system_artifact` | Stage a validated system image or equivalent system-channel artifact without activating it. | `system_artifact_staging` | Yes | `request_id_and_artifact_identity` | `required` |
| `activate_system_artifact` | Activate a staged verified system artifact through an atomic boot slot, pointer, or equivalent profile-defined transition. | `system_artifact_activation` | Yes | `request_id_expected_state_and_artifact_identity` | `required` |
| `activate_service_bundle` | Activate a compatible services-channel bundle using a complete profile-authorized transition. | `service_bundle_activation` | Yes | `request_id_expected_state_and_bundle_identity` | `required` |
| `activate_governance_bundle` | Activate an accepted and compatible governance policy bundle without creating or changing policy authority. | `governance_bundle_activation` | Yes | `request_id_expected_state_and_bundle_identity` | `required` |
| `manage_knowledge_artifact` | Install, activate, pin, unpin, quarantine, or revert a registered knowledge artifact when permitted by its class and profile. | `knowledge_artifact_lifecycle` | Yes | `request_id_expected_state_artifact_identity_and_action` | `required_for_activation_quarantine_or_revert` |
| `import_offline_bundle` | Admit a verified offline bundle into quarantine or staging for controlled local validation and activation. | `offline_bundle_import` | Yes | `request_id_bundle_identity_and_target_state` | `required` |
| `manage_declared_encrypted_volume` | Create, unlock, mount, unmount, rotate, or retire a profile-declared encrypted volume through a closed operation schema. | `encrypted_volume_lifecycle` | Yes | `request_id_volume_identity_expected_state_and_action` | `required` |
| `restart_allowlisted_service_group` | Restart one profile-declared service group after validation of current state, dependency conditions, and authorization. | `service_group_control` | Yes | `request_id_service_group_expected_state` | `required_when_critical` |
| `rotate_node_scoped_key` | Perform a governed rotation of one node-scoped key without exporting raw private-key material. | `node_key_rotation` | Yes | `request_id_key_identity_expected_version` | `required` |
| `export_node_evidence` | Export an authorized bounded node-evidence package through the applicable audit and disclosure path. | `node_evidence_export` | No | `request_id_evidence_scope_and_policy_decision` | `required` |
| `enter_recovery_target` | Transition the node into a profile-defined recovery environment or mode. | `node_recovery` | Yes | `request_id_expected_state_and_recovery_target` | `required` |
| `execute_rollback_or_forward_repair` | Apply the declared recovery strategy for a failed activation or migration. | `node_recovery` | Yes | `request_id_failed_transition_and_recovery_plan` | `required` |
<!-- GENERATED:END -->

The operation allowlist is closed. Each class has a versioned request schema, authorization class, preconditions, expected state, idempotency rules, timeout, bounded parameters, result schema, stable errors, receipt policy, and recovery behavior.

### 4.4 Prohibited interface

The Node Agent does not expose:

- arbitrary shell execution;
- arbitrary systemd or service-manager control;
- arbitrary file copy or path traversal;
- arbitrary container image or argument execution;
- generic package-manager access;
- unrestricted device access;
- raw private-key export;
- direct application database writes;
- AI-selected operations or parameters.

A new operation class requires canonical contract, security, profile, requirement, test, evidence, and compatibility updates.

### 4.5 Request and idempotency model

A canonical request contains:

`json
{
 "operation": "activate_service_bundle",
 "request_id": "uuid",
 "caller_identity": "component-or-operator-identity",
 "profile_context_ref": "contracts/profiles/sovereign-linux-node.profile.json",
 "policy_decision_ref_when_required": "decision-receipt-reference",
 "artifact_or_target_refs": ["artifact-reference"],
 "expected_current_state": {"active_release_set": "release-set-reference"},
 "parameters": {},
 "deadline_or_timeout": "declared-limit",
 "correlation_id": "correlation-reference"
}
`

The canonical request body is used for idempotency and replay protection. An equivalent repeat returns the recorded result. Reusing the identity with different content is rejected.

### 4.6 Interfaces

<!-- GENERATED:BEGIN
source=contracts/components/koa-node-agent.component.json#/interfaces/commands
renderer=canonical-table-v1
-->
| Command | Caller | Request fields | Responses |
| --- | --- | --- | --- |
| `execute_node_operation` | `authorized_local_component_or_control_plane` | `operation`, `request_id`, `caller_identity`, `profile_context_ref`, `policy_decision_ref_when_required`, `artifact_or_target_refs`, `expected_current_state`, `parameters`, `deadline_or_timeout`, `correlation_id` | `accepted`, `completed`, `rejected`, `conflict`, `timed_out`, `failed`, `recovery_required` |
| `cancel_node_operation` | `authorized_request_owner_or_operator` | `request_id`, `reason` | `cancelled`, `not_cancellable`, `already_completed`, `not_found`, `failed` |
| `acknowledge_recovery_result` | `authorized_recovery_or_lifecycle_component` | `failed_request_id`, `recovery_receipt_ref`, `verified_current_state` | `acknowledged`, `rejected`, `conflict`, `failed` |
<!-- GENERATED:END -->

<!-- GENERATED:BEGIN
source=contracts/components/koa-node-agent.component.json#/interfaces/queries
renderer=canonical-table-v1
-->
| Query | Authorization | Default result |
| --- | ---: | --- |
| `get_node_agent_capabilities` | Required | `profile_enabled_operation_classes_and_versions` |
| `get_node_operation_status` | Required | `bounded_request_state_and_receipt_reference` |
| `get_node_agent_health` | Required | `bounded_health_readiness_staging_and_recovery_state` |
<!-- GENERATED:END -->

The transport is profile-defined and authenticated. A local Unix socket is permitted. Direct database access and unregistered interfaces are outside the contract.

### 4.7 Owned data

<!-- GENERATED:BEGIN
source=contracts/components/koa-node-agent.component.json#/data_boundaries/authoritative_entities
renderer=canonical-table-v1
-->
| Entity | Purpose |
| --- | --- |
| `node_operation_request_record` | Canonicalized node-agent record used for idempotency, replay protection, and execution state. |
| `node_staging_record` | Node-local record of one validated staged artifact or offline bundle. |
| `node_operation_receipt` | Machine-readable record of one privileged host mutation or critical lifecycle transition. |
| `node_recovery_record` | Node-local record of rollback, restore, forward-repair, or recovery-target execution. |
<!-- GENERATED:END -->

Staging or caching an artifact does not transfer artifact ownership. Observing control-plane desired state does not make it node authority. The Node Agent does not persist application-component source data.

### 4.8 Activation and recovery model

Before activation, the Node Agent validates caller, authorization, profile, artifact class, manifest, integrity, signature, trust, release compatibility, expected state, capacity, and recovery readiness.

Activation uses a complete-state mechanism such as an atomic pointer, boot slot, transaction, or immutable slot switch.

The resulting state is either the previous valid state or the complete new state. Recovery follows the artifact contract through rollback, revert, restore, forward repair, or reconstruction.

The Node Agent owns the privileged **host operation and its receipt**, not the semantic active state of every artifact class. For example, Kristal Runtime owns `kristal_activation_state`; a service owner owns service lifecycle state; and kOA Spaces owns its validated presentation activation state. The Node Agent MUST NOT infer artifact selection, business authority, or epistemic/reference authority from its ability to perform a privileged switch.

### 4.9 Security and privilege

The Node Agent uses a profile-defined privileged execution identity and minimum required privilege. Operation, path, service-group, parameter, and device allowlists constrain the execution path.

Implementation hardening may include systemd sandboxing, a dedicated SELinux domain, minimal Linux capabilities, `NoNewPrivileges`, protected system paths, private temporary storage, restricted address families, resource limits, and a local Unix socket.

Break-glass uses separate operation classes and stronger policy. Caller UID alone is not emergency authority.

### 4.10 Receipts, resources, and external integrations

Critical transition receipts record request, caller, profile, policy reference, before and after state, artifacts or targets, result, reasons, timing, correlation, and recovery information.

Resource Governor limits concurrency, staging, verification, activation, recovery, I/O, networking, queues, and diagnostics. Governance Policy Runtime remains the policy authority.

ChatGPT, Suno, Gamma, and the Ariane voice adapter have no Node Agent operation path. They cannot select, authorize, parameterize, execute, validate, repair, or acknowledge privileged node operations.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-NODE-001,REQ-COMP-NODE-002,REQ-COMP-NODE-003,REQ-COMP-NODE-004,REQ-COMP-NODE-005,REQ-COMP-NODE-006,REQ-COMP-NODE-007,REQ-COMP-NODE-008,REQ-COMP-NODE-009,REQ-COMP-NODE-010,REQ-COMP-NODE-011,REQ-COMP-NODE-012,REQ-COMP-NODE-013,REQ-COMP-NODE-014,REQ-COMP-NODE-015,REQ-COMP-NODE-016,REQ-COMP-NODE-017,REQ-COMP-NODE-018,REQ-COMP-NODE-019,REQ-COMP-NODE-020,REQ-COMP-NODE-021,REQ-COMP-NODE-022,REQ-COMP-NODE-023,REQ-COMP-NODE-024 -->
- **REQ-COMP-NODE-001 — SHALL:** The kOA Node Agent shall expose only registered, versioned, closed high-level operation classes.
- **REQ-COMP-NODE-002 — SHALL NOT:** The kOA Node Agent shall expose arbitrary shell execution, arbitrary service-manager control, arbitrary file copy or path traversal, arbitrary container execution, generic package-manager access, unrestricted device access, or raw private-key export.
- **REQ-COMP-NODE-003 — SHALL:** Each operation class shall define a closed request schema, authorization class, profile permission, preconditions, expected current state, idempotency behavior, timeout, bounded parameters, result schema, stable error codes, receipt policy, and recovery behavior when mutating.
- **REQ-COMP-NODE-004 — SHALL:** Each request shall be bound to an authenticated caller, active profile context, applicable policy decision, declared targets or artifacts, expected state, deadline, and correlation identity.
- **REQ-COMP-NODE-005 — SHALL:** The Node Agent shall perform final node-local validation even when a request originates from a control plane or administrator.
- **REQ-COMP-NODE-006 — SHALL NOT:** A control-plane request, root identity, host administrator identity, or container-orchestrator role shall not be treated as sufficient application or governance authority.
- **REQ-COMP-NODE-007 — SHALL:** Equivalent repeated requests using the same request identity shall return the recorded result.
- **REQ-COMP-NODE-008 — SHALL NOT:** A request identity shall not be reused with a different canonical request body.
- **REQ-COMP-NODE-009 — SHALL:** Artifacts shall pass class, manifest, identity, compatibility, integrity, signature, trust, profile, capacity, and expected-state validation before activation.
- **REQ-COMP-NODE-010 — SHALL:** Mutating activation shall use an atomic pointer, boot slot, transaction, immutable slot switch, or artifact-class equivalent.
- **REQ-COMP-NODE-011 — SHALL NOT:** A crash or failed activation shall not leave partial authoritative state.
- **REQ-COMP-NODE-012 — SHALL:** A failed mutating transition shall preserve or restore the previous valid state and shall use the declared rollback, revert, restore, forward-repair, or reconstruction strategy.
- **REQ-COMP-NODE-013 — SHALL:** Privileged host mutation, artifact activation, release activation, recovery, key rotation, encrypted-volume lifecycle, offline-bundle import, and authorized evidence export shall produce machine-readable receipts.
- **REQ-COMP-NODE-014 — SHALL:** Operation receipts shall record request, caller, profile, authorization, before and after state, artifact or target identities, result, reasons, timing, correlation, and recovery information when applicable.
- **REQ-COMP-NODE-015 — SHALL:** The Node Agent shall write only its own request, staging, idempotency, receipt, and recovery state and shall not write directly to application-component authoritative source tables.
- **REQ-COMP-NODE-016 — SHALL:** Sensitive host mutations shall use the profile-authorized narrow privilege path and minimum required privilege.
- **REQ-COMP-NODE-017 — SHALL:** Break-glass operations shall use separate operation classes, stronger time-bound and scope-bound policy, receipts, and post-event review.
- **REQ-COMP-NODE-018 — SHALL:** Resource Governor shall bound concurrent operations, staging and temporary storage, verification, activation, recovery, I/O, network use, receipt queues, and diagnostics.
- **REQ-COMP-NODE-019 — SHALL:** Under resource pressure, the Node Agent shall serialize mutations, pause new activations, preserve active-transition integrity, preserve recovery and receipts, and enter inspection-only mode before integrity risk.
- **REQ-COMP-NODE-020 — SHALL:** Loss of the control plane shall preserve previously valid local node operation and shall block or visibly defer unsupported new remote changes.
- **REQ-COMP-NODE-021 — SHALL:** Verified offline import, local inspection, and recovery shall remain available where the active profile declares them.
- **REQ-COMP-NODE-022 — SHALL NOT:** Native or external AI shall not select, authorize, parameterize, execute, validate, repair, or acknowledge Node Agent operations.
- **REQ-COMP-NODE-023 — SHALL:** Backup, restore, and rebuild shall preserve idempotency records, receipts, release identity, staging manifests, recovery tokens, encrypted-volume state, and required configuration without partial authority.
- **REQ-COMP-NODE-024 — SHALL:** Every active kOA Node Agent claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Request validation

1. Receive a versioned command.
2. Canonicalize the request body.
3. authenticate the caller;
4. resolve the active profile and enabled operation class;
5. validate the applicable policy decision and expiry;
6. validate targets, artifacts, manifests, integrity, signatures, trust, and compatibility;
7. compare expected and actual node state;
8. check request identity and replay state;
9. check timeout, capacity, storage, and recovery readiness;
10. accept, reject, conflict, or defer the operation;
11. persist the request and validation result.

No host mutation occurs before validation completes.

### 6.2 Idempotent execution

1. Resolve the request identity.
2. compare the canonical body with any recorded request;
3. return the recorded result for an equivalent repeat;
4. reject a different body using the same identity;
5. acquire the operation-specific mutation lock;
6. record the before state;
7. execute the bounded operation;
8. record the after state and outcome;
9. produce the required receipt;
10. release the mutation lock.

### 6.3 Artifact staging

1. Resolve the artifact class and release channel.
2. verify manifest, identity, compatibility, integrity, signature, and trust;
3. verify profile and storage permission;
4. copy or import into the declared staging or quarantine location;
5. preserve active state;
6. record the staging manifest and evidence;
7. emit the required receipt.

Staging does not activate the candidate.

### 6.4 Artifact activation

1. Validate all activation preconditions.
2. verify the recovery point;
3. stage the complete candidate state;
4. execute artifact-class smoke and compatibility checks;
5. switch through the declared complete-state mechanism;
6. verify health, readiness, identity, and compatibility;
7. produce the activation receipt;
8. retain the previous valid state and recovery token.

A failed verification invokes the declared recovery strategy.

### 6.5 Recovery

1. Identify the failed request and transition.
2. resolve the recovery strategy and authorization;
3. verify the recovery artifact or target;
4. enter the profile-defined recovery path when required;
5. rollback, revert, restore, repair, or reconstruct;
6. verify the recovered complete state;
7. produce a recovery receipt;
8. acknowledge the result through the versioned interface;
9. block dependent claims until evidence is valid.

### 6.6 Offline-bundle import

1. Receive an explicitly selected bundle.
2. verify bundle identity, integrity, signature, trust, and compatibility;
3. import into quarantine or staging;
4. validate included artifacts independently;
5. reject undeclared or incompatible content;
6. activate nothing automatically;
7. record import and validation receipts;
8. continue through ordinary activation procedures.

### 6.7 Break-glass operation

1. Select a separate break-glass operation class.
2. authenticate the actor and recovery context;
3. validate stronger time-bound and scope-bound policy;
4. record expected state and recovery plan;
5. execute only the bounded emergency operation;
6. produce a receipt;
7. preserve evidence for mandatory post-event review;
8. end the authorization when the declared condition expires.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Unknown operation | Reject the request. | Host and agent state remain unchanged. | Execution and authority claim |
| Invalid or expired authorization | Fail closed. | Existing valid state | Requested mutation |
| Request identity reused with different body | Reject the request and preserve the original result. | Original idempotency record | Second operation |
| Expected-state mismatch | Return a conflict without mutation. | Current node state | Stale transition |
| Artifact verification or compatibility failure | Block staging or activation. | Previous valid artifact state | Candidate artifact |
| Activation failure or crash | Retain or restore the previous complete valid state and invoke declared recovery. | Previous valid state and recovery path | Partial activation |
| Receipt generation failure | Do not record a critical transition as successfully complete. | Transition evidence available before failure | Unsupported success claim |
| Control plane unavailable | Continue previously valid local operation and visibly block or defer new remote changes. | Node-local authority and recovery | Unsupported remote mutation |
| Governance Policy Runtime unavailable | Block policy-conditioned operations. | Independently authorized inspection or recovery where profile permits | Policy-conditioned mutation |
| Resource pressure | Serialize mutations, pause new activations, preserve recovery, receipts, and active-transition integrity. | Inspection and recovery | Additional mutating work |
| Node Agent unavailable | Preserve application-component authority while disabling privileged node operations. | Application state | Alternate hidden privilege path |

Failure never creates a generic privileged path or transfers application, policy, profile, release, artifact, or control-plane authority to the Node Agent.

## 8. Cross-Component Interactions

| Component or owner | Interaction | Node Agent responsibility | Retained external authority |
| --- | --- | --- | --- |
| Owning application component | Request a declared application-related transition | Validate and execute only the node-local host mutation | Application operation and data authority |
| Governance Policy Runtime | Return authorization or break-glass decision | Verify binding, scope, validity, and expiry | Policy authority |
| Identity and Trust | Verify caller, signer, trust scope, and revocation | Consume verification results | Identity and trust authority |
| Resource Governor | Apply limits and pressure controls | Classify work and preserve transition integrity | Resource authority |
| Control plane | Send coordinated desired-state requests | Perform final target-node validation and return receipts | Fleet coordination state |
| Artifact and release contracts | Define classes, compatibility, activation, and recovery | Execute the declared node-local lifecycle | Artifact and release authority |
| Audit Broker | Accept operation and transition receipts | Submit bounded registered evidence when required | Selective audit and disclosure |
| Publication Gateway | Deliver authorized public evidence | Export only a policy-authorized node-evidence package | Publication authority |
| Application services | Expose allowlisted service groups | Restart only declared groups | Application component behavior |
| Storage and recovery subsystem | Provide staged, active, previous, backup, and recovery targets | Execute declared volume and recovery operations | Storage artifact identity and retention |

No interaction authorizes direct application database writes or arbitrary host commands.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | Node lifecycle operates inside the local-first, explicit-authority system baseline. |
| `DEC-PROFILE-001` | Node Agent availability and implementation remain profile-scoped. |
| `DEC-DATA-001` | The Node Agent cannot write another component's authoritative source tables. |
| `DEC-GOV-001` | Governance Policy Runtime authorizes policy-conditioned actions and Resource Governor controls resources. |
| `DEC-REL-001` | Activations use registered artifact classes, release compatibility, receipts, and recovery. |
| `DEC-CONTAINER-001` | A container runtime is an implementation choice, not Node Agent authority. |
| `DEC-K8S-001` | Kubernetes is not an endpoint requirement and cluster administration does not grant application authority. |
| `DEC-AI-001` | Native and external AI cannot control privileged node operations. |

`ADR-012` records the accepted narrow privileged-broker architecture.

### Prohibited assumptions

- Root is application governance authority.
- A control-plane command is sufficient node authority.
- A Kubernetes administrator is application authority.
- A container runtime grants privilege over application contracts.
- A systemd unit name may be controlled arbitrarily.
- A closed operation may accept arbitrary command-line arguments or paths.
- An allowlisted service group permits control of all services.
- Staging an artifact activates it.
- A valid signature alone proves release compatibility.
- A successful command without a receipt proves a critical transition.
- Retrying a request permits changed parameters.
- A failed activation may leave a partial state.
- Break-glass may reuse an ordinary operation with caller UID as authorization.
- Node Agent unavailability permits a hidden alternate privilege path.
- Control-plane loss removes previously valid local authority.
- Offline import permits automatic activation.
- An external AI service may choose recovery steps.
- A recipe defines the global privilege implementation.
- Missing evidence may be replaced by operator confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-COMP-011`, status `active`, language `en`, component layer, and `koa_node_agent` scope.
2. All eleven required sections exist in numerical order.
3. The operation table matches `contracts/components/koa-node-agent.component.json#/operation_model/operation_classes`.
4. The command, query, and authoritative-entity tables match the canonical contract.
5. Every decision ID is accepted in `generated/decision-index.json`.
6. Every requirement ID appears exactly once in `generated/requirements-index.json`.
7. Every lock ID resolves to an active lock.
8. `TEST-COMP-NODE-001` verifies the closed registered operation allowlist.
9. `TEST-COMP-NODE-002` verifies absence of arbitrary shell, service-manager, file, container, package, device, and private-key interfaces.
10. `TEST-COMP-NODE-003` verifies caller, profile, policy, artifact, expected-state, timeout, compatibility, and resource validation.
11. `TEST-COMP-NODE-004` verifies target-node final validation for control-plane requests.
12. `TEST-COMP-NODE-005` verifies equivalent-repeat results and request-identity conflict rejection.
13. `TEST-COMP-NODE-006` verifies staging without activation and absence of partial state.
14. `TEST-COMP-NODE-007` verifies atomic activation and recovery to a complete valid state.
15. `TEST-COMP-NODE-008` verifies complete critical-transition receipts.
16. `TEST-COMP-NODE-009` verifies the narrow privilege path and rejects administrator identity as application authority.
17. `TEST-COMP-NODE-010` verifies safe degradation under policy, control-plane, artifact, receipt, resource, and component failures.
18. `TEST-COMP-NODE-011` verifies local inspection, verified offline import, and recovery without remote fallback.
19. `TEST-COMP-NODE-012` verifies absence of native or external AI operation control.
20. `TEST-COMP-NODE-013` verifies backup, restore, and rebuild without partial authority.
21. `TEST-COMP-NODE-014` verifies complete traceability to decisions, requirements, locks, tests, and evidence.
22. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
23. The generated requirement block matches the canonical requirement registry.
24. Generated tables match the canonical component contract and contain no manual semantic changes.

These criteria define required validation. They do not claim that a deployed Node Agent already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** A control plane requests activation of a services bundle. The Node Agent authenticates the request, verifies target profile permission, policy, Release Set compatibility, artifact signatures, expected current state, capacity, and recovery readiness. It rejects the request when the node state differs from the request.

> **Non-normative example:** A repeated activation request uses the same identifier and identical canonical body. The Node Agent returns the recorded result and receipt without executing the mutation a second time.

> **Non-normative example:** A request asks the Node Agent to run `systemctl restart` with a supplied unit name. The generic command is outside the contract. A valid request instead names one registered service group and uses the closed restart operation.

> **Non-normative example:** A system-image activation fails after staging but before the atomic slot switch. The active slot remains unchanged. A failure receipt identifies the candidate, stage, reason, and recovery state.

> **Non-normative example:** The control plane becomes unreachable. The node continues its previous valid local release, policies, components, and recovery capability. New coordinated changes remain blocked or visibly pending.

> **Non-normative example:** An operator imports a signed offline bundle. The Node Agent verifies and quarantines it, validates each included artifact, and produces an import receipt. Nothing activates until an ordinary authorized activation request succeeds.
