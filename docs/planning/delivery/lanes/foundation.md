# Foundation values — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Identity, error, revision, time and version primitives published as Foundation and Application.Abstractions.

Tasks: 7 · Owning repositories: DesktopPlatform · Integration owner(s): DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [FND.01](#task-fnd-01) | Core identity and version-axis value-type skeleton | producer | S | [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [FND.02](#task-fnd-02) | Execution identity, idempotency and Application.Abstractions ports | producer | S | [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [FND.03](#task-fnd-03) | Revision and sequence types | producer | S | [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [FND.04](#task-fnd-04) | Clock abstraction and canonical time handling | producer | S | none | not-started |
| [FND.05](#task-fnd-05) | Reason-code registry and Outcome result model | producer | M | [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [FND.06](#task-fnd-06) | Version axis value types | producer | S | none | not-started |
| [FND.07](#task-fnd-07) | Publish Foundation/Application.Abstractions and verify cross-language round trips | acceptance | S | [FND.01](#task-fnd-01) (artifact), [FND.02](#task-fnd-02) (artifact), [FND.03](#task-fnd-03) (artifact), [FND.04](#task-fnd-04) (artifact), [FND.05](#task-fnd-05) (artifact), [FND.06](#task-fnd-06) (artifact), [CON.91](contracts.md#task-con-91) (artifact) | not-started |

## Tasks

<a id="task-fnd-01"></a>

### FND.01 — Core identity and version-axis value-type skeleton

**Outcome.** ArcForges.Foundation exposes the UUID/revision/enum/error primitive types (registry-04 exact values) with generation and validation, adapting Contracts.Foundation wire types rather than redefining them.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/fnd-01` and ledger record `ledger/tasks/fnd-01.md` in the Plan repository; task branch `task/fnd-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-04.00](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.00) — all work except the parts mapped to FND.07 |
| Provides | identity-primitives; exact-value-adapters |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — ArcForges.Contracts.Foundation package: canonical UUID/Decimal/Rational/exact-value wire types and codecs. *Why:* BR-04.00 requires Foundation primitives to be adapters over the published Contracts wire types, never a duplicate/independent redefinition; the package already exists in Contracts (src/public/dotnet/ArcForges.Contracts.Foundation, Generated/ present) so this is a real but already-available artifact. |
| Entry condition | [ADOPT.02.foundation](adoption.md#task-adopt-02-foundation) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.01](app-composition.md#task-app-01), [FND.07](#task-fnd-07), [PLT.17](platform.md#task-plt-17), [PLT.36](platform.md#task-plt-36), [PLT.47](platform.md#task-plt-47), [PRF.01](runtime-proofs.md#task-prf-01), [PRF.02](runtime-proofs.md#task-prf-02), [PRF.03](runtime-proofs.md#task-prf-03) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Foundation/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) scope: Windows/Linux build + offline unit tests, compile-negative tests for identifier/axis confusion, no macOS/hosted-runtime/device CI. |
| Completion evidence | Compile-negative suite result for identifier and axis confusion; round-trip vectors for absent/default/unknown values. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/BuildingBlocks/ArcForges.Foundation/ contains only AssemblyPlaceholder.cs and a bare csproj with no PackageReference; not in eng/packaging/packages.json allowlist. Upstream Contracts.Foundation already has real generated content at Contracts HEAD e6c4a77. |

<a id="task-fnd-02"></a>

### FND.02 — Execution identity, idempotency and Application.Abstractions ports

**Outcome.** Immutable CommandId/InvocationId/AttemptId/RunId, canonical hash, Outcome<T> with typed failure/cancellation distinction, and Application.Abstractions cancellation/lifecycle ports exist as storage-free, memory-fixture-tested types.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/fnd-02` and ledger record `ledger/tasks/fnd-02.md` in the Plan repository; task branch `task/fnd-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-04.01](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.01) — full |
| Provides | execution-identity; idempotency-primitives; application-abstractions-ports |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — Contracts.Foundation exact-value/identity wire types. *Why:* same adapter requirement as FND.01; independently available now. |
| Entry condition | [ADOPT.02.foundation](adoption.md#task-adopt-02-foundation) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [PLT.01](platform.md#task-plt-01) — durable single-effect/receipt proof against real persistence. *Why:* [WP-04.01](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.01)'s own completion gate explicitly defers durable receipts/leases and crash tests to WP07/21/52; this task proves the storage-free algebra only. |
| Unblocks | [APP.04](app-composition.md#task-app-04), [EXE.01](execution.md#task-exe-01), [FND.07](#task-fnd-07), [PLT.01](platform.md#task-plt-01), [PLT.02](platform.md#task-plt-02), [PLT.06](platform.md#task-plt-06), [PLT.14](platform.md#task-plt-14) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Foundation/**`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Application.Abstractions/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline unit tests only: independent ID/hash/exact-value and state/retry algebra tests using memory-only fixtures; no storage adapter in scope. |
| Completion evidence | Storage-free command/attempt/effect identity vectors under duplication. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: ArcForges.Application.Abstractions is also a bare AssemblyPlaceholder.cs project today. |

<a id="task-fnd-03"></a>

### FND.03 — Revision and sequence types

**Outcome.** Revision (per-object monotonic, optimistic-concurrency comparable) and SequenceNumber (per-channel, gap-detecting) exist as non-interchangeable types with a compile-negative test proving they cannot be compared.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/fnd-03` and ledger record `ledger/tasks/fnd-03.md` in the Plan repository; task branch `task/fnd-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-04.02](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.02) — full |
| Provides | revision-sequence-types |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — Contracts.Foundation revision/sequence wire primitives. *Why:* same adapter requirement; independently available now. |
| Entry condition | [ADOPT.02.foundation](adoption.md#task-adopt-02-foundation) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [APP.04](app-composition.md#task-app-04), [EXE.01](execution.md#task-exe-01), [FND.07](#task-fnd-07), [PLT.01](platform.md#task-plt-01), [PLT.02](platform.md#task-plt-02) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Foundation/**` |
| Validation | Offline unit tests: optimistic concurrency conflict tests, sequence gap detection, compile-negative revision/sequence comparison test. |
| Completion evidence | Optimistic concurrency and sequence gap test results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: No Revision/Sequence types exist yet; same placeholder project as FND.01. |

<a id="task-fnd-04"></a>

### FND.04 — Clock abstraction and canonical time handling

**Outcome.** A clock abstraction provides wall-clock Instant and MonotonicTimestamp as distinct types; storage is canonical (instant plus originating zone where meaningful), presentation is localised, durations always use monotonic time.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/fnd-04` and ledger record `ledger/tasks/fnd-04.md` in the Plan repository; task branch `task/fnd-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-04.03](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.03) — full |
| Provides | clock-abstraction; instant-type; monotonic-timestamp-type |
| Start prerequisites | none |
| Entry condition | [ADOPT.02.foundation](adoption.md#task-adopt-02-foundation) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [FND.07](#task-fnd-07) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Foundation/**` |
| Validation | Offline unit tests: locale-change test asserting stored values unchanged, duration test asserting monotonic time used, DST boundary test for scheduled operations. Deterministic testing enabled by the clock abstraction itself. |
| Completion evidence | Locale, time-zone and daylight-saving test results. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: No clock abstraction exists yet. |

<a id="task-fnd-05"></a>

### FND.05 — Reason-code registry and Outcome result model

**Outcome.** A single generated reason-code registry (eng/policy/reason-codes.json, generated from source) exists with category, retryability, effect-certainty and message-key per code; Outcome<T> distinguishes success, typed failure and cancellation.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/fnd-05` and ledger record `ledger/tasks/fnd-05.md` in the Plan repository; task branch `task/fnd-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-04.04](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.04) — full |
| Provides | reason-code-registry; effect-certainty-type; outcome-result-type |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — Contracts error/reason-code wire schema. *Why:* the registry's wire shape and category taxonomy is fixed by Contracts. |
| Entry condition | [ADOPT.02.foundation](adoption.md#task-adopt-02-foundation) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [FND.07](#task-fnd-07), [PLT.01](platform.md#task-plt-01), [PLT.31](platform.md#task-plt-31), [PLT.49](platform.md#task-plt-49), [UPD.01](updater.md#task-upd-01), [UPD.06](updater.md#task-upd-06) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Foundation/**`<br>`DesktopPlatform:eng/policy/reason-codes.json` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline unit tests: registry completeness test, every failure path returns a registered code, cancellation never conflated with failure. |
| Completion evidence | Reason-code registry with a completeness report. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: eng/policy/reason-codes.json does not exist in the repository yet; eng/policy/ currently only holds WP00 to WP02 governance JSON (licence-boundary, runtime-ownership, dependency-policy, reconciliation, reference-baselines, glossary/invariants). |

<a id="task-fnd-06"></a>

### FND.06 — Version axis value types

**Outcome.** Each of the nine version axes (AppVersion, ContractSet, CapabilityVersion, NativeFormatVersion, StorageSchemaVersion, NativeAbiVersion, PolicySchemaVersion, ExtensionProtocolVersion, PackageVersion) is a distinct value type with parsing, comparison, range semantics and compile-time cross-assignment prevention.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/fnd-06` and ledger record `ledger/tasks/fnd-06.md` in the Plan repository; task branch `task/fnd-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-04.05](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.05) — full |
| Provides | version-axis-types |
| Start prerequisites | none |
| Entry condition | [ADOPT.02.foundation](adoption.md#task-adopt-02-foundation) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [FND.07](#task-fnd-07), [PLT.04](platform.md#task-plt-04) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Foundation/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline unit tests: compile-negative tests per axis pair, range comparison tests including open/partial ranges. |
| Completion evidence | Compile-negative test suite for axis confusion. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: eng/version-sources.json already declares the nine-axis schema with per-axis absence reasons and named future producers (confirmed read); no C# axis types exist yet. |

<a id="task-fnd-07"></a>

### FND.07 — Publish Foundation/Application.Abstractions and verify cross-language round trips

**Outcome.** ArcForges.Foundation and ArcForges.Application.Abstractions are packed, admitted to eng/packaging/packages.json, published from a main-branch candidate, and independently consumed to prove C#/TS round trips (values outside JS safe integers, absence/unknown values, duplicate commands, unknown effects) against Contracts' generated TS/Kotlin projections.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/fnd-07` and ledger record `ledger/tasks/fnd-07.md` in the Plan repository; task branch `task/fnd-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Package acceptance | Records the [WP-04](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-04.90](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.90) — full<br>[WP-04.00](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.00) — first real external consumption of Contracts.Foundation<br>[WP-04](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04) TypeScript/Kotlin primitive projection of registry-04 exact-value rules (UUID canonical ordering, TS bigint/Decimal, JSON exceptions) — package-level obligation contribution |
| Provides | foundation-package; application-abstractions-package |
| Start prerequisites | **artifact** [FND.01](#task-fnd-01) — identity/exact-value types. *Why:* cannot pack or round-trip test a package whose types do not exist yet.<br>**artifact** [FND.02](#task-fnd-02) — execution identity/idempotency types. *Why:* same reason.<br>**artifact** [FND.03](#task-fnd-03) — revision/sequence types. *Why:* same reason.<br>**artifact** [FND.04](#task-fnd-04) — clock abstraction. *Why:* same reason.<br>**artifact** [FND.05](#task-fnd-05) — reason-code registry. *Why:* same reason; also the completeness gate spans this evidence.<br>**artifact** [FND.06](#task-fnd-06) — version axis types. *Why:* same reason.<br>**artifact** [CON.91](contracts.md#task-con-91) — real, delivered outcome of CON.91 (WP03.01 — foundation contract types (accepted, historical)). *Why:* this integration exercises the real wP03.01 — foundation contract types (accepted, historical) instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.02.foundation](adoption.md#task-adopt-02-foundation) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:eng/packaging/packages.json`<br>`DesktopPlatform:eng/version-sources.json` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): pack once (whole-repo shared candidate version per the publish-nuget/pr-gate workflows), offline packages.py verify, no hosted runtime execution; cross-language vector tests run as local/offline unit tests against Contracts' committed fixtures, not live services. |
| Completion evidence | Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, real-versus-fixture status per the [WP-04.90](../../work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.90) template. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Neither package appears in eng/packaging/packages.json today (confirmed: only Build.Policy and five Native.* families are admitted). |
| Notes | Merged duplicate integration or closure task formerly proposed as CON.93. |
