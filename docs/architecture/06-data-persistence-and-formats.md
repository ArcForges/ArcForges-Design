# Data Persistence and Formats

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Companions: [`../requirements/13-data-formats-and-portability.md`](../requirements/13-data-formats-and-portability.md), [`07-sync-conflict-and-backup.md`](07-sync-conflict-and-backup.md), [`04-desktop-application-architecture.md`](04-desktop-application-architecture.md)

The mechanics behind the local data constitution: how the five layers are actually stored, versioned, migrated and recovered.

---

## 1. Store composition

Every product's local store is composed from the same seven parts, sized differently per product:

| Part | Nature | Loss consequence |
|---|---|---|
| **Canonical Structured Store** | Transactional, durable | **Unacceptable** — this is the user's work |
| **Revision / Recovery Store** | Append-oriented, durable | Recovery capability lost |
| **Managed Resource Store** | Content-addressed, immutable blobs | User assets lost |
| **External Resource References** | Metadata only | Links break; user files untouched |
| **Large Append Store** | Chunked, verifiable | Capture evidence lost |
| **Derived Store** | Rebuildable | **Acceptable** — rebuild |
| **Device-local State** | Rebuildable, per device | Acceptable — reset to defaults |

| # | Rule |
|---|---|
| SC-01 | **Each product owns its own store** ([P-09](../requirements/00-product-scope-and-portfolio.md#rule-p-09)). A shared cross-product database file is prohibited. |
| SC-02 | **Only the owning product writes its own store.** Even read-only direct access from another product is prohibited ([OW-02](../requirements/13-data-formats-and-portability.md#rule-ow-02) in the data requirements). |
| SC-03 | **Canonical and derived stores are physically separable**, so a derived store can be deleted wholesale without touching canonical data. |
| SC-04 | **User documents and cache directories are separate**, and the cache location is independently relocatable ([SL-03](../requirements/13-data-formats-and-portability.md#rule-sl-03) there). |
| SC-05 | **The store layout carries a `StorageSchemaVersion`** at the store level, not only per table. |

---

## 2. Canonical structured store

| # | Rule |
|---|---|
| <a id="rule-cs-01"></a>CS-01 | **An AOT-safe data access path with explicit or generated mapping.** A reflection-driven ORM runtime is not an irreplaceable dependency of an AOT host (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**). |
| CS-02 | **Connection and transaction lifetime follow the unit of work.** No global singleton connection. |
| <a id="rule-cs-03"></a>CS-03 | **Write transactions are short**, so a long user operation never holds a transaction open. |
| <a id="rule-cs-04"></a>CS-04 | **Journaling mode is enabled only after platform and file-system validation** — including network volumes, removable media and container filesystems. |
| CS-05 | **Authoritative aggregates carry an owner-assigned revision.** Pending Notes projections use the composite local token in the desktop data model; native Scope/Slate content uses its own content revision. Journal and derived-index source versions must match the body they describe. |
| CS-06 | **Soft deletion uses an explicit state plus a tombstone**, never a physical row removal, wherever sync or recovery depends on it. |
| <a id="rule-cs-07"></a>CS-07 | **Every table has explicit indexes for its known query paths**, and query plans are reviewed at the scale corpus, not at toy sizes. |
| CS-08 | **Serializers and mappers are statically generated or explicitly registered.** Runtime entity scanning is prohibited. |

### 2.1 The commit unit

A single atomic write contains: the state change, the command record (for idempotency), the journal entry, the revision increment, and the sync outbox entry where the object participates in sync. **Reporting success before this unit is durable is prohibited.**

---

## 3. Journal and snapshot

```
Command accepted
 → validate identity, permission, capability version
 → check CommandId (already executed → return the prior result)
 → check ExpectedRevision
 → enforce domain rules
 → BEGIN
     write state change
     write command record
     write journal entry
     increment revision
     write sync outbox entry (if applicable)
   COMMIT + flush
 → publish in-process notification
 → return new revision + minimal delta
```

| # | Rule |
|---|---|
| JS-01 | **A journal entry records**: sequence, `CommandId`, previous and new **typed source version**, command type and version, payload or a durable reference, checksum, actor, correlation, causation, commit time. |
| JS-02 | **The journal is the recovery mechanism, not user-facing history** ([UR-04](../requirements/13-data-formats-and-portability.md#rule-ur-04) in the data requirements). |
| JS-03 | **Snapshots are triggered by command count, elapsed time and size**, and carry a schema version and a checksum. |
| JS-04 | **Snapshot writing is temporary-file, flush, atomic-replace**, with at least one verified previous generation retained. |
| JS-05 | **Caches never enter a critical snapshot.** |
| JS-06 | **Recovery replays the journal from the most recent valid snapshot** and stops at the last verifiably committed entry. |
| JS-07 | **A corrupt journal tail is truncated at the last valid entry, and the truncation is reported** — never silently absorbed. |

---

## 4. Managed resource store

| # | Rule |
|---|---|
| MR-01 | **Managed blobs are immutable and content-identified**: `BlobId`, content hash, length. Editing produces a new blob; the referencing revision changes which blob it points at ([BL-01](../requirements/03-cloud-services-and-sync.md#rule-bl-01) in the cloud requirements). |
| MR-02 | **The integrity hash is a standard cross-platform hash (SHA-256).** A faster internal fingerprint may exist for change detection; the published integrity check uses the standard hash ([BL-04](../requirements/03-cloud-services-and-sync.md#rule-bl-04) there). |
| MR-03 | **A blob key never exposes a user filename** ([BL-03](../requirements/03-cloud-services-and-sync.md#rule-bl-03) there). The filename lives in domain metadata. |
| MR-04 | **A blob is referenced, never inlined.** Base64 embedding into canonical content is prohibited ([I-463](../requirements/01-normative-glossary-and-invariants.md#rule-i-463)). |
| MR-05 | **Reference counting or reachability analysis governs blob lifetime**, and garbage collection removes only unreferenced managed data ([DL-03](../requirements/13-data-formats-and-portability.md#rule-dl-03) there). |
| MR-06 | **Download and import verify hash and length before content reaches the application** ([BL-11](../requirements/03-cloud-services-and-sync.md#rule-bl-11) there). |
| MR-07 | **A background integrity audit samples blobs and verifies checksums** ([BL-12](../requirements/03-cloud-services-and-sync.md#rule-bl-12) there). |

---

## 5. Large append store

For ArcScope raw capture and comparable high-rate append-only data.

| # | Rule |
|---|---|
| LA-01 | **Chunked storage with per-chunk verification**, not database blobs ([LD-01](../requirements/13-data-formats-and-portability.md#rule-ld-01) in the data requirements). |
| LA-02 | **A segment manifest maps domain segments to physical chunks.** `Segment ≠ chunk` ([LD-03](../requirements/13-data-formats-and-portability.md#rule-ld-03) there). |
| LA-03 | **Writes are append-only and incrementally durable**, so an interruption leaves a known-good boundary. |
| LA-04 | **Gaps are explicit records**, with cause and time range ([SE-09](../requirements/products/arcscope.md#rule-se-09) in the ArcScope requirements). |
| LA-05 | **Finalisation seals a capture**; subsequent writes are prohibited ([SE-12](../requirements/products/arcscope.md#rule-se-12) there). |
| LA-06 | **Range reads are supported without loading the whole capture.** |
| LA-07 | **An overflow, drop or back-pressure event is recorded as data**, never merely logged ([SE-10](../requirements/products/arcscope.md#rule-se-10) there). |

---

## 6. Derived store

| # | Rule |
|---|---|
| DS-01 | **Everything derived is rebuildable from canonical data.** If deleting it loses user work, it is not derived (`§28` of the data requirements). |
| DS-02 | **Derived data carries the version of the pipeline that produced it** — extraction profile, index schema, embedding model, decoder version, render settings — so a pipeline change invalidates cleanly. |
| DS-03 | **Derived corruption is detected and discarded**, never propagated as a canonical failure ([CR-04](../requirements/12-quality-and-compatibility-contract.md#rule-cr-04) in the quality contract). |
| DS-04 | **Rebuild is a bounded background task** with its own progress, cancellation and resource budget ([IP-06](../requirements/06-knowledge-search-and-retrieval.md#rule-ip-06) in the knowledge requirements). |
| DS-05 | **Derived stores are evictable under pressure**, canonical stores never are ([MM-04](../requirements/12-quality-and-compatibility-contract.md#rule-mm-04) in the quality contract). |

---

## 7. Device-local state

Window and panel geometry, view state, recent items, expanded and collapsed sections, per-device paths, hardware selections, and local cache locations.

| # | Rule |
|---|---|
| DL-01 | **Never synchronised as user data** ([I-181](../requirements/01-normative-glossary-and-invariants.md#rule-i-181)). |
| DL-02 | **Never part of a native portable package** (`§2` of the data requirements). |
| DL-03 | **A named layout definition is a syncable concept; window coordinates are not** ([LY-03](../requirements/09-shared-desktop-experience.md#rule-ly-03)). |
| DL-04 | **Corruption or loss resets to defaults without user-visible consequence beyond layout.** |

---

## 8. Format architecture

```
Domain Model                 in memory, product-owned
   │  explicit mapping
Working Store                on disk, transactional
   │  explicit export
Native Portable Format       documented, versioned, full fidelity
   │  adapters
Interchange Formats          third-party, declared round-trip level
```

| # | Rule |
|---|---|
| FA-01 | **Object-graph serialization of the domain is prohibited** ([FV-09](../requirements/13-data-formats-and-portability.md#rule-fv-09) in the data requirements). Persistence uses an explicit schema. |
| FA-02 | **A CLR type name is never a persistent format contract** ([I-217](../requirements/01-normative-glossary-and-invariants.md#rule-i-217)). Formats use stable schema identifiers. |
| FA-03 | **Enums carry stable serialized values** never derived from declaration order ([FV-08](../requirements/13-data-formats-and-portability.md#rule-fv-08) there). |
| FA-04 | **A format reader is not the domain** ([IM-08](../requirements/13-data-formats-and-portability.md#rule-im-08) there). It produces a parsed representation mapped by an adapter. |
| FA-05 | **A format parser treats its input as untrusted** ([IM-07](../requirements/13-data-formats-and-portability.md#rule-im-07) there): bounded allocation, bounded decompression, rejected path traversal, no contained code executed, no absolute path trusted. |
| FA-06 | **Unknown additive fields are ignored on read and preserved on round trip** ([FV-04](../requirements/13-data-formats-and-portability.md#rule-fv-04) there). |
| <a id="rule-fa-07"></a>FA-07 | **An unknown domain element is preserved, marked and surfaced** — never silently dropped, never executed ([FV-05](../requirements/13-data-formats-and-portability.md#rule-fv-05) there). |
| FA-08 | **A format feature requirement is declarable**, producing an explicit "requires a newer version" state instead of a corrupt read ([FV-06](../requirements/13-data-formats-and-portability.md#rule-fv-06) there). |

> **Scope of the layer.** `Native Portable Format` exists for **ArcScope and ArcSlate**. `§4` of the data-format requirements limits the package requirements to those native formats and states plainly that they create no Notes/Chat local archive obligation; [EP-04](../requirements/products/arcnotes.md#rule-ep-04) of the ArcNotes requirements and [EX-09](../requirements/13-data-formats-and-portability.md#rule-ex-09) of the data-format requirements confirm it per product. For ArcNotes and ArcChat the layer below `Working Store` is a **Cloud-generated download**, not a native package, and it carries no re-import promise.

### 8.1 Portable package structure

```
<package>
├── manifest                    format version, product and writer version,
│                               contents inventory, round-trip level,
│                               integrity information
├── canonical/                  the exported canonical snapshot
├── resources/                  managed assets
├── history/                    optional, by user choice
└── integrity/                  checksums
```

| # | Rule |
|---|---|
| PP-01 | **The manifest is readable without loading the package**, so a tool can inspect, validate and plan first ([WS-05](../requirements/13-data-formats-and-portability.md#rule-ws-05) there). |
| PP-02 | **The manifest describes; it never duplicates content** ([WS-06](../requirements/13-data-formats-and-portability.md#rule-ws-06) there). |
| PP-03 | **A working store for a large project is a directory-backed bundle by default**; a single archive is an export option ([WS-02](../requirements/13-data-formats-and-portability.md#rule-ws-02), [WS-03](../requirements/13-data-formats-and-portability.md#rule-ws-03) there). |
| PP-04 | **Derived cache is excluded from a native export** ([EX-04](../requirements/13-data-formats-and-portability.md#rule-ex-04) there). |
| PP-05 | **Paths inside a package are relative, normalised and platform-neutral**, with a deterministic name mapping recorded in the manifest where portability requires it ([PT-01](../requirements/13-data-formats-and-portability.md#rule-pt-01), [PT-02](../requirements/13-data-formats-and-portability.md#rule-pt-02) there). |

---

## 9. Migration mechanics

### 9.1 Storage schema migration

```
Open store
 → read StorageSchemaVersion
 → if equal: proceed
 → if older: plan a migration path (version by version, no skips)
 → create a recovery point
 → run migration (transactional where small; staged where large)
 → verify
 → update StorageSchemaVersion
 → on failure: enter safe mode; never leave a half-upgraded writable store
```

| # | Rule |
|---|---|
| SM-01 | **Migrations are ordered, versioned and never skip a step**, so any historical version reaches current by a defined path. |
| SM-02 | **A small migration is transactional with a real rollback.** |
| SM-03 | **A large migration makes data safely openable first, then rebuilds in the background**, with the state visible ([MG-02](../requirements/13-data-formats-and-portability.md#rule-mg-02) there). |
| SM-04 | **Derived data is deleted and rebuilt rather than migrated** ([MG-03](../requirements/13-data-formats-and-portability.md#rule-mg-03) there). |
| SM-05 | **Canonical data receives a real migration**, never a rebuild ([MG-04](../requirements/13-data-formats-and-portability.md#rule-mg-04) there). |
| SM-06 | **A recovery point precedes any destructive migration** ([MG-05](../requirements/13-data-formats-and-portability.md#rule-mg-05) there) and is itself tested, not merely implemented ([MG-07](../requirements/12-quality-and-compatibility-contract.md#rule-mg-07) in the quality contract). |
| SM-07 | **Post-migration verification checks structure, counts, references and semantic spot checks** ([MG-07](../requirements/13-data-formats-and-portability.md#rule-mg-07) in the data requirements). |
| SM-08 | **On failure the product enters safe mode** and never continues writing half-upgraded data ([MG-08](../requirements/13-data-formats-and-portability.md#rule-mg-08) there). |
| SM-09 | **Migration is separate from application update** ([UP-08](../requirements/10-distribution-update-and-support.md#rule-up-08) in the distribution requirements). |
| SM-10 | **Downgrade behaviour is defined and tested**: an older application encountering newer data enters safe read-only or explicit-block, never silent field loss ([MG-08](../requirements/12-quality-and-compatibility-contract.md#rule-mg-08) in the quality contract). |

### 9.2 Native format migration

| # | Rule |
|---|---|
| NF-01 | **Format upgrade happens per opened object**, not as a whole-store sweep at start-up ([FV-03](../requirements/13-data-formats-and-portability.md#rule-fv-03) there). |
| NF-02 | **A user is told before an in-place upgrade makes data unreadable by the previous version** ([FV-02](../requirements/13-data-formats-and-portability.md#rule-fv-02) there). |
| NF-03 | **Every historical format version has a permanent golden fixture and a migration test** ([MG-02](../requirements/12-quality-and-compatibility-contract.md#rule-mg-02), [CM-09](../requirements/12-quality-and-compatibility-contract.md#rule-cm-09) in the quality contract). |
| NF-04 | **Read compatibility and write compatibility are declared separately** ([I-385](../requirements/01-normative-glossary-and-invariants.md#rule-i-385)). |

---

## 10. Import and export pipeline

```
Import:   source → parse (untrusted) → staging representation → validate
                 → map to domain via adapter → transactional apply
                 → record origin → produce report

Export:   domain → select scope → resolve assets → assemble package
                 → compute integrity → declare round-trip level
                 → produce loss report where lossy
```

| # | Rule |
|---|---|
| IE-01 | **Parsing never mutates the canonical store** ([IM-01](../requirements/13-data-formats-and-portability.md#rule-im-01) in the data requirements). |
| IE-02 | **A large import uses a staged transactional manifest**, so an interruption leaves cleanable staging and an untouched canonical store ([IM-02](../requirements/13-data-formats-and-portability.md#rule-im-02) there). |
| IE-03 | **Every import records origin**: source format, source identity, importer version, time, options ([IM-03](../requirements/13-data-formats-and-portability.md#rule-im-03) there). |
| IE-04 | **Re-import does not overwrite by default**; the user chooses create, update-matched or merge, with a preview ([IM-04](../requirements/13-data-formats-and-portability.md#rule-im-04) there). |
| IE-05 | **Every import produces a report** ([IM-05](../requirements/13-data-formats-and-portability.md#rule-im-05) there). |
| <a id="rule-ie-06"></a>IE-06 | **Unsupported data is preserved inert and marked**, never executed ([IM-06](../requirements/13-data-formats-and-portability.md#rule-im-06) there). |
| IE-07 | **Every export declares its round-trip level; a lossy export produces a loss report; silent loss is prohibited** ([EX-01](../requirements/13-data-formats-and-portability.md#rule-ex-01)–[EX-03](../requirements/13-data-formats-and-portability.md#rule-ex-03) there). |

---

## 11. Storage pressure and locations

| # | Rule |
|---|---|
| SP-01 | **A durability reserve is held** so a canonical commit can always complete; new operations fail safely before it is consumed ([SL-05](../requirements/13-data-formats-and-portability.md#rule-sl-05) there). |
| SP-02 | **Space is checked before importing into the managed store** ([SL-06](../requirements/13-data-formats-and-portability.md#rule-sl-06) there). |
| SP-03 | **A capture or render approaching a disk limit warns early and stops cleanly at a known boundary** ([SL-04](../requirements/13-data-formats-and-portability.md#rule-sl-04) there). |
| SP-04 | **Data location is visible per product, with sizes; relocation is an application-managed migration** ([SL-01](../requirements/13-data-formats-and-portability.md#rule-sl-01), [SL-02](../requirements/13-data-formats-and-portability.md#rule-sl-02) there). |
| SP-05 | **Cache eviction is automatic under pressure and never touches canonical data.** |

---

## 12. Repository projection — excluded delivery

**No product ships one.** `§14` of the data-format requirements excludes Git synchronisation, repository projection, linked-repository editing and LFS integration; [GT-01](../requirements/13-data-formats-and-portability.md#rule-gt-01)–[GT-09](../requirements/13-data-formats-and-portability.md#rule-gt-09) are retired dispositions, and the retirement is explicit that there is **no repository-projection feature and no acceptance gate**. [EX-09](../requirements/13-data-formats-and-portability.md#rule-ex-09) says the same for ArcNotes specifically. This section therefore states a prohibition, not a design.

What survives is the pair of invariants, which are **prohibitions about a user's own repository**, not obligations to write into one:

| # | Rule |
|---|---|
| <a id="rule-gp-01"></a>GP-01 | **No product writes a repository projection**, and no build produces a projection writer, a Git client dependency or an LFS path. A structural test asserts it (`§14` there). |
| <a id="rule-gp-02"></a>GP-02 | **[I-211](../requirements/01-normative-glossary-and-invariants.md#rule-i-211) — a repository is never runtime authority.** If a user keeps exported content inside a repository, that repository is still not a store: the runtime reads its own working store, and content arriving through a repository is an ordinary import, subject to the ordinary import pipeline (`§10`). |
| <a id="rule-gp-03"></a>GP-03 | **[I-212](../requirements/01-normative-glossary-and-invariants.md#rule-i-212) — a repository is never the live working store.** No code path opens a working store located in, or synchronised by, a repository as though it were transactional storage. |
| GP-04 | **`P3` still binds**: transaction safety and editing performance are never traded for text friendliness. With projection excluded there is nothing left to trade them for, which is the point of the exclusion. |
| GP-05 | **A product's exit path is its declared export** (`§8`), never a repository. Directing a user to a repository as a substitute for export or for multi-device sync is prohibited — a runtime database is not a mergeable document. |

---

## 13. Cloud-side persistence

The cloud data model is specified in [`05-cloud-architecture.md`](05-cloud-architecture.md) §5 and [`07-sync-conflict-and-backup.md`](07-sync-conflict-and-backup.md). Two rules bridge the layers:

| # | Rule |
|---|---|
| CB-01 | **A native package is not a cloud sync envelope, and an import format is not the internal sync format** ([I-186](../requirements/01-normative-glossary-and-invariants.md#rule-i-186), [OW-04](../requirements/13-data-formats-and-portability.md#rule-ow-04) in the data requirements). Three separate representations. |
| CB-02 | **Local canonical data and its cloud replica share object identity and revision semantics**, never storage format. |

---

## 14. Traceability

| Current document | Relationship |
|---|---|
| [Working Data, Project Formats and Cloud Portability Requirements](../requirements/13-data-formats-and-portability.md) | Owns the working store, portable-package and recovery contracts; Git projections remain excluded |
| [Desktop Local Data Model](data-model/02-desktop-data-model.md) | Defines concrete stores, revisions and journal records |
| [Product Quality and Compatibility Contract](../requirements/12-quality-and-compatibility-contract.md) | Owns migration, downgrade and recovery verification |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | AOT-safe local data access on desktop deliverables |
