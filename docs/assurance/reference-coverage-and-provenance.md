# Reference Coverage and Provenance

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: **D-012** (reference-repository roles), **D-013** (reuse policy, governs **F-013**), **D-004**/**D-021** (licence boundaries)
> Companions: [`../requirements/00-product-scope-and-portfolio.md`](../requirements/00-product-scope-and-portfolio.md), [`../architecture/01-solution-and-project-layout.md`](../architecture/01-solution-and-project-layout.md), [`release-gates.md`](release-gates.md)

This document defines two obligations that gate implementation: the **Reference Coverage Matrix** each product must have before its implementation planning is finalised (**D-012**), and the **provenance record** that must exist before any reference material is copied, translated, ported or structurally reused (**D-013**).

Nothing in this document authorises reuse. It defines the process by which reuse becomes authorised, and the evidence that must exist first.

---

## 1. What a reference repository is, and is not

| # | Rule |
|---|---|
| RR-01 | **A reference repository is a source of features, behaviour, tests, migration evidence and possibly reusable material** (**D-012**). |
| RR-02 | **A reference repository is not an architecture authority.** Its structure, layering, technology stack and runtime choices carry no weight in ArcForges design decisions. |
| RR-03 | **A reference repository is not a parity commitment.** Its feature set is evidence about a problem space, not a scope obligation. |
| RR-04 | **A reference repository is not a reason to import its runtime stack** (**D-012**). |
| RR-05 | **Reading a reference repository is always permitted; reusing its material is not** — reuse requires `§3` and `§4`. |
| RR-06 | **Reference repositories are never modified.** This is a documentation repository, and the reference checkouts are read-only evidence. |

### 1.1 The reference map (**D-012**)

| Reference | Role | Consuming product |
|---|---|---|
| AionUi | Behaviour and feature reference | ArcChat |
| AFFiNE | Behaviour, feature and editor-model reference | ArcNotes |
| SiYuan | Behaviour, feature and knowledge-model reference | ArcNotes |
| Serial-Studio | Behaviour, acquisition and visualisation reference | ArcScope |
| Olive | Behaviour, timeline and editing-model reference | ArcSlate |
| ArcVideo (existing) | Behaviour and implementation-experience reference | ArcSlate |
| ArcVideoFoundation (existing) | Media-foundation implementation experience | ArcSlate |
| StartArcForges | Packaged-product and release-behaviour oracle | Distribution and release |
| The existing ArcForges monorepo | Implementation-state inventory and reconciliation target | All — see [`implementation-state-reconciliation.md`](implementation-state-reconciliation.md) |

> **Naming note.** `ArcVideo` and `ArcVideoFoundation` appear here **only** as the names of existing reference repositories. They are **not** current products: the product baseline is exactly ArcChat, ArcNotes, ArcScope and ArcSlate (**D-002**), and `ArcCanvas`, `ArcMusic`, `ArcImage` and `ArcVideo` are superseded product names that must never appear as current products in any authoritative document.

---

## 2. The Reference Coverage Matrix

**Every product must receive a Reference Coverage Matrix before implementation planning for that product is finalised** (**D-012**). The matrix is the artifact that turns "we have a reference" into a decided, per-item position.

### 2.1 Required columns

| Column | Content |
|---|---|
| `ItemId` | Stable identifier within the product's matrix |
| Reference | Which reference repository the item comes from |
| Capability or behaviour | What the item actually is, in ArcForges vocabulary — not the reference's own naming |
| Evidence location | Where in the reference it is observable (path, feature, test, document) |
| ArcForges requirement | The requirement identifier this item maps to, or `NONE` |
| Disposition | **Copy · Rewrite · Improve · Replace · Reference Only · Drop** (**D-013**) |
| Rationale | Why that disposition, in one or two sentences |
| Licence position | The file-level licence finding for the specific material, where a disposition other than *Reference Only* or *Drop* is chosen |
| Verification oracle | How ArcForges will know its own implementation is correct (`§5`) |
| V1 scope | In V1, deferred, or out of scope |
| Owner | Named owner of the item |

| # | Rule |
|---|---|
| CM-01 | **Every item has a disposition.** "Not yet decided" is not a disposition; an undecided item blocks the matrix. |
| CM-02 | **A disposition of Copy, Rewrite, Improve or Replace requires a completed provenance record** (`§3`) before any material is used. |
| CM-03 | **A disposition of Reference Only means behavioural evidence only** — read it, learn from it, cite it in the matrix, and write original code. |
| CM-04 | **A disposition of Drop is recorded with a reason**, so the decision is not silently revisited later. |
| CM-05 | **An item with no corresponding ArcForges requirement is either dropped or produces a requirement change**, never an unrequested feature. |
| CM-06 | **The matrix is a living document per product** and is updated whenever a disposition changes. A changed disposition records who changed it and why. |
| CM-07 | **The matrix is complete before the product's implementation-planning work package is closed** — this is the completion gate that **D-012** requires. |

### 2.2 Per-product matrix status

| Product | Required references | Matrix status | Blocking gate |
|---|---|---|---|
| ArcChat | AionUi | **Not started** | Required before ArcChat implementation planning is finalised |
| ArcNotes | AFFiNE, SiYuan | **Not started** | Required before ArcNotes implementation planning is finalised |
| ArcScope | Serial-Studio | **Not started** | Required before ArcScope implementation planning is finalised |
| ArcSlate | Olive, ArcVideo, ArcVideoFoundation | **Not started** | Required before ArcSlate implementation planning is finalised |
| Distribution and release | StartArcForges | **Not started** | Required before the release-engineering work package is closed |
| Whole repository | Existing ArcForges monorepo | **Not started** | Required before restructuring begins ([`implementation-state-reconciliation.md`](implementation-state-reconciliation.md)) |

> These are honest status statements, not placeholders for missing specification. Producing each matrix requires reading a reference repository item by item, which is implementation-planning work assigned to a specific work package (`§8`). The *specification* of what each matrix must contain, and the gate it must pass, is complete here.

---

## 3. The provenance record (**D-013**)

**Before any source, test, asset or generated artifact is copied, translated, ported or structurally reused**, the following ten fields are recorded. This is not a summary of **D-013**; it is the operative checklist.

| # | Field | Requirement |
|---|---|---|
| 1 | Exact source repository | Canonical repository identity, not a nickname |
| 2 | Exact commit | A specific commit hash; "current main" is not acceptable |
| 3 | Exact source path | The specific file or files |
| 4 | File-level licence and SPDX evidence | **The file's own licence.** A repository-root licence must not be assumed to cover every file (**D-013**) |
| 5 | Copyright and attribution obligations | Every notice that must be preserved |
| 6 | Target file or project | Where the material will live in ArcForges |
| 7 | Intended disposition | Copy, Rewrite, Improve, Replace, Reference Only or Drop |
| 8 | Verification oracle | How correctness will be demonstrated (`§5`) |
| 9 | NOTICE requirement | What must appear in the distributed NOTICE, and where |
| 10 | Temporary or permanent | Whether the reuse is a transitional step or the intended end state |

| # | Rule |
|---|---|
| PR-01 | **No material is copied before its record exists.** The record is a precondition, not documentation written afterwards. |
| PR-02 | **A temporary reuse carries a removal trigger and an owner**, so "temporary" does not quietly become permanent. |
| PR-03 | **A record is immutable once material is used under it.** A changed intent produces a new record. |
| PR-04 | **Tests and assets require their own licence checks** (**D-013**). A test file, fixture, icon, font or sample media file is not covered by an assumption about source code. |
| PR-05 | **Generated artifacts inherit the licence position of their generator and inputs**, and that position is recorded explicitly. |

---

## 4. Licence gating

### 4.1 The decision table

| Source material licence | AGPL-3.0-only boundary | Apache-2.0 boundary (mobile, public clients, public SDK, public specs) |
|---|---|---|
| Permissive and compatible (MIT, BSD, Apache-2.0, …) | **Permitted after the `§3` audit** (**D-013**) | **Permitted after the `§3` audit**, subject to attribution obligations |
| AGPL-compatible copyleft | **Permitted only after exact compatibility and provenance review** (**D-013**) | **Prohibited** (**D-004**) |
| GPL-only | **Prohibited** for copy, translation or port (**D-013**) | **Prohibited** (**D-004**) |
| Licence unclear or unknown origin | **Prohibited** (**D-013**) | **Prohibited** |
| Otherwise incompatible | **Prohibited** (**D-013**) | **Prohibited** |

| # | Rule |
|---|---|
| LG-01 | **Prohibited material may still be used as controlled behavioural or reference evidence**, until an explicit compatibility decision says otherwise (**D-013**). Reading is not reuse. |
| LG-02 | **No GPL-family or AGPL-only material may enter the Apache-2.0 mobile or public-client boundary** (**D-004**), directly or transitively. |
| LG-03 | **Protocol communication across an explicit process or network boundary does not change a client's licence** (**D-004**). |
| LG-04 | **On discovering a conflicting contribution or dependency, the issue is registered and returned for decision** (**D-004**). Silently adding an exception, changing the licence, or dropping the mobile target is prohibited. |
| LG-05 | **No App Store exception, dual licensing, proprietary grant or CLA** (**D-004**). DCO continues with inbound-equals-outbound per scope. |

### 4.2 Automated enforcement

Licence compliance is automated, not remembered (`LG-06` in the security requirements).

| # | Mechanism | Where it runs |
|---|---|---|
| AE-01 | Generated licence inventory for every project and every dependency | Build |
| AE-02 | Dependency policy check against the per-boundary allowlist, build-breaking on violation | Build (`RP-*` repository policy tests) |
| AE-03 | SBOM generation per artifact | Release pipeline (`SP-06` in the build architecture) |
| AE-04 | Transitive closure verification for the mobile boundary — the **F-023** gate | Before the first mobile artifact |
| AE-05 | NOTICE generation and verification against the recorded attribution obligations | Release pipeline |
| AE-06 | Provenance-record presence check: a file whose provenance record is missing fails the audit | Repository policy test |

---

## 5. Verification oracles

A verification oracle answers: *how do we know our implementation is correct?* It is required in both the coverage matrix and the provenance record.

| Oracle kind | Use |
|---|---|
| **Reference behaviour observation** | The reference's observable behaviour for a stated scenario, recorded as an expectation — used where the reference is the best available specification of a domain behaviour |
| **Format fixture** | A file produced by the reference, which ArcForges must read correctly — used for import and migration paths |
| **Round-trip fixture** | ArcForges writes, the reference reads, or the reverse — used where interoperability is required |
| **Golden output** | A fixed input producing a fixed output within a declared tolerance — used for media, decode, render and analysis paths |
| **Specification** | An external standard the reference also implements — always preferred to the reference itself where one exists |
| **First-party test** | An ArcForges test derived from ArcForges requirements — the default where none of the above applies |

| # | Rule |
|---|---|
| VO-01 | **An oracle is named before implementation begins**, not chosen afterwards to fit what was built. |
| VO-02 | **A reference's behaviour is evidence, not a requirement.** Where a reference's behaviour conflicts with an ArcForges requirement, the requirement wins and the divergence is recorded in the matrix. |
| VO-03 | **A fixture is checked into the repository with its provenance record**, because a fixture is reused material. |
| VO-04 | **An oracle that cannot be automated is recorded as a manual verification step** with an owner, never omitted. |

---

## 6. Migration and format evidence

Reference repositories are also the source of migration evidence — what existing users' data looks like.

| # | Rule |
|---|---|
| ME-01 | **Import compatibility targets are derived from real reference-produced files**, not from documentation of those formats alone. |
| ME-02 | **A format fixture set is versioned**, covering the reference versions ArcForges claims to import. |
| ME-03 | **An import claim is only made for versions with fixtures** (`§17` of the quality contract). A claim without a fixture is removed from the product surface, not left unverified. |
| ME-04 | **Data used as a fixture is either synthetic or licence-cleared** (`PR-04`). Real user content is never checked in. |

---

## 7. The F-013 gate

**F-013 remains `DEFERRED_WITH_OWNER_AND_TRIGGER`** (**D-013**).

| Aspect | Position |
|---|---|
| What is deferred | The per-file licence determinations for reference material |
| Trigger | **The first step of the per-product Reference Coverage Matrix and licence audit**, before substantive reference source is used for planning or implementation (**D-013**) |
| Owner | Licensing and Provenance Owner |
| Blocking | Implementation planning for the affected product cannot be finalised until the matrix and audit for that product are complete (`CM-07`) |
| Related gate | **F-023** — mobile provenance and full dependency closure before the first mobile artifact (`AE-04`) |

| # | Rule |
|---|---|
| FG-01 | **F-013 is not resolved by this document.** It is scheduled by it. |
| FG-02 | **A product's licence audit result is recorded in that product's matrix**, and its completion is a work-package completion gate (`§8`). |
| FG-03 | **An audit finding that blocks a planned disposition changes the disposition**, and the change is recorded with its reason (`CM-06`). |

---

## 8. Where this work is scheduled

| Obligation | Scheduled in |
|---|---|
| Per-product Reference Coverage Matrix | The reference-audit work package for each product, ahead of that product's implementation work packages ([`../planning/README.md`](../planning/README.md)) |
| Implementation-state reconciliation inventory | Before repository restructuring begins ([`implementation-state-reconciliation.md`](implementation-state-reconciliation.md)) |
| Automated licence enforcement | The build and repository-policy work package |
| Mobile dependency closure (**F-023**) | Before the first mobile artifact is produced |
| NOTICE generation and verification | The release-engineering work package |

---

## 9. Traceability

| Source | Consumed as |
|---|---|
| **D-012** | The reference map, the non-authority position, and the per-product matrix requirement |
| **D-013** | The ten-field provenance record, the licence decision table, the disposition vocabulary, and the F-013 trigger |
| **D-004**, **D-021** | The Apache boundary prohibition and the no-exception position |
| **D-002** | The four-product baseline, and why two reference names are not product names |
| **F-013**, **F-023** | The two deferred gates this document schedules |
