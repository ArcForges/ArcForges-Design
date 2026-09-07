# Reference Coverage Matrices

> Status: **Authoritative** — Phase 2 (Detailed Specifications), design-stage evidence
> Layer: Assurance
> Governing authority: **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)** as amended 2026-09-05 (per-product matrix before implementation planning is finalized), **[P2-005](../../decisions/phase-2-specification-decisions.md#rule-p2-005)** (ArcSlate reference baseline), **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)** (reuse policy and provenance), **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)** (licence boundaries)
> Companions: [`../reference-coverage-and-provenance.md`](../reference-coverage-and-provenance.md) (method), [`../open-gates-register.md`](../open-gates-register.md)

These are the **completed design-stage Reference Coverage Matrices** required by **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**. They are evidence, not templates and not future audit instructions.

Each matrix was produced by reading the named reference repository at a recorded commit: its licence files, source tree, tests, packaging and documentation, to the depth needed to establish an item-level position. Every reviewed item carries an evidence location, the source identity and commit, an ArcForges requirement or an explicit exclusion, a disposition, a rationale, a licensing and provenance position, a verification oracle and an owner.

> **Reference map amendment, 2026-09-05.** **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**'s ArcSlate line is amended by user decision [P2-005](../../decisions/phase-2-specification-decisions.md#rule-p2-005): **ArcVideo and ArcVideoFoundation** are ArcSlate's direct references, and there is no requirement to obtain or independently review an Olive repository. **This narrows the audit scope, not the provenance obligation** — ArcVideo is a documented Olive fork, and its GPL-3.0 obligations, upstream copyright and attribution to the Olive authors are preserved wherever inherited material requires them (`§3.1` of that matrix).

> **Scope amendment, 2026-09-06 ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)).** The revised requirements exclude capabilities several rows previously mapped to: Edgeless canvas and slides (ArcNotes), external-agent integration and agent teams (ArcChat), and end-user BYOK. Those rows are **reclassified as accepted exclusions with their reason recorded**, never deleted — the evidence that the capability was reviewed and deliberately dropped is worth more than a shorter matrix. Portfolio totals across 145 rows are now **121 evidence established, 25 accepted exclusions, 0 unresolved**; [AN-14](arcnotes-affine-siyuan.md#rule-an-14) remains the one compound row, so the figures sum to 146 over 145 rows. **No row in any matrix proposes reuse.**

---

## Matrix set

| Matrix | Reference(s) | Consuming product | State |
|---|---|---|---|
| [`arcchat-aionui.md`](arcchat-aionui.md) | AionUi | ArcChat | **Complete** |
| [`arcnotes-affine-siyuan.md`](arcnotes-affine-siyuan.md) | AFFiNE, SiYuan | ArcNotes | **Complete** |
| [`arcscope-serial-studio.md`](arcscope-serial-studio.md) | Serial-Studio | ArcScope | **Complete** |
| [`arcslate-arcvideo.md`](arcslate-arcvideo.md) | ArcVideo, ArcVideoFoundation | ArcSlate | **Complete** |
| [`distribution-startarcforges.md`](distribution-startarcforges.md) | StartArcForges | Distribution and release | **Complete within the authorized oracle boundary** |

---

## Source identity

Every matrix is bound to a specific commit. Re-reading a reference at a different commit produces a different matrix; the drift check in each product's implementation package compares against these recorded commits.

| Reference | Origin | Commit | Commit date | Root licence as found |
|---|---|---|---|---|
| AionUi | `github.com/iOfficeAI/AionUi` | `29c9271a5` | 2026-07-14 | Apache-2.0 (`LICENSE`) |
| AFFiNE | `github.com/toeverything/AFFiNE` | `81df4751a3` | 2026-07-19 | **Split** — see the matrix `§2` |
| SiYuan | `github.com/siyuan-note/siyuan` | `eef105683` | 2026-07-21 | AGPL-3.0 (`LICENSE`) |
| Serial-Studio | `github.com/Serial-Studio/Serial-Studio` | `639daafb` | 2026-07-13 | **Dual GPL-3.0-only / commercial** — see the matrix `§2` |
| ArcVideo | `github.com/ArcForges/ArcVideo` | `caf5651` | 2026-03-16 | GPL-3.0 (`LICENSE`) |
| ArcVideoFoundation | `github.com/ArcForges/ArcVideoFoundation` | `139eeca` | 2026-03-30 | GPL-3.0 (`LICENSE`) |
| StartArcForges | local packaged-output tree | not a git repository | — | Per-product bundled notices |

---

## Completeness vocabulary

Every row carries exactly one of three states. They are not interchangeable, and a filled template column is not evidence.

| State | Meaning |
|---|---|
| **Evidence established** | The reference material was read, its position is determined, and the disposition follows from the evidence |
| **Accepted exclusion** | The item exists in the reference and is deliberately out of ArcForges scope; the reason is recorded and it becomes no requirement |
| **Unresolved determination** | The item's position cannot be settled from the accessible material; the exact blocker and its owner are recorded, and it blocks whatever depends on it. **None remains across the five matrices** — the one that existed was closed by [P2-005](../../decisions/phase-2-specification-decisions.md#rule-p2-005) |

| # | Rule |
|---|---|
| RC-01 | **A disposition is never inferred from the repository-root licence** (**[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**). Where a subtree carries a different licence, the subtree's licence governs. |
| <a id="rule-rc-02"></a>RC-02 | **Reference capability ≠ ArcForges requirement.** An item maps to an existing requirement, or it is an accepted exclusion. It does not create a requirement by existing. |
| <a id="rule-rc-03"></a>RC-03 | **`Reference Only` is the default disposition** where the licence prohibits reuse or where ArcForges' own design already governs the area. |
| RC-04 | **A `Copy`, `Rewrite`, `Improve` or `Replace` disposition additionally requires the full ten-field provenance record of [D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)** before any material moves. No row in this matrix set carries such a disposition without that requirement stated. |
| RC-05 | **These matrices are versioned planning inputs.** Implementation packages consume them; they do not re-create them. Later drift, changed scope and newly introduced material are handled by the maintenance check in each product package, not by a second baseline audit. |

---

## Aggregate licence position

The single most consequential finding across all five matrices — six registered references:

| Reference | Effective position for reuse | Consequence |
|---|---|---|
| AionUi | **Apache-2.0, permissive** | The only reference whose material may, after a per-file provenance record, enter either the AGPL or the Apache-2.0 boundary |
| AFFiNE — `blocksuite/**`, `packages/frontend/**`, `packages/common/**` except `native` | **MIT, permissive** | Reusable after a per-file provenance record |
| AFFiNE — `packages/backend/**`, `packages/common/native/**` | **Proprietary (Enterprise Edition licence)** | **Not reusable in any form.** Reference Only, and behavioural reference must not reproduce its expression |
| SiYuan | **AGPL-3.0** | Reusable only inside the AGPL boundary after exact compatibility and provenance review; **prohibited** in the Apache mobile and public-client boundary |
| Serial-Studio — GPL portion | **GPL-3.0-only** | **Not copyable, translatable or portable** under **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**. Reference Only |
| Serial-Studio — Pro modules | **Commercial-only, excluded from GPL** | Reference Only, and the excluded module list is respected as an authorship boundary |
| ArcVideo, ArcVideoFoundation | **GPL-3.0-only** | **Not copyable, translatable or portable** under **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**. Reference Only |

**Consequence for the whole programme.** Four of the six registered references are GPL-family, proprietary, or AGPL. Only AionUi and AFFiNE's MIT subtrees are permissively licensed. **No matrix row proposes copying, porting or translating reference source into ArcForges.** Every product is therefore an original implementation informed by behavioural evidence, and the **[F-013](../open-gates-register.md#rule-f-013)** determinations recorded here are what establishes that.

---

## What these matrices do not do

| # | Statement |
|---|---|
| ND-01 | **They record the [F-013](../open-gates-register.md#rule-f-013) determinations**; the gate is closed on that evidence ([`../open-gates-register.md`](../open-gates-register.md)). |
| <a id="rule-nd-02"></a>ND-02 | **They do not authorize any reuse.** No row proposes reuse; if one ever did, the ten-field provenance record would still be required first. |
| ND-03 | **They do not create requirements.** Items map to existing requirements or become accepted exclusions. |
| ND-04 | **They do not replace drift checking.** Each product's implementation package re-checks the recorded commit for drift and newly introduced material. |
| ND-05 | **No reference repository was modified, and no packaged binary was executed.** |
| ND-06 | **They do not remove upstream provenance.** Where a reference is itself a fork, its upstream copyright, licence obligations and attribution are recorded and retained, independently of which repositories the reference map registers. |
