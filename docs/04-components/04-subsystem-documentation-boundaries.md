<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-SUBSYSTEM-BOUNDARIES",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "components",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/terminology.contract.json",
    "contracts/ai-navigation.contract.json",
    "schemas/subsystem.schema.json",
    "contracts/subsystems/koa-spaces.subsystem.json"
  ],
  "decision_ids": [
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "subsystems",
    "documentation-boundary",
    "external-platforms",
    "uckk",
    "mediatheque",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# Subsystem Documentation Boundaries

## 1. Purpose

This document separates kOA-Linux operating boundaries from the authoritative internal documentation of independently owned kOA ecosystem systems. It also distinguishes those systems from external platforms.

## 2. Scope

The subsystem documentation-mount model applies to Ariane, Konnaxion, Orgo, SenTient, SemantiK Architect, and the optional kOA Spaces experience subsystem.

UCKK is excluded from this model. UCKK is an external Moodle platform, not a native kOA-Linux subsystem. It has its own authority, storage, lifecycle, identity, access control, operations, and Mediatheque.

The kOA Mediatheque is an internal kOA-Linux component and is documented through the component-contract model rather than through a subsystem mount.

## 3. Canonical References

Subsystem boundary contracts are under `contracts/subsystems/`. Their pinned official documentation can be exposed under `subsystems/` at the reserved paths declared by `contracts/ai-navigation.contract.json`.

External-platform interactions are declared under `contracts/integrations/`. Publication from the kOA Mediatheque to UCKK is governed by the UCKK publication integration; it is not represented by `contracts/subsystems/uckk.subsystem.json` or `subsystems/uckk/`.

## 4. Model and Responsibilities

kOA-Linux owns installation, activation, runtime dependencies, identity and authorization boundaries, data exchange, resources, health, offline availability, degradation, update compatibility, and backup or recovery boundaries.

Each mounted subsystem owns its internal domain model and product behavior. kOA Spaces owns only its presentation implementation and validated **Space activation** state; contributing modules continue to own their pages, actions, authorization, workflows, and business data. Space activation is a presentation/configuration transition and MUST NOT be confused with service activation, Kristal Runtime Pack activation, or Release Set activation.

The kOA Mediatheque owns local kOA media records and storage state. The UCKK Mediatheque owns its separate Moodle-side records and storage state. A compatible Mediatheque frame does not create shared authority or shared storage.

## 5. Applicable Normative Requirements

Executable assertions are carried by source contracts and validators rather than duplicated here.

## 6. Procedures or State Transitions

A subsystem documentation link can be installed later at its reserved path without changing the kOA-Linux boundary model. For a **final aligned development/release workspace**, the official documentation MUST be mounted or linked at the reserved path and validated with the mounted-alignment control; copying the subsystem documentation into kOA-Linux and then evolving the copy independently is not an acceptable final alignment mechanism.

The mount is documentary authority only. It does not transfer runtime, business, release, or activation ownership to kOA-Linux.

Publishing to UCKK follows a separate controlled transition: explicit selection, disclosure authorization, rights and restriction checks, Moodle destination selection, package and manifest production, authenticated transfer, result handling, and publication receipt preservation.

Controlled import from UCKK, when supported, is a separate explicitly authorized operation. It is not implicit bidirectional synchronization.

## 7. Failure States and Safe Degradation

An absent subsystem documentation mount does not block preparation unless final alignment is explicitly requested.

Unavailable UCKK connectivity affects only UCKK publication or import. Local kOA Mediatheque operation remains available. Eligible outbound publication may be held in a bounded, visible, idempotent queue.

## 8. Cross-Component and External Interactions

Interactions use declared contracts. Direct writes to another subsystem's or external platform's authoritative database are prohibited.

The Publication Gateway owns disclosure authorization. The UCKK Publication Bridge owns Moodle-specific packaging, transport, result handling, and receipts. Neither component transfers local source authority to UCKK.

## 9. Unknowns and Prohibited Assumptions

Missing internal subsystem details are resolved in the owning subsystem documentation, not recreated in kOA-Linux.

The following assumptions are prohibited:

- kOA Spaces is part of the privileged core;
- a visible module, route, menu item, public alias, or top-bar widget grants authority;
- a Space definition transfers ownership of a contributing system or its data;
- replacing or disabling kOA Spaces permits deletion or reinterpretation of business state;

- UCKK is installed as a kOA-Linux subsystem;
- UCKK is required by any kOA-Linux runtime profile;
- UCKK owns local kOA media, rights, provenance, backup, or restore state;
- the kOA Mediatheque and UCKK Mediatheque share one authoritative database;
- a compatible Mediatheque frame creates shared ownership;
- publication implies background bidirectional synchronization.

## 10. Validation Criteria

Validation confirms:

- the six reserved subsystem identities and mount paths;
- absence of an active UCKK subsystem contract or mount;
- unique subsystem identities;
- resolved boundary pages;
- absence of duplicated internal subsystem catalogs;
- kOA Mediatheque classification as an internal component;
- UCKK classification as an external Moodle platform;
- publication through a declared integration rather than direct database access;
- kOA Spaces classification as optional, replaceable, offline-capable, and non-authoritative;
- presentation contributions remain bound to the owning module authorization path.

## 11. Non-Normative Examples

A kOA-Linux page can state that Ariane receives navigation input; Ariane documentation owns the detailed interaction model.

A user can select an item from the kOA Mediatheque and publish it to a UCKK course through an authorized bridge. The local record remains authoritative in kOA-Linux, while UCKK owns the separately published Moodle-side record.

## Koali product UI modularity

This document is interpreted with the Koali product-interface portability rule:

- each independently packaged product owns its user interface and remains independently operable when its declared standalone mode is supported;
- shared Koali shell and design-system code is reusable presentation infrastructure, not a mandatory product runtime and not a source of business authority;
- an integrated composition host discovers installed and admitted product manifests dynamically rather than hard-coding a mandatory product list;
- a surface profile is a projection of the same product routes, capabilities, commands, and contextual views, not a separately implemented frontend;
- removing one product removes only that product's admitted presentation contributions and SHALL NOT require source changes to unrelated products;
- ordinary shell behavior SHALL NOT require private UI imports from another product; cross-product journeys use explicit public routes, commands, capabilities, or integration contracts.
