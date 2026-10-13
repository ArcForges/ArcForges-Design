# AD-0002 — Platform scope: Windows and Linux/WSL now; macOS later

- Status: Accepted (2026-10-12; revised 2026-10-13 after the findings review: Windows 11 floor for TLS 1.3)

## Decision

| Component | In scope now | Notes |
|---|---|---|
| Node, CLI, MCP adapter | Windows 11 (x64, arm64); Linux glibc x64/arm64 with a systemd user manager (Debian 12/13, Ubuntu 22.04/24.04), including WSL2 distributions | Windows 11 is the floor (revised 2026-10-13). The LAN transport requires TLS 1.3, which Windows' Schannel supports only from Windows 11 and Windows Server 2022; Windows 10, including 22H2, does not (V-N06). Windows 10 also reached end of support on 2025-10-14; only paid Extended Security Updates continue. A LAN transport with a TLS 1.2 fallback for Windows 10 was considered and rejected: it would weaken the peer contract and double the test matrix for an out-of-support version. Windows 11 is newer than every other API floor the design uses (nested jobs, V-W01; DNS-SD, V-T04). The installer refuses older Windows versions with a clear message. Linux without a systemd user manager runs observe-only (AD-0005). |
| Desktop (Avalonia) | Windows x64/arm64; Linux x64/arm64 with X11 or Wayland | The tray icon is optional where the desktop environment lacks support (V-N04). |
| Android app | Android 8.0 (API 26) and newer, target API 36 | Matches the existing Mobile repository. |
| Web | Current evergreen Chromium, Firefox and Safari | Blazor WebAssembly |
| Cloud | Cloudflare Workers, Durable Objects, Containers, D1, R2, Queues | AD-0009 |

**macOS is outside the current implementation and acceptance scope.** No macOS code, CI, packaging or claim is produced. To keep a future extension possible, the node accesses every OS mechanism through these platform interfaces, each with Windows and Linux implementations only:
- `IProcessLauncher`
- `IExecutionContainer` (job object or cgroup)
- `IResourceSampler`
- `ISecretStore`
- `IServiceRegistration` (autostart)
- `IServiceDiscovery` (DNS-SD)
- `IPeerCredentialCheck`
- `IFileSystemInfo`

## Validation venues

- **Windows:** the developer workstation (L-01). Real process-control tests run there.
- **Linux:** the local WSL2 Debian 13 distribution (L-02 to L-09). Tests that execute real Linux processes and cgroup controls there are **real tests of WSL2**. They are recorded as evidence for WSL2 on that kernel and systemd version, not as proof for every Linux distribution or kernel.
- **arm64:** binaries are produced by cross-compilation. Execution on real arm64 hardware is deferred validation, listed in the acceptance register.
- **Bare-metal Linux:** systemd lingering for headless operation (`loginctl enable-linger`) is a documented user step, validated when such a machine is available (acceptance register).
