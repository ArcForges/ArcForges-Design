# Node store (SQLite)

Schema: [node-store.sql](node-store.sql). It is checked by `tools/check_design.py`, which loads it into SQLite and runs the foreign-key and integrity checks.

## 1. Engine and file

- **File and journaling.** `<data root>/store/node.db`, using `Microsoft.Data.Sqlite` (SQLitePCLRaw bundle, AOT-verified in DesktopPlatform and ArcScope; re-verified by AF-NODE-02 on win-x64 and linux-x64). WAL journal, `foreign_keys=ON`, `synchronous=NORMAL`, and `busy_timeout=5000`.
- **Single writer.** The node's command processor ([02](../architecture/02-node-service.md) §1) is the only writer; readers use separate read-only connections.
- **Durability.** A receipt is returned only after its transaction commits (AD-0006 §1). `command_dedup` commits use `synchronous=FULL`, so an acknowledged `command_id` survives power loss.
- **Conventions:**
  - IDs are 16-byte UUIDv7 `BLOB`s;
  - instants are microseconds since the Unix epoch, the same unit as the Cloud D1 model;
  - enums are stored as their `arcforges.node.v1` proto numbers, so the contract and the store share one numbering;
  - protobuf columns hold serialized contract messages;
  - store-internal wrapper messages (`FindingActions`, `KeySet`, `BundleFiles`, `Reservoir`) are defined in `ArcForges.Node.Store` (`store.proto`, internal, not a public contract).
- **Migrations.** Forward-only and expand-only per release; contract steps are deferred ([13](../architecture/13-distribution-updates.md) §6). Backups are taken before every migration. `store_meta` holds `schema_version` and `min_reader_version`.

## 2. Tables

**Ownership** names the subsystem whose commands write the table ([02](../architecture/02-node-service.md) §1). **Retention** is applied by housekeeping (every 10 min), within the policy limits.

### Core

| Table | Purpose | Key / indexes | Owner | Retention |
|---|---|---|---|---|
| `store_meta` | Schema versions, node identity and role (always HOST; the guest role is retired by [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md) §4), boot identity, clean-shutdown marker, journal generation | singleton | Store | Permanent |
| `node_setting` | Node name, feature toggles, UI-facing node settings | `name` | Node | Permanent |
| `root_location` | Current path of each relocatable sub-root | `root_class` | Storage | Permanent |
| `policy_document` | Revisioned `PolicyDocument`; exactly one current revision | `revision`; partial unique `is_current` | Policy engine | Last 200 revisions |
| `command_dedup` | Idempotency record per `command_id`: method, payload digest, origin, stored response | `command_id`; `expires_at` | Api layer | 24 h after creation |
| `event_journal` | Ordered events for resume by cursor | `seq`; `at` | Event hub | 100,000 events or 24 h, whichever is smaller |
| `audit_log` | Privileged, remote and approval-gated actions (R-SEC-002) | `seq`; `at` | All, through the audit helper | 1 year |
| `job` | Long-running node jobs | `job_id`; `(state, created_at)` | Job runner | 30 days after finishing |
| `notification` | Desktop notification centre | `notification_id`; `created_at` | Notifier | Last 500 |

### Workspaces and sessions

| Table | Purpose | Key / indexes | Owner | Retention |
|---|---|---|---|---|
| `workspace` | Registered, managed-worktree and remote workspaces (SM-WORKTREE), with the concurrency mode; remote workspaces are per-attempt slots with their lease holder ([09](../architecture/09-lan.md) §6) | `workspace_id`; unique active `root_path`; unique active `(base, branch)`; unique active remote slot `(origin node, origin workspace, slot)`; unique slot lease | Workspace manager | Removed rows kept 90 days |
| `worktree_archive` | Verified archives of dirty worktrees: index and working-tree commits, bundle and side archives, intent-to-add paths, the ignored-files decision, counts, verification time ([06](../architecture/06-storage-workspaces.md) §3) | `archive_id`; `expires_at` while kept; `(base_workspace_id, created_at)` | Workspace manager | 90 days (refs and bundle), then the row is kept with `removed_at` for 90 more days |
| `session` | AI client sessions (SM-SESSION) | `session_id`; unique `(client, client_session_id)`; live agent roots; `(state, last_activity_at)` | Session service | 90 days after end |
| `session_subagent` | Subagents per session | `(session_id, agent_id)` | Session service | With the session |
| `hook_event` | Hook intake log with dedup key and routing decision (no raw payloads; command summaries redacted) | `hook_event_id`; unique `dedup_key`; `(session_id, at)` | Session service | 30 days |
| `probe_result` | Latest probe result per client and environment | `(client, environment)` | Integration service | Permanent until superseded |
| `probe_ticket` | Single-use probe tokens (hash only) | `token_hash` | Integration service | 1 day |

### Execution and records

| Table | Purpose | Key / indexes | Owner | Retention |
|---|---|---|---|---|
| `env_snapshot` | Content-addressed caller environments without secret-shaped values: identical environments are stored once (R-EXE-017) | `env_digest` (SHA-256 of the canonical entries); unreferenced `(last_used_at)` | Scheduler | Deleted 24 h after the last referencing task is purged |
| `task` | Tasks (SM-TASK) with a redacted spec, the environment snapshot reference, owner, queue fields and flags; the side-effect class with its source and the adapter's suggestion (AD-0006 §4); the large-task reservation interval; the caller hand-off time; the exact command digest used by `join_existing`. `aged_at` is the aging start that `SetTaskPriority` sets on a waiting task (never on a running one, and never by an aging step): the aging of [03](../architecture/03-resource-control.md) §4 counts from `max(queued_at, aged_at)`, and a retry, automatic or manual, clears it (added 2026-10-23, AF-SCHED-01). | `task_id`; queue index on live states; join lookup `(owner_session_id, command_digest)` on live states; `(owner_session_id, created_at)`; `(workspace_id, created_at)`; `created_at`; `(pool, state)`; `(command_fingerprint, finished_at)` | Scheduler | Records: policy `record_retention_days` (90); pinned excepted |
| `task_concurrency_key` | Effective keys per task with their mode (exclusive or shared), source (caller, adapter, workspace access or mode) and early release, so admission rebuilds the holders after a restart ([03](../architecture/03-resource-control.md) §4) | `(task_id, concurrency_key)`; held keys by `concurrency_key` | Scheduler | With the task |
| `task_secret` | Sealed values of secret-shaped environment variables, so queued tasks, restarts and retries run with the submitted environment ([04](../architecture/04-execution.md) §2). AES-256-GCM under the node data key from the OS secret store, with the task ID as associated data. | `task_id`; `purge_after` | Scheduler | Purged at `purge_after` (terminal + `storage.secret_retention_hours`, default 24 h) or on `PurgeTaskRecord`; then `RetryTask` fails with `STATE/secrets_unavailable` |
| `task_dependency` | Dependency edges (acyclic, checked at submit) | `(task_id, depends_on_task_id)`; reverse index | Scheduler | With the task |
| `attempt` | Attempts (SM-ATTEMPT): container, request and grant, result, accounting (`accounted_mem_bytes` per [03](../architecture/03-resource-control.md) §3), output offsets; who stopped it for a disk limit (`limit_enforced_by`) and whether it ran unguarded (`guard_lost`); for remote placements the output bases and the applied-output result | `attempt_id`; unique `(task_id, number)`; live states; `finished_at` | Supervisor | With the task; output files per log retention (14 days / 5 GiB) |
| `result_cache_observation` | Result cache `OBSERVE` mode: action key, output-manifest digest and would-be hit per attempt ([04](../architecture/04-execution.md) §11); no output blobs are stored (restore is roadmap RM-04) | `attempt_id`; `(action_key, observed_at)` | Cache manager | With the task |
| `attempt_cache_usage` | Per attempt and cache: the tool's own counters for the attempt (hits, misses, writes, packages installed and reused, download sizes when reported) and the cache growth the node measured, with its attribution (`COUNTED`, `SOLE_BINDER`, `SHARED`, `UNKNOWN`; [07](../architecture/07-records-diagnosis-memory.md) §1.5) | `(attempt_id, cache_id)` | Cache manager | With the task |
| `cache_usage_window` | Windows in which two or more attempts bound a cache at overlapping times, with their totals recorded once at close; the source of session, workspace and period totals for shared use ([07](../architecture/07-records-diagnosis-memory.md) §1.5) | `window_id`; `(cache_id, started_at)` | Cache manager | With its attempts |
| `cache_walk` | One walk of a managed cache: bytes removed since the previous walk and growth born while no attempt bound the cache ([07](../architecture/07-records-diagnosis-memory.md) §1.5) | `(cache_id, started_at)` | Cache manager | Record retention |
| `cache_store_ledger` | The node-served sccache store's own ledger per period: bytes of first writes, entries fetched from peers and evictions; the store is never walked ([05](../architecture/05-toolchains-caches.md) §5, [07](../architecture/07-records-diagnosis-memory.md) §1.5) | `(cache_id, period_start)` | Cache manager | Record retention |
| `timeline_segment` | Categorized intervals | `(attempt_id, start_at)` | Record builder | With the task |
| `phase_event` | Adapter phase markers | `(attempt_id, at, phase)` | Record builder | With the task |
| `process_record` | Processes seen in each attempt's tree | `(attempt_id, pid, start_at)` | Monitor | With the task |
| `resource_sample` | Machine, managed-total and per-attempt samples | `(scope, subject_id, at)` | Monitor | Attempt: 1 s while running, 10 s after; machine: 5 s for 24 h, then 1 min for 30 days |
| `finding` | Findings (SM-FINDING); deduplicated by `(kind, subject)` while not resolved | `finding_id`; partial unique open subject; `(state, severity, last_seen)` | Diagnosis | Resolved: 90 days |
| `approval` | Approvals with the captured request and outcome (SM-APPROVAL) | `approval_id`; unique `command_id`; `(state, expires_at)` | Approval service | 90 days after decision |
| `fact` | Operational memory facts, one active fact per scope | `fact_id`; partial unique active scope; `(state, last_observed)` | Memory | Stale: 30 days unobserved, then deleted after another 60 days; superseded: 30 days |

While an attempt is STOPPING, its existing `termination_reason` and `detail` fields store the pending stop intent atomically with
that state (04 section 9). They do not constitute a final result: the contract view publishes `Attempt.result` only when the attempt
is FINISHED, after finalization writes the final reason/effect/detail. A missing reason on a legacy STOPPING row retains the cancellation
fallback. The SQL schema and version are unchanged.

### Storage, caches and toolchains

| Table | Purpose | Key / indexes | Owner | Retention |
|---|---|---|---|---|
| `managed_directory` | Ownership records (06 §2) | `directory_id`; unique live `(root_class, relative_path)`; `(owner_kind, owner_id)` | Storage | Removed: 30 days |
| `size_cache` | Incremental size cache | `path_hash` | Storage analyzer | LRU 1 million rows |
| `file_digest_cache` | Content digests for fingerprints and transfers | `path_hash` | Transfer and fingerprints | LRU 2 million rows |
| `storage_analysis`, `storage_analysis_item` | Analysis results | `analysis_id`; `(analysis_id, item_id)` | Storage analyzer | 7 days |
| `cleanup_plan`, `cleanup_item` | Two-phase cleanup plans (SM-CLEANUP-PLAN), with fingerprints and per-item outcomes | `plan_id`; `(plan_id, item_id)` | Cleanup executor | 90 days (audit) |
| `quarantine_entry` | Quarantined items and purge schedule | `(plan_id, item_id)`; pending purge | Cleanup executor | 90 days after purge or restore |
| `cache_instance`, `cache_stat` | Cache registry and hourly statistics | `cache_id`; unique `(kind, compat_key)`; `(cache_id, period_start)` | Cache manager | Statistics: 90 days |
| `cas_blob`, `manifest` | Content-addressed store index and transfer manifests: inputs, outputs and output bases (pages stored as CAS blobs) | `sha256`; `(ref_count, last_used_at)`; `digest` | Transfer | LRU within the CAS quota; manifests expire with their attempts |
| `toolchain` | Detected toolchains | `(kind, path)` | Toolchain registry | Replaced on each scan |

### LAN, account, updates, integrations, support (and the retired guest tables)

| Table | Purpose | Key / indexes | Owner | Retention |
|---|---|---|---|---|
| `peer` | Discovered and paired peers, policies and status | `peer_node_id` | Peer manager | Removed peers: 30 days (blocked kept) |
| `pairing` | Pairing state (SM-PAIRING); nonces, commitments and SAS stay in memory | `pairing_id`; `(peer_node_id, created_at)` (rate limit) | Peer manager | 7 days |
| `offer` | Placement offers in both directions | `offer_id` | Placement | 7 days |
| `remote_attempt` | Executor-side remote attempts (SM-REMOTE-ATTEMPT), linked to the local `REMOTE` task | `remote_attempt_id`; `(state, lease_expires_at)` | Placement | With the local task |
| `guest_link` | **Retired by [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md); kept by the expand-only rule; never written.** Formerly: host-side links per WSL distribution (SM-GUEST-LINK, retired); link token in the OS secret store; the last pushed, acknowledged and reserved allocations (the reservation is written before each push), lease end and standalone allocation ([03](../architecture/03-resource-control.md) §6) | `distro`; unique `guest_node_id` | Guest manager (host) | Permanent |
| `host_link` | **Retired by [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md); kept by the expand-only rule; never written.** Formerly: guest-side pinned host and token hash, the last refused host, a host accepted by `TrustHost` for its next link, the last received allocation, lease end and standalone allocation, and the distribution's boot marker, so a restart during an outage keeps the same limits | singleton | Guest link (guest) | Permanent |
| `guest_grant` | **Retired by [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md); kept by the expand-only rule; never written.** Formerly: grants for guest attempts, with the host-side proxy task | `grant_id`; unique `request_id`; `state` | Scheduler (host) | 7 days after release |
| `account_link` | Account link: installation, credential reference, entitlement token, certificates, key sets | singleton | Cloud link | Until sign-out (deleted) |
| `sign_in_flow`, `phone_pairing` | Flow state without secrets | IDs | Cloud link | 1 day |
| `remote_command_log` | Every received remote command with its signature key ID and decision | `command_id`; `received_at` | Cloud link | 1 year |
| `push_outbox` | Push events waiting for the relay | `outbox_id` | Cloud link | 1 h (older events are dropped) |
| `update_state` | Updater state, rollback protection timestamp, bad versions (SM-UPDATE) | singleton | Updater | Permanent |
| `integration_plan`, `integration_write` | Integration plans and recorded writes, for exact removal (SM-INTEGRATION) | `plan_id`; `write_id`; `(client, path)` | Integration service | Writes: until removed plus 30 days |
| `support_bundle` | Local bundles and consent records | `bundle_id` | Support | 30 days |

**Retired guest data** ([AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md) §4). The tables `guest_link`, `host_link` and `guest_grant`, the column `attempt.guest_grant_id` and the guest value of `store_meta.node_role` stay in schema v1 because the schema is expand-only ([13](../architecture/13-distribution-updates.md) §9). No node writes them; a future major schema may drop them.

## 3. Data that is never stored

- **Environment values for secret-shaped names.** They are stored as presence only (R-EXE-017).
- **Raw hook payloads and transcripts.** Only pointers and redacted summaries are kept.
- **Pairing nonces, the SAS, sign-in code verifiers, device codes and QR secrets.** These stay in memory only. A node restart abandons the flow.
- **Refresh tokens, link tokens and bearer tokens.** They live in the OS secret store (Windows Credential Manager; Linux Secret Service, or a 0600 file when absent, reported as weaker). Tables keep only a reference name or a hash.

## 4. Size budget

- **Store growth target:** ≤ 50 MB per 10,000 attempts, excluding logs ([15](../architecture/15-performance-targets.md)). The largest contributors are `resource_sample` (downsampled after completion), `timeline_segment` and `process_record`. Caller environments do not grow with the attempt count: `env_snapshot` stores each distinct environment once (typically a few per shell session), and the growth benchmark submits from realistic captured shells (about 150 variables, 10–40 KB).
- **Gating.** AF-NODE-02 adds a CI benchmark that generates 10,000 synthetic attempts and asserts the bound.
