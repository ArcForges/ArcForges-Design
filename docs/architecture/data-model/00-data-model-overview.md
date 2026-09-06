# Data Model Overview

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Data model
> Governing authority: **D-008** (runtime matrix), **D-009** (contract granularity), **D-010** (topology), **D-011** (implementation target)
> Companions: [`../06-data-persistence-and-formats.md`](../06-data-persistence-and-formats.md) (mechanism), [`../05-cloud-architecture.md`](../05-cloud-architecture.md) `§5`, [`../07-sync-conflict-and-backup.md`](../07-sync-conflict-and-backup.md)

The persistence architecture states *how* storage behaves. This layer states *what is stored*: the entities, their keys, their relationships, the constraints that hold them together, and where authority for each lives.

**Why this layer exists.** Without it an implementer must invent the fundamental data relationships — which entity owns which, what a foreign key means across a sync boundary, whether a deletion cascades, which column carries the revision. Those inventions would differ per product and per module, and the resulting inconsistencies would surface as data-loss defects rather than compile errors.

---

## 1. Documents in this layer

| Document | Covers |
|---|---|
| `00-data-model-overview.md` (this) | Conventions, authority map, cross-store rules, transaction boundaries, deletion and retention semantics |
| [`01-cloud-data-model.md`](01-cloud-data-model.md) | Every Cloud module's entities, keys, relationships, indexes and constraints |
| [`02-desktop-data-model.md`](02-desktop-data-model.md) | The shared local store and each desktop product's schema |
| [`03-derived-stores.md`](03-derived-stores.md) | Search, retrieval, projection and cache stores — all rebuildable |

---

## 2. Notation

These documents specify data models, not DDL. An entity is given as its name, its key, its fields with types and nullability, its relationships, its indexes and its constraints. That is enough to generate a schema in any supported store without inventing semantics.

| Notation | Meaning |
|---|---|
| `PK` | Primary key |
| `FK →` | Foreign key, with the referenced entity and the on-delete behaviour |
| `UQ` | Unique constraint |
| `IX` | Non-unique index, with the query path it serves |
| `NN` | Not null |
| `?` after a type | Nullable |
| `⊕` | Discriminated union — exactly one variant present |
| *(derived)* | Never authoritative; reconstructable from other rows |

**Type vocabulary.** `id` is a typed 128-bit identifier (`§3.1`); `rev` is a monotonic revision (`§3.2`); `seq` is a channel sequence number; `instant` is an unambiguous point in time; `zoned` is an instant plus its originating zone; `money` is fixed-precision with a currency; `text` is unbounded Unicode; `blobref` is a content-addressed reference, never a path; `json` is a schema-validated structured value; `enum(...)` is a closed wire enumeration.

---

## 3. Identifier and versioning conventions

### 3.1 Identifiers

The implementation repository already establishes the convention, and this layer adopts it unchanged: every identifier is a `readonly record struct XId(Guid Value)` with `Guid.CreateVersion7()` generation, its own JSON converter, and no implicit conversion to or from any other identifier type.

| # | Rule |
|---|---|
| ID-01 | **Version 7 identifiers.** They sort by creation time, which makes them index-friendly as primary keys and gives natural chronological ordering without a separate column. |
| ID-02 | **One identifier type per concept.** Passing a `WorkspaceId` where a `TaskId` is required is a compile error (`WP-04.00`). |
| ID-03 | **An identifier is opaque to clients.** No client parses structure out of one, and no identifier encodes a tenant, a shard or a kind. |
| ID-04 | **Identifiers are allocated by the writer, not the store.** A client allocates the identifier for an entity it creates, which is what makes create idempotent under retry (`§6.2`). |
| ID-05 | **An identifier is never reused**, including after hard deletion. |
| ID-06 | **A cross-store identifier is the same value.** A document synced to Cloud keeps its local `DocumentId`; there is no separate cloud identifier and no mapping table. |

**The identifier set.** `RealmId`, `UserId`, `AuthIdentityId`, `WorkspaceId`, `MembershipId`, `DeviceId`, `InstallationId`, `InstanceId`, `SessionId`, `ApiTokenId`, `BillingAccountId`, `OfferId`, `PriceVersionId`, `PurchaseIntentId`, `CheckoutAttemptId`, `OrderId`, `PaymentId`, `SubscriptionId`, `GrantId`, `RevocationId`, `CreditLotId`, `ReservationId`, `LedgerEntryId`, `ProviderEventId`, `TaskId`, `RunId`, `PlanId`, `StepId`, `AttemptId`, `CommandId`, `InvocationId`, `ApprovalId`, `AutomationId`, `ConversationId`, `BranchId`, `MessageId`, `ProjectId`, `AgentProfileId`, `SkillId`, `DocumentId`, `BlockId`, `NotebookId`, `TagId`, `PropertyDefId`, `ViewId`, `SlideDeckId`, `SessionRecordId` (ArcScope), `CaptureId`, `SegmentId`, `ChannelId`, `SignalId`, `AnalysisId`, `FindingId`, `ReportId`, `SlateProjectId`, `SequenceId`, `TrackId`, `TimelineItemId`, `MediaAssetId`, `EffectInstanceId`, `RenderRequestId`, `ResourceId`, `BlobId`, `UploadSessionId`, `ArtifactId`, `PackageId`, `InstallationPackageId`, `NotificationId`, `AuditEventId`, `SupportCaseId`.

### 3.2 Revision, sequence and concurrency

| # | Rule |
|---|---|
| RV-01 | **Every mutable aggregate root carries `rev`**, a monotonic 64-bit counter maintained by its owner (`PS-03`, `CS-05`). |
| RV-02 | **`rev` increments once per commit unit**, never once per changed field and never once per child row. |
| RV-03 | **A child row does not carry its own `rev`.** Its concurrency is the aggregate root's. A block belongs to a document's revision; a message belongs to a conversation's. |
| RV-04 | **Every mutating operation carries `expectedRev`.** A mismatch is a typed conflict, never a silent overwrite. `expectedRev = 0` means *create*. |
| RV-05 | **`seq` is per channel, not per entity**, and orders delivery. `Revision ≠ Sequence` (`I-…` in the glossary catalogue), and neither is derivable from the other. |
| RV-06 | **A revision is meaningful only within its aggregate.** Comparing revisions across aggregates is a defect. |

### 3.3 Aggregate roots

An aggregate root is the unit of concurrency, authorization and sync. Everything else is a child.

| Store | Aggregate roots |
|---|---|
| Cloud | `Workspace`, `User`, `Device`, `Subscription`, `Grant`, `CreditLot`, `Task`, `Conversation`, `SyncScope`, `CloudObject`, `PolicyBundle`, `PackageInstallation`, `SupportCase` |
| ArcChat local | `Conversation`, `ArcChatProject`, `AgentProfile`, `Skill`, `Task` |
| ArcNotes local | `Document`, `Notebook`, `Canvas`, `SavedView`, `SlideDeck`, `PropertyDefinition`, `Tag` |
| ArcScope local | `ScopeProject`, `SessionRecord`, `Capture`, `AnalysisDefinition`, `Finding`, `Report`, `ConnectionProfile` |
| ArcSlate local | `SlateProject`, `Sequence`, `MediaAsset`, `ExportPreset`, `RenderRequest` |

| # | Rule |
|---|---|
| AG-01 | **A transaction never spans two aggregate roots in different modules.** Cross-aggregate consistency is achieved through the outbox, never through a wider transaction (`§6.3`). |
| AG-02 | **A foreign key across an aggregate boundary is a reference, not a cascade.** Deleting a referenced aggregate never silently deletes a referencing one. |
| AG-03 | **An aggregate is the unit of sync.** A sync change record names an aggregate root and its revision. |

---

## 4. Authority map — where the authoritative copy lives

This is the single most consequential table in the data layer. Every entity has exactly one authoritative store; every other copy is a projection, a cache or a durable pending change.

**P2-006 moves the authority for synchronised user data to Cloud.** Native clients keep a working cache of acknowledged revisions plus durable pending edits (`I-498`). Hardware acquisition and media working stores keep product-local authority.

| Entity family | Authoritative store | Held by clients as | Rule |
|---|---|---|---|
| Realm, User, AuthIdentity, Session, ApiToken | **Cloud — Identity** | A session token only, never a user record | Identity has no local authoritative copy |
| Workspace | **Cloud — Workspace** | Read-only cache | **Single-owner; there is no Membership entity** (`WO-01`) |
| Device, Installation, Presence, Trust | **Cloud — Devices** | Its own identity locally | Trust level is cloud-authoritative |
| ServiceTerm, CapacityBucket, Grant, Revocation, EntitlementSnapshot, Quota, UsageCounter | **Cloud — Entitlement** | Allowlisted projection with its version (`CG-05`) | A client never computes admission (`AD-01`) |
| BillingAccount, Offer, Order, Payment, Subscription, CreditLot, LedgerEntry, ProviderEvent, LogicalAIRequest, ProviderAttempt, AttemptUsage, SupplierCost, CustomerSettlement | **Cloud — Commerce** | Read projections only | No local write path exists |
| ConfigRevision | **Cloud — Configuration** | Allowlisted client projection only (`DC-14`) | Supplier rates and thresholds never ship to a client |
| Conversation, Message, Branch, ArcChatProject, AgentProfile, Skill | **Cloud — Chat/Agent** | Working cache + **unsent drafts** (`I-124`) | A draft is local until appended and acknowledged |
| Document, Block, Link, Tag, Property, SavedView | **Cloud — Notes** for acknowledged revisions | Working cache + **durable pending edits** (`PE-01`) | A pending edit is never discarded as cache (`PE-03`) |
| Task, Run, Plan, Step, Attempt, Approval, ToolRequest, ToolResult | **Cloud — Task/Agent** | Read projection | **Always Cloud-owned** (`§4.1`); only tool locality varies |
| Native Product Job — render, capture, index, export | **The running product** | Its own durable job record | **Not a Cloud Agent Task** (`I-121`, `I-485`); invokes no model |
| ScopeProject, SessionRecord, Capture metadata, Analysis, Finding, Report | **ArcScope local** | — | Metadata synced; **raw capture is local by default** (`I-474`) |
| SimulationDefinition, ScenarioVersion, SimulationRun, Segment, Checkpoint | **Cloud — Scope** | Downloaded segments are a verified copy | **Synthetic, cloud-owned, quota-counted** (`I-496`, `SIM-01`, `C-09`) |
| SlateProject, Sequence, Timeline, MediaAsset metadata | **ArcSlate local** | — | Project data synced; heavyweight media by explicit policy |
| OTIO artifact | **Neither** — an interchange file | Produced and consumed, never the working store | `I-497`; export binds a committed sequence revision (`OT-04`) |
| CloudObject, Blob, UploadSession | **Cloud — Resource** | Content-addressed cache; **staged uploads are pending, not cache** (`PE-02`) | A copy is verifiable by hash |
| Artifact | **The producing product** | Referenced by identity | `ArtifactRef` carries provenance, never the body |
| PolicyBundle, Flag, KillSwitch | **Cloud — Policy** | Cached with staleness and last-known-good | Compiled hard limits win over any cached value |
| AuditEvent | **Cloud — Audit** (cloud actions); **local audit store** (local actions) | Neither replicates to the other | Two append-only stores, correlated by identifier only |
| SearchIndex, RetrievalIndex, Projection, Thumbnail, Proxy, RenderCache | **Derived** — nowhere authoritative | — | Deleting every one leaves the product intact |

| # | Rule |
|---|---|
| AU-01 | **Acknowledgement is the authority boundary.** A revision Cloud has acknowledged is authoritative in Cloud; a change it has not is authoritative on the device that holds it, and is durable there (`PE-01`). |
| AU-02 | **There is no second notebook authority.** A native client never becomes the durable owner of an acknowledged revision, and requiring a Cloud acknowledgement before a local durable save is equally prohibited (item 9 of the architecture baseline changes). |
| AU-03 | **A product job is not an agent task.** Confusing the two would put a render under AI metering and Cloud recovery, which is wrong in both directions (`CM-04` of the runtime architecture).

### 4.1 Task ownership and tool locality

A Task can be created from any surface — desktop, Web, Mobile or an automation trigger. **Ownership never follows the creator, because ownership is always Cloud.**

| # | Rule |
|---|---|
| TO-01 | **Every Agent Task is Cloud-owned** (**P2-006**). `Task.owningProduct` records which product's domain the work concerns; it does not move the authoritative store. |
| TO-02 | **`Task.toolLocality ∈ {cloud, device}` is recorded per Step, not per Task.** A single Task may mix both. The old `placement ∈ {local, cloud, remoteViaBridge}` field is **retired**: there is no local task placement (`I-491`). |
| TO-03 | **The authoritative record is always `task.task` in Cloud.** Every client — including the desktop that created the Task — holds a read projection. |
| TO-04 | **A device Step's execution attempts are recorded in Cloud from the returned `ToolResult`**, and mirrored in the device's own `command_log` for local idempotency. Neither writes the other's rows (`BI-03` of the bridge contract). |
| TO-05 | **A native Product Job is not a Task at all.** A render, capture, index or export is owned and recovered by its product, has its own durable job record, and never appears in `task.task` (`AU-03`, `I-121`, `I-485`). |
| TO-06 | **Tool locality is decided per Step and recorded.** A Step declared `device` is never silently satisfied by a cloud approximation (`PL-02` of the harness); if no eligible device is online it waits with a stated reason (`WP-26.06`). |
| TO-07 | **A projection is stamped with the authoritative revision it was built from**, so a stale projection is detectable rather than silently wrong. |

---

## 5. Cross-store relationships

Four store kinds coexist: the local structured store, the Cloud database, object storage, and derived stores. Relationships between them are constrained.

| # | Rule |
|---|---|
| XS-01 | **A foreign key never crosses a store boundary.** A local row referring to a cloud object holds a `blobref` or an identifier, and the referential integrity is maintained by application logic plus a health check, never by the database. |
| XS-02 | **Object storage holds bodies; a database holds metadata, ownership and lifecycle** (`PS-07`). A row that would exceed the inline limit carries a `blobref` instead. |
| XS-03 | **The inline threshold is a declared constant**, not a per-caller judgement. Content at or above it goes to object storage. |
| XS-04 | **A blob is content-addressed.** `blobref` = (`blobId`, `contentHash`, `sizeBytes`). A local managed copy and a cloud object with the same hash are the same content, and either may satisfy a read. |
| XS-05 | **A reference to a not-yet-committed blob is never published** (`§7` of the sync architecture: Staged → Verified → Committed). |
| XS-06 | **A derived store never holds the only copy of anything**, and its rows carry the source identifier and source revision they were built from. |
| XS-07 | **An orphan is detectable in both directions**: a reference with no object, and an object with no reference. Both are data-health anomaly classes with repair actions (`WP-46.04`). |

---

## 6. Transaction boundaries

### 6.1 What a single transaction may contain

| Scope | Permitted in one transaction |
|---|---|
| **Local store** | One aggregate root's state change, its command record, its journal entry, its revision increment, and its sync outbox entry (`§2.1` of the persistence architecture) |
| **Cloud database** | One module's aggregate change plus its outbox rows plus its idempotency row (`PS-04`) |
| **Across modules** | **Never.** Module-to-module effect is achieved by outbox → event → inbox |
| **Across stores** | **Never.** No transaction spans the database and object storage |

### 6.2 Idempotency

| # | Rule |
|---|---|
| TX-01 | **Every state-changing operation carries a `CommandId`** allocated by the caller. |
| TX-02 | **The command record is written inside the same transaction as its effect.** That is what makes exactly-once effect true rather than hoped for. |
| TX-03 | **A duplicate `CommandId` returns the original result**, including the original resulting revision. It does not re-execute and does not error. |
| TX-04 | **The command record retains the response payload** for the retention window, so a retry after a lost response returns the same answer rather than a conflict. |
| TX-05 | **The command retention window is longer than the maximum client retry window**, and both are declared. |
| TX-06 | **A create is idempotent because the client allocates the identifier** (`ID-04`). Re-issuing a create with the same identifier and the same command returns the existing row. |

### 6.3 The outbox

| # | Rule |
|---|---|
| OB-01 | **An outbox row is written in the business transaction** (`PS-04`). |
| OB-02 | **An outbox row carries** its identifier, the aggregate it concerns, the aggregate revision after the change, the event type, the payload, the correlation and causation identifiers, and its dispatch state. |
| OB-03 | **Dispatch is at-least-once.** Every consumer is idempotent through the inbox. |
| OB-04 | **The inbox deduplicates by `(source, messageId)`** and retains the record for a declared window. |
| OB-05 | **A dispatch failure never rolls back the business change.** The change is committed; the notification retries. |

---

## 7. Deletion, retention and their interaction

Deletion is where data models usually fail, because five different meanings get one verb.

| Meaning | What it does | Reversible? | Propagates to sync? |
|---|---|---|---|
| **Trash** | Sets an aggregate's state to `trashed` with a timestamp; content intact | Yes, until purge | Yes, as a state change |
| **Purge** | Removes content, leaves a **tombstone** carrying identity, deletion time and deleting actor | No | Yes, as a tombstone |
| **Unsync** | Removes the cloud replica; the local authoritative copy is untouched | Yes, by re-enabling scope | Yes, as a scope change — **not** a deletion |
| **Cloud deletion** | Removes the cloud replica **and** records a deletion that propagates to other devices | Only within the recovery window | Yes |
| **Account deletion** | Removes cloud-side account data after a grace period; **local data is never touched** | Within the grace period only | Terminates sync |

| # | Rule |
|---|---|
| DL-01 | **A tombstone outlives the content.** Its retention exceeds the maximum plausible device-offline period, so a returning device converges rather than resurrecting (`WP-25.04`). |
| DL-02 | **Tombstone retention is a declared value**, and a device offline beyond it is required to perform a full resync rather than a delta. |
| DL-03 | **Purging an aggregate purges its children in the same transaction.** Children have no independent lifetime. |
| DL-04 | **Purging an aggregate does not purge what it merely references.** An ArcNotes document referencing a managed attachment releases a reference; the attachment is removed only when its reference count reaches zero and the grace period elapses. |
| DL-05 | **Reference counting is transactional with the referencing change**, and the garbage collector never removes an object whose count is above zero or whose grace period has not elapsed (`WP-07.04`). |
| DL-06 | **Deleting a professional resource created by an extension is prohibited by extension uninstall** (`PU-06` in the extension architecture). |
| DL-07 | **An audit event is never deleted by any of the five operations.** Audit retention is independent and policy-governed. |
| DL-08 | **A financial record is never deleted.** Commerce rows are append-only (`BC-05`). |
| DL-09 | **A deletion that cannot complete is retried and reported, never silently abandoned.** A stuck purge is a data-health anomaly. |

### 7.1 Retention windows

Each is versioned commercial or operational policy, not a compiled constant. The design fixes the *relationships*, which are binding:

| Relationship | Binding constraint |
|---|---|
| Tombstone retention | **>** the maximum supported offline period, which is itself declared |
| Command idempotency retention | **>** the maximum client retry window |
| Trash retention | **≥** the deleted-item recovery window offered to the user |
| Blob grace period after last reference release | **>** the maximum in-flight sync window, so a concurrent reference is never orphaned |
| Audit retention | **≥** every other retention window in the system |
| Provider event retention | **≥** the reconciliation lookback window |

---

## 8. Consistency model per relationship

| Relationship | Consistency | Mechanism |
|---|---|---|
| Aggregate root ↔ its children | **Strong** | One transaction |
| Aggregate ↔ its outbox row | **Strong** | Same transaction |
| Module ↔ module, within Cloud | **Eventual, exactly-once effect** | Outbox → event → inbox |
| Local store ↔ Cloud replica | **Eventual, convergent** | Outbox → change feed → conflict policy |
| Device ↔ device | **Eventual, convergent** | Through Cloud only; devices never talk directly |
| Database ↔ object storage | **Eventual, verifiable** | Staged → Verified → Committed, plus orphan detection |
| Canonical ↔ derived | **Eventual, rebuildable** | Rebuild is always available and always correct |
| Entitlement ↔ its cached snapshot | **Eventual, versioned** | `EntitlementVersion` comparison; realtime is a refresh hint only |
| Commerce ↔ provider | **Eventual, reconciled** | Event inbox plus two-way reconciliation |

| # | Rule |
|---|---|
| CM-01 | **"Eventual consistency" is never used without naming its mechanism and its convergence check.** Every row above names both. |
| CM-02 | **No relationship in this system relies on a distributed transaction.** |
| CM-03 | **Every eventual relationship has a detectable divergence signal** and a repair action (`WP-46.04`). |

---

## 9. Query paths and indexing discipline

An index exists because a named query path needs it. The per-entity documents list indexes with the path each serves.

| # | Rule |
|---|---|
| QP-01 | **Every index names the query path it serves.** An index with no named path is removed. |
| QP-02 | **Every list query is paginated with a stable cursor**, and the cursor is opaque and scope-bound (`WP-23.02`). |
| QP-03 | **Every tenant-scoped table's primary query path leads with the tenant column**, so a query cannot accidentally scan across workspaces. |
| QP-04 | **A query plan is reviewed at scale-corpus size**, not at development size (`CS-07`). |
| QP-05 | **A soft-deleted row is excluded by the index, not by the caller** — partial indexes on the active state, so a forgotten predicate cannot leak trashed content. |

---

## 10. Multi-tenancy enforcement

| # | Rule |
|---|---|
| MT-01 | **Every workspace-scoped table carries `workspaceId` as a real column**, never derived by join at query time. |
| MT-02 | **Tenancy is resolved once in the request pipeline and enforced again at the data layer** (`WP-21.06`). A forged scope must fail at the data layer even if the pipeline is bypassed. |
| MT-03 | **A cross-workspace query is impossible through the repository surface.** Operator queries that legitimately span workspaces use a separate, audited path (`§10` of the observability architecture). |
| MT-04 | **A cross-workspace foreign key is a defect**, except where the referenced entity is workspace-independent (Offer, PolicyBundle, ModelDescriptor, PackageDefinition). Those are enumerated per module. |

---

## 11. Schema evolution

| # | Rule |
|---|---|
| SE-01 | **Cloud uses expand → deploy → contract** (`PS-10`), so two application versions coexist during rolling deployment. |
| SE-02 | **A local store migration runs at application start, after the installer, with its own recovery path** (`UP-08`). |
| SE-03 | **A migration that cannot be reversed is split**, and the irreversible step happens only after the new version is fully deployed. |
| SE-04 | **A column is never repurposed.** Adding a column and migrating is always preferred to changing a meaning. |
| SE-05 | **A migration preserves semantics, not merely structure** (`QI-07`), verified by golden-fixture comparison. |
| SE-06 | **`StorageSchemaVersion` equals the highest applied migration** and is a distinct version axis. |
| SE-07 | **A newer device must not corrupt data an older device will read**, for the whole supported compatibility window (`§13` of the sync architecture). |

---

## 12. Verification

| # | Obligation | Where |
|---|---|---|
| DV-01 | Every aggregate round-trips through its store with all fields preserved | Per-product persistence tests |
| DV-02 | Every declared index exists and is used by its named query path, verified against the scale corpus | `WP-07`, `WP-21` |
| DV-03 | Optimistic concurrency produces a typed conflict, never a lost update, for every aggregate | `WP-07.00` |
| DV-04 | Every deletion meaning behaves as `§7` specifies, including tombstone convergence | `WP-25.04` |
| DV-05 | Reference counting never orphans and never premature-deletes, including across a crash | `WP-07.04` |
| DV-06 | A cross-workspace read fails at the data layer with a forged scope | `WP-21.06` |
| DV-07 | Every eventual relationship's divergence signal fires on an induced fault, and its repair converges | `WP-46.04` |
| DV-08 | The full migration chain preserves semantics from the earliest supported version | `WP-29.04`, `WP-21.03` |

---

## 13. Traceability

| Source | Consumed as |
|---|---|
| [`../06-data-persistence-and-formats.md`](../06-data-persistence-and-formats.md) | The storage mechanism this layer populates |
| [`../05-cloud-architecture.md`](../05-cloud-architecture.md) `§4`, `§5` | Module boundaries and persistence rules |
| [`../07-sync-conflict-and-backup.md`](../07-sync-conflict-and-backup.md) | Revision, change feed and conflict semantics |
| `ArcForges.Contracts.Foundation` in the implementation repository | The established identifier, revision, result and reference conventions this layer adopts — evidence of present convention, not design authority (**D-011**) |
| **D-010** | Why Cloud never holds a local aggregate's authority by default |
