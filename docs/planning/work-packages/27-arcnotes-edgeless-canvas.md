<a id="rule-wp-27"></a>

# WP-27 — ArcNotes Edgeless Canvas · **RETIRED**

> Status: **Retired** by **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)**, 2026-09-06
> Layer: Planning · Work package
> Retired-in-place: this identifier is **not reused** for other work

---

## Why this package no longer exists

**[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) removes Edgeless Canvas, whiteboard surfaces, shapes, connectors and frames from required ArcNotes delivery**, with no mandatory future hook. The [D-006 amendment of 2026-09-06](../../decisions/phase-1-foundation-decisions.md#rule-d-006) records the same change at decision level, and the [ArcNotes requirements](../../requirements/products/arcnotes.md) no longer contain the capability.

The original package existed to satisfy the previous [D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006) outcome, in which Stage 15 was a baseline rather than a ceiling and canvas was in complete scope, phased. That outcome is superseded, so the work is not deferred — it is **out of scope**.

---

## What happened to its content

| Former content | Disposition |
|---|---|
| Canvas as one content model with the document surface | **Dropped.** The block model has no canvas construct (`§2.1` of the editing architecture) |
| `canvas`, `canvas_element` tables | **Retired** from the desktop data model (`§3` there) |
| <a id="rule-wp-27.01"></a>Placement-syncs / viewport-is-local rule ([WP-27.01](#rule-wp-27.01)) | **Dropped** with the capability |
| Surface-reference block kind | **Dropped.** `embed` references a document, block or saved view only |
| Reference-coverage rows [AN-03](../../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-an-03) (AFFiNE edgeless) | Reclassified as **accepted exclusion** in the [ArcNotes matrix](../../assurance/reference-coverage/arcnotes-affine-siyuan.md) |

---

## Rules that survive its retirement

| # | Rule |
|---|---|
| RT-01 | **The identifier [WP-27](#rule-wp-27) is retired and never reused.** A future spatial-editing capability would receive a new identifier and its own scope decision. |
| RT-02 | **Nothing downstream may depend on this package.** [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28) now takes its upstream from `19` and `25` directly, and [WP-50](50-full-platform-production-release.md#rule-wp-50) no longer routes through it. |
| RT-03 | **No dormant hook remains.** Retaining an empty canvas table or a reserved block kind would make an excluded capability look like a configuration switch, which is precisely the ambiguity [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) removes ([WO-04](../../architecture/data-model/01-cloud-data-model.md#rule-wo-04) analogue). |
| RT-04 | **This file is the record, not a placeholder.** It is not revived by editing; reintroducing the capability requires a new decision under **[D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001)**. |
