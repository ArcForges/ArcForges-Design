<a id="rule-wp-40"></a>

# WP-40 — Knowledge, Search and Retrieval

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `19`, `25`, `28`, `43`, `44` · Downstream: `50`, `52`

> **Goal.** Build the retrieval layer on top of search: knowledge sources, scopes, indexes as derived projections, hybrid retrieval with budgets, permission-aware assembly, and evidence with citations that anchor back to real content.

---

## 1. Scope and purpose

**In scope.** Knowledge sources and their registration; knowledge scopes and the five-dimension policy model; indexes as derived projections including semantic indexes; hybrid retrieval with explicit budgets; permission-aware retrieval; evidence and citation assembly; retrieval scope as a privacy boundary; and cloud search where entitlement permits.

**Out of scope.** Model interaction and economics (`43`). Product-specific search surfaces, which each product owns.

**Why this package exists.** [the mock policy](../implementation-sequence.md#3-what-may-be-mocked-and-what-may-not) permits cloud search to be mocked but requires local full-text indexing and citation anchors to be real. Retrieval is what turns those into AI-usable evidence, and it is the point where a privacy boundary is either enforced or silently crossed.

---

## 2. Required inputs and dependencies

**Frozen design input.** [notes.scalar.v1](../../requirements/products/arcnotes.md#notes-scalar-query-profile) and completed [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28) evaluators

Cloud embeddings/retrieval consume operator-funded provider adapters and admission from [WP-43](43-managed-ai-routing-and-metering.md#rule-wp-43) and the policy resolver from WP-44. Local text indexing was already completed in [WP-19](19-arcnotes-search-and-portability.md#rule-wp-19); it does not substitute for the Cloud semantic path.

| Input | Why it matters |
|---|---|
| [`../../requirements/06-knowledge-search-and-retrieval.md`](../../requirements/06-knowledge-search-and-retrieval.md) | The full chain from knowledge source to AI context, and the privacy boundary |
| [`../../architecture/09-ai-and-agent-runtime-architecture.md`](../../architecture/09-ai-and-agent-runtime-architecture.md) `§5` | Context assembly, scope resolution and cache isolation |
| [WP-19](19-arcnotes-search-and-portability.md#rule-wp-19), [WP-25](25-sync-engine-and-blob-lifecycle.md#rule-wp-25) output | The local index with citation anchors, and synced content |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **`Search ≠ Retrieval`.** Search serves a person; retrieval assembles evidence for a model. |
| BR-02 | **An index is a derived projection**; deleting it rebuilds and never loses knowledge. |
| BR-03 | **Retrieval is permission-aware at assembly**, not filtered afterwards. |
| BR-04 | **Retrieval scope is a privacy boundary.** What a model can see is an explicit, visible decision, never an implicit consequence of having an index. |
| BR-05 | **Evidence carries citations** that anchor back to real content and report explicitly when the anchor is no longer valid. |
| BR-06 | **A retrieval budget is explicit**: token, item and latency budgets bound assembly, and exceeding them truncates with disclosure rather than silently. |
| BR-07 | **Local-only content stays local**; enabling AI never uploads content the user kept local ([I-182](../../requirements/01-normative-glossary-and-invariants.md#rule-i-182)). |
| BR-08 | **Cache is isolated per scope and per principal**; one user's retrieval cache never serves another. |
| BR-09 | **A semantic index over user content is subject to the same permission and scope rules** as the content itself. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/BuildingBlocks/ArcForges.Knowledge/` | Knowledge source registry, scope resolution, retrieval pipeline, evidence assembly |
| `src/BuildingBlocks/ArcForges.Knowledge.Index/` | Index abstraction with lexical and semantic implementations, rebuild semantics |
| `src/Cloud/ArcForges.Cloud.Modules.Search/` | Cloud index and query, entitlement-gated |
| `src/Cloud/ArcForges.Cloud.AgentRuntime/` | Retrieval integration into authoritative Cloud context assembly |
| `src/*/[Product].LocalRpc/` | Each product registers its knowledge sources |
| `tests/KnowledgeRetrievalTests/` | Permission, budget, citation, isolation and rebuild suites |

**Major types introduced.** `KnowledgeSource`, `KnowledgeScope`, `KnowledgePolicy`, `IndexProjection`, `RetrievalRequest`, `RetrievalBudget`, `RetrievalResult`, `Evidence`, `Citation`, `CitationAnchorState`, `ContextAssembly`, `RetrievalCacheKey`.

---

## 5. Required implementation work

<a id="rule-wp-40.00"></a>

### WP-40.00 — Knowledge sources and scopes

**What must be fully done.** Products register knowledge sources with their content kinds and permission model. Scopes compose sources into what a given retrieval may see, governed by the five-dimension policy model. Scope membership is visible to the user before retrieval runs.

**Testing requirements.** Source registration and scope composition tests; a visibility test; a policy-dimension coverage test.

**Completion gate.** Scope membership is explicit and visible before retrieval, with every policy dimension represented.

<a id="rule-wp-40.01"></a>

### WP-40.01 — Indexes as derived projections

**What must be fully done.** Lexical and semantic indexes as derived stores with full rebuild semantics. An index update follows the write path so it cannot diverge. Semantic index content is subject to the same permission rules as its source.

**Testing requirements.** Rebuild equivalence for each index kind; divergence test after a crash mid-update; a permission test over the semantic index.

**Completion gate.** Every index rebuilds to an equivalent state and cannot diverge after a crash; semantic content honours source permission.

<a id="rule-wp-40.02"></a>

### WP-40.02 — Hybrid retrieval and budgets

**What must be fully done.** Retrieval combining lexical and semantic signals with explicit token, item and latency budgets. Exceeding a budget truncates with disclosure. Retrieval is deterministic given the same inputs and index state.

**Testing requirements.** Budget enforcement per dimension; a truncation-disclosure assertion; a determinism test.

**Completion gate.** Budgets are enforced with disclosure, and retrieval is deterministic given fixed inputs.

<a id="rule-wp-40.03"></a>

### WP-40.03 — Permission-aware assembly

**What must be fully done.** Permission applied during retrieval so that refused content never enters candidate sets, never influences ranking, and never appears in counts. A permission change mid-assembly is honoured.

**Testing requirements.** A permission matrix; a ranking-influence test; a mid-assembly revocation test.

**Completion gate.** Refused content never influences results, ranking or counts, and mid-assembly revocation is honoured.

<a id="rule-wp-40.04"></a>

### WP-40.04 — Evidence and citations

**What must be fully done.** Retrieved material becomes evidence with citations anchored to real locations. A citation resolves back to the exact content; when the anchor is no longer valid it says so explicitly rather than resolving elsewhere.

**Testing requirements.** Citation resolution tests; anchor-invalidation tests after edits and deletions; a cross-product citation test.

**Completion gate.** Every citation resolves exactly or reports invalidity explicitly, across products.

<a id="rule-wp-40.05"></a>

### WP-40.05 — Privacy boundary and cache isolation

**What must be fully done.** The retrieval scope is presented as a privacy decision the user makes. Local-only content is never uploaded by enabling AI. Retrieval caches are keyed by scope and principal, with no cross-principal reuse.

**Testing requirements.** A local-only upload negative test; a cache-isolation test across principals and scopes; a scope-visibility test.

**Completion gate.** **Enabling AI never uploads local-only content**, and no retrieval cache entry is ever reused across principals or scopes.

<a id="rule-wp-40.06"></a>

### WP-40.06 — Cloud search

**Required design implementation and verification.** Reuse the completed scalar query semantics for the Notes filter on search.query. Compare with native cache on an identical authorized fully hydrated acknowledged dataset; preserve other search ranking modes and explicit local/Cloud completeness. Do not create a second collation or scalar evaluator profile.

**What must be fully done.** Cloud-side indexing and query over synced content, entitlement-gated, with the same permission model. Cloud search degradation never breaks local search.

**Testing requirements.** Entitlement-gating tests; a cloud-outage test asserting local search is unaffected; a parity test on permission behaviour.

**Completion gate.** Cloud search is entitlement-gated, applies the same permission model, and its outage never affects local search.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Index projections local and cloud-side, all derived |
| Protocol | Knowledge source, scope and retrieval contracts |
| UI | Scope selection, evidence display and citation navigation |
| Security | Retrieval scope as a privacy boundary; cache isolation |
| Platform | Index size and rebuild cost per platform |
| Migration | Index formats are derived and rebuildable, never migrated |
| Compatibility | Citation anchor format enters the compatibility window |

---

## 7. Tests and verification evidence

**Required evidence addition.** Notes typed-filter real Cloud/local equivalence and cursor restart tests consuming the completed query engine.

| Evidence | Produced by |
|---|---|
| Scope composition, visibility and policy coverage results | [WP-40.00](#rule-wp-40.00) |
| Index rebuild equivalence and divergence results | [WP-40.01](#rule-wp-40.01) |
| Budget enforcement, disclosure and determinism results | [WP-40.02](#rule-wp-40.02) |
| Permission matrix, ranking-influence and revocation results | [WP-40.03](#rule-wp-40.03) |
| Citation resolution and invalidation results | [WP-40.04](#rule-wp-40.04) |
| Local-only negative test and cache isolation results | [WP-40.05](#rule-wp-40.05) |
| Entitlement gating and cloud-outage independence results | [WP-40.06](#rule-wp-40.06) |

---

## 8. Completion gate

**Additional completion requirement.** Cloud retrieval consumes the existing scalar semantics; no product comparison behavior is left to the search implementation.

**All of the following, with recorded evidence:**

1. Scope membership is explicit and visible before retrieval, with every policy dimension represented.
2. Every index rebuilds to an equivalent state, cannot diverge after a crash, and honours source permission for semantic content.
3. Retrieval budgets are enforced with disclosure; retrieval is deterministic given fixed inputs.
4. Refused content never influences results, ranking or counts; mid-assembly revocation is honoured.
5. Every citation resolves exactly or reports invalidity explicitly, across products.
6. **Enabling AI never uploads local-only content**; no retrieval cache entry is reused across principals or scopes.
7. Cloud search is entitlement-gated, applies the same permission model, and its outage never affects local search.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [28 — ArcNotes Bounded Properties and Saved Views](28-arcnotes-properties-and-views.md)

- [19 — ArcNotes Search, Import, Export and Portability](19-arcnotes-search-and-portability.md)
- [25 — Sync Engine and Blob Lifecycle](25-sync-engine-and-blob-lifecycle.md)
- [43 — Cloud AI Routing, Metering and Settlement](43-managed-ai-routing-and-metering.md)
- [44 — Dynamic Policy and Configuration Control Plane](44-dynamic-policy-and-configuration.md)

**Downstream — these consume this package’s completed output.**

- [50 — Full-Platform Production Release](50-full-platform-production-release.md)
- [52 — The Cloud Harness](52-cloud-harness.md)
