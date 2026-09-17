<a id="rule-wp-21"></a>
# WP-21 — Cloudflare Container, D1 Authority and Binding Plans

> Status: Authoritative — P2-012
> Upstream: `03` · `05` · `12` · Downstream: `22` · `45` · `51` · `52`
> Repositories: Cloud. Consume only exact published upstream artifacts; no adjacent sources.

## 1. Scope and purpose

Deliver the complete owned behavior below under the [current project/package plan](../../architecture/27-platform-projects-and-application-assistants.md). Professional product semantics, security, exact values and recovery requirements remain binding. A completed Hello World or fixture cannot substitute for the listed production capability.

## 2. Required inputs and dependencies

[Producer registry](../producer-artifacts-and-integration.md), [wire registry](../../architecture/contracts/04-protobuf-wire-registry.md), [application/protocol profile](../../architecture/contracts/10-application-scope-and-streams.md), [D1 execution](../../architecture/data-model/04-d1-execution-profile.md), [history](../../architecture/data-model/05-application-history.md), [experience/acceptance](../../experience/README.md) and exact artifacts from the upstream WPs above. Later domain/AI fixtures are allowed only where explicitly named below and must be removed at their owning real integration gate.

## 3. Binding rules and decisions

Own-application composition and state, public binary gRPC-Web, helper-only local RPC, fixed D1 atomic plans, no hidden cross-product dependency. Use existing command/revision/permission/effect/format profiles. All necessary product behavior is fixed in the linked authorities; private helper implementation choices remain within those constraints.


## 4. Projects, directories, files and major types affected

Use the exact projects assigned to this WP in [architecture27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-21.00"></a>
### WP-21.00 — Ingress and host pipeline

**What must be fully done.** Implement Worker /api routing, C# AOT gRPC-Web/auth/current owner pipeline and bounded cold starts in the actual Container image.

**Testing requirements.** Deployed request/stream/cancel/CSRF/trailer path; no buffered stream or direct public Container port.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.01"></a>
### WP-21.01 — Finite durable jobs

**What must be fully done.** Replace perpetual hosted loops with Cron/Queue/Workflow-woken C# endpoints; ≤100items/20s per job, checkpoint/receipt/lease then yield.

**Testing requirements.** Sleep/restart, duplicate wake, delayed delivery, stale lease and paused simulator continuation.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.02"></a>
### WP-21.02 — Twenty module boundaries

**What must be fully done.** Implement exact module projects and D1 named-plan bridge; C# owns business decisions, Worker executes approved SQL only.

**Testing requirements.** Architecture/import/plan-hash/wrong-container/public-access refusal tests.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.03"></a>
### WP-21.03 — D1 migration and exact physical mapping

**What must be fully done.** Implement model04 full physical manifest, migrations, typed exact bind/result adapters and expand/backfill/fenced cutover.

**Testing requirements.** Actual D1 signed64/uint64/decimal/JSON/FTS5, interrupted migration, stale backfill and compatible rollback.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.04"></a>
### WP-21.04 — Receipts/outbox/archive

**What must be fully done.** Implement atomic guards plus owner writes/receipt/outbox/change archive, inbox dedup and contiguous publication.

**Testing requirements.** Constraint guard failure rolls back all rows; zero-row CAS cannot publish; duplicate/lost ack reconciles.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.05"></a>
### WP-21.05 — Shared atomic families and claims

**What must be fully done.** Implement every model00 shared transaction family as one fixed D1 batch, including authorization/revision/policy/balance/lease guards.

**Testing requirements.** Two Containers contend, stale holder cannot finalize, exact credits and sync cursor safety.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.06"></a>
### WP-21.06 — Configuration and capacity

**What must be fully done.** Implement fixed plan/config/generation checks, primary reads, bounded binding calls, D1 capacity headroom/admission and observability.

**Testing requirements.** 10GB boundary not falsely raised; overload/cold-start/current-session failures explicit.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.07"></a>
### WP-21.07 — Failure isolation and readiness

**What must be fully done.** Expose ingress/Container/D1/DO/R2/Queue health separately and preserve no-content logs.

**Testing requirements.** Missing binding/plan mismatch fails readiness, not successful partial execution.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.90"></a>
### WP-21.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Ingress and host pipeline: Deployed request/stream/cancel/CSRF/trailer path; no buffered stream or direct public Container port. | [WP-21.00](#rule-wp-21.00) |
| Finite durable jobs: Sleep/restart, duplicate wake, delayed delivery, stale lease and paused simulator continuation. | [WP-21.01](#rule-wp-21.01) |
| Twenty module boundaries: Architecture/import/plan-hash/wrong-container/public-access refusal tests. | [WP-21.02](#rule-wp-21.02) |
| D1 migration and exact physical mapping: Actual D1 signed64/uint64/decimal/JSON/FTS5, interrupted migration, stale backfill and compatible rollback. | [WP-21.03](#rule-wp-21.03) |
| Receipts/outbox/archive: Constraint guard failure rolls back all rows; zero-row CAS cannot publish; duplicate/lost ack reconciles. | [WP-21.04](#rule-wp-21.04) |
| Shared atomic families and claims: Two Containers contend, stale holder cannot finalize, exact credits and sync cursor safety. | [WP-21.05](#rule-wp-21.05) |
| Configuration and capacity: 10GB boundary not falsely raised; overload/cold-start/current-session failures explicit. | [WP-21.06](#rule-wp-21.06) |
| Failure isolation and readiness: Missing binding/plan mismatch fails readiness, not successful partial execution. | [WP-21.07](#rule-wp-21.07) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-21.90](#rule-wp-21.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

**Upstream:** `03` · `05` · `12`. Consume completed stage outputs.

**Downstream:** `22` · `45` · `51` · `52`. Consumers use exact released artifacts.
