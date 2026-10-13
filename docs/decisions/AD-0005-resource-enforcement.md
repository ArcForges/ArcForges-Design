# AD-0005 — Resource enforcement, WSL model and privileges

- Status: Accepted (2026-10-12; revised after the independent review the same day: job handle holders, guest budgets, aligned parameters; revised 2026-10-13 after the findings review: verified console signalling, guest allocation split and lease, stated memory guarantees; revised 2026-10-13 after the mechanism review: the guest's reservation kept during link loss, holders as disk guards, compiler servers per attempt)
- Evidence: [platform verification](../verification/platform-capabilities.md) V-W01–V-W06, V-L01–V-L07, L-01–L-16, L-18

The numeric limits and formulas live in [resource control](../architecture/03-resource-control.md) §2 and §5. The launch, cancellation and recovery sequences live in [execution](../architecture/04-execution.md) §3, §6 and §9. This decision fixes the mechanisms.

## Decision

### Process model

The node runs **as the signed-in user, without elevation**. It launches managed processes as that user and never elevates them. Core features need no administrator or root rights.

Optional privileged features are designed but not part of the current deliverables: a machine-wide Windows service mode (a separate per-machine installer, AR-16), and Linux I/O control. They are never required for development-stage acceptance.

### Windows

1. **Root job.** At startup the node creates (or re-opens) a named root job `Local\ArcForges.<node_id>.root`, with:
   - a hard CPU cap;
   - a job commit limit;
   - a notification limit for soft-pressure signals.

   Values per 03 §5 (V-W03–V-W05). They are updated with hysteresis when budgets change.
2. **Attempt jobs.** Each attempt runs in a child job `Local\ArcForges.<node_id>.<attempt_id>`, nested in the root job (V-W01). Its limits follow 03 §5:
   - weight-based CPU rate control, or a hard cap when a per-task cap is set;
   - a per-job commit limit;
   - `ActiveProcessLimit` when policy sets one;
   - no breakaway allowed.
3. **Handle holders keep jobs alive across node restarts.** A named job disappears from the namespace as soon as its last handle closes, even while processes still run inside it (L-14). So every attempt has a holder: the launcher role `arcforges node exec-wrap`.
   - **Where it runs.** The holder runs *outside* the job (it is not assigned to it). It inherits handles to the child job, the root job and the output files.
   - **What it does.** It creates the target process suspended, assigns it to the **root job first and then to the child job**, resumes it and waits for it. Assigning a process that is already in the root job to the child job is what nests the child under the root (V-W01); assigning it to the child alone would leave the child a top-level job outside the root caps. Where available, `PROC_THREAD_ATTRIBUTE_JOB_LIST` with `[root, child]` does the same at creation. No ArcForges job sets UI restrictions, because those prevent nesting. F-W01 verifies the resulting hierarchy.
   - **Exit record.** It writes the durable exit record with job accounting ([04](../architecture/04-execution.md) §3).
   - **Disk guard.** While the node's heartbeat is stale, it enforces the attempt's output, temporary-space and low-space limits, because it holds the job handles and the output files ([06](../architecture/06-storage-workspaces.md) §5).
   - **Lifetime.** It keeps both job handles until the node acknowledges the record, through the named event `Local\ArcForges.<node_id>.<attempt_id>.ack`.

   While any holder lives, `OpenJobObject` by name succeeds, so a restarted node re-opens the attempt and root jobs, re-reads accounting and cancels or limits them as before.
4. **Completion ports.** A job accepts one completion port. A restarted node first clears the old association, then attaches its own (L-15). It then queries `JobObjectLimitViolationInformation` and the basic accounting, to catch limit events it missed while down.
5. **Kill with node.** Tasks marked `kill_with_node` are launched by the node itself, without a holder, in a job with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. The node's handle is then the only one, so the job is killed when the node exits. Their exit status is captured only while the node runs.
6. **Launch order.** Processes are created suspended (`CREATE_SUSPENDED`), assigned to the job, then resumed, so no child escapes before assignment.
7. **Termination.**
   - **Graceful:** cancellation sends `CTRL_BREAK_EVENT` to the attempt's console process group. The root process starts with `CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP`: a windowless console and its own group. The `arcforges node signal` helper frees its own console, attaches to the root process's console and signals the group; this works on Windows 11 (L-18). Descendants with their own console, GUI processes and failed attaches fall back to `WM_CLOSE` and the forced phase ([04](../architecture/04-execution.md) §6).
   - **Forced:** after the grace period, `TerminateJobObject`.
   - **Escaped processes:** an ancestry scan finds processes that escaped (WMI-created, broker-launched) and reports them as `ESCAPED` (R-RES-012). It terminates them only if they are same-user descendants by ancestry and policy permits.
8. **No pause or soft limit.** Windows has no `memory.high` equivalent and no supported job-wide freeze, so the node reports `pause=UNSUPPORTED` on Windows. Commit-limit exhaustion fails allocations, and the node records `memory_limit_hit` from the notification limit and limit-violation queries.

### Linux (including WSL2 guests)

1. **Node unit.** The node runs as the systemd **user** unit `arcforges-node.service`, and holds no executions in its own cgroup. systemd kills the processes left in a unit's cgroup when the unit stops or restarts after a failure; keeping executions elsewhere means a node crash, update or `systemctl --user restart` never touches them (AD-0006 §2).
2. **Execution containers are transient systemd user units**, created through the user manager's D-Bus API (`org.freedesktop.systemd1.Manager.StartTransientUnit`, using the AOT-compatible `Tmds.DBus.Protocol`).
   - **Slice.** The root container is the slice `arcforges.slice`, installed as a unit file beside the node unit. The node sets its limits at runtime with `SetUnitProperties(runtime=true)`: `CPUQuota`, `MemoryHigh`, `MemoryMax` and `TasksMax` (values per 03 §5).
   - **Attempts.** Each attempt is a transient service `arcforges-a-<attempt_id>.service` in that slice, with:
     - `CPUWeight` (03 §5), plus an optional per-task `CPUQuota`;
     - `MemoryHigh`, `MemoryMax`, `OOMPolicy=kill` and an optional `MemorySwapMax`;
     - `TasksMax`;
     - `KillMode=control-group` with `TimeoutStopSec` = `leftover_grace` (default 5 s). This applies only to the stop that follows the root process's exit;
     - `ExecStopPost=<app>/current/arcforges node exit-record --attempt <id>`;
     - `CollectMode=inactive-or-failed`.
   - **Launch.**
     - The node passes the working directory and an exact environment (`Environment=`, plus `UnsetEnvironment=` for every manager variable outside the resolved set).
     - stdio is passed as file descriptors over D-Bus (`StandardInputFileDescriptor`, `StandardOutputFileDescriptor`, `StandardErrorFileDescriptor`).
     - The caller's relevant rlimits are passed as `Limit*=` properties.
   - **Parent and exit record.**
     - The user manager is the parent of every execution, so executions never depend on the node process.
     - `ExecStopPost` runs in the unit's cgroup and receives `$EXIT_CODE`, `$EXIT_STATUS` and `$SERVICE_RESULT`. It writes `logs/<attempt>/exit.json` with the cgroup accounting (`cpu.stat`, `memory.peak`, `memory.events`, `io.stat`), so the record is durable even while the node is down (L-13).
   - **Control.**
     - **Pause:** `FreezeUnit` / `ThawUnit`.
     - **Graceful cancellation:** `KillUnit("all", <stop_signal>)`, default SIGTERM.
     - **Forced cancellation:** after `cancel_grace`, `KillUnit("all", SIGKILL)`.
     - **Limit changes:** `SetUnitProperties(runtime=true)`.
     - **Statistics:** read directly from the unit's cgroup files, which are readable.
     - **Completion:** observed through D-Bus `PropertiesChanged`/`JobRemoved` and `exit.json` (V-L03–V-L05).
3. **Minimum platform.** cgroup v2 unified hierarchy and systemd ≥ 247 with a user manager. Older or absent managers degrade per capability (03 §8).
4. **Without a user manager or controllers.** If no systemd user manager exists, or a controller is missing from its delegation, the node runs in `OBSERVE_ONLY` (or `PARTIAL` per missing controller).
   - Executions are then plain child processes, and their exit status is lost if the node restarts before they finish.
   - The node refuses tasks whose policy requires enforcement (R-RES-008).
   - Without lingering, a non-WSL user manager stops at logout, and with it every execution. This is documented, and `loginctl enable-linger` is offered as a user step.
5. **I/O.** `io` control is not delegated by default (L-06). I/O limits are an optional privileged feature (A-L02). Without it the node only observes I/O (`io.stat`, `io.pressure`).

### WSL2 model

1. **Guest link.** The Windows **host node** and each managed distribution's **guest node** are separate authorities, linked by a **guest link**.
   - **Bridge.** The host launches `wsl.exe -d <distro> --exec <guest arcforges path> bridge wsl`, a long-lived child of the host node. The bridge relays one byte stream between its stdio and the guest node's Unix socket, and the host runs gRPC over it (AD-0004).
   - **Networking.** This works in NAT, mirrored and consomme networking modes alike.
   - **Distribution lifetime.** The bridge keeps the distribution alive while the host holds the link, so the user's `instanceIdleTimeout` (V-L07) needs no change. Whether the user manager stays up with only the bridge connected is verified by F-L01.
   - **Guest executions.** The guest node runs under the user manager (L-08), not under the bridge, and its executions are transient units of that user manager (Linux §2).
2. **Capacity and accounting.**
   - **Guest capacity** is what the VM exposes (`nproc` and MemTotal, bounded by `.wslconfig`).
   - **Host view:** the host counts the VM as one consumer through its VM worker process (vmmem/vmmemWSL; A-L01) and never sums guest-internal processes separately.
   - **Attribution:** guest-reported managed usage is attributed inside that consumer: `guest_other = max(0, vm_usage − guest_managed)`.
3. **Coordinated admission and enforcement** (03 §6).
   - **Admission.** While linked, a guest asks the host for a grant before admitting an attempt: a `GrantRequest` on the `GuestLinkService.OpenLink` stream, answered with `AnswerGrant`. One fair queue spans the host and its guests.
   - **Enforcement.** Demand is admitted, allocations are enforced. The host splits its enforceable CPU budget between its own root and the guest slice in proportion to demand, with positive floors on both sides, so the two always sum to `B_cpu`. Memory grants are never overcommitted. The guest's slice limits arrive by `GuestLinkService.SetGuestBudget` with a lease ([03](../architecture/03-resource-control.md) §6).
   - **Acknowledged allocations.** The guest applies each pushed allocation before answering, and the host reuses capacity the guest gives back only after that acknowledgement. A grant that raises the allocation is acknowledged before the attempt may start.
   - **Unlinked.** While the lease runs, the guest admits only within its last acknowledged allocation. After the lease lapses, it admits new attempts only within the standalone allocation, which is never larger than that acknowledged allocation (at most 25% of the host budget by default). It never lowers its slice limits below running work.
   - **The host keeps the last acknowledged allocation reserved** throughout the outage, because an idle guest can resume and use its whole allocation at any moment; measured usage never shrinks the reservation. The reservation ends only when the guest acknowledges a smaller allocation after reconnecting (having re-registered the attempts it admitted meanwhile), or when the host observes that the guest's distribution or the VM has stopped. A guest that starts in a new boot of its distribution admits nothing until it links again. Host and guest enforced allocations therefore stay within the host budget throughout. `GUEST_LINK_LOST` reports the outage and the reserved allocation (revised 2026-10-13 after the mechanism review: the earlier rule accounted the guest at the larger of its usage and the standalone allocation).
4. **Tasks that cross into WSL.** A Windows task that runs `wsl.exe` is flagged `crosses_vm_boundary`. Its Linux processes are outside the Windows job and are labelled unmanaged unless submitted to the guest node (R-RES-011).

### Observation versus control

- **Observation:** the node samples every visible process (Windows: process snapshots plus per-process times and memory; Linux: `/proc` plus cgroup statistics).
- **Control:** applies only to processes the node launched or that the user explicitly adopted (same user; recorded; R-RES-013).
- **Bypass attribution:** heavy unmanaged processes are attributed to an agent session only through process ancestry from a registered agent process (AD-0007).

## Consequences

- No step of core functionality needs elevation, and every enforcement claim is backed by a real test in its environment.
- Windows pause and memory soft-limits are honestly unavailable.
- Each Windows attempt costs one small holder process (target ≤ 3 MB private, [15](../architecture/15-performance-targets.md)). That is the price of surviving node restarts.
- Optional privileged features are designed but do not gate development-stage completion.
