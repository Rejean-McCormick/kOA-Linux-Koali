"""Native typed policy decisions cannot silently ingest Konfid's HTTP envelope."""
from __future__ import annotations

import pytest

from koa_governance_policy_runtime.api.models import (
    API_VERSION, ApiRequest, ModelValidationError, PolicyEvaluationRequest,
)


def test_native_policy_parser_requires_registered_context_not_foreign_http_shape():
    # Konfid's documented /v1/evaluate body is a separate transport contract.
    foreign = {
        "kind": "access",
        "context": {
            "request_id": "req-branch08", "tenant": "tenant-branch08",
            "actor": "principal-branch08", "action": "world.read",
            "resource": {"owner": "konnaxion", "class": "WORLD"},
            "scope": {"organization": "tenant-branch08"},
        },
    }
    request = ApiRequest("evaluate_decision", "POLREQ-BRANCH08", "CORR-BRANCH08", foreign, API_VERSION)
    with pytest.raises(ModelValidationError):
        PolicyEvaluationRequest.from_payload(foreign, request)
