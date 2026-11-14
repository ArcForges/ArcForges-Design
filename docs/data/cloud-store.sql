-- ArcForges V2 PostgreSQL design specification, not a production migration.
-- Apply only through a new reviewed numbered migration after the immutable
-- schema 0001..0011 and the qualified V2 transition described in cloud-store.md.
-- No extension is required. Existing identity/fleet/platform/entitlement/audit
-- tables remain owned by their historical migrations. Cross-row guards and
-- least-privilege grants are required in the implementation migration.

CREATE SCHEMA management;
CREATE SCHEMA commerce;

-- Account lifecycle additions owned by AFV2-ID-01. Historical auth-flow kinds
-- are extended only by a reviewed migration; no existing kind is reinterpreted.
CREATE TABLE identity.account_security_state (
    account_id uuid PRIMARY KEY REFERENCES identity.user (user_id),
    auth_epoch bigint NOT NULL CHECK (auth_epoch >= 0),
    recovery_generation bigint NOT NULL CHECK (recovery_generation >= 0),
    rev bigint NOT NULL CHECK (rev >= 1),
    updated_at timestamptz NOT NULL
);

CREATE TABLE identity.lifecycle_operation (
    account_id uuid NOT NULL REFERENCES identity.user (user_id),
    command_id uuid NOT NULL,
    kind smallint NOT NULL CHECK (kind IN (1, 2, 3)),
    state smallint NOT NULL CHECK (state BETWEEN 1 AND 7),
    intent_sha256 bytea NOT NULL CHECK (octet_length(intent_sha256) = 32),
    plan_rev bigint NOT NULL CHECK (plan_rev >= 1),
    proof_ref uuid,
    recovery_generation bigint NOT NULL CHECK (recovery_generation >= 0),
    artifact_id uuid,
    artifact_sha256 bytea,
    artifact_bytes bigint CHECK (artifact_bytes >= 0),
    artifact_expires_at timestamptz,
    created_at timestamptz NOT NULL,
    expires_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL,
    completed_at timestamptz,
    PRIMARY KEY (account_id, command_id),
    CHECK (expires_at > created_at AND updated_at >= created_at),
    CHECK (completed_at IS NULL OR completed_at >= created_at),
    CHECK ((state = 4) = (completed_at IS NOT NULL)),
    CHECK (state NOT IN (2, 3, 4) OR proof_ref IS NOT NULL),
    CHECK (artifact_id IS NULL OR kind = 3),
    CHECK ((artifact_id IS NULL) = (artifact_sha256 IS NULL)),
    CHECK ((artifact_id IS NULL) = (artifact_bytes IS NULL)),
    CHECK ((artifact_id IS NULL) = (artifact_expires_at IS NULL)),
    CHECK (artifact_sha256 IS NULL OR octet_length(artifact_sha256) = 32),
    CHECK (artifact_expires_at IS NULL OR artifact_expires_at > created_at)
);
CREATE UNIQUE INDEX account_one_deletion
    ON identity.lifecycle_operation (account_id)
    WHERE kind = 2 AND state IN (1, 2, 3);
-- kind: 1 recovery, 2 deletion, 3 export; state: 1 awaiting_proof, 2 confirmed,
-- 3 processing, 4 completed, 5 failed, 6 expired, 7 revoked.
-- Proof refs are validated against the typed proof/flow store in the same tx.
-- The implementation guards immutable intent, monotonic epochs/final outcomes,
-- current account ownership and temporary artifact authorization/expiry.

-- Enables a database-enforced account/node/enrollment ownership relationship.
ALTER TABLE fleet.node ADD CONSTRAINT node_v2_identity
    UNIQUE (enrollment_id, node_id, user_id);

CREATE TABLE management.node_protocol (
    enrollment_id uuid PRIMARY KEY,
    node_id uuid NOT NULL,
    account_id uuid NOT NULL,
    protocol_major smallint NOT NULL CHECK (protocol_major = 2),
    protocol_epoch uuid NOT NULL UNIQUE,
    initialized_at timestamptz NOT NULL,
    revoked_at timestamptz,
    rev bigint NOT NULL CHECK (rev >= 1),
    FOREIGN KEY (enrollment_id, node_id, account_id)
        REFERENCES fleet.node (enrollment_id, node_id, user_id),
    CHECK (revoked_at IS NULL OR revoked_at >= initialized_at)
);
CREATE INDEX node_protocol_account ON management.node_protocol (account_id);

-- Migration-owned catalogue generated from the closed remote API specification.
-- Runtime cannot insert/update/delete it; terminal attach/input is absent.
CREATE TABLE management.method_catalogue (
    method text PRIMARY KEY CHECK (char_length(method) BETWEEN 1 AND 128),
    permission text NOT NULL CHECK (permission IN
        ('configure', 'run', 'stop', 'resources', 'data', 'delete', 'revoke')),
    contract_major smallint NOT NULL CHECK (contract_major = 2)
);

-- namespace: 1 legacy Task tombstone, 2 legacy file tombstone, 3 V2 management.
-- Global account/command uniqueness prevents reuse across methods/enrollments.
-- Insert-only at runtime. Historical method names are evidence, not dispatch.
CREATE TABLE management.command_identity (
    account_id uuid NOT NULL REFERENCES identity.user (user_id),
    command_id uuid NOT NULL,
    enrollment_id uuid NOT NULL,
    node_id uuid NOT NULL,
    namespace smallint NOT NULL CHECK (namespace IN (1, 2, 3)),
    node_owner_epoch bytea,
    method text NOT NULL CHECK (char_length(method) BETWEEN 1 AND 128),
    intent_sha256 bytea NOT NULL CHECK (octet_length(intent_sha256) = 32),
    created_at timestamptz NOT NULL,
    replay_until timestamptz NOT NULL,
    PRIMARY KEY (account_id, command_id),
    UNIQUE (account_id, command_id, node_owner_epoch),
    FOREIGN KEY (enrollment_id, node_id, account_id)
        REFERENCES fleet.node (enrollment_id, node_id, user_id),
    CHECK (replay_until > created_at),
    CHECK ((namespace = 3) = (node_owner_epoch IS NOT NULL)),
    CHECK (node_owner_epoch IS NULL OR octet_length(node_owner_epoch) = 16)
);
-- Node store owner epoch is distinct from enrollment/protocol/channel epochs.
-- Legacy namespaces have no such epoch; they are non-executable tombstones.
CREATE INDEX command_identity_enrollment
    ON management.command_identity (enrollment_id, created_at);

-- Routing states: 1 accepted; 2 reserved; 3 succeeded; 4 failed; 5 rejected;
-- 6 expired; 7 unknown; 8 not_delivered. These are not process/Run states.
-- A migration guard verifies namespace=3, same method/enrollment as identity,
-- and current node_protocol/lease fence when admitting a new V2 operation.
CREATE TABLE management.remote_operation (
    account_id uuid NOT NULL,
    command_id uuid NOT NULL,
    node_owner_epoch bytea NOT NULL CHECK (octet_length(node_owner_epoch) = 16),
    method text NOT NULL REFERENCES management.method_catalogue (method),
    state smallint NOT NULL CHECK (state IN (1, 3, 4, 5, 6, 7, 8)),
    may_have_delivered boolean NOT NULL DEFAULT false,
    delivery_count integer NOT NULL CHECK (delivery_count >= 0),
    hub_fence bigint NOT NULL CHECK (hub_fence >= 1),
    channel_epoch uuid NOT NULL,
    request_sha256 bytea NOT NULL CHECK (octet_length(request_sha256) = 32),
    result_sha256 bytea,
    result_kind text CHECK (result_kind IN ('sandbox', 'run', 'transfer', 'policy', 'operation')),
    result_id uuid,
    effect smallint CHECK (effect IN (1, 2, 3)),
    reason text CHECK (char_length(reason) BETWEEN 1 AND 96),
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL,
    final_at timestamptz,
    PRIMARY KEY (account_id, command_id),
    FOREIGN KEY (account_id, command_id, node_owner_epoch)
        REFERENCES management.command_identity (account_id, command_id, node_owner_epoch),
    CHECK (result_sha256 IS NULL OR octet_length(result_sha256) = 32),
    CHECK ((result_kind IS NULL) = (result_id IS NULL)),
    CHECK (state <> 8 OR NOT may_have_delivered),
    CHECK (state <> 3 OR (result_sha256 IS NOT NULL AND effect = 2 AND final_at IS NOT NULL)),
    CHECK (state NOT IN (3, 4) OR may_have_delivered),
    CHECK (final_at IS NULL OR state IN (3, 4, 5, 6)),
    CHECK (updated_at >= created_at),
    CHECK (final_at IS NULL OR final_at >= created_at)
);
-- foundation.v1 EffectCertainty: 1 did_not_happen, 2 happened, 3 unknown.
CREATE INDEX remote_operation_open
    ON management.remote_operation (state, updated_at) WHERE final_at IS NULL;

-- Migration-role only: exact artifact/backup/cutover proof identity, no secrets.
CREATE TABLE management.cutover_receipt (
    cutover_id uuid PRIMARY KEY,
    source_schema integer NOT NULL CHECK (source_schema >= 0),
    target_schema integer NOT NULL CHECK (target_schema > source_schema),
    database_identity_sha256 bytea NOT NULL CHECK (octet_length(database_identity_sha256) = 32),
    artifact_manifest_sha256 bytea NOT NULL CHECK (octet_length(artifact_manifest_sha256) = 32),
    backup_manifest_sha256 bytea NOT NULL CHECK (octet_length(backup_manifest_sha256) = 32),
    retired_writer_set_sha256 bytea NOT NULL CHECK (octet_length(retired_writer_set_sha256) = 32),
    phase smallint NOT NULL CHECK (phase IN (1, 2, 3, 4)),
    recorded_at timestamptz NOT NULL,
    ready_at timestamptz,
    CHECK ((phase = 4) = (ready_at IS NOT NULL))
);
-- phase: 1 prepared, 2 writers_fenced, 3 schema_verified, 4 ready.
-- Restore creates a target-specific receipt; source readiness is not copied.

-- Provider 1 is the admitted web provider (Paddle); environment 1 production,
-- 2 provider sandbox. Exact provider API/version is pinned by AFV2-HOST-02.
CREATE TABLE commerce.customer (
    account_id uuid NOT NULL REFERENCES identity.user (user_id),
    provider smallint NOT NULL CHECK (provider = 1),
    environment smallint NOT NULL CHECK (environment IN (1, 2)),
    provider_customer_ref text NOT NULL CHECK (char_length(provider_customer_ref) BETWEEN 1 AND 128),
    created_at timestamptz NOT NULL,
    PRIMARY KEY (account_id, provider, environment),
    UNIQUE (provider, environment, provider_customer_ref)
);

CREATE TABLE commerce.checkout (
    checkout_id uuid PRIMARY KEY,
    account_id uuid NOT NULL REFERENCES identity.user (user_id),
    command_id uuid NOT NULL,
    provider smallint NOT NULL CHECK (provider = 1),
    environment smallint NOT NULL CHECK (environment IN (1, 2)),
    catalog_version text NOT NULL CHECK (char_length(catalog_version) BETWEEN 1 AND 128),
    product_ref text NOT NULL CHECK (char_length(product_ref) BETWEEN 1 AND 128),
    intent_sha256 bytea NOT NULL CHECK (octet_length(intent_sha256) = 32),
    provider_checkout_ref text CHECK (char_length(provider_checkout_ref) BETWEEN 1 AND 128),
    state smallint NOT NULL CHECK (state IN (1, 2, 3, 4, 5)),
    created_at timestamptz NOT NULL,
    expires_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL,
    UNIQUE (account_id, command_id),
    UNIQUE (provider, environment, provider_checkout_ref),
    CHECK (expires_at > created_at AND updated_at >= created_at)
);
-- checkout state: 1 pending, 2 provider_created, 3 completed, 4 expired, 5 unknown.
-- Completion follows verified provider evidence, never a browser return URL.
CREATE INDEX checkout_account ON commerce.checkout (account_id, created_at);

CREATE TABLE commerce.subscription (
    subscription_id uuid PRIMARY KEY,
    account_id uuid NOT NULL REFERENCES identity.user (user_id),
    provider smallint NOT NULL CHECK (provider = 1),
    environment smallint NOT NULL CHECK (environment IN (1, 2)),
    provider_subscription_ref text NOT NULL CHECK (char_length(provider_subscription_ref) BETWEEN 1 AND 128),
    catalog_version text NOT NULL CHECK (char_length(catalog_version) BETWEEN 1 AND 128),
    state smallint NOT NULL CHECK (state BETWEEN 1 AND 7),
    valid_from timestamptz,
    valid_until timestamptz,
    auto_renew boolean NOT NULL,
    provider_revision text CHECK (char_length(provider_revision) BETWEEN 1 AND 128),
    verified_at timestamptz NOT NULL,
    rev bigint NOT NULL CHECK (rev >= 1),
    UNIQUE (provider, environment, provider_subscription_ref),
    UNIQUE (subscription_id, account_id, provider, environment),
    FOREIGN KEY (account_id, provider, environment)
        REFERENCES commerce.customer (account_id, provider, environment),
    CHECK ((valid_from IS NULL) = (valid_until IS NULL)),
    CHECK (state NOT IN (2, 3, 4) OR valid_from IS NOT NULL),
    CHECK (valid_until IS NULL OR valid_until > valid_from)
);
CREATE INDEX subscription_account ON commerce.subscription (account_id, state);

CREATE TABLE commerce.provider_event (
    provider smallint NOT NULL CHECK (provider = 1),
    environment smallint NOT NULL CHECK (environment IN (1, 2)),
    event_ref text NOT NULL CHECK (char_length(event_ref) BETWEEN 1 AND 128),
    payload_sha256 bytea NOT NULL CHECK (octet_length(payload_sha256) = 32),
    event_kind text NOT NULL CHECK (char_length(event_kind) BETWEEN 1 AND 96),
    resource_ref text NOT NULL CHECK (char_length(resource_ref) BETWEEN 1 AND 128),
    state smallint NOT NULL CHECK (state BETWEEN 1 AND 5),
    verified_at timestamptz NOT NULL,
    received_at timestamptz NOT NULL,
    processed_at timestamptz,
    next_check_at timestamptz,
    failure_code text CHECK (char_length(failure_code) BETWEEN 1 AND 96),
    PRIMARY KEY (provider, environment, event_ref),
    CHECK (processed_at IS NULL OR processed_at >= received_at)
);
CREATE INDEX provider_event_work
    ON commerce.provider_event (state, next_check_at) WHERE state IN (1, 3);

-- Immutable verified financial facts; no card/credential/raw webhook storage.
CREATE TABLE commerce.billing_entry (
    entry_id uuid PRIMARY KEY,
    account_id uuid NOT NULL REFERENCES identity.user (user_id),
    subscription_id uuid,
    provider smallint NOT NULL CHECK (provider = 1),
    environment smallint NOT NULL CHECK (environment IN (1, 2)),
    provider_entry_ref text NOT NULL CHECK (char_length(provider_entry_ref) BETWEEN 1 AND 128),
    kind smallint NOT NULL CHECK (kind IN (1, 2, 3)),
    currency text NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    amount_minor numeric(20, 0) NOT NULL CHECK (amount_minor >= 0),
    occurred_at timestamptz NOT NULL,
    recorded_at timestamptz NOT NULL,
    UNIQUE (provider, environment, provider_entry_ref, kind),
    FOREIGN KEY (subscription_id, account_id, provider, environment)
        REFERENCES commerce.subscription (subscription_id, account_id, provider, environment)
);
-- kind: 1 payment, 2 refund, 3 chargeback; amount is unsigned with kind meaning.
CREATE INDEX billing_entry_account ON commerce.billing_entry (account_id, occurred_at);

-- Implementation obligations beyond row shape:
-- * immutable command/event/financial identity and final outcomes;
-- * monotonic may_have_delivered, delivery_count and optimistic revisions;
-- * generated closed method/permission/event allowlists, not dynamic dispatch;
-- * current enrollment, Node grant and hub fence checked at admission;
-- * business result + entitlement facts + audit/outbox in one transaction;
-- * terminal receipt compaction retains non-executable identity tombstones;
-- * migration-only catalogue/cutover/purge and enumerated runtime table grants.
