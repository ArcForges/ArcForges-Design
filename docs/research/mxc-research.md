# Microsoft MXC feasibility research

Research date: **2026-11-14 UTC**. Scope: official stable Microsoft eXecution Container (MXC), source inspection, package metadata, and an implementation decision for ArcForges V2. This report does not record a Windows or Linux runtime pass. The designated native verification hosts were unavailable to this research session.

The implementable design is **stable official MXC plus ArcForges resource management and a durable RunSupervisor**. Linux uses the public .NET SDK. Windows uses the unchanged official executor as a narrowly scoped adjunct because the stable .NET public API cannot provide ProcessContainer terminal inheritance or author the required fallback prohibition. No MXC source copy, private fork, experimental backend, or Node.js runtime is adopted. These paths are source supported; their complete terminal, filesystem, network, resources, and recovery combination remains **UNPROVEN** until P1. See [integration](../architecture/02-mxc-integration.md) and [experiments](../verification/mxc-experiments.md).

## 1. Version and evidence boundary

**V-MXC-01.** The latest official stable release observed through GitHub releases and the NuGet registry is **1.0.1**, published **2026-10-17T00:55:03Z**, tag `v1.0.1`, commit `fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2`. Its stable policy schema is **1.0.0**, independently versioned from the package. `Microsoft.Mxc.Sdk` targets `net8.0`; versioned public types are in `Microsoft.Mxc.Sdk.V1`. The Node and Rust packages are also official distribution surfaces, but are not interchangeable with .NET API capabilities. [MXCS-01][s01] [MXCS-02][s02] [MXCS-26][s26]

The [machine-readable pins](mxc-sources.json) record stable commit, file blob IDs and SHA-256 values, release metadata, package locations, and the separate unreleased snapshot. Source inspection used the exact tag, not a floating `main`. Published npm 1.0.1 text was also inspected to resolve a documentation discrepancy about ProcessContainer PTY; no npm installation or native binary execution was performed. A downloaded text file is source evidence, not a native compatibility test. Release-asset and npm digests are attributed to upstream metadata unless expressly marked locally verified.

| Evidence category | Meaning in this report |
|---|---|
| Stable public API | Callable surface published in 1.0.1, with its actual backend restrictions. |
| Stable implementation | Behavior visible at the release commit; it can explain a decision but does not create a new public extension API. |
| Published official adjunct | Unchanged Microsoft executor distributed with the stable release and documented for JSON execution. |
| Unreleased | Implemented on the separately pinned `main` snapshot, absent from the selected stable .NET package. |
| Experimental / out of scope | Not an acceptable substitute for the required Windows ProcessContainer and Linux Bubblewrap profiles. |
| UNPROVEN | A composed ArcForges behavior requiring designated native host evidence. |

**V-MXC-02.** Stable `.NET MxcContainer.SpawnWithPty` covers IsolationSession, Bubblewrap, LXC, and Seatbelt direct execution; it does **not** cover Windows ProcessContainer. The public API has neither a ProcessContainer `STARTUPINFOEX`/`HPCON` argument nor an inherited-console launch option, pre-resume callback, or Job handle injection. Stable `ContainerRequest` also lacks `fallback.allowDaclMutation`; its internal exact writer does not emit that field. Adding an invented C# property or reflecting into internal/generated types is not a supported solution. [MXCS-02][s02] [MXCS-03][s03] [MXCS-04][s04]

The official stable Node adapter launches `wxc-exec.exe` through `node-pty` with ConPTY enabled. This adapter is present both at the release commit and in the published npm 1.0.1 payload. Therefore the executor-plus-host-terminal pattern is not speculative. ArcForges adopts the unchanged executor and implements its host terminal ownership in C# Native AOT; it does not copy that adapter or introduce Node.js. Microsoft Learn documents the executor as a supported consumer of JSON requests and says to use tools from the same release as the SDK. [MXCS-09][s09] [MXCS-10][s10] [MXCS-25][s25] [MXCS-27][s27]

The separately inspected `main` commit `6a89e69c72104bdf83b1f682a2f576b529b8bd65` adds `.NET SpawnWithExtendedOptions` and `SpawnStdio.Inherit` for ProcessContainer, Bubblewrap, and Seatbelt, and a development exact-JSON surface. These are **not selected stable APIs**. A future stable release may allow removing the executor adjunct after the same gates are rerun; it is not a prerequisite that can be silently assumed in the current Plan. [MXCS-21][s21]

## 2. Requirement-to-decision matrix

The evidence column names [platform verification IDs](../verification/platform-capabilities.md) and pinned source IDs. Decisions are design obligations; they are not claims that ArcForges already implements them.

| Requirement | MXC backend | Official API / mechanism | Evidence | Gap | Decision |
|---|---|---|---|---|---|
| Ordinary command with live streams | Windows ProcessContainer; Linux Bubblewrap | `.NET Spawn/SpawnAsync`; Windows official executor with inherited pipes | V-MXC-02; MXCS-02, 09 | Typed .NET Windows request cannot forbid DACL fallback | Use the Windows executor profile for its exact policy; Linux typed V1. |
| True TTY, raw-mode TUI, resize | ProcessContainer; Bubblewrap | Windows executor inside host ConPTY; Linux `SpawnWithPty`, `MxcPtyProcess.Resize` | V-MXC-02; MXCS-04, 10, 24 | Stable .NET cannot attach ProcessContainer to supplied ConPTY; full composition untested | `windows-process-executor-v1` and `linux-bubblewrap-sdk-v1`; A-MXC-01/02. |
| Ctrl+C and terminal input | Same | Terminal input bytes; native console/terminal processing | V-MXC-06; MXCS-04, 24 | No generic public SDK signal API; application raw mode changes ETX behavior | Negotiate terminal interrupt; test real foreground/child behavior; bounded Stop escalation. |
| Attach/detach and long-running service | Same, one-shot launch | Keep process/PTY owner alive independently of client | V-MXC-06; MXCS-04, 06, 14 | SDK disposal kills; root exit ends the one-shot and remaining descendants | Detach only a client; service keeps foreground root; no daemon adoption. |
| Run exit and descendant cleanup | Same | Native wait/kill/dispose, plus outer resource-scope readback | V-MXC-06; MXCS-04, 05, 06, 09 | Executor code is not independently typed payload state; internal drain warning can continue | Preserve exit provenance/uncertainty; no terminal completion or deletion before trusted cleanup proof. |
| Windows pre-execution resource limit | ProcessContainer BaseContainer tier | ArcForges parent Job before broker/executor execution; MXC internal Job before payload resume | V-MXC-03; MXCS-05, 06, 22, 23 | SDK exposes no owned Job or pre-resume insertion point | Inherit the preinstalled outer boundary; never attach by returned PID as enforcement. |
| Windows nested Job compatibility | ProcessContainer | Native PSEC plus MXC kill-on-close Job | V-MXC-03; MXCS-05–08, 22 | AppContainer tier adds Job UI limits, conflicting with normal nested Job conditions | Require native BaseContainer and native denied paths; reject downgrade. P1 proves actual Job chain. |
| Linux pre-execution resources | Bubblewrap | Worker already inside delegated cgroup v2 / systemd unit before SDK call | V-MXC-04; MXCS-13, 14 | No generic cgroup resource API in MXC | Retain ArcForges CPU/memory/pids control, budgets, readback and controller observation. |
| Host reserve and multi-sandbox pressure response | Both | ArcForges resource manager, OS controls | V-MXC-03/04; MXCS-03, 11 | MXC is not a host-wide budget allocator | Rework valuable existing algorithms; replace conflicting process-launch/security code only after proof. |
| Authorized filesystem reads/writes | Both | `FilesystemPolicy` path lists; exact Windows stable JSON | V-MXC-05; MXCS-03, 11–14 | Baselines differ; path grants are not private-volume remapping | Enumerate owned writable subdirectories and explicit host grants; test links and denied paths. |
| Persistent configuration/cache/temp/data | Both | Owned host directories plus explicit environment and grants | V-MXC-05; MXCS-03, 12–14 | No arbitrary transparent write redirection | State the cooperative redirection guarantee and reject unauthorized writes; avoid host-home/temp grant helpers by default. |
| Default-deny / selected egress | Both | Directional network policy; Windows PSEC WFP, Linux private namespace plus firewall tools | V-MXC-04/05; MXCS-11, 13, 15 | Host-specific network capabilities; Linux dependency/IPv6 restrictions | Explicit profile capability checks and per-request validation; no host-network fallback. |
| Host/public inbound service access | ProcessContainer host capability; Bubblewrap | Windows ingress/loopback policy where native contract supports it | V-MXC-04; MXCS-13, 15, 28 | Bubblewrap rejects ingress allow and has no published port mapping | Expose supported platform differences; unsupported Linux ingress is `UnsupportedCombination`, not silently allowed. |
| Persistent Sandbox vs container lifecycle | Both chosen one-shot backends | ArcForges persistent data/config; new MXC execution per Run | V-MXC-06; MXCS-02, 18 | `.NET MxcLifecycle` is not a generic ProcessContainer/Bubblewrap manager | Do not map Sandbox CRUD onto unsupported `MxcLifecycle` calls. |
| Pause/resume | Both | No stable public generic pause API | V-MXC-06; MXCS-02, 04 | Suspending a PID does not define process-tree, PTY, watchdog, and network semantics | Capability is unsupported; pressure management uses proven limit changes or Stop. |
| Native AOT and distribution | Both | Official .NET package, native assets; Windows official executor | V-MXC-07; MXCS-19, 20, 25, 26 | Upstream AOT smoke only exercises JSON; package alone does not prove native load | Pin coherent versions; real per-RID publish/load/run, signature and hash verification under F-AOT-01. |

## 3. Windows integration facts and remaining risks

### ProcessContainer tier and resources

**V-MXC-03.** ProcessContainer is an MXC backend with several implementation tiers. Native BaseContainer/PSEC and AppContainer fallback are not equivalent capability sets. In the selected stable source, BaseContainer creates the child suspended, installs its internal Job, and only then resumes it. Job creation or assignment failure terminates the child and fails launch. The Job has `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. BaseContainer enforces UI restrictions through PSEC and does not add `JobObjectBasicUIRestrictions` to that Job; AppContainer fallback does. Microsoft's nested Job contract requires a valid parent/subset hierarchy without Job UI restrictions. [MXCS-05][s05] [MXCS-06][s06] [MXCS-07][s07] [MXCS-22][s22]

The source supports a candidate composition: an independently supervised per-Run worker is assigned to ArcForges's outer resource Job before it can execute; the executor and then the contained process inherit that boundary; MXC assigns its own inner isolation Job while the payload remains suspended. ArcForges parent Jobs must not enable UI limits or breakaway. Whether native PSEC, the actual installed Windows build, and the inherited Job hierarchy work together is **A-MXC-01**, not resolved by reading either codebase separately. Assignment of the returned PID after `Spawn` is insufficient: code and descendants may already have run, and the Windows API says memory consumed before assignment is not examined against the Job memory limit. [MXCS-06][s06] [MXCS-23][s23]

The selected Windows profile requires a nonempty `filesystem.deniedPaths` entry for the existing private Run control directory and `fallback.allowDaclMutation: false`. The stable detector requires DACL consent for Tier 3 always and for Tier 2 whenever denied paths exist. Consequently, **as a source-derived inference**, this exact request will fail before payload execution if native BaseContainer with denied-path support cannot service it, instead of silently entering an AppContainer tier. P1 must test this inference with the official binary. A prior `--probe` alone is advisory and does not prevent a changed-host race. `MXC_FORCE_TIER` is a test-build facility, not a production selector. Do not turn off UI protection, enable DACL fallback, or run host preparation to make a resource test pass. [MXCS-08][s08]

The stable native BaseContainer path also rejects `processContainer.leastPrivilege=true`, an LPAC-token option. Its name does not make it a compatible generic hardening flag. The selected profile uses explicit native PSEC policy and refuses a request requiring LPAC instead of quietly selecting AppContainer. [MXCS-06][s06]

### Terminal and exact request transport

**V-MXC-02.** `wxc-exec.exe --config <path>` is a stable official entrypoint. Its ProcessContainer inherited-console path is designed to run below ConPTY and preserve the console relationship for the child. ArcForges must own ConPTY creation, concurrent input/output pumping, resize, terminal lifetime, executor process supervision, and the already-established outer resource Job. This is host integration around MXC; MXC continues to own the security environment and contained process creation. The stable public .NET SDK cannot instead be handed an `HPCON`, custom `STARTUPINFOEX`, or caller startup attributes. [MXCS-06][s06] [MXCS-09][s09] [MXCS-10][s10] [MXCS-24][s24]

The official Node adapter sends base64 JSON on the command line. ArcForges deliberately uses the also-supported private-file transport because its request can contain paths and environment values that should not appear in process command lines. The file is under a restrictive per-Run control directory, outside every workload grant, created atomically without following reparse points, immutable for that launch, bounded in size, and removed after execution/cleanup according to the journal. A global temporary directory and raw JSON on stdin are not adopted: stdin is reserved for the application, and no raw-stdin configuration contract was established. Detailed serialization and ownership requirements are in the integration chapter. [MXCS-09][s09] [MXCS-10][s10]

### System version and alternatives

**V-MXC-07.** The release-pinned OS table lists Process Isolation starting at Windows 11 24H2 `26100.9278`, 25H2 `26200.9278`, 26H2 `26300.9550`, and 26H1 `28000.2804`. These are MXC's published base support points, not a promise that each satisfies ArcForges's native-deny, network, ConPTY and nested-resource profile. Discovery of the exact request and the qualified host matrix control admission. Do not extrapolate Windows 10 or Windows Server support from ordinary Job Object availability. [MXCS-16][s16] [MXCS-28][s28]

IsolationSession does not repair the ProcessContainer .NET PTY gap while preserving this product's policy. Its one-shot policy rejects filesystem grants and denies, requires explicit all-allow egress/ingress/host loopback, and rejects supplied UI policy. It uses an isolated user/session with different data semantics. Windows Sandbox and Windows MicroVM/Hyperlight are marked experimental in the release overview. WSLc is another backend with its own network, lifecycle, image, and resource model; its `CpuCount`/`MemoryMb` fields are not ProcessContainer resource limits. None is an automatic fallback for the two chosen profiles. [MXCS-03][s03] [MXCS-17][s17] [MXCS-20][s20]

## 4. Linux policy and resource ownership

**V-MXC-04.** Bubblewrap is the stable default Linux backend. The documented MXC floor is user namespaces (kernel 3.8+), enabled unprivileged user namespaces, and `bwrap >= 0.5.0`. ArcForges additionally requires the cgroup v2 controllers, systemd/delegation and ownership checks defined by its resource chapter; the older MXC kernel floor is not an ArcForges platform certification. `MxcPlatform.GetPlatformSupport` and `GetAvailableBackends` are advisory discovery; native execution validates again. Distribution-specific namespace/security policy can prevent launch. [MXCS-13][s13] [MXCS-28][s28]

An ArcForges RunSupervisor must already be in its assigned resource cgroup before calling `.NET Spawn` or `SpawnWithPty`. MXC then owns Bubblewrap and its security/terminal tree. MXC's process-group kill is not CPU/memory enforcement, and a post-launch move is not the required before-execution guarantee. Account for the supervisor, namespace, and network-helper overhead explicitly, without double-counting cgroup ancestor totals. No generic CPU/memory/process-count limit or resource readback contract exists in the selected typed SDK/schema. [MXCS-03][s03] [MXCS-11][s11] [MXCS-14][s14]

Default-deny networking needs a private network namespace. Network-enabled modes additionally require `slirp4netns`, `ip`, `unshare` with `--map-current-user` and `--keep-caps`, `nsenter`, `iptables`, `ip6tables`, both restore utilities, a POSIX shell, and available connection tracking. The documented usual firewall backend is nftables; legacy locking can make unprivileged setup fail. MXC refuses missing prerequisites rather than sharing the host namespace. Stable Bubblewrap rejects `ingress.default: allow` and `ingress.hostLoopback: allow`; it supplies no stable port forwarding contract. Its slirp invocation does not enable IPv6, so an IPv6 allow rule does not create IPv6 connectivity. Services can run for a long time inside the sandbox without being reachable from the host or Internet. [MXCS-13][s13] [MXCS-14][s14]

Network restrictions are endpoint/protocol/port policy, not a complete domain-name allowlist service. The runtime proxy is a separate explicit mode; it is not freely composable with direct egress rules. Windows native networking likewise has private-network and ingress/loopback coupling and build-specific capabilities. ArcForges negotiates the complete requested policy and returns a bounded unsupported reason instead of translating it into broader access. [MXCS-11][s11] [MXCS-12][s12] [MXCS-15][s15]

## 5. Filesystem and data guarantees

**V-MXC-05.** Stable public path lists authorize access. They do not declare arbitrary source-to-destination mounts or redirect every application write. Bubblewrap emits same-path read-only/read-write binds; its baseline exposes system executables/libraries, `/etc`, and resolver support read-only while the user's home, `/root`, `/opt`, `/var`, and the user's runtime directory are absent unless granted. Private `/tmp` is default; an explicit writable host `/tmp` grant can replace that protection. Directory denies are masked with tmpfs and file denies with `/dev/null`. These Linux views must not be presented as identical to Windows PSEC path authorization. [MXCS-03][s03] [MXCS-13][s13] [MXCS-14][s14]

ArcForges gives each Sandbox explicit owned `home`, `config`, `cache`, `tmp`, `work`, and `data` locations and grants only the required subdirectories. Set `HOME`, `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, the applicable `XDG_*` variables, `TMP`/`TEMP`, and working directory to their actual exposed paths. The required Windows system environment is deliberately assembled and validated; ambient service/cloud credentials are never inherited. Bubblewrap's default HOME may be its configured working directory, so an explicit separate HOME is necessary to avoid treating untrusted workspace dotfiles as trusted user configuration. [MXCS-03][s03] [MXCS-13][s13]

This collects writes from applications honoring those settings. Hardcoded writes to other unauthorized paths are denied or inaccessible, not rerouted. Known-folder APIs, registry-based configuration, named IPC, credential stores, symlinks/reparse points, and build daemons need targeted compatibility tests. An authorized writable host directory is external data, not owned Sandbox data; deletion must never traverse into it. SDK convenience helpers that discover the user profile or host temp are not the ArcForges default policy. Source-backed isolation scope and the product's deletion ownership rules are separate obligations. [MXCS-02][s02] [MXCS-12][s12]

## 6. Process, terminal, and resource handles

**V-MXC-06.** `MxcProcess` owns the native execution handle. `Kill()` terminates the tree; `Dispose()` kills a still-running tree and releases handles. `WaitAsync` cancellation abandons the wait; it does not stop the native execution. `RunAsync` cancellation also does not terminate execution. `TryGetExitCode` observes root exit only; call `Wait/WaitAsync` for backend finalization. The SDK's spawn deadline is actively enforced by its wait path, so the durable supervisor must keep a non-client-cancelled wait/deadline owner alive. [MXCS-04][s04]

For PTY, `Input` is writable and `Output` is merged stdout/stderr; valid size is 1–32767 rows/columns. Closing input requests canonical EOF, which does not guarantee exit from raw mode. Output must be drained concurrently. Streams taken by the caller become its drain responsibility; disconnecting the remote or local client must not stop draining or dispose the native handle. A bounded replay/log buffer with explicit gap reporting is an ArcForges concern, not an MXC attach API. There is no generic public pause/resume or arbitrary signal operation. [MXCS-04][s04]

ProcessContainer's native wait terminates remaining descendants after the root exits, before releasing proxy/security state. Its internal Job waits up to five seconds for emptiness; that drain failure is logged and can continue. Thus neither root exit nor successful executor exit proves the ArcForges Run's whole workload boundary is empty. Finalization requires independent trusted resource-boundary readback; a cleanup failure retains ownership and prevents deletion. A background child does not acquire an independent long-lived Run when its foreground root exits. [MXCS-05][s05] [MXCS-06][s06]

The Windows executor can emit diagnostic text and a JSON backend-error envelope on stderr. Under ConPTY, these bytes share the workload stream and can be spoofed by the workload. Never interpret them as trusted state. Record `exit_source=official_executor`, raw observed code, `payload_started=unknown` unless independently confirmed, supervisor stop/deadline intent, and effect certainty. An application exit code and executor launch failure can overlap. `RUNNING` means active supervised execution, not proof that user code reached its entrypoint. The Linux SDK's structured errors offer stronger separation, but exceptions and wait outcomes still do not replace independent cleanup evidence. [MXCS-09][s09] [MXCS-04][s04]

The stable SDK does not reopen or transfer a live native process/PTY handle after owner death. Node restart therefore reconnects to the same surviving, authenticated RunSupervisor using Run, host-boot, owner-generation and process-start identity. A PID alone is insufficient and can be reused. Supervisor failure is a fail-closed cleanup event, not a reason to adopt unknown processes. Persistent Sandbox files remain; persistent native MXC containers are not promised. MXC's separate `MxcLifecycle` surface applies to its supported lifecycle backends, not to general ProcessContainer/Bubblewrap Sandbox CRUD. [MXCS-02][s02] [MXCS-04][s04] [MXCS-18][s18]

## 7. Distribution, AOT, privacy, and cost

**V-MXC-07.** The project declares `IsAotCompatible=true` and uses source-generated JSON. The upstream AOT smoke program explicitly never calls native code. It therefore does not prove that an ArcForges Native AOT bundle loads `mxc_ffi`, stages all sidecars, launches the selected backend, or owns a terminal correctly. The NuGet packaging manifest includes Windows x64/ARM64, Linux x64/ARM64, and macOS ARM64 native asset locations; only independently qualified ArcForges Windows/Linux RIDs are advertised. [MXCS-19][s19] [MXCS-26][s26]

Ship a coherent versioned unit from official artifacts: the exact NuGet/native assets and, on Windows, the same-release official executor and its required files. Resolve from a protected installation directory, not ambient PATH or user-controlled native-loader overrides. Verify package lock/hash, upstream artifact hash and Windows signature on the actual target. The observed GitHub ZIP digest is `sha256:0e832239454ba7fcd338ff56218a287eef4c0a01c1484084b869f55feff8abe9`; this session read that upstream metadata but did not download, hash or execute the 542,051,775-byte ZIP. Include Microsoft MIT license and applicable dependency notices/SBOM. Review the resulting distributable, rather than assuming the repository's license alone describes every bundled tool. [MXCS-19][s19] [MXCS-20][s20] [MXCS-25][s25]

`wxc-host-prep` is not routine launch plumbing. Its fallback preparation can alter host drive metadata ACLs and the null device; some preparation is boot dependent. ArcForges's default profile refuses DACL-mutating fallback and never automatically runs host prep. Stable 1.0.1 telemetry has a per-request opt-in gate combined with consent and policy. Default profile requests disable optional MXC telemetry; upgrade review must revisit the contract rather than relying on floating documentation. Offline operation and absence of policy-content leakage are part of the bundle experiment. [MXCS-29][s29] [MXCS-30][s30]

No startup latency, memory overhead, sustained throughput, or maximum concurrency was measured here. P1 records cold/warm latency, idle supervisor/native/helper memory, terminal throughput under backpressure, resource-control overhead, and cleanup latency on the actual profile. Helpers count against the declared budget model. Unmeasured overhead is a benchmark obligation, not a performance promise.

## 8. Decisions and acceptance

1. Adopt `windows-process-executor-v1` and `linux-bubblewrap-sdk-v1` as the only initial native execution profiles. Backend, profile revision, SDK/native version and host capabilities are persisted with each Run. A profile can be design adopted and still unavailable on an unqualified host.
2. Keep host budgets, reserve, pressure response, CPU/memory/pids enforcement and readback in ArcForges. MXC owns security-policy application and contained process creation. Remove duplicate launch/sandbox mechanisms only after their replacement's combination gate passes.
3. Perform **F-MXC-01 / A-MXC-01** under `AFV2-MXC-02`, **F-MXC-02 / A-MXC-02** under `AFV2-MXC-03`, and **F-AOT-01** under `AFV2-MXC-01`. `AFV2-MXC-04` owns the explicit proceed/block decision.
4. The same selected profile must prove real terminal behavior, required filesystem/network policy, pre-execution resources, descendant cleanup and owner recovery together. Separate demonstrations of each feature on different backends or weaker policies do not satisfy V2.
5. If a mandatory combination fails, record the exact stable capability/host blocker and the upstream issue or supported remedy. A labeled noninteractive development path can permit limited engineering progress, but cannot satisfy the full Windows/Linux CLI acceptance requirement. Never transform an impossible step into a task instructed to report success.

## Sources

Each `MXCS-*` entry and all component-file hashes are in [mxc-sources.json](mxc-sources.json). Links below are immutable for repository sources; Microsoft Learn and registry pages were observed on the research date.

[s01]: https://github.com/microsoft/mxc/releases/tag/v1.0.1
[s02]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/docs/api-reference/dotnet/v1/api.md
[s03]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/sdk/dotnet/Microsoft.Mxc.Sdk/V1/ContainerRequest.cs
[s04]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/sdk/dotnet/Microsoft.Mxc.Sdk/V1/MxcProcess.cs
[s05]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/src/mxc-sdk/src/backends/process_container/common/job_object.rs
[s06]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/src/mxc-sdk/src/backends/process_container/common/base_container_runner.rs
[s07]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/src/mxc-sdk/src/backends/process_container/common/appcontainer_runner.rs
[s08]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/src/mxc-sdk/src/backends/process_container/common/fallback_detector.rs
[s09]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/src/tools/wxc/src/main.rs
[s10]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/sdk/node/src/bindings/process-container-pty.ts
[s11]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/schemas/stable/mxc-config.schema.1.0.0.json
[s12]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/docs/containment-policy/1.0.0/policy.md
[s13]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/docs/backends/bwrap/bubblewrap-backend.md
[s14]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/src/mxc-sdk/src/backends/bubblewrap/common/bwrap_runner.rs
[s15]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/docs/backends/process-container/networking.md
[s16]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/docs/backends/process-container/os-version-support.md
[s17]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/docs/development/architecture/backends/isolation-session/oneshot.md
[s18]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/docs/container-lifecycle.md
[s19]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/sdk/dotnet/Microsoft.Mxc.Sdk/Microsoft.Mxc.Sdk.csproj
[s20]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/LICENSE.md
[s21]: https://github.com/microsoft/mxc/blob/6a89e69c72104bdf83b1f682a2f576b529b8bd65/docs/api-reference/dotnet/v1/api.md
[s22]: https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs
[s23]: https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject
[s24]: https://learn.microsoft.com/en-us/windows/console/creating-a-pseudoconsole-session
[s25]: https://learn.microsoft.com/en-us/windows/apps/develop/mxc/releases
[s26]: https://www.nuget.org/packages/Microsoft.Mxc.Sdk/1.0.1
[s27]: https://registry.npmjs.org/@microsoft%2fmxc-sdk/1.0.1
[s28]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/sdk/dotnet/Microsoft.Mxc.Sdk/V1/MxcPlatform.cs
[s29]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/src/mxc-sdk/src/core/mxc_common/telemetry/mod.rs
[s30]: https://github.com/microsoft/mxc/blob/fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2/docs/backends/process-container/host-prep.md
