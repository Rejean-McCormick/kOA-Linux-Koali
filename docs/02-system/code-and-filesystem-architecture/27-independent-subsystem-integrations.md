<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-027",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/ai-navigation.contract.json",
    "02-system/02-logical-architecture.md",
    "02-system/04-component-boundaries.md",
    "02-system/07-cross-component-communication.md",
    "02-system/19-release-and-artifact-identity.md",
    "04-components/04-subsystem-documentation-boundaries.md",
    "05-development/00-development-model.md",
    "06-lifecycle/02-release-model.md",
    "07-security/05-privilege-boundaries.md",
    "08-operations/00-operating-model.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/23-code-and-filesystem-architecture.md",
    "contracts/subsystems/ariane.subsystem.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "contracts/subsystems/konnaxion.subsystem.json",
    "contracts/subsystems/orgo.subsystem.json",
    "contracts/subsystems/semantik-architect.subsystem.json",
    "contracts/subsystems/sentient.subsystem.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-002",
    "LOCK-CODE-FS-003",
    "LOCK-CODE-FS-006",
    "LOCK-CODE-FS-008",
    "LOCK-CODE-FS-009"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-COMP-SUBSYSTEM-BOUNDARIES"
  ],
  "tags": [
    "integrations",
    "subsystems",
    "ariane",
    "koa-spaces",
    "konnaxion",
    "orgo",
    "semantik",
    "sentient"
  ]
}
KOA:DOC-META:END -->

# Independent Subsystem Integration Files

## 1. Scope

This file freezes the kOA-Linux-side integration inventory for independently owned subsystems. These directories contain source pins, compatibility metadata, deployment and resource declarations, adapters, interface contributions, and boundary tests. They SHALL NOT contain the subsystem's internal application source, database migrations, complete API implementation, or authoritative internal documentation.

## 2. Ariane Integration

```text
integrations/ariane/README.md
integrations/ariane/source.lock.json
integrations/ariane/compatibility.json
integrations/ariane/integration.toml
integrations/ariane/deployment.toml
integrations/ariane/resource-envelope.toml
integrations/ariane/health.toml
integrations/ariane/storage.toml
integrations/ariane/backup.toml
integrations/ariane/degradation.toml
integrations/ariane/adapter/pyproject.toml
integrations/ariane/adapter/src/koa_ariane_adapter/__init__.py
integrations/ariane/adapter/src/koa_ariane_adapter/bootstrap.py
integrations/ariane/adapter/src/koa_ariane_adapter/client.py
integrations/ariane/adapter/src/koa_ariane_adapter/health.py
integrations/ariane/adapter/src/koa_ariane_adapter/capabilities.py
integrations/ariane/adapter/src/koa_ariane_adapter/receipts.py
integrations/ariane/adapter/src/koa_ariane_adapter/navigation.py
integrations/ariane/adapter/src/koa_ariane_adapter/intent_bridge.py
integrations/ariane/adapter/src/koa_ariane_adapter/voice_bridge.py
integrations/ariane/interface/module-interface.json
integrations/ariane/interface/sidebar.json
integrations/ariane/interface/widgets.json
integrations/ariane/tests/conftest.py
integrations/ariane/tests/_support.py
integrations/ariane/tests/test_contract.py
integrations/ariane/tests/test_health.py
integrations/ariane/tests/test_degradation.py
integrations/ariane/tests/test_boundary.py
```
## 3. Koali Spaces Integration

```text
integrations/koa-spaces/README.md
integrations/koa-spaces/source.lock.json
integrations/koa-spaces/compatibility.json
integrations/koa-spaces/integration.toml
integrations/koa-spaces/deployment.toml
integrations/koa-spaces/resource-envelope.toml
integrations/koa-spaces/health.toml
integrations/koa-spaces/storage.toml
integrations/koa-spaces/backup.toml
integrations/koa-spaces/degradation.toml
integrations/koa-spaces/adapter/pyproject.toml
integrations/koa-spaces/adapter/src/koa_spaces_adapter/__init__.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/bootstrap.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/appearance.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/client.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/health.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/capabilities.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/receipts.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/space_activation.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/module_manifest.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/native_workspace.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/host_bridge.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/route_bridge.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/interface_assets.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/interface_theme.py
integrations/koa-spaces/adapter/src/koa_spaces_adapter/shell_state.py
integrations/koa-spaces/interface/default-space.json
integrations/koa-spaces/interface/school-space.json
integrations/koa-spaces/interface/community-space.json
integrations/koa-spaces/interface/global-widgets.json
integrations/koa-spaces/interface/appearance/accent-palette.json
integrations/koa-spaces/interface/themes/default.json
integrations/koa-spaces/interface/themes/school.json
integrations/koa-spaces/interface/themes/community.json
integrations/koa-spaces/interface/icons/home.svg
integrations/koa-spaces/interface/icons/search.svg
integrations/koa-spaces/interface/icons/network.svg
integrations/koa-spaces/interface/icons/learn.svg
integrations/koa-spaces/interface/icons/library.svg
integrations/koa-spaces/interface/icons/assignments.svg
integrations/koa-spaces/interface/icons/guidance.svg
integrations/koa-spaces/interface/icons/community.svg
integrations/koa-spaces/interface/icons/work.svg
integrations/koa-spaces/interface/localization/koa-spaces.en.json
integrations/koa-spaces/interface/localization/koa-spaces.fr-CA.json
integrations/koa-spaces/tests/conftest.py
integrations/koa-spaces/tests/_support.py
integrations/koa-spaces/tests/test_contract.py
integrations/koa-spaces/tests/test_health.py
integrations/koa-spaces/tests/test_degradation.py
integrations/koa-spaces/tests/test_boundary.py
integrations/koa-spaces/tests/test_interface_assets.py
integrations/koa-spaces/tests/test_interface_theme.py
integrations/koa-spaces/tests/test_shell_state.py
integrations/koa-spaces/tests/test_unix_transport.py
integrations/koa-spaces/tests/test_capability_projection.py
integrations/koa-spaces/tests/test_ks2_contract_convergence.py
integrations/koa-spaces/tests/test_native_workspace_bridge.py
```
## 4. Konnaxion Integration

```text
integrations/konnaxion/README.md
integrations/konnaxion/source.lock.json
integrations/konnaxion/compatibility.json
integrations/konnaxion/integration.toml
integrations/konnaxion/deployment.toml
integrations/konnaxion/resource-envelope.toml
integrations/konnaxion/health.toml
integrations/konnaxion/storage.toml
integrations/konnaxion/backup.toml
integrations/konnaxion/degradation.toml
integrations/konnaxion/adapter/pyproject.toml
integrations/konnaxion/adapter/src/koa_konnaxion_adapter/__init__.py
integrations/konnaxion/adapter/src/koa_konnaxion_adapter/bootstrap.py
integrations/konnaxion/adapter/src/koa_konnaxion_adapter/client.py
integrations/konnaxion/adapter/src/koa_konnaxion_adapter/health.py
integrations/konnaxion/adapter/src/koa_konnaxion_adapter/capabilities.py
integrations/konnaxion/adapter/src/koa_konnaxion_adapter/receipts.py
integrations/konnaxion/adapter/src/koa_konnaxion_adapter/routes.py
integrations/konnaxion/adapter/src/koa_konnaxion_adapter/notifications.py
integrations/konnaxion/adapter/src/koa_konnaxion_adapter/surface_bridge.py
integrations/konnaxion/interface/module-interface.json
integrations/konnaxion/interface/sidebar.json
integrations/konnaxion/interface/widgets.json
integrations/konnaxion/tests/conftest.py
integrations/konnaxion/tests/_support.py
integrations/konnaxion/tests/test_contract.py
integrations/konnaxion/tests/test_health.py
integrations/konnaxion/tests/test_degradation.py
integrations/konnaxion/tests/test_boundary.py
```
## 5. Orgo Integration

```text
integrations/orgo/README.md
integrations/orgo/source.lock.json
integrations/orgo/compatibility.json
integrations/orgo/integration.toml
integrations/orgo/deployment.toml
integrations/orgo/resource-envelope.toml
integrations/orgo/health.toml
integrations/orgo/storage.toml
integrations/orgo/backup.toml
integrations/orgo/degradation.toml
integrations/orgo/adapter/pyproject.toml
integrations/orgo/adapter/src/koa_orgo_adapter/__init__.py
integrations/orgo/adapter/src/koa_orgo_adapter/bootstrap.py
integrations/orgo/adapter/src/koa_orgo_adapter/client.py
integrations/orgo/adapter/src/koa_orgo_adapter/health.py
integrations/orgo/adapter/src/koa_orgo_adapter/capabilities.py
integrations/orgo/adapter/src/koa_orgo_adapter/receipts.py
integrations/orgo/adapter/src/koa_orgo_adapter/tasks.py
integrations/orgo/adapter/src/koa_orgo_adapter/commands.py
integrations/orgo/adapter/src/koa_orgo_adapter/surface_bridge.py
integrations/orgo/interface/module-interface.json
integrations/orgo/interface/sidebar.json
integrations/orgo/interface/widgets.json
integrations/orgo/tests/conftest.py
integrations/orgo/tests/test_contract.py
integrations/orgo/tests/test_health.py
integrations/orgo/tests/test_degradation.py
integrations/orgo/tests/test_boundary.py
```
## 6. SemantiK Architect Integration

```text
integrations/semantik-architect/README.md
integrations/semantik-architect/source.lock.json
integrations/semantik-architect/compatibility.json
integrations/semantik-architect/integration.toml
integrations/semantik-architect/deployment.toml
integrations/semantik-architect/resource-envelope.toml
integrations/semantik-architect/health.toml
integrations/semantik-architect/storage.toml
integrations/semantik-architect/backup.toml
integrations/semantik-architect/degradation.toml
integrations/semantik-architect/adapter/pyproject.toml
integrations/semantik-architect/adapter/src/koa_semantik_architect_adapter/__init__.py
integrations/semantik-architect/adapter/src/koa_semantik_architect_adapter/bootstrap.py
integrations/semantik-architect/adapter/src/koa_semantik_architect_adapter/client.py
integrations/semantik-architect/adapter/src/koa_semantik_architect_adapter/health.py
integrations/semantik-architect/adapter/src/koa_semantik_architect_adapter/capabilities.py
integrations/semantik-architect/adapter/src/koa_semantik_architect_adapter/receipts.py
integrations/semantik-architect/adapter/src/koa_semantik_architect_adapter/runtime_packs.py
integrations/semantik-architect/adapter/src/koa_semantik_architect_adapter/compiler_jobs.py
integrations/semantik-architect/adapter/src/koa_semantik_architect_adapter/artifact_bridge.py
integrations/semantik-architect/interface/module-interface.json
integrations/semantik-architect/interface/sidebar.json
integrations/semantik-architect/interface/widgets.json
integrations/semantik-architect/tests/conftest.py
integrations/semantik-architect/tests/_support.py
integrations/semantik-architect/tests/test_contract.py
integrations/semantik-architect/tests/test_health.py
integrations/semantik-architect/tests/test_degradation.py
integrations/semantik-architect/tests/test_boundary.py
```
## 7. SenTient Integration

```text
integrations/sentient/README.md
integrations/sentient/source.lock.json
integrations/sentient/compatibility.json
integrations/sentient/integration.toml
integrations/sentient/deployment.toml
integrations/sentient/resource-envelope.toml
integrations/sentient/health.toml
integrations/sentient/storage.toml
integrations/sentient/backup.toml
integrations/sentient/degradation.toml
integrations/sentient/adapter/pyproject.toml
integrations/sentient/adapter/src/koa_sentient_adapter/__init__.py
integrations/sentient/adapter/src/koa_sentient_adapter/bootstrap.py
integrations/sentient/adapter/src/koa_sentient_adapter/client.py
integrations/sentient/adapter/src/koa_sentient_adapter/health.py
integrations/sentient/adapter/src/koa_sentient_adapter/capabilities.py
integrations/sentient/adapter/src/koa_sentient_adapter/receipts.py
integrations/sentient/adapter/src/koa_sentient_adapter/candidate_artifacts.py
integrations/sentient/adapter/src/koa_sentient_adapter/workbench_jobs.py
integrations/sentient/adapter/src/koa_sentient_adapter/artifact_bridge.py
integrations/sentient/interface/module-interface.json
integrations/sentient/interface/sidebar.json
integrations/sentient/interface/widgets.json
integrations/sentient/tests/conftest.py
integrations/sentient/tests/test_contract.py
integrations/sentient/tests/test_health.py
integrations/sentient/tests/test_degradation.py
integrations/sentient/tests/test_boundary.py
```

## 8. Integration File Semantics

- `source.lock.json` pins repository, release or commit, source digest, license metadata, and expected documentation release.
- `compatibility.json` declares supported kOA contract versions and explicitly rejected versions.
- `integration.toml` declares the integration identity, adapter entrypoint, required capabilities, and interface ownership.
- deployment, resource, health, storage, backup, and degradation files describe kOA-owned operating boundaries only.
- `interface/` contains presentation contributions consumed by Koali Spaces. Their visibility grants no authority.
- adapter code translates between declared interfaces. It does not reproduce subsystem business rules.
- every integration test suite SHALL prove absence of direct database writes and safe behavior when the subsystem is missing, incompatible, or offline.

## 9. Koali Spaces Restriction

The Koali Spaces integration may activate validated Space definitions, expose admitted module manifests, and bridge presentation routes. It may not perform host release activation, resource admission, identity issuance, policy evaluation, workflow mutation, course-state mutation, media ownership, or direct writes to another subsystem's data.

## Koali product UI modularity

This document is interpreted with the Koali product-interface portability rule:

- each independently packaged product owns its user interface and remains independently operable when its declared standalone mode is supported;
- shared Koali shell and design-system code is reusable presentation infrastructure, not a mandatory product runtime and not a source of business authority;
- an integrated composition host discovers installed and admitted product manifests dynamically rather than hard-coding a mandatory product list;
- a surface profile is a projection of the same product routes, capabilities, commands, and contextual views, not a separately implemented frontend;
- removing one product removes only that product's admitted presentation contributions and SHALL NOT require source changes to unrelated products;
- ordinary shell behavior SHALL NOT require private UI imports from another product; cross-product journeys use explicit public routes, commands, capabilities, or integration contracts.

## November 2026 inventory reconciliation — registered additions

The following implementation paths were already registered in the non-authoritative `.koa/file-architecture.lock.json` projection and are present in this checkout. They are recorded here to restore the correspondence between the normative source inventory and its machine projection. This registration does not authorize a release, privileged execution, or a change of ownership.

```text
integrations/koa-spaces/adapter/src/koa_spaces_adapter/unix_transport.py
```
