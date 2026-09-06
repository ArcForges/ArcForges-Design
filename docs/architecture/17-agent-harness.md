# Agent Harness

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **P2-006** (Cloud-only single Harness), **D-010** (topology), **D-020** as amended (metering), **V-01** (transparency), **V-02** (MCP vocabulary)
> Companions: [`09-ai-and-agent-runtime-architecture.md`](09-ai-and-agent-runtime-architecture.md) (the runtime this executes inside), [`contracts/02-local-rpc-operations.md`](contracts/02-local-rpc-operations.md), [`08-security-architecture.md`](08-security-architecture.md)

The runtime architecture describes the task engine, tool locality, metering and tracing. **It does not describe the loop.** This document specifies the concrete mechanism by which a model is given context, proposes actions, has them executed against real ArcForges operations, and produces durable results.

**What this is.** The single ArcForges-owned Harness, running in `ArcForges.Cloud.Host`: the turn loop, the tool protocol, context assembly and compaction, capability selection, approval interleaving, streaming, cancellation and recovery.

**What this is not.** A general-purpose coding agent, a client-side loop, or a delegation platform. ArcForges uses **models** from providers with operator-funded credentials. There are no agent teams, no sub-agents, no external-agent delegation and no end-user provider keys (`§9`).

---

## 1. Layer separation

**The Harness is Cloud-only and single** (**P2-006**). Conflating these three is the most common way a design like this becomes unimplementable.

| Layer | What it is | Who owns it | Replaceable? |
|---|---|---|---|
| **Provider transport** | HTTP to a model provider using **operator-funded credentials**; request and response shapes; streaming framing | Provider adapter, in Cloud (`§6` of the runtime architecture) | Yes — per provider |
| **Reusable mechanism** | Token counting, message serialisation, streaming parsing, retry primitives | A library **or** first-party code, chosen on merit | Yes |
| **The ArcForges Harness** | The turn loop, tool protocol, context assembly, compaction, selection, approval, durability, recovery, admission and metering | **ArcForges Cloud, always** | **No** |

| # | Rule |
|---|---|
| LS-01 | **Using a provider's model is not depending on that vendor's agent product.** The Harness speaks a provider's completion or messages API; it does not embed a coding agent. |
| LS-02 | **There is exactly one Harness, and it runs in `ArcForges.Cloud.Host`** (`RT-03` of the cloud architecture). No desktop, mobile or browser client runs a model loop (`CM-02` of the runtime architecture, `I-491`). |
| LS-03 | **A reusable library may be adopted for a mechanism layer** where it is licence-compatible (**D-004**) and passes the dependency policy. It may **never** own the Harness layer. The Cloud AOT constraint does not apply here (**D-008**, **V-03**). |
| LS-04 | **No end-user provider credential exists** in any layer (`BY-01`–`BY-04` of the commerce requirements; `I-015` retired). Provider credentials are deployment secrets injected per `DC-15`. |
| LS-05 | **Agent teams, sub-agents and external-agent delegation are excluded** (`EA-01`–`EA-08` of the extension requirements). See `§9`. |

---

## 2. The turn

A **turn** is one user-visible unit of agent work: the user asks, the agent works, the user gets a result. A turn contains one or more **model calls** and zero or more **capability invocations**.

```
StartAgentTurnAsync
  ↓
create Cloud Task (owner + tool locality recorded) ── returns TaskRef immediately
  ↓
[TURN LOOP]  ── durable; every iteration is persisted before the next begins
  │
  ├─ 1. assemble context      → ContextPack
  ├─ 2. reserve budget        → reservation, or hard stop
  ├─ 3. call model            → stream deltas; accumulate
  ├─ 4. classify the response → text | tool calls | both | refusal | truncation
  ├─ 5. if tool calls:
  │        plan the batch (§2.1) → one or more parallel groups, ordered
  │        for each group, for each call in it:
  │          a. resolve to a capability      (or reject as unknown)
  │          b. validate arguments against the descriptor's schema
  │          c. evaluate availability
  │          d. security pipeline → may require approval
  │          e. if approval required: PERSIST and SUSPEND (§5)
  │          f. invoke through ICapabilityProvider.InvokeAsync
  │          g. persist the result as a message part
  ├─ 6. settle budget         → actual usage debited, unused released
  ├─ 7. decide continuation   (§3.2)
  └─ loop, or finish
  ↓
persist the outcome; emit task.stateChanged
```

| # | Rule |
|---|---|
| TN-01 | **`StartAgentTurnAsync` returns immediately with a `TaskRef`.** Generation is durable execution, never a long synchronous call (`CH-01` of the local RPC contract). |
| TN-02 | **Every loop iteration is persisted before the next begins.** A crash resumes at the last completed step, not at the start of the turn (`§6`). |
| TN-03 | **The loop is the harness's, not the model's.** The model proposes; the harness decides whether, when and in what order to act. |
| TN-04 | **A model response is never applied directly to product state.** Every effect goes through a capability invocation with its full security pipeline. |
| TN-05 | **One iteration's tool calls become Steps of the run's plan**, and retrying one produces a new Attempt inside that Step, never a new Step (`EX-09` of the AI requirements). The loop is not a second execution model beside the task engine; it is how the engine's plan is populated for an agent-driven run. |

### 2.1 Parallel tool calls and resource conflict

Steps form a DAG, so independent work runs in parallel (`EX-08` of the AI requirements). A model that proposes four calls in one response is proposing a batch, and the harness decides its shape.

```
proposed calls
  ↓ declared conflict set per call   (from CapabilityDescriptor: reads / writes / exclusive)
  ↓ build the dependency graph        (a write conflicts with any read or write on the same target)
  ↓ partition into ordered parallel groups
  ↓ apply the concurrency ceiling     (policy-bounded, per turn and per capability)
```

| # | Rule |
|---|---|
| PA-01 | **Parallelism respects resource conflict** (`CC-02` of the AI requirements). Reading two ArcScope sessions may run in parallel; two calls editing the same ArcNotes document must not. |
| PA-02 | **The conflict set is declared by the capability owner**, not inferred from arguments. An undeclared capability is treated as exclusive, which is the safe default. |
| PA-03 | **A capability declared non-parallelisable runs alone**, whatever the model proposed. |
| PA-04 | **Group order preserves the model's relative order** where the graph permits, so a model that intended a sequence gets one. |
| PA-05 | **An approval suspension suspends the whole batch**, not one call. Resuming re-evaluates the remaining groups against revalidated context (`SI-05`), because an approval may have taken hours. |
| PA-06 | **A failure inside a group does not silently abandon its siblings.** Completed siblings' results are persisted and returned to the model with the failure, so the model sees the true state. |
| PA-07 | **Task-step parallelism and automation concurrency are different layers** and are never conflated (`CC-01` of the AI requirements, `I-104`). |

---

## 3. The model call

### 3.1 Request construction

| Element | Source | Rule |
|---|---|---|
| System instruction | Agent profile + active skills | Skills are declarative guidance and **confer no capability** (`WP-15.04`) |
| Conversation history | The branch, after compaction (`§4.6`) | Immutable messages; editing creates a new branch (`CV-04` of the ArcChat requirements) |
| Context pack | `§4` | Bounded, budgeted, permission-filtered |
| Tool declarations | The capability registry, filtered by `§4.4` | Schema-described, from `CapabilityDescriptor` |
| Model parameters | Agent profile, then policy bounds | A profile may narrow policy bounds, never widen them |

| # | Rule |
|---|---|
| MR-01 | **Tool declarations are generated from `CapabilityDescriptor`**, never hand-maintained. A capability the caller may not invoke is **not declared**, so the model cannot propose it. |
| MR-02 | **The declared schema is the closed structured value model** (`§4.2` of the extension architecture) — AOT-safe and validatable, and `L2-04` there validates it in both directions. |
| MR-03 | **Provider-specific shaping happens in the adapter.** The harness constructs one neutral request; the adapter maps it. |
| MR-04 | **A tariff snapshot is locked before the call** (`CS-08` of the commerce architecture, `MB-05` of the runtime architecture), so the charge is explainable afterwards. |

### 3.2 Response classification and continuation

| Response | Continuation |
|---|---|
| Text only | **Finish.** The turn's answer |
| Tool calls only | Execute, then **continue** with results appended |
| Text and tool calls | Persist the text as a part, execute, **continue** |
| Refusal | **Finish** with the refusal recorded as the outcome |
| Truncated by length | Persist what arrived as `interrupted`; **continue** only if the profile permits, else finish with a stated reason |
| Malformed tool call | Return a typed protocol error to the model as the tool result; **continue**, bounded by `§3.3` |
| Transport failure | Retry per `§8`; the turn state is unchanged |

| # | Rule |
|---|---|
| RC-01 | **An interrupted stream is stored as `interrupted`, never as `complete`** (`WP-15.00`). This is why `message.state` exists. |
| RC-02 | **A malformed tool call is answered, not crashed.** The model receives a structured error and may correct itself. |
| RC-03 | **Continuation is the harness's decision**, governed by `§3.3` — not the model's assertion that it wants to continue. |

### 3.3 Loop bounds

Every bound is policy-configurable within compiled hard limits (`§4.2` of the policy requirements), and exceeding one ends the turn with a stated reason rather than silently.

| Bound | Purpose |
|---|---|
| Maximum model calls per turn | Prevents an unbounded loop |
| Maximum capability invocations per turn | Prevents fan-out |
| Maximum wall-clock per turn | Prevents an indefinite hang |
| Maximum consecutive no-progress iterations | Detects a model repeating itself (`§3.4`) |
| Maximum budget per turn | Independent of the balance — a turn cannot consume everything |
| Maximum context bytes and items | `§4.5` |

### 3.4 Progress detection

| # | Rule |
|---|---|
| PD-01 | **An iteration makes progress if it produced durable text, a successful invocation, or a distinct new tool call.** |
| PD-02 | **Repeating an identical tool call with identical arguments and an unchanged result is not progress**, and the counter advances. |
| PD-03 | **Exceeding the no-progress bound ends the turn with `agent.no_progress`**, showing what was attempted. This is loop protection at the semantic level, above the engine's structural loop detection (`WP-16.07`). |

---

## 4. Context assembly

The runtime architecture gives the pipeline (`§5` there). This is the mechanism.

### 4.1 Inputs

| Source | Included when |
|---|---|
| Explicit attachments on the message | Always |
| Pinned context on the conversation | Always |
| Project context | The conversation belongs to a project |
| Temporary context | Set for this turn only |
| Retrieved evidence | The profile enables retrieval **and** a scope resolves |

**There is no ambient default scope** (`CA-01` of the runtime architecture). Absence of all five means an empty context pack, and the model is told so rather than silently receiving nothing.

### 4.2 Assembly order

```
collect references          (identity only — no content yet)
  ↓ knowledge policy filter (searchable · AI retrieval · managed AI processing)
  ↓ permission filter       (per source, at assembly, not after ranking)
  ↓ retrieval               (hybrid, budgeted, per-source capped)
  ↓ revalidate              (against the authoritative owner, at current revision)
  ↓ materialise content     (last — §4.3 of the knowledge requirements)
  ↓ pack                    (ordered, budgeted, each item bound to source+revision+anchor)
```

| # | Rule |
|---|---|
| PK-01 | **References first, content last.** A reference that fails revalidation never causes its content to be fetched. |
| PK-02 | **Every packed item carries source, revision and anchor**, which is what makes a citation resolvable afterwards (`WP-19.02`). |
| PK-03 | **Permission is applied per source during assembly.** A refused source contributes nothing, including to counts (`WP-40.03`). |
| PK-04 | **Only acknowledged Cloud revisions are packable** (`I-498`). Content that was never synchronised — an unenrolled notebook, a local-only ArcScope capture, an ArcSlate media file — is **not context**, and its absence is stated in the pack rather than silently reducing the evidence. Enabling AI never causes an upload (`OW-08` of the AI requirements, `I-182`). |

### 4.3 Staleness and invalidation

The hardest correctness problem in the loop: context assembled at step 1 may be stale by iteration four.

| # | Rule |
|---|---|
| SI-01 | **Every packed item records the revision it was read at.** |
| SI-02 | **Before a capability invocation that reads or writes an item in the pack, its revision is re-checked.** A changed revision invalidates that item. |
| SI-03 | **An invalidated item is refreshed and the model is told**, as a structured tool result: *this content changed since you were shown it*. It is never silently substituted, because the model's reasoning may depend on what it saw. |
| SI-04 | **A write against a stale revision fails with `conflict.revision_mismatch`** (`NO-02`) and is surfaced to the model as a correctable error. |
| SI-05 | **Approval-suspended turns revalidate on resume** (`§5`), because a suspension may last hours. |
| SI-06 | **An automation's scope freezes at run start** (`CA-04` of the runtime architecture) — an automation must not silently widen because content changed. |

### 4.4 Tool declaration filtering

| Filter | Effect |
|---|---|
| Capability registry | Only registered, healthy capabilities |
| Actor kind | Only capabilities declaring `agent` in `actorKinds` (`AZ-02`) |
| Entitlement | Only capabilities the workspace is entitled to |
| Permission grant | Only capabilities the actor chain holds |
| Placement | For a cloud turn, only capabilities reachable from cloud or through the bridge |
| Profile allowance | The profile may narrow further, never widen |

**A capability the caller cannot invoke is never declared**, so a refusal for lack of permission should be rare rather than routine — and when one occurs it is a real condition, not noise.

### 4.5 Budget and truncation

| # | Rule |
|---|---|
| CB-01 | **The pack has a token, item and byte budget**, and assembly stops at the first exceeded. |
| CB-02 | **Truncation is disclosed in the pack**, naming what was omitted and why. A silently truncated context produces confidently wrong output. |
| CB-03 | **Priority order is**: explicit attachments, pinned, then retrieved by score. Explicit user intent is never dropped in favour of retrieval. |

### 4.6 History and compaction

The requirements state the principle — *compaction is context engineering, not memory* (`HM-03` of the ArcChat requirements, `CA-06` of the runtime architecture, `I-158`) — without a mechanism. This is the mechanism.

**The shape of the problem.** Conversation history is append-and-branch, never rewrite (`CV-04` there). A long conversation therefore has an immutable message sequence that eventually exceeds the model's context. Compaction must reduce what is *sent* without touching what is *stored*.

```
branch message sequence (immutable, authoritative)
  ↓ window selection      keep the head (opening intent) + a recent tail verbatim
  ↓ compaction candidates the middle span, oldest first
  ↓ produce a CompactionRecord   ── a derived artifact, stored, never a message
  ↓ assemble the request:  head · CompactionRecord(s) · verbatim tail · context pack
```

| # | Rule |
|---|---|
| HC-01 | **Compaction never mutates or deletes a stored message.** It produces a `CompactionRecord` — a derived artifact keyed to `(branchId, fromMessageId, toMessageId, compactionModelId, promptVersion)`. The branch is unchanged and re-readable in full. |
| HC-02 | **A `CompactionRecord` is a derived store** and obeys `DS-01`…`DS-07`: rebuildable from the messages, never authoritative, and invalidated when its key inputs change. Losing every record costs compute, never content. |
| HC-03 | **The most recent turns are always verbatim.** A configurable tail — never zero — is never compacted, because the immediate work is what the model most needs exactly. |
| HC-04 | **The opening intent is retained.** The head of a branch carries what the user actually asked for, and losing it is how a long agent run drifts from its objective. |
| HC-05 | **Compaction is disclosed.** The user can see that a span was compacted, see the record, and expand the underlying messages. A silently shortened history is indistinguishable from a model that forgot. |
| HC-06 | **A tool call and its result are compacted as a unit or not at all.** Keeping a call without its result, or a result without its call, produces a transcript the model reads as a failure. |
| HC-07 | **An approval, a refusal and a user correction are never compacted away.** They are decision points, and a model that loses them re-proposes what the user already refused. |
| HC-08 | **Compaction is itself a model call** with its own budget reservation, cost dimensions and tariff snapshot (`§3.1`). It is metered like any other, and it is charged as platform work rather than to the user's turn where policy says so (`CU-03` of the AI requirements). |
| HC-09 | **A compaction failure degrades to hard truncation with disclosure**, never to silent loss. The turn continues, and the truncation is stated in the request record. |
| HC-10 | **A `CompactionRecord` is scoped to its branch.** Branching from a compacted point inherits the records covering the shared prefix; it never inherits a record covering messages the new branch does not contain. |
| HC-11 | **A `CompactionRecord` is not personal memory** (`HM-03` there). It is never promoted into durable preference recall, never carried into another conversation, and never survives the branch it belongs to. |
| HC-12 | **Temporary Chat compacts in memory only.** No `CompactionRecord` is persisted, consistent with the mode's promise (`HM-06` there) — and the mode still says honestly that the model received the data. |

---

## 5. Approval interleaving

The loop must pause for a human without losing its place, possibly for hours, across restarts.

```
step 5d → security pipeline returns approvalRequired
  ↓
persist: turn state, iteration index, pending invocation, frozen context, model transcript
  ↓
create approval record (durable, expiring)  ── task.state = waitingApproval
  ↓
emit approval.raised (a hint; the record is authoritative)
  ↓
… the process may exit here …
  ↓
approval.decide
  ├─ approved → resume: revalidate (§4.3), invoke, continue the loop
  ├─ rejected → append a structured tool result "refused by user", continue
  └─ expired  → append "approval expired", continue or finish per profile
```

| # | Rule |
|---|---|
| AP-01 | **The suspended turn is fully durable**, because the approval is a durable object rather than a notification (`AP-01` of the security architecture). It survives a restart of either side (`WP-14.04`). |
| AP-02 | **A rejection is a tool result, not a turn failure.** The model is told and may propose an alternative — which is what makes approval feel like collaboration rather than a dead end. |
| AP-03 | **Resume revalidates context** (`SI-05`). |
| AP-04 | **An operation requiring local presence cannot be approved remotely** (`AZ-01` of the operation catalogue), and the harness does not offer remote approval for it. |
| AP-05 | **Approval is per invocation unless the descriptor declares a broader posture**, and a broader posture is itself an authorization decision (`§5` of the security requirements). |

---

## 6. Durability, cancellation and recovery

### 6.1 What is persisted per iteration

| Record | Store |
|---|---|
| Iteration index, state, timestamps | `task.run` / `attempt` |
| The model request's identity — not its content | `provider_interaction` |
| The response's durable parts | `message_part` |
| Each invocation with its `InvocationId` and `CommandId` | `attempt` |
| Budget reservation and settlement | `entitlement.capacity_reservation`, `commerce.credit_transaction`, `commerce.customer_settlement` |
| Context pack manifest — sources and revisions, not content | Execution trace |

**Prompt and response content is never written to telemetry** (`RD-01` of the observability architecture). Durable message parts are user content in the product store; the interaction record carries counts and identifiers only.

### 6.2 Cancellation

| Point | Behaviour |
|---|---|
| Before the model call | Immediate; reservation released |
| During streaming | Stream aborted; partial text stored as `interrupted`; reservation settled at actual usage |
| During an invocation | Cancellation propagates; the capability's own semantics decide; effect certainty recorded |
| While awaiting approval | Approval withdrawn; turn ends `cancelled` |

| # | Rule |
|---|---|
| CN-01 | **Cancellation is cooperative and always leaves a determinate state.** No path ends with a turn neither running nor finished. |
| CN-02 | **A cancelled turn settles its budget at actual usage** — the user is not charged for what was not consumed, and is charged for what was. |
| CN-03 | **Cancellation during a non-idempotent invocation records `unknownEffect`** rather than assuming it did not happen. |

### 6.3 Crash recovery

| State at crash | On restart |
|---|---|
| Between iterations | Resume at the next iteration |
| Mid-model-call | The call is lost; the reservation is swept; retry the iteration |
| Mid-invocation | The local command log decides: recorded ⇒ completed, absent ⇒ safe to re-attempt |
| Mid-settlement | Settlement is idempotent per attempt; re-run |
| Awaiting approval | Nothing to do — durable by construction |

| # | Rule |
|---|---|
| CR-01 | **The command log is what makes mid-invocation recovery decidable** (`BI-02`, `BI-03` of the bridge contract). Without it every crash would produce an unknown effect. |
| CR-02 | **An orphaned reservation is released by the sweeper** (`CS-04` of the commerce architecture); a crash never permanently consumes budget. |
| CR-03 | **Recovery is verifiable**: after restart, every task is in a valid state with a reason facet, and none is stuck in a transient state (`WP-16.00`). |

---

## 7. Streaming

| # | Rule |
|---|---|
| ST-01 | **Streaming is presentation; the durable message is written once, complete** (`WP-15.00`). |
| ST-02 | **Deltas reach the UI through `task.outputAppended`** and are best-effort. Losing every delta must not affect the stored result. |
| ST-03 | **A tool call is not emitted as a delta until it is complete and parsed.** Partial tool-call syntax never reaches the UI. |
| ST-04 | **A remote surface receives the same deltas through realtime**, and re-reads authoritatively on completion (`RE-01` of the realtime contract). |

---

## 8. Provider failure handling

| Failure | Classification | Harness action |
|---|---|---|
| Rate limited | `capacity.rate_limited`, transient | Honour `retryAfter`; retry within budget |
| Timeout before any token | Transient, **did not happen** | Retry |
| Timeout mid-stream | Transient, **unknown** | Store partial as `interrupted`; ask the user or the profile before retrying |
| Content refused by provider | Permanent, refused | Record as the turn outcome |
| Context too long | Permanent, correctable | Compact harder (`§4.3` of the runtime architecture) and retry once |
| Model withdrawn | Permanent | Fail with a stated reason; **no silent substitution** (`WP-43.05`) |
| Provider outage | Transient | Fall back where policy allows, else fail; **release the reservation** |
| All routes unavailable | Permanent for now | Fail with a stated reason; page-worthy (`AL-02` of the observability architecture) |

| # | Rule |
|---|---|
| PF-01 | **A provider outage never silently consumes credit** (`WP-43.05`). |
| PF-02 | **A fallback is a policy decision, not an adapter default**, and the substitution is recorded in the interaction record and shown to the user. |
| PF-03 | **A retry produces a new Attempt inside the same Step, never a new Step** (`EX-09` there), and the `CommandId` is unchanged because the business action is unchanged (`ID-01` there, `I-085`). |
| PF-04 | **A platform-caused retry is not charged to the user** (`CU-03` there). A logical AI request whose first provider attempt failed and whose second succeeded is charged for the useful work only. |
| PF-05 | **Retry safety is declared by the capability owner, never guessed** (`FL-08` there), which is why the harness never infers idempotency from an operation's name. |

---

## 9. What the Harness is not

| # | Rule |
|---|---|
| XA-01 | **There is no external-agent integration.** External-agent providers, ACP adapters, session mapping, delegation leases and result adapters are all retired (`EA-01`–`EA-06` of the extension requirements, `I-313`, `I-314` retired). |
| XA-02 | **There are no agent teams and no sub-agents** (`EA-08` there). A Task may create **child tasks** for long or independent work, and a turn may run **parallel tool calls** (`§2.1`) — both are execution mechanisms inside the one Harness, not additional agents. |
| XA-03 | **A package, connector or MCP tool cannot start an autonomous delegated agent** (`EA-08` there). An integration contributes tools; it never contributes a planner. |
| XA-04 | **MCP remains a tool-integration edge adapter**, never the internal protocol (**V-02**, `MC-01` of the extension requirements). An MCP tool maps to a declared capability carrying risk, permission and provenance — it is never injected as a raw tool (`MC-02` there). |
| XA-05 | **MCP tool descriptions, prompts and resource contents are untrusted data** (`MC-07` there, `I-262`, `I-263`), and an MCP server changing its tool set re-enters permission review (`MC-10` there). |
| XA-06 | **Hidden model reasoning never enters the product model** (`EA-07` there, `PR-10` of the AI requirements, `I-107`). Reasoning appears as a metered cost category (`MT-03`), never as content or trace. |
| XA-07 | **The Harness is not a native Product Job runner.** A render, capture, index or export is owned by its product (`CM-04` of the runtime architecture, `I-121`, `I-485`); the Harness may observe one through a status tool, never adopt it as a Step.

---

## 10. Tool locality

The Harness always runs in Cloud (`LS-02`). What varies is **where each tool executes** (`§9` of the runtime architecture).

| Tool locality | When | Constraint |
|---|---|---|
| **Cloud tool** | The capability is Cloud-owned | Executes in-process inside the turn |
| **Device tool** | The capability requires a desktop | Each invocation is a durable `ToolRequest` pulled by the device (`§5` of the bridge contract) |

| # | Rule |
|---|---|
| PL-01 | **A Task is Cloud-owned from creation** (`TO-02` of the data-model overview). There is no local or hybrid task placement to decide. |
| PL-02 | **A device tool with no eligible online device enters `WaitingForDevice`** with a stated reason and a bounded wait — it never degrades to a cloud approximation. |
| PL-03 | **Waiting consumes no model capacity.** A turn parked on a device or an approval releases its included-capacity hold at the safe boundary and re-reserves on resume (`AC-05` of the commerce requirements). This is what stops one waiting Task from reserving the whole workspace. |
| PL-04 | **Local-only data never leaves the device to enable a cloud tool** (`OW-08` of the AI requirements). If the data cannot leave, the device tool runs or the step fails with a reason. |
| PL-05 | **Cached, unacknowledged client state is never treated as Cloud context.** Only acknowledged Cloud revisions enter the context pack (`I-498`); a pending local edit is visible to the user, not to the model, until it is acknowledged.

---

## 11. Transparency and cost

| # | Rule |
|---|---|
| TC-01 | **AI-generated content carries the marking its regime requires**, per artifact type (**V-01**; `TA-02`, `TA-03` of the security architecture). Marking is applied at the point of generation, which makes it a property of this harness and the artifact format — not of the user interface. |
| TC-02 | **A turn's cost is explainable**: which model, which tariff version, which cost dimensions — including reasoning tokens, cached input and cache writes — and which counts (`§11.3` of the AI requirements, `WP-43.04`). |
| TC-03 | **The user can see what context was sent** — sources and revisions — without the harness storing the prompt in telemetry. |
| TC-04 | **A tool call and its result are visible in the conversation** as durable parts, so the user can audit what the agent did. |
| TC-05 | **Trace is not chain-of-thought** (`PR-10` of the AI requirements, `I-107`). Hidden model reasoning is never surfaced as trace, and reasoning tokens appear as a cost dimension rather than as content. |

---

## 12. Verification

| # | Obligation | Where |
|---|---|---|
| HV-01 | A multi-step turn completes end to end in the single Cloud host, against a real provider | `WP-43.07`, `WP-17.01` |
| HV-02 | A model-proposed action reaches a real product operation through the full security pipeline | `WP-20.02` |
| HV-03 | A crash at each loop point resumes correctly, with no duplicate effect and no duplicate charge | `WP-17.08`, `WP-16.00`, `WP-26.03` |
| HV-04 | An approval-suspended turn survives restart of either side and resumes with revalidated context | `WP-14.04`, `WP-16.05` |
| HV-05 | An interrupted stream is never stored as complete, and cumulative stream usage is not summed as independent consumption | `WP-15.00`, `WP-43.02` |
| HV-06 | Stale context is detected before a write, and the model is told rather than silently corrected | `WP-20.02` |
| HV-07 | Every loop bound ends the turn with a stated reason; no unbounded loop is reachable | `WP-17.08`, `WP-16.07` |
| HV-08 | A cancelled turn settles verified consumption and releases the remainder | `WP-16.05`, `WP-43.02` |
| HV-09 | **No client runs a model loop.** A structural test asserts no desktop, mobile or browser assembly references a provider adapter or holds a provider credential | `WP-05`, `WP-17.01` |
| HV-10 | A capability not declarable to the model is never proposed, and never invocable if proposed | `WP-17.00` |
| HV-11 | **No end-user BYOK path exists.** No operation, schema field, setting or UI accepts a customer provider key | `WP-05`, `WP-43.03` |
| HV-12 | A provider outage releases the customer reservation or appends a compensating adjustment, and retains the supplier cost | `WP-43.05` |
| HV-13 | Two tool calls writing the same target never execute in parallel; two reads of independent targets do | `WP-17.08`, `WP-20.03` |
| HV-14 | An approval mid-batch suspends the whole batch, and resume re-evaluates the remainder against revalidated context | `WP-17.08`, `WP-16.05` |
| HV-15 | A failure inside a parallel group returns the siblings' real results alongside the failure | `WP-17.08`, `WP-16.02` |
| HV-16 | A platform-caused provider retry is charged once to the customer and remains fully visible in supplier cost | `WP-43.02`, `WP-43.04` |
| HV-17 | A turn waiting for a device or an approval holds no included capacity, and cannot reserve the workspace indefinitely | `WP-16.05`, `WP-43.02` |
| HV-18 | **No agent team, sub-agent or external-agent delegation is reachable.** A structural test asserts no delegation contribution kind and no second planner exists | `WP-05`, `WP-41.07` |
| HV-19 | MCP tool descriptions and retrieved content are treated as data; an instruction inside them changes no behaviour | `WP-11.06`, `WP-41.07` |
| HV-20 | Hidden model reasoning never appears in trace, and reasoning tokens appear only as a metered cost category | `WP-16.06`, `WP-43.02` |
| HV-21 | The stored branch is byte-identical before and after compaction, and losing every `CompactionRecord` costs no content | `WP-17.09` |
| HV-22 | A compacted span never loses an approval, a refusal or a user correction, and never separates a tool call from its result | `WP-17.09` |
| HV-23 | A `CompactionRecord` never becomes personal memory and never crosses a branch or a conversation | `WP-17.09`, `WP-15.01` |
| HV-24 | Official inference is refused without an active paid service term, whatever the credit balance | `WP-42.11`, `WP-43.02` |
| HV-25 | Only acknowledged Cloud revisions enter the context pack; a pending client edit never reaches the model as context | `WP-25.01`, `WP-20.02` |
