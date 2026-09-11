# AI, Agent Execution, Tasks and Automation Requirements
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** (economic model), **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** (cloud topology and local action), **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (runtime matrix)
> Companions: [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md), [`04-commerce-entitlement-and-credits.md`](04-commerce-entitlement-and-credits.md), [`07-security-privacy-and-trust.md`](07-security-privacy-and-trust.md), [`../architecture/09-ai-and-agent-runtime-architecture.md`](../architecture/09-ai-and-agent-runtime-architecture.md)

This document defines the Cloud Agent Task model and Cloud AI economics. Native product activities and jobs retain their own lifecycles.

**One Cloud Harness.** The sole model/tool loop runs in CF Workflow. C# Native AOT owns canonical Task state, deterministic scheduling, admission and business transactions. Native acquisition, editing, rendering and background maintenance are ordinary product jobs; an agent may invoke and observe them without converting them into a second agent runtime.

---

## 1. The unified execution chain

```
Intent → Task → Run → Plan → Step → Attempt → Capability Invocation / Operation → Result / Artifact
```

```
Intent
  │
  ▼
Task                              stable TaskId for the life of the work goal
  ├── Run 1                       one complete execution attempt
  │     ├── Plan Revision 1
  │     │     ├── Step A
  │     │     │     ├── Attempt 1
  │     │     │     └── Attempt 2
  │     │     └── Step B
  │     └── Plan Revision 2
  └── Run 2                       created by Retry
```

A Step may contain: an AI request, a capability invocation, a product job reference, an approval gate, a wait, or artifact production.

### 1.1 Definitions

| Term | Definition |
|---|---|
| **Intent** | What the user or system wants to accomplish: goal, constraints, requested outcome, input context, origin. Not an execution plan. |
| **Task** | A durable, trackable work **goal**. Answers "what is this job?", never "how many times has it run?". |
| **Run** | One complete execution attempt of a Task. Answers "how did it go this time?". |
| **Plan** | The Run's operational plan for satisfying the Intent — a user-legible execution structure, **never chain-of-thought**. |
| **Step** | A logical unit of work with a clear goal and dependencies. |
| **Attempt** | One actual execution try of a Step. |
| **Capability Invocation** | One semantic call into an owning application, integration or tool. |

### 1.2 Structural rules

| # | Requirement |
|---|---|
| EX-01 | **Intent is not a Task.** An ordinary chat turn produces a conversation turn and an AI response, with no Task at all. |
| <a id="rule-ex-02"></a>EX-02 | Create a Cloud Agent Task for recoverable or multi-step AI work, approvals, agent-driven side effects, automation and work waiting on tools/devices. An ordinary native render, capture, search or edit is a product Activity/Job and does not require a Cloud Task or paid AI. |
| EX-03 | **`TaskId` is stable for the life of the work goal.** A failed Run 1 followed by a successful Run 2 remains one Task. |
| <a id="rule-ex-04"></a>EX-04 | **A Task has at most one active Run at a time.** Running two Runs of one Task concurrently would produce duplicated documents, duplicated requests and duplicated external calls. A user wanting to try two approaches forks or clones the Task. |
| <a id="rule-ex-05"></a>EX-05 | **A Run freezes an Execution Snapshot at start**: intent version, agent profile version, skill versions, model and routing policy, permission policy, budget, execution-target policy, workspace and realm, input bindings, and the automation definition version where applicable. Editing a profile mid-run affects only later Runs and Tasks. |
| <a id="rule-ex-06"></a>EX-06 | **Plan revisions are retained, never overwritten.** A plan change records a categorised reason: user steering, capability unavailable, new evidence, retry strategy, alternative path. Hidden reasoning is never exposed. |
| EX-07 | **A Step is not a capability call** ([I-084](01-normative-glossary-and-invariants.md#rule-i-084)). One Step ("analyse the startup regression") may internally issue several capability invocations and AI requests. Some Steps invoke nothing at all — wait for approval, wait for device, produce the final response, evaluate results. |
| <a id="rule-ex-08"></a>EX-08 | V1 advances one model/agent loop per Run. A step may issue bounded independent tool calls concurrently and join their results before the loop continues. Dependency recording does not require a general DAG scheduler, independent planning branches or sub-agent execution. |
| <a id="rule-ex-09"></a>EX-09 | **Retrying a Step produces a new Attempt inside the same Step**, never a new Step. |
| EX-10 | Attempts distinguish **technical retry** (transient timeout; the system may re-attempt automatically) from **user retry** (a document conflict; a decision is required). Mechanical retry of the second class is prohibited. |

### 1.3 Identity separation

```
Retry Step   → new Attempt  → same Run
Retry Task   → new Run      → same Task
Run Again    → new Task
```

| # | Requirement |
|---|---|
| <a id="rule-id-01"></a>ID-01 | **`AttemptId` ≠ `CommandId`** ([I-085](01-normative-glossary-and-invariants.md#rule-i-085)). `CommandId` identifies the business action ("create this document"); `AttemptId` identifies how many times it was actually dispatched. A write capability that times out is re-sent under the **same** `CommandId`, so the owning application deduplicates rather than creating a second document. |
| ID-02 | **`InvocationId` ≠ `CommandId`** ([I-073](01-normative-glossary-and-invariants.md#rule-i-073)), and **Invocation ≠ Step** ([I-074](01-normative-glossary-and-invariants.md#rule-i-074)). |
| ID-03 | Retry preserves the original intent and fixed input bindings. A Step retry stays within its Run snapshot; a Task retry creates a new Run and revalidates current eligibility, security, model availability and customer tariff within an approved budget. Material cost changes are shown before new spending. Running against newly selected/latest data is a new Task, never a silent rewrite of historical intent. |
| ID-04 | A read capability retry is generally safe but must still consider revision: if the object read has changed, the Task must know its context moved. |

### 1.4 Input binding

| # | Requirement |
|---|---|
| <a id="rule-ib-01"></a>IB-01 | Task input uses **stable references** by default. `CurrentSelection` must never be persisted as the binding; it is resolved to a concrete resource, range and revision at Task creation. Otherwise a background Task's goal silently changes when the user clicks elsewhere. |
| IB-02 | Three binding kinds exist: **Fixed Reference** (this session, this revision), **Dynamic Selector** ("the latest ArcScope session matching project X"), and **Trigger Payload** (the event that fired). |
| IB-03 | A Dynamic Selector is **resolved once at the start of each Run** and then bound. A Run analysing "the latest session" does not switch targets mid-flight because a newer session appeared. |
| IB-04 | A trigger payload is fixed on the Trigger Occurrence and is not re-queried later. |

---

## 2. Task lifecycle

### 2.1 States

**Lifecycle State + Reason facet**, never dozens of mutually exclusive top-level enum members.

| State | Meaning |
|---|---|
| `Queued` | Accepted, not started |
| `Running` | Executing |
| `Waiting` | Wants to continue; an external condition is unmet |
| `Paused` | Explicitly told not to continue for now |
| `Interrupted` | Execution was lost unexpectedly |
| `Succeeded` | The Intent's required outcome was reached |
| `PartiallySucceeded` | Valuable results achieved, some goals unmet, and not all can or should be rolled back |
| `Failed` | The main goal was not achieved, and not enough completed to call it partial |
| `Canceled` | Cancellation was requested and has resolved |

`WaitingReason` is a separate dimension: `Approval`, `Device`, `App`, `Network`, `Resource`, `RateLimit`, `Capacity`, `Budget`, `Dependency`, `ProductJob`, `ScheduleCondition`. Adding a new reason later (for example `GPU`) must not change the state machine.

| # | Requirement |
|---|---|
| <a id="rule-st-01"></a>ST-01 | Every `Waiting` carries an **`AutoResume`** flag. `WaitingForNetwork` auto-resumes; `WaitingForApproval` does not. The interface must be able to distinguish "waiting for network" from "needs your approval". |
| ST-02 | **`Waiting` ≠ `Paused`** ([I-089](01-normative-glossary-and-invariants.md#rule-i-089)). Waiting is an unmet external condition; Paused is a deliberate suspension by user, policy or operator. |
| ST-03 | **`Interrupted` ≠ `Paused`** ([I-090](01-normative-glossary-and-invariants.md#rule-i-090)). Interruption is unexpected: application crash, machine reboot, executor lost, cloud worker terminated. |
| ST-04 | An interruption is followed by a **Recovery Evaluation** yielding one of: recoverable automatically, recoverable with user action, needs reconciliation, not recoverable. Not every interruption is recoverable, and the system must not assume it is. |
| ST-05 | **`Needs Attention` is a projection, not a state** ([I-091](01-normative-glossary-and-invariants.md#rule-i-091)). It derives from waiting-for-approval, waiting-for-device beyond a threshold, interrupted-but-recoverable, budget approval pending, conflict, or partial compensation failure. It must not become a fifth parallel state machine. |
| <a id="rule-st-06"></a>ST-06 | **`Succeeded` means the Intent's required outcome was reached** ([I-093](01-normative-glossary-and-invariants.md#rule-i-093)) — not that no exception was thrown. "Analyse three sessions and produce a report" with the analysis done and the report missing is **not** `Succeeded`. |
| ST-07 | **`Canceled` does not mean nothing happened** ([I-094](01-normative-glossary-and-invariants.md#rule-i-094)). The Task Outcome must enumerate completed effects, so the user does not assume cancellation restored the prior state. |

### 2.2 Cancellation and pause

| # | Requirement |
|---|---|
| <a id="rule-cn-01"></a>CN-01 | **Cancel is a request**: `CancelRequested → Canceling → Canceled`. Setting `Canceled` on click is prohibited. |
| CN-02 | Some work cannot stop instantly — finalising a video container, an atomic database commit, an external API that already accepted the request. The interface shows "Canceling… waiting for a safe point". |
| CN-03 | **Every capability declares its cancellation semantics**: `Cancelable`, `CancelableAtSafePoint`, `NotCancelableOnceStarted`. |
| CN-04 | **Pause is cooperative**: `PauseRequested → Pausing → Paused`. A Task that cannot pause mid-step enters `Paused` after the current Step completes. |
| CN-05 | **Resume continues the current Run from its persistent checkpoint.** A resumed Run keeps its Run identity. |
| <a id="rule-cn-06"></a>CN-06 | **Cancel Task ≠ Delete Task** ([I-199](01-normative-glossary-and-invariants.md#rule-i-199) analogue). Cancel stops execution; delete/archive is history management. They must never share one "Remove" control. |

### 2.3 Failure classification

Failure reasons are a unified, semantic set — they drive whether to auto-retry, wait, ask, or fail:

`Transient` · `DependencyUnavailable` · `Conflict` · `PermissionDenied` · `ApprovalDenied` · `BudgetExceeded` · `EntitlementBlocked` · `InvalidInput` · `CapabilityUnsupported` · `VersionIncompatible` · `ResourceMissing` · `Timeout` · `ExternalEffectUnknown` · `PermanentDomainFailure`

| # | Requirement |
|---|---|
| FL-01 | `Transient` permits **bounded** automatic retry. |
| FL-02 | `Conflict` (expected revision 42, current 50) must **not** be retried indefinitely. It requires refresh, rebase, action regeneration, and re-approval where the approval was revision-bound. |
| FL-03 | `PermissionDenied` is never retried "to see if it passes". It requires a user or policy change. |
| FL-04 | `CapabilityUnsupported` where the owning application is merely not running may launch it and retry. Where it is not installed, the Task waits or needs attention, or the plan takes an alternative. |
| <a id="rule-fl-05"></a>FL-05 | `VersionIncompatible` surfaces as a specific, actionable message ("ArcNotes 2.1 or later required"), never "tool failed". |
| <a id="rule-fl-06"></a>FL-06 | **`ExternalEffectUnknown` must never be blind-retried.** A send that lost its connection mid-flight has unknown effect. |
| <a id="rule-fl-07"></a>FL-07 | Every effect carries an **Effect Certainty**: `NotApplied`, `Applied`, `Unknown`. `Unknown` triggers reconciliation against the external system first; if it cannot be resolved, the Task goes to Needs Attention. This is what prevents duplicate emails, duplicate issue creation and duplicate payments. |
| <a id="rule-fl-08"></a>FL-08 | **Retry safety is declared by the capability owner**, never guessed by ArcChat. Capability metadata states `Idempotent`, `RetrySafe`, `RequiresReconciliation`. |

### 2.4 Timeouts and deadlines

**Deadline ≠ Timeout.** A deadline is a business goal ("by 17:00"); a timeout is an execution safety boundary ("this step may run at most 30 minutes"). On deadline the configured behaviour is one of stop, continue but mark late, or ask. A step timeout produces an attempt failure handled by the retry policy.

### 2.5 Priority

Tasks carry a limited priority: `Background`, `Normal`, `High`. Automation defaults to background or normal; a user request is normal; explicit user promotion is high. **Priority affects scheduling preference only.** It never bypasses permission, budget, entitlement, resource locks or safety.

---

## 3. Ownership and execution location

The single Harness executes in the ArcForges-AI Cloudflare Workflow through Workers AI bindings. C# Cloud owns durable business state, authorization, admission, metering and recovery ports. SDK objects are not wire or persistence authority. One Harness design supports many isolated users/tasks; it does not mean one global active task.

| # | Requirement |
|---|---|
| <a id="rule-ow-01"></a>OW-01 | Every Agent Task/Run/Step/Attempt has exactly one durable authority: the Cloud Agent module. Product jobs and user data keep their own product authority. |
| <a id="rule-ow-02"></a>OW-02 | Agent ownership never moves to a desktop. Reconnection reconstructs a Cloud projection; desktop receipt/execution of a ToolRequest does not create a local child Agent Task. |
| OW-03 | Desktop-, Web-, Mobile- and automation-originated AI all use the same Cloud authority. Ordinary chat has a durable Cloud request/usage record even when no multi-step Task is needed. |
| OW-04 | Local/Cloud describes tool execution location only. The model loop and scheduler always remain in Cloud; there is no local or hybrid Harness. |
| OW-05 | A tool may execute in Cloud or in an explicitly authorised product on a selected device. Scope hardware capture and Slate render/playback remain native jobs. |
| OW-06 | Tool target policy may select Cloud or a specific authorised device/product. It cannot select a local model/provider loop. |
| OW-07 | Automatic tool placement is bounded by data availability, capability, consent, resource authorisation, paid-service eligibility and budget. |
| <a id="rule-ow-08"></a>OW-08 | **`Auto` must never upload local-only data to enable cloud execution.** An 80 GB local capture selects an authorized desktop analysis tool; it does not become an 80 GB upload. |
| <a id="rule-ow-09"></a>OW-09 | Provider fallback remains within approved Cloud routes and the frozen customer budget. A Cloud outage never starts a desktop agent or changes the payer. |
| OW-10 | **Actor ≠ Origin ≠ Executor ≠ Capability Owner.** All four are recorded: actor `Ryan`, origin `ArcChat Mobile`, AI executor Cloud, local bridge ArcChat Desktop, capability owner/executor ArcScope. |
| OW-11 | Task origin records desktop, Mobile, Web or a Cloud automation occurrence. The initiating actor is the workspace owner or an authorised Cloud service acting for that owner; no AgentDelegation origin exists. |

---

## 4. Product jobs referenced by an Agent Task

| # | Requirement |
|---|---|
| <a id="rule-ct-01"></a>CT-01 | A long native/cloud product operation returns a ProductJobHandle with stable identity and status access. The Cloud Step waits for that job and observes completion; no hours-long blocking RPC. |
| CT-02 | The referenced Product Job records its owner, origin/correlation, output and status. It has no model loop, autonomous planning or delegated agent identity. |
| <a id="rule-ct-03"></a>CT-03 | Create a product Job only for an independent lifecycle such as capture, render/export, bulk processing or simulation. Internal agent Steps stay inside the same Cloud Run. |
| <a id="rule-ct-04"></a>CT-04 | Parent cancellation may request cancellation only of jobs it initiated and is authorised to control. Pre-existing/shared work is not cancelled; product safe-point semantics govern. |
| <a id="rule-ct-05"></a>CT-05 | The Cloud Run receives a job reference, outcome and ResourceRef/ArtifactRef, never the product internal state store. |
| <a id="rule-ct-06"></a>CT-06 | Sub-agents, agent teams, task handoff to another agent and external-agent delegation are excluded. Bounded independent tool calls are allowed inside the single Run. |
| <a id="rule-ct-07"></a>CT-07 | Job/tool concurrency remains visible through causal references and status. It never creates an independent agent workstream. |

---

## 5. Checkpoints, compensation and effects

### 5.1 Two kinds of checkpoint

| Kind | Owner | Purpose |
|---|---|---|
| **Execution Checkpoint** | The agent runtime | Resume a Run: completed steps, pending steps, continuation state, product job references |
| **Domain Checkpoint** | The owning professional application | A data recovery point, e.g. "before agent rewrite" in ArcNotes, "before agent timeline edit" in ArcSlate |

| # | Requirement |
|---|---|
| <a id="rule-ck-01"></a>CK-01 | **ArcChat can never create a system-wide snapshot.** Each product owns its own data authority. A cross-application agent requests a checkpoint from the owner and receives a `CheckpointRef`. |
| <a id="rule-ck-02"></a>CK-02 | A Domain Checkpoint is created **before** any high-risk batch modification. |
| CK-03 | **Checkpoint ≠ Undo** ([I-095](01-normative-glossary-and-invariants.md#rule-i-095)). Undo is high-frequency local edit history; a checkpoint is an explicit recovery boundary. Agent-scale changes use checkpoints. |

### 5.2 Effect semantics

Every side-effecting Step declares one of:

| Semantics | Meaning | Example |
|---|---|---|
| **Reversible** | The owner can reliably undo or restore a checkpoint | A local ArcNotes edit |
| **Compensatable** | A forward action restores a reasonable state, but history is not erased | A created document can be moved to trash |
| **Irreversible** | Cannot be undone at all | Sent email, published public content, external payment, external notification |

### 5.3 Compensation

| # | Requirement |
|---|---|
| CP-01 | **Compensation is a business-reasonable reverse or remedial action, never a database rollback** ([I-096](01-normative-glossary-and-invariants.md#rule-i-096)). |
| <a id="rule-cp-02"></a>CP-02 | Cross-application unwinding is a **Saga**, executed in reverse through each owner. Cross-process ACID transactions are not simulated. |
| <a id="rule-cp-03"></a>CP-03 | **Compensation is itself traced and visible**, never executed silently. The trace shows each compensating action and its result, including failures ("unable to retract external email ⚠"). |
| <a id="rule-cp-04"></a>CP-04 | **Compensation can fail.** A failed compensation yields Needs Attention or PartiallySucceeded. Claiming a successful rollback that did not occur is prohibited. |
| <a id="rule-cp-05"></a>CP-05 | **Failure does not automatically trigger compensation.** Task policy chooses: keep partial result, attempt compensation, or ask the user. Analysis succeeding while report creation fails usually warrants keeping the analysis, not discarding everything. |

---

## 6. Approval and steering

### 6.1 Approval

**Approval is an execution gate object, not a chat question.**

| # | Requirement |
|---|---|
| AP-01 | An Approval binds a specific action snapshot: Task, Run, Step/Capability, target resource, resource revision where relevant, proposed effect, risk level and expiry. |
| AP-02 | **Vague future permission cannot be approved.** "Allow ArcChat to change anything for this task?" is prohibited. "Allow ArcChat to replace 12 blocks in Document X at revision 42?" is the required shape. |
| AP-03 | **Approval ≠ persistent permission** ([I-097](01-normative-glossary-and-invariants.md#rule-i-097)). A persistent grant pre-authorises a class of low-risk behaviour; an approval authorises one specific action. |
| <a id="rule-ap-04"></a>AP-04 | **Resource state is re-checked after approval.** An approval issued against revision 42 is no longer valid for that exact effect at revision 49; the action is rebased, the preview regenerated, and re-approval sought. |
| AP-05 | **Every approval expires.** An external action approved two weeks ago must not suddenly execute today. |
| <a id="rule-ap-06"></a>AP-06 | **Approval denied does not necessarily fail the Task.** The agent may choose an alternative, skip an optional step, or ask. Only an unachievable Intent ends as Failed or Canceled. |

### 6.2 Steering

| # | Requirement |
|---|---|
| SG-01 | **Steering is the user's execution-direction update to an active Task** ([I-098](01-normative-glossary-and-invariants.md#rule-i-098), [I-099](01-normative-glossary-and-invariants.md#rule-i-099)). It is neither an approval nor an ordinary conversation message. |
| <a id="rule-sg-02"></a>SG-02 | Steering produces an **immutable Steering Event**. It never overwrites the original Intent. |
| <a id="rule-sg-03"></a>SG-03 | **The original Intent is always retained.** Steering affects the future execution of the current Run only. |
| SG-04 | Steering may trigger a Plan Revision; completed Steps remain in the trace even when superseded ("✓ analysed video" stays visible after "stop analysing the video"). |
| <a id="rule-sg-05"></a>SG-05 | Steering application timing is explicit: applied immediately, queued until a safe point, or cannot be applied. It must never pretend to be instantaneous. |

---

## 7. Budget

**Budget is a first-class Task Runtime capability**, not merely a billing concern.

| # | Requirement |
|---|---|
| <a id="rule-bg-01"></a>BG-01 | **Budget ≠ Entitlement** ([I-013](01-normative-glossary-and-invariants.md#rule-i-013)). Entitlement is the maximum the user is eligible for; budget is how much this Task may spend. A workspace balance of 30,000 credits does not let one Task spend 30,000. |
| BG-02 | Budget dimensions include, at minimum: **AI credit budget**, **execution time / deadline**, **external paid tool budget**, and **operational limits** (maximum expensive capability calls, maximum generated outputs). The model must be extensible. |
| BG-03 | A Task **reserves** its budget at start and settles afterwards. Reservation is what prevents three concurrent Tasks each independently observing a sufficient balance and collectively overdrawing it. |
| BG-04 | Reservation is not deduction. Actual usage produces the credit debit; the unused reservation is released. |
| BG-05 | All calls and concurrent tools within a Run share its authorised budget. Each provider dispatch has an atomic bounded reservation; no tool receives the entire workspace balance as spend authority. |
| <a id="rule-bg-06"></a>BG-06 | On approaching exhaustion the Task may reduce its plan, use a lower-cost model, or complete a partial result. Increasing the budget **requires approval** with a stated estimate. |
| <a id="rule-bg-07"></a>BG-07 | **An agent can never raise its own budget**, regardless of what the model concludes about result quality. |
| <a id="rule-bg-08"></a>BG-08 | **Auto model routing is bounded by the Task budget.** The router chooses within policy and budget rather than spending first and explaining later. |
| BG-09 | **No negative balance, ever.** On reaching a hard limit the Task stops at a safe boundary and requests a budget extension. |
| BG-10 | Ordinary chat uses a configured per-request ceiling without a mandatory budget dialog. Extra-credit consumption requires opt-in and a maximum; workspace/user/task limits may only narrow the available service capacity. |

---

## 8. Progress, outcome and trace

| # | Requirement |
|---|---|
| <a id="rule-pr-01"></a>PR-01 | **Progress is a monotonic best estimate.** Fabricating a percentage when the true fraction is unknown is prohibited. |
| PR-02 | Three progress kinds are supported: **Determinate** (a percentage), **Milestone** (`3 / 5 phases`), **Indeterminate** ("Analysing…"). |
| PR-03 | **Percentages must not go backwards** when the plan is revised. A Run that would drop from 80 % to 32 % after adding steps switches to milestone progress instead. |
| PR-04 | **Progress and Task state are independent.** `Waiting for approval` at 70 % complete is normal. |
| PR-05 | An ETA is shown only when historical data makes it reliable, and then as a range. A persistently wrong ETA must not be displayed. |
| PR-06 | **Every terminal Task carries an Outcome Summary**: what succeeded, what failed or was skipped, what changed, artifacts produced, unresolved issues, credits and cost, and execution location. |
| <a id="rule-pr-07"></a>PR-07 | **`PartiallySucceeded` requires an outcome manifest** enumerating each outcome, so the user is never left guessing what a partial success means. |
| <a id="rule-pr-08"></a>PR-08 | **Operational Trace** is the product-level execution record: plans, actions, capability input summaries, outputs, approvals, results, costs. |
| PR-09 | **Trace ≠ Logs** ([I-276](01-normative-glossary-and-invariants.md#rule-i-276) family). Trace is a product surface; logs are operational diagnostics. They are separate systems with separate retention and separate access rules. |
| <a id="rule-pr-10"></a>PR-10 | **Trace ≠ chain-of-thought** ([I-107](01-normative-glossary-and-invariants.md#rule-i-107)). Hidden model reasoning is never surfaced as trace. |

### 8.1 Snapshot as the authority

| # | Requirement |
|---|---|
| <a id="rule-sn-01"></a>SN-01 | **Task Snapshot is the authoritative read surface.** Live events are notifications only. |
| <a id="rule-sn-02"></a>SN-02 | Task Snapshot carries revision and sequence, so a client can detect that its view is at 42 while the server is at 47, and backfill. |
| <a id="rule-sn-03"></a>SN-03 | **A lost event must never damage a Task.** Re-reading the snapshot restores the correct state. |
| SN-04 | Cloud Task snapshots are read over the public HTTP/JSON authority surface. Local IPC carries tool requests and product job references, not a second authoritative Task store. |

### 8.2 Crash recovery

| # | Requirement |
|---|---|
| <a id="rule-rv-01"></a>RV-01 | Task and Run state are persisted. After a restart an in-flight Run is marked `Interrupted` and enters recovery evaluation. |
| RV-02 | **Interrupted Steps are not blanket-retried.** The evaluation asks: was the effect committed? is the operation idempotent? is reconciliation possible? does a checkpoint exist? |
| <a id="rule-rv-03"></a>RV-03 | Recovery outcomes are: safe to resume, safe to retry, needs reconciliation, requires user decision, cannot recover. |
| RV-04 | A native product crash leaves the Cloud Agent Task waiting on an interrupted product job; Cloud history survives and recovery consults the job owner before retry. |
| <a id="rule-rv-05"></a>RV-05 | Cloud host failure preserves tasks, usage and reservations in durable storage. Another replica may resume only after acquiring fenced ownership; no duplicate model/tool dispatch from competing executors. |

---

## 9. Concurrency

| # | Requirement |
|---|---|
| <a id="rule-cc-01"></a>CC-01 | **Automation concurrency and task-step parallelism are two different layers** and must never be conflated ([I-104](01-normative-glossary-and-invariants.md#rule-i-104)). |
| <a id="rule-cc-02"></a>CC-02 | Bounded tool/Step parallelism inside one Cloud Run respects resource conflict. Reading two sessions can parallelise; two Steps editing the same document must not. |
| CC-03 | **There is no global ArcForges lock manager.** Concurrency authority belongs to the owning product: ArcNotes decides document revision and locking, ArcScope decides device and session concurrency, ArcSlate decides timeline and render resource concurrency. |
| <a id="rule-cc-04"></a>CC-04 | **Optimistic revision is the default agent concurrency mode.** `ExpectedRevision` mismatch is a Conflict. Holding a document lock for the 40-minute duration of a long Task is prohibited. |
| <a id="rule-cc-05"></a>CC-05 | Genuinely exclusive resources — single-access hardware, for instance — are governed by lease/busy semantics provided by the capability owner. |

---

## 10. Automation

**Automation is a persistent rule for when and with what configuration to create a Task. It never performs work itself.**

```
Automation Definition → Trigger Occurrence → Task → Run → Steps
```

| # | Requirement |
|---|---|
| AU-01 | **An Automation is not a long-lived Task with weekly Runs.** Week 1 produces Task A with Run A1; week 2 produces Task B with Run B1. Modelling it otherwise destroys the meaning of Retry. |
| AU-02 | An Automation Definition carries: name, enabled flag, trigger, task template, project, agent profile, input resolution rules, execution target, permission policy, budget, concurrency policy and missed-run policy. |
| <a id="rule-au-03"></a>AU-03 | **"Automate this" extracts a Task Template**, not a saved trace. It captures intent, dynamic input rules, profile, target and budget — not the particular Steps that one Run happened to plan, because the next Run may legitimately plan differently. |
| AU-04 | **Automation definitions are versioned.** A Task created yesterday stays bound to yesterday's version, including its budget. |
| AU-05 | **Disabling an Automation blocks future triggers only.** A running Task is unaffected and must be cancelled explicitly. |
| AU-06 | **Deleting an Automation does not delete historical Tasks.** Their audit value and results persist. |
| <a id="rule-au-07"></a>AU-07 | `Run Now` creates a manual Trigger Occurrence and a new Task, and does **not** shift the next scheduled time. |

### 10.1 Triggers

Supported trigger families: `Manual / Run Now`, `One-time`, `Interval`, `Cron / recurring schedule`, `App Event`, `Cloud Event`, `Device Event`, and later `External Integration Event`.

| # | Requirement |
|---|---|
| <a id="rule-tg-01"></a>TG-01 | **A time trigger always carries a time zone.** Storing `09:00` without a zone is prohibited. |
| <a id="rule-tg-02"></a>TG-02 | **DST has explicit semantics** for non-existent and repeated local times. The behaviour must not depend on how the host operating system happens to interpret that day. The product model carries schedule time zone plus a DST resolution policy. |
| <a id="rule-tg-03"></a>TG-03 | **A Trigger Occurrence has a stable identity.** A scheduler restart must not fire the same scheduled occurrence twice. |
| <a id="rule-tg-04"></a>TG-04 | **An event trigger deduplicates by event id.** The same anomaly delivered twice must not create two Tasks. |

### 10.2 Missed runs and concurrency

| # | Requirement |
|---|---|
| MR-01 | Missed-run policy is one of `Skip`, `RunOnceWhenAvailable`, `CatchUp`, `Ask`. |
| <a id="rule-mr-02"></a>MR-02 | **Catch-up is bounded.** A machine offline for three months must not return and immediately run 90 daily Tasks. A maximum catch-up count and window are mandatory. |
| MR-03 | Concurrency policy is one of `SkipIfRunning`, `Queue`, `Replace`, `AllowConcurrent`. The recommended default for recurring automations is **`SkipIfRunning`**, because a daily job that takes more than a day would otherwise build an unbounded queue. |
| MR-04 | **`Replace` is cooperative**: request cancellation of the old Task, observe per safety policy, then start the replacement. Killing and immediately restarting risks overlapping side effects. |
| MR-05 | **`AllowConcurrent` must be chosen explicitly.** It is never the default for expensive AI, same-document modification or device control. |

### 10.3 Loop and storm protection

| # | Requirement |
|---|---|
| <a id="rule-lp-01"></a>LP-01 | **Every trigger carries a causation chain**: this event was caused by this Task, caused by this Automation. |
| LP-02 | **Self-recursive automation is suppressed by default**: an automation whose own output matches its own trigger does not re-fire. |
| <a id="rule-lp-03"></a>LP-03 | Cross-automation loops are guarded by **causation depth**, **rate guards** and cycle detection where feasible. `A creates a note → B sees the note and creates a finding → A sees the finding → …` must be stopped. |
| <a id="rule-lp-04"></a>LP-04 | Storm protection is mandatory: per-automation rate limit, per-workspace concurrency cap, global agent concurrency cap, AI budget cap. A malformed event must not be able to generate an unbounded number of Tasks. |
| <a id="rule-lp-05"></a>LP-05 | Automation budget is two-level: a **per-run budget** and an **aggregate budget** (per period). Reaching the aggregate budget pauses the Automation into Needs Attention. |

### 10.4 Automation and permission

| # | Requirement |
|---|---|
| <a id="rule-ap-10"></a>AP-10 | **Creating an automation does not grant it permanent unlimited authority** ([I-236](01-normative-glossary-and-invariants.md#rule-i-236)). Each Task it creates passes the current security policy, persistent grants, risk policy and approval rules. |
| AP-11 | Persistent grants inside an automation are **narrowly scoped**: "may append to the 'Weekly Reports' notebook" rather than "may write anywhere in ArcNotes forever". |
| AP-12 | **External-effect automations are strictest.** Publishing, sending email or modifying an external service must select one of: always approve, approve first run, or allow within an explicitly scoped policy. High-risk external actions never run unattended by default. |

### 10.5 Cloud automation and native jobs

| # | Requirement |
|---|---|
| <a id="rule-la-01"></a>LA-01 | Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): no desktop AI automation scheduler or offline autonomous agent mode. Ordinary native jobs may run without AI. |
| LA-02 | AI automation is scheduled by the C# Cloud Task module and requires an active paid service term plus capacity/budget. Device-originated events become durable deduplicated Cloud triggers. |
| LA-03 | A Cloud automation requiring an offline desktop waits on that device under its bounded missed-run policy. It never starts a local agent as fallback. |

### 10.6 One Task Center

All Tasks — manual, automation-created, remote — appear in one Task Center. Origin is a filter, not a separate page. Filters: origin, automation, project, device, app, execution location, status, date. The Automation page owns **definition** (schedule, policy, budget) and links each run-history entry to its Task.

**Deleting Task history never deletes professional resources.** An ArcNotes document, ArcScope report or ArcSlate video produced by a Task survives the deletion of that Task's history.

---

## 11. AI business model

All model execution uses the Cloud-operated provider adapter. Official users purchase a paid service term; included capacity and authorised extra credits fund requested inference. Desktop, Web and Mobile never expose provider-key entry.

The real metering and capacity contract is **[commerce §8.4–§8.6](04-commerce-entitlement-and-credits.md)**. Operational prices and limits are **[external deployment configuration](11-policy-and-configuration.md)**. No local AI, end-user BYOK, agent team or external-agent payer route exists.

| # | Requirement |
|---|---|
| AI-01 | Official AI requires an active paid service term and available capacity/budget; included capacity replenishes over time and extra credits require opt-in. Limits are visible. |
| AI-02 | No direct desktop-to-provider call or end-user BYOK. Provider errors cannot select a user credential. |
| AI-03 | Cloud fallback stays within authorised destinations, model class, tariff and budget; it cannot enable extra-credit spending. |
| AI-04 | Every AI entry point authenticates a realm/workspace. An independent self-host uses deployment-operator credentials and its own policy; it grants no official access. |
| AI-05 | Capacity and credits are shared by the single workspace owner across devices and products. |
| AI-06 | No credit transfer across users, workspaces or realms. |
| AI-07 | Purchase/spend velocity, concurrency and provider exposure have server-enforced configurable limits with actionable reasons. Buying credits does not bypass them. |

---

The active-service rule for official versus self-hosted realms is specified in [commerce §8.7](04-commerce-entitlement-and-credits.md#87-service-eligibility-across-realms).

### 11.1 Credit definition and precision

| # | Requirement |
|---|---|
| CD-01 | The **grant ratio** (how many credits a purchase amount yields) is versioned commercial policy under **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)**. V1 uses a simple linear purchase conversion with **no bonus tiers**, because that keeps refunds, lot valuation and reconciliation simple and avoids distinguishing bonus credits. The numeric ratio remains versioned configuration. |
| CD-02 | **A credit is not cash.** The legal and product definition is: non-transferable prepaid service usage units with no cash value, not withdrawable, not tradable, not currency, usable only for Arc Managed AI. |
| <a id="rule-cd-03"></a>CD-03 | Internal accounting uses integer micro-credits (1 credit = 1,000,000 micro-credits). UI summaries may be compact, but detailed usage exposes the settled fractional amount and source allocations. Display rounding never changes billing or shows a positive charge as exact zero. |
| CD-04 | **Credits must not obscure cost.** Tariffs are published, tasks are estimated, usage history is itemised, capacity recovery and compensation expiry are visible, with purchased credits retained across service lapse. Credits exist to unify billing units across providers, never to hide price. |

### 11.2 Tariffs

| # | Requirement |
|---|---|
| TR-01 | Supplier cost, customer tariff, subscription price and credit purchase conversion are independent versioned data. No universal markup, fixed price ratio or assumption that subscription revenue equals an AI budget. |
| TR-02 | Customer tariff rates and any derivation factors are validated external configuration under [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020) and P2-006. Official operating values need no private code repository; historical customer snapshots remain immutable. |
| <a id="rule-tr-03"></a>TR-03 | Retail tariffs are **versioned**: `RetailTariffVersion` with validity windows. Every request binds its tariff version, so any historical charge is exactly recomputable. |
| <a id="rule-tr-04"></a>TR-04 | **A Run locks a retail tariff snapshot at start.** A mid-run upstream price change does not change the rate that Run is charged at; ArcForges absorbs the variance and the new price applies from the next Run. Ordinary chat locks per message; automation locks per Automation Run. |
| TR-05 | The cost model is always built against **normal, sustainable provider prices**. Provider promotions, free quotas and startup credits are treated as **margin bonus** and must never be used to set permanent product pricing or allowances. |
| TR-06 | A significant tariff increase is notified in advance. A sudden extreme upstream increase may temporarily remove a model from automatic routing or require confirmation, rather than letting automation burn silently. |
| TR-07 | Upstream-price changes require verified operational evidence and a new supplier-rate publication. A retail-tariff change is a separate deliberate publication; updating supplier cost never automatically changes customer prices. |
| TR-08 | **Purchased credit balances never change because a model's price changed.** What changes is how many credits a future call costs. |

**Metering precedence.** Commerce [MT-01](04-commerce-entitlement-and-credits.md#rule-mt-01)–[MT-16](04-commerce-entitlement-and-credits.md#rule-mt-16) and [AC-01](04-commerce-entitlement-and-credits.md#rule-ac-01)–[AC-12](04-commerce-entitlement-and-credits.md#rule-ac-12) govern usage normalisation, unknown outcomes, fixed precision, capacity recovery and extra-credit admission. Economic summaries below do not add product capability commitments.

### 11.3 Cost dimensions

An enabled model route prices every applicable billable category/tier. The following vocabulary is not a list of new product features; unsupported generation/computer-use routes remain excluded unless separately brought into scope:

`Input` · `Cached Input` · `Cache Write` · `Output` · `Reasoning` · `Image Input` · `Image Output` · `Audio Input` · `Audio Output` · `Video` · `Tool Call` · `Search` · `Computer Use` · `Context Tier` · `Processing Tier` · `Region`

| # | Requirement |
|---|---|
| CO-01 | An enabled route must declare all applicable context/processing/region pricing tiers and their calculation basis. Unsupported/unpriced billable cases are refused before dispatch. |
| CO-02 | Actual cached and uncached usage is distinguished and charged under the published category tariff; overlapping counters are normalised without double charging. Supplier discounts and customer tariffs remain separate records. |
| <a id="rule-co-03"></a>CO-03 | **Cache isolation is a security requirement.** User-data-derived cache is workspace-scoped. Only genuinely public content — system prompts, public tool schemas, fixed instructions — may be reused across workspaces. |
| <a id="rule-co-04"></a>CO-04 | Long-context requests are **flagged to the user in advance** ("a large context will increase credit usage"), not discovered after the fact. |
| CO-05 | Multimodal consumption follows actual supplier units: tokens when token-billed; explicit image/second/call quantities when independently billed. Never invent token counts or charge tokenised media twice. |
| CO-06 | **Paid tools are part of the budget.** Web search and similar tools carry their own per-call cost alongside token cost, and task budgets estimate them together. |
| CO-07 | **Cloud search and web search are distinguished in the interface.** Searching ArcForges Cloud is a subscription feature and consumes no credits; searching the web may consume credits. Labelling both "Search" leaves the user unable to explain a charge. |

### 11.4 What consumes credits

| Consumes credits | Absorbed as ArcForges cost of goods |
|---|---|
| Chat responses | Cloud search embedding, indexing and reranking |
| Agent reasoning | Internal routing model calls |
| Selection-scoped document actions | Abuse classification |
| Supported media-understanding requests | Health checks |
| Web search on the user's behalf | Cost prediction |
| User-requested transcription | Platform-caused retry with no user value |

| # | Requirement |
|---|---|
| <a id="rule-cu-01"></a>CU-01 | **Internal platform AI never deducts user credits.** A cheap routing classifier deciding "is this ArcNotes or ArcScope?" is platform overhead. |
| <a id="rule-cu-02"></a>CU-02 | **Cloud search embedding never deducts credits.** Synchronising 100 notes must not silently cost the user credits; semantic search is a subscription capability. |
| <a id="rule-cu-03"></a>CU-03 | **Platform-caused retry is not charged to the user.** A logical AI request whose first provider attempt failed and second succeeded is charged for the useful work, not twice. |
| <a id="rule-cu-04"></a>CU-04 | User cancellation settles verified consumption already incurred within the authorised limit and releases unused holds. Unknown consumption is reconciled under commerce [MT-12](04-commerce-entitlement-and-credits.md#rule-mt-12); no assumed zero or surprise overdraft. |
| CU-05 | A provider safety block or other non-delivery with no usable result creates no customer debit, or an idempotent compensating adjustment if already settled. Actual supplier usage/cost is retained. Caller cancellation follows [CU-04](#rule-cu-04) instead. |

### 11.5 Routing

```
Arc AI Control Plane
      ↓
AI Gateway (analytics, caching, rate limiting, retry, fallback, spend limits)
      ↓
Direct provider accounts (primary)   →   Aggregator (long-tail, new models, fallback)
```

| # | Requirement |
|---|---|
| <a id="rule-rt-01"></a>RT-01 | **Infrastructure is not the product model.** A gateway vendor's concepts must never leak into ArcForges domain contracts, and its dashboard is never the business ledger. |
| RT-02 | High-volume mainstream models route through **direct provider accounts**, because aggregator platform fees are real cost of goods at volume. |
| RT-03 | An aggregator serves long-tail models, brand-new models and emergency fallback. |
| <a id="rule-rt-04"></a>RT-04 | Gateway spend limits are a **second-line safety guard**, valuable but not authoritative. The customer credit ledger is always held by ArcForges. |
| RT-05 | **Auto routing has explicit cost classes** — for example Fast, Balanced, Best — each with a stated cost ceiling, plus an explicit model chooser. |
| <a id="rule-rt-06"></a>RT-06 | **Auto must not silently escalate to a far more expensive model.** Escalation beyond the class ceiling requires an explicit user allowance for that task. |
| <a id="rule-rt-07"></a>RT-07 | **Fallback respects the cost ceiling.** A failed cheap model does not silently fall back to a premium model; fallback stays within the tariff class or asks before escalating price. |
| <a id="rule-rt-08"></a>RT-08 | **An explicitly chosen model's identity is honoured.** If the user selects a specific model, a different model must never be substituted for cost reasons. The provider *route* for that model may change (for example a different compliant channel for the same model); the model itself may not. |
| <a id="rule-rt-09"></a>RT-09 | The managed model catalogue is deliberately small and curated at launch, not an exhaustive provider list. |
| RT-10 | Very expensive specialist models are **explicit opt-in only** and never enter automatic routing. |
| RT-11 | **Model alias and model snapshot are separate** ([I-364](01-normative-glossary-and-invariants.md#rule-i-364)). "Auto Balanced" may change over time; "\<specific model\>" is a user choice. Reproducible tasks record the concrete provider model identifier and snapshot. |
| RT-12 | **Model retirement does not affect purchased credits.** The user bought Arc AI Credits, not a quantity of one provider's tokens. |
| <a id="rule-rt-13"></a>RT-13 | **History is immutable after retirement.** A historical Task retains its model identifier, provider route and tariff version permanently, even years after the model ceases to exist. |

### 11.6 Context engineering

The most effective cost control is sending fewer meaningless tokens, not reducing margin. Required techniques: semantic retrieval, conversation compaction, project context selection, relevant capability selection, prompt caching, output limits, and cheap-model routing for simple steps.

| # | Requirement |
|---|---|
| <a id="rule-ce-01"></a>CE-01 | **The full capability catalogue is never handed to the model.** With hundreds of capabilities across products, sending every tool schema each round degrades quality and explodes cost. The flow is: intent and capability discovery → select relevant applications → select a small relevant capability set → invoke the agent. |

### 11.7 Ledgers and reconciliation

| # | Requirement |
|---|---|
| <a id="rule-lg-01"></a>LG-01 | **Three separate records exist per AI request**: an **AI Usage Record** (what was used), an **Upstream Cost Record** (what ArcForges actually paid), and a **Credit Ledger** entry (what the user was charged). `credits -= 20` alone is insufficient. |
| LG-02 | The full chain is traceable: `Task → AI Request → Provider Route → Model → Usage → Upstream Cost → Retail Tariff → Credit Debit`. |
| <a id="rule-lg-03"></a>LG-03 | **Logical AI Request ≠ Provider Attempt ≠ Step Attempt.** All three are distinct and none may be merged. |
| LG-04 | Refunds, compensation and provider corrections produce **Adjustments**, never rewritten history. |
| LG-05 | **Provider invoice reconciliation is mandatory.** Internal computed cost is compared against the provider's bill, and divergence is investigated (reasoning tokens, tool cost, region pricing, provider rounding, wrong price version, retries). Discovering a months-old miscalculation is a failure of this control. |
| LG-06 | Daily operational metrics cover commerce (AI revenue, credits sold, credits consumed, deferred credit balance), cost (upstream cost, per provider, per model, tool cost, retry loss, fallback loss) and margin (gross AI margin, contribution margin, margin by model, margin by pack). |
| LG-07 | Efficiency metrics include cache hits, input/output ratio, context length, cost per completed/failed Task, tool concurrency, retry cost and model fallback rate. No sub-agent metric or corresponding runtime is required. |
| LG-08 | **Automated cost alerts** fire on abnormal upstream price movement or margin falling below threshold. Noticing a price change by occasionally reading a vendor page is not a control. |
| <a id="rule-lg-09"></a>LG-09 | **Provider prepaid balance is monitored and alerted.** Managed AI must not depend on a provider free tier, and must not fail because an upstream balance silently ran out. |
| LG-10 | **AI working capital** is planned: credits are sold before the upstream cost is incurred, so a reserve policy is required. |
| LG-11 | Provider volume discounts are not automatically passed straight through to retail price; they are absorbed as margin until a deliberate pricing decision says otherwise. |

### 11.8 User-facing transparency

- An **AI Usage** page showing, separately: included capacity remaining, recovery timing and applicable rate/concurrency limits; purchased credit balance; and a recent breakdown by source (agent, product feature, web search).
- **Task detail** showing per-model and per-tool credit usage with a total, and a "view details" affordance for advanced users. Provider invoice detail is not shown to ordinary users.
- A **model selector** showing relative cost class, expandable to the exact per-unit tariff. Users must be able to make an informed choice.

---

## 12. Scope and realm

| # | Requirement |
|---|---|
| <a id="rule-sc-01"></a>SC-01 | Every Agent Task has one explicit realm and single-owner workspace. Resource and billing authority never cross workspaces implicitly. |
| SC-02 | No local-only Agent Task. Native offline editing, rendering and acquisition are product jobs with their own domain references. |
| SC-03 | A Cloud task may reference explicitly authorised device-local media or captures through tools. Billing never grants data access and never makes local bytes automatically cloud-resident. |

---

## 13. Domain model

```
Intent
Task · TaskOrigin · TaskActor · TaskOwner · TaskPolicy · TaskOutcome
Run · ExecutionSnapshot · ExecutionTarget · ExecutionLocation
Plan · PlanRevision
Step · StepDependency
Attempt · FailureReason · EffectCertainty
CapabilityInvocation · LogicalCommand · CapabilityResult
LogicalAIRequest · ProviderAttempt
ProductJobReference
ExecutionCheckpoint · DomainCheckpointReference · CompensationAction
ApprovalRequest · ApprovalDecision · SteeringEvent
Budget · BudgetReservation · BudgetUsage
Progress · TaskSnapshot · TaskEventSequence
AutomationDefinition · AutomationVersion · TaskTemplate
TriggerDefinition · TriggerOccurrence · TriggerPayload
MissedRunPolicy · ConcurrencyPolicy · DynamicInputSelector
Causation · Correlation

AIProvider · AIModel · AIModelVersion · ProviderRoute
ProcessingTier · ContextPricingTier
UpstreamPrice · UpstreamPriceVersion · RetailTariff · RetailTariffVersion
AICredit · CreditLot · CreditReservation · CreditDebit · CreditAdjustment · CreditRefundHold
AIUsageRecord · AIUsageMetric · UpstreamCostRecord · CostAdjustment
TaskAIBudget · WorkspaceSpendPolicy · RoutingPolicy · ModelCostClass
ProviderBalance · CostReconciliation · CostAlert · AIMarginSnapshot
```

---

## 14. Acceptance scenarios

### Execution
Intent that stays a chat turn · intent that becomes a Task · Run 1 fails and Run 2 succeeds under one `TaskId` · profile edited mid-run does not affect the running Run · plan revised with reason recorded · parallel Steps on a DAG · Step retried as a new Attempt · write capability retried under one `CommandId` producing exactly one document.

### Lifecycle
Waiting for network with auto-resume · waiting for approval without auto-resume · paused by user then resumed on the same Run · interrupted by crash then recovery-evaluated · succeeded only when the outcome is truly reached · partially succeeded with an outcome manifest · cancelled after a completed side effect, with effects listed · cancel requested during a non-cancellable step.

### Failure and effect
Transient retried within bounds · conflict rebased and re-approved · permission denied not retried · capability unavailable resolved by launching the app · version incompatible surfaced actionably · external effect unknown reconciled before any retry.

### Approval and steering
Approval bound to a specific revision · approval invalidated by a revision change · approval expiring · approval denied with an alternative path · steering event recorded immutably · original intent preserved · completed steps retained after contrary steering.

### Budget
Task reserves and settles · three concurrent tasks cannot collectively overdraw · all concurrent tools share one Run budget · budget exhaustion pauses and asks · agent cannot raise its own budget · routing constrained by budget · hard stop with no negative balance.

### Automation
Weekly automation producing distinct Tasks · disabled automation leaves a running Task alone · deleted automation retains history · missed run per each policy · bounded catch-up · `SkipIfRunning` default · cooperative replace · self-recursion suppressed · cross-automation loop halted by causation depth · storm caps enforced · aggregate budget pausing the automation · DST transition with defined semantics · scheduler restart not double-firing · duplicate event not double-creating.

### AI pricing and usage
Ordinary input/output · cached input · cache write · reasoning tokens · context crossing a pricing threshold · priority tier · batch tier · region surcharge · provider price change mid-catalogue · promotional price expiring · streaming completing · user cancelling mid-stream · provider failure with no upstream charge · provider failure with partial upstream charge · automatic retry not charged to the user · model fallback within class · concurrent tool accounting · enabled tool/search billing dimensions · supported media-understanding routes only. Unscoped image/video generation is not a delivery obligation.

### Credits
Capacity recovers only in paid intervals · annual renewal does not reset capacity · separate purchased/compensation lots · disclosed source-order consumption · concurrent reservations · insufficient balance hard stop · partial refund · refund hold · compensation credit · **model retired but credits unaffected** · historical task retaining its retired model and tariff version.

### Cloud-only service boundary
No local/provider-key mode or external-agent delegation · native render/capture without Agent Task · direct product Cloud AI without ArcChat Desktop · paused/expired service stops new model calls even with credits · a self-host policy cannot unlock official AI.

---

## 15. Traceability

| Current document | Relationship |
|---|---|
| [Agent Harness](../architecture/17-agent-harness.md) | Implements the single Cloud model/tool loop and its failure handling |
| [AI and Agent Runtime Architecture](../architecture/09-ai-and-agent-runtime-architecture.md) | Defines execution state, placement, provider routing and automation |
| [Commerce, Entitlement and AI Credits Requirements](04-commerce-entitlement-and-credits.md) | Owns the commercial admission and metering obligations |
| **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** | Every economic figure is versioned commercial policy; reserve-then-settle; hard stop; three separate ledgers; per-run tariff snapshot |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Local action is a durable `ToolRequest` pulled and re-authorised by ArcChat Desktop |
| **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** | MCP task/skill vocabulary is disambiguated in the glossary and never conflated with this model |
