<a id="rule-wp-46"></a>
# WP-46 — D1, R2 and Independent Disaster Recovery

> Status: Authoritative — P2-012
> Upstream: `25` · `45` · Downstream: `48` · `50`
> Repositories: Cloud + AI + Web. Consume only exact published upstream artifacts; no adjacent sources.

## 1. Scope and purpose

Deliver the complete owned behavior below under the [current project/package plan](../../architecture/27-platform-projects-and-application-assistants.md). Professional product semantics, security, exact values and recovery requirements remain binding. A completed Hello World or fixture cannot substitute for the listed production capability.

## 2. Required inputs and dependencies

[Producer registry](../producer-artifacts-and-integration.md), [wire registry](../../architecture/contracts/04-protobuf-wire-registry.md), [application/protocol profile](../../architecture/contracts/10-application-scope-and-streams.md), [D1 execution](../../architecture/data-model/04-d1-execution-profile.md), [history](../../architecture/data-model/05-application-history.md), [experience/acceptance](../../experience/README.md) and exact artifacts from the upstream WPs above. Later domain/AI fixtures are allowed only where explicitly named below and must be removed at their owning real integration gate.

## 3. Binding rules and decisions

Own-application composition and state, public binary gRPC-Web, helper-only local RPC, fixed D1 atomic plans, no hidden cross-product dependency. Use existing command/revision/permission/effect/format profiles. All necessary product behavior is fixed in the linked authorities; private helper implementation choices remain within those constraints.

<a id="rule-br-08"></a>

## 4. Projects, directories, files and major types affected

Use the exact projects assigned to this WP in [architecture27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-46.00"></a>
### WP-46.00 — Backup layers

**What must be fully done.** Implement local canonical backup, D1 Time Travel/export/change archive, R2 objects and independent S3 COMPLIANCE copy under model04.

**Testing requirements.** RPO5min metadata/15min objects measured; no WAL tooling or same-provider-only substitute.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-46.01"></a>
### WP-46.01 — Point-in-time and fresh restore

**What must be fully done.** Verify base bookmark/sequence and contiguous after-image archive; in-place Time Travel and fresh import/replay both use generation fences.

**Testing requirements.** Missing archive/object, partial export and unsafe reopen refusal.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-46.02"></a>
### WP-46.02 — Fresh environment rebuild

**What must be fully done.** Fence old ingress/keys, restore D1/R2, replay independent restrictive safety journal, invalidate credentials/leases/cursors, reconcile external effects.

**Testing requirements.** Deleted/revoked account cannot reappear and absent attempt cannot execute twice.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-46.03"></a>
### WP-46.03 — Drill programme

**What must be fully done.** Run actual Container/Worker/DO/R2/D1 restore using separate credentials and immutable archive; then combined AI reopen at50/52.

**Testing requirements.** RTO≤4h with real evidence, not SQLite/simulator-only restore.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-46.04"></a>
### WP-46.04 — Data health

**What must be fully done.** Expose archive watermark, capacity, canonical refs/hash/pins, derived rebuild and backup lag/admission state.

**Testing requirements.** 4min/12min warning guard and exceeded-objective incident visible.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-46.05"></a>
### WP-46.05 — Export and realm migration

**What must be fully done.** Implement existing explicit realm export/import semantics using compatible D1 physical/schema/plan manifests; no automatic cross-DB transaction.

**Testing requirements.** Identity/resource/history scope preserved and unsupported mapping refused.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-46.06"></a>
### WP-46.06 — Backup release gate

**What must be fully done.** Require verified independent backup and safety journal before paid production admission.

**Testing requirements.** No unverified restore, private access or mutation reopens on incomplete inventory.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-46.90"></a>
### WP-46.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Backup layers: RPO5min metadata/15min objects measured; no WAL tooling or same-provider-only substitute. | [WP-46.00](#rule-wp-46.00) |
| Point-in-time and fresh restore: Missing archive/object, partial export and unsafe reopen refusal. | [WP-46.01](#rule-wp-46.01) |
| Fresh environment rebuild: Deleted/revoked account cannot reappear and absent attempt cannot execute twice. | [WP-46.02](#rule-wp-46.02) |
| Drill programme: RTO≤4h with real evidence, not SQLite/simulator-only restore. | [WP-46.03](#rule-wp-46.03) |
| Data health: 4min/12min warning guard and exceeded-objective incident visible. | [WP-46.04](#rule-wp-46.04) |
| Export and realm migration: Identity/resource/history scope preserved and unsupported mapping refused. | [WP-46.05](#rule-wp-46.05) |
| Backup release gate: No unverified restore, private access or mutation reopens on incomplete inventory. | [WP-46.06](#rule-wp-46.06) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-46.90](#rule-wp-46.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

**Upstream:** `25` · `45`. Consume completed stage outputs.

**Downstream:** `48` · `50`. Consumers use exact released artifacts.
