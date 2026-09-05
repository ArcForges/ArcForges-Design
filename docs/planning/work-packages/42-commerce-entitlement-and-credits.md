# WP-42 — Commerce, Entitlement and Credits

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `22`, `23` · Downstream: `43`, `44`, `48`

> **Goal.** Build the commercial system so that money is never lost, never double-charged and never silently wrong: a provider adapter boundary, a verify-everything event inbox, a derived entitlement resolver, credit lots with reserve-then-settle, three separate ledgers, and reconciliation as a first-class subsystem.

---

## 1. Scope and purpose

**In scope.** The provider adapter and its capability description; the product catalogue with versioned pricing policy; the purchase pipeline with intent, checkout and event inbox; normalised subscription state; the grant-based entitlement resolver and its distribution; quota and usage; credit lots with reservation and settlement; the three ledgers; reconciliation; refunds, disputes and commercial evidence; and the commercial go-live gates.

**Out of scope.** AI provider routing and tariffs (`43`) — the budget interface exists here. The account portal UI (`48`). Any mobile commerce surface, which is prohibited.

**Why this package exists.** `SQ-08` places commerce late because entitlement, refunds, webhook idempotency and a real payout path must all exist before pricing can be published. `I2 §V` also requires the webhook inbox, idempotency and reconciliation to be real even while provider payloads are fixtures.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/16-billing-and-commerce-architecture.md`](../../architecture/16-billing-and-commerce-architecture.md) | Module structure, purchase pipeline, resolver, ledgers, credits and reconciliation |
| [`../../requirements/04-commerce-entitlement-and-credits.md`](../../requirements/04-commerce-entitlement-and-credits.md) | The complete commercial requirement set |
| **D-005**, **D-020**, **D-022**, **D-023**, **V-06**, **V-07**, **V-08** | Provider baseline, versioned economic policy, mobile posture, regional route and their gates |
| `WP-22`, `WP-23` output | Workspace and billing identity separation; the API surface |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Paddle is the sole customer-facing Merchant of Record; Payoneer is a payout destination only** (**D-005**). |
| BR-02 | **Every commercial figure is versioned policy** (**D-020**), never a compiled constant and never retroactive. |
| BR-03 | **A provider event is a trigger, never unconditional belief.** The eight-step verification chain is mandatory. |
| BR-04 | **A success redirect is never payment authority.** |
| BR-05 | **Buyer identity is a stable internal billing identity, never an email address.** |
| BR-06 | **Entitlement is derived from immutable grants and revocations** and can always be rebuilt. |
| BR-07 | **Money and credit arithmetic is fixed-precision**; floating point is prohibited and policy-tested. |
| BR-08 | **Credits are reserved before execution and settled after**, with a hard stop at zero and no overdraft. |
| BR-09 | **The three ledgers are permanently separate** (`I-011`). |
| BR-10 | **Financial history is immutable**; corrections are new records. |
| BR-11 | **Reconciliation is a first-class subsystem**, and losing one webhook must never permanently cost a user their subscription. |
| BR-12 | **Settlement lags transactions materially** (**V-07**); the model must not assume payout timing tracks transaction timing. |
| BR-13 | **No provider type or identifier format appears outside the provider adapter.** |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.Catalog/` | Offers, prices, price versions, policy versions |
| `src/Cloud/ArcForges.Cloud.Modules.Billing/` | Purchase intent, checkout, provider adapters, event inbox, reconciliation, evidence |
| `src/Cloud/ArcForges.Cloud.Modules.Entitlement/` | Grants, revocations, resolver, snapshot, version, quota, usage, credit lots, ledgers |
| `src/Contracts/Public/ArcForges.Contracts.PublicApi.Commerce/` | Entitlement and commerce DTOs |
| `src/BuildingBlocks/ArcForges.Execution.Budget/` | The budget interface implemented against real credits |
| `fixtures/provider/` | Recorded provider event fixtures for every event type |
| `tests/CloudIntegrationTests/Commerce/` | Idempotency, ordering, resolver, concurrency, precision and reconciliation suites |

**Major types introduced.** `Offer`, `Price`, `PriceVersion`, `PolicyVersion`, `BillingAccount`, `PurchaseIntent`, `CheckoutAttempt`, `ProviderEvent`, `ProviderEventInbox`, `Order`, `Payment`, `Subscription`, `SubscriptionState`, `EntitlementGrant`, `EntitlementRevocation`, `EntitlementSnapshot`, `EntitlementVersion`, `Quota`, `UsageCounter`, `CreditLot`, `CreditReservation`, `LedgerEntry`, `ReconciliationRun`, `RefundRequest`, `DisputeRecord`.

---

## 5. Required implementation work

### WP-42.00 — Provider adapter boundary

**What must be fully done.** The provider adapter with a typed capability description that the rest of the system reads rather than assuming. No provider type, identifier format or webhook shape appears outside the adapter, enforced by an architecture test.

**Testing requirements.** A containment architecture test with a negative fixture; capability-driven behaviour tests where the system adapts to a capability being absent.

**Completion gate.** No provider type appears outside the adapter, and the system adapts to declared capabilities rather than assuming them.

### WP-42.01 — Catalogue and versioned policy

**What must be fully done.** Offers and prices as versioned policy with effective dates. A price change never alters a historical order or a settled charge. Every figure is policy data, not code.

**Testing requirements.** A retroactivity negative test; a policy-version resolution test; a scan asserting no commercial constant is compiled into code.

**Completion gate.** No commercial figure is compiled into code, and a price change never alters historical records.

### WP-42.02 — Purchase pipeline

**What must be fully done.** Purchase intent as the idempotency anchor; checkout attempts carrying internal identifiers as provider metadata; hosted checkout with no payment instrument field anywhere in ArcForges; a confirming state after redirect that waits for verified events.

**Testing requirements.** Double-submission producing one order; a redirect-forgery negative test; a metadata-completeness assertion; an expired-attempt reconciliation test.

**Completion gate.** One intent yields at most one order, a forged redirect grants nothing, and every checkout carries complete internal metadata.

### WP-42.03 — Provider event inbox

**What must be fully done.** Persist-before-process; signature verification mandatory; idempotency by event type and identifier; asynchronous processing; the fixed eight-step verification chain; out-of-order handling by state; quarantine with alerting for unprocessable events; raw payload retention; and idempotent replay.

**Testing requirements.** Duplicate, out-of-order, unsigned, unknown-product and replay tests; a backlog alert test; a convergence test replaying the inbox from a point in time.

**Completion gate.** Duplicate and out-of-order events converge correctly, unsigned events are rejected and recorded, and replaying the inbox reproduces the same commercial state.

### WP-42.04 — Entitlement resolver

**What must be fully done.** Immutable grants and revocations; a resolver producing a snapshot with per-capability reasons and a version; normalised subscription state driven by paid-through rather than a provider status string; the four entitlement kinds combined by explicit rules; deterministic evaluation against a single authoritative time source.

**Testing requirements.** A rebuild-equivalence test over fixture accounts; a reason-coverage test; a combination matrix; a clock-determinism test.

**Completion gate.** **Rebuilding a snapshot from grants and revocations always equals the stored snapshot**, and every capability carries a reason.

### WP-42.05 — Distribution and enforcement

**What must be fully done.** Clients read entitlement with its version and cache it; realtime notification is a refresh hint only; offline staleness is bounded with defined behaviour; enforcement for anything with cost is server-side; loss of entitlement never deletes local data.

**Testing requirements.** A hint-not-authority test; an offline-staleness behaviour test; a client-bypass negative test; a local-data-survival test.

**Completion gate.** A client never infers entitlement from an observed event, server-side enforcement cannot be bypassed, and losing entitlement never deletes local data.

### WP-42.06 — Quota, usage and storage accounting

**What must be fully done.** Quota as limit and usage as measurement in separate stores; reset boundaries tied to the entitlement period; storage accounting computed from committed objects; exceeding a quota producing a typed, explained refusal with a remediation path.

**Testing requirements.** Boundary-reset tests; an accounting comparison against actual committed storage; a refusal-message test.

**Completion gate.** Usage resets on the entitlement boundary, accounting matches committed storage, and quota refusals explain the remediation.

### WP-42.07 — Credits

**What must be fully done.** Credit lots with three classes and their distinct rules; earliest-expiry-first consumption within class priority; monthly allowance issue for annual subscriptions; reserve, settle and release with atomic accounting; reservation expiry sweeping; hard stop at zero; refund hold; separate presentation of allowance and purchased credits.

**Testing requirements.** Lot-ordering matrix; concurrency test asserting no overdraft; reservation-expiry sweep; a hard-stop test; a refund-hold test; a fixed-precision policy test.

**Completion gate.** **Concurrent runs never overdraw**, the balance never goes negative, orphaned reservations are released, and no floating-point path exists in money or credit arithmetic.

### WP-42.08 — Ledgers and reconciliation

**What must be fully done.** The three ledgers as separate append-only stores with their own reconciliation. Scheduled two-way reconciliation against the provider with typed repair actions expressed as new records. Divergence above a threshold alerts. Reconciliation is idempotent and safe during an incident.

**Testing requirements.** A dropped-webhook repair test; a duplicated-order repair test; a provider-side-change repair test; an immutability test asserting history cannot be edited; a ledger-separation test.

**Completion gate.** **A dropped webhook is recovered by reconciliation without editing history**, and the three ledgers remain provably separate.

### WP-42.09 — Refunds, disputes and evidence

**What must be fully done.** Refund with entitlement rollback verified; dispute records; commercial evidence export covering order, payments, provider events, entitlement history and usage for a stated period, free of payment instrument data.

**Testing requirements.** A refund-with-rollback test; an evidence completeness and reproducibility test; a payment-data absence scan.

**Completion gate.** A refund rolls entitlement back correctly, and an evidence export is complete, reproducible and free of payment instrument data.

### WP-42.10 — Go-live gates

**What must be fully done.** Supplier onboarding and account approval; sanctions and export screening for the intended market set; payout eligibility and receiving-currency confirmation; one real payment, subscription, renewal, cancellation, reactivation and refund; the webhook duplicate-and-loss test; the reconciliation repair test; and a **completed payout received**. The regional route stays disabled by configuration until its own gates are met.

**Testing requirements.** Recorded evidence per gate; a configuration assertion that the regional route is disabled.

**Completion gate.** Every commercial go-live gate is satisfied with recorded evidence, **including a payout actually received** — satisfying `VG-10` and `VG-11`. Until then the correct statement is "technical integration complete", not "the commercial loop is closed". The regional route remains disabled pending `VG-12`.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Commerce schemas: catalogue, orders, events, grants, credits, ledgers |
| Protocol | Entitlement and commerce contracts |
| UI | Purchase, subscription, credits and usage surfaces (portal in `48`) |
| Security | Commercial mutations are R2-or-above and fully audited |
| Platform | No commerce surface on mobile |
| Migration | Commercial schema changes are the highest-consequence migrations |
| Compatibility | Entitlement contract versioning across all clients |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Provider containment and capability-adaptation results | `WP-42.00` |
| Retroactivity negative test and compiled-constant scan | `WP-42.01` |
| Double-submission, redirect-forgery and metadata results | `WP-42.02` |
| Duplicate, out-of-order, unsigned and replay convergence results | `WP-42.03` |
| Resolver rebuild equivalence and reason coverage | `WP-42.04` |
| Hint-not-authority, bypass and local-data results | `WP-42.05` |
| Boundary reset, accounting comparison and refusal results | `WP-42.06` |
| Lot ordering, concurrency, sweep, hard-stop and precision results | `WP-42.07` |
| Repair-without-edit and ledger-separation results | `WP-42.08` |
| Refund rollback and evidence export results | `WP-42.09` |
| Recorded go-live gate evidence including the received payout | `WP-42.10` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. No provider type appears outside the adapter; the system adapts to declared provider capabilities.
2. No commercial figure is compiled into code; a price change never alters historical records.
3. One purchase intent yields at most one order; a forged redirect grants nothing.
4. Duplicate and out-of-order provider events converge; unsigned events are rejected; inbox replay reproduces the same state.
5. **Rebuilding an entitlement snapshot from grants and revocations always equals the stored snapshot**, with a reason per capability.
6. Clients never infer entitlement from observed events; server-side enforcement cannot be bypassed; losing entitlement never deletes local data.
7. Usage resets on the entitlement boundary; storage accounting matches committed storage.
8. **Concurrent runs never overdraw; the balance never goes negative; no floating-point path exists in money or credit arithmetic.**
9. **A dropped webhook is recovered by reconciliation without editing history**; the three ledgers remain provably separate.
10. A refund rolls entitlement back correctly; evidence export is complete and free of payment instrument data.
11. Every commercial go-live gate is satisfied **including a payout actually received** — satisfying `VG-10` and `VG-11`; the regional route remains disabled pending `VG-12`.

---

## 9. Dependencies

**Upstream.** `22` (workspace and billing identity), `23` (the API surface).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `43` — Managed AI | Real credits behind the budget interface |
| `44` — Policy | Entitlement as one of the four boundaries |
| `48` — Account portal | The commercial model it presents |
