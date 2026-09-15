# Governance Policy Runtime

Governance Policy Runtime is the kOA policy authority for profile-conditioned local governance decisions. It evaluates registered authorization, disclosure, consent, privilege, and exception requests against one exact active compatible policy set. It returns a bounded decision, obligations, diagnostics, and a policy decision receipt. The authoritative caller remains responsible for enforcing the result and for its own state transition.

## Authority boundary

The component may resolve registered policy and exception applicability, stage and validate policy bundles, atomically activate a complete policy set, retain the previous valid set, roll back when compatible, and report bounded health and compatibility state.

It does **not**:

- execute the governed operation;
- write another component's authoritative state;
- issue identities or operating-system credentials;
- allocate or schedule resources;
- execute publication or privileged host mutation;
- create consent or exception records;
- treat external AI, generated prose, prompts, or informal instructions as policy authority;
- activate a partial policy set or infer missing authority.

A policy decision never transfers data ownership, component authority, publication authority, or privilege ownership.

## Current implementation

The current package contains the policy runtime layers that earlier bootstrap-only documentation described as future work:

- domain objects for policy bundles, rules, evaluation context, and decisions;
- application use cases for bundle loading, evaluation, activation, and revocation;
- ports for bundle storage, decision receipts, signature verification, audit delivery, and time;
- filesystem bundle and receipt stores, identity-signature verification, audit, and clock adapters;
- bounded API models and routes;
- a documented versioned filesystem-state migration contract;
- packaging metadata;
- unit, contract, failure, and integration tests.

Bootstrap remains observational and fail-closed by design. It does not discover authority, silently activate policy, or write foreign state. Missing observations remain unknown rather than becoming permissive defaults.

### Version identifiers

The Python runtime/package currently uses `0.1.0`, while the component contract, public interfaces, and packaging payload use `1.0.0`. These fields are reported as distinct version namespaces; this README does not infer release compatibility from numeric equality or inequality. Any unification requires an explicit versioning decision.

## Health and readiness

Process health checks are:

- `process_responsive`;
- `local_storage_accessible`;
- `receipt_store_accessible`.

Readiness requires all of:

- `active_policy_set_resolves`;
- `policy_set_compatible_with_profile`;
- `policy_set_compatible_with_components`;
- `authority_version_resolves`;
- `required_trust_sources_resolve`;
- `required_exception_data_resolves`;
- `evaluator_version_compatible`;
- `critical_receipt_path_ready`.

The policy evaluation engine must also be explicitly observed as available. Process health never implies readiness. Remote connectivity and optional external AI are not required for native local policy evaluation.

## Audit evidence policy

`KOA_GOVERNANCE_POLICY_RUNTIME_AUDIT_EVIDENCE_POLICY` accepts:

- `not_required`;
- `local_buffer_permitted`;
- `required_delivery`.

When required delivery is unavailable, receipt-required governed transitions are blocked. Local buffering is allowed only when the profile has declared it and the local receipt path is ready. No silent fallback is performed.

## Configuration

Configuration is loaded only from explicitly supported `KOA_GOVERNANCE_POLICY_RUNTIME_*` variables. Unknown prefixed variables are rejected. Configuration contains references and operational bounds only; raw secrets and credentials are prohibited.

Useful commands:

```console
python -m koa_governance_policy_runtime check-config
python -m koa_governance_policy_runtime health
python -m koa_governance_policy_runtime health --assume-local-prerequisites-ready
```

The assumption flag is a development probe input. It does not discover, grant, or transfer authority.
