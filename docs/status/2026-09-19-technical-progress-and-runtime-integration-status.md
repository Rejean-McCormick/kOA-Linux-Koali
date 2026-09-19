<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-STATUS-005",
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
  "depends_on": [
    "DOC-STATUS-000",
    "DOC-STATUS-001",
    "DOC-STATUS-002",
    "DOC-STATUS-003",
    "DOC-STATUS-004"
  ],
  "tags": [
    "status",
    "technical-progress",
    "runtime-integration",
    "control-panel",
    "konnaxion",
    "orgo",
    "component-build-closure",
    "subsystem-source-closure",
    "e2e",
    "qualification"
  ],
  "edit_policy": "manual"
}
KOA:DOC-META:END -->

# Koali Technical Progress and Runtime Integration Status

**Assessment date:** 2026-09-19  
**Current status:** Advanced Beta — System Closure & Qualification  
**Primary application-runtime target:** Koali + Konnaxion + Orgo  
**Release state:** not pre-RC and not Release Candidate

> This document records the current demonstrated engineering state. It does not convert blocked system-image or release-qualification stages into passes, and it does not claim that deferred subsystems are complete.

## Executive summary

The 2026-09-19 work closed a major authority and build-pipeline boundary for the current sovereign Linux development profile.

The repository is now formally clean under the active architecture checks, all eight first-party component bundles build successfully through Koali Control Panel 4.1.1, the effective profile resolves correctly, and the subsystem-source stage passes for the intentionally selected base system.

The active application-runtime scope is now deliberately narrowed to:

```text
Koali shell / hosting surface
        ↓
Konnaxion
        ↓
Orgo
```

Ariane and SemantiK Architect remain present in the repository as deferred integration stubs but are excluded from the current `sovereign-linux-node` composition. Their unresolved source locks therefore no longer block the base-system pipeline.

The next engineering focus is no longer basic component or subsystem-source closure. It is application runtime integration and product experience:

```text
start Konnaxion + Orgo
        ↓
expose both through Koali
        ↓
navigate real application surfaces
        ↓
improve shell / layout / visual design
        ↓
exercise Konnaxion ↔ Orgo user journeys
        ↓
add repeatable end-to-end browser qualification
```

The system-release path remains separately blocked at package-resolution materialization, resolved deployment-plan materialization, B-0092/image projection, and final release evidence.

## Current formal diagnostic state

The latest `DEBUG PRINCIPAL` run for `sovereign-linux-node` reports:

```text
Architecture/conformance: ready

PASS  file-architecture
PASS  path-ownership
PASS  dependencies
PASS  generated-content
```

The frozen architecture inventory now contains 1,145 expected paths and the current repository reports 1,145 actual paths.

Pipeline stages currently report:

```text
profile_contract       PASS
effective_profile      PASS
component_bundles      PASS
subsystem_sources      PASS
package_resolution     BLOCKED
resolved_plan          BLOCKED
b0092_and_image        BLOCKED
release_prerequisites  BLOCKED
```

The remaining blockers are:

```text
pipeline_package_resolution_missing
pipeline_resolved_plan_missing
pipeline_b0092_not_renderable
pipeline_image_inputs_missing
pipeline_release_evidence_missing
```

These are downstream system-assembly and release-qualification blockers. They are not evidence that Konnaxion or Orgo application runtimes are unavailable for development integration.

## Repository and conformance closure

### Architecture inventory

The file-architecture and path-ownership registries are aligned with the committed repository.

A new committed root-level `.smartignore` file is now treated as an official repository file rather than an undeclared local artifact. Its presence no longer produces root-entry, frozen-inventory, or ownership findings.

Current result:

```text
file-architecture  PASS — 0 errors / 0 warnings
path-ownership     PASS — 0 errors / 0 warnings
dependencies       PASS — 0 errors / 0 warnings
generated-content  PASS — 0 errors / 0 warnings
```

### Effective-profile diagnostic correction

The effective-profile diagnostic now validates the generated nested primary-profile identity correctly. The earlier false stale-profile condition is closed.

Current effective-profile generation through Koali Control Panel:

```text
Generate Effective Profile: sovereign-linux-node
PASS: resolved sovereign_linux_node
      -> generated/profiles/sovereign_linux_node/effective-profile.json
```

## Component build closure

Koali Control Panel 4.1.1 successfully prepares the frozen all-groups Python environment and builds all eight declared component targets from the WSL workspace:

```text
audit-broker                 PASS
governance-policy-runtime    PASS
identity-and-trust           PASS
koa-mediatheque              PASS
koa-node-agent               PASS
kristal-runtime              PASS
publication-gateway          PASS
resource-governor            PASS

component_bundles            PASS
```

The supported workflow is now:

```text
Refresh Workspace
Generate Effective Profile
Discover Components
Use Git Commit Epoch
Prepare Component Build Environment
Build All Components
DEBUG PRINCIPAL
```

The build preparation step verifies and installs the frozen development environment, including the required packaging toolchain used by strict component builds.

## Subsystem-source scope and closure

### Active base subsystems

For the current base system, the required active independent application subsystems are:

```text
Konnaxion  ACTIVE
Orgo       ACTIVE
```

Their source authorities are pinned to immutable repository revisions and verified source/license digests in their kOA integration locks.

### Deferred subsystems

The following integrations remain in the tree for future work but are not part of the current sovereign base composition:

```text
Ariane              EXCLUDED / not_installed
SemantiK Architect  EXCLUDED / not_installed
```

Their unresolved source locks are intentionally retained rather than populated with fabricated authority metadata.

This allows the current profile to express the real product scope instead of forcing unfinished or unnecessary subsystems into the base system.

Current diagnostic result:

```text
subsystem_sources  PASS
```

## Koali Control Panel baseline

The current development baseline is:

**Koali Control Panel 4.1.1**

The validated 4.1.1 workflow includes:

- final-profile-aware `DEBUG PRINCIPAL` diagnostics;
- effective-profile generation for `sovereign-linux-node`;
- cleanup of transient untracked assembly `uv.lock` state when appropriate;
- frozen all-groups component build-environment preparation;
- strict offline component-bundle builds after environment preparation;
- full eight-component build orchestration;
- read-only pipeline diagnostics that distinguish formal conformance from functional readiness blockers.

## Konnaxion Koali runtime contract

Konnaxion exposes a Koali integration manifest with the following local development topology:

```text
Konnaxion Web  127.0.0.1:4301
Konnaxion API  127.0.0.1:8301
```

The manifest declares:

- API startup through `koali/start-api.ps1`;
- frontend startup through Next.js under `frontend`;
- API readiness at `/health/ready/`;
- Web readiness at `/`;
- Koali embedded surface base at `http://127.0.0.1:4301`.

The frontend receives explicit local API origins for the Koali-hosted development session.

## Orgo Koali runtime contract

Orgo exposes a Koali integration manifest with the following local development topology:

```text
Orgo Web  127.0.0.1:4302
Orgo API  127.0.0.1:4303
```

The manifest declares:

- API-stack startup through Docker Compose;
- local PostgreSQL development credentials supplied through environment variables;
- `ORGO_LOCAL_AUTO_LOGIN=true` for the local Koali development flow;
- Next.js Web startup under `apps/web`;
- API readiness at `/health/ready`;
- Web readiness at `/`;
- Koali embedded surface base at `http://127.0.0.1:4302`.

## Immediate product-development objective

The next milestone is a working Koali-hosted development environment for both active applications, not a final bootable Linux appliance.

The target development topology is:

```text
Koali
├── Home / shell
├── Konnaxion  -> 127.0.0.1:4301
└── Orgo       -> 127.0.0.1:4302

Konnaxion API  -> 127.0.0.1:8301
Orgo API       -> 127.0.0.1:4303
```

The next qualification work should establish:

1. repeatable startup and readiness of Konnaxion API + Web;
2. repeatable startup and readiness of Orgo API + Web;
3. admission of both applications into the Koali shell;
4. correct product-switcher and hosted-route navigation;
5. layout, spacing, responsive-shell, visual hierarchy, and design-system improvements based on actual hosted pages;
6. cross-application navigation or workflow handoff where product contracts require it;
7. browser-level E2E journeys with deterministic setup and teardown;
8. regression coverage for shell navigation, authentication/development-session behavior, readiness failures, and application restart behavior.

## E2E qualification target

The initial E2E campaign should prove at least the following development-runtime path:

```text
Koali shell ready
    ↓
open Konnaxion
    ↓
Konnaxion Web ready
    ↓
exercise one representative Konnaxion workflow
    ↓
return to Koali shell
    ↓
open Orgo
    ↓
Orgo Web ready
    ↓
exercise one representative Orgo workflow
    ↓
verify navigation state and application health
```

This browser evidence should be kept separate from final QEMU/appliance qualification. A successful local Koali E2E run demonstrates integrated application behavior; it does not prove boot, offline, confinement, recovery, image reproducibility, or Release Set closure.

## Remaining system-release path

After the application-runtime and E2E milestone, the unresolved system pipeline remains:

```text
materialized package-resolution.json
        ↓
authority-derived resolved-plan.json
        ↓
B-0092 assembly bundle
        ↓
system image inputs / image projection
        ↓
reproducible image candidate
        ↓
QEMU boot/session qualification
        ↓
security / confinement / offline qualification
        ↓
recovery / rollback / last-known-good evidence
        ↓
SBOM / provenance / compatibility / signatures
        ↓
complete Release Set
```

The current source snapshot does not expose a supported public command that already materializes `package-resolution.json` or the authority-derived `resolved-plan.json`. Those stages therefore remain a separate pipeline-implementation task and should not be bypassed by hand-authored generated artifacts.

## Current interpretation

The project has crossed four important boundaries that were previously open:

- repository architecture is formally clean;
- effective-profile generation is stable and correctly diagnosed;
- all eight native component bundles build successfully;
- the selected active subsystem-source set is fully resolved.

The most productive next step is therefore to use the now-stable base to improve the actual Koali-hosted product experience for Konnaxion + Orgo and create repeatable browser E2E coverage before returning to final image materialization and machine qualification.

## Relationship to earlier checkpoints

This assessment supersedes earlier current-state descriptions but does not rewrite their historical evidence:

- 2026-09-08 demonstrated Koali ⇄ Konnaxion browser integration under the earlier development stack;
- 2026-09-04 recorded eight-component build closure;
- the 2026-09-19 state adds repository-conformance closure, corrected final-profile diagnostics, active subsystem-source closure for Konnaxion + Orgo, and an explicit narrowed base-system scope with Ariane and SemantiK Architect deferred.

The next dated status should be recorded after the Konnaxion + Orgo Koali-hosted E2E milestone or after package-resolution/resolved-plan materialization becomes available, whichever closes first.
