<a id="rule-wp-25"></a>

# WP-25 — Sync Engine and Blob Lifecycle

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `19`, `24` · Downstream: `26`, `28`, `35`, `39`, `40`, `43`, `46`, `48`, `51`

> **Goal.** Prove sync on ArcNotes: a client outbox, a server inbox, a change feed, five conflict policies, deletion propagation, and a blob lifecycle that never leaves a reference pointing at nothing — with multi-device convergence demonstrated, not assumed.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud; desktop/Mobile consumers. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The sync engine end to end for ArcNotes: sync scopes, the client outbox, the server inbox, the change feed, conflict detection and resolution policies, deletion and tombstones, the blob lifecycle from staged to committed, availability states, protection profiles, data health, and multi-device convergence.

**Out of scope.** ArcScope and ArcSlate sync strategies (`35`, `39`) — this package establishes the engine those extend. Backup and disaster recovery (`46`).

**Why this package exists.** [SQ-05](../implementation-sequence.md#rule-sq-05): ArcNotes is the right product to prove the initial sync protocol — more complex than a toy, simpler than raw captures or large media, yet sufficient to validate revisions, attachments, deletions, conflicts, history and recovery.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile)

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

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

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

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

**Required design implementation and verification.** Canonical Notes write validators and sync projection preserve number/date values, semantic revisions and query profile/view bindings. Advance the acknowledged query dataset token in the same relevant source commit. Exercise a label rename, rejected dependent type change and stale-view restoration across local/Cloud revisions.

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

**Required design implementation and verification.** Implement real acknowledged-snapshot Notes/Chat exports with origin/fidelity/attachment inventory, bounded pin/retention and verified download. Stage output plus sidecars and publish one atomic bundle. Exercise failure/cancel and structurally remove runtime fixture registrations from [WP-15.06](15-arcchat-conversation-core.md#rule-wp-15.06) and [WP-19.05](19-arcnotes-search-and-portability.md#rule-wp-19.05); retained test fixtures are not runtime producers.

**What must be fully done.** Build bounded leased Cloud export jobs for Notes and Chat. Freeze an acknowledged revision manifest, pin its content/history/attachment objects, and generate the declared Markdown/JSON/text outputs, attachments, metadata/link map and fidelity report. Publish a verified, expiring download artifact; exclude device-only pending edits. Enforce resource/egress reservations and allow retained-data export during configured read/grace periods. Delete the early [WP-15.06](15-arcchat-conversation-core.md#rule-wp-15.06) and [WP-19.05](19-arcnotes-search-and-portability.md#rule-wp-19.05) export fixtures from runtime registration.

**Testing requirements.** Real host/database/object-store export across concurrent edits, notebook moves, deleted attachments, quota limit, expiry, restart, cancellation and paid-term end. Compare every delivered manifest/hash and omission; scan for secrets. Run both production clients with no fixture producer registered.

**Completion gate.** Both export exit paths work against real Cloud authority, preserve a stable snapshot and honest fidelity, and release pins/reservations on all terminal paths. This is the Cloud Notes/Chat portion of PG-07.

---

**Required implementation and closure from the final review.** Implement and independently verify [01-cloud-data-model](../../architecture/data-model/01-cloud-data-model.md). Implement real structural move/ack/conflict transactions, full native metadata replicas, job-authorized R2 staging/verification/promotion and quarantined old-generation client commands. WP25.08 closes both Notes and Chat Cloud export manifests through actual R2; test missing permission, partial transfer, loss reports, no pending-local content and response loss. Old Notebook/Document body uploads cannot bypass placement operations. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-25.90"></a>
### WP-25.90 — Verify the owned artifact and real integration

**What must be fully done.** Use R2 for the existing upload admission, multipart resume, Verified pin, owner promotion, quota and release lifecycle. Retain outbox/inbox/tombstones/conflicts/bootstrap/unknown-field behavior and export protocol.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Three-device convergence and interrupted-upload/failed-content-commit/orphan/delete cases run against actual provider adapters; [WP-25.08](#rule-wp-25.08) remains represented in its evidence and completion gate.

**Completion gate.** Three-device convergence and interrupted-upload/failed-content-commit/orphan/delete cases run against actual provider adapters; [WP-25.08](#rule-wp-25.08) remains represented in its evidence and completion gate. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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

**[WP-25.08](#rule-wp-25.08) producer evidence.** Real snapshot/export jobs, input revisions, attachment/origin/fidelity manifest, bounded retention/download, cancel/failure cases, and structural absence of the Notes/Chat runtime export fixture registrations.

**Required evidence addition.** Canonical scalar/schema and pending/acknowledged query-token sync results.

**Required evidence addition.** [WP-25.08](#rule-wp-25.08) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

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

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-25.90](#rule-wp-25.90) and all inherited domain-specific gates must pass on the same candidate closure. Three-device convergence and interrupted-upload/failed-content-commit/orphan/delete cases run against actual provider adapters; [WP-25.08](#rule-wp-25.08) remains represented in its evidence and completion gate.

**Producer completion.** [WP-25.08](#rule-wp-25.08) must pass with the explicit §7 artifacts above; it is not optional because other package checks pass. Its real Cloud Notes/Chat export format, origin-carrier and fidelity fixtures provide this package's [PG-07](../../assurance/open-gates-register.md#rule-pg-07) contribution; import/interchange producers retain their separately scheduled obligations.

**[PG-17](../../assurance/open-gates-register.md#rule-pg-17) evidence:** [WP-25.07](#rule-wp-25.07) — Bootstrap/feed convergence, old revisions/tombstones/echoes, and late commit after an advanced cursor, consuming the publisher from package 21. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**Offline evidence.** Execute this product's applicable [initial-state matrix](../../assurance/testing-and-verification-strategy.md#offline-acceptance-matrix) rows, including fresh shell, hydrated outage, unavailable content, signout and restart where applicable. Record permitted local work and explicitly unavailable Cloud actions.

**Additional completion requirement.** Notes sync preserves the declared semantics and origin through conflicts, restore and export; no mixed source revisions are presented as one successful query dataset.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

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

- [WP-19](19-arcnotes-search-and-portability.md#rule-wp-19)
- [WP-24](24-realtime-and-reliable-events.md#rule-wp-24)

**Downstream — consumers of these released outputs.**

- [WP-26](26-remote-action-and-tool-bridge.md#rule-wp-26)
- [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28)
- [WP-35](35-arcscope-integration-and-sync.md#rule-wp-35)
- [WP-39](39-arcslate-integration-and-portability.md#rule-wp-39)
- [WP-40](40-knowledge-search-and-retrieval.md#rule-wp-40)
- [WP-43](43-managed-ai-routing-and-metering.md#rule-wp-43)
- [WP-46](46-backup-recovery-and-data-health.md#rule-wp-46)
- [WP-48](48-account-portal.md#rule-wp-48)
- [WP-51](51-arcscope-cloud-simulator.md#rule-wp-51)


---
