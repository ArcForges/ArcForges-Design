# Billing and Commerce Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)** (provider baseline), **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** (versioned economic policy), **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)** (mobile commerce posture), **[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)** (Mainland China route), **[V-07](../assurance/phase-1-official-verification.md#rule-v-07)** (settlement timing)
> Companions: [`../requirements/04-commerce-entitlement-and-credits.md`](../requirements/04-commerce-entitlement-and-credits.md), [`05-cloud-architecture.md`](05-cloud-architecture.md), [`09-ai-and-agent-runtime-architecture.md`](09-ai-and-agent-runtime-architecture.md), [`08-security-architecture.md`](08-security-architecture.md)

Money is the one domain where a lost message, a duplicate delivery or a clock skew becomes a customer-visible injustice. This architecture is therefore built on three structural commitments: **the provider is never believed unconditionally**, **every financial record is immutable**, and **entitlement is a derived projection that can always be recomputed from grants**.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| BC-01 | **Paddle is the sole customer-facing Merchant of Record; Payoneer is a payout destination only** (**[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)**). Payoneer never appears in a customer purchase path. |
| BC-02 | **Every commercial figure is versioned commercial policy** (**[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)**) — never a constant compiled into product code, and never a value that silently changes a historical charge. |
| BC-03 | **A provider event is a trigger, never unconditional belief** ([EV-05](../requirements/04-commerce-entitlement-and-credits.md#rule-ev-05) in the commerce requirements). |
| BC-04 | **Entitlement is derived, never stored as an ad-hoc flag.** It is recomputed from grants and revocations, and the snapshot is a cache with a version (`§5`). |
| <a id="rule-bc-05"></a>BC-05 | **Financial history is immutable** ([CR-10](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-10) there). Corrections are new records, never edits. |
| <a id="rule-bc-06"></a>BC-06 | **Money arithmetic is fixed-precision** ([CR-08](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-08) there). Floating-point accumulation is prohibited, and a policy test enforces it. |
| <a id="rule-bc-07"></a>BC-07 | **The provider adapter boundary is absolute.** No provider type, identifier format or webhook shape appears outside the provider adapter module (`§2`). |
| BC-08 | **Reconciliation is a first-class subsystem, not a maintenance script** ([RC-01](../requirements/04-commerce-entitlement-and-credits.md#rule-rc-01), [RC-02](../requirements/04-commerce-entitlement-and-credits.md#rule-rc-02) there). |
| BC-09 | **ArcChat Mobile contains no commerce path at all** (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**), enforced by build-verifiable checks (`§10`). |

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
├── Commerce.Credits          purchased and compensation lots, reservation, settlement, refund hold
├── Commerce.Metering         usage normaliser, price resolver, cost calculator,
│                            settlement, uncertain-usage reconciliation (§7)
├── Commerce.Ledgers          three separate ledgers (§8)
├── Commerce.Reconciliation   two-way comparison and repair
└── Commerce.Evidence         commercial evidence, disputes, exports

Entitlement                  ← a SEPARATE top-level module, not part of Commerce
├── definitions, bundles
├── grants, revocations       ← Commerce writes here through the grant interface
├── service terms             ← the AI gate (§5.3); a credit balance never creates one
├── included-capacity buckets ← refill, burst ceiling, holds (§7.2)
├── admission                 ← one atomic decision over term + capacity + limits (§7.3)
├── resolver, snapshots
└── quotas, usage counters

Configuration                ← a SEPARATE top-level module (§2.2)
├── bundle loader and schema validator
├── activation, snapshot persistence, revision history
└── client projection (allowlisted fields only)
```

### 2.2 Configuration is not owned by Commerce either

[DC-01](../requirements/11-policy-and-configuration.md#rule-dc-01)–[DC-17](../requirements/11-policy-and-configuration.md#rule-dc-17) of the configuration requirements make deployment configuration the production policy source. It is a **separate top-level module**, for the same reason Entitlement is: Commerce is one of its consumers, not its owner.

| # | Rule |
|---|---|
| CG-01 | **Configuration owns the bundle, its schema, validation, activation and the persisted snapshots.** Commerce, Entitlement, the Harness and the simulator all *read* an activated revision; none of them loads or validates one. |
| <a id="rule-cg-02"></a>CG-02 | **A request records which validated revision it used** ([DC-12](../requirements/11-policy-and-configuration.md#rule-dc-12)). That recorded revision — not the current file — is what a later reproduction reads ([RP-02](#rule-rp-02), [I-494](../requirements/01-normative-glossary-and-invariants.md#rule-i-494)). |
| <a id="rule-cg-03"></a>CG-03 | **Activation is atomic and all replicas converge on one coherent revision** ([DC-11](../requirements/11-policy-and-configuration.md#rule-dc-11), [DC-12](../requirements/11-policy-and-configuration.md#rule-dc-12)). A replica that cannot load the activated revision **cannot admit affected work**; it does not fall back to a previous revision or a sample. |
| CG-04 | **Runtime facts are never configuration.** Subscription state, measured tokens, usage, reservations, balances and payment facts are database records ([DC-09](../requirements/11-policy-and-configuration.md#rule-dc-09)). Direct SQL editing is not an alternative policy authority. |
| <a id="rule-cg-05"></a>CG-05 | **Only an allowlisted projection reaches a client** ([DC-14](../requirements/11-policy-and-configuration.md#rule-dc-14)): the user's own offer and rights, published retail rates, current capacity and balance, recovery timing and availability reasons. Supplier rates, risk thresholds, route weights and other users' state never ship to a client. |
| <a id="rule-cg-06"></a>CG-06 | **Secrets are not configuration** ([DC-15](../requirements/11-policy-and-configuration.md#rule-dc-15)). Provider keys, payment credentials and signing keys are injected by secret manager or Docker secret, never present in the policy file, the image, the logs or the public sample. |

---

### 2.1 Entitlement is not owned by Commerce

**[MD-05](05-cloud-architecture.md#rule-md-05) of the cloud architecture governs**: *Commerce depends on Entitlement's grant interface, never the reverse. Entitlement must remain usable with Commerce entirely absent.* That is the authoritative ownership statement, and this document is subordinate to it.

| # | Rule |
|---|---|
| <a id="rule-eo-01"></a>EO-01 | **Entitlement is a top-level Cloud module** ([`05-cloud-architecture.md`](05-cloud-architecture.md) `§4`). It owns definitions, bundles, grants, revocations, the resolver, snapshots, quotas and usage counters. |
| EO-02 | **Commerce is a separate top-level module.** It owns billing accounts, offers, price versions, purchase intents, checkout attempts, orders, payments, provider events, subscriptions, credits, ledgers, reconciliation and commercial evidence. |
| <a id="rule-eo-03"></a>EO-03 | **Commerce writes into Entitlement only through Entitlement's published grant interface** — `IssueGrant`, `RevokeGrant` — never by writing Entitlement's tables ([MD-02](05-cloud-architecture.md#rule-md-02) there: no module writes another module's tables). |
| <a id="rule-eo-04"></a>EO-04 | **Entitlement never calls Commerce.** A grant carries its own source discriminator (`purchase`, `administrative`, `promotional`, `trial`, `store`), so Entitlement can resolve without knowing a provider exists. |
| <a id="rule-eo-05"></a>EO-05 | **Removing Commerce entirely must leave Entitlement working**, serving free-tier and administrative grants. This is the test that keeps the boundary honest, and it is asserted in [WP-42.00](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.00). |
| <a id="rule-eo-06"></a>EO-06 | **Credits belong to Commerce; quota and usage belong to Entitlement.** A credit is money-adjacent and is settled against a ledger; a quota is a capability limit resolved from a grant. Conflating them was the defect this section corrects. |
| EO-07 | **The reserve-then-settle budget interface spans both**: Commerce.Credits holds the lots and performs the accounting; Entitlement answers *may this workspace spend at all*. The execution engine calls one façade that fans out to both, and that façade lives in Commerce. |

> **Correction, 2026-09-05.** An earlier revision of this document listed `Commerce.Entitlement` and `Commerce.Quota` as sub-modules of Commerce, contradicting [MD-05](05-cloud-architecture.md#rule-md-05). Both are removed above. Every later reference in this document to *"the entitlement resolver"* means the **Entitlement module's** resolver, reached through its published interface.

| # | Rule |
|---|---|
| MB-01 | **Only `Commerce.Providers` knows a provider exists.** Every other module speaks in ArcForges' own commercial vocabulary. |
| MB-01a | **Commerce and Entitlement are separate top-level modules** (`§2.1`). Commerce reaches Entitlement only through its grant interface. |
| MB-02 | **`BillingProviderCapabilities` is a typed capability description** (`§3.1` there), read by the rest of the system to decide what is offered — never a hard-coded assumption that a provider supports a given operation. |
| <a id="rule-mb-03"></a>MB-03 | **A provider identifier is stored as an external reference on an ArcForges entity**, never as the entity's own identity. |
| MB-04 | **Entitlement state is read by everything and written only by the Entitlement module** — by its resolver for snapshots, and by its grant interface for grants and revocations (`§5`). |
| MB-05 | **No module computes an entitlement decision for itself.** Every caller asks the Entitlement module and receives a reasoned answer. |

---

## 3. Identity and ownership

| # | Rule |
|---|---|
| <a id="rule-id-01"></a>ID-01 | **Buyer identity is a stable internal billing identity, never an email address** ([PF-02](../requirements/04-commerce-entitlement-and-credits.md#rule-pf-02) there). A payment address such as a shared finance mailbox must never determine ownership, and changing an account email must never lose a subscription. |
| ID-02 | **Entitlement is issued to a Workspace** ([PF-01](../requirements/04-commerce-entitlement-and-credits.md#rule-pf-01) there), so anonymous purchase of cloud capability or credits is not possible. |
| ID-03 | **Account, Workspace and Billing Account are three separate identities** with explicit relationships (`§2` of the identity requirements). |
| <a id="rule-id-04"></a>ID-04 | **Every checkout carries internal identifiers as provider metadata** ([PF-03](../requirements/04-commerce-entitlement-and-credits.md#rule-pf-03) there): billing account, workspace, offer, price version, checkout attempt and purchase intent. An email change, account merge, workspace transfer or provider-customer change must not orphan an order. |
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
| <a id="rule-pu-01"></a>PU-01 | **A success redirect is never payment authority** ([PF-04](../requirements/04-commerce-entitlement-and-credits.md#rule-pf-04) there). The client shows a confirming state and waits for verified provider events. Granting from a redirect would be forgeable. |
| <a id="rule-pu-02"></a>PU-02 | **One purchase intent yields at most one valid checkout** ([PF-05](../requirements/04-commerce-entitlement-and-credits.md#rule-pf-05) there); a double submission never produces two orders. |
| <a id="rule-pu-03"></a>PU-03 | **The intent is the idempotency anchor for the whole chain**, including retries after a client crash. |
| <a id="rule-pu-04"></a>PU-04 | **A checkout attempt expires.** An abandoned attempt is closed by policy, and a later provider event for an expired attempt is reconciled rather than silently granted. |
| <a id="rule-pu-05"></a>PU-05 | **Checkout is hosted by the provider.** ArcForges never handles card data, and no payment instrument field exists in any ArcForges surface. |
| PU-06 | **Tax, currency and price presentation come from the provider's capability description and the versioned catalogue** (`§3` there), never from client-side computation. |

### 4.1 Provider Event Inbox

| # | Rule |
|---|---|
| <a id="rule-ei-01"></a>EI-01 | **Persist before process** ([EV-01](../requirements/04-commerce-entitlement-and-credits.md#rule-ev-01) there): provider, event id, event type, received time, raw payload, signature verification result, processing status and retry count are written before any business logic runs. |
| <a id="rule-ei-02"></a>EI-02 | **Idempotency key is event type plus event id** ([EV-02](../requirements/04-commerce-entitlement-and-credits.md#rule-ev-02) there); an event affects business state exactly once regardless of delivery count. |
| <a id="rule-ei-03"></a>EI-03 | **Signature verification is mandatory** ([EV-03](../requirements/04-commerce-entitlement-and-credits.md#rule-ev-03) there). An unverified event is recorded and rejected, never processed. |
| <a id="rule-ei-04"></a>EI-04 | **The webhook endpoint returns quickly and processes asynchronously** ([EV-04](../requirements/04-commerce-entitlement-and-credits.md#rule-ev-04) there), so provider retry behaviour is not driven by ArcForges' processing time. |
| <a id="rule-ei-05"></a>EI-05 | **The verification chain is fixed and ordered** ([EV-05](../requirements/04-commerce-entitlement-and-credits.md#rule-ev-05) there): signature → known provider → known store → known product mapping → known purchase intent or buyer identity → valid payment state → not already processed → grant. |
| <a id="rule-ei-06"></a>EI-06 | **Out-of-order events are handled by state, not by arrival order.** Each event is applied against the current normalised subscription state, and a stale event is a no-op rather than a regression. |
| <a id="rule-ei-07"></a>EI-07 | **An unprocessable event is quarantined with a reason and alerts**, never dropped. Inbox backlog is a page-worthy condition (`§7` of the observability architecture). |
| <a id="rule-ei-08"></a>EI-08 | **The raw payload is retained** for dispute evidence and for replay after a processing defect is fixed. |
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
| <a id="rule-en-01"></a>EN-01 | **Grants and revocations are immutable, append-only records** (`§6.4` there). Nothing is edited; a change is a new record. |
| <a id="rule-en-02"></a>EN-02 | **The snapshot is a derived cache** and can always be rebuilt from the record set. A rebuild that produces a different answer is a defect, and a test asserts equality. |
| EN-03 | **Every capability in the snapshot carries a reason** (`§6.5` there), so a user or an operator can always answer "why do I have this, or why not". |
| EN-04 | **`EntitlementVersion` increments on every change** and is the value clients compare; a client never infers entitlement from a purchase event it observed. |
| <a id="rule-en-05"></a>EN-05 | **Normalised subscription state is driven by `PaidThrough`**, not by a provider status string (`§5` there). Provider states map into ArcForges states through the adapter. |
| EN-06 | **The four entitlement kinds are modelled distinctly** (`§6.1` there) and combined by explicit rules, never by boolean union. |
| EN-07 | **Entitlement evaluation is deterministic given its inputs**, including the clock, so a decision can be reproduced for a dispute. |
| EN-08 | **Time is evaluated in a single authoritative time source.** A grace period, expiry or renewal boundary is never computed from a client clock. |

### 5.2 Distribution to clients

| # | Rule |
|---|---|
| ED-01 | **Clients read entitlement from the Entitlement API** and cache it with its version (`§4` of the cloud architecture). |
| <a id="rule-ed-02"></a>ED-02 | **A realtime notification is a hint to refresh**, never the source of truth (`§7` of the cloud architecture). |
| ED-03 | **A cached entitlement has a bounded staleness and a defined offline behaviour** — what remains available, for how long, and with what visible state (`§4` of the policy requirements). |
| <a id="rule-ed-04"></a>ED-04 | **Enforcement is server-side for anything with cost.** A client-side check is a user-experience affordance, never the control (`§3` of the security architecture). |
| <a id="rule-ed-05"></a>ED-05 | **Loss of entitlement never deletes local user data** (`§13` of the data requirements). Access to cloud capability changes; local content does not. |

### 5.3 The service term — the gate before every AI decision

[C-03](../requirements/00-product-scope-and-portfolio.md#rule-c-03) makes an **active paid service term** the precondition for official inference. It is a distinct concept from both entitlement capabilities and credit balance, and it is checked first ([AD-01](#rule-ad-01)).

| # | Rule |
|---|---|
| SV-01 | **A service term is an interval, not a flag.** `service_term` rows record kind (`subscription`, `pass`, `compensation`, `selfHostGrant`), start, end, source order or grant reference, and realm. The effective term is the union of overlapping intervals. |
| <a id="rule-sv-02"></a>SV-02 | **Only four things create one** (`§8.7` there): a verified subscription, a prepaid Cloud Pass (**[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)**), an audited compensation extension of an existing paid service, or — in a self-hosted realm only — an explicit operator-funded `ServiceGrant`. |
| <a id="rule-sv-03"></a>SV-03 | **A credit grant, trial flag or operator edit cannot create one** (`§8.7` there). This is the rule that makes "credits alone do not authorise AI" enforceable rather than aspirational. |
| <a id="rule-sv-04"></a>SV-04 | **A self-host `ServiceGrant` authorises only its own realm** ([BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [DC-16](../requirements/11-policy-and-configuration.md#rule-dc-16)). It confers no official-service entitlement, and no realm's grant is visible to another ([I-497](../requirements/01-normative-glossary-and-invariants.md#rule-i-497) family; realm isolation in `§3`). |
| <a id="rule-sv-05"></a>SV-05 | **Renewal grace protects data access, not AI.** During grace, retained data is readable and downloadable; **no new official inference is admitted** ([C-07](../requirements/00-product-scope-and-portfolio.md#rule-c-07)). The two windows are configured and evaluated separately. |
| <a id="rule-sv-06"></a>SV-06 | **Term expiry during a running Task stops further dispatch at a durable boundary** with the explicit eligibility reason. Work already settled stays settled; holds are released per `§7.6`. |
| SV-07 | **Self-host billing may be disabled entirely** (`§8.7` there, [DC-16](../requirements/11-policy-and-configuration.md#rule-dc-16)). Identity, authorisation, real usage measurement, budget limits and accounting correctness remain enforced; only customer payment is absent. |

---

## 6. Quota and usage

> **Ownership.** Quota and usage counters belong to **Entitlement**, not Commerce ([EO-01](#rule-eo-01), [EO-06](#rule-eo-06)). The rules below are stated here because commerce operations are their most common cause, not because Commerce owns the store.

| # | Rule |
|---|---|
| QA-01 | **Quota is a limit; usage is a measurement** (`§7` there). They are separate stores with separate lifecycles. |
| <a id="rule-qa-02"></a>QA-02 | Admission uses durable server-side quota reservations and usage events. A displayed `usage_counter` is a reconciled projection, not a check-then-act authority. Period counters use the entitlement period; gauges such as storage never reset at renewal. |
| QA-03 | Committed storage is measured from server-verified objects, including retained history and trash. Uploads first reserve their bounded declared maximum against committed-storage headroom **and** separate workspace/deployment staging limits. A client-reported size is an admission bound, never a measured usage value. Verified bytes remain reserved until promotion or physical cleanup. |
| QA-04 | **Exceeding a quota is a typed, explained refusal with a remediation path**, never a silent failure or an unbounded overage. |
| QA-05 | **Quota checks are evaluated at the same enforcement point as the operation they bound**, so a check cannot be bypassed by a different entry path. |
| QA-06 | `used + held + requested <= limit` is checked under the quota-budget row locks, with one idempotent reservation per operation. Simulator duration, samples, output bytes and egress use separately typed budgets; only measured consumption settles, and unused reservations release. No simulator work consumes model tokens. |
| QA-07 | Cancellation and expiry schedule idempotent cleanup; they do not pretend bytes disappeared. Staging and physical-storage accounting releases only after deletion is verified. A downgrade admits no new over-limit reservation but preserves reads, downloads, deletion and already admitted bounded work. |
| QA-08 | One workspace's content-address deduplication cannot expose another workspace's object existence or bypass permission checks. Quota counts each physical object once per owning workspace, with durable pins from current revisions, retained history, conflicts and exports. |

---

## 7. Capacity, credits and the metering path

**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) replaces the reissued-allowance model with a replenishing capacity bucket plus opt-in purchased credits.** Everything in this section derives from `§8.4`–`§8.7` of the commerce requirements ([MT-01](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-01)–[MT-16](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-16), [AC-01](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-01)–[AC-12](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-12)) and remains bound by **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** as amended.

### 7.1 The four separate quantities

Conflating any two of these is the defect class this section exists to prevent ([I-493](../requirements/01-normative-glossary-and-invariants.md#rule-i-493)).

| Quantity | Unit | Lives in | Recovers? |
|---|---|---|---|
| **Included capacity** | Integer micro-credits | `entitlement.capacity_bucket`, one row per workspace; parameters in `entitlement.capacity_policy_period` | **Yes** — continuously, during eligible paid service, up to a burst ceiling |
| **Purchased credits** | Integer micro-credits | `commerce.credit_lot` rows (`lot_class ∈ {purchased, compensation}`) | **No** — conserved; spendable only while a paid term is active |
| **Supplier cost** | Fixed-precision decimal money with currency, ≥ 9 fractional digits | `commerce.supplier_cost_entry` | n/a — an obligation ArcForges owes a provider |
| **Payment revenue** | Sale currency and amount | `commerce.ledger_entry` (payment ledger) | n/a |

| # | Rule |
|---|---|
| <a id="rule-cd-01"></a>CD-01 | **One credit = 1,000,000 micro-credits, and every customer amount is an integer count of micro-credits** ([MT-07](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-07)). No binary floating point appears in any accounting path. |
| <a id="rule-cd-02"></a>CD-02 | **Included capacity is a bucket, not a lot.** It has a burst ceiling and a recovery rate, both deployment parameters ([AC-01](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-01)), and it is never modelled as a credit lot with an expiry. |
| <a id="rule-cd-03"></a>CD-03 | **Purchased credits are lots and are conserved** ([AC-11](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-11)). They do not expire with time or cancellation ([CR-03](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-03)), survive service expiry, and become spendable again on renewal without reissue ([CR-05](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-05)). |
| <a id="rule-cd-04"></a>CD-04 | **Compensation lots are lots with a disclosed expiry** ([CR-03](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-03)), consumed earliest-expiry-first. |
| <a id="rule-cd-05"></a>CD-05 | **Consumption order is fixed**: included capacity, then eligible compensation, then purchased credits — and purchased credits only under an explicit extra-usage authorisation ([CR-04](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-04), [AC-06](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-06)). |
| <a id="rule-cd-06"></a>CD-06 | **A reservation preserves its source allocation.** Settlement debits and releases against the same sources it reserved from; there is no silent conversion between pools ([CR-04](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-04), [AC-11](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-11)). |
| <a id="rule-cd-07"></a>CD-07 | **Capacity and purchased credits are presented separately, never summed** (`§8.3` there), because one recovers and the other does not. |
| CD-08 | **One reservation row spans both pools.** `entitlement.capacity_reservation` records the split across three source columns; there is no separate credit reservation table. Two reservation tables would permit a partial settlement in which one pool moved and the other did not ([FU-01](data-model/01-cloud-data-model.md#rule-fu-01)). |
| CD-09 | **Reservation identity is the logical request, not the attempt** ([FU-02](data-model/01-cloud-data-model.md#rule-fu-02)). A logical request may make several provider attempts ([MT-02](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-02)); they share one hold and settle once ([ST-01](#rule-st-01)). |
| CD-10 | **Supplier accounting is per attempt; customer accounting is per logical request** ([FU-03](data-model/01-cloud-data-model.md#rule-fu-03)). The two are never joined one-to-one: a platform-caused retry produces two supplier cost rows and **one** customer debit ([ST-07](#rule-st-07)). |

### 7.2 The refill algorithm

Refill is a state transition, including on a balance read. Entitlement owns it. All instants use PostgreSQL UTC microsecond precision; rates are integer micro-credits per second. Intermediate multiplication uses checked arbitrary-precision integers; the stored fractional remainder is a reduced rational with denominator dividing 1,000,000. No floating-point or per-window rounding enters accounting.

```
advance(bucket, effective_now):
    # Caller holds the bucket lock. No mutation of held/available/history yet.
    end = max(bucket.watermark_at, effective_now)
    windows = chronological_intersection(
        [bucket.watermark_at, end), effective_service_intervals,
        workspace_capacity_plan_assignments, assigned_offer_policy_periods)
    for w in windows:
        balance = bucket.available_micro + bucket.remainder
        ceiling = max(0, w.burst_micro - bucket.held_micro)
        earned = duration_microseconds(w) * w.rate_micro_per_second / 1_000_000
        balance = min(balance + earned, max(balance, ceiling))
        bucket.available_micro = floor(balance)
        bucket.remainder = balance - floor(balance)
    bucket.watermark_at = end

mutate_capacity(operation, server_now):
    lock bucket and other participants in the shared-unit-of-work lock order
    advance(bucket, server_now)    # OLD held value applies to all elapsed time
    apply operation exactly once, recording before/after values and its receipt
    # release: remove the hold, then return its unused ORIGINAL allocation in full.
    # This is a transfer, not accrual: (available + held) falls only by consumption.
    commit watermark, remainder, balances, holds, history and receipt together
```

Accrual discarded at saturation is lost, including fractional accrual. It cannot reappear after a ceiling increase or consumption. Above-ceiling balance that existed before a reduction is preserved, including its existing fractional remainder, and cannot grow until it drains below the current ceiling.

| # | Rule |
|---|---|
| <a id="rule-rf-01"></a>RF-01 | Accrual uses the intersection of elapsed time, effective paid service, the workspace's **one** capacity-plan assignment and that offer's policy periods. Gaps contribute zero. Overlapping terms never add recovery rates or bursts. |
| <a id="rule-rf-02"></a>RF-02 | The watermark is durable and monotonic. The bucket lock serialises replicas. Clock rollback neither rewinds accrual nor creates a new service activation. |
| <a id="rule-rf-03"></a>RF-03 | Fractional accrual is exact and carried while below the ceiling; saturation discards excess **before** splitting whole and fractional units. This also holds at sub-second boundaries. |
| <a id="rule-rf-04"></a>RF-04 | Evaluation frequency does not change the result for the same ordered business events. Policy windows are integrated chronologically at their own ceilings, never with the parameters at the final read. |
| <a id="rule-rf-05"></a>RF-05 | A ceiling reduction preserves already-issued capacity, including available balance and outstanding holds. Accrual/new initialisation uses `new_available <= max(old_available, max(0, burst - held))`; a hold release is a transfer of existing funding, not issuance. Do not apply an unconditional burst CHECK that rejects grandfathered total balance. |
| <a id="rule-rf-06"></a>RF-06 | Settlement, cancellation, expiry, release, refund, compensation and first activation all **advance before changing either held or available**. A release returns the unused original allocation in full: subtract the reserved amount from held, add its unused part to available, and record consumed units. Total available-plus-held decreases only by consumption. This also preserves held capacity across a ceiling reduction; purchased credits keep their separate conservation ledger. |
| <a id="rule-rf-07"></a>RF-07 | Purchased credits never refill. No payment replay, reconnect, policy activation or term renewal creates a credit lot without its unique purchase/grant/adjustment source. |
| <a id="rule-rf-08"></a>RF-08 | Initial full capacity is issued once at the opening of an effective contiguous service run, net of outstanding holds and preserving grandfathered balance. Abutting/overlapping renewal does not initialise again. A genuine effective service gap permits one new initialisation; duplicate or late events cannot rewrite an already processed run. |
| RF-09 | Global configuration activation closes/opens immutable offer policy periods atomically and moves no workspace balance. Integration is lazy. A workspace-specific plan/term change first advances that workspace under the previous history, then appends the new effective boundary in the same transaction. |
| RF-10 | Previously held micro-credits survive a tariff/rate/burst change. Their later consumption or release cannot apply the new held value retrospectively to the interval in which they were held. |
| <a id="rule-rf-11"></a>RF-11 | Restart changes no result: balances, fractional carry, policy/plan/term histories, event receipts and watermark are durable. |
| RF-12 | **Counterexample fixed:** burst 10, rate 1/s, full hold 10 at t=0; consume that hold at t=10; read at t=11 yields **1**, whether or not anyone read at t=10. A settlement that first reduced held would incorrectly accrue 10 retroactively. Full bucket 10 at t=0, ceiling 100 at t=10 yields 11 at t=11; a full bucket cannot bank hidden fractional accrual. Hold 10, reduce burst to 3, then cancel with zero use returns the original 10; the excess cannot accrue further. Returning only 3 would confiscate 7 already-issued units. |

### 7.3 Admission

Admission is **one atomic decision**, not a sequence of independent checks ([AC-04](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-04)) — and because its funds live in two modules it uses the enumerated shared unit of work of `§6.1.1` of the data-model overview, committing **before** any provider call.

```
admit(request):
    verify beneficiary authority: paid term for user work, operator job for platform work
    resolve customer tariff snapshot (pin to Run)       # MT-06
    resolve supplier price version (dispatch-time)      # MT-06
    bound = conservative ceiling over input, output/reasoning, and
            separately billed tools, from the actual route            # MT-15
    if bound is unpriceable or unbounded:  reject                     # MT-15, DC-05
    SHARED UNIT OF WORK  (Entitlement + Commerce; §6.1.1 of the data-model overview)
        LOCK capacity_bucket(workspace)                    # fixed lock order, SU-04
        refill(bucket, now)                                # §7.2
        check workspace concurrency, per-request and per-run ceilings   # AC-04
        recheck effective authority under lock; reserve supplier exposure for this attempt
        reserve user bound across capacity -> compensation -> purchased, if user-benefiting
          writing capacity_reservation and each lot's held_micro
        write the dispatch intent                                       # DB-01
    COMMIT                                                              # <- DISPATCH BARRIER
    if insufficient:  WaitingForCapacity(recovery_time) | ExtraCreditsRequired | Reject
    -- nothing above this line has touched a provider or any network
```

| # | Rule |
|---|---|
| <a id="rule-ad-01"></a>AD-01 | Customer-benefiting official inference requires an active paid service term. Platform-funded routing, health, abuse checks, admitted indexing and corrective retries use an explicit operator job/beneficiary authority and supplier budget instead; they never invent a customer term or debit. Self-host grants are realm-scoped. Identity, data access, policy and resource limits apply to both paths. |
| <a id="rule-ad-02"></a>AD-02 | **Admission reserves atomically in one transaction spanning Entitlement and Commerce** — the enumerated shared unit of work ([SU-01](data-model/00-data-model-overview.md#rule-su-01) of the data-model overview). Concurrent runs on one workspace, across devices and replicas, cannot each pass a check against the same unreserved balance ([CR-21](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-21), [AC-04](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-04)). An asynchronous saga cannot close that window, because the window lies *between* the two writes. |
| AD-09 | **Nothing crosses the dispatch barrier inside a transaction** ([DB-02](data-model/00-data-model-overview.md#rule-db-02) there). The reservation commits first; only then does a provider call begin. Holding a transaction open across provider latency would hold the bucket lock for the provider's response time. |
| <a id="rule-ad-10"></a>AD-10 | **The dispatch intent is written in the reserving transaction** ([DB-01](data-model/00-data-model-overview.md#rule-db-01) there). Its presence with no recorded outcome means **unknown**, never *did not happen* (`§8` of the harness). |
| <a id="rule-ad-03"></a>AD-03 | **A request whose bound can never fit capacity plus authorised extra credits is rejected immediately** with a smaller-request or budget action — never queued forever ([AC-04](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-04)). |
| <a id="rule-ad-04"></a>AD-04 | **An unbounded or unpriceable route cannot enter paid service** ([MT-15](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-15), [DC-05](../requirements/11-policy-and-configuration.md#rule-dc-05)). There is no assumed zero-rate category and no wildcard model entry. |
| <a id="rule-ad-05"></a>AD-05 | **Exhausted capacity waits for a server-calculated recovery time** ([AC-06](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-06)). Purchased credits are used only after the user enables extra usage with a maximum budget; there is no automatic purchase, recharge or paid fallback. |
| AD-06 | **Background automation spends only within its previously authorised budget** ([AC-06](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-06)). |
| AD-07 | **Rate limits, safety limits and provider availability remain enforceable even with extra credits** ([AC-09](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-09)). |
| AD-08 | **All entry points share one workspace pool** ([AC-07](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-07)). Desktop, Web, Mobile and automation consume the same capacity and credits; changing model changes consumption through the tariff, never by granting a new allowance. |

The persisted admission mechanism is `commerce.spend_budget` + `spend_reservation` and `entitlement.quota_budget` + `quota_reservation` in the Cloud data model. Supplier exposure is reserved for **every** provider attempt, including retries and platform-funded work. Currency budgets are never compared to micro-credits. No admission decision relies on a materialised usage display or a read followed by a later decrement.

A logical AI request is one bounded model invocation (possibly retried), not the whole conversation Turn. All invocations in a Run also reserve against its durable authorised total. Customer settlement of each durable iteration precedes admission of the next; a waiting device holds no reservation for an undispatched future iteration. Pending supplier liability remains charged against supplier exposure after a customer hold's reconciliation deadline.

### 7.4 Usage normalisation

Provider usage shapes differ, so a normaliser turns each provider's report into **non-overlapping** ArcForges billing categories ([MT-03](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-03)).

| Category | Meaning |
|---|---|
| `input.uncached` | Input tokens billed at the full input rate |
| `input.cached_read` | Input tokens served from a provider cache |
| `input.cache_write` | Cache-creation tokens, per supported class |
| `output` | Output tokens, **inclusive of reasoning where the provider bills them together** |
| `output.reasoning` | Only where a provider bills reasoning as a separately priced category |
| `tool.<kind>` | Separately billed search, tool or media operations, with explicit quantity, unit and rate ([MT-10](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-10)) |

| # | Rule |
|---|---|
| <a id="rule-un-01"></a>UN-01 | **Each provider adapter declares its inclusion relationships**, and the normaliser asserts them ([MT-03](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-03)). Reasoning already inside `output`, and cached tokens already inside a reported input total, must not be charged twice. |
| <a id="rule-un-02"></a>UN-02 | **A category the adapter does not declare cannot be billed.** An unrecognised usage field enters reconciliation, never an automatic debit ([MT-05](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-05)). |
| <a id="rule-un-03"></a>UN-03 | **Streaming cumulative usage replaces the previous total for that attempt** ([MT-05](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-05), [I-492](../requirements/01-normative-glossary-and-invariants.md#rule-i-492)). It is never summed as independent consumption. |
| UN-04 | **Pre-call counting is an estimate for admission only** ([MT-05](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-05), [I-492](../requirements/01-normative-glossary-and-invariants.md#rule-i-492)). Local text-length estimates and client-reported counters are never final cost authority. |
| <a id="rule-un-05"></a>UN-05 | **Quantities are validated** — non-negative, matching request and model identity, matching the declared category semantics. A mismatch enters reconciliation ([MT-05](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-05)). |
| <a id="rule-un-06"></a>UN-06 | **Tier resolution uses actual request facts** ([MT-04](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-04)): context, processing and region tier come from what the request really was, not from a per-model flat rate. Each applied modifier is recorded exactly once. |

### 7.5 Settlement

```
cost      = Σ over categories:  quantity × configured_rate ÷ unit_divisor      # MT-04
supplier  = cost at the dispatch-time supplier price version, as decimal money  # MT-06, MT-07
customer  = cost at the Run's pinned retail tariff snapshot, as micro-credits   # MT-06, MT-07
```

| # | Rule |
|---|---|
| <a id="rule-st-01"></a>ST-01 | **Settlement happens once per logical request**, after category aggregation, with declared half-even rounding — never per stream fragment ([MT-07](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-07)). |
| ST-02 | **Reservation rounds conservatively upward; settlement rounds the aggregate** ([MT-07](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-07)). |
| <a id="rule-st-03"></a>ST-03 | **Settlement is idempotent per attempt usage revision and per logical request** ([MT-11](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-11)). Duplicate or reordered events never double-debit; genuinely distinct retries remain distinct supplier-cost records. |
| <a id="rule-st-04"></a>ST-04 | **A correction is an appended adjustment linked to the original records**, never an edit ([MT-11](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-11), [CR-10](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-10), **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)**). |
| <a id="rule-st-05"></a>ST-05 | **Settlement debits the sources the reservation held** and releases only their unused allocation ([CD-06](#rule-cd-06), [AC-11](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-11)), **in one shared unit of work spanning Entitlement and Commerce** ([SU-01](data-model/00-data-model-overview.md#rule-su-01) of the data-model overview). A settlement that moved one pool and failed on the other would leave funds double-counted, which is why it is not two transactions. |
| ST-06 | **Supplier cost is retained even when the customer is not charged** ([MT-09](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-09)). A platform failure releases the customer hold or appends a compensating adjustment; the money ArcForges owes upstream does not disappear. |
| <a id="rule-st-07"></a>ST-07 | **Beneficiary classification decides who pays** ([MT-08](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-08)). Delivered user-requested inference consumes capacity or authorised credits. Routing, abuse checks, health checks, admitted background indexing and platform-caused retries are **platform cost** — recorded, budgeted, and not charged to the user. |
| <a id="rule-st-08"></a>ST-08 | **Money always carries currency** ([MT-16](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-16)). V1 supplier budgets compare within one currency; there is no implicit FX conversion. Customer credits are currency-independent service units. |

### 7.6 Uncertain and missing usage

| Situation | State | Behaviour |
|---|---|---|
| Final usage never arrives | `UsagePending` | Reconcile from available provider evidence; **never zero cost, never a fabricated total** ([MT-12](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-12)) |
| Timeout after dispatch | `CostUnconfirmed` | Same. **No blind redispatch** and no repeat charge ([MT-12](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-12)) |
| Response lost in transit | `CostUnconfirmed` | Same |
| Reconciliation deadline passes unresolved | Resolved-by-policy | **Release the customer hold** with no surprise later debit; **retain the unresolved supplier liability**; alert and restrict the affected route ([MT-12](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-12)) |
| Verified supplier overrun beyond the authorised hold | Operator cost incident | **Not customer overdraft.** Block further dispatch on that route, reconcile, adjust — without erasing the real supplier usage ([MT-15](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-15)) |
| Caller cancels | Partial | Settle verified consumption already incurred within the authorised ceiling; release the remainder. Completed provider work is not presumed refundable ([MT-09](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-09)) |

| # | Rule |
|---|---|
| <a id="rule-uc-01"></a>UC-01 | **`unknown` is never silently resolved to zero.** A missing usage report is a state with a deadline, not an absence of cost ([MT-12](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-12)). |
| <a id="rule-uc-02"></a>UC-02 | **The customer-protection deadline and the supplier-liability record are independent.** Releasing one does not clear the other ([MT-12](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-12)). |
| <a id="rule-uc-03"></a>UC-03 | **Estimated, usage-confirmed and invoice-reconciled cost remain three distinguishable values** for the same request ([MT-13](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-13)). |

### 7.7 Reproducibility

| # | Rule |
|---|---|
| <a id="rule-rp-01"></a>RP-01 | **Every metering record carries the full identity chain** ([MT-14](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-14)): workspace, service term, logical request, run, attempt, reservation, usage revision, supplier price version, customer tariff snapshot, funding source, debit and any adjustment. |
| <a id="rule-rp-02"></a>RP-02 | **A historical charge is reproducible after model retirement or configuration replacement** ([MT-14](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-14)). Snapshots are persisted facts, not lookups into current configuration ([I-494](../requirements/01-normative-glossary-and-invariants.md#rule-i-494)). |
| <a id="rule-rp-03"></a>RP-03 | **Replacing configuration never resets usage, replenishes an issued allowance, reissues purchased credits or releases unresolved reservations** ([DC-13](../requirements/11-policy-and-configuration.md#rule-dc-13)). |
| <a id="rule-rp-04"></a>RP-04 | **The worked fixture of `§8.6` is an executable acceptance test**, not documentation: 800 uncached + 200 cached input + 100 output settles to USD 0.00244 supplier cost and 4,880,000 micro-credits customer cost, with a 6-credit hold releasing 1.12 credits to its original sources. |

---

## 8. The three ledgers

| Ledger | Records | Never mixed with |
|---|---|---|
| **Provider cost ledger** | What ArcForges pays upstream providers | Customer-facing credit amounts |
| **Customer credit ledger** | What a customer holds, reserves and consumes | Provider cost |
| **Payment and revenue ledger** | What was charged, refunded, disputed and settled | Either of the above |

| # | Rule |
|---|---|
| <a id="rule-lg-01"></a>LG-01 | **The three ledgers are permanently separate** ([I-011](../requirements/01-normative-glossary-and-invariants.md#rule-i-011), [CR-07](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-07) there). A single "cost" concept spanning them is prohibited. |
| LG-02 | **Each ledger is append-only** with its own record identity and its own reconciliation. |
| <a id="rule-lg-03"></a>LG-03 | **A cross-ledger relationship is a reference, never a shared row.** |
| <a id="rule-lg-04"></a>LG-04 | **Margin and unit economics are computed as a report over the ledgers**, never as a stored figure that can drift. |
| LG-05 | **A ledger export is reproducible** for a stated period and is part of commercial evidence (`§10` there). |

---

## 9. Reconciliation

| # | Rule |
|---|---|
| <a id="rule-re-01"></a>RE-01 | **Reconciliation runs on a schedule and compares in both directions** ([RC-01](../requirements/04-commerce-entitlement-and-credits.md#rule-rc-01) there): ArcForges commercial state against provider orders and subscriptions, and the reverse. |
| <a id="rule-re-02"></a>RE-02 | **Losing one webhook must never permanently cost a user their subscription** ([RC-02](../requirements/04-commerce-entitlement-and-credits.md#rule-rc-02) there). Reconciliation is the second line of defence, and its absence is a go-live blocker. |
| RE-03 | **Settlement lags transactions materially** ([RC-03](../requirements/04-commerce-entitlement-and-credits.md#rule-rc-03) there, **[V-07](../assurance/phase-1-official-verification.md#rule-v-07)**). Payout cycles run on a monthly rhythm with a further transfer delay, so the model must not assume payout timing tracks transaction timing. |
| <a id="rule-re-04"></a>RE-04 | **A divergence produces a typed repair action**, an audit record and, above a threshold, an alert — never a silent write. |
| <a id="rule-re-05"></a>RE-05 | **Repairs are expressed as new grants, revocations or ledger entries**, never as edits to history ([BC-05](#rule-bc-05)). |
| <a id="rule-re-06"></a>RE-06 | **Reconciliation is idempotent and safe to run repeatedly**, including during an incident. |
| RE-07 | **A reconciliation report is retained** and is part of commercial evidence. |

---

## 10. Mobile and store posture

| # | Rule |
|---|---|
| MO-01 | **ArcChat Mobile is consumption-only** (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)**): no purchase surface, no embedded provider checkout, no store billing integration in the initial release, no external purchase call to action, and **no licence-key or purchase-token unlock path**. |
| <a id="rule-mo-02"></a>MO-02 | **A build-time and CI check asserts every prohibition** ([MB-03](../requirements/04-commerce-entitlement-and-credits.md#rule-mb-03) there; [MC-01](11-mobile-architecture.md#rule-mc-01)–[MC-06](11-mobile-architecture.md#rule-mc-06) in the mobile architecture). |
| MO-03 | **The entitlement architecture remains capable of accepting a future store-originated grant** without implementing one ([MB-02](../requirements/04-commerce-entitlement-and-credits.md#rule-mb-02) there): a store grant would enter as another grant source through the same resolver. |
| MO-04 | **A store listing is a distribution channel, never a commerce channel** ([PL-03](../requirements/10-distribution-update-and-support.md#rule-pl-03) in the distribution requirements). |

---

## 11. Regional route

| # | Rule |
|---|---|
| RG-01 | **Mainland China is a conditional market with eight pre-enablement gates** (**[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)**), and none of them is satisfied by code alone. |
| RG-02 | **The regional route is an additional provider adapter behind the same `BillingProviderCapabilities` boundary** (`§12` there), not a parallel commerce implementation. |
| RG-03 | **Entitlement, credits, ledgers and reconciliation are unchanged by region.** Only the provider adapter, tax treatment and presentation differ. |
| <a id="rule-rg-04"></a>RG-04 | **The route stays disabled until every gate is recorded as met** (**[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)**), enforced by configuration and verified in the release gate. |

---

## 12. Security and resilience

| # | Rule |
|---|---|
| SR-01 | **A commercial mutation is an R2-or-above operation** (`§4` of the security requirements), audited with the full actor chain. |
| SR-02 | **Provider credentials are held as `SecretRef` in the secret broker** (`§6` of the security architecture); no commerce module reads a plaintext key. |
| <a id="rule-sr-03"></a>SR-03 | **The webhook endpoint is rate-limited, signature-gated and isolated**, so it cannot be used as an amplification or enumeration surface. |
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
| CT-03 | **Resolver equivalence**: rebuilding a snapshot from grants and revocations equals the stored snapshot for every fixture account ([EN-02](#rule-en-02)). |
| CT-04 | **Concurrency suite**: parallel runs against one workspace never overdraw ([AD-02](#rule-ad-02)), reservation races across devices and replicas resolve to one outcome, and reservation expiry releases correctly. **A cancel racing a dispatch** does not release a reservation whose intent is committed, and a provider response arriving after the cancel settles against it rather than finding it gone ([CN-04](17-agent-harness.md#rule-cn-04) of the harness, [DB-03](data-model/00-data-model-overview.md#rule-db-03)). |
| <a id="rule-ct-05"></a>CT-05 | **Precision suite**: no floating-point path exists in money or credit arithmetic ([BC-06](#rule-bc-06)), asserted as a repository policy test. |
| CT-06 | **Funding-order suite**: capacity → compensation → authorised purchased credits, earliest-expiry within compensation, oldest-acquisition within purchased, and refund hold, for every combination ([CD-05](#rule-cd-05)). |
| <a id="rule-ct-13"></a>CT-13 | **Refill suite**, asserting evaluation-frequency independence as its central property: over one interval containing a **ceiling raise**, a **ceiling reduction** and a **rate change**, the result is identical whether refill runs once, at every boundary, or a thousand times at random instants. The worked case is asserted exactly — burst 10 raised to 100 at *t*=10, rate 1/s, bucket full at *t*=0 → **11 at *t*=11**, never 21 and never 12 ([RF-04](#rule-rf-04)). Plus: a lapse contributing zero; a watermark that never moves backwards under clock rollback, restart, reconnect or a racing replica; a fractional carry preserved **across period boundaries**; a reduction that stops accrual without clawing back ([RF-05](#rule-rf-05)); and the ceiling expression holding after every operation including a release and a refund ([RF-06](#rule-rf-06)). |
| CT-14 | **Normalisation suite**: two providers whose cache and reasoning fields overlap differently both settle correctly; cumulative stream snapshots replace rather than sum; a duplicate usage event does not double-debit; an undeclared usage field enters reconciliation rather than a debit ([UN-01](#rule-un-01)–[UN-06](#rule-un-06), [MT-03](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-03), [MT-05](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-05)). |
| CT-15 | **Worked-fixture suite**: the `§8.6` arithmetic is asserted exactly — USD 0.00244 supplier cost, 4,880,000 micro-credits customer cost, 1.12 credits released to the original sources ([RP-04](#rule-rp-04)). |
| CT-16 | **Uncertain-usage suite**: missing final usage, post-dispatch timeout and a lost response each produce `UsagePending`/`CostUnconfirmed`, never zero and never a fabricated total; the deadline releases the customer hold while retaining the supplier liability ([UC-01](#rule-uc-01), [UC-02](#rule-uc-02), [MT-12](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-12)). |
| CT-17 | **Beneficiary suite**: a platform-caused retry is charged once to the customer and fully visible in supplier cost; routing, abuse and health calls are platform cost ([ST-07](#rule-st-07), [MT-08](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-08)). |
| CT-18 | **Service-term suite**: official inference is refused with a full credit balance and no active term; a paid term expiring mid-Task stops further dispatch at a durable boundary; renewal re-enables retained credits without reissue ([AD-01](#rule-ad-01), [CR-05](../requirements/04-commerce-entitlement-and-credits.md#rule-cr-05), `§8.7`). |
| CT-19 | **Configuration suite**: two example policies with different rates, prices, recovery rates and grants change future decisions and leave historical charges identical; replacement during concurrent requests produces no mixed-version evaluation, quota reset or duplicate grant; all replicas restart preserving balances, holds and refill state (`§10.6` of the configuration requirements). |
| CT-20 | **Real-provider suite**: one real provider usage response and one real payment-provider event are reconciled through the same code as the fixtures. Deterministic fixtures supplement this evidence; they do not replace it ([MT-01](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-01), `§10.6` there). |
| CT-07 | **Reconciliation suite**: a dropped webhook, a duplicated order and a provider-side change are each detected and repaired without editing history. |
| CT-08 | **Immutability suite**: any attempt to update or delete a grant, revocation, payment or ledger entry fails. |
| <a id="rule-ct-09"></a>CT-09 | **Boundary suite**: no provider type or identifier format appears outside the provider adapter ([BC-07](#rule-bc-07)), asserted as an architecture test. |
| CT-10 | **Mobile prohibition suite**: the commerce checks of [MO-02](#rule-mo-02) fail the build if any purchase or unlock path is introduced. |
| CT-11 | **Evidence suite**: a dispute export for a fixture account is complete, reproducible and free of payment instrument data. |
| CT-12 | **Go-live gate**: purchase, renewal, cancellation, refund, dispute, reconciliation, capacity recovery, extra-credit opt-in and entitlement distribution are all demonstrated end to end against the provider's test environment before the paid product opens (`§18` there). |

---

## 14. Non-goals

The commerce layer is **not**: a payment processor; a holder of card data; a place where a single balance number lives; a system that trusts a redirect or a webhook without verification; a store-billing integration in the initial release; a source of retroactive price changes; or a system whose history can be edited.

---

## 15. Traceability

| Current document | Relationship |
|---|---|
| [Commerce, Entitlement and AI Credits Requirements](../requirements/04-commerce-entitlement-and-credits.md) | Owns the commercial, entitlement and metering contracts |
| [Dynamic Policy and Configuration Requirements](../requirements/11-policy-and-configuration.md) | Owns private configuration and immutable policy publication |
| [Cloud Data Model](data-model/01-cloud-data-model.md) | Defines financial ledgers, provider inbox and reconciliation records |
| **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)** | Paddle as sole Merchant of Record; Payoneer as payout destination only |
| **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** | Every figure is versioned commercial policy; immutable history; fixed-precision arithmetic; hard stop at zero |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** | The mobile consumption-only posture as a build-verifiable constraint |
| **[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)** | The Mainland China conditional route and its pre-enablement gates |
| **[V-07](../assurance/phase-1-official-verification.md#rule-v-07)** | Settlement timing does not track transaction timing |
| [I-011](../requirements/01-normative-glossary-and-invariants.md#rule-i-011) | The three ledgers are permanently separate |
