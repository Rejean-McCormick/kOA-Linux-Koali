<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-008",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "artifact_family:kristal",
    "release_channel:knowledge",
    "component:kristal_runtime"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/components/kristal-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/subsystems/orgo.subsystem.json",
    "contracts/subsystems/konnaxion.subsystem.json",
    "contracts/subsystems/sentient.subsystem.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-KRISTAL-001",
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-ART-001",
    "DEC-SENT-001",
    "DEC-AI-001",
    "DEC-DATA-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-GOV-001",
    "DEC-COMP-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-KRISTAL-001",
    "REQ-LIFE-KRISTAL-002",
    "REQ-LIFE-KRISTAL-003",
    "REQ-LIFE-KRISTAL-004",
    "REQ-LIFE-KRISTAL-005",
    "REQ-LIFE-KRISTAL-006",
    "REQ-LIFE-KRISTAL-007",
    "REQ-LIFE-KRISTAL-008",
    "REQ-LIFE-KRISTAL-009",
    "REQ-LIFE-KRISTAL-010",
    "REQ-LIFE-KRISTAL-011",
    "REQ-LIFE-KRISTAL-012",
    "REQ-LIFE-KRISTAL-013",
    "REQ-LIFE-KRISTAL-014",
    "REQ-LIFE-KRISTAL-015",
    "REQ-LIFE-KRISTAL-016",
    "REQ-LIFE-KRISTAL-017",
    "REQ-LIFE-KRISTAL-018",
    "REQ-LIFE-KRISTAL-019",
    "REQ-LIFE-KRISTAL-020",
    "REQ-LIFE-KRISTAL-021",
    "REQ-LIFE-KRISTAL-022",
    "REQ-LIFE-KRISTAL-023",
    "REQ-LIFE-KRISTAL-024",
    "REQ-LIFE-KRISTAL-025",
    "REQ-LIFE-KRISTAL-026",
    "REQ-LIFE-KRISTAL-027",
    "REQ-LIFE-KRISTAL-028",
    "REQ-LIFE-KRISTAL-029",
    "REQ-LIFE-KRISTAL-030",
    "REQ-LIFE-KRISTAL-031",
    "REQ-LIFE-KRISTAL-032",
    "REQ-LIFE-KRISTAL-033",
    "REQ-LIFE-KRISTAL-034"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-015",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011",
    "DOC-CONST-012",
    "DOC-SYS-001",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-DEV-015"
  ],
  "tags": [
    "kristal",
    "epistemic-artifacts",
    "runtime-pack",
    "working-exchange",
    "reference-exchange",
    "knowledge-channel",
    "query-contract",
    "provenance",
    "authority-recognition",
    "audience-scope",
    "offline",
    "revocation",
    "rollback"
  ]
}
KOA:DOC-META:END -->

# Kristal Artifacts

## 1. Purpose

This document defines the lifecycle of Kristal epistemic artifacts from source intake through runtime use, revision, supersession, revocation, export, and recovery.

Kristal is one independently owned epistemic ecosystem system. Its Specification and implementation define portable identity, provenance, validation, recognition, distribution, query, Runtime Pack, and related artifact semantics. kOA-Linux defines only the local platform lifecycle around artifacts it receives or runs; it does not become the Kristal specification owner.

The lifecycle separates:

- source and candidate material;
- structured epistemic state;
- working exchange;
- validation and review;
- authority recognition;
- reference exchange;
- Runtime Pack compilation;
- knowledge-channel publication;
- runtime verification;
- atomic activation;
- deterministic query;
- rollback, supersession, revocation, and withdrawal.

The detailed runtime component behavior remains owned by:

`text
contracts/components/kristal-runtime.component.json
`

Artifact structure and lifecycle requirements remain owned by `contracts/artifact-classes.contract.json`.

## 2. Scope

This document applies to:

- source and input artifacts used to create Kristal knowledge;
- Structured Epistemic State;
- optional Claim-IR artifacts;
- optional SenTient candidate resolutions;
- Working Exchanges;
- validation decisions;
- review records;
- authority-recognition records;
- Reference Exchanges;
- federation manifests;
- reader policies;
- query contracts;
- Runtime Packs;
- knowledge-channel releases;
- revocation and supersession records;
- audience-scoped packs and encrypted shards;
- offline Kristal distribution bundles;
- runtime activation and rollback evidence;
- backup, export, restore, and federation.

It applies to public, private, community, research, institutional, exhibition, preservation, and other explicitly registered audience scopes.

It does not define:

- Orgo tasks, assignments, approvals, deadlines, or operational workflow state;
- Konnaxion participation or public interaction state;
- a universal graph database;
- unrestricted SPARQL or arbitrary query execution;
- native generative AI;
- mandatory Claim-IR or SenTient processing;
- one source format;
- one exact storage engine;
- one exact signature algorithm;
- profile-specific filesystem paths or deployment topology.

These details belong to component, profile, artifact, security, toolchain, and recipe contracts.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `generated/component-catalog.json` | Kristal Runtime identity, responsibilities, authoritative data domains, prohibited responsibilities, and architectural relationships. |
| `contracts/components/kristal-runtime.component.json` | Runtime stores, interfaces, events, states, workflows, failures, query behavior, resources, observability, and conformance. |
| `contracts/artifact-classes.contract.json` | Artifact identities, schemas, manifests, integrity, signatures, compatibility, publication, activation, rollback, revocation, retention, and evidence. |
| `contracts/release-channels.contract.json` | Knowledge-channel release identity, membership, publication, compatibility, and independent activation. |
| `generated/authority-manifest.json` | Active authority release, canonical registries, cutover state, and activation order. |
| `contracts/components/identity-and-trust.component.json` | Publisher, signer, artifact, tenant, channel, environment, node, workload, and trust-root identity. |
| `contracts/components/governance-policy-runtime.component.json` | Recognition, audience, activation, downgrade, disclosure, rights, withdrawal, exception, and emergency decisions. |
| `contracts/components/koa-node-agent.component.json` | Narrow privileged atomic activation and rollback operations. |
| `contracts/components/audit-broker.component.json` | Classified build, recognition, publication, activation, revocation, and recovery evidence. |
| `contracts/components/resource-governor.component.json` | Query, index, verification, activation, queue, and resource limits. |
| `contracts/subsystems/orgo.subsystem.json` | Accountable review, workflow, feedback, and remediation state that remains outside Kristal identity. |
| `contracts/subsystems/konnaxion.subsystem.json` | Product-facing discovery and bounded consumption of verified Kristal knowledge. |
| `contracts/components/sentient.component.json` | Optional isolated non-authoritative candidate research and reconciliation. |
| `contracts/profiles/*.profile.json` | Runtime inclusion, topology, storage, resource, network, offline, mirror, and recovery envelopes. |
| `generated/requirements-index.json` | Requirement statements displayed in section 5. |
| `generated/test-catalog.json` | Component, lifecycle, security, operations, profile, exit, and documentation tests. |
| `generated/evidence-catalog.json` | Executed build, publication, verification, activation, rollback, revocation, and restore evidence. |
| `02-system/19-release-and-artifact-identity.md` | Global release and artifact identity model. |
| `05-development/15-artifact-publication.md` | Development process for publishing knowledge-channel artifacts and releases. |

## 4. Model and Responsibilities

### 4.1 General lifecycle

`text
source or input
-> Kristal State v6 (`kristal_state`)
-> optional Claim-IR or SenTient candidate resolution
-> Working Exchange
-> review and validation decisions
-> authority recognition
-> Reference Exchange
-> Runtime Pack compilation
-> knowledge-channel publication
-> distribution or offline transfer
-> quarantine and verification
-> policy authorization
-> atomic activation
-> deterministic query
-> feedback, revision, supersession, withdrawal, or revocation
`

Each arrow represents a separately identified transition.

A later state does not erase earlier source, review, decision, or provenance identity.

### 4.2 Artifact families

| Artifact family | Purpose | Typical authority state |
| --- | --- | --- |
| Source or input artifact | Preserve original evidence, source material, metadata, and provenance. | Source or candidate |
| Kristal State v6 (`kristal_state`) | Represent assertions with typed `valuations[]`, statement `coordinates`, `applicability`, provenance, `record_role`, and `actionability` without transferring execution authority. | Draft, working, reviewed, recognized, or reference according to the v6 state contract |
| Claim-IR | Represent optional extracted or intermediate claims. | Non-authoritative candidate |
| SenTient candidate | Represent optional isolated reconciliation or enrichment output. | Non-authoritative candidate |
| Working Exchange | Carry reviewable and revisable epistemic content between tools or parties. | Working |
| Validation decision | Record structural, semantic, provenance, rights, and compatibility outcomes. | Evidence |
| Authority-recognition record | Identify the authority, scope, status, duration, dissent, and conditions of recognition. | Authority metadata |
| Reference Exchange | Carry recognized and review-complete reference content. | Recognized reference |
| Reader policy | Define contextual visibility and presentation without rewriting artifact status. | Governance input |
| Query contract | Define deterministic bounded access to Runtime Pack content. | Runtime contract |
| Runtime Pack | Package verified query-ready artifacts, indexes, metadata, and contracts for offline runtime use. | Published or active candidate |
| Revocation or supersession record | Change use, distribution, activation, or predecessor status without erasing identity. | Lifecycle authority |
| Federation manifest | Identify interoperable artifacts, authorities, scopes, endpoints, and compatibility. | Distribution metadata |

### 4.2.1 Kristal v6 contract boundary

The active structured-state contract is Kristal `6.0.0`, pinned by `contracts/integrations/kristal-v6.0.0.consumer-lock.json`. Canonicalization is `kristal.v6:jcs-rfc8785` version `1`. State mutation requires recomputing the content identity; projections are rebuildable and do not replace the canonical state. Reader Policy is a separate v6 artifact and does not rewrite state truth or authority.

The v6 semantic migration is explicit: `certainty_level`/`uncertainty` become typed `valuations[]`, `qualifiers` become statement `coordinates`, and `scope` becomes `applicability`. `record_role` and `actionability` remain separate concerns, and neither is interpreted as an implicit execution grant.

### 4.3 Responsibility domains

| Responsibility domain | Meaning |
| --- | --- |
| `runtime_pack_verification` | runtime pack verification |
| `artifact_compatibility_validation` | artifact compatibility validation |
| `tenant_and_channel_separated_pack_storage` | tenant and channel separated pack storage |
| `atomic_runtime_pack_activation` | atomic runtime pack activation |
| `runtime_pack_rollback` | runtime pack rollback |
| `bounded_deterministic_query_execution` | bounded deterministic query execution |
| `local_knowledge_indexing` | local knowledge indexing |
| `provenance_and_status_exposure` | provenance and status exposure |
| `revocation_and_downgrade_safety` | revocation and downgrade safety |

### 4.4 Authoritative runtime domains

| Data domain | Owner | Role |
| --- | --- | --- |
| `kristal_runtime_pack_storage` | Kristal Runtime | Authoritative |
| `kristal_activation_state` | Kristal Runtime | Authoritative |
| `kristal_local_indexes` | Kristal Runtime | Authoritative |
| `kristal_runtime_provenance` | Kristal Runtime | Authoritative |
| `kristal_revocation_state` | Kristal Runtime | Authoritative |
| `kristal_query_contract_state` | Kristal Runtime | Authoritative |

Operational workflow metadata remains outside these domains.

### 4.5 Content identity and contextual authority

Core Kristal content identity derives from content, structure, provenance, artifact class, and declared identity rules.

The following context does not change core content identity:

- tenant identifier;
- local ACL;
- assignment;
- task state;
- workflow approval record;
- local distribution state;
- user preference;
- reader session;
- cache state;
- local index generation.

Different tenants or authorities can recognize, restrict, distribute, supersede, or withdraw the same content differently through explicit scoped records.

### 4.6 Working and recognized states

A Working Exchange supports review, disagreement, revision, comparison, and correction.

An authority-recognition record identifies:

- recognizing authority;
- recognized artifact identity;
- recognition scope;
- audience;
- status;
- effective period;
- conditions;
- dissent or unresolved questions;
- review and appeal path;
- evidence.

A Reference Exchange packages content that has satisfied its declared review and recognition path.

Recognition remains scoped rather than universal.

### 4.7 Build identity

Every Runtime Pack build records:

- build identity;
- source artifact identities;
- source versions;
- schemas and contracts;
- toolchain and compiler identity;
- policy and reader-policy selections;
- query-contract identity;
- audience and channel;
- deterministic mode;
- resource limits;
- output identity;
- inventory;
- warnings;
- unresolved states;
- test results;
- provenance;
- publisher and signer context;
- evidence.

A rebuild is a distinct build event even when reproducibility evidence proves identical output.

### 4.8 Runtime Pack manifest

A Runtime Pack manifest contains or references:

- artifact-class identity;
- pack identity and version;
- knowledge-channel release identity;
- source lineage;
- complete file inventory;
- integrity identities required by the artifact class;
- publisher and signer identities;
- tenant, environment, channel, and audience scope;
- query-contract identity;
- schema and contract compatibility;
- runtime and profile compatibility;
- status and recognition metadata;
- reader-policy references;
- rights, consent, attribution, and cultural-authority metadata;
- external-AI restrictions;
- dependencies;
- creation, expiry, and freshness context;
- revocation and supersession references;
- migration and rollback information;
- test and evidence references.

### 4.9 Query contract

A query contract defines:

- contract identity and version;
- supported query classes;
- input structure;
- result structure;
- stable sort and tie-breaking;
- pagination;
- limits;
- timeout;
- memory and CPU budget;
- index requirements;
- audience and reader-policy inputs;
- status and provenance exposure;
- deterministic error codes;
- compatibility;
- unsupported operations.

The contract does not require a universal graph-query language.

### 4.10 Audience-specific artifacts

Restricted material is not placed into one universal pack and protected only by interface filtering when stronger segregation is required.

Permitted patterns include:

- public pack;
- community pack;
- research pack;
- institutional pack;
- exhibition pack;
- preservation pack;
- encrypted audience shard;
- separately signed restricted extension.

Audience identity, access authority, distribution, backup, query, withdrawal, and export remain aligned.

### 4.11 Reader policy

Reader policy can determine:

- which eligible claims are visible;
- ordering within the query contract;
- labels and explanatory context;
- audience-specific projections;
- treatment of disputed or superseded content;
- whether restricted references are exposed.

Reader policy cannot alter the stored underlying identity, lineage, validation, recognition, or revocation record.

### 4.12 Publication and release

Kristal artifacts publish through the knowledge channel.

Publication associates immutable identity with:

- release;
- channel;
- audience;
- authority;
- compatibility;
- availability;
- provenance;
- status.

Publication does not mutate the artifact or activate it.

System, services, and governance channels remain independently versioned and activated.

### 4.13 Activation sequence

`text
fetch or import
-> quarantine
-> bounded manifest parsing
-> verify artifact class and identity
-> verify channel and audience
-> verify publisher, signer, and trust roots
-> verify inventory and integrity
-> check revocation, freshness, downgrade, and substitution
-> check query-contract, schema, runtime, and profile compatibility
-> evaluate governance policy
-> stage the verified pack
-> execute narrow atomic activation through kOA Node Agent
-> verify health and declared query vectors
-> secure evidence
-> mark active
-> retain previous known-good state
`

The runtime never treats staging as activation.

### 4.14 Offline correctness

A node can query active packs without Internet access.

Trust roots, revocation state, policy, query contracts, and artifacts required for the claimed offline envelope are provisioned or securely cached in advance.

When freshness cannot be established, the runtime exposes that condition and applies the active stale-trust or stale-revocation policy.

### 4.15 Relationships

| Component | Relationship | Purpose |
| --- | --- | --- |
| `koa_node_agent` | `requests_atomic_activation_from` | Activate or roll back verified runtime packs through a narrow privileged operation. |
| `identity_and_trust` | `uses_trust_roots_from` | Verify publisher, signer, channel, tenant, and environment trust. |
| `governance_policy_runtime` | `requests_activation_decisions_from` | Authorize activation, downgrade, visibility, and governed query behavior. |
| `audit_broker` | `emits_verification_and_activation_events_to` | Preserve critical artifact lifecycle evidence. |
| `konnaxion` | `provides_verified_knowledge_to` | Expose bounded query and status surfaces for public consumption. |
| `orgo` | `provides_epistemic_artifacts_to` | Support operational workflows without absorbing workflow state. |

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-KRISTAL-001,REQ-LIFE-KRISTAL-002,REQ-LIFE-KRISTAL-003,REQ-LIFE-KRISTAL-004,REQ-LIFE-KRISTAL-005,REQ-LIFE-KRISTAL-006,REQ-LIFE-KRISTAL-007,REQ-LIFE-KRISTAL-008,REQ-LIFE-KRISTAL-009,REQ-LIFE-KRISTAL-010,REQ-LIFE-KRISTAL-011,REQ-LIFE-KRISTAL-012,REQ-LIFE-KRISTAL-013,REQ-LIFE-KRISTAL-014,REQ-LIFE-KRISTAL-015,REQ-LIFE-KRISTAL-016,REQ-LIFE-KRISTAL-017,REQ-LIFE-KRISTAL-018,REQ-LIFE-KRISTAL-019,REQ-LIFE-KRISTAL-020,REQ-LIFE-KRISTAL-021,REQ-LIFE-KRISTAL-022,REQ-LIFE-KRISTAL-023,REQ-LIFE-KRISTAL-024,REQ-LIFE-KRISTAL-025,REQ-LIFE-KRISTAL-026,REQ-LIFE-KRISTAL-027,REQ-LIFE-KRISTAL-028,REQ-LIFE-KRISTAL-029,REQ-LIFE-KRISTAL-030,REQ-LIFE-KRISTAL-031,REQ-LIFE-KRISTAL-032,REQ-LIFE-KRISTAL-033,REQ-LIFE-KRISTAL-034 -->
- **REQ-LIFE-KRISTAL-001 — SHALL:** Kristal source objects, Structured Epistemic States, Working Exchanges, validation decisions, authority-recognition records, Reference Exchanges, Runtime Packs, query contracts, reader policies, and revocation records have distinct artifact identities and lifecycle states.
- **REQ-LIFE-KRISTAL-002 — SHALL:** Compilation, validation, review, authority recognition, publication, distribution, staging, and activation remain distinct transitions.
- **REQ-LIFE-KRISTAL-003 — SHALL NOT:** A Working Exchange, candidate resolution, reviewed draft, or published Runtime Pack is treated as an active recognized reference merely because it exists or is available.
- **REQ-LIFE-KRISTAL-004 — SHALL:** Core Kristal content identity remains independent of tenant identifiers, access-control entries, assignments, workflow approvals, distribution status, local indexes, and reader-session state.
- **REQ-LIFE-KRISTAL-005 — SHALL:** Tenant, institution, community, and audience recognition is represented as explicit scoped authority or status metadata without rewriting the underlying content identity.
- **REQ-LIFE-KRISTAL-006 — SHALL:** Every release-grade Kristal build records source artifact identities, schema and contract versions, toolchain identity, policy selections, deterministic mode, resource limits, output identities, warnings, and unresolved states.
- **REQ-LIFE-KRISTAL-007 — SHALL:** A Runtime Pack derives only from declared source artifacts, validation decisions, recognition records, policies, and build definitions.
- **REQ-LIFE-KRISTAL-008 — SHALL:** Every Runtime Pack contains or references a manifest, complete file inventory, source lineage, query contract, compatibility constraints, audience and channel scope, status metadata, provenance, and lifecycle evidence.
- **REQ-LIFE-KRISTAL-009 — SHALL:** Runtime Pack inventory and integrity validation follows the active artifact-class contract, including signatures and content identities when required.
- **REQ-LIFE-KRISTAL-010 — SHALL:** Every query contract defines supported operations, input schema, result schema, stable ordering, bounded resource use, deterministic errors, compatibility, and versioning.
- **REQ-LIFE-KRISTAL-011 — SHALL NOT:** Reader policy, tenant policy, user-interface filtering, or query presentation rewrites the underlying artifact identity, provenance, validation state, recognition state, supersession state, or revocation state.
- **REQ-LIFE-KRISTAL-012 — SHALL:** Restricted or culturally governed content uses audience-scoped packs, encrypted shards, or another explicitly protected artifact structure when interface-only hiding would be insufficient.
- **REQ-LIFE-KRISTAL-013 — SHALL:** Consent, attribution, cultural authority, audience restrictions, export limits, AI restrictions, withdrawal, and recourse metadata remain enforceable across build, publication, query, backup, export, federation, and restore.
- **REQ-LIFE-KRISTAL-014 — SHALL:** Claim-IR, SenTient, external AI, extraction tools, and imported mappings remain optional non-authoritative candidate paths until explicit review and owning-contract admission.
- **REQ-LIFE-KRISTAL-015 — SHALL NOT:** A probabilistic score, inferred relation, external AI output, or SenTient candidate grants validation, authority recognition, publication, or activation.
- **REQ-LIFE-KRISTAL-016 — SHALL:** Kristal artifacts publish through the independent knowledge release channel and do not silently embed system, services, or governance activation authority.
- **REQ-LIFE-KRISTAL-017 — SHALL NOT:** Publication of a Kristal artifact implies staging, activation, tenant approval, audience eligibility, or runtime query availability.
- **REQ-LIFE-KRISTAL-018 — SHALL:** Kristal Runtime quarantines and verifies a candidate before it enters active runtime-pack storage.
- **REQ-LIFE-KRISTAL-019 — SHALL:** Activation verifies channel and audience scope, manifest and inventory, publisher and signer trust, revocation, downgrade and substitution resistance, query-contract compatibility, profile compatibility, policy authority, and required evidence.
- **REQ-LIFE-KRISTAL-020 — SHALL NOT:** Kristal Runtime obtains an untrusted network trust root during activation and treats that root as authoritative without an independently established trust chain.
- **REQ-LIFE-KRISTAL-021 — SHALL:** Runtime Pack activation is atomic and preserves the previous known-good compatible pack until post-activation health and query verification succeed.
- **REQ-LIFE-KRISTAL-022 — SHALL:** kOA Node Agent performs only the declared narrow privileged filesystem or activation transition after an operation-bound governance decision.
- **REQ-LIFE-KRISTAL-023 — SHALL:** A failed verification, activation, health, query-contract, migration, or evidence check leaves the previous valid active state available when safe.
- **REQ-LIFE-KRISTAL-024 — SHALL:** Rollback restores a compatible non-revoked predecessor, and forward repair follows an explicit controlled path when data, index, contract, or security conditions make rollback unsafe.
- **REQ-LIFE-KRISTAL-025 — SHALL:** Revocation and supersession preserve artifact identity, scope, reason, effective state, predecessor or replacement relationships, signer authority, and evidence.
- **REQ-LIFE-KRISTAL-026 — SHALL:** Offline nodes apply the newest trusted revocation and trust state available to them and expose freshness or staleness when current status cannot be established.
- **REQ-LIFE-KRISTAL-027 — SHALL:** Downgrade below a security, revocation, query-contract, or authority floor requires a separately authorized emergency path and visible risk evidence.
- **REQ-LIFE-KRISTAL-028 — SHALL:** Local indexes, caches, and derived query structures remain regenerable from verified Runtime Packs and do not become the sole authority for content identity or status.
- **REQ-LIFE-KRISTAL-029 — SHALL:** Kristal Runtime serves declared local query classes offline from active verified packs without requiring external AI, a remote graph service, or a control-plane connection.
- **REQ-LIFE-KRISTAL-030 — SHALL:** Direct writes from Orgo, Konnaxion, SenTient, or another component into Kristal authoritative stores are prohibited.
- **REQ-LIFE-KRISTAL-031 — SHALL:** Backup, export, restore, replication, mirror transfer, and federation preserve artifact identity, lineage, audience, recognition, query contracts, revocation, supersession, signatures, and evidence.
- **REQ-LIFE-KRISTAL-032 — SHALL:** Restoration independently revalidates trust, compatibility, revocation, audience, query contracts, and activation authority before any pack becomes active.
- **REQ-LIFE-KRISTAL-033 — SHALL:** Critical build, recognition, publication, import, verification, activation, rollback, revocation, withdrawal, export, and recovery transitions produce classified machine-readable evidence.
- **REQ-LIFE-KRISTAL-034 — SHALL:** Every active Kristal artifact and Runtime Pack claim has complete decision, requirement, lock, profile, component, artifact, release, test, evidence, exception, and authority traceability.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Source admission

1. Identify the source artifact and submitting authority.
2. parse the source through bounded input validation.
3. capture provenance, rights, consent, classification, and audience constraints.
4. retain original source identity.
5. create a Structured Epistemic State or explicit candidate artifact.
6. separate rejected and quarantined material.
7. record admission evidence.

### 6.2 Optional Claim-IR or SenTient path

1. Select an admitted source or Working Exchange.
2. create an isolated task and method identity.
3. produce candidate claims, mappings, or reconciliations.
4. preserve uncertainty, alternatives, contradictions, and sources.
5. mark the output non-authoritative.
6. submit it to the owning review workflow.
7. admit only explicitly accepted information into a new Working Exchange revision.

### 6.3 Review and validation

1. Freeze the Working Exchange revision.
2. validate schema, references, provenance, rights, and evidence.
3. evaluate semantic consistency and unresolved states.
4. run applicable deterministic validation vectors.
5. obtain required expert, community, cultural, institutional, or legal review.
6. record decisions, dissent, conditions, and recourse.
7. create a validation-decision artifact.
8. advance, revise, reject, or archive the Working Exchange.

### 6.4 Authority recognition

1. Identify the candidate Reference Exchange.
2. identify the recognizing authority and scope.
3. evaluate current rights, consent, policy, and evidence.
4. record audience, status, duration, conditions, disagreement, and appeal.
5. sign or otherwise protect the recognition record when required.
6. associate the recognition record without changing core content identity.
7. publish the recognized reference only through the declared lifecycle.

### 6.5 Runtime Pack compilation

1. Select declared Reference Exchanges and supporting artifacts.
2. select the query contract and reader-policy inputs.
3. select audience, channel, profile, and compatibility targets.
4. resolve the fixed toolchain and build definition.
5. compile query-ready structures and indexes deterministically.
6. create the complete inventory and manifest.
7. validate lineage, rights, status, recognition, and audience.
8. run query, ordering, error, performance-bound, and compatibility vectors.
9. create the immutable Runtime Pack candidate.
10. record build and validation evidence.

### 6.6 Knowledge-channel publication

1. Verify the Runtime Pack candidate under its artifact class.
2. resolve the knowledge release and channel.
3. resolve publisher, signer, review, and release authority.
4. verify compatibility and exception state.
5. sign the artifact or release manifest when required.
6. publish the immutable pack and manifest.
7. receive durable repository acknowledgement.
8. record publication evidence.
9. leave the pack inactive.

### 6.7 Online or offline import

1. Receive the pack through a repository, mirror, peer, or offline bundle.
2. copy it into quarantine.
3. apply path, size, recursion, decompression, object-count, and parser limits.
4. verify bundle and pack inventory.
5. verify identity, signature, provenance, channel, audience, and target scope.
6. evaluate replay, expiry, sequence, revocation, and compatibility.
7. register the verified candidate in runtime-pack storage.
8. keep it staged until activation authority resolves.
9. record import evidence.

### 6.8 Activation

1. Resolve the candidate pack and current active pack.
2. reverify identity, trust, revocation, compatibility, audience, and evidence.
3. obtain the operation-bound governance decision.
4. preserve the previous known-good state.
5. execute the narrow atomic activation transition through kOA Node Agent.
6. verify active manifest and inventory.
7. run declared health and query vectors.
8. secure local evidence.
9. mark the candidate active.
10. release or retain predecessors according to policy.

### 6.9 Rollback

1. Stop new queries that require the failed pack when necessary.
2. identify the compatible non-revoked predecessor.
3. verify predecessor identity, trust, query contract, audience, and compatibility.
4. resolve rollback authority.
5. switch atomically.
6. rebuild or pin derived indexes.
7. run health and query vectors.
8. record rollback evidence.
9. quarantine or supersede the failed pack.
10. resume queries.

### 6.10 Forward repair

1. freeze affected activation and distribution.
2. preserve evidence and recoverable state.
3. create or obtain the corrected pack, contract, migration, or runtime version.
4. verify the repair path and authority.
5. apply the controlled migration or activation.
6. verify content, indexes, query behavior, and status.
7. supersede or revoke the failed artifact.
8. record repair evidence.

### 6.11 Revocation, withdrawal, and supersession

1. identify the artifact and affected scope.
2. verify the lifecycle record and issuing authority.
3. block future activation or distribution as declared.
4. evaluate active-state treatment.
5. update indexes, caches, mirrors, federation, and audience packages.
6. preserve predecessor and replacement relationships.
7. expose current status and freshness.
8. retain minimal lawful evidence.
9. record remediation results.

### 6.12 Export and restore

1. export selected source, exchange, recognition, Runtime Pack, query, status, revocation, and evidence artifacts.
2. preserve complete identities and relationships.
3. independently verify the export.
4. restore into a clean target.
5. revalidate trust, audience, rights, compatibility, query contracts, and revocation.
6. rebuild derived indexes.
7. activate only through the normal activation process.
8. run clean-restore query and provenance tests.
9. record restore evidence.

## 7. Failure and Degradation

### 7.1 Invalid manifest or inventory

A malformed manifest, missing file, extra file, integrity mismatch, or unsupported artifact class leaves the pack quarantined.

The active pack remains unchanged.

### 7.2 Signature or trust failure

An invalid signer, signature, trust scope, trust root, or authority chain blocks import or activation.

Network availability does not permit accepting a newly fetched untrusted root.

### 7.3 Channel or audience mismatch

A pack published for another channel, tenant, environment, or audience remains inactive.

The runtime does not broaden its scope locally.

### 7.4 Query-contract incompatibility

A valid pack with an unsupported query contract remains published or stored but inactive for that runtime.

The previous compatible pack continues to serve queries.

### 7.5 Downgrade or substitution attempt

An older, revoked, differently scoped, or substituted pack is rejected unless an explicit emergency downgrade path authorizes the exact risk.

### 7.6 Failed activation

A failed atomic switch, health check, query vector, evidence write, or index transition does not produce an active claim.

The runtime returns to or retains the last known-good compatible state when safe.

### 7.7 Corrupted active pack

The runtime stops affected query classes, preserves evidence, verifies the predecessor, and enters rollback or recovery.

Unrelated components and valid packs remain available.

### 7.8 Revocation freshness uncertainty

An offline node displays the known revocation epoch and freshness state.

The active profile and policy determine whether use continues, becomes restricted, or blocks.

Uncertainty does not expand authority.

### 7.9 Rights or consent withdrawal

Affected audience access, distribution, query, indexes, caches, exports, and federation are updated through governed withdrawal.

The runtime preserves only the minimal evidence permitted by policy.

### 7.10 Resource pressure

Resource Governor protects:

- active-pack integrity;
- verification;
- activation and rollback;
- query cancellation;
- bounded core query classes;
- revocation handling;
- evidence;
- recovery.

Optional indexing, precomputation, federation, and heavy queries stop or throttle first.

### 7.11 Network loss

Active verified packs remain locally queryable.

Remote publication, mirror refresh, federation, and revocation updates become unavailable.

Local status exposes freshness and degraded capabilities.

### 7.12 Storage pressure

The runtime removes regenerable caches and indexes before authoritative packs, manifests, status, provenance, or revocation state.

New imports or activations block before durable integrity is lost.

### 7.13 Evidence destination failure

Required local evidence remains durable.

Forwarding can queue within bounds.

An activation requiring durable local evidence does not report completion until that evidence is secured.

## 8. Cross-Component Interactions

| Counterparty | Kristal interaction | Boundary |
| --- | --- | --- |
| Identity and Trust | Provides publisher, signer, artifact, tenant, channel, environment, node, workload, trust-root, and revocation identity. | Identity does not itself authorize activation. |
| Governance Policy Runtime | Decides recognition, audience, activation, downgrade, visibility, withdrawal, exception, and emergency behavior. | Policy does not mutate Runtime Pack files or indexes directly. |
| kOA Node Agent | Executes narrow atomic activation, rollback, and protected filesystem operations. | It does not choose the pack or grant its own authority. |
| Audit Broker | Receives classified build, publication, verification, activation, query-failure, revocation, and recovery evidence. | Audit storage does not alter epistemic status. |
| Resource Governor | Bounds verification, query, index, import, activation, queue, and recovery resources. | Resource control does not rewrite query results or authority. |
| Orgo | Manages accountable review, remediation, feedback, and operational workflow. | Orgo workflow state remains outside Kristal content identity and stores. |
| Konnaxion | Consumes bounded verified knowledge and status through explicit query contracts. | Konnaxion cannot write Kristal authoritative stores. |
| SenTient | Produces optional provenance-rich non-authoritative candidates. | SenTient cannot activate or directly edit Kristal authoritative state. |
| Knowledge repository or mirror | Distributes immutable published packs and lifecycle records. | Availability does not equal activation or audience authority. |
| Profile contracts | Define runtime inclusion, storage, topology, resources, network, offline, mirror, and recovery envelopes. | Profiles cannot weaken artifact verification or ownership rules. |

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-KRISTAL-001` | Kristal is a transversal epistemic foundation and not a workflow engine or universal operational database. |
| `DEC-LIFE-001` | Knowledge artifacts publish and activate independently from system, services, and governance releases. |
| `DEC-REL-001` | Release Sets record compatibility but do not activate Kristal packs automatically. |
| `DEC-ART-001` | Artifact classes own manifest, verification, integrity, activation, rollback, revocation, and evidence requirements. |
| `DEC-SENT-001` | SenTient is optional, isolated, task activated, and non-authoritative. |
| `DEC-AI-001` | External AI output remains optional candidate material and cannot grant epistemic authority. |
| `DEC-DATA-001` | Kristal Runtime owns only its registered pack, activation, index, provenance, revocation, and query-contract state. |
| `DEC-AUTH-001` | Recognition, publication, activation, downgrade, withdrawal, and recovery use explicit bounded authority. |
| `DEC-IDENT-001` | Content, tenant, audience, publisher, signer, artifact, release, node, workload, and authority identities remain distinct. |
| `DEC-GOV-001` | Governance Policy Runtime decides governed actions; Kristal Runtime enforces applicable decisions. |
| `DEC-COMP-001` | Cross-component access uses explicit contracts and rejects direct authoritative-store writes. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, and AI agents do not assume that:

- a candidate claim is recognized knowledge;
- a Working Exchange is a Reference Exchange;
- a Reference Exchange is an active Runtime Pack;
- publication implies activation;
- tenant approval changes core content identity;
- an ACL is part of epistemic identity;
- reader policy can erase revocation or disagreement;
- a high confidence score proves a claim;
- SenTient output is canonical;
- external AI output can grant recognition;
- one universal pack is safe for every audience;
- interface filtering alone protects restricted content;
- an active pack can fetch and trust a new root during activation;
- a valid signature proves audience eligibility or compatibility;
- a newer pack is compatible automatically;
- a local index is the authority for content identity;
- Orgo workflow state belongs inside Kristal;
- Konnaxion can edit Kristal stores;
- network loss invalidates an already verified active pack;
- stale revocation information can be hidden from the user or operator;
- rollback to a revoked pack is safe;
- restore can reactivate withdrawn or revoked authority automatically;
- a full graph database or unrestricted query language is globally required;
- ordinary Markdown documentation needs Runtime Pack integrity hashes.

A new implementation-affecting Kristal lifecycle choice requires an accepted owner decision before dependent authority becomes active.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Kristal component contract | `TEST-COMP-KRISTAL-001`, `TEST-COMP-KRISTAL-002`, `TEST-COMP-KRISTAL-003`, `TEST-COMP-KRISTAL-004`, `TEST-COMP-KRISTAL-005`, `TEST-COMP-KRISTAL-006`, `TEST-COMP-KRISTAL-007`, `TEST-COMP-KRISTAL-008`, `TEST-COMP-KRISTAL-009`, `TEST-COMP-KRISTAL-010` |
| Kristal and workflow separation | `TEST-CROSS-010`, `TEST-CROSS-015`, `TEST-SYS-013` |
| Offline and degradation | `TEST-SYS-001`, `TEST-SYS-004`, `TEST-SYS-005`, `TEST-SYS-011`, `TEST-SYS-012`, `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-008`, `TEST-OPS-003`, `TEST-OPS-006`, `TEST-OPS-010` |
| Artifact lifecycle | `TEST-LIFE-001`, `TEST-LIFE-002`, `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-008`, `TEST-LIFE-009`, `TEST-LIFE-010`, `TEST-LIFE-011`, `TEST-LIFE-014`, `TEST-LIFE-015` |
| Security, rights, and supply chain | `TEST-SEC-005`, `TEST-SEC-008`, `TEST-SEC-009`, `TEST-SEC-012`, `TEST-SEC-013`, `TEST-SEC-014`, `TEST-SEC-015` |
| Operations and recovery | `TEST-OPS-002`, `TEST-OPS-005`, `TEST-OPS-007`, `TEST-OPS-008`, `TEST-OPS-009` |
| Portability and exit | `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-005`, `TEST-EXIT-006`, `TEST-EXIT-007`, `TEST-EXIT-008` |
| Documentation and traceability | `TEST-DOC-VAL-003`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-007`, `TEST-DOC-VAL-008`, `TEST-DOC-VAL-009`, `TEST-DOC-VAL-010`, `TEST-DOC-VAL-012`, `TEST-DOC-VAL-016`, `TEST-DOC-VAL-017`, `TEST-DOC-VAL-018`, `TEST-DOC-VAL-019`, `TEST-DOC-VAL-020` |

Additional validation confirms:

1. every Kristal artifact family has a unique identity and declared lifecycle state;
2. the component identity, kind, responsibilities, data domains, relationships, and documentation references match `generated/component-catalog.json`;
3. source, Working Exchange, recognition, Reference Exchange, Runtime Pack, query contract, revocation, and supersession references resolve;
4. build identity binds exact sources, contracts, toolchain, policies, limits, outputs, warnings, and evidence;
5. Runtime Pack manifests contain complete inventory, lineage, query, compatibility, audience, status, rights, and lifecycle metadata;
6. probabilistic and external candidates remain non-authoritative;
7. knowledge-channel publication remains independent from other channels;
8. import uses bounded parsing and quarantine;
9. trust, signature, inventory, downgrade, substitution, revocation, query-contract, profile, and authority checks complete before activation;
10. activation and rollback are atomic;
11. the last known-good compatible state is retained;
12. query results have stable ordering, bounded resources, deterministic errors, and status and provenance exposure;
13. reader policy cannot rewrite underlying artifact state;
14. audience-scoped artifacts enforce their audience and rights;
15. offline serving works with explicit trust and revocation freshness state;
16. direct cross-component writes are rejected;
17. backup, export, restore, mirror, and federation preserve identity and governance;
18. critical transitions produce classified evidence;
19. every requirement maps to an active test or approved manual control;
20. every active claim has current traceability and evidence;
21. no unresolved authority marker exists;
22. all active prose is in English.

A failed required test blocks the affected artifact, release, activation, query, audience, or conformance claim.

## 11. Non-Normative Examples

### 11.1 Working Exchange to reference

Researchers create a Working Exchange containing claims, sources, uncertainty, and disagreements.

Reviewers validate structure and provenance. A community authority recognizes a scoped subset for a declared audience. The resulting Reference Exchange retains the earlier revision and decision lineage.

Recognition does not claim universal agreement.

### 11.2 SenTient candidate

SenTient proposes that two historical identifiers refer to the same entity.

The candidate preserves sources, alternatives, contradictions, method identity, and uncertainty. Reviewers accept part of the mapping into a new Working Exchange revision.

SenTient does not modify the active Runtime Pack.

### 11.3 Audience-scoped packs

A public pack contains public descriptions and citations.

A community pack contains additional material restricted to authorized community members. The two packs have explicit audience and lineage relationships.

Restricted material is not hidden only through a user-interface flag inside the public pack.

### 11.4 Runtime Pack build

A build selects recognized Reference Exchanges, a query contract, a reader policy, and a target profile.

The builder creates a manifest, inventory, indexes, lineage, rights metadata, compatibility metadata, and test evidence. The immutable candidate is published to the knowledge channel.

It remains inactive until the target node verifies and activates it.

### 11.5 Offline activation

A sovereign node imports a signed offline Kristal bundle.

The importer applies bounded parsing, verifies trust and inventory, checks the known revocation epoch, validates query and profile compatibility, obtains local policy authorization, and activates through kOA Node Agent.

The prior known-good pack remains available until health checks pass.

### 11.6 Query-contract mismatch

A pack is valid and correctly signed but requires a newer query contract than the local runtime supports.

The node stores or reports the candidate as incompatible and continues serving the previous compatible pack.

### 11.7 Revocation while offline

A node has revocation epoch 42 and cannot reach a newer source.

The interface exposes epoch 42 and the freshness condition. Policy can permit restricted continued use or block selected query classes.

The node does not claim current global revocation status.

### 11.8 Corrupted active pack

An integrity check detects corruption in the active pack.

The runtime stops affected queries, preserves evidence, verifies the predecessor, rolls back atomically, rebuilds derived indexes, and records the result.

### 11.9 Reader policy

Two authorized contexts use different reader policies against the same active content.

They can expose different eligible projections and labels. The underlying claim identity, provenance, recognition, supersession, and revocation state remains the same.

### 11.10 Clean restore

A clean environment restores source lineage, recognized references, Runtime Packs, query contracts, status, revocations, and evidence.

It revalidates trust and compatibility, rebuilds indexes, and activates only through the normal governed procedure.

Withdrawn content remains withdrawn after restore.
