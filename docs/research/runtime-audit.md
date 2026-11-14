# ArcForges V2: local runtime and shared-platform source audit

Audit date: 2026-11-14. This is a read-only source and historical-evidence audit, not a new runtime qualification. No product files, security settings or published packages were changed. No designated-host verification was run in this audit.

## 1. Exact baseline and evidence labels

The coordinator checked GitHub `main`; these local revisions match that remote baseline:

| Repository | Commit | Role |
|---|---|---|
| ArcForges | `10f692224f94916cfc93fbad971f80ec340c5edf` | Primary implementation audited |
| DesktopPlatform | `e02ebe455d4fe2c06b19dabc0f3179a43ab21aa6` | Shared packages and independent-consumer boundary |
| ArcForges-Design | `62172622550fff73a553135ca178f9b7117c9cbd` | Previous authority; evidence only where superseded by V2 |
| Plan | `742ed2660c5e934e1df86f90e54198b3a199e2b1` | Historical delivery/evidence baseline |
| ArcScope | `485c8d6d9a84825eb5bc737c9808b8bc4b616643` | Shared-package consumer audit |
| ArcSlate | `569785a050c97a8022fe264f6af986285766bf87` | Shared-contract consumer audit |
| ArcNotes | `2839da696cf3d6cc8ab3c241212eea8403c5a0a1` | Shared-contract consumer audit |
| Mobile | `072ee675e8ea67e779922082dbf65dbc02ed6916` | Shared-contract consumer audit |

Source paths below are relative to the named repository at the full commit above. `implemented/historical validation` means executable behavior exists and the old Plan has delivery evidence; it does **not** certify the new MXC composition. `implemented/source only` means this audit examined the behavior but has no new execution evidence. `scaffold` means source exists but is not the advertised product feature. `schema only` means storage definitions exist without a corresponding shipped subsystem. V2 combinations remain unverified until the new Plan's native experiments pass.

Canonical source roots:

- [ArcForges implementation at audited commit](https://github.com/ArcForges/ArcForges/tree/10f692224f94916cfc93fbad971f80ec340c5edf)
- [DesktopPlatform at audited commit](https://github.com/ArcForges/DesktopPlatform/tree/e02ebe455d4fe2c06b19dabc0f3179a43ab21aa6)
- [Old delivery graph](https://github.com/ArcForges/Plan/blob/742ed2660c5e934e1df86f90e54198b3a199e2b1/delivery-graph.json)
- [Old immutable ledger](https://github.com/ArcForges/Plan/blob/742ed2660c5e934e1df86f90e54198b3a199e2b1/ledger/ledger.jsonl)

The graph contains **63 tasks: 11 delivered, 8 complete, 36 planned, 8 superseded**. The 19 delivered/complete facts must stay historical, not be counted as completed V2 tasks. No active task remains in this baseline. Do not start AF-CTR-07.

Historical evidence relevant to local reuse:

| Old task | Recorded status | Concrete evidence | Limit on reuse claim |
|---|---|---|---|
| AF-EXEC-01 | delivered | ArcForges PRs [7](https://github.com/ArcForges/ArcForges/pull/7), [8](https://github.com/ArcForges/ArcForges/pull/8), [9](https://github.com/ArcForges/ArcForges/pull/9); final merge `f0cd6c91f7b68e6566b295e288cf39b86c2519d4` | Old Job execution, holders and output capture, not MXC or PTY |
| AF-EXEC-02 | delivered | PRs [10](https://github.com/ArcForges/ArcForges/pull/10), [11](https://github.com/ArcForges/ArcForges/pull/11), [12](https://github.com/ArcForges/ArcForges/pull/12); final merge `4b18e498d5142a95e0c667e90a8e03534eb5f692` | Old systemd execution. Some original task text still names WSL; later policy supersedes that venue. Do not reuse that wording for new tests |
| AF-RES-01 | complete | PRs [28](https://github.com/ArcForges/ArcForges/pull/28), [29](https://github.com/ArcForges/ArcForges/pull/29); merges `0d0eb0aab53e84c2a958485df1bb703c5f8398ea`, `e2696ae7107ab8f2ecac164fd85cc1a276c6f97b` | Source-backed resource observations, budgets and pressure; MXC membership/accounting must be requalified |
| AF-SCHED-01 | complete | PR [30](https://github.com/ArcForges/ArcForges/pull/30); merge `69c0657f4901a840f2819a5eae9c203276f85f5f` | Extract resource logic; do not preserve the old queue/dependency/retry product |
| AF-SEC-01 | complete | PR [31](https://github.com/ArcForges/ArcForges/pull/31); merge `218005351fd2bdcc45a4e82992d677ccf07a924c` | Old origins/approval/adoption rules are not V2 authorization policy |
| AF-CTR-06 | complete | ArcForges [77](https://github.com/ArcForges/ArcForges/pull/77), Contracts [133](https://github.com/ArcForges/Contracts/pull/133), Cloud [155](https://github.com/ArcForges/Cloud/pull/155) | Latest ledger says real native local-Go-Center/node file flows passed, with unavailable owner-only boundaries explicitly mocked. External hosted qualification/publication/deployment remains AR-26 deferred/not proven. Do not turn these into new Sandbox deletion claims |

## 2. Actual assembly and dependency map

`ArcForges.Host` is the multi-role executable. It dispatches Windows `node exec-wrap`/`node signal`; Linux `node exec-launch`, `node exec-stop`, `node exit-record`, `node guard`; and restricted file-effect/private-stage worker roles before entering the CLI. Normal CLI calls `ArcForges.CommandLine`; `node run` calls `Node.Api.NodeHost`.

The project references are real, not inferred from a diagram:

| Consumer | Project references | Relevant first-party package dependencies |
|---|---|---|
| Host | CommandLine, Node.Api | Contracts.Foundation |
| CommandLine | Client | Contracts.Node, Contracts.Fleet |
| Client | none | Contracts.Node, Contracts.Foundation, LocalRpc |
| Node.Api | Core, CloudLink, Platform.Windows, Platform.Linux | LocalRpc |
| Node.Core | Store, Client, Platform | Contracts.Node, Contracts.Foundation, Observability |
| Node.Platform | none | Contracts.Node |
| Platform.Windows / Platform.Linux | Platform | Contracts.Node |
| Node.Store | none | Contracts.Node, Contracts.Foundation, Security.Secrets |
| Node.CloudLink | Core | Contracts.Fleet, Contracts.Node, Contracts.Relay, Contracts.Foundation |
| Supervisor | none | No first-party runtime package |
| Desktop | none | Avalonia dependencies; no completed Sandbox UI |

All versions are centrally pinned. ArcForges currently consumes Contracts cohort `1.0.0-ci.450.1`; LocalRpc and Build.Policy `1.0.0-ci.138.1`; Observability and Security.Secrets `1.0.0-ci.141.1`. A V2 consumer must perform normal provenance/admission changes, not silently upgrade to unreviewed versions. ArcForges does **not** currently consume DesktopPlatform's `Persistence.Sqlite` in its node store; it has a separate working migration/store implementation. Replacing that implementation merely to increase shared-code reuse would add unrelated migration work.

`NodeHost` owns configuration/data-root resolution, per-user single instance, store open/backup/migration, unclean-shutdown quick check, boot identity, recovery hooks, capabilities, LocalRpc endpoint, housekeeping, and readiness. `NodeRuntime` is a concrete composition root containing the store, single-writer `CommandProcessor`, event journal, stream hub, settings, runtime lifecycle, execution supervisor, resource capabilities and optional cloud link. `NoCloudLink.Instance` exists, but current command policy intentionally restricts ordinary local execution; the mere optionality of that field does not prove the desired V2 offline use path.

Source: `src/ArcForges.Host/Program.cs`, all listed `.csproj`, `src/ArcForges.Node.Api/NodeHost.cs`, `src/ArcForges.Node.Core/NodeRuntime.cs`, `Directory.Packages.props`.

## 3. Resource assets: preserve the algorithms, change their owners

### 3.1 Observation and budget computation

`Resources/ResourceMonitor.cs` implements a dedicated sampling thread. The internal cadence is one second. Running-work process tables and persisted machine samples use five-second windows; an idle node reduces process-table/flush work to thirty seconds. Ten-minute housekeeping downsamples samples. Pending writes are bounded at 50,000 rows. It consumes `IResourceSampler` plus the current `ExecutionSupervisor`; V2 must replace that latter dependency with a snapshot of active Run resource scopes.

Machine capacity is CPU millicores (`logical processors * 1000`) and physical memory bytes. The current defaults in `ExecutionSettings` / `DefaultPolicy` are:

- CPU reserve = 1000 millicores + 10% of capacity.
- Memory reserve = 2 GiB + 10% of capacity.
- Asymmetric smoothing uses alpha 0.5 when unmanaged load rises, 0.1 when it falls.
- Unmanaged load = nonnegative total observed load minus managed workload load and Node/helper load.
- CPU budget = `max(minManagedCpu, capacityCpu - reserveCpu - smoothedUnmanagedCpu)`; current minimum = 1000 millicores.
- Memory budget = `max(0, capacityMemory - reserveMemory - smoothedUnmanagedMemory)`.

Those are the **old implemented defaults**, not a claim that every default is suitable for every V2 host. In particular, a minimum CPU floor, and the old 256 MiB lower bound for managed memory when computing root limits, can exceed an aggressively small configured capacity/reserve combination. V2 validation must clamp/reject impossible policy combinations and expose the accepted effective policy; do not promise mathematically absolute host reserves that the OS cannot enforce.

`ExecutionSupervisor.NextRootBudget` implements useful hysteresis: changes count above 5% of total capacity, falls apply immediately, rises wait until ten seconds since the last update, and a forced change applies immediately. Reuse it as a pure budget-change decision. Current `UpdateRootLimits` schedules platform work and records the intended values before the setter finishes; it is **not** a universal continuous readback proof. V2 must distinguish requested, accepted and OS-read-back effective limits with observation time and failure code.

### 3.2 Memory accounting is not cross-platform identical

The old `AttemptUsage.MemoryBytes` explicitly means resident memory excluding reclaimable page cache:

- Windows: sum of private working sets of Job members; CPU/I/O come from Job accounting, retaining exited members' cumulative CPU.
- Linux: cgroup `memory.current - inactive_file`; CPU from `cpu.stat usage_usec`, I/O from `io.stat`, membership from `cgroup.procs`.

The old admission accounting reserves `max(mem_expected, peak_observed)` for each running attempt. The monotonic peak avoids admitting new work merely because another process temporarily drops resident usage. Keep this as an admission estimate with a name that does not imply an OS hard limit.

Windows Job memory limits bound **committed memory**, not physical RSS. The old root sets a fixed commit limit of `commit_factor * managed_share` (default factor 1.5), with a pressure notification threshold from the dynamic memory budget. Linux has `MemoryHigh` from the dynamic budget and a separate fixed `MemoryMax` from the managed share, plus swap allowance. These distinctions must remain visible in V2 resource snapshots, APIs, UI labels and acceptance tests.

### 3.3 Pressure behavior worth retaining

`PressureEvaluator` is pure: caller supplies time and inputs. Normal/Tight/Pressure/Critical transitions require five seconds' persistence (six roughly one-second evaluations, with a 500 ms scheduling tolerance). Current available-memory fractions are 10%, 5%, 2%. Linux `memory some avg10 > 20` produces Pressure; unmanaged CPU rising by more than 20% of capacity in ten seconds produces Tight; a newly observed machine OOM kill holds the Critical condition for ten seconds.

`CriticalShedding` is a particularly valuable tested asset. It does not kill a victim every second of an OOM hold. One unanswered machine OOM event can trigger at most one stop while raw memory is no longer critical. After a selected victim stops, the algorithm waits for its finalization and one additional sample before considering another. Victims must be explicitly preemptible, launched, not finalizing, not already stopping and not already ending from their own OOM. Lowest priority and most recent start win selection.

The **old response policy** also includes Linux freezing of low/background attempts plus reduced `MemoryHigh`, and Windows cancellation/requeue where retry rules allow. Keep the measurement/hysteresis and safe victim selection. Remove automatic restart/requeue semantics for V2 generic Runs. A stopped CLI Run remains stopped; restarting is a new explicit Start with a new Run ID. Windows cannot claim a supported Job-wide freeze merely because Linux can freeze cgroups.

### 3.4 What the old scheduler actually contains

`Scheduling/AdmissionEngine.cs` is not a thin CPU allocator. It includes task feasibility, global/pool/workspace/session limits, exclusive/shared concurrency keys, task priority aging, pool weighted credits, per-owner deficit round robin, large-task reservations, estimated-duration backfill, queue walking and resource reservation. `RetryRules.cs`, `ServiceReadiness.cs`, `ToolConcurrency.cs`, and much of `ExecutionSupervisor.Scheduling.cs` implement old product semantics.

V2 should keep a small start-time admission transaction and ongoing resource coordinator. Preserve host budget, per-Sandbox quota/weight, per-Run cap, and explicit pressure policy. Refuse a start with a bounded `resource_unavailable` result when immediate admission is impossible; do not revive the old persistent Task queue to hide admission failures. Any later queued-start feature requires separate product authorization.

Key sources: `Resources/PressureEvaluator.cs`, `Resources/CriticalShedding.cs`, `Resources/ResourceMonitor.cs`, `Resources/ResourceSamples.cs`, `Resources/ResourceViews.cs`, `Execution/ExecutionSupport.cs`, `Execution/RunningAttempt.cs`, `Execution/ExecutionSupervisor.Scheduling.cs`, `Scheduling/AdmissionEngine.cs`, `Node.Platform/ResourceSampling.cs`.

## 4. Existing platform behavior and MXC replacement boundaries

### Windows

`WindowsExecutionPlatform` creates/reopens `Local\\ArcForges.<node>.root`, with a hard CPU cap, commit limit and notification limit. Per-attempt jobs are nested below it with a CPU weight or cap, commit limit, optional active-process limit and no breakaway. A separate `exec-wrap` holder retains handles across Node restarts; kill-with-node mode uses `KILL_ON_JOB_CLOSE`. Root setup runs a probe; Job wrappers expose CPU/limit readback and own-limit evidence. Completion ports deliver process/limit notifications.

The current public capability report **does not claim** pids enforcement, because no current policy field actually sets a process-count limit. It reports I/O observation only, no supported Job-wide pause, and limited same-user adoption. `Adopt` expressly refuses a process already in a foreign Job to avoid attaching the ArcForges hierarchy to it. This is directly relevant to MXC: simply taking an MXC-created process and assigning the old root/attempt Jobs afterwards contradicts an existing carefully defended constraint, and may leave a launch window before accounting/limits apply.

The old capability string is explicit that same-user code can change or end ArcForges containers, and work launched outside tracked ancestry never joins them. Therefore the old runtime is resource/process management, **not** the new sandbox isolation boundary. `EscapedProcesses` ancestry scans do not catch arbitrary broker/WMI/parent-spoofed external launches, which old Plan/Design already acknowledge.

V2 action: let MXC own process creation and isolation. Keep resource sampling and only the proven official integration path for Job limits/accounting. Qualify the exact SDK version and assignment ordering in a two-Run nested-Job experiment before deleting old critical control code. A missing official pre-execution or resource-owner mechanism is a blocker for the combined guarantee, not permission to fork MXC or silently run uncontained.

### Linux

`LinuxExecutionPlatform` uses the systemd user manager with minimum version 247. Root `arcforges.slice` receives runtime `CPUQuota`, `MemoryHigh`, `MemoryMax`, `MemorySwapMax` and `TasksMax`; per-attempt `arcforges-a-<attempt>.service` provides lifecycle/accounting. Startup verifies actual cgroup files (`cpu.max`, `memory.high`, `memory.max`, `pids.max`). Controllers missing from delegation become observe-only. Without a user manager, it falls back to `DirectAttemptHandle` plain child processes and reports degraded capability.

The user-unit `ReadOnlyPaths`/`InaccessiblePaths` hardening is documented in code as protecting ArcForges' own files, **not workload isolation**. Linux helpers handle output descriptors, launch environment, exit records, stop/end-step budgets, heartbeat takeover and frozen-cgroup recovery. `FreezeUnit` and `ThawUnit` are real lifecycle operations; tests and source include the special care required for frozen groups that block manager spawning.

V2 action: bubblewrap/MXC provides sandbox isolation; retain only necessary systemd/cgroup orchestration for resource ownership and a trusted owner process, after proving launcher, helper and descendants all enter the intended hierarchy before executing user code. The existing plain-process degraded path must be removed from sandbox Run admission: resource observation-only can be an explicit capability, but loss of filesystem/network/process isolation cannot be treated as a working sandbox. A backend cannot claim same recovery behavior merely because both old and new paths use Linux.

Sources: `Node.Platform.Windows/WindowsExecutionPlatform.cs`, `JobObject.cs`, `ProcessLauncher.cs`, `AttemptRunner.cs`, `WindowsAttemptHandle.cs`, `EscapedProcesses.cs`; `Node.Platform.Linux/LinuxExecutionPlatform.cs`, `LinuxAttemptHandle.cs`, `DirectAttemptHandle.cs`, `SystemdManager.cs`, `UnitControl.cs`, `HelperRoles.cs`, `GuardRole.cs`.

## 5. Terminal, lifecycle and data gaps

### Terminal

Current `RunCommand` submits TaskService requests and mirrors stdout/stderr bytes. `--stdin stream` copies bytes with `WriteTaskInput`; `Ctrl+C` first cancels a Task, second detaches. `--client-timeout` releases a caller binding for AI-client timeouts. No PTY/ConPTY terminal integration was found in shipped projects. Pipe forwarding, output files and attach IDs provide reusable framing ideas, but are not evidence of TUI redraw, line discipline, process groups, Ctrl+C delivered to a foreground application, terminal resize or detach survival.

V2 needs explicit `terminal` versus `pipes` start modes. Terminal Run ownership must live in the trusted long-lived owner, independent of a CLI connection; detach must not accidentally close the PTY master. One input writer lease, multiple authorized viewers if supported, bounded output replay, resize ownership, output offsets/gaps and reconnect semantics need their own contract. Do not globally log stdin, which includes passwords and tokens. Terminal raw-byte output is potentially sensitive and needs bounded local retention rather than automatic cloud upload.

### Local-first authorization

`LocalSubmission` and `TaskServiceHandler` intentionally allow ordinary local submit only for HUMAN diagnostics. SCRIPT is admitted only on a test-mode Node with `ARCFORGES_TEST_ALLOW_LOCAL_SCRIPT_SUBMIT=1`; AGENT is never admitted by that test seam. `RunCommand --local` is advertised as HUMAN diagnostics, while normal work is routed through Center. V2 must replace this with authenticated per-user local authorization for general callers without interpreting AI/session identity. Do not teach production users to set test variables or spoof HUMAN origin.

### Lifecycle and recovery

`NodeHost` and `INodeRecoveryParticipant` already provide a sound startup recovery boundary before normal service readiness. Old attempts store durable launch and exit records, named ownership, boot identity, process creation times and acknowledgment. They distinguish reattaching a genuinely live resource from finalizing a durable completed record. Preserve these concepts while replacing Task/Attempt state and old helper ownership.

A persistent Sandbox directory does not make an MXC container persistent. A Run needs a stable Run ID and immutable start-policy/configuration snapshot, plus an owner identity and platform resource identity. Reconciliation must not trust a bare PID after restart. On Node restart, reattach only when identity and ownership are proven; otherwise report a specific Lost/Unknown/ReconciliationRequired state, retain data, and do not terminate a process merely because its numeric PID matches. Survive Node restart and survive the owner process crash are different promises; experiments must settle each independently.

### Files and deletion

Current data root is configurable and includes `store/node.db`, run metadata and output/attempt directories. `StorePaths.CreatePrivateDirectory` creates new Linux directories with mode 0700, but leaves existing directories unchanged; that helper alone is not sufficient validation of an externally supplied V2 data root. Data root checks must verify owner, permissions, links/reparse points, root identity and nesting independently.

AF-CTR-06 added extensive real file-identity and mutation protections: opened-object identity, no-follow traversal, private stage reservations, full-durability effect journals, guards, worker PID/creation identity, quarantine/removal plans, actual-worker-exit fences and unknown-effect handling. Reuse the primitives and negative tests that support owned-Sandbox data deletion/import/export. Remove the old Center-routed workspace search/edit platform, AGENT-created-file inference and generic host cleanup policy after its records are settled/exported.

`FileCreationOwnership` states in its own contract that creation evidence is metadata, not cleanup authority. `AttemptTempProvenance` similarly records exclusive-create identity but requires fresh caller/liveness/native-identity/protection checks at deletion time. Preserve this distinction. A Sandbox data path must not become ownership proof merely because its text begins with the configured data root. External writable mounts remain user-owned and must never be traversed for recursive Sandbox deletion. No unprivileged mechanism can promise safe arbitrary-host-tree cleanup against every hostile same-user process; narrow the operation to ArcForges-created private Sandbox roots and fail closed when guards/ownership cannot be established.

Sources: `CommandLine/RunCommand.cs`, `Core/LocalSubmission.cs`, `Api/TaskServiceHandler.cs`, `Client/NodeLocations.cs`, `Core/Recovery.cs`, `Store/StorePaths.cs`, `Core/Files/FileCreationOwnership.cs`, `Core/Execution/AttemptTempProvenance.cs`, `Core/Platform/WorkspacePath*.cs`, `WorkspaceWriteGuard*.cs`, `LinuxOwnedPidfd.cs`, `WindowsOwnedStageProcess.cs`, `Files/FileMutationJournal*.cs`.

## 6. Asset disposition, with deletion dependencies

All ArcForges paths below are under `src/` unless another prefix is shown. KEEP preserves the useful implementation, subject to new contracts; REWORK extracts/adapts behavior; REPLACE_WITH_MXC removes the old execution owner only after the native substitution gate. FUTURE preserves independent shared assets without making them V2 prerequisites.

| Asset and source scope | Actual state | Classification | Decision and dependency |
|---|---|---|---|
| `Node.Core/Resources/PressureEvaluator.cs` | implemented/historical validation | KEEP | Reuse pure smoothing/pressure math with V2 names/policy validation and preserved regression tests |
| `Node.Core/Resources/CriticalShedding.cs` | implemented/historical validation | REWORK | Retain bounded victim selection; use Run identity and explicit preemptibility; remove retry/requeue consequence |
| `Node.Core/Resources/ResourceMonitor.cs` | implemented/historical validation | REWORK | Replace supervisor/attempt coupling by active Run scope snapshots; preserve bounded sample cadence and node/unmanaged separation |
| `Node.Core/Resources/ResourceSamples.cs`, `ResourceViews.cs` | implemented/historical validation | REWORK | V2 Run/Sandbox identifiers, time series and retention; distinguish unknown counters from zero |
| `Node.Platform.Windows/WindowsResourceSampler.cs` | implemented/historical validation | KEEP | Host CPU/memory observation remains useful independently of MXC |
| `Node.Platform.Linux/LinuxResourceSampler.cs`, `ProcFs.cs` | implemented/historical validation | KEEP | Host observation/PSI; reuse cgroup parsing only for verified Run resource ownership |
| `Node.Core/Execution/ExecutionSupport.cs` resource settings and `NextRootBudget` in Scheduling partial | implemented/historical validation | REWORK | Extract budget/reserve/hysteresis; discard Task/AI/cache policy members |
| `Node.Core/Execution/RunningAttempt.cs` peak accounting | implemented/historical validation | REWORK | Retain conservative expected/observed reservation in Run model, not Attempt semantics |
| `Node.Core/Scheduling/AdmissionEngine.cs` queue/pools/DRR/reservations | implemented/historical validation | REMOVE | Replace by immediate bounded Run admission plus ongoing resource shares; remove persistent queue API/storage |
| `Scheduling/ConcurrencyKeys.cs`, `RetryRules.cs`, `ServiceReadiness.cs`, `ToolConcurrency.cs` | implemented/source and tests | REMOVE | Old dependency/key/retry/adapter product is cancelled; no replacement abstractions for future tools |
| `Execution/ExecutionSupervisor*.cs`, `RunningAttempt.cs`, `TaskRecords.cs`, `Adoptions.cs`, `ExecutionHooks.cs` | implemented/historical validation | REWORK then REMOVE old runtime | Extract only resource and ownership primitives; replace Task/Attempt supervisor with one Sandbox/Run core; remove old classes after parity gates |
| `Node.Platform/ExecutionPlatform.cs` old `IExecutionPlatform`/`IAttemptHandle` | implemented/historical validation | REPLACE_WITH_MXC | New internal SDK adapter must model actual MXC ownership, capabilities and failure; do not make the old interface a permanent compatibility facade |
| `Platform.Windows/ProcessLauncher.cs`, `AttemptRunner.cs`, `WindowsExecutionPlatform.cs`, exec-wrap launch ownership | implemented/historical validation | REPLACE_WITH_MXC | Remove after official SDK startup/terminal/resource/lifecycle proof. Retain scoped necessary interop only where SDK lacks required observable resource behavior |
| `Platform.Windows/JobObject.cs`, `WindowsAttemptHandle.cs` | implemented/historical validation | REWORK | Retain only officially compatible Job read/control primitives; no automatic transplant of the root/attempt nesting topology |
| `Platform.Windows/EscapedProcesses.cs`, `WindowsAdoptedJob.cs` | implemented/historical validation | REMOVE | Host-process adoption and ancestry-based escape cleanup are outside V2; strict MXC failure must not fall back to this |
| `Platform.Linux/LinuxExecutionPlatform.cs`, `LinuxAttemptHandle.cs`, launch/end/guard helper roles | implemented/historical validation | REPLACE_WITH_MXC | Replace old process creation; extract proven cgroup/systemd resource owner integration when needed |
| `Platform.Linux/SystemdManager.cs`, `UnitControl.cs` | implemented/historical validation | REWORK | Keep only required user-service/resource lifetime and readback functions, not the old Task unit contract |
| `Platform.Linux/DirectAttemptHandle.cs` | implemented/degraded fallback | REMOVE | Plain-process fallback cannot satisfy a Sandbox isolation request |
| `Platform.Linux/LinuxAdoptedScope.cs` | implemented/source | REMOVE | Foreign host process adoption is cancelled |
| `Node.Core/NodeRuntime.cs`, `NodeLifecycle.cs`, `Recovery.cs`, `CommandProcessor.cs` | implemented/historical validation | REWORK | Keep single writer/startup reconciliation/boot identity; compose one Sandbox core, resource manager and optional remote transport |
| `Node.Core/Events/*`, `PageCursor.cs`, `Notifications.cs`, `NodeLog.cs` | implemented/historical validation | REWORK | Preserve bounded event cursors/backpressure and structured errors; remove Task/AI topics |
| `Client/*`, `Node.Api/NodeHost.cs`, `NodeApiServer.cs`, `NodeServiceHandler.cs`, `ClientSessions.cs` | implemented/historical validation | REWORK | Keep per-user endpoint/handshake/autostart, register V2 APIs and local permissions |
| `Node.Core/LocalSubmission.cs`, `Security/PermissionMatrix.cs`, `CenterRouting.cs`, origin-based rules | implemented/historical validation | REWORK | Ordinary local CLI is first-class and offline; remote grants bound to Sandbox/Run actions, no AI origin inference |
| `Node.Core/Security/AuditLog.cs`, `Approvals.cs`, `VersionIntegrity.cs` | implemented/historical validation | REWORK | Keep durable metadata audit and integrity; approvals only for explicit capabilities/consent, not old Agent platform |
| `Node.Api/TaskServiceHandler.cs`, `QueueServiceHandler.cs`, `Core/Jobs.cs`, `CommandLine/Task*`, `QueueCommands.cs`, `JobCommands.cs` | implemented/historical validation | REMOVE | Delete after V2 Sandbox/Run handlers and local CLI replacement; do not leave disabled route shells |
| `CommandLine/CliApplication.cs`, output/errors/duration/config/status/resource helpers | implemented/historical validation | REWORK | Rebuild command hierarchy; reuse parsing/structured output, remove old options and help/completions |
| `CommandLine/RunCommand.cs` | implemented pipes, no PTY | REWORK | New Run request, terminal mode/resize/signals/attach lifecycle, no AI timeout handoff/dependency/retry flags |
| `Node.Platform/OutputIndex.cs`, `Core/Execution/OutputReader.cs`, `AttemptFiles.cs` | implemented/historical validation | REWORK | Bounded per-Run logs with output gaps/replay; split terminal stream from piped stdout/stderr |
| `Node.Store/NodeStore.cs`, `StoreTransaction.cs`, `CommandDeduplication.cs`, `Migrations/*` | implemented/historical validation | KEEP/REWORK | Reuse durable transaction, backup and monotonic migration machinery; append V2 migrations and receipts |
| `Node.Store/Schema/0001..0015`, `schema-history.json` | released history; mixed live/dormant schema | KEEP history | Never edit released migration bytes. Later forward contract migration removes old live tables after copy/export/settlement |
| Old `task`, `attempt`, queue/dependency/session/hook/cache/CAS/toolchain/LAN/mobile tables | mixed implemented/schema only | REMOVE from active schema | Explicit migration inventory below; no empty tables for cancelled work |
| `Node.Store/Secrets/*`, `Environment/SecretNameMatcher.cs` | implemented/historical validation | REWORK | Preserve node keys/credential redaction and local secure storage; replace task-scoped secrets/environment snapshots with bounded Run state |
| `Node.Core/Files/*`, `Platform/WorkspacePath*`, held identity/worker primitives | implemented/historical AF06 evidence | REWORK | Extract native-owned-root safety, staging, durable unknown effect; narrow to Sandbox-owned data import/export/delete |
| `Node.Api/FileServiceHandler*`, `WorkspaceServiceHandler`, `FleetServiceHandler*`, `WorkspaceCatalog`, `WorkspaceGitStatus`, `CommandLine/WorkspaceCommands`, general `FileOperationCommands` | implemented/historical AF06 evidence | REMOVE after migration | Old remote host file/search/workspace/cleanup platform is cancelled; retain only explicitly designed Sandbox data operations |
| `Node.CloudLink/*` | implemented/historical validation | REWORK | Keep credential/channel/replay/signature assets; map only V2 remote action allowlist and local capability grants |
| `Supervisor/*`, `Client/NodeAutoStart.cs`, `eng/systemd/arcforges-node.service` | implemented/historical validation | REWORK | Node service continuity remains needed; do not confuse Windows supervisor GUI subsystem with a user-facing desktop client |
| `ArcForges.Desktop/*`, `tests/ArcForges.Desktop.Tests/*` | Hello World scaffold | REMOVE early | Remove Avalonia package/solution/publish/package entries and desktop-only gates; keep Windows Node supervisor |
| Product MCP/Hook/Harness projects | not present in current shipped `src/` inventory | REMOVE obsolete specifications/dependencies | No nonexistent code deletion claims. Remove remaining old CLI options/contracts/schema/policy expectations; preserve development MCP host access |
| Toolchain/CAS/compiler-cache/worktree management | mostly schema/design, no corresponding shipped project | REMOVE | Delete dormant schema/config/contracts in forward cleanup, not fabricate implementation migration |
| `tools/ArcForges.TestLoad`, `ArcForges.Bench`, native test fixtures | implemented/historical evidence | REWORK | Keep synthetic CPU/memory/fork/output probes and useful size/startup measurement; add genuine terminal/MXC composition tests, remove cancelled product assertions |
| Repository build/admission/package inventories | implemented | REWORK | Exact dependency closure, new shipped-project list, AOT probes and SBOM/license; no weakening host/security gates |

## 7. Shared DesktopPlatform boundary

| Shared package/scope | Classification | Concrete reuse or constraint |
|---|---|---|
| `src/BuildingBlocks/ArcForges.LocalRpc` | KEEP | Real Windows named pipes/Unix-domain endpoints, service endpoint mode, peer identity, bounded lanes/deadlines, stream admission and typed refusal; V2 owns durable command receipts. This is local transport, not an isolation boundary |
| `src/BuildingBlocks/ArcForges.Security.Secrets` | KEEP | Windows Credential Manager, Linux Secret Service and explicitly weaker owner-only file selection; must stay outside Sandbox mounts and environment. Same-user-shared backing stores do not themselves deny a hostile sibling process |
| `src/BuildingBlocks/ArcForges.Observability` | KEEP | Typed metadata/redaction processor and bounded telemetry; paths/tokens/free text are removed from exported spans. New Sandbox/Run vocabulary needs intentional admission, not bypassed redaction |
| `eng/` Build.Policy and admission/provenance | KEEP | Continue existing central versions, locked restore, AOT warnings and package provenance; update only necessary consumer inventories |
| `ArcForges.Persistence.Sqlite` | FUTURE/independent KEEP | Real migration/journal library, but Node currently has its own store. Do not add a migration of store technology to V2 without demonstrated need |
| Foundation, Security, Security.Audit, NativeInterop | KEEP where consumed | No wholesale shared-repository deletion. Use only concrete V2 needs |
| Desktop shell/design system/application-family APIs/native image/ContentSandbox | FUTURE for ArcForges V2; retain independent assets | Do not add them to CLI dependency closure or delete from shared repository. ContentSandbox is not an MXC substitute |

Independent consumers were inspected at their pinned commits: ArcScope actually references Foundation, Application.Abstractions, Native.Image/Runtime.win-x64, LocalRpc.Scope, Contracts.PublicApi, Persistence.Sqlite; its tests also use Assistant.Abstractions/Capabilities. ArcSlate and ArcNotes reference Contracts.PublicApi. Mobile references Contracts.PublicApi and Contracts.Events. These products are not V2 prerequisites and must not be damaged by broad package/namespace removal.

Sources: DesktopPlatform `LocalRpc/LocalRpcEndpoint.cs`, `LocalRpcServer.cs`, `LocalRpcCallAdmission.cs`, `LocalRpcClientChannel.cs`; `Security.Secrets/SecretStoreSelection.cs`, `OwnerOnlyFileSecretStore.cs`, `WindowsCredentialManagerSecretStore.cs`, `OsSecretStoreGuard.cs`; `Observability/RedactionProcessor.cs`; `Persistence.Sqlite/Migrations/MigrationRunner.cs`; the consumer `.csproj` files named above.

## 8. Node database migration inventory and order

The store currently advertises **SupportedSchemaVersion = 15** and the final migration's `min_reader_version = 15`. Steps 13–15 raised reader compatibility because old binaries cannot safely share the new ownership/worker-hold state. An in-place rename of v1 tables or rewriting `0001-schema-v1.sql` would violate actual migration semantics and strand deployed data.

Preserve history, then implement a bounded migration:

1. Stop new v1 work; drain or explicitly stop every old attempt and reconcile launch/exit records. Do not run old Task and new Run engines permanently in parallel.
2. Reconcile every file-operation journal/private-stage reservation/worker exit and target hold. An unresolved possible effect blocks destructive cleanup; it is not an empty table to drop.
3. Take the existing durable backup. Record source schema, node identity, inventory digest and migration result. Preserve previous binary/backup according to rollback policy.
4. Append an expand migration for Sandbox, Run, policy revisions, owned roots/mount grants, owner identities, resource state/history and operation receipts. Translate only semantics that really carry over (node identity/configuration, resource policy, optional Center enrollment). Never automatically turn arbitrary registered host workspaces into owned Sandbox roots or new writable grants.
5. Export legacy task history/audit according to retention. Do not claim old attempts were sandboxed. Creation of a new Sandbox requires a new owned root; a requested data import copies files under reviewed traversal/size bounds.
6. Append a contract migration, raising minimum reader version, to remove retired active tables and obsolete columns after the explicit compatibility cutoff. Old released migration files stay as history; fresh installs may execute them and contract away the old tables, leaving a clean final schema. A later separately reviewed squash strategy may optimize bootstrap, not rewrite deployed history casually.
7. Rollback before contract is restore-before-start, not an old binary sharing a new store. After contract, restore the named backup and document loss of post-cutover V2 changes; never silently downgrade.

Table families to classify explicitly in migration implementation:

| Family | Tables / patterns at baseline | V2 treatment |
|---|---|---|
| Core durable infrastructure | `store_meta`, `node_setting`, `policy_document`, `command_dedup`, `event_journal`, `audit_log` | Preserve/adapt schema and receipt namespaces; do not copy obsolete command results as V2 receipts |
| Task product | `job`, `task`, `task_concurrency_key`, `task_dependency`, `attempt`, `task_secret`, `env_snapshot`, `timeline_segment`, `phase_event` | Export necessary historical records; replace by Run model; remove active tables at cutoff |
| AI/hook/session | `session`, `session_subagent`, `hook_event`, `probe_result`, `probe_ticket` | Remove after needed audit export; no V2 replacement |
| Cache/toolchain | `result_cache_observation`, `attempt_cache_usage`, `cache_usage_window`, `cache_store_ledger`, `cache_walk`, `cache_instance`, `cache_stat`, `cas_blob`, `manifest`, `toolchain` | Remove final schema; don't implement unused features merely to migrate them |
| General workspace/storage | `workspace`, `worktree_archive`, `managed_directory`, `root_location`, `size_cache`, `file_digest_cache`, `storage_analysis`, `storage_analysis_item`, `cleanup_plan`, `cleanup_item`, `quarantine_entry` | Replace by narrow Sandbox ownership/size/deletion receipts; settle old quarantine and preserve user data first |
| Old delegated/LAN/mobile | `peer`, `pairing`, `offer`, `remote_attempt`, `guest_link`, `host_link`, `guest_grant`, `phone_pairing`, `push_outbox` | Remove current product bindings; no deletion of independent Cloud/shared product data by name similarity |
| Useful observations/audit | `process_record`, `resource_sample`, `finding`, `approval`, `notification`, `fact` | Keep only required V2 fields/retention, remove Task/AI foreign keys and old fact-learning product |
| Identity/remote | `account_link`, `sign_in_flow`, `remote_command_log`, `routed_call_log` | Rework for optional remote channel and V2 operations, with credential/replay migration |
| Update/integration/support | `update_state`, `integration_plan`, `integration_write`, `support_bundle` | Keep update metadata if consumed; remove old hook/integration tooling and unnecessary support-platform abstractions |
| AF06 journals/ownership | `routed_file_*`, `routed_verified_call_id`, `workspace_root_identity`, `workspace_inventory_revision`, `file_operation_journal`, `file_private_*`, `file_effect_worker`, `file_removal_*`, `file_attempt_temp_identity`, `file_ownership_*`, `file_creation_ownership`, `file_stage_*` | Settle/export old operations. Retain only proven primitives and new Sandbox-purpose records; never discard active unknown-effect/worker fences |

Source: `Node.Store/Migrations/StoreMigration.cs`, `StoreBackups.cs`, `Schema/0001-schema-v1.sql` through `0015-schema-step-15.sql`, `Schema/schema-history.json`.

## 9. Concrete V2 local delivery slices

These are scope proposals for the coordinator's new task graph; they are not new active tasks or status changes. Cross-repository contract publication and MXC experiments precede consumers.

| Slice | Code scope and output | Must remove / migration | Observable acceptance and rollback |
|---|---|---|---|
| Local baseline/freeze | Store inspection, release inventory, process/record reconciliation tool under `eng/`; V2 source inventory | Freeze Task submit at explicit cutover, export old status without claiming V2 completion | Dry-run names all live work and unresolved holds; no mutation on failed preflight; old binaries/data unchanged until approved cutover |
| Remove isolated desktop scaffold | Desktop project/tests, solution, publish/package/project lists, Avalonia pins and license/admission entries | Actual scaffold and closure removed; retain Supervisor | CLI/Node build/AOT/package remain complete; no desktop executable/package shipped; revert single isolated change if closure incomplete |
| MXC native composition proof | Minimal test-only official SDK consumer under `experiments/` or existing test tools | No old backend deletion yet | Native Windows/Linux prove pre-exec isolation, terminal, nested resource ownership, stats, stop, owner crash and reconnect. Failed combinations block dependent implementation |
| Sandbox/Run domain/store | New Core domain + append-only Store migrations, immutable policy/start snapshots, revision/CAS and receipts | No old v1 state relabelled as sandboxed; semantic translation explicit | Crash/retry creates one object or a durable unknown result; invalid revisions fail before effect; named backup recovery works |
| Windows SDK adapter | New internal MXC integration; verified Job read/control adapter only where necessary | Remove old CreateProcess/attempt Job launch path once replacement passes | Denied launch has no executing user process; cap/identity/readback correct under two simultaneous Runs; no Job inheritance escape window |
| Linux SDK adapter | New bubblewrap/MXC integration with the proven user-service/cgroup owner | Remove DirectAttemptHandle and old uncontained fallback | Namespace/mount/network failure refuses Run; cgroup counts all managed descendants; missing controller is explicit and required guarantees fail closed |
| Terminal owner | Run-owner lifetime, PTY/ConPTY according to SDK capability; bounded terminal transport | Remove AI client-timeout handoff and pipe-as-terminal assumptions | TUI, byte input, Ctrl+C, resize, root/descendant exit, disconnect/reattach; no stdin logging; owner loss correctly classified |
| Resource observation extraction | Existing samplers, pure budget/pressure and Run membership aggregator | Remove Task/Attempt/Fleet dependence from observation | Same known samples yield old math where intentionally unchanged; native accounting excludes Node overhead/double count; unknown samples do not appear as zero |
| Resource coordination | Per-Sandbox budget/weight and per-Run cap, immediate admission, effective-limit state | Remove queue DRR/backfill/dependencies/retries and Windows requeue | Multiple Runs honor total budget, no silent guarantee loss, OS setter/readback failure visible; no automatic restart of side effects |
| Local API/CLI | V2 typed services in Node.Api/Client; `sandbox` and `run` command family, normal offline local use | Delete HUMAN diagnostic-only gate and old commands/options; publish migration help | Signed out, expired subscription and unreachable Center still allow permitted local create/start/stop/delete; remote-disabled state cannot block local Core |
| Sandbox data | Owned root allocation, HOME/config/cache/temp mapping, mount grants, size/import/export/delete | Delete generic host workspace/Git/cache cleanup routes after settled records | Relative-path/link/reparse/mount escapes refuse; running Run prevents delete; external writes/mounts never recursively deleted; interrupted copy/delete recovers |
| Recovery/cutover | Run owner identity, boot identity, durable terminal/effect records, V1 drain, contract migration | Remove old execution engine/helpers/unserved v1 handlers after cutoff | Node restart reattaches only authenticated owners; PID reuse cannot kill foreign process; old table/route/flag absence verified; rollback uses exact backup |
| Local release qualification | Existing package/AOT/test tools plus new SDK/native assets | Dependency/third-party notices and cancelled-project entries cleaned | Native Windows/Linux packaged CLI passes functional matrix; approved ARM64 build coverage and platform claims match evidence; no test-only flags in production |

Task tests should preserve useful existing negative cases instead of recreating identical algorithms' tests. Material tests to adapt include `ResourceModelTests`, `ResourceServiceTests`, `AdmissionPolicyRaceTests`, `ResourceTests*.cs`, platform `ResourceSamplerTests`, Windows `MemoryEvidenceTests.ARealNestedJobLimitPacketDoesNotAttributeItsLimitToTheAttempt`, lifecycle/attempt-phase recovery suites, and file-identity/quarantine/worker-interruption suites. Do not carry cancelled UI/AI/cache feature assertions into V2 acceptance.

## 10. Remaining explicit qualification gaps

1. No source examined here proves official MXC SDK terminal/resource/lifecycle combinations. The independent MXC report and new P1 native experiments decide those points.
2. No new native test was run by this audit. Historical complete/delivered states are preserved accurately, with their original mock/defer boundaries.
3. Current Job/cgroup containment is not a security sandbox and has documented same-user/external-broker limitations. It cannot be presented as a drop-in MXC fallback.
4. Current stdout/stdin streaming is not PTY compatibility. Terminal attach after CLI disconnect and owner crash survival need separate tests.
5. Existing root-limit setters/probes do not prove every dynamic update has been read back correctly; V2 effective-state reporting is additional work.
6. Current signed routed file command machinery is tied to old identities/operations. Its safety patterns can be reused, but its RPCs are not new Sandbox authority.
7. Published Contracts cohort 450.1 and shared independent-consumer packages are not removable from registries. Stop consuming old routes/version interfaces via documented cutoff; keep immutable released artifacts and migration history.
8. Development Windows/Linux MCP hosts remain mandatory verification venues under current repository policy; cancellation of product MCP does not cancel those hosts or permit agent-sandbox substitution.
