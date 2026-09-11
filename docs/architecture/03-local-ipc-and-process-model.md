# Local IPC, Hub and Process Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** (cloud topology and local action), **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (AOT matrix), **[V-05b](../assurance/phase-1-official-verification.md#rule-v-05b)** (gRPC AOT evidence)
> Companions: [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`04-desktop-application-architecture.md`](04-desktop-application-architecture.md), [`08-security-architecture.md`](08-security-architecture.md)

Same-machine first-party business RPC uses generated gRPC over authenticated operating-system IPC, under P2-009.**

---

## 1. Generated service shape

Each process hosts explicitly registered generated protobuf services in a minimal Kestrel HTTP/2 listener. Callers use Grpc.Net.Client and ConnectCallback for the OS stream. Each side hosts its own listener for reverse calls; gRPC is not the old symmetric peer channel. ArcChat Hub is a library inside ArcChat, not another executable or a mandatory professional-product relay. The [wire registry](contracts/04-protobuf-wire-registry.md#8-transport-and-generation-acceptance) fixes exact methods, fields, framing, versions and bounded calls.

---

## 2. Authenticated local transport

Windows uses asynchronous Named Pipes with current-user ACL; inspect the actual client/server process identity through the named-pipe OS connection, not a claimed PID. Linux uses private directory0700/socket0600 and SO_PEERCRED; macOS uses peer credentials/PID and signed-code identity where available. UDS path is at most100 UTF-8 bytes. All production listeners are pipe/UDS, no fixed TCP port and no public interface. Tests exercise actual published processes, not only in-memory streams.

Verify user/process/build against the selected registered application before exchanging a random32-byte session nonce through the authenticated bootstrap. Nonces live in memory, expire with the30-second registration lease (renew10s), and are never written to the endpoint manifest. Per-peer scopes and capability grants are checked on every call. The Hub may issue a scoped peer introduction; the actual owner still authenticates and authorizes. Hub absence preserves product local use and direct Cloud access. macOS content sandbox uses its separate XPC protocol, not this general product listener.

---

## 3. Wire and flow-control profile

Use the handwritten proto/generated C# services from Contracts, HTTP/2 protobuf framing and explicit registration. No MessagePack/JSON-RPC formatter, dynamically marshaled object or runtime proxy construction. Business unary messages <=4 MiB, normal replies10s, permitted synchronous measurement30s,16 concurrent calls and64 queued per peer; refuse overflow before dispatch. Long jobs return handles and bulk content uses authorized references/transfer channels. Timeouts/cancellation after dispatch retain effect uncertainty. Reconnect rebuilds authenticated channels and typed clients; it never resends a non-idempotent command automatically.

---

## 4. Hub and registration

### 4.1 Endpoint manifest

At start-up each product writes a minimal endpoint manifest into the current user's private runtime directory, carrying: `AppId`, `InstanceId`, process id, transport kind, endpoint name, build identity, contract set identity, and start time.

| # | Rule |
|---|---|
| <a id="rule-em-01"></a>EM-01 | **The manifest is not a credential.** Session tokens are never written into it. |
| EM-02 | **A connecting process still verifies** the peer user, the expected process, the build and contract set, and the short-lived session credential issued by the Hub. |
| EM-03 | Stale manifests are detected and cleaned up. |

### 4.2 Registration lifecycle

```
Product starts
  → creates its own endpoint and RPC target
  → reaches a locally usable state (independent of the Hub)
  → connects to the Hub
  → authenticates
  → registers instance, endpoint, capabilities, contract set, versions, features
  → Hub returns RegistrationAccepted with a lease and a session token
  → heartbeats while the lease is active
```

| # | Rule |
|---|---|
| RG-01 | **A product starts its own endpoint first, then connects to the Hub.** |
| RG-02 | **Hub unavailability never prevents a product reaching a locally usable state** (`§3.1` of the product scope). |
| RG-03 | **The Hub evicts out-of-contact instances by lease**, not by inference. |
| RG-04 | **On reconnect a product uses a new session identity and idempotently replaces its old registration** (`§12` of the contracts architecture). |
| RG-05 | **Re-registration is idempotent.** |
| RG-06 | **Application-level information survives instance death**; only instance-scoped state is removed. |
| RG-07 | **A normal exit unregisters proactively; a crash is cleaned up by lease expiry.** |
| RG-08 | **After a connection is re-established, new generated clients are bound to freshly authenticated channels.** Old proxies are never reused. |

### 4.3 Health and backpressure

Instances report: `Ready` / `Busy` / `Degraded` / `Draining`, current task count, queue depth, an optional load level, the supported contract set and feature flags, and the last successful heartbeat plus process start time.

| # | Rule |
|---|---|
| HB-01 | **Callers must handle `Busy`, a retry-after hint and a queue ceiling.** |
| HB-02 | **An unbounded queue is not a fault-tolerance strategy.** Every channel and queue has a capacity and an overflow policy. |
| HB-03 | **A provider that drops offline is marked unroutable within a small, bounded number of heartbeat cycles.** |
| HB-04 | Health, presence, readiness and compatibility remain five separate dimensions (`§11` of the contracts architecture). |

### 4.4 Routing

Priority is fixed (`§13.3` of the contracts architecture): explicit `InstanceId` → resource affinity → user-selected default → the single healthy instance → `SelectionRequired`.

| # | Rule |
|---|---|
| RT-01 | **The Hub's document routing index stores only "which instance currently has which document open"** — never document content. |
| RT-02 | **The Hub never picks at random among several candidates.** |
| RT-03 | **Where several instances of one product exist, routing carries `InstanceId` or the target resource identity.** |

---

## 5. Connection management

Each product has exactly one infrastructure component owning the RPC connection lifecycle:

```
create / listen on the endpoint
  → create formatter + message handler
  → register the local target through generated metadata
  → StartListening()
  → create strongly typed proxies
  → observe Completion / Disconnected
  → reconnect with exponential backoff and jitter
  → re-authenticate, re-register, re-attach proxies
  → update connection health state
```

| # | Rule |
|---|---|
| CN-01 | **Business code never creates a pipe, a socket or an RPC instance, and never writes a method-name string.** |
| CN-02 | **Exactly one RPC instance per transport.** Calling the static attach helper more than once on one stream is prohibited — each call creates a separate RPC instance. |
| CN-03 | **When several proxies are needed, one RPC instance is created and the instance-level attach is used per interface.** |
| CN-04 | **Every multi-interface combination required under AOT is pre-generated** via the proxy interface group attribute. |
| CN-05 | **Runtime assembly scanning followed by dynamic attachment is prohibited.** |
| CN-06 | **Server targets are registered through generated target metadata**, never through reflection-enumerating convenience overloads. |
| CN-07 | **All targets are registered before listening starts.** |
| CN-08 | **RPC adapters hold no UI objects.** |
| CN-09 | Target lifetimes are explicitly tied to the connection and application lifetime. |

---

## 6. Concurrency and ordering

**The transport is not an actor.** It supports concurrent calls, and synchronization-context behaviour is no substitute for domain concurrency control.

| # | Rule |
|---|---|
| <a id="rule-cc-01"></a>CC-01 | **Each document session, timeline or capture session maintains write ordering** with a mailbox, an async lock, or a single-writer queue. |
| CC-02 | **Business ordering is never expressed through RPC arrival order.** |
| CC-03 | **A domain lock is never held while awaiting a peer callback.** |
| CC-04 | **Bidirectional callbacks must not form a cycle** in which each side synchronously waits on the other. |
| CC-05 | **Write commands rely on `ExpectedRevision` plus `CommandId`**, never on which call happened to be sent first. |
| <a id="rule-cc-06"></a>CC-06 | **Optimistic revision is the default concurrency mode** ([CC-04](../requirements/05-ai-and-agent-execution.md#rule-cc-04) in the AI requirements). A long task does not hold a document lock. |
| CC-07 | **Genuinely exclusive resources use lease and busy semantics provided by their owner** ([CC-05](../requirements/05-ai-and-agent-execution.md#rule-cc-05) there). |

---

## 7. Disconnection, cancellation and retry

The RPC layer implements no business retry.

| # | Rule |
|---|---|
| DC-01 | Calls in flight when a connection drops may fail with a connection-lost error; remote exceptions surface as remote-invocation errors; **business failures still use `ArcResult<T>`** (`§13.6` of the contracts architecture). |
| DC-02 | Connection state is driven by observing completion and disconnection. |
| DC-03 | **Cancelling locally executing calls on connection close may be enabled per scenario**, but a long-running business task never derives cancellation from connection lifetime alone. |
| DC-04 | **Reconnection uses exponential backoff with jitter.** |
| DC-05 | **Queries are safe to retry. Write commands are retried only under the same `CommandId`, with the owner implementing idempotency** ([ID-01](../requirements/05-ai-and-agent-execution.md#rule-id-01) in the AI requirements). |
| DC-06 | **After reconnecting**: re-authenticate, re-register capabilities, and backfill state by revision or sequence. |

---

## 8. Security of the local boundary

**Local IPC is not itself an authentication or authorization system.**

| # | Rule |
|---|---|
| SC-01 | **Operating-system permissions restrict access first**: pipe ACLs, socket file permissions, a private runtime directory. |
| SC-02 | **A session handshake completes as the first stage after connecting.** |
| SC-03 | **Session tokens bind `AppId`, `InstanceId`, endpoint, build identity, contract set and an expiry.** |
| SC-04 | **Session tokens never appear in the endpoint manifest.** |
| SC-05 | **Every call carries actor, scope and correlation context.** |
| SC-06 | **The owner authorizes again at the final execution point** ([DP-02](../requirements/07-security-privacy-and-trust.md#rule-dp-02) in the security requirements). |
| <a id="rule-sc-07"></a>SC-07 | **Being "local" never automatically grants every capability**, even where an untrusted process can reach the endpoint. |
| SC-08 | **Cloud never connects to a local endpoint** (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |

---

## 9. Large data across the local boundary

| # | Rule |
|---|---|
| LD-01 | **Large resources are never carried in an ordinary RPC request or response.** They cross as a `ResourceRef` plus controlled access, a file-handle strategy, or a temporary resource channel. |
| LD-02 | **Ordinary RPC calls set a sensible message size limit.** |
| LD-03 | **The Hub never relays media frames or large file bodies**. |
| LD-04 | **Resource reads support range and chunking, checksums, cancellation and rate limiting.** |
| LD-05 | **A path is returned only after both sides explicitly authorise, and after normalisation and root-directory checks.** |
| LD-06 | **Temporary resources use short-lived capability tokens.** |
| LD-07 | **Per-frame images and GPU state never cross a process boundary** (`§12` of the native interop architecture). |

---

## 10. Bidirectional communication

| Traffic | Mechanism |
|---|---|
| Commands and queries | Strongly typed methods |
| Low-frequency connection-level notifications | Interface events or an explicit callback contract |
| High-frequency state streams | Prefer revision plus delta; a validated async stream where genuinely needed |
| Large files or media frames | **Never** as ordinary RPC payloads — resource reference or controlled stream |

**Events are never durable truth.** Recovery after a disconnect relies on revision and journal queries ([EV-10](02-contracts-and-protocols.md#rule-ev-10) in the contracts architecture).

---

## 11. AOT checklist

Answerable before any local RPC change merges (with the verified constraints in **[V-05b](../assurance/phase-1-official-verification.md#rule-v-05b)**):

- [ ] Is the interface `partial`, with the contract attribute **and** the shape-generation attribute including public instance methods?
- [ ] Does the contracts assembly export its generated proxies?
- [ ] Is the interceptors property enabled on every project in the attach chain?
- [ ] Is dynamic interface or type discovery absent?
- [ ] Are multi-interface combinations pre-generated?
- [ ] Is the formatter Protocol Buffers with generated shapes, or JSON with a source-generated context?
- [ ] Is the target registered through generated metadata?
- [ ] Has a real AOT publish run with at least one RPC round trip?
- [ ] Have disconnection, reconnection, duplicate `CommandId`, revision conflict and callback deadlock all been tested?

**A missing generated proxy is a build-time or start-time error, not a silent runtime fallback.** With interceptors enabled, an attach for an interface without a generated proxy fails early — turning a missed contract generation into a testable failure rather than a production surprise.

---

## 12. Fault injection

Required scenarios:

Hub starts after the product · Hub restart · pipe or socket severed mid-call · product crashes before a command commit · product crashes after a command commit · lost heartbeats · duplicate commands · out-of-order responses · revision conflicts · potential bidirectional callback deadlock · queue overflow · slow consumer · oversized message · stale endpoint manifest · unauthorised local peer · incompatible contract set · instance restart during an in-flight task.

---

## 13. The remote bridge

**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** fixes the shape:

```
ArcChat Desktop opens an outbound authenticated connection to Cloud
  ↓
The user confirms device binding on the desktop
  ↓
Cloud delivers only restricted wake or intent messages to bound devices
  ↓
ArcChat Desktop pulls a durable ToolRequest
  ↓
ArcChat re-authorises locally: actor, capability, resource, risk, approval
  ↓
ArcChat routes to the owning product over local RPC
  ↓
The owner validates and authorises again, then executes
  ↓
Durable business results are written into the owner's own state
  ↓
An idempotent ToolResult is returned; cloud-persisted results go over HTTP
```

| # | Rule |
|---|---|
| RB-01 | **Cloud never scans the LAN**, never opens an inbound connection to a user machine, and never addresses a local endpoint. |
| RB-02 | **Mobile and web never talk to a local endpoint.** |
| RB-03 | **Realtime is never the sole source of truth for a remote write.** |
| RB-04 | **A remote write still passes through the local application service, with revision and idempotency.** |
| RB-05 | **A command left unconfirmed when a realtime connection drops is re-adjudicated through durable task state, never blindly re-executed** ([FL-06](../requirements/05-ai-and-agent-execution.md#rule-fl-06), [FL-07](../requirements/05-ai-and-agent-execution.md#rule-fl-07) in the AI requirements). |
| RB-06 | **Every step carries correlation, a `CommandId` and an audit record.** |
| RB-07 | **The user can revoke device and capability scope at any time**, taking effect at the next security boundary. |

---

## 14. Traceability

| Current document | Relationship |
|---|---|
| [ArcForges Product Scope and Portfolio](../requirements/00-product-scope-and-portfolio.md) | Owns the local coordinator and direct Cloud data paths |
| [Contracts, Protocols and the Cross-Application Semantic Model](02-contracts-and-protocols.md) | Defines capability, context, resource and compatibility semantics |
| [Local RPC Operations](contracts/02-local-rpc-operations.md) | Defines the concrete typed local interfaces |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Desktop AOT deliverable constraints |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Cloud topology and the durable local-action model |
| **[V-05b](../assurance/phase-1-official-verification.md#rule-v-05b)** | The formatter and proxy-generation evidence, and the contract-authoring obligation |
