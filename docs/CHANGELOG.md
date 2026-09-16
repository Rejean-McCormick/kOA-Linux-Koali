<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ROOT-CHANGELOG-001",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "00-governance/00-documentation-architecture.md",
    "00-governance/01-authority.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "02-system/24-koa-spaces-design-system.md",
    "03-profiles/14-koa-spaces-deployment.md",
    "10-adrs/ADR-033-koa-spaces-as-optional-replaceable-experience-subsystem.md"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-SYS-035",
    "DOC-PROFILE-014",
    "ADR-033"
  ],
  "tags": [
    "changelog",
    "documentation-release",
    "koa-spaces",
    "experience-layer",
    "profile-membership"
  ]
}
KOA:DOC-META:END -->

# Documentation Changelog

## 1.4.0 — 2026-09-16

Aligned kOA-Linux documentation with the current ecosystem boundary model without changing existing machine-readable authority contracts:

- clarified that Kristal Runtime owns local Runtime Pack verification/compatibility/active-pack/rollback state while kOA Node Agent performs only the declared narrow privileged host transition;
- distinguished Space activation, service activation, Runtime Pack activation, and Release Set activation as separately owned transitions;
- documented Interaction Kernel as an adoptable system-of-systems protocol only when a change-controlled integration contract explicitly registers the Profile/mapping;
- strengthened final subsystem-documentation alignment to require official mounted/linked docs rather than independently evolved copies;
- made `language_pack` the explicit canonical discriminator and documented `language_runtime_pack` as a historical compatibility alias only;
- updated the kOA Spaces activation recipe to prevent confusion with service, knowledge, governance, or Release Set activation.


## 1.3.0 — 2026-09-08

Clarified modular Koali product-interface architecture before Orgo frontend expansion:

- defined standalone and integrated rendering modes for independently packaged product UIs;
- made kOA Spaces an optional integrated composition host rather than a mandatory runtime for product interfaces;
- established shared Koali shell primitives as a reusable presentation library/contract, not a business application;
- separated product selection from product-owned surface profiles;
- added declarative navigation, commands, contextual inspectors, and surface composition to the integrated UI model;
- required registry-driven product discovery so individual products can be removed without source edits to unrelated interfaces;
- documented Orgo's full Control Panel as its reference maximal surface, with reduced surfaces as projections of the same capabilities and pages;
- preserved Konnaxion standalone UI ownership while allowing the same shell grammar in integrated mode.

## 1.2.0 — 2026-09-05

Closed the kOA Spaces interface-definition gap before frontend implementation:

- defined explicit Koali/Konnaxion alignment without duplicating Konnaxion business functions or authority;
- clarified that browser-rendered or web-technology interfaces can be locally installed and operate without public Internet connectivity;
- expanded module-selector, sidebar, top-bar, PageShell, interface-state, route-surface, responsive, and offline composition behavior;
- added the kOA Spaces design-system document and the reference Next.js/React/TypeScript/Ant Design/pnpm frontend recipe;
- added interface-theme and local interface-asset schemas;
- strengthened Space, module, and route schemas with design-system, local-asset, shell-compatibility, and surface metadata;
- aligned ADR-004 terminology so web technology no longer implies Internet dependency;
- strengthened ADR-033 and the kOA Spaces subsystem boundary around local-first rendering and non-duplication.

## 1.1.0 — 2026-08-06

Integrated kOA Spaces across the complete documentation surface:

- clarified kOA Spaces as the optional, replaceable, non-authoritative experience layer in the root and documentation README files;
- added explicit profile membership to eight primary-profile and overlay contracts;
- connected constitutional, system, lifecycle, operations, conformance, recipe, and example documents to the canonical subsystem boundary;
- activated the profile membership matrix in `03-profiles/14-koa-spaces-deployment.md`;
- added ADR-033 to preserve separation between presentation and business or privileged authority;
- rebuilt generated indexes and AI context packages and completed the full validator pipeline.

## 1.0.0 — 2026-08-03

Finalized the governance foundation:

- activated all governance documents;
- added `01-authority.md`;
- established explicit governance-bootstrap authority;
- removed competing frozen architecture copies from the active package;
- assigned collision-free requirement namespaces;
- normalized the AI entry point and mandatory section structure;
- finalized all authoring templates as active templates;
- removed ordinary Markdown fingerprint fields and fingerprint-based validation;
- replaced open-decision acronym markers with explicit final policy language;
- added simplified structural validation criteria.
