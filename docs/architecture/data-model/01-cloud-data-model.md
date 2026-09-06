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
| `workspace` | Workspace | `workspace` — **no membership table** (`WO-01`) |
| `device` | Devices | `device`, `installation` |
| `entitlement` | Entitlement | `grant`, `entitlement_snapshot`, `usage_counter`, `service_term`, `capacity_bucket`, `capacity_policy_period`, `capacity_reservation` |
| `commerce` | Commerce | `billing_account`, `order`, `subscription`, `credit_lot`, `provider_event`, `logical_ai_request`, `provider_attempt`, `attempt_usage`, `supplier_cost_entry`, `customer_settlement` |
| `chat` | Chat | `conversation`, `message`; plus the **transient** `stream_chunk`/`stream_state` (`§7.1` of the harness) |
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

### Workspace ownership — no membership table

**P2-006 excludes organisations, membership, invitations, collaborative editing and collaboration-only schema hooks.** The `workspace.membership` table of the previous baseline was exactly such a hook: one row per workspace, one role value, no V1 writer. It is **removed**, not retained empty.

| # | Rule |
|---|---|
| WO-01 | **Ownership is `workspace.owner_user_id`**, a single non-null column. There is no join table, no role column and no seat concept. |
| WO-02 | **Authorization is `Actor → owns → Workspace → Resource`.** The previous `Actor → Membership → Workspace → Resource` chain collapses to a direct ownership check (`MT-02` of the cloud architecture is amended accordingly). |
| WO-03 | **A workspace is a multi-device boundary, not a collaboration unit.** Several devices of one owner share it; no second principal ever holds rights in it. |
| WO-04 | **Re-introducing membership is an architecture baseline change**, not an additive migration. Retaining a dormant table would have made it look like a configuration switch, which is precisely the ambiguity P2-006 removes. |
| WO-05 | **A repository policy test asserts no schema, contract or operation carries a membership, role, invitation, seat or shared-editor concept** (`WP-05`). |

> **Retired identifier.** `workspace.membership` is retired by P2-006 and is not reused for another purpose. Its historical definition is in the git history of this document at `7ed79a6`.

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


### `entitlement.service_term` *(new — P2-006; keys corrected 2026-09-07)*

The gate before every AI decision (`§5.3` of the commerce architecture). An interval, never a flag.

> **Corrected 2026-09-07.** The previous definition set `source_ref` to the subscription id under `UQ (kind, source_ref)`. That made **renewal impossible**: the second paid period of the same subscription would collide on the key. Three identities were conflated, and are now separate.

| Identity | Meaning | Lives in |
|---|---|---|
| **Subscription identity** | The provider's long-lived subscription | `subscription_ref` |
| **Paid-period identity** | *One* paid interval of it | `period_ref` — the key |
| **Provider-event identity** | The webhook that caused this row | `commerce.provider_event`, deduplicated there (`EI-02`) |

| Field | Type | Notes |
|---|---|---|
| `service_term_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` `workspace.workspace`; restrict |
| `realm_id` | `id NN` | **Realm-scoped**; a term is never visible outside its realm (`SV-04`) |
| `kind` | `enum(subscription, pass, compensation, selfHostGrant) NN` | The only four sources (`SV-02`) |
| `subscription_ref` | `text?` | The provider subscription, for `kind = subscription`. **Stable across renewals** |
| `period_ref` | `text NN` | **The paid period's own identity** — the provider's invoice or billing-period id for a subscription; the order id for a pass; the grant id for a compensation or self-host term |
| `starts_at` | `instant NN` | |
| `ends_at` | `instant NN` | Exclusive |
| `grace_ends_at` | `instant?` | Data-access grace; **never extends AI admission** (`SV-05`) |
| `supersedes_id` | `id?` | `FK →` self. Set when this row replaces an earlier period on plan change |
| `created_at` | `instant NN` | |

- `UQ (kind, period_ref)` — **idempotent creation per period.** A replayed provider event for the same period creates nothing; a genuine renewal carries a **new** `period_ref` and creates a new row (`SV-02`)
- `IX (workspace_id, starts_at, ends_at)` — the admission-path query
- `IX (subscription_ref, starts_at)` — the renewal-chain query
- **Constraint** — `ends_at > starts_at`
- **Constraint** — `kind = 'subscription'` requires `subscription_ref IS NOT NULL`; the other kinds require it to be `NULL`
- **Constraint** — no row is created from a credit grant, a trial flag or an operator balance edit (`SV-03`), enforced by the grant interface

| # | Rule |
|---|---|
| TM-01 | **The effective term is the union of overlapping and abutting intervals** (`SV-01`). Contiguous renewal therefore extends eligibility with no gap, while remaining a separate row with its own period identity. |
| TM-02 | **Deduplication is by provider event, not by term row.** `commerce.provider_event` already deduplicates on `(eventType, eventId)` (`EI-02`); the term's own key only prevents two rows for one *period*. Conflating the two was the original defect. |
| TM-03 | **Contiguity is computed, not stored.** Two terms are contiguous when `previous.ends_at >= next.starts_at`. A gap between them means capacity accrued nothing in between (`RF-01`) and the next term is a **new activation** for `RF-07`. |
| TM-04 | **A plan change mid-period supersedes rather than edits.** The new row carries `supersedes_id`, and the superseded row's `ends_at` is set to the change instant. History stays append-only, and the union rule keeps eligibility continuous. |
| TM-05 | **A revocation — refund or chargeback — is recorded as a revocation against the term** (`RE-05` of the commerce architecture), not by deleting the row. Access ends at the revocation's effective time; the record of what was granted survives. |

### `entitlement.capacity_bucket` *(new — P2-006; refill corrected 2026-09-07)*

One row per workspace. The replenishing included-capacity bucket (`§7.2` of the commerce architecture).

> **Corrected 2026-09-07.** The previous definition stored `burst_micro` and `rate_micro_per_second` **on the bucket row**, and refill multiplied the whole elapsed interval by that single rate. That is wrong whenever the configured rate changed inside the interval: five seconds at rate 1 followed by five seconds at rate 10 earns **55**, not 100. Rate and burst now come from **immutable policy history**, and refill integrates over the intervals actually in force.

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | `id` | **PK** — exactly one bucket per workspace |
| `available_micro` | `int64 NN` | Integer micro-credits (`CD-01`). **Never a float** |
| `held_micro` | `int64 NN` | Sum of live reservations funded from capacity (`CX-08`) |
| `remainder_num`, `remainder_den` | `int64 NN` | **Exact fractional carry** as a rational (`RF-03`). Never a float, never truncated |
| `watermark_at` | `instant NN` | **Monotonic** (`RF-02`); advanced, never rewound |
| `activation_term_id` | `id?` | `FK →` `entitlement.service_term` — the term that opened the **current contiguous run** (`RF-07`, `TM-03`) |
| `rev` | `rev NN` | |

- **Constraint** — `available_micro >= 0`, `held_micro >= 0`
- **Constraint** — `available_micro <= GREATEST(0, burst_at(now) - held_micro)` (`RF-04`), evaluated on every mutation
- **Constraint** — `watermark_at` is non-decreasing, enforced by a checked update predicate (`RF-02`)
- **Rule** — burst and rate are **not columns here.** They are read from `entitlement.capacity_policy_period`, so a configuration change cannot silently rewrite a bucket's parameters or its history

### `entitlement.capacity_policy_period` *(new — 2026-09-07)*

Immutable policy history. One row per `(realm, offer, activation interval)` in which the capacity parameters were constant.

| Field | Type | Notes |
|---|---|---|
| `policy_period_id` | `id` | **PK** |
| `realm_id`, `offer_id` | `id NN` | |
| `config_revision_id` | `id NN` | `FK →` `config.revision` — which activated revision supplied these values (`CG-02`) |
| `burst_micro` | `int64 NN` | |
| `rate_micro_per_second` | `int64 NN` | |
| `effective_from` | `instant NN` | The activation instant of that revision |
| `effective_to` | `instant?` | NULL while current; set when the next revision activates |

- `UQ (realm_id, offer_id, effective_from)`
- `IX (realm_id, offer_id, effective_from, effective_to)` — the integration query
- **Constraint** — a row is **never updated except to close `effective_to`**, and never deleted (`I-494`)
- **Constraint** — periods for one `(realm, offer)` are contiguous and non-overlapping; closing one and opening the next happens in the **activation transaction** (`CA-03`), so no instant is uncovered or double-covered

#### The refill calculation

Refill runs on read, under the bucket row's lock, and **integrates over the intersection of three interval sets**: elapsed time, eligible paid service, and policy periods.

```
refill(bucket, now):
    LOCK bucket row                                   -- serialises racing replicas (RF-02)
    if now <= bucket.watermark_at:                    -- clock rollback, or already current
        return                                        -- never rewind (RF-02)

    windows = intersect(
        [bucket.watermark_at, now),
        eligible_service_intervals(workspace),        -- union of service terms (TM-01)
        policy_periods(realm, offer))                 -- immutable history

    earned = bucket.remainder_as_rational
    for w in windows in chronological order:          -- SPLIT AT EVERY BOUNDARY
        earned += duration_seconds(w) * w.rate_micro_per_second

    whole = floor(earned)
    bucket.remainder = earned - whole                 -- exact rational carry (RF-03)

    ceiling = max(0, burst_at(now) - bucket.held_micro)
    bucket.available_micro = min(bucket.available_micro + whole, ceiling)
    bucket.watermark_at = now
```

| # | Rule |
|---|---|
| RF-01 | **Recovery accrues only over the intersection of elapsed time, eligible paid intervals and policy periods.** A lapse contributes zero; an inactive period is simply absent from the window set (`AC-02`, `AC-03`). |
| RF-02 | **The watermark advances monotonically and is durable** (`AC-12`). Reconnect, restart, another device, another replica or a clock rollback cannot rewind it or refill the bucket. Racing replicas serialise on the row lock. |
| RF-03 | **The fractional remainder is carried as an exact rational**, not a scaled integer and never a float. Rate changes make the carry's natural denominator vary, and a fixed scale would round at every boundary — turning a rate change into a small permanent gift or loss. |
| RF-04 | **The ceiling uses the burst in force *now*** (`burst_at(now)`), and counts held capacity: `available <= max(0, burst - held)` (`AC-11`). A burst *reduction* therefore stops accrual immediately and lets existing balance drain; it never claws back what was already earned, and never releases a hold. |
| RF-05 | **Returned capacity is capped by the same ceiling.** Releasing a hold or issuing a refund must never mint spendable capacity above the burst (`AC-11`). |
| RF-06 | **Purchased credits never refill** (`AC-11`). No code path adds to a lot except a purchase, a compensation grant or an adjustment. |
| RF-07 | **Initialisation happens once per contiguous run**, not once per term. `activation_term_id` names the term that opened the current run; a **contiguous** renewal (`TM-03`) leaves it unchanged and does **not** refill to full (`AC-03`), while a term starting after a gap sets it and initialises once, idempotently. |
| RF-08 | **A configuration activation does not itself move capacity.** It closes one `capacity_policy_period` and opens the next inside the activation transaction (`CA-03`); the next refill for each workspace integrates across the boundary. No bucket is touched at activation, so activation cost is independent of workspace count and **no capacity is reset, released or minted** (`DC-13`). |
| RF-09 | **A hold outstanding across a rate change is unaffected.** Holds are micro-credit amounts already reserved; only accrual is rate-dependent. |
| RF-10 | **Restart is invisible.** Nothing is cached in memory: the watermark, the remainder and the policy periods are all durable, so a refill after restart produces exactly the value it would have produced without one. |

### `entitlement.capacity_reservation` *(new — P2-006)*

| Field | Type | Notes |
|---|---|---|
| `reservation_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` `entitlement.capacity_bucket` |
| `logical_request_id` | `id NN` | `FK →` `commerce.logical_ai_request` |
| `from_capacity_micro` | `int64 NN` | Portion held against the bucket |
| `from_compensation_micro` | `int64 NN` | Portion held against compensation lots |
| `from_purchased_micro` | `int64 NN` | Portion held against purchased lots — **non-zero only under an extra-usage authorisation** (`AD-05`) |
| `state` | `enum(held, settled, released, expired) NN` | |
| `expires_at` | `instant NN` | Swept when passed (`CS-04`) |
| `created_at` | `instant NN` | |

- `IX (workspace_id, state)`, `IX (state, expires_at)` — the sweeper path
- **Constraint** — the three source columns record the allocation, and settlement debits and releases **against the same sources** (`CD-06`, `ST-05`)
- **Constraint** — a `from_purchased_micro > 0` row requires a live extra-usage authorisation reference
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

### `commerce.credit_lot`, `commerce.credit_transaction`

> **Unified 2026-09-07.** The previous definition carried the pre-P2-006 model: a `subscriptionAllowance` lot class, `money`-typed customer balances, and a `credit_reservation` table keyed on `attempt_id`. All three are superseded. **Included capacity is a bucket, not a lot** (`CD-02`); customer amounts are **integer micro-credits**, not money (`CD-01`, `MT-07`); and reservation is per **logical request**, not per attempt (`§7.3` of the commerce architecture). `commerce.credit_reservation` is **retired**; `entitlement.capacity_reservation` is the single reservation table for both funding pools.

| `credit_lot` field | Type | Notes |
|---|---|---|
| `credit_lot_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` |
| `lot_class` | `enum(purchased, compensation) NN` | **Two classes.** `subscriptionAllowance` is retired — that pool is `entitlement.capacity_bucket` |
| `original_micro` | `int64 NN` | **Integer micro-credits** (`CD-01`). Never `money`, never a float |
| `remaining_micro` | `int64 NN` | |
| `held_micro` | `int64 NN` | Sum of live reservations funded from this lot |
| `expires_at` | `instant?` | **NULL for `purchased`** — purchased credits do not expire with time or cancellation (`CD-03`). Required for `compensation` (`CD-04`) |
| `refund_hold` | `bool NN` | Freezes the lot during adjudication (`CS-07`) |
| `source_ref` | `text?` | Order or compensation-grant reference |
| `created_at` | `instant NN` | |

- `IX (workspace_id, lot_class, refund_hold, expires_at, created_at)` — **the funding-order query**: compensation earliest-expiry-first, then purchased oldest-acquisition-first (`CD-05`)
- **Constraint** — `remaining_micro >= 0` and `held_micro >= 0` and `held_micro <= remaining_micro`. This is what makes "no overdraft" structural (`CR-23`)
- **Constraint** — `lot_class = 'purchased'` requires `expires_at IS NULL`; `lot_class = 'compensation'` requires `expires_at IS NOT NULL`
- **Constraint** — a lot is **never** created by a refill; only a purchase, a compensation grant or an adjustment creates one (`RF-06`)

`credit_transaction` is the append-only movement log: reserve, settle, release, expire, refund, adjust. Every row names its lot, its `reservation_id` where applicable, its **signed micro-credit amount**, its reason, and the `logical_request_id` it settles where one applies. **No row is ever updated or deleted** (`ST-04`).

#### The two funding pools, and the one reservation

| Pool | Table | Unit | Recovers | Reserved by |
|---|---|---|---|---|
| Included capacity | `entitlement.capacity_bucket` | micro-credits | **Yes** (`§7.2`) | `entitlement.capacity_reservation.from_capacity_micro` |
| Purchased and compensation | `commerce.credit_lot` | micro-credits | **No** (`RF-06`) | `capacity_reservation.from_compensation_micro` / `from_purchased_micro` |

| # | Rule |
|---|---|
| FU-01 | **One reservation row spans both pools.** `entitlement.capacity_reservation` records the split across its three source columns, and settlement moves against exactly those (`ST-05`). Two reservation tables would make a partial settlement possible, which is the defect this unification removes. |
| FU-02 | **Reservation identity is the logical request**, not the attempt: `UQ (logical_request_id)` where the state is non-terminal. A logical request may make several provider attempts (`MT-02`); they share the one hold and settle once (`ST-01`). |
| FU-03 | **Supplier accounting is per attempt; customer accounting is per logical request.** `commerce.supplier_cost_entry` has one row per `provider_attempt`; `commerce.customer_settlement` has one row per `logical_ai_request`. **They are never joined as if one-to-one** — a platform-caused retry produces two supplier rows and one customer debit (`ST-07`, `MT-08`). |
| FU-04 | **A lot's `held_micro` is maintained by the same shared unit of work that maintains the bucket's** (`§6.1.1` of the overview), so the two pools cannot disagree about what is held. |
| FU-05 | **A refund holds, then zeroes, the lot's remaining amount** (`AI-17`). It never returns micro-credits to the capacity bucket, and never mints capacity above the burst (`RF-05`). |

### `commerce.ledger_entry`

Three ledgers, one table, discriminated and **never joined across the discriminator** (`LG-01`, `LG-03`):

> **Units corrected 2026-09-08.** A single `money` amount column spanned all three ledgers, including `customerCredit` — but customer amounts are **integer micro-credits**, not money (`CD-01`, `MT-07`, `I-493`). Storing a service unit in a money column invites exactly the conflation the three-ledger rule exists to prevent. The amount is now **two mutually exclusive columns**, one per unit system.

| Field | Type | Notes |
|---|---|---|
| `ledger_entry_id` | `id` | **PK** |
| `ledger` | `enum(providerCost, customerCredit, paymentRevenue) NN` | |
| `workspace_id` | `id?` | Null for provider-cost rows that are not workspace-attributable |
| `amount_micro` | `int64?` | **Signed micro-credits.** Set **only** for `customerCredit` |
| `amount_money` | `decimal(28,9)?` | **Signed money.** Set **only** for `providerCost` and `paymentRevenue` |
| `currency` | `char(3)?` | **Required** whenever `amount_money` is set; **NULL** for `customerCredit`, which is currency-independent (`ST-08`, `MT-16`) |
| `occurred_at` | `instant NN` | |
| `reference_kind`, `reference_id` | `text NN`, `id NN` | What the entry is about |
| `created_at` | `instant NN` | |

- **Append-only.** A correction is a new entry (`BC-05`)
- `IX (ledger, occurred_at)`; `IX (ledger, workspace_id, occurred_at)`
- **Constraint** — `ledger = 'customerCredit'` requires `amount_micro IS NOT NULL AND amount_money IS NULL AND currency IS NULL`
- **Constraint** — `ledger IN ('providerCost','paymentRevenue')` requires `amount_money IS NOT NULL AND currency IS NOT NULL AND amount_micro IS NULL`
- **Constraint** — a policy test asserts no query joins two `ledger` values, and **no query sums `amount_micro` with `amount_money`** — they are different quantities in different units (`I-493`)
- **Rule** — margin is a **report** computed by relating rows across ledgers through their references, never a stored figure and never a subtraction of one column from another (`LG-04`)

---

## 8. `chat`, `task`, `agent`

**Cloud commits every row in this schema** (`§4.2` of the overview). Chat and Task are Cloud-authoritative; clients hold read projections plus, for Chat, unsent local drafts.

### `chat.conversation`, `chat.message`

The client schema (`§2` of [`02-desktop-data-model.md`](02-desktop-data-model.md)) mirrors these, not the reverse. **Cloud holds the authoritative acknowledged revision and is its committer** (`AU-01`, `CW-02`); the client copy is a working cache plus unsent drafts.

| # | Rule |
|---|---|
| CH-D1 | **Cloud writes these tables directly.** `chat.appendMessage` commits the user message; the Harness commits the assistant message. A Cloud-originated message requires no device and no client change (`CW-03`). |
| CH-D2 | **`rev` is assigned by Cloud.** A client's `local_rev` is a device-scoped counter for unsent work and never appears here (`CW-01`). |
| CH-D3 | **Every commit writes its `sync.change` row in the same transaction** (`CW-06`), so a message can never exist without being publishable. |
| CH-D4 | **An unsent draft is not a row here.** It lives only on the device that composed it (`I-124`), and is therefore never a competing revision. |
| CH-D5 | **A message is immutable once committed** (`WP-15.00`). An edit creates a new branch; a stream in progress is not a row at all until the turn completes (`§7` of the harness). |
| CH-D6 | **`chat.stream_chunk` and `chat.stream_state` are transient rows, not aggregates** (`SB-01`). They carry no revision, never appear in `sync.change`, are excluded from backup, and are swept by `expires_at`. They live in the shared database rather than in a replica's memory **because any replica must be able to serve any read** (`SB-04`); that is a deployment consequence of identical replicas, not a storage preference. |

### `task.task`

| Field | Type | Notes |
|---|---|---|
| `task_id` | `id` | **PK** |
| `workspace_id` | `id NN` | |
| `owning_product` | `text NN` | Whose **domain** the work concerns. It never transfers, and it does **not** move the authoritative store (`TO-01`) |
| `origin_surface` | `enum(desktop, web, mobile, automation) NN` | Where the request came from. Provenance only — it confers no authority (`TO-03`) |
| `origin_device_id` | `id?` | Present when a device originated it; **null for Web, Mobile and automation** |
| `state` | `enum(created, queued, running, waitingApproval, waitingDevice, waitingCapacity, paused, succeeded, failed, cancelled, unknownEffect) NN` | |
| `reason_facet` | `text?` | *Why* it is in that state (`WP-16.01`) |
| `intent_summary` | `text NN` | User-facing |
| `created_at`, `updated_at` | `instant NN` | |
| `rev` | `rev NN` | |

- `IX (workspace_id, state, updated_at)` — the task centre

> **Corrected 2026-09-08.** The table carried `placement ∈ {local, cloud, remoteViaBridge}`, `authoritative_store ∈ {cloud, device}` and a check constraint forcing local placement to device authority. All three contradict `TO-01`: **every Agent Task is Cloud-owned**, and no Agent Task has a device authoritative store. They are removed rather than defaulted, because a column whose only legal value is `cloud` invites code to branch on it.

| # | Rule |
|---|---|
| TK-01 | **There is no `placement` column and no `authoritative_store` column.** The authoritative store is always Cloud (`TO-01`). What varies is **each Step's tool locality**, which lives on `task.plan_step` (`TK-02`), because one Task routinely mixes both. |
| TK-02 | **`plan_step.tool_locality ∈ {cloud, device}`**, with `target_device_id` on the Step — not on the Task — since different Steps of one Task may target different devices, or none. |
| TK-03 | **A native Product Job is not in this table at all** (`TO-05`, `I-485`). It lives in its product's own store with its own job identity; the task centre reads both through a union projection and labels each with its owner (`WP-17.03`). |
| TK-04 | **`origin_surface` and `origin_device_id` are provenance, never authority.** A Task created from Web has no device and is fully executable; a device is required only for a Step whose locality is `device` (`CW-03`). |
| TK-05 | **Cancellation and recovery are Cloud-side for the Task and product-side for a Product Job.** Cancelling a Task cancels its Steps; a Step that started a Product Job requests that product's cancellation and records the outcome — it does not reach into the product's store. |

### `task.run`, `task.plan_step`, `task.attempt`

**Tool locality lives on the Step** (`TK-02`), because one Task mixes cloud and device Steps.

| `plan_step` field | Type | Notes |
|---|---|---|
| `plan_step_id` | `id` | **PK** |
| `run_id` | `id NN` | `FK →`; cascade |
| `step_ordinal` | `int NN` | |
| `capability_key` | `text NN` | Resolved through the generated allowlist (`DP-04`) |
| `tool_locality` | `enum(cloud, device) NN` | **Declared, never inferred** (`PL-02` of the harness) |
| `target_device_id` | `id?` | Required when `tool_locality = 'device'`, else null |
| `state`, `reason_facet` | `text NN`, `text?` | |

- `IX (target_device_id, state)` — **the tool-request pull path**, now correctly on the Step
- **Constraint** — `tool_locality = 'device'` requires `target_device_id IS NOT NULL`; `cloud` requires it to be null
- **Constraint** — a Step declared `device` is **never** satisfied by a cloud substitute (`PL-02`); if no eligible device is online the Step waits with a stated reason


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

### `agent.model_descriptor`, `agent.tariff_version`, `agent.supplier_price_version`

`model_descriptor` and the two price tables are workspace-independent catalogue rows **projected from an activated configuration revision** (`CG-02`, `DC-05`, `DC-06`). They are persisted snapshots, not live lookups into the current file (`I-494`).

| Table | Holds | Applies at |
|---|---|---|
| `agent.model_descriptor` | Provider route, concrete model and version, billed categories, per-unit divisor, inclusion semantics, tier selection rules, output and context ceilings, lifecycle state | Resolution time |
| `agent.supplier_price_version` | **What ArcForges pays**: per-category rate, currency, unit divisor, validity | **Dispatch time** (`MT-06`) |
| `agent.tariff_version` | **What the customer is charged**: per-category service units, tier, validity | **Pinned to the Run or request** (`MT-06`, `CR-09`) |

- Both price tables are **append-only with effective dates**; a new price is a new row, never an update
- **Constraint** — a `model_descriptor` with any billable category lacking a rate in the applicable `supplier_price_version` **cannot be dispatched** (`AD-04`, `DC-05`, `MT-15`). There is no assumed zero rate
- **Constraint** — `config_revision_id` on every row records which activated revision produced it, so a historical charge is reproducible after the model is retired (`RP-02`, `MT-14`)

---

## 8.1 `commerce` — the metering chain *(new — P2-006)*

Five tables carry `MT-01`–`MT-16`. They form one identity chain from request to ledger (`RP-01`).

```
logical_ai_request ──1:N──> provider_attempt ──1:N──> attempt_usage
        │                          │                       │
        │                          └──1:1──> supplier_cost_entry
        └──1:1──> capacity_reservation ──1:1──> customer_settlement ──> ledger_entry
```

### `commerce.logical_ai_request`

| Field | Type | Notes |
|---|---|---|
| `logical_request_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` |
| `service_term_id` | `id NN` | `FK →` `entitlement.service_term` — **which term authorised this** (`AD-01`, `MT-14`) |
| `run_id`, `step_id`, `attempt_id` | `id?` | Present for agent work; absent for an ordinary chat request |
| `beneficiary` | `enum(userDelivered, platformRouting, platformAbuse, platformHealth, platformIndexing, platformRetry) NN` | Decides who pays (`ST-07`, `MT-08`) |
| `tariff_version_id` | `id NN` | **Pinned here**, not looked up later (`MT-06`) |
| `config_revision_id` | `id NN` | `CG-02` |
| `state` | `enum(admitted, dispatched, settled, usagePending, costUnconfirmed, resolvedByPolicy, cancelled, rejected) NN` | `§7.6` of the commerce architecture |
| `created_at`, `settled_at` | `instant NN`, `instant?` | |

- `UQ (logical_request_id)`; `IX (workspace_id, created_at)`; `IX (state, created_at)` — the reconciliation-deadline sweep
- **Constraint** — `beneficiary != userDelivered` rows **never debit a customer** (`ST-07`)

### `commerce.provider_attempt`

| Field | Type | Notes |
|---|---|---|
| `provider_attempt_id` | `id` | **PK** |
| `logical_request_id` | `id NN` | `FK →`; **one logical request may have many attempts** (`MT-02`, `PR-07`) |
| `attempt_ordinal` | `int NN` | |
| `provider_request_ref` | `text NN` | The provider's own request identity (`MT-02`) |
| `model_descriptor_id` | `id NN` | Concrete model and version actually used |
| `supplier_price_version_id` | `id NN` | **Dispatch-time** version (`MT-06`) |
| `route`, `processing_tier`, `context_tier`, `region_tier` | `text NN` | Resolved from actual request facts (`MT-04`, `UN-06`) |
| `dispatched_at`, `completed_at` | `instant NN`, `instant?` | |
| `usage_source` | `enum(providerFinal, providerStream, invoice, unresolved) NN` | (`MT-05`) |
| `completeness` | `enum(complete, pending, unconfirmed, mismatched) NN` | (`MT-12`) |
| `outcome` | `enum(delivered, providerError, platformError, cancelled, timeout) NN` | |

- `UQ (logical_request_id, attempt_ordinal)`
- **Constraint** — **no prompt or response content** is stored here (`MT-02`); content lives in the product store, counts live here
- **Rule** — a genuinely distinct retry is a **distinct row with its own supplier cost** (`ST-03`, `MT-11`)

### `commerce.attempt_usage`

The normalised, non-overlapping category quantities (`MT-03`, `§7.4` there).

| Field | Type | Notes |
|---|---|---|
| `attempt_usage_id` | `id` | **PK** |
| `provider_attempt_id` | `id NN` | `FK →` |
| `usage_revision` | `int NN` | **Increments on each cumulative stream snapshot** (`UN-03`, `I-492`) |
| `category` | `text NN` | `input.uncached` · `input.cached_read` · `input.cache_write` · `output` · `output.reasoning` · `tool.<kind>` |
| `quantity` | `int64 NN` | Non-negative (`UN-05`) |
| `unit` | `text NN` | `token` · `request` · `second` · `image` (`MT-10`) |
| `recorded_at` | `instant NN` | |

- `UQ (provider_attempt_id, usage_revision, category)` — **this is the idempotency key** (`ST-03`, `MT-11`)
- **Rule** — a later `usage_revision` **replaces** the earlier total for that attempt; revisions are never summed (`UN-03`)
- **Constraint** — a category not declared by the attempt's model descriptor is **rejected into reconciliation**, never debited (`UN-02`, `MT-05`)

### `commerce.supplier_cost_entry`

| Field | Type | Notes |
|---|---|---|
| `supplier_cost_id` | `id` | **PK** |
| `provider_attempt_id` | `id NN` | `FK →` |
| `currency` | `char(3) NN` | **Always present** (`ST-08`, `MT-16`) |
| `amount` | `decimal(28,9) NN` | ≥ 9 fractional digits (`MT-07`). **Never a float** |
| `basis` | `enum(estimated, usageConfirmed, invoiceReconciled) NN` | The three remain distinguishable (`UC-03`, `MT-13`) |
| `unresolved` | `bool NN` | Retained even when the customer hold is released (`ST-06`, `MT-12`) |

- `IX (basis, unresolved)` — the reconciliation queue
- **Constraint** — a row is **never deleted or updated**; a correction is a new linked adjustment row (`ST-04`)

### `commerce.customer_settlement`

| Field | Type | Notes |
|---|---|---|
| `settlement_id` | `id` | **PK** |
| `logical_request_id` | `id NN` | `FK →` |
| `reservation_id` | `id NN` | `FK →` `entitlement.capacity_reservation` |
| `debit_capacity_micro`, `debit_compensation_micro`, `debit_purchased_micro` | `int64 NN` | Debited **against the sources the reservation held** (`ST-05`) |
| `released_micro` | `int64 NN` | Returned to those same sources, capped by the burst (`RF-05`) |
| `rounding_mode` | `text NN` | Declared half-even (`ST-01`) |
| `settled_at` | `instant NN` | |
| `adjusts_settlement_id` | `id?` | Present on a correction; the original is never edited (`ST-04`) |

- `UQ (logical_request_id)` **where `adjusts_settlement_id IS NULL`** — one settlement per logical request (`ST-01`)
- **Constraint** — settlement occurs **once, after category aggregation**, never per stream fragment (`ST-01`)

---

## 8.2 `config` — activated policy revisions *(new — P2-006)*

`DC-04`, `DC-09`, `DC-12` make the activated bundle a persisted fact, not a file read at request time.

### `config.revision`

| Field | Type | Notes |
|---|---|---|
| `config_revision_id` | `id` | **PK** |
| `schema_version` | `text NN` | |
| `revision_identity` | `text NN` | Operator-supplied; **immutable** |
| `content_hash` | `bytes NN` | |
| `environment`, `realm_id` | `text NN`, `id NN` | Rejected on mismatch (`DC-04`) |
| `effective_at` | `instant NN` | |
| `activated_at` | `instant?` | Null until activation succeeds |
| `state` | `enum(validated, active, superseded, rejected) NN` | |
| `document` | `json NN` | The validated bundle as activated |

- `UQ (revision_identity)` — **a revision identity cannot be reused with different content** (`DC-04`), enforced together with `content_hash`
- `UQ (realm_id, state)` **where `state = 'active'`** — exactly one active revision per realm (`CG-03`)
- **Rule** — a replica that cannot load the active revision **admits no affected work**; it does not fall back to a previous revision or a sample (`CG-03`, `DC-11`)
- **Rule** — rollback publishes a **new** revision restoring prior values (`DC-12`); it never reactivates a superseded row

---

## 8.3 `scope` — the deterministic Cloud simulator *(new — P2-006)*

`SIM-01`–`SIM-20` of the ArcScope requirements. Cloud owns the definition and the run; ArcScope owns the native session projection and the downloaded capture (`SIM-01`).

**A `SimulationRun` is a product job, not an Agent Run, and invokes no model** (`SIM-01`, `CM-04` of the runtime architecture). It consumes product-resource quota — duration, samples, bytes, egress — never model tokens (`SIM-17`).

### `scope.simulation_definition`, `scope.scenario_version`

| Field | Type | Notes |
|---|---|---|
| `definition_id` / `scenario_version_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →`; owner scope |
| `version_ordinal` | `int NN` | On `scenario_version` |
| `channel_schema` | `json NN` | Stable channel ids, value types, units, rate and timestamp semantics, encoding (`SIM-03`) |
| `expression_ast` | `json?` | Bounded AST (`SIM-04`) |
| `fault_profile` | `json?` | Latency, jitter, drop, duplicate, reorder, disconnect, malformed, outlier (`SIM-05`) |
| `content_hash` | `bytes NN` | |
| `created_at` | `instant NN` | |

- `UQ (definition_id, version_ordinal)`
- **Constraint** — a `scenario_version` is **immutable** (`SIM-02`). Editing a definition creates a new version and **affects future runs only**
- **Constraint** — AST validation runs **before admission** (`SIM-04`): acyclic channel dependencies, bounded depth, node count and per-tick operations. No script, dynamic compilation, reflection, file access or network

### `scope.simulation_run`

| Field | Type | Notes |
|---|---|---|
| `run_id` | `id` | **PK** |
| `workspace_id` | `id NN` | `FK →` |
| `scenario_version_id` | `id NN` | `FK →` — **the immutable version, not the definition** (`SIM-02`) |
| `seed` | `int64 NN` | |
| `execution_profile` | `text NN` | Pins numeric semantics, RNG, generator and encoding versions (`SIM-07`) |
| `clock_mode` | `enum(realTime, accelerated) NN` | Pacing **never changes sample values, logical timestamps or hashes** (`SIM-06`) |
| `duration_ticks` | `int64 NN` | The requested finite logical range |
| `state` | `enum(queued, starting, running, pausing, paused, stopping, canceled, succeeded, failed) NN` | (`SIM-08`) |
| `terminal_reason` | `text?` | |
| `completed_ticks` | `int64 NN` | **Partial extent is queryable** (`SIM-08`, `SIM-09`) |
| `service_term_id` | `id NN` | `FK →` — official simulation requires an active term (`SIM-17`) |
| `rev` | `rev NN` | |

- `IX (workspace_id, state)`; `IX (state, updated_at)` — the scheduler path
- **Constraint** — `succeeded` requires `completed_ticks = duration_ticks`. **A cancel records a partial outcome, never success for an incomplete range** (`SIM-08`)
- **Constraint** — a terminal run cannot be resurrected; a duplicate start creates no second run (`SIM-09`)

### `scope.simulation_lease`

| Field | Type | Notes |
|---|---|---|
| `run_id` | `id` | **PK** — one live lease per run |
| `holder_instance` | `text NN` | |
| `fence_token` | `int64 NN` | **Monotonic**; a publish carrying a stale token is rejected (`SIM-10`) |
| `expires_at` | `instant NN` | |

- **Rule** — this is what lets N identical replicas run the simulator without two of them publishing the same logical segment (`RT-04`, `SIM-10`)

### `scope.simulation_segment`

The manifest over immutable object-storage segments (`SIM-11`).

| Field | Type | Notes |
|---|---|---|
| `segment_id` | `id` | **PK** |
| `run_id` | `id NN` | `FK →` |
| `sequence` | `int64 NN` | |
| `logical_from_tick`, `logical_to_tick` | `int64 NN` | |
| `sample_count` | `int64 NN` | |
| `encoding` | `text NN` | |
| `byte_length` | `int64 NN` | |
| `content_hash` | `bytes NN` | Client-verifiable (`SIM-13`) |
| `object_key` | `text NN` | |
| `fence_token` | `int64 NN` | The token under which it was published |

- `UQ (run_id, sequence)`; `UQ (run_id, logical_from_tick)`
- **Constraint** — **a committed manifest row never references an unverified partial object** (`SIM-11`). The object is written and verified first; the manifest row is the commit point
- **Rule** — an incomplete object stays **invisible** and is cleaned; visibility is the manifest row, not the object's existence

### `scope.simulation_checkpoint`

| Field | Type | Notes |
|---|---|---|
| `run_id` | `id` | **PK** |
| `next_tick` | `int64 NN` | |
| `rng_state` | `bytes NN` | Per channel and per fault source, independently seeded (`SIM-05`) |
| `generator_state` | `json NN` | |
| `replay_position` | `json?` | For CSV replay (`SIM-18`) |
| `pending_fault_state` | `json NN` | Reorder and duplicate buffers (`SIM-05`) |
| `committed_segment_sequence` | `int64 NN` | |
| `updated_at` | `instant NN` | |

- **Constraint** — the checkpoint advances **only after** the corresponding manifest row commits (`SIM-11`, `SIM-12`)
- **Rule** — pause/resume, host loss and lease takeover produce **the same remaining canonical data**, with no duplicate and no missing logical range (`SIM-12`). This is the single most important simulator invariant, and `SIM-20` tests it by killing the host

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

> **Corrected 2026-09-07.** The previous design allocated `change_seq` from a database sequence inside the applying transaction and asserted that this prevented false gaps. **It does not.** Sequence allocation is non-transactional and ordered by *call*, while row visibility is ordered by *commit*. Transaction A may take 100 and stay open while B takes 101 and commits; a reader then serves 101, advances its cursor past 100, and **never sees A's change when A finally commits**. Monotonic allocation is not commit order, and no watermark derived from the sequence alone repairs it.

| Field | Type | Notes |
|---|---|---|
| `change_id` | `id` | **PK** — identity only, never a cursor |
| `workspace_id` | `id NN` | |
| `aggregate_kind` | `text NN` | |
| `aggregate_id` | `id NN` | |
| `aggregate_rev` | `rev NN` | |
| `change_kind` | `enum(upsert, tombstone) NN` | |
| `origin_kind` | `enum(device, cloud) NN` | **Cloud-originated changes exist** — an assistant message needs no device (`CW-03`) |
| `origin_device_id` | `id?` | **Null when `origin_kind = 'cloud'`**; set when a device submitted the change |
| `occurred_at` | `instant NN` | Wall clock, for display; **never a cursor** |
| `publish_seq` | `bigint?` | **NULL until published.** Assigned in commit order by the publisher (`§9.1`) |
| `published_at` | `instant?` | |

- `IX (workspace_id, publish_seq)` **WHERE `publish_seq IS NOT NULL`** — the only feed query path
- `IX (workspace_id, change_id)` **WHERE `publish_seq IS NULL`** — the publisher's claim path
- **Constraint** — the row is written **in the business transaction** (`CW-06`), so a committed change is always publishable
- **Constraint** — `origin_kind = 'device'` requires `origin_device_id IS NOT NULL`; `cloud` requires it to be null
- **Rule** — **echo suppression matches on `origin_device_id`, and a null never matches.** A device skips a change only when `origin_kind = 'device' AND origin_device_id = <its own>`. A Cloud-originated change is therefore **never** suppressed as somebody's echo — which, with a non-null column and a placeholder value, is exactly what would have happened to every assistant message
- **Constraint** — `UQ (workspace_id, publish_seq)`; `publish_seq` is assigned once and never changed

#### 9.1 Publication — commit order, not allocation order

The cursor is `publish_seq`, and **only the publisher assigns it**. The publisher is a lease-fenced hosted service in the single host (`RT-04` of the cloud architecture), so exactly one assigner is live per workspace shard at a time.

```
publish(workspace):
    hold the workspace's publication lease (fenced)             -- RT-04
    BEGIN
      SELECT change_id FROM sync.change
        WHERE workspace_id = ? AND publish_seq IS NULL
        ORDER BY change_id
        FOR UPDATE SKIP LOCKED                                  -- only COMMITTED rows are visible
      assign publish_seq = watermark + 1, 2, 3 ... in that order
      UPDATE sync.change SET publish_seq = ?, published_at = now()
      UPDATE sync.publication_watermark SET last_seq = ?
    COMMIT
```

| # | Rule |
|---|---|
| PB-01 | **Only committed rows are ever visible to the publisher**, because it reads them in a separate transaction. An uncommitted change is simply not there yet, and gets its `publish_seq` on a later pass — **after** the sequence numbers already served, never before. That is the property the old design tried and failed to get from an in-transaction sequence. |
| PB-02 | **A reader may never see a `publish_seq` lower than one it has already been served.** This is what makes the cursor safe, and it is a consequence of `PB-01` rather than an assertion. |
| PB-03 | **Assignment is monotonic per workspace** and gapless by construction: the publisher allocates from its own durable watermark inside the same transaction that sets the rows, so a publisher crash rolls back both. |
| PB-04 | **A rolled-back business transaction leaves no row at all**, so a rollback cannot create a gap. The old design's rollback gap came from the sequence, which this design does not use for the cursor. |
| PB-05 | **Publication latency is bounded and observable.** Oldest unpublished age is a monitored signal (`§5` of the observability architecture); a stalled publisher is a page-worthy condition, because it stalls every client's feed. |
| PB-06 | **`change_id` is never a cursor.** It orders the publisher's own claim scan only; it carries no cross-transaction ordering meaning. |

#### 9.2 Cursor, bootstrap and retention

| # | Rule |
|---|---|
| CU-01 | **A cursor is `(workspace_id, publish_seq)`** and is opaque to the client (`QP-02`). A client never constructs one. |
| CU-02 | **Bootstrap is a snapshot plus a cursor taken together.** The server reads the current watermark `W`, then serves the aggregate snapshot as of a transaction that can see everything published up to `W`, and returns the cursor `W`. Anything published after `W` arrives through the feed. **A snapshot without its matching cursor is prohibited**, because the seam between them is exactly where a change is lost. |
| CU-03 | **A cursor beyond the retention floor is refused with `sync.cursor_expired`**, and the client performs a full resync (`DL-02`). It is never silently clamped, because clamping would skip the changes between the floor and the cursor. |
| CU-04 | **Retention pruning removes only rows below the floor**, and the floor advances only after the tombstone-retention window (`DL-01`), so a returning device either resyncs fully or sees every tombstone it needs. |
| CU-05 | **Publication is per workspace**, so one workspace's slow publisher cannot stall another's feed, and a workspace's sequence has no relationship to any other's. |
| CU-06 | **The feed is at-least-once.** A client may see a `publish_seq` twice after a reconnect and applies it idempotently by `(aggregate_kind, aggregate_id, aggregate_rev)` (`GP-05` of the realtime and bridge contract — **not** the `GP-05` in the persistence or native-interop architecture, which are unrelated families; see `OG-05`). |

### `sync.publication_watermark`

| Field | Type | Notes |
|---|---|---|
| `workspace_id` | `id` | **PK** |
| `last_seq` | `bigint NN` | The highest assigned `publish_seq`; **monotonic** |
| `updated_at` | `instant NN` | |

- **Constraint** — `last_seq` is non-decreasing, enforced by a checked update predicate
- **Rule** — the watermark and the row updates commit together, so a crashed publisher leaves neither

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
| CX-02 | Every `entitlement.capacity_reservation` in `held` belongs to a live `commerce.logical_ai_request` that has not settled | Reservation creation, in the shared unit of work (`SU-01`) | The reservation sweeper (`CS-04`) |
| CX-08 | For every workspace, the sum of live `capacity_reservation.from_capacity_micro` equals `capacity_bucket.held_micro`, and the sum of `from_compensation_micro` + `from_purchased_micro` per lot equals that lot's `held_micro` | The shared unit of work (`FU-04`) | Accounting comparison (`WP-42.11`) |
| CX-09 | Every settled `logical_ai_request` has exactly one non-adjusting `customer_settlement`, and at least one `provider_attempt`; **the counts are not required to match** (`FU-03`) | Settlement, in the shared unit of work | Reconciliation (`WP-43.07`) |
| CX-10 | Every `sync.change` row with a non-null `publish_seq` has a `publish_seq` less than or equal to its workspace's `publication_watermark.last_seq` | The publisher's transaction (`PB-03`) | Feed integrity check |
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
