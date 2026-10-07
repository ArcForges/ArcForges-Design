# Workers AI routing and metering — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Provider adapters, routing, tariffs, metering, settlement and transparency.

Tasks: 11 · Owning repositories: AI, Cloud · Integration owner(s): AI integration owner, Cloud integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [AIR.00](#task-air-00) | Provider adapters and routing (Workers AI) | service | L | [CON.10](contracts.md#task-con-10) (contract), [POL.08](policy.md#task-pol-08) (artifact) | not-started |
| [AIR.01](#task-air-01) | Tariffs and cost dimensions | service | M | [POL.02](policy.md#task-pol-02) (artifact) | not-started |
| [AIR.02](#task-air-02) | Metering and settlement | service | L | [COM.08](commerce.md#task-com-08) (artifact), [AIR.00](#task-air-00) (artifact) | not-started |
| [AIR.03](#task-air-03) | Selected supplier and realm routing (no BYOK) | service | M | [AIR.00](#task-air-00) (artifact) | not-started |
| [AIR.04](#task-air-04) | Provider interaction records, redaction and cost transparency | service | M | [AIR.02](#task-air-02) (artifact), [CLOUD.69](cloud.md#task-cloud-69) (artifact) | not-started |
| [AIR.05](#task-air-05) | Content-origin marking at the provider generation boundary | service | M | [AIR.00](#task-air-00) (artifact) | not-started |
| [AIR.06](#task-air-06) | Funding and uncertain-outcome proof | service | M | [AIR.02](#task-air-02) (artifact) | not-started |
| [AIR.07](#task-air-07) | Provider test-environment coverage | service | M | [AIR.00](#task-air-00) (artifact) | not-started |
| [AIR.08](#task-air-08) | Real-provider metering evidence and stubbed-path removal | integration | L | [AIR.00](#task-air-00) (artifact), [AIR.02](#task-air-02) (artifact), [AST.15](assistant.md#task-ast-15) (artifact) | not-started |
| [AIR.90](#task-air-90) | Verify owned artifact and real integration (AI routing and metering) | service | M | [AIR.08](#task-air-08) (artifact), [AIR.01](#task-air-01) (artifact), [AIR.03](#task-air-03) (artifact), [AIR.04](#task-air-04) (artifact), [AIR.05](#task-air-05) (artifact), [AIR.06](#task-air-06) (artifact), [AIR.07](#task-air-07) (artifact) | not-started |
| [AIR.09](#task-air-09) | Complete pinned tokenizer, rendering and model input producer | producer | L | [CON.10](contracts.md#task-con-10) (artifact), [CON.11](contracts.md#task-con-11) (artifact) | not-started |

## Tasks

<a id="task-air-00"></a>

### AIR.00 — Provider adapters and routing (Workers AI)

**Outcome.** env.AI.run adapters exist for default/fast text, accepted image context, bge-m3 embedding and bge-reranker-base rerank; model availability/frozen-config/request-limits/tool-stream-shapes are validated before dispatch; C# records admission/routing/supplier version while CF executes the already-admitted intent.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/air-00` and ledger record `ledger/tasks/air-00.md` in the Plan repository; task branch `task/air-00` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L · early risk proof |
| Obligations | [WP-43.00](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00) — full |
| Provides | workers-ai-adapter |
| Start prerequisites | **contract** [CON.10](contracts.md#task-con-10) — published internal AI HTTP profile (model-intent/model-outcome/dispatch ports) from internal/ai-http/v1/schema.json. *Why:* the adapter is called through this fixed internal contract, already scaffolded in Contracts (a CommitReceipt shape observed there)<br>**artifact** [POL.08](policy.md#task-pol-08) — active model/route policy snapshot naming the admitted catalogue subset. *Why:* [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06) requires policy to gate which models are activatable; routing cannot hardcode the catalogue |
| Entry condition | [ADOPT.08.ai-routing](adoption.md#task-adopt-08-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AIR.09](#task-air-09) — actual normal published exact tokenizer/render/materializer implementation. *Why:* Execute/count the same actual profile bytes and tokens.<br>**integration** [CON.36](contracts.md#task-con-36) — actual published safe descriptor/artifact/pin and private model evidence. *Why:* Use real generated transport and new explicit model-bound profiles.<br>**integration** [CLOUD.13](cloud.md#task-cloud-13) — actual current raw session/device/install and fixed descriptor materialization union. *Why:* Current read/dispatch and opaque owner composition use real authority.<br>**integration** [CLOUD.75](cloud.md#task-cloud-75) — actual privileged configured realm/recovery guard. *Why:* Materialization/current source cannot invent realm/generation.<br>**integration** [CLOUD.21](cloud.md#task-cloud-21) — actual production signed executor/private bridge. *Why:* No proof-only executor/key policy or successful unavailable transport.<br>**integration** [CLOUD.82](cloud.md#task-cloud-82) — actual opaque same issuer/plan/scope family capabilities. *Why:* Module owners cannot author foreign SQL or caller permission. |
| Unblocks | [AIR.02](#task-air-02), [AIR.03](#task-air-03), [AIR.05](#task-air-05), [AIR.07](#task-air-07), [AIR.08](#task-air-08), [CLOUD.67](cloud.md#task-cloud-67), [HAR.00](harness.md#task-har-00), [HAR.05](harness.md#task-har-05), [SRCH.06](search.md#task-srch-06) |
| Write scope | `AI:src/providers/workers-ai/**`<br>`AI:src/inference/**`<br>`AI:src/providers/workers-ai/** and src/inference/** (actual pinned raw=true GPT-OSS adapter executing the exact counted prompt/hash; preserve other original routing and acceptance obligations)`<br>`AI:tests/model-input/** (actual generated private evidence/current route/raw prompt bytes, literal delimiters/unsupported arm/cancel/unknown dispatch components; no real inference in ordinaryCI)`<br>`AI:src/model-input/** (only exact generated evidence/descriptor/rendered object slice materialization and full hash/owner/run/config crossbinding; no shadow tokenizer or heuristic count)`<br>`AI:package.json and package-lock.json (only actual published CON36 mandatory proto closure and exact owned test registration; no toolchain/third-party changes)`<br>`AI:eng/dependency-policy.* and eng/dependency-reviews/air-00-*.json and eng/provenance/** (only actual owned generated consumer/evaluated input/legal successors)`<br>`Cloud:src/ArcForges.Cloud.Modules.Agent/ModelContext/** and AgentModule.cs (actual immutable existing descriptor projection/current bound source, public artifact read service and real owner factory)`<br>`Cloud:src/ArcForges.Cloud.Modules.Abstractions/Agent/ModelContextPort.cs (required actual generated model context/current read/materialization owner ports; no Desktop Assistant types)`<br>`Cloud:storage/plans/agent/model-context-*.sql (only actual existing descriptor row/current/lifecycle/immutable insert guards and read plans)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Physical/manifest/agent.json and Migrations/pending/agent__model-context-invariants.sql (only existing agent_model_descriptor closed original insertion/update/delete profile; preserve baseline0010 and price/tariff tables)`<br>`Cloud:eng/verification/physical-schema.ts and tests/worker/d1-physical-schema.test.ts (only fixed agentModelDescriptorOriginal exact PK/config-model-purpose conflicts/immutable originals/newactive-retired lifecycle; no arbitrary SQL or shape waiver)`<br>`Cloud:src/ArcForges.Cloud/Composition/ModelContextModule.cs and HostModules.cs (exact real Agent/Config/ModelInput factory registration; no module-private implementation import)`<br>`Cloud:src/ArcForges.Cloud/PublicApi/Agent/** (only genuine generated ModelView7 and AgentService.ReadModelArtifact ingress with current raw C13/personal Workspace and strict complete shape/slice validation)`<br>`Cloud:src/ArcForges.Cloud.Modules.Task/ModelInput/** and Modules.Chat/ModelInput/** (each owner actual immutable run input binding/guarded preparation/replay only; no crossmodule SQL)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Physical/manifest/task.json and chat.json and Migrations/pending/task__model-input-binding.sql and chat__model-input-binding.sql (only genuine each-owner run input sidecar with actual run FK/immutable descriptor-config-pin-render binding; no baseline edits or synthesized run ConfigVersion)`<br>`Cloud:storage/plans/task/model-input-*.sql and chat/model-input-*.sql (only each owner immutable run binding insert/read/current guards)`<br>`Cloud:worker/model-input/** (fixed protected encrypted render object parts/hash/owner/run/config bridge under unchanged private envelope; no workflow/log plaintext)`<br>`Cloud:tests/ArcForges.Cloud.Tests/Agent/ModelContext/** and ModelInput/** and tests/worker/model-input*.test.ts (actual original descriptor/run sidecar replacement, current authority/pin/cap/buffer/cancel/unknown and exact provider bytes components)`<br>`Cloud:Directory.Packages.props and exact owned Agent/host/tests csproj/packages.lock.json (only actual published ArcForges.AI.ModelInput and CON36 mandatory peer closure; no unrelated upgrade)`<br>`Cloud:eng/provenance/files.json and policy/dependency-policy.json and dependency-reviews/air-00-*.json and tests/ArchitectureTests/EvaluatedRepositoryGate.cs (only actual owned source/consumer/API inputs and immutable reviewed successor)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Physical/PhysicalSchema.g.cs and PlanManifest.g.cs and worker/storage/plans.generated.ts (regenerate only actual admitted own source)`<br>`Cloud:tests/worker/support/physical-rows.ts and tests/ArcForges.Cloud.Tests/Physical/PhysicalSchemaTests.cs (only legitimate correlated own descriptor/run binding fixtures and actual accepted-prefix table count; all constraints/search cap/negatives preserved)`<br>`Cloud:eng/verification/physical-schema.ts (only fixed modelRunInputOriginal exact task_model_input_binding/chat_model_input_binding PK/ref insertion and immutable/delete invariants; preserve all other table profiles)` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (exclusive), [RES-private-configuration](../shared-resources.md#res-private-configuration) (append) |
| Validation | Actual selected model/capability-shape tests, withdrawn/unknown/unsupported request tests, request-size/output-bound tests, version-mismatch tests. Real CF calls only in the credentialed candidate gate, not ordinary CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): no real AI inference in CI). |
| Completion evidence | Routing decision, explainability and streaming results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: AI repo is Hello-World stage (src/deployment.ts, hello.ts, index.ts, model.ts, model-diagnostics.ts only); no workflows/, providers/, inference/, streams/, or mcp/ trees exist. tests/workflow.test.ts and docs/evidence/workflow-*.json are early probe scaffolding, not the implementation. |
| Notes | Narrow early risk proof: if env.AI.run cannot actually deliver the required capability shapes (tool/stream) as specified, the whole AI economics/product model is affected.  2026-10-07 approved model context and exact rendering producer repair (docs/decisions/approved-model-context-and-exact-rendering-producer-2026-10-07.md). Runtime coordinates the actual Agent-owned existing descriptor and Task/Chat-owned immutable run input witnesses, current Config source and exact raw provider dispatch. Each module retains own SQL and opaque capability. Counted GPT-OSS raw routes require exact current complete modelInputEvidence and immutable rendered object bytes/hash; unsupported templates/arms refuse before admission/debit, no hidden messages framing. Original all-route/image/embedding/rerank and actual provider acceptance remain. Fixed model-descriptor-materialization.commit-current joins genuine Agent record/Config approved current predicate/Platform75 under C13 sole union. No pure count/signed descriptor grants user permission. |

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
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Agent/Tariffs/**` |
| Shared resources | [RES-private-configuration](../shared-resources.md#res-private-configuration) (append), [RES-cloud-policy-inputs](../shared-resources.md#res-cloud-policy-inputs) (append) |
| Validation | Rate-change immutability test, historical-explainability reconstruction test, per-dimension metering tests -- offline. |
| Completion evidence | Rate-change immutability and historical explainability results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

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
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Agent/Metering/**` |
| Shared resources | [RES-cloud-policy-inputs](../shared-resources.md#res-cloud-policy-inputs) (append) |
| Validation | Actual CF normal/interrupted/lost outcome with concurrent duplicates and replayed receipts; cancelled/unknown hold sweep; tariff-change and operator-job isolation tests. Real-CF cases only at the credentialed candidate gate. |
| Completion evidence | Metering accounting, idempotency, sweep and overdraft results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

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
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Agent/Routing/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append), [RES-private-configuration](../shared-resources.md#res-private-configuration) (append), [RES-cloud-policy-inputs](../shared-resources.md#res-cloud-policy-inputs) (append) |
| Validation | Unavailable/withdrawn model, missing price/config, pre-dispatch-refusal-vs-unknown-dispatch, explicit-new-model-request tests -- offline. |
| Completion evidence | No-BYOK structural assertions and credential-custody results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

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
| Unblocks | [AIR.90](#task-air-90) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Agent/InteractionRecords/**` |
| Shared resources | [RES-cloud-policy-inputs](../shared-resources.md#res-cloud-policy-inputs) (append) |
| Validation | Trace-separation test; content-redaction test; cost-explainability test -- offline. |
| Completion evidence | Trace separation, redaction and cost explainability results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |
| Notes | Planning repair 2026-10-05: every provider interaction record carries the call's correlation identity and the provider request identifier ([CR-05](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cr-05)) through the CLOUD.69 seam; this is part of this task's own acceptance and of the real provider hop that PLT.48's correlation scenario names as a later owner (no new write scope). |

<a id="task-air-05"></a>

### AIR.05 — Content-origin marking at the provider generation boundary

**Outcome.** The frozen content-origin profile is implemented at the point AI-generated content is produced; every artifact type carries the required transparency marking; malformed/hash-mismatched marks and marking retry are handled; this satisfies [VG-01](../../../assurance/open-gates-register.md#rule-vg-01) once the regime determination is recorded.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/air-05` and ledger record `ledger/tasks/air-05.md` in the Plan repository; task branch `task/air-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-43.04](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.04) — transparency marking mechanism at the provider generation boundary; marking-coverage per artifact type |
| Provides | ai-content-origin-marking |
| Start prerequisites | **artifact** [AIR.00](#task-air-00) — generated model output to mark. *Why:* marking attaches to the adapter's own output boundary |
| Entry condition | [ADOPT.08.ai-routing](adoption.md#task-adopt-08-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90), [HAR.03](harness.md#task-har-03) |
| Write scope | `AI:src/providers/workers-ai/ContentOrigin/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append) |
| Validation | Real provider text through durable output and downstream carrier fixtures; deterministic/non-AI and legacy controls; malformed/hash-mismatched mark; marking retry -- offline against fixture carriers, real text only at the AIR.08 credentialed gate. |
| Completion evidence | Marking-coverage results per artifact type; carrier/propagation/failure vectors with payload and manifest hashes. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: AI repo is Hello-World stage (src/deployment.ts, hello.ts, index.ts, model.ts, model-diagnostics.ts only); no workflows/, providers/, inference/, streams/, or mcp/ trees exist. tests/workflow.test.ts and docs/evidence/workflow-*.json are early probe scaffolding, not the implementation. |
| Notes | HAR.03 ([WP-52.03](../../work-packages/52-cloud-harness.md#rule-wp-52.03) durable output) consumes this task's ContentOrigin carrier as a start artifact -- internal the AI lanes cross-reference. |

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
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Agent/Metering/UncertainOutcome/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append), [RES-cloud-policy-inputs](../shared-resources.md#res-cloud-policy-inputs) (append) |
| Validation | Search-without-customer-debit, model-debit-once, crash-before/after-dispatch, unknown-deadline, late-usage-after-closed, no-automatic-retry tests -- offline with real-CF-shaped fixtures; real dispatch only at AIR.08's gate. |
| Completion evidence | Degradation, reservation-release and alert results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |
| Notes | HAR.04 ([WP-52.04](../../work-packages/52-cloud-harness.md#rule-wp-52.04) general effect-certainty classification) treats this task's ledger pattern as its worked precedent -- internal the AI lanes cross-reference. |

<a id="task-air-07"></a>

### AIR.07 — Provider test-environment coverage

**Outcome.** Every provider integration is exercised against the provider's own test environment, with its contract shape frozen as recorded fixtures so ordinary CI never depends on provider availability.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/air-07` and ledger record `ledger/tasks/air-07.md` in the Plan repository; task branch `task/air-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-43.06](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.06) — full |
| Provides | ai-provider-test-env-coverage |
| Start prerequisites | **artifact** [AIR.00](#task-air-00) — the adapter to exercise against the test environment. *Why:* nothing to record fixtures from before the adapter exists |
| Entry condition | [ADOPT.08.ai-routing](adoption.md#task-adopt-08-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90) |
| Write scope | `AI:tests/provider-fixtures/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append) |
| Validation | Per-provider test-environment run (credentialed, not ordinary CI); fixture-driven CI run with the provider deliberately unreachable, per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Per-provider test-environment runs and fixture-driven CI results -- [PG-10](../../../assurance/open-gates-register.md#rule-pg-10). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: AI repo is Hello-World stage (src/deployment.ts, hello.ts, index.ts, model.ts, model-diagnostics.ts only); no workflows/, providers/, inference/, streams/, or mcp/ trees exist. tests/workflow.test.ts and docs/evidence/workflow-*.json are early probe scaffolding, not the implementation. |

<a id="task-air-08"></a>

### AIR.08 — Real-provider metering evidence and stubbed-path removal

**Outcome.** Actual Workers AI responses for each selected capability are recorded and normalized into independent sanitized fixtures; deterministic fixtures run on ordinary CI while the credentialed real-CF candidate gate proves exact Worker/model/config identity; the [WP-17.05](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.05) stubbed managed provider path is retired.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/air-08` and ledger record `ledger/tasks/air-08.md` in the Plan repository; task branch `task/air-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / L |
| Obligations | [WP-43.07](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07) — full |
| Provides | ai-real-provider-evidence |
| Start prerequisites | **artifact** [AIR.00](#task-air-00) — the real adapter to record responses from. *Why:* nothing to normalize without the real adapter<br>**artifact** [AIR.02](#task-air-02) — the real settlement engine to reconcile the recorded evidence through. *Why:* [PG-13](../../../assurance/open-gates-register.md#rule-pg-13) requires 'one real provider usage response + one real payment-provider event reconciled through same code as fixtures'<br>**artifact** [AST.15](assistant.md#task-ast-15) — assistant admission path that carried the stubbed provider. *Why:* the stubbed path is removed from the consumer that introduced it |
| Entry condition | [ADOPT.08.ai-routing](adoption.md#task-adopt-08-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.90](#task-air-90) |
| Permitted substitutes | [SUB-stubbed-provider-path](../substitutes.md#sub-stubbed-provider-path) |
| Write scope | `AI:tests/provider-fixtures/**`<br>`Cloud:tests/Cloud.Tests.Integration/AiMetering/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append) |
| Validation | Model response drift, missing category, cumulative stream, embedding/rerank result validation tests offline; controlled real-provider run at the credentialed candidate gate only. |
| Completion evidence | Real-provider normalisation, settlement and worked-fixture results -- [PG-13](../../../assurance/open-gates-register.md#rule-pg-13). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: AI repo is Hello-World stage (src/deployment.ts, hello.ts, index.ts, model.ts, model-diagnostics.ts only); no workflows/, providers/, inference/, streams/, or mcp/ trees exist. tests/workflow.test.ts and docs/evidence/workflow-*.json are early probe scaffolding, not the implementation. |
| Notes | This task is the structural replacement named in implementation-sequence.md Sec.3.1: 'Stubbed managed provider path ([WP-17.05](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.05))... Deleted by [WP-43.00](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00), [WP-43.07](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07)' -- AIR.00 builds the real path, AIR.08 proves and removes the stub. |

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
| Shared resources | [RES-cloud-policy-inputs](../shared-resources.md#res-cloud-policy-inputs) (append) |
| Validation | Real selected model/tool/embedding cases and provider refusal/lost-result/usage reconciliation tied to C# admitted call and config identity; [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) proportionate. |
| Completion evidence | Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/provider, scenario, result, real-vs-fixture status. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |
| Notes | Also carries the [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) package closure text (real ExecutionOwner task/turn + operator-funded compaction/search support; durable receipts vs temporary bodies kept outside D1/SQLite history, backups and Workflow checkpoints). |

<a id="task-air-09"></a>

### AIR.09 — Complete pinned tokenizer, rendering and model input producer

**Outcome.** Normally publish ArcForges.AI.ModelInput complete pure supported o200k/Harmony tokenizer/render/materializer and semantic bundle validator with exact actual verified artifacts, immutable generated descriptor/pin inputs, original-source spans/token IDs/costs and faithful bounded rendered provider bytes. No approximate count, constructor permission, default unknown template or whole configuration/harness cycle.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/air-09` and ledger record `ledger/tasks/air-09.md` in the Plan repository; task branch `task/air-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-43.00](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00) — minimum actual independent model tokenizer/render/materializer producer; original AIR00 routing/provider acceptance retained |
| Provides | model-input-pkg; pinned-model-tokenizer; exact-model-render-count; model-bundle-semantic-validator |
| Start prerequisites | **artifact** [CON.10](contracts.md#task-con-10) — actual published complete content/profile/skill/tool records. *Why:* Pure captured inputs use real generated typed records, not authored wire.<br>**artifact** [CON.11](contracts.md#task-con-11) — actual published transcript/source/turn input records. *Why:* Original IDs/ordinals/tool-pair source is genuine typed lineage. |
| Entry condition | [ADOPT.08.ai-routing](adoption.md#task-adopt-08-ai-routing) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CON.36](contracts.md#task-con-36) — actual normal published descriptor/bundle/pin and model-bound helper source. *Why:* Final package compiles/tests exact generated new types and preserves legacy helper vectors. |
| Unblocks | [AIR.00](#task-air-00), [AST.01](assistant.md#task-ast-01), [HAR.01](harness.md#task-har-01), [POL.02](policy.md#task-pol-02) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.AI.ModelInput/** (new real pure engine/materializer/validator/captured operational inputs/API/README/project/lock; no Cloud or Desktop Assistant reference)`<br>`DesktopPlatform:tests/ModelInputTests/** (new genuine independent official tokenizer token-ID/render-byte/count/classifier/span/material/limit/cancel/disposal and unsupported-arm components)`<br>`DesktopPlatform:eng/model-input/** and fixtures/model-input/** (owned exact pinned source/UCD data legal/provenance acquisition recipe and independently authored official tokenizer goldens; no production self-test authority)`<br>`DesktopPlatform:DesktopPlatform.slnx (append only actual ModelInput and owning component test projects)`<br>`DesktopPlatform:Directory.Packages.props and exact ModelInput/tests packages.lock.json (only actual published Foundation/CON36 Validation mandatory same-release peers and existing admitted test closure)`<br>`DesktopPlatform:eng/packaging/packages.json (only new real verified ArcForges.AI.ModelInput managed package/dependencies/legal assets)`<br>`DesktopPlatform:eng/policy/architecture-projects.json and licence-boundary.json (only actual owned producer/test classification)`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json and architecture-evidence.json (only actual owned API/direct behavior evidence mappings)`<br>`DesktopPlatform:eng/policy/reconciliation/active-projects.json and project-updates.json (only actual owned new project blobs and immutable input successors)`<br>`DesktopPlatform:eng/policy/dependency-policy.json and dependency-reviews/air-09-*.json and eng/provenance/** and NOTICE.md (only actual owned producer/data/legal/evaluated input immutable successors)`<br>`DesktopPlatform:.github/workflows/pr-gate.yml and package-validation.yml (only actual owned ordinary component/producer registration, preserve all existing triggers/gates/toolchain)`<br>`DesktopPlatform:docs/model-input-producer.md (actual artifact/classifier/BPE/render/API/profile/bounds/legal and consumer obligations)` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-contract-consumer-pins](../shared-resources.md#res-contract-consumer-pins) (append) |
| Validation | Independently pinned official token IDs/counts/UTF8 rendering and complete Unicode17 scalar tables, all actual artifact hashes/category/pattern/BPE ties/span provenance, signed0 semantic legacy invariance, literal Harmony delimiters/control/astral/U2028/unpaired input, actual tool/context/resource unsupported arms, finite work/admission/cancellation/ignored callback/shutdown/key-buffer disposal. No live provider in ordinary CI; real consumer/provider acceptance remains original AIR00/HAR01/AST ownership. |
| Completion evidence | Exact independently reviewed source/data/legal/input identities, actual direct components and applicable Windows/Linux CI, real normal managed package publication and safe captured API. Pure success is not Config readiness, current permission or provider acceptance. |
| Baseline (unreviewed unless accepted) | not-started Actual AI/Cloud/Desktop source audit found no tokenizer/materializer engine; ModelView lacks approved config/artifact/framing identity. |
| Notes | 2026-10-07 approved model context and exact rendering producer repair (docs/decisions/approved-model-context-and-exact-rendering-producer-2026-10-07.md). Runtime worker w-codex-20261006-runtime owns the real pure producer. Independent package output allows Config Stage and client/server adapters to join without whole-task completion cycle; all consumer current authority and actual acceptance remain separate. |
