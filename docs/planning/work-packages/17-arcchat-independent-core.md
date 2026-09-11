<a id="rule-wp-17"></a>

# WP-17 — ArcChat Independent Core V1A

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: C — First real slice
> Upstream: `06`, `15`, `16` · Downstream: `20`, `26`, `41`, `52`

> **Goal.** Complete ArcChat as an independent product: chat, agent, task centre, capability hub, permission and approval, automation, local data and recovery — with **no claim** that its ecosystem tier is finished.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcChat; Contracts fixtures. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Fixture AI is permitted only for the named local product slice; WP52 replaces it with real CF execution before Mobile/Web/full release.

---

## 1. Scope and purpose

**In scope.** The ArcChat capability registry surface; permission, approval and audit surfaces; the task centre; basic automation creation, start and stop; the **Cloud AI client and local tool executor**; thin preview and rich handoff; and application state, start-up and recovery.

> **Scope amendment, 2026-09-06 ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)).** The Harness is Cloud-only ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02)). ArcChat Desktop presents task state, executes authorised `ToolRequest`s and runs product-local jobs. It holds **no provider credential, no model loop and no planner**.

**Out of scope.** Federated search across products, product context providers, real semantic modifications, cross-application workflows and real artifact handlers — these are **V1B**, delivered progressively as the professional products come online (`20`, `35`, `39`).

**Why this package exists.** The [ArcChat requirements](../../requirements/products/arcchat.md) are delivered through an independent client foundation and progressive ecosystem integration. At this package, Cloud and model behavior use the explicitly named fixtures; the real agent loop is delivered by [WP-52](52-cloud-harness.md#rule-wp-52). Claiming ecosystem completeness now would make every later product integration a retrofit against a false baseline.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [ArcChat product requirements](../../requirements/products/arcchat.md) | The independent client scope; this package defines the fixture boundary and its progressive ecosystem closure in §5 |
| [`../../requirements/products/arcchat.md`](../../requirements/products/arcchat.md) | The product model, capability hub role and V1 scope |
| [`../../requirements/07-security-privacy-and-trust.md`](../../requirements/07-security-privacy-and-trust.md) | Permission, approval, audit and the security centre |
| [WP-15](15-arcchat-conversation-core.md#rule-wp-15), [WP-16](16-unified-execution-engine.md#rule-wp-16) output | The conversation domain and the execution engine |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **ArcChat is a control plane, never a mandatory data gateway** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |
| BR-02 | **V1B is not claimed complete.** The ecosystem tier is explicitly marked as progressive, with each closure attached to a named later package. |
| BR-03 | **An agent is not a superuser**. It holds exactly the capabilities granted to it, subject to the same pipeline as a human actor. |
| BR-04 | **Every capability invocation passes the security pipeline** and is recorded in the audit and execution traces. |
| <a id="rule-br-05"></a>BR-05 | **Automation is not a workflow** and **a workflow is not an agent runtime**. Automation decides *when*; a plan decides *how*. |
| BR-06 | **No provider credential exists on the client** ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [I-015](../../requirements/01-normative-glossary-and-invariants.md#rule-i-015) retired). Provider credentials are deployment secrets held only by the Cloud host ([DC-15](../../requirements/11-policy-and-configuration.md#rule-dc-15)). |
| BR-07 | **Thin preview versus rich handoff**: ArcChat shows enough to act, and hands off to the owning product for real work (`§16` of the shared desktop requirements). |
| BR-08 | **Automation in V1 stays simple** — creation, start, stop, and a bounded trigger set. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcChat/ArcChat.Agent/` | **Presentation-side agent surfaces only** — turn submission, streaming display, steering controls. The turn loop, batching, planning, selection and compaction are **Cloud** (`ArcForges-AI/src/workflows/RunWorkflow`, [LS-02](../../architecture/17-agent-harness.md#rule-ls-02)) |
| `src/ArcChat/ArcChat.Application/` | Task centre, automation, permission and approval services |
| `src/ArcChat/ArcChat.LocalTools/` | First-party local capabilities ArcChat itself owns |
| `src/ArcChat/ArcChat.Presentation/`, `.Desktop/` | Task centre, capability hub, security centre, automation and handoff surfaces |
| `src/ArcChat/ArcChat.CloudClient/` | The Cloud AI client: submit a turn, read task state, surface admission reasons. **No provider adapter, no credential** |
| `tests/ArcChat.Tests.Integration/` | Agent, automation, approval, recovery and handoff suites |

**Major types introduced.** `CapabilityHub`, `AgentSessionView`, `TaskCentreView`, `AutomationDefinition`, `AutomationTrigger`, `AutomationRun`, `ToolRequestExecutor`, `AdmissionReasonView`, `PermissionGrantView`, `SecurityCentre`, `HandoffRequest`, `PreviewDescriptor`, `CloudAiClient`.

**Types that moved to Cloud under P2-006.** `TurnLoop`, `ToolCallBatch`, `ConflictSet`, `CompactionRecord`, `PlanBuilder` and `ProviderAdapter` belong to `ArcForges-AI/src/workflows/RunWorkflow` ; C# Agent/Task modules hold canonical business records, not to any desktop project.

---

## 5. Required implementation work

<a id="rule-wp-17.00"></a>

### WP-17.00 — Capability hub surface

**What must be fully done.** A surface listing every registered contribution across every connected app with its risk level, trust level, permission state and health. Unavailable capabilities show their reason. A capability from an unknown or unverified source is visibly distinguished.

**Testing requirements.** Enumeration with providers present, absent and degraded; a reason-coverage test.

**Completion gate.** Every registered capability is visible with risk, trust, permission and health, and every unavailability shows a reason.

<a id="rule-wp-17.01"></a>

### WP-17.01 — Cloud AI client and device tool executor

**What must be fully done — with real code, here.** The desktop's Cloud AI client: submit a turn, subscribe or poll for task and step state, read streamed output through `task.readStream`, and surface admission outcomes precisely. The **device tool executor**: pull an authorised `ToolRequest`, re-authorise locally, resolve the `CapabilityKey` through the generated allowlist, decode into a typed product request (`§3.1` of the local RPC contract), invoke it, and return an idempotent result. Both are **production code, not scaffolding**.

**What is fixture-backed here, and explicitly temporary.** The Cloud side of the turn is a **fixture turn endpoint** on the [WP-06.04](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04) host: it accepts a turn, returns scripted task and step transitions, emits scripted stream chunks, and issues scripted `ToolRequest`s. It runs **no model, no planner, no admission and no metering**. Its purpose is to exercise the client and the device path against real transport and real persistence before the Harness exists.

> **The fixture endpoint is deleted by [WP-52](52-cloud-harness.md#rule-wp-52), not adapted.** It is registered in the temporary-scaffolding list of `§3` of the implementation sequence, and [WP-52.05](52-cloud-harness.md#rule-wp-52.05)'s gate asserts it is gone.

**Testing requirements.** A turn submitted to the fixture endpoint on the **real** [WP-06.04](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04) host over **real** transport, asserting the client renders every scripted state transition and stream chunk correctly; a device `ToolRequest` executed end to end through decode, typed invocation and idempotent result, with a duplicate delivery producing one effect; admission-refusal rendering for each of `no_service_term`, `capacity_exhausted` with `recoveryAt`, and `extra_credits_required`; **a structural test asserting no desktop assembly contains a turn loop, a planner or a provider adapter** ([HV-09](../../architecture/17-agent-harness.md#rule-hv-09)).

**Completion gate.** The Cloud AI client and the device tool executor are complete against real transport and real persistence; **no client-side model loop is reachable**; and the fixture endpoint is **labelled temporary with its removing package named**. **Real multi-step plan execution is [WP-52](52-cloud-harness.md#rule-wp-52)'s gate, not this one** — claiming it here would require the Harness that [WP-52](52-cloud-harness.md#rule-wp-52) builds.

<a id="rule-wp-17.02"></a>

### WP-17.02 — Permission, approval and the security centre

**What must be fully done.** Permission grants are visible and revocable per capability, per app and per agent. Approvals appear as durable attention items. The security centre shows recent security-relevant events from the audit store, active leases, and connected devices where applicable.

**Testing requirements.** Grant, revoke and revoke-mid-operation tests; approval durability across restart; an audit-visibility test.

**Completion gate.** Permission is visible and revocable, revocation takes effect mid-operation, and approvals survive restart.

<a id="rule-wp-17.03"></a>

### WP-17.03 — Task centre

**What must be fully done.** All tasks across all products in one surface with state, reason facet, progress, budget consumption and outcome. Pause, resume, cancel and retry are available where the task's state permits. A task owned by another product is shown with its owner and handed off rather than manipulated directly beyond the permitted control set.

**Testing requirements.** Cross-product task visibility with a real second provider; control-availability tests per state; a handoff test.

**Completion gate.** Tasks from more than one product appear in one surface with correct controls and correct ownership attribution.

<a id="rule-wp-17.04"></a>

### WP-17.04 — Cloud automation client

**What must be fully done.** Implement automation definition/start/stop/history UI and generated Cloud-client calls. Use the registered [WP-17.01](#rule-wp-17.01) fixture endpoint for pre-Cloud state transitions. No desktop trigger scheduler, durable AutomationRun authority or model loop is introduced. Real triggers, deduplication, budget authorisation and execution are WP-52.06.

**Testing requirements.** Exercise definition/enable/disable commands, visible pending and denied states, and idempotent request retry against the test-only endpoint; assert no desktop scheduler/provider dependencies.

**Completion gate.** The client can manage and display the declared automation contract. Trigger execution and cascade protection remain specifically owned by [WP-52.06](52-cloud-harness.md#rule-wp-52.06), without a desktop substitute.

<a id="rule-wp-17.05"></a>

### WP-17.05 — Cloud AI client and admission surfacing

**What must be fully done.** The desktop's Cloud AI client: submit a turn, poll or subscribe to task state, and **surface admission outcomes precisely** — which of an active paid service term, included capacity, or extra-credit authorisation is missing, with the server-calculated recovery time where one applies. **No provider adapter, model endpoint or credential exists on the client** ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [EC-05](../../architecture/contracts/01-public-api-operations.md#rule-ec-05)). The managed provider path itself is `43`'s responsibility and is visibly stubbed here.

**Testing requirements.** A structural test asserting no desktop assembly references a provider adapter or holds a credential; a refusal test covering `entitlement.no_service_term`, `capacity_exhausted` with `recoveryAt`, and `extra_credits_required`, each surfacing the correct action; a stub-marking check asserting the managed path is not presented as complete.

**Completion gate.** **No provider credential exists on the client**, and every admission refusal states its specific reason and action rather than a generic failure.

<a id="rule-wp-17.06"></a>

### WP-17.06 — Preview, handoff and application state

**What must be fully done.** Thin preview of another product's resource with rich handoff to the owning product, carrying context. Application state, window restoration, start-up within budget and recovery after a hard kill.

**Testing requirements.** Handoff with the target running and not running; startup budget measurement; kill-and-recover test.

**Completion gate.** Handoff works whether or not the target is running, startup meets budget, and recovery is clean.

<a id="rule-wp-17.07"></a>

### WP-17.07 — V1B boundary declaration

**What must be fully done.** The ecosystem capabilities not yet delivered are enumerated in-product and in documentation as progressive, each mapped to the package that closes it: federated search, product context providers, real semantic modification, cross-application workflows and real artifact handlers.

**Testing requirements.** A completeness check that every V1B item names its closing package.

**Completion gate.** Every V1B item is enumerated with a named closing package, and nothing incomplete is presented as complete.

<a id="rule-wp-17.08"></a>
<a id="rule-wp-17.09"></a>

> **[WP-17.08](#rule-wp-17.08) and [WP-17.09](#rule-wp-17.09) are relocated to [`52-cloud-harness.md`](52-cloud-harness.md).** The turn loop, batching, bounds and history compaction are Cloud work ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02)), and Phase C predates the Cloud host by two phases. Their identifiers are retired here and not reused.

---

<a id="rule-wp-17.90"></a>
### WP-17.90 — Verify the owned artifact and real integration

**What must be fully done.** Build the independent desktop client/local executor and bounded AI fixtures. Specify the exact fixture contracts and replacement obligation at [WP-52](52-cloud-harness.md#rule-wp-52); schedules are clients of the Cloud-owned occurrence/admission contract.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Independent ArcChat behavior is real; model/Harness behavior is labelled fixture-only here and cannot close the final AI workflow gate.

**Completion gate.** Independent ArcChat behavior is real; model/Harness behavior is labelled fixture-only here and cannot close the final AI workflow gate. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Local grants, pending client requests and read projections. Automation authority, provider configuration and CompactionRecord live in Cloud and are delivered in [WP-52](52-cloud-harness.md#rule-wp-52)/[WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44) |
| Protocol | ArcChat's own capabilities and the handoff contract |
| UI | Task centre, capability hub, security centre, automation and preview surfaces |
| Security | Permission and approval become user-visible and user-controllable |
| Platform | **No local model support exists** ([C-02](../../requirements/00-product-scope-and-portfolio.md#rule-c-02)). Cloud availability and AI admission are surfaced honestly and separately |
| Migration | Automation and grant schema versions |
| Compatibility | The handoff and preview contracts other products implement |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Capability enumeration and reason-coverage results | [WP-17.00](#rule-wp-17.00) |
| Fixture-turn client results against the real [WP-06.04](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04) host, device `ToolRequest` decode-invoke-idempotency results, admission-refusal rendering per reason, and the structural no-turn-loop assertion | [WP-17.01](#rule-wp-17.01) |
| Grant, revocation and approval durability results | [WP-17.02](#rule-wp-17.02) |
| Cross-product task centre results | [WP-17.03](#rule-wp-17.03) |
| Automation client command/state/permission results; real trigger evidence is [WP-52.06](52-cloud-harness.md#rule-wp-52.06) | [WP-17.04](#rule-wp-17.04) |
| Cloud admission reason rendering and no-client-provider-credential results | [WP-17.05](#rule-wp-17.05) |
| Handoff, startup budget and recovery results | [WP-17.06](#rule-wp-17.06) |
| V1B enumeration completeness check | [WP-17.07](#rule-wp-17.07) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-17.90](#rule-wp-17.90) and all inherited domain-specific gates must pass on the same candidate closure. Independent ArcChat behavior is real; model/Harness behavior is labelled fixture-only here and cannot close the final AI workflow gate.

**Offline evidence.** Execute this product's applicable [initial-state matrix](../../assurance/testing-and-verification-strategy.md#offline-acceptance-matrix) rows, including fresh shell, hydrated outage, unavailable content, signout and restart where applicable. Record permitted local work and explicitly unavailable Cloud actions.

**All of the following, with recorded evidence:**

1. Every registered capability is visible with risk, trust, permission and health, and unavailability always shows a reason.
2. The Cloud AI client and the device tool executor work against **real transport and real persistence**, and **no desktop assembly contains a turn loop, a planner or a provider adapter** ([LS-02](../../architecture/17-agent-harness.md#rule-ls-02), [HV-09](../../architecture/17-agent-harness.md#rule-hv-09)). **Multi-step plan execution is verified in [WP-52](52-cloud-harness.md#rule-wp-52)**, where the Harness exists; claiming it here would require the thing [WP-52](52-cloud-harness.md#rule-wp-52) builds.
3. Permission is visible and revocable, revocation takes effect mid-operation, and approvals survive a restart.
4. Tasks from more than one product appear in one task centre with correct controls and ownership attribution.
5. Automations start, stop and record runs; cascades are detected and stopped; no implicit permission is acquired.
6. **No provider credential exists on the client**, and an admission refusal states which of service term, capacity or extra-credit authorisation is missing.
7. Handoff works with the target both running and not running; startup meets budget; recovery is clean.
8. **Every V1B ecosystem item is enumerated with a named closing package**, and nothing incomplete is presented as complete.
9. *(Moved to [WP-52](52-cloud-harness.md#rule-wp-52) — the Cloud Harness. The turn loop, batching and bounds run in CF Workflow and admit through C# Commerce, so they cannot be built in Phase C.)*
10. *(Moved to [WP-52](52-cloud-harness.md#rule-wp-52) — the Cloud Harness. Compaction is a Cloud concern for the same reason.)*

---

## 9. Dependencies

**Upstream — all must be complete.**

- [06 aot jit and wasm publish proof](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)
- [15 arcchat conversation core](15-arcchat-conversation-core.md#rule-wp-15)
- [16 unified execution engine](16-unified-execution-engine.md#rule-wp-16)

**Downstream — consumers of these released outputs.**

- [20 first cross product workflow](20-first-cross-product-workflow.md#rule-wp-20)
- [26 remote action and tool bridge](26-remote-action-and-tool-bridge.md#rule-wp-26)
- [41 extension platform and integrations](41-extension-platform-and-integrations.md#rule-wp-41)
- [52 cloud harness](52-cloud-harness.md#rule-wp-52)

---
