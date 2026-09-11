<a id="rule-wp-04"></a>

# WP-04 — Identity, Error, Revision and Versioning Primitives

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `03` · Downstream: `06`, `07`, `11`, `12`

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

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **`CommandId`, `InvocationId`, `AttemptId` and `RunId` are four distinct identities with four distinct roles.** Collapsing any two is a defect. |
| BR-02 | **A retry preserves command identity and allocates a new attempt only when retry is authorized.** Storage-free primitives express identity/effect certainty; an owner transaction plus durable receipt enforces one committed effect. Unknown external effects cannot acquire an exactly-once guarantee from the primitive. |
| BR-03 | **`Revision ≠ Version`** and **`Sequence ≠ Revision`**. A revision orders changes to one object; a sequence orders delivery on a channel. |
| BR-04 | **A resource identity is never a file path** ([I-192](../../requirements/01-normative-glossary-and-invariants.md#rule-i-192)). |
| BR-05 | **Canonical storage, localised presentation** ([QI-18](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-18)). Time is stored as an unambiguous instant with its originating zone where the zone is meaningful; it is never stored as a formatted string. |
| BR-06 | **Every failure carries an enumerated reason code**, shared by the product surface, support and telemetry ([DM-04](../../architecture/13-observability-and-operations.md#rule-dm-04) in the observability architecture). |
| BR-07 | **Effect certainty is part of failure classification**: whether the operation definitely did not happen, definitely did, or is unknown. |
| BR-08 | **The nine version axes are distinct value types**, so one cannot be assigned to another ([I-383](../../requirements/01-normative-glossary-and-invariants.md#rule-i-383)). |
| BR-09 | **Monotonic time is used for durations; wall-clock time is used for timestamps.** A duration is never computed by subtracting wall-clock values. |

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

### WP-04.00 — Identifier types

**What must be fully done.** Each identifier concept is a distinct value type with its own generation, parsing, validation and serialization. Identifiers are opaque to consumers, sortable where ordering is meaningful, and never carry embedded semantics that could be parsed by a client. Cross-assignment between identifier types is a compile error.

**Testing requirements.** A compile-negative test per identifier pair; round-trip and parse-rejection tests; a collision and distribution test for generated identifiers.

**Completion gate.** Cross-assignment fails to compile, and every identifier round-trips and rejects malformed input.

<a id="rule-wp-04.01"></a>

### WP-04.01 — Execution identity and idempotency

**What must be fully done.** The four execution identities are implemented with their relationships: one command may have many attempts; one invocation belongs to one attempt; one run may contain many invocations. An idempotency helper validates the fixed command fingerprint and permitted retry/effect advice. Implement the retention/replay profile in the operation catalogue as constants/contracts; owner stores enforce it at WP07/14/21, never inside this storage-free helper.

**Testing requirements.** Identity/fingerprint and retry-advice vectors, including unknown effect refusing blind retry. WP07/14 supply actual transaction/concurrent duplicate-effect proofs and the owner-defined receipt-retention policy; this storage-free package cannot claim persistence enforcement.

**Completion gate.** Identity/hash/retry-advice vectors pass and unknown effects refuse automatic resend. Owner transaction/receipt enforcement is proven by WP07/14/21; no storage-free exactly-once claim remains.

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

Implement the C# serializers and metadata projection for the exact wire rules in [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md). IDs are opaque strings; 64-bit revision/sequence/token/byte/microcredit values and decimal rates preserve exact canonical strings. Bound int32 counters remain numbers. This package consumes [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03)'s initial vectors and extends them as primitives stabilize. Runtime JSON and generated OpenAPI must agree; metadata-only stringification is a failing gate.

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
| Exactly-once effect proof under duplication, retry and concurrency | [WP-04.01](#rule-wp-04.01) |
| Optimistic concurrency and sequence gap test results | [WP-04.02](#rule-wp-04.02) |
| Locale, time-zone and daylight-saving test results | [WP-04.03](#rule-wp-04.03) |
| Reason-code registry with a completeness report | [WP-04.04](#rule-wp-04.04) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-04.90](#rule-wp-04.90) and all inherited domain-specific gates must pass on the same candidate closure. C#/TS round trips include values outside JS safe integers, absence/unknown values, duplicate commands and unknown effects; existing error identifiers remain registered.

**Additional completion requirement.** Generated reason vocabulary agrees with all operation declarations while clients tolerate additive unknown responses safely.

**All of the following, with recorded evidence:**

1. Identifier and version-axis confusion is a compile error, and every primitive round-trips.
2. Exactly-once effect holds for one command under duplication, retry and concurrency.
3. Revision and sequence implement conflict and gap semantics correctly and are non-interchangeable.
4. A locale or time-zone change never alters stored data, and durations use monotonic time.
5. Every failure path returns a registered reason code with a category, retryability and effect certainty; cancellation is never reported as failure.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03)

**Downstream — consumers of these released outputs.**

- [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)
- [WP-07](07-local-persistence-foundation.md#rule-wp-07)
- [WP-11](11-security-foundation.md#rule-wp-11)
- [WP-12](12-observability-foundation.md#rule-wp-12)


---
