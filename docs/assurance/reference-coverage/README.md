# Reference Coverage Matrices

> Status: **Authoritative** — Phase 2 (Detailed Specifications), design-stage evidence
> Layer: Assurance
> Governing authority: **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)** as amended 2026-09-05 (per-product matrix before implementation planning is finalized), **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)** (reuse policy and provenance), **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)** (licence boundaries)
> Companions: [`../reference-coverage-and-provenance.md`](../reference-coverage-and-provenance.md) (method), [`../open-gates-register.md`](../open-gates-register.md)

These are the **completed design-stage Reference Coverage Matrices** required by **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**. They are evidence, not templates and not future audit instructions.

Each matrix was produced by reading the named reference repository at a recorded commit: its licence files, source tree, tests, packaging and documentation, to the depth needed to establish an item-level position. Every reviewed item carries an evidence location, the source identity and commit, an ArcForges requirement or an explicit exclusion, a disposition, a rationale, a licensing and provenance position, a verification oracle and an owner.

> **Scope amendment, 2026-09-06 ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)).** The revised requirements exclude capabilities several rows previously mapped to: external-agent integration and agent teams (ArcChat), and end-user BYOK. Those rows are **reclassified as accepted exclusions with their reason recorded**, never deleted — the evidence that the capability was reviewed and deliberately dropped is worth more than a shorter matrix. Portfolio totals across 69 rows are **55 evidence established, 14 accepted exclusions, 0 unresolved**. **No row in any matrix proposes reuse.**

---

## Matrix set

| Matrix | Reference(s) | Consuming product | State |
|---|---|---|---|
| [`arcchat-aionui.md`](arcchat-aionui.md) | AionUi | ArcChat | **Complete** |
| [`arcscope-serial-studio.md`](arcscope-serial-studio.md) | Serial-Studio | ArcScope | **Complete** |
| [`distribution-startarcforges.md`](distribution-startarcforges.md) | StartArcForges | Distribution and release | **Complete within the authorized oracle boundary** |

---

## Source identity

Each matrix is bound to its versioned Design document and the source identity below. The two Git references have recorded commits; StartArcForges instead has observed artifact versions under its authorized directory/notice boundary. The [registration profile](../reference-baseline-registration.md) defines the machine-readable binding and later drift checks; a different source revision requires a reviewed delta, not a second baseline audit.

| Reference | Origin | Commit | Commit date | Root licence as found |
|---|---|---|---|---|
| AionUi | `github.com/iOfficeAI/AionUi` | `29c9271a5` | 2026-07-14 | Apache-2.0 (`LICENSE`) |
| Serial-Studio | `github.com/Serial-Studio/Serial-Studio` | `639daafb` | 2026-07-13 | **Dual GPL-3.0-only / commercial** — see the matrix `§2` |
| StartArcForges | local packaged-output tree | not a git repository | — | Per-product bundled notices |

---

## Completeness vocabulary

Every row carries exactly one of three states. They are not interchangeable, and a filled template column is not evidence.

| State | Meaning |
|---|---|
| **Evidence established** | The reference material was read, its position is determined, and the disposition follows from the evidence |
| **Accepted exclusion** | The item exists in the reference and is deliberately out of ArcForges scope; the reason is recorded and it becomes no requirement |
| **Unresolved determination** | The item's position cannot be settled from the accessible material; the exact blocker and its owner are recorded, and it blocks whatever depends on it. **None remains across the three matrices.** |

| # | Rule |
|---|---|
| <a id="rule-rc-01"></a>RC-01 | **A disposition is never inferred from the repository-root licence** (**[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**). Where a subtree carries a different licence, the subtree's licence governs. |
| <a id="rule-rc-02"></a>RC-02 | **Reference capability ≠ ArcForges requirement.** An item maps to an existing requirement, or it is an accepted exclusion. It does not create a requirement by existing. |
| <a id="rule-rc-03"></a>RC-03 | **`Reference Only` is the default disposition** where the licence prohibits reuse or where ArcForges' own design already governs the area. |
| <a id="rule-rc-04"></a>RC-04 | **A `Copy`, `Rewrite`, `Improve` or `Replace` disposition additionally requires the full ten-field provenance record of [D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)** before any material moves. No row in this matrix set carries such a disposition without that requirement stated. |
| <a id="rule-rc-05"></a>RC-05 | **These matrices are versioned planning inputs.** Implementation packages consume them; they do not re-create them. Later drift, changed scope and newly introduced material are handled by the maintenance check in each product package, not by a second baseline audit. |

---

## Aggregate licence position

The single most consequential finding across all three matrices — two registered references:

| Reference | Effective position for reuse | Consequence |
|---|---|---|
| AionUi | **Apache-2.0, permissive** | The only reference whose material may, after a per-file provenance record, enter either the AGPL or the Apache-2.0 boundary |
| Serial-Studio — GPL portion | **GPL-3.0-only** | **Not copyable, translatable or portable** under **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**. Reference Only |
| Serial-Studio — Pro modules | **Commercial-only, excluded from GPL** | Reference Only, and the excluded module list is respected as an authorship boundary |

**Consequence for the whole programme.** Serial-Studio is GPL-family across its GPL portion and commercial-only across its Pro modules; only AionUi is permissively licensed. **No matrix row proposes copying, porting or translating reference source into ArcForges.** Every product is therefore an original implementation informed by behavioural evidence, and the **[F-013](../open-gates-register.md#rule-f-013)** determinations recorded here are what establishes that.

---

## What these matrices do not do

| # | Statement |
|---|---|
| <a id="rule-nd-01"></a>ND-01 | **They record the [F-013](../open-gates-register.md#rule-f-013) determinations**; the gate is closed on that evidence ([`../open-gates-register.md`](../open-gates-register.md)). |
| <a id="rule-nd-02"></a>ND-02 | **They do not authorize any reuse.** No row proposes reuse; if one ever did, the ten-field provenance record would still be required first. |
| <a id="rule-nd-03"></a>ND-03 | **They do not create requirements.** Items map to existing requirements or become accepted exclusions. |
| <a id="rule-nd-04"></a>ND-04 | **They do not replace drift checking.** Each product's implementation package re-checks the recorded commit for drift and newly introduced material. |
| <a id="rule-nd-05"></a>ND-05 | **No reference repository was modified, and no packaged binary was executed.** |
| <a id="rule-nd-06"></a>ND-06 | **They do not remove upstream provenance.** Where a reference is itself a fork, its upstream copyright, licence obligations and attribution are recorded and retained, independently of which repositories the reference map registers. |
