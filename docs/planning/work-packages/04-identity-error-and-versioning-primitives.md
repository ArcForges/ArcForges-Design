# WP-04 — Identity, Error, Revision and Versioning Primitives

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `03` · Downstream: `06`, `07`, `11`, `12`

> **Goal.** Fix the small things that everything else is built from — identity, idempotency, revision, sequence, time, error and reason codes — so that no later package invents its own variant and no two subsystems disagree about what "the same operation" means.

---

## 1. Scope and purpose

**In scope.** The behaviour behind the contract types: identifier generation and validation, the four-way execution identity set, idempotency semantics, revision and sequence rules, canonical time handling, the error and reason-code model, and the version-axis value types.

**Out of scope.** Any storage implementation (`07`). Any transport (`08`). Any authorization logic (`11`).

**Why this package exists.** The invariant catalogue contains a large family of `X ≠ Y` statements about identity — command versus invocation versus attempt, revision versus version, sequence versus revision, resource identity versus file path. These are only enforceable if the primitives make the wrong thing impossible rather than merely discouraged.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/01-normative-glossary-and-invariants.md`](../../requirements/01-normative-glossary-and-invariants.md) | The invariant catalogue these primitives enforce |
| [`../../architecture/02-contracts-and-protocols.md`](../../architecture/02-contracts-and-protocols.md) | Resource reference rules and the semantic error set |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) `§4` | The four idempotency identities and their distinct roles |
| [`../../requirements/12-quality-and-compatibility-contract.md`](../../requirements/12-quality-and-compatibility-contract.md) `§11.1`, `§14` | Time handling and the nine version axes |
| `WP-03` output | The contract types this package gives behaviour to |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **`CommandId`, `InvocationId`, `AttemptId` and `RunId` are four distinct identities with four distinct roles.** Collapsing any two is a defect. |
| BR-02 | **A retry reuses the command identity and allocates a new attempt identity.** This is what makes exactly-once effect achievable. |
| BR-03 | **`Revision ≠ Version`** and **`Sequence ≠ Revision`**. A revision orders changes to one object; a sequence orders delivery on a channel. |
| BR-04 | **A resource identity is never a file path** (`I-192`). |
| BR-05 | **Canonical storage, localised presentation** (`QI-18`). Time is stored as an unambiguous instant with its originating zone where the zone is meaningful; it is never stored as a formatted string. |
| BR-06 | **Every failure carries an enumerated reason code**, shared by the product surface, support and telemetry (`DM-04` in the observability architecture). |
| BR-07 | **Effect certainty is part of failure classification**: whether the operation definitely did not happen, definitely did, or is unknown. |
| BR-08 | **The nine version axes are distinct value types**, so one cannot be assigned to another (`I-383`). |
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

### WP-04.00 — Identifier types

**What must be fully done.** Each identifier concept is a distinct value type with its own generation, parsing, validation and serialization. Identifiers are opaque to consumers, sortable where ordering is meaningful, and never carry embedded semantics that could be parsed by a client. Cross-assignment between identifier types is a compile error.

**Testing requirements.** A compile-negative test per identifier pair; round-trip and parse-rejection tests; a collision and distribution test for generated identifiers.

**Completion gate.** Cross-assignment fails to compile, and every identifier round-trips and rejects malformed input.

### WP-04.01 — Execution identity and idempotency

**What must be fully done.** The four execution identities are implemented with their relationships: one command may have many attempts; one invocation belongs to one attempt; one run may contain many invocations. An idempotency helper expresses "same command, new attempt" so that retry logic is written once. Duplicate-detection semantics are defined: what counts as the same command, and for how long a result is remembered.

**Testing requirements.** A retry test asserting one effect from many attempts; a concurrency test asserting two simultaneous submissions of one command yield one effect; a retention test for the duplicate window.

**Completion gate.** Exactly-once effect holds under duplication, retry and concurrency.

### WP-04.02 — Revision and sequence

**What must be fully done.** `Revision` implements per-object monotonic change ordering with the expected-revision comparison that optimistic concurrency uses. `SequenceNumber` implements per-channel delivery ordering with gap detection. The two are separate types and cannot be compared to one another.

**Testing requirements.** Optimistic concurrency conflict tests; sequence gap detection tests; a compile-negative test that revision and sequence cannot be compared.

**Completion gate.** Conflict and gap semantics are correct, and the types are non-interchangeable.

### WP-04.03 — Time

**What must be fully done.** A clock abstraction provides wall-clock instants and monotonic timestamps as separate concepts. Storage is canonical; presentation is localised. Where a wall-clock instant's originating zone is semantically meaningful — a scheduled automation, a user-visible deadline — the zone is stored alongside it rather than discarded.

**Testing requirements.** A locale-change test asserting stored values are unchanged; a duration test asserting monotonic time is used; a daylight-saving boundary test for scheduled operations.

**Completion gate.** A locale or time-zone change never alters stored data, and durations survive a clock adjustment.

### WP-04.04 — Error and reason codes

**What must be fully done.** A single reason-code registry is generated from source, with each code carrying its category, its retryability, its effect certainty and its user-facing message key. The result type expresses success, typed failure and cancellation distinctly — a cancellation is never reported as a failure.

**Testing requirements.** A registry completeness test; a test that every failure path returns a registered code; a test that cancellation and failure are distinguishable at every layer.

**Completion gate.** No failure path returns an unregistered code, and cancellation is never conflated with failure.

### WP-04.05 — Version axis types

**What must be fully done.** Each of the nine version axes is a distinct value type with parsing, comparison and range semantics. Cross-assignment is a compile error. Range expressions support the partial-compatibility statements the compatibility policy requires.

**Testing requirements.** Compile-negative tests per axis pair; range comparison tests including open and partial ranges.

**Completion gate.** Axes are non-interchangeable and range semantics are correct.

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

| Evidence | Produced by |
|---|---|
| Compile-negative test suite for identifier and axis confusion | `WP-04.00`, `WP-04.05` |
| Exactly-once effect proof under duplication, retry and concurrency | `WP-04.01` |
| Optimistic concurrency and sequence gap test results | `WP-04.02` |
| Locale, time-zone and daylight-saving test results | `WP-04.03` |
| Reason-code registry with a completeness report | `WP-04.04` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Identifier and version-axis confusion is a compile error, and every primitive round-trips.
2. Exactly-once effect holds for one command under duplication, retry and concurrency.
3. Revision and sequence implement conflict and gap semantics correctly and are non-interchangeable.
4. A locale or time-zone change never alters stored data, and durations use monotonic time.
5. Every failure path returns a registered reason code with a category, retryability and effect certainty; cancellation is never reported as failure.

---

## 9. Dependencies

**Upstream.** `03` — the contract types these primitives implement.

**Downstream.**

| Package | What it needs from here |
|---|---|
| `06` — AOT proof | Primitives that must survive trimming and AOT |
| `07` — Persistence | Revision, sequence and time semantics |
| `11` — Security | Typed identifiers and the actor identity set |
| `12` — Observability | Correlation, causation and reason codes |
| `16` — Execution engine | The four execution identities and idempotency |
