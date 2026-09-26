# Execution engine — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Local ProductJob execution chain, lifecycle, failures, checkpoints and concurrency.

Tasks: 9 · Owning repositories: DesktopPlatform · Integration owner(s): DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [EXE.01](#task-exe-01) | Execution chain and its persistence (ProductJob engine core) | producer | L | [APP.01](app-composition.md#task-app-01) (artifact), [FND.02](foundation.md#task-fnd-02) (artifact), [FND.03](foundation.md#task-fnd-03) (artifact), [PLT.17](platform.md#task-plt-17) (artifact) | not-started |
| [EXE.02](#task-exe-02) | Lifecycle states and reason facets | producer | S | [EXE.01](#task-exe-01) (artifact) | not-started |
| [EXE.03](#task-exe-03) | Failure classification and retry | producer | M | [EXE.01](#task-exe-01) (artifact) | not-started |
| [EXE.04](#task-exe-04) | Child tasks and ownership | producer | M | [EXE.01](#task-exe-01) (artifact) | not-started |
| [EXE.05](#task-exe-05) | Checkpoints and compensation | producer | M | [EXE.01](#task-exe-01) (artifact) | not-started |
| [EXE.06](#task-exe-06) | Approval, steering and budget integration | producer | M | [EXE.01](#task-exe-01) (artifact), [PLT.39](platform.md#task-plt-39) (artifact) | not-started |
| [EXE.07](#task-exe-07) | Progress, outcome and trace | producer | M | [EXE.01](#task-exe-01) (artifact) | not-started |
| [EXE.08](#task-exe-08) | Concurrency, loops and storms | producer | M | [EXE.01](#task-exe-01) (artifact) | not-started |
| [EXE.09](#task-exe-09) | Owned-artifact receipt and real integration | acceptance | M | [EXE.01](#task-exe-01) (artifact), [EXE.02](#task-exe-02) (artifact), [EXE.03](#task-exe-03) (artifact), [EXE.04](#task-exe-04) (artifact), [EXE.05](#task-exe-05) (artifact), [EXE.06](#task-exe-06) (artifact), [EXE.07](#task-exe-07) (artifact), [EXE.08](#task-exe-08) (artifact) | not-started |

## Tasks

<a id="task-exe-01"></a>

### EXE.01 — Execution chain and its persistence (ProductJob engine core)

**Outcome.** The full ProductJob/JobStep/JobAttempt chain with distinct types and lifecycles, persisted durably at every state transition; invalid transitions rejected; state survives process termination.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/exe-01` and ledger record `ledger/tasks/exe-01.md` in the Plan repository; task branch `task/exe-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L · early risk proof |
| Obligations | [WP-16.00](../../work-packages/16-unified-execution-engine.md#rule-wp-16.00) — full<br>[WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) Tool-result acceptance paragraph (between §5 and §6): two distinct toolRequestIds in one attempt both persist and each replay returns its own original receipt; a changed result under the same (toolRequestId,attemptId,commandId) refuses with command.reused_identifier; lost acknowledgement never allocates a fresh command or drops the second result. Bound to the wire registry, [TK-05](../../../architecture/contracts/01-public-api-operations.md#rule-tk-05) and task.tool_result -- the same key [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) uses. — package-level obligation contribution |
| Provides | execution-chain-store; productjob-engine-pkg |
| Start prerequisites | **artifact** [APP.01](app-composition.md#task-app-01) — published product/profile identity (ApplicationScope) from Assistant.Abstractions. *Why:* [BR-05](../../../architecture/14-build-packaging-and-release.md#rule-br-05) requires a task be owned by exactly one product; ownership binds to this real identity type<br>**artifact** [FND.02](foundation.md#task-fnd-02) — published execution identity and idempotency records. *Why:* JobAttempt retry allocates a new attempt but reuses the command identity from this contract<br>**artifact** [FND.03](foundation.md#task-fnd-03) — published revision and sequence records. *Why:* durable state transitions are ordered/versioned using this contract<br>**artifact** [PLT.17](platform.md#task-plt-17) — real application identity and in-process composition. *Why:* the engine composes into the host process using the real composition model |
| Entry condition | [ADOPT.02.execution](adoption.md#task-adopt-02-execution) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.10](assistant.md#task-ast-10), [AST.13](assistant.md#task-ast-13), [DEV.05](device-bridge.md#task-dev-05), [EXE.02](#task-exe-02), [EXE.03](#task-exe-03), [EXE.04](#task-exe-04), [EXE.05](#task-exe-05), [EXE.06](#task-exe-06), [EXE.07](#task-exe-07), [EXE.08](#task-exe-08), [EXE.09](#task-exe-09), [SLATE.28](arcslate.md#task-slate-28), [SLATE.30](arcslate.md#task-slate-30) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Execution/**`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Execution.Persistence/**`<br>`DesktopPlatform:tests/ExecutionEngineTests/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append), [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline unit tests: state-machine invalid-transition rejection, kill-at-every-transition-point durability; no live environment. |
| Completion evidence | State-machine coverage report, kill-at-transition recovery log. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No ArcForges.Execution* project exists in DesktopPlatform yet. |
| Notes | Narrow early-risk proof: kill-at-any-transition durability underlies WP16.03-07, WP17.03 Task Centre and the vocabulary WP52 reuses. A defect here invalidates checkpoint/compensation/concurrency work built on top. |

<a id="task-exe-02"></a>

### EXE.02 — Lifecycle states and reason facets

**Outcome.** Every reachable state carries a reason facet (waiting for approval, waiting for a resource, blocked on limit, paused, retrying) that reaches the UI; never a bare state alone.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/exe-02` and ledger record `ledger/tasks/exe-02.md` in the Plan repository; task branch `task/exe-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-16.01](../../work-packages/16-unified-execution-engine.md#rule-wp-16.01) — full |
| Provides | execution-reason-facets |
| Start prerequisites | **artifact** [EXE.01](#task-exe-01) — the real state machine to attach reason facets to. *Why:* reason facets annotate the real transitions, not a mock enum |
| Entry condition | [ADOPT.02.execution](adoption.md#task-adopt-02-execution) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXE.09](#task-exe-09) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Execution/**` |
| Validation | Offline coverage test (every reachable state has a facet) plus a presentation test that the reason reaches the UI layer. |
| Completion evidence | Reason-facet coverage report. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-exe-03"></a>

### EXE.03 — Failure classification and retry

**Outcome.** Failures classify into transient/permanent/refused/cancelled/unknown-effect with effect certainty; an unknown-effect failure on a non-idempotent operation never auto-retries.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/exe-03` and ledger record `ledger/tasks/exe-03.md` in the Plan repository; task branch `task/exe-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-16.02](../../work-packages/16-unified-execution-engine.md#rule-wp-16.02) — full |
| Provides | execution-failure-classification |
| Start prerequisites | **artifact** [EXE.01](#task-exe-01) — the real state machine to classify failures against. *Why:* classification decisions drive real transitions |
| Entry condition | [ADOPT.02.execution](adoption.md#task-adopt-02-execution) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXE.09](#task-exe-09) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Execution/**` |
| Validation | Offline classification matrix test; negative test for non-idempotent unknown-effect auto-retry. |
| Completion evidence | Classification matrix, no-auto-retry proof. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Shares vocabulary only (not implementation) with the Cloud AgentTask failure model in requirements/05 ([WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52)); no cross-repo dependency. |

<a id="task-exe-04"></a>

### EXE.04 — Child tasks and ownership

**Outcome.** A task may spawn children with their own lifecycle/budget/cancellation relationship; cancelling a parent cancels children, a failed child does not necessarily fail its parent, ownership is uniform across the tree.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/exe-04` and ledger record `ledger/tasks/exe-04.md` in the Plan repository; task branch `task/exe-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-16.03](../../work-packages/16-unified-execution-engine.md#rule-wp-16.03) — full |
| Provides | execution-child-task-tree |
| Start prerequisites | **artifact** [EXE.01](#task-exe-01) — the real state machine and persistence to attach child relationships to. *Why:* child ownership/cancellation must be durable, not in-memory only |
| Entry condition | [ADOPT.02.execution](adoption.md#task-adopt-02-execution) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXE.09](#task-exe-09) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Execution/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline tests: cancellation propagation, child-failure isolation, ownership assertion across the tree. |
| Completion evidence | Cancellation/isolation/ownership test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-exe-05"></a>

### EXE.05 — Checkpoints and compensation

**Outcome.** Checkpoints capture resumable state at declared boundaries; compensation actions run in reverse order on abort; an undeclared irreversible effect fails validation.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/exe-05` and ledger record `ledger/tasks/exe-05.md` in the Plan repository; task branch `task/exe-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-16.04](../../work-packages/16-unified-execution-engine.md#rule-wp-16.04) — full<br>[WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) Tool-result acceptance paragraph (between §5 and §6): two distinct toolRequestIds in one attempt both persist and each replay returns its own original receipt; a changed result under the same (toolRequestId,attemptId,commandId) refuses with command.reused_identifier; lost acknowledgement never allocates a fresh command or drops the second result. Bound to the wire registry, [TK-05](../../../architecture/contracts/01-public-api-operations.md#rule-tk-05) and task.tool_result -- the same key [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) uses. — package-level obligation contribution |
| Provides | execution-checkpoint-compensation |
| Start prerequisites | **artifact** [EXE.01](#task-exe-01) — the real durable state machine to checkpoint. *Why:* resume-after-kill must exercise the real persistence |
| Entry condition | [ADOPT.02.execution](adoption.md#task-adopt-02-execution) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.13](assistant.md#task-ast-13), [EXE.09](#task-exe-09) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Execution/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline tests: resume-from-checkpoint after kill, compensation-on-abort ordering, undeclared-irreversible validation failure. |
| Completion evidence | Resume and compensation-ordering test results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Same (toolRequestId,attemptId,commandId) dedup key referenced by the WP16 'Tool-result acceptance' package-level obligation shared with DEV.04/DEV.05 -- see package_obligations. |

<a id="task-exe-06"></a>

### EXE.06 — Approval, steering and budget integration

**Outcome.** Approval gates pause a task durably until resolved/expired; steering adjusts a running task without granting authority; local resource permits (CPU/memory/disk/queue) are acquired before and released after a bounded job step, with no monetary accounting.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/exe-06` and ledger record `ledger/tasks/exe-06.md` in the Plan repository; task branch `task/exe-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-16.05](../../work-packages/16-unified-execution-engine.md#rule-wp-16.05) — full |
| Provides | execution-approval-budget |
| Start prerequisites | **artifact** [EXE.01](#task-exe-01) — the real durable state machine to pause/resume. *Why:* approval-pause-across-restart requires real durability<br>**artifact** [PLT.39](platform.md#task-plt-39) — published approval/steering/step-up mechanism. *Why:* [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06) requires approval be a discrete authorization from the real security pipeline, steering grants nothing |
| Entry condition | [ADOPT.02.execution](adoption.md#task-adopt-02-execution) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXE.09](#task-exe-09) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Execution/**`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Execution.Budget/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline tests: approval-pause across restart, steering-grants-nothing, resource-permit acquisition/release, bounded queue/memory exhaustion. |
| Completion evidence | Approval/steering/budget test results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [BR-07](../../../architecture/14-build-packaging-and-release.md#rule-br-07): local resource permits only, [D-020](../../../decisions/phase-1-foundation-decisions.md#rule-d-020) monetary accounting explicitly absent here (Cloud-owned). |

<a id="task-exe-07"></a>

### EXE.07 — Progress, outcome and trace

**Outcome.** Progress is a separate best-effort channel; outcome is durable fact; execution trace, capability trace and audit stay separate (provider-interaction records stay Cloud-only); a user-visible task identifier resolves to its execution trace. Losing all progress never affects the recorded outcome.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/exe-07` and ledger record `ledger/tasks/exe-07.md` in the Plan repository; task branch `task/exe-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-16.06](../../work-packages/16-unified-execution-engine.md#rule-wp-16.06) — full |
| Provides | execution-progress-outcome-trace |
| Start prerequisites | **artifact** [EXE.01](#task-exe-01) — the real durable state machine to record outcome against. *Why:* the conflation test requires a real outcome record independent of progress delivery |
| Entry condition | [ADOPT.02.execution](adoption.md#task-adopt-02-execution) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXE.09](#task-exe-09) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Execution/**` |
| Validation | Offline tests: progress-loss-never-affects-outcome, task-id-to-trace resolution, trace-system separation. |
| Completion evidence | Conflation-test result, trace-resolution result, trace-separation result; payload/manifest hashes with content-origin carrier per WP16 §7 addition. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Content-origin behavior/carrier schema (requirements/07, requirements/13) is a frozen design input already decided, not a blocking producer task. |

<a id="task-exe-08"></a>

### EXE.08 — Concurrency, loops and storms

**Outcome.** Per-product and per-device/resource concurrency limits; loop detection preventing plan re-entry into the same step; storm protection preventing automation cascade; each limit produces a typed, explained refusal rather than silent unbounded queuing.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/exe-08` and ledger record `ledger/tasks/exe-08.md` in the Plan repository; task branch `task/exe-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-16.07](../../work-packages/16-unified-execution-engine.md#rule-wp-16.07) — full |
| Provides | execution-concurrency-guard |
| Start prerequisites | **artifact** [EXE.01](#task-exe-01) — the real state machine and job tree to bound. *Why:* loop/cascade detection operates on real step re-entry and real child trees (EXE.04) |
| Entry condition | [ADOPT.02.execution](adoption.md#task-adopt-02-execution) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXE.09](#task-exe-09) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Execution/**` |
| Validation | Offline tests: loop-injection, cascade-injection, saturation with explained refusal. |
| Completion evidence | Loop/cascade/saturation test results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Storm/cascade protection here is the native counterpart engine-level guard; the durable Cloud trigger scheduler itself is [WP-52.06](../../work-packages/52-cloud-harness.md#rule-wp-52.06) (see AST.14 substitute). |

<a id="task-exe-09"></a>

### EXE.09 — Owned-artifact receipt and real integration

**Outcome.** ProductJob-only responsibility preserved (no local model loop, no Cloud budget/Task ownership in the shared engine); shared execution vocabulary/package references, dispatch/error profiles and cancellation updated; pending later owners ([WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52)) and their closing gates recorded.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/exe-09` and ledger record `ledger/tasks/exe-09.md` in the Plan repository; task branch `task/exe-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-16.90](../../work-packages/16-unified-execution-engine.md#rule-wp-16.90) — full<br>[WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) §6 Impacts row 'Compatibility: Task contract versioning for later cloud and mobile surfaces' — package-level obligation contribution |
| Provides | wp16-accepted-artifact; productjob-ref-surface |
| Start prerequisites | **artifact** [EXE.01](#task-exe-01) — completed [WP-16.00](../../work-packages/16-unified-execution-engine.md#rule-wp-16.00). *Why:* aggregation<br>**artifact** [EXE.02](#task-exe-02) — completed [WP-16.01](../../work-packages/16-unified-execution-engine.md#rule-wp-16.01). *Why:* aggregation<br>**artifact** [EXE.03](#task-exe-03) — completed [WP-16.02](../../work-packages/16-unified-execution-engine.md#rule-wp-16.02). *Why:* aggregation<br>**artifact** [EXE.04](#task-exe-04) — completed [WP-16.03](../../work-packages/16-unified-execution-engine.md#rule-wp-16.03). *Why:* aggregation<br>**artifact** [EXE.05](#task-exe-05) — completed [WP-16.04](../../work-packages/16-unified-execution-engine.md#rule-wp-16.04). *Why:* aggregation<br>**artifact** [EXE.06](#task-exe-06) — completed [WP-16.05](../../work-packages/16-unified-execution-engine.md#rule-wp-16.05). *Why:* aggregation<br>**artifact** [EXE.07](#task-exe-07) — completed [WP-16.06](../../work-packages/16-unified-execution-engine.md#rule-wp-16.06). *Why:* aggregation<br>**artifact** [EXE.08](#task-exe-08) — completed [WP-16.07](../../work-packages/16-unified-execution-engine.md#rule-wp-16.07). *Why:* aggregation |
| Entry condition | [ADOPT.02.execution](adoption.md#task-adopt-02-execution) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.17](assistant.md#task-ast-17) |
| Write scope | `DesktopPlatform:artifacts/evidence/**` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Architecture-evidence review confirming no local model loop/Cloud budget ownership; [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) scope only. |
| Completion evidence | Source commit, producer version, candidate hashes, real-vs-fixture status (none expected for WP16 itself), task-contract versioning note for later Cloud/mobile surfaces. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Provides ProductJobRef, the surface [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52)'s Cloud Task consumes in the OTHER direction ([CT-01](../../../architecture/01-solution-and-project-layout.md#rule-ct-01)..07); WP16 does not depend on WP52, WP52 depends on this. |
