# Editing, Rich Content and Preview

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (Desktop is a Native AOT deliverable), **[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)** (Avalonia AOT evidence), `§5`–`§6` and `§9` of the ArcNotes requirements
> Companions: [`data-model/02-desktop-data-model.md`](data-model/02-desktop-data-model.md) `§3`, [`12-native-interop-and-media.md`](12-native-interop-and-media.md), [`06-data-persistence-and-formats.md`](06-data-persistence-and-formats.md)

The requirements state that ArcNotes is *"a rich block editor with Markdown-friendly interaction"* with inline content *"modelled explicitly, not as embedded markup strings"* ([BL-07](../requirements/products/arcnotes.md#rule-bl-07)) and PDF as *"a first-class attachment with in-product viewing"* ([AT-05](../requirements/products/arcnotes.md#rule-at-05)). **No architecture stated how.** This document supplies it, and states plainly which capabilities carry a real dependency cost.

An editor is where a document product is won or lost. A wrong content model, a caret that misbehaves in an IME, or an undo stack that loses an agent's edit are not cosmetic defects — they are the product failing at its core act.

> **Citation convention.** Rule identifiers are document-scoped ([OG-05](../assurance/open-gates-register.md#rule-og-05)). Within this document an unqualified `DC-`, `BL-`, `ED-`, `AT-`, `PR-` or `IX-` identifier is a **requirement of [`../requirements/products/arcnotes.md`](../requirements/products/arcnotes.md)**; every other cross-document citation names its source.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| EC-01 | **The document model is the authority; the view is a projection.** No visual state is the source of any content fact. |
| <a id="rule-ec-02"></a>EC-02 | **Inline content is a typed structure, never a markup string** ([BL-07](../requirements/products/arcnotes.md#rule-bl-07)). No path stores or round-trips content as Markdown, HTML or RTF. Those are import and export formats only (`§10`). |
| EC-03 | **Every content change is a transaction** (`§3`). There is no path that mutates a block outside one. |
| <a id="rule-ec-04"></a>EC-04 | **A `BlockId` is stable under every ordinary edit** ([BL-01](../requirements/products/arcnotes.md#rule-bl-01)) — typing, moving, indenting, splitting a sibling, converting a neighbour. |
| <a id="rule-ec-05"></a>EC-05 | **Rendering is virtualised** (`§6`). Opening a large document never realises every block. |
| <a id="rule-ec-06"></a>EC-06 | **User content never executes** ([CS-06](10-web-architecture.md#rule-cs-06) of the web architecture; [FA-07](06-data-persistence-and-formats.md#rule-fa-07) and [IE-06](06-data-persistence-and-formats.md#rule-ie-06) of the persistence architecture). Every preview path in `§8` is a decode-and-render path, never an evaluation path. |
| EC-07 | **A capability requiring a native dependency is declared as such** ([NP-01](12-native-interop-and-media.md#rule-np-01) of the native interop architecture), with the substitute analysis recorded. Calling something "preview" does not exempt it. |
| <a id="rule-ec-08"></a>EC-08 | **An agent edit and a human edit use the same transaction path** (`§3.4`). There is no privileged write. |

---

## 2. The content model

### 2.1 Block content

A `block` row stores `kind` plus a `content` structure typed by that kind (`§3` of the desktop data model). The kind set is exactly [BL-04](../requirements/products/arcnotes.md#rule-bl-04)'s V1 list — no more:

| `kind` | Content shape | Notes |
|---|---|---|
| `paragraph` | `InlineContent` | |
| `heading` | `InlineContent` + `level 1–6` | Feeds the outline ([ED-08](../requirements/products/arcnotes.md#rule-ed-08)) |
| `list` | `InlineContent` + `style ∈ {bulleted, numbered, checklist}` + `checked?` | One kind, three styles — `checked` is meaningful only for `checklist` |
| `quote` | `InlineContent` | |
| `callout` | `InlineContent` + `tone` | |
| `code` | plain text + `languageId?` + `wrap` | **Never `InlineContent`** — marks inside code are meaningless (`§7.1`) |
| `divider` | *(empty)* | |
| `table` | `TableContent` (`§7.4`) | A document table, not a database ([ED-07](../requirements/products/arcnotes.md#rule-ed-07)) |
| `math` | TeX source + `display ∈ {block}` | `§7.2` |
| `image` | `AttachmentRef` + `alt` + `layout` | References, never embeds ([AT-03](../requirements/products/arcnotes.md#rule-at-03), [AT-04](../requirements/products/arcnotes.md#rule-at-04)) |
| `attachment` | `AttachmentRef` + `presentation ∈ {chip, card, pdfViewer}` | **PDF is this kind with `pdfViewer`**, not a separate kind ([AT-05](../requirements/products/arcnotes.md#rule-at-05)) |
| `embed` | `ReferenceTarget` + `renderMode` | A reference to a document, block or saved view — never a copy ([I-224](../requirements/01-normative-glossary-and-invariants.md#rule-i-224)) |
| `toggle` | `InlineContent` + children | Collapsible; collapse state is device-local, not content |

| # | Rule |
|---|---|
| BK-01 | **The kind set is closed and statically registered** ([BL-08](../requirements/products/arcnotes.md#rule-bl-08)). Adding a kind is a schema-evolution event ([SE-01](data-model/00-data-model-overview.md#rule-se-01)–[SE-07](data-model/00-data-model-overview.md#rule-se-07) of the data-model overview), not a runtime registration. |
| BK-02 | **An unknown kind read from storage is preserved inert and shown as unsupported** ([FA-07](06-data-persistence-and-formats.md#rule-fa-07) of the persistence architecture), never dropped and never executed. This is what makes a forward-compatible read possible. |
| BK-03 | **No kind is `html` or `script`** ([BL-06](../requirements/products/arcnotes.md#rule-bl-06)). Extensibility goes through the extension platform, out of process. |
| BK-04 | **Children are structural, not content.** A block's children are `block` rows with `parent_block_id`, so hierarchy survives independently of any kind's content shape ([BL-02](../requirements/products/arcnotes.md#rule-bl-02)). |

### 2.2 Inline content

```
InlineContent := ordered list of Inline
Inline        := TextRun { text, marks }
               | Link      { target, marks, InlineContent }
               | Mention   { subject, marks }
               | InlineMath{ tex }
               | FootnoteRef { footnoteId }
               | LineBreak
Mark          := bold | italic | strikethrough | underline | code
               | highlight(colorToken) | textColor(colorToken) | superscript | subscript
```

| # | Rule |
|---|---|
| IN-01 | **Marks are a closed enumeration**, versioned with the schema. An unknown mark is preserved and ignored for rendering, never dropped. |
| IN-02 | **Text is stored NFC-normalised UTF-8.** Normalisation happens at the transaction boundary, once, so comparison, search and diff never face two encodings of one string. |
| IN-03 | **Offsets are UTF-16 code-unit indices into a run's `text`**, matching the .NET string the editor manipulates. Converting to and from grapheme positions is the caret's job (`§4.2`), not the model's. |
| IN-04 | **Adjacent runs with identical mark sets are merged at the transaction boundary.** Without this, a long editing session fragments a paragraph into thousands of runs and every subsequent operation slows down. |
| IN-05 | **A `Link` carries `InlineContent`, so a link can contain formatted text**, but a link never nests inside a link. |
| IN-06 | **A `Mention` and a `Link` to a document both store identity, never a title** ([BR-04](../planning/work-packages/18-arcnotes-document-core.md#rule-br-04) of [WP-18](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18)). The title is resolved at render time, so renaming a document updates every reference without a write. |
| <a id="rule-in-07"></a>IN-07 | **`InlineMath` stores TeX source as the authority**; its rendered form is derived and cached (`§7.2`). |
| IN-08 | **An empty run is never persisted.** Empty `InlineContent` is an empty list, which is how an empty paragraph is represented — not a run containing `""`. |

### 2.3 What the model deliberately excludes

| Excluded | Why |
|---|---|
| A markup string anywhere in the model | [EC-02](#rule-ec-02); a markup string makes `BlockId` stability and structured operations impossible |
| Arbitrary attributes on a block or run | An open bag defeats validation, migration and the closed value model ([L2-02](15-extension-platform-architecture.md#rule-l2-02) of the extension architecture) |
| Per-block revisions | The document is the aggregate; the document's revision governs ([RV-03](data-model/00-data-model-overview.md#rule-rv-03) of the data-model overview) |
| Presentation state in content | Collapse, scroll and viewport are device-local; they are view state, never a synchronised revision ([SL-03](#rule-sl-03)) |
| Backlinks in content | The index is derived; writing them into content would make a read into a write ([WP-18.02](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.02)) |

---

## 3. Editing transactions

### 3.1 Shape

```
gesture / command / agent operation
   ↓
build EditTransaction { ops[], selectionBefore, selectionAfter, origin, label }
   ↓ validate against the model     (structural legality, not taste)
   ↓ apply atomically in memory
   ↓ push the inverse onto the undo stack
   ↓ mark the document dirty; the commit unit persists it (§6 of the persistence architecture)
   ↓ raise a change notification carrying the op list, not "reload"
```

The operation set is closed:

| Operation | Meaning |
|---|---|
| `InsertBlock(parent, ordinal, kind, content)` | |
| `RemoveBlock(blockId)` | With its subtree |
| `MoveBlock(blockId, newParent, newOrdinal)` | **Preserves `BlockId`** ([EC-04](#rule-ec-04)) |
| `SetBlockKind(blockId, kind, contentMapping)` | Conversion, with a declared content mapping (`§3.3`) |
| `SplitBlock(blockId, offset)` | The original keeps its id; the tail is new |
| `MergeBlocks(firstId, secondId)` | The first keeps its id; the second is removed |
| `ReplaceInlineRange(blockId, range, InlineContent)` | The single text-editing primitive |
| `ApplyMark(blockId, range, mark, on)` | |
| `SetBlockAttribute(blockId, key, value)` | Only kind-declared attributes: heading level, list style, checked, language, tone |
| `SetProperty(documentId, propertyDefId, value)` | Document properties, not block content |

| # | Rule |
|---|---|
| TX-01 | **A transaction is atomic**: every operation applies, or none does. A validation failure at operation four leaves the document exactly as it was. |
| TX-02 | **A transaction is the undo granularity** (`§3.2`). One gesture that produces four operations undoes as one. |
| TX-03 | **Every operation is invertible by construction.** The inverse is computed at apply time, when the prior state is known, and stored with the transaction. Undo never re-derives the old state by diffing. |
| TX-04 | **Ordinals are fractional** (`§3` of the desktop data model). `InsertBlock` and `MoveBlock` compute a key between neighbours and touch no sibling. A rebalance is an ordinary transaction, and it is the only operation that rewrites sibling ordinals. |
| <a id="rule-tx-05"></a>TX-05 | **A transaction records its origin**: `user`, `agent`, `import`, `sync`, `migration`, `automation`. Origin drives labelling, undo grouping and audit, and it is never inferred later. |
| TX-06 | **Structural validity is checked, taste is not.** An empty document, an empty heading and a table with one cell are all legal. Illegal is a cycle in the block tree, a duplicate ordinal, a child of a kind that declares no children, or a mark on `code` content. |

### 3.2 Undo and redo

| # | Rule |
|---|---|
| UN-01 | **The undo stack is per document and per session.** It is not persisted, is not synced, and is not a version history — the document's own history (`§12` of the ArcNotes requirements) is the durable mechanism, and the two are never conflated. |
| UN-02 | **Typing coalesces into one undo entry** while the origin, block and adjacency hold, and breaks on a caret jump, a different block, a non-typing operation, a save point or an idle interval. This is why the undo entry carries `selectionBefore`. |
| UN-03 | **Undo restores selection as well as content.** An undo that leaves the caret elsewhere is experienced as data loss even when nothing was lost. |
| UN-04 | **An agent transaction is undoable like any other**, and is labelled with its origin so the entry reads as the agent's action rather than the user's ([TX-05](#rule-tx-05)). |
| UN-05 | **A remote change arriving mid-session is not an undo entry.** It applies outside the stack, and it rebases pending undo entries whose target blocks it touched; an entry whose target no longer exists is dropped rather than silently retargeted. |
| UN-06 | **Redo is cleared by a new transaction**, with one exception: a remote change alone does not clear it. |

### 3.3 Kind conversion

Conversion is where content is quietly lost in most editors, so the mapping is declared rather than incidental.

| From → To | Mapping |
|---|---|
| Text-bearing → text-bearing | `InlineContent` carries over unchanged; kind attributes reset to defaults |
| Text-bearing → `code` | Marks are **dropped**; text is flattened; inline math becomes its TeX source; **the user is told what was dropped** |
| `code` → text-bearing | Text becomes one unmarked run; the language attribute is discarded |
| Any → `divider` | **Refused** if content is non-empty; the user must delete deliberately |
| Text-bearing → `table` | The block becomes the first cell; **children are refused**, not silently reparented |
| `toggle` → non-toggle | Children are **promoted to siblings**, never deleted |

| # | Rule |
|---|---|
| CV-01 | **Every conversion declares its mapping**, and a mapping that loses content states what is lost before it is applied. |
| CV-02 | **A refused conversion is refused with a reason**, never silently performed differently from what was asked. |
| CV-03 | **Conversion preserves `BlockId`** ([EC-04](#rule-ec-04)), so links and citations into that block survive. |

### 3.4 The agent editing path

The agent reaches this layer through `INotesOperations` (`§4` of the local RPC contract), and its writes carry `ExpectedRev` ([NO-02](contracts/02-local-rpc-operations.md#rule-no-02) there).

| # | Rule |
|---|---|
| AE-01 | **An agent operation becomes an `EditTransaction`** with `origin = agent`. There is no second write path ([EC-08](#rule-ec-08)). |
| AE-02 | **A stale `ExpectedRev` fails with `conflict.revision_mismatch`** and is surfaced to the model as correctable ([SI-04](17-agent-harness.md#rule-si-04) of the harness). |
| AE-03 | **An agent edit to an open document appears live**, and does not require the user to reload. This follows from the change notification carrying the op list. |
| AE-04 | **An agent edit is visibly attributed** in the interface and in history. A user must be able to see what the agent changed, not only that something changed. |
| AE-05 | **A multi-block agent edit is one transaction**, so undo reverses the whole intent rather than fragments of it. |

---

## 4. Selection, caret and text input

### 4.1 Selection model

Two modes, permanently distinct:

| Mode | Anchor | Operations |
|---|---|---|
| **Text selection** | `(blockId, offset)` → `(blockId, offset)`, possibly spanning blocks | Type, delete, apply mark, split, merge, replace |
| **Block selection** | An ordered set of `BlockId` | Move, indent/outdent, convert, duplicate, delete, copy-as ([ED-05](../requirements/products/arcnotes.md#rule-ed-05)) |

| # | Rule |
|---|---|
| SL-01 | **Block selection is first-class, not a degenerate text selection** ([ED-05](../requirements/products/arcnotes.md#rule-ed-05)). Every block operation is available across a multi-block selection. |
| SL-02 | **A cross-block text selection has a defined normal form**: the partial head and tail blocks plus the fully covered middle. Every operation states its behaviour on all three parts. |
| <a id="rule-sl-03"></a>SL-03 | **Selection is view state, not content**, and is never persisted into the document or synced. |
| SL-04 | **Selection survives a remote change where it can**, by anchoring to `(blockId, offset)` and re-resolving; where the block is gone it collapses to the nearest surviving position rather than jumping to the document start. |

### 4.2 Caret and grapheme correctness

| # | Rule |
|---|---|
| CT-01 | **The caret rests only on grapheme-cluster boundaries.** Arrow keys, backspace and delete move by grapheme, not by code unit or code point — otherwise an emoji with a skin-tone modifier or a Devanagari cluster breaks apart. |
| CT-02 | **Word movement uses Unicode word-boundary rules**, not whitespace splitting. |
| CT-03 | **Bidirectional text is supported for display and caret movement.** Logical order is the storage order; visual order is a layout concern. Caret movement is **visual** for arrow keys and **logical** for home/end, which is what users of mixed-direction text expect. |
| CT-04 | **Vertical movement preserves a desired column** across lines of differing length, and the desired column resets on any horizontal movement. |
| CT-05 | **Selection painting handles bidi runs**, so a selection across a direction boundary paints as the discontiguous ranges it really is. |

### 4.3 IME and composition

| # | Rule |
|---|---|
| IM-01 | **A composition in progress is not a transaction.** Preedit text is view state; only the committed string enters the model. This is what keeps CJK, Korean and dictation input from producing hundreds of undo entries and hundreds of journal writes. |
| IM-02 | **The composition window is positioned from the caret's real screen rectangle**, recomputed on layout change. |
| IM-03 | **A commit produces exactly one `ReplaceInlineRange`**, and one undo entry. |
| IM-04 | **Cancelling a composition leaves the model untouched**, because it was never touched. |
| IM-05 | **A remote or agent edit arriving during a composition does not interrupt it.** The change applies to other blocks; a change to the composing block is deferred until commit, then rebased — interrupting a composition loses the user's in-flight word. |
| IM-06 | **Dictation and handwriting input use the same commit path**, so their behaviour is defined rather than emergent. |

### 4.4 Markdown-friendly input

| # | Rule |
|---|---|
| MK-01 | **Markdown syntax is input, never storage** ([ED-01](../requirements/products/arcnotes.md#rule-ed-01)). Typing `## ` at the start of an empty paragraph converts the block to a heading and consumes the trigger. |
| MK-02 | **Every input rule is undoable in one step back to the literal text typed**, so a user who wanted a literal `# ` gets it by pressing undo once. |
| MK-03 | **Input rules are a closed, statically registered set**, not a user-extensible grammar. |
| <a id="rule-mk-04"></a>MK-04 | **Paste of Markdown text is a conversion with a choice** — as rich content or as literal text — and never silently reinterprets what the user pasted (`§10`). |
| <a id="rule-mk-05"></a>MK-05 | **The slash menu inserts and transforms content; the command palette runs product commands** ([ED-03](../requirements/products/arcnotes.md#rule-ed-03)). They share no registry, so a command can never appear as a block type. |

---

## 5. Rendering architecture

### 5.1 The stack

| Layer | Provided by |
|---|---|
| Window, input, compositor | Avalonia (**[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)**) |
| Text shaping and glyph rasterisation | Avalonia's text stack over its platform backends |
| Block layout | **ArcForges** — the block layout engine in `§5.2` |
| Block presentation | ArcForges controls, statically templated ([AC-04](00-architecture-overview.md#rule-ac-04)) |

| # | Rule |
|---|---|
| RN-01 | **No reflection-based templating, no runtime XAML loading, no dynamic control construction from a string** ([AC-04](00-architecture-overview.md#rule-ac-04) of the architecture overview, **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**). Block presenters are resolved through a statically registered kind-to-presenter map. |
| <a id="rule-rn-02"></a>RN-02 | **ArcForges does not implement text shaping.** Shaping, font fallback and glyph rasterisation belong to the platform stack; reimplementing them is out of scope and would be a multi-year commitment (`§9`). |
| RN-03 | **A custom-drawn control is used where a composed control cannot meet the measured budget**, and that choice is recorded with its measurement — never taken by default. |
| RN-04 | **No WebView, no Chromium, no browser engine, no DOM, no JavaScript engine, no HTML-as-UI and no loopback UI server** (**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**, `§8` of the product scope). This is a technology-constitution prohibition, not a preference, and a repository policy test asserts that no desktop project references a web-view package ([WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05)). |
| RN-05 | **[I-028](../requirements/01-normative-glossary-and-invariants.md#rule-i-028) — a native editor with a working cache is not a WebView shell.** The prohibition exists because a browser-hosted editor would make the AOT constraint, the input model and the accessibility model all unenforceable. |

### 5.2 Block layout and virtualisation

```
document → block sequence (in ordinal order, hierarchy flattened with depth)
   ↓ estimate heights for unmeasured blocks (per-kind heuristic)
   ↓ realise only the viewport window plus a bounded overscan
   ↓ measure realised blocks; replace estimates; correct scroll offset
   ↓ cache measurement by (blockId, contentFingerprint, availableWidth, fontScale, locale)
```

| # | Rule |
|---|---|
| LY-01 | **Virtualisation is mandatory** ([EC-05](#rule-ec-05)). A ten-thousand-block document realises a viewport's worth of presenters, not ten thousand. |
| LY-02 | **Measurement is cached and invalidated by fingerprint**, so scrolling back does not re-measure. |
| LY-03 | **Height estimation error is corrected without visible jump.** A scroll anchor is held on a stable block, and corrections apply around it — an estimate that shifts content under the user's cursor is a defect. |
| LY-04 | **Scroll position anchors to `(blockId, offsetWithinBlock)`**, never to a pixel offset, so a remote edit above the viewport does not move the reader. |
| LY-05 | **Deeply nested and very large single blocks are bounded**: nesting depth has a compiled maximum, and an oversized single block is itself internally virtualised or truncated with an explicit expand affordance. |
| LY-06 | **Find-in-document searches the model, not realised views** — otherwise a match outside the viewport would be invisible to a feature that exists to find it. |

### 5.3 Performance obligations

| Obligation | Target |
|---|---|
| Keystroke to caret movement | Within the input latency budget of `§12` of the quality contract, measured at the 95th percentile on the reference machine |
| Opening a large document | First screen interactive without full measurement |
| Applying a mark across a large selection | One transaction, one layout pass |
| Scrolling a large document | No re-measure of previously measured blocks |

| # | Rule |
|---|---|
| PF-01 | **Editing performance is measured on a defined large-document corpus**, committed as a fixture, and regressions fail the gate ([WP-18.06](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.06)). |
| PF-02 | **A performance target without a measurement is not a target**, and none is claimed here that [WP-18](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18) does not measure. |

---

## 6. Persistence coupling

| # | Rule |
|---|---|
| PC-01 | **A transaction does not equal a write.** Transactions coalesce into the canonical commit unit (`§2` of the persistence architecture), so typing does not produce one disk write per keystroke. |
| PC-02 | **The journal makes an uncommitted edit recoverable** (`§3` there). A crash mid-paragraph loses at most the coalescing window, and what survives is a valid document, never a half-applied transaction. |
| PC-03 | **The document's revision advances per commit unit, not per transaction**, which is what keeps sync change volume proportional to work rather than to keystrokes. |
| PC-04 | **A large paste is one transaction and one commit**, not a stream of thousands. |
| PC-05 | **Derived stores are updated after commit, never inside the transaction** ([DS-06](data-model/03-derived-stores.md#rule-ds-06) of the derived-store architecture): the search index, the link index, and the outline. |

---

## 7. Rich content kinds

### 7.1 Code

| # | Rule |
|---|---|
| CD-01 | **Code content is plain text with a language identifier.** No marks, no inline structure — a mark inside code is meaningless and would corrupt copy-out fidelity. |
| CD-02 | **Syntax highlighting is a derived presentation overlay**, computed from the text and never stored in content. |
| CD-03 | **The grammar set is bounded and statically registered.** No grammar is downloaded, compiled at runtime, or loaded from user content — that path is code execution wearing a highlighting costume ([EC-06](#rule-ec-06)). |
| CD-04 | **Highlighting is incremental and cancellable**, computed off the UI thread, and a slow or failed highlight degrades to unhighlighted text rather than blocking input. |
| CD-05 | **An unknown language renders as plain text with the identifier preserved**, so a later release can highlight it without a migration. |
| CD-06 | **Copy from a code block yields the exact source text**, with no smart quotes, no reflow and no injected indentation. |

### 7.2 Math

| # | Rule |
|---|---|
| MT-01 | **TeX source is the authority** ([IN-07](#rule-in-07)); the rendered form is derived and cached by `(source, fontScale, theme)`. |
| MT-02 | **The supported subset is declared and versioned.** A construct outside it renders as its source with an explicit "unsupported construct" marker, never silently wrong — a silently mis-rendered formula is worse than an unrendered one. |
| MT-03 | **Math layout is a managed component**, chosen against the AOT and licence constraints; it introduces no native dependency. |
| MT-04 | **No TeX macro expansion from document content is executed as a general macro language** ([EC-06](#rule-ec-06)). The supported subset is fixed. |
| MT-05 | **Math participates in inline layout with a real baseline**, so inline math sits on the text baseline rather than floating. |
| MT-06 | **Math is copyable as its TeX source**, and exports as source in Markdown and as source plus rendering in HTML (`§10`). |

### 7.3 Images

| # | Rule |
|---|---|
| IG-01 | **An image block references a managed attachment or an external reference** ([AT-03](../requirements/products/arcnotes.md#rule-at-03), [AT-04](../requirements/products/arcnotes.md#rule-at-04)). No image bytes are ever in content. |
| IG-02 | **Decode is off the UI thread, bounded, and downsampled to display size.** A 100-megapixel image is decoded to what the viewport needs, never in full into UI memory. |
| IG-03 | **EXIF orientation is applied; embedded colour profiles are honoured or explicitly ignored with a stated policy.** An image that displays rotated is a correctness defect, not a nicety. |
| IG-04 | **A malformed image fails to a placeholder with a reason** and never crashes the process or the layout pass. |
| IG-05 | **Animated formats play only on explicit user action** and respect the platform's reduced-motion setting. |
| IG-06 | **Decoded images live in a bounded cache** with eviction ([EV-01](data-model/03-derived-stores.md#rule-ev-01)–[EV-05](data-model/03-derived-stores.md#rule-ev-05) of the derived-store architecture), keyed by attachment content hash and target size. |
| <a id="rule-ig-07"></a>IG-07 | **Image editing is not part of ArcNotes** (`§17` of its requirements). Crop-on-insert and resize are layout attributes, not pixel edits. |

### 7.4 Tables

| # | Rule |
|---|---|
| <a id="rule-tb-01"></a>TB-01 | **A table is a document table, not a relational engine** ([ED-07](../requirements/products/arcnotes.md#rule-ed-07)). It has no formulas, no queries, no relations and no computed columns in V1. |
| TB-02 | **A cell holds `InlineContent`**, not arbitrary blocks, in V1. This keeps layout tractable and keeps the table from becoming a second document model. |
| TB-03 | **Row and column identity is stable**, so a column insert does not renumber and invalidate anything anchored to a column. |
| TB-04 | **Merged cells are modelled as spans on the owning cell**, with a validation rule that spans never overlap. |
| TB-05 | **A wide table scrolls within its own bounds** and never forces the document to scroll horizontally. |
| TB-06 | **Copy of a table region produces a table**, and paste of a tabular clipboard payload produces a table with the shape the source had. |

### 7.5 Embeds and references

| # | Rule |
|---|---|
| EM-01 | **An embed is a reference, never a copy** ([I-224](../requirements/01-normative-glossary-and-invariants.md#rule-i-224), [WP-18.02](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.02)). Editing the source updates every embed. |
| EM-02 | **An embed renders at a bounded depth.** A cycle is detected and the inner occurrence renders as a link with a stated reason, never as infinite recursion. |
| EM-03 | **An embed re-checks permission at render**, so an embed of content the reader may not see resolves to an unavailable placeholder rather than leaking it. |
| EM-04 | **A broken reference is an explicit state** (`state = broken` in `document_link`), never a silent blank. |

---

## 8. Preview and viewers

This is where "preview" most often conceals missing capability, so each surface states what it really does and what it costs.

### 8.1 The three honest levels

| Level | What it is | Where it is used |
|---|---|---|
| **Metadata card** | Name, kind, size, availability, provenance. No content decoded. | Any unavailable or unsupported content; ArcChat's artifact list at rest |
| **Thin preview** | A bounded rendering sufficient to recognise and decide — first page, first frames, a thumbnail, an excerpt. **Read-only, no navigation into the content's own model.** | ArcChat artifacts ([AR-04](../requirements/products/arcchat.md#rule-ar-04), [PB-05](../requirements/products/arcchat.md#rule-pb-05) of the ArcChat requirements); ArcNotes attachment chips |
| **In-product viewer** | Real navigation and interaction inside the content: paging, zoom, text selection, annotation anchors. | ArcNotes PDF ([AT-05](../requirements/products/arcnotes.md#rule-at-05)); ArcSlate media preview |

| # | Rule |
|---|---|
| PV-01 | **Thin preview is a real boundary, not a fallback for unfinished work.** ArcChat previews and hands off ([PB-05](../requirements/products/arcchat.md#rule-pb-05) of the ArcChat requirements); it does not host the owning product's editing surface. |
| PV-02 | **A thin preview never claims to be authoritative** ([I-060](../requirements/01-normative-glossary-and-invariants.md#rule-i-060), [AR-04](../requirements/products/arcchat.md#rule-ar-04) of the ArcChat requirements). |
| PV-03 | **Where a level is not implemented, the surface degrades to the level below and says so** — a metadata card labelled as such is honest; a blank rectangle is not. |
| PV-04 | **A preview never executes content** ([EC-06](#rule-ec-06)) and never fetches a remote resource referenced by the content (`§7` of the security architecture). A document that phones home when previewed is an exfiltration channel. |
| PV-05 | **Preview generation is bounded in time, memory and output size**, runs off the UI thread, and a timeout degrades to the level below with a reason. |
| PV-06 | **Preview output is a derived store** ([DS-01](data-model/03-derived-stores.md#rule-ds-01)–[DS-07](data-model/03-derived-stores.md#rule-ds-07) of the derived-store architecture), cached by content hash and evictable. |

### 8.2 PDF — and the dependency it really carries

[AT-05](../requirements/products/arcnotes.md#rule-at-05) requires *in-product viewing, page-anchored annotation targets and citation anchors*. That is an in-product viewer, not a thin preview, and it cannot be met by metadata.

| # | Rule |
|---|---|
| PD-01 | **PDF rendering and text extraction are a declared dependency of ArcNotes**, with an owner, a substitute analysis and a licence position recorded under [NP-01](12-native-interop-and-media.md#rule-np-01) before adoption. |
| PD-02 | **The permitted native surface for ArcNotes is extended to document rendering and text extraction** (`§2` of the native interop architecture, amended), and to nothing else. The note, block, link and search models remain fully managed. |
| PD-03 | **The renderer is isolated behind a managed wrapper with the full C ABI discipline** ([AB-01](12-native-interop-and-media.md#rule-ab-01)–[AB-12](12-native-interop-and-media.md#rule-ab-12)), because a PDF renderer parses hostile input by definition. |
| PD-04 | **A malformed or hostile PDF degrades to a metadata card** and never affects process stability or the document that references it. |
| PD-05 | **Extracted text is derived data** ([AT-06](../requirements/products/arcnotes.md#rule-at-06), [IP-09](../requirements/06-knowledge-search-and-retrieval.md#rule-ip-09) of the ArcNotes requirements), rebuildable and never canonical. |
| PD-06 | **A page anchor is `(attachmentContentHash, pageIndex, rectOrTextRange)`**, so an annotation anchor survives re-open and is invalidated honestly if the attachment content changes. |
| PD-07 | **If the dependency is not adopted, [AT-05](../requirements/products/arcnotes.md#rule-at-05) is not met**, and that is stated as an open gate rather than absorbed by relabelling the viewer a preview. This is recorded as [PG-12](../assurance/open-gates-register.md#rule-pg-12) in the [open-gates register](../assurance/open-gates-register.md). |

### 8.3 Office documents — excluded from delivery

| # | Rule |
|---|---|
| OF-01 | **DOCX import is excluded by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**, not merely deferred. An Office attachment is presented as a metadata card with an open-in-system-application action. |
| OF-02 | **The architecture accommodates it**: import maps to blocks through the same `EditTransaction` path, and unsupported constructs are preserved inert and marked ([IE-06](06-data-persistence-and-formats.md#rule-ie-06) of the persistence architecture). |
| <a id="rule-of-03"></a>OF-03 | **No Office rendering engine is embedded**, and no Office application is automated. |
| OF-04 | **Required import is Markdown and plain text** (**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**); required export is a Cloud data export. A full-fidelity local package ecosystem is not a delivery obligation. |
| OF-05 | **The block model does not carry a DOCX-shaped construct** so that a future import would be additive. Adding DOCX later is a scope decision with its own design, not a hook waiting to be switched on. |

### 8.4 Audio and video in a document

| # | Rule |
|---|---|
| AV-01 | **ArcNotes and ArcChat present media as thin preview** — a poster frame or waveform thumbnail plus duration — and hand off to the owning application for real work ([PB-05](../requirements/products/arcchat.md#rule-pb-05)). |
| AV-02 | **The media runtime belongs to ArcSlate** (`§4` of the desktop architecture). ArcNotes does not acquire a decode pipeline to show a thumbnail; it requests a thumbnail through the artifact handler contract. |
| AV-03 | **Where no owning application is installed, the surface degrades to a metadata card with a stated reason** ([AR-07](../requirements/products/arcchat.md#rule-ar-07) of the ArcChat requirements). |

### 8.5 Untrusted content boundaries

| # | Rule |
|---|---|
| UT-01 | **Every parser reached from user content is treated as an attack surface**: bounded input size, bounded recursion, bounded time, and failure to a placeholder. |
| UT-02 | Hostile complex-format and compressed-image parsing uses the mandatory [C# ContentSandbox](24-content-and-extension-isolation.md), independently of whether extensions are enabled. An unavailable enforced profile refuses that parsing operation; it never falls back to parsing in the main process. |
| UT-03 | **Content instructions are never instructions** ([I-262](../requirements/01-normative-glossary-and-invariants.md#rule-i-262), [I-263](../requirements/01-normative-glossary-and-invariants.md#rule-i-263)). Text extracted from a PDF or an image is data with untrusted provenance, marked as such before it can reach the agent ([WP-11.06](../planning/work-packages/11-security-foundation.md#rule-wp-11.06)). |
| UT-04 | **No preview path evaluates script, macro, formula or embedded program content** in any format ([EC-06](#rule-ec-06)). |

---

## 9. What ArcForges does not build

Naming these prevents a "rich editor" from silently becoming an unbounded commitment.

| Not built | Consequence |
|---|---|
| A text shaping or font engine | Platform stack, through Avalonia ([RN-02](#rule-rn-02)) |
| A browser engine, or any HTML rendering path for content | [BL-06](../requirements/products/arcnotes.md#rule-bl-06); extensibility is out-of-process |
| A real-time collaborative editing engine | Excluded by P2-006. Stable IDs and closed operations serve the required single-owner multi-device sync; no collaboration-only reservation, hook or framework is introduced |
| A spreadsheet engine | [TB-01](#rule-tb-01) |
| An image editor | [IG-07](#rule-ig-07) |
| A diagram authoring surface | No requirement establishes one; the V1 block set ([BL-04](../requirements/products/arcnotes.md#rule-bl-04)) contains none, and none is introduced here |
| An Office rendering engine | [OF-03](#rule-of-03) |

---

## 10. Import, export and the clipboard

| # | Rule |
|---|---|
| PT-01 | **Markdown and HTML are conversion formats at the boundary** ([EC-02](#rule-ec-02)), never storage. Import and export are `§13` of the ArcNotes requirements and `§8` of the persistence architecture. |
| PT-02 | **Paste is a conversion with a declared mapping and a choice** ([MK-04](#rule-mk-04)): rich content, plain text, or — where the source is another ArcNotes document — a reference rather than a copy ([ED-06](../requirements/products/arcnotes.md#rule-ed-06); [DD-01](../requirements/09-shared-desktop-experience.md#rule-dd-01)–[DD-03](../requirements/09-shared-desktop-experience.md#rule-dd-03) of the shared desktop requirements). |
| PT-03 | **Pasted HTML is sanitised to the closed inline and block model** before it enters a transaction. Anything unmapped is dropped explicitly and reported, never carried as an opaque attribute. |
| PT-04 | **Copy produces multiple clipboard flavours**: the native structured form, Markdown, plain text and HTML, so paste into another application behaves as the user expects. |
| PT-05 | **Round-trip fidelity is stated per format, not assumed.** A format that cannot express a construct says so at export (`§13` there). |
| PT-06 | **Pasted content that references an attachment imports the attachment or references it by the shared rule** ([AT-01](../requirements/products/arcnotes.md#rule-at-01), [AT-02](../requirements/products/arcnotes.md#rule-at-02)), and never silently copies a large file. |

---

## 11. Cross-product application

| Product | What this document governs |
|---|---|
| **ArcNotes** | All of it — this is its editing core |
| **ArcChat** | `§8` preview levels for artifacts; message content uses the same inline model for its rendered parts, and the same code and math rules |
| **ArcScope** | Report and annotation text uses the inline model and `§7` rendering; measurement content is its own model, not this one |
| **ArcSlate** | Title and text overlays are its own model constrained by its render pipeline, **not** this document's editor; `§8` governs its media preview surfaces |
| **Mobile and Web** | Read and light-edit surfaces reuse the model and rules, never the desktop presenters (`§3` of the mobile architecture, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**) |

| # | Rule |
|---|---|
| XP-01 | **The content model is shared; the presenters are not.** A shared model in the contract layer, product-specific rendering per platform. |
| XP-02 | **ArcSlate's text overlay is not this editor.** Conflating them would drag the block model into the render pipeline. |
| XP-03 | **A mobile or web editing surface implements a declared subset** and states what it cannot do, rather than silently discarding what it cannot represent. |

---

## 12. Verification

| # | Obligation | Where |
|---|---|---|
| VF-01 | `BlockId` is stable across typing, move, indent, split of a sibling, conversion and merge | [WP-18.00](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) |
| VF-02 | Every transaction is atomic, and a failure at any operation leaves the document unchanged | [WP-18.00](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) |
| VF-03 | Undo restores content and selection, and one gesture undoes as one entry | [WP-18.05](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.05) |
| VF-04 | A remote or agent change mid-session rebases the undo stack without retargeting an entry to the wrong block | [WP-18.05](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.05) |
| VF-05 | Caret movement, deletion and selection are grapheme-correct on an emoji, Devanagari, Thai and combining-mark corpus | [WP-18.01](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.01) |
| VF-06 | A CJK composition produces one undo entry and one transaction, and is not interrupted by a concurrent remote edit | [WP-18.01](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.01) |
| VF-07 | Bidirectional text has correct visual caret movement and discontiguous selection painting | [WP-18.01](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.01) |
| VF-08 | A ten-thousand-block document opens interactive and scrolls without re-measuring measured blocks | [WP-18.01](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.01) |
| VF-09 | Content never round-trips through a markup string on any internal path | Repository policy test |
| VF-10 | Every kind conversion applies its declared mapping, and a lossy conversion states its loss first | [WP-18.00](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) |
| VF-11 | An agent edit is one transaction, is attributed, and is undoable | [WP-20.02](../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20.02), [WP-18.07](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.07) |
| VF-12 | A malformed image, PDF and embed each degrade to a placeholder with a reason and no crash | [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04) |
| VF-13 | No preview path fetches a remote resource or evaluates embedded program content | [WP-11.05](../planning/work-packages/11-security-foundation.md#rule-wp-11.05), [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04) |
| VF-14 | Extracted PDF and image text carries untrusted provenance before it can reach the agent | [WP-11.06](../planning/work-packages/11-security-foundation.md#rule-wp-11.06) |
| VF-15 | Copy from a code block reproduces the source exactly; copy of a table region produces a table | [WP-18.00](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) |
| VF-16 | Paste of Markdown, HTML and an internal payload each follow the declared mapping with no silent loss | [WP-19.04](../planning/work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.04), [WP-18.00](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) |
| VF-17 | An unsupported math construct renders as source with an explicit marker, never silently wrong | [WP-18.01](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.01) |
| VF-18 | An unknown block kind and an unknown mark survive a read-modify-write cycle unchanged | [WP-18.00](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.00) |
