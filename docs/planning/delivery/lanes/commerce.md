# Commerce, entitlement and credits — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Provider boundary, catalogue, purchases, events, entitlements, usage, credits, ledgers, refunds and live-gate staging.

Tasks: 15 · Owning repositories: Cloud · Integration owner(s): Cloud integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [COM.01](#task-com-01) | Provider adapter boundary | service | S | none | not-started |
| [COM.02](#task-com-02) | Catalogue and versioned policy | service | M | none | not-started |
| [COM.03](#task-com-03) | Purchase pipeline | service | L | [COM.01](#task-com-01) (artifact), [COM.02](#task-com-02) (artifact), [CLOUD.24](cloud.md#task-cloud-24) (artifact) | not-started |
| [COM.04](#task-com-04) | Provider event inbox | service | L | [COM.01](#task-com-01) (artifact), [COM.03](#task-com-03) (artifact) | not-started |
| [COM.05](#task-com-05) | Entitlement resolver | service | L | none | not-started |
| [COM.06](#task-com-06) | Distribution and enforcement | service | M | [COM.05](#task-com-05) (artifact), [CLOUD.23](cloud.md#task-cloud-23) (artifact) | not-started |
| [COM.07](#task-com-07) | Quota, usage and storage accounting | service | L | [CLOUD.07](cloud.md#task-cloud-07) (artifact), [COM.05](#task-com-05) (artifact) | not-started |
| [COM.08](#task-com-08) | Credits | service | L | [COM.05](#task-com-05) (artifact) | not-started |
| [COM.09](#task-com-09) | Ledgers and reconciliation | service | L | [COM.03](#task-com-03) (artifact), [COM.04](#task-com-04) (artifact) | not-started |
| [COM.10](#task-com-10) | Refunds, disputes and evidence | service | M | [COM.05](#task-com-05) (artifact), [COM.09](#task-com-09) (artifact) | not-started |
| [COM.11](#task-com-11) | Service term interval model | service | L | [COM.03](#task-com-03) (artifact), [COM.05](#task-com-05) (artifact), [COM.04](#task-com-04) (artifact) | not-started |
| [COM.12](#task-com-12) | Replenishing capacity bucket, refill and admission | service | XL | [COM.11](#task-com-11) (artifact), [COM.08](#task-com-08) (artifact) | not-started |
| [COM.13](#task-com-13) | Operator financial-owner proposal/approval operations | service | L | [CON.14](contracts.md#task-con-14) (contract), [CLOUD.21](cloud.md#task-cloud-21) (artifact), [COM.05](#task-com-05) (artifact), [COM.08](#task-com-08) (artifact), [COM.10](#task-com-10) (artifact) | not-started |
| [COM.14](#task-com-14) | Technical commerce closure and live-gate staging | service | L | [COM.12](#task-com-12) (artifact), [COM.03](#task-com-03) (artifact), [COM.04](#task-com-04) (artifact), [COM.05](#task-com-05) (artifact), [COM.09](#task-com-09) (artifact), [COM.10](#task-com-10) (artifact) | not-started |
| [COM.15](#task-com-15) | Owned-artifact receipt and closure | service | S | [COM.14](#task-com-14) (artifact), [COM.06](#task-com-06) (artifact), [COM.07](#task-com-07) (artifact) | not-started |

## Tasks

<a id="task-com-01"></a>

### COM.01 — Provider adapter boundary

**Outcome.** A provider-agnostic adapter boundary exists in Billing with a typed capability description; no provider type/identifier/webhook shape appears outside it, enforced by an architecture test.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-01` and ledger record `ledger/tasks/com-01.md` in the Plan repository; task branch `task/com-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-42.00](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.00) — full |
| Provides | provider-adapter-boundary; provider-capability-description |
| Start prerequisites | none |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.03](#task-com-03), [COM.04](#task-com-04) |
| Permitted substitutes | [SUB-provider-adapter-fixture](../substitutes.md#sub-provider-adapter-fixture) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Billing/**/Adapter/**`<br>`Cloud:tests/CloudIntegrationTests/Commerce/Adapter/**` |
| Validation | Offline architecture test (dependency-direction scan) + unit tests under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017); no live provider network calls in CI. |
| Completion evidence | Architecture-test pass log naming the forbidden-leakage scan; capability-driven behavior test results for at least one absent capability. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo at HEAD ce0a32a4 has no Billing module; only Hello World host (src/ArcForges.Cloud) and CF worker bootstrap exist. |

<a id="task-com-02"></a>

### COM.02 — Catalogue and versioned policy

**Outcome.** Offers, prices and policy versions exist as effective-dated policy data with no commercial figure compiled into code, and historical orders are immune to later price changes.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-02` and ledger record `ledger/tasks/com-02.md` in the Plan repository; task branch `task/com-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-42.01](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.01) — full |
| Provides | catalogue-offer-price-policy-version |
| Start prerequisites | none |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.03](#task-com-03) |
| Permitted substitutes | [SUB-commercial-figure-proposal](../substitutes.md#sub-commercial-figure-proposal) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Catalog/**` |
| Validation | Offline unit tests: retroactivity negative test, policy-version resolution test, static scan asserting no commercial constant compiled into code ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) static-check class). |
| Completion evidence | Retroactivity negative test result; compiled-constant scan result (zero hits). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No Catalog module present at Cloud HEAD ce0a32a4. |

<a id="task-com-03"></a>

### COM.03 — Purchase pipeline

**Outcome.** Purchase intent is the idempotency anchor for hosted checkout; one intent yields at most one order, a forged redirect grants nothing, and every checkout attempt carries complete internal metadata with no payment-instrument field anywhere in ArcForges.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-03` and ledger record `ledger/tasks/com-03.md` in the Plan repository; task branch `task/com-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-42.02](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.02) — full |
| Provides | purchase-intent; checkout-attempt; order-confirming-state |
| Start prerequisites | **artifact** [COM.01](#task-com-01) — provider adapter's hosted-checkout port and capability description. *Why:* checkout attempts must call the provider only through the adapter boundary; without it the pipeline would embed provider shapes directly, violating [BR-13](../../work-packages/22-identity-workspace-and-device.md#rule-br-13)<br>**artifact** [COM.02](#task-com-02) — Offer/Price/PriceVersion read model. *Why:* a purchase intent must reference a priced offer at a specific policy version to be idempotent and non-retroactive<br>**artifact** [CLOUD.24](cloud.md#task-cloud-24) — public API idempotency-key/rate-limiting primitive. *Why:* purchase intent double-submission handling is expected to reuse the platform's general idempotency mechanism rather than reinvent one per endpoint; exact API shape not yet observed since [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) is not yet built |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.04](#task-com-04), [COM.09](#task-com-09), [COM.11](#task-com-11), [COM.14](#task-com-14) |
| Permitted substitutes | [SUB-hosted-checkout-sandbox](../substitutes.md#sub-hosted-checkout-sandbox) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Billing/**/Purchase/**`<br>`Cloud:src/Contracts/Public/ArcForges.Contracts.PublicApi.Commerce/**` |
| Shared resources | [RES-contract-consumer-pins](../shared-resources.md#res-contract-consumer-pins) (append) |
| Validation | Offline unit/integration tests: double-submission, redirect-forgery negative, metadata-completeness, expired-attempt reconciliation; no live Paddle calls in CI (sandbox calls stay in manual/scheduled acceptance per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Double-submission test producing exactly one order; redirect-forgery negative result; metadata-completeness assertion. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-com-04"></a>

### COM.04 — Provider event inbox

**Outcome.** Every provider event is persisted before processing, signature-verified, deduplicated, and processed through the fixed eight-step verification chain, with quarantine and alerting for unprocessable events and idempotent full-inbox replay.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-04` and ledger record `ledger/tasks/com-04.md` in the Plan repository; task branch `task/com-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L · early risk proof |
| Obligations | [WP-42.03](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.03) — full |
| Provides | provider-event-inbox; event-verification-chain |
| Start prerequisites | **artifact** [COM.01](#task-com-01) — adapter signature-verification capability and typed event shape. *Why:* the inbox must verify signatures and interpret event types only through the adapter ([BR-13](../../work-packages/22-identity-workspace-and-device.md#rule-br-13)); it cannot parse provider payloads itself<br>**artifact** [COM.03](#task-com-03) — CheckoutAttempt/Order identifiers to correlate events against. *Why:* out-of-order handling and idempotency by event type+identifier require the purchase-side identifiers the event correlates to |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.09](#task-com-09), [COM.11](#task-com-11), [COM.14](#task-com-14) |
| Permitted substitutes | [SUB-provider-event-fixtures](../substitutes.md#sub-provider-event-fixtures) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Billing/**/Inbox/**`<br>`Cloud:fixtures/provider/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append), [RES-contract-consumer-pins](../shared-resources.md#res-contract-consumer-pins) (append) |
| Validation | Offline unit tests: duplicate, out-of-order, unsigned, unknown-product, replay, backlog-alert, convergence-from-point-in-time; deterministic fixture replay only, no live provider calls. |
| Completion evidence | Convergence test reproducing identical commercial state from inbox replay; backlog alert firing test. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Webhook idempotency/ordering/signature correctness is named by [SQ-08](../../implementation-sequence.md#rule-sq-08) as one of the two things that must be real before pricing is published; get this right before building ledgers/reconciliation on top. |

<a id="task-com-05"></a>

### COM.05 — Entitlement resolver

**Outcome.** Immutable grants and revocations resolve deterministically into an entitlement snapshot with a per-capability reason and version, and rebuilding the snapshot from its grants/revocations always reproduces the stored snapshot.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-05` and ledger record `ledger/tasks/com-05.md` in the Plan repository; task branch `task/com-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L · early risk proof |
| Obligations | [WP-42.04](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.04) — full |
| Provides | entitlement-grant-revocation-model; entitlement-snapshot-resolver |
| Start prerequisites | none |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.06](#task-com-06), [COM.07](#task-com-07), [COM.08](#task-com-08), [COM.10](#task-com-10), [COM.11](#task-com-11), [COM.13](#task-com-13), [COM.14](#task-com-14), [HAR.06](harness.md#task-har-06), [POL.04](policy.md#task-pol-04), [SIM.07](simulator.md#task-sim-07) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Entitlement/**/Resolver/**` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline unit tests: rebuild-equivalence over fixture accounts, reason-coverage, combination matrix over the four entitlement kinds, clock-determinism against an injected time source. |
| Completion evidence | Rebuild-equivalence test result (snapshot-from-scratch equals stored snapshot) across fixture accounts. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06) rebuild-equivalence is the core commerce invariant; COM.06/07/08/10/12 all read this resolver's snapshot, so its correctness gates a large share of downstream work. |

<a id="task-com-06"></a>

### COM.06 — Distribution and enforcement

**Outcome.** Entitlement is distributed with its version for client caching, realtime notification is only a refresh hint, offline staleness is bounded, all cost-bearing enforcement happens server-side, and losing entitlement never deletes local data.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-06` and ledger record `ledger/tasks/com-06.md` in the Plan repository; task branch `task/com-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-42.05](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.05) — full |
| Provides | entitlement-distribution-endpoint; server-side-enforcement-port |
| Start prerequisites | **artifact** [COM.05](#task-com-05) — EntitlementSnapshot + EntitlementVersion. *Why:* there is nothing to distribute or enforce against before the resolver produces a versioned snapshot<br>**artifact** [CLOUD.23](cloud.md#task-cloud-23) — typed-query/revision-precondition pattern. *Why:* distributing a versioned snapshot to clients is expected to reuse the public API's revision-precondition idiom rather than invent a parallel versioning scheme; [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) not yet built so exact shape unconfirmed |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.15](#task-com-15) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Entitlement/**/Distribution/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Entitlement/**/Enforcement/**` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append), [RES-contract-consumer-pins](../shared-resources.md#res-contract-consumer-pins) (append) |
| Validation | Offline tests: hint-not-authority, offline-staleness behavior, client-bypass negative, local-data-survival. |
| Completion evidence | Client-bypass negative test result; local-data-survival result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-com-07"></a>

### COM.07 — Quota, usage and storage accounting

**Outcome.** Quota (limit) and usage (measurement) live in separate stores keyed to the entitlement period, storage accounting matches committed objects exactly, and an exceeded quota produces a typed, explained refusal.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-07` and ledger record `ledger/tasks/com-07.md` in the Plan repository; task branch `task/com-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-42.06](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.06) — full |
| Provides | quota-usage-storage-accounting |
| Start prerequisites | **artifact** [CLOUD.07](cloud.md#task-cloud-07) — the published capacity/quota kernel (Capacity and Container/D1 integration producer). *Why:* [WP-42.06](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.06) text explicitly requires consuming the [WP-21.06](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.06) quota kernel rather than reimplementing gauge/reservation admission<br>**artifact** [COM.05](#task-com-05) — versioned entitlement grants. *Why:* quota resolution must apply new versioned grants without resetting gauges or outstanding reservations, which requires the resolver's version field |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.15](#task-com-15), [SIM.04](simulator.md#task-sim-04), [SIM.07](simulator.md#task-sim-07) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Entitlement/**/Quota/**` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline tests: race admissions, quota downgrade, repeated cancellation, GC timeout, period rollover with held old-period use, boundary-reset, accounting-vs-committed-storage comparison, refusal-message. |
| Completion evidence | Accounting comparison result against actual committed storage; boundary-reset test result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-com-08"></a>

### COM.08 — Credits

**Outcome.** Purchased (no-expiry) and compensation (disclosed-expiry) credit lots exist in integer micro-credits with funding order capacity to compensation to purchased, single-reservation-spans-both-pools accounting, reservation-expiry sweeping and a hard stop at zero with no floating point anywhere in the path.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-08` and ledger record `ledger/tasks/com-08.md` in the Plan repository; task branch `task/com-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-42.07](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.07) — full |
| Provides | credit-lot-model; credit-reservation-settle-release |
| Start prerequisites | **artifact** [COM.05](#task-com-05) — entitlement kind determination (which grant authorises which credit class). *Why:* a credit lot is issued against an entitlement grant/purchase and compensation lots need an entitlement-linked expiry policy |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.02](ai-routing.md#task-air-02), [COM.12](#task-com-12), [COM.13](#task-com-13) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Entitlement/**/Credits/**` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline tests: lot-ordering matrix, concurrency (no-overdraft), reservation-expiry sweep, hard-stop, refund-hold, fixed-precision policy scan (no floating point). |
| Completion evidence | Concurrency test showing no overdraft under concurrent reservation; fixed-precision scan result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-com-09"></a>

### COM.09 — Ledgers and reconciliation

**Outcome.** The three ledgers exist as separate append-only stores with scheduled two-way provider reconciliation expressing repairs as new typed records, never edits, and divergence above threshold alerts.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-09` and ledger record `ledger/tasks/com-09.md` in the Plan repository; task branch `task/com-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-42.08](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.08) — full<br>[WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure; three ledgers with unresolved holds through their existing deadline — [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure; three ledgers with unresolved holds through their existing deadline<br>[WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure — package-level obligation contribution |
| Provides | three-ledgers; reconciliation-subsystem |
| Start prerequisites | **artifact** [COM.03](#task-com-03) — Order/Payment records. *Why:* the ledgers post from confirmed purchase-pipeline outcomes<br>**artifact** [COM.04](#task-com-04) — verified ProviderEvent stream. *Why:* two-way reconciliation compares ledger state against the provider's own event history, which only the inbox holds |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.63](cloud.md#task-cloud-63), [COM.10](#task-com-10), [COM.14](#task-com-14) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Billing/**/Ledgers/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Billing/**/Reconciliation/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append) |
| Validation | Offline tests: dropped-webhook repair, duplicated-order repair, provider-side-change repair, immutability (history cannot be edited), ledger-separation. |
| Completion evidence | Dropped-webhook repair test recovering correct state without editing history; ledger-separation test. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-com-10"></a>

### COM.10 — Refunds, disputes and evidence

**Outcome.** A refund verifiably rolls entitlement back, dispute records are tracked, and a commercial evidence export covering order/payment/event/entitlement-history/usage for a period is complete, reproducible and free of payment-instrument data.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-10` and ledger record `ledger/tasks/com-10.md` in the Plan repository; task branch `task/com-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-42.09](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.09) — full |
| Provides | refund-rollback; dispute-record; commercial-evidence-export |
| Start prerequisites | **artifact** [COM.05](#task-com-05) — entitlement rollback path. *Why:* a refund must verifiably reverse the grant(s) it funded<br>**artifact** [COM.09](#task-com-09) — ledger entries to export. *Why:* the evidence export is built from ledger + event + entitlement history, which only exist once COM.09 posts them |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.66](cloud.md#task-cloud-66), [COM.13](#task-com-13), [COM.14](#task-com-14) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Billing/**/Refunds/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append) |
| Validation | Offline tests: refund-with-rollback, evidence completeness/reproducibility, payment-data-absence scan. |
| Completion evidence | Refund-with-rollback test result; payment-instrument-absence scan (zero hits) on the evidence export. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-com-11"></a>

### COM.11 — Service term interval model

**Outcome.** entitlement.service_term exists as an interval keyed on (kind, period_ref) with subscription_ref stable across renewals, a renewal always creating a new period_ref row, a replayed provider event extending nothing twice, and a plan change superseding rather than editing.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-11` and ledger record `ledger/tasks/com-11.md` in the Plan repository; task branch `task/com-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-42.11](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) — service_term interval model keyed on (kind, period_ref); the three separated identities (subscription_ref stable / period_ref per paid interval / provider-event dedup in commerce.provider_event); union-of-overlap effective term; plan-change supersede. Capacity bucket/refill/reservation half split to COM.12. |
| Provides | service-term-interval-model |
| Start prerequisites | **artifact** [COM.03](#task-com-03) — paid period identifiers (checkout/order confirmation producing a period_ref-worthy paid interval). *Why:* a service term's period_ref is the paid period's own identity, which only the purchase pipeline mints<br>**artifact** [COM.05](#task-com-05) — offer assignment and entitlement kind. *Why:* service term sourcing includes the currently assigned offer; the resolver is where offer assignment is decided<br>**artifact** [COM.04](#task-com-04) — deduplicated ProviderEvent stream. *Why:* [TM-02](../../../architecture/data-model/01-cloud-data-model.md#rule-tm-02) requires provider-event dedup to live in commerce.provider_event so a replayed event cannot extend a term twice; the inbox is the only place that dedup exists |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.12](#task-com-12) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Entitlement/**/ServiceTerm/**` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline tests: renewal creating a second term row without violating the (kind,period_ref) key, replayed event creating nothing, plan change superseding not editing, overlap/genuine-gap union-of-interval tests. |
| Completion evidence | Renewal-without-key-violation test; replay-creates-nothing test; supersede-not-edit test. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-com-12"></a>

### COM.12 — Replenishing capacity bucket, refill and admission

**Outcome.** The capacity bucket refills by a per-period saturating accrual independent of evaluation frequency, backed by a monotonic durable watermark and exact rational carry, never claws back on a ceiling reduction, initialises exactly once per contiguous run, and admission is atomic with the service-term check first, committing before dispatch.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-12` and ledger record `ledger/tasks/com-12.md` in the Plan repository; task branch `task/com-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / XL · early risk proof |
| Obligations | [WP-42.11](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) — entitlement.capacity_bucket refill algorithm (§7.2), capacity_policy_period history, capacity_reservation with three funding sources, idempotent once-per-contiguous-run initialisation, and atomic admission with the service-term check first |
| Provides | capacity-bucket-refill; capacity-reservation-three-source; admission-unit-of-work |
| Start prerequisites | **artifact** [COM.11](#task-com-11) — service_term interval and (kind,period_ref) rows. *Why:* capacity_policy_period parameters are read from term history; admission checks the service term first in the same unit of work<br>**artifact** [COM.08](#task-com-08) — CreditReservation reserve/settle/release primitive. *Why:* capacity_reservation is explicitly a reservation spanning capacity plus the two credit pools; it extends rather than forks COM.08's reservation mechanics |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.02](ai-routing.md#task-air-02), [COM.14](#task-com-14), [HAR.02](harness.md#task-har-02), [SIM.07](simulator.md#task-sim-07) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Entitlement/**/Capacity/**` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline deterministic tests only (no wall-clock sleep): full-hold-then-consume-then-read fixture, fractional saturation, changed plan, overlap, genuine gap, unchanged renewal, grandfathered above-ceiling balance, the [CT-13](../../../architecture/16-billing-and-commerce-architecture.md#rule-ct-13) refill fixture (identical result whether refill runs once or a thousand times over an interval containing a ceiling raise, reduction and rate change, asserting 11 at t=11), clock rollback/restart/reconnect/second-device/racing-replica watermark tests, ceiling-reduction-preserves-held-funding test, ledger-unit-separation test (customerCredit carries micro-credits with no currency; the other two carry money with currency; no query sums them). |
| Completion evidence | The [CT-13](../../../architecture/16-billing-and-commerce-architecture.md#rule-ct-13) refill fixture result exactly (11 at t=11, not 21 or 12); watermark non-rewind evidence across restart/second-device/racing-replica; ceiling-reduction-preserves-funding result. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | The single most algorithmically risky unit in this area (§7.2 saturating accrual with exact rational carry); named as the [PG-13](../../../assurance/open-gates-register.md#rule-pg-13)/[PG-16](../../../assurance/open-gates-register.md#rule-pg-16) producer that must close before [WP-42.10](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10) despite its higher substep number. Consider a narrow property-based-test spike on the refill function ahead of the full admission integration. |

<a id="task-com-13"></a>

### COM.13 — Operator financial-owner proposal/approval operations

**Outcome.** The financial-owner operator RPCs (grant/revokeGrant/issueCredit/adjustCredit/refund) are implemented exactly once against the registry04 §9 typed proposal/approval protocol with all eight authorization fields, refusing public customer/PAT/agent access, and one approved proposal cannot execute twice.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-13` and ledger record `ledger/tasks/com-13.md` in the Plan repository; task branch `task/com-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) Operator contract closure — financial owners (grant/revokeGrant/issueCredit/adjustCredit/refund) — operator contract closure; financial-owner RPC implementations: grant, revokeGrant, issueCredit, adjustCredit, refund |
| Provides | operator-financial-owner-rpcs |
| Start prerequisites | **contract** [CON.14](contracts.md#task-con-14) — the OperatorService full RPC surface (ProposeAction/ApproveAction/execute, grant/revokeGrant/issueCredit/adjustCredit/refund message shapes, eight authorization fields, negative vectors) per registry04 §9. *Why:* only a single placeholder message (OperatorCallContext, a context shape with no RPCs) exists at Contracts HEAD e6c4a77f; no operator service or per-domain RPC message is generated yet<br>**artifact** [CLOUD.21](cloud.md#task-cloud-21) — real identity/dispatch conformance for operator calls. *Why:* the operator paragraph explicitly assigns 'real identity/dispatch conformance' to [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23); operator RPCs need that routing/auth layer to refuse public customer/PAT/agent callers<br>**artifact** [COM.05](#task-com-05) — grant/revocation model. *Why:* grant/revokeGrant operate directly on COM.05's EntitlementGrant/EntitlementRevocation<br>**artifact** [COM.08](#task-com-08) — credit lot issue/adjust primitives. *Why:* issueCredit/adjustCredit operate on COM.08's CreditLot model<br>**artifact** [COM.10](#task-com-10) — refund/rollback path. *Why:* the refund RPC drives COM.10's refund-with-rollback mechanism |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [OPS.13](operations.md#task-ops-13) — the operator console UI actually calling these RPCs end-to-end. *Why:* [WP-45.04](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.04) is named as 'the real console join'; this task's RPCs are not exercised by a real operator until the console wires them in |
| Unblocks | [CLOUD.64](cloud.md#task-cloud-64), [OPS.05](operations.md#task-ops-05), [OPS.13](operations.md#task-ops-13) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Billing/**/Operator/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Entitlement/**/Operator/**` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append), [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Offline tests: distinct approver, stale hash/revision/configuration, role revocation, expiry, concurrent consumption, lost receipt, double-execution-of-one-approval, no-direct-SQL/public-SDK-import architecture test. |
| Completion evidence | Double-execution negative result (one approved proposal cannot execute twice); public-customer/PAT/agent refusal result for every method. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Contracts HEAD e6c4a77f has only OperatorCallContext; no OperatorService or grant/issueCredit/refund RPC definitions found. |

<a id="task-com-14"></a>

### COM.14 — Technical commerce closure and live-gate staging

**Outcome.** Deterministic provider normalization and the full sandbox lifecycle are proven with synthetic and Paddle/Payoneer-sandbox vectors, SubscriptionState exactly matches requirements-04, plan changes start next term without proration, and the live-payment/payout/refund/merchant gates are explicitly preserved as pending for WP50.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-14` and ledger record `ledger/tasks/com-14.md` in the Plan repository; task branch `task/com-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-42.10](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10) — full<br>[WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure — package-level obligation contribution |
| Provides | technical-commerce-closure; activation-checklist |
| Start prerequisites | **artifact** [COM.12](#task-com-12) — passing durable term/capacity/refill state ([WP-42.11](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) evidence). *Why:* the design's own 'Frozen semantics' ordering states [WP-42.11](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) must pass before [WP-42.10](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10) despite the suffix order; [PG-13](../../../assurance/open-gates-register.md#rule-pg-13)/[PG-16](../../../assurance/open-gates-register.md#rule-pg-16) evidence is produced at 42.11 and consumed here<br>**artifact** [COM.03](#task-com-03) — purchase pipeline end to end. *Why:* sandbox lifecycle vectors exercise purchase/checkout as their entry point<br>**artifact** [COM.04](#task-com-04) — event inbox end to end. *Why:* vectors explicitly include event duplication/loss scenarios<br>**artifact** [COM.05](#task-com-05) — entitlement resolver end to end. *Why:* SubscriptionState must exactly match requirements-04, which the resolver computes<br>**artifact** [COM.09](#task-com-09) — ledgers and reconciliation end to end. *Why:* ledger integrity is an explicit technical-receipt item<br>**artifact** [COM.10](#task-com-10) — refund path end to end. *Why:* test-mode charge/refund/webhook-replay vectors are explicit |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.15](#task-com-15), [WEB.14](web.md#task-web-14), [WEB.29](web.md#task-web-29) |
| Write scope | `Cloud:tests/CloudIntegrationTests/Commerce/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Billing/**` |
| Shared resources | [RES-cloud-runbooks-and-fixtures](../shared-resources.md#res-cloud-runbooks-and-fixtures) (append) |
| Validation | Recorded Paddle/Payoneer sandbox scenario vectors (no-term, cancellation, lost result, unknown exposure, future-effective changes) plus synthetic fixtures; per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) this acceptance-level sandbox evidence stays outside routine CI (manual/scheduled), while regression-level assertions stay in offline CI. |
| Completion evidence | Full synthetic/sandbox ledger vector results; activation checklist document handed to WP48/WP50; explicit statement that [VG-10](../../../assurance/open-gates-register.md#rule-vg-10)/[VG-11](../../../assurance/open-gates-register.md#rule-vg-11)/[VG-12](../../../assurance/open-gates-register.md#rule-vg-12)/[L-30](../../../assurance/release-gates.md#rule-l-30) remain open. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Completion explicitly does not require WP48 (account portal) or WP50 (real go-live); this task closes the technical/test-mode gate only ([PG-10](../../../assurance/open-gates-register.md#rule-pg-10)) and stages the activation checklist. Real checkout/payout evidence and [VG-10](../../../assurance/open-gates-register.md#rule-vg-10)/[VG-11](../../../assurance/open-gates-register.md#rule-vg-11)/[VG-12](../../../assurance/open-gates-register.md#rule-vg-12)/[L-30](../../../assurance/release-gates.md#rule-l-30) stay with WP50 per [WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) §8.11. Retires SUB-provider-event-fixtures and SUB-hosted-checkout-sandbox. |

<a id="task-com-15"></a>

### COM.15 — Owned-artifact receipt and closure

**Outcome.** The package-level owned-artifact/real-integration receipt is recorded (source commit, producer version, candidate hashes, actual runtime/provider, scenario, result, real-vs-fixture status) and the [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) active-Pass/subscription-exclusivity and ledger-hold-deadline vectors pass.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-15` and ledger record `ledger/tasks/com-15.md` in the Plan repository; task branch `task/com-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Package acceptance | Records the [WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-42.90](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.90) — full<br>[WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure; active Pass/subscription mutual exclusion, no immediate proration, exact renewal/reset periods — [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure; active Pass/subscription mutual exclusion, no immediate proration, exact renewal/reset periods<br>[WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure — package-level obligation contribution |
| Provides | wp42-closure-receipt |
| Start prerequisites | **artifact** [COM.14](#task-com-14) — technical commerce closure results to attach to the receipt. *Why:* [WP-42.90](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.90) explicitly must keep [WP-42.11](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) evidence and its order before [WP-42.10](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10), and the receipt aggregates every amended §5 producer/consumer result; COM.14 is the last domain producer to close<br>**artifact** [COM.06](#task-com-06) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [COM.07](#task-com-07) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.06](release.md#task-rel-06), [REL.08](release.md#task-rel-08) |
| Write scope | `Cloud:eng/provenance/records/**` |
| Validation | Aggregation only: existing concurrent admission/idempotent settlement/reversal/storage-accounting cases re-asserted at the candidate closure; no new test logic. |
| Completion evidence | The owned-artifact/real-integration receipt itself, with inapplicable fields explicitly marked. |
| Baseline (unreviewed unless accepted) | not-started |
