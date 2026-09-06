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
| ArcNotes local | `Document`, `Notebook`, `SavedView`, `PropertyDefinition`, `Tag` — `Canvas` and `SlideDeck` **retired by P2-006** |
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

### 4.2 Commit authority — who executes the transaction that assigns a revision

The authority map says *where the authoritative copy lives*. It does not by itself say **who commits**, and for Chat that gap was previously filled by two contradictory sentences. This section settles it.

**Cloud is the sole committer of every acknowledged revision of synchronised data.** A client never assigns an authoritative revision. What differs between Chat and Notes is not who commits — it is where a change *originates* and whether it is durably staged before it reaches Cloud.

| | Chat | Notes |
|---|---|---|
| Origination | Any client, **or Cloud itself** (an assistant message) | A client only |
| Staged locally before submission | An unsent draft is local (`I-124`); a submitted message is not re-staged | **Yes** — a durable pending edit survives offline (`PE-01`) |
| Submitted through | `chat.appendMessage` | `sync.pushChange` |
| Committer | Cloud | Cloud |
| Revision assigned by | Cloud | Cloud |

| # | Rule |
|---|---|
| CW-01 | **A client never writes an acknowledged revision.** It submits a proposal and receives the revision Cloud assigned. `local_rev` on a client row is a device-scoped counter for pending work; it is **not** the aggregate's revision and never appears in a contract as one. |
| CW-02 | **Cloud writes Chat directly.** `chat.appendMessage` commits the user message in Cloud; the Harness commits the assistant message in Cloud. **There is no rule that Cloud may only apply a client change** — that statement described a Notes-shaped replica model and was wrong for Chat. |
| CW-03 | **A Cloud-originated row needs no client.** With every device offline, a Web user's message and the Harness's reply both commit normally; devices discover them through the change feed when they return. |
| CW-04 | **Notes changes originate on a device and are staged durably before submission** (`PE-01`), which is what makes offline editing safe. Cloud still commits, and the client's pending row clears only on the acknowledgement (`PE-02`). |
| CW-05 | **One writer per aggregate per transaction.** The module that owns the schema executes the write; no other module and no client writes those tables (`MD-02`, `SU-02`). |
| CW-06 | **Every commit that changes a synchronised aggregate writes its `sync.change` row in the same transaction** (`§9`), so a change can never be committed and un-publishable. |

#### 4.2.1 Worked path — Web message and Cloud reply with Desktop offline

| # | Step | Committer | Transaction contents | Revision |
|---|---|---|---|---|
| 1 | Web calls `chat.appendMessage` | **Cloud — Chat**, enlisting Sync | `chat.message` (user), its command record, its `sync.change` row (`origin_kind = cloud`, since Web is not a sync device) | `rev = r1`, assigned by Cloud |
| 2 | A Task is created (`CH-01`) | **Cloud — Task** | `task.task`; linked to the message by identifier | separate aggregate |
| 3 | Admission reserves (`§6.1.1`) | Entitlement + Commerce | shared unit of work; commits **before** dispatch (`DB-01`) | — |
| 4 | Provider streams; deltas are transient (`§7` of the harness) | **nobody** — the stream buffer is not an aggregate | none | none |
| 5 | Turn completes; the assistant message is committed once | **Cloud — Chat**, enlisting Sync and Task in one shared unit of work (`§6.1.1a`) | `chat.message` (assistant) + its `sync.change` row (`origin_kind = cloud`, **no device**) + the Task's terminal state | `rev = r2`, assigned by Cloud |
| 6 | Settlement | Entitlement + Commerce | A **separate** shared unit of work, after step 5 — it must not hold the message behind provider latency (`TU-01`) | — |
| 7 | Desktop reconnects and pulls from its cursor | — | reads `r1` and `r2` in publication order (`§9`). **Neither is suppressed as its own echo**, because `origin_device_id` is null and a null never matches | — |
| 8 | Desktop had an unsent draft for the same conversation | Desktop, locally | the draft is local-only and is **not** a competing revision (`I-124`) | none |

**Nothing in this path requires a device.** Step 8 is the only place a device holds state, and a draft is deliberately outside the revision model.

#### 4.2.2 Worked path — offline note edit

| # | Step | Committer | Result |
|---|---|---|---|
| 1 | User edits offline | **Device**, into its working store | Durable pending change taking the next `local_seq`; **not** an acknowledged revision (`CW-01`, `PE-04`) |
| 2 | Device reconnects, submits `sync.pushChange` with its `CommandId` | — | — |
| 3 | Cloud applies it | **Cloud — Notes** | `document`/`block` rows, the command record, and the `sync.change` row, in one transaction (`CW-06`); Cloud assigns `rev` |
| 4 | Acknowledgement returns the assigned `rev` | — | The watermark advances to **the highest `local_seq` the batch covered, and no further** (`RV-C4`). Edits made while the batch was in flight remain pending (`SB-L1`) |
| 5 | A concurrent change existed | **Cloud — Notes** | Conflict raised with both branches retained; resolution is a **new** Cloud-assigned revision |

| # | Rule |
|---|---|
| CW-07 | **`ExpectedRev` on a client write is the last acknowledged Cloud revision the client saw**, never a local sequence (`RV-C1`). A local RPC instead carries `(acked_rev, head_local_seq)` (`RV-C5`), because a local caller saw the local state including pending work. |
| CW-08 | **A conflict is resolved by a new revision, never by a client overwriting one** (`§4` of the sync architecture). |

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
| **Cloud database, ordinary case** | One module's aggregate change plus its outbox rows plus its idempotency row (`PS-04`) |
| **Cloud database, enumerated shared unit of work** | The **operation classes** listed in `§6.1.1`, and only those. Note that **every synchronised aggregate write is one of them** (`CW-06`), so this is a routine path rather than a rare exception |
| **Across stores** | **Never.** No transaction spans the database and object storage |

**Ordinary module-to-module effect is asynchronous** — outbox → event → inbox — and every consumer is idempotent (`OB-03`).

#### 6.1.1 The shared unit of work — a closed exception

Asynchronous propagation cannot express a decision that must be **all-or-nothing at the instant it is taken**. Two situations qualify, and only two.

**Funding.** AI admission draws on Entitlement's capacity bucket and Commerce's credit lots. If either half can succeed alone there is an overdraft window in which two concurrent runs each pass a check against the same unreserved funds (`AD-02`). A saga cannot close it, because the window lies *between* the two writes.

**Publication.** A synchronised aggregate's change and its `sync.change` row must commit together (`CW-06`). If they did not, a committed change could be unpublishable, or a published change could name a row that never committed. `sync` is a separate schema, so **every** synchronised write is already a two-module transaction.

Because Cloud is **one deployable host over one database** (`RT-03` of the cloud architecture), the mechanism is a genuine shared transaction with a **closed, enumerated participant list** — not a distributed protocol simulating one.

| # | Rule |
|---|---|
| SU-01 | **Only the operation classes in the table below may open a shared unit of work.** The list is closed; adding a class is an architecture baseline change. |
| SU-02 | **A participant never touches another module's tables** (`MD-02` of the cloud architecture). Each exposes a **transaction-participating API** that accepts the ambient unit of work and operates on its own tables through its own repository. The rule that survives is *no foreign table access*, which was always the point of the module boundary. |
| SU-03 | **The participant list is asserted by an architecture test**: exactly these classes, exactly these participants, and no other call site enlists a second module (`WP-05`). |
| SU-04 | **Lock order is fixed and declared, globally**: `Entitlement → Commerce → Chat → Notes → Task → Sync`. Within Entitlement, the workspace's `capacity_bucket` row first. A single global order is what makes deadlock structurally impossible rather than retried. |
| SU-05 | **A shared unit of work is short and contains no I/O.** No provider call, no object-storage write, no network hop occurs inside one. It commits, and only then does dispatch begin (`§6.1.2`). |
| SU-06 | **Every cross-module effect not in the table stays asynchronous.** Purchase → grant remains outbox-driven with its reconciliation repair (`PE-06` of the lifecycles), because money that moved is a fact and the grant can be retried forward. |
| SU-07 | **`sync` is a participant, never an initiator.** It has no operation of its own here; it is enlisted by whichever module is committing a synchronised aggregate. |

| Operation class | Participants | Why it cannot be asynchronous |
|---|---|---|
| **Synchronised aggregate write** — any commit to Chat, Notes or another synchronised store | The owning module + **Sync** (`sync.change`) | `CW-06`: a committed change must be publishable, and a published change must exist |
| **AI admission** (`§7.3` of the commerce architecture) | Entitlement (`capacity_bucket`, `capacity_reservation`) + Commerce (`credit_lot`) | The reservation must exclude concurrent runs before dispatch (`AD-02`) |
| **AI settlement** (`§7.5` there) | Entitlement + Commerce (`credit_lot`, `customer_settlement`) | Debit and release must move against the same sources the reservation held (`ST-05`) |
| **Reservation sweep** (`AI-09` of the lifecycles) | Entitlement + Commerce | Releasing a hold must restore the same sources atomically |
| **Agent turn completion** | **Chat** (`chat.message`) + **Sync** (`sync.change`) + **Task** (terminal state) | See `§6.1.1a` |

##### 6.1.1a Why turn completion is one transaction, and what it excludes

A completed turn commits the assistant message, its publication row and the Task's terminal state. Splitting them produces a state a client can observe and cannot interpret: a message with no completed Task reads as still generating; a completed Task with no message reads as an empty answer.

| # | Rule |
|---|---|
| TU-01 | **These three, and nothing else, commit together.** Settlement is **not** in this transaction — it is its own class above, running after, because it depends on usage the provider reports and must not hold the message write behind provider latency (`SU-05`). |
| TU-02 | **A crash between turn completion and settlement leaves a completed turn with an outstanding reservation.** That is a resolvable state, not a lost one: the sweeper and the usage reconciliation resolve it (`AI-08`, `UU-01`), and the user has their answer meanwhile. The reverse ordering — settling first — would risk charging for an answer that was never delivered. |
| TU-03 | **The Task's terminal state and the message are inseparable; the Task's *progress* updates are not.** Progress is written independently and is explicitly lossy (`RE-03`). |

##### 6.1.1b What stays asynchronous, and how it recovers

| Effect | Mechanism | Recovery |
|---|---|---|
| Purchase → entitlement grant | `platform.outbox` → event → Entitlement inbox | Reconciliation invariant: *every paid order has a matching grant* (`PE-06`) |
| Change → search and retrieval indexing | Outbox → indexer hosted service | Derived store; rebuildable, and losing it costs compute not content (`DS-01`) |
| Change → notification fan-out | Outbox → notification service | Durable notifications are re-readable (`RE-04`) |
| Deletion → downstream purge across stores | Outbox → per-store purger | Completion invariant per store, retried to convergence (`DE-01`, `DE-05`) |
| Settlement → ledger entries | Same transaction as settlement (**not** asynchronous) | — |

| # | Rule |
|---|---|
| AS-01 | **Every asynchronous cross-module effect names its outbox, its consumer and its recovery mechanism** in the table above. An effect with no named recovery is a defect, because at-least-once delivery without a reconciliation path is at-most-once in practice. |
| AS-02 | **No rule elsewhere demands atomicity for a row in that table.** Where a design wants an asynchronous effect to be atomic, the resolution is to add an operation class to `SU-01` — a baseline change — not to assert atomicity that `SU-06` forbids. |

#### 6.1.2 The dispatch barrier

Reservation and the external act are **separated by a commit**, so no external effect can occur inside a transaction and no transaction can be held open across a network call.

```
1. SHARED UNIT OF WORK        reserve + write dispatch intent   -> COMMIT
2. DISPATCH BARRIER           nothing before this point has touched a provider
3. EXTERNAL ACT               provider call / device tool / MCP tool
4. SEPARATE TRANSACTION       record outcome, settle, release
```

| # | Rule |
|---|---|
| DB-01 | **The dispatch intent is written before the barrier**, in the reserving transaction. Its presence with no recorded outcome means **unknown**, never *did not happen* (`§9` of the harness). |
| DB-02 | **Nothing crosses the barrier inside a transaction.** A held transaction across a provider call would hold row locks for the provider's latency and is prohibited. |
| DB-03 | **A crash between the barrier and the outcome leaves a reservation and an intent with no outcome.** That state is resolved by reconciliation, not by assuming either result (`§7.6` of the commerce architecture). |

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
| QP-03 | **Every tenant-scoped table's primary query path leads with the tenant column.** This is a *performance* property: it makes the scoped query cheap. **It is not the isolation mechanism** — isolation is enforced at the data access layer (`MT-03` of the cloud architecture), which is what makes a missing filter a structural impossibility rather than a slow query. |
| QP-04 | **A query plan is reviewed at scale-corpus size**, not at development size (`CS-07`). |
| QP-05 | **A partial index does not filter rows.** It contains only rows matching its predicate, so a query *without* that predicate simply does not use it — and returns trashed rows from a sequential scan. Partial indexes on the active state are kept for size and speed, and are **never** claimed as an exclusion guarantee. |
| QP-06 | **Soft-delete exclusion is enforced where a query cannot bypass it**: every soft-deletable aggregate is reachable from application code **only** through a repository whose read surface applies the state predicate, and the underlying table is not exposed. The negative test asserts that a trashed row is absent from every repository read path, **and** that no application assembly can construct a query against the raw table (`WP-05`). |
| QP-07 | **The same distinction applies wherever an index is described as a guarantee.** An index is a plan input. A guarantee needs a predicate the caller cannot omit — a repository, a view, or a database-enforced policy — and the mechanism is named at the point the guarantee is made. |

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
| DV-08 | The full migration chain preserves semantics from the earliest supported version | `WP-18.06`, `WP-21.03` |

---

## 13. Traceability

| Source | Consumed as |
|---|---|
| [`../06-data-persistence-and-formats.md`](../06-data-persistence-and-formats.md) | The storage mechanism this layer populates |
| [`../05-cloud-architecture.md`](../05-cloud-architecture.md) `§4`, `§5` | Module boundaries and persistence rules |
| [`../07-sync-conflict-and-backup.md`](../07-sync-conflict-and-backup.md) | Revision, change feed and conflict semantics |
| `ArcForges.Contracts.Foundation` in the implementation repository | The established identifier, revision, result and reference conventions this layer adopts — evidence of present convention, not design authority (**D-011**) |
| **D-010** | Why Cloud never holds a local aggregate's authority by default |
