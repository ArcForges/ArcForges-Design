<a id="rule-wp-19"></a>

# WP-19 — ArcNotes Search, Import, Export and Portability

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: D — ArcNotes core
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Make ArcNotes content findable and portable **within the accepted exit path** (`§13` of the ArcNotes requirements): search over hydrated content with citation anchors, non-destructive Markdown and plain-text import, and the **Cloud-generated notebook download** — proving the exit path rather than asserting it.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcNotes; Cloud export interfaces. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The local search index over hydrated content and its query surface; citation anchors; saved views over queries; non-destructive import from Markdown and plain-text sources including an Obsidian-style folder layout ([IM-02](../../requirements/products/arcnotes.md#rule-im-02)); and the client half of the **Cloud notebook export** with its fidelity report.

**Out of scope by [EP-04](../../requirements/products/arcnotes.md#rule-ep-04), [IM-02](../../requirements/13-data-formats-and-portability.md#rule-im-02) and `§14` of the data-format requirements.** Repository projection, Git synchronisation, linked-repository editing and LFS integration; native portable packages; HTML, PDF and DOCX export pipelines; bit-for-bit archive round-trips; custom local encrypted export; DOCX, Notion-specific, HTML and proprietary full-fidelity importers; and any live bidirectional folder mirror or linked-vault mode ([IM-07](../../requirements/products/arcnotes.md#rule-im-07)).

**Out of scope.** Cloud search (`40` and `25`). Semantic retrieval and embeddings (`40`). Database-view queries (`28`) — saved views here are list projections only.

**Why this package exists.** [the mock policy](../implementation-sequence.md#3-what-may-be-mocked-and-what-may-not) requires local full-text indexing and citation anchors to be **real early**, because cloud search may be mocked but the local index cannot. Export is also the precondition for sync: a format that cannot round-trip locally will not round-trip through a server.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile)

**Frozen design input.** [content-origin behavior](../../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carrier schema](../../requirements/13-data-formats-and-portability.md#content-origin-carriers) is fixed before this package; implement it without choosing a different marking mechanism.

| Input | Why it matters |
|---|---|
| [`../../requirements/06-knowledge-search-and-retrieval.md`](../../requirements/06-knowledge-search-and-retrieval.md) | Search versus retrieval, evidence and citation anchors, permission-aware retrieval |
| [`../../requirements/13-data-formats-and-portability.md`](../../requirements/13-data-formats-and-portability.md) | The portability constitution, import and export obligations, and the **repository-projection exclusion** (`§14`, [EX-09](../../requirements/13-data-formats-and-portability.md#rule-ex-09)) |
| [`../../architecture/06-data-persistence-and-formats.md`](../../architecture/06-data-persistence-and-formats.md) `§8` | The import pipeline and the export pipeline |
| [WP-18](18-arcnotes-document-core.md#rule-wp-18) output | The document model, link index and attachment model |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Search over hydrated content works during a Cloud outage.** Workspace-wide search is `search.query` on the public surface; the two are separate operations with different completeness and neither is presented as the other ([NO-05](../../architecture/contracts/02-local-rpc-operations.md#rule-no-05)). |
| <a id="rule-br-02"></a>BR-02 | **`Search ≠ Retrieval`.** Search serves a person; retrieval assembles evidence for a model. They share an index but not a contract. |
| <a id="rule-br-03"></a>BR-03 | **The index is a derived store**: deleting it rebuilds completely ([QI-10](../../requirements/12-quality-and-compatibility-contract.md#rule-qi-10)). |
| <a id="rule-br-04"></a>BR-04 | **Search reveals nothing direct access would refuse** — permission is applied at query, not after ranking. |
| <a id="rule-br-05"></a>BR-05 | **A citation anchor is stable**, surviving edits around it where the cited content still exists, and reporting explicitly when it does not. |
| <a id="rule-br-06"></a>BR-06 | **Import is non-destructive**: the source is never modified, and a partial import is reported rather than silently completed. |
| <a id="rule-br-07"></a>BR-07 | **Export declares its fidelity.** The Cloud exit path is Markdown documents, authorized attachments, metadata/link manifest and explicit loss report, under [EP-04](../../requirements/products/arcnotes.md#rule-ep-04) and [EX-01](../../requirements/13-data-formats-and-portability.md#rule-ex-01)/[EX-02](../../requirements/13-data-formats-and-portability.md#rule-ex-02). Verify the declared content/link/attachment fidelity; do not build a native portable package, encrypted local export or bit-for-bit archive re-import promise. |
| <a id="rule-br-08"></a>BR-08 | **An export never silently loses fidelity.** A lossy target format states what it drops. |
| <a id="rule-br-09"></a>BR-09 | **No repository projection, Git synchronisation, linked-repository mode or LFS path is built** (`§14` and [EX-09](../../requirements/13-data-formats-and-portability.md#rule-ex-09) of the data-format requirements; [EE-04](../../requirements/13-data-formats-and-portability.md#rule-ee-04) there). [GT-01](../../requirements/13-data-formats-and-portability.md#rule-gt-01)–[GT-09](../../requirements/13-data-formats-and-portability.md#rule-gt-09) are retired, explicitly including their acceptance gates, so no Git-friendliness level is declared and none may be demanded. |

---

## 4. Projects, directories, files and major types affected

Content payloads use typed ContentOrigin and content-unit bindings under their existing owner revision; format/schema fixtures include that projection.

| Location | Change |
|---|---|
| `src/ArcNotes/ArcNotes.Search/` | Index, tokenisation, query, ranking, citation anchors, saved views |
| `src/ArcNotes/ArcNotes.ImportExport/` | Markdown and plain-text import pipeline, and the client half of the Cloud export download. **No portable-package writer, no HTML/PDF/DOCX pipeline** ([EP-04](../../requirements/products/arcnotes.md#rule-ep-04)) |
| `src/ArcNotes/ArcNotes.Application/` | Search and import/export application services |
| `fixtures/formats/import/` | Source-format fixtures for every supported import claim |
| `fixtures/formats/arcnotes/v1/` | Markdown/plain-text import and Cloud-export manifest/fidelity fixtures |
| `tests/ArcNotes.Tests.Integration/` | Search, import and Cloud-export client suites |

**Major types introduced.** `SearchIndex`, `SearchQuery`, `SearchResult`, `CitationAnchor`, `SavedView`, `ImportSource`, `ImportPlan`, `ImportReport`, `ExportTarget`, `ExportReport`, `CloudExportManifest`.

---

## 5. Required implementation work

<a id="rule-wp-19.00"></a>

### WP-19.00 — Local full-text index

**What must be fully done.** An incremental index over document content, block content, properties, tags and attachment-extracted text. Updates follow the write path so the index never diverges. The index rebuilds fully from canonical data. Query latency meets budget on the scale corpus.

**Testing requirements.** Divergence test after a crash mid-index-update; full rebuild equivalence; latency measurement against the scale corpus.

**Completion gate.** The index never diverges after a crash, rebuilds to an equivalent state, and meets query latency budget at scale.

<a id="rule-wp-19.01"></a>

### WP-19.01 — Query, ranking and permission

**Required design implementation and verification.** Apply the profile to bounded scalar predicates in the local hydrated query path; ordinary full-text ranking stays separate. Include source token and explicit completeness/pending status.

**What must be fully done.** Query supporting text, property, tag and structural filters. Ranking is explainable at a basic level. Permission is applied during query evaluation so that a refused document never influences results, including result counts.

**Testing requirements.** Filter coverage tests; a permission test asserting refused content affects neither results nor counts; a ranking stability test.

**Completion gate.** Permission is applied at query evaluation and refused content is invisible in every observable way.

<a id="rule-wp-19.02"></a>

### WP-19.02 — Citation anchors

**What must be fully done.** Anchors identify a location precisely enough to navigate back to it and remain valid across edits that do not remove the cited content. When the cited content is gone, the anchor reports that state explicitly rather than silently resolving elsewhere.

**Testing requirements.** Anchor survival across insert, delete, reorder and reparent; an explicit-invalid test after content removal.

**Completion gate.** Anchors survive surrounding edits and report invalidity explicitly rather than drifting.

<a id="rule-wp-19.03"></a>

### WP-19.03 — Saved views

**Required design implementation and verification.** Persist notebook scope, query profile, semantic definition bindings and view revision. The initial list projection implements eq/ne/isMissing/isPresent for all declared scalar kinds, all/any/not composition and DocumentId ordering under the same bounds; later value operators and property sorting are explicitly unavailable until the full query package. Full typed query/table delivery is completed in [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28), not silently emulated here.

**What must be fully done.** A saved view is a saved query plus sort and filter configuration, producing a list projection. A saved view does not own documents; deleting it never deletes content.

**Testing requirements.** Ownership test asserting deletion is non-destructive; a re-evaluation test asserting results reflect current content.

**Completion gate.** A saved view owns nothing and always reflects current content.

<a id="rule-wp-19.04"></a>

### WP-19.04 — Non-destructive import

**What must be fully done.** Import from the declared source formats, producing an import plan the user can review, then an import report stating exactly what was created, transformed and skipped. The source is never modified. A partially failed import leaves a coherent result and a clear report, never a half-state presented as success.

**Testing requirements.** Import from every declared source fixture; a source-immutability assertion; an induced-failure test asserting a coherent partial result with a report.

**Completion gate.** Every declared import source has a fixture and imports correctly; the source is never modified; partial failure is reported rather than hidden.

<a id="rule-wp-19.05"></a>

### WP-19.05 — Owner-specific portability

**What must be fully done.** Implement the Notes Cloud-export client over acknowledged source revisions, with authorized Markdown/attachments/metadata and a fidelity report. Offline clipboard/attachment saving and recovery of pending local edits remain ordinary local recovery, not a notebook-export implementation or a complete Cloud snapshot. Assistant-history archive implementation belongs to WP15.06/model05 and is not duplicated here. Use the registered export fixture at this early stage; WP25.08 supplies the real Cloud export join.

**Testing requirements.** Cloud unavailable refuses a new Cloud export without losing local drafts or pending changes; ordinary copy/save recovery remains available for accessible content. Test acknowledged-source snapshot identity, attachment hashes, metadata/link fidelity and complete loss entries. Re-import tests cover only the accepted Markdown/plain-text subset; they must not assert reconstruction of a native archive or pending device-only changes. Distinguish recorded export fixtures here from actual Cloud artifacts at WP25.08.

**Completion gate.** Notes export names its acknowledged Cloud authority, fidelity and completeness; offline recovery is labelled separately, and the real producer join is required at WP25.08. No native Notes archive obligation is introduced.

<a id="rule-wp-19.06"></a>

### WP-19.06 — The repository-projection prohibition

> **This step builds nothing.** It replaces a Git-friendliness step that `§14` of the data-format requirements retired, gates included. A retired delivery still needs an assertion, because the way an excluded feature returns is by a later package quietly adding it.

**What must be fully done.** A structural assertion that **no ArcNotes assembly — and no assembly it references — carries a repository-projection writer, a Git client dependency or an LFS path** (`§14` and [EX-09](../../requirements/13-data-formats-and-portability.md#rule-ex-09) of the data-format requirements). The exclusion is recorded where a reader looks for the feature, so a user asking for a Git-backed notebook gets the stated answer instead of a silent absence ([EE-04](../../requirements/13-data-formats-and-portability.md#rule-ee-04) of the data-format requirements; [EP-05](../../requirements/11-policy-and-configuration.md#rule-ep-05) of the policy requirements).

**Testing requirements.** A dependency-policy test failing the build on a Git or LFS client package reference from any ArcNotes project; a structural test asserting no type implements or is named as a projection writer; a presentation test asserting the excluded capability is explained rather than merely hidden.

**Completion gate.** **No projection path exists and none can be added without failing the build**, and the exclusion is stated to the user rather than left as a gap.

---

<a id="rule-wp-19.90"></a>
### WP-19.90 — Verify the owned artifact and real integration

**What must be fully done.** Preserve lexical search, Markdown/plain-text import and the accepted Cloud export client. Use exact initial query semantics and generated resource/export contracts. No Git mirror, DOCX or newly invented export suite.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Independent import/search/export and missing-resource outcomes; public value profiles and owner authorization remain compatible.

**Completion gate.** Independent import/search/export and missing-resource outcomes; public value profiles and owner authorization remain compatible. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The search index as a derived store with its own lifecycle |
| Protocol | Search and export capabilities become invocable |
| UI | Search surface, saved views, import review and export dialogs |
| Security | Permission-aware querying; import treats source content as untrusted |
| Platform | File dialogs and safe path handling per platform; no Notes printing/PDF-export feature is added |
| Migration | Export format versioning begins |
| Compatibility | The import fixture set fixes the compatibility claims ArcNotes makes |

---

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-19.90](#rule-wp-19.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

**Required evidence addition.** Initial saved-list/missing/case/number vectors and honest unsupported-operator/completeness results.

**Required evidence addition.** [WP-19.05](#rule-wp-19.05) records the carrier/propagation/failure vectors above with payload and manifest hashes; early packages use declared fixtures, while provider/Harness packages require their real integrations.

| Evidence | Produced by |
|---|---|
| Index divergence, rebuild equivalence and latency results | [WP-19.00](#rule-wp-19.00) |
| Filter, permission and ranking results | [WP-19.01](#rule-wp-19.01) |
| Anchor survival and invalidity results | [WP-19.02](#rule-wp-19.02) |
| Saved view ownership and freshness results | [WP-19.03](#rule-wp-19.03) |
| Per-source import results, immutability assertion, partial-failure report | [WP-19.04](#rule-wp-19.04) |
| Cloud export content, attachment-hash, link-manifest and fidelity results | [WP-19.05](#rule-wp-19.05) |
| Dependency-policy, structural and presentation results proving **no repository-projection or Git/LFS path exists** | [WP-19.06](#rule-wp-19.06) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-19.90](#rule-wp-19.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-19.90](#rule-wp-19.90) and all inherited domain-specific gates must pass on the same candidate closure. Independent import/search/export and missing-resource outcomes; public value profiles and owner authorization remain compatible.

**Additional completion requirement.** The initial view stores the final profile and bindings; it neither invents a temporary semantic profile nor claims full table/query delivery before its owning package.

**Additional completion requirement.** The package's content paths pass the stated origin vectors, including unknown input and failed publication; a valid stored/rendered payload alone cannot satisfy the carrier requirement.

**All of the following, with recorded evidence:**

1. The index never diverges after a crash, rebuilds to an equivalent state, and meets query latency budget at scale.
2. Permission is applied during query evaluation; refused content is invisible in results and counts.
3. Citation anchors survive surrounding edits and report invalidity explicitly.
4. A saved view owns no content and always reflects current data.
5. Every declared import source has a fixture, imports correctly, never modifies the source, and reports partial failure honestly — **this is what satisfies [PG-07](../../assurance/open-gates-register.md#rule-pg-07) for ArcNotes**, which is a fixture obligation on *import*, not on export.
6. The export client validates fixture manifests and loss/omission/error presentation here. WP25.08 supplies real Cloud export completeness, including Notes/Chat content, permission and pinning evidence before release.
7. **No repository-projection or Git/LFS path exists in ArcNotes or its dependencies**, the build fails if one is added, and the exclusion is explained rather than hidden.
8. **Search over hydrated content survives a Cloud outage**, and pending work remains durably recoverable. Export is a Cloud operation and is unavailable during an outage, which the interface states rather than failing opaquely.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [NOTES.15](../delivery/lanes/arcnotes.md#task-notes-15) | [WP-19.00](19-arcnotes-search-and-portability.md#rule-wp-19.00) (full) | [NOTES.02](../delivery/lanes/arcnotes.md#task-notes-02) (artifact), [PLT.07](../delivery/lanes/platform.md#task-plt-07) (artifact) |
| [NOTES.16](../delivery/lanes/arcnotes.md#task-notes-16) | [WP-19.01](19-arcnotes-search-and-portability.md#rule-wp-19.01) (full) | [NOTES.07](../delivery/lanes/arcnotes.md#task-notes-07) (artifact) |
| [NOTES.17](../delivery/lanes/arcnotes.md#task-notes-17) | [WP-19.02](19-arcnotes-search-and-portability.md#rule-wp-19.02) (full) | none |
| [NOTES.18](../delivery/lanes/arcnotes.md#task-notes-18) | [WP-19.03](19-arcnotes-search-and-portability.md#rule-wp-19.03) (full - eq/ne/isMissing/isPresent for all declared scalar kinds, all/any/not composition, DocumentId ordering under the profile bounds; later value operators and property sorting explicitly unavailable until [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28))<br>[WP-19](19-arcnotes-search-and-portability.md#rule-wp-19) S8 additional completion requirement: the initial view stores the final profile/bindings; neither invents a temporary semantic profile nor claims full table/query delivery before [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28) (package-level obligation contribution) | [NOTES.07](../delivery/lanes/arcnotes.md#task-notes-07) (artifact), [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract) |
| [NOTES.19](../delivery/lanes/arcnotes.md#task-notes-19) | [WP-19.04](19-arcnotes-search-and-portability.md#rule-wp-19.04) (full) | [NOTES.01](../delivery/lanes/arcnotes.md#task-notes-01) (artifact), [NOTES.02](../delivery/lanes/arcnotes.md#task-notes-02) (artifact), [NOTES.06](../delivery/lanes/arcnotes.md#task-notes-06) (artifact) |
| [NOTES.20](../delivery/lanes/arcnotes.md#task-notes-20) | [WP-19.05](19-arcnotes-search-and-portability.md#rule-wp-19.05) (full - client-side export flow, fidelity manifest, offline-refuses-new-export-without-losing-drafts behaviour)<br>[WP-19](19-arcnotes-search-and-portability.md#rule-wp-19) S6 Impacts: no Notes printing/PDF-export feature is added (package-level obligation contribution) | [NOTES.01](../delivery/lanes/arcnotes.md#task-notes-01) (artifact), [CON.91](../delivery/lanes/contracts.md#task-con-91) (contract), [CON.20](../delivery/lanes/contracts.md#task-con-20) (contract) |
| [NOTES.21](../delivery/lanes/arcnotes.md#task-notes-21) | [WP-19.06](19-arcnotes-search-and-portability.md#rule-wp-19.06) (full) | [GOV.03](../delivery/lanes/governance.md#task-gov-03) (artifact) |
| [NOTES.22](../delivery/lanes/arcnotes.md#task-notes-22) | [WP-19.90](19-arcnotes-search-and-portability.md#rule-wp-19.90) (full) | none |

**Consumers outside this package:** [NOTES.24](../delivery/lanes/arcnotes.md#task-notes-24), [NOTES.26](../delivery/lanes/arcnotes.md#task-notes-26), [NOTES.30](../delivery/lanes/arcnotes.md#task-notes-30), [NOTES.33](../delivery/lanes/arcnotes.md#task-notes-33), [REL.01](../delivery/lanes/release.md#task-rel-01).

<!-- delivery-graph:end -->

