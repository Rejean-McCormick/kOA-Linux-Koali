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

**Evidence basis updated:** 2026-09-15  
**Release state:** not pre-RC and not Release Candidate

The living status no longer publishes one scalar engineering-maturity percentage. Specification/contract completeness, functional implementation, integration, runtime qualification, and release readiness move independently and are reported separately below. Historical percentage estimates remain in their dated reports as historical engineering estimates only.

## Current evidence by dimension

| Dimension | Current status | Evidence / interpretation |
| --- | --- | --- |
| Diagnostic environment and repository | **PASS for current checks** | LevelUpDiag `audit-total` N00, N01, and N02 passed under WSL2; the frozen `uv` environment synchronized successfully and the audited worktree was clean. |
| Contracts | **PASS for current checks** | N04 passed; the contract gate reported 19 contract/profile/release binding tests passing. |
| First-party component implementation | **Substantial; alignment correction applied** | N05 ran 682 component/integration tests: 681 passed and one Koali Spaces boundary test failed only because the implemented `unix_transport.py` path was missing from the test allowlist. The alignment overlay adds that path. A fresh post-change run is still required before recording N05 as PASS. |
| Profiles | **PASS for current checks** | N07 passed with 40 profile tests. |
| Documentation conformance | **Alignment correction applied; post-change LevelUpDiag run pending** | N03 exposed deterministic validator drift: the non-authoritative `docs/KOALI_MAJOR_UPDATE_SPEC_2026-09/` was still scanned by canonical/greenfield checks even though generated navigation excluded it, and the generated-Markdown checker rejected the marker format emitted by `build_indexes.py`. The overlay aligns these validator boundaries. |
| Security architecture | **Static/contract checks pass; machine qualification incomplete** | In N08, security architecture, AI-boundary, and component-boundary checks passed. The gate then failed on the same canonical-document ownership drift as N03. QEMU confinement evidence is still unavailable and is not counted as passed. |
| Integration | **Partial / not freshly aggregated by N06** | N06 is intentionally unconfigured in the current LevelUpDiag configuration and therefore skipped. The 2026-09-08 Koali Spaces ⇄ Konnaxion browser-integration result remains a demonstrated historical milestone, not a fresh N06 verdict from the 2026-09-15 audit. |
| Offline qualification | **BLOCKED** | N09 requires a qualified QEMU image and explicit offline navigation/profile inputs. No offline-machine PASS is claimed. |
| System/appliance qualification | **BLOCKED** | N10 requires a QEMU image, expected release identity, compositor readiness, and session readiness evidence. No complete appliance PASS is claimed. |
| Release readiness | **Not qualified** | Reproducible release artifact, complete machine-observed security/offline/system qualification, recovery/rollback evidence, and final Release Set evidence remain prerequisites to pre-RC/RC classification. |

## Latest diagnostic snapshot

The latest full-target diagnostic evidence reviewed for this status is the LevelUpDiag-Koali 2.4.1 `audit-total` run `20260915T145602Z-6818af57` in DEBUG/non-blocking mode. The diagnostic machinery completed successfully (`execution_verdict: PASS`), while testability remained partial because qualification prerequisites were unavailable.

```text
N00  PASS      Diagnostic Integrity
N01  PASS      Environment
N02  PASS      Repository / Structure
N03  FAIL      Documentation              known canonical-source exclusion drift
N04  PASS      Contracts
N05  FAIL      Components                 681 passed / 1 allowlist-drift failure
N06  SKIP      Integrations               command not configured
N07  PASS      Profiles                   40 passed
N08  FAIL      Security Runtime           same canonical-ownership drift before QEMU qualification
N09  BLOCKED   Offline Runtime            QEMU image/profile/navigation inputs unavailable
N10  BLOCKED   System Runtime             QEMU image/release/session inputs unavailable
```

These local FAIL states must not be inflated into missing implementation when the evidence identifies a narrower cause. Conversely, correcting documentation or allowlist drift must not be inflated into QEMU, offline, security-confinement, recovery, or release qualification.

## Alignment corrections represented by the current repository update

The current alignment update addresses documentation/code drift that made implemented layers appear absent:

- Audit Broker README: domain, application, persistence, API, migration, packaging, and tests are documented as present.
- Governance Policy Runtime README and package metadata: policy evaluation, bundle lifecycle, stores, routes, packaging, and tests are documented as present.
- Identity and Trust README/package metadata: domain, use cases, stores/key adapters, API, migrations, and tests are documented as present.
- Resource Governor README/package metadata: domain, admission/application, probes/adapters, API, packaging, and tests are documented as present; durable queue/allocation persistence remains explicitly unclaimed.
- kOA Node Agent README/library description: request validation, broker, fixed backends, socket transport, packaging, and tests are documented as present while production `serve` wiring remains fail-closed.
- kOA Mediatheque README/package metadata: domain, application, stores/queues, API, migration, workers, and tests are documented as present while bootstrap remains observational.
- the non-authoritative `KOALI_MAJOR_UPDATE_SPEC_2026-09` package is excluded consistently from documentation-source scanners until explicit adoption;
- generated-Markdown validation now accepts the `KOA:GENERATED` marker + heading format emitted by `build_indexes.py`;
- the Koali Spaces boundary allowlist includes its implemented Unix transport source.

## Versioning note

Audit Broker and Governance Policy Runtime currently expose different numeric values across implementation/package metadata and contract/interface/payload metadata (`0.1.0` and `1.0.0`). This status does not silently reinterpret or renumber those fields. Their READMEs record the distinction; any convergence requires an explicit versioning decision.

## What remains before pre-RC

The principal remaining boundary is qualification rather than basic component scaffolding:

1. produce/select the reproducible system image that will actually be qualified;
2. execute QEMU boot/session and confinement validation against that image;
3. execute the declared offline navigation/media scenarios with network disabled;
4. demonstrate recovery, last-known-good, rollback or forward-repair behavior against the qualified artifact;
5. complete SBOM/provenance/signature and Release Set evidence;
6. record a strict validation/release run after these prerequisites exist.

## Assessment history

- [2026-09-08 — Technical Progress and Maturity Assessment](./2026-09-08-technical-progress-and-maturity-assessment.md) — integrated Koali Spaces ⇄ Konnaxion runtime and browser navigation; historical engineering-maturity estimates
- [2026-09-04 — Technical Progress and Maturity Assessment](./2026-09-04-technical-progress-and-maturity-assessment.md) — first-party component build closure and development-environment automation
- [2026-08-28 — Technical Maturity Assessment](./2026-08-28-technical-maturity-assessment.md) — system closure and qualification
- [2026-08-27 — Technical Maturity Assessment](./2026-08-27-technical-maturity-assessment.md) — integration hardening

A dated assessment is evidence from its date, not a perpetual claim about the current tree.
