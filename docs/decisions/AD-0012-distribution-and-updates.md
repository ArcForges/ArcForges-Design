# AD-0012 — Distribution, signing, updates and rollback

- Status: Accepted (2026-10-12; revised after the independent review the same day: per-user setup program instead of MSI, update ownership per install source, in-place junction retarget, ES256 manifests)

## Decision

1. **Install layout (per user, no administrator rights):**

| Platform | Root | Layout |
|---|---|---|
| Windows | `%LOCALAPPDATA%\ArcForges\` | `app\<version>\` (`arcforges.exe`, `arcforges-supervisor.exe`, `arcforges-setup.exe`, optional `arcforges-desktop.exe`); `app\current` and `app\previous` (directory junctions; `current` is the only ArcForges entry on the user PATH); `data\` (default node data root) |
| Linux | `~/.local/share/arcforges/` | `app/<version>/arcforges`, `app/current` and `app/previous` (symlinks); `~/.local/bin/arcforges` (symlink to `app/current/arcforges`); `~/.config/systemd/user/arcforges-node.service`, `arcforges.slice` and `arcforges-node-rollback.service`; data root `~/.local/share/arcforges/data/` |

   Version directories are installed read-only and verified by digest at node start (AD-0007 §8).
2. **Installers.**
   - **Windows: a per-user setup program.** `arcforges-setup-<v>-<rid>.exe` is a Native AOT, GUI-subsystem C# program, project `ArcForges.Setup`, signed with Authenticode. A Windows Installer package is not used: the node updates itself, and an MSI-owned product registration would go stale after the first self-update.
     - **Install** puts the version directory in place, sets the junctions (`FSCTL_SET_REPARSE_POINT`, L-16), the user PATH and the `HKCU\...\Run` autostart for `arcforges-supervisor.exe` (AD-0003 §1), and writes its **own** uninstall entry under `HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\ArcForges`. The updater keeps `DisplayVersion` current there.
     - **Uninstall** stops the node, the supervisor and the Desktop app, relaunches the setup program from `%TEMP%` (so no running image remains in a version directory), then removes every `app\*` version directory, both junctions, the PATH entry, the Run key and the uninstall entry. It keeps the data root unless the user chooses to remove it.
     - **Desktop** is installed when selected (default on for interactive installs).
     - **Silent mode** (`--silent`) is used by winget.
     - **Machine-wide service mode** (administrator) is out of the current scope (AR-16). It would be a separate per-machine installer.
   - **Linux:** `install.sh` (user-level; verifies the signed manifest before extracting) and a `.deb` package (system-wide binaries in `/opt/arcforges/<version>`, plus a user unit file under `/usr/lib/systemd/user/`). Both enable the user unit, and print the `loginctl enable-linger` guidance for headless hosts.
3. **Signing.**
   - **Windows:** binaries and the setup program are signed with Authenticode.
   - **Release manifest:** artifacts are listed with their SHA-256 digests in a **release manifest signed with ES256** (ECDSA P-256 with SHA-256; a DER-encoded signature, so `openssl dgst -verify` can check it; .NET has no built-in Ed25519, V-N05). The release key is held offline; its custody is a human prerequisite.
   - **Linux:** the apt repository is signed with GPG. `install.sh` verifies the manifest with `openssl`; the updater uses .NET's `ECDsa`.
   - **Android:** Play App Signing with an upload key.
   - **Test keys** are used for development-stage tests and are never shipped.
4. **Updates (node-driven) and their ownership per install source.** Update ownership is decided by `install_source`, recorded at install time (`HKCU\Software\ArcForges\InstallSource`, or `store_meta` on Linux):

| `install_source` | Who updates | Notes |
|---|---|---|
| `setup` (direct download) | Node updater | The updater keeps the uninstall entry's `DisplayVersion` current |
| `winget` | Node updater | winget reads the current `DisplayVersion`. `winget upgrade` runs the newer setup program, which hands over to the same staged-switch engine. |
| `scoop` | Scoop | Scoop owns its app directories. The node's updater is disabled and reports "managed by Scoop". |
| `install.sh` | Node updater | — |
| `deb` | apt | The node's updater is disabled and reports "managed by apt" |

   The node updater works as follows ([13](../architecture/13-distribution-updates.md) §5):
   1. **Check and stage.** It checks `releases.arcforges.com/<channel>/manifest.json` at most every 6 h, or on demand. It downloads with resume, verifies the manifest signature and artifact digests, and stages into `app/<version>/`.
   2. **Switch.** When the policy window allows (default: immediately; managed executions survive restarts, R-EXE-008), it switches `current` atomically:
      - **Linux:** rename a new symlink over the old one.
      - **Windows:** retarget the existing junction in place with `FSCTL_SET_REPARSE_POINT` (L-16). Replacing a junction with `MoveFileEx` fails.

      Each step is recorded in `run/update-switch.json` for crash recovery.
   3. **Health check.** It restarts its own roles and runs a health check: a node API handshake, store open, the enforcement self-test, and recovery of surviving executions.
   4. **Rollback.** A failed health check within 120 s, or a crash loop right after a switch, restores the previous `current` and marks the version bad. The last two versions are kept.
   5. **Clients.** The Desktop and the MCP adapter re-exec on their next start.
5. **Channels.** `stable`, `beta` and `dev`. The release manifest can mark a version as revoked, and the updater then moves away from it.
6. **Package-manager and plugin routes.** A winget manifest (installer type `exe`, the setup program with `--silent`), a Scoop manifest (zip of the version directory with the same signature), an apt repository, a Claude Code plugin marketplace entry and a Codex plugin. These install or configure, but the native node is installed only by the platform installers or package managers, never by an AI-client plugin (R-DIST-004).
7. **Android distribution.** Google Play (AAB, Play App Signing). Signed APK prereleases on GitHub Releases stay as a development channel.
