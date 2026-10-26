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
| `arcforges-setup-<v>-win-x64.exe`, `-win-arm64.exe` | Per-user setup program (§3.1) |
| `arcforges-<v>-win-x64.zip`, `-win-arm64.zip` | Version directory (Scoop, updater payload) |
| `arcforges-<v>-linux-x64.tar.zst`, `-linux-arm64.tar.zst` | Version directory (`install.sh`, updater payload) |
| `arcforges_<v>_amd64.deb`, `_arm64.deb` | System package (§3.3) |
| `install.sh` | User-level installer script (versioned with the release) |
| `manifest.json`, `manifest.json.sig` | Release manifest and its ES256 signature (§4) |
| `sbom.cdx.json` | CycloneDX SBOM ([11](11-security-privacy.md) §6) |

- **Windows version directory:** `arcforges.exe`, `arcforges-supervisor.exe`, `arcforges-setup.exe` (uninstall and repair), and `arcforges-desktop.exe` with its native Avalonia/Skia libraries.
- **Linux version directory:** `arcforges` and `arcforges-desktop` with its native libraries.
- **Both:** `digests.json`, written by the packaging step: `{"version": "<v>", "files": {"<relative path, / separators>": "<SHA-256 hex>", …}}` for every file of the version directory except itself. The node checks its version directory against it ([AD-0007](../decisions/AD-0007-ai-integration.md) §8; added 2026-10-23, AF-SEC-01).
- **Android:** released separately through Google Play (§8).

## 3. Installation

### 3.1 Windows (per-user setup program; no administrator rights)

- **Program.** `arcforges-setup-<v>-<rid>.exe` (project `ArcForges.Setup`; Native AOT; GUI subsystem; Authenticode-signed). It shares the staged-switch engine with the node updater (`ArcForges.Node.Updates`), so first install, upgrade and self-update use one code path ([AD-0012](../decisions/AD-0012-distribution-and-updates.md) §2).
- **Platform check.** The setup program refuses Windows versions before Windows 11 with a message that names the reason (TLS 1.3 for LAN, end of support; [AD-0002](../decisions/AD-0002-platform-scope.md)).
- **Options (pages):**
  - **Core** (always): version directory, the `current` and `previous` junctions, PATH entry, autostart and uninstall entry;
  - **Desktop** (default on): `arcforges-desktop.exe`, a Start menu shortcut and an optional Desktop shortcut;
  - **Set up AI clients** (default off): opens the Desktop first-run integration step. It never writes client configuration without consent (R-AI-008).
- **Registrations.**
  - `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\ArcForgesNode` = `"%LOCALAPPDATA%\ArcForges\app\current\arcforges-supervisor.exe"`. The supervisor is a GUI-subsystem executable, so logon shows no console window. It starts `arcforges.exe node run` with `CREATE_NO_WINDOW` (AD-0003 §1; A-N03).
  - `HKCU\Environment\Path` gets `%LOCALAPPDATA%\ArcForges\app\current` appended, followed by a `WM_SETTINGCHANGE` broadcast.
  - `HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\ArcForges` is written by the setup program with:
    - `DisplayName`, `DisplayVersion` (kept current by the updater), `Publisher`, `InstallLocation` and `EstimatedSize`;
    - `UninstallString` = `"…\app\current\arcforges-setup.exe" --uninstall` and `QuietUninstallString`;
    - `NoModify` and `NoRepair`.
  - `HKCU\Software\ArcForges\InstallSource` = `setup`, `winget` (set by `--source winget` from the winget manifest) or `scoop` (Scoop installs the portable zip and runs `arcforges-setup --register-scoop`, which skips the updater) ([AD-0012](../decisions/AD-0012-distribution-and-updates.md) §4).
- **After install:** start `arcforges-supervisor.exe`, then `arcforges node wait-ready --timeout 30`.
- **Uninstall.**
  - **Steps:**
    1. `arcforges node stop --reason uninstall --timeout 60`; running managed executions are listed, and the user chooses to wait or to cancel them all (R-DIST-001).
    2. Stop the supervisor and the Desktop app, which also run from `app\current`.
    3. The setup program copies itself to `%TEMP%`, relaunches from there and exits, so no running image remains under `app\`.
    4. The copy removes **every** `app\*` version directory, both junctions, the PATH entry, the Run key, `InstallSource` and the uninstall entry. The copy stays in `%TEMP%`, where the system's temporary-file cleanup (Storage Sense) removes it. A reboot-time delete (`MOVEFILE_DELAY_UNTIL_REBOOT`) is not used, because it needs administrator rights.
    5. *Added 2026-10-19 (step 4 omitted them):* it also removes the Start menu shortcut, the optional Desktop shortcut and the toast notification registration (AUMID); replays the recorded integration writes in reverse ([AD-0007](../decisions/AD-0007-ai-integration.md) §6), so no AI-client entry ArcForges wrote remains; and deletes the node's own Credential Manager entries by exact name, one at a time.
  - **Data:** the data root is kept unless the user ticks **Remove ArcForges data**, which runs `arcforges node wipe --scope all` first; the uninstaller's own confirmation stands in for the command's interactive prompt (corrected 2026-10-19 to the CLI's `--scope` syntax, [cli](../experience/cli.md)). The node's own credentials are removed in either case (step 5). A reinstall over a kept data root therefore finds no node credential or data key: values sealed under the old key fail closed ([04](04-execution.md) §2), and the node must re-enroll ([AD-0011](../decisions/AD-0011-identity-and-login.md) §2).
  - **Test tier:** uninstall tests use the isolated secret-store backend; one real-store check of the exact-name deletion runs in the separate, sequential OS secret-store tier ([AD-0016](../decisions/AD-0016-local-first-verification.md) §5 and its 2026-10-17 amendment; [16](16-testing-strategy.md) §1).
- **Test isolation.** For automated tests, `--test-root <dir> --test-registry-key HKCU\Software\ArcForges-Test` installs under a temporary root and registry key, never touching the user's real Run key, PATH or uninstall entry. The real logon start of the supervisor is a human-attended check (H-15).
- **Machine-wide service mode** is out of the current scope (AR-16). It would be a separate per-machine installer.

### 3.2 Linux user install (`install.sh`)

1. **Check prerequisites:** the architecture, systemd user sessions (`systemctl --user is-system-running` reports any state other than `offline`), cgroup v2 and glibc ≥ 2.31. Missing systemd or cgroup v2 is reported as degraded enforcement ([03](03-resource-control.md) §8), not as an install failure.
2. **Download and verify:** fetch `manifest.json` and its `.sig` from the channel URL, verify the signature with the embedded public key, then download the tarball and verify its SHA-256.
3. **Extract:** into `~/.local/share/arcforges/app/<v>/`, then create `app/current` and `~/.local/bin/arcforges`.
4. **Install the units:** write the units of §3.4 to `~/.config/systemd/user/`, then run `systemctl --user daemon-reload` and `systemctl --user enable --now arcforges-node.service arcforges-guard.service`.
5. **Confirm:** run `arcforges node wait-ready --timeout 30`, then print the status, the capability summary and the `loginctl enable-linger` guidance for headless use.
6. **Uninstall:** `install.sh --uninstall [--remove-data]` reverses the steps. It also removes the node's own Secret Service items, or its 0600 fallback file, by exact name (added 2026-10-19), under the test tier of §3.1.

### 3.3 Debian package

- **Files:** `/opt/arcforges/<v>/…`, `/usr/bin/arcforges` → `/opt/arcforges/current/arcforges`, and the units of §3.4 under `/usr/lib/systemd/user/`, with `ExecStart=/usr/bin/arcforges node run --systemd` for the node and `ExecStart=/usr/bin/arcforges node guard` for the guard.
- **Maintainer scripts:** limited to `systemctl --global enable arcforges-node.service arcforges-guard.service` (postinst) and its reverse. They use no network ([11](11-security-privacy.md) §6).
- **Removal and per-user secrets** (added 2026-10-19). Package removal runs as root, outside any user's session, and its maintainer scripts are limited to the step above, so removing the package cannot remove any user's node secrets. Each user removes them first with a user-level step: `arcforges node wipe --scope all` (`WipeNode`, scope `ALL`: everything in the data root, including the node's identity and credentials) deletes the node's own Secret Service items, or its 0600 fallback file, by exact name, under the test tier of §3.1. A user who skips that step before `apt remove` keeps them.
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
WatchdogSec=30
TimeoutAbortSec=5s
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

`arcforges-guard.service` (the disk guard for running executions while the node is down; [06](06-storage-workspaces.md) §5):

```ini
[Unit]
Description=ArcForges disk guard for running executions
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=%h/.local/share/arcforges/app/current/arcforges node guard
Restart=always
RestartSec=2

[Install]
WantedBy=default.target
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
- **Watchdog.** `WatchdogSec=30`: the node's enforcement loop sends `WATCHDOG=1` with each heartbeat, so a hung node is killed and restarted ([06](06-storage-workspaces.md) §5). `TimeoutAbortSec=5s` bounds the abort: the .NET runtime does not always exit promptly on the watchdog's SIGABRT, so systemd sends SIGKILL after 5 s. Measured restart after a hung enforcement loop: about 35 s; after a hung cache-store probe (three missed 5 s probes first), about 49 s (L-25).
- **Rollback hook.** `OnFailure=` and `arcforges-node-rollback.service` are installed together by the updater task. Until then the shipped node unit omits the `OnFailure=` line, so a crash does not try to enqueue a missing unit (the node unit's own restart is unaffected either way).
- **Restart after an update.** Exit code 75 means "restart me": `RestartForceExitStatus` restarts the node, and `SuccessExitStatus` keeps the exit from being logged as a failure (§5.3).
- **Guard.** `arcforges-guard.service` is independent of the node unit, so it keeps guarding executions while the node is stopped, failed or restarting. After an update switch the node restarts it from the new `current` while the node itself is up.

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

- **Signature.** `manifest.json.sig` is JSON `{"kid": "…", "alg": "ES256", "sig": "<base64 DER ECDSA signature>"}` over the exact manifest bytes.
  - **Verifiers:** the updater (.NET `ECDsa.VerifyData` with `Rfc3279DerSequence`), the setup program, and `install.sh` (`openssl dgst -sha256 -verify <embedded pem> -signature <der>`; the script refuses to install when `openssl` is missing and says how to install it).
  - **Keys:** at most two active public keys, embedded in releases and rotated through them.
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
2. **Record the switch.** The node writes `run/update-switch.json {from, to, phase, switched_at, attempt_count}` before each step, then points `previous` at the running version and `current` at `<v>`. The phases are `staged`, `previous_set`, `current_set`, `started` and `healthy`.
   - **Linux:** create symlink `app/.next` → `<v>`, then `rename()` it over `app/current` (atomic). `previous` is set the same way.
   - **Windows:** retarget the existing `app\current` junction in place. Open it with `FILE_FLAG_OPEN_REPARSE_POINT | FILE_FLAG_BACKUP_SEMANTICS` and call `FSCTL_SET_REPARSE_POINT` with mount-point data for `app\<v>`. This works without elevation and replaces the target in one operation (L-16). Replacing a junction with `MoveFileEx` fails (error 5), so it is never used. `previous` is retargeted the same way.
   - **Crash recovery:** on start, the node (or, on Windows, the supervisor) reads `update-switch.json` and completes or reverts a switch that stopped between phases.
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
- **Rollback triggers** (only for a switch that is recent and not yet `healthy`):
  1. The new node detects an unrecoverable condition, such as a store incompatibility or a failed self-test.
  2. The node fails to reach `HEALTHY` within 120 s.
  3. The node crash-loops: systemd's start limit (5 in 10 minutes) fires `OnFailure`, or the Windows supervisor counts 3 failed starts within 5 minutes of a switch.
- **Recent-switch guard.** `arcforges-node-rollback.service` (via `OnFailure`) and the supervisor act only when `update-switch.json` shows a switch in the last 15 minutes that never reached `healthy`. A crash loop unrelated to an update leaves the unit failed, writes a log entry and lets the next client auto-start try again. It never rolls back a healthy version.
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
  **Amended 2026-10-26 (MR-13):** retained backups never carry sealed environment values. The temporary SQLite copy replaces all
  live `task_secret` payloads with purged tombstones, zeros overwritten content, compacts the copy and checks integrity before
  rename/publish. Existing retained copies from older binaries are sanitized on store open before any migration or node startup;
  their nonsecret records and schema versions stay intact. If a retained copy is corrupt, locked or cannot be sanitized, opening
  fails with a backup error instead of silently retaining recoverable values. A task requiring sealed input after a backup
  restore fails closed with `secrets_unavailable` and needs a new submission; backups preserve records, not a second lifetime
  for the sealed input. This is a retention repair using existing tables and tombstones, not a new schema migration. It does
  not delete or rotate the node data key or access credential-store/orphan-credential files.

## 7. Package-manager and AI-client routes (R-DIST-005)

| Route | Artifact | Publication |
|---|---|---|
| winget | Manifest (installer type `exe`) referencing the setup program URL and SHA-256, with silent switches `--silent --source winget` | PR to `microsoft/winget-pkgs` (release task; human account) |
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
| Setup program install, upgrade (as a self-update and as a newer setup) and uninstall, under `--test-root` and a test registry key on the workstation; a clean machine is deferred (AR-01); the real logon start needs a human logoff and logon (H-15). Uninstall leaves no shortcut, AUMID registration or recorded integration write, and deletes the node's own credentials by exact name, against the isolated secret-store backend (§3.1, test tier; added 2026-10-19) | Real, workstation |
| `install.sh` and `.deb` in a clean, systemd-enabled native Linux environment (a container or a fresh user on a native Linux host; [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md) §5). `install.sh --uninstall`, and for the `.deb` the user-level `arcforges node wipe --scope all` before package removal, delete the node's own Secret Service items or 0600 fallback file by exact name, against the isolated backend; package removal alone leaves them (added 2026-10-19) | Real |
| One real-store check of the uninstall's exact-name deletion per platform (added 2026-10-19) | OS secret-store tier ([16](16-testing-strategy.md) §1) |
| Update switch with running executions on both platforms; crash injection at each phase of `update-switch.json`; junction retarget recovery; health-check failure; crash-loop rollback; the recent-switch guard refusing rollback of a healthy version; ownership rules per install source (Scoop and apt disable the updater) | Real |
| Manifest signature, expiry, freeze and rollback protection, revocation | Unit, plus closed-loop tests with a local HTTP server |
| Expand-only migration check: a schema diff tool fails on any drop or rename in a release | CI |
| Production signing, SmartScreen reputation, winget and apt publication | Deferred (acceptance register) |
