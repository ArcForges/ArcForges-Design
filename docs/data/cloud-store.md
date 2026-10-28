# Cloud store (Cloudflare D1)

**Amended 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) §8.** The center's store is PostgreSQL (Neon in the official deployment), not D1. The model below is the D1 baseline the PostgreSQL model is derived from; §6 states the derivation rules, and the PostgreSQL migrations of the Cloud repository are its implementation (AF-CTR-02, AF-CTR-03, AF-CTR-04, AF-CTR-09).

Baseline: Cloud main `92ba1dc9`. Its D1 physical model is generated from `src/ArcForges.Cloud.Storage.D1/Physical/manifest/*.json` (Design D1 profile section 2), which fixes:
- module-prefixed table names;
- `STRICT` tables;
- canonical UUID text IDs;
- instants as UTC microseconds;
- enums as registered numbers;
- generated constraint names.

The flagship adds one module, `fleet`, and adapts a few reused tables. The new tables are specified in [cloud-store.sql](cloud-store.sql), which is checked in SQLite with stubs for the referenced reused tables. AF-CLD-01 writes them as `Physical/manifest/fleet.json` and generates the migration.

## 1. New tables (`fleet` module)

| Table | Purpose | Keys and indexes | Retention | Owner flow |
|---|---|---|---|---|
| `fleet_node` | Node registry: account, device, installation, name, OS, architecture, role and host link (both retired for guests by [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md) §3: every node is a host and `host_node_id` is never set), version, LAN hints (reserved for roadmap RM-01), relay flag, revocation | PK `node_id`; unique `installation_id`; `(user_id, revoked_at)`; `host_node_id` | Until revoked + 30 days | Enrollment, `ReportNodeInfo`, `ReportLanEndpoints`, `RevokeNode` |
| `fleet_node_sign_in` | Browser sign-in consent and the node being enrolled. PKCE, code and attempts reuse `identity_native_authorization` (same `flow_id`). | PK `flow_id`; `expires_at` | 7 days | 10 §3.1 (SM-SIGN-IN) |
| `fleet_device_authorization` | Device-code flows; codes stored as hashes only | PK `authorization_id`; unique `device_code_hash`; unique live `user_code_hash`; `expires_at` | 7 days | 10 §3.2 (SM-DEVICE-AUTH) |
| `fleet_phone_pairing` | QR pairing for phone sign-in; secret and claim token as hashes | PK `pairing_id`; `(node_id, created_at)` | 7 days | 10 §3.3 (SM-PHONE-PAIRING) |
| `fleet_node_certificate` | Reserved for account-based LAN trust (roadmap RM-01); not written in release 1 | PK `serial`; `(node_id, expires_at)` | Expiry + 30 days | `IssueNodeCertificate`, revocation |
| `fleet_remote_command` | Remote commands with signed envelopes and signed results (SM-REMOTE-COMMAND) | PK `command_id`; `(node_id, created_at)`; `(state, expires_at)`; `(user_id, created_at)` | 90 days | 10 §3.6 |
| `fleet_play_purchase` | Google Play purchase tokens (hash; the token itself encrypted at rest for API re-reads), link state, acknowledgement due date | PK `purchase_token_hash`; `user_id`; pending acknowledgement | 7 years (billing records) | AD-0010 §3 |
| `fleet_play_notification` | RTDN inbox, deduplicated by Pub/Sub message ID | PK `message_id`; unprocessed | 90 days | 10 §3.9 |
| `fleet_push_preference` | Push preferences per kind and node (`FleetService.GetPushPreferences`, `UpdatePushPreferences`) | PK `(user_id, kind, node_scope)` | Until account deletion | Notification preferences |
| `fleet_signing_key` | Key metadata: key ID, purpose (command signing, entitlement token, relay HMAC; a Node Issuing CA intermediate only once roadmap RM-01 is delivered), validity, secret binding name. Private keys live only in platform secrets. | PK `kid` | Permanent | Key rotation runbook |

## 2. Reused tables

"Reuse" here means the **D1 schema** at Cloud main `92ba1dc9`. Most of these modules have no service implementation yet. The building tasks are named in [10](../architecture/10-cloud.md) §2.

| Module | Tables | Use |
|---|---|---|
| Identity (reuse) | `identity_user`, `identity_session`, `identity_spent_refresh`, `identity_native_authorization`, `identity_step_up_challenge`, `identity_auth_identity`, `identity_recovery_*`, `identity_security_flow` | Accounts and authentication. Node credentials are native-bearer sessions (`credential_kind` 1, refresh rotation with reuse detection through `identity_spent_refresh`) bound to the node's installation. Phones get native-bearer sessions bound to their `arcforges-mobile` installation, with scope `mobile.limited` until a step-up. Step-up for remote commands. Endpoints: AF-ID-01, AF-ID-02. |
| Device (reuse) | `device_device`, `device_installation`, `device_remote_policy` | **One device record per node** (a Linux node a user runs in WSL2 is an ordinary node; WSL guest nodes are retired by [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md)), with one installation of product `arcforges-node`. One device record per phone, with one installation of product `arcforges-mobile`. This respects the unique index `(device_id, product_id)` without change. `fleet_node.device_id` links the node to its device. Endpoints: AF-ID-02. |
| Entitlement (reuse) | `entitlement_*` | Plan catalogue (configuration revision), snapshots and the cloud features `remote.*` and `push` (local and LAN features are never gated, AD-0015). The resolver exists; endpoints: AF-CLD-03. |
| Commerce (adapt) | `commerce_subscription`, `commerce_provider_event`, `commerce_checkout_attempt`, `commerce_provider_customer`, `commerce_refund`, … | Paddle provider (AF-COM-01); the Play provider (AF-CLD-07) writes subscription state through the same tables, linked from `fleet_play_purchase.subscription_id` |
| Notification (adapt) | `notification_push_registration`, `notification_delivery*`, `notification_suppression` | FCM push for node events (AF-CLD-06) |
| Support (reuse) | `support_support_case`, `support_case_message`, `support_access_grant` | Cases and access grants; support-bundle uploads are referenced from case messages (R2 object keys) (AF-SUP-01) |
| Audit (reuse) | `audit_audit_event`, `audit_operator_*` | Enrollment, revocation, remote commands, commerce and operator actions (writer and reader: AF-PLAT-01) |
| Platform (reuse) | `platform_command`, `platform_command_guard`, `platform_inbox`, `platform_outbox`, `platform_job_lease`, `platform_operating_budget`, `platform_operating_reservation` | Implemented in the D1 storage layer: command dedup (receipts and guard), the webhook inbox, the outbox and their purge plans. New in AF-PLAT-01: job lease plans and the cron-driven job runner (acknowledgement, purges), the scheduled retention sweeps that apply the Retention column of this model, and the operating-budget service. |
| Config (reuse) | `config_revision` | Kill switches, limits and the plan catalogue (AF-PLAT-01) |

## 3. Adaptations (migration notes)

| Change | Tables | Migration |
|---|---|---|
| Product ID domain gains `arcforges-node`, `arcforges-mobile` and `arcforges-web` (the last added 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) §7; on the Go center the PostgreSQL `CHECK` of §6 carries all three beside the retained `arcscope` and `companion`, AF-CTR-03) | `device_installation.product_id` and `identity_session.product_id`; today `CHECK (product_id IN ('arcscope', 'companion'))` | The `productId` type change regenerates the check constraints. SQLite cannot alter a CHECK, so the Cloud generator emits a table-rebuild migration (create new, copy, swap) under the repository's migration rules. Indexes are unchanged, because each node is its own device (§2). AF-CLD-01. |
| Operating dimensions gain `containerCpuSeconds` (8), `doRequests` (9), `d1RowsRead` (10), `d1RowsWritten` (11), `pushSends` (12), `containerInstanceSeconds` (13), `doDurationGbSeconds` (14), `workerRequests` (15), `doRowsWritten` (16), `egressBytes` (17), `queueOperations` (18) and `emailsSent` (19) ([14](../architecture/14-commercial-operations.md) §7.1) | `platform_operating_budget.dimension` and `platform_operating_reservation.dimension`; today `CHECK (dimension IN (1..7))` | Same table-rebuild migration pattern as the product ID change. Estimated dimensions (`doDurationGbSeconds`) are recorded after the fact, without reservations. AF-PLAT-01. |
| Device platform values | `device_device.platform` already lists `windows`, `linux` and `android` | None |
| Push kinds | `notification_*` kind columns (text) | None (data) |
| Plan features | Entitlement configuration | Configuration revision (data) |
| Cost switches: `cloud.essential_only`, the ladder steps, `ops.unit_prices` | `config_revision` | Configuration revision (data); [14](../architecture/14-commercial-operations.md) §7. The activation switches are deployment settings, not D1 data: `FLAGSHIP_SURFACES` in `wrangler.json` and the Web deploy configuration ([10](../architecture/10-cloud.md) §8). |

## 4. Not stored in D1

- **Live status.** It lives in the `FleetHub` Durable Object (latest summary and snapshot per node, last 100 summary changes) and is never persisted as time series (AD-0009 §8).
- **Task records, output and samples.** They stay on nodes.
- **Support bundles.** They are R2 objects (30 days); D1 holds only the reference.
- **Release manifests and artifacts.** These are R2 static objects.

## 5. Deletion

Account deletion follows the reused contract's flow, built by AF-ID-02: request, then a 30-day grace period, then purge.
- **Purge** cascades through `identity_user` to `fleet_node`, phone pairings and commands.
- **Revocation** revokes certificates and closes relay sockets through `HostEnvelope.kill_switches`, scoped to the account.
- **Kept records:** `fleet_play_purchase` and commerce records stay for the statutory billing retention, keyed by hashed references with personal fields cleared ([11](../architecture/11-security-privacy.md) §5).

## 6. PostgreSQL model (AD-0021)

Added 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) §8. The D1 model above is mapped to PostgreSQL by these rules; the Cloud repository's migrations under `center/` are the implementation, and each rule's delivery is named. The AF-CTR-02 rows are delivered (Cloud #116 at `ec596f2`, migration `0001_platform_store.sql`, applied to production on 2026-10-28); the module rows follow with their tasks.

| D1 baseline | PostgreSQL | Delivered by |
|---|---|---|
| Module-prefixed tables (`identity_user`) in one database | One schema per module (`identity.user`), owned by the migration role; the runtime role receives only the grants its module needs | AF-CTR-02 (platform), AF-CTR-03, AF-CTR-04, AF-CTR-09 |
| `STRICT` tables, canonical UUID text IDs | `uuid` columns; `text` with length checks where the contract bounds a string | AF-CTR-02 |
| Instants as UTC microseconds (`INTEGER`) | `timestamptz` (microsecond precision) | AF-CTR-02 |
| Enums as registered numbers with `CHECK (x IN (…))` | `smallint` with named `CHECK` constraints; a new value is an ordinary `ALTER TABLE … DROP/ADD CONSTRAINT` migration | AF-CTR-02 |
| Table-rebuild migrations (create, copy, swap) for changed checks | Ordinary `ALTER TABLE` in a transaction; expand and contract for changes the running revision must survive | AF-CTR-02 |
| Named storage plans, guarded batches and the commit tail | Native multi-statement transactions with row locks or `SERIALIZABLE` where invariants span rows, serialization-failure retry, receipts and outbox rows written in the same transaction | AF-CTR-02 |
| Command receipts and the command guard | `platform.command_receipt` unique per principal and command ID, with the request digest; a replay returns the stored result, a different digest is refused | AF-CTR-02 |
| Inbox and outbox with purge plans | `platform.inbox` (unique by provider message ID), `platform.outbox` with a publisher that marks delivery; retention sweeps (AF-PLAT-01) | AF-CTR-02, AF-PLAT-01 |
| Job lease (`lease` guard: holder and fence) | `platform.job_lease` with `SELECT … FOR UPDATE` and a monotonically increasing fence | AF-CTR-02 |
| Migration runner and plan-manifest hashes | Versioned SQL files with SHA-256 checksums in `platform.schema_migration`, applied under an exclusive session advisory lock; an edited applied file is refused | AF-CTR-02 |

**Roles and the runtime credential (delivered by AF-CTR-02).**

- **Migration role.** The database owner, used through the direct (unpooled) connection by the protected deployment's migration step (before promotion), its runtime-credential rotation and its post-deploy promotion record, and by an operator's documented recovery. It owns the module schemas and reconciles the runtime grants on every run. Until AF-CTR-09 the C# Hello/rollback secret is the same owner role; it reaches only the C# host.
- **Runtime role.** A `NOLOGIN` group with exactly the declared table privileges of each module: no `DELETE`, `TRUNCATE` or DDL, no update or delete of audit events (only the chain-head row that serializes appends), no write of signing keys or of the migration record, and no read of an ungranted table. The center creates two login roles (`<group>_a`, `<group>_b`), each `INHERIT` and `CONNECTION LIMIT 16`, as its members; the center connects through the pooled connection, and the rotation makes one unpooled proof connection.
- **Database privileges.** `CONNECT` and `TEMPORARY` are revoked from `PUBLIC` on the center's database, and the runtime group alone receives `CONNECT`, so one environment's runtime credential cannot connect to another environment's database.
- **Rotation.** Each deployment sets a new random password on the login role of one slot, proves it through the pooled and an unpooled connection, and hands it to the new Worker version as a secret; the slot is recorded as promoted only after that version is live, and each version is labelled with its slot. The rotated slot is the one other than the live version's label, or, when the label is missing or unreadable, other than the most recently promoted slot; a failed or retried deployment therefore rotates only an unpromoted slot. Only if Cloudflare cannot be read after a lost promotion record can the live slot be rotated; the manual confirmation in Cloud `docs/postgres-store.md` closes that gap.
- **Secret handling.** The password never appears in a top-level statement, a bind parameter or a reported error: it reaches the server as COPY data and is applied by a nested statement whose known log emitters are switched off, and the rotation refuses the settings that record nested statements in full (`pg_stat_statements.track` or `pg_stat_monitor.pgsm_track` = `all`, `log_parser_stats` on). A cancellation, a termination or a password-check-hook WARNING can still log the nested statement; a cancelled or terminated rotation aborts, so that value never becomes a working credential, whereas a WARNING does not abort it: operators must not install password-check hooks on a center database. Neon receives the plaintext (it does not support pre-hashed passwords); a self-hosted PostgreSQL receives a SCRAM-SHA-256 verifier computed by the center.
- **Recovery.** A logical-backup restore drill on an isolated PostgreSQL runs on every Linux verification; Neon's history window bounds point-in-time restore of the whole branch (production and acceptance share it), and its recorded value is an owner action of the acceptance register.

What the center does not store is unchanged (§4) and widened by AD-0021 §10: task specifications, output and file contents pass through the center transiently and are never persisted.
