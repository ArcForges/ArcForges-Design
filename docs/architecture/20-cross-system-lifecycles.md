# Cross-System Lifecycles

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **D-010** (topology), **D-020** (commercial figures and metering), `§9` of the commerce architecture, `§13` of the sync architecture
> Companions: [`07-sync-conflict-and-backup.md`](07-sync-conflict-and-backup.md), [`16-billing-and-commerce-architecture.md`](16-billing-and-commerce-architecture.md), [`contracts/03-realtime-and-bridge.md`](contracts/03-realtime-and-bridge.md), [`data-model/00-data-model-overview.md`](data-model/00-data-model-overview.md)

Each architecture document states its own rules correctly. **What no document states is what happens when a lifecycle crossing two or more of them fails halfway.** A payment captured without an entitlement granted, a change applied on the server but lost before the client recorded it, a deletion that completed in three stores out of five — these are the defects that reach production, because each system behaved correctly in isolation.

This document traces each cross-system lifecycle end to end and states, for every failure point: **what the user's effect certainty is, who detects the divergence, who owns the repair, and whether repair is automatic.**

---

## 1. Vocabulary

| Term | Meaning |
|---|---|
| **Effect certainty** | `didNotHappen` · `happened` · `unknown` — the three states any cross-system step can leave (`§3` of the operation catalogue) |
| **Partial success** | Some systems applied the change and some did not. **Never reported to the user as success**, and never as plain failure |
| **Detector** | The mechanism that notices the divergence: a foreground path, a reconciliation job, a health check, or a user report |
| **Owner** | The component responsible for the repair. Exactly one per failure |
| **Auto-repair** | Whether the system converges without a human. Where it does not, the outcome is an explicit attention item, never a silent stall |

| # | Rule |
|---|---|
| XL-01 | **Every cross-system lifecycle has exactly one authoritative owner per step**, and the owner is named in this document. A step with two owners is a defect. |
| XL-02 | **A partial success is a distinct outcome.** It is recorded as partial, reported as partial, and repaired as partial — not rounded to success or to failure. |
| XL-03 | **No lifecycle relies on a message arriving.** Every step that matters is recoverable by a scheduled comparison of authoritative state (`RE-01` of the commerce architecture; `GP-03` of the realtime contract). |
| XL-04 | **`unknown` is never silently resolved to `didNotHappen`.** Assuming an effect did not happen is how a duplicate charge or a duplicate real-world action is produced (`CN-03` of the harness). |
| XL-05 | **Auto-repair is permitted only where the repair is idempotent and its blast radius is bounded.** Everything else raises an attention item with the evidence attached. |
| XL-06 | **A repair is expressed as a new record**, never as an edit to history (`RE-05` there, `BC-05`). |
| XL-07 | **Every lifecycle below has at least one release-gating test per failure row** (`§10`). A failure row with no test is an untested claim. |

---

## 2. Purchase to entitlement

The single most consequential lifecycle: money moves in one system and access changes in another.

```
client                cloud commerce            provider              entitlement
  │  purchase.createIntent  │                        │                     │
  ├────────────────────────▶│ purchase_intent (open) │                     │
  │                         ├───────────────────────▶│ checkout session    │
  │  ◀── redirect / sheet ──┤                        │                     │
  │  ══════ user pays at the provider ═══════════════▶                     │
  │                         │◀── webhook: paid ──────┤                     │
  │                         │ provider_event (persist before process)      │
  │                         │ verify → order → payment                     │
  │                         ├─────────────────────────────────────────────▶│ grant
  │                         │                        │  entitlement_version++
  │  ◀── entitlement.changed (a hint) ───────────────────────────────────  │
  │  ── entitlement.getSnapshot (authoritative) ────────────────────────▶  │
```

| # | Failure point | Effect certainty | Detected by | Owner | Outcome | Auto-repair |
|---|---|---|---|---|---|---|
| PE-01 | Intent created; user never pays | `didNotHappen` | Attempt expiry sweep | Commerce | Intent closed by policy; a later event for it is **reconciled, not silently granted** (`PU-04`) | Yes |
| PE-02 | User paid; webhook never arrives | **`happened` at the provider, `didNotHappen` in ArcForges** | Scheduled reconciliation comparing both directions | Commerce | Order and grant created from provider state. **Losing a webhook must never cost the user their subscription** (`RE-02`) | Yes |
| PE-03 | Webhook arrives twice | `happened` once | Inbox idempotency on `(eventType, eventId)` | Commerce | Second delivery is a no-op (`EI-02`) | Yes |
| PE-04 | Webhook arrives out of order | `happened` | State-based application | Commerce | Applied against current normalised state; a stale event is a no-op, never a regression (`EI-06`) | Yes |
| PE-05 | Webhook signature invalid | `unknown` | Verification chain | Commerce | Recorded and **rejected, never processed** (`EI-03`); quarantined with a reason and alerting (`EI-07`) | No — investigated |
| PE-06 | Order written, **grant write fails** | **Partial success** | Foreground failure plus a reconciliation invariant: *every paid order has a matching grant* | Entitlement | Grant retried from the durable order; the order is never rolled back, because the money moved | Yes |
| PE-07 | Grant written, `entitlement_version` not bumped | Partial success | Reconciliation invariant: *every grant is reflected in the current snapshot* | Entitlement | Version recomputed; clients re-read | Yes |
| PE-08 | Grant written; client never receives `entitlement.changed` | `happened` | The client re-reads the snapshot on reconnect and on entitlement-sensitive actions | Client | Converges on next read (`RE-06` of the realtime contract) | Yes |
| PE-09 | Provider reports paid; ArcForges has **no matching intent** | `happened` at the provider | Verification chain step "known purchase intent or buyer identity" (`EI-05`) | Commerce | Quarantined for investigation. **Not granted** — an unmatched payment is a fraud and a defect signal, not a grant trigger | No |
| PE-10 | Payment later refunded or charged back | `happened` then reversed | Provider event, plus reconciliation | Commerce → Entitlement | **Revocation, never grant deletion** (`RE-05`). Access ends per the revocation's own effective time | Yes |
| PE-11 | Payment captured, currency or amount differs from the locked price version | Partial success | Reconciliation amount comparison | Commerce | Divergence produces a typed repair action, an audit record and, above a threshold, an alert (`RE-04`) | No — above threshold |

| # | Rule |
|---|---|
| PE-R1 | **The order is never rolled back to "fix" a failed grant.** Money that moved is a fact; the repair is forward (`XL-06`). |
| PE-R2 | **A grant is never created from a client assertion**, only from a verified provider event or an administrative action with its own audit trail. |
| PE-R3 | **Entitlement survives Commerce being unavailable** (`EO-05`), so a commerce outage degrades purchasing, never existing access. |

---

## 3. Subscription lifecycle

| # | Failure point | Effect certainty | Detected by | Owner | Outcome | Auto-repair |
|---|---|---|---|---|---|---|
| SU-01 | Renewal succeeds at the provider; no event received | `happened` | Reconciliation | Commerce | Period extended from provider state | Yes |
| SU-02 | Renewal fails (payment declined) | `didNotHappen` | Provider event | Commerce → Entitlement | Grace period per policy, then revocation. **The user is told before access changes**, not after | Yes |
| SU-03 | User cancels in the provider's own portal | `happened` | Provider event, and reconciliation as backstop | Commerce | Subscription state normalised; access continues to period end | Yes |
| SU-04 | Cancellation recorded in ArcForges; provider still renews | Partial success | Reconciliation, both directions (`RE-01`) | Commerce | Divergence raised; refund or correction is a typed repair action with audit | No |
| SU-05 | Plan change mid-period | `happened` | Provider event | Commerce → Entitlement | Proration per the provider's own model; **the entitlement snapshot reflects the new plan at its effective time**, not at event-arrival time | Yes |
| SU-06 | Downgrade leaves the workspace over quota | `happened` | Quota evaluation | Entitlement | **Read, download and delete remain permitted; writes that increase usage are refused with the entitlement reason** (`§13` of the sync architecture). Data is never deleted to enforce a downgrade | Yes |
| SU-07 | Store-mediated subscription (mobile) diverges from cloud state | Partial success | Reconciliation against the store's server-side receipt | Commerce | Store receipt is authoritative for store-mediated purchases; ArcForges state is corrected toward it | Yes |

---

## 4. AI admission, capacity and settlement

**P2-006 replaces the single-balance credit lifecycle with a service term, a replenishing bucket and opt-in credits.** Three things must go right in order, and each can fail independently.

```
service term active?  --no-->  entitlement.no_service_term          -- a credit balance does NOT resolve this
   | yes
   v
refill bucket over eligible paid interval only                       -- AC-02, RF-01
   |
   v
ATOMIC admit: reserve bound from capacity -> compensation -> authorised purchased
   |          + concurrency, per-request/per-run ceilings, provider budget
   |--insufficient--> WaitingForCapacity(recoveryAt) | ExtraCreditsRequired | Reject
   v
dispatch -> provider attempts -> normalise usage into non-overlapping categories
   v
settle once per logical request: supplier cost (dispatch price) + customer cost (pinned tariff)
   v
debit and release against the SAME sources the reservation held
```

| # | Failure point | Effect certainty | Detected by | Owner | Outcome | Auto-repair |
|---|---|---|---|---|---|---|
| AI-01 | Purchased credits present, paid term expired | `didNotHappen` | Admission, **first check** | Entitlement | `entitlement.no_service_term`. Credits are **retained and remain recorded**; renewal re-enables them without reissue (`CR-05`) | N/A — the user renews |
| AI-02 | Capacity exhausted, no extra-credit authorisation | `didNotHappen` | Admission | Entitlement | `entitlement.capacity_exhausted` with a **server-calculated `recoveryAt`** (`AC-06`, `EC-03`) | Yes — recovery is time-based |
| AI-03 | Capacity exhausted, credits present, extra usage not opted in | `didNotHappen` | Admission | Entitlement | `entitlement.extra_credits_required`. **No automatic purchase, recharge or paid fallback** (`AC-06`) | No — explicit opt-in |
| AI-04 | Request bound can never fit capacity plus authorised credits | `didNotHappen` | Admission | Entitlement | Rejected immediately with a smaller-request or budget action, **never queued forever** (`AC-04`, `AD-03`) | No |
| AI-05 | Two devices admit concurrently against one bucket | Both attempt | Atomic reservation under the bucket lock | Entitlement | One succeeds, one waits or is refused. **A check without a reservation would let both pass** (`AD-02`, `CR-21`) | Yes |
| AI-06 | Replica race on refill | — | Monotonic watermark plus row lock | Entitlement | Serialised; **no double credit** (`RF-02`, `AC-12`) | Yes |
| AI-07 | Clock rolls backwards | — | `watermark_at` non-decreasing constraint | Entitlement | Elapsed time clamps to zero; the bucket does not refill (`AC-02`) | Yes |
| AI-08 | Process restart mid-turn | `unknown` for the in-flight attempt | Reservation expiry sweep | Commerce | Orphaned reservation released (`CS-04`); the attempt resolves through `§4.1` | Yes |
| AI-09 | Reservation held, work never dispatched | `didNotHappen` | Expiry sweep | Commerce | Released to its original sources, capped by the burst (`RF-05`) | Yes |
| AI-10 | Settlement write fails after provider work | **Partial — usage occurred, not charged** | Invariant: *no completed attempt lacks a settlement or an unresolved marker* | Commerce | Settlement is idempotent per attempt usage revision and re-runs (`ST-03`) | Yes |
| AI-11 | Duplicate or reordered usage events | `happened` once | `UQ (provider_attempt_id, usage_revision, category)` | Commerce | Later revision **replaces**, never sums (`UN-03`, `I-492`) | Yes |
| AI-12 | Provider retry caused by the platform | `happened` twice upstream | Beneficiary classification | Commerce | **Charged once to the customer, fully visible in supplier cost** (`ST-07`, `MT-08`) | Yes |
| AI-13 | Caller cancels mid-stream | Partial | Cancellation path | Commerce | Verified consumption within the authorised ceiling settles; the remainder releases. **Completed provider work is not presumed refundable** (`MT-09`) | Yes |
| AI-14 | Paid term expires **during** a running Task | `happened` so far | Term evaluation at each dispatch | Entitlement | Further dispatch stops at a **durable boundary** with the eligibility reason (`SV-06`). Settled work stays settled; holds release per `§7.6` | Yes |
| AI-15 | Task waiting for a device or an approval | — | Safe-boundary release | Entitlement | The included-capacity hold is **released at the boundary and re-reserved on resume** (`AC-05`, `PL-03`). One waiting Task cannot reserve the workspace | Yes |
| AI-16 | Configuration replaced mid-flight | — | Pinned snapshots | Configuration | The Run keeps its pinned customer tariff; supplier price applies to **future** dispatch only. **No reset of usage, capacity, credits or holds** (`DC-12`, `DC-13`, `AC-09`) | Yes |
| AI-17 | Refund of a purchased lot | Reversal | Refund hold then settlement | Commerce | Lot amount frozen, then zeroed. **A refund must not mint capacity above the burst** (`RF-05`, `AC-11`) | Yes |
| AI-18 | Verified supplier overrun beyond the authorised hold | `happened` | Reconciliation against provider evidence | Operations | **Operator cost incident, not customer overdraft** (`MT-15`). Block further dispatch on that route, reconcile, adjust; the real supplier usage is never erased | No |

### 4.1 Uncertain usage

| # | Failure point | Effect certainty | Detected by | Owner | Outcome | Auto-repair |
|---|---|---|---|---|---|---|
| UU-01 | Final usage never arrives | **`unknown`** | Attempt completeness state | Commerce | `UsagePending`. Reconcile from available provider evidence — **never zero, never a fabricated total** (`MT-12`) | Partly |
| UU-02 | Timeout after dispatch | **`unknown`** | Same | Commerce | `CostUnconfirmed`. **No blind redispatch and no repeat charge** (`MT-12`) | Partly |
| UU-03 | Reconciliation deadline passes unresolved | Still unknown | Deadline sweep | Commerce | **Release the customer hold with no surprise later debit; retain the unresolved supplier liability**; alert and restrict the route. The two deadlines are independent (`UC-02`) | Yes |
| UU-04 | Provider invoice diverges from computed cost | Partial | Invoice reconciliation (`MT-13`) | Commerce | Estimated, usage-confirmed and invoice-reconciled cost remain three distinguishable values (`UC-03`); the difference is a reconciliation adjustment, never a silent rewrite | No |

---

## 5. Sync change lifecycle

```
device A                       cloud                       device B
  │ local commit (journal + outbox, one transaction)          │
  ├── sync.pushChanges ─────────▶ inbox → apply → change feed │
  │                              ├── sync.changed (a hint) ──▶│
  │◀── ack: server revision      │                            ├── sync.pullChanges (cursor)
  │    outbox row cleared        │                            └── apply by (kind, id, rev)
```

| # | Failure point | Effect certainty | Detected by | Owner | Outcome | Auto-repair |
|---|---|---|---|---|---|---|
| SY-01 | Push sent; response lost | **`unknown`** | Outbox retry with the same idempotency key | Client | Re-push is a no-op server-side; **the outbox row is cleared only on a confirmed ack** | Yes |
| SY-02 | Applied server-side; client crashes before clearing the outbox | `happened` | Re-push idempotency | Client | Duplicate push recognised by revision; converges | Yes |
| SY-03 | `sync.changed` never delivered to device B | `happened` | Reconnect reconciliation, unconditional (`GP-03`) | Client B | Pulled from the last cursor | Yes |
| SY-04 | Sequence gap detected | `happened` | `seq` gap check | Client | **Scoped reconciliation, not a blanket resync** (`GP-02`); convergence is verified (`GP-04`) | Yes |
| SY-05 | Simultaneous edit on two devices | Both `happened` | Revision comparison | Client + Cloud | Conflict raised with **both branches retained**; resolution produces a **new revision**, never an overwrite | Partly — policy-dependent |
| SY-06 | Edit on A, delete on B | Both `happened` | Conflict handling | Cloud | **The delete does not silently win.** The conflict is surfaced with the edited content recoverable | No — user decides |
| SY-07 | Offline device returns after tombstone retention elapsed | `happened` | Cursor age check | Client | **Full resync required, not a delta** (`DL-02`), so a purged object cannot be resurrected | Yes |
| SY-08 | Object arrives referencing a blob not yet uploaded | Partial success | Availability state | Client | Object is present with the asset in an explicit unavailable state (`§7` there) — never a broken silent blank | Yes |
| SY-09 | Newer client writes a schema an older client cannot read | `happened` | Schema version on the object | Client | Older client shows the object as requiring an update, **preserves unknown fields on round trip**, and never writes a lossy version | Yes |
| SY-10 | Sync applied; local derived stores not updated | Partial success | Derived-store staleness key (`DS-01`) | Client | Rebuilt; **losing a derived store costs compute, never content** | Yes |

---

## 6. Asset and blob lifecycle

| # | Failure point | Effect certainty | Detected by | Owner | Outcome | Auto-repair |
|---|---|---|---|---|---|---|
| AS-01 | Multipart upload interrupted | `didNotHappen` (uncommitted) | Upload session state | Client | Resumed from the last completed part; an abandoned session expires and its parts are collected | Yes |
| AS-02 | Parts uploaded; commit never sent | **Partial — bytes stored, no object** | Upload-session expiry sweep | Cloud | Session expires; storage reclaimed. **An uncommitted upload is never referenceable** | Yes |
| AS-03 | Commit succeeds; hash mismatch | `didNotHappen` | Hash verification at commit | Cloud | **Rejected**; the client is told the content did not match | Yes |
| AS-04 | Object row written; blob missing in storage | Partial success | Data-health scan (`§9` there) | Cloud | Anomaly raised; restore from the second provider where a backup exists (`§10` there) | Partly |
| AS-05 | Last reference released; blob not collected | Partial | Reference-count invariant plus grace period (`DL-05`) | Cloud | Collected on the next pass; **never collected while the count is above zero or the grace period is unelapsed** | Yes |
| AS-06 | Reference released in error, then restored | `happened` | Grace period | Cloud | The grace period exists precisely so restore within it needs no re-upload | Yes |
| AS-07 | External asset moved or deleted by the user | `happened` outside ArcForges | Availability check | Client | Explicit `missing external` state with recovery affordances (`AT-07`). **ArcForges never silently uploads it to compensate** | No |

---

## 7. Deletion across systems

Five distinct operations (`§8` of the data-model overview), and the failure modes differ by operation.

| Operation | Scope | Reversible? |
|---|---|---|
| **Trash** | One aggregate, marked | Yes — restore preserves identity |
| **Purge** | Aggregate and children, permanent | No |
| **Unsync** | Cloud copy removed, local retained | Yes — re-sync |
| **Cloud deletion** | Workspace's cloud data | No |
| **Account deletion** | Cloud identity and all workspace data | No |

| # | Failure point | Effect certainty | Detected by | Owner | Outcome | Auto-repair |
|---|---|---|---|---|---|---|
| DE-01 | Purge completes in the primary store, not in the search index | **Partial — content unreadable but findable** | Deletion-completion invariant across every store | Owning product | Retried; **a permanent delete must remove search and vector entries** (`§13` of the sync architecture) | Yes |
| DE-02 | Purge completes locally; tombstone not propagated | Partial success | Tombstone propagation check | Cloud | Retried. Without the tombstone a returning device resurrects the object (`DL-01`) | Yes |
| DE-03 | Purge stuck part-way | Partial success | Data-health anomaly | Owning product | **Retried and reported, never silently abandoned** (`DL-09`) | Partly |
| DE-04 | Account deletion completes for identity, not for workspace data | **Partial — the most serious row here** | Deletion-completion invariant per store, plus an explicit end-to-end confirmation | Cloud | Continues to completion and is confirmed to the user only when every store reports done | Yes |
| DE-05 | Account deletion requested while a purchase is in flight | `unknown` | Pre-deletion check | Commerce + Cloud | Deletion waits on in-flight commercial operations. **Financial records are never deleted** (`DL-08`); they are retained under their own policy with identity minimised | Yes |
| DE-06 | Any deletion attempts to remove audit records | — | Constraint | Cloud | **Refused.** Audit retention is independent and policy-governed (`DL-07`) | N/A |
| DE-07 | Local data present after account deletion | `happened` as designed | — | — | **Correct behaviour, not a failure.** Local data is not part of account deletion (`DL-01` of the identity requirements, `I-016`); a separate explicit choice exists | N/A |
| DE-08 | Extension uninstall attempts to delete professional resources it created | — | Constraint | Extension host | **Prohibited** (`DL-06`). Uninstall removes the extension, never the user's work | N/A |

---

## 8. Device and session lifecycle

| # | Failure point | Effect certainty | Detected by | Owner | Outcome | Auto-repair |
|---|---|---|---|---|---|---|
| DV-01 | Device revoked while a bridge request is in flight | `unknown` | Authorization re-check at pull and at submit | Cloud + Desktop | The request is refused at the next boundary crossing; a result submitted by a revoked device is rejected | Yes |
| DV-02 | Device revoked while a realtime subscription is open | `happened` | Permission re-check on change (`SB-01`) | Cloud | **Delivery stops immediately and the client is told** | Yes |
| DV-03 | Device offline past a queued request's expiry | `didNotHappen` | Expiry | Cloud | Closed with a typed reason and shown to the requester (`BI-04`, `BI-05`) | Yes |
| DV-04 | Presence stale — device shows online but is gone | `unknown` | Heartbeat timeout | Cloud | Marked not eligible for remote targeting; **a request is never silently routed to a dead device** | Yes |
| DV-05 | Revoked device still holds cached content | `happened` | Local revocation check at start-up and on reconnect | Desktop | Cached acknowledged content is cleared per policy; **unacknowledged pending edits are preserved and offered for recovery or export** (`PE-03`). There is no provider credential on the device to clear (`BY-01`–`BY-04`) | Yes |

---

## 9. Who detects what

The same divergence must not be hunted by three mechanisms, and none must be hunted by none.

| Detector | Runs | Covers |
|---|---|---|
| **Foreground failure handling** | Per operation | Rows where the caller is still present: `PE-06`, `SY-01`, `AS-03` |
| **Expiry and sweep jobs** | Continuously | `PE-01`, `AI-08`, `AI-09`, `UU-03`, `AS-02`, `DV-03` |
| **Commerce reconciliation** | Scheduled, both directions | `PE-02`, `PE-07`, `PE-11`, `SU-01`, `SU-04`, `SU-07`, `AI-10`, `UU-01`–`UU-04` |
| **Sync reconciliation** | On reconnect and on gap | `SY-03`, `SY-04`, `SY-10` |
| **Data-health scans** | Scheduled | `AS-04`, `AS-05`, `DE-03` |
| **Completion invariants** | Per lifecycle | `PE-06`, `DE-01`, `DE-02`, `DE-04`, `CR-02` |
| **The user** | — | `SY-06`, `AS-07`, `SU-04` where a repair needs a decision |

| # | Rule |
|---|---|
| DT-01 | **Every failure row above names exactly one detector.** A row detected by nothing is an undetectable defect. |
| DT-02 | **A reconciliation job is idempotent and safe to run during an incident** (`RE-06`), which is exactly when it is most needed. |
| DT-03 | **A detector that finds nothing for a long period is itself suspect.** Reconciliation runs report their coverage, not only their findings, so a silently broken detector is visible. |
| DT-04 | **Anything raising an attention item attaches its evidence** — the records compared, the divergence, and the proposed repair — so a human decision is informed rather than guessed. |

---

## 10. Verification

Each row is release-gating (`XL-07`).

| # | Obligation | Where |
|---|---|---|
| LV-01 | A dropped purchase webhook is recovered by reconciliation with no user-visible loss of entitlement | `WP-42.03`, `WP-42.08` |
| LV-02 | A duplicated, out-of-order and replayed provider event each converge to one commercial state | `WP-42.03` |
| LV-03 | A paid order whose grant write failed converges to a granted entitlement without a second charge | `WP-42.03`, `WP-42.04` |
| LV-04 | An unmatched provider payment is quarantined and never grants access | `WP-42.03` |
| LV-05 | A refund and a chargeback each produce a revocation, never a deleted grant | `WP-42.09`, `WP-42.04` |
| LV-06 | A downgrade over quota permits read, download and delete and deletes nothing | `WP-42.06`, `WP-25.05` |
| LV-07 | Parallel runs against one workspace cannot collectively overdraw, and a crash releases the reservation | `WP-42.11`, `WP-43.05` |
| LV-19 | Official inference is refused with a full credit balance and no active paid service term | `WP-42.11` |
| LV-20 | Capacity recovers only over eligible paid intervals; a lapse accrues nothing and a renewal does not refill to full | `WP-42.11` |
| LV-21 | Clock rollback, restart, reconnect, a second device and a racing replica each fail to rewind the watermark or double-credit | `WP-42.11` |
| LV-22 | No path mints capacity above the burst, including a release and a refund | `WP-42.11` |
| LV-23 | A duplicate or reordered usage event replaces rather than sums, and never double-debits | `WP-43.07` |
| LV-24 | Missing final usage releases the customer hold at the deadline while retaining the supplier liability | `WP-43.07` |
| LV-25 | A paid term expiring mid-Task stops dispatch at a durable boundary with its reason | `WP-42.11` |
| LV-26 | A Task waiting for a device or an approval holds no included capacity | `WP-42.11`, `WP-16.05` |
| LV-27 | Configuration replacement mid-flight resets no usage, capacity, credit or hold, and changes no started Run's tariff | `WP-44.01`, `WP-42.11` |
| LV-08 | Provider invoice reconciliation detects an injected divergence | `WP-42.08`, `WP-43.02` |
| LV-09 | A lost push response, a crash before outbox clearing, and a re-push all converge with one effect | `WP-25.01`, `WP-25.02` |
| LV-10 | An induced sequence gap reconciles to verified convergence without a blanket resync | `WP-24.02`, `WP-24.03` |
| LV-11 | Edit-versus-delete surfaces a conflict with the edited content recoverable | `WP-25.03` |
| LV-12 | A device returning after tombstone retention performs a full resync and resurrects nothing | `WP-25.04`, `WP-25.07` |
| LV-13 | An interrupted multipart upload resumes; an abandoned one expires and reclaims storage | `WP-25.05` |
| LV-14 | A blob missing under a live object is detected by the data-health scan and restored | `WP-25.06`, `WP-46.01` |
| LV-15 | A purge removes primary, search and vector entries, and a partial purge is retried to completion | `WP-25.04`, `WP-19.00` |
| LV-16 | Account deletion is confirmed only when every store reports completion; financial records survive under their own retention, and local files are untouched | `WP-22.06`, `WP-42.09` |
| LV-17 | A revoked device cannot complete an in-flight bridge request or keep a subscription open | `WP-26.02`, `WP-24.01` |
| LV-18 | Every failure row in this document has a named test, and a row without one fails the completeness check | `WP-50.00` |
