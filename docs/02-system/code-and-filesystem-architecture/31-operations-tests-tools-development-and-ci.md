<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-031",
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
    "05-development/14-build-test-and-validation.md",
    "08-operations/00-operating-model.md",
    "09-conformance/00-conformance-model.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-004",
    "LOCK-CODE-FS-008",
    "LOCK-CODE-FS-009"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-DEV-014",
    "DOC-OPS-000",
    "DOC-CONF-000"
  ],
  "tags": [
    "operations",
    "tests",
    "tools",
    "development",
    "ci"
  ]
}
KOA:DOC-META:END -->

# Operations, Tests, Tools, Development, and CI Files

## 1. Scope

This file freezes the operational code, cross-system test suites, repository tooling, local development environment, and reusable CI policy inventory. Operational procedures remain documented under `docs/08-operations/` and `docs/11-recipes/`; this file lists executable implementation paths only.

## 2. Operations Code

```text
operations/README.md
operations/pyproject.toml
operations/src/koa_operations/__init__.py
operations/src/koa_operations/__main__.py
operations/src/koa_operations/cli.py
operations/src/koa_operations/config.py
operations/src/koa_operations/evidence.py
operations/src/koa_operations/backup/__init__.py
operations/src/koa_operations/backup/plan.py
operations/src/koa_operations/backup/run.py
operations/src/koa_operations/backup/verify.py
operations/src/koa_operations/backup/native_applications.py
operations/src/koa_operations/restore/__init__.py
operations/src/koa_operations/restore/plan.py
operations/src/koa_operations/restore/run.py
operations/src/koa_operations/restore/verify.py
operations/src/koa_operations/diagnostics/__init__.py
operations/src/koa_operations/diagnostics/health.py
operations/src/koa_operations/diagnostics/support_bundle.py
operations/src/koa_operations/diagnostics/redaction.py
operations/src/koa_operations/maintenance/__init__.py
operations/src/koa_operations/maintenance/cleanup.py
operations/src/koa_operations/maintenance/verify_storage.py
operations/src/koa_operations/maintenance/rotate_receipts.py
operations/src/koa_operations/migration/__init__.py
operations/src/koa_operations/migration/plan.py
operations/src/koa_operations/migration/apply.py
operations/src/koa_operations/migration/verify.py
operations/src/koa_operations/recovery/__init__.py
operations/src/koa_operations/recovery/enter.py
operations/src/koa_operations/recovery/repair.py
operations/src/koa_operations/recovery/rollback.py
operations/tests/conftest.py
operations/tests/test_backup.py
operations/tests/test_restore.py
operations/tests/test_diagnostics.py
operations/tests/test_redaction.py
operations/tests/test_maintenance.py
operations/tests/test_migration.py
operations/tests/test_recovery.py
operations/tests/test_native_applications.py
```
## 3. Cross-System Tests

```text
tests/README.md
tests/conftest.py
tests/fixtures/minimal-release-set.json
tests/fixtures/minimal-profile-plan.json
tests/fixtures/offline-bundle.json
tests/fixtures/invalid-signature.json
tests/contracts/test_schema_validation.py
tests/contracts/test_generated_bindings.py
tests/contracts/test_component_contracts.py
tests/contracts/test_subsystem_contracts.py
tests/contracts/test_profile_contracts.py
tests/contracts/test_release_contracts.py
tests/boundaries/test_no_private_component_imports.py
tests/boundaries/test_no_cross_database_writes.py
tests/boundaries/test_no_vendored_subsystems.py
tests/boundaries/test_ui_has_no_privileged_access.py
tests/boundaries/test_generated_roots.py
tests/boundaries/test_path_ownership.py
tests/profiles/test_user_lightweight.py
tests/profiles/test_developer_linux.py
tests/profiles/test_developer_wsl.py
tests/profiles/test_sovereign_node.py
tests/profiles/test_sovereign_hub.py
tests/profiles/test_build_farm.py
tests/profiles/test_control_plane.py
tests/profiles/test_high_assurance.py
tests/profiles/test_sovereign_offline.py
tests/profiles/test_appliance_shell.py
tests/integration/test_ariane.py
tests/integration/test_koa_spaces.py
tests/integration/test_konnaxion.py
tests/integration/test_orgo.py
tests/integration/test_semantik_architect.py
tests/integration/test_sentient.py
tests/integration/test_uckk_publication.py
tests/integration/test_uckk_import.py
tests/system/test_boot_verification.py
tests/system/test_service_activation.py
tests/system/test_health_aggregation.py
tests/system/test_release_activation.py
tests/system/test_last_known_good.py
tests/system/test_backup_coordination.py
tests/system/test_restore_coordination.py
tests/system/test_appliance_session.py
tests/system/test_native_workspace.py
tests/system/test_native_workspace_package_set.py
tests/security/test_privileged_catalog.py
tests/security/test_path_traversal.py
tests/security/test_capability_drop.py
tests/security/test_seccomp_profiles.py
tests/security/test_network_exposure.py
tests/security/test_secret_absence.py
tests/security/test_signature_failure.py
tests/security/test_break_glass.py
tests/offline/test_offline_boot.py
tests/offline/test_offline_navigation.py
tests/offline/test_offline_import.py
tests/offline/test_cached_artifacts.py
tests/offline/test_network_loss.py
tests/offline/test_no_undeclared_substitution.py
tests/recovery/test_recovery_boot.py
tests/recovery/test_restore_last_known_good.py
tests/recovery/test_forward_repair.py
tests/recovery/test_failed_activation.py
tests/recovery/test_recovery_evidence.py
tests/reproducibility/test_contract_generation.py
tests/reproducibility/test_profile_plan_determinism.py
tests/reproducibility/test_image_manifest_determinism.py
tests/reproducibility/test_bundle_determinism.py
tests/reproducibility/test_sbom_determinism.py
tests/conformance/test_requirement_traceability.py
tests/conformance/test_release_evidence.py
tests/conformance/test_profile_claims.py
tests/conformance/test_filesystem_architecture.py
```

### 3.1 Registered ordinary additions

The following previously registered additions remain part of the frozen implementation inventory:

```text
tests/reproducibility/test_image_binary_determinism.py
tests/system/qemu-machine.toml
tests/system/qemu_harness.py
tests/system/test_qemu_boot.py
tests/system/test_qemu_appliance_session.py
tests/system/test_qemu_navigation.py
tests/system/test_qemu_mediatheque.py
tests/system/test_qemu_semantik_architect.py
tests/system/test_rootfs_materialization.py
tests/system/test_system_image_build.py
tests/security/test_qemu_appliance_confinement.py
tests/recovery/test_qemu_recovery_boot.py
tests/recovery/test_qemu_failed_candidate_rollback.py
tests/offline/test_qemu_offline_navigation.py
```

The following implementation files are registered after the frozen baseline inventory under the ordinary-addition rules in `33-path-ownership-and-change-rules.md`. They inherit the existing `tests/` owner and do not amend a structural root or authority boundary.

- `tests/reproducibility/test_image_binary_determinism.py` — byte-for-byte system-image rootfs reproducibility evidence for identical declared inputs and toolchain, including the declared `SOURCE_DATE_EPOCH` variable.
- `tests/system/test_qemu_navigation.py` — QEMU-observed keyboard navigation on the local surface admitted by the effective profile; an unselected kOA Spaces source is not a prerequisite.
- `tests/system/test_qemu_mediatheque.py` — QEMU-observed kOA Mediatheque availability only when its admitted artifact belongs to the active Release Set services channel; service payloads remain outside the system image.
- `tests/system/test_qemu_semantik_architect.py` — fail-closed QEMU validation for an independently sourced SemantiK Architect artifact, with unselected or unadmitted states never promoted to pass.
- `tests/offline/test_qemu_offline_navigation.py` — QEMU validation with the VM network device disabled, preserving admitted local navigation and deterministic Mediatheque behavior when selected.

- `tests/system/qemu-machine.toml` — deterministic QEMU machine configuration used by the system-validation harness.
- `tests/system/qemu_harness.py` — shared bounded QEMU harness for boot, navigation, confinement, offline, and recovery validation.
- `tests/system/test_qemu_boot.py` — QEMU boot validation for the built system image and declared boot evidence.
- `tests/system/test_qemu_appliance_session.py` — QEMU validation of the appliance session boundary and observable local surface.
- `tests/system/test_rootfs_materialization.py` — deterministic rootfs materialization validation before image assembly.
- `tests/system/test_system_image_build.py` — system-image build-plan and artifact validation for the declared image pipeline.
- `tests/security/test_qemu_appliance_confinement.py` — QEMU-observed confinement validation for the appliance session security boundary.
- `tests/recovery/test_qemu_recovery_boot.py` — QEMU validation that the declared recovery target boots independently.
- `tests/recovery/test_qemu_failed_candidate_rollback.py` — QEMU validation that a failed candidate returns to the retained valid state.

## 4. Repository Tooling

```text
tools/README.md
tools/src/koa_tools/__init__.py
tools/src/koa_tools/cli.py
tools/src/koa_tools/config.py
tools/src/koa_tools/process.py
tools/src/koa_tools/repository.py
tools/src/koa_tools/commands/__init__.py
tools/src/koa_tools/commands/validate.py
tools/src/koa_tools/commands/generate.py
tools/src/koa_tools/commands/assemble.py
tools/src/koa_tools/commands/build_image.py
tools/src/koa_tools/commands/build_component.py
tools/src/koa_tools/commands/build_bundle.py
tools/src/koa_tools/commands/verify.py
tools/src/koa_tools/commands/test.py
tools/src/koa_tools/commands/release.py
tools/src/koa_tools/commands/diagnose.py
tools/src/koa_tools/checks/__init__.py
tools/src/koa_tools/checks/file_architecture.py
tools/src/koa_tools/checks/path_ownership.py
tools/src/koa_tools/checks/dependencies.py
tools/src/koa_tools/checks/generated_content.py
tools/src/koa_tools/checks/source_pins.py
tools/src/koa_tools/checks/runtime_paths.py
tools/scripts/bootstrap.sh
tools/scripts/bootstrap.ps1
tools/scripts/setup-development.sh
tools/scripts/setup-development.ps1
tools/tests/test_cli.py
tools/tests/test_file_architecture.py
tools/tests/test_path_ownership.py
tools/tests/test_source_pins.py
tools/tests/test_build_component.py
tools/tests/test_build_image.py
```
## 5. Development Environment

```text
dev/README.md
dev/containers/Containerfile
dev/containers/compose.yaml
dev/containers/devcontainer.json
dev/workspaces/default.workspace.json
dev/workspaces/wsl.workspace.json
dev/local-services/compose.yaml
dev/local-services/ports.toml
dev/local-services/volumes.toml
dev/fixtures/sample-space.json
dev/fixtures/sample-media-record.json
dev/fixtures/sample-kristal.json
dev/fixtures/sample-policy-bundle.json
dev/fixtures/sample-release-set.json
dev/examples/component-client.py
dev/examples/integration-adapter.py
dev/examples/health-probe.py
```
## 6. CI Policies and Scripts

```text
ci/README.md
ci/policies/required-checks.json
ci/policies/path-filters.json
ci/policies/release-gates.json
ci/policies/security-gates.json
ci/policies/offline-gates.json
ci/scripts/check-clean.py
ci/scripts/check-changed-paths.py
ci/scripts/run-contracts.py
ci/scripts/run-components.py
ci/scripts/run-system-tests.py
ci/scripts/run-security.py
ci/scripts/run-offline.py
ci/scripts/run-reproducibility.py
ci/scripts/build-release-candidate.py
ci/scripts/publish-evidence.py
```

## 7. Test Placement Rules

- component-internal tests remain with their component;
- integration-adapter tests remain with their integration;
- `tests/` contains only cross-component, profile, host, security, offline, recovery, reproducibility, and conformance verification;
- a system E2E test is not sufficient evidence for an authority boundary that can be tested at a lower level;
- security and offline failure behavior are separate suites and cannot be inferred from nominal-path success.

## 8. Tooling Rules

The root `pyproject.toml` exposes the `koa` command and includes `tools/src`. CI workflows call these same commands. Scripts in `ci/` and `.github/workflows/` are thin orchestration layers. No release, signing, path-ownership, or architecture-validation logic may exist only in hosted CI.

## November 2026 inventory reconciliation — registered additions

The following implementation paths were already registered in the non-authoritative `.koa/file-architecture.lock.json` projection and are present in this checkout. They are recorded here to restore the correspondence between the normative source inventory and its machine projection. This registration does not authorize a release, privileged execution, or a change of ownership.

```text
ci/scripts/gate_scope.py
ci/tests/test_gate_scopes.py
ci/UPDATE_20260919.md
ci/UPDATE_FILES_20260919.json
tests/system/test_third_party_store.py
```
