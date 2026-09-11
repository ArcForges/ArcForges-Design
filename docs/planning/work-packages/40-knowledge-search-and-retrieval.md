<a id="rule-wp-40"></a>

# WP-40 — Knowledge, Search and Retrieval

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `19`, `25`, `28`, `43`, `44` · Downstream: `50`, `52`

> **Goal.** Build the retrieval layer on top of search: knowledge sources, scopes, indexes as derived projections, hybrid retrieval with budgets, permission-aware assembly, and evidence with citations that anchor back to real content.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud search authority; AI model adapter; clients. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Knowledge sources and their registration; knowledge scopes and the five-dimension policy model; indexes as derived projections including semantic indexes; hybrid retrieval with explicit budgets; permission-aware retrieval; evidence and citation assembly; retrieval scope as a privacy boundary; and cloud search where entitlement permits.

**Out of scope.** Model interaction and economics (`43`). Product-specific search surfaces, which each product owns.

**Why this package exists.** [the mock policy](../implementation-sequence.md#3-what-may-be-mocked-and-what-may-not) permits cloud search to be mocked but requires local full-text indexing and citation anchors to be real. Retrieval is what turns those into AI-usable evidence, and it is the point where a privacy boundary is either enforced or silently crossed.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

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

| Owner / location | Deliverable |
|---|---|
| Cloud: src/Cloud/ArcForges.Cloud.Modules.Search/ | Permission-filtered source/query/index state, queued inference jobs and published derived results |
| AI: src/inference/ | Bounded Workers AI embedding/reranking adapter using the selected job ports; no planner |
| AI: src/workflows/RunWorkflow.ts | Consumes authorized context refs/results for the sole Harness |
| Each desktop product: its own index/source and LocalRpc adapters | Real local lexical/source behavior, exact citations and owner permissions |
| Contracts: public generated Search/knowledge records | The selected SearchQuery and immutable source/result profile |
| Owner tests and Cloud integration suite | Real CF job/usage/index/revoke/rebuild, local source and citation tests |

No shared mechanism package owns product knowledge policy, authorization or persistence behavior.

---

## 5. Required implementation work

<a id="rule-wp-40.00"></a>

### WP-40.00 — Knowledge sources and scopes

**What must be fully done.** Products register knowledge sources with their content kinds and permission model. Scopes compose sources into what a given retrieval may see, governed by the five-dimension policy model. Scope membership is visible to the user before retrieval runs.

**Testing requirements.** Source registration and scope composition tests; a visibility test; a policy-dimension coverage test.

**Completion gate.** Scope membership is explicit and visible before retrieval, with every policy dimension represented.

<a id="rule-wp-40.01"></a>

### WP-40.01 — Indexes as derived projections


**What must be fully done.** Implement lexical and semantic derived index lifecycle owned by Search, keyed by source version/hash, permission scope, model/profile/dimension and config version. Use the selected C# inference job outbox and CF embedding ports; publish only complete validated 1024-dimension results after the shared Search/Commerce outcome receipt, retaining any unresolved supplier liability. Stale/revoked/deleted source results are discarded and indexes rebuild from authorized source.

**Testing requirements.** Real bge-m3 embedding job with immutable source pins, partial/duplicate/unknown usage, crash before result publication, model/profile change and full rebuild; no source mutation or duplicate debit.

**Completion gate.** Semantic readiness is explicit and derived; keyword search remains available when CF/semantic indexing fails.

<a id="rule-wp-40.02"></a>

### WP-40.02 — Hybrid retrieval and budgets


**What must be fully done.** Implement the selected general SearchQuery lexical/metadata/semantic/hybrid modes and bounded retrieval budgets. Use permission-filtered lexical/vector candidates, the [retrieval.hybrid.v1](../../architecture/data-model/03-derived-stores.md#selected-retrieval-profile-retrievalhybridv1) ranking/tie-break and typed budget rules and the declared rerank inference job when enabled; no dynamic provider selection. Disclose truncation and retain source/model/config pins.

**Testing requirements.** Stable query/input/index vectors, ties, over-budget candidate set, actual reranker and unavailable/unknown provider outcomes; use the independent RRF60/exact/tie/dedup/source-cap vectors from the authority.

**Completion gate.** The selected ranked result semantics and fallback are reproducible within their fixed profile; no unauthorized or unaccounted candidate influences output.

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


**What must be fully done.** Run Cloud search only on authorized synced sources and current entitlement. Implement inference-input/outcome/state receipts, queue limits and selected funding policy through WP43; Search jobs use the enumerated admission/outcome transactions and existing operator supplier budgets, with no customer capacity reservation, settlement or credit debit. Implement the source/version/lease/receipt fields from the canonical Search record. Preserve independent local lexical/scalar search.

**Testing requirements.** Actual C#→CF inference→C# outcome/index publication and usage ledger; service expiry, revoked source and Cloud/CF loss with local search still usable.

**Completion gate.** Cloud semantic/rerank is operationally complete without a second Harness or an AOT-incompatible C# model adapter.

<a id="rule-wp-40.90"></a>
### WP-40.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Keep lexical/scalar/source authorization in their owners; bind embedding/model calls to selected Workers AI and the internal integration contract. Implement index/version/backfill and citation/content-origin behavior from the frozen design.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28) precedes full retrieval; permission-at-query, deletion/revocation, exact scalar filtering and independent retrieval/embedding-version fixtures remain.

**Completion gate.** [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28) precedes full retrieval; permission-at-query, deletion/revocation, exact scalar filtering and independent retrieval/embedding-version fixtures remain. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-40.90](#rule-wp-40.90) and all inherited domain-specific gates must pass on the same candidate closure. [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28) precedes full retrieval; permission-at-query, deletion/revocation, exact scalar filtering and independent retrieval/embedding-version fixtures remain.

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

- [WP-19](19-arcnotes-search-and-portability.md#rule-wp-19)
- [WP-25](25-sync-engine-and-blob-lifecycle.md#rule-wp-25)
- [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28)
- [WP-43](43-managed-ai-routing-and-metering.md#rule-wp-43)
- [WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44)

**Downstream — consumers of these released outputs.**

- [WP-50](50-full-platform-production-release.md#rule-wp-50)
- [WP-52](52-cloud-harness.md#rule-wp-52)


---
