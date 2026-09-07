# WP-19 — ArcNotes Search, Import, Export and Portability

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: D — ArcNotes core
> Upstream: `18` · Downstream: `20`, `25`, `28`, `40`

> **Goal.** Make ArcNotes content findable and portable **within the accepted exit path** (`§13` of the ArcNotes requirements): search over hydrated content with citation anchors, non-destructive Markdown and plain-text import, and the **Cloud-generated notebook download** — proving the exit path rather than asserting it.

---

## 1. Scope and purpose

**In scope.** The local search index over hydrated content and its query surface; citation anchors; saved views over queries; non-destructive import from Markdown and plain-text sources including an Obsidian-style folder layout (`IM-02`); and the client half of the **Cloud notebook export** with its fidelity report.

**Out of scope by `EP-04`, `IM-02` and `§14` of the data-format requirements.** Repository projection, Git synchronisation, linked-repository editing and LFS integration; native portable packages; HTML, PDF and DOCX export pipelines; bit-for-bit archive round-trips; custom local encrypted export; DOCX, Notion-specific, HTML and proprietary full-fidelity importers; and any live bidirectional folder mirror or linked-vault mode (`IM-07`).

**Out of scope.** Cloud search (`40` and `25`). Semantic retrieval and embeddings (`40`). Database-view queries (`28`) — saved views here are list projections only.

**Why this package exists.** `I2 §V` requires local full-text indexing and citation anchors to be **real early**, because cloud search may be mocked but the local index cannot. Export is also the precondition for sync: a format that cannot round-trip locally will not round-trip through a server.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/06-knowledge-search-and-retrieval.md`](../../requirements/06-knowledge-search-and-retrieval.md) | Search versus retrieval, evidence and citation anchors, permission-aware retrieval |
| [`../../requirements/13-data-formats-and-portability.md`](../../requirements/13-data-formats-and-portability.md) | The portability constitution, import and export obligations, and the **repository-projection exclusion** (`§14`, `EX-09`) |
| [`../../architecture/06-data-persistence-and-formats.md`](../../architecture/06-data-persistence-and-formats.md) `§8` | The import pipeline and the export pipeline |
| `WP-18` output | The document model, link index and attachment model |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Search over hydrated content works during a Cloud outage.** Workspace-wide search is `search.query` on the public surface; the two are separate operations with different completeness and neither is presented as the other (`NO-05`). |
| BR-02 | **`Search ≠ Retrieval`.** Search serves a person; retrieval assembles evidence for a model. They share an index but not a contract. |
| BR-03 | **The index is a derived store**: deleting it rebuilds completely (`QI-10`). |
| BR-04 | **Search reveals nothing direct access would refuse** — permission is applied at query, not after ranking. |
| BR-05 | **A citation anchor is stable**, surviving edits around it where the cited content still exists, and reporting explicitly when it does not. |
| BR-06 | **Import is non-destructive**: the source is never modified, and a partial import is reported rather than silently completed. |
| BR-07 | **Export is complete**: a native export can be re-imported to reconstruct the content, including attachments and structure (`EX-01` in the data requirements). |
| BR-08 | **An export never silently loses fidelity.** A lossy target format states what it drops. |
| BR-09 | **No repository projection, Git synchronisation, linked-repository mode or LFS path is built** (`§14` and `EX-09` of the data-format requirements; `EE-04` there). `GT-01`–`GT-09` are retired, explicitly including their acceptance gates, so no Git-friendliness level is declared and none may be demanded. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcNotes/ArcNotes.Search/` | Index, tokenisation, query, ranking, citation anchors, saved views |
| `src/ArcNotes/ArcNotes.ImportExport/` | Markdown and plain-text import pipeline, and the client half of the Cloud export download. **No portable-package writer, no HTML/PDF/DOCX pipeline** (`EP-04`) |
| `src/ArcNotes/ArcNotes.Application/` | Search and import/export application services |
| `fixtures/formats/import/` | Source-format fixtures for every supported import claim |
| `fixtures/formats/arcnotes/v1/` | Extended with export round-trip fixtures |
| `tests/ArcNotes.Tests.Integration/` | Search, import, export and round-trip suites |

**Major types introduced.** `SearchIndex`, `SearchQuery`, `SearchResult`, `CitationAnchor`, `SavedView`, `ImportSource`, `ImportPlan`, `ImportReport`, `ExportTarget`, `ExportReport`, `PortablePackage`.

---

## 5. Required implementation work

### WP-19.00 — Local full-text index

**What must be fully done.** An incremental index over document content, block content, properties, tags and attachment-extracted text. Updates follow the write path so the index never diverges. The index rebuilds fully from canonical data. Query latency meets budget on the scale corpus.

**Testing requirements.** Divergence test after a crash mid-index-update; full rebuild equivalence; latency measurement against the scale corpus.

**Completion gate.** The index never diverges after a crash, rebuilds to an equivalent state, and meets query latency budget at scale.

### WP-19.01 — Query, ranking and permission

**What must be fully done.** Query supporting text, property, tag and structural filters. Ranking is explainable at a basic level. Permission is applied during query evaluation so that a refused document never influences results, including result counts.

**Testing requirements.** Filter coverage tests; a permission test asserting refused content affects neither results nor counts; a ranking stability test.

**Completion gate.** Permission is applied at query evaluation and refused content is invisible in every observable way.

### WP-19.02 — Citation anchors

**What must be fully done.** Anchors identify a location precisely enough to navigate back to it and remain valid across edits that do not remove the cited content. When the cited content is gone, the anchor reports that state explicitly rather than silently resolving elsewhere.

**Testing requirements.** Anchor survival across insert, delete, reorder and reparent; an explicit-invalid test after content removal.

**Completion gate.** Anchors survive surrounding edits and report invalidity explicitly rather than drifting.

### WP-19.03 — Saved views

**What must be fully done.** A saved view is a saved query plus sort and filter configuration, producing a list projection. A saved view does not own documents; deleting it never deletes content.

**Testing requirements.** Ownership test asserting deletion is non-destructive; a re-evaluation test asserting results reflect current content.

**Completion gate.** A saved view owns nothing and always reflects current content.

### WP-19.04 — Non-destructive import

**What must be fully done.** Import from the declared source formats, producing an import plan the user can review, then an import report stating exactly what was created, transformed and skipped. The source is never modified. A partially failed import leaves a coherent result and a clear report, never a half-state presented as success.

**Testing requirements.** Import from every declared source fixture; a source-immutability assertion; an induced-failure test asserting a coherent partial result with a report.

**Completion gate.** Every declared import source has a fixture and imports correctly; the source is never modified; partial failure is reported rather than hidden.

### WP-19.05 — Export and round-trip

**What must be fully done.** **The required exit path is a Cloud-generated notebook download** (`§13.2` of the ArcNotes requirements): Markdown documents, attachments, a machine-readable metadata and link manifest, and a fidelity report. It snapshots **acknowledged** revisions and states plainly that pending device-only edits are excluded until they synchronise (`EP-03`). **`EP-04` excludes** custom local encrypted export, native portable packages, HTML/PDF/DOCX pipelines and bit-for-bit archive round-trips; none is built. Ordinary clipboard and attachment saving remain.

**Testing requirements.** A Cloud export of a selected notebook verifying content, attachment hashes, link mapping and the declared loss report (`§13.3` there); an export interrupted and retried; an export while pending device edits exist, asserting they are **excluded and the exclusion stated** (`EP-03`); an export after a paid term ends, asserting retained data is still exportable within its bounded artifact lifetime (`EP-02`); a fidelity-statement check for each lossy target; a large-corpus export performance measurement.

**Completion gate.** A Cloud export produces Markdown, attachments, a link manifest and a fidelity report over acknowledged revisions, with pending edits excluded and said so; and every lossy target states its losses before writing. **This satisfies `PG-07` for ArcNotes.**

### WP-19.06 — The repository-projection prohibition

> **This step builds nothing.** It replaces a Git-friendliness step that `§14` of the data-format requirements retired, gates included. A retired delivery still needs an assertion, because the way an excluded feature returns is by a later package quietly adding it.

**What must be fully done.** A structural assertion that **no ArcNotes assembly — and no assembly it references — carries a repository-projection writer, a Git client dependency or an LFS path** (`§14` and `EX-09` of the data-format requirements). The exclusion is recorded where a reader looks for the feature, so a user asking for a Git-backed notebook gets the stated answer instead of a silent absence (`EE-04` of the data-format requirements; `EP-05` of the policy requirements).

**Testing requirements.** A dependency-policy test failing the build on a Git or LFS client package reference from any ArcNotes project; a structural test asserting no type implements or is named as a projection writer; a presentation test asserting the excluded capability is explained rather than merely hidden.

**Completion gate.** **No projection path exists and none can be added without failing the build**, and the exclusion is stated to the user rather than left as a gap.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The search index as a derived store with its own lifecycle |
| Protocol | Search and export capabilities become invocable |
| UI | Search surface, saved views, import review and export dialogs |
| Security | Permission-aware querying; import treats source content as untrusted |
| Platform | File dialogs, printing and path handling per platform |
| Migration | Export format versioning begins |
| Compatibility | The import fixture set fixes the compatibility claims ArcNotes makes |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Index divergence, rebuild equivalence and latency results | `WP-19.00` |
| Filter, permission and ranking results | `WP-19.01` |
| Anchor survival and invalidity results | `WP-19.02` |
| Saved view ownership and freshness results | `WP-19.03` |
| Per-source import results, immutability assertion, partial-failure report | `WP-19.04` |
| Cloud export content, attachment-hash, link-manifest and fidelity results | `WP-19.05` |
| Dependency-policy, structural and presentation results proving **no repository-projection or Git/LFS path exists** | `WP-19.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. The index never diverges after a crash, rebuilds to an equivalent state, and meets query latency budget at scale.
2. Permission is applied during query evaluation; refused content is invisible in results and counts.
3. Citation anchors survive surrounding edits and report invalidity explicitly.
4. A saved view owns no content and always reflects current data.
5. Every declared import source has a fixture, imports correctly, never modifies the source, and reports partial failure honestly — **this is what satisfies `PG-07` for ArcNotes**, which is a fixture obligation on *import*, not on export.
6. A Cloud export is complete, verifiable and honest about what it omits; every lossy target states its losses before writing.
7. **No repository-projection or Git/LFS path exists in ArcNotes or its dependencies**, the build fails if one is added, and the exclusion is explained rather than hidden.
8. **Search over hydrated content survives a Cloud outage**, and pending work remains durably recoverable. Export is a Cloud operation and is unavailable during an outage, which the interface states rather than failing opaquely.

---

## 9. Dependencies

**Upstream.** `18` (the document model, link index and attachments).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `20` — First workflow | Search and artifact production for the real workflow |
| `25` — Sync | A format proven to round-trip locally before it round-trips through a server |
| `28` — Bounded properties and views | The V1 baseline plus a proven export path to extend. **`27` is retired by P2-006** |
| `40` — Knowledge | The local index and citation anchors retrieval builds on |
