# WP-23 — Public API Surface and Generated Clients

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `03`, `22` · Downstream: `24`, `30`, `42`, `44`

> **Goal.** Expose the cloud through one versioned public API generated from the C# source of truth, with typed clients that work identically from a Native AOT desktop binary, a Mono AOT mobile binary and a WebAssembly application — and a compatibility window that is tested rather than promised.

---

## 1. Scope and purpose

**In scope.** The public HTTP surface: endpoint mapping from the contract set, request validation, problem-detail responses, pagination, filtering, conditional requests, rate limiting, and the generated typed clients with their compatibility window and contract tests.

**Out of scope.** Realtime (`24`). The endpoints of modules that do not yet exist — each later module adds its own endpoints under the rules established here.

**Why this package exists.** `I2 §IV` asks how far server interfaces should be designed now: far enough that clients can be written against them and mocks replaced without redesign. `I2 §V` requires real protocol compatibility tests early.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) `§6` | The public API surface rules |
| [`../../architecture/02-contracts-and-protocols.md`](../../architecture/02-contracts-and-protocols.md) `§11` | Compatibility rules and the supported window |
| **D-009** | C# as source of truth; generated wire artifacts |
| **F-026** | Typed client entry point and reflection prohibition |
| `WP-03`, `WP-22` output | The contract set and authenticated, tenancy-scoped requests |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Endpoints are mapped from the contract set**, not hand-written in divergence from it (**D-009**). |
| BR-02 | **The generated document is produced by the build and diffed against a baseline** (`WP-03.05`). |
| BR-03 | **Every client uses the generated-only entry point**; the reflection package is absent (**F-026**). |
| BR-04 | **Every error is a problem detail with a registered reason code.** No raw exception text is ever returned. |
| BR-05 | **The supported client window is declared and tested**, in both directions: an older client against the current server, and the current client against the minimum supported server. |
| BR-06 | **Requests are idempotent where they change state**, keyed by command identity. |
| BR-07 | **A response never leaks the existence of a resource the caller may not see** where existence itself is sensitive. |
| BR-08 | **Rate limits are per identity and per capability class**, and produce a typed, explained refusal with retry guidance. |
| BR-09 | **Object bodies go over standard HTTP upload and download, never over realtime** (`I3 §14.3`). |
| BR-10 | **Clients never choose arbitrary storage locations**; upload targets are issued by the server. |

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

### WP-23.00 — Endpoint mapping and validation

**What must be fully done.** Endpoints mapped from the contract set with request validation at the boundary. A request failing validation never reaches a handler. Validation messages are reason-coded and localisable, never raw.

**Testing requirements.** Per-endpoint validation tests; a test asserting no handler is reachable with an invalid request; a message-sourcing test.

**Completion gate.** Invalid requests never reach a handler, and every validation failure carries a reason code.

### WP-23.01 — Problem details and error mapping

**What must be fully done.** Every failure maps to a problem detail with a registered reason code, an HTTP status, and where applicable a retry indication. No exception text, stack trace or internal identifier is exposed.

**Testing requirements.** An exhaustive mapping test over the reason-code registry; a leak test asserting no internal detail appears in any response.

**Completion gate.** Every reason code maps to a problem detail, and no internal detail leaks in any response.

### WP-23.02 — Pagination, filtering and conditional requests

**What must be fully done.** Cursor-based pagination with stable ordering; filtering constrained to declared fields; conditional requests using revision so a client can avoid re-fetching unchanged state. A cursor is opaque and cannot be constructed by a client to escape scope.

**Testing requirements.** Pagination stability under concurrent mutation; a cursor-forging test; conditional-request correctness.

**Completion gate.** Pagination is stable under concurrent mutation and a forged cursor cannot escape scope.

### WP-23.03 — Idempotency and rate limiting

**What must be fully done.** State-changing requests accept a command identity and produce exactly one effect under retry. Rate limits are applied per identity and per capability class, with typed refusals carrying retry guidance.

**Testing requirements.** Retry-produces-one-effect at the API boundary; rate-limit tests per class; a test asserting a limited response carries actionable guidance.

**Completion gate.** One command produces one effect at the API boundary, and rate limiting refuses with actionable guidance.

### WP-23.04 — Object upload and download

**What must be fully done.** Upload through server-issued tickets with chunking, checksums, resumption and an idempotent completion commit. Download through server-issued tickets with permission checked both at issue and at consumption. Clients never choose storage locations.

**Testing requirements.** Interrupted upload resumption; checksum mismatch rejection; permission-at-consumption test; a negative test asserting a client-chosen location is refused.

**Completion gate.** Uploads resume and verify, permission is checked at both issue and consumption, and client-chosen locations are refused.

### WP-23.05 — Generated clients

**What must be fully done.** Typed clients generated from the contract set, sharing one factory with a token handler and serialised refresh. The clients work from a Native AOT desktop binary and a WebAssembly application, with the reflection package absent everywhere.

**Testing requirements.** Client tests from a published AOT binary and from the WebAssembly host; a dependency assertion for the reflection package; a refresh-storm test.

**Completion gate.** Generated clients work from published AOT and WebAssembly hosts with no reflection package present.

### WP-23.06 — Compatibility window

**What must be fully done.** The supported client window is declared. Golden wire vectors exist per contract version. The compatibility matrix runs both directions: previous client against current server, current client against minimum supported server. A breaking change is detectable before release.

**Testing requirements.** The bidirectional matrix; a negative test asserting a breaking change fails the matrix.

**Completion gate.** The bidirectional compatibility matrix passes and a deliberately breaking change is caught by it.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Conditional requests and pagination constrain index design |
| Protocol | This package *is* the public protocol surface |
| UI | Clients become available to every surface |
| Security | Validation, rate limiting, ticket issuance and existence-leak prevention |
| Platform | Client behaviour verified on AOT desktop and WebAssembly |
| Migration | Contract versioning and the supported window |
| Compatibility | The golden vector corpus and the bidirectional matrix |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Validation coverage and unreachable-handler assertion | `WP-23.00` |
| Reason-code mapping exhaustiveness and leak test | `WP-23.01` |
| Pagination stability and cursor-forging results | `WP-23.02` |
| API-boundary idempotency and rate-limit results | `WP-23.03` |
| Upload resumption, checksum and permission results | `WP-23.04` |
| AOT and WebAssembly client results with dependency assertion | `WP-23.05` |
| Bidirectional compatibility matrix and its negative test | `WP-23.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Invalid requests never reach a handler; every validation failure carries a reason code.
2. Every registered reason code maps to a problem detail; no internal detail leaks in any response.
3. Pagination is stable under concurrent mutation; a forged cursor cannot escape scope.
4. One command produces one effect at the API boundary; rate limiting refuses with actionable guidance.
5. Uploads resume and verify; permission is checked at ticket issue and at consumption; client-chosen storage locations are refused.
6. Generated clients work from a published Native AOT binary and a WebAssembly host with the reflection package absent.
7. The bidirectional compatibility matrix passes and catches a deliberately breaking change.

---

## 9. Dependencies

**Upstream.** `03` (contracts), `22` (authenticated, tenancy-scoped requests).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `24` — Realtime | The HTTP surface realtime backfills against |
| `25` — Sync | Upload, download and conditional requests |
| `30` — Mobile | The generated Apache-boundary clients |
| `42`, `44` | The endpoint conventions their modules follow |
| `48`, `49` — Web surfaces | The clients they consume |
