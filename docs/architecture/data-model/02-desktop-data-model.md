# Desktop Local Data Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Data model
> Governing authority: [`00-data-model-overview.md`](00-data-model-overview.md), [`../06-data-persistence-and-formats.md`](../06-data-persistence-and-formats.md)
> Companions: [`../04-desktop-application-architecture.md`](../04-desktop-application-architecture.md), [`../07-sync-conflict-and-backup.md`](../07-sync-conflict-and-backup.md)

Each desktop product owns its SQLite store. Chat/Notes hold acknowledged Cloud projections plus durable unsent/pending work. Scope/Slate retain local authority for native working content and jobs, with separately revisioned Cloud metadata replicas. The version domains are defined in [the authority map](00-data-model-overview.md#4-authority-map--where-the-authoritative-copy-lives).

**Store technology.** An embedded relational store with an AOT-safe access path ([CS-01](../06-data-persistence-and-formats.md#rule-cs-01)). Journaling is enabled only after per-platform and per-filesystem validation ([CS-04](../06-data-persistence-and-formats.md#rule-cs-04)), because network volumes, removable media and container filesystems each break different assumptions.

---

## 1. What every product store contains

Five table groups are identical in shape across all four products. They are specified once here and referenced, not repeated.

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
| `result_version` | `json?` | Typed result token: Cloud revision, Notes local token, or native content revision |
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
| `source_version` | `json NN` | Notes `(acked_rev, head_local_seq)` or native `content_rev`; discriminator fixes the version domain |
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

A Notes working aggregate carries `acked_rev`, `acked_local_seq` and `head_local_seq`. `acked_rev` names its separately retained canonical Cloud shadow; the displayed body is that shadow plus unresolved local edits. A Scope/Slate root additionally owns `content_rev`, which advances on every native domain commit and is what local jobs snapshot. Its sync metadata tracks the same submission identities separately. Chat uses durable draft/command identities and acknowledged Cloud projections; an unsent draft is not a synchronised aggregate revision.

| # | Rule |
|---|---|
| RV-C1 | **`acked_rev` is the only revision Cloud ever sees**, and it is the `ExpectedRev` on `sync.pushChange`. A device that sent a local counter would conflict on every second edit, because Cloud has never heard of it. |
| RV-C2 | **The pending predicate is `head_local_seq > acked_local_seq`**, not a counter being non-zero. In the counterexample, acknowledging A advances `acked_local_seq` to A's sequence while `head_local_seq` is B's — so the row is correctly still pending. |
| <a id="rule-rv-c3"></a>RV-C3 | **`local_seq` is never reset.** Resetting is what destroyed the ability to say which work an acknowledgement covered. It is a per-aggregate, per-device counter and its absolute value has no meaning outside that pair. |
| <a id="rule-rv-c4"></a>RV-C4 | **An acknowledgement advances the watermark to the highest `local_seq` the submitted batch contained — and no further.** The batch records its range when it is dispatched, so the covered set is a recorded fact, not a re-derivation at acknowledgement time. |
| <a id="rule-rv-c5"></a>RV-C5 | **A Notes local RPC takes and returns `(acked_rev, head_local_seq)`.** Every user edit or explicit conflict-resolution edit advances `head_local_seq`; applying a newer Cloud shadow advances `acked_rev` and rebases pending work atomically. A body cannot change while both token components stay unchanged. Scope/Slate RPC instead uses its native `content_rev`. |
| RV-C6 | **A conflict compares `acked_rev`, never a local sequence.** Two devices conflict when they submitted against the same `acked_rev`; how much local work each accumulated is irrelevant to that question. |

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
| SB-L4 | **A duplicate or delayed acknowledgement is idempotent.** Advancing the watermark to a value at or below its current one is a no-op, so an acknowledgement arriving twice — or late, after a newer one — cannot move it backwards. |
| SB-L5 | **A lost response is resolved by re-sending the same `batch_id`.** Cloud returns the original result ([TX-04](00-data-model-overview.md#rule-tx-04)), including the revision it assigned, so the client learns the outcome without a second effect. |
| SB-L6 | **Restart resumes from the log.** A `dispatched` batch with no settlement is re-sent; a `pending` batch is built and sent. Nothing is inferred from in-memory state. |
| SB-L7 | **Conflict does not advance the acknowledgement watermark.** Stop dispatch for that aggregate, retain the old proposal and fetch the current Cloud shadow. Rebase unresolved local events in one local transaction. Automatic structural rebase cannot decide a semantic conflict. An explicit user resolution appends a new local event, supersedes the conflicted proposal and any dependent undispatched proposals, and creates one replacement covering the contiguous unresolved range through the resolution event against the new `acked_rev`. Original local event identities and bytes remain immutable. |
| SB-L8 | **Replacement has explicit lineage and dispositions.** Its receipt states which original edits were retained, transformed or explicitly discarded by the user. Even a keep-Cloud resolution sends an idempotent resolution command; its no-content-change receipt can acknowledge the resolved range without inventing a content revision. Advance `acked_local_seq` only over a contiguous accepted/resolved prefix. Superseded receipts never advance it independently. Historical discarded content is retained for the declared recovery window. |

#### Safe eviction

| # | Rule |
|---|---|
| <a id="rule-ev-l1"></a>EV-L1 | **A row is evictable only when `head_local_seq == acked_local_seq`** and no staged upload and no unreturned tool receipt references it. This is [PE-02](#rule-pe-02), restated against the watermark. |
| <a id="rule-ev-l2"></a>EV-L2 | **The corroborating invariant is that no batch for the aggregate is in a non-terminal state.** The two conditions must agree; a periodic check asserts they do, and a disagreement is a defect rather than a tie-break. |
| EV-L3 | **Cache pressure, sign-out, account switch and subscription restriction all run this same gate** ([PE-03](#rule-pe-03)). None has a shortcut, because each is a path by which unacknowledged work has historically been lost. |

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
| PE-05 | **Pending work survives reinstall-level recovery.** The outbox, the journal and staged upload content are in the durable store, not in a cache directory that a cleanup tool may remove. |
| PE-06 | **An acknowledged revision that is evicted is re-fetchable; an unacknowledged change that is lost is gone.** That asymmetry is why [PE-02](#rule-pe-02) is a constraint and not a heuristic. |

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

The [content origin carrier](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is an immutable typed record stored with the owning payload. A content unit has a stable `ContentUnitId`, bound to exactly one message part, Notes block/attachment, report section/finding or media asset/output; it is a child of that owner's revision, not an independently mutable aggregate. A new payload version gets a new `ContentOriginId`, payload hash and parent lineage. The owning revision references both payload and origin. Their insertion/reference update is atomic through the same journal/write/sync path. Retained revisions pin their own origin records; deletion/GC follows the owning content's history/pins, never a separate metadata expiry.

Chat cache mirrors Cloud part origins. Notes pending events, conflict alternatives, undo, checkpoints and restored revisions preserve origin along with content; restoring/copying to a new payload version retains its kinds. Scope/Slate native stores own local origins; Cloud metadata replicas carry the same typed projection without taking native authority. Native packages, generated downloads and sidecars use the carrier contract. Legacy absent metadata becomes `unknown`; unknown profile/fields remain inert and readable, and a writer unable to preserve them refuses affected writes. No origin payload includes credentials or an executable type name.

## 2. ArcChat local store

### `conversation` *(aggregate root)*

| Field | Type | Notes |
|---|---|---|
| `conversation_id` | `id` | **PK** |
| `project_id` | `id?` | `FK →` `arcchat_project`; set null on project delete |
| `title` | `text NN` | |
| `agent_profile_id` | `id?` | The profile in force |
| `state` | `enum(active, archived, trashed) NN` | |
| `trashed_at` | `instant?` | |
| `created_at`, `updated_at` | `instant NN` | |
| `rev` | `rev NN` | |

- `IX (state, updated_at)` — the conversation list, the single hottest query
- `IX (project_id, state, updated_at)` — project-scoped list

### `conversation_branch`

| Field | Type | Notes |
|---|---|---|
| `branch_id` | `id` | **PK** |
| `conversation_id` | `id NN` | `FK →`; cascade |
| `parent_branch_id` | `id?` | Null for the trunk |
| `branch_point_message_id` | `id?` | The message this branched from |
| `created_at` | `instant NN` | |

- `IX (conversation_id, parent_branch_id)`
- **Constraint** — branching **shares prior history by reference, never by copy** ([WP-15.01](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.01)). Messages before the branch point belong to the parent branch and are read through it; there is no duplication.

### `message`

| Field | Type | Notes |
|---|---|---|
| `message_id` | `id` | **PK** |
| `conversation_id` | `id NN` | `FK →`; cascade |
| `branch_id` | `id NN` | `FK →`; cascade |
| `ordinal` | `bigint NN` | Position within the branch |
| `role` | `enum(user, assistant, tool, system) NN` | |
| `state` | `enum(composing, complete, interrupted, failed) NN` | |
| `revision_of_message_id` | `id?` | An edit creates a new row; the prior is retained |
| `created_at` | `instant NN` | |

- `UQ (branch_id, ordinal)`
- `IX (conversation_id, created_at)`
- **Constraint** — a committed message is **immutable**; an edit creates a new row ([WP-15.00](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.00))
- **Constraint** — a row is written with `state = complete` **only** when the stream finished. An interrupted stream is stored as `interrupted`, never as complete ([WP-15.00](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.00)) — this is why `state` exists rather than a nullable completion timestamp.

### `message_part`

| Field | Type | Notes |
|---|---|---|
| `part_id` | `id` | **PK** |
| `message_id` | `id NN` | `FK →`; cascade |
| `ordinal` | `int NN` | |
| `kind` | `enum(text, toolCall, toolResult, artifactRef, attachmentRef, citation, redaction) NN` | |
| `payload` | `json NN` | Kind-specific, schema-validated |

- `UQ (message_id, ordinal)`
- **Rule** — `toolCall` and `toolResult` parts carry the `InvocationId` so a message links to its execution record without embedding it

### `attachment`

| Field | Type | Notes |
|---|---|---|
| `attachment_id` | `id` | **PK** |
| `message_id` | `id?` | Null while attached to a draft |
| `conversation_id` | `id NN` | |
| `mode` | `enum(managed, externalReference) NN` | |
| `resource_id` | `id?` | Set when `managed` — `FK →` `managed_resource` |
| `external_locator` | `json?` | Set when `externalReference` |
| `availability` | `enum(available, unavailable, checking) NN` | A visible state, not an error ([WP-15.02](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.02)) |
| `display_name` | `text NN` | |

- **Constraint** — `mode = managed` ⟺ `resource_id` is not null; `mode = externalReference` ⟺ `external_locator` is not null. A check constraint enforces the discriminated union.
- **Constraint** — **no attachment body is ever stored in `message_part.payload`** ([WP-15.02](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.02)), asserted by a size limit on the column and a policy test.

### `arcchat_project`, `agent_profile`, `skill`

`arcchat_project` groups conversations with its own instructions and context references. `agent_profile` bundles model choice, mode and behaviour, versioned so a historical run records the version it used. `skill` is versioned declarative guidance: **a skill grants no capability** ([WP-15.04](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.04)), so there is no permission column on it, and `skill_version` rows are immutable so a skill update never alters a historical result.

### `context_reference`

| Field | Type | Notes |
|---|---|---|
| `context_ref_id` | `id` | **PK** |
| `scope_kind` | `enum(pinned, project, temporary) NN` | |
| `owner_kind`, `owner_id` | `text NN`, `id NN` | Conversation or project |
| `target_product` | `text NN` | |
| `target_ref` | `json NN` | A `ResourceRef` or a product-specific selector |
| `added_at` | `instant NN` | |

- **Rule** — **there is no ambient default scope** ([CA-01](../09-ai-and-agent-runtime-architecture.md#rule-ca-01)). Absence of rows means absence of context.

### `task_projection`

The local read projection of tasks whose authority is elsewhere ([TO-07](00-data-model-overview.md#rule-to-07)): carries `task_id`, `authoritative_rev`, state, reason facet, and `projected_at`. **Stamped with the authoritative revision**, so staleness is detectable.

---

## 3. ArcNotes local store

### Cloud projection and folder ownership

The canonical shape is [Cloud Notes §8.4](01-cloud-data-model.md#84-notes--canonical-cloud-knowledge-store). SQLite stores the same logical notebook, folder, document, block and scalar-property fields, scoped to the enrolled workspace, alongside a separate acknowledged shadow and pending journal. Local table `rev` fields in this section mean `acked_rev` on the shadow; working mutations use the composite local token, not a fabricated Cloud revision.

`notebook` has `notebook_id`, `workspace_id`, title, state and the local version fields. `folder` has `folder_id`, `notebook_id`, nullable `parent_folder_id`, name, fractional ordinal, state and timestamps. Folder rows are children of the notebook revision. Parent and document-placement foreign keys remain within one notebook; cycles are rejected under the notebook writer. Root and nested sibling order is `(ordinal, folder_id)` with an explicit root predicate, not a uniqueness assumption about NULL. Folder trash hides descendants without changing each document's own trash state. The same folder and placement commands and lock order are validated locally and in Cloud.

### `notebook`, `document` *(aggregate roots)*

| `document` field | Type | Notes |
|---|---|---|
| `document_id` | `id` | **PK** |
| `notebook_id` | `id NN` | `FK →` `notebook`; restrict |
| `folder_id` | `id?` | Null at notebook root; composite FK `(notebook_id, folder_id)` to `folder`, restrict |
| `title` | `text NN` | **An independent field, not the first heading block** ([DC-03](../../requirements/products/arcnotes.md#rule-dc-03)) |
| `state` | `enum(active, trashed) NN` | |
| `trashed_at` | `instant?` | |
| `created_at`, `updated_at` | `instant NN` | |
| `rev` | `rev NN` | |

- `IX (notebook_id, state, updated_at)`
- `IX (state, updated_at)` — the global recent list
- **Partial index** on `state = active` for every list path — for **size and speed only**. It does **not** filter: a query omitting the predicate simply does not use it and returns trashed rows from a sequential scan ([QP-05](00-data-model-overview.md#rule-qp-05))
- **Exclusion is enforced by the repository read surface**, which applies the state predicate and is the only reachable path to this table from application code ([QP-06](00-data-model-overview.md#rule-qp-06))

### `block`

| Field | Type | Notes |
|---|---|---|
| `block_id` | `id` | **PK** — stable across reorder and reparent ([WP-18.00](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00)) |
| `document_id` | `id NN` | `FK →`; cascade |
| `parent_block_id` | `id?` | Null at document root |
| `ordinal` | `text NN` | **A fractional order key**, not an integer |
| `kind` | `text NN` | Exactly the [BL-04](../../requirements/products/arcnotes.md#rule-bl-04) V1 set: `paragraph`, `heading`, `list`, `quote`, `callout`, `code`, `divider`, `table`, `math`, `image`, `attachment`, `embed`, `toggle`. **Checklist is a `list` style and PDF is an `attachment` presentation** — neither is a separate kind (`§2.1` of the editing architecture) |
| `content` | `json NN` | The kind's declared content shape; text-bearing kinds carry `InlineContent` (`§2` of the [editing architecture](../18-editing-and-rich-content.md)) |
| `created_at` | `instant NN` | |

- `UQ (document_id, parent_block_id, ordinal)`
- `IX (document_id, parent_block_id, ordinal)` — the document read path, in document order
- **Constraint** — a block carries **no revision of its own** ([RV-03](00-data-model-overview.md#rule-rv-03)); the document's revision governs
- **Why a fractional order key** — inserting between two blocks must not renumber siblings, because renumbering would make every insert a whole-document write and would defeat sync's per-aggregate change detection. The key is a string with a defined mid-point algorithm and a rebalance operation that is itself a normal revision.

### `document_link`, `link_index`

| `document_link` field | Type | Notes |
|---|---|---|
| `link_id` | `id` | **PK** |
| `source_document_id` | `id NN` | `FK →`; cascade |
| `source_block_id` | `id?` | |
| `target_kind` | `enum(document, block, external) NN` | |
| `target_document_id`, `target_block_id` | `id?` | **Identity, never a title** ([BR-04](../../planning/work-packages/18-arcnotes-document-core.md#rule-br-04) of [WP-18](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18)) |
| `display_alias` | `text?` | |
| `state` | `enum(resolved, broken) NN` | An explicit state, never a silent failure |

- `IX (target_document_id)` — **the backlink query path**
- **Rule** — `link_index` is *(derived)*: the backlink panel reads it, and **backlinks are never written into block content** ([WP-18.02](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.02)). Deleting the index rebuilds it.

### `tag`, `document_tag`

`tag` is cross-cutting classification carrying **no hierarchical position**. `document_tag` is `(document_id, tag_id)`. **Deleting a tag deletes the `document_tag` rows and nothing else** — documents survive ([BR-07](../../planning/work-packages/18-arcnotes-document-core.md#rule-br-07) of [WP-18](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18)), enforced by the foreign key direction.

### `property_definition`, `property_value`

| `property_definition` field | Type | Notes |
|---|---|---|
| `property_def_id` | `id` | **PK** |
| `key` | `text NN` | |
| `owner` | `enum(system, user) NN` | Separated, never conflated ([WP-28.00](../../planning/work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.00)) |
| `type` | `enum(text, number, date, dateTime, select, multiSelect, checkbox, url) NN` | The [required scalar property kinds](../../requirements/products/arcnotes.md#7-properties-tags-and-views); `select` is single-select |
| `config` | `json NN` | Typed `notes.scalar.v1` profile/options and optional scale (default 9, max 9), per the [query profile](../../requirements/products/arcnotes.md#notes-scalar-query-profile); no relation/evaluator |
| `semantic_rev` | `rev NN` | Changes for comparison-affecting config/type/option membership, not labels; normal `rev` changes for every edit |
| `rev` | `rev NN` | |

`property_value` is `(document_id, property_def_id)` with exactly one typed value column set per type. Numbers use exact decimal storage (28 significant digits, scale at most 9); date and UTC instant have distinct columns; options use stable IDs and multi-select is a bounded set. No row means missing; a null write deletes the row, while empty/false/zero remain present. The [query profile](../../requirements/products/arcnotes.md#notes-scalar-query-profile) governs write validation, type-change refusal and every comparison. **A document with no property rows has no property overhead** — this is what makes [WP-28.04](../../planning/work-packages/28-arcnotes-properties-and-views.md#rule-wp-28.04)'s lightness requirement structural rather than a UI choice.

- `IX (property_def_id, value_text)`, `IX (property_def_id, value_number)`, `IX (property_def_id, value_date)` — the query-and-view paths

### `saved_view`

`saved_view` is a saved query plus its configuration and view kind. **It owns no documents**, so its deletion cascades to nothing.

| Field | Type | Notes |
|---|---|---|
| `saved_view_id` | `id` | **PK** |
| `notebook_id` | `id NN` | One authorized notebook, per the accepted saved-view scope |
| `query_profile` | `text NN` | `notes.scalar.v1`; unknown version remains read-only and cannot execute |
| `definition_semantic_revs` | `json NN` | Typed map of referenced PropertyDefId to semantic revision |
| `kind` | `enum(list, table) NN` | **Exactly two layouts** ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)). Board, gallery, calendar and timeline layouts are excluded |
| `filter` | `json?` | Null means match-all; otherwise bounded property predicates over the declared scalar kinds in [property storage](#property_definition-property_value), governed by the [ArcNotes property and view requirements](../../requirements/products/arcnotes.md#7-properties-tags-and-views) |
| `sort` | `json NN` | At most 8 typed keys, missing last and final DocumentId ascending; [profile](../../requirements/products/arcnotes.md#notes-scalar-query-profile) |
| `columns` | `json?` | Table layout only |
| `rev` | `rev NN` | |

- **Constraint** — a filter references only **declared property definitions with scalar types**. There is no formula, relation or rollup evaluator ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)), and no expression language enters this column
- **Rule** — a view is a **query, never a container**. Deleting a view deletes no document; a document appears in a view because it matches, not because it was added

> **Retired identifiers.** `canvas`, `canvas_element`, `slide_deck`, `slide` and `speaker_note` are **retired by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** and are not reused. Edgeless canvas, whiteboard surfaces, shapes, connectors, frames and presentations are excluded from delivery, with no mandatory future hook. Their historical definitions are in the git history of this document at `7ed79a6`.

**Query dataset token.** The materialized Notes query source maintains a monotonically changing token for relevant notebook membership/value/trash changes; local evaluation also binds hydration and pending-local generations. Authorization is rechecked on each page. A consistent read returns its token with results; a cursor checks that token before reading the next page. Token change produces the profile's explicit restart, not a page from another dataset. Tokens are opaque equality/version evidence, never content revision values compared across different aggregates. Label-only definition rename leaves semantic bindings valid; type/config changes follow the profile's refusal/repair rules.

### `document_history`, `checkpoint`, `trash_entry`

Three distinct mechanisms plus the journal make four ([QI-09](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-09)):

| Mechanism | Table | Scope | Retention |
|---|---|---|---|
| Undo | *in-memory session stack, not persisted* | Session | Session |
| History | `document_history` | Per document, per revision | Policy window |
| Checkpoint | `checkpoint` | Explicit user act | Until deleted |
| Journal | `journal` (§1.3) | Crash recovery | Until snapshot |

**None substitutes for another**, and a test asserts each behaves independently ([WP-18.05](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.05)).

---

## 4. ArcScope local store

### `scope_project`, `session_record` *(aggregate roots)*

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

## 5. ArcSlate local store

### `slate_project`, `sequence` *(aggregate roots)*

| `sequence` field | Type | Notes |
|---|---|---|
| `sequence_id` | `id` | **PK** |
| `project_id` | `id NN` | `FK →`; cascade |
| `frame_rate_num`, `frame_rate_den` | `int NN` | **The sequence's own output video grid.** Rational, stored exactly — never a float. A sequence has exactly one; its sources may have many different ones ([SG-01](../23-simulator-and-interchange.md#rule-sg-01)) |
| `drop_frame` | `bool NN` | Timecode **presentation** only; it never affects position arithmetic (`§3.6` of the time model) |
| `sample_rate` | `int NN` | **The sequence's own output audio grid** ([SG-02](../23-simulator-and-interchange.md#rule-sg-02)) |
| `ticks_per_video_frame` | `bigint NN` | *(derived, materialised)* Exact ticks per output frame. **NOT NULL** — a sequence grid that is not exactly representable cannot exist ([TB-02](../23-simulator-and-interchange.md#rule-tb-02)) |
| `ticks_per_audio_sample` | `bigint NN` | *(derived, materialised)* Exact ticks per output sample |
| `width`, `height` | `int NN` | |
| `working_color_config` | `json NN` | |
| `rev` | `rev NN` | |

- **Constraint** — `ticks_per_video_frame` and `ticks_per_audio_sample` are **exact**: `705600000 × frame_rate_den` must divide by `frame_rate_num`, and `705600000` by `sample_rate`. A sequence whose grid is not exactly representable **cannot be created** ([TB-02](../23-simulator-and-interchange.md#rule-tb-02), [SG-03](../23-simulator-and-interchange.md#rule-sg-03))
- **Constraint** — a frame rate is **never** stored as a floating-point value. This single decision is what prevents accumulated drift ([WP-36.01](../../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.01)), and a policy test asserts no float column exists in the time model.

### `media_asset`, `media_stream`

| `media_asset` field | Type | Notes |
|---|---|---|
| `media_asset_id` | `id` | **PK** — a stable logical identity |
| `project_id` | `id NN` | |
| `mode` | `enum(externalReference, managed) NN` | Reference-in-place by default ([MD-03](../../requirements/products/arcslate.md#rule-md-03)) |
| `content_hash` | `text?` | Present when managed or once hashed |
| `availability` | `enum(available, offline, checking) NN` | **A normal state, not an error** ([MD-05](../../requirements/products/arcslate.md#rule-md-05)) |
| `metadata` | `json NN` | Streams, codecs, dimensions, rate, duration, colour metadata, timecode, channel layout |
| `color_interpretation_override` | `json?` | **Never modifies the source** ([CO-03](../../requirements/products/arcslate.md#rule-co-03)) |

- **Constraint** — `media_asset_id` is **not a file path** ([I-192](../../requirements/01-normative-glossary-and-invariants.md#rule-i-192)), and **a clip never references a file** ([MD-07](../../requirements/products/arcslate.md#rule-md-07))
- `media_location` is a separate table keyed `(media_asset_id, device_id)` — **the same asset may resolve to different locations on different devices** ([MD-08](../../requirements/products/arcslate.md#rule-md-08)) while remaining one logical asset. This table is device-local and does not sync.


**Source time bases live here, not on the sequence** ([SG-01](../23-simulator-and-interchange.md#rule-sg-01)). One sequence routinely contains sources with different stream time bases, so a single per-sequence field could not represent them.

| `media_stream` field | Type | Notes |
|---|---|---|
| `media_stream_id` | `id` | **PK** |
| `media_asset_id` | `id NN` | `FK →`; cascade |
| `stream_kind` | `enum(video, audio, subtitle, data) NN` | |
| `stream_index` | `int NN` | The container's own index |
| `rate_num`, `rate_den` | `int NN` | **This stream's own** rate. Rational, exact, never a float |
| `pts_time_base_num`, `pts_time_base_den` | `int NN` | The container's PTS base for **this stream** — generally neither the stream rate nor any sequence's |
| `ticks_per_pts_unit` | `bigint?` | Exact tick mapping where the PTS base divides the tick base; **NULL means the mapping rounds** ([SM-03](../23-simulator-and-interchange.md#rule-sm-03)), and the rounding is recorded in the conform report |
| `start_pts` | `bigint NN` | The container's own origin, preserved rather than normalised away |

- `UQ (media_asset_id, stream_index)`
- **Constraint** — a `NULL` `ticks_per_pts_unit` is legal and **does not block import** ([SM-03](../23-simulator-and-interchange.md#rule-sm-03)); it makes the stream's mapping approximate, and the approximation is reported, never silent
- **Rule** — a stream's rate is never assumed equal to the sequence's output grid. That assumption is the defect [SG-01](../23-simulator-and-interchange.md#rule-sg-01) exists to prevent

### `track`, `timeline_item`, `clip`, `transition`

> **Corrected 2026-09-07.** Positions were stored as integer frames with a **parallel integer sample column set**. Those two grids cannot agree: at 30000/1001 fps and 48 kHz one frame is 1601.6 samples, so most frame positions have no integer sample and most sample positions have no integer frame. Storing both made the model self-contradictory. Positions are now **canonical ticks** (`§3` of the [time model](../23-simulator-and-interchange.md)); frames and samples are computed projections.

| `timeline_item` field | Type | Notes |
|---|---|---|
| `timeline_item_id` | `id` | **PK** |
| `sequence_id`, `track_id` | `id NN` | `FK →`; cascade |
| `kind` | `enum(clip, transition, gap, generatedMedia, title, subtitleCue) NN` | |
| `start_ticks` | `bigint NN` | **Canonical ticks at 705 600 000 Hz** ([TB-01](../23-simulator-and-interchange.md#rule-tb-01)) |
| `duration_ticks` | `bigint NN` | |
| `media_asset_id` | `id?` | Clips only |
| `source_in_ticks`, `source_out_ticks` | `bigint?` | In the **source's** canonical tick domain, mapped by conform ([SM-02](../23-simulator-and-interchange.md#rule-sm-02)) |

- `IX (sequence_id, track_id, start_ticks)` — **the timeline read path**
- **Constraint** — many timeline items may reference one `media_asset` independently ([I-477](../../requirements/01-normative-glossary-and-invariants.md#rule-i-477)); there is no back-reference from asset to clip
- **Constraint** — **no position column is a frame number, a sample index, a float or a duration type** ([TB-01](../23-simulator-and-interchange.md#rule-tb-01), [TB-04](../23-simulator-and-interchange.md#rule-tb-04)), asserted by a repository policy test ([TV-02](../23-simulator-and-interchange.md#rule-tv-02))
- **Constraint** — `duration_ticks > 0`; a zero-length item is not representable
- **Rule** — the sequence's frame rate and the project's audio rate are **projection parameters**, not storage units. Changing a sequence's frame rate reprojects the display without altering a single stored position, which is what makes a rate change non-destructive.

### `effect_instance`, `effect_parameter`, `keyframe`, `animation_curve`

`effect_instance` references an `effect_definition_id` from a catalogue — **definition and instance are separate** ([I-483](../../requirements/01-normative-glossary-and-invariants.md#rule-i-483), [WP-37.03](../../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.03)). `keyframe` carries `scope ∈ {clipLocal, sequence}` **explicitly**, so keyframe time can never silently switch domain when a clip moves ([PG-09](../../assurance/open-gates-register.md#rule-pg-09) of the ArcSlate requirements).

### Derived stores — proxy, render cache, waveform, thumbnail

All four are *(derived)*, in a **separate store file** from the project, so [WP-37.05](../../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.05)'s "delete every cache and the project is intact" is structurally true rather than a promise. Each row records the source asset, the source content hash and the generation parameters, so a stale entry is detectable. **Switching proxy on or off never changes render output** ([MP-06](../12-native-interop-and-media.md#rule-mp-06)) because the render path resolves the original unless proxy render is explicitly declared on the `render_request`.

### `export_preset`, `render_request`

| `render_request` field | Type | Notes |
|---|---|---|
| `render_request_id` | `id` | **PK** |
| `sequence_id` | `id NN` | |
| `bound_project_rev`, `bound_sequence_rev` | `rev NN` | **The immutable snapshot binding** ([RN-04](../../requirements/products/arcslate.md#rule-rn-04)) |
| `range_start_ticks`, `range_end_ticks` | `bigint NN` | **Canonical ticks** ([TB-01](../23-simulator-and-interchange.md#rule-tb-01)). Output is half-open and follows [BO-01](../23-simulator-and-interchange.md#rule-bo-01) through [BO-04](../23-simulator-and-interchange.md#rule-bo-04); outward decode coverage never expands emitted sample ownership |
| `export_preset_id` | `id NN` | |
| `allow_proxy_render` | `bool NN` | Explicit, recorded in output metadata |
| `job_id` | `id NN` | A render is a **native Product Job**, not a Cloud Agent Task ([CM-04](../09-ai-and-agent-runtime-architecture.md#rule-cm-04) of the runtime architecture, [I-485](../../requirements/01-normative-glossary-and-invariants.md#rule-i-485)). ArcSlate owns its progress, cancellation and recovery |
| `destination` | `text NN` | |

- **Constraint** — the render reads the bound revisions, never live editor state. Editing during a render cannot affect its output ([WP-38.02](../../planning/work-packages/38-arcslate-render-and-colour.md#rule-wp-38.02)).

---

## 6. The portable package

**Which products have one.** The package requirements apply to **the ArcScope and ArcSlate native formats**, and to any package a product explicitly offers. **They create no ArcNotes or ArcChat local archive obligation** (`§4` of the data-format requirements; [EP-04](../../requirements/products/arcnotes.md#rule-ep-04) of the ArcNotes requirements; [EX-01](../../requirements/products/arcchat.md#rule-ex-01) of the ArcChat requirements): those two products' exit path is a Cloud-generated download over acknowledged revisions, with client fixtures in [WP-19.05](../../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.05) and [WP-15.06](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.06) and the real Cloud export gate in [WP-25.08](../../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08), and neither produces a re-importable native package. Reading this section as a universal obligation is how an impossible round-trip gate gets written.

The working store is not the exchange format (`§8` of the persistence architecture). Where a product has a package, it is a directory or archive containing:

```
manifest.json          format version, product, created-by, content inventory with hashes
content/               canonical serialised aggregates, one file per aggregate root
resources/             managed resources by content hash
attachments-external/  external reference descriptors, never the files themselves
```

| # | Rule |
|---|---|
| PP-01 | **The package is complete**: re-importing reconstructs every aggregate, relationship and managed resource ([WP-39.02](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.02), [WP-35.04](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04)). |
| PP-02 | **Serialisation is deterministic** — stable ordering, stable key order, no timestamps outside content. Two exports of unchanged content are byte-identical ([WP-39.02](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.02), [WP-35.04](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04)). |
| PP-03 | **Derived data is excluded.** No index, cache, proxy or thumbnail enters a package. |
| PP-04 | **External references are exported as descriptors**, and collect/consolidate is the separate explicit operation that turns them into managed content ([WP-39.02](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.02)). |
| PP-05 | **The manifest carries `nativeFormatVersion`**, distinct from `storageSchemaVersion` — a version axis of its own. |

---

## 7. Verification

| # | Obligation | Where |
|---|---|---|
| DL-01 | Every aggregate round-trips with all fields and relationships | Per-product persistence tests |
| DL-02 | Block order survives insert-between without renumbering siblings | [WP-18.00](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) |
| DL-03 | A finalised capture is structurally immutable | [WP-33.04](../../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.04) |
| DL-04 | No floating-point column exists in the ArcSlate time model | [WP-36.01](../../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.01) policy test |
| DL-05 | Deleting every derived store leaves each product fully intact | [WP-07.06](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.06), [WP-37.05](../../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.05) |
| DL-06 | Undo, history, checkpoint and journal behave independently | [WP-18.05](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.05) |
| DL-07 | **Where a product has a portable package**, it round-trips with equivalence, deterministically | [WP-39.02](../../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.02), [WP-35.04](../../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04) |
| DL-07a | **Where a product's exit path is a Cloud download**, the export is complete over acknowledged revisions, states its exclusions, and **is not asserted to re-import** | [WP-19.05](../../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.05), [WP-15.06](../../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.06) |
| DL-08 | **The repository read surface** excludes a trashed row from every list path, and **no application assembly can construct a query against the raw table** ([QP-06](00-data-model-overview.md#rule-qp-06)) | [WP-18.00](../../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00), [WP-05](../../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) |
| DL-09 | A crash at any write-path point recovers to a committed boundary | [WP-07.02](../../planning/work-packages/07-local-persistence-foundation.md#rule-wp-07.02) |

## P2-009 transport, storage and recovery composition

The [CF/R2 lifecycle](../contracts/05-cloudflare-integration.md) fixes part verification, Verified pins, authorization on consumption, release/deletion and independent immutable restore. C# owning transactions, sync cursors/tombstones/conflicts, desktop pending changes, native job snapshots and derived-source revision checks above retain their semantics. The [wire profile](../contracts/04-protobuf-wire-registry.md) transports exact values without changing content-origin, Notes scalar or Scope measurement oracles. CF checkpoints/streams never become product history, and restoration cannot silently redispatch an uncertain external act.

## Structural outbox and Slate metadata completeness

Notes outbox entries have a closed payload union: contentProposal or namedStructuralCommand. The latter stores operation ID plus its generated request, ordered affected root IDs and their composite base tokens, immutable request hash, batchId/local sequence range, explicit classification mapping and preview hash. Structural command acknowledgement carries every changed root revision; one local transaction installs those acknowledgements and rebases the remaining pending tail. Folder/document create→move→edit dependencies wait for their predecessor receipts. A conflict preserves the original payload and pending graph. Do not rewrite a pending structural operation into a full NotesDocument upload; that would bypass the Cloud owner locks and classification rules.

Slate local stores preserve all fields of slate.project.v1: independent bins; sequence grid/audio/colour configuration; track role/name/lock; item kind and typed source; graph nodes/edges and effect definition/instance identity; exact keyframe scope; title/subtitle style/text; managed small assets and immutable transcript provenance. Nested sequences add a same-project FK and cycle check. Project archive and metadata replica use the same complete projection, excluding device paths, cache/proxy bytes and transient editor UI. A graph and its effect-stack view have one stored authority. Unknown effect definitions remain inert bytes within the versioned graph, bounded by the existing immutable body channel when oversized, rather than being discarded by a narrower DTO.

## Client recovery generation

Per-realm session/cache metadata records recoveryGeneration; each outgoing command/outbox lineage captures it at creation. A generation change atomically stops dispatch and moves old entries to recoveryQuarantine while preserving payload, old IDs/revisions/hashes and attachments. Bootstrap starts new cursor state. Review/reapply produces a new command with the current generation and current owner precondition, retaining provenance to the quarantined item. Quarantine has no automatic expiry that deletes pending user content. A local native command unrelated to Cloud remains governed by its native store and is not rewritten by a realm restore.
