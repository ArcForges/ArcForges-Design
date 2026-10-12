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
| `side_effect` | `PURE`, `IDEMPOTENT`, `SIDE_EFFECTING` or `UNKNOWN` (default). Adapters may propose a class, but only the caller or an adapter rule with `assert_class=true` sets `PURE`. |
| `retry` | `max_attempts` (≤5) and `backoff`. Effective only per [AD-0006](../decisions/AD-0006-execution-semantics.md) §4. |
| `depends_on` | ≤64 entries of `{task_id, condition}`. Referenced tasks must exist; cycles are refused. |
| `placement` | `LOCAL_ONLY` (default), `ANY`, or a specific node, plus required toolchains, OS, architecture and labels. |
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
4. **Environment resolution order:** inherit base → `unset` → `set` → adapter redirections ([05](05-toolchains-caches.md)) → ArcForges variables (`ARCFORGES_TASK_ID`, `ARCFORGES_ATTEMPT_ID`, `ARCFORGES_NODE_ID`, `ARCFORGES_SESSION` where an owner session exists). Names matching secret patterns are stored as presence-only (`set` without value) in records (R-EXE-017). Patterns are policy `privacy.secret_name_patterns`; defaults include `*TOKEN*`, `*SECRET*`, `*PASSWORD*`, `*PASSWD*`, `*_KEY`, `*APIKEY*`, `AWS_*`, `AZURE_*`, `GH_*`, `GITHUB_TOKEN` and `NPM_TOKEN`.

## 3. Launch

| Step | Windows | Linux |
|---|---|---|
| Container | Create the named child job under the root job ([03](03-resource-control.md) §5) | `StartTransientUnit("arcforges-a-<attempt>.service", "fail", properties)` in `arcforges.slice`, with the limits of [03](03-resource-control.md) §5. The node waits for the job's `JobRemoved` signal (result `done`) before recording `STARTED`. |
| Output | Create `logs/<attempt>/stdout.bin` and `stderr.bin` (share read/write) as inheritable handles; restrict inheritance with `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` | Opened by the node with `O_APPEND` and passed as `StandardOutputFileDescriptor` / `StandardErrorFileDescriptor` unit properties (file descriptors over D-Bus) |
| stdin | NUL / temp file / file / pipe | `/dev/null` / file / pipe, passed as `StandardInputFileDescriptor` |
| Process | `CreateProcessW(..., CREATE_SUSPENDED \| CREATE_NEW_PROCESS_GROUP \| CREATE_UNICODE_ENVIRONMENT \| EXTENDED_STARTUPINFO_PRESENT, ...)` with a hidden console (`CREATE_NO_WINDOW`) for console programs → `AssignProcessToJobObject` → `ResumeThread` | Unit properties: `ExecStart` (resolved absolute program path and argv), `WorkingDirectory`, the exact environment (`Environment` plus `UnsetEnvironment` for every manager variable outside the resolved set), the caller's relevant rlimits as `Limit*`, and `BindsTo=arcforges-node.service` only for `kill_with_node` tasks. The user manager forks and execs the process inside the unit's cgroup, so no child ever runs outside its container. |
| Exit capture | The node waits on the root process handle. After a node restart, exit is read from `JobObjectBasicAccountingInformation` (no active processes) plus `logs/<attempt>/exit.json`, written by a wait-thread in the `arcforges node exec-wrap` role. That role wraps Windows launches when the task opts into `survive_restart_exit_code` (default true). | While the node runs: D-Bus `PropertiesChanged` on the unit (`ExecMainCode`, `ExecMainStatus`, `Result`). Durable: `logs/<attempt>/exit.json`, written by `ExecStopPost=<app>/current/arcforges node exit-record --attempt <id>`, which systemd runs with `$EXIT_CODE`, `$EXIT_STATUS` and `$SERVICE_RESULT` even when the node is down (L-13). |

**Process tree tracking.** Container membership is authoritative (`JobObjectBasicProcessIdList` / the unit's `cgroup.procs`). An ancestry scan every 5 s detects `ESCAPED` descendants ([03](03-resource-control.md) §9).

**Root exit and leftover processes.** The attempt's result is fixed when its root process exits. Processes still in the container after that are terminated with the forced phase of §6 after `leftover_grace` (default 5 s).
- **Linux:** the unit's own stop, with `KillMode=control-group` and `TimeoutStopSec` = `leftover_grace`.
- **Windows:** the node or the `exec-wrap` role calls `TerminateJobObject` on the child job.

The record lists the terminated leftovers (image names and counts). Repeated leftovers raise the finding `LEFTOVER_PROCESSES`. Long-lived helpers belong in shared services ([05](05-toolchains-caches.md) §5) or in `kind=SERVICE` tasks.

**Compatibility of the helper roles.** `exit-record` and `exec-wrap` are invoked by path through `app/current` and may run a newer binary than the node that launched the attempt (after an update). Their arguments and the `exit.json` format are therefore a stable internal contract: `{schema: 1, attempt_id, exit_code_kind, exit_status, service_result, recorded_at}`. New fields are additive only.

## 4. Output capture and streaming

- Each attempt has the files `stdout.bin`, `stderr.bin` and `index.bin`.
- The node's tailer reads new bytes every 100 ms, or on change notification, and appends index records `{stream:u8, offset:u64, length:u32, unix_nanos:i64, flags:u8}`.
  - Chunks written while the node was down receive the re-attach time with flag `APPROXIMATE_TIME`.
  - The merged, ordered view interleaves the two streams by index order.
- `ReadTaskOutput(attempt, stream, from_offset, max_bytes ≤ 4 MiB)` returns bytes plus index records. `WatchTaskOutput` streams new chunks (≤64 KiB per frame) after an optional backfill.
- Throughput target: ≥200 MB/s capture without loss (R-PERF-001). The process writes the files directly, so capture never back-pressures the process.
- Retention: output is kept for the record retention period (default 14 days or 5 GiB total, oldest first; pinned tasks excepted). Compression with gzip happens after 24 h for files larger than 1 MiB.

## 5. Attach (`AttachTask`)

A server stream delivers the state, output chunks, progress, readiness and the final result. While attached, the caller may send stdin chunks with `WriteTaskInput` and close with `CloseTaskInput`.
- Detaching never affects the task.
- `arcforges run` (attached by default) mirrors stdout to stdout and stderr to stderr byte-exactly, and exits with the task's exit code. A signal or termination maps to exit codes 128 + n on Linux, and to 1 plus a message on stderr on Windows. The CLI also exits with code 75 when the node was unreachable and nothing ran (`EX_TEMPFAIL`, effect `DID_NOT_HAPPEN`).

## 6. Cancellation, timeouts and termination

1. **Graceful phase.**
   - Windows: the `arcforges node signal` helper role attaches to the attempt's console and sends `CTRL_BREAK_EVENT` to its process group. GUI processes in the tree get `WM_CLOSE` on their top-level windows.
   - Linux: `KillUnit("all", SIGTERM)` (or the task's `stop_signal`), which signals every process in the unit's cgroup.
2. **Grace period:** `cancel_grace` (default 10 s, policy maximum 300 s).
3. **Forced phase:** `TerminateJobObject` / `KillUnit("all", SIGKILL)` (the user manager uses `cgroup.kill` where the kernel supports it).
4. **Escaped descendants:** terminated if same-user and policy `terminate_escaped=true` (default true for cancellation, false for node shutdown).
5. **Verification:** the container must report zero processes within 5 s. Otherwise the attempt is marked `TERMINATION_INCOMPLETE` with the PIDs left, and a finding is raised (R-EXE-006).

Timeouts and CPU-time limits run the same sequence with the reason `TIMED_OUT` / `CPU_TIME_EXCEEDED`. CPU time on Windows uses `PerJobUserTimeLimit` where it applies, otherwise accounting polling; on Linux, `cpu.stat` polling.

## 7. Exit normalization

`AttemptResult` holds:
- `exit_code` (int32);
- `signal` (Linux number, plus `core_dumped`);
- `windows_status` (NTSTATUS when the exit code is an exception code ≥ 0xC0000000);
- `termination_reason`: `EXITED`, `CANCELLED`, `TIMED_OUT`, `CPU_TIME_EXCEEDED`, `OOM_KILLED` (Linux: `memory.events` oom_kill increased, or `SERVICE_RESULT=oom-kill`), `MEMORY_LIMIT` (Windows commit-limit notification observed and exit ≠ 0), `PREEMPTED`, `LOST`, `SPAWN_FAILED`, `NODE_SHUTDOWN`, `POLICY_DENIED` or `TERMINATION_INCOMPLETE`;
- `effect`: `DID_NOT_HAPPEN` only for `SPAWN_FAILED` and `POLICY_DENIED`; `HAPPENED` for completed processes; `UNKNOWN` for `LOST`.

## 8. Dependencies, services, retries

- **Dependencies:** a task with unmet dependencies is `WAITING_DEPENDENCY`. If a `SUCCEEDED`-condition dependency fails or is cancelled, the dependent becomes `CANCELLED` with reason `dependency_failed`.
- **Services:**
  - Readiness conditions: `output_regex` (RE2-compatible subset, matched on either stream), `tcp_listen` (127.0.0.1 or ::1 port) or `file_exists`, with `readiness_timeout` (default 120 s).
  - State `RUNNING` with `ready=true` after the condition holds. A service stops with its owner session when `stop_with_session=true` (default for agent-owned services).
- **Retries:** a new attempt with backoff `5 s × 2^n` (cap 60 s), only per [AD-0006](../decisions/AD-0006-execution-semantics.md) §4. Every attempt keeps its own records.

## 9. Restart recovery and LOST

See [02](02-node-service.md) §2 step 5.
- Attempts recovered after a node restart get a `node_gap` timeline segment.
- Attempts whose container vanished, or whose boot identity changed, become `LOST` with evidence `{boot_id_old, boot_id_new}` or `{container_missing}`.
- A `LOST` attempt of a retryable task schedules a retry. Others wait for a user or agent decision (`RetryTask`).

## 10. Adoption

`ResourceService.AdoptProcess(pid, start_time)`:
1. Same-user check.
2. Windows: `AssignProcessToJobObject` on a new adoption job under the root job (V-W01). Linux: `StartTransientUnit("arcforges-x-<id>.scope", PIDs=[pid])` in `arcforges.slice`. The user manager can move only processes inside its own subtree (V-L01), so processes elsewhere (login-session scopes, WSL `/non-systemd`) are refused with `adopt_not_permitted`.
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

Declared output globs are stored in the CAS (`cache/cas/`). Policy `result_cache.mode` per workspace: `OFF` (default), `OBSERVE` (record would-hit) or `RESTORE`. A restore produces an attempt with `termination_reason=EXITED`, `cache_restored=true` and recorded output replay. Restores never run for `SIDE_EFFECTING` or `UNKNOWN` tasks.
