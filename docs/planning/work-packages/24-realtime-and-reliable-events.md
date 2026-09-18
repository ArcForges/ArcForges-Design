<a id="rule-wp-24"></a>
# WP-24 — gRPC-Web Streams and Durable Event Recovery

> Status: Authoritative — P2-012
> Upstream: `23` · Downstream: `25` · `26` · `30`
> Repositories: Cloud + DesktopPlatform + Contracts. Consume only exact published upstream artifacts; no adjacent sources.

## 1. Scope and purpose

Deliver the complete owned behavior below under the [current project/package plan](../../architecture/27-platform-projects-and-application-assistants.md). Professional product semantics, security, exact values and recovery requirements remain binding. A completed Hello World or fixture cannot substitute for the listed production capability.

## 2. Required inputs and dependencies

[Producer registry](../producer-artifacts-and-integration.md), [wire registry](../../architecture/contracts/04-protobuf-wire-registry.md), [application/protocol profile](../../architecture/contracts/10-application-scope-and-streams.md), [D1 execution](../../architecture/data-model/04-d1-execution-profile.md), [history](../../architecture/data-model/05-application-history.md), [experience/acceptance](../../experience/README.md) and exact artifacts from the upstream WPs above. Later domain/AI fixtures are allowed only where explicitly named below and must be removed at their owning real integration gate.

## 3. Binding rules and decisions

Own-application composition and state, public binary gRPC-Web, helper-only local RPC, fixed D1 atomic plans, no hidden cross-product dependency. Use existing command/revision/permission/effect/format profiles. All necessary product behavior is fixed in the linked authorities; private helper implementation choices remain within those constraints.

<a id="rule-br-02"></a>

## 4. Projects, directories, files and major types affected

Use the exact projects assigned to this WP in [architecture 27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-24.00"></a>
### WP-24.00 — Connection and authentication

**What must be fully done.** Implement EventService.Watch and ExecutionService.WatchOutput public server-streaming shells with generated StreamFrame; current session/scope authorization every 15s.

**Testing requirements.** Real C#/browser/Kotlin binary streams, trailers/cancel/expiry and no WebSocket path.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-24.01"></a>
### WP-24.01 — Scoped subscription

**What must be fully done.** Bind feed to owner/product/filter/recovery generation, one events/two output streams per foreground profile.

**Testing requirements.** Mixed-product/unauthorized feed refused; account-security identifiers separate.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-24.02"></a>
### WP-24.02 — Cursor and gap handling

**What must be fully done.** Keep sequence/hash/offset and snapshot high-water recovery from annex 10; DO is projection backed by D1 outbox.

**Testing requirements.** Duplicate/conflicting frames, expired cursor, deleted DO and revision replay.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-24.03"></a>
### WP-24.03 — Durable unary fallback

**What must be fully done.** Implement Poll/readOutput with the same owner/cursor profile; replace old HTTP task stream endpoint. AI terminal bodies arrive at 52.

**Testing requirements.** Blocked stream recovers through real unary read without invented completion.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-24.04"></a>
### WP-24.04 — Publication and wake

**What must be fully done.** Publish D1 committed outbox into bounded DO feed; wake hints via Queues, no business ownership in DO.

**Testing requirements.** Contiguous watermark, no skipped commit, duplicate queue event safe.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-24.05"></a>
### WP-24.05 — Bounded lifecycle

**What must be fully done.** 5min stream,15s heartbeat,45s silence, bounded jitter/queue; Android background closes streams and later refetches.

**Testing requirements.** Slow reader overflow resets, no unbounded memory or hibernation-cost claim.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-24.06"></a>
### WP-24.06 — Reusable consumer adapters

**What must be fully done.** Publish Platform Cloud.Client and Contracts TS/Kotlin stream fixtures; expose typed lifecycle states, no UI-specific transport logic.

**Testing requirements.** Clean generated-client consumers and real deployed C# ownership paths.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-24.90"></a>
### WP-24.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

**Tool-result acceptance.** Submit two distinct toolRequestIds in one attempt (for both Task and ChatTurn owners), then replay each original command/hash: both results persist and each replay returns its own original receipt. A changed result under the same `(toolRequestId, attemptId, commandId)` refuses with `command.reused_identifier`; lost acknowledgement never allocates a fresh command or drops the second result. Bind the wire registry, TK-05 and `task.tool_result` to this same key.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Connection and authentication: Real C#/browser/Kotlin binary streams, trailers/cancel/expiry and no WebSocket path. | [WP-24.00](#rule-wp-24.00) |
| Scoped subscription: Mixed-product/unauthorized feed refused; account-security identifiers separate. | [WP-24.01](#rule-wp-24.01) |
| Cursor and gap handling: Duplicate/conflicting frames, expired cursor, deleted DO and revision replay. | [WP-24.02](#rule-wp-24.02) |
| Durable unary fallback: Blocked stream recovers through real unary read without invented completion. | [WP-24.03](#rule-wp-24.03) |
| Publication and wake: Contiguous watermark, no skipped commit, duplicate queue event safe. | [WP-24.04](#rule-wp-24.04) |
| Bounded lifecycle: Slow reader overflow resets, no unbounded memory or hibernation-cost claim. | [WP-24.05](#rule-wp-24.05) |
| Reusable consumer adapters: Clean generated-client consumers and real deployed C# ownership paths. | [WP-24.06](#rule-wp-24.06) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-24.90](#rule-wp-24.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

**Upstream:** `23`. Consume completed stage outputs.

**Downstream:** `25` · `26` · `30`. Consumers use exact released artifacts.
