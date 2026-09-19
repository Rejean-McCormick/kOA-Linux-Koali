<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-024",
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
    "02-system/23-code-and-filesystem-architecture.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-001",
    "LOCK-CODE-FS-004",
    "LOCK-CODE-FS-009",
    "LOCK-CODE-FS-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-GOV-000"
  ],
  "tags": [
    "repository-root",
    "documentation-boundary",
    "ci",
    "ownership"
  ]
}
KOA:DOC-META:END -->

# Repository Root and Documentation Files

## 1. Scope

This document freezes all repository-root control files, repository metadata, primary CI entrypoints, license inventory files, and the documentation boundary used by the code architecture.

The complete existing documentation file inventory remains the generated `docs/generated/document-index.json`. Repeating all active documentation filenames here would create a circular architectural dependency and would incorrectly make every editorial addition a code-layout change. The stable `docs/` section roots and the complete files of this architecture series are frozen here.

## 2. Exact Baseline File Inventory

```text
.editorconfig
.gitattributes
.gitignore
.smartignore
.pre-commit-config.yaml
.python-version
.rustfmt.toml
Cargo.lock
Cargo.toml
CHANGELOG.md
CONTRIBUTING.md
NOTICE.md
README.md
REUSE.toml
SECURITY.md
pyproject.toml
rust-toolchain.toml
uv.lock
LICENSES/README.md
LICENSES/THIRD_PARTY.md
.koa/repository.json
.koa/path-ownership.json
.koa/dependency-rules.json
.koa/generated-paths.json
.koa/runtime-paths.json
.koa/source-pins.json
.koa/file-architecture.lock.json
.koa/workspace.schema.json
.github/CODEOWNERS
.github/dependabot.yml
.github/pull_request_template.md
.github/ISSUE_TEMPLATE/architecture-change.yml
.github/ISSUE_TEMPLATE/bug.yml
.github/ISSUE_TEMPLATE/documentation.yml
.github/workflows/documentation.yml
.github/workflows/contracts.yml
.github/workflows/components.yml
.github/workflows/system-image.yml
.github/workflows/offline.yml
.github/workflows/security.yml
.github/workflows/release.yml
docs/README.md
docs/AI_CONTEXT.md
docs/CHANGELOG.md
docs/CONTRIBUTING.md
docs/02-system/23-code-and-filesystem-architecture.md
docs/02-system/code-and-filesystem-architecture/24-repository-root-and-documentation.md
docs/02-system/code-and-filesystem-architecture/25-internal-components-node-trust-governance.md
docs/02-system/code-and-filesystem-architecture/26-internal-components-data-publication-and-knowledge.md
docs/02-system/code-and-filesystem-architecture/27-independent-subsystem-integrations.md
docs/02-system/code-and-filesystem-architecture/28-uckk-external-services-and-transport-interfaces.md
docs/02-system/code-and-filesystem-architecture/29-host-platform-files.md
docs/02-system/code-and-filesystem-architecture/30-assembly-profiles-packaging-and-release.md
docs/02-system/code-and-filesystem-architecture/31-operations-tests-tools-development-and-ci.md
docs/02-system/code-and-filesystem-architecture/32-installed-runtime-filesystem.md
docs/02-system/code-and-filesystem-architecture/33-path-ownership-and-change-rules.md
```

## 3. Stable Documentation Roots

```text
docs/
├── 00-governance/
├── 01-constitution/
├── 02-system/
├── 03-profiles/
├── 04-components/
├── 05-development/
├── 06-lifecycle/
├── 07-security/
├── 08-operations/
├── 09-conformance/
├── 10-adrs/
├── 11-recipes/
├── contracts/
├── finalization-reports/
├── generated/
├── schemas/
├── subsystems/
└── tools/
```

No implementation source, runtime state, package payload, subsystem checkout, container build context, or secret may be placed under `docs/`.

## 4. Root File Responsibilities

| File | Responsibility |
| --- | --- |
| `README.md` | Human repository entrypoint and current implementation status |
| `SECURITY.md` | Security reporting and supported release policy |
| `CONTRIBUTING.md` | Contribution workflow and validation entrypoints |
| `CHANGELOG.md` | Repository release history |
| `NOTICE.md` | Attribution and legal notices |
| `REUSE.toml` | Repository licensing metadata configuration |
| `pyproject.toml` | Root Python tooling workspace and `koa` developer CLI |
| `uv.lock` | Reproducible Python tooling dependency lock |
| `Cargo.toml` | Rust workspace membership for host-privileged code |
| `Cargo.lock` | Reproducible Rust dependency lock |
| `rust-toolchain.toml` | Admitted Rust toolchain channel and components |
| `.pre-commit-config.yaml` | Local deterministic validation hooks |

## 5. `.koa/` Control Files

`file-architecture.lock.json` is a machine-readable projection of this documentation series. It contains path classes and hashes but does not override this normative document. `path-ownership.json` assigns one owner to every structural root. `dependency-rules.json` defines allowed import directions. `generated-paths.json` lists generated roots and manual-edit prohibitions. `runtime-paths.json` maps repository payloads to installed paths. `source-pins.json` aggregates independently versioned source references without replacing the individual integration locks.

## 6. CI Boundary

The workflow files are orchestration only. Reusable logic SHALL be stored under `ci/` or `tools/`, not embedded as large shell programs inside workflow YAML. Release workflows SHALL call the same local commands used by developers and SHALL NOT contain hidden release logic.
