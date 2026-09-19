# Reference Coverage and Provenance

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** (reference-repository roles), **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** (reuse policy, governs **[F-013](open-gates-register.md#rule-f-013)**), **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** (licence boundaries)
> Companions: [`../requirements/00-product-scope-and-portfolio.md`](../requirements/00-product-scope-and-portfolio.md), [`../architecture/01-solution-and-project-layout.md`](../architecture/01-solution-and-project-layout.md), [`release-gates.md`](release-gates.md)

This document defines two obligations that gate implementation: the **Reference Coverage Matrix** each product must have before its implementation planning is finalised (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**), and the **provenance record** that must exist before any reference material is copied, translated, ported or structurally reused (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**).

Nothing in this document authorises reuse. It defines the process by which reuse becomes authorised, and the evidence that must exist first.

---

## 1. What a reference repository is, and is not

| # | Rule |
|---|---|
| <a id="rule-rr-01"></a>RR-01 | **A reference repository is a source of features, behaviour, tests, migration evidence and possibly reusable material** (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**). |
| <a id="rule-rr-02"></a>RR-02 | **A reference repository is not an architecture authority.** Its structure, layering, technology stack and runtime choices carry no weight in ArcForges design decisions. |
| <a id="rule-rr-03"></a>RR-03 | **A reference repository is not a parity commitment.** Its feature set is evidence about a problem space, not a scope obligation. |
| <a id="rule-rr-04"></a>RR-04 | **A reference repository is not a reason to import its runtime stack** (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**). |
| <a id="rule-rr-05"></a>RR-05 | **Reading a reference repository is always permitted; reusing its material is not** — reuse requires `§3` and `§4`. |
| <a id="rule-rr-06"></a>RR-06 | **Reference repositories are never modified.** This is a documentation repository, and the reference checkouts are read-only evidence. |

### 1.1 The reference map (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**, as amended 2026-09-05 by [P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005))

| Reference | Role | Consuming product |
|---|---|---|
| AionUi | Behaviour and feature reference | ArcChat |
| AFFiNE | Behaviour, feature and editor-model reference | ArcNotes |
| SiYuan | Behaviour, feature and knowledge-model reference | ArcNotes |
| Serial-Studio | Behaviour, acquisition and visualisation reference | ArcScope |
| ArcVideo | Behaviour, timeline, editing-model and implementation-experience reference | ArcSlate |
| ArcVideoFoundation | Media-foundation implementation experience | ArcSlate |
| StartArcForges | Packaged-product and release-behaviour oracle | Distribution and release |
| The existing ArcForges monorepo | Implementation-state inventory and reconciliation target | All — see [`implementation-state-reconciliation.md`](implementation-state-reconciliation.md) |

> **Naming note.** `ArcVideo` and `ArcVideoFoundation` appear here **only** as the names of existing reference repositories. They are **not** current products: the desktop product baseline is exactly ArcNotes, ArcScope and ArcSlate, with embedded assistants and Android/Web companions under **[P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012)**, and `ArcCanvas`, `ArcMusic`, `ArcImage` and `ArcVideo` are superseded product names that must never appear as current products in any authoritative document.

---

## 2. The Reference Coverage Matrix

**Every product must receive a Reference Coverage Matrix before implementation planning for that product is finalised** (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**). The matrix is the artifact that turns "we have a reference" into a decided, per-item position.

### 2.1 Required columns

| Column | Content |
|---|---|
| `ItemId` | Stable identifier within the product's matrix |
| Reference | Which reference repository the item comes from |
| Capability or behaviour | What the item actually is, in ArcForges vocabulary — not the reference's own naming |
| Evidence location | Where in the reference it is observable (path, feature, test, document) |
| ArcForges requirement | The requirement identifier this item maps to, or `NONE` |
| Disposition | **Copy · Rewrite · Improve · Replace · Reference Only · Drop** (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) |
| Rationale | Why that disposition, in one or two sentences |
| Licence position | The file-level licence finding for the specific material, where a disposition other than *Reference Only* or *Drop* is chosen |
| Verification oracle | How ArcForges will know its own implementation is correct (`§5`) |
| V1 scope | In V1, deferred, or out of scope |
| Owner | Named owner of the item |

| # | Rule |
|---|---|
| <a id="rule-cm-01"></a>CM-01 | **Every item has a disposition.** "Not yet decided" is not a disposition; an undecided item blocks the matrix. |
| <a id="rule-cm-02"></a>CM-02 | **A disposition of Copy, Rewrite, Improve or Replace requires a completed provenance record** (`§3`) before any material is used. |
| <a id="rule-cm-03"></a>CM-03 | **A disposition of Reference Only means behavioural evidence only** — read it, learn from it, cite it in the matrix, and write original code. |
| <a id="rule-cm-04"></a>CM-04 | **A disposition of Drop is recorded with a reason**, so the decision is not silently revisited later. |
| <a id="rule-cm-05"></a>CM-05 | **An item with no corresponding ArcForges requirement is either dropped or produces a requirement change**, never an unrequested feature. |
| <a id="rule-cm-06"></a>CM-06 | **The matrix is a living document per product** and is updated whenever a disposition changes. A changed disposition records who changed it and why. |
| <a id="rule-cm-07"></a>CM-07 | **The matrix is complete before the product's implementation-planning work package is closed** — this is the completion gate that **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** requires. |

### 2.2 Per-product matrix status

**All matrices are complete.** They were produced as design-stage evidence before the implementation plan was derived, as **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** and **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** require. This document defines the method; [`reference-coverage/`](reference-coverage/README.md) holds the evidence.

| Product | Required references | Matrix | Rows | Status |
|---|---|---|---|---|
| ArcChat | AionUi | [`arcchat-aionui.md`](reference-coverage/arcchat-aionui.md) | 30 | **Complete** — 24 evidence established, 6 accepted exclusions, 0 unresolved |
| ArcNotes | AFFiNE, SiYuan | [`arcnotes-affine-siyuan.md`](reference-coverage/arcnotes-affine-siyuan.md) | 41 | **Complete** — 33 evidence established, 9 accepted exclusions, 0 unresolved |
| ArcScope | Serial-Studio | [`arcscope-serial-studio.md`](reference-coverage/arcscope-serial-studio.md) | 31 | **Complete** — 24 evidence established, 7 accepted exclusions, 0 unresolved |
| ArcSlate | ArcVideo, ArcVideoFoundation | [`arcslate-arcvideo.md`](reference-coverage/arcslate-arcvideo.md) | 31 | **Complete** |
| Distribution and release | StartArcForges | [`distribution-startarcforges.md`](reference-coverage/distribution-startarcforges.md) | 12 | **Complete** within the authorized oracle boundary |
| Whole repository | Existing ArcForges monorepo | [`implementation-state-reconciliation.md`](implementation-state-reconciliation.md) | 166 projects | **Complete** — item-level, with dispositions |

**Counting rule.** The five matrices contain 145 item rows, 121 evidence dispositions and 25 exclusion dispositions (146 total). [Notes AN-14](reference-coverage/arcnotes-affine-siyuan.md#rule-an-14) has both an established quota half and excluded sharing half; row count and disposition count must not be conflated.

**Gate consequence.** [PG-01](open-gates-register.md#rule-pg-01) and [F-013](open-gates-register.md#rule-f-013) are **closed** for every registered reference. [PG-02](open-gates-register.md#rule-pg-02) is **closed**. Implementation packages consume these matrices as versioned inputs and run drift checks only ([WP-15.07](../planning/work-packages/15-arcchat-conversation-core.md#rule-wp-15.07), [WP-18.08](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.08), [WP-33.07](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.07), [WP-36.07](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.07), [WP-01.00](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.00)).

---

## 3. The provenance record (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**)

**Before any source, test, asset or generated artifact is copied, translated, ported or structurally reused**, the following ten fields are recorded. This is not a summary of **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**; it is the operative checklist.

| # | Field | Requirement |
|---|---|---|
| 1 | Exact source repository | Canonical repository identity, not a nickname |
| 2 | Exact commit | A specific commit hash; "current main" is not acceptable |
| 3 | Exact source path | The specific file or files |
| 4 | File-level licence and SPDX evidence | **The file's own licence.** A repository-root licence must not be assumed to cover every file (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) |
| 5 | Copyright and attribution obligations | Every notice that must be preserved |
| 6 | Target file or project | Where the material will live in ArcForges |
| 7 | Intended disposition | Copy, Rewrite, Improve, Replace, Reference Only or Drop |
| 8 | Verification oracle | How correctness will be demonstrated (`§5`) |
| 9 | NOTICE requirement | What must appear in the distributed NOTICE, and where |
| 10 | Temporary or permanent | Whether the reuse is a transitional step or the intended end state |

| # | Rule |
|---|---|
| <a id="rule-pr-01"></a>PR-01 | **No material is copied before its record exists.** The record is a precondition, not documentation written afterwards. |
| <a id="rule-pr-02"></a>PR-02 | **A temporary reuse carries a removal trigger and an owner**, so "temporary" does not quietly become permanent. |
| <a id="rule-pr-03"></a>PR-03 | **A record is immutable once material is used under it.** A changed intent produces a new record. |
| <a id="rule-pr-04"></a>PR-04 | **Tests and assets require their own licence checks** (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**). A test file, fixture, icon, font or sample media file is not covered by an assumption about source code. |
| <a id="rule-pr-05"></a>PR-05 | **Generated artifacts inherit the licence position of their generator and inputs**, and that position is recorded explicitly. |

### 3.1 Current-repository implementation profile

[WP-00.03](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.03) implements this profile in each of the nine current implementation owners. The current repositories are the audit subjects. The retired ArcChat initialization repository is historical lineage only; it is not a producer, build input or required checkout. This does not change the ArcChat feature name or the completed reference matrices.

**Storage and identity.** Each owner keeps a reusable JSON template at `eng/provenance/template.json`, records at `eng/provenance/records/<id>.json`, an active file inventory at `eng/provenance/files.json`, and the decision table at `eng/policy/reuse-policy.json`. IDs are unique lowercase words/numbers separated by hyphens and end in an explicit revision, for example `gradle-wrapper-9-7-1-r1`. A record contains all ten fields above, plus its schema version, stable ID, material kind and review evidence. The template documents the required shape; it is never counted as an approved record. Source repositories are canonical HTTPS identities, commits are full immutable Git object IDs, and source/target paths are explicit repository-relative paths without wildcards, traversal or links outside the owner. A release tag or package version supplements a commit; it never replaces one.

**Material and evidence.** Identify copied, translated, ported, structurally reused and generated source, tests, assets, fixtures, build wrappers, patches and retained third-party notices. The file inventory accounts for Git-tracked files, including tracked ignored files, and non-ignored new files during local checks. It distinguishes first-party authored material from active record bindings; a directory-wide exemption is not a provenance record. Each reused target is bound to an exact record and a SHA-256 digest, with declared LF normalization for text or raw bytes for binary material. An audit failure includes an unclassified file, missing record, missing target or changed recorded bytes. Reviewing the complete contribution identifies newly reused material, including material inserted into an existing authored file: an automated inventory does not prove authorship.

The licence evidence names the governing file/header and its exact source identity, the selected SPDX expression, any subordinate licence override and the compatibility finding. A package or repository root is evidence only after checking the particular source path's licensing scope. Attribution is explicit, including a reason where no attribution is required. Generated material records each generator and each input, their immutable identities and respective licence positions, the generation command and the resulting target licence position. An owned input or generator may reference an earlier owner commit containing those unchanged files; a record must not invent the future commit that will contain itself. The verification oracle records how source identity, transformation or regeneration is checked; source-archive/package digests and exact archive members supplement the source paths when material is retained from a published artifact.

**Existing material.** Initial records state the inspected current owner commit, the review date and that this is reconciliation of material already present. They do not claim that a new record existed before a historical copy. Retain available upstream and package evidence and verify the actual current bytes. An unresolved origin or licence conflict follows §4.3 and blocks the affected reuse; a baseline label does not grant an exception. Canonical licence text may be reconciled against a pinned authoritative template with an explicit byte/transformation oracle, without asserting an unknown historical download origin. Subsequent new reuse follows [PR-01](#rule-pr-01): complete and review its record before introducing the material, in the same reviewed contribution or an earlier one.

**Record lifecycle.** Used records are append-only, including records no longer active. A different source revision, target content, intent, attribution or lifetime produces a new record; the active file inventory identifies the replacement and the new record cites the superseded ID. Removing a target retires its active binding and preserves its record. CI compares record contents and presence against the event's trusted base commit; local checks compare with the fetched default branch, or the current committed baseline on that branch. Required history must be available, and a missing comparison base fails rather than silently disabling immutability. Temporary records name an accountable owner and an observable removal trigger. Reference Only and Drop record the decision but cannot bind reused implementation material.

**NOTICE and legal documents.** Each active record states whether a notice is required, the exact attribution text and the repository/distribution locations that retain it, or a reviewed reason that no distributed notice is required. Generate the source provenance notice summary deterministically from active records and verify it in CI. Preserve full licence texts and existing dependency notices; the summary never replaces them. Each existing packager verifies the obligations relevant to material it actually distributes. Build-only wrappers or declarations that are absent from a runtime artifact do not imply that their tools are bundled in it. A retained licence/NOTICE document is identified as legal text and reviewed under its own reproduction terms. Carrying that document does not admit the implementation governed by it, relicense it, or create an exception to the Apache boundary. In particular, preserving a dependency's required legal text must not be interpreted as permission to port its code. Generated notice summaries are checked against their record inputs and owned renderer; they do not require recursively self-referential records.

### 3.2 Material introduced only during packaging

The Git file inventory does not cover every distributed byte. Documentation generators, bundlers and packagers can introduce third-party scripts, styles, icons, fonts and other resources directly into an archive. These materials require the same ten-field provenance and compatibility review as checked-in files. A generator's own licence is not evidence that every resource it copies has that licence. Identify the actual included resources and their direct/transitive origins; preserve required full licence and NOTICE text in every affected companion archive as well as the main artifact. An SBOM describing only the runtime library graph does not establish the documentation resource closure.

For these outputs, a record may bind an exact owning project/package and artifact kind instead of pretending that a generated archive member is a tracked source file. Its generator and input identities, file-level licence evidence, attribution, disposition, oracle, notice locations and lifetime remain mandatory. The owner registers active artifact records explicitly and checks them before packaging. The candidate gate then produces a source-bound receipt containing the actual archive identity/hash, closed member inventory, member hashes, matched record IDs and verified notices. Fixed copied resources must match reviewed upstream/package bytes. Variable generated pages are verified against the pinned generator, declared inputs and generation oracle; their concrete hashes belong to the candidate receipt. New or changed unclassified resources fail the gate. Future CI version numbers or a commit that would contain the record itself are not invented in the immutable record.

This profile is required by the observed Contracts documentation archives: the JDK documentation producer copies executable resources, while the Dokka producer copies its own frontend and third-party resources. The current owning implementation audit must inspect their actual bytes and resolve any boundary conflict under §4.3 before publishing a replacement candidate. Replacement preserves complete API documentation, existing public package identities and immutable prior versions; it does not add a licence exception or treat a successful code compilation as a resource-licence check. The same trigger applies when another owner's existing packaging introduces such material. This implements [PR-05](#rule-pr-05), [AE-05](#rule-ae-05) and [AE-06](#rule-ae-06) within [WP-00.03](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.03), without importing a future producer or expanding product scope.

### 3.3 Existing native distribution closure

The [admitted native packages](../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry) retain their existing compiled-dependency, ABI, isolated-consumer and publication gates. Their artifact provenance profile also binds each included upstream component to its exact source commit, archive integrity, selected source/configuration, applicable file-level licence, build recipe and notices. A port manifest's licence label or `NOASSERTION` alone is not a compatibility decision. Record the actual selected licence and scope, including permissive alternatives and excluded subtrees; a build tool whose code is absent from the output is not represented as a runtime dependency. Compilation does not make the compiler's own implementation part of the application.

Review retained legal text for referenced companions. A summary containing a licence name or hyperlink cannot replace a required full licence, copyright or NOTICE file. Preserve existing notices and add the missing applicable texts from their immutable source. Candidate verification checks the exact legal bytes and closed recipe/resource membership, the installed binary and source-recipe identities, and every packaged member. The resulting receipt binds the owning commit, package, selected component records and actual hashes. An upstream version, licence scope, recipe or legal-text change needs a newly reviewed profile and superseding record.

Matching corresponding-source archives required for LGPL distribution remain separate compliance material, with their own original licences and exact digests. Their presence does not admit excluded source into the compiled product. The selected FFmpeg configuration continues to reject GPL/nonfree features; actual binary configuration, dynamic replaceability and matching source/patch delivery remain mandatory. Preserve the full upstream archive where it is the verified source of the selected build; identify the compiled scope and the archive's separate licensing scope explicitly. Do not relabel the complete archive as if every file had the selected runtime licence.

### 3.4 Existing Windows compiler-runtime redistributable

The existing Windows native closure includes unmodified Microsoft Visual C++ runtime DLLs. These compiler-runtime binaries retain Microsoft's terms; they are not first-party AGPL source or permissively licensed upstream source. Their review is specific to the compiler-runtime role in AGPL-3.0 §1's System Libraries definition and to Microsoft's independent redistribution grant. Neither finding supplies the other. This does not grant proprietary rights in ArcForges code, alter the five-row source-reuse table, admit vendor SDK implementation into an Apache boundary or authorize arbitrary proprietary libraries.

For this existing binary-only input, the immutable native artifact profile contains a separately reviewed platform-runtime record with the same ten evidence subjects: official vendor/distribution identity; exact release and actual DLL product/file versions; explicit distribution-relative file paths; the applicable licence and redistribution-list evidence; copyright/terms obligations; exact target projects/packages; unmodified-redistribution disposition; verification oracle; distributed notice/terms locations; and lifetime. Record the reason that no public source repository/commit exists. Use an explicit absence for those source-only fields, never an invented Git commit or a licence-document commit presented as the DLL source. Retain the official download/distribution identity, actual file hashes, Microsoft signature/publisher evidence and exact reviewed terms identity. The enclosing SDK/redist directory name alone is not the DLL version.

The Licensing and Provenance Owner records the permission, System Libraries reasoning, applicable distribution obligations and review date; the Architecture Owner confirms the narrow compiler-runtime role. The record binds only the reviewed release and exact files. The Windows producer verifies the vendor signature and unchanged bytes; packaging independently matches the approved hashes and requires the separate vendor notice/terms. A newly observed file, version, publisher, changed terms or unsupported role fails closed until a new reviewed record is admitted. Preserve recipients' rights in ArcForges source and apply vendor restrictions only to the separate vendor components. Unknown-source material does not qualify merely by calling itself a runtime.

**Audit basis (2026-09-19).** DesktopPlatform `1.0.0-ci.12.1`, source `3bc1917d5cb2d76261c0e27ceba774b9067da8c6`, has 11 Microsoft DLL occurrences across its four native runtime archives. All match the licensed Visual Studio redistributable bytes with valid Microsoft signatures and DLL product version `14.51.36247.0`; its prior SBOM reports the enclosing directory `14.51.36231`. The current [Microsoft redistribution guidance](https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files), [Visual Studio 2026 distributable list](https://learn.microsoft.com/en-us/visualstudio/releases/2026/redistribution) and [Community 2026 terms](https://visualstudio.microsoft.com/license-terms/vs2026-ga-community/) require review of the actual permitted files and distribution conditions. The [runtime end-user terms](https://visualstudio.microsoft.com/license-terms/vs2026-ga-visualcpp-v14-redist-runtime/) alone are not a redistribution grant. DesktopPlatform owns the record/notice repair and actual candidate verification; these observations do not assert that its replacement release already passed.

---

## 4. Licence gating

### 4.1 The decision table

| Source material licence | AGPL-3.0-only boundary | Apache-2.0 boundary (mobile, public clients, public SDK, public specs) |
|---|---|---|
| Permissive and compatible (MIT, BSD, Apache-2.0, …) | **Permitted after the `§3` audit** (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) | **Permitted after the `§3` audit**, subject to attribution obligations |
| AGPL-compatible copyleft | **Permitted only after exact compatibility and provenance review** (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) | **Prohibited** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**) |
| GPL-only | **Prohibited** for copy, translation or port (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) | **Prohibited** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**) |
| Licence unclear or unknown origin | **Prohibited** (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) | **Prohibited** |
| Otherwise incompatible | **Prohibited** (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) | **Prohibited** |

| # | Rule |
|---|---|
| <a id="rule-lg-01"></a>LG-01 | **Prohibited material may still be used as controlled behavioural or reference evidence**, until an explicit compatibility decision says otherwise (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**). Reading is not reuse. |
| <a id="rule-lg-02"></a>LG-02 | **No GPL-family or AGPL-only material may enter the Apache-2.0 mobile or public-client boundary** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**), directly or transitively. |
| <a id="rule-lg-03"></a>LG-03 | **Protocol communication across an explicit process or network boundary does not change a client's licence** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |
| <a id="rule-lg-04"></a>LG-04 | **On discovering a conflicting contribution or dependency, the issue is registered and returned for decision** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**). Silently adding an exception, changing the licence, or dropping the mobile target is prohibited. |
| <a id="rule-lg-05"></a>LG-05 | **No App Store exception, dual licensing, proprietary grant or CLA** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**). DCO continues with inbound-equals-outbound per scope. |

### 4.2 Automated enforcement

Licence compliance is automated, not remembered ([LG-06](../requirements/07-security-privacy-and-trust.md#rule-lg-06) in the security requirements).

| # | Mechanism | Where it runs |
|---|---|---|
| <a id="rule-ae-01"></a>AE-01 | Generated licence inventory for every project and every dependency | Build |
| <a id="rule-ae-02"></a>AE-02 | Dependency policy check against the per-boundary allowlist, build-breaking on violation | Build (`RP-*` repository policy tests) |
| <a id="rule-ae-03"></a>AE-03 | SBOM generation per artifact | Release pipeline ([SP-06](../architecture/14-build-packaging-and-release.md#rule-sp-06) in the build architecture) |
| <a id="rule-ae-04"></a>AE-04 | Transitive closure verification for the mobile boundary — the **[F-023](open-gates-register.md#rule-f-023)** gate | Before the first mobile artifact |
| <a id="rule-ae-05"></a>AE-05 | NOTICE generation and verification against the recorded attribution obligations | Release pipeline |
| <a id="rule-ae-06"></a>AE-06 | Provenance inventory and record checks under §3.1: every identified reused file has a complete, valid and immutable record; missing records fail the audit | Repository policy test and current owner CI |

### 4.3 Review responsibility and conflicts

The **Licensing and Provenance Owner** approves a disposition within the existing decision table after reviewing the particular files, licence evidence, boundary, attribution, oracle and lifetime. A repository maintainer exercising that assigned role, including a maintainer-authorized implementation review, records the reviewer identity, date and rationale in the record and retains the contribution's review evidence. The role remains accountable under [D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016); a field containing the word "approved" does not substitute for the review. The Architecture Owner decides a boundary/ownership question, and the Product Owner is the final authority when a product decision is required. Routine compatible reuse needs no new product decision.

Encode all five rows of §4.1 as closed policy data, preserving the difference between permitted-after-audit, exact-review-required and prohibited. Unknown licence classes, unsupported expressions and a changed decision table fail validation. A legal-document record also requires evidence of its own copying permission; it cannot be used to classify source code as a notice. Owners use their existing tooling languages and licence boundaries; this profile creates no sibling-source build dependency and does not move AGPL tooling into Contracts or Mobile.

Before copying or accepting a contribution, review the inventory and all ten fields, the actual file-level source evidence, generated inputs, required notices and the automated check result. A conflict is recorded in `eng/provenance/conflicts/<id>.json` with the affected material, observed evidence, boundary, accountable role, required decision and blocking status. The affected material is not accepted or distributed while the conflict is unresolved. Resolution records the formal decision and a new admissible record, or removes the material; it never silently changes the licence policy, adds an exception or removes a required product. A conflict discovered in an existing artifact also invokes the existing release gate and remediation owner.

Each owner's CI checks its real inventory and at least one used record, all ten fields and conditional generated/temporary obligations, legal-document classification, path containment, target digests, deterministic notices, closed policy decisions and record immutability. Failure tests cover missing/blank fields, missing records, inventory drift, incompatible boundary, changed bytes, escaping paths and mutation/removal of used records. These current checks implement [WP-00.03](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.03); the broader repository-policy work package does not postpone them. Dependency closure, SBOM and real release/runtime verification retain their separate existing gates.

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
| <a id="rule-vo-01"></a>VO-01 | **An oracle is named before implementation begins**, not chosen afterwards to fit what was built. |
| <a id="rule-vo-02"></a>VO-02 | **A reference's behaviour is evidence, not a requirement.** Where a reference's behaviour conflicts with an ArcForges requirement, the requirement wins and the divergence is recorded in the matrix. |
| <a id="rule-vo-03"></a>VO-03 | **A fixture is checked into the repository with its provenance record**, because a fixture is reused material. |
| <a id="rule-vo-04"></a>VO-04 | **An oracle that cannot be automated is recorded as a manual verification step** with an owner, never omitted. |

---

## 6. Migration and format evidence

Reference repositories are also the source of migration evidence — what existing users' data looks like.

| # | Rule |
|---|---|
| <a id="rule-me-01"></a>ME-01 | **Import compatibility targets are derived from real reference-produced files**, not from documentation of those formats alone. |
| <a id="rule-me-02"></a>ME-02 | **A format fixture set is versioned**, covering the reference versions ArcForges claims to import. |
| <a id="rule-me-03"></a>ME-03 | **An import claim is only made for versions with fixtures** (`§17` of the quality contract). A claim without a fixture is removed from the product surface, not left unverified. |
| <a id="rule-me-04"></a>ME-04 | **Data used as a fixture is either synthetic or licence-cleared** ([PR-04](#rule-pr-04)). Real user content is never checked in. |

---

## 7. The [F-013](open-gates-register.md#rule-f-013) gate — discharged

**[F-013](open-gates-register.md#rule-f-013)'s trigger has fired and been satisfied for the five accessible references.**

| Aspect | Position |
|---|---|
| What was deferred | The per-file licence determinations for reference material |
| Trigger | The first step of the per-product Reference Coverage Matrix and licence audit (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) — **fired 2026-09-05** |
| What was determined | Root and subtree licences read per reference; **the AFFiNE split and the Serial-Studio Pro-module exclusion were found below the repository root**, exactly the case **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** warns about. Every one of the 145 rows carries a licence position |
| Result | **No row proposes reuse.** Four of six accessible references are GPL-family, proprietary or AGPL. The per-file determination that would be required before any copy, translation or port has no pending subject |
| Owner | Licensing and Provenance Owner |
| State | **`CLOSED` 2026-09-05** for AionUi, AFFiNE, SiYuan, Serial-Studio, ArcVideo and ArcVideoFoundation — **the complete amended reference map** (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** as amended, [P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005)). No unresolved determination remains |
| Related gate | **[F-023](open-gates-register.md#rule-f-023)** — mobile provenance and full dependency closure before the first mobile artifact ([AE-04](#rule-ae-04)). Requires its own dependency-closure audit; see the [current candidate evidence and status](open-gates-register.md#21-current-android-candidate-licence-evidence). A reference audit cannot satisfy it |

| # | Rule |
|---|---|
| <a id="rule-fg-01"></a>FG-01 | **[F-013](open-gates-register.md#rule-f-013) closed on evidence, not on assertion.** The evidence is the five matrices and their per-row licence positions. |
| <a id="rule-fg-02"></a>FG-02 | **A per-file determination is still required before any future reuse.** Closing [F-013](open-gates-register.md#rule-f-013) records that none is currently proposed; it does not pre-authorise reuse. |
| <a id="rule-fg-03"></a>FG-03 | **A licence position can change upstream.** Each product's drift-check sub-step re-reads the reference's licence files, and a changed subtree licence corrects the affected dispositions before dependent work continues. |
| <a id="rule-fg-04"></a>FG-04 | **Upstream provenance survives a reference-map amendment.** [P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005) removed Olive as a separate required reference; ArcVideo's fork relationship, GPL-3.0 obligations and upstream attribution are unaffected and are preserved wherever inherited material requires them. |

---

## 8. Where this work is scheduled

| Obligation | Scheduled in |
|---|---|
| Per-product Reference Coverage Matrix | The reference-audit work package for each product, ahead of that product's implementation work packages ([`../planning/README.md`](../planning/README.md)) |
| Implementation-state reconciliation inventory | Before repository restructuring begins ([`implementation-state-reconciliation.md`](implementation-state-reconciliation.md)) |
| Automated licence enforcement | The build and repository-policy work package |
| Mobile dependency closure (**[F-023](open-gates-register.md#rule-f-023)**) | Before the first mobile artifact is produced |
| NOTICE generation and verification | The release-engineering work package |

---

## 9. Traceability

| Source | Consumed as |
|---|---|
| **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** | The reference map, the non-authority position, and the per-product matrix requirement |
| **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** | The ten-field provenance record, the licence decision table, the disposition vocabulary, and the [F-013](open-gates-register.md#rule-f-013) trigger |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** | The Apache boundary prohibition and the no-exception position |
| **[D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002)** | The four-product baseline, and why two reference names are not product names |
| **[F-013](open-gates-register.md#rule-f-013)**, **[F-023](open-gates-register.md#rule-f-023)** | The two deferred gates this document schedules |
