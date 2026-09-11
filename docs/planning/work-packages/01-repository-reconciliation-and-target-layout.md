<a id="rule-wp-01"></a>

# WP-01 — Repository Reconciliation and Target Layout

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `00` · Downstream: `02`

> **Goal.** Execute the dispositions the completed inventory already records. The highest-priority item is not a move but a correction: **55 source files declare a licence Phase 1 forbids for their boundary.**

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform and new owners. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** **Executing** the dispositions recorded in the completed inventory; validating it against current head; and the reconciliation moves that block downstream work — principally the contract licence-boundary correction and the fencing of unmigrated code.

**Out of scope.** Behaviour changes of any kind ([RC-08](../../requirements/11-policy-and-configuration.md#rule-rc-08) in the reconciliation document). Cloud module boundary changes that require schema decisions — those belong to `21`. Per-product project reorganisation beyond what the boundary split requires — those land inside each product's own package.

**Why this package exists.** The inventory is complete; its dispositions are not executed. `§5.1` of the reconciliation evidence found **55 files actively declaring a licence that Phase 1 forbids for their boundary** — a defect, not merely pending work, and one the mobile artifact gate (**[F-023](../../assurance/open-gates-register.md#rule-f-023)**) will block.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../assurance/implementation-state-reconciliation.md`](../../assurance/implementation-state-reconciliation.md) | **The completed item-level inventory** — 166 rows, per-shim dispositions, six corrections, and the revised priority order. A versioned planning input, not work to be done |
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) | The target layout, project conventions and reference-direction rules that dispositions are measured against |
| [`../../architecture/00-architecture-overview.md`](../../architecture/00-architecture-overview.md) | The layering rules and the shared-foundation boundary |
| [WP-00](00-specification-naming-and-rights-freeze.md#rule-wp-00) output | The licence boundary declaration and naming freeze |
| The existing monorepo at `ede43db` | **166 projects**, 28 test-suite projects, 6 native shims, and the `eng/` build property set — measured, not estimated |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The inventory exists before restructuring begins** ([MG-04](../../architecture/01-solution-and-project-layout.md#rule-mg-04) in the solution layout; gate [PG-02](../../assurance/open-gates-register.md#rule-pg-02)) — **satisfied**: it was completed as design-stage evidence before this plan was derived. |
| BR-02 | **Dispositions are Keep · Rename · Move · Split · Merge · Rewrite · Fence · Delete** ([RM-03](../../assurance/implementation-state-reconciliation.md#rule-rm-03) in the reconciliation document). |
| BR-03 | Unmigrated conflicting code is fenced until its explicit disposition is executed; deletion needs a recorded reason ([RM-07](../../assurance/implementation-state-reconciliation.md#rule-rm-07) of the reconciliation evidence). Conforming projects cannot reference a fenced component. |
| BR-04 | A project spanning licence boundaries is split according to the item-level reconciliation and **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**; a broad exception cannot erase the boundary. |
| BR-05 | A project combining domain and adapter responsibilities is split under [PJ-01](../../architecture/01-solution-and-project-layout.md#rule-pj-01) of the solution layout, with its inventory disposition updated. |
| BR-06 | Names conflicting with the canonical glossary are reconciled under **[D-018](../../decisions/phase-1-foundation-decisions.md#rule-d-018)**, retaining migration compatibility only where explicitly specified. |
| BR-07 | **Deleting existing work requires an explicit disposition with a reason** ([RC-06](../../requirements/11-policy-and-configuration.md#rule-rc-06) there). |
| <a id="rule-br-08"></a>BR-08 | **No step leaves the repository unbuildable at a commit boundary** ([RC-07](../../requirements/11-policy-and-configuration.md#rule-rc-07) there). |
| <a id="rule-br-09"></a>BR-09 | **A commit either moves code or changes what it does, never both** ([RC-08](../../requirements/11-policy-and-configuration.md#rule-rc-08) there). |
| BR-10 | **Existing behaviour is evidence, not authority** ([RM-07](../../assurance/implementation-state-reconciliation.md#rule-rm-07) there). Where existing code disagrees with the specification, the specification governs. |
| BR-11 | Existing repository location is not evidence of original authorship. Newly introduced or inherited external material keeps the source, commit, licence, target, oracle and NOTICE provenance required by **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**. Original first-party work records that origin without inventing an external source. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| Every `.csproj` under `src/` and `tests/` | Receives a disposition; those Kept receive the boundary and convention properties |
| `src/Contracts/` | **Split** into a public Apache-2.0 set and an internal AGPL set (executed in `03`; the split decision is made here) |
| `src/DesktopHelpers/` | Disposition assigned against the shared-foundation boundary |
| `src/BuildingBlocks/ArcForges.Desktop.*` | Reviewed against the shared-foundation boundary; mechanism-only projects Kept, product-aware projects Split or Moved |
| `src/Cloud/Modules.*` | Map the 17 observed scaffold module names to the 20 declared domain owners in `21`; preserve the single Host with internal AgentRuntime/BackgroundJobs libraries and development-only AppHost |
| `native/` | Dispositions already assigned (`§5.2` there): four `Keep`, **two `Fence`** pending substitute analyses. All six are ABI skeletons of ~90–120 lines, not implementations |
| `tests/` | Each suite mapped to a required test family; gaps recorded |
| `fixtures/` | Created as an empty, documented root for golden fixtures |
| `eng/policy/reconciliation/` | The inventory exported as machine-readable data for the drift check |

**Major types introduced:** none.

---

## 5. Required implementation work

<a id="rule-wp-01.00"></a>

### WP-01.00 — Validate the completed inventory against current head

> **Design-stage prerequisite already complete.** The item-level inventory was produced during the Stage 2 repair, before the plan was derived (**[D-019](../../decisions/phase-1-foundation-decisions.md#rule-d-019)**), and is recorded in [`../../assurance/implementation-state-reconciliation.md`](../../assurance/implementation-state-reconciliation.md): 166 of 166 projects, 6 of 6 native shims, 28 test suites, with dispositions and six corrections to earlier false findings. It is bound to commit `ede43db`. **[PG-02](../../assurance/open-gates-register.md#rule-pg-02) is closed.** This sub-step does not re-create it.

**What must be fully done.** The inventory is re-validated against the repository's current head: projects added, removed or renamed since `ede43db` are identified, and each gains a disposition using the same vocabulary. The dispositions recorded in `§5` of that document are confirmed as still applicable, or amended with a reason.

**Testing requirements.** A drift comparison between the bound commit and current head, listing every added, removed and renamed project; a completeness check that every drifted item has a disposition.

**Completion gate.** Drift against `ede43db` is enumerated and every drifted item has a disposition. **[PG-02](../../assurance/open-gates-register.md#rule-pg-02) is not re-closed here** — it was closed by the design-stage evidence; this step keeps that evidence current.

<a id="rule-wp-01.01"></a>

### WP-01.01 — Implement the frozen contract split

**What must be fully done.** Every type in the existing contract projects is assigned to the public Apache-2.0 set or the internal AGPL set, using the enumerated Apache set from [WP-00.02](00-specification-naming-and-rights-freeze.md#rule-wp-00.02). Types that are currently public but should not be, and types that are currently internal but must be public for interoperability, are both identified. Apply the already selected package/schema licence split from the layout and wire registry; WP03 generates it.

**Testing requirements.** A review that every contract type has an assignment; a check that no type assigned to the public set transitively depends on an internal type.

**Completion gate.** The assignment is complete and dependency-consistent. **This is the highest-priority reconciliation item** (`§3` of the reconciliation document).

<a id="rule-wp-01.02"></a>

### WP-01.02 — Shared-foundation boundary review

**What must be fully done.** Every building-block project is classified as mechanism-only or product-aware. Mechanism-only projects are Kept. Product-aware content is moved into the owning product or split out. The shared-foundation boundary rules (`§7` of the architecture overview) are the criterion.

**Testing requirements.** A reference check that no building-block project references a product project; a review record for each reclassification.

**Completion gate.** No product knowledge remains in the shared foundation, and the reference check passes.

<a id="rule-wp-01.03"></a>

### WP-01.03 — Execute the native surface dispositions


**What must be fully done.** Retain the approved native foundations in DesktopPlatform; apply the selected vcpkg/official OTIO admission and MDF exclusion from the native registry. Migrate capability-specific managed wrappers into their DesktopPlatform packages; consume risky parsers only through the existing signed PlatformBroker isolation. Remove product copies only after exact source/NOTICE and package tests prove the transfer.

**Testing requirements.** Compare native source/import manifests and reference dispositions; reject direct MDF use, duplicate wrappers, cross-product source links and unadmitted native binaries.

**Completion gate.** Every retained native component has the selected package owner and admission state; no substitute selection is deferred to product integration.

<a id="rule-wp-01.04"></a>

### WP-01.04 — Test suite mapping

**What must be fully done.** Every existing test suite is mapped to one of the eighteen required families. Families with no home are recorded as gaps and assigned to the package that will create them. The repository-policy suite is identified as absent and scheduled for `05`.

**Testing requirements.** A coverage report: family → suite, with gaps explicit.

**Completion gate.** Every family has either an existing suite or a named future package.

<a id="rule-wp-01.05"></a>

### WP-01.05 — Execute the blocking moves and fence the rest


**What must be fully done.** Create the ten owner repositories with the fixed source/package mapping. The current implementation history becomes DesktopPlatform; migrate only licensed selected native/mechanism material, with explicit provenance. Other owners receive new application shells and released dependencies. Remove retired Notes canvas/slides scaffolds and obsolete monorepo source/solution references according to the existing disposition; preserve unrelated work and reference histories.

**Testing requirements.** Validate owner entry points and dependency-free shells in isolation; forbidden sibling ProjectReference/submodule/source import fixtures fail. Generated package-consuming builds occur after WP03 publication in WP06; verify retired scope remains absent.

**Completion gate.** The selected repository graph exists without changing accepted product behavior or importing old placeholders as implemented features.

<a id="rule-wp-01.90"></a>
### WP-01.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Implement the already selected source/package graph; reuse native foundations, assign product/Cloud/Web/Mobile/SDK/test/tool ownership, retain retired-project dispositions. Resolve native fences from the frozen admission record.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Complete old-group → target-owner/disposition mapping; independently buildable roots; no product domain copied into Platform, no forced suite, no blanket retention of six shipping shims.

**Completion gate.** Complete old-group → target-owner/disposition mapping; independently buildable roots; no product domain copied into Platform, no forced suite, no blanket retention of six shipping shims. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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
| The item-level inventory, 100 % coverage, approved | [WP-01.00](#rule-wp-01.00) |
| The contract type assignment, dependency-consistent | [WP-01.01](#rule-wp-01.01) |
| Shared-foundation reference check, clean | [WP-01.02](#rule-wp-01.02) |
| Native shim decision records, one per shim | [WP-01.03](#rule-wp-01.03) |
| Test family coverage report with explicit gaps | [WP-01.04](#rule-wp-01.04) |
| Green build at every commit boundary; retired Notes paths absent and fenced-reference check clean | [WP-01.05](#rule-wp-01.05) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-01.90](#rule-wp-01.90) and all inherited domain-specific gates must pass on the same candidate closure. Complete old-group → target-owner/disposition mapping; independently buildable roots; no product domain copied into Platform, no forced suite, no blanket retention of six shipping shims.

**All of the following, with recorded evidence:**

1. Drift against the inventory's bound commit `ede43db` is enumerated, and every drifted item carries a disposition. The inventory itself was completed as design-stage evidence and closed [PG-02](../../assurance/open-gates-register.md#rule-pg-02) before this package began.
2. Every contract type is assigned to a licence boundary, with no public type depending on an internal one.
3. No product knowledge remains in the shared foundation.
4. The two `Fence` shims are unreferenceable, and their substitute analyses are scheduled against named sub-steps.
5. Every required test family maps to an existing suite or a named future package.
6. The blocking moves and explicit deletion of `ArcNotes.Edgeless`/`ArcNotes.Slides` are executed, their obsolete solution/project/lock entries and excluded hooks are absent, the retained Notes core builds green, and all remaining non-`Keep` code is fenced and unreferenceable.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [00 specification naming and rights freeze](00-specification-naming-and-rights-freeze.md#rule-wp-00)

**Downstream — consumers of these released outputs.**

- [02 build governance and analyzer policy](02-build-governance-and-analyzer-policy.md#rule-wp-02)

---
