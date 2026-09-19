<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-STATUS-000",
  "document_class": "explanatory_markdown",
  "status": "active",
  "authority_participation": "non_authoritative",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "status",
    "maturity",
    "release-readiness"
  ],
  "edit_policy": "manual"
}
KOA:DOC-META:END -->

# Status

This is the living technical-status page for kOA-Linux. Dated assessments remain historical checkpoints; this page records the latest evidence without rewriting those earlier reports.

## Current classification

**Advanced Beta — System Closure & Qualification**

**Evidence basis updated:** 2026-09-19  
**Primary application-runtime target:** Koali + Konnaxion + Orgo  
**Release state:** not pre-RC and not Release Candidate

The living status does not publish one scalar engineering-maturity percentage. Specification/contract completeness, functional implementation, integration, runtime qualification, and release readiness move independently and are reported separately below. Historical percentage estimates remain in their dated reports as historical engineering estimates only.

## Current evidence by dimension

| Dimension | Current status | Evidence / interpretation |
| --- | --- | --- |
| Repository architecture / conformance | **PASS** | `file-architecture`, `path-ownership`, `dependencies`, and `generated-content` all pass with zero findings. Frozen architecture inventory: 1,145 actual / 1,145 expected paths. |
| Profile contract | **PASS** | `sovereign-linux-node` profile contract passes under `DEBUG PRINCIPAL`. |
| Effective profile | **PASS** | Koali Control Panel 4.1.1 generates `generated/profiles/sovereign_linux_node/effective-profile.json`; the corrected diagnostic accepts the generated nested primary-profile identity. |
| First-party component bundles | **PASS** | All eight declared component build targets build successfully through the Control Panel and the `component_bundles` pipeline stage passes. |
| Active subsystem sources | **PASS for current base scope** | Konnaxion and Orgo are the active required application subsystems. Ariane and SemantiK Architect are retained as deferred `excluded / not_installed` stubs and do not block the current base profile. |
| Koali application integration | **Current development focus** | Konnaxion and Orgo both expose `koali.integration.json` manifests with local Web/API processes and readiness probes. The next target is simultaneous Koali-hosted navigation and repeatable E2E qualification. |
| Package resolution | **BLOCKED / not materialized** | No generated `package-resolution.json` exists. |
| Resolved deployment plan | **BLOCKED / not materialized** | `generated/profiles/sovereign_linux_node/resolved-plan.json` is absent. |
| B-0092 / image projection | **BLOCKED** | B-0092 assembly bundle and final image inputs are not yet available. |
| Security/offline/system machine qualification | **Not yet qualified** | Final image/QEMU prerequisites remain unavailable; no machine-level PASS is claimed. |
| Release readiness | **Not qualified** | Complete Release Set, image qualification, recovery evidence, SBOM/provenance/signatures, and compatibility closure remain outstanding. |

## Latest diagnostic snapshot

The latest `DEBUG PRINCIPAL` evidence for `sovereign-linux-node` reports:

```text
Architecture/conformance: ready

file-architecture      PASS
path-ownership         PASS
dependencies           PASS
generated-content      PASS

profile_contract       PASS
effective_profile      PASS
component_bundles      PASS
subsystem_sources      PASS
package_resolution     BLOCKED
resolved_plan          BLOCKED
b0092_and_image        BLOCKED
release_prerequisites  BLOCKED
```

Current blockers:

```text
pipeline_package_resolution_missing
pipeline_resolved_plan_missing
pipeline_b0092_not_renderable
pipeline_image_inputs_missing
pipeline_release_evidence_missing
```

These blockers are downstream system-assembly/release boundaries. They must not be interpreted as failures of the current Konnaxion + Orgo application-development target.

## Current base-system scope

```text
ACTIVE
  Konnaxion
  Orgo

DEFERRED / STUB
  Ariane
  SemantiK Architect
```

The deferred integrations remain in the repository without fabricated authority metadata. Their source locks may remain unresolved while the profile excludes them from the current base composition.

## Current application-development topology

```text
Koali shell
├── Konnaxion Web  127.0.0.1:4301
│   └── API         127.0.0.1:8301
└── Orgo Web        127.0.0.1:4302
    └── API         127.0.0.1:4303
```

The next development milestone is to start both product stacks through their declared Koali integration manifests, admit both applications into Koali, navigate their real interfaces, improve shell/layout/design behavior, and add repeatable browser E2E journeys.

## Koali Control Panel baseline

Current validated development baseline:

**Koali Control Panel 4.1.1**

Supported current workflow:

```text
Refresh Workspace
Generate Effective Profile
Discover Components
Use Git Commit Epoch
Build All Components
DEBUG PRINCIPAL
```

The pipeline is now clean through `subsystem_sources` for the selected base scope.

## What remains before pre-RC

The principal remaining release boundary is still system materialization and machine qualification:

1. implement or expose authoritative package-resolution materialization;
2. implement or expose authority-derived resolved-plan materialization;
3. produce B-0092 and final image inputs;
4. build/select the reproducible system image that will actually be qualified;
5. execute QEMU boot/session and confinement validation against that image;
6. execute declared offline navigation/media scenarios with network disabled;
7. demonstrate recovery, last-known-good, rollback or forward-repair behavior against the qualified artifact;
8. complete SBOM/provenance/signature and Release Set evidence;
9. record a strict validation/release run after these prerequisites exist.

Application-runtime E2E work for Koali + Konnaxion + Orgo can proceed before those final image/release stages are complete.

## Assessment history

- [2026-09-19 — Technical Progress and Runtime Integration Status](./2026-09-19-technical-progress-and-runtime-integration-status.md) — architecture clean; effective profile, component bundles, and selected subsystem sources PASS; Konnaxion + Orgo established as current base; next focus Koali-hosted UX/E2E
- [2026-09-08 — Technical Progress and Maturity Assessment](./2026-09-08-technical-progress-and-maturity-assessment.md) — integrated Koali Spaces ⇄ Konnaxion runtime and browser navigation; historical engineering-maturity estimates
- [2026-09-04 — Technical Progress and Maturity Assessment](./2026-09-04-technical-progress-and-maturity-assessment.md) — first-party component build closure and development-environment automation
- [2026-08-28 — Technical Maturity Assessment](./2026-08-28-technical-maturity-assessment.md) — system closure and qualification
- [2026-08-27 — Technical Maturity Assessment](./2026-08-27-technical-maturity-assessment.md) — integration hardening

A dated assessment is evidence from its date, not a perpetual claim about the current tree.
