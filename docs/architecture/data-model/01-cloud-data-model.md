# Cloud Data Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Data model
> Governing authority: [`00-data-model-overview.md`](00-data-model-overview.md), [`../05-cloud-architecture.md`](../05-cloud-architecture.md) `§4`, `§5`
> Companions: [`../16-billing-and-commerce-architecture.md`](../16-billing-and-commerce-architecture.md), [`../08-security-architecture.md`](../08-security-architecture.md)

One PostgreSQL database, one schema per module (`PS-01`). A module owns its schema exclusively: no other module reads or writes its tables, and cross-module reference is by identifier plus a published module API (`MD-02`, `MD-03`).

Notation is defined in [`00-data-model-overview.md`](00-data-model-overview.md) `§2`.

---

## 1. Schema map

| Schema | Module | Aggregate roots |
|---|---|---|
| `identity` | Identity | `user`, `auth_identity`, `session` |
| `workspace` | Workspace | `workspace`, `membership` |
| `device` | Devices | `device`, `installation` |
| `entitlement` | Entitlement | `grant`, `entitlement_snapshot`, `usage_counter` |
| `commerce` | Commerce | `billing_account`, `order`, `subscription`, `credit_lot`, `provider_event` |
| `chat` | Chat | `conversation` |
| `task` | Task | `task`, `automation` |
| `agent` | Agent | `agent_profile`, `model_descriptor`, `tariff_version` |
| `sync` | Sync | `sync_scope`, `change` |
| `resource` | Resource | `cloud_object`, `upload_session` |
| `search` | Search | *(derived — see [`03-derived-stores.md`](03-derived-stores.md))* |
| `notification` | Notification | `notification`, `push_registration` |
| `policy` | Policy | `policy_bundle` |
| `audit` | Audit | `audit_event` |
| `support` | Support | `support_case`, `access_grant` |
| `trustsafety` | TrustSafety | `report`, `enforcement_action` |
| `platform` | shared infrastructure | `outbox`, `inbox`, `command`, `job_lease` |

---

## 2. `platform` — infrastructure tables

These exist once and are used by every module. They are the mechanism behind `TX-01`–`TX-06` and `OB-01`–`OB-05`.

### `platform.command`

| Field | Type | Notes |
|---|---|---|
| `command_id` | `id` | **PK**. Allocated by the caller |
| `workspace_id` | `id?` | `NN` for workspace-scoped operations |
| `actor_ref` | `text NN` | De-identified actor reference |
| `operation` | `text NN` | The operation name, e.g. `chat.appendMessage` |
| `request_hash` | `text NN` | Hash of the canonical request, to detect a reused id with different content |
| `status` | `enum(inProgress, succeeded, failed) NN` | |
| `result_payload` | `json?` | The original response, retained for `TX-04` |
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
| `state` | `enum(ready, leased, succeeded, deadLettered) NN` | |
| `payload` | `json NN` | |
| `available_at` | `instant NN` | Backoff scheduling |

- `IX (state, available_at)` — the only claim path
- **Constraint** — a lease is claimed by a conditional update on `leased_until`, so two workers cannot hold one job

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
- **Constraint** — a `deleted` user retains the row with all personal fields cleared; the identifier is never reused (`ID-05`)

### `identity.auth_identity`

| Field | Type | Notes |
|---|---|---|
| `auth_identity_id` | `id` | **PK** |
| `user_id` | `id NN` | `FK →` `identity.user`; restrict |
| `method` | `enum(passkey, emailCode) NN` | |
| `subject` | `text NN` | Credential identifier — for passkey, the credential id |
| `public_key` | `text?` | Passkey only |
| `sign_count` | `bigint?` | Passkey replay defence |
| `label` | `text?` | User-visible name for the credential |
| `created_at` | `instant NN` | |
| `last_used_at` | `instant?` | |
| `revoked_at` | `instant?` | |

- `UQ (method, subject)` — one credential belongs to one user
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
- **Rule** — email is a **contact and recovery channel, never an identity** (`ID-01` of the commerce architecture). Changing it never changes `user_id` and never affects entitlement.

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
| `refresh_token_hash` | `text NN` | Hash only; never the token |
| `refresh_generation` | `int NN` | Rotation counter — a reused older generation revokes the family |
| `step_up_at` | `instant?` | When step-up was last satisfied |
| `step_up_classes` | `text[]` | Which operation classes the step-up covers |

- `IX (user_id, revoked_at, expires_at)` — active-session listing and mass revocation
- `IX (device_id)` — device revocation cascade
- `UQ (refresh_token_hash)`
- **Constraint** — presenting a superseded `refresh_generation` revokes the entire session family and raises a security audit event. This is the detection mechanism for a stolen refresh token.

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
| `protection_profile` | `enum(standard, enhanced) NN` | |
| `state` | `enum(active, suspended, pendingDeletion) NN` | |
| `created_at` | `instant NN` | |
| `rev` | `rev NN` | |

- `IX (owner_user_id, state)`
- **Constraint** — `data_region` is immutable; moving a workspace between regions is a realm migration operation that creates a new workspace and migrates content (`WP-46.05`), never an update

### `workspace.membership`

| Field | Type | Notes |
|---|---|---|
| `membership_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →`; cascade on purge |
| `user_id` | `id NN` | `FK →`; restrict |
| `role` | `enum(owner) NN` | |
| `created_at` | `instant NN` | |

- `UQ (workspace_id, user_id)`

> **V1 scope.** The implementation repository's `WorkspaceId` documentation states: *"V1 has no organisation membership, team workspace or shared seat. A workspace belongs to one user; it is a boundary, not a collaboration unit."* That matches the accepted scope, where team capability builds a base but does not launch. The table exists with a single role so that adding roles later is an additive migration rather than a structural one — but **no V1 code path creates a second membership**, and a policy test asserts it.

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
| `trust_raised_at` | `instant?` | Requires step-up (`WP-22.03`) |
| `remote_enabled` | `bool NN` | Default **false** |
| `first_seen_at` | `instant NN` | |
| `last_seen_at` | `instant NN` | |
| `revoked_at` | `instant?` | |
| `rev` | `rev NN` | |

- `IX (user_id, revoked_at)`
- **Constraint** — device identity is **not** a hardware fingerprint (`BR-08` of `WP-22`). It is a server-issued identifier the client stores in secure storage and survives ordinary hardware change.
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
- `IX (contract_set_version)` — the minimum-version rollout query (`UP-11`)

### `device.presence`

| Field | Type | Notes |
|---|---|---|
| `device_id` | `id` | **PK**, `FK →`; cascade |
| `connection_state` | `enum(connected, disconnected) NN` | |
| `last_heartbeat_at` | `instant NN` | |
| `stale_after` | `instant NN` | |
| `eligible_for_remote` | `bool NN` | *(derived)* from trust, remote_enabled and connection |

- `IX (eligible_for_remote, stale_after)` — target selection for remote work
- **Constraint** — presence is never inferred from a valid session (`WP-26.00`). A row past `stale_after` reports disconnected regardless of `connection_state`.

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
| `source` | `enum(purchase, administrative, promotional, trial, store, free) NN` | **No provider identifier appears here** (`EO-04`) |
| `source_ref` | `text?` | An opaque reference the issuing module understands |
| `effective_from` | `instant NN` | |
| `effective_until` | `instant?` | Null = open-ended |
| `issued_by_actor` | `text NN` | For administrative grants, the operator |
| `created_at` | `instant NN` | |

- **Append-only.** No update, no delete (`EN-01` of the commerce architecture)
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

*(derived — always rebuildable from grants and revocations, `EN-02`)*

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | `id` | **PK** |
| `entitlement_version` | `bigint NN` | Increments on every change; clients compare this |
| `computed_at` | `instant NN` | |
| `valid_until` | `instant?` | The next time-based transition, so the resolver knows when to recompute |
| `capabilities` | `json NN` | Capability → `{granted, reason, sourceGrantId}` |
| `quotas` | `json NN` | Quota key → `{limit, reason, sourceGrantId}` |
| `features` | `json NN` | |

- **Constraint** — a rebuild must equal the stored snapshot for every fixture account (`WP-42.04`). A difference is a defect, not a refresh.
- **Rule** — `valid_until` exists so the resolver is deterministic without a clock scan: the sweeper recomputes exactly the workspaces whose `valid_until` has passed.

### `entitlement.usage_counter`

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | `id` | **PK part 1** |
| `quota_key` | `text NN` | **PK part 2** |
| `period_start` | `instant NN` | **PK part 3** — tied to the entitlement period, not the calendar |
| `used` | `bigint NN` | |
| `updated_at` | `instant NN` | |

- **Constraint** — the period boundary comes from the entitlement snapshot, never from a calendar convenience (`QA-02`)
- **Constraint** — storage usage is computed from **committed** objects (`QA-03`), so this counter is a materialised aggregate over `resource.cloud_object`, reconciled by a data-health check rather than incremented optimistically

---

## 7. `commerce`

### `commerce.billing_account`

| Field | Type | Notes |
|---|---|---|
| `billing_account_id` | `id` | **PK** — the stable internal buyer identity (`ID-01`) |
| `owner_user_id` | `id NN` | |
| `created_at` | `instant NN` | |
| `rev` | `rev NN` | |

- **Rule** — **never keyed by email.** A payment email such as a shared finance mailbox must not determine ownership.

### `commerce.provider_customer`

| Field | Type | Notes |
|---|---|---|
| `billing_account_id` | `id` | **PK part 1** |
| `provider` | `text NN` | **PK part 2** |
| `external_customer_ref` | `text NN` | The provider's identifier, held as an external reference (`MB-03`) |

- `UQ (provider, external_customer_ref)`
- **Rule** — this is the **only** table where a provider identifier appears as a key component

### `commerce.offer`, `commerce.price_version`

Workspace-independent catalogue rows (`MT-04`). An `offer` names what is sold; a `price_version` carries the amounts, currency, effective dates and tax category. **A price change creates a new `price_version`; existing orders retain the version they were bought under** (`PC-01`), so `order.price_version_id` is a restrict-delete foreign key and a price version is never mutated.

### `commerce.purchase_intent`

| Field | Type | Notes |
|---|---|---|
| `purchase_intent_id` | `id` | **PK** — the idempotency anchor for the whole chain (`PU-03`) |
| `billing_account_id` | `id NN` | `FK →`; restrict |
| `workspace_id` | `id NN` | Entitlement target |
| `offer_id` | `id NN` | |
| `price_version_id` | `id NN` | |
| `state` | `enum(open, checkoutStarted, completed, expired, abandoned) NN` | |
| `created_at` | `instant NN` | |
| `expires_at` | `instant NN` | |

- `UQ (purchase_intent_id)`; `IX (state, expires_at)` — the expiry sweeper
- **Constraint** — at most one `checkout_attempt` in a non-terminal state per intent, enforced by a partial unique index. This is what makes `PU-02` true.

### `commerce.checkout_attempt`

Carries the internal metadata sent to the provider (`ID-04`): billing account, workspace, offer, price version, attempt and intent identifiers. Holds the provider's session reference and its own expiry. **A success redirect writes nothing here** (`PU-01`) — only a verified provider event advances state.

### `commerce.provider_event`

| Field | Type | Notes |
|---|---|---|
| `provider_event_id` | `id` | **PK** |
| `provider` | `text NN` | |
| `external_event_id` | `text NN` | |
| `event_type` | `text NN` | |
| `raw_payload` | `json NN` | Retained for dispute evidence and replay (`EI-08`) |
| `signature_verified` | `bool NN` | |
| `received_at` | `instant NN` | |
| `processing_state` | `enum(received, processed, quarantined) NN` | |
| `retry_count` | `int NN` | |
| `quarantine_reason` | `text?` | |

- `UQ (provider, event_type, external_event_id)` — **this composite key is the idempotency of `EI-02`**
- `IX (processing_state, received_at)` — backlog age, a page-worthy alert (`AL-02`)
- **Constraint** — the row is written **before** processing (`EI-01`). An unverified event is stored with `signature_verified = false` and rejected, never processed.

### `commerce.order`, `commerce.payment`, `commerce.subscription`

`order` links intent → offer → price version → billing account, and is append-only after completion. `payment` records each provider payment with its external reference, amount as `money`, and state. `subscription` carries the **normalised** state driven by `paid_through` (`EN-05`), not by a provider status string:

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

### `commerce.credit_lot`, `commerce.credit_reservation`, `commerce.credit_transaction`

| `credit_lot` field | Type | Notes |
|---|---|---|
| `credit_lot_id` | `id` | **PK** |
| `workspace_id` | `id NN` | |
| `lot_class` | `enum(subscriptionAllowance, purchased, promotional) NN` | Three classes, three rule sets (`CD-02`) |
| `original_amount` | `money NN` | Fixed-precision (`BC-06`) |
| `remaining_amount` | `money NN` | |
| `expires_at` | `instant?` | |
| `refund_hold` | `bool NN` | Freezes the lot during adjudication (`CS-07`) |
| `source_ref` | `text?` | Order or grant reference |
| `created_at` | `instant NN` | |

- `IX (workspace_id, refund_hold, expires_at)` — **the consumption-order query**: earliest-expiry-first within class priority (`CD-03`)
- **Constraint** — `remaining_amount ≥ 0`, enforced by a check constraint. This is what makes "no overdraft" structural rather than procedural (`CS-06`).

| `credit_reservation` field | Type | Notes |
|---|---|---|
| `reservation_id` | `id` | **PK** |
| `workspace_id`, `attempt_id` | `id NN` | |
| `amount` | `money NN` | |
| `state` | `enum(held, settled, released, expired) NN` | |
| `expires_at` | `instant NN` | Sweeper releases orphans (`CS-04`) |

- `UQ (attempt_id)` where state is non-terminal — **one live reservation per attempt**, which is what prevents double-charging on retry
- `IX (state, expires_at)`

`credit_transaction` is the append-only movement log: reservation, settlement, release, expiry, refund. Every row names its lot, its reservation where applicable, its signed amount and its reason.

### `commerce.ledger_entry`

Three ledgers, one table, discriminated and **never joined across the discriminator** (`LG-01`, `LG-03`):

| Field | Type | Notes |
|---|---|---|
| `ledger_entry_id` | `id` | **PK** |
| `ledger` | `enum(providerCost, customerCredit, paymentRevenue) NN` | |
| `workspace_id` | `id?` | Null for provider-cost rows that are not workspace-attributable |
| `amount` | `money NN` | Signed |
| `occurred_at` | `instant NN` | |
| `reference_kind`, `reference_id` | `text NN`, `id NN` | What the entry is about |
| `created_at` | `instant NN` | |

- **Append-only.** A correction is a new entry (`BC-05`)
- `IX (ledger, occurred_at)`; `IX (ledger, workspace_id, occurred_at)`
- **Constraint** — a policy test asserts no query joins two `ledger` values

---

## 8. `chat`, `task`, `agent`

These hold the **cloud replica** of locally authoritative data (`§4` of the overview), plus genuinely cloud-owned execution state.

### `chat.conversation`, `chat.message`

Mirror the local model (`§2` of [`02-desktop-data-model.md`](02-desktop-data-model.md)) with `workspace_id`, `rev`, sync state and a tombstone flag. **Cloud is a replica, not the authority** — a cloud-side edit is impossible; the only writer is the sync engine applying a client change.

### `task.task`

| Field | Type | Notes |
|---|---|---|
| `task_id` | `id` | **PK** |
| `workspace_id` | `id NN` | |
| `owning_product` | `text NN` | Never transfers (`TO-01`) |
| `placement` | `enum(local, cloud, remoteViaBridge) NN` | Decided once (`TO-06`) |
| `authoritative_store` | `enum(cloud, device) NN` | *(derived from placement)* |
| `origin_device_id` | `id?` | |
| `target_device_id` | `id?` | For `remoteViaBridge` |
| `state` | `enum(created, queued, running, waitingApproval, waitingBudget, paused, succeeded, failed, cancelled, unknownEffect) NN` | |
| `reason_facet` | `text?` | *Why* it is in that state (`WP-16.01`) |
| `intent_summary` | `text NN` | User-facing |
| `created_at`, `updated_at` | `instant NN` | |
| `rev` | `rev NN` | |

- `IX (workspace_id, state, updated_at)` — the task centre
- `IX (target_device_id, state)` — the tool-request pull path
- **Constraint** — a task with `placement = local` must have `authoritative_store = device`; a check constraint enforces it, so `TO-07` cannot be violated by a code path

### `task.run`, `task.plan_step`, `task.attempt`

`run` groups attempts at one task. `plan_step` holds the ordered plan with each step's capability, arguments reference, compensation declaration and approval requirement. `attempt` is the unit of retry:

| `attempt` field | Type | Notes |
|---|---|---|
| `attempt_id` | `id` | **PK** |
| `run_id`, `step_id` | `id NN` | |
| `command_id` | `id NN` | **Reused across retries of the same command** (`BR-02` of `WP-16`) |
| `state` | `enum(pending, running, succeeded, failed, cancelled) NN` | |
| `failure_class` | `enum(transient, permanent, refused, cancelled, unknownEffect)?` | |
| `effect_certainty` | `enum(didNotHappen, happened, unknown)?` | |
| `started_at`, `ended_at` | `instant?` | |

- `UQ (command_id, attempt_ordinal)`
- **Constraint** — an attempt with `effect_certainty = unknown` on a non-idempotent step **must not** auto-retry (`WP-16.02`); the state machine refuses the transition

### `task.approval`

Durable pending state with `expires_at`, the operation described in user terms, the risk level, and whether local presence is required. **Survives restart of either side** (`WP-14.04`).

### `task.tool_request`, `task.tool_result`

The durable bridge (**D-010**). A request carries its target device, its payload, its expiry and its delivery state; a result carries the answering attempt and is **idempotent on `(task_id, attempt_id)`** so a re-submitted result has one effect.

### `agent.model_descriptor`, `agent.tariff_version`, `agent.provider_interaction`

`model_descriptor` and `tariff_version` are workspace-independent catalogue rows. `tariff_version` is **append-only with effective dates**, and every run stores the `tariff_version_id` it locked at start (`CS-08`), which is what makes a historical charge explainable. `provider_interaction` is a **separate trace store** (`§4` of the observability architecture) carrying provider request identifier, token and media unit counts, duration and result — **never prompt or response content**.

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
| `content_exclusions` | `json NN` | **Expressive enough for `I-474`** — raw capture excluded by default |
| `rev` | `rev NN` | |

- `UQ (workspace_id, product_id, scope_kind, scope_ref)`

### `sync.change`

The change feed. One row per aggregate revision that entered the cloud replica.

| Field | Type | Notes |
|---|---|---|
| `change_seq` | `bigint` | **PK** — monotonic per workspace, allocated by a sequence |
| `workspace_id` | `id NN` | |
| `aggregate_kind` | `text NN` | |
| `aggregate_id` | `id NN` | |
| `aggregate_rev` | `rev NN` | |
| `change_kind` | `enum(upsert, tombstone) NN` | |
| `origin_device_id` | `id NN` | So a device can skip its own echo |
| `occurred_at` | `instant NN` | |

- `IX (workspace_id, change_seq)` — **the only feed query path**, and the cursor is `(workspace_id, change_seq)`
- **Constraint** — `change_seq` is allocated **inside** the applying transaction, so the feed can never show a gap that is not a real gap

### `sync.tombstone`

| Field | Type | Notes |
|---|---|---|
| `aggregate_kind`, `aggregate_id` | **PK** | |
| `workspace_id` | `id NN` | |
| `deleted_at` | `instant NN` | |
| `deleted_by_device_id` | `id?` | |
| `retain_until` | `instant NN` | `§7.1` of the overview |

- `IX (retain_until)` — the purge sweeper
- **Constraint** — a device whose cursor predates the oldest retained tombstone **must** full-resync; the feed returns `sync.cursor_expired` rather than a silently incomplete delta (`WP-25.02`)

### `sync.conflict`

Records a detected conflict, the policy applied, and — where a policy discarded a version — **a reference to the retained discarded version** (`WP-25.03`). A discarded version is never destroyed.

---

## 10. `resource`

### `resource.cloud_object`

| Field | Type | Notes |
|---|---|---|
| `cloud_object_id` | `id` | **PK** |
| `workspace_id` | `id NN` | |
| `owner_product` | `text NN` | |
| `content_hash` | `text NN` | Content address |
| `size_bytes` | `bigint NN` | |
| `content_type` | `text?` | |
| `sensitivity` | `enum(public, internal, confidential, restricted) NN` | |
| `state` | `enum(staged, verified, committed, releasing, deleted) NN` | The lifecycle of `§7` of the sync architecture |
| `storage_key` | `text NN` | **Server-issued**; a client never chooses it (`BR-10` of `WP-23`) |
| `reference_count` | `int NN` | |
| `last_reference_released_at` | `instant?` | Starts the grace period |
| `created_at` | `instant NN` | |

- `IX (workspace_id, state)`; `IX (content_hash)` — deduplication; `IX (state, last_reference_released_at)` — the garbage collector's only path
- **Constraint** — `reference_count ≥ 0`, and a reference is only published when `state = committed` (`XS-05`)
- **Constraint** — storage accounting sums `size_bytes` over `state = committed` only (`QA-03`)

### `resource.object_reference`

| Field | Type | Notes |
|---|---|---|
| `cloud_object_id` | `id NN` | **PK part 1** |
| `referrer_kind`, `referrer_id` | `text NN`, `id NN` | **PK parts 2, 3** |
| `created_at` | `instant NN` | |

- The reference count is **derived from this table**, not incremented independently — which is what makes a crash mid-operation recoverable (`WP-07.04`)

### `resource.upload_session`

Chunked upload state with the expected hash, received chunk bitmap, expiry and an idempotent completion. **Resumable** (`WP-23.04`).

---

## 11. `notification`, `policy`, `audit`, `support`, `trustsafety`

| Table | Key points |
|---|---|
| `notification.notification` | Carries **durability class** (`durable` \| `transient`). A durable item persists until resolved regardless of push delivery (`WP-10.04`). `IX (workspace_id, durability, resolved_at)` |
| `notification.push_registration` | Per device **and** installation; revoked with the device (`PD-01`). `UQ (device_id, installation_id)` |
| `policy.policy_bundle` | Versioned, signed, append-only. Carries `schema_version` and the full validated document. A bundle is applied atomically or not at all (`WP-44.01`) |
| `policy.rollout_assignment` | *(derived)* — deterministic per installation, so it can be recomputed rather than stored; stored only as a cache with the rule version it came from |
| `audit.audit_event` | **Append-only, no update, no delete** (`AU-01`). Carries the full actor chain, the enumerated event type, the reason code and the correlation identifier. `IX (workspace_id, occurred_at)`; `IX (actor_ref, occurred_at)`. Retention exceeds every other window (`§7.1`) |
| `support.support_case` | Links to a **diagnostic reference**, never to content (`WP-45.06`) |
| `support.access_grant` | Scoped, expiring, consented where required, and **itself audited** (`OP-04`). `IX (expires_at)` |
| `trustsafety.enforcement_action` | Records the ladder position, the reason, the communication sent and the appeal state |

---

## 12. Constraints that span modules

These cannot be foreign keys (`AG-01`, `MD-02`). Each is an application invariant with a named enforcement point and a data-health check.

| # | Invariant | Enforced at | Detected by |
|---|---|---|---|
| CX-01 | Every `entitlement.grant` with `source = purchase` corresponds to a completed `commerce.order` | Commerce's grant issue call | Reconciliation (`WP-42.08`) |
| CX-02 | Every `commerce.credit_reservation` in `held` belongs to a live `task.attempt` | Reservation creation | The reservation sweeper (`CS-04`) |
| CX-03 | Every `resource.object_reference` referrer exists in its owning module | Reference creation | Orphan detection (`WP-46.04`) |
| CX-04 | Every `sync.change` names an aggregate that exists or has a tombstone | The applying transaction | Feed integrity check |
| CX-05 | Every `task.tool_request` targets a device that exists and is eligible | Request creation | Presence sweeper |
| CX-06 | Every `identity.session` names a live, unrevoked device | Session issue | Device revocation cascade |
| CX-07 | `entitlement.usage_counter` for storage equals the committed sum in `resource` | — *(materialised)* | Accounting comparison (`WP-42.06`) |

---

## 13. Verification

| # | Obligation | Where |
|---|---|---|
| CV-01 | Every table round-trips every field, including nullability and enum boundaries | `WP-21.03` |
| CV-02 | Every declared index exists and serves its named path at scale-corpus size | `WP-21.03` |
| CV-03 | Every check constraint refuses its negative case — negative credit, orphan reference, mismatched placement | `WP-21.02` |
| CV-04 | The `platform.command` reuse constraint refuses a reused id with different content | `WP-23.03` |
| CV-05 | The `provider_event` composite key makes duplicate delivery a no-op | `WP-42.03` |
| CV-06 | A cross-workspace read fails at the data layer with a forged scope | `WP-21.06` |
| CV-07 | Every cross-module invariant in `§12` has a detection check that fires on an induced violation | `WP-46.04` |
| CV-08 | Entitlement resolves correctly with the entire `commerce` schema absent (`EO-05`) | `WP-42.00` |
