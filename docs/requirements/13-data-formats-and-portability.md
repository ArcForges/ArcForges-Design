# Working Data, Project Formats and Cloud Portability Requirements
> Current scope amendment: **[P2-006](../decisions/phase-2-specification-decisions.md)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Companions: [`03-cloud-services-and-sync.md`](03-cloud-services-and-sync.md), [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md), [`../architecture/06-data-persistence-and-formats.md`](../architecture/06-data-persistence-and-formats.md)

This contract governs native working data, Cloud-acknowledged authority, pending-change durability and the product-specific portability formats. It does not require a standalone local ArcNotes/ArcChat product, encrypted export or a universal local backup package.

---

## 1. Five layers, never conflated

| Layer | Definition | Authority |
|---|---|---|
| **Domain Model** | The product's in-memory business model | The product |
| **Working Store** | Durable native working data and Cloud persistence with explicit revision ownership | Cloud acknowledges Notes/Chat state; native products own local tools, pending edits and Scope/Slate working stores |
| **Native Portable Format** | Required Scope/Slate project portability, where explicitly specified | The owning product; not a universal notebook/chat archive requirement |
| **Interchange Format** | Third-party formats — Markdown, HTML, PDF, CSV, media, subtitle, timeline exchange | Adapters; **full fidelity is not guaranteed** |
| **Derived Projection / Cache** | Indexes, thumbnails, proxies, decoded caches, embeddings | Rebuildable; never authority |

### 1.1 The three highest principles

| # | Principle |
|---|---|
| **P1** | **Runtime Storage Format ≠ User Interchange Format** (`I-187`). What is efficient and transactional on disk is not what a user should receive when they export. |
| **P2** | **The logical format of user data is independent of the current database technology** (`I-184`). Replacing the storage engine must not change the user's data format. |
| **P3** | **Transaction safety and editing performance are never sacrificed for "Git friendliness"** (`I-211`). The working store serves correctness first; text friendliness uses only the exports/interchange explicitly in product scope. |

---

## 2. Local data classification

| Class | Examples | Durability requirement |
|---|---|---|
| **Canonical Structured State** | Notebooks, documents, blocks, links, tags, sessions, measurements, sequences, tracks, clips, conversations, tasks | **Must reach a reliable durable store** |
| **Managed Assets** | Imported attachments, imported media, uploaded telemetry | Owned, hashed, lifecycle-managed |
| **External References** | Files left where the user put them | Referenced, never owned |
| **Append-only / Large Data** | Raw captures, long event streams | Chunked, verifiable large-scale storage — **never an ordinary blob column** |
| **Revision / Recovery State** | Revisions, checkpoints, recovery journal | Reliability infrastructure |
| **Derived Data** | Search index, embeddings, thumbnails, waveforms, proxies, decoded caches | **Delete and rebuild** |
| **Device-local Presentation State** | Window and panel layout, view state, recent items | Device-local by default; **never part of native project portability** |
| **Secrets** | Credentials, keys | Platform secure storage only — **never inside a project or document format** |
| **Temporary Data** | Scratch, staging, render temp | Directly cleanable |

---

## 3. Storage strategy per product

Each product owns its own local store (`P-09`). A single shared `ArcForges.db` is prohibited.

| Product | Strategy | Shape |
|---|---|---|
| **ArcChat** | Cloud authority with native cache | Cloud conversations/projects/agent state; native history projections, unsent drafts, bounded attachments and local tool receipts. Cloud export is the portability route. |
| **ArcNotes** | Cloud authority with durable native working cache | Cloud-acknowledged documents/blocks/properties/attachments/revisions; native cached data, pending-edit journal and local lexical index. Markdown is interchange, not the working store. |
| **ArcScope** | **Project-centric hybrid** | A clearly identifiable project store: manifest, canonical metadata, a chunked capture store, managed assets, recovery state, derived caches. |
| **ArcSlate** | **Project-centric hybrid** | A project store plus media references and managed media plus derived stores. **Original media is never inserted into the core database.** |

### 3.1 Authority and native working content

| Product | Native durable content | Cloud authority |
|---|---|---|
| ArcNotes | Cached acknowledged documents/attachments, stable pending edits and attachment uploads, local lexical index, device UI state | Acknowledged revisions, synced attachments, history, trash, semantic index and export jobs |
| ArcChat | Cached history/projections, unsent drafts, permission grants and idempotent local tool receipts | Conversations/projects/profiles/memory, the single agent runtime and schedules, usage and export jobs |
| ArcScope | Project metadata, hardware captures/chunks, analysis and recovery state; downloaded synthetic capture | Synced metadata and explicitly uploaded raw data; simulator scenarios, runs and committed output manifests |
| ArcSlate | Project/edit store, managed/external media references, recovery and revision state; derived proxies/caches | Synced project revisions and explicitly selected media |

Pending edits, attachment bytes awaiting upload and unacknowledged tool receipts are not evictable cache. They survive restart, outage and service expiry until acknowledged or explicitly discarded. Evicting acknowledged downloaded content never creates a new domain revision. Cloud loss cannot be disguised by promoting a stale client projection into unrestricted server authority.

---

### 3.2 Large and append-only data

| # | Requirement |
|---|---|
| LD-01 | **Raw capture uses independent, chunked, verifiable large-scale storage**, not a blob column in a relational table. |
| LD-02 | Chunking exists so that a long capture can be written incrementally and durably, recovered after interruption at a known boundary, read by range without loading everything, and verified per chunk. |
| LD-03 | **A capture segment is not a physical chunk.** Segment is a domain concept; chunk is a storage concept. They are related by a manifest, never equated. |
| LD-04 | **Raw capture is immutable after finalisation.** It is evidence. Producing a cleaned or transformed version creates a **new managed representation**; it never rewrites the original. |
| LD-05 | **Decoder output does not enter the raw store** (`I-471`). It is derived and reproducible. |

---

## 4. Working store versus portable package

These package requirements apply to the Scope/Slate native formats and any explicitly offered package. They do not create a Notes/Chat local archive obligation.

| # | Requirement |
|---|---|
| WS-01 | **Working Store ≠ Portable Package** (`I-188`). One is optimised for transactional editing; the other for transport and archival. |
| WS-02 | **A large project's working store is a directory-backed bundle by default**, not a single compressed container. Forcing every project into one archive file makes incremental, transactional editing impossible. |
| WS-03 | **Portable export may produce a single-file archive** when the user asks for one; a folder bundle is equally valid. |
| WS-04 | **A portable bundle always contains a manifest**: format version, product and writer version, contents inventory, resource identities, integrity information, and the round-trip level. |
| WS-05 | **The manifest must be readable without loading the whole project**, so a tool can inspect, validate and plan before committing to a full read. |
| WS-06 | **The manifest is not a second copy of the project content.** It describes; it does not duplicate a timeline or a document body. |

---

## 5. Format versioning

Four independent version axes at this layer (`I-383`):

| Axis | Meaning |
|---|---|
| **`StorageSchemaVersion`** | The internal working store — migrated by the application or its migrator |
| **`NativeFormatVersion`** | The portable project/document format |
| **`ProductVersion`** | The installed application |
| **Reader / Writer version** | What this build can read, and what it can safely write |

| # | Requirement |
|---|---|
| FV-01 | **Backward read and backward write are separate declarations** (`I-385`). Reading old data does not imply writing it safely. |
| FV-02 | **A new version opening old data must not silently destroy old compatibility.** If opening would upgrade in place and make the data unreadable by the previous version, the user is told before it happens, and given a choice. |
| FV-03 | **Format upgrade is separate from application startup.** Only data actually opened, or explicitly batch-migrated, is upgraded. A startup that migrates everything is prohibited. |
| FV-04 | **Unknown additive fields are ignored on read and preserved on round-trip** (`FV-08`), never dropped. |
| FV-05 | **An unknown domain element is preserved, marked and surfaced**, not silently discarded — and **never executed** for the sake of preservation. |
| FV-06 | **A format feature requirement is declarable**: a document may state that it requires a capability the reader lacks, producing an explicit "requires a newer version" state rather than a corrupted read. |
| FV-07 | **A CLR type name is never a persistent format contract** (`I-217`). Formats use stable schema identifiers. |
| FV-08 | **Enums are designed for persistence**, with stable serialized values that are never derived from declaration order. |
| FV-09 | **Object-graph serialization of the domain is prohibited.** Persistence uses an explicit schema, always. |

---

## 6. Migration

| # | Requirement |
|---|---|
| MG-01 | **Small schema migrations are transactional** with a real rollback. |
| MG-02 | **Large migrations must not pretend one transaction solves everything.** The pattern is: make the data safely openable first, then rebuild in the background, with the state visible. |
| MG-03 | **Derived data usually does not migrate at all** — it is deleted and rebuilt (`I-196`). |
| MG-04 | **Canonical user data receives a real migration**, never a delete-and-rebuild. |
| MG-05 | **A recovery point is created before any destructive migration** (`SY-23`). |
| MG-06 | **Migration Recovery Point ≠ normal Undo** (`I-207`). It is system recovery, not user edit history. |
| MG-07 | **Migration is verified after completion** — structure, counts, references, and semantic spot checks — not merely "no exception thrown" (`I-386`). |
| MG-08 | **On migration failure the product enters safe mode.** **It must never continue writing half-upgraded data** (`I-207`). |
| MG-09 | **Application binary rollback ≠ data rollback** (`I-208`). Both exist, both are tested, and the updater must know the data compatibility state so it can refuse an unsafe downgrade. |

---

## 7. Save semantics

| # | Requirement |
|---|---|
| SV-01 | A native edit commits its pending operation and required local content durably before reporting local save. Cloud sync then acknowledges a revision. Cloud-created chat/agent/simulator work commits in Cloud directly; it does not require a desktop write first. |
| SV-02 | The UI distinguishes Saved on this device / Pending sync / Synced. Synced means the owning Cloud authority acknowledged the revision and required assets; queued writes and optimistic UI alone are not saved. |
| SV-03 | **Autosave is incremental and transactional** (`I-198`). It never rewrites an entire project on each keystroke. |
| SV-04 | **UI transient state and committed edits are separate.** A preview state, an in-progress drag, an uncommitted parameter scrub are not durable edits. |
| SV-05 | **Continuous text input coalesces into one edit transaction** over a short window, so history is meaningful and writes are efficient. |
| SV-06 | **Explicit Save remains available** where users expect it, and means "commit and flush now", not "the only time data becomes durable". |
| SV-07 | Durable pending sync does not require an unsaved-edit prompt on ordinary window close. Sign-out, cache reset, account deletion or data migration that would discard pending work must show a separate data-loss warning and preserve it unless explicitly discarded. |

---

## 8. Undo, Revision, Checkpoint, Recovery Journal

Four permanently separate concepts (`I-201`–`I-204`):

| Concept | Meaning | Visibility |
|---|---|---|
| **Undo** | Reversible in-session edit history, based on **semantic commands** | User-facing, high frequency |
| **Revision** | Durable history of committed states | User-facing history |
| **Checkpoint** | A named recovery landmark at a stable revision | User-facing, low frequency |
| **Recovery Journal** | Persistence infrastructure for crash recovery | **Not a user-browsable list** |

| # | Requirement |
|---|---|
| UR-01 | **Undo is based on semantic commands**, never on UI snapshots. |
| UR-02 | **Undo never deletes a revision.** Undoing produces a new state; history is not rewritten. |
| UR-03 | **A checkpoint is not created per command.** It marks a meaningful landmark — before an agent batch edit, before a migration, before a risky operation. |
| UR-04 | **Users must never be shown a million journal entries.** The journal serves recovery and diagnosis. |
| UR-05 | **Revision history must be durable. Undo continuity across restarts may be persisted per product, but is never the only recovery mechanism.** |
| UR-06 | It must never be claimed that undo history survives a crash unless it demonstrably does. |

---

## 9. Crash recovery

| # | Requirement |
|---|---|
| CR-01 | **Every confirmed durable commit must survive** (`CR-01` in the quality contract). |
| CR-02 | **Recovery must not depend on a clean exit.** A power loss is a normal test case, not an exceptional one. |
| CR-03 | The startup recovery pipeline: detect abnormal exit → validate the canonical store → replay or roll back the journal to the last committed revision → validate derived stores → quarantine anything suspected of causing the fault → present a recovery report. |
| CR-04 | **Damaged derived cache must never produce "project corrupt."** The cache is discarded and rebuilt. |
| CR-05 | **A damaged canonical store enters Recovery Mode**, which is read-first and does not overwrite in place. |
| CR-06 | **Recovery must not repeatedly attempt destructive in-place repair.** The damaged source is preserved so a later, better recovery attempt remains possible. |
| CR-07 | **Task recovery and data recovery are separate** (`RV-01`–`RV-05` in the AI requirements versus this section). An incomplete long task is not a data-integrity event by itself. |

---

## 10. External references

| # | Requirement |
|---|---|
| ER-01 | **A path is only a locator hint** (`I-194`). Identity is the asset identity. |
| ER-02 | **A portable project must not depend on the original machine's absolute paths.** A missing external resource is an explicit, recoverable state (`AS-04`). |
| ER-03 | **Managed assets inside a project use relative positions**, so the bundle moves intact. |
| ER-04 | **External file changes are detected**, using a fingerprint that need not rehash an enormous file every time — size, timestamp, sampled content and recorded hash together are sufficient to detect meaningful change and to trigger a full verification when warranted. |
| ER-05 | **`ArcSlate` timeline clip identity never changes because a file changed** (`I-477`). Clip identity binds to the media asset identity, not the bytes. |

### 10.1 External editing boundaries

| # | Requirement |
|---|---|
| EE-01 | **V1 performs no real-time bidirectional mirroring of an external Markdown folder.** The boundary is explicit rather than accidentally half-working. |
| EE-02 | **A managed attachment may be opened externally** with an external application, and the change flows back through a controlled re-import — never by an external process writing into the internal store. |
| EE-03 | **An external editor must never modify the internal store directly.** That is a corruption interface, not a feature. |
| EE-04 | A linked Markdown workspace or Git-backed notebook mode is excluded from the current delivery. Explicit Markdown import does not establish a second live writer. |
| EE-05 | **A finalised ArcScope capture does not follow external file changes.** Choosing to link or replay an external source produces a new source revision or import state. |
| EE-06 | **ArcSlate media may always be external**; external subtitle or metadata files may have an explicit linked mode that watches for changes. |

### 10.2 Single writer authority

| # | Requirement |
|---|---|
| WA-01 | **A canonical resource has exactly one writer authority at any moment** (`WN-04`). |
| WA-02 | **Any external-edit mode must declare which side holds authority.** |
| WA-03 | **A lock file alone is not sufficient** — it is a coordination hint. Stale locks are detectable, and taking ownership is an explicit, confirmed act. |
| WA-04 | **One process, several windows on one document** share a document session (`WN-04`). |
| WA-05 | **Two devices editing a synced project concurrently** is a sync conflict, resolved by the sync conflict model, not by a local lock. |
| WA-06 | **An external checkout overwriting project files** is detected as an external store change and handled explicitly, never silently absorbed. |

---

## 11. Import

| # | Requirement |
|---|---|
| IM-01 | **Parsing must not mutate the canonical store.** Parse into a staging representation first. A half-import must be impossible. |
| IM-02 | **A large import that cannot be one transaction uses a staged transactional manifest**, so an interruption leaves cleanable staging data and an untouched canonical store. |
| IM-03 | **Every import records its origin**: source format, source file identity, importer version, time, and options used. |
| IM-04 | **Re-import does not overwrite by default.** The user chooses: create new, update matched, or merge — with a preview. |
| IM-05 | **Every import produces a report**: what was imported, what was skipped, what was approximated, what was preserved-but-unmapped, and what was lost. |
| IM-06 | **Unsupported data is preserved wherever possible**, in a marked, inert form. **Preservation never justifies executing unknown content.** |
| IM-07 | **A format parser is untrusted input** (`I-216`). Bounds are checked, allocations are limited, path traversal is rejected, decompression is bounded, and no contained code is executed. **A native format is not a trusted memory dump.** |
| IM-08 | **A format reader is not the domain** (`I-183`). It produces a parsed representation that is mapped into the domain by an adapter. |

---

## 12. Export

The product scope determines which exports exist:

| Product | Required portability |
|---|---|
| ArcNotes | Cloud Markdown export with selected attachments, hierarchy/property metadata and fidelity manifest; Markdown/text import under the Notes requirements |
| ArcChat | Cloud conversation JSON/text and selected task-summary/artifact export; no local execution archive |
| ArcScope | Native investigation bundle, CSV/JSON and report outputs; simulator provenance retained |
| ArcSlate | Native project/collect package, rendered media/subtitles, and canonical .otio in both directions (OT-01–OT-12) |

The following classes describe an offered export; they do not require every product to implement all three:

| Class | Purpose | Round-trip |
|---|---|---|
| **Native full-fidelity** | Move between ArcForges installations | Complete |
| **Interoperable** | Open in another tool | Partial, with declared losses |
| **Presentation** | Consume the result | None |

| # | Requirement |
|---|---|
| EX-01 | **Every export declares its round-trip level** explicitly, in the interface and in the manifest. |
| EX-02 | **A lossy export produces a loss report** naming what could not be represented. |
| EX-03 | **Silent data loss is absolutely prohibited** (`I-386`). |
| EX-04 | **Native export excludes derived cache.** Exporting a project must not ship a render cache. |
| EX-05 | Exports bind a consistent revision snapshot and declare scope/history/attachment availability. Full archival history export is not a universal requirement; product-specific supported choices must not silently imply omitted history is included. |
| EX-06 | **Managed assets are included by default** in a native export; the user may exclude them. |
| EX-07 | **External resources are excluded by default**, with an explicit "collect external assets into the export" option (`EX-04` in the cloud requirements). |
| EX-08 | **ArcSlate "collect project"** and **ArcScope "collect investigation bundle"** are first-class operations under this architecture: they gather the project, its managed assets and, on request, its external references into a portable bundle, without destroying the originals. |
| EX-09 | ArcNotes portability is its Cloud-produced Markdown, attachments and metadata/fidelity manifest under [EP-01–EP-04](products/arcnotes.md). A local native/encrypted archive, DOCX import, Git projection or PDF/HTML export engine is not required. |
| EX-10 | Every export excludes credentials, private deployment policy and unselected source data. ArcChat exports only authorized conversation/task summaries and selected artifacts. |
| EX-11 | **Export ≠ Backup** (`I-210`). Export is portability; backup is recovery. |

---

## 13. Portability constitution

| # | Requirement |
|---|---|
| PT-01 | **Paths inside a portable bundle are relative, normalised and platform-neutral.** |
| PT-02 | **Names are validated for portability**: reserved names, case collisions, length limits and illegal characters produce a **deterministic mapping recorded in the manifest**, never a silent rename or a failure. |
| PT-03 | **Unicode normalisation must not change resource identity.** A differently normalised filename is the same resource. |
| PT-04 | **Line endings never enter domain identity.** A CRLF/LF change must not make a document a new resource. |
| PT-05 | **Time zone is never implicit portable state.** Storage uses a stable instant plus, where meaningful, the original zone semantics. |
| PT-06 | **A native format supports integrity detection** — checksums at the manifest and content level. |
| PT-07 | **Partial damage is localised as far as possible.** One damaged asset must not make an entire project unreadable. |
| PT-08 | **Canonical metadata damage is more serious than a missing asset**, and the two produce different recovery experiences. |

---

## 14. Git and repository projections — excluded delivery

No product must ship Git synchronization, repository projection, linked-repository editing or LFS integration. Source-code repositories and deployment configuration remain normal engineering artifacts. Runtime databases are not mergeable documents, and Git cannot substitute for multi-device sync.


| # | Disposition |
|---|---|
| GT-01 | Retired by P2-006 as a product delivery obligation; no repository-projection feature or acceptance gate. |
| GT-02 | Retired by P2-006 as a product delivery obligation; no repository-projection feature or acceptance gate. |
| GT-03 | Retired by P2-006 as a product delivery obligation; no repository-projection feature or acceptance gate. |
| GT-04 | Retired by P2-006 as a product delivery obligation; no repository-projection feature or acceptance gate. |
| GT-05 | Retired by P2-006 as a product delivery obligation; no repository-projection feature or acceptance gate. |
| GT-06 | Retired by P2-006 as a product delivery obligation; no repository-projection feature or acceptance gate. |
| GT-07 | Retired by P2-006 as a product delivery obligation; no repository-projection feature or acceptance gate. |
| GT-08 | Retired by P2-006 as a product delivery obligation; no repository-projection feature or acceptance gate. |
| GT-09 | Retired by P2-006 as a product delivery obligation; no repository-projection feature or acceptance gate. |

---

## 15. Backup and restore

Native backup UX here applies to Scope/Slate project data. Notes/Chat use Cloud operator recovery and protected native pending-change durability; custom local-store encryption, encrypted export and end-to-end encryption are excluded. TLS, encrypted server storage/backups and system secret storage remain mandatory.

| # | Requirement |
|---|---|
| BK-01 | **Backup ≠ Export** (`I-210`). |
| BK-02 | **A backup must never copy an open database file directly.** A consistent snapshot is required; copying a live file yields an inconsistent backup. |
| BK-03 | Scope/Slate native project backups use consistent manifest snapshots and incremental content. Notes/Chat disaster recovery is the Cloud operator backup/restore contract; durable pending-change recovery remains native, not a user-managed full local backup product. |
| BK-04 | ArcSlate large media may be included in a backup, and the collect-project operation is the supported route for a self-contained copy. |
| BK-05 | **Backup integrity is validated** — the backup is verified, not merely written (`BK-06` in the cloud requirements). |
| BK-06 | **Restore must not overwrite an open project in place.** It restores to a new location or requires the project to be closed, with explicit confirmation. |

---

## 16. Ownership of the local store

| # | Requirement |
|---|---|
| OW-01 | Only the owning product writes its native store. Cloud modules own their respective authoritative server data; cross-boundary changes use revision-checked APIs or product capabilities. |
| OW-02 | **Even read-only direct SQL access from another product is prohibited.** Access goes through capabilities. |
| OW-03 | **A search index is never a cross-product shared database** (`I-136`, `SR-04`). Each product may have its own index. |
| OW-04 | **A native package is not a cloud sync envelope** (`I-186`), and **an import format is not the internal sync format**. Three separate representations. |

---

## 17. Storage location and pressure

| # | Requirement |
|---|---|
| SL-01 | **The data location is visible to the user**, per product, with sizes. |
| SL-02 | **Moving local data is an application-managed migration**, not a "copy the folder and hope" instruction. |
| SL-03 | **Cache location may be moved independently** of canonical data, so a user can place caches on a fast drive. |
| SL-04 | **Low disk during capture or render must degrade safely**: warn early, stop cleanly at a known boundary, and never corrupt what is already committed. |
| SL-05 | **Emergency durability headroom is reserved** so a canonical commit can always complete; new operations fail safely before that headroom is consumed. |
| SL-06 | **Space is checked before importing into the managed store**, not discovered mid-copy. |

---

## 18. Deletion and garbage collection

| # | Requirement |
|---|---|
| DL-01 | **Deleting an external reference never deletes the external file** by default. |
| DL-02 | **Deleting a managed asset may delete the application-managed file**, after a reference-integrity check. |
| DL-03 | **Garbage collection only removes unreferenced managed data** (`I-215`). |
| DL-04 | **Resource GC and user delete are separate operations** with separate triggers, separate visibility and separate audit. |
| DL-05 | Only genuinely derived/acknowledged cached content is evictable. Pending edits, pending uploads and unsettled local tool receipts are protected until reconciled or explicitly discarded. |

---

## 19. Acceptance scenarios

**Cloud/cache** — offline edits and pending uploads survive cache pressure and restart; another device receives only acknowledged revisions; Cloud export identifies pending local content not yet included. Simulator chunks and OTIO imports follow their product-specific commit/fidelity rules.

**Durability** — kill after save, OS crash, disk full, corrupted store, interrupted migration, application downgrade; in every case, everything reported saved is present.

**Autosave** — continuous typing produces coalesced transactions, not per-keystroke project rewrites; "saved" appears only when durable.

**Undo/Revision/Checkpoint/Recovery** — undo does not delete revisions; a checkpoint is a landmark, not per-command; the journal is never surfaced as user history.

**Format versioning** — an older reader encountering a newer format reports "requires a newer version"; unknown additive fields survive a round trip; a downgrade cannot silently drop fields.

**Migration** — small migrations roll back; large migrations open safely then rebuild; a failure enters safe mode with no half-upgraded store; a recovery point genuinely restores.

**External references** — a moved file produces an explicit missing-asset state, relink verifies by content, and the project still opens.

**External editing** — an externally opened attachment flows back through controlled re-import; no external process writes into the internal store.

**Single writer** — two windows share one document session; a stale lock is detectable and ownership transfer is explicit.

**Import** — a malformed package is rejected without touching the canonical store; a path-traversal archive is refused; an archive bomb is bounded; every import produces an origin record and a report.

**Export** — every export declares its round-trip level; a lossy export lists losses; a native export omits derived cache; external assets are excluded unless requested.

**Portability** — a bundle moves between platforms with reserved names deterministically mapped, Unicode normalisation not changing identity, and line-ending changes not creating new resources.

**Excluded paths** — no notebook local archive/encryption, DOCX import or repository-projection delivery is inferred from generic portability rules. Required Scope/Slate exports, OTIO and native recovery remain covered.

**Backup and restore** — a backup of an open store is consistent; integrity is validated; restore does not overwrite an open project.

**Ownership** — an attempt to read another product's store directly fails architecture tests.

**Storage pressure** — low disk during capture stops at a clean boundary; committed data survives; the reserve headroom protects the final commit.

**Deletion** — deleting an external reference leaves the file; garbage collection removes only unreferenced managed data; derived cache eviction is invisible to correctness.

---

## 20. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 22` | The entire local data constitution: five layers, data classification, per-product storage strategy, working store versus portable package, format versioning, migration, save semantics, undo/revision/checkpoint/journal separation, crash recovery, external references and editing boundaries, import and export architecture, portability constitution, Git friendliness, backup, ownership, storage pressure and deletion |
| `I4 §Stage 9` | Object identity, revisions, managed versus external assets, immutable blobs, tombstones, and deletion propagation on the cloud side |
| `I4 §Stage 27` | The migration, compatibility and recovery contracts that gate this layer |
| `I3 §10`, `§11`, `§12`, `§14` | Document identity and revisions, undo ownership, journal and snapshot design, resource path discipline |
| **D-008** | AOT-safe persistence path constraints for desktop deliverables |
