# Audit Broker

The Audit Broker is the kOA component responsible for bounded audit-record custody, selective evidence disclosure, access and disclosure receipts, retention state, and chain-of-custody records.

It does **not** own source-component state, identity, authorization policy, consent policy, privilege, resource allocation, release activation, publication authority, test definitions, or evidence-validity decisions.

## Current implementation

The current component is no longer limited to bootstrap scaffolding. The repository snapshot includes:

- domain models for audit events, evidence scope, redaction, and retention policy;
- application use cases for append, query, disclosure/export, and retention actions;
- explicit ports for the event store, identity context, policy decisions, and clock;
- SQLite and PostgreSQL event-store adapters plus identity, governance, journal-export, and clock adapters;
- bounded API models and routes;
- the `0001_initial.sql` component-owned migration;
- packaging metadata;
- unit, contract, failure, and integration tests.

Bootstrap, health, configuration, and CLI probes remain deliberately bounded and do not by themselves imply that every production deployment path has been qualified. The component must still be activated through the applicable profile, dependency, storage, recovery, and release gates.

## Runtime contract

The component identity is `audit_broker`; the active component contract is `contracts/components/audit-broker.component.json` version `1.0.0`.

Version identifiers are currently separate repository fields: `component.toml` and the Python package identify the implementation as `0.1.0`, while the component contract, public interfaces, and packaging payload use `1.0.0`. This README records those values without treating them as interchangeable lifecycle claims. Renumbering or unifying them requires an explicit versioning decision.

Startup validates configuration and the declared dependency states before exposing readiness. The startup preconditions are:

1. configuration is valid;
2. supported schema and interface versions are selected;
3. Identity and Trust is available;
4. the record store is available;
5. retention policy references are resolvable;
6. a Resource Governor envelope is available.

The Governance Policy Runtime path may be explicitly degraded for ingestion-only operation, but policy-gated disclosures remain unavailable.

## Configuration

Configuration is read from environment variables with the `KOA_AUDIT_BROKER_` prefix. No secret value is accepted by this package.

| Variable | Default | Meaning |
| --- | --- | --- |
| `COMPONENT_ID` | `audit_broker` | Fixed component identity; other values are rejected. |
| `CONTRACT_VERSION` | `1.0.0` | Active component contract version. |
| `INTERFACE_VERSION` | `1.0.0` | Public interface version. |
| `SERVICE_IDENTITY` | `audit_broker` | Component-scoped service identity. |
| `UNIX_SOCKET_PATH` | `/run/koa/audit-broker/audit-broker.sock` | Local service socket path. |
| `STATE_DIRECTORY` | `/var/lib/koa/audit-broker` | Audit Broker-owned persistent state root. |
| `RUNTIME_DIRECTORY` | `/run/koa/audit-broker` | Runtime state root. |
| `MAX_INGESTION_QUEUE_DEPTH` | `4096` | Hard bound for ingestion work. |
| `MAX_QUERY_QUEUE_DEPTH` | `256` | Hard bound for query work. |
| `MAX_DISCLOSURE_QUEUE_DEPTH` | `128` | Hard bound for disclosure work. |
| `STORAGE_WARNING_PERCENT` | `80` | Capacity-warning threshold. |
| `STORAGE_READ_ONLY_PERCENT` | `95` | Threshold at which integrity-preserving read-only mode is required. |
| `RETENTION_POLICY_REFS` | empty | Comma-separated canonical retention-policy references. |
| `LAST_RECOVERY_POINT` | empty | Optional non-sensitive recovery-point reference. |

Paths must be absolute and queue or capacity limits must remain positive and ordered.

## CLI

From an installed package:

```text
python -m koa_audit_broker check-config
python -m koa_audit_broker health
```

`health` reports a bounded JSON document. It never includes audit record content, protected identifiers, secrets, evidence payloads, or policy details.

## Receipt boundary

`receipts.py` creates receipts only for transitions owned by the Audit Broker, such as ingestion acceptance or rejection, disclosure access outcomes, retention changes, invalidation, and recovery. It never fabricates receipts for policy decisions, source-component commits, privileged operations, publication commits, or release activation.

Receipt identifiers are deterministic for a stable request, transition, correlation identifier, terminal outcome, and timestamp. Protected evidence remains referenced separately and is never embedded in ordinary receipt content.
