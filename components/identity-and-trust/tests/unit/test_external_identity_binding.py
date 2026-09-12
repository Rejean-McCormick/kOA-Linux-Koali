from __future__ import annotations

from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
import sys

import pytest

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_identity_and_trust.application import (  # noqa: E402
    BindExternalIdentity,
    BindExternalIdentityCommand,
    Conflict,
    ResolveExternalIdentity,
    ResolveExternalIdentityCommand,
)
from koa_identity_and_trust.ports import ExternalIdentityBindingRecord, IdentityRecord  # noqa: E402

NOW = datetime(2026, 9, 11, 12, 0, tzinfo=UTC)


class Clock:
    def now(self):
        return NOW


class Audit:
    def __init__(self):
        self.events = []
    def ensure_available(self, *, critical: bool):
        assert critical is True
    def publish(self, event):
        self.events.append(event)


class Store:
    def __init__(self):
        self.identities = {
            "identity-human": IdentityRecord(
                identity_id="identity-human",
                subject_type="human",
                display_name="Human",
                owner_ref="owner-human",
                tenant_ref="tenant-a",
                environment="production",
                status="active",
                created_at=NOW,
                activated_at=NOW,
                expires_at=None,
            )
        }
        self.bindings = {}

    @contextmanager
    def transaction(self):
        yield None

    def get_identity(self, identity_id):
        return self.identities.get(identity_id)

    def get_external_identity_binding(self, *, provider_id, issuer, subject, tenant_ref, environment):
        return self.bindings.get((provider_id, issuer, subject, tenant_ref, environment))

    def put_external_identity_binding(self, record: ExternalIdentityBindingRecord):
        key = (record.provider_id, record.issuer, record.subject, record.tenant_ref, record.environment)
        self.bindings[key] = record


def command(**overrides):
    values = {
        "request_id": "request-1",
        "provider_id": "koa-common",
        "issuer": "https://id.example.test/realms/koa",
        "subject": "subject-001",
        "local_identity_id": "identity-human",
        "tenant_ref": "tenant-a",
        "environment": "production",
        "evidence_refs": ("evidence:oidc-validation",),
    }
    values.update(overrides)
    return BindExternalIdentityCommand(**values)


def test_bind_and_resolve_exact_issuer_subject():
    store, audit = Store(), Audit()
    bound = BindExternalIdentity(store, Clock(), audit).execute(command())
    resolved = ResolveExternalIdentity(store).execute(
        ResolveExternalIdentityCommand(
            provider_id="koa-common",
            issuer="https://id.example.test/realms/koa",
            subject="subject-001",
            tenant_ref="tenant-a",
            environment="production",
        )
    )
    assert bound.identity_ref == "identity-human"
    assert bound.authorizes_business_action is False
    assert resolved.identity_result == "established"
    assert resolved.identity_ref == "identity-human"
    assert audit.events[0].event_type == "external_identity_bound"


def test_subject_matching_is_exact_and_not_email_based():
    store, audit = Store(), Audit()
    BindExternalIdentity(store, Clock(), audit).execute(command())
    different_subject = ResolveExternalIdentity(store).execute(
        ResolveExternalIdentityCommand(
            provider_id="koa-common",
            issuer="https://id.example.test/realms/koa",
            subject="SUBJECT-001",
            tenant_ref="tenant-a",
            environment="production",
        )
    )
    assert different_subject.identity_result == "not_established"


def test_same_external_subject_cannot_rebind_to_another_identity():
    store, audit = Store(), Audit()
    store.identities["identity-other"] = IdentityRecord(
        identity_id="identity-other",
        subject_type="human",
        display_name="Other",
        owner_ref="owner-other",
        tenant_ref="tenant-a",
        environment="production",
        status="active",
        created_at=NOW,
        activated_at=NOW,
        expires_at=None,
    )
    binder = BindExternalIdentity(store, Clock(), audit)
    binder.execute(command())
    with pytest.raises(Conflict, match="already bound"):
        binder.execute(command(request_id="request-2", local_identity_id="identity-other"))
