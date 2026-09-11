<a id="rule-wp-08"></a>

# WP-08 — Local gRPC and Registration

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Upstream: `06`, `07` · Downstream: `09`, `11`, `13`, `14`

> **Goal.** Make the local plane real: a transport per platform, an endpoint manifest, a registration lifecycle with leases and heartbeats, routing, health, backpressure and reconnection — all working between genuinely AOT-published processes.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform mechanisms; ArcChat Hub; each provider. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The local RPC transport implementation, the endpoint manifest and discovery, registration and lease lifecycle, the connection manager, routing, health and backpressure, disconnection and reconnection, local transport security, and the large-data escape path.

**Out of scope.** The capability semantics carried over the transport (`09`). The Hub's product behaviour (`14`). Any cloud path.

**Why this package exists.** [SQ-03](../implementation-sequence.md#rule-sq-03) allows external vendors to be mocked but never architectural boundaries. Local IPC is the most important such boundary: ArcChat is a control plane and never a mandatory data gateway (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**), and every professional product must work with ArcChat absent.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/03-local-ipc-and-process-model.md`](../../architecture/03-local-ipc-and-process-model.md) | Transport, manifest, registration, routing, health, backpressure, reconnection and security rules |
| [`../../architecture/00-architecture-overview.md`](../../architecture/00-architecture-overview.md) `§3` | The three communication responsibilities and the four data paths |
| **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** | ArcChat as control plane, never a mandatory data gateway; Cloud never connects to a local endpoint |
| [WP-06.01](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.01) output | Proven bidirectional RPC between published AOT binaries |
| [WP-07](07-local-persistence-foundation.md#rule-wp-07) output | Durable state behind the RPC surface |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Named pipe on Windows, Unix domain socket elsewhere**, access-controlled to the current user, never a network endpoint. |
| BR-02 | **A professional product must start, work and save with ArcChat absent** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). Registration failure degrades ecosystem features only. |
| <a id="rule-br-03"></a>BR-03 | **The Hub is a coordinator, not a data relay.** Large data never traverses it ([BF-05](../../architecture/12-native-interop-and-media.md#rule-bf-05) in the native architecture). |
| BR-04 | **Cloud never connects to localhost, a named pipe, a domain socket or local standard I/O** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |
| BR-05 | **Registration is leased with heartbeats**; a lease expires rather than leaking a dead endpoint. |
| BR-06 | **Re-registration after Hub restart is automatic and idempotent.** |
| BR-07 | **Backpressure is explicit**: a saturated consumer blocks, sheds with a recorded reason, or fails — never grows unbounded. |
| BR-08 | **Reflection convenience paths are prohibited** in target registration and proxy construction. |
| <a id="rule-br-09"></a>BR-09 | **Every RPC method is task-returning and cancellation-aware.** |
| <a id="rule-br-10"></a>BR-10 | **Large payloads use a resource reference plus a controlled channel**, never an inline body. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/BuildingBlocks/ArcForges.LocalRpc/` | Created: transport, connection manager, registration client, health and backpressure |
| `src/ArcChat/ArcChat.LocalHub/` | The Hub's registry, routing and lifecycle (product behaviour lands in `14`) |
| `src/*/[Product].LocalRpc/` | Per-product adapter: hosts the product's contracts and consumes others' |
| `%LocalAppData%`-equivalent endpoint manifest location | The manifest format and its per-platform location |
| `tests/LocalRpcAotTests/` | Extended to the full lifecycle matrix |
| `tests/RemoteToolBridgeTests/` | Seeded — the remote bridge lands in `26` |

**Major types introduced.** `EndpointManifest`, `EndpointDescriptor`, `RegistrationLease`, `ConnectionManager`, `RpcConnection`, `HealthReport`, `BackpressureState`, `TransferChannel`.

---

## 5. Required implementation work

<a id="rule-wp-08.00"></a>

### WP-08.00 — Transport and framing


**What must be fully done.** Implement Kestrel HTTP/2 over named pipes on Windows and UDS elsewhere, explicit generated gRPC registration and ConnectCallback clients. Apply owner-only ACL/peer OS identity and the selected LocalBootstrap nonce/epoch binding before ordinary methods. Use protobuf wire framing only; readable diagnostics are logs, never an alternate accepted protocol.

**Testing requirements.** Actual AOT processes on each OS: foreign-user/forged-manifest/expired-nonce/malformed-frame and size-limit failures.

**Completion gate.** The selected OS-authenticated local transport works with no public TCP listener or text fallback.

<a id="rule-wp-08.01"></a>

### WP-08.01 — Endpoint manifest and discovery

**What must be fully done.** The manifest records live endpoints with their identity, transport address, contract set and version. It is written atomically, is readable while being written, and self-heals when it contains a stale entry. Discovery never scans a network.

**Testing requirements.** Concurrent read-write tests; a stale-entry self-heal test; a negative test asserting no network discovery occurs.

**Completion gate.** Discovery is local-only, concurrent-safe and self-healing.

<a id="rule-wp-08.02"></a>

### WP-08.02 — Registration lifecycle


**What must be fully done.** Implement registration lease 30 seconds, renewal 10 seconds and generation/epoch fencing from the IPC contract. Publish/remove endpoint manifests atomically, expire dead registrations and re-register idempotently after Hub restart; products start and save with Hub absent.

**Testing requirements.** Restart both sides at registration/renewal/expiry boundaries; stale callback and duplicate registration; Hub-absent product persistence.

**Completion gate.** No dead endpoint or stale generation remains eligible and Hub loss cannot block local product work.

<a id="rule-wp-08.03"></a>

### WP-08.03 — Routing and versioning

**What must be fully done.** Routing resolves a call to a registered endpoint by contract and version, with the fixed routing priority of the contract architecture. Version negotiation happens at connect; an unsatisfiable version produces a clean, explained refusal.

**Testing requirements.** Routing priority tests; version negotiation matrix including refusal.

**Completion gate.** Routing follows the fixed priority and version mismatch refuses cleanly.

<a id="rule-wp-08.04"></a>

### WP-08.04 — Health, backpressure and concurrency


**What must be fully done.** Enforce the selected 16 active/64 queued call limits, deadlines and declared capability ordering/conflict rules. Use separate owned listeners for bidirectional calls; never hold a synchronous callback waiting on the same saturated lane. Emit five-dimension health and typed overload reason.

**Testing requirements.** Saturation/bounded-memory, cross-direction cancellation/deadlock and priority/order tests against published peers.

**Completion gate.** Queue/call/memory limits and failure behavior match the fixed local profile.

<a id="rule-wp-08.05"></a>

### WP-08.05 — Disconnection, cancellation and reconnection

**What must be fully done.** Disconnection produces a typed failure with effect certainty for every in-flight call. Cancellation propagates across the boundary. Reconnection is automatic with backoff, and in-flight work is either resumed by idempotency or reported as unknown-effect.

**Testing requirements.** Fault-injection tests: mid-call disconnect, slow peer, half-open connection, and peer restart.

**Completion gate.** Every fault produces a typed outcome with correct effect certainty, and no call hangs indefinitely.

<a id="rule-wp-08.06"></a>

### WP-08.06 — Large-data path


**What must be fully done.** Implement LocalTransferTicket, BeginTransfer/ReadChunk/OpenRead/GetJob with immutable ResourceVersionRef, offset/hash/range, expiry, cancellation and selected bounds. Transfer directly between authorized owning peers; Hub only routes references.

**Testing requirements.** Interrupted/resumed read, wrong owner/version/hash, expired ticket, oversized inline body and unauthorized range.

**Completion gate.** Large data remains owner-scoped, verifiable and resumable without entering Hub control payloads.

<a id="rule-wp-08.90"></a>
### WP-08.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Replace retired IPC scaffolding using the fixed local gRPC Named Pipe/UDS design. Preserve first-party discovery, ACL/identity, leases, protocol negotiation, bounded queues/calls and registration cleanup. Hub remains in ArcChat.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Actual AOT process-to-process tests cover registration, expiry, incompatible peers, backpressure, cancellation and malformed/unauthorized calls; no public TCP listener is required.

**Completion gate.** Actual AOT process-to-process tests cover registration, expiry, incompatible peers, backpressure, cancellation and malformed/unauthorized calls; no public TCP listener is required. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None directly; durable state sits behind the RPC surface |
| Protocol | This package *is* the local protocol implementation |
| UI | Connection and health states become surfaceable in the shell |
| Security | Local transport access control, peer identity and the prohibition on network exposure |
| Platform | Per-platform transport and manifest location |
| Migration | Contract version negotiation at connect |
| Compatibility | The local contract version window becomes enforced at runtime |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Cross-platform transport and access-control results | [WP-08.00](#rule-wp-08.00) |
| Manifest concurrency and self-heal results | [WP-08.01](#rule-wp-08.01) |
| Lifecycle matrix: restart, crash, absent Hub, double registration | [WP-08.02](#rule-wp-08.02) |
| Routing priority and version negotiation matrix | [WP-08.03](#rule-wp-08.03) |
| Saturation, ordering and deadlock results | [WP-08.04](#rule-wp-08.04) |
| Fault-injection outcomes with effect certainty | [WP-08.05](#rule-wp-08.05) |
| Large-transfer results and the Hub no-body assertion | [WP-08.06](#rule-wp-08.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-08.90](#rule-wp-08.90) and all inherited domain-specific gates must pass on the same candidate closure. Actual AOT process-to-process tests cover registration, expiry, incompatible peers, backpressure, cancellation and malformed/unauthorized calls; no public TCP listener is required.

**All of the following, with recorded evidence, between genuinely AOT-published binaries:**

1. The transport works on every desktop platform and rejects a foreign-user connection.
2. Discovery is local-only, concurrent-safe and self-healing; no network scan occurs.
3. A provider survives a Hub restart; a dead provider's lease expires; a product starts, works and saves with no Hub present.
4. Routing follows the fixed priority and version mismatch refuses cleanly with an explanation.
5. Saturation is bounded and observable; bidirectional calls cannot deadlock.
6. Every injected fault produces a typed outcome with correct effect certainty; no call hangs.
7. Large transfers resume after interruption, and the Hub carries no payload body.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)
- [WP-07](07-local-persistence-foundation.md#rule-wp-07)

**Downstream — consumers of these released outputs.**

- [WP-09](09-capability-contribution-and-resource-model.md#rule-wp-09)
- [WP-11](11-security-foundation.md#rule-wp-11)
- [WP-13](13-high-risk-technical-probes.md#rule-wp-13)
- [WP-14](14-hub-and-minimal-provider-slice.md#rule-wp-14)


---
