<a id="rule-wp-24"></a>

# WP-24 — Realtime, Reliable Events and Recovery

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `23` · Downstream: `25`, `26`, `30`

> **Goal.** Deliver realtime updates that are useful without ever being authoritative: connect, subscribe, deliver, detect a gap, and backfill authoritative state over HTTP — with disconnected compensation recovery proven, because it is the case that actually happens.

---

## 1. Scope and purpose

**In scope.** The realtime transport and its protocol; connection lifecycle and authentication; subscription scoping; sequence numbering and gap detection; HTTP snapshot backfill; delivery guarantees and their honest limits; fan-out and scaling posture; and the client-side reconnection behaviour shared by desktop, web and mobile.

**Out of scope.** What is delivered over it — sync change notifications (`25`), task progress (`26`), entitlement changes (`42`), policy updates (`44`). Realtime is a channel, not a feature.

**Why this package exists.** `I2 §III.6` requires HTTP snapshot, sequence gap and disconnected compensation recovery in the first real server version. A realtime channel whose recovery path is untested becomes a silent data-divergence engine.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) `§7`, `§8` | Realtime and reliable event rules, including [RL-04](../../architecture/05-cloud-architecture.md#rule-rl-04) backfill |
| [`../../requirements/products/arcforges-cloud.md`](../../requirements/products/arcforges-cloud.md) `§7` | Resilience and degradation posture |
| **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)** | Realtime under AOT is supported; the stale corpus claim is corrected |
| [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) output | The HTTP surface backfill uses |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Realtime carries only realtime updates.** All commands and queries go over HTTP ([NW-01](../../architecture/11-mobile-architecture.md#rule-nw-01) in the mobile architecture). |
| <a id="rule-br-02"></a>BR-02 | **A realtime message is a hint, never authority.** A client needing full fidelity re-reads authoritative state ([RL-04](../../architecture/05-cloud-architecture.md#rule-rl-04)). |
| BR-03 | **Every message carries a sequence number** scoped to its subscription, so a gap is detectable. |
| BR-04 | **A detected gap triggers HTTP backfill**, never a silent resync that hides the gap. |
| BR-05 | **Object bodies never travel over realtime** (`I3 §14.3`). |
| BR-06 | **Subscriptions are permission-scoped at subscribe and re-checked on change**, so a permission loss stops delivery. |
| BR-07 | **Delivery guarantees are stated honestly**: at-most-once delivery with gap detection plus authoritative backfill, not exactly-once delivery. |
| BR-08 | **Realtime loss degrades to polling**, and the degradation is visible to the user. |
| BR-09 | **Transport logs redact tokens** ([WB-08](../../architecture/08-security-architecture.md#rule-wb-08) in the security architecture). |
| BR-10 | **The client works under a published Native AOT binary** with source-generated payload metadata (**[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Realtime/` | Hubs, connection lifecycle, subscription registry, sequence assignment, fan-out |
| `src/Cloud/ArcForges.Cloud.Modules.*/` | Publish through the reliable event path rather than directly to connections |
| `src/BuildingBlocks/ArcForges.CloudClient.Realtime/` | Shared client: connect, subscribe, gap detect, backfill, reconnect with backoff |
| `src/Contracts/Public/ArcForges.Contracts.Realtime/` | Realtime payloads with source-generated metadata |
| `tests/RealtimeReconnectTests/` | Connection, gap, backfill, permission-revocation and scale suites |

**Major types introduced.** `RealtimeConnection`, `Subscription`, `SubscriptionScope`, `SequencedMessage`, `GapDetection`, `BackfillRequest`, `ReconnectPolicy`, `DeliveryState`.

---

## 5. Required implementation work

<a id="rule-wp-24.00"></a>

### WP-24.00 — Connection lifecycle and authentication

**What must be fully done.** Connection with the same identity and tenancy resolution as HTTP. A session revocation terminates the connection. Reconnection uses exponential backoff with jitter. Connection state is visible to the user.

**Testing requirements.** Authentication failure paths; revocation-terminates-connection; backoff distribution under mass reconnect; a token-redaction assertion in transport logs.

**Completion gate.** Session revocation terminates the connection promptly, mass reconnection does not synchronise, and no token appears in transport logs.

<a id="rule-wp-24.01"></a>

### WP-24.01 — Subscriptions and permission

**What must be fully done.** Subscriptions scoped to workspace, resource or task, checked at subscribe and re-checked when permission changes. Losing permission stops delivery immediately and informs the client.

**Testing requirements.** Subscribe-refusal tests; a mid-stream permission revocation test; a scope-escape attempt test.

**Completion gate.** Permission loss stops delivery immediately, and no subscription can escape its scope.

<a id="rule-wp-24.02"></a>

### WP-24.02 — Sequencing and gap detection

**What must be fully done.** Every message carries a subscription-scoped sequence number. The client detects a gap deterministically and records it. A gap is never silently ignored, and a duplicate is discarded idempotently.

**Testing requirements.** Induced-gap detection; duplicate delivery; out-of-order delivery; a counter assertion that gaps are recorded as telemetry.

**Completion gate.** Every induced gap is detected and recorded; duplicates and out-of-order messages are handled without corruption.

<a id="rule-wp-24.03"></a>

### WP-24.03 — HTTP backfill

**What must be fully done.** On a detected gap, or on reconnection, the client queries authoritative state over HTTP from its last known sequence and revision, converging without a full resynchronisation where a scoped query suffices. Convergence is verifiable.

**Testing requirements.** Backfill after a gap, after a long disconnection, and after a server restart; a convergence assertion comparing client and server state.

**Completion gate.** After any gap or disconnection, the client converges to authoritative state, verified by comparison.

<a id="rule-wp-24.04"></a>

### WP-24.04 — Reliable event publication

**What must be fully done.** Modules publish through the outbox so a state change and its notification cannot diverge. Realtime fan-out consumes published events; a fan-out failure never rolls back the state change, and the missed notification is recoverable by backfill.

**Testing requirements.** A divergence test with fan-out failing; an ordering test per subscription; a load test on fan-out.

**Completion gate.** A fan-out failure never loses the state change, and the client still converges through backfill.

<a id="rule-wp-24.05"></a>

### WP-24.05 — Degradation and offline behaviour

**What must be fully done.** Realtime loss degrades to polling authoritative state at a bounded interval, with the degraded state visible. A cloud outage does not blank any client; capabilities report unavailability with reasons.

**Testing requirements.** Realtime-down polling test; a visibility test asserting the user is told; a full-outage test asserting no client blanks.

**Completion gate.** Realtime loss degrades to visible polling, and a full outage never blanks a client.

<a id="rule-wp-24.06"></a>

### WP-24.06 — AOT and cross-surface client

**What must be fully done.** One shared client used by desktop, web and later mobile, using source-generated payload metadata, working from a published Native AOT binary and a WebAssembly host.

**Testing requirements.** Published-AOT and WebAssembly connection tests; a shared-implementation assertion that no surface has its own divergent client.

**Completion gate.** One client implementation serves every surface and works from published AOT and WebAssembly hosts.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Sequence assignment and the outbox feed realtime |
| Protocol | The realtime protocol and its payload contracts |
| UI | Connection state, degradation indicators and live updates |
| Security | Subscription permission, revocation propagation and token redaction |
| Platform | Realtime verified under AOT and WebAssembly |
| Migration | Realtime payload versioning enters the compatibility window |
| Compatibility | The sequence and backfill contract clients depend on |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Revocation, backoff distribution and redaction results | [WP-24.00](#rule-wp-24.00) |
| Subscription permission and scope-escape results | [WP-24.01](#rule-wp-24.01) |
| Gap, duplicate and out-of-order handling results | [WP-24.02](#rule-wp-24.02) |
| Backfill convergence comparisons | [WP-24.03](#rule-wp-24.03) |
| Fan-out failure divergence results | [WP-24.04](#rule-wp-24.04) |
| Degradation and outage visibility results | [WP-24.05](#rule-wp-24.05) |
| Published-AOT and WebAssembly client results | [WP-24.06](#rule-wp-24.06) |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Session revocation terminates the connection promptly; mass reconnection does not synchronise; no token appears in transport logs.
2. Permission loss stops delivery immediately; no subscription escapes its scope.
3. Every induced gap is detected and recorded; duplicates and out-of-order messages cause no corruption.
4. **After any gap, disconnection or server restart the client converges to authoritative state, verified by comparison.**
5. A fan-out failure never loses the underlying state change, and the client still converges through backfill.
6. Realtime loss degrades to visible polling; a full cloud outage never blanks a client.
7. One shared client implementation works from a published Native AOT binary and a WebAssembly host.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [23 — Public API Surface and Generated Clients](23-public-api-and-generated-clients.md)

**Downstream — these consume this package’s completed output.**

- [25 — Sync Engine and Blob Lifecycle](25-sync-engine-and-blob-lifecycle.md)
- [26 — Device Presence, Remote Action and the Tool Bridge](26-remote-action-and-tool-bridge.md)
- [30 — Mobile Shared Architecture and the Apache Boundary](30-mobile-shared-architecture.md)
