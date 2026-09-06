# WP-29 — ArcNotes Slides and Presentation · **RETIRED**

> Status: **Retired** by **[P2-006](../../decisions/phase-2-specification-decisions.md)**, 2026-09-06
> Layer: Planning · Work package
> Retired-in-place: this identifier is **not reused** for other work

---

## Why this package no longer exists

**P2-006 removes slides, presentations, slide generation, frame ordering and presentation navigation from required ArcNotes delivery**, with no mandatory future hook. The [D-006 amendment of 2026-09-06](../../decisions/phase-1-foundation-decisions.md) records it at decision level, and the glossary entry `ArcNotes.Slides` is retired.

---

## What happened to its content

| Former content | Disposition |
|---|---|
| Slides as a presentation view over document and canvas content | **Dropped.** Canvas is also retired (`WP-27`), so the projection had no remaining source |
| `slide_deck`, `slide`, `speaker_note` tables | **Retired** from the desktop data model (`§3` there) |
| Presentation navigation and frame ordering | **Dropped** |
| Reference-coverage finding **F-AN-2** — *neither reference implements slides, so `WP-29` has no reference oracle* | **Closes by scope rather than by evidence.** The missing oracle no longer matters because the capability is not delivered |

---

## Rules that survive its retirement

| # | Rule |
|---|---|
| RT-01 | **The identifier `WP-29` is retired and never reused.** |
| RT-02 | **`WP-50` no longer depends on it.** The full-platform release gate drops `29` from its upstream set. |
| RT-03 | **`WP-28` has no downstream successor in Phase F.** Phase F is now a single package. |
| RT-04 | **No dormant hook remains** in the block model, the schema or the export formats. |
