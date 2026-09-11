<a id="rule-wp-31"></a>

# WP-31 — ArcChat Mobile Android Remote Closed Loop

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Integration after real Cloud prerequisites
> Upstream: `26`, `30`, `52` · Downstream: `32`

> **Goal.** Deliver the complete remote control surface: conversation, task, approval and steering from a phone, through Cloud, to a desktop — with **no direct connection to a LAN Hub, named pipe, socket or professional application** anywhere in the design.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Mobile; real Cloud/AI. Inputs: exact Apache Contracts npm packages/descriptors and the selected RN/native package closure; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: RN/Hermes artifact and real generated service clients with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Authentication and device binding; conversation, message, slash command and context mention; model, mode and agent profile selection; task, run, step, tool call and progress; approval, rejection, cancel, pause, retry and steering; artifact, file and result preview; device presence and target selection; push, deep links, background resume and weak-network recovery.

**Out of scope.** Any commerce surface (**[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**) — enforced as a build check in `32`. Any professional product editing. Store submission (`32`).

**Why this package exists.** [the companion requirements](../../requirements/products/arcchat-mobile-and-web.md) define ArcChat Android as a chat-style computer remote controller with a complete remote control surface — not a phone edition of a professional product, and not a generic screen-and-input remote tool.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

The real Task, streaming, approval and recovery gates in this package consume WP-52. A scripted Cloud endpoint cannot close the Android product loop, so this package executes in J after the Harness; [WP-30](30-mobile-shared-architecture.md#rule-wp-30) preserves early mobile contract work.

| Input | Why it matters |
|---|---|
| [Mobile architecture](../../architecture/11-mobile-architecture.md) | Companion positioning, Cloud-only communication, platform boundaries and the Android delivery posture |
| [`../../requirements/products/arcchat-mobile-and-web.md`](../../requirements/products/arcchat-mobile-and-web.md) | The companion product model, offline behaviour and notification rules |
| [`../../architecture/11-mobile-architecture.md`](../../architecture/11-mobile-architecture.md) | Network, offline, push, deep links and placement constraints |
| [WP-26](26-remote-action-and-tool-bridge.md#rule-wp-26), [WP-30](30-mobile-shared-architecture.md#rule-wp-30) output | The remote closed loop and the mobile foundation |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Direct connection from mobile to a LAN Hub, named pipe, domain socket or professional application is prohibited** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). The only path is mobile → Cloud → ArcChat Desktop. |
| BR-02 | **The client never scans a network and never performs local discovery.** |
| BR-03 | **A high-risk agent task is never auto-executed on reconnection**; it requires explicit confirmation. |
| BR-04 | **A push notification is not durable attention state.** Missing a push never loses a pending approval. |
| BR-05 | **A push action opens a surface; it never carries authorization.** |
| BR-06 | **An operation requiring local presence cannot be completed from mobile alone** ([WP-26.04](26-remote-action-and-tool-bridge.md#rule-wp-26.04)). |
| BR-07 | **Mobile holds no professional product's writable domain state.** |
| BR-08 | **No provider credential exists on any client** ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)). Provider credentials are held by their designated C# or CF deployment ([DC-15](../../requirements/11-policy-and-configuration.md#rule-dc-15)) and never projected to a client ([DC-14](../../requirements/11-policy-and-configuration.md#rule-dc-14)). |
| BR-09 | **Offline caching is restrained and bounded**: recent task state, recent conversation summaries, pending attention items and small previews — evictable and never authoritative. |
| BR-10 | **Complex configuration surfaces live on desktop and web**, not on mobile. |

---

## 4. Projects, directories, files and major types affected

All paths are in ArcForges-Mobile. [The mobile surface and state table](../../architecture/11-mobile-architecture.md#15-mobile-repository-screens-and-execution-state) is binding.

| Location | Deliverable |
|---|---|
| src/app/ | Authentication stack, four tabs, typed nested routes, account/realm guards |
| src/features/auth/, devices/, settings/ | Sign-in/recovery, workspace and installation binding, target presence, account/settings surfaces |
| src/features/conversations/ | Paginated list/detail/branch, composer, slash/context/model/profile choices, live/final rendering |
| src/features/tasks/, approvals/ | Task/run/step/tool/progress, reason and recovery actions, explicit control and approval cards |
| src/features/artifacts/ | Bounded read-only accepted previews, authorized downloads and OS file/share integration |
| src/services/, src/storage/, src/platform/ | Foundation service composition, projections/outbox and platform integrations reused by these slices |
| tests/unit/, tests/contract/, tests/device/ | Feature state, compatibility and actual Android/Cloud/CF/desktop loops |

Every feature delivers its loading/empty/offline/denied/expired/error states, localization and accessibility with its happy path.

---

## 5. Required implementation work

<a id="rule-wp-31.00"></a>

### WP-31.00 — Authentication, workspace and device binding


**What must be fully done.** Implement the realm/sign-in/recovery stack, workspace selector, installation registration and Devices/Settings tabs using the selected identity/workspace/device/entitlement RPCs. Enforce generation-bound navigation and state partitioning. Show target offline/eligibility and read-only account/usage, with only the allowed portal link-outs.

**Testing requirements.** Passkey/email/recovery, workspace change, offline target and remote revoke; launch with no account and with hydrated offline state; prohibited commerce route negative cases.

**Completion gate.** All authentication and account/device entry states lead to the specified next surface or a recoverable reason; no stale session is reused.

<a id="rule-wp-31.01"></a>

### WP-31.01 — Conversation surface


**What must be fully done.** Implement Conversations list/detail/branch and composer using chat operations and model/profile catalogues. Preserve context origins, stable IDs and branch pins; queue only explicit Send; show draft/pending/partial/committed states. CF live and catch-up use the Task stream identity; committed Chat replaces transient text.

**Testing requirements.** Real CF model turn, branch and profile selection, attachments/context, 1000-message virtualized list, 4 MiB live answer, interrupted stream and lost append acknowledgement with one canonical message/turn.

**Completion gate.** All accepted conversation functions work through released public clients; no draft is lost or duplicate AI turn created by recovery.

<a id="rule-wp-31.02"></a>

### WP-31.02 — Task, approval and steering


**What must be fully done.** Implement Tasks list/detail with run/step/tool/progress, blocking reason and recovery state; Approvals/attention routes show proposal, risk, target, expiry, scope and budget. Bind cancel/pause/resume/retry/steer/decide RPCs to current revision and explicit command identity. Requery stale proposals; require current foreground confirmation for high-risk actions and show desktop-presence requirements.

**Testing requirements.** Duplicate each control, stale revision/proposal, expired approval, unknown nonterminal state, desktop offline/return and actual mixed Cloud/desktop turn.

**Completion gate.** Controls preserve task/attempt/approval semantics and never infer success from a notification or connection state.

<a id="rule-wp-31.03"></a>

### WP-31.03 — Artifacts and previews


**What must be fully done.** Implement the accepted Notes excerpt/PDF, Scope chart/table/measurement and Slate media/result previews from Resource metadata/version pins. Obtain authenticated CF download tickets, support bounded range/cellular policy and explicit OS save/share. Keep professional domain state read-only.

**Testing requirements.** Each preview kind, missing local-only source, invalid/revoked ticket, mid-range revocation, large download denial and unavailable-content fallback.

**Completion gate.** Previews and exports remain authorized, bounded and read-only; missing content is honestly identified.

<a id="rule-wp-31.04"></a>

### WP-31.04 — Presence, push and deep links


**What must be fully done.** Wire durable notifications/approvals and device presence polling to badges/routes. Register push per installation; revoke/unregister on sign-out/device revoke. Parse canonical HTTPS app links with an allowlist and current realm/permission checks. Notification actions only navigate.

**Testing requirements.** No push and missed push retain attention; hostile link and wrong realm refuse; revoked/expired target displays recovery; device presence changes update eligibility.

**Completion gate.** Push is an optional hint; every attention item and remote target state is recoverable by current RPC reads.

<a id="rule-wp-31.05"></a>

### WP-31.05 — Background, weak network and reconnection


**What must be fully done.** Apply the foundation generation/outbox lifecycle to every feature. Resume validates session, polls authoritative state, handles cursor reset then connects to CF tail. Preserve cached read/draft behavior offline; queued ordinary sends reconcile, while high-risk controls wait for renewed explicit confirmation.

**Testing requirements.** Kill during send/refresh, airplane/flapping network, background process removal, sign-out/revoke during an in-flight read and expired approval on reconnect.

**Completion gate.** All feature states converge without lost durable user work, stale-account data or repeated external effect.

<a id="rule-wp-31.06"></a>

### WP-31.06 — Prohibited-path enforcement


**What must be fully done.** Enforce the exact remote path Mobile → public C# admission/control and CF presentation/object facade → Cloud bridge → ArcChat desktop. Native OS passkey/push/file interactions are the declared platform exceptions; no local discovery/Hub RPC/professional editor/provider secret or executable extension enters Mobile.

**Testing requirements.** Import/route policy negative fixtures and runtime network observation over the complete product loop; five commerce prohibitions and no local network target.

**Completion gate.** The independent Apache app implements only the accepted companion capabilities and declared endpoints.

<a id="rule-wp-31.90"></a>
### WP-31.90 — Verify the owned artifact and real integration


**What must be fully done.** Run the complete signed-candidate Android companion against the actual Cloud OCI, deployed CF Worker/R2 and ArcChat bridge from the integration manifest after WP52.

**Testing requirements.** Create a Cloud-only turn with desktop off, then a desktop-tool turn with approval, network interruption and device return; verify durable final message/Task and usage outcome.

**Completion gate.** Every surface, failure/recovery state and prohibited-path condition above passes on actual Android; no product behavior remains for implementation-time design.

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Bounded mobile cache and outbox |
| Protocol | Mobile as a full consumer of the task, approval and steering contracts |
| UI | The complete companion surface |
| Security | Push without authorization, untrusted deep links, no local secrets |
| Platform | Android lifecycle, notifications, background limits and secure storage |
| Migration | Mobile cache schema versioning |
| Compatibility | Mobile client version enters the supported window |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Sign-in, workspace and device revocation results | [WP-31.00](#rule-wp-31.00) |
| Streaming, offline composition and profile switching results | [WP-31.01](#rule-wp-31.01) |
| Control idempotency and local-presence refusal results | [WP-31.02](#rule-wp-31.02) |
| Preview and no-writable-state results | [WP-31.03](#rule-wp-31.03) |
| Push, deep link and missed-push durability results | [WP-31.04](#rule-wp-31.04) |
| Background resume, weak network and high-risk confirmation results | [WP-31.05](#rule-wp-31.05) |
| Prohibited-path policy test and runtime network observation | [WP-31.06](#rule-wp-31.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-31.90](#rule-wp-31.90) and all inherited domain-specific gates must pass on the same candidate closure. Android device tests cover full admitted AI turn, pending/expired approval, dropped network, process restart, duplicate send and durable final answer. No professional editor or local-LAN execution path.

**Offline evidence.** Execute this product's applicable [initial-state matrix](../../assurance/testing-and-verification-strategy.md#offline-acceptance-matrix) rows, including fresh shell, hydrated outage, unavailable content, signout and restart where applicable. Record permitted local work and explicitly unavailable Cloud actions.

**All of the following, with recorded evidence:**

1. Sign-in, workspace selection and device binding work; revoking the device elsewhere terminates it promptly.
2. Conversation works online and composes offline with an explicit pending state.
3. Every task control is idempotent; a local-presence-required operation is clearly refused with an explanation.
4. Previews are read-only and bounded; no professional writable domain state exists on the device.
5. Push carries no authorization; deep links reject hostile input; missing a push never loses a pending approval.
6. The client converges after background resume and weak network, and never auto-executes a high-risk task on reconnection.
7. **No prohibited connection path exists** — verified structurally by policy test and by runtime network observation.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [26 remote action and tool bridge](26-remote-action-and-tool-bridge.md#rule-wp-26)
- [30 mobile shared architecture](30-mobile-shared-architecture.md#rule-wp-30)
- [52 cloud harness](52-cloud-harness.md#rule-wp-52)

**Downstream — consumers of these released outputs.**

- [32 mobile release and store gates](32-mobile-release-and-store-gates.md#rule-wp-32)

---
