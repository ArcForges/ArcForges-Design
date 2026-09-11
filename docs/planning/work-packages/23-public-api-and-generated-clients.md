<a id="rule-wp-23"></a>

# WP-23 — Public Proto APIs and Generated Clients

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `03`, `22` · Downstream: `24`, `30`, `42`, `44`, `51`, `52`

> **Goal.** Expose the cloud through one versioned public API generated from the handwritten proto source of truth, with typed clients that work identically from a Native AOT desktop binary, a RN/Hermes mobile artifact and a React browser application — and a compatibility window that is tested rather than promised.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud + Contracts; all clients. Inputs: the assigned exact Contracts packages/descriptors and actual provider artifacts; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The public HTTP surface: endpoint mapping from the contract set, request validation, problem-detail responses, pagination, filtering, conditional requests, rate limiting, and the generated typed clients with their compatibility window and contract tests.

**Out of scope.** Realtime (`24`). The endpoints of modules that do not yet exist — each later module adds its own endpoints under the rules established here.

**Why this package exists.** The [public operation catalogue](../../architecture/contracts/01-public-api-operations.md) and [generated SDK contract](../../architecture/25-web-toolchain-and-sdk.md) define the interfaces clients implement. [the mock policy](../implementation-sequence.md#3-what-may-be-mocked-and-what-may-not) requires real protocol compatibility tests before fixture evidence is replaced by production integration.

---

## 2. Required inputs and dependencies

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

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Endpoints are mapped from the contract set**, not hand-written in divergence from it (**[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)**). |
| BR-02 | **The generated document is produced by the build and diffed against a baseline** ([WP-03.05](03-contract-foundation-and-licence-split.md#rule-wp-03.05)). |
| BR-03 | **C# clients use generated-only generated gRPC client with no reflection package; TypeScript uses the generated proto gRPC-Web SDK.** Both obey one public operation contract; their authentication adapters are language/surface-specific. |
| BR-04 | **Every error is a problem detail with a registered reason code.** No raw exception text is ever returned. |
| BR-05 | **The supported client window is declared and tested**, in both directions: an older client against the current server, and the current client against the minimum supported server. |
| BR-06 | **Requests are idempotent where they change state**, keyed by command identity. |
| BR-07 | **A response never leaks the existence of a resource the caller may not see** where existence itself is sensitive. |
| BR-08 | **Rate limits are per identity and per capability class**, and produce a typed, explained refusal with retry guidance. |
| BR-09 | **Object bodies go over standard HTTP upload and download, never over realtime**. |
| <a id="rule-br-10"></a>BR-10 | **Clients never choose arbitrary storage locations**; upload targets are issued by the server. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.PublicApi/` | Endpoint mapping, validation, problem-detail mapping, pagination, conditional requests, rate limiting |
| `src/Contracts/Public/ArcForges.Contracts.PublicApi.*/` | Extended per module as endpoints are added |
| `src/BuildingBlocks/ArcForges.CloudClient/` | The shared typed client factory, token handler and refresh serialisation |
| `artifacts/contracts/openapi/` | The generated documents and their baselines |
| `fixtures/wire/publicapi/` | Golden request and response vectors per contract version |
| `tests/PublicApiContractTests/` | Generated client against a real server, plus the compatibility matrix |

**Major types introduced.** `EndpointRegistration`, `RequestValidator`, `ProblemDetail`, `PageRequest`, `PageResult`, `ConditionalRequest`, `RateLimitPolicy`, `UploadTicket`, `DownloadTicket`, `ApiClientFactory`.

---

## 5. Required implementation work

<a id="rule-wp-23.00"></a>

### WP-23.00 — Endpoint mapping and validation


**What must be fully done.** Register generated proto service methods with exact request/reply/semantic validation from the registry. Use native gRPC and unary gRPC-Web through the same owner handlers; register only the listed standard HTTP exceptions separately. Map owner mutations and Sync allowlist exactly.

**Testing requirements.** Exercise each method category through native and TS transport, malformed/unknown request values and denied scope before handler.

**Completion gate.** Every selected operation has a concrete typed endpoint and owner; no ad-hoc REST business API is introduced.

<a id="rule-wp-23.01"></a>

### WP-23.01 — Problem details and error mapping


**What must be fully done.** Implement the selected transport status/domain ProblemDetail mapping, reason categories, retry guidance and effect certainty. gRPC trailers carry status/details; HTTP exceptions use the declared HTTP status/schema. Never treat an unknown post-dispatch outcome as safe-to-retry transport failure.

**Testing requirements.** Common native/browser/RN error vectors including malformed trailers, cancellation, unknown enum and correlation; secret/internal detail redaction.

**Completion gate.** Error/recovery meaning is identical across the declared transports.

<a id="rule-wp-23.02"></a>

### WP-23.02 — Pagination, filtering and conditional requests


**What must be fully done.** Implement the fixed page/sort/filter/cursor and expected-revision contracts per operation. Scope all cursors, apply selected Notes query and general Search variants, enforce limits and return typed reset/conflict where needed.

**Testing requirements.** Stable order/page replay, current permission changes, wrong scope/revision and page-limit cases.

**Completion gate.** Reads and conditional writes use the predesigned profiles without consumer-defined query languages.

<a id="rule-wp-23.03"></a>

### WP-23.03 — Idempotency and rate limiting

**What must be fully done.** State-changing requests accept a command identity and produce exactly one effect under retry. Rate limits are applied per identity and per capability class, with typed refusals carrying retry guidance.

**Testing requirements.** Retry-produces-one-effect at the API boundary; rate-limit tests per class; a test asserting a limited response carries actionable guidance.

**Completion gate.** One command produces one effect at the API boundary, and rate limiting refuses with actionable guidance.

<a id="rule-wp-23.04"></a>

### WP-23.04 — Reserved, verified and promoted objects


**What must be fully done.** Implement C# upload admission/status/ticket-renew/complete owner operations and real CF staged multipart verification from the object contract. Reserve committed/staging quotas before bytes, verify immutable whole hash/type, pin Verified state, then publish in the owning transaction. Enforce authenticated download/range and cleanup receipts before releasing exposure.

**Testing requirements.** Real R2 multipart/retry/status/expiry/permission/deletion checks, verifier restart and largest-admitted-object capacity proof; quota and owner-commit crash points.

**Completion gate.** No Verified object is visible as Published early, no raw permanent R2 URL is public, and quota/references/deletion converge.

<a id="rule-wp-23.05"></a>

### WP-23.05 — Generated C# and TypeScript clients


**What must be fully done.** Consume released Contracts C# native clients and TS React/RN clients against these actual endpoints. Compose opaque bearer and single-flight refresh for native/RN, browser opaque cookie plus CSRF/Origin, cancellation/backoff and generation-scoped callbacks outside generated code.

**Testing requirements.** Exact-value and current/previous contract matrix from AOT desktop, production React and physical RN release; concurrent refresh/session revoke.

**Completion gate.** All actual consumer runtimes use the selected public protocol and authentication without handwritten wire authority.

<a id="rule-wp-23.06"></a>

### WP-23.06 — Compatibility window

**What must be fully done.** The supported client window is declared. Golden wire vectors exist per contract version. The compatibility matrix runs both directions: previous client against current server, current client against minimum supported server. A breaking change is detectable before release.

**Testing requirements.** The bidirectional matrix; a negative test asserting a breaking change fails the matrix.

**Completion gate.** The bidirectional compatibility matrix passes and a deliberately breaking change is caught by it.

---

<a id="rule-wp-23.90"></a>
### WP-23.90 — Verify the owned artifact and real integration

**What must be fully done.** Implement each frozen public operation mapping as gRPC/gRPC-Web or its explicitly retained standard HTTP endpoint. Publish versioned clients and operation-specific validation/error adapters; no business DTO authority in Cloud.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Real C#/browser/RN calls against the AOT image, previous/current compatibility and complete operation mapping, including auth, files and webhooks outside gRPC.

**Completion gate.** Real C#/browser/RN calls against the AOT image, previous/current compatibility and complete operation mapping, including auth, files and webhooks outside gRPC. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

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

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-23.90](#rule-wp-23.90) and all inherited domain-specific gates must pass on the same candidate closure. Real C#/browser/RN calls against the AOT image, previous/current compatibility and complete operation mapping, including auth, files and webhooks outside gRPC.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-23.05](#rule-wp-23.05) — Generated C#/TS contracts and real-server exact-value/error/header/client conformance. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Additional completion requirement.** Notes cursor/error semantics are implemented before the full query consumer; general cursor tests honor the operation-specific stable-or-restart guarantee.

**All of the following, with recorded evidence:**

1. Invalid requests never reach a handler; every validation failure carries a reason code.
2. Every registered reason code maps to a problem detail; no internal detail leaks in any response.
3. Pagination is stable under concurrent mutation; a forged cursor cannot escape scope.
4. One command produces one effect at the API boundary; rate limiting refuses with actionable guidance.
5. Uploads resume and verify; permission is checked at ticket issue and at consumption; client-chosen storage locations are refused.
6. Generated C# and TS clients pass the real-server, exact-value and compatibility matrix, with native reflection exclusion and browser cookie/CSRF semantics verified.
7. The bidirectional compatibility matrix passes and catches a deliberately breaking change.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [03 contract foundation and licence split](03-contract-foundation-and-licence-split.md#rule-wp-03)
- [22 identity workspace and device](22-identity-workspace-and-device.md#rule-wp-22)

**Downstream — consumers of these released outputs.**

- [24 realtime and reliable events](24-realtime-and-reliable-events.md#rule-wp-24)
- [30 mobile shared architecture](30-mobile-shared-architecture.md#rule-wp-30)
- [42 commerce entitlement and credits](42-commerce-entitlement-and-credits.md#rule-wp-42)
- [44 dynamic policy and configuration](44-dynamic-policy-and-configuration.md#rule-wp-44)
- [51 arcscope cloud simulator](51-arcscope-cloud-simulator.md#rule-wp-51)
- [52 cloud harness](52-cloud-harness.md#rule-wp-52)

---
