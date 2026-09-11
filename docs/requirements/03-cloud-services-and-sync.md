# Cloud Services, Sync, Assets and Data Integrity Requirements
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Governing authority: `docs/decisions/phase-1-foundation-decisions.md` (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**, **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)**, **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)**)
> Companions: [`02-identity-account-and-workspace.md`](02-identity-account-and-workspace.md), [`13-data-formats-and-portability.md`](13-data-formats-and-portability.md), [`../architecture/05-cloud-architecture.md`](../architecture/05-cloud-architecture.md), [`../architecture/07-sync-conflict-and-backup.md`](../architecture/07-sync-conflict-and-backup.md)

ArcForges Cloud is **the continuity and remote-execution layer of ArcForges** — not "local software moved onto a server", and not a network drive.

```
ArcForges Cloud
├── Continuity        cross-device, Web, Mobile, task-state continuity
├── Sync & Recovery   replication, version history, restore, cloud storage
├── Remote Execution  remote tasks, device scheduling, automation
└── Managed Services  cloud search, subscription AI, metering, notifications
```

**Founding principle:** Cloud owns AI orchestration and acknowledged synchronised revisions. Native clients preserve working caches and pending edits during outages; local acquisition/media jobs keep running. No offline AI or account-free notebook service is promised.

---

## 1. Commercial policy parameters

Every numeric allowance below is **versioned commercial policy under [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)**, not a frozen figure. Each requires Commercial Operations Owner specification and Product Owner approval at first consumption and again before launch. The illustrative defaults in this table are *proposals* so that design work has a concrete shape; nothing here is a commitment.

| Parameter | Illustrative proposed default | Status |
|---|---|---|
| Included workspace shared storage | 50 GB | Proposal; requires approval |
| Version history window | 30 days | Proposal; requires approval |
| Deleted-item recovery window | 30 days | Proposal; requires approval |
| Payment grace period | 7 days | Proposal; requires approval |
| Post-entitlement cloud retention | 30 days | Proposal; requires approval |
| Infrastructure backup retention | ≈ 35 days | Proposal; requires approval |
| Storage add-on tiers | +100 GB / +500 GB / +1 TB | Proposal; requires approval |

Two figures are **structural**, not policy, and are binding: storage is **workspace-shared, not per-product**, and storage/AI constraints are honestly disclosed under [C-04](00-product-scope-and-portfolio.md#rule-c-04)/C-09. Replenishing AI capacity is specified by commerce [AC-01](04-commerce-entitlement-and-credits.md#rule-ac-01)–AC-12.

---

## 2. Cloud capability bundle

| Capability | Native/offline boundary | Active official service |
|---|---|---|
| Editor/capture/media operations | Available for local files and authorised hydrated data | Cloud features separately enabled |
| Notebook/chat continuity | Scoped cache/pending drafts; no autonomous AI | Acknowledged data, sync, history and recovery |
| Search | Keyword/metadata over available native data | Cloud keyword and permitted semantic search |
| AI tasks/automation | No local loop/provider-key mode | Cloud single Harness, included capacity and opt-in extra credits |
| Scope simulator | Downloaded captures remain inspectable | Real deterministic Cloud simulation under resource/storage limits |

| # | Requirement |
|---|---|
| CL-01 | Purchased credits remain recorded after subscription expiry but are spendable only during an active paid service term. |
| CL-02 | After PaidThrough, new official AI/model-based jobs stop and capacity does not replenish. Native pending work is preserved; retained Cloud data stays readable/exportable under the published retention lifecycle. |
| <a id="rule-cl-03"></a>CL-03 | Capability health is independent. An AI provider outage does not stop note sync, keyword search or native editing; status distinguishes Identity, Sync, Storage, Search, Tools, Tasks, AI and Billing. |

---

## 3. Data classification

Every byte in the ecosystem belongs to exactly one class. A new data type must be classified before it is added. "Put it in AppData and sync the folder" is prohibited.

| Class | Examples | User asset? | Default cloud treatment |
|---|---|---|---|
| **Canonical User Data** | ArcNotes Document, ArcSlate Project, ArcScope Project, ArcChat Conversation | Yes | Syncable |
| **Managed Asset** | Imported images, video, audio, attachments, uploaded telemetry | Yes | By policy |
| **External Reference** | A video on the user's own disk | Yes, but ArcForges does not own it | **Never uploaded by default** |
| **Derived Data** | Thumbnail, waveform, embedding, search index, preview, transcode cache | No | Rebuildable; not synced as user data |
| **Device-local State** | Window position, GPU configuration, device paths, local caches, recent folders | No | Never synced |
| **Secret** | Device/login credentials, connector tokens, operator provider keys | Sensitive | Dedicated credential storage; never ordinary sync data |
| **Ephemeral Data** | Temp files, agent scratch, logs, render temp, task working directories | No | Never synced |
| **Operational Data** | Sync cursor, job state | System | Cloud-owned |
| **Audit / Commercial** | Billing records, security audit | System | Independently retained, separate retention |

[I-181](01-normative-glossary-and-invariants.md#rule-i-181): **User Data ≠ Asset ≠ Cache ≠ Search Index ≠ Secret.**

### 3.1 Authority boundaries

| System | Responsible for | Never responsible for |
|---|---|---|
| Professional product | The **business semantics** of its data (what a Document, Session or Timeline means) | Replication mechanics |
| Sync subsystem | Replication, revisions, conflicts, device state | Understanding how to merge a video timeline |
| Object storage | Blobs | Being the authoritative record of "what the current version is" |
| Search | A derived projection | Any authority over user data |

**The user's current data state is never inferred by enumerating the object store.** The object store is a blob store, not the domain database.

---

### 3.2 Cloud acknowledgement and native pending work

For Notes/Chat, Cloud product modules own acknowledged revisions. Native writes commit durably to an owner-scoped pending journal and become authoritative Cloud versions only after revision validation and acknowledgement. The UI distinguishes local durability from Cloud sync success. Pending edits cannot be evicted as cache, reassigned on account switch, or overwritten by a newer Cloud snapshot. Scope/Slate local capture/media authority and explicit upload choices remain unchanged. No permanent local-only notebook mode is required.

## 4. Sync Scope

Sync is never "the app directory is uploaded". The unit of participation is a **Sync Scope**.

| # | Requirement |
|---|---|
| <a id="rule-sy-01"></a>SY-01 | A sync scope declares owner realm/workspace, enrolled resources, local hydration/large-asset policy and conflict semantics. No encryption mode or collaboration profile is required. |
| <a id="rule-sy-02"></a>SY-02 | **Sync Scope ≠ ArcChat Project.** An ArcChat Project is agent context/work topic; a Sync Scope is which data participates in cloud replication. One ArcChat Project may reference three objects with three different sync states. |
| SY-03 | Per-product default sync policy: see §4.1. Defaults are conservative for large data. |
| SY-04 | Expose Synced, Syncing, Offline, PendingChanges, Conflict, StorageFull and Error with last Cloud acknowledgement, pending transfers and next action. LocalOnly applies to unuploaded capture/media resources, not a separate notebook or Agent mode. |
| <a id="rule-sy-05"></a>SY-05 | Pausing sync/hydration preserves pending edits. Evicting acknowledged cache requires an explicit local-space action and cannot delete Cloud data. Leaving a realm or deleting Cloud content is a separate confirmed operation. |

### 4.1 Per-product default sync policy

| Product | Synced by default | Not synced | User-selectable escalation |
|---|---|---|---|
| **ArcChat** | Conversations, Projects, task records, artifact references, agent profiles, user skills, automation definitions, selected preferences | Device-local paths, transient task working data, logs, device secrets | — |
| **ArcNotes** | Documents, Notebooks, metadata, managed attachments | External-reference targets | — |
| **ArcScope** | Projects, session metadata, annotations, analyses, reports, configurations | **Raw capture — local only by default** | Per-session "upload raw data" |
| **ArcSlate** | **Project only** by default: timeline, project metadata, editing decisions, text/subtitles, small assets | Managed originals, proxies | `Project + Managed Proxies` → `Project + Selected Originals` → `Full Managed Media` |

ArcSlate is never a single Sync On/Off toggle ([I-487](01-normative-glossary-and-invariants.md#rule-i-487): **Project Sync ≠ original media upload**).

### 4.2 Object identity

| # | Requirement |
|---|---|
| <a id="rule-sy-10"></a>SY-10 | Every syncable object is identified by `Workspace + App + ObjectId`. **A file path is never an identity** ([I-195](01-normative-glossary-and-invariants.md#rule-i-195)), and **a filename is never an identity**. |
| <a id="rule-sy-11"></a>SY-11 | Renaming a file is a rename, not "delete old + create unrelated new". Breaking this destroys version history, deep links, artifact references and cross-product references. |
| <a id="rule-sy-12"></a>SY-12 | A cross-product reference stores the target `ObjectId`, never a local path. Deep links are `arcforges://<product>/<kind>/<id>`, resolved to a local location on each device. |

### 4.3 Revisions

| # | Requirement |
|---|---|
| <a id="rule-sy-20"></a>SY-20 | Every user object carries a **Revision** chain. A Revision records at minimum: `RevisionId`, `ObjectId`, `ParentRevision`, created time, `Actor`, `Device`, `AppVersion`, `SchemaVersion`. |
| <a id="rule-sy-21"></a>SY-21 | An agent-produced Revision additionally records `TaskId`, `Capability` and the approval reference where relevant, so the user can see "Edited by ArcChat Agent" with a traceable cause. |
| <a id="rule-sy-22"></a>SY-22 | **Historical Revisions are immutable.** A change produces a new Revision; it never rewrites an existing one. This is what makes sync, history, backup, agent undo and audit tractable. |
| <a id="rule-sy-23"></a>SY-23 | A checkpoint Revision is created **before** any high-risk batch agent modification (e.g. "reorganise my entire notebook") and before any breaking data migration. Recovery must not depend on the agent remembering what it did. |
| <a id="rule-sy-24"></a>SY-24 | The Revision system carries product-distinguishable kinds — autosave revision, user version, agent checkpoint, migration checkpoint — sharing one underlying mechanism with distinct product semantics ([I-201](01-normative-glossary-and-invariants.md#rule-i-201)–[I-204](01-normative-glossary-and-invariants.md#rule-i-204)). |

### 4.4 Change propagation

| # | Requirement |
|---|---|
| <a id="rule-sy-30"></a>SY-30 | Sync is **change-based**, never a full scan. A `SyncCursor` plus a server change feed drives convergence. Enumerating a million cloud objects at startup is prohibited. |
| SY-31 | Every change is idempotent, carrying `ChangeId`, `ObjectId` and `RevisionId`. A change received twice applies once. |
| <a id="rule-sy-32"></a>SY-32 | The client holds a **durable Sync Outbox**. A local edit commits to local durable storage first, then enqueues an outbox entry. A crash immediately after save must leave the outbox intact for the next launch. An in-memory task is not an outbox. |
| SY-33 | The server holds an **Inbox / idempotency** record. Five retries of the same client change produce exactly one Revision. |
| <a id="rule-sy-34"></a>SY-34 | **Local save can never fail because Cloud failed.** The path is `local edit → local durable commit → sync outbox → cloud when available`. |
| <a id="rule-sy-35"></a>SY-35 | Sync priority separates metadata from large blobs: project metadata, notes and conversations first; large media afterwards. A second machine must show the user's projects within seconds, not after a 40 GB upload. |
| <a id="rule-sy-36"></a>SY-36 | Users control network policy: sync over metered connections, upload large assets on Wi-Fi only, bandwidth limit, pause media sync. |
| SY-37 | Sync progress is expressed in human terms — files in flight, per-file bytes, queue depth, estimate — with Pause, Resume and Prioritize. A bare percentage is insufficient for ArcSlate-scale data. |
| <a id="rule-sy-38"></a>SY-38 | **Cloud search indexing must never block sync success.** Canonical data syncs, sync reports success, indexing proceeds asynchronously. An index outage degrades search, never sync. |

### 4.5 Conflicts

| # | Requirement |
|---|---|
| <a id="rule-cf-01"></a>CF-01 | **There is no single global conflict algorithm.** Each object type declares a `ConflictPolicy` from: `Append`, `Merge`, `RevisionCompare`, `ConflictBranch`, `Immutable`. |
| <a id="rule-cf-02"></a>CF-02 | **Silent last-write-wins on user-created content is prohibited.** Where safe automatic merge is impossible, the original and both device versions are all retained. |
| <a id="rule-cf-03"></a>CF-03 | Conflict presentation names what happened: which device, which time, with actions to open either version, keep both, or resolve. `Sync error 409` is not acceptable user-facing behaviour. |
| <a id="rule-cf-04"></a>CF-04 | No CRDT, Yjs, awareness, shared cursors or multi-user editing. Multi-device sync uses stable IDs, explicit base revisions, outbox/inbox, change feed, tombstones and durable conflicts; no silent last-write-wins. |

### 4.6 Deletion

| # | Requirement |
|---|---|
| <a id="rule-de-01"></a>DE-01 | Deletion produces a **Tombstone** (`ObjectId`, deleted-at, delete revision), never a bare server-side row removal. Without tombstones an offline device resurrects deleted objects on reconnect. |
| DE-02 | Trash is built on tombstones. During the recovery window the object is restorable, its blobs are retained, its history is retained, and it still counts toward storage. |
| <a id="rule-de-03"></a>DE-03 | **Restore restores the original `ObjectId`.** Allocating a new id would sever ArcChat project references, deep links and artifact links. Restore is a new Revision that revokes the tombstone state. |
| <a id="rule-de-04"></a>DE-04 | **Permanent delete is a propagation process**, not a row delete. It must clear: canonical metadata, blob references, now-unused blobs, version references, search documents, vector index entries, previews and caches, future share/access state, and schedule backup expiry. |
| <a id="rule-de-05"></a>DE-05 | **Deletion propagation is tracked to completion.** A permanently deleted document must not remain discoverable through semantic search ([I-165](01-normative-glossary-and-invariants.md#rule-i-165)). |
| <a id="rule-de-06"></a>DE-06 | The deletion promise is stated honestly: deleted data becomes **immediately inaccessible from the online system** and disappears from disaster backups when the backup retention window elapses. A claim that pressing Delete instantly erases every historical backup copy must not be made ([I-220](01-normative-glossary-and-invariants.md#rule-i-220)). |

---

## 5. Assets and blobs

### 5.1 Managed Asset versus External Reference

| # | Requirement |
|---|---|
| AS-01 | **Managed Asset** — the user chose to import content into ArcForges. ArcForges owns its `AssetId`, lifecycle, hash, sync, relocation and backup. |
| <a id="rule-as-02"></a>AS-02 | **External Reference** — the user chose to leave the file where it is. ArcForges stores an `ExternalAssetReference` and **does not own the file**. |
| <a id="rule-as-03"></a>AS-03 | **External assets are never silently copied to Cloud.** Enabling sync on a project must never begin uploading a 200 GB external library. The user is given an explicit choice: keep local only / make managed / upload original. This is a privacy boundary as well as a bandwidth one. |
| <a id="rule-as-04"></a>AS-04 | An unavailable external asset yields **Missing / Unavailable Asset**, and the project still opens. Recovery affordances: Locate file, Relink, Find by content, Use proxy. "Project corrupted" is not acceptable. |
| <a id="rule-as-05"></a>AS-05 | Relink verifies content, not filenames: `AssetId`, expected size, content hash and metadata. A same-named file with different content must be reported as different. |
| <a id="rule-as-06"></a>AS-06 | **ArcForges must never delete a user's original local source file to save space.** Only a **Managed** asset may be offloaded, and only after an explicit "free up local space" action, leaving a cloud-backed placeholder that hydrates on demand. External references can never be offloaded. |
| <a id="rule-as-07"></a>AS-07 | Assets carry a **Local Availability Policy**: `Always keep on this device`, `Available offline`, `Download on demand`, `Cloud only`. |
| <a id="rule-as-08"></a>AS-08 | New-device bootstrap fetches workspace metadata, object catalogue, project metadata and small assets first. Large media and raw telemetry hydrate on demand. A full download of the whole quota on sign-in is prohibited. |

### 5.2 Immutable blobs

| # | Requirement |
|---|---|
| <a id="rule-bl-01"></a>BL-01 | Managed blobs use an **immutable** model: a blob carries `BlobId`, content hash and length, and is never overwritten in place. Editing produces a new blob; the project Revision changes which blob it references. |
| BL-02 | This makes conflict a **domain-revision** question rather than an object-store last-writer-wins race, and it makes backup incremental by construction. |
| <a id="rule-bl-03"></a>BL-03 | **Blob keys must not expose user filenames.** The key is internal and unguessable; the filename lives in domain metadata. Renaming therefore does not move a blob, special characters cause no key problems, and URLs leak no titles. |
| <a id="rule-bl-04"></a>BL-04 | Integrity uses a standard cross-platform hash — **SHA-256** as the recorded integrity hash. Faster internal fingerprints may exist, but the published integrity check uses the standard hash. |
| BL-05 | **A multipart ETag is never a content hash** ([I-218](01-normative-glossary-and-invariants.md#rule-i-218)). The real checksum is computed and stored by ArcForges. |
| <a id="rule-bl-06"></a>BL-06 | Large assets use resumable multipart upload. A failure at 99 % re-sends only the failed parts, never the whole object. |
| <a id="rule-bl-07"></a>BL-07 | **The client never receives a permanent object-storage credential.** The flow is `client requests upload authorization → Cloud issues a short-lived, object-scoped, operation-scoped authorization → client uploads`. Presigned authorizations are bearer capabilities: short TTL, one object, limited operations. |
| <a id="rule-bl-08"></a>BL-08 | An **Upload Session** has an explicit lifecycle: `Staged → Verified → Committed`, or `Abandoned`. A Revision may reference a blob **only after** checksum and integrity verification succeed. This is what prevents orphan blobs and broken references from half-successful uploads. |
| <a id="rule-bl-09"></a>BL-09 | Staged blobs with no committing Revision are garbage-collected after a bounded window. |
| <a id="rule-bl-10"></a>BL-10 | Deduplication is **workspace-scoped only**. Cross-user global deduplication is prohibited: it creates privacy side channels, permission complexity, deletion difficulty and tenant-isolation problems. Provider-internal physical deduplication is a separate matter. |
| <a id="rule-bl-11"></a>BL-11 | Downloads verify expected hash and length before content reaches the application. A mismatch is reported as `Corrupted`; a bad file is never handed to the product. |
| <a id="rule-bl-12"></a>BL-12 | A background **integrity audit** samples metadata/checksum consistency, random objects and backup copies. A primary hash mismatch triggers recovery from backup. |

### 5.3 Storage accounting

| # | Requirement |
|---|---|
| ST-01 | Quota counts **canonical synced user data, attachments, managed originals, explicitly stored proxies, trashed items still recoverable, and historical user blobs that remain restorable**. |
| ST-02 | Quota does **not** count ArcForges-generated derived data: vector index, embeddings, search index, internal DB metadata, thumbnails, operational logs, temporary agent files. A user who uploaded 40 GB must not see 47 GB. |
| ST-03 | The same managed blob reused across three projects in one workspace counts **once**. |
| ST-04 | Explicit user-requested cloud proxies count toward quota; pure implementation caches do not. |
| ST-05 | Storage is presented by product plus versions/trash, and is explainable: a per-product breakdown plus a "Manage storage" affordance. |
| <a id="rule-st-06"></a>ST-06 | **Storage full never destroys local work.** Local save, local edit and reads of existing cloud data all continue; only cloud upload and sync writes pause. The message is explicit: "Cloud storage is full. Your local work is safe." |
| ST-07 | **Quota downgrade never deletes data.** A workspace over quota enters `Over Quota`, which limits new cloud writes only. Automatic deletion to fit a smaller quota is prohibited. |

---

## 6. Standard Cloud protection

| # | Requirement |
|---|---|
| PR-01 | V1 ships **Standard Protected Cloud**: TLS in transit, encryption at rest, workspace isolation, strict service authorization, secret separation. This is what makes cloud search, semantic indexing, cloud agent, managed AI context and web access possible. |
| <a id="rule-pr-02"></a>PR-02 | Retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006): no E2EE mode, profile field, key-sharing protocol or deferred delivery requirement. |
| <a id="rule-pr-03"></a>PR-03 | Custom local encrypted stores and encrypted portable exports are excluded. Login/device secret protection and encrypted operator backups remain infrastructure requirements; no zero-knowledge claim. |
| <a id="rule-pr-04"></a>PR-04 | No claim of "zero-knowledge cloud" may be made while `Standard` is the operating mode. |

---

## 7. Sync and AI are independent

[I-182](01-normative-glossary-and-invariants.md#rule-i-182): **Sync ≠ AI upload.**

| # | Requirement |
|---|---|
| AI-01 | Sending a local file to managed AI as explicit context does **not** enrol it in cloud sync. |
| AI-02 | Enabling sync for a scope does **not** make its contents available to AI retrieval. Eligibility for AI is a separate, explicit decision (see [`06-knowledge-search-and-retrieval.md`](06-knowledge-search-and-retrieval.md)). |
| AI-03 | Cloud search must respect product data policy: unsynced ArcScope raw telemetry is not searchable in the cloud, and must never be uploaded in the background to make search work. |

---

## 8. Cloud search

| # | Requirement |
|---|---|
| CS-01 | Cloud search spans ArcChat conversations, ArcNotes content, ArcScope reports and metadata, ArcSlate project metadata, and artifacts. Results carry title, snippet, source product, object type, modified time and a deep link. |
| CS-02 | Three levels exist and are distinguished: **metadata search**, **full-text search**, **semantic search** ([I-145](01-normative-glossary-and-invariants.md#rule-i-145)). |
| CS-03 | **The search index is never data authority** ([I-135](01-normative-glossary-and-invariants.md#rule-i-135)). The chain is `canonical object → search document → full-text index → vector index`, all derived, all deletable and rebuildable at any time. This is what makes changing the vector backend possible later. |
| CS-04 | The ArcForges search API must not expose any vendor's vector-database concepts. |
| <a id="rule-cs-05"></a>CS-05 | Cloud search is restricted to the authenticated owner workspace and authorised resources. Another realm/workspace is never included implicitly. |
| CS-06 | Deleting a source object removes its search document, vector entries and derived previews ([DE-04](#rule-de-04), [DE-05](#rule-de-05)). |

---

## 9. Remote and cloud execution

Three tool-location shapes under one Cloud agent runtime, always visible to the user ([I-023](01-normative-glossary-and-invariants.md#rule-i-023), [I-105](01-normative-glossary-and-invariants.md#rule-i-105)):

| Mode | Where it runs | Desktop required? |
|---|---|---|
| **Desktop tool execution** | Authorised native product job, requested by the Cloud Harness | Yes, online for remote control |
| **Cloud Execution** | ArcForges Cloud | No — the machine may be off |
| **Mixed tool targets** | One Cloud Run observes Cloud and desktop product jobs | For desktop tools only |

| # | Requirement |
|---|---|
| RX-01 | Task details distinguish Cloud agent orchestration from each tool target, including a named desktop/product. A desktop target never denotes a desktop model loop. |
| <a id="rule-rx-02"></a>RX-02 | A task targeted at an offline device enters **`WaitingForDevice`**, not `Failed`. The user may wait, run when online, cancel, or choose another device. |
| RX-03 | Remote desktop access uses a **desktop-initiated outbound authenticated connection**. Opening an inbound public port on a user machine is prohibited. |
| RX-04 | Remote access defaults to off and requires explicit enablement per device, with per-capability grants (see [`02-identity-account-and-workspace.md`](02-identity-account-and-workspace.md) §5). |
| RX-05 | **Device Presence** is an ephemeral cloud capability showing device online state, app version, remote-enabled flag and per-product readiness. It is not durable data and is never trust ([I-250](01-normative-glossary-and-invariants.md#rule-i-250)). |
| RX-06 | **Cloud task runtime is not a general-purpose VPS.** It carries a maximum runtime, CPU and memory limits, disk limits, network policy, AI budget and output limits. |
| <a id="rule-rx-07"></a>RX-07 | Trusted Cloud tools run as bounded internal jobs in the single Native AOT host, with per-job workspace scope, cancellation and temporary resources. No arbitrary user code or per-task container/TaskRunner deployment is required. Durable task/usage records survive process failure. |
| RX-08 | Secrets are injected per capability, never as a whole vault. A task needing one connector receives only that connector's secret handle. |
| RX-09 | **Cloud execution does not mean unlimited permission.** Every risk-tiered capability check still applies, and R4-class operations still require local confirmation on a trusted device. |
| <a id="rule-rx-10"></a>RX-10 | The server re-authorises independently. It never trusts that the desktop already checked. Session, workspace, entitlement, permission, device trust and capability are all re-validated server-side. **The client is never the security authority.** |

---

## 10. Automation in the cloud

| # | Requirement |
|---|---|
| AU-01 | Every AI automation is Cloud-scheduled. Its tools may target Cloud or an explicitly authorised device/product; no local automation Harness. |
| AU-02 | Every Automation declares a **Missed Run Policy**: `Run when device returns`, `Skip missed run`, or `Ask me`. Silent guessing is prohibited. |
| AU-03 | Every Automation declares a **Concurrency Policy**: `Skip`, `Queue`, `Replace`, or `Allow concurrent`. |
| AU-04 | Every Automation is bound to an **AI Budget**: max credits per run, per day and per month. On reaching the budget the automation **pauses and asks**; it never continues spending. |
| AU-05 | **Automation ≠ Task** ([I-100](01-normative-glossary-and-invariants.md#rule-i-100)); **Automation Occurrence ≠ Task Retry** ([I-101](01-normative-glossary-and-invariants.md#rule-i-101)); disabling an Automation does not cancel a task already running ([I-103](01-normative-glossary-and-invariants.md#rule-i-103)). |

---

## 11. Notifications

| # | Requirement |
|---|---|
| NT-01 | A Cloud Notification Center is a first-class product surface, covering: task completed, task failed, approval needed, desktop offline, automation missed, storage near quota, storage full, AI credits low, subscription issue, security event. |
| NT-02 | Three channels with distinct purposes: **in-app** (desktop, web, mobile), **push** (ArcChat Mobile), **email** (security, billing, critical account issues only). Email is not sent for ordinary task completion. |
| NT-03 | **Lock-screen and preview notifications must not leak sensitive content by default.** The default text is generic ("An ArcChat task needs your attention"); full content requires an explicit "show notification previews" opt-in. |
| <a id="rule-nt-04"></a>NT-04 | **Push Notification ≠ Durable Attention State** ([I-448](01-normative-glossary-and-invariants.md#rule-i-448) family). Missing a push never loses the underlying pending approval or task state. |

---

## 12. Subscription lifecycle for cloud data

| Phase | Cloud behaviour | Local behaviour |
|---|---|---|
| **Active** | Full cloud capability | Unaffected |
| **Grace** (payment failure window) | Data continuity follows published grace policy; no new AI, embedding, paid-tool or simulation dispatch after PaidThrough | Cached edits and native jobs remain available; no local AI |
| **Cloud Retention** (after entitlement ends) | **Read / export / download only.** New upload, new sync write, remote agent, new simulations and cloud tasks are blocked | Unaffected |
| **After retention** | Notified Cloud purge follows the deletion/retention policy | Pending work and independent native files are preserved; acknowledged cache follows recorded deletions and cannot resurrect purged objects |

| # | Requirement |
|---|---|
| SB-01 | Re-subscribing during the retention window reactivates cloud immediately, with no re-upload of everything. |
| <a id="rule-sb-02"></a>SB-02 | **Export must remain available throughout retention.** "Pay first to get your data back" is prohibited. |
| SB-03 | **Cloud data deletion is a separate operation from account deletion.** A user may delete cloud data while retaining the account, AI credits and purchase history. |

---

## 13. Export and import

| # | Requirement |
|---|---|
| EX-01 | V1 offers the product-specific exports in [data §12](13-data-formats-and-portability.md): Notes Markdown/attachments/metadata, Chat history/task summaries, Scope data/reports and Slate project/OTIO/media as applicable. Cloud exports only data it actually holds. |
| <a id="rule-ex-02"></a>EX-02 | Workspace export coordinates the supported per-product Cloud exports with one inventory/checksum/fidelity manifest. It declares included revisions, attachment availability and omitted device-only/pending content. It is not a universal native archive or a promise to restore execution, credentials or billing state. |
| <a id="rule-ex-03"></a>EX-03 | The export manifest format is **documented and public**, covering manifest, schema version, objects, references, assets and checksums. A convenience container extension may exist; an undocumented opaque archive is prohibited, because the product's premise is that data is not locked in. |
| <a id="rule-ex-04"></a>EX-04 | Device-only/external assets are listed by availability and safe provenance, not silently fetched or bundled. Including permitted missing assets requires a separately authorized transfer; a user library is never copied automatically. |
| <a id="rule-ex-05"></a>EX-05 | **Import treats the package as untrusted input.** It must not trust internal absolute paths, must reject `../` path traversal, must bound decompression against archive bombs, must never execute contained scripts, and must never load contained binaries. |
| <a id="rule-ex-06"></a>EX-06 | Cloud-stored assets are never treated as executable content. Web preview uses sandboxing, safe content disposition and content-type validation. An agent runtime never executes a file merely because it is present in a workspace. |

---

### 13.1 Cloud simulator data contract

The Scope module must deliver [SIM-01](products/arcscope.md#rule-sim-01)–[SIM-20](products/arcscope.md#rule-sim-20) in this same deployment: admitted definitions, immutable versions, finite runs, fenced leases, durable checkpoints, verifiable manifests and native download/replay. Operator resource policy and service eligibility apply independently of model usage. Simulator data is synthetic and never represented as physical acquisition evidence.

## 14. Backup and disaster recovery

Backup protects ArcForges' own systems. It is not a user feature and is not sync ([I-180](01-normative-glossary-and-invariants.md#rule-i-180)). **Sync propagates mistakes efficiently**; what saves a user is version history, trash and backup.

### 14.1 Layers

```
Layer 1   Local durable state
Layer 2   Cloud sync revisions
Layer 3   Version history + trash window
Layer 4   Primary immutable backup protection (object-lock on the primary provider)
Layer 5   Independent cross-provider disaster backup (object lock at the second provider)
```

No layer may be described as making another unnecessary.

| # | Requirement |
|---|---|
| BK-01 | The metadata database supports **point-in-time recovery** via continuous WAL archiving plus base backups. A nightly dump alone is insufficient. |
| BK-02 | **High durability is not backup** ([I-219](01-normative-glossary-and-invariants.md#rule-i-219)). Provider durability does not protect against a mistaken deletion script, stolen credentials, a wrong lifecycle rule, operator error or an account-level disaster. |
| BK-03 | The primary object store uses an immutability control (bucket/object lock) on backup snapshots and backup prefixes as the first protection layer. |
| <a id="rule-bk-04"></a>BK-04 | **Disaster backup is replicated to an independent provider in a different fault domain.** Primary and only-backup must not share a provider or account. The second copy uses object lock with a retention period. |
| <a id="rule-bk-05"></a>BK-05 | Because blobs are immutable, backup is naturally incremental: each new blob is copied once and never re-copied. |
| <a id="rule-bk-06"></a>BK-06 | **A backup exists only once a restore has been proven.** Required verification cadence: automated daily sample metadata restore, sample blob restore and checksum verification; a monthly small-scale restore drill; a quarterly full disaster-recovery exercise into a fresh environment, restoring the database, restoring/accessing the object backup, and verifying a workspace end to end. |
| <a id="rule-bk-07"></a>BK-07 | A **Backup Health Dashboard** is mandatory, showing last database backup, PITR archive lag, object backup lag, objects awaiting backup, checksum failures, last restore test and last full DR drill. |
| <a id="rule-bk-08"></a>BK-08 | **Backup never blocks a user save.** Primary commit succeeds and the user proceeds; secondary replication is asynchronous. Backup lag exceeding its objective raises an operational alert, never a user-facing failure. |
| <a id="rule-bk-09"></a>BK-09 | **User content retention ≠ commercial record retention.** Billing, payment, refund and security records have their own, longer retention driven by tax, anti-fraud and legal requirements. A single `RetentionDays` value must not govern all data. |

### 14.2 Internal engineering objectives

These are **internal engineering objectives, not an external SLA** ([I-403](01-normative-glossary-and-invariants.md#rule-i-403)). Converting any of them into a public commitment requires a completed recovery drill and explicit approval.

| Objective | Target |
|---|---|
| Metadata RPO | ≤ 5 minutes |
| Blob backup RPO | ≤ 1 hour (alert when lag > 4 hours) |
| Critical service RTO | ≤ 4 hours |
| Full blob recovery / provider switch | ≤ 24 hours |
| Backup retention | ≈ 35 days (policy parameter, §1) |

No public claim of seconds-scale cross-cloud failover may be made.

---

## 15. Data health

A background **Data Health** service is an operational requirement, not a user feature. It continuously checks for: metadata referencing a missing blob, a blob with no metadata reference, a Revision with a missing parent, a search document with a missing source, a tombstoned object still searchable, and a primary blob with no backup copy.

Tracked indicators: `BrokenReferences`, `OrphanBlobs`, `ConflictRate`, `SyncBacklog`, `ChecksumFailures`, `BackupLag`, `RestoreFailures`, `DeletionBacklog`, `IndexDrift`.

---

## 16. Schema versioning and mixed-version safety

| # | Requirement |
|---|---|
| SV-01 | Every syncable domain payload carries `ObjectType` and `SchemaVersion`. Products release independently, so mixed versions across a user's devices are the normal case, not an edge case. |
| <a id="rule-sv-02"></a>SV-02 | **An older client must never silently destroy newer data.** Opening and saving a `v4` object from a `v3`-only client must not drop the `v4` fields. |
| <a id="rule-sv-03"></a>SV-03 | Compatibility negotiation expresses at least `Readable`, `Writable`, `RequiresUpgrade` ([I-385](01-normative-glossary-and-invariants.md#rule-i-385): **Read Compatibility ≠ Write Compatibility**). |
| <a id="rule-sv-04"></a>SV-04 | A breaking migration is preceded by a local recovery snapshot **and** a cloud revision checkpoint, and provides a **Migration Recovery** path ([I-207](01-normative-glossary-and-invariants.md#rule-i-207)). |
| <a id="rule-sv-05"></a>SV-05 | **Application update and data migration are not one transaction.** The sequence is `installer update → app starts → data compatibility check → migration`, with migration recoverable independently of the installer. The updater is never responsible for business data migration. |

---

## 17. Self-hosting

| # | Requirement |
|---|---|
| SH-01 | The same self-hosted Cloud provides identity, single-owner workspaces, sync, storage, search, bounded tasks/automation, simulator and operator-funded remote-provider AI. |
| SH-02 | The deployment operator supplies provider credentials and a validated realm policy. End users have no BYOK interface. Payment collection may be disabled for that realm; usage, budget and authorisation remain real. No local models or official entitlement bypass. |
| <a id="rule-sh-03"></a>SH-03 | Self-host uses the same implementation, public contracts and data semantics. Public sample deployment policy is sufficient for testing with operator credentials; production private values are not a code dependency. |
| <a id="rule-sh-04"></a>SH-04 | Realms never share object-identity authority. An imported object may retain an **origin identity** for provenance, but the receiving realm mints its own realm-local identity and mapping. |
| <a id="rule-sh-05"></a>SH-05 | V1 realm portability uses the supported product export/import formats with disclosed fidelity and new destination identities. It does not migrate billing grants, live agent execution, device trust or secrets. Full-state realm cloning and live bidirectional official/self-host sync are excluded. |

---

## 18. Deliberate V1 exclusions

Outside current scope; no speculative implementation or schema reservations:

- Real-time multi-user collaborative editing (presence, cursors, OT/CRDT convergence)
- Public "anyone with the link" sharing
- Zero-knowledge E2EE, custom local encrypted stores and encrypted portable exports
- Full ArcNotes or ArcSlate web editors
- Cloud video rendering farm
- Unlimited general-purpose cloud compute
- Complex team collaboration, enterprise SSO, SCIM
- Cross-realm live sync
- Arbitrary third-party cloud plug-ins
- Multi-region active-active with user region selection

---

## 19. Domain concepts

The cloud and data domain must be able to express:

```
CloudWorkspace · OwnerUserId · DataRegion
SyncScope · SyncCursor · SyncChange · SyncOutbox · SyncInbox · SyncConflict · ConflictBranch · Tombstone
UserDataObject · ObjectType · ObjectIdentity · ObjectRevision · RevisionParent · RevisionActor
CloudObject · CloudObjectRevision · CloudBlob · ObjectReference
ManagedAsset · ExternalAssetReference · DerivedAsset · AssetAvailability · AssetSyncPolicy
Blob · BlobIntegrity · BlobReference · UploadSession · MultipartUpload · StagedBlob · OrphanBlob
StorageQuota · StorageUsage
TrashItem · DeletedItem · RecoveryRevision · RecoveryPoint
SearchDocument · SearchIndexState
DevicePresence · DeviceConnection · RemoteSession
CloudTask · TaskExecution · ExecutionTarget · CloudArtifact
SimulationDefinition · ScenarioVersion · SimulationRun · SimulationSegment · SimulationEvent
Automation · AutomationRun · MissedRunPolicy · ConcurrencyPolicy · Approval
CloudSecret · SecretReference · Notification
ExportManifest · ExportJob · ImportSession · DeletionJob · DeletionPropagation · RetentionPolicy
BackupSnapshot · BackupCopy · BackupRetention · BackupVerification · RestoreJob
DataSchemaVersion · CompatibilityPolicy · MigrationCheckpoint · DataHealthCheck
```

Not one database table per name; the semantics must exist.

---

## 20. Acceptance scenarios

Every scenario below must pass before the corresponding capability is released.

### Local durability
Force-kill immediately after save · OS crash · disk full · local database corruption · interrupted data migration · application downgrade.

### Sync
One device · two devices · three devices · long-offline return · double edit of one object · simultaneous rename · simultaneous edit-and-delete · deletion reaching a device that returns online later · duplicated change · out-of-order change · sync API timeout · server retry.

### Assets
1 KB · 100 MB · 20 GB · multipart interrupt · resume · hash mismatch · missing external reference · relink · one asset referenced by multiple projects · managed → cloud-only offload · **external assets are never uploaded automatically**.

### ArcSlate
Project-only sync · proxy sync · selected originals · one original reused by several projects · **timeline edits never re-upload the original**.

### ArcScope
Hardware telemetry local-only · explicit upload · resumed session upload · session deletion · Cloud scenario/seed/profile replay · immutable segment hashes · pause/resume/fenced takeover · native simulator adapter · SIM-20.

### History and deletion
Version restore · delete · restore from trash · retention purge · **tombstone prevents an old device resurrecting an object** · search entry disappears after deletion · vector entry disappears after deletion.

### Quota
Approaching quota · storage full · local work continues · over-quota downgrade · dropping below quota restores sync automatically.

### Backup
Database PITR restore · missing primary blob · restore from secondary backup · backup-credential compromise simulation · erroneous primary deletion simulation · backup object lock enforced · random checksum restore · full DR drill.

### Export and import
Workspace export with an explicit per-product inventory and loss report · supported Markdown/OTIO/Scope formats imported into a fresh account or self-host realm · no assumed live-task/credit/secret migration · device-only data reported unavailable · malformed inputs, traversal and archive bombs rejected.

### Remote and tasks
Desktop online · desktop offline → `WaitingForDevice` · mobile steering · device revoke · remote disabled · R4 requires local confirmation · machine fully powered off and a cloud-only task still completes · hybrid task waits for the desktop · cloud task timeout · budget exhausted · provider 429 and fallback · task interrupted and recovered.

### Automation
Cloud schedule with Cloud or desktop tool targets · missed run per policy · concurrent run per policy · AI budget enforcement.

### Subscription
Active · grace · retention · re-subscribe · retention expiry · local files still present · export during retention.

### Security
Cross-workspace object-id probe · cross-workspace blob-id probe · expired presigned URL · stolen upload URL · revoked device · secret accidentally submitted as an asset · malicious HTML or document preview · task attempting an unauthorised capability.

---

## 21. Traceability

| Current document | Relationship |
|---|---|
| [Sync, Conflict and Backup Architecture](../architecture/07-sync-conflict-and-backup.md) | Implements sync, conflict, blob, retention and recovery obligations |
| [Cross-System Lifecycles](../architecture/20-cross-system-lifecycles.md) | Composes subscription, deletion and resource lifecycles |
| [Cloud Data Model](../architecture/data-model/01-cloud-data-model.md) | Defines the authoritative Cloud records |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Cloud is an ASP.NET Core Native AOT modular monolith |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Cloud never touches local IPC; durable `ToolRequest`/`ToolResult` model |
| **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** | Every allowance in §1 is versioned commercial policy, not a frozen figure |
