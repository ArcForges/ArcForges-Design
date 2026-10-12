# 03 — Resource observation, budgets, admission and enforcement

Units: CPU in **millicores** (1,000 = one logical processor fully busy), memory in **bytes**. All defaults are policy values ([data/node-store.md](../data/node-store.md) `policy_document`, schema in `arcforges.node.v1.ResourcePolicy`).

## 1. Observation

| Signal | Windows source | Linux source | Interval |
|---|---|---|---|
| Machine CPU | `GetSystemTimes` | `/proc/stat` | 1 s internal, 5 s published |
| Machine memory | `GlobalMemoryStatusEx` (total, available, commit total/limit) | `/proc/meminfo` (MemTotal, MemAvailable, SwapTotal/Free, Committed_AS) | 1 s / 5 s |
| Pressure | n/a | `/proc/pressure/{cpu,memory,io}`; per cgroup `*.pressure` | 5 s |
| Disk | `GetDiskFreeSpaceExW` per volume of each managed root | `statvfs` | 60 s |
| Process list | `CreateToolhelp32Snapshot` (pid, ppid, exe) | `/proc/[pid]/stat` (ppid, comm, starttime) | 5 s |
| Process detail (managed trees, agent trees, top 20 CPU and memory) | `GetProcessTimes`, `GetProcessMemoryInfo` (private bytes, working set), `GetProcessIoCounters`; `PROCESS_QUERY_LIMITED_INFORMATION` | `/proc/[pid]/{stat,status,io}` | 1 s (managed), 5 s (others) |
| Managed execution totals | `QueryInformationJobObject` (`JobObjectBasicAndIoAccountingInformation`, `JobObjectBasicProcessIdList`, extended limit peak commit) | cgroup `cpu.stat`, `memory.current`, `memory.peak`, `memory.events`, `io.stat`, `pids.current`, `cgroup.events` | 1 s |
| WSL VM consumer (host only) | The VM worker process (vmmem/vmmemWSL; A-L01): CPU time and private working set | n/a | 5 s |

Process identity is `(pid, start_time)`, never pid alone. Samples are stored per execution at 1 s resolution for its lifetime and downsampled to 10 s after completion. Machine samples are kept at 5 s for 24 h, then 1 min for 30 days, then dropped (R-RES-001, R-REC-005).

## 2. Capacity, headroom and budgets

For each node (host or guest):

```
C_cpu  = logical processors × 1000                      (guest: nproc inside the VM)
C_mem  = physical memory                                (guest: MemTotal)
R_cpu  = reserve_cpu_fixed + reserve_cpu_fraction × C_cpu      default 1000 + 0.10 × C_cpu
R_mem  = reserve_mem_fixed + reserve_mem_fraction × C_mem      default 2 GiB + 0.10 × C_mem
U_cpu  = smoothed(total_cpu − managed_cpu − node_self_cpu − vm_consumer_cpu)
U_mem  = smoothed(used_mem − managed_mem − node_self_mem − vm_consumer_mem)
         where used_mem = C_mem − available_mem
B_cpu  = max(min_managed_cpu, C_cpu − R_cpu − U_cpu − guest_other_cpu)    min_managed_cpu default 1000
B_mem  = max(0, C_mem − R_mem − U_mem − guest_other_mem)
```

On the 18-thread, 31.5 GiB workstation (L-01) the defaults give `R_cpu = 2800`, `R_mem ≈ 5.15 GiB`.

**Smoothing.** Smoothing is asymmetric so the user's own load is respected quickly and released slowly. `x_t = x_{t−1} + α·(sample − x_{t−1})` with `α_up = 0.5` when the sample rises and `α_down = 0.1` when it falls, evaluated every 1 s.

**Guest terms (host only).**
- `vm_consumer_*` is the measured usage of the WSL VM.
- `guest_other_* = max(0, vm_consumer_* − Σ guest-reported managed usage)` is in-VM load that no guest manages.
- Guest-managed usage is accounted through guest grants (§6), so nothing is counted twice (R-RES-010).

## 3. Resource requests (estimates)

Each attempt carries `request = {cpu_demand, mem_expected, mem_ceiling, source}` resolved in order:

1. **Explicit hint** in the task spec, clamped to policy maximums (`source=HINT`).
2. **Operational memory:** p90 of peak memory and mean CPU of the last 10 runs with the same scope key, when at least 3 observations exist and the fact is fresh (`source=MEMORY`) ([07](07-records-diagnosis-memory.md)).
3. **Adapter default** for the classified tool and phase, for example `dotnet build`: cpu 4,000, mem 2 GiB; `cargo build`: cpu = parallelism × 1,000, mem 1.5 GiB × min(parallelism, 4) (`source=ADAPTER`).
4. **Generic default:** cpu 1,000, mem 512 MiB (`source=DEFAULT`).

`mem_ceiling = min(policy.max_task_memory, max(2 × mem_expected, mem_expected + 1 GiB))`, unless the hint gives one.

**Online correction.** If an attempt's measured memory exceeds `mem_expected` by more than 25% for 10 s, the scheduler raises its accounted expectation to `1.1 × observed`. This can stop further admissions; it never kills.

## 4. Admission

### Pools and limits

- **Pools:** `interactive`, `default`, `background` and `agents` are built in; users can create more.
- `max_parallel`: `AUTO` = `max(1, floor(B_cpu / 1000))`, a fixed number, or `1` when parallelism is disabled. A disable policy can apply globally, per pool, per workspace or per session (R-EXE-013).
- `weight` is used for round-robin between pools.
- Global cap: `global_max_running` (default `min(64, 2 × C_cpu/1000)`).

### Ordering

1. Effective priority class, strict: `INTERACTIVE > HIGH > NORMAL > LOW > BACKGROUND`.
2. Within a class, deficit round robin across **owners** (session, or client user for non-agent submissions) by owner weight (default 1).
3. FIFO within an owner.

**Aging:** a task waiting longer than `starvation_bound` (default 10 min) is raised one class, up to `HIGH` (R-EXE-014).

### Algorithm

The scheduler runs on events (submit, exit, grant release, budget change) and at least every 2 s.

```
avail_mem = B_mem − Σ accounted_mem(running attempts and outstanding guest grants)
cpu_load  = Σ cpu_demand(running) ;  cpu_limit = overcommit_cpu × B_cpu      (overcommit_cpu default 1.5)
for pool in pools in weighted round-robin order:
  for t in pool.queue ordered as above:
    if running(pool) ≥ pool.max_parallel or running(all) ≥ global_max_running: break
    if t.reserved_for_large: skip others whose admission would consume t's reservation
    r = request(t)
    if r.mem_expected > avail_mem or cpu_load + r.cpu_demand > cpu_limit:
        if waited(t) > large_task_bypass (default 2 min): reserve(t)   # stop smaller tasks from overtaking
        continue
    grant(t, r); start(t); avail_mem −= r.mem_expected; cpu_load += r.cpu_demand
```

**Memory is never overcommitted** (`overcommit_mem = 1.0`, R-RES-005). CPU can be overcommitted because weights share it without harming the reserved headroom: the root cap protects that headroom (§5).

A task whose `mem_expected` exceeds `B_mem` even on an idle node is not rejected. It waits with the queue blocking reason `exceeds_budget` and an explanation (`QueueService.ExplainTask`), so the user can raise the budget, lower the estimate with a hint, or cancel. A task that waits longer than twice the starvation bound raises `QUEUE_STARVATION`.

## 5. Enforcement mapping

### Root container (protects headroom)

| | Windows root job | Linux `arcforges.slice` (runtime unit properties) |
|---|---|---|
| CPU | Hard cap `CpuRate = round(B_cpu / C_cpu × 10000)` (minimum 100) | `CPUQuota = B_cpu / 10 %` (→ `cpu.max = "<B_cpu × 100> 100000"`) |
| Memory | `JobMemoryLimit = commit_factor × (C_mem − R_mem)` (commit_factor default 1.5); notification limit at `B_mem` | `MemoryHigh = B_mem`, `MemoryMax = C_mem − R_mem` |
| Processes | none | `TasksMax = 32768` |

Root limits are updated when `B` changes by more than 5% of capacity, at most every 10 s (hysteresis). While WSL guests are linked, the host's root CPU cap and commit limit exclude the totals granted to guests (§6). On Linux every limit is set through the user manager's D-Bus API (`SetUnitProperties`, runtime only), never by writing cgroup files the manager owns. Statistics are read directly from the unit cgroups ([AD-0005](../decisions/AD-0005-resource-enforcement.md) Linux §2; L-13).

### Attempt containers

| | Windows child job | Linux transient unit `arcforges-a-<attempt>.service` |
|---|---|---|
| CPU share | Weight from priority (INTERACTIVE 9, HIGH 7, NORMAL 5, LOW 3, BACKGROUND 1). If the policy sets a per-task CPU cap, the job uses hard-cap mode instead (Windows cannot combine both, V-W04). | `CPUWeight` (→ `cpu.weight`): 400, 200, 100, 50, 10. Optional per-task `CPUQuota`. |
| Memory | `JobMemoryLimit = commit_factor × mem_ceiling` (commit limit, V-W05); physical usage is watched by the monitor | `MemoryHigh = 1.25 × mem_expected`, `MemoryMax = mem_ceiling`, `OOMPolicy=kill` (whole unit on OOM kill) |
| Processes | `ActiveProcessLimit` if policy sets one | `TasksMax` (default 4096) |
| Kill | `TerminateJobObject` | `KillUnit(all, SIGKILL)` |
| Pause | unsupported | `FreezeUnit` / `ThawUnit` (→ `cgroup.freeze`) |

### Tool-level concurrency

The adapter sets the tool's parallelism to `clamp(ceil(cpu_grant/1000), 1, adapter_max)`, unless the caller already passed an explicit flag; the caller's flag is respected and recorded. Records show both the tool-level setting and the OS enforcement, and never call the tool flag a limit (R-TOOL-003).

## 6. WSL host–guest coordination

1. **Grant request.** While a guest link is up, the guest asks for a grant before admitting each attempt. It sends a `GrantRequest` frame on the link stream the host opened (`GuestLinkService.OpenLink`), because the host is the gRPC client of the guest over the bridge.
2. **Fair queueing.** The host enqueues the request as a **guest proxy task** in its own scheduler, so it competes fairly with host tasks.
3. **Grant.** The host answers with `GuestLinkService.AnswerGrant` when admitted, and the guest starts the attempt as a transient unit under its own user manager. Under pressure, the host may call `RevokeGrant`.
4. **Release.** The guest releases the grant at completion with a `GrantRelease` frame, which carries the final usage.
5. **Enforcement matches the grants.**
   - Whenever the granted totals change by more than 5% of guest capacity (at most every 10 s), the host calls `GuestLinkService.SetGuestBudget`. This sets the guest slice's `CPUQuota`, `MemoryHigh`, `MemoryMax` and `TasksMax` to the granted totals.
   - At the same time the host lowers its own root limits by the same amounts:
     - `CpuRate` from `B_cpu − Σ granted_cpu`;
     - the commit limit to `commit_factor × (C_mem − R_mem − Σ granted_mem)`;
     - the memory notification limit to `B_mem − Σ granted_mem`.
   - CPU caps on both sides together therefore never exceed `B_cpu`, and the host's memory notification limit plus the guest's `MemoryHigh` never exceed `B_mem`. The Windows commit limit bounds committed virtual memory, not physical use, and is reduced proportionally. The user's reserved headroom holds under saturating load on both sides.
   - The closed-loop test runs concurrent saturating host and guest loads (AF-WSL-01).
6. **Link loss.** If the link is down for more than 30 s, the guest admits standalone within its own `B_guest` and reports `link_lost`. The guest keeps its last pushed slice limits until it admits standalone, then sets its own. Host-side accounting treats all VM usage as `guest_other` until the link returns. This degraded mode can over-commit the physical machine, and `GUEST_LINK_LOST` says so.

## 7. Adaptation and pressure

| Level | Condition (evaluated every 1 s with 5 s persistence) | Actions |
|---|---|---|
| Normal | `available_mem ≥ 10% C_mem` and `U_cpu` stable | Normal admission |
| Tight | `available_mem < 10% C_mem` or `U_cpu` rose by more than 20% of `C_cpu` within 10 s | Admit only `INTERACTIVE`; shrink the root CPU cap (§5) |
| Pressure | `available_mem < 5% C_mem` or Linux `memory.pressure some avg10 > 20` | Linux: freeze pausable `BACKGROUND`/`LOW` attempts and lower their `MemoryHigh` to current usage to force reclaim. Windows: requeue preemptible `BACKGROUND` attempts (cancel, then requeue only if retryable). Notify. |
| Critical | `available_mem < 2% C_mem`, or an OOM kill observed | Cancel preemptible attempts from lowest priority up until the level recovers; raise a finding; notify |

Every action is journaled with its trigger and evidence. Frozen attempts thaw in priority order when the level returns to Normal for 30 s (R-RES-009).

## 8. Capabilities and degraded modes

`NodeCapabilities` reports, per resource:

| Field | Values |
|---|---|
| `cpu` | `ENFORCED_SHARE_AND_CAP`, `ENFORCED_SHARE`, `OBSERVE_ONLY` |
| `memory` | `ENFORCED_SOFT_AND_HARD` (Linux), `ENFORCED_COMMIT` (Windows), `OBSERVE_ONLY` |
| `pids` | `ENFORCED`, `OBSERVE_ONLY` |
| `io` | `OBSERVE_ONLY`, `ENFORCED` (privileged option) |
| `pause` | `SUPPORTED`, `UNSUPPORTED` |
| `kill_tree` | `GUARANTEED`, `BEST_EFFORT` |
| `adopt` | `SUPPORTED`, `LIMITED`, `UNSUPPORTED` |

Each value carries the reason (for example "user manager has no cpu delegation"). A task spec can require enforcement (`require_enforcement = {cpu, memory}`). Such a task is refused with `ERROR_CATEGORY_RESOURCE`, code `enforcement_unavailable`, when the capability is missing. Otherwise it runs with the record flag `unenforced=true` if the policy `allow_unenforced` is true (default true for `OBSERVE_ONLY` nodes, with a visible banner) (R-RES-008).

## 9. Unmanaged, escaped and bypassed processes

| Label | Meaning | Source |
|---|---|---|
| `MANAGED` | In an attempt container | Container membership |
| `ADOPTED` | Explicitly adopted by the user | Adoption record |
| `ESCAPED` | Descendant of a managed process by ancestry but outside its container (WMI, breakaway, service broker) | Ancestry scan of exited and running processes |
| `BYPASSED` | Descendant of a registered agent process, not managed, above the policy thresholds (`routing.bypass_cpu_threshold_millicores`, default 1,000 for 10 s, or `routing.bypass_mem_threshold_bytes`, default 1 GiB) | Session process roots ([08](08-ai-integration.md)) |
| `UNMANAGED` | Everything else | — |
| `GUEST_VM` | The WSL VM consumer on the host | VM worker identification |

Only `MANAGED` and `ADOPTED` processes are ever controlled (R-RES-002).
