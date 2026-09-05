# Billing and Commerce Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **D-005** (provider baseline), **D-020** (versioned economic policy), **D-022** (mobile commerce posture), **D-023** (Mainland China route), **V-07** (settlement timing)
> Companions: [`../requirements/04-commerce-entitlement-and-credits.md`](../requirements/04-commerce-entitlement-and-credits.md), [`05-cloud-architecture.md`](05-cloud-architecture.md), [`09-ai-and-agent-runtime-architecture.md`](09-ai-and-agent-runtime-architecture.md), [`08-security-architecture.md`](08-security-architecture.md)

Money is the one domain where a lost message, a duplicate delivery or a clock skew becomes a customer-visible injustice. This architecture is therefore built on three structural commitments: **the provider is never believed unconditionally**, **every financial record is immutable**, and **entitlement is a derived projection that can always be recomputed from grants**.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| BC-01 | **Paddle is the sole customer-facing Merchant of Record; Payoneer is a payout destination only** (**D-005**). Payoneer never appears in a customer purchase path. |
| BC-02 | **Every commercial figure is versioned commercial policy** (**D-020**) — never a constant compiled into product code, and never a value that silently changes a historical charge. |
| BC-03 | **A provider event is a trigger, never unconditional belief** (`EV-05` in the commerce requirements). |
| BC-04 | **Entitlement is derived, never stored as an ad-hoc flag.** It is recomputed from grants and revocations, and the snapshot is a cache with a version (`§5`). |
| BC-05 | **Financial history is immutable** (`CR-10` there). Corrections are new records, never edits. |
| BC-06 | **Money arithmetic is fixed-precision** (`CR-08` there). Floating-point accumulation is prohibited, and a policy test enforces it. |
| BC-07 | **The provider adapter boundary is absolute.** No provider type, identifier format or webhook shape appears outside the provider adapter module (`§2`). |
| BC-08 | **Reconciliation is a first-class subsystem, not a maintenance script** (`RC-01`, `RC-02` there). |
| BC-09 | **ArcChat Mobile contains no commerce path at all** (**D-022**), enforced by build-verifiable checks (`§10`). |

---

## 2. Module structure and boundaries

```
Cloud modular monolith
├── Commerce.Catalog          offers, prices, price versions, policy versions
├── Commerce.Purchase         purchase intent, checkout attempt, order, payment
├── Commerce.Providers        provider adapters + BillingProviderCapabilities
│    └── Paddle adapter       the only customer-facing adapter
├── Commerce.EventInbox       provider event persistence, verification, dispatch
├── Commerce.Subscription     normalised subscription state machine
├── Commerce.Entitlement      grants, revocations, resolver, snapshot, version
├── Commerce.Quota            quota definitions, usage counters, enforcement reads
├── Commerce.Credits          credit lots, reservation, settlement, refund hold
├── Commerce.Ledgers          three separate ledgers (§8)
├── Commerce.Reconciliation   two-way comparison and repair
└── Commerce.Evidence         commercial evidence, disputes, exports
```

| # | Rule |
|---|---|
| MB-01 | **Only `Commerce.Providers` knows a provider exists.** Every other module speaks in ArcForges' own commercial vocabulary. |
| MB-02 | **`BillingProviderCapabilities` is a typed capability description** (`§3.1` there), read by the rest of the system to decide what is offered — never a hard-coded assumption that a provider supports a given operation. |
| MB-03 | **A provider identifier is stored as an external reference on an ArcForges entity**, never as the entity's own identity. |
| MB-04 | **Entitlement is read by everything and written by nothing except the resolver** (`§5`). |
| MB-05 | **No module outside `Commerce.*` computes an entitlement decision.** They ask, and receive a reasoned answer. |

---

## 3. Identity and ownership

| # | Rule |
|---|---|
| ID-01 | **Buyer identity is a stable internal billing identity, never an email address** (`PF-02` there). A payment address such as a shared finance mailbox must never determine ownership, and changing an account email must never lose a subscription. |
| ID-02 | **Entitlement is issued to a Workspace** (`PF-01` there), so anonymous purchase of cloud capability or credits is not possible. |
| ID-03 | **Account, Workspace and Billing Account are three separate identities** with explicit relationships (`§2` of the identity requirements). |
| ID-04 | **Every checkout carries internal identifiers as provider metadata** (`PF-03` there): billing account, workspace, offer, price version, checkout attempt and purchase intent. An email change, account merge, workspace transfer or provider-customer change must not orphan an order. |
| ID-05 | **Ownership transfer is an explicit modelled operation**, not a side effect of changing a provider customer record. |

---

## 4. Purchase pipeline

```
Signed-in user, selected Workspace
   ↓
PurchaseIntent            idempotency anchor, ArcForges-owned
   ↓
CheckoutAttempt           carries internal ids as provider metadata
   ↓
Provider hosted checkout  (Paddle)
   ↓ payment
Provider webhook  ──►  Provider Event Inbox  (persist first, then process)
   ↓ verification chain
Order + Payment recognised
   ↓
EntitlementGrant created (immutable)
   ↓
Entitlement Resolver recomputes the Workspace
   ↓
EntitlementSnapshot; EntitlementVersion++
   ↓ realtime notification
Clients refresh from the Entitlement API
```

| # | Rule |
|---|---|
| PU-01 | **A success redirect is never payment authority** (`PF-04` there). The client shows a confirming state and waits for verified provider events. Granting from a redirect would be forgeable. |
| PU-02 | **One purchase intent yields at most one valid checkout** (`PF-05` there); a double submission never produces two orders. |
| PU-03 | **The intent is the idempotency anchor for the whole chain**, including retries after a client crash. |
| PU-04 | **A checkout attempt expires.** An abandoned attempt is closed by policy, and a later provider event for an expired attempt is reconciled rather than silently granted. |
| PU-05 | **Checkout is hosted by the provider.** ArcForges never handles card data, and no payment instrument field exists in any ArcForges surface. |
| PU-06 | **Tax, currency and price presentation come from the provider's capability description and the versioned catalogue** (`§3` there), never from client-side computation. |

### 4.1 Provider Event Inbox

| # | Rule |
|---|---|
| EI-01 | **Persist before process** (`EV-01` there): provider, event id, event type, received time, raw payload, signature verification result, processing status and retry count are written before any business logic runs. |
| EI-02 | **Idempotency key is event type plus event id** (`EV-02` there); an event affects business state exactly once regardless of delivery count. |
| EI-03 | **Signature verification is mandatory** (`EV-03` there). An unverified event is recorded and rejected, never processed. |
| EI-04 | **The webhook endpoint returns quickly and processes asynchronously** (`EV-04` there), so provider retry behaviour is not driven by ArcForges' processing time. |
| EI-05 | **The verification chain is fixed and ordered** (`EV-05` there): signature → known provider → known store → known product mapping → known purchase intent or buyer identity → valid payment state → not already processed → grant. |
| EI-06 | **Out-of-order events are handled by state, not by arrival order.** Each event is applied against the current normalised subscription state, and a stale event is a no-op rather than a regression. |
| EI-07 | **An unprocessable event is quarantined with a reason and alerts**, never dropped. Inbox backlog is a page-worthy condition (`§7` of the observability architecture). |
| EI-08 | **The raw payload is retained** for dispute evidence and for replay after a processing defect is fixed. |
| EI-09 | **Replay is supported and idempotent**: reprocessing the inbox from a point in time converges to the same commercial state. |

---

## 5. Entitlement architecture

### 5.1 The resolver

```
Inputs                                     Output
├── EntitlementGrant*        (immutable)
├── EntitlementRevocation*   (immutable)   →  EntitlementSnapshot
├── Subscription state                        ├── effective capabilities
├── Policy version                            ├── quotas
├── Bundle definition version                 ├── reasons per capability
└── Clock (PaidThrough)                       └── EntitlementVersion
```

| # | Rule |
|---|---|
| EN-01 | **Grants and revocations are immutable, append-only records** (`§6.4` there). Nothing is edited; a change is a new record. |
| EN-02 | **The snapshot is a derived cache** and can always be rebuilt from the record set. A rebuild that produces a different answer is a defect, and a test asserts equality. |
| EN-03 | **Every capability in the snapshot carries a reason** (`§6.5` there), so a user or an operator can always answer "why do I have this, or why not". |
| EN-04 | **`EntitlementVersion` increments on every change** and is the value clients compare; a client never infers entitlement from a purchase event it observed. |
| EN-05 | **Normalised subscription state is driven by `PaidThrough`**, not by a provider status string (`§5` there). Provider states map into ArcForges states through the adapter. |
| EN-06 | **The four entitlement kinds are modelled distinctly** (`§6.1` there) and combined by explicit rules, never by boolean union. |
| EN-07 | **Entitlement evaluation is deterministic given its inputs**, including the clock, so a decision can be reproduced for a dispute. |
| EN-08 | **Time is evaluated in a single authoritative time source.** A grace period, expiry or renewal boundary is never computed from a client clock. |

### 5.2 Distribution to clients

| # | Rule |
|---|---|
| ED-01 | **Clients read entitlement from the Entitlement API** and cache it with its version (`§4` of the cloud architecture). |
| ED-02 | **A realtime notification is a hint to refresh**, never the source of truth (`§7` of the cloud architecture). |
| ED-03 | **A cached entitlement has a bounded staleness and a defined offline behaviour** — what remains available, for how long, and with what visible state (`§4` of the policy requirements). |
| ED-04 | **Enforcement is server-side for anything with cost.** A client-side check is a user-experience affordance, never the control (`§3` of the security architecture). |
| ED-05 | **Loss of entitlement never deletes local user data** (`§13` of the data requirements). Access to cloud capability changes; local content does not. |

---

## 6. Quota and usage

| # | Rule |
|---|---|
| QA-01 | **Quota is a limit; usage is a measurement** (`§7` there). They are separate stores with separate lifecycles. |
| QA-02 | **A usage counter is authoritative server-side**, with a defined reset boundary tied to the entitlement period, not to a calendar convenience. |
| QA-03 | **Storage accounting is computed from committed objects**, never from a client-reported figure (`§8` of the cloud requirements). |
| QA-04 | **Exceeding a quota is a typed, explained refusal with a remediation path**, never a silent failure or an unbounded overage. |
| QA-05 | **Quota checks are evaluated at the same enforcement point as the operation they bound**, so a check cannot be bypassed by a different entry path. |

---

## 7. Credit architecture

### 7.1 Lots

| # | Rule |
|---|---|
| CD-01 | **A balance is never a single number** (`CR-01` there). It is the sum over credit lots, each with source, reference, original amount, remaining amount, creation time, expiry and refund status. |
| CD-02 | **Three lot classes with different rules** (`CR-03` there): subscription allowance (reissued per period, no rollover, voided at period end), purchased credits (accumulate, expire, no cash value, not withdrawable, not transferable), and promotional or compensation credits (independent expiry, non-refundable). |
| CD-03 | **Consumption order is earliest-expiry-first within the specified class priority** (`CR-04` there), so user-visible loss is minimised. |
| CD-04 | **Purchased credits survive subscription end** (`CR-05` there). |
| CD-05 | **An annual subscription issues its allowance monthly on the anniversary** (`CR-06` there), never as twelve periods at once. |
| CD-06 | **Allowance and purchased credits are presented separately** (`§8.3` there), never summed, because they expire differently. |

### 7.2 Reserve, settle, release

```
Run requested
  → estimate cost from the locked tariff snapshot
  → RESERVE against available lots      (Available ↓, Reserved ↑)
  → execute
  → SETTLE actual                        (Reserved ↓, Consumed ↑)
  → RELEASE the unused reservation       (Reserved ↓, Available ↑)
```

| # | Rule |
|---|---|
| CS-01 | **Reservation happens before execution and settlement after it** (`CR-20` there). Three quantities exist: available, reserved, consumed. |
| CS-02 | **Reservation is what prevents overdraft under concurrency** (`CR-21` there). Concurrent runs must not each pass a balance check against the same unreserved balance. |
| CS-03 | **Reservation and settlement are atomic against the lot set**, using a single transactional boundary with explicit conflict handling. |
| CS-04 | **A reservation has an expiry.** An orphaned reservation from a crashed run is released by a sweeper, and the sweep is observable. |
| CS-05 | **Settlement is idempotent per attempt.** A retried settlement for the same attempt does not double-debit (`§4` of the agent runtime architecture). |
| CS-06 | **Negative balances are impossible** (`CR-23` there). Exhaustion is a hard stop with a clear prompt to purchase or switch to BYOK; post-paid overdraft is not offered. |
| CS-07 | **A refund request places the affected lot into a refund hold** (`CR-24` there), freezing the amount under adjudication so it cannot be spent. |
| CS-08 | **Every run carries a tariff snapshot** (`CR-09` there), so a historical charge is explainable against the rates in force at the time. |
| CS-09 | **A provider price change never retroactively alters a settled charge** (**D-020**). |

---

## 8. The three ledgers

| Ledger | Records | Never mixed with |
|---|---|---|
| **Provider cost ledger** | What ArcForges pays upstream providers | Customer-facing credit amounts |
| **Customer credit ledger** | What a customer holds, reserves and consumes | Provider cost |
| **Payment and revenue ledger** | What was charged, refunded, disputed and settled | Either of the above |

| # | Rule |
|---|---|
| LG-01 | **The three ledgers are permanently separate** (`I-011`, `CR-07` there). A single "cost" concept spanning them is prohibited. |
| LG-02 | **Each ledger is append-only** with its own record identity and its own reconciliation. |
| LG-03 | **A cross-ledger relationship is a reference, never a shared row.** |
| LG-04 | **Margin and unit economics are computed as a report over the ledgers**, never as a stored figure that can drift. |
| LG-05 | **A ledger export is reproducible** for a stated period and is part of commercial evidence (`§10` there). |

---

## 9. Reconciliation

| # | Rule |
|---|---|
| RE-01 | **Reconciliation runs on a schedule and compares in both directions** (`RC-01` there): ArcForges commercial state against provider orders and subscriptions, and the reverse. |
| RE-02 | **Losing one webhook must never permanently cost a user their subscription** (`RC-02` there). Reconciliation is the second line of defence, and its absence is a go-live blocker. |
| RE-03 | **Settlement lags transactions materially** (`RC-03` there, **V-07**). Payout cycles run on a monthly rhythm with a further transfer delay, so the model must not assume payout timing tracks transaction timing. |
| RE-04 | **A divergence produces a typed repair action**, an audit record and, above a threshold, an alert — never a silent write. |
| RE-05 | **Repairs are expressed as new grants, revocations or ledger entries**, never as edits to history (`BC-05`). |
| RE-06 | **Reconciliation is idempotent and safe to run repeatedly**, including during an incident. |
| RE-07 | **A reconciliation report is retained** and is part of commercial evidence. |

---

## 10. Mobile and store posture

| # | Rule |
|---|---|
| MO-01 | **ArcChat Mobile is consumption-only** (**D-022**, **V-09**): no purchase surface, no embedded provider checkout, no store billing integration in the initial release, no external purchase call to action, and **no licence-key or purchase-token unlock path**. |
| MO-02 | **A build-time and CI check asserts every prohibition** (`MB-03` there; `MC-01`–`MC-06` in the mobile architecture). |
| MO-03 | **The entitlement architecture remains capable of accepting a future store-originated grant** without implementing one (`MB-02` there): a store grant would enter as another grant source through the same resolver. |
| MO-04 | **A store listing is a distribution channel, never a commerce channel** (`PL-03` in the distribution requirements). |

---

## 11. Regional route

| # | Rule |
|---|---|
| RG-01 | **Mainland China is a conditional market with eight pre-enablement gates** (**D-023**), and none of them is satisfied by code alone. |
| RG-02 | **The regional route is an additional provider adapter behind the same `BillingProviderCapabilities` boundary** (`§12` there), not a parallel commerce implementation. |
| RG-03 | **Entitlement, credits, ledgers and reconciliation are unchanged by region.** Only the provider adapter, tax treatment and presentation differ. |
| RG-04 | **The route stays disabled until every gate is recorded as met** (**D-023**), enforced by configuration and verified in the release gate. |

---

## 12. Security and resilience

| # | Rule |
|---|---|
| SR-01 | **A commercial mutation is an R2-or-above operation** (`§4` of the security requirements), audited with the full actor chain. |
| SR-02 | **Provider credentials are held as `SecretRef` in the secret broker** (`§6` of the security architecture); no commerce module reads a plaintext key. |
| SR-03 | **The webhook endpoint is rate-limited, signature-gated and isolated**, so it cannot be used as an amplification or enumeration surface. |
| SR-04 | **A provider outage degrades purchase, never entitlement.** Existing entitlement continues to be served from ArcForges state (`§13` of the cloud architecture). |
| SR-05 | **Credit operations continue during a provider outage** for already-held credits; only purchase is unavailable. |
| SR-06 | **An operator cannot silently grant or revoke entitlement.** Administrative grants are a distinct grant kind, are attributed, and appear in the user's own entitlement reasons (`§6.4` there). |
| SR-07 | **Commercial evidence is exportable for disputes** (`§10` there): order, payments, provider events, entitlement history and usage, for a stated period. |
| SR-08 | **Telemetry never carries payment data** (`§4` of the observability architecture); commercial audit is separate from observability. |

---

## 13. Testing and gates

| # | Test obligation |
|---|---|
| CT-01 | **Idempotency suite**: duplicate webhook delivery, duplicate checkout submission, retried settlement, replayed inbox — each converges to one outcome. |
| CT-02 | **Out-of-order event suite**: renewal before payment, cancellation before renewal, refund before settlement — each produces the specified state. |
| CT-03 | **Resolver equivalence**: rebuilding a snapshot from grants and revocations equals the stored snapshot for every fixture account (`EN-02`). |
| CT-04 | **Concurrency suite**: parallel runs against one balance never overdraw (`CS-02`), and reservation expiry releases correctly. |
| CT-05 | **Precision suite**: no floating-point path exists in money or credit arithmetic (`BC-06`), asserted as a repository policy test. |
| CT-06 | **Lot-ordering suite**: consumption order, expiry, allowance void and refund hold behave as specified for every lot-class combination. |
| CT-07 | **Reconciliation suite**: a dropped webhook, a duplicated order and a provider-side change are each detected and repaired without editing history. |
| CT-08 | **Immutability suite**: any attempt to update or delete a grant, revocation, payment or ledger entry fails. |
| CT-09 | **Boundary suite**: no provider type or identifier format appears outside the provider adapter (`BC-07`), asserted as an architecture test. |
| CT-10 | **Mobile prohibition suite**: the commerce checks of `MO-02` fail the build if any purchase or unlock path is introduced. |
| CT-11 | **Evidence suite**: a dispute export for a fixture account is complete, reproducible and free of payment instrument data. |
| CT-12 | **Go-live gate**: purchase, renewal, cancellation, refund, dispute, reconciliation, credit lifecycle and entitlement distribution are all demonstrated end to end against the provider's test environment before the paid product opens (`§18` there). |

---

## 14. Non-goals

The commerce layer is **not**: a payment processor; a holder of card data; a place where a single balance number lives; a system that trusts a redirect or a webhook without verification; a store-billing integration in the initial release; a source of retroactive price changes; or a system whose history can be edited.

---

## 15. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 3` | The commercial domain, purchase pipeline, entitlement grant model, subscription lifecycle and provider event handling |
| `I4 §Stage 4` | The grant-based unified entitlement system and its separation from subscription state |
| `I4 §Stage 8` | AI economics, tariff versioning, the three ledgers, and reserve-then-settle metering |
| **D-005** | Paddle as sole Merchant of Record; Payoneer as payout destination only |
| **D-020** | Every figure is versioned commercial policy; immutable history; fixed-precision arithmetic; hard stop at zero |
| **D-022**, **V-09** | The mobile consumption-only posture as a build-verifiable constraint |
| **D-023** | The Mainland China conditional route and its pre-enablement gates |
| **V-07** | Settlement timing does not track transaction timing |
| `I-011` | The three ledgers are permanently separate |
