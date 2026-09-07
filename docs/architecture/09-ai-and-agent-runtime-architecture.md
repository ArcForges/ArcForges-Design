# AI and Agent Runtime Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **D-008** (agent framework only on AOT-validated surfaces), **D-010** (remote execution), **D-020** (economic model), **V-02** (MCP)
> Companions: [`../requirements/05-ai-and-agent-execution.md`](../requirements/05-ai-and-agent-execution.md), [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`16-billing-and-commerce-architecture.md`](16-billing-and-commerce-architecture.md)

One Cloud Harness, one Task model, one metering path. Tool locality varies; the model loop never leaves Cloud (**P2-006**, `I-491`).

---

## 1. Component map

**Every model call, the single Harness and all durable agent orchestration are Cloud** (**P2-006**). The desktop contributes UI, authorised local tool execution and product-local jobs. There is no second agent runtime anywhere.

```
+----------- ArcChat / product desktop -----------+   +------- ArcForges Cloud Host -------+
| Presentation and command surfaces               |   | THE HARNESS  (single, Cloud-only)  |
|  - conversation, task and approval UI           |   |  - turn loop and tool protocol     |
|  - product AI entry points (selection-scoped)   |   |  - context assembly                |
|                                                 |   |  - capability selection            |
| Local tool executor                             |   |  - approval interleaving           |
|  - pulls authorised ToolRequests                |<--|  - ToolRequest issuer              |
|  - re-authorises locally, executes, returns     |-->|  - trace recorder                  |
|                                                 |   |                                    |
| Product job runner  (NOT an agent runtime)      |   | AI control plane                   |
|  - render, capture, index, export               |   |  - routing and tariff resolution   |
|  - owns its own progress and recovery           |   |  - admission, capacity, credits    |
+-------------------------------------------------+   |  - usage and supplier cost records |
                                                       |  - provider adapters (operator-    |
                                                       |    funded credentials only)        |
                                                       +------------------------------------+
```

| # | Rule |
|---|---|
| CM-01 | **There is one Task model and one Harness, both Cloud-owned** (**P2-006**). Tool *locality* varies; the model loop does not (`I-491`). |
| CM-02 | **No desktop, mobile or browser client runs a model loop, holds provider credentials or plans agent work.** A client proposes intent and executes authorised tools. |
| CM-03 | **The credit ledger is always cloud-side and always ArcForges-owned** (`RT-04` in the AI requirements). A gateway's dashboard is never the business ledger. |
| CM-04 | **A Cloud Agent Task and a native Product Job are different things** (`I-121`, `I-485`). A render, a capture, an index rebuild and an export are product jobs: they invoke no model, consume no AI capacity, and are owned and recovered by the product that runs them. |
| CM-05 | **Product AI entry points call the Cloud AI surface directly** with minimal authorised context (`§4.5` of the product scope). They do not require ArcChat Desktop and do not constitute a second orchestrator. |
| CM-06 | **Official inference requires an active paid service term** (`C-03`, `§8.7` of the commerce requirements). No local mode, desktop setting, credit balance or self-host flag can authorise it.

---

## 2. Agent runtime under AOT

**D-008** and `I2 §I.3` resolve the AOT/JIT tension explicitly.

| # | Rule |
|---|---|
| AO-01 | **Built-in agents, tools and capabilities are statically registered or source-generated.** |
| AO-02 | **Arbitrary runtime assembly scanning, dynamic proxies and runtime code generation are prohibited** in the ArcChat main process. |
| AO-03 | **Third-party executable extensions run out of process by default** (`EX-01` in the extension requirements), so they may use any runtime while the host stays a Native AOT deliverable. |
| AO-04 | **An agent framework feature is enabled only on surfaces validated by AOT analysis and a real publish** — never assumed from a debug build. |
| AO-05 | **A capability is exposed to the model through an explicitly generated binding**, not through runtime reflection over method signatures. |
| AO-06 | **Where a framework feature cannot be made AOT-safe, the surface is narrowed or the feature is replaced** — the desktop is not silently downgraded to JIT while still being described as AOT (`§23.4` of `I3`). |

---

## 3. Capability registry

```
Static contribution manifests (readable before start-up)
        +
Runtime instance registrations (availability, health, contract set)
        =
Capability Registry  →  filtered by intent, permission, entitlement, policy, budget
                     →  a small relevant tool set exposed to the model
```

| # | Rule |
|---|---|
| CR-01 | **The full catalogue is never handed to the model** (`CE-01` in the AI requirements). Hundreds of tool schemas per turn degrade quality and explode cost. |
| CR-02 | **Selection is a pipeline**: intent and capability discovery → relevant products → a small relevant capability set → invoke. |
| CR-03 | **Capability metadata drives behaviour**, not the model's inference: execution shape, effect semantics, retry semantics, cancellation semantics, preview support, checkpoint support, compensation support, risk and scope (`§4.2` of the contracts architecture). |
| CR-04 | **Invocation ordering is fixed**: native capability → trusted connector, MCP or API → computer use as an advanced fallback (`§8.1` of the ArcChat requirements). |
| CR-05 | **A capability's availability is dynamic** and reflects installation, running state, health, compatibility, permission, entitlement and policy (`AC-04` in the contracts architecture). |

---

## 4. Task engine

### 4.1 Structure

```
Intent
 └── Task            durable, owned, one authoritative owner
      └── Run        one execution attempt; freezes an Execution Snapshot at start
           ├── Plan Revision (retained, reasoned)
           │    └── Step (DAG)
           │         └── Attempt
           │              └── Capability Invocation / AI Request / Child Task / Gate / Wait
           └── Checkpoints, budget reservation, trace
```

| # | Rule |
|---|---|
| TE-01 | **Task, run, plan, step and attempt are separate persisted entities** (`I-080`–`I-085`). |
| TE-02 | **A run freezes its execution snapshot at start** (`EX-05` in the AI requirements): intent version, profile version, skill versions, model and routing policy, permission policy, budget, execution target, workspace and realm, input bindings, automation version, **and the resolved policy and tariff decisions**. |
| TE-03 | **One active run per task** (`EX-04` there). |
| TE-04 | **Plan revisions are retained with categorised reasons** (`EX-06` there). |
| TE-05 | **Steps form a DAG**; the interface presents an ordered checklist (`EX-08` there). |
| TE-06 | **State is `LifecycleState + Reason facet`**, so adding a wait reason never changes the state machine (`§2.1` there). |
| TE-07 | **Task authority never migrates** (`OW-02` there). Remote continuation is a cloud root task referencing a local child task. |

### 4.2 Persistence

| # | Rule |
|---|---|
| TP-01 | **Task, run, plan, step, attempt, approval, steering event, budget reservation and trace entry are all durable**, on the owner's side. |
| TP-02 | **A process crash leaves an interrupted run that enters recovery evaluation** (`RV-01`–`RV-03` there), never a blanket retry. |
| TP-03 | **A cloud worker crash does not lose a task** (`RV-05` there). |
| TP-04 | **The task snapshot is the authoritative read surface**, carrying revision and sequence (`SN-01`, `SN-02` there). |
| TP-05 | **Realtime progress is notification only** (`SN-03` there). |

### 4.3 Idempotency

| Identity | Scope |
|---|---|
| `CommandId` | The logical write action — stable across attempts |
| `InvocationId` | This actual call |
| `AttemptId` | This execution try of a step |
| Provider attempt id | This upstream request try |

**A write retried after an ambiguous failure re-sends the same `CommandId`**, and the owner deduplicates (`ID-01` there). **Effect certainty** — `NotApplied`, `Applied`, `Unknown` — governs whether retry is even permitted (`FL-07` there).

---

## 5. Context assembly

```
Explicit attachments  ·  pinned context  ·  project context  ·  temporary context
        ↓ scope resolution (explicit → project → profile → nothing)
        ↓ knowledge policy filter (searchable · AI retrieval · managed AI processing)
        ↓ permission filter (authorization-aware retrieval)
        ↓ retrieval (hybrid: lexical + semantic + metadata, with budget and per-source cap)
        ↓ revalidation against the authoritative owner
        ↓ evidence assembly (bound to source, revision, anchor, permission decision)
        ↓ Context Pack  → the model
```

| # | Rule |
|---|---|
| CA-01 | **There is no ambient default scope** (`AS-02` in the knowledge requirements). |
| CA-02 | **Scope expansion is visible and enters the retrieval trace** (`AS-05`, `AS-06` there). |
| CA-03 | **References are retrieved first; content is materialised last** (`CP-02` there). |
| CA-04 | **An automation's scope freezes into the run's evidence scope** (`AS-07` there). |
| CA-05 | **Cache isolation is a security requirement**: user-derived prompt cache is workspace-scoped; only genuinely public content is reused across workspaces (`CO-03` in the AI requirements). |
| CA-06 | **Conversation compaction is context engineering, not memory** (`HM-03` in the ArcChat requirements). |
| CA-07 | **Only acknowledged Cloud revisions are packable** (`I-498`, `PK-04` of the harness). Content that exists only on a device — an unenrolled notebook, a local-only ArcScope capture, an ArcSlate media file, an edit not yet acknowledged — **is not context**, and the pack states its absence rather than quietly assembling less evidence. Enabling AI never causes an upload (`OW-08` of the AI requirements, `I-182`). |

---

## 6. Provider routing

Providers are reached with **deployment-operator credentials only**. End-user BYOK does not exist in any form (`BY-01`–`BY-04` of the commerce requirements, `I-015` retired).

```
Logical AI Request  (Cloud, authorised, service term verified)
   -> resolve model (explicit pin honoured; Auto routes within its cost class)
   -> resolve supplier price version applicable at dispatch
   -> resolve customer retail tariff snapshot and pin it to the Run/request
   -> admission: capacity + credits + concurrency + provider budget, reserved atomically
   -> resolve provider route (direct primary; aggregator for long tail and fallback)
   -> Provider Attempt 1 ... N
   -> usage normalisation -> supplier cost record + customer settlement + ledger entries
```

| # | Rule |
|---|---|
| PR-01 | **Provider and model are separate axes** (`I-116`). The source axis is gone: there is exactly one source, the operator-funded Cloud provider set. |
| PR-02 | **An explicitly pinned model is never substituted** (`RT-08` in the AI requirements). The provider route may change; the model may not. |
| PR-03 | **Auto routing is bounded by cost class, policy and task budget** (`RT-06`, `BG-08` there). |
| PR-04 | **Fallback stays within the tariff class or asks before escalating price** (`RT-07` there). |
| PR-05 | **Supplier price and customer tariff are resolved separately and never derived from one another** (`MT-06`). The supplier version applies at dispatch; the customer snapshot pins to the Run. |
| PR-06 | **A gateway is infrastructure, never a domain concept** (`RT-01` there), and never a single point of failure — a direct-provider bypass exists (`§7` of the cloud product requirements). |
| PR-07 | **`Logical AI Request ≠ Provider Attempt ≠ Step Attempt`** (`LG-03` there, `MT-02`). |
| PR-08 | **Model availability is policy, not health** (`I-361`), and a task snapshots its model policy decision (`PA-07` in the policy requirements). |
| PR-09 | **An emergency model suspension may interrupt future invocations inside a running run** — the single documented exception to snapshot immutability (`PA-08` there). |
| PR-10 | **A route with no configured price for a billable category cannot be dispatched** (`DC-05`, `MT-15`). There is no assumed zero rate and no silent default.

---

## 7. Metering and budget

```
Task start
 → estimate → reserve from the credit ledger (Available → Reserved)
 → execute; each logical request debits actual usage at the locked tariff
 → completion: settle actual, release the remainder
 → hard stop at exhaustion; no negative balance ever
```

| # | Rule |
|---|---|
| MB-01 | **Reservation precedes execution** (`CR-20` there), which is what prevents concurrent tasks from collectively overdrawing. |
| MB-02 | **Multi-agent runs share one reservation pool** (`BG-05` there). |
| MB-03 | **Three records per request**: usage, upstream cost, credit debit (`LG-01` there). |
| MB-04 | **Every request binds a tariff version** (`TR-03` there), so any historical charge is exactly recomputable. |
| MB-05 | **A run locks its tariff snapshot at start** (`TR-04` there); mid-run upstream price changes are absorbed. |
| MB-06 | **Fixed-precision sub-credit accounting**; per-request rounding up is prohibited (`CD-03` there). |
| MB-07 | **Platform-caused retries are not charged to the user** (`CU-03` there). |
| MB-08 | **Internal platform AI — routing classifiers, embedding, reranking, safety, health, cost prediction — never debits user credits** (`CU-01`, `CU-02` there). |
| MB-09 | **An agent cannot raise its own budget** (`BG-07` there). |
| MB-10 | **Three ledgers stay separate**: provider cost, customer credit, payment/revenue (`I-011`). |

---

## 8. Approval and steering integration

| # | Rule |
|---|---|
| AS-01 | **An approval gate is a Step**, not an out-of-band interruption. The run enters `Waiting` with reason `Approval` and `AutoResume = false` (`ST-01` there). |
| AS-02 | **The approval binds the action snapshot including target revision and a parameter digest** (`AP-02` in the security architecture). |
| AS-03 | **A revision change invalidates the approval**; the action is rebased, the preview regenerated, approval re-requested (`AP-04` in the AI requirements). |
| AS-04 | **Steering produces an immutable event** that may trigger a plan revision; the original intent is never rewritten (`SG-02`, `SG-03` there). |
| AS-05 | **Steering application timing is explicit** — applied, queued to a safe point, or not applicable (`SG-05` there). |
| AS-06 | **A denied approval does not automatically fail the task** (`AP-06` there). |

---

## 9. Tool locality and remote execution

Placement no longer describes where the model loop runs — it always runs in Cloud (`I-491`). It describes **where an individual tool executes**.

| Tool locality | Executed by | Reached how |
|---|---|---|
| **Cloud tool** | The Cloud host itself | In-process, inside the Harness turn |
| **Device tool** | An authorised desktop, through ArcChat Desktop's local tool executor | Durable `ToolRequest` pulled by the device (**D-010**) |

| # | Rule |
|---|---|
| PL-01 | **Every Task is Cloud-owned.** There is no local, hybrid or auto *task placement*; the only variable is each tool's locality. |
| PL-02 | **A tool declares its locality**, and a tool that requires the device is never silently substituted by a cloud approximation. |
| PL-03 | **A device tool with no eligible online device enters `WaitingForDevice`** with a stated reason and a bounded wait (`RX-02` in the cloud requirements). Waiting consumes no model capacity (`AC-05`). |
| PL-04 | **Remote execution is a durable `ToolRequest` pulled by the desktop, re-authorised locally, answered with an idempotent `ToolResult`** (**D-010**, `§10` of the cloud architecture). Cloud never connects to a device. |
| PL-05 | **A device tool never uploads local-only data merely to make a cloud alternative possible** (`OW-08` in the AI requirements). If the data cannot leave, the tool runs on the device or the step fails with a reason. |
| PL-06 | **A cloud failure never silently performs an external side effect on a desktop** (`OW-09` there), and the reverse is equally prohibited. |
| PL-07 | **A native Product Job is not a tool locality.** A render, capture or export started by the user is owned and recovered by its product (`CM-04`); the Harness may *observe* one through a status tool, never adopt it as a Step.

---

## 10. Child tasks and long-running capabilities

```
Parent Step invokes a long-running capability
  → the owner returns a TaskHandle
  → the parent step enters Waiting(ChildTask)
  → the parent observes the child by snapshot and events
  → completion: the parent receives result, ResourceRef, ArtifactRef, outcome
```

| # | Rule |
|---|---|
| CT-01 | **Not every step becomes a child task** (`CT-03` there) — only work with an independent lifecycle, owner, duration, cancellability or artifact. |
| CT-02 | **Parent cancellation propagates only to exclusively-created children** (`CT-04` there). |
| CT-03 | **The parent never receives the child's internal state** (`CT-05` there). |
| CT-04 | **Multi-agent work uses parallel steps or child tasks — never a second runtime** (`CT-06` there). |

---

## 11. Compensation and checkpoints

| # | Rule |
|---|---|
| CC-01 | **Two checkpoint kinds**: an execution checkpoint owned by the runtime, and a domain checkpoint owned by the product (`§5.1` there). |
| CC-02 | **ArcChat never creates a system-wide snapshot** (`CK-01` there). It requests a checkpoint and receives a reference. |
| CC-03 | **A domain checkpoint precedes any high-risk batch modification** (`CK-02` there). |
| CC-04 | **Cross-application unwinding is a saga executed in reverse through each owner** (`CP-02` there), never a simulated distributed transaction. |
| CC-05 | **Compensation is traced and can fail** (`CP-03`, `CP-04` there). |
| CC-06 | **Failure does not automatically trigger compensation** (`CP-05` there). |

---

## 12. Trace and explainability

```
Operational Trace          product-level, user-visible: plans, actions, capability input
                           summaries, outputs, approvals, results, costs
Retrieval Trace            what was searched, in what scope, what was admitted or excluded and why
Audit                      security decisions and high-value effects
Diagnostic Log             operations only
```

| # | Rule |
|---|---|
| TR-01 | **All four are separate systems** (`I-107`, `I-167`, `I-272`–`I-276`). |
| TR-02 | **Chain-of-thought never enters any of them** (`PR-10` in the AI requirements). |
| TR-03 | **An external agent's internal reasoning never enters the ArcChat model** (`EA-07` in the extension requirements). |
| TR-04 | **An AI context inspector renders what the model was actually given** (`RT-03` in the knowledge requirements). |

---

## 13. Automation engine

```
Automation Definition (versioned)
  → Scheduler (time zone + DST policy) or Event Subscriber (durable events only)
      → Trigger Occurrence (stable identity; deduplicated)
          → Task (created from the Task Template, with the version bound)
              → Run
```

| # | Rule |
|---|---|
| AU-01 | **An automation is a rule that creates tasks; it never executes work itself** (`§10` of the AI requirements). |
| AU-02 | **A trigger occurrence has stable identity**, so a scheduler restart does not double-fire (`TG-03` there). |
| AU-03 | **Event triggers deduplicate by event id** (`TG-04` there) and subscribe only to durable events (`EV-07` in the contracts architecture). |
| AU-04 | **Loop protection is structural**: causation chains, causation depth limits, self-recursion suppression, cross-automation cycle detection where feasible (`LP-01`–`LP-03` there). |
| AU-05 | **Storm caps are enforced**: per-automation rate limit, per-workspace concurrency, global agent concurrency, AI budget cap (`LP-04` there). |
| AU-06 | **Catch-up is bounded** (`MR-02` there). |
| AU-07 | **Every triggered task re-authorises** (`AP-10` there). |
| AU-08 | **Local automation runs entirely on the desktop with no cloud dependency** (`LA-01` there). |

---

## 14. MCP integration

| # | Rule |
|---|---|
| MC-01 | **MCP is an edge adapter behind the capability registry** (`MC-01` in the extension requirements), never the internal protocol. |
| MC-02 | **The protocol core is stateless** (**V-02**): no initialize exchange, no session header, per-request capability negotiation. **ArcForges must not build session identity on MCP transport state.** |
| MC-03 | **Server-to-client requests use the protocol's multi-round-trip mechanism**, which is transport, not an ArcForges execution concept. |
| MC-04 | **MCP's own task and skill vocabulary never conflates with ArcForges'** (glossary §9). |
| MC-05 | **The exact SDK version is pinned at first consumption, and the vocabulary mapping is recorded.** *Owner: Architecture Owner. Trigger: start of the MCP/extension work package.* |
| MC-06 | **MCP content is untrusted data** (`§8` of the security architecture). |
| MC-07 | **A down MCP server degrades that integration only** (`IN-05` in the ArcChat requirements). |

---

## 15. Failure handling

| Failure class | Runtime behaviour |
|---|---|
| `Transient` | Bounded automatic retry with backoff |
| `Conflict` | Refresh, rebase, regenerate the action, re-approve if the approval was revision-bound |
| `PermissionDenied` / `ApprovalDenied` | Stop or ask; never retry to probe |
| `BudgetExceeded` | Pause and request an extension |
| `EntitlementBlocked` | Report the entitlement reason, distinct from a policy or security reason |
| `CapabilityUnsupported` | Launch on demand and retry, or wait, or take an alternative path |
| `VersionIncompatible` | Wait or need attention, naming the required version |
| `ExternalEffectUnknown` | **Reconcile before any retry**; unresolved → Needs Attention |
| `Timeout` | Attempt failure handled by the retry policy |
| `PermanentDomainFailure` | Fail the step; the task policy decides keep / compensate / ask |

**Retry safety is declared by the capability owner, never guessed** (`FL-08` in the AI requirements).

---

## 16. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 19` | The complete execution model, states, ownership, checkpoints, compensation, approval, steering, budget, trace, automation and failure classification |
| `I4 §Stage 8` | Provider routing, tariff versioning, metering, the three ledgers, cost dimensions and transparency |
| `I4 §Stage 6`, `§Stage 17` | Agent placement, capability registry, mode contracts, memory layering |
| `I2 §I.3` | The ArcChat AOT/JIT resolution: static registration, no runtime scanning, out-of-process third-party extensions |
| `I3 §8`, `§13` | Capability system, agent placement, `TaskHandle`, long-task model |
| **D-008** | Agent framework enabled only on AOT-validated surfaces; desktop stays a Native AOT deliverable |
| **D-010** | Durable `ToolRequest` / `ToolResult` remote execution |
| **D-020** | Reserve-then-settle, fixed precision, per-run tariff snapshot, hard stop, three ledgers |
| **V-02** | MCP stability, statelessness and vocabulary disambiguation |
