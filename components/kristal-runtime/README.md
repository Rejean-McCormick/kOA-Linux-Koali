# Kristal Runtime

> **Kristal v6 baseline (2026-10-01):** the canonical structured artifact is `kristal_state` (`schema_version: 6.0`) pinned to standard `6.0.0` and `kristal.v6:jcs-rfc8785`. Exact schemas and the consumer lock live under `docs/contracts/`. Interaction Kernel Kristal boundary profiles are pinned at `2.0.0`. The historical `kristal_artifact` wrapper remains compatibility-only. `record_role` and `actionability` are preserved as data and never transfer execution authority.


This package provides the bounded startup surface for the kOA Kristal Runtime.
It owns configuration validation, bootstrap state, health/readiness projection,
and machine-readable receipts for Runtime Pack verification, activation,
rollback, and failure.

The component resolves Kristal identity from canonical epistemic content and
tracks verified Runtime Pack lifecycle state. It does not implement workflow
state, application databases, policy authority, resource scheduling, host
privilege, external AI, release-channel ownership, or direct writes to another
component's authoritative state.

## Contract

- Component ID: `kristal_runtime`
- Contract: `docs/contracts/components/kristal-runtime.component.json`
- Contract version: `1.0.0`
- Accepted release channel: `knowledge`
- Runtime Pack schema: `docs/contracts/artifact-contracts/runtime-pack.schema.json`
- Kristal artifact schema: `docs/contracts/artifact-contracts/kristal-artifact.schema.json`

Activation is never inferred from package validity alone. A candidate remains
inactive until schema, identity, digest, provenance, trust when required,
compatibility, release-channel, downgrade/substitution, authorization, resource,
and evidence preconditions have resolved. The previous known-good compatible
Runtime Pack remains available until a successful atomic transition completes.

## Commands

```console
koa-kristal-runtime check-config
koa-kristal-runtime health
koa-kristal-runtime health --assume-local-prerequisites-ready
```

The readiness assumption flag is a development-only probe input. It does not
create authorization, a resource grant, trust, release-channel membership, or
an activation claim.

Configuration uses the `KOA_KRISTAL_RUNTIME_` prefix. Unknown prefixed variables
are rejected. Configuration contains references and implementation settings,
never raw credentials, signatures, artifact content, or policy decisions.

## Health and degradation

Health reports local process, state, active-record, and receipt-path checks.
Readiness additionally requires explicit profile membership, artifact-contract
resolution, knowledge-channel resolution, interface compatibility, and the
applicable external authority observations. Missing authority blocks only the
capabilities that require it; it never expands authority or activates a
substitute.

Receipts are deterministic canonical JSON projections. They are evidence of a
Kristal Runtime transition, not credentials and not evidence-custody ownership.
