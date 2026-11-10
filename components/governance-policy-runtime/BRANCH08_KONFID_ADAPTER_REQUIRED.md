# Branch 08 — Required Konfid bridge to the kOA governance policy API

**Status:** `SPEC_DECISION_REQUIRED`; no generic HTTP transport route is inferred from the typed API. This implementation note lives with the policy component, **not** in the kOA-Linux contract-first normative document registry.

The local `api/routes.py` defines a closed typed operation `evaluate_decision` (`IFACE-GOV-POL-001`), with `PolicyEvaluationRequest` requiring `decision_class`, verified `requester`, `action`, `target`, `scope`, `policy_set_ref`, `authority_version`, and exactly the registered context fields. It produces `PolicyEvaluationResponse` with a bounded policy decision receipt, policy/authority version and obligations. It does not execute the owner action.

Konfid's observed `KoaPolicyEngine` calls `POST /v1/evaluate` and expects its own `AccessResponse` or control/response decision shape. These are **separate** interfaces. `tests/contract/test_branch08_konfid_bridge_boundary.py` asserts the native parser rejects the unadapted foreign body. A policy caller cannot silently gain an `ALLOW` by passing an unrecognized envelope.

**Implementation instruction:** ask both owners to adopt a versioned adapter profile, auth/tenant/receipt and correlation mappings, policy-set/authority-version pins, requirement for audit evidence, response TTL/obligation mapping and a real enforcing PEP. Both sides must run positive and negative tests. Use separate, isolated fixture collections; do not change the host release, policy set or deployment by introducing this documentation.

**Local code gate:** `PYTHONPATH=components/governance-policy-runtime/src python -m pytest -q components/governance-policy-runtime/tests/contract/test_branch08_konfid_bridge_boundary.py`.

This file is not a request to weaken kOA-Linux source closure or edit its generated documentation locks. Any eventual normative contract change must follow the owner's documented architecture/lock-generation workflow.
