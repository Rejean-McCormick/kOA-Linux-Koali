# Identity and Trust migrations

This directory owns the authoritative SQLite schema for Identity and Trust. It
must never be used as a shared database by another component.

## `0001_initial.sql`

The initial migration creates separate records for identities, credential
lifecycles, scoped trust roots, revocations, verification evidence and monotonic
offline trust-update state. Private key bytes are deliberately absent: database
rows store only protected key or material references.

The migration is idempotent for an empty or already-initialized database and
uses SQLite `STRICT` tables, foreign keys, JSON validity checks and closed state
enumerations. Applications must apply it inside an exclusive migration step and
must not activate a partially restored or partially migrated store.

## Operational rules

- Back up identity metadata, trust roots, revocations and verification evidence
  through the component-owned backup path.
- Back up private material only through a separately declared protected path.
- Verify a restored database before atomic activation.
- Never edit a migration after it has been released; add a new numbered
  migration instead.
- Never grant another component direct write access to these tables.


## `0002_external_identity_bindings.sql`

Adds the local federation map used by `koa-common-oidc-v1`. The unique external identity key is the exact `provider_id + issuer + subject + tenant_ref + environment` tuple. Email and display name are deliberately absent. The row points to a local `identities.identity_id`; owner applications still make their own authorization decisions.
