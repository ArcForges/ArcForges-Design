# Data Model Overview

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Data model
> Governing authority: **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)** (runtime matrix), **[D-009](../../decisions/phase-1-foundation-decisions.md#rule-d-009)** (contract granularity), **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** (topology), **[D-011](../../decisions/phase-1-foundation-decisions.md#rule-d-011)** (implementation target)
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

<a id="canonical-id-order"></a>
**Canonical ID-byte ordering.** When a content/query profile explicitly requires ordering, compare the 16 UUID bytes obtained from left-to-right pairs of the canonical lowercase hexadecimal UUID text, ignoring hyphens, as unsigned bytes. Host-specific Guid memory layout must not change this order. General API identifiers remain opaque; ordering is used only where a profile declares it.

| # | Rule |
|---|---|
| ID-01 | **Version 7 identifiers** improve timestamp locality in indexes. Same-millisecond random bits, clock rollback and different writers make them unsuitable for business, revision or commit ordering; those use explicit revisions/publication sequence. |
| ID-02 | **One identifier type per concept.** Passing a `WorkspaceId` where a `TaskId` is required is a compile error ([WP-04.00](../../planning/work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04.00)). |
| ID-03 | **An identifier is opaque to clients.** No client parses structure out of one, and no identifier encodes a tenant, a shard or a kind. |
| <a id="rule-id-04"></a>ID-04 | **Identifiers are allocated by the writer, not the store.** A client allocates the identifier for an entity it creates, which is what makes create idempotent under retry (`§6.2`). |
| <a id="rule-id-05"></a>ID-05 | **An identifier is never reused**, including after hard deletion. |
| ID-06 | **A cross-store identifier is the same value.** A document synced to Cloud keeps its local `DocumentId`; there is no separate cloud identifier and no mapping table. |

**The identifier set.** `RealmId`, `UserId`, `AuthIdentityId`, `WorkspaceId`, `DeviceId`, `InstallationId`, `InstanceId`, `SessionId`, `ApiTokenId`, `BillingAccountId`, `OfferId`, `PriceVersionId`, `PurchaseIntentId`, `CheckoutAttemptId`, `OrderId`, `PaymentId`, `SubscriptionId`, `GrantId`, `RevocationId`, `CreditLotId`, `ReservationId`, `LedgerEntryId`, `ProviderEventId`, `TaskId`, `RunId`, `PlanId`, `StepId`, `AttemptId`, `CommandId`, `InvocationId`, `ApprovalId`, `AutomationId`, `ConversationId`, `BranchId`, `MessageId`, `ProjectId`, `AgentProfileId`, `SkillId`, `FolderId`, `DocumentId`, `BlockId`, `NotebookId`, `TagId`, `PropertyDefId`, `ViewId`, `SessionRecordId` (ArcScope), `CaptureId`, `SegmentId`, `ChannelId`, `SignalId`, `AnalysisId`, `FindingId`, `ReportId`, `SlateProjectId`, `SequenceId`, `TrackId`, `TimelineItemId`, `MediaAssetId`, `EffectInstanceId`, `RenderRequestId`, `ResourceId`, `BlobId`, `UploadSessionId`, `ArtifactId`, `ContentOriginId`, `ContentUnitId`, `PackageId`, `InstallationPackageId`, `NotificationId`, `AuditEventId`, `SupportCaseId`.

### 3.2 Revision, sequence and concurrency

| # | Rule |
|---|---|
| RV-01 | **Each authoritative mutable root carries its owner-assigned revision**: CloudRevision for Cloud authority, NativeContentRevision for native Scope/Slate work. Notes materialised projections also carry LocalNotesVersion(acked_rev, head_local_seq); a bare Cloud rev cannot represent pending local changes. |
| RV-02 | **`rev` increments once per commit unit**, never once per changed field and never once per child row. |
| <a id="rule-rv-03"></a>RV-03 | **A child row does not carry its own `rev`.** Its concurrency is the aggregate root's. A block belongs to a document's revision; a message belongs to a conversation's. |
| RV-04 | **Each conditional mutation carries the expected version of its target authority.** A local Notes edit uses the composite local token; Cloud sync uses expectedCloudRevision; native product edits use expectedNativeContentRevision. Create has an explicit create precondition. Idempotent receipt replay returns its original result, without an extra revision increment. |
| RV-05 | **`seq` is per channel, not per entity**, and orders delivery. `Revision ≠ Sequence` (distinct types and roles defined in this section), and neither is derivable from the other. |
| RV-06 | **A revision is meaningful only within its aggregate.** Comparing revisions across aggregates is a defect. |

### 3.3 Aggregate roots

An aggregate root is the unit of concurrency, authorization and sync. Everything else is a child.

| Store | Aggregate roots |
|---|---|
| Cloud | `Workspace`, `User`, `Device`, `Subscription`, `Grant`, `CreditLot`, `Task`, `Conversation`, `Notebook`, `Document`, `SavedView`, `PropertyDefinition`, `Tag`, `SyncScope`, `CloudObject`, `PolicyBundle`, `PackageInstallation`, `SupportCase` |
| ArcChat local | Acknowledged read projections of `Conversation`, `ArcChatProject`, `AgentProfile`, `Skill` and Cloud Task; durable unsent drafts and device-tool receipts have local ownership |
| ArcNotes local | Working projections and pending edits for `Document`, `Notebook` (including its folders), `SavedView`, `PropertyDefinition`, `Tag`; no canvas or slide domain |
| ArcScope local | `ScopeProject`, `SessionRecord`, `Capture`, `AnalysisDefinition`, `Finding`, `Report`, `ConnectionProfile` |
| ArcSlate local | `SlateProject`, `Sequence`, `MediaAsset`, `ExportPreset`, `RenderRequest` |

| # | Rule |
|---|---|
| <a id="rule-ag-01"></a>AG-01 | **Cross-module transactions are limited to the operation families in §6.1.1.** Each participant accesses only its own tables. Other cross-module effects use a named outbox consumer and recovery invariant. Within one module, a declared command may lock multiple roots in sorted identity order when a folder move or another structural invariant requires it. |
| AG-02 | **A foreign key across an aggregate boundary is a reference, not a cascade.** Deleting a referenced aggregate never silently deletes a referencing one. |
| AG-03 | **An aggregate is the unit of sync.** A sync change record names an aggregate root and its revision. |

---

## 4. Authority map — where the authoritative copy lives

This is the single most consequential table in the data layer. Every entity has exactly one authoritative store; every other copy is a projection, a cache or a durable pending change.

**[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) moves the authority for synchronised user data to Cloud.** Native clients keep a working cache of acknowledged revisions plus durable pending edits ([I-498](../../requirements/01-normative-glossary-and-invariants.md#rule-i-498)). Hardware acquisition and media working stores keep product-local authority.

| Entity family | Authoritative store | Held by clients as | Rule |
|---|---|---|---|
| Realm, User, AuthIdentity, Session, ApiToken | **Cloud — Identity** | A session token only, never a user record | Identity has no local authoritative copy |
| Workspace | **Cloud — Workspace** | Read-only cache | **Single-owner; there is no Membership entity** ([WO-01](01-cloud-data-model.md#rule-wo-01)) |
| Device, Installation, Presence, Trust | **Cloud — Devices** | Its own identity locally | Trust level is cloud-authoritative |
| ServiceTerm, CapacityBucket, Grant, Revocation, EntitlementSnapshot, Quota, UsageCounter | **Cloud — Entitlement** | Allowlisted projection with its version ([CG-05](../16-billing-and-commerce-architecture.md#rule-cg-05)) | A client never computes admission ([AD-01](../16-billing-and-commerce-architecture.md#rule-ad-01)) |
| BillingAccount, Offer, Order, Payment, Subscription, CreditLot, LedgerEntry, ProviderEvent, LogicalAIRequest, ProviderAttempt, AttemptUsage, SupplierCost, CustomerSettlement | **Cloud — Commerce** | Read projections only | No local write path exists |
| ConfigRevision | **Cloud — Configuration** | Allowlisted client projection only ([DC-14](../../requirements/11-policy-and-configuration.md#rule-dc-14)) | Supplier rates and thresholds never ship to a client |
| Conversation, Message, Branch, ArcChatProject, AgentProfile, Skill | **Cloud — Chat/Agent** | Working cache + **unsent drafts** ([I-124](../../requirements/01-normative-glossary-and-invariants.md#rule-i-124)) | A draft is local until appended and acknowledged |
| Notebook, Folder, Document, Block, Link, Tag, Property, SavedView | **Cloud — Notes** for acknowledged revisions | Working cache + **durable pending edits** ([PE-01](02-desktop-data-model.md#rule-pe-01)) | A pending edit is never discarded as cache ([PE-03](02-desktop-data-model.md#rule-pe-03)) |
| Task, Run, Plan, Step, Attempt, Approval, ToolRequest, ToolResult | **Cloud — Task/Agent** | Read projection | **Always Cloud-owned** (`§4.1`); only tool locality varies |
| Native Product Job — render, capture, index, export | **The running product** | Its own durable job record | **Not a Cloud Agent Task** ([I-121](../../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)); invokes no model |
| ScopeProject, SessionRecord, Capture metadata, Analysis, Finding, Report | **ArcScope local** | — | Metadata synced; **raw capture is local by default** ([I-474](../../requirements/01-normative-glossary-and-invariants.md#rule-i-474)) |
| SimulationDefinition, ScenarioVersion, SimulationRun, Segment, Checkpoint | **Cloud — Scope** | Downloaded segments are a verified copy | **Synthetic, cloud-owned, quota-counted** ([I-496](../../requirements/01-normative-glossary-and-invariants.md#rule-i-496), [SIM-01](../../requirements/products/arcscope.md#rule-sim-01), [C-09](../../requirements/00-product-scope-and-portfolio.md#rule-c-09)) |
| SlateProject, Sequence, Timeline, MediaAsset metadata | **ArcSlate local** | — | Project data synced; heavyweight media by explicit policy |
| OTIO artifact | **Neither** — an interchange file | Produced and consumed, never the working store | [I-497](../../requirements/01-normative-glossary-and-invariants.md#rule-i-497); export binds a committed sequence revision ([OT-04](../../requirements/products/arcslate.md#rule-ot-04)) |
| CloudObject, Blob, UploadSession | **Cloud — Resource** | Content-addressed cache; **staged uploads are pending, not cache** ([PE-02](02-desktop-data-model.md#rule-pe-02)) | A copy is verifiable by hash |
| Artifact | **The producing product** | Referenced by identity | `ArtifactRef` carries provenance, never the body |
| PolicyBundle, Flag, KillSwitch | **Cloud — Policy** | Cached with staleness and last-known-good | Compiled hard limits win over any cached value |
| AuditEvent | **Cloud — Audit** (cloud actions); **local audit store** (local actions) | Neither replicates to the other | Two append-only stores, correlated by identifier only |
| SearchIndex, RetrievalIndex, Projection, Thumbnail, Proxy, RenderCache | **Derived** — nowhere authoritative | — | Deleting every one leaves the product intact |

| # | Rule |
|---|---|
| <a id="rule-au-01"></a>AU-01 | **Acknowledgement is the authority boundary.** A revision Cloud has acknowledged is authoritative in Cloud; a change it has not is authoritative on the device that holds it, and is durable there ([PE-01](02-desktop-data-model.md#rule-pe-01)). |
| AU-02 | **There is no second notebook authority.** A native client never becomes the durable owner of an acknowledged revision, and requiring a Cloud acknowledgement before a local durable save is equally prohibited (item 9 of the architecture baseline changes). |
| <a id="rule-au-03"></a>AU-03 | **A product job is not an agent task.** Confusing the two would put a render under AI metering and Cloud recovery, which is wrong in both directions ([CM-04](../09-ai-and-agent-runtime-architecture.md#rule-cm-04) of the runtime architecture). |

### 4.1 Task ownership and tool locality

A Task can be created from any surface — desktop, Web, Mobile or an automation trigger. **Ownership never follows the creator, because ownership is always Cloud.**

| # | Rule |
|---|---|
| <a id="rule-to-01"></a>TO-01 | **Every Agent Task is Cloud-owned** (**[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)**). `Task.owningProduct` records which product's domain the work concerns; it does not move the authoritative store. |
| <a id="rule-to-02"></a>TO-02 | **`Task.toolLocality ∈ {cloud, device}` is recorded per Step, not per Task.** A single Task may mix both. The old `placement ∈ {local, cloud, remoteViaBridge}` field is **retired**: there is no local task placement ([I-491](../../requirements/01-normative-glossary-and-invariants.md#rule-i-491)). |
| <a id="rule-to-03"></a>TO-03 | **The authoritative record is always `task.task` in Cloud.** Every client — including the desktop that created the Task — holds a read projection. |
| TO-04 | **A device Step's execution attempts are recorded in Cloud from the returned `ToolResult`**, and mirrored in the device's own `command_log` for local idempotency. Neither writes the other's rows ([BI-03](../contracts/03-realtime-and-bridge.md#rule-bi-03) of the bridge contract). |
| <a id="rule-to-05"></a>TO-05 | **A native Product Job is not a Task at all.** A render, capture, index or export is owned and recovered by its product, has its own durable job record, and never appears in `task.task` ([AU-03](#rule-au-03), [I-121](../../requirements/01-normative-glossary-and-invariants.md#rule-i-121), [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). |
| <a id="rule-to-06"></a>TO-06 | **Tool locality is decided per Step and recorded.** A Step declared `device` is never silently satisfied by a cloud approximation ([PL-02](../17-agent-harness.md#rule-pl-02) of the harness); if no eligible device is online it waits with a stated reason ([WP-26.06](../../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.06)). |
| <a id="rule-to-07"></a>TO-07 | **A projection is stamped with the authoritative revision it was built from**, so a stale projection is detectable rather than silently wrong. |

---

### 4.2 Commit authority — who executes the transaction that assigns a revision

The authority map says *where the authoritative copy lives*. It does not by itself say **who commits**, and for Chat that gap was previously filled by two contradictory sentences. This section settles it.

**Cloud assigns every Cloud replica revision.** Chat and Notes use that revision as the authority for acknowledged content. ArcScope and ArcSlate additionally retain a product-local `content_rev` for their native working store and jobs; the Cloud replica revision never replaces it. A device submits against its last acknowledged Cloud replica revision, not against a native working revision. Chat and Notes differ in origination and local staging:

| | Chat | Notes |
|---|---|---|
| Origination | Any client, **or Cloud itself** (an assistant message) | A client only |
| Staged locally before submission | An unsent draft is local ([I-124](../../requirements/01-normative-glossary-and-invariants.md#rule-i-124)); a submitted message is not re-staged | **Yes** — a durable pending edit survives offline ([PE-01](02-desktop-data-model.md#rule-pe-01)) |
| Submitted through | `chat.appendMessage` | `sync.pushChange` |
| Committer | Cloud | Cloud |
| Revision assigned by | Cloud | Cloud |

| # | Rule |
|---|---|
| <a id="rule-cw-01"></a>CW-01 | **A client never assigns a Cloud acknowledgement.** Notes stages edits with `local_seq`; its local optimistic token is `(acked_rev, head_local_seq)`. Native Scope/Slate operations use their own `content_rev`, while the replication envelope separately carries `expected_cloud_rev`. These version domains are distinct contract types. |
| <a id="rule-cw-02"></a>CW-02 | **Cloud writes Chat directly.** `chat.appendMessage` commits the user message in Cloud; the Harness commits the assistant message in Cloud. **There is no rule that Cloud may only apply a client change** — that statement described a Notes-shaped replica model and was wrong for Chat. |
| <a id="rule-cw-03"></a>CW-03 | **A Cloud-originated row needs no client.** With every device offline, a Web user's message and the Harness's reply both commit normally; devices discover them through the change feed when they return. |
| CW-04 | **Notes changes originate on a device and are staged durably before submission** ([PE-01](02-desktop-data-model.md#rule-pe-01)), which is what makes offline editing safe. Cloud still commits, and the client's pending row clears only on the acknowledgement ([PE-02](02-desktop-data-model.md#rule-pe-02)). |
| CW-05 | **One writer per aggregate per transaction.** The module that owns the schema executes the write; no other module and no client writes those tables ([MD-02](../05-cloud-architecture.md#rule-md-02), [SU-02](#rule-su-02)). |
| <a id="rule-cw-06"></a>CW-06 | **Every commit that changes a synchronised aggregate writes its `sync.change` row in the same transaction** (`§9`), so a change can never be committed and un-publishable. |

#### 4.2.1 Worked path — Web message and Cloud reply with Desktop offline

| # | Step | Committer | Transaction contents | Revision |
|---|---|---|---|---|
| 1 | Web calls `chat.appendMessage` | **Cloud — Chat**, enlisting Sync | `chat.message` (user), its command record, its `sync.change` row (`origin_kind = cloud`, since Web is not a sync device) | `rev = r1`, assigned by Cloud |
| 2 | Task creation is part of step 1 when the selected profile starts a Turn | **Cloud — Task**, enlisted by Chat | `task.task` linked to the message and original command receipt in the same commit | Separate aggregate, atomic acceptance |
| 3 | Admission reserves (`§6.1.1`) | Entitlement + Commerce | shared unit of work; commits **before** dispatch ([DB-01](#rule-db-01)) | — |
| 4 | Provider streams, then each invocation output is persisted and settled | **Cloud — Commerce/Task/Chat** | Transient presentation chunks, then immutable iteration output and usage evidence; separate idempotent settlement | No final conversation revision yet |
| 5 | Turn completes; the assistant message is committed once | **Cloud — Chat**, enlisting Sync and Task in one shared unit of work (`§6.1.1a`) | `chat.message` (assistant) + its `sync.change` row (`origin_kind = cloud`, **no device**) + the Task's terminal state | `rev = r2`, assigned by Cloud |
| 6 | Reconciliation if any usage remains unknown | Entitlement + Commerce | Customer deadline and supplier liability are tracked independently; ordinary per-call settlement already occurred in step 4 | — |
| 7 | Desktop reconnects and pulls from its cursor | — | reads `r1` and `r2` in publication order (`§9`). **Neither is suppressed as its own echo**, because `origin_device_id` is null and a null never matches | — |
| 8 | Desktop had an unsent draft for the same conversation | Desktop, locally | the draft is local-only and is **not** a competing revision ([I-124](../../requirements/01-normative-glossary-and-invariants.md#rule-i-124)) | none |

**Nothing in this path requires a device.** Step 8 is the only place a device holds state, and a draft is deliberately outside the revision model.

#### 4.2.2 Worked path — offline note edit

| # | Step | Committer | Result |
|---|---|---|---|
| 1 | User edits offline | **Device**, into its working store | Durable pending change taking the next `local_seq`; **not** an acknowledged revision ([CW-01](#rule-cw-01), [PE-04](02-desktop-data-model.md#rule-pe-04)) |
| 2 | Device reconnects, submits `sync.pushChange` with its `CommandId` | — | — |
| 3 | Cloud applies it | **Cloud — Notes** | `document`/`block` rows, the command record, and the `sync.change` row, in one transaction ([CW-06](#rule-cw-06)); Cloud assigns `rev` |
| 4 | Acknowledgement returns the assigned `rev` | — | The watermark advances to **the highest `local_seq` the batch covered, and no further** ([RV-C4](02-desktop-data-model.md#rule-rv-c4)). Edits made while the batch was in flight remain pending ([SB-L1](02-desktop-data-model.md#rule-sb-l1)) |
| 5 | A concurrent change existed | **Cloud — Notes** | Conflict raised with both branches retained; resolution is a **new** Cloud-assigned revision |

| # | Rule |
|---|---|
| CW-07 | **A sync submission carries the last acknowledged Cloud revision as `expectedRev`.** Notes local RPC uses `(acked_rev, head_local_seq)`; native Scope/Slate RPC uses `content_rev`. A transport adapter never substitutes one version domain for another. |
| CW-08 | **A conflict is resolved by a new revision, never by a client overwriting one** (`§4` of the sync architecture). |

## 5. Cross-store relationships

Four store kinds coexist: the local structured store, the Cloud database, object storage, and derived stores. Relationships between them are constrained.

| # | Rule |
|---|---|
| <a id="rule-xs-01"></a>XS-01 | **A foreign key never crosses a store boundary.** A local row referring to a cloud object holds a `blobref` or an identifier, and the referential integrity is maintained by application logic plus a health check, never by the database. |
| XS-02 | **Object storage holds bodies; a database holds metadata, ownership and lifecycle** ([PS-07](../05-cloud-architecture.md#rule-ps-07)). A row that would exceed the inline limit carries a `blobref` instead. |
| XS-03 | **The inline threshold is a declared constant**, not a per-caller judgement. Content at or above it goes to object storage. |
| XS-04 | **A blob is content-addressed.** `blobref` = (`blobId`, `contentHash`, `sizeBytes`). A local managed copy and a cloud object with the same hash are the same content, and either may satisfy a read. |
| <a id="rule-xs-05"></a>XS-05 | **A reference to a not-yet-committed blob is never published** (`§7` of the sync architecture: Staged → Verified → Committed). |
| <a id="rule-xs-06"></a>XS-06 | **A derived store never holds the only copy of anything**, and its rows carry the source identifier and source revision they were built from. |
| XS-07 | **An orphan is detectable in both directions**: a reference with no object, and an object with no reference. Both are data-health anomaly classes with repair actions ([WP-46.04](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.04)). |

---

## 6. Transaction boundaries

### 6.1 What a single transaction may contain

| Scope | Permitted in one transaction |
|---|---|
| **Local store** | One aggregate root's state change, its command record, its journal entry, its revision increment, and its sync outbox entry (`§2.1` of the persistence architecture) |
| **Cloud database, ordinary case** | One module's aggregate change plus its outbox rows plus its idempotency row ([PS-04](../05-cloud-architecture.md#rule-ps-04)) |
| **Cloud database, enumerated shared unit of work** | The **operation classes** listed in `§6.1.1`, and only those. Note that **every synchronised aggregate write is one of them** ([CW-06](#rule-cw-06)), so this is a routine path rather than a rare exception |
| **Across stores** | **Never.** No transaction spans the database and object storage |

**Ordinary module-to-module effect is asynchronous** — outbox → event → inbox — and every consumer is idempotent ([OB-03](#rule-ob-03)).

#### 6.1.1 Shared units of work

Cloud is one deployable host and one PostgreSQL database. A unit of work owns one connection and transaction. A participant exposes a transaction-aware application port and accesses only its own schema. Ordinary effects use outbox/inbox; the following operation families require a shared commit because partial visibility would violate an existing product invariant.

| # | Rule |
|---|---|
| <a id="rule-su-01"></a>SU-01 | **The write-participant list below is closed.** Adding a family or participant is an architecture change. Read-only authorisation and policy ports may participate without acquiring write ownership of their tables. |
| <a id="rule-su-02"></a>SU-02 | **No foreign table access.** The coordinator passes the ambient transaction to each module's own port; it never executes SQL against another module's tables. |
| SU-03 | **Enlistment is observable and tested.** Architecture tests assert the family, permitted participants and their write sets, including optional Resource/Sync enlistment when a body/reference/publication is involved. |
| SU-04 | **Acquire locks in module order:** Config → Identity → Workspace → Device → Entitlement → Commerce → Policy → Agent → Chat → Notes → Scope → Slate → Task → Notification → Resource → Sync. Within a module sort stable keys; Notes locks notebooks before documents. Entitlement locks quota/bucket rows before reservation rows. Collect the complete lock set before modifying anything. Constraint/index locks can still deadlock: abort and retry the entire idempotent transaction with bounded jitter, never a partial statement or an external act. |
| <a id="rule-su-05"></a>SU-05 | **No external I/O inside the transaction.** Provider, object-storage and device calls happen outside it. Pre-staged verified bodies are promoted/pinned by metadata only. Every operation has bounded rows, bytes and time; large purges/exports use durable jobs. |
| SU-06 | **Everything not listed uses a named asynchronous recovery path.** A producer outbox row is part of its business commit. No caller reports the downstream effect as complete until its durable state confirms it. |
| <a id="rule-su-07"></a>SU-07 | **Sync publishes another module's commit; it does not own that module's body.** Only the owner decides whether the proposal is valid. |

| Operation family | Write participants | Commit invariant |
|---|---|---|
| Synchronised content or structural mutation, history restore, or reference release | Entitlement when quota changes + owning content module + Resource when references/pins change + Sync | Current body, immutable revision, command receipt, exact reference set and publication row agree; Notes may lock several roots for a declared structural command |
| Chat acceptance that starts an Agent Task | Entitlement when quota changes + Chat + Task + Resource when attachments are pinned + Sync | User message and its linked Task are created once with one command receipt; accepted work cannot disappear between message and task creation |
| AI admission and provider dispatch intent | Entitlement + Commerce | Customer reservation when applicable, total Run budget, concurrency permits, supplier exposure reservation and provider intent all exist before dispatch |
| Provider-call durable outcome | Entitlement when quota changes + Commerce + Chat + Task, plus Resource for a staged body | Attempt/usage evidence and immutable iteration output/tool proposals agree; this is not final Turn completion |
| Customer settlement, cancellation/sweep of customer holds, refund adjustment | Entitlement + Commerce | Advance accrual before changing holds, then debit/release against original funding sources and append accounting entries once; supplier liability remains independent |
| Agent Turn terminal outcome | Entitlement when quota changes + Chat + Task + Resource when needed + Sync | Terminal Task carries the final/interrupted message reference or an explicit no-answer outcome; no completed Task points at an uncommitted answer |
| Resource upload admission, verified-object promotion, final release/GC accounting | Entitlement + Resource | Staging/storage/egress reservations and committed-byte accounting transition once with object state; network deletion is separate and retryable |
| Simulator admission, bounded segment publication, cancellation and permit release | Entitlement + Scope + Resource | Product permits and bytes are reserved; manifest/checkpoint and segment references commit together under the current fence; AI credits are untouched |
| Policy-file activation | Config + Entitlement + Commerce + Agent + Policy | Active head, immutable route/tariff/offer/client projections and capacity-policy intervals agree on one revision; no workspace balance moves during activation |
| Browser authentication completion | Identity + Device | Consumed one-use browser flow, lowest-trust device/installation and live opaque-cookie session commit together; lost response may require a fresh authentication flow |
| Device revocation | Identity + Device + Notification | Device denial, session revocation and push-registration revocation become visible together; queued tool withdrawals follow the named asynchronous path |

#### 6.1.1a Per-call delivery and final Turn completion

| # | Rule |
|---|---|
| TU-01 | **A logical AI request is one bounded model invocation.** A Turn can contain many such requests. Persist the invocation's durable output/tool proposals and usage evidence before its customer settlement. A tool-only response used by the Harness is delivered work; it need not terminate the Task. |
| TU-02 | **Settle that request before admitting the next model invocation.** A restart can reconstruct an unsettled request from its immutable output and usage identity. It never needs to re-call the model to learn whether an answer was stored. Unknown usage follows the deadline policy; moving to the next invocation requires the remaining authorised Run budget and cannot erase unresolved supplier exposure. |
| TU-03 | **Final Turn completion is a separate shared transaction.** It assembles the final answer from durable iteration parts, commits its Chat revision/publication and the terminal Task together. Cancellation/failure may commit an interrupted message or an explicit `noAnswer` outcome. Already delivered, authorised per-call usage is not contingent on the Turn later succeeding. |
| TU-04 | **A crash at every seam has a durable discriminator.** Intent without outcome means unknown effect; persisted output without settlement means settlement pending; settled iterations without terminal Turn mean resume the Harness from those iterations. None authorises blind provider redispatch. |

#### 6.1.1b Asynchronous recovery

| Effect | Producer / consumer | Durable completion and recovery |
|---|---|---|
| Purchase → entitlement term/grant | Commerce `platform.outbox` → Entitlement inbox | Every completed order maps to an idempotent term/grant; reconciliation repairs a missing delivery |
| Content → search/index projections | Content outbox → Search indexer | Version-guarded derived projection; rebuild and journal/feed catch-up |
| Content/Task → notifications | Owner outbox → Notification inbox | Durable attention is readable even if push fails |
| Account/device denial → queued work withdrawal | Identity/Device outbox → Task inbox | Admission and device execution recheck denial immediately; cancellation consumer drains queued work idempotently |
| Deletion → per-store purge | Deletion coordinator outbox → named module purgers | Per-store completion records, retries and retention; no false global completion |
| Logical object release → physical object removal | Resource outbox → Resource deletion worker | `releasing` object is inaccessible; delete external bytes idempotently, then commit deletion and release physical-capacity accounting |
| Settlement → accounting report/projection | Commerce outbox → reporting consumer | Ledger entries are already in the settlement transaction; only reports are asynchronous |

| # | Rule |
|---|---|
| AS-01 | **An asynchronous effect names its producer, consumer and reconciliation predicate.** The tables above are the baseline; a new effect must extend the baseline before implementation. |

#### 6.1.2 Dispatch barrier

```text
1. Reserve permitted customer/operator resources and write provider intent -> COMMIT
2. Perform the provider/device/MCP act outside every database transaction
3. Persist outcome and durable output -> COMMIT
4. Settle the logical request from verified evidence -> COMMIT
5. Continue the Turn, or commit its explicit terminal outcome
```

| # | Rule |
|---|---|
| <a id="rule-db-01"></a>DB-01 | **A provider intent is an actual `commerce.provider_attempt` row in `intentCommitted` state**, bound to its logical request, lease fence and supplier reservation. The provider's own request reference is nullable until received. Device/MCP intent similarly names the durable tool request/attempt before sending. |
| <a id="rule-db-02"></a>DB-02 | **No network act occurs before its intent commit.** The dispatcher's current fence and cancellation/availability policy are checked at admission to dispatch; already committed/in-flight acts follow uncertain-effect recovery. |
| <a id="rule-db-03"></a>DB-03 | **Intent without a recorded outcome is unknown.** Reconcile by declared provider/owner idempotency or status, then the configured deadline; never infer no effect from a missing result. |
| DB-04 | **Infrastructure leases carry a monotonically increasing fence token.** Every effect-publication transaction checks the current holder/token and expiry under the lease row lock. An expired process cannot publish after another holder takes over. |

### 6.2 Idempotency

| # | Rule |
|---|---|
| <a id="rule-tx-01"></a>TX-01 | **Every state-changing operation carries a `CommandId`** allocated by the caller. |
| TX-02 | **The command record is written inside the same transaction as its effect.** That is what makes exactly-once effect true rather than hoped for. |
| <a id="rule-tx-03"></a>TX-03 | **A duplicate `CommandId` returns the original result**, including the original resulting revision. It does not re-execute and does not error. |
| <a id="rule-tx-04"></a>TX-04 | **The command record retains the response payload** for the retention window, so a retry after a lost response returns the same answer rather than a conflict. |
| TX-05 | **The command retention window is longer than the maximum client retry window**, and both are declared. |
| <a id="rule-tx-06"></a>TX-06 | **A create is idempotent because the client allocates the identifier** ([ID-04](#rule-id-04)). Re-issuing a create with the same identifier and the same command returns the existing row. |

### 6.3 The outbox

| # | Rule |
|---|---|
| <a id="rule-ob-01"></a>OB-01 | **An outbox row is written in the business transaction** ([PS-04](../05-cloud-architecture.md#rule-ps-04)). |
| OB-02 | **An outbox row carries** its identifier, the aggregate it concerns, the aggregate revision after the change, the event type, the payload, the correlation and causation identifiers, and its dispatch state. |
| <a id="rule-ob-03"></a>OB-03 | **Dispatch is at-least-once.** Every consumer is idempotent through the inbox. |
| OB-04 | **The inbox deduplicates by `(source, messageId)`** and retains the record for a declared window. |
| <a id="rule-ob-05"></a>OB-05 | **A dispatch failure never rolls back the business change.** The change is committed; the notification retries. |

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
| DL-01 | **A tombstone outlives the content.** Its retention exceeds the maximum plausible device-offline period, so a returning device converges rather than resurrecting ([WP-25.04](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.04)). |
| <a id="rule-dl-02"></a>DL-02 | **Tombstone retention is a declared value**, and a device offline beyond it is required to perform a full resync rather than a delta. |
| DL-03 | **Purging an aggregate purges its children in the same transaction.** Children have no independent lifetime. |
| DL-04 | **Purging an aggregate does not purge what it merely references.** An ArcNotes document referencing a managed attachment releases a reference; the attachment is removed only when its reference count reaches zero and the grace period elapses. |
| <a id="rule-dl-05"></a>DL-05 | **Reference counting is transactional with the referencing change**, and the garbage collector never removes an object whose count is above zero or whose grace period has not elapsed ([WP-07.04](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.04)). |
| <a id="rule-dl-06"></a>DL-06 | **Deleting a professional resource created by an extension is prohibited by extension uninstall** ([PU-06](../15-extension-platform-architecture.md#rule-pu-06) in the extension architecture). |
| <a id="rule-dl-07"></a>DL-07 | **An audit event is never deleted by any of the five operations.** Audit retention is independent and policy-governed. |
| <a id="rule-dl-08"></a>DL-08 | **A financial record is never deleted.** Commerce rows are append-only ([BC-05](../16-billing-and-commerce-architecture.md#rule-bc-05)). |
| <a id="rule-dl-09"></a>DL-09 | **A deletion that cannot complete is retried and reported, never silently abandoned.** A stuck purge is a data-health anomaly. |

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
| CM-03 | **Every eventual relationship has a detectable divergence signal** and a repair action ([WP-46.04](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.04)). |

---

## 9. Query paths and indexing discipline

An index exists because a named query path needs it. The per-entity documents list indexes with the path each serves.

| # | Rule |
|---|---|
| QP-01 | **Every index names the query path it serves.** An index with no named path is removed. |
| QP-02 | **Every list query is paginated with a stable cursor**, and the cursor is opaque and scope-bound ([WP-23.02](../../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.02)). |
| QP-03 | **Every tenant-scoped table's primary query path leads with the tenant column.** This is a *performance* property: it makes the scoped query cheap. **It is not the isolation mechanism** — isolation is enforced at the data access layer ([MT-03](../05-cloud-architecture.md#rule-mt-03) of the cloud architecture), which is what makes a missing filter a structural impossibility rather than a slow query. |
| QP-04 | **A query plan is reviewed at scale-corpus size**, not at development size ([CS-07](../06-data-persistence-and-formats.md#rule-cs-07)). |
| <a id="rule-qp-05"></a>QP-05 | **A partial index does not filter rows.** It contains only rows matching its predicate, so a query *without* that predicate simply does not use it — and returns trashed rows from a sequential scan. Partial indexes on the active state are kept for size and speed, and are **never** claimed as an exclusion guarantee. |
| <a id="rule-qp-06"></a>QP-06 | **Soft-delete exclusion is enforced where a query cannot bypass it**: every soft-deletable aggregate is reachable from application code **only** through a repository whose read surface applies the state predicate, and the underlying table is not exposed. The negative test asserts that a trashed row is absent from every repository read path, **and** that no application assembly can construct a query against the raw table ([WP-05](../../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05)). |
| QP-07 | **The same distinction applies wherever an index is described as a guarantee.** An index is a plan input. A guarantee needs a predicate the caller cannot omit — a repository, a view, or a database-enforced policy — and the mechanism is named at the point the guarantee is made. |

---

## 10. Multi-tenancy enforcement

| # | Rule |
|---|---|
| MT-01 | **Every workspace-scoped table carries `workspaceId` as a real column**, never derived by join at query time. |
| MT-02 | **Tenancy is resolved once in the request pipeline and enforced again at the data layer** ([WP-21.06](../../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.06)). A forged scope must fail at the data layer even if the pipeline is bypassed. |
| <a id="rule-mt-03"></a>MT-03 | **A cross-workspace query is impossible through the repository surface.** Operator queries that legitimately span workspaces use a separate, audited path (`§10` of the observability architecture). |
| <a id="rule-mt-04"></a>MT-04 | **A cross-workspace foreign key is a defect**, except where the referenced entity is workspace-independent (Offer, PolicyBundle, ModelDescriptor, PackageDefinition). Those are enumerated per module. |

---

## 11. Schema evolution

| # | Rule |
|---|---|
| <a id="rule-se-01"></a>SE-01 | **Cloud uses expand → deploy → contract** ([PS-10](../05-cloud-architecture.md#rule-ps-10)), so two application versions coexist during rolling deployment. |
| SE-02 | **A local store migration runs at application start, after the installer, with its own recovery path** ([UP-08](../../requirements/10-distribution-update-and-support.md#rule-up-08)). |
| SE-03 | **A migration that cannot be reversed is split**, and the irreversible step happens only after the new version is fully deployed. |
| SE-04 | **A column is never repurposed.** Adding a column and migrating is always preferred to changing a meaning. |
| SE-05 | **A migration preserves semantics, not merely structure** ([QI-07](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-07)), verified by golden-fixture comparison. |
| <a id="rule-se-06"></a>SE-06 | **`StorageSchemaVersion` equals the highest applied migration** and is a distinct version axis. |
| <a id="rule-se-07"></a>SE-07 | **A newer device must not corrupt data an older device will read**, for the whole supported compatibility window (`§13` of the sync architecture). |

---

## 12. Verification

| # | Obligation | Where |
|---|---|---|
| DV-01 | Every aggregate round-trips through its store with all fields preserved | Per-product persistence tests |
| DV-02 | Every declared index exists and is used by its named query path, verified against the scale corpus | [WP-07](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07), [WP-21](../../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21) |
| DV-03 | Optimistic concurrency produces a typed conflict, never a lost update, for every aggregate | [WP-07.00](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.00) |
| DV-04 | Every deletion meaning behaves as `§7` specifies, including tombstone convergence | [WP-25.04](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.04) |
| DV-05 | Reference counting never orphans and never premature-deletes, including across a crash | [WP-07.04](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.04) |
| DV-06 | A cross-workspace read fails at the data layer with a forged scope | [WP-21.06](../../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.06) |
| DV-07 | Every eventual relationship's divergence signal fires on an induced fault, and its repair converges | [WP-46.04](../../planning/work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.04) |
| DV-08 | The full migration chain preserves semantics from the earliest supported version | [WP-18.06](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.06), [WP-21.03](../../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) |

---

## 13. Traceability

| Source | Consumed as |
|---|---|
| [`../06-data-persistence-and-formats.md`](../06-data-persistence-and-formats.md) | The storage mechanism this layer populates |
| [`../05-cloud-architecture.md`](../05-cloud-architecture.md) `§4`, `§5` | Module boundaries and persistence rules |
| [`../07-sync-conflict-and-backup.md`](../07-sync-conflict-and-backup.md) | Revision, change feed and conflict semantics |
| `ArcForges.Contracts.Foundation` in the implementation repository | The established identifier, revision, result and reference conventions this layer adopts — evidence of present convention, not design authority (**[D-011](../../decisions/phase-1-foundation-decisions.md#rule-d-011)**) |
| **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Why Cloud never holds a local aggregate's authority by default |
