# AD-0002 — Platform scope: Windows and Linux/WSL now; macOS later

- Status: Accepted (2026-10-12)

## Decision

| Component | In scope now | Notes |
|---|---|---|
| Node, CLI, MCP adapter | Windows 10 22H2 and Windows 11 (x64, arm64); Linux glibc x64/arm64 with a systemd user manager (Debian 12/13, Ubuntu 22.04/24.04), including WSL2 distributions | Windows 10 22H2, the last Windows 10 release, is the floor. It is newer than every API floor the design uses: nested jobs since Windows 8 (V-W01), and DNS-SD (`DnsServiceRegister`/`DnsServiceBrowse`, documented for Windows 10 without a precise build, V-T04). The workstation verifies Windows 11 (F-T03); Windows 10 22H2 is an acceptance-register item. Linux without a systemd user manager runs observe-only (AD-0005). |
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
