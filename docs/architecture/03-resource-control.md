# 03 — Resource observation, budgets, admission and enforcement

Units: CPU in **millicores** (1,000 = one logical processor fully busy), memory in **bytes**. All defaults are policy values ([data/node-store.md](../data/node-store.md) `policy_document`, schema in `arcforges.node.v1.ResourcePolicy`).

## 1. Observation

| Signal | Windows source | Linux source | Interval |
|---|---|---|---|
| Machine CPU | `GetSystemTimes` | `/proc/stat` | 1 s internal, 5 s published |
| Machine memory | `GlobalMemoryStatusEx` (total, available, commit total/limit) | `/proc/meminfo` (MemTotal, MemAvailable, SwapTotal/Free, Committed_AS) | 1 s / 5 s |
| Pressure | n/a | `/proc/pressure/{cpu,memory,io}`; per cgroup `*.pressure` | 5 s |
| Disk | `GetDiskFreeSpaceExW` per volume of each managed root | `statvfs` | 5 s for volumes holding managed roots or a running attempt's working directory (the low-space guard, [06](06-storage-workspaces.md) §5); 60 s otherwise |
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

For example, on a host with 16 logical processors and 32 GiB the defaults give `R_cpu = 2600` and `R_mem = 5.2 GiB`.

**Smoothing.** Smoothing is asymmetric so the user's own load is respected quickly and released slowly. `x_t = x_{t−1} + α·(sample − x_{t−1})` with `α_up = 0.5` when the sample rises and `α_down = 0.1` when it falls, evaluated every 1 s.

**Guest terms (host only).**
- `vm_consumer_*` is the measured usage of the WSL VM.
- `guest_other_* = max(0, vm_consumer_* − Σ guest-reported managed usage)` is in-VM load that no guest manages.
- While a link is lost, guest-reported usage is unknown. The host then uses `guest_other_* = max(0, vm_consumer_* − reserved guest allocation)` (§6), so the reservation and the measured VM load are never counted twice.
- Guest-managed usage is accounted through guest grants (§6), so nothing is counted twice (R-RES-010).

## 3. Resource requests (estimates)

Each attempt carries `request = {cpu_demand, mem_expected, mem_ceiling, source}` resolved in order:

1. **Explicit hint** in the task spec, clamped to policy maximums (`source=HINT`).
2. **Operational memory:** p90 of peak memory and mean CPU of the last 10 runs with the same scope key, when at least 3 observations exist and the fact is fresh (`source=MEMORY`) ([07](07-records-diagnosis-memory.md)).
3. **Adapter default** for the classified tool and phase, for example `dotnet build`: cpu 4,000, mem 2 GiB; `cargo build`: cpu = parallelism × 1,000, mem 1.5 GiB × min(parallelism, 4) (`source=ADAPTER`).
4. **Light estimate** for a command routed by `rewrite-all` that no adapter classifies and no fact describes: cpu 250, mem 128 MiB (`source=LIGHT`, [08](08-ai-integration.md) §4.1).
5. **Generic default:** cpu 1,000, mem 512 MiB (`source=DEFAULT`).

**Ceilings.** For `HINT` (unless the hint gives one), `MEMORY` and `ADAPTER` estimates: `mem_ceiling = min(policy.max_task_memory, max(2 × mem_expected, mem_expected + 1 GiB))`. For `LIGHT` and `DEFAULT` estimates nothing is known about the command, so the ceiling does not derive from the guess: `mem_ceiling = min(policy.max_task_memory, max_share_mem / 2)`. Accounted memory, the root bound and the pressure response protect the rest (§5.4), and the first observed peak replaces the guess for admission at once.

**Accounted memory.** Admission counts every running attempt at `accounted_mem = max(mem_expected, peak_observed)`.
- `peak_observed` is the highest sampled resident use of the attempt container so far, excluding reclaimable page cache: Linux `memory.current` minus `inactive_file` (from `memory.stat`); Windows the sum of the processes' private working sets.
- It never decreases while the attempt runs, so admission never counts an attempt below what it has actually used. Growth stops further admissions. The scheduler never stops an attempt for growing below its ceiling, but the OS limits and the pressure response still apply (§5.4, §7): an OOM kill inside the slice on Linux, the commit limit on Windows, and stopping preemptible work.
- `mem_ceiling` is a per-attempt hard bound (§5). Ceilings are **not** reserved: the sum of ceilings may exceed `B_mem`, and §5.4 states what follows from that.

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
max_share_mem   = C_mem − R_mem                                   (the most managed work may ever use)
idle_budget_mem = C_mem − R_mem − U_mem − guest_other_mem          (B_mem with no managed work)
avail_mem = B_mem − Σ accounted_mem(running attempts and outstanding guest grants)
cpu_load  = Σ cpu_granted(running) ;  cpu_limit = overcommit_cpu × B_cpu      (overcommit_cpu default 1.5)
for pool in pools in weighted round-robin order:
  for t in pool.queue ordered as above:
    if running(all) ≥ global_max_running: stop
    if running(pool) ≥ pool.max_parallel and not light(t): continue   # light routed commands skip pool limits (08 §4.1)
    r = request(t) ;  c = min(r.cpu_demand, B_cpu)                    # CPU is compressible: never wait for more than the budget
    if r.mem_expected > min(max_share_mem, policy.max_task_memory): mark(t, exceeds_capacity); continue
    if r.mem_expected > idle_budget_mem:                          mark(t, exceeds_budget);   continue
    if keys(t) conflict with keys held by running attempts:       mark(t, exclusive_key);    continue
    if reservation active for another task u and admitting t would delay u: continue   # unless t backfills or is light
    if r.mem_expected > avail_mem or cpu_load + c > cpu_limit:
        if waited(t) > large_task_bypass (default 2 min) and no reservation is active and not light(t): reserve(t)
        continue
    grant(t, r, cpu = c); start(t); avail_mem −= r.mem_expected; cpu_load += c
```

**Memory is never overcommitted at admission** (`overcommit_mem = 1.0`, R-RES-005): the sum of accounted memory never exceeds `B_mem` when an attempt is admitted. CPU can be overcommitted because weights share it without harming the reserved headroom: the root cap protects that headroom (§5). What holds after admission is stated in §5.4.

**CPU is compressible.** Admission counts a task's CPU at most at `B_cpu` (`c` above), and the grant sets the tool's parallelism (§5.3). A task that asks for more CPU than the node has therefore runs, with less parallelism, instead of waiting forever. For example, on a 4-processor node (`B_cpu` = 2,600 when idle) a `dotnet build` estimated at 4,000 millicores is granted 2,600 and runs with `-m:3`. On a busy node such a task may take the large-task reservation (below), so a stream of smaller tasks cannot starve it.

### Feasibility

The scheduler separates capacity that is temporarily unavailable from requests that cannot be met:

| Class | Condition | Behaviour |
|---|---|---|
| Feasible | `mem_expected ≤ idle_budget_mem` | Waits for running work to drain; may take the large-task reservation |
| `exceeds_budget` | `idle_budget_mem < mem_expected ≤ max_share_mem` | Fits only if unmanaged load falls. Never reserves, so it cannot hold back feasible work. Raises `QUEUE_STARVATION` after twice the starvation bound. |
| `exceeds_capacity` | `mem_expected > max_share_mem` or `> max_task_memory` | Can never run under the current reserve. Never admitted or reserved; raises `TASK_INFEASIBLE` at once. The user lowers the reserve, gives a hint, or cancels. |

Feasibility concerns memory only. CPU never makes a task infeasible, because demand above the budget is clamped (above).

Explicit hints above `max_task_memory` are refused at submission (validation). Estimates from operational memory are not, because they describe past runs; they are classified as above. `QueueService.ExplainTask` returns the class (`feasibility`) and the numbers.

### Large-task reservation

A feasible task that waited longer than `large_task_bypass` would otherwise be overtaken forever by smaller tasks. The reservation is bounded:
- **One at a time.** At most one reservation per node; the longest-waiting qualifying task holds it.
- **Narrow.** Only feasible tasks reserve, so every reservation can be met once running work drains: memory by the feasibility rule, CPU because demand is clamped (above). The reservation holds back only tasks of its own and lower priority classes that would take the resource it is short of. Higher classes and light commands still run.
- **Backfill.** A held-back task still starts when operational memory gives it an `ACTIVE` `DURATION` p90 that ends before the reservation's estimated start (the drain estimate from the running attempts' own facts). Without facts there is no backfill.
- **Lapse.** The reservation lapses after `large_task_reservation_max` (default 30 min), or as soon as the task becomes `exceeds_budget` or `exceeds_capacity`. A task whose reservation lapsed cannot take a new one for the same interval.

### Workspace concurrency and keys

Concurrent tasks in one workspace can overwrite each other's files (the `obj/` and `bin/` of shared referenced projects, `node_modules`, `target/`, the git index), or read files another task is rewriting. Admission therefore honours **keys** (R-EXE-019):
- **Modes.** A writer holds an *exclusive* key; a reader holds a *shared* key.
- **Sources.**
  - The caller's `TaskSpec.concurrency` (`exclusive_keys`, `shared_keys`).
  - The adapter's keys for the tool and operation ([05](05-toolchains-caches.md) §2–3). For example:
    - .NET build-family operations (`restore`, `build`, `test`, `pack`, `publish`, `msbuild`) take `tool:dotnet:<workspace>` exclusively, because each of them restores and builds every referenced project, so any two of them in one workspace can write the same `obj/` and `bin/` directories. `test --no-build` and `run --no-build` take it shared.
    - `npm ci` and `npm install` take `ws:<workspace>/<package dir>:deps` exclusively; `npm test`, `npm run` and `npx` take it shared.
    - Cargo takes `tool:cargo:<target dir>`, which Cargo's own build-directory lock also serializes.
    - git commands that rewrite the working tree (`checkout`, `switch`, `pull`, `merge`, `rebase`, `reset --hard`, `restore`, `stash`, `cherry-pick`, `revert`, `clean`) take `ws:<workspace>` exclusively, so they wait for every build and test in the workspace; index-only writers (`add`, `commit`, `rm --cached`) take `tool:git:<workspace>`.
  - `access = EXCLUSIVE`, or the workspace's concurrency mode `SERIAL`, adds `ws:<workspace>` exclusively. Mode `SHARED` ignores adapter keys and keeps only the caller's.
- **Conflict rule.** Keys *overlap* as follows, and overlapping keys conflict unless both are shared:
  - **Directory keys** (`ws:<workspace>/<dir>[:<purpose>]`) overlap when one key's directory is the other's directory, an ancestor or a descendant. Purposes (`:deps`) separate two uses of the same directory only when both keys carry a purpose and the purposes differ.
  - **Tool keys** (`tool:<name>:<scope>`) cover a tool's own state, not a directory tree, and overlap only the same tool key. A .NET build therefore runs beside npm, CMake or Python work in other directories of the workspace.
  - **The workspace key** `ws:<workspace>` overlaps every key of that workspace, including tool keys whose scope is the workspace or a directory in it.
  - **Name keys** (`name:<text>`) overlap only the same name.
- **Effect.** A task whose keys conflict with running attempts waits with the blocking reason `exclusive_key`. `ExplainTask` lists the keys and their holders.
- **Lifetime.** Keys are held from start to the end of the task, with two exceptions, so that a long-running program does not block other work indefinitely:
  - run operations (`dotnet run`, `cargo run`, `npm start`) release their keys when the adapter's phase detector sees the program start;
  - `SERVICE` tasks release `ws:<workspace>` (from `SERIAL` or `access = EXCLUSIVE`) once they are ready.
- **Remote placement.** A task placed on another node holds no keys at the origin while it runs there; the executor's workspace slot is private to the attempt. Applying its returned outputs at the origin takes, exclusively, the keys of the output paths and the tool keys the task's adapter emits (for example `tool:dotnet:<workspace>` for a placed .NET build), so no local build writes and no local reader reads those outputs meanwhile ([09](09-lan.md) §6).
- **Scope.** Keys order managed tasks only. They do not stop unmanaged processes, and `git worktree lock` only prevents pruning. Keys also cannot see work that one tool's build scripts start in another tool (for example an MSBuild target that runs `npm install`); repositories that do this use the `SERIAL` mode. Agents that need full isolation, and parallel builds of one solution, use separate managed worktrees ([06](06-storage-workspaces.md) §3).
- **Default.** Commands no adapter knows carry no keys and may run side by side. Users who want strict ordering set the workspace to `SERIAL` or a parallelism limit of 1 for the workspace (R-EXE-013).

## 5. Enforcement mapping

**Same-user qualifier** (added 2026-10-19). Every resource guarantee in this section, and every enforcement value of §8, is **ENFORCED against accidental and over-privileged workloads, and a GUARDRAIL against workloads that target ArcForges' objects**. The containers belong to the signed-in user: on Windows, other processes of the same user can open ArcForges' named jobs (V-W11); on Linux, the attempt units and their cgroups belong to the user's own user manager (V-L01, V-L05). Same-user code can therefore change limits or end other attempts (T-22), and work launched outside the recorded ancestry never joins a container (§9, T-23). Release 1 confines no workload, so no workload is kept from these objects ([11](11-security-privacy.md) §1).

### 5.1 Root container (protects headroom)

| | Windows root job | Linux `arcforges.slice` (runtime unit properties) |
|---|---|---|
| CPU | Hard cap `CpuRate = round(B_cpu / C_cpu × 10000)` (minimum 100) | `CPUQuota = B_cpu / 10 %` (→ `cpu.max = "<B_cpu × 100> 100000"`) |
| Memory | `JobMemoryLimit = commit_factor × (C_mem − R_mem)` (commit_factor default 1.5; a bound on committed virtual memory, V-W05); notification limit at `B_mem` | `MemoryHigh = B_mem` (soft: reclaim and throttling), `MemoryMax = C_mem − R_mem` (hard), `MemorySwapMax = swap_allowance` (default 0) |
| Processes | none | `TasksMax = 32768` |

Root limits are updated when `B` changes by more than 5% of capacity, at most every 10 s (hysteresis). While WSL guests are linked, the host's root CPU cap is its share `H_cpu` of the enforceable budget and its memory limits exclude the memory granted to guests (§6). On Linux every limit is set through the user manager's D-Bus API (`SetUnitProperties`, runtime only), never by writing cgroup files the manager owns. Statistics are read directly from the unit cgroups ([AD-0005](../decisions/AD-0005-resource-enforcement.md) Linux §2; L-13).

### 5.2 Attempt containers

| | Windows child job | Linux transient unit `arcforges-a-<attempt>.service` |
|---|---|---|
| CPU share | Weight from priority (INTERACTIVE 9, HIGH 7, NORMAL 5, LOW 3, BACKGROUND 1). If the policy sets a per-task CPU cap, the job uses hard-cap mode instead (Windows cannot combine both, V-W04). | `CPUWeight` (→ `cpu.weight`): 400, 200, 100, 50, 10. Optional per-task `CPUQuota`. |
| Memory | `JobMemoryLimit = commit_factor × mem_ceiling` (commit limit, V-W05); physical usage is watched by the monitor | `MemoryHigh = 1.25 × mem_expected`, `MemoryMax = mem_ceiling`, `OOMPolicy=kill` (whole unit on OOM kill) |
| Processes | `ActiveProcessLimit` if policy sets one | `TasksMax` (default 4096) |
| Kill | `TerminateJobObject` | `FreezeUnit`, SIGKILL to each process of the unit's cgroup, direct `cgroup.freeze=0`, `ThawUnit` ([04](04-execution.md) §6) |
| Pause | unsupported | `FreezeUnit` / `ThawUnit` (→ `cgroup.freeze`) |

**Windows jobs and UI limits** (added 2026-10-19). No ArcForges job, root or attempt, sets UI limits, because jobs that set UI restrictions do not nest (V-W01; [AD-0005](../decisions/AD-0005-resource-enforcement.md) Windows §3). For the same reason, a workload that sets UI limits on jobs for its own children may fail to nest them inside its attempt job. Chromium's sandbox source code sets such limits for its sandboxed child processes ([`sandbox/win/src/job.cc`](https://chromium.googlesource.com/chromium/src/+/HEAD/sandbox/win/src/job.cc)), so Chromium-family programs, among them browser-automation MCP servers and other Chromium-based tools run as tasks, are expected to do the same. That expectation is unverified for ArcForges workloads and is not a register fact. Whether such workloads degrade or fail inside an attempt job is unknown; it is a known compatibility risk, and the design relies on no outcome.

### 5.3 Tool-level concurrency

The adapter sets the tool's parallelism to `clamp(ceil(cpu_grant/1000), 1, adapter_max)`, unless the caller already passed an explicit flag; the caller's flag is respected and recorded. Records show both the tool-level setting and the OS enforcement, and never call the tool flag a limit (R-TOOL-003).

### 5.4 What the memory controls guarantee

The reserve `R_mem` is protected in four layers. Each states exactly what it guarantees (R-RES-014), with the same-user qualifier of §5: every guarantee holds against accidental and over-privileged workloads, and is a guardrail against workloads that target ArcForges' objects or launch work outside the recorded ancestry (T-22, T-23):

| Layer | Guarantee | Linux | Windows |
|---|---|---|---|
| Admission | When an attempt starts, the accounted memory of all running attempts and guest grants is at most `B_mem`. | Same | Same |
| Hard containment of managed work | Managed work can never use more than the managed share. | **Hard:** the slice's `MemoryMax = C_mem − R_mem` covers resident memory including page cache, and `MemorySwapMax` (default 0) stops managed work from pushing into swap. Exceeding it means reclaim, then an OOM kill inside the slice only. | **Commit bound only:** the root job's commit limit bounds committed virtual memory at `commit_factor × (C_mem − R_mem)`. Windows offers no unprivileged hard cap on a job's physical memory (V-W05), so physical use is defended by the monitor layer. |
| Per-attempt ceilings | One runaway attempt is stopped at its own ceiling. | `MemoryMax = mem_ceiling` | Commit limit `commit_factor × mem_ceiling` |
| Pressure response | Unmanaged growth after admission, and managed growth below the hard bounds, are **defended, not guaranteed**: they are detected within 1 s sampling plus 5 s persistence, and acted on at once (§7). | `MemoryHigh = B_mem` shrinks with `B_mem` and forces reclaim; freezing and cancellation of preemptible attempts | Cancellation of preemptible attempts; admission stops |

Consequences stated plainly:
- **Linux.** Managed work alone can never consume the reserve. Unmanaged applications can: the node then sheds preemptible managed work in priority order.
- **Why the hard bound ignores unmanaged usage.** The admission budget `B_mem` subtracts unmanaged usage; the hard bound `C_mem − R_mem` deliberately does not. Lowering a hard limit as other applications grow would turn their growth into immediate OOM kills of managed work, including non-preemptible work. The soft limit (`MemoryHigh = B_mem`), admission and the pressure response follow unmanaged usage instead.
- **Windows.** Committed memory is bounded, physical memory is not. Physical headroom depends on the pressure response, and a test proves its reaction time.
- **Non-preemptible attempts** are never cancelled because of unmanaged growth. If only non-preemptible work remains while available memory is below 2% of `C_mem`, the node raises a critical finding and leaves the decision to the user; the OS limits above still apply.
- The tests cover the Linux hard bound under saturating managed load (AF-EXEC-02), the Windows commit bound (AF-EXEC-01), the pressure response to a synthetic unmanaged allocator on both platforms (AF-RES-01), and admission under the standard load (AF-SCHED-01).

## 6. WSL host–guest coordination

1. **Grant request.** While a guest link is up, the guest asks for a grant before admitting each attempt. It sends a `GrantRequest` frame on the link stream the host opened (`GuestLinkService.OpenLink`), because the host is the gRPC client of the guest over the bridge.
2. **Fair queueing.** The host enqueues the request as a **guest proxy task** in its own scheduler, so it competes fairly with host tasks.
3. **Grant.** The host answers with `GuestLinkService.AnswerGrant` when admitted, and the guest starts the attempt as a transient unit under its own user manager. Under pressure, the host may call `RevokeGrant`.
4. **Release.** The guest releases the grant at completion with a `GrantRelease` frame, which carries the final usage.
5. **Demand is admitted; allocations are enforced.** Grants are admitted like host attempts, against the host's accounting: CPU demand may be overcommitted up to `overcommit_cpu × B_cpu`, memory never. Enforcement then divides the host's **enforceable** budget, which can never be overcommitted:
   - **CPU split.** With `D_h` the CPU demand of running host attempts and `D_g` the granted guest demand:
     `G_cpu = clamp(B_cpu × D_g / (D_h + D_g), min_guest_cpu, min(B_cpu − min_host_cpu, C_guest_cpu − R_guest_cpu))` and `H_cpu = B_cpu − G_cpu`, where `min_guest_cpu = min_host_cpu = 100` millicores. With no grants, `G_cpu = min_guest_cpu`. Both shares are positive, the guest never gets more than its own processors can use, and the two sum to exactly `B_cpu`, however far demand is overcommitted.
   - **Memory.** Admission keeps `Σ granted mem_expected` within the host's available budget. The guest slice gets `MemoryHigh = Σ granted mem_expected` and `MemoryMax = min(Σ granted mem_ceiling, C_guest_mem − R_guest_mem)`. The host's root keeps its own formulas with the granted expected memory subtracted, never below zero: notification limit `max(0, B_mem − Σ granted mem_expected)`, and commit limit `commit_factor × max(1 GiB, C_mem − R_mem − Σ granted mem_expected)`.
   - **Allocations are acknowledged.** The host pushes each allocation with `GuestLinkService.SetGuestBudget` (`CPUQuota = G_cpu`, the memory values, `TasksMax`, the lease end `lease_until` = now + 120 s, the **standalone allocation** below, and an increasing `allocation_seq`). The guest applies the slice limits before it answers, so the answer acknowledges the allocation. The host accounts the guest at the larger of its granted totals and every allocation pushed since the last acknowledged one: capacity the guest releases is reused only after the guest acknowledges the smaller allocation.
     - **Persisted before it is sent.** Before each push, the host writes the pushed values and raises its persisted **reserved allocation** (`guest_link.reserved_*`) to cover them. On each acknowledgement it records the acknowledged values (`guest_link.acked_*`) and lowers the reservation to the larger of them and any push still unacknowledged. A host restart therefore never forgets a raise it may have sent. Pushes are serialized: the host sends the next push only after the previous one is acknowledged or the link is lost, so at most one push is ever unacknowledged.
   - **Pushing.** A grant that raises the allocation is pushed and acknowledged before `AnswerGrant`, so a granted attempt never starts under a smaller slice limit. Decreases and CPU rebalancing are pushed when they change by more than 5% of guest capacity, at most every 10 s, and at least every 30 s as a lease renewal. The host sets its own `CpuRate` from `H_cpu` at the same time.
   - **Result.** CPU caps on both sides sum to `B_cpu`; the host's memory notification limit plus the guest's `MemoryHigh` stay within `B_mem`. The closed-loop test runs concurrent saturating host and guest loads (AF-WSL-01).
6. **Link loss never over-commits the machine.** The invariant is that the host never accounts a guest below the allocation the guest enforces.
   - **While the lease runs**, the guest admits only within its last acknowledged allocation and keeps its slice limits. The host keeps that allocation accounted.
   - **After the lease lapses**, the guest admits a new attempt only while the accounted demand of its running attempts and the new one (as in admission, §4) stays within the **standalone allocation** of its last acknowledged push. Measured usage is not used, because idle attempts can grow again. The standalone allocation is `min(that allocation, guest_standalone_fraction × B_host)` for CPU and memory (fraction default 25%), never its own `B_guest`. It does not lower its slice limits, because that could kill or throttle running attempts; they finish normally. It reports `link_lost`.
   - **The host keeps the guest's reserved allocation**: the last acknowledged allocation, together with any larger push the guest has not acknowledged (persisted, item 5), for as long as the guest may still enforce it.
     - Measured usage never shrinks the reservation. An idle guest has given nothing back: its slice limits still let its work use the whole allocation the moment it resumes, for example after waiting on I/O.
     - The host's own limits follow the reservation: its CPU cap is `B_cpu − reserved G_cpu` (never below `min_host_cpu`), and its memory limits exclude the reserved guest memory.
     - If unmanaged load shrinks `B_cpu` during the outage, only the host's share shrinks, down to `min_host_cpu`. The guest's cap cannot be lowered without the link, so the two caps can then exceed the smaller budget until the link returns; the pressure response acts on host work meanwhile (§7).
   - **The reservation ends only on evidence** that the guest enforces less:
     - **The link returns** and the guest acknowledges a smaller allocation. On reconnection the guest's `GuestHello` reports the allocation it applies (`applied_seq` and the applied values), which the host adds to the reservation if it is larger, and the guest re-registers every attempt it admitted during the outage, with `GrantRequest.already_running=true`. The host accounts those attempts at once, so its next push covers all running guest work, and the guest never applies a limit below its running work.
     - **The guest's processes have all ended**: the host observes that the guest's distribution has stopped, or that the VM worker process has exited. It checks with `wsl.exe --list --running --quiet` every 30 s while the link is lost; that call never starts a stopped distribution (L-23). A call that fails, or does not answer within 10 s, counts as running.
   - **Restarted distributions.** The kernel's boot ID is shared by every distribution of the VM and survives `wsl --terminate`, so it cannot tell a distribution restart.
     - The guest node therefore keeps a marker with a random ID in its distribution's tmpfs runtime directory (`$XDG_RUNTIME_DIR/arcforges/distro-boot`, L-23), and that ID in `host_link`.
     - At startup the guest creates the marker if it is missing. Without a link, it admits under its persisted allocation only when the marker's ID equals `host_link.distro_boot_marker`, the ID recorded when it last applied an allocation. Otherwise (a new boot of its distribution, even one in which an earlier guest process already created the marker, or a lost runtime directory) it admits nothing until it links again, because the host may have released its reservation (A-L05).
   - **Disabling the link** (`SetGuestLink enabled=false`) or removing the guest binary does not end the reservation; only the evidence above does.
   - **Cost.** During a long outage the host can run with less capacity than it could otherwise use. `GUEST_LINK_LOST` shows the reserved allocation and the two ways to end the reservation: restore the link, or stop the distribution.
   - **Several distributions** share one VM. Each guest's acknowledged allocation is reserved separately. A stopped distribution releases only its own; the VM worker's exit releases all of them.
   - **Restarts.** Both sides persist the last pushed, acknowledged and reserved allocations, the lease end and the standalone allocation (`guest_link`, `host_link`), so a node restart during an outage keeps the same limits and the same reservation.
   - **Never linked.** A guest that has never been linked (no pinned host in `host_link`) is an independent Linux node and admits within its own budget inside the VM. Until the first link, the host counts the VM's whole usage as `guest_other`, which lowers the host budget only after the load appears. This window is not coordinated: D-05 shows the guest as `DISCOVERED` or `CONNECTING` with the explanation, and it closes at the first link, which the host starts as soon as it discovers the guest node (SM-GUEST-LINK `DISCOVERED` → `CONNECTING`).
   - `GUEST_LINK_LOST` reports the outage and the allocation in force.

## 7. Adaptation and pressure

| Level | Condition (evaluated every 1 s with 5 s persistence) | Actions |
|---|---|---|
| Normal | `available_mem ≥ 10% C_mem` and `U_cpu` stable | Normal admission |
| Tight | `available_mem < 10% C_mem` or `U_cpu` rose by more than 20% of `C_cpu` within 10 s | Admit only `INTERACTIVE`; shrink the root CPU cap (§5) |
| Pressure | `available_mem < 5% C_mem` or Linux `memory.pressure some avg10 > 20` | Linux: freeze pausable `BACKGROUND`/`LOW` attempts and lower their `MemoryHigh` to current usage to force reclaim. Windows: requeue preemptible `BACKGROUND` attempts (cancel, then requeue only if retryable). Notify. |
| Critical | `available_mem < 2% C_mem`, or an OOM kill observed | Stop preemptible attempts from lowest priority up, without the graceful phase ([04](04-execution.md) §6), until the level recovers; raise a finding; notify |

Every action is journaled with its trigger and evidence. Frozen attempts thaw in priority order when the level returns to Normal for 30 s (R-RES-009).

- **Non-preemptible attempts** are never frozen or cancelled by these levels. When only such attempts remain at Critical, the node raises a critical `MEMORY_PRESSURE` finding and notifies; it does not kill them (§5.4).
- **Disk.** Free space on volumes that hold managed roots has its own levels (`DiskPressureLevel`) and actions ([06](06-storage-workspaces.md) §5).

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

Each value carries the reason (for example "user manager has no cpu delegation"). The `kill_tree` reasons carry the same-user qualifier of §5 (amended 2026-10-19; the delivered reasons gain this ending with AF-SEC-01). The Linux reason "every process of an attempt is in its unit's cgroup, which the node freezes and kills; no process can leave it without the user manager" and the Windows reason "TerminateJobObject ends every process of the attempt's job; jobs allow no breakaway" each end with "; same-user code can change or end ArcForges' containers (T-22), and work launched outside the recorded ancestry never joins them (T-23)". A task spec can require enforcement (`require_enforcement = {cpu, memory}`). Such a task is refused with `ERROR_CATEGORY_RESOURCE`, code `enforcement_unavailable`, when the capability is missing. Otherwise it runs with the record flag `unenforced=true` if the policy `allow_unenforced` is true (default true for `OBSERVE_ONLY` nodes, with a visible banner) (R-RES-008).

## 9. Unmanaged, escaped and bypassed processes

| Label | Meaning | Source |
|---|---|---|
| `MANAGED` | In an attempt container | Container membership |
| `ADOPTED` | Explicitly adopted by the user | Adoption record |
| `ESCAPED` | A process outside an attempt's container whose recorded ancestry passes through a member of that container | Ancestry scan of exited and running processes |
| `BYPASSED` | Descendant of a registered agent process, not managed, above the policy thresholds (`routing.bypass_cpu_threshold_millicores`, default 1,000 for 10 s, or `routing.bypass_mem_threshold_bytes`, default 1 GiB) | Session process roots ([08](08-ai-integration.md)) |
| `UNMANAGED` | Everything else | — |
| `GUEST_VM` | The WSL VM consumer on the host | VM worker identification |

Only `MANAGED` and `ADOPTED` processes are ever controlled (R-RES-002).

**What the ancestry scan detects** (corrected 2026-10-19; the `ESCAPED` row previously named WMI, breakaway and service brokers as detected causes). On Windows the scan detects only escapes whose recorded ancestry still passes through a job member. Attempt jobs allow no breakaway ([AD-0005](../decisions/AD-0005-resource-enforcement.md) Windows §2). Launches through WMI, a broker, a service, a scheduled task or a spoofed parent leave no such ancestry (V-W01, V-W10): they are not detected and appear as `UNMANAGED`. This is a documented gap ([11](11-security-privacy.md) §1, T-23; A-W04), not a detection.
