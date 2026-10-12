# 06 — Managed storage, workspaces and cleanup

## 1. Data root layout

Default data root: `%LOCALAPPDATA%\ArcForges\data\` (Windows), `~/.local/share/arcforges/data/` (Linux) ([AD-0012](../decisions/AD-0012-distribution-and-updates.md)).

| Sub-root | Path | Content | Default quota | Retention |
|---|---|---|---|---|
| `store` | `store/node.db` (+ `-wal`, `-shm`) | Node store | guard: 1 GiB free on the volume | n/a |
| `work` | `work/<workspace_id>/` | Node-managed git worktrees; remote workspaces for LAN placement | 100 GiB (warn) | Until released; idle reports after 14 days |
| `tmp` | `tmp/<attempt_id>/` | Per-attempt TMP/TEMP/TMPDIR | 20 GiB (hard) | Deleted at attempt end; failed attempts kept 24 h if `keep_failed_tmp` |
| `cache` | `cache/<kind>/` | Shared caches ([05](05-toolchains-caches.md) §4) | per cache | Eviction rules |
| `out` | `out/<workspace_id>/<key>/` | Managed build outputs (opt-in per workspace) | 50 GiB (warn) | Until workspace release; regenerable |
| `logs` | `logs/<attempt_id>/`, `logs/node/` | Attempt output and node logs | 5 GiB | 14 days (pinned excepted) |
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
| `MANAGED_WORKTREE` | `WorkspaceService.CreateWorktree(base_workspace, branch, base_ref, owner)` | Same repository identity; branch; path `work/<workspace_id>/` | `RemoveWorktree`. Refused if the worktree is dirty, unless `archive_changes=true`, which saves `git diff` (tracked) plus untracked files to `records/worktree-archives/<id>.tar.zst` first and needs approval. Never discards work silently. |
| `REMOTE` | Placement from a LAN origin | `origin_node_id/origin_workspace_id` | Released by origin or after 30 days idle |

**Managed worktree rules:**
- Default branch name `af/<owner-short>/<name>`.
- Git `worktree lock` is held while a task or session uses the worktree.
- Creation runs as a node job, using the git toolchain within a managed attempt.
- One worktree per branch.

## 4. Per-attempt directories

Each attempt gets `tmp/<attempt_id>/` (TMP, TEMP and TMPDIR point there), created at launch with an ownership record. At attempt end it is deleted, unless the attempt failed and `keep_failed_tmp=true` (default true, 24 h), so diagnosis can inspect it (R-STOR-004). Outputs that a tool insists on writing into the system temp directory (BEST_EFFORT tools) are reported by the disk analyzer, not chased.

## 5. Quotas

Quota checks happen at allocation (attempt start, worktree creation, transfer receive, export) and in housekeeping (every 10 min).

| Quota kind | Effect when exceeded |
|---|---|
| Hard | New allocations fail with `ERROR_CATEGORY_RESOURCE` and code `quota_exceeded`. Running work continues. A finding is raised. |
| Warn | A finding only |

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
