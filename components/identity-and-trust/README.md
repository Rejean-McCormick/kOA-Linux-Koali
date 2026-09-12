# Identity and Trust

Identity and Trust is the kOA-Linux component that establishes bounded identity and trust evidence for human, service, component-instance, node, device, workspace, tenant, organization, integration, artifact-signer, and recovery-operator subjects.

The component authenticates and verifies. It does **not** authorize application actions, governance decisions, publication, resource admission, release activation, or host mutation.

## This bundle

This initial bundle provides:

- package and component metadata;
- strict, secret-free configuration loading;
- deterministic bootstrap state;
- bounded liveness, health, and readiness evaluation;
- immutable identity-and-trust receipt envelopes;
- a local diagnostic CLI.

Domain records, application use cases, ports, adapters, APIs, migrations, packaging payloads, and service integration are owned by later bundles.

## Configuration

Configuration can be loaded from a TOML file and overridden by an explicit environment allowlist. The component rejects unknown `KOA_IDENTITY_TRUST_*` variables so misspelled security settings do not silently fall back.

Supported environment variables:

| Variable | Meaning |
| --- | --- |
| `KOA_IDENTITY_TRUST_INSTANCE_ID` | Stable service-instance identifier. |
| `KOA_IDENTITY_TRUST_ENVIRONMENT` | Deployment environment identifier. |
| `KOA_IDENTITY_TRUST_PROFILE` | Canonical base profile. |
| `KOA_IDENTITY_TRUST_CONFIG_PATH` | Component configuration path. |
| `KOA_IDENTITY_TRUST_STATE_ROOT` | Component-owned state root. |
| `KOA_IDENTITY_TRUST_RUNTIME_ROOT` | Ephemeral runtime root. |
| `KOA_IDENTITY_TRUST_SOCKET_PATH` | Local Unix-socket path. |
| `KOA_IDENTITY_TRUST_RECEIPT_MODE` | `durable`, `buffered`, or `unavailable`. |
| `KOA_IDENTITY_TRUST_RECEIPT_BUFFER_LIMIT` | Bounded local receipt capacity. |
| `KOA_IDENTITY_TRUST_KEY_PROVIDER_MODE` | `available`, `degraded`, or `unavailable`. |
| `KOA_IDENTITY_TRUST_REVOCATION_MAX_AGE_SECONDS` | Maximum admitted revocation age. |
| `KOA_IDENTITY_TRUST_OFFLINE` | Explicit offline mode. |

No private key, credential secret, factor value, bearer token, or password is accepted by this configuration surface.

## Local diagnostics

With the package source directory on `PYTHONPATH`:

```bash
python -m koa_identity_and_trust describe
python -m koa_identity_and_trust check-config --config /etc/koa/components/identity-and-trust/config.toml
python -m koa_identity_and_trust health --config /etc/koa/components/identity-and-trust/config.toml
python -m koa_identity_and_trust readiness --config /etc/koa/components/identity-and-trust/config.toml
```

The frequent probes are bounded local reads. They do not call remote identity providers, refresh trust, perform migrations, issue credentials, activate roots, or mutate authoritative state.

## Health semantics

Liveness only states whether the local process can make bounded progress. Health evaluates the component-local store, protected-key provider, trust-context structure, and receipt path. Readiness additionally evaluates required roots, revocation freshness, supported algorithms, issuers, and contract/schema compatibility.

A missing optional or online-only capability degrades only the affected capability. An indeterminate identity or trust condition never becomes authorization and never broadens trust.

## Receipt semantics

Critical identity and trust transitions require machine-readable receipts. Receipt identifiers are deterministic for a fixed canonical envelope, enabling idempotent retry detection. Ordinary receipt views exclude evidence details and reject secret-bearing context keys.

The Audit Broker may collect and disclose these receipts, but it does not become the owner of identity, credential, trust-root, revocation, or verification state.


## Common OIDC federation binding

The component supports the ecosystem profile `koa-common-oidc-v1` through a local external identity binding. The external key is the exact OIDC `issuer + subject (sub)` pair, scoped by provider, tenant and environment, and it resolves to a stable local `identity_id`. Email and display name are not federation keys.

The binding is internal identity evidence supporting the existing authentication boundary. It does not create owner-application sessions, propagate roles, share passwords, or grant business authorization. Machine/service authentication remains separate from human OIDC SSO.
