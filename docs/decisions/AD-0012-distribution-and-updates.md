# AD-0012 — Distribution, signing, updates and rollback

- Status: Accepted (2026-10-12)

## Decision

1. **Install layout (per user, no administrator rights):**

| Platform | Root | Layout |
|---|---|---|
| Windows | `%LOCALAPPDATA%\ArcForges\` | `app\<version>\arcforges.exe`, `app\<version>\arcforges-supervisor.exe`, `app\<version>\arcforges-desktop.exe` (optional); `app\previous` (junction to the rollback version); `app\current` (directory junction to the active version, and the only ArcForges entry on the user PATH); `data\` (default node data root) |
| Linux | `~/.local/share/arcforges/` | `app/<version>/arcforges`, `app/current` and `app/previous` (symlinks); `~/.local/bin/arcforges` (symlink to `app/current/arcforges`); `~/.config/systemd/user/arcforges-node.service`, `arcforges.slice` and `arcforges-node-rollback.service`; data root `~/.local/share/arcforges/data/` |

   Version directories are read-only for managed tasks (AD-0007 §8).
2. **Installers.**
   - **Windows:** a signed per-user MSI (WiX Toolset authoring; installer tooling, not product logic) that:
     - installs the first version directory and the `current` junction;
     - sets the user PATH and writes the `HKCU\...\Run` autostart for `arcforges-supervisor.exe` (AD-0003 §1);
     - registers uninstall (which stops the node, removes app files and keeps the data root unless the user ticks "remove data");
     - installs the Desktop only when the "Desktop app" feature is selected (default on for interactive installs).

     A machine-wide service mode (administrator) is a separate optional MSI feature.
   - **Linux:** `install.sh` (user-level; verifies the signed manifest before extracting) and a `.deb` package (system-wide binaries in `/opt/arcforges/<version>` plus a user unit file under `/usr/lib/systemd/user/`). Both enable the user unit, and print the `loginctl enable-linger` guidance for headless hosts.
3. **Signing.**
   - Windows binaries and the MSI: Authenticode. Release artifacts: SHA-256 digests in a **release manifest signed with Ed25519** (offline release key; custody is a human prerequisite).
   - Linux: the apt repository is signed with GPG, and the manifest signature is verified by `install.sh` and the updater.
   - Android: Play App Signing with an upload key.
   - Test keys are used for development-stage tests and are never shipped.
4. **Updates (node-driven).**
   1. The node checks `releases.arcforges.com/<channel>/manifest.json` (R2 static) at most every 6 h, or on demand. It downloads with resume, verifies the manifest signature and artifact digests, and stages into `app/<version>/`.
   2. When the policy window allows (default: immediately; managed executions survive restarts, R-EXE-008), it switches `current` atomically: Linux creates a new symlink and renames it over; Windows retargets the junction through a temporary name and a verified rename, with startup recovery.
   3. It restarts its own roles through the service registration and runs a health check: a node API handshake, store open and enforcement self-test.
   4. **Rollback:** a failed health check within 120 s restores the previous `current` and marks the version bad. The last two versions are kept.
   5. The Desktop and the MCP adapter re-exec on their next start.
5. **Channels.** `stable`, `beta` and `dev`. The release manifest can mark a version as revoked, and the updater then moves away from it.
6. **Package-manager and plugin routes.** A winget manifest (MSI), a Scoop manifest (zip of the version directory with the same signature), an apt repository, a Claude Code plugin marketplace entry and a Codex plugin. These install or configure, but the native node is installed only by the platform installers or package managers, never by an AI-client plugin (R-DIST-004).
7. **Android distribution.** Google Play (AAB, Play App Signing). Signed APK prereleases on GitHub Releases stay as a development channel.
