<a id="rule-wp-08"></a>
# WP-08 — Private Helper gRPC and Parent Registration

> Status: Authoritative — [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).
> Repositories: DesktopPlatform. Consume only exact published upstream artifacts; no adjacent sources.

## 1. Scope and purpose

Deliver the complete owned behavior below under the [current project/package plan](../../architecture/27-platform-projects-and-application-assistants.md). Professional product semantics, security, exact values and recovery requirements remain binding. A completed Hello World or fixture cannot substitute for the listed production capability.

## 2. Required inputs and dependencies

[Producer registry](../producer-artifacts-and-integration.md), [wire registry](../../architecture/contracts/04-protobuf-wire-registry.md), [application/protocol profile](../../architecture/contracts/10-application-scope-and-streams.md), [D1 execution](../../architecture/data-model/04-d1-execution-profile.md), [history](../../architecture/data-model/05-application-history.md), [experience/acceptance](../../experience/README.md) and exact artifacts from the upstream WPs above. Later domain/AI fixtures are allowed only where explicitly named below and must be removed at their owning real integration gate.

## 3. Binding rules and decisions

Own-application composition and state, public binary gRPC-Web, helper-only local RPC, fixed D1 atomic plans, no hidden cross-product dependency. Use existing command/revision/permission/effect/format profiles. All necessary product behavior is fixed in the linked authorities; private helper implementation choices remain within those constraints.

<a id="rule-br-01"></a>
<a id="rule-br-03"></a>
<a id="rule-br-09"></a>
<a id="rule-br-10"></a>

## 4. Projects, directories, files and major types affected

Use the exact projects assigned to this WP in [architecture 27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-08.00"></a>
### WP-08.00 — Transport and framing

**What must be fully done.** Implement generated gRPC HTTP/2 over Windows Named Pipe/Unix domain socket for parent-owned helper/extension children; no product listener or global discovery. Use explicit registration and AOT-safe serialization.

**Testing requirements.** Actual OS streams, malformed frames, wrong-user denial and no local TCP listener.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-08.01"></a>
### WP-08.01 — Parent-owned endpoint identity

**What must be fully done.** Parent launch descriptor fixes endpoint, process/build/protocol, nonce and epoch; atomically create/remove owner-only endpoint files. A stale descriptor never authorizes a child.

**Testing requirements.** Concurrent launch, stale descriptor, forged nonce/build and parent-death cleanup.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-08.02"></a>
### WP-08.02 — Child registration lifecycle

**What must be fully done.** Authenticate LocalBootstrap; keep30s lease/10s renewal, epoch fencing and restartable restricted launch. No owning professional application process or peer application registry.

**Testing requirements.** Expired/stale child cannot call; parent restart requires fresh grants.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-08.03"></a>
### WP-08.03 — Static routing and version refusal

**What must be fully done.** Resolve only explicitly launched children and their declared generated services. Reject unsupported version/capability; never select an installed product as fallback.

**Testing requirements.** Version mismatch and unregistered service refusal.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-08.04"></a>
### WP-08.04 — Bounds and concurrency

**What must be fully done.** Retain 16 active/64 queued bounded calls, deadlines and parent-owned callback channels; no recursive saturated callback lane.

**Testing requirements.** Queue/memory bound, fairness, timeout and typed overload.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-08.05"></a>
### WP-08.05 — Disconnect/cancel/retry

**What must be fully done.** Preserve effect certainty, stable command/receipt and cancellation across helper crashes; replay only when allowed.

**Testing requirements.** Kill before/after commit, lost ack and unknown effect.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-08.06"></a>
### WP-08.06 — Brokered large data

**What must be fully done.** Use annex 09 sandbox resources/buffers and bounded verified chunks, parent-authorized only. No direct product-to-product transfer ticket.

**Testing requirements.** Wrong resource grant, range/hash/expiry/cancel and orphan cleanup.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-08.90"></a>
### WP-08.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Transport and framing: Actual OS streams, malformed frames, wrong-user denial and no local TCP listener. | [WP-08.00](#rule-wp-08.00) |
| Parent-owned endpoint identity: Concurrent launch, stale descriptor, forged nonce/build and parent-death cleanup. | [WP-08.01](#rule-wp-08.01) |
| Child registration lifecycle: Expired/stale child cannot call; parent restart requires fresh grants. | [WP-08.02](#rule-wp-08.02) |
| Static routing and version refusal: Version mismatch and unregistered service refusal. | [WP-08.03](#rule-wp-08.03) |
| Bounds and concurrency: Queue/memory bound, fairness, timeout and typed overload. | [WP-08.04](#rule-wp-08.04) |
| Disconnect/cancel/retry: Kill before/after commit, lost ack and unknown effect. | [WP-08.05](#rule-wp-08.05) |
| Brokered large data: Wrong resource grant, range/hash/expiry/cancel and orphan cleanup. | [WP-08.06](#rule-wp-08.06) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-08.90](#rule-wp-08.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [PLT.09](../delivery/lanes/platform.md#task-plt-09) | [WP-08.00](08-local-ipc-and-registration.md#rule-wp-08.00) (full)<br>[WP-08](08-local-ipc-and-registration.md#rule-wp-08) No product listener/global discovery - structural constraint on every substep, most directly tested by transport/registration (package-level obligation contribution) | [PRF.04](../delivery/lanes/runtime-proofs.md#task-prf-04) (artifact), [CON.04](../delivery/lanes/contracts.md#task-con-04) (contract) |
| [PLT.10](../delivery/lanes/platform.md#task-plt-10) | [WP-08.01](08-local-ipc-and-registration.md#rule-wp-08.01) (full) | none |
| [PLT.11](../delivery/lanes/platform.md#task-plt-11) | [WP-08.02](08-local-ipc-and-registration.md#rule-wp-08.02) (full)<br>[WP-08](08-local-ipc-and-registration.md#rule-wp-08) No product listener/global discovery - structural constraint on every substep, most directly tested by transport/registration (package-level obligation contribution) | none |
| [PLT.12](../delivery/lanes/platform.md#task-plt-12) | [WP-08.03](08-local-ipc-and-registration.md#rule-wp-08.03) (full) | none |
| [PLT.13](../delivery/lanes/platform.md#task-plt-13) | [WP-08.04](08-local-ipc-and-registration.md#rule-wp-08.04) (full) | none |
| [PLT.14](../delivery/lanes/platform.md#task-plt-14) | [WP-08.05](08-local-ipc-and-registration.md#rule-wp-08.05) (full) | [FND.02](../delivery/lanes/foundation.md#task-fnd-02) (artifact) |
| [PLT.15](../delivery/lanes/platform.md#task-plt-15) | [WP-08.06](08-local-ipc-and-registration.md#rule-wp-08.06) (full) | [CON.04](../delivery/lanes/contracts.md#task-con-04) (contract) |
| [PLT.16](../delivery/lanes/platform.md#task-plt-16) | [WP-08.90](08-local-ipc-and-registration.md#rule-wp-08.90) (full) | none |

**Consumers outside this package:** [NAT.01](../delivery/lanes/native.md#task-nat-01), [PLT.24](../delivery/lanes/platform.md#task-plt-24), [PLT.38](../delivery/lanes/platform.md#task-plt-38), [PLT.45](../delivery/lanes/platform.md#task-plt-45).

<!-- delivery-graph:end -->

