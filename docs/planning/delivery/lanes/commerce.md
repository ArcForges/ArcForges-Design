# Commerce, entitlement and credits — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Provider boundary, catalogue, purchases, events, entitlements, usage, credits, ledgers, refunds and live-gate staging.

Tasks: 16 · Owning repositories: Cloud · Integration owner(s): Cloud integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [COM.01](#task-com-01) | Provider adapter boundary | service | S | none | not-started |
| [COM.02](#task-com-02) | Catalogue and versioned policy | service | M | none | not-started |
| [COM.03](#task-com-03) | Purchase pipeline | service | L | [COM.01](#task-com-01) (artifact), [COM.02](#task-com-02) (artifact), [CLOUD.24](cloud.md#task-cloud-24) (artifact) | not-started |
| [COM.04](#task-com-04) | Provider event inbox | service | L | [COM.01](#task-com-01) (artifact), [COM.03](#task-com-03) (artifact), [COM.16](#task-com-16) (artifact) | not-started |
| [COM.05](#task-com-05) | Entitlement resolver | service | L | none | not-started |
| [COM.06](#task-com-06) | Distribution and enforcement | service | M | [COM.05](#task-com-05) (artifact), [CLOUD.23](cloud.md#task-cloud-23) (artifact), [COM.16](#task-com-16) (artifact), [CON.08](contracts.md#task-con-08) (contract) | not-started |
| [COM.07](#task-com-07) | Quota, usage and storage accounting | service | L | [CLOUD.07](cloud.md#task-cloud-07) (artifact), [COM.05](#task-com-05) (artifact) | not-started |
| [COM.08](#task-com-08) | Credits | service | L | [COM.05](#task-com-05) (artifact) | not-started |
| [COM.09](#task-com-09) | Ledgers and reconciliation | service | L | [COM.03](#task-com-03) (artifact), [COM.04](#task-com-04) (artifact) | not-started |
| [COM.10](#task-com-10) | Refunds, disputes and evidence | service | M | [COM.05](#task-com-05) (artifact), [COM.09](#task-com-09) (artifact), [COM.16](#task-com-16) (artifact) | not-started |
| [COM.11](#task-com-11) | Service term interval model | service | L | [COM.03](#task-com-03) (artifact), [COM.05](#task-com-05) (artifact), [COM.04](#task-com-04) (artifact), [COM.16](#task-com-16) (artifact) | not-started |
| [COM.12](#task-com-12) | Replenishing capacity bucket, refill and admission | service | XL | [COM.11](#task-com-11) (artifact), [COM.08](#task-com-08) (artifact) | not-started |
| [COM.13](#task-com-13) | Operator financial-owner proposal/approval operations | service | L | [CON.14](contracts.md#task-con-14) (contract), [CLOUD.21](cloud.md#task-cloud-21) (artifact), [COM.05](#task-com-05) (artifact), [COM.08](#task-com-08) (artifact), [COM.10](#task-com-10) (artifact), [COM.16](#task-com-16) (artifact) | not-started |
| [COM.14](#task-com-14) | Technical commerce closure and live-gate staging | service | L | [COM.12](#task-com-12) (artifact), [COM.03](#task-com-03) (artifact), [COM.04](#task-com-04) (artifact), [COM.05](#task-com-05) (artifact), [COM.09](#task-com-09) (artifact), [COM.10](#task-com-10) (artifact) | not-started |
| [COM.15](#task-com-15) | Owned-artifact receipt and closure | service | S | [COM.14](#task-com-14) (artifact), [COM.06](#task-com-06) (artifact), [COM.07](#task-com-07) (artifact) | not-started |
| [COM.16](#task-com-16) | Entitlement grant port and durable Entitlement store | service | L | [COM.05](#task-com-05) (artifact), [CLOUD.03](cloud.md#task-cloud-03) (artifact), [CLOUD.04](cloud.md#task-cloud-04) (artifact), [CLOUD.06](cloud.md#task-cloud-06) (artifact) | not-started |

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
| Start prerequisites | **artifact** [COM.01](#task-com-01) — adapter signature-verification capability and typed event shape. *Why:* the inbox must verify signatures and interpret event types only through the adapter ([BR-13](../../work-packages/22-identity-workspace-and-device.md#rule-br-13)); it cannot parse provider payloads itself<br>**artifact** [COM.03](#task-com-03) — CheckoutAttempt/Order identifiers to correlate events against. *Why:* out-of-order handling and idempotency by event type+identifier require the purchase-side identifiers the event correlates to<br>**artifact** [COM.16](#task-com-16) — the published IssueGrant and RevokeGrant port and the durable Entitlement store behind it. *Why:* the last step of the fixed verification chain ([EI-05](../../../architecture/16-billing-and-commerce-architecture.md#rule-ei-05)) is the grant, and [EO-03](../../../architecture/16-billing-and-commerce-architecture.md#rule-eo-03) lets Commerce write into Entitlement only through that port; replaying the inbox must reproduce the persisted grants, which needs the real store behind the port and not a test store |
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
| Obligations | [WP-42.04](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.04) — the grant and revocation model, the resolver and the snapshot with per-capability reasons and version, with rebuild equivalence proven over the resolver's store port (the Commerce-facing grant interface in the shared Abstractions project, the [GR-05](../../../requirements/04-commerce-entitlement-and-credits.md#rule-gr-05) reason on the grant row, and the durable D1 store with its atomic snapshot commit are mapped to COM.16) |
| Provides | entitlement-grant-revocation-model; entitlement-snapshot-resolver |
| Start prerequisites | none |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.06](#task-com-06), [COM.07](#task-com-07), [COM.08](#task-com-08), [COM.10](#task-com-10), [COM.11](#task-com-11), [COM.13](#task-com-13), [COM.14](#task-com-14), [COM.16](#task-com-16), [HAR.06](harness.md#task-har-06), [PLT.20](platform.md#task-plt-20), [POL.04](policy.md#task-pol-04), [SIM.07](simulator.md#task-sim-07) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Entitlement/Resolver/** (the real layout of the planned src/Cloud/ArcForges.Cloud.Modules.Entitlement/**/Resolver/**: the one Entitlement project CLOUD.02 creates, whose Domain, Application and Infrastructure layers are folders and namespaces; the resolver and the grant and revocation model are folders inside it)`<br>`Cloud:src/ArcForges.Cloud.Modules.Entitlement/EntitlementModule.cs and Cloud:src/ArcForges.Cloud.Modules.Entitlement/ArcForges.Cloud.Modules.Entitlement.csproj (only the module's own Register entry point listing the resolver services, and InternalsVisibleTo for the existing test assembly so that no public method needs a public-API-to-test mapping; no package, reference or behavior change)`<br>`Cloud:tests/ArcForges.Cloud.Tests/Entitlement/** and Cloud:tests/ArchitectureTests/** (resolver tests in the existing test projects; the architecture tests only for the reviewed project role and layering binding of the Entitlement project)`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/com-05-*.json (new immutable successor chained from the then-active receipt, only because hash-bound project and release inputs change; no coordinate, integrity value or closure entry changes)`<br>`Cloud:eng/provenance/** (immutable successor release profile, Worker bundle and runtime-notice records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt)`<br>`Cloud:docs/entitlement-resolver.md (new, factual description of the resolver and its fixtures) and Cloud:AGENTS.md (only if the module description changes)` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline unit tests: rebuild-equivalence over fixture accounts, reason-coverage, combination matrix over the four entitlement kinds, clock-determinism against an injected time source. |
| Completion evidence | Rebuild-equivalence test result (snapshot-from-scratch equals stored snapshot) across fixture accounts. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06) rebuild-equivalence is the core commerce invariant; COM.06/07/08/10/12 all read this resolver's snapshot, so its correctness gates a large share of downstream work. |

<a id="task-com-06"></a>

### COM.06 — Distribution and enforcement

**Outcome.** Entitlement is distributed with its version for client caching through EntitlementService.GetSnapshot and Check (CON.08), served from the stored snapshot and EntitlementVersion of the COM.16 store and never from grant tables, events or client input; realtime notification is only a refresh hint: this task supplies the entitlement hint projection (the entitlement.snapshot.changed outbox payload to the public entitlement.changed hint, which carries only entitlementVersion) that CLOUD.31's closed event-hint registry uses; offline staleness is bounded per [DS-05](../../../architecture/06-data-persistence-and-formats.md#rule-ds-05) (staleness per policy class; the server re-decides on every actual request) from fields that already exist (the stored snapshot's ComputedAt and ValidUntil and the public ServiceTerm endsAt and graceEndsAt), with no new wire field; all cost-bearing enforcement happens server-side through a published enforcement port that other modules call, so a client-supplied entitlement or version never admits; and losing entitlement never deletes local data. The Entitlement module's internal IEntitlementDefinitionSource gets its production binding here (S59(8)): it supplies the active definition set over the Entitlement-owned definitions activations of data model 01 (entitlement.definitions_activation; Design #249), read through the module's own store and the existing storage/plans/entitlement/activations-load.sql, so production resolution of the distribution waits only for the production business composition (CLOUD.87). This task delivers and proves the Cloud half of [WP-42.05](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.05). The client halves (caching by version, re-reading on a hint, the offline staleness behaviour and local-data survival on each client) are their consumers' acceptance by S59(10): the desktop half is PLT.20's completion-follow-up acceptance, and the Android and Web halves are named on AND.19 and WEB.14, outside this run.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-06` and ledger record `ledger/tasks/com-06.md` in the Plan repository; task branch `task/com-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-42.05](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.05) — the Cloud half: versioned distribution through EntitlementService.GetSnapshot and Check, the refresh-hint projection, the offline staleness bound per [DS-05](../../../architecture/06-data-persistence-and-formats.md#rule-ds-05) decided on the server, server-side enforcement through the published port, no server instruction to delete local data, and the production IEntitlementDefinitionSource binding (S59(8)); the client halves are named on their consumers by planning repair fix8 delta (S59(10)): the desktop half (entitlement caching by version, a re-read on a hint, the offline staleness bound and local-data survival) is PLT.20's completion-follow-up acceptance, and the Android and Web halves are named on AND.19 and WEB.14, outside this run |
| Provides | entitlement-distribution-endpoint; server-side-enforcement-port |
| Start prerequisites | **artifact** [COM.05](#task-com-05) — EntitlementSnapshot + EntitlementVersion. *Why:* there is nothing to distribute or enforce against before the resolver produces a versioned snapshot<br>**artifact** [CLOUD.23](cloud.md#task-cloud-23) — typed-query/revision-precondition pattern. *Why:* distributing a versioned snapshot to clients is expected to reuse the public API's revision-precondition idiom rather than invent a parallel versioning scheme; [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) not yet built so exact shape unconfirmed<br>**artifact** [COM.16](#task-com-16) — the durable Entitlement store that holds the stored snapshot with its EntitlementVersion. *Why:* distribution reads the persisted snapshot and version ([ED-01](../../../architecture/16-billing-and-commerce-architecture.md#rule-ed-01), [ES-03](../../../requirements/04-commerce-entitlement-and-credits.md#rule-es-03)); it must not read a test store or the grant tables, and the store is where the snapshot is committed atomically with the records that cause it<br>**contract** [CON.08](contracts.md#task-con-08) — the generated EntitlementService (GetSnapshot, Check) and EntitlementSnapshot in ArcForges.Contracts.PublicApi. *Why:* distribution and Check are served from the generated service base; CON.08 is complete, and its output is in the already-pinned PublicApi 1.0.0-ci.287.1, so the edge changes no ordering |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [COM.15](#task-com-15), [PLT.20](platform.md#task-plt-20) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Entitlement/Distribution/** (new: the distribution service over the COM.16 store, the conditional read by expected version in the CLOUD.23 revision-precondition idiom, the staleness bound per DS-05 from the existing snapshot and service-term fields, and the pure entitlement hint projection of the module's outbox payload (entitlement.snapshot.changed: revision and entitlementVersion) to the public entitlement.changed hint)`<br>`Cloud:src/ArcForges.Cloud.Modules.Entitlement/Enforcement/** (new: the internal implementation of the enforcement port over the stored snapshot, with typed refusals)`<br>`Cloud:src/ArcForges.Cloud.Modules.Entitlement/Definitions/** (new, internal, S59(8): the production IEntitlementDefinitionSource binding over the Entitlement-owned entitlement.definitions_activation records (data model 01; Design #249), read through the module's own store and the existing storage/plans/entitlement/activations-load.sql; no Configuration-module table is read and no definition content is compiled into code) and Cloud:storage/plans/entitlement/** (only a new read plan, if the existing plans cannot serve the binding), with the regenerated Cloud:src/ArcForges.Cloud.Storage.D1/PlanManifest.g.cs and Cloud:worker/storage/plans.generated.ts (generator output only; RES-cloud-storage-plans)`<br>`Cloud:src/ArcForges.Cloud.Modules.Abstractions/Entitlement/** (only new files: the public server-side enforcement port and the public form of the entitlement hint projection, primitives only, referencing no module; EntitlementGrantPort.cs unchanged)`<br>`Cloud:src/ArcForges.Cloud.Modules.Entitlement/EntitlementModule.cs (only the Register entries of the distribution service, the enforcement port, the production IEntitlementDefinitionSource binding and, if CLOUD.31's Abstractions/Events contribution seam exists when this task lands, the registration of the hint projection through it; otherwise CLOUD.31 registers it)`<br>`Cloud:src/ArcForges.Cloud/PublicApi/Endpoints/** (only this task's partial-class file of the EntitlementService endpoint class that CLOUD.21 declares, with the GetSnapshot and Check handlers over the generated ArcForges.Contracts.PublicApi service base, and this task's rows in the CLOUD.21 endpoint registry, whose RpcPolicy entries the registry builds from the CON.41 operation metadata, and in the operation-to-owner coverage table; no hand-written RpcPolicy entry)`<br>`Cloud:src/ArcForges.Cloud/Generation/TransportBudgets.cs (only the ByMethod rows for /arcforges.publicapi.v1.EntitlementService/GetSnapshot and /arcforges.publicapi.v1.EntitlementService/Check; S34) and the generated Cloud:worker/tables/cloud-tables.generated.ts (regenerated with npm run generate after rebase, never hand-edited; npm run check:generated)`<br>`Cloud:tests/ArcForges.Cloud.Tests/Entitlement/**, Cloud:tests/ArcForges.Cloud.Tests/Generation/** (only the new generated rows) and Cloud:tests/ArchitectureTests/** (distribution, hint, bypass and data-survival tests; the architecture tests only to assert, append-only, that the enforcement port lives in Abstractions and that no module references Entitlement internals; RES-architecture-tests) and Cloud:tests/worker/ingress-routes.test.ts (only the new generated rows)`<br>`Cloud:.dockerignore (only the allow-list lines that admit the new Distribution/ and Enforcement/ folders of the Entitlement project to the image build context, as COM.05 did for Resolver; tests/worker/docker-context.test.ts only if it pins the list)`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/com-06-*.json (new immutable successor chained from the then-active receipt, only because hash-bound project, lock, package.json or wrangler.json inputs change; S25 reviewer fields naming the actual independent reviewer)`<br>`Cloud:eng/provenance/** (immutable successor release profile, Worker bundle and runtime-notice records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt, derived by the repository tooling) and Cloud:tests/worker/release-provenance.test.ts (only the pinned Worker bundle digest refresh, S29, if the Worker bundle changes)`<br>`Cloud:docs/entitlement-resolver.md (the distribution, hint and enforcement sections) and Cloud:AGENTS.md (only factual pointers)` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-cloud-storage-plans](../shared-resources.md#res-cloud-storage-plans) (append) |
| Validation | Offline C# tests (CI): hint-not-authority (the hint carries only entitlementVersion, and GetSnapshot, Check and the enforcement port read only the stored snapshot, so no event, hint or client-supplied version changes a decision); offline-staleness behaviour per [DS-05](../../../architecture/06-data-persistence-and-formats.md#rule-ds-05) from the existing snapshot and service-term fields ([ED-03](../../../architecture/16-billing-and-commerce-architecture.md#rule-ed-03)), with the server re-deciding on the actual request; the hint projection (an entitlement.snapshot.changed payload maps to an entitlement.changed hint that carries only entitlementVersion); client-bypass negative (a client that asserts an entitlement or a version is refused by Check and by the enforcement port, which decide from the stored snapshot only); local-data-survival (losing entitlement produces no server instruction to delete local data); the conditional read by expected version; the generated-table drift check and the worker route tests for the two new rows; the architecture tests; AOT compile. The production IEntitlementDefinitionSource binding is tested over the SQLite oracle on the real migrations with the module's own plans (S59(8)). Production resolution of the distribution is recorded as 'blocked on the production business composition (CLOUD.87), not proven', and the services are proven in a composition that binds the plan executor and this task's definition-source binding. The [WP-42.05](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.05) client halves are the acceptance of PLT.20 (desktop), AND.19 (Android) and WEB.14 (Web) by S59(10), not of this task. No hosted live CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Client-bypass negative test result; local-data-survival result; hint-not-authority, hint-projection and offline-staleness results; the definition-source binding results; the production-resolution leg recorded as 'blocked on the production business composition (CLOUD.87), not proven'; source commit. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair fix8 2026-10-10 ([DLV-34](../README.md#rule-dlv-34); coordinator ruling S57(13); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): the write scope named a layout (src/Cloud/ArcForges.Cloud.Modules.Entitlement) that does not exist; it is bound to the real module project src/ArcForges.Cloud.Modules.Entitlement (Distribution/ and Enforcement/ beside COM.16's Persistence/ and COM.05's Resolver/), the cross-module enforcement port and the public form of the hint projection to Abstractions/Entitlement (EntitlementGrantPort precedent), and the public GetSnapshot and Check handlers to the host folder src/ArcForges.Cloud/PublicApi/Endpoints through the mechanism CLOUD.21 establishes (S57(12)). The offline staleness bound follows [DS-05](../../../architecture/06-data-persistence-and-formats.md#rule-ds-05) from fields that already exist (the stored snapshot's ComputedAt and ValidUntil and the public ServiceTerm endsAt and graceEndsAt); no Contracts field is added. The client halves of [WP-42.05](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.05) are the consumers' acceptance. This task supplies the entitlement hint projection to CLOUD.31's closed event-hint registry; delivery of the hint is CLOUD.31 and CLOUD.33's, so there is no edge and the hint content is proven offline. RES-contract-consumer-pins is dropped because PublicApi 1.0.0-ci.287.1 is already a direct reference; RES-architecture-tests (append) is added for the architecture-test rows. Contract start edge CON.08 (complete) added. Production resolution of the distribution needs the production plan executor (CLOUD.87) and an IEntitlementDefinitionSource binding (EntitlementService.ReadAsync compares the stored snapshot with the current definitions version); until both exist, production resolution is 'blocked on the production business composition (CLOUD.87) and the IEntitlementDefinitionSource production binding, not proven', and the services are proven in a composition that binds both. No acceptance is removed. Review round 2 (2026-10-10): (1) The client halves of [WP-42.05](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.05) are no longer called the consumers' acceptance: no in-scope ArcScope, Mobile, Web or DesktopPlatform task carries entitlement caching by version, offline staleness or local-data survival, and [DLV-34](../README.md#rule-dlv-34) moves scope only between named tasks. They stay this task's [WP-42.05](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.05) acceptance (its obligation stays 'full') and are recorded as 'blocked on an assigned owner of the [WP-42.05](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.05) client halves (entitlement caching by version, re-reading on a hint, the offline staleness behaviour and local-data survival on each client), not proven', an open gap in [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) item 20 that gates completion until a coordinator ruling names the recipient client tasks. The earlier sentence of this note that the client halves are the consumers' acceptance is withdrawn. (2) GetSnapshot and Check are registered through one mechanism, the CLOUD.21 endpoint registry, which builds their RpcPolicy entries from the CON.41 operation metadata, with this task's row in the operation-to-owner coverage table (the CLOUD.86 form); the HostModules.cs write with hand-written RpcPolicy.Unary entries is removed. This task already runs after CLOUD.21 (it starts on CLOUD.23, which starts on CLOUD.21). Planning repair fix8 delta 2026-10-11 ([DLV-34](../README.md#rule-dlv-34); coordinator rulings S59(8) and S59(10)). (1) IEntitlementDefinitionSource is owned by this task, the Entitlement module: it binds the port over the Entitlement-owned definitions activations that Design #249 added (data model 01), through the module's own store and plans, with no COM.02 edge. The 'blocked on the IEntitlementDefinitionSource production binding' legs are withdrawn, and production resolution stays blocked only on CLOUD.87. If the definition content behind an activated version has no in-scope publisher when this task is implemented, the claimant records that leg as 'blocked on <owner>, not proven' and stops for a coordinator ruling instead of compiling definitions into code. RES-cloud-storage-plans (append) is declared for a read plan the binding may need. (2) [WP-42.05](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.05) client halves (S59(10)): the desktop half is PLT.20's own completion-follow-up acceptance (PLT.20 already completes on this task, so no cycle), and the Android and Web halves are named on AND.19 and WEB.14 with notes and stay outside this run. This task keeps the Cloud half only; the review-round-2 sentences that kept the client halves here as an unassigned gap gating completion are superseded. |

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
| Start prerequisites | **artifact** [COM.05](#task-com-05) — entitlement rollback path. *Why:* a refund must verifiably reverse the grant(s) it funded<br>**artifact** [COM.09](#task-com-09) — ledger entries to export. *Why:* the evidence export is built from ledger + event + entitlement history, which only exist once COM.09 posts them<br>**artifact** [COM.16](#task-com-16) — the RevokeGrant side of the published grant port. *Why:* a refund rolls entitlement back by appending a revocation against the grant it funded ([GR-03](../../../requirements/04-commerce-entitlement-and-credits.md#rule-gr-03)), which Commerce can do only through the published port ([EO-03](../../../architecture/16-billing-and-commerce-architecture.md#rule-eo-03)) |
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
| Start prerequisites | **artifact** [COM.03](#task-com-03) — paid period identifiers (checkout/order confirmation producing a period_ref-worthy paid interval). *Why:* a service term's period_ref is the paid period's own identity, which only the purchase pipeline mints<br>**artifact** [COM.05](#task-com-05) — offer assignment and entitlement kind. *Why:* service term sourcing includes the currently assigned offer; the resolver is where offer assignment is decided<br>**artifact** [COM.04](#task-com-04) — deduplicated ProviderEvent stream. *Why:* [TM-02](../../../architecture/data-model/01-cloud-data-model.md#rule-tm-02) requires provider-event dedup to live in commerce.provider_event so a replayed event cannot extend a term twice; the inbox is the only place that dedup exists<br>**artifact** [COM.16](#task-com-16) — the widened append path of the durable Entitlement store for service terms and term actions, with its D1 plans. *Why:* a term, a renewal or a plan-change supersede must commit atomically with the snapshot refresh it causes (the resolver port carried grants and revocations only); COM.16 provides the one append path and the D1 plans, COM.11 owns the term rules |
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
| Start prerequisites | **contract** [CON.14](contracts.md#task-con-14) — the OperatorService full RPC surface (ProposeAction/ApproveAction/execute, grant/revokeGrant/issueCredit/adjustCredit/refund message shapes, eight authorization fields, negative vectors) per registry04 §9. *Why:* only a single placeholder message (OperatorCallContext, a context shape with no RPCs) exists at Contracts HEAD e6c4a77f; no operator service or per-domain RPC message is generated yet<br>**artifact** [CLOUD.21](cloud.md#task-cloud-21) — real identity/dispatch conformance for operator calls. *Why:* the operator paragraph explicitly assigns 'real identity/dispatch conformance' to [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23); operator RPCs need that routing/auth layer to refuse public customer/PAT/agent callers<br>**artifact** [COM.05](#task-com-05) — grant/revocation model. *Why:* grant/revokeGrant operate directly on COM.05's EntitlementGrant/EntitlementRevocation<br>**artifact** [COM.08](#task-com-08) — credit lot issue/adjust primitives. *Why:* issueCredit/adjustCredit operate on COM.08's CreditLot model<br>**artifact** [COM.10](#task-com-10) — refund/rollback path. *Why:* the refund RPC drives COM.10's refund-with-rollback mechanism<br>**artifact** [COM.16](#task-com-16) — the IssueGrant and RevokeGrant port carrying the [GR-05](../../../requirements/04-commerce-entitlement-and-credits.md#rule-gr-05) reason. *Why:* operator grant and revokeGrant (AdminGrant and Compensation sources) must reach Entitlement through the published interface with reason, operator and incident reference, never through its tables or its internal service |
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

<a id="task-com-16"></a>

### COM.16 — Entitlement grant port and durable Entitlement store

**Outcome.** Commerce, the operator path and the refund path reach Entitlement only through one published IssueGrant/RevokeGrant port that lives in ArcForges.Cloud.Modules.Abstractions and is implemented by the Entitlement module ([EO-03](../../../architecture/16-billing-and-commerce-architecture.md#rule-eo-03), [MD-03](../../../architecture/05-cloud-architecture.md#rule-md-03)), so no module references Entitlement internals or writes its tables; an administrative, compensation or migration grant carries its reason on the grant row ([GR-05](../../../requirements/04-commerce-entitlement-and-credits.md#rule-gr-05)); and the Entitlement module has its production D1 store: grants, revocations, service terms, term actions, definitions activations, workspace status facts and the derived snapshot (the whole resolver output) are appended and replaced in one guarded named plan under the workspace revision together with the owner receipt and notification outbox row, so a grant or term never exists without the snapshot and EntitlementVersion that reflect it, a stale writer commits nothing, and the snapshot rebuilt from the D1-stored records equals the stored snapshot. The Entitlement store reaches D1 only through a generic plan-execution port that this task creates in ArcForges.Cloud.Modules.Abstractions (outside the Entitlement folder, so every later module reuses it) and a Storage.D1 adapter that implements it over the signed Worker executor; an Entitlement plan names only entitlement_ and platform_ tables. The port commits on its own; joining the same grant statements to the enumerated purchase unit of work is the Entitlement participation of CLOUD.63.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/com-16` and ledger record `ledger/tasks/com-16.md` in the Plan repository; task branch `task/com-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-42.04](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.04) — the Commerce-facing grant interface ([EO-03](../../../architecture/16-billing-and-commerce-architecture.md#rule-eo-03): IssueGrant and RevokeGrant as a public port in the shared Abstractions project, implemented by the Entitlement module), the [GR-05](../../../requirements/04-commerce-entitlement-and-credits.md#rule-gr-05) reason carried on the grant row, and the durable D1 Entitlement store: grants, revocations, service terms and term actions committed atomically with the snapshot and its EntitlementVersion under one guarded plan, with rebuild equivalence over D1-stored records (the resolver, its rules and its in-memory-store rebuild equivalence are COM.05) |
| Provides | entitlement-grant-port; entitlement-d1-store |
| Start prerequisites | **artifact** [COM.05](#task-com-05) — the grant and revocation model, the EntitlementService admission rules and the IEntitlementStore port contract. *Why:* the port exposes, and the D1 store implements, exactly the contract COM.05 defined and tested; nothing of the resolver or its admission rules is redefined here<br>**artifact** [CLOUD.03](cloud.md#task-cloud-03) — the physical entitlement tables (grant with its reason column, revocation, revision, snapshot, service_term and service_term_action), their append-only triggers and the typed bind/result adapters. *Why:* the store binds to the checked-in physical manifest; the manifest is generated from model 01, whose entitlement.grant now carries the [GR-05](../../../requirements/04-commerce-entitlement-and-credits.md#rule-gr-05) reason, and the only tables this task adds are the three append-only inputs model 01 now lists (entitlement.definitions_activation, workspace_status_fact and feature_release)<br>**artifact** [CLOUD.04](cloud.md#task-cloud-04) — the owner receipt and notification outbox rows of a guarded write. *Why:* every atomic guarded write carries its receipt and outbox entry in the same batch, and the snapshot commit is such a write ([ES-04](../../../requirements/04-commerce-entitlement-and-credits.md#rule-es-04): the realtime hint is published from that outbox row)<br>**artifact** [CLOUD.06](cloud.md#task-cloud-06) — the guarded-batch executor and its revision guard primitive with the [SU-04](../../../architecture/04-desktop-application-architecture.md#rule-su-04) module order. *Why:* the commit is one guarded batch of the Entitlement participant; it runs through the shared engine instead of a private executor |
| Entry condition | [ADOPT.07.commerce](adoption.md#task-adopt-07-commerce) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.16](cloud.md#task-cloud-16), [CLOUD.63](cloud.md#task-cloud-63), [CLOUD.72](cloud.md#task-cloud-72), [CLOUD.87](cloud.md#task-cloud-87), [COM.04](#task-com-04), [COM.06](#task-com-06), [COM.10](#task-com-10), [COM.11](#task-com-11), [COM.13](#task-com-13) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Abstractions/Entitlement/** (new and public: the IssueGrant and RevokeGrant port with its request, result and refusal types, built from primitives only and referencing no module and no Entitlement internal type; cross-module ports belong to this shared boundary project (architecture 01 section 5, MD-03); no change to IModuleBoundary or ModuleDescriptor; the generic plan-execution port is not part of this folder: see Abstractions/Storage/**)`<br>`Cloud:src/ArcForges.Cloud.Modules.Abstractions/Storage/** (new and public: the generic plan-execution port, a named plan id with exact typed parameters in, typed rows or a typed refusal out, that a module project may use because a module references only this project and never the storage layer; it names no table, no SQL and no module; CLOUD.02 published none, and CLOUD.04 and CLOUD.06 write only inside Storage.D1 and so cannot publish one)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/ModuleBinding/** and Cloud:src/ArcForges.Cloud.Storage.D1/ArcForges.Cloud.Storage.D1.csproj (new folder owned by this task, no overlap with the Migrations, Physical, Receipts, Outbox or SharedFamilies folders of CLOUD.03, CLOUD.04 and CLOUD.06: the adapter that implements the Abstractions plan-execution port over the existing signed Worker executor and refuses a plan id whose owner is not the caller's module descriptor; the project file only for the project reference to Abstractions; later module tasks reuse the adapter and add nothing here)`<br>`Cloud:src/ArcForges.Cloud.Modules.Entitlement/** except Resolver/Domain (the port adapter over EntitlementService that carries the reason, the widened EntitlementAppend that also carries service terms and term actions, the D1 IEntitlementStore under Persistence/** written against the Abstractions plan-execution port, and the module's own Register entry listing them; the resolver rules, rebuild semantics and admission rules of COM.05 are unchanged)`<br>`Cloud:storage/plans/entitlement/** and the generated plan manifest in Cloud:src/ArcForges.Cloud.Storage.D1/PlanManifest.g.cs (the Entitlement module's named plans as owner entitlement, naming only entitlement_ and platform_ tables (CM-01 to CM-03); the manifest hash is regenerated by the author after rebase; RES-cloud-storage-plans)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Migrations/** (one append-only expand migration under Migrations/pending that creates the three new entitlement tables with their append-only triggers and any index the plans need; numbered at merge by the integration owner; RES-cloud-d1-migrations)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Physical/manifest/entitlement.json and Cloud:src/ArcForges.Cloud.Storage.D1/Physical/PhysicalSchema.g.cs (the Entitlement module's own manifest file, only the three new tables with their inline enum, and the regenerated column maps, hash and migration identity; no other owner's manifest changes; RES-cloud-d1-migrations)`<br>`Cloud:worker/storage/plans.generated.ts, Cloud:tests/worker/**, Cloud:eng/verification/d1-entitlement-local.ts and the script entry for it in Cloud:package.json (the regenerated Worker plan dictionary; the Entitlement plan and migration tests on the SQLite oracle and the counts and pins the physical-schema tests assert for the three new tables; the explicit local opt-in run on workerd's D1 for the atomic commit and the concurrent writers, never CI)`<br>`Cloud:src/**/packages.lock.json and Cloud:tests/**/packages.lock.json (only the project-reference entries that the new Storage.D1 reference to the Abstractions project adds; no package coordinate or integrity value changes)`<br>`Cloud:docs/d1-physical-schema.md, Cloud:docs/d1-receipts-outbox.md and Cloud:CONTRIBUTING.md (only the table counts, the stated limit that no module owns a tail-carrying plan yet, and the opt-in local command this task changes)`<br>`Cloud:src/ArcForges.Cloud/Composition/HostModules.cs (only the append that binds the Storage.D1 ModuleBinding adapter to the Abstractions plan-execution port, and the Entitlement store to the Entitlement port, by composition; RES-cloud-host-composition)`<br>`Cloud:tests/ArcForges.Cloud.Tests/Entitlement/** and Cloud:tests/ArchitectureTests/** (port contract tests and store tests; the architecture tests only to assert that Commerce reaches Entitlement only through the Abstractions port and that the Abstractions project references no module)`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/com-16-*.json (new immutable successor chained from the then-active receipt, only because hash-bound project and release inputs change; no coordinate, integrity value or closure entry changes)`<br>`Cloud:eng/provenance/** (immutable successor release profile, Worker bundle and runtime-notice records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt)`<br>`Cloud:docs/entitlement-resolver.md (the port, the reason column and the store replace the stated limits it records), Cloud:docs/storage-plans.md (the entitlement owner) and Cloud:AGENTS.md (only if the module description changes)` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append), [RES-cloud-storage-plans](../shared-resources.md#res-cloud-storage-plans) (append), [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | Offline unit tests: port contract (idempotent replay by source reference, stale-version refusal, reason required for administrative, compensation and migration grants, no Entitlement type crosses the port), store tests through the plan-bridge fakes and the physical column map (atomic append and snapshot replace, a stale revision commits nothing, concurrent writers, append-only enforcement, reason round trip), rebuild equivalence over D1-stored fixture records, architecture tests for the Commerce-to-Entitlement path; opt-in local runtime run against a real D1 instance for the atomic commit and the concurrent-writer case per docs/validation-policy.md; no hosted runtime, live-service or browser CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Port contract and architecture test results; the D1 atomic-commit, stale-revision and concurrent-writer results (the local D1 run recorded once, or recorded as untested); rebuild-equivalence result over D1-stored records; reason round-trip result; source commit. |
| Baseline (unreviewed unless accepted) | not-started Observed, unreviewed: COM.05 (Cloud PR 47, in review) keeps the resolver service internal to the Entitlement project, tests it against an in-memory store only and records that the Commerce grant port, the [GR-05](../../../requirements/04-commerce-entitlement-and-credits.md#rule-gr-05) reason column and the D1 store have no owning task; CLOUD.02 (complete) published only IModuleBoundary and ModuleDescriptor in the Abstractions project. |
| Notes | Added by the COM.05 review finding that nothing owned the [EO-03](../../../architecture/16-billing-and-commerce-architecture.md#rule-eo-03) port, the [GR-05](../../../requirements/04-commerce-entitlement-and-credits.md#rule-gr-05) reason column or the D1 IEntitlementStore. Decisions: the port type lives in Abstractions (Commerce cannot reference the Entitlement project); the reason column is a model 01 correction made by the planning pair that added this task and is mapped by the CLOUD.03 manifest; the D1 store is the Entitlement module's own persistence (module owners own their plans, architecture 01 section 5), not CLOUD.63, which joins the same statements to the shared families once Commerce exists. Plan execution: a module project references only Abstractions (docs/storage-plans.md), so this task creates the generic plan-execution port in Abstractions/Storage/** and its adapter in Storage.D1/ModuleBinding/**, and an Entitlement plan may name only entitlement_ and platform_ tables. Revision guard: the per-workspace revision COM.05's port commits under is held in the new Entitlement-owned table entitlement.revision (model 01, added by the planning pair that added this task), never in a workspace_ table, and every Entitlement commit guards and increments it in the same batch. The persistence of the workspace status facts, feature releases and definitions activations that COM.05's record set reads is settled by the planning pair that amended model 01 for COM.16 (never decided in code, [D-001](../../../decisions/phase-1-foundation-decisions.md#rule-d-001), [ADP-07](../adoption.md#rule-adp-07)): three new append-only Entitlement-owned records, entitlement.definitions_activation, entitlement.workspace_status_fact and entitlement.feature_release, so the whole record set of a snapshot lives in entitlement_ tables; workspace.state and the commerce.subscription fields stay owned by their modules, only the Entitlement module appends to the three records, and trust and safety (status facts) and configuration (feature releases) reach it through ports their own tasks add, so COM.16 stores, reads and tests the records and publishes no port for them. The entitlement.snapshot row holds the whole resolver output (model 01 gives the shapes of its three json columns), so rebuild equivalence is a comparison of the stored row with a rebuild from the stored records. Revision fence: the guard reads an absent entitlement.revision row as revision 0 and the first commit of a workspace creates the row with an insert that cannot overwrite an existing one, so two concurrent first commits cannot both succeed. The service terms and term actions a later owner appends (COM.11) travel through the same widened append as complete rows, so a term row and its action carry every column of model 01. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): the generated TypeScript plan dictionary (worker/storage/plans.generated.ts) becomes data generated from C# under CLOUD.84. The port, store and tests named here are otherwise unchanged. Outcome, validation and evidence above are recorded history and are unchanged. |
