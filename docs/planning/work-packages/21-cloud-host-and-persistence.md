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

Use the exact projects assigned to this WP in [architecture 27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-21.00"></a>
### WP-21.00 — Ingress and host pipeline

**What must be fully done.** Implement Worker /api routing, C# AOT gRPC-Web/auth/current owner pipeline and bounded cold starts in the actual Container image.

**Testing requirements.** Deployed request/stream/cancel/CSRF/trailer path; no buffered stream or direct public Container port.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.01"></a>
### WP-21.01 — Finite durable jobs

**What must be fully done.** Replace perpetual hosted loops with Cron/Queue/Workflow-woken C# endpoints; ≤100 items/20s per job, checkpoint/receipt/lease then yield.

**Testing requirements.** Sleep/restart, duplicate wake, delayed delivery, stale lease and paused simulator continuation.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.02"></a>
### WP-21.02 — Twenty-one module boundaries

**What must be fully done.** Implement exact module projects and D1 named-plan bridge; C# owns business decisions, Worker executes approved SQL only.

**Testing requirements.** Architecture/import/plan-hash/wrong-container/public-access refusal tests.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.03"></a>
### WP-21.03 — D1 migration and exact physical mapping

**What must be fully done.** Implement model 04 full physical manifest, migrations, typed exact bind/result adapters and expand/backfill/fenced cutover.

**Testing requirements.** Actual D1 signed 64/uint64/decimal/JSON/FTS5, interrupted migration, stale backfill and compatible rollback.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.04"></a>
### WP-21.04 — Receipts/outbox/archive

**What must be fully done.** Implement atomic guards plus owner writes/receipt/outbox/change archive, inbox dedup and contiguous publication.

**Testing requirements.** Constraint guard failure rolls back all rows; zero-row CAS cannot publish; duplicate/lost ack reconciles.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.05"></a>
### WP-21.05 — Shared atomic families and claims

**What must be fully done.** Implement every model 00 shared transaction family as one fixed D1 batch, including authorization/revision/policy/balance/lease guards.

**Testing requirements.** Two Containers contend, stale holder cannot finalize, exact credits and sync cursor safety.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.06"></a>
### WP-21.06 — Capacity and Container/D1 integration producer

**What must be fully done.** Implement model 04 named plans, guarded batch fixtures, primary authorization, route/service-binding/outbound-handler matrix, job slice and SimulationPacer infrastructure. Produce L-16 measurement harness/config and proposed capacity report.

**Testing requirements.** Real D1 rollback/duplicate/competing-writer/cold-start tests; public /internal denial, blocked egress, forged service headers, stream limits and headroom measurement.

**Completion gate.** Real deployed storage/ingress works; proposed launch envelope approval/load evidence remains explicitly open until WP50, not closed by SQLite.

<a id="rule-wp-21.07"></a>
### WP-21.07 — Failure isolation and readiness

**What must be fully done.** Expose ingress/Container/D1/DO/R2/Queue health separately and preserve no-content logs.

**Testing requirements.** Missing binding/plan mismatch fails readiness, not successful partial execution.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-21.08"></a>

### WP-21.08 — Selfhost.v1 deployment profile

**What must be fully done.** Produce operator-owned CF deployment/config/realm descriptor and health validation using deployment 22. Default payment disabled, separate keys/identity/providers; preserve immutable artifacts and independent backup requirements.

**Testing requirements.** Fresh development account/realm provisioning, missing binding/secret/unsupported descriptor/redirect failures and no official token acceptance.

**Completion gate.** WP46 receives a runnable deployment and complete configuration inventory; production PG-25 remains external evidence.

<a id="rule-wp-21.90"></a>
### WP-21.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

**Launch configuration acceptance.** Produce the exact model04 launch-capacity.v1 and deployed Worker/Container identity. Test four fixed standard-2 slots, no per-account instance creation, idle sleep/wake, pre-dispatch refusal versus unknown dispatched outcome, control-slot reserve and Vectorize/R2 reservation thresholds. Record cold-start and measured cost inputs; a localhost benchmark cannot close PG-26.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and WP-21.90 evidence. Current P2-013 contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

| Evidence | Produced by |
|---|---|
| Ingress and host pipeline: Deployed request/stream/cancel/CSRF/trailer path; no buffered stream or direct public Container port. | [WP-21.00](#rule-wp-21.00) |
| Finite durable jobs: Sleep/restart, duplicate wake, delayed delivery, stale lease and paused simulator continuation. | [WP-21.01](#rule-wp-21.01) |
| Twenty-one module boundaries: Architecture/import/plan-hash/wrong-container/public-access refusal tests. | [WP-21.02](#rule-wp-21.02) |
| D1 migration and exact physical mapping: Actual D1 signed 64/uint64/decimal/JSON/FTS5, interrupted migration, stale backfill and compatible rollback. | [WP-21.03](#rule-wp-21.03) |
| Receipts/outbox/archive: Constraint guard failure rolls back all rows; zero-row CAS cannot publish; duplicate/lost ack reconciles. | [WP-21.04](#rule-wp-21.04) |
| Shared atomic families and claims: Two Containers contend, stale holder cannot finalize, exact credits and sync cursor safety. | [WP-21.05](#rule-wp-21.05) |
| Configuration and capacity: 10 GB boundary not falsely raised; overload/cold-start/current-session failures explicit. | [WP-21.06](#rule-wp-21.06) |
| Failure isolation and readiness: Missing binding/plan mismatch fails readiness, not successful partial execution. | [WP-21.07](#rule-wp-21.07) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-21.90](#rule-wp-21.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

**Upstream:** `03` · `05` · `12`. Consume completed stage outputs.

**Downstream:** `22` · `45` · `51` · `52`. Consumers use exact released artifacts.
