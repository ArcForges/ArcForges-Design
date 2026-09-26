<a id="rule-wp-15"></a>
# WP-15 — Application Assistant Conversation, History and Project Packages

> Status: Authoritative — [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).
> Repositories: DesktopPlatform. Consume only exact published upstream artifacts; no adjacent sources.

## 1. Scope and purpose

Deliver the complete owned behavior below under the [current project/package plan](../../architecture/27-platform-projects-and-application-assistants.md). Professional product semantics, security, exact values and recovery requirements remain binding. A completed Hello World or fixture cannot substitute for the listed production capability.

## 2. Required inputs and dependencies

[Producer registry](../producer-artifacts-and-integration.md), [wire registry](../../architecture/contracts/04-protobuf-wire-registry.md), [application/protocol profile](../../architecture/contracts/10-application-scope-and-streams.md), [D1 execution](../../architecture/data-model/04-d1-execution-profile.md), [history](../../architecture/data-model/05-application-history.md), [experience/acceptance](../../experience/README.md) and exact artifacts from the upstream WPs above. Later domain/AI fixtures are allowed only where explicitly named below and must be removed at their owning real integration gate.

## 3. Binding rules and decisions

Own-application composition and state, public binary gRPC-Web, helper-only local RPC, fixed D1 atomic plans, no hidden cross-product dependency. Use existing command/revision/permission/effect/format profiles. All necessary product behavior is fixed in the linked authorities; private helper implementation choices remain within those constraints.


## 4. Projects, directories, files and major types affected

Use the exact projects assigned to this WP in [architecture 27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-15.00"></a>
### WP-15.00 — Single application history store

**What must be fully done.** Implement model 05 SQLite schema/migrations/transactions and typed payloads, plus Android logical-schema fixtures. Retire competing model 02 conversation tables. Include attachment/project/profile/skill/context/task/compaction/pending-work ownership.

**Testing requirements.** Execute DDL with foreign keys; migrations, disk-full, branch fork, concurrent-window stale revision, duplicate terminal frame and interrupted send.

**Completion gate.** One canonical local store per application/profile preserves all committed and pending content.

<a id="rule-wp-15.01"></a>
### WP-15.01 — Branches and window drafts

**What must be fully done.** Implement immutable ancestry and fork-at-message; per-window draft revisions, shared committed service within one application.

**Testing requirements.** Concurrent windows, draft preserved during another send, parent/child isolation.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-15.02"></a>
### WP-15.02 — Attachments and provenance

**What must be fully done.** Implement typed local refs, authorized file staging/preview, resource ownership and explicit egress. Never assume attachment selection is upload consent.

**Testing requirements.** Missing/hostile file, lost URI/path grant, source labels, quota and temporary exclusion.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-15.03"></a>
### WP-15.03 — Projects and profiles

**What must be fully done.** Implement accepted project/instruction/profile CRUD, validation, immutable per-execution snapshots and application partitioning.

**Testing requirements.** Conflict/revision and profile change cannot alter an active execution.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-15.04"></a>
### WP-15.04 — Skills

**What must be fully done.** Implement accepted skill/version/permission metadata and selection without installing an external agent or granting authority from content.

**Testing requirements.** Untrusted instructions remain content; cross-app source denied.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-15.05"></a>
### WP-15.05 — Local search

**What must be fully done.** Index only committed non-deleted normal history in the owning partition; exact citations/branches and rebuildable index.

**Testing requirements.** Delete/rebuild, partial index and no temporary/other-app leak.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-15.06"></a>
### WP-15.06 — Local history export and import

**What must be fully done.** Produce/consume assistant-history.v1 from committed local snapshots, preserving branch/message/resource provenance and missing-resource reports. Import remaps identities; Cloud promotion remains WP25.

**Testing requirements.** Offline full round-trip; malformed/archive-hash/foreign references, draft exclusion, branch graph cycles and canceled import. Use assistant-history.v1 for the selected local/cloud/temporary history mode. Its fixtures do not imply a native ArcNotes archive importer; compare its declared preservation and loss rules independently.

**Completion gate.** Local export is complete without Cloud, implicit upload or mode conversion.

<a id="rule-wp-15.07"></a>
### WP-15.07 — Reference and package proof

**What must be fully done.** Record AionUi component evidence/provenance and consume the actual candidate Core/Sqlite package from a clean test application.

**Testing requirements.** No reference runtime/imported agent scope; full local behavior and exact package hashes.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-15.90"></a>
### WP-15.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-15.90](#rule-wp-15.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

| Evidence | Produced by |
|---|---|
| Conversation and local history store: Actual SQLite transaction/kill/disk-full; independent product partitions and immutable committed messages. | [WP-15.00](#rule-wp-15.00) |
| Branches and window drafts: Concurrent windows, draft preserved during another send, parent/child isolation. | [WP-15.01](#rule-wp-15.01) |
| Attachments and provenance: Missing/hostile file, lost URI/path grant, source labels, quota and temporary exclusion. | [WP-15.02](#rule-wp-15.02) |
| Projects and profiles: Conflict/revision and profile change cannot alter an active execution. | [WP-15.03](#rule-wp-15.03) |
| Skills: Untrusted instructions remain content; cross-app source denied. | [WP-15.04](#rule-wp-15.04) |
| Local search: Delete/rebuild, partial index and no temporary/other-app leak. | [WP-15.05](#rule-wp-15.05) |
| Export, promotion and recovery: Lost finalize ack, changed local history, account switch and migration/downgrade refusal. | [WP-15.06](#rule-wp-15.06) |
| Reference and package proof: No reference runtime/imported agent scope; full local behavior and exact package hashes. | [WP-15.07](#rule-wp-15.07) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-15.90](#rule-wp-15.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [AST.01](../delivery/lanes/assistant.md#task-ast-01) | [WP-15.00](15-arcchat-conversation-core.md#rule-wp-15.00) (full) | [APP.01](../delivery/lanes/app-composition.md#task-app-01) (artifact), [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract), [CON.11](../delivery/lanes/contracts.md#task-con-11) (contract) |
| [AST.02](../delivery/lanes/assistant.md#task-ast-02) | [WP-15.01](15-arcchat-conversation-core.md#rule-wp-15.01) (full) | none |
| [AST.03](../delivery/lanes/assistant.md#task-ast-03) | [WP-15.02](15-arcchat-conversation-core.md#rule-wp-15.02) (full) | [APP.06](../delivery/lanes/app-composition.md#task-app-06) (artifact) |
| [AST.04](../delivery/lanes/assistant.md#task-ast-04) | [WP-15.03](15-arcchat-conversation-core.md#rule-wp-15.03) (full) | none |
| [AST.05](../delivery/lanes/assistant.md#task-ast-05) | [WP-15.04](15-arcchat-conversation-core.md#rule-wp-15.04) (full) | [PLT.42](../delivery/lanes/platform.md#task-plt-42) (artifact) |
| [AST.06](../delivery/lanes/assistant.md#task-ast-06) | [WP-15.05](15-arcchat-conversation-core.md#rule-wp-15.05) (full) | none |
| [AST.07](../delivery/lanes/assistant.md#task-ast-07) | [WP-15.06](15-arcchat-conversation-core.md#rule-wp-15.06) (full) | [CON.11](../delivery/lanes/contracts.md#task-con-11) (contract) |
| [AST.08](../delivery/lanes/assistant.md#task-ast-08) | [WP-15.07](15-arcchat-conversation-core.md#rule-wp-15.07) (full) | none |
| [AST.09](../delivery/lanes/assistant.md#task-ast-09) | [WP-15.90](15-arcchat-conversation-core.md#rule-wp-15.90) (full) | none |

**Consumers outside this package:** [AST.10](../delivery/lanes/assistant.md#task-ast-10), [AST.11](../delivery/lanes/assistant.md#task-ast-11), [AST.15](../delivery/lanes/assistant.md#task-ast-15), [AST.21](../delivery/lanes/assistant.md#task-ast-21), [AST.22](../delivery/lanes/assistant.md#task-ast-22).

<!-- delivery-graph:end -->

