<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-030",
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
    "contracts/release-channels.contract.json",
    "03-profiles/00-profile-model.md",
    "06-lifecycle/04-release-sets.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-004",
    "LOCK-CODE-FS-007",
    "LOCK-CODE-FS-009"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-PRO-000",
    "DOC-LIFE-004"
  ],
  "tags": [
    "assembly",
    "profiles",
    "packaging",
    "release",
    "generated"
  ]
}
KOA:DOC-META:END -->

# Assembly, Profiles, Packaging, and Release Files

## 1. Scope

This file freezes the source inventory that converts canonical contracts and profile selections into deterministic deployment plans, packages, system images, offline bundles, and release sets. Profiles compose shared components. They never own parallel source implementations.

## 2. Assembly Engine

```text
assembly/README.md
assembly/pyproject.toml
assembly/src/koa_assembly/__init__.py
assembly/src/koa_assembly/__main__.py
assembly/src/koa_assembly/cli.py
assembly/src/koa_assembly/model.py
assembly/src/koa_assembly/contract_loader.py
assembly/src/koa_assembly/diagnostics.py
assembly/src/koa_assembly/profiles/__init__.py
assembly/src/koa_assembly/profiles/resolver.py
assembly/src/koa_assembly/profiles/overlays.py
assembly/src/koa_assembly/profiles/membership.py
assembly/src/koa_assembly/profiles/capabilities.py
assembly/src/koa_assembly/plans/__init__.py
assembly/src/koa_assembly/plans/dependency_graph.py
assembly/src/koa_assembly/plans/service_plan.py
assembly/src/koa_assembly/plans/resource_plan.py
assembly/src/koa_assembly/plans/storage_plan.py
assembly/src/koa_assembly/plans/network_plan.py
assembly/src/koa_assembly/plans/backup_plan.py
assembly/src/koa_assembly/renderers/__init__.py
assembly/src/koa_assembly/renderers/systemd.py
assembly/src/koa_assembly/renderers/quadlet.py
assembly/src/koa_assembly/renderers/compose.py
assembly/src/koa_assembly/renderers/kubernetes.py
assembly/src/koa_assembly/renderers/image.py
assembly/src/koa_assembly/renderers/offline_bundle.py
assembly/src/koa_assembly/releases/__init__.py
assembly/src/koa_assembly/releases/release_set.py
assembly/src/koa_assembly/releases/locks.py
assembly/src/koa_assembly/releases/manifest.py
assembly/tests/conftest.py
assembly/tests/test_profile_resolution.py
assembly/tests/test_overlay_resolution.py
assembly/tests/test_dependency_graph.py
assembly/tests/test_service_plan.py
assembly/tests/test_resource_plan.py
assembly/tests/test_storage_plan.py
assembly/tests/test_render_determinism.py
assembly/tests/test_release_set.py
```
## 3. Profile Implementation Settings

```text
profiles/README.md
profiles/implementation-settings/user-lightweight.toml
profiles/implementation-settings/developer-linux-workstation.toml
profiles/implementation-settings/developer-windows-wsl.toml
profiles/implementation-settings/sovereign-linux-node.toml
profiles/implementation-settings/sovereign-hub.toml
profiles/implementation-settings/build-farm.toml
profiles/implementation-settings/control-plane.toml
profiles/implementation-settings/high-assurance.toml
profiles/implementation-settings/sovereign-offline.toml
profiles/implementation-settings/appliance-shell.toml
profiles/overlays/high-assurance.toml
profiles/overlays/sovereign-offline.toml
profiles/overlays/appliance-shell.toml
profiles/test-fixtures/minimal-user.json
profiles/test-fixtures/sovereign-node.json
profiles/test-fixtures/offline-school.json
profiles/test-fixtures/build-worker.json
profiles/native-applications/README.md
profiles/native-applications/admission/firefox.json
profiles/native-applications/admission/vlc.json
profiles/native-applications/admission/libreoffice.json
profiles/native-applications/admission/thunderbird.json
profiles/native-applications/data/firefox.json
profiles/native-applications/data/vlc.json
profiles/native-applications/data/libreoffice.json
profiles/native-applications/data/thunderbird.json
profiles/native-applications/fixtures/files-selection.json
```
## 4. Packaging Inputs

```text
packaging/README.md
packaging/system/image.toml
packaging/system/recovery-image.toml
packaging/system/package-sources.toml
packaging/components/audit-broker.toml
packaging/components/governance-policy-runtime.toml
packaging/components/identity-and-trust.toml
packaging/components/koa-mediatheque.toml
packaging/components/koa-node-agent.toml
packaging/components/kristal-runtime.toml
packaging/components/publication-gateway.toml
packaging/components/resource-governor.toml
packaging/containers/audit-broker/Containerfile
packaging/containers/audit-broker/container.toml
packaging/containers/governance-policy-runtime/Containerfile
packaging/containers/governance-policy-runtime/container.toml
packaging/containers/identity-and-trust/Containerfile
packaging/containers/identity-and-trust/container.toml
packaging/containers/koa-mediatheque/Containerfile
packaging/containers/koa-mediatheque/container.toml
packaging/containers/kristal-runtime/Containerfile
packaging/containers/kristal-runtime/container.toml
packaging/containers/publication-gateway/Containerfile
packaging/containers/publication-gateway/container.toml
packaging/containers/resource-governor/Containerfile
packaging/containers/resource-governor/container.toml
packaging/subsystems/ariane.toml
packaging/subsystems/koa-spaces.toml
packaging/subsystems/konnaxion.toml
packaging/subsystems/orgo.toml
packaging/subsystems/semantik-architect.toml
packaging/subsystems/sentient.toml
packaging/subsystems/uckk.toml
packaging/offline-bundles/manifest.toml
packaging/offline-bundles/include-rules.toml
packaging/offline-bundles/verification-policy.toml
packaging/repositories/repository.toml
packaging/repositories/metadata-policy.toml
```
## 5. Release Construction and Generated Root

```text
release/README.md
release/channels/os-image.toml
release/channels/service-bundle.toml
release/channels/governance-policy.toml
release/channels/kristal-artifacts.toml
release/locks/README.md
release/manifests/release-set.template.json
release/manifests/artifact-manifest.template.json
release/signing/policy.toml
release/signing/roles.toml
release/signing/offline-signing.toml
release/verification/verification-policy.toml
release/verification/verify-release.py
release/sbom/sbom-policy.toml
release/sbom/generate-sbom.py
release/provenance/provenance-policy.toml
release/provenance/generate-provenance.py
release/promotion/channels.toml
release/promotion/promote.py
release/promotion/rollback.py
release/native-workspace-security.toml
generated/.gitignore
generated/README.md
```

## 6. Contract-Driven Assembly

The assembly pipeline SHALL load canonical contracts from `docs/contracts/`, resolve profile inheritance and overlays, compute membership and capabilities, build dependency and resource plans, and render deployment outputs. Hand-maintained service lists SHALL NOT be duplicated across profile settings, systemd files, container manifests, and documentation.

## 7. Generated Output Rule

`generated/` is the code-and-deployment build output root. Except for `.gitignore` and `README.md`, its contents are not manually maintained source files. Typical generated subtrees include contract bindings, profile plans, service units, deployment manifests, image manifests, release locks, catalogs, and test fixtures. Every generated file must identify its generator and source digest or be reproducibly attributable to a build manifest.

## 8. Release Separation

Packaging determines how admitted source becomes a package or image payload. Release construction determines compatible versions, signatures, provenance, SBOMs, promotion, rollback, and channel identity. Component source code SHALL NOT contain release-channel policy or signing keys.

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
profiles/native-applications/admission/koali-essentials.json
profiles/native-applications/admission/koali-store.json
profiles/native-applications/data/koali-essentials.json
profiles/native-applications/data/koali-store.json
```
