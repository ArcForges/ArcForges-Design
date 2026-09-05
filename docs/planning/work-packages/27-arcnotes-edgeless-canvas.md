# WP-27 — ArcNotes Edgeless Canvas

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: F — ArcNotes completion
> Upstream: `19`, `25` · Downstream: `28`

> **Goal.** Add the spatial editing surface as **one content model with the document surface**, not a second incompatible data structure — the first step of the phased full inclusion **D-006** requires.

---

## 1. Scope and purpose

**In scope.** The edgeless canvas: spatial arrangement of content, canvas-native elements, the shared content semantics between document and canvas surfaces, canvas navigation and selection, export and import of canvas content, sync of canvas content, and the migration path from V1 documents.

**Out of scope.** Database views (`28`) and slides (`29`). Real-time multi-user collaboration, which the corpus places later and which must not block local product completion.

**Why this package exists.** `I2 §III.7` is explicit that edgeless comes first, because it establishes unified content semantics for document and spatial surfaces. Building database views or slides before that unification would fork the content model.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| **D-006** | Phased full inclusion of edgeless, database views and slides |
| `I2 §III.7` | The ordering and the backward-compatibility requirement |
| [`../../requirements/products/arcnotes.md`](../../requirements/products/arcnotes.md) | The canvas model within the product |
| `WP-18`, `WP-19`, `WP-25` output | The V1 baseline, the export path and the sync engine |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Every step must maintain backward migration compatibility with V1 documents** (`I2 §III.7`). **No incompatible secondary data structure may be created.** |
| BR-02 | **Document and canvas share one content model.** A block is a block wherever it appears; only its placement differs. |
| BR-03 | **Operation and revision compatibility boundaries are not violated**, even though multi-user collaboration is later (`I2 §III.7`). |
| BR-04 | **The V1 format fixture must still open correctly** after this package. |
| BR-05 | **Canvas placement is content, not layout state.** It syncs; window and viewport state does not. |
| BR-06 | **An embedded reference's editing authority stays with the original object** (`BR-09` in `WP-18`). |
| BR-07 | **Canvas content is exportable and re-importable** through the native package with equivalence. |
| BR-08 | **Performance is budgeted for a large canvas**, with virtualisation rather than degradation. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcNotes/ArcNotes.Domain/` | Canvas, canvas element, placement, grouping, connector; unified with block content |
| `src/ArcNotes/ArcNotes.Edgeless/` | The canvas surface: rendering, hit testing, selection, navigation, virtualisation |
| `src/ArcNotes/ArcNotes.Infrastructure/` | Schema migration from V1 adding canvas without breaking documents |
| `src/ArcNotes/ArcNotes.ImportExport/` | Canvas export and import in the native package |
| `src/ArcNotes/ArcNotes.CloudClient/` | Canvas content in the sync scope |
| `fixtures/formats/arcnotes/v2/` | The canvas-era fixture, alongside the retained V1 fixture |
| `tests/VirtualizationTests/` | Large-canvas virtualisation and responsiveness |

**Major types introduced.** `Canvas`, `CanvasElement`, `ElementPlacement`, `ElementGroup`, `Connector`, `CanvasViewport`, `CanvasSelection`, `FrameElement`.

---

## 5. Required implementation work

### WP-27.00 — Unified content semantics

**What must be fully done.** The content model is extended so that the same block content can exist in a document or on a canvas, with placement as an additional dimension rather than a separate representation. Moving content between surfaces preserves identity and history.

**Testing requirements.** A move-between-surfaces test asserting identity and history are preserved; a structural test asserting no duplicate content representation exists.

**Completion gate.** Content moves between document and canvas with identity and history preserved, and no second content representation exists.

### WP-27.01 — Canvas surface and navigation

**What must be fully done.** Pan, zoom, fit, selection, multi-selection, grouping, alignment and connectors. Navigation state is device-local; placement is content. Keyboard accessibility for every canvas operation.

**Testing requirements.** Interaction coverage per operation; a keyboard-only completion test; a device-local assertion for viewport state.

**Completion gate.** Every canvas operation is keyboard-completable, and viewport state never syncs.

### WP-27.02 — Migration from V1

**What must be fully done.** A schema migration adding canvas support that leaves every V1 document readable and editable. A V1 document opens unchanged; a document that has never used a canvas gains no canvas artefacts.

**Testing requirements.** Migration from the retained V1 fixture with semantic comparison; a no-op assertion that a canvas-free document is unchanged; a downgrade behaviour test.

**Completion gate.** **The V1 fixture still opens and round-trips correctly**, and a canvas-free document is unchanged by the migration.

### WP-27.03 — Export, import and sync

**What must be fully done.** Canvas content exports and re-imports through the native package with equivalence. Canvas content syncs through the existing engine with the existing conflict policies; placement conflicts resolve under a declared policy.

**Testing requirements.** Round-trip equivalence including placement; a multi-device canvas convergence test; a placement-conflict test.

**Completion gate.** Canvas content round-trips with equivalence and converges across devices under a declared conflict policy.

### WP-27.04 — Performance at scale

**What must be fully done.** Virtualised rendering so a large canvas remains responsive. Scale corpus targets defined for element count and content weight. Memory stays within the product's ceiling.

**Testing requirements.** Scale corpus interaction measurements; a memory ceiling assertion; a soak test on a large canvas.

**Completion gate.** A large canvas meets responsiveness and memory budgets under the scale corpus.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Schema version 2 with canvas, migrating from V1 without loss |
| Protocol | Canvas content in the sync and capability contracts |
| UI | The canvas surface within the shared shell |
| Security | Unchanged; canvas content follows document permission |
| Platform | Rendering performance verified per platform |
| Migration | The first real ArcNotes schema migration with a retained V1 fixture |
| Compatibility | The V1 baseline must remain readable indefinitely |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Move-between-surfaces and no-duplicate-representation results | `WP-27.00` |
| Canvas interaction and keyboard completion results | `WP-27.01` |
| V1 fixture migration and no-op assertions | `WP-27.02` |
| Round-trip equivalence and multi-device convergence results | `WP-27.03` |
| Scale corpus responsiveness, memory and soak results | `WP-27.04` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Content moves between document and canvas with identity and history preserved; no second content representation exists.
2. Every canvas operation is completable by keyboard; viewport state is device-local and never syncs.
3. **The retained V1 fixture still opens, edits and round-trips correctly**, and a canvas-free document is unchanged by the migration.
4. Canvas content round-trips through the native package with equivalence and converges across devices under a declared conflict policy.
5. A large canvas meets responsiveness and memory budgets under the scale corpus.

---

## 9. Dependencies

**Upstream.** `19` (export path), `25` (sync engine).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `28` — Database views | The unified content semantics established here |
| `29` — Slides | Document and canvas content as slide sources |
