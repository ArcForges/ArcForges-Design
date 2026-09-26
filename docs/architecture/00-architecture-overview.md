# ArcForges Architecture Overview

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture — the entry point for every other architecture document
> Governing authority: `docs/decisions/phase-1-foundation-decisions.md`
> Companions: [`../requirements/00-product-scope-and-portfolio.md`](../requirements/00-product-scope-and-portfolio.md), [`../requirements/01-normative-glossary-and-invariants.md`](../requirements/01-normative-glossary-and-invariants.md)

This document fixes the shape of the system. Everything else in `docs/architecture/` elaborates one part of it and must not contradict it.

---

## 1. The controlling constraints

Five constraints determine almost every structural decision downstream.

| # | Constraint | Consequence |
|---|---|---|
| <a id="rule-ac-01"></a>AC-01 | **State has exactly one owner** | No shared writable business database; no central service holding product state; caches record source and revision and are never write points |
| <a id="rule-ac-02"></a>AC-02 | **Calls cross boundaries as strongly typed contracts** | No catch-all `Invoke(string, object)`; no dictionary payloads; no runtime-discovered interfaces on the AOT path |
| <a id="rule-ac-03"></a>AC-03 | Public business RPC uses handwritten proto and binary gRPC-Web for C#, TypeScript and Kotlin | Generated clients and one operation/error/stream vocabulary; only declared standard HTTP exceptions remain |
| <a id="rule-ac-04"></a>AC-04 | **Every production main path must be statically analysable where it is an AOT deliverable** | Source generation everywhere; no reflection fallback; no runtime code generation on the desktop main path |
| <a id="rule-ac-05"></a>AC-05 | **Failure is recoverable, and permission is validated at the final execution point** | Journals, revisions, idempotency, compensation — and owner-side re-authorization on every invocation |

**The most important constraint is not that all code lives in one repository.** It is that these five hold.

---

## 2. Runtime topology

```text
ArcNotes + own assistant/store ─┐
ArcScope + own assistant/store ─┤
ArcSlate + own assistant/store ─┼─ HTTPS gRPC-Web → Worker → C# Container
Android / Web companions ───────┘                           ↓
                                            D1 / DO / Queues / R2
                                            AI Workflow / Workers AI
Private parser/extension children: own parent ↔ gRPC Named Pipe/UDS
```

### 2.1 Three communication responsibilities, never conflated

| Path | Technology | Carries |
|---|---|---|
| **Private parent/child process boundary** | Authored proto + generated native gRPC over Named Pipe / UDS | Restricted parser/extension controls only; product handlers execute in process |
| **Public request/response** | ASP.NET Core gRPC-Web server; generated C#/TS/Connect Kotlin clients | Commands, queries, durable state, uploads and downloads |
| **Public realtime** | Generated Event/Execution server streams with unary Poll/ReadOutput recovery | Bounded hints and output; owner state remains durable |

**Prohibited:** public TCP listeners for local business IPC; authoritative mutations carried only by lossy hints; C++ pointers in RPC; bypassing the owner with direct database writes. Local Kestrel HTTP/2 over authenticated named pipes/UDS is the selected gRPC transport.

### 2.2 Four paths, four purposes

| Path | Route | Rule |
|---|---|---|
| **Application capability** | host registry → typed Application handler within that process | Owner-authorized; no product-to-product IPC or remote UI |
| **Cloud data** | Each product ↔ Cloud directly | **ArcChat is not a gateway** (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**) |
| **Remote agent** | Mobile/Web → Cloud → **durable `ToolRequest`** → the explicitly targeted owning application pulls, re-authorises, executes → idempotent `ToolResult` | **Cloud never connects to localhost, a pipe, a socket or local stdio** (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**) |
| **Own-app navigation** | Embedded assistant → its owner Application handler in process | Verified resource reference and open intent; cross-product collaboration is future-only |

---

## 3. Layering

Identical in every product and in Cloud:

```
Desktop / LocalRpc / Infrastructure / MinimalApi / Kotlin Android adapters
                              ↓
                       Application Services
                              ↓
                           Domain
```

| # | Rule |
|---|---|
| <a id="rule-ly-01"></a>LY-01 | **Domain references nothing** — not Application, not Infrastructure, not UI, not Contracts, not a database provider, not a transport library, not the file system, not a native handle. |
| <a id="rule-ly-02"></a>LY-02 | **Application depends only on Domain plus a small set of abstractions (ports).** |
| <a id="rule-ly-03"></a>LY-03 | **Infrastructure implements Application's ports.** |
| <a id="rule-ly-04"></a>LY-04 | **Adapters are entry points only.** A local RPC adapter performs local identity, validation, DTO mapping, cancellation propagation and an application-service call — nothing else. A Minimal API adapter performs authentication, authorization, HTTP semantics, JSON mapping and an application-service call — nothing else. |
| <a id="rule-ly-05"></a>LY-05 | **A realtime hub never mutates domain state directly.** When a write is required it calls the same application service, preserving command identity and revision semantics. |
| <a id="rule-ly-06"></a>LY-06 | **Local clicks, local RPC and public HTTP produce the same domain commands, the same revisions, the same journal entries and the same notifications.** This is [SI-04](../requirements/09-shared-desktop-experience.md#rule-si-04) in the shared desktop requirements, expressed structurally. |
| <a id="rule-ly-07"></a>LY-07 | **View models consume view state and call facades.** They hold no database connection, no session, no native pointer. |
| <a id="rule-ly-08"></a>LY-08 | **A transport DTO is never a domain entity, and a view model is never a transport DTO.** |
| <a id="rule-ly-09"></a>LY-09 | **A remote caller never drives another process's user interface.** Projection happens inside the owning process. |

---

## 4. Runtime and AOT matrix

Fixed by **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, evidenced by **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)** and **[V-05](../assurance/phase-1-official-verification.md#rule-v-05)**.

| Host | Mode | Notes |
|---|---|---|
| **ArcNotes / ArcScope / ArcSlate desktop** | **Native AOT** | Trim/AOT-safe dependency rules; real publish proof per RID per release |
| **ArcForges Cloud** | **ASP.NET Core Native AOT modular monolith** | Native AOT is mandatory; every dependency and real adapter participates in publish/run proof |
| **ArcChat Mobile — Android** | **Kotlin/Jetpack Compose** | Pinned Kotlin/Jetpack Compose and native modules; release artifact inspected and exercised on a real Android device |
| **ArcForges Web** | **React/TypeScript; Node.js/npm build tooling** | [browser-support.v1](../requirements/12-quality-and-compatibility-contract.md#202-browser-supportv1); static public pre-rendering; [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) |

| # | Rule |
|---|---|
| <a id="rule-ao-01"></a>AO-01 | **AOT release gates apply only to projects actually consumed by an AOT deliverable** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**). |
| <a id="rule-ao-02"></a>AO-02 | **Shared public contracts and client libraries consumed by desktop or mobile remain trim-safe and source-generation friendly**, regardless of who else consumes them. |
| <a id="rule-ao-03"></a>AO-03 | **The absence of an official AOT guarantee is never treated as proof of AOT compatibility** (**[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)**, **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**). Where documentation cannot prove a dependency's behaviour under an AOT deliverable, a real publish-and-test proof is a registered gate with an owner and trigger. |
| <a id="rule-ao-04"></a>AO-04 | Cloud publishes the complete selected Native AOT closure. CF Workflow executes TypeScript remotely; this does not create a C# JIT exemption. |

---

## 5. Product process model

| # | Rule |
|---|---|
| <a id="rule-pm-01"></a>PM-01 | **Each product instance is a complete, autonomous operating-system process.** "Single process" means the product plus its native libraries in one process — never all products merged into one. |
| <a id="rule-pm-02"></a>PM-02 | Each professional application hosts its own assistant window/service, SQLite store and Cloud connection through Platform packages. |
| <a id="rule-pm-03"></a>PM-03 | Capabilities, context, approvals and local tool execution are registered only inside the owning application. Cloud holds authorized application presence/remote queue state. |
| <a id="rule-pm-04"></a>PM-04 | Platform shares code and mechanisms, never a cross-product domain database, filesystem, undo stack or live singleton. |
| <a id="rule-pm-05"></a>PM-05 | A professional application starts/saves locally without Cloud; its own Cloud session/presence reconnects in the background. |
| <a id="rule-pm-06"></a>PM-06 | **Products never reference another product's Domain or Application assemblies.** Shared mechanisms come from Platform packages; current remote control targets one application. Cross-product collaboration is future-only. |
| <a id="rule-pm-07"></a>PM-07 | **Three identity axes exist and are distinct**: `AppId` (stable product identity), `InstallationId` (one installed copy on one device), `InstanceId` (one running process). `AppId == ProcessId` is prohibited. |

---

## 6. Shared foundation boundary

**Shared foundation provides mechanism. Products provide meaning and ownership.**

| Permitted in shared foundation | Prohibited in shared foundation |
|---|---|
| Stable identity primitives | Any product domain type |
| Result and error primitives | A global writable document store |
| `ResourceRef`, `ArtifactRef`, `TaskHandle` and other cross-domain stable values | A shared business database |
| Pagination, time and base enumerations | Business rules |
| Observability, cloud client infrastructure, security primitives, update integration, design system | A shared business view model |

Types such as `ArcForges.Foundation.Document`, `.VideoTimeline` or `.TelemetrySession` are prohibited. `ArcProductBase` domain hierarchies are prohibited. **Shared foundation must never become a fifth hidden product.**

---

## 7. Licence boundaries in the architecture

Two boundaries, enforced by build-time checks (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**).

```text
ArcNotes + own assistant/store ─┐
ArcScope + own assistant/store ─┤
ArcSlate + own assistant/store ─┼─ HTTPS gRPC-Web → Worker → C# Container
Android / Web companions ───────┘                           ↓
                                            D1 / DO / Queues / R2
                                            AI Workflow / Workers AI
Private parser/extension children: own parent ↔ gRPC Named Pipe/UDS
```

| # | Rule |
|---|---|
| <a id="rule-lb-01"></a>LB-01 | **AGPL components may consume the Apache-2.0 interoperability packages** without changing their own licence. |
| <a id="rule-lb-02"></a>LB-02 | **No GPL-family or AGPL-only source, project reference, package, generated artifact or transitive dependency may enter the ArcChat Mobile distributable** — enforced by architecture and dependency tests (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** obligation 7). |
| <a id="rule-lb-03"></a>LB-03 | **Base ViewModel patterns are not shared between Avalonia desktop and Kotlin Android mobile** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). Each UI stack owns its implementation. |
| <a id="rule-lb-04"></a>LB-04 | **Protocol communication across an explicit process or network boundary does not change a client's licence.** Desktop and server implementations remain separate works. |

---

## 8. Consistency model

| Scope | Guarantee |
|---|---|
| Commands within one document | Strongly consistent under a local transaction |
| Multiple documents in one product | Per-document transactions coordinated by an application-level saga |
| External/store boundary | Explicit outbox/saga, idempotency and visible recovery; same-store commands remain atomic |
| Public HTTP | A success response means the server completed or accepted the request as defined; long work returns a `TaskHandle` |
| Realtime | Visibility only, never the sole source of truth; gaps backfill by revision/sequence over HTTP |
| Cross-device | The sync protocol plus revisions; **synchronising a database file is prohibited** |
| Multi-step agent operations | Ordinary controlled capability calls; every failure observable, recoverable and subject to approval |

---

## 9. Write path

Every write — from a local click, a local RPC call, a public HTTP request or an agent invocation — follows one path:

```
1.  Verify identity, permission and capability version
2.  Check whether this CommandId has already been executed
       already executed -> RETURN THE PRIOR RESULT, do not re-execute
3.  Check ExpectedRevision
4.  Enforce domain rules
5.  ONE TRANSACTION, containing every participant and no I/O:
       state change
       command record
       journal entry (local) / change row (Cloud)
       revision increment
       outbox entry, where the write has an asynchronous effect
6.  COMMIT and flush
       <- THE DISPATCH BARRIER.  Nothing external has happened yet
7.  Publish the in-process notification, and only now begin any dispatch
8.  Return the new revision and the minimal delta
```

**Step 5 is a closed list, not an illustration.** Which participants may share one transaction is enumerated by operation class in `§6.1.1` of the data-model overview ([SU-01](data-model/00-data-model-overview.md#rule-su-01)–[SU-07](data-model/00-data-model-overview.md#rule-su-07)), using the deterministic guarded D1 batch statement order in [SU-04](data-model/00-data-model-overview.md#rule-su-04); `sync`, when enlisted for a synchronised write, is a participant and never an initiator ([SU-07](data-model/00-data-model-overview.md#rule-su-07)), which is why its row is inside the transaction rather than after it. **Step 6 is the dispatch barrier** (`§6.1.2`, [DB-01](data-model/00-data-model-overview.md#rule-db-01)–[DB-03](data-model/00-data-model-overview.md#rule-db-03)): no provider call, object-storage write or network hop occurs before it ([SU-05](data-model/00-data-model-overview.md#rule-su-05)). The local elaboration of the same path is `§3` of [the persistence architecture](06-data-persistence-and-formats.md). Those two are authoritative; this is the skeleton they share, and it is not a third specification.

Every write command carries at minimum `CommandId`, the target identity, `ExpectedRevision`, actor and device from the authentication context, causation and correlation identifiers, business parameters, and an optional approval reference.

**A revision mismatch never resolves as implicit last-write-wins.** It returns the current revision, a disclosure-safe conflict summary, whether automatic replay is possible, and a recommended action.

---

## 10. Architecture document map

| Document | Scope |
|---|---|
| [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md) | Repository layout, project boundaries, reference direction, licence boundaries, architecture tests |
| [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md) | Contract split (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**), the shared semantic model, versioning and compatibility |
| [`03-local-ipc-and-process-model.md`](03-local-ipc-and-process-model.md) | gRPC, transports, private helper registration, authentication and routing, health, backpressure |
| [`04-desktop-application-architecture.md`](04-desktop-application-architecture.md) | Avalonia host, MVVM, threading, multi-window, AOT constraints, lifecycle |
| [`05-cloud-architecture.md`](05-cloud-architecture.md) | Native AOT modular business host, module boundaries, host pipeline, persistence, outbox, realtime, background work |
| [`06-data-persistence-and-formats.md`](06-data-persistence-and-formats.md) | Local stores, journals and snapshots, native formats, migration mechanics |
| [`07-sync-conflict-and-backup.md`](07-sync-conflict-and-backup.md) | Sync protocol, change feed, conflict policies, tombstones, blob lifecycle, backup topology |
| [`08-security-architecture.md`](08-security-architecture.md) | Identity layering, authorization enforcement points, secret handling, egress, audit |
| [`09-ai-and-agent-runtime-architecture.md`](09-ai-and-agent-runtime-architecture.md) | Agent runtime, capability registry, task engine, provider routing, credit metering |
| [`10-web-architecture.md`](10-web-architecture.md) | Static generation, React/TypeScript application, per-surface deployment and security |
| [`11-mobile-architecture.md`](11-mobile-architecture.md) | Kotlin Android structure, Apache boundary, offline outbox, push, secure storage |
| [`12-native-interop-and-media.md`](12-native-interop-and-media.md) | P/Invoke discipline, the C ABI, SafeHandle, media and acquisition pipelines |
| [`13-observability-and-operations.md`](13-observability-and-operations.md) | Telemetry, correlation, health, incident tooling, operator surface |
| [`14-build-packaging-and-release.md`](14-build-packaging-and-release.md) | Build governance, versioning axes, packaging, signing, update feed, CI gates |
| [`15-extension-platform-architecture.md`](15-extension-platform-architecture.md) | Extension host, protocol, schema model, package runtime, catalog |
| [`16-billing-and-commerce-architecture.md`](16-billing-and-commerce-architecture.md) | Provider adapter, event inbox, entitlement resolver, ledgers, reconciliation |

---

## 11. Architecture review checklist

Answerable before any feature merges:

**Products and state** — Is the authoritative owner explicit? Are reusable assistant state and professional domain state separated within each application? Do local editing, saved history and recovery work offline? Does each remote action keep its frozen application target and reconcile unknown effects?

**Layering** — Do local UI, local RPC and public HTTP all reach the same application service? Do adapters avoid referencing view models and controls entirely? Is Domain free of UI, database, transport and native dependencies? Are DTOs, domain models and view state kept unmixed?

**Local RPC** — Is every operation in the pinned handwritten proto set with generated messages/services/clients and explicit listener registration? Do Named Pipe/UDS peer bootstrap and reverse callbacks work in the actual AOT artifact? Are limits, cancellation, command identity, correct revision kind and previous-client compatibility verified without runtime discovery or proxy fallback?

**Public RPC** — Are C#/TS/Kotlin package clients using binary gRPC-Web and matching descriptors/metadata? Do trailers, 64-bit values, scope, cancellation and output recovery agree? HTTP exceptions remain explicitly named.

**Realtime** — Used only for realtime need, never as the sole durable fact? C# and TS payloads generated from the same authored contract? Recoverable through HTTP by revision or sequence after a disconnect?

**IPC and security** — Are pipe and socket permissions minimised? Are instance, session and actor verified? Does the owner perform final authorization? Are fixed public ports and arbitrary-path loading avoided?

**Native interop** — Is a native library genuinely required? Does it cross a stable C ABI through source-generated P/Invoke? `SafeHandle` with explicit ownership? Are native exceptions contained inside the ABI? Are fuzz, sanitizer, ABI and crash-recovery tests present? Has no new long-lived C++ worker been added?

**UI and tasks** — Does the UI thread do only lightweight work? Is every queue bounded and back-pressured? Does long work return a `TaskHandle`? Is the task queryable, recoverable and cancellable — or explicitly non-cancellable?

**AOT and publishing** — Does the host genuinely publish AOT where applicable? Are there no unreviewed trimming or AOT warnings? Does Android use the pinned Kotlin/Jetpack Compose release artifact? Are native and managed shipped as one version set? Are updates, rollbacks, schema and document formats compatible? Are signing, SBOM, dependency and secret scans present?

---

## 12. Principal risks and their mitigations

| Risk | Mitigation |
|---|---|
| Local gRPC AOT closure | Pin generated descriptors/parsers/clients, explicitly register services and verify real Named Pipe/UDS calls and reverse callbacks in published AOT artifacts. Dynamic discovery and proxy fallback are prohibited. |
| Bidirectional RPC produces concurrency or deadlock misjudgement | The transport is not an actor: serialize domain writes per document; never hold a lock while awaiting a callback; base writes on revision and command identity; fault-inject bidirectional callbacks and disconnects |
| Typed HTTP client silently falls back to reflection | Generated-only API, reflection package absent from production, analyzer diagnostics escalated to errors, an AOT publish contract test per public method |
| Realtime misused as a reliable bus | Realtime is the visibility layer; business facts land in the database, journal and outbox; clients recover by revision or sequence over HTTP |
| Android strict AOT misrepresented | Documentation and inspected artifact state Kotlin/Jetpack Compose; server Native AOT is a separate target |
| ORM blocks strict AOT on a desktop deliverable | Desktop persistence uses an AOT-safe access path; a heavyweight ORM runtime is not a hard dependency of an AOT host |
| In-process native library crash | Narrow C ABI, `SafeHandle`, input validation, fuzzing and sanitizers, sacrificial-process tests, crash dumps, journal recovery |
| Over-sharing produces a giant monolith | A shared language is not a shared model: split contracts by boundary and ownership, enforce module ownership, ban cross-product infrastructure references |
| Breaking renames under interface-first RPC | Contract versioning rules, V1/V2 coexistence, an old-client matrix, and API diffs |
| Platform becomes a universal business database | Assistant packages own reusable assistant state only; professional tables/documents/undo belong to the product. Package reference and schema ownership tests enforce this boundary |
| An agent bypasses permission | Agents call only ordinary typed capabilities; the owner performs final authorization; high-risk approvals bind a parameter digest; auditing is end to end |
| Premature microservices and messaging infrastructure | Cloud starts as a modular monolith; splitting requires demonstrated need; no distributed messaging on the local machine |

---

## 13. Traceability

| Current document | Relationship |
|---|---|
| [ArcForges Product Scope and Portfolio](../requirements/00-product-scope-and-portfolio.md) | Owns the portfolio, ownership, topology and technical boundaries |
| [ArcForges Normative Glossary and Invariant Catalogue](../requirements/01-normative-glossary-and-invariants.md) | Owns canonical terms and invariant definitions |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** | Two-boundary licensing enforced structurally |
| **[D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007)** | Web rendering boundary |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | The runtime and AOT matrix, including Cloud as Native AOT under [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) |
| **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** | Contract granularity |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Cloud topology and the durable local-action model |
| **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** | The implementation nine-repository target under [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) |
| **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)**, **[V-05](../assurance/phase-1-official-verification.md#rule-v-05)** | The AOT evidence underpinning the matrix |

## Retired runtime concepts

Standalone ArcChat desktop, cross-product Hub/discovery/SSO/handoff/federation, public native-gRPC clients, OpenAPI business generation, SignalR, public AI WebSockets, MAUI/RN Mobile, PostgreSQL business storage and a monorepo build are historical baselines superseded by [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009)…[P2-013](../decisions/phase-2-specification-decisions.md#rule-p2-013). Current professional hosts embed Platform assistant packages, retain separate history/session/database state and communicate directly with Cloud. Private helper gRPC and standardized external MCP/device protocols remain explicit different boundaries. Historical decision/review text is provenance, not an active work package.
