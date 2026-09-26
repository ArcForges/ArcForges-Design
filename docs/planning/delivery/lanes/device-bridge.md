# Application presence and tool bridge — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Application presence, durable target queue, owner reauthorization and exact result reconciliation.

Tasks: 12 · Owning repositories: Cloud, DesktopPlatform · Integration owner(s): Cloud integration owner, DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [DEV.01](#task-dev-01) | Application presence (ApplicationService List/Heartbeat/Disconnect) | service | M | [CLOUD.13](cloud.md#task-cloud-13) (artifact), [CLOUD.29](cloud.md#task-cloud-29) (artifact), [CON.11](contracts.md#task-con-11) (contract) | not-started |
| [DEV.02](#task-dev-02) | Durable target queue | service | M | [DEV.01](#task-dev-01) (artifact), [CON.10](contracts.md#task-con-10) (contract) | not-started |
| [DEV.03](#task-dev-03) | Owner reauthorization (Device.Runtime local re-authorization) | service | M | [AST.11](assistant.md#task-ast-11) (artifact), [APP.05](app-composition.md#task-app-05) (artifact), [PLT.43](platform.md#task-plt-43) (artifact) | not-started |
| [DEV.04](#task-dev-04) | Execution and result deduplication -- Cloud D1 attempt/result store | service | M | [DEV.02](#task-dev-02) (artifact), [CON.10](contracts.md#task-con-10) (contract) | not-started |
| [DEV.05](#task-dev-05) | Execution and result deduplication -- Desktop command_log agreement | service | M | [DEV.03](#task-dev-03) (artifact), [EXE.01](execution.md#task-exe-01) (artifact) | not-started |
| [DEV.06](#task-dev-06) | Remote approval and steering | service | M | [DEV.02](#task-dev-02) (artifact), [DEV.03](#task-dev-03) (artifact), [PLT.39](platform.md#task-plt-39) (artifact) | not-started |
| [DEV.07](#task-dev-07) | Offline expiry and recovery | service | S | [DEV.02](#task-dev-02) (artifact) | not-started |
| [DEV.08](#task-dev-08) | Frozen application locality | service | S | [DEV.02](#task-dev-02) (artifact) | not-started |
| [DEV.09](#task-dev-09) | Owned-artifact receipt and real integration | acceptance | M | [DEV.01](#task-dev-01) (artifact), [DEV.02](#task-dev-02) (artifact), [DEV.03](#task-dev-03) (artifact), [DEV.04](#task-dev-04) (artifact), [DEV.05](#task-dev-05) (artifact), [DEV.06](#task-dev-06) (artifact), [DEV.07](#task-dev-07) (artifact), [DEV.08](#task-dev-08) (artifact), [DEV.12](#task-dev-12) (artifact) | not-started |
| [DEV.12](#task-dev-12) | Cross-repo (toolRequestId,attemptId,commandId) agreement between Cloud D1 and Desktop command_log | integration | M | [DEV.04](#task-dev-04) (artifact), [DEV.05](#task-dev-05) (artifact) | not-started |
| [DEV.13](#task-dev-13) | Real Harness-planned tool request flowing through the real device bridge end-to-end | integration | M | [AST.19](assistant.md#task-ast-19) (artifact), [HAR.02](harness.md#task-har-02) (artifact), [DEV.02](#task-dev-02) (artifact), [DEV.03](#task-dev-03) (artifact), [DEV.04](#task-dev-04) (artifact), [DEV.05](#task-dev-05) (artifact), [DEV.06](#task-dev-06) (artifact), [DEV.12](#task-dev-12) (artifact) | not-started |
| [DEV.14](#task-dev-14) | Real device tool bridge over the deployed realtime transport | integration | M | [CLOUD.29](cloud.md#task-cloud-29) (artifact), [CLOUD.30](cloud.md#task-cloud-30) (artifact), [CLOUD.31](cloud.md#task-cloud-31) (artifact), [CLOUD.33](cloud.md#task-cloud-33) (artifact), [CLOUD.34](cloud.md#task-cloud-34) (artifact), [AST.11](assistant.md#task-ast-11) (artifact), [DEV.01](#task-dev-01) (artifact), [DEV.02](#task-dev-02) (artifact), [DEV.03](#task-dev-03) (artifact), [DEV.04](#task-dev-04) (artifact), [DEV.05](#task-dev-05) (artifact), [DEV.12](#task-dev-12) (artifact) | not-started |

## Tasks

<a id="task-dev-01"></a>

### DEV.01 — Application presence (ApplicationService List/Heartbeat/Disconnect)

**Outcome.** ApplicationService.List/Heartbeat/Disconnect implemented with DO projection of D1 installation authority; separate app rows per device; 30s expiry/10s renewal, restarted epoch, app-offline-without-device-wide-false-availability proven.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/dev-01` and ledger record `ledger/tasks/dev-01.md` in the Plan repository; task branch `task/dev-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-26.00](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.00) — full |
| Provides | application-presence-service |
| Start prerequisites | **artifact** [CLOUD.13](cloud.md#task-cloud-13) — real device/installation/instance/session authority in D1 (not a placeholder). *Why:* the DO projects this real installation authority; Cloud repo currently has only a hello-world endpoint, no identity model<br>**artifact** [CLOUD.29](cloud.md#task-cloud-29) — real Durable-Object-backed connection/authentication substrate. *Why:* presence heartbeat/disconnect rides the same authenticated realtime connection<br>**contract** [CON.11](contracts.md#task-con-11) — published ApplicationService.List/Heartbeat/Disconnect wire definitions. *Why:* the Cloud implementation is generated-contract-first |
| Entry condition | [ADOPT.07.device-bridge](adoption.md#task-adopt-07-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [DEV.02](#task-dev-02), [DEV.09](#task-dev-09), [DEV.14](#task-dev-14) |
| Write scope | `Cloud:src/ArcForges.Cloud/Presence/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | Offline/local Worker+DO test harness only (per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), no hosted live-service CI): expiry/renewal timers, restarted epoch, offline-without-false-availability. |
| Completion evidence | Expiry/renewal timer test results, restarted-epoch test, per-device-row isolation proof. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Cloud repo HEAD ce0a32a has only the ArcForges.Cloud hello-world project (BuildIdentity/HealthStatus/HelloEndpoint/Program); no Application/Presence service exists. |
| Notes | Exact Cloud-side project path for the WP21 to WP26 service split is not yet established in-repo; glob is a reasonable placeholder pending that layout decision (the Cloud lane / WP22 to WP23 territory). |

<a id="task-dev-02"></a>

### DEV.02 — Durable target queue

**Outcome.** ToolRequest freezes product/device/installation and current instance epoch; commands/receipts remain in D1. Another application cannot claim; duplicate/lost ack/expiry and per-owner budget proven.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/dev-02` and ledger record `ledger/tasks/dev-02.md` in the Plan repository; task branch `task/dev-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-26.01](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.01) — full |
| Provides | tool-request-queue |
| Start prerequisites | **artifact** [DEV.01](#task-dev-01) — the real installation/epoch projection to freeze against. *Why:* ToolRequest freezes the current instance epoch established by presence<br>**contract** [CON.10](contracts.md#task-con-10) — published ToolRequest wire shape (contracts/03 §5.1 fields). *Why:* the queue persists the exact published fields (toolRequestId, attemptId, commandId, targetDeviceId, capability, etc.) |
| Entry condition | [ADOPT.07.device-bridge](adoption.md#task-adopt-07-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.25](android.md#task-and-25), [DEV.04](#task-dev-04), [DEV.06](#task-dev-06), [DEV.07](#task-dev-07), [DEV.08](#task-dev-08), [DEV.09](#task-dev-09), [DEV.13](#task-dev-13), [DEV.14](#task-dev-14), [WEB.28](web.md#task-web-28) |
| Write scope | `Cloud:src/ArcForges.Cloud/ToolBridge/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | Offline/local Worker+D1 test harness: another-app-cannot-claim, duplicate/lost-ack/expiry, per-owner budget. |
| Completion evidence | Claim-isolation, duplicate/lost-ack, expiry and budget test results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: |

<a id="task-dev-03"></a>

### DEV.03 — Owner reauthorization (Device.Runtime local re-authorization)

**Outcome.** Device.Runtime invokes registered typed in-process product handlers after current grant/resource/revision/egress checks; no local product RPC, shared database or delegation through a shared integration owner.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/dev-03` and ledger record `ledger/tasks/dev-03.md` in the Plan repository; task branch `task/dev-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-26.02](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.02) — full |
| Provides | device-runtime-owner-reauth |
| Start prerequisites | **artifact** [AST.11](assistant.md#task-ast-11) — the Device.Runtime project skeleton and typed dispatch adapter interfaces built as the 17.01 fixture boundary. *Why:* this task extends that same project with real owner-reauthorization logic rather than creating a parallel one<br>**artifact** [APP.05](app-composition.md#task-app-05) — the exact [WP-14.04](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04) owner approval/authorization enforcement point. *Why:* contracts/02 confirms InvokeAsync performs owner-side final validation under [WP-14.04](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04) and [WP-26.02](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.02) -- the same mechanism, two call sites<br>**artifact** [PLT.43](platform.md#task-plt-43) — published capability leases and trust verification. *Why:* re-authorization re-checks the real lease/trust state, not a private duplicate |
| Entry condition | [ADOPT.02.device-bridge](adoption.md#task-adopt-02-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.25](android.md#task-and-25), [DEV.05](#task-dev-05), [DEV.06](#task-dev-06), [DEV.09](#task-dev-09), [DEV.13](#task-dev-13), [DEV.14](#task-dev-14), [SLATE.33](arcslate.md#task-slate-33), [WEB.28](web.md#task-web-28) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Communication.DeviceRuntime/**` |
| Validation | Offline unit tests: no local product RPC/shared database/integration owner delegation. |
| Completion evidence | Negative tests proving no RPC/shared-database/integration owner path exists. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-dev-04"></a>

### DEV.04 — Execution and result deduplication -- Cloud D1 attempt/result store

**Outcome.** Bridge request/result persisted in D1 using full ApplicationTarget and (toolRequestId,attemptId,commandId) plus result hash; multiple tool requests per attempt both persist; identical replay returns its own receipt; changed result hash refuses; stale epoch and cross-application delivery rejected.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/dev-04` and ledger record `ledger/tasks/dev-04.md` in the Plan repository; task branch `task/dev-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) — Cloud-side D1 attempt-row persistence, hash dedup and cross-application delivery guard<br>[WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) Tool-result acceptance paragraph (between §5 and §6): two distinct toolRequestIds in one attempt both persist and each replay returns its own original receipt; a changed result under the same (toolRequestId,attemptId,commandId) refuses with command.reused_identifier; lost acknowledgement never allocates a fresh command or drops the second result. Bound to the wire registry, [TK-05](../../../architecture/contracts/01-public-api-operations.md#rule-tk-05) and task.tool_result -- the same key [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) uses. — package-level obligation contribution |
| Provides | bridge-dedup-store-cloud |
| Start prerequisites | **artifact** [DEV.02](#task-dev-02) — the real durable target queue to attach results to. *Why:* result persistence extends the same D1 queue row<br>**contract** [CON.10](contracts.md#task-con-10) — published (toolRequestId,attemptId,commandId)+hash wire shape, [TK-05](../../../architecture/contracts/01-public-api-operations.md#rule-tk-05), task.tool_result. *Why:* the dedup key is fixed by the published wire registry, shared with EXE's execution-persistence key |
| Entry condition | [ADOPT.07.device-bridge](adoption.md#task-adopt-07-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [DEV.09](#task-dev-09), [DEV.12](#task-dev-12), [DEV.13](#task-dev-13), [DEV.14](#task-dev-14) |
| Write scope | `Cloud:src/ArcForges.Cloud/ToolBridge/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | Offline/local D1 test harness: multi-request-per-attempt, identical replay, changed-hash refusal, stale epoch, cross-application delivery rejection. |
| Completion evidence | Dedup/replay/hash-mismatch/stale-epoch test results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: |
| Notes | Split from [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) by repo; see DEV.05 for the desktop-side half and IM.tool-bridge-dedup-agreement for the cross-repo proof. |

<a id="task-dev-05"></a>

### DEV.05 — Execution and result deduplication -- Desktop command_log agreement

**Outcome.** Owner handler's normal in-process validation records the same (toolRequestId,attemptId,commandId) plus result hash into a local command_log; agrees with the Cloud attempt row ([BI-03](../../../architecture/contracts/03-realtime-and-bridge.md#rule-bi-03)); duplicate delivery and uncertain external effect handled locally.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/dev-05` and ledger record `ledger/tasks/dev-05.md` in the Plan repository; task branch `task/dev-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) — Desktop command_log persistence and (toolRequestId,attemptId,commandId) agreement with the Cloud attempt row<br>[WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) Tool-result acceptance paragraph (between §5 and §6): two distinct toolRequestIds in one attempt both persist and each replay returns its own original receipt; a changed result under the same (toolRequestId,attemptId,commandId) refuses with command.reused_identifier; lost acknowledgement never allocates a fresh command or drops the second result. Bound to the wire registry, [TK-05](../../../architecture/contracts/01-public-api-operations.md#rule-tk-05) and task.tool_result -- the same key [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) uses. — package-level obligation contribution |
| Provides | bridge-dedup-store-desktop |
| Start prerequisites | **artifact** [DEV.03](#task-dev-03) — the real owner-reauthorization call site to log results from. *Why:* command_log records the outcome of the real reauthorized invocation<br>**artifact** [EXE.01](execution.md#task-exe-01) — the execution-persistence project to extend with the command_log table, rather than a parallel store. *Why:* avoids a second unrelated persistence mechanism for the same dedup concern EXE.01 already owns at the execution level |
| Entry condition | [ADOPT.02.device-bridge](adoption.md#task-adopt-02-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [DEV.09](#task-dev-09), [DEV.12](#task-dev-12), [DEV.13](#task-dev-13), [DEV.14](#task-dev-14) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Execution.Persistence/**`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Communication.DeviceRuntime/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline unit tests: duplicate delivery, uncertain external effect, local/Cloud key agreement using a contract-bound fixture for the Cloud side. |
| Completion evidence | Duplicate-delivery and uncertain-effect test results; local-vs-fixture-Cloud key agreement proof. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Real cross-repo agreement (this store vs the actual Cloud D1 row) is proven by IM.tool-bridge-dedup-agreement, not by this task alone. |

<a id="task-dev-06"></a>

### DEV.06 — Remote approval and steering

**Outcome.** One-target approvals, sensitive local-presence requirements and ordinary steering bounds preserved; mobile biometric cannot substitute for target presence; stale approval fails.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/dev-06` and ledger record `ledger/tasks/dev-06.md` in the Plan repository; task branch `task/dev-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-26.04](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.04) — full |
| Provides | bridge-remote-approval |
| Start prerequisites | **artifact** [DEV.02](#task-dev-02) — the real durable target queue to gate with approval. *Why:* approval attaches to the real queued ToolRequest<br>**artifact** [DEV.03](#task-dev-03) — the real desktop local-presence enforcement to require. *Why:* [AZ-01](../../../architecture/08-security-architecture.md#rule-az-01) requires sensitive approvals reach real target presence, not a Cloud-only assertion<br>**artifact** [PLT.39](platform.md#task-plt-39) — published approval/steering/step-up mechanism. *Why:* remote approval reuses the real security step-up primitive, not a private one |
| Entry condition | [ADOPT.07.device-bridge](adoption.md#task-adopt-07-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.25](android.md#task-and-25), [DEV.09](#task-dev-09), [DEV.13](#task-dev-13), [WEB.28](web.md#task-web-28) |
| Write scope | `Cloud:src/ArcForges.Cloud/ToolBridge/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | Offline/local test harness: mobile-biometric-cannot-substitute, stale-approval-fails. |
| Completion evidence | Biometric-substitution-refusal and stale-approval test results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: |

<a id="task-dev-07"></a>

### DEV.07 — Offline expiry and recovery

**Outcome.** Explicit offline queue expiry/reconciliation; changing the selected app cannot retarget queued work. Disconnect/revoke/reinstall proven with no silent alternate product/device selection.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/dev-07` and ledger record `ledger/tasks/dev-07.md` in the Plan repository; task branch `task/dev-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-26.05](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.05) — full |
| Provides | bridge-offline-expiry |
| Start prerequisites | **artifact** [DEV.02](#task-dev-02) — the real durable target queue to expire/reconcile. *Why:* expiry acts on real queued rows |
| Entry condition | [ADOPT.07.device-bridge](adoption.md#task-adopt-07-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.25](android.md#task-and-25), [DEV.09](#task-dev-09), [WEB.28](web.md#task-web-28) |
| Write scope | `Cloud:src/ArcForges.Cloud/ToolBridge/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | Offline/local test harness: disconnect/revoke/reinstall, no silent retarget. |
| Completion evidence | Disconnect/revoke/reinstall test results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: |

<a id="task-dev-08"></a>

### DEV.08 — Frozen application locality

**Outcome.** Cloud-only steps may run without a desktop; every device step in one execution remains in the frozen product scope. Own-app multi-tool workflow passes; cross-product capability absent/future.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/dev-08` and ledger record `ledger/tasks/dev-08.md` in the Plan repository; task branch `task/dev-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-26.06](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.06) — full |
| Provides | bridge-frozen-locality |
| Start prerequisites | **artifact** [DEV.02](#task-dev-02) — the real durable target queue whose ApplicationTarget freeze this enforces. *Why:* locality is enforced on the real frozen ApplicationTarget field |
| Entry condition | [ADOPT.07.device-bridge](adoption.md#task-adopt-07-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [DEV.09](#task-dev-09), [HAR.05](harness.md#task-har-05) |
| Write scope | `Cloud:src/ArcForges.Cloud/ToolBridge/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | Offline/local test harness: own-app multi-tool workflow, cross-product-absent assertion. |
| Completion evidence | Multi-tool workflow and cross-product-absence test results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: |

<a id="task-dev-09"></a>

### DEV.09 — Owned-artifact receipt and real integration

**Outcome.** WP26 built/packed once from a clean environment across both repositories; all applicable UX acceptance groups recorded; failure/recovery and the real boundaries above proven; no later-provider fixture closes a real WP26 gate.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/dev-09` and ledger record `ledger/tasks/dev-09.md` in the Plan repository; task branch `task/dev-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-26.90](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.90) — full |
| Provides | wp26-accepted-artifact |
| Start prerequisites | **artifact** [DEV.01](#task-dev-01) — completed [WP-26.00](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.00). *Why:* aggregation<br>**artifact** [DEV.02](#task-dev-02) — completed [WP-26.01](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.01). *Why:* aggregation<br>**artifact** [DEV.03](#task-dev-03) — completed [WP-26.02](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.02). *Why:* aggregation<br>**artifact** [DEV.04](#task-dev-04) — completed [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) Cloud half. *Why:* aggregation<br>**artifact** [DEV.05](#task-dev-05) — completed [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) Desktop half. *Why:* aggregation<br>**artifact** [DEV.06](#task-dev-06) — completed [WP-26.04](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.04). *Why:* aggregation<br>**artifact** [DEV.07](#task-dev-07) — completed [WP-26.05](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.05). *Why:* aggregation<br>**artifact** [DEV.08](#task-dev-08) — completed [WP-26.06](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.06). *Why:* aggregation<br>**artifact** [DEV.12](#task-dev-12) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.device-bridge](adoption.md#task-adopt-07-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `Cloud:artifacts/evidence/**` |
| Validation | Clean-environment build/pack across both repos; [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) scope only (no live-service CI); real cross-repo dedup agreement proven per IM.tool-bridge-dedup-agreement. |
| Completion evidence | Source commits (both repos), artifact versions/hashes, environment, UX-D/E rows, real-boundary test results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Own capabilities are real here (device-tool-path mechanics are 'must be real early' per implementation-sequence §3); the CONTENT of tool requests (model-driven planning) stays fixture/scripted until [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) -- see IM.agent-driven-device-tool-use for that separate real-scenario proof. |

<a id="task-dev-12"></a>

### DEV.12 — Cross-repo (toolRequestId,attemptId,commandId) agreement between Cloud D1 and Desktop command_log

**Outcome.** [BI-03](../../../architecture/contracts/03-realtime-and-bridge.md#rule-bi-03): the Cloud attempt row and the desktop command_log genuinely agree under concurrent/duplicate/lost-ack delivery, not just each side's own unit tests

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/dev-12` and ledger record `ledger/tasks/dev-12.md` in the Plan repository; task branch `task/dev-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-26.03](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) — cross-repo agreement proof beyond each side's own unit coverage |
| Start prerequisites | **artifact** [DEV.04](#task-dev-04) — real, delivered outcome of DEV.04 (Execution and result deduplication -- Cloud D1 attempt/result store). *Why:* this integration exercises the real execution and result deduplication -- Cloud D1 attempt/result store instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [DEV.05](#task-dev-05) — real, delivered outcome of DEV.05 (Execution and result deduplication -- Desktop command_log agreement). *Why:* this integration exercises the real execution and result deduplication -- Desktop command_log agreement instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.07.device-bridge](adoption.md#task-adopt-07-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.25](android.md#task-and-25), [CLOUD.36](cloud.md#task-cloud-36), [DEV.09](#task-dev-09), [DEV.13](#task-dev-13), [DEV.14](#task-dev-14), [WEB.28](web.md#task-web-28) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | [BI-03](../../../architecture/contracts/03-realtime-and-bridge.md#rule-bi-03): the Cloud attempt row and the desktop command_log genuinely agree under concurrent/duplicate/lost-ack delivery, not just each side's own unit tests |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-dev-13"></a>

### DEV.13 — Real Harness-planned tool request flowing through the real device bridge end-to-end

**Outcome.** an actual Cloud-planned Agent Task step (not a scripted ToolRequest) reaches a real desktop, is locally re-authorized, executed and its result accepted -- the real integration producer-artifacts.md names as closing WP26's remaining fixture-content gap

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/dev-13` and ledger record `ledger/tasks/dev-13.md` in the Plan repository; task branch `task/dev-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-52.05](../../work-packages/52-cloud-harness.md#rule-wp-52.05) — all work except the parts mapped to AST.19, HAR.05 |
| Start prerequisites | **artifact** [AST.19](assistant.md#task-ast-19) — real, delivered outcome of AST.19 (Real Cloud Harness turn loop replacing the fixture turn endpoint). *Why:* this integration exercises the real real Cloud Harness turn loop replacing the fixture turn endpoint instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [HAR.02](harness.md#task-har-02) — real Harness approval and tool-dispatch path. *Why:* a Harness-planned tool request must originate from the real approval and dispatch loop<br>**artifact** [DEV.02](#task-dev-02) — the real durable target queue. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.03](#task-dev-03) — real owner reauthorization on the desktop. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.04](#task-dev-04) — real Cloud attempt and result deduplication. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.05](#task-dev-05) — real desktop command_log agreement. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.06](#task-dev-06) — real remote approval and steering. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.12](#task-dev-12) — the cross-repository (toolRequestId, attemptId, commandId) agreement. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.07.device-bridge](adoption.md#task-adopt-07-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [HAR.05](harness.md#task-har-05) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | an actual Cloud-planned Agent Task step (not a scripted ToolRequest) reaches a real desktop, is locally re-authorized, executed and its result accepted -- the real integration producer-artifacts.md names as closing WP26's remaining fixture-content gap |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-dev-14"></a>

### DEV.14 — Real device tool bridge over the deployed realtime transport

**Outcome.** The device tool path (pull, local re-authorisation, generated decode, typed invocation, idempotent result) works over the real deployed stream transport -- this is explicitly must-be-real-early per implementation-sequence §3, owned jointly with the assistant lanes [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26)

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform`; also touches Cloud |
| Claim, branch and ledger | `claims/dev-14` and ledger record `ledger/tasks/dev-14.md` in the Plan repository; task branch `task/dev-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-24.01](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.01) — device-targeted feed real integration |
| Start prerequisites | **artifact** [CLOUD.29](cloud.md#task-cloud-29) — real, delivered outcome of CLOUD.29 (Stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells)). *Why:* this integration exercises the real stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.30](cloud.md#task-cloud-30) — real, delivered outcome of CLOUD.30 (Scoped subscription (owner/product/filter/recovery-generation binding)). *Why:* this integration exercises the real scoped subscription (owner/product/filter/recovery-generation binding) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.31](cloud.md#task-cloud-31) — real, delivered outcome of CLOUD.31 (Cursor and gap handling (DO projection backed by D1 outbox)). *Why:* this integration exercises the real cursor and gap handling (DO projection backed by D1 outbox) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.33](cloud.md#task-cloud-33) — real, delivered outcome of CLOUD.33 (Publication and wake (D1 outbox to bounded DO feed via Queues)). *Why:* this integration exercises the real publication and wake (D1 outbox to bounded DO feed via Queues) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.34](cloud.md#task-cloud-34) — real, delivered outcome of CLOUD.34 (Bounded stream lifecycle). *Why:* this integration exercises the real bounded stream lifecycle instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [AST.11](assistant.md#task-ast-11) — assistant Cloud client and device runtime. *Why:* the real bridge integration replaces the loopback used by the assistant device runtime<br>**artifact** [DEV.01](#task-dev-01) — real application presence. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.02](#task-dev-02) — the real durable target queue. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.03](#task-dev-03) — real owner reauthorization on the desktop. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.04](#task-dev-04) — real Cloud attempt and result deduplication. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.05](#task-dev-05) — real desktop command_log agreement. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.12](#task-dev-12) — the cross-repository (toolRequestId, attemptId, commandId) agreement. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.02.device-bridge](adoption.md#task-adopt-02-device-bridge) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.36](cloud.md#task-cloud-36) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | The device tool path (pull, local re-authorisation, generated decode, typed invocation, idempotent result) works over the real deployed stream transport -- this is explicitly must-be-real-early per implementation-sequence §3, owned jointly with the assistant lanes [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) |
| Baseline (unreviewed unless accepted) | not-started |
