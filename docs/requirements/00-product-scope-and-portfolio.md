# ArcForges Product Scope and Portfolio

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: `docs/decisions/phase-1-foundation-decisions.md` (D-001 … D-023)
> Companions: [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md), [`../architecture/00-architecture-overview.md`](../architecture/00-architecture-overview.md)

This document defines what ArcForges is, what it contains, what it deliberately does not contain, and the product-level boundaries that every other requirement, architecture and work-package document must respect.

Nothing in this document reopens a Phase 1 decision. Where a Phase 1 decision governs a statement, the decision is cited inline as `D-nnn`.

---

## 1. Product statement

ArcForges is a **completely open-source, local-first, AI-native professional desktop software ecosystem**, with an optional paid managed cloud and metered managed AI.

Three commercial layers, strictly separated:

| Layer | Contents | Commercial posture |
|---|---|---|
| **Local products** | The four desktop applications and every local capability they provide | Free forever, open source |
| **ArcForges Cloud** | Official managed sync, storage, cross-device continuity, remote agent, cloud search, cloud knowledge index, notifications | Paid subscription; self-hosting is a supported free alternative |
| **Arc AI** | Managed AI inference purchased through ArcForges | Metered credits; never unlimited |

The separation is a hard product rule, not a marketing position:

> **Software and services are completely separated.** Ending a subscription stops official cloud services. It never removes, degrades, time-limits or locks a local capability, a local document, a local agent, or a locally configured provider key.

### 1.1 Commercial invariants

These are requirements, not pricing. Amounts, allowances and pack sizes are versioned commercial policy under **D-020** and are deliberately absent from this document.

| # | Invariant | Authority |
|---|---|---|
| C-01 | Every local feature of every desktop product is free, with no feature gating by plan, no quality ceiling by plan, and no object-count ceiling by plan. | D-002, Stage 0 |
| C-02 | Local agent capability — capability discovery, cross-application calls, agent tool calling, multi-application workflows, local agent sessions, local knowledge, local full-text search, local vector search, local embedding, local models and local BYOK — is free forever and must never move behind a subscription. | Stage 0, Stage 13 §88 |
| C-03 | Cloud BYOK is included in the cloud subscription. No token commission is charged on the user's own provider spend. | Stage 0 |
| C-04 | Managed AI is quota-based. "Unlimited AI" must never be offered, described, implied or configurable. | Stage 0, D-020 |
| C-05 | No account is required to install, launch or use any desktop product locally. | Stage 1, Stage 13 §56 |
| C-06 | Logging in without paying never reduces local functionality. | Stage 0 §15 |
| C-07 | Subscription expiry never locks the software, the local data, the local agent, or local BYOK. Cloud-resident data enters a defined grace period. Cloud sync stops growing. | Stage 0 §15 |
| C-08 | Self-hosting the server is a first-class supported deployment, not a degraded mode. | Stage 0 §13, Stage 7 |
| C-09 | Storage is quantified and tiered. "Unlimited storage" must never be offered. Large raw media defaults to local, with cloud participation as an explicit user act. | Stage 0 §7 |
| C-10 | `ProductScope` is modelled from day one even though a single suite subscription is sold initially. It exists to permit later per-product plans without a data-model change; it is not a reason to split pricing now. | Stage 0 §5, Stage 13 §86–87 |
| C-11 | All customer-facing commerce is transacted by **Paddle** as Merchant of Record; **Payoneer** is the payout destination only and never appears in a customer-facing flow. | D-005 |
| C-12 | ArcChat Mobile is a free consumption-only companion. It sells nothing, embeds no checkout, exposes no external purchase call to action, and unlocks nothing from a locally entered key or token. | D-022 |

---

## 2. The product portfolio

### 2.1 Frozen desktop portfolio

The Phase 1 product baseline contains **exactly four desktop products** (**D-002**).

| Product | Stable product identity | Positioning | Business classification | Roadmap priority |
|---|---|---|---|---|
| **ArcChat** | `arcchat` | AI Agent Command Center / Chat / Task / Automation / Local Hub / Remote Control Plane | Coordination & Agent product | Core |
| **ArcNotes** | `arcnotes` | Local-first Knowledge & Document authority | Knowledge product | Core |
| **ArcScope** | `arcscope` | Local-first Observation / Acquisition / Telemetry Analysis authority | Observation & Analysis product | Core |
| **ArcSlate** | `arcslate` | Local-first Professional Non-linear Video Editing authority | Media Creation product | Second |

**Roadmap priority is not architectural status.** All four are first-class products with independent installation, execution, versioning, projects, data, undo and recovery, release cadence, capability surface, cloud participation, settings and lifecycle. ArcSlate being scheduled later never makes it a second-class architectural citizen (Stage 13 §4).

The classification above is *product classification only*. It must not become a domain inheritance hierarchy; no `ArcProductBase` domain type may be created to unify the four (Stage 13 §85).

### 2.2 Non-desktop products and surfaces

| Surface | Identity | Positioning | Notes |
|---|---|---|---|
| **ArcForges Cloud** | `cloud` | One logical managed platform | ASP.NET Core JIT modular monolith (**D-008**). Not four per-product backends (Stage 13 §43). |
| **ArcForges Web** | `web` | Public static site + one interactive Blazor WebAssembly application | Static public pages plus `ArcForges.Web.App` (**D-007**). Account and Chat are deployment configurations of one codebase (**D-014**). |
| **ArcChat Mobile** | `arcchat-mobile` | ArcChat continuity/companion surface on Android (iOS architecture-present, build-deferred) | Apache-2.0 boundary (**D-004**); consumption-only (**D-022**); Android on .NET 10 Mono AOT (**D-008**). |

Mobile and Web are **ArcChat companion surfaces**, not mobile or web editions of the four desktop products (Stage 13 §45–46, Invariant 16). There is no ArcNotes Mobile editor, no ArcScope Mobile editor and no ArcSlate Mobile editor in this baseline. Their absence is a baseline statement, not a permanent prohibition; adding one is an Architecture Baseline Change.

### 2.3 Excluded product names

`ArcCanvas`, `ArcMusic`, `ArcImage` and `ArcVideo` are **obsolete and SUPERSEDED** (**D-002**). They are not current products, future products, reserved products, aliases or re-entry candidates.

Consequences that bind every downstream document, schema, contract, identifier, directory name, test name and CI matrix entry:

- No database, table, column, enum member, runtime component, dependency, navigation entry, contract, specification, roadmap item, work package, telemetry dimension or feature flag may be created for them.
- **ArcScope is an independently defined product, not a rename or continuation of ArcImage.** The ArcImage domain vocabulary — Canvas, Layer, Mask, Filter, image editing — must never be mechanically migrated into ArcScope (Stage 13 §2, §3; D-002).
- **ArcSlate inherits product *direction* from ArcVideo, not its model.** The retained high-level concepts are Project, Timeline, Track, Clip, Effect, Media, Proxy, Render, Undo/Recovery and resource ownership. The complete ArcSlate model is defined by its own product specification, informed by ArcVideo and ArcVideoFoundation as references only (**D-012** as amended 2026-09-05, `P2-005`) (Stage 13 §2, §7).
- **ArcNotes Edgeless Canvas is an ArcNotes capability**, never a standalone product (**D-002**).
- The raw input files under `docs/inputs/` retain these names as preserved historical evidence and are never edited.

### 2.4 Adding a fifth product

A future fifth first-class product is an **Architecture Baseline Change** requiring a formal decision, not a solution-file addition. Before acceptance it must answer, in writing (Stage 13 §81):

1. What state does it own authoritatively?
2. Can it perform its core work with ArcChat absent?
3. What are its resources and their lifecycle?
4. What does it synchronise, and under which sync scope?
5. What capabilities does it expose, at what risk levels?
6. What artifacts does it produce, and who owns them?
7. How does it recover from crash, corruption and interrupted migration?
8. What native boundary, if any, does it require?

Adding a product must not require modifying `ArcChat.Domain`. ArcChat must recognise a new product through the cross-application capability/contribution contract, never through a compile-time `switch (appId)` (Stage 13 §82–83).

---

## 3. Product independence requirements

### 3.1 Local-first independence

Every professional product must complete its core professional work with ArcChat absent, with no account, and with no network (Stage 13 §10, Invariants 7 and 8).

| Product | Core work that must succeed with ArcChat absent, signed out and offline |
|---|---|
| ArcNotes | Open, create, edit, locally search, save, export, recover |
| ArcScope | Connect a source, capture, inspect, analyse, save, export |
| ArcSlate | Import, edit, play back, save project, render/export |
| ArcChat | Chat, run local agents, use local models and local BYOK, run local tasks, manage its own projects and history |

### 3.2 Installation combinations

Every subset of the four products is a legal installation, including each product alone. Requirements (Stage 13 §12):

- No installer may refuse to install because another product is absent.
- No product may require another product to be running in order to save, open, export or recover.
- Absence of ArcChat degrades ecosystem capability; it never causes professional-application failure.

**Ecosystem Capability Degradation** — the defined, user-visible, non-failing loss when ArcChat is not running — covers exactly: cross-application agent orchestration, "Ask ArcChat", agent-driven multi-application workflows, ArcChat-local task orchestration, remote desktop agent, and ArcChat-hosted automation requiring local capabilities (Stage 13 §11).

### 3.3 Account and cloud independence

- Local usage requires no account (**C-05**).
- A cloud account is required only to activate a cloud capability: sync, cloud search, managed AI, remote agent, cloud BYOK (Stage 13 §57).
- **ArcNotes signing in to Cloud must not require ArcChat to exist.** The unified same-device account and session experience is shared desktop foundation, never an ArcChat-private authentication service (Stage 13 §58).
- No product may hard-code `api.arcforges.com` as the only possible realm. Official cloud and self-hosted deployments are different **Realms**. V1 user experience may default to Official (Stage 13 §59).
- Cross-realm objects are never the same authoritative object, even when the account email matches. Every cross-application and cross-device reference is realm-aware (Stage 13 §60).

---

## 4. Cross-product interaction model

### 4.1 Two distinct interaction shapes

| Shape | Path | When |
|---|---|---|
| **Handoff** | `App → App` directly, via Resource Reference plus Deep Link | A single user-directed step, e.g. "Open this report in ArcNotes" |
| **Orchestration** | `App/User → ArcChat → Apps` | Any automated multi-step workflow |

Automated cross-application orchestration goes through ArcChat, which owns intent, task, permission, approval, trace, compensation and artifact coordination (Stage 13 §13–14, Invariants 9 and 10). This does not make ArcChat a mandatory hop for ordinary user actions.

There is no full mesh between professional products. `ArcNotes ↔ ArcScope ↔ ArcSlate` direct automation relationships are prohibited.

### 4.2 Reference versus copy

Two cross-application semantics must be distinguished in the product surface, never blurred (Stage 13 §62):

- **Reference** — ArcNotes references an ArcScope Report. Ownership stays with ArcScope.
- **Copy / Import** — a new ArcNotes Document is created *from* an ArcScope Report. The new object is owned by ArcNotes.

The system must never silently produce a shared writable object between two products. Two products must never edit the same domain object (Stage 13 §23).

> **Reference ≠ Ownership.**

### 4.3 Artifacts

An **Artifact** is a meaningful work result produced by a task, agent or application — an ArcNotes Document, an ArcScope Report or Session, an ArcSlate rendered video or project, or an ordinary file. It is **not** "an ArcChat file" (Stage 13 §61).

ArcChat may hold an `ArtifactReference`, provenance and task relationship. The underlying business object is always owned by its producing or owning application.

### 4.4 Semantic capability, never remote UI

Cross-application calls transmit semantic capability invocations and references. Remotely operating another product's user interface, controls, view models or dispatcher is prohibited (Stage 13 Invariant 11; I3 §1.1).

### 4.5 Product-local AI entry points are permitted

ArcNotes, ArcScope and ArcSlate may each expose their own AI-assisted entry points ("Ask ArcChat about selection", "Analyze with ArcChat", "Ask ArcChat to edit…") and may contain local, specialised AI features. None of them implements a second complete agent orchestration platform. The unified multi-application agent system is ArcChat (Stage 13 §80).

---

## 5. State ownership

Ownership is a product-level requirement before it is an architectural one. The authoritative owner of each class of state is fixed.

| State | Authoritative owner |
|---|---|
| Chat / Conversation / Message | ArcChat |
| Agent task orchestration | ArcChat |
| Agent Profile, Skill configuration | ArcChat |
| ArcChat Projects | ArcChat |
| Local application/instance registry and capability registry | ArcChat Hub |
| Local approval coordination and local permission coordination | ArcChat Hub |
| ArcNotes Documents, Notes, knowledge organisation | ArcNotes |
| ArcNotes attachments and document metadata | ArcNotes |
| ArcScope Sessions and Capture state | ArcScope |
| ArcScope raw captured data | ArcScope |
| ArcScope measurements, annotations, analysis results, reports | ArcScope |
| ArcSlate Projects, Sequences/Timelines, Tracks, Clips | ArcSlate |
| ArcSlate media references, proxy state, render jobs, export configuration | ArcSlate |
| Undo and crash recovery for any professional object | The owning application |
| Cloud User, Identity, Workspace | ArcForges Cloud |
| Billing, Subscription, Entitlement | ArcForges Cloud |
| Cloud sync metadata | Cloud Sync module |
| Cloud stored blobs | Cloud Storage subsystem |
| Managed AI commercial ledger | ArcForges Cloud |

### 5.1 Prohibited ownership

ArcChat must never own (Stage 13 §17, §28):

- An authoritative ArcNotes document copy, or a writable ArcNotes knowledge database.
- An authoritative ArcScope Session, or raw ArcScope capture data.
- An ArcSlate Timeline, or ArcSlate media asset ownership.
- Any professional application's undo stack.
- A global crash journal on behalf of another product (Stage 13 §65).

The Hub is a **platform coordination plane** only. It must never store professional authoritative objects, proxy professional files or media, become a shared filesystem, become a universal project database, or become a universal undo service.

### 5.2 Caching does not transfer ownership

A cached projection of another product's state is permitted and must (Stage 13 §30; I3 §4.1):

- record its source and its revision;
- be discardable and re-fetchable;
- never become a write point;
- never widen visibility beyond the security permissions of the source.

The moment business changes begin to be written into a cached DTO, the ownership rule has been violated.

### 5.3 Native resources

Native resources — an ArcSlate GPU texture, an ArcScope device handle — belong exclusively to the owning product process. They must never enter the ArcChat domain, a Cloud DTO, or a `ResourceRef` as a raw pointer. Only stable resource identity, metadata and controlled access cross a boundary (Stage 13 §66).

---

## 6. Data and control paths

Four paths exist and are never conflated (Stage 13 §36–41, Invariants 13–15; **D-010**).

### 6.1 Local capability path

```
ArcChat (Hub)  ── StreamJsonRpc over Named Pipe / UDS ──  ArcNotes / ArcScope / ArcSlate
```

Same-machine, first-party, strongly typed semantic capability calls.

### 6.2 Cloud data path

```
ArcChat ────┐
ArcNotes ───┤
ArcScope ───┼── HTTPS (HTTP/JSON, + realtime where required) ──  ArcForges Cloud
ArcSlate ───┘
```

Each cloud-capable product participates directly in the cloud features of **its own data** — sync participation, upload and download, workspace object state, cloud storage participation. ArcChat is not required to be installed or running.

> **ArcChat is the local agent/coordination control plane, not the mandatory data gateway for professional applications.**

Requiring ArcChat in this path would mean "ArcChat crashes → ArcNotes cloud sync stops", which is prohibited (Stage 13 §39).

### 6.3 Remote desktop agent path

```
ArcChat Mobile / ArcChat Web
        ↓ HTTPS + realtime
   ArcForges Cloud
        ↓ durable ToolRequest, pulled by the desktop
   ArcChat Desktop  (re-authorises locally)
        ↓ StreamJsonRpc capability call
   ArcNotes / ArcScope / ArcSlate
```

This path always traverses ArcChat Desktop, because permission, approval, remote trust, task trace and orchestration belong to ArcChat (Stage 13 §40, Invariant 15).

**Cloud never connects to localhost, a Named Pipe, a Unix domain socket or local stdio** (**D-010**). The Cloud issues a durable `ToolRequest`; ArcChat Desktop pulls it, re-authorises it locally, executes the approved capability and returns an idempotent `ToolResult`.

Mobile and Web must never scan the LAN, discover a desktop Hub, or address a Named Pipe or UDS (Stage 13 §47).

### 6.4 The cloud response still goes through the owning domain

A cloud sync response must never be written straight into a UI model. It enters through the owning application's Application/Sync integration and then its domain and local state, exactly as a local edit does (Stage 13 §42).

---

## 7. Runtime and process requirements

| # | Requirement | Authority |
|---|---|---|
| P-01 | Each of the four products is a complete, autonomous operating-system application: `ArcChat`, `ArcNotes`, `ArcScope`, `ArcSlate` as separate executables (platform-appropriate package names). | Stage 13 §8, Invariant 3 |
| P-02 | There is **no** hidden central ArcForges desktop service holding product business state, and none may be introduced. | Stage 13 §8, §91 |
| P-03 | No professional application is a plug-in UI over an ArcChat universal database. | Stage 13 §9 |
| P-04 | Exactly one authoritative local coordinator exists: the ArcChat Hub. Products must not each run a competing Hub. | Stage 13 §48, Invariant 6 |
| P-05 | The ArcChat Hub is hosted inside the ArcChat process lifecycle. It is not installed as a system service (`ArcForgesService.exe` is prohibited). A background/tray mode is permitted and remains part of the ArcChat lifecycle. | Stage 13 §49 |
| P-06 | ArcChat may request that another installed product be launched on demand. Once started, that product is an independent runtime instance with its own lifecycle; ArcChat does not own it. | Stage 13 §50 |
| P-07 | Installed application and runtime instance are permanently distinct. `AppId == ProcessId` is prohibited. A product may have multiple runtime instances. | Stage 13 §51 |
| P-08 | Three identities are distinct and all three exist: `ProductId`/`AppId` (stable), `InstallationId` (device installation), `InstanceId` (process lifecycle). | Stage 13 §52 |
| P-09 | Each desktop product has its own local persistence. A single shared `ArcForges.db` covering all products is prohibited. Independent databases do not require different technologies. | Stage 13 §34–35, Invariant 5 |
| P-10 | Products must not reference one another's Domain or Application assemblies. Cross-product interaction is via stable cross-application contracts only. | Stage 13 §31 |
| P-11 | Shared foundation may provide **mechanism** only — identity primitives, result/error primitives, resource-reference primitives, task-reference primitives, cross-application contract primitives, observability, cloud client infrastructure, security primitives, update integration, design system. It must never hold business state and never become a fifth hidden product. Types such as `ArcForges.Foundation.Document` are prohibited. | Stage 13 §32, §74–75, Invariant 18 |
| P-12 | Product versions and release lifecycles are independent (`ArcChat 2.4` with `ArcNotes 1.8` is legal). No mandatory suite release train. A marketing release campaign is permitted; the production release unit remains the individual product. | Stage 13 §53, §55, Invariant 17 |
| P-13 | Application version and capability contract version are separate. Differing product version numbers must never by themselves cause a connection refusal; compatibility is negotiated on contract version. | Stage 13 §54 |

---

## 8. Technology constitution (inherited, not reopened)

The following are settled and are not reopened by any Phase 2 document.

| Area | Baseline | Authority |
|---|---|---|
| Language and runtime | C# / .NET 10 LTS across every product | I3 §2; Stage 13 §5 |
| Desktop UI | Avalonia, Windows / macOS / Linux, **Native AOT deliverable** | I3 §2.1; **D-008** |
| Cloud | ASP.NET Core **JIT modular monolith**; strict Native AOT is *not* a Cloud requirement | **D-008** |
| Mobile | .NET MAUI; **Android on the supported .NET 10 Mono AOT release path**; iOS architecture-present, build-deferred | **D-008** |
| Web | Static HTML/CSS public pages + one standalone Blazor WebAssembly application with `RunAOTCompilation=false` | **D-007** |
| Public request/response | ASP.NET Core Minimal API server; Refit generated-only HTTP/JSON client | I3 §16.3; **D-008** |
| Public realtime | SignalR, real-time delivery only, never the sole durable truth | I3 §16.5 |
| Local IPC | StreamJsonRpc Interface Code First over Named Pipe / Unix domain socket | I3 §6; **D-010** |
| Local wire format | Nerdbank.MessagePack with generated TypeShape by default | I3 §6.6 |
| Public JSON | `System.Text.Json` source generation, no reflection fallback | I3 §2.1 |
| Native interop | In-process `[LibraryImport]` P/Invoke across a narrow, versioned C ABI | I3 §15 |
| Prohibited | C++ workers, a central service owning all state, gRPC/Protobuf/MagicOnion/Aeron as the main RPC, Electron, Qt product bodies, Java/Kotlin desktop, reflection-based dynamic plug-ins on the AOT main path | I3 §1.2; Stage 13 §73 |

### 8.1 Permitted technical exceptions

The exception list is closed. Adding to it requires a formal decision (Stage 13 §67–73, Invariant 20).

| Exception | Boundary |
|---|---|
| **A — Android runtime** | Production is .NET 10 Mono AOT. Android CoreCLR and Android Native AOT are experimental and are not production baselines. Documentation must never conflate Mono AOT with CoreCLR Native AOT. (**D-008**, V-04) |
| **B — EF Core** | A strict Native AOT production host does not treat the EF Core runtime as irreplaceable infrastructure. Under **D-008** Cloud is JIT, so this constrains only AOT deliverables. Migration and build tooling may be isolated. |
| **C — Native libraries** | Codecs, FFmpeg, GPU, device SDKs, system APIs and high-performance primitives may enter the owning product process via `[LibraryImport]`/P/Invoke and a thin C ABI where required. **A native library must never own an ArcForges domain**: a native decoder is permitted, a native ArcSlate project manager is not. Product domain, business rules, tasks and state ownership are C#. |
| **D — Build/migration tooling** | Build tools, SDK tools and migration helpers need not themselves be Native AOT production processes. The production main path still follows the constitution. |
| **Future — Isolation host** | May be introduced by a formal decision if untrusted plug-ins, unstable drivers or real security isolation demand it. It is a controlled escape hatch, not a default route back to a C++ worker. |

---

## 9. Licensing scope

Two boundaries, per **D-004** and **D-021**.

| Boundary | Contents | Licence |
|---|---|---|
| **Apache-2.0 (interoperability)** | ArcChat Mobile application; mobile-only libraries, tests, packaging and platform integrations; ArcForges-owned public protocol specifications required for mobile interoperability; the corresponding wire schemas, DTOs and generated or handwritten client libraries; validation rules that express wire-format constraints; public protocol state semantics required for independent interoperability; the future public SDK surface | `Apache-2.0` |
| **AGPL-3.0-only (everything else)** | ArcChat Desktop, ArcNotes, ArcScope, ArcSlate, ArcForges Cloud and all server implementations, product-domain behaviour, server orchestration, desktop application use cases, policy decisions, persistence behaviour, entitlement authority, base ViewModel implementations and UI scaffolding, and everything not explicitly assigned to the Apache-2.0 boundary | `AGPL-3.0-only` |

Binding rules:

- AGPL components may consume the Apache-2.0 interoperability packages without changing their own licence.
- **ArcChat Mobile must not contain, link to, copy from, port from or reference any GPL-family or AGPL-only implementation**, directly or transitively.
- No App Store exception, dual licensing, proprietary grant or CLA. DCO continues with inbound-equals-outbound per scope.
- **Base ViewModel patterns are not shared between Avalonia desktop and MAUI mobile.** Each UI stack owns its implementation (**D-021**).
- Protocol communication across an explicit process or network boundary does not change the mobile client's licence.

Reuse of reference-repository material is licence-gated and provenance-gated under **D-013**; see [`../assurance/reference-coverage-and-provenance.md`](../assurance/reference-coverage-and-provenance.md).

---

## 10. Reference repositories

Reference repositories are sources of features, behaviour, tests, migration evidence and possibly reusable material. **They are never architecture authorities, parity commitments, or reasons to import a runtime stack** (**D-012**).

| Reference repository | Role |
|---|---|
| AionUi | ArcChat reference |
| AFFiNE, SiYuan | ArcNotes references |
| Serial-Studio | ArcScope reference |
| ArcVideo, ArcVideoFoundation | ArcSlate references (**D-012** as amended 2026-09-05, `P2-005`) |
| StartArcForges | Packaged-product and release-behaviour oracle |
| The existing `ArcForges` monorepo | Implementation-state inventory and reconciliation target (**D-011**) |

Every product receives a **Reference Coverage Matrix** — Copy / Rewrite / Improve / Replace / Reference Only / Drop — before its implementation planning is finalised (**D-012**, **D-006**).

---

## 11. Architecture Baseline Changes

The following changes are **Architecture Baseline Changes**. None may be made as an ordinary change; each requires a formal decision recorded in `docs/decisions/` (Stage 13 §91).

1. Making ArcNotes (or any professional product) depend on ArcChat.
2. Adding a shared writable business database.
3. Letting ArcChat hold an ArcScope Session or any other professional authoritative object.
4. Letting professional products reference each other's Domain or Application assemblies.
5. Adding a central desktop service that holds business state.
6. Changing the local host RPC technology.
7. Moving any desktop product off C#/Avalonia.
8. Introducing a new long-lived C++ worker.
9. Making Cloud a required condition for a local save.
10. Letting Mobile control a professional application directly, bypassing the ArcChat trust model.
11. Changing a product's domain ownership.
12. Adding a fifth first-class product.

Changes that do **not** reopen the baseline (Stage 13 §92): adding an ArcNotes block type, an ArcScope adapter, an ArcSlate effect, an ArcChat home card, a capability, an import format, an AI provider, or a cloud storage package — provided no invariant above is broken.

---

## 12. Design-time acceptance questions

Every subsequent design, specification and work package must be able to answer these immediately (Stage 13 §96):

1. Which product does this function belong to? (Unique, or an explicit cross-application orchestrator.)
2. Who owns its data?
3. Is ArcChat the owner, or a reference-holder/orchestrator?
4. Can the product still do its core work without ArcChat? (For a professional product: **yes**.)
5. Can the user still work locally without Cloud? (For every desktop product: **yes**.)
6. Is this cross-application behaviour a Handoff or an Orchestration?
7. Is this an ordinary implementation choice, or is it creating a new architecture exception?

A specification that cannot answer all seven is not complete.

---

## 13. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 0` | Business model, commercial layering, free/paid boundary, AI economics shape |
| `I4 §Stage 13` | Product portfolio freeze, state ownership, topology, invariants, baseline-change list |
| `I3 §0–§5`, `§31` | Technology constitution, reference direction, contract split rationale |
| `I2 §I`, `§II` | Name reconciliation, reference-repository roles, scope confirmations |
| `D-002` | Four-product baseline; exclusion of ArcCanvas / ArcMusic / ArcImage |
| `D-004`, `D-021` | Two-boundary licensing |
| `D-005`, `D-020`, `D-022`, `D-023` | Commercial posture, provider baseline, mobile commerce |
| `D-007`, `D-008` | Web and runtime/AOT matrix |
| `D-010` | Cloud topology and local-action model |
| `D-012`, `D-013` | Reference-repository roles and reuse gating |
