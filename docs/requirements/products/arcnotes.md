# ArcNotes — Product Requirements

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements / Products
> Product identity: `arcnotes` · Positioning: **Local-first Professional Knowledge & Document Workspace**
> Governing authority: **D-006** (complete scope: Canvas, Database and Slides are in scope, phased), **D-002** (Edgeless Canvas is an ArcNotes capability, never a product)
> Companions: [`../06-knowledge-search-and-retrieval.md`](../06-knowledge-search-and-retrieval.md), [`../13-data-formats-and-portability.md`](../13-data-formats-and-portability.md), [`arcchat.md`](arcchat.md)

> **ArcNotes is a document-first, block-based, local-first professional knowledge and documentation system, and the long-term knowledge authority of ArcForges.**

---

## 1. Scope

### 1.1 Complete scope versus V1 baseline

**D-006 is binding.** The document core is the **V1 baseline, not the ceiling of the product**.

| Capability family | Status |
|---|---|
| **Document core** | V1 — this document's §3–§13 |
| **Edgeless Canvas** | **In complete scope**, phased after the document core stabilises |
| **Typed multi-view Database** | **In complete scope**, phased, built on typed properties, queries and saved views |
| **Slides / Presentation** | **In complete scope**, phased, defaulting to a **presentation view over document and canvas content** rather than a third content model |
| Real-time multi-user collaboration | Later; compatibility must be preserved from the start |

| # | Requirement |
|---|---|
| SC-01 | "Incorporate in full, in phases" means all three families are in scope. **It does not mean feature-for-feature parity with any external product.** Depth is decided by the ArcNotes Reference Coverage Matrix using Copy / Rewrite / Improve / Replace / Reference Only / Drop (**D-006**, **D-012**). |
| SC-02 | **No fake empty Canvas, Database or Slides implementations may be created** (**D-006**). |
| SC-03 | **ArcNotes Edgeless Canvas is an ArcNotes capability, never a standalone product** (**D-002**). |

### 1.2 V1 compatibility hooks — binding from the beginning

**D-006** makes these binding from the first line of code:

| # | Hook |
|---|---|
| CH-01 | Stable Document/Space and Block identities, with revisions and unified reference semantics |
| CH-02 | A block model that permits later addition of Surface/Canvas block types |
| CH-03 | Canvas spatial positions, connectors, groupings and layout data **isolated from ordinary document layout** |
| CH-04 | Typed properties, queries and saved views as the multi-view database foundation |
| CH-05 | **No stuffing of future fields into the core Block** |
| CH-06 | Block types and extension types registered **statically or by source generation** under AOT (**D-008**) |
| CH-07 | `DocumentId` / `BlockId` / `Operation` / `Revision` preserving future collaboration compatibility from the start, even though V1 implements no real-time collaboration |

---

## 2. Product principles

| # | Principle |
|---|---|
| PR-01 | **Document-first, not database-first.** A note is a document; the database capability grows over documents, not the reverse. |
| PR-02 | **Local-first.** Full capability with no account and no network. |
| PR-03 | **Canonical Document ≠ Markdown file** (`I-190`). Markdown is a first-class **interchange** format, not the runtime authority. |
| PR-04 | **Not being Markdown internally must not create lock-in.** Portability is guaranteed by first-class import and export (§12), not by adopting a lossy runtime format. |
| PR-05 | **ArcNotes is the long-term knowledge authority** (`§9` of the knowledge requirements). ArcChat references and retrieves; it never becomes a second knowledge store. |
| PR-06 | **ArcNotes does not become a Notion-style database and application builder.** It implements its own typed database and multi-view capability at a depth ArcForges chooses. |

### 2.1 Three depths of use

ArcNotes must serve, in one product: quick capture and everyday notes; structured personal knowledge with links, properties and retrieval; and long professional documents with history, attachments and export.

---

## 3. Organisation model

```
Notebook
 └── Folder (hierarchical)
      └── Document
           └── Block (hierarchical)
```

| # | Requirement |
|---|---|
| OR-01 | **Notebook = the top-level ArcNotes knowledge/document container.** |
| OR-02 | **Notebooks do not nest.** Hierarchy is provided by folders. |
| OR-03 | **Notebook ≠ ArcForges Workspace** (`I-460`). A workspace is the cloud tenancy boundary; a notebook is an ArcNotes container. |
| OR-04 | **A local-only notebook is a first-class, permanent state** requiring no workspace. |
| OR-05 | **The notebook is the default ArcNotes cloud sync scope** (`SY-01`). |
| OR-06 | **Folder = hierarchical location organisation inside a notebook.** |
| OR-07 | **Documents do not nest inside documents.** Document hierarchy must not be used as a substitute for folders. |
| OR-08 | **`Folder ≠ Tag`** (`I-460`). Location and cross-cutting classification are separate. |

---

## 4. Document

| # | Requirement |
|---|---|
| DC-01 | **Document is the core authoritative object.** Quick notes, daily notes and long documents are **all documents**; `Note` is not a second data model (`I-461`). |
| DC-02 | A document carries at minimum: stable `DocumentId`, title, ordered block content, typed properties, tags, system metadata, revisions, and its notebook and folder placement. |
| DC-03 | **Title is an independent concept**, not merely the first heading block. |
| DC-04 | **Quick Capture creates an ordinary document** in a defined default location (an Inbox notebook or equivalent). **No `QuickNote` entity exists.** |
| DC-05 | **Daily Note is an ordinary document** created by a template or creation recipe. It is not a separate model. |
| DC-06 | **`Document ≠ File`** (`I-460`). |

---

## 5. Block

**Document = an ordered block structure.**

| # | Requirement |
|---|---|
| BL-01 | Every block has a **stable `BlockId`** that does **not** change under ordinary editing — editing text, moving, indenting or re-ordering preserves it. This is what makes block links, citations and future collaboration possible. |
| BL-02 | **Blocks support hierarchy** (nesting), independent of document nesting. |
| BL-03 | **`Block ≠ Markdown line`** (`I-460`). |
| BL-04 | **V1 first-party block types**: paragraph, headings, bulleted list, numbered list, checklist item, quote, callout, code, divider, table, math, image, file/attachment, PDF, embed/reference, toggle/collapsible. |
| BL-05 | **`ArcNotes.ChecklistItem ≠ ArcChat Agent Task`** (`I-464`). A checklist item is document content. It may later relate to an agent task explicitly; it is never silently one. |
| BL-06 | **Arbitrary HTML or script blocks are not offered in V1.** Extensibility goes through the extension model, out of process, with declared capability (`§8` of the extension requirements). |
| BL-07 | **Inline content** — bold, italic, code, links, mentions, math, footnote references — is modelled explicitly, not as embedded markup strings. |
| BL-08 | Block types are registered **statically or by source generation** (`CH-06`). |

---

## 6. Editor

**A rich block editor with Markdown-friendly interaction** — not a Markdown source editor.

| # | Requirement |
|---|---|
| ED-01 | Markdown keyboard syntax is supported as an **input convenience** (typing `#` produces a heading), never as the storage model. |
| ED-02 | A **slash menu** inserts blocks and applies content actions. |
| ED-03 | **The slash menu is not the command palette** (`CM-07`). The palette runs product commands; the slash menu inserts and transforms content. |
| ED-04 | Complete block operations: insert, delete, duplicate, move up/down, indent/outdent, convert type, split, merge, copy as, and multi-block operations. |
| ED-05 | **Multi-block selection is a first-class capability**, with keyboard and mouse, and all block operations available across a selection. |
| ED-06 | **Block drag and drop within a document is a move.** Cross-document and cross-application drops follow the shared semantics — Reference / Copy / Import — and are never silently destructive (`DD-01`–`DD-03`). |
| ED-07 | **A Table block is a document table, not a relational database engine.** V1 does not turn it into one (`PR-06`). |
| ED-08 | An **Outline** view derives from headings. |

---

## 7. Properties, tags and views

| # | Requirement |
|---|---|
| PT-01 | **Typed properties are distinct from tables** (`I-462`). Properties describe the document; a table is content inside it. |
| PT-02 | Property types include at minimum: text, number, date, checkbox, select, multi-select, URL, relation to a document, and person or actor where applicable. |
| PT-03 | **System properties and user properties are separated.** Created time, modified time, author and revision are system-owned and not user-editable as arbitrary fields. |
| PT-04 | **Properties must not make ordinary notes heavy.** A plain note has no mandatory property ceremony. |
| PT-05 | **`Property ≠ document content`** (`I-462`). |
| PT-06 | **Tag = cross-cutting classification.** A tag carries no hierarchical location (`OR-08`). |
| PT-07 | **Deleting a tag never deletes documents** (`I-462`); it removes a classification. |
| PT-08 | Tag scope follows data-ownership scope, not a global namespace across unrelated notebooks. |
| PT-09 | **Saved View = a saved query plus sort, filter and view configuration.** |
| PT-10 | **A saved view owns nothing** (`I-462`). Deleting a view deletes the view definition only. |
| PT-11 | **V1 may provide a list view only**; the model supports further view kinds as the database capability phases in. |
| PT-12 | **Favorites and Recent are user-level presentation state**, and Recent is derived. Neither is content. |

---

## 8. Links and references

| # | Requirement |
|---|---|
| LK-01 | **Internal links target a stable document identity**, never a title or a path. |
| LK-02 | **Renaming a document never breaks a link** (`SY-11`). |
| LK-03 | **Link display supports an alias**: target identity and display text are separate. |
| LK-04 | **Block links** target a stable `BlockId`. |
| LK-05 | **Backlinks are a derived relationship** from the link index. **They are never written into the document body** (`I-134`). |
| LK-06 | **A broken link has an explicit state** — target deleted, target unavailable, target in an unsynced notebook — and is never silently rendered as plain text. |
| LK-07 | **Reference embed renders another document or block as a reference view.** |
| LK-08 | **Editing authority for embedded content stays with the original object** (`WA-01`). An embed is never a second writable block. |
| LK-09 | A **Backlinks panel** lists incoming references with context. |

---

## 9. Attachments

Two categories, permanently separate (`I-193`):

| Category | Meaning |
|---|---|
| **Managed Attachment** | Added into ArcNotes; ArcNotes owns identity, lifecycle, hash, sync and backup |
| **External Attachment Reference** | Left where the user put it; ArcNotes references and does not own it |

| # | Requirement |
|---|---|
| AT-01 | Dragging an ordinary small file into a document creates a **managed attachment** by default. |
| AT-02 | A large file, or one obviously belonging to an external library, prompts for the choice rather than silently copying (`AS-03`). |
| AT-03 | **An attachment is never base64-embedded into document content** (`I-463`). |
| AT-04 | **An image block references an attachment**; image editing is not part of ArcNotes. |
| AT-05 | **PDF is supported as a first-class attachment** with in-product viewing, page-anchored annotation targets and citation anchors. |
| AT-06 | **Extracted PDF text is derived data** (`IP-09`), rebuildable, and never canonical. |
| AT-07 | **Attachment availability is an explicit state**: present locally, cloud-only, downloading, missing external, or unavailable — with recovery affordances (`AS-04`). |

---

## 10. Search and knowledge

| # | Requirement |
|---|---|
| SR-01 | Search is a first-class ArcNotes capability, in three scopes: **within the current document**, **within the current notebook**, **across all local notebooks** (plus cloud where enabled). |
| SR-02 | **Basic search never requires AI** (`IX-03`). Full-text and metadata search work with no model present. |
| SR-03 | Search filters cover notebook, folder, tag, property, date range, block type and attachment presence. |
| SR-04 | **A search result locates the specific block** wherever possible, so opening lands the user at the match. |
| SR-05 | **Semantic search is an enhancement, never a replacement** (`IX-04`). With the semantic index unavailable, ordinary search still works. |
| SR-06 | Semantic search may be **local or cloud**, and these are separate policy decisions (`§4` of the knowledge requirements). |
| SR-07 | The **knowledge status of a notebook is visible**: indexed, partially indexed, not indexed, excluded, stale. |
| SR-08 | **Knowledge is a projection, never a second copy** (`I-134`). Documents and attachments are the source. |
| SR-09 | **Knowledge participation is per notebook with per-document override** (`KS-06`). |
| SR-10 | **Knowledge eligibility is separate from ordinary search permission** (`I-253`). |
| SR-11 | **Cloud knowledge is never automatically enabled** by enabling sync (`I-182`, `PL-06`). |

---

## 11. AI in ArcNotes

Three layers, with a firm boundary at the third:

| Layer | What it is |
|---|---|
| **1 — Editor AI actions** | Selection-scoped actions: summarise, rewrite, translate, extract, continue, fix, explain |
| **2 — Ask ArcChat** | Hands a context reference to ArcChat and receives an answer or an artifact |
| **3 — Agent-driven ArcNotes capabilities** | ArcChat's agent invokes ArcNotes capabilities under the full permission model |

| # | Requirement |
|---|---|
| AI-01 | **ArcNotes native AI does not require ArcChat to be installed** (`§3.2` of the product scope). Layer 1 works standalone with local AI or BYOK. |
| AI-02 | **ArcNotes does not implement a second agent orchestration platform** (`I-030`). Complex orchestration belongs to ArcChat. |
| AI-03 | **"Ask ArcChat" passes a context reference, never a blanket copy** (`CX-03`). |
| AI-04 | **Clicking "Ask ArcChat" must never upload an entire notebook.** The minimum necessary context is passed (`AS-08`). |
| AI-05 | **Every AI modification carries provenance** (`SY-21`): actor is the agent, with task, capability and approval reference. |
| AI-06 | **A checkpoint is created before any large-scale agent modification** (`CK-02`), labelled meaningfully ("before agent edit"). |
| AI-07 | **A complex AI edit supports Review Changes** — a diff the user accepts or rejects — before it is committed. |
| AI-08 | **A small AI insertion does not require a full diff interface**; it is an ordinary undoable edit. |

### 11.1 Capabilities exposed to ArcChat

ArcNotes contributes **context providers**, **agent capabilities**, **artifact handlers**, **actions**, **suggested tasks** and **deep link targets** (`AP-06` in the ArcChat requirements). Capability families include: query and search; read document and block; create document; insert, update and restructure blocks; manage properties and tags; manage links; manage attachments; create checkpoints; export; and delete.

| # | Requirement |
|---|---|
| CP-01 | **Deletion capabilities exist and are high-risk**, carrying elevated risk level, explicit approval and a checkpoint (`R2`–`R4` per operation scale). |
| CP-02 | **ArcNotes is an artifact handler**: a task producing a report creates an **ArcNotes Document owned by ArcNotes**, and ArcChat receives an `ArtifactRef` (`AR-01`). |
| CP-03 | **An ArcScope report becoming an ArcNotes document is a copy/import**, creating a new ArcNotes-owned object with provenance — never a shared writable object (`§4.2` of the product scope). |
| CP-04 | **An ArcNotes document may reference an ArcScope resource** by `ResourceRef`, without owning it. |

---

## 12. History, recovery and deletion

Four separate levels (`I-201`–`I-205`):

| Level | Meaning |
|---|---|
| **Undo / Redo** | In-session, semantic-command based |
| **Document Revision History** | Durable committed history |
| **Checkpoint** | A named recovery landmark |
| **Trash** | Deleted items pending purge |

| # | Requirement |
|---|---|
| HR-01 | **History UI displays the actor** — user, or agent with its task — so "why did this change?" is answerable. |
| HR-02 | **Restoring an earlier state does not delete subsequent history.** Restore creates a new revision. |
| HR-03 | **Local history is not a cloud-only capability.** Local revision history, checkpoints and trash are free local features; the cloud adds cross-device version history and deleted-item recovery. |
| HR-04 | **Restoring from trash preserves the `DocumentId`** (`DE-03`). |
| HR-05 | **Deleting a folder moves the folder and its descendants to trash.** |
| HR-06 | **Deleting a tag has entirely different semantics**: documents are untouched (`PT-07`). |
| HR-07 | **Deleting a saved view deletes the view definition only** (`PT-10`). |
| HR-08 | Crash recovery follows [`../13-data-formats-and-portability.md`](../13-data-formats-and-portability.md) §9: everything reported saved survives; a damaged derived index never produces "corrupt". |

---

## 13. Import and export

### 13.1 Import

| # | Requirement |
|---|---|
| IM-01 | **Import is a first-class ArcNotes capability**, not an afterthought. |
| IM-02 | **First official import families**: Markdown files and folders, an Obsidian-style vault, a Notion-style export, plain text, HTML, and ArcNotes' own native package. |
| IM-03 | **Import is always non-destructive** (`IM-04` in the data requirements). It creates ArcNotes objects; it never mutates or deletes the source. |
| IM-04 | **Import preserves relationships wherever possible**: internal links, attachments, tags, properties, folder structure and dates. |
| IM-05 | **Every import produces a report** (`IM-05` in the data requirements): imported, skipped, approximated, preserved-unmapped, and lost. |
| IM-06 | **Repeated import identifies its origin** so a second run can update rather than duplicate (`IM-03`, `IM-04` in the data requirements). |
| IM-07 | **V1 does not implement real-time bidirectional Markdown folder mirroring** (`EE-01`). Import and export are the boundary. A **Linked Vault Mode** is a possible later capability, and only as an explicitly declared mode with declared writer authority. |

### 13.2 Export

**Export must be more reliable than import, because it is the user's exit freedom.**

| Format | Fidelity |
|---|---|
| **ArcNotes native package** | Full fidelity |
| **Markdown** | High fidelity for representable content, with a loss report |
| **HTML** | Presentation fidelity |
| **PDF** | Fixed-layout sharing and printing |
| **Plain text / clipboard** | Lossy by design |
| **DOCX** | Later; the architecture supports it |

| # | Requirement |
|---|---|
| EX-01 | **Content Markdown cannot represent** — typed properties, certain block types, embeds, canvas content later — is handled by a declared strategy: front-matter, a sidecar, an approximation, or an explicit loss entry. **Silent loss is prohibited** (`EX-03` in the data requirements). |
| EX-02 | **External attachments are excluded from export by default**, with an explicit "collect external attachments" option (`EX-07` in the data requirements). |
| EX-03 | Every export declares its round-trip level (`EX-01` in the data requirements). |

---

## 14. Cloud behaviour

| # | Requirement |
|---|---|
| CL-01 | **ArcNotes' cloud data capabilities do not depend on ArcChat** (**D-010**). |
| CL-02 | **The notebook is the cloud enablement unit** (`OR-05`), enabled explicitly per notebook. |
| CL-03 | **Nothing is uploaded automatically after sign-in** (`ID-06`). |
| CL-04 | **A synced notebook still holds a complete local replica.** It is a local-first replicated notebook, **not** a cloud document with a cache. |
| CL-05 | **With Cloud unavailable**, everything local continues; sync queues; the state is visible and non-alarming. |
| CL-06 | **Storage full** pauses cloud writes only; local editing and saving continue (`ST-06`). |
| CL-07 | **A new device fetches metadata and small content first**; attachments hydrate per policy (`AS-08`). |
| CL-08 | **Attachment availability policy is user-controlled** per notebook (`AS-07`). |
| CL-09 | **Cloud search covers only synced and authorised content**, and content is never uploaded merely to make cloud search work (`SR-08` in the knowledge requirements). |

---

## 15. Window and session behaviour

| # | Requirement |
|---|---|
| WN-01 | Multi-window and split view are supported (`WN-02`). |
| WN-02 | **The same document open in several windows of one process shares one logical document session and one write authority** (`WN-04`). |
| WN-03 | **Window physical coordinates are device-local** (`WN-05`); a named layout is the syncable concept (`LY-03`). |
| WN-04 | Document tabs, breadcrumb and an inspector panel (properties, backlinks, outline, history, attachments) are provided. |
| WN-05 | **Breadcrumb shows the ArcNotes location** — notebook and folder — not a cloud workspace path. |

---

## 16. First run

| # | Requirement |
|---|---|
| FR-01 | **No account required**; the editor is usable immediately (`ID-01`). |
| FR-02 | **First value within seconds**: create a note and start typing. |
| FR-03 | **AI configuration must never block the editor** (`AI-13` in the ArcChat requirements applied here). |
| FR-04 | **ArcChat absent changes nothing about core ArcNotes** (`§3.1` of the product scope). AI actions that require ArcChat show as ecosystem capabilities that are currently unavailable. |
| FR-05 | Startup meets the budget in [`../12-quality-and-compatibility-contract.md`](../12-quality-and-compatibility-contract.md) §5, with no cloud dependency in the startup path. |

---

## 17. Non-goals

ArcNotes is **not**: a Notion clone or an application builder; a spreadsheet; a project-management suite; an image editor; a real-time collaborative editor in V1; a Markdown folder mirror; or a second agent platform.

**A knowledge graph, if offered, is a derived view of the link graph** — never a separate authoritative store (`IX-06`).

**A web clipper**, if offered later, is an import path producing ordinary ArcNotes documents, not a live external mirror.

**Checklist items may relate to agent tasks later, explicitly** (`BL-05`); they never become tasks implicitly.

---

## 18. Domain model

```
Notebook · Folder · Document · Block · BlockType · InlineContent
DocumentProperty · PropertyDefinition · Tag · DocumentTag
DocumentLink · BlockLink · ReferenceEmbed
Attachment · ManagedAttachment · ExternalAttachmentReference
DocumentTemplate · SavedView
DocumentRevision · DocumentCheckpoint · DocumentTrashEntry
DocumentSession
SearchResult · SearchScope · KnowledgeEligibility · IndexState
ImportJob · ImportOrigin · ExportJob
ArcNotesArtifactReference
```

Reserved for the phased capabilities, consistent with `CH-01`–`CH-07`: surface/canvas block types with isolated spatial data; query, view kind and database view definitions over typed properties; and presentation view definitions over document and canvas content.

---

## 19. V1 scope

| Area | V1 |
|---|---|
| **Content** | Notebook, folder, document, block editor, rich text, lists and checklists, code, table, math, image/file/PDF |
| **Organisation** | Tags, properties, favorites, recent, internal links, backlinks, outline |
| **Retrieval** | Full-text search, metadata filters, basic saved views |
| **Reliability** | Autosave, undo/redo, history, checkpoint, trash, crash recovery |
| **Portability** | Markdown import and export, plain text, HTML, PDF export, vault-style import |
| **AI** | Selection AI actions, Ask ArcChat, ArcChat context and capabilities, agent provenance and checkpoints |
| **Cloud** | Explicit notebook sync, managed attachment sync, cloud status, version and recovery integration |

A Notion-style importer may land in V1 or shortly after; **the architecture supports it directly**.

---

## 20. Reference relationship

**AFFiNE and SiYuan are ArcNotes references** (**D-012**) — sources of features, behaviour, tests and migration evidence, **never architecture authorities or parity commitments**.

| # | Requirement |
|---|---|
| RF-01 | An **ArcNotes Reference Coverage Matrix** is required before ArcNotes implementation planning is finalised (**D-012**, **D-006**), mapping each reference feature to Copy / Rewrite / Improve / Replace / Reference Only / Drop, to a phase (V1 / Edgeless / Database / Slides / later collaboration), to a target domain, data, UI or contract area, and to a test and completion gate. |
| RF-02 | **Reuse is licence-gated and provenance-gated** (**D-013**). File-level SPDX evidence against the local repository baseline is required before any copy, translation or port — the **F-013** gate. AGPL-identified material is behavioural reference only, implemented independently. |
| RF-03 | Reference material informs feature depth; **the target runtime architecture is ArcForges' own** — C#, Avalonia, Native AOT, the ArcForges domain and persistence model. |

---

## 21. Acceptance scenarios

**Basic** — no account, no network; create a notebook, folder and document; edit; save; reopen; search; export.

**Block identity** — editing text, moving, indenting and reordering a block preserve its `BlockId`; a block link still resolves afterwards.

**Rename** — renaming a document leaves every internal link intact.

**Backlinks** — a link creates a backlink; deleting the source removes it; the backlink was never written into the target's body.

**Broken link** — a deleted target produces an explicit broken-link state, not silent plain text.

**Attachments** — a small drop becomes managed; a large external file prompts; nothing is base64-embedded; a missing external attachment produces a recoverable state.

**Search** — full-text works with no model; a result lands on the matching block; with the semantic index down, search still works.

**Knowledge policy** — a notebook excluded from AI is still searchable by title and keyword; enabling sync does not enable cloud AI indexing.

**AI** — a selection action works with local BYOK and no ArcChat; "Ask ArcChat" passes a reference rather than the notebook; an agent edit creates a checkpoint and carries provenance; Review Changes gates a large edit.

**Cross-application** — ArcChat requests a report; ArcNotes creates the document; the document is ArcNotes-owned; ArcChat holds an `ArtifactRef`; deleting the artifact entry leaves the document.

**History** — restore an old revision; subsequent history remains; trash restore preserves `DocumentId`; deleting a tag deletes no documents.

**Import/export** — a vault import is non-destructive, preserves links and produces a report; re-import updates rather than duplicating; Markdown export reports what it could not represent; native export round-trips losslessly.

**Cloud** — enabling notebook sync uploads nothing until confirmed; a synced notebook remains fully editable offline; storage-full pauses upload only; a new device shows documents before attachments finish.

**Reliability** — kill the process immediately after typing; the change is present on restart; a corrupted search index rebuilds without any claim of document corruption.

**Compatibility hooks** — adding a surface/canvas block type later requires no change to existing document data; typed properties already support the query and saved-view foundation.

---

## 22. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 15` | The complete ArcNotes product specification: organisation model, document and block model, editor, properties and tags, links and references, attachments, search and knowledge, AI layers, history and deletion, import and export, cloud behaviour, windows, first run, non-goals, domain model and V1 scope |
| `I2 §II` | The V1 compatibility hooks made binding by **D-006** |
| `I4 §Stage 13 §18–20` | ArcNotes as the long-term knowledge authority and its owned state |
| `I4 §Stage 22 §23–26`, `§195` | ArcNotes storage strategy and local structure |
| `I4 §Stage 23 §138–139` | ArcNotes knowledge responsibilities |
| **D-002** | Edgeless Canvas is an ArcNotes capability, never a product |
| **D-006** | Complete scope with phased Canvas, Database and Slides; binding V1 hooks; no fake empty implementations |
| **D-012**, **D-013** | AFFiNE and SiYuan as licence-gated references with a required coverage matrix |
