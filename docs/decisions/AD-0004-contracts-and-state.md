# AD-0004 — Contracts, transports and authoritative state

- Status: Accepted (2026-10-12)

## Decision

### Contracts

1. **`.proto` files are the canonical first-party contracts**, published from the Contracts repository as NuGet packages. They follow the existing Contracts conventions:
   - request field 1 is `arcforges.foundation.v1.RequestMeta`, fields 2–9 are reserved and business fields start at 10;
   - response field 1 is `ResponseMeta`, followed by `oneof outcome { <Method>Value value = 2; ArcError error = 3; }`;
   - every field carries an explicit `json_name`.
2. **New packages** (specified in [contracts/](../contracts/README.md); adopted into Contracts by delivery task AF-CON-01):

| Package | Proto package | Access | Used by |
|---|---|---|---|
| `ArcForges.Contracts.Node` | `arcforges.node.v1` | public | node, CLI, Desktop, MCP adapter, WSL bridge, future products |
| `ArcForges.Contracts.Peer` | `arcforges.peer.v1` | internal | node-to-node (LAN mTLS) and host-to-guest (bridge) |
| `ArcForges.Contracts.Fleet` | `arcforges.fleet.v1` | public | cloud API for web, Android and nodes (gRPC-Web) |
| `ArcForges.Contracts.Relay` | `arcforges.relay.v1` | internal | node ↔ relay Durable Object frames, and relay ↔ C# host envelopes |

3. **Reused existing packages:**
   - `arcforges.foundation.v1`: `RequestMeta`, `ResponseMeta`, `ArcError`, `Id`, `Revision`, `Instant`, `PageRequest`, `PageState`, `Receipt` and `ActorChain`.
   - `arcforges.publicapi.v1` for identity, device, entitlement, commerce, notification and support. The existing services are unchanged. The flagship adds data values (device product values `arcforges-node` and `arcforges-mobile`, node push kinds, plan features) and one new service in a new file (`SupportAccessService`). The Google Play provider is the new `fleet.v1.StoreBillingService` ([contracts/reuse-map.md](../contracts/reuse-map.md)).
   - `arcforges.operator.v1` (internal): `OperatorService` unchanged, plus the new `OperatorReadService` in a new file.

   ArcChat-family services (Chat, Task, Agent, Sync, Search, Scope, Simulation, Transfer, Export, Catalog, Extensions) are retained but unused by the flagship.

### Transports

| Path | Transport | Authentication |
|---|---|---|
| Desktop, CLI, MCP adapter → local node | gRPC over HTTP/2 on a Windows named pipe or a Unix domain socket (DesktopPlatform LocalRpc, adapted) | Same-user peer check (pipe DACL; socket directory mode 0700 and SO_PEERCRED) plus a per-connection client hello naming the client kind |
| Host node ↔ WSL guest node | gRPC over HTTP/2 on the byte stream of `arcforges bridge wsl` (wsl.exe stdio) → guest Unix socket | Bridge launched by the host user; guest checks the peer uid; link token exchanged at link creation |
| Node ↔ node (LAN) | gRPC over HTTP/2 with mutual TLS 1.3 on TCP | Account-issued or pinned node certificates (AD-0008) |
| Web, Android, nodes → cloud API | gRPC-Web over HTTPS through the Worker ingress (existing) | Account session (native bearer or browser cookie with CSRF) or node credential |
| Node ↔ cloud relay | WebSocket carrying `arcforges.relay.v1` frames to a hibernating Durable Object | Short-lived signed node token (AD-0009) |
| AI client → MCP adapter | MCP JSON-RPC over stdio (a local HTTP transport is roadmap RM-05) | Process ownership (stdio) |

### Authoritative state

1. Each node is the **only writer** of its execution, resource, storage, cache, policy, session and record state (SQLite store, [data/node-store.md](../data/node-store.md)).
2. A task belongs to its **origin node**. An attempt belongs to its **executing node**, and the origin mirrors remote attempts from the executor's stream.
3. The cloud is the only writer of account, device registry, entitlement, commerce, relay routing, remote-command and push state. It holds node status only as an expiring cache for remote viewing.
4. Clients keep caches only. They reconcile from snapshot-then-incremental streams (`NodeEventService.Subscribe`) ordered by a per-node `event_seq`, within a `stream_generation` that changes when the journal is reset or restored. A client resumes from its last cursor, or receives `reset` plus a fresh snapshot.
5. Commands carry `RequestMeta.command_id` for idempotency (replay returns the stored receipt for 24 h), and `expected_rev` where a resource is revisioned (policies, pool definitions, workspace settings).
6. Errors use `ArcError`. `EffectCertainty` is mandatory on execution-affecting failures, so a caller can tell "did not start" from "may have run".
