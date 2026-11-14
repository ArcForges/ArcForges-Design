# AD-0002 — Platform scope: Windows and Linux now; macOS later

- Status: Accepted (2026-10-12; revised 2026-10-13 after the findings review: Windows 11 floor for TLS 1.3; revised 2026-10-13 by the product owner's decisions (AD-0015): Windows 11 floor confirmed; no Windows 10 support; amended 2026-10-19 by AD-0017: macOS becomes an accepted future execution target by the product owner's decision of 2026-10-18, outside the current implementation and acceptance scope until roadmap RM-15 is promoted; the platform-interface list revised, for the execution mechanisms, to the delivered execution-platform seam; research venues added; relabelled 2026-10-19 by AD-0017 as amended: the Apple-silicon-only proposal and the LaunchAgent design are candidates for macOS development, not current decisions; amended 2026-10-21 by AD-0018: Linux is native Linux, and a user may run the Linux node in a compatible WSL2 distribution without integration; the Linux validation venue is a native Linux machine; title changed from "Windows and Linux/WSL now"; amended 2026-10-28 by [AD-0021](AD-0021-central-access-go-center.md): the center's store is Neon/PostgreSQL, not D1; platform scope otherwise unchanged (Windows 11, native Linux, x64 and arm64, Android 8.0+, evergreen browsers; no Windows 10 or macOS))

## Decision

| Component | In scope now | Notes |
|---|---|---|
| Node, CLI, MCP adapter | Windows 11 (x64, arm64); Linux glibc x64/arm64 with a systemd user manager (Debian 12/13, Ubuntu 22.04/24.04); a user may run the Linux node in a compatible WSL2 distribution, without integration ([AD-0018](AD-0018-native-platforms-without-wsl-integration.md); amended 2026-10-21, formerly "including WSL2 distributions") | Windows 11 is the floor (revised 2026-10-13). The LAN transport requires TLS 1.3, which Windows' Schannel supports only from Windows 11 and Windows Server 2022; Windows 10, including 22H2, does not (V-N06). Windows 10 also reached end of support on 2025-10-14; only paid Extended Security Updates continue. A LAN transport with a TLS 1.2 fallback for Windows 10 was considered and rejected: it would weaken the peer contract and double the test matrix for an out-of-support version. Supporting Windows 10 for local features only (no LAN) was also considered. Nothing in the node depends on LAN, so that remains possible later, but it is not offered at launch: it needs its own support and test matrix for an out-of-support version, and a "not available on this Windows version" state on every LAN surface. The product owner confirmed this on 2026-10-13: no effort goes into Windows 10 ([AD-0015](AD-0015-direction-editions-roadmap.md) §3). Windows 11 is newer than every other API floor the design uses (nested jobs, V-W01; DNS-SD, V-T04). The installer refuses older Windows versions with a clear message. Linux without a systemd user manager runs observe-only (AD-0005). |
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

*The list above is kept as history. It is superseded as a description of the code by the dated revision of 2026-10-19 below.* The scope sentence above still binds release 1 (see Direction, item 1).

**Dated revision (2026-10-19, recorded with the macOS amendment of [AD-0017](AD-0017-delegated-execution-direction.md); Direction, item 2).** The node does not implement the eight interfaces listed above. The delivered execution-platform seam is `IExecutionPlatform` with `IAttemptHandle` (`src/ArcForges.Node.Platform/ExecutionPlatform.cs` in ArcForges/ArcForges at `b22d2ec`), which keeps the execution mechanisms behind one interface, with Windows and Linux implementations. It is the successor of the list above for the execution mechanisms (process launch, the job object or cgroup, resource sampling). Of the other mechanisms, the secret store and peer identity are reached through DesktopPlatform's `ArcForges.Security.Secrets` and `ArcForges.LocalRpc` ([AD-0013](AD-0013-reuse-and-supersession.md) §4), and autostart and DNS-SD discovery are designed outside the seam ([13](../architecture/13-distribution-updates.md) §3, [09](../architecture/09-lan.md) §2). A macOS node would be the seam's third implementation, plus macOS backends for those other mechanisms. This revises the text to match the delivered code; it is not a correction of any claim, and no scope changes.

## Validation venues

- **Windows:** the developer workstation (L-01). Real process-control tests run there.
- **Linux** (amended 2026-10-21 by [AD-0018](AD-0018-native-platforms-without-wsl-integration.md) §5): a native Linux machine: the Claude Code Cloud Linux environment for the checks it can run, and a real Linux host with a systemd user manager and cgroups v2 delegation for real-OS tests. Local WSL Debian is not a development dependency. *Amended again 2026-10-21 by [AD-0019](AD-0019-mcp-first-verification.md): the Linux venue is the Linux MCP host, reached through the Linux MCP server; neither local WSL nor an agent's own sandbox (such as the Claude Code Cloud Linux environment) is a venue.* *Superseded 2026-10-21 by [AD-0018](AD-0018-native-platforms-without-wsl-integration.md) (kept as history):* the local WSL2 Debian 13 distribution (L-02 to L-09). Tests that execute real Linux processes and cgroup controls there are **real tests of WSL2**. They are recorded as evidence for WSL2 on that kernel and systemd version, not as proof for every Linux distribution or kernel.
- **arm64:** binaries are produced by cross-compilation. Execution on real arm64 hardware is deferred validation, listed in the acceptance register.
- **Bare-metal Linux:** systemd lingering for headless operation (`loginctl enable-linger`) is a documented user step, validated when such a machine is available (acceptance register).
- **Research venue** (amended 2026-10-19 by AD-0017; Direction, item 3): a disposable lab VM or wipeable lab hardware: research evidence for roadmap rows, for that build only; not a validation venue for release-1 tasks. Its lab entries are in the [research record](../research/2026-10-18-delegated-execution/lab-register.md).
- **Research distributions** (amended 2026-10-19 by AD-0017; Direction, item 4): Fedora and Ubuntu 26.04 are research venues, not supported targets. Whether Fedora becomes a supported target is an owner decision ([17](../architecture/17-delegated-execution.md) §17, decision 18).

## Direction (roadmap; not release 1)

Amended 2026-10-19 by [AD-0017](AD-0017-delegated-execution-direction.md). The decision table and the scope sentence above bind release 1 unchanged.

1. **macOS as an accepted future execution target.** On 2026-10-18 the product owner decided, in section 3 of the request for the long-term evolution study:

   > The execution targets are:
   > Windows, Linux, and macOS.
   > Android, iOS, and the Web are control clients, not local application sandbox or execution targets.
   > That distinction is final.

   macOS will therefore be an execution target for the node only, local-only in its first stage, as roadmap row RM-15 (the monitored local node). It stays outside the current implementation and acceptance scope until RM-15 is promoted: no macOS code, CI, packaging or claim is produced before then. This reverses, as direction, the scope position recorded above, which followed the product owner's decision of 2026-10-08 that macOS was not required for that delivery. This decision defines no macOS floor. Architecture coverage, hardware, the developer program, signing and notarization, the lab venue and the launch design are decided when macOS development starts, by the product owner's instruction of 2026-10-19: "Do not make Apple hardware purchasing, developer-program enrollment, specific lab setup, architecture coverage, or detailed implementation decisions now. Those belong to actual macOS development later." The node's macOS capability statements (monitored resources; the TCC rules) are in [17](../architecture/17-delegated-execution.md) §5.3 and §14.6, and in [18](../architecture/18-application-workload-control.md) §14.3. *Relabelled 2026-10-19; superseded:* "**Apple silicon only** is a study proposal for the owner to confirm, not an existing floor: this decision defines no macOS floor ([17] §17, decision 21). The node's macOS design (a signed, notarized LaunchAgent; monitored resources; the TCC rules) is in [17] §5.3 and §14.6."
   - **Effective:** now, as recorded direction that changes no release-1 scope; macOS execution takes effect when RM-15 is promoted.
2. **The dated revision above** replaces the interface list as a description of the code; the delivered execution-platform seam succeeds it for the execution mechanisms. **Effective:** now, as a dated revision, not a correction.
3. **The research venue** above. **Effective:** now.
4. **The research distributions** above. **Effective:** now.
