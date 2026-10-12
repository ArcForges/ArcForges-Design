# Platform capability verification register

Status: verified 2026-10-12 for the ArcForges flagship design (decision [AD-0001](../decisions/AD-0001-flagship-pivot.md)).

This register separates three kinds of statement. The design cites them by ID.

- **V (verified):** confirmed against current primary documentation or source, with the source linked.
- **L (local probe):** observed directly on the development workstation (Windows 11 build 26300 and WSL2 Debian 13). A probe proves behaviour only for that environment, not for every deployment.
- **A (assumption) and F (future validation):** an expectation the design relies on that is not yet proven. Each has an owner task in the delivery plan that must prove or refute it before dependent acceptance closes.

Mocked or simulated tests never upgrade an A/F item to V. Only a real run of the named mechanism does.

## 1. Development workstation (local probes, 2026-10-12)

| ID | Observation |
|---|---|
| L-01 | Windows 11 Pro for Workstations 10.0.26300; Intel Core Ultra 5 125H, 14 cores / 18 logical processors (hybrid P/E cores); 31.5 GB RAM. |
| L-02 | WSL 3.0.1.0, kernel `6.18.40.1-microsoft-standard-WSL2`, one distribution `Debian` (Debian GNU/Linux 13 trixie), WSL2. |
| L-03 | `%UserProfile%\.wslconfig`: `memory=16GB`, `swap=8GB`, `networkingMode=mirrored`, `dnsTunneling=true`, `firewall=true`, `autoProxy=true`, `[experimental] autoMemoryReclaim=dropCache`. Inside the guest, `nproc` = 18 and total memory = 15,993 MiB. |
| L-04 | `/etc/wsl.conf` has `[boot] systemd=true`; PID 1 is systemd 257 (257.13-1~deb13u1); `systemctl --user` reports `running`; `Linger=no` for uid 1000. |
| L-05 | cgroup v2 unified hierarchy (`cgroup2fs`). Root controllers: `cpuset cpu io memory hugetlb pids rdma`. Root `subtree_control`: `cpuset cpu io memory pids`. |
| L-06 | `user@1000.service` has `Delegate=yes`, `DelegateControllers=cpu memory pids`. The directory `/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service` and its `cgroup.procs` are owned by the user. `app.slice` exposes `cpu memory pids`. The `io` controller is **not** delegated to the user manager. |
| L-07 | `systemd-run --user --scope -p MemoryMax=64M -p CPUQuota=50% -p TasksMax=32` placed the process in `.../user@1000.service/app.slice/run-*.scope` with `memory.max=67108864`, `cpu.max=50000 100000` and `pids.max=32`. Unprivileged per-task CPU, memory and process-count enforcement works in this WSL2 environment. |
| L-08 | Processes started through `wsl.exe` run in `0::/non-systemd`, a root-owned cgroup outside the user manager. An unprivileged process started directly by `wsl.exe` cannot create controlled child cgroups there. |
| L-09 | The kernel exposes `cgroup.kill`, `cgroup.freeze`, `cgroup.events`, `memory.high`, `memory.peak`, `memory.events` and PSI files (`cpu.pressure`, `memory.pressure`, `io.pressure`). |
| L-10 | Windows tools: .NET SDK 10.0.401 (Program Files) and 10.0.400 (`%UserProfile%\.dotnet`), the android workload, Rust (rustup cargo/rustc), CMake, Ninja, sccache, Node LTS/npm, git, gh, Python, winget and Scoop. No `cl.exe` on PATH (a Visual Studio 18 instance exists), and no ccache or FASTBuild. `protoc` is available from the Grpc.Tools 2.84.0 NuGet cache. |
| L-11 | WSL tools: gcc, g++, clang, git, Docker CLI, npm and Python 3; .NET SDK 10.0.400 under `~/.dotnet` (not on PATH). No cargo, rustc, CMake, Ninja, sccache, ccache or Avahi. |
| L-12 | WSL2 mirrored networking: the guest sees the host's LAN address (192.168.1.99/24) directly. |
| L-13 | Transient user services (`systemd-run --user`, the CLI form of `StartTransientUnit`) in a user slice, on systemd 257: per-unit `CPUWeight=400`, `MemoryHigh=48M`, `MemoryMax=64M` and `TasksMax=64` appeared as `cpu.weight=400`, `memory.high=50331648`, `memory.max=67108864` and `pids.max=64`. A runtime `set-property` on the slice (`CPUQuota=200%`, `MemoryHigh=900M`, `MemoryMax=1G`, `TasksMax=2000`) appeared as `cpu.max=200000 100000`, with the memory and pids values matching. `ExecStopPost` received `EXIT_CODE=exited`, `EXIT_STATUS=3` and `SERVICE_RESULT=exit-code` for a process that exited with 3. Output went to the configured file. `freeze`/`thaw` toggled `cgroup.events frozen`, `set-property --runtime MemoryHigh` changed `memory.high` live, and `kill` ended the unit. With `--collect`, units were garbage-collected. The unit's main process was a child of the user manager (`systemd`), not of the caller. |

## 2. Windows process and resource control

| ID | Fact | Source |
|---|---|---|
| V-W01 | A job object groups processes. Children created with `CreateProcess` join the job by default, unless breakaway is allowed (`JOB_OBJECT_LIMIT_BREAKAWAY_OK` with `CREATE_BREAKAWAY_FROM_JOB`, or `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK`). Nested jobs are supported from Windows 8. Processes created through WMI `Win32_Process.Create` do **not** join the caller's job. | [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) |
| V-W02 | With `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, closing the last job handle terminates every associated process, including those in child jobs. `TerminateJobObject` terminates all processes in the job. | same |
| V-W03 | Completion-port notifications (new process, exit, limit events) are **not guaranteed**, except for limits set with `JobObjectNotificationLimitInformation`. Accounting (`JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION`) covers terminated processes and aggregates child jobs into parents. | same |
| V-W04 | CPU rate control (Windows 8+): a hard cap (`CpuRate` in 1/100 percent of the whole machine, or of the parent job's allocation when nested), weight-based (1–9, default 5), or min/max rates. Not usable under Remote Desktop Services when Dynamic Fair Share Scheduling is active. | [JOBOBJECT_CPU_RATE_CONTROL_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_cpu_rate_control_information) |
| V-W05 | Job and process memory limits limit **committed virtual memory**, not working set. An allocation beyond the limit fails, and the process is not killed. Peak committed usage is tracked. A notification-only limit is available through `JobObjectNotificationLimitInformation`. | [JOBOBJECT_EXTENDED_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information) |
| V-W06 | Process Governor (procgov) applies these limits through job objects: commit caps, working-set bounds (which need `SeIncreaseBasePriorityPrivilege`), affinity, CPU rate, clock and user-time limits, priority and efficiency mode. It can attach to existing PIDs. Its service mode (beta) runs as SYSTEM. Job limits cannot change after creation unless the job is named, and processes cannot move between its jobs. | [process-governor](https://github.com/lowleveldesign/process-governor) |
| A-W01 | Creating a job, setting CPU and commit limits on it, and assigning processes the same user created requires no administrator rights. The owner task must prove this with a real non-elevated run. | F-W01 |
| A-W02 | An agent's child tools that create their own jobs (for example a build server or a test host) still run correctly inside an ArcForges job, because Windows 8+ nests jobs. The owner task must prove this with real `dotnet build`, `cargo build` and `cmake --build` runs. | F-W02 |

**Design consequences.**
- Windows enforcement uses one job object per managed execution, with KILL_ON_JOB_CLOSE, CPU rate control and a commit limit, inside a per-service root job.
- Memory pressure on Windows is a commit cap plus a notification-driven soft threshold, decided by the scheduler. Windows has no equivalent of Linux `memory.high`, and the design never claims one.
- Processes created through WMI, services, COM servers and the WSL VM are outside any job. ArcForges reports them as unmanaged or "escaped", never as controlled.

## 3. Linux (WSL2) process and resource control

| ID | Fact | Source |
|---|---|---|
| V-L01 | Delegation gives a non-root user write access to a cgroup directory's `cgroup.procs`, `cgroup.threads` and `cgroup.subtree_control`. Resource-control files of the delegated directory stay unwritable to the delegatee. Migrating a process needs write access to `cgroup.procs` of the source, the destination and their common ancestor. | [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) |
| V-L02 | No internal processes: controllers can only be enabled in `cgroup.subtree_control` of a cgroup that has no processes of its own (the root is exempt). | same |
| V-L03 | `memory.high` throttles and reclaims and never invokes the OOM killer. `memory.max` is hard, and OOM kills inside the cgroup when it cannot reclaim. `memory.events` counts high, max, oom and oom_kill. `memory.oom.group` kills the whole group together. `memory.peak` records the peak. | same |
| V-L04 | `cpu.max` (`$MAX $PERIOD`, default `max 100000`) is a bandwidth cap. `cpu.weight` (1–10000, default 100) is proportional. `pids.max` makes fork fail with EAGAIN at the limit. | same |
| V-L05 | Writing `1` to `cgroup.kill` SIGKILLs the whole subtree, even with concurrent forks. `cgroup.freeze` stops all processes, which can still be killed. `cgroup.events` reports `populated` and `frozen` with file-modified notifications (inotify or poll). | same |
| V-L06 | `io.max` limits bytes/s and IOPS per device. `io.weight` needs iocost or BFQ. | same |
| V-L07 | WSL `.wslconfig`: `memory` (default 50% of host memory) and `processors` (default all logical processors) size the VM. `vmIdleTimeout` defaults to 60 s, and `[general] instanceIdleTimeout` defaults to 15 s (-1 disables automatic distro shutdown). `networkingMode` is `nat` (default), `mirrored`, `consomme` or `none`. `localhostForwarding` applies only in NAT mode. `isolateDistroCgroup` (default true) gives each distribution its own cgroup. `wsl.conf [automount] cgroups` defaults to v2, and `[boot] systemd=true` enables systemd. | [WSL configuration](https://learn.microsoft.com/en-us/windows/wsl/wsl-config) |
| L-07 | Unprivileged CPU, memory and pids enforcement through the systemd user manager works on the workstation (section 1). | local |
| L-08 | Processes started directly by `wsl.exe` cannot be controlled by an unprivileged guest component (section 1). | local |
| A-L01 | The WSL VM appears on Windows as a separate VM worker process (vmmem/vmmemWSL), which aggregates all guest memory, including page cache until reclaim. The owner task must observe the process name and its accounting on the workstation and record it. Note: no vmmem process was observed while the distribution was stopped. | F-L01 |
| A-L02 | `io` control requires a root-owned guest component (a system unit with `Delegate=io` or direct cgroup writes). The design treats I/O limits as optional and only available after an explicit privileged install. | F-L02 |
| A-L03 | The node, as a Native AOT C# client of the user manager's D-Bus API (`Tmds.DBus.Protocol`), can create the same transient services with file descriptors passed for stdio (`Standard*FileDescriptor`), an exact environment (`Environment` plus `UnsetEnvironment`) and `ExecStopPost`. Such executions keep running and keep their durable exit record across a node crash, a `systemctl --user restart` of the node unit and an update switch. L-13 proves the mechanism through `systemd-run`, not yet from the node. | F-L03 |

**Design consequences.**
- **Guest node.** The Linux node runs as a systemd **user** unit (`arcforges-node.service`) in the delegated subtree. Each managed execution gets its own child cgroup with `cpu.max` or `cpu.weight`, `memory.high`/`memory.max`, `pids.max` and `memory.oom.group=1`. The node kills a tree with `cgroup.kill`, pauses it with `cgroup.freeze`, and detects completion through `cgroup.events`.
- **Keeping WSL alive.** Because `wsl.exe`-started processes land outside the user manager, the Windows host reaches the guest through a long-lived `wsl.exe` bridge process. The bridge only relays a byte stream to the guest node's Unix socket. It also keeps the distribution alive while the host has work for it, so ArcForges never depends on changing the user's `instanceIdleTimeout`.
- **Requirements without systemd.** When systemd or user delegation is absent, the guest node reports `enforcement=observe-only` for CPU and memory and refuses executions whose policy requires enforcement. It never silently runs them unenforced.

## 4. Local IPC, gRPC and runtimes

| ID | Fact | Source |
|---|---|---|
| V-N01 | ASP.NET Core lists gRPC as fully supported under Native AOT, along with WebSockets, rate limiting, health checks and JWT authentication. `CreateSlimBuilder` omits HTTPS and HTTP/3 unless enabled explicitly. | [ASP.NET Core Native AOT](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot?view=aspnetcore-10.0) |
| V-N02 | DesktopPlatform `ArcForges.LocalRpc` (main `60309ec9`) already hosts generated gRPC over HTTP/2 on Kestrel through a custom listener restricted to a Windows named pipe or Unix domain socket. It is `IsAotCompatible`, with admission lanes, deadlines and peer-connection authorization. Its AOT behaviour has local evidence (PRF.04, DesktopPlatform #177). | repository source and ledger |
| V-N03 | gRPC-Web supports unary and server-streaming calls from browsers. Client and bidirectional streaming are unsupported. Browser server streaming requires `GrpcWebMode.GrpcWebText`. | [gRPC-Web in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/grpc/grpcweb?view=aspnetcore-10.0) |
| V-N04 | Avalonia supports Native AOT when compiled bindings are used and reflection bindings avoided. TrayIcon works on Windows and on some Linux desktops only, and needs a native menu. | [Avalonia Native AOT](https://docs.avaloniaui.net/docs/deployment/native-aot), [TrayIcon](https://v11.docs.avaloniaui.net/docs/reference/controls/tray-icon/) |
| A-N01 | The official C# MCP SDK (`ModelContextProtocol.Core` 2.2.0, with an `Extensions.Tasks` package) publishes under Native AOT without warnings and speaks protocol revisions 2025-11-25 and 2026-07-28. Not stated in its README. If either fails, the adapter implements the needed stdio JSON-RPC subset in C# with source-generated JSON. | F-N01 |
| A-N02 | `System.CommandLine` 2.x publishes under Native AOT without trim warnings and meets the CLI cold-start target. If not, the CLI uses a small in-house parser for the specified grammar. | F-N02 |
| A-N03 | Windows supervisor and console behaviour: a GUI-subsystem Native AOT executable (`arcforges-supervisor.exe`) starts at logon from the `HKCU` Run key with no visible window, and launches the console-subsystem node with `CREATE_NO_WINDOW` so that it receives a hidden console usable for `CTRL_BREAK_EVENT` delivery to child process groups. | F-N03 |

## 5. AI client integration

| ID | Fact | Source |
|---|---|---|
| V-A01 | MCP revision **2026-07-28** removes the initialize handshake and protocol sessions. Every request carries its protocol version and client capabilities in `_meta`, and servers MUST implement `server/discover`. Long-running work moved to the official extension `io.modelcontextprotocol/tasks` (polling with `tasks/get`, input with `tasks/update`). Progress notifications travel on the related request's response stream, Streamable HTTP lost resumability (a broken stream loses the request), and Roots, Sampling and Logging are deprecated. Servers needing cross-call state use explicit server-minted handles passed as tool arguments. | [MCP changelog](https://modelcontextprotocol.io/specification/latest/changelog) |
| V-A02 | Claude Code hooks include SessionStart, SessionEnd, PreToolUse, PostToolUse, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, WorktreeCreate, WorktreeRemove, Stop and others. Common input carries `session_id`, `transcript_path` and `cwd`, and subagent events add `agent_id` and `agent_type`. A PreToolUse hook can return `permissionDecision` (`allow`, `deny`, `ask`, `defer`) and `updatedInput`, which rewrites the tool arguments. `CLAUDE_ENV_FILE` persists environment variables for later Bash commands. Plugins ship `hooks/hooks.json`. Managed settings can set `allowManagedHooksOnly`, which disables user, project and plugin hooks. Default command-hook timeout: 600 s. | [Claude Code hooks](https://code.claude.com/docs/en/hooks) |
| V-A03 | Claude Code's Bash sandbox runs on Linux, WSL2 and macOS; native Windows commands run unsandboxed. MCP servers and hooks run **outside** the sandbox. Unix-socket access inside the sandbox is governed by `sandbox.network.allowUnixSockets`. `excludedCommands` run outside the sandbox, and admin-required sandboxes ignore repository loosening. | [Claude Code sandboxing](https://code.claude.com/docs/en/sandboxing) |
| V-A04 | Codex hooks are SessionStart, SessionEnd, PreToolUse, PermissionRequest, PostToolUse, PreCompact, PostCompact, UserPromptSubmit, SubagentStart, SubagentStop, Stop and Interrupt. PreToolUse covers shell (`Bash`, `exec_command`), `apply_patch` and MCP tools, and supports `permissionDecision: "deny"` and `"allow"` with `updatedInput`, but not `"ask"`. Hooks are **fail-open** ("a useful guardrail, not a complete enforcement boundary"). Non-managed hooks must be trusted through `/hooks`. Subagent events carry `agent_id` and `agent_type` with the parent `session_id`. MCP servers are configured in `config.toml` (`[mcp_servers.<name>]`), and project config loads only for trusted projects. | [Codex hooks](https://learn.chatgpt.com/docs/hooks) |
| V-A05 | Codex's Linux sandbox (bubblewrap/Landlock with a seccomp network filter) has been reported across versions to deny AF_UNIX `connect`/`bind` unless `sandbox_workspace_write.network_access = true`. Behaviour differs by version. | [codex#10797](https://github.com/openai/codex/issues/10797), [codex#33793](https://github.com/openai/codex/issues/33793) |
| A-A01 | A command rewritten into `arcforges run …` reaches the ArcForges service from inside an AI client's command sandbox. This is **not** assumed. Each client connection runs a reachability probe inside the client's own command environment, and routing by rewrite is enabled only where the probe passes. Otherwise managed execution goes through the MCP tools, which run outside the sandbox. | F-A01 |

## 6. Cloud (Cloudflare) and commerce

| ID | Fact | Source |
|---|---|---|
| V-C01 | Durable Objects can accept WebSockets through the Hibernation API (`ctx.acceptWebSocket`). Clients stay connected while the object is evicted, and billable duration does not accrue during hibernation. Ping frames are answered without waking it. Per-connection attachments persist across hibernation (up to 16,384 bytes). Only server-side WebSockets hibernate. | [DO WebSockets](https://developers.cloudflare.com/durable-objects/best-practices/websockets/) |
| V-C02 | Containers instance types range from `lite` (1/16 vCPU, 256 MiB, 2 GB disk) to `standard-4` (4 vCPU, 12 GiB). Billing counts provisioned memory and disk, and CPU only while active, at 10 ms granularity while running. Billing stops when the instance sleeps. Each container has its own Durable Object. | [Containers limits](https://developers.cloudflare.com/containers/platform-details/limits/), [pricing](https://developers.cloudflare.com/containers/pricing/) |
| V-C03 | D1: 10 GB per database, 1,000 queries per Worker invocation, 100 bound parameters, 2 MB per row, 100 columns. Each database is single-threaded (about 1,000 queries/s at 1 ms each) and returns "overloaded" when its queue fills. | [D1 limits](https://developers.cloudflare.com/d1/platform/limits/) |
| V-C04 | Cloudflare has **no hard spending cap** for Workers, Durable Objects or D1. Budget alerts are notification-only and are processed daily for the prior day. Only AI Gateway has blocking spend limits. | [budget alerts](https://developers.cloudflare.com/changelog/post/2026-06-15-budget-alerts-default-on/), [usage-based billing](https://developers.cloudflare.com/billing/understand/usage-based-billing/) |
| V-C05 | Google Play Billing Library is at 9.1.0 (June 2026). An initial subscription purchase must be acknowledged within three days of entering PURCHASED, or it is refunded and the entitlement revoked. Acknowledge server-side with `purchases.subscriptions.acknowledge` after backend verification. `obfuscatedAccountId` links a purchase to an account, and purchases made outside the app carry no such identifier. The backend reads state with `purchases.subscriptionsv2` and is driven by Real-time Developer Notifications. | [Play Billing integrate](https://developer.android.com/google/play/billing/integrate), [release notes](https://developer.android.com/google/play/billing/release-notes) |
| V-C06 | The .NET binding `Xamarin.Android.Google.BillingClient` 9.1.0.1 wraps Play Billing 9.1.0. | [NuGet](https://www.nuget.org/packages/Xamarin.Android.Google.BillingClient) |
| A-C01 | The binding restores and links in a `net10.0-android` MAUI project under the repository's Mono AOT, trimming and R8 settings. | F-C01 |
| A-C02 | A camera QR scanning library for .NET MAUI Android works under the repository's trimming, AOT and R8 settings, with manual code entry as the fallback. | F-C02 |
| V-C07 | The historical design already decided Paddle as the sole web Merchant of Record, FCM HTTP v1 with short-lived service-account credentials for push, and system-browser PKCE for native sign-in. ArcForges-Design-Parallel main `64173614`: `docs/architecture/16-billing-and-commerce-architecture.md` BC-01, `13-observability-and-operations.md`, `08-security-architecture.md`. | historical design |

**Design consequences.**
- **Live connections.** Live node and viewer connections terminate in hibernating Durable Objects through a thin adapter. The C# container is needed only for business decisions, so it can sleep when idle.
- **Cost control.** Every metered cloud path is guarded by application-enforced quotas and operating budgets with kill switches. Cloudflare budget alerts are notification only and never count as cost control.
- **Telemetry storage.** Telemetry is local-first. D1 holds account, entitlement and registry data, never time-series telemetry.

## 7. Toolchains and caches

| ID | Fact | Source |
|---|---|---|
| V-T01 | Four environment variables relocate NuGet's folders, and environment variables override NuGet.Config: `NUGET_PACKAGES` (global packages), `NUGET_HTTP_CACHE_PATH`, `NUGET_SCRATCH` (NuGet 6.2+) and `NUGET_PLUGINS_CACHE_PATH`. Processes that share the global-packages or http-cache folders **must share the same scratch folder**, or errors can occur. | [NuGet folders](https://learn.microsoft.com/en-us/nuget/consume-packages/managing-the-global-packages-and-cache-folders) |
| V-T02 | sccache uses a local cache by default (`SCCACHE_DIR`, `SCCACHE_CACHE_SIZE`, default 10 GB). Remote backends include S3, R2, Redis, Memcached, GCS, Azure, GitHub Actions and WebDAV (`SCCACHE_WEBDAV_ENDPOINT`), plus multi-level chains (`SCCACHE_MULTILEVEL_CHAIN`). sccache-dist provides distributed compilation through a scheduler. | [sccache](https://github.com/mozilla/sccache), [configuration](https://github.com/mozilla/sccache/blob/main/docs/Configuration.md) |
| V-T03 | ccache: `CCACHE_DIR`, `max_size` (default 5 GB) with LRU cleanup, and `remote_storage` (`file:`, `http://`, `redis://`). Built-in HTTP and Redis are being replaced by remote storage helpers (ccache 4.13+). | [ccache manual](https://ccache.dev/manual/latest.html) |
| V-T04 | Windows provides DNS-SD through `DnsServiceRegister` and `DnsServiceBrowse` (Windows 10+, desktop apps). A registration ends with its process, and removal events may not be delivered. | [DnsServiceBrowse](https://learn.microsoft.com/en-us/windows/win32/api/windns/nf-windns-dnsservicebrowse), [Q&A report](https://learn.microsoft.com/en-us/answers/questions/1329531/mdns-browsing-not-reporting-removals-of-entries) |
| V-T05 | Pueue is a reference design: a single-user daemon and CLI, groups with parallel limits, task states (queued, stashed, paused, running, done), dependencies, logs persisted to disk, state restored after a crash, and the environment and working directory captured at submission. Distributed execution and multi-user operation are out of its scope. | [Pueue](https://github.com/Nukesor/pueue) |
| A-T01 | MSBuild and the .NET CLI honour `MSBUILDDISABLENODEREUSE=1` and `-nodeReuse:false`. Cargo honours `CARGO_HOME`, `CARGO_TARGET_DIR` and `CARGO_BUILD_JOBS`. CMake honours `CMAKE_BUILD_PARALLEL_LEVEL`, Ninja `-j`, and npm `npm_config_cache`. The adapter tasks must confirm each with a real run on the workstation before claiming redirection or concurrency control for that tool. | F-T01 |

## 8. Future-validation index

| ID | What must be proven | Owner (delivery task) | Environment |
|---|---|---|---|
| F-W01 | Non-elevated job creation, CPU rate cap, commit cap and kill-on-close on real processes | AF-EXEC-01 | Windows workstation |
| F-W02 | Nested jobs with real `dotnet`, `cargo` and `cmake` builds | AF-EXEC-01 | Windows workstation |
| F-L01 | vmmem/vmmemWSL accounting and host/guest reconciliation | AF-WSL-01 | Windows + WSL2 |
| F-L02 | Optional privileged I/O control in the guest | AF-WSL-01 (optional leg) | WSL2 with explicit privileged install |
| F-L03 | Transient-unit executions from the node: fd-passed stdio, exact environment, durable exit record, survival across node crash, restart and update | AF-EXEC-02 | WSL2 |
| F-N01 | MCP SDK AOT publish and protocol coverage, or the in-house subset | AF-MCP-01 | Windows + WSL2 |
| F-N02 | System.CommandLine AOT publish and cold start, or the in-house parser | AF-NODE-01 | Windows + WSL2 |
| F-N03 | Windowless supervisor at logon and hidden-console CTRL_BREAK delivery | AF-EXEC-01 (logon start re-verified by AF-DIST-01) | Windows workstation |
| F-A01 | Per-client sandbox reachability probe (Claude Code, Codex) | AF-AI-02 | Workstation clients |
| F-C01 | Play Billing binding under `net10.0-android` release settings | AF-AND-03 | Local build + emulator |
| F-C02 | QR scanning library under release settings | AF-AND-01 | Local build + emulator |
| F-T01 | Each toolchain adapter's redirection and concurrency claims | AF-TOOL-01 (.NET), AF-TOOL-02 (others) | Windows + WSL2 |

Physical multi-machine LAN runs, Google Play production purchases, FCM delivery to physical devices, real Paddle production checkout and code-signing reputation are **deferred real-world validation**. They are listed in the delivery plan's acceptance register. They never block development-stage completion, and they are never reported as proven by simulation.
