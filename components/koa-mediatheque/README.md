# kOA Mediatheque

`koa_mediatheque` is the authoritative private local and offline Mediatheque component of kOA-Linux. The current package includes domain models, application use cases, ports, storage/job/publication adapters, API routes, a component-owned SQLite migration, concrete rendition workers, packaging metadata, health/readiness, receipts, and integration/unit/failure/contract tests.

## Authority boundary

The component owns local records, versions, managed-content bindings, classification, rights bindings, provenance, renditions, local lifecycle, import/export history, and coordinated backup/restore state. It does not own UCKK records, remote transport, publication authorization, identity authority, policy decisions, host storage mechanisms, or another component's database.

A shared Mediatheque frame is an interchange contract. It does not create shared identifiers, storage, access control, lifecycle, or authority. UCKK publication and import remain separate directional integrations; reconnection never triggers background bidirectional synchronization.

## Bootstrap behavior

Bootstrap is observational and fail-closed. It does not create directories, initialize SQLite, start workers, accept media, activate restored state, publish content, or mutate authoritative records. Those mutations are implemented behind the component's application, port, adapter, API, migration, and worker layers and must be invoked through their explicit lifecycle boundaries rather than as bootstrap side effects.

The default configuration reports the component as not ready until stores, queues, receipt delivery, local authority, and required runtime adapters have been verified. UCKK unavailability does not make the local Mediatheque unhealthy. Optional rendition and publication work is blocked before local catalog and accepted-content access.

## Configuration

Configuration is read from an optional absolute TOML path and `KOA_MEDIATHEQUE_*` environment overrides. Unknown keys, secret-like keys, relative paths, path traversal, overlapping authoritative roots, and unsupported profiles are rejected.

```toml
[koa_mediatheque]
instance_id = "koa-mediatheque-1"
environment = "production"
profile = "sovereign_offline"
state_root = "/var/lib/koa/mediatheque"
runtime_root = "/run/koa/koa-mediatheque"
socket_path = "/run/koa/sockets/koa-mediatheque.sock"
database_path = "/var/lib/koa/mediatheque/catalog.sqlite3"
content_root = "/var/lib/koa/mediatheque/content"
staging_root = "/var/lib/koa/mediatheque/staging"
quarantine_root = "/var/lib/koa/mediatheque/quarantine"
receipt_root = "/var/lib/koa/mediatheque/receipts"
database_mode = "read_write"
content_mode = "read_write"
integrity_queue_mode = "durable"
rendition_queue_mode = "durable"
publication_queue_mode = "durable"
receipt_mode = "durable"
```

No rights grant, publication decision, consent, remote credential, resource envelope, media content, or secret belongs in this configuration.

## Health and readiness

The seven health dimensions are exactly: database, managed-content root, integrity queue, rendition queue, publication queue, backup checkpoint, and storage pressure. Operational metrics contain counts and byte totals only; health output never includes media payloads or restricted metadata.

Liveness means the diagnostic process can respond. Readiness additionally requires supported contracts, loaded local authority, a durable receipt path, and the required stores, queues, and runtime adapters to be wired and verified.

## Receipts

`create_transition_receipt` emits immutable deterministic decision receipts for the registered component events. Every transition requires a durable receipt path. Receipts carry record or version references, reason codes, traceability, and optional evidence references, but no content payload, secret, remote credential, or restricted metadata.

## Workers

`koa_mediatheque.workers` registers thumbnail, preview, and text-extraction identities without starting work as an import side effect. Concrete worker modules are present in the package and remain bounded Resource Governor-controlled task processors; they never become a second metadata authority.

## Diagnostic CLI

```console
koa-mediatheque describe
koa-mediatheque --config /etc/koa/koa-mediatheque.toml check-config
koa-mediatheque --config /etc/koa/koa-mediatheque.toml health --view operational
koa-mediatheque --config /etc/koa/koa-mediatheque.toml readiness --view public
```

The CLI performs no ingest, deletion, publication, restore activation, worker start, or host mutation.
