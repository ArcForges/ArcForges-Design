<a id="rule-wp-04"></a>

# WP-04 — Identity, Error, Revision and Versioning Primitives

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Fix the small things that everything else is built from — identity, idempotency, revision, sequence, time, error and reason codes — so that no later package invents its own variant and no two subsystems disagree about what "the same operation" means.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Contracts; owner-specific adapters. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The behaviour behind the contract types: identifier generation and validation, the four-way execution identity set, idempotency semantics, revision and sequence rules, canonical time handling, the error and reason-code model, and the version-axis value types.

**Out of scope.** Any storage implementation (`07`). Any transport (`08`). Any authorization logic (`11`).

**Why this package exists.** The invariant catalogue contains a large family of `X ≠ Y` statements about identity — command versus invocation versus attempt, revision versus version, sequence versus revision, resource identity versus file path. These are only enforceable if the primitives make the wrong thing impossible rather than merely discouraged.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [error catalogue](../../architecture/contracts/00-operation-catalogue.md#3-the-error-model)

| Input | Why it matters |
|---|---|
| [`../../requirements/01-normative-glossary-and-invariants.md`](../../requirements/01-normative-glossary-and-invariants.md) | The invariant catalogue these primitives enforce |
| [`../../architecture/02-contracts-and-protocols.md`](../../architecture/02-contracts-and-protocols.md) | Resource reference rules and the semantic error set |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) `§4` | The four idempotency identities and their distinct roles |
| [`../../requirements/12-quality-and-compatibility-contract.md`](../../requirements/12-quality-and-compatibility-contract.md) `§11.1`, `§14` | Time handling and the nine version axes |
| [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) output | The contract types this package gives behaviour to |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) as amended by [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **`CommandId`, `InvocationId`, `AttemptId` and `RunId` are four distinct identities with four distinct roles.** Collapsing any two is a defect. |
| <a id="rule-br-02"></a>BR-02 | **A retry preserves command identity and allocates a new attempt only when retry is authorized.** Storage-free primitives express identity/effect certainty; an owner transaction plus durable receipt enforces one committed effect. Unknown external effects cannot acquire an exactly-once guarantee from the primitive. |
| <a id="rule-br-03"></a>BR-03 | **`Revision ≠ Version`** and **`Sequence ≠ Revision`**. A revision orders changes to one object; a sequence orders delivery on a channel. |
| <a id="rule-br-04"></a>BR-04 | **A resource identity is never a file path** ([I-192](../../requirements/01-normative-glossary-and-invariants.md#rule-i-192)). |
| <a id="rule-br-05"></a>BR-05 | **Canonical storage, localised presentation** ([QI-18](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-18)). Time is stored as an unambiguous instant with its originating zone where the zone is meaningful; it is never stored as a formatted string. |
| <a id="rule-br-06"></a>BR-06 | **Every failure carries an enumerated reason code**, shared by the product surface, support and telemetry ([DM-04](../../architecture/13-observability-and-operations.md#rule-dm-04) in the observability architecture). |
| <a id="rule-br-07"></a>BR-07 | **Effect certainty is part of failure classification**: whether the operation definitely did not happen, definitely did, or is unknown. |
| <a id="rule-br-08"></a>BR-08 | **The nine version axes are distinct value types**, so one cannot be assigned to another ([I-383](../../requirements/01-normative-glossary-and-invariants.md#rule-i-383)). |
| <a id="rule-br-09"></a>BR-09 | **Monotonic time is used for durations; wall-clock time is used for timestamps.** A duration is never computed by subtracting wall-clock values. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Contracts/Public/ArcForges.Contracts.Foundation/` | Identity, revision, sequence, time and error primitives gain their validation and generation behaviour |
| `src/BuildingBlocks/ArcForges.Foundation/` | Identity generation, clock abstraction, reason-code registry, result types |
| `eng/policy/reason-codes.json` | The enumerated reason-code registry, generated from source |
| `tests/ContractSchemaTests/` | Extended with primitive invariant assertions |

**Major types introduced.** `CommandId`, `InvocationId`, `AttemptId`, `RunId`, `TaskId`, `WorkspaceId`, `RealmId`, `DeviceId`, `InstallationId`, `InstanceId`, `SessionId`, `Revision`, `SequenceNumber`, `ReasonCode`, `EffectCertainty`, `Outcome<T>`, `Instant`, `MonotonicTimestamp`, and one value type per version axis.

---

## 5. Required implementation work

<a id="rule-wp-04.00"></a>

### WP-04.00 — Shared identity, error and version primitives

**What must be fully done.** Implement registry 04 exact UUID/revision/enum/error primitives and generation/recovery scopes from the published Contracts packages. Proto controls business schema; HTTP exception JSON uses source-generated serialization only.

**Testing requirements.** Cross-language vectors, absent/default/unknown values, wrong revision kind, effect-certainty and error mapping.

**Completion gate.** No OpenAPI/REST business contract or copied DTO authority is created.

<a id="rule-wp-04.01"></a>

### WP-04.01 — Execution identity and idempotency

**What must be fully done.** Implement immutable execution owner/command/run/step/attempt IDs, canonical hash and retry/effect primitives with explicit clock/cancellation interfaces. No storage adapter is required in this primitive WP.

**Testing requirements.** Independent ID/hash/exact-value and state/retry algebra tests using memory-only fixtures.

**Completion gate.** Storage-free package complete; durable receipts/leases and crash tests belong to WP07/21/52.

<a id="rule-wp-04.02"></a>

### WP-04.02 — Revision and sequence

**What must be fully done.** `Revision` implements per-object monotonic change ordering with the expected-revision comparison that optimistic concurrency uses. `SequenceNumber` implements per-channel delivery ordering with gap detection. The two are separate types and cannot be compared to one another.

**Testing requirements.** Optimistic concurrency conflict tests; sequence gap detection tests; a compile-negative test that revision and sequence cannot be compared.

**Completion gate.** Conflict and gap semantics are correct, and the types are non-interchangeable.

<a id="rule-wp-04.03"></a>

### WP-04.03 — Time

**What must be fully done.** A clock abstraction provides wall-clock instants and monotonic timestamps as separate concepts. Storage is canonical; presentation is localised. Where a wall-clock instant's originating zone is semantically meaningful — a scheduled automation, a user-visible deadline — the zone is stored alongside it rather than discarded.

**Testing requirements.** A locale-change test asserting stored values are unchanged; a duration test asserting monotonic time is used; a daylight-saving boundary test for scheduled operations.

**Completion gate.** A locale or time-zone change never alters stored data, and durations survive a clock adjustment.

<a id="rule-wp-04.04"></a>

### WP-04.04 — Error and reason codes

**Required design implementation and verification.** Register identity.last_credential and validation.ast_bounds_exceeded with no-effect/nonretryable semantics. Map simulator invalid input to validation.invalid_request. Test rejected final credential removal and rejected overbound AST before effects; validate unknown future error fallback without converting it to success/retry.

**What must be fully done.** A single reason-code registry is generated from source, with each code carrying its category, its retryability, its effect certainty and its user-facing message key. The result type expresses success, typed failure and cancellation distinctly — a cancellation is never reported as a failure.

**Testing requirements.** A registry completeness test; a test that every failure path returns a registered code; a test that cancellation and failure are distinguishable at every layer.

**Completion gate.** No failure path returns an unregistered code, and cancellation is never conflated with failure.

<a id="rule-wp-04.05"></a>

### WP-04.05 — Version axis types

**What must be fully done.** Each of the nine version axes is a distinct value type with parsing, comparison and range semantics. Cross-assignment is a compile error. Range expressions support the partial-compatibility statements the compatibility policy requires.

**Testing requirements.** Compile-negative tests per axis pair; range comparison tests including open and partial ranges.

**Completion gate.** Axes are non-interchangeable and range semantics are correct.

---

### TypeScript primitive projection

Implement the generated C#/TypeScript/Kotlin adapters for [registry 04 exact-value rules](../../architecture/contracts/04-protobuf-wire-registry.md#2-exact-values-canonical-identity-and-evolution). UUID uses canonical 16-byte ordering on protobuf, 64-bit integers use TS bigint and checked .NET/Kotlin equivalents, Decimal uses its canonical exact string, and int32 remains bounded. Standard JSON exceptions use the declared canonical string representation. Consume WP03's independent cross-language vectors; generation metadata cannot substitute for actual round-trip values. No OpenAPI business generation stage is involved.

---

<a id="rule-wp-04.90"></a>
### WP-04.90 — Verify the owned artifact and real integration

**What must be fully done.** Implement the exact ID/time/decimal/rational/cursor/error/revision/idempotency profiles. Keep public primitives separate from internal authorization implementation. Map gRPC failures without fabricating domain outcomes.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** C#/TS round trips include values outside JS safe integers, absence/unknown values, duplicate commands and unknown effects; existing error identifiers remain registered.

**Completion gate.** C#/TS round trips include values outside JS safe integers, absence/unknown values, duplicate commands and unknown effects; existing error identifiers remain registered. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Revision and sequence semantics constrain the storage schema in `07` and `21` |
| Protocol | Every message carries these primitives |
| UI | Reason codes become the source of user-facing failure messages |
| Security | Typed identifiers prevent a class of authorization confusion; effect certainty informs approval and retry decisions |
| Platform | The clock abstraction is what makes deterministic testing possible on every platform |
| Migration | Version axis types are what migration compatibility is expressed in |
| Compatibility | Range semantics are the basis of the supported window |

---

## 7. Tests and verification evidence

**Required evidence addition.** Known-producer-code closure and unknown-reader-code negative vectors.

| Evidence | Produced by |
|---|---|
| Compile-negative test suite for identifier and axis confusion | [WP-04.00](#rule-wp-04.00), [WP-04.05](#rule-wp-04.05) |
| Storage-free command/attempt/effect identity vectors under duplication; durable owner proof at WP07/21 | [WP-04.01](#rule-wp-04.01) |
| Optimistic concurrency and sequence gap test results | [WP-04.02](#rule-wp-04.02) |
| Locale, time-zone and daylight-saving test results | [WP-04.03](#rule-wp-04.03) |
| Reason-code registry with a completeness report | [WP-04.04](#rule-wp-04.04) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-04.90](#rule-wp-04.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-04.90](#rule-wp-04.90) and all inherited domain-specific gates must pass on the same candidate closure. C#/TS round trips include values outside JS safe integers, absence/unknown values, duplicate commands and unknown effects; existing error identifiers remain registered.

**Additional completion requirement.** Generated reason vocabulary agrees with all operation declarations while clients tolerate additive unknown responses safely.

**All of the following, with recorded evidence:**

1. Identifier and version-axis confusion is a compile error, and every primitive round-trips.
2. Command and attempt identities, canonical hashes and uncertainty/retry types are unambiguous; durable single-effect/receipt proof is deferred explicitly to owner persistence in 07/21/52.
3. Revision and sequence implement conflict and gap semantics correctly and are non-interchangeable.
4. A locale or time-zone change never alters stored data, and durations use monotonic time.
5. Every failure path returns a registered reason code with a category, retryability and effect certainty; cancellation is never reported as failure.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [FND.01](../delivery/lanes/foundation.md#task-fnd-01) | [WP-04.00](04-identity-error-and-versioning-primitives.md#rule-wp-04.00) (all work except the parts mapped to FND.07) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract) |
| [FND.02](../delivery/lanes/foundation.md#task-fnd-02) | [WP-04.01](04-identity-error-and-versioning-primitives.md#rule-wp-04.01) (full) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract) |
| [FND.03](../delivery/lanes/foundation.md#task-fnd-03) | [WP-04.02](04-identity-error-and-versioning-primitives.md#rule-wp-04.02) (full) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract) |
| [FND.04](../delivery/lanes/foundation.md#task-fnd-04) | [WP-04.03](04-identity-error-and-versioning-primitives.md#rule-wp-04.03) (full) | none |
| [FND.05](../delivery/lanes/foundation.md#task-fnd-05) | [WP-04.04](04-identity-error-and-versioning-primitives.md#rule-wp-04.04) (full) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract) |
| [FND.06](../delivery/lanes/foundation.md#task-fnd-06) | [WP-04.05](04-identity-error-and-versioning-primitives.md#rule-wp-04.05) (full) | none |
| [FND.07](../delivery/lanes/foundation.md#task-fnd-07) | [WP-04.90](04-identity-error-and-versioning-primitives.md#rule-wp-04.90) (full)<br>[WP-04.00](04-identity-error-and-versioning-primitives.md#rule-wp-04.00) (first real external consumption of Contracts.Foundation)<br>[WP-04](04-identity-error-and-versioning-primitives.md#rule-wp-04) TypeScript/Kotlin primitive projection of registry-04 exact-value rules (UUID canonical ordering, TS bigint/Decimal, JSON exceptions) (package-level obligation contribution) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (artifact) |

**Consumers outside this package:** [APP.01](../delivery/lanes/app-composition.md#task-app-01), [APP.04](../delivery/lanes/app-composition.md#task-app-04), [EXE.01](../delivery/lanes/execution.md#task-exe-01), [PLT.01](../delivery/lanes/platform.md#task-plt-01), [PLT.02](../delivery/lanes/platform.md#task-plt-02), [PLT.04](../delivery/lanes/platform.md#task-plt-04), [PLT.06](../delivery/lanes/platform.md#task-plt-06), [PLT.14](../delivery/lanes/platform.md#task-plt-14), [PLT.17](../delivery/lanes/platform.md#task-plt-17), [PLT.31](../delivery/lanes/platform.md#task-plt-31), [PLT.36](../delivery/lanes/platform.md#task-plt-36), [PLT.47](../delivery/lanes/platform.md#task-plt-47), [PLT.49](../delivery/lanes/platform.md#task-plt-49), [PRF.01](../delivery/lanes/runtime-proofs.md#task-prf-01), [PRF.02](../delivery/lanes/runtime-proofs.md#task-prf-02), [PRF.03](../delivery/lanes/runtime-proofs.md#task-prf-03), [UPD.01](../delivery/lanes/updater.md#task-upd-01), [UPD.06](../delivery/lanes/updater.md#task-upd-06).

<!-- delivery-graph:end -->

