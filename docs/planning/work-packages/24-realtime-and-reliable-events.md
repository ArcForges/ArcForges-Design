<a id="rule-wp-24"></a>

# WP-24 — Bounded Hints and Reliable Events

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `23` · Downstream: `25`, `26`, `30`

> **Goal.** Deliver realtime updates that are useful without ever being authoritative: connect, subscribe, deliver, detect a gap, and backfill authoritative state over HTTP — with disconnected compensation recovery proven, because it is the case that actually happens.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud; clients; AI stream contract. Inputs: the assigned exact Contracts packages/descriptors and actual provider artifacts; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The realtime transport and its protocol; connection lifecycle and authentication; subscription scoping; sequence numbering and gap detection; HTTP snapshot backfill; delivery guarantees and their honest limits; fan-out and scaling posture; and the client-side reconnection behaviour shared by desktop, web and mobile.

**Out of scope.** What is delivered over it — sync change notifications (`25`), task progress (`26`), entitlement changes (`42`), policy updates (`44`). Realtime is a channel, not a feature.

**Why this package exists.** The [realtime and bridge contract](../../architecture/contracts/03-realtime-and-bridge.md) requires HTTP snapshot, sequence gap and disconnected compensation recovery in the first real server version. A realtime channel whose recovery path is untested becomes a silent data-divergence engine.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) `§7`, `§8` | Realtime and reliable event rules, including [RL-04](../../architecture/05-cloud-architecture.md#rule-rl-04) backfill |
| [`../../requirements/products/arcforges-cloud.md`](../../requirements/products/arcforges-cloud.md) `§7` | Resilience and degradation posture |
| **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)** | Realtime under AOT is supported; the stale corpus claim is corrected |
| [WP-23](23-public-api-and-generated-clients.md#rule-wp-23) output | The HTTP surface backfill uses |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Realtime carries only realtime updates.** All commands and queries go over HTTP ([NW-01](../../architecture/11-mobile-architecture.md#rule-nw-01) in the mobile architecture). |
| <a id="rule-br-02"></a>BR-02 | **A realtime message is a hint, never authority.** A client needing full fidelity re-reads authoritative state ([RL-04](../../architecture/05-cloud-architecture.md#rule-rl-04)). |
| BR-03 | **Every message carries a sequence number** scoped to its subscription, so a gap is detectable. |
| BR-04 | **A detected gap triggers HTTP backfill**, never a silent resync that hides the gap. |
| BR-05 | **Object bodies never travel over realtime**. |
| BR-06 | **Subscriptions are permission-scoped at subscribe and re-checked on change**, so a permission loss stops delivery. |
| BR-07 | **Delivery guarantees are stated honestly**: at-most-once delivery with gap detection plus authoritative backfill, not exactly-once delivery. |
| BR-08 | **Realtime loss degrades to polling**, and the degradation is visible to the user. |
| BR-09 | **Transport logs redact tokens** ([WB-08](../../architecture/08-security-architecture.md#rule-wb-08) in the security architecture). |
| BR-10 | **The client works under a published Native AOT binary** with generated protobuf payload types (**[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). |

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


**What must be fully done.** Implement EventService.Poll through the ordinary auth/scope pipeline; each call is bounded and reauthorizes. Clients display polling/reconnecting state, suspend background mobile polling and use the selected jitter/backoff profile. CF live presentation has the separate session-binding/first-frame nonce protocol.

**Testing requirements.** Real native/Web/RN session expiry/revoke/Origin and request cancellation; no SignalR negotiation or bearer URL.

**Completion gate.** Hint polling and optional live presentation use their exact authenticated boundaries.

<a id="rule-wp-24.01"></a>

### WP-24.01 — Subscriptions and permission


**What must be fully done.** Implement the catalogue allowlist of event/scope kinds. Initial empty cursor returns an empty hint page, current scoped cursor and resetRequired; the client then reads authorized owner snapshots before continuing; scope/session change discards it. Every next page rechecks current permission; unsupported scope refuses rather than expanding subscription.

**Testing requirements.** Wrong workspace/device/task scope, mid-page revocation and first-call/reset behavior.

**Completion gate.** No hint or snapshot crosses an unauthorized scope and initialization is unambiguous.

<a id="rule-wp-24.02"></a>

### WP-24.02 — Sequencing and gap detection


**What must be fully done.** Persist the selected 24-hour/10000-row per-scope hint log, allocate monotonic sequence under row lock in the same publication transaction and return bounded pages. Duplicates are harmless; expired/lost cursor yields explicit reset to authoritative snapshot.

**Testing requirements.** Concurrent writers, crash before/after commit, duplicate pages, retention expiry and out-of-order client delivery.

**Completion gate.** No permanently skipped committed hint; loss never implies lost business state.

<a id="rule-wp-24.03"></a>

### WP-24.03 — HTTP backfill


**What must be fully done.** Implement client snapshot/read reconciliation through generated owner RPCs. A reset/backlog or permission change invalidates affected projections; chat/task final state comes from C#, while CF catch-up may report completed/truncated/superseded/evicted stream presentation separately.

**Testing requirements.** Long disconnect/cursor expiry/stream eviction and final-message replacement on all selected clients.

**Completion gate.** Clients converge to canonical owner state without inferring task outcome from stream completion.

<a id="rule-wp-24.04"></a>

### WP-24.04 — Reliable event publication


**What must be fully done.** Publish hint rows from committed owner outbox events with inbox dedup and bounded fan-out. Keep Task/Chat/Sync data canonical in PostgreSQL; CF DO retains only disposable stream tails and markers.

**Testing requirements.** Publication crash/duplicate/DO loss and database restore recovery; authoritative reads survive missing presentation.

**Completion gate.** A missed hint or discarded CF projection never rolls back or substitutes for an owner transaction.

<a id="rule-wp-24.05"></a>

### WP-24.05 — Degradation and offline behaviour


**What must be fully done.** Use the selected Poll intervals (active Task/bridge 2s, ordinary foreground 15s, idle 60s, 20% jitter and failure backoff capped30s) and bounded page sizes. Distinguish offline/denied/cursor-reset; no busy retry or blanking authorized local work.

**Testing requirements.** Network outage, rate-limit/retry guidance, foreground/background and degraded partial capability tests.

**Completion gate.** Polling and recovery are bounded and visible on each runtime.

<a id="rule-wp-24.06"></a>

### WP-24.06 — C# and TypeScript realtime adapters


**What must be fully done.** Publish event/poll DTOs from Contracts and compose one native C# consumer and TS browser/RN adapters against their respective transports. Apply browser cookie/CSRF and native secure bearer rules; CF socket uses first-frame nonce plus C# authorization for every frame/range.

**Testing requirements.** Common event/exact-value vectors plus actual AOT/React/RN polling and CF stream interruption/revocation tests.

**Completion gate.** All consumers agree on hint versus canonical state and preserve stream byte/cursor semantics.

<a id="rule-wp-24.90"></a>
### WP-24.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Replace retired SignalR scaffolding using the fixed hint/read transports and cursor/snapshot recovery. Separate durable C# facts from CF live stream projections. Implement bounded reconnect/expiry and per-client supported call shapes.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Lost, duplicated, reordered or expired hints converge through authoritative reads. Real full AI stream completion is asserted only after [WP-52](52-cloud-harness.md#rule-wp-52), not by an event fixture.

**Completion gate.** Lost, duplicated, reordered or expired hints converge through authoritative reads. Real full AI stream completion is asserted only after [WP-52](52-cloud-harness.md#rule-wp-52), not by an event fixture. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Sequence assignment and the outbox feed realtime |
| Protocol | The realtime protocol and its payload contracts |
| UI | Connection state, degradation indicators and live updates |
| Security | Subscription permission, revocation propagation and token redaction |
| Platform | Realtime verified under AOT and React browser |
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
| Published-AOT and React browser client results | [WP-24.06](#rule-wp-24.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-24.90](#rule-wp-24.90) and all inherited domain-specific gates must pass on the same candidate closure. Lost, duplicated, reordered or expired hints converge through authoritative reads. Real full AI stream completion is asserted only after [WP-52](52-cloud-harness.md#rule-wp-52), not by an event fixture.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-24.06](#rule-wp-24.06) — Real browser realtime loss/reconnect/polling convergence with correct session and byte-cursor handling. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. Session revocation terminates the connection promptly; mass reconnection does not synchronise; no token appears in transport logs.
2. Permission loss stops delivery immediately; no subscription escapes its scope.
3. Every induced gap is detected and recorded; duplicates and out-of-order messages cause no corruption.
4. **After any gap, disconnection or server restart the client converges to authoritative state, verified by comparison.**
5. A fan-out failure never loses the underlying state change, and the client still converges through backfill.
6. Realtime loss degrades to visible polling; a full cloud outage never blanks a client.
7. C# and TypeScript realtime adapters pass the shared real-server recovery matrix with generated event contracts and their correct authentication boundaries.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [23 public api and generated clients](23-public-api-and-generated-clients.md#rule-wp-23)

**Downstream — consumers of these released outputs.**

- [25 sync engine and blob lifecycle](25-sync-engine-and-blob-lifecycle.md#rule-wp-25)
- [26 remote action and tool bridge](26-remote-action-and-tool-bridge.md#rule-wp-26)
- [30 mobile shared architecture](30-mobile-shared-architecture.md#rule-wp-30)

---
