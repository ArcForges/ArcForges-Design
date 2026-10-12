# AD-0005 — Resource enforcement, WSL model and privileges

- Status: Accepted (2026-10-12)
- Evidence: [platform verification](../verification/platform-capabilities.md) V-W01–V-W06, V-L01–V-L07, L-01–L-13

## Decision

### Process model

The node runs **as the signed-in user, without elevation**. It launches managed processes as that user and never elevates them. Core features need no administrator or root rights. Two optional privileged features exist, each only after an explicit OS-level installation prompt: a machine-wide Windows service mode for headless build machines, and Linux I/O control. They are never required for development-stage acceptance.

### Windows

1. At startup the node creates (or re-opens) a named **root job** `Local\ArcForges.<node_id>.root` with:
   - a hard CPU cap = `(capacity − reserved headroom) / capacity × 10000`, updated when policy or unmanaged load changes (V-W04);
   - a job commit limit = managed memory budget (V-W05);
   - a notification-limit threshold at 90% of that budget for soft-pressure signals (V-W03).
2. Each attempt runs in a **child job** `Local\ArcForges.<node_id>.<attempt_id>`, nested in the root job (V-W01). Its limits:
   - weight-based CPU rate control (weight 1–9 mapped from priority class and grant);
   - a per-job commit limit (the attempt's memory ceiling);
   - `ActiveProcessLimit` when policy sets one;
   - no breakaway allowed.

   `KILL_ON_JOB_CLOSE` is **not** set by default, so executions survive node restarts (AD-0006). The job is named so a restarted node re-opens it. Tasks marked `kill_with_node` get KILL_ON_JOB_CLOSE.
3. Processes are launched suspended (`CREATE_SUSPENDED`), assigned to the job, then resumed, so no child escapes before assignment.
4. **Termination.**
   - Cancellation sends `CTRL_BREAK_EVENT` to the attempt's console process group (each attempt gets a new process group and a hidden console).
   - After the grace period, `TerminateJobObject`.
   - An ancestry scan finds processes that escaped (WMI-created, broker-launched) and reports them as `ESCAPED` (R-RES-012). It terminates them only if they are same-user descendants by ancestry and policy permits.
5. Windows has no `memory.high` equivalent and no supported job-wide freeze, so the node reports `pause=UNSUPPORTED` on Windows. Commit-limit exhaustion fails allocations, and the node records `memory_limit_hit` from the guaranteed notification limit.

### Linux (including WSL2 guests)

1. **Node unit.** The node runs as the systemd **user** unit `arcforges-node.service`. It does not hold executions in its own cgroup.
   - **Why:** systemd kills the processes left in a unit's cgroup when the unit stops or restarts after a failure.
   - **Effect:** a node crash, update or `systemctl --user restart` never touches running executions (AD-0006 §2).
2. **Execution containers are transient systemd user units, created through the user manager's D-Bus API** (`org.freedesktop.systemd1.Manager.StartTransientUnit`, with the AOT-compatible `Tmds.DBus.Protocol`).
   - **Slice.** The root container is the slice `arcforges.slice`, installed as a unit file beside the node unit. At runtime the node sets these properties with `SetUnitProperties(runtime=true)`:
     - `CPUQuota` (= `cpu.max`), which protects the reserved headroom;
     - `MemoryHigh` and `MemoryMax`, which hold the managed memory budget;
     - `TasksMax`.
   - **Attempts.** Each attempt is a transient service `arcforges-a-<attempt_id>.service` in that slice, with:
     - `CPUWeight` from priority and grant, plus an optional per-task `CPUQuota`;
     - `MemoryHigh` = estimate × 1.25, `MemoryMax` = ceiling, `OOMPolicy=kill` (the whole unit stops when an OOM kill occurs) and optional `MemorySwapMax`;
     - `TasksMax` (default 4096);
     - `KillMode=control-group` with `TimeoutStopSec` = the task's cancellation grace;
     - `ExecStopPost=<app>/arcforges node exit-record --attempt <id>`;
     - `CollectMode=inactive-or-failed`.
   - **Launch details:**
     - The node passes the working directory and an exact environment: `Environment=` plus `UnsetEnvironment=` for every manager variable outside the resolved set.
     - stdio arrives as file descriptors passed over D-Bus (`StandardInputFileDescriptor`, `StandardOutputFileDescriptor`, `StandardErrorFileDescriptor`, opened by the node on its own log files and stdin pipe).
     - The caller's relevant rlimits are passed as `Limit*=` properties.
   - **Parent and exit status.**
     - The user manager is the parent of every execution, so executions never depend on the node process.
     - `ExecStopPost` receives `$EXIT_CODE`, `$EXIT_STATUS` and `$SERVICE_RESULT` and writes `logs/<attempt>/exit.json`. The exit status is therefore durable even while the node is down.
     - Local evidence: L-13.
   - **Control:**
     - Pause uses `FreezeUnit` and `ThawUnit`.
     - Graceful cancellation is `KillUnit(main, SIGINT|SIGTERM)` followed by `StopUnit`, whose `KillMode=control-group` kills the rest after the grace period. Forced cancellation is `KillUnit(all, SIGKILL)`.
     - Limit changes use `SetUnitProperties(runtime=true)`.
     - Statistics are read directly from the unit's cgroup files (`ControlGroup` property; read-only access), and completion is observed through D-Bus `PropertiesChanged`/`JobRemoved` signals plus `exit.json` (V-L03–V-L05).
3. **Minimum platform.** cgroup v2 unified hierarchy and systemd ≥ 247 with a user manager. Older or absent managers degrade per capability (§4 and [resource control](../architecture/03-resource-control.md) §8).
4. **Without a user manager or controllers.** If no systemd user manager exists, or a controller is missing in the user manager's delegation, the node runs in `OBSERVE_ONLY` (or `PARTIAL` per missing controller).
   - Executions are then plain child processes, and their exit status is lost if the node restarts before they finish.
   - The node refuses tasks whose policy requires enforcement (R-RES-008).
   - Without lingering, a non-WSL user manager stops at logout, and with it every execution. This is documented, and `loginctl enable-linger` is offered as a user step.
5. **I/O.** `io` control is not delegated by default (L-06). I/O limits are an optional privileged feature (A-L02). Without it the node only observes I/O (`io.stat`, `io.pressure`).

### WSL2 model

1. The Windows **host node** and each managed distribution's **guest node** are separate authorities linked by a **guest link**. The host launches `wsl.exe -d <distro> --exec <guest arcforges path> bridge wsl`, a long-lived child of the host node. The bridge relays one byte stream between its stdio and the guest node's Unix socket, and the host runs gRPC over it (AD-0004).
   - This works in NAT, mirrored and consomme networking modes alike.
   - The bridge keeps the distribution alive while the host holds the link, so the user's `instanceIdleTimeout` (V-L07) needs no change.
   - The guest node itself runs under the user manager (L-08), not under the bridge. Its executions are transient units of that user manager (Linux §2).
2. **Capacity and accounting.**
   - The guest's capacity is what the VM exposes (`nproc` and MemTotal, bounded by `.wslconfig`).
   - The host counts the VM as one consumer through its VM worker process (vmmem/vmmemWSL; A-L01) and never sums guest-internal processes separately.
   - Guest-reported managed usage is attributed inside that consumer: `guest_other = max(0, vm_usage − guest_managed)`.
3. **Coordinated admission.** While linked, a guest asks the host for a grant before admitting an attempt (a `GrantRequest` on the `GuestLinkService.OpenLink` stream, answered by the host through `AnswerGrant`), so one fair queue spans the host and its guests. Unlinked, the guest admits within its own capacity minus its own reserve.
4. A Windows task that runs `wsl.exe` is flagged `crosses_vm_boundary`. Its Linux processes are outside the Windows job and are labelled unmanaged unless submitted to the guest node (R-RES-011).

### Observation versus control

- **Observation:** the node samples every visible process (Windows: process snapshots plus per-process times and memory; Linux: `/proc` plus cgroup statistics).
- **Control:** applies only to processes the node launched or that the user explicitly adopted (same user; recorded; R-RES-013).
- **Bypass attribution:** heavy unmanaged processes are attributed to an agent session only through process ancestry from a registered agent process (AD-0007).

## Consequences

- No step of core functionality needs elevation, and every enforcement claim is backed by a real test in its environment.
- Windows pause and memory soft-limits are honestly unavailable.
- Optional privileged features are designed but do not gate development-stage completion.
