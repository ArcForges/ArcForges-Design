# Cloud store (Cloudflare D1)

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
| `fleet_node` | Node registry: account, device, installation, name, OS, architecture, role, host link, version, LAN hints, relay flag, revocation | PK `node_id`; unique `installation_id`; `(user_id, revoked_at)`; `host_node_id` | Until revoked + 30 days | Enrollment, `ReportNodeInfo`, `ReportLanEndpoints`, `RevokeNode` |
| `fleet_node_sign_in` | Browser sign-in consent and the node being enrolled. PKCE, code and attempts reuse `identity_native_authorization` (same `flow_id`). | PK `flow_id`; `expires_at` | 7 days | 10 §3.1 (SM-SIGN-IN) |
| `fleet_device_authorization` | Device-code flows; codes stored as hashes only | PK `authorization_id`; unique `device_code_hash`; unique live `user_code_hash`; `expires_at` | 7 days | 10 §3.2 (SM-DEVICE-AUTH) |
| `fleet_phone_pairing` | QR pairing for phone sign-in; secret and claim token as hashes | PK `pairing_id`; `(node_id, created_at)` | 7 days | 10 §3.3 (SM-PHONE-PAIRING) |
| `fleet_node_certificate` | Issued node certificates; source of the revocation list carried in entitlement tokens | PK `serial`; `(node_id, expires_at)` | Expiry + 30 days | `IssueNodeCertificate`, revocation |
| `fleet_remote_command` | Remote commands with signed envelopes and signed results (SM-REMOTE-COMMAND) | PK `command_id`; `(node_id, created_at)`; `(state, expires_at)`; `(user_id, created_at)` | 90 days | 10 §3.6 |
| `fleet_play_purchase` | Google Play purchase tokens (hash; the token itself encrypted at rest for API re-reads), link state, acknowledgement due date | PK `purchase_token_hash`; `user_id`; pending acknowledgement | 7 years (billing records) | AD-0010 §3 |
| `fleet_play_notification` | RTDN inbox, deduplicated by Pub/Sub message ID | PK `message_id`; unprocessed | 90 days | 10 §3.9 |
| `fleet_push_preference` | Push preferences per kind and node (`FleetService.GetPushPreferences`, `UpdatePushPreferences`) | PK `(user_id, kind, node_scope)` | Until account deletion | Notification preferences |
| `fleet_signing_key` | Key metadata: key ID, purpose (command signing, entitlement token, relay HMAC, Node Issuing CA intermediate), validity, secret binding name. Private keys live only in platform secrets; the Node Issuing CA root stays offline. | PK `kid` | Permanent | Key rotation runbook |

## 2. Reused tables

"Reuse" here means the **D1 schema** at Cloud main `92ba1dc9`. Most of these modules have no service implementation yet. The building tasks are named in [10](../architecture/10-cloud.md) §2.

| Module | Tables | Use |
|---|---|---|
| Identity (reuse) | `identity_user`, `identity_session`, `identity_spent_refresh`, `identity_native_authorization`, `identity_step_up_challenge`, `identity_auth_identity`, `identity_recovery_*`, `identity_security_flow` | Accounts and authentication. Node credentials are native-bearer sessions (`credential_kind` 1, refresh rotation with reuse detection through `identity_spent_refresh`) bound to the node's installation. Phones get native-bearer sessions bound to their `arcforges-mobile` installation, with scope `mobile.limited` until a step-up. Step-up for remote commands. Endpoints: AF-ID-01, AF-ID-02. |
| Device (reuse) | `device_device`, `device_installation`, `device_remote_policy` | **One device record per node**, including each WSL guest node, with one installation of product `arcforges-node`. One device record per phone, with one installation of product `arcforges-mobile`. This respects the unique index `(device_id, product_id)` without change. `fleet_node.device_id` links the node to its device. Endpoints: AF-ID-02. |
| Entitlement (reuse) | `entitlement_*` | Plan catalogue (configuration revision), snapshots and features `lan.*`, `remote.*`, `push`. The resolver exists; endpoints: AF-CLD-03. |
| Commerce (adapt) | `commerce_subscription`, `commerce_provider_event`, `commerce_checkout_attempt`, `commerce_provider_customer`, `commerce_refund`, … | Paddle provider (AF-COM-01); the Play provider (AF-CLD-07) writes subscription state through the same tables, linked from `fleet_play_purchase.subscription_id` |
| Notification (adapt) | `notification_push_registration`, `notification_delivery*`, `notification_suppression` | FCM push for node events (AF-CLD-06) |
| Support (reuse) | `support_support_case`, `support_case_message`, `support_access_grant` | Cases and access grants; support-bundle uploads are referenced from case messages (R2 object keys) (AF-SUP-01) |
| Audit (reuse) | `audit_audit_event`, `audit_operator_*` | Enrollment, revocation, remote commands, commerce and operator actions (writer and reader: AF-PLAT-01) |
| Platform (reuse) | `platform_command`, `platform_command_guard`, `platform_inbox`, `platform_outbox`, `platform_job_lease`, `platform_operating_budget`, `platform_operating_reservation` | Command dedup, webhook inbox, outbox to the relay, jobs (acknowledgement, purge) are implemented in the D1 storage layer. The operating-budget service is AF-PLAT-01. |
| Config (reuse) | `config_revision` | Kill switches, limits and the plan catalogue (AF-PLAT-01) |

## 3. Adaptations (migration notes)

| Change | Tables | Migration |
|---|---|---|
| Product ID domain gains `arcforges-node` and `arcforges-mobile` | `device_installation.product_id` and `identity_session.product_id`; today `CHECK (product_id IN ('arcscope', 'companion'))` | The `productId` type change regenerates the check constraints. SQLite cannot alter a CHECK, so the Cloud generator emits a table-rebuild migration (create new, copy, swap) under the repository's migration rules. Indexes are unchanged, because each node is its own device (§2). AF-CLD-01. |
| Operating dimensions gain `containerCpuSeconds` (8), `doRequests` (9), `d1RowsRead` (10), `d1RowsWritten` (11) and `pushSends` (12) | `platform_operating_budget.dimension` and `platform_operating_reservation.dimension`; today `CHECK (dimension IN (1..7))` | Same table-rebuild migration pattern as the product ID change. AF-PLAT-01. |
| Device platform values | `device_device.platform` already lists `windows`, `linux` and `android` | None |
| Push kinds | `notification_*` kind columns (text) | None (data) |
| Plan features | Entitlement configuration | Configuration revision (data) |

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
