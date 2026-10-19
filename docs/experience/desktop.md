# ArcForges Desktop

Architecture: [12](../architecture/12-client-applications.md) §2. Template and standard states: [README](README.md). Every Desktop page runs with origin `HUMAN`. Every page applies S-LOADING, S-NODE-STOPPED, S-RECONNECTING, S-INCOMPATIBLE and S-FAILED unless stated otherwise. Figures in the mockups are illustrative: an example host with 16 logical processors and 32 GiB.

## Shell

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ArcForges  ● Node ready  CPU 6.2/13.4 cores  Mem 9.8/19.6 GiB  ◐ Normal  🔔 3 ☺ │ status bar
├────────────┬─────────────────────────────────────────────────────────────────┤
│ Overview   │                                                                 │
│ Tasks      │                         content area                            │
│ Queue      │                                                                 │
│ Resources  │                                                                 │
│ Sessions   │                                                                 │
│ Findings ②│                                                                 │
│ Approvals ①│                                                                 │
│ Workspaces │                                                                 │
│ Storage    │                                                                 │
│ Caches     │                                                                 │
│ Toolchains │                                                                 │
│ Integrations│                                                                │
│ LAN        │                                                                 │
│ Account    │                                                                 │
│ Policy     │                                                                 │
│ Updates    │                                                                 │
│ Diagnostics│                                                                 │
│ Settings   │                                                                 │
└────────────┴─────────────────────────────────────────────────────────────────┘
```

- **Status bar.** It shows the node state, managed CPU and memory against their budgets, the pressure level, a notifications button and the account menu. Clicking a gauge opens Resources.
- **Global keys:**
  - `Ctrl+K`: command palette (reused shell model);
  - `Ctrl+1…9`: first nine pages;
  - `Ctrl+N`: Run task;
  - `F5`: refresh the current page snapshot;
  - `Ctrl+,`: Settings.
- **Navigation badges** show counts of open error findings and pending approvals.
- **Data:** `NodeEventService.Subscribe` with topics NODE, QUEUE, RESOURCES (5 s), FINDINGS, APPROVALS, ACCOUNT and NOTIFICATIONS, plus page-specific topics while a page is open.

---

## D-00 First run

- **Purpose.** Introduce the node, show its enforcement capability, and optionally sign in, integrate AI clients and run a demonstration task.
- **Permissions.** HUMAN.
- **Layout.** A five-step wizard: Welcome → Capabilities → Account (optional) → AI clients (optional) → Try it.

```
┌ Welcome to ArcForges ───────────────────────────────── Step 2 of 5 ┐
│ This machine: Windows 11 · 16 logical CPUs · 32 GiB               │
│ Reserved for you: 2.6 cores, 5.2 GiB (change later in Policy)      │
│ Enforcement:  CPU ✔ shares and cap   Memory ✔ commit limit         │
│               Pause ✖ not supported on Windows (why?)              │
│ WSL: Debian ✔ guest node linked                                    │
│                                    [Back]  [Skip setup]  [Next]  │
└────────────────────────────────────────────────────────────────────┘
```

- **Data:** `NodeService.GetCapabilities`, `ResourceService.GetResourceSnapshot`, `ResourceService.ListGuestLinks`, `IntegrationService.ListClients`, `AccountService.GetAccountStatus`.
- **Actions:**
  - Account step → **Sign in** (`AccountService.BeginSignIn`) or Skip.
  - AI clients step → **Plan** (`IntegrationService.PlanIntegration`), which shows the diff, then **Apply** (`ApplyIntegration`; the user must review the diff first).
  - Try it → **Run demo**: `TaskService.SubmitTask` with a bundled CPU and memory load (`arcforges node self-test --demo`) that shows queueing and limits.
- **States:** S-LOADING. If an enforcement value is degraded, the reason and its remedy are shown (e.g. "systemd user manager not available in this distribution").
- **Accessibility.** The wizard announces "Step n of 5" and the step title. Enter activates Next, and Escape asks to skip setup.

## D-01 Overview

- **Purpose.** At-a-glance health: what is running and waiting, budgets, and what needs attention.
- **Permissions.** HUMAN.

```
┌ Overview ─────────────────────────────────────────────────────────────────┐
│ Running 6   Queued 4   Paused 0   Failed (24 h) 2        [Run task  Ctrl+N] │
├──────────────── Budget ────────────────┬──── Needs attention ─────────────┤
│ CPU   ████████████░░░░  9.1 / 12.4 cores│ ⚠ STALL  dotnet test (12 min idle)│
│ Mem   ██████░░░░░░░░░░  7.2 / 21.4 GiB  │ ⓘ REPEATED_WORK cargo build ×3    │
│ Reserve 5.2 GiB · Pressure: Normal      │ ① Approval: cancel task (agent)   │
│ Disk  D: 412 GiB free · level Normal    │                                   │
├──────────────── Running ───────────────┴───────────────────────────────────┤
│ Task                     Owner          Pool     CPU   Mem    Elapsed  Cat. │
│ dotnet build Arc.sln     Claude Code·a1 agents   3.8   2.1G   04:12    BUILD│
│ cargo test               Codex·7f       agents   2.0   0.9G   01:03    TEST │
├──────────────── Sessions ──────────────────────────────────────────────────┤
│ Claude Code a1  ACTIVE  managed 14  bypassed 1   coverage: hooks+MCP        │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** subscription topics TASKS (running and queued summaries), QUEUE, RESOURCES (including each managed volume's free space and `DiskPressureLevel`), FINDINGS (open), APPROVALS (pending) and SESSIONS (active); `QueueService.GetQueue` for the initial view.
- **Actions:**
  - **Run task** opens the Run dialog (§D-02).
  - A row opens D-03.
  - An attention item opens its finding or approval.
  - The context menu on a running row: Cancel (confirmation), Priority.
- **States:** S-EMPTY ("Nothing running. Tasks you or your AI agents submit appear here.") and the standard states.
- **Accessibility.** The tables are grids with row headers. The attention list is a polite live region, and the budget gauges have text equivalents.

## D-02 Tasks

- **Purpose.** Find, filter and act on tasks.
- **Permissions.** HUMAN.

```
┌ Tasks ─ [Search title or command ] [State ▾] [Session ▾] [Workspace ▾] [Pool ▾] ┐
│ ☐ State     Title                    Owner        Pool    Started   Dur.  Exit  │
│ ☐ RUNNING   dotnet build Arc.sln     Claude·a1    agents  10:02     04:12   –   │
│ ☐ FAILED    npm test                 CLI          default 09:41     01:10   1   │
│ ☐ QUEUED    cargo build --release    Codex·7f     agents  –         –       –   │
│ [Cancel selected] [Retry selected] [Pin]                     Page 1 of 7  ◀ ▶  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `TaskService.ListTasks` (filter, page), plus the TASKS topic for live rows.
- **Actions:**
  - Row → D-03.
  - **Cancel selected** (`CancelTask` per task). The confirmation lists the tasks and owners. For other owners' tasks the dialog says "Tasks owned by agent sessions are cancelled now. Agents see the result as CANCELLED."
  - **Retry selected** (`RetryTask`). Side-effecting or unknown tasks show the warning "This command may have external effects. Retrying runs it again."
  - **Pin** (`PinTask`).
- **Run dialog** (`Ctrl+N`):
  - fields: command (argv or shell toggle), working directory (picker), pool, priority, timeout, labels, and an advanced section:
    - environment, stdin file, readiness for services;
    - **concurrency**: workspace access (adapter default, shared, exclusive) and extra exclusive or shared keys, with the adapter's keys shown read-only ([03](../architecture/03-resource-control.md) §4);
    - **retry safety**: unknown (default), idempotent or pure. Choosing one records the user's assertion (`side_effect_source=CALLER`); the adapter's suggestion is shown beside it (AD-0006 §4);
    - **placement**: local, a peer or any; inputs and declared outputs; output conflict (stage (default), skip existing, fail, overwrite) ([09](../architecture/09-lan.md) §6);
  - **Run** = `SubmitTask` then open D-03 attached.
- **States:** S-EMPTY, S-FAILED. Bulk actions report per-item results.
- **Accessibility.** Checkboxes have the label "Select <title>". `Space` toggles a row and `Ctrl+A` selects all visible rows.

## D-03 Task detail

- **Purpose.** Everything about one task: live output, timeline, resources, processes, attempts, findings and actions.
- **Permissions.** HUMAN. An agent-owned task shows "Owned by Claude Code session a1 (agent)".

```
┌ dotnet build Arc.sln ── RUNNING · attempt 1 · agents · NORMAL ────────────────┐
│ [Cancel] [Pause ⓘ unsupported] [Priority ▾] [Pin] [Retry] [Export] [⋯]          │
├─ Summary ──────────┬─ Output (merged ▾) ─────────────────────── [Follow ✔] ────┤
│ Command  dotnet b… │ Restore complete (2.1 s)                                   │
│ Dir  C:\src\arc    │   Arc.Core -> C:\src\arc\bin\Debug\Arc.Core.dll            │
│ Owner  Claude·a1   │ ...                                                        │
│ Grant  4.0 cores   │                                                            │
│        2.0 GiB exp │                                                            │
│ Tool   dotnet.build│                                                            │
│ -m:4 (tool flag)   │                                                            │
│ Keys dotnet (excl) │                                                            │
│ Retry  UNKNOWN     │                                                            │
│  (adapter: IDEMP.) │                                                            │
├─ Timeline ─────────┴────────────────────────────────────────────────────────────┤
│ QUEUED_ADMISSION ▏RESTORE ██ ▏BUILD ████████████ ▏NETWORK_WAIT (inferred) ░      │
├─ Resources ─ CPU ╱╲╱╲  Mem ▁▂▄▆  (table view)  ─ Processes (12) ─ Attempts (1) ─┤
│ Findings: none                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:**
  - `TaskService.GetTask(FULL)` and `GetTimeline`; the summary shows the effective keys (exclusive and shared), and the retry-safety class with its source and the adapter's suggestion;
  - `AttachTask` (output and state while the page is open; it never sends stdin unless **Send input** is enabled for STREAM tasks);
  - `ResourceService.GetSamples(ATTEMPT)` and `ListAttempts`;
  - `DiagnosisService.ListFindings(subject = task)`.
- **Actions:**

| Action | RPC | Rules |
|---|---|---|
| Cancel | `CancelTask` | Confirmation "Cancel <title>? The process tree receives a stop signal, then is terminated after 10 s." |
| Pause / Resume | `PauseTask` / `ResumeTask` | Shown disabled on Windows with the reason |
| Priority | `SetTaskPriority` | — |
| Retry | `RetryTask` | Shows the AD-0006 class warning |
| Pin | `PinTask` | — |
| Export | `DiagnosisService.ExportRecords(task_ids)` | — |
| Purge records | `PurgeTaskRecord` | Typed confirmation of the task title |
| Copy command | — | Copies the redacted command |

- **States:** S-LOADING, plus:
  - "Output purged by retention" (with the date);
  - "Remote attempt on <peer>" (output streamed from the peer);
  - `TERMINATION_INCOMPLETE` banner with remaining PIDs and **Terminate** (approval for other owners);
  - **Output limit**: "Output passed 2 GiB. The task was stopped (`OUTPUT_LIMIT`)", or with `disk_limit_action=NOTIFY` "Output passed 2 GiB. It is kept, and a finding was raised";
  - **Disk limit**: "Stopped: temporary files passed 20 GiB", or "Stopped: drive D: critically low" (`DISK_LIMIT`), with a link to D-11. A stop made while the node was down adds "Stopped by the attempt guard while ArcForges was not running" (`limit_enforced_by=GUARD`), and an attempt that ran unguarded shows "Disk limits were not checked for part of this run" (`guard_lost`);
  - **Compiler-cache endpoint taken** (`ENDPOINT_TAKEN`): "Stopped: another program was listening on this task's compiler-cache address, so its compiles could have reached it." with a link to the toolchain page;
  - **Outputs staged** (`OUTPUT_CONFLICT`): "2 returned files changed locally since submission and were staged." **Compare**, **Keep local**, **Take remote** (`out/…/conflicts/`);
  - **Handed off**: "The agent's command reached its client timeout at 10:44. The task continues; the agent was told to wait with `arcforges tasks wait`." ([08](../architecture/08-ai-integration.md) §4.1).
- **Accessibility.**
  - Output is a read-only text area with a find box (`Ctrl+F`) and a polite live region throttled to one announcement per 5 s ("12 new lines").
  - The timeline has an accessible table alternative.

## D-04 Queue and pools

- **Purpose.** See admission order and why tasks wait; manage pools and parallelism.
- **Permissions.** HUMAN (pool changes create policy revisions).

```
┌ Queue ─ Budget: CPU 12.4 cores (limit 18.6 with overcommit) · Mem 21.4 GiB ──────┐
│ Pools      Weight Max parallel   Running Queued  State   [New pool] [Pause all] │
│ interactive  4    AUTO (12)      0       0       ▶                               │
│ default      2    AUTO (12)      2       1       ▶                               │
│ agents       1    FIXED 4        4       3       ⏸ Paused  [Resume]              │
│ background   1    AUTO (12)      0       0       ▶                               │
├ Waiting (admission order) ───────────────────────────────────────────────────────┤
│ #1 cargo build --release  agents  needs 6.0 GiB, 3.4 GiB free → budget_memory    │
│    ETA ~3 min · ages to HIGH at 10:24 · [Explain] [Priority ▾]                    │
│    Reservation: holds memory for this task · lapses 10:52                        │
│ #2 npm ci  default  exclusive_key ws:web/app:deps (held by npm install)          │
│ #3 link-all  agents  needs 40 GiB > managed share 26 GiB → exceeds_capacity      │
│    Cannot start on this machine. [Explain] [Cancel]                              │
│ Parallelism: [Global: AUTO ▾]  Disable parallel execution for: [scope ▾] [Apply] │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `QueueService.GetQueue`, `ListPools`; topic QUEUE.
- **Actions:**
  - Pool create, update and delete (`CreatePool`, `UpdatePool`, `DeletePool`).
  - Pause and resume (`PausePool`, `ResumePool`).
  - **Explain** (`ExplainTask`) opens a side panel with the AdmissionExplanation text and numbers: the feasibility class (feasible, exceeds budget, exceeds capacity), the blocking keys and their holders, and the large-task reservation if one applies ([03](../architecture/03-resource-control.md) §4).
  - **Blocking reasons** are shown by name: `budget_memory`, `budget_cpu`, `exclusive_key`, `disk_space`, `exceeds_capacity` and the others of `QueueInfo`. An `exceeds_capacity` task also raises `TASK_INFEASIBLE`.
  - **Parallelism** (`SetParallelism`). Choosing DISABLED shows "Tasks in <scope> will run one at a time."
- **States:** S-EMPTY ("No waiting tasks"), S-DENIED for read-only policy (managed by a script), revision conflict ("Policy changed elsewhere. Review and apply again.").
- **Accessibility.** The waiting list is ordered, with position announced, and the Explain panel is a dialog with focus trapping.

## D-05 Resources

- **Purpose.** Capacity, reservations, unmanaged load, budgets, pressure, process classification, guests and adoption.
- **Permissions.** HUMAN (adoption is HUMAN only).

```
┌ Resources ─ Capacity 16.0 cores · 32.0 GiB ──────────── Pressure: Normal ───────┐
│ CPU  [reserve 2.6][unmanaged 3.1][managed 9.1][free 1.2]                          │
│ Mem  [reserve 5.2][unmanaged 8.7][managed 7.2][guest other 1.0][free 9.9]         │
│ Enforcement: CPU shares+cap ✔  Memory commit ✔  PIDs –  I/O observe  Pause ✖     │
├ Processes [Managed ▾ Escaped Bypassed Unmanaged Guest VM Shared] [Top 50 ▾] ──────┤
│ PID   Image          Label      CPU   Mem    Task / Session        Actions       │
│ 9921  cl.exe         MANAGED    1.0   0.3G   dotnet build · a1                  │
│ 7720  node.exe       BYPASSED   2.2   1.1G   session Codex·7f      [Terminate]  │
│ 5512  vmmemWSL       GUEST_VM   1.5   4.0G   Debian (linked)                    │
│ 1200  Code.exe       UNMANAGED  0.4   0.8G   –                     [Adopt]      │
├ WSL guests ─ Debian: LINKED · CPU 3.1 cores · Mem 6.0 GiB · lease 10:46 ────────┤
│ Standalone if the link is lost: 3.1 cores · 5.4 GiB (≤ allocation; ≤ 25% budget) │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `ResourceService.GetResourceSnapshot`, `WatchResources` (5 s), `ListProcesses(filter)`, `ListGuestLinks`; topics RESOURCES and GUESTS.
- **Actions:**
  - **Adopt** (`AdoptProcess`): confirmation "Place <image> (PID) and its children under ArcForges control in pool default?"
  - **Terminate** (`TerminateProcess`): confirmation naming the process and its classification. Only for MANAGED, ESCAPED, BYPASSED and leftover processes.
  - **Guest link** enable, disable and re-link (`SetGuestLink`).
- **Memory guarantees.** An info panel states what holds on this platform ([03](../architecture/03-resource-control.md) §5.4): admission keeps accounted memory within the budget; Linux enforces hard per-attempt and root limits; Windows bounds commit only; the pressure response defends the reserve but cannot guarantee it.
- **WSL guests.** Each linked guest shows its current acknowledged allocation, the lease end and the standalone allocation, which is never larger than the acknowledged allocation. A lost link shows `GUEST_LINK_LOST`, the allocation still reserved for the guest, and the two ways to release it: restore the link, or stop the distribution ([03](../architecture/03-resource-control.md) §6).
- **States:** S-EMPTY for a filter; "Observation only" banner when the capability is OBSERVE_ONLY, with the reason.
- **Accessibility.** The stacked bars have text and table equivalents, and the process table is sortable by keyboard (`Enter` on a column header).

## D-06 Sessions

- **Purpose.** AI client sessions, their coverage and routing.
- **Permissions.** HUMAN.

```
┌ Sessions ─ [Active ▾] [Client ▾] ───────────────────────────────────────────────┐
│ Client       Session  State   Workspace  Managed  Share  Routes          Started │
│ Claude Code  a1c4…    ACTIVE  arc        14       92%    hooks rewrite   09:12   │
│ Codex        7f02…    IDLE    web        3        40%    MCP only        08:55   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `SessionService.ListSessions`; topic SESSIONS.
- **Actions:** Row → D-07. **End session** (`EndSession`), with the confirmation "Services started by this session will stop."
- **States:** S-EMPTY ("No AI sessions seen. Set up integrations on the Integrations page."). The coverage column says "unknown" when no hooks were seen. **Share** is the managed share of the session's process CPU time ([08](../architecture/08-ai-integration.md) §5). "MCP only" means no command is routed unless the agent calls the `run` tool.

## D-07 Session detail

- **Purpose.** What a session ran through ArcForges, what it ran around ArcForges, and what cannot be known.
- **Permissions.** HUMAN.

```
┌ Claude Code session a1c4… ── ACTIVE · started 09:12 · cwd C:\src\arc ────────────┐
│ Coverage (observed facts, not completeness):                                     │
│  MCP connected ✔   Hooks seen: SessionStart 1, PreToolUse 52, PostToolUse 51     │
│  Routing: rewrite (heavy) ✔ (probe PASS windows/git-bash)  Route failures: 0     │
│  Managed share 92% · hand-offs 1 · joined resubmissions 1                        │
│  Managed 14 tasks · 38 CPU-min      Bypassed 1 command · 1.2 CPU-min             │
│  Unknown: subagent attribution of MCP work; model state (never available)        │
├ Tasks ─────────────────────────────────── ┬ Client events ───────────────────────┤
│ dotnet build ✔ 04:12   cargo test ✖ …      │ 09:12 SessionStart  09:40 Subagent… │
└───────────────────────────────────────────┴──────────────────────────────────────┘
```

- **Data:** `SessionService.GetSession`, `GetSessionCoverage`; `TaskService.ListTasks(session)`; `DiagnosisService.GetReport(SESSION)`.
- **Actions:** **Session report** (opens the report view); **What this release manages** (opens the release coverage statement on D-14); **End session**.
- **Accessibility.** The coverage list is structured with headings, and the "Unknown" items read as a list.

## D-08 Findings

- **Purpose.** Evidence-based problems and their remedies.
- **Permissions.** HUMAN.

```
┌ Findings ─ [Open ▾] [Severity ▾] [Kind ▾] ──────────────────────────────────────┐
│ ⚠ STALL       dotnet test (task 81f2)  idle 12 min  first 10:31  ×1              │
│ ⓘ PER_TASK_RESTORE  3 tasks restored into private NUGET_PACKAGES (1.4 GiB)       │
├ Detail ──────────────────────────────────────────────────────────────────────────┤
│ No CPU, I/O, output or process change for 12 min (threshold 10 min for dotnet    │
│ test). Evidence: cpu 0 m, io 0 B/s, last output 10:31:07.                        │
│ Actions: [Collect tree snapshot ✔ done] [Cancel task — approval] [Retry]  [Mute] │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `DiagnosisService.ListFindings`, `GetFinding`; topic FINDINGS.
- **Actions:** Acknowledge (`AcknowledgeFinding`), Mute (`MuteFinding`, with a duration picker), Remedy actions (`ApplyRemedy`), each confirmed with its risk.
- **States:** S-EMPTY ("No open findings"). An approval chip appears when a remedy needs approval.

## D-09 Approvals

- **Purpose.** Decide pending approvals, mostly requested by agents.
- **Permissions.** HUMAN only. Agents cannot approve.

```
┌ Approvals ─ Pending (1) · History ───────────────────────────────────────────────┐
│ Codex·7f asks: Cancel task "npm test" owned by CLI (medium risk)  expires 22 h   │
│ Details: task 4c1e…, reason "stale after rebase"                                 │
│                                              [Deny] [Approve and run]            │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `ApprovalService.ListApprovals`; topic APPROVALS.
- **Actions:** Approve or Deny (`DecideApproval`) with an optional comment. Approve executes the captured request, and the outcome appears in History.
- **States:** S-EMPTY; S-EXPIRED for items that expired while open.
- **Accessibility.** Each approval is a group labelled "<requester> asks: <summary>". The buttons are in the order Deny, Approve.

## D-10 Workspaces

- **Purpose.** Registered repositories and node-managed worktrees.
- **Permissions.** HUMAN.

```
┌ Workspaces ─ [Register folder…] ────────────────────────────────────────────────┐
│ arc   C:\src\arc   git main · clean · routing: inherit (OBSERVE)  [Worktrees ▾] │
│       concurrency: adapter keys · running 2  [Concurrency ▾]                     │
│   └ af/a1/fix-tests  work\3f2a…  ACTIVE · dirty (2 files) · session a1  [Remove] │
│ web   C:\src\web   git main · 3 ahead                                            │
│ Archives: af/a1/old-spike  archived 10-02 · verified · 37 files  [Restore]       │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `WorkspaceService.ListWorkspaces`, `GetWorkspace`; topic WORKSPACES.
- **Actions:**
  - Register (`RegisterWorkspace`) and unregister (`UnregisterWorkspace`, "Files are not touched").
  - Create worktree (`CreateWorktree`; dialog: branch, base ref, name).
  - Remove (`RemoveWorktree`). A clean worktree is removed at once. A dirty worktree offers **Archive changes, then remove** ([06](../architecture/06-storage-workspaces.md) §3), which needs approval when requested by an agent:
    - the dialog lists staged, unstaged and untracked files, binaries included;
    - ignored files that are not regenerable output (for example `.env`) are listed (`PlanWorktreeRemoval`) with the choice **Include in the archive** or **Confirm they may be lost**. Without a choice nothing is removed. Included files stay in a plain side archive for 90 days;
    - unmerged entries or submodules with their own changes are shown as blocking, and the remove action stays disabled;
    - progress shows the snapshot, the bundle and the verification. A failed verification keeps the worktree and raises a finding.
  - **Archives** (`ListWorktreeArchives`): branch, date, file count, verification time and expiry (90 days). **Restore** (`RestoreWorktree`) recreates the worktree with the staged and unstaged states.
  - Routing override and **concurrency mode** (`UpdateWorkspaceSettings`): adapter keys (default), serial (one managed task at a time) or shared (only keys callers supply), with the explanation of each.
- **States:** S-EMPTY. Worktree creation shows job progress.

## D-11 Storage

- **Purpose.** Disk usage, analysis, safe cleanup and quarantine.
- **Permissions.** HUMAN. "Add external path" is HUMAN only, with a second confirmation.

```
┌ Storage ─ data root D:\ArcForges\data (Dev Drive) · free 412 GiB ───────────────┐
│ Roots: work 38 GiB/100 · cache 61 GiB · logs 2.1/5 · tmp 0.4/20  [Relocate…]    │
│ Volumes: D: Normal · C: Low (3.1 GiB free) — new writers on C: wait             │
│ [Analyze]  Last analysis 10:02 · reclaimable (low risk) 23.4 GiB                 │
├ Cleanup plan (expires 10:58) ────────────────────────────────────────────────────┤
│ ☑ REGENERABLE_OUTPUT  C:\src\arc\obj         4.2 GiB  low    quarantine          │
│ ☑ PER_TASK_RESTORE    D:\…\tmp\pkgs-81f2     1.4 GiB  low    quarantine          │
│ ☐ ABANDONED_WORKTREE  af/a1/old-spike        2.0 GiB  medium git worktree remove │
│ [Add external path…]              Selected 5.6 GiB   [Execute cleanup]           │
├ Quarantine (purged after 24 h) ─ 3 items · 3.1 GiB  [Restore]                    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `StorageService.GetStorageSummary`, `GetStorageAnalysis`, `GetCleanupPlan`, `ListQuarantine`; topics STORAGE and JOBS.
- **Actions:**
  - Analyze (`AnalyzeStorage`) and Plan (`PlanCleanup`).
  - **Execute cleanup** (`ExecuteCleanup` with the digest). Confirmation: "Move 5.6 GiB into quarantine and remove 1 worktree. Quarantined items can be restored for 24 hours."
  - Restore (`RestoreQuarantine`).
  - Relocate (`UpdateRoot`), as a wizard with a free-space check.
- **Limits.** Each quota and limit names its kind: admission threshold, monitored limit (with its interval), tool-enforced or report-only ([06](../architecture/06-storage-workspaces.md) §5). Nothing claims file-system enforcement.
- **Disk levels.** Each volume shows `NORMAL`, `LOW` or `CRITICAL` with the free space and the thresholds. `LOW` explains that new attempts writing there wait (`disk_space`); `CRITICAL` lists the attempts that were frozen or stopped (`DISK_LIMIT`) and, if the store's volume is affected, the node's `DEGRADED` state.
- **States:**
  - S-EXPIRED (plan expired: re-plan);
  - PARTIAL results with per-item outcomes (IN_USE, CHANGED and others);
  - truncated analysis with its reason.
- **Accessibility.** Item checkboxes are labelled with the class and path, and the running total is announced on change.

## D-12 Caches

- **Purpose.** Cache locations, sizes, effectiveness, duplicates and sharing.
- **Permissions.** HUMAN. LAN sharing is free; it needs a paired peer whose policy allows cache access (D-15).

```
┌ Caches ─ [Report: last 7 days ▾] ───────────────────────────────────────────────┐
│ Kind            Path                  Size/Quota     Hit rate  LAN    Actions    │
│ nuget.packages  D:\…\cache\nuget\pkgs 18.2/40 GiB    94% reuse  –     [Verify]   │
│ sccache         D:\…\cache\sccache    6.1/20 GiB     71%       Shared [Settings]│
│ Duplicates: C:\Users\me\.nuget\packages 9.8 GiB (82% overlap) → [Plan cleanup]   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `CacheService.ListCaches`, `GetCacheReport`.
- **Actions:** Verify (`VerifyCache`), Settings (`UpdateCacheSettings`: quota, LAN sharing), Plan cleanup for duplicates or a trim (opens D-11 with rules).
- **States:** a "Maintenance in progress" chip while a lease is held. The LAN column and the LAN sharing setting are added with LAN cache sharing (AF-LAN-03). Until a peer is paired, the setting explains how to pair (link to D-15).

## D-13 Toolchains

- **Purpose.** See detected tools, what each adapter guarantees, and preview how a command would run.
- **Permissions.** HUMAN. Rescanning is allowed for every origin; nothing here installs tools.
- **Layout.** The toolchain table (kind, version, path, identity); the adapter manifests (each environment edit marked HONORED or BEST_EFFORT, with its source); the **Preview** box.
- **Wireframe:**

```
┌ Toolchains ─ last scan 09:12 ─────────────────────────────────────── [Rescan] ┐
│ Kind      Version   Path                                   Identity            │
│ dotnet    10.0.401  C:\Program Files\dotnet\dotnet.exe     sdk 10.0.401 x64    │
│ cargo     1.92.0    C:\Users\sam\.cargo\bin\cargo.exe      rustc 1.92.0        │
│ fastbuild —         Not installed; ArcForges never installs tools.             │
├ Adapter: dotnet ───────────────────────────────────────────────────────────────┤
│ MSBUILDDISABLENODEREUSE=1   HONORED      (A-T01, F-T01)                         │
│ NUGET_PACKAGES=<cache>      HONORED                                             │
├ Preview ───────────────────────────────────────────────────────────────────────┤
│ Command [dotnet build -c Release____]  in [C:\src\app ▾]          [Preview]    │
│ → argv, environment edits, caches bound, concurrency flags                     │
└────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `ToolchainService.ListToolchains`, `ListAdapters`; topic JOBS while a rescan runs.
- **Actions:** **Rescan** (`DetectToolchains`, a job with progress); **Preview** (`PreviewInvocation`), which shows the resolved argv, environment edits, cache bindings and concurrency flags without running anything.
- **States:** S-EMPTY ("No toolchains detected"). Missing tools show "Not installed; ArcForges never installs tools." Rescan running (progress); preview refused (unknown tool: "Runs unadapted; no cache or concurrency control").
- **Accessibility.** HONORED and BEST_EFFORT are text with an icon. The preview result is a read-only text region that follows the Preview button in focus order.

## D-14 Integrations

- **Purpose.** Connect Claude Code and Codex: MCP server, hooks, routing mode, probes and conflicts.
- **Permissions.** HUMAN only for apply and remove.

```
┌ Integrations ───────────────────────────────────────────────────────────────────┐
│ Claude Code 2.x  ✔ detected   State: CONFIGURED (user scope)  Routing: rewrite   │
│   Probe: windows/git-bash PASS · wsl:Debian PASS     [Run probe] [Remove]        │
│ Codex 0.x        ✔ detected   State: DEGRADED — hooks untrusted                  │
│   Fix: run /hooks in Codex and trust ArcForges hooks   [Re-check]                │
├ Plan (Claude Code, user scope) ──────────────────────────────────────────────────┤
│ ~/.claude/settings.json  MODIFY  + "hooks": {"PreToolUse": [...arcforges hook…]} │
│ Conflicts: none        [Cancel] [Apply exactly these changes]                    │
│ MCP alone routes nothing: shell commands are managed only by hook rewriting.     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `IntegrationService.ListClients`, `ListProbeResults`; topic INTEGRATIONS.
- **Release coverage statement.** A panel lists what this release manages, the reported gaps and the journeys that verify them (`SessionService.GetReleaseScope`; product definition §9), so the page never implies broader coverage.
- **Routing modes** (per client and workspace, [08](../architecture/08-ai-integration.md) §4.1): observe, guide, **rewrite** (heavy patterns only) and **rewrite all** (every shell command except passthrough patterns). Each mode shows what it covers and what stays unmanaged, from the coverage map ([08](../architecture/08-ai-integration.md) §4.4).
- **Copy.** Choosing MCP without hooks shows: "Connecting MCP alone routes nothing. Your agent's own shell commands run outside ArcForges unless hooks rewrite them, or the agent calls the run tool." Choosing **rewrite all** shows: "Every routed command asks for your confirmation unless you pre-approve rewritten commands (deny rules written for the original commands then no longer match)." For Codex, rewriting needs that pre-approval; otherwise Codex gets guidance. Every plan that enables an MCP or hook route shows, in the consent panel with its diff, the client's routing statement: the Stated limit text of the client's routing row of `GetReleaseScope` (`routing:claude-code` or `routing:codex`; product definition §9), verbatim ([AD-0007](../decisions/AD-0007-ai-integration.md) §4). Applying the plan records the consent (added 2026-10-19).
- **Actions:**
  - Plan (`PlanIntegration`: scope, components, routing), Apply (`ApplyIntegration` with the digest).
  - Remove (`PlanRemoval`, then Apply).
  - Run probe (`StartProbe`). This shows the instruction to paste into the client, and the result arrives by event.
  - Copy snippet (`GetInstructionSnippet`).
- **States:**
  - client not found;
  - plan expired;
  - conflict list (never auto-resolved);
  - write failure, with the restored files listed.
- **Accessibility.** The diff view is a text region with change markers announced ("added line").

## D-15 LAN

- **Purpose.** Enable LAN features, pair machines, set per-peer policy.
- **Permissions.** HUMAN only. Everything on this page is free and needs no account: pairing, status, placement and cache sharing.

```
┌ LAN ─ Listener ON :47820 · 192.168.1.99 · fingerprint 3F9A…  [Disable]          │
│ Peers                                                                            │
│ buildbox   PAIRED (pinned)  online  8 cores budget · queue 0  [Policy] [Remove]  │
│ laptop     DISCOVERED       untrusted                          [Pair]            │
├ Pairing with laptop ─────────────────────────────────────────────────────────────┤
│ Both screens must show the same number:      4 8 1 · 2 9 0                        │
│                       [They differ]   [They match]          expires in 01:42     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `PeerService.GetLanStatus`, `ListPeers`, `GetPeer`, `GetPairing`; topic PEERS (peer and pairing events).
- **Actions:**
  - Enable or disable (`SetLanEnabled`), with a firewall note on first enable.
  - Pair (`BeginPairing`).
  - Incoming request dialog (`RespondToPairing`).
  - Confirm digits (`ConfirmPairing`), Cancel (`CancelPairing`).
  - Policy editor (`UpdatePeerPolicy`): placement out and in, cache read and write, shares, toolchains, command patterns, approval, data out (source, outputs, logs). Defaults are status only.
  - Add by address (`AddPeerAddress`), Remove or Block (`RemovePeer`).
- **States:** INCOMPATIBLE peers with the required version; mismatch, expired and blocked pairing results.
- **Accessibility.** The SAS digits are read as individual digits ("four eight one, two nine zero"), and the countdown is announced at 60, 30 and 10 seconds.

## D-16 Account

- **Purpose.** Sign-in, plan, cloud link, phone pairing, sign-out.
- **Permissions.** HUMAN.

```
┌ Account ─ Signed in as Sam (s***@example.com) · Pro (renews 12 Nov) ────────────┐
│ This node: enrolled ✔  Relay: CONNECTED  Remote control: low risk only [Policy] │
│ Entitlement token valid until 26 Oct (offline grace)                            │
│ [Connect phone (QR)] [Manage subscription ↗] [Sign out]                          │
├ Connect phone ───────────────────────────────────────────────────────────────────┤
│   ▓▓▓▓ QR ▓▓▓▓   Scan with ArcForges for Android. Expires in 01:54.              │
│   Can't scan? Enter code 7KQ2-M9XD-… in the app.                                  │
│   Waiting for scan…  →  "Allow Pixel 9 to sign in as Sam?" [Deny] [Allow]        │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `AccountService.GetAccountStatus`, `GetSignInFlow`, `GetPhonePairing`; topic ACCOUNT (sign-in and phone pairing events).
- **Actions:**
  - Sign in: `BeginSignIn(BROWSER)` opens the system browser. "Use a code instead" uses DEVICE_CODE and shows the code, URL and QR.
  - Connect phone (`CreatePhonePairing`, then `ConfirmPhonePairing`).
  - Cloud link toggle (`SetCloudLink`).
  - Sign out (`SignOut`), with the confirmation "Remote access stops on this node. Local and LAN work is unaffected."
  - Manage subscription opens `arcforges.com/account/subscription`.
- **States:** not signed in; flow expired or denied; S-OFFLINE (cloud unreachable; entitlement shown with offline grace); "Weaker credential storage" warning on Linux without a secret service.

## D-17 Policy

- **Purpose.** Edit the node policy safely.
- **Permissions.** HUMAN. Changes from scripts or agents need approval.
- **Layout.** Section list: Resources, Pools, Parallelism, Permissions, Agents, Routing, Diagnosis actions, Storage and retention, Cleanup, Caches, Privacy, Remote control, Updates, LAN, Approvals. Each section is a form with defaults shown, and a **JSON view** (protobuf JSON) is available for advanced users.

```
┌ Policy ─ revision 14 · changed 09:20 by you ─ [Revisions] [Reset section] ──────┐
│ Resources                                                                        │
│  Reserved CPU: 1.0 cores + 10 %  (= 2.6 cores)      Reserved memory: 2 GiB + 10 %│
│  CPU overcommit ×1.5   Memory overcommit ×1.0 (fixed)   Max task memory 26 GiB   │
│  ☑ Allow unenforced execution when enforcement is unavailable                    │
│                                     [Validate] [Discard] [Apply revision 15]     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `PolicyService.GetPolicy`, `GetDefaultPolicy`, `ListPolicyRevisions`; topic POLICY.
- **Actions:**
  - Validate (`ValidatePolicy`), which shows issues inline by path.
  - Apply (`UpdatePolicy` with expected_rev; optional comment).
  - Restore revision (`RestorePolicyRevision`).
  - Explain permission (`ExplainPermission`) in the Permissions section.
- **States:** revision conflict (shows a three-way comparison and asks to re-apply); ERROR issues block Apply.
- **Accessibility.** Inline errors are linked to their fields with `aria-describedby`-equivalent automation properties.

## D-18 Updates

- **Purpose.** See the installed version and channel, update now or later, and roll back.
- **Permissions.** HUMAN. Rollback is HUMAN-only and interactive (11 §1).
- **Layout.** Current and previous version; channel and install source; the update state (SM-UPDATE); the available version with notes; the schedule; bad versions; "Managed by <package manager>" when applicable.
- **Wireframe:**

```
┌ Updates ─ 1.2.0 (stable) · installed by setup program ────────────────────────┐
│ State: AVAILABLE   1.2.1 · released 10 Oct · [Release notes ↗]                 │
│ Schedule: daily 02:00–05:00 (Policy → Updates)    Metered network: defer       │
│ [Update now]  [Postpone 1 day]  [Check now]                                    │
│ Previous version: 1.1.4                                   [Roll back…]          │
│ Bad versions (never installed): 1.2.0-beta.3                                    │
└────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `UpdateService.GetUpdateStatus`; topic UPDATES.
- **Actions:**
  - **Check now** (`CheckNow`).
  - **Update now** (`ApplyNow`), with the confirmation "The node restarts. Running tasks continue."
  - **Postpone** (`Postpone`).
  - **Roll back** (`Rollback`), with the confirmation "ArcForges returns to 1.1.4 and restarts. Running tasks continue."
  - Channel and window are edited in Policy → Updates.
- **States:** MANAGED_EXTERNALLY (read-only, naming winget, Scoop or apt); ROLLED_BACK with the reason; switching (progress, with actions disabled); S-OFFLINE for checks.
- **Accessibility.** The state is a polite live region during download and switch. Release notes open in the browser, and the link says so.

## D-19 Diagnostics and support

- **Purpose.** Doctor, reports, exports and support bundles.
- **Permissions.** HUMAN. Bundle upload needs sign-in and consent.

```
┌ Diagnostics ─ [Run doctor] ─ Overall: WARN ──────────────────────────────────────┐
│ ✔ node.store  ✔ enforcement.cpu  ⚠ guest.debian.systemd lingering off (remedy…)  │
│ Reports: [Waste ▾ last 7 days] [Capacity] [Cache] [Disk]    [Export records…]    │
├ Support bundle ──────────────────────────────────────────────────────────────────┤
│ [Create bundle]  bundle 2c… READY 3.4 MiB · 14 files · 212 redactions [Review]   │
│ Review: logs/node-1.jsonl (redacted) … [Upload to case ▾] (consent required)     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data and actions:**
  - `DiagnosisService.RunDoctor`, `GetReport` and `ExportRecords` (job, then **Open folder**);
  - `SupportService.CreateSupportBundle`, `GetSupportBundle`, `UploadSupportBundle` (consent checkbox "I reviewed the files listed above"), `DeleteSupportBundle`.
- **States:** S-OFFLINE for upload; rate-limited upload.

## D-20 Settings

- **Purpose.** Node configuration (`node.json`) and Desktop preferences.
- **Permissions.** HUMAN.
- **Layout.** Two groups: **Node** (data root, log level, telemetry) and **Desktop** (theme, notifications, start at sign-in, tray behaviour).
- **Wireframe:**

```
┌ Settings ──────────────────────────────────────────────────────────────────────┐
│ Node                                                                            │
│  Data root   D:\ArcForges\data                         [Relocate… → Storage]    │
│  Log level   [Information ▾]     ⓘ Restart required                             │
│  Telemetry   ☐ Send daily anonymous counters  (What is sent?)                   │
│ Desktop                                                                         │
│  Theme       (•) System ( ) Light ( ) Dark ( ) High contrast                    │
│  Notify me   ☑ Task failed ☐ Task finished ☑ Approval needed ☑ Finding ☑ Update │
│  ☑ Start ArcForges Desktop when I sign in    Close button: [Minimize to tray ▾] │
│                                                          [Discard] [Save]       │
└─────────────────────────────────────────────────────────────────────────────────┘
```

- **Fields:**
  - data root (relocation goes to D-11);
  - log level;
  - telemetry opt-in (off by default, with an explanation of the counters);
  - theme (system, light, dark, high contrast);
  - notifications (per kind: task failed or finished, approval needed, finding, update);
  - start Desktop at sign-in;
  - tray behaviour.
- **Data and actions:** `NodeService.GetNodeSettings` and `UpdateNodeSettings` (log level, telemetry), the same as `arcforges config`; the data root links to D-11 relocation. Desktop preferences (theme, notifications, start at sign-in, tray) are stored locally by the reused shell layout persistence.
- **States:** "Restart required" for data root and log level; unsaved changes (leaving the page asks to save or discard).
- **Accessibility.** Each group is a labelled region. "What is sent?" opens the counter list as a dialog. The theme applies at once and is announced.

## D-21 Notification drawer

- **Purpose.** Recent notifications with deep links.
- **Permissions.** HUMAN.
- **Layout.** A right-side drawer listing the notification centre entries, with **Mark all read**. Entries link to tasks, findings, approvals and updates.
- **Wireframe:**

```
                                   ┌ Notifications ─────────── [Mark all read] ✕ ┐
                                   │ ● npm test failed (exit 1) · 2 min ago       │
                                   │ ● Codex asks to cancel npm test · 5 min ago  │
                                   │   Update 1.2.1 available · today 08:00       │
                                   └──────────────────────────────────────────────┘
```

- **Data:** `NodeService.ListNotifications` (the latest 500 entries) and topic NOTIFICATIONS for new ones; the bell badge shows `unread_count`.
- **Actions:** open an entry (navigates to its link and calls `MarkNotificationsRead` with its ID); **Mark all read** (`MarkNotificationsRead` with `up_to` = now).
- **States:** S-EMPTY ("You're all caught up"); entry target gone (for example a purged task: "This item no longer exists").
- **Accessibility.** The drawer is a dialog; `Esc` closes it and returns focus to the bell button. Unread entries say "unread" in text.

## D-22 About

- **Purpose.** Identify the installed versions, find logs and data, and read licences.
- **Permissions.** HUMAN.
- **Layout.** Versions (Desktop, node, contract); paths (data root, log folder); licences and SBOM; **Copy diagnostics summary**.
- **Wireframe:**

```
┌ About ArcForges ────────────────────────────────────────────────────────────────┐
│ Desktop 1.2.0 · Node 1.2.0 · Contract node.v1 (1.0)                              │
│ Data root  D:\ArcForges\data                                       [Open folder] │
│ Logs       D:\ArcForges\data\logs                                  [Open folder] │
│ Third-party notices · SBOM (CycloneDX) · AGPL-3.0 licence                        │
│                                               [Copy diagnostics summary]         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `NodeService.GetNodeInfo`.
- **Actions:** **Open folder** (the OS file manager); licence and SBOM links; **Copy diagnostics summary** (versions, OS, capabilities summary and the node state; never secrets, paths under the user profile are shortened).
- **States:** node stopped (Desktop version only, with **Start node**).
- **Accessibility.** Paths are selectable text. The copy action announces "Copied".
