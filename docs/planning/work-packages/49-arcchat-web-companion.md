<a id="rule-wp-49"></a>

# WP-49 — ArcChat Web Companion

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: K — Web and release
> Upstream: `26`, `48`, `52` · Downstream: `50`

> **Goal.** Deliver the browser companion as the second deployment profile of the same application: chat, tasks, approvals, steering, artifacts and remote control — a cloud surface, distinct from the account portal, sharing no state with it.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Web + Cloud + AI. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: production React build and real C#/CF endpoints with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The chat deployment profile: conversation, message and streaming; task, run and step surfaces; approval, steering and cancellation; artifact preview; project and automation visibility; device presence and target selection; and the honest offline and degradation behaviour of a browser client.

**Out of scope.** Any professional product editing. Account management, which is `48`'s profile. A second account application, which is forbidden.

**Why this package exists.** [the current dependency model](../implementation-sequence.md#2-phase-structure) requires the web companion to follow stabilisation of chat, task, approval, remote and realtime — which is why it lands after `26` and after the portal establishes the shared shell.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

The Web companion verifies real generation, tool approval, stream fallback and recovery through WP-52. Portal completion alone is not a working AI service.

| Input | Why it matters |
|---|---|
| [`../../requirements/products/arcchat-mobile-and-web.md`](../../requirements/products/arcchat-mobile-and-web.md) | The companion product model shared with mobile |
| [`../../architecture/10-web-architecture.md`](../../architecture/10-web-architecture.md) `§3`, `§4` | The application structure and the surface matrix |
| [WP-26](26-remote-action-and-tool-bridge.md#rule-wp-26), [WP-48](48-account-portal.md#rule-wp-48) output | The remote closed loop and the shared application shell |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The chat profile shares no state, storage or cookies with the account profile** (**[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**). |
| BR-02 | **The browser never connects to a local endpoint.** Remote work goes through Cloud and the durable tool bridge (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |
| BR-03 | **An operation requiring local presence cannot be completed from the browser alone.** |
| BR-04 | **A web session is shorter-lived and less trusted than a desktop session.** |
| BR-05 | **Web offline is minimal and honest**: it states it is offline and preserves unsent input; it does not pretend to work. |
| BR-06 | **Realtime loss degrades to polling authoritative state**, then backfills on reconnection. |
| BR-07 | **Preview rendering of user content is sandboxed**; untrusted content never executes in the application origin. |
| BR-08 | **There are no public share links in V1.** Links are authenticated and private. |
| BR-09 | **A cloud resource URL verifies permission at access**, and a denial does not disclose existence where that would leak. |
| BR-10 | **Bundle size and interactivity budgets apply**, with a regression gate. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Web/ArcForges.Web.App/app/features/chat/` | Conversation, message, streaming, slash commands, context mentions |
| `src/Web/ArcForges.Web.App/app/features/tasks/` | Task, run, step, tool call, progress, approval, steering |
| `src/Web/ArcForges.Web.App/app/features/artifacts/` | Sandboxed artifact preview and download |
| `src/Web/ArcForges.Web.App/app/features/devices/` | Presence and target selection |
| `deploy/edge/chat/` | Origin configuration for the chat surface |
| `src/Web/tests/chat/` | Streaming, approval, offline, sandbox and budget suites |

**Major types introduced.** `ChatProfile`, `ConversationView`, `StreamingAssembler`, `TaskBoardView`, `ApprovalPanel`, `SteeringPanel`, `ArtifactSandbox`, `PresencePicker`.

---

## 5. Required implementation work

<a id="rule-wp-49.00"></a>

### WP-49.00 — React Chat profile and design-system integration

**What must be fully done.** Compose Chat routes in the same React/TypeScript application using the owned UI tokens/components and generated TS SDK. Account/Chat assets, cookies, query scopes and public config are independently selected and validated. Implement responsive conversation navigation/composer/task panel and native-product handoff with keyboard/reduced-motion support; no Node/browser agent loop.

**Testing requirements.** Production route/profile inspection; approved light/dark/narrow-screen Chat visual baselines; keyboard, touch and long-text states; source/dependency assertion that no provider or Harness implementation enters the browser.

**Completion gate.** The Chat profile is a coherent consumer interface with isolated session/state and no duplicated business authority.

<a id="rule-wp-49.01"></a>

### WP-49.01 — Conversation, exact streaming and recovery

**What must be fully done.** Use the real Cloud Chat/Harness from [WP-52](52-cloud-harness.md#rule-wp-52) for conversation history, submission, bounded output streams and canonical persisted messages. The generated SDK and TS realtime adapter preserve CommandId, exact revisions and UTF-8 byte offsets. Distinguish open/completed/truncated/evicted/superseded stream outcomes from Task terminal state; reconnect/backfill never resubmits the turn. Preserve in-memory unsent input on transient loss, clear scoped state on logout/revocation.

**Testing requirements.** Real Cloud/Harness test configuration with production browser assets: multibyte split boundaries, duplicate/delayed chunks, final-message race, window truncation, attempt replacement, polling-only recovery, expired session and concurrent tabs; peak memory and long-message rendering budgets; verify one customer operation despite reconnect.

**Completion gate.** History, pending input, stream and final-message presentation stay consistent with the Cloud authority under every declared recovery outcome and retain exact positions without duplicate execution.

<a id="rule-wp-49.02"></a>

### WP-49.02 — Tasks, approval and steering

**What must be fully done.** Task, run, step and tool-call surfaces with progress; approve, reject, cancel, pause, retry and steer as idempotent commands; approval requests described in the user's terms; local-presence-required operations clearly refused with an explanation.

**Testing requirements.** Idempotency per control; a local-presence negative test; approval expiry; a durable-attention test asserting a missed notification loses nothing.

**Completion gate.** Every control is idempotent, local-presence-required operations are refused with an explanation, and no pending approval is lost by a missed notification.

<a id="rule-wp-49.03"></a>

### WP-49.03 — Artifacts and sandboxing

**What must be fully done.** Artifact preview inside a sandbox so untrusted content never executes in the application origin. Downloads verify permission at access. No public share links exist in V1.

**Testing requirements.** A sandbox escape attempt with hostile content; a permission-at-access test; an existence-disclosure test on a denied resource; an absence assertion for public share links.

**Completion gate.** **Hostile content cannot escape the preview sandbox**, permission is verified at access, and no public share link exists.

<a id="rule-wp-49.04"></a>

### WP-49.04 — Remote control

**What must be fully done.** Device presence and target selection; remote task issuance through the durable tool bridge; honest state when a target is offline including queue state and expiry.

**Testing requirements.** Offline-target queueing; presence transitions; a no-local-connection assertion for the browser client.

**Completion gate.** Remote work reaches a desktop only through the cloud bridge, and an offline target shows an honest queued state with an expiry.

<a id="rule-wp-49.05"></a>

### WP-49.05 — Offline, degradation and accessibility

**What must be fully done.** Honest offline messaging with unsent input preserved; realtime loss degrading to polling with backfill; a cloud outage reporting which capabilities are unavailable rather than blanking; accessibility with keyboard-only completion of every core workflow.

**Testing requirements.** Offline and reconnection tests; a polling-degradation test; a cloud-outage test; accessibility automated and manual passes.

**Completion gate.** The application never blanks, states what is unavailable and why, converges after reconnection, and completes every core workflow by keyboard.

<a id="rule-wp-49.06"></a>

### WP-49.06 — Performance budgets

**What must be fully done.** Bundle size, first-interactive and interaction responsiveness measured against budget with a regression gate applied at release.

**Testing requirements.** Budget measurements per release candidate; a regression-gate negative test.

**Completion gate.** All three budgets are met and a deliberate regression is caught by the gate.

---

<a id="rule-wp-49.90"></a>
### WP-49.90 — Verify the owned artifact and real integration

**What must be fully done.** Use the fixed same-origin session and CF AI HTTPS/WebSocket route with generated business clients. Keep the companion surface, durable task/message fallback and remote-device authorization.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Full real admitted CF turn/tool/approval/reconnect in a browser; blocked/expired live stream reconciles to the authoritative result without leaking session credentials.

**Completion gate.** Full real admitted CF turn/tool/approval/reconnect in a browser; blocked/expired live stream reconciles to the authoritative result without leaking session credentials. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None directly; consumes cloud APIs |
| Protocol | Consumes chat, task, approval, artifact and presence contracts |
| UI | The browser companion experience |
| Security | Sandboxed previews, per-origin isolation, no public sharing in V1 |
| Platform | Browser support matrix |
| Migration | Cached client handling with a grace period |
| Compatibility | The web client enters the supported client window |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Cross-profile isolation results | [WP-49.00](#rule-wp-49.00) |
| Streaming, interruption and partial-message results | [WP-49.01](#rule-wp-49.01) |
| Control idempotency, local-presence and attention-durability results | [WP-49.02](#rule-wp-49.02) |
| Sandbox escape, permission-at-access and share-link absence results | [WP-49.03](#rule-wp-49.03) |
| Offline-target queueing and no-local-connection results | [WP-49.04](#rule-wp-49.04) |
| Offline, degradation, convergence and accessibility results | [WP-49.05](#rule-wp-49.05) |
| Budget measurements and regression-gate negative test | [WP-49.06](#rule-wp-49.06) |

---

**React/Cloud evidence.** All Chat gates use the generated TS SDK and real Cloud/Harness test deployment. Fixture UI mode remains development-only and is excluded from release routes. Record schema fingerprint, browser/realtime conformance, scope-clearing and visual/accessibility evidence; [PG-23](../../assurance/open-gates-register.md#rule-pg-23) must close before release.

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-49.90](#rule-wp-49.90) and all inherited domain-specific gates must pass on the same candidate closure. Full real admitted CF turn/tool/approval/reconnect in a browser; blocked/expired live stream reconciles to the authoritative result without leaking session credentials.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-49](#rule-wp-49) — Real Chat Harness/task/stream workflows and approved visual/accessibility/performance evidence. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Offline evidence.** Execute this product's applicable [initial-state matrix](../../assurance/testing-and-verification-strategy.md#offline-acceptance-matrix) rows, including fresh shell, hydrated outage, unavailable content, signout and restart where applicable. Record permitted local work and explicitly unavailable Cloud actions.

**All of the following, with recorded evidence:**

1. The chat and account profiles share code and provably share no state, storage or cookies.
2. An interrupted stream is always shown as interrupted, never as complete.
3. Every task control is idempotent; local-presence-required operations are refused with an explanation; a missed notification never loses a pending approval.
4. **Hostile content cannot escape the preview sandbox**; permission is verified at access; no public share link exists in V1.
5. Remote work reaches a desktop only through the cloud bridge; an offline target shows an honest queued state with an expiry.
6. The application never blanks during an outage, converges after reconnection, and completes every core workflow by keyboard.
7. Bundle, first-interactive and interaction budgets are met, and a deliberate regression is caught by the gate.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-26](26-remote-action-and-tool-bridge.md#rule-wp-26)
- [WP-48](48-account-portal.md#rule-wp-48)
- [WP-52](52-cloud-harness.md#rule-wp-52)

**Downstream — consumers of these released outputs.**

- [WP-50](50-full-platform-production-release.md#rule-wp-50)


---
