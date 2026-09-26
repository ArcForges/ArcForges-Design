# Embedded assistant — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Assistant abstractions, core, history store, Cloud client surface and Avalonia presentation embedded by each product.

Tasks: 22 · Owning repositories: DesktopPlatform · Integration owner(s): DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [AST.01](#task-ast-01) | Single application history store (model 05 schema) | producer | L | [APP.01](app-composition.md#task-app-01) (artifact), [CON.91](contracts.md#task-con-91) (contract), [CON.11](contracts.md#task-con-11) (contract) | not-started |
| [AST.02](#task-ast-02) | Branches and window drafts | producer | M | [AST.01](#task-ast-01) (artifact) | not-started |
| [AST.03](#task-ast-03) | Attachments and provenance | producer | M | [AST.01](#task-ast-01) (artifact), [APP.06](app-composition.md#task-app-06) (artifact) | not-started |
| [AST.04](#task-ast-04) | Projects and profiles | producer | S | [AST.01](#task-ast-01) (artifact) | not-started |
| [AST.05](#task-ast-05) | Skills | producer | S | [AST.01](#task-ast-01) (artifact), [PLT.42](platform.md#task-plt-42) (artifact) | not-started |
| [AST.06](#task-ast-06) | Local search | producer | M | [AST.01](#task-ast-01) (artifact) | not-started |
| [AST.07](#task-ast-07) | Local history export and import (assistant-history.v1) | producer | M | [AST.01](#task-ast-01) (artifact), [CON.11](contracts.md#task-con-11) (contract) | not-started |
| [AST.08](#task-ast-08) | Reference and package proof (AionUi evidence, clean-app package consumption) | producer | S | [AST.01](#task-ast-01) (artifact) | not-started |
| [AST.09](#task-ast-09) | Owned-artifact receipt and UX acceptance | acceptance | M | [AST.01](#task-ast-01) (artifact), [AST.02](#task-ast-02) (artifact), [AST.03](#task-ast-03) (artifact), [AST.04](#task-ast-04) (artifact), [AST.05](#task-ast-05) (artifact), [AST.06](#task-ast-06) (artifact), [AST.07](#task-ast-07) (artifact), [AST.08](#task-ast-08) (artifact) | not-started |
| [AST.10](#task-ast-10) | Complete assistant navigation shell | producer | L | [EXE.01](execution.md#task-exe-01) (artifact), [AST.01](#task-ast-01) (artifact), [AST.02](#task-ast-02) (artifact), [AST.04](#task-ast-04) (artifact), [AST.05](#task-ast-05) (artifact), [AST.06](#task-ast-06) (artifact), [AST.07](#task-ast-07) (artifact) | not-started |
| [AST.11](#task-ast-11) | Cloud client and device runtime (fixture turn endpoint boundary) | producer | L | [CON.10](contracts.md#task-con-10) (contract), [PRF.05](runtime-proofs.md#task-prf-05) (artifact), [AST.01](#task-ast-01) (artifact) | not-started |
| [AST.12](#task-ast-12) | Security and approval surface | producer | M | [AST.10](#task-ast-10) (artifact), [APP.05](app-composition.md#task-app-05) (artifact), [PLT.39](platform.md#task-plt-39) (artifact) | not-started |
| [AST.13](#task-ast-13) | Task centre | producer | M | [AST.10](#task-ast-10) (artifact), [EXE.01](execution.md#task-exe-01) (artifact), [EXE.05](execution.md#task-exe-05) (artifact), [AST.11](#task-ast-11) (artifact) | not-started |
| [AST.14](#task-ast-14) | Automation client (automation fixture state transitions) | producer | M | [AST.10](#task-ast-10) (artifact), [CON.10](contracts.md#task-con-10) (contract) | not-started |
| [AST.15](#task-ast-15) | History and AI admission (local/cloud/temporary modes) | producer | M | [AST.10](#task-ast-10) (artifact), [AST.07](#task-ast-07) (artifact) | not-started |
| [AST.16](#task-ast-16) | Preview and host context | producer | M | [AST.10](#task-ast-10) (artifact), [APP.06](app-composition.md#task-app-06) (artifact) | not-started |
| [AST.17](#task-ast-17) | Complete package acceptance (Assistant.Avalonia/Core/Sqlite/Cloud) | acceptance | L | [AST.10](#task-ast-10) (artifact), [AST.11](#task-ast-11) (artifact), [AST.12](#task-ast-12) (artifact), [AST.13](#task-ast-13) (artifact), [AST.14](#task-ast-14) (artifact), [AST.15](#task-ast-15) (artifact), [AST.16](#task-ast-16) (artifact) | not-started |
| [AST.18](#task-ast-18) | Owned-artifact receipt and real integration | acceptance | M | [AST.17](#task-ast-17) (artifact) | not-started |
| [AST.19](#task-ast-19) | Real Cloud Harness turn loop replacing the fixture turn endpoint | integration | M | [AST.11](#task-ast-11) (artifact), [HAR.00](harness.md#task-har-00) (artifact), [HAR.03](harness.md#task-har-03) (artifact) | not-started |
| [AST.20](#task-ast-20) | Real durable Cloud automation scheduler replacing the automation fixture | integration | M | [AST.14](#task-ast-14) (artifact), [HAR.06](harness.md#task-har-06) (artifact) | not-started |
| [AST.21](#task-ast-21) | Real Cloud Notes/Chat export producer replacing the local assistant-history.v1 fixture | integration | M | [AST.07](#task-ast-07) (artifact), [CLOUD.45](cloud.md#task-cloud-45) (artifact) | not-started |
| [AST.22](#task-ast-22) | Real Cloud application-history restartable import receiving promoted local history | integration | M | [AST.15](#task-ast-15) (artifact), [CLOUD.46](cloud.md#task-cloud-46) (artifact), [AST.01](#task-ast-01) (artifact) | not-started |

## Tasks

<a id="task-ast-01"></a>

### AST.01 — Single application history store (model 05 schema)

**Outcome.** Assistant.Persistence.Sqlite implements the full data-model-05 schema (assistant_conversation/branch/message/draft/turn/receipt/outbox/history_import/attachment/project/conversation_project/profile/skill/context/task_projection/compaction), migrations and typed payloads, plus Android logical-schema fixtures. Competing model-02 conversation tables retired.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-01` and ledger record `ledger/tasks/ast-01.md` in the Plan repository; task branch `task/ast-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L · early risk proof |
| Obligations | [WP-15.00](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.00) — full |
| Provides | assistant-history-store; assistant-core-pkg |
| Start prerequisites | **artifact** [APP.01](app-composition.md#task-app-01) — published Assistant.Abstractions product/profile identity. *Why:* one canonical store is scoped per application/profile using this real identity type<br>**contract** [CON.91](contracts.md#task-con-91) — published Foundation contract types (identity/error/revision). *Why:* typed payloads and transaction/revision handling are built on these records<br>**contract** [CON.11](contracts.md#task-con-11) — complete generated package/schema gate output. *Why:* SQLite schema and typed payloads mirror the generated Contracts schema definitions, not a private redefinition |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.02](#task-ast-02), [AST.03](#task-ast-03), [AST.04](#task-ast-04), [AST.05](#task-ast-05), [AST.06](#task-ast-06), [AST.07](#task-ast-07), [AST.08](#task-ast-08), [AST.09](#task-ast-09), [AST.10](#task-ast-10), [AST.11](#task-ast-11), [AST.22](#task-ast-22) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Core/**`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Persistence.Sqlite/**`<br>`DesktopPlatform:tests/AssistantCoreTests/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append), [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline unit tests: DDL with foreign keys, migrations, disk-full, branch fork, concurrent-window stale revision, duplicate terminal frame, interrupted send; no live environment. |
| Completion evidence | Schema/migration hash, transaction-kill and disk-full test results, one-store-per-application-profile proof. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No Assistant.Core or Assistant.Persistence.Sqlite project exists in DesktopPlatform yet. |
| Notes | Foundation for all other WP15 substeps and for WP16/17's reuse of conversation identities; a schema mistake here invalidates branches, attachments, projects, skills, search and export simultaneously, so it should land and stabilize early. |

<a id="task-ast-02"></a>

### AST.02 — Branches and window drafts

**Outcome.** Immutable ancestry and fork-at-message; per-window draft revisions with a shared committed service within one application. Concurrent windows, draft preserved during another send, parent/child isolation proven.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-02` and ledger record `ledger/tasks/ast-02.md` in the Plan repository; task branch `task/ast-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-15.01](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.01) — full |
| Provides | assistant-branch-service |
| Start prerequisites | **artifact** [AST.01](#task-ast-01) — the real history store's branch/message tables. *Why:* branching operates on the real committed-message store, not a private cache |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.09](#task-ast-09), [AST.10](#task-ast-10) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Core/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline unit tests: concurrent windows, draft preserved during another send, parent/child isolation. |
| Completion evidence | Concurrent-window and fork-isolation test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-03"></a>

### AST.03 — Attachments and provenance

**Outcome.** Typed local refs, authorized file staging/preview, resource ownership and explicit egress; attachment selection is never treated as upload consent. Missing/hostile file, lost URI/path grant, source labels, quota and temporary exclusion covered.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-03` and ledger record `ledger/tasks/ast-03.md` in the Plan repository; task branch `task/ast-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-15.02](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.02) — full |
| Provides | assistant-attachment-service |
| Start prerequisites | **artifact** [AST.01](#task-ast-01) — the real history store's attachment table. *Why:* attachment provenance persists into the real store<br>**artifact** [APP.06](app-composition.md#task-app-06) — the real [WP-14.05](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05) context/artifact freeze and preview port. *Why:* attachment staging/preview must use the same frozen-resource mechanism, not a private duplicate |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.09](#task-ast-09) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Core/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline unit tests: missing/hostile file, lost URI/path grant, quota, temporary exclusion. |
| Completion evidence | Attachment provenance and egress-consent test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-04"></a>

### AST.04 — Projects and profiles

**Outcome.** Accepted project/instruction/profile CRUD, validation, immutable per-execution snapshots and application partitioning; conflict/revision handling and profile change cannot alter an active execution.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-04` and ledger record `ledger/tasks/ast-04.md` in the Plan repository; task branch `task/ast-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-15.03](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.03) — full |
| Provides | assistant-project-profile-service |
| Start prerequisites | **artifact** [AST.01](#task-ast-01) — the real history store's project/profile tables. *Why:* CRUD and snapshotting operate on the real store |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.09](#task-ast-09), [AST.10](#task-ast-10) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Core/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline unit tests: conflict/revision, active-execution immutability. |
| Completion evidence | Immutable-snapshot-during-active-execution test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-05"></a>

### AST.05 — Skills

**Outcome.** Accepted skill/version/permission metadata and selection, without installing an external agent or granting authority from content; untrusted instructions remain content, cross-app source denied.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-05` and ledger record `ledger/tasks/ast-05.md` in the Plan repository; task branch `task/ast-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-15.04](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.04) — full |
| Provides | assistant-skill-service |
| Start prerequisites | **artifact** [AST.01](#task-ast-01) — the real history store's skill table. *Why:* skill metadata persists into the real store<br>**artifact** [PLT.42](platform.md#task-plt-42) — published instruction provenance mechanism. *Why:* skill content must be tracked as untrusted instruction provenance, not granted authority |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.09](#task-ast-09), [AST.10](#task-ast-10) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Core/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline unit tests: untrusted-instruction and cross-app-source-denied cases. |
| Completion evidence | Skill selection/provenance test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-06"></a>

### AST.06 — Local search

**Outcome.** Indexes only committed non-deleted normal history in the owning partition, with exact citations/branches and a rebuildable index; delete/rebuild, partial index and no temporary/other-app leak proven.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-06` and ledger record `ledger/tasks/ast-06.md` in the Plan repository; task branch `task/ast-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-15.05](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.05) — full |
| Provides | assistant-local-search |
| Start prerequisites | **artifact** [AST.01](#task-ast-01) — the real committed-message store to index. *Why:* search must index the real committed content, not a fixture, to prove no temporary/other-app leak |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.09](#task-ast-09), [AST.10](#task-ast-10) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Core/**` |
| Validation | Offline unit tests: delete/rebuild, partial index, isolation leak checks. |
| Completion evidence | Rebuild and isolation-leak test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-07"></a>

### AST.07 — Local history export and import (assistant-history.v1)

**Outcome.** Produces/consumes assistant-history.v1 from committed local snapshots, preserving branch/message/resource provenance and missing-resource reports; import remaps identities. Complete offline without Cloud, implicit upload or mode conversion. Cloud promotion itself remains [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25).

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-07` and ledger record `ledger/tasks/ast-07.md` in the Plan repository; task branch `task/ast-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-15.06](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.06) — full |
| Provides | assistant-history-export-format |
| Start prerequisites | **artifact** [AST.01](#task-ast-01) — the real committed history store to export from. *Why:* offline round-trip must exercise the real store's branch graph<br>**contract** [CON.11](contracts.md#task-con-11) — published assistant-history.v1 format definition. *Why:* export/import implements the published format, not a private one |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.09](#task-ast-09), [AST.10](#task-ast-10), [AST.15](#task-ast-15), [AST.21](#task-ast-21) |
| Permitted substitutes | [SUB-assistant-history-fixture](../substitutes.md#sub-assistant-history-fixture) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Core/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline full round-trip tests: malformed/hash/foreign references, draft exclusion, branch cycles, canceled import; no Cloud in CI. |
| Completion evidence | Round-trip hash manifests, malformed/cycle/cancel test results, named-fixture manifest entry for this substitute. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | One of the four named scaffolding rows in implementation-sequence.md §3.1 (shared with ArcNotes' own [WP-19.05](../../work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.05), not mine). See integration_proposals IM.history-export-cloud-promotion. |

<a id="task-ast-08"></a>

### AST.08 — Reference and package proof (AionUi evidence, clean-app package consumption)

**Outcome.** AionUi component evidence/provenance recorded; the actual candidate Assistant.Core/Assistant.Persistence.Sqlite package consumed from a clean test application with no reference runtime or imported agent scope.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-08` and ledger record `ledger/tasks/ast-08.md` in the Plan repository; task branch `task/ast-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-15.07](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.07) — full |
| Provides | assistant-core-sqlite-package-proof |
| Start prerequisites | **artifact** [AST.01](#task-ast-01) — published Assistant.Core/Assistant.Persistence.Sqlite candidate packages. *Why:* this substep proves package-only consumption of the actual candidate, distinct from in-repo testing |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.09](#task-ast-09) |
| Write scope | `DesktopPlatform:tests/AssistantCoreTests/**` |
| Validation | Package-only restore in a clean test app; offline behavior tests; exact package hash recorded. |
| Completion evidence | Package hash manifest, AionUi reference-coverage citation (arcchat-aionui.md, no reused code), clean-app test results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: arcchat-aionui.md reference matrix already exists (bound to commit 29c9271a5) with zero reuse rows; this task re-checks for drift, does not recreate the matrix. |

<a id="task-ast-09"></a>

### AST.09 — Owned-artifact receipt and UX acceptance

**Outcome.** WP15 built/packed once from a clean environment; all applicable UX acceptance groups recorded; package/contract/owner/version compatibility and failure/recovery evidence attached; no later-provider fixture closes a real WP15 gate.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-09` and ledger record `ledger/tasks/ast-09.md` in the Plan repository; task branch `task/ast-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-15](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-15.90](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.90) — full |
| Provides | wp15-accepted-artifact |
| Start prerequisites | **artifact** [AST.01](#task-ast-01) — completed [WP-15.00](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.00). *Why:* aggregation<br>**artifact** [AST.02](#task-ast-02) — completed [WP-15.01](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.01). *Why:* aggregation<br>**artifact** [AST.03](#task-ast-03) — completed [WP-15.02](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.02). *Why:* aggregation<br>**artifact** [AST.04](#task-ast-04) — completed [WP-15.03](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.03). *Why:* aggregation<br>**artifact** [AST.05](#task-ast-05) — completed [WP-15.04](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.04). *Why:* aggregation<br>**artifact** [AST.06](#task-ast-06) — completed [WP-15.05](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.05). *Why:* aggregation<br>**artifact** [AST.07](#task-ast-07) — completed [WP-15.06](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.06). *Why:* aggregation<br>**artifact** [AST.08](#task-ast-08) — completed [WP-15.07](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.07). *Why:* aggregation |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:artifacts/evidence/**` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Build/pack once; UX-C history ledger rows recorded; [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) scope only. |
| Completion evidence | Source commit, package versions/hashes, UX-C rows, named-fixture manifest (assistant-history.v1 export fixture). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-10"></a>

### AST.10 — Complete assistant navigation shell

**Outcome.** All AS01 to AS13 docked/floating/expanded surfaces are reachable through the architecture-27 AssistantHost API; the same composition code works independently in each product. All actions reachable at minimum size; window/draft/account/keyboard/accessibility matrix passes.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-10` and ledger record `ledger/tasks/ast-10.md` in the Plan repository; task branch `task/ast-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-17.00](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.00) — full |
| Provides | assistant-host-shell; assistanthost-api |
| Start prerequisites | **artifact** [EXE.01](execution.md#task-exe-01) — the real execution chain to surface job state in navigation. *Why:* AS05/AS10-linked navigation elements read real ProductJob state<br>**artifact** [AST.01](#task-ast-01) — the real application history store the shell hosts. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AST.02](#task-ast-02) — real branches and window drafts to navigate. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AST.04](#task-ast-04) — real projects and profiles to navigate. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AST.05](#task-ast-05) — real skills to navigate. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AST.06](#task-ast-06) — real local search to surface. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AST.07](#task-ast-07) — real local history export and import to surface. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.12](#task-ast-12), [AST.13](#task-ast-13), [AST.14](#task-ast-14), [AST.15](#task-ast-15), [AST.16](#task-ast-16), [AST.17](#task-ast-17) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Avalonia/**`<br>`DesktopPlatform:samples/AssistantHost/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline UI tests: minimum-size reachability, window/draft/account/keyboard/accessibility matrix; no live Cloud in CI. |
| Completion evidence | Reachability matrix results, accessibility pass, source commit. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No Assistant.Avalonia or samples/AssistantHost exists yet in DesktopPlatform. |
| Notes | This is the navigation shell/chrome only; deeper per-surface behavior (security, task centre, automation, history, preview) is separately owned by AST.12-16 and composed into this shell. |

<a id="task-ast-11"></a>

### AST.11 — Cloud client and device runtime (fixture turn endpoint boundary)

**Outcome.** Reusable Cloud.Client (session/event/output/upload) and Device.Runtime (own-app registration/presence, pull/claim/result, typed dispatch adapter) implemented against generated gRPC-Web contracts; own-app typed dispatch adapters work end-to-end in-process. Named future-owner fixtures stand in for [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) through [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26) and [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52) until those exist.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-11` and ledger record `ledger/tasks/ast-11.md` in the Plan repository; task branch `task/ast-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-17.01](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.01) — full |
| Provides | cloud-client-sdk; device-runtime-client-adapter |
| Start prerequisites | **contract** [CON.10](contracts.md#task-con-10) — published generated C#/TypeScript/Kotlin gRPC-Web client stubs and numbered wire registry. *Why:* Cloud.Client's typed SDK wraps the generated stubs; nothing to wrap without the published package<br>**artifact** [PRF.05](runtime-proofs.md#task-prf-05) — proven generated gRPC-Web under Native AOT pattern. *Why:* Cloud.Client must be AOT-safe; reuse the already-proven pattern<br>**artifact** [AST.01](#task-ast-01) — the history store assistant_turn and assistant_outbox records the Cloud client writes into. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.13](#task-ast-13), [AST.17](#task-ast-17), [AST.19](#task-ast-19), [DEV.03](device-bridge.md#task-dev-03), [DEV.14](device-bridge.md#task-dev-14), [HAR.05](harness.md#task-har-05) |
| Permitted substitutes | [SUB-device-runtime-loopback](../substitutes.md#sub-device-runtime-loopback), [SUB-fixture-turn-endpoint](../substitutes.md#sub-fixture-turn-endpoint) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Communication.CloudClient/**`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Communication.DeviceRuntime/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline tests against generated gRPC-Web calls/typed states with an explicit named-fixture manifest; no live Cloud in CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Fixture manifest naming each replacement producer ([WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23)..26, [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52)), typed-state test results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No Communication project tree exists in DesktopPlatform yet. |
| Notes | This is the DesktopPlatform half of the WP26 dual-repo split: Device.Runtime's project skeleton is built here and extended (not duplicated) by DEV.03/DEV.05. |

<a id="task-ast-12"></a>

### AST.12 — Security and approval surface

**Outcome.** AS06/11/12 implemented with actor/target/context/egress/cost/expiry and local-presence escalation; no persistent allow-all or cross-product grant, stale approval refused.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-12` and ledger record `ledger/tasks/ast-12.md` in the Plan repository; task branch `task/ast-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-17.02](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.02) — full |
| Provides | assistant-security-surface |
| Start prerequisites | **artifact** [AST.10](#task-ast-10) — the navigation shell to compose this surface into. *Why:* AS06/11/12 are surfaces within the shell<br>**artifact** [APP.05](app-composition.md#task-app-05) — the exact [WP-14.04](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04) owner approval enforcement point. *Why:* this surface renders and escalates the same owner approval, never a separate UI-only mock<br>**artifact** [PLT.39](platform.md#task-plt-39) — published approval/steering/step-up mechanism. *Why:* local-presence escalation reuses the real security step-up primitive |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.17](#task-ast-17), [SCOPE.20](arcscope.md#task-scope-20) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Avalonia/**` |
| Validation | Offline tests: no persistent allow-all/cross-product grant, stale approval refused. |
| Completion evidence | Allow-all/cross-product/stale-approval negative test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-13"></a>

### AST.13 — Task centre

**Outcome.** Task timeline, tools, artifacts, cancellation/steering and ProductJob links with effect certainty; canceled/interrupted/unknown/complete distinguishable, closing the view does not cancel.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-13` and ledger record `ledger/tasks/ast-13.md` in the Plan repository; task branch `task/ast-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-17.03](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.03) — full |
| Provides | assistant-task-centre |
| Start prerequisites | **artifact** [AST.10](#task-ast-10) — the navigation shell to compose this surface into. *Why:* task centre is a surface within the shell<br>**artifact** [EXE.01](execution.md#task-exe-01) — the real execution chain (ProductJobRecord/JobAttempt) to link to. *Why:* 17.03 explicitly links to ProductJob with effect certainty; a mock task list would not exercise real cancellation/steering<br>**artifact** [EXE.05](execution.md#task-exe-05) — real checkpoint/compensation state for display. *Why:* task centre must distinguish canceled/interrupted/unknown/complete using real EffectCertainty, not a placeholder enum<br>**artifact** [AST.11](#task-ast-11) — the Cloud client's TaskRef/output stream for the Cloud Agent Task side of the timeline. *Why:* the timeline shows both native ProductJob and Cloud Agent Task entries distinctly |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.17](#task-ast-17) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Avalonia/**` |
| Validation | Offline tests: canceled/interrupted/unknown/complete distinguishability, close-does-not-cancel. |
| Completion evidence | State-distinguishability and close-behavior test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-14"></a>

### AST.14 — Automation client (automation fixture state transitions)

**Outcome.** Existing Cloud-owned rule/occurrence UI implemented: schedule/timezone/target/budget and action availability; offline edits remain drafts and never imply local scheduling.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-14` and ledger record `ledger/tasks/ast-14.md` in the Plan repository; task branch `task/ast-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-17.04](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.04) — full |
| Provides | assistant-automation-client |
| Start prerequisites | **artifact** [AST.10](#task-ast-10) — the navigation shell to compose this surface into. *Why:* automation client is a surface within the shell<br>**contract** [CON.10](contracts.md#task-con-10) — published Cloud-owned rule/occurrence record shapes. *Why:* this client only renders Cloud-owned records, it does not define its own scheduling model |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.17](#task-ast-17), [AST.20](#task-ast-20) |
| Permitted substitutes | [SUB-automation-fixture](../substitutes.md#sub-automation-fixture) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Avalonia/**` |
| Validation | Offline tests: offline edits remain drafts; no live scheduler in CI. |
| Completion evidence | Named-fixture manifest entry, offline-draft test results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Second of the four named scaffolding rows in implementation-sequence.md §3.1. |

<a id="task-ast-15"></a>

### AST.15 — History and AI admission (local/cloud/temporary modes)

**Outcome.** Local/cloud/temporary disclosure, mode selection, Cloud promotion/copy UI and real local lifecycle implemented, with named Cloud fixtures for the promotion target; no implicit upload; denied-admission/credit-consent and transient-output-recovery states covered.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-15` and ledger record `ledger/tasks/ast-15.md` in the Plan repository; task branch `task/ast-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-17.05](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.05) — full |
| Provides | assistant-history-admission-ui |
| Start prerequisites | **artifact** [AST.10](#task-ast-10) — the navigation shell to compose this surface into. *Why:* history/admission is a surface within the shell<br>**artifact** [AST.07](#task-ast-07) — the real assistant-history.v1 local export/import surface. *Why:* Cloud promotion/copy UI operates on the real local export, not a separate format |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.08](ai-routing.md#task-air-08), [AST.17](#task-ast-17), [AST.22](#task-ast-22), [HAR.03](harness.md#task-har-03), [SCOPE.21](arcscope.md#task-scope-21) |
| Permitted substitutes | [SUB-history-admission-fixture](../substitutes.md#sub-history-admission-fixture), [SUB-stubbed-provider-path](../substitutes.md#sub-stubbed-provider-path) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Cloud/**` |
| Validation | Offline tests: no implicit upload, denied admission/credit consent, transient output recovery states; no live Cloud in CI. |
| Completion evidence | Named-fixture manifest entry, admission/consent/recovery test results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | See integration_proposals IM.cloud-history-admission for the real [WP-25.09](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.09) receiver proof. |

<a id="task-ast-16"></a>

### AST.16 — Preview and host context

**Outcome.** AS03/08 own-app selection/preview/navigation implemented using the frozen [WP-14.05](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05) host ports, with safe fallback for unsupported native preview; no live-selection mutation, no another-product destination, citations/resources keep ownership.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-16` and ledger record `ledger/tasks/ast-16.md` in the Plan repository; task branch `task/ast-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-17.06](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.06) — full |
| Provides | assistant-preview-surface |
| Start prerequisites | **artifact** [AST.10](#task-ast-10) — the navigation shell to compose this surface into. *Why:* preview is a surface within the shell<br>**artifact** [APP.06](app-composition.md#task-app-06) — the exact frozen [WP-14.05](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.05) context/artifact preview port. *Why:* 17.06 explicitly requires using the frozen host ports, not a duplicate preview mechanism |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.17](#task-ast-17) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Assistant.Avalonia/**` |
| Validation | Offline tests: no live-selection mutation, no cross-product destination, citation/resource ownership preserved. |
| Completion evidence | Selection-mutation and ownership test results. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-17"></a>

### AST.17 — Complete package acceptance (Assistant.Avalonia/Core/Sqlite/Cloud)

**Outcome.** Assistant.Avalonia/Core/Sqlite/Cloud candidates published; a clean Native AOT host consumes only required packages; every accepted assistant capability is mapped; UX-A/B/C/H pass locally; real Cloud/AI fixtures remain explicit and close only at [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26)/[WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52).

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-17` and ledger record `ledger/tasks/ast-17.md` in the Plan repository; task branch `task/ast-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / L |
| Obligations | [WP-17.07](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.07) — full |
| Provides | assistant-full-package-set |
| Start prerequisites | **artifact** [AST.10](#task-ast-10) — completed [WP-17.00](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.00). *Why:* aggregation<br>**artifact** [AST.11](#task-ast-11) — completed [WP-17.01](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.01). *Why:* aggregation<br>**artifact** [AST.12](#task-ast-12) — completed [WP-17.02](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.02). *Why:* aggregation<br>**artifact** [AST.13](#task-ast-13) — completed [WP-17.03](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.03). *Why:* aggregation<br>**artifact** [AST.14](#task-ast-14) — completed [WP-17.04](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.04). *Why:* aggregation<br>**artifact** [AST.15](#task-ast-15) — completed [WP-17.05](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.05). *Why:* aggregation<br>**artifact** [AST.16](#task-ast-16) — completed [WP-17.06](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.06). *Why:* aggregation |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [APP.08](app-composition.md#task-app-08) — [WP-14](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14) acceptance complete. *Why:* the [WP-17](../../work-packages/17-arcchat-independent-core.md#rule-wp-17) package acceptance includes the accepted [WP-14](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14) artifact; its verification can be prepared before that closes<br>**integration** [EXE.09](execution.md#task-exe-09) — [WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) acceptance complete. *Why:* the [WP-17](../../work-packages/17-arcchat-independent-core.md#rule-wp-17) package acceptance includes the accepted [WP-16](../../work-packages/16-unified-execution-engine.md#rule-wp-16) artifact; its verification can be prepared before that closes |
| Unblocks | [AST.18](#task-ast-18) |
| Write scope | `DesktopPlatform:samples/AssistantHost/**`<br>`DesktopPlatform:artifacts/evidence/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Clean-environment AOT publish/run of the sample host; UX-A/B/C/H ledger rows recorded locally; real Cloud/AI fixtures explicitly named, not closed here; [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) scope only. |
| Completion evidence | Package set versions/hashes, clean-host run log, UX-A/B/C/H rows, consolidated named-fixture manifest. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-18"></a>

### AST.18 — Owned-artifact receipt and real integration

**Outcome.** WP17 built/packed once from a clean environment; all applicable UX acceptance groups recorded; later external evidence ([WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26)/[WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41)/[WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52)) remains explicitly named, not fabricated.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-18` and ledger record `ledger/tasks/ast-18.md` in the Plan repository; task branch `task/ast-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-17](../../work-packages/17-arcchat-independent-core.md#rule-wp-17) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-17.90](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.90) — full |
| Provides | wp17-accepted-artifact |
| Start prerequisites | **artifact** [AST.17](#task-ast-17) — completed [WP-17.07](../../work-packages/17-arcchat-independent-core.md#rule-wp-17.07) package acceptance. *Why:* the final receipt aggregates the completed package acceptance |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:artifacts/evidence/**` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) scope only; no macOS/E2E/live-service CI. |
| Completion evidence | Source commit, artifact versions/hashes, environment, UX ledger rows, named-fixture list for [WP-26](../../work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26)/41/52. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Two orphaned substep anchors (rule-wp-17.08, rule-wp-17.09) exist in the WP17 doc with no substep content and no entry in substeps.json --; not modeled as tasks. |

<a id="task-ast-19"></a>

### AST.19 — Real Cloud Harness turn loop replacing the fixture turn endpoint

**Outcome.** [HV-09](../../../architecture/17-agent-harness.md#rule-hv-09) structural test 'no client runs a model loop' plus a live streamed turn against the deployed Harness, deleting the fixture turn endpoint structurally

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-19` and ledger record `ledger/tasks/ast-19.md` in the Plan repository; task branch `task/ast-19` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-52.05](../../work-packages/52-cloud-harness.md#rule-wp-52.05) — all work except the parts mapped to DEV.13, HAR.05 |
| Start prerequisites | **artifact** [AST.11](#task-ast-11) — real, delivered outcome of AST.11 (Cloud client and device runtime (fixture turn endpoint boundary)). *Why:* this integration exercises the real cloud client and device runtime (fixture turn endpoint boundary) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [HAR.00](harness.md#task-har-00) — real Harness turn loop. *Why:* the assistant switches from the fixture turn endpoint to the real Workflow loop<br>**artifact** [HAR.03](harness.md#task-har-03) — real generated streaming and durable output. *Why:* the assistant reads real output streams |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [DEV.13](device-bridge.md#task-dev-13), [HAR.05](harness.md#task-har-05) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | [HV-09](../../../architecture/17-agent-harness.md#rule-hv-09) structural test 'no client runs a model loop' plus a live streamed turn against the deployed Harness, deleting the fixture turn endpoint structurally |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-20"></a>

### AST.20 — Real durable Cloud automation scheduler replacing the automation fixture

**Outcome.** a live scheduled occurrence executes and cascades with storm protection, observed end-to-end from the AST.14 client

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/ast-20` and ledger record `ledger/tasks/ast-20.md` in the Plan repository; task branch `task/ast-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-52.06](../../work-packages/52-cloud-harness.md#rule-wp-52.06) — all work except the parts mapped to HAR.06, HAR.91 |
| Start prerequisites | **artifact** [AST.14](#task-ast-14) — real, delivered outcome of AST.14 (Automation client (automation fixture state transitions)). *Why:* this integration exercises the real automation client (automation fixture state transitions) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [HAR.06](harness.md#task-har-06) — real, delivered outcome of HAR.06 (Durable Cloud automation, scheduling and automation-fixture removal). *Why:* this integration exercises the real durable Cloud automation, scheduling and automation-fixture removal instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [HAR.06](harness.md#task-har-06) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | a live scheduled occurrence executes and cascades with storm protection, observed end-to-end from the AST.14 client |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-21"></a>

### AST.21 — Real Cloud Notes/Chat export producer replacing the local assistant-history.v1 fixture

**Outcome.** a real deployed Cloud export/snapshot job round-trips the same assistant-history.v1 archive that AST.07's offline fixture produces, for both ArcChat and ArcNotes history

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform`; also touches Cloud |
| Claim, branch and ledger | `claims/ast-21` and ledger record `ledger/tasks/ast-21.md` in the Plan repository; task branch `task/ast-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) — all work except the parts mapped to CLOUD.45, CLOUD.58, NOTES.33 |
| Start prerequisites | **artifact** [AST.07](#task-ast-07) — real, delivered outcome of AST.07 (Local history export and import (assistant-history.v1)). *Why:* this integration exercises the real local history export and import (assistant-history.v1) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.45](cloud.md#task-cloud-45) — real, delivered outcome of CLOUD.45 (Real Cloud Notes and Chat export producers). *Why:* this integration exercises the real real Cloud Notes and Chat export producers instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.47](cloud.md#task-cloud-47), [CLOUD.58](cloud.md#task-cloud-58) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | a real deployed Cloud export/snapshot job round-trips the same assistant-history.v1 archive that AST.07's offline fixture produces, for both ArcChat and ArcNotes history |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-ast-22"></a>

### AST.22 — Real Cloud application-history restartable import receiving promoted local history

**Outcome.** AST.15's Cloud promotion/copy UI successfully drives a real restartable import, including lost-finalize-ack, changed-local-history and account-switch recovery

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform`; also touches Cloud |
| Claim, branch and ledger | `claims/ast-22` and ledger record `ledger/tasks/ast-22.md` in the Plan repository; task branch `task/ast-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-25.09](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.09) — full; consumer-side real integration |
| Start prerequisites | **artifact** [AST.15](#task-ast-15) — real, delivered outcome of AST.15 (History and AI admission (local/cloud/temporary modes)). *Why:* this integration exercises the real history and AI admission (local/cloud/temporary modes) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.46](cloud.md#task-cloud-46) — real, delivered outcome of CLOUD.46 (Application Cloud history and restartable import). *Why:* this integration exercises the real application Cloud history and restartable import instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [AST.01](#task-ast-01) — real, delivered outcome of AST.01 (Single application history store (model 05 schema)). *Why:* this integration exercises the real single application history store (model 05 schema) instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.02.assistant](adoption.md#task-adopt-02-assistant) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.47](cloud.md#task-cloud-47) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | AST.15's Cloud promotion/copy UI successfully drives a real restartable import, including lost-finalize-ack, changed-local-history and account-switch recovery |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as CLOUD.57. |
