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

     A manual `RetryTask` after the purge fails with `STATE/secrets_unavailable` and asks for a new submission.

     **A lost key fails closed.** If the node data key that sealed the values is missing from the OS secret store or cannot be read, the values are unavailable. The node never launches a task with a partial environment, `RetryTask` fails with `STATE/secrets_unavailable` (without a purge time), and new submissions are sealed under a new key version. The design relies on no consistency guarantee of the OS store under concurrent modification (L-26).

     **Production read-back policy.** Production does not read back a node data key after writing it. The key stays in memory; a lost write surfaces at the next load (node restart) and fails closed as above. Read-back and absence checks are test verification only ([16](16-testing-strategy.md) §1).

     **Same-user qualifier** (added 2026-10-19). Sealing protects the values at rest from other users and keeps them out of records. It does not protect them from the signed-in user's own processes: the OS secret store, like the Linux 0600-file fallback ([AD-0011](../decisions/AD-0011-identity-and-login.md) §4), protects the data key from other users, not from processes of the same user, and a running task's environment holds the values in clear (§3, environment visibility). Managed tasks run as that user ([11](11-security-privacy.md) §3, T-25).

     Non-secret environment snapshots are content-addressed (`env_snapshot`), so identical environments are stored once.

## 3. Launch

| Step | Windows | Linux |
|---|---|---|
| Container | The node creates the named child job under the root job ([03](03-resource-control.md) §5) and starts the holder `arcforges node exec-wrap` **outside** the job, passing inheritable handles to the child job, the root job, the output files and the ack event ([AD-0005](../decisions/AD-0005-resource-enforcement.md) Windows §3) | `StartTransientUnit("arcforges-a-<attempt>.service", "fail", properties)` in `arcforges.slice`, with the limits of [03](03-resource-control.md) §5. The node waits for the job's `JobRemoved` signal (result `done`) before recording `STARTED`. |
| Output | Create `logs/<attempt>/stdout.bin` and `stderr.bin` (share read/write) as inheritable handles; restrict inheritance with `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` | Opened by the node with `O_APPEND` and passed as `StandardOutputFileDescriptor` / `StandardErrorFileDescriptor` unit properties (file descriptors over D-Bus) |
| stdin | NUL / temp file / file / pipe | `/dev/null` / file / pipe, passed as `StandardInputFileDescriptor` |
| Process | The holder calls `CreateProcessW(..., CREATE_SUSPENDED \| CREATE_NEW_PROCESS_GROUP \| CREATE_UNICODE_ENVIRONMENT \| EXTENDED_STARTUPINFO_PRESENT, ...)` with a windowless console (`CREATE_NO_WINDOW`: a console without a window, which a helper can attach to; L-18) for console programs → `AssignProcessToJobObject(root job)` → `AssignProcessToJobObject(child job)`, which nests the child job under the root → `ResumeThread`, and reports the PID and start time to the node. `kill_with_node` tasks skip the holder: the node launches them itself into a job with kill-on-close. | Unit properties: `ExecStart` (resolved absolute program path and argv), `WorkingDirectory`, the exact environment (`Environment`; `exec-launch` keeps only the resolved names before it executes anything, so variables the user manager adds never reach the command, the launch steps or the end steps), the node's own limits as `Limit*` (`LimitCORE` and `LimitSTACK` with the node's soft and hard values; `LimitNOFILE` with the node's hard value and a soft value of min(1024, hard)), and `BindsTo=arcforges-node.service` only for `kill_with_node` tasks. The user manager forks and execs the process inside the unit's cgroup, so no child ever runs outside its container. |
| Launch steps | Adapter launch steps (for example the attempt's sccache server, [05](05-toolchains-caches.md) §5) run in the attempt's jobs before the root process is resumed; the holder waits for them. If a step fails, the holder terminates the job and records `SPAWN_FAILED` with the step's error. | `ExecStart` is `arcforges node exec-launch --attempt <id> -- <command>`: it runs the launch steps inside the unit's cgroup, then replaces itself with the command (`execve`), so the command is the unit's main process. If a step fails, `exec-launch` writes `logs/<attempt>/launch.json` and exits, and `exit-record` records `SPAWN_FAILED` with the step's error. |
| End steps | After the root process exits, the holder runs the adapter's end steps (for example sccache statistics and stop), bounded to 10 s, before leftover termination | `ExecStop=-<app>/current/arcforges node exec-stop --attempt <id>` runs them; systemd runs it when the main process exits on its own, before it stops the remaining processes, and also when it stops the unit after an OOM kill (`OOMPolicy=stop`, [L-27](../verification/platform-capabilities.md); amended 2026-10-23), when the main process may still be running: the end steps then run first, and the forced phase after `leftover_grace` also ends the main process, which the record lists among the terminated leftovers; the result stays `OOM_KILLED` (§7). The `-` keeps a failing end step from changing the unit's result. `SuccessExitStatus` lists every exit code and every signal (1–31 and SIGRTMIN–SIGRTMAX), so the end steps always run, and `exit-record` takes the command's real result from `$EXIT_CODE` and `$EXIT_STATUS`. After `leftover_grace`, `exec-stop` kills what remains with SIGKILL (the forced phase); `TimeoutStopSec` = the end-step budget (10 s) + `leftover_grace` + 5 s for `exec-stop` itself, so systemd's own stop timeout is not reached. |
| Disk guard | The holder is the attempt's guard while the node is down ([06](06-storage-workspaces.md) §5). | `arcforges-guard.service` guards every attempt unit while the node is down (06 §5). |
| Exit capture | The holder waits for the root process. After `leftover_grace` it terminates leftovers, then writes `logs/<attempt>/exit.json` with the exit code and the job accounting: basic and I/O accounting, peak job commit, and limit violations from `JobObjectLimitViolationInformation`. It keeps the job handles until the node sets the ack event. The node receives the same events from the job's completion port while it runs. | While the node runs: D-Bus `PropertiesChanged` on the unit (`ExecMainCode`, `ExecMainStatus`, `Result`). Durable: `logs/<attempt>/exit.json`, written by `ExecStopPost=<app>/current/arcforges node exit-record --attempt <id>`, which systemd runs with `$EXIT_CODE`, `$EXIT_STATUS` and `$SERVICE_RESULT` even when the node is down (L-13). Units are kept until the node has recorded them (`CollectMode=inactive`), because `exit-record` may not run to the end: in systemd's stop sequence, an OOM kill while `ExecStopPost` runs sends the unit to its final SIGKILL, which ends `exit-record` too. The node then records from the unit's properties and resets the unit. *Amended 2026-10-23* ([L-27](../verification/platform-capabilities.md)): formerly "because an OOM kill under `OOMPolicy=kill` can skip `ExecStopPost`"; under `OOMPolicy=stop` a skipped `ExecStopPost` has not been observed. |

**Environment visibility (Linux).** The resolved environment, values included, is part of the transient unit while it is loaded: `systemctl --user show` and the transient unit file under `$XDG_RUNTIME_DIR/systemd/transient/` show it to the same user, as `/proc/<pid>/environ` does. Other users cannot read it. Records, exports and the per-attempt `steps.json` (names only) carry no values (§2).

**Process tree tracking.** Container membership is authoritative (`JobObjectBasicProcessIdList` / the unit's `cgroup.procs`). An ancestry scan every 5 s detects `ESCAPED` descendants: processes outside the container whose recorded ancestry passes through a member. Launches through WMI, a broker, a service, a scheduled task or a spoofed parent are not detected and appear as `UNMANAGED` ([03](03-resource-control.md) §9; T-23; corrected 2026-10-19).

**Root exit and leftover processes.** The attempt's result is fixed when its root process exits. Processes still in the container after that are terminated with the forced phase of §6 after `leftover_grace` (default 5 s). On Linux an OOM kill also stops the unit when the root has not exited (`OOMPolicy=stop`, [L-27](../verification/platform-capabilities.md); amended 2026-10-23): a surviving root is ended with the leftovers by the same forced phase, and the result is `OOM_KILLED`.
- **Linux:** the unit's own stop, with `KillMode=control-group`: `exec-stop` kills the leftovers with SIGKILL after `leftover_grace`, and `TimeoutStopSec` = the end-step budget + `leftover_grace` + 5 s.
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
- The node's tailer reads new bytes every 100 ms, or on change notification, and appends index records (each covering at most 1 MiB; on Linux each indexed range is then dropped from the page cache, [15](15-performance-targets.md) §2) `{stream:u8, offset:u64, length:u32, unix_nanos:i64, flags:u8}`.
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
3. **Forced phase:** `TerminateJobObject` on Windows. On Linux: `FreezeUnit`, SIGKILL to every process in the unit's cgroup (the main process last), then a direct write of `0` to the cgroup's `cgroup.freeze` before `ThawUnit`. `KillUnit("all", SIGKILL)` is not used: it makes systemd skip `ExecStop` and `ExecStopPost`, so no durable exit record would be written, and while the user manager spawns `ExecStop` into a frozen cgroup, systemd 257 blocks the whole manager and systemd 255 leaves the unit deactivating with its exit record pending, until the cgroup is thawed (L-24). A starting node, and the guard while the node is down, thaw an attempt cgroup that a dead node left frozen in this state, recognised by containing nothing but processes the user manager spawned for the unit (a child of the manager that is `systemd-executor`, or an unreadable fork named `systemd` or a parenthesised name), or by being empty. A paused attempt still holds its own processes, so it stays frozen.
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

## 12. Direction (roadmap; not release 1)

Added 2026-10-19 ([AD-0017](../decisions/AD-0017-delegated-execution-direction.md), amended; [18](18-application-workload-control.md) §6, §7). §1–§11 bind release 1 unchanged. Each item is effective at RM-18 (EX-25's stage a) unless it says otherwise.

- **The application class** (a value on `SERVICE` and `COMMAND` tasks; no new execution kind) replaces each batch default of §1, §3, §4 and §6 that would harm an interactive application: standard output discarded and standard error captured with a notification instead of the terminating output limit; the user's temp, or a measured persistent temp under the Installation's state root, instead of the per-attempt temp deleted at the end; readiness `NONE`; no wall-clock timeout; a 30 s graceful stop after `WM_CLOSE` or SIGTERM; on Linux the session-environment passthrough (`DISPLAY`, `WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `DBUS_SESSION_BUS_ADDRESS`, `XDG_ACTIVATION_TOKEN`, `MEMORY_PRESSURE_WATCH`); `kill_with_node` forbidden; owner placement outside freeze and requeue.
- **`lifetime = CONTAINER`**, so that tray and single-instance applications are not cut short: one additive SM-ATTEMPT trigger, "container empty" → FINALIZING without §3's leftover kill. On Windows the holder polls job membership on a timer as well as on the job message, because the empty-job message is best effort; on Linux an `ExitType=cgroup` unit (systemd 250 and later); where that is unavailable, the attempt's lifetime stays its root process, and the card says so. No `machines.json` change before promotion.
- **Strangers.** Before a stop or a tree kill of an owner-placed application, processes in its job or unit whose executable or desktop identity does not match it are listed and, by default, moved out or put to the owner (on Windows they cannot be moved out; [18](18-application-workload-control.md) §6.2); a container lifetime ends when only detected strangers remain.
- **Adoption** (§10; effective at EX-25 stages b and c). Adoption kinds `job_attach` (Windows: identify by `(pid, creation time)`, check current commit, no lethal limit at assignment, assign, sweep descendants, read back), `unit_in_place` (Linux: the desktop's own unit, properties set at run time, prior values journaled and read back) and `scope_migrated` (only for programs without a unit, with migration's losses of charges, children and identity stated); resource fields; an optional placement field whose default keeps §10's root-first behaviour. A process adopted under the root stays there until it exits.
- **Restart policy for services** (§8; effective at EX-25 stage e). Modes `NEVER`, `ON_FAILURE`, `ALWAYS`, never for `COMMAND` or `ADOPTED`; one restart owner per Installation (ArcForges, the application, or none); backoff 5 s × 2ⁿ up to 60 s, reset after 10 healthy minutes; more than 5 ends in 10 minutes raises `RESTART_LOOP`; never after an owner cancellation; after an own-limit failure once, then the owner decides. Realized on §8's retry path, through admission, with an SM-TASK restart guard and a clean-exit trigger as amendments of the delivered machine. systemd `Restart=` and holder restarts are not used.
