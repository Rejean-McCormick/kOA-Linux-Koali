<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-IDT-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "component:identity_and_trust"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/authority_model",
    "contracts/system.contract.json#/receipts_and_critical_transitions",
    "generated/component-catalog.json#/components/identity_and_trust",
    "contracts/components/identity-and-trust.component.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-CONST-002",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-COMP-IDT-001",
    "REQ-COMP-IDT-002",
    "REQ-COMP-IDT-003",
    "REQ-COMP-IDT-004",
    "REQ-COMP-IDT-005",
    "REQ-COMP-IDT-006",
    "REQ-COMP-IDT-007",
    "REQ-COMP-IDT-008",
    "REQ-COMP-IDT-009",
    "REQ-COMP-IDT-010",
    "REQ-COMP-IDT-011",
    "REQ-COMP-IDT-012",
    "REQ-COMP-IDT-013",
    "REQ-COMP-IDT-014",
    "REQ-COMP-IDT-015",
    "REQ-COMP-IDT-016",
    "REQ-COMP-IDT-017",
    "REQ-COMP-IDT-018",
    "REQ-COMP-IDT-019",
    "REQ-COMP-IDT-020",
    "REQ-COMP-IDT-021",
    "REQ-COMP-IDT-022",
    "REQ-COMP-IDT-023",
    "REQ-COMP-IDT-024"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-COMP-003"
  ],
  "tags": [
    "component",
    "identity",
    "trust",
    "authentication",
    "credentials",
    "certificates",
    "signatures",
    "trust-roots",
    "revocation",
    "offline-trust",
    "receipts",
    "selective-disclosure"
  ]
}
KOA:DOC-META:END -->

# Identity and Trust

## 1. Purpose

This document explains the `identity_and_trust` component.

Identity and Trust establishes who or what is presenting evidence and whether a credential, certificate, signature, key, package, attestation, or trust update is valid for an exact declared use context.

The component provides identity and trust evidence. It does not provide general business authorization.

The distinction is fundamental:

`text
identity evidence
 → identity result
trust evidence
 → trust result
requested action
 → authorization by the owning component or policy authority
`

A valid human identity does not automatically authorize publication, privileged host mutation, data access, governance action, or release activation. A valid artifact signature does not automatically make the artifact compatible or authorized for activation. A valid service credential does not grant access to every component.

The component supports connected, restricted-connectivity, offline, maintenance, recovery, and break-glass contexts while preserving fail-closed authority, selective disclosure, component ownership, and lifecycle recovery.

## 2. Scope

This document applies to component behavior involving:

- human and recovery-operator authentication;
- service, component-instance, node, device, and workspace authentication;
- tenant and organization identity;
- external-integration identity;
- artifact-signer identity;
- credential issuance, validation, suspension, expiration, revocation, and retirement;
- certificate and key lifecycle;
- trust-root registration, scoping, activation, revocation, supersession, and retirement;
- signature and attestation verification;
- revocation-state resolution;
- key rotation;
- signed offline trust and revocation updates;
- protected identity and trust backup and restore;
- identity and trust receipts;
- selective identity and evidence views;
- health, readiness, degradation, and recovery.

The component does not own:

- application business authorization;
- governance policy decisions;
- publication decisions;
- resource scheduling or admission;
- host privilege decisions;
- release compatibility;
- component business data;
- external identity-provider source records;
- the Audit Broker's receipt store;
- general application secret storage.

Profile contracts determine deployment membership, assurance level, storage topology, hardware-backed key requirements, offline freshness limits, factor policy, and operational capacity.

## 3. Canonical References

The canonical sources for this document are:

`text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/authority_model
contracts/system.contract.json#/receipts_and_critical_transitions
generated/component-catalog.json#/components/identity_and_trust
contracts/components/identity-and-trust.component.json
generated/profile-catalog.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/integration-types.contract.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/evidence-catalog.json
generated/exception-index.json
`

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `identity-and-trust.component.json` | Observable component responsibilities, data, interfaces, states, failures, profiles, lifecycle, and conformance |
| `components.registry.json` | Component identity and system boundary |
| `system.registry.json#/authority_model` | Global distinction among identity, trust, and authorization |
| `system.registry.json#/receipts_and_critical_transitions` | Receipt classes and critical-transition behavior |
| `profiles/index.json` and profile contracts | Profile membership, assurance, offline, storage, and capacity requirements |
| `release-channels.registry.json` | Release-channel identities used in trust scopes |
| `artifact-classes.registry.json` | Artifact classes used in trust and verification scopes |
| `integrations.registry.json` | External integration identity and transfer boundaries |
| `requirements.registry.json` | Normative requirement text and validation ownership |
| `locks.registry.json` | Data, lifecycle, profile, identifier, and decision-closure invariants |
| `traceability.registry.json` | Requirement, lock, profile, test, evidence, and component relationships |
| `evidence.registry.json` | Registered verification and conformance evidence |
| `exceptions.registry.json` | Bounded deviations that cannot create missing identity, trust, or authorization |

This document explains the component contract and does not redefine its arrays, states, interface fields, profile behavior, or conformance facts.

## 4. Model and Responsibilities

### 4.1 Result model

The component produces two principal result classes.

| Result class | Positive result | Negative result | Inconclusive result |
| --- | --- | --- | --- |
| Identity | `established` | `not_established` | `indeterminate` |
| Trust | `trusted` | `untrusted` | `indeterminate` |

The result states preserve diagnostic meaning. Protected use proceeds only when the required result is positive and a separate authorization path approves the requested action.

### 4.2 Identity classes

The component supports these subject classes:

`text
human
service
component_instance
node
device
workspace
tenant
organization
external_integration
artifact_signer
recovery_operator
`

An active identity record contains a stable identifier, subject class, owner, tenant, environment, lifecycle state, credential references, timestamps, and evidence references.

Identity lifecycle states are:

`text
pending
active
suspended
revoked
expired
retired
`

Display names remain descriptive attributes. They are not canonical identity.

### 4.3 Authentication factors

Supported factor classes include:

- knowledge factors;
- possession factors;
- inherence factors;
- service credentials;
- device credentials;
- recovery credentials.

The active profile and authentication policy determine factor combinations and assurance. The component reports the achieved context without converting factor success into action authority.

### 4.4 Credential model

Credential classes include:

`text
password_verifier
public_key
x509_certificate
ssh_certificate
service_token
device_credential
recovery_code
attestation_credential
`

Credential lifecycle states are:

`text
pending
active
suspended
revoked
expired
retired
`

Credential validation examines the complete declared context rather than the credential object alone. The context includes subject binding, issuer, tenant, environment, intended use, time, scope, revocation, assurance, algorithm, and supported version.

### 4.5 Trust-root scoping

Trust roots are exact-scope objects.

The scope can contain:

`text
tenant
environment
release_channel
artifact_class
integration
component
purpose
`

A root trusted for a governance policy bundle in one environment does not automatically validate a service artifact, knowledge package, external integration, another tenant, or another environment.

Trust-root states are:

`text
staged
active
suspended
revoked
superseded
retired
`

### 4.6 Signature and attestation verification

Verification resolves:

- the presented chain, key, or attestation;
- the declared identity;
- the intended use;
- the exact trust context;
- the signer or subject identity;
- the algorithm and version;
- object binding;
- time validity;
- revocation state;
- the resulting reason code;
- evidence references.

Verification establishes integrity and trusted provenance under a scope. Compatibility and authorization remain separate decisions.

### 4.7 Revocation

Revocation can target:

- identities;
- credentials;
- certificates;
- keys;
- trust roots;
- issuers;
- nodes;
- services;
- artifact signers.

Revocation blocks new protected use. Pending operations are reevaluated. Historical committed records remain preserved. Cached results are invalidated within the bounds defined by the active profile and credential class.

### 4.8 Rotation

Rotation uses a successor lifecycle:

`text
create successor
verify owner and scope
stage successor
update consumers
activate successor
use explicit overlap where required
retire or revoke predecessor
record receipts
`

Implicit permanent overlap is not a rotation strategy.

### 4.9 Protected material

Private keys and credential secrets use protected material references rather than ordinary inline data.

Ordinary interfaces, receipts, logs, exports, and diagnostics exclude:

- private keys;
- password material;
- recovery secrets;
- token secrets;
- authentication factor values;
- unrestricted personal data;
- protected evidence payloads.

Hardware-backed storage and protected backup depend on the active profile.

### 4.10 Data ownership

Identity and Trust owns its identity, credential lifecycle, certificate lifecycle, trust-root, trust-scope, revocation, trust-update, verification-result, attestation-result, receipt, and protected-key lifecycle records.

Other components use declared commands, queries, events, and verification references. They do not write the component's source tables.

Identity and Trust does not write business authorization results or another component's source data.

### 4.11 Observable interfaces

The contract defines eight command interfaces:

| Command | Purpose |
| --- | --- |
| `authenticate_subject` | Establish a human or recovery-operator identity |
| `authenticate_service` | Establish a service, component, node, or device identity |
| `validate_credential` | Validate credential binding, scope, time, proof, and revocation |
| `verify_signature` | Verify a signed artifact, bundle, policy, release, receipt, or update |
| `issue_credential` | Issue or register a bounded credential where profile-authorized |
| `register_trust_root` | Stage or activate an exactly scoped trust root |
| `revoke_trust_object` | Revoke an identity, credential, certificate, key, issuer, signer, or root |
| `apply_offline_trust_update` | Verify and atomically apply a signed offline trust update |

The contract also defines three query interfaces:

| Query | Purpose |
| --- | --- |
| `resolve_identity` | Return an authorized public identity view |
| `resolve_trust_context` | Return active roots and revocation state for an exact use context |
| `get_component_status` | Return health, readiness, trust freshness, rotation, and offline-update status |

Each view uses selective disclosure.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-IDT-001,REQ-COMP-IDT-002,REQ-COMP-IDT-003,REQ-COMP-IDT-004,REQ-COMP-IDT-005,REQ-COMP-IDT-006,REQ-COMP-IDT-007,REQ-COMP-IDT-008,REQ-COMP-IDT-009,REQ-COMP-IDT-010,REQ-COMP-IDT-011,REQ-COMP-IDT-012,REQ-COMP-IDT-013,REQ-COMP-IDT-014,REQ-COMP-IDT-015,REQ-COMP-IDT-016,REQ-COMP-IDT-017,REQ-COMP-IDT-018,REQ-COMP-IDT-019,REQ-COMP-IDT-020,REQ-COMP-IDT-021,REQ-COMP-IDT-022,REQ-COMP-IDT-023,REQ-COMP-IDT-024 -->
- **REQ-COMP-IDT-001 — SHALL:** The component establish human, service, component-instance, node, device, workspace, tenant, organization, integration, signer, and recovery-operator identities only from validated evidence applicable to the requested context.
- **REQ-COMP-IDT-002 — SHALL NOT:** A successful authentication or trust verification be treated as application, governance, publication, resource, privilege, release, or host-mutation authorization.
- **REQ-COMP-IDT-003 — SHALL:** Identity and trust evaluations return explicit established, rejected, or indeterminate results with stable reason codes.
- **REQ-COMP-IDT-004 — SHALL:** An indeterminate identity or trust result fail closed for the protected use while preserving independently valid capabilities.
- **REQ-COMP-IDT-005 — SHALL:** Identity identifiers remain stable and immutable after activation, and retired identifiers remain permanently reserved.
- **REQ-COMP-IDT-006 — SHALL NOT:** Display names, network locations, physical possession, operating-system privilege, or previous successful use substitute for a stable identity.
- **REQ-COMP-IDT-007 — SHALL:** Every credential record declare its subject, type, issuer, scope, validity interval, state, protected material reference, and revocation reference.
- **REQ-COMP-IDT-008 — SHALL:** Credential validation cover structure, version, issuer, subject binding, time validity, scope, proof, revocation, assurance, and intended use.
- **REQ-COMP-IDT-009 — SHALL NOT:** Expired, revoked, unsupported, malformed, out-of-scope, or ambiguously bound credentials be accepted.
- **REQ-COMP-IDT-010 — SHALL:** Private keys and secret credential material remain outside ordinary logs, receipts, diagnostics, exports, and unrestricted component interfaces.
- **REQ-COMP-IDT-011 — SHALL:** Trust roots be scoped by the applicable tenant, environment, release channel, artifact class, integration, component, and purpose.
- **REQ-COMP-IDT-012 — SHALL NOT:** A trust root expand implicitly across tenants, environments, release channels, artifact classes, integrations, components, or purposes.
- **REQ-COMP-IDT-013 — SHALL:** Signature and attestation verification bind the presented proof to the resolved signer identity, exact trust root, intended use, object identity, algorithm, version, verification time, and revocation context.
- **REQ-COMP-IDT-014 — SHALL:** Revocation prevent new protected use, invalidate affected cached results within declared bounds, and force pending operations to be reevaluated before effect.
- **REQ-COMP-IDT-015 — SHALL:** Credential, key, certificate, issuer, signer, and trust-root rotation use staged successor activation, explicit overlap, predecessor retirement or revocation, and transition receipts.
- **REQ-COMP-IDT-016 — SHALL:** Profiles claiming sovereign offline behavior support signed, versioned, monotonic, scoped, time-bounded, rollback-protected trust and revocation update packages.
- **REQ-COMP-IDT-017 — SHALL NOT:** Missing, invalid, stale, or rollback-vulnerable offline trust material broaden or renew trust.
- **REQ-COMP-IDT-018 — SHALL:** The component own its identity, credential lifecycle, trust-root, revocation, verification, and protected key lifecycle records under a separate storage identity.
- **REQ-COMP-IDT-019 — SHALL NOT:** Another component write directly to identity-and-trust source tables, or Identity and Trust write directly to another component's authoritative source tables.
- **REQ-COMP-IDT-020 — SHALL:** Identity and trust commands expose bounded requests and responses, explicit intended use, selective disclosure, idempotency behavior, and correlation context.
- **REQ-COMP-IDT-021 — SHALL:** Identity activation, credential issuance and revocation, trust-root activation and revocation, key rotation, offline trust updates, protected key restoration, and trust-store restoration produce machine-readable receipts.
- **REQ-COMP-IDT-022 — SHALL:** Access to restricted identity, trust, key, or evidence views require explicit authority and produce an accountable access record where the active policy requires it.
- **REQ-COMP-IDT-023 — SHALL:** Backup, restore, migration, activation, rollback, and forward repair preserve identity, trust scope, revocation state, protected material handling, references, and receipt evidence.
- **REQ-COMP-IDT-024 — SHALL:** Profile-specific assurance, storage, hardware-key, offline, rotation, and evidence requirements remain explicit and cannot be generalized into the global component contract.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Subject authentication

Subject authentication follows this sequence:

1. receive the subject hint, context, factors, tenant, environment, and profile;
2. resolve the applicable identity record and authentication policy;
3. validate factor structure and provenance;
4. evaluate the factor set;
5. evaluate identity lifecycle state;
6. produce `established`, `not_established`, or `indeterminate`;
7. expose the achieved assurance context and expiration;
8. record the result according to the active risk and receipt policy;
9. return identity evidence to the requesting authority owner.

No application action is authorized during this procedure.

### 6.2 Service and node authentication

Service authentication:

1. receives the presented credential and expected subject class;
2. validates issuer, subject binding, intended use, tenant, environment, scope, time, and revocation;
3. resolves the stable service, component-instance, node, or device identity;
4. returns the validated scope and expiration;
5. leaves action authorization to the caller or Governance Policy Runtime.

### 6.3 Credential issuance

Credential issuance:

1. resolves the active issuer and issuance authority;
2. validates the subject identity;
3. validates credential class, scope, validity, and assurance;
4. creates or references protected key material;
5. stages the credential;
6. verifies the resulting record and proof;
7. activates the credential atomically;
8. records the issuance receipt;
9. exposes only the permitted credential representation.

### 6.4 Trust-root activation

Trust-root activation:

1. receives the public material reference, type, owner, validity, scope, authority, and evidence;
2. validates every scope dimension;
3. checks for conflicting active ownership;
4. stages the root;
5. tests verification for the intended use;
6. activates the root atomically;
7. records the transition receipt;
8. notifies consumers of the new exact trust context.

Failure leaves the previous valid trust context active.

### 6.5 Verification

Signature or attestation verification:

1. receives the signed object reference, proof, intended use, and scope context;
2. resolves the active trust context;
3. validates structure, algorithm, version, signer, chain, object binding, validity, and revocation;
4. returns `trusted`, `untrusted`, or `indeterminate`;
5. records the verification reference and reason code;
6. leaves activation, publication, acceptance, or execution to the owning workflow.

### 6.6 Revocation

Revocation:

1. identifies the target and revocation authority;
2. validates target type, scope, reason, and effective time;
3. records the revocation state atomically;
4. blocks new protected use;
5. invalidates affected caches within declared bounds;
6. notifies dependent consumers;
7. records the transition receipt;
8. initiates replacement or recovery when required.

### 6.7 Rotation

Key or credential rotation:

1. creates successor material;
2. verifies successor owner and scope;
3. stages the successor;
4. updates declared consumers;
5. activates the successor;
6. maintains only the authorized overlap interval;
7. retires or revokes the predecessor;
8. verifies dependent services;
9. records completion evidence.

### 6.8 Offline trust update

A signed offline trust or revocation update:

1. resolves the expected profile and trust scope;
2. verifies package identity, issuer, signature, integrity, version, sequence, validity, and rollback protection;
3. rejects sequence rollback or scope expansion;
4. stages the changes;
5. evaluates effects on active credentials, roots, and issuers;
6. applies the update atomically;
7. preserves the previous valid state for recovery;
8. records the application receipt;
9. reconciles with connected authority after connectivity returns.

### 6.9 Backup and restore

Protected backup includes identity metadata, trust roots, scope bindings, revocation state, required verification evidence, and protected key material through an approved path.

Restore:

1. isolates the recovery scope;
2. verifies the recovery source;
3. restores metadata and protected material;
4. verifies references, scope, sequence, validity, and revocation;
5. activates the restored state atomically;
6. records recovery receipts;
7. preserves rollback or forward repair.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `identity_not_established` | Presented identity evidence fails validation | Authentication is denied | Public or anonymous capability only when separately declared |
| `identity_result_indeterminate` | Required evidence or verifier is unavailable | Authentication is denied | Independently valid existing sessions follow their own lifecycle |
| `credential_expired` | Credential validity has ended | Credential use is denied | Renewal or recovery flow |
| `credential_revoked` | Credential is revoked | Credential use is denied | Replacement credential flow |
| `trust_scope_mismatch` | Root scope does not match the exact use context | Trust is denied | Resolve the correct trust context |
| `trust_root_unavailable` | No active root exists for the exact context | Protected verification is denied | Current valid state remains unchanged |
| `revocation_state_stale` | Revocation freshness exceeds the profile bound | Affected use follows fail-closed policy | Separately authorized read-only or recovery behavior |
| `signature_invalid` | Signature, chain, signer, digest, or intended-use binding fails | Object or update is rejected | Current valid artifact or trust state remains active |
| `algorithm_or_version_unsupported` | Credential, proof, attestation, or schema version is unsupported | Verification is denied | Compatibility or migration workflow |
| `private_key_provider_unavailable` | Protected signing or decryption material is unavailable | Issuance, signing, or protected restore is unavailable | Verification and public identity reads can continue where valid |
| `offline_trust_update_invalid` | Signature, sequence, scope, validity, or rollback protection fails | Update remains inactive | Previous valid trust state remains active |
| `identity_store_restore_partial` | Restore cannot complete atomically | Partial state remains inactive | Rollback or declared forward repair |
| `receipt_path_unavailable` | A critical transition has no approved receipt path | The critical transition is blocked | Non-critical verification can continue where permitted |
| `cross_component_identity_write_attempt` | Another component attempts a direct source-table write | Write is denied | Use a declared command, event, or registration interface |

Degradation remains capability-scoped. Loss of online enrollment does not automatically disable valid local signature verification. Loss of protected signing does not automatically disable public identity resolution. Stale revocation state never becomes fresh by assumption.

## 8. Cross-Component Interactions

### 8.1 Governance Policy Runtime

Identity and Trust supplies validated actor, service, node, credential, signer, and trust evidence.

Governance Policy Runtime evaluates governance authorization, disclosure, consent, privilege, and governed exceptions. Identity and Trust does not issue those decisions.

### 8.2 Resource Governor

Resource Governor controls CPU, memory, I/O, queues, scheduling, and process limits.

Identity or trust success does not reserve resources. Resource availability does not authorize identity issuance, root activation, or protected use.

### 8.3 Audit Broker

Identity and Trust produces its identity, trust, verification, and lifecycle receipts.

Audit Broker validates, stores, indexes, discloses, and exports receipts without owning the underlying identity, credential, root, or revocation state.

### 8.4 Lifecycle and release services

Lifecycle services request signature, signer, package, and trust verification before activation.

A trusted signature proves the declared trust relationship. Lifecycle services separately evaluate artifact class, release channel, compatibility, activation, rollback, and repair.

### 8.5 Component owners

Application and system components authenticate callers and services through declared interfaces. Each component remains responsible for authorization over its own actions and data.

### 8.6 Privileged broker

A privileged broker uses established operator or service identity and explicit policy authority.

Operating-system privilege does not replace identity evidence or governance authorization, and Identity and Trust does not directly execute host mutation.

### 8.7 External identity providers

An external identity provider is an integration source. Identity and Trust validates the integration result, maps it to a local stable identity under declared rules, and preserves provenance.

The external provider does not become the owner of local authorization or component data.

### 8.8 Offline bundles

Offline bundles can contain signed trust and revocation updates.

Identity and Trust verifies exact scope, version, sequence, validity, issuer, signature, and rollback protection before atomic activation.

### 8.9 Development workspaces

Development profiles use workspace-scoped identities, credentials, services, data, and secrets.

Development identities remain separate from production identities and trust roots. A workspace credential does not become a production credential by reuse.

## 9. Decision Closure and Prohibited Assumptions

This document closes the component interpretation as follows:

- identity and authorization are separate;
- trust verification and compatibility are separate;
- identity and trust results include explicit indeterminate states;
- protected uses fail closed when required identity or trust is indeterminate;
- stable identifiers survive display-name changes;
- trust roots are exact-scope objects;
- revocation affects new and pending use without erasing history;
- rotation uses staged successors and bounded overlap;
- offline updates are signed, monotonic, scoped, and rollback-protected;
- protected material remains outside ordinary interfaces;
- Identity and Trust owns its source records;
- Audit Broker stores receipts without owning identity state;
- profile-specific assurance remains profile-specific.

The following assumptions are prohibited:

- authentication implies authorization;
- root or administrator privilege proves application authority;
- a display name is a stable identity;
- network location proves identity;
- physical possession proves authority;
- a trust root applies globally because it validated one object;
- a service credential can be reused for another tenant or environment;
- a valid signature proves release compatibility;
- an expired credential remains usable during an outage;
- unknown revocation state means not revoked;
- offline operation permits trust expansion;
- external identity-provider success grants local business authority;
- a receipt can expose secrets for diagnostic convenience;
- another component can update identity records directly;
- restored partial state can become active;
- a profile-specific hardware or storage choice is a global component mandate.

A new identity class, credential class, trust-scope dimension, result state, interface, root type, revocation semantic, or protected-material behavior requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 24 requirement identifiers are unique and match the component contract;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. the component contract owns all observable interface and lifecycle values displayed here;
7. identity tests cover positive, negative, and indeterminate outcomes;
8. trust tests cover positive, negative, and indeterminate outcomes;
9. tests prove that authentication does not create business or host authority;
10. credential tests cover structure, version, issuer, subject, time, scope, proof, revocation, assurance, and intended use;
11. trust-root tests cover tenant, environment, channel, artifact class, integration, component, and purpose scope;
12. tests reject implicit root fallback and cross-scope reuse;
13. revocation tests block new use and reevaluate pending operations;
14. rotation tests prove staged successor activation and predecessor retirement;
15. private-material tests prove exclusion from ordinary logs, receipts, diagnostics, and exports;
16. interface tests cover all eight commands and three queries;
17. selective-disclosure tests restrict identity, trust, key, and evidence views;
18. cross-component tests reject direct source-table writes;
19. offline tests cover signatures, monotonic sequences, scope, validity, rollback protection, and no trust expansion;
20. lifecycle tests cover activation, upgrade, backup, restore, rollback, forward repair, and retirement;
21. receipt tests cover all critical identity and trust transitions;
22. profile tests preserve explicit assurance, storage, offline, hardware-key, rotation, and evidence behavior;
23. unsupported versions and algorithms fail explicitly;
24. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
25. active prose is English;
26. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

`text
identity_not_established
identity_result_indeterminate
credential_expired
credential_revoked
trust_scope_mismatch
trust_root_unavailable
revocation_state_stale
signature_invalid
algorithm_or_version_unsupported
private_key_provider_unavailable
offline_trust_update_invalid
identity_store_restore_partial
receipt_path_unavailable
cross_component_identity_write_attempt
authentication_authorization_boundary_violation
trust_root_scope_undefined
private_material_disclosure_detected
component_conformance_evidence_incomplete
`

## 11. Non-Normative Examples

### 11.1 Valid user, denied action

A user successfully authenticates. The requesting component then denies a publication action because no disclosure authority covers the target audience. The authentication remains valid, but no publication occurs.

### 11.2 Signed artifact with incompatible release

Identity and Trust verifies an artifact signature under the correct service-channel root. Lifecycle validation then rejects activation because the artifact is incompatible with the active Release Set. Signature validity is preserved without claiming compatibility.

### 11.3 Revoked service credential

A service presents a structurally valid credential that appears on the current revocation state. Authentication is denied, pending operations are reevaluated, and the service enters its declared degraded state.

### 11.4 Offline revocation package

A sovereign node receives a signed revocation update through an offline bundle. Identity and Trust verifies the issuer, signature, scope, sequence, validity, and rollback protection before activating it atomically.

### 11.5 Protected signing unavailable

A hardware-backed key provider becomes unavailable. New credential issuance and signing stop. Existing public-key verification and authorized public identity queries continue while the component reports the signing capability as degraded.


## Common OIDC federation profile

`koa-common-oidc-v1` maps an externally verified OIDC subject to a local Identity and Trust identity without transferring application authorization. The federation key is the exact `issuer + subject (sub)` pair. Email, username and display name are descriptive attributes and MUST NOT be used for silent linking.

The local binding stores provider identity, issuer, subject, local identity reference, tenant/environment scope, creation time and evidence references. It does not store the external IdP source record or owner-application roles.

When the IdP is unavailable, external-provider authentication may degrade or be denied according to profile/offline state; local identity and local authentication capabilities remain separately evaluated.
