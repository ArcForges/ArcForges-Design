# Cloud Data Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Data model
> Governing authority: [`00-data-model-overview.md`](00-data-model-overview.md), [`../05-cloud-architecture.md`](../05-cloud-architecture.md) `§4`, `§5`
> Companions: [`../16-billing-and-commerce-architecture.md`](../16-billing-and-commerce-architecture.md), [`../08-security-architecture.md`](../08-security-architecture.md)

One PostgreSQL database, one schema per module ([PS-01](../05-cloud-architecture.md#rule-ps-01)). A module owns its schema exclusively: no other module reads or writes its tables, and cross-module reference is by identifier plus a published module API ([MD-02](../05-cloud-architecture.md#rule-md-02), [MD-03](../05-cloud-architecture.md#rule-md-03)).

Notation is defined in [`00-data-model-overview.md`](00-data-model-overview.md) `§2`.

---

## 1. Schema map

| Schema | Module | Aggregate roots |
|---|---|---|
| `identity` | Identity | `user`, `auth_identity`, `session` |
| `workspace` | Workspace | `workspace` — **no membership table** ([WO-01](#rule-wo-01)) |
| `device` | Devices | `device`, `installation` |
| `entitlement` | Entitlement | `grant`, `entitlement_snapshot`, `usage_counter`, `service_term`, `capacity_bucket`, `capacity_policy_period`, `capacity_reservation` |
| `commerce` | Commerce | `billing_account`, `order`, `subscription`, `credit_lot`, `provider_event`, `logical_ai_request`, `provider_attempt`, `attempt_usage`, `supplier_cost_entry`, `customer_settlement` |
| `notes` | Notes | `notebook` (owns `folder`), `document` (owns `block` and document metadata), `tag`, `property_definition`, `saved_view`; immutable revision records |
| `slate` | ArcSlate Cloud | Revisioned metadata replicas; native working authority remains local |
| `chat` | Chat | `conversation`, `message` and their committed content; Task owns iteration output, CF DO owns transient stream projection |
| `task` | Task | `task`, `automation` |
| `agent` | Agent | `agent_profile`, `model_descriptor`, `tariff_version`, `supplier_price_version` |
| `sync` | Sync | `sync_scope`, `change` |
| `resource` | Resource | `cloud_object`, `upload_session` |
| `search` | Search | *(derived — see [`03-derived-stores.md`](03-derived-stores.md))* |
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
| `fence_token` | `bigint NN` | Incremented on each acquisition; checked under the lease-row lock by every effect publication |
| `state` | `enum(ready, leased, succeeded, deadLettered) NN` | |
| `payload` | `json NN` | |
| `available_at` | `instant NN` | Backoff scheduling |

- `IX (state, available_at)` — the only claim path
- **Constraint** — acquisition conditionally updates `leased_until`, holder and `fence_token` together. A stale worker may still run after expiry but cannot commit an effect: every publication locks and validates the current lease and fence inside that same transaction. Network uncertainty is handled by the dispatch barrier, not by the lease alone.

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
| `rev` | `rev NN` | |

- `IX (realm_id, state)`
- **Constraint** — a `deleted` user retains the row with all personal fields cleared; the identifier is never reused ([ID-05](00-data-model-overview.md#rule-id-05))

### `identity.auth_identity`

| Field | Type | Notes |
|---|---|---|
| `auth_identity_id` | `id` | **PK** |
| `user_id` | `id NN` | `FK →` `identity.user`; restrict |
| `method` | `enum(passkey, emailCode, password, oidc) NN` | |
| `subject` | `text NN` | Credential identifier — for passkey, the credential id |
| `public_key` | `text?` | Passkey only |
| `sign_count` | `bigint?` | Passkey replay defence |
| `label` | `text?` | User-visible name for the credential |
| `created_at` | `instant NN` | |
| `last_used_at` | `instant?` | |
| `revoked_at` | `instant?` | |

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
| `step_up_classes` | `text[]` | Which operation classes the step-up covers |

- `IX (user_id, revoked_at, expires_at)` — active-session listing and mass revocation
- `IX (device_id)` — device revocation cascade
- Partial `UQ (refresh_token_hash)` for native sessions; partial `UQ (browser_handle_hash)` for browser sessions; `IX (browser_origin, idle_expires_at)` for browser expiry maintenance.
- **Exclusive credential check:** nativeBearer requires refresh hash/generation and null browser fields; browserCookie requires handle hash/origin/idle expiry and null refresh fields. The server accepts no browser cookie on the native bearer scheme.
- **Native constraint:** presenting a superseded refresh generation revokes the family and raises a security audit event.
- **Browser constraint:** exact origin, unrevoked user/device/installation/session, absolute expiry and idle expiry are checked before authorization. The random handle is issued only in a host-only HttpOnly cookie and stored as a hash; no plaintext refresh token is stored for the browser.
- **Browser creation:** verified authentication consumes its one-use pre-auth challenge and creates/validates the lowest-trust browser device and installation through the owning modules, then creates the session in the same enlisted transaction. Follow the declared Identity → Device lock order; the browser cannot supply a trusted device assertion. Lost login responses may require reauthentication; they never cause an operation replay with increased authority.
- **Activity:** update idle expiry with a conditional write only for an unrevoked, currently unexpired session, bounded by absolute expires_at. Concurrent requests cannot revive expired/revoked rows; passive hint polls/CF stream frames do not extend session life. Logout/revocation sets revoked_at before cookie deletion and terminates live connections. Already committed commands keep their recorded result.
- **Replica/restore:** every Cloud replica validates the same store. Database restore invalidates browser sessions under the existing security recovery procedure; explicit hashed CSRF tokens and session/pre-auth state support antiforgery across replicas. Authentication needs no replica affinity or in-memory-only session authority; business transport uses gRPC-Web unary reads; AI presentation follows the CF WS/HTTP contract.
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

The row plus its separate cookie binding and antiforgery validation bind a browser challenge; a flow ID alone grants no authority. Verify the existing method proof, then atomically compare the unconsumed/unexpired row, consume it and create the session/device in the registered transaction family. Duplicate completions fail safely. Expired/consumed rows are purged under the short challenge retention policy; logs never contain challenge proofs or binding secrets. Session bootstrap does not allocate an unbounded flow on every GET: beginAuthentication creates one under abuse limits. Explicit CSRF/session state is shared in PostgreSQL; no framework Session/cookie-auth serialization is required.

### `identity.step_up_challenge`, `identity.recovery_flow`

Short-lived rows with `expires_at`, an attempt counter, and a rate-limit key. Both are swept on expiry. A recovery flow records every state transition for the audit trail, because recovery is the highest-value attack surface in the system.

---

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
| `product_id` | `text NN` | `arcchat` \| `arcnotes` \| `arcscope` \| `arcslate` \| `mobile` \| `web` |
| `app_version` | `text NN` | |
| `contract_set_version` | `text NN` | Drives the compatibility window |
| `installed_at` | `instant NN` | |
| `last_active_at` | `instant NN` | |

- `UQ (device_id, product_id)`
- `IX (contract_set_version)` — the minimum-version rollout query ([UP-11](../../requirements/10-distribution-update-and-support.md#rule-up-11))

### `device.presence`

| Field | Type | Notes |
|---|---|---|
| `device_id` | `id` | **PK**, `FK →`; cascade |
| `connection_state` | `enum(connected, disconnected) NN` | |
| `last_heartbeat_at` | `instant NN` | |
| `stale_after` | `instant NN` | |
| `eligible_for_remote` | `bool NN` | *(derived)* from trust, remote_enabled and connection |

- `IX (eligible_for_remote, stale_after)` — target selection for remote work
- **Constraint** — presence is never inferred from a valid session ([WP-26.00](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.00)). A row past `stale_after` reports disconnected regardless of `connection_state`.

---

## 6. `entitlement`

The Entitlement module is **independent of Commerce** (`§2.1` of the commerce architecture). Nothing here references a `commerce` table.

### `entitlement.grant`

| Field | Type | Notes |
|---|---|---|
| `grant_id` | `id` | **PK** |
| `workspace_id` | `id NN` | |
| `kind` | `enum(capability, quota, credit, feature) NN` | The four entitlement kinds |
| `subject` | `text NN` | The capability, quota or feature key |
| `value` | `json NN` | Kind-specific payload — a limit, a bundle reference, a boolean |
| `source` | `enum(purchase, administrative, promotional, trial, store, free) NN` | **No provider identifier appears here** ([EO-04](../16-billing-and-commerce-architecture.md#rule-eo-04)) |
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
- **Constraint** — this is a display/reconciliation projection over durable quota events and measured objects. Admission locks `quota_budget` and reserves, never trusts this projection. Storage is a non-resetting gauge; period-based simulator/egress usage carries its explicit period.

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
| `period_ref` | `text NN` | **The paid period's own identity** — the provider's invoice or billing-period id for a subscription; the order id for a pass; the grant id for a compensation or self-host term |
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
| <a id="rule-tm-04"></a>TM-04 | Term rows are immutable. Supersession/revocation is an append to `service_term_action(term_action_id PK, term_id, kind, effective_at, recorded_at, source_ref UNIQUE, replacement_term_id?)`. The original `ends_at` is never rewritten. Under the workspace lock, advance capacity first; operational changes take effect at `max(server_now, watermark_at)`. A provider's earlier event time is evidence, not a backdated change to served history. |
| <a id="rule-tm-05"></a>TM-05 | One capacity offer applies at each instant: select the eligible term with highest pinned `selection_priority`, then `service_term_id` for a stable tie break. Subscription renewals retain their plan generation; an explicitly selected new plan/pass/grant has a new generation. An old delayed webhook cannot override a newer selection. Grace is excluded. When the selected term ends, resolve the remaining eligible set. Rates and bursts are never summed. |
| TM-06 | `capacity_plan_assignment(assignment_id PK, workspace_id, offer_id, term_id, selection_priority, effective_from, effective_to?, cause_ref)` records the non-overlapping resolved timeline. All known term starts/ends/actions are resolution boundaries; lazy advancement first materialises these boundaries under the bucket lock. Only closing a current assignment and appending its successor is permitted. The refill join is assignment.offer_id → policy period at that instant, never the workspace's current offer applied to its whole history. |

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
| Serialisation of racing replicas | The `capacity_bucket` row lock ([RF-02](../16-billing-and-commerce-architecture.md#rule-rf-02)) |
| The one contiguous run, so initialisation happens once | `capacity_bucket.activation_term_id` with [TM-03](#rule-tm-03) ([RF-08](../16-billing-and-commerce-architecture.md#rule-rf-08)) |

**Cross-checks this schema owes the algorithm.** [CX-08](#rule-cx-08) reconciles `held_micro` against live reservations. [CX-11](#rule-cx-11) asserts that no stored `available_micro` was produced by an increase past the bound above — the property the removed `CHECK` was reaching for, expressed where it is actually true.

### `entitlement.capacity_reservation` *(new — [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006))*

| Field | Type | Notes |
|---|---|---|
| `reservation_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` `entitlement.capacity_bucket` |
| `logical_request_id` | `id NN` | `FK →` `commerce.logical_ai_request` |
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

Admission locks all budget keys in stable order, checks `used + held + bound <= limit`, and inserts all reservations in one shared unit of work. A multi-limit operation either reserves all limits or none. Declared upload size and deterministic simulation bounds are conservative admission maxima; server measurement is settlement authority. Concurrency has separate leased slots, not sample/byte units.

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
- **Rule** — this is the **only** table where a provider identifier appears as a key component

### `commerce.offer`, `commerce.price_version`

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

| Field | Type | Notes |
|---|---|---|
| `subscription_id` | `id` | **PK** |
| `billing_account_id` | `id NN` | |
| `workspace_id` | `id NN` | |
| `offer_id`, `price_version_id` | `id NN` | |
| `state` | `enum(trialing, active, pastDue, graceperiod, cancelled, expired) NN` | Derived from `paid_through` and policy |
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

**Cloud commits every row in this schema** (`§4.2` of the overview). Chat and Task are Cloud-authoritative; clients hold read projections plus, for Chat, unsent local drafts.

### `chat.conversation`, `chat.message`

The client schema (`§2` of [`02-desktop-data-model.md`](02-desktop-data-model.md)) mirrors these, not the reverse. **Cloud holds the authoritative acknowledged revision and is its committer** ([AU-01](00-data-model-overview.md#rule-au-01), [CW-02](00-data-model-overview.md#rule-cw-02)); the client copy is a working cache plus unsent drafts.

| # | Rule |
|---|---|
| CH-D1 | **Cloud writes these tables directly.** `chat.appendMessage` commits the user message; the Harness commits the assistant message. A Cloud-originated message requires no device and no client change ([CW-03](00-data-model-overview.md#rule-cw-03)). |
| CH-D2 | **`rev` is assigned by Cloud.** A client's `local_rev` is a device-scoped counter for unsent work and never appears here ([CW-01](00-data-model-overview.md#rule-cw-01)). |
| CH-D3 | **Every commit writes its `sync.change` row in the same transaction** ([CW-06](00-data-model-overview.md#rule-cw-06)), so a message can never exist without being publishable. |
| CH-D4 | **An unsent draft is not a row here.** It lives only on the device that composed it ([I-124](../../requirements/01-normative-glossary-and-invariants.md#rule-i-124)), and is therefore never a competing revision. |
| CH-D5 | A committed Chat message is immutable; edit creates a branch. Stream chunks are presentation, each invocation has immutable `task.iteration_output`, and the terminal Turn publishes a separate final/interrupted message or explicit no-answer outcome. |
| CH-D6 | Stream chunks/state live in the CF RunStream DO with bounded TTL, excluded from PostgreSQL WAL and backup. C# stores only canonical iteration/final content and stream pointers. Restore discards projections and reconciles durable attempts under [CF integration](../contracts/05-cloudflare-integration.md). |

### `task.iteration_output` and terminal references

`iteration_output` has PK output ID, unique `(run_id, iteration_ordinal)`, logical request ID, winning provider-attempt ID, state `complete/interrupted/refused/toolProposals`, immutable typed parts or verified ResourceRef, checksum and created time. Each content part carries the [content origin record](../../requirements/13-data-formats-and-portability.md#content-origin-carriers), bound and committed with its payload before completed output publication; staged marking failure creates no delivered receipt. It is written with the provider outcome/usage receipt before customer settlement. Tool proposal/result parts link durable invocation IDs, and can be read through the authorised Task view without pretending the Turn is terminal. Resource promotion includes Entitlement quota conversion where required.

`task.task` additionally carries `current_iteration`, `current_provider_attempt_id?`, `final_message_id?`, `no_answer_reason?`, and `terminal_output_commit_id?`. Terminal states require exactly one final/interrupted message reference or explicit no-answer reason in the same Chat/Task/Resource/Sync transaction. A provider callback cannot set Task succeeded merely because its own invocation finished. Updating intermediate Task state uses a typed read projection; synchronised aggregate changes still require publication.

### `task.task`

| Field | Type | Notes |
|---|---|---|
| `task_id` | `id` | **PK** |
| `workspace_id` | `id NN` | |
| `owning_product` | `text NN` | Whose **domain** the work concerns. It never transfers, and it does **not** move the authoritative store ([TO-01](00-data-model-overview.md#rule-to-01)) |
| `origin_surface` | `enum(desktop, web, mobile, automation) NN` | Where the request came from. Provenance only — it confers no authority ([TO-03](00-data-model-overview.md#rule-to-03)) |
| `origin_device_id` | `id?` | Present when a device originated it; **null for Web, Mobile and automation** |
| `state` | `enum(created, queued, running, waitingApproval, waitingDevice, waitingCapacity, paused, succeeded, failed, cancelled, unknownEffect) NN` | |
| `reason_facet` | `text?` | *Why* it is in that state ([WP-16.01](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.01)) |
| `intent_summary` | `text NN` | User-facing |
| `created_at`, `updated_at` | `instant NN` | |
| `rev` | `rev NN` | |

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

**Tool locality lives on the Step** ([TK-02](#rule-tk-02)), because one Task mixes cloud and device Steps.

| `plan_step` field | Type | Notes |
|---|---|---|
| `plan_step_id` | `id` | **PK** |
| `run_id` | `id NN` | `FK →`; cascade |
| `step_ordinal` | `int NN` | |
| `capability_key` | `text NN` | Resolved through the generated allowlist ([DP-04](../contracts/02-local-rpc-operations.md#rule-dp-04)) |
| `tool_locality` | `enum(cloud, device) NN` | **Declared, never inferred** ([PL-02](../17-agent-harness.md#rule-pl-02) of the harness) |
| `target_device_id` | `id?` | Required when `tool_locality = 'device'`, else null |
| `state`, `reason_facet` | `text NN`, `text?` | |

- `IX (target_device_id, state)` — **the tool-request pull path**, now correctly on the Step
- **Constraint** — `tool_locality = 'device'` requires `target_device_id IS NOT NULL`; `cloud` requires it to be null
- **Constraint** — a Step declared `device` is **never** satisfied by a cloud substitute ([PL-02](../17-agent-harness.md#rule-pl-02)); if no eligible device is online the Step waits with a stated reason


`run` groups attempts at one task. `plan_step` holds the ordered plan with each step's capability, arguments reference, compensation declaration and approval requirement. `attempt` is the unit of retry:

| `attempt` field | Type | Notes |
|---|---|---|
| `attempt_id` | `id` | **PK** |
| `run_id`, `step_id` | `id NN` | |
| `command_id` | `id NN` | **Reused across retries of the same command** ([BR-02](../../planning/work-packages/16-unified-execution-engine.md#rule-br-02) of [WP-16](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16)) |
| `state` | `enum(pending, running, succeeded, failed, cancelled) NN` | |
| `failure_class` | `enum(transient, permanent, refused, cancelled, unknownEffect)?` | |
| `effect_certainty` | `enum(didNotHappen, happened, unknown)?` | |
| `started_at`, `ended_at` | `instant?` | |

- `UQ (command_id, attempt_ordinal)`
- **Constraint** — an attempt with `effect_certainty = unknown` on a non-idempotent step **must not** auto-retry ([WP-16.02](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.02)); the state machine refuses the transition

### `task.approval`

Durable pending state with `expires_at`, the operation described in user terms, the risk level, and whether local presence is required. **Survives restart of either side** ([WP-14.04](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04)).

### `task.automation_definition` and `automation_occurrence`

`automation_definition` stores stable ID, workspace, immutable definition version, enabled state/revision, trigger kind, UTC schedule with timezone policy or durable event cursor, authorised grant/budget snapshot, misfire/coalescing bounds and next due instant. `automation_occurrence` has unique `(automation_id, definition_version, occurrence_key)`, scheduled time/event identity, admission outcome, Task ID and completion reason. The enumerated automation shared transaction records occurrence, Task, context pins and dispatch outbox together; a leased runner resumes from that receipt after crash. Definition changes invalidate future old-version occurrences, without rewriting past runs. Disable/revoke has an explicit in-flight cancellation policy; neither resets usage nor grants permission.

### `task.tool_request`, `task.tool_result`

The durable bridge (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). A request carries its target device, its payload, its expiry and its delivery state; a result carries the answering attempt and is **idempotent on `(task_id, attempt_id)`** so a re-submitted result has one effect.

### `agent.model_descriptor`, `agent.tariff_version`, `agent.supplier_price_version`

`model_descriptor` and the two price tables are workspace-independent catalogue rows **projected from an activated configuration revision** ([CG-02](../16-billing-and-commerce-architecture.md#rule-cg-02), [DC-05](../../requirements/11-policy-and-configuration.md#rule-dc-05), [DC-06](../../requirements/11-policy-and-configuration.md#rule-dc-06)). They are persisted snapshots, not live lookups into the current file ([I-494](../../requirements/01-normative-glossary-and-invariants.md#rule-i-494)).

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

`spend_budget` has PK `(scope_kind, scope_id, period_key, unit)`, a pinned limit, used, held and revision. Supplier scopes include provider account/route, deployment total and configured workspace sublimit; `unit` is the exact ISO currency. Customer Run scope uses integer micro-credits and its explicit authorised maximum. Supplier decimal quantities use `decimal(28,9)`; no FX or comparison between money and credits is implicit.

`spend_reservation` has a unique `(provider_attempt_id, supplier_budget_key)` for supplier exposure, or `(logical_request_id, run_budget_key)` for the customer ceiling; bound, used, state, lease/deadline and linked reconciliation record. Admission locks every applicable budget row in stable order, verifies all `used + held + bound <= limit` predicates and reserves all or none in the Entitlement/Commerce unit of work. A platform call has supplier reservations and an operator job authority, without a customer capacity reservation. A retry has fresh supplier exposure and shares the logical request's one customer ceiling.

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
| `outcome` | `enum(delivered, providerError, platformError, cancelled, timeout)?` | NULL at intent and while unknown |
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

- `IX (workspace_id, state)`; `IX (state, updated_at)` — the scheduler path
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

The child field shapes for blocks, links, tags and scalar values are shared with [the desktop model](02-desktop-data-model.md#3-arcnotes-local-store). PostgreSQL uses typed columns and `jsonb` for the declared content structures; SQLite uses equivalent explicit SQL and validated JSON. Provider-specific storage types never enter contracts. Notebook/folder placement, revision ownership and the server-side constraints are defined here, not inferred from a local table name.

| # | Rule |
|---|---|
| ND-01 | **Folder structure belongs to the Notebook aggregate.** Creating, renaming, reordering, reparenting or trashing a folder takes the notebook's expected revision and increments it once. Under that root lock, reject cycles, cross-notebook parents and an active child under a trashed ancestor. Sibling order is deterministic by `(ordinal, id)` including root folders; names need not be unique. |
| ND-02 | **Document placement belongs to the Document aggregate.** A move validates the source and destination notebook/folder under sorted notebook locks followed by the document lock. It carries both notebook revisions and the document revision. A cross-notebook move changes placement and emits the removal/addition projections without changing DocumentId, BlockIds or history. An upload, AI edit or import cannot bypass this operation. |
| ND-03 | **Folder trash is a visibility operation, not recursive content deletion.** Descendants remain in place and are hidden by the repository's ancestor-state predicate. Restoring the folder restores that visibility; independently trashed documents stay trashed. Permanent folder removal requires an empty subtree after explicit move or tracked purge; FK RESTRICT enforces it. Notebook deletion uses the tracked deletion lifecycle, never an unbounded cascade in a request handler. |
| ND-04 | **Every accepted content commit stores the current rows, immutable revision, command receipt and publication row in one unit of work.** Resource participants pin attachments and any staged revision body. No network or blob upload occurs while the transaction is open. Conflict rejection preserves the proposed content and does not change current rows. |
| ND-05 | **Read paths have one authority.** Hydration and `sync.getAggregate` reconstruct these canonical rows; local pending data never enters a Cloud export or AI context. History restore creates a new revision. Export freezes a manifest of notebook structure and document revisions, pins their attachments, then renders the Cloud Markdown/attachment/fidelity download from that manifest. It is not a re-importable native Notes package. |
| ND-06 | **Local edits and remote updates share domain validation.** The client catches invalid structure early; Cloud repeats all checks as the final owner. A document's `rev` governs blocks and document metadata. Folder and document operations use explicit typed requests, with bounded bulk operations and per-operation receipts. |
| ND-07 | **All durable payloads are accounted for.** Large revision bodies are staged as verified Resource objects before the Notes commit; that commit promotes them and adds a revision reference. Current content, retained history, conflict branches and active export manifests each pin the objects they need. Garbage collection starts only after the last pin and reader lease ends. |

Required operations: `CreateNotebook`, `UpdateNotebook`, `CreateFolder`, `MoveFolder`, `TrashFolder`, `RestoreFolder`, `MoveDocument`, `GetNotebookTree`, `GetDocumentRevision`, `ListHistory` and `RestoreRevision`, alongside the typed block/property operations. These are Notes application operations reached through local RPC and typed sync proposals; no professional editor is added to Web or Mobile. A batch with a structural dependency submits the parent operation first and binds its acknowledgement before submitting the dependent operation. [WP-18.00](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) owns client/domain semantics; [WP-25.00](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.00) owns the real PostgreSQL counterpart and API integration.

### 8.5 Native-product metadata replicas

`scope.synced_aggregate` and `slate.synced_aggregate` store `(workspace_id, aggregate_kind, aggregate_id)` as PK, server `rev`, schema version, typed canonical metadata payload, source device and source `content_rev`, state/tombstone and timestamps. A generated product-kind allowlist determines the DTO and validation; this is not an executable or arbitrary type-name payload. Immutable replica revisions and Resource references use the same publication and retention rules as Notes.

Cloud accepts these through each owning module's sync adapter. The native SQLite model remains the working authority for hardware/media work. Raw capture and media bodies require their explicit upload policy; proxies and render caches are excluded. Fetching a replica does not assign a native `content_rev`: a local import/reconciliation command commits a new local revision and records which Cloud revision it reconciled. [WP-35.02](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.02) and [WP-39.04](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.04) implement these adapters against the already-delivered sync infrastructure.

---

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

```text
publish(workspace, fence):
    BEGIN
      lock sync.publication_watermark(workspace)
      verify current holder, fence and lease expiry
      select a bounded set of aggregates with unpublished rows,
        rotating after last_aggregate_key (wrap in sorted kind/id order)
      for each selected aggregate:
        read its lowest unpublished aggregate_rev from committed sync.change rows
        assign last_seq + 1 to that row, then advance last_seq
      persist last_aggregate_key, last_seq and assigned rows
    COMMIT
```

Each batch admits at most one revision per selected aggregate; subsequent passes advance busy aggregates fairly. Limits on aggregates, rows and transaction time are configured. Indexes serve the lowest-unpublished query; no unbounded sort/materialisation or scan past a retained history is required.

| # | Rule |
|---|---|
| <a id="rule-pb-01"></a>PB-01 | **Only committed changes are selectable.** A transaction that commits after a previous publication gets a later cursor, even if its UUID sorts earlier. A rollback leaves no change row. |
| PB-02 | **No row can appear later below an already-served cursor.** Assignment and watermark commit atomically; sequence allocation outside this transaction is prohibited. |
| <a id="rule-pb-03"></a>PB-03 | **One validated fence publishes per workspace.** Lease acquisition, renewal and publication lock the same watermark row. A stale fence is rejected before assigning any number. A crashed assignment rolls back both rows and watermark. |
| PB-04 | **Per-aggregate revision order is explicit.** The owner serialises its revision commits and writes each publication row in that commit. The publisher selects the lowest unpublished revision of that aggregate; it never uses UUID or timestamp order as a substitute. |
| PB-05 | **Scheduling is bounded and fair.** A persisted round-robin aggregate key prevents a hot aggregate from starving another; unpublished age and publication lag are monitored. |
| PB-06 | **There is no global business-commit-order or cross-aggregate atomic-observation guarantee.** Clients can split a publication batch across pages. Referential dependencies are resolved by stable identifiers and canonical reads, not by assuming a parent is on the preceding page. |
| PB-07 | **Publication reads immutable change fields after locking the watermark.** Business writers do not lock the watermark. There is no `SKIP LOCKED` claim scan over change rows; the current fence and lowest-unpublished predicate supply the exclusion/order. This is a design algorithm, with PostgreSQL fault-injection evidence still required by [PG-17](../../assurance/open-gates-register.md#rule-pg-17). |

#### 9.2 Bootstrap, application and retention

| # | Rule |
|---|---|
| CU-01 | **A cursor binds workspace, scope/filter generation and `publish_seq`.** It is opaque and authenticated. Changing selective-sync scope requires a new bootstrap; a cursor cannot silently change its filter. |
| CU-02 | **Bootstrap materialises one consistent snapshot with a lower-bound cursor.** Read watermark W on the primary, then establish a REPEATABLE READ snapshot S that sees at least W. Materialise bounded immutable pages plus an explicit manifest under S; do not paginate live aggregate queries across unrelated snapshots. A bounded expiry/retention pin protects W until bootstrap completes. Abort and restart if the build exceeds its time/storage bound. |
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

Acquisition updates holder/expiry and increments the fence under a conditional row lock. Publication rechecks them in its own locked transaction. `last_seq` never decreases. `sync.bootstrap_manifest` records workspace/scope, W, immutable page references, build state, expiry and the retention pin; partial manifests are invisible and their staged objects are swept. This is bounded background work in the existing host.

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

`upload_session` stores `upload_id PK`, workspace, operation/idempotency key, server-issued object key, expected hash, declared maximum bytes, received chunk bitmap with verified chunk lengths, reservation-group ID, state `receiving/verified/promoted/expiring/deleted`, created/expiry times and bounded extension count. Unique `(workspace_id, operation_key)` returns the same session. Oversize/chunk mismatch refuses further upload and enters cleanup. Completion verifies bytes/hash and creates a **Verified** object plus a provisional pin; it does not publish an owner reference. Owner commit enlists Entitlement, Resource and Sync where applicable, promotes to Committed, converts storage quota and pins the object atomically. Duplicate completion/promotion returns the recorded receipt.

Expiry forbids new writes and starts idempotent physical cleanup. The sweeper verifies deletion before releasing staging/storage reservations. An object-store timeout leaves cleanup retryable and exposure held; a bounded deployment staging limit prevents abandoned sessions from exhausting unaccounted storage. Partially received multipart uploads are explicitly aborted through the storage adapter.

---

## 11. `notification`, `policy`, `audit`, `support`, `trustsafety`

| Table | Key points |
|---|---|
| `notification.notification` | Carries **durability class** (`durable` \| `transient`). A durable item persists until resolved regardless of push delivery ([WP-10.04](../../planning/work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.04)). `IX (workspace_id, durability, resolved_at)` |
| `notification.push_registration` | Per device **and** installation; revoked with the device ([PD-01](../11-mobile-architecture.md#rule-pd-01)). `UQ (device_id, installation_id)` |
| `policy.policy_bundle` | Versioned, signed, append-only. Carries `schema_version` and the full validated document. A bundle is applied atomically or not at all ([WP-44.01](../../planning/work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.01)) |
| `policy.rollout_assignment` | *(derived)* — deterministic per installation, so it can be recomputed rather than stored; stored only as a cache with the rule version it came from |
| `audit.audit_event` | **Append-only, no update, no delete** ([AU-01](../13-observability-and-operations.md#rule-au-01)). Carries the full actor chain, the enumerated event type, the reason code and the correlation identifier. `IX (workspace_id, occurred_at)`; `IX (actor_ref, occurred_at)`. Retention exceeds every other window (`§7.1`) |
| `support.support_case` | Links to a **diagnostic reference**, never to content ([WP-45.06](../../planning/work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.06)) |
| `support.access_grant` | Scoped, expiring, consented where required, and **itself audited** ([OP-04](../13-observability-and-operations.md#rule-op-04)). `IX (expires_at)` |
| `trustsafety.enforcement_action` | Records the ladder position, the reason, the communication sent and the appeal state |

---

## 12. Constraints that span modules

These cannot be foreign keys ([AG-01](00-data-model-overview.md#rule-ag-01), [MD-02](../05-cloud-architecture.md#rule-md-02)). Each is an application invariant with a named enforcement point and a data-health check.

| # | Invariant | Enforced at | Detected by |
|---|---|---|---|
| CX-01 | Every `entitlement.grant` with `source = purchase` corresponds to a completed `commerce.order` | Commerce's grant issue call | Reconciliation ([WP-42.08](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.08)) |
| CX-02 | Every `entitlement.capacity_reservation` in `held` belongs to a live `commerce.logical_ai_request` that has not settled | Reservation creation, in the shared unit of work ([SU-01](00-data-model-overview.md#rule-su-01)) | The reservation sweeper ([UU-03](../20-cross-system-lifecycles.md#rule-uu-03) of the cross-system lifecycles) |
| <a id="rule-cx-08"></a>CX-08 | For every workspace, the sum of live `capacity_reservation.from_capacity_micro` equals `capacity_bucket.held_micro`, and the sum of `from_compensation_micro` + `from_purchased_micro` per lot equals that lot's `held_micro` | The shared unit of work ([FU-04](#rule-fu-04)) | Accounting comparison ([WP-42.11](../../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11)) |
| CX-09 | Every customer-benefiting settled `logical_ai_request` has exactly one non-adjusting `customer_settlement`, and at least one `provider_attempt`; **the counts are not required to match** ([FU-03](#rule-fu-03)) | Settlement, in the shared unit of work | Reconciliation ([WP-43.07](../../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07)) |
| CX-10 | Every `sync.change` row with a non-null `publish_seq` has a `publish_seq` less than or equal to its workspace's `publication_watermark.last_seq` | The publisher's transaction ([PB-03](#rule-pb-03)) | Feed integrity check |
| <a id="rule-cx-11"></a>CX-11 | No `capacity_bucket.available_micro` was raised past `max(previous_available, max(0, burst_in_force - held_micro))` by any operation, and a balance sitting above the current ceiling after a reduction is **not** a violation ([RF-05](../16-billing-and-commerce-architecture.md#rule-rf-05) of the commerce architecture) | The bucket update predicate | Capacity accounting check |
| CX-03 | Every `resource.object_reference` referrer exists in its owning module | Reference creation | Orphan detection ([WP-46.04](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.04)) |
| CX-04 | Every `sync.change` names an aggregate that exists or has a tombstone | The applying transaction | Feed integrity check |
| CX-05 | Every `task.tool_request` targets a device that exists and is eligible | Request creation | Presence sweeper |
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

## P2-009 state additions and projection relocation

Implement exact [execution/receipt records](../contracts/05-cloudflare-integration.md#1-deployment-and-authority), late-outcome evidence constraints and object verification receipts. identity.session gains nullable access_token_hash/access_expires_at for nativeBearer, null for browserCookie; unique access hash, native refresh rotation unchanged. Add csrf_hash to session/preauth flow (never plaintext), auth_epoch and recovery_generation checked by every endpoint. Identity owns disjoint operator_session/operator_access/operator_action approval records with tenant/operator subject and proposal hash; only operator scheme can create/read them. Upload sessions retain sealed part manifest, verification job ID/status and immutable part receipts; completeUpload returns verifying while the content is not readable. Resource/Entitlement final verification and owner promotion remain separate commits. DO stream_chunk/state are not PG tables; task.run keeps only stream IDs/status/pointers. No other canonical owner changes.

## Search inference job execution record

Search owns search.inference_job as the canonical business control/receipt record; vectors and reranked candidates remain derived. It is a bounded platform Job, not task.task or a second AI loop. The private [CF inference ports](../contracts/05-cloudflare-integration.md#8-session-bindings-inference-jobs-and-deployment-transitions) carry this identity.

| Fields | Type and invariant |
|---|---|
| job_id; workspace_id; principal_id; service_term_id | id PK and non-null scoped owner/eligibility identities; scheduled indexing uses its explicit operator-job grant for that workspace, never a fabricated interactive session |
| purpose; input_hash; source_manifest_ref; source_set_hash | embedding/rerank; exact hash plus immutable ResourceVersionRef; input hash includes kind, normalized input, ordered source revisions/hashes, principal/scope/policy snapshot, model/profile/config and effective budget |
| model_descriptor_id; config_revision_id; profile | Pinned activated catalogue/config and selected inference profile; no dynamic provider fallback |
| state; reason; rev; created_at; updated_at; deadline | queued/running/unknown/succeeded/failed/cancelled; named reason, monotonic revision and UTC instants. Admission-to-result deadline120 seconds; before-dispatch expiry refuses, possible-dispatch expiry is unknown |
| logical_request_id; provider_attempt_id; intent_receipt | Existing Commerce identities, one bounded invocation per admitted job; beneficiary=platformIndexing, funding_class=platformJob, operator_job_ref=job_id. No customer capacity reservation/tariff/settlement |
| workflow_id; worker_version; recovery_generation; lease_holder; lease_epoch; lease_expires_at | Same deterministic CF ID and observed version as the private contract; conditional60-second claim, renewal20 seconds; old epoch cannot act after takeover/expiry |
| result_ref?; outcome_receipt?; outcome_hash?; source_publication_ref? | Immutable validated result and canonical outcome digest/receipt. succeeded requires complete result; unknown has no claim of completion. Projection delivery receipt records publish/discard under current source/policy; never provider content in Commerce |
| cancellation_requested_at?; completed_at? | Cancellation blocks new dispatch/publication; an already-sent invocation still records supplier facts under the existing uncertainty policy |

Stable job_id comes from the committed Search source/query command, reused on outbox/redelivery. Reusing it with a different input hash is conflict. Unique logical request/attempt references and the outcome hash make receipts idempotent. Model calls never retry merely because a job/lease expired; a proven pre-dispatch refusal may be rescheduled by a new authorized job, and unknown attempts stay in supplier reconciliation. New source/model/config revisions produce new input identities, not edits to old outcomes.

The two enumerated Search families in the [transaction authority](00-data-model-overview.md#611-shared-units-of-work) use each module's own SQL port on one connection; no external CF/R2 call occurs inside the commit. Search is after Task and before Notification in lock order. The dispatch outbox creates/gets the exact Workflow; CF input fetch rechecks current source permissions, active service term and AI-exclusion policy. Source deletion/revocation cancels queued jobs and invalidates derived publication even when a late output is complete.

Record every supplier attempt and keep unresolved exposure through expiry/period closure. A complete result may coexist with costUnconfirmed; it cannot create a customer debit or release conservative liability. Retain accounting identity/receipt under existing commerce retention; source text/result pins use Resource content/deletion policy, never extend user-content retention merely to retain cost evidence. A completed projection consumer releases ephemeral pins; interrupted consumers retry idempotently and rebuild readiness from current authoritative source, never from CF checkpoint data.

## Account state and proof constraints

Identity user/profile and credential rows carry owner revisions; profile/avatar reference changes enlist Resource when required. auth_identity adds realm_id/provider_id and password_hash (password only, no raw secret); provider configuration is versioned and secrets referenced only from the secret store. UQ(workspace.realm_id, owner_user_id) enforces one personal workspace. Initial grants are unique by owner and configured grant identity, not session or installation.

| Identity-owned record | Required fields and constraints |
|---|---|
| spent_refresh | token_hash PK, session_id/family_id FK, generation, consumed_at, family_expires_at; unique family/generation. Retain through family expiry plus the 60-second validation skew. Rotation locks the family, inserts spent hash and replaces current hash atomically. |
| recovery_code | set_id, code_hash PK, user_id, issued_at, consumed_at, invalidated_at; one live set per user, consumption conditional on both code and set remaining active. |
| api_token | token_id PK, user_id, workspace_id, secret_hash unique, name, scopes, created_at, expires_at, last_used_at, revoked_at, rev, auth_epoch, recovery_generation. Receipt persists safe summary only; no reusable plaintext. |
| security_flow | flow_id PK, kind/provider/purpose, user_id if known, installation/device/origin binding, proof_hash, target payload hash, expires_at, attempts, consumed_at; email-change, SSO, enrollment, provider callback and deletion reauth use mutually exclusive typed payloads. Consumption and its owner/session effect share one transaction. |
| session additions | purpose, recovery_generation, auth_epoch, rev; cancelDeletion purpose enforces an API allowlist independent of ordinary ownership. Every family can be revoked through user/device/session indexes. |
| device remote policy | device_id PK/FK, allowed_capabilities, local_confirmation_capabilities, rev; part of Device ownership, not a claim supplied by a heartbeat. |
| workspace data deletion | deletion_id PK, workspace_id, preview_hash, captured_revision, state, owner_job_inventory, completed_at, rev; bounded owner jobs record restartable progress, purge fence and reference release receipts. |

Account proof changes and their Notification outbox are one Identity + Notification shared unit; profile avatar changes additionally enlist Resource/Entitlement. Workspace data deletion uses the existing owner content/reference-release shared family per batch and a Workspace coordinator outbox, never a transaction spanning all content and object storage. Security flow completion that creates a session uses the authentication family. The independently retained safety receipts in deployment architecture fence post-restore reuse and access resurrection.

## Structural move and complete media replica constraints

A Notes cross-notebook move validates one explicit disposition for every used property/tag. Destination properties must have the same scalar type/scale, matching semantic revision, and complete mappings for used select options. Duplicate destination assignments, missing/trashed targets, implicit label matching or numeric conversion refuse. Explicit removal is previewed and retained in immutable history; document/block IDs and original values in old revisions survive. The preview hash binds all participating revisions and mapping. Under the existing sorted locks, commit updates the document placement/classification and source/destination membership publications atomically. Named structural operations retain their typed command payload and results; a generic sync NotesDocument replacement cannot move an existing document.

Slate replicas encode the complete [slate.project.v1 wire projection](../contracts/04-protobuf-wire-registry.md#4-shared-record-field-registry), including every sequence timeline/graph, exact grids, colour/input assignments, bins, markers, text/subtitles, generators/nesting, keyframe scopes and managed small-asset references. Validate identity, referential closure, type/graph/nesting cycles and source contentRev before storing the immutable replica. sequence summaries cannot substitute for timelines. Originals remain opt-in; absent bytes produce Offline Media without losing edit metadata. TranscriptRecord is an immutable derived Resource artifact linked to Task/source revision; adopting it creates ordinary authored native content with retained AI origin, never a server-side rewrite of a Slate project.

## Service object and recovery persistence

Resource service_object_grant stores grant_id PK, owner_kind/job_id, attempt_id?, realm/workspace, epoch, recovery_generation, direction, resource/upload_id, byte_limit, expires_at and revoked_at. It uses the existing upload reservations/verification pins, not a second object lifecycle. Every grant authorization validates its current owner job and fence. Task/Search/Resource keep cf_instance_inventory keyed by kind/instance_id/generation with owner workspace/job, actual worker version and deletion receipt; each module writes only its owned rows and exposes inventory through the deletion coordinator.

platform.safety_receipt records immutable external journal record ID/hash, related owner command/intent ID, generation, kind and pending/verified status. It is a local receipt/cache, never authority over the independent signed journal head. Outbox dispatch cannot pass its external boundary before verified barrier; security denial cannot return durable success before verified fence. platform.recovery_epoch records the installed independent generation, recovery point, journal inventory hash and reopening state. Restored outstanding effects have explicit quarantined/unknown reconciliation records, retaining original identities even when their newer PG outcome was outside the recovery point.
