<a id="rule-wp-28"></a>

# WP-28 — ArcNotes Bounded Properties and Saved Views

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: F — ArcNotes completion
> Upstream: `19`, `25` · Downstream: `50`

> **Goal.** Add **bounded** typed properties, queries and saved **list and table** views — the depth [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) retains — without turning ArcNotes into a database platform and without making a plain note heavier.

> **Scope amendment, 2026-09-06 ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)).** Board, gallery, calendar and timeline layouts, formula evaluation, relation and rollup engines are **excluded from delivery**, with no mandatory future hook. Required depth is common scalar property types plus saved list and table views with filtering and sorting.

---

## 1. Scope and purpose

**In scope.** Typed property definitions and values; the query model; saved list and table projections; view configuration; and compatibility for shipped scalar-property/list/table schemas.

**Out of scope.** Slides and canvas (retired). A general relational engine — explicitly a non-goal. Cross-workspace queries.

**Why this package exists.** `I2 §III.7` places database views after typed properties, queries and saved views exist, because a view is a projection over a query and building views first would fabricate a parallel data model.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| **[D-006](../../decisions/phase-1-foundation-decisions.md#rule-d-006)** | Phased full inclusion, of which this is the second phase |
| `I2 §III.7` | The ordering: properties and queries before views |
| [`../../requirements/products/arcnotes.md`](../../requirements/products/arcnotes.md) | Property, tag, view and non-goal statements |
| [WP-18](18-arcnotes-document-core.md#rule-wp-18), [WP-19](19-arcnotes-search-and-portability.md#rule-wp-19), [WP-27](27-arcnotes-edgeless-canvas.md#rule-wp-27) output | Properties, search, saved views and unified content semantics |

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
| `src/ArcNotes/ArcNotes.Search/` | Query evaluation extended with property predicates and sorting |
| `src/ArcNotes/ArcNotes.Infrastructure/` | Property indexes and the schema migration |
| `src/ArcNotes/ArcNotes.Presentation/` | **Table and list** view surfaces only ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)) |
| `fixtures/formats/arcnotes/v3/` | The views-era fixture, with V1 and V2 retained |
| `tests/ArcNotes.Tests.Integration/` | Query, view, migration and performance suites |

**Major types introduced.** `PropertySchema`, `PropertyType`, `PropertyIndex`, `Query`, `QueryPredicate`, `QuerySort`, `ViewDefinition`, `ViewKind`, `ViewConfiguration`, `Projection`, `GroupingRule`.

---

## 5. Required implementation work

<a id="rule-wp-28.00"></a>

### WP-28.00 — Typed property schemas

**What must be fully done.** Property definitions with **bounded scalar types only** — text, number, date, select, multi-select, checkbox ([P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)). **`relation` and `derived` are excluded**: a relation type implies a join engine and a derived type implies a formula evaluator, and both are outside the delivered scope. With validation and defaults. System properties are separate. A property definition has a lifecycle: creation, rename, type change with a stated migration behaviour, and deletion with a stated consequence.

**Testing requirements.** Type validation per kind; a rename test asserting values are preserved; a type-change test asserting the stated behaviour; a deletion test asserting the stated consequence.

**Completion gate.** Every property type validates, and rename, type change and deletion behave as stated with no silent data loss.

<a id="rule-wp-28.01"></a>

### WP-28.01 — Query model

**What must be fully done.** A query with predicates over properties, tags, links, content and structure, with sorting and grouping. Permission is applied during evaluation. Query results are stable and paginated for large result sets.

**Testing requirements.** Predicate coverage; a permission test asserting refused documents affect neither results nor counts; stability under concurrent mutation.

**Completion gate.** Queries evaluate with permission applied and remain stable under concurrent mutation.

<a id="rule-wp-28.02"></a>

### WP-28.02 — View kinds

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

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Property indexes and schema version 3 |
| Protocol | Query and view definitions in export and sync |
| UI | Four view surfaces and a property editing experience |
| Security | Query-time permission and view-edit permission |
| Platform | View rendering performance per platform |
| Migration | Third schema version with two retained prior fixtures |
| Compatibility | V1, V2 and V3 all readable |

---

## 7. Tests and verification evidence

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

- [19 — ArcNotes Search, Import, Export and Portability](19-arcnotes-search-and-portability.md)
- [25 — Sync Engine and Blob Lifecycle](25-sync-engine-and-blob-lifecycle.md)

**Downstream — these consume this package’s completed output.**

- [50 — Full-Platform Production Release](50-full-platform-production-release.md)
