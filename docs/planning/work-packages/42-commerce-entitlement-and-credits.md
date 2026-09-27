<a id="rule-wp-42"></a>

# WP-42 — Commerce, Entitlement and Credits

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Build the commercial system so that money is never lost, never double-charged and never silently wrong: a provider adapter boundary, a verify-everything event inbox, a derived entitlement resolver, credit lots with reserve-then-settle, three separate ledgers, and reconciliation as a first-class subsystem.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud; AI usage producer. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The provider adapter and its capability description; the product catalogue with versioned pricing policy; the purchase pipeline with intent, checkout and event inbox; normalised subscription state; the grant-based entitlement resolver and its distribution; quota and usage; credit lots with reservation and settlement; the three ledgers; reconciliation; refunds, disputes and commercial evidence; and the commercial go-live gates.

**Out of scope.** AI provider routing and tariffs (`43`) — the budget interface exists here. The account portal UI (`48`). Any mobile commerce surface, which is prohibited.

**Why this package exists.** [SQ-08](../implementation-sequence.md#rule-sq-08) places commerce late because entitlement, refunds, webhook idempotency and a real payout path must all exist before pricing can be published. [the mock policy](../implementation-sequence.md#3-what-may-be-mocked-and-what-may-not) also requires the webhook inbox, idempotency and reconciliation to be real even while provider payloads are fixtures.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/16-billing-and-commerce-architecture.md`](../../architecture/16-billing-and-commerce-architecture.md) | Module structure, purchase pipeline, resolver, ledgers, credits and reconciliation |
| [`../../requirements/04-commerce-entitlement-and-credits.md`](../../requirements/04-commerce-entitlement-and-credits.md) | The complete commercial requirement set |
| **[D-005](../../decisions/phase-1-foundation-decisions.md#rule-d-005)**, **[D-020](../../decisions/phase-1-foundation-decisions.md#rule-d-020)**, **[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[D-023](../../decisions/phase-1-foundation-decisions.md#rule-d-023)**, **[V-06](../../assurance/phase-1-official-verification.md#rule-v-06)**, **[V-07](../../assurance/phase-1-official-verification.md#rule-v-07)**, **[V-08](../../assurance/phase-1-official-verification.md#rule-v-08)** | Provider baseline, versioned economic policy, mobile posture, regional route and their gates |
| [WP-22](22-identity-workspace-and-device.md#rule-wp-22), [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) output | Workspace and billing identity separation; the API surface |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Paddle is the sole customer-facing Merchant of Record; Payoneer is a payout destination only** (**[D-005](../../decisions/phase-1-foundation-decisions.md#rule-d-005)**). |
| <a id="rule-br-02"></a>BR-02 | **Every commercial figure is versioned policy** (**[D-020](../../decisions/phase-1-foundation-decisions.md#rule-d-020)**), never a compiled constant and never retroactive. |
| <a id="rule-br-03"></a>BR-03 | **A provider event is a trigger, never unconditional belief.** The eight-step verification chain is mandatory. |
| <a id="rule-br-04"></a>BR-04 | **A success redirect is never payment authority.** |
| <a id="rule-br-05"></a>BR-05 | **Buyer identity is a stable internal billing identity, never an email address.** |
| <a id="rule-br-06"></a>BR-06 | **Entitlement is derived from immutable grants and revocations** and can always be rebuilt. |
| <a id="rule-br-07"></a>BR-07 | **Money and credit arithmetic is fixed-precision**; floating point is prohibited and policy-tested. |
| <a id="rule-br-08"></a>BR-08 | **Credits are reserved before execution and settled after**, with a hard stop at zero and no overdraft. |
| <a id="rule-br-09"></a>BR-09 | **The three ledgers are permanently separate** ([I-011](../../requirements/01-normative-glossary-and-invariants.md#rule-i-011)). |
| <a id="rule-br-10"></a>BR-10 | **Financial history is immutable**; corrections are new records. |
| <a id="rule-br-11"></a>BR-11 | **Reconciliation is a first-class subsystem**, and losing one webhook must never permanently cost a user their subscription. |
| <a id="rule-br-12"></a>BR-12 | **Settlement lags transactions materially** (**[V-07](../../assurance/phase-1-official-verification.md#rule-v-07)**); the model must not assume payout timing tracks transaction timing. |
| <a id="rule-br-13"></a>BR-13 | **No provider type or identifier format appears outside the provider adapter.** |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.Catalog/` | Offers, prices, price versions, policy versions |
| `src/Cloud/ArcForges.Cloud.Modules.Billing/` | Purchase intent, checkout, provider adapters, event inbox, reconciliation, evidence |
| `src/Cloud/ArcForges.Cloud.Modules.Entitlement/` | Grants, revocations, resolver, snapshot, version, quota, usage, credit lots, ledgers |
| `src/Contracts/Public/ArcForges.Contracts.PublicApi.Commerce/` | Entitlement and commerce DTOs |
| Cloud: `src/Cloud/ArcForges.Cloud.Modules.Commerce/` and Entitlement owner ports | Actual budget/credits/admission/settlement; no shared DesktopPlatform economics |
| `fixtures/provider/` | Recorded provider event fixtures for every event type |
| `tests/CloudIntegrationTests/Commerce/` | Idempotency, ordering, resolver, concurrency, precision and reconciliation suites |

**Major types introduced.** `Offer`, `Price`, `PriceVersion`, `PolicyVersion`, `BillingAccount`, `PurchaseIntent`, `CheckoutAttempt`, `ProviderEvent`, `ProviderEventInbox`, `Order`, `Payment`, `Subscription`, `SubscriptionState`, `EntitlementGrant`, `EntitlementRevocation`, `EntitlementSnapshot`, `EntitlementVersion`, `Quota`, `UsageCounter`, `CreditLot`, `CreditReservation`, `LedgerEntry`, `ReconciliationRun`, `RefundRequest`, `DisputeRecord`.

---

## 5. Required implementation work

<a id="rule-wp-42.00"></a>

### WP-42.00 — Provider adapter boundary

**What must be fully done.** The provider adapter with a typed capability description that the rest of the system reads rather than assuming. No provider type, identifier format or webhook shape appears outside the adapter, enforced by an architecture test.

**Testing requirements.** A containment architecture test with a negative fixture; capability-driven behaviour tests where the system adapts to a capability being absent.

**Completion gate.** No provider type appears outside the adapter, and the system adapts to declared capabilities rather than assuming them.

<a id="rule-wp-42.01"></a>

### WP-42.01 — Catalogue and versioned policy

**What must be fully done.** Offers and prices as versioned policy with effective dates. A price change never alters a historical order or a settled charge. Every figure is policy data, not code.

**Testing requirements.** A retroactivity negative test; a policy-version resolution test; a scan asserting no commercial constant is compiled into code.

**Completion gate.** No commercial figure is compiled into code, and a price change never alters historical records.

<a id="rule-wp-42.02"></a>

### WP-42.02 — Purchase pipeline

**What must be fully done.** Purchase intent as the idempotency anchor; checkout attempts carrying internal identifiers as provider metadata; hosted checkout with no payment instrument field anywhere in ArcForges; a confirming state after redirect that waits for verified events.

**Testing requirements.** Double-submission producing one order; a redirect-forgery negative test; a metadata-completeness assertion; an expired-attempt reconciliation test.

**Completion gate.** One intent yields at most one order, a forged redirect grants nothing, and every checkout carries complete internal metadata.

<a id="rule-wp-42.03"></a>

### WP-42.03 — Provider event inbox

**What must be fully done.** Persist-before-process; signature verification mandatory; idempotency by event type and identifier; asynchronous processing; the fixed eight-step verification chain; out-of-order handling by state; quarantine with alerting for unprocessable events; raw payload retention; and idempotent replay.

**Testing requirements.** Duplicate, out-of-order, unsigned, unknown-product and replay tests; a backlog alert test; a convergence test replaying the inbox from a point in time.

**Completion gate.** Duplicate and out-of-order events converge correctly, unsigned events are rejected and recorded, and replaying the inbox reproduces the same commercial state.

<a id="rule-wp-42.04"></a>

### WP-42.04 — Entitlement resolver

**What must be fully done.** Immutable grants and revocations; a resolver producing a snapshot with per-capability reasons and a version; normalised subscription state driven by paid-through rather than a provider status string; the four entitlement kinds combined by explicit rules; deterministic evaluation against a single authoritative time source.

**Testing requirements.** A rebuild-equivalence test over fixture accounts; a reason-coverage test; a combination matrix; a clock-determinism test.

**Completion gate.** **Rebuilding a snapshot from grants and revocations always equals the stored snapshot**, and every capability carries a reason.

<a id="rule-wp-42.05"></a>

### WP-42.05 — Distribution and enforcement

**What must be fully done.** Clients read entitlement with its version and cache it; realtime notification is a refresh hint only; offline staleness is bounded with defined behaviour; enforcement for anything with cost is server-side; loss of entitlement never deletes local data.

**Testing requirements.** A hint-not-authority test; an offline-staleness behaviour test; a client-bypass negative test; a local-data-survival test.

**Completion gate.** A client never infers entitlement from an observed event, server-side enforcement cannot be bypassed, and losing entitlement never deletes local data.

<a id="rule-wp-42.06"></a>

### WP-42.06 — Quota, usage and storage accounting

**What must be fully done.** Consume the [WP-21.06](21-cloud-host-and-persistence.md#rule-wp-21.06) quota kernel; resolve versioned grants without resetting gauges or outstanding reservations. Cover staging, committed/history/trash storage, simulation and egress in separate units.  Quota as limit and usage as measurement in separate stores; reset boundaries tied to the entitlement period; storage accounting computed from committed objects; exceeding a quota producing a typed, explained refusal with a remediation path.

**Testing requirements.** Race admissions, quota downgrade, repeated cancellation, GC timeout and period rollover with held old-period use.  Boundary-reset tests; an accounting comparison against actual committed storage; a refusal-message test.

**Completion gate.** The displayed usage is reconciled from measured facts and cannot authorise an unreserved operation.  Usage resets on the entitlement boundary, accounting matches committed storage, and quota refusals explain the remediation.

<a id="rule-wp-42.07"></a>

### WP-42.07 — Credits

**What must be fully done.** Credit lots with **two** classes — `purchased` (no expiry, conserved) and `compensation` (disclosed expiry) — in **integer micro-credits**, never money ([CD-01](../../architecture/16-billing-and-commerce-architecture.md#rule-cd-01)). **`subscriptionAllowance` is retired**: included capacity is a replenishing bucket, not a lot, and **no allowance is issued monthly, annually or on any schedule** ([CD-02](../../architecture/16-billing-and-commerce-architecture.md#rule-cd-02), [RF-07](../../architecture/16-billing-and-commerce-architecture.md#rule-rf-07)). Funding order capacity → compensation (earliest expiry) → purchased (oldest acquisition), the last only under an explicit extra-usage authorisation ([CD-05](../../architecture/16-billing-and-commerce-architecture.md#rule-cd-05)). **One reservation spanning both pools**, keyed on the logical request ([FU-01](../../architecture/data-model/01-cloud-data-model.md#rule-fu-01), [FU-02](../../architecture/data-model/01-cloud-data-model.md#rule-fu-02)); reserve, settle and release with atomic accounting; reservation expiry sweeping; hard stop at zero; refund hold; separate presentation of allowance and purchased credits.

**Testing requirements.** Lot-ordering matrix; concurrency test asserting no overdraft; reservation-expiry sweep; a hard-stop test; a refund-hold test; a fixed-precision policy test.

**Completion gate.** **Concurrent runs never overdraw**, the balance never goes negative, orphaned reservations are released, and no floating-point path exists in money or credit arithmetic.

<a id="rule-wp-42.08"></a>

### WP-42.08 — Ledgers and reconciliation

**What must be fully done.** The three ledgers as separate append-only stores with their own reconciliation. Scheduled two-way reconciliation against the provider with typed repair actions expressed as new records. Divergence above a threshold alerts. Reconciliation is idempotent and safe during an incident.

**Testing requirements.** A dropped-webhook repair test; a duplicated-order repair test; a provider-side-change repair test; an immutability test asserting history cannot be edited; a ledger-separation test.

**Completion gate.** **A dropped webhook is recovered by reconciliation without editing history**, and the three ledgers remain provably separate.

<a id="rule-wp-42.09"></a>

### WP-42.09 — Refunds, disputes and evidence

**What must be fully done.** Refund with entitlement rollback verified; dispute records; commercial evidence export covering order, payments, provider events, entitlement history and usage for a stated period, free of payment instrument data.

**Testing requirements.** A refund-with-rollback test; an evidence completeness and reproducibility test; a payment-data absence scan.

**Completion gate.** A refund rolls entitlement back correctly, and an evidence export is complete, reproducible and free of payment instrument data.

<a id="rule-wp-42.11"></a>

### WP-42.11 — Service term and replenishing capacity

**What must be fully done.** Advance the capacity bucket before every hold/balance/term/assignment mutation. Implement immutable term actions, single selected offer assignment and chronological policy joins, including overlap, delayed verification, revocation and renewal.  `entitlement.service_term` as an interval with the four permitted sources, keyed on **`(kind, period_ref)`** — the **paid period's** own identity, not the subscription's ([TM-01](../../architecture/data-model/01-cloud-data-model.md#rule-tm-01)–[TM-05](../../architecture/data-model/01-cloud-data-model.md#rule-tm-05)). The three identities stay separate: `subscription_ref` is stable across renewals, `period_ref` identifies one paid interval, and provider-event deduplication lives in `commerce.provider_event` ([TM-02](../../architecture/data-model/01-cloud-data-model.md#rule-tm-02)). A renewal therefore carries a **new** `period_ref` and creates a new row, while a replayed provider event extends nothing twice; the effective term is the union of overlapping and abutting intervals ([TM-01](../../architecture/data-model/01-cloud-data-model.md#rule-tm-01)), and a plan change **supersedes** rather than edits ([TM-04](../../architecture/data-model/01-cloud-data-model.md#rule-tm-04)). `entitlement.capacity_bucket` with the refill algorithm of `§7.2` of the commerce architecture: per-period saturating accrual whose result is **independent of evaluation frequency** ([RF-04](../../architecture/16-billing-and-commerce-architecture.md#rule-rf-04)), a monotonic durable watermark, an exact rational carry across period boundaries, a reduction that stops accrual without clawing back ([RF-05](../../architecture/16-billing-and-commerce-architecture.md#rule-rf-05)), and parameters read from immutable `capacity_policy_period` history rather than stored on the bucket. Idempotent initialisation **once per contiguous run** ([RF-08](../../architecture/16-billing-and-commerce-architecture.md#rule-rf-08)), computed from the terms rather than a flag. `entitlement.capacity_reservation` recording its three funding sources so settlement debits and releases against the same ones. Atomic admission with the **service-term check first**, in the shared unit of work of `§6.1.1` of the data-model overview, committing before dispatch.

**Testing requirements.** Assert the full-hold t=0→consume t=10→read t=11 result is 1 regardless of intervening reads; test fractional saturation, changed plan, overlap, genuine gap, unchanged renewal and grandfathered above-ceiling balance.  Official inference refused with a full credit balance and no active term; **a renewal of the same subscription creating a second term row without violating the key** ([TM-02](../../architecture/data-model/01-cloud-data-model.md#rule-tm-02)); a replayed provider event creating nothing; a plan change superseding rather than editing; contiguous renewal not refilling to full while a term after a genuine gap initialises once ([RF-08](../../architecture/16-billing-and-commerce-architecture.md#rule-rf-08)); **the refill fixture of [CT-13](../../architecture/16-billing-and-commerce-architecture.md#rule-ct-13) — identical result whether refill runs once or a thousand times over an interval containing a ceiling raise, a ceiling reduction and a rate change, with the worked case asserting 11 at *t*=11 rather than 21 or 12**; clock rollback, restart, reconnect, a second device and a racing replica each failing to rewind the watermark or double-credit; a ceiling reduction preserving held funding: reserve 10, reduce burst to 3, cancel without use and recover the original 10 with no further above-ceiling accrual; a purchased-credit refund creating no included capacity; a request whose bound can never fit rejected immediately; a waiting-for-device turn holding no included capacity; extra credits spent only after opt-in and never beyond the stated budget; **a ledger constraint test asserting `customerCredit` rows carry micro-credits with no currency and the other two carry money with a currency, and that no query sums the two**.

**Completion gate.** No later hold value or current offer is applied retrospectively to prior time; replay and read frequency cannot mint capacity.  **A credit balance never authorises inference**; a renewal is recordable and contiguity is computed from the terms; **the refill result does not depend on how often refill runs**; no path mints capacity above the ceiling in force and no reduction claws back; and customer, supplier and payment amounts remain in their own units throughout.

<a id="rule-wp-42.10"></a>

### WP-42.10 — Technical commerce closure and live gate staging

**What must be fully done.** Complete deterministic provider normalization and sandbox lifecycle proof. No official free tier, grant kinds and SubscriptionState exactly match requirements 04; plan changes start next term without proration. Preserve all live-payment/payout/refund/merchant gates for WP50 after WP48 account checkout and operations are available.

**Testing requirements.** Full synthetic/provider-sandbox ledger vectors including no-term, cancellation, lost result, unknown exposure and future-effective changes.

**Completion gate.** Technical commerce gates pass; real receipt/payout evidence is explicitly pending at WP50, never claimed from sandbox.

<a id="rule-wp-42.90"></a>
### WP-42.90 — Verify the owned artifact and real integration

**What must be fully done.** Retain current subscription/admission/credit/quota/settlement/reversal rules. Bind the CF usage/config identities and exact quantities; keep synthetic price fixtures distinct from live configuration. Do not add mandatory prepayment.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Existing concurrent admission/idempotent settlement/reversal/storage-accounting cases; keep [WP-42.11](#rule-wp-42.11) evidence and its order before [WP-42.10](#rule-wp-42.10).

**Completion gate.** Existing concurrent admission/idempotent settlement/reversal/storage-accounting cases; keep [WP-42.11](#rule-wp-42.11) evidence and its order before [WP-42.10](#rule-wp-42.10). Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

**Operator contract closure.** Consume [registry04 §9](../../architecture/contracts/04-protobuf-wire-registry.md#9-operator-control-and-separate-identity-boundary) and [model01 operator state](../../architecture/data-model/01-cloud-data-model.md#operator-proposal-approval-and-financial-owner-closure). Generate/implement every operation exactly once with its eight authorization fields, operator scope and [OC-03](../../requirements/10-distribution-update-and-support.md#rule-oc-03) role binding. Public customer/PAT/agent access refuses. Verify distinct approver, stale hash/revision/configuration, role revocation, expiry, concurrent consumption and lost receipt; no direct SQL or public-SDK operator import. WP03 produces schema/negative vectors, WP23 real identity/dispatch conformance, WP42 the financial owners, WP44 configuration/policy owners, and WP45 the real console join. Earlier packages retain their named fixture boundary until the existing downstream join.

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

Acceptance includes every amended §5 producer/consumer and [WP-42.90](#rule-wp-42.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

**[WP-42.11](#rule-wp-42.11) producer evidence.** Real payment-event reconciliation, immutable term/offer history, exact refill/hold fixtures and durable multi-replica restart evidence. This producer must pass before commercial go-live; later AI/configuration producers supply their remaining shared-gate evidence.

| Evidence | Produced by |
|---|---|
| Provider containment and capability-adaptation results | [WP-42.00](#rule-wp-42.00) |
| Retroactivity negative test and compiled-constant scan | [WP-42.01](#rule-wp-42.01) |
| Double-submission, redirect-forgery and metadata results | [WP-42.02](#rule-wp-42.02) |
| Duplicate, out-of-order, unsigned and replay convergence results | [WP-42.03](#rule-wp-42.03) |
| Resolver rebuild equivalence and reason coverage | [WP-42.04](#rule-wp-42.04) |
| Hint-not-authority, bypass and local-data results | [WP-42.05](#rule-wp-42.05) |
| Boundary reset, accounting comparison and refusal results | [WP-42.06](#rule-wp-42.06) |
| Lot ordering, concurrency, sweep, hard-stop and precision results | [WP-42.07](#rule-wp-42.07) |
| Repair-without-edit and ledger-separation results | [WP-42.08](#rule-wp-42.08) |
| Refund rollback and evidence export results | [WP-42.09](#rule-wp-42.09) |
| Technical commerce receipts: ledger integrity, test-mode charge/refund/webhook replay, period/renewal/exclusivity and unknown effects; activation checklist handed to WP48/WP50. Actual checkout and received payout are verified there | [WP-42.10](#rule-wp-42.10) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-42.90](#rule-wp-42.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-42.90](#rule-wp-42.90) and all inherited domain-specific gates must pass on the same candidate closure. Existing concurrent admission/idempotent settlement/reversal/storage-accounting cases; keep [WP-42.11](#rule-wp-42.11) evidence and its order before [WP-42.10](#rule-wp-42.10).

**Producer completion.** [WP-42.11](#rule-wp-42.11) must pass with the explicit §7 artifacts above; it is not optional because other package checks pass.

**[PG-16](../../assurance/open-gates-register.md#rule-pg-16) evidence:** [WP-42.11](#rule-wp-42.11) — Durable term/capacity/refill state survives concurrent requests and restart without double grant; combine with configuration activation evidence from package 44. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-13](../../assurance/open-gates-register.md#rule-pg-13) evidence:** [WP-42.11](#rule-wp-42.11) — Real payment event normalized through persistent term/capacity code; combine with provider usage and the exact monetary fixture from package 43. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-10](../../assurance/open-gates-register.md#rule-pg-10) evidence:** [WP-42.10](#rule-wp-42.10) — Recorded payment-provider test-environment scenarios and contract fixtures, including event duplication/loss; retain the separate real commercial go-live evidence. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

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
11. Test-mode commerce and the activation checklist are complete. Production merchant eligibility, checkout/refund and received-payout evidence remain at WP50, including [L-30](../../assurance/release-gates.md#rule-l-30); WP42 does not claim [VG-10](../../assurance/open-gates-register.md#rule-vg-10)/[VG-11](../../assurance/open-gates-register.md#rule-vg-11) closed. The regional route remains disabled pending [VG-12](../../assurance/open-gates-register.md#rule-vg-12).

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [COM.01](../delivery/lanes/commerce.md#task-com-01) | [WP-42.00](42-commerce-entitlement-and-credits.md#rule-wp-42.00) (full) | none |
| [COM.02](../delivery/lanes/commerce.md#task-com-02) | [WP-42.01](42-commerce-entitlement-and-credits.md#rule-wp-42.01) (full) | none |
| [COM.03](../delivery/lanes/commerce.md#task-com-03) | [WP-42.02](42-commerce-entitlement-and-credits.md#rule-wp-42.02) (full) | [CLOUD.24](../delivery/lanes/cloud.md#task-cloud-24) (artifact) |
| [COM.04](../delivery/lanes/commerce.md#task-com-04) | [WP-42.03](42-commerce-entitlement-and-credits.md#rule-wp-42.03) (full) | none |
| [COM.05](../delivery/lanes/commerce.md#task-com-05) | [WP-42.04](42-commerce-entitlement-and-credits.md#rule-wp-42.04) (full) | none |
| [COM.06](../delivery/lanes/commerce.md#task-com-06) | [WP-42.05](42-commerce-entitlement-and-credits.md#rule-wp-42.05) (full) | [CLOUD.23](../delivery/lanes/cloud.md#task-cloud-23) (artifact) |
| [COM.07](../delivery/lanes/commerce.md#task-com-07) | [WP-42.06](42-commerce-entitlement-and-credits.md#rule-wp-42.06) (full) | [CLOUD.07](../delivery/lanes/cloud.md#task-cloud-07) (artifact) |
| [COM.08](../delivery/lanes/commerce.md#task-com-08) | [WP-42.07](42-commerce-entitlement-and-credits.md#rule-wp-42.07) (full) | none |
| [COM.09](../delivery/lanes/commerce.md#task-com-09) | [WP-42.08](42-commerce-entitlement-and-credits.md#rule-wp-42.08) (full)<br>[WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure; three ledgers with unresolved holds through their existing deadline ([P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure; three ledgers with unresolved holds through their existing deadline)<br>[WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (package-level obligation contribution) | none |
| [COM.10](../delivery/lanes/commerce.md#task-com-10) | [WP-42.09](42-commerce-entitlement-and-credits.md#rule-wp-42.09) (full) | none |
| [COM.11](../delivery/lanes/commerce.md#task-com-11) | [WP-42.11](42-commerce-entitlement-and-credits.md#rule-wp-42.11) (service_term interval model keyed on (kind, period_ref); the three separated identities (subscription_ref stable / period_ref per paid interval / provider-event dedup in commerce.provider_event); union-of-overlap effective term; plan-change supersede. Capacity bucket/refill/reservation half split to COM.12.) | none |
| [COM.12](../delivery/lanes/commerce.md#task-com-12) | [WP-42.11](42-commerce-entitlement-and-credits.md#rule-wp-42.11) (entitlement.capacity_bucket refill algorithm (§7.2), capacity_policy_period history, capacity_reservation with three funding sources, idempotent once-per-contiguous-run initialisation, and atomic admission with the service-term check first) | none |
| [COM.13](../delivery/lanes/commerce.md#task-com-13) | [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) Operator contract closure — financial owners (grant/revokeGrant/issueCredit/adjustCredit/refund) (operator contract closure; financial-owner RPC implementations: grant, revokeGrant, issueCredit, adjustCredit, refund) | [CON.14](../delivery/lanes/contracts.md#task-con-14) (contract), [CLOUD.21](../delivery/lanes/cloud.md#task-cloud-21) (artifact) |
| [COM.14](../delivery/lanes/commerce.md#task-com-14) | [WP-42.10](42-commerce-entitlement-and-credits.md#rule-wp-42.10) (full)<br>[WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (package-level obligation contribution) | none |
| [COM.15](../delivery/lanes/commerce.md#task-com-15) | [WP-42.90](42-commerce-entitlement-and-credits.md#rule-wp-42.90) (full)<br>[WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure; active Pass/subscription mutual exclusion, no immediate proration, exact renewal/reset periods ([P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure; active Pass/subscription mutual exclusion, no immediate proration, exact renewal/reset periods)<br>[WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (package-level obligation contribution) | none |

**Consumers outside this package:** [AIR.02](../delivery/lanes/ai-routing.md#task-air-02), [CLOUD.63](../delivery/lanes/cloud.md#task-cloud-63), [CLOUD.64](../delivery/lanes/cloud.md#task-cloud-64), [CLOUD.66](../delivery/lanes/cloud.md#task-cloud-66), [HAR.02](../delivery/lanes/harness.md#task-har-02), [HAR.06](../delivery/lanes/harness.md#task-har-06), [OPS.05](../delivery/lanes/operations.md#task-ops-05), [OPS.13](../delivery/lanes/operations.md#task-ops-13), [POL.04](../delivery/lanes/policy.md#task-pol-04), [REL.06](../delivery/lanes/release.md#task-rel-06), [REL.08](../delivery/lanes/release.md#task-rel-08), [SIM.04](../delivery/lanes/simulator.md#task-sim-04), [SIM.07](../delivery/lanes/simulator.md#task-sim-07), [WEB.14](../delivery/lanes/web.md#task-web-14), [WEB.29](../delivery/lanes/web.md#task-web-29).

<!-- delivery-graph:end -->

## [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure

Test active Pass/subscription mutual exclusion, no immediate proration, exact renewal/reset periods and three ledgers with unresolved holds through their existing deadline. The referenced normative profile and producer stage matrix are binding inputs. Record independent positive/negative vectors and actual owner integration at this WP's assigned stage; a mock cannot close a real-provider/device requirement.
