<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-REC-KOA-SPACES-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "profile:user_lightweight"
  ],
  "canonical_refs": [
    "contracts/artifact-contracts/space-definition.schema.json",
    "contracts/artifact-contracts/module-interface-manifest.schema.json",
    "contracts/artifact-contracts/space-activation-receipt.schema.json",
    "contracts/artifact-contracts/interface-theme.schema.json",
    "contracts/artifact-contracts/interface-asset-manifest.schema.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "02-system/24-koa-spaces-design-system.md",
    "04-components/subsystems/koa-spaces.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-SYS-035",
    "DOC-SUB-KOA-SPACES"
  ],
  "tags": [
    "recipe",
    "koa-spaces",
    "activation",
    "user-lightweight",
    "rollback"
  ]
}
KOA:DOC-META:END -->

# Activate a kOA Space

## Purpose

This recipe describes a safe activation pattern for one kOA Space on a lightweight local installation.

**Terminology boundary:** “Space activation” in this recipe means selecting and committing a validated presentation/composition definition in kOA Spaces. It does **not** mean starting a service, activating a Kristal Runtime Pack, activating a governance bundle, or committing a complete Release Set. Those transitions remain owned by their respective contracts and components.

## Preconditions

- kOA Spaces is installed as an optional subsystem;
- the selected Space definition is available locally;
- every referenced module manifest is installed;
- every manifest, interface theme, and interface asset bundle has passed artifact admission;
- required capabilities can be evaluated locally;
- the previous active Space definition remains available for rollback.

## Procedure

1. Place the candidate Space definition and its referenced manifests in a staging directory.
2. Validate each JSON artifact against its declared schema.
3. Verify signatures or pinned hashes according to the active profile.
4. Resolve every module identifier to an installed and enabled contribution.
5. Resolve every route, sidebar item, widget action, icon, localization resource, page reference, theme reference, and local asset bundle reference.
6. Reject duplicate route identifiers, path collisions, circular redirects, and unknown references.
7. Evaluate required capabilities without granting any new capability.
8. Simulate online and offline composition, verify that every route and widget has a declared state, and verify local asset closure for each surface claiming offline availability.
9. Run keyboard, focus-order, contrast, reduced-motion, and narrow-display checks required by the profile.
10. Produce the candidate activation receipt.
11. Atomically switch the active Space pointer to the validated candidate.
12. Start or reload kOA Spaces and verify its health endpoint and default route.
13. Finalize the activation receipt with the observed result.

## Rollback

Rollback restores the previous validated Space pointer and restarts or reloads the presentation process. It does not modify subsystem data.

Rollback is required when:

- the global frame fails to load;
- the default module cannot resolve;
- a required module contribution is unavailable;
- a route collision appears after deployment;
- accessibility or capability checks fail;
- the health check does not reach the declared ready state.

## Offline Check

Disconnect the network and confirm that:

- the module selector still renders;
- local and cached modules remain visible according to policy;
- online-only widgets enter their declared unavailable state;
- the current Space remains understandable and renderable without public remote runtime assets;
- deep links to unavailable routes fail safely;
- Ariane can still navigate to locally permitted routes when its local mode is available.

## Evidence

Retain:

- the Space definition digest;
- all module manifest digests;
- schema validation results;
- route collision results;
- capability evaluation results;
- accessibility check results;
- activation and rollback timestamps;
- the finalized activation receipt.

## Modular product-interface behavior

This recipe assumes product UI portability. A product that supports standalone operation keeps its own product-owned entry point. When an integrated composition host is selected, the product contributes the same admitted routes and capabilities through its interface manifest. Reduced surfaces are projections of that product definition rather than separate frontends. Removing the product removes its integrated contributions without changing unrelated product source code.
