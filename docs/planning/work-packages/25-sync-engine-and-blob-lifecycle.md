# WP-25 — Sync Engine and Blob Lifecycle

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `19`, `24` · Downstream: `26`, `27`, `35`, `39`, `40`, `46`

> **Goal.** Prove sync on ArcNotes: a client outbox, a server inbox, a change feed, five conflict policies, deletion propagation, and a blob lifecycle that never leaves a reference pointing at nothing — with multi-device convergence demonstrated, not assumed.

---

## 1. Scope and purpose

**In scope.** The sync engine end to end for ArcNotes: sync scopes, the client outbox, the server inbox, the change feed, conflict detection and resolution policies, deletion and tombstones, the blob lifecycle from staged to committed, availability states, protection profiles, data health, and multi-device convergence.

**Out of scope.** ArcScope and ArcSlate sync strategies (`35`, `39`) — this package establishes the engine those extend. Backup and disaster recovery (`46`).

**Why this package exists.** `SQ-05`: ArcNotes is the right product to prove the initial sync protocol — more complex than a toy, simpler than raw captures or large media, yet sufficient to validate revisions, attachments, deletions, conflicts, history and recovery (`I2 §III.6`).

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/07-sync-conflict-and-backup.md`](../../architecture/07-sync-conflict-and-backup.md) | Identity and revision, outbox/inbox, change feed, conflict policies, blob lifecycle, protection profiles, data health |
| [`../../requirements/03-cloud-services-and-sync.md`](../../requirements/03-cloud-services-and-sync.md) | Sync scopes, per-product defaults, change propagation, tombstones, storage accounting |
| `WP-19`, `WP-24` output | A format proven to round-trip locally, and gap-detecting change notification |

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
| BR-08 | **`Cloud Sync ≠ Raw Capture Upload`** (`I-474`) — the scope model must make product-specific exclusions expressible from the start. |
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

### WP-25.00 — Sync scopes

**What must be fully done.** Scopes declared per product with defaults, so a product can sync metadata while excluding heavyweight content. Scope changes take effect without re-uploading unchanged content. The exclusion mechanism is expressive enough for `BR-08` before ArcScope needs it.

**Testing requirements.** Scope enable, disable and re-enable without redundant transfer; an exclusion expressiveness test using a simulated large-content scope.

**Completion gate.** Scopes are per-product, changeable without redundant transfer, and can express a content exclusion.

### WP-25.01 — Client outbox

**What must be fully done.** A durable outbox capturing local changes with command identities, surviving termination, retrying with backoff, and preserving causal order where required. Outbox depth and age are visible.

**Testing requirements.** Kill-with-pending-entries; retry ordering; a long-offline accumulation test with bounded growth and a clear state.

**Completion gate.** Pending changes survive termination, retry in correct order, and accumulate with bounded, visible growth.

### WP-25.02 — Server inbox and change feed

**What must be fully done.** The inbox deduplicates by command identity. The change feed is cursor-based, stable under concurrent writes, and resumable from any retained cursor. An expired cursor produces an explicit full-resync instruction rather than silent divergence.

**Testing requirements.** Duplicate submission; feed stability under concurrent mutation; expired-cursor behaviour.

**Completion gate.** Duplicates have no additional effect, the feed is stable and resumable, and an expired cursor produces an explicit instruction.

### WP-25.03 — Conflict detection and policies

**What must be fully done.** Conflicts detected by revision. Five policies implemented per the architecture, chosen per scope and per object kind. Where a policy discards, the discarded version is retained and recoverable. Conflicts requiring the user are surfaced with both versions intelligible.

**Testing requirements.** A conflict matrix across object kinds and policies; a recoverability test for every discard; a user-facing presentation test.

**Completion gate.** Every conflict path is covered, every discarded version is recoverable, and user-facing conflicts present both versions.

### WP-25.04 — Deletion and tombstones

**What must be fully done.** Deletion propagates through tombstones with defined retention. A device offline beyond retention resolves deterministically rather than resurrecting deleted content silently. Local deletion, cloud deletion and unsync are distinguished.

**Testing requirements.** Offline-beyond-retention convergence; a resurrection-prevention test; a distinction test across the three delete-like actions.

**Completion gate.** Deleted content never silently resurrects, and the three delete-like actions are distinguishable.

### WP-25.05 — Blob lifecycle

**What must be fully done.** Upload through a server-issued session, chunked and checksummed, moving Staged → Verified → Committed. A reference is only published after commit. Orphan cleanup removes uncommitted staging without touching committed data. Storage accounting is computed from committed objects.

**Testing requirements.** Interrupted upload resumption; a verification-failure path; an orphan-cleanup safety test; an accounting comparison against actual committed storage.

**Completion gate.** No reference is published before commit, orphan cleanup never touches committed data, and accounting matches committed storage.

### WP-25.06 — Availability, protection and data health

**What must be fully done.** Availability states surfaced per object. Protection profiles applied per scope. A data health report detects and reports divergence, missing blobs, orphan references and stale cursors, with a repair path for each.

**Testing requirements.** Induced divergence, induced missing blob and induced orphan reference, each detected and repaired; an availability-state test per object state.

**Completion gate.** Every induced integrity fault is detected and repaired, and availability is an explicit state rather than a read-time error.

### WP-25.07 — Multi-device convergence

**What must be fully done.** Three devices editing concurrently, one offline for an extended period, converge to identical state with all conflicts either resolved by policy or surfaced. Convergence is verified by comparison, not by absence of errors.

**Testing requirements.** A three-device convergence harness with concurrent edits, an extended offline device, attachments, deletions and a mid-sync crash.

**Completion gate.** **Three devices converge to verifiably identical state** under concurrent editing, extended offline periods, attachments, deletions and a crash.

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
| Scope change and exclusion results | `WP-25.00` |
| Outbox survival, ordering and growth results | `WP-25.01` |
| Deduplication, feed stability and expired-cursor results | `WP-25.02` |
| Conflict matrix and recoverability results | `WP-25.03` |
| Tombstone convergence and resurrection-prevention results | `WP-25.04` |
| Blob lifecycle, orphan cleanup and accounting results | `WP-25.05` |
| Integrity fault detection and repair results | `WP-25.06` |
| Three-device convergence comparison | `WP-25.07` |

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

**Upstream.** `19` (a locally proven format), `24` (gap-detecting change notification).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `26` — Remote action | Sync state as the basis for remote work |
| `27` — Edgeless | Sync for new content kinds on the proven engine |
| `35`, `39` | The engine ArcScope and ArcSlate extend with their own scope rules |
| `40` — Knowledge | Synced content as a knowledge source |
| `46` — Backup | Committed state as the backup subject |
