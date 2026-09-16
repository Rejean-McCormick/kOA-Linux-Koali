<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-009",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "artifact_class:pgf_artifact",
    "artifact_class:language_pack",
    "release_channel:knowledge"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/global_capabilities",
    "contracts/system.contract.json#/global_boundaries",
    "generated/component-catalog.json",
    "contracts/subsystems/semantik-architect.subsystem.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/artifact-contracts/language-pack.schema.json",
    "contracts/artifact-contracts/runtime-pack.schema.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-PROFILE-001",
    "DEC-AI-001",
    "DEC-DATA-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-LANG-001",
    "REQ-LIFE-LANG-002",
    "REQ-LIFE-LANG-003",
    "REQ-LIFE-LANG-004",
    "REQ-LIFE-LANG-005",
    "REQ-LIFE-LANG-006",
    "REQ-LIFE-LANG-007",
    "REQ-LIFE-LANG-008",
    "REQ-LIFE-LANG-009",
    "REQ-LIFE-LANG-010",
    "REQ-LIFE-LANG-011",
    "REQ-LIFE-LANG-012",
    "REQ-LIFE-LANG-013",
    "REQ-LIFE-LANG-014",
    "REQ-LIFE-LANG-015",
    "REQ-LIFE-LANG-016",
    "REQ-LIFE-LANG-017",
    "REQ-LIFE-LANG-018",
    "REQ-LIFE-LANG-019",
    "REQ-LIFE-LANG-020",
    "REQ-LIFE-LANG-021",
    "REQ-LIFE-LANG-022",
    "REQ-LIFE-LANG-023",
    "REQ-LIFE-LANG-024",
    "REQ-LIFE-LANG-025",
    "REQ-LIFE-LANG-026",
    "REQ-LIFE-LANG-027",
    "REQ-LIFE-LANG-028",
    "REQ-LIFE-LANG-029",
    "REQ-LIFE-LANG-030",
    "REQ-LIFE-LANG-031",
    "REQ-LIFE-LANG-032",
    "REQ-LIFE-LANG-033",
    "REQ-LIFE-LANG-034",
    "REQ-LIFE-LANG-035",
    "REQ-LIFE-LANG-036",
    "REQ-LIFE-LANG-037",
    "REQ-LIFE-LANG-038",
    "REQ-LIFE-LANG-039",
    "REQ-LIFE-LANG-040"
  ],
  "lock_ids": [
    "LOCK-COMP-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-002",
    "DOC-DEV-016",
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-018"
  ],
  "tags": [
    "lifecycle",
    "language-artifacts",
    "pgf",
    "language-runtime-pack",
    "gf-wordbench",
    "semantik-architect-runtime",
    "knowledge-channel",
    "deterministic-language-runtime",
    "atomic-activation",
    "rollback",
    "offline"
  ]
}
KOA:DOC-META:END -->

# Language Artifacts

## 1. Purpose

This document defines the **kOA-Linux lifecycle** for SemantiK Architect runtime-language assets. It governs artifact identity, release-channel placement, admission, compatibility, local activation when applicable, recovery, offline transfer, and evidence.

It does not define SemantiK Architect's internal planner/renderer architecture.

```text
SemantiK Architect source/build workflow
→ validated language/runtime assets
→ language-pack candidate
→ knowledge-channel publication
→ kOA-Linux transfer/quarantine
→ verification + compatibility
→ local admission/staging
→ atomic activation when applicable
→ runtime use
→ rollback / forward repair / supersession
```

## 2. Artifact scope

A language pack can include one or more declared runtime asset families:

- GF/PGF assets;
- family-renderer resources;
- safe-mode resources;
- lexicon/runtime data;
- message/template resources used by the active Architect version;
- companion configuration/manifests;
- validation and compatibility evidence.

No backend family is universal unless the active SemantiK Architect profile explicitly makes it so.

## 3. Ownership

### SemantiK Architect

Owns the meaning of language/runtime assets, planner/renderer compatibility, language/construction capability, build/test semantics, and the runtime API that consumes those assets.

### kOA-Linux

Owns the local artifact lifecycle assigned by the active platform contracts: release-channel handling, transfer/quarantine, integrity/trust checks, profile compatibility, local storage, activation state when applicable, recovery, retention, backup/restore coordination, and evidence.

## 4. Artifact identity and manifest

A release-grade language pack identifies at least:

- artifact identity and version;
- language/locale scope;
- SemantiK Architect consumer/runtime compatibility;
- declared backend/resource assets;
- source/build provenance;
- integrity records;
- validation results;
- profile compatibility;
- release-channel membership;
- activation/recovery requirements;
- retention and traceability information.

A GF-backed pack additionally identifies the GF/PGF-specific assets/toolchain it uses.

The canonical kOA-Linux artifact-class discriminator is `language_pack`. The historical `language_runtime_pack` value is a historical compatibility alias only; new manifests, examples, validators, release records, and activation records MUST emit `language_pack`. A compatibility reader may accept the historical value only through an explicit boundary mapping and must normalize it before canonical validation or persistence.

## 5. Build and publication

Language asset construction occurs inside the owning SemantiK Architect development/build workflow. kOA-Linux does not define one universal compiler. GF tooling can be used for a GF-backed profile; other backends can use their declared build/resource process.

Publication creates a published artifact in the `knowledge` channel. Publication never activates a runtime by itself.

## 6. Admission and compatibility

Before a local candidate becomes activation-eligible, the platform validates the applicable combination of:

- artifact schema;
- artifact identity and digest;
- provenance/signatures/trust when required;
- SemantiK Architect contract/runtime version;
- declared backend assets;
- required companion artifacts;
- target profile and platform envelope;
- release-channel and Release Set constraints;
- downgrade/substitution/revocation policy.

Unknown compatibility fails closed where the contract requires an explicit compatibility decision.

## 7. Activation

When the artifact class/profile uses local activation, the sequence is atomic:

```text
installed/staged candidate
→ isolated load/health checks
→ preserve previous valid state
→ atomic active-state switch
→ post-activation readiness
→ receipt/evidence
```

A partially copied, partially verified, partially loaded, or rejected candidate never becomes active.

## 8. Runtime and caches

Runtime use is governed by SemantiK Architect. kOA-Linux can enforce the process/resource/security envelope.

Caches remain derived and rebuildable. A cached rendering, generated text, or local temporary resource does not replace the active declared artifact as authority.

## 9. Offline and backup

Offline bundles preserve the same identities, provenance, compatibility, trust, and activation requirements as connected transfer.

Backup/restore preserves the records needed to reconstruct a valid local runtime state without requiring the build toolchain on the target node.

## 10. Recovery

If activation or runtime initialization fails, the platform restores the previous compatible state where valid or follows an explicit forward-repair path. A failed candidate remains rejected/quarantined according to policy.

## 11. Applicable normative requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-LANG-001,REQ-LIFE-LANG-002,REQ-LIFE-LANG-003,REQ-LIFE-LANG-004,REQ-LIFE-LANG-005,REQ-LIFE-LANG-006,REQ-LIFE-LANG-007,REQ-LIFE-LANG-008,REQ-LIFE-LANG-009,REQ-LIFE-LANG-010,REQ-LIFE-LANG-011,REQ-LIFE-LANG-012,REQ-LIFE-LANG-013,REQ-LIFE-LANG-014,REQ-LIFE-LANG-015,REQ-LIFE-LANG-016,REQ-LIFE-LANG-017,REQ-LIFE-LANG-018,REQ-LIFE-LANG-019,REQ-LIFE-LANG-020,REQ-LIFE-LANG-021,REQ-LIFE-LANG-022,REQ-LIFE-LANG-023,REQ-LIFE-LANG-024,REQ-LIFE-LANG-025,REQ-LIFE-LANG-026,REQ-LIFE-LANG-027,REQ-LIFE-LANG-028,REQ-LIFE-LANG-029,REQ-LIFE-LANG-030,REQ-LIFE-LANG-031,REQ-LIFE-LANG-032,REQ-LIFE-LANG-033,REQ-LIFE-LANG-034,REQ-LIFE-LANG-035,REQ-LIFE-LANG-036,REQ-LIFE-LANG-037,REQ-LIFE-LANG-038,REQ-LIFE-LANG-039,REQ-LIFE-LANG-040 -->
- **REQ-LIFE-LANG-001 — SHALL:** SemantiK Architect shall remain the owner of language-generation architecture and runtime asset semantics.
- **REQ-LIFE-LANG-002 — SHALL:** kOA-Linux shall own only the local artifact/release/admission/activation responsibilities assigned by its contracts.
- **REQ-LIFE-LANG-003 — SHALL NOT:** kOA-Linux shall not require one renderer backend or compiler for every SemantiK Architect language pack.
- **REQ-LIFE-LANG-004 — SHALL:** Every language-pack build shall identify the SemantiK Architect version/profile and target language or locale scope.
- **REQ-LIFE-LANG-005 — SHALL:** Every release-grade build shall identify its declared source, toolchain/resource inputs, dependencies, environment, and validation fixtures applicable to that backend profile.
- **REQ-LIFE-LANG-006 — SHALL NOT:** Undeclared local files, mutable shared workspace state, editor state, or machine-specific paths shall influence a published language pack when the selected build profile claims reproducibility.
- **REQ-LIFE-LANG-007 — SHALL:** Every published runtime asset and package manifest shall have stable declared artifact identity and integrity records.
- **REQ-LIFE-LANG-008 — SHALL:** A language pack shall bind its declared backend/runtime assets, manifest, compatibility declaration, provenance, validation results, and required runtime metadata.
- **REQ-LIFE-LANG-009 — SHALL:** Language-pack provenance shall identify source/build inputs and the tooling or resource process used to produce the declared assets.
- **REQ-LIFE-LANG-010 — SHALL:** Language candidates shall pass the structural, compatibility, deterministic-runtime, regression, packaging, load, activation, and recovery validation applicable to their declared backend profile.
- **REQ-LIFE-LANG-011 — SHALL:** Validation shall identify the exact language/locale, candidate package, Architect/runtime contract, backend assets, target profiles, tests, and terminal results.
- **REQ-LIFE-LANG-012 — SHALL NOT:** A skipped, blocked, unavailable, or incomplete required test shall be represented as passing.
- **REQ-LIFE-LANG-013 — SHALL:** Published language artifacts shall satisfy the determinism/reproducibility guarantees declared by the active SemantiK Architect contract and backend profile.
- **REQ-LIFE-LANG-014 — SHALL NOT:** External AI output shall directly define, validate, publish, activate, or mutate authoritative language artifacts without the owning workflow explicitly accepting it.
- **REQ-LIFE-LANG-015 — SHALL:** Externally assisted language material shall remain candidate source until reviewed and adopted through the owning SemantiK Architect workflow.
- **REQ-LIFE-LANG-016 — SHALL:** Language packs shall be published through the `knowledge` release channel.
- **REQ-LIFE-LANG-017 — SHALL:** A published language artifact shall retain independent identity, version, provenance, compatibility, and integrity/signature evidence according to its contract.
- **REQ-LIFE-LANG-018 — SHALL NOT:** Publication of a language artifact shall activate it in a runtime implicitly.
- **REQ-LIFE-LANG-019 — SHALL:** A Release Set shall identify the exact language/runtime assets compatible with the selected SemantiK Architect deployment and target profiles.
- **REQ-LIFE-LANG-020 — SHALL:** Independent knowledge-channel updates shall preserve declared compatibility with active system, services, governance, runtime, and profile versions.
- **REQ-LIFE-LANG-021 — SHALL:** A runtime activation boundary shall stage a complete verified candidate before changing active state.
- **REQ-LIFE-LANG-022 — SHALL:** Language-artifact activation shall be atomic and preserve a valid predecessor or explicit forward-repair path.
- **REQ-LIFE-LANG-023 — SHALL NOT:** A partially copied, verified, indexed, loaded, or activated language pack shall become active.
- **REQ-LIFE-LANG-024 — SHALL:** The runtime boundary shall load only assets admitted and selected for the effective deployment/profile.
- **REQ-LIFE-LANG-025 — SHALL:** Multiple installed language packs shall retain separate identities, compatibility, activation, rollback, and evidence state.
- **REQ-LIFE-LANG-026 — SHALL:** Derived language caches shall remain rebuildable and subordinate to active published artifacts.
- **REQ-LIFE-LANG-027 — SHALL NOT:** A cache, rendered message, local patch, or build-workspace output shall replace the active published artifact as authority.
- **REQ-LIFE-LANG-028 — SHALL:** A failed activation shall retain or restore the previous compatible language state when valid.
- **REQ-LIFE-LANG-029 — SHALL:** A language change that prevents safe rollback shall define and test forward-repair behavior before publication.
- **REQ-LIFE-LANG-030 — SHALL:** Language-artifact backup and offline bundles shall preserve identity, provenance, compatibility, integrity/signature evidence, and Release Set relationships.
- **REQ-LIFE-LANG-031 — SHALL:** Offline installation and activation shall perform the same required artifact, compatibility, validation, and atomicity checks as connected installation.
- **REQ-LIFE-LANG-032 — SHALL:** A language artifact shall declare supported Architect/runtime contracts, language/locale scope, required companion assets, backend identity, and incompatible states.
- **REQ-LIFE-LANG-033 — SHOULD:** Backend-specific assets such as GF/PGF should remain explicitly identified rather than being treated as universal fields when the pack can support multiple backend families.
- **REQ-LIFE-LANG-034 — SHALL:** Retirement or replacement shall identify affected profiles/consumers, replacement artifacts where applicable, and removal conditions.
- **REQ-LIFE-LANG-035 — SHALL NOT:** A retired language-artifact identity or version identifier shall be reused.
- **REQ-LIFE-LANG-036 — SHALL:** Language source, candidates, published artifacts, active packs, previous packs, evidence, and derived caches shall use distinct retention and authority classifications.
- **REQ-LIFE-LANG-037 — SHALL:** Runtime consumers shall pass structured inputs through the active SemantiK Architect contract and remain responsible for the meaning/authority of those inputs.
- **REQ-LIFE-LANG-038 — SHALL NOT:** SemantiK Architect or its host runtime boundary shall acquire ownership of Orgo, Konnaxion, Kristal, Ariane, or another system's source data by generating language output.
- **REQ-LIFE-LANG-039 — SHALL:** Build, publication, admission, activation, rollback, replacement, and recovery events shall produce the evidence required by applicable artifact/profile/release contracts.
- **REQ-LIFE-LANG-040 — SHALL:** A semantic change to language-artifact ownership, packaging, compatibility, release placement, activation, rollback, or runtime consumption shall update the canonical contract and its dependent conformance surfaces.
<!-- GENERATED:REQUIREMENTS:END -->

## 12. Cross-system boundaries

Konnaxion, Orgo, Kristal, Ariane, and other callers retain authority over their source facts/state. SemantiK Architect owns language planning/realization; kOA-Linux owns only the platform lifecycle assigned to the deployed subsystem and its admitted artifacts.

## 13. Non-normative examples

> A GF-backed French pack can contain a PGF artifact and GF provenance. A family-renderer pack can contain a different backend asset set. Both are valid only when their declared SemantiK Architect compatibility passes.

> A node can restore an already published language pack and run Architect without installing the development/build toolchain that produced the pack.
