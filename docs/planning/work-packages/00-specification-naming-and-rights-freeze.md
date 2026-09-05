# WP-00 — Specification, Naming and Rights Freeze

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: — · Downstream: `01`, `47`

> **Goal.** Make the vocabulary, the product set, the licence position and the reuse process *settled facts* before any code is written against them. This is the first hard gate: if naming, terminology, licence boundaries or product scope move later, editors, data formats, capabilities and cloud sync all rework (`I2 §III.0`).

---

## 1. Scope and purpose

**In scope.** Establishing in the implementation repository the enforceable form of decisions already taken in Phase 1: the product baseline, the normative glossary and invariant catalogue, the licence boundary declaration, the reuse and provenance process, the reference audit method, and the terminology enforcement mechanism.

**Out of scope.** Any product feature. Any architectural decision — those are made; this package records and enforces them. Producing the *content* of each per-product Reference Coverage Matrix beyond the first (those sit inside each product's own package).

**Why this package exists.** Every later package cites terms, boundaries and identifiers from this one. A term that means two things, a project on the wrong side of a licence boundary, or a reused file with no provenance record are all defects that become exponentially more expensive after code exists.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../decisions/phase-1-foundation-decisions.md`](../../decisions/phase-1-foundation-decisions.md) | D-001 … D-023 are binding and are not reopened here |
| [`../../requirements/00-product-scope-and-portfolio.md`](../../requirements/00-product-scope-and-portfolio.md) | The four-product freeze, the technology constitution and the closed exception list |
| [`../../requirements/01-normative-glossary-and-invariants.md`](../../requirements/01-normative-glossary-and-invariants.md) | The glossary and invariant catalogue this package makes enforceable |
| [`../../assurance/reference-coverage-and-provenance.md`](../../assurance/reference-coverage-and-provenance.md) | The matrix columns, the ten-field provenance record and the licence decision table |
| [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md) | The gates this package opens and schedules |
| The existing monorepo's `NOTICE.md`, `LICENSE` and package declarations | The current licence position that must be verified rather than assumed |
| Upstream work packages | **None.** This is the first package. |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The product baseline is exactly ArcChat, ArcNotes, ArcScope and ArcSlate** (**D-002**). `ArcCanvas`, `ArcMusic`, `ArcImage` and `ArcVideo` are superseded and must never appear as current products. |
| BR-02 | **`ArcVideo` and `ArcVideoFoundation` remain valid only as the names of existing reference repositories** (**D-012**), never as products. |
| BR-03 | **Paddle is the sole customer-facing Merchant of Record; Payoneer is a payout destination only** (**D-005**). The superseded provider name never appears. |
| BR-04 | **One canonical definition per cross-product term; product-specific meanings are namespaced** (**D-018**). |
| BR-05 | **Every accepted `X ≠ Y` invariant is preserved** (**D-018**) and becomes enforceable. |
| BR-06 | **Two licence boundaries exist**: Apache-2.0 for the interoperability boundary, AGPL-3.0-only for everything else (**D-004**, **D-021**). |
| BR-07 | **No App Store exception, dual licensing, proprietary grant or CLA** (**D-004**). DCO continues with inbound-equals-outbound per scope. |
| BR-08 | **Copy First is licence-gated and provenance-gated** (**D-013**). Unconditional copying is rejected. |
| BR-09 | **A repository-root licence must not be assumed to cover every file** (**D-013**). |
| BR-10 | **The technical exception list is closed** (`§8.1` of the scope requirements). Adding to it requires a formal decision. |
| BR-11 | **The ArcChat AOT position is settled**: ArcChat Desktop is a Native AOT deliverable like the other desktop products (**D-008**). Any residual corpus text suggesting otherwise is stale. |
| BR-12 | **ArcNotes scope is the phased full inclusion of edgeless, database views and slides** (**D-006**), not a reduced subset. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `eng/policy/` | Created: forbidden-term list, obsolete-name list, banned-symbol list, licence policy per boundary |
| `eng/policy/glossary-terms.json` | Created: the canonical term set with namespacing, generated from the glossary document |
| `NOTICE.md` | Verified and regenerated from the provenance records that exist |
| `LICENSE`, per-project SPDX declarations | Verified; every project declares its SPDX identifier and its boundary |
| `Directory.Build.props` | Gains the boundary property that every project must set |
| `docs/` in the implementation repository | Reduced to implementation-facing notes; design authority stays in this repository (**D-017**) |
| `tests/RepositoryPolicyTests/` | Created (implemented in `05`; the policy data lands here) |
| Reference audit workspace | Created: the per-product matrix template and the provenance record template |

**Major types introduced:** none — this package produces policy data, declarations and process artifacts, not runtime types.

---

## 5. Required implementation work

### WP-00.00 — Product and naming freeze

**What must be fully done.** A single naming authority file listing the four current products with their canonical identifiers, display names, reserved namespaces and file-association identifiers. The superseded product names and the superseded payment provider are recorded as **forbidden**, with the reference-repository exception (`BR-02`) stated explicitly and narrowly. Legacy-to-target name mapping is recorded so historical material can be read without reintroducing the old names.

**Testing requirements.** A scan asserting no forbidden name appears in source, identifiers, resource strings or implementation documentation. The scan's exception list contains only the reference-repository names in provenance contexts.

**Completion gate.** The scan runs clean, and the exception list is reviewed and minimal.

### WP-00.01 — Glossary and invariant enforcement data

**What must be fully done.** The canonical term set and the invariant catalogue are exported from the glossary requirements into machine-readable policy data: canonical terms with their term space (domain, wire, UI, storage, commercial), product namespacing, forbidden aliases, and every `X ≠ Y` invariant with its identifier. Each invariant records its intended enforcement mechanism — type distinction, policy test, unit test or end-to-end test.

**Testing requirements.** A consistency check that every term in the policy data appears in the glossary document and the reverse; a check that every invariant has an enforcement mechanism assigned.

**Completion gate.** The policy data is complete, matches the glossary document exactly, and every invariant has a named mechanism. **This satisfies part of `PG-06`**; the coverage assertion itself lands in `05`.

### WP-00.02 — Licence boundary declaration

**What must be fully done.** Every project declares its SPDX identifier and its licence boundary as a build property. The Apache-2.0 set is enumerated explicitly: public protocol specifications, wire schemas, DTOs, public clients, contract-level validators, the public SDK, mobile-only libraries and ArcChat Mobile. Everything else is AGPL-3.0-only. The boundary is expressed as data that a policy test can read.

**Testing requirements.** A check that every project declares a boundary; a check that the declared boundary matches the enumerated set; a reference-direction check that no AGPL project is referenced from an Apache project.

**Completion gate.** Every project declares a boundary, and the reference-direction check passes. **This is a precondition for `03`.**

### WP-00.03 — Reuse and provenance process

**What must be fully done.** The provenance record template implementing the ten fields of **D-013** exists, with a storage location, a naming convention and a review step. The licence decision table is encoded as policy data. The process states who may approve a disposition, and what happens on discovery of a conflicting contribution — registered and returned for decision, never silently excepted (`BR-07`).

**Testing requirements.** A check that every file identified as externally originated has a provenance record; a check that no record is missing a required field.

**Completion gate.** The process exists, the template is in use for at least one real record, and the checks run in CI.

### WP-00.04 — Reference audit method and the first matrix

**What must be fully done.** The Reference Coverage Matrix template exists with every required column. The **first** matrix is produced end to end for one product, to prove the method works and to calibrate effort. ArcChat with AionUi is the calibration target, because ArcChat is the first product built.

**Testing requirements.** A completeness check on the produced matrix: every item has a disposition, a rationale, a licence position where required, a verification oracle and an owner.

**Completion gate.** The template is proven by one complete matrix. **This fires the `F-013` trigger for ArcChat** and satisfies `PG-01` for ArcChat.

### WP-00.05 — Stale-claim reconciliation

**What must be fully done.** Every claim in existing repository documentation that conflicts with the frozen position is corrected: the ArcChat AOT position (`BR-11`), the ArcNotes scope position (`BR-12`), any statement that Cloud must publish as Native AOT (contradicted by **D-008** and **V-03**), any statement that realtime is unsupported under AOT (contradicted by **V-03**), and any reference to the superseded payment provider or superseded products.

**Testing requirements.** The forbidden-term scan plus a manual review of every implementation document that states a runtime, licence or scope position.

**Completion gate.** No stale claim remains in the implementation repository.

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
| Forbidden-term scan report, clean | `WP-00.00`, `WP-00.05` |
| Glossary and invariant policy data, consistency-checked | `WP-00.01` |
| Licence boundary declaration report, every project covered | `WP-00.02` |
| Provenance record set with a completeness check | `WP-00.03` |
| The ArcChat Reference Coverage Matrix, complete | `WP-00.04` |
| A review record for every corrected stale claim | `WP-00.05` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. The four-product baseline and forbidden-name set are enforced by a scan that runs clean.
2. The glossary and invariant catalogue exist as machine-readable policy data, consistent with the glossary document, with an enforcement mechanism assigned to every invariant.
3. Every project declares an SPDX identifier and a licence boundary, and the reference-direction check passes.
4. The provenance process exists, is encoded as policy data, and is in use for at least one real record.
5. The Reference Coverage Matrix template is proven by one complete matrix (ArcChat/AionUi), satisfying `PG-01` for ArcChat and firing the `F-013` trigger for it.
6. No stale runtime, licence or scope claim remains in the implementation repository.

---

## 9. Dependencies

**Upstream.** None. This is the first package in the sequence.

**Downstream.**

| Package | What it needs from here |
|---|---|
| `01` — Repository reconciliation | The licence boundary declaration and the naming freeze, so dispositions can be assigned correctly |
| `47` — Static public site | Frozen product names, display names and the content source of truth |
| `05` — Policy tests | The policy data this package produces |
| `15`, `18`, `33`, `36` — product cores | The matrix method, and for ArcChat the completed matrix |
| Every later package | The vocabulary, invariants and licence boundaries |
