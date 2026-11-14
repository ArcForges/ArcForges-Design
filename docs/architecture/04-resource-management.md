# Resource observation and coordination

Status: current V2 design. Implementation is assigned to AFV2-RES-01 through AFV2-RES-03, after the platform composition decisions in AFV2-MXC-01 through AFV2-MXC-04. Historical implementation facts are distinguished from new requirements. See [runtime audit](../research/runtime-audit.md) and [lifecycle](07-lifecycle-recovery.md).

## 1. Responsibilities and authority

The Node Resource Manager observes the host, admits immediate Run starts, allocates the managed CPU budget, tracks memory reservations, applies explicit limits and records what the OS actually accepted. MXC owns isolation and sandboxed process creation. The durable RunSupervisor owns one Run's process/container/terminal lifetime. These roles compose one Sandbox Core; the Center and Web do not implement a second scheduler or enforcement path.

Policy has three levels: the host managed budget, a Sandbox's limit and weight, and a Run's immutable start request plus explicitly versioned runtime adjustments. A Run cannot enlarge its Sandbox permissions or exceed its hard limits. A remote resource update passes through the same Node authorization, validation and application code as a local update.

An OS resource scope includes every managed descendant and the trusted supervisor/helper overhead required to own it. The Resource Manager keeps two views: aggregate managed-scope cost (used for the total managed budget) and workload estimate (shown per Run with its measurement kind). Nested counters must not be summed twice. External host processes are observed only; ArcForges neither adopts nor kills them to make a budget fit.

## 2. Existing assets and deliberate changes

The existing implementation has real host samplers, one-second observations, asymmetric unmanaged-load smoothing, pressure persistence, conservative memory accounting and root-limit hysteresis. Those algorithms are extracted from their Task/Attempt dependencies. The old scheduler's pools, queue, per-AI-owner fairness, priority aging, dependency graph, concurrency keys, backfill, automatic retries and requeue behavior are removed. A Start either reserves resources and begins one Run, or fails with an observable refusal; it does not create an indefinitely queued Task.

Source evidence at ArcForges `10f692224f94916cfc93fbad971f80ec340c5edf`:

- [ResourceMonitor](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Resources/ResourceMonitor.cs)
- [PressureEvaluator and AsymmetricSmoother](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Resources/PressureEvaluator.cs)
- [CriticalShedding](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Resources/CriticalShedding.cs)
- [ExecutionSettings](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Execution/ExecutionSupport.cs)
- [Scheduling and NextRootBudget](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/Execution/ExecutionSupervisor.Scheduling.cs)

These are evidence for reuse, not evidence that MXC already satisfies the new composition.

## 3. Policy model

All numeric policy values are validated before committing a revision. CPU is expressed in millicores; memory and storage are bytes; durations use milliseconds on the wire. Negative values, overflow, NaN/infinity, unknown enum values and internally inconsistent caps are rejected. Missing optional values mean the documented inherited policy, not zero. No generic dictionary of arbitrary OS properties is exposed to application callers.

| Scope | Fields | Meaning |
|---|---|---|
| Node | host CPU/memory reserve targets and managed ceilings; internal smoothing/floor/pressure/retention parameters | Host protection and observation policy, versioned as one revision; public updates use only the typed `ResourcePolicy` fields |
| Sandbox | CPU weight, optional CPU cap, expected-memory default per Run, platform-typed memory hard ceiling, maximum concurrent Runs, permitted pressure-stop policy | Defaults and aggregate upper boundary for this Sandbox |
| Run | expected memory, requested CPU cap/weight bounded by Sandbox, optional stricter memory ceiling, preemptible flag, stop grace | Immutable start snapshot; later supported changes create a resource-policy revision and a recorded operation |

The initial inherited defaults preserve the tested resource model: reserve CPU 1000 millicores plus 10%, reserve memory 2 GiB plus 10%, alpha-up 0.5, alpha-down 0.1; memory-pressure fractions 10%, 5%, 2%, and Linux memory-some PSI threshold 20. The defaults are a starting policy, not a promise that low-capacity machines can reserve more than they possess. On capability discovery, normalize reserve to at most capacity, clamp the CPU floor to the remaining managed share and show the normalized values. Zero managed capacity refuses new Starts with `RESOURCE/budget_unavailable`; it never launches an unbounded process. A configured hard limit below an already-running scope's safe adjustable boundary is refused before applying it; the user can explicitly stop the Run and start a new Run under the new limit.

The same-user host remains outside the sandbox's resource trust boundary: the user or another privileged host component can change total load or OS policy. ArcForges reserves resources by managing its own scopes; it cannot reserve an absolute quantity against all other host actors. The UI calls this a host-reserve **target** and exposes actual managed limits and pressure.

The public host-reserve fields contain the resolved byte/millicore targets; the initial fixed-plus-fraction defaults are normalized to those values at host discovery. Internal smoothing, hysteresis and pressure thresholds are versioned implementation policy, not arbitrary caller-supplied OS options. `expected_memory_bytes` is a positive reservation estimate distinct from `memory_max_bytes`; a Run inherits the Sandbox's admitted default when omitted, and Start rejects an unresolved estimate. Priority ranges from -20 through 20, with larger values favored. The initial pressure-admission bands are background (-20 through -1), normal (0 through 9) and explicitly interactive (10 through 20); these are caller-requested bounded resource preferences and do not infer whether a program is human- or AI-driven.

## 4. Observation contract

`ResourceSnapshot` contains a monotonic sample sequence, wall-clock display time, sample interval, policy revision, freshness state and separate host/managed/Node/unmanaged measurements. Its typed fields expose capacity, current derived budgets, CPU interval/cumulative use, memory measurement kind/peak/reservations, process count, supported PSI observations and pressure state/reason. The containing Sandbox/Run capability snapshot identifies the backend profile. The internal sampler also reads available memory, commit, I/O and OOM facts where available to derive pressure and control decisions; the public API promises only its explicit typed fields, not an arbitrary counter dictionary.

Per Run include scope identity, current labeled memory estimate, monotonic observed peak, cumulative CPU, current process count, configured reservation, hard-limit kind, desired/applied/readback state and last error. Do not label a resident observation as Windows Job committed memory or infer a resident hard cap from it. Per Sandbox aggregate each owned Run once. Unavailable data is absent with `unsupported`, `permission_denied`, `scope_lost` or `sample_failed`; zero is a real observation and must not stand for failure.

Use the existing one-second internal cadence. Publish five-second aggregates for normal remote dashboards; idle process-table scans/flushes may reduce to thirty seconds. A local subscriber may request the bounded one-second stream. Cap each event queue and sample store; a slow usage subscriber closes with RESOURCE/overloaded and reconnects for fresh complete snapshots, without cursor replay or backfill. Node event publication does not block the resource control loop.

Sample staleness after three missed internal intervals makes new Start admission unavailable until a fresh capacity/resource snapshot exists. Existing Runs retain the last successfully applied hard limits; uncertainty never causes limits to be removed. Emit a degraded event and retry the failing observation at bounded intervals. An operator can inspect and stop Runs during degraded observation.

Historical measurement definitions must remain explicit:

| Platform | Existing useful source | Meaning and limitation |
|---|---|---|
| Windows host | `GetSystemTimes`, `GlobalMemoryStatusEx`, process table/private working sets | Physical/resident observation differs from Job committed-memory control |
| Windows managed scope | Job cumulative accounting and actual scope membership | Includes exited members' cumulative CPU; nested completion messages alone do not prove which scope hit a memory limit |
| Linux host | `/proc/stat`, `/proc/meminfo`, PSI, vmstat | Kernel/distro capability may make a counter unavailable |
| Linux managed scope | `cpu.stat`, `memory.current`, `memory.stat`, `io.stat`, `cgroup.procs` | Resident estimate excludes `inactive_file`; the kernel memory-controller limit applies to its own broader accounting |

Pinned definitions: [ResourceSampling](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Platform/ResourceSampling.cs), [Windows sampler](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Platform.Windows/WindowsResourceSampler.cs), [Linux sampler](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Platform.Linux/LinuxResourceSampler.cs).

## 5. Budget and immediate admission

For each dimension derive unmanaged use from nonnegative host use minus managed-scope use and Node overhead, without subtracting an overhead process twice. Smooth rising unmanaged use with alpha-up and falling use with alpha-down. The managed CPU budget follows the existing model, with floor and reserve normalized to capacity; the memory budget is `max(0, capacity - reserve - smoothed unmanaged use)`.

An active Run reserves `max(expected resident memory, observed resident peak)` for start-admission accounting. Its platform hard memory limit is a separate field. Raising the expected memory of one Run cannot manufacture additional capacity. Node-wide and Sandbox-wide sums are checked in a single admission transaction under the current policy revision and resource sample sequence. The transaction inserts a durable Run in Starting and its reservation before the supervisor can execute user code. Start rollback releases its reservation only after launch is proven not to have occurred or ownership cleanup has been confirmed.

At every admission decision check:

1. Current Sandbox revision and profile support all required isolation/terminal/resource capabilities.
2. The Sandbox is READY, its configuration write lease is free, and its concurrent-Run allowance is available.
3. The host observation is fresh and required resource controllers are available.
4. Expected memory and requested bounds fit the normalized host and Sandbox budgets.
5. The current pressure policy permits a start of this priority; Critical refuses all starts, Tight/Pressure permits only explicitly interactive-priority starts that still fit.
6. Existing and prospective scope reservations are accounted exactly once.

Failure after durable command admission returns `RESOURCE/budget_unavailable` with the limiting dimension, requested amount, available amount, policy revision and sample time. An idempotent replay returns the same admitted outcome for the same owner epoch, operation ID and canonical request; after response compaction its retained identity still cannot execute. A later explicit attempt after resources change uses a new operation ID. The distinct earlier journal/identity-capacity check can refuse before command admission with DID_NOT_HAPPEN and no receipt; it must explicitly say not admitted, preserve capacity for existing Run Stop/revocation/reconciliation, and never masquerade as a recorded resource-budget refusal. No automatic retry turns a known durable refusal into hidden later execution.

CPU weights express relative shares only among contending managed Runs; they are not minimum-core guarantees. Allocate the managed budget across active Sandboxes by positive weight subject to hard caps, redistribute unused allocations among runnable scopes, then divide each Sandbox allocation across its Runs subject to Run caps. Stable ordering by ID breaks rounding ties. A scope's total assigned ceiling must not exceed the budget because of rounding; OS granularity and normalized readback are exposed. Idle Sandboxes reserve no CPU. No future plugin, GPU or tool-specific allocator is introduced.

## 6. Applying and reading back limits

Every adjustable dimension has one state record:

| Field | Required meaning |
|---|---|
| desired revision/value | Last authorized policy request; not proof of enforcement |
| applied value/time | Last successful setter call and normalized value |
| readback value/time | Last actual OS query of the owned scope, with scope identity |
| status | pending, effective, degraded, failed or unsupported |
| reason | Stable bounded reason code; operator detail must not leak credentials or arbitrary command text |

`effective` is set only when readback confirms the accepted value within documented OS granularity at the same scope identity. Setter success without readback remains pending/degraded. Readback mismatch, resource-owner loss or access denial cannot be hidden by copying desired values into the effective fields. Serialize updates per scope and discard stale completions by policy revision. Observe the physical scope again after reconnect before advertising enforcement.

Retain the tested hysteresis: changes above 5% of host capacity count, falls apply immediately, increases wait ten seconds since the prior update, and a pressure-entry forced change applies immediately. Readback is associated with each applied revision; repeated telemetry sampling need not re-set unchanged limits. A failed update keeps the known previous limit, records the new failure and denies starts requiring the missing guarantee. It does not destroy unrelated Runs or disable isolation.

Memory semantics differ:

- Windows: committed-memory limit and notification threshold are labeled as such. Do not report an RSS hard cap. Lowering the commit limit below current committed usage is refused or handled only by the documented explicit stop path.
- Linux: dynamic `MemoryHigh` may cause reclaim/stalls; `MemoryMax` and swap allowance remain explicit hard boundaries. The initial resource contract does not expose a freeze/pause action.
- A process-count or I/O limit is advertised only when the selected profile actually applies and reads it back. Old wrappers' ability to set a field is insufficient if no product policy invokes it.

## 7. Platform composition gate

Windows existing Jobs and Linux existing systemd units are not retained as an alternative execution engine. The intended composition is a RunSupervisor admitted into its ArcForges resource scope **before** it invokes the official SDK or executor, with all user-code descendants remaining below that scope. This is conditional on AFV2-MXC experiments proving the exact official release/profile. Windows fallback modes that introduce incompatible Job UI restrictions cannot silently replace the verified profile. Linux missing namespace/bubblewrap support cannot fall back to a plain process. No unverified late PID-assignment path is allowed.

The platform proof must cover two independent Run scopes, root/Sandbox aggregate accounting, nested-job message provenance, hard-cap readback, descendant limits, parent/supervisor/Node failure, and cleanup without affecting a foreign scope. If the official API does not expose enough ownership or pre-execution composition to meet a required guarantee, mark that profile unsupported and stop dependent implementation until a conforming official mechanism is available. Do not change MXC source or invent an unsafe fallback.

The original Windows code already refuses foreign-Job adoption and distinguishes commit limits from RSS: [WindowsExecutionPlatform](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Platform.Windows/WindowsExecutionPlatform.cs). Linux source demonstrates root slice and cgroup readback, not MXC compatibility: [LinuxExecutionPlatform](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Platform.Linux/LinuxExecutionPlatform.cs).

## 8. Pressure actions and no implicit rerun

Pressure transitions use monotonic time and the existing five-second persistence; machine OOM observations retain the ten-second raw Critical hold. Record raw state, effective state and trigger independently. A short dip must not stop Runs before persistence. Returning to Normal does not restart a terminated Run.

At Tight, tighten managed CPU according to the budget and deny noninteractive new starts. At Pressure, apply supported soft limits under `THROTTLE`; `STOP_PREEMPTIBLE` additionally authorizes the critical-stop algorithm when `preemptible=true`. The initial contract does not advertise pause or freeze. Existing Linux freeze/thaw primitives may be retained as platform research assets, but a product action requires a later explicit contract and native proof. Windows pause is unsupported; do not simulate it by stopping/retrying.

At Critical, stop only Runs whose committed policy permits pressure stop. Use the existing safe victim algorithm: lowest priority, most recent first; skip already stopping/finalizing/OOM-ending Runs. Await confirmed termination and a new sample before selecting another. An OOM-only hold causes at most one additional stop per newly observed unanswered OOM event. When no eligible victim exists, expose `pressure_unrelieved` and refuse new starts; do not terminate a nonpreemptible or external process without authority.

## 9. Acceptance and deletion gate

AFV2-RES-01 extracts observation/math and proves source-level regression against the existing ResourceModel tests. AFV2-RES-02 implements allocation, admission and requested/applied/readback state. AFV2-RES-03 qualifies real native multi-Run behavior, host responsiveness and pressure recovery on the exact supported profiles. These tasks consume the MXC experiment result, not an assumed backend guarantee.

Required evidence includes saturated managed CPU with an unmanaged responsiveness probe; correct CPU cap normalization; mixed Sandbox weights/caps; resident-versus-commit display; memory pressure with bounded preemption; no repeated OOM-hold shedding; policy changes racing with Start; setter failure/readback mismatch; unavailable controller; stale observation; supervisor restart/identity loss; and the same local result with Center offline or subscription expired. Native tests use test-owned scopes and bounded synthetic workloads on the designated hosts.

Only after this evidence passes may the old queue/Task admission classes, platform launch branches and obsolete resource contracts be removed. Preserve source-backed regression tests that protect the extracted behavior; remove tests whose sole purpose is the cancelled old product. A failed resource migration is rolled back by reverting the consumer change before data-contract cutoff, or restoring the named pre-cutover backup afterward. It never falls back to uncontained execution.
