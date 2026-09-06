# WP-17 — ArcChat Independent Core V1A

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: C — First real slice
> Upstream: `06`, `15`, `16` · Downstream: `20`, `26`, `41`, `52`

> **Goal.** Complete ArcChat as an independent product: chat, agent, task centre, capability hub, permission and approval, automation, local data and recovery — with **no claim** that its ecosystem tier is finished (`I2 §III.4`).

---

## 1. Scope and purpose

**In scope.** The ArcChat capability registry surface; permission, approval and audit surfaces; the task centre; basic automation creation, start and stop; the **Cloud AI client and local tool executor**; thin preview and rich handoff; and application state, start-up and recovery.

> **Scope amendment, 2026-09-06 (P2-006).** The Harness is Cloud-only (`LS-02`). ArcChat Desktop presents task state, executes authorised `ToolRequest`s and runs product-local jobs. It holds **no provider credential, no model loop and no planner**.

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
| BR-06 | **No provider credential exists on the client** (`BY-01`–`BY-04`, `I-015` retired). Provider credentials are deployment secrets held only by the Cloud host (`DC-15`). |
| BR-07 | **Thin preview versus rich handoff**: ArcChat shows enough to act, and hands off to the owning product for real work (`§16` of the shared desktop requirements). |
| BR-08 | **Automation in V1 stays simple** — creation, start, stop, and a bounded trigger set (`I4 §Stage 19 §62`). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcChat/ArcChat.Agent/` | **Presentation-side agent surfaces only** — turn submission, streaming display, steering controls. The turn loop, batching, planning, selection and compaction are **Cloud** (`ArcForges.Cloud.AgentRuntime`, `LS-02`) |
| `src/ArcChat/ArcChat.Application/` | Task centre, automation, permission and approval services |
| `src/ArcChat/ArcChat.LocalTools/` | First-party local capabilities ArcChat itself owns |
| `src/ArcChat/ArcChat.Presentation/`, `.Desktop/` | Task centre, capability hub, security centre, automation and handoff surfaces |
| `src/ArcChat/ArcChat.CloudClient/` | The Cloud AI client: submit a turn, read task state, surface admission reasons. **No provider adapter, no credential** |
| `tests/ArcChat.Tests.Integration/` | Agent, automation, approval, recovery and handoff suites |

**Major types introduced.** `CapabilityHub`, `AgentSessionView`, `TaskCentreView`, `AutomationDefinition`, `AutomationTrigger`, `AutomationRun`, `ToolRequestExecutor`, `AdmissionReasonView`, `PermissionGrantView`, `SecurityCentre`, `HandoffRequest`, `PreviewDescriptor`, `CloudAiClient`.

**Types that moved to Cloud under P2-006.** `TurnLoop`, `ToolCallBatch`, `ConflictSet`, `CompactionRecord`, `PlanBuilder` and `ProviderAdapter` belong to `ArcForges.Cloud.AgentRuntime` and `ArcForges.Cloud.Modules.AI`, not to any desktop project.

---

## 5. Required implementation work

### WP-17.00 — Capability hub surface

**What must be fully done.** A surface listing every registered contribution across every connected app with its risk level, trust level, permission state and health. Unavailable capabilities show their reason. A capability from an unknown or unverified source is visibly distinguished.

**Testing requirements.** Enumeration with providers present, absent and degraded; a reason-coverage test.

**Completion gate.** Every registered capability is visible with risk, trust, permission and health, and every unavailability shows a reason.

### WP-17.01 — Cloud AI client and device tool executor

**What must be fully done — with real code, here.** The desktop's Cloud AI client: submit a turn, subscribe or poll for task and step state, read streamed output through `task.readStream`, and surface admission outcomes precisely. The **device tool executor**: pull an authorised `ToolRequest`, re-authorise locally, resolve the `CapabilityKey` through the generated allowlist, decode into a typed product request (`§3.1` of the local RPC contract), invoke it, and return an idempotent result. Both are **production code, not scaffolding**.

**What is fixture-backed here, and explicitly temporary.** The Cloud side of the turn is a **fixture turn endpoint** on the `WP-06.04` host: it accepts a turn, returns scripted task and step transitions, emits scripted stream chunks, and issues scripted `ToolRequest`s. It runs **no model, no planner, no admission and no metering**. Its purpose is to exercise the client and the device path against real transport and real persistence before the Harness exists.

> **The fixture endpoint is deleted by `WP-52`, not adapted.** It is registered in the temporary-scaffolding list of `§3` of the implementation sequence, and `WP-52.05`'s gate asserts it is gone.

**Testing requirements.** A turn submitted to the fixture endpoint on the **real** `WP-06.04` host over **real** transport, asserting the client renders every scripted state transition and stream chunk correctly; a device `ToolRequest` executed end to end through decode, typed invocation and idempotent result, with a duplicate delivery producing one effect; admission-refusal rendering for each of `no_service_term`, `capacity_exhausted` with `recoveryAt`, and `extra_credits_required`; **a structural test asserting no desktop assembly contains a turn loop, a planner or a provider adapter** (`HV-09`).

**Completion gate.** The Cloud AI client and the device tool executor are complete against real transport and real persistence; **no client-side model loop is reachable**; and the fixture endpoint is **labelled temporary with its removing package named**. **Real multi-step plan execution is `WP-52`'s gate, not this one** — claiming it here would require the Harness that `WP-52` builds.

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

### WP-17.05 — Cloud AI client and admission surfacing

**What must be fully done.** The desktop's Cloud AI client: submit a turn, poll or subscribe to task state, and **surface admission outcomes precisely** — which of an active paid service term, included capacity, or extra-credit authorisation is missing, with the server-calculated recovery time where one applies. **No provider adapter, model endpoint or credential exists on the client** (`BY-01`–`BY-04`, `EC-05`). The managed provider path itself is `43`'s responsibility and is visibly stubbed here.

**Testing requirements.** A structural test asserting no desktop assembly references a provider adapter or holds a credential; a refusal test covering `entitlement.no_service_term`, `capacity_exhausted` with `recoveryAt`, and `extra_credits_required`, each surfacing the correct action; a stub-marking check asserting the managed path is not presented as complete.

**Completion gate.** **No provider credential exists on the client**, and every admission refusal states its specific reason and action rather than a generic failure.

### WP-17.06 — Preview, handoff and application state

**What must be fully done.** Thin preview of another product's resource with rich handoff to the owning product, carrying context. Application state, window restoration, start-up within budget and recovery after a hard kill.

**Testing requirements.** Handoff with the target running and not running; startup budget measurement; kill-and-recover test.

**Completion gate.** Handoff works whether or not the target is running, startup meets budget, and recovery is clean.

### WP-17.07 — V1B boundary declaration

**What must be fully done.** The ecosystem capabilities not yet delivered are enumerated in-product and in documentation as progressive, each mapped to the package that closes it: federated search, product context providers, real semantic modification, cross-application workflows and real artifact handlers.

**Testing requirements.** A completeness check that every V1B item names its closing package.

**Completion gate.** Every V1B item is enumerated with a named closing package, and nothing incomplete is presented as complete.

> **`WP-17.08` and `WP-17.09` are relocated to [`52-cloud-harness.md`](52-cloud-harness.md).** The turn loop, batching, bounds and history compaction are Cloud work (`LS-02`), and Phase C predates the Cloud host by two phases. Their identifiers are retired here and not reused.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Automation definitions, grants, task state, provider configuration and the `CompactionRecord` derived store |
| Protocol | ArcChat's own capabilities and the handoff contract |
| UI | Task centre, capability hub, security centre, automation and preview surfaces |
| Security | Permission and approval become user-visible and user-controllable |
| Platform | **No local model support exists** (`C-02`). Cloud availability and AI admission are surfaced honestly and separately |
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
2. The Cloud AI client and the device tool executor work against **real transport and real persistence**, and **no desktop assembly contains a turn loop, a planner or a provider adapter** (`LS-02`, `HV-09`). **Multi-step plan execution is verified in `WP-52`**, where the Harness exists; claiming it here would require the thing `WP-52` builds.
3. Permission is visible and revocable, revocation takes effect mid-operation, and approvals survive a restart.
4. Tasks from more than one product appear in one task centre with correct controls and ownership attribution.
5. Automations start, stop and record runs; cascades are detected and stopped; no implicit permission is acquired.
6. **No provider credential exists on the client**, and an admission refusal states which of service term, capacity or extra-credit authorisation is missing.
7. Handoff works with the target both running and not running; startup meets budget; recovery is clean.
8. **Every V1B ecosystem item is enumerated with a named closing package**, and nothing incomplete is presented as complete.
9. *(Moved to `WP-52` — the Cloud Harness. The turn loop, batching and bounds run in the Cloud host and admit through Commerce, so they cannot be built in Phase C.)*
10. *(Moved to `WP-52` — the Cloud Harness. Compaction is a Cloud concern for the same reason.)*

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
