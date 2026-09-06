# WP-16 — Unified Execution Engine

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: C — First real slice
> Upstream: `09`, `11`, `14` · Downstream: `17`, `43`

> **Goal.** Implement the **native Product Job** model — the lifecycle every long-running *product* operation shares: render, capture, index, import, export. Cloud Agent Tasks are a **different** model owned by `WP-44` (`CM-04`, `I-121`, `I-485`). This package delivers lifecycle states, failure classification, checkpoints, compensation, approval, steering and budget — durable, resumable and identical wherever it runs.

---

## 1. Scope and purpose

**In scope.** The task engine: the execution chain and its persistence; lifecycle states and reason facets; failure classification with effect certainty; child tasks; checkpoints and compensation; approval and steering integration; the budget reserve-then-settle interface; progress, outcome and trace; crash recovery; and concurrency control.

**Out of scope.** Provider routing and real metering (`43`) — the budget interface exists here, its economics do not. Cloud placement (`26`). Automation triggers (`17`). Workflow blueprints (`41`).

> **Scope amendment, 2026-09-07 (P2-006).** The previous goal said *an agent run, a render, a capture, an import and an automation are the same Task*. Under P2-006 they are **two** models: a **Cloud Agent Task** owned by the Harness, and a **native Product Job** owned by the product that runs it (`CM-04` of the runtime architecture). Conflating them would put a render under AI metering and Cloud recovery, and would put an agent turn under a desktop lifecycle. This package now owns the Product Job; `WP-44` owns the Agent Task. They share vocabulary and failure classification deliberately — not an implementation.

**Why this package exists.** Every long-running *product* operation — a render, a capture, an index rebuild, an import, an export — has the same lifecycle needs. Building four of them produces four different recovery stories and four different approval models.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/05-ai-and-agent-execution.md`](../../requirements/05-ai-and-agent-execution.md) | The full execution chain, lifecycle, ownership, checkpoints, approval and budget model |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) | The engine structure, persistence, idempotency identities and trace systems |
| `WP-04` output | The four execution identities and idempotency semantics |
| `WP-09`, `WP-11` output | Capability invocation and the security pipeline |
| `WP-13.00` output | Proof that an agent loop runs under Native AOT |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **One Task model serves every long-running operation**, whatever its placement. |
| BR-02 | **`Task ≠ Run ≠ Plan ≠ Step ≠ Attempt`.** Five distinct concepts with five distinct lifecycles. |
| BR-03 | **A retry allocates a new attempt and reuses the command identity** (`WP-04.01`). |
| BR-04 | **Failure classification includes effect certainty**: definitely-not, definitely-did, or unknown. An unknown effect never auto-retries a non-idempotent operation. |
| BR-05 | **A task is owned by exactly one product** and its ownership never transfers. |
| BR-06 | **Approval is a discrete authorization; steering adjusts a running operation and grants nothing** (`WP-11.03`). |
| BR-07 | **Budget is reserved before execution and settled after**, with a hard stop at zero and no overdraft (**D-020**). |
| BR-08 | **A checkpoint is not an undo entry and not a revision** (`QI-09`). |
| BR-09 | **Compensation is explicit per step**, declared where an operation is not naturally reversible. |
| BR-10 | **Progress is an estimate; outcome is a fact.** They are separate channels and never conflated. |
| BR-11 | **A task survives a process crash** and resumes or fails explicitly — never silently disappears. |
| BR-12 | **Loop and storm protection are engine concerns**, not left to each caller. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/BuildingBlocks/ArcForges.Execution/` | Created: the task engine, scheduler, state machine, checkpoint and compensation infrastructure |
| `src/BuildingBlocks/ArcForges.Execution.Persistence/` | Created: durable execution state and its recovery |
| `src/BuildingBlocks/ArcForges.Execution.Budget/` | Created: the reserve-settle-release interface, implemented against a local stub here |
| `src/ArcChat/ArcChat.Agent/` | The agent runtime hosting plans over the engine |
| `tests/ExecutionEngineTests/` | Lifecycle, idempotency, recovery, compensation, concurrency and storm-protection suites |

**Major types introduced.** `Intent`, `TaskRecord`, `Run`, `Plan`, `PlanStep`, `Attempt`, `ExecutionState`, `ReasonFacet`, `FailureClass`, `EffectCertainty`, `Checkpoint`, `CompensationAction`, `ApprovalGate`, `SteeringSignal`, `BudgetReservation`, `ProgressReport`, `ExecutionOutcome`, `ExecutionTrace`.

---

## 5. Required implementation work

### WP-16.00 — The execution chain and its persistence

**What must be fully done.** The full chain with distinct types and lifecycles, persisted durably at every state transition. State transitions are validated: an invalid transition is rejected rather than silently applied. Execution state survives process termination.

**Testing requirements.** A state-machine test asserting every invalid transition is rejected; a durability test killing the process at each transition point.

**Completion gate.** No invalid transition is possible, and a kill at any transition leaves recoverable state.

### WP-16.01 — Lifecycle states and reason facets

**What must be fully done.** States carry reason facets explaining *why* a task is in its state — waiting for approval, waiting for a provider, blocked on budget, paused by the user, retrying after a transient failure. A state alone is never the whole story presented to the user.

**Testing requirements.** Coverage that every state reachable in practice carries a reason facet; a presentation test asserting the reason reaches the UI.

**Completion gate.** Every observed state carries a reason facet, surfaced to the user.

### WP-16.02 — Failure classification and retry

**What must be fully done.** Failures classify into transient, permanent, refused, cancelled and unknown-effect, each with effect certainty. Retry policy derives from classification: an unknown-effect failure on a non-idempotent operation never auto-retries and instead surfaces a decision.

**Testing requirements.** A classification matrix; a negative test asserting a non-idempotent unknown-effect failure does not auto-retry.

**Completion gate.** Every failure classifies, and unknown-effect non-idempotent operations never auto-retry.

### WP-16.03 — Child tasks and ownership

**What must be fully done.** A task may spawn children with their own lifecycle, budget allocation and cancellation relationship. Cancelling a parent cancels its children; a failed child does not necessarily fail its parent. Ownership stays with the owning product across the whole tree.

**Testing requirements.** Cancellation propagation; child-failure isolation; an ownership assertion across the tree.

**Completion gate.** Cancellation propagates correctly, child failure is isolatable, and ownership is uniform across the tree.

### WP-16.04 — Checkpoints and compensation

**What must be fully done.** Checkpoints capture resumable state at declared boundaries. Compensation actions are declared per step for operations that are not naturally reversible, and run in reverse order on abort. A step with an irreversible effect and no compensation is a declaration error caught at plan validation, not at runtime.

**Testing requirements.** Resume-from-checkpoint after a kill; compensation-on-abort ordering; a plan-validation negative test for an uncompensated irreversible step.

**Completion gate.** Resume from checkpoint works after a kill, compensation runs in reverse order, and an uncompensated irreversible step fails plan validation.

### WP-16.05 — Approval, steering and budget integration

**What must be fully done.** Approval gates pause a task durably until resolved or expired. Steering signals adjust a running task without granting authority. Budget is reserved before a costed step and settled after, with unused reservation released; exhaustion is a hard stop with a clear remediation prompt.

**Testing requirements.** Approval-pause across a restart; a steering test asserting no authority escalation; reserve-settle-release accounting; a hard-stop test at zero.

**Completion gate.** Approval survives restart, steering escalates nothing, and budget never goes negative.

### WP-16.06 — Progress, outcome and trace

**What must be fully done.** Progress is a separate best-effort channel; outcome is durable fact. Four separate trace systems are maintained without conflation: execution trace, capability trace, provider interaction record and audit. A user-visible task identifier resolves to its execution trace.

**Testing requirements.** A conflation test asserting progress loss never affects outcome; a resolution test from task identifier to trace; a separation test across the four trace systems.

**Completion gate.** Losing all progress updates never affects the recorded outcome, and the four trace systems remain separate.

### WP-16.07 — Concurrency, loops and storms

**What must be fully done.** Per-workspace and per-provider concurrency limits; loop detection preventing a plan from re-entering the same step indefinitely; storm protection preventing an automation cascade. Each limit produces a typed, explained refusal rather than silent queuing forever.

**Testing requirements.** A loop-injection test; a cascade-injection test; a saturation test asserting bounded queue depth with an explained refusal.

**Completion gate.** Loops and cascades are detected and stopped with explanation, and saturation refuses rather than growing unbounded.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Durable execution state, checkpoints and traces |
| Protocol | Task, progress and approval messages become live protocol |
| UI | Task centre, progress, approval, steering and outcome surfaces |
| Security | Approval, leases and audit integration at every attempt |
| Platform | Engine behaviour is identical across desktop placements |
| Migration | Execution state schema and its recovery across versions |
| Compatibility | Task contract versioning for later cloud and mobile surfaces |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| State-machine and kill-at-transition results | `WP-16.00` |
| Reason facet coverage report | `WP-16.01` |
| Failure classification matrix and no-auto-retry proof | `WP-16.02` |
| Cancellation, isolation and ownership results | `WP-16.03` |
| Checkpoint resume and compensation ordering results | `WP-16.04` |
| Approval-across-restart, steering and budget accounting results | `WP-16.05` |
| Progress/outcome separation and trace separation results | `WP-16.06` |
| Loop, cascade and saturation results | `WP-16.07` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Invalid state transitions are impossible, and a kill at any transition leaves recoverable state.
2. Every observed state carries a reason facet that reaches the user.
3. Every failure classifies with effect certainty, and a non-idempotent unknown-effect failure never auto-retries.
4. Cancellation propagates through child tasks, child failure is isolatable, and ownership is uniform.
5. Resume from checkpoint works after a kill; compensation runs in reverse order; an uncompensated irreversible step fails plan validation.
6. Approval survives a restart, steering grants no authority, and budget never goes negative.
7. Losing every progress update never affects the recorded outcome, and the four trace systems remain separate.
8. Loops and automation cascades are detected and stopped with an explanation; saturation refuses rather than growing unbounded.

---

## 9. Dependencies

**Upstream.** `09` (capability invocation), `11` (approval, leases, audit), `14` (a proven cross-process invocation path).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `17` — ArcChat V1A | The engine its agent and automation surfaces run on |
| `26` — Remote action | The task model that spans cloud and desktop |
| `43` — Managed AI | The budget interface and provider interaction record |
| `33`, `36`–`38` | Capture, render and export as Tasks |
