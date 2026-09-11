# Sync, Conflict and Backup Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Companions: [`../requirements/03-cloud-services-and-sync.md`](../requirements/03-cloud-services-and-sync.md), [`06-data-persistence-and-formats.md`](06-data-persistence-and-formats.md), [`05-cloud-architecture.md`](05-cloud-architecture.md)

The mechanics of replication, convergence, conflict handling, blob lifecycle and recovery.

---

## 1. Identity and revision

```
Workspace + AppId + ObjectId          the stable identity of a syncable object
ObjectRevision                        immutable, parented, actor-attributed
```

| # | Rule |
|---|---|
| ID-01 | **Identity is never a path or a filename** ([SY-10](../requirements/03-cloud-services-and-sync.md#rule-sy-10) in the cloud requirements). |
| ID-02 | **`ObjectId` is never reused** ([RR-04](02-contracts-and-protocols.md#rule-rr-04) in the contracts architecture). |
| ID-03 | **A revision records**: `RevisionId`, `ObjectId`, `ParentRevision`, created time, actor, device, app version, schema version — and for an agent write, task, capability and approval reference ([SY-20](../requirements/03-cloud-services-and-sync.md#rule-sy-20), [SY-21](../requirements/03-cloud-services-and-sync.md#rule-sy-21)). |
| ID-04 | **Historical revisions are immutable.** A change produces a new revision ([SY-22](../requirements/03-cloud-services-and-sync.md#rule-sy-22)). |
| ID-05 | **Restore is a new revision**, never a history rewrite ([HR-02](../requirements/products/arcnotes.md#rule-hr-02) in the ArcNotes requirements). |
| ID-06 | **Revision kinds are distinguishable** — autosave, user version, agent checkpoint, migration checkpoint — over one mechanism ([SY-24](../requirements/03-cloud-services-and-sync.md#rule-sy-24)). |

---

## 2. Sync scope

```
Product  →  Sync Scope  →  Objects
              ├── enabled state
              ├── protection profile (Standard)
              ├── large-asset policy
              ├── selective-sync policy
              └── conflict policy
```

| # | Rule |
|---|---|
| SS-01 | **The scope is the unit of participation**, not the application data directory ([SY-01](../requirements/03-cloud-services-and-sync.md#rule-sy-01)). |
| SS-02 | **`Sync Scope ≠ ArcChat Project`** ([SY-02](../requirements/03-cloud-services-and-sync.md#rule-sy-02)). |
| SS-03 | **Per-product defaults are conservative for large data** (`§4.1` of the cloud requirements). |
| SS-04 | **Disabling a scope asks whether to keep local files, defaulting to yes** ([SY-05](../requirements/03-cloud-services-and-sync.md#rule-sy-05)). |

---

## 3. Change propagation

**Client submission is a log of immutable batches, not a mutable queue** (`§1.3a` of the desktop data model). Each batch records the exact `local_seq` range it covers; an acknowledgement advances the watermark to that range's end **and no further**, so an edit made while a batch was in flight stays pending ([RV-C4](data-model/02-desktop-data-model.md#rule-rv-c4), [SB-L1](data-model/02-desktop-data-model.md#rule-sb-l1)). A dispatched batch is never mutated — appending to it would change what its idempotency identity means ([SB-L2](data-model/02-desktop-data-model.md#rule-sb-l2)) — and there is at most one batch in flight per aggregate ([SB-L3](data-model/02-desktop-data-model.md#rule-sb-l3)).

### 3.1 Client outbox

```
Local edit
 → local durable commit (state + journal + outbox entry, one transaction)
 → immutable batch: batch_id, ObjectId, expected Cloud revision, local sequence range, payload reference
 → background sender: ordered per object, parallel across objects
 → server acknowledgement advances the sent watermark
```

| # | Rule |
|---|---|
| OB-01 | **The outbox is durable and part of the commit unit** ([SY-32](../requirements/03-cloud-services-and-sync.md#rule-sy-32)). A crash immediately after save leaves it intact. |
| OB-02 | **An in-memory queue is not an outbox.** |
| OB-03 | **Ordering is per object, not global.** Cross-object ordering is never assumed. |
| OB-04 | **The outbox drains opportunistically** and never blocks local work ([SY-34](../requirements/03-cloud-services-and-sync.md#rule-sy-34)). |
| OB-05 | **A local save can never fail because the cloud failed** ([SY-34](../requirements/03-cloud-services-and-sync.md#rule-sy-34)). |

### 3.2 Server inbox

| # | Rule |
|---|---|
| IB-01 | **Every submission carries batch/command identity, ObjectId and expected Cloud revision.** The server returns the accepted revision and the original batch receipt; the client does not assign a Cloud RevisionId. |
| IB-02 | **The server deduplicates by batch CommandId and canonical request hash.** Five identical deliveries return one original receipt; reused identity with different content is refused. |
| IB-03 | **The server validates the parent revision** before accepting a change. |
| IB-04 | **Acceptance is transactional with the outbox write** that will notify other devices. |

### 3.3 Change feed and cursor

```
Client holds a SyncCursor per scope
 → requests changes after the cursor
 → server returns an ordered page: create / update / delete(tombstone) / conflict
 → client applies idempotently, advances the cursor
 → realtime notifies that new changes exist; it never carries authority
```

| # | Rule |
|---|---|
| CF-01 | **Sync is change-based; a full enumeration at start-up is prohibited** ([SY-30](../requirements/03-cloud-services-and-sync.md#rule-sy-30)). |
| CF-02 | **The cursor is durable per scope per device.** |
| CF-03 | **Application is idempotent**, so a replayed page converges identically. |
| CF-04 | **Realtime accelerates; HTTP is authoritative** ([RL-04](05-cloud-architecture.md#rule-rl-04) in the cloud architecture). |
| CF-05 | **Metadata precedes large blobs** in priority ([SY-35](../requirements/03-cloud-services-and-sync.md#rule-sy-35)). |

---

## 4. Conflict handling

### 4.1 Policies

| Policy | Applies to | Behaviour |
|---|---|---|
| **Append** | Event logs, task events, conversation entries, audit streams | Both sides retained in order |
| **Merge** | Content that can be safely merged | Structured merge, where and only where it is genuinely safe |
| **RevisionCompare** | Structured configuration and metadata | Base revision → new revision; mismatch surfaces a conflict |
| **ConflictBranch** | Complex project documents | Original plus both device versions all retained |
| **Immutable** | Blobs | Content-identified; no in-place modification exists |

| # | Rule |
|---|---|
| CP-01 | **There is no single global conflict algorithm** ([CF-01](../requirements/03-cloud-services-and-sync.md#rule-cf-01) in the cloud requirements). Each object type declares its policy. |
| CP-02 | **Silent last-write-wins on user content is prohibited** ([CF-02](../requirements/03-cloud-services-and-sync.md#rule-cf-02) there). |
| CP-03 | **Where safe automatic merge is impossible, the original and both versions are all retained.** |
| CP-04 | **The conflict is a first-class object**: participants, devices, times, base revision, and the resolution options. |
| CP-05 | **Resolution is a user act producing a new revision**, never an automatic discard. |
| CP-06 | **V1 does not force CRDT** ([CF-04](../requirements/03-cloud-services-and-sync.md#rule-cf-04) there). The goal is no silent data loss, not real-time multi-user convergence. |
| CP-07 | **The conflict rate is an operational metric** (`§9`). |

### 4.2 Concurrency at the source

Conflicts are minimised before they occur: optimistic revision on every write ([CC-06](03-local-ipc-and-process-model.md#rule-cc-06) in the local IPC architecture), per-document serial write ordering ([CC-01](03-local-ipc-and-process-model.md#rule-cc-01) there), and short transactions ([CS-03](06-data-persistence-and-formats.md#rule-cs-03) in the persistence architecture).

---

## 5. Deletion

```
Delete
 → tombstone (ObjectId, deleted-at, delete revision, actor)
 → propagate as an ordinary change
 → trash retention window: restorable, blobs retained, history retained, counts toward storage
 → permanent delete: propagation job
      canonical metadata → blob references → now-unreferenced blobs
      → version references → search documents → vector entries
      → previews and caches → future share state → backup expiry schedule
 → completion tracked
```

| # | Rule |
|---|---|
| <a id="rule-dl-01"></a>DL-01 | **Deletion is a tombstone, never a bare row removal** ([DE-01](../requirements/03-cloud-services-and-sync.md#rule-de-01) in the cloud requirements). Without it, an offline device resurrects deleted objects. |
| DL-02 | **Restore preserves `ObjectId`** ([DE-03](../requirements/03-cloud-services-and-sync.md#rule-de-03) there); it is a new revision revoking the tombstone. |
| DL-03 | **Permanent deletion is a tracked propagation job**, not a single statement ([DE-04](../requirements/03-cloud-services-and-sync.md#rule-de-04), [DE-05](../requirements/03-cloud-services-and-sync.md#rule-de-05) there). |
| DL-04 | **A deleted document must not remain discoverable through semantic search** ([I-165](../requirements/01-normative-glossary-and-invariants.md#rule-i-165)). |
| DL-05 | **Deletion propagation backlog is an operational metric** (`§9`). |
| DL-06 | **The disaster-backup honesty rule holds**: deleted data becomes immediately inaccessible online and disappears from backups when retention elapses ([DE-06](../requirements/03-cloud-services-and-sync.md#rule-de-06) there). |

---

## 6. Blob lifecycle

```text
Client requests upload admission -> reserve bounded staging/storage bytes
  -> upload immutable chunks outside the transaction
  -> completeUpload verifies checksum/length/type -> Verified + provisional pin
  -> owner content/manifest commit enlists Resource and Entitlement
  -> promote object to Committed, convert quota hold to committed bytes,
     add exact object references, commit the referencing revision/publication
  -> or expiry/abandonment -> inaccessible releasing state -> verified deletion
```

An unattached upload is Verified, not Committed. A standalone saved attachment or simulator segment has an explicit owning aggregate/manifest whose commit promotes it. Download authorization requires that owner/reference, not merely an upload ticket. Verification and promotion are separate idempotent transitions. A failed content commit leaves a bounded verified staging object and its hold for retry/expiry, never a published broken reference.

| # | Rule |
|---|---|
| BL-01 | **A revision may reference a blob only after verification** ([BL-08](../requirements/03-cloud-services-and-sync.md#rule-bl-08) in the cloud requirements). This is what prevents orphan blobs and broken references. |
| BL-02 | **The client never holds a permanent storage credential** ([BL-07](../requirements/03-cloud-services-and-sync.md#rule-bl-07) there). |
| BL-03 | **Upload is multipart and resumable**; a failure re-sends only failed parts ([BL-06](../requirements/03-cloud-services-and-sync.md#rule-bl-06) there). |
| BL-04 | **The integrity hash is computed and stored by ArcForges.** A provider's composite entity tag is never treated as a content hash ([I-218](../requirements/01-normative-glossary-and-invariants.md#rule-i-218)). |
| BL-05 | **Blobs are immutable and content-identified** ([BL-01](../requirements/03-cloud-services-and-sync.md#rule-bl-01) there); an edit produces a new blob and the revision changes its reference. |
| BL-06 | **Deduplication is workspace-scoped only.** Cross-user global deduplication is prohibited ([BL-10](../requirements/03-cloud-services-and-sync.md#rule-bl-10) there). |
| BL-07 | **Staged blobs with no committing revision are garbage-collected after a bounded window** ([BL-09](../requirements/03-cloud-services-and-sync.md#rule-bl-09) there). |
| BL-08 | **Download verifies hash and length before content reaches the application** ([BL-11](../requirements/03-cloud-services-and-sync.md#rule-bl-11) there). |
| BL-09 | **Blob keys never expose user filenames** ([BL-03](../requirements/03-cloud-services-and-sync.md#rule-bl-03) there). |

---

## 7. Asset availability

| State | Meaning |
|---|---|
| `AlwaysKeep` | Retained locally regardless of pressure |
| `AvailableOffline` | Downloaded; may be offloaded under explicit user action |
| `OnDemand` | Fetched when opened |
| `CloudOnly` | Placeholder locally |
| `MissingExternal` | An external reference whose target is not reachable here |

| # | Rule |
|---|---|
| AV-01 | **Only a managed asset may be offloaded, and only after an explicit user action** ([AS-06](../requirements/03-cloud-services-and-sync.md#rule-as-06) in the cloud requirements). |
| AV-02 | **An external reference is never offloaded or deleted by ArcForges.** |
| AV-03 | **Availability is separate from identity** ([RR-09](02-contracts-and-protocols.md#rule-rr-09) in the contracts architecture). |
| AV-04 | **New-device bootstrap fetches metadata, catalogue and small content first** ([AS-08](../requirements/03-cloud-services-and-sync.md#rule-as-08) there). |

---

## 8. Protection profiles

| Profile | Server capability |
|---|---|
| **Standard** (V1) | TLS in transit, encryption at rest, workspace isolation, strict service authorization, secret separation — enabling cloud search, semantic indexing, cloud agent, managed AI context and web access |
| **EndToEndEncrypted** — **retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** | End-to-end encryption, custom local encrypted stores and encrypted portable exports are excluded. TLS in transit, server-side storage and backup protection, system secret storage and pending-work recovery remain. The profile value is retired and not reused. Historical definition: the server saw opaque objects: sync, versioning and download to a trusted device work; server-side full-text search, semantic search, cloud-native agent context and cloud preview do not |

| # | Rule |
|---|---|
| PR-01 | Standard authenticated Cloud processing is the only protection profile. No E2EE mode, key-sharing protocol or future encryption-profile column is introduced ([PR-02](../requirements/03-cloud-services-and-sync.md#rule-pr-02) of the cloud requirements). |
| PR-02 | The service states where content is processed, its retention and access protections. Custom local encrypted stores and encrypted exports are excluded ([PR-03](../requirements/03-cloud-services-and-sync.md#rule-pr-03) of the cloud requirements). |
| PR-03 | **No zero-knowledge claim is made while Standard is the operating mode** ([PR-04](../requirements/03-cloud-services-and-sync.md#rule-pr-04) there). |

---

## 9. Data health

A continuous background service checking for: metadata referencing a missing blob; a blob with no metadata reference; a revision with a missing parent; a search document with a missing source; a tombstoned object still searchable; a primary blob with no backup copy; a conflict older than a threshold; and an unfinished deletion propagation.

Tracked indicators: `BrokenReferences`, `OrphanBlobs`, `ConflictRate`, `SyncBacklog`, `ChecksumFailures`, `BackupLag`, `RestoreFailures`, `DeletionBacklog`, `IndexDrift`.

**These are operational metrics with alert thresholds, not a dashboard nobody reads** ([QD-01](../requirements/12-quality-and-compatibility-contract.md#rule-qd-01) in the quality contract).

---

## 10. Backup topology

```
Layer 1   Local durable state                    on the user's machine
Layer 2   Cloud sync revisions                   the replicated canonical record
Layer 3   Version history + trash window         user-recoverable
Layer 4   Primary immutable backup protection    object lock on the primary provider
Layer 5   Independent cross-provider copy        a different provider, object lock, separate fault domain
```

| # | Rule |
|---|---|
| BK-01 | **Metadata uses continuous archiving plus base backups for point-in-time recovery.** A nightly dump alone is insufficient (`BK-01` in the cloud requirements). |
| BK-02 | **Provider durability is not backup** ([I-219](../requirements/01-normative-glossary-and-invariants.md#rule-i-219)). It protects against media failure, not against a mistaken deletion script, stolen credentials, a wrong lifecycle rule, operator error or an account-level disaster. |
| BK-03 | **The second copy lives in a different provider and a different fault domain** ([BK-04](../requirements/03-cloud-services-and-sync.md#rule-bk-04) there), under object lock with a retention period. |
| BK-04 | **Backup is naturally incremental** because blobs are immutable: each new blob is copied once and never re-copied ([BK-05](../requirements/03-cloud-services-and-sync.md#rule-bk-05) there). |
| BK-05 | **A backup exists only once a restore has been proven** ([BK-06](../requirements/03-cloud-services-and-sync.md#rule-bk-06) there): automated daily sample restores with checksum verification, a monthly small-scale drill, and a quarterly full disaster-recovery exercise into a fresh environment. |
| <a id="rule-bk-06"></a>BK-06 | **A backup health dashboard is mandatory** ([BK-07](../requirements/03-cloud-services-and-sync.md#rule-bk-07) there). |
| BK-07 | **Backup never blocks a user save** ([BK-08](../requirements/03-cloud-services-and-sync.md#rule-bk-08) there). Primary commit succeeds; replication is asynchronous; lag beyond objective raises an operational alert. |
| BK-08 | **User content retention and commercial record retention are separate** ([BK-09](../requirements/03-cloud-services-and-sync.md#rule-bk-09) there). |

---

## 11. Export and realm migration

| # | Rule |
|---|---|
| EX-01 | **Workspace export produces a documented manifest plus per-product data plus managed assets** ([EX-02](../requirements/03-cloud-services-and-sync.md#rule-ex-02), [EX-03](../requirements/03-cloud-services-and-sync.md#rule-ex-03) in the cloud requirements). |
| EX-02 | **Export remains available throughout the post-entitlement retention window** ([SB-02](../requirements/03-cloud-services-and-sync.md#rule-sb-02) there). |
| EX-03 | **Import treats the package as untrusted input** ([EX-05](../requirements/03-cloud-services-and-sync.md#rule-ex-05) there). |
| EX-04 | **Realm migration in V1 is export then import** ([SH-05](../requirements/03-cloud-services-and-sync.md#rule-sh-05) there). |
| EX-05 | **Realms never share object-identity authority.** An imported object may retain an origin identity for provenance; the receiving realm mints its own identity and mapping ([SH-04](../requirements/03-cloud-services-and-sync.md#rule-sh-04) there). |
| EX-06 | **Self-host uses the same protocol and data model** ([SH-03](../requirements/03-cloud-services-and-sync.md#rule-sh-03) there). There is no simplified second sync implementation. |

---

## 12. Schema versioning across devices

| # | Rule |
|---|---|
| SV-01 | **Every syncable payload carries `ObjectType` and `SchemaVersion`** (`SV-01` in the cloud requirements). |
| SV-02 | **Mixed versions across a user's devices are the normal case**, because products release independently ([P-12](../requirements/00-product-scope-and-portfolio.md#rule-p-12)). |
| SV-03 | **An older client must never silently destroy newer data** ([SV-02](../requirements/03-cloud-services-and-sync.md#rule-sv-02) there). Unknown fields survive a round trip. |
| SV-04 | **Compatibility negotiation expresses `Readable`, `Writable`, `RequiresUpgrade`** ([SV-03](../requirements/03-cloud-services-and-sync.md#rule-sv-03) there). |
| SV-05 | **A `RequiresUpgrade` object is visible and legible, and is not editable by the older client.** |

---

## 13. Sync test matrix

Required scenarios, all release-gating:

**Convergence** — one, two and three devices · long-offline return · duplicated change · out-of-order change · API timeout · server retry.

**Conflict** — simultaneous edit of one object · simultaneous rename · simultaneous edit and delete · conflict branch retained · resolution produces a new revision.

**Deletion** — delete propagates · **tombstone prevents resurrection by a returning offline device** · restore preserves identity · permanent delete removes search and vector entries · propagation completes.

**Assets** — 1 KB, 100 MB and multi-gigabyte uploads · multipart interruption and resume · hash mismatch rejected · one asset referenced by several objects · managed offload and rehydrate · **an external asset is never uploaded automatically**.

**Quota** — approaching quota · storage full pauses uploads only · over-quota after downgrade permits read, download and delete · dropping below quota resumes automatically.

**Backup** — point-in-time restore · missing primary blob restored from the second provider · credential-compromise simulation · erroneous deletion simulation · object lock enforced · random checksum restore · full drill.

**Versioning** — a newer client writing to an older-client-visible object · an older client encountering a newer schema · unknown-field round trip.

**Security** — cross-workspace object-id probe · cross-workspace blob-id probe · expired upload authorization · stolen upload URL · revoked device.

---

## 14. Traceability

| Current document | Relationship |
|---|---|
| [Cloud Services, Sync, Assets and Data Integrity Requirements](../requirements/03-cloud-services-and-sync.md) | Owns sync scopes, revisions, conflicts, blobs, retention and backup |
| [Working Data, Project Formats and Cloud Portability Requirements](../requirements/13-data-formats-and-portability.md) | Owns local durability and portable-format boundaries |
| [Cloud Data Model](data-model/01-cloud-data-model.md) | Defines Cloud sync, resource, deletion and quota records |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Cloud persistence posture |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Direct product-to-cloud sync without an ArcChat gateway |

## P2-009 transport, storage and recovery composition

The [CF/R2 lifecycle](contracts/05-cloudflare-integration.md) fixes part verification, Verified pins, authorization on consumption, release/deletion and independent immutable restore. C# owning transactions, sync cursors/tombstones/conflicts, desktop pending changes, native job snapshots and derived-source revision checks above retain their semantics. The [wire profile](contracts/04-protobuf-wire-registry.md) transports exact values without changing content-origin, Notes scalar or Scope measurement oracles. CF checkpoints/streams never become product history, and restoration cannot silently redispatch an uncertain external act.

## Restored realm and client pending state

The [recovery generation and safety journal](22-deployment-and-release-execution.md#recovery-generation-and-safety-journal) governs disaster recovery and prevents acknowledged post-backup deletion/revocation or possibly executed commands from disappearing silently. A new generation invalidates read cursors and quarantines old client mutations before bootstrap. Preserved pending edits are compared and explicitly reapplied as new commands; no automatically re-labelled outbox can resurrect deleted content. This extends the existing pending-edit recovery view and does not create a second local Notes authority.
