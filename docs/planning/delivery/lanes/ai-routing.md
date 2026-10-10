# Workers AI routing and metering — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Provider adapters, routing, tariffs, metering, settlement and transparency.

Tasks: 10 · Owning repositories: Cloud · Integration owner(s): Cloud integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [AIR.00](#task-air-00) | Provider adapters and routing (Workers AI) | service | L | [CON.10](contracts.md#task-con-10) (contract), [POL.08](policy.md#task-pol-08) (artifact), [HAR.40](harness.md#task-har-40) (artifact) | not-started |
| [AIR.01](#task-air-01) | Tariffs and cost dimensions | service | M | [POL.02](policy.md#task-pol-02) (artifact) | not-started |
| [AIR.02](#task-air-02) | Metering and settlement | service | L | [COM.08](commerce.md#task-com-08) (artifact), [AIR.00](#task-air-00) (artifact) | not-started |
| [AIR.03](#task-air-03) | Selected supplier and realm routing (no BYOK) | service | M | [AIR.00](#task-air-00) (artifact) | not-started |
| [AIR.04](#task-air-04) | Provider interaction records, redaction and cost transparency | service | M | [AIR.02](#task-air-02) (artifact), [CLOUD.69](cloud.md#task-cloud-69) (artifact) | not-started |
| [AIR.05](#task-air-05) | Content-origin marking at the provider generation boundary | service | M | [AIR.00](#task-air-00) (artifact) | not-started |
| [AIR.06](#task-air-06) | Funding and uncertain-outcome proof | service | M | [AIR.02](#task-air-02) (artifact) | not-started |
| [AIR.07](#task-air-07) | Provider test-environment coverage | service | M | [AIR.00](#task-air-00) (artifact) | not-started |
| [AIR.08](#task-air-08) | Real-provider metering evidence and stubbed-path removal | integration | L | [AIR.00](#task-air-00) (artifact), [AIR.02](#task-air-02) (artifact), [AST.15](assistant.md#task-ast-15) (artifact) | not-started |
| [AIR.90](#task-air-90) | Verify owned artifact and real integration (AI routing and metering) | service | M | [AIR.08](#task-air-08) (artifact), [AIR.01](#task-air-01) (artifact), [AIR.03](#task-air-03) (artifact), [AIR.04](#task-air-04) (artifact), [AIR.05](#task-air-05) (artifact), [AIR.06](#task-air-06) (artifact), [AIR.07](#task-air-07) (artifact) | not-started |

## Tasks

<a id="task-air-00"></a>

### AIR.00 — Provider adapters and routing (Workers AI)

**Outcome.** Workers AI provider adapters in the C# Cloud Agent module (default and fast text, accepted image context, bge-m3 embedding) build each request, parse each response and normalise usage in C#; they dispatch only through the HAR.40 ai.internal thin adapter on the env.AI binding; model availability, frozen configuration, request limits and tool-stream shapes are validated in C# before dispatch; C# records admission, routing and supplier version while CF executes the already-admitted intent. No Workers AI token, REST path or AI Gateway is used.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-00` and ledger record `ledger/tasks/air-00.md` in the Plan repository; task branch `task/air-00` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L · early risk proof |
| Obligations | [WP-43.00](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00) — full |
| Provides | workers-ai-adapter |
| Start prerequisites | **contract** [CON.10](contracts.md#task-con-10) — published internal AI HTTP profile (model-intent/model-outcome/dispatch ports) from internal/ai-http/v1/schema.json. *Why:* the adapter is called through this fixed internal contract, already scaffolded in Contracts (a CommitReceipt shape observed there)<br>**artifact** [POL.08](policy.md#task-pol-08) — active model/route policy snapshot naming the admitted catalogue subset. *Why:* [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06) requires policy to gate which models are activatable; routing cannot hardcode the catalogue<br>**artifact** [HAR.40](harness.md#task-har-40) — the ai.internal thin adapter and the Hello-slice dispatch path, with the Workers AI binding shapes proven. *Why:* provider adapters dispatch through the single Workers AI adapter surface, and the binding shapes are proven in HAR.40 before the catalogue adapters are built |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.02](#task-air-02), [AIR.03](#task-air-03), [AIR.05](#task-air-05), [AIR.07](#task-air-07), [AIR.08](#task-air-08), [CLOUD.67](cloud.md#task-cloud-67), [HAR.00](harness.md#task-har-00), [HAR.05](harness.md#task-har-05), [SRCH.06](search.md#task-srch-06) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Agent/Providers/**`<br>`Cloud:src/ArcForges.Cloud.Modules.Agent/Inference/**` |
| Shared resources | [RES-private-configuration](../shared-resources.md#res-private-configuration) (append) |
| Validation | Actual selected model and capability-shape tests, withdrawn/unknown/unsupported request tests, request-size and output-bound tests, version-mismatch tests in ArcForges.Cloud.Tests against recorded fixtures (offline). Real Workers AI calls only at the credentialed candidate gate, run locally opt-in against the deployed proof origin, never in ordinary CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): no real AI inference in CI). |
| Completion evidence | Routing decision, explainability and streaming results. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08. Cloud b05361e: module shell only (src/ArcForges.Cloud.Modules.Agent: AgentModule.cs and project); no Providers or Inference code; no worker/ai adapter; wrangler.json has no ai binding. AI main b2b3aa2: Hello slice only (src/index.ts HelloAgentWorkflow, hello.ts, model.ts, deployment.ts, model-diagnostics.ts); no src/providers, src/inference, src/streams, src/mcp or src/workflows tree; tests/workflow.test.ts and docs/evidence/workflow-*.json are early probe scaffolding. |
| Notes | Narrow early risk proof: if env.AI.run cannot actually deliver the required capability shapes (tool/stream) as specified, the whole AI economics/product model is affected. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): the adapter moves from the AI repository (src/providers/workers-ai, not on main) into the C# Cloud Agent module, and the Workers AI invocation is reduced to the HAR.40 ai.internal thin adapter ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) items 1 and 5). Catalogue, routing, admission and version-recording requirements are unchanged. The narrow early risk proof (capability shapes, latency, gpt-oss tier, 429 semantics) runs in HAR.40 before the catalogue adapters are built. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021); review fix): the exclusive hold on RES-ai-workflow-and-routes is withdrawn. AIR.00 no longer runs against the AI deployment environment and its writes are Cloud paths; its shared list keeps RES-private-configuration only. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: the bge-reranker-base rerank adapter is out of scope, not completed; the bge-m3 embedding adapter stays for the semantic leg (S4). |

<a id="task-air-01"></a>

### AIR.01 — Tariffs and cost dimensions

**Outcome.** Versioned tariffs with effective dates and the full cost-dimension set exist; each run locks a tariff snapshot at start; a historical charge is reconstructible from its locked snapshot; image-context units are metered separately from text units.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-01` and ledger record `ledger/tasks/air-01.md` in the Plan repository; task branch `task/air-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-43.01](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.01) — full |
| Provides | ai-tariffs |
| Start prerequisites | **artifact** [POL.02](policy.md#task-pol-02) — the customerTariffs/supplierPrices keys in Private configuration.v1 and its signed activation mechanism. *Why:* tariffs are policy-owned configuration (contracts/08's Private configuration.v1 names customerTariffs/supplierPrices explicitly as a [WP-43](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43)/[WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) shared schema); AIR.01 consumes [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44)'s activation rather than inventing its own config channel |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Agent/Tariffs/**`<br>`Cloud:storage/plans/agent/tariffs/**`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Migrations/**` |
| Shared resources | [RES-private-configuration](../shared-resources.md#res-private-configuration) (append), [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append), [RES-cloud-storage-plans](../shared-resources.md#res-cloud-storage-plans) (append) |
| Validation | Rate-change immutability test, historical-explainability reconstruction test, per-dimension metering tests -- offline. |
| Completion evidence | Rate-change immutability and historical explainability results. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08 (Cloud b05361e): module shell only (src/ArcForges.Cloud.Modules.Agent: AgentModule.cs and project); no Tariffs code and no storage/plans/agent folder. The POL.02 configuration channel is not built. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): write paths corrected from src/Cloud/ArcForges.Cloud.Modules.Agent (not in the real layout) to src/ArcForges.Cloud.Modules.Agent; the tariff tables are Agent-owned D1 tables under storage/plans/agent/tariffs. The locked-snapshot, immutability and separate image-unit rules are unchanged. |

<a id="task-air-02"></a>

### AIR.02 — Metering and settlement

**Outcome.** C# reservation/intent commits before CF I/O, outcome receipt precedes settlement, attempt usage revisions are immutable; interactive runs and bounded inference jobs are both covered with stable attempt identity, supplier exposure, Run customer total and exact credit lots; unknown usage follows the deadline/liability ladder, never an automatic resend.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-02` and ledger record `ledger/tasks/air-02.md` in the Plan repository; task branch `task/air-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-43.02](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.02) — full |
| Provides | ai-metering-settlement |
| Start prerequisites | **artifact** [COM.08](commerce.md#task-com-08) — real budget/credit/admission ports (reservation, settlement transaction participants). *Why:* [WP-43](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43)'s own input table names this explicitly: '[WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) output -- Real budget/credit/admission ports; native ProductJobs do not provide AI economics'<br>**artifact** [AIR.00](#task-air-00) — a dispatchable provider call to meter. *Why:* metering has nothing to reserve/settle against before a call kind exists |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [COM.12](commerce.md#task-com-12) — the real capacity admission participant. *Why:* metering starts from the credits participant; its settlement acceptance also runs against the real capacity admission participant |
| Unblocks | [AIR.04](#task-air-04), [AIR.06](#task-air-06), [AIR.08](#task-air-08) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Agent/Metering/**`<br>`Cloud:storage/plans/agent/metering/**`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Migrations/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append), [RES-cloud-storage-plans](../shared-resources.md#res-cloud-storage-plans) (append) |
| Validation | Actual CF normal/interrupted/lost outcome with concurrent duplicates and replayed receipts; cancelled/unknown hold sweep; tariff-change and operator-job isolation tests. Real-CF cases only at the credentialed candidate gate. |
| Completion evidence | Metering accounting, idempotency, sweep and overdraft results. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08 (Cloud b05361e): module shell only (src/ArcForges.Cloud.Modules.Agent: AgentModule.cs and project); no Metering code and no storage/plans/agent folder. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): write paths corrected to the real Cloud module layout (src/ArcForges.Cloud.Modules.Agent, storage/plans/agent). Reservation before I/O, receipt before settlement, immutable revisions and the no-automatic-resend ladder are unchanged; the dispatch being metered goes through the HAR.40 ai.internal adapter. |

<a id="task-air-03"></a>

### AIR.03 — Selected supplier and realm routing (no BYOK)

**Outcome.** Only the Workers AI binding and explicit admitted catalogue route calls, with no AI Gateway/multiprovider bypass/fallback; self-host uses operator-owned credentials/funding with payment disabled by default; no silent substitution or credit crossing between official/self-host realms.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-03` and ledger record `ledger/tasks/air-03.md` in the Plan repository; task branch `task/air-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-43.03](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.03) — full |
| Provides | ai-realm-routing |
| Start prerequisites | **artifact** [AIR.00](#task-air-00) — the adapter's admitted-catalogue validation. *Why:* realm routing decides among the same catalogue AIR.00 validates |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Agent/Routing/**` |
| Shared resources | [RES-private-configuration](../shared-resources.md#res-private-configuration) (append) |
| Validation | Unavailable/withdrawn model, missing price/config, pre-dispatch-refusal-vs-unknown-dispatch, explicit-new-model-request tests -- offline. |
| Completion evidence | No-BYOK structural assertions and credential-custody results. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08 (Cloud b05361e): module shell only (src/ArcForges.Cloud.Modules.Agent); no Routing code; no worker/ai adapter yet. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): write path corrected to src/ArcForges.Cloud.Modules.Agent/Routing (real layout). Routing invocation is only the HAR.40 Workers AI binding adapter, with no AI Gateway, multiprovider bypass or BYOK ([PR-06](../../../architecture/04-desktop-application-architecture.md#rule-pr-06) unchanged). |

<a id="task-air-04"></a>

### AIR.04 — Provider interaction records, redaction and cost transparency

**Outcome.** A provider interaction record exists per call, separate from execution/capability/audit traces, carrying no content beyond policy; cost transparency surfaces show what a run cost and why.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-04` and ledger record `ledger/tasks/air-04.md` in the Plan repository; task branch `task/air-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-43.04](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.04) — interaction record, redaction, and cost-transparency surfaces (Cloud side) |
| Provides | ai-interaction-records |
| Start prerequisites | **artifact** [AIR.02](#task-air-02) — metered attempts to record interactions against. *Why:* an interaction record without a metered attempt has nothing to redact/explain<br>**artifact** [CLOUD.69](cloud.md#task-cloud-69) — the Cloud-side correlation seam for the provider interaction record. *Why:* propagating correlation once is a Cloud seam ([CR-06](../../../architecture/13-observability-and-operations.md#rule-cr-06)); this task builds on it instead of adding per-module propagation |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90), [PLT.53](platform.md#task-plt-53) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Agent/InteractionRecords/**`<br>`Cloud:storage/plans/agent/interaction-records/**`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Migrations/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append), [RES-cloud-storage-plans](../shared-resources.md#res-cloud-storage-plans) (append) |
| Validation | Trace-separation test; content-redaction test; cost-explainability test -- offline. |
| Completion evidence | Trace separation, redaction and cost explainability results. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08 (Cloud b05361e): module shell only (src/ArcForges.Cloud.Modules.Agent); no InteractionRecords code and no storage/plans/agent folder. |
| Notes | Planning repair 2026-10-05: every provider interaction record carries the call's correlation identity and the provider request identifier ([CR-05](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cr-05)) through the CLOUD.69 seam; this is part of this task's own acceptance and of the real provider hop that PLT.48's correlation scenario names as a later owner (no new write scope). Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): write paths corrected to the real Cloud module layout (src/ArcForges.Cloud.Modules.Agent, storage/plans/agent). The record, redaction and transparency acceptance is unchanged. |

<a id="task-air-05"></a>

### AIR.05 — Content-origin marking at the provider generation boundary

**Outcome.** The frozen content-origin profile is implemented in C# at the point AI-generated content is produced (the Agent module generation boundary, after the ai.internal adapter returns the output); every artifact type carries the required transparency marking; malformed or hash-mismatched marks and marking retry are handled; this satisfies [VG-01](../../../assurance/open-gates-register.md#rule-vg-01) once the regime determination is recorded.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-05` and ledger record `ledger/tasks/air-05.md` in the Plan repository; task branch `task/air-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-43.04](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.04) — transparency marking mechanism at the provider generation boundary; marking-coverage per artifact type |
| Provides | ai-content-origin-marking |
| Start prerequisites | **artifact** [AIR.00](#task-air-00) — generated model output to mark. *Why:* marking attaches to the adapter's own output boundary |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90), [HAR.03](harness.md#task-har-03) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Agent/ContentOrigin/**`<br>`Cloud:tests/ArcForges.Cloud.Tests/Vectors/AiContentOrigin/**` |
| Validation | Real provider text through durable output and downstream carrier fixtures; deterministic/non-AI and legacy controls; malformed or hash-mismatched mark; marking retry. Offline in ArcForges.Cloud.Tests against fixture carriers; real text only at the AIR.08 credentialed gate. |
| Completion evidence | Marking-coverage results per artifact type; carrier/propagation/failure vectors with payload and manifest hashes. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08. Cloud b05361e: module shell only (src/ArcForges.Cloud.Modules.Agent: AgentModule.cs and project); no ContentOrigin code. AI main b2b3aa2: Hello slice only; no ContentOrigin code on main. |
| Notes | HAR.03 ([WP-52.03](../../work-packages/52-cloud-harness.md#rule-wp-52.03) durable output) consumes this task's ContentOrigin carrier as a start artifact -- internal the AI lanes cross-reference. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): marking logic moves from the AI repository TypeScript provider boundary (src/providers/workers-ai/ContentOrigin, not on main) to C#, because content-origin compliance is business logic ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 1). Coverage per artifact type and the carrier, propagation and failure vectors are unchanged; HAR.03 still consumes this carrier. |

<a id="task-air-06"></a>

### AIR.06 — Funding and uncertain-outcome proof

**Outcome.** Supplier intent/exposure and customer settlement are proven independent: Brave search is operator-funded while processing results is customer inference; a crash before/after dispatch, an unknown deadline, and late usage after a closed no-later-debit window are all handled without an automatic model retry.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-06` and ledger record `ledger/tasks/air-06.md` in the Plan repository; task branch `task/air-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-43.05](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.05) — full |
| Provides | ai-funding-uncertainty-proof |
| Start prerequisites | **artifact** [AIR.02](#task-air-02) — the reservation/settlement engine to prove uncertainty handling against. *Why:* this substep proves AIR.02's ledgers under crash/uncertain scenarios, it doesn't build a new ledger |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90), [HAR.04](harness.md#task-har-04), [SRCH.06](search.md#task-srch-06) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.Agent/Metering/UncertainOutcome/**` |
| Validation | Search-without-customer-debit, model-debit-once, crash-before/after-dispatch, unknown-deadline, late-usage-after-closed, no-automatic-retry tests -- offline with real-CF-shaped fixtures; real dispatch only at AIR.08's gate. |
| Completion evidence | Degradation, reservation-release and alert results. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08 (Cloud b05361e): module shell only (src/ArcForges.Cloud.Modules.Agent: AgentModule.cs and project); no UncertainOutcome code. |
| Notes | HAR.04 ([WP-52.04](../../work-packages/52-cloud-harness.md#rule-wp-52.04) general effect-certainty classification) treats this task's ledger pattern as its worked precedent -- internal the AI lanes cross-reference. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): write path corrected from src/Cloud/ArcForges.Cloud.Modules.Agent to src/ArcForges.Cloud.Modules.Agent (real layout). The uncertain-outcome, funding-separation and no-automatic-retry acceptance is unchanged. |

<a id="task-air-07"></a>

### AIR.07 — Provider test-environment coverage

**Outcome.** Every provider integration is exercised in C# against the provider's own test environment, with its contract shape frozen as recorded fixtures so ordinary CI never depends on provider availability.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-07` and ledger record `ledger/tasks/air-07.md` in the Plan repository; task branch `task/air-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-43.06](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.06) — full |
| Provides | ai-provider-test-env-coverage |
| Start prerequisites | **artifact** [AIR.00](#task-air-00) — the adapter to exercise against the test environment. *Why:* nothing to record fixtures from before the adapter exists |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90) |
| Write scope | `Cloud:tests/ArcForges.Cloud.Tests/Vectors/AiProvider/**`<br>`Cloud:tests/Cloud.Tests.Integration/AiProviderEnvironment/**` |
| Validation | Per-provider test-environment run (credentialed, local opt-in, never ordinary CI); fixture-driven C# CI run with the provider deliberately unreachable, per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Per-provider test-environment runs and fixture-driven CI results -- [PG-10](../../../assurance/open-gates-register.md#rule-pg-10). |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08. AI main b2b3aa2 has tests/ArchitectureTests, hello, model, workflow and model-diagnostics tests and no provider-fixtures tree. Cloud b05361e: tests/ArcForges.Cloud.Tests has no AiProvider vectors and no Cloud.Tests.Integration project exists yet. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): provider fixtures and tests migrate from the AI repository (tests/provider-fixtures, TypeScript) to C# ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 1: C# test suites replace the TypeScript ones one-for-one). Fixture shapes, [PG-10](../../../assurance/open-gates-register.md#rule-pg-10) evidence and the no-CI-dependency rule are unchanged. |

<a id="task-air-08"></a>

### AIR.08 — Real-provider metering evidence and stubbed-path removal

**Outcome.** Actual Workers AI responses for each selected capability are recorded and normalized into independent sanitized fixtures; deterministic fixtures run on ordinary CI while the credentialed real-CF candidate gate proves exact Worker/model/config identity; the [WP-17.05](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.05) stubbed managed provider path is retired.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-08` and ledger record `ledger/tasks/air-08.md` in the Plan repository; task branch `task/air-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / L |
| Obligations | [WP-43.07](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07) — full |
| Provides | ai-real-provider-evidence |
| Start prerequisites | **artifact** [AIR.00](#task-air-00) — the real adapter to record responses from. *Why:* nothing to normalize without the real adapter<br>**artifact** [AIR.02](#task-air-02) — the real settlement engine to reconcile the recorded evidence through. *Why:* [PG-13](../../../assurance/open-gates-register.md#rule-pg-13) requires 'one real provider usage response + one real payment-provider event reconciled through same code as fixtures'<br>**artifact** [AST.15](assistant.md#task-ast-15) — assistant admission path that carried the stubbed provider. *Why:* the stubbed path is removed from the consumer that introduced it |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90) |
| Permitted substitutes | [SUB-stubbed-provider-path](../substitutes.md#sub-stubbed-provider-path) |
| Write scope | `Cloud:tests/ArcForges.Cloud.Tests/Vectors/AiEvidence/**`<br>`Cloud:tests/Cloud.Tests.Integration/AiMetering/**` |
| Validation | Model response drift, missing category, cumulative stream, embedding result validation tests offline; controlled real-provider run at the credentialed candidate gate only. |
| Completion evidence | Real-provider normalisation, settlement and worked-fixture results -- [PG-13](../../../assurance/open-gates-register.md#rule-pg-13). |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08. No real-provider evidence exists in either repository. AI docs/evidence holds Hello-slice evidence only (gpt-oss-20b). Cloud b05361e has no Cloud.Tests.Integration project yet. |
| Notes | This task is the structural replacement named in implementation-sequence.md Sec.3.1: 'Stubbed managed provider path ([WP-17.05](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.05))... Deleted by [WP-43.00](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00), [WP-43.07](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07)' -- AIR.00 builds the real path, AIR.08 proves and removes the stub. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): sanitised real-provider fixtures migrate from the AI repository (tests/provider-fixtures) to the C# test vectors. Normalisation, the stub retirement, the [PG-13](../../../assurance/open-gates-register.md#rule-pg-13) reconciliation and the credentialed gate are unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: the rerank result validation and fixtures are out of scope, not completed; the embedding result validation stays for the semantic leg (S4). |

<a id="task-air-90"></a>

### AIR.90 — Verify owned artifact and real integration (AI routing and metering)

**Outcome.** All AIR deliverables assemble under the selected repository/package/runtime/protocol authorities with the frozen Workers AI model subset, capability matrix, normalization and known/unknown usage contract proven; Gateway is confirmed not a required dependency.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/air-90` and ledger record `ledger/tasks/air-90.md` in the Plan repository; task branch `task/air-90` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Package acceptance | Records the [WP-43](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-43.90](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.90) — remaining aggregation/receipt<br>[WP-43](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure: real ExecutionOwner task/turn + operator-funded compaction/search support, durable receipts vs temporary bodies outside D1/SQLite/backups/checkpoints — package-level obligation contribution |
| Provides | ai-routing-package-acceptance |
| Start prerequisites | **artifact** [AIR.08](#task-air-08) — real-provider evidence. *Why:* acceptance cannot close without [PG-13](../../../assurance/open-gates-register.md#rule-pg-13) evidence in hand<br>**artifact** [AIR.01](#task-air-01) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [AIR.03](#task-air-03) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [AIR.04](#task-air-04) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [AIR.05](#task-air-05) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [AIR.06](#task-air-06) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [AIR.07](#task-air-07) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.ai-routing](adoption.md#task-adopt-07-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.06](release.md#task-rel-06) |
| Write scope | `Cloud:tests/Cloud.Tests.Integration/AiMetering/**` |
| Validation | Real selected model/tool/embedding cases and provider refusal/lost-result/usage reconciliation tied to C# admitted call and config identity; [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) proportionate. |
| Completion evidence | Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/provider, scenario, result, real-vs-fixture status. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08 (Cloud b05361e): module shells only (src/ArcForges.Cloud.Modules.Agent and .Task); no Agent domain code; tests/Cloud.Tests.Integration/AiMetering not yet created. |
| Notes | Also carries the [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) package closure text (real ExecutionOwner task/turn + operator-funded compaction/search support; durable receipts vs temporary bodies kept outside D1/SQLite history, backups and Workflow checkpoints). Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): the [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) closure text names Workflow checkpoints; in this Cloud task they mean executor checkpoints in D1 ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 5), and durable receipts stay outside D1/SQLite history, backups and executor checkpoints. No write or acceptance change. |
