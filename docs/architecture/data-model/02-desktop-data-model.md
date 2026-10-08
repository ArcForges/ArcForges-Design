# Desktop Local Data Model

[P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012) current implementation authorities: [Canonical local assistant history, complete schema and mode lifecycle](05-application-history.md).

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Data model
> Governing authority: [`00-data-model-overview.md`](00-data-model-overview.md), [`../06-data-persistence-and-formats.md`](../06-data-persistence-and-formats.md)
> Companions: [`../04-desktop-application-architecture.md`](../04-desktop-application-architecture.md), [`../07-sync-conflict-and-backup.md`](../07-sync-conflict-and-backup.md)

Each desktop product owns its SQLite store. Cloud-mode assistant history holds acknowledged Cloud projections plus durable pending work; local-mode assistant history is canonical in its own app store under model 05. ArcScope retains local authority for native working content and jobs, with separately revisioned Cloud metadata replicas. The version domains are defined in [the authority map](00-data-model-overview.md#4-authority-map--where-the-authoritative-copy-lives).

**Store technology.** An embedded relational store with an AOT-safe access path ([CS-01](../06-data-persistence-and-formats.md#rule-cs-01)). Journaling is enabled only after per-platform and per-filesystem validation ([CS-04](../06-data-persistence-and-formats.md#rule-cs-04)), because network volumes, removable media and container filesystems each break different assumptions.

---

## 1. What every product store contains

Five table groups are identical in shape across ArcScope and the shared assistant. They are specified once here and referenced, not repeated.

### 1.1 `sys_meta`

| Field | Type | Notes |
|---|---|---|
| `key` | `text` | **PK** |
| `value` | `text NN` | |

Holds `storageSchemaVersion`, `nativeFormatVersion`, `installationId`, `lastCleanShutdownAt`, `lastRecoveryOutcome`. **`storageSchemaVersion` equals the highest applied migration** ([SE-06](00-data-model-overview.md#rule-se-06)).

### 1.2 `command_log`

The local half of [TX-01](00-data-model-overview.md#rule-tx-01)–[TX-06](00-data-model-overview.md#rule-tx-06).

| Field | Type | Notes |
|---|---|---|
| `command_id` | `id` | **PK** |
| `operation` | `text NN` | |
| `request_hash` | `text NN` | |
| `status` | `enum(inProgress, succeeded, failed) NN` | |
| `result_version` | `json?` | Typed result token: Cloud revision, ArcScope metadata local token, or native content revision |
| `result_payload` | `json?` | Original typed response, including generated references; retained for the duplicate window |
| `error_code` | `text?` | |
| `created_at`, `expires_at` | `instant NN` | |

- `IX (expires_at)`
- **Constraint** — written **in the same transaction as its effect**. This is what makes a retried local RPC call idempotent ([WP-14.03](../../planning/work-packages/14-hub-and-minimal-provider-slice.md#rule-wp-14.03)).

### 1.3 `journal`

| Field | Type | Notes |
|---|---|---|
| `journal_seq` | `bigint` | **PK**, monotonic |
| `aggregate_kind`, `aggregate_id` | `text NN`, `id NN` | |
| `source_version` | `json NN` | ArcScope metadata `(acked_rev, head_local_seq)` or native `content_rev`; discriminator fixes the version domain |
| `local_seq` | `bigint?` | Durable local edit identity for sync-eligible work; separate from store-wide journal order |
| `command_id` | `id NN` | |
| `payload` | `json NN` | Enough to replay |
| `committed_at` | `instant NN` | |

- `IX (aggregate_kind, aggregate_id, journal_seq)` — per-aggregate replay
- **Constraint** — the journal entry is durable **before** the commit is acknowledged ([WP-07.01](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.01)). This is the difference between crash-free and recoverable ([QI-08](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-08)).
- **Truncation** — safe under concurrent read, bounded by snapshot policy

### 1.3a Local edit identity, submission and acknowledgement

[CW-01](00-data-model-overview.md#rule-cw-01) of the data-model overview says a client never assigns an authoritative revision. What that leaves open — and what the previous formulation got wrong — is **exactly how much local work an acknowledgement covers**.

> **Corrected 2026-09-08.** The previous [RV-C5](#rule-rv-c5) reset `local_rev` to 0 whenever an acknowledgement arrived. Counterexample: edit **A** becomes durable and is submitted; while A is in flight, edit **B** becomes durable on the same aggregate; Cloud acknowledges A; `local_rev` resets to 0 although B is still pending; the eviction gate then reports the row as having no pending work and **B is discardable as cache**. A monotonic counter cannot express *which* work an acknowledgement covered, so it is replaced by a watermark over an ordered log.

#### The four identities

| Identity | Scope | Assigned by | Purpose |
|---|---|---|---|
| `local_seq` | Per aggregate, per device | The device, strictly increasing, **never reset** | Orders durable local edits and names exactly what a submission covered |
| `batch_id` | Per submission | The device, allocated once | The **idempotency identity** of a dispatched request ([TX-01](00-data-model-overview.md#rule-tx-01)) |
| `acked_rev` | Per aggregate | **Cloud** | The authoritative revision, and the `ExpectedRev` a submission is made against |
| `acked_local_seq` | Per aggregate, per device | Set from the acknowledgement | The **watermark**: local work at or below it is acknowledged |

An ArcScope metadata aggregate carries `acked_rev`, `acked_local_seq` and `head_local_seq`. `acked_rev` names its separately retained canonical Cloud shadow; the displayed body is that shadow plus unresolved local edits. An ArcScope native root additionally owns `content_rev`, which advances on every native domain commit and is what local jobs snapshot. Its sync metadata tracks the same submission identities separately. Chat uses durable draft/command identities and acknowledged Cloud projections; an unsent draft is not a synchronised aggregate revision.

| # | Rule |
|---|---|
| <a id="rule-rv-c1"></a>RV-C1 | **`acked_rev` is the only revision Cloud ever sees**, and it is the `ExpectedRev` on `sync.pushChange`. A device that sent a local counter would conflict on every second edit, because Cloud has never heard of it. |
| <a id="rule-rv-c2"></a>RV-C2 | **The pending predicate is `head_local_seq > acked_local_seq`**, not a counter being non-zero. In the counterexample, acknowledging A advances `acked_local_seq` to A's sequence while `head_local_seq` is B's — so the row is correctly still pending. |
| <a id="rule-rv-c3"></a>RV-C3 | **`local_seq` is never reset.** Resetting is what destroyed the ability to say which work an acknowledgement covered. It is a per-aggregate, per-device counter and its absolute value has no meaning outside that pair. |
| <a id="rule-rv-c4"></a>RV-C4 | **An acknowledgement advances the watermark to the highest `local_seq` the submitted batch contained — and no further.** The batch records its range when it is dispatched, so the covered set is a recorded fact, not a re-derivation at acknowledgement time. |
| <a id="rule-rv-c5"></a>RV-C5 | **A synced-metadata write through the local store takes and returns `(acked_rev, head_local_seq)`.** Every user edit or explicit conflict-resolution edit advances `head_local_seq`; applying a newer Cloud shadow advances `acked_rev` and rebases pending work atomically. A body cannot change while both token components stay unchanged. ArcScope's native RPC instead uses its native `content_rev`. |
| <a id="rule-rv-c6"></a>RV-C6 | **A conflict compares `acked_rev`, never a local sequence.** Two devices conflict when they submitted against the same `acked_rev`; how much local work each accumulated is irrelevant to that question. |

#### The submission log

`sync_outbox` becomes a log of **immutable submission batches** rather than a queue of mutable rows.

| Field | Type | Notes |
|---|---|---|
| `batch_id` | `id` | **PK**, and the idempotency identity sent to Cloud |
| `aggregate_kind`, `aggregate_id` | `text NN`, `id NN` | |
| `from_local_seq`, `to_local_seq` | `bigint NN` | **The exact local work this batch covers** — inclusive range |
| `expected_rev` | `rev NN` | The `acked_rev` the batch was built against |
| `payload_ref` | `id NN` | The **immutable** change content; never edited after dispatch |
| `state` | `enum(pending, dispatched, acknowledged, conflicted, superseded) NN` | A conflicted batch remains live until an explicit resolution replaces it |
| `supersedes_batch_id` | `id?` | FK to the previous immutable proposal for the same local range |
| `replacement_batch_id` | `id?` | Set atomically when this batch becomes superseded; no cycles or branching replacement chain |
| `resolution_local_seq` | `bigint?` | The appended user resolution record; never edits or renumbers original local events |
| `attempts`, `next_attempt_at`, `created_at` | `int NN`, `instant NN`, `instant NN` | Transport retry metadata only; retries retain batch identity and content |
| `dispatched_at`, `settled_at` | `instant?` | |

- `UQ (batch_id)`; `IX (aggregate_id, from_local_seq)`; `IX (state, dispatched_at)`
- **Constraint** — once `state = 'dispatched'`, `payload_ref`, `from_local_seq`, `to_local_seq` and `expected_rev` are **immutable**. A retry re-sends the identical request under the identical `batch_id` ([TX-03](00-data-model-overview.md#rule-tx-03))
- **Constraint** — live batches (`pending`, `dispatched`, `conflicted`) for one aggregate have non-overlapping, ascending `local_seq` ranges. A superseded historical proposal may overlap its single replacement. A transaction marks the old proposal superseded before admitting its replacement and verifies the replacement chain, covered event set and absence of any other live overlap. An acknowledged range is never submitted again as new work.

| # | Rule |
|---|---|
| <a id="rule-sb-l1"></a>SB-L1 | **An edit made while a batch is in flight does not join it.** It takes the next `local_seq` and waits for the next batch. **Editing is never blocked on network latency** — the user keeps typing, and the work accumulates behind the dispatched batch. |
| <a id="rule-sb-l2"></a>SB-L2 | **A dispatched batch is never mutated.** Appending to an in-flight request would change what a `batch_id` means, and a retry would then carry different content under the same idempotency key ([TX-03](00-data-model-overview.md#rule-tx-03)). |
| <a id="rule-sb-l3"></a>SB-L3 | **The next batch is built against the `acked_rev` the previous one produced.** Batches for one aggregate are therefore strictly sequential; there is at most one in flight per aggregate. |
| <a id="rule-sb-l4"></a>SB-L4 | **A duplicate or delayed acknowledgement is idempotent.** Advancing the watermark to a value at or below its current one is a no-op, so an acknowledgement arriving twice — or late, after a newer one — cannot move it backwards. |
| <a id="rule-sb-l5"></a>SB-L5 | **A lost response is resolved by re-sending the same `batch_id`.** Cloud returns the original result ([TX-04](00-data-model-overview.md#rule-tx-04)), including the revision it assigned, so the client learns the outcome without a second effect. |
| <a id="rule-sb-l6"></a>SB-L6 | **Restart resumes from the log.** A `dispatched` batch with no settlement is re-sent; a `pending` batch is built and sent. Nothing is inferred from in-memory state. |
| <a id="rule-sb-l7"></a>SB-L7 | **Conflict does not advance the acknowledgement watermark.** Stop dispatch for that aggregate, retain the old proposal and fetch the current Cloud shadow. Rebase unresolved local events in one local transaction. Automatic structural rebase cannot decide a semantic conflict. An explicit user resolution appends a new local event, supersedes the conflicted proposal and any dependent undispatched proposals, and creates one replacement covering the contiguous unresolved range through the resolution event against the new `acked_rev`. Original local event identities and bytes remain immutable. |
| <a id="rule-sb-l8"></a>SB-L8 | **Replacement has explicit lineage and dispositions.** Its receipt states which original edits were retained, transformed or explicitly discarded by the user. Even a keep-Cloud resolution sends an idempotent resolution command; its no-content-change receipt can acknowledge the resolved range without inventing a content revision. Advance `acked_local_seq` only over a contiguous accepted/resolved prefix. Superseded receipts never advance it independently. Historical discarded content is retained for the declared recovery window. |

#### Safe eviction

| # | Rule |
|---|---|
| <a id="rule-ev-l1"></a>EV-L1 | **A row is evictable only when `head_local_seq == acked_local_seq`** and no staged upload and no unreturned tool receipt references it. This is [PE-02](#rule-pe-02), restated against the watermark. |
| <a id="rule-ev-l2"></a>EV-L2 | **The corroborating invariant is that no batch for the aggregate is in a non-terminal state.** The two conditions must agree; a periodic check asserts they do, and a disagreement is a defect rather than a tie-break. |
| <a id="rule-ev-l3"></a>EV-L3 | **Cache pressure, sign-out, account switch and subscription restriction all run this same gate** ([PE-03](#rule-pe-03)). None has a shortcut, because each is a path by which unacknowledged work has historically been lost. |

### 1.4 Submission transport and acknowledgement application

The table in §1.3a is the **only** `sync_outbox` schema. `batch_id` is also the wire `CommandId`; there is no second `outbox_id`, second state vocabulary or client-assigned Cloud revision. The sender creates a bounded immutable batch from journal events in a short local transaction. It then sends outside the transaction. Edits made during sending remain later journal events.

On acknowledgement, lock the aggregate, verify batch identity and request hash, record the receipt, and advance only its contiguous accepted/resolved prefix. Update the Cloud shadow if the returned revision is newer; rebuild the working projection by replaying later pending events. An old receipt never replaces a newer shadow or working body. A restart replays this same transaction. A server rejection preserves both the original proposal and any later edits.

Own-device feed entries suppress duplicate notifications only. They still reconcile the shadow and any matching batch receipt; a feed echo is not proof that all local edits were acknowledged. Conflict replacement, journal changes, shadow/projection update, command response and batch lineage commit together. Index rebuilds and previews consume the resulting typed source version; none reads a bare `rev` as a proxy for pending content.

**[I-498](../../requirements/01-normative-glossary-and-invariants.md#rule-i-498) — an evictable acknowledged cache is not an unacknowledged edit.** This is the distinction that decides whether a user loses work, so it is a schema property rather than a convention.

| # | Rule |
|---|---|
| <a id="rule-pe-01"></a>PE-01 | **Cloud is authoritative for acknowledged revisions of synchronised data** (`§5` of the product scope). The local store holds a **working cache** of what Cloud has acknowledged, plus **durable pending changes** that it has not. |
| <a id="rule-pe-02"></a>PE-02 | **A row is evictable only if every change to it has been acknowledged.** The gate is `head_local_seq == acked_local_seq` ([EV-L1](#rule-ev-l1)) **and** no staged upload and no unreturned tool receipt references it. The watermark comparison is the primary test because it is on the row itself; the batch-state check is the corroborating invariant, and the two must agree ([EV-L2](#rule-ev-l2)). |
| <a id="rule-pe-03"></a>PE-03 | **Cache pressure, sign-out, account switch, subscription restriction and workspace change never discard an unacknowledged change** ([C-06](../../requirements/00-product-scope-and-portfolio.md#rule-c-06)). Each of these paths runs the same eviction gate; none has a shortcut. |
| <a id="rule-pe-04"></a>PE-04 | **A durable local save is never presented as saved to Cloud** (`§3.1` of the product scope). The UI distinguishes *saved on this device* from *acknowledged by Cloud*, and the outbox row is what makes the difference queryable. |
| <a id="rule-pe-05"></a>PE-05 | **Pending work survives reinstall-level recovery.** The outbox, the journal and staged upload content are in the durable store, not in a cache directory that a cleanup tool may remove. |
| <a id="rule-pe-06"></a>PE-06 | **An acknowledged revision that is evicted is re-fetchable; an unacknowledged change that is lost is gone.** That asymmetry is why [PE-02](#rule-pe-02) is a constraint and not a heuristic. |

### 1.5 `local_audit`

Append-only, separate from telemetry ([OA-06](../13-observability-and-operations.md#rule-oa-06)), holding local security-relevant events: capability grant and revocation, approval decision, secret use, egress authorisation, local presence proof.

### 1.6 `managed_resource` and `resource_reference`

| `managed_resource` field | Type | Notes |
|---|---|---|
| `resource_id` | `id` | **PK** |
| `content_hash` | `text NN` | Content address |
| `size_bytes` | `bigint NN` | |
| `content_type` | `text?` | |
| `relative_path` | `text NN` | **Inside the managed store only** — never a user path |
| `state` | `enum(staging, verified, committed, releasing) NN` | |
| `reference_count` | `int NN` | *(derived from `resource_reference`)* |
| `last_reference_released_at` | `instant?` | |
| `cloud_object_id` | `id?` | Set when a cloud copy exists |

- `UQ (content_hash)` — local deduplication
- `IX (state, last_reference_released_at)` — garbage collection
- **Constraint** — `resource_id` is **never a file path** ([I-192](../../requirements/01-normative-glossary-and-invariants.md#rule-i-192)), and a `ResourceRef` crossing a boundary carries identity and metadata only ([BF-08](../12-native-interop-and-media.md#rule-bf-08))

`resource_reference` is `(resource_id, referrer_kind, referrer_id)` as a composite primary key. **Reference count derives from it** so a crash between reference and store is recoverable.

---

<a id="content-origin-storage"></a>
### Content origin storage and revision ownership

The [content origin carrier](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is an immutable typed record stored with the owning payload. A content unit has a stable `ContentUnitId`, bound to exactly one message part or report section/finding; it is a child of that owner's revision, not an independently mutable aggregate. A new payload version gets a new `ContentOriginId`, payload hash and parent lineage. The owning revision references both payload and origin. Their insertion/reference update is atomic through the same journal/write/sync path. Retained revisions pin their own origin records; deletion/GC follows the owning content's history/pins, never a separate metadata expiry.

Chat cache mirrors Cloud part origins. ArcScope native stores own local origins; Cloud metadata replicas carry the same typed projection without taking native authority. Native packages, generated downloads and sidecars use the carrier contract. Legacy absent metadata becomes `unknown`; unknown profile/fields remain inert and readable, and a writer unable to preserve them refuses affected writes. No origin payload includes credentials or an executable type name.

## 2. ArcChat local store

The historical feature name identifies no standalone application or database. All assistant tables, messages, attachments, projects, profiles, skills, context, compaction and pending execution are defined exclusively in [model 05](05-application-history.md). Each owning desktop has its own store; the MAUI Android build mirrors the logical schema in SQLite through its C# data layer ([P2-021](../../decisions/phase-2-specification-decisions.md#rule-p2-021); the Kotlin Room mirror is retired). Model 02 §1 still owns common product journal/resource mechanisms. Do not generate a second conversation/message schema from this section.

## 3. ArcScope local store

### `scope_project`, `session_record` *(aggregate roots)*

| Table | Required root fields / constraints |
|---|---|
| scope_project | project_id:id PK; name:Name NN; content_rev:bigint NN; state:enum(live,deleted) NN; created_at/updated_at:instant NN; deleted_at:instant?. Stable ID survives rename/restore; state and deleted_at agree. |
| session_record | session_id:id PK; project_id:id FK → scope_project NN; name:Name NN; content_rev:bigint NN; state:enum(live,deleted) NN; created_at/updated_at:instant NN; deleted_at:instant?. Stable ID survives rename/restore; state and deleted_at agree. Membership changes are native session commands and advance its content_rev. |

Both roots use the common command/journal and separate sync submission/shadow fields in §1. Project rename advances the project native revision without rewriting session names; each session belongs to exactly one project. Native deletion tombstones the root; no cascading physical deletion bypasses retention/resource pins. A deleted project hides its still-live sessions until restore or an explicit native move to a live project. New/moved sessions require a live local parent. Cloud project deletion changes the replica/shadow and is reconciled under normal pending-edit rules, never silently deleting native working data.

The sync adapter publishes `ScopeProjectMetadata` (project ID/name) and `ScopeMetadata` (session ID/name/project ID and declared content) to their distinct registered aggregate kinds. Native content revisions never substitute for their independent Cloud revisions. Enabling session/project metadata sync includes its parent metadata; parent publication and child publication need not be observed atomically. Missing/deleted Cloud parents suppress library visibility until reconciliation; they do not imply deletion of child data. Project sync disable retains the existing keep-local policy, while explicit replica deletion uses the normal tombstone lifecycle.

### `connection_profile` and `effective_configuration_snapshot`

| `effective_configuration_snapshot` field | Type | Notes |
|---|---|---|
| `snapshot_id` | `id` | **PK** |
| `session_id` | `id NN` | `FK →`; cascade |
| `captured_at` | `instant NN` | |
| `configuration` | `json NN` | **The settings actually in force** |
| `timing_source` | `enum(hardware, host) NN` | |
| `timing_uncertainty_ns` | `bigint?` | Recorded when host timing is used |

- **Constraint** — **immutable once written**. Editing a `connection_profile` never rewrites a historical snapshot ([SD-05](../../requirements/products/arcscope.md#rule-sd-05)). This is the row that makes a capture evidentially meaningful.

### `capture`, `capture_segment`, `gap`

| `capture` field | Type | Notes |
|---|---|---|
| `capture_id` | `id` | **PK** |
| `session_id` | `id NN` | `FK →`; restrict |
| `state` | `enum(armed, running, paused, stopped, finalized, interrupted) NN` | |
| `finalized_at` | `instant?` | |
| `end_marker` | `enum(clean, truncatedAtBoundary, truncatedMidChunk)?` | The **honest end marker** ([AQ-09](../12-native-interop-and-media.md#rule-aq-09)) |
| `recorded_loss` | `json?` | Counts and time ranges of loss |
| `store_root` | `text NN` | The chunked store location |

- **Constraint** — once `state = finalized`, **the row and its chunked data are immutable** ([SE-12](../../requirements/products/arcscope.md#rule-se-12)). A trigger or repository guard refuses any update, and a test asserts it.
- `capture_segment` records contiguous runs; `gap` records explicit interruptions with cause and duration. **A disconnect produces a gap row, never a silently shortened capture** ([AQ-08](../12-native-interop-and-media.md#rule-aq-08)).

### The chunked capture store

Raw capture is **not** in the relational store ([SE-14](../../requirements/products/arcscope.md#rule-se-14)). It is a chunked append store on disk:

| Element | Content |
|---|---|
| Chunk file | Fixed-size frames plus a per-chunk checksum |
| Chunk index | `(capture_id, chunk_ordinal) → offset, sample range, time range, checksum` |
| End marker | Written on finalisation; its absence means the capture was interrupted |

- **Recovery** — on start, an unfinalised capture is verified chunk by chunk; the verifiable prefix is retained and the loss is recorded ([WP-07.05](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.05), [AQ-09](../12-native-interop-and-media.md#rule-aq-09))
- **Constraint** — **no third-party extension has a write path to this store** ([EP-01](../../requirements/products/arcscope.md#rule-ep-01), [WP-35.05](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.05))

### `channel`, `signal`, `event_record`, `analysis_definition`, `analysis_result`, `annotation`, `finding`, `report`

<a id="measurement-storage"></a>
**Measurement projection.** `analysis_definition` stores the typed request: `profile=scope.measurement.v1`, source capture/channel and frozen revision/hash, start/end in the recorded timebase, alignment/calibration/unit and configuration snapshot, family set, optional cursor positions, optional reference levels. Its immutable request hash binds these fields. Execution resolves default levels against that same source/window and records them, never against a later live capture. `analysis_result` stores definition ID/version/hash, source bindings, resolved configuration, finite/excluded/run counts, requested/covered duration, timing uncertainty, and typed per-family `{status, reason?, value?, unit, observationCount}`. A numeric value exists only for `ok`; cursor delta has its two components/sample IDs. The [measurement profile](../../requirements/products/arcscope.md#measurement-profile) defines statuses, formulas and tolerance. Reports/UI reference the same result/configuration; an unsupported profile preserves historical display but refuses recomputation. Results are derived, while authored explanations and their origin are revisioned content.

`analysis_result` is *(derived)*: **deleting every result and rebuilding produces equivalent output under the recorded profile tolerance** ([WP-34.04](../../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.04)), so each row records its `analysis_definition_version`, its `decoder_version`, its input capture and range, and its configuration snapshot — the five things [LB-04](../../requirements/products/arcscope.md#rule-lb-04) requires for reproducibility. `annotation` and `finding` are **authored content with their own identity and history**, and are **never written into raw capture** ([WP-34.05](../../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.05)).

---

## 4. The portable package

**Which products have one.** These native working-package rules apply to **ArcScope**, and to a package explicitly offered by its owner; they impose no universal assistant archive format. The embedded assistant's exit path is a Cloud-generated download over acknowledged revisions, implemented as [assistant-history.v1](05-application-history.md) and [WP15.06](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.06), including its explicit local history export, with the real Cloud export producer in [WP25.08](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08). It is not a re-importable native package.

The working store is not the exchange format (`§8` of the persistence architecture). Where a product has a package, it is a directory or archive containing:

```
manifest.json          format version, product, created-by, content inventory with hashes
content/               canonical serialised aggregates, one file per aggregate root
resources/             managed resources by content hash
attachments-external/  external reference descriptors, never the files themselves
```

| # | Rule |
|---|---|
| <a id="rule-pp-01"></a>PP-01 | **The package is complete**: re-importing reconstructs every aggregate, relationship and managed resource ([WP-35.04](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04)). |
| <a id="rule-pp-02"></a>PP-02 | **Serialisation is deterministic** — stable ordering, stable key order, no timestamps outside content. Two exports of unchanged content are byte-identical ([WP-35.04](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04)). |
| <a id="rule-pp-03"></a>PP-03 | **Derived data is excluded.** No index or cache enters a package. |
| <a id="rule-pp-04"></a>PP-04 | **External references are exported as descriptors**, and collect/consolidate is the separate explicit operation that turns them into managed content ([WP-35.04](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04)). |
| <a id="rule-pp-05"></a>PP-05 | **The manifest carries `nativeFormatVersion`**, distinct from `storageSchemaVersion` — a version axis of its own. |

---

## 5. Verification

| # | Obligation | Where |
|---|---|---|
| <a id="rule-dl-01"></a>DL-01 | Every aggregate round-trips with all fields and relationships | Per-product persistence tests |
| <a id="rule-dl-03"></a>DL-03 | A finalised capture is structurally immutable | [WP-33.04](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.04) |
| <a id="rule-dl-05"></a>DL-05 | Deleting every derived store leaves each product fully intact | [WP-07.06](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.06) |
| <a id="rule-dl-07"></a>DL-07 | **Where a product has a portable package**, it round-trips with equivalence, deterministically | [WP-35.04](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04) |
| <a id="rule-dl-07a"></a>DL-07a | **Where a product's exit path is a Cloud download**, the export is complete over acknowledged revisions, states its exclusions, and **is not asserted to re-import** | [WP-15.06](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.06), [WP-25.08](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) |
| <a id="rule-dl-08"></a>DL-08 | **The repository read surface** excludes a trashed row from every list path, and **no application assembly can construct a query against the raw table** ([QP-06](00-data-model-overview.md#rule-qp-06)) | [WP-05](../../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) |
| <a id="rule-dl-09"></a>DL-09 | A crash at any write-path point recovers to a committed boundary | [WP-07.02](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.02) |

## [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) transport, storage and recovery composition

The [CF/R2 lifecycle](../contracts/05-cloudflare-integration.md) fixes part verification, Verified pins, authorization on consumption, release/deletion and independent immutable restore. C# owning transactions, sync cursors/tombstones/conflicts, desktop pending changes, native job snapshots and derived-source revision checks above retain their semantics. The [wire profile](../contracts/04-protobuf-wire-registry.md) transports exact values without changing content-origin or Scope measurement oracles. CF checkpoints/streams never become product history, and restoration cannot silently redispatch an uncertain external act.

## Client recovery generation

Per-realm session/cache metadata records recoveryGeneration; each outgoing command/outbox lineage captures it at creation. A generation change atomically stops dispatch and moves old entries to recoveryQuarantine while preserving payload, old IDs/revisions/hashes and attachments. Bootstrap starts new cursor state. Review/reapply produces a new command with the current generation and current owner precondition, retaining provenance to the quarantined item. Quarantine has no automatic expiry that deletes pending user content. A local native command unrelated to Cloud remains governed by its native store and is not rewritten by a realm restore.

## Local transport and connector records

EndpointManifest protobuf and connection/peer leases follow [local 09](../contracts/09-local-grpc-and-sandbox.md). Nonces, launch secrets and helper handle maps are memory-only. Discovery files are untrusted hints in the private runtime directory, not account/session persistence.

The owning product keeps local connector_connection(connection_id, definition_id, manifest_hash, name, state, scopes, revision, expires_at, reason, secret_ref?) and connector_flow(flow_id, connection_id, definition_hash, target_origins, scopes, expires_at, consumed_at). IDs/closed states and ten-minute one-use flow follow the generated Connector records; revision is a positive local row counter checked by expectedRev. Consent binds the exact manifest/origins/scopes. Secrets reside only in OS-protected storage referenced by secret_ref. Complete consumes flow and commits the local connection/secret reference atomically through the broker's compensation journal; a crash either reconciles the existing secret handle or removes an unreferenced handle. Revoke invalidates the connection before asynchronous provider cleanup; a failed provider cleanup never restores local authority. This state is not synchronized into Cloud connector credentials. WP11 supplies protected persistence/broker mechanics; WP41 supplies real provider integration.
