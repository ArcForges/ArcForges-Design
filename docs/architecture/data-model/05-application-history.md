# Application-Owned Assistant History

Authority: [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012). Applies to Platform Assistant.Persistence.Sqlite and Android Room's equivalent owner/projection rules. It extends [desktop model 02](02-desktop-data-model.md) without changing Notes/Scope/Slate professional canonical data. Public operations and new fields are in [annex 10](../contracts/10-application-scope-and-streams.md).

## 1. Partition and ownership

Desktop path is `<OS private app-data>/ArcForges/<product>/<profileKey>/assistant/history.sqlite3`. `profileKey` is a stable opaque hash of realm/account/workspace (or a device-local anonymous profile ID), not an email/path supplied by a server. Files use the OS-user-only permissions and existing secure-storage policy. One application composition root owns its connections, writer queue, history service, Cloud channel and credentials. Different products neither open nor attach each other's databases. Windows of one application share committed history, not editor drafts. Product canonical stores stay separate and are linked by resource IDs/revisions, never cross-database FKs or transactions.

Desktop defaults to `local`. Android own-chat defaults to `cloud` with a clear first-use explanation and can choose `local`; Web own-chat uses `cloud`, with memory-only temporary sessions and no offline canonical browser database. Cloud conversation scope is `(realm, account/workspace visibility, productId)`; companion-owned chats use productId=`companion`. A mobile view of a desktop Cloud conversation retains that desktop productId. Online presence never grants access to local-only history.

## 2. Fixed history modes

| Mode | Canonical body | AI handling | Remote visibility / deletion |
|---|---|---|---|
| Local | this installation's SQLite/Room | explicitly selected turn/context sent to Cloud execution; encrypted transient R2 content, bounded resume, no canonical Cloud Chat/message/index rows | absent from other installations; deleting history removes local bodies/indexes and requests immediate transient purge |
| Cloud | Cloud Chat in D1/R2 under one product scope; local acknowledged projection plus pending work | normal admitted Cloud turn/Harness, canonical commit before complete state | available only to authorized clients explicitly selecting this product scope; tombstone sync and existing retention/export rules |
| Temporary | live UI memory; no history/search/draft body persisted | existing isolated ephemeral execution; no memory/project writeback | closes with purge request; failsafe expiry≤24h, active deletion target≤1h; content absent from durable business backups |

All modes use the same explicit egress, model admission, credits, approval and task semantics. “Local history” never means a local model or that selected content stays off the server. Native offline use permits history/search/draft/edit/export already hydrated locally; a new AI send needs network and is visibly pending until admitted. Never silently upgrade local to Cloud or normal to temporary.

Local execution stores only IDs, authorization, effect/usage/settlement and expiry facts in durable Cloud tables. Input/output bodies are envelope-encrypted R2 objects under an ephemeral key held in the run DO and excluded from backup/export/search; expiry or explicit purge denies body access immediately and schedules deletion of the key and objects. DO storage is durable for bounded recovery, but is not independently backed up with business history. Provider internal retention is disclosed separately; deletion does not promise immediate physical erasure of provider replicas. Restrictive purge/expiry fences are replayed before any restored environment reopens, including after a DO restore. Workers AI retention/transparency disclosure stays current. Terminal output is retained until client acknowledgement plus 1h, or 24h from terminal state, whichever occurs first; running executions follow existing run limits. On missing/expired output, the client shows an interrupted/unavailable result and may preserve its local prefix, never fabricating completion. Financial/audit metadata retains its existing policy.

## 3. Physical SQLite profile and schemas

Use WAL, `foreign_keys=ON`, `busy_timeout=5000`, `synchronous=FULL`; one serialized write queue and bounded concurrent read connections. Migration runs before UI access under a single application lock; unknown writable schema refuses writes and preserves/exportable evidence. OS private storage and disk encryption expectations follow security 08; this is not a claim of built-in SQLite encryption. No raw content is written to logs. Store schema manifest fixes each table/column/index and migration hash. Generated message-part/project/profile/skill/resource records from registry 04 are the payload authority; the physical assistant schema below is the only local table authority.

```sql
CREATE TABLE assistant_conversation (
 id TEXT PRIMARY KEY, product_id TEXT NOT NULL,
 mode TEXT NOT NULL CHECK(mode IN ('local','cloud')),
 title TEXT NOT NULL, revision INTEGER NOT NULL CHECK(revision>=1),
 cloud_id TEXT UNIQUE, updated_us INTEGER NOT NULL, deleted_us INTEGER,
 CHECK((mode='local' AND cloud_id IS NULL) OR (mode='cloud' AND cloud_id IS NOT NULL))
);
CREATE INDEX assistant_conversation_list
 ON assistant_conversation(deleted_us,updated_us DESC,id);
CREATE TABLE assistant_branch (
 id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL REFERENCES assistant_conversation(id),
 parent_id TEXT REFERENCES assistant_branch(id), fork_message_id TEXT,
 revision INTEGER NOT NULL CHECK(revision>=1)
);
CREATE TABLE assistant_message (
 id TEXT PRIMARY KEY, branch_id TEXT NOT NULL REFERENCES assistant_branch(id),
 ordinal INTEGER NOT NULL, role TEXT NOT NULL,
 body_proto BLOB NOT NULL, source_kind TEXT NOT NULL,
 created_us INTEGER NOT NULL, UNIQUE(branch_id,ordinal)
);
CREATE TABLE assistant_draft (
 window_id TEXT NOT NULL, conversation_id TEXT NOT NULL REFERENCES assistant_conversation(id),
 body_proto BLOB NOT NULL, revision INTEGER NOT NULL, updated_us INTEGER NOT NULL,
 PRIMARY KEY(window_id,conversation_id)
);
CREATE TABLE assistant_turn (
 command_id TEXT PRIMARY KEY, request_hash TEXT NOT NULL,
 conversation_id TEXT NOT NULL REFERENCES assistant_conversation(id),
 expected_revision INTEGER NOT NULL, execution_id TEXT UNIQUE,
 state TEXT NOT NULL, output_cursor TEXT, output_prefix BLOB,
 terminal_hash TEXT, committed_message_id TEXT, revision INTEGER NOT NULL
);
CREATE TABLE assistant_receipt (
 command_id TEXT PRIMARY KEY, request_hash TEXT NOT NULL,
 result_proto BLOB NOT NULL, committed_us INTEGER NOT NULL
);
CREATE TABLE assistant_outbox (
 command_id TEXT PRIMARY KEY, kind TEXT NOT NULL, body_proto BLOB NOT NULL,
 state TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, next_attempt_us INTEGER
);
CREATE TABLE assistant_history_import (
 local_id TEXT PRIMARY KEY REFERENCES assistant_conversation(id),
 import_id TEXT NOT NULL UNIQUE, cloud_id TEXT, snapshot_hash TEXT NOT NULL,
 snapshot_revision INTEGER NOT NULL, state TEXT NOT NULL, last_error TEXT
);
CREATE TABLE assistant_attachment (
 id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL REFERENCES assistant_conversation(id),
 message_id TEXT REFERENCES assistant_message(id), mode TEXT NOT NULL,
 resource_id TEXT, external_locator_proto BLOB, availability TEXT NOT NULL,
 display_name TEXT NOT NULL,
 CHECK((mode='managed' AND resource_id IS NOT NULL AND external_locator_proto IS NULL)
 OR (mode='externalReference' AND resource_id IS NULL AND external_locator_proto IS NOT NULL))
);
CREATE TABLE assistant_project (
 id TEXT PRIMARY KEY, body_proto BLOB NOT NULL, revision INTEGER NOT NULL, deleted_us INTEGER
);
CREATE TABLE assistant_conversation_project (
 conversation_id TEXT PRIMARY KEY REFERENCES assistant_conversation(id),
 project_id TEXT NOT NULL REFERENCES assistant_project(id)
);
CREATE TABLE assistant_profile (
 id TEXT NOT NULL, revision INTEGER NOT NULL, body_proto BLOB NOT NULL,
 active INTEGER NOT NULL CHECK(active IN (0,1)), PRIMARY KEY(id,revision)
);
CREATE UNIQUE INDEX assistant_profile_head ON assistant_profile(id) WHERE active=1;
CREATE TABLE assistant_skill (
 id TEXT NOT NULL, revision INTEGER NOT NULL, body_proto BLOB NOT NULL,
 active INTEGER NOT NULL CHECK(active IN (0,1)), PRIMARY KEY(id,revision)
);
CREATE UNIQUE INDEX assistant_skill_head ON assistant_skill(id) WHERE active=1;
CREATE TABLE assistant_context (
 id TEXT PRIMARY KEY, owner_kind TEXT NOT NULL CHECK(owner_kind IN ('conversation','project')),
 owner_id TEXT NOT NULL, lifetime TEXT NOT NULL, target_product TEXT NOT NULL,
 target_proto BLOB NOT NULL, added_us INTEGER NOT NULL
);
CREATE TABLE assistant_task_projection (
 task_id TEXT PRIMARY KEY, authoritative_revision INTEGER NOT NULL,
 body_proto BLOB NOT NULL, projected_us INTEGER NOT NULL
);
CREATE TABLE assistant_compaction (
 id TEXT PRIMARY KEY, branch_id TEXT NOT NULL REFERENCES assistant_branch(id),
 through_ordinal INTEGER NOT NULL, source_hash TEXT NOT NULL, summary_proto BLOB NOT NULL,
 model_id TEXT NOT NULL, policy_version TEXT NOT NULL, summary_hash TEXT NOT NULL,
 created_us INTEGER NOT NULL, UNIQUE(branch_id,through_ordinal,source_hash,policy_version)
);

```

All IDs, role/source/turn state and serialized message parts validate against the existing typed registry. `body_proto` is an explicit versioned generated message, never arbitrary JSON: MessageView/MessageDraft for message/draft, ChatProjectRecord for project, AgentProfile/SkillRecord for profile/skill, TaskSnapshot for task projection, CompactionRecord for summary and ContextRef for target_proto. Context owner_kind/id is checked against the matching conversation/project in the same transaction; no orphan or foreign-product context can commit. Profile/skill version rows are immutable after use; only active-head flags change. Attachments never inline file bytes into messages. The store metadata records the one allowed productId and the open path is validated before any query; products cannot override it. Branch parent/fork must belong to the same conversation; validate this in the transaction. Committed messages are immutable: editing creates a branch and new message. Draft and streaming prefix are mutable, separately typed, and never masquerade as a committed message. Attachments/references, projects/profiles/skills, compaction and task projections use the tables above. Common product journals/resources remain model 02 §1; no cross-database FK is assumed. Assistant-owned FTS5 contains only non-deleted committed normal history in this partition; temporary content is never indexed.

## 4. Required queries and atomic operations

| Operation | Fixed behavior / SQL shape |
|---|---|
| List | `WHERE deleted_us IS NULL` and keyset `(updated_us < :t OR (updated_us=:t AND id>:id)) ORDER BY updated_us DESC,id LIMIT :limit`; first page omits cursor, default 50/max 100; scope/query-bound cursor. |
| Read branch | resolve parent chain only to the frozen fork message; merge immutable prefix and branch-owned messages by ordinal; refuse corrupt/cyclic lineage with evidence preserved. |
| Rename / trash | one `BEGIN IMMEDIATE` transaction: check expected revision and mode, update title/tombstone and revision, update index/journal, insert receipt; Cloud mode queues the typed proposal and keeps acknowledged vs pending versions separate. |
| Submit | validate frozen context/egress and draft revision; transaction creates immutable user message/turn and outbox record, clears only the submitted window draft if its revision still matches. Network starts after commit. Offline drafts remain visible; no pre-admission “sent” claim. |
| Retry send | reuse command ID/hash until receipt proves absent/same outcome; changed content is a new turn/branch, never overwrites a sent message. |
| Apply output | verify contiguous cursor/hash, journal prefix; on terminal canonical result, transaction inserts one immutable assistant message, terminal receipt and clears prefix/outbox. Duplicate terminal frame is no-op; gap fetches authoritative output. |
| Fork | transaction freezes original fork message, creates branch/revision and independent draft; parent history cannot be edited through the child. |
| Delete / GC | tombstone first and hide from list/search; stop new work, separately cancel active executions; delete eligible bodies only after required Cloud ack/retention. A failed cancel does not recreate history. GC resolves live refs and cannot delete product-owned canonical resources. |
| Export | snapshot one committed revision; local exports from own store, Cloud exports through owned API; report missing/unhydrated resources; no implicit promotion/upload. |

Transactions include journal/receipt/outbox and are committed before acknowledging durable UI changes. No transaction waits for Cloud, a file dialog, native parser or product database write. Local revision and Cloud revision remain distinct; pending work/conflict lineage follows model 02. Sync does not overwrite an unsent per-window draft. Same conversation can be viewed in multiple windows; a submitted mutation carrying a stale revision offers refresh/fork rather than last-writer-wins loss.

<a id="context-window-and-compaction"></a>
### Deterministic context window and compaction

Resolve the selected branch at one revision, including its inherited prefix through each frozen fork point. Preserve original message IDs/roles/ordinals and complete tool-call/result pairs. The selected model's admitted context limit minus maximum output, system/tool schemas and fixed framing allowance is the input budget; use its published tokenizer/version or the conservative UTF-8-byte upper bound if a local tokenizer is unavailable. Select the most recent complete turns that fit plus all protected content from [Harness HC-09](../17-agent-harness.md#rule-hc-09). Never drop a protected item or turn half to make the counter fit. Authorized resource context consumes the same budget.

If older unprotected turns are omitted, attach the newest valid CompactionRecord covering exactly that prefix/source hash. No valid summary means explicit compactionRequested; the server compacts only admitted unprotected history under its platform-funded compaction rules, returns the typed record and retries assembly without silently changing the current user request. Cloud mode stores it as derived chat.compaction_record; local mode commits assistant_compaction only after branch/hash verification. Temporary summary stays in the run's ephemeral storage. User-edit/fork/source-policy changes invalidate affected summaries; summaries are hints, never approvals, tool receipts or system instructions.

Worked vectors with an input budget of 8,000 units: protected 1,000 + recent 2,000 + old 3,000 fits without compaction; protected 1,000 + recent 3,000 + old 8,000 compacts the old prefix to ≤4,000, otherwise visibly refuses until a smaller selection is chosen; protected 9,000 alone returns validation.invalid_request with reason context.protected_overflow without model dispatch or debit. A summary through ordinal 20 cannot be used after editing/forking at ordinal 12 unless its covered prefix hash still matches. Partial tool pairs are never separately counted/admitted. The annex 10 envelope/object limits are additional hard bounds, independent of tokenizer units.

Local export uses the same `assistant-history.v1` archive as promotion, from a committed snapshot; draft export is a separately labelled optional recovery file, never silently included. Validate round-trip branch topology, content origins, immutable resource hashes and missing-resource report. Import remaps IDs, preserves sources and grants no capability. Export/import does not require Cloud or change local mode.

## 5. Opt-in promotion and disabling Cloud history

`Save to Cloud` requires account/workspace selection, scope disclosure and explicit confirmation listing conversation/messages/attachments and retention. Snapshot a local conversation revision; create a durable local import journal, request an import ID, upload a verified versioned archive through the normal admitted R2 transfer, stage records in Cloud, then finalize once. Import is invisible in normal chat/search until its manifest, references, counts and checksums verify. Cloud transaction flips one manifest visibility pointer and creates the receipt; it does not require inserting an unbounded history in one D1 batch. Chunk staging uses ≤100 records/batch; archive admission uses existing resource quota and bounded chunk profile, with clear size/unsupported-item refusal and no partial visible import.

Finalization is idempotent by `(scope, importId, manifestHash)`, yields a new Cloud conversation ID. Local commit switches to Cloud mode only if the local revision still equals the snapshotted revision; if the user edited meanwhile, retain the local conversation and present the imported snapshot as a separate Cloud copy. A crash after Cloud finalization is recovered by import-status lookup; never upload a second copy automatically. Cancellation before visibility removes staged records/pins under normal expiry (24h); after finalization it requires normal Cloud deletion. Promotion includes only this conversation, never every local conversation/project.

`Keep new chats local` changes only the creation default. For an existing Cloud conversation, `Make local copy` downloads/verifies all selected content and creates a new local ID; the Cloud original remains until separately deleted with explicit consequences. Do not offer a misleading “unsync” toggle implying instant removal from all backups/devices. Exports, account deletion and retention disclosures distinguish local copies, Cloud history and legally retained usage records.

## 6. Profile switch, crash and upgrade

Switching account/workspace/realm cancels streams, locks the old store/session, clears previews/clipboard grants and opens the new partition. Pending old-profile work remains sealed; it is never sent under the new account. Logout offers retain OS-private app data or explicitly remove local data after export opportunity; access to a retained signed-in partition requires that account to authenticate again. Anonymous history remains device-local; sign-in does not silently attach/upload it. Android process death restores persisted drafts/pending receipts; temporary sessions show expired/interrupted rather than resurrecting bodies. Web logout clears memory and allowed cached identifiers, not server history.

Schema migration backs up/verifies the existing database, applies numbered transactional steps, checks integrity and publishes the new schema marker only after success. A version unable to read/write the resulting schema refuses downgrade and uses the updater interlock. Tests cover power loss at every local commit/promotion stage, disk full, missing objects, two windows, account switch, same product on two devices and different products on one device. SQLite tests are E2 mechanism evidence; packaged AOT/Room/Cloud consumers supply E3/E4 acceptance.

## 7. Cloud metadata and transient execution closure

Chat turns and Tasks carry `product_id`, `history_mode`, `origin_installation_id?`, `transient_input_ref?` and `transient_output_receipt_id?`. Cloud mode retains existing conversation/message FKs and canonical output rules. Local/temporary mode requires the origin installation, null Cloud conversation/input/final-message FKs, and a transient input reference. The run/owner discriminator remains the existing ChatTurn or Task; no invented Task is needed for ordinary chat. Scope is immutable after admission. A new local agent execution uses the same Task state machine/approval/metering with local history mode.

`execution_transient_receipt(id PK, owner_kind, owner_id, run_id, attempt_id, product_id, origin_installation_id, output_hash, output_size, output_ref, key_ref, state, committed_at, expires_at, acknowledged_at?, purged_at?)` is metadata only; unique(owner_kind,owner_id,run_id,attempt_id) prevents duplicate output settlement. The actual input/output/iteration content and content-bearing tool arguments/results live in encrypted transient R2 objects. Rows/checkpoints/logs contain IDs, hashes, typed effect states and generic labels, never copied prompt text, titles derived from it or plaintext arguments. Existing Task/Chat storage adapters hydrate the admitted typed payload from those references after current authorization. Explicit user-authorized professional tool effects and deliberately saved resources remain in their professional owner's store under that owner's retention; local chat deletion does not undo them.

For a terminal local/temporary outcome, first verify the immutable encrypted object and content-origin/hash record; then a guarded D1 batch writes the output receipt, owner outcome, provider/usage receipt and settlement transition together. It creates no Cloud Chat message or history Sync change. Client acknowledgement is sent only after its own SQLite terminal commit and may shorten retention; it is not a condition for correct charging. Missing/expired/purged bytes never reverse established usage, invent a no-answer outcome or silently rerun a paid request. The UI distinguishes an execution outcome from body availability. A lost DO key can make transient content unavailable even when outcome/financial receipts survive; this is an explicit recovery limit, not durable-history success.

Application presence has durable identity/trust/install records in D1. Frequent heartbeat timestamps/capability availability live in a scope-bound DO, expire after 30s and cannot authorize a tool by themselves. New registration obtains an epoch through guarded durable owner state; DO loss is rebuilt as offline until a current verified heartbeat. A stale instance cannot resurrect its predecessor's lease.

History imports expire24h after Begin unless already committed. Finalize transitions staging→verifying→ready→committed; verification failure→failed, precommit Cancel→canceled, timeout→expired. Transition and epoch checks prevent a canceled/expired verifier from activating a manifest. All Chat list/get/search/sync readers filter the committed visibility pointer. Records staged in earlier batches cannot leak through an alternate read path.
