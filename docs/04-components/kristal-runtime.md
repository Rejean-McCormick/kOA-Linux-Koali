<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-KRISTAL-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "component:kristal_runtime"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/components/kristal-runtime.component.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/artifact-contracts/runtime-pack.schema.json"
  ],
  "decision_ids": [
    "DEC-SYS-KRISTAL-001",
    "DEC-DATA-001",
    "DEC-AI-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-COMP-KRISTAL-001",
    "REQ-COMP-KRISTAL-002",
    "REQ-COMP-KRISTAL-003",
    "REQ-COMP-KRISTAL-004",
    "REQ-COMP-KRISTAL-005",
    "REQ-COMP-KRISTAL-006",
    "REQ-COMP-KRISTAL-007",
    "REQ-COMP-KRISTAL-008",
    "REQ-COMP-KRISTAL-009",
    "REQ-COMP-KRISTAL-010",
    "REQ-COMP-KRISTAL-011",
    "REQ-COMP-KRISTAL-012",
    "REQ-CONST-COMP-009",
    "REQ-SYS-DATA-017"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-COMP-000"
  ],
  "tags": [
    "components",
    "kristal",
    "epistemic-runtime",
    "runtime-pack",
    "knowledge-channel",
    "atomic-activation",
    "content-identity",
    "safe-degradation"
  ]
}
KOA:DOC-META:END -->

# Kristal Runtime

Kristal Runtime is a native kOA-Linux component. **Kristal is the broader ecosystem system**; its Specification and implementation remain the owner of Kristal epistemic/artifact semantics. This component owns only the local runtime boundary declared here.

## 1. Purpose

Kristal Runtime is the transversal epistemic-artifact runtime of the kOA operating environment.

It resolves Kristal identity from canonical epistemic content, verifies compatible Runtime Packs, activates one valid pack atomically, exposes runtime status, and preserves recoverable activation evidence.

Kristal Runtime is intentionally narrower than a workflow engine, application database, policy authority, resource scheduler, privileged host agent, or external AI service. Its transversal role allows components to consume verified epistemic artifacts without merging their operational ownership.

## 2. Scope

This document applies to:

- the `kristal_runtime` component;
- Kristal content-identity resolution;
- Runtime Pack validation, activation, status, rollback, and recovery;
- Kristal artifacts admitted through active artifact contracts;
- the knowledge release channel;
- component and profile interactions that consume Kristal Runtime;
- runtime verification, compatibility, health, receipts, tests, and evidence.

This document does not:

- define tenant workflow state;
- define Orgo or Konnaxion application state;
- define UCKK media ownership;
- define Ariane interface state;
- provide a universal operational database;
- provide universal workflow execution;
- own authorization or resource scheduling;
- perform host privilege operations;
- provide native or external AI processing;
- own release-channel identity;
- assign profile membership outside active profile contracts.

Detailed canonical behavior remains owned by:

`text
contracts/components/kristal-runtime.component.json
`

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/component-catalog.json#/components/kristal_runtime` | Owns component identity, classification, primary responsibility, and high-level boundary. |
| `generated/component-catalog.json` | Owns contract catalog membership, path, active version, and lifecycle status. |
| `contracts/components/kristal-runtime.component.json` | Owns interfaces, authoritative data, activation behavior, dependencies, failure states, security, observability, tests, and evidence. |
| `contracts/profiles/*.profile.json` | Owns profile membership, activation mode, physical topology, and profile-scoped constraints. |
| `contracts/release-channels.contract.json#/channels/knowledge` | Owns knowledge release-channel identity and membership. |
| `contracts/artifact-contracts/runtime-pack.schema.json` | Owns the Runtime Pack artifact format. |
| `contracts/artifact-contracts/kristal-artifact.schema.json` | Owns the Kristal artifact format. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns component, data, AI, and lifecycle alignment assertions. |
| `generated/traceability.json` | Owns decision, requirement, lock, test, and evidence relationships. |
| `generated/test-catalog.json` and `generated/evidence-catalog.json` | Own conformance test and evidence identities. |

This Markdown document explains the component contract and does not redefine its canonical values.

## 4. Model and Responsibilities

### 4.1 Component role

Kristal Runtime provides a stable runtime boundary between epistemic artifacts and the components that consume them.

Its owned responsibilities are:

- resolving Kristal content identity;
- recording Runtime Pack verification state;
- evaluating Runtime Pack compatibility;
- selecting the active Runtime Pack;
- recording activation and rollback state;
- producing activation receipts;
- exposing runtime health.

The component does not own application workflows, tenant state, component business state, policy, resources, privilege, external AI, or release-channel definitions.

For Runtime Pack deployment, Kristal Runtime is the authoritative owner of the **local Kristal runtime state**: verification outcome, compatibility state, active-pack identity, rollback target, runtime indexes/provenance, revocation state, and query-contract state. When a host mutation requires privilege, Kristal Runtime requests the declared narrow transition through kOA Node Agent; that privileged execution does not transfer `kristal_activation_state` ownership to the Node Agent.

This ownership is scoped to Kristal Runtime Packs. It does not make Kristal Runtime the owner of Space activation, service activation, governance activation, system-image activation, or Release Set composition.

### 4.2 Identity model

Kristal identity is based on canonical epistemic content.

The identity model is independent from:

- tenant workflow state;
- user-interface state;
- deployment topology;
- runtime cache state.

A workflow can reference a Kristal identity. It does not become part of that identity. A user interface can display or select a Kristal artifact. It does not become the artifact owner.

### 4.3 Authoritative and derived data

Kristal Runtime owns three authoritative record classes:

| Record | Purpose |
| --- | --- |
| Active Runtime Pack record | Identifies the currently active verified Runtime Pack. |
| Verification record | Records identity, integrity, trust, compatibility, channel, and policy results. |
| Activation record | Records atomic activation, rollback, blocked, or failed outcomes and receipt references. |

Loaded caches and read models are derived. They can be rebuilt and cannot act as mutation sources.

### 4.4 Artifact boundary

Kristal Runtime accepts:

- Runtime Packs through the Runtime Pack artifact contract;
- Kristal artifacts through the Kristal artifact contract.

Both artifact classes belong to the knowledge release channel.

A candidate Runtime Pack is rejected when its identity, digest, provenance, required trust, compatibility, release channel, downgrade policy, or substitution policy fails validation.

### 4.5 Observable interfaces

The following table is an explanatory projection of the active component contract.

<!-- GENERATED:INTERFACE-SUMMARY:BEGIN source=contracts/components/kristal-runtime.component.json#/interfaces -->
| Interface | Direction | Class | Purpose | Authoritative effect |
| --- | --- | --- | --- | --- |
| `kristal_identity_resolution` | `inbound` | `query` | Resolve or verify Kristal identity from canonical epistemic content. | none |
| `runtime_pack_validation` | `inbound` | `command` | Validate a candidate Runtime Pack before activation. | Updates only runtime_pack_verification_record. |
| `runtime_pack_activation` | `inbound` | `command` | Atomically activate a verified compatible Runtime Pack. | Atomically replaces active_runtime_pack_record after all preconditions pass. |
| `runtime_pack_rollback` | `inbound` | `command` | Restore the last valid compatible Runtime Pack after an activation or runtime failure. | Atomically restores the declared last valid runtime state. |
| `runtime_status_query` | `inbound` | `query` | Return active Runtime Pack identity, verification state, activation state, and health. | none |
<!-- GENERATED:INTERFACE-SUMMARY:END -->

Queries do not change authoritative state. Commands can change only the Kristal Runtime records named by the active contract.

### 4.6 Authority separation

Kristal Runtime interacts with several independent authorities:

| Dependency or authority | Responsibility retained outside Kristal Runtime |
| --- | --- |
| Identity and Trust | Identity, credential, signature, and trust verification |
| Resource Governor | Resource budgets, admission, scheduling, and runtime limits |
| Governance Policy Runtime | Authorization and governed exceptions when required by the effective profile |
| Audit Broker or evidence authority | Evidence custody and authorized audit views |
| Knowledge release channel | Release-channel identity and membership |
| Owning application component | Acceptance of any candidate result into application-owned authoritative state |

Kristal Runtime consumes these decisions without absorbing their authority.

### 4.7 Runtime states

The state names below are projections of the component contract.

<!-- GENERATED:STATE-SUMMARY:BEGIN source=contracts/components/kristal-runtime.component.json#/observability/exposed_states -->
| State | Meaning |
| --- | --- |
| `inactive` | No active Runtime Pack is exposed. |
| `verification_pending` | A candidate artifact is under validation. |
| `verified` | The candidate passed verification but is not yet active. |
| `active` | A verified compatible Runtime Pack is the active runtime state. |
| `blocked` | A required authority, validation, or compatibility condition is unresolved. |
| `degraded` | The runtime remains available with an explicitly reduced capability. |
| `rollback_in_progress` | The declared last valid state is being restored. |
| `failed` | The attempted transition ended without a valid active replacement. |
<!-- GENERATED:STATE-SUMMARY:END -->

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-KRISTAL-001,REQ-COMP-KRISTAL-002,REQ-COMP-KRISTAL-003,REQ-COMP-KRISTAL-004,REQ-COMP-KRISTAL-005,REQ-COMP-KRISTAL-006,REQ-COMP-KRISTAL-007,REQ-COMP-KRISTAL-008,REQ-COMP-KRISTAL-009,REQ-COMP-KRISTAL-010,REQ-COMP-KRISTAL-011,REQ-COMP-KRISTAL-012,REQ-CONST-COMP-009,REQ-SYS-DATA-017 -->
- **REQ-COMP-KRISTAL-001 — SHALL:** Kristal identity is resolved from canonical epistemic content and remains independent from tenant workflow state, interface state, deployment topology, and runtime cache state.
- **REQ-COMP-KRISTAL-002 — SHALL:** Kristal Runtime owns only Kristal content-identity resolution, Runtime Pack verification and compatibility state, active Runtime Pack selection, activation state, activation receipts, and runtime health state.
- **REQ-COMP-KRISTAL-003 — SHALL NOT:** Kristal Runtime owns tenant workflow state, component business state, universal operational storage, universal workflow execution, governance policy, resource scheduling, host privilege, external AI processing, or release-channel identity.
- **REQ-COMP-KRISTAL-004 — SHALL NOT:** Kristal Runtime writes directly to another component's authoritative storage, private queues, private files, internal object namespaces, or private state.
- **REQ-COMP-KRISTAL-005 — SHALL:** A candidate Runtime Pack is validated for schema, identity, digest, provenance, compatibility, release channel, required trust, and downgrade or substitution policy before activation eligibility is granted.
- **REQ-COMP-KRISTAL-006 — SHALL:** Kristal Runtime accepts Runtime Packs and Kristal artifacts only through the knowledge release channel and their active artifact contracts.
- **REQ-COMP-KRISTAL-007 — SHALL:** Runtime Pack activation is atomic and retains the last valid Runtime Pack until all activation preconditions pass.
- **REQ-COMP-KRISTAL-008 — SHALL NOT:** Kristal Runtime performs an implicit downgrade, artifact substitution, partial authoritative activation, or unverified artifact execution.
- **REQ-COMP-KRISTAL-009 — SHALL:** A failed activation preserves or restores the last valid runtime state and emits the declared failure, rollback, or forward-repair evidence.
- **REQ-COMP-KRISTAL-010 — SHALL NOT:** Kristal identity resolution, Runtime Pack verification, activation, rollback, or runtime operation depends on native AI or an external AI integration.
- **REQ-COMP-KRISTAL-011 — SHALL:** Kristal Runtime is active only when the effective profile explicitly declares it as required or optional and all declared prerequisites resolve.
- **REQ-COMP-KRISTAL-012 — SHALL:** Runtime Pack verification, activation, rollback, and failure transitions produce machine-readable receipts and traceable conformance evidence.
- **REQ-CONST-COMP-009 — SHALL NOT:** Kristal becomes a universal operational database, workflow engine, or substitute for component-owned authoritative state.
- **REQ-SYS-DATA-017 — SHALL NOT:** Kristal is used as a universal operational database, universal workflow state store, or replacement for component-owned authoritative data.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Resolving Kristal identity

Identity resolution follows this sequence:

1. receive a content identity claim, canonical content reference, or content digest;
2. resolve the canonical epistemic content;
3. verify the content digest;
4. calculate or confirm the Kristal identity;
5. return the resolved identity and verification outcome;
6. leave authoritative application state unchanged.

An unresolved source or invalid digest produces a non-mutating failure outcome.

### 6.2 Validating a Runtime Pack

Runtime Pack validation:

1. resolves the active artifact contract;
2. validates the artifact schema;
3. verifies artifact identity and digest;
4. verifies provenance;
5. verifies trust when required;
6. evaluates compatibility;
7. verifies knowledge-channel membership;
8. evaluates downgrade and substitution policy;
9. records the verification outcome;
10. exposes activation eligibility.

Validation alone does not activate the candidate.

### 6.3 Activating a Runtime Pack

Activation:

1. resolves a successful verification record;
2. verifies required authorization;
3. verifies required resource admission;
4. prepares the candidate runtime state;
5. keeps the previous valid state available;
6. switches the active runtime pointer atomically;
7. rebuilds or reuses compatible derived caches;
8. records the active identity and activation outcome;
9. emits the activation receipt.

Partial authoritative activation is not an accepted outcome.

### 6.4 Rolling back or repairing

Recovery:

1. identifies the last valid compatible runtime state;
2. verifies rollback authorization;
3. validates the target state;
4. performs the atomic restoration when valid;
5. emits a rollback receipt;
6. selects forward repair when rollback is unavailable or unsafe;
7. keeps unrelated component authority unchanged.

### 6.5 Changing the component contract

A semantic change to Kristal identity, authority, accepted artifact classes, activation behavior, dependency authority, or failure semantics:

1. records an accepted owner decision;
2. produces a transitive impact report;
3. updates the component registry and contract;
4. updates artifact, release, profile, requirement, and lock references;
5. updates tests and evidence;
6. updates this explanation and generated contexts;
7. passes full validation;
8. activates the replacement contract last.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved state | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Canonical content cannot be resolved | Return an unresolved identity result | Existing active Runtime Pack | Identity-dependent request | Identity-resolution outcome |
| Content or artifact digest is invalid | Reject the candidate | Existing authoritative state | Candidate use or activation | Integrity failure |
| Required trust cannot be established | Reject the candidate | Existing active Runtime Pack | Candidate activation | Trust-validation outcome |
| Runtime Pack is incompatible | Reject before activation | Last valid active Runtime Pack | Candidate activation | Compatibility report |
| Artifact uses the wrong release channel | Reject before activation | Last valid active Runtime Pack | Candidate activation | Channel-validation outcome |
| Downgrade or substitution is unauthorized | Reject before activation | Current active Runtime Pack | Requested replacement | Policy-validation outcome |
| Authorization is unavailable | Keep the governed operation blocked | Current active Runtime Pack | Activation or rollback | Authorization failure |
| Resource admission is unavailable | Keep new resource-dependent work blocked | Current active Runtime Pack | Activation work | Resource-decision failure |
| Activation fails before the atomic switch | Discard the candidate transition | Last valid active Runtime Pack | Candidate activation | Failure receipt |
| Runtime fails after activation | Begin declared rollback or forward repair | Recoverable previous state when valid | Affected runtime capability | Recovery evidence |
| Evidence custody is unavailable | Apply the active synchronous-fail or bounded-queue evidence rule | Source activation authority | Transition requiring unavailable mandatory evidence | Evidence-path state |
| Optional consumer is unavailable | Keep only that consumer integration unavailable | Kristal Runtime and other consumers | Consumer-specific capability | Dependency-health record |

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust supplies credential, signature, and trust verification when required by the active profile or artifact policy.

Kristal Runtime records the verification outcome but does not become the identity authority.

### 8.2 Resource Governor

The Resource Governor supplies resource admission and runtime limits for verification, activation, cache loading, rollback, and runtime operation.

A resource grant does not authorize artifact activation.

### 8.3 Governance Policy Runtime

The Governance Policy Runtime supplies authorization for policy-gated activation, rollback, or restricted status access when required.

A policy decision does not perform the Kristal Runtime state transition.

### 8.4 Audit and evidence

Kristal Runtime emits verification, activation, rollback, and failure receipts.

The Audit Broker or active evidence authority can preserve those receipts without gaining the right to rewrite Kristal Runtime state.

### 8.5 Application components

Konnaxion, Orgo, UCKK, Ariane, or another component can consume verified Kristal identities or artifacts through active contracts.

Kristal Runtime does not write directly to those components. Candidate content becomes application-owned state only after the receiving component accepts it through its own contract.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-SYS-KRISTAL-001` | Establishes Kristal as a transversal epistemic foundation without universal operational ownership. |
| `DEC-DATA-001` | Preserves logical data ownership and prohibits direct cross-component writes. |
| `DEC-AI-001` | Keeps native system authority free of generative and autonomous AI behavior. |
| `DEC-REL-001` | Establishes release-channel identity and compatible Release Sets. |

### Prohibited assumptions

- transversal means universal operational authority;
- a Kristal identity includes tenant workflow or interface state;
- a loaded cache is authoritative;
- Runtime Pack verification is equivalent to activation;
- a candidate artifact can run before validation completes;
- the newest version is automatically compatible;
- a downgrade or substitution is safe without explicit authorization;
- a Runtime Pack can arrive through any release channel;
- an activation can leave partial authoritative state;
- a receipt can replace the activation record;
- Kristal Runtime can write directly to a consumer's database;
- a profile includes Kristal Runtime because the component exists in the repository;
- AI is required to resolve Kristal identity or activate a Runtime Pack;
- Kristal Runtime owns policy, resource scheduling, host privilege, or workflow execution;
- failure transfers Kristal authority to another component.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-COMP-KRISTAL-001` is active at `04-components/kristal-runtime.md`.
2. The component registry contains the active `kristal_runtime` identity.
3. The component-contract index resolves the active Kristal Runtime contract.
4. The contract validates against `schemas/component-contract.schema.json`.
5. Every canonical reference resolves.
6. Every listed decision exists with status `accepted`.
7. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
8. Every listed lock exists and is active.
9. Contract identity, documentation path, component identity, and profile references agree.
10. Kristal identity remains independent from workflow, interface, topology, and cache state.
11. Kristal Runtime does not own universal operational storage or workflow execution.
12. No interface permits direct writes to another component's authoritative state.
13. Runtime Packs validate schema, identity, digest, provenance, compatibility, channel, required trust, and replacement policy.
14. Runtime Packs and Kristal artifacts resolve to the knowledge release channel.
15. Activation is atomic and preserves the last valid state.
16. Unauthorized downgrade, substitution, partial activation, and unverified execution fail validation.
17. Rollback or forward-repair behavior resolves for activation failure.
18. Native and external AI dependency lists remain empty.
19. Profile membership resolves only from active profile contracts.
20. All five interface identifiers match the active component contract.
21. All exposed runtime states match the active component contract.
22. Verification, activation, rollback, and failure transitions map to tests and evidence.
23. Active prose is English and contains no unresolved-authority marker.
24. No normative keyword appears outside the generated requirement block.
25. The documentation dependency graph remains acyclic.

The validation entry point is:

`bash
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates identity independence.

Orgo can associate a workflow item with a Kristal identity. Changing the workflow status does not change the Kristal identity because the workflow state is outside the canonical epistemic content.

> **Non-normative example:** This example illustrates atomic activation.

Kristal Runtime can validate a new Runtime Pack while the previous pack remains active. Only after every precondition succeeds does the active pointer switch to the new pack.

> **Non-normative example:** This example illustrates recovery.

A new Runtime Pack can pass static verification but fail during runtime initialization. Kristal Runtime can restore the last valid pack or enter a declared forward-repair state without modifying consumer databases.

> **Non-normative example:** This example illustrates candidate acceptance.

A component can consume a verified Kristal artifact as candidate input. That component applies its own validation before creating application-owned authoritative state.
