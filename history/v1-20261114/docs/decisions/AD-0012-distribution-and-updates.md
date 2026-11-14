# AD-0012 — Distribution, signing, updates and rollback

- Status: Accepted (2026-10-12; revised after the independent review the same day: per-user setup program instead of MSI, update ownership per install source, in-place junction retarget, ES256 manifests; amended 2026-10-19 by the current-design corrections: the uninstall also removes the Start-menu and Desktop shortcuts, the toast AUMID registration, the recorded integration writes and the node's own credential entries, and the `.deb` limit on per-user secrets is stated, §2; amended 2026-10-19 by AD-0017: direction only: `install_source` will become `update_owner` at EX-13 stage b, probe reference data will travel as signed release-manifest data at EX-11, and a macOS stable-bundle-path rule at RM-15, relabelled 2026-10-19 by AD-0017 as amended as a candidate for macOS development, not a current decision)

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
       - *Amended 2026-10-19:* the list above omitted writes ArcForges itself makes. The uninstall also removes the Start-menu shortcut and the optional Desktop shortcut and the toast notification registration (AUMID); replays the recorded integration writes in reverse (AD-0007 §6); and deletes the node's own Credential Manager entries by exact name, one at a time, whether or not the data root is kept. A reinstall over a kept data root then finds no node credential or data key, so the sealed task secrets fail closed ([04](../architecture/04-execution.md) §2) and the node must re-enroll.
     - **Desktop** is installed when selected (default on for interactive installs).
     - **Silent mode** (`--silent`) is used by winget.
     - **Machine-wide service mode** (administrator) is out of the current scope (AR-16). It would be a separate per-machine installer.
   - **Linux:** `install.sh` (user-level; verifies the signed manifest before extracting) and a `.deb` package (system-wide binaries in `/opt/arcforges/<version>`, plus a user unit file under `/usr/lib/systemd/user/`). Both enable the user unit, and print the `loginctl enable-linger` guidance for headless hosts. *Amended 2026-10-19:* `install.sh --uninstall`, which runs as the user, also removes the node's own Secret Service items, or its 0600 fallback file, by exact name. Removing the `.deb` runs as root outside any user's session and cannot remove them; each user removes them first with the user-level `arcforges node wipe --scope all` ([13](../architecture/13-distribution-updates.md) §3.3).
   - **Uninstall tests** (amended 2026-10-19) use the isolated secret-store backend; one real-store check of the exact-name deletion runs in the separate, sequential OS secret-store tier ([AD-0016](AD-0016-local-first-verification.md) §5 and its 2026-10-17 amendment).
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

## Direction (roadmap; not release 1)

Amended 2026-10-19 by [AD-0017](AD-0017-delegated-execution-direction.md). §1–§7 bind release 1 unchanged. Each item below takes effect only with its roadmap row:
1. **`install_source` will become `update_owner`** (effective when EX-13 stage b is promoted). Every Installation, ArcForges' own included, will record **exactly one** owner of its updates, decided before installation: **ARCFORGES** (OWNED; the switch, health check and rollback of §4 apply), **MANAGER** (a package or tool manager that owns updates, as Scoop and apt do for ArcForges itself in the table of §4, or, for other software, winget, Flatpak, Homebrew, a delegated tool manager, or a distribution package manager in a transaction the owner runs and approves; ArcForges reports and records) or **VENDOR** (an application's own updater; ArcForges reports). A third-party application whose own updater replaces its install root cannot be OWNED, because read-only version directories forbid that; it is DELEGATED with rollback NONE, or refused. ArcForges never forcibly disables a vendor updater ([17](../architecture/17-delegated-execution.md) §6.4).
2. **Probe reference data will travel as signed release-manifest data** (effective when EX-11 is promoted). The exact fixed-revision lists for distribution packages such as bwrap, the Landlock ABI tables and similar data that the isolation probe compares against will be carried in the signed release manifest of §3. Where the node's updater runs (`setup`, `winget`, `install.sh`), the update check of §4 already fetches that manifest, so the probe needs no new outbound lookup. For package-managed installs (`scoop`, `deb`), whose updater is disabled (§4; [13](../architecture/13-distribution-updates.md) §3.3), how the data arrives without a new outbound lookup (for example, shipped in the package) is decided at EX-11's promotion. An unknown revision counts as unfixed. The owner of the data is named at EX-11's promotion ([17](../architecture/17-delegated-execution.md) §5.2).
3. **A candidate for macOS development, not a current decision** (relabelled 2026-10-19, by the product owner's instruction of 2026-10-19: "Do not make Apple hardware purchasing, developer-program enrollment, specific lab setup, architecture coverage, or detailed implementation decisions now. Those belong to actual macOS development later."). Kept as a fact: TCC and Local Network grants may be keyed to the path and the signature (D-macos-32 of the [research record](../research/2026-10-18-delegated-execution/evidence/macos.md)). The signing, notarization, bundle-path and layout design of the macOS node is decided when macOS development starts; the questions LAB-MAC-07 asks (a per-version directory with a `current` link, a bundle replaced in place, or a binary replaced at a stable path) stay open for then. *Superseded:* "**The macOS stable-bundle-path rule** (effective when RM-15 is promoted). The macOS node will be a Developer-ID-signed, notarized bundle at a stable path, with an unchanged designated requirement across the update switch, … Developer ID signing and notarization will join Authenticode and GPG in §3."
