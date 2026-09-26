# Desktop platform mechanisms — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Persistence, local helper gRPC, capabilities, design system and shell, security and observability packages.

Tasks: 56 · Owning repositories: DesktopPlatform · Integration owner(s): DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [PLT.01](#task-plt-01) | Store abstraction and the single transactional write path | producer | L | [FND.02](foundation.md#task-fnd-02) (artifact), [FND.03](foundation.md#task-fnd-03) (artifact), [FND.05](foundation.md#task-fnd-05) (artifact) | not-started |
| [PLT.02](#task-plt-02) | Append-only journal with durability and bounded truncation | producer | M | [FND.02](foundation.md#task-fnd-02) (artifact), [FND.03](foundation.md#task-fnd-03) (artifact) | not-started |
| [PLT.03](#task-plt-03) | Snapshot and crash/corruption recovery | producer | L | [PLT.02](#task-plt-02) (artifact) | not-started |
| [PLT.04](#task-plt-04) | Migration runner | producer | M | [FND.06](foundation.md#task-fnd-06) (artifact) | not-started |
| [PLT.05](#task-plt-05) | Managed resource store (content-addressed blobs) | producer | M | [PLT.01](#task-plt-01) (artifact) | not-started |
| [PLT.06](#task-plt-06) | Large append store for high-rate chunked data | producer | M | [FND.02](foundation.md#task-fnd-02) (artifact) | not-started |
| [PLT.07](#task-plt-07) | Derived-store abstraction and storage-pressure model | producer | S | [PLT.01](#task-plt-01) (artifact) | not-started |
| [PLT.08](#task-plt-08) | Publish Persistence packages and verify real integration | acceptance | S | [PLT.01](#task-plt-01) (artifact), [PLT.02](#task-plt-02) (artifact), [PLT.03](#task-plt-03) (artifact), [PLT.04](#task-plt-04) (artifact), [PLT.05](#task-plt-05) (artifact), [PLT.06](#task-plt-06) (artifact), [PLT.07](#task-plt-07) (artifact) | not-started |
| [PLT.09](#task-plt-09) | Local gRPC transport and framing over Named Pipe/UDS | producer | L | [PRF.04](runtime-proofs.md#task-prf-04) (artifact), [CON.04](contracts.md#task-con-04) (contract) | not-started |
| [PLT.10](#task-plt-10) | Parent-owned endpoint identity | producer | M | [PLT.09](#task-plt-09) (artifact) | not-started |
| [PLT.11](#task-plt-11) | Child registration lifecycle | producer | M | [PLT.10](#task-plt-10) (artifact) | not-started |
| [PLT.12](#task-plt-12) | Static routing and version refusal | producer | S | [PLT.11](#task-plt-11) (artifact) | not-started |
| [PLT.13](#task-plt-13) | Bounds and concurrency | producer | M | [PLT.09](#task-plt-09) (artifact) | not-started |
| [PLT.14](#task-plt-14) | Disconnect, cancel and retry semantics | producer | M | [PLT.09](#task-plt-09) (artifact), [FND.02](foundation.md#task-fnd-02) (artifact) | not-started |
| [PLT.15](#task-plt-15) | Brokered large data over the sandbox boundary | producer | M | [PLT.09](#task-plt-09) (artifact), [CON.04](contracts.md#task-con-04) (contract) | not-started |
| [PLT.16](#task-plt-16) | Publish LocalRpc package and verify real integration | acceptance | S | [PLT.09](#task-plt-09) (artifact), [PLT.10](#task-plt-10) (artifact), [PLT.11](#task-plt-11) (artifact), [PLT.12](#task-plt-12) (artifact), [PLT.13](#task-plt-13) (artifact), [PLT.14](#task-plt-14) (artifact), [PLT.15](#task-plt-15) (artifact) | not-started |
| [PLT.17](#task-plt-17) | Application identity and in-process composition | producer | S | [CON.91](contracts.md#task-con-91) (contract), [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [PLT.18](#task-plt-18) | Static contribution registration | producer | M | [PLT.17](#task-plt-17) (artifact) | not-started |
| [PLT.19](#task-plt-19) | Capability registry and selection | producer | L | [PLT.17](#task-plt-17) (artifact), [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [PLT.20](#task-plt-20) | Actions and availability | producer | M | [PLT.19](#task-plt-19) (artifact) | not-started |
| [PLT.21](#task-plt-21) | Context providers and freezing | producer | M | [PLT.17](#task-plt-17) (artifact) | not-started |
| [PLT.22](#task-plt-22) | Resources and artifacts resolution | producer | M | [PLT.05](#task-plt-05) (artifact), [PLT.17](#task-plt-17) (artifact) | not-started |
| [PLT.23](#task-plt-23) | Own navigation, hints and health | producer | M | [PLT.22](#task-plt-22) (artifact) | not-started |
| [PLT.24](#task-plt-24) | Invocation pipeline | producer | L | [PLT.19](#task-plt-19) (artifact), [PLT.20](#task-plt-20) (artifact), [PLT.21](#task-plt-21) (artifact) | not-started |
| [PLT.25](#task-plt-25) | Publish Capabilities/Contributions packages and verify real integration | acceptance | S | [PLT.17](#task-plt-17) (artifact), [PLT.18](#task-plt-18) (artifact), [PLT.19](#task-plt-19) (artifact), [PLT.20](#task-plt-20) (artifact), [PLT.21](#task-plt-21) (artifact), [PLT.22](#task-plt-22) (artifact), [PLT.23](#task-plt-23) (artifact), [PLT.24](#task-plt-24) (artifact), [PLT.57](#task-plt-57) (artifact) | not-started |
| [PLT.26](#task-plt-26) | Token system and theming | producer | M | [PRF.01](runtime-proofs.md#task-prf-01) (artifact) | not-started |
| [PLT.27](#task-plt-27) | Windows, panels and layout | producer | L | [PLT.26](#task-plt-26) (artifact) | not-started |
| [PLT.28](#task-plt-28) | Command system | producer | M | [PLT.27](#task-plt-27) (artifact), [PLT.20](#task-plt-20) (artifact) | not-started |
| [PLT.29](#task-plt-29) | Scoped settings | producer | M | [PLT.26](#task-plt-26) (artifact), [PLT.04](#task-plt-04) (artifact) | not-started |
| [PLT.30](#task-plt-30) | Attention and notification model | producer | M | [PLT.27](#task-plt-27) (artifact) | not-started |
| [PLT.31](#task-plt-31) | Error presentation | producer | S | [PLT.26](#task-plt-26) (artifact), [FND.05](foundation.md#task-fnd-05) (artifact) | not-started |
| [PLT.32](#task-plt-32) | Lifecycle, menus and shutdown | producer | M | [PLT.28](#task-plt-28) (artifact) | not-started |
| [PLT.33](#task-plt-33) | Accessibility and localisation baseline | producer | L | [PLT.27](#task-plt-27) (artifact) | not-started |
| [PLT.34](#task-plt-34) | Third-party control admission | producer | M | [PRF.01](runtime-proofs.md#task-prf-01) (artifact) | not-started |
| [PLT.35](#task-plt-35) | Publish DesignSystem/Shell packages and verify real integration | acceptance | S | [PLT.26](#task-plt-26) (artifact), [PLT.27](#task-plt-27) (artifact), [PLT.28](#task-plt-28) (artifact), [PLT.29](#task-plt-29) (artifact), [PLT.30](#task-plt-30) (artifact), [PLT.31](#task-plt-31) (artifact), [PLT.32](#task-plt-32) (artifact), [PLT.33](#task-plt-33) (artifact), [PLT.34](#task-plt-34) (artifact) | not-started |
| [PLT.36](#task-plt-36) | Principals and the actor chain | producer | M | [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [PLT.37](#task-plt-37) | Risk model and classification | producer | M | [PLT.19](#task-plt-19) (artifact) | not-started |
| [PLT.38](#task-plt-38) | Decision pipeline and the four enforcement points | producer | L | [PLT.36](#task-plt-36) (artifact), [PLT.37](#task-plt-37) (artifact), [PLT.10](#task-plt-10) (artifact) | not-started |
| [PLT.39](#task-plt-39) | Approval, steering and step-up | producer | L | [PLT.37](#task-plt-37) (artifact), [PLT.01](#task-plt-01) (artifact) | not-started |
| [PLT.40](#task-plt-40) | Per-application secrets and session isolation | producer | L | [PLT.36](#task-plt-36) (artifact) | not-started |
| [PLT.41](#task-plt-41) | Egress control | producer | M | [PLT.38](#task-plt-38) (artifact) | not-started |
| [PLT.42](#task-plt-42) | Instruction provenance | producer | L | [PLT.21](#task-plt-21) (artifact) | not-started |
| [PLT.43](#task-plt-43) | Capability leases and trust | producer | M | [PLT.38](#task-plt-38) (artifact), [PLT.01](#task-plt-01) (artifact) | not-started |
| [PLT.44](#task-plt-44) | Append-only audit subsystem | producer | M | [PLT.36](#task-plt-36) (artifact), [PLT.01](#task-plt-01) (artifact) | not-started |
| [PLT.45](#task-plt-45) | Content helper and OS-enforced isolation (ContentSandbox host) | producer | XL | [PLT.15](#task-plt-15) (artifact), [PLT.09](#task-plt-09) (artifact), [CON.04](contracts.md#task-con-04) (contract) | not-started |
| [PLT.46](#task-plt-46) | Publish Security packages and verify real integration | acceptance | M | [PLT.36](#task-plt-36) (artifact), [PLT.37](#task-plt-37) (artifact), [PLT.38](#task-plt-38) (artifact), [PLT.39](#task-plt-39) (artifact), [PLT.40](#task-plt-40) (artifact), [PLT.41](#task-plt-41) (artifact), [PLT.42](#task-plt-42) (artifact), [PLT.43](#task-plt-43) (artifact), [PLT.44](#task-plt-44) (artifact), [PLT.45](#task-plt-45) (artifact), [PLT.54](#task-plt-54) (artifact), [PLT.57](#task-plt-57) (artifact) | not-started |
| [PLT.47](#task-plt-47) | Emission and required dimensions | producer | M | [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [PLT.48](#task-plt-48) | Correlation and causation propagation | producer | M | [PLT.47](#task-plt-47) (artifact) | not-started |
| [PLT.49](#task-plt-49) | Redaction by construction | producer | L | [PLT.40](#task-plt-40) (artifact), [FND.05](foundation.md#task-fnd-05) (artifact) | not-started |
| [PLT.50](#task-plt-50) | Cardinality and sampling | producer | M | [PLT.49](#task-plt-49) (artifact) | not-started |
| [PLT.51](#task-plt-51) | Health probes | producer | S | [PLT.23](#task-plt-23) (artifact) | not-started |
| [PLT.52](#task-plt-52) | Desktop diagnostics and consent | producer | L | [PLT.31](#task-plt-31) (artifact), [PLT.49](#task-plt-49) (artifact) | not-started |
| [PLT.53](#task-plt-53) | Publish Observability packages and verify real integration | acceptance | S | [PLT.47](#task-plt-47) (artifact), [PLT.48](#task-plt-48) (artifact), [PLT.49](#task-plt-49) (artifact), [PLT.50](#task-plt-50) (artifact), [PLT.51](#task-plt-51) (artifact), [PLT.52](#task-plt-52) (artifact) | not-started |
| [PLT.54](#task-plt-54) | Real hostile-input containment proof with production parser libraries loaded in ContentSandbox | integration | M | [PLT.45](#task-plt-45) (artifact), [NAT.14](native.md#task-nat-14) (artifact) | not-started |
| [PLT.56](#task-plt-56) | Three professional products compose the shared DesignSystem/Shell without divergence | integration | M | [PLT.35](#task-plt-35) (artifact), [NOTES.03](arcnotes.md#task-notes-03) (artifact), [SCOPE.09](arcscope.md#task-scope-09) (artifact), [SLATE.22](arcslate.md#task-slate-22) (artifact) | not-started |
| [PLT.57](#task-plt-57) | End-to-end capability invocation with real security enforcement inside one product | integration | M | [PLT.24](#task-plt-24) (artifact), [PLT.38](#task-plt-38) (artifact), [APP.01](app-composition.md#task-app-01) (artifact) | not-started |

## Tasks

<a id="task-plt-01"></a>

### PLT.01 — Store abstraction and the single transactional write path

**Outcome.** IStore/CommitUnit/WriteCommand exist with the eight-step write path (validate, authorize, begin commit unit, apply, journal, advance revision, enqueue outbox, commit, notify) implemented exactly once; persistence types never cross the repository boundary; a policy test proves no alternative write path exists.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-01` and ledger record `ledger/tasks/plt-01.md` in the Plan repository; task branch `task/plt-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-07.00](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.00) — full<br>[WP-07](../../work-packages/07-local-persistence-foundation.md#rule-wp-07) Content-origin carrier projection committed atomically with payload in the same owner transaction/journal boundary (SS2 required design input) — package-level obligation contribution |
| Provides | persistence-write-path; commit-unit-type |
| Start prerequisites | **artifact** [FND.02](foundation.md#task-fnd-02) — CommandId/effect-certainty types. *Why:* the commit unit's idempotency slot and outbox entry are typed with [WP-04.01](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.01)'s execution identities; cannot write the transactional envelope without them.<br>**artifact** [FND.03](foundation.md#task-fnd-03) — Revision type. *Why:* the write path's 'advance revision exactly once' step is defined in terms of [WP-04.02](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.02)'s Revision type, not an ad hoc integer.<br>**artifact** [FND.05](foundation.md#task-fnd-05) — reason-code registry. *Why:* every refusal in the pipeline (validate/authorize failures) must return a registered code per [BR-06](../../../architecture/14-build-packaging-and-release.md#rule-br-06)/07 of WP04. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.38](cloud.md#task-cloud-38), [FND.02](foundation.md#task-fnd-02), [NAT.02](native.md#task-nat-02), [NOTES.01](arcnotes.md#task-notes-01), [NOTES.02](arcnotes.md#task-notes-02), [PLT.05](#task-plt-05), [PLT.07](#task-plt-07), [PLT.08](#task-plt-08), [PLT.39](#task-plt-39), [PLT.43](#task-plt-43), [PLT.44](#task-plt-44), [SCOPE.01](arcscope.md#task-scope-01), [SLATE.10](arcslate.md#task-slate-10) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Sqlite/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline unit + integration tests against a real local SQLite file (no external service): policy test asserting no alternative write path, concurrency tests for serialised writes/concurrent reads, boundary test that no storage type appears in an application signature. AOT/trim diagnostics build-breaking since this library is IsAotCompatible. |
| Completion evidence | Single-write-path policy test result. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/BuildingBlocks/ArcForges.Persistence.Sqlite/ is a bare AssemblyPlaceholder.cs project with zero dependencies declared; Microsoft.Data.Sqlite is not yet in Directory.Packages.props. |
| Notes | Interface-first decoupling recommended: define IJournalWriter/IJournalReader here as the seam PLT.02 implements, so PLT.01 and PLT.02 can be authored in parallel PRs against the same interface rather than serially. |

<a id="task-plt-02"></a>

### PLT.02 — Append-only journal with durability and bounded truncation

**Outcome.** JournalEntry records every commit with enough information to replay; journal writes are durable before a commit is acknowledged; growth is bounded by snapshot policy and truncation is safe under concurrent read.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-02` and ledger record `ledger/tasks/plt-02.md` in the Plan repository; task branch `task/plt-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-07.01](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.01) — full |
| Provides | persistence-journal |
| Start prerequisites | **artifact** [FND.02](foundation.md#task-fnd-02) — CommandId type. *Why:* [JS-01](../../../architecture/06-data-persistence-and-formats.md#rule-js-01) requires the journal entry to carry CommandId, checksum, actor, correlation, causation, commit time - these are [WP-04](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04) types.<br>**artifact** [FND.03](foundation.md#task-fnd-03) — Revision/Sequence types. *Why:* [JS-01](../../../architecture/06-data-persistence-and-formats.md#rule-js-01) requires previous/new typed source version fields. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.11](arcnotes.md#task-notes-11), [PLT.03](#task-plt-03), [PLT.08](#task-plt-08), [SLATE.11](arcslate.md#task-slate-11) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Sqlite/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline tests: durability test using a simulated process kill between journal write and commit acknowledgement (in-process fault injection, not a real OS-level crash - that remains local opt-in); replay test; truncation-under-read test. |
| Completion evidence | Durability and replay results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: No journal table/type exists. |

<a id="task-plt-03"></a>

### PLT.03 — Snapshot and crash/corruption recovery

**Outcome.** Snapshots are policy-triggered, self-describing and verifiable; recovery selects the latest verifiable snapshot and replays the journal forward to typed outcomes (clean, recovered-with-loss, unrecoverable-with-preserved-evidence); native crash and safe-start paths are handled.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-03` and ledger record `ledger/tasks/plt-03.md` in the Plan repository; task branch `task/plt-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L · early risk proof |
| Obligations | [WP-07.02](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.02) — full |
| Provides | persistence-snapshot-recovery; recovery-outcome-type |
| Start prerequisites | **artifact** [PLT.02](#task-plt-02) — journal append/replay implementation. *Why:* recovery is defined as 'replay the journal forward from the most recent valid snapshot'; cannot be written or tested against a real journal until PLT.02's replay contract exists (may start against the IJournalReader interface from PLT.01 with a fake, but the real recovery matrix needs the real journal). |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.11](arcnotes.md#task-notes-11), [PLT.08](#task-plt-08), [SLATE.11](arcslate.md#task-slate-11) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Sqlite/**` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline tests: full recovery matrix (clean shutdown, hard kill, kill during snapshot, kill during migration, corrupted snapshot, corrupted journal tail, disk-full during write) using simulated fault injection; native-crash/safe-start scenarios beyond process-level simulation are local opt-in only. |
| Completion evidence | Full recovery matrix with a named outcome per case. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: No snapshot mechanism exists. |
| Notes | This is one of the two narrowest, highest-value early risk proofs in the whole platform area (with PLT.45 content-helper isolation): if crash recovery has a hidden defect, every downstream product's data-loss guarantees are invalid. Recommend starting this in the same wave as PLT.01/02, not deferred. |

<a id="task-plt-04"></a>

### PLT.04 — Migration runner

**Outcome.** Numbered migrations run through a transactional-per-step, idempotent, resumable-after-interruption runner; StorageSchemaVersion equals the highest applied migration; downgrade is either an explicit reverse migration or a clean refusal.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-04` and ledger record `ledger/tasks/plt-04.md` in the Plan repository; task branch `task/plt-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-07.03](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.03) — full |
| Provides | persistence-migration-runner; storage-schema-version-axis-source |
| Start prerequisites | **artifact** [FND.06](foundation.md#task-fnd-06) — StorageSchemaVersion axis type. *Why:* the runner's version bookkeeping is defined in terms of the typed axis, not a raw integer. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.11](arcnotes.md#task-notes-11), [PLT.08](#task-plt-08), [PLT.29](#task-plt-29), [SLATE.10](arcslate.md#task-slate-10), [UPD.04](updater.md#task-upd-04) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Sqlite/**`<br>`DesktopPlatform:fixtures/formats/**` |
| Shared resources | [RES-desktopplatform-fixtures](../shared-resources.md#res-desktopplatform-fixtures) (append) |
| Validation | Offline tests: forward migration from every historical version fixture, interruption/resume, refusal test for unsupported downgrade, golden-fixture semantic comparison ([QI-07](../../../requirements/12-quality-and-compatibility-contract.md#rule-qi-07)). |
| Completion evidence | Migration results against every historical fixture plus semantic comparison. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: No migrations, no fixtures directory populated yet; this task is the first producer of a real StorageSchemaVersion source, which eng/version-sources.json currently marks not-produced pending 'WP07 and product storage owners'. |

<a id="task-plt-05"></a>

### PLT.05 — Managed resource store (content-addressed blobs)

**Outcome.** Content-addressed storage with identity-to-location resolution, integrity verification on read, reference counting derived from a referrer table, and a GC path that never deletes a referenced object even after a crash mid-operation.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-05` and ledger record `ledger/tasks/plt-05.md` in the Plan repository; task branch `task/plt-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-07.04](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.04) — full |
| Provides | persistence-resource-store; managed-resource-ref-type |
| Start prerequisites | **artifact** [PLT.01](#task-plt-01) — store abstraction's write-path pattern. *Why:* the resource store follows the same single-writer discipline ([BR-11](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-br-11)) even though it is a separate table set; reuses the transactional idiom PLT.01 establishes rather than inventing a second one. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.08](arcnotes.md#task-notes-08), [PLT.08](#task-plt-08), [PLT.22](#task-plt-22) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Resources/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline tests: integrity verification on read, reference-counting test including crash between reference and store, garbage-collection safety test. |
| Completion evidence | Integrity, reference-counting and garbage-collection safety results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/BuildingBlocks/ArcForges.Persistence.Resources/ does not exist yet as a project (only Persistence.Sqlite exists as a placeholder); this is a new project the task must create. |

<a id="task-plt-06"></a>

### PLT.06 — Large append store for high-rate chunked data

**Outcome.** A chunked, verifiable append store outside the relational working store, with per-chunk checksums, an explicit end marker, and honest truncation: a crash mid-append yields a verifiable prefix plus a recorded loss, never a silently short file.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-06` and ledger record `ledger/tasks/plt-06.md` in the Plan repository; task branch `task/plt-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-07.05](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.05) — full |
| Provides | persistence-append-store |
| Start prerequisites | **artifact** [FND.02](foundation.md#task-fnd-02) — execution/effect-certainty types for loss records. *Why:* recorded loss counts/time ranges are typed data, not free text. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.08](#task-plt-08), [SCOPE.07](arcscope.md#task-scope-07), [SLATE.35](arcslate.md#task-slate-35) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Resources/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline tests: append-under-kill at chunk boundaries and mid-chunk, verification of recovered prefix, loss-record assertion. |
| Completion evidence | Append-under-kill results with loss records. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: No append-store mechanism exists; this is entirely new. |

<a id="task-plt-07"></a>

### PLT.07 — Derived-store abstraction and storage-pressure model

**Outcome.** A DerivedStore abstraction with declared rebuild semantics (every derived store deletable/rebuildable from canonical data) and a StoragePressureState model whose eviction policy only ever touches derived data.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-07` and ledger record `ledger/tasks/plt-07.md` in the Plan repository; task branch `task/plt-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-07.06](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.06) — full |
| Provides | persistence-derived-store-pressure; derived-store-abstraction |
| Start prerequisites | **artifact** [PLT.01](#task-plt-01) — store abstraction boundary. *Why:* the derived-store contract is defined relative to canonical data owned by PLT.01's store abstraction ([DS-02](../../../architecture/06-data-persistence-and-formats.md#rule-ds-02): separate file/schema from canonical data). |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.15](arcnotes.md#task-notes-15), [PLT.08](#task-plt-08), [SLATE.21](arcslate.md#task-slate-21) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Derived/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline tests: delete-and-rebuild test per derived-store kind, eviction test asserting canonical data is never evicted. |
| Completion evidence | Rebuild and eviction results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/BuildingBlocks/ArcForges.Persistence.Derived/ does not exist yet. |

<a id="task-plt-08"></a>

### PLT.08 — Publish Persistence packages and verify real integration

**Outcome.** ArcForges.Persistence.Sqlite,.Persistence.Resources and.Persistence.Derived are packed, admitted to the publication allowlist, published, and independently consumed; package consumption is shown not to centralise product data ownership.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-08` and ledger record `ledger/tasks/plt-08.md` in the Plan repository; task branch `task/plt-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-07](../../work-packages/07-local-persistence-foundation.md#rule-wp-07) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-07.90](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.90) — full |
| Provides | persistence-sqlite-package; persistence-resources-package; persistence-derived-package |
| Start prerequisites | **artifact** [PLT.01](#task-plt-01) — write path. *Why:* cannot publish an incomplete store.<br>**artifact** [PLT.02](#task-plt-02) — journal. *Why:* same.<br>**artifact** [PLT.03](#task-plt-03) — snapshot/recovery. *Why:* same.<br>**artifact** [PLT.04](#task-plt-04) — migration runner. *Why:* same.<br>**artifact** [PLT.05](#task-plt-05) — resource store. *Why:* same.<br>**artifact** [PLT.06](#task-plt-06) — append store. *Why:* same.<br>**artifact** [PLT.07](#task-plt-07) — derived store/pressure. *Why:* same. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:eng/packaging/packages.json`<br>`DesktopPlatform:eng/version-sources.json` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): offline packages.py verify plus policy tests; real crash/hardware-level recovery evidence beyond simulated kills is local opt-in, recorded separately. |
| Completion evidence | Owned artifact and real-integration receipt per the [WP-07.90](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.90) template. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: None of the three persistence packages are in eng/packaging/packages.json today. |

<a id="task-plt-09"></a>

### PLT.09 — Local gRPC transport and framing over Named Pipe/UDS

**Outcome.** Generated gRPC over HTTP/2 runs on Windows Named Pipe/Unix domain socket between parent and owned helper/extension children via a custom Kestrel IConnectionListenerFactory and ConnectCallback client, with explicit registration, AOT-safe serialization, and zero local TCP listener.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-09` and ledger record `ledger/tasks/plt-09.md` in the Plan repository; task branch `task/plt-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-08.00](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.00) — full<br>[WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) No product listener/global discovery - structural constraint on every substep, most directly tested by transport/registration — package-level obligation contribution |
| Provides | ipc-transport |
| Start prerequisites | **artifact** [PRF.04](runtime-proofs.md#task-prf-04) — proven AOT gRPC-over-OS-stream pattern from the two real helper-probe processes. *Why:* architecture/03-local-ipc-and-process-model.md states explicitly 'WP06 proves two real AOT helper-probe processes over each exact OS transport; WP08 implements the parent-bound mechanics' - the Kestrel custom listener + ConnectCallback + no-TCP-listener discipline must be established as AOT-compatible before the full protocol is layered on it. A substitute in-process/TCP transport would not validate the AOT-sensitive OS-stream code path [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) exists to de-risk. Owned by the native and runtime-proof lanes.<br>**contract** [CON.04](contracts.md#task-con-04) — ArcForges.Contracts.LocalRpc.Platform/.Sandbox generated proto services. *Why:* the transport carries these generated messages; per contracts/09-local-grpc-and-sandbox.md WP03 publishes all descriptors, methods, validation and fixtures before consumers. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.01](native.md#task-nat-01), [PLT.10](#task-plt-10), [PLT.13](#task-plt-13), [PLT.14](#task-plt-14), [PLT.15](#task-plt-15), [PLT.16](#task-plt-16), [PLT.45](#task-plt-45) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | CI uses targeted deterministic offline framing and authentication fixtures. Actual Named Pipe/Unix domain socket behavior, malformed-frame handling, wrong-user denial and the absence of a local TCP listener are checked locally once when the existing environment supports the affected behavior and the change requires it; fixture evidence never substitutes for actual OS-stream evidence. Do not execute real IPC integration in CI or provision an environment solely for validation. |
| Completion evidence | Actual OS streams, malformed frames, wrong-user denial and no local TCP listener. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: No LocalRpc project exists yet anywhere in the repository tree. |
| Notes | This is the WP-level edge most worth re-examining: the old header lists WP08 upstream as '06 and 07'. [WP-07](../../work-packages/07-local-persistence-foundation.md#rule-wp-07) (Persistence) is NOT a real start need for any WP08 substep - [WP-04.01](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.01)'s own gate explicitly defers durable command/receipt storage to WP07/21/52, meaning WP08's in-flight idempotency stays memory-only; nothing in WP-08.00-08.06 touches SQLite. Recommend dropping the 07->08 start edge entirely; it appears to be inherited phase-grouping (both are 'Phase A/B foundation') rather than a genuine code dependency. |

<a id="task-plt-10"></a>

### PLT.10 — Parent-owned endpoint identity

**Outcome.** Parent launch descriptor fixes endpoint, process/build/protocol identity, nonce and epoch; owner-only endpoint files are created/removed atomically; a stale descriptor never authorizes a child.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-10` and ledger record `ledger/tasks/plt-10.md` in the Plan repository; task branch `task/plt-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-08.01](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.01) — full |
| Provides | ipc-endpoint-identity |
| Start prerequisites | **artifact** [PLT.09](#task-plt-09) — transport/framing. *Why:* endpoint identity is meaningless without a transport to bind it to; genuinely sequential within WP08. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.11](#task-plt-11), [PLT.16](#task-plt-16), [PLT.38](#task-plt-38) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Validation | Offline/local tests: concurrent launch, stale descriptor, forged nonce/build, parent-death cleanup. |
| Completion evidence | Concurrent launch, stale descriptor, forged nonce/build and parent-death cleanup results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-11"></a>

### PLT.11 — Child registration lifecycle

**Outcome.** LocalBootstrap authentication with 30s lease/10s renewal, epoch fencing and restartable restricted launch; expired/stale children cannot call; parent restart requires fresh grants.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-11` and ledger record `ledger/tasks/plt-11.md` in the Plan repository; task branch `task/plt-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-08.02](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.02) — full<br>[WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) No product listener/global discovery - structural constraint on every substep, most directly tested by transport/registration — package-level obligation contribution |
| Provides | ipc-registration |
| Start prerequisites | **artifact** [PLT.10](#task-plt-10) — endpoint identity. *Why:* registration authenticates against the endpoint identity/nonce PLT.10 establishes. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.12](#task-plt-12), [PLT.16](#task-plt-16) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Validation | Offline/local tests: expired/stale child cannot call, parent restart requires fresh grants. |
| Completion evidence | Expired/stale child cannot call; parent restart requires fresh grants. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-12"></a>

### PLT.12 — Static routing and version refusal

**Outcome.** Resolves only explicitly launched children and their declared generated services; rejects unsupported version/capability; never selects an installed product as fallback.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-12` and ledger record `ledger/tasks/plt-12.md` in the Plan repository; task branch `task/plt-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-08.03](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.03) — full |
| Provides | ipc-routing |
| Start prerequisites | **artifact** [PLT.11](#task-plt-11) — registration lifecycle. *Why:* routing operates over registered children. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.16](#task-plt-16) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Validation | Offline tests: version mismatch and unregistered service refusal. |
| Completion evidence | Version mismatch and unregistered service refusal. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-13"></a>

### PLT.13 — Bounds and concurrency

**Outcome.** 16 active/64 queued bounded calls, deadlines and parent-owned callback channels; no recursive saturated callback lane.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-13` and ledger record `ledger/tasks/plt-13.md` in the Plan repository; task branch `task/plt-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-08.04](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.04) — full |
| Provides | ipc-bounds |
| Start prerequisites | **artifact** [PLT.09](#task-plt-09) — transport. *Why:* bounds/backpressure wrap the transport's call dispatch; can proceed in parallel with PLT.10-12 once the transport shape is fixed, not strictly serial after routing. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.16](#task-plt-16) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Validation | Offline tests: queue/memory bound, fairness, timeout and typed overload. |
| Completion evidence | Queue/memory bound, fairness, timeout and typed overload. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-14"></a>

### PLT.14 — Disconnect, cancel and retry semantics

**Outcome.** Effect certainty, stable command/receipt identity and cancellation are preserved across helper crashes; replay only when explicitly allowed; kill before/after commit and lost-ack scenarios resolve to typed unknown-effect outcomes, in-memory only (durable receipts remain WP07/21/52 territory per [WP-04.01](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.01)'s own gate).

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-14` and ledger record `ledger/tasks/plt-14.md` in the Plan repository; task branch `task/plt-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-08.05](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.05) — full |
| Provides | ipc-cancel-retry |
| Start prerequisites | **artifact** [PLT.09](#task-plt-09) — transport. *Why:* cancellation/retry wrap the transport call lifecycle.<br>**artifact** [FND.02](foundation.md#task-fnd-02) — effect-certainty/Outcome types. *Why:* unknown-effect classification is a [WP-04.01](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.01) type, not invented locally. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.16](#task-plt-16) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Validation | Offline/local tests: kill before/after commit, lost ack and unknown effect. |
| Completion evidence | Kill before/after commit, lost ack and unknown effect. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-15"></a>

### PLT.15 — Brokered large data over the sandbox boundary

**Outcome.** Bounded verified chunks over annex-09 sandbox resources/buffers, parent-authorized only; no direct product-to-product transfer ticket.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-15` and ledger record `ledger/tasks/plt-15.md` in the Plan repository; task branch `task/plt-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-08.06](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.06) — full |
| Provides | ipc-brokered-data |
| Start prerequisites | **artifact** [PLT.09](#task-plt-09) — transport. *Why:* brokered transfer is a call pattern over the same transport.<br>**contract** [CON.04](contracts.md#task-con-04) — ContentSandboxService/slot-grant wire shapes in contracts/09-local-grpc-and-sandbox.md. *Why:* the exact grant/seal/ack/cancel lifecycle is fixed by the published contract, not invented here. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [PLT.45](#task-plt-45) — the real ContentSandbox helper actually using these brokered buffers. *Why:* [WP-08.06](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.06) implements the generic broker mechanism; PLT.45 ([WP-11.09](../../work-packages/11-security-foundation.md#rule-wp-11.09)) is the first real consumer that proves it end to end with a hostile parser. |
| Unblocks | [PLT.16](#task-plt-16), [PLT.24](#task-plt-24), [PLT.45](#task-plt-45) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Validation | Offline/local tests: wrong resource grant, range/hash/expiry/cancel and orphan cleanup. |
| Completion evidence | Wrong resource grant, range/hash/expiry/cancel and orphan cleanup. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-16"></a>

### PLT.16 — Publish LocalRpc package and verify real integration

**Outcome.** ArcForges.LocalRpc is packed, admitted, published, and independently consumed; all owned actions/schemas/public interfaces and tests are complete with applicable UX acceptance ledger rows recorded.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-16` and ledger record `ledger/tasks/plt-16.md` in the Plan repository; task branch `task/plt-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-08.90](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.90) — full |
| Provides | localrpc-package |
| Start prerequisites | **artifact** [PLT.09](#task-plt-09) — transport. *Why:* publish needs the complete substep set.<br>**artifact** [PLT.10](#task-plt-10) — endpoint identity. *Why:* same.<br>**artifact** [PLT.11](#task-plt-11) — registration. *Why:* same.<br>**artifact** [PLT.12](#task-plt-12) — routing. *Why:* same.<br>**artifact** [PLT.13](#task-plt-13) — bounds. *Why:* same.<br>**artifact** [PLT.14](#task-plt-14) — cancel/retry. *Why:* same.<br>**artifact** [PLT.15](#task-plt-15) — brokered data. *Why:* same. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): offline verify plus policy tests; real multi-process OS-stream evidence beyond the repo's own build-machine tests is local opt-in. |
| Completion evidence | Exact artifact/consumer and applicable UX acceptance ledger. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: LocalRpc not in packages.json. |

<a id="task-plt-17"></a>

### PLT.17 — Application identity and in-process composition

**Outcome.** AppIdentity/InstallationIdentity/InstanceIdentity bound to each application composition root; two products on one device keep separate sessions/history/capabilities; forged/missing target refuses; no running-product registry or shared Hub.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-17` and ledger record `ledger/tasks/plt-17.md` in the Plan repository; task branch `task/plt-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-09.00](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.00) — full |
| Provides | app-identity-composition |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — descriptor contract types (App/Installation/Instance identity wire shapes). *Why:* [WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09)'s own header lists [WP-03](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03) output as the descriptor contract types this package needs.<br>**artifact** [FND.01](foundation.md#task-fnd-01) — identity primitive types. *Why:* these identities are built on [WP-04](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04)'s identity adapters. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.01](app-composition.md#task-app-01), [EXE.01](execution.md#task-exe-01), [PLT.18](#task-plt-18), [PLT.19](#task-plt-19), [PLT.21](#task-plt-21), [PLT.22](#task-plt-22), [PLT.25](#task-plt-25) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline unit tests: two-product separation, forged/missing target refusal. |
| Completion evidence | Identity lifecycle matrix. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Neither ArcForges.Capabilities nor ArcForges.Contributions exist anywhere in the repository tree yet. |
| Notes | The old header lists WP09 upstream as '03, 08'. Reading contracts/02-local-rpc-operations.md closely: product capability ports (ICapabilityProvider etc.) are IN-PROCESS typed calls; only helper/extension children use the [WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) Named Pipe/UDS transport. WP-09.00-09.06 (identity, registration, selection, availability, context, resources, navigation/health) do not need [WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) at all. Recommend narrowing the 08->09 edge to apply only where PLT.24 (invocation pipeline) routes to an admitted child - see PLT.24's own start edges. |

<a id="task-plt-18"></a>

### PLT.18 — Static contribution registration

**Outcome.** Capability/context/artifact/lifecycle/deep-link handlers register inside the owning process through generated descriptors and explicit composition; duplicate IDs, wrong owner, unavailable child, undeclared tool schema and cross-product registration all refuse; registration is idempotent and survives restart.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-18` and ledger record `ledger/tasks/plt-18.md` in the Plan repository; task branch `task/plt-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-09.01](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.01) — full<br>[WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09) Contribution/registration state durable across restarts (SS6 impacts) — package-level obligation contribution |
| Provides | contribution-registration |
| Start prerequisites | **artifact** [PLT.17](#task-plt-17) — application identity/composition root. *Why:* contributions register against a specific app's composition root. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.01](native.md#task-nat-01), [NOTES.12](arcnotes.md#task-notes-12), [PLT.25](#task-plt-25) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Contributions/**` |
| Validation | Offline tests: duplicate IDs, wrong owner, unavailable child, undeclared tool schema, cross-product registration refusal; registration survives a simulated restart against the persistence layer PLT.01/PLT.05 provide. |
| Completion evidence | Registration idempotency and namespace refusal results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-19"></a>

### PLT.19 — Capability registry and selection

**Outcome.** The wire CapabilityDescriptor/OperationBinding/effect/locus/context/cancellation schema is implemented with a complete initial first-party binding matrix; enumerated bindings are validated against declared Contracts methods; unsupported major, inconsistent pureRead/write classification, readiness mismatch and ambiguous target all reject.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-19` and ledger record `ledger/tasks/plt-19.md` in the Plan repository; task branch `task/plt-19` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-09.02](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.02) — full |
| Provides | capability-registry-selection; capability-descriptor-type |
| Start prerequisites | **artifact** [PLT.17](#task-plt-17) — identity/composition. *Why:* the registry is scoped per application instance.<br>**contract** [CON.91](contracts.md#task-con-91) — CapabilityDescriptor/OperationBinding wire schema. *Why:* BR of WP09 says 'no implementer invents binding fields or capability behavior to join products' - the schema is Contracts-owned. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.00](extensions.md#task-ext-00), [PLT.20](#task-plt-20), [PLT.24](#task-plt-24), [PLT.25](#task-plt-25), [PLT.37](#task-plt-37) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**` |
| Validation | Offline tests: enumerate expected bindings, reject missing/extra methods/unsupported major/inconsistent classification/readiness mismatch/ambiguous target. |
| Completion evidence | Selection priority, determinism and explainability results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-20"></a>

### PLT.20 — Actions and availability

**Outcome.** Actions are computed from capabilities plus current context, side-effect free, cheap enough for UI enumeration; unavailability always yields a typed reason across permission/entitlement/health/context/version causes.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-20` and ledger record `ledger/tasks/plt-20.md` in the Plan repository; task branch `task/plt-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-09.03](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.03) — full |
| Provides | action-availability; availability-result-type |
| Start prerequisites | **artifact** [PLT.19](#task-plt-19) — capability registry. *Why:* availability is computed from registered capabilities plus context. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.24](#task-plt-24), [PLT.25](#task-plt-25), [PLT.28](#task-plt-28) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**` |
| Validation | Offline tests: availability tests across permission/entitlement/health/context/version reasons; purity test asserting no side effect. |
| Completion evidence | Availability reason matrix and purity assertion. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-21"></a>

### PLT.21 — Context providers and freezing

**Outcome.** Context providers contribute typed context; at invocation the context is frozen into an immutable snapshot carried with the invocation; a later live-context change never affects an in-flight invocation; oversized context is refused explicitly.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-21` and ledger record `ledger/tasks/plt-21.md` in the Plan repository; task branch `task/plt-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-09.04](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.04) — full |
| Provides | context-freezing; frozen-context-type |
| Start prerequisites | **artifact** [PLT.17](#task-plt-17) — identity/composition. *Why:* context is scoped to the owning application instance. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.06](app-composition.md#task-app-06), [PLT.24](#task-plt-24), [PLT.25](#task-plt-25), [PLT.42](#task-plt-42) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**` |
| Validation | Offline tests: mutation-during-invocation test asserting frozen snapshot used; size-bounding test asserting oversized context is refused rather than truncated. |
| Completion evidence | Context freezing and size-bound results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-22"></a>

### PLT.22 — Resources and artifacts resolution

**Outcome.** Resource resolution from reference to access honours ownership and floating-versus-pinned distinction; artifact handlers register per kind; a reference never carries a path/pointer/handle; resolution re-checks permission at access time.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-22` and ledger record `ledger/tasks/plt-22.md` in the Plan repository; task branch `task/plt-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-09.05](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.05) — full |
| Provides | resource-artifact-resolution; resource-ref-type |
| Start prerequisites | **artifact** [PLT.05](#task-plt-05) — managed resource store's identity-to-location resolution. *Why:* ResourceRef resolution at the capability layer is built on the persistence-level ManagedResourceRef PLT.05 defines; this is a real cross-lane (persistence->capabilities) dependency within the DesktopPlatform repository.<br>**artifact** [PLT.17](#task-plt-17) — identity/composition. *Why:* resource ownership is per-application. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.06](app-composition.md#task-app-06), [PLT.23](#task-plt-23), [PLT.25](#task-plt-25) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**` |
| Validation | Offline tests: resolution across owner-present/owner-absent/permission-denied/version-pinned cases; structural test that a reference cannot carry a path. |
| Completion evidence | Resource resolution matrix and structural path prohibition. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-23"></a>

### PLT.23 — Own navigation, hints and health

**Outcome.** Artifact opens and deep links route to the owning application handler; bounded in-process state hints cause authoritative rereads; invalid ownership, missing content, expired child cursor, restart and duplicate hint all recover without launching another product.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-23` and ledger record `ledger/tasks/plt-23.md` in the Plan repository; task branch `task/plt-23` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-09.06](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.06) — full |
| Provides | own-navigation-health; health-dimension-type |
| Start prerequisites | **artifact** [PLT.22](#task-plt-22) — resource/artifact resolution. *Why:* navigation opens resolved artifacts. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.25](#task-plt-25), [PLT.51](#task-plt-51) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**` |
| Validation | Offline tests: invalid ownership, missing content, expired child cursor, restart, duplicate hint recovery. |
| Completion evidence | Deep-link hostile-input, event and health results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-24"></a>

### PLT.24 — Invocation pipeline

**Outcome.** The end-to-end path resolve -> check availability -> freeze context -> authorize -> invoke -> validate result -> record is the ONLY route to a capability; every failure maps to the closed semantic error set; every invocation is traced.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-24` and ledger record `ledger/tasks/plt-24.md` in the Plan repository; task branch `task/plt-24` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-09.07](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.07) — all work except the parts mapped to PLT.57 |
| Provides | invocation-pipeline |
| Start prerequisites | **artifact** [PLT.19](#task-plt-19) — capability registry/selection. *Why:* resolve step needs the registry.<br>**artifact** [PLT.20](#task-plt-20) — availability. *Why:* check-availability step.<br>**artifact** [PLT.21](#task-plt-21) — context freezing. *Why:* freeze-context step. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [PLT.15](#task-plt-15) — real LocalRpc brokered routing for the subset of invocations that target an admitted helper/extension child. *Why:* the core in-process invocation path (most capabilities) never touches [WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08); only the child-routing branch does, and that branch's real proof is later (WP41 extension platform). |
| Unblocks | [APP.02](app-composition.md#task-app-02), [PLT.25](#task-plt-25), [PLT.57](#task-plt-57) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline tests: policy test asserting no bypass route exists; error-mapping tests for every semantic error; tracing test. |
| Completion evidence | Pipeline bypass-prohibition, error-mapping and tracing results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-25"></a>

### PLT.25 — Publish Capabilities/Contributions packages and verify real integration

**Outcome.** ArcForges.Capabilities (and the Contributions internals it packages) is packed, admitted, published, and independently consumed; owner refuses invalid/stale invocations and opaque references do not grant access.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-25` and ledger record `ledger/tasks/plt-25.md` in the Plan repository; task branch `task/plt-25` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-09.90](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.90) — full |
| Provides | capabilities-package |
| Start prerequisites | **artifact** [PLT.17](#task-plt-17) — identity/composition. *Why:* publish needs the complete substep set.<br>**artifact** [PLT.18](#task-plt-18) — contribution registration. *Why:* same.<br>**artifact** [PLT.19](#task-plt-19) — registry/selection. *Why:* same.<br>**artifact** [PLT.20](#task-plt-20) — actions/availability. *Why:* same.<br>**artifact** [PLT.21](#task-plt-21) — context freezing. *Why:* same.<br>**artifact** [PLT.22](#task-plt-22) — resources/artifacts. *Why:* same.<br>**artifact** [PLT.23](#task-plt-23) — navigation/health. *Why:* same.<br>**artifact** [PLT.24](#task-plt-24) — invocation pipeline. *Why:* same.<br>**artifact** [PLT.57](#task-plt-57) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:eng/packaging/packages.json`<br>`DesktopPlatform:eng/version-sources.json` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): offline verify/policy tests; real cross-product UI acceptance is deferred to product WPs (14/18/33/36) that actually consume this package. |
| Completion evidence | Owned artifact and real-integration receipt per the [WP-09.90](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.90) template. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Not in packages.json. |

<a id="task-plt-26"></a>

### PLT.26 — Token system and theming

**Outcome.** Semantic tokens for colour/typography/spacing/radius/elevation/motion with light/dark/high-contrast themes and first-class density modes; no component references a raw literal.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-26` and ledger record `ledger/tasks/plt-26.md` in the Plan repository; task branch `task/plt-26` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-10.00](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.00) — full<br>[WP-10](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10) Reconciliation of the five legacy src/BuildingBlocks/ArcForges.Desktop.{Experience,Graphics,Preview,RichContent,Text} scaffold projects per [WP-01.02](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.02) into DesignSystem/Shell — package-level obligation contribution |
| Provides | design-tokens |
| Start prerequisites | **artifact** [PRF.01](runtime-proofs.md#task-prf-01) — a proven Avalonia Native AOT publish with zero trim/AOT diagnostics. *Why:* WP10's own header lists [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) output as 'the AOT proof and the control admission process'; every control this package introduces inherits [V-05a](../../../assurance/phase-1-official-verification.md#rule-v-05a). Owned by the native and runtime-proof lanes. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.03](arcnotes.md#task-notes-03), [NOTES.04](arcnotes.md#task-notes-04), [PLT.27](#task-plt-27), [PLT.29](#task-plt-29), [PLT.31](#task-plt-31), [PLT.35](#task-plt-35) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.DesignSystem/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline tests: policy test asserting no raw colour/size literal in component code; contrast tests across every theme; density snapshot suite. Real AOT publish-with-zero-diagnostics evidence is local opt-in, recorded at PLT.34/PLT.35. |
| Completion evidence | Raw-literal policy result and contrast reports per theme. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/DesignSystem/ does not exist. Five legacy placeholder projects exist today at src/BuildingBlocks/ArcForges.Desktop.{Experience,Graphics,Preview,RichContent,Text}/ (each a bare AssemblyPlaceholder.cs, disposition 'Keep' in eng/policy/reconciliation/current.json). Per architecture 27 and [WP-01.02](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.02), these are the mechanism-only survivors slated to fold into DesignSystem/Shell; this task's real starting point includes deciding what, if anything, from those five carries forward versus a clean rebuild. |

<a id="task-plt-27"></a>

### PLT.27 — Windows, panels and layout

**Outcome.** Multi-window-per-instance window model, dockable/collapsible panel host, device-local layout persistence resilient to a missing panel or changed screen configuration.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-27` and ledger record `ledger/tasks/plt-27.md` in the Plan repository; task branch `task/plt-27` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-10.01](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.01) — full<br>[WP-10](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10) Reconciliation of the five legacy src/BuildingBlocks/ArcForges.Desktop.{Experience,Graphics,Preview,RichContent,Text} scaffold projects per [WP-01.02](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.02) into DesignSystem/Shell — package-level obligation contribution |
| Provides | window-panel-layout |
| Start prerequisites | **artifact** [PLT.26](#task-plt-26) — token system. *Why:* layout chrome is built from the token set. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NOTES.03](arcnotes.md#task-notes-03), [NOTES.04](arcnotes.md#task-notes-04), [NOTES.05](arcnotes.md#task-notes-05), [PLT.28](#task-plt-28), [PLT.30](#task-plt-30), [PLT.33](#task-plt-33), [PLT.35](#task-plt-35), [SLATE.22](arcslate.md#task-slate-22), [SLATE.25](arcslate.md#task-slate-25) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline tests: restore tests across missing panel, changed display arrangement, corrupted layout state; device-local assertion. |
| Completion evidence | Layout restore matrix. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/DesignSystem/ArcForges.Desktop.Shell does not exist. |

<a id="task-plt-28"></a>

### PLT.28 — Command system

**Outcome.** Command registry with availability, shortcut binding, command palette and conflict detection; command availability is computed from the same evaluation the capability model uses so command and capability never disagree.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-28` and ledger record `ledger/tasks/plt-28.md` in the Plan repository; task branch `task/plt-28` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-10.02](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.02) — full |
| Provides | command-system |
| Start prerequisites | **artifact** [PLT.27](#task-plt-27) — window/panel host. *Why:* commands attach to shell chrome (palette, menus).<br>**artifact** [PLT.20](#task-plt-20) — capability availability evaluation ([WP-09.03](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.03)). *Why:* explicit BR: command availability must reuse [WP-09.03](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.03)'s evaluation so the two never disagree; this is a real cross-lane (capabilities->shell) dependency within the DesktopPlatform repository, distinct from the rest of WP10 which does not need WP09 at all. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.32](#task-plt-32), [PLT.35](#task-plt-35), [SLATE.22](arcslate.md#task-slate-22) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**` |
| Validation | Offline tests: shortcut conflict detection; availability agreement tests against the capability model; palette search relevance tests. |
| Completion evidence | Shortcut conflict and availability agreement results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |
| Notes | The old [WP-10](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10) header claims upstream '06, 09' for the whole package. Only this substep genuinely needs [WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09); PLT.26/27/29/30/31/32/33/34 do not. |

<a id="task-plt-29"></a>

### PLT.29 — Scoped settings

**Outcome.** Fixed scope resolution (application/workspace/device/instance), typed schemas, migration on schema change, explainable effective value; device-scoped settings never sync.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-29` and ledger record `ledger/tasks/plt-29.md` in the Plan repository; task branch `task/plt-29` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-10.03](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.03) — full |
| Provides | scoped-settings |
| Start prerequisites | **artifact** [PLT.26](#task-plt-26) — token/theming groundwork. *Why:* loosely - settings UI reuses shell chrome; can largely proceed in parallel with PLT.27/28 once PLT.26 lands.<br>**artifact** [PLT.04](#task-plt-04) — migration runner pattern ([WP-07.03](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.03)). *Why:* settings schema migration reuses the same migration idiom persistence establishes, applied to a device-local settings store rather than product canonical data. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.35](#task-plt-35) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**` |
| Validation | Offline tests: resolution order tests across every scope combination; explainability tests; migration test. |
| Completion evidence | Settings resolution and explainability results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-30"></a>

### PLT.30 — Attention and notification model

**Outcome.** Attention items classified by durability; a durable item (pending approval, failed task) persists until resolved regardless of a missed transient notification; lock-screen/system-notification content is non-sensitive by default.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-30` and ledger record `ledger/tasks/plt-30.md` in the Plan repository; task branch `task/plt-30` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-10.04](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.04) — full |
| Provides | attention-model |
| Start prerequisites | **artifact** [PLT.27](#task-plt-27) — window/panel host. *Why:* attention surfaces render inside shell chrome. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.35](#task-plt-35) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**` |
| Validation | Offline tests: missed-notification test asserting durable state survives; sensitivity test on notification content. |
| Completion evidence | Missed-notification durability result. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-31"></a>

### PLT.31 — Error presentation

**Outcome.** Errors are presented from the reason-code registry with a human-readable statement, retry guidance and a support reference identifier; a raw exception message never reaches the user.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-31` and ledger record `ledger/tasks/plt-31.md` in the Plan repository; task branch `task/plt-31` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-10.05](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.05) — full |
| Provides | error-presentation |
| Start prerequisites | **artifact** [PLT.26](#task-plt-26) — token system. *Why:* error surfaces are themed shell chrome.<br>**artifact** [FND.05](foundation.md#task-fnd-05) — reason-code registry. *Why:* every presented error is keyed off a registered reason code; this is a direct FND->Shell contract dependency. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.35](#task-plt-35), [PLT.52](#task-plt-52) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**` |
| Validation | Offline tests: no raw exception text displayed; coverage that every registered reason code has a message. |
| Completion evidence | Raw-exception prohibition and reason-code coverage. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-32"></a>

### PLT.32 — Lifecycle, menus and shutdown

**Outcome.** Start-up sequence within budget; single-instance routing; shutdown prompts stating consequences when work is running/unsaved; menu contribution from the command registry.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-32` and ledger record `ledger/tasks/plt-32.md` in the Plan repository; task branch `task/plt-32` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-10.06](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.06) — full |
| Provides | lifecycle-shutdown |
| Start prerequisites | **artifact** [PLT.28](#task-plt-28) — command registry. *Why:* menus contribute from the command registry. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.07](app-composition.md#task-app-07), [PLT.35](#task-plt-35), [SCOPE.09](arcscope.md#task-scope-09), [UPD.03](updater.md#task-upd-03) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**` |
| Validation | Offline tests: startup budget measurement per product host (local perf harness, not hosted CI); shutdown-during-work test; single-instance routing test. |
| Completion evidence | Startup budget measurements and shutdown-during-work result. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-33"></a>

### PLT.33 — Accessibility and localisation baseline

**Outcome.** Every shell surface carries assistive-technology semantics, correct focus order and keyboard reachability; all strings externalised; RTL layout supported structurally.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-33` and ledger record `ledger/tasks/plt-33.md` in the Plan repository; task branch `task/plt-33` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-10.07](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.07) — full |
| Provides | accessibility-l10n |
| Start prerequisites | **artifact** [PLT.27](#task-plt-27) — window/panel/layout. *Why:* focus order and keyboard reachability are properties of the layout model. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.35](#task-plt-35) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**`<br>`DesktopPlatform:tests/DesktopUiTests/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline automated accessibility checks plus pseudo-localisation pass and RTL layout pass run in CI; the dated manual assistive-technology verification is explicit local opt-in per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (device/GUI testing is excluded from hosted CI). |
| Completion evidence | Accessibility automated plus dated manual record; pseudo-localisation report. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists; tests/DesktopUiTests does not exist yet. |

<a id="task-plt-34"></a>

### PLT.34 — Third-party control admission

**Outcome.** Every third-party control the shell uses passes a real AOT publish proof with zero diagnostics before adoption, with a recorded licence position per control.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-34` and ledger record `ledger/tasks/plt-34.md` in the Plan repository; task branch `task/plt-34` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-10.08](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.08) — full |
| Provides | third-party-control-admission |
| Start prerequisites | **artifact** [PRF.01](runtime-proofs.md#task-prf-01) — the established AOT-publish-with-zero-diagnostics harness/process. *Why:* this substep applies the same proof methodology [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) establishes to each additional control the shell adopts; it is ongoing (a standing admission process), not a one-time gate. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.35](#task-plt-35), [PRF.09](runtime-proofs.md#task-prf-09) |
| Write scope | `DesktopPlatform:src/DesignSystem/**`<br>`DesktopPlatform:docs/**` |
| Validation | Per-control real AOT publish proof - genuinely requires local/CI compilation (Windows/Linux AOT publish IS in the retained CI scope per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)), so this can run in CI unlike device/GUI checks. |
| Completion evidence | Per-control AOT proofs and licence records. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: No third-party controls beyond bare Avalonia itself have been evaluated yet; [VG-03](../../../assurance/open-gates-register.md#rule-vg-03) in open-gates-register.md is OPEN. |

<a id="task-plt-35"></a>

### PLT.35 — Publish DesignSystem/Shell packages and verify real integration

**Outcome.** ArcForges.DesignSystem and ArcForges.Desktop.Shell are packed, admitted, published, and independently consumed; each app is shown to restore only the packages/mechanisms it needs.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-35` and ledger record `ledger/tasks/plt-35.md` in the Plan repository; task branch `task/plt-35` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-10](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-10.90](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.90) — all work except the parts mapped to PLT.56 |
| Provides | designsystem-shell-packages |
| Start prerequisites | **artifact** [PLT.26](#task-plt-26) — tokens. *Why:* publish needs the complete substep set.<br>**artifact** [PLT.27](#task-plt-27) — windows/panels. *Why:* same.<br>**artifact** [PLT.28](#task-plt-28) — commands. *Why:* same.<br>**artifact** [PLT.29](#task-plt-29) — settings. *Why:* same.<br>**artifact** [PLT.30](#task-plt-30) — attention. *Why:* same.<br>**artifact** [PLT.31](#task-plt-31) — error presentation. *Why:* same.<br>**artifact** [PLT.32](#task-plt-32) — lifecycle/menus. *Why:* same.<br>**artifact** [PLT.33](#task-plt-33) — a11y/l10n. *Why:* same.<br>**artifact** [PLT.34](#task-plt-34) — control admission. *Why:* same. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [PLT.56](#task-plt-56) — ArcNotes actually composing the shell for its own product UI. *Why:* 'independent app restores only needed packages' is only truly proven once a real product consumes it; WP10's own gate accepts a clean package-only consumer diagnostic as sufficient for THIS package's completion, with full product UX acceptance remaining product-owned. |
| Unblocks | [PLT.56](#task-plt-56) |
| Write scope | `DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): offline verify/policy tests plus the retained AOT-publish gate. |
| Completion evidence | Owned artifact and real-integration receipt per [WP-10.90](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.90). |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Not in packages.json. |

<a id="task-plt-36"></a>

### PLT.36 — Principals and the actor chain

**Outcome.** Every operation carries a complete actor chain (human principal, device, installation, session, any acting agent/extension) constructed once at the entry point and flowing through every layer without reconstruction; no operation reaches an enforcement point without it.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-36` and ledger record `ledger/tasks/plt-36.md` in the Plan repository; task branch `task/plt-36` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-11.00](../../work-packages/11-security-foundation.md#rule-wp-11.00) — full |
| Provides | actor-chain |
| Start prerequisites | **artifact** [FND.01](foundation.md#task-fnd-01) — identity primitive types. *Why:* the actor chain is composed of [WP-04](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04) typed identifiers. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.38](#task-plt-38), [PLT.40](#task-plt-40), [PLT.44](#task-plt-44), [PLT.46](#task-plt-46) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**` |
| Validation | Offline unit tests: propagation test asserting the chain survives every hop including queue/process boundaries; completeness test. |
| Completion evidence | Actor chain propagation and completeness results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/BuildingBlocks/ArcForges.Security/ is a bare AssemblyPlaceholder.cs project today. |

<a id="task-plt-37"></a>

### PLT.37 — Risk model and classification

**Outcome.** R0 to R4 with runtime modifiers; every capability declares a base risk; modifiers raise it based on scope/target/reversibility/egress/actor kind; effective risk is computed, explainable and monotonic (never lowered).

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-37` and ledger record `ledger/tasks/plt-37.md` in the Plan repository; task branch `task/plt-37` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-11.01](../../work-packages/11-security-foundation.md#rule-wp-11.01) — full |
| Provides | risk-model |
| Start prerequisites | **artifact** [PLT.19](#task-plt-19) — CapabilityDescriptor carrying risk level/trust requirement/side-effect class ([WP-09.02](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.02)). *Why:* [WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09)'s own [BR-10](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-br-10) states 'a capability descriptor is richer than a tool description: it carries risk level, trust requirement, side-effect class, reversibility and approval posture' - the risk model classifies against fields the capability descriptor already declares. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.38](#task-plt-38), [PLT.39](#task-plt-39), [PLT.46](#task-plt-46) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**` |
| Validation | Offline unit tests: classification tests across every modifier combination; monotonicity test. |
| Completion evidence | Risk classification and monotonicity matrix. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-38"></a>

### PLT.38 — Decision pipeline and the four enforcement points

**Outcome.** The fourteen-step decision pipeline implemented once and invoked at each of the four enforcement points (caller pre-check, transport boundary, service-side decision, owner-side final validation always last); every step produces a typed outcome; a refusal names the failing step and reason code; the pipeline is unbypassable.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-38` and ledger record `ledger/tasks/plt-38.md` in the Plan repository; task branch `task/plt-38` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-11.02](../../work-packages/11-security-foundation.md#rule-wp-11.02) — all work except the parts mapped to PLT.57 |
| Provides | decision-pipeline; security-decision-type |
| Start prerequisites | **artifact** [PLT.36](#task-plt-36) — actor chain. *Why:* every pipeline step operates on the actor chain.<br>**artifact** [PLT.37](#task-plt-37) — risk model. *Why:* the pipeline classifies effective risk as one of its steps.<br>**artifact** [PLT.10](#task-plt-10) — LocalRpc session handshake ([WP-08.01](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.01)/08.02). *Why:* enforcement point 2 ('transport boundary') is literally the local IPC handshake per architecture/08-security-architecture.md SS2; the pipeline's transport-boundary step wraps this real mechanism, not a placeholder. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.02](app-composition.md#task-app-02), [GOV.16](governance.md#task-gov-16), [PLT.41](#task-plt-41), [PLT.43](#task-plt-43), [PLT.46](#task-plt-46), [PLT.57](#task-plt-57) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline unit tests: step-coverage test asserting every step runs; refusal matrix producing a distinct reason code per failing step; bypass test. |
| Completion evidence | Pipeline bypass, step-coverage and refusal matrix. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-39"></a>

### PLT.39 — Approval, steering and step-up

**Outcome.** Approval requests with bounded lifetime, durable pending state and explicit outcome; steering adjusts a running operation without granting authority; step-up challenges for enumerated sensitive operations; local presence required for the highest risk class, biometric app-unlock never substituting.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-39` and ledger record `ledger/tasks/plt-39.md` in the Plan repository; task branch `task/plt-39` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-11.03](../../work-packages/11-security-foundation.md#rule-wp-11.03) — full |
| Provides | approval-stepup; approval-request-type |
| Start prerequisites | **artifact** [PLT.37](#task-plt-37) — risk model. *Why:* step-up/local-presence requirements are keyed off risk class.<br>**artifact** [PLT.01](#task-plt-01) — durable persistence for the approval object. *Why:* [AP-01](../../../architecture/05-cloud-architecture.md#rule-ap-01) requires an approval to survive an application restart and a device change - it must be a durable persisted object, not in-memory. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.05](app-composition.md#task-app-05), [AST.12](assistant.md#task-ast-12), [DEV.06](device-bridge.md#task-dev-06), [EXE.06](execution.md#task-exe-06), [PLT.46](#task-plt-46) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**` |
| Validation | Offline tests: approval expiry, duplicate-approval, approval-after-cancel tests; steering-cannot-escalate test; biometric-does-not-satisfy-step-up test. Real OS biometric/local-presence hardware evidence is local opt-in. |
| Completion evidence | Approval, steering and step-up results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-40"></a>

### PLT.40 — Per-application secrets and session isolation

**Outcome.** Platform secure storage/broker primitives scoped to realm/account/product/installation with no cross-product SSO endpoint; SecretRef Use != Reveal; connector child grants are foreground/definition-bound and cannot export raw secrets; own sign-out leaves other apps/local data intact.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-40` and ledger record `ledger/tasks/plt-40.md` in the Plan repository; task branch `task/plt-40` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-11.04](../../work-packages/11-security-foundation.md#rule-wp-11.04) — full<br>[WP-11](../../work-packages/11-security-foundation.md#rule-wp-11) Application credential boundary: shared security packages use the caller application/installation storage namespace; deny sibling credential reads; no device-SSO signing broker — package-level obligation contribution |
| Provides | secret-broker; secret-ref-type |
| Start prerequisites | **artifact** [PLT.36](#task-plt-36) — actor chain. *Why:* secret scoping is per realm/account/product/installation, which the actor chain carries. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.18](cloud.md#task-cloud-18) — real Cloud authentication. *Why:* [WP-11.04](../../work-packages/11-security-foundation.md#rule-wp-11.04)'s own gate explicitly says 'Cloud authentication arrives in WP22'; this task supplies OS secret-store adapters and isolation only. |
| Unblocks | [CLOUD.18](cloud.md#task-cloud-18), [PLT.46](#task-plt-46), [PLT.49](#task-plt-49), [UPD.01](updater.md#task-upd-01) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security.Secrets/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline tests where possible; real OS secure-storage round trips (Windows Credential Manager/keychain/keystore) are local opt-in per platform, recorded separately from CI. |
| Completion evidence | Secret structural prohibitions and platform round-trip results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ArcForges.Security.Secrets does not exist as a separate project yet; the WP11 architecture doc names it as a new project distinct from the single 'ArcForges.Security' package registry row -. |

<a id="task-plt-41"></a>

### PLT.41 — Egress control

**Outcome.** Every outbound data transfer is its own egress decision, distinct from read access, recording data class/destination/authority; a denied egress produces a typed refusal and every egress is audited.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-41` and ledger record `ledger/tasks/plt-41.md` in the Plan repository; task branch `task/plt-41` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-11.05](../../work-packages/11-security-foundation.md#rule-wp-11.05) — full |
| Provides | egress-control |
| Start prerequisites | **artifact** [PLT.38](#task-plt-38) — decision pipeline. *Why:* egress is evaluated as a distinct authorization within the same pipeline machinery. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.06](app-composition.md#task-app-06), [PLT.46](#task-plt-46) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**` |
| Validation | Offline tests: matrix asserting read access alone never authorizes egress; destination allowlist tests; audit assertion. |
| Completion evidence | Egress authorization matrix and audit assertions. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-42"></a>

### PLT.42 — Instruction provenance

**Outcome.** Every input that can carry instructions (model output, extension output, retrieved content, imported documents, deep links, catalog metadata) is marked with its provenance; untrusted provenance can be processed but never gains authority to trigger an operation unapproved.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-42` and ledger record `ledger/tasks/plt-42.md` in the Plan repository; task branch `task/plt-42` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-11.06](../../work-packages/11-security-foundation.md#rule-wp-11.06) — full |
| Provides | instruction-provenance |
| Start prerequisites | **artifact** [PLT.21](#task-plt-21) — context freezing ([WP-09.04](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.04)). *Why:* provenance marking travels with the same context objects the capability model freezes at invocation. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.05](assistant.md#task-ast-05), [PLT.46](#task-plt-46) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**` |
| Validation | Offline tests: injection corpus asserting untrusted content cannot cause an unapproved operation; marking-completeness test over every input path. |
| Completion evidence | Injection corpus results and marking coverage. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-43"></a>

### PLT.43 — Capability leases and trust

**Outcome.** A delegation creates a lease with scope/expiry/revocation, enforced at use not only at issue; typed trust levels evaluated at defined points; trust never substitutes for permission.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-43` and ledger record `ledger/tasks/plt-43.md` in the Plan repository; task branch `task/plt-43` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-11.07](../../work-packages/11-security-foundation.md#rule-wp-11.07) — full |
| Provides | capability-leases |
| Start prerequisites | **artifact** [PLT.38](#task-plt-38) — decision pipeline. *Why:* lease checks are a pipeline step.<br>**artifact** [PLT.01](#task-plt-01) — durable persistence for lease state. *Why:* leases must be revocable mid-operation and survive restart; needs a durable store. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [DEV.03](device-bridge.md#task-dev-03), [PLT.46](#task-plt-46) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**` |
| Validation | Offline tests: lease expiry-at-use, revocation-mid-operation, scope-escalation-attempt tests; trust-never-grants-permission test. |
| Completion evidence | Lease expiry, revocation and trust-separation results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-44"></a>

### PLT.44 — Append-only audit subsystem

**Outcome.** Append-only audit append/query with a dedicated policy-retention maintenance authority; ordinary roles cannot UPDATE/DELETE; audited retention purge removes only expired unheld partitions under declared policy; complete separation from telemetry.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-44` and ledger record `ledger/tasks/plt-44.md` in the Plan repository; task branch `task/plt-44` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-11.08](../../work-packages/11-security-foundation.md#rule-wp-11.08) — full |
| Provides | audit-subsystem; audit-event-type |
| Start prerequisites | **artifact** [PLT.36](#task-plt-36) — actor chain. *Why:* every audit event records the full actor chain per architecture/08 SS11 [AD-04](../../../architecture/08-security-architecture.md#rule-ad-04).<br>**artifact** [PLT.01](#task-plt-01) — persistence write path. *Why:* audit is a durable append-only store built on the same persistence foundation, in its own local_audit table per the desktop data model (SS1.5), kept separate from ordinary product tables. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.46](#task-plt-46) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security.Audit/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline tests: reject ordinary UPDATE/DELETE and forged retention role; approved expiry purge; legal hold; complete security events; telemetry separation test (also exercised jointly with PLT.49's redaction/separation evidence). |
| Completion evidence | Audit immutability, completeness and separation results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ArcForges.Security.Audit does not exist as a project yet (same naming-granularity note as PLT.40). |

<a id="task-plt-45"></a>

### PLT.45 — Content helper and OS-enforced isolation (ContentSandbox host)

**Outcome.** The first-party C# Native AOT ContentSandbox, generated gRPC broker/control bindings and all restricted RID launch profiles (Windows AppContainer+Job Object, Linux Landlock+seccomp, macOS App-Sandbox+XPC handoff) are built and solely owned here; ContentSandbox.Contracts/.Broker and the foundation Runtime.<rid> are published before WP13 consumes them; OS containment is proven with a deliberately hostile first-party test parser. Production PDF/image/media/OTIO libraries are WP13's job, never an upstream input here.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-45` and ledger record `ledger/tasks/plt-45.md` in the Plan repository; task branch `task/plt-45` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / XL · early risk proof |
| Obligations | [WP-11.09](../../work-packages/11-security-foundation.md#rule-wp-11.09) — full; production ContentSandbox helper, real transport<br>[WP-11](../../work-packages/11-security-foundation.md#rule-wp-11) Local gRPC closure (SS7): own actual signed restricted gRPC helper, launch-secret/OS-descriptor allowlist, hostile-fixture containment, private-copy/digest validation, ConnectorBroker security boundary (real connector providers are WP41) — package-level obligation contribution |
| Provides | content-helper-isolation; contentsandbox-host |
| Start prerequisites | **artifact** [PLT.15](#task-plt-15) — LocalRpc brokered large-data mechanism ([WP-08.06](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.06)). *Why:* the sandbox's slot grant/seal/ack/cancel lifecycle rides on the generic broker [WP-08.06](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.06) defines; ContentSandbox is the first real consumer.<br>**artifact** [PLT.09](#task-plt-09) — LocalRpc transport/restricted launch identity ([WP-08.00](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.00)/08.01). *Why:* the parent-created duplex stream and one-use launch secret are [WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) mechanisms this helper is launched through.<br>**contract** [CON.04](contracts.md#task-con-04) — ArcForges.Contracts.LocalRpc.Sandbox generated ContentSandboxService/session/grant schema. *Why:* contracts/09-local-grpc-and-sandbox.md SS6 fixes WP03 as publishing the complete schema before this stage; ContentSandbox.Contracts is only a facade over it. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [NAT.14](native.md#task-nat-14) — production PDF/image/media/OTIO parser composition rebuilt and signed on top of this same helper. *Why:* this task's own gate is explicit: 'WP13 later adds production parser composition to the same host and publishes a new immutable Runtime version; this stage has no reverse dependency on those parsers.' Full [PG-12](../../../assurance/open-gates-register.md#rule-pg-12)/[PG-22](../../../assurance/open-gates-register.md#rule-pg-22) closure additionally needs [WP-18.04](../../work-packages/18-arcnotes-document-core.md#rule-wp-18.04) (Notes PDF viewer) and [WP-37.01](../../work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.01)/41.00 real per-format/extension proofs. |
| Unblocks | [EXT.00](extensions.md#task-ext-00), [NAT.11](native.md#task-nat-11), [NAT.14](native.md#task-nat-14), [NAT.25](native.md#task-nat-25), [NOTES.09](arcnotes.md#task-notes-09), [NOTES.37](arcnotes.md#task-notes-37), [PLT.15](#task-plt-15), [PLT.46](#task-plt-46), [PLT.54](#task-plt-54) |
| Permitted substitutes | [SUB-hostile-test-parser](../substitutes.md#sub-hostile-test-parser) |
| Write scope | `DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox.Broker/**`<br>`DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox.Contracts/**`<br>`DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox/**` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) CRITICAL NUANCE: static/offline unit and policy tests run in CI, but the actual required evidence - real OS containment (AppContainer/Job Object denial, Landlock/seccomp denial, App-Sandbox/XPC denial, native crash/hang/memory-exhaustion/parent-death cleanup) - is device/OS-level execution that [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) explicitly excludes from hosted CI ('no macOS CI; no CI for... desktop GUI... sandbox execution'). This evidence MUST be recorded as local opt-in runs on each supported RID, per the ci-and-local-validation-policy.md and the architecture 24 rule 'a mocked launcher or same-user unrestricted child satisfies this gate: never'. |
| Completion evidence | Real child attempts at product-DB/token reads, outbound TCP/UDP/loopback, sibling-process access, spawn escape, oversized output; OS denial, resource bounds and parent-death cleanup on every supported RID. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/DesktopHelpers/ArcForges.ContentSandbox/ contains only Program.cs (a placeholder, per docs/runtime-ownership.md: 'the ContentSandbox scaffold is not accepted containment behavior'). ContentSandbox.Contracts and.Broker do not exist as separate projects yet. |
| Notes | This is the single highest-stakes early risk proof in the desktop platform foundation: [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) explicitly states a mocked launcher or unrestricted same-user child cannot close the gate, and the failure mode (hostile parsing escaping containment) would invalidate downstream trust in every product that later touches untrusted content (Notes PDF, Slate media/OTIO, extensions). Recommend prioritising this alongside PLT.03 (persistence recovery). Merged duplicate integration or closure task formerly proposed as CON.96. |

<a id="task-plt-46"></a>

### PLT.46 — Publish Security packages and verify real integration

**Outcome.** ArcForges.Security,.Security.Secrets and.Security.Audit are packed, admitted, published and independently consumed; the signed parent-bound helper and OS broker are packaged with only this stage's dependencies and the test-only parser fixture, no dependency back on WP13.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-46` and ledger record `ledger/tasks/plt-46.md` in the Plan repository; task branch `task/plt-46` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-11](../../work-packages/11-security-foundation.md#rule-wp-11) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-11.90](../../work-packages/11-security-foundation.md#rule-wp-11.90) — full |
| Provides | security-package |
| Start prerequisites | **artifact** [PLT.36](#task-plt-36) — actor chain. *Why:* publish needs the complete substep set.<br>**artifact** [PLT.37](#task-plt-37) — risk model. *Why:* same.<br>**artifact** [PLT.38](#task-plt-38) — decision pipeline. *Why:* same.<br>**artifact** [PLT.39](#task-plt-39) — approval/step-up. *Why:* same.<br>**artifact** [PLT.40](#task-plt-40) — secrets/session isolation. *Why:* same.<br>**artifact** [PLT.41](#task-plt-41) — egress control. *Why:* same.<br>**artifact** [PLT.42](#task-plt-42) — instruction provenance. *Why:* same.<br>**artifact** [PLT.43](#task-plt-43) — leases/trust. *Why:* same.<br>**artifact** [PLT.44](#task-plt-44) — audit. *Why:* same.<br>**artifact** [PLT.45](#task-plt-45) — content helper isolation. *Why:* same.<br>**artifact** [PLT.54](#task-plt-54) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [PLT.57](#task-plt-57) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): offline verify/policy tests in CI; the real OS-isolation matrix (PLT.45's evidence) is local opt-in, recorded and cross-referenced here rather than re-run. |
| Completion evidence | Cross-boundary owner refusal, stale approval/revocation, secrets/redaction and real OS-isolation tests per [WP-11.90](../../work-packages/11-security-foundation.md#rule-wp-11.90). |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: None of the Security-family packages are in eng/packaging/packages.json today. |

<a id="task-plt-47"></a>

### PLT.47 — Emission and required dimensions

**Outcome.** A single emission surface for metrics/traces/structured logs with the required dimension set attached automatically from ambient context; a present dimension is always attached, an absent one omitted rather than defaulted; build identifier and instance identity are on every signal.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-47` and ledger record `ledger/tasks/plt-47.md` in the Plan repository; task branch `task/plt-47` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-12.00](../../work-packages/12-observability-foundation.md#rule-wp-12.00) — full |
| Provides | signal-emission |
| Start prerequisites | **artifact** [FND.01](foundation.md#task-fnd-01) — identity primitive types (instance identity, build id). *Why:* required dimensions are typed [WP-04](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04) identifiers, not free strings. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.48](#task-plt-48), [PLT.53](#task-plt-53), [UPD.06](updater.md#task-upd-06) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Observability/**` |
| Validation | Offline tests: dimension-coverage test across representative operations; absent-dimension-omitted test. |
| Completion evidence | Dimension coverage report. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/BuildingBlocks/ArcForges.Observability/ is a bare AssemblyPlaceholder.cs project today. |

<a id="task-plt-48"></a>

### PLT.48 — Correlation and causation propagation

**Outcome.** Correlation created at the originating edge or accepted from a validated client value, propagated across HTTP/queue/worker/realtime/provider calls once, in shared infrastructure; causation records which operation caused which; a user-visible task/run identifier resolves to its trace.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-48` and ledger record `ledger/tasks/plt-48.md` in the Plan repository; task branch `task/plt-48` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-12.01](../../work-packages/12-observability-foundation.md#rule-wp-12.01) — full |
| Provides | correlation-causation |
| Start prerequisites | **artifact** [PLT.47](#task-plt-47) — emission surface. *Why:* correlation/causation are dimensions carried on every emitted signal. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.01](cloud.md#task-cloud-01) — a real Cloud hop to prove the full HTTP/queue/worker/realtime/provider chain. *Why:* the desktop side can only prove propagation up to its own local hops (RPC, in-process) until a real Cloud counterpart exists; the [WP-12.90](../../work-packages/12-observability-foundation.md#rule-wp-12.90) receipt records this as a named later real-integration item. |
| Unblocks | [PLT.53](#task-plt-53) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Observability/**` |
| Validation | Offline tests: synthetic end-to-end action producing one connected trace across available local hop kinds; resolution test from task identifier to trace; validation test rejecting malformed client-supplied correlation. |
| Completion evidence | A single connected trace across every available hop kind. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-49"></a>

### PLT.49 — Redaction by construction

**Outcome.** Secret-bearing and content types have no logging representation; a scrubbing processor removes known-sensitive header/field names as a second line of defence; URLs recorded as route templates plus identifiers; exception messages mapped to reason codes before export.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-49` and ledger record `ledger/tasks/plt-49.md` in the Plan repository; task branch `task/plt-49` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-12.02](../../work-packages/12-observability-foundation.md#rule-wp-12.02) — full<br>[WP-12](../../work-packages/12-observability-foundation.md#rule-wp-12) eng/policy/telemetry-policy.json creation: dimension allowlist, metric label allowlist, sampling and retention configuration — package-level obligation contribution |
| Provides | redaction |
| Start prerequisites | **artifact** [PLT.40](#task-plt-40) — SecretRef type with no accessible string representation. *Why:* [RD-03](../../../architecture/01-solution-and-project-layout.md#rule-rd-03) requires SecretRef's formatting to emit only a reference; redaction structurally depends on Security's type design, not merely a logging convention.<br>**artifact** [FND.05](foundation.md#task-fnd-05) — reason-code registry. *Why:* [RD-07](../../../architecture/01-solution-and-project-layout.md#rule-rd-07) maps exception messages to reason codes before export. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.50](#task-plt-50), [PLT.52](#task-plt-52), [PLT.53](#task-plt-53) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Observability/**`<br>`DesktopPlatform:eng/policy/telemetry-policy.json` |
| Validation | Offline tests: marker values injected as headers/tokens/prompts/note-content/file-paths must never appear in exported signals; structural test that content types cannot be logged. This is exactly [PG-05](../../../assurance/open-gates-register.md#rule-pg-05)'s own evidence requirement, run offline against a local test exporter, not a live telemetry backend. |
| Completion evidence | Marker-injection redaction report, zero findings - satisfies [PG-05](../../../assurance/open-gates-register.md#rule-pg-05). |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: eng/policy/telemetry-policy.json does not exist yet. [PG-05](../../../assurance/open-gates-register.md#rule-pg-05) is OPEN in open-gates-register.md, owner Operations Owner, trigger 'first telemetry export to an external backend'. |

<a id="task-plt-50"></a>

### PLT.50 — Cardinality and sampling

**Outcome.** Metric labels and bounded trace policy enforced from observability architecture SS13: head sample plus bounded diagnostic buffer, error/slow promotion only for spans still retained, explicit overflow/loss counters; unsampled mandatory error facts remain redacted under consent.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-50` and ledger record `ledger/tasks/plt-50.md` in the Plan repository; task branch `task/plt-50` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-12.03](../../work-packages/12-observability-foundation.md#rule-wp-12.03) — full<br>[WP-12](../../work-packages/12-observability-foundation.md#rule-wp-12) eng/policy/telemetry-policy.json creation: dimension allowlist, metric label allowlist, sampling and retention configuration — package-level obligation contribution |
| Provides | cardinality-sampling |
| Start prerequisites | **artifact** [PLT.49](#task-plt-49) — redaction processor. *Why:* sampling/cardinality policy is applied on top of the already-redacted signal shape. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.53](#task-plt-53) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Observability/**`<br>`DesktopPlatform:eng/policy/telemetry-policy.json` |
| Validation | Offline tests: cardinality negative fixture, sampled/unsampled error, slow-span buffer expiry, overflow and disabled-consent tests. |
| Completion evidence | Cardinality negative fixture and sampling retention results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-51"></a>

### PLT.51 — Health probes

**Outcome.** Liveness, readiness and capability health as three distinct probe kinds; readiness fails closed on a missing required dependency; capability health uses the five health dimensions (reachable, ready, healthy, degraded, capacity) shared with the contract model.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-51` and ledger record `ledger/tasks/plt-51.md` in the Plan repository; task branch `task/plt-51` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-12.04](../../work-packages/12-observability-foundation.md#rule-wp-12.04) — full |
| Provides | health-probes; health-dimension-source |
| Start prerequisites | **artifact** [PLT.23](#task-plt-23) — HealthDimension type ([WP-09.06](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.06)). *Why:* the same five-dimension vocabulary is defined once in the capability model and reused identically here. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.53](#task-plt-53) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Observability/**` |
| Validation | Offline tests: dependency-outage test asserting readiness fails closed; capability-health test reflecting simulated degradation. |
| Completion evidence | Health probe fail-closed and degradation results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-plt-52"></a>

### PLT.52 — Desktop diagnostics and consent

**Outcome.** Local diagnostics always available without upload; three tiers (minimal always-on local, user-approved report, time-bounded self-disabling verbose session visible while active); a report is generated, shown in full, sent only after approval; no memory dump by default; consent is revocable and stops collection immediately and locally.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-52` and ledger record `ledger/tasks/plt-52.md` in the Plan repository; task branch `task/plt-52` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-12.05](../../work-packages/12-observability-foundation.md#rule-wp-12.05) — full |
| Provides | desktop-diagnostics-consent |
| Start prerequisites | **artifact** [PLT.31](#task-plt-31) — error presentation shell surface ([WP-10.05](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.05)). *Why:* the diagnostic report/consent flow is presented through shell UI, and the verbose-session indicator is shell chrome.<br>**artifact** [PLT.49](#task-plt-49) — redaction. *Why:* a generated diagnostic report must already be redacted before it is shown to the user for approval. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.53](#task-plt-53) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Observability.Desktop/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline tests: consent-absent test asserting no signal leaves the device; crash test asserting no automatic upload; verbose-session expiry test; revocation test. All runnable as local simulated-consent-state tests, no live telemetry backend needed. |
| Completion evidence | Consent-absent, crash-approval, verbose-expiry and revocation results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ArcForges.Observability.Desktop does not exist as a project yet. |

<a id="task-plt-53"></a>

### PLT.53 — Publish Observability packages and verify real integration

**Outcome.** ArcForges.Observability and.Observability.Desktop are packed, admitted, published and independently consumed; a trace can join one request across owners without logging prompts/credentials/unbounded payloads; health distinguishes backend/CF/model/R2 failures once those exist.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-53` and ledger record `ledger/tasks/plt-53.md` in the Plan repository; task branch `task/plt-53` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-12](../../work-packages/12-observability-foundation.md#rule-wp-12) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-12.90](../../work-packages/12-observability-foundation.md#rule-wp-12.90) — full |
| Provides | observability-package |
| Start prerequisites | **artifact** [PLT.47](#task-plt-47) — emission/dimensions. *Why:* publish needs the complete substep set.<br>**artifact** [PLT.48](#task-plt-48) — correlation/causation. *Why:* same.<br>**artifact** [PLT.49](#task-plt-49) — redaction. *Why:* same.<br>**artifact** [PLT.50](#task-plt-50) — cardinality/sampling. *Why:* same.<br>**artifact** [PLT.51](#task-plt-51) — health probes. *Why:* same.<br>**artifact** [PLT.52](#task-plt-52) — diagnostics/consent. *Why:* same. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): offline verify/policy tests; Cloud-side hop evidence deferred per PLT.48's complete edge. |
| Completion evidence | Owned artifact and real-integration receipt per [WP-12.90](../../work-packages/12-observability-foundation.md#rule-wp-12.90). |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Not in packages.json. |

<a id="task-plt-54"></a>

### PLT.54 — Real hostile-input containment proof with production parser libraries loaded in ContentSandbox

**Outcome.** that [PG-12](../../../assurance/open-gates-register.md#rule-pg-12)/[PG-22](../../../assurance/open-gates-register.md#rule-pg-22)'s OS isolation mechanics (proven against a first-party hostile test parser in PLT.45) hold once real PDFium/FFmpeg/OpenImageIO/OpenColorIO/OTIO composition is loaded into the same helper by [WP-13.13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) ; this is the point where the SUB-hostile-test-parser substitute is actually replaced.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-54` and ledger record `ledger/tasks/plt-54.md` in the Plan repository; task branch `task/plt-54` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-11.09](../../work-packages/11-security-foundation.md#rule-wp-11.09) — containment mechanics re-verified against the real parser closure<br>[WP-13.13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) — production parser composition and its own containment evidence |
| Start prerequisites | **artifact** [PLT.45](#task-plt-45) — real, delivered outcome of PLT.45 (Content helper and OS-enforced isolation (ContentSandbox host)). *Why:* this integration exercises the real content helper and OS-enforced isolation (ContentSandbox host) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NAT.14](native.md#task-nat-14) — real, delivered outcome of NAT.14 (Pdf family: PDFium and production parser containment in the WP11 helper (NEW library)). *Why:* this integration exercises the real pdf family: PDFium and production parser containment in the WP11 helper (NEW library) instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.30](native.md#task-nat-30), [PLT.46](#task-plt-46) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | that [PG-12](../../../assurance/open-gates-register.md#rule-pg-12)/[PG-22](../../../assurance/open-gates-register.md#rule-pg-22)'s OS isolation mechanics (proven against a first-party hostile test parser in PLT.45) hold once real PDFium/FFmpeg/OpenImageIO/OpenColorIO/OTIO composition is loaded into the same helper by [WP-13.13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) ; this is the point where the SUB-hostile-test-parser substitute is actually replaced. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-plt-56"></a>

### PLT.56 — Three professional products compose the shared DesignSystem/Shell without divergence

**Outcome.** that ArcNotes, ArcScope and ArcSlate each restore only the shell packages/mechanisms they need, feel like one family (shared tokens/commands/settings/attention/error presentation), and that no product had to depend on another to render its own UI ([BR-02](../../../architecture/14-build-packaging-and-release.md#rule-br-02) of WP10).

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-56` and ledger record `ledger/tasks/plt-56.md` in the Plan repository; task branch `task/plt-56` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-10.90](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.90) — the multi-product consumption evidence beyond a single clean package-only diagnostic |
| Start prerequisites | **artifact** [PLT.35](#task-plt-35) — real, delivered outcome of PLT.35 (Publish DesignSystem/Shell packages and verify real integration). *Why:* this integration exercises the real publish DesignSystem/Shell packages and verify real integration instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [NOTES.03](arcnotes.md#task-notes-03) — real, delivered outcome of NOTES.03 (Editor interaction: caret, selection, IME composition, markdown-friendly input). *Why:* this integration exercises the real editor interaction: caret, selection, IME composition, markdown-friendly input instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SCOPE.09](arcscope.md#task-scope-09) — real, delivered outcome of SCOPE.09 (Long-running capture in the shell). *Why:* this integration exercises the real long-running capture in the shell instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [SLATE.22](arcslate.md#task-slate-22) — real, delivered outcome of SLATE.22 (Viewer: source and sequence, professional transport). *Why:* this integration exercises the real viewer: source and sequence, professional transport instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.35](#task-plt-35) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | that ArcNotes, ArcScope and ArcSlate each restore only the shell packages/mechanisms they need, feel like one family (shared tokens/commands/settings/attention/error presentation), and that no product had to depend on another to render its own UI ([BR-02](../../../architecture/14-build-packaging-and-release.md#rule-br-02) of WP10). |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-plt-57"></a>

### PLT.57 — End-to-end capability invocation with real security enforcement inside one product

**Outcome.** that the [WP-09.07](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.07) invocation pipeline's 'authorize' step, wired to the real [WP-11.02](../../work-packages/11-security-foundation.md#rule-wp-11.02) decision pipeline, actually gates a real product capability end to end (resolve -> availability -> freeze -> authorize -> invoke -> validate -> record -> audit), closing the IAuthorizer interface seam both PLT.24 and PLT.38 are built against.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-57` and ledger record `ledger/tasks/plt-57.md` in the Plan repository; task branch `task/plt-57` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-09.07](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.07) — real authorize-step integration<br>[WP-11.02](../../work-packages/11-security-foundation.md#rule-wp-11.02) — real invocation-pipeline attachment |
| Start prerequisites | **artifact** [PLT.24](#task-plt-24) — real, delivered outcome of PLT.24 (Invocation pipeline). *Why:* this integration exercises the real invocation pipeline instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PLT.38](#task-plt-38) — real, delivered outcome of PLT.38 (Decision pipeline and the four enforcement points). *Why:* this integration exercises the real decision pipeline and the four enforcement points instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [APP.01](app-composition.md#task-app-01) — real, delivered outcome of APP.01 (Assistant.Abstractions host ports and application identity). *Why:* this integration exercises the real assistant.Abstractions host ports and application identity instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.25](#task-plt-25), [PLT.46](#task-plt-46) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | that the [WP-09.07](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.07) invocation pipeline's 'authorize' step, wired to the real [WP-11.02](../../work-packages/11-security-foundation.md#rule-wp-11.02) decision pipeline, actually gates a real product capability end to end (resolve -> availability -> freeze -> authorize -> invoke -> validate -> record -> audit), closing the IAuthorizer interface seam both PLT.24 and PLT.38 are built against. |
| Baseline (unreviewed unless accepted) | not-started |
