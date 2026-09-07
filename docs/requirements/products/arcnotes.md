# ArcNotes — Product Requirements
> Current scope amendment: **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements / Products
> Product identity: `arcnotes` · Positioning: **Cloud-backed Personal Knowledge & Document Workspace**
> Governing authority: **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** amends [D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006); [D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002) and [D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)/[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013) retain portfolio and reference boundaries.
> Companions: [`../06-knowledge-search-and-retrieval.md`](../06-knowledge-search-and-retrieval.md), [`../13-data-formats-and-portability.md`](../13-data-formats-and-portability.md), [`arcchat.md`](arcchat.md)

> **ArcNotes is a document-first, block-based notebook application with cloud history and multi-device sync. Its native editor uses durable working caches; the Cloud Notes module owns acknowledged document revisions.**

---

## 1. Scope

### 1.1 Current complete scope

The notebook core and cloud continuity are the product. Reference applications inform behaviour and correctness; their feature catalogues do not expand this scope.

| Capability family | Delivery |
|---|---|
| Document core | Rich text, document/folder hierarchy, stable blocks, block references, backlinks, outline, tags, search, attachments, undo, history and trash |
| Properties and views | Common scalar properties, saved list/table views, filtering, sorting and bounded queries |
| Cloud | Single-owner workspace, multi-device revisions/conflicts, attachment availability and recovery |
| AI | Selection actions and product tools executed through the Cloud AI service |
| Excluded | Edgeless/whiteboard, shapes/connectors/spatial workbench, frames/frame ordering, slides/presentations, spaced repetition/flashcards, DOCX import, formula/relation/rollup engines and collaboration |

| # | Requirement |
|---|---|
| SC-01 | Deliver the notebook scope above. AFFiNE and SiYuan are behaviour references; no external-product parity or phased presentation/whiteboard obligation remains. |
| SC-02 | No empty implementation, reserved project, schema hook or acceptance gate is created for an excluded capability. |
| SC-03 | Retired by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006): Edgeless Canvas is not a current ArcNotes capability or separate product. |

### 1.2 Required foundations

| # | Hook |
|---|---|
| CH-01 | Stable notebook/document/block identities, explicit revisions and unified reference semantics support edits and multi-device conflict handling. |
| CH-02 | Retired by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006): no required future Surface/Canvas block extension. |
| CH-03 | Retired by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006): no canvas positions, connectors, frames or spatial-layout storage. |
| CH-04 | Typed scalar properties, bounded queries and saved views support notebook organisation. |
| CH-05 | No speculative fields in core blocks for excluded product families. |
| <a id="rule-ch-06"></a>CH-06 | Supported block types use static/source-generated registration compatible with Native AOT. |
| CH-07 | Stable IDs, base revisions, outbox/inbox and tombstones serve single-user multi-device sync; no CRDT, membership, shared cursors or future-collaboration reservation. |

---

## 2. Product principles

| # | Principle |
|---|---|
| PR-01 | **Document-first, not database-first.** A note is a document; the database capability grows over documents, not the reverse. |
| <a id="rule-pr-02"></a>PR-02 | **Cloud-backed with native editing.** A realm/workspace is required for notebook enrolment. Previously hydrated notes remain editable/searchable offline; pending edits survive crashes and are distinct from acknowledged Cloud versions. |
| PR-03 | **Canonical Document ≠ Markdown file** ([I-190](../01-normative-glossary-and-invariants.md#rule-i-190)). Markdown is a first-class **interchange** format, not the runtime authority. |
| PR-04 | Basic data portability is provided by the Cloud export in §13; no proprietary encrypted local package is required. |
| PR-05 | **ArcNotes is the long-term knowledge authority** (`§9` of the knowledge requirements). ArcChat references and retrieves; it never becomes a second knowledge store. |
| <a id="rule-pr-06"></a>PR-06 | ArcNotes provides bounded notebook properties and query views. It does not implement a spreadsheet, relational application builder or complete reference-product database engine. |

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
| OR-03 | **Notebook ≠ ArcForges Workspace** ([I-460](../01-normative-glossary-and-invariants.md#rule-i-460)). A workspace is the cloud tenancy boundary; a notebook is an ArcNotes container. |
| OR-04 | Every notebook belongs to one single-owner Cloud workspace. Device cache availability is a local policy, not a permanent local-only notebook ownership mode. |
| OR-05 | **The notebook is the default ArcNotes cloud sync scope** ([SY-01](../03-cloud-services-and-sync.md#rule-sy-01)). |
| OR-06 | **Folder = hierarchical location organisation inside a notebook.** |
| OR-07 | **Documents do not nest inside documents.** Document hierarchy must not be used as a substitute for folders. |
| <a id="rule-or-08"></a>OR-08 | **`Folder ≠ Tag`** ([I-460](../01-normative-glossary-and-invariants.md#rule-i-460)). Location and cross-cutting classification are separate. |

---

## 4. Document

| # | Requirement |
|---|---|
| DC-01 | **Document is the core authoritative object.** Quick notes, daily notes and long documents are **all documents**; `Note` is not a second data model ([I-461](../01-normative-glossary-and-invariants.md#rule-i-461)). |
| DC-02 | A document carries at minimum: stable `DocumentId`, title, ordered block content, typed properties, tags, system metadata, revisions, and its notebook and folder placement. |
| <a id="rule-dc-03"></a>DC-03 | **Title is an independent concept**, not merely the first heading block. |
| DC-04 | **Quick Capture creates an ordinary document** in a defined default location (an Inbox notebook or equivalent). **No `QuickNote` entity exists.** |
| DC-05 | **Daily Note is an ordinary document** created by a template or creation recipe. It is not a separate model. |
| DC-06 | **`Document ≠ File`** ([I-460](../01-normative-glossary-and-invariants.md#rule-i-460)). |

---

## 5. Block

**Document = an ordered block structure.**

| # | Requirement |
|---|---|
| <a id="rule-bl-01"></a>BL-01 | Every block has a stable BlockId under editing, moves, indentation and reordering. References and multi-device revision reconciliation depend on this identity. |
| <a id="rule-bl-02"></a>BL-02 | **Blocks support hierarchy** (nesting), independent of document nesting. |
| BL-03 | **`Block ≠ Markdown line`** ([I-460](../01-normative-glossary-and-invariants.md#rule-i-460)). |
| <a id="rule-bl-04"></a>BL-04 | **V1 first-party block types**: paragraph, headings, bulleted list, numbered list, checklist item, quote, callout, code, divider, table, math, image, file/attachment, PDF, embed/reference, toggle/collapsible. |
| <a id="rule-bl-05"></a>BL-05 | **`ArcNotes.ChecklistItem ≠ ArcChat Agent Task`** ([I-464](../01-normative-glossary-and-invariants.md#rule-i-464)). A checklist item is document content. It may later relate to an agent task explicitly; it is never silently one. |
| <a id="rule-bl-06"></a>BL-06 | **Arbitrary HTML or script blocks are not offered in V1.** Extensibility goes through the extension model, out of process, with declared capability (`§8` of the extension requirements). |
| <a id="rule-bl-07"></a>BL-07 | **Inline content** — bold, italic, code, links, mentions, math, footnote references — is modelled explicitly, not as embedded markup strings. |
| <a id="rule-bl-08"></a>BL-08 | Block types are registered **statically or by source generation** ([CH-06](#rule-ch-06)). |

---

## 6. Editor

**A rich block editor with Markdown-friendly interaction** — not a Markdown source editor.

| # | Requirement |
|---|---|
| <a id="rule-ed-01"></a>ED-01 | Markdown keyboard syntax is supported as an **input convenience** (typing `#` produces a heading), never as the storage model. |
| ED-02 | A **slash menu** inserts blocks and applies content actions. |
| <a id="rule-ed-03"></a>ED-03 | **The slash menu is not the command palette** ([CM-07](../09-shared-desktop-experience.md#rule-cm-07)). The palette runs product commands; the slash menu inserts and transforms content. |
| ED-04 | Complete block operations: insert, delete, duplicate, move up/down, indent/outdent, convert type, split, merge, copy as, and multi-block operations. |
| <a id="rule-ed-05"></a>ED-05 | **Multi-block selection is a first-class capability**, with keyboard and mouse, and all block operations available across a selection. |
| <a id="rule-ed-06"></a>ED-06 | **Block drag and drop within a document is a move.** Cross-document and cross-application drops follow the shared semantics — Reference / Copy / Import — and are never silently destructive ([DD-01](../09-shared-desktop-experience.md#rule-dd-01)–[DD-03](../09-shared-desktop-experience.md#rule-dd-03)). |
| <a id="rule-ed-07"></a>ED-07 | **A Table block is a document table, not a relational database engine.** V1 does not turn it into one ([PR-06](#rule-pr-06)). |
| <a id="rule-ed-08"></a>ED-08 | An **Outline** view derives from headings. |

---

## 7. Properties, tags and views

| # | Requirement |
|---|---|
| PT-01 | **Typed properties are distinct from tables** ([I-462](../01-normative-glossary-and-invariants.md#rule-i-462)). Properties describe the document; a table is content inside it. |
| PT-02 | Required property types: text, number, date/date-time, checkbox, single-select, multi-select and URL. Person/member fields, computed formulas, relationship properties and rollups are excluded. |
| PT-03 | **System properties and user properties are separated.** Created time, modified time, author and revision are system-owned and not user-editable as arbitrary fields. |
| PT-04 | **Properties must not make ordinary notes heavy.** A plain note has no mandatory property ceremony. |
| PT-05 | **`Property ≠ document content`** ([I-462](../01-normative-glossary-and-invariants.md#rule-i-462)). |
| PT-06 | **Tag = cross-cutting classification.** A tag carries no hierarchical location ([OR-08](#rule-or-08)). |
| <a id="rule-pt-07"></a>PT-07 | **Deleting a tag never deletes documents** ([I-462](../01-normative-glossary-and-invariants.md#rule-i-462)); it removes a classification. |
| PT-08 | Tag scope follows data-ownership scope, not a global namespace across unrelated notebooks. |
| PT-09 | **Saved View = a saved query plus sort, filter and view configuration.** |
| <a id="rule-pt-10"></a>PT-10 | **A saved view owns nothing** ([I-462](../01-normative-glossary-and-invariants.md#rule-i-462)). Deleting a view deletes the view definition only. |
| PT-11 | **V1 delivers saved list and table views.** A view selects authorised documents in a notebook, projects chosen properties and applies bounded typed filters and stable sorting. Calendar, board, gallery and spatial layouts are not required. |
| PT-12 | **Favorites and Recent are user-level presentation state**, and Recent is derived. Neither is content. |
| PT-13 | Property definitions and options have stable IDs. Renaming preserves existing values and view bindings; changing type requires validation and a loss preview. Incompatible values are preserved or the change is refused, never silently discarded. |
| PT-14 | Missing value differs from empty string, false and zero. Date/time zone, number comparison, case sensitivity, null ordering and an identity tie-breaker are declared so Cloud and native cached views agree. |
| PT-15 | View edits change the owning document property through the ordinary revision/conflict path. Deleting a view never deletes source documents. Unsupported query operators and excessive query complexity fail explicitly. |

---

## 8. Links and references

| # | Requirement |
|---|---|
| LK-01 | **Internal links target a stable document identity**, never a title or a path. |
| LK-02 | **Renaming a document never breaks a link** ([SY-11](../03-cloud-services-and-sync.md#rule-sy-11)). |
| LK-03 | **Link display supports an alias**: target identity and display text are separate. |
| LK-04 | **Block links** target a stable `BlockId`. |
| LK-05 | **Backlinks are a derived relationship** from the link index. **They are never written into the document body** ([I-134](../01-normative-glossary-and-invariants.md#rule-i-134)). |
| LK-06 | **A broken link has an explicit state** — target deleted, target unavailable, target in an unsynced notebook — and is never silently rendered as plain text. |
| LK-07 | **Reference embed renders another document or block as a reference view.** |
| LK-08 | **Editing authority for embedded content stays with the original object** ([WA-01](../13-data-formats-and-portability.md#rule-wa-01)). An embed is never a second writable block. |
| LK-09 | A **Backlinks panel** lists incoming references with context. |

---

## 9. Attachments

Two categories, permanently separate ([I-193](../01-normative-glossary-and-invariants.md#rule-i-193)):

| Category | Meaning |
|---|---|
| **Managed Attachment** | Added into ArcNotes; ArcNotes owns identity, lifecycle, hash, sync and backup |
| **External Attachment Reference** | Left where the user put it; ArcNotes references and does not own it |

| # | Requirement |
|---|---|
| <a id="rule-at-01"></a>AT-01 | Dragging an ordinary small file into a document creates a **managed attachment** by default. |
| <a id="rule-at-02"></a>AT-02 | A large file, or one obviously belonging to an external library, prompts for the choice rather than silently copying ([AS-03](../03-cloud-services-and-sync.md#rule-as-03)). |
| <a id="rule-at-03"></a>AT-03 | **An attachment is never base64-embedded into document content** ([I-463](../01-normative-glossary-and-invariants.md#rule-i-463)). |
| <a id="rule-at-04"></a>AT-04 | **An image block references an attachment**; image editing is not part of ArcNotes. |
| <a id="rule-at-05"></a>AT-05 | **PDF is supported as a first-class attachment** with in-product viewing, page-anchored annotation targets and citation anchors. |
| <a id="rule-at-06"></a>AT-06 | **Extracted PDF text is derived data** ([IP-09](../06-knowledge-search-and-retrieval.md#rule-ip-09)), rebuildable, and never canonical. |
| <a id="rule-at-07"></a>AT-07 | **Attachment availability is an explicit state**: present locally, cloud-only, downloading, missing external, or unavailable — with recovery affordances ([AS-04](../03-cloud-services-and-sync.md#rule-as-04)). |

---

## 10. Search and knowledge

| # | Requirement |
|---|---|
| SR-01 | Search is a first-class ArcNotes capability, in three scopes: **within the current document**, **within the current notebook**, **across hydrated notebooks** (with an explicit broader Cloud search scope). |
| SR-02 | **Basic search never requires AI** ([IX-03](../06-knowledge-search-and-retrieval.md#rule-ix-03)). Full-text and metadata search work with no model present. |
| SR-03 | Search filters cover notebook, folder, tag, property, date range, block type and attachment presence. |
| SR-04 | **A search result locates the specific block** wherever possible, so opening lands the user at the match. |
| SR-05 | **Semantic search is an enhancement, never a replacement** ([IX-04](../06-knowledge-search-and-retrieval.md#rule-ix-04)). With the semantic index unavailable, ordinary search still works. |
| SR-06 | Semantic retrieval and model-based embedding run only in Cloud and require service entitlement and explicit knowledge eligibility. Native full-text/metadata search over hydrated content remains available without AI. |
| SR-07 | The **knowledge status of a notebook is visible**: indexed, partially indexed, not indexed, excluded, stale. |
| SR-08 | **Knowledge is a projection, never a second copy** ([I-134](../01-normative-glossary-and-invariants.md#rule-i-134)). Documents and attachments are the source. |
| SR-09 | **Knowledge participation is per notebook with per-document override** ([KS-06](../06-knowledge-search-and-retrieval.md#rule-ks-06)). |
| SR-10 | **Knowledge eligibility is separate from ordinary search permission** ([I-253](../01-normative-glossary-and-invariants.md#rule-i-253)). |
| SR-11 | **Cloud knowledge is never automatically enabled** by enabling sync ([I-182](../01-normative-glossary-and-invariants.md#rule-i-182), [PL-06](../06-knowledge-search-and-retrieval.md#rule-pl-06)). |

---

## 11. AI in ArcNotes

Three layers, with a firm boundary at the third:

| Layer | What it is |
|---|---|
| **1 — Editor AI actions** | Selection-scoped actions: summarise, rewrite, translate, extract, continue, fix, explain |
| **2 — Ask ArcChat** | Hands a context reference to ArcChat and receives an answer or an artifact |
| **3 — Agent-driven ArcNotes capabilities** | The Cloud agent invokes authorized ArcNotes capabilities under the full permission model |

| # | Requirement |
|---|---|
| AI-01 | Selection AI actions call Cloud directly and do not require ArcChat Desktop. An authenticated workspace, active service term, allowed context and available capacity are required. No local AI or BYOK path exists. |
| AI-02 | ArcNotes has no agent loop. Cloud owns the single Harness; ArcChat provides task interaction and the authorised cross-product local-tool bridge. |
| AI-03 | **"Ask ArcChat" passes a context reference, never a blanket copy** ([CX-03](arcchat.md#rule-cx-03)). |
| AI-04 | **Clicking "Ask ArcChat" must never upload an entire notebook.** The minimum necessary context is passed ([AS-08](../06-knowledge-search-and-retrieval.md#rule-as-08)). |
| AI-05 | **Every AI modification carries provenance** ([SY-21](../03-cloud-services-and-sync.md#rule-sy-21)): actor is the agent, with task, capability and approval reference. |
| AI-06 | **A checkpoint is created before any large-scale agent modification** ([CK-02](../05-ai-and-agent-execution.md#rule-ck-02)), labelled meaningfully ("before agent edit"). |
| AI-07 | **A complex AI edit supports Review Changes** — a diff the user accepts or rejects — before it is committed. |
| AI-08 | **A small AI insertion does not require a full diff interface**; it is an ordinary undoable edit. |

### 11.1 Capabilities exposed to ArcChat

ArcNotes contributes **context providers**, **agent capabilities**, **artifact handlers**, **actions**, **suggested tasks** and **deep link targets** ([AP-06](arcchat.md#rule-ap-06) in the ArcChat requirements). Capability families include: query and search; read document and block; create document; insert, update and restructure blocks; manage properties and tags; manage links; manage attachments; create checkpoints; export; and delete.

| # | Requirement |
|---|---|
| CP-01 | **Deletion capabilities exist and are high-risk**, carrying elevated risk level, explicit approval and a checkpoint (`R2`–`R4` per operation scale). |
| CP-02 | **ArcNotes is an artifact handler**: a task producing a report creates an **ArcNotes Document owned by ArcNotes**, and ArcChat receives an `ArtifactRef` ([AR-01](arcchat.md#rule-ar-01)). |
| <a id="rule-cp-03"></a>CP-03 | **An ArcScope report becoming an ArcNotes document is a copy/import**, creating a new ArcNotes-owned object with provenance — never a shared writable object (`§4.2` of the product scope). |
| CP-04 | **An ArcNotes document may reference an ArcScope resource** by `ResourceRef`, without owning it. |

---

## 12. History, recovery and deletion

Four separate levels ([I-201](../01-normative-glossary-and-invariants.md#rule-i-201)–[I-205](../01-normative-glossary-and-invariants.md#rule-i-205)):

| Level | Meaning |
|---|---|
| **Undo / Redo** | In-session, semantic-command based |
| **Document Revision History** | Durable committed history |
| **Checkpoint** | A named recovery landmark |
| **Trash** | Deleted items pending purge |

| # | Requirement |
|---|---|
| HR-01 | **History UI displays the actor** — user, or agent with its task — so "why did this change?" is answerable. |
| <a id="rule-hr-02"></a>HR-02 | **Restoring an earlier state does not delete subsequent history.** Restore creates a new revision. |
| HR-03 | Cloud history is the acknowledged multi-device record. Local undo, recovery journal and unacknowledged edit checkpoints protect working changes; they do not form a second independently authoritative notebook history. |
| HR-04 | **Restoring from trash preserves the `DocumentId`** ([DE-03](../03-cloud-services-and-sync.md#rule-de-03)). |
| HR-05 | **Deleting a folder moves the folder and its descendants to trash.** |
| HR-06 | **Deleting a tag has entirely different semantics**: documents are untouched ([PT-07](#rule-pt-07)). |
| HR-07 | **Deleting a saved view deletes the view definition only** ([PT-10](#rule-pt-10)). |
| HR-08 | Crash recovery follows [`../13-data-formats-and-portability.md`](../13-data-formats-and-portability.md) §9: everything reported saved survives; a damaged derived index never produces "corrupt". |

---

## 13. Import and export

### 13.1 Import

| # | Requirement |
|---|---|
| IM-01 | Import remains a non-destructive way to move existing notes into a Cloud notebook. |
| <a id="rule-im-02"></a>IM-02 | Required formats are plain text and Markdown files/folders with local attachments and relative links, including an Obsidian-style folder/vault layout. DOCX, Notion-specific, HTML and proprietary full-fidelity package importers are not required. |
| IM-03 | Sources are never modified or deleted. Input size, attachment access and path traversal are validated before processing. |
| IM-04 | Preserve representable hierarchy, links, attachments, tags and metadata. Unsupported constructs are retained as safe text or reported; no silent loss or execution of embedded content. |
| IM-05 | Produce an import report: created, skipped, approximated, unresolved references and rejected files, with actionable reasons. |
| IM-06 | Import batches have stable origins and idempotency keys. Retrying the same batch cannot duplicate documents; deliberately importing again offers a preview before updates/copies. |
| <a id="rule-im-07"></a>IM-07 | No live bidirectional folder mirror, linked-vault mode or standalone local notebook is required. Staged import work remains recoverable until Cloud commit or explicit cancellation. |

### 13.2 Export

The required exit path is a **Cloud-generated notebook/account download**, with Markdown documents, attachments, a machine-readable metadata/link manifest and a fidelity report. It preserves access to user-created data without promising lossless interchange for every editor representation.

| # | Requirement |
|---|---|
| <a id="rule-ep-01"></a>EP-01 | Users select the notebooks/documents to export. Export validates owner/workspace access and reports missing or unavailable attachments; it never silently claims a complete result. |
| EP-02 | Export is available for retained data after a paid term ends. The downloadable artifact has a bounded lifetime and authorised access. Cancellation or expiry of that artifact does not delete source notes. |
| EP-03 | Snapshot the acknowledged source revisions. Pending device-only edits are not falsely included; the UI explains that they must synchronise first or be recovered locally. |
| <a id="rule-ep-04"></a>EP-04 | Custom local encrypted export, native portable packages, HTML/PDF/DOCX export pipelines and bit-for-bit native archive round-trips are not required. Ordinary clipboard/attachment saving and crash recovery are not removed. |

The earlier export identifiers remain binding within this narrower Cloud exit path:

| # | Requirement |
|---|---|
| EX-01 | Supported scalar properties, links and hierarchy that Markdown cannot represent use documented metadata/sidecars. Unsupported blocks/formatting receive explicit approximations or loss entries; no excluded canvas/presentation support is inferred. |
| EX-02 | External attachments are excluded by default. Only explicitly selected and authorized available bytes may be collected; device-only references are listed as unavailable until separately uploaded. |
| EX-03 | Every export declares its semantic round-trip/fidelity level. Markdown plus metadata is not advertised as a lossless native execution/archive format. |

### 13.3 Portability acceptance

Import a Markdown folder with nested links and attachments; retry without duplication; synchronise; export the selected notebook from Cloud; verify content, attachment hashes, link mapping and the declared loss report. Interrupt export and retry without changing source state. No DOCX importer or excluded package UI is reachable.

---

## 14. Cloud behaviour

| # | Requirement |
|---|---|
| CL-01 | **ArcNotes' cloud data capabilities do not depend on ArcChat** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |
| <a id="rule-cl-02"></a>CL-02 | Notebook creation/enrolment explicitly identifies the Cloud workspace. Subsequent notebook edits synchronise automatically under that enrolment; turning off device hydration does not change Cloud ownership. |
| CL-03 | Notebook onboarding explains that new documents and managed attachments will be stored in Cloud. Sign-in alone never uploads unrelated local files, existing external libraries or device folders. |
| CL-04 | Each device holds a selected, revision-labelled working cache, not a mandatory complete replica. Pending writes are durable and cannot be evicted before acknowledgement or explicit user discard. |
| <a id="rule-cl-05"></a>CL-05 | Cloud unavailability preserves editing and keyword search for hydrated content. Pending changes are visibly unsynchronised; unavailable content, AI and Cloud operations show specific unavailable states. |
| CL-06 | **Storage full** pauses cloud writes only; local editing and saving continue ([ST-06](../03-cloud-services-and-sync.md#rule-st-06)). |
| CL-07 | **A new device fetches metadata and small content first**; attachments hydrate per policy ([AS-08](../03-cloud-services-and-sync.md#rule-as-08)). |
| CL-08 | **Attachment availability policy is user-controlled** per notebook ([AS-07](../03-cloud-services-and-sync.md#rule-as-07)). |
| CL-09 | **Cloud search covers only synced and authorised content**, and content is never uploaded merely to make cloud search work ([SR-08](../06-knowledge-search-and-retrieval.md#rule-sr-08) in the knowledge requirements). |

---

## 15. Window and session behaviour

| # | Requirement |
|---|---|
| WN-01 | Multi-window and split view are supported ([WN-02](../09-shared-desktop-experience.md#rule-wn-02)). |
| WN-02 | **The same document open in several windows of one process shares one logical document session and one write authority** ([WN-04](#rule-wn-04)). |
| WN-03 | **Window physical coordinates are device-local** ([WN-05](../09-shared-desktop-experience.md#rule-wn-05)); a named layout is the syncable concept ([LY-03](../09-shared-desktop-experience.md#rule-ly-03)). |
| <a id="rule-wn-04"></a>WN-04 | Document tabs, breadcrumb and an inspector panel (properties, backlinks, outline, history, attachments) are provided. |
| WN-05 | **Breadcrumb shows the ArcNotes location** — notebook and folder — not a cloud workspace path. |

---

## 16. First run

| # | Requirement |
|---|---|
| FR-01 | First notebook use signs into a realm and selects its workspace. Returning users open authorized cached content during outages. Sign-out blocks normal workspace views; the explicit local pending-work recovery path in identity [DL-01](../02-identity-account-and-workspace.md#rule-dl-01) is a narrow exception, not account-free notebook creation or AI. |
| FR-02 | After account/workspace setup, first value is creating a note and typing immediately; shell startup never waits for background hydration/indexing. |
| FR-03 | AI entitlement, provider availability and model configuration never block ordinary editing of available content. |
| FR-04 | ArcChat absence does not disable ArcNotes editing or direct Cloud AI entry points. Cross-product desktop tool requests requiring the ArcChat bridge report that dependency. |
| FR-05 | Startup meets the budget in [`../12-quality-and-compatibility-contract.md`](../12-quality-and-compatibility-contract.md) §5, with no cloud dependency in the startup path. |

---

## 17. Non-goals

ArcNotes is **not**: a Notion clone or an application builder; a spreadsheet; a project-management suite; an image editor; a collaborative editor; a Markdown folder mirror; or a second agent platform.

**A knowledge graph, if offered, is a derived view of the link graph** — never a separate authoritative store ([IX-06](../06-knowledge-search-and-retrieval.md#rule-ix-06)).

**A web clipper**, if offered later, is an import path producing ordinary ArcNotes documents, not a live external mirror.

**Checklist items may relate to agent tasks later, explicitly** ([BL-05](#rule-bl-05)); they never become tasks implicitly.

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

The domain contains only the accepted notebook and property-view concepts. No canvas, presentation, flashcard or collaboration domain reservations are required.

---

## 19. V1 scope

| Area | V1 |
|---|---|
| **Content** | Notebook, folder, document, block editor, rich text, lists and checklists, code, table, math, image/file/PDF |
| **Organisation** | Tags, properties, favorites, recent, internal links, backlinks, outline |
| **Retrieval** | Full-text search, metadata filters, basic saved views |
| **Reliability** | Autosave, undo/redo, history, checkpoint, trash, crash recovery |
| **Portability** | Markdown/text and folder/vault import; Cloud Markdown/attachment/metadata export |
| **AI** | Selection AI actions, Ask ArcChat, ArcChat context and capabilities, agent provenance and checkpoints |
| **Cloud** | Explicit notebook sync, managed attachment sync, cloud status, version and recovery integration |

Advanced importers and excluded workbenches are outside the current delivery baseline.

---

## 20. Reference relationship

**AFFiNE and SiYuan are ArcNotes references** (**[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**) — sources of features, behaviour, tests and migration evidence, **never architecture authorities or parity commitments**.

| # | Requirement |
|---|---|
| RF-01 | Maintain an ArcNotes Reference Coverage Matrix for AFFiNE and SiYuan, mapping accepted notebook behaviour to target data/UI/contracts and acceptance evidence. Classify excluded whiteboard, presentation, collaboration, flashcard and advanced database behaviour as Drop or Reference Only; no implementation gate remains for them. |
| RF-02 | **Reuse is licence-gated and provenance-gated** (**[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**). File-level SPDX evidence against the local repository baseline is required before any copy, translation or port — the **[F-013](../../assurance/open-gates-register.md#rule-f-013)** gate. AGPL-identified material is behavioural reference only, implemented independently. |
| RF-03 | Reference material informs feature depth; **the target runtime architecture is ArcForges' own** — C#, Avalonia, Native AOT, the ArcForges domain and persistence model. |

---

## 21. Acceptance scenarios

**Notebook core** — sign into a workspace, create a notebook/folder/document, edit rich blocks, save and acknowledge Cloud; reopen on another device; links, ordering, tags and metadata agree.

**Native resilience** — hydrate a notebook, disconnect, edit and search it; restart after a durable local save; pending edits survive and remain visibly unsynchronised. Reconnect against a changed base revision: both versions survive as an explicit conflict. Never call pending edits Cloud-saved.

**Block identity and references** — move/rename/edit without breaking document or block links; backlinks are derived; deleted or unavailable targets have explicit states.

**Properties/views** — list and table views share the same source documents; typed filtering/sorting agrees between Cloud and hydrated cache; rename a property without losing values; reject a lossy type change without confirmation; deleting a view leaves documents intact.

**Attachments** — managed uploads preserve bytes and references, large/external files require a clear choice, hydration loss is recoverable, and an unavailable attachment does not masquerade as downloaded.

**AI** — selection AI works through Cloud without ArcChat Desktop; no service term means no AI even with credits; no BYOK/model download UI exists; context is minimal; bulk edits require review and checkpoints.

**History/trash** — restore creates a new revision; trash restore preserves identity; deleting tags/views deletes no notes; deleting a folder has an explicit descendant scope.

**Portability** — §13.3 passes, including expired-subscription export of retained data and explicit handling of device-only pending edits.

**Scope enforcement** — no whiteboard, frames/slides, presentation navigation, spaced repetition, DOCX importer, formula/relation/rollup engine, E2EE or collaboration-only schema/acceptance obligation remains.

---

## 22. Traceability

| Current document | Relationship |
|---|---|
| [Editing, Rich Content and Preview](../../architecture/18-editing-and-rich-content.md) | Defines the native document editor and attachment presentation |
| [Desktop Local Data Model](../../architecture/data-model/02-desktop-data-model.md) | Defines the native working store and note structures |
| [Reference Coverage Matrix — ArcNotes / AFFiNE + SiYuan](../../assurance/reference-coverage/arcnotes-affine-siyuan.md) | Records accepted and excluded reference-source capabilities under the current scope |
| **[D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002)**, **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** | Four-product portfolio; excluded canvas/presentation features do not re-enter through references |
| **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006) as amended by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** | Notebook core, bounded property views, Cloud continuity and explicit exclusions |
| **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**, **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)** | AFFiNE and SiYuan as licence-gated references with a required coverage matrix |
