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

`DC-01`–`DC-17` of the configuration requirements make deployment configuration the production policy source. It is a **separate top-level module**, for the same reason Entitlement is: Commerce is one of its consumers, not its owner.

| # | Rule |
|---|---|
| CG-01 | **Configuration owns the bundle, its schema, validation, activation and the persisted snapshots.** Commerce, Entitlement, the Harness and the simulator all *read* an activated revision; none of them loads or validates one. |
| CG-02 | **A request records which validated revision it used** (`DC-12`). That recorded revision — not the current file — is what a later reproduction reads (`RP-02`, `I-494`). |
| CG-03 | **Activation is atomic and all replicas converge on one coherent revision** (`DC-11`, `DC-12`). A replica that cannot load the activated revision **cannot admit affected work**; it does not fall back to a previous revision or a sample. |
| CG-04 | **Runtime facts are never configuration.** Subscription state, measured tokens, usage, reservations, balances and payment facts are database records (`DC-09`). Direct SQL editing is not an alternative policy authority. |
| CG-05 | **Only an allowlisted projection reaches a client** (`DC-14`): the user's own offer and rights, published retail rates, current capacity and balance, recovery timing and availability reasons. Supplier rates, risk thresholds, route weights and other users' state never ship to a client. |
| CG-06 | **Secrets are not configuration** (`DC-15`). Provider keys, payment credentials and signing keys are injected by secret manager or Docker secret, never present in the policy file, the image, the logs or the public sample. |

---

### 2.1 Entitlement is not owned by Commerce

**`MD-05` of the cloud architecture governs**: *Commerce depends on Entitlement's grant interface, never the reverse. Entitlement must remain usable with Commerce entirely absent.* That is the authoritative ownership statement, and this document is subordinate to it.

| # | Rule |
|---|---|
| EO-01 | **Entitlement is a top-level Cloud module** ([`05-cloud-architecture.md`](05-cloud-architecture.md) `§4`). It owns definitions, bundles, grants, revocations, the resolver, snapshots, quotas and usage counters. |
| EO-02 | **Commerce is a separate top-level module.** It owns billing accounts, offers, price versions, purchase intents, checkout attempts, orders, payments, provider events, subscriptions, credits, ledgers, reconciliation and commercial evidence. |
| EO-03 | **Commerce writes into Entitlement only through Entitlement's published grant interface** — `IssueGrant`, `RevokeGrant` — never by writing Entitlement's tables (`MD-02` there: no module writes another module's tables). |
| EO-04 | **Entitlement never calls Commerce.** A grant carries its own source discriminator (`purchase`, `administrative`, `promotional`, `trial`, `store`), so Entitlement can resolve without knowing a provider exists. |
| EO-05 | **Removing Commerce entirely must leave Entitlement working**, serving free-tier and administrative grants. This is the test that keeps the boundary honest, and it is asserted in `WP-42.00`. |
| EO-06 | **Credits belong to Commerce; quota and usage belong to Entitlement.** A credit is money-adjacent and is settled against a ledger; a quota is a capability limit resolved from a grant. Conflating them was the defect this section corrects. |
| EO-07 | **The reserve-then-settle budget interface spans both**: Commerce.Credits holds the lots and performs the accounting; Entitlement answers *may this workspace spend at all*. The execution engine calls one façade that fans out to both, and that façade lives in Commerce. |

> **Correction, 2026-09-05.** An earlier revision of this document listed `Commerce.Entitlement` and `Commerce.Quota` as sub-modules of Commerce, contradicting `MD-05`. Both are removed above. Every later reference in this document to *"the entitlement resolver"* means the **Entitlement module's** resolver, reached through its published interface.

| # | Rule |
|---|---|
| MB-01 | **Only `Commerce.Providers` knows a provider exists.** Every other module speaks in ArcForges' own commercial vocabulary. |
| MB-01a | **Commerce and Entitlement are separate top-level modules** (`§2.1`). Commerce reaches Entitlement only through its grant interface. |
| MB-02 | **`BillingProviderCapabilities` is a typed capability description** (`§3.1` there), read by the rest of the system to decide what is offered — never a hard-coded assumption that a provider supports a given operation. |
| MB-03 | **A provider identifier is stored as an external reference on an ArcForges entity**, never as the entity's own identity. |
| MB-04 | **Entitlement state is read by everything and written only by the Entitlement module** — by its resolver for snapshots, and by its grant interface for grants and revocations (`§5`). |
| MB-05 | **No module computes an entitlement decision for itself.** Every caller asks the Entitlement module and receives a reasoned answer. |

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

### 5.3 The service term — the gate before every AI decision

`C-03` makes an **active paid service term** the precondition for official inference. It is a distinct concept from both entitlement capabilities and credit balance, and it is checked first (`AD-01`).

| # | Rule |
|---|---|
| SV-01 | **A service term is an interval, not a flag.** `service_term` rows record kind (`subscription` | `pass` | `compensation` | `selfHostGrant`), start, end, source order or grant reference, and realm. The effective term is the union of overlapping intervals. |
| SV-02 | **Only four things create one** (`§8.7` there): a verified subscription, a prepaid Cloud Pass (**D-023**), an audited compensation extension of an existing paid service, or — in a self-hosted realm only — an explicit operator-funded `ServiceGrant`. |
| SV-03 | **A credit grant, trial flag or operator edit cannot create one** (`§8.7` there). This is the rule that makes "credits alone do not authorise AI" enforceable rather than aspirational. |
| SV-04 | **A self-host `ServiceGrant` authorises only its own realm** (`BY-04`, `DC-16`). It confers no official-service entitlement, and no realm's grant is visible to another (`I-497` family; realm isolation in `§3`). |
| SV-05 | **Renewal grace protects data access, not AI.** During grace, retained data is readable and downloadable; **no new official inference is admitted** (`C-07`). The two windows are configured and evaluated separately. |
| SV-06 | **Term expiry during a running Task stops further dispatch at a durable boundary** with the explicit eligibility reason. Work already settled stays settled; holds are released per `§7.6`. |
| SV-07 | **Self-host billing may be disabled entirely** (`§8.7` there, `DC-16`). Identity, authorisation, real usage measurement, budget limits and accounting correctness remain enforced; only customer payment is absent. |

---

## 6. Quota and usage

> **Ownership.** Quota and usage counters belong to **Entitlement**, not Commerce (`EO-01`, `EO-06`). The rules below are stated here because commerce operations are their most common cause, not because Commerce owns the store.

| # | Rule |
|---|---|
| QA-01 | **Quota is a limit; usage is a measurement** (`§7` there). They are separate stores with separate lifecycles. |
| QA-02 | **A usage counter is authoritative server-side**, with a defined reset boundary tied to the entitlement period, not to a calendar convenience. |
| QA-03 | **Storage accounting is computed from committed objects**, never from a client-reported figure (`§8` of the cloud requirements). |
| QA-04 | **Exceeding a quota is a typed, explained refusal with a remediation path**, never a silent failure or an unbounded overage. |
| QA-05 | **Quota checks are evaluated at the same enforcement point as the operation they bound**, so a check cannot be bypassed by a different entry path. |

---

## 7. Capacity, credits and the metering path

**P2-006 replaces the reissued-allowance model with a replenishing capacity bucket plus opt-in purchased credits.** Everything in this section derives from `§8.4`–`§8.7` of the commerce requirements (`MT-01`–`MT-16`, `AC-01`–`AC-12`) and remains bound by **D-020** as amended.

### 7.1 The four separate quantities

Conflating any two of these is the defect class this section exists to prevent (`I-493`).

| Quantity | Unit | Lives in | Recovers? |
|---|---|---|---|
| **Included capacity** | Integer micro-credits | `entitlement.capacity_bucket`, one row per workspace | **Yes** — continuously, during eligible paid service, up to a burst ceiling |
| **Purchased credits** | Integer micro-credits | `commerce.credit_lot` rows | **No** — conserved; spendable only while a paid term is active |
| **Supplier cost** | Fixed-precision decimal money with currency, ≥ 9 fractional digits | `commerce.supplier_cost_entry` | n/a — an obligation ArcForges owes a provider |
| **Payment revenue** | Sale currency and amount | `commerce.ledger_entry` (payment ledger) | n/a |

| # | Rule |
|---|---|
| CD-01 | **One credit = 1,000,000 micro-credits, and every customer amount is an integer count of micro-credits** (`MT-07`). No binary floating point appears in any accounting path. |
| CD-02 | **Included capacity is a bucket, not a lot.** It has a burst ceiling and a recovery rate, both deployment parameters (`AC-01`), and it is never modelled as a credit lot with an expiry. |
| CD-03 | **Purchased credits are lots and are conserved** (`AC-11`). They do not expire with time or cancellation (`CR-03`), survive service expiry, and become spendable again on renewal without reissue (`CR-05`). |
| CD-04 | **Compensation lots are lots with a disclosed expiry** (`CR-03`), consumed earliest-expiry-first. |
| CD-05 | **Consumption order is fixed**: included capacity, then eligible compensation, then purchased credits — and purchased credits only under an explicit extra-usage authorisation (`CR-04`, `AC-06`). |
| CD-06 | **A reservation preserves its source allocation.** Settlement debits and releases against the same sources it reserved from; there is no silent conversion between pools (`CR-04`, `AC-11`). |
| CD-07 | **Capacity and purchased credits are presented separately, never summed** (`§8.3` there), because one recovers and the other does not. |

### 7.2 The refill algorithm

This is the part most likely to be got wrong, so it is specified rather than described. It runs on read, under the bucket row's own lock.

```
refill(bucket, now):
    eligible = overlap(bucket.watermark .. now, workspace's eligible paid intervals)
    if eligible <= 0:                          # lapsed, or clock went backwards
        bucket.watermark = max(bucket.watermark, now)   # monotonic, never backwards
        return                                          # AC-02, AC-12

    earned_exact  = eligible * rate_per_second + bucket.remainder_micro
    earned_whole  = floor(earned_exact)
    bucket.remainder_micro = earned_exact - earned_whole   # fractional carry, AC-12

    ceiling = max(0, bucket.burst - bucket.held)           # AC-11
    bucket.available = min(bucket.available + earned_whole, ceiling)
    bucket.watermark = now
```

| # | Rule |
|---|---|
| RF-01 | **Recovery accrues only over the overlap with eligible paid intervals** (`AC-02`). A lapse contributes zero; capacity does not accumulate during a gap (`AC-03`). |
| RF-02 | **The watermark advances monotonically and is durable** (`AC-12`). Reconnect, process restart, another device, another replica or a clock rollback cannot rewind it or refill the bucket. |
| RF-03 | **The fractional remainder is preserved across evaluations** (`AC-12`). Without it, frequent small requests would round the recovery rate down and slow requests would round it up — either way the contractual rate would not be delivered. |
| RF-04 | **The ceiling counts held capacity** (`AC-11`): `available ≤ max(0, burst − held)`. This is what stops a large outstanding hold from coexisting with a full bucket and effectively doubling the burst. |
| RF-05 | **Returned capacity is capped by the same ceiling.** Releasing a hold or issuing a refund must never mint spendable capacity above the burst (`AC-11`). |
| RF-06 | **Purchased credits never refill** (`AC-11`). They have their own conservation ledger, and no code path adds to a purchased lot except a purchase, a compensation grant or an explicit adjustment. |
| RF-07 | **First paid activation initialises the bucket once under an idempotent grant** keyed by the service term (`AC-03`). Contiguous renewal extends the eligible interval and does **not** refill to full. |
| RF-08 | **A configuration change applies at a recorded boundary** without resetting the watermark, releasing holds or reissuing capacity (`AC-12`, `DC-13`). |

### 7.3 Admission

Admission is one atomic decision, not a sequence of independent checks (`AC-04`).

```
admit(request):
    verify active paid service term                     # C-03, §8.7 — fails first, cheapest
    resolve customer tariff snapshot (pin to Run)       # MT-06
    resolve supplier price version (dispatch-time)      # MT-06
    bound = conservative ceiling over input, output/reasoning, and
            separately billed tools, from the actual route            # MT-15
    if bound is unpriceable or unbounded:  reject                     # MT-15, DC-05
    ATOMIC:
        refill(bucket, now)                                           # §7.2
        check workspace concurrency, per-request and per-run ceilings  # AC-04
        check provider budget                                          # AC-04
        reserve bound from  capacity -> compensation -> purchased      # CD-05
    if insufficient:  WaitingForCapacity(recovery_time) | ExtraCreditsRequired | Reject
```

| # | Rule |
|---|---|
| AD-01 | **The service-term check precedes everything.** No credit balance, trial flag, operator edit or self-host setting substitutes for it (`§8.7`, `C-03`). |
| AD-02 | **Admission reserves atomically.** Concurrent runs on one workspace, across devices and replicas, cannot each pass a check against the same unreserved balance (`CR-21`, `AC-04`). |
| AD-03 | **A request whose bound can never fit capacity plus authorised extra credits is rejected immediately** with a smaller-request or budget action — never queued forever (`AC-04`). |
| AD-04 | **An unbounded or unpriceable route cannot enter paid service** (`MT-15`, `DC-05`). There is no assumed zero-rate category and no wildcard model entry. |
| AD-05 | **Exhausted capacity waits for a server-calculated recovery time** (`AC-06`). Purchased credits are used only after the user enables extra usage with a maximum budget; there is no automatic purchase, recharge or paid fallback. |
| AD-06 | **Background automation spends only within its previously authorised budget** (`AC-06`). |
| AD-07 | **Rate limits, safety limits and provider availability remain enforceable even with extra credits** (`AC-09`). |
| AD-08 | **All entry points share one workspace pool** (`AC-07`). Desktop, Web, Mobile and automation consume the same capacity and credits; changing model changes consumption through the tariff, never by granting a new allowance. |

### 7.4 Usage normalisation

Provider usage shapes differ, so a normaliser turns each provider's report into **non-overlapping** ArcForges billing categories (`MT-03`).

| Category | Meaning |
|---|---|
| `input.uncached` | Input tokens billed at the full input rate |
| `input.cached_read` | Input tokens served from a provider cache |
| `input.cache_write` | Cache-creation tokens, per supported class |
| `output` | Output tokens, **inclusive of reasoning where the provider bills them together** |
| `output.reasoning` | Only where a provider bills reasoning as a separately priced category |
| `tool.<kind>` | Separately billed search, tool or media operations, with explicit quantity, unit and rate (`MT-10`) |

| # | Rule |
|---|---|
| UN-01 | **Each provider adapter declares its inclusion relationships**, and the normaliser asserts them (`MT-03`). Reasoning already inside `output`, and cached tokens already inside a reported input total, must not be charged twice. |
| UN-02 | **A category the adapter does not declare cannot be billed.** An unrecognised usage field enters reconciliation, never an automatic debit (`MT-05`). |
| UN-03 | **Streaming cumulative usage replaces the previous total for that attempt** (`MT-05`, `I-492`). It is never summed as independent consumption. |
| UN-04 | **Pre-call counting is an estimate for admission only** (`MT-05`, `I-492`). Local text-length estimates and client-reported counters are never final cost authority. |
| UN-05 | **Quantities are validated** — non-negative, matching request and model identity, matching the declared category semantics. A mismatch enters reconciliation (`MT-05`). |
| UN-06 | **Tier resolution uses actual request facts** (`MT-04`): context, processing and region tier come from what the request really was, not from a per-model flat rate. Each applied modifier is recorded exactly once. |

### 7.5 Settlement

```
cost      = Σ over categories:  quantity × configured_rate ÷ unit_divisor      # MT-04
supplier  = cost at the dispatch-time supplier price version, as decimal money  # MT-06, MT-07
customer  = cost at the Run's pinned retail tariff snapshot, as micro-credits   # MT-06, MT-07
```

| # | Rule |
|---|---|
| ST-01 | **Settlement happens once per logical request**, after category aggregation, with declared half-even rounding — never per stream fragment (`MT-07`). |
| ST-02 | **Reservation rounds conservatively upward; settlement rounds the aggregate** (`MT-07`). |
| ST-03 | **Settlement is idempotent per attempt usage revision and per logical request** (`MT-11`). Duplicate or reordered events never double-debit; genuinely distinct retries remain distinct supplier-cost records. |
| ST-04 | **A correction is an appended adjustment linked to the original records**, never an edit (`MT-11`, `CR-10`, **D-020**). |
| ST-05 | **Settlement debits the sources the reservation held** and releases only their unused allocation (`CD-06`, `AC-11`). |
| ST-06 | **Supplier cost is retained even when the customer is not charged** (`MT-09`). A platform failure releases the customer hold or appends a compensating adjustment; the money ArcForges owes upstream does not disappear. |
| ST-07 | **Beneficiary classification decides who pays** (`MT-08`). Delivered user-requested inference consumes capacity or authorised credits. Routing, abuse checks, health checks, admitted background indexing and platform-caused retries are **platform cost** — recorded, budgeted, and not charged to the user. |
| ST-08 | **Money always carries currency** (`MT-16`). V1 supplier budgets compare within one currency; there is no implicit FX conversion. Customer credits are currency-independent service units. |

### 7.6 Uncertain and missing usage

| Situation | State | Behaviour |
|---|---|---|
| Final usage never arrives | `UsagePending` | Reconcile from available provider evidence; **never zero cost, never a fabricated total** (`MT-12`) |
| Timeout after dispatch | `CostUnconfirmed` | Same. **No blind redispatch** and no repeat charge (`MT-12`) |
| Response lost in transit | `CostUnconfirmed` | Same |
| Reconciliation deadline passes unresolved | Resolved-by-policy | **Release the customer hold** with no surprise later debit; **retain the unresolved supplier liability**; alert and restrict the affected route (`MT-12`) |
| Verified supplier overrun beyond the authorised hold | Operator cost incident | **Not customer overdraft.** Block further dispatch on that route, reconcile, adjust — without erasing the real supplier usage (`MT-15`) |
| Caller cancels | Partial | Settle verified consumption already incurred within the authorised ceiling; release the remainder. Completed provider work is not presumed refundable (`MT-09`) |

| # | Rule |
|---|---|
| UC-01 | **`unknown` is never silently resolved to zero.** A missing usage report is a state with a deadline, not an absence of cost (`MT-12`). |
| UC-02 | **The customer-protection deadline and the supplier-liability record are independent.** Releasing one does not clear the other (`MT-12`). |
| UC-03 | **Estimated, usage-confirmed and invoice-reconciled cost remain three distinguishable values** for the same request (`MT-13`). |

### 7.7 Reproducibility

| # | Rule |
|---|---|
| RP-01 | **Every metering record carries the full identity chain** (`MT-14`): workspace, service term, logical request, run, attempt, reservation, usage revision, supplier price version, customer tariff snapshot, funding source, debit and any adjustment. |
| RP-02 | **A historical charge is reproducible after model retirement or configuration replacement** (`MT-14`). Snapshots are persisted facts, not lookups into current configuration (`I-494`). |
| RP-03 | **Replacing configuration never resets usage, replenishes an issued allowance, reissues purchased credits or releases unresolved reservations** (`DC-13`). |
| RP-04 | **The worked fixture of `§8.6` is an executable acceptance test**, not documentation: 800 uncached + 200 cached input + 100 output settles to USD 0.00244 supplier cost and 4,880,000 micro-credits customer cost, with a 6-credit hold releasing 1.12 credits to its original sources.

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
| CT-04 | **Concurrency suite**: parallel runs against one workspace never overdraw (`AD-02`), reservation races across devices and replicas resolve to one outcome, and reservation expiry releases correctly. |
| CT-05 | **Precision suite**: no floating-point path exists in money or credit arithmetic (`BC-06`), asserted as a repository policy test. |
| CT-06 | **Funding-order suite**: capacity → compensation → authorised purchased credits, earliest-expiry within compensation, oldest-acquisition within purchased, and refund hold, for every combination (`CD-05`). |
| CT-13 | **Refill suite**: recovery accrues only over eligible paid intervals; a lapse contributes zero; the watermark never moves backwards under clock rollback, restart, reconnect or a racing replica; the fractional remainder is preserved so that many small evaluations deliver the same total as one large one; and `available ≤ max(0, burst − held)` holds after every operation including a refund (`RF-01`–`RF-06`). |
| CT-14 | **Normalisation suite**: two providers whose cache and reasoning fields overlap differently both settle correctly; cumulative stream snapshots replace rather than sum; a duplicate usage event does not double-debit; an undeclared usage field enters reconciliation rather than a debit (`UN-01`–`UN-06`, `MT-03`, `MT-05`). |
| CT-15 | **Worked-fixture suite**: the `§8.6` arithmetic is asserted exactly — USD 0.00244 supplier cost, 4,880,000 micro-credits customer cost, 1.12 credits released to the original sources (`RP-04`). |
| CT-16 | **Uncertain-usage suite**: missing final usage, post-dispatch timeout and a lost response each produce `UsagePending`/`CostUnconfirmed`, never zero and never a fabricated total; the deadline releases the customer hold while retaining the supplier liability (`UC-01`, `UC-02`, `MT-12`). |
| CT-17 | **Beneficiary suite**: a platform-caused retry is charged once to the customer and fully visible in supplier cost; routing, abuse and health calls are platform cost (`ST-07`, `MT-08`). |
| CT-18 | **Service-term suite**: official inference is refused with a full credit balance and no active term; a paid term expiring mid-Task stops further dispatch at a durable boundary; renewal re-enables retained credits without reissue (`AD-01`, `CR-05`, `§8.7`). |
| CT-19 | **Configuration suite**: two example policies with different rates, prices, recovery rates and grants change future decisions and leave historical charges identical; replacement during concurrent requests produces no mixed-version evaluation, quota reset or duplicate grant; all replicas restart preserving balances, holds and refill state (`§10.6` of the configuration requirements). |
| CT-20 | **Real-provider suite**: one real provider usage response and one real payment-provider event are reconciled through the same code as the fixtures. Deterministic fixtures supplement this evidence; they do not replace it (`MT-01`, `§10.6` there). |
| CT-07 | **Reconciliation suite**: a dropped webhook, a duplicated order and a provider-side change are each detected and repaired without editing history. |
| CT-08 | **Immutability suite**: any attempt to update or delete a grant, revocation, payment or ledger entry fails. |
| CT-09 | **Boundary suite**: no provider type or identifier format appears outside the provider adapter (`BC-07`), asserted as an architecture test. |
| CT-10 | **Mobile prohibition suite**: the commerce checks of `MO-02` fail the build if any purchase or unlock path is introduced. |
| CT-11 | **Evidence suite**: a dispute export for a fixture account is complete, reproducible and free of payment instrument data. |
| CT-12 | **Go-live gate**: purchase, renewal, cancellation, refund, dispute, reconciliation, capacity recovery, extra-credit opt-in and entitlement distribution are all demonstrated end to end against the provider's test environment before the paid product opens (`§18` there). |

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
