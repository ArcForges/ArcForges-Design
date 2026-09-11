# ArcForges Normative Glossary and Invariant Catalogue
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements — cross-cutting, consumed by every requirements, architecture, assurance and planning document
> Governs: **[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** vocabulary and **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** term disambiguation. Earlier coverage evidence must be reconciled to [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) before the revised requirements claim closure.
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
| **Organization** | retired | Excluded by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): no organization, team, membership, invitation or collaboration-specific schema reservation. |
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

The simulator additionally defines Cloud-owned **SimulationDefinition**, immutable **ScenarioVersion**, non-agent **SimulationRun**, immutable **SimulationSegment** and ordered **SimulationEvent**. [SIM-01](products/arcscope.md#rule-sim-01)–[SIM-20](products/arcscope.md#rule-sim-20) in the ArcScope requirements govern these objects; synthetic provenance is mandatory.

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

Every active entry is binding where its concepts are in current product scope. A distinction does not itself require an excluded feature or a dedicated table/type for an otherwise unnecessary concept. Retired rows retain IDs for historical traceability and create no delivery obligation. [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) changes invalidate prior unchanged-coverage claims; downstream mappings must be reconciled before Stage 2 closes.

### 7.1 Identity, tenancy and commerce

| # | Invariant |
|---|---|
| <a id="rule-i-001"></a>I-001 | User ≠ Workspace ≠ Device ≠ Session ≠ Subscription ≠ Entitlement |
| <a id="rule-i-002"></a>I-002 | Subscription cancellation ≠ Account deletion |
| <a id="rule-i-003"></a>I-003 | `canceling` state ≠ use prohibited |
| <a id="rule-i-004"></a>I-004 | Entitlement ≠ Feature Flag |
| <a id="rule-i-005"></a>I-005 | AppId ≠ ProductScope |
| <a id="rule-i-006"></a>I-006 | AppId ≠ Process |
| <a id="rule-i-007"></a>I-007 | App ≠ Installation ≠ Instance |
| <a id="rule-i-008"></a>I-008 | Instance ≠ Window |
| <a id="rule-i-009"></a>I-009 | AppId ≠ InstanceId |
| <a id="rule-i-010"></a>I-010 | Growth Analytics ≠ Entitlement ≠ Billing ≠ Policy |
| <a id="rule-i-011"></a>I-011 | Provider Cost Ledger ≠ Customer Credit Ledger ≠ Payment/Revenue Ledger |
| <a id="rule-i-012"></a>I-012 | Reserved Credits ≠ Charged Credits |
| <a id="rule-i-013"></a>I-013 | Budget ≠ Entitlement |
| <a id="rule-i-014"></a>I-014 | AI Billing Workspace ≠ Conversation Storage Scope |
| <a id="rule-i-015"></a>I-015 | **Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006):** Cloud BYOK and Local BYOK are both excluded, with no customer credential types or routes required. |
| <a id="rule-i-016"></a>I-016 | Cloud Account Restriction ≠ Local Data Confiscation |
| <a id="rule-i-017"></a>I-017 | ArcForges Cloud Agent ≠ free VPS |

### 7.2 Product boundaries and ownership

| # | Invariant |
|---|---|
| <a id="rule-i-020"></a>I-020 | Reference ≠ Ownership |
| <a id="rule-i-021"></a>I-021 | Shared Experience ≠ Shared Shell ≠ Shared Domain |
| <a id="rule-i-022"></a>I-022 | Shared Foundation ≠ Shared Domain |
| <a id="rule-i-023"></a>I-023 | Task Owner ≠ Execution Location |
| <a id="rule-i-024"></a>I-024 | Actor ≠ Executor ≠ Caller Instance ≠ Identity |
| <a id="rule-i-025"></a>I-025 | App Version ≠ Contract Version |
| <a id="rule-i-026"></a>I-026 | Semantic Contract ≠ Wire Contract |
| <a id="rule-i-027"></a>I-027 | Mobile/Web Companion ≠ Professional-app Mobile/Web port |
| <a id="rule-i-028"></a>I-028 | Native ArcNotes editor/working cache ≠ WebView shell; acknowledged Cloud revision ≠ pending local edit |
| <a id="rule-i-029"></a>I-029 | ArcScope Report ≠ ArcNotes Document |
| <a id="rule-i-030"></a>I-030 | Product AI surface ≠ agent runtime; all products use the single Cloud harness |
| <a id="rule-i-031"></a>I-031 | ArcChat Federated Search ≠ a central ArcForges database |
| <a id="rule-i-032"></a>I-032 | Upstream product reference ≠ ArcSlate runtime architecture |

### 7.3 Capability, context and resource

| # | Invariant |
|---|---|
| <a id="rule-i-040"></a>I-040 | Capability ≠ Action |
| <a id="rule-i-041"></a>I-041 | Capability ≠ UI Command |
| <a id="rule-i-042"></a>I-042 | Capability ≠ Permission |
| <a id="rule-i-043"></a>I-043 | Action ≠ Capability Invocation |
| <a id="rule-i-044"></a>I-044 | Capability ≠ Package |
| <a id="rule-i-045"></a>I-045 | Static Capability ≠ Runtime Capability Availability |
| <a id="rule-i-046"></a>I-046 | Context ≠ Resource |
| <a id="rule-i-047"></a>I-047 | Context Provider ≠ Search Engine |
| <a id="rule-i-048"></a>I-048 | Context Provider ≠ Resource Database |
| <a id="rule-i-049"></a>I-049 | Context Freeze ≠ copy all data |
| <a id="rule-i-050"></a>I-050 | Current Selection ≠ durable Resource Identity |
| <a id="rule-i-051"></a>I-051 | ResourceRef ≠ Resource Content |
| <a id="rule-i-052"></a>I-052 | ResourceRef ≠ File Path |
| <a id="rule-i-053"></a>I-053 | ResourceRef ≠ Capability Token |
| <a id="rule-i-054"></a>I-054 | ResourceRef ≠ Permission Token |
| <a id="rule-i-055"></a>I-055 | ResourceRef ≠ universal domain entity |
| <a id="rule-i-056"></a>I-056 | ResourceRef ≠ Resource Selection |
| <a id="rule-i-057"></a>I-057 | ResourceRef ≠ Search Result |
| <a id="rule-i-058"></a>I-058 | Artifact ≠ Resource |
| <a id="rule-i-059"></a>I-059 | ArtifactRef ≠ ResourceRef |
| <a id="rule-i-077"></a>I-077 | ArtifactRef ≠ Permission Token |
| <a id="rule-i-060"></a>I-060 | Artifact Preview ≠ Artifact Authority |
| <a id="rule-i-061"></a>I-061 | Cloud Artifact Copy ≠ source professional resource |
| <a id="rule-i-062"></a>I-062 | Deep Link ≠ Command |
| <a id="rule-i-063"></a>I-063 | Deep Link ≠ Permission Token |
| <a id="rule-i-064"></a>I-064 | Event ≠ Command |
| <a id="rule-i-065"></a>I-065 | Event ≠ Realtime Signal |
| <a id="rule-i-066"></a>I-066 | Realtime Event Delivery ≠ Persistent Truth |
| <a id="rule-i-067"></a>I-067 | Health ≠ Presence |
| <a id="rule-i-068"></a>I-068 | Presence ≠ Readiness |
| <a id="rule-i-069"></a>I-069 | Health ≠ Compatibility |
| <a id="rule-i-070"></a>I-070 | Health ≠ Trust |
| <a id="rule-i-071"></a>I-071 | Health ≠ Capability Availability |
| <a id="rule-i-072"></a>I-072 | Compatibility ≠ Feature Flag |
| <a id="rule-i-073"></a>I-073 | InvocationId ≠ CommandId |
| <a id="rule-i-074"></a>I-074 | Invocation ≠ Task Step |
| <a id="rule-i-075"></a>I-075 | TaskHandle ≠ RPC Connection |
| <a id="rule-i-076"></a>I-076 | MCP Resource ≠ ArcForges Resource |

### 7.4 Execution and agent model

| # | Invariant |
|---|---|
| <a id="rule-i-080"></a>I-080 | Intent ≠ Task |
| <a id="rule-i-081"></a>I-081 | Task ≠ Run |
| <a id="rule-i-082"></a>I-082 | Run ≠ Step |
| <a id="rule-i-083"></a>I-083 | Step ≠ Attempt |
| <a id="rule-i-084"></a>I-084 | Step ≠ Capability Invocation |
| <a id="rule-i-085"></a>I-085 | AttemptId ≠ CommandId |
| <a id="rule-i-086"></a>I-086 | Task Retry ≠ Step Retry |
| <a id="rule-i-087"></a>I-087 | Retry ≠ Resume |
| <a id="rule-i-088"></a>I-088 | Retry ≠ Run Again |
| <a id="rule-i-089"></a>I-089 | Pause ≠ Waiting |
| <a id="rule-i-090"></a>I-090 | Waiting ≠ Interrupted |
| <a id="rule-i-091"></a>I-091 | Needs Attention ≠ Task State |
| <a id="rule-i-092"></a>I-092 | Cancel Requested ≠ Canceled |
| <a id="rule-i-093"></a>I-093 | Succeeded ≠ no exception |
| <a id="rule-i-094"></a>I-094 | Canceled ≠ no side effects |
| <a id="rule-i-095"></a>I-095 | Checkpoint ≠ Undo |
| <a id="rule-i-096"></a>I-096 | Compensation ≠ Transaction Rollback |
| <a id="rule-i-097"></a>I-097 | Approval ≠ Permission Grant |
| <a id="rule-i-098"></a>I-098 | Approval ≠ Steering |
| <a id="rule-i-099"></a>I-099 | Steering ≠ Conversation Message |
| <a id="rule-i-100"></a>I-100 | Automation ≠ Task |
| <a id="rule-i-101"></a>I-101 | Automation Occurrence ≠ Task Retry |
| <a id="rule-i-102"></a>I-102 | Trigger Definition ≠ Trigger Occurrence |
| <a id="rule-i-103"></a>I-103 | Automation Disable ≠ cancel running Task |
| <a id="rule-i-104"></a>I-104 | Automation Concurrency ≠ Step Parallelism |
| <a id="rule-i-105"></a>I-105 | Hybrid tool locality ≠ additional agent runtime |
| <a id="rule-i-106"></a>I-106 | Progress Event ≠ Task Authority |
| <a id="rule-i-107"></a>I-107 | Operational Trace ≠ Chain-of-Thought |
| <a id="rule-i-108"></a>I-108 | Conversation ≠ Task |
| <a id="rule-i-109"></a>I-109 | Message ≠ Tool Call |
| <a id="rule-i-110"></a>I-110 | Attachment ≠ Context Reference |
| <a id="rule-i-111"></a>I-111 | Input Attachment ≠ Artifact |
| <a id="rule-i-112"></a>I-112 | Agent Profile ≠ Running Agent |
| <a id="rule-i-113"></a>I-113 | Agent Profile ≠ Model |
| <a id="rule-i-114"></a>I-114 | Agent Profile ≠ running agent; external-agent execution is excluded |
| <a id="rule-i-115"></a>I-115 | Provider ≠ Model |
| <a id="rule-i-116"></a>I-116 | Provider ≠ AI Source |
| <a id="rule-i-117"></a>I-117 | Chat Mode ≠ no tools |
| <a id="rule-i-118"></a>I-118 | Agent Mode ≠ unlimited permission |
| <a id="rule-i-119"></a>I-119 | Task Creation Authorization ≠ lifetime authorization |
| <a id="rule-i-120"></a>I-120 | Remote Task ≠ Remote Desktop |
| <a id="rule-i-121"></a>I-121 | Cloud Agent Task ≠ native Product Job |
| <a id="rule-i-122"></a>I-122 | Remote Task ≠ Cloud-only Task |
| <a id="rule-i-123"></a>I-123 | Conversation Sync ≠ Remote Task State |
| <a id="rule-i-124"></a>I-124 | Unsent local draft ≠ acknowledged Cloud conversation |
| <a id="rule-i-125"></a>I-125 | Continuity ≠ mirroring UI |

### 7.5 Knowledge, search and retrieval

| # | Invariant |
|---|---|
| <a id="rule-i-130"></a>I-130 | Knowledge Source ≠ Data Copy |
| <a id="rule-i-131"></a>I-131 | Knowledge Source ≠ Context Provider |
| <a id="rule-i-132"></a>I-132 | Knowledge Source ≠ Import |
| <a id="rule-i-133"></a>I-133 | Knowledge Scope ≠ Index Scope |
| <a id="rule-i-134"></a>I-134 | Index ≠ Canonical Data |
| <a id="rule-i-135"></a>I-135 | Search Index ≠ Knowledge Authority |
| <a id="rule-i-136"></a>I-136 | Search Index ≠ User Data Authority |
| <a id="rule-i-137"></a>I-137 | Knowledge Index ≠ Document Copy |
| <a id="rule-i-138"></a>I-138 | Semantic Index ≠ Knowledge |
| <a id="rule-i-139"></a>I-139 | Embedding ≠ Permission |
| <a id="rule-i-140"></a>I-140 | Cloud Sync ≠ Cloud Index |
| <a id="rule-i-141"></a>I-141 | Cloud Index ≠ AI Retrieval |
| <a id="rule-i-142"></a>I-142 | Cloud Search ≠ Cloud AI Indexing |
| <a id="rule-i-143"></a>I-143 | AI Retrieval ≠ Managed AI Processing |
| <a id="rule-i-144"></a>I-144 | Exclude from AI ≠ Exclude from Search |
| <a id="rule-i-145"></a>I-145 | Keyword Search ≠ Semantic Search |
| <a id="rule-i-146"></a>I-146 | Search ≠ Retrieval |
| <a id="rule-i-147"></a>I-147 | Search ≠ Ask AI |
| <a id="rule-i-148"></a>I-148 | Web Search ≠ ArcChat Global Search |
| <a id="rule-i-149"></a>I-149 | Web Search ≠ long-term knowledge |
| <a id="rule-i-150"></a>I-150 | Retrieval Candidate ≠ Evidence |
| <a id="rule-i-151"></a>I-151 | Evidence ≠ Citation |
| <a id="rule-i-152"></a>I-152 | Search Result ≠ Citation |
| <a id="rule-i-153"></a>I-153 | Citation ≠ Vector Chunk ID |
| <a id="rule-i-154"></a>I-154 | Retrieval Unit ≠ Domain Resource |
| <a id="rule-i-155"></a>I-155 | Context Pack ≠ entire Knowledge Source |
| <a id="rule-i-156"></a>I-156 | ArcNotes Knowledge ≠ ArcChat Memory |
| <a id="rule-i-157"></a>I-157 | Personal Memory ≠ ArcNotes Knowledge |
| <a id="rule-i-158"></a>I-158 | Conversation Summary ≠ Personal Memory |
| <a id="rule-i-159"></a>I-159 | Conversation Context ≠ long-term knowledge |
| <a id="rule-i-160"></a>I-160 | Raw Capture ≠ text knowledge chunk |
| <a id="rule-i-161"></a>I-161 | Raw Video ≠ default vector corpus |
| <a id="rule-i-162"></a>I-162 | AI Summary ≠ Source Evidence |
| <a id="rule-i-163"></a>I-163 | AI Summary ≠ Measurement Result |
| <a id="rule-i-164"></a>I-164 | Derived Knowledge Artifact ≠ Original Source |
| <a id="rule-i-165"></a>I-165 | Source Revision ≠ Index Revision |
| <a id="rule-i-166"></a>I-166 | Index Freshness ≠ Source Freshness |
| <a id="rule-i-167"></a>I-167 | Retrieval Trace ≠ Chain-of-Thought |
| <a id="rule-i-168"></a>I-168 | Source Removal ≠ delete files |
| <a id="rule-i-169"></a>I-169 | Search ranking ≠ paid placement |

### 7.6 Data, sync, formats and recovery

| # | Invariant |
|---|---|
| <a id="rule-i-180"></a>I-180 | Sync ≠ Backup ≠ Version History ≠ Trash ≠ Export |
| <a id="rule-i-181"></a>I-181 | User Data ≠ Asset ≠ Cache ≠ Search Index ≠ Secret |
| <a id="rule-i-182"></a>I-182 | Sync ≠ AI upload; sync transmission ≠ AI transmission |
| <a id="rule-i-183"></a>I-183 | Domain Model ≠ Database Schema |
| <a id="rule-i-184"></a>I-184 | Database Schema ≠ Native File Format |
| <a id="rule-i-185"></a>I-185 | Native Format ≠ Interchange Format |
| <a id="rule-i-186"></a>I-186 | Native Format ≠ Cloud Sync Protocol |
| <a id="rule-i-187"></a>I-187 | Runtime Storage Format ≠ User Interchange Format |
| <a id="rule-i-188"></a>I-188 | Working Store ≠ Portable Package |
| <a id="rule-i-189"></a>I-189 | Project ≠ single file |
| <a id="rule-i-190"></a>I-190 | Document ≠ Markdown file; Canonical Document ≠ Markdown file |
| <a id="rule-i-191"></a>I-191 | Raw Capture ≠ Analysis Result |
| <a id="rule-i-192"></a>I-192 | MediaAsset ≠ File Path |
| <a id="rule-i-193"></a>I-193 | Managed Asset ≠ External Reference |
| <a id="rule-i-194"></a>I-194 | External Locator ≠ Resource Identity |
| <a id="rule-i-195"></a>I-195 | File Path ≠ Resource Identity |
| <a id="rule-i-196"></a>I-196 | Cache ≠ Canonical Data |
| <a id="rule-i-197"></a>I-197 | Proxy ≠ Original |
| <a id="rule-i-198"></a>I-198 | Autosave ≠ rewrite entire project |
| <a id="rule-i-199"></a>I-199 | Saved Locally ≠ Synced to Cloud |
| <a id="rule-i-200"></a>I-200 | Cloud Pending ≠ Unsaved |
| <a id="rule-i-201"></a>I-201 | Undo ≠ Revision |
| <a id="rule-i-202"></a>I-202 | Undo ≠ Revision History |
| <a id="rule-i-203"></a>I-203 | Revision ≠ Checkpoint |
| <a id="rule-i-204"></a>I-204 | Checkpoint ≠ Recovery Journal |
| <a id="rule-i-205"></a>I-205 | Revision History ≠ Trash |
| <a id="rule-i-206"></a>I-206 | Crash Recovery ≠ Undo |
| <a id="rule-i-207"></a>I-207 | Migration Recovery ≠ user Undo; Migration Recovery Point ≠ normal Undo |
| <a id="rule-i-208"></a>I-208 | App Binary Rollback ≠ Data Rollback |
| <a id="rule-i-209"></a>I-209 | Import ≠ live external sync |
| <a id="rule-i-210"></a>I-210 | Export ≠ Backup |
| <a id="rule-i-211"></a>I-211 | Repository Projection ≠ Runtime Authority |
| <a id="rule-i-212"></a>I-212 | Repository Projection ≠ Live Working Store |
| <a id="rule-i-213"></a>I-213 | Git Merge ≠ Collaboration Protocol |
| <a id="rule-i-214"></a>I-214 | Git Versioning ≠ Cloud Sync |
| <a id="rule-i-215"></a>I-215 | Resource Delete ≠ Managed Blob garbage collection |
| <a id="rule-i-216"></a>I-216 | Native Package ≠ Trusted Input |
| <a id="rule-i-217"></a>I-217 | CLR Type ≠ persistent format contract |
| <a id="rule-i-218"></a>I-218 | ETag ≠ ArcForges Content Hash |
| <a id="rule-i-219"></a>I-219 | High Durability ≠ Backup |
| <a id="rule-i-220"></a>I-220 | Permanent user deletion ≠ same-day disappearance from every disaster backup |
| <a id="rule-i-221"></a>I-221 | Read compatibility ≠ safe write compatibility |
| <a id="rule-i-222"></a>I-222 | Cache Recovery ≠ Canonical Data Recovery |
| <a id="rule-i-223"></a>I-223 | Projection Repair ≠ Canonical Data Repair |
| <a id="rule-i-224"></a>I-224 | Project Reference ≠ Resource Copy |

### 7.7 Security, permission and trust

| # | Invariant |
|---|---|
| <a id="rule-i-230"></a>I-230 | Identity ≠ Actor ≠ Executor ≠ Caller Process |
| <a id="rule-i-231"></a>I-231 | App Identity ≠ Human Authority |
| <a id="rule-i-232"></a>I-232 | Agent Profile ≠ Security Principal |
| <a id="rule-i-233"></a>I-233 | Agent Capability Configuration ≠ Permission |
| <a id="rule-i-234"></a>I-234 | Automation ≠ Principal |
| <a id="rule-i-235"></a>I-235 | Automation Definition ≠ Automation Principal |
| <a id="rule-i-236"></a>I-236 | Automation Creator Permission Snapshot ≠ permanent authority |
| <a id="rule-i-237"></a>I-237 | Role ≠ Permission |
| <a id="rule-i-238"></a>I-238 | Capability Permission ≠ Resource Authorization |
| <a id="rule-i-239"></a>I-239 | Permission ≠ Approval |
| <a id="rule-i-240"></a>I-240 | Permission Grant ≠ Approval |
| <a id="rule-i-241"></a>I-241 | Approval ≠ Persistent Grant |
| <a id="rule-i-242"></a>I-242 | Approval ≠ Step-up Authentication; Step-up ≠ Approval |
| <a id="rule-i-243"></a>I-243 | Remote Approval ≠ Local Presence |
| <a id="rule-i-244"></a>I-244 | Trust ≠ Permission |
| <a id="rule-i-245"></a>I-245 | Trust ≠ Risk |
| <a id="rule-i-246"></a>I-246 | Trust ≠ Entitlement |
| <a id="rule-i-247"></a>I-247 | Package Signature ≠ Safety |
| <a id="rule-i-248"></a>I-248 | Verified Publisher ≠ Unlimited Access; Verified Publisher ≠ safe capability |
| <a id="rule-i-249"></a>I-249 | First-party ≠ Unlimited Access |
| <a id="rule-i-250"></a>I-250 | Device Presence ≠ Device Trust |
| <a id="rule-i-251"></a>I-251 | Device Online ≠ Remote Agent Enabled |
| <a id="rule-i-252"></a>I-252 | Registered Device ≠ Remote-authorized Device |
| <a id="rule-i-253"></a>I-253 | Knowledge Eligibility ≠ Read Permission |
| <a id="rule-i-254"></a>I-254 | Read Permission ≠ Data Egress Permission |
| <a id="rule-i-255"></a>I-255 | Synced Data ≠ allowed external transmission |
| <a id="rule-i-256"></a>I-256 | SecretRef ≠ Secret Value |
| <a id="rule-i-257"></a>I-257 | Secret Use ≠ Secret Reveal |
| <a id="rule-i-258"></a>I-258 | Secret Permission ≠ general Settings permission |
| <a id="rule-i-259"></a>I-259 | Extension Isolation ≠ Authorization |
| <a id="rule-i-260"></a>I-260 | Out-of-process ≠ automatically safe |
| <a id="rule-i-261"></a>I-261 | MCP Protocol ≠ Trust |
| <a id="rule-i-262"></a>I-262 | MCP Tool Description ≠ Trusted Instruction |
| <a id="rule-i-263"></a>I-263 | Retrieved Content ≠ Security Instruction |
| <a id="rule-i-264"></a>I-264 | Skill Guidance ≠ Permission Grant |
| <a id="rule-i-265"></a>I-265 | Workflow Definition ≠ Authorization |
| <a id="rule-i-266"></a>I-266 | Delegation ≠ Privilege Amplification |
| <a id="rule-i-267"></a>I-267 | Permission Revocation ≠ Undo |
| <a id="rule-i-268"></a>I-268 | Revocation ≠ Compensation |
| <a id="rule-i-269"></a>I-269 | Declared Permission ≠ Granted Permission |
| <a id="rule-i-270"></a>I-270 | Installation ≠ authorize all operations |
| <a id="rule-i-271"></a>I-271 | Developer Mode ≠ permission bypass ≠ secret bypass ≠ workspace-policy bypass |
| <a id="rule-i-272"></a>I-272 | Audit ≠ Debug Log |
| <a id="rule-i-273"></a>I-273 | Audit ≠ Telemetry |
| <a id="rule-i-274"></a>I-274 | Audit ≠ Domain Revision History; Audit ≠ Product History |
| <a id="rule-i-275"></a>I-275 | Audit ≠ Task Operational Trace |
| <a id="rule-i-276"></a>I-276 | Diagnostic Log ≠ Audit |
| <a id="rule-i-277"></a>I-277 | App Lock ≠ Account Authentication |
| <a id="rule-i-278"></a>I-278 | Mobile Biometric Unlock ≠ high-risk authorization |
| <a id="rule-i-279"></a>I-279 | HTTPS Private Link ≠ Public Share Link |
| <a id="rule-i-280"></a>I-280 | Search ≠ Remote Desktop scan |
| <a id="rule-i-281"></a>I-281 | Stage-25 Product Policy ≠ Stage-26 Authorization |

### 7.8 Extensions, packages and interoperability

| # | Invariant |
|---|---|
| <a id="rule-i-290"></a>I-290 | Skill ≠ Capability |
| <a id="rule-i-291"></a>I-291 | Skill ≠ Extension Code |
| <a id="rule-i-292"></a>I-292 | Skill ≠ MCP |
| <a id="rule-i-293"></a>I-293 | Template ≠ Skill |
| <a id="rule-i-294"></a>I-294 | Template ≠ live parent resource |
| <a id="rule-i-295"></a>I-295 | Workflow ≠ Automation |
| <a id="rule-i-296"></a>I-296 | Workflow ≠ Task |
| <a id="rule-i-297"></a>I-297 | Workflow ≠ Agent Plan |
| <a id="rule-i-298"></a>I-298 | Workflow ≠ arbitrary script runtime |
| <a id="rule-i-299"></a>I-299 | Automation ≠ Workflow |
| <a id="rule-i-300"></a>I-300 | Package ≠ Contribution |
| <a id="rule-i-301"></a>I-301 | Package Version ≠ Protocol Version |
| <a id="rule-i-302"></a>I-302 | Package Version ≠ App Version |
| <a id="rule-i-303"></a>I-303 | Install ≠ Enable |
| <a id="rule-i-304"></a>I-304 | Install ≠ Permission Grant |
| <a id="rule-i-305"></a>I-305 | Compatibility ≠ Trust |
| <a id="rule-i-306"></a>I-306 | Compatibility ≠ Enablement |
| <a id="rule-i-307"></a>I-307 | MCP ≠ native Arc capability |
| <a id="rule-i-308"></a>I-308 | MCP ≠ Connector |
| <a id="rule-i-309"></a>I-309 | MCP Definition ≠ MCP Connection |
| <a id="rule-i-310"></a>I-310 | MCP Prompt ≠ Skill |
| <a id="rule-i-311"></a>I-311 | Connector ≠ Connection |
| <a id="rule-i-312"></a>I-312 | Connector ≠ imported snapshot |
| <a id="rule-i-313"></a>I-313 | **Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006):** external-agent integration is excluded, not a separate agent-profile implementation. |
| <a id="rule-i-314"></a>I-314 | **Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006):** no external-agent task/delegation adapter is required. |
| <a id="rule-i-315"></a>I-315 | ACP Session ≠ Conversation |
| <a id="rule-i-316"></a>I-316 | ACP ≠ ArcChat runtime model |
| <a id="rule-i-317"></a>I-317 | Extension ≠ third-party Arc App |
| <a id="rule-i-318"></a>I-318 | Extension Process ≠ Host Process |
| <a id="rule-i-319"></a>I-319 | Extension Private State ≠ Product Domain State |
| <a id="rule-i-320"></a>I-320 | Extension Capability ≠ Permission |
| <a id="rule-i-321"></a>I-321 | Third-party Package ≠ runtime DLL injection |
| <a id="rule-i-322"></a>I-322 | Runtime Extension ≠ NuGet package restore |
| <a id="rule-i-323"></a>I-323 | Catalog ≠ Marketplace |
| <a id="rule-i-324"></a>I-324 | Catalog ≠ runtime dependency |
| <a id="rule-i-325"></a>I-325 | Community Package ≠ automatically trusted |
| <a id="rule-i-326"></a>I-326 | Package Dependency ≠ Capability Dependency |
| <a id="rule-i-327"></a>I-327 | Public SDK Contract ≠ internal LocalRpc Contract |
| <a id="rule-i-328"></a>I-328 | Extension Schema ≠ `Dictionary<string, object>` |
| <a id="rule-i-329"></a>I-329 | Dynamic Extension Boundary ≠ core product capability protocol |
| <a id="rule-i-330"></a>I-330 | Deprecate ≠ Revoke |

### 7.9 Policy and configuration

| # | Invariant |
|---|---|
| <a id="rule-i-340"></a>I-340 | Policy ≠ Setting |
| <a id="rule-i-341"></a>I-341 | Policy ≠ Entitlement |
| <a id="rule-i-342"></a>I-342 | Policy ≠ Permission |
| <a id="rule-i-343"></a>I-343 | Policy ≠ Runtime Health |
| <a id="rule-i-344"></a>I-344 | Policy ≠ Domain State |
| <a id="rule-i-345"></a>I-345 | Policy Control Plane ≠ request Data Plane |
| <a id="rule-i-346"></a>I-346 | Policy Scope ≠ Entitlement Scope |
| <a id="rule-i-347"></a>I-347 | Feature ≠ Feature Flag |
| <a id="rule-i-348"></a>I-348 | Feature Flag ≠ Rollout |
| <a id="rule-i-349"></a>I-349 | Rollout ≠ Experiment |
| <a id="rule-i-350"></a>I-350 | Experiment ≠ Entitlement |
| <a id="rule-i-351"></a>I-351 | Experiment ≠ Security Policy |
| <a id="rule-i-352"></a>I-352 | Experiment Assignment ≠ random every request |
| <a id="rule-i-353"></a>I-353 | Kill Switch ≠ Feature Lifecycle |
| <a id="rule-i-354"></a>I-354 | Kill Switch ≠ delete data |
| <a id="rule-i-355"></a>I-355 | Remote Config ≠ User Preference |
| <a id="rule-i-356"></a>I-356 | Remote Config ≠ arbitrary code |
| <a id="rule-i-357"></a>I-357 | Remote Config ≠ Project Format |
| <a id="rule-i-358"></a>I-358 | Remote Config ≠ transport selection |
| <a id="rule-i-359"></a>I-359 | Compatibility Policy ≠ Capability Negotiation |
| <a id="rule-i-360"></a>I-360 | Minimum Cloud Version ≠ Minimum Local Data Version |
| <a id="rule-i-361"></a>I-361 | Provider Availability ≠ Provider Health |
| <a id="rule-i-362"></a>I-362 | Model Availability ≠ Model Entitlement |
| <a id="rule-i-363"></a>I-363 | Model Availability ≠ Model Capability |
| <a id="rule-i-364"></a>I-364 | Recommended Model ≠ Pinned Model |
| <a id="rule-i-365"></a>I-365 | Workspace Policy ≠ Workspace Permission |
| <a id="rule-i-366"></a>I-366 | Policy Bundle ≠ live mutable database view |
| <a id="rule-i-367"></a>I-367 | Policy Push Event ≠ Policy Authority |
| <a id="rule-i-368"></a>I-368 | Last Known Good ≠ current cloud truth |
| <a id="rule-i-369"></a>I-369 | Published Revision ≠ Draft |
| <a id="rule-i-370"></a>I-370 | Policy Rollback ≠ rewrite history |
| <a id="rule-i-371"></a>I-371 | Dynamic Policy ≠ Architecture Constitution |
| <a id="rule-i-372"></a>I-372 | Dynamic Policy ≠ business-logic deployment |

### 7.10 Quality, compatibility and platform

| # | Invariant |
|---|---|
| <a id="rule-i-380"></a>I-380 | Fast in Debug ≠ Fast in Production |
| <a id="rule-i-381"></a>I-381 | JIT test pass ≠ AOT compatibility |
| <a id="rule-i-382"></a>I-382 | Build success ≠ runtime compatibility |
| <a id="rule-i-383"></a>I-383 | App Version ≠ Contract Version |
| <a id="rule-i-384"></a>I-384 | Contract Compatibility ≠ Product Policy Availability |
| <a id="rule-i-385"></a>I-385 | Read Compatibility ≠ Write Compatibility |
| <a id="rule-i-386"></a>I-386 | Migration Success ≠ Data Semantic Preservation |
| <a id="rule-i-387"></a>I-387 | Crash-free ≠ Recoverable |
| <a id="rule-i-388"></a>I-388 | Small Benchmark ≠ Scale Reliability |
| <a id="rule-i-389"></a>I-389 | Startup Time ≠ Time To Usable |
| <a id="rule-i-390"></a>I-390 | Managed Heap ≠ Total Memory |
| <a id="rule-i-391"></a>I-391 | Process Running ≠ Healthy |
| <a id="rule-i-392"></a>I-392 | Responsive Animation ≠ Responsive Product |
| <a id="rule-i-393"></a>I-393 | Accessible Color ≠ Accessible Product |
| <a id="rule-i-394"></a>I-394 | Keyboard Shortcut ≠ Keyboard Accessibility |
| <a id="rule-i-395"></a>I-395 | Localized UI ≠ Locale-safe Data |
| <a id="rule-i-396"></a>I-396 | Display Unit ≠ Canonical Quantity |
| <a id="rule-i-397"></a>I-397 | Automated Test ≠ real-hardware validation |
| <a id="rule-i-398"></a>I-398 | One OS passing ≠ cross-platform support |
| <a id="rule-i-399"></a>I-399 | Diagnostics ≠ Telemetry Consent |
| <a id="rule-i-400"></a>I-400 | Performance Target ≠ Marketing Claim |
| <a id="rule-i-401"></a>I-401 | Quality Waiver ≠ permanently lower standard |
| <a id="rule-i-402"></a>I-402 | Quality Requirement ≠ Engineering Suggestion |
| <a id="rule-i-403"></a>I-403 | SLO ≠ external SLA |
| <a id="rule-i-404"></a>I-404 | Focus ≠ Selection |
| <a id="rule-i-405"></a>I-405 | Push Notification ≠ Durable Attention State |

### 7.11 Support, operations and trust & safety

| # | Invariant |
|---|---|
| <a id="rule-i-410"></a>I-410 | Feedback ≠ Support Case |
| <a id="rule-i-411"></a>I-411 | Bug Report ≠ Engineering Defect |
| <a id="rule-i-412"></a>I-412 | Feature Request ≠ Product Commitment |
| <a id="rule-i-413"></a>I-413 | Known Issue ≠ Incident |
| <a id="rule-i-414"></a>I-414 | Incident ≠ Security Advisory |
| <a id="rule-i-415"></a>I-415 | Support ≠ Impersonation |
| <a id="rule-i-416"></a>I-416 | Operator ≠ User |
| <a id="rule-i-417"></a>I-417 | Operator Role ≠ unlimited access |
| <a id="rule-i-418"></a>I-418 | Support Access ≠ User Session |
| <a id="rule-i-419"></a>I-419 | Support Access ≠ permanent permission |
| <a id="rule-i-420"></a>I-420 | Break Glass ≠ Impersonation |
| <a id="rule-i-421"></a>I-421 | Break Glass ≠ global superuser |
| <a id="rule-i-422"></a>I-422 | Operator Console ≠ Database Console |
| <a id="rule-i-423"></a>I-423 | Operator Console ≠ Domain Owner |
| <a id="rule-i-424"></a>I-424 | Diagnostic Bundle ≠ automatic telemetry upload |
| <a id="rule-i-425"></a>I-425 | Diagnostic Bundle ≠ Recovery Package |
| <a id="rule-i-426"></a>I-426 | Recovery ≠ direct SQL mutation |
| <a id="rule-i-427"></a>I-427 | Recovery ≠ silent overwrite |
| <a id="rule-i-428"></a>I-428 | Recovery ≠ guaranteed recovery of missing data |
| <a id="rule-i-429"></a>I-429 | Report ≠ Investigation ≠ Enforcement ≠ Appeal |
| <a id="rule-i-430"></a>I-430 | Community Report ≠ Enforcement |
| <a id="rule-i-431"></a>I-431 | Report Count ≠ Guilt |
| <a id="rule-i-432"></a>I-432 | Delist ≠ Revoke |
| <a id="rule-i-433"></a>I-433 | Publisher Yank ≠ platform enforcement |
| <a id="rule-i-434"></a>I-434 | Package Revocation ≠ delete user project |
| <a id="rule-i-435"></a>I-435 | Package Revocation ≠ delete created resources |
| <a id="rule-i-436"></a>I-436 | Copyright Removal ≠ delete local canonical data |
| <a id="rule-i-437"></a>I-437 | Public Share Removal ≠ delete private source |
| <a id="rule-i-438"></a>I-438 | Account Cloud Restriction ≠ local data lock |
| <a id="rule-i-439"></a>I-439 | Appeal ≠ delete enforcement history |
| <a id="rule-i-440"></a>I-440 | Security Report ≠ public bug report |
| <a id="rule-i-441"></a>I-441 | Security Advisory ≠ Kill Switch |
| <a id="rule-i-442"></a>I-442 | Security Advisory ≠ Package Revocation |
| <a id="rule-i-443"></a>I-443 | Official Advisory ≠ self-host policy authority; Advisory ≠ remote policy authority |
| <a id="rule-i-444"></a>I-444 | Staff Access ≠ Secret Access |
| <a id="rule-i-445"></a>I-445 | Support Attachment ≠ product resource authority |
| <a id="rule-i-446"></a>I-446 | Audit ≠ operator-editable history |
| <a id="rule-i-447"></a>I-447 | Data exists in the Cloud ≠ support has the right to browse it |
| <a id="rule-i-448"></a>I-448 | Archive ≠ Delete |

### 7.12 Product-local invariants

| # | Invariant |
|---|---|
| <a id="rule-i-460"></a>I-460 | Notebook ≠ Workspace; Folder ≠ Tag; Document ≠ File; Block ≠ Markdown Line |
| <a id="rule-i-461"></a>I-461 | Note ≠ a second content model independent of Document |
| <a id="rule-i-462"></a>I-462 | Property ≠ Document Content; Saved View ≠ Ownership |
| <a id="rule-i-463"></a>I-463 | Attachment ≠ embedded base64 |
| <a id="rule-i-464"></a>I-464 | ArcNotes Checklist Item ≠ ArcChat Agent Task |
| <a id="rule-i-465"></a>I-465 | ArcScope Project ≠ ArcForges Workspace |
| <a id="rule-i-466"></a>I-466 | Device ≠ DataSource; ConnectionProfile ≠ Connection |
| <a id="rule-i-467"></a>I-467 | Session ≠ Connection; Session ≠ Capture |
| <a id="rule-i-468"></a>I-468 | Channel ≠ Signal; Signal ≠ Event; Raw Signal ≠ Derived Signal |
| <a id="rule-i-469"></a>I-469 | Live View ≠ Recording; Pause View ≠ Pause Capture |
| <a id="rule-i-470"></a>I-470 | Display Decimation ≠ Measurement Data |
| <a id="rule-i-471"></a>I-471 | Measurement ≠ Analysis; Decoder Output ≠ Raw Data |
| <a id="rule-i-472"></a>I-472 | Annotation ≠ data mutation; Comparison ≠ Merge |
| <a id="rule-i-473"></a>I-473 | Source Profile ≠ historical Session configuration |
| <a id="rule-i-474"></a>I-474 | ArcScope Cloud Sync ≠ raw capture upload |
| <a id="rule-i-475"></a>I-475 | View ≠ Signal Ownership |
| <a id="rule-i-476"></a>I-476 | ArcSlate Project ≠ Sequence; Project ≠ Media Folder |
| <a id="rule-i-477"></a>I-477 | Source Media ≠ Timeline Clip; Clip ≠ Source Media; MediaAsset ≠ Clip |
| <a id="rule-i-478"></a>I-478 | Source Time ≠ Timeline Time; Video Frame Time ≠ Audio Sample Time |
| <a id="rule-i-479"></a>I-479 | Playback ≠ final render; Preview Quality ≠ Export Quality |
| <a id="rule-i-480"></a>I-480 | Viewer frame drop ≠ source data loss; dropped preview frame ≠ dropped media data |
| <a id="rule-i-481"></a>I-481 | Transition ≠ random clip overlap state |
| <a id="rule-i-482"></a>I-482 | Effect Definition ≠ Effect Instance; Effect Stack ≠ separate effect engine |
| <a id="rule-i-483"></a>I-483 | Node Graph ≠ arbitrary script runtime; Keyframe ≠ current parameter value |
| <a id="rule-i-484"></a>I-484 | Proxy ≠ Render Cache; Render Cache ≠ Project Authority |
| <a id="rule-i-485"></a>I-485 | Native Render Job ≠ Cloud Agent Task ≠ UI progress dialog; Rendered Artifact ≠ ArcSlate Project |
| <a id="rule-i-486"></a>I-486 | Transcript ≠ Subtitle; AI Analysis ≠ Timeline Edit |
| <a id="rule-i-487"></a>I-487 | Agent Context ≠ media upload; Project Sync ≠ original media upload |
| <a id="rule-i-488"></a>I-488 | External Media ≠ Managed Media |
| <a id="rule-i-489"></a>I-489 | ArcSlate Link ≠ shared identity |
| <a id="rule-i-490"></a>I-490 | ArcSlate Sequence ≠ Timeline Clip |

---

### 7.13 [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) scope and accounting invariants

| # | Invariant |
|---|---|
| <a id="rule-i-491"></a>I-491 | Model loop location ≠ tool execution location |
| <a id="rule-i-492"></a>I-492 | Actual measured tokens ≠ estimated tokens; cumulative stream usage ≠ per-event delta |
| <a id="rule-i-493"></a>I-493 | Included recoverable capacity ≠ purchased credits ≠ supplier cost ≠ subscription payment |
| <a id="rule-i-494"></a>I-494 | Current configuration ≠ historical pricing snapshot; changing configuration ≠ resetting customer balances |
| <a id="rule-i-495"></a>I-495 | Open executable policy logic ≠ private deployment values; secret mount ≠ customer BYOK |
| <a id="rule-i-496"></a>I-496 | Synthetic capture ≠ hardware evidence; preview sample ≠ canonical simulation data |
| <a id="rule-i-497"></a>I-497 | OTIO interchange ≠ ArcSlate working project ≠ embedded source media |
| <a id="rule-i-498"></a>I-498 | Evictable acknowledged cache ≠ unacknowledged edits/uploads/tool receipts |

---

## 8. Forbidden aliases and obsolete terms

| Forbidden / obsolete | Reason | Use instead |
|---|---|---|
| `ArcCanvas`, `ArcMusic`, `ArcImage`, `ArcVideo` | `SUPERSEDED` product names (**[D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002)**) | No replacement canvas/slides product or capability; nothing; `ArcScope`; `ArcSlate` |
| "Workspace" meaning a panel layout | Collides with the cloud tenancy boundary | **Layout** |
| Bare "Project" in cross-product text | Three incompatible product meanings | `ArcChat.Project` / `ArcScope.Project` / `ArcSlate.Project` |
| Bare "Scope" | Eight distinct meanings exist | Name the scope explicitly: Knowledge Scope, Sync Scope, Permission Scope, Policy Scope, Product Scope, Search Scope, Egress Scope, Resource Scope |
| "ArcForges Suite 2.0" as a version | No mandatory suite release train | Per-product versions plus an optional release campaign name |
| "Central desktop service", `ArcForgesService.exe` | Prohibited architecture | ArcChat-hosted Hub |
| Unqualified "Unlimited AI" / "unlimited storage" | Prohibited unbounded commercial claims | Disclosed AI capacity recovery/rate/concurrency/model limits and storage tier |
| ".NET AOT" applied to RN Android | RN/Hermes is its own runtime under [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) | "React Native/Hermes release build" |
| "Cloud may remain JIT" | Superseded by [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) | "C# Cloud publishes Native AOT" |
| "A realtime connection is durable authority" | Hints are projections | "Reconcile using the typed authoritative read" |
| Waffo Pancake and every Waffo-specific mechanic | `SUPERSEDED` provider (**[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)**) | Paddle (MoR) and Payoneer (payout destination) |
| "License key unlock" in ArcChat Mobile | Prohibited by Apple 3.1.1 and **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)** | Cloud-resolved entitlement |
| `InvokeAsync(string, object)` / `Dictionary<string,object>` capability calls | Bypasses contracts, permissions and versioning | Strongly typed capability interfaces |
| `ArcForges.Foundation.Document`, `.VideoTimeline`, `.TelemetrySession` | Shared foundation must not hold domain | Product-owned domain types |
| `ArcProductBase` domain hierarchy | Product classification is not inheritance | Independent domains + platform contracts |

---

## 9. MCP disambiguation ([V-02](../assurance/phase-1-official-verification.md#rule-v-02))

The Model Context Protocol `2026-07-28` revision is a **stable** specification with a formal extensions framework that defines its own `Task` and `Skill` concepts. These collide with the ArcForges execution vocabulary and must be disambiguated explicitly wherever both appear.

| MCP term | ArcForges term | Relationship |
|---|---|---|
| `MCP.Task` | `ArcForges.Task` | **Unrelated.** An MCP task is a protocol-level unit of work at an MCP server. An ArcForges Task is a durable, owned, auditable unit in the ArcForges execution model. An MCP task never becomes an ArcForges Task implicitly; if one is created, it is created explicitly, owned by the Cloud agent module, and carries its own `TaskId`. |
| `MCP.Skill` | `ArcChat.Skill` | **Unrelated.** MCP skills are server-published behaviour packs. `ArcChat.Skill` is ArcChat-owned configuration. An MCP skill never becomes an `ArcChat.Skill`; it is surfaced as a capability contribution subject to the ordinary trust and permission model. |
| `MCP.Resource` | `ArcForges.Resource` | **Distinct.** [I-076](#rule-i-076), [I-341](#rule-i-341). An MCP resource is addressed by the MCP server's own scheme and is never an ArcForges `ResourceRef`. |
| `MCP.Prompt` | `ArcChat.Skill` | **Distinct** ([I-310](#rule-i-310)). |
| MCP statelessness | `Session` | The `2026-07-28` core is stateless: `initialize`/`initialized` removed, `Mcp-Session-Id` eliminated, capability negotiation moved per-request. ArcForges must not build session identity on MCP transport state. This is consistent with `Session ≠ Connection`. |
| MCP Multi Round-Trip Requests (MRTR) | Callback contracts | Server-to-client requests are restructured through MRTR. This is a transport mechanism, not an ArcForges execution concept. |

MCP tool descriptions, prompts, resource contents and server metadata are **untrusted data**, never instructions ([I-262](#rule-i-262), [I-263](#rule-i-263)).

---

## 10. Enforcement

The glossary is enforced, not merely published.

| Control | Mechanism | Where specified |
|---|---|---|
| Forbidden term scan | Repository-policy test failing the build on any forbidden alias or obsolete product name in `src/`, `docs/` (excluding `docs/deprecated-inputs/`), identifiers and resource strings | [`../assurance/testing-and-verification-strategy.md`](../assurance/testing-and-verification-strategy.md) |
| Invariant traceability | Every invariant maps to at least one architecture rule, one test, and one work-package completion gate | [`../assurance/traceability-matrix.md`](../assurance/traceability-matrix.md) |
| Namespaced-term enforcement | Architecture tests asserting product-owned types are not lifted into shared foundation namespaces | [`../architecture/01-solution-and-project-layout.md`](../architecture/01-solution-and-project-layout.md) |
| Glossary change control | A new canonical term, a changed definition, or a retired invariant requires a decision record in `docs/decisions/` | **[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** |

---

## 11. Traceability

| Current document | Relationship |
|---|---|
| [Invariant Coverage](../assurance/invariant-coverage.md) | Maps the current catalogue to architecture, verification and implementation owners |
| [Contracts, Protocols and the Cross-Application Semantic Model](../architecture/02-contracts-and-protocols.md) | Applies the canonical vocabulary to cross-product contracts |
| **[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** | The requirement that this document exists and gates detailed specification |
| **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** | The MCP term-collision requirement discharged in §9 |

## P2-009 technology invariants

Proto is authored wire authority; the sole model loop is CF Workflow; canonical business state is C#/PostgreSQL; object bytes are R2; product repositories consume immutable packages; Mobile is RN/Hermes. These replace superseded technology examples without renumbering inherited invariant IDs. Content-origin, Notes scalar queries, Scope measurement and Slate rational/tick meaning remain unchanged.
