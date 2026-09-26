<a id="rule-wp-03"></a>

# WP-03 — Proto Contract Foundation and License Split

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Publish the handwritten proto authority and generated C#/TS public/internal package closure, exact-value fixtures and compatibility baselines before product/persistence consumers.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Contracts. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The contract project structure and its licence split; the source-generated serialization posture; the pipeline that generates protobuf descriptors, C#/TS DTOs/clients/validators and declared HTTP-exception schemas; the contract versioning mechanism; the baseline-diff gate; and the contract-authoring obligations that make the local RPC path AOT-correct.

**Out of scope.** Product behavior implementations; the complete selected initial wire records and operation signatures are already specified and generated here. The local IPC transport itself (`08`). The cloud endpoint implementations (`23`).

**Why this package exists.** **[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)** rejects a single ever-growing contracts assembly, and **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)** require that the entire Contracts repository be Apache-2.0 under [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) while product implementations keep their own licence. Both are structural decisions that are cheap now and extremely expensive after every product depends on the wrong shape.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers), [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile) and [scope.measurement.v1](../../requirements/products/arcscope.md#measurement-profile) are definitions, not decisions deferred to later product packages.

| Input | Why it matters |
|---|---|
| [`../../architecture/02-contracts-and-protocols.md`](../../architecture/02-contracts-and-protocols.md) | The two-layer contract model, compatibility rules and contract-authoring obligations [CA-01](../../architecture/02-contracts-and-protocols.md#rule-ca-01)–[CA-14](../../architecture/02-contracts-and-protocols.md#rule-ca-14) |
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) `§3` | The contract project split and licence enforcement rules |
| **[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)** | Contract granularity: split by boundary, ownership, cadence and licence |
| **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)** | All Contracts material is Apache-2.0 under [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010); public/internal import access remains separate |
| **[V-05b](../../assurance/phase-1-official-verification.md#rule-v-05b)** | Historical verification superseded by authored proto and explicit generated service registration under [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009)/010 |
| [WP-01.01](01-repository-reconciliation-and-target-layout.md#rule-wp-01.01) output | The type-by-type assignment to each licence boundary |
| [WP-02](02-build-governance-and-analyzer-policy.md#rule-wp-02) output | Generator settings, locked packages and the diagnostic posture |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) as amended by [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Handwritten proto is the business wire authority; C#/TS DTOs, validators and descriptors are generated** (**[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)**). Hand-edited generated DTOs or undeclared proto changes are defects. |
| <a id="rule-br-02"></a>BR-02 | **Contracts split by communication boundary, product/domain ownership, release cadence and licence boundary** (**[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)**). |
| <a id="rule-br-03"></a>BR-03 | **The Apache-2.0 set is exactly**: public protocol specifications, wire schemas, DTOs, public clients, contract-level validators, and the public SDK (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| <a id="rule-br-04"></a>BR-04 | **No Apache-boundary project references an AGPL project**, directly or transitively (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |
| <a id="rule-br-05"></a>BR-05 | C#/TS wire types derive from handwritten proto descriptors. Native code uses generated protobuf serializers; HTTP exceptions use explicit source-generated JSON metadata. No parallel handwritten business DTO or C#-exported wire authority. |
| <a id="rule-br-06"></a>BR-06 | **Every local RPC contract interface carries the generated service/descriptor identity with public instance methods included** (**[V-05b](../../assurance/phase-1-official-verification.md#rule-v-05b)**), asserted by a policy test. |
| <a id="rule-br-07"></a>BR-07 | **Base ViewModel patterns are never shared between desktop and mobile** (**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**) — the shared boundary is contracts and semantics, not UI patterns. |
| <a id="rule-br-08"></a>BR-08 | **Contract version and application version are separate axes** ([QI-04](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-04)), and a contract change without a version change fails the build. |
| <a id="rule-br-09"></a>BR-09 | **Contract-level validators express wire constraints only** (**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**), never business policy. |
| <a id="rule-br-10"></a>BR-10 | **Product-domain behaviour, server orchestration, policy decisions, persistence behaviour and entitlement authority stay outside the shared boundary** (**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |

---

## 4. Projects, directories, files and major types affected

All paths are in ArcForges-Contracts under the [selected package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry).

| Location | Deliverable |
|---|---|
| public/proto/, internal/proto/ | Handwritten initial schema/service/field/enum profiles from the wire registry; public versus internal Apache-2.0 import closure |
| public/http/, internal/ai-http/, fixtures/public/, fixtures/internal/ | Selected CF/auth/provider HTTP exceptions, independent canonical positive/negative vectors |
| ArcForges.Contracts.slnx; src/public/dotnet/, src/internal/dotnet/ | Retain the existing solution identity; actual source-bearing public/internal C# projects with generated outputs under their owned Generated directories |
| src/public/ts/{proto,api-client,contract-fixtures}/; src/internal/ts/{ai-internal,operator-client}/; src/public/kotlin/ | Preserve existing generated paths and package identities; generated DTOs, descriptors/clients and validators stay with their owning package and are never hand edited |
| src/transport/ | Apache Connect Kotlin binary gRPC-Web adapter and selected public C# transport composition only |
| eng/, artifacts/contracts/ | Pinned generation, descriptor/breaking-change baselines, signed versioned package manifests and candidate publication |
| tests/ | Schema closure, exact-value/unknown-field/conformance vectors and C#/TS compatibility |

The complete initial Resource/owner/query/measurement/simulator, public operation and local operation types are selected in the wire registry. Product evaluators, database mappings, authorization and UI are not shared.

---

## 5. Required implementation work

**Validation policy for every substep.** [P2-017](../../decisions/phase-2-specification-decisions.md#rule-p2-017) governs the execution of all gates below. Retain necessary Windows/Linux compilation, packaging, static checks, targeted offline schema/unit tests and non-duplicated security. Consumer restoration/compilation does not authorize installed-package execution in CI, public-byte polling or another post-merge test cycle. Product/runtime scenarios remain with their named owners and supported local environments; absent coverage is recorded, never inferred from schema or publication success.

<a id="rule-wp-03.00"></a>

### WP-03.00 — Create the split project structure

**What must be fully done.** Create public/local/internal/SDK/HTTP schema projects and exact package outputs from the producer matrix. All authored schemas/tools/fixtures are Apache-2.0; public imports cannot reach local/operator/internal protocols.

**Testing requirements.** Negative public→internal/GPL import fixture, package identity/SPDX and generated-header tests.

**Completion gate.** All package boundaries and generators exist with no implementation dependency.

The [WP03.00 implementation profile](../../assurance/wp03-00-contract-structure-profile.md) fixes the ordered implementation and publication prerequisites. A manifest of future projects or empty packages does not satisfy this gate. Each selected project has substantive schema-derived content or useful declared SDK/validator/CLI behavior; later substeps complete their assigned schema and semantic inventories.

<a id="rule-wp-03.01"></a>

### WP-03.01 — Foundation contract types


**What must be fully done.** Implement generated wire identities plus domain-safe wrapper/conversion boundaries for IDs, revisions, sequences, cursors, exact decimals, semantic errors and content origin. Generate the complete selected Notes scalar/query and Scope measurement profiles and owner-body unions before persistence consumers.

**Testing requirements.** Independent positive/negative vectors cover exact integer/decimal, optional/oneof, invalid enum/ID, typed error and all three original audit profiles.

**Completion gate.** All selected records and their semantic constraints round-trip consistently in C# and TS.

The [WP03.01 implementation profile](../../assurance/wp03-01-foundation-contract-profile.md) fixes the complete selected seed/dependency closure, safe value boundaries, profile fixtures and ordered implementation/publication plan. Its owner-body dependency generation does not close WP03.03's descriptor/resource/Sync semantic gate or WP03.05's complete operation, scope, stream/history and language-client gate. Query, measurement and transaction engines remain with their product owners.

The [WP03.01 completion receipt](../../assurance/wp03-01-implementation-evidence.md) records reviewed source, passing required checks, exact C#/TS conformance and complete normal publication. Substep 03.02 is complete; later-owner gates remain open.

<a id="rule-wp-03.02"></a>

### WP-03.02 — Serialization posture


**What must be fully done.** Use Google.Protobuf generated C# and protobuf-es generated TS with explicit service registration. Implement only the declared source-generated JSON metadata for HTTP exceptions; unknown fields, scalar presence and enum behavior follow the registry.

**Testing requirements.** AOT publish, forbidden reflection serializer/dependency checks, binary/JSON-exception conformance and decode limits.

**Completion gate.** No runtime schema discovery, dynamic business serializer or duplicate handwritten wire type is reachable.

The [WP03.02 implementation profile](../../assurance/wp03-02-serialization-posture-profile.md) fixes the decode limits, strict HTTP-exception JSON codecs, generated service catalogues, forbidden serializer/dependency gate, Native AOT probe and ordered implementation/publication plan. It contributes to, but does not close, [F-026](../../assurance/open-gates-register.md#rule-f-026); WP06.02 retains the real published generated-client AOT call.

The [WP03.02 completion receipt](../../assurance/wp03-02-implementation-evidence.md) records reviewed source, passing required checks, the Linux Native AOT probe, C#/TS vector conformance and complete normal publication. Substep 03.03 has not started.

<a id="rule-wp-03.03"></a>

### WP-03.03 — Capability and resource contract types


**What must be fully done.** Generate capability/action/context/resource/version/health and each owner-body record from the selected profile. ResourceRef remains an address; immutable bytes use ResourceVersionRef/BlobRef. Include the closed Sync mutation allowlist and immutable oversized-body reference form.

**Testing requirements.** Cross-owner/wrong-revision/opaque-object/forbidden-path negative vectors plus compatible unknown-response preservation.

**Completion gate.** Every shared descriptor/reference/body is actionable from the fixed schema without a consumer inventing its meaning.

<a id="rule-wp-03.04"></a>

### WP-03.04 — Private helper and in-process contract split

**What must be fully done.** Author the closed ContentSandbox/Extension/Connector and bootstrap/resource/event proto closure from annex 09. Product interfaces use generated records and static in-process adapters; reserve removed Hub/SSO/transfer names without registering services.

**Testing requirements.** Wrong child direction/role, removed methods, parent death and cross-product server registration fail; verify no public package imports internal schemas.

**Completion gate.** Published internal descriptors and transport fixtures expose only admitted child services.

<a id="rule-wp-03.05"></a>

### WP-03.05 — Complete generated package and schema gate

**What must be fully done.** Generate C#/TS/Kotlin-lite plus Connect Kotlin gRPC-Web packages from registry 04/annex 10, including native-auth HTTP exceptions, catalog operations and all transcript/output fields. Retire native-grpc-only contracts-client before the first business schema release. Export every method's eight authorization fields, scope, tags, risks, compatibility and exact source rule. Commit generated source and descriptor manifests.

**Testing requirements.** Independent exact-value/state/target/context/archive vectors in three languages; descriptor-tag collision/removal and operation-count checks; regeneration clean; consumers restore NuGet/npm/Maven from immutable candidate feeds.

**Completion gate.** Every active operation is classified and decodable; future names are reserved; all packages pass the applicable offline conformance, isolated restore/compilation and candidate packaging checks under P2-017. Publication completion uses original candidate identity and successful provider receipts; no installed-package consumer execution or routine public artifact download is required.

<a id="rule-wp-03.06"></a>

### WP-03.06 — Cross-language compatibility window


**What must be fully done.** Implement the registry compatibility and semantic hash profiles: wire bigint, decimal coefficient/scale, canonical semantic hash distinct from wire byte hash, oneof presence, unknown fields and additive response evolution. Version descriptors independently of applications and enforce the supported window.

**Testing requirements.** Previous-client/current-server and current-client/minimum-server matrices; deletion/tag-reuse/type-change failures; shared canonical hash vectors.

**Completion gate.** Breaking schema changes fail before publication and all selected values retain meaning across clients.

**Required implementation and closure from the final review.** Implement and independently verify [04-protobuf-wire-registry](../../architecture/contracts/04-protobuf-wire-registry.md). Generate every added account/provider, structural move, full Slate/ASR and encodedBody operation/record. Preserve field tags, exact ticks/integers and ModelId grammar. Independently decode >4 MiB Document/Timeline/Task bodies and reject wrong descriptor/hash/generation. Include all public/local methods in descriptor compatibility and the real-provider coverage map. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-03.07"></a>

### WP-03.07 — Signed catalog and update format producer

**What must be fully done.** Publish catalog-index.v1, catalog-revocations.v1, android-update.v1 and realm.v1 schemas, canonical signing vectors and separate fixture trust roots. Define malformed, expired, rollback and mixed-shard vectors under arch 15/deployment 22. Production keys are WP53 output, not an input here.

**Testing requirements.** Independent signature/hash verification, exact integer handling and expired/revoked/unknown-key refusal.

**Completion gate.** WP32/WP41 can implement complete consumers with deterministic fixture keys and named later production replacement.

<a id="rule-wp-03.90"></a>
### WP-03.90 — Verify the owned artifact and real integration

**What must be fully done.** Create handwritten proto from the frozen first-version schema registry, public/internal package split, private CF binding/event definitions and generated C#/TS/Kotlin artifacts. Publish profiles, independent fixtures and version metadata before consumers. Remove C# → OpenAPI as business wire authority.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Deterministic generation, compatibility/reserved-field checks, Apache closure and independent precise-value/error/profile vectors; all three generated client ecosystems restore actual candidate artifacts.

**Completion gate.** Deterministic generation, compatibility/reserved-field checks, Apache closure and independent precise-value/error/profile vectors; all three generated client ecosystems restore actual candidate artifacts. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

**Operator contract closure.** Consume [registry04 §9](../../architecture/contracts/04-protobuf-wire-registry.md#9-operator-control-and-separate-identity-boundary) and [model01 operator state](../../architecture/data-model/01-cloud-data-model.md#operator-proposal-approval-and-financial-owner-closure). Generate/implement every operation exactly once with its eight authorization fields, operator scope and [OC-03](../../requirements/10-distribution-update-and-support.md#rule-oc-03) role binding. Public customer/PAT/agent access refuses. Verify distinct approver, stale hash/revision/configuration, role revocation, expiry, concurrent consumption and lost receipt; no direct SQL or public-SDK operator import. WP03 produces schema/negative vectors, WP23 real identity/dispatch conformance, WP42 the financial owners, WP44 configuration/policy owners, and WP45 the real console join. Earlier packages retain their named fixture boundary until the existing downstream join.

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

State fixtures enumerate every numbered TaskState and TaskReasonFacet, including waiting with approval/device/capacity/dependency/reconciliation and non-waiting with none. An unknown future response facet renders an unknown reason while retaining authoritative TaskState and revision; it never grants authority or invents success. Unknown request facets refuse. Retained enum numbers remain fixed and descriptor compatibility prevents reuse of reserved values.

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-03.90](#rule-wp-03.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

[Local gRPC closure](../../architecture/contracts/09-local-grpc-and-sandbox.md): Publish complete .LocalRpc.Platform/.Sandbox and all typed parser/connector/hint/bootstrap methods before consumers. Descriptor fixture checks include every field in local 09 and wire 04.

Generate an operation-by-actor reachability matrix for every public/local/operator/CF/exception binding under catalogue 00 [AZ-04](../../architecture/contracts/00-operation-catalogue.md#rule-az-04), with all seven effective authorization fields and source profile. Fail unclassified/ambiguous fields, nonexistent idempotency examples, public imports of local schema and tool reachability of human-only approval/credential/commerce/policy methods. Include resource/context/connector egress denials and hostile actor-chain cases.

**Required evidence addition.** Generated wire/schema vectors for origin, scalar queries and measurement results, including exact decimals/instants, statuses and unknown-field/version behavior. The contract suite checks all catalogue producer codes.

| Evidence | Produced by |
|---|---|
| Reference-direction and licence declaration reports | [WP-03.00](#rule-wp-03.00) |
| Round-trip results for every foundation and descriptor type | [WP-03.01](#rule-wp-03.01), [WP-03.03](#rule-wp-03.03) |
| Reflection-absence and generator-diagnostic reports | [WP-03.02](#rule-wp-03.02) |
| RPC contract policy test results | [WP-03.04](#rule-wp-03.04) |
| Determinism, complete application-scope manifest, new stream/history records and negative baseline-diff test | [WP-03.05](#rule-wp-03.05) |
| Compatibility matrix results and the committed golden vectors | [WP-03.06](#rule-wp-03.06) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-03.90](#rule-wp-03.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-03.90](#rule-wp-03.90) and all inherited domain-specific gates must pass on the same candidate closure. Deterministic generation, compatibility/reserved-field checks, Apache closure and independent precise-value/error/profile vectors; all three generated client ecosystems restore actual candidate artifacts.

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

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [CON.02](../delivery/lanes/contracts.md#task-con-02) | [WP-03.03](03-contract-foundation-and-licence-split.md#rule-wp-03.03) (capability/action/context/version/health descriptor records only, plus EncodedBodyRef (the immutable oversized-body reference form); excludes the Sync mutation allowlist and cross-owner/wrong-revision/opaque-object/forbidden-path negative vectors, which are CON.03) | none |
| [CON.03](../delivery/lanes/contracts.md#task-con-03) | [WP-03.03](03-contract-foundation-and-licence-split.md#rule-wp-03.03) (the Sync mutation allowlist and oversized-body admission negative-vector half; ResourceRef/ResourceVersionRef/BlobRef schema itself is already done (CON.91/[WP-03.01](03-contract-foundation-and-licence-split.md#rule-wp-03.01))) | none |
| [CON.04](../delivery/lanes/contracts.md#task-con-04) | [WP-03.04](03-contract-foundation-and-licence-split.md#rule-wp-03.04) (ContentSandboxService only, from annex 09 §§2-6 (OpenSession/RenewSession/GrantSlot/AckBuffer/ProbeMedia/OpenMediaReader/ReadMediaFrame/SeekMedia/CopyVideoFrame/CopyAudioFrame/CloseFrame/CloseReader/OpenImage/GetImageInfo/ReadImageTile/CloseImage/OpenPdf/GetPdfPage/ExtractPdfText/RenderPdfTile/ClosePdf/ReadOtio/WriteOtio/OtioReadChunk/CancelSession/CloseSession = 24 methods))<br>[WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) §7 evidence: Local gRPC closure — complete.LocalRpc.Platform/.Sandbox typed parser/connector/hint/bootstrap methods before consumers (package-level obligation contribution) | none |
| [CON.05](../delivery/lanes/contracts.md#task-con-05) | [WP-03.04](03-contract-foundation-and-licence-split.md#rule-wp-03.04) (ExtensionHostService (remaining Handshake/Invoke/Stop; RenewLease already done), ILocalBootstrap (Challenge/Confirm/Renew), IConnectorBroker (ListDefinitions/ListConnections/BeginConnection/CompleteConnection/GetConnection/RevokeConnection); reserve removed Hub/SSO/transfer names (IHubRegistry/IHubRouting/DeviceSsoBrokerService) without registering them)<br>[WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) §7 evidence: Local gRPC closure — complete.LocalRpc.Platform/.Sandbox typed parser/connector/hint/bootstrap methods before consumers (package-level obligation contribution) | none |
| [CON.06](../delivery/lanes/contracts.md#task-con-06) | [WP-03.04](03-contract-foundation-and-licence-split.md#rule-wp-03.04) (the 'Product interfaces use generated records and static in-process adapters' half — full method surface for the four product-port packages plus ICapabilityProvider/IContextProvider/IArtifactHandler/IResourceAccess/IProductLifecycle/IDeepLinkTarget)<br>[WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (source KnowledgePolicy/Patch/View, typed one-use overrides, Notes run/atom/table-cell positions, complete initial owner/profile records) ([P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior: source KnowledgePolicy/Patch/View and typed one-use overrides (source.getPolicy/setPolicy/clearPolicy, source.createConsent/revokeConsent) fall inside IChatOperations/context-provider scope; stable Notes run/atom/table-cell positions (NotesTextPosition already exists in content.proto from WP03.01 — this task only needs to verify no gap remains for table-cell addressing); package-level obligation contribution) | none |
| [CON.07](../delivery/lanes/contracts.md#task-con-07) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (IdentityService (29 ops)/WorkspaceService (4)/DeviceService (6) from registry04 §5, plus contracts07 §1 native PKCE token endpoint and the four /session/v1 browser routes as declared JSON exceptions) | none |
| [CON.08](../delivery/lanes/contracts.md#task-con-08) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (EntitlementService (6 ops) + CommerceService (~14 ops) from registry04 §5, all declared 'frozen' compatibility class per catalogue00 [CC-04](../../architecture/04-desktop-application-architecture.md#rule-cc-04)) | none |
| [CON.09](../delivery/lanes/contracts.md#task-con-09) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (SyncService (~10 ops incl. listScopes/pullChanges/pushChange/pushBatch/getAggregate/listConflicts/resolveConflict/requestFullResync/getBootstrapPage), ResourceService transfer ops (beginUpload/completeUpload/getDownloadTicket/getMetadata/release/getUploadStatus/renewUploadTicket), TransferService (realm-transfer.v1: requestExport/previewImport/commitImport/get/list/cancel) from registry04 §5 and contracts07 §5) | none |
| [CON.10](../delivery/lanes/contracts.md#task-con-10) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (TaskService(~9)/ApprovalService(2)/BridgeService(3)/public ChatOperationsService(~25)/AgentService(3)/AutomationService(9)/search.query from registry04 §5, plus internal/ai-http/v1 schema.json (ai-internal npm/CloudInternal package) for the C#<->AI-Worker internal HTTP ports in contracts05 §3)<br>[WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure (source KnowledgePolicy/Patch/View, typed one-use overrides, Notes run/atom/table-cell positions, complete initial owner/profile records) (package-level obligation contribution) | none |
| [CON.11](../delivery/lanes/contracts.md#task-con-11) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (the annex10 13 new operations (ApplicationService.List/Heartbeat/Disconnect, HistoryService.BeginImport/FinalizeImport/GetImport/CancelImport, ExecutionService.StartTransientTurn/ReadOutput/WatchOutput/AcknowledgeOutput/PurgeTransient, EventService.Watch) plus EventService.Poll's 17 hint payloads ([CA-12](../../architecture/02-contracts-and-protocols.md#rule-ca-12)) and StreamFrame/OutputChunk/StreamPosition/StreamReset server-streaming framing)<br>[WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) Current application and stream contract completeness (annex10+manifest11, explicitly required before 03 completion) ('Current application and stream contract completeness' package-level obligation — explicitly required before 03 completion, not a.90-deferred item) | none |
| [CON.12](../delivery/lanes/contracts.md#task-con-12) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (extension/policy schemas named in [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) §4's projects table ('Selected CF/auth/provider HTTP exceptions') and contracts08 in full:.arcpkg manifest.v1, workflow.v1 DAG, panel.v1 declarative UI, PolicyBundle body.v1, internal ConfigurationDocument (20 sections)) | none |
| [CON.13](../delivery/lanes/contracts.md#task-con-13) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (the public CatalogService (search/getPackage/listVersions/registerPublisher/verifyPublisher/submitVersion/getSubmission, 7 ops) and PublisherView/CatalogPackageView/CatalogVersionView/CatalogSubmissionView/CatalogReviewDecision records from registry04 §4/§5) | none |
| [CON.14](../delivery/lanes/contracts.md#task-con-14) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (OperatorService's ~29 methods with all eight authorization fields and the [OC-03](../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role matrix)<br>[WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) 'Operator contract closure' package-level obligation — schema and negative vectors only; [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) owns real identity/dispatch, [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) financial owners, [WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44) config/policy owners, [WP-45](45-operations-support-and-trust-safety.md#rule-wp-45) the console join ('Operator contract closure' package-level obligation — schema and negative vectors only; [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) owns real identity/dispatch, [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) financial owners, [WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44) config/policy owners, [WP-45](45-operations-support-and-trust-safety.md#rule-wp-45) the console join; package-level obligation contribution) | none |
| [CON.15](../delivery/lanes/contracts.md#task-con-15) | [WP-03.90](03-contract-foundation-and-licence-split.md#rule-wp-03.90) ('Private CF binding/event definitions' input — the remaining contracts05 ports not already covered by CON.10 (ai-internal): /internal/objects/v1/* (authorize/part-receipt/verification/job-grant/job-authorize), /internal/ai/v1/dispatch/control/delete (Worker-side), inference-job family (embedding/rerank), and CfDeletionTarget/CfDeletionReceipt/SessionBinding/BackupManifest records) | none |
| [CON.16](../delivery/lanes/contracts.md#task-con-16) | [WP-03.07](03-contract-foundation-and-licence-split.md#rule-wp-03.07) (full — publish catalog-index.v1, catalog-revocations.v1, android-update.v1 and realm.v1 schemas, canonical signing vectors and separate fixture trust roots; production keys are explicitly [WP-53](53-desktop-distribution-and-update.md#rule-wp-53) output, not a [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) input) | none |
| [CON.17](../delivery/lanes/contracts.md#task-con-17) | [WP-03.06](03-contract-foundation-and-licence-split.md#rule-wp-03.06) (full — wire bigint/decimal-coefficient-scale/oneof-presence/unknown-field/additive-response-evolution profile; canonical semantic hash distinct from wire byte hash; independent versioning of descriptors from applications; supported-window enforcement (previous-client/current-server and current-client/minimum-server matrices); deletion/tag-reuse/type-change failure tests) | none |
| [CON.18](../delivery/lanes/contracts.md#task-con-18) | [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) §7 evidence: operation-by-actor reachability matrix ([AZ-04](../../architecture/08-security-architecture.md#rule-az-04)) for public/local/operator/CF/exception bindings (§7 evidence requirement: 'Generate an operation-by-actor reachability matrix for every public/local/operator/CF/exception binding under catalogue 00 [AZ-04](../../architecture/08-security-architecture.md#rule-az-04), with all seven effective authorization fields and source profile. Fail unclassified/ambiguous fields...'; package-level obligation contribution) | none |
| [CON.19](../delivery/lanes/contracts.md#task-con-19) | [WP-03.90](03-contract-foundation-and-licence-split.md#rule-wp-03.90) (all work except the parts mapped to CON.15)<br>[WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) §8 completion gate (6 items) + [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009)/[VG-04](../../assurance/open-gates-register.md#rule-vg-04)/[F-026](../../assurance/open-gates-register.md#rule-f-026) scoped gate contributions (§8 completion gate items 1-6 and the [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009)/[VG-04](../../assurance/open-gates-register.md#rule-vg-04)/[F-026](../../assurance/open-gates-register.md#rule-f-026) gate contributions; package-level obligation contribution) | [CON.01](../delivery/lanes/contracts.md#task-con-01) (artifact) |
| [CON.20](../delivery/lanes/contracts.md#task-con-20) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (notes.* operations (17), their records, eight authorization fields and vectors) | none |
| [CON.21](../delivery/lanes/contracts.md#task-con-21) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (simulation.* operations (12), their records, authorization fields and vectors) | none |
| [CON.22](../delivery/lanes/contracts.md#task-con-22) | [WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05) (support.*, notification.*, data.*, preference.*, policy.getBundle and export.* operations (15), records and vectors) | none |
| [CON.90](../delivery/lanes/contracts.md#task-con-90) | [WP-03.00](03-contract-foundation-and-licence-split.md#rule-wp-03.00) (full) | none |
| [CON.91](../delivery/lanes/contracts.md#task-con-91) | [WP-03.01](03-contract-foundation-and-licence-split.md#rule-wp-03.01) (full) | none |
| [CON.92](../delivery/lanes/contracts.md#task-con-92) | [WP-03.02](03-contract-foundation-and-licence-split.md#rule-wp-03.02) (full) | none |

**Consumers outside this package:** [AIR.00](../delivery/lanes/ai-routing.md#task-air-00), [AND.04](../delivery/lanes/android.md#task-and-04), [AND.05](../delivery/lanes/android.md#task-and-05), [AND.12](../delivery/lanes/android.md#task-and-12), [AND.20](../delivery/lanes/android.md#task-and-20), [APP.01](../delivery/lanes/app-composition.md#task-app-01), [AST.01](../delivery/lanes/assistant.md#task-ast-01), [AST.07](../delivery/lanes/assistant.md#task-ast-07), [AST.11](../delivery/lanes/assistant.md#task-ast-11), [AST.14](../delivery/lanes/assistant.md#task-ast-14), [CLOUD.01](../delivery/lanes/cloud.md#task-cloud-01), [CLOUD.20](../delivery/lanes/cloud.md#task-cloud-20), [CLOUD.21](../delivery/lanes/cloud.md#task-cloud-21), [CLOUD.23](../delivery/lanes/cloud.md#task-cloud-23), [CLOUD.29](../delivery/lanes/cloud.md#task-cloud-29), [CLOUD.37](../delivery/lanes/cloud.md#task-cloud-37), [CLOUD.45](../delivery/lanes/cloud.md#task-cloud-45), [COM.13](../delivery/lanes/commerce.md#task-com-13), [DEV.01](../delivery/lanes/device-bridge.md#task-dev-01), [DEV.02](../delivery/lanes/device-bridge.md#task-dev-02), [DEV.04](../delivery/lanes/device-bridge.md#task-dev-04), [EXT.02](../delivery/lanes/extensions.md#task-ext-02), [EXT.04](../delivery/lanes/extensions.md#task-ext-04), [EXT.06](../delivery/lanes/extensions.md#task-ext-06), [EXT.10](../delivery/lanes/extensions.md#task-ext-10), [FND.01](../delivery/lanes/foundation.md#task-fnd-01), [FND.02](../delivery/lanes/foundation.md#task-fnd-02), [FND.03](../delivery/lanes/foundation.md#task-fnd-03), [FND.05](../delivery/lanes/foundation.md#task-fnd-05), [FND.07](../delivery/lanes/foundation.md#task-fnd-07), [GOV.05](../delivery/lanes/governance.md#task-gov-05), [GOV.16](../delivery/lanes/governance.md#task-gov-16), [HAR.00](../delivery/lanes/harness.md#task-har-00), [HAR.01](../delivery/lanes/harness.md#task-har-01), [HAR.02](../delivery/lanes/harness.md#task-har-02), [NOTES.01](../delivery/lanes/arcnotes.md#task-notes-01), [NOTES.02](../delivery/lanes/arcnotes.md#task-notes-02), [NOTES.07](../delivery/lanes/arcnotes.md#task-notes-07), [NOTES.12](../delivery/lanes/arcnotes.md#task-notes-12), [NOTES.18](../delivery/lanes/arcnotes.md#task-notes-18), [NOTES.20](../delivery/lanes/arcnotes.md#task-notes-20), [NOTES.23](../delivery/lanes/arcnotes.md#task-notes-23), [NOTES.24](../delivery/lanes/arcnotes.md#task-notes-24), [OPS.05](../delivery/lanes/operations.md#task-ops-05), [OPS.07](../delivery/lanes/operations.md#task-ops-07), [OPS.10](../delivery/lanes/operations.md#task-ops-10), [OPS.11](../delivery/lanes/operations.md#task-ops-11), [OPS.13](../delivery/lanes/operations.md#task-ops-13), [PLT.09](../delivery/lanes/platform.md#task-plt-09), [PLT.15](../delivery/lanes/platform.md#task-plt-15), [PLT.17](../delivery/lanes/platform.md#task-plt-17), [PLT.19](../delivery/lanes/platform.md#task-plt-19), [PLT.45](../delivery/lanes/platform.md#task-plt-45), [POL.02](../delivery/lanes/policy.md#task-pol-02), [POL.05](../delivery/lanes/policy.md#task-pol-05), [POL.09](../delivery/lanes/policy.md#task-pol-09), [PRF.01](../delivery/lanes/runtime-proofs.md#task-prf-01), [PRF.02](../delivery/lanes/runtime-proofs.md#task-prf-02), [PRF.03](../delivery/lanes/runtime-proofs.md#task-prf-03), [PRF.04](../delivery/lanes/runtime-proofs.md#task-prf-04), [PRF.05](../delivery/lanes/runtime-proofs.md#task-prf-05), [PRF.07](../delivery/lanes/runtime-proofs.md#task-prf-07), [PRF.08](../delivery/lanes/runtime-proofs.md#task-prf-08), [PRF.10](../delivery/lanes/runtime-proofs.md#task-prf-10), [SCOPE.01](../delivery/lanes/arcscope.md#task-scope-01), [SCOPE.02](../delivery/lanes/arcscope.md#task-scope-02), [SCOPE.14](../delivery/lanes/arcscope.md#task-scope-14), [SCOPE.20](../delivery/lanes/arcscope.md#task-scope-20), [SIM.01](../delivery/lanes/simulator.md#task-sim-01), [SIM.05](../delivery/lanes/simulator.md#task-sim-05), [SIM.06](../delivery/lanes/simulator.md#task-sim-06), [SLATE.12](../delivery/lanes/arcslate.md#task-slate-12), [SLATE.37](../delivery/lanes/arcslate.md#task-slate-37), [SRCH.00](../delivery/lanes/search.md#task-srch-00), [SRCH.01](../delivery/lanes/search.md#task-srch-01), [UPD.07](../delivery/lanes/updater.md#task-upd-07), [WEB.10](../delivery/lanes/web.md#task-web-10), [WEB.14](../delivery/lanes/web.md#task-web-14), [WEB.15](../delivery/lanes/web.md#task-web-15).

<!-- delivery-graph:end -->

## [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure

Include source KnowledgePolicy/Patch/View, typed one-use overrides, stable Notes run/atom/table-cell positions and all complete initial owner/profile records. Descriptor fixtures and cross-language validation must enumerate them. The referenced normative profile and producer stage matrix are binding inputs. Record independent positive/negative vectors and actual owner integration at this WP's assigned stage; a mock cannot close a real-provider/device requirement.

## Current application and stream contract completeness

WP03.05 implements [annex 10](../../architecture/contracts/10-application-scope-and-streams.md) and the exhaustive [scope manifest11](../../architecture/contracts/11-operation-scope-manifest.md) together with the existing registry. Generate all appended fields, history-import archive records,13 new operations, EventService.Poll and operator bindings. Verify every operation has one current scope/transport class; reserved future Hub/DeviceSso methods are absent from active service registration and tool allowlists. Public connector management remains an application-scoped Cloud API, not helper IPC. C#/TS/Kotlin fixtures include binary unary/stream frames and scope/presence/unknown fields; clean consumers must use current published contracts-connect-client rather than the older native-grpc-only Android client. This is required before 03 completion, not a .90 design task.
