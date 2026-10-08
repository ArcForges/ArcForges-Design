# Rich Content and Preview

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (Desktop is a Native AOT deliverable), **[V-05a](../assurance/phase-1-official-verification.md#rule-v-05a)** (Avalonia AOT evidence)
> Companions: [`data-model/02-desktop-data-model.md`](data-model/02-desktop-data-model.md) `§3`, [`12-native-interop-and-media.md`](12-native-interop-and-media.md), [`06-data-persistence-and-formats.md`](06-data-persistence-and-formats.md)

ArcScope reports and annotations, and the embedded application assistant, render one shared vocabulary of rich content — code, math, images, tables and embedded references — built from a single inline content model. **No architecture stated how.** This document supplies it, and states plainly which preview capability carries a real dependency cost.

> **Citation convention.** Rule identifiers are document-scoped ([OG-05](../assurance/open-gates-register.md#rule-og-05)); every cross-document citation names its source.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| <a id="rule-ec-01"></a>EC-01 | **The content model is the authority; the view is a projection.** No visual state is the source of any content fact. |
| <a id="rule-ec-02"></a>EC-02 | **Inline content is a typed structure, never a markup string.** No path stores or round-trips content as Markdown, HTML or RTF. |
| <a id="rule-ec-06"></a>EC-06 | **User content never executes** ([CS-06](10-web-architecture.md#rule-cs-06) of the web architecture; [FA-07](06-data-persistence-and-formats.md#rule-fa-07) and [IE-06](06-data-persistence-and-formats.md#rule-ie-06) of the persistence architecture). Every preview path in `§8` is a decode-and-render path, never an evaluation path. |
| <a id="rule-ec-07"></a>EC-07 | **A capability requiring a native dependency is declared as such** ([NP-01](12-native-interop-and-media.md#rule-np-01) of the native interop architecture), with the substitute analysis recorded. Calling something "preview" does not exempt it. |

---

## 2. The content model

### 2.2 Inline content

```
InlineContent := ordered list of Inline
Inline        := TextRun { text, marks }
               | Link      { target, marks, InlineContent }
               | Mention   { subject, marks }
               | InlineMath{ tex }  // legacy preservation only; not V1 authoring
               | FootnoteRef { footnoteId }
               | LineBreak
Mark          := bold | italic | strikethrough | underline | code
               | highlight(colorToken) | textColor(colorToken) | superscript | subscript
```

| # | Rule |
|---|---|
| <a id="rule-in-01"></a>IN-01 | **Marks are a closed enumeration**, versioned with the schema. An unknown mark is preserved and ignored for rendering, never dropped. |
| <a id="rule-in-02"></a>IN-02 | **Text is stored NFC-normalised UTF-8.** Normalisation happens at the transaction boundary, once, so comparison, search and diff never face two encodings of one string. |
| <a id="rule-in-03"></a>IN-03 | **Offsets are UTF-16 code-unit indices into a run's `text`**, matching the .NET string the editor manipulates. Converting to and from grapheme positions belongs to the presenting surface, not the model. |
| <a id="rule-in-04"></a>IN-04 | **Adjacent runs with identical mark sets are merged at the transaction boundary.** Without this, a long editing session fragments a paragraph into thousands of runs and every subsequent operation slows down. |
| <a id="rule-in-05"></a>IN-05 | **A `Link` carries `InlineContent`, so a link can contain formatted text**, but a link never nests inside a link. |
| <a id="rule-in-06"></a>IN-06 | **A `Mention` and a `Link` both store identity, never a title.** The title is resolved at render time, so a rename updates every reference without a write. |
| <a id="rule-in-07"></a>IN-07 | **TeX source is the authority for math blocks**; their rendered form is derived and cached (`§7.2`). The legacy `InlineMath` shape preserves unsupported source and its identity, never enables V1 inline authoring or silently converts it to a block. |
| <a id="rule-in-08"></a>IN-08 | **An empty run is never persisted.** Empty `InlineContent` is an empty list, which is how an empty paragraph is represented — not a run containing `""`. |

### 2.3 What the model deliberately excludes

| Excluded | Why |
|---|---|
| A markup string anywhere in the model | [EC-02](#rule-ec-02); a markup string makes structured operations impossible |
| Arbitrary attributes on a block or run | An open bag defeats validation, migration and the closed value model ([L2-02](15-extension-platform-architecture.md#rule-l2-02) of the extension architecture) |
| Per-item revisions | The owning aggregate governs its own revision ([RV-03](data-model/00-data-model-overview.md#rule-rv-03) of the data-model overview) |
| Presentation state in content | Scroll and viewport are device-local view state, never a synchronised revision |

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
| <a id="rule-rn-01"></a>RN-01 | **No reflection-based templating, no runtime XAML loading, no dynamic control construction from a string** ([AC-04](00-architecture-overview.md#rule-ac-04) of the architecture overview, **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**). Block presenters are resolved through a statically registered kind-to-presenter map. |
| <a id="rule-rn-02"></a>RN-02 | **ArcForges does not implement text shaping.** Shaping, font fallback and glyph rasterisation belong to the platform stack; reimplementing them is out of scope and would be a multi-year commitment (`§9`). |
| <a id="rule-rn-03"></a>RN-03 | **A custom-drawn control is used where a composed control cannot meet the measured budget**, and that choice is recorded with its measurement — never taken by default. |
| <a id="rule-rn-04"></a>RN-04 | **No WebView, no Chromium, no browser engine, no DOM, no JavaScript engine, no HTML-as-UI and no loopback UI server** (**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**, `§8` of the product scope). This is a technology-constitution prohibition, not a preference, and a repository policy test asserts that no desktop project references a web-view package ([WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05)). |

## 7. Rich content kinds

### 7.1 Code

| # | Rule |
|---|---|
| <a id="rule-cd-01"></a>CD-01 | **Code content is plain text with a language identifier.** No marks, no inline structure — a mark inside code is meaningless and would corrupt copy-out fidelity. |
| <a id="rule-cd-02"></a>CD-02 | **Syntax highlighting is a derived presentation overlay**, computed from the text and never stored in content. |
| <a id="rule-cd-03"></a>CD-03 | **The grammar set is bounded and statically registered.** No grammar is downloaded, compiled at runtime, or loaded from user content — that path is code execution wearing a highlighting costume ([EC-06](#rule-ec-06)). |
| <a id="rule-cd-04"></a>CD-04 | **Highlighting is incremental and cancellable**, computed off the UI thread, and a slow or failed highlight degrades to unhighlighted text rather than blocking input. |
| <a id="rule-cd-05"></a>CD-05 | **An unknown language renders as plain text with the identifier preserved**, so a later release can highlight it without a migration. |
| <a id="rule-cd-06"></a>CD-06 | **Copy from a code block yields the exact source text**, with no smart quotes, no reflow and no injected indentation. |

### 7.2 Math

| # | Rule |
|---|---|
| <a id="rule-mt-01"></a>MT-01 | **TeX source is the authority** ([IN-07](#rule-in-07)); the rendered form is derived and cached by `(source, fontScale, theme)`. |
| <a id="rule-mt-02"></a>MT-02 | **The supported subset is declared and versioned.** A construct outside it renders as its source with an explicit "unsupported construct" marker, never silently wrong — a silently mis-rendered formula is worse than an unrendered one. |
| <a id="rule-mt-03"></a>MT-03 | **Math layout is a managed component**, chosen against the AOT and licence constraints; it introduces no native dependency. |
| <a id="rule-mt-04"></a>MT-04 | **No TeX macro expansion from document content is executed as a general macro language** ([EC-06](#rule-ec-06)). The supported subset is fixed. |
| <a id="rule-mt-05"></a>MT-05 | V1 math is a block construct. Use bounded block measurement, baseline metrics inside the math box, accessibility source text and reflow; no V1 inline-math authoring is supported. Existing inline payloads remain source-preserving unsupported content, with their wire field numbers unchanged. |
| <a id="rule-mt-06"></a>MT-06 | **Math is copyable as its TeX source.** |

### 7.3 Images

| # | Rule |
|---|---|
| <a id="rule-ig-01"></a>IG-01 | **An image block references a managed attachment or an external reference.** No image bytes are ever in content. |
| <a id="rule-ig-02"></a>IG-02 | **Decode is off the UI thread, bounded, and downsampled to display size.** A 100-megapixel image is decoded to what the viewport needs, never in full into UI memory. |
| <a id="rule-ig-03"></a>IG-03 | **EXIF orientation is applied; embedded colour profiles are honoured or explicitly ignored with a stated policy.** An image that displays rotated is a correctness defect, not a nicety. |
| <a id="rule-ig-04"></a>IG-04 | **A malformed image fails to a placeholder with a reason** and never crashes the process or the layout pass. |
| <a id="rule-ig-05"></a>IG-05 | **Animated formats play only on explicit user action** and respect the platform's reduced-motion setting. |
| <a id="rule-ig-06"></a>IG-06 | **Decoded images live in a bounded cache** with eviction ([EV-01](data-model/03-derived-stores.md#rule-ev-01)–[EV-05](data-model/03-derived-stores.md#rule-ev-05) of the derived-store architecture), keyed by attachment content hash and target size. |
| <a id="rule-ig-07"></a>IG-07 | **Image editing is not provided.** Crop-on-insert and resize are layout attributes, not pixel edits. |

### 7.4 Tables

| # | Rule |
|---|---|
| <a id="rule-tb-01"></a>TB-01 | **A table is a content table, not a relational engine.** It has no formulas, no queries, no relations and no computed columns in V1. |
| <a id="rule-tb-02"></a>TB-02 | **A cell holds `InlineContent`**, not arbitrary blocks, in V1. This keeps layout tractable and keeps the table from becoming a second document model. |
| <a id="rule-tb-03"></a>TB-03 | **Row and column identity is stable**, so a column insert does not renumber and invalidate anything anchored to a column. |
| <a id="rule-tb-04"></a>TB-04 | **Merged cells are modelled as spans on the owning cell**, with a validation rule that spans never overlap. |
| <a id="rule-tb-05"></a>TB-05 | **A wide table scrolls within its own bounds** and never forces the document to scroll horizontally. |
| <a id="rule-tb-06"></a>TB-06 | **Copy of a table region produces a table**, and paste of a tabular clipboard payload produces a table with the shape the source had. |

### 7.5 Embeds and references

| # | Rule |
|---|---|
| <a id="rule-em-01"></a>EM-01 | **An embed is a reference, never a copy** ([I-224](../requirements/01-normative-glossary-and-invariants.md#rule-i-224)). Editing the source updates every embed. |
| <a id="rule-em-02"></a>EM-02 | **An embed renders at a bounded depth.** A cycle is detected and the inner occurrence renders as a link with a stated reason, never as infinite recursion. |
| <a id="rule-em-03"></a>EM-03 | **An embed re-checks permission at render**, so an embed of content the reader may not see resolves to an unavailable placeholder rather than leaking it. |
| <a id="rule-em-04"></a>EM-04 | **A broken reference is an explicit state** (`state = broken` on the reference), never a silent blank. |

---

## 8. Preview and viewers

This is where "preview" most often conceals missing capability, so each surface states what it really does and what it costs.

### 8.1 The three honest levels

| Level | What it is | Where it is used |
|---|---|---|
| **Metadata card** | Name, kind, size, availability, provenance. No content decoded. | Any unavailable or unsupported content; ArcChat's artifact list at rest |
| **Thin preview** | A bounded rendering sufficient to recognise and decide — first frames, a thumbnail, a still image, an excerpt. **Read-only, no navigation into the content's own model.** | ArcChat artifacts ([AR-04](../requirements/products/arcchat.md#rule-ar-04), [PB-05](../requirements/products/arcchat.md#rule-pb-05) of the ArcChat requirements); image attachments through the ContentSandbox. PDF attachments have no thin preview (retired, `§8.2`; [P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)) |

| # | Rule |
|---|---|
| <a id="rule-pv-01"></a>PV-01 | Thin preview remains read-only and bounded inside the owning application assistant; opening a supported artifact invokes that same application's handler, never embeds another product editor. |
| <a id="rule-pv-02"></a>PV-02 | **A thin preview never claims to be authoritative** ([I-060](../requirements/01-normative-glossary-and-invariants.md#rule-i-060), [AR-04](../requirements/products/arcchat.md#rule-ar-04) of the ArcChat requirements). |
| <a id="rule-pv-03"></a>PV-03 | **Where a level is not implemented, the surface degrades to the level below and says so** — a metadata card labelled as such is honest; a blank rectangle is not. |
| <a id="rule-pv-04"></a>PV-04 | **A preview never executes content** ([EC-06](#rule-ec-06)) and never fetches a remote resource referenced by the content (`§7` of the security architecture). A document that phones home when previewed is an exfiltration channel. |
| <a id="rule-pv-05"></a>PV-05 | **Preview generation is bounded in time, memory and output size**, runs off the UI thread, and a timeout degrades to the level below with a reason. |
| <a id="rule-pv-06"></a>PV-06 | **Preview output is a derived store** ([DS-01](data-model/03-derived-stores.md#rule-ds-01)–[DS-07](data-model/03-derived-stores.md#rule-ds-07) of the derived-store architecture), cached by content hash and evictable. |

### 8.2 PDF — retired (superseded 2026-10-08 by P2-022)

Native in-app PDF preview and local PDF parsing, text extraction and tile rendering are retired, and no thin PDF preview is delivered. A PDF attachment is a generic attachment: it is stored, transferred and downloaded as an opaque file and never parsed. Its actions are Save As and Open through the system handler, with no in-app parsing ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022) item 2). The assistant does not claim to read PDF content, and no AI PDF reading path exists. A metadata card (`§8.1`) with a download or share action is the only in-product representation of a PDF attachment. ArcScope report export (`arcscope.report.pdf.v1`) remains a desktop output; companions present the exported report PDF only through the platform's own viewer and never embed a PDF parser or renderer ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022) item 2). On Web, the exported report PDF is offered only as a download or open action under the original resource policy of the untrusted-content row of [requirements/12 section 20.2](../requirements/12-quality-and-compatibility-contract.md#202-browser-supportv1) (line 421). It is shown in a sandboxed frame only if the Web proof shows that an enforced sandboxed frame can host the browser's built-in PDF viewer; until that result is recorded, the frame branch is not claimed. The app performs no PDF parsing or rendering, and the report's origin sidecar travels with the PDF in the bundle. On Android, the system viewer is reached through an `ACTION_VIEW` intent. The design does not claim `nosniff` or attachment-disposition headers for download serving, or a scoped read grant for the Android handoff; no Design document states those mechanisms, so they are not preserved obligations until an authoritative rule carries them (P2-022 item 2). No writer for `arcscope.report.pdf.v1` is admitted yet, so report-export acceptance stays blocked until [SCOPE.18](../planning/delivery/lanes/arcscope.md#task-scope-18) admits one under dependency admission. No completion edge from [NAT.32](../planning/delivery/lanes/native.md#task-nat-32) to that admission is made (P2-021, coordinator confirmation (e)).

| # | Rule |
|---|---|
| <a id="rule-pd-01"></a>PD-01 | **Retired (P2-022):** PDFium, ArcForges.Native.Pdf, the arcpdf ABI and the ContentSandbox PDF parser path are not selected, built or shipped for any surface. Removal is owned by [NAT.32](../planning/delivery/lanes/native.md#task-nat-32). |
| <a id="rule-pd-02"></a>PD-02 | **The permitted native surface is not extended to PDF** (superseded 2026-10-08 by P2-022; `§2` of the native interop architecture). The only native parsing reachable from the assistant preview path is the still-image family composed into ContentSandbox by [NAT.31](../planning/delivery/lanes/native.md#task-nat-31). Every other model remains fully managed. |
| <a id="rule-pd-03"></a>PD-03 | **Retired as a PDF rule (P2-022).** No PDF renderer is wrapped. The general rule that any native parser reached from user content is isolated behind a managed wrapper with the full C ABI discipline ([AB-01](12-native-interop-and-media.md#rule-ab-01)–[AB-12](12-native-interop-and-media.md#rule-ab-12)) and runs in ContentSandbox still applies to the still-image parsers composed by [NAT.31](../planning/delivery/lanes/native.md#task-nat-31). |
| <a id="rule-pd-04"></a>PD-04 | **Retired as a PDF rule (P2-022).** A PDF is never parsed, so a malformed or hostile PDF cannot affect process stability or the surface that references it. It is handled only as a generic attachment (metadata card, download or share, `§8.1`). |
| <a id="rule-pd-05"></a>PD-05 | (Restated under P2-022.) **No PDF text is extracted.** Derived text from the supported still-image parsers is derived data ([IP-09](../requirements/06-knowledge-search-and-retrieval.md#rule-ip-09) of the knowledge requirements), rebuildable and never canonical. |
| <a id="rule-pd-07"></a>PD-07 | **Retired (P2-022):** [PG-12](../assurance/open-gates-register.md#rule-pg-12) is retired, not completed. The PDFium gate is not a delivery prerequisite, and PDF preview is not enabled on any surface. Retirement evidence is produced by [NAT.32](../planning/delivery/lanes/native.md#task-nat-32). |

### 8.4 Audio and video

| # | Rule |
|---|---|
| <a id="rule-av-03"></a>AV-03 | **Audio and video attachments have no native decode or preview family.** Every such attachment degrades to the metadata card with a stated reason ([AR-07](../requirements/products/arcchat.md#rule-ar-07) of the ArcChat requirements). |

### 8.5 Untrusted content boundaries

| # | Rule |
|---|---|
| <a id="rule-ut-01"></a>UT-01 | **Every parser reached from user content is treated as an attack surface**: bounded input size, bounded recursion, bounded time, and failure to a placeholder. |
| <a id="rule-ut-02"></a>UT-02 | Hostile complex-format and compressed-image parsing uses the mandatory [C# ContentSandbox](24-content-and-extension-isolation.md), independently of whether extensions are enabled. An unavailable enforced profile refuses that parsing operation; it never falls back to parsing in the main process. |
| <a id="rule-ut-03"></a>UT-03 | **Content instructions are never instructions** ([I-262](../requirements/01-normative-glossary-and-invariants.md#rule-i-262), [I-263](../requirements/01-normative-glossary-and-invariants.md#rule-i-263)). Text extracted from an image is data with untrusted provenance (PDF text extraction is retired under [P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)), marked as such before it can reach the agent ([WP-11.06](../planning/work-packages/11-security-foundation.md#rule-wp-11.06)). |
| <a id="rule-ut-04"></a>UT-04 | **No preview path evaluates script, macro, formula or embedded program content** in any format ([EC-06](#rule-ec-06)). |

---

## 9. What ArcForges does not build

Naming these prevents a "rich editor" from silently becoming an unbounded commitment.

| Not built | Consequence |
|---|---|
| A text shaping or font engine | Platform stack, through Avalonia ([RN-02](#rule-rn-02)) |
| A browser engine, or any HTML rendering path for content | [RN-04](#rule-rn-04); extensibility is out-of-process |
| A real-time collaborative editing engine | Excluded by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006). The retained single-owner multi-device sync model (`20-cross-system-lifecycles.md`) serves this without it; no collaboration-only reservation, hook or framework is introduced |
| A spreadsheet engine | [TB-01](#rule-tb-01) |
| An image editor | [IG-07](#rule-ig-07) |
| A diagram authoring surface | No requirement establishes one; the retained content kinds (`§7`) contain none, and none is introduced here |
| An Office rendering engine | No Office format is decoded beyond the metadata card level (`§8.1`) |

---

## 11. shared application

| Product | What this document governs |
|---|---|
| **ArcChat** | `§8` preview levels for artifacts; message content uses the same inline model for its rendered parts, and the same code and math rules |
| **ArcScope** | Report and annotation text uses the inline model and `§7` rendering; measurement content is its own model, not this one |
| **Mobile and Web** | Chat rendering surfaces reuse the model and rules, never the desktop presenters (`§3` of the mobile architecture, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**) |

| # | Rule |
|---|---|
| <a id="rule-xp-01"></a>XP-01 | **The content model is shared; the presenters are not.** A shared model in the contract layer, product-specific rendering per platform. |
| <a id="rule-xp-03"></a>XP-03 | **A mobile or web rendering surface implements a declared subset** and states what it cannot show, rather than silently discarding what it cannot represent. |

---

## 12. Verification

| # | Obligation | Where |
|---|---|---|
| <a id="rule-vf-09"></a>VF-09 | Content never round-trips through a markup string on any internal path | Repository policy test |
| <a id="rule-vf-12"></a>VF-12 | A malformed image degrades to a placeholder with a reason and no crash (PDF parsing is retired under P2-022, so no PDF input reaches a parser) | [WP-11.09](../planning/work-packages/11-security-foundation.md#rule-wp-11.09), [WP-13.13](../planning/work-packages/13-high-risk-technical-probes.md#rule-wp-13.13) (image-only containment under PLT.54 and NAT.31, P2-022 item 4) |
| <a id="rule-vf-13"></a>VF-13 | No preview path fetches a remote resource or evaluates embedded program content | [WP-11.05](../planning/work-packages/11-security-foundation.md#rule-wp-11.05) |
| <a id="rule-vf-14"></a>VF-14 | Extracted image text carries untrusted provenance (no PDF text extraction exists, P2-022) before it can reach the agent | [WP-11.06](../planning/work-packages/11-security-foundation.md#rule-wp-11.06) |
| <a id="rule-vf-15"></a>VF-15 | Copy from a code block reproduces the source exactly; copy of a table region produces a table | Repository policy test |
| <a id="rule-vf-17"></a>VF-17 | An unsupported math construct renders as source with an explicit marker, never silently wrong | [WP-17](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17) |
| <a id="rule-vf-18"></a>VF-18 | An unknown mark survives a read-modify-write cycle unchanged | Repository policy test |

