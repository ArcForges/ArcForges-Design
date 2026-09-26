<a id="rule-wp-00"></a>

# WP-00 — Specification, Naming and Rights Freeze

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Make the vocabulary, the product set, the licence position and the reuse process *settled facts* before any code is written against them. This is the first hard gate: if naming, terminology, licence boundaries or product scope move later, editors, data formats, capabilities and cloud sync all rework.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: All repositories; Design authority. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Establishing in the implementation repository the enforceable form of decisions already taken in Phase 1: the product baseline, the normative glossary and invariant catalogue, the licence boundary declaration, the reuse and provenance process, the reference audit method, and the terminology enforcement mechanism.

**Out of scope.** Any product feature. Any architectural decision — those are made; this package records and enforces them. **Producing any Reference Coverage Matrix or the reconciliation inventory** — both were completed as design-stage evidence before the plan was derived (**[D-019](../../decisions/phase-1-foundation-decisions.md#rule-d-019)**), and this package consumes them.

**Why this package exists.** Every later package cites terms, boundaries and identifiers from this one. A term that means two things, a project on the wrong side of a licence boundary, or a reused file with no provenance record are all defects that become exponentially more expensive after code exists.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../decisions/phase-1-foundation-decisions.md`](../../decisions/phase-1-foundation-decisions.md) | [D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001) … [D-023](../../decisions/phase-1-foundation-decisions.md#rule-d-023) are binding and are not reopened here |
| [`../../requirements/00-product-scope-and-portfolio.md`](../../requirements/00-product-scope-and-portfolio.md) | The three desktop products, companion identity and assistant feature boundary, the technology constitution and the closed exception list |
| [`../../requirements/01-normative-glossary-and-invariants.md`](../../requirements/01-normative-glossary-and-invariants.md) | The glossary and invariant catalogue this package makes enforceable |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The matrix method, the ten-field provenance record and the licence decision table |
| [`../../assurance/reference-coverage/`](../../assurance/reference-coverage/README.md) | **The five completed matrices** — versioned planning inputs, not work to be done |
| [`../../assurance/invariant-coverage.md`](../../assurance/invariant-coverage.md) | **The completed invariant accounting and item-level mapping** — **429** rows |
| [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md) | The gates this package opens and schedules |
| The existing monorepo's `NOTICE.md`, `LICENSE` and package declarations | The current licence position that must be verified rather than assumed |
| Upstream work packages | **None.** This is the first package. |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **The desktop product baseline is exactly ArcNotes, ArcScope and ArcSlate** under **[P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)** and **[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013)**. ArcChat names the embedded assistant/companion feature; it is not a fourth executable or product ID. The fourth allowed wire ProductId, `companion`, belongs to Android/Web. `ArcCanvas`, `ArcMusic`, `ArcImage` and `ArcVideo` are superseded and must never appear as current products. |
| <a id="rule-br-02"></a>BR-02 | **`ArcVideo` and `ArcVideoFoundation` remain valid only as the names of existing reference repositories** (**[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**), never as products. |
| <a id="rule-br-03"></a>BR-03 | **Paddle is the sole customer-facing Merchant of Record; Payoneer is a payout destination only** (**[D-005](../../decisions/phase-1-foundation-decisions.md#rule-d-005)**). The superseded provider name never appears. |
| <a id="rule-br-04"></a>BR-04 | **One canonical definition per shared family term; product-specific meanings are namespaced** (**[D-018](../../decisions/phase-1-foundation-decisions.md#rule-d-018)**). |
| <a id="rule-br-05"></a>BR-05 | **Every accepted `X ≠ Y` invariant is preserved** (**[D-018](../../decisions/phase-1-foundation-decisions.md#rule-d-018)**) and becomes enforceable. |
| <a id="rule-br-06"></a>BR-06 | **Two licence boundaries exist**: Apache-2.0 for the interoperability boundary, AGPL-3.0-only for everything else (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| <a id="rule-br-07"></a>BR-07 | **No App Store exception, dual licensing, proprietary grant or CLA** (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**). DCO continues with inbound-equals-outbound per scope. |
| <a id="rule-br-08"></a>BR-08 | **Copy First is licence-gated and provenance-gated** (**[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**). Unconditional copying is rejected. |
| <a id="rule-br-09"></a>BR-09 | **A repository-root licence must not be assumed to cover every file** (**[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**). |
| <a id="rule-br-10"></a>BR-10 | **The technical exception list is closed** (`§8.1` of the scope requirements). Adding to it requires a formal decision. |
| <a id="rule-br-11"></a>BR-11 | **The ArcChat AOT position is settled**: the owning desktop application is a Native AOT deliverable like the other desktop products (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**). Any residual corpus text suggesting otherwise is stale. |
| <a id="rule-br-12"></a>BR-12 | **ArcNotes scope is the notebook core, bounded typed properties, saved list/table views, references and cloud sync** (**[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** as amended by **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)**, 2026-09-06). Edgeless, slides and further database layouts are **excluded from delivery**, with no mandatory future hook. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `Contracts/eng/policy/product-names.json` | WP00.00: single interoperable naming authority and forbidden-name data; other WP00 policy owners follow their substeps |
| `eng/policy/` | Created in each assigned owner: glossary, banned-symbol and licence policy data |
| `DesktopPlatform/eng/policy/glossary-terms.json`, `invariants.json` | Generated canonical vocabulary and invariant mapping, with exact Design source identity |
| `NOTICE.md` | Verified and regenerated from the provenance records that exist |
| `LICENSE`, per-project SPDX declarations | Verified; every project declares its SPDX identifier and its boundary |
| `Directory.Build.props` | Gains the boundary property that every project must set |
| `docs/` in the implementation repository | Reduced to implementation-facing notes; design authority stays in this repository (**[D-017](../../decisions/phase-1-foundation-decisions.md#rule-d-017)**) |
| `tests/RepositoryPolicyTests/` | Created (implemented in `05`; the policy data lands here) |
| `DesktopPlatform/eng/policy/reference-baselines.json` | Five matrix registrations, exact Design identities and reference-source identities under the [registration profile](../../assurance/reference-baseline-registration.md) |
| Provenance record store | Created: the location and naming convention for the ten-field records |

**Major types introduced:** none — this package produces policy data, declarations and process artifacts, not runtime types.

---

## 5. Required implementation work

<a id="rule-wp-00.00"></a>

### WP-00.00 — Product and naming freeze

**What must be fully done.** Contracts owns the single machine-readable `eng/policy/product-names.json`, following the [naming policy](../../architecture/28-product-naming-policy.md). List the three desktop products, the `companion` wire identity and the separately owned `assistant` feature, with canonical IDs, display names, reserved namespaces and file-association identifiers (explicitly empty where no native format is owned). Record superseded names as forbidden, the narrow reference-repository exception ([BR-02](#rule-br-02)), and historical dispositions without creating runtime aliases. Preserve observed package/application identities and the already scheduled WP30 Android prerelease migration.

**Testing requirements.** Run the Contracts-owned scanner over Git-tracked paths and file contents in all nine implementation repositories, including generated source, configuration, resource strings and implementation documentation. Include non-ignored new files during local validation. Validate the naming policy itself as closed-schema enforcement data, not an arbitrary excluded file. Only exact, hash-bound provenance records may admit the two reference-repository names; no directory-wide, source-code or historical-document exemptions. Test mixed case, identifier substrings, UTF-16 resources, forbidden paths, policy tampering, missing files and invalid/stale exceptions. Record each repository commit and working-tree state. Contracts CI runs the scanner and its negative tests; family-wide automatic build enforcement remains WP02/WP05, without postponing the current nine-repository scan.

**Completion gate.** The scan runs clean, and the exception list is reviewed and minimal.

<a id="rule-wp-00.01"></a>

### WP-00.01 — Glossary and invariant enforcement data

> **Design-stage prerequisite already complete.** The item-level mapping is recorded in [`../../assurance/invariant-coverage.md`](../../assurance/invariant-coverage.md): **429** current catalogue rows — 421 plus the 8 [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) added — each with an architecture home, an enforcement mechanism, a planned verification and an owning gate. **[PG-06](../../assurance/open-gates-register.md#rule-pg-06) is closed.** This sub-step consumes the current catalogue and mapping; it does not repeat the completed historical input extraction.

**What must be fully done.** DesktopPlatform owns the exporter, generated AGPL policy data and continuing checks under the [design policy export profile](../../architecture/29-design-policy-export.md). The completed catalogue and its mapping are exported into machine-readable policy data the build can read: canonical terms with their term space (domain, wire, UI, storage, commercial), product namespacing, forbidden aliases, and every invariant with its identifier, its assigned mechanism and its owning package.

**And the identifier index** ([PG-21](../../assurance/open-gates-register.md#rule-pg-21), [SV-01](../../assurance/testing-and-verification-strategy.md#rule-sv-01)): regenerate the defining-document and stable-anchor index and check all active citations. The design repair already closes the current corpus; this step verifies drift and installs the continuing check. Same-spelled rules in different documents must remain distinguishable ([OG-05](../../assurance/open-gates-register.md#rule-og-05)).

**Testing requirements.** Compare both forward dependency tables, every WP header/section 9 and the exact reverse transpose; validate the explicit topological schedule and current counts. Require unique top-level section numbers, resolvable links/anchors and one .90 evidence row per active WP. Historical review fixtures are scoped separately. A round-trip consistency check that the exported data matches [`../../requirements/01-normative-glossary-and-invariants.md`](../../requirements/01-normative-glossary-and-invariants.md) and `§7` of the coverage document exactly, in both directions — no term or invariant present in one and absent from the other. **A resolver run over every citation in `docs/`**, reporting each one's defining document and failing on a citation that resolves to zero definitions, or to several with no named home; the earlier **1,597 ambiguous citations** are historical evidence, not the current denominator. Recompute every current occurrence and work defects to zero or an individually recorded classification with a reason.

**Completion gate.** The exported policy data matches both source documents exactly, **and every citation in `docs/` resolves to exactly one definition or carries a recorded waiver** ([PG-21](../../assurance/open-gates-register.md#rule-pg-21)). **This does not close [PG-06](../../assurance/open-gates-register.md#rule-pg-06), which is already closed by design evidence, and it does not close [PG-11](../../assurance/open-gates-register.md#rule-pg-11), which requires implemented, passing checks.**

<a id="rule-wp-00.02"></a>

### WP-00.02 — Licence boundary declaration

**What must be fully done.** Every project declares its SPDX identifier and its licence boundary as a build property. The Apache-2.0 set includes all Contracts public/internal schemas/tools/generators/fixtures/SDK/CLI under [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010) and public protocol specifications, wire schemas, DTOs, public clients, contract-level validators, the public SDK, mobile-only libraries and Android companion. Everything else is AGPL-3.0-only. The boundary is expressed as data that a policy test can read.

**Testing requirements.** A check that every project declares a boundary; a check that the declared boundary matches the enumerated set; a reference-direction check that no AGPL project is referenced from an Apache project. Apply the [project declaration and verification profile](../../architecture/01-solution-and-project-layout.md#41-project-declaration-and-verification-profile) across .NET, npm, Gradle and native/IDE projects, including current candidate licence gates.

**Completion gate.** Every project declares a boundary, and the reference-direction check passes. **This is a precondition for `03`.**

<a id="rule-wp-00.03"></a>

### WP-00.03 — Reuse and provenance process

**What must be fully done.** The provenance record template implementing the ten fields of **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)** exists, with a storage location, a naming convention and a review step. The licence decision table is encoded as policy data. The process states who may approve a disposition, and what happens on discovery of a conflicting contribution — registered and returned for decision, never silently excepted ([BR-07](#rule-br-07)).

Apply the [current-repository implementation profile](../../assurance/reference-coverage-and-provenance.md#31-current-repository-implementation-profile) and [review responsibilities](../../assurance/reference-coverage-and-provenance.md#43-review-responsibility-and-conflicts) in all nine owners. The initial audit reconciles existing wrappers, generated material, patches and retained notices with explicit source evidence; the completed reference matrices' absence of proposed reuse does not exempt those files. Preserve historical records and existing artifact notice/closure gates.

Include [material introduced only during packaging](../../assurance/reference-coverage-and-provenance.md#32-material-introduced-only-during-packaging). A clean tracked-file inventory cannot waive provenance for copied documentation/frontend resources in an actual distributable; verify the owning candidate and every affected companion archive.

For the existing native packages, apply the [native closure profile](../../assurance/reference-coverage-and-provenance.md#33-existing-native-distribution-closure) and the separately scoped [Windows compiler-runtime record](../../assurance/reference-coverage-and-provenance.md#34-existing-windows-compiler-runtime-redistributable). Retain source-reuse boundaries, exact corresponding source and full applicable notices; a vendor binary without public source must not be assigned a fictitious Git identity.

**Testing requirements.** A check that every file identified as externally originated has a provenance record; a check that no record is missing a required field.

**Completion gate.** The process exists, the template is in use for at least one real record, and the checks run in CI.

**Recorded execution.** The [2026-09-19 implementation receipt](../../assurance/wp00-03-implementation-evidence.md) binds all nine owners to their reviewed merged revisions, published artifacts and required runtime evidence. It closes this substep for those revisions, without starting its siblings or satisfying later commercial gates.

<a id="rule-wp-00.04"></a>

### WP-00.04 — Register the completed reference matrices as versioned planning inputs

> **Design-stage prerequisite already complete.** All five Reference Coverage Matrices were produced during the Stage 2 repair, before the plan was derived, as **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)** and **[D-019](../../decisions/phase-1-foundation-decisions.md#rule-d-019)** require. They are in [`../../assurance/reference-coverage/`](../../assurance/reference-coverage/README.md): ArcChat/AionUi (30 rows), ArcNotes/AFFiNE+SiYuan (41), ArcScope/Serial-Studio (31), ArcSlate/ArcVideo+ArcVideoFoundation (31), distribution/StartArcForges (12). **[PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) are closed** for the five accessible references. **This sub-step does not create a matrix.**

**What must be fully done.** Each matrix is registered as a **versioned planning input** under the [registration profile](../../assurance/reference-baseline-registration.md), with its exact Design document identity and bound source identity, so downstream packages consume a fixed baseline rather than re-reading a moving reference. The drift-check procedure is defined: what is compared against the recorded commit, what counts as newly introduced material, and who assesses it.

**Testing requirements.** A registration check that all five matrices match their pinned Design documents, all six Git reference commits resolve in the registered repositories, and the non-Git packaged reference matches its observed-version and permitted-evidence registration; a real dry run of the drift check against one reference, plus rejection tests for changed or incomplete registrations.

**Completion gate.** All five matrices are registered with verified bound identities (six resolvable Git commits and the non-Git packaged observation), and the drift-check procedure is defined and exercised once. **No unresolved determination is carried forward** — the one that existed, [OC-01](../../assurance/open-gates-register.md#rule-oc-01), was closed by user decision on 2026-09-05 ([P2-005](../../decisions/phase-2-specification-decisions.md#rule-p2-005)), which amended **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)**'s ArcSlate reference line to ArcVideo and ArcVideoFoundation ([`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md) `§6`).

**Recorded execution.** [Implementation and post-merge evidence](../../assurance/wp00-04-implementation-evidence.md) records the reviewed changes, immutable source identities, exercised drift procedure and verified automatic publications.

<a id="rule-wp-00.05"></a>

### WP-00.05 — Stale-claim reconciliation


**What must be fully done.** Apply the current naming/scope/runtime authority to implementation repository manifests and policies: three professional desktop AOT products with embedded assistants, Native AOT Cloud, React Web, Kotlin/Jetpack Compose Mobile and CF-only Harness. Record the nine implementation repository owners and retired implementation scaffold dispositions under the [runtime and ownership profile](../../architecture/30-runtime-and-source-ownership-policy.md); Design remains the separate documentation authority. Historical evidence stays bound to its observed date/revision and cannot override the accepted design.

**Testing requirements.** Repository-policy checks reject superseded product/provider names outside registered reference provenance, old runtime configuration and unassigned source ownership. Verify actual current roots, structured build/runtime inputs and negative fixtures using the profile; preserve the current package examples and explicitly assigned later migrations.

**Completion gate.** Implementation policy data matches current formal decisions; no new scope or architecture decision is delegated to downstream packages.

**Recorded execution.** [Implementation and post-merge evidence](../../assurance/wp00-05-implementation-evidence.md) binds the current nine-owner policy, reviewed claim corrections, actual source/build checks, public packages and real Cloud/AI deployment results. Later product gates retain their assigned owners.

<a id="rule-wp-00.90"></a>
### WP-00.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Enforce the nine-repository, proto, AOT, Android, CF/R2 amendment. Carry licence boundaries and current product exclusions. Reconcile old implementation instructions as historical inputs; preserve the design-repair baseline.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** A named authority/licence/runtime/ownership table, with each repository's instructions derived from the revised design. No archived-input or old implementation document becomes authority.

**Completion gate.** A named authority/licence/runtime/ownership table, with each repository's instructions derived from the revised design. No archived-input or old implementation document becomes authority. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

**Recorded execution.** [WP00 stage acceptance](../../assurance/wp00-stage-acceptance.md) and its [exact closure receipt](../../assurance/wp00-stage-acceptance.json) verify the six preceding substeps, all nine instruction/owner/licence/runtime assignments, source policies, fixed candidates and actual evidence limits. This closes the WP00 stage; later product and commercial gates remain with their named owners.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None |
| Protocol | None directly; establishes the vocabulary every later contract uses |
| UI | Establishes the canonical display names and reserved identifiers |
| Security | Establishes the licence boundary that later prevents incompatible material entering the mobile and public-client surfaces |
| Platform | None |
| Migration | None |
| Compatibility | Establishes the naming and namespacing that later compatibility rules depend on |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Forbidden-term scan report, clean | [WP-00.00](#rule-wp-00.00), [WP-00.05](#rule-wp-00.05) |
| Glossary and invariant policy data, consistency-checked | [WP-00.01](#rule-wp-00.01) |
| Licence boundary declaration report, every project covered | [WP-00.02](#rule-wp-00.02) |
| Provenance record set with a completeness check | [WP-00.03](#rule-wp-00.03) |
| Five versioned matrix registrations, source-resolution evidence and one exercised drift report | [WP-00.04](#rule-wp-00.04) |
| A review record for every corrected stale claim | [WP-00.05](#rule-wp-00.05) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-00.90](#rule-wp-00.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-00.90](#rule-wp-00.90) and all inherited domain-specific gates must pass on the same candidate closure. A named authority/licence/runtime/ownership table, with each repository's instructions derived from the revised design. No archived-input or old implementation document becomes authority.

**[PG-21](../../assurance/open-gates-register.md#rule-pg-21) evidence:** [WP-00.01](#rule-wp-00.01) — Current corpus paths/anchors and document-scoped semantic citation check; subsequent normative edits repeat the check. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. The three desktop products, companion identity, assistant feature boundary and forbidden-name set are recorded in the single naming authority; the nine-repository scan runs clean.
2. The glossary and invariant catalogue exist as machine-readable policy data, consistent with the glossary document, with an enforcement mechanism assigned to every invariant.
3. Every project declares an SPDX identifier and a licence boundary, and the reference-direction check passes.
4. The provenance process exists, is encoded as policy data, and is in use for at least one real record.
5. All five completed Reference Coverage Matrices are registered as versioned planning inputs under the [registration profile](../../assurance/reference-baseline-registration.md), with six resolvable Git commits and the non-Git packaged observation, and the drift-check procedure is defined and exercised once. [PG-01](../../assurance/open-gates-register.md#rule-pg-01) and [F-013](../../assurance/open-gates-register.md#rule-f-013) were closed by the design-stage evidence itself, not by this package.
6. No stale runtime, licence or scope claim remains in the implementation repository.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [GOV.01](../delivery/lanes/governance.md#task-gov-01) | [WP-00.00](00-specification-naming-and-rights-freeze.md#rule-wp-00.00) (full)<br>[WP-00.01](00-specification-naming-and-rights-freeze.md#rule-wp-00.01) (full)<br>[WP-00.02](00-specification-naming-and-rights-freeze.md#rule-wp-00.02) (full)<br>[WP-00.03](00-specification-naming-and-rights-freeze.md#rule-wp-00.03) (full)<br>[WP-00.04](00-specification-naming-and-rights-freeze.md#rule-wp-00.04) (full)<br>[WP-00.05](00-specification-naming-and-rights-freeze.md#rule-wp-00.05) (full)<br>[WP-00.90](00-specification-naming-and-rights-freeze.md#rule-wp-00.90) (full) | none |

**Consumers outside this package:** [GOV.02](../delivery/lanes/governance.md#task-gov-02), [GOV.04](../delivery/lanes/governance.md#task-gov-04), [GOV.11](../delivery/lanes/governance.md#task-gov-11), [GOV.14](../delivery/lanes/governance.md#task-gov-14).

<!-- delivery-graph:end -->

## Current source baseline and migration input

The 166-project ede43db monorepo inventory is historical disposition evidence, not the current checkout shape. [Family completion review](../../assurance/family-design-completion-review.md) records the separate DesktopPlatform/Contracts/Mobile bootstrap evidence and scope. Before coding, verify each actual source HEAD/dirty state and map only retained required mechanisms to its owning repository/package; preserve existing published Hello/probe compatibility and Mobile app/signing/version identity. Do not recreate deleted scaffolds, copy every legacy project, or treat unpublished implementation as missing design. Generated protocol artifacts follow the tracked authored-schema/generator baseline and immutable producer manifest from WP03; generated outputs are not categorically forbidden from version control.
