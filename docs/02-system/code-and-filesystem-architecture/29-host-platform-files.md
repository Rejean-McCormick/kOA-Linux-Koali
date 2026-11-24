<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-029",
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
    "10-adrs/ADR-002-immutable-signed-os-image.md",
    "10-adrs/ADR-012-single-narrow-privileged-broker.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-001",
    "LOCK-CODE-FS-005",
    "LOCK-CODE-FS-008",
    "LOCK-CODE-FS-009"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-ADR-002",
    "DOC-ADR-012",
    "DOC-SEC-006"
  ],
  "tags": [
    "host",
    "linux",
    "systemd",
    "boot",
    "recovery",
    "security",
    "storage",
    "network"
  ]
}
KOA:DOC-META:END -->

# Host Platform Files

## 1. Scope

`host/` contains the Linux operating-system integration owned by kOA-Linux. It does not contain component business logic. Its files map admitted component descriptors and profile plans to boot, recovery, immutable image, systemd, Linux security, network, storage, device, and session mechanisms.

## 2. Exact Host File Inventory

```text
host/README.md
host/boot/boot-policy.toml
host/boot/verify-release-set.py
host/boot/select-release-slot.py
host/boot/mark-boot-success.py
host/boot/enter-last-known-good.py
host/recovery/recovery-policy.toml
host/recovery/recovery-entry.py
host/recovery/restore-controller.py
host/recovery/forward-repair.py
host/recovery/collect-recovery-evidence.py
host/image/base-packages.yaml
host/image/package-sets/user-lightweight.yaml
host/image/filesystem-layout.yaml
host/image/partition-layout.yaml
host/image/image-manifest.yaml
host/image/build-rootfs.py
host/image/materialize-rootfs.py
host/image/build-boot-artifact.py
host/image/build-recovery-artifact.py
host/image/build-disk-image.py
host/image/seal-image.py
host/image/verify-image.py
host/systemd/targets/koa-node.target
host/systemd/targets/koa-core.target
host/systemd/targets/koa-critical.target
host/systemd/targets/koa-background.target
host/systemd/targets/koa-optional.target
host/systemd/targets/koa-activation.target
host/systemd/targets/koa-recovery.target
host/systemd/units/koa-node-agent.service
host/systemd/units/koa-node-agent.socket
host/systemd/units/koa-privileged-broker.service
host/systemd/units/koa-privileged-broker.socket
host/systemd/units/koa-release-set-verify.service
host/systemd/units/koa-activation.service
host/systemd/units/koa-health-aggregate.service
host/systemd/units/koa-offline-import.path
host/systemd/units/koa-offline-import.service
host/systemd/units/koa-backup.service
host/systemd/units/koa-backup.timer
host/systemd/units/koa-maintenance.service
host/systemd/units/koa-maintenance.timer
host/systemd/templates/koa-component.service.in
host/systemd/templates/koa-component.socket.in
host/systemd/templates/koa-worker.service.in
host/systemd/templates/koa-subsystem.service.in
host/systemd/templates/koa-timer.timer.in
host/systemd/sysusers/koa-components.conf
host/systemd/sysusers/koa-privileged-broker.conf
host/systemd/tmpfiles/koa-components.conf
host/systemd/tmpfiles/koa-runtime.conf
host/security/lsm/policy.yaml
host/security/lsm/render-apparmor.py
host/security/lsm/render-selinux.py
host/security/seccomp/component-default.json
host/security/seccomp/koa-node-agent.json
host/security/seccomp/koa-privileged-broker.json
host/security/seccomp/appliance-browser.json
host/security/capabilities/catalog.json
host/security/capabilities/component-defaults.json
host/security/polkit/50-koa.rules
host/security/sandboxing/defaults.toml
host/security/trust-bootstrap/bootstrap-policy.toml
host/networking/zones.toml
host/networking/service-exposure.toml
host/networking/offline-policy.toml
host/networking/restricted-policy.toml
host/networking/firewall.nft.in
host/networking/render-firewall.py
host/storage/layout.toml
host/storage/mounts.toml
host/storage/encryption.toml
host/storage/quotas.toml
host/storage/snapshot-policy.toml
host/storage/render-mount-units.py
host/devices/udev/90-koa-removable-media.rules
host/devices/removable-media-policy.toml
host/devices/device-policy.toml
host/sessions/graphical-session.toml
host/sessions/appliance-session.toml
host/sessions/maintenance-session.toml
host/sessions/recovery-session.toml
host/sessions/koa-session-launcher.py
host/sessions/native_workspace.py
host/sessions/koa-native-workspace-broker.py
host/sessions/native-workspace.toml
host/sessions/session_runtime.py
host/sessions/koa-appliance-session.py
host/sessions/koa-maintenance-session.py
host/sessions/koa-recovery-session.py
host/adapters/README.md
host/adapters/systemd.py
host/adapters/podman.py
host/adapters/filesystem.py
host/adapters/network.py
host/adapters/storage.py
host/adapters/koa_spaces_unix_transport.py
host/adapters/native_workspace_unix_transport.py
host/adapters/koa_spaces_adapter_factory.py
```

## 3. Separation Rules

- `boot/` verifies and selects already admitted releases; it does not build releases.
- `recovery/` operates from a bounded recovery environment and writes recovery evidence.
- `image/` creates immutable host images from release inputs and does not mutate live component data.
- static systemd targets and the narrow Node Agent units are committed; profile-derived component and subsystem units are generated from templates.
- security renderers may produce distribution-specific AppArmor or SELinux outputs from one policy source, but the generated outputs remain derived.
- network files expose only profile-admitted services.
- storage files define mount, encryption, quota, and snapshot mechanisms; component ownership remains defined by contracts.
- session files launch graphical, appliance, maintenance, or recovery sessions. kOA Spaces may be the configured navigation interface, but session launch does not grant it host authority.

## November 2026 inventory reconciliation — registered additions

The following implementation paths were already registered in the non-authoritative `.koa/file-architecture.lock.json` projection and are present in this checkout. They are recorded here to restore the correspondence between the normative source inventory and its machine projection. This registration does not authorize a release, privileged execution, or a change of ownership.

```text
host/store/koali-essentials.desktop
host/store/koali-store.desktop
host/store/README.md
host/store/setup-user.py
host/store/third-party-store.py
```
