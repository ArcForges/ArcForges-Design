# 15 — Performance and footprint targets

Requirement: R-PERF-001. Every target names its measurement. "Workstation" means the development machine of L-01/L-02 (Windows 11, 18 logical processors, 31.5 GB; WSL2 Debian with 16 GB).

- **Benchmark tool.** Benchmarks run through `tools/ArcForges.Bench` (part of the ArcForges repository). It emits JSON results that tasks attach to their PR evidence.
- **CI benchmarks** (size, startup) run on hosted runners. They gate only on size, plus startup regressions above 25% against the previous main run, because hosted runners are noisy.
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
| Per-execution helper overhead | Windows `exec-wrap` ≤ 3 MB private each; Linux 0 (`exit-record` runs only at exit) | Private bytes of the helper process | Workstation |
| Admission latency (submit → `STARTED` when capacity exists) | p95 ≤ 150 ms (Windows), ≤ 250 ms (Linux, including the transient-unit job) | 500 submissions | Workstation |
| Local event latency (state change → client stream) | p95 ≤ 200 ms | Timestamps in the event and the receiver | Workstation |
| Output capture | ≥ 200 MB/s sustained, no loss | `TestLoad` writer at maximum rate; byte-for-byte digest comparison | Workstation |
| Store growth | ≤ 50 MB per 10,000 attempts (records, timelines, samples; logs excluded) | Database file size after generating attempts | Workstation, CI (smaller scale) |
| Node startup to ready (warm, 100 surviving executions to re-attach) | ≤ 3 s | Startup timestamps | Workstation |
| Guest node idle (WSL2) | ≤ 40 MB RSS, ≤ 0.5% of one core | Guest after 10 minutes idle | Workstation |

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
| Fairness | With two sessions submitting equal work in the same pool, each receives 50% ± 10% of managed CPU-seconds over 10 minutes | Records |
| Queue start after release | When an execution ends, the next admissible queued task starts within 500 ms | Event timestamps |

## 5. Rules

- A task changing a measured path runs the relevant benchmark and attaches the result. A regression beyond a target fails the task's acceptance unless the PR records an explicit justification that the reviewer accepts.
- Targets apply to Release Native AOT builds only.
- Physical-machine variety, ARM64 hardware and slow disks are deferred validation (acceptance register).
