# Desktop platform mechanisms — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Persistence, local helper gRPC, capabilities, design system and shell, security and observability packages.

Tasks: 55 · Owning repositories: DesktopPlatform · Integration owner(s): DesktopPlatform integration owner

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
| [PLT.14](#task-plt-14) | Disconnect, cancel and retry semantics | producer | M | [PLT.09](#task-plt-09) (artifact), [FND.02](foundation.md#task-fnd-02) (artifact), [PLT.13](#task-plt-13) (artifact) | not-started |
| [PLT.15](#task-plt-15) | Brokered large data over the sandbox boundary | producer | M | [PLT.09](#task-plt-09) (artifact), [CON.04](contracts.md#task-con-04) (contract), [PLT.13](#task-plt-13) (artifact) | not-started |
| [PLT.16](#task-plt-16) | Publish LocalRpc package and verify real integration | acceptance | S | [PLT.09](#task-plt-09) (artifact), [PLT.10](#task-plt-10) (artifact), [PLT.11](#task-plt-11) (artifact), [PLT.12](#task-plt-12) (artifact), [PLT.13](#task-plt-13) (artifact), [PLT.14](#task-plt-14) (artifact), [PLT.15](#task-plt-15) (artifact) | not-started |
| [PLT.17](#task-plt-17) | Application identity and in-process composition | producer | S | [CON.91](contracts.md#task-con-91) (contract), [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [PLT.18](#task-plt-18) | Static contribution registration | producer | M | [PLT.17](#task-plt-17) (artifact) | not-started |
| [PLT.19](#task-plt-19) | Capability registry and selection | producer | L | [PLT.17](#task-plt-17) (artifact), [CON.91](contracts.md#task-con-91) (contract), [CON.02](contracts.md#task-con-02) (contract) | not-started |
| [PLT.20](#task-plt-20) | Actions and availability | producer | M | [PLT.19](#task-plt-19) (artifact) | not-started |
| [PLT.21](#task-plt-21) | Context providers and freezing | producer | M | [PLT.17](#task-plt-17) (artifact) | not-started |
| [PLT.22](#task-plt-22) | Resources and artifacts resolution | producer | M | [PLT.05](#task-plt-05) (artifact), [PLT.17](#task-plt-17) (artifact) | not-started |
| [PLT.23](#task-plt-23) | Own navigation, hints and health | producer | M | [PLT.22](#task-plt-22) (artifact) | not-started |
| [PLT.24](#task-plt-24) | Invocation pipeline | producer | L | [PLT.19](#task-plt-19) (artifact), [PLT.20](#task-plt-20) (artifact), [PLT.21](#task-plt-21) (artifact) | not-started |
| [PLT.25](#task-plt-25) | Publish Capabilities/Contributions packages and verify real integration | acceptance | S | [PLT.17](#task-plt-17) (artifact), [PLT.18](#task-plt-18) (artifact), [PLT.19](#task-plt-19) (artifact), [PLT.20](#task-plt-20) (artifact), [PLT.21](#task-plt-21) (artifact), [PLT.22](#task-plt-22) (artifact), [PLT.23](#task-plt-23) (artifact), [PLT.24](#task-plt-24) (artifact), [PLT.57](#task-plt-57) (artifact) | not-started |
| [PLT.26](#task-plt-26) | Token system and theming | producer | M | [PRF.02](runtime-proofs.md#task-prf-02) (artifact) | not-started |
| [PLT.27](#task-plt-27) | Windows, panels and layout | producer | L | [PLT.26](#task-plt-26) (artifact) | not-started |
| [PLT.28](#task-plt-28) | Command system | producer | M | [PLT.27](#task-plt-27) (artifact), [PLT.20](#task-plt-20) (artifact) | not-started |
| [PLT.29](#task-plt-29) | Scoped settings | producer | M | [PLT.26](#task-plt-26) (artifact), [PLT.04](#task-plt-04) (artifact) | not-started |
| [PLT.30](#task-plt-30) | Attention and notification model | producer | M | [PLT.27](#task-plt-27) (artifact) | not-started |
| [PLT.31](#task-plt-31) | Error presentation | producer | S | [PLT.26](#task-plt-26) (artifact), [FND.05](foundation.md#task-fnd-05) (artifact) | not-started |
| [PLT.32](#task-plt-32) | Lifecycle, menus and shutdown | producer | M | [PLT.28](#task-plt-28) (artifact) | not-started |
| [PLT.33](#task-plt-33) | Accessibility and localisation baseline | producer | L | [PLT.27](#task-plt-27) (artifact) | not-started |
| [PLT.34](#task-plt-34) | Third-party control admission | producer | M | [PRF.02](runtime-proofs.md#task-prf-02) (artifact) | not-started |
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
| [PLT.45](#task-plt-45) | Content helper and OS-enforced isolation (ContentSandbox host) | producer | XL | [PLT.15](#task-plt-15) (artifact), [PLT.09](#task-plt-09) (artifact), [PLT.10](#task-plt-10) (artifact), [CON.04](contracts.md#task-con-04) (contract) | not-started |
| [PLT.46](#task-plt-46) | Publish Security packages and verify real integration | acceptance | M | [PLT.36](#task-plt-36) (artifact), [PLT.37](#task-plt-37) (artifact), [PLT.38](#task-plt-38) (artifact), [PLT.39](#task-plt-39) (artifact), [PLT.40](#task-plt-40) (artifact), [PLT.41](#task-plt-41) (artifact), [PLT.42](#task-plt-42) (artifact), [PLT.43](#task-plt-43) (artifact), [PLT.44](#task-plt-44) (artifact), [PLT.45](#task-plt-45) (artifact), [PLT.54](#task-plt-54) (artifact), [PLT.57](#task-plt-57) (artifact) | not-started |
| [PLT.47](#task-plt-47) | Emission and required dimensions | producer | M | [FND.01](foundation.md#task-fnd-01) (artifact) | not-started |
| [PLT.48](#task-plt-48) | Correlation and causation propagation | producer | M | [PLT.47](#task-plt-47) (artifact) | not-started |
| [PLT.49](#task-plt-49) | Redaction by construction | producer | L | [PLT.40](#task-plt-40) (artifact), [FND.05](foundation.md#task-fnd-05) (artifact) | not-started |
| [PLT.50](#task-plt-50) | Cardinality and sampling | producer | M | [PLT.49](#task-plt-49) (artifact) | not-started |
| [PLT.51](#task-plt-51) | Health probes | producer | S | [PLT.23](#task-plt-23) (artifact) | not-started |
| [PLT.52](#task-plt-52) | Desktop diagnostics and consent | producer | L | [PLT.31](#task-plt-31) (artifact), [PLT.49](#task-plt-49) (artifact) | not-started |
| [PLT.53](#task-plt-53) | Publish Observability packages and verify real integration | acceptance | S | [PLT.47](#task-plt-47) (artifact), [PLT.48](#task-plt-48) (artifact), [PLT.49](#task-plt-49) (artifact), [PLT.50](#task-plt-50) (artifact), [PLT.51](#task-plt-51) (artifact), [PLT.52](#task-plt-52) (artifact) | not-started |
| [PLT.54](#task-plt-54) | Real hostile-input containment proof with production parser libraries loaded in ContentSandbox | integration | M | [PLT.45](#task-plt-45) (artifact), [NAT.14](native.md#task-nat-14) (artifact) | not-started |
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
| Unblocks | [APP.08](app-composition.md#task-app-08), [CLOUD.38](cloud.md#task-cloud-38), [FND.02](foundation.md#task-fnd-02), [PLT.05](#task-plt-05), [PLT.07](#task-plt-07), [PLT.08](#task-plt-08), [PLT.39](#task-plt-39), [PLT.43](#task-plt-43), [PLT.44](#task-plt-44), [SCOPE.01](arcscope.md#task-scope-01) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Sqlite/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline unit + integration tests against a real local SQLite file (no external service): policy test asserting no alternative write path, concurrency tests for serialised writes/concurrent reads, boundary test that no storage type appears in an application signature. AOT/trim diagnostics build-breaking since this library is IsAotCompatible. |
| Completion evidence | Single-write-path policy test result. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/BuildingBlocks/ArcForges.Persistence.Sqlite/ is a bare AssemblyPlaceholder.cs project with zero dependencies declared; Microsoft.Data.Sqlite is not yet in Directory.Packages.props. |
| Notes | Interface-first decoupling recommended: define IJournalWriter/IJournalReader here as the seam PLT.02 implements, so PLT.01 and PLT.02 can be authored in parallel PRs against the same interface rather than serially. Security-exception scope is limited to CA2100 on the internal SqliteReadContext.CreateCommand(string) method in src/BuildingBlocks/ArcForges.Persistence.Sqlite/Store/StoreDatabase.cs. Independent review must establish that every caller supplies literal SQL, a fixed internal identifier, or explicitly trusted owner-authored MigrationStep.Statements, with data values bound as parameters. The SQLite schema authorizer is additional defense, not a sanitizer or permission to accept untrusted SQL. A documented method-only suppression may cover this demonstrated statement-factory false positive; no file-wide, project-wide or repository-wide suppression, new caller trust, or weakened authorizer is authorized. Fix any real injection finding instead; retain targeted offline migration/journal tests and all other security diagnostics. Retain strict boundary negatives for untrusted data, forbidden schema actions and protected tables; the exemption must not extend to any other method or diagnostic. |

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
| Completion prerequisites | **integration** [PLT.03](#task-plt-03) — actual durable verified snapshots and recovery integrated with journal truncation. *Why:* The journal artifact can be delivered first and remains the start input for PLT.03; full bounded growth by snapshot policy requires its real snapshot producer, followed by PLT.02 snapshot/truncate/replay and repeated bounded-growth acceptance. |
| Unblocks | [PLT.03](#task-plt-03), [PLT.08](#task-plt-08) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Sqlite/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | Offline tests: durability test using a simulated process kill between journal write and commit acknowledgement (in-process fault injection, not a real OS-level crash - that remains local opt-in); replay test; truncation-under-read test. |
| Completion evidence | Durability and replay results. Completion additionally records exact PLT.03 snapshot artifacts and real snapshot/truncate/replay, concurrent-read and repeated bounded-growth acceptance; fixture-only evidence supports delivery only. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: No journal table/type exists. |
| Notes | Deliver the durable append/replay journal and verified-boundary truncation seam against an explicitly named snapshot fixture before the snapshot producer exists. A fixture never proves durable snapshot validity or the full bounded-growth obligation. Keep the ledger delivered while PLT.03 is pending; after that producer is complete, perform the real snapshot/truncate/replay, concurrent-read and repeated bounded-growth acceptance before completing PLT.02. Preserve every [WP-07.01](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.01) obligation and PLT.03 existing artifact start edge; this staging does not authorize starting any unclaimed downstream task. |

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
| Unblocks | [PLT.02](#task-plt-02), [PLT.08](#task-plt-08) |
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
| Unblocks | [PLT.08](#task-plt-08), [PLT.29](#task-plt-29), [UPD.04](updater.md#task-upd-04) |
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
| Unblocks | [PLT.08](#task-plt-08), [PLT.22](#task-plt-22) |
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
| Unblocks | [PLT.08](#task-plt-08), [SCOPE.07](arcscope.md#task-scope-07) |
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
| Unblocks | [PLT.08](#task-plt-08) |
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
| Write scope | `DesktopPlatform:eng/packaging/packages.json`<br>`DesktopPlatform:eng/version-sources.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Resources/ArcForges.Persistence.Resources.csproj`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Resources/README.md`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Derived/ArcForges.Persistence.Derived.csproj`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Derived/README.md` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): offline packages.py verify plus policy tests; real crash/hardware-level recovery evidence beyond simulated kills is local opt-in, recorded separately. |
| Completion evidence | Owned artifact and real-integration receipt per the [WP-07.90](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.90) template. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ArcForges.Persistence.Sqlite is already listed and packable; ArcForges.Persistence.Resources and ArcForges.Persistence.Derived are absent from eng/packaging/packages.json and their existing project files set IsPackable=false. |
| Notes | PLT.08-only package activation: the outcome requires the existing Resources and Derived projects to publish as their named managed packages. The task-owned project files authorize only setting IsPackable=true, explicit existing package IDs, readme and description metadata, the existing AGPL-3.0-only licence metadata, and packaging the repository LICENSE and NOTICE; the new task-owned Derived README documents this owned mechanism. The Resources README is authorized for exactly one documentation correction: replace `This project is nonpackable; PLT.08 owns package/integration acceptance.` with `This package provides shared persistence mechanisms without centralizing product data ownership: each product owns its canonical files, schemas and domain records.`; no other Resources README content may change. Preserve public APIs, project references, exact dependency closure, versions and package identities; preserve the existing Sqlite package entry and append only the missing Resources and Derived allowlist entries. Narrow [ADP-07](../adoption.md#rule-adp-07) supporting bindings for these changes: update only the active input hashes for eng/packaging/packages.json and the two task-owned Resources/Derived csproj files in eng/policy/dependency-policy.json and the PLT.08 immutable successor at eng/policy/dependency-reviews/plt-08-r1.json; preserve the active predecessor chain and do not change any dependency coordinate, version or closure. In eng/provenance/files.json, append only the task-owned Derived README and the new immutable PLT.08 successor receipt as firstParty; leave the already-classified Resources README row unchanged, and regenerate only required NOTICE/provenance derivatives. Because the two task-owned csproj blobs change, update only their blob hashes on the two corresponding existing project rows in eng/policy/reconciliation/active-projects.json. Do not add or remove projects, edit project-updates.json or source.json, or change the reconciliation algorithm/checker. No workflow, lock, solution, project registration, architecture, licence/runtime policy row, pack algorithm, dependency/version or source API change is authorized. |

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
| Unblocks | [PLT.11](#task-plt-11), [PLT.16](#task-plt-16), [PLT.38](#task-plt-38), [PLT.45](#task-plt-45) |
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
| Unblocks | [PLT.12](#task-plt-12), [PLT.16](#task-plt-16), [PRF.02](runtime-proofs.md#task-prf-02) |
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

**Outcome.** 16 active/64 queued bounded data calls, deadlines and parent-owned callback channels, plus exactly two reserved control slots outside the data-call budget for bootstrap, lease renewal, cancellation and health; all four control operations remain serviceable while data dispatch is saturated, with no recursive saturated callback lane.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-13` and ledger record `ledger/tasks/plt-13.md` in the Plan repository; task branch `task/plt-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-08.04](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.04) — full |
| Provides | ipc-bounds; ipc-two-reserved-control-slots |
| Start prerequisites | **artifact** [PLT.09](#task-plt-09) — transport. *Why:* bounds/backpressure wrap the transport's call dispatch; can proceed in parallel with PLT.10-12 once the transport shape is fixed, not strictly serial after routing. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.14](#task-plt-14), [PLT.15](#task-plt-15), [PLT.16](#task-plt-16) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Validation | Offline deterministic tests: queue/memory bound, fairness, timeout and typed overload; hold the ordinary 16-active/64-queued data dispatcher at saturation and prove the exactly two reserved control slots remain outside that budget and service bootstrap, lease renewal, cancellation and health operations (each operation is exercised under saturation), without recursive callback dispatch. |
| Completion evidence | Queue/memory bound, fairness, timeout and typed overload; saturated data-dispatch results proving the exactly two reserved control slots service bootstrap, lease renewal, cancellation and health. |
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
| Start prerequisites | **artifact** [PLT.09](#task-plt-09) — transport. *Why:* cancellation/retry wrap the transport call lifecycle.<br>**artifact** [FND.02](foundation.md#task-fnd-02) — effect-certainty/Outcome types. *Why:* unknown-effect classification is a [WP-04.01](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.01) type, not invented locally.<br>**artifact** [PLT.13](#task-plt-13) — two reserved cancellation/control slots under saturated bounded dispatch. *Why:* Annex 09 §3 reserves two separate control slots for bootstrap, renewal, cancellation and health; [WP-08.05](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.05) cancellation must remain serviceable when ordinary calls saturate the bounded dispatcher. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.16](#task-plt-16) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Validation | Offline/local tests: kill before/after commit, lost ack and unknown effect; while ordinary data dispatch is saturated, prove cancellation progresses through one of PLT.13's two reserved control slots. |
| Completion evidence | Kill before/after commit, lost ack and unknown effect; cancellation succeeds under saturated data dispatch through a reserved control slot. |
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
| Start prerequisites | **artifact** [PLT.09](#task-plt-09) — transport. *Why:* brokered transfer is a call pattern over the same transport.<br>**contract** [CON.04](contracts.md#task-con-04) — ContentSandboxService/slot-grant wire shapes in contracts/09-local-grpc-and-sandbox.md. *Why:* the exact grant/seal/ack/cancel lifecycle is fixed by the published contract, not invented here.<br>**artifact** [PLT.13](#task-plt-13) — two reserved cancellation/control slots under saturated bounded dispatch. *Why:* Annex 09 §3 reserves two separate control slots for bootstrap, renewal, cancellation and health; [WP-08.06](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.06) transfer cancellation must remain serviceable when ordinary calls saturate the bounded dispatcher. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [PLT.45](#task-plt-45) — the real ContentSandbox helper actually using these brokered buffers. *Why:* [WP-08.06](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.06) implements the generic broker mechanism; PLT.45 ([WP-11.09](../../work-packages/11-security-foundation.md#rule-wp-11.09)) is the first real consumer that proves it end to end with a hostile parser. |
| Unblocks | [PLT.16](#task-plt-16), [PLT.24](#task-plt-24), [PLT.45](#task-plt-45) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.LocalRpc/**` |
| Validation | Offline/local tests: wrong resource grant, range/hash/expiry/cancel and orphan cleanup; while ordinary data dispatch is saturated, prove transfer cancellation progresses through one of PLT.13's two reserved control slots. |
| Completion evidence | Wrong resource grant, range/hash/expiry/cancel and orphan cleanup; transfer cancellation succeeds under saturated data dispatch through a reserved control slot. |
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
| Write scope | `DesktopPlatform:eng/packaging/packages.json`<br>`DesktopPlatform:eng/policy/dependency-policy.json`<br>`DesktopPlatform:eng/policy/dependency-reviews/plt-16-r1.json`<br>`DesktopPlatform:eng/provenance/files.json` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): offline package and policy tests plus one independent consumer check against the exact prepublication CI candidate package. The consumer must resolve the recorded package ID/version and SHA256 from the candidate artifact through an isolated temporary package source/cache, with no project reference, sibling-source fallback or substitute package; record source commit, CI run/artifact identity, package identity/digest and consumer restore/build/run result. This existing-environment candidate check is local opt-in and performed once for the affected candidate; do not add a hosted installed-consumer test or a permanent consumer harness. Real multi-process OS-stream evidence beyond the repo's own build-machine tests remains local opt-in. |
| Completion evidence | Exact CI candidate artifact/source commit and package identity/version/SHA256; independent isolated consumer restore/build/run proving it resolved only that exact candidate with no project/source fallback; package/policy checks and applicable UX acceptance ledger. Record any separately required real OS-stream run once as local opt-in evidence. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: LocalRpc not in packages.json. |
| Notes | [ADP-07](../adoption.md#rule-adp-07) support is limited to the exact append-only package-inventory row in eng/packaging/packages.json and its required existing-gate bindings: refresh only that file's active input hash and the current dependency-review pointer/active review object in eng/policy/dependency-policy.json; add immutable eng/policy/dependency-reviews/plt-16-r1.json as a successor to the then-current receipt, preserving the admitted dependency coordinates, versions and closure; and append only that receipt as firstParty in eng/provenance/files.json. Use RES-desktopplatform-policy-data for these task-owned policy/provenance bindings and RES-desktopplatform-package-inventory for the package row. Do not invent or predeclare LocalRpc package dependency IDs, version ranges or closure here: derive them only from the reviewed, frozen PLT.09 project references and their separately admitted exact pins; if that frozen graph requires any unadmitted package/version change, obtain authority before changing it. Do not change projects, package locks, reconciliation, architecture classifications or test maps, licences, runtime behavior, policy algorithms or unrelated records. PLT.16 may publish/consume the progressive exact package candidate once its declared PLT.09-15 artifacts exist; it has no PLT.45 completion prerequisite. PLT.15 remains complete only after PLT.45 integrates the brokered-data mechanism. |

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
| Unblocks | [APP.01](app-composition.md#task-app-01), [APP.08](app-composition.md#task-app-08), [EXE.01](execution.md#task-exe-01), [PLT.18](#task-plt-18), [PLT.19](#task-plt-19), [PLT.21](#task-plt-21), [PLT.22](#task-plt-22), [PLT.25](#task-plt-25) |
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
| Unblocks | [NAT.01](native.md#task-nat-01), [PLT.25](#task-plt-25) |
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
| Start prerequisites | **artifact** [PLT.17](#task-plt-17) — identity/composition. *Why:* the registry is scoped per application instance.<br>**contract** [CON.91](contracts.md#task-con-91) — accepted Foundation contract profile, including ResourceRef/ResourceVersionRef/ArtifactRef. *Why:* retain [WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09)'s inherited base-contract prerequisite; this published Foundation profile is distinct from the capability descriptor schema introduced by CON.02.<br>**contract** [CON.02](contracts.md#task-con-02) — CapabilityDescriptor/OperationBinding wire schema. *Why:* CON.02 is the Contracts producer of CapabilityDescriptor and the descriptor types used by OperationBinding; BR of WP09 forbids inventing binding fields or capability behavior. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [EXT.00](extensions.md#task-ext-00), [PLT.20](#task-plt-20), [PLT.24](#task-plt-24), [PLT.25](#task-plt-25), [PLT.37](#task-plt-37) |
| Write scope | `DesktopPlatform:Directory.Packages.props`<br>`DesktopPlatform:eng/packaging/packages.json`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json`<br>`DesktopPlatform:eng/policy/dependency-policy.json`<br>`DesktopPlatform:eng/policy/dependency-reviews/plt-19-r1.json`<br>`DesktopPlatform:eng/policy/reconciliation/active-projects.json`<br>`DesktopPlatform:eng/provenance/files.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Application.Abstractions/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/Tests/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Contributions/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Contributions/Tests/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Foundation/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Foundation/Tests/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Observability/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Observability/Tests/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Resources/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Resources/Tests/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Sqlite/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Security/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Security/Tests/packages.lock.json`<br>`DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox/packages.lock.json`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**`<br>`DesktopPlatform:tests/PersistenceTests/packages.lock.json` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline tests: enumerate expected bindings, reject missing/extra methods/unsupported major/inconsistent classification/readiness mismatch/ambiguous target. Verify the implementation-only closed owner union: Product(AppIdentity) only for ArcScope/Companion inProcess descriptors, or CloudService(SearchService) only for the currently declared search.query publicGrpc descriptor; CloudService is static catalogue metadata and never constructs a CapabilityTarget or enters the local instance selector, while caller scope remains ApplicationScope. Force-evaluate and perform locked restore for the exact 17-project Contracts.Foundation 1.0.0-ci.216.1 consumer set; confirm all other projects retain the 1.0.0-ci.113.1 repository default, including Foundation.Acceptance. Validate generated package metadata for the five authorized package rows and restore repository-external locked consumers of ArcForges.Capabilities and ArcForges.Capabilities plus ArcForges.Persistence.Sqlite against the candidate feed with no NU1107, NU1605 or NU1608. |
| Completion evidence | Selection priority, determinism and explainability results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |
| Notes | Keep the repository-wide ArcForges.Contracts.Foundation default at 1.0.0-ci.113.1 and authorize the exact 1.0.0-ci.216.1 central pin only for these 17 MSBuildProjectName values: LocalRpcAotTests, ArcForges.Application.Abstractions, ArcForges.Capabilities, ArcForges.Capabilities.Tests, ArcForges.ContentSandbox, ArcForges.Contributions, ArcForges.Contributions.Tests, ArcForges.Foundation, ArcForges.Foundation.Tests, ArcForges.Observability, ArcForges.Observability.Tests, ArcForges.Persistence.Resources, ArcForges.Persistence.Resources.Tests, ArcForges.Persistence.Sqlite, ArcForges.Security, ArcForges.Security.Tests, and ArcForges.Tests.PersistenceTests. Preserve Foundation.Acceptance and all other projects on the repository default; do not change the existing LocalRpcAotTests pin. In eng/packaging/packages.json, change only externalDependencies.ArcForges.Contracts.Foundation from 1.0.0-ci.113.1 to 1.0.0-ci.216.1 for the existing rows ArcForges.Foundation, ArcForges.Application.Abstractions, ArcForges.Capabilities, ArcForges.Persistence.Sqlite, and ArcForges.Persistence.Resources. Preserve each row's package ID, project, kind, owned dependencies, required files and all other fields, as well as every other package row. Only these 16 semantic lock paths may change: src/BuildingBlocks/ArcForges.Application.Abstractions/packages.lock.json; src/BuildingBlocks/ArcForges.Capabilities/packages.lock.json; src/BuildingBlocks/ArcForges.Capabilities/Tests/packages.lock.json; src/BuildingBlocks/ArcForges.Contributions/packages.lock.json; src/BuildingBlocks/ArcForges.Contributions/Tests/packages.lock.json; src/BuildingBlocks/ArcForges.Foundation/packages.lock.json; src/BuildingBlocks/ArcForges.Foundation/Tests/packages.lock.json; src/BuildingBlocks/ArcForges.Observability/packages.lock.json; src/BuildingBlocks/ArcForges.Observability/Tests/packages.lock.json; src/BuildingBlocks/ArcForges.Persistence.Resources/packages.lock.json; src/BuildingBlocks/ArcForges.Persistence.Resources/Tests/packages.lock.json; src/BuildingBlocks/ArcForges.Persistence.Sqlite/packages.lock.json; src/BuildingBlocks/ArcForges.Security/packages.lock.json; src/BuildingBlocks/ArcForges.Security/Tests/packages.lock.json; src/DesktopHelpers/ArcForges.ContentSandbox/packages.lock.json; and tests/PersistenceTests/packages.lock.json. Fourteen of these locks move from the already-admitted 113.1 coordinate to 216.1; the Capabilities and Capabilities.Tests locks may change only for the Foundation project-reference edge. LocalRpcAotTests and eng/acceptance/foundation/packages.lock.json remain unchanged, and no DesignSystem newline-only or other lockfile changes are authorized. Preserve the existing 51 NuGet coordinates and 10 Python package closure unchanged. The only permitted dependency-coordinate adjustment is the already-admitted Contracts.Foundation 1.0.0-ci.113.1 to 1.0.0-ci.216.1 selection for these exact five package rows and 17 projects; do not add or delete coordinates, change any license or package identity, or alter unrelated dependencies. Refresh dependency-policy.json and the immutable plt-19-r1 receipt only for actual task inputs, mirroring the same input hashes in review.inputHashes; chain the receipt from the active receipt at integration and do not modify historical receipts. No new project, package ID, version axis, global default pin, packaging algorithm, release mechanism, solution, workflow or licence-boundary change is authorized. The capability owner is an implementation-only closed union: Product(AppIdentity), limited to ArcScope/Companion inProcess descriptors, or CloudService(SearchService), limited to the currently declared search.query publicGrpc descriptor. Do not change wire CapabilityDescriptor, AppIdentity, ProductId or ApplicationScope. CloudService registration is static catalogue metadata only; it must not construct CapabilityTarget or enter the local instance selector, and caller scope remains the request ApplicationScope. Do not add a PublicApi dependency, package or closure edge. |

<a id="task-plt-20"></a>

### PLT.20 — Actions and availability

**Outcome.** Actions are computed from capabilities plus current context, side-effect free, cheap enough for UI enumeration; unavailability always yields a typed reason across permission/entitlement/health/context/version causes.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-20` and ledger record `ledger/tasks/plt-20.md` in the Plan repository; task branch `task/plt-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-09.03](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.03) — full |
| Provides | action-availability; availability-result-type; availability-evidence-snapshot |
| Start prerequisites | **artifact** [PLT.19](#task-plt-19) — capability registry. *Why:* availability is computed from registered capabilities plus context. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [PLT.38](#task-plt-38) — Security-owner read-only permission evidence for the acting principal, exact capability and scope. *Why:* The UI availability projection must consume the real Security owner's current permission facts; it is only a preflight and the owner still rechecks at invocation.<br>**integration** [COM.05](commerce.md#task-com-05) — canonical per-capability entitlement reason and version from the immutable grant/revocation resolver. *Why:* The local projection must not compute entitlement or replace the resolver's effective snapshot.<br>**integration** [COM.06](commerce.md#task-com-06) — the versioned client-distributed entitlement snapshot and bounded-staleness/refresh behavior. *Why:* Desktop availability consumes the actual client view; cached or asserted state remains UX-only and Cloud re-evaluates before protected dispatch. |
| Unblocks | [PLT.24](#task-plt-24), [PLT.25](#task-plt-25), [PLT.28](#task-plt-28) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only the exact PLT.20 availability API-to-direct-test binding after source/test names are frozen)`<br>`DesktopPlatform:eng/provenance/files.json (append only exact PLT.20-owned firstParty rows for source/test files within the existing task source scope, after file names are frozen)` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline tests: availability tests across permission/entitlement/health/context/version reasons; purity test asserting no side effect. |
| Completion evidence | Availability reason matrix and purity assertion. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |
| Notes | [ADP-07](../adoption.md#rule-adp-07) support is limited to the two exact supporting files above and append-only updates. Map `ArcResult<T>` to the delivered `ArcForges.Foundation.Errors.Outcome<T>` and `FrozenContext` to PLT.21's delivered `FrozenContextSnapshot`; preserve the exact `ValueTask<Outcome<AvailabilityResult>> ICapabilityProvider.EvaluateAvailabilityAsync(ActionKey actionKey, FrozenContextSnapshot context, CancellationToken cancellationToken = default)` signature and all nine existing result facts. Add only a Capabilities-owned immutable in-process `AvailabilityEvidenceSnapshot` supplied at provider construction by a trusted host; it is a local CLR contract, not protobuf, wire DTO, PublicApi dependency or grant. Bind one snapshot to `FrozenContextSnapshot.Owner`, provider principal/session, and finite unique action/capability/target keys; require exactly one matching record and reject missing, duplicate or mismatched keys. The host captures one fixed as-of time for each UI enumeration, computes freshness disposition before constructing the short-lived provider, and discards/rebuilds it on refresh or expiry; evaluation consumes only immutable evidence and its precomputed freshness disposition, never reads a clock or performs I/O. Permission facts must be owner-issued and preserve principal/capability/scope/constraints/lifetime; entitlement reason/version comes from COM.05/06; health/readiness/compatibility, product-version, installed and running facts require explicit trusted sources. PLT.19 `CapabilityTarget`/descriptor data does not establish distinct installed-versus-running state or product version: never infer these from an absent target or contract version. Missing, stale-at-capture, unknown or contradictory evidence must not yield `Available`; return an existing typed reason only for an explicitly established fact, otherwise `TemporarilyUnavailable`. Context applicability comes from the frozen context. Keep evaluation a pure projection over immutable inputs: `availabilityRule` keys select a finite private closed table of pure rule kinds; do not permit arbitrary caller-registered delegates, I/O, discovery, authorization, mutation or side effects. This is UX preflight only; Security rechecks at invocation and Cloud re-evaluates protected dispatch. `PolicyDisabled` requires explicit authorized input to an existing rule; do not invent a policy authority. Test expired-at-capture evidence returns `TemporarilyUnavailable` and host refresh constructs a new provider/snapshot; local tests may synthesize snapshots, but do not claim full [WP-09.03](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09.03) integration until the PLT.38 and COM.05/06 completion edges and real producer inputs are satisfied. Bind only the exact API to its direct PLT.20 test in [RP-10](../../../architecture/01-solution-and-project-layout.md#rule-rp-10) after names are frozen. Append only PLT.20-owned firstParty provenance rows within `src/BuildingBlocks/ArcForges.Capabilities/**`, preserving all rows and the RES-architecture-tests/RES-desktopplatform-policy-data append protocols. No new project, package, dependency, lock, solution, workflow, licence boundary, runtime owner, PublicApi reference, protobuf or reconciliation change is authorized; outcome, prerequisites and runtime behavior remain unchanged. |

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
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**`<br>`DesktopPlatform:eng/provenance/files.json (append only exact PLT.23-owned firstParty rows for source/test files within the task write scope)`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only exact PLT.23 public API to direct-test bindings)` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline tests: invalid ownership, missing content, expired child cursor, restart, duplicate hint recovery. |
| Completion evidence | Deep-link hostile-input, event and health results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |
| Notes | HealthDimension is only the closed capability-probe aspect-key type defined by [WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09): reachable, ready, healthy, degraded and capacity. It carries no observation value or snapshot fields. These keys are not Architecture 02 §11's five independent axes (Installation, Presence, Health, Readiness, Compatibility). This clarification changes no Contracts/wire or Foundation HealthSnapshot/InstanceHealth/InstanceReadiness semantics and defines no Cloud presence/heartbeat behavior. [ADP-07](../adoption.md#rule-adp-07) support is limited to the two exact supporting paths above: append only PLT.23-owned firstParty source/test inventory rows and exact public-API-to-direct-test rows required by the existing provenance and [RP-10](../../../architecture/01-solution-and-project-layout.md#rule-rp-10) gates. These changes use RES-desktopplatform-policy-data, owned by the DesktopPlatform integration owner: generated policy data is regenerated from its pinned source and never hand-edited; task-owned API/test and inventory rows are additive, and each task adds its own tests/evidence. No evaluator, schema, algorithm, ReasonCode, dependency closure or unrelated policy change is authorized; task outcome, prerequisites and runtime behavior remain unchanged. |

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
| Notes | Generated request and context binding: the invocation request is the published Registry 04 ArcForges.Sdk.Contracts.V1.Invocation from Contracts/public/proto/arcforges/extensions/v1/extensions.proto, not a second local Invocation DTO. Use its generated FrozenContext directly with PLT.21 FrozenContextSnapshot, bound to the resolved owner InstanceIdentity and captured before asynchronous dispatch; preserve protobuf descriptor/type and the generated request's identity, evidence, arguments and expected-version oneof. Product capability calls remain in-process. Result-version binding under contracts/02-local-rpc-operations.md §3: the local InvocationOutcome has a closed result-version arm of Revision, NativeContentRev or NonVersioned. On a successful operation whose typed owner result defines an authority version, carry that exact owner-provided version in its matching type, including an unchanged version observed by a versioned read. A successful read/no-state-change operation whose typed owner result defines no single authoritative version uses NonVersioned, which is not a version precondition and cannot chain a versioned write. A mutation whose typed owner result defines a version cannot succeed without it; expected_rev/expected_native is only a precondition, never the returned version; failure/cancellation remain non-success outcomes. A same-CommandId retry returns the originally recorded outcome and result-version arm, per the command-idempotency rule in contracts/02-local-rpc-operations.md and [WP-14.03](../../work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.03). Registry 04 shows why the arm is typed: search.query returns items and PageState without a top-level revision, IScopeOperations.CreateAnnotation/CreateFinding return NativeContentRev, chat.AppendUserMessage returns a Receipt with optional Revision, and chat.StartAgentTurn returns a Revision-bearing TaskSnapshot. Use each registered operation's typed owner contract, not field-name guessing or a flattened integer/string. The PLT.15 completion prerequisite applies only to the existing admitted helper/extension-child subset: forward the same generated Invocation through ExtensionHostServiceInvokeRequest.invocation and keep RequestMeta/LocalCallContext metadata consistent. The existing ExtensionHostServiceInvokeResponse.meta.ResponseMeta.result_rev can carry Revision but has no NativeContentRev arm; its value.result is PublicApi ToolResult without a generic result-version field (its payload remains the declared operation-specific type). A child operation whose result must carry NativeContentRev through the invocation outcome/version chain is therefore a PLT.15 completion blocker unless the existing child route can demonstrably preserve it; do not generalize this blocker to all child invocations or add wire fields here. Use PLT.15 brokered ResourceRef transfer only where that child route requires it. Do not add dependencies or another Invocation/context shape; no wire-schema change is authorized by this task. |

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
| Start prerequisites | **artifact** [PRF.02](runtime-proofs.md#task-prf-02) — a proven Avalonia Native AOT publish with zero trim/AOT diagnostics. *Why:* WP10's own header lists [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) output as 'the AOT proof and the control admission process'; every control this package introduces inherits [V-05a](../../../assurance/phase-1-official-verification.md#rule-v-05a). Owned by the native and runtime-proof lanes. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PLT.27](#task-plt-27), [PLT.29](#task-plt-29), [PLT.31](#task-plt-31), [PLT.35](#task-plt-35) |
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
| Unblocks | [APP.08](app-composition.md#task-app-08), [PLT.28](#task-plt-28), [PLT.29](#task-plt-29), [PLT.30](#task-plt-30), [PLT.31](#task-plt-31), [PLT.33](#task-plt-33), [PLT.35](#task-plt-35) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**`<br>`DesktopPlatform:Directory.Packages.props (append only ArcForges.Desktop.Shell and ArcForges.Desktop.Shell.Tests to the existing ArcForges.Contracts.Foundation 1.0.0-ci.216.1 MSBuildProjectName selector; preserve the 1.0.0-ci.113.1 default)`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only exact PLT.27 public API to direct-test bindings)`<br>`DesktopPlatform:eng/policy/architecture-projects.json (append only the PLT.27 Shell production and test project classifications)`<br>`DesktopPlatform:eng/policy/dependency-policy.json (refresh only exact task-owned input hashes and active receipt pointer)`<br>`DesktopPlatform:eng/policy/dependency-reviews/plt-27-r1.json (one immutable PLT.27 dependency receipt successor after rebase)`<br>`DesktopPlatform:eng/policy/licence-boundary.json (append only exact PLT.27 Shell production and test project rows)`<br>`DesktopPlatform:eng/policy/runtime-ownership.json (append only exact PLT.27 Shell production and test project rows)`<br>`DesktopPlatform:eng/policy/reconciliation/active-projects.json (append only exact PLT.27 Shell project registrations)`<br>`DesktopPlatform:eng/policy/reconciliation/directories.json (append only exact PLT.27 Shell directory registrations)`<br>`DesktopPlatform:eng/policy/reconciliation/source.json (refresh only the exact source inventory snapshot required by the existing reconciliation gate)`<br>`DesktopPlatform:eng/provenance/files.json (append only exact PLT.27-owned firstParty paths and immutable receipt)` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline tests: restore tests across missing panel, changed display arrangement, corrupted layout state; device-local assertion. |
| Completion evidence | Layout restore matrix. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/DesignSystem/ArcForges.Desktop.Shell does not exist. |
| Notes | [ADP-07](../adoption.md#rule-adp-07) support is limited to the exact policy, reconciliation, provenance and central package configuration paths listed above, required to bind the task-owned Shell production/test projects, APIs, direct tests, source files and project locks to existing gates. The only Directory.Packages.props change authorized is to append ArcForges.Desktop.Shell and ArcForges.Desktop.Shell.Tests to the existing ArcForges.Contracts.Foundation 1.0.0-ci.216.1 MSBuildProjectName selector introduced by PLT.19. This changes only those two projects' selection from the repository-wide 1.0.0-ci.113.1 default to the already-admitted 1.0.0-ci.216.1 coordinate; preserve that default and all other selectors. Package identity, the available package coordinate/version set and aggregate dependency closure remain unchanged. The only corresponding semantic lock changes permitted are in src/DesignSystem/ArcForges.Desktop.Shell/packages.lock.json and src/DesignSystem/ArcForges.Desktop.Shell/Tests/packages.lock.json, reflecting that exact Foundation project edge; no other lockfile may change semantically. The PLT.27 dependency-policy/plt-27-r1 successor must record exactly these 19 consumers of 1.0.0-ci.216.1: LocalRpcAotTests, ArcForges.Application.Abstractions, ArcForges.Capabilities, ArcForges.Capabilities.Tests, ArcForges.ContentSandbox, ArcForges.Contributions, ArcForges.Contributions.Tests, ArcForges.Foundation, ArcForges.Foundation.Tests, ArcForges.Observability, ArcForges.Observability.Tests, ArcForges.Persistence.Resources, ArcForges.Persistence.Resources.Tests, ArcForges.Persistence.Sqlite, ArcForges.Security, ArcForges.Security.Tests, ArcForges.Tests.PersistenceTests, ArcForges.Desktop.Shell and ArcForges.Desktop.Shell.Tests. Preserve the immutable PLT.19 receipt as the PLT.27 successor's direct predecessor and the complete PLT.19 history. Append only exact task-owned rows; refresh only exact input hashes, the current immutable dependency-review successor and the existing reconciliation snapshot fields required by those paths. Preserve unrelated records, policy semantics, schemas, generators and checkers. Do not activate packages or change package inventory, package identity, available coordinate/version set, aggregate dependency closure, or PLT.35's package-activation boundary. These bindings use RES-desktopplatform-policy-data for task-owned policy/architecture/traceability entries and retain RES-desktopplatform-build-config for solution, central package selector, CI and the two project locks; no other shared resource is authorized. Task outcome, prerequisites and runtime behavior remain unchanged. |

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
| Unblocks | [PLT.32](#task-plt-32), [PLT.35](#task-plt-35) |
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
| Completion prerequisites | **integration** [PLT.27](#task-plt-27) — PLT.27 Shell project and test host are integrated. *Why:* PLT.29 adds settings sources and tests to the Shell project and reuses its project-owned ApplicationKey and atomic file-writer foundation; it can be developed against the frozen PLT.27 candidate but cannot complete until PLT.27 is integrated. |
| Unblocks | [PLT.35](#task-plt-35) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only six PLT.29 public API to direct-[Fact] test bindings)`<br>`DesktopPlatform:eng/provenance/files.json (append only four PLT.29 Settings first-party source/test paths)` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
| Validation | Offline tests: resolution order tests across every scope combination; explainability tests; migration test. |
| Completion evidence | Settings resolution and explainability results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |
| Notes | The only supporting-file additions are six exact public ordinary API-to-direct-[Fact] bindings in eng/policy/architecture-contract-tests.json for DeviceLocalSettingsStore.CreateSyncSnapshot, DeviceLocalSettingsStore.Load, DeviceLocalSettingsStore.Save, ISettingSchema.Migrate, ScopedSettingsResolver.Resolve<T>, and SettingDefinition<T>.ToStoredValue; and four first-party provenance entries in eng/provenance/files.json for src/DesignSystem/ArcForges.Desktop.Shell/Settings/DeviceLocalSettingsStore.cs, src/DesignSystem/ArcForges.Desktop.Shell/Settings/ScopedSettings.cs, src/DesignSystem/ArcForges.Desktop.Shell/Settings/ScopedSettingsResolver.cs, and src/DesignSystem/ArcForges.Desktop.Shell/Tests/Settings/ScopedSettingsTests.cs. The six bindings target the task-owned direct [Fact] methods SynchronizationProjectionNeverIncludesDeviceOrInstanceSettings, StoreMigratesOlderValuesAtomicallyAndRefusesDowngradeWithoutChangingTheFile, and ResolutionCoversEveryScopeCombinationAndExplainsTheWinningSource. No project, csproj, solution, workflow, lock, dependency input/closure, immutable dependency-admission receipt, licence, runtime ownership, reconciliation, package inventory/identity, NOTICE, checker, or algorithm changes are in scope. |

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
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only four exact PLT.30 public ordinary API-to-direct-[Fact] bindings)`<br>`DesktopPlatform:eng/provenance/files.json (append only firstParty classifications for the two PLT.30-owned Attention source and test files)` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline tests: missed-notification test asserting durable state survives; sensitivity test on notification content. |
| Completion evidence | Missed-notification durability result. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |
| Notes | The only supporting-file additions are four exact public ordinary API-to-direct-[Fact] bindings in eng/policy/architecture-contract-tests.json and two firstParty classifications in eng/provenance/files.json for src/DesignSystem/ArcForges.Desktop.Shell/Attention/AttentionModel.cs and src/DesignSystem/ArcForges.Desktop.Shell/Tests/AttentionModelTests.cs. Bind ArcForges.Desktop.Shell.AttentionModel.Publish(ArcForges.Desktop.Shell.AttentionItem, System.Func<ArcForges.Desktop.Shell.SystemNotificationContent, bool>?, ArcForges.Desktop.Shell.NotificationPreviewConsent), ArcForges.Desktop.Shell.AttentionModel.Snapshot(), and ArcForges.Desktop.Shell.AttentionModel.RemoveResolved(string) directly to ArcForges.Desktop.Shell.Tests.AttentionModelTests.MissedNotificationLeavesDurableAttentionUntilOwnerResolvesIt(); bind ArcForges.Desktop.Shell.AttentionModel.CreateSystemNotificationContent(ArcForges.Desktop.Shell.AttentionItem, ArcForges.Desktop.Shell.NotificationPreviewConsent) directly to ArcForges.Desktop.Shell.Tests.AttentionModelTests.SensitiveSystemNotificationUsesGenericContentUnlessPreviewConsentIsExplicit(). RES-architecture-tests and RES-desktopplatform-policy-data are append-only task-owned rows under their existing protocols. No project, csproj, solution, workflow, lock, dependency input/closure, immutable dependency-admission receipt, licence, runtime ownership, reconciliation, package inventory/identity, NOTICE, checker, algorithm, or unrelated architecture/provenance row changes are authorized. The outcome and prerequisite remain unchanged. |

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
| Completion prerequisites | **integration** [PLT.27](#task-plt-27) — PLT.27 Shell project and test host are integrated. *Why:* PLT.31 adds the error presentation implementation, resources and tests to the Shell project; it can be validated against the frozen PLT.27 candidate but cannot complete until the Shell project and test host are integrated. |
| Unblocks | [PLT.35](#task-plt-35), [PLT.52](#task-plt-52) |
| Write scope | `DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/**`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only the exact PLT.31 ErrorPresenter.Present(TypedFailure) to direct-[Fact] test binding)`<br>`DesktopPlatform:eng/provenance/files.json (append only the three PLT.31 Errors source/resource/test first-party paths)` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
| Validation | Offline tests: no raw exception text displayed; coverage that every registered reason code has a message. |
| Completion evidence | Raw-exception prohibition and reason-code coverage. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |
| Notes | The only supporting-file additions are one exact ordinary public API-to-direct-[Fact] binding in eng/policy/architecture-contract-tests.json: ArcForges.Desktop.Shell.Errors.ErrorPresenter.Present(ArcForges.Foundation.Errors.TypedFailure) maps to ArcForges.Desktop.Shell.Tests.ErrorPresentationTests.PresentationUsesOnlyRegisteredTextAndNeverEchoesExceptionDetailsOrPaths(). The only first-party provenance additions are src/DesignSystem/ArcForges.Desktop.Shell/Errors/ErrorPresentationStrings.resx, src/DesignSystem/ArcForges.Desktop.Shell/Errors/ErrorPresenter.cs, and src/DesignSystem/ArcForges.Desktop.Shell/Tests/ErrorPresentationTests.cs. No project, csproj, solution, workflow, lock, dependency input/closure, immutable dependency-admission receipt, licence, runtime ownership, reconciliation, package inventory/identity, NOTICE, checker, or algorithm changes are in scope. |

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
| Validation | Offline tests: startup budget measurement for the ArcScope host (local perf harness, not hosted CI); shutdown-during-work test; single-instance routing test. |
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
| Start prerequisites | **artifact** [PRF.02](runtime-proofs.md#task-prf-02) — the established AOT-publish-with-zero-diagnostics harness/process. *Why:* this substep applies the same proof methodology [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) establishes to each additional control the shell adopts; it is ongoing (a standing admission process), not a one-time gate. |
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
| Obligations | [WP-10.90](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.90) — full |
| Provides | designsystem-shell-packages |
| Start prerequisites | **artifact** [PLT.26](#task-plt-26) — tokens. *Why:* publish needs the complete substep set.<br>**artifact** [PLT.27](#task-plt-27) — windows/panels. *Why:* same.<br>**artifact** [PLT.28](#task-plt-28) — commands. *Why:* same.<br>**artifact** [PLT.29](#task-plt-29) — settings. *Why:* same.<br>**artifact** [PLT.30](#task-plt-30) — attention. *Why:* same.<br>**artifact** [PLT.31](#task-plt-31) — error presentation. *Why:* same.<br>**artifact** [PLT.32](#task-plt-32) — lifecycle/menus. *Why:* same.<br>**artifact** [PLT.33](#task-plt-33) — a11y/l10n. *Why:* same.<br>**artifact** [PLT.34](#task-plt-34) — control admission. *Why:* same. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:eng/packaging/packages.json`<br>`DesktopPlatform:src/DesignSystem/ArcForges.DesignSystem/ArcForges.DesignSystem.csproj (final IsPackable/package activation only; PLT.26 remains non-packable)`<br>`DesktopPlatform:src/DesignSystem/ArcForges.Desktop.Shell/ArcForges.Desktop.Shell.csproj (final IsPackable/package activation only; PLT.26 remains non-packable)` |
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
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only PLT.37 RP-10 direct public-API-to-[Fact] mappings from src/BuildingBlocks/ArcForges.Security/RiskModel.cs to src/BuildingBlocks/ArcForges.Security/Tests/RiskModelTests.cs)`<br>`DesktopPlatform:eng/provenance/files.json (ADP-07 append only firstParty rows for src/BuildingBlocks/ArcForges.Security/RiskModel.cs and src/BuildingBlocks/ArcForges.Security/Tests/RiskModelTests.cs)` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline unit tests exhaustively enumerate descriptor baselines R0–R4 and every runtime-modifier combination; verify effective risk equals the maximum of the baseline and active fixed floors, every active modifier is explained, adding a modifier never lowers risk, descriptor risk parsing is closed to canonical R0–R4, and the three explicit R4 interactions are covered. |
| Completion evidence | Risk classification and monotonicity matrix. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |
| Notes | Fixed minimum floors: remote origin R3; automation origin/Automation actor R2; unverified package R3; large data volume R2; external egress R3; sensitive resource R2; bulk scope R2; irreversible effect R4. Actor-kind floors: None/direct human adds no floor, InternalService R1, Agent R2, Automation R2, Extension R3. Exactly three two-factor interactions additionally require R4: Automation + external egress; sensitive resource + external egress; Extension + unverified package (the privileged-extension case). Effective risk is the maximum of the declared capability baseline and all active floors; every other combination adds no interaction floor. No configurable weights, additive scoring, third-party lowering, or implicit interactions are introduced. |

<a id="task-plt-38"></a>

### PLT.38 — Decision pipeline and the four enforcement points

**Outcome.** The fourteen-step decision pipeline implemented once and invoked at each of the four enforcement points (caller pre-check, transport boundary, service-side decision, owner-side final validation always last); every step produces a typed outcome; a refusal names the failing step and reason code; the pipeline is unbypassable.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-38` and ledger record `ledger/tasks/plt-38.md` in the Plan repository; task branch `task/plt-38` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-11.02](../../work-packages/11-security-foundation.md#rule-wp-11.02) — all work except the parts mapped to PLT.57 |
| Provides | decision-pipeline; security-decision-type; permission-availability-evidence |
| Start prerequisites | **artifact** [PLT.36](#task-plt-36) — actor chain. *Why:* every pipeline step operates on the actor chain.<br>**artifact** [PLT.37](#task-plt-37) — risk model. *Why:* the pipeline classifies effective risk as one of its steps.<br>**artifact** [PLT.10](#task-plt-10) — LocalRpc session handshake ([WP-08.01](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.01)/08.02). *Why:* enforcement point 2 ('transport boundary') is literally the local IPC handshake per architecture/08-security-architecture.md SS2; the pipeline's transport-boundary step wraps this real mechanism, not a placeholder. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.02](app-composition.md#task-app-02), [GOV.16](governance.md#task-gov-16), [PLT.20](#task-plt-20), [PLT.41](#task-plt-41), [PLT.43](#task-plt-43), [PLT.46](#task-plt-46), [PLT.57](#task-plt-57) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Capabilities/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline unit tests: step-coverage test asserting every step runs; refusal matrix producing a distinct reason code per failing step; bypass test. |
| Completion evidence | Pipeline bypass, step-coverage and refusal matrix. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |
| Notes | The pipeline's availability-facing permission output is a read-only, immutable owner projection for a specific principal, capability and scope, preserving applicable constraints and lifetime. It is only a UI preflight; it is never a permission grant, resource authorization or substitute for owner-side final validation at invocation. |

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
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security.Secrets/**`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only exact PLT.40 public API-to-focused-test bindings)`<br>`DesktopPlatform:eng/policy/architecture-projects.json (append only the PLT.40 production and test project rows)`<br>`DesktopPlatform:tests/ArchitectureTests/RepositoryPolicyTests.cs (append only the exact PLT.40 Advapi32 LibraryImport owner/export mapping)`<br>`DesktopPlatform:eng/policy/licence-boundary.json (append only the PLT.40 production and test project classifications)`<br>`DesktopPlatform:eng/policy/runtime-ownership.json (append only the PLT.40 production and test project roles)`<br>`DesktopPlatform:eng/provenance/files.json (append only PLT.40 first-party source, project, test, README, lock and immutable receipt paths)`<br>`DesktopPlatform:eng/policy/reconciliation/active-projects.json (append only the exact PLT.40 production and test project path/blob rows)`<br>`DesktopPlatform:eng/policy/dependency-policy.json (add only exact PLT.40 project and lock input hashes and point reviewReceipt to the PLT.40 successor)`<br>`DesktopPlatform:eng/policy/dependency-reviews/plt-40-r1.json (new immutable PLT.40 receipt successor with the exact mirrored active input map)`<br>`DesktopPlatform:.gitleaks.toml (add exactly two PLT.40 generic-api-key AND allowlists, each with regexTarget=line and one anchored path: dependency-policy.json has its four observed whole-line alternatives and plt-40-r1.json its two observed whole-line alternatives; do not form path-by-digest cross combinations and preserve every other rule and allowlist)`<br>`DesktopPlatform:eng/test_dependency_policy.py (append only a focused test of the actual two PLT.40 Gitleaks allowlists and their exact six observed whole-line matches, rejecting swapped key/digest/path pairs, a trailing credential, unrelated 64-hex values, and any other rule)` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
| Validation | Offline tests where possible; real OS secure-storage round trips (Windows Credential Manager/keychain/keystore) are local opt-in per platform, recorded separately from CI. PLT.40 scan-support validation requires the focused actual-config positive/negative test and a passing pinned full-history Gitleaks run; no other rule, workflow, scanner behavior, or finding may be suppressed. |
| Completion evidence | Secret structural prohibitions, platform round-trip results, focused exact PLT.40 Gitleaks allowlist tests, and passing pinned full-history secret-scan evidence. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ArcForges.Security.Secrets does not exist as a separate project yet; the WP11 architecture doc names it as a new project distinct from the single 'ArcForges.Security' package registry row -. |
| Notes | Narrow [ADP-07](../adoption.md#rule-adp-07) support is limited to the exact ten additional DesktopPlatform paths listed above, plus the exact RepositoryPolicyTests.cs change authorized below. The scan-support extension authorizes exactly the six observed whole lines, in two separate path-bound groups. The dependency-policy.json group permits exactly four complete lines:     "src/BuildingBlocks/ArcForges.Security.Secrets/ArcForges.Security.Secrets.csproj": "8ff03fdcaf23b09386fac47dd5e3e4f9689a665a569137f726456c9e59a9ecef",     "src/BuildingBlocks/ArcForges.Security.Secrets/Tests/ArcForges.Security.Secrets.Tests.csproj": "d6798bbbcf980fab4467c6d831871b075e55aeef6e09c7df67c4d72cd2334120",       "src/BuildingBlocks/ArcForges.Security.Secrets/ArcForges.Security.Secrets.csproj": "8ff03fdcaf23b09386fac47dd5e3e4f9689a665a569137f726456c9e59a9ecef",       "src/BuildingBlocks/ArcForges.Security.Secrets/Tests/ArcForges.Security.Secrets.Tests.csproj": "d6798bbbcf980fab4467c6d831871b075e55aeef6e09c7df67c4d72cd2334120", The dependency-reviews/plt-40-r1.json group permits exactly the last two complete lines above. Each group has one anchored exact path, targets only generic-api-key, uses condition AND and regexTarget line, and cannot cross-combine paths and digests. The focused test must inspect the actual config, verify the four plus two matches, and reject swapped key/digest/path combinations, changed digests, appended credentials, unrelated 64-hex values, and other rules. No other finding, path, rule, scanner behavior, workflow, suppression, or dependency is authorized. The existing RES-desktopplatform-build-config append continues to cover only DesktopPlatform.slnx and .github/workflows/package-validation.yml. RES-desktopplatform-policy-data covers task-owned policy, test-map, reconciliation, dependency-admission and provenance rows under their exact scopes. The existing source write scope contains exactly the new production and test projects, including src/BuildingBlocks/ArcForges.Security.Secrets/packages.lock.json and src/BuildingBlocks/ArcForges.Security.Secrets/Tests/packages.lock.json; regenerate these locks after rebase and preserve the existing dependency closure, coordinates and versions. architecture-contract-tests.json adds only exact public API-to-focused-test bindings; architecture-projects.json, licence-boundary.json and runtime-ownership.json add only the two task-owned project rows/classifications. The PLT.40 production project role is NativeAdapter because it owns the Windows Credential Manager LibraryImport boundary; the test project remains Test. RepositoryPolicyTests.cs may only extend the closed LibraryImport owner/export map with Advapi32.dll owned by the exact directory src/BuildingBlocks/ArcForges.Security.Secrets and exactly CredWriteW, CredReadW, CredDeleteW, and CredFree. Preserve the existing ArcImageNative three-export mapping, DllImport prohibition, LibraryImport syntax checks, duplicate detection, and exact export-set checks. This does not authorize wildcard libraries, paths, owners, or entrypoints, scanner algorithm changes, a Native project, or dependency expansion. active-projects.json adds only those projects' exact paths and git blob IDs. dependency-policy.json may add only the hashes of the two project files and two lock files to inputHashes and set reviewReceipt to the new plt-40-r1 successor. The successor's review.inputHashes must exactly mirror the resulting active dependency-policy inputHashes map; it is immutable and chains from the then-current receipt. No other policy field, dependency coordinate, version, closure, or admission algorithm may change. provenance/files.json appends only first-party paths for the nine task-owned source/project/test/README/lock files and the new immutable receipt. Do not change directories.json, project-updates.json or source.json, package inventory, central package versions, dependency algorithms, or unrelated rows. These bindings authorize no new runtime behavior, dependency, package identity or security semantics and do not change PLT.40's outcome, prerequisites or completion condition. |

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

**Outcome.** The first-party C# Native AOT ContentSandbox, generated gRPC broker/control bindings and all restricted RID launch profiles (Windows AppContainer+Job Object, Linux Landlock+seccomp, macOS App-Sandbox+XPC handoff) are built and solely owned here; ContentSandbox.Contracts/.Broker and the foundation Runtime.<rid> are published before WP13 consumes them; OS containment is proven with a deliberately hostile first-party test parser. Production PDF/image libraries are WP13's job, never an upstream input here.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/plt-45` and ledger record `ledger/tasks/plt-45.md` in the Plan repository; task branch `task/plt-45` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / XL · early risk proof |
| Obligations | [WP-11.09](../../work-packages/11-security-foundation.md#rule-wp-11.09) — full; production ContentSandbox helper, real transport<br>[WP-11](../../work-packages/11-security-foundation.md#rule-wp-11) Local gRPC closure (SS7): own actual signed restricted gRPC helper, launch-secret/OS-descriptor allowlist, hostile-fixture containment, private-copy/digest validation, ConnectorBroker security boundary (real connector providers are WP41) — package-level obligation contribution |
| Provides | content-helper-isolation; contentsandbox-host |
| Start prerequisites | **artifact** [PLT.15](#task-plt-15) — LocalRpc brokered large-data mechanism ([WP-08.06](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.06)). *Why:* the sandbox's slot grant/seal/ack/cancel lifecycle rides on the generic broker [WP-08.06](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.06) defines; ContentSandbox is the first real consumer.<br>**artifact** [PLT.09](#task-plt-09) — LocalRpc transport ([WP-08.00](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.00)). *Why:* the parent-created duplex stream is the [WP-08](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08) transport this helper is launched through; restricted endpoint identity and the one-use launch secret are owned separately by PLT.10.<br>**artifact** [PLT.10](#task-plt-10) — restricted endpoint identity and one-use launch secret ([WP-08.01](../../work-packages/08-local-ipc-and-registration.md#rule-wp-08.01)). *Why:* the helper must bind to the parent-owned endpoint/process/build/protocol identity and reject stale descriptors; transport existence from PLT.09 alone does not establish this launch authorization.<br>**contract** [CON.04](contracts.md#task-con-04) — ArcForges.Contracts.LocalRpc.Sandbox generated ContentSandboxService/session/grant schema. *Why:* contracts/09-local-grpc-and-sandbox.md SS6 fixes WP03 as publishing the complete schema before this stage; ContentSandbox.Contracts is only a facade over it. |
| Entry condition | [ADOPT.02.platform](adoption.md#task-adopt-02-platform) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [NAT.14](native.md#task-nat-14) — production PDF/image parser composition rebuilt and signed on top of this same helper. *Why:* this task's own gate is explicit: 'WP13 later adds production parser composition to the same host and publishes a new immutable Runtime version; this stage has no reverse dependency on those parsers.' Full [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) closure additionally needs the [WP-41.00](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41.00) real extension proof. |
| Unblocks | [EXT.00](extensions.md#task-ext-00), [NAT.11](native.md#task-nat-11), [NAT.14](native.md#task-nat-14), [NAT.25](native.md#task-nat-25), [PLT.15](#task-plt-15), [PLT.46](#task-plt-46), [PLT.54](#task-plt-54) |
| Permitted substitutes | [SUB-hostile-test-parser](../substitutes.md#sub-hostile-test-parser) |
| Write scope | `DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox.Broker/**`<br>`DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox.Contracts/**`<br>`DesktopPlatform:src/DesktopHelpers/ArcForges.ContentSandbox/**` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) CRITICAL NUANCE: static/offline unit and policy tests run in CI, but the actual required evidence - real OS containment (AppContainer/Job Object denial, Landlock/seccomp denial, App-Sandbox/XPC denial, native crash/hang/memory-exhaustion/parent-death cleanup) - is device/OS-level execution that [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) explicitly excludes from hosted CI ('no macOS CI; no CI for... desktop GUI... sandbox execution'). This evidence MUST be recorded as local opt-in runs on each supported RID, per the ci-and-local-validation-policy.md and the architecture 24 rule 'a mocked launcher or same-user unrestricted child satisfies this gate: never'. |
| Completion evidence | Real child attempts at product-DB/token reads, outbound TCP/UDP/loopback, sibling-process access, spawn escape, oversized output; OS denial, resource bounds and parent-death cleanup on every supported RID. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/DesktopHelpers/ArcForges.ContentSandbox/ contains only Program.cs (a placeholder, per docs/runtime-ownership.md: 'the ContentSandbox scaffold is not accepted containment behavior'). ContentSandbox.Contracts and.Broker do not exist as separate projects yet. |
| Notes | This is the single highest-stakes early risk proof in the desktop platform foundation: [PG-22](../../../assurance/open-gates-register.md#rule-pg-22) explicitly states a mocked launcher or unrestricted same-user child cannot close the gate, and the failure mode (hostile parsing escaping containment) would invalidate downstream trust in every product that later touches untrusted content (assistant image/PDF previews, extensions). Recommend prioritising this alongside PLT.03 (persistence recovery). Merged duplicate integration or closure task formerly proposed as CON.96. |

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
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Observability/**`<br>`DesktopPlatform:eng/policy/architecture-contract-tests.json (append only exact PLT.48 public API-to-test bindings for the existing Observability test project)`<br>`DesktopPlatform:eng/provenance/files.json (append only first-party paths for new PLT.48 source and test files)` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
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
| Notes | Consume PLT.23's HealthDimension only as the same closed capability-probe aspect-key type defined by [WP-09](../../work-packages/09-capability-contribution-and-resource-model.md#rule-wp-09): reachable, ready, healthy, degraded and capacity. It carries no observation value or snapshot fields and is distinct from Architecture 02 §11's five independent axes (Installation, Presence, Health, Readiness, Compatibility). This clarification changes no Contracts/wire or Foundation HealthSnapshot/InstanceHealth/InstanceReadiness semantics and defines no Cloud presence/heartbeat behavior. |

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
| Completion prerequisites | **integration** [PLT.48](#task-plt-48) — PLT.48 completion, including the real Cloud HTTP/queue/worker/realtime/provider hop. *Why:* [WP-12.90](../../work-packages/12-observability-foundation.md#rule-wp-12.90)'s cross-owner trace is not closed by PLT.48's delivered local stage; keep the package closure delivered until its real Cloud integration is complete. |
| Unblocks | none |
| Write scope | `DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): offline verify/policy tests; Cloud-side hop evidence deferred per PLT.48's complete edge. |
| Completion evidence | Owned artifact and real-integration receipt per [WP-12.90](../../work-packages/12-observability-foundation.md#rule-wp-12.90). |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Not in packages.json. |

<a id="task-plt-54"></a>

### PLT.54 — Real hostile-input containment proof with production parser libraries loaded in ContentSandbox

**Outcome.** that [PG-12](../../../assurance/open-gates-register.md#rule-pg-12)/[PG-22](../../../assurance/open-gates-register.md#rule-pg-22)'s OS isolation mechanics (proven against a first-party hostile test parser in PLT.45) hold once real PDFium/OpenImageIO composition is loaded into the same helper by [WP-13.13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) ; this is the point where the SUB-hostile-test-parser substitute is actually replaced.

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
| Completion evidence | that [PG-12](../../../assurance/open-gates-register.md#rule-pg-12)/[PG-22](../../../assurance/open-gates-register.md#rule-pg-22)'s OS isolation mechanics (proven against a first-party hostile test parser in PLT.45) hold once real PDFium/OpenImageIO composition is loaded into the same helper by [WP-13.13](../../work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) ; this is the point where the SUB-hostile-test-parser substitute is actually replaced. |
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
