<a id="rule-wp-16"></a>

# WP-16 — Unified Execution Engine

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: C — First real slice
> Upstream: `09`, `11`, `14` · Downstream: `17`

> **Goal.** Implement the **native Product Job** model — the lifecycle every long-running *product* operation shares: render, capture, index, import, export. Cloud Agent Tasks are a **different** model owned by [WP-52](52-cloud-harness.md#rule-wp-52) ([CM-04](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cm-04), [I-121](../../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). This package delivers lifecycle states, failure classification, checkpoints, compensation, approval, steering and budget — durable, resumable and identical wherever it runs.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Product-owned executors; shared mechanisms. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The **native Product Job** engine: the execution chain and its persistence; lifecycle states and reason facets; failure classification with effect certainty; child jobs; checkpoints and compensation; approval and steering integration; the budget reserve-then-settle interface; progress, outcome and trace; crash recovery; and concurrency control.

**Out of scope.** **The Cloud Agent Task and its Harness (`52`)** — a different model with a different owner ([CM-04](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cm-04)). Provider routing and real metering (`43`). Device tool delivery (`26`). Cloud automation triggers (`52`). Workflow blueprints (`41`).

> **What the two models share, and what they do not.** Product Jobs and Agent Tasks share *vocabulary* — lifecycle states, reason facets, effect certainty, checkpointing — because the same failure questions arise in both. They do **not** share an implementation, an owner, a store or a budget: a Product Job is owned by the product that runs it and consumes no AI capacity, while an Agent Task is Cloud-owned and metered ([I-121](../../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). Building one implementation for both is what would put a render under AI metering.

> **Scope amendment, 2026-09-07 ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)).** The previous goal said *an agent run, a render, a capture, an import and an automation are the same Task*. Under [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) they are **two** models: a **Cloud Agent Task** owned by the Harness, and a **native Product Job** owned by the product that runs it ([CM-04](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cm-04) of the runtime architecture). Conflating them would put a render under AI metering and Cloud recovery, and would put an agent turn under a desktop lifecycle. This package now owns the Product Job; [WP-52](52-cloud-harness.md#rule-wp-52) owns the Agent Task. They share vocabulary and failure classification deliberately — not an implementation.

**Why this package exists.** Every long-running *product* operation — a render, a capture, an index rebuild, an import, an export — has the same lifecycle needs. Building four of them produces four different recovery stories and four different approval models.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [`../../requirements/05-ai-and-agent-execution.md`](../../requirements/05-ai-and-agent-execution.md) | The full execution chain, lifecycle, ownership, checkpoints, approval and budget model |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) | The engine structure, persistence, idempotency identities and trace systems |
| [WP-04](04-identity-error-and-versioning-primitives.md#rule-wp-04) output | The four execution identities and idempotency semantics |
| [WP-09](09-capability-contribution-and-resource-model.md#rule-wp-09), [WP-11](11-security-foundation.md#rule-wp-11) output | Capability invocation and the security pipeline |
| [WP-13.00](13-high-risk-technical-probes.md#rule-wp-13.00) output | Proof that device tool execution and product-command recovery work under Native AOT; no local agent loop |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **One *Product Job* model serves every long-running product operation** — render, capture, index, import, export. A **Cloud Agent Task is a different model with a different owner** ([CM-04](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cm-04), [I-121](../../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)), owned by [WP-52](52-cloud-harness.md#rule-wp-52). They share vocabulary, never an implementation. |
| <a id="rule-br-02"></a>BR-02 | **`ProductJob ≠ JobAttempt ≠ JobCheckpoint ≠ Cloud Agent Task`.** Native job identities are product-owned; no Cloud plan/model state is persisted here. |
| BR-03 | **A retry allocates a new attempt and reuses the command identity** ([WP-04.01](04-identity-error-and-versioning-primitives.md#rule-wp-04.01)). |
| BR-04 | **Failure classification includes effect certainty**: definitely-not, definitely-did, or unknown. An unknown effect never auto-retries a non-idempotent operation. |
| BR-05 | **A task is owned by exactly one product** and its ownership never transfers. |
| BR-06 | **Approval is a discrete authorization; steering adjusts a running operation and grants nothing** ([WP-11.03](11-security-foundation.md#rule-wp-11.03)). |
| BR-07 | **Local resource permits are acquired before work and released after**, with bounded CPU/memory/disk/queue use. [D-020](../../decisions/phase-1-foundation-decisions.md#rule-d-020) monetary accounting belongs to Cloud and is absent here. |
| BR-08 | **A checkpoint is not an undo entry and not a revision** ([QI-09](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-09)). |
| BR-09 | **Compensation is explicit per step**, declared where an operation is not naturally reversible. |
| BR-10 | **Progress is an estimate; outcome is a fact.** They are separate channels and never conflated. |
| BR-11 | **A task survives a process crash** and resumes or fails explicitly — never silently disappears. |
| BR-12 | **Loop and storm protection are engine concerns**, not left to each caller. |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/BuildingBlocks/ArcForges.Execution/` | Created: the task engine, scheduler, state machine, checkpoint and compensation infrastructure |
| `src/BuildingBlocks/ArcForges.Execution.Persistence/` | Created: durable execution state and its recovery |
| `src/BuildingBlocks/ArcForges.Execution.Budget/` | Created: local CPU/memory/disk/queue permits with real measured bounds; no token or credit accounting |
| `src/BuildingBlocks/ArcForges.Execution/` | The Product Job lifecycle shared by every product. **No agent runtime here** — the Harness is Cloud ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02)) |
| `tests/ExecutionEngineTests/` | Lifecycle, idempotency, recovery, compensation, concurrency and storm-protection suites |

**Major types introduced.** `ProductJobId`, `ProductJobRecord`, `JobStep`, `JobAttempt`, `ExecutionState`, `ReasonFacet`, `FailureClass`, `EffectCertainty`, `Checkpoint`, `CompensationAction`, `ApprovalGate`, `SteeringSignal`, `ResourcePermit`, `ProgressReport`, `ExecutionOutcome`, `ExecutionTrace`.

---

## 5. Required implementation work

<a id="rule-wp-16.00"></a>

### WP-16.00 — The execution chain and its persistence

**What must be fully done.** The full chain with distinct types and lifecycles, persisted durably at every state transition. State transitions are validated: an invalid transition is rejected rather than silently applied. Execution state survives process termination.

**Testing requirements.** A state-machine test asserting every invalid transition is rejected; a durability test killing the process at each transition point.

**Completion gate.** No invalid transition is possible, and a kill at any transition leaves recoverable state.

<a id="rule-wp-16.01"></a>

### WP-16.01 — Lifecycle states and reason facets

**What must be fully done.** States carry reason facets explaining *why* a task is in its state — waiting for approval, waiting for a product resource, blocked on its resource limit, paused by the user, retrying after a transient failure. A state alone is never the whole story presented to the user.

**Testing requirements.** Coverage that every state reachable in practice carries a reason facet; a presentation test asserting the reason reaches the UI.

**Completion gate.** Every observed state carries a reason facet, surfaced to the user.

<a id="rule-wp-16.02"></a>

### WP-16.02 — Failure classification and retry

**What must be fully done.** Failures classify into transient, permanent, refused, cancelled and unknown-effect, each with effect certainty. Retry policy derives from classification: an unknown-effect failure on a non-idempotent operation never auto-retries and instead surfaces a decision.

**Testing requirements.** A classification matrix; a negative test asserting a non-idempotent unknown-effect failure does not auto-retry.

**Completion gate.** Every failure classifies, and unknown-effect non-idempotent operations never auto-retry.

<a id="rule-wp-16.03"></a>

### WP-16.03 — Child tasks and ownership

**What must be fully done.** A task may spawn children with their own lifecycle, budget allocation and cancellation relationship. Cancelling a parent cancels its children; a failed child does not necessarily fail its parent. Ownership stays with the owning product across the whole tree.

**Testing requirements.** Cancellation propagation; child-failure isolation; an ownership assertion across the tree.

**Completion gate.** Cancellation propagates correctly, child failure is isolatable, and ownership is uniform across the tree.

<a id="rule-wp-16.04"></a>

### WP-16.04 — Checkpoints and compensation

**What must be fully done.** Checkpoints capture resumable state at declared boundaries. Compensation actions are declared per step for operations that are not naturally reversible, and run in reverse order on abort. An irreversible step declares that fact, explicit confirmation and its status/recovery path; it never advertises fictional compensation.

**Testing requirements.** Resume-from-checkpoint after a kill; compensation-on-abort ordering; a validation test rejecting an undeclared irreversible effect.

**Completion gate.** Resume from checkpoint works after a kill, compensation runs in reverse order, and an undeclared irreversible effect fails validation.

<a id="rule-wp-16.05"></a>

### WP-16.05 — Approval, steering and budget integration

**What must be fully done.** Approval gates pause a task durably until resolved or expired. Steering signals adjust a running task without granting authority. Local resource permits are acquired before a bounded job step and released afterwards; resource exhaustion has a clear reason. No included-capacity, customer-credit or provider-price implementation exists here.

**Testing requirements.** Approval-pause across a restart; a steering test asserting no authority escalation; resource-permit acquisition/release; bounded queue and memory exhaustion.

**Completion gate.** Approval survives restart, steering escalates nothing, and resource permits never overcommit or leak.

<a id="rule-wp-16.06"></a>

### WP-16.06 — Progress, outcome and trace

**Required design implementation and verification.** Artifact publication requires the verified payload and origin carrier together. Test staging failure, cancellation and marking retry with one original product job/output, no new provider attempt or delivered receipt; preserve ordinary ProductJob versus Cloud AgentTask ownership.

**What must be fully done.** Progress is a separate best-effort channel; outcome is durable fact. Four separate trace systems are maintained without conflation: execution trace, capability trace, and audit; provider interaction records belong only to Cloud. A user-visible task identifier resolves to its execution trace.

**Testing requirements.** A conflation test asserting progress loss never affects outcome; a resolution test from task identifier to trace; a separation test across the declared trace systems.

**Completion gate.** Losing all progress updates never affects the recorded outcome, and the declared trace systems remain separate.

<a id="rule-wp-16.07"></a>

### WP-16.07 — Concurrency, loops and storms

**What must be fully done.** Per-product and per-device/resource concurrency limits; loop detection preventing a plan from re-entering the same step indefinitely; storm protection preventing an automation cascade. Each limit produces a typed, explained refusal rather than silent queuing forever.

**Testing requirements.** A loop-injection test; a cascade-injection test; a saturation test asserting bounded queue depth with an explained refusal.

**Completion gate.** Loops and cascades are detected and stopped with explanation, and saturation refuses rather than growing unbounded.

---

<a id="rule-wp-16.90"></a>
### WP-16.90 — Verify the owned artifact and real integration

**What must be fully done.** Preserve the repaired ProductJob-only responsibility. Update shared execution vocabulary/package references, dispatch/error profiles and cancellation. Cloud AI Task/Run execution belongs to [WP-52](52-cloud-harness.md#rule-wp-52), not a new reusable desktop agent engine.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Product-job lifecycle/compensation/unknown-effect tests remain; architecture evidence shows no local model loop or Cloud budget/Task ownership in the shared engine.

**Completion gate.** Product-job lifecycle/compensation/unknown-effect tests remain; architecture evidence shows no local model loop or Cloud budget/Task ownership in the shared engine. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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

**Required evidence addition.** [WP-16.06](#rule-wp-16.06) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| State-machine and kill-at-transition results | [WP-16.00](#rule-wp-16.00) |
| Reason facet coverage report | [WP-16.01](#rule-wp-16.01) |
| Failure classification matrix and no-auto-retry proof | [WP-16.02](#rule-wp-16.02) |
| Cancellation, isolation and ownership results | [WP-16.03](#rule-wp-16.03) |
| Checkpoint resume and compensation ordering results | [WP-16.04](#rule-wp-16.04) |
| Approval-across-restart, steering and budget accounting results | [WP-16.05](#rule-wp-16.05) |
| Progress/outcome separation and trace separation results | [WP-16.06](#rule-wp-16.06) |
| Loop, cascade and saturation results | [WP-16.07](#rule-wp-16.07) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-16.90](#rule-wp-16.90) and all inherited domain-specific gates must pass on the same candidate closure. Product-job lifecycle/compensation/unknown-effect tests remain; architecture evidence shows no local model loop or Cloud budget/Task ownership in the shared engine.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. Invalid state transitions are impossible, and a kill at any transition leaves recoverable state.
2. Every observed state carries a reason facet that reaches the user.
3. Every failure classifies with effect certainty, and a non-idempotent unknown-effect failure never auto-retries.
4. Cancellation propagates through child tasks, child failure is isolatable, and ownership is uniform.
5. Resume from checkpoint works after a kill; compensation runs in reverse order; an undeclared irreversible effect fails validation.
6. Approval survives a restart, steering grants no authority, and resource permits never overcommit or leak.
7. Losing every progress update never affects the recorded outcome, and the declared trace systems remain separate.
8. Loops and automation cascades are detected and stopped with an explanation; saturation refuses rather than growing unbounded.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-09](09-capability-contribution-and-resource-model.md#rule-wp-09)
- [WP-11](11-security-foundation.md#rule-wp-11)
- [WP-14](14-hub-and-minimal-provider-slice.md#rule-wp-14)

**Downstream — consumers of these released outputs.**

- [WP-17](17-arcchat-independent-core.md#rule-wp-17)


---
