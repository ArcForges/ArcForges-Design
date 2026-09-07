# Agent Harness

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (Cloud-only single Harness), **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** (topology), **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** as amended (metering), **[V-01](../assurance/phase-1-official-verification.md#rule-v-01)** (transparency), **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** (MCP vocabulary)
> Companions: [`09-ai-and-agent-runtime-architecture.md`](09-ai-and-agent-runtime-architecture.md) (the runtime this executes inside), [`contracts/02-local-rpc-operations.md`](contracts/02-local-rpc-operations.md), [`08-security-architecture.md`](08-security-architecture.md)

The runtime architecture describes the task engine, tool locality, metering and tracing. **It does not describe the loop.** This document specifies the concrete mechanism by which a model is given context, proposes actions, has them executed against real ArcForges operations, and produces durable results.

**What this is.** The single ArcForges-owned Harness, running in `ArcForges.Cloud.Host`: the turn loop, the tool protocol, context assembly and compaction, capability selection, approval interleaving, streaming, cancellation and recovery.

**What this is not.** A general-purpose coding agent, a client-side loop, or a delegation platform. ArcForges uses **models** from providers with operator-funded credentials. There are no agent teams, no sub-agents, no external-agent delegation and no end-user provider keys (`§9`).

---

## 1. Layer separation

**The Harness is Cloud-only and single** (**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**). Conflating these three is the most common way a design like this becomes unimplementable.

| Layer | What it is | Who owns it | Replaceable? |
|---|---|---|---|
| **Provider transport** | HTTP to a model provider using **operator-funded credentials**; request and response shapes; streaming framing | Provider adapter, in Cloud (`§6` of the runtime architecture) | Yes — per provider |
| **Reusable mechanism** | Token counting, message serialisation, streaming parsing, retry primitives | A library **or** first-party code, chosen on merit | Yes |
| **The ArcForges Harness** | The turn loop, tool protocol, context assembly, compaction, selection, approval, durability, recovery, admission and metering | **ArcForges Cloud, always** | **No** |

| # | Rule |
|---|---|
| LS-01 | **Using a provider's model is not depending on that vendor's agent product.** The Harness speaks a provider's completion or messages API; it does not embed a coding agent. |
| <a id="rule-ls-02"></a>LS-02 | **There is exactly one Harness, and it runs in `ArcForges.Cloud.Host`** ([RT-03](05-cloud-architecture.md#rule-rt-03) of the cloud architecture). No desktop, mobile or browser client runs a model loop ([CM-02](09-ai-and-agent-runtime-architecture.md#rule-cm-02) of the runtime architecture, [I-491](../requirements/01-normative-glossary-and-invariants.md#rule-i-491)). |
| LS-03 | **A reusable library may be adopted for a mechanism layer** where it is licence-compatible (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**) and passes the dependency policy. It may **never** own the Harness layer. The Cloud AOT constraint does not apply here (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**). |
| LS-04 | **No end-user provider credential exists** in any layer ([BY-01](../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04) of the commerce requirements; [I-015](../requirements/01-normative-glossary-and-invariants.md#rule-i-015) retired). Provider credentials are deployment secrets injected per [DC-15](../requirements/11-policy-and-configuration.md#rule-dc-15). |
| LS-05 | **Agent teams, sub-agents and external-agent delegation are excluded** ([EA-01](../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-08](../requirements/08-extensions-and-developer-platform.md#rule-ea-08) of the extension requirements). See `§9`. |

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
  ├─ 5. commit immutable iteration output + usage/outcome receipt; settle this invocation
  ├─ 6. if tool calls:
  │        plan the batch (§2.1) → one or more parallel groups, ordered
  │        for each group, for each call in it:
  │          a. resolve to a capability      (or reject as unknown)
  │          b. validate arguments against the descriptor's schema
  │          c. evaluate availability
  │          d. security pipeline → may require approval
  │          e. if approval required: PERSIST and SUSPEND (§5)
  │          f. invoke through ICapabilityProvider.InvokeAsync
  │          g. persist the result as a message part
  ├─ 7. decide continuation   (§3.2); next invocation has a fresh bounded reservation
  └─ loop, or finish
  ↓
atomically commit final/interrupted message (or explicit no-answer) + terminal Task + publication; emit hint
```

| # | Rule |
|---|---|
| TN-01 | **`StartAgentTurnAsync` returns immediately with a `TaskRef`.** Generation is durable execution, never a long synchronous call ([CH-01](contracts/02-local-rpc-operations.md#rule-ch-01) of the local RPC contract). |
| TN-02 | **Every loop iteration is persisted before the next begins.** A crash resumes at the last completed step, not at the start of the turn (`§6`). |
| TN-03 | **The loop is the harness's, not the model's.** The model proposes; the harness decides whether, when and in what order to act. |
| TN-04 | **A model response is never applied directly to product state.** Every effect goes through a capability invocation with its full security pipeline. |
| TN-05 | **One iteration's tool calls become Steps of the run's plan**, and retrying one produces a new Attempt inside that Step, never a new Step ([EX-09](../requirements/05-ai-and-agent-execution.md#rule-ex-09) of the AI requirements). The loop is not a second execution model beside the task engine; it is how the engine's plan is populated for an agent-driven run. |
| TN-06 | One `logical_ai_request` is one bounded model invocation; its provider retries share one customer hold and have separate supplier exposure. A Turn can have many logical requests. Commit complete/interrupted iteration output and parsed tool proposals before settling delivered usage; settle or explicitly resolve uncertainty before the next invocation. A durable tool proposal used by the Harness is delivered inference even when the Turn later fails. |
| TN-07 | Terminal Task and final/interrupted Chat message, or an explicit no-answer reason, commit atomically. Previously settled iterations are not charged again at Turn completion. A crash with durable output but no settlement retries only settlement; a crash with settled output resumes the next durable step; an intent without outcome follows unknown-effect reconciliation and never blind redispatch. |

### 2.1 Parallel tool calls and resource conflict

Steps form a DAG, so independent work runs in parallel ([EX-08](../requirements/05-ai-and-agent-execution.md#rule-ex-08) of the AI requirements). A model that proposes four calls in one response is proposing a batch, and the harness decides its shape.

```
proposed calls
  ↓ declared conflict set per call   (from CapabilityDescriptor: reads / writes / exclusive)
  ↓ build the dependency graph        (a write conflicts with any read or write on the same target)
  ↓ partition into ordered parallel groups
  ↓ apply the concurrency ceiling     (policy-bounded, per turn and per capability)
```

| # | Rule |
|---|---|
| PA-01 | **Parallelism respects resource conflict** ([CC-02](../requirements/05-ai-and-agent-execution.md#rule-cc-02) of the AI requirements). Reading two ArcScope sessions may run in parallel; two calls editing the same ArcNotes document must not. |
| PA-02 | **The conflict set is declared by the capability owner**, not inferred from arguments. An undeclared capability is treated as exclusive, which is the safe default. |
| PA-03 | **A capability declared non-parallelisable runs alone**, whatever the model proposed. |
| PA-04 | **Group order preserves the model's relative order** where the graph permits, so a model that intended a sequence gets one. |
| PA-05 | **An approval suspension suspends the whole batch**, not one call. Resuming re-evaluates the remaining groups against revalidated context ([SI-05](#rule-si-05)), because an approval may have taken hours. |
| PA-06 | **A failure inside a group does not silently abandon its siblings.** Completed siblings' results are persisted and returned to the model with the failure, so the model sees the true state. |
| PA-07 | **Task-step parallelism and automation concurrency are different layers** and are never conflated ([CC-01](../requirements/05-ai-and-agent-execution.md#rule-cc-01) of the AI requirements, [I-104](../requirements/01-normative-glossary-and-invariants.md#rule-i-104)). |

---

## 3. The model call

### 3.1 Request construction

| Element | Source | Rule |
|---|---|---|
| System instruction | Agent profile + active skills | Skills are declarative guidance and **confer no capability** ([WP-15.04](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.04)) |
| Conversation history | The branch, after compaction (`§4.6`) | Immutable messages; editing creates a new branch ([CV-04](../requirements/products/arcchat.md#rule-cv-04) of the ArcChat requirements) |
| Context pack | `§4` | Bounded, budgeted, permission-filtered |
| Tool declarations | The capability registry, filtered by `§4.4` | Schema-described, from `CapabilityDescriptor` |
| Model parameters | Agent profile, then policy bounds | A profile may narrow policy bounds, never widen them |

| # | Rule |
|---|---|
| <a id="rule-mr-01"></a>MR-01 | **Tool declarations are generated from `CapabilityDescriptor`**, never hand-maintained. A capability the caller may not invoke is **not declared**, so the model cannot propose it. |
| MR-02 | **The declared schema is the closed structured value model** (`§4.2` of the extension architecture) — AOT-safe and validatable, and [L2-04](15-extension-platform-architecture.md#rule-l2-04) there validates it in both directions. |
| MR-03 | **Provider-specific shaping happens in the adapter.** The harness constructs one neutral request; the adapter maps it. |
| MR-04 | **A tariff snapshot is pinned to the Run before the call** ([MT-06](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-06) of the commerce requirements, [MB-05](09-ai-and-agent-runtime-architecture.md#rule-mb-05) of the runtime architecture), so the charge is explainable afterwards. |

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
| RC-01 | **An interrupted stream is stored as `interrupted`, never as `complete`** ([WP-15.00](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.00)). This is why `message.state` exists. |
| <a id="rule-rc-02"></a>RC-02 | **A malformed tool call is answered, not crashed.** The model receives a structured error and may correct itself. |
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
| PD-03 | **Exceeding the no-progress bound ends the turn with `agent.no_progress`**, showing what was attempted. This is loop protection at the semantic level, above the same Run's bounded execution counters ([WP-52.00](../planning/work-packages/52-cloud-harness.md#rule-wp-52.00)). |

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

**There is no ambient default scope** ([CA-01](09-ai-and-agent-runtime-architecture.md#rule-ca-01) of the runtime architecture). Absence of all five means an empty context pack, and the model is told so rather than silently receiving nothing.

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
| PK-02 | **Every packed item carries source, revision and anchor**, which is what makes a citation resolvable afterwards ([WP-19.02](../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.02)). |
| PK-03 | **Permission is applied per source during assembly.** A refused source contributes nothing, including to counts ([WP-40.03](../planning/work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.03)). |
| <a id="rule-pk-04"></a>PK-04 | **Only acknowledged Cloud revisions are packable** ([I-498](../requirements/01-normative-glossary-and-invariants.md#rule-i-498)). Content that was never synchronised — an unenrolled notebook, a local-only ArcScope capture, an ArcSlate media file — is **not context**, and its absence is stated in the pack rather than silently reducing the evidence. Enabling AI never causes an upload ([OW-08](../requirements/05-ai-and-agent-execution.md#rule-ow-08) of the AI requirements, [I-182](../requirements/01-normative-glossary-and-invariants.md#rule-i-182)). |

### 4.3 Staleness and invalidation

The hardest correctness problem in the loop: context assembled at step 1 may be stale by iteration four.

| # | Rule |
|---|---|
| SI-01 | **Every packed item records the revision it was read at.** |
| SI-02 | **Before a capability invocation that reads or writes an item in the pack, its revision is re-checked.** A changed revision invalidates that item. |
| SI-03 | **An invalidated item is refreshed and the model is told**, as a structured tool result: *this content changed since you were shown it*. It is never silently substituted, because the model's reasoning may depend on what it saw. |
| <a id="rule-si-04"></a>SI-04 | **A write against a stale revision fails with `conflict.revision_mismatch`** ([NO-02](contracts/02-local-rpc-operations.md#rule-no-02)) and is surfaced to the model as a correctable error. |
| <a id="rule-si-05"></a>SI-05 | **Approval-suspended turns revalidate on resume** (`§5`), because a suspension may last hours. |
| SI-06 | **An automation's scope freezes at run start** ([CA-04](09-ai-and-agent-runtime-architecture.md#rule-ca-04) of the runtime architecture) — an automation must not silently widen because content changed. |

### 4.4 Tool declaration filtering

| Filter | Effect |
|---|---|
| Capability registry | Only registered, healthy capabilities |
| Actor kind | Only capabilities declaring `agent` in `actorKinds` ([AZ-02](contracts/00-operation-catalogue.md#rule-az-02)) |
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

The requirements state the principle — *compaction is context engineering, not memory* ([HM-03](../requirements/products/arcchat.md#rule-hm-03) of the ArcChat requirements, [CA-06](09-ai-and-agent-runtime-architecture.md#rule-ca-06) of the runtime architecture, [I-158](../requirements/01-normative-glossary-and-invariants.md#rule-i-158)) — without a mechanism. This is the mechanism.

**The shape of the problem.** Conversation history is append-and-branch, never rewrite ([CV-04](../requirements/products/arcchat.md#rule-cv-04) there). A long conversation therefore has an immutable message sequence that eventually exceeds the model's context. Compaction must reduce what is *sent* without touching what is *stored*.

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
| HC-02 | **A `CompactionRecord` is a derived store** and obeys [DS-01](data-model/03-derived-stores.md#rule-ds-01)…[DS-07](data-model/03-derived-stores.md#rule-ds-07): rebuildable from the messages, never authoritative, and invalidated when its key inputs change. Losing every record costs compute, never content. |
| HC-03 | **The most recent turns are always verbatim.** A configurable tail — never zero — is never compacted, because the immediate work is what the model most needs exactly. |
| HC-04 | **The opening intent is retained.** The head of a branch carries what the user actually asked for, and losing it is how a long agent run drifts from its objective. |
| HC-05 | **Compaction is disclosed.** The user can see that a span was compacted, see the record, and expand the underlying messages. A silently shortened history is indistinguishable from a model that forgot. |
| HC-06 | **A tool call and its result are compacted as a unit or not at all.** Keeping a call without its result, or a result without its call, produces a transcript the model reads as a failure. |
| HC-07 | **An approval, a refusal and a user correction are never compacted away.** They are decision points, and a model that loses them re-proposes what the user already refused. |
| HC-08 | **Compaction is itself a model call** with its own budget reservation, cost dimensions and tariff snapshot (`§3.1`). It is metered like any other, and it is charged as platform work rather than to the user's turn where policy says so ([CU-03](../requirements/05-ai-and-agent-execution.md#rule-cu-03) of the AI requirements). |
| HC-09 | **A compaction failure degrades to hard truncation with disclosure**, never to silent loss. The turn continues, and the truncation is stated in the request record. |
| HC-10 | **A `CompactionRecord` is scoped to its branch.** Branching from a compacted point inherits the records covering the shared prefix; it never inherits a record covering messages the new branch does not contain. |
| HC-11 | **A `CompactionRecord` is not personal memory** ([HM-03](../requirements/products/arcchat.md#rule-hm-03) there). It is never promoted into durable preference recall, never carried into another conversation, and never survives the branch it belongs to. |
| HC-12 | **Temporary Chat compacts in memory only.** No `CompactionRecord` is persisted, consistent with the mode's promise ([HM-06](../requirements/products/arcchat.md#rule-hm-06) there) — and the mode still says honestly that the model received the data. |

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
| AP-01 | **The suspended turn is fully durable**, because the approval is a durable object rather than a notification (`AP-01` of the security architecture). It survives a restart of either side ([WP-14.04](../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04)). |
| AP-02 | **A rejection is a tool result, not a turn failure.** The model is told and may propose an alternative — which is what makes approval feel like collaboration rather than a dead end. |
| AP-03 | **Resume revalidates context** ([SI-05](#rule-si-05)). |
| AP-04 | **An operation requiring local presence cannot be approved remotely** ([AZ-01](contracts/00-operation-catalogue.md#rule-az-01) of the operation catalogue), and the harness does not offer remote approval for it. |
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

**Prompt and response content is never written to telemetry** ([RD-01](13-observability-and-operations.md#rule-rd-01) of the observability architecture). Durable message parts are user content in the product store; the interaction record carries counts and identifiers only.

### 6.2 Cancellation

**The dispatch barrier divides this table.** Before it, nothing external has happened and a reservation may be released outright. After it, cancellation is a request to stop — it can never release a reservation whose dispatch intent is already committed, because [DB-01](data-model/00-data-model-overview.md#rule-db-01) makes an intent with no outcome mean *unknown*. Cancellation is a crash you asked for, and it gets the same treatment.

| Point | Relative to the barrier | Behaviour |
|---|---|---|
| Queued in `waitingCapacity` | **Before** — no reservation exists | Turn ends `cancelled`; nothing to release, nothing to settle |
| Admitted, intent **not yet committed** | **Before** | Immediate; the reserving transaction is abandoned or its reservation released outright |
| Admitted, intent **committed**, provider not yet called | **After** | **The reservation is not released.** Dispatch is asked to abort, and the turn resolves through `§6.4`'s ladder like any other unknown — released only once an outcome or the deadline says it is safe ([DB-03](data-model/00-data-model-overview.md#rule-db-03), `§7.6` of the commerce architecture) |
| Waiting in `waitingDevice` for a device tool | **After** — a `tool_request` exists | The request is withdrawn and expires; a device that already pulled it reports its own outcome, which decides ([CN-03](#rule-cn-03)) |
| During streaming | **After** | Stream aborted; partial text stored as `interrupted`; verified consumption within the authorised ceiling settles and **only the remainder releases** — completed provider work is not presumed refundable ([MT-09](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-09)) |
| During an invocation | **After** | Cancellation propagates; the capability's own semantics decide; effect certainty recorded |
| While awaiting approval | **Before**, for the un-dispatched step | Approval withdrawn; turn ends `cancelled` |

| # | Rule |
|---|---|
| CN-01 | **Cancellation is cooperative and always leaves a determinate state.** No path ends with a turn neither running nor finished. |
| CN-02 | **A cancelled turn settles its budget at actual usage** — the user is not charged for what was not consumed, and is charged for what was. |
| <a id="rule-cn-03"></a>CN-03 | **Cancellation during a non-idempotent invocation records `unknownEffect`** rather than assuming it did not happen. |
| <a id="rule-cn-04"></a>CN-04 | **A committed dispatch intent makes release conditional, never immediate.** Releasing on the cancel request would free capacity while a provider call may still be in flight, and settlement would then have no reservation to debit — the user gets free inference or the usage goes unrecorded. **The barrier, not the user's intent, decides what may be released** ([DB-01](data-model/00-data-model-overview.md#rule-db-01), [DB-03](data-model/00-data-model-overview.md#rule-db-03), [AD-10](16-billing-and-commerce-architecture.md#rule-ad-10) of the commerce architecture). |

### 6.3 Crash recovery

> **Corrected 2026-09-07.** The previous table said an absent command-log record made a re-attempt safe. That is true only when the log write and the effect are **the same transaction** — which holds for a local database write and holds for nothing else. A device tool, an MCP server, a provider call and any network side effect cannot commit atomically with a row in ArcForges' database. Absence of a record therefore proves **nothing**, and treating it as proof would duplicate real-world effects.

Recovery is decided by **dispatch intent**, not by outcome absence.

```
intent written, no outcome      ->  UNKNOWN        (never "did not happen")
intent written, outcome written ->  that outcome
no intent                       ->  did not happen (the only safe absence)
```

The asymmetry is the point: **the intent is written before the act, so its absence is meaningful and its presence is not.**

| State at crash | Recorded state | Effect certainty | On restart |
|---|---|---|---|
| Before the reserving transaction committed | No intent | **Did not happen** | Start the iteration cleanly |
| Between the dispatch barrier and any provider byte | Intent, no attempt outcome | **Unknown** | `§6.4` — resolve, do not assume |
| Mid-model-call, stream started | Intent + partial attempt | **Unknown**, and usage is partially known | Preserve available presentation separately; publish a final/interrupted message only through the terminal rule ([SR-04](#rule-sr-04)); reconcile usage (`§7.6` of the commerce architecture) |
| Mid-invocation of a **local** capability whose command record commits with its effect | Command record present or absent | **Decidable** — this is the one atomic case | Present ⇒ completed; absent ⇒ safe to re-attempt |
| Mid-invocation of a **device, MCP or network** capability | Intent, no result | **Unknown** | `§6.4`. Never re-attempt on absence alone |
| Mid-settlement | Reservation held, settlement absent | Decidable | Settlement is idempotent per attempt usage revision; re-run ([ST-03](16-billing-and-commerce-architecture.md#rule-st-03)) |
| Awaiting approval | Durable approval record | — | Nothing to do — durable by construction |

| # | Rule |
|---|---|
| CR-01 | **A local command log decides recovery only for effects that commit with it.** For an ArcNotes edit on the same device, the log write and the edit are one transaction and absence is proof. For anything crossing a process, a device or a network, it is not, and the design says so rather than relying on a convenient assumption. |
| CR-02 | The sweeper releases an orphaned **customer** hold at its reconciliation deadline ([UU-03](20-cross-system-lifecycles.md#rule-uu-03) of the cross-system lifecycles). It records a terminal no-later-customer-debit disposition. An unresolved supplier liability remains reserved and reconciled independently ([UC-02](16-billing-and-commerce-architecture.md#rule-uc-02) of the commerce architecture). |
| CR-03 | **Recovery is verifiable**: after restart, every task is in a valid state with a reason facet, and none is stuck in a transient state ([WP-16.00](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.00)). |
| CR-04 | **`Unknown` is a terminal-until-resolved state, not a synonym for failure.** It has its own reason facet, its own resolution path (`§6.4`) and its own user-visible presentation. Collapsing it into success or failure is what produces either a duplicated effect or a lost one. |

### 6.4 Resolving an unknown effect

Resolution is ordered from cheapest and most certain to least, and stops at the first that answers.

| # | Step | Applies when | Result |
|---|---|---|---|
| 1 | **Consult the declared idempotency** ([FL-08](../requirements/05-ai-and-agent-execution.md#rule-fl-08) of the AI requirements) | The capability declares `Idempotent` | Re-attempt with the same `CommandId`. One effect regardless of how many attempts ([CI-06](contracts/02-local-rpc-operations.md#rule-ci-06)) |
| 2 | **Ask the owner** | The capability declares a status or reconciliation operation | The owner's answer is authoritative; record it and continue |
| 3 | **Ask the provider** | A model attempt with a provider request identity ([MT-02](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-02)) | Usage and outcome from the provider's own record; settle against it ([MT-12](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-12)) |
| 4 | **Wait for the deadline** | Nothing above answers | The reconciliation deadline releases the customer hold while retaining the supplier liability ([UU-03](20-cross-system-lifecycles.md#rule-uu-03) of the lifecycles) |
| 5 | **Surface a decision** | The capability is non-idempotent, has no status operation, and the effect matters | Present what is known and let the user decide ([BE-01](contracts/03-realtime-and-bridge.md#rule-be-01) of the bridge contract). **Never retry silently** |

| # | Rule |
|---|---|
| <a id="rule-ur-01"></a>UR-01 | **Retry safety is a declared property of the capability, never inferred from the absence of a record** ([FL-08](../requirements/05-ai-and-agent-execution.md#rule-fl-08)). This is the rule the previous recovery table violated. |
| <a id="rule-ur-02"></a>UR-02 | **A capability that can produce an external effect and declares neither idempotency nor a status operation cannot be invoked by the Harness at all.** Such a capability would make every crash an unresolvable ambiguity, so the descriptor requirement is a precondition of registration, not a nicety ([WP-17.00](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.00)). |
| UR-03 | **Step 2 is why `CapabilityDescriptor` carries a status operation reference.** Without it there is no mechanical way to answer "did it happen", and every uncertain case escalates to a human. |
| <a id="rule-ur-04"></a>UR-04 | **The bridge's command log resolves the device case at step 1**, because the device's log commits with the device-local effect ([BI-02](contracts/03-realtime-and-bridge.md#rule-bi-02), [BI-03](contracts/03-realtime-and-bridge.md#rule-bi-03) of the bridge contract). It does not resolve an effect the device itself made across a further network. |

---

## 7. Streaming

### 7.1 Shared presentation storage and retention

`chat.stream_chunk` and `chat.stream_state` are short-lived **ordinary logged PostgreSQL tables** shared by every identical Cloud replica. They are presentation projections, have no aggregate revision and never appear in sync. They **are included in WAL/physical backups** with the rest of the database; calling them transient does not exclude their bytes. Online TTL and backup/PITR retention are distinct privacy boundaries. Access, encryption at rest, backup access and erasure-after-backup-expiry follow the deployment data policy. Restore purges transient rows and reconciles Task/attempt authority before serving traffic; no restored stream restarts provider work.

| Table | Required columns and constraints |
|---|---|
| `stream_chunk` | `(task_id, stream_id, from_offset)` PK; UTF-8 payload, end offset, created/expiry times; contiguous append, bounded bytes, immutable within a stream. Offset is measured in UTF-8 bytes, at code-point boundaries. |
| `stream_state` | `(task_id, stream_id)` PK; provider attempt ID, owner fence, state `open/completed/truncated/superseded/evicted`, next offset, optional successor stream ID, current flag, expiry. Unique current stream per Task; append locks this row and verifies the current Task lease/fence. |

| # | Rule |
|---|---|
| <a id="rule-sb-01"></a>SB-01 | Presentation is not canonical Chat history. Complete model responses/tool proposals become immutable `task.iteration_output` before customer settlement; terminal Task publication separately creates the final/interrupted message. Loss of presentation cannot erase either durable fact. |
| SB-02 | Each provider attempt has a new stream ID. Retrying or starting a later model invocation cannot concatenate two attempts into one answer. The previous stream identifies its successor where one exists. |
| SB-03 | Initial limits: 64 KiB per chunk/read, 4 MiB per stream, flush at 250 ms or the chunk bound, ten-minute tail TTL and 24-hour state-marker retention, all bounded validated deployment parameters. Unicode boundary-safe appends update chunk + next offset together. |
| <a id="rule-sb-04"></a>SB-04 | Reads use the shared primary authority. A replica has no private cache whose miss can be mistaken for eviction. Database unavailability is a transport failure with retry, not an empty successful stream. |
| SB-05 | Missing chunks do not determine Task state. Missing/expired stream metadata resolves through the authoritative Task and provider-attempt receipt; it never fabricates `open` indefinitely or a nonexistent final message. |
| SB-06 | The sweeper marks eviction before removing chunks. A later reader still gets Task state, current attempt, durable output/final-message references and a retry/reconciliation action. State-marker expiry cannot delete Task authority. |
| SB-07 | A size/time bound sets **truncated**, never `completed`. Generation may continue. The client displays unavailable live output and polls Task status; it requests a final message only when that reference exists. |
| SB-08 | Lease takeover preserves readable buffered bytes, not a dead process's provider socket. Only a surviving fenced attempt or a provider's verified resume protocol may continue that invocation. Otherwise record interrupted/unknown, reconcile supplier usage, and require the declared retry authority before a new invocation. |
| SB-09 | Append, state transition and Task outcome publication reject a stale fence. Each model invocation's stream can complete while the Task is waiting for tools or another model call. Stream completion never implies Turn completion. |

### 7.2 Client read contract

`task.readStream(taskId, streamId?, fromOffset)` returns a bounded JSON object:

```
{ streamId?, fromOffset, text, nextOffset, streamState,
  taskState, taskRevision, attemptState?, currentStreamId?,
  iterationOutputRef?, finalMessageRef?, noAnswerReason?, retryAfter? }
```

`text` is decoded UTF-8 text, not a Base64 `byte[]`; large artifacts continue to use ResourceRef. A supplied offset must be a returned boundary; invalid or expired ranges have a typed reset action. Omitting stream ID selects the current attempt. An authoritative read returns Task status even when no stream has started or retained data has expired. Permission and workspace checks apply to every read and reference.

| # | Rule |
|---|---|
| <a id="rule-sr-01"></a>SR-01 | `task.outputAppended` remains an optional identifier/offset hint with no content. Polling the same read contract works without SignalR. |
| SR-02 | `open` means this attempt may append; `completed` means this attempt's stream ended; `truncated` means buffering stopped; `superseded` names a replacement; `evicted` means retained presentation expired. **None alone states that the Task completed.** No stream yet uses a null stream ID and the durable Task status. |
| SR-03 | Reconnect resumes at the last returned offset for the same stream. A successor resets presentation to its own origin; the client does not concatenate a retry with old text. An expired range requests the authoritative iteration/message view, with a visible live-output gap where necessary. |
| <a id="rule-sr-04"></a>SR-04 | Only a non-null final-message reference authorises fetching a final answer. A terminal no-answer Task shows its reason; running/waiting Task with completed/truncated/evicted presentation continues bounded status polling. |
| SR-05 | Auth is rechecked on each read. A lost buffer/metadata row, lease death, cancellation and database restore all return a resolvable durable Task state or an explicit unavailable error. |
| SR-06 | Clients never persist concatenated presentation as the canonical message. They replace it with the committed output/message identified by Cloud. |
| SR-07 | Desktop, Mobile and Web use the identical fallback. No client model loop, sticky routing, or second streaming service is introduced. |

### 7.3 Durable output

| # | Rule |
|---|---|
| <a id="rule-st-01"></a>ST-01 | An invocation's completed/interrupted output is committed once to `task.iteration_output`, with parsed proposals, provider-attempt identity and checksum. Final Turn publication creates its immutable Chat message separately. |
| ST-02 | Deltas are best effort; losing them cannot lose committed output, cause a debit without durable delivered evidence, or justify repeating an unknown provider call. |
| ST-03 | A tool call enters execution/UI only after complete parsing and schema validation, never from partial stream syntax. |
| ST-04 | Every surface reads the same authoritative Task/output/message path after a presentation gap. |
| ST-05 | Interrupted text remains explicitly interrupted; a stream state never relabels it complete. |

---

## 8. Provider failure handling

> **Corrected 2026-09-07.** A timeout before the first token was previously classified *did not happen* and retried. **A missing response is not evidence that the provider did no work** — the request may have been received, processed and billed while the response was lost. That classification contradicted [MT-12](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-12) of the commerce requirements, [UU-02](20-cross-system-lifecycles.md#rule-uu-02) of the lifecycles and [XL-04](20-cross-system-lifecycles.md#rule-xl-04)'s own rule that `unknown` is never silently resolved to `didNotHappen`. Certainty now depends on **where the failure occurred relative to dispatch**, not on whether bytes came back.

| Failure | Dispatched? | Effect certainty | Harness action |
|---|---|---|---|
| Refused before dispatch — admission, unpriced route, bad request | **No** | **Did not happen** | Fail with the stated reason; release the reservation in full |
| Connection refused or DNS failure — no request left the host | **No** | **Did not happen** | Retry within budget |
| Rate limited, response received | Yes, rejected by the provider | **Did not happen** — the provider said so | Honour `retryAfter`; retry within budget |
| **Timeout before any token** | **Yes** | **Unknown** | `§6.4`: reconcile against the provider's own record before deciding. **Never an automatic retry** |
| Timeout mid-stream | Yes | **Unknown**, usage partially known | Store the partial as `interrupted`; reconcile usage; ask the user or the profile before retrying |
| Response lost after dispatch | Yes | **Unknown** | `§6.4` |
| Content refused by the provider, response received | Yes | **Happened** — and may be billable | Record as the turn outcome; settle whatever the provider reports |
| Context too long, rejected before generation | Yes, rejected | **Did not happen** for generation | Compact harder (`§4.6`) and retry once |
| Model withdrawn | No | **Did not happen** | Fail with a stated reason; **no silent substitution** ([WP-43.05](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.05)) |
| Provider outage, no route reached | **No** | **Did not happen** | Fall back where policy allows, else fail; release the reservation |
| All routes unavailable | No | **Did not happen** | Fail with a stated reason; page-worthy ([AL-02](13-observability-and-operations.md#rule-al-02) of the observability architecture) |

| # | Rule |
|---|---|
| PF-01 | **A provider outage that never reached a route consumes no credit** ([WP-43.05](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.05)), because nothing was dispatched. An outage *after* dispatch is an `unknown`, and its customer hold is released at the reconciliation deadline while the supplier liability is retained ([UU-03](20-cross-system-lifecycles.md#rule-uu-03) of the lifecycles). |
| PF-06 | **The dividing line is the dispatch barrier** ([DB-01](data-model/00-data-model-overview.md#rule-db-01) of the data-model overview), not the arrival of bytes. Before it, absence is proof; after it, absence is `unknown`. |
| PF-07 | **An `unknown` is never retried automatically**, whatever the transport reported. It enters `§6.4`, which resolves it by declared idempotency, an owner status operation, the provider's own record, the deadline, or a user decision — in that order. |
| PF-02 | **A fallback is a policy decision, not an adapter default**, and the substitution is recorded in the interaction record and shown to the user. |
| PF-03 | **A retry produces a new Attempt inside the same Step, never a new Step** ([EX-09](../requirements/05-ai-and-agent-execution.md#rule-ex-09) there), and the `CommandId` is unchanged because the business action is unchanged ([ID-01](../requirements/05-ai-and-agent-execution.md#rule-id-01) there, [I-085](../requirements/01-normative-glossary-and-invariants.md#rule-i-085)). |
| PF-04 | **A platform-caused retry is not charged to the user** ([CU-03](../requirements/05-ai-and-agent-execution.md#rule-cu-03) there). A logical AI request whose first provider attempt failed and whose second succeeded is charged for the useful work only. |
| PF-05 | **Retry safety is declared by the capability owner, never guessed** ([FL-08](../requirements/05-ai-and-agent-execution.md#rule-fl-08) there), which is why the harness never infers idempotency from an operation's name. |

---

## 9. What the Harness is not

| # | Rule |
|---|---|
| <a id="rule-xa-01"></a>XA-01 | **There is no external-agent integration.** External-agent providers, ACP adapters, session mapping, delegation leases and result adapters are all retired ([EA-01](../requirements/08-extensions-and-developer-platform.md#rule-ea-01)–[EA-06](../requirements/08-extensions-and-developer-platform.md#rule-ea-06) of the extension requirements, [I-313](../requirements/01-normative-glossary-and-invariants.md#rule-i-313), [I-314](../requirements/01-normative-glossary-and-invariants.md#rule-i-314) retired). |
| <a id="rule-xa-02"></a>XA-02 | There are no agent teams, sub-agents or delegated agent Tasks ([EA-08](../requirements/08-extensions-and-developer-platform.md#rule-ea-08) of the extension requirements). Bounded parallel tool calls remain Steps inside the same Run. Long native or Cloud product operations return ProductJob references with their own status, cancellation and owner; they contain no model loop ([CT-01](../requirements/05-ai-and-agent-execution.md#rule-ct-01)–[CT-07](../requirements/05-ai-and-agent-execution.md#rule-ct-07) of the AI requirements). |
| <a id="rule-xa-03"></a>XA-03 | **A package, connector or MCP tool cannot start an autonomous delegated agent** ([EA-08](../requirements/08-extensions-and-developer-platform.md#rule-ea-08) there). An integration contributes tools; it never contributes a planner. |
| XA-04 | **MCP remains a tool-integration edge adapter**, never the internal protocol (**[V-02](../assurance/phase-1-official-verification.md#rule-v-02)**, [MC-01](../requirements/08-extensions-and-developer-platform.md#rule-mc-01) of the extension requirements). An MCP tool maps to a declared capability carrying risk, permission and provenance — it is never injected as a raw tool ([MC-02](../requirements/08-extensions-and-developer-platform.md#rule-mc-02) there). |
| XA-05 | **MCP tool descriptions, prompts and resource contents are untrusted data** ([MC-07](../requirements/08-extensions-and-developer-platform.md#rule-mc-07) there, [I-262](../requirements/01-normative-glossary-and-invariants.md#rule-i-262), [I-263](../requirements/01-normative-glossary-and-invariants.md#rule-i-263)), and an MCP server changing its tool set re-enters permission review ([MC-10](../requirements/08-extensions-and-developer-platform.md#rule-mc-10) there). |
| <a id="rule-xa-06"></a>XA-06 | **Hidden model reasoning never enters the product model** ([EA-07](../requirements/08-extensions-and-developer-platform.md#rule-ea-07) there, [PR-10](../requirements/05-ai-and-agent-execution.md#rule-pr-10) of the AI requirements, [I-107](../requirements/01-normative-glossary-and-invariants.md#rule-i-107)). Reasoning appears as a metered cost category ([MT-03](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-03)), never as content or trace. |
| <a id="rule-xa-07"></a>XA-07 | **The Harness is not a native Product Job runner.** A render, capture, index or export is owned by its product ([CM-04](09-ai-and-agent-runtime-architecture.md#rule-cm-04) of the runtime architecture, [I-121](../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../requirements/01-normative-glossary-and-invariants.md#rule-i-485)); the Harness may observe one through a status tool, never adopt it as a Step. |

---

## 10. Tool locality

The Harness always runs in Cloud ([LS-02](#rule-ls-02)). What varies is **where each tool executes** (`§9` of the runtime architecture).

| Tool locality | When | Constraint |
|---|---|---|
| **Cloud tool** | The capability is Cloud-owned | Executes in-process inside the turn |
| **Device tool** | The capability requires a desktop | Each invocation is a durable `ToolRequest` pulled by the device (`§5` of the bridge contract) |

| # | Rule |
|---|---|
| PL-01 | **A Task is Cloud-owned from creation** ([TO-01](data-model/00-data-model-overview.md#rule-to-01) of the data-model overview). There is no local or hybrid task placement to decide. |
| <a id="rule-pl-02"></a>PL-02 | **A device tool with no eligible online device enters `WaitingForDevice`** with a stated reason and a bounded wait — it never degrades to a cloud approximation. |
| <a id="rule-pl-03"></a>PL-03 | **Waiting consumes no model capacity.** A turn parked on a device or an approval releases its included-capacity hold at the safe boundary and re-reserves on resume ([AC-05](../requirements/04-commerce-entitlement-and-credits.md#rule-ac-05) of the commerce requirements). This is what stops one waiting Task from reserving the whole workspace. |
| PL-04 | **Local-only data never leaves the device to enable a cloud tool** ([OW-08](../requirements/05-ai-and-agent-execution.md#rule-ow-08) of the AI requirements). If the data cannot leave, the device tool runs or the step fails with a reason. |
| PL-05 | **Cached, unacknowledged client state is never treated as Cloud context.** Only acknowledged Cloud revisions enter the context pack ([I-498](../requirements/01-normative-glossary-and-invariants.md#rule-i-498)); a pending local edit is visible to the user, not to the model, until it is acknowledged. |

---

## 11. Transparency and cost

| # | Rule |
|---|---|
| TC-01 | **AI-generated content carries the marking its regime requires**, per artifact type (**[V-01](../assurance/phase-1-official-verification.md#rule-v-01)**; [TA-02](08-security-architecture.md#rule-ta-02), [TA-03](08-security-architecture.md#rule-ta-03) of the security architecture). Marking is applied at the point of generation, which makes it a property of this harness and the artifact format — not of the user interface. |
| TC-02 | **A turn's cost is explainable**: which model, which tariff version, which cost dimensions — including reasoning tokens, cached input and cache writes — and which counts (`§11.3` of the AI requirements, [WP-43.04](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.04)). |
| TC-03 | **The user can see what context was sent** — sources and revisions — without the harness storing the prompt in telemetry. |
| TC-04 | **A tool call and its result are visible in the conversation** as durable parts, so the user can audit what the agent did. |
| TC-05 | **Trace is not chain-of-thought** ([PR-10](../requirements/05-ai-and-agent-execution.md#rule-pr-10) of the AI requirements, [I-107](../requirements/01-normative-glossary-and-invariants.md#rule-i-107)). Hidden model reasoning is never surfaced as trace, and reasoning tokens appear as a cost dimension rather than as content. |

---

## 12. Verification

| # | Obligation | Where |
|---|---|---|
| HV-01 | A multi-step turn completes end to end in the single Cloud host, against a real provider | [WP-43.07](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07), [WP-17.01](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.01) |
| HV-02 | A model-proposed action reaches a real product operation through the full security pipeline | [WP-20.02](../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20.02) |
| HV-03 | A crash at each loop point resumes correctly, with no duplicate effect and no duplicate charge | [WP-52.00](../planning/work-packages/52-cloud-harness.md#rule-wp-52.00), [WP-16.00](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.00), [WP-26.03](../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) |
| HV-04 | An approval-suspended turn survives restart of either side and resumes with revalidated context | [WP-14.04](../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.04), [WP-16.05](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.05) |
| HV-05 | An interrupted stream is never stored as complete, and cumulative stream usage is not summed as independent consumption | [WP-15.00](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.00), [WP-43.02](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.02) |
| HV-06 | Stale context is detected before a write, and the model is told rather than silently corrected | [WP-20.02](../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20.02) |
| HV-07 | Every loop bound ends the turn with a stated reason; no unbounded loop is reachable | [WP-52.00](../planning/work-packages/52-cloud-harness.md#rule-wp-52.00), [WP-16.07](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.07) |
| HV-08 | A cancelled turn settles verified consumption and releases the remainder | [WP-16.05](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.05), [WP-43.02](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.02) |
| HV-08a | **Cancellation arriving after the dispatch intent commits does not release the reservation.** The turn resolves through the unknown ladder, and a provider response arriving after the cancel still settles against the reservation it was dispatched under ([CN-04](#rule-cn-04), [DB-03](data-model/00-data-model-overview.md#rule-db-03)) | [WP-52.02](../planning/work-packages/52-cloud-harness.md#rule-wp-52.02), [WP-43.02](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.02) |
| <a id="rule-hv-09"></a>HV-09 | **No client runs a model loop.** A structural test asserts no desktop, mobile or browser assembly references a provider adapter or holds a provider credential | [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), [WP-17.01](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.01) |
| HV-10 | A capability not declarable to the model is never proposed, and never invocable if proposed | [WP-17.00](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.00) |
| HV-11 | **No end-user BYOK path exists.** No operation, schema field, setting or UI accepts a customer provider key | [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), [WP-43.03](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.03) |
| HV-12 | A provider outage releases the customer reservation or appends a compensating adjustment, and retains the supplier cost | [WP-43.05](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.05) |
| HV-13 | Two tool calls writing the same target never execute in parallel; two reads of independent targets do | [WP-52.00](../planning/work-packages/52-cloud-harness.md#rule-wp-52.00), [WP-20.02](../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20.02) |
| HV-14 | An approval mid-batch suspends the whole batch, and resume re-evaluates the remainder against revalidated context | [WP-52.00](../planning/work-packages/52-cloud-harness.md#rule-wp-52.00), [WP-16.05](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.05) |
| HV-15 | A failure inside a parallel group returns the siblings' real results alongside the failure | [WP-52.00](../planning/work-packages/52-cloud-harness.md#rule-wp-52.00), [WP-16.02](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.02) |
| HV-16 | A platform-caused provider retry is charged once to the customer and remains fully visible in supplier cost | [WP-43.02](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.02), [WP-43.04](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.04) |
| HV-17 | A turn waiting for a device or an approval holds no included capacity, and cannot reserve the workspace indefinitely | [WP-16.05](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.05), [WP-43.02](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.02) |
| <a id="rule-hv-18"></a>HV-18 | **No agent team, sub-agent or external-agent delegation is reachable.** A structural test asserts no delegation contribution kind and no second planner exists | [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), [WP-41.07](../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41.07) |
| HV-19 | MCP tool descriptions and retrieved content are treated as data; an instruction inside them changes no behaviour | [WP-11.06](../planning/work-packages/11-security-foundation.md#rule-wp-11.06), [WP-41.07](../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41.07) |
| HV-20 | Hidden model reasoning never appears in trace, and reasoning tokens appear only as a metered cost category | [WP-16.06](../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.06), [WP-43.02](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.02) |
| HV-21 | The stored branch is byte-identical before and after compaction, and losing every `CompactionRecord` costs no content | [WP-52.01](../planning/work-packages/52-cloud-harness.md#rule-wp-52.01) |
| HV-22 | A compacted span never loses an approval, a refusal or a user correction, and never separates a tool call from its result | [WP-52.01](../planning/work-packages/52-cloud-harness.md#rule-wp-52.01) |
| HV-23 | A `CompactionRecord` never becomes personal memory and never crosses a branch or a conversation | [WP-52.01](../planning/work-packages/52-cloud-harness.md#rule-wp-52.01), [WP-15.01](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.01) |
| HV-24 | Official inference is refused without an active paid service term, whatever the credit balance | [WP-42.11](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11), [WP-43.02](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.02) |
| HV-25 | Only acknowledged Cloud revisions enter the context pack; a pending client edit never reaches the model as context | [WP-25.01](../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.01), [WP-20.02](../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20.02) |
