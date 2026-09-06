# Derived Stores

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture · Data model
> Governing authority: [`00-data-model-overview.md`](00-data-model-overview.md) `§4`, `§8`
> Companions: [`../09-ai-and-agent-runtime-architecture.md`](../09-ai-and-agent-runtime-architecture.md) `§5`, [`../06-data-persistence-and-formats.md`](../06-data-persistence-and-formats.md)

Every store here is **reconstructable from canonical data**. Deleting all of them leaves every product fully functional and loses no user content (`QI-10`). That property is what makes them safe to evict under storage pressure, safe to rebuild after a schema change, and safe to exclude from backup.

---

## 1. The contract every derived store obeys

| # | Rule |
|---|---|
| DS-01 | **A derived row records its source identity and source revision.** Without those, staleness is undetectable and a rebuild cannot be incremental. |
| DS-02 | **A derived store lives in a separate file or schema from canonical data**, so deletion is a single operation that cannot damage authority. |
| DS-03 | **A derived store is never the only copy of anything** (`XS-06`). |
| DS-04 | **A derived store never syncs as authority.** It may be transported as a convenience, but the receiving device treats it as a cache with its own validity check. |
| DS-05 | **A rebuild is always available and always correct.** "Rebuild produces a different answer" is a defect, not a refresh (`WP-19.00`). |
| DS-06 | **Update follows the write path.** A derived store updated outside the commit unit will diverge on crash; every one here is updated from the journal or the change feed, not from a caller. |
| DS-07 | **Eviction is permitted at any time.** Nothing may hold a derived row's continued existence as an invariant. |

---

## 2. Local search index

The lexical index over each product's content. **Works with no cloud and no account** (`BR-01` of `WP-19`).

### `search_document`

| Field | Type | Notes |
|---|---|---|
| `search_doc_id` | `id` | **PK** |
| `source_kind`, `source_id` | `text NN`, `id NN` | The canonical aggregate |
| `source_rev` | `rev NN` | **The staleness check** (`DS-01`) |
| `workspace_scope` | `id?` | For permission filtering |
| `title` | `text NN` | |
| `body` | `text NN` | Extracted plain text |
| `indexed_at` | `instant NN` | |

- `UQ (source_kind, source_id)`
- Full-text index over `title` and `body`, with the tokeniser and stemming configuration recorded in `sys_meta` so a configuration change forces a rebuild rather than producing silently mixed results

### `search_anchor`

| Field | Type | Notes |
|---|---|---|
| `anchor_id` | `id` | **PK** |
| `search_doc_id` | `id NN` | `FK →`; cascade |
| `block_id` | `id?` | The precise location |
| `offset_start`, `offset_end` | `int NN` | Character range within the block |
| `content_fingerprint` | `text NN` | **Hash of the anchored text** |

- **This is the citation anchor** (`WP-19.02`). Resolution compares `content_fingerprint` against the current content: a match resolves exactly; a mismatch reports **invalid explicitly** rather than drifting to a nearby location.
- `IX (search_doc_id, offset_start)`

### Update and rebuild

| # | Rule |
|---|---|
| SI-01 | **The index updates from the journal**, not from the editor. A crash mid-update leaves the journal ahead of the index, and the next start replays the difference — so divergence is impossible rather than unlikely (`WP-19.00`). |
| SI-02 | **A full rebuild scans canonical content in aggregate order** and produces an index equivalent to the incremental one. Equivalence is asserted, not assumed. |
| SI-03 | **Permission is applied at query evaluation**, so a refused document affects neither results nor counts (`WP-19.01`). The index does not store a permission decision, because permission can change without the content changing. |

---

## 3. Retrieval index (semantic)

Separate from lexical search, and subject to the **same permission and scope rules as its source** (`WP-40.01`).

### `retrieval_chunk`

| Field | Type | Notes |
|---|---|---|
| `chunk_id` | `id` | **PK** |
| `source_kind`, `source_id`, `source_rev` | as above | |
| `anchor_id` | `id?` | Links back to a citation anchor |
| `chunk_ordinal` | `int NN` | |
| `text` | `text NN` | |
| `embedding_model_id` | `text NN` | **Part of the staleness key** |
| `embedding` | `vector NN` | |
| `embedded_at` | `instant NN` | |

- `IX (source_kind, source_id, source_rev)` — incremental invalidation
- Vector index over `embedding`, configured per store
- **Constraint** — changing `embedding_model_id` invalidates every chunk produced by the old model. Mixing embeddings from two models in one similarity search is a correctness defect, and the model identifier is part of the query filter, not merely metadata.
- **Constraint** — **vector retrieval is a replaceable module** and never bleeds into the canonical document model (`PS-08`, `IX-10`)

### Cache isolation

| # | Rule |
|---|---|
| RI-01 | **Retrieval cache keys include the workspace and the principal** (`CA-05`). No cache entry is reused across principals or scopes (`WP-40.05`). |
| RI-02 | **Only genuinely public content may be cached across workspaces**, and "public" is a recorded classification, not an inference. |
| RI-03 | **Enabling AI never uploads local-only content** (`I-182`). The retrieval index for local-only content is local, and no path exports it. |

---

## 4. Product-specific derived stores

| Store | Product | Source | Invalidated by | Rebuild cost |
|---|---|---|---|---|
| `link_index` | ArcNotes | `document_link` | Any link change | Cheap — a scan of link rows |
| `backlink_projection` | ArcNotes | `link_index` | Same | Cheap |
| `property_index` | ArcNotes | `property_value` | Property or definition change | Moderate |
| `view_result_cache` | ArcNotes | Query + content | Any content change in scope | Cheap; often not worth caching |
| `outline_projection` | ArcNotes | Block structure | Document revision | Cheap |
| `waveform_cache` | ArcSlate, ArcScope | Audio source | Source content hash | Expensive — background |
| `thumbnail_cache` | ArcSlate, ArcNotes | Media/attachment | Source content hash | Moderate |
| `proxy_representation` | ArcSlate | `media_asset` | Source content hash, proxy policy | **Very expensive** — background, resumable |
| `render_cache` | ArcSlate | Sequence + processing graph | Any revision in the evaluated range | Very expensive |
| `analysis_result` | ArcScope | Capture + definition version + config | Any of the three | Expensive |
| `decoded_event_index` | ArcScope | Capture + decoder version | Either | Expensive |
| `task_projection` | ArcChat, all | Authoritative task store | Authoritative revision | Cheap |
| `capability_registry_cache` | ArcChat | Live registrations | Registration change | Cheap; rebuilt on Hub restart |

| # | Rule |
|---|---|
| PD-01 | **A proxy is not a render cache** (`I-484`). A proxy is a cheaper source decode; a render cache is a stored result of timeline processing. They have different invalidation triggers and different lifetimes, and conflating them produces wrong output. |
| PD-02 | **Analysis results record all five reproducibility inputs** — session, capture, configuration snapshot, decoder version and configuration, analysis definition and version (`LB-04`). A result missing any of them cannot be trusted and is treated as absent. |
| PD-03 | **An expensive rebuild is resumable and cancellable**, and runs as a Task so its progress and failure are visible like any other long operation. |

---

## 5. Cloud derived stores

### `search.search_document`, `search.retrieval_chunk`

Same shape as the local stores, scoped by `workspace_id`, populated from the change feed rather than a journal. **Entitlement-gated**: cloud search is a paid capability, and its absence never affects local search (`WP-40.06`).

### `entitlement.snapshot`

Listed here as well as in the cloud data model because it is genuinely derived: **rebuilding from grants and revocations must equal the stored row** (`EN-02`), and the rebuild is the test.

### `policy.rollout_assignment`

Deterministic per installation, so it is **recomputable rather than stored**. Where stored, the row carries the rule version it came from, and a rule change invalidates it. This is what makes rollout stable across restarts without a durable assignment table being load-bearing (`WP-44.03`).

---

## 6. Storage pressure and eviction

| # | Rule |
|---|---|
| EV-01 | **Eviction touches only derived stores** (`WP-07.06`). Canonical data is never evicted, at any pressure. |
| EV-02 | **Eviction order is by rebuild cost ascending and last-use ascending** — cheap and cold first. |
| EV-03 | **Storage pressure is a visible product state**, with what is consuming space and what may be safely reclaimed (`§14` of the data requirements). |
| EV-04 | **An evicted derived store rebuilds on demand**, and the product remains usable while it does — degraded, not broken. |
| EV-05 | **A derived store never counts against a user's cloud storage quota** (`QA-03`), because it is not user content. |

---

## 7. Verification

| # | Obligation | Where |
|---|---|---|
| DR-01 | Deleting every derived store leaves each product fully functional with no content loss | `WP-07.06`, `WP-37.05` |
| DR-02 | A full rebuild produces a state equivalent to the incremental one, for every store | `WP-19.00`, `WP-40.01` |
| DR-03 | A crash mid-update leaves the index recoverable from the journal, with no divergence | `WP-19.00` |
| DR-04 | A citation anchor resolves exactly or reports invalidity — never drifts | `WP-19.02` |
| DR-05 | No retrieval cache entry is reused across principals or scopes | `WP-40.05` |
| DR-06 | Changing the embedding model invalidates every chunk from the previous model | `WP-40.01` |
| DR-07 | Render output is identical with proxies enabled and disabled | `WP-37.05` |
| DR-08 | Eviction under pressure never removes canonical data | `WP-07.06` |
