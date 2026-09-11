<a id="rule-wp-28"></a>

# WP-28 — ArcNotes Bounded Properties and Saved Views

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: F — ArcNotes completion
> Upstream: `19`, `25` · Downstream: `40`, `50`

> **Goal.** Add **bounded** typed properties, queries and saved **list and table** views — the depth [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) retains — without turning ArcNotes into a database platform and without making a plain note heavier.

> **Scope amendment, 2026-09-06 ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)).** Board, gallery, calendar and timeline layouts, formula evaluation, relation and rollup engines are **excluded from delivery**, with no mandatory future hook. Required depth is common scalar property types plus saved list and table views with filtering and sorting.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: ArcNotes + Cloud; Contracts profile. Inputs: exact compatible Contracts packages/descriptors and applicable DesktopPlatform packages; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: Native AOT candidate packages/executables with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Typed property definitions and values; the query model; saved list and table projections; view configuration; and compatibility for shipped scalar-property/list/table schemas.

**Out of scope.** Slides and canvas (retired). A general relational engine — explicitly a non-goal. Cross-workspace queries.

**Why this package exists.** The work in section 5 establishes typed schemas and the query model before list/table projections, because a view is a projection over a query and building views first would fabricate a parallel data model. The [ArcNotes property and view requirements](../../requirements/products/arcnotes.md#7-properties-tags-and-views) define the accepted behavior.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

**Frozen design input.** [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile) and [NotesQuery](../../architecture/contracts/02-local-rpc-operations.md#notes-query-contract)

| Input | Why it matters |
|---|---|
| **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** as amended by **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** | Notebook core plus bounded properties and list/table views; canvas, slides and advanced database engines are excluded |
| [Property storage](../../architecture/data-model/02-desktop-data-model.md#property_definition-property_value), [saved-view storage](../../architecture/data-model/02-desktop-data-model.md#saved_view) and [typed property mutation](../../architecture/contracts/02-local-rpc-operations.md#rule-no-06) | Persist declared scalar properties and query projections; edits use the same revision and permission path as document edits |
| [`../../requirements/products/arcnotes.md`](../../requirements/products/arcnotes.md) | Property, tag, view and non-goal statements |
| [WP-18](18-arcnotes-document-core.md#rule-wp-18), [WP-19](19-arcnotes-search-and-portability.md#rule-wp-19) and [WP-25](25-sync-engine-and-blob-lifecycle.md#rule-wp-25) output | Document/property foundations, search and saved list queries, and the real Cloud revision/sync path |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **ArcNotes does not become a relational database clone.** A view is a projection over a query, not a table with foreign keys. **No formula, relation or rollup evaluator is built** ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)), and no expression language reaches the filter path ([NO-06](../../architecture/contracts/02-local-rpc-operations.md#rule-no-06) of the local RPC contract). |
| BR-02 | **A document table block is a document table**, not a database view. The two remain distinct concepts. |
| BR-03 | **Properties must not make plain notes heavy.** A note with no properties has no property overhead and no property UI imposed. |
| BR-04 | **System properties and user properties are separated** and never conflated. |
| BR-05 | **A view owns no documents.** Deleting a view never deletes content (`BR` in [WP-19.03](19-arcnotes-search-and-portability.md#rule-wp-19.03)). |
| BR-06 | **Backward compatibility applies to actually shipped supported Notes schemas**, without inventing a canvas-era native package. |
| BR-07 | **A query is evaluated with permission applied**, exactly as search is. |
| BR-08 | **View performance is budgeted** on the scale corpus; a large result set virtualises rather than degrading. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/ArcNotes/ArcNotes.Domain/` | Property definition and value model extended to typed schemas |
| `src/ArcNotes/ArcNotes.Database/` | Query model, view definitions, view configuration, projections |
| `src/ArcNotes/ArcNotes.Search/` and Cloud Notes/Search query adapters | Native and Cloud evaluators of the same scalar profile, with common conformance vectors and permission/dataset binding |
| `src/ArcNotes/ArcNotes.Infrastructure/` | Property indexes and the schema migration |
| `src/ArcNotes/ArcNotes.Presentation/` | **Table and list** view surfaces only ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)) |
| `fixtures/formats/arcnotes/` | Supported shipped schema fixtures plus notes.scalar.v1 conformance vectors; no invented historical versions |
| `tests/ArcNotes.Tests.Integration/` | Query, view, migration and performance suites |

**Major types introduced.** `PropertySchema`, `PropertyType`, `PropertyIndex`, `Query`, `QueryPredicate`, `QuerySort`, `ViewDefinition`, `ViewKind`, `ViewConfiguration`, `Projection`, `QueryProfile`, `QueryDatasetToken`.

---

## 5. Required implementation work

<a id="rule-wp-28.00"></a>

### WP-28.00 — Typed property schemas

**Required design implementation and verification.** Implement all eight declared scalar kinds/config bounds and exact encodings. Rename preserves semantic bindings; dependent type/option changes are refused after the required preview; trashed definitions make views visibly invalid.

**What must be fully done.** Property definitions with **bounded scalar types only** — text, number, date/date-time, single-select, multi-select, checkbox and URL, as specified by the [ArcNotes property requirements](../../requirements/products/arcnotes.md#7-properties-tags-and-views). **`relation` and `derived` are excluded**: a relation type implies a join engine and a derived type implies a formula evaluator, and both are outside the delivered scope. Validation follows the scalar profile; missing values receive no implicit default. System properties are separate. A property definition has a lifecycle: creation, rename, type change with a stated migration behaviour, and deletion with a stated consequence.

**Testing requirements.** Type validation per kind; a rename test asserting values are preserved; a type-change test asserting the stated behaviour; a deletion test asserting the stated consequence.

**Completion gate.** Every property type validates, and rename, type change and deletion behave as stated with no silent data loss.

<a id="rule-wp-28.01"></a>

### WP-28.01 — Query model

**Required design implementation and verification.** Implement every v1 operator, boolean/missing behavior, AST limit, ordinal/decimal/instant comparison and signed dataset-bound pagination exactly as defined. Use one semantic conformance suite against native cache and Cloud evaluators; storage/index algorithms may differ.

**What must be fully done.** A query with predicates over properties, tags, links, content and structure, with the declared stable sorting and scalar query profile. Permission is applied during evaluation. Query results are stable and paginated for large result sets.

**Testing requirements.** Predicate coverage; a permission test asserting refused documents affect neither results nor counts; stability under concurrent mutation.

**Completion gate.** Queries evaluate with permission applied and remain stable under concurrent mutation.

<a id="rule-wp-28.02"></a>

### WP-28.02 — View kinds

**Required design implementation and verification.** List and table share identical query ordering with missing last and ascending DocumentId tie-break. Commit the D1–D4, numeric/checkbox/offset, equal-key and mutation-restart vectors, including two-page comparisons and declared partial hydration.

**What must be fully done.** **Table and list** views as projections over a query, each with its own configuration — visible properties, sorting and filtering over scalar properties ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)). **Board, gallery, calendar and timeline layouts are excluded**, and no grouping engine that presupposes them is built. A view kind change preserves the underlying query.

**Testing requirements.** Per-kind rendering and interaction tests; a kind-switch test asserting query preservation; an ownership test asserting deletion is non-destructive.

**Completion gate.** Every view kind projects the same query correctly, switching kinds preserves the query, and deleting a view destroys nothing.

<a id="rule-wp-28.03"></a>

### WP-28.03 — Editing through a view

**What must be fully done.** Property values are editable in a view, with edits going through the same write path as document editing, producing revisions on the underlying documents. A view edit is never a shortcut that bypasses validation or permission.

**Testing requirements.** Write-path assertion for view edits; a validation test; a permission test.

**Completion gate.** View edits use the single write path with full validation and permission.

<a id="rule-wp-28.04"></a>

### WP-28.04 — Lightness preservation

**What must be fully done.** A plain note remains plain: no property panel imposed, no schema required, no performance cost. The property system is opt-in per document and per collection.

**Testing requirements.** A default-experience test asserting a new note requires nothing; a performance comparison asserting no regression for property-free documents.

**Completion gate.** A plain note has no imposed property surface and no measurable performance cost.

<a id="rule-wp-28.05"></a>

### WP-28.05 — Supported-schema migration and export fidelity

**What must be fully done.** Migrate actual shipped scalar-property/list/table schemas, preserving stable IDs and additive fields. Cloud export includes declared property/view metadata and a fidelity report. No canvas-era fixture, native Notes package, formula/relation engine or lossless export/re-import contract is required.

**Testing requirements.** Upgrade historical supported schemas; read additive unknown fields; export through the real [WP-25.08](25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) producer and verify declared values/metadata/omissions.

**Completion gate.** Supported data survives schema upgrade and Cloud export describes its fidelity accurately; no excluded product feature is reintroduced by a compatibility test.

<a id="rule-wp-28.06"></a>

### WP-28.06 — Scale

**What must be fully done.** Large collections with many properties and large result sets remain responsive through virtualisation and indexing. Memory stays within the product ceiling.

**Testing requirements.** Scale corpus measurements per view kind; memory ceiling assertion; a soak test on a large view.

**Completion gate.** Every view kind meets responsiveness and memory budgets on the scale corpus.

---

<a id="rule-wp-28.90"></a>
### WP-28.90 — Verify the owned artifact and real integration

**What must be fully done.** Keep scalar properties, list/table projections and the full `notes.scalar.v1` evaluator semantics. Bind field/presence/order/cursor rules to proto and the TS public representation.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Independent local/Cloud query vectors, null/missing/invalid values, sorting/tie-breaks and snapshot pagination. Keep the producer edge to WP-40.

**Completion gate.** Independent local/Cloud query vectors, null/missing/invalid values, sorting/tie-breaks and snapshot pagination. Keep the producer edge to WP-40. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Property indexes, query profile/semantic revision fields and the next actual schema migration |
| Protocol | Query and view definitions in export and sync |
| UI | Two view surfaces (list and table) and a property editing experience |
| Security | Query-time permission and view-edit permission |
| Platform | View rendering performance per platform |
| Migration | Migration from each supported shipped schema, preserving unknown metadata |
| Compatibility | All supported shipped schemas and known query profiles readable; unknown query profiles preserved but not executed |

---

## 7. Tests and verification evidence

**Required evidence addition.** Complete Cloud/local match-set, sort and page equality on identical authorized fully hydrated revisions, plus all profile boundary/rename/type-change/unknown-version tests.

| Evidence | Produced by |
|---|---|
| Property lifecycle results with no silent loss | [WP-28.00](#rule-wp-28.00) |
| Query permission and stability results | [WP-28.01](#rule-wp-28.01) |
| Per-kind projection, switch and ownership results | [WP-28.02](#rule-wp-28.02) |
| View-edit write-path, validation and permission results | [WP-28.03](#rule-wp-28.03) |
| Lightness default and performance comparison | [WP-28.04](#rule-wp-28.04) |
| Supported-schema migration and Cloud-export fidelity results | [WP-28.05](#rule-wp-28.05) |
| Scale corpus and soak results per view kind | [WP-28.06](#rule-wp-28.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-28.90](#rule-wp-28.90) and all inherited domain-specific gates must pass on the same candidate closure. Independent local/Cloud query vectors, null/missing/invalid values, sorting/tie-breaks and snapshot pagination. Keep the producer edge to WP-40.

**Additional completion requirement.** Every scalar/query/profile vector passes on both owners; all supported list/table operations are implemented without new product design choices.

**All of the following, with recorded evidence:**

1. Every property type validates; rename, type change and deletion behave as stated with no silent data loss.
2. Queries evaluate with permission applied and remain stable under concurrent mutation.
3. Every view kind projects the same query correctly; switching kinds preserves the query; deleting a view destroys nothing.
4. View edits use the single write path with full validation and permission.
5. **A plain note has no imposed property surface and no measurable performance cost.**
6. Supported scalar/list/table schema fixtures remain readable; Cloud export declares metadata and losses without promising native re-import.
7. Every view kind meets responsiveness and memory budgets on the scale corpus.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [19 arcnotes search and portability](19-arcnotes-search-and-portability.md#rule-wp-19)
- [25 sync engine and blob lifecycle](25-sync-engine-and-blob-lifecycle.md#rule-wp-25)

**Downstream — consumers of these released outputs.**

- [40 knowledge search and retrieval](40-knowledge-search-and-retrieval.md#rule-wp-40)
- [50 full platform production release](50-full-platform-production-release.md#rule-wp-50)

---
