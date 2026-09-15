<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ROOT-CODE-ALIGNMENT",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": ["global"],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/terminology.contract.json",
    "contracts/subsystems/konnaxion.subsystem.json",
    "contracts/subsystems/orgo.subsystem.json",
    "contracts/subsystems/semantik-architect.subsystem.json",
    "contracts/components/kristal-runtime.component.json",
    "contracts/artifact-contracts/language-pack.schema.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": ["DOC-SYS-000", "DOC-CONST-013", "DOC-SYS-013", "DOC-LIFE-009"],
  "tags": ["alignment", "implementation", "contracts", "subsystems", "language", "kristal"]
}
KOA:DOC-META:END -->

# kOA-Linux — Code and Contract Alignment Notes

## Purpose

This is one technical alignment note. It identifies implementation/contracts that should converge with the current kOA-Linux architecture. The supplied package is documentation/contracts rather than a complete kOA-Linux application source snapshot, so implementation-path observations are contract-driven unless the file exists in this corpus.

## 1. Treat integrated ecosystem systems as subsystems, not native components

Konnaxion, Orgo and SemantiK Architect have active subsystem contracts and official documentation mounts. Runtime/deployment code should resolve those subsystem identities rather than assuming they are native kOA-Linux component owners.

Host responsibilities include process lifecycle, resources, trust exposure, storage/network exposure, artifact admission, health, backup coordination and degradation. Internal domain/workflow/API semantics remain with the subsystem.

## 2. Keep subsystem references out of the native component catalog

The generated component catalog is built from `contracts/components/*.component.json` and represents native kOA-Linux component contracts. Konnaxion, Orgo, SemantiK Architect, Ariane and SenTient instead have `contracts/subsystems/*.subsystem.json` boundaries.

Implementation/configuration must not recreate synthetic references such as `generated/component-catalog.json#/components/konnaxion` or `.../semantik_architect_runtime` when no corresponding native component contract exists. Use the subsystem contract or a specifically defined host-local native component contract.

## 3. Keep SemantiK Architect planner-first and backend-flexible

The current Architect documentation defines the runtime around:

```text
normalization → planner → PlannedSentence → ConstructionPlan
→ lexical resolution → renderer backend → SurfaceResult
```

GF/PGF is one backend/tooling family. kOA-Linux code should not implement a separate GF-first architecture or make PGF mandatory for every Architect deployment.

The updated `language-pack.schema.json` permits a declared generic backend asset set while retaining explicit PGF assets for GF-backed packs. Implementers should align pack builders, validators and activation code with the declared backend rather than hard-coding `gf_wordbench` / `compiled_pgf_required` as universal truth.

## 4. Align language-pack discriminator and artifact class

The previous language-pack schema used `artifact_class = language_runtime_pack` while the artifact-class registry and example used `language_pack`. The updated contract uses `language_pack`.

Any pack builder, verifier, fixture, release validator, database enum or activation service still using `language_runtime_pack` as the kOA artifact-class discriminator should be updated or given an explicit compatibility mapping at the boundary.

## 5. Preserve Kristal system vs local Kristal Runtime distinction

`kristal_runtime` is a native kOA-Linux component. **Kristal is the broader epistemic ecosystem system.**

Code around Runtime Pack handling should keep these layers separate:

```text
Kristal Specification / implementation
    owns artifact semantics

kOA-Linux artifact boundary
    verifies/adopts a candidate locally

kristal_runtime
    owns local verification/compatibility/active-pack/rollback/runtime state
```

Do not put Orgo workflow, Konnaxion domain state, policy authorization, resource scheduling or host privilege inside `kristal_runtime`.

## 6. Preserve scoped Runtime Pack discriminators

Kristal uses its own manifest discriminator (`artifact_type = runtime_pack_manifest`) while kOA-Linux can classify the platform artifact as `artifact_class = runtime_pack`. Code should treat these as different scoped fields rather than forcing one global enum.

## 7. kOA Spaces `module` means interface contribution, not architecture ownership

Any implementation that reads `module_interface_manifest` or renders the module selector should treat `module` as a presentation contribution identity. It must not infer:

- native component ownership;
- business authorization;
- workflow ownership;
- host privilege;
- resource admission;
- release activation authority.

## 8. Mount official subsystem documentation without copying it

The validator currently reports absent reserved mounts for independently owned subsystems. The final development/release workspace should mount/link the official docs for Konnaxion, Orgo, SemantiK Architect, Ariane, SenTient and kOA Spaces at the reserved `docs/subsystems/*` paths.

Do not copy internal subsystem documentation into kOA-Linux and then evolve it independently.

## 9. Keep host authorization, resource admission and business authority separate

Implementation paths that activate artifacts or perform host-sensitive work should preserve the current separation:

```text
identity/trust result
≠ policy authorization
≠ resource grant
≠ privileged host operation
≠ component/domain mutation
```

A successful resource admission does not authorize activation. A policy decision does not perform the activation. A receipt does not replace the active-state record.

## 10. Keep offline behavior fail-closed

Offline/degraded code should continue from already admitted local state where the active profile permits it. It should not:

- bypass trust;
- invent a substitute subsystem;
- fetch network content as a hidden side effect;
- invoke external AI silently;
- activate an unverified candidate;
- transfer domain authority to a platform fallback.

## 11. Re-run the documentation/contracts validators with implementation changes

The documentation corpus already provides `docs/tools/validate_docs.py` and generated catalogs. Contract-affecting implementation changes should stay consistent with those machine-readable sources and their conformance checks.

## 12. Keep Koali product UIs standalone and composable

Product user interfaces should support independent product lifecycle and integrated Koali composition. Generic shell behavior belongs in shared Koali UI primitives or a compatible reusable library; it should not be obtained by importing another product's private UI implementation.

A product such as Orgo or Konnaxion can expose a standalone application entry point and also publish declarative surfaces, routes, navigation, commands, inspectors, and capability metadata for an admitted composition host such as kOA Spaces. Installed-product selection should be registry-driven so removing one product does not require source changes to unrelated product interfaces.

For Orgo, the full Control Panel can act as the reference maximal surface while reduced surfaces reuse the same product capabilities and pages rather than becoming independent frontends.

## 13. Keep component package documentation synchronized with implemented layers

A component README must distinguish the narrow behavior of bootstrap/diagnostic entry points from the implementation state of the complete package. It must not describe domain, application, port, adapter, API, migration, worker, broker, or test layers as future work when those layers are present in the repository.

The 2026-09-15 alignment pass corrects this drift for Audit Broker, Governance Policy Runtime, Identity and Trust, Resource Governor, kOA Node Agent, and kOA Mediatheque. Remaining limitations must be expressed narrowly: for example, missing durable Resource Governor queue persistence or unqualified Node Agent production wiring, rather than relabeling the whole component as bootstrap-only.

## 14. Keep proposed architecture packages outside canonical authority until adoption

`docs/KOALI_MAJOR_UPDATE_SPEC_2026-09/` explicitly declares itself a standalone proposed target and says the existing repository documentation/contracts remain authoritative until adoption. Canonical documentation scanners must therefore exclude that package until an explicit adoption/change-control step assigns canonical metadata and authority.

Generated navigation already follows this rule; shared source enumeration must use the same boundary.

## 15. Do not infer one version lifecycle from unrelated version fields

Package/runtime, component-contract, interface, and packaging-payload version fields may currently differ. Tooling and documentation must report the concrete field and namespace being evaluated rather than presenting one number as a universal component maturity or release version. Where Audit Broker or Governance Policy Runtime expose both `0.1.0` and `1.0.0`, convergence requires an explicit versioning decision rather than a documentation-only renumbering.

## 16. Keep generated-content validators aligned with their generators

Generated-content checks must validate the format actually emitted by the canonical generator. `build_indexes.py` prefixes generated Markdown with a `KOA:GENERATED` comment and then emits the document heading; `check_generated_blocks.py` must accept that exact marker-plus-heading structure rather than requiring the heading to be byte zero.

A validator/generator disagreement is documentation-tooling drift, not evidence that the generated catalog content is semantically invalid.

