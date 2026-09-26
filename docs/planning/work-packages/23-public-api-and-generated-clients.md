<a id="rule-wp-23"></a>

# WP-23 — Public Proto APIs and Generated Clients

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Expose the cloud through one versioned public API generated from the handwritten proto source of truth, with typed clients that work identically from a Native AOT desktop binary, a Kotlin/Jetpack Compose mobile artifact and a React browser application — and a compatibility window that is tested rather than promised.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud + Contracts; all clients. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The public HTTP surface: endpoint mapping from the contract set, request validation, problem-detail responses, pagination, filtering, conditional requests, rate limiting, and the generated typed clients with their compatibility window and contract tests.

**Out of scope.** Realtime (`24`). The endpoints of modules that do not yet exist — each later module adds its own endpoints under the rules established here.

**Why this package exists.** The [public operation catalogue](../../architecture/contracts/01-public-api-operations.md) and [generated SDK contract](../../architecture/25-web-toolchain-and-sdk.md) define the interfaces clients implement. [the mock policy](../implementation-sequence.md#3-what-may-be-mocked-and-what-may-not) requires real protocol compatibility tests before fixture evidence is replaced by production integration.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile) and the [shared errors/cursors](../../architecture/contracts/00-operation-catalogue.md)

| Input | Why it matters |
|---|---|
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) `§6` | The public API surface rules |
| [`../../architecture/02-contracts-and-protocols.md`](../../architecture/02-contracts-and-protocols.md) `§11` | Compatibility rules and the supported window |
| **[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)** | Handwritten proto authority; generated C#/TS wire artifacts |
| **[F-026](../../assurance/open-gates-register.md#rule-f-026)** | Typed client entry point and reflection prohibition |
| [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-22](22-identity-workspace-and-device.md#rule-wp-22) output | The contract set and authenticated, tenancy-scoped requests |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) as amended by [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Endpoints are mapped from the contract set**, not hand-written in divergence from it (**[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)**). |
| <a id="rule-br-02"></a>BR-02 | **The generated document is produced by the build and diffed against a baseline** ([WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05)). |
| <a id="rule-br-03"></a>BR-03 | **C# clients use generated-only generated gRPC client with no reflection package; TypeScript uses the generated proto gRPC-Web SDK.** Both obey one public operation contract; their authentication adapters are language/surface-specific. |
| <a id="rule-br-04"></a>BR-04 | **Every error is a problem detail with a registered reason code.** No raw exception text is ever returned. |
| <a id="rule-br-05"></a>BR-05 | **The supported client window is declared and tested**, in both directions: an older client against the current server, and the current client against the minimum supported server. |
| <a id="rule-br-06"></a>BR-06 | **Requests are idempotent where they change state**, keyed by command identity. |
| <a id="rule-br-07"></a>BR-07 | **A response never leaks the existence of a resource the caller may not see** where existence itself is sensitive. |
| <a id="rule-br-08"></a>BR-08 | **Rate limits are per identity and per capability class**, and produce a typed, explained refusal with retry guidance. |
| <a id="rule-br-09"></a>BR-09 | **Object bodies go over standard HTTP upload and download, never over realtime**. |
| <a id="rule-br-10"></a>BR-10 | **Clients never choose arbitrary storage locations**; upload targets are issued by the server. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.PublicApi/` | Endpoint mapping, validation, problem-detail mapping, pagination, conditional requests, rate limiting |
| `src/Contracts/Public/ArcForges.Contracts.PublicApi.*/` | Extended per module as endpoints are added |
| `src/BuildingBlocks/ArcForges.CloudClient/` | The shared typed client factory, token handler and refresh serialisation |
| `artifacts/contracts/descriptors/` | The generated documents and their baselines |
| `fixtures/wire/publicapi/` | Golden request and response vectors per contract version |
| `tests/PublicApiContractTests/` | Generated client against a real server, plus the compatibility matrix |

**Major types introduced.** `EndpointRegistration`, `RequestValidator`, `ProblemDetail`, `PageRequest`, `PageResult`, `ConditionalRequest`, `RateLimitPolicy`, `UploadTicket`, `DownloadTicket`, `ApiClientFactory`.

---

## 5. Required implementation work

<a id="rule-wp-23.00"></a>

### WP-23.00 — Endpoint mapping and validation


**What must be fully done.** Register generated proto service methods with exact request/reply/semantic validation from the registry. Use binary gRPC-Web unary calls and declared server streams through the same owner handlers; register only the listed standard HTTP exceptions separately. Map owner mutations and Sync allowlist exactly.

**Testing requirements.** Exercise each method category through native and TS transport, malformed/unknown request values and denied scope before handler.

**Completion gate.** Every selected operation has a concrete typed endpoint and owner; no ad-hoc REST business API is introduced.

<a id="rule-wp-23.01"></a>

### WP-23.01 — Typed protocol and error mapping

**What must be fully done.** Map generated ArcResult domain errors and gRPC-Web transport statuses/trailers exactly under registry 04. ProblemDetails is limited to documented HTTP exceptions.

**Testing requirements.** HTTP200 with error trailers, partial frame, 64-bit values, deadline/cancel after dispatch and command receipt reconciliation.

**Completion gate.** Every C#/TS/Kotlin client distinguishes transport uncertainty from a domain refusal.

<a id="rule-wp-23.02"></a>

### WP-23.02 — Typed queries and revision preconditions

**What must be fully done.** Implement opaque scope-bound PageRequest cursors, registered typed filters and RequestMeta expected owner revision; no ETag/If-Match for business RPC. Standard HTTP byte/static exceptions retain their own conditional semantics.

**Testing requirements.** Wrong product/scope cursor, stale revision, page limits, unsupported filter/version and exact scalar vectors.

**Completion gate.** Generated clients exercise the authoritative RPC query/revision rules without REST aliases.

<a id="rule-wp-23.03"></a>

### WP-23.03 — Idempotency and rate limiting

**What must be fully done.** State-changing requests accept a command identity and produce exactly one effect under retry. Rate limits are applied per identity and per capability class, with typed refusals carrying retry guidance.

**Testing requirements.** Retry-produces-one-effect at the API boundary; rate-limit tests per class; a test asserting a limited response carries actionable guidance.

**Completion gate.** One command produces one effect at the API boundary, and rate limiting refuses with actionable guidance.

<a id="rule-wp-23.04"></a>

### WP-23.04 — Resource transport and future-owner boundary

**What must be fully done.** Register the complete generated upload/status/ticket/verification/owner-promotion schema and permission/error envelope; exercise it through declared protocol fixtures. The minimal actual R2 transport is already proved by WP06. Full Resource/Entitlement/sync owner tables, staged verification and real R2 multipart behavior are owned by WP25.

**Testing requirements.** Independent request/result/expiry/hash/denied-scope and encoded-body fixtures across C#/TS/Kotlin; release excludes fixture handlers. Record every endpoint's real owner/fixture/replacement WP.

**Completion gate.** No missing resource schema; no claim that WP23 alone delivered Resource/R2 owner behavior. WP25 actual integration is mandatory before resource-consuming products complete.

<a id="rule-wp-23.05"></a>

### WP-23.05 — Generated C#/TypeScript/Kotlin clients

**What must be fully done.** Consume released C# native, TypeScript gRPC-Web and Kotlin native clients against actual Identity/Workspace/Device endpoints. Supply native single-flight refresh, Web cookie/CSRF/Origin and generation-scoped callbacks outside generated code. Use WP06 Android probe, not the future complete app.

**Testing requirements.** Independent exact-value/current-previous-major vectors, actual 22 session expiry/revoke/refresh, public/internal leak rejection; future domain fixtures labeled and excluded from production.

**Completion gate.** Three ecosystem clients work against the actual host; owner implementations are replaced by 25/42/52 before full release.

<a id="rule-wp-23.06"></a>

### WP-23.06 — Compatibility window

**What must be fully done.** The supported client window is declared. Golden wire vectors exist per contract version. The compatibility matrix runs both directions: previous client against current server, current client against minimum supported server. A breaking change is detectable before release.

**Testing requirements.** The bidirectional matrix; a negative test asserting a breaking change fails the matrix.

**Completion gate.** The bidirectional compatibility matrix passes and a deliberately breaking change is caught by it.

---

**Required implementation and closure from the final review.** Implement and independently verify [04-protobuf-wire-registry](../../architecture/contracts/04-protobuf-wire-registry.md). Maintain complete operation→real producer/fixture→closing WP coverage. Prove real implemented Identity/session/transport behavior and descriptor compatibility for all future owners; do not claim all business handlers complete. Test encodedBody outcomes and recoveryGeneration in actual C#/TS/Kotlin framing, including revision/hash/auth failures. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-23.90"></a>
### WP-23.90 — Verify the owned artifact and real integration

**What must be fully done.** Implement each frozen public operation mapping as gRPC/gRPC-Web or its explicitly retained standard HTTP endpoint. Publish versioned clients and operation-specific validation/error adapters; no business DTO authority in Cloud.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Real C#/browser/Kotlin calls against the AOT image, previous/current compatibility and complete operation mapping, including auth, files and webhooks outside gRPC.

**Completion gate.** Real C#/browser/Kotlin calls against the AOT image, previous/current compatibility and complete operation mapping, including auth, files and webhooks outside gRPC. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

**Operator contract closure.** Consume [registry04 §9](../../architecture/contracts/04-protobuf-wire-registry.md#9-operator-control-and-separate-identity-boundary) and [model01 operator state](../../architecture/data-model/01-cloud-data-model.md#operator-proposal-approval-and-financial-owner-closure). Generate/implement every operation exactly once with its eight authorization fields, operator scope and [OC-03](../../requirements/10-distribution-update-and-support.md#rule-oc-03) role binding. Public customer/PAT/agent access refuses. Verify distinct approver, stale hash/revision/configuration, role revocation, expiry, concurrent consumption and lost receipt; no direct SQL or public-SDK operator import. WP03 produces schema/negative vectors, WP23 real identity/dispatch conformance, WP42 the financial owners, WP44 configuration/policy owners, and WP45 the real console join. Earlier packages retain their named fixture boundary until the existing downstream join.

**Browser matrix acceptance.** Use [browser-support.v1](../../requirements/12-quality-and-compatibility-contract.md#202-browser-supportv1) and the exact release artifact/OS/browser patches. For each output’s existing flows, verify supported/degraded/blocked browser behavior: delayed-stream polling where streaming exists, refusal of unavailable required authentication/step-up, safe-preview refusal and preserved pending work. Static site acceptance includes no-JavaScript readability; it does not invent interactive account/stream APIs. Operator step-up retains its separate Entra/MFA authority. WP23 proves generated transports; WP45/47/48/49 prove their respective operations/site/account/chat output; WP50 joins all four production hashes and real browser evidence. A Playwright WebKit run alone does not claim Safari/OS authenticator proof.

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Conditional requests and pagination constrain index design |
| Protocol | This package *is* the public protocol surface |
| UI | Clients become available to every surface |
| Security | Validation, rate limiting, ticket issuance and existence-leak prevention |
| Platform | Client behaviour verified on AOT desktop and production React browser |
| Migration | Contract versioning and the supported window |
| Compatibility | The golden vector corpus and the bidirectional matrix |

---

## 7. Tests and verification evidence

**Required evidence addition.** Real boundary error/cursor tests and generated C#/TS exact-value vectors; no runtime query engine is claimed from fixtures.

| Evidence | Produced by |
|---|---|
| Validation coverage and unreachable-handler assertion | [WP-23.00](#rule-wp-23.00) |
| Reason-code mapping exhaustiveness and leak test | [WP-23.01](#rule-wp-23.01) |
| Pagination stability and cursor-forging results | [WP-23.02](#rule-wp-23.02) |
| API-boundary idempotency and rate-limit results | [WP-23.03](#rule-wp-23.03) |
| Upload resumption, checksum and permission results | [WP-23.04](#rule-wp-23.04) |
| C# AOT and generated TS browser contract results | [WP-23.05](#rule-wp-23.05) |
| Bidirectional compatibility matrix and its negative test | [WP-23.06](#rule-wp-23.06) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-23.90](#rule-wp-23.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-23.90](#rule-wp-23.90) and all inherited domain-specific gates must pass on the same candidate closure. Real C#/browser/Kotlin calls against the AOT image, previous/current compatibility and complete operation mapping, including auth, files and webhooks outside gRPC.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-23.05](#rule-wp-23.05) — Generated C#/TS contracts and real-server exact-value/error/header/client conformance. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** Notes cursor/error semantics are implemented before the full query consumer; general cursor tests honor the operation-specific stable-or-restart guarantee.

**All of the following, with recorded evidence:**

1. Invalid requests never reach a handler; every validation failure carries a reason code.
2. Every registered reason code maps to a problem detail; no internal detail leaks in any response.
3. Pagination is stable under concurrent mutation; a forged cursor cannot escape scope.
4. One command produces one effect at the API boundary; rate limiting refuses with actionable guidance.
5. Generated upload schema/transport/authorization error fixtures pass here; WP25 proves actual resume, verification and ticket consumption against R2 with client-chosen storage locations refused.
6. Generated C# and TS clients pass the real-server, exact-value and compatibility matrix, with native reflection exclusion and browser cookie/CSRF semantics verified.
7. The bidirectional compatibility matrix passes and catches a deliberately breaking change.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [AND.07](../delivery/lanes/android.md#task-and-07) | [WP-23.05](23-public-api-and-generated-clients.md#rule-wp-23.05) (Android real-consumer integration beyond the [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) probe) | [AND.03](../delivery/lanes/android.md#task-and-03) (artifact), [AND.04](../delivery/lanes/android.md#task-and-04) (artifact), [AND.05](../delivery/lanes/android.md#task-and-05) (artifact), [AND.06](../delivery/lanes/android.md#task-and-06) (artifact), [CLOUD.13](../delivery/lanes/cloud.md#task-cloud-13) (artifact), [CLOUD.42](../delivery/lanes/cloud.md#task-cloud-42) (artifact), [CLOUD.39](../delivery/lanes/cloud.md#task-cloud-39) (artifact), [CLOUD.18](../delivery/lanes/cloud.md#task-cloud-18) (artifact), [CLOUD.19](../delivery/lanes/cloud.md#task-cloud-19) (artifact), [CLOUD.29](../delivery/lanes/cloud.md#task-cloud-29) (artifact) |
| [CLOUD.21](../delivery/lanes/cloud.md#task-cloud-21) | [WP-23.00](23-public-api-and-generated-clients.md#rule-wp-23.00) (full) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract), [CLOUD.13](../delivery/lanes/cloud.md#task-cloud-13) (artifact) |
| [CLOUD.22](../delivery/lanes/cloud.md#task-cloud-22) | [WP-23.01](23-public-api-and-generated-clients.md#rule-wp-23.01) (full) | none |
| [CLOUD.23](../delivery/lanes/cloud.md#task-cloud-23) | [WP-23.02](23-public-api-and-generated-clients.md#rule-wp-23.02) (full) | [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract) |
| [CLOUD.24](../delivery/lanes/cloud.md#task-cloud-24) | [WP-23.03](23-public-api-and-generated-clients.md#rule-wp-23.03) (full) | none |
| [CLOUD.25](../delivery/lanes/cloud.md#task-cloud-25) | [WP-23.04](23-public-api-and-generated-clients.md#rule-wp-23.04) (full (schema/transport/fixture boundary only; real R2 multipart behavior is [WP-25.05](25-sync-engine-and-blob-lifecycle.md#rule-wp-25.05))) | [PRF.07](../delivery/lanes/runtime-proofs.md#task-prf-07) (artifact) |
| [CLOUD.26](../delivery/lanes/cloud.md#task-cloud-26) | [WP-23.05](23-public-api-and-generated-clients.md#rule-wp-23.05) (all work except the parts mapped to AND.07, WEB.30) | [CLOUD.19](../delivery/lanes/cloud.md#task-cloud-19) (artifact), [PRF.10](../delivery/lanes/runtime-proofs.md#task-prf-10) (artifact) |
| [CLOUD.27](../delivery/lanes/cloud.md#task-cloud-27) | [WP-23.06](23-public-api-and-generated-clients.md#rule-wp-23.06) (full) | none |
| [CLOUD.28](../delivery/lanes/cloud.md#task-cloud-28) | [WP-23.90](23-public-api-and-generated-clients.md#rule-wp-23.90) (full)<br>[WP-23](23-public-api-and-generated-clients.md#rule-wp-23) Operator contract closure appendix -- Cloud's own share: generate/implement every operation with its eight authorization fields, operator scope and [OC-03](../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role binding, refuse public customer/PAT/agent access, verify distinct approver/stale hash/revision/configuration/role revocation/expiry/concurrent consumption/lost receipt; the financial owners ([WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42)), configuration/policy owners ([WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44)) and console join ([WP-45](45-operations-support-and-trust-safety.md#rule-wp-45)) are NOT this task's obligation -- see IM.operator-contract-closure (Operator contract closure appendix -- Cloud's own share: generate/implement every operation with its eight authorization fields, operator scope and [OC-03](../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role binding, refuse public customer/PAT/agent access, verify distinct approver/stale hash/revision/configuration/role revocation/expiry/concurrent consumption/lost receipt; the financial owners ([WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42)), configuration/policy owners ([WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44)) and console join ([WP-45](45-operations-support-and-trust-safety.md#rule-wp-45)) are NOT this task's obligation -- see IM.operator-contract-closure)<br>[WP-23](23-public-api-and-generated-clients.md#rule-wp-23) Browser matrix acceptance appendix -- Cloud's own share: prove generated transports support delayed-stream polling, refusal of unavailable required auth/step-up, safe-preview refusal, preserved pending work; [WP-45](45-operations-support-and-trust-safety.md#rule-wp-45)/47/48/49/50's own operations/site/account/chat/production-hash evidence is NOT this task's obligation -- see IM.browser-matrix-acceptance (Browser matrix acceptance appendix -- Cloud's own share: prove generated transports support delayed-stream polling, refusal of unavailable required auth/step-up, safe-preview refusal, preserved pending work; [WP-45](45-operations-support-and-trust-safety.md#rule-wp-45)/47/48/49/50's own operations/site/account/chat/production-hash evidence is NOT this task's obligation -- see IM.browser-matrix-acceptance)<br>[WP-23](23-public-api-and-generated-clients.md#rule-wp-23) Operator contract closure appendix (registry04 §9 + model01 operator state; eight authorization fields, operator scope, [OC-03](../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role binding) (package-level obligation contribution)<br>[WP-23](23-public-api-and-generated-clients.md#rule-wp-23) Browser matrix acceptance appendix (browser-support.v1, supported/degraded/blocked behavior for generated transports) (package-level obligation contribution) | none |
| [CLOUD.64](../delivery/lanes/cloud.md#task-cloud-64) | [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) Operator contract closure appendix, full cross-area join (Operator contract closure appendix, full cross-area join) | [COM.13](../delivery/lanes/commerce.md#task-com-13) (artifact), [POL.05](../delivery/lanes/policy.md#task-pol-05) (artifact), [OPS.05](../delivery/lanes/operations.md#task-ops-05) (artifact) |
| [WEB.30](../delivery/lanes/web.md#task-web-30) | [WP-23.05](23-public-api-and-generated-clients.md#rule-wp-23.05) (Web real-consumer integration) | [CLOUD.19](../delivery/lanes/cloud.md#task-cloud-19) (artifact), [CLOUD.29](../delivery/lanes/cloud.md#task-cloud-29) (artifact), [WEB.07](../delivery/lanes/web.md#task-web-07) (artifact), [WEB.14](../delivery/lanes/web.md#task-web-14) (artifact), [WEB.19](../delivery/lanes/web.md#task-web-19) (artifact), [PRF.08](../delivery/lanes/runtime-proofs.md#task-prf-08) (artifact) |
| [WEB.31](../delivery/lanes/web.md#task-web-31) | [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) Browser matrix acceptance appendix, full cross-area join (Browser matrix acceptance appendix, full cross-area join) | [OPS.05](../delivery/lanes/operations.md#task-ops-05) (artifact), [WEB.07](../delivery/lanes/web.md#task-web-07) (artifact), [WEB.14](../delivery/lanes/web.md#task-web-14) (artifact), [WEB.19](../delivery/lanes/web.md#task-web-19) (artifact) |

**Consumers outside this package:** [AND.04](../delivery/lanes/android.md#task-and-04), [AND.08](../delivery/lanes/android.md#task-and-08), [AND.09](../delivery/lanes/android.md#task-and-09), [AND.10](../delivery/lanes/android.md#task-and-10), [AND.11](../delivery/lanes/android.md#task-and-11), [AND.12](../delivery/lanes/android.md#task-and-12), [CLOUD.29](../delivery/lanes/cloud.md#task-cloud-29), [CLOUD.42](../delivery/lanes/cloud.md#task-cloud-42), [CLOUD.66](../delivery/lanes/cloud.md#task-cloud-66), [COM.03](../delivery/lanes/commerce.md#task-com-03), [COM.06](../delivery/lanes/commerce.md#task-com-06), [COM.13](../delivery/lanes/commerce.md#task-com-13), [REL.06](../delivery/lanes/release.md#task-rel-06), [SIM.05](../delivery/lanes/simulator.md#task-sim-05).

<!-- delivery-graph:end -->

