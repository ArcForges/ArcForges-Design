<a id="rule-wp-01"></a>

# WP-01 — Repository Reconciliation and Target Layout

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Reconcile the nine current repositories against the accepted ownership and licence boundaries. The historical ede43db inventory recorded **55 incorrectly licensed files**; verify current source before assigning a correction, move or retirement.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform and new owners. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** **Executing** the dispositions recorded in the completed inventory; validating it against current head; and the reconciliation moves that block downstream work — principally the contract licence-boundary correction and the fencing of unmigrated code.

**Out of scope.** Behaviour changes of any kind ([RC-08](../../requirements/11-policy-and-configuration.md#rule-rc-08) in the reconciliation document). Cloud module boundary changes that require schema decisions — those belong to `21`. Per-product project reorganisation beyond what the boundary split requires — those land inside each product's own package.

**Why this package exists.** The historical inventory identified licence and ownership defects. WP00 has since verified current first-party boundaries in nine independent repositories; its receipt does not complete contract type assignment or product behavior. WP01 records the actual remaining dispositions before restructuring. The mobile artifact gate (**[F-023](../../assurance/open-gates-register.md#rule-f-023)**) remains binding for its actual candidate.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../assurance/implementation-state-reconciliation.md`](../../assurance/implementation-state-reconciliation.md) | **The historical item-level inventory at ede43db** — 166 rows, per-shim dispositions, six corrections, and the revised priority order. A versioned planning input, not work to be done |
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) | The target layout, project conventions and reference-direction rules that dispositions are measured against |
| [`../../architecture/00-architecture-overview.md`](../../architecture/00-architecture-overview.md) | The layering rules and the shared-foundation boundary |
| [WP-00](00-specification-naming-and-rights-freeze.md#rule-wp-00) output | The licence boundary declaration and naming freeze |
| The existing monorepo at `ede43db` | **historical 166 projects at ede43db**, 28 test-suite projects, 6 native shims, and the `eng/` build property set — measured, not estimated |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) as amended by [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **The inventory exists before restructuring begins** ([MG-04](../../architecture/01-solution-and-project-layout.md#rule-mg-04) in the solution layout; gate [PG-02](../../assurance/open-gates-register.md#rule-pg-02)) — **satisfied**: it was completed as design-stage evidence before this plan was derived. |
| <a id="rule-br-02"></a>BR-02 | **Dispositions are Keep · Rename · Move · Split · Merge · Rewrite · Fence · Delete** ([RM-03](../../assurance/implementation-state-reconciliation.md#rule-rm-03) in the reconciliation document). |
| <a id="rule-br-03"></a>BR-03 | Unmigrated conflicting code is fenced until its explicit disposition is executed; deletion needs a recorded reason ([RM-07](../../assurance/implementation-state-reconciliation.md#rule-rm-07) of the reconciliation evidence). Conforming projects cannot reference a fenced component. |
| <a id="rule-br-04"></a>BR-04 | A project spanning licence boundaries is split according to the item-level reconciliation and **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**; a broad exception cannot erase the boundary. |
| <a id="rule-br-05"></a>BR-05 | A project combining domain and adapter responsibilities is split under [PJ-01](../../architecture/01-solution-and-project-layout.md#rule-pj-01) of the solution layout, with its inventory disposition updated. |
| <a id="rule-br-06"></a>BR-06 | Names conflicting with the canonical glossary are reconciled under **[D-018](../../decisions/phase-1-foundation-decisions.md#rule-d-018)**, retaining migration compatibility only where explicitly specified. |
| <a id="rule-br-07"></a>BR-07 | **Deleting existing work requires an explicit disposition with a reason** ([RC-06](../../requirements/11-policy-and-configuration.md#rule-rc-06) there). |
| <a id="rule-br-08"></a>BR-08 | **No step leaves the repository unbuildable at a commit boundary** ([RC-07](../../requirements/11-policy-and-configuration.md#rule-rc-07) there). |
| <a id="rule-br-09"></a>BR-09 | **A commit either moves code or changes what it does, never both** ([RC-08](../../requirements/11-policy-and-configuration.md#rule-rc-08) there). |
| <a id="rule-br-10"></a>BR-10 | **Existing behaviour is evidence, not authority** ([RM-07](../../assurance/implementation-state-reconciliation.md#rule-rm-07) there). Where existing code disagrees with the specification, the specification governs. |
| <a id="rule-br-11"></a>BR-11 | Existing repository location is not evidence of original authorship. Newly introduced or inherited external material keeps the source, commit, licence, target, oracle and NOTICE provenance required by **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**. Original first-party work records that origin without inventing an external source. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| Every `.csproj` under `src/` and `tests/` | Receives a disposition; those Kept receive the boundary and convention properties |
| `src/Contracts/` | **Split** into a public Apache-2.0 set and an internal Apache-2.0 set with restricted imports (executed in `03`; the split decision is made here) |
| `src/DesktopHelpers/` | Disposition assigned against the shared-foundation boundary |
| `src/BuildingBlocks/ArcForges.Desktop.*` | Reviewed against the shared-foundation boundary; mechanism-only projects Kept, product-aware projects Split or Moved |
| `src/Cloud/Modules.*` | Map the 17 historical scaffold names to the 21 declared domain owners in `21`; Cloud owns the Native AOT Container host and Worker bindings, while AI owns the sole Workflow Harness. Retired AppHost/AgentRuntime scaffolds are not requirements |
| `native/` | Apply the current WP01.03 admission: retain admitted native mechanisms in DesktopPlatform, use the pinned official OTIO adapter, exclude MDF; old skeletons are not product implementation evidence |
| `tests/` | Each suite mapped to a required test family; gaps recorded |
| `fixtures/` | Owned by each producing repository; create with substantive golden fixtures when its producing step requires them, never as an empty placeholder |
| `eng/policy/reconciliation/` | The inventory exported as machine-readable data for the drift check |

**Major types introduced:** none.

---

## 5. Required implementation work

<a id="rule-wp-01.00"></a>

### WP-01.00 — Verify nine independent current repositories

**What must be fully done.** Record actual clean commit/worktree states for DesktopPlatform, Contracts, Cloud, AI, Web, Mobile, ArcNotes, ArcScope and ArcSlate. Inventory existing Hello World/build/publish artifacts against arch 27 and the package registry. Earlier ede43db monorepo inventories are historical provenance, not current source inventory.

**Testing requirements.** Compare each owned path/project to current Git tree and published artifact identity; reject adjacent-source/submodule integration.

**Completion gate.** Every planned directory has one repository owner and explicit keep/move/retire disposition; no source mutation is justified solely by a dated baseline. Follow the [current inventory profile](../../assurance/wp01-00-inventory-policy.md) for the versioned data, historical drift, artifact and enforcement boundaries.

**Recorded execution (2026-09-20).** [WP01.00 evidence](../../assurance/wp01-00-implementation-evidence.md) records nine current owners, 75 build projects, all 166 historical projects, 359 planned/current directory dispositions, Windows/Linux drift gates, reviewed merges and the verified public candidate. This closes only WP01.00.

<a id="rule-wp-01.01"></a>

### WP-01.01 — Implement the frozen contract split

**What must be fully done.** Every type in the existing contract projects is assigned to the public Apache-2.0 set or the internal Apache-2.0 set with restricted imports, using the enumerated Apache set from [WP-00.02](00-specification-naming-and-rights-freeze.md#rule-wp-00.02). Types that are currently public but should not be, and types that are currently internal but must be public for interoperability, are both identified. Apply the already selected package/schema licence split from the layout and wire registry; WP03 generates it.

**Testing requirements.** A review that every contract type has an assignment; a check that no type assigned to the public set transitively depends on an internal type.

**Completion gate.** The assignment is complete and dependency-consistent. **This is the highest-priority reconciliation item** (`§3` of the reconciliation document). Use the [current contract access profile](../../assurance/wp01-01-contract-access-policy.md); both sets are Apache-2.0, and retired monorepo DTOs do not become current source.

**Recorded execution (2026-09-20).** [WP01.01 evidence](../../assurance/wp01-01-implementation-evidence.md) records complete current type assignment, compiled dependency rejection, reviewed CI-green merge, isolated Linux/Windows consumers and verified public NuGet/npm/Maven candidate `1.0.0-ci.60.1`. This closes only WP01.01.

<a id="rule-wp-01.02"></a>

### WP-01.02 — Shared-foundation boundary review

**What must be fully done.** Every building-block project is classified as mechanism-only or product-aware. Mechanism-only projects are Kept. Product-aware content is moved into the owning product or split out. The [shared-foundation boundary rules](../../architecture/00-architecture-overview.md#6-shared-foundation-boundary) are the criterion.

**Testing requirements.** A reference check that no building-block project references a product project; a review record for each reclassification.

**Completion gate.** No product knowledge remains in the shared foundation, and the reference check passes.

**Recorded execution (2026-09-20).** [WP01.02 review](../../assurance/wp01-02-foundation-review.md) classifies all 11 current BuildingBlocks projects as mechanism-only, confirms current Keep dispositions, and records actual evaluated reference checks, locked restore, Release build and architecture tests. This closes current content/reference review only; future mechanism implementation remains with its scheduled producer.

<a id="rule-wp-01.03"></a>

### WP-01.03 — Execute the native surface dispositions


**What must be fully done.** Retain the approved native foundations in DesktopPlatform; apply the selected vcpkg/official OTIO admission and MDF exclusion from the native registry. Migrate capability-specific managed wrappers into their DesktopPlatform packages; consume risky parsers only through the ContentSandbox/Broker isolation required by [architecture 24](../../architecture/24-content-and-extension-isolation.md). WP11 supplies the restricted helper and WP13 composes production parsers; WP01 must not introduce an uncontained parser or claim that the current Hello helper is a signed sandbox. Remove product copies only after exact source/NOTICE and package tests prove the transfer.

**Testing requirements.** Compare native source/import manifests and reference dispositions; reject direct MDF use, duplicate wrappers, cross-product source links and unadmitted native binaries.

**Completion gate.** Every retained native component has the selected package owner and admission state; no substitute selection is deferred to product integration.

**Current execution profile.** [Native reconciliation](../../assurance/wp01-03-native-reconciliation-policy.md) separates existing ABI probes and package admission from the already scheduled functional parser/helper producers. Independent test-oracle bindings stay in tests; production bindings have one capability owner.

**Recorded execution (2026-09-20).** [Native reconciliation evidence](../../assurance/wp01-03-native-reconciliation.md) closes the current dispositions: test-only oracle relocation, single production binding ownership, selected native admissions and product-copy audit. The reviewed implementation passed all PR and post-merge gates, local independent JIT/AOT/C17 consumers and public payload comparison for all ten `1.0.0-ci.17.1` packages. Functional parser/helper acceptance remains with its named producers.

<a id="rule-wp-01.04"></a>

### WP-01.04 — Test suite mapping

**What must be fully done.** Every existing test suite is mapped to one of the eighteen required families. Families with no home are recorded as gaps and assigned to the package that will create them. Existing repository-policy checks are inventoried with their actual coverage; the full AT/RP rule set and invariant-enforcement accounting remain scheduled for `05`. Historical scaffold names and old test counts are not current coverage.

**Testing requirements.** A coverage report: family → suite, with gaps explicit.

**Completion gate.** Every family has either an existing suite or a named future package.

**Recorded execution (2026-09-20).** [Test-family mapping](../../assurance/wp01-04-test-family-map.md) assigns all discovered current test sources/verification entrypoints and 28 historical test projects. All eighteen families have current bounded coverage or an explicit gap and named future producer; ten families are partial and eight have no current suite. This closes mapping only, not their implementation or release acceptance.

<a id="rule-wp-01.05"></a>

### WP-01.05 — Apply bounded repository reconciliation

**What must be fully done.** Implement only inventory-backed owner moves and names in the nine repositories; replace legacy ArcChat host/Harness or product RPC scaffolds with the arch 27 composition boundaries. Preserve working builds while each consumer adopts immutable package artifacts.

**Testing requirements.** Clean-checkout builds with no sibling source; verify licenses and package closure.

**Completion gate.** Current repository/project map agrees with actual owned trees and every move has a tested consumer path.

**Recorded execution (2026-09-20).** [Bounded reconciliation evidence](../../assurance/wp01-05-bounded-reconciliation.md) verifies all nine current owners, 75 projects and 359 directory dispositions, clean exact-head CI, licence/runtime/reference checks and a new clean-worktree Notes build with 89 passing tests. Retired blocking paths are already absent; no additional source move or deletion is needed. Future producer moves and explicitly retained bootstrap compatibility remain scheduled.

<a id="rule-wp-01.90"></a>
### WP-01.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Implement the already selected source/package graph; reuse native foundations, assign product/Cloud/Web/Mobile/SDK/test/tool ownership, retain retired-project dispositions. Resolve native fences from the frozen admission record.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Complete old-group → target-owner/disposition mapping; independently buildable roots; no product domain copied into Platform, no forced suite, no blanket retention of six shipping shims.

**Completion gate.** Complete old-group → target-owner/disposition mapping; independently buildable roots; no product domain copied into Platform, no forced suite, no blanket retention of six shipping shims. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

**Recorded execution (2026-09-20).** [WP01 stage acceptance](../../assurance/wp01-stage-acceptance.md) joins all six completed substeps to the nine current exact source/candidate identities, verifies all 166 historical project mappings, and re-downloads and hashes 33 Platform/Contracts public files. Current owner/build/licence gates pass; actual runtime evidence retains its original scenarios and dates. This closes the reconciliation stage only; named later producers remain required.

---

**Cloud module layout acceptance.** WP01 records all 21 domain owners listed in architecture01 §5 and their Cloud ownership. [WP21.02](21-cloud-host-and-persistence.md#rule-wp-21.02) implements their substantive Domain/Application/Infrastructure projects and compares the project list to the model01 schema map, including PackageCatalog. Platform remains shared infrastructure. Do not create empty module projects during reconciliation; this follows the schema-boundary exclusion in §1 and preserves the full 21-module acceptance at its producing step. The count is distinct from the nine independent implementation repositories.

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
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-01.90](#rule-wp-01.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-01.90](#rule-wp-01.90) and all inherited domain-specific gates must pass on the same candidate closure. Complete old-group → target-owner/disposition mapping; independently buildable roots; no product domain copied into Platform, no forced suite, no blanket retention of six shipping shims.

**All of the following, with recorded evidence:**

1. Drift against the inventory's bound commit `ede43db` is enumerated, and every drifted item carries a disposition. The inventory itself was completed as design-stage evidence and closed [PG-02](../../assurance/open-gates-register.md#rule-pg-02) before this package began.
2. Every contract type is assigned to a licence boundary, with no public type depending on an internal one.
3. No product knowledge remains in the shared foundation.
4. Current native admissions are applied: official OTIO is the selected interchange boundary, MDF is excluded, and unmigrated conflicting skeletons are unreferenceable; no pending substitute choice overrides WP01.03.
5. Every required test family maps to an existing suite or a named future package.
6. The blocking moves and explicit deletion of `ArcNotes.Edgeless`/`ArcNotes.Slides` are executed, their obsolete solution/project/lock entries and excluded hooks are absent, the retained Notes core builds green, and all remaining conflicting code whose disposition is due at this stage is fenced and unreferenceable. Explicit bootstrap compatibility retained until a named later producer, including the Kotlin native-grpc client until the first business release in WP03, is not prematurely removed.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [GOV.02](../delivery/lanes/governance.md#task-gov-02) | [WP-01.00](01-repository-reconciliation-and-target-layout.md#rule-wp-01.00) (full)<br>[WP-01.01](01-repository-reconciliation-and-target-layout.md#rule-wp-01.01) (full)<br>[WP-01.02](01-repository-reconciliation-and-target-layout.md#rule-wp-01.02) (full)<br>[WP-01.03](01-repository-reconciliation-and-target-layout.md#rule-wp-01.03) (full)<br>[WP-01.04](01-repository-reconciliation-and-target-layout.md#rule-wp-01.04) (full)<br>[WP-01.05](01-repository-reconciliation-and-target-layout.md#rule-wp-01.05) (full)<br>[WP-01.90](01-repository-reconciliation-and-target-layout.md#rule-wp-01.90) (full)<br>[WP-01](01-repository-reconciliation-and-target-layout.md#rule-wp-01) Cloud module layout acceptance - map 17 historical scaffold names to the 21 declared domain owners in WP21; Cloud owns the Native AOT Container host and Worker bindings, AI owns the sole Workflow Harness; empty module projects are not created during reconciliation (package-level obligation contribution) | [GOV.01](../delivery/lanes/governance.md#task-gov-01) (artifact) |

**Consumers outside this package:** [GOV.03](../delivery/lanes/governance.md#task-gov-03).

<!-- delivery-graph:end -->

## Current source baseline and migration input

The 166-project ede43db monorepo inventory is historical disposition evidence, not the current checkout shape. [Family completion review](../../assurance/family-design-completion-review.md) records the separate DesktopPlatform/Contracts/Mobile bootstrap evidence and scope. Before coding, verify each actual source HEAD/dirty state and map only retained required mechanisms to its owning repository/package; preserve existing published Hello/probe compatibility and Mobile app/signing/version identity. Do not recreate deleted scaffolds, copy every legacy project, or treat unpublished implementation as missing design. Generated protocol artifacts follow the tracked authored-schema/generator baseline and immutable producer manifest from WP03; generated outputs are not categorically forbidden from version control.
