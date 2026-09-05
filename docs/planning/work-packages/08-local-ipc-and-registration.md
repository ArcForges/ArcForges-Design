# WP-08 — Local IPC Transport and Registration Lifecycle

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Upstream: `06`, `07` · Downstream: `09`, `11`, `13`, `14`

> **Goal.** Make the local plane real: a transport per platform, an endpoint manifest, a registration lifecycle with leases and heartbeats, routing, health, backpressure and reconnection — all working between genuinely AOT-published processes.

---

## 1. Scope and purpose

**In scope.** The local RPC transport implementation, the endpoint manifest and discovery, registration and lease lifecycle, the connection manager, routing, health and backpressure, disconnection and reconnection, local transport security, and the large-data escape path.

**Out of scope.** The capability semantics carried over the transport (`09`). The Hub's product behaviour (`14`). Any cloud path.

**Why this package exists.** `SQ-03` allows external vendors to be mocked but never architectural boundaries. Local IPC is the most important such boundary: ArcChat is a control plane and never a mandatory data gateway (**D-010**), and every professional product must work with ArcChat absent.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/03-local-ipc-and-process-model.md`](../../architecture/03-local-ipc-and-process-model.md) | Transport, manifest, registration, routing, health, backpressure, reconnection and security rules |
| [`../../architecture/00-architecture-overview.md`](../../architecture/00-architecture-overview.md) `§3` | The three communication responsibilities and the four data paths |
| **D-010** | ArcChat as control plane, never a mandatory data gateway; Cloud never connects to a local endpoint |
| `WP-06.01` output | Proven bidirectional RPC between published AOT binaries |
| `WP-07` output | Durable state behind the RPC surface |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Named pipe on Windows, Unix domain socket elsewhere**, access-controlled to the current user, never a network endpoint. |
| BR-02 | **A professional product must start, work and save with ArcChat absent** (**D-010**). Registration failure degrades ecosystem features only. |
| BR-03 | **The Hub is a coordinator, not a data relay.** Large data never traverses it (`BF-05` in the native architecture). |
| BR-04 | **Cloud never connects to localhost, a named pipe, a domain socket or local standard I/O** (**D-010**). |
| BR-05 | **Registration is leased with heartbeats**; a lease expires rather than leaking a dead endpoint. |
| BR-06 | **Re-registration after Hub restart is automatic and idempotent.** |
| BR-07 | **Backpressure is explicit**: a saturated consumer blocks, sheds with a recorded reason, or fails — never grows unbounded. |
| BR-08 | **Reflection convenience paths are prohibited** in target registration and proxy construction (`I3 §6.8`). |
| BR-09 | **Every RPC method is task-returning and cancellation-aware.** |
| BR-10 | **Large payloads use a resource reference plus a controlled channel**, never an inline body. |

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

### WP-08.00 — Transport and framing

**What must be fully done.** The per-platform transport with correct access control, message framing, the binary formatter with generated shapes, and a text-format fallback where diagnostics require it. Connection setup verifies the peer is the same user.

**Testing requirements.** Cross-platform transport tests; a framing test with maximum-size and malformed messages; an access-control test asserting another user cannot connect.

**Completion gate.** The transport works on every desktop platform and rejects a foreign-user connection.

### WP-08.01 — Endpoint manifest and discovery

**What must be fully done.** The manifest records live endpoints with their identity, transport address, contract set and version. It is written atomically, is readable while being written, and self-heals when it contains a stale entry. Discovery never scans a network.

**Testing requirements.** Concurrent read-write tests; a stale-entry self-heal test; a negative test asserting no network discovery occurs.

**Completion gate.** Discovery is local-only, concurrent-safe and self-healing.

### WP-08.02 — Registration lifecycle

**What must be fully done.** Registration with a lease and heartbeat; graceful deregistration; lease expiry on a dead process; automatic idempotent re-registration after a Hub restart; and a product that starts fully with no Hub present.

**Testing requirements.** Hub-restart re-registration; provider-crash lease expiry; Hub-absent product start; double-registration idempotency.

**Completion gate.** A provider survives a Hub restart, a dead provider's lease expires, and a product starts and saves with no Hub present.

### WP-08.03 — Routing and versioning

**What must be fully done.** Routing resolves a call to a registered endpoint by contract and version, with the fixed routing priority of the contract architecture. Version negotiation happens at connect; an unsatisfiable version produces a clean, explained refusal.

**Testing requirements.** Routing priority tests; version negotiation matrix including refusal.

**Completion gate.** Routing follows the fixed priority and version mismatch refuses cleanly.

### WP-08.04 — Health, backpressure and concurrency

**What must be fully done.** Health reporting across the five dimensions; per-connection and per-method concurrency limits; explicit backpressure with a recorded shed reason; ordering guarantees stated and enforced; no deadlock between bidirectional calls.

**Testing requirements.** Saturation tests asserting bounded memory; an ordering test; a bidirectional-call deadlock test.

**Completion gate.** Saturation is bounded and observable, and bidirectional calls cannot deadlock.

### WP-08.05 — Disconnection, cancellation and reconnection

**What must be fully done.** Disconnection produces a typed failure with effect certainty for every in-flight call. Cancellation propagates across the boundary. Reconnection is automatic with backoff, and in-flight work is either resumed by idempotency or reported as unknown-effect.

**Testing requirements.** Fault-injection tests: mid-call disconnect, slow peer, half-open connection, and peer restart.

**Completion gate.** Every fault produces a typed outcome with correct effect certainty, and no call hangs indefinitely.

### WP-08.06 — Large-data path

**What must be fully done.** A controlled transfer channel for large payloads, using a resource reference with range, checksum, cancellation and rate limiting. The Hub never relays the body. A payload exceeding the inline limit is rejected with guidance rather than silently truncated.

**Testing requirements.** Large-transfer tests with interruption and resumption; a negative test asserting an oversized inline payload is refused; an assertion that the Hub carries no body.

**Completion gate.** Large transfers work with interruption and resumption, and the Hub demonstrably carries no payload body.

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
| Cross-platform transport and access-control results | `WP-08.00` |
| Manifest concurrency and self-heal results | `WP-08.01` |
| Lifecycle matrix: restart, crash, absent Hub, double registration | `WP-08.02` |
| Routing priority and version negotiation matrix | `WP-08.03` |
| Saturation, ordering and deadlock results | `WP-08.04` |
| Fault-injection outcomes with effect certainty | `WP-08.05` |
| Large-transfer results and the Hub no-body assertion | `WP-08.06` |

---

## 8. Completion gate

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

**Upstream.** `06` (proven AOT RPC), `07` (durable state behind the surface).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `09` — Capability model | A transport to carry capability invocations |
| `11` — Security | Local authentication and the enforcement point at the transport boundary |
| `13` — Probes | The real transport the probes exercise |
| `14` — First slice | Everything |
| `26` — Remote bridge | The local half of the durable tool-request path |
