# Application-Owned Assistant History

Authority: [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012). Applies to Platform Assistant.Persistence.Sqlite and Android Room's equivalent owner/projection rules. It extends [desktop model 02](02-desktop-data-model.md) without changing ArcScope professional canonical data. Public operations and new fields are in [annex 10](../contracts/10-application-scope-and-streams.md).

## 1. Partition and ownership

Desktop path is derived only by `Path.Combine(options.DataRoot.GetProfileDirectory(partition), "assistant", "history.sqlite3")` using the shipped typed AssistantDataRoot. Its layout is `<platformDataRoot>/<product>/<installation N>/profiles/<profile N>/assistant/history.sqlite3`; platformDataRoot is already the trusted OS-private base and may contain ArcForges, so no second fixed ArcForges segment is appended. Profile GUID is identity only; a current owner profile authority explicitly binds DeviceLocal or Authenticated owner/realm/workspace scope. No account authority is inferred from the GUID and no email/path is supplied by a server. Files use the OS-user-only permissions and existing secure-storage policy. One application composition root owns its connections, writer queue, history service, Cloud channel and credentials. Different products neither open nor attach each other's databases. Windows of one application share committed history, not editor drafts. Product canonical stores stay separate and are linked by resource IDs/revisions, never cross-database FKs or transactions.

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
 view_proto BLOB NOT NULL, local_revision INTEGER NOT NULL CHECK(local_revision>=1),
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
 tool_call_id TEXT, tool_result_for TEXT,
 created_us INTEGER NOT NULL, UNIQUE(branch_id,ordinal)
);
CREATE TABLE assistant_draft (
 draft_id TEXT PRIMARY KEY, window_id TEXT NOT NULL,
 conversation_id TEXT REFERENCES assistant_conversation(id),
 body_proto BLOB NOT NULL, revision INTEGER NOT NULL CHECK(revision>=1), updated_us INTEGER NOT NULL,
 UNIQUE(window_id,conversation_id)
);
CREATE UNIQUE INDEX assistant_draft_unbound_window
 ON assistant_draft(window_id) WHERE conversation_id IS NULL;
CREATE TABLE assistant_turn (
 command_id TEXT PRIMARY KEY, request_hash TEXT NOT NULL,
 conversation_id TEXT NOT NULL REFERENCES assistant_conversation(id),
 expected_revision INTEGER NOT NULL, execution_id TEXT UNIQUE,
 state TEXT NOT NULL, output_cursor TEXT, output_prefix BLOB,
 turn_proto BLOB, progress_proto BLOB, run_proto BLOB,
 owner_kind TEXT, owner_id TEXT, configuration_proto BLOB,
 terminal_committed INTEGER NOT NULL DEFAULT 0 CHECK(terminal_committed IN (0,1)),
 output_position_proto BLOB, output_offset TEXT,
 terminal_hash TEXT, committed_message_id TEXT, revision INTEGER NOT NULL,
 CHECK((owner_kind IS NULL AND owner_id IS NULL) OR
       (owner_kind IS NOT NULL AND owner_kind IN ('chatTurn','task') AND owner_id IS NOT NULL)),
 CHECK((output_position_proto IS NULL AND output_offset IS NULL) OR
       (output_position_proto IS NOT NULL AND output_offset IS NOT NULL)),
 UNIQUE(owner_kind,owner_id)
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

-- Derived assistant-owned metadata, semantic journal and committed-history index.
CREATE TABLE assistant_store_meta (
 singleton INTEGER PRIMARY KEY CHECK(singleton=1),
 database_id TEXT NOT NULL UNIQUE CHECK(length(database_id)=32 AND database_id NOT GLOB '*[^0-9a-f]*'),
 product_id TEXT NOT NULL CHECK(product_id IN ('arcscope','companion')),
 installation_id TEXT NOT NULL CHECK(length(installation_id)=32 AND installation_id NOT GLOB '*[^0-9a-f]*'),
 profile_id TEXT NOT NULL CHECK(length(profile_id)=32 AND profile_id NOT GLOB '*[^0-9a-f]*'),
 profile_kind TEXT NOT NULL CHECK(profile_kind IN ('deviceLocal','authenticated')),
 principal_binding TEXT NOT NULL CHECK(length(principal_binding)=64 AND principal_binding NOT GLOB '*[^0-9a-f]*'),
 schema_version INTEGER NOT NULL CHECK(schema_version>=0 AND schema_version<=4294967295),
 migration_hash TEXT NOT NULL CHECK(length(migration_hash)=64 AND migration_hash NOT GLOB '*[^0-9a-f]*'),
 manifest_hash TEXT NOT NULL CHECK(length(manifest_hash)=64 AND manifest_hash NOT GLOB '*[^0-9a-f]*')
);

CREATE TABLE assistant_journal (
 sequence INTEGER PRIMARY KEY AUTOINCREMENT CHECK(sequence>=1),
 command_id TEXT NOT NULL UNIQUE REFERENCES assistant_receipt(command_id) DEFERRABLE INITIALLY DEFERRED,
 operation TEXT NOT NULL CHECK(operation IN (
  'history.create','history.queue','history.edit','history.trash','history.fork',
  'draft.save','draft.discard','turn.submit','turn.prefix','history.acknowledge',
  'turn.complete','turn.facts','outbox.update','outbox.quarantine','outbox.acknowledge',
  'history.import','catalog.put','catalog.remove')),
 semantic_sha256 TEXT NOT NULL CHECK(length(semantic_sha256)=64 AND semantic_sha256 NOT GLOB '*[^0-9a-f]*'),
 committed_us INTEGER NOT NULL CHECK(committed_us>=0),
 profile_generation TEXT NOT NULL CHECK(length(profile_generation) BETWEEN 1 AND 20
  AND profile_generation NOT GLOB '*[^0-9]*' AND substr(profile_generation,1,1) BETWEEN '1' AND '9'),
 principal_binding TEXT NOT NULL CHECK(length(principal_binding)=64 AND principal_binding NOT GLOB '*[^0-9a-f]*')
);
CREATE INDEX assistant_journal_command ON assistant_journal(command_id,sequence);

CREATE VIRTUAL TABLE assistant_message_fts USING fts5(
 message_id UNINDEXED,
 conversation_id UNINDEXED,
 branch_id UNINDEXED,
 committed_text,
 tokenize='unicode61 remove_diacritics 2'
);

```

All IDs, role/source/turn state and serialized message parts validate against the existing typed registry. `body_proto` is an explicit versioned generated message, never arbitrary JSON: MessageView/MessageDraft for message/draft, ChatProjectRecord for project, AgentProfile/SkillRecord for profile/skill, TaskSnapshot for task projection, CompactionRecord for summary and ContextRef for target_proto. Context owner_kind/id is checked against the matching conversation/project in the same transaction; no orphan or foreign-product context can commit. Profile/skill version bodies are immutable from insertion; exact-byte replay is allowed, changed content requires a new version, and only active-head flags change. Attachments never inline file bytes into messages. The store metadata records the one allowed productId and the open path is validated before any query; products cannot override it. Branch parent/fork must belong to the same conversation; validate this in the transaction. Committed messages are immutable: editing creates a branch and new message. Draft and streaming prefix are mutable, separately typed, and never masquerade as a committed message. Attachments/references, projects/profiles/skills, compaction and task projections use the tables above. Common product journals/resources remain model 02 §1; no cross-database FK is assumed. Assistant-owned FTS5 contains only non-deleted committed normal history in this partition; temporary content is never indexed.


### 2026-10-06 production payload and draft identity amendment

Stable draft_id is the shipped APP07 AssistantDraftId authority: recovery, compare-and-swap and discard address it independently of conversation. An unattached unsent editor has null conversation_id and one unbound draft per window; never manufacture a hidden canonical conversation. Draft identity survives authorized window remapping. Writes compare the exact expected revision and persist expected+1.

view_proto is the complete versioned generated ConversationView; id/product/mode/title/acknowledged revision and other duplicated scalar facts agree with it. local_revision fences local stale windows/pending work and remains distinct from the acknowledged View.Revision. Cloud pending proposals never overwrite acknowledged canonical rows or view payloads: existing assistant_outbox is their sole authority and pending UI projection is explicit. Local mode uses the authored checked signed64 revision.

turn_proto/progress_proto/run_proto preserve actual generated ChatTurnView, Events.ExecutionProgress and RunView, with null meaning no such fact has been received. Validate duplicated command/conversation/revision/state/execution identities. Never fabricate remote views, attempts, streams, success or completion. output_prefix remains a separately typed mutable MessageDraft; contiguous cursor/hash validation and one immutable terminal message remain required. Existing outbox kinds use closed versioned actual generated named Chat requests or ExecutionServiceStartTransientTurnRequest, retaining exact RequestMeta command/precondition/application/recovery scope; generic Sync/ChangeProposal client writes are not substitutes for these authored owner APIs.

AST01 produces one real reusable Core session factory and the complete physical store, including migrations, actual typed history/turn/draft services, memory-only temporary sessions, and the actual supplied authenticated generated-call-invoker backend. Complete component behavior and contracts advance independently of unavailable remote system acceptance. Numbered initial/pending migrations are allocated by the integration owner, never by rewriting a merged migration.


### Derived identity, semantic journal and index support

assistant_store_meta binds the actual product/installation/profile and deviceLocal/authenticated kind plus immutable principal_binding before any domain query on reopen. principal_binding is the lowercase SHA256 of the trusted profile authority's canonical versioned actual principal snapshot; its profile/realm/principal/type fields are defined by the typed owner and complete bytes are compared through that authority. It is a binding digest, never authentication or a permission grant, and a partition GUID alone cannot authorize reopening. DeviceLocal never fabricates a Cloud UserId. Only supported schema/migration/manifest identity and integrity publish a successful service; schema0 is migration-only. Unknown schema/downgrade preserves database/sidecars as evidence and refuses writes.

assistant_journal is derived owner metadata and co-commits with its receipt, canonical/outbox/index effects. The operation set above is closed to the actual Core command union. Same command and complete semantic hash returns the original receipt without another effect or journal row; changed hash refuses. Receipt linkage/hash inconsistency is corruption. Receipt remains the sole immutable replay-result body; no duplicate replay or pending authority is introduced. profile_generation is canonical positive uint64 decimal TEXT, fully checked in the owner rather than truncated to SQLite signed64. history.queue commits an actual generated Cloud create request in existing outbox without inventing an acknowledged conversation/branch. Failed/cancelled/interrupted terminal facts may lack an actual terminal MessageView; successful completion requires one.

assistant_message_fts and SQLite-generated shadows/sqlite_sequence are derived provider support, not another canonical schema. Index only generated committed MessageView text in current nondeleted local or acknowledged Cloud normal history. Never drafts, prefixes, pending proposals/configuration, temporary sessions or resource bytes. Trash/index changes co-commit; rebuild resolves committed canonical rows only. Search always joins current canonical conversation/message/branch identity and deletion state rather than trusting FTS alone. Metadata/journal/index schema and migration hashes remain explicitly sealed with the original model05 tables.


### Genuine execution lineage and durable recovery

HistoryTurn exposes optional actual owner kind/ID, immutable Configuration snapshots, IsSealed, Position and OutputOffset. owner_kind/owner_id remain jointly null until real ChatTurnView.TurnId, RunView.Owner or ExecutionProgress.Execution supplies the registered chatTurn/task owner; do not infer from submission CommandId. An indexed unique owner pair supports bounded root control lookup and every read/update compares complete generated facts. configuration_proto is the closed version1 frame of actual generated AgentProfile and SkillRecord snapshots selected at Submit, immutable thereafter, at most1000 skills/4MiB total with exact Profile.SkillIds set agreement; null only when genuinely no agent configuration was selected. Retain exact snapshots after outbox deletion, never refill from current/latest catalog heads.

Only CompleteHistoryTurn sets terminal_committed/IsSealed. Prefix/fact changes refuse sealed turns. Failed/cancelled/no-answer outcomes can seal without inventing message/hash; an interrupted factual snapshot remains resumable only under genuine current owner facts. Stream completion does not prove owner success. output_position_proto is actual generated Events.StreamPosition; output_offset is canonical uint64 decimal TEXT (0 allowed), checked losslessly by the owner. They are jointly absent until real received facts, with cursor at most4096 UTF8 bytes and exact attempt/stream/generation/sequence/global offset. Never derive offsets from displayed answer text: toolStatus/usage share the stream. Partial UTF8 input does not advance the durable page cursor; resume/replay the prior complete checkpoint after interruption.

assistant_message tool_call_id/tool_result_for are optional genuine UUID metadata from actual TranscriptMessage or the owned invocation relationship. ToolProposal.ProposalId and ToolResult.InvocationId are distinct and cannot imply pairing. Tool-containing rows without genuine complete association refuse compaction/window construction; plaintext has no fabricated IDs. CON32 appends archive HistoryMessage optional Id tags4/5, preserves original tags1/2/3 and plaintext compatibility, and requires the actual published consumer before full tool archive roundtrip.

Existing outbox remains the sole pending authority. Its closed named request union includes actual TaskServiceCancelRequest/Response and RootKind task, with genuine TaskId owner binding, plus existing Chat/Agent/Execution/catalog controls. history.queue queues each closed named request without fake acknowledged canonical rows. AcknowledgeHistoryPending (outbox.acknowledge) binds the exact pending CommandId and expected request hash to a genuine closed generated response. In one owner transaction apply only actual returned project/profile/skill facts, record journal/receipt, and remove only that matching dispatch. Control acknowledgment never manufactures conversation/model success. Conversation acknowledgment and terminal completion stay separately typed.

Each branch owns contiguous ordinals from0. Resolved history concatenates the oldest frozen selected ancestor prefix and child-owned rows, preserving original ordinals that may overlap across lineage. Cursor binds resolved position plus actual messageId, not a supposed global ordinal. ThroughOrdinal covers the selected branch's own prefix together with unchanged frozen inheritance. No global renumber or sort can rewrite authored history.

## 4. Required queries and atomic operations

| Operation | Fixed behavior / SQL shape |
|---|---|
| List | `WHERE deleted_us IS NULL` and keyset `(updated_us < :t OR (updated_us=:t AND id>:id)) ORDER BY updated_us DESC,id LIMIT :limit`; first page omits cursor, default 50/max 100; scope/query-bound cursor. |
| Read branch | resolve parent chain only to the frozen fork message; concatenate oldest selected ancestor frozen prefix then each child branch's own messages, preserving owner-local ordinals; refuse corrupt/cyclic lineage with evidence preserved. |
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

The shared lifecycle profile handoff is two-phase: authorize/open/recover the candidate, fence new views/work, flush or refuse old dirty/local work, cancel/close/drain old views, then atomically activate the new immutable history/draft generation and retire the old commit permission under synchronized gates; drain/dispose old physical storage afterward. Captured old view/service/draft ports remain bound to their old partition and refuse revoked generation before commit, including abandoned timeout saves; they never redirect to the new store. Failure before promotion preserves old authority and unsaved durable state. Initial immutable HostServices identity remains unchanged.

Schema migration backs up/verifies the existing database, applies numbered transactional steps, checks integrity and publishes the new schema marker only after success. A version unable to read/write the resulting schema refuses downgrade and uses the updater interlock. Tests cover power loss at every local commit/promotion stage, disk full, missing objects, two windows, account switch, same product on two devices and different products on one device. SQLite tests are E2 mechanism evidence; packaged AOT/Room/Cloud consumers supply E3/E4 acceptance.

## 7. Cloud metadata and transient execution closure

Chat turns and Tasks carry `product_id`, `history_mode`, `origin_installation_id?`, `transient_input_ref?` and `transient_output_receipt_id?`. Cloud mode retains existing conversation/message FKs and canonical output rules. Local/temporary mode requires the origin installation, null Cloud conversation/input/final-message FKs, and a transient input reference. The run/owner discriminator remains the existing ChatTurn or Task; no invented Task is needed for ordinary chat. Scope is immutable after admission. A new local agent execution uses the same Task state machine/approval/metering with local history mode.

`execution_transient_receipt(id PK, owner_kind, owner_id, run_id, attempt_id, product_id, origin_installation_id, output_hash, output_size, output_ref, key_ref, state, committed_at, expires_at, acknowledged_at?, purged_at?)` is metadata only; unique(owner_kind,owner_id,run_id,attempt_id) prevents duplicate output settlement. The actual input/output/iteration content and content-bearing tool arguments/results live in encrypted transient R2 objects. Rows/checkpoints/logs contain IDs, hashes, typed effect states and generic labels, never copied prompt text, titles derived from it or plaintext arguments. Existing Task/Chat storage adapters hydrate the admitted typed payload from those references after current authorization. Explicit user-authorized professional tool effects and deliberately saved resources remain in their professional owner's store under that owner's retention; local chat deletion does not undo them.

For a terminal local/temporary outcome, first verify the immutable encrypted object and content-origin/hash record; then a guarded D1 batch writes the output receipt, owner outcome, provider/usage receipt and settlement transition together. It creates no Cloud Chat message or history Sync change. Client acknowledgement is sent only after its own SQLite terminal commit and may shorten retention; it is not a condition for correct charging. Missing/expired/purged bytes never reverse established usage, invent a no-answer outcome or silently rerun a paid request. The UI distinguishes an execution outcome from body availability. A lost DO key can make transient content unavailable even when outcome/financial receipts survive; this is an explicit recovery limit, not durable-history success.

Application presence has durable identity/trust/install records in D1. Frequent heartbeat timestamps/capability availability live in a scope-bound DO, expire after 30s and cannot authorize a tool by themselves. New registration obtains an epoch through guarded durable owner state; DO loss is rebuilt as offline until a current verified heartbeat. A stale instance cannot resurrect its predecessor's lease.

History imports expire24h after Begin unless already committed. Finalize transitions staging→verifying→ready→committed; verification failure→failed, precommit Cancel→canceled, timeout→expired. Transition and epoch checks prevent a canceled/expired verifier from activating a manifest. All Chat list/get/search/sync readers filter the committed visibility pointer. Records staged in earlier batches cannot leak through an alternate read path.

## Shared compaction integrity framing

This closes an undefined ordinary production consistency predicate in model05/annex10, without adding a wire message. Current Cloud source has only compaction physical schema, no implemented source-hash producer; preserve that fact and require its later producer to use these same vectors.

SourceHash is the existing published CanonicalSemanticHash (SHA256 over canonical semantic JSON) of:
{"schemaVersion":"arcforges.assistant.compaction-source.v1","messages":[...]}
Messages are the full frozen resolved prefix in resolved ancestry concatenation order, preserving every original owner-local uint64 ordinal (which can overlap between ancestor and child); no synthetic message IDs, branch IDs, changed role, partial tool-call/result pair, omitted protected content, or reordered parts. Each actual TranscriptMessage projection uses the exact known field names:
message_id (lowercase dashed network-order UUID), ordinal (canonical unsigned decimal string), role (canonical enum integer decimal string), parts (ordered known MessagePart projection), optional tool_call_id, optional tool_result_for.
MessagePart and nested bodies/origins/resources use the same explicit Contracts324 known-field projection as the current owner Core (AssistantPayloadProjection); all actual optional known presence and native uint64 arms are retained, unknown protobuf fields are inert and excluded from semantic identity.
A message ID is unique in the prefix. Actual generated shape validation runs before projection. ToolProposal and ToolResult parts require genuine separately supplied ToolCallId/ToolResultFor metadata; distinct proposal/invocation IDs cannot be equated. Unknown role or invalid tool-pair/ordinal structure refuses before a summary is used.
The prefix hash contains no branch identity or branch revision: those remain separate exact CompactionRecord bindings. An unaffected identical prefix may remain verifiable after a fork; changed message identity/content/ordinal invalidates it. ThroughOrdinal binds the selected branch own covered prefix; inherited frozen prefix remains unchanged and the actual branch-resolution transaction verifies the complete requested prefix, not a window missing earlier messages.
Input is bounded to 2000 TranscriptMessage records, 16000 aggregate parts and 4MiB total canonical JSON. The published canonical semantic helper retains its own canonicalization bounds; refuse rather than silently truncate.
SummaryHash is lower-case SHA256 of the exact strict UTF-8 bytes of CompactionRecord.Summary, without Unicode/newline/whitespace normalization. Refuse invalid UTF-16 surrogate input. Summary is bounded by actual generated contract shape plus <=262144 bytes UTF8. Source and summary hashes are distinct from mutable local prefix payload integrity and remote stream chunk/final hashes.
The shared Core exposes AssistantCompactionIntegrity.ComputeSource(IReadOnlyList<TranscriptMessage>) and ComputeSummary(string). SQL resolves and verifies actual branch prefix/tool pairs in the committing transaction, compares both hashes and exact branch/through bindings, and does not accept an arbitrary well-shaped caller hash.
Ordinary deterministic cross-language vectors cover UTF8/non-ASCII, known presence, field/order changes, unknown protobuf fields retained/inert, original ordinal>2^53, native uint64 maximum, edited/forked prefix, wrong summary hash, incomplete tool pair and protected overflow. These do not prove real Cloud/provider deployment or inferred model/tokenizer behavior.


### Atomic profile activation fence

After candidate recovery and prepared old-view/work drain, activate current session/history and lifecycle DraftStore together under their synchronized gates. Retire old commit permission at that same linearization point; drain/dispose the old physical store afterward. Do not irreversibly Dispose the old authority before a candidate commit that can still fail. Failed/cancelled activation leaves the old current authority unrevoked and preserves unsaved/durable data. Old captured ports keep their old immutable partition/generation and never redirect to the new store. A scoped handoff Commit callback/gate seam may synchronize real activation with lifecycle Dispose; it cannot waive ownership or generation checks. This precise activation ordering governs the earlier retire/lock/drain shorthand.


## Captured lifetime and received Task facts (2026-10-07)

The real AST01 RAM kernel and SQL store are distinct actual owners. Complete factory/UI composition uses immutable AssistantConversationScope: actual conversation, captured History/Turns/Drafts, Retirement and explicit StorageLifetime. Profile History/Turns/Drafts retain their durable SQL generation; captured ports never redirect after handoff. Session.OpenScopeAsync authorizes current profile and opens the genuine local/acknowledged root; temporary roots/branches exist only in bounded RAM. Session.OpenView(scope,window,recoveredDraft) validates exact owner, partition and current generation before reusable lifecycle admission.

Add explicit backward-compatible AssistantDraftStorageLifetime Durable/Ephemeral to actual store, draft, view and checkpoint evidence; existing default Durable remains. Durable Save still means actual durable CAS/crash recovery. Ephemeral Save means exact bounded live RAM CAS, never durable recovery or a saved-to-disk label. Constructors, successors and recovery preserve lifetime; unknown/mismatched lifetime refuses. Lifecycle.OpenEphemeralView captures the genuine RAM store and conversation retirement, without replacing the profile DraftStore. Exclude ephemeral bodies from durable unclaimed/prepared-old/failed-handoff recovery queues, SQLite, FTS and backup. Failed synchronized promotion keeps old RAM scope live/unrevoked without private SQL copying; successful promotion retires old commit permission at the same session/lifecycle activation point, then drains physical/callback work outside gates.

Add sealed AssistantDraftConsumption with internal constructor accessible only through exact friend ArcForges.Assistant.Core. Trusted Core mints it only after actual Submit committed receipt matches queue command and exact consumed-draft intent, capturing real store reference, owner/partition/generation retirement, consumed DraftId/revision/exact text and queue receipt identity. AssistantView.AcknowledgeSubmissionAsync holds savegate and viewgate, verifies exact captured store/generation/ID/revision, rotates fresh DraftId/revision0. Clear editor only if current text still equals submitted exact text; preserve newly typed full text dirty under fresh identity and actual autosave. Wrong, retired or stale token refuses without changing text. Never call Discard/SQL delete on an already consumed row, expose public minting/caller success Boolean, or claim Queued is remote Accepted. Keep source receipt capability immutable and secret-free diagnostic output; private draft content is never logged.

Task-only ChatServiceAppendMessageValue.Task is genuine TaskSnapshot authority. UpdateHistoryTurnFacts may accept that typed source-bound fact, atomically commit it to existing assistant_task_projection and derive real task owner/scalars, cross-checking actual Run/Progress where present. Revision must be monotone; same revision requires exact factual bytes. HistoryTurn retains owner reference; GetTaskAsync returns explicitly current projection, not a frozen per-turn historical Task payload. No task_proto column, fake Progress, guessed Run/attempt/stream or submission UUID as server owner/revision.

Local stale fencing is Submit.ExpectedLocalRevision. A new transient request has no remote Chat row, so Pending.BaseRevision0 and RequestMeta.ExpectedRev absent; do not send local conversation revision as remote authority. Actual received turn/task owner revisions remain mandatory for controls. Complete source selection/hashes, output reset/snapshot and pinned execution configuration require their separate actual Contracts/server producer repair; this lifetime amendment grants none of those missing facts or remote activation.

Core/Sqlite/backend source paths, evaluated immutable admission, public API/test mapping and exact publication remain governed by existing AST01 scopes. Ordinary real RAM/SQL/lifecycle/consumption/race components are mandatory. AST10 consumes the shared factory/services/views, never a product-private duplicate.


## 2026-10-07 complete output and bounded recovery producer

The [reviewed assistant output and recovery decision](../../decisions/assistant-output-snapshots-and-semantic-profiles-2026-10-07.md) governs compatible output snapshots, exact configuration pins, closed shared semantic-v1 hashes and explicit initial capacity-overflow recovery with candidate handoff refusal. Actual generated publication and real logical-body/tokenizer/current-target producers remain mandatory; no incomplete recovery or stream state is reported as successful canonical content. Existing durable/ephemeral, transaction, authorization, retention and original task obligations are retained.


## 2026-10-07 actual execution output implementation

The [reviewed execution output producer decision](../../decisions/execution-output-and-logical-body-producer-2026-10-07.md) binds the actual Task/Chat/Resource/RunStream implementations, Chat-owned physical transient receipt mapping, logical decoded-body facade and exact guarded terminal/ack/purge authority. Existing history/stream/retention/accounting/permission limits and real producer acceptance remain required; source composition or projections never invent canonical completion.
