<a id="rule-wp-25"></a>

# WP-25 — Sync Engine and Blob Lifecycle

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `19`, `24` · Downstream: `26`, `28`, `35`, `39`, `40`, `43`, `46`, `51`

> **Goal.** Prove sync on ArcNotes: a client outbox, a server inbox, a change feed, five conflict policies, deletion propagation, and a blob lifecycle that never leaves a reference pointing at nothing — with multi-device convergence demonstrated, not assumed.

---

## 1. Scope and purpose

**In scope.** The sync engine end to end for ArcNotes: sync scopes, the client outbox, the server inbox, the change feed, conflict detection and resolution policies, deletion and tombstones, the blob lifecycle from staged to committed, availability states, protection profiles, data health, and multi-device convergence.

**Out of scope.** ArcScope and ArcSlate sync strategies (`35`, `39`) — this package establishes the engine those extend. Backup and disaster recovery (`46`).

**Why this package exists.** [SQ-05](../implementation-sequence.md#rule-sq-05): ArcNotes is the right product to prove the initial sync protocol — more complex than a toy, simpler than raw captures or large media, yet sufficient to validate revisions, attachments, deletions, conflicts, history and recovery.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/07-sync-conflict-and-backup.md`](../../architecture/07-sync-conflict-and-backup.md) | Identity and revision, outbox/inbox, change feed, conflict policies, blob lifecycle, protection profiles, data health |
| [`../../requirements/03-cloud-services-and-sync.md`](../../requirements/03-cloud-services-and-sync.md) | Sync scopes, per-product defaults, change propagation, tombstones, storage accounting |
| [WP-19](19-arcnotes-search-and-portability.md#rule-wp-19), [WP-24](24-realtime-and-reliable-events.md#rule-wp-24) output | A format proven to round-trip locally, and gap-detecting change notification |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Sync is per scope, not all-or-nothing**, with explicit per-product defaults. |
| BR-02 | **The client outbox is durable** and survives process termination; every entry carries a command identity. |
| BR-03 | **The server inbox deduplicates** so a replayed entry has no additional effect. |
| BR-04 | **A conflict is detected by revision**, never by timestamp comparison alone. |
| BR-05 | **A conflict is never silently resolved by discarding a side.** Where a policy chooses, the discarded version remains recoverable. |
| BR-06 | **Deletion propagates through tombstones** with a defined retention, so a deletion is not undone by a device that was offline. |
| BR-07 | **A blob is Staged, then Verified, then Committed.** A reference is never published before its blob is committed. |
| BR-08 | **`Cloud Sync ≠ Raw Capture Upload`** ([I-474](../../requirements/01-normative-glossary-and-invariants.md#rule-i-474)) — the scope model must make product-specific exclusions expressible from the start. |
| BR-09 | **Availability is an explicit state**: available locally, available remotely, syncing, unavailable — never an error at read time. |
| BR-10 | **Storage accounting is computed from committed objects**, never from client-reported figures. |
| BR-11 | **Loss of subscription never deletes user data**; it changes access, with an explicit stated behaviour. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.Sync/` | Server inbox, change feed, conflict evaluation, tombstones, scope registry |
| `src/Cloud/ArcForges.Cloud.Modules.Resource/` | Blob lifecycle, upload tickets, verification, commit, garbage collection, accounting |
| `src/BuildingBlocks/ArcForges.Sync/` | Client outbox, change application, conflict presentation, availability states |
| `src/ArcNotes/ArcNotes.CloudClient/` | ArcNotes sync adapter: scope mapping, attachment handling, conflict surfacing |
| `tests/SyncConflictTests/` | Convergence, conflict, deletion, blob and multi-device suites |

**Major types introduced.** `SyncScope`, `OutboxEntry`, `InboxRecord`, `ChangeFeedCursor`, `ChangeRecord`, `ConflictPolicy`, `ConflictResolution`, `Tombstone`, `BlobState`, `UploadSession`, `AvailabilityState`, `ProtectionProfile`, `DataHealthReport`.

---

## 5. Required implementation work

<a id="rule-wp-25.00"></a>

### WP-25.00 — Cloud Notes authority and sync scopes

**What must be fully done.** Implement the canonical notes schema in [Cloud data model §8.4](../../architecture/data-model/01-cloud-data-model.md#84-cloud-notes-canonical-model): notebook-owned folders, document-owned blocks and values, tags, property definitions, saved views, immutable revisions, checkpoints and derived backlinks. Add the typed folder/document/history operations and their sorted-root revision checks. Cloud validates the same typed operations as the local domain; publication, receipts and Resource/Entitlement enlistment share the commit.

**Testing requirements.** Folder cycle/reorder/reparent, cross-notebook move with stable document IDs, concurrent move/delete, ancestor trash/restore without restoring separately trashed documents, stale revisions, immutable history and revision/attachment pins. Verify generated API/SQLite projections against real PostgreSQL.

**Completion gate.** A note has one complete server authority model and hierarchy, with executable operations, history and resource ownership; no client is required to create authoritative schema or assign Cloud revisions.

<a id="rule-wp-25.01"></a>

### WP-25.01 — Pending batches and conflict lineage

**What must be fully done.** Implement the single sync_outbox schema, acked shadow plus pending journal, frozen batch hash/revision/range, and explicit supersession lineage in the desktop data model. A user conflict resolution appends a new local event and records retained/transformed/discarded dispositions; it never edits the frozen failed batch. Replacement covers the unacknowledged range, while historical superseded ranges remain auditable.

**Testing requirements.** Edit during dispatch, conflict followed by keep-local/keep-Cloud/merge, dependent undispatched batches, crash at each resolution write, late old receipt and own-origin feed echo. Verify local composite version advances, original pending work remains recoverable and no old receipt acknowledges a replacement.

**Completion gate.** Every local edit has a durable outcome and exactly one live submission lineage. Query/index tokens describe the materialised state and no conflict silently drops pending content.

<a id="rule-wp-25.02"></a>

### WP-25.02 — Published feed, bootstrap and revision application

**What must be fully done.** Implement the committed publication sequence and bounded bootstrap manifest/pin protocol. Capture W then a primary repeatable-read snapshot at or after W, retain bounded immutable pages, and resume the feed after W. Every client applies only a newer aggregate revision including tombstones; duplicates/older rows never replace a newer bootstrap value. Advance a page cursor only after durable processing; resolve cross-aggregate references by canonical minRevision lookup.

**Testing requirements.** Bootstrap sees v2 while feed still includes v1; own-origin echo; two same-millisecond UUID revisions in reverse order; late commit above advanced cursor; page retry/cursor expiry; tombstone retention floor and missing structural dependency. Preserve pending edits through full resync.

**Completion gate.** Bootstrap plus feed loses no committed change and never regresses an aggregate, even with duplicates, delayed publication, structural references and pending local work. [PG-17](../../assurance/open-gates-register.md#rule-pg-17) stays a real multi-writer test gate.

<a id="rule-wp-25.03"></a>

### WP-25.03 — Conflict detection and policies

**What must be fully done.** Conflicts detected by revision. Five policies implemented per the architecture, chosen per scope and per object kind. Where a policy discards, the discarded version is retained and recoverable. Conflicts requiring the user are surfaced with both versions intelligible.

**Testing requirements.** A conflict matrix across object kinds and policies; a recoverability test for every discard; a user-facing presentation test.

**Completion gate.** Every conflict path is covered, every discarded version is recoverable, and user-facing conflicts present both versions.

<a id="rule-wp-25.04"></a>

### WP-25.04 — Deletion and tombstones

**What must be fully done.** Deletion propagates through tombstones with defined retention. A device offline beyond retention resolves deterministically rather than resurrecting deleted content silently. Local deletion, cloud deletion and unsync are distinguished.

**Testing requirements.** Offline-beyond-retention convergence; a resurrection-prevention test; a distinction test across the three delete-like actions.

**Completion gate.** Deleted content never silently resurrects, and the three delete-like actions are distinguishable.

<a id="rule-wp-25.05"></a>

### WP-25.05 — Blob lifecycle

**What must be fully done.** Upload through a server-issued session, chunked and checksummed, moving Staged → Verified → Committed. A reference is only published after commit. Orphan cleanup removes uncommitted staging without touching committed data. Storage accounting is computed from committed objects.

**Testing requirements.** Interrupted upload resumption; a verification-failure path; an orphan-cleanup safety test; an accounting comparison against actual committed storage.

**Completion gate.** No reference is published before commit, orphan cleanup never touches committed data, and accounting matches committed storage.

<a id="rule-wp-25.06"></a>

### WP-25.06 — Availability, protection and data health

**What must be fully done.** Availability states surfaced per object. Protection profiles applied per scope. A data health report detects and reports divergence, missing blobs, orphan references and stale cursors, with a repair path for each.

**Testing requirements.** Induced divergence, induced missing blob and induced orphan reference, each detected and repaired; an availability-state test per object state.

**Completion gate.** Every induced integrity fault is detected and repaired, and availability is an explicit state rather than a read-time error.

<a id="rule-wp-25.07"></a>

### WP-25.07 — Multi-device convergence

**What must be fully done.** Three devices editing concurrently, one offline for an extended period, converge to identical state with all conflicts either resolved by policy or surfaced. Convergence is verified by comparison, not by absence of errors.

**Testing requirements.** A three-device convergence harness with concurrent edits, an extended offline device, attachments, deletions and a mid-sync crash.

**Completion gate.** **Three devices converge to verifiably identical state** under concurrent editing, extended offline periods, attachments, deletions and a crash.

---

<a id="rule-wp-25.08"></a>

### WP-25.08 — Real Cloud Notes and Chat export producers

**What must be fully done.** Build bounded leased Cloud export jobs for Notes and Chat. Freeze an acknowledged revision manifest, pin its content/history/attachment objects, and generate the declared Markdown/JSON/text outputs, attachments, metadata/link map and fidelity report. Publish a verified, expiring download artifact; exclude device-only pending edits. Enforce resource/egress reservations and allow retained-data export during configured read/grace periods. Delete the early [WP-15.06](15-arcchat-conversation-core.md#rule-wp-15.06) and [WP-19.05](19-arcnotes-search-and-portability.md#rule-wp-19.05) export fixtures from runtime registration.

**Testing requirements.** Real host/database/object-store export across concurrent edits, notebook moves, deleted attachments, quota limit, expiry, restart, cancellation and paid-term end. Compare every delivered manifest/hash and omission; scan for secrets. Run both production clients with no fixture producer registered.

**Completion gate.** Both export exit paths work against real Cloud authority, preserve a stable snapshot and honest fidelity, and release pins/reservations on all terminal paths. This is the Cloud Notes/Chat portion of PG-07.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Sync state, tombstones, change feed and blob metadata |
| Protocol | Sync, change feed and blob contracts |
| UI | Sync state, conflict resolution, availability and storage surfaces |
| Security | Permission re-checked on every sync operation; protection profiles |
| Platform | Offline behaviour per platform |
| Migration | Cross-device schema versioning: an older device must not corrupt newer data |
| Compatibility | The sync contract enters the supported window with strict rules |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Scope change and exclusion results | [WP-25.00](#rule-wp-25.00) |
| Batch-log survival, in-flight-edit, duplicate-acknowledgement and conflict-rebase results | [WP-25.01](#rule-wp-25.01) |
| Deduplication, feed stability and expired-cursor results | [WP-25.02](#rule-wp-25.02) |
| Conflict matrix and recoverability results | [WP-25.03](#rule-wp-25.03) |
| Tombstone convergence and resurrection-prevention results | [WP-25.04](#rule-wp-25.04) |
| Blob lifecycle, orphan cleanup and accounting results | [WP-25.05](#rule-wp-25.05) |
| Integrity fault detection and repair results | [WP-25.06](#rule-wp-25.06) |
| Three-device convergence comparison | [WP-25.07](#rule-wp-25.07) |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Scopes are per-product, changeable without redundant transfer, and can express a content exclusion.
2. Pending changes survive termination, retry in order, and accumulate with bounded visible growth.
3. Duplicate submissions have no additional effect; the change feed is stable and resumable; an expired cursor produces an explicit instruction.
4. Every conflict path is covered; every discarded version is recoverable; user-facing conflicts present both versions intelligibly.
5. Deleted content never silently resurrects; local delete, cloud delete and unsync are distinguishable.
6. No blob reference is published before commit; orphan cleanup never touches committed data; accounting matches committed storage.
7. Every induced integrity fault is detected and repaired; availability is an explicit state.
8. **Three devices converge to verifiably identical state** under concurrent editing, an extended offline period, attachments, deletions and a mid-sync crash.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [19 — ArcNotes Search, Import, Export and Portability](19-arcnotes-search-and-portability.md)
- [24 — Realtime, Reliable Events and Recovery](24-realtime-and-reliable-events.md)

**Downstream — these consume this package’s completed output.**

- [26 — Device Presence, Remote Action and the Tool Bridge](26-remote-action-and-tool-bridge.md)
- [28 — ArcNotes Bounded Properties and Saved Views](28-arcnotes-properties-and-views.md)
- [35 — ArcScope Integration and Metadata Sync](35-arcscope-integration-and-sync.md)
- [39 — ArcSlate Integration and Portability](39-arcslate-integration-and-portability.md)
- [40 — Knowledge, Search and Retrieval](40-knowledge-search-and-retrieval.md)
- [43 — Cloud AI Routing, Metering and Settlement](43-managed-ai-routing-and-metering.md)
- [46 — Backup, Disaster Recovery and Data Health](46-backup-recovery-and-data-health.md)
- [51 — ArcScope Deterministic Cloud Simulator](51-arcscope-cloud-simulator.md)
