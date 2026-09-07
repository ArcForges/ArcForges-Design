# Realtime Events and the Durable Bridge

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Contracts
> Governing authority: [`00-operation-catalogue.md`](00-operation-catalogue.md), **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**, [`../05-cloud-architecture.md`](../05-cloud-architecture.md) `§7`, `§10`
> Companions: [`01-public-api-operations.md`](01-public-api-operations.md), [`../data-model/01-cloud-data-model.md`](../data-model/01-cloud-data-model.md)

Two mechanisms, one principle: **neither carries authority**. Realtime tells a client something changed; the client re-reads the fact. The bridge carries a request and an answer; the desktop decides whether to honour it.

---

## 1. The realtime event set

Every event carries `{ subscriptionKey, seq, workspaceId, occurredAt, correlationId }` plus its own payload. `seq` is per subscription ([RV-05](#rule-rv-05)), which is what makes a gap detectable.

| Event | Payload | Consumer action |
|---|---|---|
| `sync.changed` | `aggregateKind`, `aggregateId`, `aggregateRev`, `originDeviceId` | Pull from the change feed; skip own echo |
| `sync.conflictRaised` | `aggregateKind`, `aggregateId` | Surface it; fetch through `sync.listConflicts` |
| `task.stateChanged` | `taskId`, `state`, `reasonFacet`, `rev` | Refresh the task if displayed |
| `task.progress` | `taskId`, `runId`, `progress`, `stepOrdinal` | **Best-effort display only** — never persisted as outcome |
| `task.outputAppended` | `taskId`, `streamId`, `nextOffset` | **A hint that more output exists.** Read it with `task.readStream(taskId, streamId, fromOffset)` (`§7.2` of the harness). **Carries no content** ([RE-02](#rule-re-02)), and is optional — polling reaches the same output ([SR-01](../17-agent-harness.md#rule-sr-01) of the harness) |
| `approval.raised` | `approvalId`, `taskId`, `riskLevel`, `expiresAt` | Show it; **also durable**, so a missed event loses nothing |
| `approval.resolved` | `approvalId`, `decision` | Dismiss the prompt |
| `entitlement.changed` | `entitlementVersion` | Re-read `entitlement.getSnapshot` |
| `device.presenceChanged` | `deviceId`, `connectionState`, `eligibleForRemote` | Update target selection |
| `bridge.requestAvailable` | `count` | **Trigger a pull** — carries no request content |
| `notification.raised` | `notificationId`, `durability` | Show; a durable one is also in `notification.list` |
| `policy.bundleAvailable` | `bundleVersion` | Fetch and validate the bundle |
| `resource.committed` | `cloudObjectId`, `contentHash` | A pending upload finished |
| `capacity.changed` | `workspaceId`, `recoveryAt?` | Re-read `entitlement.getCapacity`; **never used as the balance itself** |
| `serviceTerm.changed` | `workspaceId` | Re-read `entitlement.getServiceTerm` — a term ended, renewed or entered grace |
| `simulation.stateChanged` | `runId`, `state`, `committedSequence` | Refresh the run; **fetch segments by manifest**, never from this event ([SO-04](01-public-api-operations.md#rule-so-04)) |
| `config.revisionActivated` | `configRevisionId` | Re-read the allowlisted client projection ([DC-14](../../requirements/11-policy-and-configuration.md#rule-dc-14)) |

| # | Rule |
|---|---|
| RE-01 | **No event carries authoritative state** ([SO-02](00-operation-catalogue.md#rule-so-02)). Every payload above is an identifier plus enough metadata to decide whether to act. |
| <a id="rule-re-02"></a>RE-02 | **No event carries an object body, a message body, or document content.** |
| RE-03 | **`task.progress` is explicitly lossy.** Losing every progress event must not affect the recorded outcome ([WP-16.06](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.06)). |
| RE-04 | **`approval.raised` is a hint over durable state.** Missing it never loses a pending approval ([PD-02](../11-mobile-architecture.md#rule-pd-02)). |
| RE-05 | **`bridge.requestAvailable` carries a count, not content** — the desktop pulls, which keeps **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** true even in the notification. |
| <a id="rule-re-06"></a>RE-06 | **A missed event is always recoverable by re-reading**, and every event above names what to re-read. |
| <a id="rule-re-07"></a>RE-07 | **Realtime is optional, and its absence is a complete-fallback case, not a degraded one.** Every event above has a polling or cursor equivalent on the HTTP surface, and a client with realtime permanently disabled reaches the same state — later, not less completely ([SO-05](01-public-api-operations.md#rule-so-05), [SIM-13](../../requirements/products/arcscope.md#rule-sim-13)). |
| RE-08 | **No commercial decision is ever taken from an event.** `capacity.changed` and `serviceTerm.changed` are refresh hints; admission is server-side and atomic ([AD-01](../16-billing-and-commerce-architecture.md#rule-ad-01), [EC-02](01-public-api-operations.md#rule-ec-02)). A client that admitted work because an event said capacity was available would be wrong under concurrency. |
| RE-09 | **Bulk data never flows over realtime** ([SO-04](01-public-api-operations.md#rule-so-04)): no simulator segment, object body, message body or document content. |

---

## 2. Subscriptions

```
subscribe(subscriptionKey) → { accepted, startSeq } | refused(reason)
```

| Subscription key | Scope | Permission |
|---|---|---|
| `workspace:{id}` | Sync, entitlement, capacity, service term, notification, policy, simulation for one workspace | **Ownership** ([WO-02](../data-model/01-cloud-data-model.md#rule-wo-02)) |
| `task:{id}` | One task's state, progress and output | Read on the task |
| `device:{id}` | Presence and bridge availability for one device | The device's own session |
| `approval:{workspaceId}` | Approvals awaiting this user | **Ownership** ([WO-02](../data-model/01-cloud-data-model.md#rule-wo-02)) |

| # | Rule |
|---|---|
| <a id="rule-sb-01"></a>SB-01 | **Permission is checked at subscribe and re-checked when permission changes.** Losing permission stops delivery immediately and tells the client ([WP-24.01](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.01)). |
| SB-02 | **A subscription cannot escape its scope**, and an attempt is refused rather than silently narrowed. |
| SB-03 | **`startSeq` is returned at subscribe**, so a client knows where its gap detection begins. |

---

## 3. Gap detection and recovery

```
client tracks lastSeq per subscription
   ↓ receives seq
      seq == lastSeq + 1  → apply, advance
      seq  > lastSeq + 1  → GAP: record it, then reconcile over HTTP
      seq <= lastSeq      → duplicate: discard idempotently
```

| # | Rule |
|---|---|
| GP-01 | **A gap is never ignored.** It is recorded as telemetry and triggers reconciliation ([WP-24.02](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.02)). |
| <a id="rule-gp-02"></a>GP-02 | **Reconciliation is scoped, not a blanket resync.** A `sync.changed` gap pulls the change feed from the last cursor; a `task` gap re-reads that task. |
| <a id="rule-gp-03"></a>GP-03 | **Reconnection reconciles unconditionally**, because the client cannot know what it missed while disconnected. |
| <a id="rule-gp-04"></a>GP-04 | **Convergence is verifiable** — after reconciliation, client and server state compare equal for the subscription's scope ([WP-24.03](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.03)). |
| GP-05 | **Out-of-order and duplicate delivery cause no corruption**, because application is idempotent by `(aggregateKind, aggregateId, aggregateRev)`. |

---

## 4. Degradation

| Condition | Behaviour |
|---|---|
| Realtime unavailable | Poll authoritative state at a bounded interval; **degradation is visible** ([WP-24.05](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.05)) |
| Realtime flapping | Exponential backoff with jitter; no reconnect storm ([WP-24.00](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.00)) |
| Cloud fully unavailable | Client reports which capabilities are unavailable with reasons; **never blanks** ([OR-02](../10-web-architecture.md#rule-or-02)) |
| Subscription refused | Named reason; the client does not silently retry a permission failure |

---

## 5. The durable tool bridge

**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** forbids Cloud from connecting to a device. The bridge is therefore pull-and-answer, and its shape is a direct consequence of that decision rather than a preference.

```
Remote surface (mobile / web)
   │  task.create  (origin_surface = mobile | web)   ── provenance only, not authority
   ▼
Cloud owns the Task; the Cloud plan decides locality per Step
   │  plan_step.tool_locality = device, target_device_id   ── declared, never inferred
   ▼
Cloud ── writes task.tool_request (durable, expiring) ──▶ queue
   │
   │  realtime: bridge.requestAvailable { count }        ── a hint only
   ▼
ArcChat Desktop
   │  bridge.pullRequests                                ── the desktop initiates
   ▼
LOCAL RE-AUTHORIZATION  ── local policy, local registry, local grants, local actor chain
   │        │
   │        └── refused → bridge.submitResult { refused, reasonCode }
   ▼
Local capability invocation (ICapabilityProvider.InvokeAsync)
   ▼
bridge.submitResult { outcome, resultRev }               ── idempotent on (taskId, attemptId)
   ▼
Cloud updates the task; realtime hints the requester; the requester re-reads
```

### 5.1 The request

| Field | Notes |
|---|---|
| `toolRequestId`, `taskId`, `attemptId` | |
| `targetDeviceId` | |
| `capabilityKey` | What is being asked for |
| `arguments` | Structured value; **bounded** — large data crosses by reference |
| `frozenContext` | Frozen at creation |
| `actorChain` | Who is asking, through what |
| `cloudApprovalToken?` | **Evidence, not authority** |
| `expiresAt` | |
| `state` | `queued` \| `delivered` \| `answered` \| `expired` \| `refused` |

### 5.2 Local re-authorization — the central control

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **The desktop re-evaluates every request against local policy, the local capability registry, local permission grants and the local actor chain** ([WP-26.02](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.02)). |
| BR-02 | **A cloud-approved request may still be refused locally**, and the refusal reason is returned rather than swallowed. |
| BR-03 | **A `cloudApprovalToken` is never sufficient.** It is one input to the local decision. |
| BR-04 | **An operation requiring local presence cannot be satisfied through the bridge** ([AZ-01](00-operation-catalogue.md#rule-az-01)), because the requester is by definition not present. |
| BR-05 | **The bridge never bypasses owner-side validation.** The desktop still calls `ICapabilityProvider.InvokeAsync`, which validates again. |

### 5.3 Idempotency and lost answers

| # | Rule |
|---|---|
| BI-01 | **`bridge.submitResult` is idempotent on `(taskId, attemptId)`.** Re-submission after a lost response has one effect ([WP-26.03](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03)). |
| <a id="rule-bi-02"></a>BI-02 | **A request delivered but unanswered before a desktop crash is re-delivered** on the next pull, and the local command log makes re-execution a no-op if it already ran (`§1.2` of the desktop data model). |
| <a id="rule-bi-03"></a>BI-03 | **This is the one place where local and cloud idempotency must agree**: the desktop's `command_log` and Cloud's `attempt` row both key on the same `CommandId`. A mismatch here is the defect class most likely to cause a duplicate real-world effect, and [WP-26.03](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) tests it specifically. |
| <a id="rule-bi-04"></a>BI-04 | **An expired request closes with a typed reason**, never ambiguously ([WP-26.05](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.05)). |
| <a id="rule-bi-05"></a>BI-05 | **An offline target queues visibly** with its expiry shown to the requester ([WP-26.05](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.05)). |

### 5.4 Effect certainty across the bridge

| Failure | Effect certainty | Auto-retry? |
|---|---|---|
| Request never delivered — target offline until expiry | Did not happen | Yes, on a new request |
| Delivered, refused locally | Did not happen | No — the refusal is the answer |
| Delivered, executed, result lost in transit | **Unknown** | Yes **only if** the capability is idempotent |
| Delivered, desktop crashed mid-execution | **Unknown** | Resolved by the local command log on re-delivery |
| Answered, cloud failed to record | Happened | Yes — re-submission is idempotent |

| # | Rule |
|---|---|
| <a id="rule-be-01"></a>BE-01 | **An `unknown` effect on a non-idempotent capability surfaces a decision** rather than retrying ([WP-16.02](../../planning/work-packages/16-unified-execution-engine.md#rule-wp-16.02)). |
| BE-02 | **The command log resolves most `unknown` cases automatically**, which is why it is written in the same transaction as the effect. |

---

## 6. What the bridge is not

| Not | Why |
|---|---|
| A tunnel | Cloud never opens a connection to a device (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**) |
| A relay | No payload body flows through it; large data crosses by reference |
| Synchronous | Every request is durable and may be answered minutes later |
| An authorization channel | Local re-authorization is mandatory and final ([BR-01](#rule-br-01)) |
| A discovery mechanism | The requester names a device from `device.list`; there is no scanning |

---

### 6.1 Browser adapter

The browser uses the official SignalR JavaScript client with DTOs, event names and runtime validators generated from C#-exported JSON Schema. C# clients retain their AOT-aware implementation; both run the same sequence/duplicate/reconnect/backfill conformance vectors. Browser transport uses same-origin cookies, WebSocket Origin checks, WebSockets-only and skipNegotiation, never an access token in a query URL. Upgrade failure uses bounded authoritative HTTP polling, not SignalR long polling; periodic catch-up covers a wakeup emitted on another replica. No replica affinity or backplane is required for browser correctness. The Task stream keeps byte offsets and bounded buffers; JavaScript UTF-16 string length is not a cursor. See [Web realtime rules](../25-web-toolchain-and-sdk.md#32-realtime-and-streaming).

---

## 7. Verification

| # | Obligation | Where |
|---|---|---|
| RV-01 | Every induced gap is detected, recorded, and reconciled to verified convergence | [WP-24.02](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.02), [WP-24.03](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.03) |
| RV-02 | Duplicate and out-of-order delivery cause no corruption | [WP-24.02](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.02) |
| RV-03 | Permission loss stops delivery immediately | [WP-24.01](../../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24.01) |
| RV-04 | No event payload carries authoritative state or a body | Contract policy test |
| <a id="rule-rv-05"></a>RV-05 | **No cloud-initiated connection to a device exists anywhere**, verified structurally and by runtime network observation | [WP-26.01](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.01), [WP-31.06](../../planning/work-packages/31-arcchat-mobile-android.md#rule-wp-31.06) |
| RV-06 | A cloud-approved request is still refused when local policy denies it | [WP-26.02](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.02) |
| RV-07 | One request produces one effect under duplicate delivery, lost result and mid-execution crash | [WP-26.03](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.03) |
| RV-08 | A local-presence operation cannot be completed through the bridge | [WP-26.04](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.04) |
| RV-09 | An offline target queues visibly and expires with a typed reason | [WP-26.05](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.05) |
