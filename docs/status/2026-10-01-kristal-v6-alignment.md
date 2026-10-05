<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-STATUS-006",
  "document_class": "explanatory_markdown",
  "status": "active",
  "authority_participation": "non_authoritative",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/integrations/kristal-v6.integration.json",
    "contracts/integrations/kristal-v6.0.0.consumer-lock.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-STATUS-000",
    "DOC-STATUS-001",
    "DOC-STATUS-002",
    "DOC-STATUS-003",
    "DOC-STATUS-004",
    "DOC-STATUS-005"
  ],
  "tags": [
    "status",
    "kristal",
    "integration",
    "contracts",
    "qualification"
  ],
  "edit_policy": "manual"
}
KOA:DOC-META:END -->

# kOA-Linux — Kristal v6 alignment

Status: **implemented in this snapshot**  
Effective baseline: **Kristal 6.0.0**  
Canonical artifact: **`kristal_state`**  
Canonicalization: **`kristal.v6:jcs-rfc8785` / version `1`**  
Interaction Kernel boundary profiles: **`2.0.0`**

## Pinned upstream contracts

The repository vendors Kristal v6 State and Reader Policy schemas adapted to the local kOA schema namespace while preserving their upstream schema IDs in `x-upstream-id`. The consumer lock pins the adapted local contract bytes, while the upstream standard manifest remains pinned separately.

## Runtime behavior

`kristal_runtime` now admits `kristal_state` documents directly. A state is content-addressed with SHA-256 over RFC 8785 JCS canonical bytes after the declared top-level exclusions `state_id`, `content_hash`, and `signatures`. Both `state_id` and `content_hash.value` must match the recomputed digest.

The v6 semantic model is preserved: typed `valuations[]`, statement `coordinates`, `applicability`, `record_role`, and `actionability`. Pre-v6 semantic fields (`certainty_level`, `uncertainty`, `qualifiers`, `scope`) are rejected inside a v6 state.

`actionability.mode = automatic` is never treated as execution authority. Kristal State verification does not make a state activation-eligible; Runtime Pack activation remains governed by the existing activation, policy, authorization, and resource boundaries.

## Compatibility

The historical `kristal_artifact` wrapper remains accepted as a compatibility path so existing kOA consumers are not broken in-place. It is explicitly non-canonical for Kristal v6 and is superseded by `kristal_state` for new integrations.

## Validation performed

- Kristal State schema digest: matches the pinned consumer lock.
- Reader Policy schema digest: matches the pinned consumer lock.
- RFC 8785 JCS conformance: 9/9 supplied IK normative vectors pass.
- Kristal Runtime focused tests: 26/26 pass.
- Existing domain/integration/failure tests: 28/28 pass.
- Component contract tests: 11/11 pass.
- Total targeted checks: 65 tests passing, in addition to the 9 JCS vectors.

The contract-test directory in this snapshot has no package marker, so its existing relative imports require a temporary test-only package marker when executed directly. No such marker is shipped in the aligned tree.
