# Contracts

Decision: [AD-0004](../decisions/AD-0004-contracts-and-state.md). Protobuf is canonical. First-party transports are gRPC; browsers and Android use binary gRPC-Web; live relay traffic uses protobuf frames over WebSockets.

**Amended 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) (target until each AF-CTR task is delivered).** Business decisions are made by the Go center (not the C# host), which consumes Go bindings generated from these protos in the Contracts repository (AF-CTR-01); node connections terminate in the Go center instead of `FleetHub`. `arcforges.peer.v1` stays in `v1`, compatible and not served.

The `.proto` files under [proto/](proto/) are the **specification**. Task AF-CON-01 adopts them into the Contracts repository unchanged, apart from placement:
- `node`, `fleet` → `public/proto`;
- `peer`, `relay` → `internal/proto`.

The files compile with the protoc bundled in Grpc.Tools 2.84.0 (libprotoc 35.1) against the pinned foundation contract in [reference/contracts-b774c322/](reference/contracts-b774c322/README.md). The generated C# (messages and gRPC stubs) builds with zero warnings under `IsAotCompatible` (checked by `tools/check_design.py --compile`).

## 1. Packages

| Package | Files | C# namespace / package | Transport | Locality | Callers |
|---|---|---|---|---|---|
| `arcforges.node.v1` | 20 files, 19 services | `ArcForges.Contracts.Node.V1` / `ArcForges.Contracts.Node` | gRPC over HTTP/2 on a named pipe or Unix socket (DesktopPlatform LocalRpc service-endpoint mode) | One node | CLI, Desktop, MCP adapter, hook handler, probe; relay commands mapped internally |
| `arcforges.peer.v1` | `peer.proto`, 6 services | `ArcForges.Contracts.Peer.V1` / `ArcForges.Contracts.Peer` (internal) | gRPC over HTTP/2 with TLS 1.3 mTLS on TCP 47820 (`GuestLinkService`, formerly carried over the WSL bridge byte stream, is retired: §7) | Node ↔ node | Paired peers |
| `arcforges.fleet.v1` | `fleet.proto`, 3 services | `ArcForges.Contracts.Fleet.V1` / `ArcForges.Contracts.Fleet` | Binary gRPC-Web through the Worker ingress to the C# host; `WatchFleet` as gRPC-Web text streaming | Cloud | Nodes (node credential), web and Android (account session), unauthenticated flow endpoints |
| `arcforges.relay.v1` | `relay.proto`, messages only | `ArcForges.Contracts.Relay.V1` / `ArcForges.Contracts.Relay` (internal) | Protobuf binary WebSocket messages; the DO ↔ C# internal container route | Relay | Nodes, viewers, `FleetHub`, C# host |
| `arcforges.publicapi.v1` (additive) | `support_access.proto`, 1 new service (`SupportAccessService`); the reused services are unchanged | `ArcForges.Contracts.PublicApi.V1` (the package's existing namespace) | Binary gRPC-Web through the Worker ingress to the C# host | Cloud | Web Account profile (account session) |
| `arcforges.operator.v1` (additive) | `operator_read.proto`, 1 new service (`OperatorReadService`); the reused `OperatorService` is unchanged | `ArcForges.Contracts.CloudInternal.Operator.V1` (the package's existing namespace; internal) | Binary gRPC-Web from the Operations profile to the C# host | Cloud | Operators (operator session with step-up) |

Reused contracts are listed in [reuse-map.md](reuse-map.md). The method-by-method index is [api-catalogue.md](api-catalogue.md), generated from the protos.

## 2. Message conventions (existing Contracts rules)

- **Request:** `arcforges.foundation.v1.RequestMeta meta = 1; reserved 2 to 9;` with business fields from 10. `meta.command_id` (UUIDv7) is required on every mutating call.
- **Response:** `ResponseMeta meta = 1; oneof outcome { <Method>Value value = 2; ArcError error = 3; } reserved 4 to 9;`. Value fields start at 10.
- **Naming:**
  - Messages are named `<Service><Method>Request`, `…Response`, `…Value` and `…Frame`.
  - Domain messages carry plain names. `ManagedTask` is not called `Task`, because that would clash with `System.Threading.Tasks.Task` in C#.
- **Fields:**
  - Every field has an explicit `json_name` in lowerCamel.
  - Singular scalar and enum fields are `optional` (explicit presence).
  - Enums start with `<ENUM>_UNSPECIFIED = 0`, and values carry the enum-name prefix.
- **Identifiers:** `arcforges.foundation.v1.Id` (16-byte UUIDv7). Text form: Crockford base32, lower case (CLI, MCP, URLs).
- **Units:**
  - CPU: millicores (`*_millicores`);
  - bytes: `*_bytes`;
  - durations: milliseconds (`*_ms`);
  - time points: `arcforges.foundation.v1.Instant`.
- **Bounds:**
  - gRPC message size limit 4 MiB, except `TransferService` and output reads, which use chunking;
  - output frames ≤ 64 KiB;
  - lists paged with `PageRequest` / `PageState`, defaulting to 100 entries.

## 3. Streams

Server streams return `<Service><Method>Frame`:

```proto
message XFrame {
  arcforges.foundation.v1.ResponseMeta meta = 1;
  StreamPosition position = 2;        // cursor, sequence, generation
  reserved 3 to 9;
  oneof frame {
    StreamReset reset = 10;           // gap, generation change, overflow; snapshot follows if stated
    Heartbeat heartbeat = 11;         // every 15 s unless stated
    arcforges.foundation.v1.ArcError error = 12;  // terminal error frame
    ...                               // method-specific frames from 20
  }
}
```

- **Shape.** The position shape is reused from `arcforges.events.v1.StreamPosition`, but not imported, so the legacy event registry is not pulled in.
- **Resuming.** A client resumes with the last cursor.
- **Resets.** The server answers a stale cursor (beyond retention or another generation) with `reset{snapshot_follows=true}` and a snapshot.
- **Duplicates.** Clients drop events with `seq ≤ last applied`.
- **Client-to-server streaming** is not used. Input travels as ordered unary calls (`WriteTaskInput` with an offset), so the same contracts work over gRPC-Web.

## 4. Method annotations

Every RPC carries structured comments, which `tools/check_design.py` verifies and renders into the API catalogue.

| Key | Content |
|---|---|
| (first lines) | Purpose |
| `auth:` | Permission per origin (`HUMAN`, `SCRIPT`, `AGENT`: `A` allow, `P` approval, `D` deny), and the remote risk class. `REMOTE=low\|medium\|high` marks the method that a `fleet.v1.NodeCommandBody` kind invokes, with that kind's class. `REMOTE=-` means no remote command reaches the method; remote viewers see only the status summaries the node publishes. Peer and cloud methods name the credential (`PEER: paired`, `account session`, `node credential`, step-up). Defaults come from [security](../architecture/11-security-privacy.md) §1. |
| `idempotency:` | `read`; `command_id` with its window (24 h; payload digest compared); or `natural: <key>` |
| `deadline:` | Default server bound. For streams: lifetime, heartbeat and idle limits. |
| `stream:` | `none`, or `server: <Frame>` with end conditions |
| `errors:` | `CATEGORY/code` list from [errors.md](errors.md), excluding the implicit codes |
| `locality:` | Where the call executes: `node`, `node -> cloud`, `peer`, `cloud`, `cloud -> relay -> node`; `guest` appears only on the retired surfaces of §7 |
| `state:` | Optional state-machine transitions caused ([state-machines](../state-machines/README.md)) |

**Field validation** appears as a trailing `// validate:` comment on request and input fields. A violation returns `VALIDATION/invalid_argument`, with the field path in `details.state.reason`.

## 5. Authorization and identity

- **Local node API.** The node assigns the origin at `NodeService.Hello` from the connection (the verified peer process, its client kind and process ancestry) and applies the permission matrix. Caller-supplied identity is never trusted ([11](../architecture/11-security-privacy.md) §1).
- **Peer API.** Identity comes from the TLS client certificate (pinned fingerprint or account SAN). Origin `PEER`. The origins `HOST` and `GUEST` (formerly the bridge's) are retired (§7).
- **Fleet API.** The credential decides access: an account session from the Identity service (reused contract; endpoints AF-ID-01), or a node credential. Step-up uses the reused Identity step-up. Entitlement checks use the reused Entitlement module.

## 6. Idempotency

- **Mutations** deduplicate by `meta.command_id` for 24 hours. The node stores `(command_id, payload_digest, outcome)`.
  - Same ID and same payload: the stored logical outcome is returned. For `PurgeTaskRecord`, its post-commit WAL checkpoint is also attempted on replay (MR-14; [node-store](../data/node-store.md) section 1). A busy or failed checkpoint returns the transient `INTERNAL/internal` error with known effect `HAPPENED` instead of success; it does not replace the stored logical outcome. Replaying identical bytes retries the checkpoint without deleting the task record again.
  - Same ID and a different payload: `CONFLICT/command_id_reused`.
- **Approvals** keep the original `command_id`, so an agent that retries after approval receives the executed outcome.
- **Cloud mutations** use the reused platform command-dedup table.

## 7. Compatibility

- **Within `v1`, changes are additive only:**
  - new fields and methods;
  - new enum values, which clients must treat as unknown;
  - new oneof members.
- **Never:** renumbering, retyping or reusing numbers. Removed fields become `reserved` with their names. Breaking changes need a `v2` package beside `v1`.
- **From when.** These rules apply from the first cohort that AF-CON-01 publishes. Until then the design protos are specifications and may still change; each change is listed in the design PR.
- **Clients** feature-detect with the `features` lists in `NodeService.Hello` and `PeerHandshakeService.Hello`. The Contracts repository's wire-compatibility gate compares each change with the last published package.
- **Error codes** are additive. Clients treat an unknown code by its category.
- **Retired v1 surfaces** ([AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md) §3). The dedicated Windows–WSL integration was dropped on 2026-10-21. Its declarations stay in the v1 packages for wire compatibility, but no node serves, calls, sets or relies on them, no client shows them, and no later change extends them; a future major version may drop them. They are `peer.v1.GuestLinkService` and its messages (`GuestHello`, `GrantRequest`, `GrantRelease`, `GuestUsageReport`, `GrantDecision`); `ResourceService.ListGuestLinks`, `SetGuestLink`, `GetHostLink` and `TrustHost`, with `GuestLinkView` and `GuestLinkState`; `NODE_ROLE_GUEST` (every node is `NODE_ROLE_HOST`), `NodeRef.host_node_id`, `ORIGIN_GUEST` and `ORIGIN_HOST`, `ResourceSnapshot.guests` and `GuestConsumer`, `NodeInfo.guest_links`, `EVENT_TOPIC_GUESTS` and `NodeEvent.guest_link`, `FINDING_KIND_GUEST_LINK_LOST`, `ResourcePolicy.guest_standalone_fraction`, `ProbeObservation.wsl_distro`, the fleet's `role` and `host_node_id` for guests, and the error `STATE/link_down`. Still in use: `PROCESS_LABEL_GUEST_VM` and `ProcessView.crosses_vm_boundary`. The generated [API catalogue](api-catalogue.md) still lists the retired methods, as the protos declare them.

## 8. JSON mapping

The canonical protobuf JSON mapping (with the explicit `json_name`s) is used by:
- CLI `--json`;
- MCP `structuredContent`;
- `ExportRecords` JSON Lines;
- configuration snapshots in support bundles.

Ids are base64 in the canonical mapping. The CLI and MCP adapter additionally render `*_id` fields as Crockford base32 strings, documented as a presentation layer ([experience/cli.md](../experience/cli.md), [experience/mcp.md](../experience/mcp.md)).
