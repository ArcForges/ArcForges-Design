# Desktop Local Data Model

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Data model
> Governing authority: [`00-data-model-overview.md`](00-data-model-overview.md), [`../06-data-persistence-and-formats.md`](../06-data-persistence-and-formats.md)
> Companions: [`../04-desktop-application-architecture.md`](../04-desktop-application-architecture.md), [`../07-sync-conflict-and-backup.md`](../07-sync-conflict-and-backup.md)

Each desktop product owns its own local store. The store is **authoritative** for that product's content (`§4` of the overview); Cloud holds a replica when a sync scope is enabled.

**Store technology.** An embedded relational store with an AOT-safe access path (`CS-01`). Journaling is enabled only after per-platform and per-filesystem validation (`CS-04`), because network volumes, removable media and container filesystems each break different assumptions.

---

## 1. What every product store contains

Five table groups are identical in shape across all four products. They are specified once here and referenced, not repeated.

### 1.1 `sys_meta`

| Field | Type | Notes |
|---|---|---|
| `key` | `text` | **PK** |
| `value` | `text NN` | |

Holds `storageSchemaVersion`, `nativeFormatVersion`, `installationId`, `lastCleanShutdownAt`, `lastRecoveryOutcome`. **`storageSchemaVersion` equals the highest applied migration** (`SE-06`).

### 1.2 `command_log`

The local half of `TX-01`–`TX-06`.

| Field | Type | Notes |
|---|---|---|
| `command_id` | `id` | **PK** |
| `operation` | `text NN` | |
| `request_hash` | `text NN` | |
| `status` | `enum(inProgress, succeeded, failed) NN` | |
| `result_rev` | `rev?` | |
| `error_code` | `text?` | |
| `created_at`, `expires_at` | `instant NN` | |

- `IX (expires_at)`
- **Constraint** — written **in the same transaction as its effect**. This is what makes a retried local RPC call idempotent (`WP-14.03`).

### 1.3 `journal`

| Field | Type | Notes |
|---|---|---|
| `journal_seq` | `bigint` | **PK**, monotonic |
| `aggregate_kind`, `aggregate_id` | `text NN`, `id NN` | |
| `aggregate_rev` | `rev NN` | Revision after the change |
| `command_id` | `id NN` | |
| `payload` | `json NN` | Enough to replay |
| `committed_at` | `instant NN` | |

- `IX (aggregate_kind, aggregate_id, journal_seq)` — per-aggregate replay
- **Constraint** — the journal entry is durable **before** the commit is acknowledged (`WP-07.01`). This is the difference between crash-free and recoverable (`QI-08`).
- **Truncation** — safe under concurrent read, bounded by snapshot policy

### 1.4 `sync_outbox`

| Field | Type | Notes |
|---|---|---|
| `outbox_id` | `id` | **PK** |
| `aggregate_kind`, `aggregate_id` | `text NN`, `id NN` | |
| `aggregate_rev` | `rev NN` | |
| `change_kind` | `enum(upsert, tombstone) NN` | |
| `command_id` | `id NN` | Carried to the server for idempotency |
| `state` | `enum(pending, sending, sent, failed) NN` | |
| `attempts` | `int NN` | |
| `created_at`, `next_attempt_at` | `instant NN` | |

- `IX (state, next_attempt_at)`
- **Constraint** — written in the business transaction (`§2.1` of the persistence architecture); survives process termination (`WP-25.01`)

**`I-498` — an evictable acknowledged cache is not an unacknowledged edit.** This is the distinction that decides whether a user loses work, so it is a schema property rather than a convention.

| # | Rule |
|---|---|
| PE-01 | **Cloud is authoritative for acknowledged revisions of synchronised data** (`§5` of the product scope). The local store holds a **working cache** of what Cloud has acknowledged, plus **durable pending changes** that it has not. |
| PE-02 | **A row is evictable only if every change to it has been acknowledged.** Eviction is gated on `NOT EXISTS (SELECT 1 FROM sync_outbox WHERE aggregate_id = ? AND state <> 'sent')`, and on the absence of a pending upload or an unreturned tool receipt. |
| PE-03 | **Cache pressure, sign-out, account switch, subscription restriction and workspace change never discard an unacknowledged change** (`C-06`). Each of these paths runs the same eviction gate; none has a shortcut. |
| PE-04 | **A durable local save is never presented as saved to Cloud** (`§3.1` of the product scope). The UI distinguishes *saved on this device* from *acknowledged by Cloud*, and the outbox row is what makes the difference queryable. |
| PE-05 | **Pending work survives reinstall-level recovery.** The outbox, the journal and staged upload content are in the durable store, not in a cache directory that a cleanup tool may remove. |
| PE-06 | **An acknowledged revision that is evicted is re-fetchable; an unacknowledged change that is lost is gone.** That asymmetry is why `PE-02` is a constraint and not a heuristic.

### 1.5 `local_audit`

Append-only, separate from telemetry (`OA-06`), holding local security-relevant events: capability grant and revocation, approval decision, secret use, egress authorisation, local presence proof.

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
- **Constraint** — `resource_id` is **never a file path** (`I-192`), and a `ResourceRef` crossing a boundary carries identity and metadata only (`BF-08`)

`resource_reference` is `(resource_id, referrer_kind, referrer_id)` as a composite primary key. **Reference count derives from it** so a crash between reference and store is recoverable.

---

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
- **Constraint** — branching **shares prior history by reference, never by copy** (`WP-15.01`). Messages before the branch point belong to the parent branch and are read through it; there is no duplication.

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
- **Constraint** — a committed message is **immutable**; an edit creates a new row (`WP-15.00`)
- **Constraint** — a row is written with `state = complete` **only** when the stream finished. An interrupted stream is stored as `interrupted`, never as complete (`WP-15.00`) — this is why `state` exists rather than a nullable completion timestamp.

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
| `availability` | `enum(available, unavailable, checking) NN` | A visible state, not an error (`WP-15.02`) |
| `display_name` | `text NN` | |

- **Constraint** — `mode = managed` ⟺ `resource_id` is not null; `mode = externalReference` ⟺ `external_locator` is not null. A check constraint enforces the discriminated union.
- **Constraint** — **no attachment body is ever stored in `message_part.payload`** (`WP-15.02`), asserted by a size limit on the column and a policy test.

### `arcchat_project`, `agent_profile`, `skill`

`arcchat_project` groups conversations with its own instructions and context references. `agent_profile` bundles model choice, mode and behaviour, versioned so a historical run records the version it used. `skill` is versioned declarative guidance: **a skill grants no capability** (`WP-15.04`), so there is no permission column on it, and `skill_version` rows are immutable so a skill update never alters a historical result.

### `context_reference`

| Field | Type | Notes |
|---|---|---|
| `context_ref_id` | `id` | **PK** |
| `scope_kind` | `enum(pinned, project, temporary) NN` | |
| `owner_kind`, `owner_id` | `text NN`, `id NN` | Conversation or project |
| `target_product` | `text NN` | |
| `target_ref` | `json NN` | A `ResourceRef` or a product-specific selector |
| `added_at` | `instant NN` | |

- **Rule** — **there is no ambient default scope** (`CA-01`). Absence of rows means absence of context.

### `task_projection`

The local read projection of tasks whose authority is elsewhere (`TO-07`): carries `task_id`, `authoritative_rev`, state, reason facet, and `projected_at`. **Stamped with the authoritative revision**, so staleness is detectable.

---

## 3. ArcNotes local store

### `notebook`, `document` *(aggregate roots)*

| `document` field | Type | Notes |
|---|---|---|
| `document_id` | `id` | **PK** |
| `notebook_id` | `id NN` | `FK →` `notebook`; restrict |
| `title` | `text NN` | **An independent field, not the first heading block** (`DC-03`) |
| `state` | `enum(active, trashed) NN` | |
| `trashed_at` | `instant?` | |
| `created_at`, `updated_at` | `instant NN` | |
| `rev` | `rev NN` | |

- `IX (notebook_id, state, updated_at)`
- `IX (state, updated_at)` — the global recent list
- **Partial index** on `state = active` for every list path (`QP-05`), so a forgotten predicate cannot leak trashed content

### `block`

| Field | Type | Notes |
|---|---|---|
| `block_id` | `id` | **PK** — stable across reorder and reparent (`WP-18.00`) |
| `document_id` | `id NN` | `FK →`; cascade |
| `parent_block_id` | `id?` | Null at document root |
| `ordinal` | `text NN` | **A fractional order key**, not an integer |
| `kind` | `text NN` | Exactly the `BL-04` V1 set: `paragraph`, `heading`, `list`, `quote`, `callout`, `code`, `divider`, `table`, `math`, `image`, `attachment`, `embed`, `toggle`. **Checklist is a `list` style and PDF is an `attachment` presentation** — neither is a separate kind (`§2.1` of the editing architecture) |
| `content` | `json NN` | The kind's declared content shape; text-bearing kinds carry `InlineContent` (`§2` of the [editing architecture](../18-editing-and-rich-content.md)) |
| `created_at` | `instant NN` | |

- `UQ (document_id, parent_block_id, ordinal)`
- `IX (document_id, parent_block_id, ordinal)` — the document read path, in document order
- **Constraint** — a block carries **no revision of its own** (`RV-03`); the document's revision governs
- **Why a fractional order key** — inserting between two blocks must not renumber siblings, because renumbering would make every insert a whole-document write and would defeat sync's per-aggregate change detection. The key is a string with a defined mid-point algorithm and a rebalance operation that is itself a normal revision.

### `document_link`, `link_index`

| `document_link` field | Type | Notes |
|---|---|---|
| `link_id` | `id` | **PK** |
| `source_document_id` | `id NN` | `FK →`; cascade |
| `source_block_id` | `id?` | |
| `target_kind` | `enum(document, block, external) NN` | |
| `target_document_id`, `target_block_id` | `id?` | **Identity, never a title** (`BR-04` of `WP-18`) |
| `display_alias` | `text?` | |
| `state` | `enum(resolved, broken) NN` | An explicit state, never a silent failure |

- `IX (target_document_id)` — **the backlink query path**
- **Rule** — `link_index` is *(derived)*: the backlink panel reads it, and **backlinks are never written into block content** (`WP-18.02`). Deleting the index rebuilds it.

### `tag`, `document_tag`

`tag` is cross-cutting classification carrying **no hierarchical position**. `document_tag` is `(document_id, tag_id)`. **Deleting a tag deletes the `document_tag` rows and nothing else** — documents survive (`BR-07` of `WP-18`), enforced by the foreign key direction.

### `property_definition`, `property_value`

| `property_definition` field | Type | Notes |
|---|---|---|
| `property_def_id` | `id` | **PK** |
| `key` | `text NN` | |
| `owner` | `enum(system, user) NN` | Separated, never conflated (`WP-28.00`) |
| `type` | `enum(text, number, date, select, multiSelect, checkbox, relation, derived) NN` | |
| `config` | `json NN` | Options, precision, relation target |
| `rev` | `rev NN` | |

`property_value` is `(document_id, property_def_id)` with a typed value column set per type. **A document with no property rows has no property overhead** — this is what makes `WP-28.04`'s lightness requirement structural rather than a UI choice.

- `IX (property_def_id, value_text)`, `IX (property_def_id, value_number)`, `IX (property_def_id, value_date)` — the query-and-view paths

### `saved_view`

`saved_view` is a saved query plus its configuration and view kind. **It owns no documents**, so its deletion cascades to nothing.

| Field | Type | Notes |
|---|---|---|
| `saved_view_id` | `id` | **PK** |
| `notebook_id` | `id?` | Scope; null means workspace-wide |
| `kind` | `enum(list, table) NN` | **Exactly two layouts** (`P2-006`). Board, gallery, calendar and timeline layouts are excluded |
| `filter` | `json NN` | Property predicates over the bounded scalar types of `§2.1` of the editing architecture |
| `sort` | `json NN` | Ordered sort keys |
| `columns` | `json?` | Table layout only |
| `rev` | `rev NN` | |

- **Constraint** — a filter references only **declared property definitions with scalar types**. There is no formula, relation or rollup evaluator (`P2-006`), and no expression language enters this column
- **Rule** — a view is a **query, never a container**. Deleting a view deletes no document; a document appears in a view because it matches, not because it was added

> **Retired identifiers.** `canvas`, `canvas_element`, `slide_deck`, `slide` and `speaker_note` are **retired by P2-006** and are not reused. Edgeless canvas, whiteboard surfaces, shapes, connectors, frames and presentations are excluded from delivery, with no mandatory future hook. Their historical definitions are in the git history of this document at `7ed79a6`.

### `document_history`, `checkpoint`, `trash_entry`

Three distinct mechanisms plus the journal make four (`QI-09`):

| Mechanism | Table | Scope | Retention |
|---|---|---|---|
| Undo | *in-memory session stack, not persisted* | Session | Session |
| History | `document_history` | Per document, per revision | Policy window |
| Checkpoint | `checkpoint` | Explicit user act | Until deleted |
| Journal | `journal` (§1.3) | Crash recovery | Until snapshot |

**None substitutes for another**, and a test asserts each behaves independently (`WP-18.05`).

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

- **Constraint** — **immutable once written**. Editing a `connection_profile` never rewrites a historical snapshot (`SD-05`). This is the row that makes a capture evidentially meaningful.

### `capture`, `capture_segment`, `gap`

| `capture` field | Type | Notes |
|---|---|---|
| `capture_id` | `id` | **PK** |
| `session_id` | `id NN` | `FK →`; restrict |
| `state` | `enum(armed, running, paused, stopped, finalized, interrupted) NN` | |
| `finalized_at` | `instant?` | |
| `end_marker` | `enum(clean, truncatedAtBoundary, truncatedMidChunk)?` | The **honest end marker** (`AQ-09`) |
| `recorded_loss` | `json?` | Counts and time ranges of loss |
| `store_root` | `text NN` | The chunked store location |

- **Constraint** — once `state = finalized`, **the row and its chunked data are immutable** (`SE-12`). A trigger or repository guard refuses any update, and a test asserts it.
- `capture_segment` records contiguous runs; `gap` records explicit interruptions with cause and duration. **A disconnect produces a gap row, never a silently shortened capture** (`AQ-08`).

### The chunked capture store

Raw capture is **not** in the relational store (`SE-14`). It is a chunked append store on disk:

| Element | Content |
|---|---|
| Chunk file | Fixed-size frames plus a per-chunk checksum |
| Chunk index | `(capture_id, chunk_ordinal) → offset, sample range, time range, checksum` |
| End marker | Written on finalisation; its absence means the capture was interrupted |

- **Recovery** — on start, an unfinalised capture is verified chunk by chunk; the verifiable prefix is retained and the loss is recorded (`WP-07.05`, `AQ-09`)
- **Constraint** — **no third-party extension has a write path to this store** (`EP-01`, `WP-35.05`)

### `channel`, `signal`, `event_record`, `analysis_definition`, `analysis_result`, `annotation`, `finding`, `report`

`analysis_result` is *(derived)*: **deleting every result and rebuilding produces identical output** (`WP-34.04`), so each row records its `analysis_definition_version`, its `decoder_version`, its input capture and range, and its configuration snapshot — the five things `LB-04` requires for reproducibility. `annotation` and `finding` are **authored content with their own identity and history**, and are **never written into raw capture** (`WP-34.05`).

---

## 5. ArcSlate local store

### `slate_project`, `sequence` *(aggregate roots)*

| `sequence` field | Type | Notes |
|---|---|---|
| `sequence_id` | `id` | **PK** |
| `project_id` | `id NN` | `FK →`; cascade |
| `frame_rate_num`, `frame_rate_den` | `int NN` | The source's **own** rate. Rational, stored exactly (`TM-03`) — never a float, and never assumed equal to the sequence's (`SM-01`) |
| `pts_time_base_num`, `pts_time_base_den` | `int NN` | The container's PTS base, recorded because it is generally neither rate (`SM-01`) |
| `ticks_per_source_unit` | `bigint?` | The exact tick mapping where the source base divides the tick base; **NULL means the mapping rounds**, and the rounding is in the conform report (`SM-03`) |
| `drop_frame` | `bool NN` | |
| `sample_rate` | `int NN` | |
| `width`, `height` | `int NN` | |
| `working_color_config` | `json NN` | |
| `rev` | `rev NN` | |

- **Constraint** — a frame rate is **never** stored as a floating-point value. This single decision is what prevents accumulated drift (`WP-36.01`), and a policy test asserts no float column exists in the time model.

### `media_asset`, `media_stream`

| `media_asset` field | Type | Notes |
|---|---|---|
| `media_asset_id` | `id` | **PK** — a stable logical identity |
| `project_id` | `id NN` | |
| `mode` | `enum(externalReference, managed) NN` | Reference-in-place by default (`MD-03`) |
| `content_hash` | `text?` | Present when managed or once hashed |
| `availability` | `enum(available, offline, checking) NN` | **A normal state, not an error** (`MD-05`) |
| `metadata` | `json NN` | Streams, codecs, dimensions, rate, duration, colour metadata, timecode, channel layout |
| `color_interpretation_override` | `json?` | **Never modifies the source** (`CO-03`) |

- **Constraint** — `media_asset_id` is **not a file path** (`I-192`), and **a clip never references a file** (`MD-07`)
- `media_location` is a separate table keyed `(media_asset_id, device_id)` — **the same asset may resolve to different locations on different devices** (`MD-08`) while remaining one logical asset. This table is device-local and does not sync.

### `track`, `timeline_item`, `clip`, `transition`

> **Corrected 2026-09-07.** Positions were stored as integer frames with a **parallel integer sample column set**. Those two grids cannot agree: at 30000/1001 fps and 48 kHz one frame is 1601.6 samples, so most frame positions have no integer sample and most sample positions have no integer frame. Storing both made the model self-contradictory. Positions are now **canonical ticks** (`§3` of the [time model](../23-simulator-and-interchange.md)); frames and samples are computed projections.

| `timeline_item` field | Type | Notes |
|---|---|---|
| `timeline_item_id` | `id` | **PK** |
| `sequence_id`, `track_id` | `id NN` | `FK →`; cascade |
| `kind` | `enum(clip, transition, gap, generatedMedia, title, subtitleCue) NN` | |
| `start_ticks` | `bigint NN` | **Canonical ticks at 705 600 000 Hz** (`TB-01`) |
| `duration_ticks` | `bigint NN` | |
| `media_asset_id` | `id?` | Clips only |
| `source_in_ticks`, `source_out_ticks` | `bigint?` | In the **source's** canonical tick domain, mapped by conform (`SM-02`) |

- `IX (sequence_id, track_id, start_ticks)` — **the timeline read path**
- **Constraint** — many timeline items may reference one `media_asset` independently (`I-477`); there is no back-reference from asset to clip
- **Constraint** — **no position column is a frame number, a sample index, a float or a duration type** (`TB-01`, `TB-04`), asserted by a repository policy test (`TV-02`)
- **Constraint** — `duration_ticks > 0`; a zero-length item is not representable
- **Rule** — the sequence's frame rate and the project's audio rate are **projection parameters**, not storage units. Changing a sequence's frame rate reprojects the display without altering a single stored position, which is what makes a rate change non-destructive.

### `effect_instance`, `effect_parameter`, `keyframe`, `animation_curve`

`effect_instance` references an `effect_definition_id` from a catalogue — **definition and instance are separate** (`I-483`, `WP-37.03`). `keyframe` carries `scope ∈ {clipLocal, sequence}` **explicitly**, so keyframe time can never silently switch domain when a clip moves (`PG-09` of the ArcSlate requirements).

### Derived stores — proxy, render cache, waveform, thumbnail

All four are *(derived)*, in a **separate store file** from the project, so `WP-37.05`'s "delete every cache and the project is intact" is structurally true rather than a promise. Each row records the source asset, the source content hash and the generation parameters, so a stale entry is detectable. **Switching proxy on or off never changes render output** (`MP-06`) because the render path resolves the original unless proxy render is explicitly declared on the `render_request`.

### `export_preset`, `render_request`

| `render_request` field | Type | Notes |
|---|---|---|
| `render_request_id` | `id` | **PK** |
| `sequence_id` | `id NN` | |
| `bound_project_rev`, `bound_sequence_rev` | `rev NN` | **The immutable snapshot binding** (`RN-04`) |
| `range_start_ticks`, `range_end_ticks` | `bigint NN` | **Canonical ticks** (`TB-01`). The encoder's own grid is a projection with directional rounding (`TG-05`) |
| `export_preset_id` | `id NN` | |
| `allow_proxy_render` | `bool NN` | Explicit, recorded in output metadata |
| `job_id` | `id NN` | A render is a **native Product Job**, not a Cloud Agent Task (`CM-04` of the runtime architecture, `I-485`). ArcSlate owns its progress, cancellation and recovery |
| `destination` | `text NN` | |

- **Constraint** — the render reads the bound revisions, never live editor state. Editing during a render cannot affect its output (`WP-38.02`).

---

## 6. The portable package

The working store is not the exchange format (`§8` of the persistence architecture). A portable package is a directory or archive containing:

```
manifest.json          format version, product, created-by, content inventory with hashes
content/               canonical serialised aggregates, one file per aggregate root
resources/             managed resources by content hash
attachments-external/  external reference descriptors, never the files themselves
```

| # | Rule |
|---|---|
| PP-01 | **The package is complete**: re-importing reconstructs every aggregate, relationship and managed resource (`WP-19.05`). |
| PP-02 | **Serialisation is deterministic** — stable ordering, stable key order, no timestamps outside content. Two exports of unchanged content are byte-identical (`WP-19.06`). |
| PP-03 | **Derived data is excluded.** No index, cache, proxy or thumbnail enters a package. |
| PP-04 | **External references are exported as descriptors**, and collect/consolidate is the separate explicit operation that turns them into managed content (`WP-39.02`). |
| PP-05 | **The manifest carries `nativeFormatVersion`**, distinct from `storageSchemaVersion` — a version axis of its own. |

---

## 7. Verification

| # | Obligation | Where |
|---|---|---|
| DL-01 | Every aggregate round-trips with all fields and relationships | Per-product persistence tests |
| DL-02 | Block order survives insert-between without renumbering siblings | `WP-18.00` |
| DL-03 | A finalised capture is structurally immutable | `WP-33.04` |
| DL-04 | No floating-point column exists in the ArcSlate time model | `WP-36.01` policy test |
| DL-05 | Deleting every derived store leaves each product fully intact | `WP-07.06`, `WP-37.05` |
| DL-06 | Undo, history, checkpoint and journal behave independently | `WP-18.05` |
| DL-07 | The portable package round-trips with equivalence, deterministically | `WP-19.05`, `WP-19.06` |
| DL-08 | A partial index prevents a trashed row from appearing in any list path | `WP-18.00` |
| DL-09 | A crash at any write-path point recovers to a committed boundary | `WP-07.02` |
