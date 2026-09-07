<a id="rule-wp-31"></a>

# WP-31 — ArcChat Mobile Android Remote Closed Loop

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Integration after real Cloud prerequisites
> Upstream: `26`, `30`, `52` · Downstream: `32`

> **Goal.** Deliver the complete remote control surface: conversation, task, approval and steering from a phone, through Cloud, to a desktop — with **no direct connection to a LAN Hub, named pipe, socket or professional application** anywhere in the design.

---

## 1. Scope and purpose

**In scope.** Authentication and device binding; conversation, message, slash command and context mention; model, mode and agent profile selection; task, run, step, tool call and progress; approval, rejection, cancel, pause, retry and steering; artifact, file and result preview; device presence and target selection; push, deep links, background resume and weak-network recovery.

**Out of scope.** Any commerce surface (**[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**) — enforced as a build check in `32`. Any professional product editing. Store submission (`32`).

**Why this package exists.** [the companion requirements](../../requirements/products/arcchat-mobile-and-web.md) define ArcChat Android as a chat-style computer remote controller with a complete remote control surface — not a phone edition of a professional product, and not a generic screen-and-input remote tool.

---

## 2. Required inputs and dependencies

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
| BR-08 | **No provider credential exists on any client** ([BY-01](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)). Provider credentials are deployment secrets held only by the Cloud host ([DC-15](../../requirements/11-policy-and-configuration.md#rule-dc-15)) and never projected to a client ([DC-14](../../requirements/11-policy-and-configuration.md#rule-dc-14)). |
| BR-09 | **Offline caching is restrained and bounded**: recent task state, recent conversation summaries, pending attention items and small previews — evictable and never authoritative. |
| BR-10 | **Complex configuration surfaces live on desktop and web**, not on mobile. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Mobile/ArcChat.Mobile/` | Application shell, navigation, platform integration |
| `src/Mobile/ArcChat.Mobile.Presentation/` | Conversation, task, approval, steering, artifact and device surfaces |
| `src/Mobile/ArcChat.Mobile.Application/` | Companion application services over the shared clients |
| `src/Mobile/ArcChat.Mobile.Persistence/` | Bounded cache and the outbox |
| `tests/AndroidUiTests/`, `tests/MobileContractTests/` | Interaction, offline, reconnection and contract suites |

**Major types introduced.** `CompanionSession`, `ConversationView`, `SlashCommand`, `ContextMention`, `TaskView`, `ApprovalCard`, `SteeringControl`, `ArtifactPreview`, `TargetDevice`, `PushRegistration`, `DeepLinkRoute`.

---

## 5. Required implementation work

<a id="rule-wp-31.00"></a>

### WP-31.00 — Authentication, workspace and device binding

**What must be fully done.** Sign-in with passkey and email code; workspace selection; device registration with its own trust level; and target-device selection for remote work. The device's remote eligibility is visible.

**Testing requirements.** Sign-in paths; workspace switch; device registration and revocation from another device taking effect; a target-selection test with a device offline.

**Completion gate.** Sign-in, workspace selection and device binding work, and revoking this device elsewhere terminates it promptly.

<a id="rule-wp-31.01"></a>

### WP-31.01 — Conversation surface

**What must be fully done.** Conversation and message display with streaming assembly, slash commands, context mentions, and model, mode and agent profile selection. Message composition works offline into the outbox with a visible pending state.

**Testing requirements.** Streaming, interruption and resume; offline composition and send-on-reconnect; profile and model switching.

**Completion gate.** Conversation works online and composes offline with an explicit pending state.

<a id="rule-wp-31.02"></a>

### WP-31.02 — Task, approval and steering

**What must be fully done.** Task, run, step and tool-call display with progress; approve, reject, cancel, pause, retry and steer, each producing an idempotent command. Approval cards state what is being approved in the user's terms. Operations requiring local presence are shown as requiring the desktop.

**Testing requirements.** Each control's idempotency under retry; a local-presence-required negative test; an approval-expiry test.

**Completion gate.** Every control is idempotent, and a local-presence-required operation is clearly refused with an explanation.

<a id="rule-wp-31.03"></a>

### WP-31.03 — Artifacts and previews

**What must be fully done.** Artifact, file and result previews as bounded, read-only representations. A preview never becomes an editing surface for a professional product's state. Downloads respect cellular policy.

**Testing requirements.** Preview per artifact kind; a structural test asserting no writable professional state exists on device; a cellular-policy test.

**Completion gate.** Previews are read-only and bounded, and no professional writable state exists on the device.

<a id="rule-wp-31.04"></a>

### WP-31.04 — Presence, push and deep links

**What must be fully done.** Device presence display with honest offline state; push registration per device and installation, revoked with the device; push actions opening the right surface without carrying authorization; universal links opening the installed application; deep links treated as untrusted input carrying no secret.

**Testing requirements.** Presence transitions; push registration and revocation; a push-authorization negative test; a hostile deep-link test; a missed-push test asserting durable attention survives.

**Completion gate.** Push carries no authorization, deep links reject hostile input, and missing a push never loses a pending approval.

<a id="rule-wp-31.05"></a>

### WP-31.05 — Background, weak network and reconnection

**What must be fully done.** Foreground and background transitions rebuilding or restoring the realtime session; sequence-gap backfill over HTTP on resume; exponential backoff with jitter; and a high-risk task requiring explicit confirmation rather than auto-executing on reconnection.

**Testing requirements.** Background-resume with an induced gap; weak-network and flapping-connection tests; a high-risk auto-execution negative test.

**Completion gate.** The client converges after background resume and weak network, and never auto-executes a high-risk task on reconnection.

<a id="rule-wp-31.06"></a>

### WP-31.06 — Prohibited-path enforcement

**What must be fully done.** A structural assertion that no code path performs network discovery, addresses a named pipe or socket, or connects to anything other than the cloud endpoints. This is asserted as a policy test, not merely reviewed.

**Testing requirements.** A policy test with a negative fixture; a runtime network-observation test asserting only cloud endpoints are contacted.

**Completion gate.** **No prohibited connection path exists**, verified both structurally and by runtime observation.

---

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

- [26 — Device Presence, Remote Action and the Tool Bridge](26-remote-action-and-tool-bridge.md)
- [30 — Mobile Shared Architecture and the Apache Boundary](30-mobile-shared-architecture.md)
- [52 — The Cloud Harness](52-cloud-harness.md)

**Downstream — these consume this package’s completed output.**

- [32 — Mobile Release Engineering and Store Gates](32-mobile-release-and-store-gates.md)
