# AD-0006 — Execution semantics: durability, retries, pause and caching

- Status: Accepted (2026-10-12)
- References: Pueue design (V-T05) for queue and persisted-log patterns; independent C# implementation.

## Decision

1. **Persist before acknowledging.** `SubmitTask` commits the task to the node store (SQLite WAL) before returning its receipt. A crash after the receipt never loses the task.
2. **Survive node restarts.**
   - Managed processes write stdout and stderr to node-owned files under `logs/<attempt_id>/`, never to pipes held by the node.
   - Process containers are named Windows jobs, or transient systemd user units on Linux whose processes are children of the user manager, not of the node (AD-0005).
   - Exit status is recorded durably by a helper outside the node: `exec-wrap` on Windows, the unit's `ExecStopPost` on Linux.
   - A restarted node re-attaches: it re-opens jobs or cgroups listed in the store, tails logs from the stored offsets, and records a `node_gap` segment for the downtime (R-EXE-008, R-EXE-018).
3. **Machine reboot.** The store records the boot identity (Windows: last boot time with machine identity; Linux: `/proc/sys/kernel/random/boot_id`). On startup, attempts that were running under a different boot become `LOST` with evidence (R-EXE-009).
4. **Side-effect classes and retry rules:**

| Class | Meaning | Automatic retry | Result caching | Default for |
|---|---|---|---|---|
| `PURE` | Output determined by declared inputs; no external effect | Yes (policy max, default 2) | Optional, opt-in with declared inputs and outputs | Adapter-classified compile/test commands, only when the adapter asserts it |
| `IDEMPOTENT` | May be repeated safely | Yes (default 2) | No | Restores, fetches (adapter-classified) |
| `SIDE_EFFECTING` | External effects | Never | No | Declared by caller |
| `UNKNOWN` | Not classified | Never; an unknown effect is reported | No | Any unclassified command |

   An infrastructure failure **before the process started** (spawn failure, placement failure, transfer failure) may be retried for every class. An out-of-memory kill may be retried with a larger memory grant only for `PURE` and `IDEMPOTENT` tasks.
5. **Pause and resume.** Linux uses the unit freezer (`FreezeUnit`, i.e. `cgroup.freeze`) for tasks marked `pausable` (default: true for adapter-classified build/test work, false otherwise). Windows reports unsupported. Pausing never frees memory; it only stops CPU use.
6. **Long-running tasks** (`kind=SERVICE`) have no default timeout. They support readiness conditions (output regex, TCP listen on localhost port, or a file appearing) and stop with their owner session, unless `detach=true`.
7. **Interactive attach.** `run --attach` streams output and forwards stdin while attached. Detaching never stops the task. stdin forwarding does not survive a node restart, and the task then sees end-of-file (documented).
8. **Result caching (opt-in, `PURE` only).**
   - The action key is the digest of the normalized argv, declared environment subset, toolchain identity, working-directory-relative input manifest digests and the platform.
   - Outputs are stored in the node's content-addressed store. A hit restores the declared outputs and replays recorded output.
   - Hits are always labelled `cache_restored`, never as an execution.
   - The default is `observe` mode, which records would-be hits without restoring until the user enables restore per workspace.
9. **Idempotent operations.** Submit, cancel, retry, priority change, policy change and cleanup are idempotent by `command_id` (24 h). Replays return the original receipt.
