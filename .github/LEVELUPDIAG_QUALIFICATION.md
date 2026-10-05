# GitHub-hosted LevelUpDiag qualification

This workflow adds a correlated GitHub-hosted qualification layer without
replacing the existing kOA-Linux workflows.

## Hosted gate

`.github/workflows/levelupdiag.yml` runs the LevelUpDiag-Koali `validation`
campaign (N00-N10) against the exact kOA-Linux commit that triggered the run.

The diagnostic repository is pinned to:

`1faa39727347fe91935894ccfff456b09d956feb`

The runner is Ubuntu 24.04 with Python 3.13, UV, the repository-declared Rust
1.85.1 toolchain, Cargo and the native C compiler. The Python environment is
synchronized with `uv sync --frozen --all-groups`; Cargo dependencies are
prefetched from `Cargo.lock` before the diagnostic campaign.

## Evidence

The workflow uploads:

- the complete `.levelupdiag/` evidence tree;
- `qualification-metadata/components.txt`;
- the exact kOA-Linux and LevelUpDiag Git SHAs;
- Python / UV / Rust / Cargo versions;
- SHA-256 of `uv.lock` and `Cargo.lock`.

## Deliberately excluded from the hosted gate

N12 (`koali-system`) is a **live Koali product-system** test. It requires fresh
Koali state, the Shell HTTP endpoint and linked product runtimes. A clean
GitHub-hosted worker must not manufacture those conditions.

N13 (`store`) contains source checks plus optional real Linux desktop-session
probes. A headless hosted worker is not a substitute for the documented VM
acceptance scenario.

N11 (`delivery`) requires an explicit delivery target and belongs to a release
artifact workflow, not the ordinary source-validation workflow.

These scopes should remain separate so a green GitHub badge never overclaims
live-system, store-installation, or delivery qualification.
