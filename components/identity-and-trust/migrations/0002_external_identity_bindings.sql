PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS external_identity_bindings (
    binding_id TEXT PRIMARY KEY,
    provider_type TEXT NOT NULL CHECK (provider_type = 'oidc'),
    provider_id TEXT NOT NULL,
    issuer TEXT NOT NULL,
    subject TEXT NOT NULL,
    local_identity_id TEXT NOT NULL REFERENCES identities(identity_id) ON UPDATE RESTRICT ON DELETE RESTRICT,
    tenant_ref TEXT NOT NULL DEFAULT '',
    environment TEXT NOT NULL,
    created_at TEXT NOT NULL,
    evidence_refs_json TEXT NOT NULL DEFAULT '[]' CHECK (json_valid(evidence_refs_json)),
    UNIQUE (provider_id, issuer, subject, tenant_ref, environment)
) STRICT;

CREATE INDEX IF NOT EXISTS idx_external_identity_local_identity
    ON external_identity_bindings(local_identity_id);

INSERT OR IGNORE INTO schema_migrations(version, applied_at)
VALUES ('0002_external_identity_bindings', strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));
