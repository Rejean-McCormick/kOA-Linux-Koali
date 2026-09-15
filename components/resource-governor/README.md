# Resource Governor

Resource Governor is the kOA-Linux component authority for deterministic resource-envelope resolution, workload admission, allocation, queueing, scheduling, throttling, suspension, and bounded process-control decisions.

Resource availability is **not** business authorization. This component does not decide identity, consent, disclosure, privilege, publication, governed exceptions, or application-domain mutations. A workload that requires both policy authorization and resource admission proceeds only after the two independent authorities pass.

## Current implementation

The current Resource Governor implementation includes:

- domain models for resource claims, envelopes, admission decisions, and degradation state;
- application use cases for admission, envelope application, degradation, usage reconciliation, and workload restoration;
- explicit ports for profile resolution, usage probes, Node Agent execution, audit delivery, and time;
- profile-file, procfs, systemd-usage, Node Agent, audit, and clock adapters;
- bounded API models and routes;
- packaging metadata;
- unit, contract, failure, and integration tests.

There is intentionally no SQL migration for the current adapter bundle. Durable allocation/queue persistence remains a separately inventoried future persistence boundary and must not be inferred from the presence of runtime adapters. Bootstrap and local diagnostics remain observational and do not themselves admit work or mutate host controls.

## Configuration

Configuration is loaded from an optional TOML file and an explicit environment allowlist. Unknown `KOA_RESOURCE_GOVERNOR_*` variables are rejected so misspelled controls cannot silently fall back.

Supported environment variables:

| Variable | Meaning |
| --- | --- |
| `KOA_RESOURCE_GOVERNOR_INSTANCE_ID` | Stable component-instance identifier. |
| `KOA_RESOURCE_GOVERNOR_ENVIRONMENT` | Deployment environment identifier. |
| `KOA_RESOURCE_GOVERNOR_PROFILE` | Canonical primary-profile identifier. |
| `KOA_RESOURCE_GOVERNOR_CONFIG_PATH` | Absolute TOML configuration path. |
| `KOA_RESOURCE_GOVERNOR_STATE_ROOT` | Component-owned persistent state root. |
| `KOA_RESOURCE_GOVERNOR_RUNTIME_ROOT` | Ephemeral runtime root. |
| `KOA_RESOURCE_GOVERNOR_SOCKET_PATH` | Local Unix-socket path. |
| `KOA_RESOURCE_GOVERNOR_ENFORCEMENT_ADAPTER_MODE` | `available`, `degraded`, or `unavailable`. |
| `KOA_RESOURCE_GOVERNOR_OBSERVATION_SOURCE_MODE` | `available`, `stale`, or `unavailable`. |
| `KOA_RESOURCE_GOVERNOR_QUEUE_BACKEND_MODE` | `durable`, `volatile`, or `unavailable`. |
| `KOA_RESOURCE_GOVERNOR_RECEIPT_MODE` | `durable`, `buffered`, or `unavailable`. |
| `KOA_RESOURCE_GOVERNOR_RECEIPT_BUFFER_LIMIT` | Bounded local receipt capacity. |
| `KOA_RESOURCE_GOVERNOR_QUEUE_CAPACITY` | Finite queue capacity; never an active envelope limit. |
| `KOA_RESOURCE_GOVERNOR_OBSERVATION_MAX_AGE_SECONDS` | Maximum admitted age of observations. |
| `KOA_RESOURCE_GOVERNOR_ALLOW_LOW_RISK_WITHOUT_OBSERVATION` | Permit only explicitly declared low-risk work during observation degradation. |
| `KOA_RESOURCE_GOVERNOR_RECONCILIATION_REQUIRED` | Require allocation and execution reconciliation before readiness. |

The configuration surface accepts no workload payload, policy grant, secret, credential, bearer token, host-wide privilege, CPU or memory allowance, or active-envelope replacement. Actual limits remain owned by verified resource-envelope artifacts and the active profile.

## Local diagnostics

With the package source directory on `PYTHONPATH`:

```bash
python -m koa_resource_governor describe
python -m koa_resource_governor check-config --config /etc/koa/components/resource-governor/config.toml
python -m koa_resource_governor health --config /etc/koa/components/resource-governor/config.toml
python -m koa_resource_governor readiness --config /etc/koa/components/resource-governor/config.toml
```

The probes are bounded local reads. They do not activate an envelope, admit work, create allocations, dequeue jobs, alter operating-system controls, or mutate authoritative state.

## Health and readiness

Liveness states only that the process can make bounded local progress. Health evaluates the declared runtime, profile, envelope, enforcement, observation, queue, reconciliation, pressure, and receipt signals. Readiness is withheld until the runtime implementation, active profile, active envelopes, enforcement adapter, observation source, and allocation reconciliation are verified.

Pressure can leave the component alive while capabilities become degraded or blocked. Unknown or missing enforcement never becomes a zero-usage observation and never authorizes unconstrained work. Existing independently verified controls may remain active while new affected work is blocked.

## Receipt behavior

Critical resource transitions use immutable decision receipts. Resource-envelope activation, governed override, forced termination, emergency degradation, rollback, and recovery fail closed when their required durable receipt path is unavailable. Receipt identifiers are deterministic for the same canonical input, supporting idempotent retries without duplicate authoritative effects.

Receipts contain resource metadata, reason codes, contract references, and traceability. They reject secret-bearing fields and workload business payloads. The Audit Broker may retain or disclose receipts, but it does not become the owner of resource allocations, queues, active envelopes, or application state.
