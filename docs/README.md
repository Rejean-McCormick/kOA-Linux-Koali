<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ROOT-README",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "documentation_governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/ai-navigation.contract.json",
    "contracts/system.contract.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "contracts/architecture-patterns.contract.json",
    "02-system/34-architecture-patterns.md",
    "06-lifecycle/20-resilience-and-projection-artifacts.md",
    "08-operations/20-architecture-pattern-operations.md",
    "09-conformance/22-architecture-pattern-conformance.md",
    "contracts/security-controls.contract.json",
    "schemas/security-controls.contract.schema.json",
    "contracts/artifact-contracts/security-evidence.schema.json",
    "07-security/21-security-control-architecture.md",
    "07-security/22-security-control-profile-matrix.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-SPACES-001",
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-PAYLOAD-001",
    "LOCK-BFF-001",
    "LOCK-CQRS-001",
    "LOCK-CACHE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-034",
    "DOC-LIFE-020",
    "DOC-OPS-020",
    "DOC-CONF-022",
    "DOC-SEC-021",
    "DOC-SEC-022",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "documentation",
    "navigation",
    "koa-spaces",
    "experience-layer",
    "architecture-patterns",
    "security-controls",
    "security-evidence",
    "profile-membership"
  ]
}
KOA:DOC-META:END -->

# kOA-Linux Documentation

This corpus documents **kOA-Linux Operating System**: the sovereign local operating system and platform boundary used to run, isolate, govern, update, recover, and operate local kOA workloads.

## Scope

kOA-Linux is **not** the whole kOA Digital Ecosystem.

```text
kOA
└── kOA Digital Ecosystem        system of systems / operable digital ecosystem
    ├── Konnaxion               independent ecosystem system
    ├── Orgo                    independent ecosystem system
    ├── Kristal                 independent ecosystem system
    ├── SemantiK Architect      independent ecosystem system
    ├── other applications / gateways / systems
    └── kOA-Linux Operating System
         ├── native platform components
         ├── deployment profiles
         ├── trust / resources / privilege / lifecycle
         ├── local artifact admission / activation / recovery
         └── host-relative subsystem boundaries for integrated systems
```

The phrase **sociotechnical operating system** can describe the broader kOA Digital Ecosystem when software, governance, people, roles, and institutions are considered together. It is not a second technical operating-system product and is not a synonym for kOA-Linux.

## Authority model

Machine-readable contracts are canonical for the objects they own. Prose explains those contracts. Generated indexes are derived navigation and have no independent authority.

Independently owned ecosystem systems retain authority over their internal behavior when integrated by kOA-Linux. In the kOA-Linux scope they can be called **integrated subsystems**; this is a host-relative deployment classification, not an ownership transfer.

Native kOA-Linux components own only their declared platform state. A shared host, process supervisor, database server, container runtime, network, or filesystem does not transfer domain authority.

## Core local responsibilities

kOA-Linux owns or mediates the platform concerns declared by its contracts, including:

- deployment-profile composition;
- component and subsystem process lifecycle;
- identity and trust boundaries;
- resource governance;
- privilege mediation;
- network and storage exposure;
- artifact admission and verification;
- local activation and rollback where the artifact contract assigns them to the platform;
- safe degradation;
- offline continuity;
- backup, restore, portability, and recovery;
- selective audit/evidence paths;
- optional experience composition through kOA Spaces.

It does not redefine Konnaxion, Orgo, Kristal, or SemantiK Architect internals.

## Important boundaries

### Kristal

Kristal is one ecosystem system. Its Specification and implementation belong to the same Kristal system. kOA-Linux does not redefine Kristal schemas or epistemic semantics. The local `kristal_runtime` component owns only the kOA-Linux runtime boundary for verified Kristal artifacts and Runtime Packs.

### SemantiK Architect

SemantiK Architect is one planner-centered NLG ecosystem system. kOA-Linux governs its local deployment boundary, resources, artifact admission, health, storage/network exposure, and safe degradation. Architect itself owns request normalization, planning, `PlannedSentence`, `ConstructionPlan`, lexical resolution, renderer selection/backends, `SurfaceResult`, and its public generation contract. GF/PGF is a supported backend/tooling family, not the architecture itself.

### Konnaxion and Orgo

Konnaxion and Orgo are independent ecosystem systems. kOA-Linux integrates them through subsystem contracts and official documentation mounts. It does not duplicate their internal model, workflow, API, or UI documentation.

### kOA Spaces

kOA Spaces is optional and replaceable. It composes validated interface contributions but owns no business authority, workflow authority, host privilege, resource admission, release activation, backup, or recovery.

## Where to start

- `contracts/system.contract.json` — global kOA-Linux system contract.
- `contracts/terminology.contract.json` — canonical vocabulary.
- `01-constitution/13-glossary.md` — human-readable taxonomy.
- `02-system/00-system-overview.md` — system model and boundaries.
- `02-system/05-data-authority-and-ownership.md` — logical authority.
- `02-system/07-cross-component-communication.md` — commands, queries, events, artifacts, receipts and gateways.
- `04-components/` — native component boundaries.
- `04-components/subsystems/` — host-side boundaries for independently owned integrated systems.
- `03-profiles/` — deployment profiles and overlays.
- `06-lifecycle/` — artifact/release/activation/recovery lifecycle.
- `07-security/` — trust, security, privacy and privilege boundaries.
- `08-operations/` — operating behavior.
- `09-conformance/` — conformance model and validators.
- `CODE_ALIGNMENT_NOTES.md` — implementation/contract areas that still need alignment.

The documentation validators remain the executable consistency check for this corpus.

## Product UI architecture

The canonical UI rule is product autonomy plus optional composition. Product interfaces own their standalone entry points and business-facing route implementations. Shared Koali UI contracts and shell primitives provide reusable layout, navigation, command, context, inspector, responsive, and accessibility behavior. kOA Spaces may compose admitted product manifests when selected, but it is not the mandatory runtime of product UIs.

## Vérification des dépôts satellites

- [Contrats, versions et limites de qualification (27 octobre 2026)](Integration-Verification-2026-10-27.md)
