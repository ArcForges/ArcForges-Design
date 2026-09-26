# Cloud Harness — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

The sole Cloudflare Workflow Harness: admission, context, tools and approvals, outputs, automation and reconciliation.

Tasks: 9 · Owning repositories: AI, Cloud · Integration owner(s): AI integration owner, Cloud integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [HAR.00](#task-har-00) | Turn loop, tool batching and bounds (RunWorkflow core) | service | XL | [CLOUD.01](cloud.md#task-cloud-01) (artifact), [CON.15](contracts.md#task-con-15) (contract), [CON.10](contracts.md#task-con-10) (contract), [CLOUD.05](cloud.md#task-cloud-05) (artifact) | not-started |
| [HAR.01](#task-har-01) | Context assembly and compaction | service | L | [HAR.00](#task-har-00) (artifact), [CON.11](contracts.md#task-con-11) (contract) | not-started |
| [HAR.02](#task-har-02) | Approval, cancellation and crash recovery | service | L | [HAR.00](#task-har-00) (artifact), [CON.10](contracts.md#task-con-10) (contract) | not-started |
| [HAR.03](#task-har-03) | Generated streaming and durable output | service | L | [HAR.00](#task-har-00) (artifact), [AIR.05](ai-routing.md#task-air-05) (artifact) | not-started |
| [HAR.04](#task-har-04) | Provider failure and effect-certainty classification | service | M | [HAR.00](#task-har-00) (artifact), [AIR.06](ai-routing.md#task-air-06) (contract) | not-started |
| [HAR.05](#task-har-05) | Own-application execution proof and fixture turn-endpoint removal | integration | XL | [HAR.00](#task-har-00) (artifact), [HAR.01](#task-har-01) (artifact), [HAR.02](#task-har-02) (artifact), [HAR.03](#task-har-03) (artifact), [HAR.04](#task-har-04) (artifact), [AST.11](assistant.md#task-ast-11) (artifact), [DEV.08](device-bridge.md#task-dev-08) (artifact), [AST.19](assistant.md#task-ast-19) (artifact), [DEV.13](device-bridge.md#task-dev-13) (artifact), [AND.24](android.md#task-and-24) (artifact), [WEB.27](web.md#task-web-27) (artifact), [AIR.00](ai-routing.md#task-air-00) (artifact), [NOTES.12](arcnotes.md#task-notes-12) (artifact), [APP.03](app-composition.md#task-app-03) (artifact) | not-started |
| [HAR.06](#task-har-06) | Durable Cloud automation, scheduling and automation-fixture removal | service | L | [HAR.00](#task-har-00) (artifact), [HAR.04](#task-har-04) (artifact), [COM.05](commerce.md#task-com-05) (artifact) | not-started |
| [HAR.90](#task-har-90) | Verify owned artifact and real integration (Harness) | service | M | [HAR.05](#task-har-05) (artifact), [HAR.06](#task-har-06) (artifact), [HAR.91](#task-har-91) (artifact) | not-started |
| [HAR.91](#task-har-91) | Paid Slate transcription end-to-end adoption | integration | M | [HAR.06](#task-har-06) (artifact), [AIR.09](ai-routing.md#task-air-09) (artifact), [SLATE.30](arcslate.md#task-slate-30) (artifact), [AIR.08](ai-routing.md#task-air-08) (artifact) | not-started |

## Tasks

<a id="task-har-00"></a>

### HAR.00 — Turn loop, tool batching and bounds (RunWorkflow core)

**Outcome.** The sole RunWorkflow implements deterministic Workflow identity with C# claim/epoch/generation and actual deployed Worker version; iteration/context references and model/tool dispatch intent persist before effects; immutable outcome receipts persist before continuation; model/tool/parallel/progress/time/step budgets and declared conflict sets are enforced, with a 60-second execution lease renewed every 20 seconds during long awaits.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/har-00` and ledger record `ledger/tasks/har-00.md` in the Plan repository; task branch `task/har-00` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / XL · early risk proof |
| Obligations | [WP-52.00](../../work-packages/52-cloud-harness.md#rule-wp-52.00) — full |
| Provides | turn-loop-core |
| Start prerequisites | **artifact** [CLOUD.01](cloud.md#task-cloud-01) — the single Cloud host and its lease-fenced hosted services. *Why:* claim/epoch/generation fencing is built on [WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21)'s real lease primitive; a substitute lease mechanism would invalidate the exact-once dispatch guarantee this task exists to prove<br>**contract** [CON.15](contracts.md#task-con-15) — the generated internal AI HTTP port surface (claim/renew/reconcile/dispatch/control). *Why:* the Workflow calls these as generated contracts, not ad hoc HTTP<br>**contract** [CON.10](contracts.md#task-con-10) — published ToolRequest and StructuredValue records in the task/agent closure. *Why:* tool-declaration filtering and dispatch intent must be typed against the same dual-capability-boundary model extensions use<br>**artifact** [CLOUD.05](cloud.md#task-cloud-05) — lease-fenced finite durable jobs (Cron/Queue/Workflow wake) in the Cloud host. *Why:* the Harness hands lease-fenced work to the single C# host; the durable-job mechanism must exist to claim and renew it |
| Entry condition | [ADOPT.08.harness](adoption.md#task-adopt-08-harness) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AIR.00](ai-routing.md#task-air-00) — a dispatchable model/tool call target. *Why:* the loop has nothing to dispatch without a provider adapter; see SUB-provider-response-fixture for the early substitute |
| Unblocks | [AND.24](android.md#task-and-24), [AST.19](assistant.md#task-ast-19), [CLOUD.67](cloud.md#task-cloud-67), [HAR.01](#task-har-01), [HAR.02](#task-har-02), [HAR.03](#task-har-03), [HAR.04](#task-har-04), [HAR.05](#task-har-05), [HAR.06](#task-har-06), [WEB.27](web.md#task-web-27) |
| Permitted substitutes | [SUB-provider-response-fixture](../substitutes.md#sub-provider-response-fixture), [SUB-same-app-fixture-tool](../substitutes.md#sub-same-app-fixture-tool) |
| Write scope | `AI:src/workflows/RunWorkflow.ts`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Task/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append), [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Real Workflow with forced duplicate start, replay, 120-second model await, lease loss/stale outcome, no-progress and every bound test; no automatic effect retry after intent. CF Workflow deployment tests apply to the loop per [BR-02](../../../architecture/14-build-packaging-and-release.md#rule-br-02); C# integration ports retain the AOT gate. Real CF only at the credentialed candidate gate, not ordinary CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Loop-bound, crash-resume, no-progress and conflict-batching results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: AI repo has no src/workflows tree; tests/workflow.test.ts and docs/evidence/workflow-*.json exist as early probe/evidence scaffolding only (WP-03-level), not the RunWorkflow implementation. |
| Notes | Foundational early risk proof: if the CF Workflow model cannot actually sustain the durable claim/epoch/generation + budget semantics at the required step-guard ceiling (24000 steps, 25000 hard ceiling per contracts/05-cloudflare-integration.md), the entire single-Harness architecture is affected. |

<a id="task-har-01"></a>

### HAR.01 — Context assembly and compaction

**Outcome.** Context assembles through authorized C# ports in a fixed order, pages under one snapshot hash, and retains immutable source pins/content origins; invocable capabilities are filtered before model declaration with budget truncation disclosed; compaction refs are stored derived; source/revision and active grant are revalidated before mutation.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/har-01` and ledger record `ledger/tasks/har-01.md` in the Plan repository; task branch `task/har-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-52.01](../../work-packages/52-cloud-harness.md#rule-wp-52.01) — full |
| Provides | context-assembly-compaction |
| Start prerequisites | **artifact** [HAR.00](#task-har-00) — the turn-loop skeleton to assemble context inside. *Why:* context assembly is a step inside HAR.00's orchestration<br>**contract** [CON.11](contracts.md#task-con-11) — typed TranscriptWindow/CompactionRecord records (model 05). *Why:* [WP-52.01](../../work-packages/52-cloud-harness.md#rule-wp-52.01)'s testing requirement runs model-05 context vectors through these exact typed inputs |
| Entry condition | [ADOPT.08.harness](adoption.md#task-adopt-08-harness) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [SRCH.00](search.md#task-srch-00) — a retrieval/context source to pull from (fixture-backed lexical-only path is sufficient at start). *Why:* context assembly must have something real to page through; SRCH's D1 FTS lexical path (no AIR dependency) can serve here before SRCH.06's real semantic path lands |
| Unblocks | [HAR.05](#task-har-05) |
| Write scope | `AI:src/workflows/context.ts`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Task/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append) |
| Validation | Large-context paging, permission loss, stale source, prior-compaction-version, unsupported-capability tests; no raw prompts in Workflow checkpoints; all four model-05 context vectors (under budget, compaction, protected overflow, changed branch) plus wrong role/tool-pair, hash and origin-installation negatives; [HC-09](../../../architecture/17-agent-harness.md#rule-hc-09) refusal and no-customer-debit-for-compaction assertions; both inline and transient-object input. |
| Completion evidence | Context permission, staleness and compaction results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: AI repo is Hello-World stage (src/deployment.ts, hello.ts, index.ts, model.ts, model-diagnostics.ts only); no workflows/, providers/, inference/, streams/, or mcp/ trees exist. tests/workflow.test.ts and docs/evidence/workflow-*.json are early probe scaffolding, not the implementation. |

<a id="task-har-02"></a>

### HAR.02 — Approval, cancellation and crash recovery

**Outcome.** Approval waiting is bounded (selected wait/reconcile steps, seven-day bound) with reauthorization on resume; explicit cancel/pause/steer controls and C# reconciliation exist; wait/cancel/recovery always yields one canonical outcome or an explicit unknownEffect via the intent-to-owner/provider-evidence-to-deadline-to-user-decision ladder; a UI session closing never cancels a durable Task.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/har-02` and ledger record `ledger/tasks/har-02.md` in the Plan repository; task branch `task/har-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-52.02](../../work-packages/52-cloud-harness.md#rule-wp-52.02) — full |
| Provides | approval-cancel-recovery |
| Start prerequisites | **artifact** [HAR.00](#task-har-00) — the turn-loop skeleton to interleave approval into. *Why:* approval waiting is a suspend/resume state of the same loop<br>**contract** [CON.10](contracts.md#task-con-10) — published internal admission and commit-before-dispatch port schema. *Why:* the Harness calls the admission port through the generated internal contract; the real capacity bucket joins at completion |
| Entry condition | [ADOPT.08.harness](adoption.md#task-adopt-08-harness) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [COM.12](commerce.md#task-com-12) — the real admission/commit-before-dispatch port. *Why:* [BR-04](../../../architecture/14-build-packaging-and-release.md#rule-br-04) ('admission commits before dispatch') governs the same transaction boundary approval reconciliation must respect |
| Unblocks | [CLOUD.67](cloud.md#task-cloud-67), [DEV.13](device-bridge.md#task-dev-13), [HAR.05](#task-har-05) |
| Write scope | `AI:src/workflows/approval.ts`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Task/Approvals/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append), [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Restart Workflow/Cloud during wait/model/tool, missed wake event, expired/stale proposal, cancel race, generation rotation, late evidence tests. |
| Completion evidence | Approval-across-restart, cancellation and uncertain-effect results ([PG-18](../../../assurance/open-gates-register.md#rule-pg-18), joint with HAR.04). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: AI repo is Hello-World stage (src/deployment.ts, hello.ts, index.ts, model.ts, model-diagnostics.ts only); no workflows/, providers/, inference/, streams/, or mcp/ trees exist. tests/workflow.test.ts and docs/evidence/workflow-*.json are early probe scaffolding, not the implementation. |

<a id="task-har-03"></a>

### HAR.03 — Generated streaming and durable output

**Outcome.** execution.readOutput/watchOutput, transient-turn admission/ack/purge and DO projections work per annex 10/model 05; Cloud histories commit canonically while local histories recover verified transient output without a Cloud Chat body; a stream projection never becomes message authority or determines Task state.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/har-03` and ledger record `ledger/tasks/har-03.md` in the Plan repository; task branch `task/har-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-52.03](../../work-packages/52-cloud-harness.md#rule-wp-52.03) — full<br>[WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) Sec.8 gate item 9: every surface converges to the same authoritative final answer/artifact with realtime disabled — package-level obligation contribution |
| Provides | streaming-durable-output |
| Start prerequisites | **artifact** [HAR.00](#task-har-00) — the turn-loop skeleton producing output to stream. *Why:* nothing to stream before the loop emits output<br>**artifact** [AIR.05](ai-routing.md#task-air-05) — the ContentOrigin marking at the provider generation boundary. *Why:* durable output carrier propagation must carry the marks AIR.05 attaches at generation; internal the AI lanes dependency |
| Entry condition | [ADOPT.08.harness](adoption.md#task-adopt-08-harness) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AST.15](assistant.md#task-ast-15) — local history recovery of transient output on the client bridge. *Why:* the completion evidence requires local/temporary output to 'survive reconnect within its declared retention' on the real client, owned by the assistant lanes [WP-17](../../work-packages/17-arcchat-independent-core.md#rule-wp-17) |
| Unblocks | [AND.24](android.md#task-and-24), [AST.19](assistant.md#task-ast-19), [CLOUD.67](cloud.md#task-cloud-67), [HAR.05](#task-har-05), [WEB.27](web.md#task-web-27) |
| Write scope | `AI:src/streams/RunStream.ts` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append) |
| Validation | Scope/permission, wrong/stale target, loss/retry, expiry and applicable native UI cases; cross-replica read, miss-is-not-eviction, takeover, realtime-disabled equivalence, buffer-lifecycle tests; the same four model-05 context vectors and [HC-09](../../../architecture/17-agent-harness.md#rule-hc-09)/no-debit assertions as HAR.01 (shared testing-requirement text in the WP). |
| Completion evidence | Cross-replica read, miss-is-not-eviction, takeover, realtime-disabled equivalence and buffer-lifecycle results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: AI repo is Hello-World stage (src/deployment.ts, hello.ts, index.ts, model.ts, model-diagnostics.ts only); no workflows/, providers/, inference/, streams/, or mcp/ trees exist. tests/workflow.test.ts and docs/evidence/workflow-*.json are early probe scaffolding, not the implementation. |

<a id="task-har-04"></a>

### HAR.04 — Provider failure and effect-certainty classification

**Outcome.** Failure classification keys on whether dispatch occurred, never on whether bytes returned; the unknown path releases customer holds at the reconciliation deadline while retaining supplier liability; no failure path silently resolves unknown to didNotHappen, and no dispatched request is retried automatically.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/har-04` and ledger record `ledger/tasks/har-04.md` in the Plan repository; task branch `task/har-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-52.04](../../work-packages/52-cloud-harness.md#rule-wp-52.04) — full |
| Provides | effect-certainty-classification |
| Start prerequisites | **artifact** [HAR.00](#task-har-00) — dispatch-intent records to classify. *Why:* classification operates on HAR.00's persisted dispatch intents<br>**contract** [AIR.06](ai-routing.md#task-air-06) — the worked AI-provider uncertain-outcome/deadline-release pattern. *Why:* [WP-52.04](../../work-packages/52-cloud-harness.md#rule-wp-52.04) generalizes dispatch-intent-based classification to all capabilities (tools, MCP, automation) and should reuse rather than re-derive the pattern AIR.06 already proved for AI-provider dispatch specifically -- internal the AI lanes dependency |
| Entry condition | [ADOPT.07.harness](adoption.md#task-adopt-07-harness) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [HAR.05](#task-har-05), [HAR.06](#task-har-06), [OPS.03](operations.md#task-ops-03) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Task/EffectCertainty/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append), [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Timeout-before-first-token asserting unknown-not-retry; lost response reconciled against the provider's own record; platform-caused retry charged once and fully visible in supplier cost; deadline-expiry releasing customer hold while retaining supplier liability. |
| Completion evidence | Effect-certainty classification and deadline-release results ([PG-18](../../../assurance/open-gates-register.md#rule-pg-18), joint with HAR.02). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

<a id="task-har-05"></a>

### HAR.05 — Own-application execution proof and fixture turn-endpoint removal

**Outcome.** Two end-to-end oracles pass: the ArcNotes embedded assistant processes its own selected document plus local/cloud history, and Android/Web explicitly target an authorized ArcNotes installation for an approved Notes command -- covering typed transcript/compaction, promotion/export, binary streams and offline recovery. The [WP-17.01](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.01) fixture turn endpoint is structurally proven absent from the codebase.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/har-05` and ledger record `ledger/tasks/har-05.md` in the Plan repository; task branch `task/har-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / XL |
| Obligations | [WP-52.05](../../work-packages/52-cloud-harness.md#rule-wp-52.05) — all work except the parts mapped to AST.19, DEV.13<br>[WP-52.90](../../work-packages/52-cloud-harness.md#rule-wp-52.90) — structural assertion that the [WP-17.01](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.01) fixture turn endpoint no longer exists (Sec.8 gate item 10) |
| Provides | own-app-execution-proof; fixture-turn-endpoint-removed |
| Start prerequisites | **artifact** [HAR.00](#task-har-00) — the complete real turn loop. *Why:* the oracles run the real loop end to end, not a fixture<br>**artifact** [HAR.01](#task-har-01) — real context assembly/compaction. *Why:* the oracle scenarios explicitly include typed transcript/compaction and protected-context overflow<br>**artifact** [HAR.02](#task-har-02) — real approval/crash recovery. *Why:* the oracle scenarios include app restart, revoke/epoch change<br>**artifact** [HAR.03](#task-har-03) — real streaming/durable output. *Why:* the oracle scenarios include binary streams, interrupted output/final hash, lost ack<br>**artifact** [HAR.04](#task-har-04) — real effect-certainty classification. *Why:* the oracle scenarios include forged tool history and failure variants reaching specified terminals<br>**artifact** [AST.11](assistant.md#task-ast-11) — the real device-side tool executor and desktop surfaces in an actual AOT release binary. *Why:* this is the must-be-real-early device tool path; the oracle is precisely where its reality is proven, retiring SUB-same-app-fixture-tool<br>**artifact** [DEV.08](device-bridge.md#task-dev-08) — the real one-application bridge. *Why:* the Android/Web oracle explicitly targets an authorized ArcNotes installation remotely through this bridge<br>**artifact** [AST.19](assistant.md#task-ast-19) — consumer switched from the fixture turn endpoint to the real Harness. *Why:* the fixture endpoint is deleted only after every consumer runs against the real Harness, so the deletion can be asserted structurally<br>**artifact** [DEV.13](device-bridge.md#task-dev-13) — consumer switched from the fixture turn endpoint to the real Harness. *Why:* the fixture endpoint is deleted only after every consumer runs against the real Harness, so the deletion can be asserted structurally<br>**artifact** [AND.24](android.md#task-and-24) — consumer switched from the fixture turn endpoint to the real Harness. *Why:* the fixture endpoint is deleted only after every consumer runs against the real Harness, so the deletion can be asserted structurally<br>**artifact** [WEB.27](web.md#task-web-27) — consumer switched from the fixture turn endpoint to the real Harness. *Why:* the fixture endpoint is deleted only after every consumer runs against the real Harness, so the deletion can be asserted structurally<br>**artifact** [AIR.00](ai-routing.md#task-air-00) — real Workers AI provider adapters. *Why:* the execution proof runs against real provider responses<br>**artifact** [NOTES.12](arcnotes.md#task-notes-12) — the real ArcNotes capability surface the approved Notes command invokes. *Why:* both oracles invoke a registered ArcNotes command on a real installation<br>**artifact** [APP.03](app-composition.md#task-app-03) — ArcNotes composed as a clean Native AOT package consumer. *Why:* the embedded oracle runs the real ArcNotes host with its own assistant |
| Entry condition | [ADOPT.08.harness](adoption.md#task-adopt-08-harness) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [HAR.90](#task-har-90) |
| Write scope | `AI:src/workflows/RunWorkflow.ts`<br>`AI:tests/Cloud.Tests.Integration/OwnApp/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append) |
| Validation | Protected-context overflow, stale summary/branch, large transient object, forged tool history, interrupted output/final hash, lost ack, app restart, revoke/epoch change, refused cross-product target -- real device/AOT binary tests run locally/affected-scope per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (no desktop GUI or device CI), not as a hosted CI job. |
| Completion evidence | Full same-application workflow with every failure variant; structural absence of the [WP-17.01](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.01) fixture turn endpoint. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: n/a |
| Notes | This is the task that performs implementation-sequence.md Sec.3.1's 'Fixture turn endpoint... No [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) substep or gate names an extension/MCP-sourced tool call as oracle evidence anywhere in the WP text; both named oracles are native Notes commands. |

<a id="task-har-06"></a>

### HAR.06 — Durable Cloud automation, scheduling and automation-fixture removal

**Outcome.** Automation definition/version, trigger schedule/event cursor, occurrence dedup and grant/budget snapshot live in C# Task-owned tables; bounded leased jobs dispatch the same RunWorkflow identity through the existing outbox; disabled/revoked automation stops future occurrences; the labelled [WP-17](../../work-packages/17-arcchat-independent-core.md#rule-wp-17) automation fixture is removed.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/har-06` and ledger record `ledger/tasks/har-06.md` in the Plan repository; task branch `task/har-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-52.06](../../work-packages/52-cloud-harness.md#rule-wp-52.06) — automation definition/version, trigger schedule/event cursor, occurrence dedup, grant/budget snapshot, bounded leased dispatch through the existing outbox, disable/revoke control, and removal of the labelled [WP-17](../../work-packages/17-arcchat-independent-core.md#rule-wp-17) automation fixture -- excluding the Slate transcription closure scenario<br>[WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) Final-review closure paragraph: paid Slate transcription end-to-end, CF purge inventory paging, seven-day wait guards, post-backup unsafe-effect quarantine, real active/waiting/unknown states for [WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) recovery — package-level obligation contribution |
| Provides | automation-scheduler; automation-fixture-removed |
| Start prerequisites | **artifact** [HAR.00](#task-har-00) — the RunWorkflow identity automation dispatches into. *Why:* automation triggers the same loop, it does not build a second one ([BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06) no agent teams/second loop)<br>**artifact** [HAR.04](#task-har-04) — effect-certainty classification for occurrence dispatch. *Why:* occurrence dispatch is itself a dispatch-intent subject to the same classification<br>**artifact** [COM.05](commerce.md#task-com-05) — service/grant expiry and budget snapshot ports. *Why:* [WP-52.06](../../work-packages/52-cloud-harness.md#rule-wp-52.06)'s testing requirement explicitly includes 'service/grant expiry' against real admission |
| Entry condition | [ADOPT.07.harness](adoption.md#task-adopt-07-harness) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AST.20](assistant.md#task-ast-20) — desktop assistant switched to the real automation scheduler. *Why:* automation fixtures are removed only after every consumer uses real occurrences<br>**integration** [AND.24](android.md#task-and-24) — Android companion switched to real automation occurrences. *Why:* automation fixtures are removed only after every consumer uses real occurrences |
| Unblocks | [AST.20](assistant.md#task-ast-20), [HAR.90](#task-har-90), [HAR.91](#task-har-91) |
| Permitted substitutes | [SUB-automation-fixture](../substitutes.md#sub-automation-fixture) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Task/Automation/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append), [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Duplicate schedule/event, catch-up/coalescing, service/grant expiry, disable-during-wait tests; actual CF occurrence/usage with one linked Task at the credentialed gate. |
| Completion evidence | Real automation scheduling, missed-run policy, occurrence deduplication, cancellation and fixture-removal results (core mechanics). |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |
| Notes | The Slate transcription closure scenario named in [WP-52.06](../../work-packages/52-cloud-harness.md#rule-wp-52.06)'s final-review paragraph is deliberately excluded from this task and modeled as IM.slate-transcription-adoption, since it needs [WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) real audio and this task's core scheduler mechanics do not. |

<a id="task-har-90"></a>

### HAR.90 — Verify owned artifact and real integration (Harness)

**Outcome.** The specified Worker/Workflow/DO roles are implemented and verified together; context, model/tool loop, approval, retries, cancel, streams and schedule execution run against real C# transactions/ports and selected Workers AI; the named [WP-17](../../work-packages/17-arcchat-independent-core.md#rule-wp-17) fixtures are confirmed removed; this package owns the first complete AI same-application workflow.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/har-90` and ledger record `ledger/tasks/har-90.md` in the Plan repository; task branch `task/har-90` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Package acceptance | Records the [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-52.90](../../work-packages/52-cloud-harness.md#rule-wp-52.90) — remaining aggregation/receipt beyond HAR.05's structural assertion<br>[WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure: ordinary persistent/temporary ChatTurn and AgentTask through the same RunWorkflow, pure-read vs promoted-effectful mode — package-level obligation contribution |
| Provides | harness-package-acceptance |
| Start prerequisites | **artifact** [HAR.05](#task-har-05) — own-application execution proof. *Why:* acceptance cannot close before the two oracles pass<br>**artifact** [HAR.06](#task-har-06) — real automation evidence. *Why:* acceptance aggregates automation evidence too<br>**artifact** [HAR.91](#task-har-91) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.08.harness](adoption.md#task-adopt-08-harness) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.06](release.md#task-rel-06) |
| Write scope | `AI:tests/Cloud.Tests.Integration/**` |
| Validation | Real C#/CF/R2/device integration; duplicate/lost-ack/approval/restart/stream-tail/terminal-commit cases; usage and provenance. One loop, one canonical business outcome, no unexplained provider retry. |
| Completion evidence | Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, real-vs-fixture status. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: n/a |
| Notes | Also carries the [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) package closure text (ordinary persistent/temporary ChatTurn and AgentTask through the same real RunWorkflow, pure-read vs promoted-effectful mode, transient source expiry/cleanup, platform-funded protected compaction). |

<a id="task-har-91"></a>

### HAR.91 — Paid Slate transcription end-to-end adoption

**Outcome.** Actual [WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) selected-audio upload through CF Whisper, normal C# metering/final artifact and explicit local subtitle adoption; partial/unknown outcome, cancellation, budget bound, origin and no-raw-video-upload; paged exact CF purge inventory, stale controls/late evidence, seven-day wait budget guards, post-backup unsafe-effect quarantine; real active/waiting/unknown states for [WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) recovery.

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai`; also touches ArcSlate |
| Claim, branch and ledger | `claims/har-91` and ledger record `ledger/tasks/har-91.md` in the Plan repository; task branch `task/har-91` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-52.06](../../work-packages/52-cloud-harness.md#rule-wp-52.06) — the Slate transcription closure paragraph from the final-review addendum<br>[WP-38.05](../../work-packages/38-arcslate-render-and-colour.md#rule-wp-38.05) — the ASR real-provider closure named explicitly: 'WP43 provides real model output and WP52 closes the paid end-to-end path'<br>[WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) Final-review closure paragraph: paid Slate transcription end-to-end, CF purge inventory paging, seven-day wait guards, post-backup unsafe-effect quarantine, real active/waiting/unknown states for [WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) recovery — package-level obligation contribution |
| Start prerequisites | **artifact** [HAR.06](#task-har-06) — real, delivered outcome of HAR.06 (Durable Cloud automation, scheduling and automation-fixture removal). *Why:* this integration exercises the real durable Cloud automation, scheduling and automation-fixture removal instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [AIR.09](ai-routing.md#task-air-09) — real, delivered outcome of AIR.09 (ASR/Whisper capability closure and inference-late-outcome reconciliation). *Why:* this integration exercises the real aSR/Whisper capability closure and inference-late-outcome reconciliation instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SLATE.30](arcslate.md#task-slate-30) — real, delivered outcome of SLATE.30 (Local transcription extraction ProductJob and TranscriptRecord adoption). *Why:* this integration exercises the real local transcription extraction ProductJob and TranscriptRecord adoption instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [AIR.08](ai-routing.md#task-air-08) — real, delivered outcome of AIR.08 (Real-provider metering evidence and stubbed-path removal). *Why:* this integration exercises the real real-provider metering evidence and stubbed-path removal instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.08.harness](adoption.md#task-adopt-08-harness) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [HAR.90](#task-har-90), [SLATE.30](arcslate.md#task-slate-30), [SLATE.32](arcslate.md#task-slate-32) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Actual [WP-39](../../work-packages/39-arcslate-integration-and-portability.md#rule-wp-39) selected-audio upload through CF Whisper, normal C# metering/final artifact and explicit local subtitle adoption; partial/unknown outcome, cancellation, budget bound, origin and no-raw-video-upload; paged exact CF purge inventory, stale controls/late evidence, seven-day wait budget guards, post-backup unsafe-effect quarantine; real active/waiting/unknown states for [WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) recovery. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as SLATE.41. |
