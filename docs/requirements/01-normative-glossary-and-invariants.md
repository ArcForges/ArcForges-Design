# ArcForges Normative Glossary and Invariant Catalogue
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements — cross-cutting, consumed by every requirements, architecture, assurance and planning document
> Governs: **D-018** vocabulary and **V-02** term disambiguation. Earlier coverage evidence must be reconciled to P2-006 before the revised requirements claim closure.
> Owner role: Architecture Owner

This document is the single normative vocabulary for ArcForges. Every other authoritative document uses these terms with these meanings and no others.

## How to use this document

1. **One definition per canonical term.** If a term appears in a specification, contract, schema, UI string, telemetry dimension, database column, test name or work package, it carries the meaning defined here.
2. **Product-specific meanings are namespaced.** Where a word means different things in different products, the bare word is not usable; the namespaced form is mandatory (`ArcChat.Project`, `ArcScope.Project`, `ArcSlate.Project`).
3. **Every active `X ≠ Y` invariant in §7 is binding within current scope. Retired entries are historical only.**** Merging two sides of an invariant into one type, one table, one column, one flag, one enum, one endpoint, one event or one permission is an architecture violation, not a simplification.
4. **Forbidden aliases (§8) must not appear** in any new authoritative document, identifier, or user-visible string.
5. Terms are classified by space — **wire**, **domain**, **UI**, **storage**, **commercial** — in §6. A term may exist in more than one space; when it does, the spaces are distinct types and are never the same object.

---

## 1. Identity and tenancy

| Term | Space | Definition |
|---|---|---|
| **Realm** | domain, wire | An independent deployment of ArcForges Cloud that is its own authority: the Official realm, or a self-hosted realm. Objects are never identical across realms even when the account email matches. Every cross-device and cross-application reference is realm-aware. |
| **User** | domain, wire | A cloud account identity within a realm. |
| **Local Anonymous User** | domain | A signed-out native operator without a Cloud UserId. May use product-specific native functions; has no official AI access or account-free notebook service. |
| **Workspace** | domain, wire | A single-user Cloud data, device, sync, billing and permission boundary. One owner in a realm; never a team/member container or panel layout. |
| **Layout** | UI | A desktop panel/window arrangement. The mandatory term for what some products elsewhere call a "workspace". |
| **Organization** | retired | Excluded by P2-006: no organization, team, membership, invitation or collaboration-specific schema reservation. |
| **Device** | domain, wire | A registered client machine or handset within a realm. |
| **Installation** / `InstallationId` | domain | One installed copy of one product on one device. Long-lived. |
| **Instance** / `InstanceId` | domain, wire | One running process of one product. Per-launch. |
| **App** / `AppId`, `ProductId` | domain, wire | The stable product identity: `arcchat`, `arcnotes`, `arcscope`, `arcslate`. Never a process id, never a product-scope, never a licence unit. |
| **Window** | UI | An OS window belonging to an Instance. An Instance may own several. |
| **Session** | domain, wire | An authenticated interaction lifetime. Distinct from Connection, from Device and from Subscription. |
| **Connection** | wire | A transport-level link (Named Pipe/UDS stream, HTTP connection, realtime connection). Carries no identity of its own. |
| **Identity** | domain | Who a principal is. |
| **Actor** | domain, wire | On whose authority an operation runs. |
| **Executor** | domain | What actually performs an operation. |
| **Caller Instance** / **Caller Process** | wire | Which process issued a call. Never a substitute for Actor. |
| **Principal** | domain | A security subject that may hold permissions: a human User, or a scoped delegate. |
| **Agent Actor** | domain | An agent acting on behalf of a user session. Never an independent superuser identity, never a security principal in its own right. |
| **Local OS User** | domain | The operating-system account that owns local IPC endpoints and secure storage. |

---

## 2. Resources, references and artifacts

| Term | Space | Definition |
|---|---|---|
| **Resource** | domain, wire | A durable business object owned by exactly one product in exactly one realm. |
| **ResourceRef** | wire | A stable, realm-aware, typed reference to a Resource: identity plus metadata. Never resource content, never a file path, never a capability token, never a permission token, never a universal domain entity, never a selection. |
| **ResourceId** | domain, wire | The stable identifier inside a ResourceRef. Never reused. |
| **ResourceKind** | wire | The namespaced type of a Resource, e.g. `arcnotes.document`, `arcscope.session`, `arcslate.project`. |
| **External Locator** | storage | A path, URI or device address by which external content is reached. Never a Resource Identity. |
| **Managed Asset** | storage | Content whose bytes ArcForges owns and garbage-collects. |
| **External Reference** | storage | Content that remains under the user's own control, referenced but not owned. |
| **Artifact** | domain, wire | A meaningful work result produced by a Task, Agent or App — a document, report, session, rendered video, project or ordinary file. Never "an ArcChat file". |
| **ArtifactRef** | wire | A reference to an Artifact, carrying provenance and task relationship. Distinct from `ResourceRef`. Never a permission token. |
| **Artifact Preview** | UI | A rendered or summarised view of an Artifact. Never the Artifact's authority. |
| **Deep Link** | wire, UI | A user-directed navigation address into a product surface. Never a command. Never a permission token. |
| **Provenance** | domain | The recorded origin of a derived object: source resource, task, actor, revision. |

---

## 3. Capability, action and invocation

| Term | Space | Definition |
|---|---|---|
| **Capability** | domain, wire | A semantic, versioned, strongly typed operation a product exposes to the platform. Identified by a `capabilityId` string used only for discovery, display, policy, tool selection, routing and audit — never as the call mechanism. |
| **CapabilityDescriptor** | wire | The declared metadata of a Capability: identity, provider app/instance, typed method identity, contract version and feature flags, input/output summary, whether it writes state, required scope, risk level, whether confirmation is mandatory, dry-run/undo/cancel support, resource size, expected duration and concurrency limits. |
| **Action** | domain | A user- or agent-visible intent that may be fulfilled by one or more Capability invocations. Not itself a Capability. |
| **UI Command** | UI | A menu item, button or shortcut. Never a Capability. |
| **Invocation** / `InvocationId` | wire | One call of one Capability. Distinct from `CommandId`, and distinct from a Task Step. |
| **CommandId** | wire, storage | The idempotency key of a write command. Distinct from `InvocationId` and from `AttemptId`. |
| **Context** | domain, wire | What the caller is currently working on. References Resources; is not itself a Resource. |
| **Context Provider** | domain | A product-side component that answers "what is the user looking at / has selected". Not a search engine, not a resource database. |
| **Context Pack** | wire | A bounded, frozen set of context handed to a run. Never an entire knowledge source, never a copy of all data. |
| **Current Selection** | UI | Volatile UI state. Never a durable resource identity. |
| **Capability Token** | wire | A short-lived, narrowly scoped credential authorising one controlled access. Distinct from `ResourceRef`. |
| **Semantic Contract** | domain | The meaning and obligations of a Capability. |
| **Wire Contract** | wire | The serialized shape by which a Capability is called. Distinct from the Semantic Contract. |

---

## 4. Execution: intent, task, run, step, attempt

The ArcForges execution vocabulary is a strict hierarchy. No level may be collapsed into another.

| Term | Space | Definition |
|---|---|---|
| **Intent** | domain | What the user asked for, before any plan exists. |
| **Task** | domain, wire | Durable Cloud agent work with a lifecycle and persistent record. Ordinary render, capture, import or simulation jobs are not agent Tasks. |
| **Run** | domain, wire | One execution of a Task. A Task may have several Runs. |
| **Step** | domain, wire | One planned unit inside a Run. |
| **Attempt** / `AttemptId` | domain, wire | One execution try of a Step. Distinct from `CommandId`. |
| **Task Owner** | domain | The Cloud agent module holding authoritative Task/Run/Step/Attempt state. A desktop tool owner is not a Task Owner. |
| **Orchestrator** | domain | The single Cloud harness sequencing agent work and authorized tools. ArcChat presents tasks and bridges local tools; it does not run another orchestrator. |
| **Execution Location** | domain | Cloud for the AI runtime. Desktop/Cloud/Hybrid labels on a task describe tool locality only; they never select another model loop. |
| **TaskHandle** | wire | A stable Cloud Agent Task reference for query/correlation, never an RPC connection or product job identity. |
| **TaskSnapshot** | wire | An authoritative point-in-time projection of Task state, retrievable over HTTP. |
| **Progress Event** | wire | A best-effort realtime notification. Never task authority. |
| **Checkpoint** | domain, storage | A resumable execution marker inside a Run. Never an Undo entry; never a Recovery Journal. |
| **Compensation** | domain | A forward action that reverses the observable effect of a completed step. Never a transaction rollback. |
| **Approval** | domain, wire | A bounded, parameter-bound, time-limited human authorisation of a specific pending operation. Never a persistent permission grant, never step-up authentication, never steering. |
| **Steering** | domain, wire | A user's execution-direction update to an active Task. Never an approval, never an ordinary conversation message. |
| **Needs Attention** | UI | A derived presentation flag over one or more pending Approvals or errors. Never a Task state. |
| **Budget** | domain | A per-task or per-automation ceiling on cost, credits, time or steps. Never an Entitlement. |
| **Automation** | domain | A durable definition that creates Tasks when a Trigger fires. Never itself a Task. |
| **Automation Occurrence** | domain | One firing of an Automation. Never a Task retry. |
| **Trigger Definition** | domain | The configured rule. |
| **Trigger Occurrence** | domain | One event matching the rule. |
| **Operational Trace** | domain | The recorded sequence of steps, invocations, decisions and results for a Run, safe to show. Never model chain-of-thought; never an Audit record. |

### 4.1 Related jobs and commercial terms

| Term | Space | Definition |
|---|---|---|
| **Product Job / Activity** | domain, UI | Bounded non-agent work owned by a product or Cloud module: capture, render, import, indexing, simulation. It has its own progress/cancel/recovery contract, never a second model loop. |
| **ProductJobHandle** | wire | Typed, owner-qualified reference to a product job that a Cloud Task may observe through tools. Not a TaskHandle. |
| **Measured Usage** | domain, storage | Normalized actual provider usage per attempt/category, with provenance and settled/unknown status; not a prompt-size estimate. |
| **Supplier Cost** | commercial | Actual billable provider units multiplied by the applicable supplier-rate snapshot, independently reconciled against provider charges. |
| **Customer Tariff** | commercial | Versioned rates converting eligible usage to customer service units; distinct from supplier cost and payment price. |
| **Included Capacity** | commercial | A bounded recoverable service-unit balance replenishing during eligible service time. Not a monthly cash or purchased-credit lot. |
| **Additional Credits** | commercial | Separate purchased/compensation lots consumed only with explicit consent and an eligible service term. Credit ownership alone grants no official AI access. |
| **Policy Publication** | storage | One validated, immutable version/hash of operator deployment configuration, archived for audit; not a mutable rewrite of historical usage or paid grants. |

### 4.2 Task lifecycle states

The lifecycle states are Queued, Running, Waiting, Paused, Interrupted, Succeeded, PartiallySucceeded, Failed and Canceled, as specified in AI execution §2. Waiting carries a reason such as device, approval, capacity or budget.

CancelRequested/Canceling and PauseRequested/Pausing describe control-request progress, not completed outcomes. Canceled does not imply no side effects. Succeeded means the declared postcondition holds. Product jobs and SimulationRun have their own documented lifecycle; a common progress surface does not force them into the Agent Task state machine.

---

## 5. Product-namespaced terms

### 5.1 ArcChat

The ArcChat product domain is Cloud-owned unless explicitly designated as native UI, draft, cache, Hub or local permission/tool state.

| Term | Definition |
|---|---|
| `ArcChat.Conversation` | An ordered thread of Messages. Not a Task. |
| `ArcChat.Message` | One turn in a Conversation. Not a Tool Call. |
| `ArcChat.Project` | An ArcChat-scoped grouping of conversations, context references and settings. **Not** a Workspace, **not** an `ArcScope.Project`, **not** an `ArcSlate.Project`. |
| `ArcChat.AgentProfile` | A saved configuration of model, tools, instructions and limits. Not a running agent; not a model; not a security principal. |
| `ArcChat.Skill` | Reusable guidance and configuration that shapes agent behaviour. Not a Capability; not extension code; not MCP; not a permission grant. |
| `ArcChat.PersonalMemory` | ArcChat-owned durable user-preference recall. Not ArcNotes knowledge; not a conversation summary. |
| `ArcChat.Hub` | The local platform coordination plane hosted inside the ArcChat process. |
| `ArcChat.Artifact` | An `ArtifactRef` held by ArcChat. Never the underlying owned object. |

### 5.2 ArcNotes

Cloud-acknowledged revisions are authoritative; native working caches preserve pending edits without becoming a separate account-free product.

| Term | Definition |
|---|---|
| `ArcNotes.Notebook` | The top-level ArcNotes container. **Not** a Workspace. |
| `ArcNotes.Folder` | A hierarchical container. **Not** a Tag. |
| `ArcNotes.Document` | The canonical document object. **Not** a file; **not** a Markdown file. |
| `ArcNotes.Block` | The addressable unit inside a Document, with a stable `BlockId`. **Not** a Markdown line. |
| `ArcNotes.Property` | Typed metadata on a Document or Block. **Not** document content. |
| `ArcNotes.Tag` | A non-hierarchical label. |
| `ArcNotes.SavedView` | A stored query and presentation over typed properties. Confers **no ownership** of the objects it lists. |
| `ArcNotes.Attachment` | A referenced binary managed by ArcNotes. Never base64 embedded in canonical content. |
| `ArcNotes.Canvas` (Edgeless) | Retired by P2-006. Edgeless, whiteboard, shape/connector/frame workspaces are excluded. |
| `ArcNotes.Database` | Bounded note organization through scalar properties, queries and table/list Saved Views; not the SQLite/PostgreSQL storage schema or a formula/relation/rollup platform. |
| `ArcNotes.Slides` | Retired by P2-006. Presentations, slide generation, frame ordering and presentation navigation are excluded. |
| `ArcNotes.ChecklistItem` | A document-local task item. **Not** an ArcChat Agent Task. |

### 5.3 ArcScope

| Term | Definition |
|---|---|
| `ArcScope.Project` | An ArcScope-scoped container of sources, sessions and analyses. **Not** an ArcForges Workspace. |
| `ArcScope.Device` | Physical or logical hardware. **Not** a DataSource. |
| `ArcScope.DataSource` | A configured source definition. |
| `ArcScope.ConnectionProfile` | Stored connection settings. **Not** a live Connection. |
| `ArcScope.Session` | An observation lifetime. **Not** a Connection; **not** a Capture. |
| `ArcScope.Capture` | A recorded data acquisition within a Session. |
| `ArcScope.Channel` | A transport-level stream of values. **Not** a Signal. |
| `ArcScope.Signal` | A semantically typed, named quantity. **Not** an Event. |
| `ArcScope.Event` | A discrete occurrence in time. |
| `ArcScope.RawSignal` / `DerivedSignal` | Acquired versus computed. Never conflated. |
| `ArcScope.Measurement` | A quantified reading with units and uncertainty. **Not** an Analysis. |
| `ArcScope.Analysis` | An interpretation over measurements. |
| `ArcScope.Decoder` | A protocol interpreter producing Decoder Output. **Decoder Output ≠ Raw Data.** |
| `ArcScope.Annotation` | A non-destructive marking. **Never** a data mutation. |
| `ArcScope.Comparison` | A side-by-side relation between sessions or captures. **Not** a merge. |
| `ArcScope.Report` | An ArcScope-owned report artifact. **Not** an ArcNotes Document. |
| `ArcScope.LiveView` / `Recording` | Display versus persistence. Pausing the view never pauses the capture. |
| `ArcScope.DisplayDecimation` | Downsampling for rendering only. Never the measurement data. |

The simulator additionally defines Cloud-owned **SimulationDefinition**, immutable **ScenarioVersion**, non-agent **SimulationRun**, immutable **SimulationSegment** and ordered **SimulationEvent**. SIM-01–SIM-20 in the ArcScope requirements govern these objects; synthetic provenance is mandatory.

### 5.4 ArcSlate

| Term | Definition |
|---|---|
| `ArcSlate.Project` | The editing project. **Not** a Sequence; **not** a media folder. |
| `ArcSlate.Sequence` | A timeline composition. **Not** a Timeline Clip. |
| `ArcSlate.Timeline` | The temporal arrangement inside a Sequence. |
| `ArcSlate.Track` | A lane within a Timeline. |
| `ArcSlate.Clip` | A placed reference to source media with in/out points. **Not** the source media. |
| `ArcSlate.MediaAsset` | The managed identity of a piece of media. **Not** a file path; **not** a Clip. |
| `ArcSlate.SourceTime` / `TimelineTime` | Source-relative versus composition-relative time. Never interchangeable. |
| `ArcSlate.VideoFrameTime` / `AudioSampleTime` | Distinct rate domains. Never the same clock. |
| `ArcSlate.Transition` | A declared relation between adjacent clips. **Not** an incidental overlap. |
| `ArcSlate.EffectDefinition` / `EffectInstance` | Type versus applied instance with parameters. |
| `ArcSlate.Keyframe` | A time-anchored parameter value. **Not** the current parameter value. |
| `ArcSlate.Proxy` | A lower-cost stand-in for original media. **Not** the original; **not** a render cache. |
| `ArcSlate.RenderCache` | Rebuildable rendered output. **Never** project authority. |
| `ArcSlate.RenderJob` | An ArcSlate-owned native product render/export Job, distinct from a Cloud Agent Task and UI progress dialog. |
| `ArcSlate.RenderedArtifact` | The produced media file. **Not** the ArcSlate Project. |
| `ArcSlate.Transcript` / `Subtitle` | Machine text versus authored, timed, styled display text. |

---

## 6. Term spaces

The same word may live in more than one space. When it does, the spaces are separate types and conversion is explicit.

| Space | Rule |
|---|---|
| **Domain** | The product's own model. Never serialized directly; never a database row; never a view model. |
| **Wire** | Contract DTOs and identifiers. Never a domain entity; never persisted as-is as the canonical store. |
| **UI** | View state and presentation. Never a transport DTO; never a domain object. |
| **Storage** | Database schema, native file format, cache format. Distinct from both Domain and Wire. |
| **Commercial** | Plan, Offer, Price, Entitlement, Credit, Ledger. Never a Feature Flag; never a Permission. |

> **Domain Model ≠ Database Schema ≠ Native File Format ≠ Interchange Format ≠ Cloud Sync Protocol.** A CLR type is never itself a persistent format contract.

---

## 7. Invariant catalogue

Every active entry is binding where its concepts are in current product scope. A distinction does not itself require an excluded feature or a dedicated table/type for an otherwise unnecessary concept. Retired rows retain IDs for historical traceability and create no delivery obligation. P2-006 changes invalidate prior unchanged-coverage claims; downstream mappings must be reconciled before Stage 2 closes.

### 7.1 Identity, tenancy and commerce

| # | Invariant |
|---|---|
| I-001 | User ≠ Workspace ≠ Device ≠ Session ≠ Subscription ≠ Entitlement |
| I-002 | Subscription cancellation ≠ Account deletion |
| I-003 | `canceling` state ≠ use prohibited |
| I-004 | Entitlement ≠ Feature Flag |
| I-005 | AppId ≠ ProductScope |
| I-006 | AppId ≠ Process |
| I-007 | App ≠ Installation ≠ Instance |
| I-008 | Instance ≠ Window |
| I-009 | AppId ≠ InstanceId |
| I-010 | Growth Analytics ≠ Entitlement ≠ Billing ≠ Policy |
| I-011 | Provider Cost Ledger ≠ Customer Credit Ledger ≠ Payment/Revenue Ledger |
| I-012 | Reserved Credits ≠ Charged Credits |
| I-013 | Budget ≠ Entitlement |
| I-014 | AI Billing Workspace ≠ Conversation Storage Scope |
| I-015 | **Retired by P2-006:** Cloud BYOK and Local BYOK are both excluded, with no customer credential types or routes required. |
| I-016 | Cloud Account Restriction ≠ Local Data Confiscation |
| I-017 | ArcForges Cloud Agent ≠ free VPS |

### 7.2 Product boundaries and ownership

| # | Invariant |
|---|---|
| I-020 | Reference ≠ Ownership |
| I-021 | Shared Experience ≠ Shared Shell ≠ Shared Domain |
| I-022 | Shared Foundation ≠ Shared Domain |
| I-023 | Task Owner ≠ Execution Location |
| I-024 | Actor ≠ Executor ≠ Caller Instance ≠ Identity |
| I-025 | App Version ≠ Contract Version |
| I-026 | Semantic Contract ≠ Wire Contract |
| I-027 | Mobile/Web Companion ≠ Professional-app Mobile/Web port |
| I-028 | Native ArcNotes editor/working cache ≠ WebView shell; acknowledged Cloud revision ≠ pending local edit |
| I-029 | ArcScope Report ≠ ArcNotes Document |
| I-030 | Product AI surface ≠ agent runtime; all products use the single Cloud harness |
| I-031 | ArcChat Federated Search ≠ a central ArcForges database |
| I-032 | Upstream product reference ≠ ArcSlate runtime architecture |

### 7.3 Capability, context and resource

| # | Invariant |
|---|---|
| I-040 | Capability ≠ Action |
| I-041 | Capability ≠ UI Command |
| I-042 | Capability ≠ Permission |
| I-043 | Action ≠ Capability Invocation |
| I-044 | Capability ≠ Package |
| I-045 | Static Capability ≠ Runtime Capability Availability |
| I-046 | Context ≠ Resource |
| I-047 | Context Provider ≠ Search Engine |
| I-048 | Context Provider ≠ Resource Database |
| I-049 | Context Freeze ≠ copy all data |
| I-050 | Current Selection ≠ durable Resource Identity |
| I-051 | ResourceRef ≠ Resource Content |
| I-052 | ResourceRef ≠ File Path |
| I-053 | ResourceRef ≠ Capability Token |
| I-054 | ResourceRef ≠ Permission Token |
| I-055 | ResourceRef ≠ universal domain entity |
| I-056 | ResourceRef ≠ Resource Selection |
| I-057 | ResourceRef ≠ Search Result |
| I-058 | Artifact ≠ Resource |
| I-059 | ArtifactRef ≠ ResourceRef |
| I-077 | ArtifactRef ≠ Permission Token |
| I-060 | Artifact Preview ≠ Artifact Authority |
| I-061 | Cloud Artifact Copy ≠ source professional resource |
| I-062 | Deep Link ≠ Command |
| I-063 | Deep Link ≠ Permission Token |
| I-064 | Event ≠ Command |
| I-065 | Event ≠ Realtime Signal |
| I-066 | Realtime Event Delivery ≠ Persistent Truth |
| I-067 | Health ≠ Presence |
| I-068 | Presence ≠ Readiness |
| I-069 | Health ≠ Compatibility |
| I-070 | Health ≠ Trust |
| I-071 | Health ≠ Capability Availability |
| I-072 | Compatibility ≠ Feature Flag |
| I-073 | InvocationId ≠ CommandId |
| I-074 | Invocation ≠ Task Step |
| I-075 | TaskHandle ≠ RPC Connection |
| I-076 | MCP Resource ≠ ArcForges Resource |

### 7.4 Execution and agent model

| # | Invariant |
|---|---|
| I-080 | Intent ≠ Task |
| I-081 | Task ≠ Run |
| I-082 | Run ≠ Step |
| I-083 | Step ≠ Attempt |
| I-084 | Step ≠ Capability Invocation |
| I-085 | AttemptId ≠ CommandId |
| I-086 | Task Retry ≠ Step Retry |
| I-087 | Retry ≠ Resume |
| I-088 | Retry ≠ Run Again |
| I-089 | Pause ≠ Waiting |
| I-090 | Waiting ≠ Interrupted |
| I-091 | Needs Attention ≠ Task State |
| I-092 | Cancel Requested ≠ Canceled |
| I-093 | Succeeded ≠ no exception |
| I-094 | Canceled ≠ no side effects |
| I-095 | Checkpoint ≠ Undo |
| I-096 | Compensation ≠ Transaction Rollback |
| I-097 | Approval ≠ Permission Grant |
| I-098 | Approval ≠ Steering |
| I-099 | Steering ≠ Conversation Message |
| I-100 | Automation ≠ Task |
| I-101 | Automation Occurrence ≠ Task Retry |
| I-102 | Trigger Definition ≠ Trigger Occurrence |
| I-103 | Automation Disable ≠ cancel running Task |
| I-104 | Automation Concurrency ≠ Step Parallelism |
| I-105 | Hybrid tool locality ≠ additional agent runtime |
| I-106 | Progress Event ≠ Task Authority |
| I-107 | Operational Trace ≠ Chain-of-Thought |
| I-108 | Conversation ≠ Task |
| I-109 | Message ≠ Tool Call |
| I-110 | Attachment ≠ Context Reference |
| I-111 | Input Attachment ≠ Artifact |
| I-112 | Agent Profile ≠ Running Agent |
| I-113 | Agent Profile ≠ Model |
| I-114 | Agent Profile ≠ running agent; external-agent execution is excluded |
| I-115 | Provider ≠ Model |
| I-116 | Provider ≠ AI Source |
| I-117 | Chat Mode ≠ no tools |
| I-118 | Agent Mode ≠ unlimited permission |
| I-119 | Task Creation Authorization ≠ lifetime authorization |
| I-120 | Remote Task ≠ Remote Desktop |
| I-121 | Cloud Agent Task ≠ native Product Job |
| I-122 | Remote Task ≠ Cloud-only Task |
| I-123 | Conversation Sync ≠ Remote Task State |
| I-124 | Unsent local draft ≠ acknowledged Cloud conversation |
| I-125 | Continuity ≠ mirroring UI |

### 7.5 Knowledge, search and retrieval

| # | Invariant |
|---|---|
| I-130 | Knowledge Source ≠ Data Copy |
| I-131 | Knowledge Source ≠ Context Provider |
| I-132 | Knowledge Source ≠ Import |
| I-133 | Knowledge Scope ≠ Index Scope |
| I-134 | Index ≠ Canonical Data |
| I-135 | Search Index ≠ Knowledge Authority |
| I-136 | Search Index ≠ User Data Authority |
| I-137 | Knowledge Index ≠ Document Copy |
| I-138 | Semantic Index ≠ Knowledge |
| I-139 | Embedding ≠ Permission |
| I-140 | Cloud Sync ≠ Cloud Index |
| I-141 | Cloud Index ≠ AI Retrieval |
| I-142 | Cloud Search ≠ Cloud AI Indexing |
| I-143 | AI Retrieval ≠ Managed AI Processing |
| I-144 | Exclude from AI ≠ Exclude from Search |
| I-145 | Keyword Search ≠ Semantic Search |
| I-146 | Search ≠ Retrieval |
| I-147 | Search ≠ Ask AI |
| I-148 | Web Search ≠ ArcChat Global Search |
| I-149 | Web Search ≠ long-term knowledge |
| I-150 | Retrieval Candidate ≠ Evidence |
| I-151 | Evidence ≠ Citation |
| I-152 | Search Result ≠ Citation |
| I-153 | Citation ≠ Vector Chunk ID |
| I-154 | Retrieval Unit ≠ Domain Resource |
| I-155 | Context Pack ≠ entire Knowledge Source |
| I-156 | ArcNotes Knowledge ≠ ArcChat Memory |
| I-157 | Personal Memory ≠ ArcNotes Knowledge |
| I-158 | Conversation Summary ≠ Personal Memory |
| I-159 | Conversation Context ≠ long-term knowledge |
| I-160 | Raw Capture ≠ text knowledge chunk |
| I-161 | Raw Video ≠ default vector corpus |
| I-162 | AI Summary ≠ Source Evidence |
| I-163 | AI Summary ≠ Measurement Result |
| I-164 | Derived Knowledge Artifact ≠ Original Source |
| I-165 | Source Revision ≠ Index Revision |
| I-166 | Index Freshness ≠ Source Freshness |
| I-167 | Retrieval Trace ≠ Chain-of-Thought |
| I-168 | Source Removal ≠ delete files |
| I-169 | Search ranking ≠ paid placement |

### 7.6 Data, sync, formats and recovery

| # | Invariant |
|---|---|
| I-180 | Sync ≠ Backup ≠ Version History ≠ Trash ≠ Export |
| I-181 | User Data ≠ Asset ≠ Cache ≠ Search Index ≠ Secret |
| I-182 | Sync ≠ AI upload; sync transmission ≠ AI transmission |
| I-183 | Domain Model ≠ Database Schema |
| I-184 | Database Schema ≠ Native File Format |
| I-185 | Native Format ≠ Interchange Format |
| I-186 | Native Format ≠ Cloud Sync Protocol |
| I-187 | Runtime Storage Format ≠ User Interchange Format |
| I-188 | Working Store ≠ Portable Package |
| I-189 | Project ≠ single file |
| I-190 | Document ≠ Markdown file; Canonical Document ≠ Markdown file |
| I-191 | Raw Capture ≠ Analysis Result |
| I-192 | MediaAsset ≠ File Path |
| I-193 | Managed Asset ≠ External Reference |
| I-194 | External Locator ≠ Resource Identity |
| I-195 | File Path ≠ Resource Identity |
| I-196 | Cache ≠ Canonical Data |
| I-197 | Proxy ≠ Original |
| I-198 | Autosave ≠ rewrite entire project |
| I-199 | Saved Locally ≠ Synced to Cloud |
| I-200 | Cloud Pending ≠ Unsaved |
| I-201 | Undo ≠ Revision |
| I-202 | Undo ≠ Revision History |
| I-203 | Revision ≠ Checkpoint |
| I-204 | Checkpoint ≠ Recovery Journal |
| I-205 | Revision History ≠ Trash |
| I-206 | Crash Recovery ≠ Undo |
| I-207 | Migration Recovery ≠ user Undo; Migration Recovery Point ≠ normal Undo |
| I-208 | App Binary Rollback ≠ Data Rollback |
| I-209 | Import ≠ live external sync |
| I-210 | Export ≠ Backup |
| I-211 | Repository Projection ≠ Runtime Authority |
| I-212 | Repository Projection ≠ Live Working Store |
| I-213 | Git Merge ≠ Collaboration Protocol |
| I-214 | Git Versioning ≠ Cloud Sync |
| I-215 | Resource Delete ≠ Managed Blob garbage collection |
| I-216 | Native Package ≠ Trusted Input |
| I-217 | CLR Type ≠ persistent format contract |
| I-218 | ETag ≠ ArcForges Content Hash |
| I-219 | High Durability ≠ Backup |
| I-220 | Permanent user deletion ≠ same-day disappearance from every disaster backup |
| I-221 | Read compatibility ≠ safe write compatibility |
| I-222 | Cache Recovery ≠ Canonical Data Recovery |
| I-223 | Projection Repair ≠ Canonical Data Repair |
| I-224 | Project Reference ≠ Resource Copy |

### 7.7 Security, permission and trust

| # | Invariant |
|---|---|
| I-230 | Identity ≠ Actor ≠ Executor ≠ Caller Process |
| I-231 | App Identity ≠ Human Authority |
| I-232 | Agent Profile ≠ Security Principal |
| I-233 | Agent Capability Configuration ≠ Permission |
| I-234 | Automation ≠ Principal |
| I-235 | Automation Definition ≠ Automation Principal |
| I-236 | Automation Creator Permission Snapshot ≠ permanent authority |
| I-237 | Role ≠ Permission |
| I-238 | Capability Permission ≠ Resource Authorization |
| I-239 | Permission ≠ Approval |
| I-240 | Permission Grant ≠ Approval |
| I-241 | Approval ≠ Persistent Grant |
| I-242 | Approval ≠ Step-up Authentication; Step-up ≠ Approval |
| I-243 | Remote Approval ≠ Local Presence |
| I-244 | Trust ≠ Permission |
| I-245 | Trust ≠ Risk |
| I-246 | Trust ≠ Entitlement |
| I-247 | Package Signature ≠ Safety |
| I-248 | Verified Publisher ≠ Unlimited Access; Verified Publisher ≠ safe capability |
| I-249 | First-party ≠ Unlimited Access |
| I-250 | Device Presence ≠ Device Trust |
| I-251 | Device Online ≠ Remote Agent Enabled |
| I-252 | Registered Device ≠ Remote-authorized Device |
| I-253 | Knowledge Eligibility ≠ Read Permission |
| I-254 | Read Permission ≠ Data Egress Permission |
| I-255 | Synced Data ≠ allowed external transmission |
| I-256 | SecretRef ≠ Secret Value |
| I-257 | Secret Use ≠ Secret Reveal |
| I-258 | Secret Permission ≠ general Settings permission |
| I-259 | Extension Isolation ≠ Authorization |
| I-260 | Out-of-process ≠ automatically safe |
| I-261 | MCP Protocol ≠ Trust |
| I-262 | MCP Tool Description ≠ Trusted Instruction |
| I-263 | Retrieved Content ≠ Security Instruction |
| I-264 | Skill Guidance ≠ Permission Grant |
| I-265 | Workflow Definition ≠ Authorization |
| I-266 | Delegation ≠ Privilege Amplification |
| I-267 | Permission Revocation ≠ Undo |
| I-268 | Revocation ≠ Compensation |
| I-269 | Declared Permission ≠ Granted Permission |
| I-270 | Installation ≠ authorize all operations |
| I-271 | Developer Mode ≠ permission bypass ≠ secret bypass ≠ workspace-policy bypass |
| I-272 | Audit ≠ Debug Log |
| I-273 | Audit ≠ Telemetry |
| I-274 | Audit ≠ Domain Revision History; Audit ≠ Product History |
| I-275 | Audit ≠ Task Operational Trace |
| I-276 | Diagnostic Log ≠ Audit |
| I-277 | App Lock ≠ Account Authentication |
| I-278 | Mobile Biometric Unlock ≠ high-risk authorization |
| I-279 | HTTPS Private Link ≠ Public Share Link |
| I-280 | Search ≠ Remote Desktop scan |
| I-281 | Stage-25 Product Policy ≠ Stage-26 Authorization |

### 7.8 Extensions, packages and interoperability

| # | Invariant |
|---|---|
| I-290 | Skill ≠ Capability |
| I-291 | Skill ≠ Extension Code |
| I-292 | Skill ≠ MCP |
| I-293 | Template ≠ Skill |
| I-294 | Template ≠ live parent resource |
| I-295 | Workflow ≠ Automation |
| I-296 | Workflow ≠ Task |
| I-297 | Workflow ≠ Agent Plan |
| I-298 | Workflow ≠ arbitrary script runtime |
| I-299 | Automation ≠ Workflow |
| I-300 | Package ≠ Contribution |
| I-301 | Package Version ≠ Protocol Version |
| I-302 | Package Version ≠ App Version |
| I-303 | Install ≠ Enable |
| I-304 | Install ≠ Permission Grant |
| I-305 | Compatibility ≠ Trust |
| I-306 | Compatibility ≠ Enablement |
| I-307 | MCP ≠ native Arc capability |
| I-308 | MCP ≠ Connector |
| I-309 | MCP Definition ≠ MCP Connection |
| I-310 | MCP Prompt ≠ Skill |
| I-311 | Connector ≠ Connection |
| I-312 | Connector ≠ imported snapshot |
| I-313 | **Retired by P2-006:** external-agent integration is excluded, not a separate agent-profile implementation. |
| I-314 | **Retired by P2-006:** no external-agent task/delegation adapter is required. |
| I-315 | ACP Session ≠ Conversation |
| I-316 | ACP ≠ ArcChat runtime model |
| I-317 | Extension ≠ third-party Arc App |
| I-318 | Extension Process ≠ Host Process |
| I-319 | Extension Private State ≠ Product Domain State |
| I-320 | Extension Capability ≠ Permission |
| I-321 | Third-party Package ≠ runtime DLL injection |
| I-322 | Runtime Extension ≠ NuGet package restore |
| I-323 | Catalog ≠ Marketplace |
| I-324 | Catalog ≠ runtime dependency |
| I-325 | Community Package ≠ automatically trusted |
| I-326 | Package Dependency ≠ Capability Dependency |
| I-327 | Public SDK Contract ≠ internal LocalRpc Contract |
| I-328 | Extension Schema ≠ `Dictionary<string, object>` |
| I-329 | Dynamic Extension Boundary ≠ core product capability protocol |
| I-330 | Deprecate ≠ Revoke |

### 7.9 Policy and configuration

| # | Invariant |
|---|---|
| I-340 | Policy ≠ Setting |
| I-341 | Policy ≠ Entitlement |
| I-342 | Policy ≠ Permission |
| I-343 | Policy ≠ Runtime Health |
| I-344 | Policy ≠ Domain State |
| I-345 | Policy Control Plane ≠ request Data Plane |
| I-346 | Policy Scope ≠ Entitlement Scope |
| I-347 | Feature ≠ Feature Flag |
| I-348 | Feature Flag ≠ Rollout |
| I-349 | Rollout ≠ Experiment |
| I-350 | Experiment ≠ Entitlement |
| I-351 | Experiment ≠ Security Policy |
| I-352 | Experiment Assignment ≠ random every request |
| I-353 | Kill Switch ≠ Feature Lifecycle |
| I-354 | Kill Switch ≠ delete data |
| I-355 | Remote Config ≠ User Preference |
| I-356 | Remote Config ≠ arbitrary code |
| I-357 | Remote Config ≠ Project Format |
| I-358 | Remote Config ≠ transport selection |
| I-359 | Compatibility Policy ≠ Capability Negotiation |
| I-360 | Minimum Cloud Version ≠ Minimum Local Data Version |
| I-361 | Provider Availability ≠ Provider Health |
| I-362 | Model Availability ≠ Model Entitlement |
| I-363 | Model Availability ≠ Model Capability |
| I-364 | Recommended Model ≠ Pinned Model |
| I-365 | Workspace Policy ≠ Workspace Permission |
| I-366 | Policy Bundle ≠ live mutable database view |
| I-367 | Policy Push Event ≠ Policy Authority |
| I-368 | Last Known Good ≠ current cloud truth |
| I-369 | Published Revision ≠ Draft |
| I-370 | Policy Rollback ≠ rewrite history |
| I-371 | Dynamic Policy ≠ Architecture Constitution |
| I-372 | Dynamic Policy ≠ business-logic deployment |

### 7.10 Quality, compatibility and platform

| # | Invariant |
|---|---|
| I-380 | Fast in Debug ≠ Fast in Production |
| I-381 | JIT test pass ≠ AOT compatibility |
| I-382 | Build success ≠ runtime compatibility |
| I-383 | App Version ≠ Contract Version |
| I-384 | Contract Compatibility ≠ Product Policy Availability |
| I-385 | Read Compatibility ≠ Write Compatibility |
| I-386 | Migration Success ≠ Data Semantic Preservation |
| I-387 | Crash-free ≠ Recoverable |
| I-388 | Small Benchmark ≠ Scale Reliability |
| I-389 | Startup Time ≠ Time To Usable |
| I-390 | Managed Heap ≠ Total Memory |
| I-391 | Process Running ≠ Healthy |
| I-392 | Responsive Animation ≠ Responsive Product |
| I-393 | Accessible Color ≠ Accessible Product |
| I-394 | Keyboard Shortcut ≠ Keyboard Accessibility |
| I-395 | Localized UI ≠ Locale-safe Data |
| I-396 | Display Unit ≠ Canonical Quantity |
| I-397 | Automated Test ≠ real-hardware validation |
| I-398 | One OS passing ≠ cross-platform support |
| I-399 | Diagnostics ≠ Telemetry Consent |
| I-400 | Performance Target ≠ Marketing Claim |
| I-401 | Quality Waiver ≠ permanently lower standard |
| I-402 | Quality Requirement ≠ Engineering Suggestion |
| I-403 | SLO ≠ external SLA |
| I-404 | Focus ≠ Selection |
| I-405 | Push Notification ≠ Durable Attention State |

### 7.11 Support, operations and trust & safety

| # | Invariant |
|---|---|
| I-410 | Feedback ≠ Support Case |
| I-411 | Bug Report ≠ Engineering Defect |
| I-412 | Feature Request ≠ Product Commitment |
| I-413 | Known Issue ≠ Incident |
| I-414 | Incident ≠ Security Advisory |
| I-415 | Support ≠ Impersonation |
| I-416 | Operator ≠ User |
| I-417 | Operator Role ≠ unlimited access |
| I-418 | Support Access ≠ User Session |
| I-419 | Support Access ≠ permanent permission |
| I-420 | Break Glass ≠ Impersonation |
| I-421 | Break Glass ≠ global superuser |
| I-422 | Operator Console ≠ Database Console |
| I-423 | Operator Console ≠ Domain Owner |
| I-424 | Diagnostic Bundle ≠ automatic telemetry upload |
| I-425 | Diagnostic Bundle ≠ Recovery Package |
| I-426 | Recovery ≠ direct SQL mutation |
| I-427 | Recovery ≠ silent overwrite |
| I-428 | Recovery ≠ guaranteed recovery of missing data |
| I-429 | Report ≠ Investigation ≠ Enforcement ≠ Appeal |
| I-430 | Community Report ≠ Enforcement |
| I-431 | Report Count ≠ Guilt |
| I-432 | Delist ≠ Revoke |
| I-433 | Publisher Yank ≠ platform enforcement |
| I-434 | Package Revocation ≠ delete user project |
| I-435 | Package Revocation ≠ delete created resources |
| I-436 | Copyright Removal ≠ delete local canonical data |
| I-437 | Public Share Removal ≠ delete private source |
| I-438 | Account Cloud Restriction ≠ local data lock |
| I-439 | Appeal ≠ delete enforcement history |
| I-440 | Security Report ≠ public bug report |
| I-441 | Security Advisory ≠ Kill Switch |
| I-442 | Security Advisory ≠ Package Revocation |
| I-443 | Official Advisory ≠ self-host policy authority; Advisory ≠ remote policy authority |
| I-444 | Staff Access ≠ Secret Access |
| I-445 | Support Attachment ≠ product resource authority |
| I-446 | Audit ≠ operator-editable history |
| I-447 | Data exists in the Cloud ≠ support has the right to browse it |
| I-448 | Archive ≠ Delete |

### 7.12 Product-local invariants

| # | Invariant |
|---|---|
| I-460 | Notebook ≠ Workspace; Folder ≠ Tag; Document ≠ File; Block ≠ Markdown Line |
| I-461 | Note ≠ a second content model independent of Document |
| I-462 | Property ≠ Document Content; Saved View ≠ Ownership |
| I-463 | Attachment ≠ embedded base64 |
| I-464 | ArcNotes Checklist Item ≠ ArcChat Agent Task |
| I-465 | ArcScope Project ≠ ArcForges Workspace |
| I-466 | Device ≠ DataSource; ConnectionProfile ≠ Connection |
| I-467 | Session ≠ Connection; Session ≠ Capture |
| I-468 | Channel ≠ Signal; Signal ≠ Event; Raw Signal ≠ Derived Signal |
| I-469 | Live View ≠ Recording; Pause View ≠ Pause Capture |
| I-470 | Display Decimation ≠ Measurement Data |
| I-471 | Measurement ≠ Analysis; Decoder Output ≠ Raw Data |
| I-472 | Annotation ≠ data mutation; Comparison ≠ Merge |
| I-473 | Source Profile ≠ historical Session configuration |
| I-474 | ArcScope Cloud Sync ≠ raw capture upload |
| I-475 | View ≠ Signal Ownership |
| I-476 | ArcSlate Project ≠ Sequence; Project ≠ Media Folder |
| I-477 | Source Media ≠ Timeline Clip; Clip ≠ Source Media; MediaAsset ≠ Clip |
| I-478 | Source Time ≠ Timeline Time; Video Frame Time ≠ Audio Sample Time |
| I-479 | Playback ≠ final render; Preview Quality ≠ Export Quality |
| I-480 | Viewer frame drop ≠ source data loss; dropped preview frame ≠ dropped media data |
| I-481 | Transition ≠ random clip overlap state |
| I-482 | Effect Definition ≠ Effect Instance; Effect Stack ≠ separate effect engine |
| I-483 | Node Graph ≠ arbitrary script runtime; Keyframe ≠ current parameter value |
| I-484 | Proxy ≠ Render Cache; Render Cache ≠ Project Authority |
| I-485 | Native Render Job ≠ Cloud Agent Task ≠ UI progress dialog; Rendered Artifact ≠ ArcSlate Project |
| I-486 | Transcript ≠ Subtitle; AI Analysis ≠ Timeline Edit |
| I-487 | Agent Context ≠ media upload; Project Sync ≠ original media upload |
| I-488 | External Media ≠ Managed Media |
| I-489 | ArcSlate Link ≠ shared identity |
| I-490 | ArcSlate Sequence ≠ Timeline Clip |

---

### 7.13 P2-006 scope and accounting invariants

| # | Invariant |
|---|---|
| I-491 | Model loop location ≠ tool execution location |
| I-492 | Actual measured tokens ≠ estimated tokens; cumulative stream usage ≠ per-event delta |
| I-493 | Included recoverable capacity ≠ purchased credits ≠ supplier cost ≠ subscription payment |
| I-494 | Current configuration ≠ historical pricing snapshot; changing configuration ≠ resetting customer balances |
| I-495 | Open executable policy logic ≠ private deployment values; secret mount ≠ customer BYOK |
| I-496 | Synthetic capture ≠ hardware evidence; preview sample ≠ canonical simulation data |
| I-497 | OTIO interchange ≠ ArcSlate working project ≠ embedded source media |
| I-498 | Evictable acknowledged cache ≠ unacknowledged edits/uploads/tool receipts |

---

## 8. Forbidden aliases and obsolete terms

| Forbidden / obsolete | Reason | Use instead |
|---|---|---|
| `ArcCanvas`, `ArcMusic`, `ArcImage`, `ArcVideo` | `SUPERSEDED` product names (**D-002**) | No replacement canvas/slides product or capability; nothing; `ArcScope`; `ArcSlate` |
| "Workspace" meaning a panel layout | Collides with the cloud tenancy boundary | **Layout** |
| Bare "Project" in cross-product text | Three incompatible product meanings | `ArcChat.Project` / `ArcScope.Project` / `ArcSlate.Project` |
| Bare "Scope" | Eight distinct meanings exist | Name the scope explicitly: Knowledge Scope, Sync Scope, Permission Scope, Policy Scope, Product Scope, Search Scope, Egress Scope, Resource Scope |
| "ArcForges Suite 2.0" as a version | No mandatory suite release train (Stage 13 §55) | Per-product versions plus an optional release campaign name |
| "Central desktop service", `ArcForgesService.exe` | Prohibited architecture (Stage 13 §8, §49) | ArcChat-hosted Hub |
| Unqualified "Unlimited AI" / "unlimited storage" | Prohibited unbounded commercial claims | Disclosed AI capacity recovery/rate/concurrency/model limits and storage tier |
| "Native AOT" applied to Android production builds | Conflates Mono AOT with CoreCLR Native AOT (**D-008**, V-04) | ".NET 10 Mono AOT" |
| "Cloud must publish as Native AOT" | Removed by **D-008** | "Cloud is an ASP.NET Core JIT modular monolith" |
| "SignalR is unsupported under Native AOT" | Stale .NET 8 statement (V-03) | "SignalR has Partial support under .NET 10 Native AOT" |
| Waffo Pancake and every Waffo-specific mechanic | `SUPERSEDED` provider (**D-005**) | Paddle (MoR) and Payoneer (payout destination) |
| "License key unlock" in ArcChat Mobile | Prohibited by Apple 3.1.1 and **D-022** | Cloud-resolved entitlement |
| `InvokeAsync(string, object)` / `Dictionary<string,object>` capability calls | Bypasses contracts, permissions and versioning (I3 §8.1) | Strongly typed capability interfaces |
| `ArcForges.Foundation.Document`, `.VideoTimeline`, `.TelemetrySession` | Shared foundation must not hold domain (Stage 13 §32) | Product-owned domain types |
| `ArcProductBase` domain hierarchy | Product classification is not inheritance (Stage 13 §85) | Independent domains + platform contracts |

---

## 9. MCP disambiguation (V-02)

The Model Context Protocol `2026-07-28` revision is a **stable** specification with a formal extensions framework that defines its own `Task` and `Skill` concepts. These collide with the ArcForges execution vocabulary and must be disambiguated explicitly wherever both appear.

| MCP term | ArcForges term | Relationship |
|---|---|---|
| `MCP.Task` | `ArcForges.Task` | **Unrelated.** An MCP task is a protocol-level unit of work at an MCP server. An ArcForges Task is a durable, owned, auditable unit in the ArcForges execution model. An MCP task never becomes an ArcForges Task implicitly; if one is created, it is created explicitly, owned by the Cloud agent module, and carries its own `TaskId`. |
| `MCP.Skill` | `ArcChat.Skill` | **Unrelated.** MCP skills are server-published behaviour packs. `ArcChat.Skill` is ArcChat-owned configuration. An MCP skill never becomes an `ArcChat.Skill`; it is surfaced as a capability contribution subject to the ordinary trust and permission model. |
| `MCP.Resource` | `ArcForges.Resource` | **Distinct.** `I-076`, `I-341`. An MCP resource is addressed by the MCP server's own scheme and is never an ArcForges `ResourceRef`. |
| `MCP.Prompt` | `ArcChat.Skill` | **Distinct** (`I-310`). |
| MCP statelessness | `Session` | The `2026-07-28` core is stateless: `initialize`/`initialized` removed, `Mcp-Session-Id` eliminated, capability negotiation moved per-request. ArcForges must not build session identity on MCP transport state. This is consistent with `Session ≠ Connection`. |
| MCP Multi Round-Trip Requests (MRTR) | Callback contracts | Server-to-client requests are restructured through MRTR. This is a transport mechanism, not an ArcForges execution concept. |

MCP tool descriptions, prompts, resource contents and server metadata are **untrusted data**, never instructions (`I-262`, `I-263`).

---

## 10. Enforcement

The glossary is enforced, not merely published.

| Control | Mechanism | Where specified |
|---|---|---|
| Forbidden term scan | Repository-policy test failing the build on any forbidden alias or obsolete product name in `src/`, `docs/` (excluding `docs/inputs/`), identifiers and resource strings | [`../assurance/testing-and-verification-strategy.md`](../assurance/testing-and-verification-strategy.md) |
| Invariant traceability | Every invariant maps to at least one architecture rule, one test, and one work-package completion gate | [`../assurance/traceability-matrix.md`](../assurance/traceability-matrix.md) |
| Namespaced-term enforcement | Architecture tests asserting product-owned types are not lifted into shared foundation namespaces | [`../architecture/01-solution-and-project-layout.md`](../architecture/01-solution-and-project-layout.md) |
| Glossary change control | A new canonical term, a changed definition, or a retired invariant requires a decision record in `docs/decisions/` | **D-018** |

---

## 11. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 1, 3, 4, 9, 13–28` | The `X ≠ Y` invariant corpus (589 marked lines reduced to the catalogue in §7) |
| `I4 §Stage 21` | Cross-application semantic vocabulary (App, Instance, Capability, Action, Context, Artifact, ResourceRef, Deep Link, Event, Health, Invocation, Compatibility) |
| `I4 §Stage 19` | Intent / Task / Run / Step / Attempt / Approval / Steering / Automation model |
| `I4 §Stage 27` | Quality invariants (§7.10) |
| `I3 §4`, `§6`, `§13`, `§14` | Wire/domain/storage separation, TaskHandle, ResourceRef |
| **D-018** | The requirement that this document exists and gates detailed specification |
| **V-02** | The MCP term-collision requirement discharged in §9 |
