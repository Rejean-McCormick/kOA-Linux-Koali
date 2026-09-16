<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-013",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/system.contract.json#/lifecycle_model",
    "generated/component-catalog.json#/components/koa_node_agent",
    "contracts/components/koa-node-agent.component.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-LIFE-ACT-001",
    "DEC-COMP-NODE-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AUDIT-001",
    "DEC-SYS-RESOURCE-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-ACT-001",
    "REQ-LIFE-ACT-002",
    "REQ-LIFE-ACT-003",
    "REQ-LIFE-ACT-004",
    "REQ-LIFE-ACT-005",
    "REQ-LIFE-ACT-006",
    "REQ-LIFE-ACT-007",
    "REQ-LIFE-ACT-008",
    "REQ-LIFE-ACT-009",
    "REQ-LIFE-ACT-010",
    "REQ-LIFE-ACT-011",
    "REQ-LIFE-ACT-012",
    "REQ-LIFE-ACT-013",
    "REQ-LIFE-ACT-014",
    "REQ-LIFE-ACT-015",
    "REQ-LIFE-ACT-016",
    "REQ-LIFE-ACT-017",
    "REQ-LIFE-ACT-018",
    "REQ-LIFE-ACT-019",
    "REQ-LIFE-ACT-020",
    "REQ-LIFE-ACT-021",
    "REQ-LIFE-ACT-022",
    "REQ-LIFE-ACT-023",
    "REQ-LIFE-ACT-024",
    "REQ-LIFE-ACT-025",
    "REQ-LIFE-ACT-026",
    "REQ-LIFE-ACT-027",
    "REQ-LIFE-ACT-028",
    "REQ-LIFE-ACT-029",
    "REQ-LIFE-ACT-030",
    "REQ-LIFE-ACT-031",
    "REQ-LIFE-ACT-032",
    "REQ-LIFE-ACT-033",
    "REQ-LIFE-ACT-034",
    "REQ-LIFE-ACT-035",
    "REQ-LIFE-ACT-036",
    "REQ-LIFE-ACT-037",
    "REQ-LIFE-ACT-038",
    "REQ-LIFE-ACT-039",
    "REQ-LIFE-ACT-040"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-GOV-001",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-GATE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-DEV-000",
    "DOC-LIFE-003"
  ],
  "tags": [
    "activation",
    "rollback",
    "forward-repair",
    "release-set",
    "atomicity",
    "authority-last",
    "last-known-good",
    "recovery",
    "receipts",
    "offline-activation",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Activation and Rollback

## 1. Purpose

This document defines the lifecycle rules for activating, rolling back, repairing, and recovering kOA Release Sets.

Activation is the transition that changes the authoritative local release state. It is not equivalent to downloading, staging, unpacking, restarting a service, applying one migration, or verifying one artifact. A successful activation establishes one complete compatible Release Set containing the system, services, governance, and knowledge channels.

Rollback is also a complete Release Set transition. It restores a known compatible prior state and reconciles all affected artifacts, services, policies, schemas, data, and knowledge according to registered recovery contracts.

The model exists to ensure:

- no partial active authority;
- no implicit channel mixing;
- expected-state protection;
- idempotent lifecycle requests;
- complete staging before commit;
- authority activation last;
- durable last-known-good state;
- deterministic crash recovery;
- durable critical-transition receipts;
- safe rollback or forward repair;
- equivalent controls for online and offline activation.

## 2. Scope

This document applies globally to:

- Release Set activation;
- rollback;
- forward repair;
- activation recovery;
- staged artifacts;
- release-channel transitions;
- service and component activation;
- governance and authority activation;
- knowledge activation;
- schema and data migration associated with release transitions;
- trust and revocation checks;
- profile-specific lifecycle authority;
- online and offline distribution paths;
- activation receipts;
- lifecycle tests and evidence;
- emergency and recovery-environment transitions.

It applies to every node or deployment scope that claims an active kOA Release Set.

This document does not define channel membership, artifact internals, signing-key custody, build implementation, deployment schedules, or profile hardware values. Those facts remain owned by the release-channel, artifact, trust, build, profile, and component contracts.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Release channels, channel versions, Release Sets, and compatibility | `contracts/release-channels.contract.json` |
| Artifact identity, manifests, integrity, and recovery behavior | `contracts/artifact-classes.contract.json` |
| Active authority and current canonical versions | `generated/authority-manifest.json` |
| Accepted lifecycle decisions | `generated/decision-index.json` |
| Activation executor boundary | `contracts/components/koa-node-agent.component.json` |
| Node Agent identity | `generated/component-catalog.json#/components/koa_node_agent` |
| Profile activation authority and offline behavior | `contracts/profiles/*.profile.json` |
| External and offline transfer paths | `contracts/integration-types.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Lifecycle invariants | `generated/assertion-index.json` |
| Request, Release Set, artifact, test, receipt, and evidence links | `generated/traceability.json` |
| Lifecycle tests | `generated/test-catalog.json` |
| Lifecycle evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |

kOA Node Agent executes the local privileged transition where its contract applies. It does not own release compatibility, policy authorization, signing authority, artifact semantics, component business data, or profile conformance.

## 4. Lifecycle Model and Authority

### 4.1 Activation unit

The activation unit is one Release Set containing:

`text
system
services
governance
knowledge
`

Each entry identifies one specific channel version. The Release Set also binds compatibility results, tests, evidence, manifests, signatures, and recovery information.

A target node has one authoritative active Release Set per governed activation scope.

### 4.2 Lifecycle identities

Every lifecycle transition uses:

| Identity | Purpose |
| --- | --- |
| `request_id` | Stable lifecycle request identity |
| `idempotency_id` | Binds replay to one canonical request body |
| `transaction_id` | Identifies the local activation transaction |
| `release_set_id` | Identifies the target complete release combination |
| `profile_ref` | Identifies applicable lifecycle authority and constraints |
| `node_or_scope_ref` | Identifies the activation target |
| `correlation_id` | Connects workflow, audit, tests, and recovery |

A repeated request with the same canonical meaning returns the recorded result. A different meaning uses a new identity.

### 4.3 Activation authorities

The lifecycle separates these responsibilities:

| Responsibility | Owner |
| --- | --- |
| Release Set composition and compatibility | Release-channel authority |
| Artifact identity and integrity contract | Artifact-class authority |
| Signer and trust verification | Identity and Trust |
| Lifecycle authorization | Governance Policy Runtime or registered authority |
| Resource admission | Resource Governor |
| Privileged local execution | kOA Node Agent |
| Component-owned data migration | Owning component |
| Audit receipt storage | Audit Broker |
| Profile eligibility and constraints | Active profile contract |

No single successful check replaces the others.

### 4.3.1 Activation vocabulary and owner scoping

The word **activation** is always scoped to a contract and MUST NOT be treated as one global state transition. In particular:

| Activation term | Meaning | Authoritative owner |
| --- | --- | --- |
| Space activation | Makes one validated kOA Spaces definition/presentation composition current | kOA Spaces control/runtime boundary |
| Service activation | Starts/switches a service artifact or service bundle according to its component/service contract | Service artifact owner through the selected service activator |
| Runtime Pack activation | Changes the active Kristal Runtime Pack after verification/authorization | Kristal Runtime for `kristal_activation_state`; kOA Node Agent performs only the declared privileged host transition when required |
| Release Set activation | Coordinates one compatible `system` + `services` + `governance` + `knowledge` combination | Release lifecycle transaction with channel-owner adapters; no single channel acquires the others' authority |

A Space becoming active does not activate a Runtime Pack. A Runtime Pack becoming active does not imply that a complete Release Set changed. A Release Set activation does not transfer component-owned active-state records to the kOA Node Agent.

The kOA Node Agent is the narrow privileged executor for host mutations. It is not the semantic owner of every activated artifact and does not select knowledge, governance, service, or presentation state on its own.

### 4.4 Lifecycle states

The activation transaction uses:

`text
requested
identity_verified
authorization_verified
expected_state_verified
target_verified
resources_admitted
staging_verified
pre_activation_validated
transaction_started
dependent_state_committed
authority_commit_pending
authority_committed
post_activation_validated
receipt_durable
completed
`

Alternative states are:

`text
blocked
rejected
cancelled
failed
conflicted
expired
rolled_back
forward_repair_required
recovery_required
`

### 4.5 Last-known-good state

The last-known-good state identifies a complete prior Release Set that:

- was active successfully;
- remains trusted;
- remains inside the rollback floor;
- has retrievable artifacts and manifests;
- has compatible recovery contracts;
- remains valid for the profile or has an explicitly bounded recovery role.

The lifecycle contract records how long it is retained and when it can be retired.

### 4.6 Recovery strategy

Every Release Set declares one strategy:

`text
rollback
forward_repair
rollback_or_forward_repair
`

The strategy can differ by artifact or migration, but the Release Set exposes one complete executable recovery plan.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-ACT-001,REQ-LIFE-ACT-002,REQ-LIFE-ACT-003,REQ-LIFE-ACT-004,REQ-LIFE-ACT-005,REQ-LIFE-ACT-006,REQ-LIFE-ACT-007,REQ-LIFE-ACT-008,REQ-LIFE-ACT-009,REQ-LIFE-ACT-010,REQ-LIFE-ACT-011,REQ-LIFE-ACT-012,REQ-LIFE-ACT-013,REQ-LIFE-ACT-014,REQ-LIFE-ACT-015,REQ-LIFE-ACT-016,REQ-LIFE-ACT-017,REQ-LIFE-ACT-018,REQ-LIFE-ACT-019,REQ-LIFE-ACT-020,REQ-LIFE-ACT-021,REQ-LIFE-ACT-022,REQ-LIFE-ACT-023,REQ-LIFE-ACT-024,REQ-LIFE-ACT-025,REQ-LIFE-ACT-026,REQ-LIFE-ACT-027,REQ-LIFE-ACT-028,REQ-LIFE-ACT-029,REQ-LIFE-ACT-030,REQ-LIFE-ACT-031,REQ-LIFE-ACT-032,REQ-LIFE-ACT-033,REQ-LIFE-ACT-034,REQ-LIFE-ACT-035,REQ-LIFE-ACT-036,REQ-LIFE-ACT-037,REQ-LIFE-ACT-038,REQ-LIFE-ACT-039,REQ-LIFE-ACT-040 -->
- **REQ-LIFE-ACT-001 — SHALL:** Every activation target one complete validated Release Set containing exactly one compatible version of the system, services, governance, and knowledge channels.
- **REQ-LIFE-ACT-002 — SHALL NOT:** A single channel version, individual service package, governance object, knowledge artifact, or system artifact activate as an unregistered partial authority state.
- **REQ-LIFE-ACT-003 — SHALL:** Every activation request identify the target Release Set, expected active Release Set, target node or deployment scope, active profile, requesting identity, authorizing decision, correlation identity, deadline, and idempotency identity.
- **REQ-LIFE-ACT-004 — SHALL:** Every activation idempotency identity bind to one canonical request body and return the recorded result for an equivalent replay.
- **REQ-LIFE-ACT-005 — SHALL NOT:** Reuse of an activation or rollback idempotency identity with different meaning be accepted.
- **REQ-LIFE-ACT-006 — SHALL:** The activation authority verify caller identity, authorization, profile scope, trust, signature, revocation state, Release Set compatibility, artifact integrity, expected current state, resources, and recovery readiness before mutation.
- **REQ-LIFE-ACT-007 — SHALL:** All Release Set artifacts and dependent contracts be staged in inactive storage before activation begins.
- **REQ-LIFE-ACT-008 — SHALL NOT:** Download, transfer, copy, unpack, staging, signature verification, compatibility verification, or service restart be reported as completed activation.
- **REQ-LIFE-ACT-009 — SHALL:** Activation use an atomic mechanism or validated equivalent that yields either the prior complete valid state or the new complete valid state after interruption.
- **REQ-LIFE-ACT-010 — SHALL:** The active authority index or equivalent active Release Set pointer change after every dependent artifact, service, policy, contract, and knowledge object is committed.
- **REQ-LIFE-ACT-011 — SHALL NOT:** The authority index declare a Release Set active before dependent objects have completed their activation transaction.
- **REQ-LIFE-ACT-012 — SHALL:** Activation success require the privileged effect to be committed, the active state to match the target Release Set, post-activation validation to pass, and the activation receipt to be durable.
- **REQ-LIFE-ACT-013 — SHALL:** Every activation preserve the prior complete Release Set as the last-known-good state for the applicable rollback or forward-repair interval.
- **REQ-LIFE-ACT-014 — SHALL:** Every activation verify that an applicable rollback, forward-repair, or rollback-or-forward-repair path is available before committing.
- **REQ-LIFE-ACT-015 — SHALL NOT:** An activation proceed when required recovery artifacts, trust material, manifests, tests, or evidence are missing, revoked, incompatible, corrupted, or unverifiable.
- **REQ-LIFE-ACT-016 — SHALL:** Pre-activation validation include artifact, channel, profile, component, schema, migration, storage, resource, trust, security, offline, and recovery checks applicable to the target.
- **REQ-LIFE-ACT-017 — SHALL:** Post-activation validation verify the active Release Set identity, all four channel versions, service and component readiness, governance authority, knowledge availability, data migrations, interfaces, audit delivery, and recovery state.
- **REQ-LIFE-ACT-018 — SHALL:** A failed pre-activation check preserve the prior active Release Set and keep staged objects inactive.
- **REQ-LIFE-ACT-019 — SHALL:** A failed post-activation check trigger the registered rollback or forward-repair decision path and prevent an unqualified active conformance claim.
- **REQ-LIFE-ACT-020 — SHALL:** Rollback target one complete prior Release Set that remains trusted, compatible, permitted by the rollback floor, locally or remotely retrievable, and valid for the active profile.
- **REQ-LIFE-ACT-021 — SHALL NOT:** Rollback independently select channel versions, artifact versions, or service versions at execution time.
- **REQ-LIFE-ACT-022 — SHALL:** Rollback use the same identity, authorization, expected-state, idempotency, staging, atomicity, authority-last, receipt, and validation controls as forward activation.
- **REQ-LIFE-ACT-023 — SHALL:** A rollback restore or reconcile schema, data, configuration, service, policy, knowledge, and artifact state according to the target Release Set's registered recovery contracts.
- **REQ-LIFE-ACT-024 — SHALL NOT:** Rollback discard authoritative data, audit evidence, recourse state, pending transfers, or migration records merely to recover executable compatibility.
- **REQ-LIFE-ACT-025 — SHALL:** A rollback-incompatible data or schema transition use a registered forward-repair path, compensating migration, or recovery environment rather than an unsafe version reversal.
- **REQ-LIFE-ACT-026 — SHALL:** Forward repair produce a new complete validated Release Set with its own identity, tests, evidence, signature, compatibility result, and recovery path.
- **REQ-LIFE-ACT-027 — SHALL NOT:** Forward repair mutate a published channel version or active Release Set in place.
- **REQ-LIFE-ACT-028 — SHALL:** Every interrupted activation or rollback reconstruct transaction state from durable journals and verify actual host, service, artifact, and authority state before replay.
- **REQ-LIFE-ACT-029 — SHALL:** An unknown privileged effect enter recovery-required state and block blind retry until reconciliation determines the actual outcome.
- **REQ-LIFE-ACT-030 — SHALL:** Concurrent activation, rollback, forward-repair, trust-root update, and conflicting host-configuration transactions be serialized for the affected target scope.
- **REQ-LIFE-ACT-031 — SHALL:** The Resource Governor admit activation resources and protect active state, journals, receipts, rollback artifacts, and recovery reserves under pressure.
- **REQ-LIFE-ACT-032 — SHALL NOT:** Resource admission or pressure response decide release authorization, compatibility, revocation, publication, or governance policy.
- **REQ-LIFE-ACT-033 — SHALL:** Activation and rollback remain locally executable without Internet or a remote control plane when the active profile declares local or offline-transfer lifecycle support.
- **REQ-LIFE-ACT-034 — SHALL:** Offline activation verify the same manifests, signatures, compatibility, integrity, profile, trust, revocation, staging, atomicity, receipt, and recovery controls as connected activation.
- **REQ-LIFE-ACT-035 — SHALL:** Every activation, rollback, and forward-repair produce a durable critical-transition receipt containing the prior and resulting Release Sets, all channel versions, actor, authority, profile, node, transaction, tests, evidence, timing, result, and recovery references.
- **REQ-LIFE-ACT-036 — SHALL NOT:** Receipts contain secret values, raw private keys, unrestricted payloads, or sensitive evidence outside their declared audit class.
- **REQ-LIFE-ACT-037 — SHALL:** Revocation of an active or staged artifact, channel version, Release Set, signer, or trust root trigger the registered block, rollback, isolation, shutdown, or repair behavior.
- **REQ-LIFE-ACT-038 — SHALL:** Profile conformance identify the active Release Set, activation receipt, last-known-good Release Set, recovery strategy, and current lifecycle evidence.
- **REQ-LIFE-ACT-039 — SHALL:** Activation and rollback traceability connect requests, identities, decisions, profiles, Release Sets, channels, artifacts, compatibility constraints, migrations, tests, evidence, receipts, failures, and recovery actions.
- **REQ-LIFE-ACT-040 — SHALL:** Activation-and-rollback conformance include request closure, expected-state checks, complete staging, signature and compatibility verification, atomicity, authority-last sequencing, durable receipts, last-known-good preservation, rollback or repair readiness, crash recovery, offline execution, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Admission and Staging

### 6.1 Activation request

An activation request includes:

`text
request_id
idempotency_id
target_release_set_ref
expected_active_release_set_ref
node_or_scope_ref
profile_ref
requesting_identity_ref
authorization_decision_ref
resource_admission_ref
activation_window_ref
correlation_id
requested_at
deadline_at
`

Optional fields can identify an offline bundle, maintenance plan, approved interruption window, or recovery environment. The request schema remains closed.

### 6.2 Expected-state protection

The expected active Release Set is compared with the actual active state before staging validation and immediately before authority commit.

A mismatch produces a conflict. The system does not overwrite a concurrent activation or rollback.

Expected-state checks also cover applicable active configuration, schema, migration, trust, and component-state references.

### 6.3 Target verification

Target verification includes:

- Release Set lifecycle status;
- all four channel identities and versions;
- signature;
- signer trust and revocation;
- manifests;
- artifact identities;
- functional integrity records;
- compatibility constraints;
- profile eligibility;
- target architecture and environment;
- tests and evidence;
- recovery strategy.

A validated Release Set can still be ineligible for one target profile.

### 6.4 Resource admission

Resource admission accounts for:

- staging storage;
- transaction journals;
- rollback retention;
- migration workspace;
- temporary service duplication;
- restart capacity;
- post-activation tests;
- recovery reserve;
- receipt durability.

The Resource Governor can delay or reject an operation. It does not authorize the release.

### 6.5 Staging

Staging places the complete target in inactive locations.

The staging record identifies:

- target Release Set;
- source integration or offline bundle;
- staged artifact references;
- verified integrity records;
- storage locations;
- profile and target;
- staging time;
- expiry;
- cleanup behavior;
- pre-activation test references.

A staged artifact does not become active through location, file name, package installation, image pull, or successful verification.

### 6.6 Pre-activation validation

Pre-activation validation evaluates:

- active and target Release Sets;
- compatibility;
- signatures and trust;
- artifact integrity;
- profile and hardware constraints;
- component-contract compatibility;
- service dependencies;
- governance authority;
- knowledge compatibility;
- schema and migration plans;
- backup and restore readiness;
- rollback or repair material;
- offline requirements;
- resource reserves;
- test and evidence currency.

Every required result is recorded before transaction start.

## 7. Atomic Activation Procedure

### 7.1 Transaction start

The activation executor creates a durable transaction journal before the first privileged mutation.

The journal records:

- transaction identity;
- canonical request;
- expected state;
- target state;
- staged artifacts;
- planned steps;
- commit boundaries;
- compensation actions;
- last-known-good state;
- receipt destination;
- recovery environment.

### 7.2 Dependent-state commit

Dependent state can include:

- system slots or pointers;
- service packages and service manifests;
- governance artifacts and schemas;
- knowledge packages and runtime packs;
- component-owned migrations;
- local configuration;
- indexes that are contractual release artifacts.

Each step records before and after state.

A component-owned migration executes through that component's contract or registered migration authority. kOA Node Agent does not infer data transformations.

### 7.3 Authority-last commit

After every dependent object is committed and verified, the activation executor changes the active Release Set pointer or active authority index.

This pointer binds the authoritative combination. Until it changes, the staged target remains inactive.

The authority commit is serialized for the target scope.

### 7.4 Post-activation validation

Post-activation validation verifies:

- active Release Set identity;
- all four active channel versions;
- active authority references;
- component readiness;
- interface compatibility;
- governance-policy availability;
- knowledge and runtime-pack availability;
- migration completion;
- audit delivery;
- resource health;
- rollback and recovery readiness;
- profile conformance.

A degraded result is acceptable only when the target Release Set and profile explicitly define that degradation as conformant.

### 7.5 Completion

Completion occurs after:

1. the authority commit is verified;
2. post-activation validation passes;
3. the critical-transition receipt is durable;
4. the active Release Set and lifecycle evidence are visible to authorized status interfaces.

Service startup alone is not completion.

### 7.6 Receipt

The activation receipt includes:

`text
receipt_id
request_id
transaction_id
prior_release_set_ref
target_release_set_ref
prior_channel_versions
target_channel_versions
requesting_identity_ref
authorization_decision_ref
node_or_scope_ref
profile_ref
test_refs
evidence_refs
started_at
finished_at
result
rollback_or_recovery_ref
correlation_id
`

The receipt uses the `security_and_node_audit` class unless another canonical rule assigns a stricter class.

## 8. Rollback, Forward Repair, and Recovery

### 8.1 Rollback admission

Rollback admission verifies:

- current active Release Set;
- expected current state;
- target prior Release Set;
- rollback floor;
- revocation state;
- trust and signatures;
- target profile compatibility;
- artifacts and manifests;
- data and schema recovery;
- resource reserve;
- authorization;
- rollback tests and evidence.

A prior version is not automatically a valid rollback target.

### 8.2 Rollback procedure

Rollback follows the activation transaction:

`text
rollback_requested
target_prior_set_verified
expected_state_verified
rollback_resources_admitted
rollback_artifacts_staged
rollback_prechecks_passed
rollback_transaction_started
dependent_state_restored_or_reconciled
authority_pointer_restored
rollback_postchecks_passed
rollback_receipt_durable
rolled_back
`

The restored pointer identifies one complete prior Release Set.

### 8.3 Data and schema behavior

Rollback classes include:

| Class | Behavior |
| --- | --- |
| `fully_reversible` | Registered reverse migration restores compatible prior state |
| `snapshot_restore` | Verified snapshot restores the target component state |
| `dual_read_or_dual_write_transition` | Compatibility interval supports either implementation |
| `forward_only` | Rollback of executable artifacts is unsafe; forward repair is required |
| `manual_recovery` | Registered recovery environment and human authority execute the repair |

The applicable class is declared before activation.

Authoritative data is not deleted merely because an older executable version cannot read it.

### 8.4 Forward repair

Forward repair:

1. freezes the failed state sufficiently for evidence;
2. identifies affected channels and artifacts;
3. produces corrected immutable versions;
4. assembles a new Release Set;
5. runs compatibility and recovery tests;
6. obtains evidence and signature;
7. stages and activates through the normal procedure;
8. links the repair receipt to the failed transition.

The failed Release Set remains immutable and retains its lifecycle history.

### 8.5 Crash recovery

On restart, the activation executor reads the durable transaction journal and classifies the transaction:

`text
not_started
pre_commit
authority_commit_unknown
authority_committed_postcheck_incomplete
completed_receipt_pending
`

Recovery verifies actual pointers, artifacts, services, migrations, and receipts.

A transaction with an unknown authority or host effect enters `recovery_required`. The executor does not replay it until reconciliation determines the actual state.

### 8.6 Recovery environment

A recovery environment is a verified lifecycle artifact capable of:

- inspecting active and staged state;
- verifying trust and artifacts;
- reading activation journals;
- restoring the last-known-good Release Set;
- applying a forward repair;
- restoring backups;
- exporting evidence;
- preserving audit records.

Entering recovery is itself a critical transition.

### 8.7 Revocation response

Revocation can require:

- block before activation;
- quarantine staged artifacts;
- isolate an active component;
- disable a capability;
- roll back;
- enter recovery;
- apply forward repair;
- shut down a target scope.

The revocation record and profile determine the response.

### 8.8 Offline activation and rollback

Offline operation uses signed transfer bundles or locally retained artifacts.

The same lifecycle rules apply:

- complete Release Set;
- trust and signature verification;
- integrity;
- compatibility;
- expected state;
- staging;
- atomicity;
- authority last;
- receipt durability;
- local rollback or repair material.

Network absence is not an exception to lifecycle authority.

## 9. Failure Modes and Security Boundaries

### 9.1 Failure model

| Failure | Required behavior |
| --- | --- |
| Request schema invalid | Reject before staging or mutation. |
| Caller or signer untrusted | Block the transition. |
| Authorization missing, expired, or outside scope | Block the transition. |
| Expected active state mismatch | Enter conflict without mutation. |
| Release Set incomplete | Reject as invalid target. |
| Compatibility indeterminate or failed | Block the transition. |
| Artifact integrity failed | Quarantine the affected artifact and block. |
| Resource admission denied | Preserve active state and defer or reject. |
| Staging incomplete | Keep the target inactive. |
| Pre-activation test failed | Preserve prior active state. |
| Failure before authority commit | Restore or retain prior active state. |
| Authority commit outcome unknown | Enter recovery and block replay. |
| Post-activation test failed | Initiate registered rollback or repair decision path. |
| Receipt storage unavailable | Block final completion and preserve transaction state. |
| Audit Broker unavailable | Retain the receipt locally and retry without duplication. |
| Rollback target revoked or incompatible | Use forward repair or recovery environment. |
| Power loss | Recover from durable journals and actual state. |
| Network loss | Continue local lifecycle behavior supported by the profile. |
| Contract or profile invalid | Block new lifecycle mutations and preserve the last valid state. |

### 9.2 Identity and authorization

Activation uses verified:

- user or service identity;
- node identity;
- signing identity;
- artifact identity;
- profile;
- governance decision;
- target scope;
- time and freshness;
- break-glass state where applicable.

Root access, process identity, local socket access, or possession of an artifact does not establish authorization.

### 9.3 Privilege boundary

Host mutation uses the registered privileged broker.

The activation executor accepts only closed lifecycle operations and parameters. It does not expose arbitrary shell, package-manager, service-control, filesystem, container, or boot-loader interfaces.

### 9.4 Secrets and evidence

Requests, manifests, receipts, logs, and evidence use managed references.

They exclude:

- private signing keys;
- raw credentials;
- unrestricted sensitive payloads;
- another component's authoritative data;
- unbounded host snapshots.

Restricted evidence access is audited.

### 9.5 Resource boundary

The Resource Governor protects:

- active artifacts;
- transaction journals;
- receipts;
- rollback artifacts;
- recovery environment;
- migration state;
- critical services.

Resource pressure can stop optional work or reject activation. It cannot select a release or grant authority.

### 9.6 Component and gateway boundaries

Activation does not change component data ownership.

The Publication Gateway and the kOA Mediatheque admission boundary remain separate from lifecycle activation. Activating a component or artifact does not authorize cross-domain publication or transfer to the external UCKK platform.

## 10. Exceptions and Validation

### 10.1 Exceptions

A bounded exception can adjust:

- an activation window;
- a test environment;
- an evidence source;
- a profile-specific staging limit;
- a recovery interval;
- an implementation adapter;
- a compatibility interval already authorized by the release authority.

An exception cannot:

- activate a partial Release Set;
- bypass expected-state checks;
- bypass trust, signature, compatibility, or integrity verification;
- change authority before dependent state;
- remove transaction journaling;
- remove last-known-good preservation;
- authorize unsafe rollback;
- permit blind replay after an unknown effect;
- remove durable receipts;
- weaken offline activation controls;
- authorize a false active claim.

### 10.2 Validation criteria

This document is conformant when validation confirms:

1. every activation and rollback targets one complete Release Set;
2. the request schema is closed;
3. idempotency identity binds to one canonical body;
4. expected active state is checked before mutation and authority commit;
5. caller, signer, artifact, profile, authorization, and target references resolve;
6. all four channel versions and manifests are present;
7. compatibility and revocation checks pass;
8. all artifacts are staged inactive before transaction start;
9. recovery material and last-known-good state exist;
10. pre-activation tests pass;
11. transaction journaling begins before privileged mutation;
12. dependent state commits before authority;
13. authority commits last;
14. post-activation tests verify the complete active state;
15. completion waits for durable receipt;
16. rollback selects a complete prior compatible Release Set;
17. migration recovery classes are explicit;
18. forward repair creates a new immutable Release Set;
19. crash recovery reconciles actual state before retry;
20. unknown effects enter recovery;
21. conflicting lifecycle transactions are serialized;
22. resource admission and governance authorization remain separate;
23. offline activation uses equivalent authority and integrity controls;
24. receipts exclude secrets and unrestricted payloads;
25. profile claims include active and last-known-good lifecycle state;
26. every decision, profile, component, Release Set, channel, artifact, migration, test, evidence, receipt, and exception reference resolves;
27. no prohibited open-state marker enters active lifecycle authority.

The principal validation entry point is:

`bash
python docs/tools/validate_docs.py
`

Supporting checks include:

`text
tools/check_release_sets.py
tools/check_artifact_contracts.py
tools/check_component_boundaries.py
tools/check_interfile_locks.py
tools/check_profile_inheritance.py
tools/check_traceability.py
tools/check_decision_closure.py
tools/check_no_unresolved_state.py
`

A failed lifecycle check blocks the affected activation, rollback, repair, recovery completion, or conformance claim.

## 11. Non-Normative Examples

### 11.1 Standard activation

A node stages a validated Release Set, verifies all channel manifests and recovery artifacts, runs prechecks, commits dependent state, changes the authority pointer, runs postchecks, and records a durable receipt.

### 11.2 Expected-state conflict

An operator requests activation based on Release Set A, but Release Set B is now active. The request enters conflict and performs no mutation.

### 11.3 Pre-activation failure

A service migration test fails before transaction start. The staged target remains inactive, and the prior Release Set remains active.

### 11.4 Post-activation failure

The authority pointer commits, but a required component fails readiness. The lifecycle invokes the registered rollback-or-forward-repair decision path and blocks the new conformance claim.

### 11.5 Complete rollback

A services defect requires rollback. The node restores the prior complete Release Set, including its system, services, governance, and knowledge versions, instead of reverting only the service package.

### 11.6 Forward-only migration

A governance schema migration cannot be reversed safely. The release declares `forward_only`, so recovery produces and activates a corrected Release Set.

### 11.7 Power loss

Power fails after dependent state commit but before the authority result is known. On restart, the Node Agent inspects the journal and actual authority pointer before choosing completion, rollback, or recovery.

### 11.8 Offline activation

A sovereign-offline node imports a signed Release Set bundle. It verifies trust, integrity, compatibility, profile eligibility, and rollback material locally, then uses the same atomic activation procedure.

### 11.9 Receipt delivery outage

Audit Broker is unavailable after a successful local commit. The lifecycle receipt remains locally durable, completion state remains explicit, and delivery resumes idempotently when the broker returns.

### 11.10 Revoked target

A staged Release Set is revoked before activation. The node quarantines it, preserves the active Release Set, and follows replacement guidance from the revocation record.
