# 07 — Execution records, diagnosis and operational memory

## 1. Records

Every attempt produces:
- **timeline segments:** contiguous intervals with one category;
- **resource samples:** 1 s while running, downsampled later;
- **process records:** each process seen in the tree, with identity, executable, redacted arguments, first and last seen, and peak memory;
- **phase events:** adapter markers with their timestamps;
- **output** files ([04](04-execution.md) §4);
- **findings.**

Tasks aggregate their attempts. Sessions, workspaces and periods aggregate tasks (R-REC-001, R-REC-003).

### 1.1 Categories

| Category | Meaning | Source of truth |
|---|---|---|
| `QUEUED_ADMISSION` | Waiting for budget or concurrency | Scheduler state |
| `QUEUED_DEPENDENCY` | Waiting for dependencies | Scheduler state |
| `RETRY_BACKOFF` | Between attempts | Scheduler state |
| `WORKSPACE_PREPARATION` | Worktree creation, remote workspace materialization | Node jobs |
| `TRANSFER` | Input or output transfer for placement | Transfer service |
| `RESTORE` | Dependency restore or download phase | Adapter markers |
| `BUILD` | Compile and build | Adapter markers, process names (compiler, MSBuild nodes) |
| `TEST` | Test execution | Adapter markers, process names (`testhost*`) |
| `LINK_PACKAGE` | Linking, packaging, publishing | Adapter markers, process names (linkers) |
| `RUN` | Generic running work | Default for running attempts |
| `NETWORK_WAIT` | Little CPU, no output, inside a network-bound phase (restore or download) | **Inferred** (no per-process network attribution) |
| `DISK_WAIT` | Little CPU with I/O stall evidence | Linux: cgroup `io.pressure`. Windows: high I/O operation rate with low CPU (inferred, low confidence) |
| `IDLE_NO_PROGRESS` | No CPU, I/O, output or process change beyond the idle threshold | Signals |
| `THROTTLED` | CPU throttled more than 50% of the interval | Linux `cpu.stat throttled_usec`. Windows: root cap active and job CPU at its share (inferred) |
| `PAUSED` | Frozen | Freeze state |
| `NODE_GAP` | The node was down; work may have continued | Recovery |
| `FINALIZING` | Exit seen, output and accounting being finalized | Supervisor |
| `UNKNOWN` | No classification | Fallback |

### 1.2 Classifier

Each running attempt is evaluated every second from these signals:
- CPU delta (millicores);
- I/O byte delta;
- output byte delta;
- process set changes;
- the current adapter phase;
- Linux per-cgroup PSI (`cpu`, `memory`, `io` `some avg10`) and throttling;
- freeze state.

Rules in order:
1. frozen → `PAUSED`;
2. throttled → `THROTTLED`;
3. low activity, where CPU < 50 millicores, I/O < 64 KiB/s and no output: in a network-bound phase → `NETWORK_WAIT` (confidence MEDIUM); with I/O pressure (Linux `io some avg10 ≥ 10`) → `DISK_WAIT` (HIGH); beyond the idle threshold → `IDLE_NO_PROGRESS`; otherwise the current phase category with confidence LOW;
4. otherwise the adapter phase (`RESTORE`, `BUILD`, `TEST`, `LINK_PACKAGE`) or `RUN`.

Ticks merge into segments, and segments shorter than 2 s merge into neighbours. **Confidence:** `HIGH` when an adapter marker and the signals agree; `MEDIUM` for marker-only or adapter-informed inference; `LOW` for heuristics. Each segment stores its evidence, for example `"cpu 12m, io 0 B/s, phase=restore, 48 s"`.

**Non-claims (R-REC-002).** Progress is never inferred from process existence. Elapsed time is never described as model thinking. Network waits are always labelled as inferred, because the node does not attribute network traffic per process.

### 1.3 Repeat and stale detection

- **Input fingerprint:**
  - git workspaces: digest of `HEAD` plus a digest of the `git status --porcelain=v2` output and the content digests of modified tracked and untracked files under the task's working directory, bounded to 50 MiB of hashing (beyond that, recorded as `fingerprint=PARTIAL`);
  - non-git directories: no fingerprint (`UNAVAILABLE`).
- **Repeat:** a new attempt with the same command fingerprint and input fingerprint as a previous successful attempt, whose inputs did not change between them, is flagged `REPEAT` and raises finding `REPEATED_WORK` (R-REC-004).
- **Stale:** the fingerprint is computed at submission, admission and completion. A change between submission and completion flags the attempt `STALE`.

### 1.4 Reports and exports

| Report | Scope | Content |
|---|---|---|
| Task timeline | task / attempt | Segments, samples, phases, process tree, result, findings |
| Session report | agent session | Tasks, managed versus bypassed work, time by category, repeats, stale work, failures, retries, coverage |
| Waste report | node and period | Time by category across tasks; admission wait versus execution; idle no-progress; repeats; stale work; per-task restores; top contributors |
| Cache report | node and period | [05](05-toolchains-caches.md) §7 |
| Disk report | node | [06](06-storage-workspaces.md) §6 |
| Capacity report | node and period | Budget, utilisation, pressure levels, admissions refused or delayed |

All reports come as tables and timelines in the UIs, as `DiagnosisService.GetReport` (protobuf), and as JSON Lines exports (`ExportRecords`), one record type per line, schema `arcforges.node.v1` JSON mapping (R-REC-003).

## 2. Diagnosis

### 2.1 Progress checks

The diagnosis engine evaluates every running attempt every `check_interval` (default 15 s), and node-wide rules every 60 s. Findings are deduplicated by `(kind, subject)`.

Finding lifecycle (state machine `SM-FINDING`): `OPEN` → `ACKNOWLEDGED` | `RESOLVED` | `AUTO_RESOLVED` | `MUTED`. A finding resolves automatically when its condition clears for 2 checks.

### 2.2 Finding catalogue

| Kind | Detection | Severity | Recommended actions (default handling) |
|---|---|---|---|
| `STALL` | `IDLE_NO_PROGRESS` longer than `stall_threshold` (default 5 min; adapter overrides, for example dotnet test 10 min). Services are excluded unless readiness was lost. | warning → error after 3× | Collect a tree snapshot (auto); notify (auto); cancel (approval); retry (approval, retryable only) |
| `QUEUE_STARVATION` | Queued longer than 2 × starvation bound | warning | Notify; suggest a priority or pool change |
| `OVERSUBSCRIBED` | CPU demand > 2 × `B_cpu` for 5 min | info | Suggest lower parallelism (shows the policy edit) |
| `MEMORY_PRESSURE` | Pressure level ≥ Pressure ([03](03-resource-control.md) §7) | warning | Automatic pressure actions per policy; notify |
| `OOM_KILLED` | `memory.events` oom_kill increased, or the Windows commit-limit notification with failure | error | Suggest a higher ceiling; retry with more memory (auto for PURE/IDEMPOTENT if policy allows) |
| `REPEATED_WORK` | §1.3 | info | Notify; suggest result caching or skipping |
| `STALE_WORK` | §1.3 | warning | Cancel (approval); notify |
| `PER_TASK_RESTORE` | [05](05-toolchains-caches.md) §7 | info | Suggest removing the override; cleanup plan (approval) |
| `CACHE_MISS_STORM` | sccache/ccache miss rate > 80% over 50 compilations in a workspace with a warm cache | info | Explain compatibility-key changes; suggest a configuration check |
| `CACHE_CORRUPT` | Adapter failure classifier | error | Clear affected entries (approval) |
| `DISK_PRESSURE` | Volume free < 10% or < 5 GiB | warning → error at < 2 GiB | Create a cleanup plan (auto); execute (approval) |
| `QUOTA_EXCEEDED` | [06](06-storage-workspaces.md) §5 | warning | Cleanup plan; quota change |
| `UNMANAGED_HEAVY` | `BYPASSED` processes in an agent session ([03](03-resource-control.md) §9) | warning | Suggest enabling routing; show coverage |
| `BYPASSED_COMMAND` | A hook saw a heavy command run without routing (observe mode) | info | Same as above |
| `ESCAPED_PROCESS` | [03](03-resource-control.md) §9 | warning | Terminate (approval) |
| `TERMINATION_INCOMPLETE` | [04](04-execution.md) §6 | error | Terminate PIDs (approval); notify |
| `LEFTOVER_PROCESSES` | The same command fingerprint left processes behind after its root exited in 3 of its last 5 attempts ([04](04-execution.md) §3) | info | Explain which processes; suggest a shared service or `kind=SERVICE` |
| `DEAD_EXECUTION` | Attempt running, container empty, no exit captured | error | Finalize as `LOST` (auto) |
| `SERVICE_UNREADY` | Service readiness lost for 30 s | warning | Notify; restart (approval) |
| `ENFORCEMENT_DEGRADED` | Capabilities changed for the worse | error | Notify; show the reason and remedy (for example enable systemd) |
| `INTEGRATION_DEGRADED` | Hooks disabled or untrusted, probe failed, MCP server not configured | warning | Notify; re-run probe; open the integration page |
| `GUEST_LINK_LOST` | WSL link down for 30 s | warning | Re-link (auto, bounded backoff); notify |
| `PEER_UNREACHABLE` | Paired peer offline while it holds attempts | warning | Wait for the lease; mark LOST at lease end (auto) |
| `UPDATE_FAILED` | Health check failed and rolled back | error | Notify; keep the previous version |

### 2.3 Remedies and automation boundaries

Policy `diagnosis.actions` maps each `(finding kind, action)` to `AUTO`, `APPROVAL` or `NOTIFY_ONLY` (R-DIAG-003). The default table is the one above.
- **Approval-only actions:** destructive or side-effecting actions (cancel, terminate, cleanup execution, retry of a non-retryable task, policy change) stay `APPROVAL`, unless the user changes them explicitly. Agents cannot change this table without approval (AD-0007 §8).
- `ApplyRemedy` runs the same public operations a user would run (for example `CancelTask`), with the finding as provenance, and journals the result.

### 2.4 Doctor

`DiagnosisService.RunDoctor` and `arcforges doctor` run the following checks and return pass, warn or fail with remedies (R-DIAG-004):
- node health (store integrity, lock, endpoint);
- enforcement self-test per resource;
- guest links (WSL: systemd present, user delegation, controllers, bridge reachable);
- storage (free space, quotas, untracked directories);
- caches (sizes, configuration);
- integrations (configuration present, hooks trusted or enabled, probe result per client);
- account and entitlement state;
- update state;
- LAN (listener, certificate validity, peers).

## 3. Operational memory

### 3.1 Facts

| Kind | Value | Used by |
|---|---|---|
| `DURATION` | count, mean, p50, p90, min, max (seconds) | ETAs, stall thresholds, placement scoring |
| `PEAK_MEMORY` | p50, p90, max (bytes) | Admission estimates ([03](03-resource-control.md) §3) |
| `CPU_PROFILE` | mean and p90 millicores | Admission estimates, parallelism |
| `PHASE_PROFILE` | share of time by category | Diagnosis baselines |
| `FAILURE_SIGNATURE` | normalized output pattern → classification, count | Failure classification, transient retry decisions |
| `CACHE_BEHAVIOR` | hit rate per cache and workspace | Cache diagnosis |

**Scope key:**
- `project_id` (repository identity hash, or path hash for non-git);
- `environment` (node ID, or `os/arch` for portable facts);
- `toolchain` (identity and version);
- `command_fingerprint`: tool, operation and significant arguments such as the target project or solution and configuration, with volatile arguments removed.

Restore-related facts add `input_key`, the digest of lock files (`packages.lock.json`, `Cargo.lock`, `package-lock.json`). Facts store normalized, redacted fingerprints, never raw command lines or environment values (R-MEM-001).

### 3.2 Learning and staleness

- **Update.** Each successful or failed attempt updates the matching facts. Statistics use a reservoir of the last 50 observations.
- **Validity:**
  - A changed toolchain version or input key creates a new fact. The old fact becomes `SUPERSEDED`.
  - A fact not observed for `ttl_days` (default 30) becomes `STALE`.
- **Use.**
  - Only `ACTIVE` facts with confidence ≥ MEDIUM (n ≥ 3) feed admission. Confidence is HIGH at n ≥ 10 with a coefficient of variation < 0.5.
  - Stale facts are shown with a stale label and are never used silently (R-MEM-002).
  - The first observation after staleness revalidates: the fact resets to the new reservoir if the values differ by more than 50%.
- **Control.** `MemoryService.ListFacts`, `GetFact`, `ForgetFact` (one fact or a scope prefix) and `QueryFacts` (MCP `memory_query`) (R-MEM-003).
