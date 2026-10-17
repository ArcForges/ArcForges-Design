# Minimal DesktopPlatform refactor

Decision: [AD-0013](../decisions/AD-0013-reuse-and-supersession.md) §4. Baseline: DesktopPlatform main `60309ec9`, `src/BuildingBlocks/ArcForges.LocalRpc` (WP-08.00–08.06) and `ArcForges.Security.Secrets`.

Two packages change: `ArcForges.LocalRpc` and `ArcForges.Security.Secrets`. Everything else the flagship uses is reused unchanged, or written in the ArcForges repository. The changes are additive: existing parent–child behaviour, limits and tests stay as they are, and the published single-version release set gets a new version.

## 1. `ArcForges.LocalRpc`: service-endpoint mode (AF-DP-01)

### 1.1 Why

The current library serves a parent and the helper children it launched. That model does not fit a long-lived per-user service:

| Current behaviour | Effect on the node API |
|---|---|
| The endpoint is supplied by the launcher | The node needs a well-known per-user pipe or socket that clients find |
| At most 8 connections | The CLI, Desktop, several MCP adapters, hooks and probes connect concurrently |
| Data calls: 10 s default, 30 s maximum deadline | `WaitTask` waits up to 55 s, and `RunDoctor` and `GetReport` up to 60 s |
| Streams count as data calls under the same deadline | `Subscribe`, `AttachTask`, `WatchResources` and `WatchTaskOutput` are long-lived |
| Connections close after 60 s without a call in flight | The Desktop holds a subscription for hours |
| The connection decision does not see the peer process or user | The node must verify same-user peers and derive the caller's origin ([11](../architecture/11-security-privacy.md) §1–2) |

### 1.2 Additions

1. **`LocalRpcServerOptions.Mode = Service`.** The default stays `ParentChild`.
   - **Endpoint.** Service mode binds a well-known endpoint given by the owner:
     - Windows: pipe `arcforges-<sid-hash>-node`;
     - Linux: socket under `$XDG_RUNTIME_DIR/arcforges/`.
   - **Access control.** The library creates the endpoint with same-user-only access:
     - Windows: a DACL granting the owner SID and SYSTEM, an explicit deny for `NT AUTHORITY\NETWORK`, and `PIPE_REJECT_REMOTE_CLIENTS`;
     - Linux: a 0700 directory and a 0600 socket.

     If the existing endpoint code already applies these, the task proves it with tests.
   - **Connections.** `MaxConnections` is configurable up to 256 in service mode, default 64. The backlog and slot behaviour is unchanged.
   - **Idle rule.** A connection holding an open stream is never idle. Otherwise the idle close is 10 minutes in service mode. The handshake timeout stays 10 s.
2. **Stream lane.**
   - **Registration.** The owner registers server-streaming methods with `RegisterStream(method, StreamProfile)`. They run in a lane separate from the data and control lanes: default 8 concurrent streams per connection, 32 per server per client process.
   - **`StreamProfile`:**
     - `MaxLifetime` (unbounded allowed);
     - `HeartbeatInterval` (the owner's frames; the library only measures inactivity);
     - `MaxBufferedMessages`: back-pressure bound, after which the library completes the call with `RESOURCE_EXHAUSTED`, so the owner sends a `reset`;
     - `RequireReads`: the client must read within N seconds, or the stream is cancelled.
   - **Deadlines.** Stream calls are exempt from the 30 s cap and use their profile instead.
3. **Per-method limit profiles.** `RegisterMethod(method, CallProfile)` sets the default and maximum deadline per method (for example `WaitTask` 60 s, `RunDoctor` 60 s, `GetReport` 30 s). Methods without a profile keep 10 s / 30 s. Profiles may lower the global bounds, or raise the deadline only for methods registered in service mode.
4. **Peer identity provider.**
   - **Interface.** `ILocalRpcPeerIdentity` is resolved once per accepted connection, before HTTP/2 reads a byte, and passed to `AuthorizeConnectionsAsync`. Handlers read it as a connection feature (`LocalRpcPeer`: `ProcessId`, `ProcessStartTime`, `UserSid` or `Uid`, `ExecutablePath`).
   - **Windows:** `GetNamedPipeClientProcessId`, then `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)`, `OpenProcessToken`, the user SID, and `GetProcessTimes` for the start time.
   - **Linux:** `SO_PEERCRED` (pid, uid, gid), `/proc/<pid>/stat` for the start time, and `/proc/<pid>/exe`.
   - **Races.** A peer that exits between accept and query is denied.
5. **Unchanged:** message size limits (4 MiB), refusal trailers, the control lane, command journal and receipts, launch descriptors, the brokered large-data mechanism, and no compression.

### 1.3 Tests

- **Existing tests** pass unchanged.
- **New tests on both platforms:**
  - service-mode endpoint ACL (a second-user check is deferred to AR-02 when no second account exists);
  - 64 concurrent connections;
  - a stream lasting 15 minutes with heartbeats while 16 data calls run;
  - back-pressure reset;
  - per-method deadline profile;
  - peer identity correctness, including a peer exiting before the query;
  - idle rules.
- **AOT:** publish with zero trim warnings.

## 2. `ArcForges.Security.Secrets`: Linux backends (AF-DP-02)

- **Secret Service.** A `SecretService` backend implements `org.freedesktop.secrets` over the session D-Bus (`Tmds.DBus.Protocol`; AOT-compatible): create, read and delete items in the default collection, with attributes `{application: arcforges, name: <key>}`. A locked collection prompts through the desktop keyring, and without a session bus the backend is unavailable.
- **File fallback.**
  - **Storage:** files under `<data root>/run/secrets/` with mode 0600 in a 0700 directory, written atomically (`rename`), each holding one secret.
  - **Reporting:** the backend reports `Protection = FileOwnerOnly`, which the node shows as weaker storage (R-AUTH-003).
- **Selection.** Secret Service when it is available, otherwise the file fallback. The choice is recorded and shown in `AccountStatus.credential_in_os_store`.
- **Tests.** Real tests in WSL2 Debian: the file fallback (always available). Secret Service tests belong to the OS secret-store integration tier ([16](../architecture/16-testing-strategy.md) §1): they run in the isolated `ArcForgesTest` distribution on explicit opt-in, minimal and sequential, when the user has installed a Secret Service provider such as `gnome-keyring` there (otherwise skipped with a reason). The Windows Credential Manager backend is unchanged; its real tests follow the same tier.

## 3. Not changed

Every other DesktopPlatform package, including the unfinished Linux TSYNC, the Desktop.Shell Avalonia adapter and the PLT.66 move, which stay retained (C-15).
