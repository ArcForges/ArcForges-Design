# WP-17 — ArcChat Independent Core V1A

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: C — First real slice
> Upstream: `15`, `16` · Downstream: `20`, `26`, `41`

> **Goal.** Complete ArcChat as an independent product: chat, agent, task centre, capability hub, permission and approval, automation, local data and recovery — with **no claim** that its ecosystem tier is finished (`I2 §III.4`).

---

## 1. Scope and purpose

**In scope.** The ArcChat capability registry surface; permission, approval and audit surfaces; the task centre; basic automation creation, start and stop; local BYOK and provider adapter wiring; thin preview and rich handoff; and application state, start-up and recovery.

**Out of scope.** Federated search across products, product context providers, real semantic modifications, cross-application workflows and real artifact handlers — these are **V1B**, delivered progressively as the professional products come online (`20`, `35`, `39`).

**Why this package exists.** `I2 §III.4` is explicit that ArcChat splits into V1A — independent chat, agent, task and hub complete — and V1B, closed progressively. Claiming ecosystem completeness now would make every later product integration a retrofit against a false baseline.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| `I2 §III.4` | The V1A/V1B split and its explicit contents |
| [`../../requirements/products/arcchat.md`](../../requirements/products/arcchat.md) | The product model, capability hub role and V1 scope |
| [`../../requirements/07-security-privacy-and-trust.md`](../../requirements/07-security-privacy-and-trust.md) | Permission, approval, audit and the security centre |
| `WP-15`, `WP-16` output | The conversation domain and the execution engine |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **ArcChat is a control plane, never a mandatory data gateway** (**D-010**). |
| BR-02 | **V1B is not claimed complete.** The ecosystem tier is explicitly marked as progressive, with each closure attached to a named later package. |
| BR-03 | **An agent is not a superuser** (`I3 §8.4`). It holds exactly the capabilities granted to it, subject to the same pipeline as a human actor. |
| BR-04 | **Every capability invocation passes the security pipeline** and is recorded in the audit and execution traces. |
| BR-05 | **Automation is not a workflow** and **a workflow is not an agent runtime** (`I4 §Stage 24 §17`, `§20`). Automation decides *when*; a plan decides *how*. |
| BR-06 | **A local BYOK secret never leaves the device** and never reaches a mobile or cloud surface (`AI-03` in the companion requirements). |
| BR-07 | **Thin preview versus rich handoff**: ArcChat shows enough to act, and hands off to the owning product for real work (`§16` of the shared desktop requirements). |
| BR-08 | **Automation in V1 stays simple** — creation, start, stop, and a bounded trigger set (`I4 §Stage 19 §62`). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcChat/ArcChat.Agent/` | The agent runtime, plan construction, capability selection and steering |
| `src/ArcChat/ArcChat.Application/` | Task centre, automation, permission and approval services |
| `src/ArcChat/ArcChat.LocalTools/` | First-party local capabilities ArcChat itself owns |
| `src/ArcChat/ArcChat.Presentation/`, `.Desktop/` | Task centre, capability hub, security centre, automation and handoff surfaces |
| `src/ArcChat/ArcChat.Infrastructure/` | Provider adapters with a local BYOK secret path through the broker |
| `tests/ArcChat.Tests.Integration/` | Agent, automation, approval, recovery and handoff suites |

**Major types introduced.** `CapabilityHub`, `AgentSession`, `PlanBuilder`, `TaskCentreView`, `AutomationDefinition`, `AutomationTrigger`, `AutomationRun`, `PermissionGrantView`, `SecurityCentre`, `HandoffRequest`, `PreviewDescriptor`, `ProviderAdapter`.

---

## 5. Required implementation work

### WP-17.00 — Capability hub surface

**What must be fully done.** A surface listing every registered contribution across every connected app with its risk level, trust level, permission state and health. Unavailable capabilities show their reason. A capability from an unknown or unverified source is visibly distinguished.

**Testing requirements.** Enumeration with providers present, absent and degraded; a reason-coverage test.

**Completion gate.** Every registered capability is visible with risk, trust, permission and health, and every unavailability shows a reason.

### WP-17.01 — Agent runtime over the engine

**What must be fully done.** The agent constructs plans over the execution engine, selects capabilities through the registry, and executes attempts through the security pipeline. Static registration is used; no reflection path exists. A plan is validated before execution, including the compensation declaration check.

**Testing requirements.** A published-AOT agent run; a plan-validation negative test; a capability-selection explainability test.

**Completion gate.** Multi-step plans execute inside a published AOT binary with explainable capability selection.

### WP-17.02 — Permission, approval and the security centre

**What must be fully done.** Permission grants are visible and revocable per capability, per app and per agent. Approvals appear as durable attention items. The security centre shows recent security-relevant events from the audit store, active leases, and connected devices where applicable.

**Testing requirements.** Grant, revoke and revoke-mid-operation tests; approval durability across restart; an audit-visibility test.

**Completion gate.** Permission is visible and revocable, revocation takes effect mid-operation, and approvals survive restart.

### WP-17.03 — Task centre

**What must be fully done.** All tasks across all products in one surface with state, reason facet, progress, budget consumption and outcome. Pause, resume, cancel and retry are available where the task's state permits. A task owned by another product is shown with its owner and handed off rather than manipulated directly beyond the permitted control set.

**Testing requirements.** Cross-product task visibility with a real second provider; control-availability tests per state; a handoff test.

**Completion gate.** Tasks from more than one product appear in one surface with correct controls and correct ownership attribution.

### WP-17.04 — Automation V1

**What must be fully done.** Automation definitions with a bounded trigger set, explicit start and stop, visible run history, and engine-level loop and storm protection. An automation never gains permission implicitly; it runs under an explicit grant.

**Testing requirements.** Trigger firing, stop-while-running, cascade injection, and a permission test asserting no implicit grant.

**Completion gate.** Automations start, stop and record runs; cascades are stopped; no implicit permission is acquired.

### WP-17.05 — Provider adapters and local BYOK

**What must be fully done.** Provider adapters behind one interface, with a local BYOK secret stored through the secret broker and used without being revealed. A local model path is supported where the platform allows. Managed provider economics are stubbed and explicitly marked as `43`'s responsibility.

**Testing requirements.** A use-without-reveal test; an adapter-substitution test; a stub-marking check asserting the managed path is not presented as complete.

**Completion gate.** A local BYOK secret is used without being revealed, and the managed path is visibly stubbed rather than falsely complete.

### WP-17.06 — Preview, handoff and application state

**What must be fully done.** Thin preview of another product's resource with rich handoff to the owning product, carrying context. Application state, window restoration, start-up within budget and recovery after a hard kill.

**Testing requirements.** Handoff with the target running and not running; startup budget measurement; kill-and-recover test.

**Completion gate.** Handoff works whether or not the target is running, startup meets budget, and recovery is clean.

### WP-17.07 — V1B boundary declaration

**What must be fully done.** The ecosystem capabilities not yet delivered are enumerated in-product and in documentation as progressive, each mapped to the package that closes it: federated search, product context providers, real semantic modification, cross-application workflows and real artifact handlers.

**Testing requirements.** A completeness check that every V1B item names its closing package.

**Completion gate.** Every V1B item is enumerated with a named closing package, and nothing incomplete is presented as complete.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Automation definitions, grants, task state and provider configuration |
| Protocol | ArcChat's own capabilities and the handoff contract |
| UI | Task centre, capability hub, security centre, automation and preview surfaces |
| Security | Permission and approval become user-visible and user-controllable |
| Platform | Local model support varies per platform and is surfaced honestly |
| Migration | Automation and grant schema versions |
| Compatibility | The handoff and preview contracts other products implement |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Capability enumeration and reason-coverage results | `WP-17.00` |
| Published-AOT agent run and plan-validation results | `WP-17.01` |
| Grant, revocation and approval durability results | `WP-17.02` |
| Cross-product task centre results | `WP-17.03` |
| Automation trigger, cascade and permission results | `WP-17.04` |
| Use-without-reveal and adapter-substitution results | `WP-17.05` |
| Handoff, startup budget and recovery results | `WP-17.06` |
| V1B enumeration completeness check | `WP-17.07` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Every registered capability is visible with risk, trust, permission and health, and unavailability always shows a reason.
2. Multi-step agent plans execute inside a published AOT binary with explainable capability selection and validated plans.
3. Permission is visible and revocable, revocation takes effect mid-operation, and approvals survive a restart.
4. Tasks from more than one product appear in one task centre with correct controls and ownership attribution.
5. Automations start, stop and record runs; cascades are detected and stopped; no implicit permission is acquired.
6. A local BYOK secret is used without being revealed; the managed provider path is visibly stubbed.
7. Handoff works with the target both running and not running; startup meets budget; recovery is clean.
8. **Every V1B ecosystem item is enumerated with a named closing package**, and nothing incomplete is presented as complete.

---

## 9. Dependencies

**Upstream.** `15` (conversation domain), `16` (execution engine).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `20` — First workflow | The agent, task centre and artifact surfaces |
| `26` — Remote action | ArcChat Desktop as the durable tool-request consumer |
| `41` — Extension platform | The capability hub and permission surfaces extensions plug into |
| `31` — Mobile | The task, approval and steering semantics the companion mirrors |
