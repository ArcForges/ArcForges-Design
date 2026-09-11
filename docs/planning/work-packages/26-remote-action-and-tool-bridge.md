<a id="rule-wp-26"></a>

# WP-26 — Device Presence, Remote Action and the Tool Bridge

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `17`, `24`, `25` · Downstream: `31`, `33`, `36`, `49`, `52`

> **Goal.** Let a remote surface ask a desktop to do something, without Cloud ever reaching into a machine: a durable `ToolRequest` pulled by ArcChat Desktop, re-authorised locally, and answered with an idempotent `ToolResult`.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud + AI ports; ArcChat and product owners. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Device presence; **per-Step tool locality and device targeting** ([TK-02](../../architecture/data-model/01-cloud-data-model.md#rule-tk-02)); the durable tool-request bridge and its local re-authorisation; remote approval and steering; result and artifact return; and the honest degradation when the target desktop is offline.

**Out of scope.** The mobile client that uses it (`31`). The web companion (`49`). Cloud-side AI execution economics (`43`).

**Why this package exists.** **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** forbids Cloud from connecting to localhost, a named pipe, a domain socket or local standard I/O. Remote action therefore cannot be a reverse tunnel; it must be a durable pull-and-answer protocol. Getting this shape right is what makes the mobile companion possible at all.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** | The prohibition that determines the entire design |
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) `§10` | The remote action model |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) | Placement, remote execution and idempotency |
| [`../../requirements/02-identity-account-and-workspace.md`](../../requirements/02-identity-account-and-workspace.md) `§5` | Device trust as the gate for remote access |
| [WP-17](17-arcchat-independent-core.md#rule-wp-17), [WP-24](24-realtime-and-reliable-events.md#rule-wp-24), [WP-25](25-sync-engine-and-blob-lifecycle.md#rule-wp-25) output | ArcChat Desktop, realtime and sync |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Cloud never initiates a connection to a local endpoint** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). The desktop pulls. |
| BR-02 | **A tool request is durable.** It survives a desktop being offline and is delivered when it returns. |
| <a id="rule-br-03"></a>BR-03 | **Local re-authorisation is mandatory.** A cloud-side approval is not a local authorisation; the desktop re-evaluates against local policy and the local actor chain. |
| BR-04 | **A tool result is idempotent**: answering twice has one effect, and a lost result is recoverable by re-answering. |
| BR-05 | **Remote access requires device trust** and is off by default ([WP-22.03](22-identity-workspace-and-device.md#rule-wp-22.03)). |
| <a id="rule-br-06"></a>BR-06 | **A high-risk operation is not executed remotely without the approval its risk level demands**, including local presence where required. |
| BR-07 | **An offline target degrades honestly**: the request is queued with a visible state and an expiry, never silently dropped or falsely reported as running. |
| BR-08 | **The tool request carries a bounded payload**; large data crosses by reference through the resource path. |
| BR-09 | **Locality is explicit per Step** ([TK-02](../../architecture/data-model/01-cloud-data-model.md#rule-tk-02)): a Step records where it ran, and a Step that must run locally never silently runs in the cloud. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.Agent/` | Tool request queue, per-Step locality, result reconciliation |
| `src/Cloud/ArcForges.Cloud.Modules.Identity/` | Device presence tracking and trust-gated remote eligibility |
| `src/ArcChat/ArcChat.CloudClient/` | The pull loop, local re-authorisation, result submission |
| `src/ArcChat/ArcChat.Agent/` | Cloud task projection and device-tool bridge presentation; no local agent execution engine |
| `src/BuildingBlocks/ArcForges.Execution/` | Per-Step locality recording and remote attempt semantics |
| `tests/RemoteToolBridgeTests/` | Bridge, re-authorisation, offline, duplicate and expiry suites |

**Major types introduced.** `DevicePresence`, `RemoteEligibility`, `ToolRequest`, `ToolRequestState`, `ToolResult`, `LocalReauthorization`, `PlacementDecision`, `RemoteApproval`, `RequestExpiry`.

---

## 5. Required implementation work

<a id="rule-wp-26.00"></a>

### WP-26.00 — Device presence

**What must be fully done.** Presence reflecting whether a device's ArcChat Desktop is connected and eligible for remote work, with a heartbeat and a stale-presence timeout. Presence is a capability of Cloud, visible to the user, and never inferred from a stale session.

**Testing requirements.** Presence transition tests; stale-timeout accuracy; a test asserting a valid session with no live connection does not report present.

**Completion gate.** Presence reflects live connectivity and never reports present from a stale session.

<a id="rule-wp-26.01"></a>

### WP-26.01 — Tool request queue

**What must be fully done.** A durable per-device queue with ordering, expiry and visible state. The desktop pulls with a long-poll or realtime signal plus HTTP fetch. A request survives cloud restarts and desktop restarts.

**Testing requirements.** Queue survival across restarts of both sides; ordering; expiry; a test asserting no cloud-initiated connection to the device occurs.

**Completion gate.** Requests survive restarts on both sides and no cloud-initiated local connection exists.

<a id="rule-wp-26.02"></a>

### WP-26.02 — Local re-authorisation

**What must be fully done.** On receipt, ArcChat Desktop re-evaluates the request against local policy, the local capability registry, local permission grants and the local actor chain. A request the cloud accepted may still be refused locally, with a reason returned.

**Testing requirements.** A refusal matrix covering local policy denial, missing capability, revoked grant, and risk requiring local presence; a forged-approval test.

**Completion gate.** A cloud-approved request is still refused locally when local policy denies it, and the reason is returned.

<a id="rule-wp-26.03"></a>

### WP-26.03 — Execution and result

**What must be fully done.** An accepted request invokes the typed local product capability after re-authorisation. A long-running product operation returns a product-owned ProductJobRef; the Cloud Agent Task remains in Cloud. Progress is projected back and an idempotent ToolResult is submitted. A duplicate result submission has one effect. A lost result is recoverable by re-submission without duplicating the effect.

**Testing requirements.** Duplicate submission; lost-result recovery; kill-during-execution followed by reconnect; an effect-certainty assertion for each failure mode.

**Completion gate.** One request produces one effect, and a lost result is recoverable without duplication.

<a id="rule-wp-26.04"></a>

### WP-26.04 — Remote approval, steering and presence-gated risk

**What must be fully done.** Approval and steering delivered from a remote surface, with high-risk operations demanding the approval their risk level requires. An operation requiring local presence cannot be approved remotely.

**Testing requirements.** Remote approval and steering paths; a negative test asserting a local-presence-required operation cannot complete via remote approval alone.

**Completion gate.** Remote approval works for permitted risk levels and cannot satisfy a local-presence requirement.

<a id="rule-wp-26.05"></a>

### WP-26.05 — Offline degradation and expiry

**What must be fully done.** With the target offline, the request queues with a visible state and a stated expiry. The requesting surface is told honestly. On expiry the request is closed with a typed reason, never left ambiguous.

**Testing requirements.** Offline queue-and-deliver; expiry-while-offline; a state-visibility test on the requesting surface.

**Completion gate.** An offline target queues visibly with an expiry, and expiry closes the request with a typed reason.

<a id="rule-wp-26.06"></a>

### WP-26.06 — Per-Step tool locality and device targeting

**What must be fully done.** **Every Task is Cloud-owned** ([TO-01](../../architecture/data-model/00-data-model-overview.md#rule-to-01)); there is no task placement to record. **Each Step records its `tool_locality ∈ {cloud, device}`** with `target_device_id` on the Step, since one Task routinely mixes both ([TK-02](../../architecture/data-model/01-cloud-data-model.md#rule-tk-02)). A Step declared `device` is never satisfied by a cloud substitute; with no eligible device online it enters `waitingDevice` with a stated reason and a bounded wait, holding no included capacity ([PL-03](../../architecture/09-ai-and-agent-runtime-architecture.md#rule-pl-03)). Locality is visible in the task centre and in the trace.

**Testing requirements.** A negative test asserting a `device` Step is **never** satisfied by a cloud substitute; a mixed-locality Task exercising both Step kinds; a `waitingDevice` test asserting a bounded wait, a stated reason and **no capacity held** while waiting; a schema test asserting no `placement` or `authoritative_store` column exists on `task.task` ([TK-01](../../architecture/data-model/01-cloud-data-model.md#rule-tk-01)).

**Completion gate.** Every Step's locality is recorded and visible; a `device` Step is never satisfied by a cloud substitute; a Task with no eligible device waits with a stated reason holding no capacity; and no `placement` or `authoritative_store` column exists on `task.task` ([TK-01](../../architecture/data-model/01-cloud-data-model.md#rule-tk-01)).

---

<a id="rule-wp-26.90"></a>
### WP-26.90 — Verify the owned artifact and real integration

**What must be fully done.** Preserve durable pull-based ToolRequest/ToolResult authority and per-step locality. Connect CF through authenticated C# ports; connect desktop through generated gRPC and product local owners.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Duplicate delivery, device absence, stale permission, approval expiry, timeout-after-dispatch and result reconciliation are tested without Cloud/CF dialing a local endpoint.

**Completion gate.** Duplicate delivery, device absence, stale permission, approval expiry, timeout-after-dispatch and result reconciliation are tested without Cloud/CF dialing a local endpoint. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Tool request queue, presence, and **per-Step tool locality** ([TK-02](../../architecture/data-model/01-cloud-data-model.md#rule-tk-02)) |
| Protocol | The tool-request and tool-result contracts |
| UI | Presence, remote task state, remote approval and expiry surfaces |
| Security | Local re-authorisation is the central control; trust gates eligibility |
| Platform | Desktop pull behaviour under sleep, network change and restart |
| Migration | Tool request contract versioning across desktop versions |
| Compatibility | A desktop older than the cloud must still answer or refuse cleanly |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Presence transition and stale-session results | [WP-26.00](#rule-wp-26.00) |
| Queue survival, ordering, expiry and no-inbound-connection assertion | [WP-26.01](#rule-wp-26.01) |
| Local refusal matrix and forged-approval results | [WP-26.02](#rule-wp-26.02) |
| Duplicate, lost-result and kill-during-execution results | [WP-26.03](#rule-wp-26.03) |
| Remote approval and local-presence negative results | [WP-26.04](#rule-wp-26.04) |
| Offline queue, delivery and expiry results | [WP-26.05](#rule-wp-26.05) |
| Per-Step locality, no-cloud-substitute and waiting-device results | [WP-26.06](#rule-wp-26.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-26.90](#rule-wp-26.90) and all inherited domain-specific gates must pass on the same candidate closure. Duplicate delivery, device absence, stale permission, approval expiry, timeout-after-dispatch and result reconciliation are tested without Cloud/CF dialing a local endpoint.

**All of the following, with recorded evidence:**

1. Presence reflects live connectivity and never reports present from a stale session.
2. Tool requests survive restarts on both sides; **no cloud-initiated connection to a local endpoint exists anywhere in the implementation.**
3. A cloud-approved request is still refused locally when local policy denies it, with the reason returned.
4. One request produces one effect; a lost result is recoverable without duplicating the effect.
5. Remote approval works for permitted risk levels and can never satisfy a local-presence requirement.
6. An offline target queues visibly with an expiry, and expiry closes the request with a typed reason.
7. Every Step's locality is recorded and visible; a `device` Step is never satisfied by a cloud substitute; and no task-level placement column exists.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [17 arcchat independent core](17-arcchat-independent-core.md#rule-wp-17)
- [24 realtime and reliable events](24-realtime-and-reliable-events.md#rule-wp-24)
- [25 sync engine and blob lifecycle](25-sync-engine-and-blob-lifecycle.md#rule-wp-25)

**Downstream — consumers of these released outputs.**

- [31 arcchat mobile android](31-arcchat-mobile-android.md#rule-wp-31)
- [33 arcscope acquisition and session](33-arcscope-acquisition-and-session.md#rule-wp-33)
- [36 arcslate project and timeline](36-arcslate-project-and-timeline.md#rule-wp-36)
- [49 arcchat web companion](49-arcchat-web-companion.md#rule-wp-49)
- [52 cloud harness](52-cloud-harness.md#rule-wp-52)

---
