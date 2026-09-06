# Commerce, Entitlement and AI Credits Requirements
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: **D-005** (Paddle MoR, Payoneer payout), **D-020** (economic model), **D-022** (mobile commerce), **D-023** (mainland China)
> Companions: [`02-identity-account-and-workspace.md`](02-identity-account-and-workspace.md), [`05-ai-and-agent-execution.md`](05-ai-and-agent-execution.md), [`../architecture/16-billing-and-commerce-architecture.md`](../architecture/16-billing-and-commerce-architecture.md)

Two layers, permanently separated:

| Layer | Answers | Authority |
|---|---|---|
| **Commerce** | Did money change hands, for what, under which terms? | The payment provider is authoritative for payment facts |
| **Entitlement** | What may this Workspace do right now? | **ArcForges is always authoritative** |

> The client never asks the payment provider whether a subscription is active. It asks ArcForges what entitlements it currently holds.

---

## 1. Provider baseline

| # | Requirement | Authority |
|---|---|---|
| PV-01 | **Paddle is the sole customer-facing Merchant of Record** for ArcForges web and cloud commerce. It owns checkout, subscriptions, recurring billing, applicable sales-tax and VAT handling, compliant invoices, refunds, chargebacks and payment webhooks. | D-005, V-06 |
| PV-02 | **Payoneer is the payout and settlement destination only.** It is not a second Merchant of Record, not an interchangeable checkout provider, and not a customer-facing fallback processor. It never appears in a customer-facing flow, never issues an entitlement, and never appears in a client authority contract. | D-005, V-07 |
| PV-03 | **Waffo Pancake is obsolete and SUPERSEDED.** It must not be verified, recommended, integrated, or included in any specification, roadmap, dependency, runtime component or implementation step. | D-005 |
| PV-04 | The Merchant-of-Record relationship is a **commercial and tax fact, not an architectural one**. It must not propagate into domain contracts. | V-06 |
| PV-05 | **Provider identifiers never reach the client.** The client knows `ArcForges Cloud Monthly`, never a provider product id. Purchase flows resolve provider mapping server-side. | D-005 |
| PV-06 | Any provider secret, API key or signing key exists **only** in the ArcForges Cloud backend. It must never enter a desktop product, a mobile build or the browser bundle. | D-005 |
| PV-07 | Test and production environments are fully isolated, with separate provider credentials. A test environment must never hold a production key. | Stage 3 §43 |

### 1.1 Responsibility split

| Provider is authoritative for | ArcForges is authoritative for |
|---|---|
| Whether payment actually occurred | Who the user is |
| Amount, currency, tax amount | Which Workspace is entitled |
| Payment status | Whether ArcForges Cloud is available |
| Provider subscription status | Cloud expiry (`PaidThrough`) |
| Refunds and chargebacks | Storage quota |
| Invoices | AI allowance and purchased credit balance |
| End-customer payment method | Cloud AI and authorised desktop-tool entitlement |
| | Single-owner workspace product status |

`Provider subscription == active` must **never** be read directly by a client as "the user is entitled".

---

## 2. Product catalogue

Structural product shapes are fixed; all amounts are versioned commercial policy (**D-020**).

| Offer | Shape | Purpose |
|---|---|---|
| **ArcForges Cloud — recurring (monthly)** | Provider subscription product | Recurring cloud entitlement |
| **ArcForges Cloud — recurring (annual)** | Provider subscription product | Recurring cloud entitlement, discounted cadence |
| **ArcForges Cloud Pass** | One-time product, fixed 365-day term, **no auto-renewal** | Serves users who cannot or will not use a recurring method — required by **D-023**, because WeChat Pay supports no subscriptions at all and Alipay carries a renewal ceiling |
| **Arc AI Credits** | One-time products in several denominations | Prepaid managed-AI usage credits |
| **Storage add-ons** (later) | Recurring or one-time quota grants | Additive storage quota |

| # | Requirement |
|---|---|
| CT-01 | **Monthly, annual and Pass grant the same Cloud entitlement bundle.** Purchase method differs; entitlement does not. The annual advantage is price, never a different feature or quota set. |
| CT-02 | A provider may require separate provider-side products per billing period. That is an **adapter-level** concern. ArcForges must not model monthly and annual as two different business products. |
| CT-03 | Arc AI Credits are non-transferable prepaid service units, with no cash value or withdrawal/trading facility. Purchase and consumption require an active official paid service term; credit ownership alone never enables AI. |
| CT-04 | V1 sells one suite offer, not per-product plans. `ProductScope` is modelled from day one (`suite`, and per-product values) so a later split needs no data-model change (`C-10`). |
| CT-05 | V1 implements the suite subscription, the existing Cloud Pass, extra credit purchases and support compensation. Trials, coupons, referrals, seats and promotional campaigns are not required. |
| CT-06 | Duplicate-entitlement purchases are prevented: an active subscription blocks Pass purchase; an active Pass either blocks or defers a new subscription so two sources do not both set `PaidThrough`. |
| CT-07 | Repeated Pass purchase **extends** rather than replaces: `newStart = max(currentPaidThrough, purchaseTime)`, `newPaidThrough = newStart + term`. No remaining time is lost. |
| CT-08 | Pass accrual is capped (proposed default: 36 months into the future) because cloud costs, prices and product shape change. Purchases beyond the cap are refused. |

---

## 3. Pricing, currency and tax

| # | Requirement |
|---|---|
| PC-01 | The price model is `Offer → PriceVersion → RegionalPrice`. A price change creates a new `PriceVersion`; existing purchases retain the version they were bought under. |
| PC-02 | **ArcForges never computes tax.** As Merchant of Record, Paddle calculates, collects and remits applicable sales tax, VAT and GST. ArcForges supplies the offer, the suggested price and a tax category; the provider determines final checkout tax and the invoice. Reimplementing provider tax logic is prohibited. |
| PC-03 | Every pricing surface states that final price and applicable taxes are determined at checkout. |
| PC-04 | **CNY product pricing is required, not forbidden**, for the mainland-China route. Paddle's Alipay route requires CNY-priced products and conditions approval on it (V-08). This inverts the corpus's earlier position and is absorbed by **D-023**'s "CNY product and tax configuration" gate. |
| PC-05 | **Provider caps, currencies, approval rules and platform limitations must never be hard-coded into domain contracts** (**D-023**). They are expressed through `BillingProviderCapabilities` and verified commercial configuration. |
| PC-06 | Dynamic or server-overridden pricing, where used, is decided **only** by the ArcForges server. A client must never be able to propose a price. |

### 3.1 `BillingProviderCapabilities`

A first-class, load-bearing concept (**D-005**, made concrete by **V-08**), because payment methods differ materially from each other and from cards:

| Capability dimension | Why it varies |
|---|---|
| Supports recurring | WeChat Pay supports **no subscriptions** |
| Supports one-time | Universally supported |
| Supported currencies | Alipay is **CNY only**; WeChat Pay is CNY or USD |
| Supported platforms | WeChat Pay is **desktop only** |
| Renewal/charge cap | Alipay caps subscription renewals and charges; payments above the cap fail into dunning |
| Requires separate approval | Alipay requires a separate Paddle approval application |
| Supports chargebacks | **Neither Alipay nor WeChat Pay supports chargebacks** |
| Supports saved payment methods | Neither China method does |
| Supports plan switch | Provider-dependent; must not be assumed |
| Supports partial refund | Provider-dependent |
| Supports customer portal | Provider-dependent |

Business logic must branch on capability, never on provider name.

---

## 4. Purchase flow

```
Signed-in user
      ↓ selects Workspace
Purchase Intent            (ArcForges; idempotency anchor)
      ↓
Checkout Attempt           (ArcForges; carries internal ids as metadata)
      ↓
Provider hosted checkout
      ↓ payment
Provider webhook  ──────►  Provider Event Inbox
      ↓ verify signature, provider, store, product mapping,
        purchase intent, buyer identity, payment state, prior processing
Order + Payment recognised
      ↓
Entitlement Grant created
      ↓
Entitlement Resolver recomputes the Workspace
      ↓
New Entitlement Snapshot; EntitlementVersion++
      ↓ realtime notification
Clients refresh from the Entitlement API
```

| # | Requirement |
|---|---|
| PF-01 | **Checkout requires a signed-in ArcForges account and a selected Workspace.** Anonymous purchase of Cloud or AI Credits is not permitted, because entitlement must be issued to a specific Workspace. |
| PF-02 | **Buyer identity is a stable internal billing identity**, never an email address. A payment email such as `finance@company.com` must never determine ownership. Changing the account email must never lose a subscription. |
| PF-03 | Checkout binds BillingAccountId, WorkspaceId, OfferId, PriceVersionId, CheckoutAttemptId and PurchaseIntentId server-side. Email changes do not change ownership. Cross-owner workspace transfer is not a supported purchase path. |
| PF-04 | **A success redirect is never payment authority.** After returning from checkout the product shows a "confirming payment" state and waits for verified provider events. Granting entitlement from a redirect URL would be forgeable. |
| PF-05 | Purchases are idempotent end to end: one `PurchaseIntent` yields at most one valid checkout; double-clicking Buy never produces two orders. |

### 4.1 Provider Event Inbox

| # | Requirement |
|---|---|
| EV-01 | Every provider event is persisted before processing: provider, event id, event type, received time, raw payload, signature verification result, processing status, retry count. |
| EV-02 | **Idempotency key is `eventType + eventId`.** The same event may affect business state exactly once, however many times it is delivered. |
| EV-03 | Signature verification is mandatory. An unverified event is recorded and rejected, never processed. |
| EV-04 | Webhook handling returns quickly and processes asynchronously. |
| EV-05 | **A webhook is a trigger, never unconditional belief.** The processing chain validates: signature → known provider → known store → known product mapping → known purchase intent / buyer identity → valid payment state → not already processed → grant. |

### 4.2 Reconciliation

| # | Requirement |
|---|---|
| RC-01 | Periodic reconciliation compares ArcForges commercial state against provider orders and subscriptions in both directions, and repairs divergence. |
| RC-02 | **Losing one webhook must never permanently cost a user their subscription.** Reconciliation is the second line of defence, not an optional extra. |
| RC-03 | Settlement lags transactions materially (payout cycles run on a monthly rhythm with a further transfer delay). **The reconciliation model must not assume payout timing tracks transaction timing** (V-07). |

---

## 5. Subscription lifecycle

Provider subscription states are **normalised** into ArcForges states. The provider's raw state is retained as `ExternalProviderStatus` for diagnostics only.

| ArcForges state | Meaning |
|---|---|
| `Pending` | Purchase initiated, not yet confirmed |
| `Active` | Entitlement valid through `PaidThrough` |
| `Grace` | Renewal failed; data continuity follows grace policy; no paid AI after PaidThrough |
| `CancelScheduled` | Auto-renewal off; entitlement continues to `PaidThrough` |
| `Ended` | `PaidThrough` elapsed |
| `Suspended` | Administrative or risk suspension |

| # | Requirement |
|---|---|
| SU-01 | Paid service eligibility requires server time before PaidThrough, a valid grant and no effective suspension/revocation. A raw provider status never authorises an operation. Renewal grace after PaidThrough is a separate data-access policy, not paid AI eligibility. |
| SU-02 | **`CancelScheduled` ≠ access removed.** The user interface says "Cancellation scheduled — Cloud remains active until \<date\>", never "Canceled". Reactivation before period end is supported where the provider supports it. |
| SU-03 | `AutoRenew = false` and `EntitlementActive = true` are two independent facts and must never be merged into one flag. |
| SU-04 | Failed renewal enters Grace for data continuity according to the published policy. After PaidThrough, no new model calls, embedding jobs, paid tools or AI automation dispatch; included capacity stops replenishing and extra credits remain locked. Already dispatched work is reconciled and settled, never forgotten. |
| SU-05 | After grace, CloudRestricted blocks new sync writes, uploads, simulations and AI. Sign-in, reading/downloading retained data, export and billing management remain available during retention. No pending local work is deleted. |
| SU-06 | Recovery is immediate and automatic on successful payment. It must not require re-sign-in, reinstall or a support ticket. |
| SU-07 | The grace duration is configuration, never hard-coded and never inherited from provider behaviour. |
| SU-08 | Plan switching (monthly ↔ annual) is modelled as a `PlanChangeIntent`. Where a provider does not support in-place switching, the supported experience is cancel-at-period-end followed by a new purchase, and the intent model records the user's stated goal so the switch can be automated later without a data-model change. |

---

## 6. Entitlement model

### 6.1 Four distinct entitlement kinds

`IsPro = true` is prohibited. Entitlements are of four kinds with different resolution rules:

| Kind | Example | Result shape | Combination rule |
|---|---|---|---|
| **Capability** | `cloud.sync`, `cloud.remote_agent`, `cloud.ai`, `cloud.vector_index`, `cloud.version_history`, `cloud.web_continuity` | Enabled / Disabled | Valid sourced grant AND paid-service eligibility where required; administrative credit alone never enables official AI |
| **Quota** | `cloud.storage.bytes` | A quantity | **SUM** — base plus add-ons |
| **Allowance** | included AI capacity | A bounded quantity recovering over eligible elapsed time | One workspace capacity account; no duplicate issuance |
| **Consumable balance** | Purchased AI credits | A ledger balance | Ledger computation, never resolver arithmetic |

Two further combination rules exist for later use: **MAX** (e.g. two valid device-limit grants resolve to their declared maximum, not their sum) and **priority replace** (e.g. support level).

### 6.2 Ownership and separation

| # | Requirement |
|---|---|
| EN-01 | Entitlement belongs to a single-owner Workspace. The owner UserId and explicit actor/resource authorisation are required; no organisation workspace, member role or team credit pool exists. |
| EN-02 | **Billing Account pays; Workspace receives.** `Billing Account → Commercial Purchase → Workspace → Entitlements`. Who pays and who uses are different concepts. |
| EN-03 | Native editing, acquisition, playback, rendering and pending-edit recovery do not consume AI entitlement. No local AI, local embedding, local agent or BYOK capability is defined. |
| EN-04 | **Entitlement ≠ Feature Flag** (`I-004`). A feature flag says whether a capability has shipped; entitlement says whether a workspace may use it. |
| EN-05 | **Entitlement ≠ Authorization** (`I-238`). `cloud.notes = enabled` says the workspace may use cloud notes; it never says a given actor may read a given document. Resource access always goes through authorization. |
| EN-06 | **No product computes its own entitlement.** Every product consumes one resolved snapshot from one resolver. Per-product logic such as `if provider status == active` is prohibited. |

### 6.3 Bundles and versioning

| # | Requirement |
|---|---|
| BN-01 | Entitlement bundles are **defined data, not code**. `if plan == Cloud { storage = X; remote = true }` is prohibited. |
| BN-02 | Bundles are **versioned**. A later bundle version may change quota or allowance; existing subscribers are either migrated or grandfathered by explicit commercial policy, resolved by the entitlement layer without code change. |
| BN-03 | A bundle change is a **catalogue release event** carrying version, effective date, affected offers, existing-subscriber policy and migration behaviour. An administrator editing a number in place is prohibited. |
| BN-04 | Entitlements carry a `scope`. V1 grants use `scope = suite`; the model supports `scope = product:<appId>` without a schema change. |

### 6.4 Grants and revocations

| # | Requirement |
|---|---|
| GR-01 | Effective entitlement is **derived from grants**, never stored as a mutable end state. "Storage = 150 GB" must always be explainable as a sum of sourced grants. |
| GR-02 | Grant sources are Subscription, CloudPass, StorageAddOn, PurchasedCredit, AdminGrant, Migration and Compensation. Each names its originating transaction or audited administrative action. No TeamPlan source is required. |
| GR-03 | **Grants are immutable; loss is expressed as a Revocation.** A refund or chargeback creates an `EntitlementRevocation` against the original grant rather than mutating its validity window. This is what makes refunds, chargebacks, fraud handling, administrative correction and account migration auditable. |
| GR-04 | Compensation is a first-class grant, never a silent date adjustment. "Add 7 days for incident X" is a `Compensation` grant with a reason, not `expiry += 7`. |
| GR-05 | Administrative grants require reason, operator, created-at, starts-at, ends-at, ticket or incident reference, and an audit record. Direct database modification is prohibited. |
| GR-06 | **Entitlement records are never physically deleted.** Grants, revocations, capacity history and credit lots are retained as commercial audit data, because support, refunds, chargebacks, finance, migration and audit all depend on them. |
| GR-07 | A durable subscription source and idempotent paid-service periods enable the configured included-capacity policy. Renewals extend eligibility without issuing duplicate capacity or resetting usage. Annual and prepaid terms use the same time-based policy; no twelve-month upfront AI grant. |

### 6.5 Effective entitlement snapshot

| # | Requirement |
|---|---|
| ES-01 | Clients consume an **Effective Entitlement Snapshot**, never grants, revocations, subscriptions or provider state. |
| ES-02 | Each entitlement in the snapshot carries a **reason** when unavailable: `available`, `no_entitlement`, `subscription_expired`, `payment_grace`, `quota_exceeded`, `temporarily_restricted`, `workspace_suspended`, `feature_unavailable`. A bare `false` produces "something went wrong" user interfaces. |
| ES-03 | The snapshot carries an **`EntitlementVersion`** that increments on every effective change, so clients can cheaply detect staleness. |
| ES-04 | Realtime notification announces that entitlement changed; **it is never the source of the new state**. The client re-reads from the entitlement API. A lost realtime message, an offline app or a backgrounded phone must not produce a wrong state. |
| ES-05 | Clients cache the last verified snapshot and tolerate a bounded offline window (proposed default: 24 hours) so a transient cloud outage does not present as "your subscription ended". The cached snapshot is a **UX** measure only. |
| ES-06 | Cloud re-evaluates identity, paid service term, policy, capacity and authorisation before each model/paid-tool dispatch and each other protected Cloud operation. A client assertion or cached entitlement is never authority. |
| ES-07 | An **Entitlement Explain** view exists for support: it renders the derivation ("Base Cloud +50 GB; Storage add-on +100 GB; add-on ended −100 GB; effective 50 GB") so a support agent never guesses. |

### 6.6 Composite availability

A capability is available only when **all** of the following hold:

```
Product feature exists (feature flag / release state)
AND Entitlement allows it
AND Workspace policy allows it
AND Device / user setting allows it
```

Worked example — Remote Agent: feature flag GA, entitlement yes, workspace policy yes, **device consent no** → final: **not available**. **A commercial entitlement can never override a security authorization or a user's device consent.**

---

## 7. Quota and usage

| # | Requirement |
|---|---|
| QU-01 | **Quota and Usage are separate data domains.** Storing only `remaining` is prohibited; purchasing an add-on must naturally change quota while usage is untouched. |
| QU-02 | Storage quota is workspace-shared, not per product (`C-09`). |
| QU-03 | **A quota downgrade never deletes data.** Usage above quota enters `Over Quota`: new uploads blocked; existing files readable; downloads allowed; deletion allowed. Dropping below quota automatically restores writes. |
| QU-04 | Quota presentation is explainable, showing the base grant, each add-on, and the resulting total, plus a per-product usage breakdown including versions and trash. |

---

## 8. AI credits

### 8.1 Ledger model

| # | Requirement |
|---|---|
| CR-01 | AI credits use a **Credit Ledger with Credit Lots**, never a single balance number. |
| CR-02 | A purchased/compensation lot records source, grant/purchase reference, original amount, available/reserved/consumed amounts, creation, applicable term version and refund status. Current numerical balance is derived from immutable entries. |
| CR-03 | IncludedCapacity is a replenishing subscription allowance, separately recorded from purchased CreditLots. V1 purchased credits do not expire merely with time or subscription cancellation; refunds, chargebacks and account deletion follow their explicit settlement rules. Compensation lots carry disclosed expiry. |
| CR-04 | Use available included capacity first, then eligible compensation, then purchased credits only with explicit extra-usage authorisation. Compensation consumes earliest expiry first; purchased lots consume oldest acquisition first. Reservations preserve source allocation; no silent conversion between pools. |
| CR-05 | Purchased credits survive service expiry but cannot be spent until a paid service term is active again. Renewal re-enables the retained balance without reissuing or transferring it. Expiry never causes a credit-only AI fallback. |
| CR-06 | Monthly, annual and prepaid service terms use the same continuous included-capacity recovery policy. Paid-period transitions do not reset consumed usage or duplicate grants. |
| CR-07 | **Three ledgers are permanently separate** (`I-011`): the **provider cost ledger**, the **customer credit ledger**, and the **payment/revenue ledger**. |
| CR-08 | Credit accounting uses **fixed-precision arithmetic**. Floating-point accumulation is prohibited (**D-020**). |
| CR-09 | Each run carries a **tariff snapshot**, so a historical charge is always explainable against the rates in force at the time (**D-020**). |
| CR-10 | Historical financial records are **immutable** (**D-020**). |

### 8.2 Reservation and settlement

| # | Requirement |
|---|---|
| CR-20 | Credits are **reserved before execution and settled afterwards**. Three quantities exist: `Available`, `Reserved`, `Consumed`. |
| CR-21 | Concurrent agent runs must not each independently pass a balance check against the same unreserved balance. Reservation is what prevents overdraft under concurrency. |
| CR-22 | On completion the actual consumption is debited and the unused reservation released. |
| CR-23 | No customer overdraft. Exhausted included capacity waits for recovery, or uses explicitly authorised extra credits within the task budget. With neither available, no new provider call starts. The UI states the reason and recovery/action path; no BYOK fallback. |
| CR-24 | A refund request places the corresponding lot into **`RefundHold`**, freezing the affected amount, so the balance under review cannot be spent while the request is adjudicated. |

### 8.3 Presentation

Allowance and purchased credits are **displayed separately**, never summed into one figure, because included capacity recovers only during eligible service while purchased credits persist and require service reactivation to spend. Show recovery timing, any compensation expiry and extra-credit consent separately.

---

### 8.4 Token metering contract

| # | Requirement |
|---|---|
| MT-01 | Implement a real provider-usage normaliser, price resolver, capacity/reservation evaluator, settlement path and durable ledger. Public sample configuration must exercise this same code. Interfaces, fixed success responses or in-memory mock balances are not completion evidence. |
| MT-02 | Each LogicalAIRequest may produce multiple ProviderAttempts. Record each actual attempt and its provider request identity, concrete model/version, route, processing/context/region tier, timestamps, usage source, completeness state and cost-version reference. Do not log prompts or content in the billing evidence. |
| MT-03 | Meter non-overlapping provider-billable categories: uncached input, cached input/read, cache creation by supported class, output and any separately billed token modality. A normaliser must state inclusion relationships; reasoning already included in output and cached tokens already included in input must not be charged twice. |
| MT-04 | Cost is the sum of each billable quantity multiplied by its configured category rate and unit divisor. The applicable context/processing/region tier is resolved from actual request facts; no universal per-model flat token price or silent default rate. Record applied modifiers exactly once. |
| MT-05 | Pre-call token counting is an estimate used for admission/reservation. Final consumption uses provider-reported billable usage. Local text-length estimates and client-reported counters are never final cost authority. Streaming cumulative usage replaces earlier totals for that attempt; it is not summed as independent consumption. Validate non-negative quantities, request/model identity and declared category semantics; invalid or mismatched evidence enters reconciliation, never an automatic debit. |
| MT-06 | Cost, customer service units and collected revenue are distinct. Cost uses the supplier price version applicable at dispatch; customer units use the Run's retail tariff snapshot (per request for ordinary chat). Upstream changes never retroactively alter customer tariffs or purchased lot balances. |
| MT-07 | Record supplier amounts as fixed-precision decimal money with currency and at least nine fractional digits internally; customer accounting uses integer micro-credits (one credit = 1,000,000 micro-credits). No binary floating point. Reserve conservatively upward; settle once per logical request by declared half-even rounding after category aggregation, never per stream fragment. Provider invoice rounding differences are reconciliation adjustments. |
| MT-08 | Every AI call is classified by beneficiary/purpose. User-requested delivered inference consumes included capacity or authorised extra credits. Platform routing, abuse checks, health checks, admitted background indexing and platform-caused failed/retried work are recorded as platform cost without charging the user for duplicate/non-delivered work. Such overhead still has provider and workspace resource budgets. |
| MT-09 | Caller cancellation settles verified consumption already incurred within the authorised ceiling and releases the remainder; completed provider work is not presumed refundable. Platform failure/non-delivery releases customer reservation or appends a compensating credit adjustment. Supplier cost is retained in either case. |
| MT-10 | Independently billed search/tool/media operations use explicit quantity/unit/rate lines alongside tokens. No feature may be enabled with an unpriced billable dimension. Supporting the metering contract does not itself add image/video generation or arbitrary paid tools to product scope. |
| MT-11 | Persist settlement idempotency for each attempt usage revision and logical request. Duplicate/reordered events never double-debit; distinct real retries remain distinct supplier-cost records. Corrections append adjustments linked to the original records. |
| MT-12 | Missing final usage, timeout after dispatch and lost responses produce UsagePending/CostUnconfirmed, never zero cost or a fabricated exact total. Reconcile through the available provider evidence; no blind redispatch or repeat charge. After the configured reconciliation deadline, release unresolved customer holds without surprise later debit, retain the unresolved supplier liability and alert/restrict the affected route as required. |
| MT-13 | Reconcile calculated supplier cost against provider usage statements/invoices. Reconcile payments against the payment provider separately. Estimated cost, usage-confirmed calculated cost and invoice-reconciled cost remain distinguishable. |
| MT-14 | Metering records contain the identities linking workspace, service term, request/run, attempt, reservation, usage, supplier price, customer tariff, lot/capacity source, debit and adjustment. Historical charges must remain reproducible after model retirement or configuration replacement. |
| MT-15 | Dispatch must have an enforceable conservative bound on input, output/reasoning and separately billed tools, using actual route/category rules. An unbounded or unpriceable route cannot enter paid service. Verified supplier overrun beyond the authorized hold is an operator cost incident, not customer overdraft; block further dispatch, reconcile and adjust without erasing the real supplier usage. |
| MT-16 | Money always carries currency. V1 supplier budgets compare amounts in the same currency; no implicit FX conversion or addition across currencies. Customer credits are currency-independent service units. Payment/refund amounts retain the original sale currency and terms. |

### 8.5 Replenishing subscription capacity and extra credits

| # | Requirement |
|---|---|
| AC-01 | IncludedCapacity is a workspace-wide bucket denominated in the same fixed-precision customer service units as the retail tariff. Its burst capacity and recovery rate are explicit deployment parameters. They are independent of the monthly sale price and supplier-cost budget; none is inferred by treating subscription revenue as an equal amount of provider spend. |
| AC-02 | Capacity recovers only during a valid paid service interval, up to the configured burst ceiling. Authoritative server time and durable refill/account state govern recovery; clamp backward elapsed time to zero. Reconnect, process restart, another device, replica or request cannot reset the bucket. |
| AC-03 | First paid activation initialises the configured capacity once under an idempotent grant. Contiguous renewal extends the eligible interval without refilling to full. On lapse, included capacity becomes unavailable and does not accumulate during the gap; a new paid term initialises once under its own source. Remaining purchased credits are unaffected. |
| AC-04 | Admission atomically reserves capacity/credits and checks workspace concurrency, per-request/per-run ceilings, provider budget and current entitlement. A request whose bound can never fit the allowed capacity plus authorised extra credits is rejected with a smaller-request/budget action, never queued forever. |
| AC-05 | Reserve the next bounded model/tool invocation before dispatch and settle its actual usage afterward. Long Tasks additionally have a total authorised ceiling; they cannot reserve the whole workspace indefinitely while waiting for a device or approval. Release unused holds at terminal/safe boundaries, retaining only documented unresolved-cost holds. |
| AC-06 | Included capacity may cause WaitingForRateLimit/Capacity until a server-calculated recovery time. Extra credits are used only after a user enables extra usage with a maximum budget. Background automation obeys its previously authorised budget. No automatic purchase, recharge or unbounded paid fallback. |
| AC-07 | All desktop, Web, Mobile and automation entry points share the same workspace capacity/credits and actor authorisation. Changing a model changes consumption through the tariff, not by granting a new independent allowance. |
| AC-08 | Customer-facing limits state available capacity, recovery timing, model cost class, applicable per-task/concurrency restrictions and extra-credit rules. A recurring monthly allowance cap, if later introduced, must be disclosed as a cap and requires an explicit policy/terms revision. No hidden cap is described as merely a speed restriction. |
| AC-09 | Rate limiting, safety limits and provider availability remain enforceable even with extra credits. A new operator price/configuration release cannot retroactively lower a started Run's customer budget or silently raise its tariff. |
| AC-10 | Subscription capacity consumption, purchased-credit consumption, compensation, supplier cost and payment revenue remain separately queryable. A user can explain which pool funded a request and why it waited, stopped or charged credits. |
| AC-11 | Refill arithmetic counts included reservations against the burst ceiling: after accounting for eligible elapsed time, available capacity cannot exceed max(0, burst − held included capacity). Settling a hold debits actual use and releases only its unused source allocation. Returned capacity is capped; a refund must not mint spendable capacity above the burst. Purchased credits have a separate conservation ledger and never refill. |
| AC-12 | Preserve fractional refill remainder across evaluations. Advance the durable refill watermark monotonically, never backwards; calculate only the overlap with eligible service intervals. Frequent requests, rounding, clock rollback, racing replicas or a long outage cannot increase the contractual recovery rate. Config changes apply at recorded boundaries without resetting the watermark or releasing holds. |

### 8.6 Configuration and acceptance

The following arithmetic fixture is synthetic, not a provider price or launch offer. For 1,000 reported input tokens including 200 cached tokens, plus 100 output tokens including any reasoning: bill 800 uncached input + 200 cached input + 100 output. Synthetic supplier rates of USD 2 / 0.20 / 8 per million respectively produce **USD 0.00244**. Independent retail rates of 4,000 / 400 / 16,000 credits per million produce **4.88 credits**, or **4,880,000 micro-credits**. A 6-credit hold settles 4.88 and releases 1.12 to its original funding sources; cumulative stream snapshots must not change that result. This illustrates two independently configured rate sets, not a fixed markup requirement.

Model rates, customer tariffs, plan prices, capacity/recovery parameters, limits and payment-platform price mappings are typed, versioned deployment data governed by [configuration requirements](11-policy-and-configuration.md) §10.5. Formal price values require verified operational inputs; the implementation must run end to end before those final values are selected.

Acceptance includes: a hand-calculable multi-category usage fixture; two providers whose cache/reasoning fields overlap differently; cumulative stream events and duplicates; a real model call through the same metering path; cancellation with consumed tokens; lost final usage; provider retry charged once to the customer but fully visible in cost; token-category/tier price changes; reservation races across devices/replicas; restart without quota reset; paid-term expiry during a Task; recovery without buying credits; extra-credit opt-in and hard ceiling; and historical replay after changing all current rates. Sample configuration is labelled non-production and never silently selected by an official deployment.

---

### 8.7 Service eligibility across realms

Official paid-service rules apply uniformly to all official AI, including chat, agent steps, embedding and AI media processing. Paid term means verified subscription or prepaid Cloud Pass coverage, including audited compensation extending an existing paid service. A credit grant, trial flag or operator edit cannot bypass it. Self-hosted realms may instead issue an explicit operator-funded ServiceGrant; references to an active service term in product AI requirements use that grant in the self-host realm. Real metering, authorization, resource budgets and the prohibition on end-user BYOK remain identical. A self-host deployment with billing disabled requires no customer credit purchase.

## 9. Subscription-only AI access

| # | Requirement |
|---|---|
| BY-01 | Retired by P2-006: no local BYOK access path, entitlement bypass or provider-key UI. |
| BY-02 | Retired by P2-006: no end-user Cloud BYOK product, key store or paid feature. |
| BY-03 | Deployment-operator provider credentials fund the Cloud service; they never become end-user keys or change a user's payer mid-request. |
| BY-04 | Independent self-host policy authorises only its own realm and operator-funded providers. No local flag or self-host grant can authorise official Cloud AI. |

---

## 10. Refunds, disputes and evidence

| # | Requirement |
|---|---|
| RF-01 | A refund must **roll back entitlement**, not merely mark an order refunded. A refunded Cloud Pass revokes its 365-day grant; a refunded credit purchase zeroes the corresponding lot's remaining amount. This is why every grant records its source. |
| RF-02 | Partial refund is designed primarily for **AI credits**, where the unused proportion is naturally computable. A fixed-term Pass is treated as fully refundable or not per policy in V1; day-proportional automatic partial refunds are not implemented, because term, tax and compensation-day interactions are disproportionately complex. |
| RF-03 | Subscription handling is cancel-at-period-end. The interface must **not** claim subscriptions are never refundable; the Merchant of Record may still refund under law, consumer protection or payment risk. The stated path is cancel plus a separate billing-support request. |
| RF-04 | **Commercial Evidence is retained per order**: order, checkout, terms version, refund-policy version, account identity, workspace, entitlement granted, sign-in activity, cloud usage, AI usage, support history, cancellation request, refund request. Its purpose is proving delivery in a dispute, not surveillance. |
| RF-05 | **The dispute model must not assume the card pathway.** Neither Alipay nor WeChat Pay supports chargebacks (V-08), so refund and reconciliation behaviour cannot be modelled once and assumed universal. |

---

## 11. Portal division of responsibility

| ArcForges Account Portal | Provider portal |
|---|---|
| Plan and cloud status | Invoices and receipts |
| Renewal or end date | Payment and billing details |
| Storage quota and usage breakdown | Subscription cancellation (where provider-hosted) |
| AI allowance and purchased credits, shown separately | Billing-related refund requests |
| Entitlement list with reasons | Tax information |
| Billing history summary, with "Manage Billing →" | |

ArcForges must not reimplement an invoice engine, a tax-invoice editor or a payment-detail editor. Where the provider exposes a customer-session API, a fully in-portal billing surface may be built later; V1 uses the provider portal.

---

## 12. Mainland China

Governed entirely by **D-023**, confirmed item-for-item by **V-08**.

| # | Requirement |
|---|---|
| CN-01 | Mainland China is a **conditional launch market**. No second payment provider for V1. |
| CN-02 | The route is Paddle-hosted checkout with the methods Paddle makes available: **Alipay** for supported CNY one-time and recurring purchases (subject to separate Paddle approval and current limits), **WeChat Pay** for supported one-time desktop-web purchases (no subscriptions, desktop only), plus supported cards and other Paddle methods. Payoneer remains payout only. |
| CN-03 | **Cloud Pass is the non-recurring product for customers who cannot or will not use a recurring method.** This is load-bearing: WeChat Pay users cannot subscribe at all, and Alipay users meet a renewal ceiling. |
| CN-04 | ArcChat Mobile contains no China-specific checkout and remains consumption-only. |
| CN-05 | Eight pre-enablement gates must pass before mainland-China sales are enabled: Paddle supplier onboarding; Alipay/WeChat Pay approval where required; **CNY product and tax configuration**; checkout and webhook reachability; Payoneer payout eligibility; refund and reconciliation behaviour validated **against the absence of chargebacks**; sanctions, export, privacy and applicable Chinese regulatory review; production network preflight. |
| CN-06 | On gate failure, mainland-China sales are disabled by **explicit regional policy** without blocking the global launch. Silently substituting another provider is prohibited. |

---

## 13. Mobile commerce posture

Governed by **D-022**, confirmed by **V-09**.

| ArcChat Mobile may | ArcChat Mobile must not |
|---|---|
| Sign in | Sell subscriptions, cloud access or AI credits in-app |
| Display current plan and entitlement state | Embed provider checkout |
| Consume cloud capabilities and AI credits acquired elsewhere | Integrate StoreKit or Play Billing for the initial release |
| Display remote tasks, runs, approvals, notifications and results | Display an external purchase button, link or call to action |
| Manage non-commercial account and security settings permitted by store policy | **Unlock functionality from a locally entered licence key or purchase token** |

| # | Requirement |
|---|---|
| MB-01 | The same conservative behaviour applies across **all** storefronts, even where a regional programme permits external links. This avoids region-specific commercial builds and continuously tracked programme eligibility. |
| MB-02 | The entitlement architecture stays **capable of accepting a future store-originated grant** — an Apple or Google purchase would produce an ordinary `EntitlementGrant` with a different source — but that source is not implemented until a new explicit decision authorises mobile purchasing. |
| MB-03 | A build-time and CI check asserts that no code path in a mobile build can present a purchase call to action or accept a licence key. The licence-key path is the prohibition most likely to be violated by accident, since it is a natural engineering shortcut for offline entitlement. |

---

## 14. Provider portability

| # | Requirement |
|---|---|
| PP-01 | All provider identifiers (`ProviderCustomerId`, `ProviderOrderId`, `ProviderPaymentId`, `ProviderSubscriptionId`, `ProviderProductId`) exist only inside a **Provider Mapping**. ArcForges' own `OfferId`, `SubscriptionId` and `EntitlementId` are always its own. |
| PP-02 | A future additional or replacement source — Apple, Google, another Merchant of Record — produces `EntitlementGrant`s with a different `EntitlementSource`. **No client or product logic changes.** |
| PP-03 | The architecture must not depend irreversibly on any one provider's proprietary data model (**D-005**). |
| PP-04 | Provider capability gaps are absorbed by the ArcForges layer. Where a provider cannot perform an in-place plan switch, ArcForges still models the user's intent and delivers the outcome by a supported path. |

---

## 15. Domain model

```
BillingProvider · BillingProviderCapabilities · ProviderMapping · ProviderEvent
BillingAccount
Offer · ProductScope · PriceVersion · RegionalPrice
PurchaseIntent · CheckoutAttempt · Order · Payment
Subscription · SubscriptionState · PlanChangeIntent · CloudPass
EntitlementDefinition · EntitlementBundle · EntitlementBundleVersion
EntitlementGrant · EntitlementRevocation · EntitlementSource
EffectiveEntitlement · EntitlementSnapshot · EntitlementSnapshotVersion
QuotaDefinition · QuotaGrant · QuotaUsage
IncludedCapacityAccount · CapacityGrant · CapacityReservation · CapacityUsage
CreditLot · CreditReservation · CreditDebit · CreditAdjustment · CreditRefundHold
GracePeriod · EntitlementPolicy · EntitlementResolutionRule · EntitlementAuditEvent
Refund · RefundRequest · Dispute · Chargeback
Reconciliation · InvoiceReference · CommercialEvidence
Payout · Settlement · FinanceStatement
```

---

## 16. Responsibility layers

Responsibility layers that must never be conflated:

| Layer | Question |
|---|---|
| **Billing** | What did the user buy? |
| **Provider adapter** | What happened at the provider? |
| **Entitlement** | What should this Workspace have now? |
| **Quota** | What is the maximum that may be used? |
| **Usage** | How much has been used? |
| **AI credit ledger** | How much is left to spend? |
| **Authorization** | May this actor access this specific resource? |
| **Feature flags** | Has this feature been released to this audience? |

---

## 17. Acceptance scenarios

### Subscription
First payment succeeds · duplicate webhook · delayed webhook · **webhook entirely lost and recovered by reconciliation** · monthly renewal · annual renewal · cancellation with continued entitlement · reactivation · renewal failure entering grace · payment recovered inside grace · grace elapsing into restricted · subscription ending.

### Pass
First Pass · Pass purchased again early and extending correctly · Pass expiring · full Pass refund revoking the grant · subscription and Pass overlap prevented.

### Storage
Normal usage · add-on applied · add-on cancelled · usage above quota after downgrade · download and delete still permitted while over quota · falling below quota restoring writes.

### AI
Capacity activation and continuous recovery · renewal without reset · purchased/compensation lots · concurrent reservations · refund hold and partial refund · expired paid term blocks new AI despite retained credits · renewal unlocks the same retained balance · all token metering and configuration scenarios in §8.6.

### Provider capability
Recurring purchase where the method supports it · one-time purchase where the method does not support subscriptions · a payment method available only on desktop · a renewal above a method's cap failing into dunning · a dispute on a method with no chargeback support.

### Security and resilience
Client asserts entitlement it does not hold · stale entitlement cache · realtime message lost · billing service temporarily unavailable · provider API unavailable · manual compensation grant · administrative correction · simulated provider migration.

### Mobile
No purchase surface reachable in any build path · no external purchase call to action · **no licence-key unlock path exists** · consumption of an entitlement purchased on the web.

---

## 18. Go-live threshold

Commerce is production-ready only after: supplier onboarding and account approval; sanctions and export screening for the intended market set; Payoneer eligibility and receiving-currency confirmation; one real card payment; one real subscription; one real renewal; one cancellation and reactivation; one refund with entitlement rollback verified; a webhook duplicate-and-loss recovery test; a reconciliation repair test; and a completed payout received.

Until funds are actually received, the correct statement is "technical integration complete" — not "the commercial loop is closed".

---

## 19. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 3` | Provider-independent commercial domain model, checkout and webhook discipline, evidence retention, portal division — **with every Waffo-specific mechanic excluded as SUPERSEDED** |
| `I4 §Stage 4` | The complete entitlement model: kinds, grants, revocations, resolver, snapshot, quotas, credit ledger, grace and restriction behaviour |
| `I4 §Stage 0`, `§Stage 8` | Commercial layering, credit accounting shape |
| **D-005** | Paddle MoR, Payoneer payout, preserved abstraction principles |
| **D-020** | Every amount is versioned commercial policy; fixed-precision accounting; reserve-then-settle; hard stop |
| **D-022**, **V-09** | Mobile consumption-only posture and its traceable prohibitions |
| **D-023**, **V-08** | Mainland-China route, capability variation, chargeback absence, CNY requirement |
| **V-06**, **V-07** | Merchant-of-Record scope; payout relationship and settlement timing |
