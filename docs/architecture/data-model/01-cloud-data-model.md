# Cloud Data Model

P2-012 current implementation authorities: [Physical D1 mapping, fixed plans and recovery](04-d1-execution-profile.md); [Cloud opt-in and transient local-history body exclusion](05-application-history.md).

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Data model
> Governing authority: [`00-data-model-overview.md`](00-data-model-overview.md), [`../05-cloud-architecture.md`](../05-cloud-architecture.md) `§4`, `§5`
> Companions: [`../16-billing-and-commerce-architecture.md`](../16-billing-and-commerce-architecture.md), [`../08-security-architecture.md`](../08-security-architecture.md)

One D1 database, one logical schema per module (physical table prefixes under model 04, not PostgreSQL schemas) ([PS-01](../05-cloud-architecture.md#rule-ps-01)). A module owns its schema exclusively: no other module reads or writes its tables, and cross-module reference is by identifier plus a published module API ([MD-02](../05-cloud-architecture.md#rule-md-02), [MD-03](../05-cloud-architecture.md#rule-md-03)).

Notation is defined in [`00-data-model-overview.md`](00-data-model-overview.md) `§2`.

---

## 1. Schema map

| Schema | Module | Aggregates and owned records |
|---|---|---|
| `identity` | Identity | `user`, `auth_identity`, `session` |
| `workspace` | Workspace | `workspace` — **no membership table** ([WO-01](#rule-wo-01)) |
| `device` | Devices | `device`, `installation` |
| `entitlement` | Entitlement | `grant`, `snapshot`, `usage_counter`, `service_term`, `capacity_bucket`, `capacity_policy_period`, `capacity_reservation` |
| `commerce` | Commerce | `billing_account`, `order`, `subscription`, `credit_lot`, `provider_event`, `logical_ai_request`, `provider_attempt`, `attempt_usage`, `supplier_cost_entry`, `customer_settlement` |
| `notes` | Notes | `notebook` (owns `folder`), `document` (owns `block` and document metadata), `tag`, `property_definition`, `saved_view`; immutable revision records |
| `slate` | ArcSlate Cloud | Revisioned metadata replicas; native working authority remains local |
| `chat` | Chat | `conversation`, `message` and their committed content; Task owns iteration output, CF DO owns transient stream projection |
| `task` | Task | `task`, `automation_definition`, `automation_occurrence` |
| `agent` | Agent | `agent_profile`, `model_descriptor`, `tariff_version`, `supplier_price_version` |
| `sync` | Sync | `sync_scope`, `change` |
| `resource` | Resource | `cloud_object`, `upload_session` |
| `search` | Search | inference_job receipts; derived indexes are separately rebuildable |
| `package_catalog` | PackageCatalog | publisher, package, version, review, revocation |
| `notification` | Notification | `notification`, `push_registration` |
| `policy` | Policy | `policy_bundle` |
| `scope` | ArcScope Cloud | `simulation_definition`, `simulation_run`, `simulation_segment` (`§8.3`) |
| `config` | Configuration | `revision` — activated deployment policy (`§8.2`) |
| `audit` | Audit | `audit_event` |
| `support` | Support | `support_case`, `access_grant` |
| `trustsafety` | TrustSafety | `report`, `enforcement_action` |
| `platform` | shared infrastructure | `outbox`, `inbox`, `command`, `job_lease` |

---

## 2. `platform` — infrastructure tables

These exist once and are used by every module. They are the mechanism behind [TX-01](00-data-model-overview.md#rule-tx-01)–[TX-06](00-data-model-overview.md#rule-tx-06) and [OB-01](00-data-model-overview.md#rule-ob-01)–[OB-05](00-data-model-overview.md#rule-ob-05).

### `platform.command`

| Field | Type | Notes |
|---|---|---|
| `command_id` | `id` | **PK**. Allocated by the caller |
| `workspace_id` | `id?` | `NN` for workspace-scoped operations |
| `actor_ref` | `text NN` | De-identified actor reference |
| `operation` | `text NN` | The operation name, e.g. `chat.appendMessage` |
| `request_hash` | `text NN` | Hash of the canonical request, to detect a reused id with different content |
| `status` | `enum(inProgress, succeeded, failed) NN` | |
| `result_payload` | `json?` | The original response, retained for [TX-04](00-data-model-overview.md#rule-tx-04) |
| `result_rev` | `rev?` | The resulting aggregate revision |
| `error_code` | `text?` | Stable code when `failed` |
| `created_at` | `instant NN` | |
| `expires_at` | `instant NN` | Retention per `§7.1` of the overview |

- `UQ (command_id)`
- `IX (expires_at)` — the retention sweep
- **Constraint** — a second call with the same `command_id` and a different `request_hash` is rejected as `command.reused_identifier`, never executed

### `platform.outbox`

| Field | Type | Notes |
|---|---|---|
| `outbox_id` | `id` | **PK** |
| `aggregate_kind` | `text NN` | |
| `aggregate_id` | `id NN` | |
| `aggregate_rev` | `rev NN` | Revision **after** the change |
| `event_type` | `text NN` | |
| `payload` | `json NN` | |
| `workspace_id` | `id?` | |
| `correlation_id` | `id NN` | |
| `causation_id` | `id?` | |
| `state` | `enum(pending, dispatched, deadLettered) NN` | |
| `attempts` | `int NN` | |
| `created_at` | `instant NN` | |
| `dispatched_at` | `instant?` | |

- `IX (state, created_at)` — the dispatcher's only query path
- `IX (aggregate_kind, aggregate_id, aggregate_rev)` — replay for one aggregate

### `platform.inbox`

| Field | Type | Notes |
|---|---|---|
| `source` | `text NN` | **PK part 1** — the producing system |
| `message_id` | `text NN` | **PK part 2** |
| `received_at` | `instant NN` | |
| `processed_at` | `instant?` | Null while in flight |
| `outcome` | `enum(applied, duplicateIgnored, rejected) ?` | |
| `expires_at` | `instant NN` | |

- `PK (source, message_id)` — this composite key *is* the deduplication
- `IX (expires_at)`

### `platform.job_lease`

| Field | Type | Notes |
|---|---|---|
| `job_id` | `id` | **PK** |
| `job_type` | `text NN` | |
| `holder` | `text?` | Instance identity while leased |
| `leased_until` | `instant?` | |
| `attempts` | `int NN` | |
| `fence_token` | `bigint NN` | Incremented on each acquisition; checked under the lease-atomic D1 batch guard by every effect publication |
| `state` | `enum(ready, leased, succeeded, deadLettered) NN` | |
| `payload` | `json NN` | |
| `available_at` | `instant NN` | Backoff scheduling |

- `IX (state, available_at)` — the only claim path
- **Constraint** — acquisition conditionally updates `leased_until`, holder and `fence_token` together. A stale worker may still run after expiry but cannot commit an effect: every publication guards the current lease and fence in its registered D1 batch. Network uncertainty is handled by the dispatch barrier, not by the lease alone.

---

## 3. `identity`

### `identity.user`

| Field | Type | Notes |
|---|---|---|
| `user_id` | `id` | **PK** |
| `realm_id` | `id NN` | `FK →` realm; restrict |
| `display_name` | `text NN` | |
| `state` | `enum(active, restricted, suspended, pendingDeletion, deleted) NN` | |
| `created_at` | `instant NN` | |
| `deletion_requested_at` | `instant?` | Starts the grace period |
| `rev` | `rev NN` | Profile and credential-lifecycle guard |

- `IX (realm_id, state)`
- **Constraint** — a `deleted` user retains the row with all personal fields cleared; the identifier is never reused ([ID-05](00-data-model-overview.md#rule-id-05))

### `identity.auth_identity`

| Field | Type | Notes |
|---|---|---|
| `auth_identity_id` | `id` | **PK** |
| `user_id` | `id NN` | `FK →` `identity.user`; restrict |
| `method` | `enum(passkey, emailCode, password, oidc) NN` | |
| `subject` | `text NN` | Credential identifier — for passkey, the credential id |
| `public_key` | `blob?` | Passkey COSE public-key bytes only |
| `user_handle` | `blob?` | Stable opaque WebAuthn user handle, required for passkey |
| `backup_eligible`, `backup_state` | `bool?` | Passkey BE/BS flags; backup_state requires backup_eligible |
| `transports` | `json?` | Validated WebAuthn transport list; hint only, never authentication authority |
| `sign_count` | `bigint?` | Passkey counter observation; zero/synced counters follow the security 21 backup-aware policy, never unconditional account lockout |
| `label` | `text?` | User-visible name for the credential |
| `created_at` | `instant NN` | |
| `last_used_at` | `instant?` | |
| `revoked_at` | `instant?` | |
| `realm_id` | `id NN` | Configured realm, part of provider identity uniqueness |
| `provider_id` | `text NN` | Official passkey/email provider key or activated self-host provider |
| `password_hash` | `text?` | Versioned salted password verifier only for password; null otherwise |
| `rev` | `rev NN` | Credential mutation guard |

- `UQ (realm_id, provider_id, subject)` — one configured-provider credential belongs to one user; password stores a versioned salted hash, OIDC subject is the verified issuer subject
- `IX (user_id, revoked_at)` — listing a user's credentials
- **Constraint** — a user must retain **at least one** usable authentication identity or an active recovery path; removing the last one is refused as `identity.last_credential`

### `identity.email_address`

| Field | Type | Notes |
|---|---|---|
| `email_id` | `id` | **PK** |
| `user_id` | `id NN` | `FK →` `identity.user`; cascade on purge |
| `address_normalised` | `text NN` | Normalised for comparison |
| `verified_at` | `instant?` | |
| `purpose` | `enum(primary, recovery, notification) NN` | |

- `UQ (address_normalised, purpose)` where verified
- **Rule** — email is a **contact and recovery channel, never an identity** ([ID-01](../16-billing-and-commerce-architecture.md#rule-id-01) of the commerce architecture). Changing it never changes `user_id` and never affects entitlement.

<a id="browser-session-storage"></a>

### `identity.session`

| Field | Type | Notes |
|---|---|---|
| `session_id` | `id` | **PK** |
| `user_id` | `id NN` | `FK →`; cascade on purge |
| `device_id` | `id NN` | `FK →` `device.device`; restrict |
| `installation_id` | `id NN` | |
| `issued_at` | `instant NN` | |
| `expires_at` | `instant NN` | |
| `revoked_at` | `instant?` | |
| `credential_kind` | `enum(nativeBearer, browserCookie) NN` | Selects exactly one credential shape |
| `refresh_token_hash` | `text?` | Native bearer family only; hash only |
| `browser_handle_hash` | `text?` | Browser only; hash of cryptographically random 256-bit handle |
| `browser_origin` | `text?` | Browser only; exact configured Account or Chat origin |
| `idle_expires_at` | `instant?` | Browser only; never later than absolute expires_at |
| `last_activity_at` | `instant?` | Accepted interactive HTTP activity, not passive realtime keepalive |
| `session_policy_version` | `text NN` | Issuance policy reference; current revocation/tighter security policy still enforced |
| `refresh_generation` | `int?` | Native bearer only; reused superseded generation revokes the family |
| `step_up_at` | `instant?` | When step-up was last satisfied |
| `step_up_classes` | `JSON TEXT` | Which operation classes the step-up covers |
| `access_token_hash` | `text?` | Unique hash for nativeBearer; null for browserCookie |
| `access_expires_at` | `instant?` | Required with native access hash |
| `csrf_hash` | `text?` | Required for browserCookie; secret absent from storage |
| `purpose` | `AuthPurpose NN` | cancelDeletion limited API allowlist |
| `auth_epoch`, `recovery_generation`, `rev` | `bigint NN` | Current account/session and restore fences |
| `family_id` | `id?` | Native refresh family, required with refresh hash |
| `product_id` | `text NN` | Closed ProductId; installation binding |

- `IX (user_id, revoked_at, expires_at)` — active-session listing and mass revocation
- `IX (device_id)` — device revocation cascade
- Partial `UQ (refresh_token_hash)` for native sessions; partial `UQ (browser_handle_hash)` for browser sessions; `IX (browser_origin, idle_expires_at)` for browser expiry maintenance.
- **Exclusive credential check:** nativeBearer requires refresh hash/generation and null browser fields; browserCookie requires handle hash/origin/idle expiry and null refresh fields. The server accepts no browser cookie on the native bearer scheme.
- **Native constraint:** presenting a superseded refresh generation revokes the family and raises a security audit event.
- **Browser constraint:** exact origin, unrevoked user/device/installation/session, absolute expiry and idle expiry are checked before authorization. The random handle is issued only in a host-only HttpOnly cookie and stored as a hash; no plaintext refresh token is stored for the browser.
- **Browser creation:** verified authentication consumes its one-use pre-auth challenge and creates/validates the lowest-trust browser device and installation through the owning modules, then creates the session in the same enlisted transaction. Follow the declared Identity → Device statement order; the browser cannot supply a trusted device assertion. Lost login responses may require reauthentication; they never cause an operation replay with increased authority.
- **Activity:** update idle expiry with a conditional write only for an unrevoked, currently unexpired session, bounded by absolute expires_at. Concurrent requests cannot revive expired/revoked rows; passive hint polls/CF stream frames do not extend session life. Logout/revocation sets revoked_at before cookie deletion and terminates live connections. Already committed commands keep their recorded result.
- **Replica/restore:** every Cloud replica validates the same store. Database restore invalidates browser sessions under the existing security recovery procedure; explicit hashed CSRF tokens and session/pre-auth state support antiforgery across replicas. Authentication needs no replica affinity or in-memory-only session authority; business reads/control and AI presentation use the generated binary gRPC-Web unary/server-streaming contracts.
- **Cleanup:** expired handles and pre-auth challenges are purged by bounded Identity jobs after the security retention interval; secret hashes never enter application logs. User/device purge follows existing session FK/cascade rules.


### `identity.browser_auth_flow`

| Field | Type | Notes |
|---|---|---|
| `flow_id` | `id` | **PK**; public correlation ID, not sufficient proof of ownership |
| `binding_hash` | `text NN` | Hash of random pre-auth binding issued only in a host-only Secure/HttpOnly cookie |
| `origin` | `text NN` | Exact configured browser origin; method/RP expectations are server-set |
| `method` / `purpose` | `enum NN` | Existing passkey/email method and authentication/recovery/enrollment purpose |
| `challenge` | `json NN` | Typed, bounded method-specific public challenge plus server verification metadata; hash any email proof secret |
| `created_at` / `expires_at` | `instant NN` | Short server-policy lifetime; indexed expiry cleanup |
| `attempts` / `max_attempts` | `int NN` | Atomically bounded, with existing rate-limit keys |
| `consumed_at` | `instant?` | One-way terminal consumption; no client reset |
| `csrf_hash` | `text NN` | Hash of origin-bound preauthentication antiforgery secret |

The row plus its separate cookie binding and antiforgery validation bind a browser challenge; a flow ID alone grants no authority. Verify the existing method proof, then atomically compare the unconsumed/unexpired row, consume it and create the session/device in the registered transaction family. Duplicate completions fail safely. Expired/consumed rows are purged under the short challenge retention policy; logs never contain challenge proofs or binding secrets. Session bootstrap does not allocate an unbounded flow on every GET: beginAuthentication creates one under abuse limits. Explicit CSRF/session state is shared in D1; no framework Session/cookie-auth serialization is required.

### `identity.step_up_challenge`, `identity.recovery_flow`

| Table | Required fields / constraints |
|---|---|
| identity.step_up_challenge | challenge_id:id PK; user_id/session_id:id FK NN; operation_class/target_hash/method:text NN; proof_hash:hash NN; state:enum(pending,proved,consumed,expired,denied) NN; attempt_count:int NN CHECK 0..5; created_at/expires_at:instant NN; consumed_at:instant?; auth_epoch/recovery_generation:bigint NN; rev:rev NN; IX(session_id,expires_at). |
| identity.recovery_flow | flow_id:id PK; realm_id:id NN; user_id:id?; method:RecoveryMethod NN; proof_hash:hash NN; replacement_challenge:blob?; state:enum(pending,proved,completed,expired,denied) NN; attempt_count:int NN CHECK 0..5; rate_limit_key:text NN; created_at/expires_at:instant NN; completed_at:instant?; auth_epoch/recovery_generation:bigint NN; rev:rev NN; IX(expires_at). No credential replacement before bound proof. |



Short-lived rows with `expires_at`, an attempt counter, and a rate-limit key. Both are swept on expiry. A recovery flow records every state transition for the audit trail, because recovery is the highest-value attack surface in the system.

---

<a id="account-state-and-proof-constraints"></a>
### Account proofs and lifecycle records

User/profile and credential columns are defined above once; avatar changes enlist Resource when required. Provider configuration is versioned and references deployment secrets. Workspace enforces UQ(realm_id,owner_user_id). Official enrollment creates no service grant; explicit sourced grants are unique by owner/source action, not session or installation.

| Identity-owned record | Required fields and constraints |
|---|---|
| spent_refresh | token_hash:hash PK; session_id/family_id:id FK NN; generation:bigint NN; consumed_at/family_expires_at:instant NN; UQ(family_id,generation). Retain through family expiry plus 60-second skew. Rotation guards the family revision, inserts the spent hash and replaces current hash atomically. |
| recovery_code | code_hash:hash PK; set_id/user_id:id NN; issued_at:instant NN; consumed_at/invalidated_at:instant?; IX(user_id,set_id). One live set per user; consumption requires both code and set active. |
| api_token | token_id:id PK; user_id/workspace_id:id FK NN; secret_hash:hash UNIQUE NN; name:text NN; scopes:canonical JSON array of exact operation IDs NN; created_at/expires_at:instant NN; last_used_at/revoked_at:instant?; rev:rev NN; auth_epoch/recovery_generation:bigint NN; IX(user_id,revoked_at). No reusable plaintext. |
| security_flow | flow_id:id PK; kind/purpose:Key NN; provider:text?; user_id/installation_id/device_id:id?; origin:text?; proof_hash/target_payload_hash:hash NN; expires_at:instant NN; attempts:int NN; consumed_at:instant?; payload_proto:typed flow payload NN. Native authorization code rows are identity.native_authorization; this coordinator references flow_id, never stores a second code. Other kinds are enrollment, emailChange, providerCallback, deletionReauth. Consumption and owner/session effect share one batch. |
| device remote policy | device.remote_policy: device_id:id PK/FK; allowed_capabilities/local_confirmation_capabilities:canonical Key arrays NN; rev:rev NN. Device-owned, not a heartbeat claim. |
| workspace data deletion | workspace.data_deletion: deletion_id:id PK; workspace_id:id FK NN; preview_hash:hash NN; captured_revision:rev NN; state:enum(pending,running,completed,failed) NN; owner_job_inventory:canonical JSON of owner/job/receipt references NN; completed_at:instant?; rev:rev NN. Bounded jobs retain restartable progress, purge fence and resource release receipts. |

Account proof changes and their Notification outbox are one Identity + Notification shared unit; profile avatar changes additionally enlist Resource/Entitlement. Workspace data deletion uses the existing owner content/reference-release shared family per batch and a Workspace coordinator outbox, never a transaction spanning all content and object storage. Security flow completion that creates a session uses the authentication family. The independently retained safety receipts in deployment architecture fence post-restore reuse and access resurrection.


### Native authorization and operator records

| Table | Fields / constraints |
|---|---|
| identity.native_authorization | flow_id:id PK; realm_id:id NN; installation_id:id NN; client_id/redirect_uri/state_hash/pkce_challenge:text NN; code_hash:text? UNIQUE; user_id/session_id:id?; created_at/expires_at:instant NN; code_expires_at/consumed_at:instant?; attempt_count:int NN CHECK 0..5; rev:rev NN. Exact code/PKCE/origin/installation guarded consumption creates the session atomically; no plaintext code/verifier. |
| identity.operator_session | session_id:id PK; provider_id/subject/tenant_id:text NN; handle_hash:text UNIQUE NN; issued_at/expires_at:instant NN; revoked_at:instant?; auth_epoch/recovery_generation:bigint NN. Customer credential scheme cannot read it. |
| identity.operator_access | provider_id/subject/role:text composite PK; granted_by:text NN; expires_at/revoked_at:instant?; rev:rev NN. Roles from registry 04 §9 only. |
| identity.operator_action | action_id:id PK; proposer:text NN; approver:text?; operation_id/proposal_hash:text NN; evidence_ref:text NN; state:text NN; expires_at/created_at:instant NN; consumed_at:instant?; rev:rev NN. Dual-control operations require different active subjects and exact proposal hash. |

## 4. `workspace`

### `workspace.workspace`

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | `id` | **PK** |
| `realm_id` | `id NN` | |
| `owner_user_id` | `id NN` | `FK →` `identity.user`; restrict |
| `name` | `text NN` | |
| `data_region` | `text NN` | Immutable after creation |
| `protection_profile` | `enum(standard) NN` | |
| `state` | `enum(active, suspended, pendingDeletion) NN` | |
| `created_at` | `instant NN` | |
| `rev` | `rev NN` | |

- `UQ (realm_id, owner_user_id)` — one personal workspace per realm

- `IX (owner_user_id, state)`
- **Constraint** — `data_region` is immutable; moving a workspace between regions is a realm migration operation that creates a new workspace and migrates content ([WP-46.05](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.05)), never an update

### Workspace ownership — no membership table

**[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) excludes organisations, membership, invitations, collaborative editing and collaboration-only schema hooks.** The `workspace.membership` table of the previous baseline was exactly such a hook: one row per workspace, one role value, no V1 writer. It is **removed**, not retained empty.

| # | Rule |
|---|---|
| <a id="rule-wo-01"></a>WO-01 | **Ownership is `workspace.owner_user_id`**, a single non-null column. There is no join table, no role column and no seat concept. |
| <a id="rule-wo-02"></a>WO-02 | **Authorization is `Actor → owns → Workspace → Resource`.** The previous `Actor → Membership → Workspace → Resource` chain collapses to a direct ownership check ([MT-02](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-02) of the cloud architecture is amended accordingly). |
| WO-03 | **A workspace is a multi-device boundary, not a collaboration unit.** Several devices of one owner share it; no second principal ever holds rights in it. |
| <a id="rule-wo-04"></a>WO-04 | **Re-introducing membership is an architecture baseline change**, not an additive migration. Retaining a dormant table would have made it look like a configuration switch, which is precisely the ambiguity [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) removes. |
| <a id="rule-wo-05"></a>WO-05 | **A repository policy test rejects customer workspace membership, role, invitation, seat and shared-editor concepts.** Separate operator authorization roles and self-host account enrollment are not workspace membership. |

> **Retired identifier.** `workspace.membership` is retired by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) and is not reused for another purpose. Its historical definition is in the git history of this document at `7ed79a6`.

---

### Resumable owner-data transfer

| Table | Required fields / constraints |
|---|---|
| workspace.transfer_job | transfer_id:id PK; workspace_id:id FK NN; direction:enum(import,export) NN; state:TransferState NN; manifest_hash:hash NN; manifest_resource_id:id?; preview_hash:hash?; rev:rev NN; created_at:instant NN; expires_at:instant?; committed_roots/total_roots:bigint NN; reason:ReasonCode?; IX(workspace_id,state,created_at). |
| workspace.transfer_mapping | transfer_id:id FK + source_kind:text + source_id:id composite PK; target_kind:text NN; target_id:id NN; state:TransferState NN; source_hash:hash NN; target_rev:rev?; receipt_id:id?; UQ(transfer_id,target_kind,target_id). |
| workspace.transfer_issue | transfer_id:id FK + ordinal:bigint composite PK; code:ReasonCode NN; source_kind:text?; source_id:id?; blocks_commit:bool NN; accepted_at:instant?. |



Job owner may coordinate but each imported content handler writes only its own tables in the declared shared family. Batch<=100 roots and complete mapping validation precede visibility; committed root receipts and IDs survive retry. Policy/quota/revision change invalidates preview or blocks the next root without rewriting past receipts. All mappings/issues are paged. Excluded authority and missing/unsupported bytes follow the journey profile, not blind copying of DB rows.

Data-health states detected/repairing/repaired/irrecoverable/acknowledged preserve last evidence/source hashes. Irrecoverable is not repaired; explicit replacement creates a new resource revision. No recovery job fabricates missing bytes or erases the anomaly to make a gate green.


## 5. `device`

### `device.device`

| Field | Type | Notes |
|---|---|---|
| `device_id` | `id` | **PK** |
| `user_id` | `id NN` | `FK →`; restrict |
| `display_name` | `text NN` | User-editable |
| `platform` | `enum(windows, macos, linux, android, ios, web) NN` | |
| `trust_level` | `enum(untrusted, trusted) NN` | Default `untrusted` |
| `trust_raised_at` | `instant?` | Requires step-up ([WP-22.03](../../planning/work-packages/22-identity-workspace-and-device.md#rule-wp-22.03)) |
| `remote_enabled` | `bool NN` | Default **false** |
| `first_seen_at` | `instant NN` | |
| `last_seen_at` | `instant NN` | |
| `revoked_at` | `instant?` | |
| `rev` | `rev NN` | |

- `IX (user_id, revoked_at)`
- **Constraint** — device identity is **not** a hardware fingerprint ([BR-08](../../planning/work-packages/22-identity-workspace-and-device.md#rule-br-08) of [WP-22](../../planning/work-packages/22-identity-workspace-and-device.md#rule-wp-22)). It is a server-issued identifier the client stores in secure storage and survives ordinary hardware change.
- **Constraint** — `remote_enabled` cannot be set true without `trust_level = trusted` **and** a step-up within the validity window.

### `device.installation`

| Field | Type | Notes |
|---|---|---|
| `installation_id` | `id` | **PK** |
| `device_id` | `id NN` | `FK →`; cascade |
| `product_id` | `text NN` | arcnotes / arcscope / arcslate / companion; platform is a separate field |
| `app_version` | `text NN` | |
| `contract_set_version` | `text NN` | Drives the compatibility window |
| `installed_at` | `instant NN` | |
| `last_active_at` | `instant NN` | |
| `platform` | `text NN` | windows/linux/macos/android/web |
| `public_key`, `key_version` | `text NN`, `bigint NN` | Installation proof and rotation |
| `revoked_at` | `instant?` | Revokes sessions, presence and delivery eligibility |
| `rev` | `rev NN` | Installation authorization guard |

- `UQ (device_id, product_id)`
- `IX (contract_set_version)` — the minimum-version rollout query ([UP-11](../../requirements/10-distribution-update-and-support.md#rule-up-11))

### Application presence projection

No device.presence D1 table exists. ApplicationPresence DO partitions `(realm,workspace,product,installation)` with deviceId, instanceEpoch, state, capabilities digest, lastSeenAt and expiresAt. Heartbeat lease is 30 seconds, renewed every 10 seconds. On expiry the projection is offline regardless of a surviving session. Trust, remote policy and installation revocation remain durable D1 authority and are rechecked on delivery/result. Device lists derive live children from Application.List; disconnected is not uninstalled. No second device heartbeat or InstancePresence model exists.

## 6. `entitlement`

The Entitlement module is **independent of Commerce** (`§2.1` of the commerce architecture). Nothing here references a `commerce` table.

### `entitlement.grant`

| Field | Type | Notes |
|---|---|---|
| `grant_id` | `id` | **PK** |
| `workspace_id` | `id NN` | |
| `kind` | `enum(capability, quota, allowance) NN` | Grant-row kinds only; consumable balances are Commerce ledger/lot projections |
| `subject` | `text NN` | The capability, quota or feature key |
| `value` | `json NN` | Kind-specific payload — a limit, a bundle reference, a boolean |
| `source` | `enum(Subscription, CloudPass, StorageAddOn, PurchasedCredit, AdminGrant, Migration, Compensation) NN` | **No provider identifier appears here** ([EO-04](../16-billing-and-commerce-architecture.md#rule-eo-04)) |
| `source_ref` | `text?` | An opaque reference the issuing module understands |
| `effective_from` | `instant NN` | |
| `effective_until` | `instant?` | Null = open-ended |
| `issued_by_actor` | `text NN` | For administrative grants, the operator |
| `created_at` | `instant NN` | |

- **Append-only.** No update, no delete ([EN-01](../16-billing-and-commerce-architecture.md#rule-en-01) of the commerce architecture)
- `IX (workspace_id, kind, effective_from)` — the resolver's only scan path
- `IX (source, source_ref)` — reconciliation lookup

### `entitlement.revocation`

| Field | Type | Notes |
|---|---|---|
| `revocation_id` | `id` | **PK** |
| `grant_id` | `id NN` | `FK →` `entitlement.grant`; restrict |
| `reason_code` | `text NN` | |
| `effective_from` | `instant NN` | |
| `issued_by_actor` | `text NN` | |
| `created_at` | `instant NN` | |

- **Append-only.** A revocation is how a grant ends; the grant row is never mutated
- `IX (grant_id)`

### `entitlement.snapshot`

*(derived — always rebuildable from grants and revocations, [EN-02](../16-billing-and-commerce-architecture.md#rule-en-02))*

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | `id` | **PK** |
| `entitlement_version` | `bigint NN` | Increments on every change; clients compare this |
| `computed_at` | `instant NN` | |
| `valid_until` | `instant?` | The next time-based transition, so the resolver knows when to recompute |
| `capabilities` | `json NN` | Capability → `{granted, reason, sourceGrantId}` |
| `quotas` | `json NN` | Quota key → `{limit, reason, sourceGrantId}` |
| `features` | `json NN` | |

- **Constraint** — a rebuild must equal the stored snapshot for every fixture account ([WP-42.04](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.04)). A difference is a defect, not a refresh.
- **Rule** — `valid_until` exists so the resolver is deterministic without a clock scan: the sweeper recomputes exactly the workspaces whose `valid_until` has passed.

### `entitlement.usage_counter`

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | `id` | **PK part 1** |
| `quota_key` | `text NN` | **PK part 2** |
| `period_start` | `instant NN` | **PK part 3** — tied to the entitlement period, not the calendar |
| `used` | `bigint NN` | |
| `updated_at` | `instant NN` | |

- **Constraint** — the period boundary comes from the entitlement snapshot, never from a calendar convenience ([QA-02](../16-billing-and-commerce-architecture.md#rule-qa-02))
- **Constraint** — this is a display/reconciliation projection over durable quota events and measured objects. Admission guards current `quota_budget` revisions and reserves atomically, never trusts this projection. Storage is a non-resetting gauge; period-based simulator/egress usage carries its explicit period.

---


### `entitlement.service_term` *(new — [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006); keys corrected 2026-09-07)*

The gate before every AI decision (`§5.3` of the commerce architecture). An interval, never a flag.

> **Corrected 2026-09-07.** The previous definition set `source_ref` to the subscription id under `UQ (kind, source_ref)`. That made **renewal impossible**: the second paid period of the same subscription would collide on the key. Three identities were conflated, and are now separate.

| Identity | Meaning | Lives in |
|---|---|---|
| **Subscription identity** | The provider's long-lived subscription | `subscription_ref` |
| **Paid-period identity** | *One* paid interval of it | `period_ref` — the key |
| **Provider-event identity** | The webhook that caused this row | `commerce.provider_event`, deduplicated there ([EI-02](../16-billing-and-commerce-architecture.md#rule-ei-02)) |

| Field | Type | Notes |
|---|---|---|
| `service_term_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` `workspace.workspace`; restrict |
| `realm_id` | `id NN` | **Realm-scoped**; a term is never visible outside its realm ([SV-04](../16-billing-and-commerce-architecture.md#rule-sv-04)) |
| `kind` | `enum(subscription, pass, compensation, selfHostGrant) NN` | The only four sources ([SV-02](../16-billing-and-commerce-architecture.md#rule-sv-02)) |
| `subscription_ref` | `text?` | The provider subscription, for `kind = subscription`. **Stable across renewals** |
| `period_ref` | `text NN` | **Normalized domain service-period identity**, minted once by the owner admission/adapter mapping; provider invoice/billing identifiers stay in Commerce. Pass/order and grant references are normalized domain IDs. |
| `starts_at` | `instant NN` | |
| `ends_at` | `instant NN` | Exclusive |
| `grace_ends_at` | `instant?` | Data-access grace; **never extends AI admission** ([SV-05](../16-billing-and-commerce-architecture.md#rule-sv-05)) |
| `supersedes_id` | `id?` | Logical predecessor for an explicit plan change; never authorises editing its interval |
| `offer_id`, `offer_snapshot_id` | `id NN` | The purchased/granted capacity offer and immutable commercial version |
| `authorized_at` | `instant NN` | Server-recorded verification time; effective service begins no earlier than this time |
| `selection_priority` | `bigint NN` | Server-issued plan-selection generation pinned to the checkout/grant intent, not webhook delivery order |
| `created_at` | `instant NN` | |

- `UQ (realm_id, kind, period_ref)` — **idempotent creation per period.** A replayed provider event for the same period creates nothing; a genuine renewal carries a **new** `period_ref` and creates a new row ([SV-02](../16-billing-and-commerce-architecture.md#rule-sv-02))
- `IX (workspace_id, starts_at, ends_at)` — the admission-path query
- `IX (subscription_ref, starts_at)` — the renewal-chain query
- **Constraint** — `ends_at > starts_at`
- **Constraint** — `kind = 'subscription'` requires `subscription_ref IS NOT NULL`; the other kinds require it to be `NULL`
- **Constraint** — no row is created from a credit grant, a trial flag or an operator balance edit ([SV-03](../16-billing-and-commerce-architecture.md#rule-sv-03)), enforced by the grant interface

| # | Rule |
|---|---|
| <a id="rule-tm-01"></a>TM-01 | Effective eligibility is the union of `[max(starts_at, authorized_at), ends_at)` after applying effective revocations. Scheduled renewals verified before their start abut normally. A late verification does not retrospectively authorise calls, refill a past gap or rewrite prior settlement. The original paid invoice interval remains available for reconciliation/compensation. |
| <a id="rule-tm-02"></a>TM-02 | Provider events and paid periods have separate idempotency keys. A replay cannot create a second interval or change the checkout's plan-selection priority. |
| <a id="rule-tm-03"></a>TM-03 | Contiguity is calculated from **effective** intervals after actions. Initialisation is recorded once against the effective run-opening term and boundary, never once per webhook or per overlapping offer. |
| <a id="rule-tm-04"></a>TM-04 | Term rows are immutable. Supersession/revocation is an append to `service_term_action(term_action_id PK, term_id, kind, effective_at, recorded_at, source_ref UNIQUE, replacement_term_id?)`. The original `ends_at` is never rewritten. In the guarded workspace/bucket batch, advance capacity first; operational changes take effect at `max(server_now, watermark_at)`. A provider's earlier event time is evidence, not a backdated change to served history. |
| <a id="rule-tm-05"></a>TM-05 | One capacity offer applies at each instant: select the eligible term with highest pinned `selection_priority`, then `service_term_id` for a stable tie break. Subscription renewals retain their plan generation; an explicitly selected new plan/pass/grant has a new generation. An old delayed webhook cannot override a newer selection. Grace is excluded. When the selected term ends, resolve the remaining eligible set. Rates and bursts are never summed. |
| TM-06 | `capacity_plan_assignment(assignment_id PK, workspace_id, offer_id, term_id, selection_priority, effective_from, effective_to?, cause_ref)` records the non-overlapping resolved timeline. All known term starts/ends/actions are resolution boundaries; lazy advancement first materialises these boundaries under the guarded bucket revision. Only closing a current assignment and appending its successor is permitted. The refill join is assignment.offer_id → policy period at that instant, never the workspace's current offer applied to its whole history. |

### `entitlement.service_term_action`, `entitlement.capacity_plan_assignment`

| Table | Required fields / constraints |
|---|---|
| entitlement.service_term_action | term_action_id:id PK; term_id:id FK NN; kind:enum(supersede,revoke) NN; effective_at/recorded_at:instant NN; source_ref:text NN UNIQUE; replacement_term_id:id? FK; supersede requires replacement_term_id, revoke forbids it; both terms share realm/workspace; append-only under TM-04. |
| entitlement.capacity_plan_assignment | assignment_id:id PK; workspace_id/offer_id/term_id:id FK NN; selection_priority:bigint NN; effective_from:instant NN; effective_to:instant?; cause_ref:id NN; UQ(workspace_id,effective_from); IX(workspace_id,effective_to); non-overlap and closing/appending are guarded by the workspace bucket revision under TM-06. |

### `entitlement.capacity_bucket` *(new — [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006); refill corrected 2026-09-07)*

One row per workspace. The replenishing included-capacity bucket (`§7.2` of the commerce architecture).

> **Corrected 2026-09-07.** The previous definition stored `burst_micro` and `rate_micro_per_second` **on the bucket row**, and refill multiplied the whole elapsed interval by that single rate. That is wrong whenever the configured rate changed inside the interval: five seconds at rate 1 followed by five seconds at rate 10 earns **55**, not 100. Rate and burst now come from **immutable policy history**, and refill integrates over the intervals actually in force.

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | `id` | **PK** — exactly one bucket per workspace |
| `available_micro` | `int64 NN` | Integer micro-credits ([CD-01](../16-billing-and-commerce-architecture.md#rule-cd-01)). **Never a float** |
| `held_micro` | `int64 NN` | Sum of live reservations funded from capacity ([CX-08](#rule-cx-08)) |
| `remainder_num`, `remainder_den` | `int64 NN` | **Exact fractional carry** as a rational ([RF-03](../16-billing-and-commerce-architecture.md#rule-rf-03)). Never a float, never truncated |
| `watermark_at` | `instant NN` | **Monotonic** ([RF-02](../16-billing-and-commerce-architecture.md#rule-rf-02)); advanced, never rewound |
| `activation_term_id` | `id?` | `FK →` `entitlement.service_term` — the term that opened the **current contiguous run** ([RF-07](../16-billing-and-commerce-architecture.md#rule-rf-07), [TM-03](#rule-tm-03)) |
| `rev` | `rev NN` | |

- **Constraint** — `available_micro >= 0`, `held_micro >= 0`
- **Constraint** — `available_micro` may **never be increased** past `GREATEST(available_micro_before, GREATEST(0, burst_in_force - held_micro))` by any operation ([RF-04](../16-billing-and-commerce-architecture.md#rule-rf-04), [RF-05](../16-billing-and-commerce-architecture.md#rule-rf-05) of the commerce architecture). It is a **bound on the increase, not on the resting value**, and the difference is not pedantry: a ceiling reduction leaves a balance legitimately above the new ceiling ([RF-05](../16-billing-and-commerce-architecture.md#rule-rf-05)), so a `CHECK` on the row would reject the workspace's *next unrelated write* and strand the bucket. Enforced by the update predicate, which no path may bypass
- **Constraint** — `watermark_at` is non-decreasing, enforced by a checked update predicate ([RF-02](../16-billing-and-commerce-architecture.md#rule-rf-02))
- **Rule** — burst and rate are **not columns here.** They are read from `entitlement.capacity_policy_period`, so a configuration change cannot silently rewrite a bucket's parameters or its history

### `entitlement.capacity_policy_period` *(new — 2026-09-07)*

Immutable policy history. One row per `(realm, offer, activation interval)` in which the capacity parameters were constant.

| Field | Type | Notes |
|---|---|---|
| `policy_period_id` | `id` | **PK** |
| `realm_id`, `offer_id` | `id NN` | |
| `config_revision_id` | `id NN` | `FK →` `config.revision` — which activated revision supplied these values ([CG-02](../16-billing-and-commerce-architecture.md#rule-cg-02)) |
| `burst_micro` | `int64 NN` | |
| `rate_micro_per_second` | `int64 NN` | |
| `effective_from` | `instant NN` | The activation instant of that revision |
| `effective_to` | `instant?` | NULL while current; set when the next revision activates |

- `UQ (realm_id, offer_id, effective_from)`
- `IX (realm_id, offer_id, effective_from, effective_to)` — the integration query
- **Constraint** — a row is **never updated except to close `effective_to`**, and never deleted ([I-494](../../requirements/01-normative-glossary-and-invariants.md#rule-i-494))
- **Constraint** — periods for one `(realm, offer)` are contiguous and non-overlapping; closing one and opening the next happens in the **activation transaction** ([CA-03](../22-deployment-and-release-execution.md#rule-ca-03)), so no instant is uncovered or double-covered

#### The refill calculation

> **The algorithm lives in one place, and this is not it.** It is `§7.2` of [the billing and commerce architecture](../16-billing-and-commerce-architecture.md), with its rules [RF-01](../16-billing-and-commerce-architecture.md#rule-rf-01)–[RF-11](../16-billing-and-commerce-architecture.md#rule-rf-11). This section previously restated it and **the two copies had diverged**: the restatement summed every window and applied one ceiling from `burst_at(now)`, instead of saturating at each period's own ceiling in chronological order, and its assignment omitted the `max(available, cap)` clause. Worked examples of the divergence — a ceiling that rises mid-interval yields 15 under the corrected algorithm and 20 under the restatement; a ceiling reduction yields 50 against 10, confiscating balance that [RF-05](../16-billing-and-commerce-architecture.md#rule-rf-05) says is preserved. A second copy of an algorithm is a second answer, so this one is removed rather than re-synchronised.

**What this schema must provide for it**, and all that belongs here:

| Need | Supplied by |
|---|---|
| The integration lower bound, durable and monotonic | `capacity_bucket.watermark_at` ([RF-02](../16-billing-and-commerce-architecture.md#rule-rf-02)) |
| Exact fractional carry across period boundaries | `capacity_bucket.remainder_num` / `remainder_den` ([RF-03](../16-billing-and-commerce-architecture.md#rule-rf-03)) |
| The eligible-service interval set | `entitlement.service_term`, unioned by [TM-01](#rule-tm-01) |
| The selected offer and its policy at each instant | `capacity_plan_assignment` joined to `capacity_policy_period`; both non-overlapping for their scope |
| Held capacity, constant between bucket mutations | `capacity_bucket.held_micro`; every mutation advances under the old value first; reconciled by [CX-08](#rule-cx-08) |
| Serialisation of racing replicas | The `capacity_bucket` atomic D1 batch guard ([RF-02](../16-billing-and-commerce-architecture.md#rule-rf-02)) |
| The one contiguous run, so initialisation happens once | `capacity_bucket.activation_term_id` with [TM-03](#rule-tm-03) ([RF-08](../16-billing-and-commerce-architecture.md#rule-rf-08)) |

**Cross-checks this schema owes the algorithm.** [CX-08](#rule-cx-08) reconciles `held_micro` against live reservations. [CX-11](#rule-cx-11) asserts that no stored `available_micro` was produced by an increase past the bound above — the property the removed `CHECK` was reaching for, expressed where it is actually true.

### `entitlement.capacity_reservation` *(new — [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006))*

| Field | Type | Notes |
|---|---|---|
| `reservation_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` `entitlement.capacity_bucket` |
| `logical_request_id` | `id NN` | Normalized request identity; no Commerce FK. Entitlement standalone owner operations preserve the same uniqueness/fence. |
| `from_capacity_micro` | `int64 NN` | Portion held against the bucket |
| `from_compensation_micro` | `int64 NN` | Portion held against compensation lots |
| `from_purchased_micro` | `int64 NN` | Portion held against purchased lots — **non-zero only under an extra-usage authorisation** ([AD-05](../16-billing-and-commerce-architecture.md#rule-ad-05)) |
| `state` | `enum(held, settled, released, expired) NN` | |
| `expires_at` | `instant NN` | Swept when passed ([UU-03](../20-cross-system-lifecycles.md#rule-uu-03) of the cross-system lifecycles) |
| `created_at` | `instant NN` | |

- `IX (workspace_id, state)`, `IX (state, expires_at)` — the sweeper path
- **Constraint** — the three source columns record the allocation, and settlement debits and releases **against the same sources** ([CD-06](../16-billing-and-commerce-architecture.md#rule-cd-06), [ST-05](../16-billing-and-commerce-architecture.md#rule-st-05))
- **Constraint** — a `from_purchased_micro > 0` row requires a live extra-usage authorisation reference
### `entitlement.quota_budget`, `quota_reservation`, `quota_event`

| Table | Required shape and constraints |
|---|---|
| `quota_budget` | PK `(scope_kind, scope_id, quota_key, period_key)`; scope is workspace or deployment, period is explicit entitlement period or `gauge`; `unit`, `limit`, `used`, `held`, `policy_version`, `rev`. Non-negative checked int64 quantities. The limit is resolved from sourced grants; a downgrade may leave `used + held > limit` but cannot authorise a new increase. |
| `quota_reservation` | PK reservation ID; unique `(operation_id, budget_key)`; budget reference, owner kind/id, bound, consumed, state `held/settled/releasing/released`, expiry, lease/fence where applicable. Check consumed ≤ bound; enlarging requires a new atomic admission before the extra work. |
| `quota_event` | Immutable unique `(reservation_id, effect_id)`; typed consume/release/adjust event, measured quantity, resulting budget revision, source object/segment/deletion receipt. Replays return the prior receipt. Gauges decrement only through verified deletion or replacement effects; period use never resets by restarting a job. |

Admission guards all budget revisions in one fixed batch, checks `used + held + bound <= limit`, and inserts all reservations in one shared unit of work. A multi-limit operation either reserves all limits or none. Declared upload size and deterministic simulation bounds are conservative admission maxima; server measurement is settlement authority. Concurrency has separate leased slots, not sample/byte units.

Storage reserves both future committed headroom and workspace/deployment staging headroom at upload start. Promotion atomically converts committed headroom to measured used bytes and releases only unused allocation; physical staging exposure persists until any duplicate/staging copy is deleted. Current/history/trash/conflict/export pins keep an object live. Releasing its final pin starts GC, which records verified object deletion before freeing physical/storage gauge use. Quota repair appends an audited adjustment from a verified inventory and never overwrites history.

Simulation admission reserves bounded duration, sample count, output bytes and egress under its service term and template snapshot. Each fenced segment-publication transaction records measured consumption and object pins; completion/cancellation releases unused budgets. Period rollover cannot migrate outstanding old-period reservations into a fresh empty budget. The lease sweeper uses the same fenced publication/cleanup paths.

## 7. `commerce`

### `commerce.billing_account`

| Field | Type | Notes |
|---|---|---|
| `billing_account_id` | `id` | **PK** — the stable internal buyer identity ([ID-01](../16-billing-and-commerce-architecture.md#rule-id-01)) |
| `owner_user_id` | `id NN` | |
| `created_at` | `instant NN` | |
| `rev` | `rev NN` | |

- **Rule** — **never keyed by email.** A payment email such as a shared finance mailbox must not determine ownership.

### `commerce.provider_customer`

| Field | Type | Notes |
|---|---|---|
| `billing_account_id` | `id` | **PK part 1** |
| `provider` | `text NN` | **PK part 2** |
| `external_customer_ref` | `text NN` | The provider's identifier, held as an external reference ([MB-03](../16-billing-and-commerce-architecture.md#rule-mb-03)) |

- `UQ (provider, external_customer_ref)`
- **Rule** — provider-specific key components stay inside Commerce adapter/mapping tables; Entitlement has no provider identifier dependency

### `commerce.offer`, `commerce.price_version`

| Table | Required fields / constraints |
|---|---|
| commerce.offer | offer_id:id PK; kind:enum(subscription,pass,credit,storageAddOn) NN; name:text NN; scope:text NN; active:bool NN; term_profile:text NN; created_at:instant NN; rev:rev NN. Only currently accepted CT-05 kinds are activated. |
| commerce.price_version | price_version_id:id PK; offer_id:id FK NN; version:bigint NN; amount:money NN; tax_category:text NN; starts_at:instant NN; ends_at:instant?; config_revision_id:id NN; UQ(offer_id,version); IX(offer_id,starts_at). Immutable/restrict-delete once referenced. |



Workspace-independent catalogue rows ([MT-04](00-data-model-overview.md#rule-mt-04)). An `offer` names what is sold; a `price_version` carries the amounts, currency, effective dates and tax category. **A price change creates a new `price_version`; existing orders retain the version they were bought under** ([PC-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-pc-01)), so `order.price_version_id` is a restrict-delete foreign key and a price version is never mutated.

### `commerce.purchase_intent`

| Field | Type | Notes |
|---|---|---|
| `purchase_intent_id` | `id` | **PK** — the idempotency anchor for the whole chain ([PU-03](../16-billing-and-commerce-architecture.md#rule-pu-03)) |
| `billing_account_id` | `id NN` | `FK →`; restrict |
| `workspace_id` | `id NN` | Entitlement target |
| `offer_id` | `id NN` | |
| `price_version_id` | `id NN` | |
| `state` | `enum(open, checkoutStarted, completed, expired, abandoned) NN` | |
| `created_at` | `instant NN` | |
| `expires_at` | `instant NN` | |

- `UQ (purchase_intent_id)`; `IX (state, expires_at)` — the expiry sweeper
- **Constraint** — at most one `checkout_attempt` in a non-terminal state per intent, enforced by a partial unique index. This is what makes [PU-02](../16-billing-and-commerce-architecture.md#rule-pu-02) true.

### `commerce.checkout_attempt`

| Table | Required fields / constraints |
|---|---|
| commerce.checkout_attempt | attempt_id:id PK; intent_id/billing_account_id/workspace_id/offer_id/price_version_id:id FK NN; provider:text NN; external_session_ref:text?; state:enum(prepared,created,unknown,completed,expired,failed) NN; request_hash:hash NN; created_at/expires_at:instant NN; rev:rev NN; UQ(provider,external_session_ref); IX(intent_id,created_at). Provider outcome after dispatch may be unknown; browser return cannot advance it. |



Carries the internal metadata sent to the provider ([ID-04](../16-billing-and-commerce-architecture.md#rule-id-04)): billing account, workspace, offer, price version, attempt and intent identifiers. Holds the provider's session reference and its own expiry. **A success redirect writes nothing here** ([PU-01](../16-billing-and-commerce-architecture.md#rule-pu-01)) — only a verified provider event advances state.

### `commerce.provider_event`

| Field | Type | Notes |
|---|---|---|
| `provider_event_id` | `id` | **PK** |
| `provider` | `text NN` | |
| `external_event_id` | `text NN` | |
| `event_type` | `text NN` | |
| `raw_payload` | `json NN` | Retained for dispute evidence and replay ([EI-08](../16-billing-and-commerce-architecture.md#rule-ei-08)) |
| `signature_verified` | `bool NN` | |
| `received_at` | `instant NN` | |
| `processing_state` | `enum(received, processed, quarantined) NN` | |
| `retry_count` | `int NN` | |
| `quarantine_reason` | `text?` | |

- `UQ (provider, event_type, external_event_id)` — **this composite key is the idempotency of [EI-02](../16-billing-and-commerce-architecture.md#rule-ei-02)**
- `IX (processing_state, received_at)` — backlog age, a page-worthy alert ([AL-02](../13-observability-and-operations.md#rule-al-02))
- **Constraint** — the row is written **before** processing ([EI-01](../16-billing-and-commerce-architecture.md#rule-ei-01)). An unverified event is stored with `signature_verified = false` and rejected, never processed.

### `commerce.order`, `commerce.payment`, `commerce.subscription`

`order` links intent → offer → price version → billing account, and is append-only after completion. `payment` records each provider payment with its external reference, amount as `money`, and state. `subscription` carries the **normalised** state driven by `paid_through` ([EN-05](../16-billing-and-commerce-architecture.md#rule-en-05)), not by a provider status string:

| Table | Required fields / constraints |
|---|---|
| commerce.order | order_id:id PK; purchase_intent_id/billing_account_id/workspace_id/offer_id/price_version_id:id FK NN; amount:money NN; state:enum(pending,completed,canceled) NN; created_at:instant NN; completed_at:instant?; rev:rev NN; UQ(purchase_intent_id). A verified captured payment completes the order in the purchase transaction. Completed commercial terms are immutable; refunds/disputes append financial events, never rewrite the original sale. |
| commerce.payment | payment_id:id PK; order_id:id FK NN; provider/provider_payment_ref:text NN; amount:money NN; state:enum(pending,captured,failed,canceled) NN; provider_event_id:id FK NN; created_at:instant NN; captured_at:instant?; rev:rev NN; UQ(provider,provider_payment_ref). Captured is established only by verified provider evidence. Contradictory or older events reconcile instead of regressing it. Refund/dispute movements use linked ledger entries; they do not make the capture unhappen. |

Subscription fields:

| Field | Type | Notes |
|---|---|---|
| `subscription_id` | `id` | **PK** |
| `billing_account_id` | `id NN` | |
| `workspace_id` | `id NN` | |
| `offer_id`, `price_version_id` | `id NN` | |
| `state` | `enum(pending, active, grace, cancelScheduled, ended, suspended) NN` | Derived from `paid_through` and policy |
| `paid_through` | `instant NN` | **The authoritative field** |
| `cancel_at_period_end` | `bool NN` | |
| `external_subscription_ref` | `text?` | |
| `rev` | `rev NN` | |

- `IX (state, paid_through)` — the state-transition sweeper
- **Constraint** — `state` is recomputed from `paid_through` plus the grace policy; it is never set directly from a provider webhook field

### `commerce.credit_lot`, `commerce.credit_transaction`

> **Unified 2026-09-07.** The previous definition carried the pre-P2-006 model: a `subscriptionAllowance` lot class, `money`-typed customer balances, and a `credit_reservation` table keyed on `attempt_id`. All three are superseded. **Included capacity is a bucket, not a lot** ([CD-02](../16-billing-and-commerce-architecture.md#rule-cd-02)); customer amounts are **integer micro-credits**, not money ([CD-01](../16-billing-and-commerce-architecture.md#rule-cd-01), [MT-07](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-07)); and reservation is per **logical request**, not per attempt (`§7.3` of the commerce architecture). `commerce.credit_reservation` is **retired**; `entitlement.capacity_reservation` is the single reservation table for both funding pools.

| `credit_lot` field | Type | Notes |
|---|---|---|
| `credit_lot_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` |
| `lot_class` | `enum(purchased, compensation) NN` | **Two classes.** `subscriptionAllowance` is retired — that pool is `entitlement.capacity_bucket` |
| `original_micro` | `int64 NN` | **Integer micro-credits** ([CD-01](../16-billing-and-commerce-architecture.md#rule-cd-01)). Never `money`, never a float |
| `remaining_micro` | `int64 NN` | |
| `held_micro` | `int64 NN` | Sum of live reservations funded from this lot |
| `expires_at` | `instant?` | **NULL for `purchased`** — purchased credits do not expire with time or cancellation ([CD-03](../16-billing-and-commerce-architecture.md#rule-cd-03)). Required for `compensation` ([CD-04](../16-billing-and-commerce-architecture.md#rule-cd-04)) |
| `refund_hold` | `bool NN` | Freezes the lot during adjudication ([AI-17](../20-cross-system-lifecycles.md#rule-ai-17) of the cross-system lifecycles) |
| `source_ref` | `text?` | Order or compensation-grant reference |
| `created_at` | `instant NN` | |

- `IX (workspace_id, lot_class, refund_hold, expires_at, created_at)` — **the funding-order query**: compensation earliest-expiry-first, then purchased oldest-acquisition-first ([CD-05](../16-billing-and-commerce-architecture.md#rule-cd-05))
- **Constraint** — `remaining_micro >= 0` and `held_micro >= 0` and `held_micro <= remaining_micro`. This is what makes "no overdraft" structural ([CR-23](../../requirements/04-commerce-entitlement-and-credits.md#rule-cr-23))
- **Constraint** — `lot_class = 'purchased'` requires `expires_at IS NULL`; `lot_class = 'compensation'` requires `expires_at IS NOT NULL`
- **Constraint** — a lot is **never** created by a refill; only a purchase, a compensation grant or an adjustment creates one ([RF-07](../16-billing-and-commerce-architecture.md#rule-rf-07) of the commerce architecture)

`credit_transaction` is the append-only movement log: reserve, settle, release, expire, refund, adjust. Every row names its lot, its `reservation_id` where applicable, its **signed micro-credit amount**, its reason, and the `logical_request_id` it settles where one applies. **No row is ever updated or deleted** ([ST-04](../16-billing-and-commerce-architecture.md#rule-st-04)).

| Table | Required fields / constraints |
|---|---|
| commerce.credit_transaction | transaction_id:id PK; workspace_id/credit_lot_id:id FK NN; reservation_id/logical_request_id:id?; kind:enum(reserve,settle,release,expire,refund,adjust) NN; amount_micro:int64 NN; reason:ReasonCode NN; command_id:id NN; movement_ordinal:int NN; created_at:instant NN; UQ(command_id,movement_ordinal); IX(credit_lot_id,created_at). Signed exact microcredits; append-only and atomically paired with the guarded lot/reservation change. |

#### The two funding pools, and the one reservation

| Pool | Table | Unit | Recovers | Reserved by |
|---|---|---|---|---|
| Included capacity | `entitlement.capacity_bucket` | micro-credits | **Yes** (`§7.2`) | `entitlement.capacity_reservation.from_capacity_micro` |
| Purchased and compensation | `commerce.credit_lot` | micro-credits | **No** ([RF-07](../16-billing-and-commerce-architecture.md#rule-rf-07) of the commerce architecture) | `capacity_reservation.from_compensation_micro` / `from_purchased_micro` |

| # | Rule |
|---|---|
| <a id="rule-fu-01"></a>FU-01 | **One reservation row spans both pools.** `entitlement.capacity_reservation` records the split across its three source columns, and settlement moves against exactly those ([ST-05](../16-billing-and-commerce-architecture.md#rule-st-05)). Two reservation tables would make a partial settlement possible, which is the defect this unification removes. |
| <a id="rule-fu-02"></a>FU-02 | **Reservation identity is the logical request**, not the attempt: `UQ (logical_request_id)` where the state is non-terminal. A logical request may make several provider attempts ([MT-02](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-02)); they share the one hold and settle once ([ST-01](../16-billing-and-commerce-architecture.md#rule-st-01)). |
| <a id="rule-fu-03"></a>FU-03 | **Supplier accounting is per attempt; customer accounting is per logical request.** `commerce.supplier_cost_entry` has a base entry plus linked adjustments per `provider_attempt`; `commerce.customer_settlement` has one row per `logical_ai_request`. **They are never joined as if one-to-one** — a platform-caused retry produces two supplier rows and one customer debit ([ST-07](../16-billing-and-commerce-architecture.md#rule-st-07), [MT-08](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-08)). |
| <a id="rule-fu-04"></a>FU-04 | **A lot's `held_micro` is maintained by the same shared unit of work that maintains the bucket's** (`§6.1.1` of the overview), so the two pools cannot disagree about what is held. |
| FU-05 | **A refund holds, then zeroes, the lot's remaining amount** ([AI-17](../20-cross-system-lifecycles.md#rule-ai-17)). It never returns micro-credits to the capacity bucket, and never mints capacity above the burst ([RF-05](../16-billing-and-commerce-architecture.md#rule-rf-05)). |

### `commerce.ledger_entry`

Three separately balanced ledgers share a discriminated table ([LG-01](../16-billing-and-commerce-architecture.md#rule-lg-01), [LG-03](../16-billing-and-commerce-architecture.md#rule-lg-03) of the commerce architecture). Reports may correlate references; money and micro-credit amounts are never netted or summed across units:

> **Units corrected 2026-09-08.** A single `money` amount column spanned all three ledgers, including `customerCredit` — but customer amounts are **integer micro-credits**, not money ([CD-01](../16-billing-and-commerce-architecture.md#rule-cd-01), [MT-07](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-07), [I-493](../../requirements/01-normative-glossary-and-invariants.md#rule-i-493)). Storing a service unit in a money column invites exactly the conflation the three-ledger rule exists to prevent. The amount is now **two mutually exclusive columns**, one per unit system.

| Field | Type | Notes |
|---|---|---|
| `ledger_entry_id` | `id` | **PK** |
| `ledger` | `enum(providerCost, customerCredit, paymentRevenue) NN` | |
| `workspace_id` | `id?` | Null for provider-cost rows that are not workspace-attributable |
| `amount_micro` | `int64?` | **Signed micro-credits.** Set **only** for `customerCredit` |
| `amount_money` | `decimal(28,9)?` | **Signed money.** Set **only** for `providerCost` and `paymentRevenue` |
| `currency` | `char(3)?` | **Required** whenever `amount_money` is set; **NULL** for `customerCredit`, which is currency-independent ([ST-08](../16-billing-and-commerce-architecture.md#rule-st-08), [MT-16](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-16)) |
| `occurred_at` | `instant NN` | |
| `reference_kind`, `reference_id` | `text NN`, `id NN` | What the entry is about |
| `created_at` | `instant NN` | |

- **Append-only.** A correction is a new entry ([BC-05](../16-billing-and-commerce-architecture.md#rule-bc-05))
- `IX (ledger, occurred_at)`; `IX (ledger, workspace_id, occurred_at)`
- **Constraint** — `ledger = 'customerCredit'` requires `amount_micro IS NOT NULL AND amount_money IS NULL AND currency IS NULL`
- **Constraint** — `ledger IN ('providerCost','paymentRevenue')` requires `amount_money IS NOT NULL AND currency IS NOT NULL AND amount_micro IS NULL`
- **Constraint** — write/accounting paths never net distinct ledgers or sum micro-credits with money. Read-only reconciliation/margin reports may join their stable references and compare money only within one currency, with the source bases stated.
- **Rule** — margin is a **report** computed by relating rows across ledgers through their references, never a stored figure and never a subtraction of one column from another ([LG-04](../16-billing-and-commerce-architecture.md#rule-lg-04))

---

## 8. `chat`, `task`, `agent`

**Cloud commits every row in this Cloud schema.** Cloud-history Chat and all execution metadata remain Cloud-authoritative. Local assistant bodies are independently canonical under [model 05](05-application-history.md); they do not become Chat rows merely because Cloud executes an AI request.

### `chat.conversation`, `chat.message`

For Cloud-history mode, the client projection in [`02-desktop-data-model.md`](02-desktop-data-model.md) mirrors these rows. Local-history stores instead follow model 05. **Cloud holds the authoritative acknowledged revision and is its committer** ([AU-01](00-data-model-overview.md#rule-au-01), [CW-02](00-data-model-overview.md#rule-cw-02)); the client copy is a working cache plus unsent drafts.

| Table | Complete fields and constraints |
|---|---|
| chat.conversation | conversation_id:id PK; workspace_id:id NN; product_id:ProductId NN; title:text NN; active_branch_id:id NN; project_id:id?; mode=cloud; created_at/updated_at:instant NN; deleted_at:instant?; rev:rev NN; UQ(workspace_id,product_id,conversation_id); list IX(workspace_id,product_id,deleted_at,updated_at,conversation_id). |
| chat.branch | branch_id:id PK; conversation_id:id FK NN; parent_branch_id:id? self-FK; fork_message_id:id?; created_at:instant NN; parent/fork must belong to this conversation and form an acyclic graph. |
| chat.message | message_id:id PK; conversation_id:id FK NN; branch_id:id FK NN; ordinal:bigint NN; role:TranscriptRole NN; state:text NN; parts_proto:blob?; body_resource_id:id?; body_hash:hash NN; task_id/turn_id:id? (at most one); created_at:instant NN; conversation_rev_at_commit:rev NN; UQ(branch_id,ordinal); exactly one inline parts or verified body resource (16 KiB threshold). Committed content immutable. conversation_rev_at_commit is the immutable MessageView.revision/VersionedRef snapshot, never a child CAS counter. Conversation commands guard the current root revision. |
| chat.project | project_id:id PK; workspace_id:id NN; product_id:ProductId NN; body_proto:ChatProjectRecord NN; rev:rev NN; deleted_at:instant?; IX(workspace_id,product_id,deleted_at). |
| agent.agent_profile / agent.skill | profile_id / skill_id:id PK; workspace_id:id NN; product_id:ProductId NN; revision:rev NN; body_proto:AgentProfile / SkillRecord NN; deleted_at:instant?; version rows PK(id,revision) are immutable; declarations never grant capability. |
| chat.compaction_record | compaction_id:id PK; conversation_id:id FK NN; branch_id:id FK NN; through_ordinal:bigint NN; source_hash:hash NN; summary_resource_id:id NN; summary_hash:hash NN; model_id/config_version:text NN; created_at:instant NN; UQ(branch_id,through_ordinal,source_hash,config_version). Rebuildable, no user-authority state; publication guards current source hash/branch revision. |

| # | Rule |
|---|---|
| CH-D1 | **Cloud writes these tables directly.** `chat.appendMessage` commits the user message; the Harness commits the assistant message. A Cloud-originated message requires no device and no client change ([CW-03](00-data-model-overview.md#rule-cw-03)). |
| CH-D2 | **`rev` is assigned by Cloud.** A client's `local_rev` is a device-scoped counter for unsent work and never appears here ([CW-01](00-data-model-overview.md#rule-cw-01)). |
| CH-D3 | **Every commit writes its `sync.change` row in the same transaction** ([CW-06](00-data-model-overview.md#rule-cw-06)), so a message can never exist without being publishable. |
| CH-D4 | **An unsent draft is not a row here.** It lives only on the device that composed it ([I-124](../../requirements/01-normative-glossary-and-invariants.md#rule-i-124)), and is therefore never a competing revision. |
| CH-D5 | A committed Chat message is immutable; edit creates a branch. Stream chunks are presentation, each invocation has immutable `task.iteration_output`, and the terminal Turn publishes a separate final/interrupted message or explicit no-answer outcome. |
| CH-D6 | Stream chunks/state live in the CF RunStream DO with bounded TTL, excluded from D1 change archives and business backups. C# stores Cloud-history canonical iteration/final content and pointers; local/temporary bodies use model 05 transient storage. Restore discards projections and reconciles durable attempts under [CF integration](../contracts/05-cloudflare-integration.md). |

### Chat-owned ordinary and temporary execution

| Table | Complete fields and constraints |
|---|---|
| chat.turn | turn_id:id PK; workspace_id:id NN; product_id:ProductId NN; history_mode:HistoryMode NN; origin_installation_id:id?; conversation_id/input_message_id/final_message_id:id?; mode:ChatMode NN; state:ChatTurnState NN; rev:rev NN; run_id/stream_id:id?; reason:ReasonCode?; created_at:instant NN; expires_at:instant?; has_unknown_effect:bool NN; transient_input_ref:id?; transient_output_receipt_id:id?; UQ(workspace_id,input_message_id); IX(workspace_id,product_id,state,created_at). |
| chat.turn_promotion | turn_id:id PK/FK; task_id:id FK UNIQUE NN; preview_hash:hash NN; command_id:id UNIQUE NN; created_at:instant NN. Promotion creates a separate linked Task once, never changes a turn into an agent in place. |
| chat.execution_lease | Same typed fields, PK and fence constraints as task.execution_lease; run_id references chat.run. |
| chat.execution_command | Same typed fields, PK/UQ and replay rules as task.execution_command; run_id references chat.run. |
| chat.run | Same typed fields and UQ as task.run with turn_id instead of task_id; owner must exist in Chat. |
| chat.iteration_output | Same fields, constraints and receipt rules as task.iteration_output; run_id references chat.run. |
| chat.transient_content | resource_id:id PK; workspace_id:id NN; product_id:ProductId NN; origin_installation_id:id NN; turn_id/task_id:id? (exactly one execution owner); purpose:enum(transientInput,transientOutput) NN; key_ref/ciphertext_ref:text NN; sha256:hash NN; size:bigint NN CHECK ≥0; expires_at:instant NN; closed_at/purged_at:instant?; IX(expires_at,purged_at). References encrypted bytes, not plaintext; metadata is not canonical history. |
| task.control_receipt / chat.control_receipt | command_id:id PK; owner_id:id FK NN to respective Task/Turn; kind:Key NN; state:ControlState NN; requested_at:instant NN; acknowledged_at:instant?; reason:ReasonCode?; request_hash:hash NN; IX(owner_id,requested_at). Retains prior receipts rather than overwriting one latest state. |

Cloud-history turns require conversation/input-message FKs and a committed final message or explicit no-answer outcome before success. Local/temporary turns have null Cloud conversation/message FKs, require origin_installation_id and bind verified transient input/output receipts from model 05. Temporary requires mode=temporary; other turns require mode=ordinary. Scope is immutable at admission. Shared provider/execution records use a validated ExecutionOwner, never a phantom Task or an unchecked polymorphic ID. Chat and Task own their respective table writes inside the registered shared batch.

Transient content is encrypted, excluded from ordinary history, Sync, Knowledge and backups, and expires within 24 hours; close denies access immediately and purges within 1 hour. CF checkpoints carry IDs only. Account revocation/deletion denies access regardless of purge lag. Temporary compaction summaries never enter this table. Stable owner/accounting receipts retain hashes/counts/reasons, not body text.

### `task.iteration_output` and terminal references

| Table | Complete fields and constraints |
|---|---|
| task.iteration_output | output_id:id PK; run_id:id FK NN; iteration_ordinal:int NN; logical_request_id:id NN; provider_attempt_id:id NN; state:enum(complete,interrupted,refused,toolProposals) NN; parts_proto:blob?; body_resource_id:id?; checksum:hash NN; created_at:instant NN; UQ(run_id,iteration_ordinal); exactly one parts_proto or verified body_resource_id. |

 Each content part carries the [content origin record](../../requirements/13-data-formats-and-portability.md#content-origin-carriers), bound and committed with its payload before completed output publication; staged marking failure creates no delivered receipt. It is written with the provider outcome/usage receipt before customer settlement. Tool proposal/result parts link durable invocation IDs, and can be read through the authorised Task view without pretending the Turn is terminal. Resource promotion includes Entitlement quota conversion where required.

Cloud-history terminal states require exactly one final/interrupted message reference or explicit no-answer reason in the same Chat/Task/Resource/Sync atomic batch. Local/temporary mode instead requires a verified transient-output commit receipt or explicit no-answer reason under model 05; it never creates a dummy Cloud message. A provider callback cannot set Task succeeded merely because its own invocation finished. Updating intermediate Task state uses a typed read projection; synchronised aggregate changes still require publication.

### `task.task`

| Field | Type | Notes |
|---|---|---|
| `task_id` | `id` | **PK** |
| `workspace_id` | `id NN` | |
| `origin_surface` | `enum(desktop, web, mobile, automation) NN` | Where the request came from. Provenance only — it confers no authority ([TO-03](00-data-model-overview.md#rule-to-03)) |
| `origin_device_id` | `id?` | Present when a device originated it; **null for browser/automation without a native installation; Android may carry its originating device** |
| `state` | `enum(queued, running, waiting, paused, interrupted, succeeded, partiallySucceeded, failed, canceled) NN` | |
| `reason_facet` | `TaskReasonFacet NN` | none/approval/device/capacity/dependency/reconciliation; non-none exactly while waiting. |
| `intent_summary` | `text NN` | User-facing |
| `created_at`, `updated_at` | `instant NN` | |
| `rev` | `rev NN` | |
| `product_id` | `ProductId NN` | Frozen application scope: arcnotes/arcscope/arcslate/companion |
| `origin_installation_id` | `id?` | Required for local-history origin; no body visibility to other devices |
| `transient_input_ref`, `transient_output_receipt_id` | `id?` | Verified input/output for local history only; null for Cloud history |
| `current_iteration` | `int NN` | Nonnegative iteration ordinal |
| `current_provider_attempt_id`, `final_message_id`, `terminal_output_commit_id` | `id?` | Exact receipt/pointer, never derived from a presentation buffer |
| `no_answer_reason` | `ReasonCode?` | Explicit terminal no-answer disposition |
| `has_unknown_effect` | `bool NN` | Separate from TaskState |
| `history_mode` | `enum(local,cloud) NN` | Temporary cannot be an agent; local metadata carries no conversation body |

- `IX (workspace_id, state, updated_at)` — the task centre

> **Corrected 2026-09-08.** The table carried `placement ∈ {local, cloud, remoteViaBridge}`, `authoritative_store ∈ {cloud, device}` and a check constraint forcing local placement to device authority. All three contradict [TO-01](00-data-model-overview.md#rule-to-01): **every Agent Task is Cloud-owned**, and no Agent Task has a device authoritative store. They are removed rather than defaulted, because a column whose only legal value is `cloud` invites code to branch on it.

| # | Rule |
|---|---|
| <a id="rule-tk-01"></a>TK-01 | **There is no `placement` column and no `authoritative_store` column.** The authoritative store is always Cloud ([TO-01](00-data-model-overview.md#rule-to-01)). What varies is **each Step's tool locality**, which lives on `task.plan_step` ([TK-02](#rule-tk-02)), because one Task routinely mixes both. |
| <a id="rule-tk-02"></a>TK-02 | **`plan_step.tool_locality ∈ {cloud, device}`**, with `target_device_id` on the Step — not on the Task — since different Steps of one Task may target different devices, or none. |
| TK-03 | **A native Product Job is not in this table at all** ([TO-05](00-data-model-overview.md#rule-to-05), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). It lives in its product's own store with its own job identity; the task centre reads both through a union projection and labels each with its owner ([WP-17.03](../../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.03)). |
| <a id="rule-tk-04"></a>TK-04 | **`origin_surface` and `origin_device_id` are provenance, never authority.** A Task created from Web has no device and is fully executable; a device is required only for a Step whose locality is `device` ([CW-03](00-data-model-overview.md#rule-cw-03)). |
| TK-05 | **Cancellation and recovery are Cloud-side for the Task and product-side for a Product Job.** Cancelling a Task cancels its Steps; a Step that started a Product Job requests that product's cancellation and records the outcome — it does not reach into the product's store. |

### `task.run`, `task.plan_step`, `task.attempt`

| Table | Complete fields and constraints |
|---|---|
| task.run | run_id:id PK; task_id:id FK NN; ordinal:int NN; state:TaskState NN; workflow_id/worker_version:text NN; recovery_generation:bigint NN; last_iteration_receipt:hash?; created_at/updated_at:instant NN; rev:rev NN; UQ(task_id,ordinal); IX(state,updated_at). |
| task.execution_lease | run_id:id PK/FK; holder/workflow_id/worker_version:text NN; epoch:bigint NN; expires_at:instant NN; recovery_generation:bigint NN; IX(expires_at). |
| task.execution_command | command_id:id PK; run_id:id FK NN; epoch:bigint NN; operation/request_sha256/state:text NN; result_ref:typed JSON TEXT?; created_at:instant NN; UQ(run_id,operation,command_id). |

No external call occurs inside a registered guarded commit. A device step requires a full frozen target; retargeting requires a new approved command, never automatic fallback to another application.

**Tool locality lives on the Step** ([TK-02](#rule-tk-02)), because one Task mixes cloud and device Steps.

| `plan_step` field | Type | Notes |
|---|---|---|
| `plan_step_id` | `id` | **PK** |
| `run_id` | `id NN` | `FK →`; cascade |
| `step_ordinal` | `int NN` | |
| `capability_key` | `text NN` | Resolved through the generated allowlist ([DP-04](../contracts/02-local-rpc-operations.md#rule-dp-04)) |
| `tool_locality` | `enum(cloud, device) NN` | **Declared, never inferred** ([PL-02](../17-agent-harness.md#rule-pl-02) of the harness) |
| `target_device_id` | `id?` | Required when `tool_locality = 'device'`, else null |
| `target_product_id` | `ProductId?` | Required for device locality, matches Task product |
| `target_installation_id` | `id?` | Required for device locality |
| `target_instance_epoch` | `bigint?` | Required after device delivery/claim; current bound instance |
| `arguments_proto` | `CapabilityArguments NN` | Validated typed capability arguments |
| `approval_required` | `bool NN` | Frozen approval requirement, never authority by itself |
| `compensation_proto` | `typed record?` | Declared compensation capability/arguments or absent |
| `state`, `reason_facet` | `text NN`, `text?` | |

- `IX (target_device_id, target_installation_id, state)` — **the tool-request pull path**, now correctly on the Step
- **Constraint** — `tool_locality = 'device'` requires target_device_id, target_product_id and target_installation_id; epoch is filled and fenced at delivery. `cloud` requires all target fields to be null
- **Constraint** — a Step declared `device` is **never** satisfied by a cloud substitute ([PL-02](../17-agent-harness.md#rule-pl-02)); if no eligible device is online the Step waits with a stated reason


`run` groups attempts at one task. `plan_step` holds the ordered plan with each step's capability, arguments reference, compensation declaration and approval requirement. `attempt` is the unit of retry:

| `attempt` field | Type | Notes |
|---|---|---|
| `attempt_id` | `id` | **PK** |
| `run_id`, `step_id` | `id NN` | |
| `command_id` | `id NN` | **Reused across retries of the same command** ([BR-02](../../planning/work-packages/16-unified-execution-engine.md#rule-br-02) of [WP-16](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16)) |
| `state` | `enum(pending, running, succeeded, failed, canceled) NN` | |
| `attempt_ordinal` | `int NN` | Monotonic under the command/run guard |
| `failure_class` | `enum(transient, permanent, refused, canceled, unknownEffect)?` | |
| `effect_certainty` | `enum(didNotHappen, happened, unknown)?` | |
| `started_at`, `ended_at` | `instant?` | |

- `UQ (command_id, attempt_ordinal)`
- **Constraint** — an attempt with `effect_certainty = unknown` on a non-idempotent step **must not** auto-retry ([WP-16.02](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.02)); the state machine refuses the transition

### `task.approval`

| Table | Required fields / constraints |
|---|---|
| task.approval | approval_id:id PK; task_id/run_id/step_id:id FK NN; proposal_hash:hash NN; actor_proto:ActorChain NN; frozen_context_proto:FrozenContext NN; risk:Key NN; local_presence_required:bool NN; description:text NN; state:enum(pending,approved,rejected,expired,withdrawn) NN; decision_by:id?; created_at/expires_at:instant NN; decided_at/consumed_at:instant?; rev:rev NN; IX(task_id,state,expires_at). Decision/consumption guards exact proposal, actor, scope, revision and expiry. |



Durable pending state with `expires_at`, the operation described in user terms, the risk level, and whether local presence is required. **Survives restart of either side** ([WP-14.04](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04)).

### `task.automation_definition` and `automation_occurrence`

| Table | Required fields / constraints |
|---|---|
| task.automation_definition | automation_id:id PK; workspace_id:id FK NN; product_id:ProductId NN; definition_version:bigint NN; definition_proto:AutomationSpec NN; enabled:bool NN; next_due_at:instant?; event_cursor:text?; created_at/updated_at:instant NN; rev:rev NN; IX(enabled,next_due_at). Definition freezes trigger, timezone, grants, target, misfire/coalescing and budgets. |
| task.automation_occurrence | occurrence_id:id PK; automation_id:id FK NN; definition_version:bigint NN; occurrence_key:text NN; scheduled_at:instant NN; event_id:id?; state:enum(pending,admitted,skipped,completed,failed,canceled) NN; task_id:id?; reason:ReasonCode?; completed_at:instant?; UQ(automation_id,definition_version,occurrence_key); IX(state,scheduled_at). |



`automation_definition` stores stable ID, workspace, immutable definition version, enabled state/revision, trigger kind, UTC schedule with timezone policy or durable event cursor, authorised grant/budget snapshot, misfire/coalescing bounds and next due instant. `automation_occurrence` has unique `(automation_id, definition_version, occurrence_key)`, scheduled time/event identity, admission outcome, Task ID and completion reason. The enumerated automation shared transaction records occurrence, Task, context pins and dispatch outbox together; a leased runner resumes from that receipt after crash. Definition changes invalidate future old-version occurrences, without rewriting past runs. Disable/revoke has an explicit in-flight cancellation policy; neither resets usage nor grants permission.

### `task.tool_request`, `task.tool_result`

The durable bridge (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). A request carries its target device, its payload, its expiry and its delivery state; a result carries the answering attempt and is **idempotent on `(tool_request_id, attempt_id, command_id)`** so a re-submitted result has one effect.

| Table | Complete fields / constraints |
|---|---|
| task.tool_request | tool_request_id:id PK; workspace_id:id NN; product_id:ProductId NN; task_id:id FK NN; run_id/step_id/attempt_id/command_id:id NN; target_device_id/target_installation_id:id?; target_product_id:ProductId?; target_instance_epoch:bigint?; capability:text NN; arguments_proto/context_proto/actor_proto:blob NN; approval_id:id?; expires_at:instant NN; state:queued/delivered/answered/expired/refused; rev:rev NN. Device requests require the full target, cloud requests omit it. IX(workspace_id,target_installation_id,state,expires_at); immutable command payload/hash. |
| task.tool_result | tool_request_id:id FK + attempt_id:id + command_id:id composite PK; result_hash:hash NN; body_proto:ToolResult NN; effect_certainty:EffectCertainty NN; received_at:instant NN. Repeated key and same hash returns the receipt; different hash refuses; no deduplication on Task alone. |
| chat.tool_request / chat.tool_result | Same fields/constraints with turn_id instead of task_id; ChatTurn permits only its admitted pure-read tool set, no fabricated Task FK. |

### `agent.model_descriptor`, `agent.tariff_version`, `agent.supplier_price_version`

`model_descriptor` and the two price tables are workspace-independent catalogue rows **projected from an activated configuration revision** ([CG-02](../16-billing-and-commerce-architecture.md#rule-cg-02), [DC-05](../../requirements/11-policy-and-configuration.md#rule-dc-05), [DC-06](../../requirements/11-policy-and-configuration.md#rule-dc-06)). They are persisted snapshots, not live lookups into the current file ([I-494](../../requirements/01-normative-glossary-and-invariants.md#rule-i-494)).

| Table | Required fields / constraints |
|---|---|
| agent.model_descriptor | model_descriptor_id:id PK; model_id:ModelId NN; config_revision_id:id FK NN; provider:enum(workersAi) NN; route/purpose/lifecycle_state:Key NN; descriptor_json:canonical closed models profile from contracts 08 NN; descriptor_hash:hash NN; created_at:instant NN; UQ(config_revision_id,model_id,purpose). Route, tokenizer, category/tier semantics and context/output limits are immutable for this descriptor identity. |
| agent.supplier_price_version | supplier_price_version_id:id PK; model_descriptor_id/config_revision_id:id FK NN; currency:text NN; valid_from:instant NN; valid_to:instant?; rates_json:canonical closed supplierPrices profile from contracts 08 NN; rates_hash:hash NN; created_at:instant NN; IX(model_descriptor_id,valid_from). Exact Decimal rates/divisors, no missing-category zero; append-only snapshot. |
| agent.tariff_version | tariff_version_id:id PK; model_descriptor_id/config_revision_id:id FK NN; valid_from:instant NN; valid_to:instant?; rates_json:canonical closed customerTariffs profile from contracts 08 NN; rates_hash:hash NN; created_at:instant NN; IX(model_descriptor_id,valid_from). Exact service-unit rates and declared dimensions; pinned per run/request; append-only snapshot. |

| Table | Holds | Applies at |
|---|---|---|
| `agent.model_descriptor` | Provider route, concrete model and version, billed categories, per-unit divisor, inclusion semantics, tier selection rules, output and context ceilings, lifecycle state | Resolution time |
| `agent.supplier_price_version` | **What ArcForges pays**: per-category rate, currency, unit divisor, validity | **Dispatch time** ([MT-06](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-06)) |
| `agent.tariff_version` | **What the customer is charged**: per-category service units, tier, validity | **Pinned to the Run or request** ([MT-06](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-06), [CR-09](../../requirements/04-commerce-entitlement-and-credits.md#rule-cr-09)) |

- Both price tables are **append-only with effective dates**; a new price is a new row, never an update
- **Constraint** — a `model_descriptor` with any billable category lacking a rate in the applicable `supplier_price_version` **cannot be dispatched** ([AD-04](../16-billing-and-commerce-architecture.md#rule-ad-04), [DC-05](../../requirements/11-policy-and-configuration.md#rule-dc-05), [MT-15](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-15)). There is no assumed zero rate
- **Constraint** — `config_revision_id` on every row records which activated revision produced it, so a historical charge is reproducible after the model is retired ([RP-02](../16-billing-and-commerce-architecture.md#rule-rp-02), [MT-14](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-14))

---

## 8.1 `commerce` — the metering chain *(new — [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006))*

The linked request, attempt, usage, reservation and settlement tables carry [MT-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-01)–[MT-16](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-16). They form one identity chain from request to ledger ([RP-01](../16-billing-and-commerce-architecture.md#rule-rp-01)).

```
logical_ai_request ──1:N──> provider_attempt ──1:N──> attempt_usage
        │                          │                       │
        │                          └──1:N──> supplier_cost_entry
        └──0:1──> capacity_reservation ──1:1──> customer_settlement ──> ledger_entry
```

### `commerce.spend_budget` and `spend_reservation`

| Table | Required fields / constraints |
|---|---|
| commerce.spend_budget | scope_kind:text + scope_id:text + period_key:text + unit:text composite PK; limit/used/held:decimal(28,9) NN; rev:rev NN; period_ends_at:instant?; CHECK limit,used,held≥0. unit is currency for supplier scopes or microcredit for customer Run; the latter is integer-valued. No mixed-unit arithmetic. |
| commerce.spend_reservation | reservation_id:id PK; provider_attempt_id:id?; logical_request_id:id?; scope_kind/scope_id/period_key/unit:text NN (composite FK to spend_budget); bound/used:decimal(28,9) NN; state:enum(held,settled,released,uncertain) NN; lease_expires_at/reconcile_at:instant?; reconciliation_ref:id?; rev:rev NN; UQ(provider_attempt_id,scope_kind,scope_id,period_key,unit); UQ(logical_request_id,scope_kind,scope_id,period_key,unit); exactly one request identity. Supplier uncertainty cannot expire as a customer hold. |



`spend_budget` has PK `(scope_kind, scope_id, period_key, unit)`, a pinned limit, used, held and revision. Supplier scopes include provider account/route, deployment total and configured workspace sublimit; `unit` is the exact ISO currency. Customer Run scope uses integer micro-credits and its explicit authorised maximum. Supplier decimal quantities use `decimal(28,9)`; no FX or comparison between money and credits is implicit.

`spend_reservation` has a unique `(provider_attempt_id, supplier_budget_key)` for supplier exposure, or `(logical_request_id, run_budget_key)` for the customer ceiling; bound, used, state, lease/deadline and linked reconciliation record. Admission guards every applicable budget revision in one registered D1 batch, verifies all `used + held + bound <= limit` predicates and reserves all or none in the Entitlement/Commerce unit of work. A platform call has supplier reservations and an operator job authority, without a customer capacity reservation. A retry has fresh supplier exposure and shares the logical request's one customer ceiling.

Supplier exposure cannot expire merely because a customer hold expires. Confirmed usage replaces its conservative exposure; uncertainty remains reserved (or explicitly consumed as a conservative operator exposure adjustment) until provider reconciliation or an audited operator-funded resolution. Period closure carries unresolved exposure into the provider account's non-resetting outstanding-liability limit, so midnight/restart never unlocks another unbounded call. Customer Run ceilings similarly retain consumed/uncertain authorised exposure until resolved, even when spendable capacity is released. If no finite supported request bound exists, the route is unavailable for paid use.

### `commerce.logical_ai_request`

| Field | Type | Notes |
|---|---|---|
| `logical_request_id` | `id` | **PK** |
| `workspace_id` | `id?` | Required for user/data-scoped work; absent only for deployment health with no customer data |
| `service_term_id` | `id?` | Required for user-delivered official inference and workspace indexing/reranking eligibility; may be absent only for separately authorized deployment platform work without customer service dependency |
| `operator_job_ref` | `id?` | Required and authorised for platform beneficiaries; never a substitute for user inference eligibility |
| `run_id`, `step_id`, `attempt_id` | `id?` | Required for every Cloud user chat/agent invocation; absent only for separately authorised platform jobs |
| `beneficiary` | `enum(userDelivered, platformRouting, platformAbuse, platformHealth, platformIndexing, platformRetry) NN` | Decides who pays ([ST-07](../16-billing-and-commerce-architecture.md#rule-st-07), [MT-08](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-08)) |
| `tariff_version_id` | `id?` | Required and pinned for customer-benefiting work; absent for pure platform jobs |
| `config_revision_id` | `id NN` | [CG-02](../16-billing-and-commerce-architecture.md#rule-cg-02) |
| `state` | `enum(admitted, dispatched, settled, usagePending, costUnconfirmed, resolvedByPolicy, cancelled, rejected) NN` | `§7.6` of the commerce architecture |
| `created_at`, `settled_at` | `instant NN`, `instant?` | |

- `UQ (logical_request_id)`; `IX (workspace_id, created_at)`; `IX (state, created_at)` — the reconciliation-deadline sweep
- **Constraint** — pure platform jobs never debit a customer and have no customer settlement/reservation. A corrective provider retry belongs to the existing user logical request, marks its attempt as platform-funded, and does not create a second customer charge. One logical request is one bounded invocation; a Turn may contain many.

### `commerce.provider_attempt`

| Field | Type | Notes |
|---|---|---|
| `provider_attempt_id` | `id` | **PK** |
| `logical_request_id` | `id NN` | `FK →`; **one logical request may have many attempts** ([MT-02](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-02), [PR-07](../09-ai-and-agent-runtime-architecture.md#rule-pr-07)) |
| `attempt_ordinal` | `int NN` | |
| `provider_request_ref` | `text?` | NULL before the provider supplies an identity, and possibly still NULL after a lost response; never fabricated |
| `client_dispatch_key` | `id NN` | Stable internal idempotency/correlation key committed before network I/O |
| `dispatch_state` | `enum(intentCommitted, outcomeRecorded, unknown, reconciled) NN` | An intent with no outcome is conservatively unknown after owner loss |
| `intent_committed_at`, `owner_fence` | `instant NN`, `int64 NN` | Durable dispatch barrier and fencing generation |
| `funding_class` | `enum(userAttempt, platformRetry, platformJob) NN` | Retry supplier exposure does not imply a new customer debit |
| `model_descriptor_id` | `id NN` | Concrete model and version actually used |
| `supplier_price_version_id` | `id NN` | **Dispatch-time** version ([MT-06](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-06)) |
| `route`, `processing_tier`, `context_tier`, `region_tier` | `text NN` | Resolved from actual request facts ([MT-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-04), [UN-06](../16-billing-and-commerce-architecture.md#rule-un-06)) |
| `dispatched_at`, `completed_at` | `instant?`, `instant?` | Observations only; NULL dispatch time does not prove the call did not happen |
| `usage_source` | `enum(providerFinal, providerStream, invoice, unresolved) NN` | ([MT-05](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-05)) |
| `completeness` | `enum(complete, pending, unconfirmed, mismatched) NN` | ([MT-12](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-12)) |
| `outcome` | `enum(delivered, providerError, platformError, canceled, timeout)?` | NULL at intent and while unknown |
| `output_commit_ref` | `id?` | Durable Task iteration / Chat output receipt, or Search inference outcome receipt for platformIndexing; required before customer settlement of delivered user use. A Search receipt never creates customer settlement |

- `UQ (logical_request_id, attempt_ordinal)`; `UQ (client_dispatch_key)`; provider identity uniqueness is conditional on non-NULL and scoped to the provider account
- **Constraint** — **no prompt or response content** is stored here ([MT-02](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-02)); content lives in the product store, counts live here
- **Rule** — a genuinely distinct retry is a **distinct row with its own supplier cost** ([ST-03](../16-billing-and-commerce-architecture.md#rule-st-03), [MT-11](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-11))

### `commerce.attempt_usage`

The normalised, non-overlapping category quantities ([MT-03](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-03), `§7.4` there).

| Field | Type | Notes |
|---|---|---|
| `attempt_usage_id` | `id` | **PK** |
| `provider_attempt_id` | `id NN` | `FK →` |
| `usage_revision` | `int NN` | **Increments on each cumulative stream snapshot** ([UN-03](../16-billing-and-commerce-architecture.md#rule-un-03), [I-492](../../requirements/01-normative-glossary-and-invariants.md#rule-i-492)) |
| `category` | `text NN` | `input.uncached` · `input.cached_read` · `input.cache_write` · `output` · `output.reasoning` · `tool.<kind>` |
| `quantity` | `int64 NN` | Non-negative ([UN-05](../16-billing-and-commerce-architecture.md#rule-un-05)) |
| `unit` | `text NN` | `token` · `request` · `second` · `image` ([MT-10](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-10)) |
| `recorded_at` | `instant NN` | |

- `UQ (provider_attempt_id, usage_revision, category)` — **this is the idempotency key** ([ST-03](../16-billing-and-commerce-architecture.md#rule-st-03), [MT-11](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-11))
- **Rule** — a later `usage_revision` **replaces** the earlier total for that attempt; revisions are never summed ([UN-03](../16-billing-and-commerce-architecture.md#rule-un-03))
- **Constraint** — a category not declared by the attempt's model descriptor is **rejected into reconciliation**, never debited ([UN-02](../16-billing-and-commerce-architecture.md#rule-un-02), [MT-05](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-05))

### `commerce.supplier_cost_entry`

| Field | Type | Notes |
|---|---|---|
| `supplier_cost_id` | `id` | **PK** |
| `provider_attempt_id` | `id NN` | `FK →` |
| `currency` | `char(3) NN` | **Always present** ([ST-08](../16-billing-and-commerce-architecture.md#rule-st-08), [MT-16](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-16)) |
| `amount` | `decimal(28,9) NN` | ≥ 9 fractional digits ([MT-07](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-07)). **Never a float** |
| `basis` | `enum(estimated, usageConfirmed, invoiceReconciled) NN` | The three remain distinguishable ([UC-03](../16-billing-and-commerce-architecture.md#rule-uc-03), [MT-13](../../requirements/04-commerce-entitlement-and-credits.md#rule-mt-13)) |
| `unresolved` | `bool NN` | This entry’s recorded basis; current reconciliation state derives from its linked adjustment chain |
| `adjusts_cost_id` | `id?` | Prior cost entry corrected by this immutable adjustment; unique source reconciliation event prevents replay |

- `IX (basis, unresolved)` — the reconciliation queue
- **Constraint** — a row is **never deleted or updated**; a correction is a new linked adjustment row ([ST-04](../16-billing-and-commerce-architecture.md#rule-st-04))

### `commerce.customer_settlement`

| Field | Type | Notes |
|---|---|---|
| `settlement_id` | `id` | **PK** |
| `logical_request_id` | `id NN` | `FK →` |
| `reservation_id` | `id NN` | `FK →` `entitlement.capacity_reservation` |
| `debit_capacity_micro`, `debit_compensation_micro`, `debit_purchased_micro` | `int64 NN` | Debited **against the sources the reservation held** ([ST-05](../16-billing-and-commerce-architecture.md#rule-st-05)) |
| `released_micro` | `int64 NN` | Unused original funding returned to those same sources in full; total funding is conserved ([RF-06](../16-billing-and-commerce-architecture.md#rule-rf-06) of the commerce architecture) |
| `rounding_mode` | `text NN` | Declared half-even ([ST-01](../16-billing-and-commerce-architecture.md#rule-st-01)) |
| `settled_at` | `instant NN` | |
| `adjusts_settlement_id` | `id?` | Present on a correction; the original is never edited ([ST-04](../16-billing-and-commerce-architecture.md#rule-st-04)) |

- `UQ (logical_request_id)` **where `adjusts_settlement_id IS NULL`** — one settlement per logical request ([ST-01](../16-billing-and-commerce-architecture.md#rule-st-01))
- **Constraint** — settlement occurs **once, after category aggregation**, never per stream fragment ([ST-01](../16-billing-and-commerce-architecture.md#rule-st-01))

---

## 8.2 `config` — activated policy revisions *(new — [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006))*

[DC-04](../../requirements/11-policy-and-configuration.md#rule-dc-04), [DC-09](../../requirements/11-policy-and-configuration.md#rule-dc-09), [DC-12](../../requirements/11-policy-and-configuration.md#rule-dc-12) make the activated bundle a persisted fact, not a file read at request time.

### `config.revision`

| Field | Type | Notes |
|---|---|---|
| `config_revision_id` | `id` | **PK** |
| `schema_version` | `text NN` | |
| `revision_identity` | `text NN` | Operator-supplied; **immutable** |
| `content_hash` | `bytes NN` | |
| `environment`, `realm_id` | `text NN`, `id NN` | Rejected on mismatch ([DC-04](../../requirements/11-policy-and-configuration.md#rule-dc-04)) |
| `effective_at` | `instant NN` | |
| `activated_at` | `instant?` | Null until activation succeeds |
| `state` | `enum(validated, active, superseded, rejected) NN` | |
| `document` | `json NN` | The validated bundle as activated |

- `UQ (revision_identity)` — **a revision identity cannot be reused with different content** ([DC-04](../../requirements/11-policy-and-configuration.md#rule-dc-04)), enforced together with `content_hash`
- `UQ (realm_id, state)` **where `state = 'active'`** — exactly one active revision per realm ([CG-03](../16-billing-and-commerce-architecture.md#rule-cg-03))
- **Rule** — a replica that cannot load the active revision **admits no affected work**; it does not fall back to a previous revision or a sample ([CG-03](../16-billing-and-commerce-architecture.md#rule-cg-03), [DC-11](../../requirements/11-policy-and-configuration.md#rule-dc-11))
- **Rule** — rollback publishes a **new** revision restoring prior values ([DC-12](../../requirements/11-policy-and-configuration.md#rule-dc-12)); it never reactivates a superseded row

---

## 8.3 `scope` — the deterministic Cloud simulator *(new — [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006))*

[SIM-01](../../requirements/products/arcscope.md#rule-sim-01)–[SIM-20](../../requirements/products/arcscope.md#rule-sim-20) of the ArcScope requirements. Cloud owns the definition and the run; ArcScope owns the native session projection and the downloaded capture ([SIM-01](../../requirements/products/arcscope.md#rule-sim-01)).

**A `SimulationRun` is a product job, not an Agent Run, and invokes no model** ([SIM-01](../../requirements/products/arcscope.md#rule-sim-01), [CM-04](../09-ai-and-agent-runtime-architecture.md#rule-cm-04) of the runtime architecture). It consumes product-resource quota — duration, samples, bytes, egress — never model tokens ([SIM-17](../../requirements/products/arcscope.md#rule-sim-17)).

### `scope.simulation_definition`, `scope.scenario_version`

| Field | Type | Notes |
|---|---|---|
| `definition_id` / `scenario_version_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →`; owner scope |
| `version_ordinal` | `int NN` | On `scenario_version` |
| `channel_schema` | `json NN` | Stable channel ids, value types, units, rate and timestamp semantics, encoding ([SIM-03](../../requirements/products/arcscope.md#rule-sim-03)) |
| `expression_ast` | `json?` | Bounded AST ([SIM-04](../../requirements/products/arcscope.md#rule-sim-04)) |
| `fault_profile` | `json?` | Latency, jitter, drop, duplicate, reorder, disconnect, malformed, outlier ([SIM-05](../../requirements/products/arcscope.md#rule-sim-05)) |
| `content_hash` | `bytes NN` | |
| `created_at` | `instant NN` | |

- `UQ (definition_id, version_ordinal)`
- **Constraint** — a `scenario_version` is **immutable** ([SIM-02](../../requirements/products/arcscope.md#rule-sim-02)). Editing a definition creates a new version and **affects future runs only**
- **Constraint** — AST validation runs **before admission** ([SIM-04](../../requirements/products/arcscope.md#rule-sim-04)): acyclic channel dependencies, bounded depth, node count and per-tick operations. No script, dynamic compilation, reflection, file access or network

### `scope.simulation_run`

| Field | Type | Notes |
|---|---|---|
| `run_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` |
| `scenario_version_id` | `id NN` | `FK →` — **the immutable version, not the definition** ([SIM-02](../../requirements/products/arcscope.md#rule-sim-02)) |
| `seed` | `int64 NN` | |
| `execution_profile` | `text NN` | Pins numeric semantics, RNG, generator and encoding versions ([SIM-07](../../requirements/products/arcscope.md#rule-sim-07)) |
| `clock_mode` | `enum(realTime, accelerated) NN` | Pacing **never changes sample values, logical timestamps or hashes** ([SIM-06](../../requirements/products/arcscope.md#rule-sim-06)) |
| `duration_ticks` | `int64 NN` | The requested finite logical range |
| `state` | `enum(queued, starting, running, pausing, paused, stopping, canceled, succeeded, failed) NN` | ([SIM-08](../../requirements/products/arcscope.md#rule-sim-08)) |
| `terminal_reason` | `text?` | |
| `completed_ticks` | `int64 NN` | **Partial extent is queryable** ([SIM-08](../../requirements/products/arcscope.md#rule-sim-08), [SIM-09](../../requirements/products/arcscope.md#rule-sim-09)) |
| `service_term_id` | `id NN` | `FK →` — official simulation requires an active term ([SIM-17](../../requirements/products/arcscope.md#rule-sim-17)) |
| `rev` | `rev NN` | |
| `created_at`, `updated_at` | `instant NN` | Admission and latest durable transition |
| `pacing_origin_at` | `instant?` | Real-time wall origin, reset on explicit resume |
| `pacing_origin_tick` | `int64 NN` | Committed logical tick at that origin |
| `next_due_at` | `instant?` | Nonterminal next wake; indexed for Cron rescue |
| `pacer_epoch` | `bigint NN` | Increases on pause/resume/cancel/recovery fencing |

- `IX (workspace_id, state)`; `IX (state, updated_at)`; `IX (state, next_due_at)` — the scheduler path
- **Constraint** — `succeeded` requires `completed_ticks = duration_ticks`. **A cancel records a partial outcome, never success for an incomplete range** ([SIM-08](../../requirements/products/arcscope.md#rule-sim-08))
- **Constraint** — a terminal run cannot be resurrected; a duplicate start creates no second run ([SIM-09](../../requirements/products/arcscope.md#rule-sim-09))

### `scope.simulation_lease`

| Field | Type | Notes |
|---|---|---|
| `run_id` | `id` | **PK** — one live lease per run |
| `holder_instance` | `text NN` | |
| `fence_token` | `int64 NN` | **Monotonic**; a publish carrying a stale token is rejected ([SIM-10](../../requirements/products/arcscope.md#rule-sim-10)) |
| `expires_at` | `instant NN` | |

- **Rule** — this is what lets N identical replicas run the simulator without two of them publishing the same logical segment ([RT-04](../05-cloud-architecture.md#rule-rt-04), [SIM-10](../../requirements/products/arcscope.md#rule-sim-10))

### `scope.simulation_segment`

The manifest over immutable object-storage segments ([SIM-11](../../requirements/products/arcscope.md#rule-sim-11)).

| Field | Type | Notes |
|---|---|---|
| `segment_id` | `id` | **PK** |
| `run_id` | `id NN` | `FK →` |
| `sequence` | `int64 NN` | |
| `logical_from_tick`, `logical_to_tick` | `int64 NN` | |
| `sample_count` | `int64 NN` | |
| `encoding` | `text NN` | |
| `byte_length` | `int64 NN` | |
| `content_hash` | `bytes NN` | Client-verifiable ([SIM-13](../../requirements/products/arcscope.md#rule-sim-13)) |
| `object_key` | `text NN` | |
| `fence_token` | `int64 NN` | The token under which it was published |

- `UQ (run_id, sequence)`; `UQ (run_id, logical_from_tick)`
- **Constraint** — **a committed manifest row never references an unverified partial object** ([SIM-11](../../requirements/products/arcscope.md#rule-sim-11)). The object is written and verified first; the manifest row is the commit point
- **Rule** — an incomplete object stays **invisible** and is cleaned; visibility is the manifest row, not the object's existence

### `scope.simulation_checkpoint`

| Field | Type | Notes |
|---|---|---|
| `run_id` | `id` | **PK** |
| `next_tick` | `int64 NN` | |
| `rng_state` | `bytes NN` | Per channel and per fault source, independently seeded ([SIM-05](../../requirements/products/arcscope.md#rule-sim-05)) |
| `generator_state` | `json NN` | |
| `replay_position` | `json?` | For CSV replay ([SIM-18](../../requirements/products/arcscope.md#rule-sim-18)) |
| `pending_fault_state` | `json NN` | Reorder and duplicate buffers ([SIM-05](../../requirements/products/arcscope.md#rule-sim-05)) |
| `committed_segment_sequence` | `int64 NN` | |
| `updated_at` | `instant NN` | |

- **Constraint** — the checkpoint advances **only after** the corresponding manifest row commits ([SIM-11](../../requirements/products/arcscope.md#rule-sim-11), [SIM-12](../../requirements/products/arcscope.md#rule-sim-12))
- **Rule** — pause/resume, host loss and lease takeover produce **the same remaining canonical data**, with no duplicate and no missing logical range ([SIM-12](../../requirements/products/arcscope.md#rule-sim-12)). This is the single most important simulator invariant, and [SIM-20](../../requirements/products/arcscope.md#rule-sim-20) tests it by killing the host

---

<a id="84-cloud-notes-canonical-model"></a>

## 8.4 `notes` — canonical Cloud knowledge store

Notes scalar value/config/query semantics are fixed by [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile). The [desktop logical property/view fields](02-desktop-data-model.md#property_definition-property_value), including `semantic_rev`, query profile and definition revision bindings, project identically to Cloud; Cloud rows use Cloud revisions rather than local pending tokens. Saved views require one notebook. An acknowledged Notes dataset token advances with relevant membership/value/trash changes; the query reads one consistent token and rejects a stale page cursor. There is no nullable workspace-wide saved-view variant.

Every block/attachment payload and immutable revision snapshot preserves its [content origin](02-desktop-data-model.md#content-origin-storage). Direct HTTP, sync, authorized tool writes and export use the same typed validators: a caller cannot clear known AI origin, reinterpret a property type or execute an unknown query profile. Scope/Slate metadata replicas preserve origin/profile fields while leaving native content authority local.

Cloud owns acknowledged Notes content. SQLite holds a projection of these shapes plus the device's pending-edit journal. `sync.change` is a publication index, not the body store. All Notes keys and references include `workspace_id`; repository APIs require the authenticated workspace, and compound foreign keys prevent cross-workspace or cross-notebook placement.

| Table | Keys, fields and constraints | Read/write paths |
|---|---|---|
| `notes.notebook` | PK `(workspace_id, notebook_id)`; `title`, `state(active,trashed)`, `rev`, `created_at`, `updated_at`, `trashed_at?`; notebooks do not nest | Workspace list, sync scope, default capture destination |
| `notes.folder` | PK `(workspace_id, notebook_id, folder_id)`; `parent_folder_id?`, `name`, `ordinal`, `state(active,trashed)`, timestamps; parent FK in the same notebook, RESTRICT on delete; no independent revision | Notebook tree; index `(workspace_id, notebook_id, parent_folder_id, ordinal, folder_id)` |
| `notes.document` | PK `(workspace_id, document_id)`; `notebook_id`, `folder_id?`, independent `title`, `state(active,trashed)`, `rev`, timestamps; placement FK into the same notebook; no document parent field | Folder listing, recent documents, acknowledged document fetch |
| `notes.block` | PK `(workspace_id, block_id)`; unique `(workspace_id, document_id, block_id)` for same-document parent references; `document_id`, `parent_block_id?`, `ordinal`, `kind`, canonical typed `InlineContent`/kind payload; parent FK scoped to the same document; no independent revision | Ordered document reconstruction; content uses the editing architecture's V1 kinds |
| `notes.document_link`, `notes.document_tag`, `notes.property_value` | Child rows of a document; stable target identifiers, typed scalar values; a reference to another document may be unresolved and never cascades deletion to its source | Forward links, tags and property queries; mutations increment the document revision |
| `notes.tag`, `notes.property_definition`, `notes.saved_view` | Independently revisioned roots; scalar property types only; saved views contain typed filter/sort and `list` or `table` configuration, never document ownership | Workspace classification and opt-in query views |
| `notes.aggregate_revision` | PK `(workspace_id, aggregate_kind, aggregate_id, rev)`; `parent_rev`, immutable canonical snapshot or verified `payload_object_id`, `schema_version`, actor/source/command identity, time, optional Task/capability/approval attribution | History, checkpoint, conflict recovery, revision-pinned export; retention never removes a pinned revision |
| `notes.checkpoint` | PK `(workspace_id, checkpoint_id)`; target aggregate and revision, label, creator/time; references an existing revision | User checkpoint listing and restore as a new revision |
| `notes.link_index` | Derived backlink rows keyed by stable source/target identity and source revision | Rebuilt from document links; not canonical and not a second writer |

The child field shapes for blocks, links, tags and scalar values are shared with [the desktop model](02-desktop-data-model.md#3-arcnotes-local-store). D1 uses typed columns and `JSON TEXT` for the declared content structures; SQLite uses equivalent explicit SQL and validated JSON. Provider-specific storage types never enter contracts. Notebook/folder placement, revision ownership and the server-side constraints are defined here, not inferred from a local table name.

| # | Rule |
|---|---|
| ND-01 | **Folder structure belongs to the Notebook aggregate.** Creating, renaming, reordering, reparenting or trashing a folder takes the notebook's expected revision and increments it once. Under that root revision guard, reject cycles, cross-notebook parents and an active child under a trashed ancestor. Sibling order is deterministic by `(ordinal, id)` including root folders; names need not be unique. |
| ND-02 | **Document placement belongs to the Document aggregate.** A move validates the source and destination notebook/folder under guards for both notebook revisions and the document revision. It carries both notebook revisions and the document revision. A cross-notebook move changes placement and emits the removal/addition projections without changing DocumentId, BlockIds or history. An upload, AI edit or import cannot bypass this operation. |
| ND-03 | **Folder trash is a visibility operation, not recursive content deletion.** Descendants remain in place and are hidden by the repository's ancestor-state predicate. Restoring the folder restores that visibility; independently trashed documents stay trashed. Permanent folder removal requires an empty subtree after explicit move or tracked purge; FK RESTRICT enforces it. Notebook deletion uses the tracked deletion lifecycle, never an unbounded cascade in a request handler. |
| ND-04 | **Every accepted content commit stores the current rows, immutable revision, command receipt and publication row in one unit of work.** Resource participants pin attachments and any staged revision body. No network or blob upload occurs while the transaction is open. Conflict rejection preserves the proposed content and does not change current rows. |
| ND-05 | **Read paths have one authority.** Hydration and `sync.getAggregate` reconstruct these canonical rows; local pending data never enters a Cloud export or AI context. History restore creates a new revision. Export freezes a manifest of notebook structure and document revisions, pins their attachments, then renders the Cloud Markdown/attachment/fidelity download from that manifest. It is not a re-importable native Notes package. |
| ND-06 | **Local edits and remote updates share domain validation.** The client catches invalid structure early; Cloud repeats all checks as the final owner. A document's `rev` governs blocks and document metadata. Folder and document operations use explicit typed requests, with bounded bulk operations and per-operation receipts. |
| ND-07 | **All durable payloads are accounted for.** Large revision bodies are staged as verified Resource objects before the Notes commit; that commit promotes them and adds a revision reference. Current content, retained history, conflict branches and active export manifests each pin the objects they need. Garbage collection starts only after the last pin and reader lease ends. |

Required operations: `CreateNotebook`, `UpdateNotebook`, `CreateFolder`, `MoveFolder`, `TrashFolder`, `RestoreFolder`, `MoveDocument`, `GetNotebookTree`, `GetDocumentRevision`, `ListHistory` and `RestoreRevision`, alongside the typed block/property operations. These are Notes application operations reached through in-process ports and typed sync proposals; no professional editor is added to Web or Mobile. A batch with a structural dependency submits the parent operation first and binds its acknowledgement before submitting the dependent operation. [WP-18.00](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) owns client/domain semantics; [WP-25.00](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.00) owns the real D1 counterpart and API integration.

### 8.5 Native-product metadata replicas

| Table | Required fields / constraints |
|---|---|
| scope.synced_aggregate / slate.synced_aggregate | workspace_id:id + aggregate_kind:text + aggregate_id:id composite PK; rev:rev NN; schema_version:text NN; payload_proto:typed blob NN; source_device_id:id NN; content_rev:bigint NN; state:enum(live,deleted) NN; created_at/updated_at:instant NN; deleted_at:instant?; IX(workspace_id,aggregate_kind,state,aggregate_id). Registered kind determines the exact validated record; state/deleted_at must agree. |
| scope.replica_revision / slate.replica_revision | workspace_id:id + aggregate_kind:text + aggregate_id:id + rev:rev composite PK; schema_version:text NN; payload_resource_id:id NN; payload_hash:hash NN; created_at:instant NN. Immutable retained revision, not a second current owner. |



`scope.synced_aggregate` and `slate.synced_aggregate` store `(workspace_id, aggregate_kind, aggregate_id)` as PK, server `rev`, schema version, typed canonical metadata payload, source device and source `content_rev`, state/tombstone and timestamps. A generated product-kind allowlist determines the DTO and validation; this is not an executable or arbitrary type-name payload. Immutable replica revisions and Resource references use the same publication and retention rules as Notes.

Cloud accepts these through each owning module's sync adapter. The native SQLite model remains the working authority for hardware/media work. Raw capture and media bodies require their explicit upload policy; proxies and render caches are excluded. Fetching a replica does not assign a native `content_rev`: a local import/reconciliation command commits a new local revision and records which Cloud revision it reconciled. [WP-35.02](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.02) and [WP-39.04](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.04) implement these adapters against the already-delivered sync infrastructure.

---

<a id="structural-move-and-complete-media-replica-constraints"></a>
### Structural and replica validation

A Notes cross-notebook move validates one explicit disposition for every used property/tag. Destination properties must have the same scalar type/scale, matching semantic revision, and complete mappings for used select options. Duplicate destination assignments, missing/trashed targets, implicit label matching or numeric conversion refuse. Explicit removal is previewed and retained in immutable history; document/block IDs and original values in old revisions survive. The preview hash binds all participating revisions and mapping. Under guards for every captured root revision, commit updates the document placement/classification and source/destination membership publications atomically. Named structural operations retain their typed command payload and results; a generic sync NotesDocument replacement cannot move an existing document.

Slate replicas encode the complete [slate.project.v1 wire projection](../contracts/04-protobuf-wire-registry.md#4-shared-record-field-registry), including every sequence timeline/graph, exact grids, colour/input assignments, bins, markers, text/subtitles, generators/nesting, keyframe scopes and managed small-asset references. Validate identity, referential closure, type/graph/nesting cycles and source contentRev before storing the immutable replica. sequence summaries cannot substitute for timelines. Originals remain opt-in; absent bytes produce Offline Media without losing edit metadata. TranscriptRecord is an immutable derived Resource artifact linked to Task/source revision; adopting it creates ordinary authored native content with retained AI origin, never a server-side rewrite of a Slate project.


## 9. `sync`

### `sync.sync_scope`

| Field | Type | Notes |
|---|---|---|
| `sync_scope_id` | `id` | **PK** |
| `workspace_id` | `id NN` | |
| `product_id` | `text NN` | |
| `scope_kind` | `text NN` | e.g. `arcnotes.notebook`, `arcscope.projectMetadata` |
| `scope_ref` | `id?` | The specific object, null for product-wide |
| `enabled` | `bool NN` | |
| `content_exclusions` | `json NN` | **Expressive enough for [I-474](../../requirements/01-normative-glossary-and-invariants.md#rule-i-474)** — raw capture excluded by default |
| `rev` | `rev NN` | |

- `UQ (workspace_id, product_id, scope_kind, scope_ref)`

### `sync.change`

The change feed. One row per aggregate revision that entered the cloud replica.

> **Corrected 2026-09-07.** The previous design allocated `change_seq` from a database sequence inside the applying transaction and asserted that this prevented false gaps. **It does not.** Sequence allocation is non-transactional and ordered by *call*, while row visibility is ordered by *commit*. Transaction A may take 100 and stay open while B takes 101 and commits; a reader then serves 101, advances its cursor past 100, and **never sees A's change when A finally commits**. Monotonic allocation is not commit order, and no watermark derived from the sequence alone repairs it.

| Field | Type | Notes |
|---|---|---|
| `change_id` | `id` | **PK** — identity only, never a cursor |
| `workspace_id` | `id NN` | |
| `aggregate_kind` | `text NN` | |
| `aggregate_id` | `id NN` | |
| `aggregate_rev` | `rev NN` | |
| `change_kind` | `enum(upsert, tombstone) NN` | |
| `origin_kind` | `enum(device, cloud) NN` | **Cloud-originated changes exist** — an assistant message needs no device ([CW-03](00-data-model-overview.md#rule-cw-03)) |
| `origin_device_id` | `id?` | **Null when `origin_kind = 'cloud'`**; set when a device submitted the change |
| `occurred_at` | `instant NN` | Wall clock, for display; **never a cursor** |
| `publish_seq` | `bigint?` | NULL until published; monotonically assigned by the publisher, preserving each aggregate's revision order (§9.1) |
| `published_at` | `instant?` | |

- `IX (workspace_id, publish_seq)` **WHERE `publish_seq IS NOT NULL`** — the only feed query path
- `IX (workspace_id, aggregate_kind, aggregate_id, aggregate_rev)` **WHERE `publish_seq IS NULL`** — find the first unpublished revision of an aggregate
- `UQ (workspace_id, aggregate_kind, aggregate_id, aggregate_rev)` — exactly one publication identity per committed revision
- **Constraint** — the row is written **in the business transaction** ([CW-06](00-data-model-overview.md#rule-cw-06)), so a committed change is always publishable
- **Constraint** — `origin_kind = 'device'` requires `origin_device_id IS NOT NULL`; `cloud` requires it to be null
- **Rule** — matching `origin_device_id` suppresses a duplicate user notification only. The client still reconciles the authoritative revision and any matching batch receipt. Null never matches; Cloud-originated changes are always processed. An origin match cannot advance `acked_local_seq` without the actual accepted batch identity/range.
- **Constraint** — `UQ (workspace_id, publish_seq)`; `publish_seq` is assigned once and never changed

#### 9.1 Publication order and a safe cursor

`change_id` is identity only. UUIDv7 includes random bits and is not a same-millisecond revision ordering mechanism. Wall clocks also do not prove transaction order. The publisher assigns `publish_seq` only to committed rows, and explicitly preserves increasing `aggregate_rev` for each aggregate.

Read primary watermark/fence and at most 100 committed unpublished rows. Select a contiguous publication batch, preserving each aggregate's revision order. One guarded D1 batch validates watermark revision/fence plus every selected change's identity/hash/unpublished state and required predecessor; assigns publish_seq in selected order and advances the watermark by exactly that count. On conflict, reread and reselect. Crash commits all or none. See model 04 §5 for interleavings; no open interactive SQL transaction crosses reads.


Each batch admits at most one revision per selected aggregate; subsequent passes advance busy aggregates fairly. Limits on aggregates, rows and transaction time are configured. Indexes serve the lowest-unpublished query; no unbounded sort/materialisation or scan past a retained history is required.

| # | Rule |
|---|---|
| <a id="rule-pb-01"></a>PB-01 | **Only committed changes are selectable.** A transaction that commits after a previous publication gets a later cursor, even if its UUID sorts earlier. A rollback leaves no change row. |
| PB-02 | **No row can appear later below an already-served cursor.** Assignment and watermark commit atomically; sequence allocation outside this transaction is prohibited. |
| <a id="rule-pb-03"></a>PB-03 | One validated publication fence per workspace. Guard the watermark revision/fence and all selected rows in the same batch; stale publisher aborts with no numbering or watermark change. |
| PB-04 | **Per-aggregate revision order is explicit.** The owner serialises its revision commits and writes each publication row in that commit. The publisher selects the lowest unpublished revision of that aggregate; it never uses UUID or timestamp order as a substitute. |
| PB-05 | **Scheduling is bounded and fair.** A persisted round-robin aggregate key prevents a hot aggregate from starving another; unpublished age and publication lag are monitored. |
| PB-06 | **There is no global business-commit-order or cross-aggregate atomic-observation guarantee.** Clients can split a publication batch across pages. Referential dependencies are resolved by stable identifiers and canonical reads, not by assuming a parent is on the preceding page. |
| PB-07 | **Publication reads immutable change fields after guarding the watermark revision.** Business writers do not mutate the watermark. There is no `SKIP LOCKED` claim scan over change rows; the current fence and lowest-unpublished predicate supply the exclusion/order. This is a design algorithm, with D1 fault-injection evidence still required by [PG-17](../../assurance/open-gates-register.md#rule-pg-17). |

#### 9.2 Bootstrap, application and retention

| # | Rule |
|---|---|
| CU-01 | **A cursor binds workspace, scope/filter generation and `publish_seq`.** It is opaque and authenticated. Changing selective-sync scope requires a new bootstrap; a cursor cannot silently change its filter. |
| CU-02 | Bootstrap pins a primary-read lower-bound publication cursor W and scans primary aggregate/tombstone pages by immutable stable key. It is a convergent bootstrap, not a multi-request SQL snapshot. Return actual row revisions and replay all published changes above W through a captured completion high water. Pages/pin expire after 15 minutes or 100 MiB metadata; exceedance returns bootstrap_expired and preserves pending client work. model 04 §5 defines interleavings. |
| CU-02a | **The snapshot may contain revisions published after W.** Return each aggregate's actual revision, including tombstone/state. Clients apply only a strictly newer Cloud revision; equal is idempotent and older is ignored. Thus replay above W cannot replace a newer snapshot with an older, previously unseen revision. |
| CU-03 | **An expired cursor or expired bootstrap pin returns `sync.cursor_expired`.** Resync replaces only acknowledged shadow/cache data. Durable local journals, unacknowledged uploads and tool receipts survive and are rebased; they are not discarded with the cache. |
| CU-04 | **A feed page is processed durably.** Persist the page, then atomically apply/stage every item and advance its cursor. A dependent object may be fetched with `sync.getAggregate(minRevision)` before exposing the relationship, or shown as an explicit unresolved reference pending that fetch. No missing page/dependency is treated as deletion. |
| CU-05 | **Canonical reads return a revision at least as new as the requested minimum, or its explicit tombstone.** Later revisions can subsume intermediate upserts. A hard-purged object behind the retention floor requires resync, never a fabricated empty body. |
| CU-06 | **Monotonicity is per aggregate, including deletion and restore.** Compare incoming Cloud revision to the retained shadow/tombstone watermark; ignore smaller or equal revisions. Apply a newer shadow and rebase pending local edits in one local transaction. A tombstone cannot erase pending work; it creates a recoverable conflict. |
| CU-07 | **Retention observes active bootstrap/export/reader pins.** Pins have bounded lifetimes and quotas. Tombstone pruning raises the retention floor; a device below it must bootstrap. A delayed receipt/feed echo never resurrects an older body. |

### `sync.publication_watermark`

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | `id` | PK |
| `last_seq` | `bigint NN` | Highest committed publication sequence |
| `last_aggregate_key` | `text?` | Durable bounded round-robin scheduling position |
| `holder_instance` | `text?` | Current publisher |
| `fence_token` | `bigint NN` | Increased on each acquisition |
| `lease_expires_at` | `instant?` | Authoritative database time |
| `updated_at` | `instant NN` | |

Acquisition updates holder/expiry and increments the fence under a conditional atomic D1 batch guard. Publication rechecks them in its own guarded D1 batch. `last_seq` never decreases. `sync.bootstrap_manifest` records workspace/scope, W, immutable page references, build state, expiry and the retention pin; partial manifests are invisible and their staged objects are swept. This is bounded background work in the existing host.

### `sync.tombstone`

| Field | Type | Notes |
|---|---|---|
| `aggregate_kind`, `aggregate_id` | **PK** | |
| `workspace_id` | `id NN` | |
| `deleted_at` | `instant NN` | |
| `deleted_by_device_id` | `id?` | |
| `retain_until` | `instant NN` | `§7.1` of the overview |

- `IX (retain_until)` — the purge sweeper
- **Constraint** — a device whose cursor predates the oldest retained tombstone **must** full-resync; the feed returns `sync.cursor_expired` rather than a silently incomplete delta ([WP-25.02](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.02))

### `sync.conflict`

| Table | Required fields / constraints |
|---|---|
| sync.conflict | conflict_id:id PK; workspace_id:id NN; aggregate_kind:text NN; aggregate_id:id NN; base_rev/current_rev:rev NN; incoming_hash:hash NN; retained_version_ref:id NN; policy_version:text NN; state:enum(unresolved,resolved) NN; resolution:Key?; created_at:instant NN; resolved_at:instant?; resolution_command_id:id? UNIQUE; rev:rev NN; IX(workspace_id,state,created_at). Losing content is retained before resolution receipt. |



Records a detected conflict, the policy applied, and — where a policy discarded a version — **a reference to the retained discarded version** ([WP-25.03](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.03)). A discarded version is never destroyed.

---

## 10. `resource`

### `resource.cloud_object`

| Field | Type | Notes |
|---|---|---|
| `cloud_object_id` | `id` | **PK** |
| `quota_reservation_id` | `id NN` | Storage/staging reservation group; promotion and verified deletion settle its gauges |
| `workspace_id` | `id NN` | |
| `owner_product` | `text NN` | |
| `content_hash` | `text NN` | Content address |
| `size_bytes` | `bigint NN` | |
| `content_type` | `text?` | |
| `sensitivity` | `enum(public, internal, confidential, restricted) NN` | |
| `state` | `enum(staged, verified, committed, releasing, deleted) NN` | The lifecycle of `§7` of the sync architecture |
| `storage_key` | `text NN` | **Server-issued**; a client never chooses it ([BR-10](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-br-10) of [WP-23](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23)) |
| `reference_count` | `int NN` | |
| `last_reference_released_at` | `instant?` | Starts the grace period |
| `created_at` | `instant NN` | |

- `IX (workspace_id, state)`; `UQ (workspace_id, content_hash, size_bytes)` for live physical objects — deduplication within an authorised workspace; `IX (state, last_reference_released_at)` — the garbage collector's only path
- **Constraint** — `reference_count ≥ 0`, and a reference is only published when `state = committed` ([XS-05](00-data-model-overview.md#rule-xs-05))
- **Constraint** — committed-use projection sums committed/releasing objects until verified physical deletion. Staged/verified objects hold admission and staging reservations. A logical reference release does not immediately free bytes or permit staging-limit bypass.

### `resource.object_reference`

| Field | Type | Notes |
|---|---|---|
| `cloud_object_id` | `id NN` | **PK part 1** |
| `referrer_kind`, `referrer_id` | `text NN`, `id NN` | **PK parts 2, 3** |
| `created_at` | `instant NN` | |

- The reference count is **derived from this table**, not incremented independently — which is what makes a crash mid-operation recoverable ([WP-07.04](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.04))

### `resource.upload_session`

`upload_session` stores `upload_id PK`, workspace, operation/idempotency key, server-issued object key, expected hash, declared maximum bytes, received chunk bitmap with verified chunk lengths, reservation-group ID, state `receiving/verifying/verified/promoted/expiring/deleted`, created/expiry times and bounded extension count. Unique `(workspace_id, operation_key)` returns the same session. Oversize/chunk mismatch refuses further upload and enters cleanup. Completion verifies bytes/hash and creates a **Verified** object plus a provisional pin; it does not publish an owner reference. Owner commit enlists Entitlement, Resource and Sync where applicable, promotes to Committed, converts storage quota and pins the object atomically. Duplicate completion/promotion returns the recorded receipt.

The table also stores sealed_parts_proto:PartReceipt[]?, verification_job_id:id?, verification_state:pending/running/verified/failed, verification_hash:hash?, provisional_pin_id:id?, completed_at:instant?, rev:rev NN. `resource.upload_part` has PK(upload_id,part_number), offset/length:uint64 NN, sha256:hash NN, provider_receipt:text NN, verified_at:instant NN. Exact repeat is accepted; changed bytes at an accepted part number refuse. Complete seals the immutable manifest and enters verifying; only a verified result creates the object/pin.

Expiry forbids new writes and starts idempotent physical cleanup. The sweeper verifies deletion before releasing staging/storage reservations. An object-store timeout leaves cleanup retryable and exposure held; a bounded deployment staging limit prevents abandoned sessions from exhausting unaccounted storage. Partially received multipart uploads are explicitly aborted through the storage adapter.

---

<a id="search-inference-job-execution-record"></a>
## 10.1 `search` — inference jobs

Search owns search.inference_job as the canonical business control/receipt record; vectors and reranked candidates remain derived. It is a bounded platform Job, not task.task or a second AI loop. The private [CF inference ports](../contracts/05-cloudflare-integration.md#8-session-bindings-inference-jobs-and-deployment-transitions) carry this identity.

| Fields | Type and invariant |
|---|---|
| job_id; workspace_id; principal_id; service_term_id | id PK and non-null scoped owner/eligibility identities; scheduled indexing uses its explicit operator-job grant for that workspace, never a fabricated interactive session |
| purpose; input_hash; source_manifest_ref; source_set_hash | embedding/rerank; exact hash plus immutable ResourceVersionRef; input hash includes kind, normalized input, ordered source revisions/hashes, principal/scope/policy snapshot, model/profile/config and effective budget |
| model_descriptor_id; config_revision_id; profile | Pinned activated catalogue/config and selected inference profile; no dynamic provider fallback |
| state; reason; rev; created_at; updated_at; deadline | queued/running/unknown/succeeded/failed/cancelled; named reason, monotonic revision and UTC instants. Admission-to-result deadline 120 seconds; before-dispatch expiry refuses, possible-dispatch expiry is unknown |
| logical_request_id; provider_attempt_id; intent_receipt | Existing Commerce identities, one bounded invocation per admitted job; beneficiary=platformIndexing, funding_class=platformJob, operator_job_ref=job_id. No customer capacity reservation/tariff/settlement |
| workflow_id; worker_version; recovery_generation; lease_holder; lease_epoch; lease_expires_at | Same deterministic CF ID and observed version as the private contract; conditional 60-second claim, renewal 20 seconds; old epoch cannot act after takeover/expiry |
| result_ref?; outcome_receipt?; outcome_hash?; source_publication_ref? | Immutable validated result and canonical outcome digest/receipt. succeeded requires complete result; unknown has no claim of completion. Projection delivery receipt records publish/discard under current source/policy; never provider content in Commerce |
| cancellation_requested_at?; completed_at? | Cancellation blocks new dispatch/publication; an already-sent invocation still records supplier facts under the existing uncertainty policy |

Stable job_id comes from the committed Search source/query command, reused on outbox/redelivery. Reusing it with a different input hash is conflict. Unique logical request/attempt references and the outcome hash make receipts idempotent. Model calls never retry merely because a job/lease expired; a proven pre-dispatch refusal may be rescheduled by a new authorized job, and unknown attempts stay in supplier reconciliation. New source/model/config revisions produce new input identities, not edits to old outcomes.

The two enumerated Search families in the [transaction authority](00-data-model-overview.md#611-shared-units-of-work) use each module's own SQL port in one D1 batch; no external CF/R2 call occurs inside the commit. Search is after Task and before Notification in statement order. The dispatch outbox creates/gets the exact Workflow; CF input fetch rechecks current source permissions, active service term and AI-exclusion policy. Source deletion/revocation cancels queued jobs and invalidates derived publication even when a late output is complete.

Record every supplier attempt and keep unresolved exposure through expiry/period closure. A complete result may coexist with costUnconfirmed; it cannot create a customer debit or release conservative liability. Retain accounting identity/receipt under existing commerce retention; source text/result pins use Resource content/deletion policy, never extend user-content retention merely to retain cost evidence. A completed projection consumer releases ephemeral pins; interrupted consumers retry idempotently and rebuild readiness from current authoritative source, never from CF checkpoint data.


### Service object and recovery receipts

| Table | Required fields / constraints |
|---|---|
| resource.service_object_grant | grant_id:id PK; realm_id/workspace_id/owner_job_id:id NN; owner_kind:Key NN; attempt_id:id?; epoch/recovery_generation:bigint NN; direction:enum(read,write) NN; resource_id:id NN; upload_id:id?; byte_limit:bigint NN; expires_at:instant NN; revoked_at:instant?; IX(expires_at). Limits and current owner lease checked each use. |
| task.cf_instance_inventory / chat.cf_instance_inventory / search.cf_instance_inventory / resource.cf_instance_inventory | kind:text + instance_id:text + recovery_generation:bigint composite PK; workspace_id/owner_job_id:id NN; worker_version:text NN; deletion_receipt:text?; updated_at:instant NN. Each owner writes its own rows; deletion coordinator reads via ports. |
| platform.safety_receipt | journal_record_id:text PK; record_hash:hash NN; owner_command_id:id NN; recovery_generation:bigint NN; kind:Key NN; status:enum(pending,verified) NN; independent_receipt:text?; created_at:instant NN; verified_at:instant?; IX(status,created_at). Verified receipt is required before the protected success/dispatch. |
| platform.recovery_epoch | realm_id:id PK; recovery_generation:bigint NN; recovery_point:text NN; journal_inventory_hash:hash NN; state:enum(fenced,restoring,reconciling,open) NN; updated_at:instant NN; rev:rev NN. Installed generation cannot decrease. |



Resource service_object_grant stores grant_id PK, owner_kind/job_id, attempt_id?, realm/workspace, epoch, recovery_generation, direction, resource/upload_id, byte_limit, expires_at and revoked_at. It uses the existing upload reservations/verification pins, not a second object lifecycle. Every grant authorization validates its current owner job and fence. Task/Search/Resource keep cf_instance_inventory keyed by kind/instance_id/generation with owner workspace/job, actual worker version and deletion receipt; each module writes only its owned rows and exposes inventory through the deletion coordinator.

platform.safety_receipt records immutable external journal record ID/hash, related owner command/intent ID, generation, kind and pending/verified status. It is a local receipt/cache, never authority over the independent signed journal head. Outbox dispatch cannot pass its external boundary before verified barrier; security denial cannot return durable success before verified fence. platform.recovery_epoch records the installed independent generation, recovery point, journal inventory hash and reopening state. Restored outstanding effects have explicit quarantined/unknown reconciliation records, retaining original identities even when their newer D1 outcome was outside the recovery point.


### Purpose-bound source consent

| Table | Required fields / constraints |
|---|---|
| resource.source_consent | consent_id:id PK; realm_id/workspace_id/actor_id:id NN; operation_id/purpose:Key NN; source_manifest_hash:hash NN; policy_rev:rev NN; max_bytes:bigint NN; expires_at:instant NN; consumed_at/revoked_at:instant?; generation:bigint NN; IX(expires_at). The one-use receipt binds the declared source/purpose/operation and current policy/recovery generation; it never changes durable source policy or grants arbitrary egress. |


## 11. `notification`, `policy`, `audit`, `support`, `trustsafety`

| Table | Key points |
|---|---|
| `notification.notification` | notification_id:id PK; workspace_id/user_id:id NN; product_id:ProductId?; kind:Key NN; owner_ref:AggregateRef NN; durability:enum(durable,transient) NN; created_at:instant NN; expires_at/resolved_at:instant?; rev:rev NN. Carries **durability class** (`durable` \| `transient`). A durable item persists until resolved regardless of push delivery ([WP-10.04](../../planning/work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.04)). `IX (workspace_id, durability, resolved_at)` |
| `notification.push_registration` | registration_id:id PK; device_id/installation_id:id NN; registration_revision:bigint NN; encrypted_token/token_hash:text NN; recovery_generation:bigint NN; updated_at:instant NN. Per authorized device/installation, UQ(device_id,installation_id), increasing registration_revision, encrypted token, token_hash, platform=android-fcm, recovery_generation and updated_at. RegisterPush rotates/upserts transactionally, supersedes old pending intents and recreates only still-authorized unresolved/unexpired intents at the new revision; logout/device revoke/UnregisterPush removes current row. Confirmed token-invalid receipt compares registration_id/revision/token_hash/generation before deletion; stale response cannot delete a replacement. Wrong project/payload is not invalid-token evidence. |
| `notification.push_delivery` | delivery_id:id PK; notification_id/registration_id:id NN; registration_revision/recovery_generation:bigint NN; expires_at/next_attempt_at/created_at:instant NN; attempt_count/lease_fence:bigint NN; provider_message_id:text?; last_reason:ReasonCode?; completed_at:instant?. Unique(notification_id,registration_id,registration_revision,recovery_generation), notification-owned creation transaction plus outbox. Fields: delivery_id, expires_at, state(pending/sending/providerAccepted/expired/invalidated/configurationFailed), attempt_count, next_attempt_at, lease_fence, provider_message_id?, last_reason, created_at, completed_at?. No payload text or token copy. A crashed sending claim may retry within TTL after fence takeover; physical duplicates are permitted and client-deduplicated. Delete completed delivery diagnostics after 30 days; durable notification retention is independent. |
| `policy.policy_bundle` | bundle_id:id + version:bigint composite PK; schema_version:text NN; document_proto:PolicyBundle NN; hash/signature:text NN; issued_at/expires_at:instant NN. Versioned, signed, append-only. Carries `schema_version` and the full validated document. A bundle is applied atomically or not at all ([WP-44.01](../../planning/work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.01)) |
| `policy.rollout_assignment` | installation_id:id + rollout_id:id composite PK; rule_version:bigint NN; bucket:int NN; expires_at:instant NN. *(derived)* — deterministic per installation, so it can be recomputed rather than stored; stored only as a cache with the rule version it came from |
| `audit.audit_event` | event_id:id PK; workspace_id:id?; actor_ref:text NN; actor_proto:ActorChain NN; event_type:Key NN; reason:ReasonCode NN; correlation_id/command_id:id?; target_ref:AggregateRef?; occurred_at:instant NN; payload_proto:typed event-schema JSON NN (registered event kind, IDs, revision/hash and disposition only; no content or secret); previous_hash/event_hash:hash NN. **Append-only under normal application/operator roles; only approved expired-partition retention purge may delete** ([AU-01](../13-observability-and-operations.md#rule-au-01)). Carries the full actor chain, the enumerated event type, the reason code and the correlation identifier. `IX (workspace_id, occurred_at)`; `IX (actor_ref, occurred_at)`. Retention follows the explicit security/financial policy and holds, independently of short telemetry windows |
| `support.support_case` | case_id:id PK; workspace_id/user_id:id NN; category/subject:text NN; state:enum(open,inProgress,awaitingUser,resolved,closed) NN; diagnostic_ref:id?; created_at/updated_at:instant NN; rev:rev NN; IX(user_id,state,updated_at). Messages use support.case_message(message_id:id PK,case_id:id FK,ordinal:bigint NN,actor_ref:text NN,text:text NN,created_at:instant NN,UQ(case_id,ordinal)). Links to a **diagnostic reference**, never to content ([WP-45.06](../../planning/work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.06)) |
| `support.access_grant` | access_id:id PK; case_id:id FK NN; workspace_id/user_id:id NN; operator_subject:text NN; scope_proto:typed support.access.v1 JSON NN (case-bound resource IDs, allowed read/export actions and purpose; no wildcard or arbitrary SQL); proposal_hash:hash NN; consented_at:instant?; expires_at:instant NN; revoked_at:instant?; rev:rev NN. Scoped, expiring, consented where required, and **itself audited** ([OP-04](../13-observability-and-operations.md#rule-op-04)). `IX (expires_at)` |
| `trustsafety.report` | report_id:id PK; reporter_user_id:id NN; subject_ref:AggregateRef NN; reason:ReasonCode NN; evidence_ref:text NN; state:enum(received,reviewing,actioned,dismissed) NN; action_id:id?; created_at/updated_at:instant NN; rev:rev NN; IX(state,created_at). Evidence access is purpose-bound and audited; reports alone do not grant content access or apply enforcement. |
| `trustsafety.enforcement_action` | action_id:id PK; subject_ref:AggregateRef NN; level/reason:Key NN; evidence_ref:text NN; operator_subject:text NN; notification_id:id NN; appeal_state:enum(none,pending,upheld,reversed) NN; created_at:instant NN; expires_at:instant?; rev:rev NN; IX(subject_ref,created_at). Records the ladder position, the reason, the communication sent and the appeal state |

---


### Notification email delivery

| Table | Complete fields and constraints |
|---|---|
| notification.delivery | delivery_id:id PK; user_id:id FK NN; template_version/purpose/recipient_hash:text NN; recipient_secret_ref:text NN; state:enum(pending,sending,providerAccepted,unknown,rejected,bounced,complained,expired,canceled) NN; challenge_ref:id?; security_epoch:bigint NN; current_attempt_id:id?; created_at/expires_at:instant NN; rev:rev NN; IX(state,expires_at). Recipient and template variables are encrypted purpose-limited inputs; no raw proof in telemetry. |
| notification.delivery_attempt | attempt_id:id PK; delivery_id:id FK NN; provider:enum(postmark,ses) NN; dispatch_state:enum(prepared,dispatched,accepted,rejected,unknown) NN; request_hash:hash NN; provider_message_id:text?; accepted_at:instant?; outcome:Key?; reconciled_at:instant?; UQ(provider,provider_message_id); IX(dispatch_state,reconciled_at). Intent commits before dispatch; unknown is not rejection. |
| notification.provider_event | provider:text + event_id:text composite PK; delivery_id/attempt_id:id NN; body_hash:hash NN; kind:Key NN; received_at:instant NN; applied_at:instant?; contradictory replay is rejected. If the provider has no event ID, use canonical message ID/event kind/provider timestamp/body hash as its deterministic key. |
| notification.suppression | recipient_hash:text + stream:enum(security,broadcast) composite PK; reason:enum(hardBounce,complaint,operator) NN; provider_event_id:text?; created_at:instant NN; cleared_at:instant?; rev:rev NN. Permanent bounce/complaint stops retries on that stream and alerts the owner to use another verified recovery route. Clearing requires corrected destination or audited operator evidence, never blind failover. |

Templates, domain/provider settings, expiry and callback authentication are fixed by architecture 13/contracts 08. An attempt cannot restore an expired challenge or change account state. Unknown outcomes reconcile original provider evidence; absence of a search hit never authorizes secondary dispatch. Retain only proof-safe delivery metadata after challenge expiry; destroy recipient/template secret material after the delivery retention policy.

### Source knowledge policy

| Table | Required fields / constraints |
|---|---|
| policy.source_policy | workspace_id:id + target_kind:Key + target_id:id composite PK; revision:rev NN; searchable/cloudIndexAllowed/aiRetrievalAllowed/managedAiProcessingAllowed:bool?; updated_by:id NN; updated_at:instant NN; command_id:id NN. Four nullable overrides map exactly to KnowledgePolicyPatch in registry 04 and the source-policy rules in contracts 07; null inherits. |

Owner/resource existence and authorization are checked through owner ports; no cross-module write. Command receipt, policy revision, audit event and index-reconciliation outbox commit atomically under Policy+Audit with the target's current scope/recovery generation. Clear creates a versioned inherited-state row rather than deleting the command fence. Source consent records reference exact policy revision, explicit temporary patch, operation/source hash and expiry; no durable policy write occurs when the receipt is used. Search and dispatch always read current effective policy; source.getPolicy gives the client its current projection. No generic sync body can write this table.

## 11.1 `package_catalog`

| Table | Fields / constraints |
|---|---|
| publisher | publisher_id:id PK; owner_user_id:id FK NN; domain:text UNIQUE NN; state:pending/verified/suspended; challenge_hash:text NN; challenge_expires_at:instant NN; verified_at:instant?; rev:rev NN. DNS verification rules are registry 04 authority. |
| package | package_id:text PK; publisher_id:id FK NN; name/summary/kind:text NN; created_at:instant NN; rev:rev NN. Publisher binding immutable; no package ID takeover. |
| version | package_id:text FK + version:text composite PK; submission_id:id UNIQUE NN; archive_resource_id:id NN; digest/manifest_hash:text NN; state:submitted/reviewing/published/rejected/revoked; submitted_at:instant NN; published_at:instant?; rev:rev NN. Archive immutable; submission ownership follows publisher. |
| review | review_id:id PK; submission_id:id FK NN; operator_subject/decision/reason/evidence:text NN; proposal_hash:text NN; decided_at:instant NN; command_id:id UNIQUE NN. Append-only and separate from customer access. |
| revocation | revocation_id:id PK; package_id/version composite FK NN; reason/operator_subject:text NN; revoked_at:instant NN; publication_revision:bigint UNIQUE NN; command_id:id UNIQUE NN. Never erase a published revocation. |
| publication | channel:text PK; revision:bigint NN; index_hash/revocation_hash:text NN; signed_object_ref:text?; state:pending/published; updated_at:instant NN. Guarded revision advances with review/revocation; outbox publishes immutable signed snapshots. |

## 12. Constraints that span modules

These cannot be foreign keys ([AG-01](00-data-model-overview.md#rule-ag-01), [MD-02](../05-cloud-architecture.md#rule-md-02)). Each is an application invariant with a named enforcement point and a data-health check.

| # | Invariant | Enforced at | Detected by |
|---|---|---|---|
| CX-01 | Every `entitlement.grant` with `source = purchase` corresponds to a completed `commerce.order` | Commerce's grant issue call | Reconciliation ([WP-42.08](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.08)) |
| CX-02 | With Commerce enabled, every customer AI capacity reservation in `held` maps to one unsettled normalized logical request; Entitlement-only operation validates its own admission receipt without a Commerce schema/FK | Reservation creation, in the shared unit of work ([SU-01](00-data-model-overview.md#rule-su-01)) | The reservation sweeper ([UU-03](../20-cross-system-lifecycles.md#rule-uu-03) of the cross-system lifecycles) |
| <a id="rule-cx-08"></a>CX-08 | For every workspace, the sum of live `capacity_reservation.from_capacity_micro` equals `capacity_bucket.held_micro`, and the sum of `from_compensation_micro` + `from_purchased_micro` per lot equals that lot's `held_micro` | The shared unit of work ([FU-04](#rule-fu-04)) | Accounting comparison ([WP-42.11](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11)) |
| CX-09 | Every customer-benefiting settled `logical_ai_request` has exactly one non-adjusting `customer_settlement`, and at least one `provider_attempt`; **the counts are not required to match** ([FU-03](#rule-fu-03)) | Settlement, in the shared unit of work | Reconciliation ([WP-43.07](../../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07)) |
| CX-10 | Every `sync.change` row with a non-null `publish_seq` has a `publish_seq` less than or equal to its workspace's `publication_watermark.last_seq` | The publisher's transaction ([PB-03](#rule-pb-03)) | Feed integrity check |
| <a id="rule-cx-11"></a>CX-11 | No `capacity_bucket.available_micro` was raised past `max(previous_available, max(0, burst_in_force - held_micro))` by any operation, and a balance sitting above the current ceiling after a reduction is **not** a violation ([RF-05](../16-billing-and-commerce-architecture.md#rule-rf-05) of the commerce architecture) | The bucket update predicate | Capacity accounting check |
| CX-03 | Every `resource.object_reference` referrer exists in its owning module | Reference creation | Orphan detection ([WP-46.04](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.04)) |
| CX-04 | Every `sync.change` names an aggregate that exists or has a tombstone | The applying transaction | Feed integrity check |
| CX-05 | Every device tool request targets an eligible application installation/product and a current delivery epoch; cloud-local requests have no device target | Request creation and claim/result fence | Application-presence and command-receipt reconciliation |
| CX-06 | Every `identity.session` names a live, unrevoked device | Session issue | Device revocation cascade |
| CX-07 | `entitlement.usage_counter` for storage equals the committed sum in `resource` | — *(materialised)* | Accounting comparison ([WP-42.06](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.06)) |

---

## 13. Verification

| # | Obligation | Where |
|---|---|---|
| CV-01 | Every table round-trips every field, including nullability and enum boundaries | [WP-21.03](../../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |
| CV-02 | Every declared index exists and serves its named path at scale-corpus size | [WP-21.03](../../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |
| CV-03 | Every check constraint refuses its negative case — negative credit, orphan reference, or a device-local Step lacking its required target binding | [WP-21.02](../../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.02) |
| CV-04 | The `platform.command` reuse constraint refuses a reused id with different content | [WP-23.03](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.03) |
| CV-05 | The `provider_event` composite key makes duplicate delivery a no-op | [WP-42.03](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.03) |
| CV-06 | A cross-workspace read fails at the data layer with a forged scope | [WP-21.06](../../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.06) |
| CV-07 | Every cross-module invariant in `§12` has a detection check that fires on an induced violation | [WP-46.04](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.04) |
| CV-08 | Entitlement resolves correctly with the entire `commerce` schema absent ([EO-05](../16-billing-and-commerce-architecture.md#rule-eo-05)) | [WP-42.00](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.00) |
