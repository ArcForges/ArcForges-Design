# 15 — Performance and footprint targets

Requirement: R-PERF-001. Every target names its measurement. "Workstation" means the development machine of L-01/L-02 (Windows 11, 18 logical processors, 31.5 GB; WSL2 Debian with 16 GB).

- **Benchmark tool.** Benchmarks run through `tools/ArcForges.Bench` (part of the ArcForges repository). It emits JSON results that tasks attach to their PR evidence.
- **CI benchmarks** (size, startup) run in the CI-equivalent verification: the local pre-push verification for the owner's PRs and hosted runners for external PRs ([AD-0016](../decisions/AD-0016-local-first-verification.md)). They gate only on size, plus startup regressions above 25% against the PR's base commit built on the same machine (the hook: the merge base; external-PR CI: the base commit on the same runner), because the measurements are noisy.
- **Workstation benchmarks** (footprint, load) run locally and are recorded with their raw data.

## 1. Executables

| Target | Value | Measurement | Where |
|---|---|---|---|
| `arcforges` binary size (win-x64, linux-x64) | ≤ 45 MB | File size of the published binary | CI (gate) |
| `arcforges-supervisor.exe` size | ≤ 4 MB | File size | CI (gate) |
| `arcforges-desktop` publish size (without native Skia libraries) | ≤ 60 MB | Directory size | CI (gate) |
| CLI cold start (`arcforges --version`) | p50 ≤ 40 ms, p95 ≤ 80 ms | 50 runs after one warm-up of the file cache; process start to exit | Workstation; CI regression check |
| CLI status round trip (`arcforges status --json`, node running) | p50 ≤ 60 ms | 50 runs | Workstation |
| Hook handler (`arcforges hook claude-code pre-tool-use`, typical payload, observe mode) | p95 ≤ 50 ms | 100 runs, stdin fixture | Workstation |

## 2. Node

| Target | Value | Measurement | Where |
|---|---|---|---|
| Idle CPU | ≤ 0.5% of one core (10-minute average) | Process CPU time delta, LAN and cloud off. Timers: monitor 1 s; diagnosis 15 s per running attempt (none while idle) and 60 s for node-wide rules ([07](07-records-diagnosis-memory.md) §2). | Workstation, both OSes |
| Idle memory | Windows ≤ 60 MB private bytes (node + supervisor); Linux ≤ 70 MB RSS | After 10 minutes idle, with a store of 10,000 attempts | Workstation |
| Under load: 50 concurrent executions (synthetic `TestLoad` workers) | Node ≤ 2% of one core (excluding the executions), ≤ 150 MB | 10-minute steady state | Workstation |
| Per-execution helper overhead | Windows `exec-wrap` (holder and disk guard) ≤ 10 MB private each (measured 6.65 MB, 2026-10-16); Linux 0 per execution (`exit-record` runs only at exit) | Private bytes of the helper process | Workstation |
| Disk guard | Linux `arcforges-guard.service` ≤ 12 MB private (measured 8.18 MB, 2026-10-16), one per user, idle while the node's heartbeat is fresh; takeover within `storage.guard_takeover_ms` + 1 s on both platforms | Private bytes; time from the node's stop to the first guard check | Workstation |
| Admission latency (submit → `STARTED` when capacity exists) | p95 ≤ 150 ms (Windows), ≤ 250 ms (Linux, including the transient-unit job) | 500 submissions | Workstation |
| Local event latency (state change → client stream) | p95 ≤ 200 ms | Timestamps in the event and the receiver | Workstation |
| Output capture | ≥ 200 MB/s sustained, no loss. On Linux the node drops each indexed range of the output files from the page cache (`posix_fadvise(POSIX_FADV_DONTNEED)`), because written pages are charged to the attempt's memory and reclaim at its `MemoryHigh` would otherwise throttle the writer (L-25). | `TestLoad` writer at maximum rate; byte-for-byte digest comparison | Workstation |
| Store growth | ≤ 50 MB per 10,000 attempts (records, timelines, samples, cache usage and result-cache observations; logs excluded) | Database file size after generating attempts | Workstation, CI (smaller scale) |
| Evidence collection per attempt | Cache-usage measurement ≤ 2 s of background work (policy `caches.usage_scan_budget_ms`), never delaying the attempt's result | Timestamps of the measurement job | Workstation |
| Node startup to ready (warm, 100 surviving executions to re-attach) | ≤ 3 s | Startup timestamps | Workstation |
| Guest node idle (WSL2) | ≤ 40 MB RSS, ≤ 0.5% of one core | Guest after 10 minutes idle | Workstation |

**Helper memory (decision of the product owner, 2026-10-16).** The holder and the guard are roles of the one multi-role binary ([AD-0003](../decisions/AD-0003-architecture-and-runtimes.md)), whose `exec-wrap` role measured 5.5 MB private before it had read its specification (AF-EXEC-01 review, Windows), so the earlier 3 MB (holder) and 8 MB (guard) targets could not be met without a separate executable. Keeping one binary is preferred: the targets above are set from measurements with headroom. MB here means 1,000,000 bytes, as in the CI benchmarks. A dedicated lightweight helper executable is accepted future work (roadmap RM-14), revisited only if per-attempt overhead becomes a real constraint.

*Direction (roadmap; not release 1; [AD-0017](../decisions/AD-0017-delegated-execution-direction.md)):* when EX-11 is promoted, the per-execution helper row above will record the Linux per-confined-attempt overhead of `exec-init`, measured in LAB-LNX-19 ([17](17-delegated-execution.md) §15.4); until then "Linux 0 per execution" is unchanged.

## 3. Clients

| Target | Value | Measurement |
|---|---|---|
| Desktop start to first interactive frame | ≤ 1.5 s (warm) | Timestamp from process start to the first-render callback |
| Desktop idle | ≤ 1% of one core, ≤ 150 MB private | 10 minutes on the Overview page with 20 running tasks updating |
| MCP adapter idle | ≤ 40 MB | Private bytes after `initialize` |
| MCP overhead per tool call (excluding the task's own run time) | p95 ≤ 30 ms | `task_status` round trip versus a direct RPC |
| Remote viewer latency (node change → web or Android client) | p95 ≤ 5 s while watched | Closed-loop test with the relay fake; real relay deferred |
| Web Account and Fleet profile bundles | Within the existing Web budget tool limits | CI (existing gate) |
| Android cold start | ≤ 2.5 s on the emulator reference image | Emulator measurement; physical devices deferred |

## 4. Resource-control quality

| Target | Value | Measurement |
|---|---|---|
| Headroom protection | With managed CPU load at 100% of the budget, an unmanaged interactive probe (a fixed busy-loop with a 10 ms deadline per 100 ms period) misses ≤ 1% of deadlines | `TestLoad` probe under a saturating managed load, both OSes |
| Memory admission | Zero OOM kills of unmanaged processes caused by managed load in the standard load scenario (`TestLoad mem-ramp`) | Kernel log / Windows commit failures |
| Memory bounds | Linux: no attempt or root exceeds its `MemoryMax`, and swap stays within `swap_allowance` (default 0). Windows: no attempt or root exceeds its commit limit. What these bounds do and do not guarantee is stated in [03](03-resource-control.md) §5.4. | cgroup `memory.events` and `memory.swap.current`; job accounting, in `TestLoad mem-ramp` |
| Fairness | With two sessions submitting equal work in the same pool, each receives 50% ± 10% of managed CPU-seconds over 10 minutes | Records |
| Queue start after release | When an execution ends, the next admissible queued task starts within 500 ms | Event timestamps |

## 5. Rules

- A task changing a measured path runs the relevant benchmark and attaches the result. A regression beyond a target fails the task's acceptance unless the PR records an explicit justification that the reviewer accepts.
- Targets apply to Release Native AOT builds only.
- Physical-machine variety, ARM64 hardware and slow disks are deferred validation (acceptance register).
