from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import sys

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_identity_and_trust.adapters import SQLiteIdentityStore  # noqa: E402
from koa_identity_and_trust.ports import ExternalIdentityBindingRecord  # noqa: E402


def test_external_identity_binding_round_trip(tmp_path):
    store = SQLiteIdentityStore(tmp_path / "identity.sqlite3")
    store.initialize()
    now = datetime(2026, 9, 11, 12, 0, tzinfo=UTC)
    store.put_identity(
        {
            "identity_id": "identity-human",
            "subject_type": "human",
            "display_name": "Human",
            "owner_ref": "owner-human",
            "tenant_ref": "tenant-a",
            "environment": "production",
            "status": "active",
            "created_at": now.isoformat(),
            "activated_at": now.isoformat(),
            "expires_at": None,
            "credential_refs": [],
            "evidence_refs": [],
        }
    )
    store.put_external_identity_binding(
        ExternalIdentityBindingRecord(
            binding_id="binding-1",
            provider_type="oidc",
            provider_id="koa-common",
            issuer="https://id.example.test/realms/koa",
            subject="subject-001",
            local_identity_id="identity-human",
            tenant_ref="tenant-a",
            environment="production",
            created_at=now,
            evidence_refs=("evidence:oidc-validation",),
        )
    )
    record = store.get_external_identity_binding(
        provider_id="koa-common",
        issuer="https://id.example.test/realms/koa",
        subject="subject-001",
        tenant_ref="tenant-a",
        environment="production",
    )
    assert record is not None
    assert record["local_identity_id"] == "identity-human"
    assert record["evidence_refs"] == ["evidence:oidc-validation"]
