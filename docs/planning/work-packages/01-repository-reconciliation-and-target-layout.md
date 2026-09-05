# WP-01 — Repository Reconciliation and Target Layout

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `00` · Downstream: `02`

> **Goal.** Know exactly what already exists before moving any of it. Produce the item-level inventory of the existing monorepo with a disposition for every project and every native shim, then execute the highest-priority structural moves so that later packages build on the target layout rather than around it.

---

## 1. Scope and purpose

**In scope.** The item-level reconciliation inventory required by `PG-02`; the disposition decision for every existing project, test suite and native shim; and the execution of the reconciliation moves that block downstream work — principally the contract licence-boundary split and the fencing of unmigrated code.

**Out of scope.** Behaviour changes of any kind (`RC-08` in the reconciliation document). Cloud module boundary changes that require schema decisions — those belong to `21`. Per-product project reorganisation beyond what the boundary split requires — those land inside each product's own package.

**Why this package exists.** **D-011** makes the existing monorepo the implementation target and **D-012** makes it a reconciliation target. Restructuring without an inventory risks discarding conforming work, and building on the current layout risks entrenching a licence boundary violation that the mobile artifact gate (**F-023**) will later block.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../assurance/implementation-state-reconciliation.md`](../../assurance/implementation-state-reconciliation.md) | The method, disposition vocabulary, observed first-pass inventory, conformance findings and priority order |
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) | The target layout, project conventions and reference-direction rules that dispositions are measured against |
| [`../../architecture/00-architecture-overview.md`](../../architecture/00-architecture-overview.md) | The layering rules and the shared-foundation boundary |
| `WP-00` output | The licence boundary declaration and naming freeze |
| The existing monorepo | 332 project files, 25 test suites, 6 native shims, and the `eng/` build property set |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The inventory exists before restructuring begins** (`MG-04` in the solution layout; gate `PG-02`). |
| BR-02 | **Dispositions are Keep · Rename · Move · Split · Merge · Rewrite · Fence · Delete** (`RM-03` in the reconciliation document). |
| BR-03 | **Unmigrated code is fenced, not deleted** (`RM-04` there): retained but unreferenceable from conforming projects. |
| BR-04 | **A project spanning two licence boundaries is split, never excepted** (`RC-02` there, **D-004**). |
| BR-05 | **A project that is both domain and adapter is split** (`PJ-01`, `RC-03` there). |
| BR-06 | **An existing name conflicting with the glossary is renamed** (`RC-01` there, **D-018**), not preserved for familiarity. |
| BR-07 | **Deleting existing work requires an explicit disposition with a reason** (`RC-06` there). |
| BR-08 | **No step leaves the repository unbuildable at a commit boundary** (`RC-07` there). |
| BR-09 | **A commit either moves code or changes what it does, never both** (`RC-08` there). |
| BR-10 | **Existing behaviour is evidence, not authority** (`RM-07` there). Where existing code disagrees with the specification, the specification governs. |
| BR-11 | **Code already in the monorepo needs no provenance record; code of external origin does** (`RF-01`, `RF-02` there). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| Every `.csproj` under `src/` and `tests/` | Receives a disposition; those Kept receive the boundary and convention properties |
| `src/Contracts/` | **Split** into a public Apache-2.0 set and an internal AGPL set (executed in `03`; the split decision is made here) |
| `src/DesktopHelpers/` | Disposition assigned against the shared-foundation boundary |
| `src/BuildingBlocks/ArcForges.Desktop.*` | Reviewed against the shared-foundation boundary; mechanism-only projects Kept, product-aware projects Split or Moved |
| `src/Cloud/Modules.*` | Inventoried and mapped to the sixteen architecture modules; execution deferred to `21` |
| `native/` | Each of the six shims receives a permitted-surface decision and a licence review |
| `tests/` | Each suite mapped to a required test family; gaps recorded |
| `fixtures/` | Created as an empty, documented root for golden fixtures |
| `eng/policy/reconciliation/` | The inventory itself, as reviewable data |

**Major types introduced:** none.

---

## 5. Required implementation work

### WP-01.00 — Produce the item-level inventory

**What must be fully done.** Every existing project, test suite, native shim and top-level directory receives an inventory row with all nine required fields: identifier, existing path, target path, disposition, licence boundary, conformance findings, migration slice, owner and risk. External-origin code is identified (`BR-11`) and its provenance status recorded.

**Testing requirements.** A completeness check that no project file is absent from the inventory and no row has a missing field; a consistency check that every target path is valid under the target layout.

**Completion gate.** The inventory covers 100 % of projects with no missing fields, and is approved by the Architecture Owner. **This satisfies `PG-02`.**

### WP-01.01 — Decide the contract split

**What must be fully done.** Every type in the existing contract projects is assigned to the public Apache-2.0 set or the internal AGPL set, using the enumerated Apache set from `WP-00.02`. Types that are currently public but should not be, and types that are currently internal but must be public for interoperability, are both identified. The split is decided here and executed in `03`.

**Testing requirements.** A review that every contract type has an assignment; a check that no type assigned to the public set transitively depends on an internal type.

**Completion gate.** The assignment is complete and dependency-consistent. **This is the highest-priority reconciliation item** (`§3` of the reconciliation document).

### WP-01.02 — Shared-foundation boundary review

**What must be fully done.** Every building-block project is classified as mechanism-only or product-aware. Mechanism-only projects are Kept. Product-aware content is moved into the owning product or split out. The shared-foundation boundary rules (`§7` of the architecture overview) are the criterion.

**Testing requirements.** A reference check that no building-block project references a product project; a review record for each reclassification.

**Completion gate.** No product knowledge remains in the shared foundation, and the reference check passes.

### WP-01.03 — Native surface reconciliation

**What must be fully done.** Each of the six native shims receives a permitted-surface decision against `§2` of the native architecture and a licence review against the consuming product's boundary. A shim outside the permitted surface is narrowed with a recorded decision or removed from the product path (`RC-05` there).

**Testing requirements.** A check that every shipped native asset has a recorded licence position and a permitted-surface decision.

**Completion gate.** Every shim has both decisions recorded. **This partially satisfies `PG-03`**; per-product native dependency review continues in `13`, `33` and `36`.

### WP-01.04 — Test suite mapping

**What must be fully done.** Every existing test suite is mapped to one of the eighteen required families. Families with no home are recorded as gaps and assigned to the package that will create them. The repository-policy suite is identified as absent and scheduled for `05`.

**Testing requirements.** A coverage report: family → suite, with gaps explicit.

**Completion gate.** Every family has either an existing suite or a named future package.

### WP-01.05 — Execute the blocking moves and fence the rest

**What must be fully done.** The moves that block downstream work are executed: contract project structure created (types moved in `03`), shared-foundation violations resolved, and everything else with a non-`Keep` disposition fenced so a conforming project cannot reference it. Each move is a separate commit that does not change behaviour (`BR-09`).

**Testing requirements.** The repository builds green at every commit boundary (`BR-08`); a reference check that no conforming project references fenced code.

**Completion gate.** The repository builds, fenced code is unreferenceable, and the remaining dispositions are scheduled against named packages.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None — schema changes are deferred to `07` and `21` |
| Protocol | The contract split decision determines which types are publicly versioned; execution in `03` |
| UI | None |
| Security | The licence boundary becomes structurally enforceable, which the mobile artifact gate depends on |
| Platform | Native shim decisions determine which platforms can ship which product capability |
| Migration | None to user data |
| Compatibility | Establishes the project structure that contract version axes attach to |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| The item-level inventory, 100 % coverage, approved | `WP-01.00` |
| The contract type assignment, dependency-consistent | `WP-01.01` |
| Shared-foundation reference check, clean | `WP-01.02` |
| Native shim decision records, one per shim | `WP-01.03` |
| Test family coverage report with explicit gaps | `WP-01.04` |
| Green build at every commit boundary; fenced-reference check clean | `WP-01.05` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. The item-level inventory exists, covers every project, test suite and native shim with no missing fields, and is approved — satisfying `PG-02`.
2. Every contract type is assigned to a licence boundary, with no public type depending on an internal one.
3. No product knowledge remains in the shared foundation.
4. Every native shim has a permitted-surface decision and a licence position.
5. Every required test family maps to an existing suite or a named future package.
6. The blocking moves are executed, the repository builds green, and all remaining non-`Keep` code is fenced and unreferenceable.

---

## 9. Dependencies

**Upstream.**

| Package | What this needs from it |
|---|---|
| `00` | The licence boundary declaration, the naming freeze and the glossary policy data |

**Downstream.**

| Package | What it needs from here |
|---|---|
| `02` — Build governance | A settled project set to apply conventions to |
| `03` — Contract foundation | The contract type assignment decided here |
| `21` — Cloud host | The cloud module inventory and mapping |
| `13`, `33`, `36` | The native shim decisions |
| Every later package | A target layout it can build into rather than around |
