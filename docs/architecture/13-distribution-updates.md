# 13 — Distribution, installation and updates

Decision: [AD-0012](../decisions/AD-0012-distribution-and-updates.md). State machine: [SM-UPDATE](../state-machines/README.md#sm-update). Requirements: R-DIST-001..005.

## 1. Versions and compatibility

| Item | Scheme | Rule |
|---|---|---|
| Product version | SemVer `MAJOR.MINOR.PATCH`, with prerelease `-beta.N` (beta channel) and `-dev.N` (dev channel) | One version for all executables of a release |
| Node API contract | `arcforges.node.v1`; `NodeService.Hello` exchanges `{contract_major, contract_minor, features[]}` | Clients accept any node with the same major. A newer minor is backward compatible (new fields and methods only). Clients feature-detect rather than compare versions. |
| Peer protocol | `peer.v1` range in DNS-SD `v` and in `PeerHandshakeService.Hello` | Peers interoperate within the overlapping range ([09](09-lan.md) §7) |
| Relay frames | `relay.v1` with a `frame_version` field | The DO forwards unknown frame kinds unchanged; nodes ignore unknown kinds |
| Node store schema | Integer `schema_version` and `min_reader_version` in `store_meta` | See §6 |
| Internal helper contract | Arguments of `exit-record` and `exec-wrap`, and the `exit.json` format ([04](04-execution.md) §3) | Additive only, because helpers may run a newer binary than the node that launched the attempt |
| Configuration files | `node.json` has `"schema": 1` | Unknown keys are preserved and reported |

## 2. Release artifacts

Hosted CI builds each release `<v>` from a tagged commit of the ArcForges repository:

| Artifact | Contents |
|---|---|
| `arcforges-<v>-win-x64.msi`, `-win-arm64.msi` | Per-user MSI (§3.1) |
| `arcforges-<v>-win-x64.zip`, `-win-arm64.zip` | Version directory (Scoop, updater payload) |
| `arcforges-<v>-linux-x64.tar.zst`, `-linux-arm64.tar.zst` | Version directory (`install.sh`, updater payload) |
| `arcforges_<v>_amd64.deb`, `_arm64.deb` | System package (§3.3) |
| `install.sh` | User-level installer script (versioned with the release) |
| `manifest.json`, `manifest.json.sig` | Release manifest and its Ed25519 signature (§4) |
| `sbom.cdx.json` | CycloneDX SBOM ([11](11-security-privacy.md) §6) |

- **Windows version directory:** `arcforges.exe`, `arcforges-supervisor.exe`, and `arcforges-desktop.exe` with its native Avalonia/Skia libraries.
- **Linux version directory:** `arcforges` and `arcforges-desktop` with its native libraries.
- **Android:** released separately through Google Play (§8).

## 3. Installation

### 3.1 Windows (per-user MSI; no administrator rights)

- **Package.** Per-user install scope (`MSIINSTALLPERUSER=1`, `ALLUSERS=2` resolved to per-user), authored with WiX Toolset.
- **Features:**
  - `Core` (required): version directory, `current` junction, PATH entry, autostart, uninstall entry;
  - `Desktop` (default on): `arcforges-desktop.exe`, a Start menu shortcut and an optional Desktop shortcut;
  - `Integrations` (default off): opens the Desktop first-run integration step. It never writes client configuration without consent (R-AI-008).
- **Registrations.**
  - `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\ArcForgesNode` = `"%LOCALAPPDATA%\ArcForges\app\current\arcforges-supervisor.exe"`. The supervisor is a GUI-subsystem executable, so logon shows no console window. It starts `arcforges.exe node run` with `CREATE_NO_WINDOW` (AD-0003 §1; A-N03).
  - `HKCU\Environment\Path` gets `%LOCALAPPDATA%\ArcForges\app\current` appended, followed by a `WM_SETTINGCHANGE` broadcast.
  - The uninstall entry is the MSI's own.
- **Custom actions.** Each is an invocation of the installed native executable; there are no script custom actions.
  - After install: start `arcforges-supervisor.exe`, then `arcforges node wait-ready --timeout 30`.
  - Before uninstall: `arcforges node stop --reason uninstall --timeout 60`. Running managed executions are listed in the uninstall dialog, and the user chooses either to wait or to cancel them all (R-DIST-001).
- **Uninstall** removes the version directories, junctions, PATH entry and Run key. It keeps the data root unless the user ticks **Remove ArcForges data**, which runs `arcforges node wipe --all --yes` before removal.
- **Optional machine-wide service mode** (separate administrator MSI feature `MachineService`). It installs a Windows service `ArcForgesNode` that runs the same node, as the installing user (credential prompt). No product flow requires it; it exists for always-on hosts that need the node before logon.

### 3.2 Linux user install (`install.sh`)

1. **Check prerequisites:** the architecture, systemd user sessions (`systemctl --user is-system-running` reports any state other than `offline`), cgroup v2 and glibc ≥ 2.31. Missing systemd or cgroup v2 is reported as degraded enforcement ([03](03-resource-control.md) §8), not as an install failure.
2. **Download and verify:** fetch `manifest.json` and its `.sig` from the channel URL, verify the signature with the embedded public key, then download the tarball and verify its SHA-256.
3. **Extract:** into `~/.local/share/arcforges/app/<v>/`, then create `app/current` and `~/.local/bin/arcforges`.
4. **Install the units:** write the units of §3.4 to `~/.config/systemd/user/`, then run `systemctl --user daemon-reload` and `systemctl --user enable --now arcforges-node.service`.
5. **Confirm:** run `arcforges node wait-ready --timeout 30`, then print the status, the capability summary and the `loginctl enable-linger` guidance for headless use.
6. **Uninstall:** `install.sh --uninstall [--remove-data]` reverses the steps.

### 3.3 Debian package

- **Files:** `/opt/arcforges/<v>/…`, `/usr/bin/arcforges` → `/opt/arcforges/current/arcforges`, and the units of §3.4 under `/usr/lib/systemd/user/`, with `ExecStart=/usr/bin/arcforges node run --systemd`.
- **Maintainer scripts:** limited to `systemctl --global enable arcforges-node.service` (postinst) and its reverse. They use no network ([11](11-security-privacy.md) §6).
- **Updates:** through apt (repository signed with GPG). The node's self-updater disables itself when it detects a package-managed install (`/opt/arcforges` owned by root), and reports "updates are managed by apt".

### 3.4 systemd user units

`arcforges-node.service`:

```ini
[Unit]
Description=ArcForges node
Documentation=https://arcforges.com/docs
OnFailure=arcforges-node-rollback.service
StartLimitIntervalSec=600
StartLimitBurst=5

[Service]
Type=notify
NotifyAccess=main
ExecStart=%h/.local/share/arcforges/app/current/arcforges node run --systemd
Restart=on-failure
RestartSec=2
RestartForceExitStatus=75
SuccessExitStatus=75
TimeoutStopSec=30

[Install]
WantedBy=default.target
```

`arcforges.slice`:

```ini
[Unit]
Description=ArcForges managed executions

[Slice]
```

`arcforges-node-rollback.service`:

```ini
[Unit]
Description=ArcForges update rollback

[Service]
Type=oneshot
ExecStart=%h/.local/share/arcforges/app/previous/arcforges node update-rollback --restart
```

- **Executions are not in the node unit.** They are transient units in `arcforges.slice` ([AD-0005](../decisions/AD-0005-resource-enforcement.md) Linux §2). Stopping or restarting `arcforges-node.service` kills only the node and its own short-lived helpers (the default `KillMode=control-group`). Executions keep running, except `kill_with_node` tasks, which are bound to the node unit with `BindsTo=`.
- **Slice limits.** The slice's limits are runtime properties set by the node, so the unit file carries none.
- **Readiness.** `Type=notify` with `sd_notify("READY=1")` after startup step 9 ([02](02-node-service.md) §2).
- **Restart after an update.** Exit code 75 means "restart me": `RestartForceExitStatus` restarts the node, and `SuccessExitStatus` keeps the exit from being logged as a failure (§5.3).

### 3.5 First run

1. **The node** creates its data root ([06](06-storage-workspaces.md) §1), node identity, store, default policy and capability report.
2. **The Desktop** runs its first-run flow (page D-00 in [experience/desktop.md](../experience/desktop.md)):
   - capability summary;
   - optional sign-in;
   - AI-client integration plan;
   - a demonstration task.

## 4. Release manifest

`https://releases.arcforges.com/<channel>/manifest.json` (R2, cached at the edge for at most 5 minutes):

```json
{
  "schema": 1,
  "channel": "stable",
  "published_at": "2026-10-12T00:00:00Z",
  "expires_at": "2026-11-11T00:00:00Z",
  "latest": "1.2.0",
  "revoked": ["1.1.3"],
  "min_supported": "1.0.0",
  "releases": [
    {
      "version": "1.2.0",
      "notes_url": "https://arcforges.com/releases/1.2.0",
      "artifacts": [
        {"rid": "win-x64", "kind": "zip", "url": "https://releases.arcforges.com/1.2.0/arcforges-1.2.0-win-x64.zip",
         "size": 41234567, "sha256": "<64 hex>"}
      ],
      "store_schema": {"writes": 7, "min_reader": 6}
    }
  ]
}
```

- **Signature.** `manifest.json.sig` holds the key ID (`kid`) and an Ed25519 signature over the exact manifest bytes. The updater, `install.sh` and the MSI embed the public key set: at most two active keys, rotated through releases.
- **Validity.** A manifest is refused in either case:
  - `expires_at` has passed (protection against freeze attacks);
  - `published_at` is older than the last accepted manifest (rollback protection; the node stores the last accepted timestamp).
- **Revocation.** A revoked version is never installed. A node running a revoked version notifies the user, then updates to `latest` regardless of the policy window.
- **`min_supported`.** Versions below it show a persistent banner, "unsupported: update required for cloud features", and the cloud refuses their relay tokens.

## 5. Node-driven updates

### 5.1 Policy

`updates` policy:
- `mode`: `AUTO` (default), `NOTIFY` or `MANUAL`;
- `channel`;
- `window`: time ranges, default any time;
- `metered`: `DEFER` (default; Windows only, from the connection cost API) or `ALLOW`.

### 5.2 Check and stage

1. **Check:** at most every 6 h (jittered by ±30 min), plus on `UpdateService.CheckNow`.
2. **Choose:** the highest non-revoked version above the current one in the channel, for this RID.
3. **Download:** into `downloads/updates/<v>/` with HTTP range resume, and verify the artifact SHA-256.
4. **Extract and verify:** extract to `app/.staging-<v>/`. On Windows, verify each binary's Authenticode signature and its chain to the expected publisher. Development-stage tests use test certificates under an explicit test trust flag.
5. **Self-test the staged binary:** run `app/.staging-<v>/arcforges node self-test --staged`. It covers start-up, store read compatibility (§6) and platform probes, without opening the node endpoint.
6. **Mark staged:** rename to `app/<v>/` and mark it `STAGED`.

### 5.3 Switch and restart

1. **Announce.** When the policy window opens, or the user chooses **Restart now**, the node announces `UPDATE_PENDING` to clients. The Desktop shows a 60-second countdown with a **Postpone** button.
2. **Record the switch.** The node writes `run/update-switch.json {from, to, phase, attempt_count}`, then points `previous` at the running version and `current` at `<v>`:
   - **Linux:** create symlink `app/.next` → `<v>`, then `rename()` it over `app/current`. This is atomic.
   - **Windows:** create junction `app\.next` → `<v>`, then `MoveFileEx(.next, current, MOVEFILE_REPLACE_EXISTING)`. Junction replacement is not guaranteed atomic, so startup recovery completes or reverts any half-finished switch it finds recorded in `update-switch.json`.
3. **Restart the node.**
   - **Linux:** the node runs shutdown ([02](02-node-service.md) §2) and exits with code 75. systemd restarts it from the new `current` (§3.4).
   - **Windows:** the node runs shutdown and exits with code 75. The supervisor starts the new `current\arcforges.exe node run`, then hands itself over: it starts `current\arcforges-supervisor.exe --adopt <node pid>` and exits, so no process keeps running from the old version directory.
   - **Executions:** unaffected on both platforms. They live in their own containers (Windows jobs without kill-on-close; Linux transient units), and their exit records are durable (R-EXE-008, A-L03).

### 5.4 Health check, commit and rollback

- **Health check.** Within 120 s the new node must:
  - complete startup, including recovery of every surviving execution;
  - pass the enforcement self-test;
  - answer a client handshake.

  It then writes phase `HEALTHY` to `update-switch.json`.
- **Commit.** The node marks `<v>` `ACTIVE` and the previous version `PREVIOUS`. It deletes versions older than the last two once no process holds files in them. On Windows that is checked by attempting to rename the directory; a failed attempt is retried hourly.
- **Rollback triggers:**
  1. The new node detects an unrecoverable condition, such as a store incompatibility or a failed self-test.
  2. The node fails to reach `HEALTHY` within 120 s.
  3. The node crash-loops: systemd's start limit (5 in 10 minutes) fires `OnFailure`, or the Windows supervisor counts 3 failed starts within 5 minutes of a switch.
- **Rollback mechanism.**
  - **Linux:** `arcforges-node-rollback.service` runs `app/previous/arcforges node update-rollback --restart`.
  - **Windows:** the supervisor runs the equivalent steps from the previous version.
  - **Steps:**
    1. Switch `current` back to `previous`.
    2. Mark `<v>` `BAD`. It is not retried until a newer manifest lists a higher version.
    3. Restart the previous node (Linux also resets the unit's failed state).
    4. Raise the finding `UPDATE_FAILED` with the reason.

### 5.5 Clients

- **CLI, hook handlers and MCP adapters** start from `app/current` at launch. Long-running MCP adapters keep their old binary until the AI client restarts them. Version skew is tolerated within the contract major, and `Hello` reports it.
- **Desktop** shows "Restart Desktop to update" and re-execs from `current` on confirmation.

## 6. Store migrations and rollback safety

- **Expand–contract.** Store migrations are forward-only SQL scripts, and each release's migrations are **expand-only**: new tables, new nullable columns, new indexes. Contract steps (drop or rename) happen only in a later release, once `min_reader` excludes every version still eligible as a rollback target.
- **Reader check.** `store_meta` records `schema_version` (written) and `min_reader_version`. A binary refuses to open a store whose `min_reader_version` is above its own supported schema, so a rolled-back binary never misreads a contracted store.
- **Backups.** Before migrating, the node checkpoints SQLite (`wal_checkpoint(TRUNCATE)`) and copies the database to `records/backups/store-<from>-<to>-<timestamp>.db`, keeping the last three ([02](02-node-service.md) §2 step 3).

## 7. Package-manager and AI-client routes (R-DIST-005)

| Route | Artifact | Publication |
|---|---|---|
| winget | Manifest referencing the MSI URL and SHA-256 | PR to `microsoft/winget-pkgs` (release task; human account) |
| Scoop | Bucket manifest referencing the zip and its hash | ArcForges bucket repository |
| apt | Repository with a signed `Release` file | R2 static hosting, signed with the apt GPG key (human custody) |
| Claude Code plugin | Marketplace plugin: `.mcp.json` (runs `arcforges mcp serve`), hooks configuration and a skill | Plugin marketplace repository. Installing it does not install the native node; the hooks print guidance when `arcforges` is missing (R-DIST-004). |
| Codex plugin | Plugin with MCP server configuration and a skill | Codex plugin distribution; same rule |

## 8. Android release

- **Build and signing.** The Mobile repository's CI builds the AAB with R8 and AOT. It is signed with the upload key (human custody) and released through Play App Signing.
- **Tracks:** internal testing → closed testing → production.
- **Development channel.** Signed APK prereleases on GitHub Releases remain a development channel. They do not offer subscriptions, because Play Billing requires a Play install.

## 9. Tests

| Test | Kind |
|---|---|
| MSI install, upgrade and uninstall on a separate per-user data root on the workstation; a fresh second Windows account is deferred (acceptance register) | Real, workstation |
| `install.sh` and `.deb` in a clean systemd-enabled WSL2 Debian environment | Real |
| Update switch with running executions on both platforms; crash injection at each switch phase; health-check failure; crash-loop rollback | Real |
| Manifest signature, expiry, freeze and rollback protection, revocation | Unit, plus closed-loop tests with a local HTTP server |
| Expand-only migration check: a schema diff tool fails on any drop or rename in a release | CI |
| Production signing, SmartScreen reputation, winget and apt publication | Deferred (acceptance register) |
