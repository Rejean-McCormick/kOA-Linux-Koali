# kOA Node Agent

The kOA Node Agent is the node-local owner of privileged-operation execution state, staging state, activation and recovery execution state, idempotency records, and node-operation receipts. It is a narrow broker, not a general administration service.

The current crate includes domain requests and authorization models, request validation and dispatch, explicit ports, a fixed privileged-operation broker, systemd/mount/network host backends, a bounded Unix-socket transport, packaging metadata, and contract/integration/security tests in addition to bootstrap, health, and receipt primitives. The service remains fail-closed: a production `serve` path is not considered ready until peer authentication, durable idempotency/receipt state, fixed adapter wiring, and the applicable profile/release qualification are configured and verified.

## Authority boundary

The Node Agent may reject a request after final node-local validation. It may not invent or replace:

- caller or signer identity;
- governance authorization;
- profile membership or implementation selection;
- artifact class, manifest, release compatibility, or recovery strategy;
- Resource Governor admission;
- Audit Broker disclosure policy;
- application-component authoritative state.

A control-plane request is never sufficient authority. Root identity is an execution property, not application governance authority.

## Closed public surface

The registered command interfaces are:

- `execute_node_operation`;
- `cancel_node_operation`;
- `acknowledge_recovery_result`.

The registered queries are:

- `get_node_agent_capabilities`;
- `get_node_operation_status`;
- `get_node_agent_health`.

The registered command/query identities are modeled by the crate and constrained to a fixed operation catalog. The privileged broker can validate and dispatch bounded registered operations through fixed backends; it does not expose a shell, arbitrary command runner, generic service-manager, generic file-transfer, package-manager, container, device, or private-key interface. The production socket service remains fail-closed until its authenticated transport and durable runtime wiring are configured.

## Configuration

Configuration is read from an optional absolute TOML path with one `[koa_node_agent]` table and from the closed `KOA_NODE_AGENT_*` environment namespace. Unknown keys and unknown prefixed environment variables are rejected. Secret-like configuration names are prohibited.

The default configuration is intentionally fail-closed:

- no operation class is profile-enabled;
- external authority and verification dependencies are unavailable;
- receipt and idempotency stores are unavailable;
- staging capacity and resource pressure are unknown;
- recovery is unavailable.

Example for local validation only:

```toml
[koa_node_agent]
profile_context_ref = "contracts/profiles/sovereign-linux-node.profile.json"
enabled_operation_classes = ["inspect_node_state"]
identity_verification_mode = "available"
profile_validation_mode = "available"
policy_runtime_mode = "unavailable"
artifact_verification_mode = "unavailable"
resource_envelope_mode = "available"
control_plane_mode = "unavailable"
receipt_store_mode = "durable"
idempotency_store_mode = "durable"
staging_capacity_state = "available"
recovery_path_state = "verified"
resource_pressure_state = "normal"
```

Enabling a class in configuration does not authorize an operation. It only records profile-resolved availability. Runtime request validation remains responsible for identity, policy, expected state, artifacts, compatibility, resource admission, replay protection, timeout, and recovery readiness.

## Health and readiness

Health output is bounded and contains no secrets, private keys, application data, or authority-bearing payloads. It reports the contract-owned fields:

- component state;
- enabled and blocked operation classes;
- active request and operation in the authenticated operational view;
- staging capacity;
- receipt and idempotency store state;
- artifact verification and recovery state;
- resource pressure;
- last successful critical transition time.

Loss of the control plane preserves existing node-local authority. Loss of identity, profile validation, policy, receipt durability, idempotency durability, artifact verification, resource admission, or recovery readiness blocks the affected operation. There is no silent alternate privileged path.

## Receipts

`NodeOperationReceipt` requires the fields declared in the component contract. Successful critical transitions require a durable receipt path. Receipt identifiers are deterministic correlation fingerprints, not signatures or trust proofs; integrity and signing remain conditioned by the applicable artifact and profile contracts and by the public interface bindings.

Public receipt views omit policy-decision and recovery-token references. Operational views remain secret-free.

## Build and local checks

```text
cargo fmt --check --manifest-path components/koa-node-agent/Cargo.toml
cargo check --manifest-path components/koa-node-agent/Cargo.toml
cargo test --manifest-path components/koa-node-agent/Cargo.toml
```

The crate declares B-0018 through the public `interfaces/rust` Cargo package and contains no private component dependency. Request, transport, broker, and fixed backend layers are present in the current crate; cross-component authority still flows only through registered public interfaces and production activation remains subject to system qualification.
