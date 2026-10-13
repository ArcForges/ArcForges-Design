# 04 — Execution

## 1. Task specification

Defined by `arcforges.node.v1.TaskSpec` ([contracts](../contracts/proto/arcforges/node/v1/tasks.proto)). Validation runs in the Api layer before the command is accepted. A violation returns `ERROR_CATEGORY_VALIDATION`, with `code` naming the field and `effect=DID_NOT_HAPPEN`.

| Field | Rules |
|---|---|
| `command.argv` *or* `command.shell` | Exactly one. `argv` has 1–4,096 elements and ≤1 MiB total. `shell.script` is ≤1 MiB, and `shell.kind` is one of `CMD`, `POWERSHELL`, `PWSH`, `BASH`, `SH`, `SYSTEM_DEFAULT`, with an optional `shell_path` |
| `working_directory` | Absolute, existing directory on the executing node. Clients resolve relative paths before submitting. |
| `environment` | `inherit` = `NONE`, `CALLER` or `NODE`. `set` holds ≤4,096 entries; names cannot be empty or contain `=` (or a leading `=` on Windows). `unset` names list. |
| `stdin` | `NONE`, `BYTES` (≤1 MiB), `FILE` (absolute path) or `STREAM` (requires an attached caller) |
| `timeout` | Optional wall-clock duration (1 s – 30 days). `cpu_time_limit` is optional. `SERVICE` tasks default to no timeout. |
| `priority` | `INTERACTIVE`, `HIGH`, `NORMAL` (default), `LOW` or `BACKGROUND`. `INTERACTIVE` is allowed only from human surfaces (CLI and Desktop), or by a policy grant for a session. |
| `pool` | Existing pool name (default `default`; agent sessions default to `agents`) |
| `kind` | `COMMAND` (default) or `SERVICE`, with a readiness condition |
| `side_effect` | `PURE`, `IDEMPOTENT`, `SIDE_EFFECTING` or `UNKNOWN` (default). Adapters only suggest a class unless they can verify it; a caller (an AGENT only when policy allows) or a `retry_safety` rule asserts it ([AD-0006](../decisions/AD-0006-execution-semantics.md) §4). The task records the source. |
| `retry` | `max_attempts` (≤5) and `backoff`. Effective only per [AD-0006](../decisions/AD-0006-execution-semantics.md) §4. |
| `depends_on` | ≤64 entries of `{task_id, condition}`. Referenced tasks must exist; cycles are refused. |
| `placement` | `LOCAL_ONLY` (default), `ANY`, or a specific node, plus required toolchains, OS, architecture and labels. Remote placement needs `inputs`; declared outputs return with `output_conflict` (default `STAGE`, [09](09-lan.md) §6). |
| `concurrency` | Optional `exclusive_keys` (≤16) and `access` (`SHARED` or `EXCLUSIVE`). Adapter keys are added; the workspace's concurrency mode applies ([03](03-resource-control.md) §4). |
| `resources` | Optional hint `{cpu_demand, mem_expected, mem_ceiling}`, `require_enforcement`, `preemptible`, `pausable` |
| `labels` | ≤32 key/value pairs. Keys ≤64 characters, values ≤256. |
| `title` | ≤200 characters, shown in UIs. It may leave the node as D1 data. Defaults to a redacted command summary. |
| `owner` | Set by the node from the connection: client kind, session, agent and user. Never caller-asserted. |
| `workspace_id` | Optional. Otherwise derived by longest-prefix match of `working_directory` against registered workspaces. |
| `output` | `capture` = `FILES` (default) or `DISCARD`; retention override |

## 2. Command resolution

1. **Executable lookup (argv mode).**
   - Windows: search `PATH` from the resolved environment with `PATHEXT`, after the working directory (current-directory search disabled, as with `NoDefaultCurrentDirectoryInExePath`).
   - Linux: `execvp` semantics against the resolved `PATH`.
2. **Windows command line.** Built from `argv` with the quoting rules inverse to `CommandLineToArgvW` (backslash and quote handling). If `argv[0]` resolves to `.bat` or `.cmd`, the node invokes `cmd.exe /d /s /c` and applies cmd-safe escaping. **Any argument that cannot be represented safely** (unbalanced quotes with metacharacters `% ! ^ & | < >` or line breaks) is refused with `VALIDATION/unsafe_batch_argument`, the class of risk behind CVE-2024-24576.
3. **Shell mode.**
   - Windows `SYSTEM_DEFAULT` = `PWSH` if detected, otherwise `POWERSHELL`. `BASH` resolves to Git for Windows bash when detected (the shell AI clients typically use on Windows), otherwise it is refused.
   - Linux `SYSTEM_DEFAULT` = `SH`.
   - A script over 8,000 characters (CMD) or 30,000 characters (others) is written to `tmp/<attempt>/command.<ext>` and executed as a file.
4. **Environment resolution order:** inherit base → `unset` → `set` → adapter redirections ([05](05-toolchains-caches.md)) → ArcForges variables (`ARCFORGES_TASK_ID`, `ARCFORGES_ATTEMPT_ID`, `ARCFORGES_NODE_ID`, `ARCFORGES_SESSION` where an owner session exists). Names matching secret patterns (policy `privacy.secret_name_patterns`; defaults include `*TOKEN*`, `*SECRET*`, `*PASSWORD*`, `*PASSWD*`, `*_KEY`, `*APIKEY*`, `AWS_*`, `AZURE_*`, `GH_*`, `GITHUB_TOKEN` and `NPM_TOKEN`) are handled in two places:
   - **Records** (task views, exports, support bundles) show them as presence only (R-EXE-017).
   - **Execution state** keeps their values **sealed** until they are no longer needed, so queued tasks, restarts and retries run with the submitted environment:
     - the values are encrypted with AES-256-GCM under a node data key kept in the OS secret store, and stored in `task_secret`;
     - they are purged when the task reaches a terminal state and `storage.secret_retention_hours` (default 24) has passed, or on `PurgeTaskRecord`.

     A manual `RetryTask` after the purge fails with `STATE/secrets_unavailable` and asks for a new submission. Non-secret environment snapshots are content-addressed (`env_snapshot`), so identical environments are stored once.

## 3. Launch

| Step | Windows | Linux |
|---|---|---|
| Container | The node creates the named child job under the root job ([03](03-resource-control.md) §5) and starts the holder `arcforges node exec-wrap` **outside** the job, passing inheritable handles to the child job, the root job, the output files and the ack event ([AD-0005](../decisions/AD-0005-resource-enforcement.md) Windows §3) | `StartTransientUnit("arcforges-a-<attempt>.service", "fail", properties)` in `arcforges.slice`, with the limits of [03](03-resource-control.md) §5. The node waits for the job's `JobRemoved` signal (result `done`) before recording `STARTED`. |
| Output | Create `logs/<attempt>/stdout.bin` and `stderr.bin` (share read/write) as inheritable handles; restrict inheritance with `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` | Opened by the node with `O_APPEND` and passed as `StandardOutputFileDescriptor` / `StandardErrorFileDescriptor` unit properties (file descriptors over D-Bus) |
| stdin | NUL / temp file / file / pipe | `/dev/null` / file / pipe, passed as `StandardInputFileDescriptor` |
| Process | The holder calls `CreateProcessW(..., CREATE_SUSPENDED \| CREATE_NEW_PROCESS_GROUP \| CREATE_UNICODE_ENVIRONMENT \| EXTENDED_STARTUPINFO_PRESENT, ...)` with a windowless console (`CREATE_NO_WINDOW`: a console without a window, which a helper can attach to; L-18) for console programs → `AssignProcessToJobObject(root job)` → `AssignProcessToJobObject(child job)`, which nests the child job under the root → `ResumeThread`, and reports the PID and start time to the node. `kill_with_node` tasks skip the holder: the node launches them itself into a job with kill-on-close. | Unit properties: `ExecStart` (resolved absolute program path and argv), `WorkingDirectory`, the exact environment (`Environment` plus `UnsetEnvironment` for every manager variable outside the resolved set), the caller's relevant rlimits as `Limit*`, and `BindsTo=arcforges-node.service` only for `kill_with_node` tasks. The user manager forks and execs the process inside the unit's cgroup, so no child ever runs outside its container. |
| Launch steps | Adapter launch steps (for example the attempt's sccache server, [05](05-toolchains-caches.md) §5) run in the attempt's jobs before the root process is resumed; the holder waits for them. If a step fails, the holder terminates the job and records `SPAWN_FAILED` with the step's error. | `ExecStart` is `arcforges node exec-launch --attempt <id> -- <command>`: it runs the launch steps inside the unit's cgroup, then replaces itself with the command (`execve`), so the command is the unit's main process. If a step fails, `exec-launch` writes `logs/<attempt>/launch.json` and exits, and `exit-record` records `SPAWN_FAILED` with the step's error. |
| End steps | After the root process exits, the holder runs the adapter's end steps (for example sccache statistics and stop), bounded to 10 s, before leftover termination | `ExecStop=-<app>/current/arcforges node exec-stop --attempt <id>` runs them; systemd runs it when the main process exits on its own, before it stops the remaining processes. The `-` keeps a failing end step from changing the unit's result, `TimeoutStopSec` covers the end-step budget (10 s) plus `leftover_grace`, and `exit-record` takes the command's result from `$EXIT_CODE` and `$EXIT_STATUS`. |
| Disk guard | The holder is the attempt's guard while the node is down ([06](06-storage-workspaces.md) §5). | `arcforges-guard.service` guards every attempt unit while the node is down (06 §5). |
| Exit capture | The holder waits for the root process. After `leftover_grace` it terminates leftovers, then writes `logs/<attempt>/exit.json` with the exit code and the job accounting: basic and I/O accounting, peak job commit, and limit violations from `JobObjectLimitViolationInformation`. It keeps the job handles until the node sets the ack event. The node receives the same events from the job's completion port while it runs. | While the node runs: D-Bus `PropertiesChanged` on the unit (`ExecMainCode`, `ExecMainStatus`, `Result`). Durable: `logs/<attempt>/exit.json`, written by `ExecStopPost=<app>/current/arcforges node exit-record --attempt <id>`, which systemd runs with `$EXIT_CODE`, `$EXIT_STATUS` and `$SERVICE_RESULT` even when the node is down (L-13). |

**Process tree tracking.** Container membership is authoritative (`JobObjectBasicProcessIdList` / the unit's `cgroup.procs`). An ancestry scan every 5 s detects `ESCAPED` descendants ([03](03-resource-control.md) §9).

**Root exit and leftover processes.** The attempt's result is fixed when its root process exits. Processes still in the container after that are terminated with the forced phase of §6 after `leftover_grace` (default 5 s).
- **Linux:** the unit's own stop, with `KillMode=control-group` and `TimeoutStopSec` = the end-step budget plus `leftover_grace`.
- **Windows:** the holder (or the node, for `kill_with_node` tasks) calls `TerminateJobObject` on the child job.

The record lists the terminated leftovers (image names and counts). Repeated leftovers raise the finding `LEFTOVER_PROCESSES`. Long-lived helpers belong in `kind=SERVICE` tasks. Compiler servers run per attempt and stop with it ([05](05-toolchains-caches.md) §5).

**Compatibility of the helper roles.** `exit-record`, `exec-wrap`, `exec-launch`, `exec-stop` and `node guard` are invoked by path through `app/current`, so after an update they may run a newer binary than the node that launched the attempt. Their arguments and the formats of `exit.json`, `launch.json`, `guard.json`, `guard-events.jsonl` and the heartbeat are therefore a stable internal contract, with additive changes only. The format (schema 1):

```json
{"schema": 1, "attempt_id": "<base32>", "exit_code_kind": "exited|killed|dumped", "exit_status": 0,
 "service_result": "success|exit-code|signal|oom-kill|timeout", "recorded_at": "<RFC 3339>",
 "cpu_user_ms": 0, "cpu_kernel_ms": 0, "mem_peak_bytes": 0, "io_read_bytes": 0, "io_write_bytes": 0,
 "oom_kills": 0, "limit_violations": ["job_memory", "cpu_time"], "leftovers_terminated": ["image.exe"]}
```

On Linux, `exit-record` reads `cpu.stat`, `memory.peak`, `memory.events` and `io.stat` of its own unit cgroup, in which `ExecStopPost` runs.

## 4. Output capture and streaming

- Each attempt has the files `stdout.bin`, `stderr.bin` and `index.bin`.
- The node's tailer reads new bytes every 100 ms, or on change notification, and appends index records `{stream:u8, offset:u64, length:u32, unix_nanos:i64, flags:u8}`.
  - Chunks written while the node was down receive the re-attach time with flag `APPROXIMATE_TIME`.
  - The merged, ordered view interleaves the two streams by index order.
- `ReadTaskOutput(attempt, stream, from_offset, max_bytes ≤ 4 MiB)` returns bytes plus index records. `WatchTaskOutput` streams new chunks (≤64 KiB per frame) after an optional backfill.
- Throughput target: ≥200 MB/s capture without loss (R-PERF-001). The process writes the files directly, so capture never back-pressures the process.
- **Output limit.** Because the process writes the files directly, the node cannot cap them at the file system. The tailer compares the two files' size with `storage.max_attempt_output_bytes` (default 2 GiB) on every read (100 ms). On crossing it, `disk_limit_action` applies: `TERMINATE` (default) stops the attempt at once, without the graceful phase (§6), with `termination_reason=OUTPUT_LIMIT`; `NOTIFY` raises a finding and lets the attempt continue, and the output is kept, because the process writes the files itself. The overshoot is bounded by the write rate over one tailer interval plus the stop latency ([06](06-storage-workspaces.md) §5). While the node is down, the attempt's guard checks the files at the same interval, and the bound grows by the takeover delay (06 §5, attempt guards).
- Retention: output is kept for the record retention period (default 14 days or 5 GiB total, oldest first; pinned tasks excepted). Compression with gzip happens after 24 h for files larger than 1 MiB.

## 5. Attach (`AttachTask`)

A server stream delivers the state, output chunks, progress, readiness and the final result. While attached, the caller may send stdin chunks with `WriteTaskInput` and close with `CloseTaskInput`.
- Detaching never affects the task.
- `arcforges run` (attached by default) mirrors stdout to stdout and stderr to stderr byte-exactly, and exits with the task's exit code. A signal or termination maps to exit codes 128 + n on Linux, and to 1 plus a message on stderr on Windows. The CLI also exits with code 75 when the node was unreachable and nothing ran (`EX_TEMPFAIL`, effect `DID_NOT_HAPPEN`).

## 6. Cancellation, timeouts and termination

1. **Graceful phase.**
   - Windows (L-18):
     - The holder started the root process with `CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP`, so it has a windowless console and its PID is its process-group ID.
     - The `arcforges node signal` helper is started without a console of its own. It calls `FreeConsole`, then `AttachConsole(root pid)`, ignores control events itself (`SetConsoleCtrlHandler(NULL, TRUE)`), and calls `GenerateConsoleCtrlEvent(CTRL_BREAK_EVENT, root pid)`. One helper process serves one attempt, because a process can attach to one console at a time.
     - Descendants that created their own console or process group, and GUI processes, do not receive the event. GUI processes in the tree get `WM_CLOSE` on their top-level windows.
     - If the attach or the event fails (the root process has exited, or it is not a console program), the node records the reason and goes straight to the grace period. The forced phase (step 3) ends the whole job either way.
   - Linux: `KillUnit("all", SIGTERM)` (or the task's `stop_signal`), which signals every process in the unit's cgroup.
2. **Grace period:** `cancel_grace` (default 10 s, policy maximum 300 s).
3. **Forced phase:** `TerminateJobObject` / `KillUnit("all", SIGKILL)` (the user manager uses `cgroup.kill` where the kernel supports it).
4. **Limit stops** (`OUTPUT_LIMIT`, `DISK_LIMIT`, `ENDPOINT_TAKEN`, and Critical memory or disk pressure) skip the graceful phase, because the process would keep writing or allocating during the grace period: on Linux the unit is frozen at once and then killed; on Windows the job is terminated at once.
4. **Escaped descendants:** terminated if same-user and policy `terminate_escaped=true` (default true for cancellation, false for node shutdown).
5. **Verification:** the container must report zero processes within 5 s. Otherwise the attempt is marked `TERMINATION_INCOMPLETE` with the PIDs left, and a finding is raised (R-EXE-006).

Timeouts and CPU-time limits run the same sequence with the reason `TIMED_OUT` / `CPU_TIME_EXCEEDED`. CPU time on Windows uses `PerJobUserTimeLimit` where it applies, otherwise accounting polling; on Linux, `cpu.stat` polling.

## 7. Exit normalization

`AttemptResult` holds:
- `exit_code` (int32);
- `signal` (Linux number, plus `core_dumped`);
- `windows_status` (NTSTATUS when the exit code is an exception code ≥ 0xC0000000);
- `termination_reason`: `EXITED`, `CANCELLED`, `TIMED_OUT`, `CPU_TIME_EXCEEDED`, `OOM_KILLED` (Linux: `memory.events` oom_kill increased, or `SERVICE_RESULT=oom-kill`), `MEMORY_LIMIT` (Windows commit-limit notification observed and exit ≠ 0), `PREEMPTED`, `LOST`, `SPAWN_FAILED`, `NODE_SHUTDOWN`, `POLICY_DENIED`, `TERMINATION_INCOMPLETE`, `CACHE_RESTORED` (result-cache restore; never an execution), `OUTPUT_LIMIT` (§4), `DISK_LIMIT` (per-attempt temporary space, or critical free space on a written volume; [06](06-storage-workspaces.md) §5) or `ENDPOINT_TAKEN` (another process listened on the attempt's own sccache endpoint, or took the cache store's port; [05](05-toolchains-caches.md) §5);
- `effect`: `DID_NOT_HAPPEN` only for `SPAWN_FAILED` and `POLICY_DENIED`; `HAPPENED` for completed processes; `UNKNOWN` for `LOST`.

## 8. Dependencies, services, retries

- **Dependencies:** a task with unmet dependencies is `WAITING_DEPENDENCY`. If a `SUCCEEDED`-condition dependency fails or is cancelled, the dependent becomes `CANCELLED` with reason `dependency_failed`.
- **Services:**
  - Readiness conditions: `output_regex` (RE2-compatible subset, matched on either stream), `tcp_listen` (127.0.0.1 or ::1 port) or `file_exists`, with `readiness_timeout` (default 120 s).
  - State `RUNNING` with `ready=true` after the condition holds. A service stops with its owner session when `stop_with_session=true` (default for agent-owned services).
- **Retries:** a new attempt with backoff `5 s × 2^n` (cap 60 s), only per [AD-0006](../decisions/AD-0006-execution-semantics.md) §4: the class must be asserted by the caller, a `retry_safety` rule or a verifying adapter. A suggested class alone never retries. Every attempt keeps its own records.

## 9. Restart recovery and LOST

See [02](02-node-service.md) §2 step 5.
- **Windows.** The attempt's holder keeps the child and root jobs open, so the restarted node re-opens them by name. It re-associates its completion port (clear, then attach; L-15), reads accounting and limit violations, and can cancel, limit or account the attempt as before. After the node records a finished attempt, it sets the attempt's ack event and the holder exits.
- **Linux.** The node finds the unit by name, reads its state and cgroup files, and reads `exit.json` for attempts that finished while it was down.
- Attempts recovered after a node restart get a `node_gap` timeline segment.
- Attempts whose container vanished, or whose boot identity changed, become `LOST` with evidence `{boot_id_old, boot_id_new}` or `{container_missing}`.
- A `LOST` attempt of a retryable task schedules a retry. Others wait for a user or agent decision (`RetryTask`).

## 10. Adoption

`ResourceService.AdoptProcess(pid, start_time)`:
1. Same-user check.
2. Windows: a process already in any job (`IsProcessInJob`) is refused with `adopt_not_permitted`, because joining it would attach the ArcForges hierarchy to a foreign job. Otherwise the node assigns it to the root job and then to a new adoption job, which nests the adoption job under the root (V-W01). Linux: `StartTransientUnit("arcforges-x-<id>.scope", PIDs=[pid])` in `arcforges.slice`. The user manager can move only processes inside its own subtree (V-L01), so processes elsewhere (login-session scopes, WSL `/non-systemd`) are refused with `adopt_not_permitted`.
3. Children existing at adoption time are adopted individually (best effort, with each result recorded). Later children follow the container.

Adoption creates a synthetic task (`kind=ADOPTED`) so the process appears in all surfaces (R-RES-013).

## 11. Result caching (opt-in)

Per [AD-0006](../decisions/AD-0006-execution-semantics.md) §8. The action key is SHA-256 over:
- the canonical argv, or the script digest;
- `PATH`-resolved executable digests;
- the declared environment subset;
- toolchain identities;
- the input manifest digest (declared input globs relative to the workspace);
- OS and architecture.

Policy `result_cache` sets a mode per workspace: `OFF` (default) or `OBSERVE`. In `OBSERVE`, each finished attempt of a task with declared outputs records its action key and the digest of its output manifest in `result_cache_observation`, and an observation whose key matches an earlier successful one with the same output digest counts as a would-be hit. `CacheService.GetCacheReport` reports observations and would-be hits: the evidence for when restores would pay off. Output blobs are not stored for restores in release 1. `RESTORE` is accepted future work (roadmap RM-04), and policy validation refuses it in release 1. When it arrives, declared outputs are stored in the CAS (`cache/cas/`), and a restore produces an attempt of kind `CACHE_RESTORE` with `termination_reason=CACHE_RESTORED`, the recorded exit code and output replay; it is never shown as an execution, and it runs only for `PURE` tasks (AD-0006 §8).
