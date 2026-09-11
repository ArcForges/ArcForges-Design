<a id="rule-wp-03"></a>

# WP-03 — Proto Contract Foundation and License Split

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `02` · Downstream: `04`, `05`, `06`, `09`, `21`, `23`, `30`

> **Goal.** Publish the handwritten proto authority and generated C#/TS public/internal package closure, exact-value fixtures and compatibility baselines before product/persistence consumers.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Contracts. Inputs: the assigned exact Contracts packages/descriptors and actual provider artifacts; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The contract project structure and its licence split; the source-generated serialization posture; the pipeline that generates protobuf descriptors, C#/TS DTOs/clients/validators and declared HTTP-exception schemas; the contract versioning mechanism; the baseline-diff gate; and the contract-authoring obligations that make the local RPC path AOT-correct.

**Out of scope.** Product behavior implementations; the complete selected initial wire records and operation signatures are already specified and generated here. The local IPC transport itself (`08`). The cloud endpoint implementations (`23`).

**Why this package exists.** **[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)** rejects a single ever-growing contracts assembly, and **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)** require that the public interoperability surface be Apache-2.0 while everything else is AGPL-3.0-only. Both are structural decisions that are cheap now and extremely expensive after every product depends on the wrong shape.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers), [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile) and [scope.measurement.v1](../../requirements/products/arcscope.md#measurement-profile) are definitions, not decisions deferred to later product packages.

| Input | Why it matters |
|---|---|
| [`../../architecture/02-contracts-and-protocols.md`](../../architecture/02-contracts-and-protocols.md) | The two-layer contract model, compatibility rules and contract-authoring obligations [CA-01](../../architecture/02-contracts-and-protocols.md#rule-ca-01)–[CA-14](../../architecture/02-contracts-and-protocols.md#rule-ca-14) |
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) `§3` | The contract project split and licence enforcement rules |
| **[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)** | Contract granularity: split by boundary, ownership, cadence and licence |
| **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)** | Which contract material is Apache-2.0 and which is AGPL-3.0-only |
| **[V-05b](../../assurance/phase-1-official-verification.md#rule-v-05b)** | The generated-shape obligation on every local RPC contract interface |
| [WP-01.01](01-repository-reconciliation-and-target-layout.md#rule-wp-01.01) output | The type-by-type assignment to each licence boundary |
| [WP-02](02-build-governance-and-analyzer-policy.md#rule-wp-02) output | Generator settings, locked packages and the diagnostic posture |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Handwritten proto is the business wire authority; C#/TS DTOs, validators and descriptors are generated** (**[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)**). Hand-edited generated DTOs or undeclared proto changes are defects. |
| BR-02 | **Contracts split by communication boundary, product/domain ownership, release cadence and licence boundary** (**[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)**). |
| BR-03 | **The Apache-2.0 set is exactly**: public protocol specifications, wire schemas, DTOs, public clients, contract-level validators, and the public SDK (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| <a id="rule-br-04"></a>BR-04 | **No Apache-boundary project references an AGPL project**, directly or transitively (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |
| BR-05 | C#/TS wire types derive from handwritten proto descriptors. Native code uses generated protobuf serializers; HTTP exceptions use explicit source-generated JSON metadata. No parallel handwritten business DTO or C#-exported wire authority. |
| BR-06 | **Every local RPC contract interface carries the generated service/descriptor identity with public instance methods included** (**[V-05b](../../assurance/phase-1-official-verification.md#rule-v-05b)**), asserted by a policy test. |
| BR-07 | **Base ViewModel patterns are never shared between desktop and mobile** (**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**) — the shared boundary is contracts and semantics, not UI patterns. |
| BR-08 | **Contract version and application version are separate axes** ([QI-04](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-04)), and a contract change without a version change fails the build. |
| BR-09 | **Contract-level validators express wire constraints only** (**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**), never business policy. |
| BR-10 | **Product-domain behaviour, server orchestration, policy decisions, persistence behaviour and entitlement authority stay outside the shared boundary** (**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |

---

## 4. Projects, directories, files and major types affected

All paths are in ArcForges-Contracts under the [selected package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry).

| Location | Deliverable |
|---|---|
| public/proto/, internal/proto/ | Handwritten initial schema/service/field/enum profiles from the wire registry; Apache versus AGPL dependency closure |
| public/http/, internal/ai-http/, fixtures/public/, fixtures/internal/ | Selected CF/auth/provider HTTP exceptions, independent canonical positive/negative vectors |
| generated/csharp/, generated/typescript/ | Generated DTOs, service descriptors/clients and wire validators; never hand edited |
| src/transport/ | Apache RN unary gRPC-Web adapter and selected public C# transport composition only |
| eng/, artifacts/contracts/ | Pinned generation, descriptor/breaking-change baselines, signed versioned package manifests and candidate publication |
| tests/ | Schema closure, exact-value/unknown-field/conformance vectors and C#/TS compatibility |

The complete initial Resource/owner/query/measurement/simulator, public operation and local operation types are selected in the wire registry. Product evaluators, database mappings, authorization and UI are not shared.

---

## 5. Required implementation work

<a id="rule-wp-03.00"></a>

### WP-03.00 — Create the split project structure


**What must be fully done.** Author the selected proto files and package dependencies from the fixed public/internal record and operation registry. Carry SPDX, source ownership and reserved field/enum numbers. Public packages cannot depend on internal packages; generate named product schemas without moving behavior into Contracts.

**Testing requirements.** Compile all schemas with the pinned compiler, validate imports/licence closure and generate both languages in a clean checkout.

**Completion gate.** Every selected schema/service has its assigned package and compiles without an untyped placeholder.

<a id="rule-wp-03.01"></a>

### WP-03.01 — Foundation contract types


**What must be fully done.** Implement generated wire identities plus domain-safe wrapper/conversion boundaries for IDs, revisions, sequences, cursors, exact decimals, semantic errors and content origin. Generate the complete selected Notes scalar/query and Scope measurement profiles and owner-body unions before persistence consumers.

**Testing requirements.** Independent positive/negative vectors cover exact integer/decimal, optional/oneof, invalid enum/ID, typed error and all three original audit profiles.

**Completion gate.** All selected records and their semantic constraints round-trip consistently in C# and TS.

<a id="rule-wp-03.02"></a>

### WP-03.02 — Serialization posture


**What must be fully done.** Use Google.Protobuf generated C# and protobuf-es generated TS with explicit service registration. Implement only the declared source-generated JSON metadata for HTTP exceptions; unknown fields, scalar presence and enum behavior follow the registry.

**Testing requirements.** AOT publish, forbidden reflection serializer/dependency checks, binary/JSON-exception conformance and decode limits.

**Completion gate.** No runtime schema discovery, dynamic business serializer or duplicate handwritten wire type is reachable.

<a id="rule-wp-03.03"></a>

### WP-03.03 — Capability and resource contract types


**What must be fully done.** Generate capability/action/context/resource/version/health and each owner-body record from the selected profile. ResourceRef remains an address; immutable bytes use ResourceVersionRef/BlobRef. Include the closed Sync mutation allowlist and immutable oversized-body reference form.

**Testing requirements.** Cross-owner/wrong-revision/opaque-object/forbidden-path negative vectors plus compatible unknown-response preservation.

**Completion gate.** Every shared descriptor/reference/body is actionable from the fixed schema without a consumer inventing its meaning.

<a id="rule-wp-03.04"></a>

### WP-03.04 — Local RPC contract discipline


**What must be fully done.** Generate local services, request/reply types, LocalBootstrap, lease and controlled transfer/read-chunk contracts. Map each selected method to the exact service descriptor and cancellation/deadline/error shape; runtime peer authentication belongs to WP08.

**Testing requirements.** Compile every local operation, descriptor-registration policy checks, wrong-oneof and malformed-transfer fixtures.

**Completion gate.** All local contracts needed by products have concrete generated signatures and explicit registration paths.

<a id="rule-wp-03.05"></a>

### WP-03.05 — C# export, TS generation and baseline gate


**What must be fully done.** Run network-free protoc/C#/TS generation from handwritten source, including public gRPC/gRPC-Web clients, the selected RN adapter package and HTTP-exception schemas. Export descriptor hashes and independent fixtures; publish immutable candidate NuGet/npm bundles before consumers. CI compares regeneration to committed baselines.

**Testing requirements.** Generator drift and public-to-internal leak negative fixtures; independent fresh-checkout package restore in C#, React and RN probes.

**Completion gate.** Released packages/descriptors/fixtures match the hand-authored source; no C#→OpenAPI business generation remains.

<a id="rule-wp-03.06"></a>

### WP-03.06 — Cross-language compatibility window


**What must be fully done.** Implement the registry compatibility and semantic hash profiles: wire bigint, decimal coefficient/scale, canonical semantic hash distinct from wire byte hash, oneof presence, unknown fields and additive response evolution. Version descriptors independently of applications and enforce the supported window.

**Testing requirements.** Previous-client/current-server and current-client/minimum-server matrices; deletion/tag-reuse/type-change failures; shared canonical hash vectors.

**Completion gate.** Breaking schema changes fail before publication and all selected values retain meaning across clients.

<a id="rule-wp-03.90"></a>
### WP-03.90 — Verify the owned artifact and real integration

**What must be fully done.** Create handwritten proto from the frozen first-version schema registry, public/internal package split, AI HTTP/event definitions and generated C#/TS artifacts. Publish profiles, independent fixtures and version metadata before consumers. Remove C# → OpenAPI as business wire authority.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Deterministic generation, compatibility/reserved-field checks, Apache closure and independent precise-value/error/profile vectors; both generated client ecosystems restore actual candidate artifacts.

**Completion gate.** Deterministic generation, compatibility/reserved-field checks, Apache closure and independent precise-value/error/profile vectors; both generated client ecosystems restore actual candidate artifacts. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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

**Required evidence addition.** Generated wire/schema vectors for origin, scalar queries and measurement results, including exact decimals/instants, statuses and unknown-field/version behavior. The contract suite checks all catalogue producer codes.

| Evidence | Produced by |
|---|---|
| Reference-direction and licence declaration reports | [WP-03.00](#rule-wp-03.00) |
| Round-trip results for every foundation and descriptor type | [WP-03.01](#rule-wp-03.01), [WP-03.03](#rule-wp-03.03) |
| Reflection-absence and generator-diagnostic reports | [WP-03.02](#rule-wp-03.02) |
| RPC contract policy test results | [WP-03.04](#rule-wp-03.04) |
| Determinism proof and negative baseline-diff test | [WP-03.05](#rule-wp-03.05) |
| Compatibility matrix results and the committed golden vectors | [WP-03.06](#rule-wp-03.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-03.90](#rule-wp-03.90) and all inherited domain-specific gates must pass on the same candidate closure. Deterministic generation, compatibility/reserved-field checks, Apache closure and independent precise-value/error/profile vectors; both generated client ecosystems restore actual candidate artifacts.

**[VG-04](../../assurance/open-gates-register.md#rule-vg-04) evidence:** [WP-03.04](#rule-wp-03.04) — Generated-shape policy for every real RPC interface; combine with the published-host RPC proof from package 06. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[F-026](../../assurance/open-gates-register.md#rule-f-026) evidence:** [WP-03.02](#rule-wp-03.02) — Generated-only client/version pin, reflection-package absence and build-breaking diagnostics; combine with the real AOT publish from package 06. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** All three profile baselines exist and round-trip before storage/product work starts; no placeholder field or later profile-selection task remains.

**All of the following, with recorded evidence:**

1. The contract projects are split by boundary and licence, with no public project referencing an internal one.
2. Foundation and descriptor types exist, round-trip, and make identifier confusion a compile error.
3. No reflection-based serialization path is reachable; all service and exception serializers use the selected generated metadata with AOT diagnostics treated as errors.
4. Every local RPC contract interface carries the generated service/descriptor identity, guarded by a policy test.
5. Contract artifact generation is deterministic and an undeclared change fails the build.
6. The compatibility matrix passes and the initial golden wire vectors are committed as immutable fixtures.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [02 build governance and analyzer policy](02-build-governance-and-analyzer-policy.md#rule-wp-02)

**Downstream — consumers of these released outputs.**

- [04 identity error and versioning primitives](04-identity-error-and-versioning-primitives.md#rule-wp-04)
- [05 architecture and repository policy tests](05-architecture-and-repository-policy-tests.md#rule-wp-05)
- [06 aot jit and wasm publish proof](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)
- [09 capability contribution and resource model](09-capability-contribution-and-resource-model.md#rule-wp-09)
- [21 cloud host and persistence](21-cloud-host-and-persistence.md#rule-wp-21)
- [23 public api and generated clients](23-public-api-and-generated-clients.md#rule-wp-23)
- [30 mobile shared architecture](30-mobile-shared-architecture.md#rule-wp-30)

---
