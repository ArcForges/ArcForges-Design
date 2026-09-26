<a id="rule-wp-26"></a>
# WP-26 — Application Presence and One-Application Tool Bridge

> Status: Authoritative — [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).
> Repositories: Cloud + DesktopPlatform. Consume only exact published upstream artifacts; no adjacent sources.

## 1. Scope and purpose

Deliver the complete owned behavior below under the [current project/package plan](../../architecture/27-platform-projects-and-application-assistants.md). Professional product semantics, security, exact values and recovery requirements remain binding. A completed Hello World or fixture cannot substitute for the listed production capability.

## 2. Required inputs and dependencies

[Producer registry](../producer-artifacts-and-integration.md), [wire registry](../../architecture/contracts/04-protobuf-wire-registry.md), [application/protocol profile](../../architecture/contracts/10-application-scope-and-streams.md), [D1 execution](../../architecture/data-model/04-d1-execution-profile.md), [history](../../architecture/data-model/05-application-history.md), [experience/acceptance](../../experience/README.md) and exact artifacts from the upstream WPs above. Later domain/AI fixtures are allowed only where explicitly named below and must be removed at their owning real integration gate.

## 3. Binding rules and decisions

Own-application composition and state, public binary gRPC-Web, helper-only local RPC, fixed D1 atomic plans, no hidden cross-product dependency. Use existing command/revision/permission/effect/format profiles. All necessary product behavior is fixed in the linked authorities; private helper implementation choices remain within those constraints.

<a id="rule-br-01"></a>
<a id="rule-br-03"></a>
<a id="rule-br-06"></a>

## 4. Projects, directories, files and major types affected

Use the exact projects assigned to this WP in [architecture 27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-26.00"></a>
### WP-26.00 — Application presence

**What must be fully done.** Implement ApplicationService.List/Heartbeat/Disconnect and DO projection of D1 installation authority; separate app rows per device.

**Testing requirements.** 30s expiry/10s renewal, restarted epoch, app offline without device-wide false availability.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-26.01"></a>
### WP-26.01 — Durable target queue

**What must be fully done.** ToolRequest freezes product/device/installation and current instance epoch; commands/receipts remain in D1.

**Testing requirements.** Another application cannot claim; duplicate/lost ack/expiry and per-owner budget.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-26.02"></a>
### WP-26.02 — Owner reauthorization

**What must be fully done.** Device.Runtime invokes registered typed in-process product handlers after current grant/resource/revision/egress checks.

**Testing requirements.** No local product RPC, shared database or delegation through an shared coordinator.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-26.03"></a>
### WP-26.03 — Execution and exact result deduplication

**What must be fully done.** Persist bridge request/result using full ApplicationTarget and `(toolRequestId,attemptId,commandId)` plus result hash. Same attempt may contain several requests; owner handler uses its normal in-process validation.

**Testing requirements.** Multiple tool requests per attempt, identical replay, changed result hash, stale epoch, duplicate delivery and uncertain external effect.

**Completion gate.** No duplicated effect, dropped sibling result or cross-application delivery.

<a id="rule-wp-26.04"></a>
### WP-26.04 — Remote approval and steering

**What must be fully done.** Preserve one-target approvals, sensitive local-presence requirements and ordinary steering bounds.

**Testing requirements.** Mobile biometric cannot substitute for target presence; stale approval fails.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-26.05"></a>
### WP-26.05 — Offline expiry and recovery

**What must be fully done.** Keep explicit offline queue expiry/reconciliation; changing selected app cannot retarget queued work.

**Testing requirements.** Disconnect/revoke/reinstall, no silent alternate product/device selection.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-26.06"></a>
### WP-26.06 — Frozen application locality

**What must be fully done.** Cloud-only steps may run without a desktop; every device step in one execution remains in the frozen product scope.

**Testing requirements.** Own-app multi-tool workflow passes; cross-product capability is absent/future.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-26.90"></a>
### WP-26.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-26.90](#rule-wp-26.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

| Evidence | Produced by |
|---|---|
| Application presence: 30s expiry/10s renewal, restarted epoch, app offline without device-wide false availability. | [WP-26.00](#rule-wp-26.00) |
| Durable target queue: Another application cannot claim; duplicate/lost ack/expiry and per-owner budget. | [WP-26.01](#rule-wp-26.01) |
| Owner reauthorization: No local product RPC, shared database or delegation through an shared coordinator. | [WP-26.02](#rule-wp-26.02) |
| Execution and result: Crash before/after effect, checkpoint, cancel and stale epoch reconciliation. Two distinct tool requests in one attempt both persist; identical `(toolRequestId, attemptId, commandId)`/hash retry returns its receipt and changed hash refuses. | [WP-26.03](#rule-wp-26.03) |
| Remote approval and steering: Mobile biometric cannot substitute for target presence; stale approval fails. | [WP-26.04](#rule-wp-26.04) |
| Offline expiry and recovery: Disconnect/revoke/reinstall, no silent alternate product/device selection. | [WP-26.05](#rule-wp-26.05) |
| Frozen application locality: Own-app multi-tool workflow passes; cross-product capability is absent/future. | [WP-26.06](#rule-wp-26.06) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-26.90](#rule-wp-26.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [DEV.01](../delivery/lanes/device-bridge.md#task-dev-01) | [WP-26.00](26-remote-action-and-tool-bridge.md#rule-wp-26.00) (full) | [CLOUD.13](../delivery/lanes/cloud.md#task-cloud-13) (artifact), [CLOUD.29](../delivery/lanes/cloud.md#task-cloud-29) (artifact), [CON.11](../delivery/lanes/contracts.md#task-con-11) (contract) |
| [DEV.02](../delivery/lanes/device-bridge.md#task-dev-02) | [WP-26.01](26-remote-action-and-tool-bridge.md#rule-wp-26.01) (full) | [CON.10](../delivery/lanes/contracts.md#task-con-10) (contract) |
| [DEV.03](../delivery/lanes/device-bridge.md#task-dev-03) | [WP-26.02](26-remote-action-and-tool-bridge.md#rule-wp-26.02) (full) | [AST.11](../delivery/lanes/assistant.md#task-ast-11) (artifact), [APP.05](../delivery/lanes/app-composition.md#task-app-05) (artifact), [PLT.43](../delivery/lanes/platform.md#task-plt-43) (artifact) |
| [DEV.04](../delivery/lanes/device-bridge.md#task-dev-04) | [WP-26.03](26-remote-action-and-tool-bridge.md#rule-wp-26.03) (Cloud-side D1 attempt-row persistence, hash dedup and cross-application delivery guard) | [CON.10](../delivery/lanes/contracts.md#task-con-10) (contract) |
| [DEV.05](../delivery/lanes/device-bridge.md#task-dev-05) | [WP-26.03](26-remote-action-and-tool-bridge.md#rule-wp-26.03) (Desktop command_log persistence and (toolRequestId,attemptId,commandId) agreement with the Cloud attempt row) | [EXE.01](../delivery/lanes/execution.md#task-exe-01) (artifact) |
| [DEV.06](../delivery/lanes/device-bridge.md#task-dev-06) | [WP-26.04](26-remote-action-and-tool-bridge.md#rule-wp-26.04) (full) | [PLT.39](../delivery/lanes/platform.md#task-plt-39) (artifact) |
| [DEV.07](../delivery/lanes/device-bridge.md#task-dev-07) | [WP-26.05](26-remote-action-and-tool-bridge.md#rule-wp-26.05) (full) | none |
| [DEV.08](../delivery/lanes/device-bridge.md#task-dev-08) | [WP-26.06](26-remote-action-and-tool-bridge.md#rule-wp-26.06) (full) | none |
| [DEV.09](../delivery/lanes/device-bridge.md#task-dev-09) | [WP-26.90](26-remote-action-and-tool-bridge.md#rule-wp-26.90) (full) | none |
| [DEV.12](../delivery/lanes/device-bridge.md#task-dev-12) | [WP-26.03](26-remote-action-and-tool-bridge.md#rule-wp-26.03) (cross-repo agreement proof beyond each side's own unit coverage) | none |

**Consumers outside this package:** [AND.25](../delivery/lanes/android.md#task-and-25), [CLOUD.36](../delivery/lanes/cloud.md#task-cloud-36), [DEV.13](../delivery/lanes/device-bridge.md#task-dev-13), [DEV.14](../delivery/lanes/device-bridge.md#task-dev-14), [HAR.05](../delivery/lanes/harness.md#task-har-05), [SLATE.33](../delivery/lanes/arcslate.md#task-slate-33), [WEB.28](../delivery/lanes/web.md#task-web-28).

<!-- delivery-graph:end -->

