<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-034",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/architecture-patterns.contract.json",
    "02-system/23-code-and-filesystem-architecture.md",
    "contracts/system.contract.json#/architecture_patterns",
    "contracts/artifact-classes.contract.json",
    "contracts/terminology.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/dead-letter-record.schema.json",
    "contracts/artifact-contracts/distributed-workflow.schema.json",
    "contracts/artifact-contracts/large-payload-reference.schema.json",
    "contracts/artifact-contracts/experience-view-adapter.schema.json",
    "contracts/artifact-contracts/cqrs-projection.schema.json",
    "contracts/artifact-contracts/cache-policy.schema.json"
  ],
  "decision_ids": [
    "DEC-RES-001",
    "DEC-MSG-001",
    "DEC-WF-001",
    "DEC-PAYLOAD-001",
    "DEC-BFF-001",
    "DEC-CQRS-001",
    "DEC-CACHE-001"
  ],
  "requirement_ids": [
    "REQ-PATTERN-001",
    "REQ-PATTERN-002",
    "REQ-PATTERN-003",
    "REQ-PATTERN-004",
    "REQ-PATTERN-005",
    "REQ-PATTERN-006",
    "REQ-PATTERN-007",
    "REQ-PATTERN-008",
    "REQ-PATTERN-009",
    "REQ-PATTERN-010",
    "REQ-PATTERN-011",
    "REQ-PATTERN-012",
    "REQ-PATTERN-013",
    "REQ-PATTERN-014",
    "REQ-PATTERN-015",
    "REQ-PATTERN-016",
    "REQ-PATTERN-017",
    "REQ-PATTERN-018",
    "REQ-PATTERN-019",
    "REQ-PATTERN-020",
    "REQ-PATTERN-021",
    "REQ-PATTERN-022",
    "REQ-PATTERN-023",
    "REQ-PATTERN-024",
    "REQ-PATTERN-025",
    "REQ-PATTERN-026",
    "REQ-PATTERN-027",
    "REQ-PATTERN-028",
    "REQ-PATTERN-029",
    "REQ-PATTERN-030",
    "REQ-PATTERN-031",
    "REQ-PATTERN-032",
    "REQ-PATTERN-033",
    "REQ-PATTERN-034",
    "REQ-PATTERN-035",
    "REQ-PATTERN-036",
    "REQ-PATTERN-037",
    "REQ-PATTERN-038",
    "REQ-PATTERN-039",
    "REQ-PATTERN-040",
    "REQ-PATTERN-041",
    "REQ-PATTERN-042"
  ],
  "lock_ids": [
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-PAYLOAD-001",
    "LOCK-BFF-001",
    "LOCK-CQRS-001",
    "LOCK-CACHE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-SYS-007",
    "DOC-SYS-016",
    "DOC-SYS-020",
    "DOC-SYS-021",
    "DOC-SYS-022"
  ],
  "tags": [
    "architecture-patterns",
    "resilience",
    "messaging",
    "distributed-workflow",
    "large-payload",
    "experience-view-adapter",
    "cqrs",
    "cache-aside"
  ]
}
KOA:DOC-META:END -->

# Architecture Patterns

## 1. Purpose

This document defines the final system-level application of seven architecture patterns: circuit breaker, dead-letter handling, distributed workflow, large payload reference, experience view adapter, command-query separation, and cache-aside.

This document follows the code and filesystem architecture series (`DOC-SYS-023` through `DOC-SYS-033`) and therefore owns `DOC-SYS-034`.

The canonical policy is `contracts/architecture-patterns.contract.json`. The pattern contract is complete now. Individual components activate a pattern only when its declared applicability condition is true, but they do not defer defining its authority, lifecycle, failure, operational, or conformance behavior.

## 2. Global rule

A pattern optimizes resilience, delivery, or presentation. It never changes the component that owns authoritative data, authorization, policy, or a business transition.

- **REQ-PATTERN-001 — MUST** Every activated pattern use a validated artifact class registered in `contracts/artifact-classes.contract.json`.
- **REQ-PATTERN-002 — MUST** Pattern activation preserve the canonical owner of every command, datum, policy decision, and receipt.
- **REQ-PATTERN-003 — MUST NOT** A cache, projection, adapter, queue, or workflow coordinator become an undeclared source of authority.
- **REQ-PATTERN-004 — MUST** Pattern failure preserve independent local and offline capabilities.
- **REQ-PATTERN-005 — MUST** Every pattern expose enough state and evidence for conformance and incident review.

## 3. Circuit breaker

A circuit breaker is required around fallible network or process-boundary calls when repeated failure could exhaust resources or cascade. It has `closed`, `open`, and `half_open` states.

- **REQ-PATTERN-006 — MUST** Timeouts and a total request budget bound every attempt before retry is considered.
- **REQ-PATTERN-007 — MUST** The breaker open after the declared failure threshold and fail fast for the declared open period.
- **REQ-PATTERN-008 — MUST** Half-open recovery use bounded probes and bounded concurrency.
- **REQ-PATTERN-009 — MUST NOT** An open circuit report authoritative success.
- **REQ-PATTERN-010 — MUST** A degraded response identify whether it is unavailable, queued, empty and non-authoritative, or stale and labeled.
- **REQ-PATTERN-011 — MUST** Manual breaker override be authorized, time-bounded, audited, and receipted.

## 4. Dead-letter handling

Asynchronous work that cannot be silently lost uses bounded retry followed by quarantine.

- **REQ-PATTERN-012 — MUST** Consumers distinguish transient, permanent, authorization, policy, compatibility, and corruption failures.
- **REQ-PATTERN-013 — MUST** Retry be bounded and use backoff with jitter for transient failures.
- **REQ-PATTERN-014 — MUST** Known permanent failures enter quarantine without wasteful repeated execution.
- **REQ-PATTERN-015 — MUST NOT** A failed message or job be silently deleted when its contract requires preservation.
- **REQ-PATTERN-016 — MUST** Redrive require compatibility verification and explicit authorization.
- **REQ-PATTERN-017 — MUST** Discard require explicit authorization and a closure receipt.
- **REQ-PATTERN-018 — MUST** A non-empty dead-letter set trigger an operational signal.

## 5. Distributed workflow

A transition spanning multiple authoritative owners uses an explicit distributed workflow rather than a global cross-owner lock. Orchestration is the default. Choreography is permitted only with complete causal tracing and cycle prevention.

- **REQ-PATTERN-019 — MUST** Every step identify its owner, local transaction, timeout, idempotency behavior, state, and evidence.
- **REQ-PATTERN-020 — MUST** Intermediate externally visible state be labeled pending until the required owners complete acceptance.
- **REQ-PATTERN-021 — MUST** Every completed reversible step define compensation.
- **REQ-PATTERN-022 — MUST** Every irreversible step declare forward repair and human intervention behavior.
- **REQ-PATTERN-023 — MUST NOT** Partial success be hidden or represented as final success.
- **REQ-PATTERN-024 — MUST** The workflow end in a completed, compensated, failed-closed, cancelled, or forward-repair terminal state with evidence.

The UCKK publication and import flows are distributed workflows because local kOA authority and remote UCKK authority remain separate.

## 6. Large payload reference

Large media and objects remain in owner-controlled storage. General messages carry a bounded reference.

- **REQ-PATTERN-025 — MUST** Payloads above the active profile inline limit use a large payload reference.
- **REQ-PATTERN-026 — MUST** The reference carry owner identity, object identity and version, media type, byte length, digest, audience, capability, and expiry.
- **REQ-PATTERN-027 — MUST** Consumers verify the digest before processing.
- **REQ-PATTERN-028 — MUST NOT** The reference embed a bearer secret or an unbounded public locator.
- **REQ-PATTERN-029 — MUST** The payload remain retained until its workflow reaches a terminal state.
- **REQ-PATTERN-030 — MUST** Orphan detection and cleanup ownership be declared.

## 7. Experience view adapter

The kOA form of Backend for Frontend is an **experience view adapter**. It belongs to a module or experience integration package and shapes data for one declared surface.

- **REQ-PATTERN-031 — MUST** The adapter contain presentation shaping, bounded aggregation, and delegated commands only.
- **REQ-PATTERN-032 — MUST NOT** The adapter own business rules, authoritative storage, authorization decisions, or cross-owner transaction logic.
- **REQ-PATTERN-033 — MUST** Every owner re-evaluate authorization for its query or delegated command.
- **REQ-PATTERN-034 — MUST** Fan-out, timeouts, circuit policies, payload sizes, and partial view behavior be bounded.
- **REQ-PATTERN-035 — MUST NOT** One universal adapter erase module or subsystem boundaries.

kOA Spaces may render results from experience view adapters but remains a non-authoritative presentation subsystem.

## 8. Command-query separation

When a component creates a read-optimized model distinct from its write model, the read model is a CQRS projection.

- **REQ-PATTERN-036 — MUST** Commands reach the authoritative owner and never the projection store.
- **REQ-PATTERN-037 — MUST** The projection declare its source feed, checkpoint, rebuild method, maximum staleness, and deletion propagation.
- **REQ-PATTERN-038 — MUST NOT** A stale projection authorize a fresh privileged or irreversible action.
- **REQ-PATTERN-039 — MUST** Projection lag and rebuild state be observable.

## 9. Cache-aside

A cache-aside implementation uses a validated cache policy.

- **REQ-PATTERN-040 — MUST** A cache declare its source of truth, key scope, TTL, invalidation, negative caching, stampede protection, staleness, security, and failure behavior.
- **REQ-PATTERN-041 — MUST** Cache keys include tenant and authority-domain boundaries, and an empty cache remain safe.
- **REQ-PATTERN-042 — MUST NOT** A cache become authority, receive owner writes in place of the owner store, or serve stale data for fresh authorization without an explicit stricter policy.

## 10. Required compositions

| Situation | Required composition |
| --- | --- |
| Fallible remote call | timeout budget, backoff with jitter, circuit breaker |
| Asynchronous work that cannot be lost | idempotency, bounded retry, dead-letter handling |
| Multi-owner transition | distributed workflow, idempotency, outbox where a local commit emits work, receipts |
| Large asynchronous media | large payload reference, digest verification, dead-letter handling |
| Experience aggregation | experience view adapter, bounded fan-out, circuit policy, optional CQRS projection and cache policy |
| UCKK publication or import | distributed workflow, large payload reference, circuit breaker, dead-letter handling |

## 11. Prohibited shortcuts

The following are prohibited:

- infinite retries;
- raising timeouts as the primary recovery strategy;
- silent message loss;
- unmonitored quarantine;
- global locks across independent authorities;
- presenting pending state as complete;
- embedding large media in general event streams;
- business logic in an experience adapter;
- commands against projection stores;
- cache-only writes;
- unbounded cache lifetime;
- fresh authorization based on stale projection or cache state.

## Koali product UI modularity

This document is interpreted with the Koali product-interface portability rule:

- each independently packaged product owns its user interface and remains independently operable when its declared standalone mode is supported;
- shared Koali shell and design-system code is reusable presentation infrastructure, not a mandatory product runtime and not a source of business authority;
- an integrated composition host discovers installed and admitted product manifests dynamically rather than hard-coding a mandatory product list;
- a surface profile is a projection of the same product routes, capabilities, commands, and contextual views, not a separately implemented frontend;
- removing one product removes only that product's admitted presentation contributions and SHALL NOT require source changes to unrelated products;
- ordinary shell behavior SHALL NOT require private UI imports from another product; cross-product journeys use explicit public routes, commands, capabilities, or integration contracts.

## 12. Senior Architecture Patterns reference alignment

This subsection is an explanatory cross-reference to the separate **Senior Architecture Patterns** catalog used during architectural review. It does not create additional requirements or override the canonical policy in `contracts/architecture-patterns.contract.json`.

| Senior Architecture Patterns name | kOA-Linux application | Alignment |
| --- | --- | --- |
| Circuit Breaker | Canonical circuit policy for qualifying network/process boundaries | Direct |
| Exponential Backoff + Jitter | Bounded transient-failure retry; full jitter is part of the canonical resilience envelope | Direct |
| Graceful Degradation | System-wide safe-degradation rule preserves independent local/offline capabilities and labels partial/unavailable state | Direct |
| Rate Limiting / Throttling | Resource Governor admission/envelopes and bounded expensive/external work | Selective |
| Timeout Budgets | Attempt and total-request budgets bound fallible remote work before retry | Direct |
| Hexagonal Architecture / Ports & Adapters | Internal components separate domain/application logic from ports and concrete adapters | Structural alignment |
| Anti-Corruption Layer | External and independent-system integrations translate at explicit adapter/boundary layers rather than leaking foreign authority models inward | Selective |
| Backend for Frontend (BFF) | Implemented as the narrower **experience view adapter**, which may shape/aggregate presentation data but owns no business authority | Direct equivalent |
| CQRS | Read-optimized projections are explicitly non-authoritative and rebuildable; commands remain owner-directed | Direct |
| Saga | Implemented as an explicit **distributed workflow** with owner-local transactions, compensation, forward repair, terminal states, and evidence | Direct equivalent |
| Idempotency | Required for replay-safe workflow steps and asynchronous/control operations where semantics permit | Direct |
| Transactional Outbox | Used when a local authoritative commit must emit asynchronous work | Selective composition |
| Cache-Aside / Lazy Loading | Canonical cache policy with owner source of truth, TTL, invalidation, staleness bounds, and safe empty-cache behavior | Direct |
| Dead-Letter Queue (DLQ) | Canonical dead-letter/quarantine behavior with bounded retry, alerting, authorized redrive, and receipted discard | Direct |
| Claim Check | Implemented as **large payload reference**: owner-controlled object storage plus bounded reference and digest verification | Direct equivalent |
| Blue-Green Deployment | Supported as a service-update strategy where the active profile/deployment model makes it appropriate | Selective |
| Canary Release | Supported as a bounded service-update strategy rather than a universal endpoint requirement | Selective |
| Immutable Infrastructure | Signed immutable OS/system-image architecture and controlled release activation | Direct |
| Distributed Tracing | Correlation/causal tracing across distributed boundaries and receipts | Selective |
| Health Check API | Explicit health/readiness contracts and per-component health implementations | Direct |
| Metrics and Alerting | Operational observability and alerts for breakers, queues, workflows, projections, caches, readiness, and SLO-sensitive failure | Direct |

The following catalog patterns are **not system-wide kOA-Linux defaults merely because they exist in the reference**: Event Sourcing, Sharding/Partitioning, Pub/Sub, CDN offloading, Sidecar or service-mesh architecture, Cell-Based Architecture, Modular Monolith, and Data Mesh. They require a separate applicability decision if a concrete subsystem needs them.

The important distinction is that kOA-Linux adopts patterns **by applicability and authority boundary**, not by checklist. A pattern may improve resilience, delivery, deployment, or presentation, but it does not transfer canonical ownership of data, authorization, policy, or business transitions.

