# Engineering Profile

> Generated deterministically by RepoSurveyor from the current local project files. 
> This is a scale/engineering-surface characterization, not a quality score or release-readiness claim.

## Engineering Footprint

- **1,664** files in the active engineering surface
- **737** active source files
- **520** production source files
- **217** test source files
- **599** active documentation files
- **110,444** production nonblank physical source lines
- **32,877** test nonblank physical source lines
- **17** migration-related files
- **81** schema-related files
- **1,280** statically detected test declarations *(not executed-test count)*

## Language Footprint

| Language | Nonblank physical source lines |
|---|---:|
| Python | 130,401 |
| Rust | 12,165 |
| SQL | 547 |
| PowerShell | 130 |
| Shell | 78 |

Method: RepoSurveyor extension classification + nonblank physical line count. Comments are included in this fallback measure.

## Structural Surface

| Area | Files | Source files | Docs | Nonblank source lines |
|---|---:|---:|---:|---:|
| `components` | 371 | 326 | 20 | 58,980 |
| `integrations` | 257 | 127 | 11 | 20,145 |
| `host` | 100 | 34 | 2 | 10,015 |
| `operations` | 41 | 39 | 1 | 9,981 |
| `assembly` | 40 | 38 | 1 | 8,836 |
| `interfaces` | 28 | 12 | 1 | 8,583 |
| `tests` | 88 | 82 | 1 | 8,059 |
| `docs` | 545 | 28 | 545 | 7,715 |
| `tools` | 34 | 33 | 1 | 6,197 |
| `ci` | 16 | 10 | 1 | 2,337 |
| `release` | 21 | 5 | 2 | 2,200 |
| `dev` | 17 | 3 | 1 | 273 |
| `packaging` | 38 | 0 | 1 | 0 |
| `profiles` | 28 | 0 | 2 | 0 |
| `(root)` | 15 | 0 | 5 | 0 |

## Complexity

- Functions analyzed by Lizard: **7,629**
- Median cyclomatic complexity (CCN): **2**
- 95th percentile CCN: **27.6**
- Maximum CCN: **429**
- Functions with CCN > 15: **732**
- Method: Lizard XML function measure / CCN column

## Verification Surface

- Static test declarations: **1,280** — static language-aware declaration scan; not collected/executed/passed tests
- No supported existing coverage report detected.

## Detected Engineering Controls

- **Automated tests** — configured/detected via `assembly/pyproject.toml`, `components/audit-broker/pyproject.toml`, `components/governance-policy-runtime/pyproject.toml` (+11 more)
- **CI configuration** — configured/detected via `.github/workflows/components.yml`, `.github/workflows/contracts.yml`, `.github/workflows/documentation.yml` (+4 more)
- **Containerization** — configured/detected via `dev/containers/compose.yaml`, `dev/local-services/compose.yaml`
- **Linting** — configured/detected via `assembly/pyproject.toml`, `components/audit-broker/pyproject.toml`, `components/governance-policy-runtime/pyproject.toml` (+8 more)
- **Machine-readable schemas** — configured/detected via `docs/schemas/ai-context-package.schema.json`, `docs/schemas/ai-navigation.contract.schema.json`, `docs/schemas/architecture-patterns.contract.schema.json` (+17 more)
- **Pre-commit hooks** — configured/detected via `.pre-commit-config.yaml`
- **Static typing** — configured/detected via `components/audit-broker/pyproject.toml`, `components/publication-gateway/pyproject.toml`, `integrations/semantik-architect/adapter/pyproject.toml` (+2 more)

## Analysis Scope

- Active surface: **1,664** files
- Excluded `dependency-lock`: **2** files
- Excluded `diagnostic-evidence`: **252** files
- Excluded `local-ignore`: **1** files
- Pruned dependency/cache/generated directories: **96**

## Measurement Notes

- Generated: `2026-09-16T15:18:21.447228+00:00`
- RepoSurveyor survey schema: `1.0`
- Source model: current local filesystem; Git state/history is intentionally irrelevant.
- Archive copies, diagnostics, dependency caches, generated output, lockfiles and private local configuration are excluded from the active engineering surface.
- Tool/configuration presence is evidence of configured engineering infrastructure, not evidence that its latest run passed.
- Static test declarations are not the same as collected, executed or passing tests.
- Existing coverage reports are not treated as freshly measured coverage.
- RepoSurveyor never converts these measurements into a synthetic quality, maturity or architecture score.
