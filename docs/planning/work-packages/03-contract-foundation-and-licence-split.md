# WP-03 — Contract Foundation and the Licence Boundary Split

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `02` · Downstream: `04`, `05`, `06`, `09`, `21`, `23`, `30`

> **Goal.** Create the contract projects the whole system speaks through — split by communication boundary, product ownership, release cadence and licence boundary — with C# as the single source of truth and every wire artifact generated from it.

---

## 1. Scope and purpose

**In scope.** The contract project structure and its licence split; the source-generated serialization posture; the generation pipeline that produces OpenAPI documents, JSON Schema and capability descriptors from C# types; the contract versioning mechanism; the baseline-diff gate; and the contract-authoring obligations that make the local RPC path AOT-correct.

**Out of scope.** The content of any specific product contract — those land with their product. The local IPC transport itself (`08`). The cloud endpoint implementations (`23`).

**Why this package exists.** **D-009** rejects a single ever-growing contracts assembly, and **D-004**/**D-021** require that the public interoperability surface be Apache-2.0 while everything else is AGPL-3.0-only. Both are structural decisions that are cheap now and extremely expensive after every product depends on the wrong shape.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/02-contracts-and-protocols.md`](../../architecture/02-contracts-and-protocols.md) | The two-layer contract model, compatibility rules and contract-authoring obligations `CA-01`–`CA-14` |
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) `§3` | The contract project split and licence enforcement rules |
| **D-009** | Contract granularity: split by boundary, ownership, cadence and licence |
| **D-004**, **D-021** | Which contract material is Apache-2.0 and which is AGPL-3.0-only |
| **V-05b** | The generated-shape obligation on every local RPC contract interface |
| `WP-01.01` output | The type-by-type assignment to each licence boundary |
| `WP-02` output | Generator settings, locked packages and the diagnostic posture |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **C# DTOs are the source of truth; OpenAPI and JSON Schema are generated** (**D-009**). A hand-edited wire schema is a defect. |
| BR-02 | **Contracts split by communication boundary, product/domain ownership, release cadence and licence boundary** (**D-009**). |
| BR-03 | **The Apache-2.0 set is exactly**: public protocol specifications, wire schemas, DTOs, public clients, contract-level validators, and the public SDK (**D-004**, **D-021**). |
| BR-04 | **No Apache-boundary project references an AGPL project**, directly or transitively (**D-004**). |
| BR-05 | **Every public DTO belongs to a source-generated serialization context.** No reflection-based serialization exists on any main path. |
| BR-06 | **Every local RPC contract interface carries the generated-shape attribute with public instance methods included** (**V-05b**), asserted by a policy test. |
| BR-07 | **Base ViewModel patterns are never shared between desktop and mobile** (**D-021**) — the shared boundary is contracts and semantics, not UI patterns. |
| BR-08 | **Contract version and application version are separate axes** (`QI-04`), and a contract change without a version change fails the build. |
| BR-09 | **Contract-level validators express wire constraints only** (**D-021**), never business policy. |
| BR-10 | **Product-domain behaviour, server orchestration, policy decisions, persistence behaviour and entitlement authority stay outside the shared boundary** (**D-021**). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Contracts/Public/ArcForges.Contracts.Foundation/` | Apache-2.0: identifiers, error model, revision, sequence, pagination, common value types |
| `src/Contracts/Public/ArcForges.Contracts.PublicApi.*/` | Apache-2.0: cloud request and response DTOs, split per domain area |
| `src/Contracts/Public/ArcForges.Contracts.Realtime/` | Apache-2.0: realtime message payloads |
| `src/Contracts/Public/ArcForges.Contracts.Capability/` | Apache-2.0: capability descriptor, action, context, resource reference, artifact, deep link, event and health types |
| `src/Contracts/Public/ArcForges.Contracts.Validation/` | Apache-2.0: contract-level validators expressing wire constraints |
| `src/Contracts/Internal/ArcForges.Contracts.LocalRpc.*/` | AGPL-3.0-only: local RPC interfaces per product boundary |
| `src/Contracts/Internal/ArcForges.Contracts.Internal.*/` | AGPL-3.0-only: internal orchestration contracts |
| `eng/build/contracts.props` | Generator configuration, serialization context settings, interceptor enablement |
| `artifacts/contracts/` | Generated OpenAPI documents, JSON Schema and capability descriptors, diffed against a committed baseline |
| `tests/ContractSchemaTests/`, `tests/ContractCompatibilityTests/` | Extended with the baseline diff and compatibility matrix |

**Major types introduced.** `ResourceRef`, `ResourceVersionRef`, `ArtifactRef`, `CapabilityDescriptor`, `ActionDescriptor`, `ContextDescriptor`, `HealthState`, `ProblemDetail`, `Revision`, `SequenceNumber`, `CommandId`, `CorrelationId`, and the per-boundary serialization contexts.

---

## 5. Required implementation work

### WP-03.00 — Create the split project structure

**What must be fully done.** The public and internal contract project trees are created per `§4`, each project declaring its SPDX identifier and licence boundary. Types are moved according to the `WP-01.01` assignment. No public project references an internal one.

**Testing requirements.** A reference-direction test asserting `BR-04`; a licence declaration test asserting every contract project declares its boundary.

**Completion gate.** The split exists, both tests pass, and the solution builds.

### WP-03.01 — Foundation contract types

**What must be fully done.** The foundation types are defined: identifier types (strongly typed, not bare primitives), the error and problem model with enumerated reason codes, `Revision`, `SequenceNumber`, pagination, and common value types. Identifier types are distinct per concept so that a workspace identifier cannot be passed where a task identifier is expected.

**Testing requirements.** Round-trip serialization for every type; a compile-time test that identifier types are not interchangeable.

**Completion gate.** Every foundation type round-trips, and identifier confusion is a compile error.

### WP-03.02 — Serialization posture

**What must be fully done.** Every public DTO belongs to a source-generated serialization context. The binary formatter used for local RPC has its generated type shapes in place. No reflection-based serialization path exists. The reflection package of the typed HTTP client is absent from the dependency graph, and its generator diagnostic is build-breaking.

**Testing requirements.** A test asserting no reflection-based serializer is reachable; a dependency check asserting the reflection package is absent; a build test asserting the generator diagnostic is an error.

**Completion gate.** All three pass. **This satisfies the packaging half of `F-026`**; the AOT publish proof completes it in `06`.

### WP-03.03 — Capability and resource contract types

**What must be fully done.** The capability descriptor, action descriptor, context descriptor, `ResourceRef`, `ResourceVersionRef`, artifact reference, deep link, event and health types are defined per the contract architecture, with `ResourceRef` rules enforced by construction: identity and metadata only, never a raw path, pointer or handle.

**Testing requirements.** A test asserting `ResourceRef` cannot carry a filesystem path or native handle; round-trip tests for every descriptor.

**Completion gate.** The types exist, the prohibition is structural, and round-trips pass.

### WP-03.04 — Local RPC contract discipline

**What must be fully done.** Local RPC interfaces are defined per product boundary. Every interface carries the generated-shape attribute including public instance methods (**V-05b**). Server target registration uses explicit generated registration; reflection convenience paths are absent. Interface style follows the hard rules of the local IPC architecture — task-returning, cancellation-aware, no overloads that generated marshalling cannot express.

**Testing requirements.** A policy test asserting the attribute on every RPC contract interface; a compile test that a non-conforming interface fails.

**Completion gate.** Every RPC contract interface conforms and the policy test guards it. **This is a precondition for `VG-04`.**

### WP-03.05 — Generation pipeline and the baseline gate

**What must be fully done.** The build generates OpenAPI documents, JSON Schema and capability descriptors from the C# source of truth into a stable artifact location, deterministically. A committed baseline exists, and the build diffs against it. A change without a declared contract version bump and a compatibility note fails.

**Testing requirements.** A determinism test — two builds produce byte-identical artifacts; a negative test — an undeclared contract change fails the build.

**Completion gate.** Generation is deterministic and the baseline gate blocks an undeclared change.

### WP-03.06 — Compatibility rules and the supported window

**What must be fully done.** The compatibility rules `VC-01`–`VC-10` are implemented as tests: additive-only changes within a version, required-field additions as breaking, unknown-field handling, and the supported client window. Golden wire vectors are captured for the initial version.

**Testing requirements.** A compatibility matrix test across the declared window using the golden vectors.

**Completion gate.** The matrix passes and the initial golden vectors are committed as immutable fixtures.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None directly; establishes revision and sequence semantics that persistence uses |
| Protocol | This package *is* the protocol foundation for local RPC, public API and realtime |
| UI | None |
| Security | Establishes the licence boundary structurally; establishes typed identifiers that prevent authorization confusion |
| Platform | The Apache boundary is what makes the mobile artifact possible at all |
| Migration | Establishes contract versioning that later migrations depend on |
| Compatibility | Establishes the baseline, the golden vectors and the supported window |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Reference-direction and licence declaration reports | `WP-03.00` |
| Round-trip results for every foundation and descriptor type | `WP-03.01`, `WP-03.03` |
| Reflection-absence and generator-diagnostic reports | `WP-03.02` |
| RPC contract policy test results | `WP-03.04` |
| Determinism proof and negative baseline-diff test | `WP-03.05` |
| Compatibility matrix results and the committed golden vectors | `WP-03.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. The contract projects are split by boundary and licence, with no public project referencing an internal one.
2. Foundation and descriptor types exist, round-trip, and make identifier confusion a compile error.
3. No reflection-based serialization path is reachable; the typed HTTP client's reflection package is absent and its diagnostic is build-breaking.
4. Every local RPC contract interface carries the generated-shape attribute, guarded by a policy test.
5. Contract artifact generation is deterministic and an undeclared change fails the build.
6. The compatibility matrix passes and the initial golden wire vectors are committed as immutable fixtures.

---

## 9. Dependencies

**Upstream.**

| Package | What this needs from it |
|---|---|
| `02` | Generator settings, locked packages, and a build that fails on diagnostics |
| `01` (via `02`) | The type-by-type licence assignment |

**Downstream.**

| Package | What it needs from here |
|---|---|
| `04` — Primitives | The foundation types it extends with identity and versioning behaviour |
| `05` — Policy tests | The contract rules to assert |
| `06` — AOT proof | Real contracts to publish and prove |
| `09` — Capability model | The descriptor types |
| `21`, `23` — Cloud | The public API contract set |
| `30` — Mobile | The Apache-2.0 contract and client set |
