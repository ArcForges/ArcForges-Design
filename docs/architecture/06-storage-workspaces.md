# 06 — Managed storage, workspaces and cleanup

## 1. Data root layout

Default data root: `%LOCALAPPDATA%\ArcForges\data\` (Windows), `~/.local/share/arcforges/data/` (Linux) ([AD-0012](../decisions/AD-0012-distribution-and-updates.md)).

| Sub-root | Path | Content | Default quota | Retention |
|---|---|---|---|---|
| `store` | `store/node.db` (+ `-wal`, `-shm`) | Node store | guard: 1 GiB free on the volume | n/a |
| `work` | `work/<workspace_id>/`, `work/remote/<origin_node>/<origin_workspace>/<slot>/` | Node-managed git worktrees; remote workspace slots for LAN placement ([09](09-lan.md) §6) | 100 GiB (warn) | Until released; idle reports after 14 days; idle remote slots removed after 7 days |
| `tmp` | `tmp/<attempt_id>/` | Per-attempt TMP/TEMP/TMPDIR | 20 GiB root (hard: admission); 20 GiB per attempt (monitored, §5) | Deleted at attempt end; failed attempts kept 24 h if `keep_failed_tmp` |
| `cache` | `cache/<kind>/` | Shared caches ([05](05-toolchains-caches.md) §4) | per cache | Eviction rules |
| `out` | `out/<workspace_id>/<key>/` | Managed build outputs (opt-in per workspace) | 50 GiB (warn) | Until workspace release; regenerable |
| `logs` | `logs/<attempt_id>/`, `logs/node/` | Attempt output and node logs | 5 GiB root (retention); 2 GiB output per attempt (monitored, §5) | 14 days (pinned excepted) |
| `records` | `records/exports/`, `records/support/`, `records/backups/`, `records/worktree-archives/` | Exports, support bundles, store backups, archived worktree patches | 5 GiB | Exports 7 days; support bundles 30 days; backups last 3; archives 90 days |
| `downloads` | `downloads/` | Update packages, toolchain-adapter downloads (none by default) | 5 GiB | Last 2 versions |
| `staging` | `staging/quarantine/<plan_id>/`, `staging/transfer/` | Cleanup quarantine; incoming transfers | 20 GiB | Quarantine purged after 24 h; transfers after 1 h idle |
| `run` | `run/` | Endpoint descriptor, sockets (Linux fallback) | — | — |

Any sub-root may be relocated (`StorageService.UpdateRoot`), for example to a Dev Drive on Windows. Relocation is refused while attempts use the sub-root. Otherwise it copies, verifies and switches, and the old location moves to quarantine (R-STOR-001).

## 2. Ownership records

Every directory the node creates under a managed sub-root has a `managed_directory` row (R-STOR-002):

| Field | Meaning |
|---|---|
| `owner_kind`, `owner_id` | `ATTEMPT`, `TASK`, `WORKSPACE`, `CACHE`, `NODE`, `PLAN` or `TRANSFER`, with the owning ID |
| `root_class`, `relative_path` | Sub-root and path |
| `created_at`, `last_used_at`, `pinned` | Lifecycle |
| `size_bytes`, `size_measured_at` | Last measurement |
| `state` | `ACTIVE`, `IDLE`, `CANDIDATE`, `QUARANTINED` or `REMOVED` |

A directory found under a managed sub-root without a record is reported as `UNTRACKED` and never deleted automatically.

## 3. Workspaces

| Kind | Created by | Identity | Removal |
|---|---|---|---|
| `REGISTERED` | User (CLI, Desktop) or automatically on the first task whose working directory is inside a git repository (policy `auto_register=true`) | `git rev-parse --git-common-dir` plus remote URLs (hashed) and the root path; for non-git roots, the canonical path | Unregister only (never deletes files) |
| `MANAGED_WORKTREE` | `WorkspaceService.CreateWorktree(base_workspace, branch, base_ref, owner)` | Same repository identity; branch; path `work/<workspace_id>/` | `RemoveWorktree`. Refused if the worktree is dirty, unless `archive_changes=true` (needs approval), which archives the staged and working-tree state and **verifies** the archive before anything is removed (below). Never discards work silently. |
| `REMOTE` | Placement from a LAN origin | `origin_node_id/origin_workspace_id/slot` | Each slot is leased by one remote attempt at a time ([09](09-lan.md) §6). Released by the origin, removed after 7 days idle. |

**Managed worktree rules:**
- Default branch name `af/<owner-short>/<name>`.
- Git `worktree lock` is held while a task or session uses the worktree. It prevents `git worktree prune` only; it is **not** a file-write lock. Concurrent writers and readers inside a workspace are ordered by keys ([03](03-resource-control.md) §4), and concurrent agents get separate worktrees.
- Each workspace has a **concurrency mode** (`UpdateWorkspaceSettings`): `ADAPTER_KEYS` (default), `SERIAL` or `SHARED`.
- Creation runs as a node job, using the git toolchain within a managed attempt.
- One worktree per branch.

### Archiving a dirty worktree

`RemoveWorktree` with `archive_changes=true` runs as a node job while no task, session or lock uses the worktree (state `ARCHIVING`, SM-WORKTREE). It preserves the staged state, the unstaged state and untracked files, binaries included, and proves it can restore them before removing anything (R-STOR-003). L-19 records a round trip of these steps.
1. **Plan.** `WorkspaceService.PlanWorktreeRemoval` runs `git status --porcelain=v2 -z --ignored` and reports:
   - the staged, unstaged and untracked counts;
   - intent-to-add paths (`git add -N`, status `.A`), which `git write-tree` leaves out; they are recorded and re-applied on restore;
   - ignored files outside the regenerable-output detectors (§6: `bin/`, `obj/`, `target/`, CMake build trees, `node_modules`), for example `.env`, with a digest of the list;
   - what blocks archiving: unmerged index entries (a merge or rebase in progress), and submodules or nested repositories with their own uncommitted changes, whose content an archive of this repository cannot hold.
2. **Decision.** If ignored files are listed, `RemoveWorktree` must carry `ignored_files` (`INCLUDE`, or `DISCARD_CONFIRMED`, which only HUMAN callers may choose) and the list digest; a changed list fails with `CONFLICT/digest_mismatch`. An agent's request goes through approval, and the approval shows the list. Anything listed under `blocking` refuses the removal (`STATE/invalid_state`), and nothing is removed.
3. **Index snapshot.** `git write-tree` of the worktree's real index, committed with `git commit-tree -p HEAD`, gives commit `I`: exactly the staged state, apart from the intent-to-add entries of step 1.
4. **Working-tree snapshot.** A temporary index (`GIT_INDEX_FILE`) is loaded from `I` (`git read-tree I`) and takes `git add -A`: tracked and untracked (not ignored) files, deletions and binaries as git blobs, with modes and symbolic links as git records them, through the repository's own filters. `git write-tree` and `git commit-tree -p I` give commit `W`.
5. **Keeping and exporting.**
   - The refs `refs/arcforges/archive/<archive_id>/index` and `/worktree` in the main repository keep `I` and `W` alive.
   - A bundle `records/worktree-archives/<archive_id>.bundle` holds `I`, `W` and the branch commits not reachable from the base ref. Its prerequisites are base-ref commits, which the repository and its remote keep, so the archive can be restored even if the archive refs are lost.
   - Included ignored files go to `<archive_id>-ignored.tar.zst`.
   - Files whose bytes do not survive the repository's filters (for example mixed line endings under `core.autocrlf`), and the content of LFS files, are kept byte for byte in `<archive_id>-raw.tar.zst` (step 6 finds them).
6. **Verification.**
   - `git bundle verify` confirms that the repository holds the bundle's prerequisites.
   - A temporary bare repository fetches the base ref from the main repository, then the archive refs from the bundle. The fetched commits must have the IDs `I` and `W`, and `git fsck --connectivity-only` must pass, so the bundle alone restores exactly those trees.
   - The live working tree must match `W` in git's terms: the blob IDs and modes of `git ls-tree -r W` against every live file hashed with `git hash-object --path` and its mode as git records it, tracked and untracked alike, with no path missing or extra.
   - It must also match byte for byte: a temporary checkout of `W` with the repository's filter configuration is compared with the live files. Files that differ only through filters, and LFS files, go to the raw archive and are compared by SHA-256.
   - The live index (`git ls-files -s`, without the intent-to-add entries) must equal the tree of `I`.
   - Included ignored files must match by SHA-256.
   - Any mismatch stops the job: the state returns to `ACTIVE`, nothing is removed, and a finding is raised.
7. **Removal.** Only after verification: `git worktree remove --force` (safe, because everything is archived), then branch handling as requested. The archive record (`worktree_archive`) stores the commits, the intent-to-add paths, the side archives, counts, the ignored-files decision and the verification time.
8. **Restore.** `WorkspaceService.RestoreWorktree(archive_id)` (CLI `arcforges worktree restore <id>`) runs as a job:
   - `git worktree add --no-checkout` at the archived `HEAD`: on the archived branch when it is free and still points there, otherwise on a new branch (`<branch>-restored` by default);
   - `git read-tree -u --reset W` writes the working-tree state, including staged deletions and renames;
   - `git read-tree I` restores the staged state without touching files, and `git add -N` re-applies the intent-to-add paths;
   - the raw archive and the included ignored files are extracted;
   - the job ends by comparing the restored worktree with the archive: the index with `I` plus the intent-to-add paths, and every file's blob ID and SHA-256 with `W` and the side archives. If that fails, the restored worktree is kept for inspection, the archive is unchanged, and a finding is raised.

Archives are listed by `ListWorktreeArchives` and kept 90 days (refs, bundle and side archives). Retention then removes them, with a notice 7 days before. Included ignored files such as `.env` stay in the side archive for that time, protected only by the data root's permissions; the decision dialog says so.

## 4. Per-attempt directories

Each attempt gets `tmp/<attempt_id>/` (TMP, TEMP and TMPDIR point there), created at launch with an ownership record. At attempt end it is deleted, unless the attempt failed and `keep_failed_tmp=true` (default true, 24 h), so diagnosis can inspect it (R-STOR-004). Outputs that a tool insists on writing into the system temp directory (BEST_EFFORT tools) are reported by the disk analyzer, not chased.

## 5. Quotas, disk limits and low space

ArcForges runs unprivileged, so **no limit is enforced by the file system**. Per-user NTFS quotas and Linux project quotas need administrator or root rights and are outside the current scope. Every disk limit is therefore one of these kinds, and the UI and records name the kind (R-STOR-005, R-STOR-009):

| Kind | When it is checked | Effect | Enforced by |
|---|---|---|---|
| **Admission threshold** | At allocation: attempt start, worktree creation, transfer receive, export | The allocation is refused (`RESOURCE/quota_exceeded`, `RESOURCE/disk_space`) | ArcForges, before anything is written |
| **Monitored limit** | At a stated interval while the writer runs | `storage.disk_limit_action`: `TERMINATE` (default) stops the writer at once, without the graceful phase ([04](04-execution.md) §6); `NOTIFY` raises a finding and lets it continue | ArcForges, after detection. The overshoot is bounded by write rate × (interval + stop latency). |
| **Tool-enforced limit** | By the tool itself | The tool evicts | ccache (`max_size`). The sccache store's quota is enforced by the node, its only writer ([05](05-toolchains-caches.md) §5). |
| **Report-only** (`WARN` quotas) | Housekeeping (every 10 min) | A finding only | — |

**Runtime limits on running writers:**

| Writer | Limit | Interval | Action |
|---|---|---|---|
| Attempt output (stdout plus stderr) | `max_attempt_output_bytes` (default 2 GiB) | Every tailer read (100 ms) | `TERMINATE`: stopped at once, `termination_reason=OUTPUT_LIMIT`; or `NOTIFY`: a finding, and the output is kept ([04](04-execution.md) §4) |
| Attempt temporary directory | `max_attempt_tmp_bytes` (default 20 GiB) and `max_attempt_tmp_entries` (default 1,000,000) | 15 s. Each pass is a full walk of `tmp/<attempt>/` that keeps no per-file state, so a file growing in place is seen (L-22) and memory stays small. A pass reads at most `max_attempt_tmp_entries` entries; beyond that the attempt counts as over its limit. | `TERMINATE`: stopped at once, `DISK_LIMIT`; or `NOTIFY`: a finding |
| Sub-root totals (`HARD` quotas of §1) | Per sub-root | At allocation, and in housekeeping | New allocations refused; a finding. Running writers are covered by the rows above and by the low-space guard. |
| Caches | Per cache quota | After write bursts, and in housekeeping | Eviction under the maintenance lease ([05](05-toolchains-caches.md) §4) |
| Incoming transfers | Manifest size against free space and the `staging` quota | Before pulling, then every 5 s | Refused before, or aborted during, with `RESOURCE/disk_space` |

**Low-space guard.** Every volume that holds a managed root, or the working directory of a running attempt, is checked every 5 s (`GetDiskFreeSpaceExW`, `statvfs`). While the node is down, the attempt guards below keep checking:

| Level | Condition | Actions |
|---|---|---|
| `NORMAL` | Free space ≥ the LOW threshold `max(min_free_bytes, min(5% of the volume, low_free_cap_bytes))` (defaults 1 GiB and 20 GiB) | — |
| `LOW` | Below that | No new attempt whose working directory, temporary directory or output root is on the volume (blocking reason `disk_space`). Housekeeping runs at once (retention, expired quarantine, idle remote slots). Finding `DISK_PRESSURE`. |
| `CRITICAL` | Free space < `critical_free_bytes` (default 512 MiB) | Running attempts that write to the volume: on Linux, pausable attempts are frozen; the rest are stopped at once (`DISK_LIMIT`), preemptible attempts first, then by ascending priority, unless `disk_limit_action=NOTIFY`, in which case they continue and a finding is raised. Node logging drops to warnings. |

**The node's own store.**
- The node keeps a preallocated reserve file, `store/reserve.bin` (64 MiB). At `CRITICAL` on the store's volume, the writers there are frozen or stopped first. The reserve is deleted only when a store write fails for lack of space; the write is then retried once, and the file is recreated when the level is back to `NORMAL`.
- If the retry also fails (for example because an unmanaged process took the freed space), SQLite rolls the transaction back. The node then enters the lifecycle state `DEGRADED` with the reason `store_out_of_space`: it stays readable, refuses mutations with `RESOURCE/disk_space`, and returns to `READY` when space returns. It never continues with unrecorded state. This, not the reserve, is the guarantee (R-STOR-009).

The disk level of each volume is part of `ResourceSnapshot.volumes` and of the remote status summary (`disk_level`).

**Attempt guards: the limits hold while the node is down.** Executions survive a node stop, crash or crash loop ([02](02-node-service.md) §2), so the runtime limits above cannot depend on the node alone.
- **Who guards.**
  - **Windows:** each attempt's holder (`arcforges node exec-wrap`). It already runs outside the job, holds the job handles and the output files, and lives until the node acknowledges the exit record ([AD-0005](../decisions/AD-0005-resource-enforcement.md) Windows §3).
  - **Linux:** one user unit, `arcforges-guard.service` (`Restart=always`, no start limit; [13](13-distribution-updates.md) §3.4). It guards every running attempt unit.
- **What it knows.** Before starting an attempt, the node writes `logs/<attempt>/guard.json`: the output files, the temporary directory, the volumes the attempt writes to, the limits and actions in force, and whether the attempt is preemptible and pausable. The node renews a heartbeat, `run/node-heartbeat`, from its enforcement loop, once recovery is done and each monitor (the output tailer, the temporary-directory pass and the low-space check) has completed a cycle ([02](02-node-service.md) §2). Each renewal, every second, writes the node's instance ID and an increasing sequence number.
- **Takeover.** A guard acts while the heartbeat's instance and sequence have not changed for policy `storage.guard_takeover_ms` (2,000–60,000 ms; default 5,000), measured on the guard's own monotonic clock, so changes of the wall clock do not matter.
  - That covers a node that is stopped, crashed or hung.
  - It also covers a node that restarts in a loop: a node renews only once it enforces, so restarts faster than the threshold leave the guards in charge.

  A guard that has taken over applies the runtime limits above at the same intervals:
  - the output files every 100 ms;
  - the temporary directory every 15 s, with the same full walk as the node;
  - free space on the attempt's volumes every 5 s.
- **Actions.** The same as the node's:
  - `TERMINATE` stops the attempt at once, with `OUTPUT_LIMIT` or `DISK_LIMIT`: Windows `TerminateJobObject`; on Linux the guard freezes the unit, then `KillUnit`, as the node does;
  - at `CRITICAL`, Linux freezes pausable attempts (`FreezeUnit`) and stops the rest. While the node is still down, the guard thaws them once the level has been back to `NORMAL` for 30 s;
  - `NOTIFY` is recorded and leaves the attempt running.
- **Records.** Each action is appended to `logs/<attempt>/guard-events.jsonl` with its evidence. The guard never writes the node store. When the node returns, it records the stops with `limit_enforced_by=GUARD`, raises the findings the actions call for, and thaws frozen attempts once the level is back to `NORMAL`. Stops are idempotent: a stop that the node and a guard both make is recorded once, and the first recorded reason wins.
- **Stand-down.** When the heartbeat is fresh again, the guard stops checking and the node resumes.
- **Bound.** While the node is down, the overshoot is the write rate × (takeover delay + interval + stop latency).
- **Hung nodes are restarted.** A node whose heartbeat stalls for 30 s is restarted:
  - **Linux:** by systemd's watchdog (`WatchdogSec=30`, active once the node reports ready);
  - **Windows:** by the supervisor, which counts from the node's first heartbeat, so a long store migration at startup is not mistaken for a hang.

  The enforcement loop renews the heartbeat and pings the watchdog only while the cache store answers its own probe: an in-memory request to the store's request loop, with a 5 s timeout, that touches no disk. Three probes missed in a row stop the renewals, so a hung store also leads to a restart, while a disk stall under load does not. The store refuses a request it cannot complete within 30 s rather than hold it. A hang therefore cannot last, which also bounds how long compiles can wait on the store ([05](05-toolchains-caches.md) §5).
- **When a guard is missing.** A Windows holder that crashed, or a Linux guard unit that cannot run, leaves its attempts unguarded until the node returns. The node then records `guard_lost` on those attempts and raises a finding. This is the remaining gap, and it is stated, not hidden.

## 6. Disk analysis

`StorageService.AnalyzeStorage(scope)` starts a node job and produces a `storage_analysis` with items (R-STOR-007):

| Detector | Rule | Item class |
|---|---|---|
| Sub-root usage | Size per sub-root and per owner | `USAGE` |
| Regenerable outputs | `bin/`, `obj/` (with a `.csproj` sibling), `target/` (with `Cargo.toml`), CMake build trees (`CMakeCache.txt`) inside registered workspaces | `REGENERABLE_OUTPUT` (low risk) |
| Abandoned managed worktrees | No running or queued task and no live session for 14 days, **and** the branch is merged into its base or deleted upstream, **and** the worktree is clean | `ABANDONED_WORKTREE` (medium) |
| Dirty idle worktrees | Like above but dirty | `IDLE_DIRTY_WORKTREE` (report only; archive-then-remove needs explicit approval) |
| Duplicate caches | Global-packages-like folders outside managed caches (`.nupkg.metadata` layout), multiple `node_modules/.cache`, old sccache/ccache directories, with overlap estimate | `DUPLICATE_CACHE` (medium) |
| Per-task restore copies | Folders named in the records of managed attempts as overridden `NUGET_PACKAGES` | `PER_TASK_RESTORE` (low) |
| Cache over quota | Cache size > quota | `CACHE_TRIM` |
| Old logs and records | Beyond retention | `RETENTION` (low) |
| Quarantine pending purge | — | `QUARANTINE` |
| Untracked managed directories | §2 | `UNTRACKED` (report only) |

Sizes use an incremental size cache keyed by `(path, mtime, inode/file-id)`. The same size cache measures managed caches for per-attempt evidence ([07](07-records-diagnosis-memory.md) §1.5). Directory symlinks and junctions are never followed outside their root. Analysis is bounded (default 15 min, 5 million entries) and reports truncation explicitly.

## 7. Cleanup (two-phase, bounded)

1. **Plan.** `PlanCleanup(analysis_id or rules, selection)` returns a `cleanup_plan`. Each item has: ID, absolute path, size, class, reason, risk, action (`QUARANTINE`, `GIT_WORKTREE_REMOVE`, `TOOL_CLEAN`, `ARCHIVE_THEN_REMOVE` or `DIRECT_DELETE`), and a validation fingerprint (mtime, size, owner state). The plan expires after 60 min and carries a digest. No item is acted on during planning.
2. **Approval.** Human surfaces approve explicitly. MCP callers may plan, but execution from MCP needs an approval unless policy `cleanup.agent_execute=LOW_RISK_ONLY` and every selected item is low risk.
3. **Execute.** `ExecuteCleanup(plan_id, plan_digest, item_ids)` re-validates each item immediately before acting:
   - it is still not referenced by any queued or running attempt, live session, pinned record or maintenance lease;
   - its fingerprint is unchanged within tolerance;
   - it is still inside an allowed location: managed sub-roots, registered-workspace regenerable outputs, or paths the user explicitly added to *this* plan through `AddExternalPath`, which needs a separate confirmation.

   Actions:
   - `QUARANTINE`: rename into a quarantine root on the item's own volume, so the move is a rename and never a copy:
     - `staging/quarantine/<plan_id>/<item_id>` for items on the data-root volume;
     - otherwise `<quarantine root>/<plan_id>/<item_id>`, where policy `storage.quarantine_roots` maps the volume to a directory on it. The user creates or confirms each root, and the node keeps it user-only (owner ACL on Windows, mode `0700` on Linux).

     The rename fails safely if files are open, and the item is then reported `IN_USE`.
   - `GIT_WORKTREE_REMOVE`: `git worktree remove` without `--force`.
   - `TOOL_CLEAN`: the tool's own command, for example `dotnet nuget locals http-cache --clear`.
   - `ARCHIVE_THEN_REMOVE`: §3.
   - `DIRECT_DELETE`: only for items on a volume that has no quarantine root, after an explicit per-item "delete without quarantine" confirmation (R-STOR-006).
4. **Purge.** Housekeeping deletes plan directories in every quarantine root once they are older than `quarantine_hours` (default 24 h). `RestoreQuarantine(item)` moves an item back while it remains.
5. **Bounds.** No API deletes a path that is not an item of a validated plan. No wildcard or recursive-delete parameter exists. Each execution acts only on the listed items, at most 10,000 items and 2 TiB per plan (R-STOR-006, R-STOR-008).
