# ArcChat — Product Requirements
> Current scope amendment: **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements / Products
> Product identity: `arcchat` · Positioning: **AI Agent Command Center / Local Hub / Task Center / Cross-App Orchestrator**
> Companions: [`../05-ai-and-agent-execution.md`](../05-ai-and-agent-execution.md), [`../06-knowledge-search-and-retrieval.md`](../06-knowledge-search-and-retrieval.md), [`../08-extensions-and-developer-platform.md`](../08-extensions-and-developer-platform.md), [`../09-shared-desktop-experience.md`](../09-shared-desktop-experience.md), [`arcchat-mobile-and-web.md`](arcchat-mobile-and-web.md)

> **ArcChat = Chat-first interface + Agent execution surface + Task control centre + ArcForges capability hub.**

Six sentences that decide almost every design question:

> **Chat** when you want an answer.
> **Agent** when you want work done.
> **Tasks** when work outlives the conversation.
> **Projects** when work has long-term context.
> **Artifacts** when work produces something valuable.
> **Arc Apps** when a specialist tool should own the real professional result.

---

## 1. Positioning and boundaries

| # | Requirement |
|---|---|
| PB-01 | ArcChat serves **three depths of use in one product**: a quick answer, a directed piece of work, and a long-running orchestrated workflow. It must not fork into three products or three modes of a shell. |
| PB-02 | **ArcChat is a control plane, never a mandatory data gateway** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). Professional products reach Cloud directly for their own data. |
| PB-03 | The ArcChat product domain owns conversations, messages, projects, profiles, skills, memory and automation definitions in Cloud. Cloud owns all agent execution and orchestration state. Desktop owns cached projections, drafts, the local application/capability registry, permission checks and idempotent local tool receipts. |
| PB-04 | **ArcChat never owns**: an authoritative ArcNotes document copy, a writable ArcNotes knowledge database, an authoritative ArcScope session, raw ArcScope capture, an ArcSlate timeline, ArcSlate media ownership, or any professional product's undo stack ([I-020](../01-normative-glossary-and-invariants.md#rule-i-020)). |
| <a id="rule-pb-05"></a>PB-05 | Thin Preview + Rich Handoff governs results. Native text/image previews and document/media metadata or thumbnails are sufficient; a code/Diff/Office/PDF editing or full media preview workbench is not required. Professional editing opens the owning product; required edit-approval previews remain reviewable. |
| PB-06 | The native client and local capability bridge are open-source product functionality. Official AI requires an active paid service term with replenishing capacity and optional credits. Local AI, end-user BYOK and a desktop agent scheduler are excluded. |

### 1.1 Non-goals

ArcChat is **not**: an IDE, a document editor, a telemetry analysis workbench, a video editor, a package manager for third-party software, a general-purpose automation scripting environment, or a model marketplace. Each of those has an owner, and ArcChat orchestrates rather than replaces them.

---

## 2. Information architecture

Primary surfaces:

| Surface | Role |
|---|---|
| **Home** | Start + Continue + Attention |
| **Chats** | Conversation history |
| **Tasks** | The Task Center |
| **Artifacts** | The artifact library |
| **Projects** | Long-term working contexts |
| **Apps** | The ArcForges capability centre |
| **Automations** | Automation definitions and run history |
| **Settings** | Preferences and configuration |

| # | Requirement |
|---|---|
| IA-01 | **Home is not a marketing dashboard.** It is Start (a composer), Continue (recent work), and Attention (what needs the user). |
| IA-02 | **The composer is the most important element of Home.** "Ask or do something" is the primary action. |
| IA-03 | **Needs Attention is a projection** ([I-091](../01-normative-glossary-and-invariants.md#rule-i-091)) over pending approvals, waiting-too-long tasks, recoverable interruptions, budget approvals, conflicts and failed compensations. It is not a fifth task state. |
| IA-04 | **Artifacts is a first-class surface with a global library**, because work products outlive the conversations that produced them. |
| IA-05 | **Search need not occupy a permanent navigation slot**; the quick bar and per-surface search cover it. |

---

## 3. Conversation

**Conversation = a continuous human–computer interaction context.**

| # | Requirement |
|---|---|
| CV-01 | **A conversation need not belong to a project.** An unfiled conversation is a first-class, permanent state. |
| CV-02 | **A conversation has at most one primary project**, which does not prevent it referencing other resources. |
| CV-03 | Conversation lifecycle: active → archived → deleted. **Archive ≠ Delete** ([I-448](../01-normative-glossary-and-invariants.md#rule-i-448)). |
| <a id="rule-cv-04"></a>CV-04 | **Conversation history is append-and-branch, never rewrite.** Editing an earlier message creates a **new conversation branch**; regenerating creates an **alternative branch**; forking creates a **new conversation**. |
| CV-05 | **Even deleting content leaves a trace**: redaction produces a tombstone, so history is never silently rewritten. |
| CV-06 | Conversation titles are generated but always user-editable. |
| CV-07 | **Message ≠ Task** ([I-108](../01-normative-glossary-and-invariants.md#rule-i-108)). A task is not a message; a conversation **links** to tasks. |
| CV-08 | **A tool call is not ordinary chat text** ([I-109](../01-normative-glossary-and-invariants.md#rule-i-109)). It is an activity detail with its own presentation. |
| CV-09 | **Model chain-of-thought is never displayed** ([I-107](../01-normative-glossary-and-invariants.md#rule-i-107)). |
| CV-10 | Response details show the executed model, public route identity, customer tariff version, measured usage and charge status, tools and citations. Private supplier prices, provider credentials and unrestricted deployment policy are never exposed. |

---

## 4. Composer

| # | Requirement |
|---|---|
| CO-01 | **The composer defaults to one simple layer.** Advanced agent controls exist but are never all expanded permanently. |
| CO-02 | **The composer has a durable draft**, stored as device-local state. |
| CO-03 | Two interaction contracts, not two products: |

| Mode | Contract |
|---|---|
| **Chat Mode** | **Answer-first, minimal side effects.** Tools are not forbidden; the side-effect contract is narrow, and anything with a durable external effect requires explicit escalation. |
| **Agent Mode** | **Do the work.** Creates a Task by default ([EX-02](#rule-ex-02)). |

| # | Requirement |
|---|---|
| CO-04 | **Chat Mode does not mean "no tools"** ([I-117](../01-normative-glossary-and-invariants.md#rule-i-117)); it means a constrained side-effect contract. |
| CO-05 | **Agent Mode is not unlimited permission** ([I-118](../01-normative-glossary-and-invariants.md#rule-i-118)). Every capability call passes the full security pipeline. |
| CO-06 | **Automation is not a third composer mode.** It is a separate surface producing definitions ([AU-01](#rule-au-01)). |
| <a id="rule-co-07"></a>CO-07 | A complex agent task may display a **plan summary** ([EX-06](../05-ai-and-agent-execution.md#rule-ex-06)); a simple task must not be forced through a ceremonial plan. |

### 4.1 Context

| # | Requirement |
|---|---|
| CX-01 | **Composer context is a first-class object**, not a hidden prompt suffix. |
| CX-02 | **Input attachments and context references are different** ([I-110](../01-normative-glossary-and-invariants.md#rule-i-110), [I-111](../01-normative-glossary-and-invariants.md#rule-i-111)). An attachment is content the user supplied for this turn; a reference points at a resource that lives elsewhere. |
| <a id="rule-cx-03"></a>CX-03 | **A context reference does not copy content** ([I-051](../01-normative-glossary-and-invariants.md#rule-i-051)). Content is materialised at retrieval time, minimally ([CP-02](../06-knowledge-search-and-retrieval.md#rule-cp-02)). |
| CX-04 | **"Attach" never means "copy everything"** for a large resource. A large document, session or project is referenced and queried through its owner. |
| CX-05 | The **`@` picker** addresses resources, apps, projects and artifacts; the **`/` prefix** addresses commands and skills. Their semantics are distinct and never overloaded. |
| CX-06 | **`@App` does not mean "add the whole application to the prompt".** It qualifies scope, or invokes that application's context contribution. |
| CX-07 | **A Context Inspector must exist**, showing exactly what will be sent, with per-item removal. |
| CX-08 | Three context lifetimes are distinguished: **pinned** (persists), **temporary** (this turn only), **project** (inherited from the project). |
| CX-09 | **Context scope is never expanded silently** ([AS-05](../06-knowledge-search-and-retrieval.md#rule-as-05)). Any expansion is user-visible and enters the retrieval trace. |

---

## 5. Project

**`ArcChat.Project` = ArcChat's long-term working-context container.** It is **not** an ArcForges Workspace ([I-108](../01-normative-glossary-and-invariants.md#rule-i-108) family, glossary §5.1).

| # | Requirement |
|---|---|
| PJ-01 | A project owns: instructions, references, its conversations, its tasks, its artifacts, a default agent profile and a default context. |
| PJ-02 | **A project stores references, not copies** of professional data ([I-051](../01-normative-glossary-and-invariants.md#rule-i-051)). |
| PJ-03 | **Deleting a project never cascades into external professional resources** ([LC-05](../08-extensions-and-developer-platform.md#rule-lc-05) analogue). Referenced ArcNotes documents, ArcScope sessions and ArcSlate projects survive. |
| PJ-04 | ArcChat-owned content inside a deleted project — its conversations and tasks — is preserved or explicitly handled, never silently destroyed. |
| PJ-05 | Projects and their acknowledged content belong to the selected Cloud workspace. Native cached projections and unsent drafts are durable; a local-only agent project is not a supported storage or execution mode. |

---

## 6. Task Center

| # | Requirement |
|---|---|
| TC-01 | The Task Center projects Cloud agent tasks from interactive and automation origins. It may display associated native product jobs distinctly, with owner and availability; a render or capture does not become an AI task merely by appearing here. |
| TC-02 | **A task does not require a conversation** ([I-108](../01-normative-glossary-and-invariants.md#rule-i-108)), and **a conversation may link many tasks**. |
| TC-03 | Task detail contains: intent, status with reason, execution location, plan, operational trace, artifacts, approvals, cost, budget, origin, actor chain and outcome summary. |
| TC-04 | **Task trace shows the operational trace only** ([I-107](../01-normative-glossary-and-invariants.md#rule-i-107), [PR-08](../05-ai-and-agent-execution.md#rule-pr-08)–[PR-10](../05-ai-and-agent-execution.md#rule-pr-10)). |
| TC-05 | Task controls — pause, resume, cancel, retry, steer, approve, adjust budget — are available from one unified entry point. |
| TC-06 | **A task outlives its user interface.** Closing a conversation, a window or the application does not end a task, and reopening finds it. |
| TC-07 | On completion a task enters stable history and remains inspectable. |
| TC-08 | **Cancel ≠ Delete** for tasks ([CN-06](../05-ai-and-agent-execution.md#rule-cn-06)). |
| TC-09 | The full execution semantics are specified in [`../05-ai-and-agent-execution.md`](../05-ai-and-agent-execution.md); ArcChat is the surface, not a second model. |

---

## 7. Artifacts

**Artifact = a work product with independent value that the user can view, use or deliver.**

| # | Requirement |
|---|---|
| <a id="rule-ar-01"></a>AR-01 | **An artifact need not be owned by ArcChat** ([I-058](../01-normative-glossary-and-invariants.md#rule-i-058), [I-059](../01-normative-glossary-and-invariants.md#rule-i-059)). An ArcNotes document produced by a task is owned by ArcNotes; ArcChat holds an `ArtifactRef`. |
| AR-02 | **ArcChat-native artifacts exist** — a generated answer document, an exported summary, a produced file — and those it does own. |
| AR-03 | The **Artifact Library** lists artifacts across tasks and projects, with owner, kind, provenance and availability. |
| <a id="rule-ar-04"></a>AR-04 | **Artifact preview is thin preview** ([PB-05](#rule-pb-05)). Deep work happens in the owning product. |
| AR-05 | **Deleting an artifact entry is not deleting the source resource** ([I-060](../01-normative-glossary-and-invariants.md#rule-i-060), [LC-05](../08-extensions-and-developer-platform.md#rule-lc-05)). |
| AR-06 | **Every artifact retains provenance**: producing task, run, actor chain, capability, source references and time. |
| <a id="rule-ar-07"></a>AR-07 | **Artifact availability is a distinct state**: available, requires the owning application, requires a device, unavailable, or deleted at source. |

---

## 8. Apps and capability hub

**Apps = the ArcForges capability centre**, not an installed-programs list.

| # | Requirement |
|---|---|
| AP-01 | Each application card shows: identity, installed state, running state, version, contract compatibility, health, and its contributed capabilities. |
| AP-02 | **Installed and running are separate states** ([I-007](../01-normative-glossary-and-invariants.md#rule-i-007)). An installed but stopped application can be **launched on demand** ([P-06](../00-product-scope-and-portfolio.md#rule-p-06)). |
| AP-03 | Capabilities are inspectable per application, with risk level, permission requirements and current availability. |
| AP-04 | **The Apps page is not a third-party package manager in V1.** Package management belongs to the extension platform surfaces. |
| AP-05 | A not-installed Arc product may be shown, without becoming marketing pressure ([CA-09](../08-extensions-and-developer-platform.md#rule-ca-09)). |
| <a id="rule-ap-06"></a>AP-06 | **Applications contribute six kinds of thing**, not merely "tools": **Actions**, **Agent Capabilities**, **Context Providers**, **Artifact Handlers**, **Suggested Tasks**, and **Deep Links / Open Targets**. |
| AP-07 | **A capability's description is richer than an ordinary tool schema** (`CapabilityDescriptor` in the glossary): identity, typed method, contract version, input/output summary, whether it writes, required scope, risk level, confirmation requirement, dry-run/undo/cancel support, expected duration, resource size and concurrency limits. |
| AP-08 | **Every capability carries a trust level** (§9). |
| AP-09 | **Capability version compatibility exists from the first release** ([P-13](../00-product-scope-and-portfolio.md#rule-p-13), [CM-01](../12-quality-and-compatibility-contract.md#rule-cm-01)). |
| AP-10 | **Application events may drive agent automation** — the event feeds an ordinary automation trigger with deduplication, causation and throttling ([EP-05](../08-extensions-and-developer-platform.md#rule-ep-05)). **V1 keeps event automation simple**; time triggers are the baseline. |
| AP-11 | AI cross-product orchestration runs in the single Cloud harness. ArcChat bridges authorized desktop tools; simple user-directed handoffs can go directly to the owning product. |

### 8.1 Capability invocation ordering

The agent's preference order is fixed:

1. **Native Arc capability** — typed, owned, auditable
2. **Trusted connector / MCP / API** — external but declared and permissioned
3. **Computer use** — permitted as an advanced fallback, **never a V1 core mechanism**

| # | Requirement |
|---|---|
| CI-01 | The agent must not reach for a lower tier when a higher tier can do the job. |
| CI-02 | **Computer use is high-risk by construction** and carries the strictest approval posture. |

---

## 9. Permission and approval in ArcChat

| # | Requirement |
|---|---|
| PM-01 | ArcChat applies the full security model in [`../07-security-privacy-and-trust.md`](../07-security-privacy-and-trust.md). |
| PM-02 | **Allow is never a bare Yes/No.** A grant states scope, constraints and lifetime (`PM-02`, [PM-08](../07-security-privacy-and-trust.md#rule-pm-08)). |
| PM-03 | **The pattern for a consequential operation is Preview → Confirm → Execute**, with an impact preview and, for R2 and above, a checkpoint. |
| PM-04 | **An unrestricted autonomous mode is prohibited.** There is no "do anything without asking" switch. |
| PM-05 | The approval interface shows: what will happen, to which resource at which revision, the effective risk, the execution location, and the consequences — never a bare "allow?" ([AP-02](../07-security-privacy-and-trust.md#rule-ap-02) in the security requirements). |
| PM-06 | **An external effect is highlighted distinctly** from a local one. |
| PM-07 | **Remote approval displays the execution location** and cannot substitute for local presence where required ([LP-02](../07-security-privacy-and-trust.md#rule-lp-02)). |

---

## 10. Agent profiles and skills

**Agent Profile = a reusable agent working-mode configuration.**

| # | Requirement |
|---|---|
| AG-01 | **A profile is not a running agent** ([I-112](../01-normative-glossary-and-invariants.md#rule-i-112)) and **not a model** ([I-113](../01-normative-glossary-and-invariants.md#rule-i-113)). |
| AG-02 | A profile may contain: instructions, model policy, effort level, enabled skills, permitted capability classes, default budgets, default execution target, and default context policy. |
| AG-03 | **A profile must not contain**: secrets, granted permissions, or entitlement ([I-233](../01-normative-glossary-and-invariants.md#rule-i-233)). |
| AG-04 | A built-in default profile exists and may be **duplicated**, not silently mutated. |
| AG-05 | **Editing a profile does not change a running task** ([EX-05](../05-ai-and-agent-execution.md#rule-ex-05)). |
| AG-06 | **Deleting a profile does not delete historical tasks**; those retain their frozen snapshot. |
| AG-07 | Profile resolution order: explicit per-message selection → conversation setting → project default → global default. |

**Skill = a reusable agent instruction, methodology and working-knowledge package.**

| # | Requirement |
|---|---|
| SK-01 | **Skill ≠ Capability** ([I-290](../01-normative-glossary-and-invariants.md#rule-i-290)) and **Skill ≠ MCP** ([I-292](../01-normative-glossary-and-invariants.md#rule-i-292)). A skill describing how to use a capability does not grant it. |
| SK-02 | Skills come from three sources: built-in, user-authored, and packaged (`§1` of the extension requirements). User skills are directly editable. |
| SK-03 | **Skills are versioned** (`SK-03`). |
| SK-04 | A profile enables a set of skills; a project may recommend or enable skills. **There must not be two conflicting ownership models for skills.** |
| SK-05 | The task trace may show which skills applied. |

---

## 11. Integrations

| # | Requirement |
|---|---|
| IN-01 | **MCP is external capability integration** ([MC-01](../08-extensions-and-developer-platform.md#rule-mc-01)). |
| IN-02 | The MCP management surface shows: server identity, connection state, declared tools, granted tools, secrets by reference, health, and last error. |
| IN-03 | **Adding a server does not let the agent call all its tools.** Tools are enabled deliberately ([MC-10](../08-extensions-and-developer-platform.md#rule-mc-10)). |
| IN-04 | **MCP credentials are secrets**, not configuration strings ([SE-01](#rule-se-01)). |
| <a id="rule-in-05"></a>IN-05 | **A down MCP server must not break ArcChat.** The product continues; the integration shows degraded. |
| IN-06 | **An MCP resource does not automatically become AI context** ([I-076](../01-normative-glossary-and-invariants.md#rule-i-076)). |
| IN-07 | MCP servers and connectors share an Integrations surface. External agent/ACP adapters, handoff and agent delegation are excluded. |

---

## 12. AI source, provider and model

Cloud service access has one customer mode: subscribed, operator-managed AI. The model picker selects an Auto class or an available concrete model; provider routing is server-side infrastructure. Self-hosting changes the service realm and operator configuration, not the desktop into a model host.

---

| # | Requirement |
|---|---|
| AI-01 | **The default is an Auto class** (for example Balanced), not a specific model. |
| <a id="rule-ai-02"></a>AI-02 | **Advanced users may pin an explicit model**, and a pinned model is never silently substituted ([PA-05](../11-policy-and-configuration.md#rule-pa-05)). |
| AI-03 | **The model picker is a curated catalogue**, not an exhaustive provider list ([RT-09](../05-ai-and-agent-execution.md#rule-rt-09)), and shows relative cost class. |
| AI-04 | The product understands **model capabilities** — context window, modality support, tool-calling ability, reasoning support — and uses them for routing and for warning the user. |
| AI-05 | **Effort is a provider-neutral product control**, not a per-vendor parameter leaked into the interface. |
| AI-06 | A conversation remembers its model policy; **a single message may override without permanently changing the default**. |
| AI-07 | Resolution order: per-message override → conversation policy → project default → profile → global default, bounded by availability policy and budget. |
| AI-08 | **A task freezes its AI policy at start** ([TR-04](../05-ai-and-agent-execution.md#rule-tr-04), [TS-01](../11-policy-and-configuration.md#rule-ts-01)). |
| AI-09 | AI always uses the selected Cloud service realm. Provider unavailability cannot cause desktop inference, end-user key use or a silent switch to another service realm. |
| AI-10 | **Auto routing is explainable**: the user can see which model ran and why. |
| AI-11 | Usage shows replenishing included capacity, recovery timing, additional credits, configured rate/concurrency limits and per-response/task measured consumption. Extra-credit use is opt-in and visibly capped. |
| AI-12 | **Long context is flagged before it is used** ([CO-04](../05-ai-and-agent-execution.md#rule-co-04)). |
| AI-13 | The client starts without a paid term and exposes sign-in, preferences, application status and authorized cached history. Sending a model request requires Cloud connectivity and service eligibility; no provider setup or offline agent alternative is offered. |
| AI-14 | **Provider failure is productised**: a clear state, a retry path, an alternative, and never a red-flagged conversation. |

---

## 13. Search

**Search = deterministic discovery of existing information** ([I-146](../01-normative-glossary-and-invariants.md#rule-i-146), [I-147](../01-normative-glossary-and-invariants.md#rule-i-147)).

| # | Requirement |
|---|---|
| <a id="rule-se-01"></a>SE-01 | Global search covers ArcChat's own data — conversations, projects, tasks, artifacts — and **federates** to other Arc products ([SR-03](../06-knowledge-search-and-retrieval.md#rule-sr-03)). |
| SE-02 | **Search results display their owner** ([SR-09](../06-knowledge-search-and-retrieval.md#rule-sr-09)). |
| SE-03 | **Search never copies authoritative data.** ArcChat does not build a second complete index of another product's content ([I-031](../01-normative-glossary-and-invariants.md#rule-i-031)). |
| SE-04 | **Search does not cross workspaces by default** ([CS-05](../03-cloud-services-and-sync.md#rule-cs-05)). |
| SE-05 | Local and cloud search share one user experience while remaining distinct in scope and capability. |
| SE-06 | A search result is directly actionable: open, attach as context, add to a project, or hand off. |
| SE-07 | **A search query is not a prompt** ([I-147](../01-normative-glossary-and-invariants.md#rule-i-147)). Typing a search does not invoke a model. |
| SE-08 | **Web search is an AI/agent capability**, labelled distinctly from cloud search, costs credits, and **requires citations** ([CO-07](#rule-co-07), [EC-09](../06-knowledge-search-and-retrieval.md#rule-ec-09)). |
| SE-09 | **ArcChat does not save whole web pages as invisible long-term knowledge** ([I-149](../01-normative-glossary-and-invariants.md#rule-i-149), [KP-01](../06-knowledge-search-and-retrieval.md#rule-kp-01)). Web content is request context and citation. |

---

## 14. History and memory

| # | Requirement |
|---|---|
| HM-01 | **There is no universal history domain.** Each object owns its own history: conversations own message history, tasks own run history, automations own run history, artifacts own provenance. A global Activity view is a **projection** ([I-274](../01-normative-glossary-and-invariants.md#rule-i-274)). |
| HM-02 | Memory is explicitly layered and must never be a black box: **conversation context** (this conversation), **project instructions and context** (this project), **personal memory** (ArcChat-owned durable preference recall), and **long-term knowledge** — which is **ArcNotes**, not ArcChat memory ([I-156](../01-normative-glossary-and-invariants.md#rule-i-156)). |
| <a id="rule-hm-03"></a>HM-03 | **A runtime context summary is not user memory** ([I-158](../01-normative-glossary-and-invariants.md#rule-i-158)). Compaction is context engineering, not a durable record about the user. |
| HM-04 | **Personal memory is visible, inspectable, editable and deletable.** |
| HM-05 | **Memory is never shared silently across workspaces** ([AS-02](../06-knowledge-search-and-retrieval.md#rule-as-02)). |
| <a id="rule-hm-06"></a>HM-06 | **Temporary Chat** exists as an explicit mode: not stored in history. It follows the actual route in use — **it does not mean the model never received the data** — and the interface must say so honestly. |
| HM-07 | **A genuinely long-running agent task is unsuitable for a purely temporary conversation**, and the product says so rather than silently losing state. |

---

## 15. Automations surface

| # | Requirement |
|---|---|
| <a id="rule-au-01"></a>AU-01 | Automations has its own page listing definitions with: schedule, trigger, execution target, policies, budget, enabled state, last run and next run. |
| AU-02 | **The primary creation route is "Automate this"** from a task that already succeeded — far better than asking a user to write a schedule expression first. It extracts a **task template** ([AU-03](../05-ai-and-agent-execution.md#rule-au-03) in the AI requirements), not a saved trace. |
| AU-03 | **Every automation run appears in the Task Center** as an ordinary task. |
| AU-04 | Trigger, missed-run policy and concurrency policy are configured here and enforced per [`../05-ai-and-agent-execution.md`](../05-ai-and-agent-execution.md) §10. |

---

## 16. Quick Bar

| # | Requirement |
|---|---|
| QB-01 | A **global Quick Bar** is available system-wide, distinct from the in-product **Command Palette** ([CM-07](../09-shared-desktop-experience.md#rule-cm-07)). The palette runs commands in the current product; the quick bar starts work anywhere. |
| QB-02 | **The global shortcut is platform-safe and user-configurable** ([SH-04](../09-shared-desktop-experience.md#rule-sh-04)). |
| QB-03 | Invoked from a professional product, the quick bar may carry that product's **current context**. |
| QB-04 | Invoked globally from the operating system, it carries **no professional context by default**. |

---

## 17. Onboarding

| # | Requirement |
|---|---|
| ON-01 | Onboarding is restrained and explains the Cloud account/service dependency where needed. No forced tour or suite install. |
| ON-02 | AI onboarding selects an available Cloud model policy after sign-in, shows service eligibility and usage limits, and obtains any required purchase through the approved commerce surface. |
| <a id="rule-on-03"></a>ON-03 | Local AI and all end-user BYOK setup paths are excluded. |
| ON-04 | Official AI requires an ArcForges account and active paid service term. Extra credits alone do not activate AI. Self-hosting uses the configured operator service grant, not official credits. |
| ON-05 | **Application detection is informative, not coercive.** Discovering that ArcNotes is installed enables capabilities; not having it must not push a suite installation. |
| ON-06 | **Permissions are not front-loaded into onboarding** ([UX-01](../07-security-privacy-and-trust.md#rule-ux-01)). They are just-in-time. |
| ON-07 | For an eligible account, first value is a first answer or simple Cloud agent task. An ineligible/offline state gives a precise next action rather than a fake response. |

---

## 18. Settings

| Section | Contents |
|---|---|
| **Chat & Composer** | Defaults, draft behaviour, display, conversation data |
| **Agent & Tasks** | Default profile, default budgets, default execution target, approval defaults |
| **AI & Usage** | Cloud model policy, service status, included capacity, extra-credit consent and budgets |
| **Memory & Personalization** | Personal memory, its visibility and controls |
| **Data & Privacy** | Sync scope, AI processing, export, local data location |
| **Account & Workspace** | Identity, realm, active workspace, storage |
| **Appearance, Shortcuts, Advanced** | Shared desktop experience settings |

| # | Requirement |
|---|---|
| ST-01 | **Skills, MCP and Apps are manageable product objects with their own surfaces**, not buried in Settings. Settings carries defaults and preferences. |
| ST-02 | End users never configure model-provider credentials. MCP/connector credentials remain purpose-scoped secrets by reference; they cannot act as a BYOK inference bypass. |
| ST-03 | Cloud sync and AI processing permissions are distinct. Sync does not authorize every resource as AI context. Conversations/tasks are Cloud-owned; sending AI content is Cloud processing. |
| ST-04 | Every Cloud agent operation uses one selected owner workspace for data authorization, service eligibility and metering. Cross-realm billing or a local-only agent task billed elsewhere is excluded. |
| ST-05 | Unsent drafts and local-only professional files are never uploaded merely on sign-in. Sending/attaching explicitly authorizes only the displayed content scope. |
| ST-06 | **The active workspace and context scope are always visible** ([AC-03](../09-shared-desktop-experience.md#rule-ac-03)), and there is **no silent cross-workspace context** ([AS-02](../06-knowledge-search-and-retrieval.md#rule-as-02)). |

---

## 19. Failure behaviour

| Failure | Required behaviour |
|---|---|
| **Cloud outage** | Cached history, drafts, deterministic search and authorized native tools remain usable. New AI requests wait for Cloud; there is no local model loop. Cloud-dependent capabilities degrade with a specific reason. The whole product does not enter a red offline mode ([ST-03](../09-shared-desktop-experience.md#rule-st-03) in the shared desktop requirements). |
| **Provider failure** | Reserved credits are released; the failure is reported with a retry or alternative; the user is not charged for platform-caused retries ([CU-03](../05-ai-and-agent-execution.md#rule-cu-03)). |
| **Agent task failure** | The **task** is marked failed, **not the conversation**. |
| **Professional application unavailable** | The task waits or needs attention with a specific reason and a launch or install route ([HO-02](../09-shared-desktop-experience.md#rule-ho-02)–[HO-04](../09-shared-desktop-experience.md#rule-ho-04)). |
| **MCP server down** | ArcChat continues; the integration is degraded. |

---

## 20. Export

| # | Requirement |
|---|---|
| <a id="rule-ex-01"></a>EX-01 | Cloud conversation export supplies documented JSON/text content with an attachment manifest and explicit availability. The client downloads the artifact; no standalone local conversation archive/recovery format is required. |
| <a id="rule-ex-02"></a>EX-02 | Cloud task-summary and selected artifact export preserve provenance and declared scope. They exclude secret credentials, private operational traces and another product’s unselected data. |
| <a id="rule-ex-03"></a>EX-03 | **ArcChat export never includes API keys or secrets** ([EX-10](../13-data-formats-and-portability.md#rule-ex-10) in the data requirements). |
| EX-04 | **Public share links are not in V1** (`§18` of the cloud requirements). Sharing is by export. |

---

## 21. Background and lifecycle

| # | Requirement |
|---|---|
| BL-01 | ArcChat may visibly run in the background for the local Hub and Cloud ToolRequest bridge. Automation scheduling and the model loop remain in Cloud; stopping the bridge makes local tools unavailable without ending Cloud-only work. |
| BL-02 | **It must never reside in the background secretly.** The state is visible, and the user can stop it. |
| BL-03 | Restart recovers Cloud task projections and durable local tool receipts. A lost reply reconciles by operation identity; the desktop never recreates or blindly reruns the Cloud agent loop. |
| BL-04 | **The Hub is hosted in the ArcChat process** ([P-05](../00-product-scope-and-portfolio.md#rule-p-05)); no system service is installed. |

---

## 22. Domain model

```
Conversation · ConversationBranch · Message · MessageContent · MessageRedaction
ConversationDraft
ContextReference · PinnedContext · TemporaryContext
ArcChatProject · ProjectInstruction · ProjectReference
AgentProfile · AgentProfileVersion
Skill · SkillVersion · SkillAssignment
AISelectionPolicy · AIResponseUsage · CloudModelSelection · ModelDescriptor
TaskReference · ApprovalReference
Artifact · ArtifactReference · ArtifactProvenance
AppRegistrationProjection · CapabilityProjection
McpIntegration · IntegrationStatus
AutomationDefinitionReference
PersonalMemory
SearchResultReference · ActivityProjection
ArcChatDataScope
```

---

## 23. V1 scope

| Area | Required in V1 |
|---|---|
| **Core chat** | Conversation, messages, branch and regenerate, archive, search, attachments, context |
| **Composer** | Chat/Agent modes, `@` context, model selection, basic agent profile, attachments |
| **Projects** | Instructions, references, chats, tasks, artifacts |
| **Agent** | Task creation, Task Center, progress, approval, cancel, artifacts |
| **Apps** | Detect Arc products, installed/running state, capabilities, launch on demand |
| **Profiles / Skills** | A default profile, user profiles, user skills, skill assignment |
| **AI** | Cloud subscription service, Auto/explicit model, actual usage, capacity recovery and opt-in extra credits |
| **Search** | ArcChat data search plus the federated search foundation |
| **Memory** | Transparent personal memory, project context, conversation context |
| **Automation** | List, enable/disable, create, "automate this" |
| **Cloud** | Authoritative conversations/projects, single-owner workspace, AI tasks and local-tool integration |

**Not required in V1**: a third-party package manager inside ArcChat, an integration marketplace, a full extension ecosystem, computer use as a core mechanism, public share links, or a large model catalogue.

**Multi-agent execution, sub-agents, agent teams, handoff and external-agent delegation are excluded internally and in the UI.** Bounded concurrent tools and ordinary product jobs remain supported.

---

## 24. Reference relationship

**AionUi is the ArcChat reference** (**[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**): a source of features, behaviour, tests and possibly reusable material — **never an architecture authority, a parity commitment, or a reason to import its runtime stack**. Its licence is Apache-2.0 (**[F-013](../../assurance/open-gates-register.md#rule-f-013)**, corrected in `I4 §Stage 6.77`), one-way compatible into the AGPL boundary with attribution and NOTICE, subject to the file-level provenance audit required by **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**.

ArcChat explicitly **does not** copy AionUi's product centre of gravity. In particular, the ArcChat centre is the capability hub and task centre, with deep third-party tooling treated as **advanced integration, not the product centre**.

An **ArcChat Reference Coverage Matrix** is required before ArcChat implementation planning is finalised (**[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**): see [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md).

---

## 25. Acceptance scenarios

**First run** — the native shell opens; sign-in/service requirements are clear; cached functions work as authorized; sending requires an eligible Cloud service. No provider-key or local-model setup exists.

**Chat versus Agent** — a question in Chat Mode answers with no task; a work request in Agent Mode creates a task with a visible plan and controls.

**Context** — attaching a large ArcNotes notebook references rather than copies; the Context Inspector shows exactly what is sent; removing an item removes it.

**Branching** — editing an earlier message creates a branch; the original history remains; regenerate creates an alternative branch.

**Project** — deleting a project leaves referenced ArcNotes documents and ArcScope sessions intact.

**Task** — a task survives closing the conversation, closing the window and restarting the application, and is found in the Task Center.

**Approval** — an approval names the resource and revision, shows the impact, and is invalidated by a revision change.

**Cross-application** — ArcChat requests a report; ArcNotes creates the document; ArcChat receives an `ArtifactRef`; the document is owned by ArcNotes; deleting the artifact entry does not delete the document.

**Application not running** — the capability launches ArcNotes on demand, or reports unavailability with a clear route.

**Version mismatch** — an incompatible professional product produces a specific "requires version X" message.

**Model** — a pinned model is never substituted; Auto stays within its cost class; a per-message override does not change the default.

**Service usage** — exhausted included capacity offers recovery timing or explicitly authorized extra credits; a credit balance without an active paid term cannot invoke official AI.

**Memory** — personal memory is inspectable and deletable; a temporary chat is honest about what the model received.

**Search** — federated results show owners; ArcChat holds no second copy of another product's corpus; workspace scoping holds.

**Automation** — "automate this" from a successful task produces a template with dynamic input, and each run appears in the Task Center.

**Cloud outage** — cached history, drafts and native tools survive; new AI is unavailable. Recovery reconciles Cloud state and pending local tool results without duplicate execution or billing.

**Background** — background operation is visible and stoppable; interrupted tasks are recovered and evaluated on restart.

---

## 26. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 17` | The complete ArcChat product specification: information architecture, conversation, composer, context, project, task centre, artifacts, apps, profiles, skills, MCP, AI selection, search, history and memory, automations, quick bar, onboarding, settings, failure behaviour, export and V1 scope |
| `I4 §Stage 6` | Platform positioning, thin-preview/rich-handoff, capability contribution kinds, invocation ordering, trust levels, permission posture, task and artifact first-class status, mode separation, Apache-2.0 reference correction |
| `I4 §Stage 13` | ArcChat's owned and prohibited state; control-plane role |
| `I4 §Stage 19` | The execution model ArcChat surfaces |
| `I4 §Stage 23` | Retrieval orchestration responsibilities |
| **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Control plane, never a mandatory data gateway |
| **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**, **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)** | AionUi as a reference under licence-gated reuse |
| **[D-020](../../decisions/phase-1-foundation-decisions.md#rule-d-020)**, **[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)** | Credit surfaces, and mobile commerce boundaries reflected in the companion |
