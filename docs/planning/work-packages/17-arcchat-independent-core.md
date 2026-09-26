<a id="rule-wp-17"></a>
# WP-17 — Complete Embedded Assistant and Cloud Client Surface

> Status: Authoritative — [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).
> Repositories: DesktopPlatform. Consume only exact published upstream artifacts; no adjacent sources.

## 1. Scope and purpose

Deliver the complete owned behavior below under the [current project/package plan](../../architecture/27-platform-projects-and-application-assistants.md). Professional product semantics, security, exact values and recovery requirements remain binding. A completed Hello World or fixture cannot substitute for the listed production capability.

## 2. Required inputs and dependencies

[Producer registry](../producer-artifacts-and-integration.md), [wire registry](../../architecture/contracts/04-protobuf-wire-registry.md), [application/protocol profile](../../architecture/contracts/10-application-scope-and-streams.md), [D1 execution](../../architecture/data-model/04-d1-execution-profile.md), [history](../../architecture/data-model/05-application-history.md), [experience/acceptance](../../experience/README.md) and exact artifacts from the upstream WPs above. Later domain/AI fixtures are allowed only where explicitly named below and must be removed at their owning real integration gate.

## 3. Binding rules and decisions

Own-application composition and state, public binary gRPC-Web, helper-only local RPC, fixed D1 atomic plans, no hidden cross-product dependency. Use existing command/revision/permission/effect/format profiles. All necessary product behavior is fixed in the linked authorities; private helper implementation choices remain within those constraints.

<a id="rule-br-05"></a>
<a id="rule-wp-17.08"></a>
<a id="rule-wp-17.09"></a>

## 4. Projects, directories, files and major types affected

Use the exact projects assigned to this WP in [architecture 27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-17.00"></a>
### WP-17.00 — Complete assistant navigation

**What must be fully done.** Implement all AS01–AS13 docked/floating/expanded surfaces and architecture 27 AssistantHost API. Same code composes independently into each product.

**Testing requirements.** All actions reachable at minimum size; window/draft/account/keyboard/accessibility matrix.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-17.01"></a>
### WP-17.01 — Cloud client and device runtime

**What must be fully done.** Implement reusable Cloud.Client/Device.Runtime session/event/output/upload and own-app typed dispatch adapters. Use named future-owner fixtures only until 23–26/52.

**Testing requirements.** Generated gRPC-Web calls/typed states; fixture manifest names each replacement producer.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-17.02"></a>
### WP-17.02 — Security and approval surface

**What must be fully done.** Implement AS06/11/12 with actor/target/context/egress/cost/expiry and local-presence escalation.

**Testing requirements.** No persistent allow-all or cross-product grant; stale approval refused.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-17.03"></a>
### WP-17.03 — Task centre

**What must be fully done.** Implement task timeline, tools, artifacts, cancellation/steering and ProductJob links with effect certainty.

**Testing requirements.** Canceled/interrupted/unknown/complete distinguishable; closing view does not cancel.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-17.04"></a>
### WP-17.04 — Automation client

**What must be fully done.** Implement existing Cloud-owned rule/occurrence UI, schedule/timezone/target/budget and action availability.

**Testing requirements.** Offline edits remain drafts and do not imply local scheduling.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-17.05"></a>
### WP-17.05 — History and AI admission

**What must be fully done.** Implement local/cloud/temporary disclosure, mode selection, Cloud promotion/copy UI and real local lifecycle with named Cloud fixtures.

**Testing requirements.** No implicit upload; denied admission/credit consent and transient output recovery states.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-17.06"></a>
### WP-17.06 — Preview and host context

**What must be fully done.** Implement AS03/08 own-app selection/preview/navigation using frozen host ports and safe fallback for unsupported native preview.

**Testing requirements.** No live-selection mutation, no another-product destination, citations/resources keep ownership.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-17.07"></a>
### WP-17.07 — Complete package acceptance

**What must be fully done.** Publish Assistant.Avalonia/Core/Sqlite/Cloud candidates; clean AOT host consumes only required packages, all accepted assistant capabilities mapped.

**Testing requirements.** UX-A/B/C/H pass locally; real Cloud/AI fixtures remain explicit and close at 26/52, not here.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-17.90"></a>
### WP-17.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Complete assistant navigation: All actions reachable at minimum size; window/draft/account/keyboard/accessibility matrix. | [WP-17.00](#rule-wp-17.00) |
| Cloud client and device runtime: Generated gRPC-Web calls/typed states; fixture manifest names each replacement producer. | [WP-17.01](#rule-wp-17.01) |
| Security and approval surface: No persistent allow-all or cross-product grant; stale approval refused. | [WP-17.02](#rule-wp-17.02) |
| Task centre: Canceled/interrupted/unknown/complete distinguishable; closing view does not cancel. | [WP-17.03](#rule-wp-17.03) |
| Automation client: Offline edits remain drafts and do not imply local scheduling. | [WP-17.04](#rule-wp-17.04) |
| History and AI admission: No implicit upload; denied admission/credit consent and transient output recovery states. | [WP-17.05](#rule-wp-17.05) |
| Preview and host context: No live-selection mutation, no another-product destination, citations/resources keep ownership. | [WP-17.06](#rule-wp-17.06) |
| Complete package acceptance: UX-A/B/C/H pass locally; real Cloud/AI fixtures remain explicit and close at 26/52, not here. | [WP-17.07](#rule-wp-17.07) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-17.90](#rule-wp-17.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [AST.10](../delivery/lanes/assistant.md#task-ast-10) | [WP-17.00](17-arcchat-independent-core.md#rule-wp-17.00) (full) | [EXE.01](../delivery/lanes/execution.md#task-exe-01) (artifact), [AST.01](../delivery/lanes/assistant.md#task-ast-01) (artifact), [AST.02](../delivery/lanes/assistant.md#task-ast-02) (artifact), [AST.04](../delivery/lanes/assistant.md#task-ast-04) (artifact), [AST.05](../delivery/lanes/assistant.md#task-ast-05) (artifact), [AST.06](../delivery/lanes/assistant.md#task-ast-06) (artifact), [AST.07](../delivery/lanes/assistant.md#task-ast-07) (artifact) |
| [AST.11](../delivery/lanes/assistant.md#task-ast-11) | [WP-17.01](17-arcchat-independent-core.md#rule-wp-17.01) (full) | [CON.10](../delivery/lanes/contracts.md#task-con-10) (contract), [PRF.05](../delivery/lanes/runtime-proofs.md#task-prf-05) (artifact), [AST.01](../delivery/lanes/assistant.md#task-ast-01) (artifact) |
| [AST.12](../delivery/lanes/assistant.md#task-ast-12) | [WP-17.02](17-arcchat-independent-core.md#rule-wp-17.02) (full) | [APP.05](../delivery/lanes/app-composition.md#task-app-05) (artifact), [PLT.39](../delivery/lanes/platform.md#task-plt-39) (artifact) |
| [AST.13](../delivery/lanes/assistant.md#task-ast-13) | [WP-17.03](17-arcchat-independent-core.md#rule-wp-17.03) (full) | [EXE.01](../delivery/lanes/execution.md#task-exe-01) (artifact), [EXE.05](../delivery/lanes/execution.md#task-exe-05) (artifact) |
| [AST.14](../delivery/lanes/assistant.md#task-ast-14) | [WP-17.04](17-arcchat-independent-core.md#rule-wp-17.04) (full) | [CON.10](../delivery/lanes/contracts.md#task-con-10) (contract) |
| [AST.15](../delivery/lanes/assistant.md#task-ast-15) | [WP-17.05](17-arcchat-independent-core.md#rule-wp-17.05) (full) | [AST.07](../delivery/lanes/assistant.md#task-ast-07) (artifact) |
| [AST.16](../delivery/lanes/assistant.md#task-ast-16) | [WP-17.06](17-arcchat-independent-core.md#rule-wp-17.06) (full) | [APP.06](../delivery/lanes/app-composition.md#task-app-06) (artifact) |
| [AST.17](../delivery/lanes/assistant.md#task-ast-17) | [WP-17.07](17-arcchat-independent-core.md#rule-wp-17.07) (full) | none |
| [AST.18](../delivery/lanes/assistant.md#task-ast-18) | [WP-17.90](17-arcchat-independent-core.md#rule-wp-17.90) (full) | none |

**Consumers outside this package:** [AIR.08](../delivery/lanes/ai-routing.md#task-air-08), [AST.19](../delivery/lanes/assistant.md#task-ast-19), [AST.20](../delivery/lanes/assistant.md#task-ast-20), [AST.22](../delivery/lanes/assistant.md#task-ast-22), [DEV.03](../delivery/lanes/device-bridge.md#task-dev-03), [DEV.14](../delivery/lanes/device-bridge.md#task-dev-14), [HAR.03](../delivery/lanes/harness.md#task-har-03), [HAR.05](../delivery/lanes/harness.md#task-har-05), [SCOPE.20](../delivery/lanes/arcscope.md#task-scope-20), [SCOPE.21](../delivery/lanes/arcscope.md#task-scope-21).

<!-- delivery-graph:end -->

