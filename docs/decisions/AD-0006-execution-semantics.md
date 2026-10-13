# AD-0006 — Execution semantics: durability, retries, pause and caching

- Status: Accepted (2026-10-12; revised 2026-10-13 after the findings review: retry-safety assertion sources, caller hand-off and joined resubmissions)
- References: Pueue design (V-T05) for queue and persisted-log patterns; independent C# implementation.

## Decision

1. **Persist before acknowledging.** `SubmitTask` commits the task to the node store (SQLite WAL) before returning its receipt. A crash after the receipt never loses the task.
   - The full execution input persists with it, including the values of secret-shaped environment variables.
   - Those values are sealed with AES-256-GCM under a node data key held in the OS secret store, and purged after the task is terminal and the retry window has passed ([04](../architecture/04-execution.md) §2).
   - Records only ever show them as present (R-EXE-017).
2. **Survive node restarts.**
   - Managed processes write stdout and stderr to node-owned files under `logs/<attempt_id>/`, never to pipes held by the node.
   - Process containers are named Windows jobs, or transient systemd user units on Linux whose processes are children of the user manager, not of the node (AD-0005).
   - Exit status and accounting are recorded durably by a helper outside the node: the attempt's holder (`exec-wrap`) on Windows, which also keeps the job openable by name, and the unit's `ExecStopPost` on Linux (AD-0005).
   - A restarted node re-attaches: it re-opens jobs or cgroups listed in the store, tails logs from the stored offsets, and records a `node_gap` segment for the downtime (R-EXE-008, R-EXE-018).
3. **Machine reboot.** The store records the boot identity (Windows: last boot time with machine identity; Linux: `/proc/sys/kernel/random/boot_id`). On startup, attempts that were running under a different boot become `LOST` with evidence (R-EXE-009).
4. **Side-effect classes and retry rules:**

| Class | Meaning | Automatic retry | Result caching | Default for |
|---|---|---|---|---|
| `PURE` | Output determined by declared inputs; no external effect | Yes (policy max, default 2) | Optional, opt-in with declared inputs and outputs | Only by assertion (below) |
| `IDEMPOTENT` | May be repeated safely | Yes (default 2) | No | Only by assertion (below), or adapter-asserted operations whose tool guarantees no project code runs (`cargo fetch`, `git fetch`, `npm ci --ignore-scripts`) |
| `SIDE_EFFECTING` | External effects | Never | No | Declared by caller |
| `UNKNOWN` | Not classified | Never; an unknown effect is reported | No | **Every command by default**, including builds, tests and installs, whose project scripts can have external effects |

   **Who may assert a class** (`ManagedTask.side_effect_source`):
   - **The caller**, through `TaskSpec.side_effect`: HUMAN and SCRIPT callers always; AGENT callers only when the policy `retry_safety.accept_agent_assertions` is true (default false). Otherwise an agent's `PURE` or `IDEMPOTENT` becomes `UNKNOWN` with a warning.
   - **A `retry_safety` rule**: a HUMAN-edited pattern per workspace or global, for example "`dotnet build` in this repository is IDEMPOTENT".
   - **An adapter**, only for what it can verify ([05](../architecture/05-toolchains-caches.md) §2). Otherwise it records a *suggestion*, which the UI offers as a one-click rule, never as an automatic retry.

   An infrastructure failure **before the process started** (spawn failure, placement failure, transfer failure) may be retried for every class. An out-of-memory kill may be retried with a larger memory grant only for `PURE` and `IDEMPOTENT` tasks.
5. **Pause and resume.** Linux uses the unit freezer (`FreezeUnit`, i.e. `cgroup.freeze`) for tasks marked `pausable` (default: true for adapter-classified build/test work, false otherwise). Windows reports unsupported. Pausing never frees memory; it only stops CPU use.
6. **Long-running tasks** (`kind=SERVICE`) have no default timeout. They support readiness conditions (output regex, TCP listen on localhost port, or a file appearing) and stop with their owner session, unless `detach=true`.
7. **Interactive attach.** `run --attach` streams output and forwards stdin while attached.
   - **Detaching** never stops the task, except for tasks submitted with `cancel_when_caller_gone`.
   - **Hand-off before a client timeout.** A hook-rewritten run knows the client's tool timeout. Shortly before it (`routing.handoff_margin_ms`, default 15 s), if the task has not finished, the CLI calls `TaskService.ReleaseCallerBinding`, prints the task ID with how to wait for it, and exits with code 124. The task keeps its place in the queue and keeps running ([08](../architecture/08-ai-integration.md) §4.1). A task is therefore never cancelled because it was queued or slow, and never requeued at the back.
   - **Interrupts still cancel.** If the caller disappears *before* the hand-off (the user interrupted the client), the binding cancels the task within 5 s, as the original command would have stopped.
   - **No duplicates.** Rewritten runs submit with `join_existing`: a resubmission of the same command, working directory and environment by the same session joins the non-terminal task instead of queueing a second copy.
   - **Restart:** stdin forwarding does not survive a node restart, and the task then sees end-of-file (documented).
8. **Result caching (opt-in, `PURE` only).**
   - The action key is the digest of the normalized argv, declared environment subset, toolchain identity, working-directory-relative input manifest digests and the platform.
   - Outputs are stored in the node's content-addressed store. A hit restores the declared outputs and replays recorded output.
   - A restore is recorded as an attempt of kind `CACHE_RESTORE` with `termination_reason=CACHE_RESTORED`, never as an execution.
   - Policy `result_cache` sets the mode per workspace: `OFF` (default), `OBSERVE` (records would-be hits without restoring) or `RESTORE` ([04](../architecture/04-execution.md) §11).
9. **Idempotent operations.** Submit, cancel, retry, priority change, policy change and cleanup are idempotent by `command_id` (24 h). Replays return the original receipt.
