# WP-29 — ArcNotes Slides and Presentation

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: F — ArcNotes completion
> Upstream: `28` · Downstream: `50`

> **Goal.** Complete the phased inclusion **D-006** requires: a presentation view built on existing document and canvas content, with export, history and recovery — and the V1 baseline still readable.

---

## 1. Scope and purpose

**In scope.** The slide model as a projection over existing content; slide composition, ordering and transitions; the presentation mode; speaker view where the platform supports it; slide export to the native package and to a portable presentation form; and the final ArcNotes compatibility position across every schema version.

**Out of scope.** A full presentation-authoring product with animation timelines. Live collaborative presenting.

**Why this package exists.** `I2 §III.7` places slides last because they build on document and canvas content. Building slides first would have produced a third content model.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| **D-006** | The third and final phase of the ArcNotes inclusion |
| `I2 §III.7` | Slides build on document and canvas content |
| [`../../requirements/products/arcnotes.md`](../../requirements/products/arcnotes.md) | The slide scope and its non-goals |
| `WP-27`, `WP-28` output | Canvas content and query-driven views as slide sources |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **A slide is a projection over existing content**, not a fourth content model. |
| BR-02 | **Backward compatibility with V1, canvas-era and views-era content is preserved.** |
| BR-03 | **Presenting is a mode, not a separate document.** Exiting presentation returns to the same content unchanged. |
| BR-04 | **Slide export states its fidelity** and never silently drops content. |
| BR-05 | **Presentation mode is accessible**: keyboard navigable, with assistive-technology semantics for slide structure. |
| BR-06 | **No animation timeline** — ArcNotes is not becoming a motion-graphics tool. |
| BR-07 | **Presentation display selection and viewport are device-local**, never synced work content. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcNotes/ArcNotes.Slides/` | Slide model, composition, ordering, presentation mode, speaker view |
| `src/ArcNotes/ArcNotes.Domain/` | Slide deck as a projection definition over content |
| `src/ArcNotes/ArcNotes.ImportExport/` | Slide export writers with stated fidelity |
| `src/ArcNotes/ArcNotes.Infrastructure/` | Schema migration adding slide decks |
| `fixtures/formats/arcnotes/v4/` | The slides-era fixture, with V1, V2 and V3 retained |
| `tests/ArcNotes.Tests.Ui/` | Presentation mode, keyboard navigation and accessibility suites |

**Major types introduced.** `SlideDeck`, `Slide`, `SlideSource`, `SlideOrder`, `SlideTransition`, `PresentationSession`, `SpeakerNote`, `DisplayTarget`.

---

## 5. Required implementation work

### WP-29.00 — Slide model as projection

**What must be fully done.** A deck references existing document sections, canvas frames or view results as slide sources. Editing a source updates its slide; editing a slide edits the source through the same write path. No slide holds a private copy of content.

**Testing requirements.** A source-edit propagation test; a structural test asserting no private content copy; a write-path assertion for slide edits.

**Completion gate.** Slides project existing content with no private copy, and edits flow through the single write path.

### WP-29.01 — Composition and ordering

**What must be fully done.** Adding, removing, reordering and grouping slides; per-slide layout selection; speaker notes as content associated with a slide, not embedded in the source. Simple transitions only.

**Testing requirements.** Composition operation coverage; a speaker-note association test asserting notes do not appear in the source content.

**Completion gate.** Composition operations work and speaker notes never leak into source content.

### WP-29.02 — Presentation mode

**What must be fully done.** A full-screen presentation mode with keyboard navigation, a display target selection where multiple displays exist, and a speaker view where the platform supports it. Exiting returns to the exact prior state.

**Testing requirements.** Keyboard navigation coverage; multi-display selection test; an exit-state test; an accessibility pass with assistive technology.

**Completion gate.** Presentation is fully keyboard navigable, exits cleanly to the prior state, and passes the accessibility pass.

### WP-29.03 — Export

**What must be fully done.** Export to the native package with full fidelity, and to a portable presentation form with its fidelity stated before writing. A printable form is available.

**Testing requirements.** Native round-trip equivalence; a fidelity-statement check for the portable form; a print-output check.

**Completion gate.** Native export round-trips with equivalence and every lossy target states its losses before writing.

### WP-29.04 — Final compatibility position

**What must be fully done.** All four ArcNotes schema versions are readable, with the migration chain tested end to end from V1. The compatibility position is documented: which versions are readable, which are writable, and what a downgrade does.

**Testing requirements.** A full V1 → V4 migration chain test with semantic comparison at every step; a downgrade behaviour test from each version.

**Completion gate.** **The full V1 → V4 migration chain preserves semantics at every step**, and downgrade behaviour is defined and tested from each version.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Schema version 4 with slide decks |
| Protocol | Slide decks in export and sync |
| UI | Presentation and speaker surfaces |
| Security | Unchanged; slides follow source permission |
| Platform | Multi-display and presentation behaviour per platform |
| Migration | The complete ArcNotes migration chain |
| Compatibility | ArcNotes' final compatibility position across four versions |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Projection, no-copy and write-path results | `WP-29.00` |
| Composition and speaker-note isolation results | `WP-29.01` |
| Keyboard, multi-display, exit-state and accessibility results | `WP-29.02` |
| Native round-trip and fidelity-statement results | `WP-29.03` |
| Full V1 → V4 chain and downgrade results | `WP-29.04` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Slides project existing content with no private copy; slide edits flow through the single write path.
2. Composition operations work; speaker notes never leak into source content.
3. Presentation mode is fully keyboard navigable, exits cleanly to the prior state, and passes the accessibility pass.
4. Native export round-trips with equivalence; every lossy target states its losses before writing.
5. **The full V1 → V4 migration chain preserves semantics at every step**, and downgrade behaviour is defined and tested from each version.
6. **ArcNotes is complete per D-006**, with edgeless, database views and slides all delivered on one content model.

---

## 9. Dependencies

**Upstream.** `28` (properties, queries and views).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `50` — Production release | ArcNotes as a complete product against **D-006** |
