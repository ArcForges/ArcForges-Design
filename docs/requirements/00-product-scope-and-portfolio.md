# ArcForges Product Scope and Portfolio
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: `docs/decisions/phase-1-foundation-decisions.md` ([D-001](../decisions/phase-1-foundation-decisions.md#rule-d-001) … [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023))
> Companions: [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md), [`../architecture/00-architecture-overview.md`](../architecture/00-architecture-overview.md)

This document defines what ArcForges is, what it contains, what it deliberately does not contain, and the product-level boundaries that every other requirement, architecture and work-package document must respect.

[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) is the dated user-directed amendment. Earlier decisions apply only where consistent with that amendment. The [deprecated inputs](../deprecated-inputs/README.md) are historical provenance only and do not add current requirements.

---

## 1. Product statement

ArcForges is a C# product family with native professional desktop applications and a **cloud-centred account, continuity and AI service**. Desktop UI is Avalonia/Skia without WebView. Cloud operates the single agent Harness, model-provider access, subscription capacity, credits and policy. Native editing, acquisition and media processing remain product responsibilities.

| Layer | Contents | Commercial posture |
|---|---|---|
| Native applications | Editing, acquisition, playback, rendering, local working caches and recovery | Open-source applications; ordinary native processing is not AI service consumption |
| ArcForges Cloud | Account, single-owner workspaces, synchronised data, history, storage, search and continuity | Official paid service term; independent self-host deployment supported |
| Cloud AI | Model calls, single-agent tasks and automation, cloud retrieval and authorised tool coordination | Active service term plus replenishing included capacity; opt-in purchased credits for extra usage |

### 1.1 Commercial invariants

| # | Invariant | Authority |
|---|---|---|
| C-01 | Native editing, acquisition, playback and recovery have no plan-dependent quality ceiling. Cloud availability, cloud writes and AI access are separately gated; no universal offline-AI or account-free notebook promise is made. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| <a id="rule-c-02"></a>C-02 | All AI and AI automation run in Cloud. No local model, local embedding provider, local autonomous agent or end-user provider-key mode exists. Ordinary keyword search and native product jobs do not require AI. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| <a id="rule-c-03"></a>C-03 | Official AI requires an active paid service term. Purchased credits alone, a desktop setting or a self-host policy cannot authorise official inference. No end-user BYOK exists. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| <a id="rule-c-04"></a>C-04 | Subscription AI capacity replenishes under declared rate and resource limits. Exact metering and opt-in extra credits are specified in the commerce requirements. Unqualified unlimited-compute promises are prohibited; any hard allowance limit must be disclosed. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006), [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020) as amended |
| <a id="rule-c-05"></a>C-05 | Installation and launch require no account. Cloud notebook enrolment, cloud continuity and AI require an authenticated realm and workspace; AI additionally requires service entitlement. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| <a id="rule-c-06"></a>C-06 | Signing in or changing plans never deletes native files or pending edits. UI distinguishes cloud unavailability from local processing availability. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| <a id="rule-c-07"></a>C-07 | After the paid term ends, new official AI calls stop even with purchased credit remaining. Credits remain recorded; retained data can be read/downloaded during the published retention period. Pending native edits remain recoverable. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| C-08 | Self-hosting uses the same Cloud implementation and public contracts with deployment-operator credentials and policy. It need not charge its own users, and grants no access to official paid services. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| <a id="rule-c-09"></a>C-09 | Storage is quantified and tiered. Raw device captures and original media are not automatically uploaded; native resource locality remains explicit. Cloud-generated simulation data is cloud-owned and counts against storage quota. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| <a id="rule-c-10"></a>C-10 | One suite offer is sold initially. ProductScope identifies eligible capabilities; it does not require separate product plans or team offers. | [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| C-11 | Paddle remains the customer-facing Merchant of Record; Payoneer remains payout only. The prepaid Cloud Pass is an active paid service term under [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023), not credit-only access. | [D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005), [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023), [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| C-12 | ArcChat Mobile remains consumption-only: no checkout, purchase call to action or locally entered entitlement key. All surfaces consume the same server-owned entitlement and usage. | [D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022), [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |

Official operating values are external deployment configuration, not compiled constants. Public schemas, runnable examples and the real metering/entitlement implementation remain available; no private policy repository or proprietary policy engine is required.

---

## 2. The product portfolio

### 2.1 Frozen desktop portfolio

The Phase 1 product baseline contains **exactly four desktop products** (**[D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002)**).

| Product | Stable product identity | Positioning | Business classification | Roadmap priority |
|---|---|---|---|---|
| **ArcChat** | `arcchat` | AI Agent Command Center / Chat / Task / Automation / Local Hub / Remote Control Plane | Coordination & Agent product | Core |
| **ArcNotes** | `arcnotes` | Cloud-backed Knowledge & Document workspace | Knowledge product | Core |
| **ArcScope** | `arcscope` | Local-first Observation / Acquisition / Telemetry Analysis authority | Observation & Analysis product | Core |
| **ArcSlate** | `arcslate` | Local-first Professional Non-linear Video Editing authority | Media Creation product | Second |

**Roadmap priority is not architectural status.** All four are first-class products with independent installation, execution, versioning, projects, data, undo and recovery, release cadence, capability surface, cloud participation, settings and lifecycle. ArcSlate being scheduled later never makes it a second-class architectural citizen.

The classification above is *product classification only*. It must not become a domain inheritance hierarchy; no `ArcProductBase` domain type may be created to unify the four.

### 2.2 Non-desktop products and surfaces

| Surface | Identity | Positioning | Notes |
|---|---|---|---|
| **ArcForges Cloud** | `cloud` | One logical managed platform | ASP.NET Core Native AOT modular monolith (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**). Not four per-product backends. |
| **ArcForges Web** | `web` | Public static site + one interactive React/TypeScript application | Static public pages plus `ArcForges.Web.App` (**[D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007)**). Account and Chat are deployment configurations of one codebase (**[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)**). |
| **ArcChat Mobile** | `arcchat-mobile` | ArcChat continuity/companion surface on Android (iOS architecture-present, build-deferred) | Apache-2.0 boundary (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**); consumption-only (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**); Android on React Native/Hermes (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**). |

Mobile and Web are **ArcChat companion surfaces**, not mobile or web editions of the four desktop products. There is no ArcNotes Mobile editor, no ArcScope Mobile editor and no ArcSlate Mobile editor in this baseline. Their absence is a baseline statement, not a permanent prohibition; adding one is an Architecture Baseline Change.

### 2.3 Excluded product names

`ArcCanvas`, `ArcMusic`, `ArcImage` and `ArcVideo` are **obsolete and SUPERSEDED** (**[D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002)**). They are not current products, future products, reserved products, aliases or re-entry candidates.

Consequences that bind every downstream document, schema, contract, identifier, directory name, test name and CI matrix entry:

- No database, table, column, enum member, runtime component, dependency, navigation entry, contract, specification, roadmap item, work package, telemetry dimension or feature flag may be created for them.
- **ArcScope is an independently defined product, not a rename or continuation of ArcImage.** The ArcImage domain vocabulary — Canvas, Layer, Mask, Filter, image editing — must never be mechanically migrated into ArcScope ([D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002)).
- **ArcSlate inherits product *direction* from ArcVideo, not its model.** The retained high-level concepts are Project, Timeline, Track, Clip, Effect, Media, Proxy, Render, Undo/Recovery and resource ownership. The complete ArcSlate model is defined by its own product specification, informed by ArcVideo and ArcVideoFoundation as references only (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** as amended 2026-09-05, [P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005)).
- ArcNotes Edgeless/Canvas and presentation capabilities are excluded by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006); the historical [D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002) naming distinction is not a delivery obligation.
- The files under [`docs/deprecated-inputs/`](../deprecated-inputs/README.md) retain these names only in their unchanged historical bodies; they are excluded from current design and audit scope.

### 2.4 Adding a fifth product

A future fifth first-class product is an **Architecture Baseline Change** requiring a formal decision, not a solution-file addition. Before acceptance it must answer, in writing:

1. What state does it own authoritatively?
2. Can it perform its core work with ArcChat absent?
3. What are its resources and their lifecycle?
4. What does it synchronise, and under which sync scope?
5. What capabilities does it expose, at what risk levels?
6. What artifacts does it produce, and who owns them?
7. How does it recover from crash, corruption and interrupted migration?
8. What native boundary, if any, does it require?

Adding a product must not require modifying `ArcChat.Domain`. ArcChat must recognise a new product through the cross-application capability/contribution contract, never through a compile-time `switch (appId)`.

---

## 3. Product independence requirements

### 3.1 Native product independence and cloud continuity

Every product installs and runs without another product. Cloud features can depend on the selected Cloud realm; they must not depend on ArcChat being installed.

| Product | Native responsibility with ArcChat absent or Cloud unavailable |
|---|---|
| ArcNotes | Open authorised cached content; edit and search hydrated notes; durably preserve pending edits and recover after a crash. Initial notebook creation/enrolment and uncached content require Cloud. |
| ArcScope | Connect a local source, capture, inspect, analyse, save and produce outputs. A Cloud simulation requires Cloud; already downloaded capture data remains usable. |
| ArcSlate | Import media, edit, play back, save, render/export and exchange .otio. Cloud features and AI are independently unavailable. |
| ArcChat | Display cached conversation/task state and manage native UI. No offline model loop, autonomous task execution or AI automation. Local tool execution requires a valid Cloud request and local authorisation. |

The Cloud acknowledgement is authoritative for synchronised revisions. A local durable save protects an edit pending synchronisation; it must never be labelled as already saved to Cloud. Scope/Slate hardware and media working stores retain their product-local authority.

---

### 3.2 Installation combinations

Every subset of the four products is a legal installation, including each product alone. Requirements:

- No installer may refuse to install because another product is absent.
- No product may require another product to be running in order to save, open, export or recover.
- Absence of ArcChat degrades ecosystem capability; it never causes professional-application failure.

When ArcChat is absent, user-directed deep links and direct product Cloud access remain. Cloud tasks needing the desktop tool bridge wait for the authorised device/app; Cloud-only AI and product-scoped AI entry points do not depend on ArcChat Desktop.

### 3.3 Account and cloud boundary

- Cloud notebook enrolment, AI and cross-device continuity require an authenticated realm/workspace.
- Existing cached data and pending edits survive connectivity loss and subscription expiry; cloud writes, AI admission and retention follow their explicit lifecycle.
- Each professional product authenticates directly through the shared client foundation, without ArcChat as a login service.
- Official and self-hosted servers are separate realms. Identity, credits, policy and resources never cross realms implicitly.
- A single-owner workspace remains isolated from every other owner's data. There are no organisation, member, invite or shared-editor concepts.

---

## 4. Cross-product interaction model

### 4.1 Two distinct interaction shapes

| Shape | Path | When |
|---|---|---|
| **Handoff** | `App → App` directly, via Resource Reference plus Deep Link | A single user-directed step, e.g. "Open this report in ArcNotes" |
| **Orchestration** | User/product → Cloud Harness → authorised Cloud tools or desktop ToolRequest bridge | AI-driven multi-step work |

The Cloud Harness owns durable intent, task, run, approval, trace, budget and compensation coordination. ArcChat presents this state and bridges authorised local tools. Ordinary native activities are product-owned jobs, not Cloud Agent Tasks.

There is no full mesh between professional products. `ArcNotes ↔ ArcScope ↔ ArcSlate` direct automation relationships are prohibited.

### 4.2 Reference versus copy

Two cross-application semantics must be distinguished in the product surface, never blurred:

- **Reference** — ArcNotes references an ArcScope Report. Ownership stays with ArcScope.
- **Copy / Import** — a new ArcNotes Document is created *from* an ArcScope Report. The new object is owned by ArcNotes.

The system must never silently produce a shared writable object between two products. Two products must never edit the same domain object.

> **Reference ≠ Ownership.**

### 4.3 Artifacts

An **Artifact** is a meaningful work result produced by a task, agent or application — an ArcNotes Document, an ArcScope Report or Session, an ArcSlate rendered video or project, or an ordinary file. It is **not** "an ArcChat file".

ArcChat may hold an `ArtifactReference`, provenance and task relationship. The underlying business object is always owned by its producing or owning application.

### 4.4 Semantic capability, never remote UI

Cross-application calls transmit semantic capability invocations and references. Remotely operating another product's user interface, controls, view models or dispatcher is prohibited.

### 4.5 Product AI entry points

ArcNotes, ArcScope and ArcSlate may expose selection-scoped AI actions and call the Cloud AI surface directly with minimal authorised context. No desktop contains provider credentials, model orchestration or a second Harness. Cloud results enter the owning product's validated editing/application path; bulk changes remain reviewable and reversible.

---

## 5. State ownership

Ownership is a product-level requirement before it is an architectural one. The authoritative owner of each class of state is fixed.

| State | Authoritative owner |
|---|---|
| Chat / Conversation / Message | Cloud Chat module; ArcChat clients hold projections and pending user drafts |
| Agent task orchestration | Cloud Agent module / single Harness |
| Agent Profile, Skill configuration | Cloud Agent module; clients edit authorised configuration |
| ArcChat Projects | Cloud Chat module |
| Local application/instance registry and capability registry | ArcChat Hub |
| Local approval coordination and local permission coordination | ArcChat Hub |
| ArcNotes Documents, Notes, knowledge organisation | Cloud Notes module for acknowledged revisions; ArcNotes for local pending edits and editor state |
| ArcNotes attachments and document metadata | Cloud Notes module; native clients keep scoped caches and pending upload staging |
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

ArcChat must never own:

- An authoritative ArcNotes document copy, or a writable ArcNotes knowledge database.
- An authoritative ArcScope Session, or raw ArcScope capture data.
- An ArcSlate Timeline, or ArcSlate media asset ownership.
- Any professional application's undo stack.
- A global crash journal on behalf of another product.

The Hub is a **platform coordination plane** only. It must never store professional authoritative objects, proxy professional files or media, become a shared filesystem, become a universal project database, or become a universal undo service.

### 5.2 Caching does not transfer ownership

A cached projection of another product's state is permitted and must:

- record its source and its revision;
- be discardable and re-fetchable;
- never become a write point;
- never widen visibility beyond the security permissions of the source.

The moment business changes begin to be written into a cached DTO, the ownership rule has been violated.

### 5.3 Native resources

Native resources — an ArcSlate GPU texture, an ArcScope device handle — belong exclusively to the owning product process. They must never enter the ArcChat domain, a Cloud DTO, or a `ResourceRef` as a raw pointer. Only stable resource identity, metadata and controlled access cross a boundary.

---

## 6. Data and control paths

Four paths exist and are never conflated (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**).

### 6.1 Local capability path

```
ArcChat (Hub)  ── gRPC over Named Pipe / UDS ──  ArcNotes / ArcScope / ArcSlate
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

> **ArcChat is the local tool bridge and coordination UI; professional products access their own Cloud services directly.**

Requiring ArcChat in this path would mean "ArcChat crashes → ArcNotes cloud sync stops", which is prohibited.

### 6.3 Remote desktop agent path

```
ArcChat Mobile / ArcChat Web
        ↓ HTTPS + realtime
   ArcForges Cloud
        ↓ durable ToolRequest, pulled by the desktop
   ArcChat Desktop  (re-authorises locally)
        ↓ gRPC capability call
   ArcNotes / ArcScope / ArcSlate
```

A Cloud task needing first-party desktop capabilities uses ArcChat Desktop for device-side authorisation and IPC. Durable task, approval and trace authority stays in Cloud. Both desktop-originated and companion-originated AI use this same path.

**Cloud never connects to localhost, a Named Pipe, a Unix domain socket or local stdio** (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**). The Cloud issues a durable `ToolRequest`; ArcChat Desktop pulls it, re-authorises it locally, executes the approved capability and returns an idempotent `ToolResult`.

Mobile and Web must never scan the LAN, discover a desktop Hub, or address a Named Pipe or UDS.

### 6.4 The cloud response still goes through the owning domain

A cloud sync response must never be written straight into a UI model. It enters through the owning application's Application/Sync integration and then its domain and local state, exactly as a local edit does.

---

## 7. Runtime and process requirements

| # | Requirement | Current definition / implementation |
|---|---|---|
| P-01 | Each of the four products is a complete, autonomous operating-system application: `ArcChat`, `ArcNotes`, `ArcScope`, `ArcSlate` as separate executables (platform-appropriate package names). | [Desktop process structure](../architecture/04-desktop-application-architecture.md#1-process-structure) |
| P-02 | There is **no** hidden central ArcForges desktop service holding product business state, and none may be introduced. | [Architecture constraints](../architecture/00-architecture-overview.md) |
| P-03 | No professional application is a plug-in UI over an ArcChat universal database. | [Product independence](#3-product-independence-requirements) |
| P-04 | Exactly one authoritative local coordinator exists: the ArcChat Hub. Products must not each run a competing Hub. | [Hub lifecycle](../architecture/03-local-ipc-and-process-model.md#4-hub-and-registration) |
| <a id="rule-p-05"></a>P-05 | The ArcChat Hub is hosted inside the ArcChat process lifecycle. It is not installed as a system service (`ArcForgesService.exe` is prohibited). A background/tray mode is permitted and remains part of the ArcChat lifecycle. | [Hub lifecycle](../architecture/03-local-ipc-and-process-model.md#4-hub-and-registration) |
| <a id="rule-p-06"></a>P-06 | ArcChat may request that another installed product be launched on demand. Once started, that product is an independent runtime instance with its own lifecycle; ArcChat does not own it. | [Product lifecycle operations](../architecture/contracts/02-local-rpc-operations.md#5-resource-access-and-lifecycle) |
| P-07 | Installed application and runtime instance are permanently distinct. `AppId == ProcessId` is prohibited. A product may have multiple runtime instances. | [Identity definitions](01-normative-glossary-and-invariants.md#1-identity-and-tenancy) |
| P-08 | Three identities are distinct and all three exist: `ProductId`/`AppId` (stable), `InstallationId` (device installation), `InstanceId` (process lifecycle). | [Identity definitions](01-normative-glossary-and-invariants.md#1-identity-and-tenancy) |
| <a id="rule-p-09"></a>P-09 | Each desktop product has its own local persistence. A single shared `ArcForges.db` covering all products is prohibited. Independent databases do not require different technologies. | [Desktop data model](../architecture/data-model/02-desktop-data-model.md) |
| <a id="rule-p-10"></a>P-10 | Products must not reference one another's Domain or Application assemblies. Cross-product interaction is via stable cross-application contracts only. | [Project reference rules](../architecture/01-solution-and-project-layout.md) |
| P-11 | Shared foundation may provide **mechanism** only — identity primitives, result/error primitives, resource-reference primitives, task-reference primitives, cross-application contract primitives, observability, cloud client infrastructure, security primitives, update integration, design system. It must never hold business state and never become a fifth hidden product. Types such as `ArcForges.Foundation.Document` are prohibited. | [Shared-foundation boundary](../architecture/00-architecture-overview.md) |
| <a id="rule-p-12"></a>P-12 | Product versions and release lifecycles are independent (`ArcChat 2.4` with `ArcNotes 1.8` is legal). No mandatory suite release train. A marketing release campaign is permitted; the production release unit remains the individual product. | [Distribution and release requirements](10-distribution-update-and-support.md) |
| <a id="rule-p-13"></a>P-13 | Application version and capability contract version are separate. Differing product version numbers must never by themselves cause a connection refusal; compatibility is negotiated on contract version. | [Contract compatibility](../architecture/02-contracts-and-protocols.md) |

---

## 8. Technology constitution

The following apply with the explicit user amendment P2-006.

| Area | Baseline | Current definition / decision |
|---|---|---|
| Language and runtime | Managed applications: C# / .NET 10 LTS; Web: React/TypeScript with Node.js tooling | [Runtime matrix](../architecture/00-architecture-overview.md), [Web amendment](../decisions/phase-2-specification-decisions.md#rule-p2-008) |
| Desktop UI | Pure-native Avalonia/Skia, Windows / macOS / Linux, Native AOT; no WebView, Chromium, DOM, JavaScript engine, HTML-as-UI or loopback UI | [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008), [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| Cloud | One ASP.NET Core Native AOT modular-monolith deployment host, including bounded business background services and canonical Task/Agent ports; replicas use the same host. CF Workflow owns the sole model/tool loop | [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008), [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) |
| Mobile | .NET React Native; **Android on the supported React Native/Hermes release path**; iOS architecture-present, build-deferred | **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** |
| Web | Static React-generated public HTML/CSS plus one React/TypeScript Account/Chat application; Node.js/npm tooling; proto → C#/TypeScript SDKs | **[P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008)** |
| Public request/response | Handwritten proto; generated C# native gRPC and TS/RN unary gRPC-Web; same owner errors/revisions | [Wire registry](../architecture/contracts/04-protobuf-wire-registry.md) |
| Public realtime | gRPC hint polling, real-time delivery only, never the sole durable truth | [Realtime contract](../architecture/contracts/03-realtime-and-bridge.md) |
| Local IPC | gRPC Interface Code First over Named Pipe / Unix domain socket | [Transport definition](../architecture/03-local-ipc-and-process-model.md#2-authenticated-local-transport) |
| Local wire format | Protocol Buffers with generated TypeShape by default | [Wire format definition](../architecture/03-local-ipc-and-process-model.md#3-wire-and-flow-control-profile) |
| Public JSON | `System.Text.Json` source generation, no reflection fallback | [Operation contract](../architecture/contracts/00-operation-catalogue.md) |
| Native interop | `[LibraryImport]` across a narrow C ABI, in its owning product or the approved C# content helper according to the isolation profile | [Native ABI contract](../architecture/12-native-interop-and-media.md#3-managed-to-native-calling-discipline), [isolation](../architecture/24-content-and-extension-isolation.md) |
| Prohibited | C++ workers, a central service owning all state, gRPC/Protobuf/MagicOnion/Aeron as the main RPC, Electron, Qt product bodies, Java/Kotlin desktop, reflection-based dynamic plug-ins on the AOT main path | [Architecture constraints](../architecture/00-architecture-overview.md), [permitted exceptions](#81-permitted-technical-exceptions) |

### 8.1 Permitted technical exceptions

The exception list is closed. Adding to it requires a formal decision.

| Exception | Boundary |
|---|---|
| **A — Android runtime** | React Native/Hermes is the selected Android runtime under [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009). Server Native AOT imposes no .NET runtime requirement on Mobile. iOS architecture remains build-deferred. |
| **B — EF Core** | A strict Native AOT production host does not treat the EF Core runtime as irreplaceable infrastructure. Under **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** Cloud is Native AOT, so this constrains only AOT deliverables. Migration and build tooling may be isolated. |
| **C — Native libraries** | Codecs, FFmpeg, GPU, device SDKs, system APIs and high-performance primitives may enter the owning product process via `[LibraryImport]`/P/Invoke and a thin C ABI where required. **A native library must never own an ArcForges domain**: a native decoder is permitted, a native ArcSlate project manager is not. Product domain, business rules, tasks and state ownership are C#. |
| **D — Build/migration tooling** | Build tools, SDK tools and migration helpers need not themselves be Native AOT production processes. The production main path still follows the constitution. |
| **E — Content isolation ([P2-007](../decisions/phase-2-specification-decisions.md#rule-p2-007))** | A first-party C# Native AOT ContentSandbox runs hostile parsers/codecs under an OS-enforced profile, on demand and parent-bound. No UI, network, credentials, durable business state or agent loop. Product authority stays C# in its owner. Executable extensions use separately enforced package profiles. This exercises [D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016) and adds no C++ business worker. |

---

## 9. Licensing scope

Two boundaries, per **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** and **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**.

| Boundary | Contents | Licence |
|---|---|---|
| **Apache-2.0 (interoperability)** | ArcChat Mobile application; mobile-only libraries, tests, packaging and platform integrations; ArcForges-owned public protocol specifications required for mobile interoperability; the corresponding wire schemas, DTOs and generated or handwritten client libraries; validation rules that express wire-format constraints; public protocol state semantics required for independent interoperability; the future public SDK surface | `Apache-2.0` |
| **AGPL-3.0-only (everything else)** | ArcChat Desktop, ArcNotes, ArcScope, ArcSlate, ArcForges Cloud and all server implementations, product-domain behaviour, server orchestration, desktop application use cases, policy decisions, persistence behaviour, entitlement authority, base ViewModel implementations and UI scaffolding, and everything not explicitly assigned to the Apache-2.0 boundary | `AGPL-3.0-only` |

Binding rules:

- AGPL components may consume the Apache-2.0 interoperability packages without changing their own licence.
- **ArcChat Mobile must not contain, link to, copy from, port from or reference any GPL-family or AGPL-only implementation**, directly or transitively.
- No App Store exception, dual licensing, proprietary grant or CLA. DCO continues with inbound-equals-outbound per scope.
- **Base ViewModel patterns are not shared between Avalonia desktop and React Native mobile.** Each UI stack owns its implementation (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**).
- Protocol communication across an explicit process or network boundary does not change the mobile client's licence.

Reuse of reference-repository material is licence-gated and provenance-gated under **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**; see [`../assurance/reference-coverage-and-provenance.md`](../assurance/reference-coverage-and-provenance.md).

---

Production deployment values and credentials are not public sample configuration. Configuration format, validation, metering and enforcement code remain under their existing licence scope. Calling executable implementation a configuration file does not exempt it from applicable source obligations.

## 10. Reference repositories

Reference repositories are sources of features, behaviour, tests, migration evidence and possibly reusable material. **They are never architecture authorities, parity commitments, or reasons to import a runtime stack** (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**).

| Reference repository | Role |
|---|---|
| AionUi | ArcChat reference |
| AFFiNE, SiYuan | ArcNotes references |
| Serial-Studio | ArcScope reference |
| ArcVideo, ArcVideoFoundation | ArcSlate references (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** as amended 2026-09-05, [P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005)) |
| StartArcForges | Packaged-product and release-behaviour oracle |
| The existing `ArcForges` monorepo | Implementation-state inventory and reconciliation target (**[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)**) |

Every product receives a **Reference Coverage Matrix** — Copy / Rewrite / Improve / Replace / Reference Only / Drop — before its implementation planning is finalised (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**, **[D-006](../decisions/phase-1-foundation-decisions.md#rule-d-006)**).

---

## 11. Architecture Baseline Changes

The following changes are **Architecture Baseline Changes**. None may be made as an ordinary change; each requires a formal decision recorded in `docs/decisions/`.

1. Making ArcNotes (or any professional product) depend on ArcChat.
2. Adding a shared writable business database.
3. Letting ArcChat hold an ArcScope Session or any other professional authoritative object.
4. Letting professional products reference each other's Domain or Application assemblies.
5. Adding a central desktop service that holds business state.
6. Changing the local host RPC technology.
7. Moving any desktop product off C#/Avalonia.
8. Introducing a new long-lived C++ worker.
9. Requiring a Cloud acknowledgement before a native pending edit can be saved durably, or introducing a second independent notebook authority.
10. Letting Mobile control a professional application directly, bypassing the ArcChat trust model.
11. Changing a product's domain ownership.
12. Adding a fifth first-class product.

Changes that do **not** reopen the baseline: adding an ArcNotes block type, an ArcScope adapter, an ArcSlate effect, an ArcChat home card, a capability, an import format, an AI provider, or a cloud storage package — provided no invariant above is broken.

---

## 12. Design-time acceptance questions

Every subsequent design, specification and work package must be able to answer these immediately:

1. Which product does this function belong to? (Unique, or an explicit cross-application orchestrator.)
2. Who owns its data?
3. Is ArcChat the owner, or a reference-holder/orchestrator?
4. Can the product still do its core work without ArcChat? (For a professional product: **yes**.)
5. Which cached/native operations work without Cloud, and which require an account, fresh Cloud data or active service? The answer follows §3.1, not a blanket offline promise.
6. Is this cross-application behaviour a Handoff or an Orchestration?
7. Is this an ordinary implementation choice, or is it creating a new architecture exception?

A specification that cannot answer all seven is not complete.

---

## 13. Traceability

| Current document | Relationship |
|---|---|
| [ArcForges Architecture Overview](../architecture/00-architecture-overview.md) | Implements the accepted portfolio, ownership and runtime boundaries |
| [Solution and Project Layout](../architecture/01-solution-and-project-layout.md) | Places the products and shared mechanisms in their owning repositories |
| [D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002) | Four-product baseline; exclusion of ArcCanvas / ArcMusic / ArcImage |
| [D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004), [D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021) | Two-boundary licensing |
| [D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005), [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020), [D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022), [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023) | Commercial posture, provider baseline, mobile commerce |
| [D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007), [D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008) | Web and runtime/AOT matrix |
| [D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010) | Cloud topology and local-action model |
| [D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012), [D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013) | Reference-repository roles and reuse gating |

## Technology ownership amendment — P2-009

The ten-repository, Native AOT/proto/RN/CF/R2 boundary is fixed in [solution ownership](../architecture/01-solution-and-project-layout.md) and [CF integration](../architecture/contracts/05-cloudflare-integration.md). C# keeps canonical business rules; CF executes the sole model loop. Scope, permissions, data meanings, independent professional products and commercial recovery remain the accepted requirements above.
