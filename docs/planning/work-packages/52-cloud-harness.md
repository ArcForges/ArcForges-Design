# WP-52 — The Cloud Harness

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion *(sequenced after `43`; numbered `52` because `00`–`51` are allocated and a retired identifier is never reused)*
> Upstream: `15`, `17`, `21`, `23`, `42`, `43` · Downstream: `50`

> **Goal.** Build the **single Cloud Harness** of [`../../architecture/17-agent-harness.md`](../../architecture/17-agent-harness.md): the turn loop, tool batching, context assembly, compaction, approval interleaving, streaming, cancellation and recovery — running in `ArcForges.Cloud.Host`, against real admission and real metering.

---

## 1. Scope and purpose

**Why this package exists, and why it is here.** P2-006 moved the model loop to Cloud (`LS-02`). Its work was previously distributed across `WP-13.00` (a Native AOT desktop agent probe), `WP-16` (a unified Task engine that also covered agent runs), `WP-17.08`/`WP-17.09` (the turn loop and compaction, in a **Phase C** desktop package) and `WP-20.03` (the first agent-driven workflow, in **Phase D**). **Every one of those placements is now unexecutable**: the Harness runs in the Cloud host, which does not exist until Phase E, and it admits and meters through Commerce and Cloud AI, which do not exist until Phase J.

Rather than leave a package whose steps cannot run in their stated order, the Harness is one package at its real dependency position.

**In scope.** The turn loop and its durable iteration; response classification and continuation; loop bounds and progress detection; parallel tool batching against declared conflict sets; context assembly, staleness invalidation and tool-declaration filtering; history compaction; approval interleaving across restarts; the stream buffer and its read path; crash recovery by dispatch intent; provider failure classification; and the first agent-driven cross-product workflow.

**Out of scope.** Provider routing, tariffs, normalisation and settlement (`43`). Admission, capacity and service terms (`42`). The device-side tool executor (`17`, `26`). Product capability surfaces (`18`, `20`, `33`, `36`).

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/17-agent-harness.md`](../../architecture/17-agent-harness.md) | The complete Harness design |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) | The runtime it executes inside |
| `WP-21` output | The single host and its lease-fenced hosted services |
| `WP-23` output | The public API surface the clients use |
| `WP-42` output | Service term, capacity, admission (`§7.3` of the commerce architecture) |
| `WP-43` output | Provider adapters, supplier prices, customer tariffs, settlement |
| `WP-17` output | The device-side tool executor and the desktop surfaces |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **One Harness, Cloud-only** (`LS-02`). No desktop, mobile or browser assembly contains a turn loop, a planner or a provider adapter. |
| BR-02 | **The Cloud host is JIT, not AOT** (**D-008**, **V-03**). No AOT constraint applies to Harness code, and no gate here asks for an AOT publish. |
| BR-03 | **A Cloud Agent Task is not a native Product Job** (`CM-04`, `I-121`, `I-485`). This package owns the former; `WP-16` owns the latter. |
| BR-04 | **Admission commits before dispatch** (`§6.1.2` of the data-model overview). Nothing crosses the dispatch barrier inside a transaction. |
| BR-05 | **Recovery is decided by dispatch intent, never by outcome absence** (`§6.3` of the harness). Retry safety is a declared capability property (`FL-08`). |
| BR-06 | **No agent teams, sub-agents or external-agent delegation** (`EA-01`–`EA-08`, `§9` of the harness). |
| BR-07 | **The stream buffer is transient presentation state**, never a message and never synchronised (`SB-01`). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.AgentRuntime/` | The turn loop, batching, context assembly, compaction, recovery |
| `src/Cloud/ArcForges.Cloud.Modules.Agent/` | Task, run, plan, step, attempt persistence; approval records |
| `src/Cloud/ArcForges.Cloud.Modules.Chat/` | The stream buffer and the committed message write path (`CW-02`) |
| `src/Cloud/ArcForges.Cloud.PublicApi/` | `task.readStream` and the turn operations |
| `src/Cloud/ArcForges.Cloud.BackgroundJobs/` | The harness runner as a lease-fenced hosted service |
| `tests/Cloud.Tests.Integration/` | Loop, recovery, streaming, compaction and workflow suites |

**Major types introduced.** `TurnLoop`, `TurnIteration`, `ToolCallBatch`, `ConflictSet`, `ContextPack`, `CompactionRecord`, `StreamBuffer`, `DispatchIntent`, `EffectCertainty`, `ResolutionLadder`.

---

## 5. Required implementation work

### WP-52.00 — The turn loop, batching and bounds

**What must be fully done.** The durable turn loop of `§2`: every iteration persisted before the next begins; response classification and continuation decisions (`§3.2`); every loop bound ending the turn with a stated reason (`§3.3`); no-progress detection (`§3.4`); and parallel tool batching against declared conflict sets with an undeclared capability treated as exclusive (`§2.1`).

**Testing requirements.** A crash-injection suite resuming from each loop point with no duplicate effect and no duplicate charge; a bounds suite proving no unbounded loop is reachable; a repetition test proving no-progress termination; a conflict suite proving two writes to one target never run in parallel while two independent reads do; a partial-failure test proving a failing call returns its siblings' real results.

**Completion gate.** No unbounded loop is reachable, every bound ends the turn with a stated reason, and parallel batching never violates a declared conflict.

### WP-52.01 — Context assembly and compaction

**What must be fully done.** Assembly in the order of `§4.2` — references first, content last — with permission applied per source; revision stamping and staleness invalidation before a write (`§4.3`); tool-declaration filtering so an uninvocable capability is never declared (`§4.4`); budget and disclosed truncation (`§4.5`); and history compaction as a derived `CompactionRecord` (`§4.6`).

**Testing requirements.** A permission test asserting a refused source contributes nothing including to counts; a staleness test asserting a changed revision is reported to the model rather than silently substituted; **a test asserting only acknowledged Cloud revisions enter the pack** and a pending client edit never does (`PK-04`, `I-498`); a long-conversation suite proving the stored branch is byte-identical before and after compaction; a decision-retention test proving a refused proposal is not re-proposed.

**Completion gate.** Context is bounded, permission-filtered and revision-stamped; compaction reduces what is sent without altering what is stored and never loses an approval, a refusal or a user correction.

### WP-52.02 — Approval, cancellation and crash recovery

**What must be fully done.** Durable approval suspension surviving a restart of either side, with context revalidated on resume (`§5`); cancellation at every point leaving a determinate state (`§6.2`); and recovery decided by **dispatch intent** with the resolution ladder of `§6.4` — declared idempotency, owner status operation, provider record, deadline, user decision.

**Testing requirements.** An approval-suspended turn surviving restart of both sides; cancellation at each loop point; **a crash after dispatch but before any outcome, asserting the state is `unknown` and is not retried automatically**; a capability declaring neither idempotency nor a status operation, asserting it **cannot be registered** (`UR-02`); a device-tool crash resolved by the device command log.

**Completion gate.** No crash path resolves an uncertain external effect to *did not happen*, and no non-idempotent capability is retried without a resolution step.

### WP-52.03 — Streaming across identical replicas

**What must be fully done.** The transient buffer of `§7.1` of the harness as `chat.stream_chunk` and `chat.stream_state` rows **in the shared database**, so any replica serves any read (`SB-04`). Monotonic state transitions; exactly one `current` attempt per task; eviction that sets state **before** deleting chunks so a late reader still gets an answer (`SB-06`); bounded, batched appends (`SB-09`); and `task.readStream` with `streamId` optional. The committed message written once on completion (`ST-01`).

**Testing requirements.** **A read served by a replica that never wrote the stream**, returning identical bytes (`SB-04`). **A read arriving before any chunk exists, asserting `open` — not `evicted`, not an error** (`SB-05`). Lease takeover mid-stream, asserting the same `stream_id` continues or a new one supersedes, with no silent gap (`SB-08`). A drained replica mid-stream. A restart mid-stream. Eviction with a late reader, asserting the state row still answers after chunks are gone. A superseded attempt, asserting the client discards what it rendered. **Polling with realtime fully disabled reaching byte-identical output** (`SR-02`). An `evicted` state with a still-running Task, asserting the UI reports lost presentation rather than a finished turn (`SR-07`). A bound-exceeded stream continuing the turn. An interrupted stream stored as `interrupted`, never complete.

**Completion gate.** **A read reaching any replica returns correct data**, a miss is never reported as an eviction, takeover and restart lose no output, and every surface reaches identical output with realtime disabled.

### WP-52.04 — Provider failure and effect certainty

**What must be fully done.** The classification of `§8`, keyed on whether dispatch occurred rather than on whether bytes returned; the `unknown` path into `§6.4`; release of customer holds at the reconciliation deadline with the supplier liability retained (`UU-03`).

**Testing requirements.** A timeout before the first token asserting **`unknown`, not a retry**; a lost response reconciled against the provider's own record; a platform-caused retry charged once to the customer and fully visible in supplier cost; a deadline expiry releasing the customer hold while retaining the supplier liability.

**Completion gate.** No failure path silently resolves `unknown` to `didNotHappen`, and no dispatched request is retried automatically.

### WP-52.05 — The first agent-driven cross-product workflow

**What must be fully done.** *(Relocated from `WP-20.03`, which was in Phase D and could not run before the Cloud Harness existed.)* The end-to-end workflow of `I2 §III.5`: ArcChat is asked to produce a report, ArcNotes creates the document and receives its content through a device tool, the user approves, the result saves, undoes and recovers, and an artifact reference resolves.

**Testing requirements.** The full workflow end to end — request, admission, dispatch, document creation, block insertion, approval, write, undo, save, kill, recovery, artifact resolution — with **every failure variant** exercised: device offline, approval expired, capacity exhausted mid-turn, term expiring mid-turn, and a crash after dispatch.

**Completion gate.** The full workflow passes end to end against the real Cloud host, real admission and a real provider, and every failure variant reaches a stated terminal state.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Task, run, plan, step, attempt, approval; the `CompactionRecord` derived store |
| Protocol | `task.readStream`; `task.outputAppended` payload; the turn operations |
| UI | Streaming display, approval prompts, admission reasons — all client-side rendering of Cloud state |
| Security | Every tool invocation passes the pipeline; MCP content stays untrusted data |
| Platform | Cloud JIT only; **no AOT constraint applies to this package** |
| Migration | `CompactionRecord` is derived and rebuildable; losing it costs compute, never content |
| Compatibility | The turn and stream contracts are consumed by Desktop, Web and Mobile alike |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Loop-bound, crash-resume, no-progress and conflict-batching results | `WP-52.00` |
| Context permission, staleness and compaction results | `WP-52.01` |
| Approval-across-restart, cancellation and uncertain-effect results | `WP-52.02` |
| Cross-replica read, miss-is-not-eviction, takeover, realtime-disabled equivalence and buffer-lifecycle results | `WP-52.03` |
| Effect-certainty classification and deadline-release results | `WP-52.04` |
| Full cross-product workflow with every failure variant | `WP-52.05` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Multi-step turns execute in the single Cloud host against a real provider, and **no desktop, mobile or browser assembly contains a turn loop, a planner or a provider adapter**.
2. No unbounded loop is reachable; every bound ends the turn with a stated reason.
3. Parallel batching never violates a declared conflict, and a failure returns its siblings' real results.
4. Only acknowledged Cloud revisions enter the context pack; a pending client edit never reaches the model.
5. Compaction reduces what is sent without altering what is stored, and never loses an approval, a refusal or a user correction.
6. An approval-suspended turn survives restart of either side and resumes with revalidated context.
7. **No crash or failure path resolves an uncertain external effect to *did not happen***, and no non-idempotent capability is retried without a resolution step.
8. A capability that can produce an external effect and declares neither idempotency nor a status operation **cannot be registered**.
9. Every surface reaches identical streamed output **with realtime fully disabled**; **a read served by a replica that never wrote the stream returns correct data**; a miss is never reported as an eviction; and no buffer byte is persisted as a message.
10. The full cross-product workflow passes end to end with every failure variant reaching a stated terminal state.

---

## 9. Dependencies

**Upstream.** `15` (conversation domain), `17` (device tool executor, desktop surfaces), `21` (host and hosted services), `23` (public API), `42` (service term, capacity, admission), `43` (providers, prices, settlement).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `50` — Full-platform release | The Harness acceptance evidence and the cross-product workflow |
