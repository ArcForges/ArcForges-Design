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
- Git `worktree lock` is held while a task or session uses the worktree. It prevents `git worktree prune` only; it is **not** a file-write lock. Concurrent writers inside a workspace are ordered by exclusive keys ([03](03-resource-control.md) §4), and concurrent agents get separate worktrees.
- Each workspace has a **concurrency mode** (`UpdateWorkspaceSettings`): `ADAPTER_KEYS` (default), `SERIAL` or `SHARED`.
- Creation runs as a node job, using the git toolchain within a managed attempt.
- One worktree per branch.

### Archiving a dirty worktree

`RemoveWorktree` with `archive_changes=true` runs as a node job while no task, session or lock uses the worktree (state `ARCHIVING`, SM-WORKTREE). It preserves the staged state, the unstaged state and untracked files, binaries included, and proves it can restore them before removing anything (R-STOR-003):
1. **Inventory.** `git status --porcelain=v2 -z --ignored` lists staged, unstaged, untracked and ignored paths.
   - Ignored paths matching the regenerable-output detectors (§6: `bin/`, `obj/`, `target/`, CMake build trees, `node_modules`) are dropped.
   - Other ignored files (for example `.env`) are listed in the approval request. The user either includes them in the archive or confirms they may be lost. Without that decision, nothing is removed.
2. **Index snapshot.** `git write-tree` of the worktree's real index, committed with `git commit-tree -p HEAD`, gives commit `I`: exactly the staged state. An index with unmerged entries (a merge or rebase in progress) cannot be written; the job stops, removes nothing and reports it.
3. **Working-tree snapshot.** A temporary index (`GIT_INDEX_FILE`) is loaded from `I` (`git read-tree I`) and takes `git add -A`: tracked and untracked (not ignored) files, deletions and binaries as git blobs, with modes and symbolic links as git records them, through the repository's own filters. `git write-tree` and `git commit-tree -p I` give commit `W`.
4. **Keeping and exporting.**
   - The refs `refs/arcforges/archive/<archive_id>/index` and `/worktree` in the main repository keep `I` and `W` alive.
   - A bundle `records/worktree-archives/<archive_id>.bundle` holds `I`, `W` and the branch commits not reachable from the base ref. Its prerequisites are base-ref commits, which the repository and its remote keep, so the archive can be restored even if the archive refs are lost.
   - Included ignored files go to `<archive_id>-ignored.tar.zst`.
5. **Verification.**
   - `git bundle verify` confirms that the repository holds the bundle's prerequisites.
   - A temporary bare repository fetches the base ref from the main repository, then the archive refs from the bundle. The fetched commits must have the IDs `I` and `W`, and `git fsck --connectivity-only` must pass, so the bundle alone restores exactly those trees.
   - The live working tree must still match `W`: the blob IDs and modes of `git ls-tree -r W` against every live file hashed with `git hash-object --path` (the repository's filters apply) and its mode as git records it, tracked and untracked alike, with no path missing or extra.
   - The live index (`git ls-files -s`) must equal the tree of `I`.
   - Included ignored files must match by SHA-256.
   - Any mismatch stops the job: the state returns to `ACTIVE`, nothing is removed, and a finding is raised.
6. **Removal.** Only after verification: `git worktree remove --force` (safe, because everything is archived), then branch handling as requested. The archive record (`worktree_archive`) stores the commits, paths, counts and verification time.
7. **Restore.** `WorkspaceService.RestoreWorktree(archive_id)` (CLI `arcforges worktree restore <id>`) runs as a job:
   - it creates a worktree on the archived branch, or a new branch, at the archived `HEAD`;
   - `git read-tree I` restores the staged state;
   - `git restore --source=W --worktree -- .` restores unstaged and untracked files without touching the index;
   - included ignored files are extracted;
   - the job ends by re-running the step-5 comparison.

Archives are listed by `ListWorktreeArchives` and kept 90 days (refs and bundle). Retention then removes them, with a notice 7 days before.

## 4. Per-attempt directories

Each attempt gets `tmp/<attempt_id>/` (TMP, TEMP and TMPDIR point there), created at launch with an ownership record. At attempt end it is deleted, unless the attempt failed and `keep_failed_tmp=true` (default true, 24 h), so diagnosis can inspect it (R-STOR-004). Outputs that a tool insists on writing into the system temp directory (BEST_EFFORT tools) are reported by the disk analyzer, not chased.

## 5. Quotas, disk limits and low space

ArcForges runs unprivileged, so **no limit is enforced by the file system**. Per-user NTFS quotas and Linux project quotas need administrator or root rights and are outside the current scope. Every disk limit is therefore one of these kinds, and the UI and records name the kind (R-STOR-005, R-STOR-009):

| Kind | When it is checked | Effect | Enforced by |
|---|---|---|---|
| **Admission threshold** | At allocation: attempt start, worktree creation, transfer receive, export | The allocation is refused (`RESOURCE/quota_exceeded`, `RESOURCE/disk_space`) | ArcForges, before anything is written |
| **Monitored limit** | At a stated interval while the writer runs | `storage.disk_limit_action`: `TERMINATE` (default) or `NOTIFY`; a finding | ArcForges, after detection. The overshoot is bounded by write rate × interval. |
| **Tool-enforced limit** | By the tool itself | The tool evicts | sccache (`SCCACHE_CACHE_SIZE`), ccache (`max_size`) |
| **Report-only** (`WARN` quotas) | Housekeeping (every 10 min) | A finding only | — |

**Runtime limits on running writers:**

| Writer | Limit | Interval | Action |
|---|---|---|---|
| Attempt output (stdout plus stderr) | `max_attempt_output_bytes` (default 2 GiB) | Every tailer read (100 ms) | `TERMINATE` → `termination_reason=OUTPUT_LIMIT`, or `NOTIFY` ([04](04-execution.md) §4) |
| Attempt temporary directory | `max_attempt_tmp_bytes` (default 20 GiB) | 15 s (incremental walk of `tmp/<attempt>/` through the size cache) | `TERMINATE` → `DISK_LIMIT`, or `NOTIFY` |
| Sub-root totals (`HARD` quotas of §1) | Per sub-root | At allocation, and in housekeeping | New allocations refused; a finding. Running writers are covered by the rows above and by the low-space guard. |
| Caches | Per cache quota | After write bursts, and in housekeeping | Eviction under the maintenance lease ([05](05-toolchains-caches.md) §4) |
| Incoming transfers | Manifest size against free space and the `staging` quota | Before pulling, then every 5 s | Refused before, or aborted during, with `RESOURCE/disk_space` |

**Low-space guard.** Every volume that holds a managed root, or the working directory of a running attempt, is checked every 5 s (`GetDiskFreeSpaceExW`, `statvfs`):

| Level | Condition | Actions |
|---|---|---|
| `NORMAL` | Free space ≥ `max(min_free_bytes, 5% of the volume)` | — |
| `LOW` | Below that | No new attempt whose working directory, temporary directory or output root is on the volume (blocking reason `disk_space`). Housekeeping runs at once (retention, expired quarantine, idle remote slots). Finding `DISK_PRESSURE`. |
| `CRITICAL` | Free space < `critical_free_bytes` (default 512 MiB) | Running attempts that write to the volume: on Linux, pausable attempts are frozen; the rest follow `disk_limit_action`, preemptible attempts first, then by ascending priority (`DISK_LIMIT`). Node logging drops to warnings. |

**The node's own store.**
- The node keeps a preallocated reserve file, `store/reserve.bin` (64 MiB). At `CRITICAL` on the store's volume it deletes the file, so store commits and the event journal can continue. It recreates the file when the level is back to `NORMAL`.
- If a store write still fails for lack of space, SQLite rolls the transaction back. The node then enters the lifecycle state `DEGRADED` with the reason `store_out_of_space`: it stays readable, refuses mutations with `RESOURCE/disk_space`, and returns to `READY` when space returns. It never continues with unrecorded state.

The disk level of each volume is part of `ResourceSnapshot.volumes` and of the remote status summary (`disk_level`).

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

Sizes use an incremental size cache keyed by `(path, mtime, inode/file-id)`. Directory symlinks and junctions are never followed outside their root. Analysis is bounded (default 15 min, 5 million entries) and reports truncation explicitly.

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
