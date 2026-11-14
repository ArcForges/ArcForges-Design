# Node store (SQLite)

Schema: [node-store.sql](node-store.sql). It is checked by `tools/check_design.py`, which loads it into SQLite and runs the foreign-key and integrity checks.

## 1. Engine and file

- **File and journaling.** `<data root>/store/node.db`, using `Microsoft.Data.Sqlite` (SQLitePCLRaw bundle, AOT-verified in DesktopPlatform and ArcScope; re-verified by AF-NODE-02 on win-x64 and linux-x64). WAL journal, `foreign_keys=ON`, `synchronous=NORMAL`, and `busy_timeout=5000`.
- **Sealed-value erasure (MR-14).** The writer enables `secure_delete=ON` before updates and deletes. After a secret purge, a truncating WAL checkpoint removes older page images from the live database and WAL. `PurgeTaskRecord` performs this after its transaction commits, also on command replay; a checkpoint blocked by a read snapshot or an SQLite failure returns the existing `INTERNAL/internal` error with effect `HAPPENED`, because the logical purge is already committed. Retrying the identical command replays that logical result and attempts the checkpoint again. Housekeeping attempts the checkpoint on every purge pass, even when no new row is due, so a busy checkpoint is retried after readers leave, including after a node restart. Until it completes, an older read snapshot or file page can retain the sealed bytes; no successful physical-erasure claim is made for that interval. This concerns the live SQLite files, without a filesystem, storage-device or external-copy erasure guarantee. Retained backups follow MR-13.
- **Single writer.** The node's command processor ([02](../architecture/02-node-service.md) §1) is the only writer; readers use separate read-only connections.
- **Durability.** A receipt is returned only after its transaction commits (AD-0006 §1). `command_dedup` commits use `synchronous=FULL`, so an acknowledged `command_id` survives power loss.
- **Conventions:**
  - IDs are 16-byte UUIDv7 `BLOB`s;
  - instants are microseconds since the Unix epoch, the same unit as the Cloud D1 model;
  - enums are stored as their `arcforges.node.v1` proto numbers, so the contract and the store share one numbering;
  - protobuf columns hold serialized contract messages;
  - store-internal wrapper messages (`FindingActions`, `KeySet`, `BundleFiles`, `Reservoir`) are defined in `ArcForges.Node.Store` (`store.proto`, internal, not a public contract).
- **Migrations.** Forward-only and expand-only per release; contract steps are deferred ([13](../architecture/13-distribution-updates.md) §6). Backups are taken before every migration; they exclude sealed task values, and older retained copies are sanitized on store open (MR-13; [13](../architecture/13-distribution-updates.md) section 6). A backup restore therefore leaves those inputs unavailable. `store_meta` holds `schema_version` and `min_reader_version`.

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
| `task_secret` | Sealed values of secret-shaped environment variables, so queued tasks, restarts and retries run with the submitted environment ([04](../architecture/04-execution.md) §2). AES-256-GCM under the node data key from the OS secret store, with the task ID as associated data. | `task_id`; `purge_after` | Scheduler | Purged at `purge_after` (terminal + `storage.secret_retention_hours`, default 24 h) or on `PurgeTaskRecord`; then `RetryTask` fails with `STATE/secrets_unavailable`; retained backups contain tombstones and presence-only names, never sealed values (MR-13) |
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
| `remote_command_log` | Every received remote command with its signature key ID and decision. AF-CTR-05 target: kept for the unserved command kinds only; routed calls use `routed_call_log` | `command_id`; `received_at` | Cloud link | 1 year |
| `routed_call_log` | AF-CTR-05 delivered (schema step 2, §2a): every received center-routed call frame, verified or refused, with its decision, digests and sizes, never a payload | `log_id`; `received_at`; `call_id`; `command_id` | Cloud link | 1 year; executed reads 7 days; verification refusals 1 year or the newest 10,000, whichever is fewer |
| `push_outbox` | Push events waiting for the relay | `outbox_id` | Cloud link | 1 h (older events are dropped) |
| `update_state` | Updater state, rollback protection timestamp, bad versions (SM-UPDATE) | singleton | Updater | Permanent |
| `integration_plan`, `integration_write` | Integration plans and recorded writes, for exact removal (SM-INTEGRATION) | `plan_id`; `write_id`; `(client, path)` | Integration service | Writes: until removed plus 30 days |
| `support_bundle` | Local bundles and consent records | `bundle_id` | Support | 30 days |

**Retired guest data** ([AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md) §4). The tables `guest_link`, `host_link` and `guest_grant`, the column `attempt.guest_grant_id` and the guest value of `store_meta.node_role` stay in schema v1 because the schema is expand-only ([13](../architecture/13-distribution-updates.md) §9). No node writes them; a future major schema may drop them.

## 2a. Schema step 2 (AF-CTR-05)

*Added 2026-11-05 (Plan decisions PN-7 and Q8); delivered by AF-CTR-05 part N1, ArcForges #72.* Step 1 is [node-store.sql](node-store.sql) above the blank line before its `schema step 2` line of dashes, unchanged since `4823296` (SHA-256 `8f56a161…a649`); the ArcForges node store ships it verbatim as its migration step 1. Step 2 is the block beginning at `-- ------------------------------------------------------------------ schema step 2` and ending with the newline of its final `CREATE INDEX ix_routed_call_log__command ...;` line, before the additional blank separator and step-3 marker; the node store ships those bytes verbatim as migration step 2 (part N1). The single blank separator between steps is not part of either migration. Historical source `611dda6` is the definitive step-2 snapshot; extracting to the current file end is incorrect now that later steps are appended. The SQL's original target-status comment is retained as historical text to preserve the byte-exact shipped migration and schema-history checksum. Both steps are expand-only (§1, "Migrations").

- **`task.local_diagnostic`** (Plan decision Q8). `1` marks a diagnostic local submission ([AD-0021](../decisions/AD-0021-central-access-go-center.md) §5 as amended): a local `SubmitTask` from a HUMAN caller, or from a SCRIPT caller of a `--test-mode` node with the test allowance. A routed call never sets it, and every view labels such a task diagnostic.
- **`routed_call_log`** (Plan decision PN-7). `remote_command_log` does not fit routed calls: its key is a command ID, which reads do not carry and which a forged frame could occupy before the legitimate call arrives, its decisions have no value for a verification refusal, and its result is a `NodeCommandResult`. The routed calls get their own log, and `remote_command_log` stays for the unserved command kinds of `SendNodeCommand`.
  - **Rows.** One row per received call frame: every call that passed the node's verification ([11](../architecture/11-security-privacy.md) T-11) and every frame refused by it.
  - **Key.** A surrogate `log_id`. `call_id`, `signature_kid`, `method`, `caller`, `command_id` and the digests are written only for a verified call, so an unverified frame never names or occupies an ID; a CHECK leaves every one of them empty in a verification refusal. A refused frame is named by `frame_sha256` and its failed step only.
  - **Replay after a restart** (review finding N-5). N1 refuses at verification (`refusal_step` `call_replayed`) a call whose `call_id` is already logged, also after a node restart, because a logged row outlives the call's validity (at most 300 s plus the 120 s skew); the unique index holds one row per verified call ID. The row of a verified call is written at verification, before any effect, with decision `5` (pending), and updated to its final decision afterwards (C-N3), so of two concurrent copies of one call only the first passes; the second fails the unique index and is refused `call_replayed`. A new call that repeats a logged command ID, the center's resend after an uncertain outcome, is not a replay: it carries a new call ID, passes verification, and the node's command deduplication replays the recorded outcome (Plan CTR5-RTE-03).
  - **Decision.** `1` executed: the TaskService handler ran, and its answer, a success or the handler's own refusal (`refusal_code`), is the signed result. `2` refused by the center-routed policy or the permission matrix, an approval raised included ([11](../architecture/11-security-privacy.md) §1, "Center-routed callers"). `3` refused at verification: `refusal_step` names the step (closed vocabulary, part N1) and `refusal_code` is `AUTHENTICATION/signature_invalid` (with `call_replayed` for a replay, C-N3) or `STATE/expired`. `4` expired before the effect: verified, but the re-check of the expiry immediately before the effect failed (`STATE/expired`). `5` verified, outcome pending: the row written at verification; a row left at `5` after a crash names a verified call whose outcome was not recorded, which command deduplication covers for a mutation.
  - **What it never holds.** No request or response payload, argv, working directory, environment or output, and no refusal message or details: only the refusal's `CATEGORY/code`, digests and sizes (Plan decision PN-6).
  - **Retention.** Submit, cancel and every refused call: 1 year, like `remote_command_log`. Executed reads: 7 days, because a client that follows output reads often. Refusals at verification: 1 year or the newest 10,000 rows, whichever is fewer, so a flood of forged frames cannot grow the store.
- **What a routed read returns** of a task's specification is decided in [11](../architecture/11-security-privacy.md) §1, "Center-routed callers" (Plan decision PN-8, the privacy policy `remote_command_lines`).

## 2b. Schema step 3 — AF-CTR-06 implementation candidate

This is a reviewed implementation candidate, not delivered AF-CTR-06 acceptance. The step-3 block appended to [node-store.sql](node-store.sql) is byte-identical to ArcForges implementation source `68d1bc340edfd08d590f87af8d2307711f6b1a2d`, `src/ArcForges.Node.Store/Schema/0003-schema-step-3.sql`. Steps 1 and 2 and their released checksums remain unchanged. Step 3 keeps `min_reader_version=1`; this database read compatibility does not establish complete older-binary protocol or rollback compatibility.

Step 3 adds the bounded metadata-only `routed_file_call_log` for methods 9–20, plus `routed_verified_call_id` shared with the immutable task log. The migration holds its immediate writer transaction while backfilling all retained verified task IDs and installing database triggers. Verification refusals do not reserve caller-supplied IDs. Both tables explicitly abort a duplicate global call ID or replacement of an existing log key before insertion; `INSERT OR IGNORE` or `OR REPLACE` cannot discard an old receipt or suppress the registry check. Updating either key, including SQLite's `rowid`, `_rowid_` and `oid` aliases, is prohibited. Retention deletes only the removed row's matching registry ownership in the same transaction. The file log records no request or response bodies; verified requests are 1–245,760 serialized bytes, executed responses are 1–1,040,384 bytes with paired SHA-256 and size, and non-executed rows have no response observation.

SQLite exposes both an unspecified automatic row ID and an explicit `-1` as `NEW.log_id=-1` in a BEFORE trigger. If a table contains an explicit retained `-1` row, the strict replacement guard therefore refuses automatic insertion into that table too. It preserves the receipt until normal retention deletes it; it does not rewrite or prematurely purge the row. When no retained `-1` row exists, ordinary product-generated positive auto IDs are unaffected; a retained `-1` blocks automatic insertion even if SQLite would otherwise allocate a positive ID. This availability boundary is explicit, not evidence that every schema-valid legacy database or older binary has full protocol compatibility. Current code checks the shared registry before recording an old task call and returns its ordinary signed `call_replayed` refusal and refusal audit for a verified cross-log replay. A genuinely older binary only checks its old table; a cross-log collision can instead fail closed at SQLite without that normal signed answer. Actual older-binary rollout and supported rollback remain unproven integration work and cannot be inferred from `min_reader_version` or a synthetic SQL writer.

`workspace_root_identity` stores a versioned bounded native identity and canonical path separately from the unchanged workspace row. One exact `(platform, native_identity)` byte tuple has at most one active registration; a released tuple can be registered again. Unique registration of the same actually opened native object additionally requires the still-unimplemented canonical identity encoding and its native equivalence tests. No identity is invented for a legacy registration. This table alone does not implement registration, native identity encoding, Git metadata, policy or root verification.

Native author and independent checks of these components are recorded separately from formal delivery: actual SQLite migration/constraint/concurrency cases, existing retention, and a loopback signed cross-log rejection exercise the real node verifier, crypto and database; their synthetic file receipt, FakeCenter peer and manual clock do not prove FileService or a real-center file route. Consumer full profiles, Windows checks at the corrected source, real platform/file integration and strict successful cleanup remain required. [06a](../architecture/06a-node-files.md) still governs all behavior and does not accept enforcement-unavailable refusal as positive cleanup acceptance.

## 2c. Further AF-CTR-06 schema — still required

The file-operation journal/receipts, created-object ownership and restricted removal plans remain target work after step 3; they are not implemented by the call-ID registry or root-identity table. Add actual versioned tables with the implementation and a verified immutable checksum, preserving every released predecessor. The journal binds command ID, request digest, specific caller, object identities, preconditions, effect phase and metadata outcome; it contains neither file bodies nor search strings. Unresolved records and the target hold survive restart until a local HUMAN acknowledges them; completed receipts and operation status are retained for at least 24 hours from first execution, longer for an unresolved UNKNOWN until local HUMAN acknowledgment; acknowledgment retains terminal metadata at least through the original 24-hour window. The center's maximum 23-hour-52-minute routed replay window prevents execution after that retention, even after lost settlement or restart. Ownership lives until invalidated or unregistered, plans expire after 60 minutes, and audit/verification logs follow 06a and §2a. Any private staging file is separately access-restricted and handled by 06a §6, never embedded in SQLite audit, receipt or backup as a payload. New-file-log retention and service integration also remain implementation work; a component test deleting its own fixture rows does not establish that retention job.

## 3. Data that is never stored

- **Environment values for secret-shaped names.** They are stored as presence only (R-EXE-017).
- **Raw hook payloads and transcripts.** Only pointers and redacted summaries are kept.
- **Pairing nonces, the SAS, sign-in code verifiers, device codes and QR secrets.** These stay in memory only. A node restart abandons the flow.
- **Refresh tokens, link tokens and bearer tokens.** They live in the OS secret store (Windows Credential Manager; Linux Secret Service, or a 0600 file when absent, reported as weaker). Tables keep only a reference name or a hash.

## 4. Size budget

- **Store growth target:** ≤ 50 MB per 10,000 attempts, excluding logs ([15](../architecture/15-performance-targets.md)). The largest contributors are `resource_sample` (downsampled after completion), `timeline_segment` and `process_record`. Caller environments do not grow with the attempt count: `env_snapshot` stores each distinct environment once (typically a few per shell session), and the growth benchmark submits from realistic captured shells (about 150 variables, 10–40 KB).
- **Gating.** AF-NODE-02 adds a CI benchmark that generates 10,000 synthetic attempts and asserts the bound.
