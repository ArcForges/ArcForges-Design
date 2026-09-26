<a id="rule-wp-40"></a>
# WP-40 — Application-Scoped Knowledge Search and Retrieval

> Status: Authoritative — [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).
> Repositories: Cloud + AI + DesktopPlatform. Consume only exact published upstream artifacts; no adjacent sources.

## 1. Scope and purpose

Deliver the complete owned behavior below under the [current project/package plan](../../architecture/27-platform-projects-and-application-assistants.md). Professional product semantics, security, exact values and recovery requirements remain binding. A completed Hello World or fixture cannot substitute for the listed production capability.

## 2. Required inputs and dependencies

[Producer registry](../producer-artifacts-and-integration.md), [wire registry](../../architecture/contracts/04-protobuf-wire-registry.md), [application/protocol profile](../../architecture/contracts/10-application-scope-and-streams.md), [D1 execution](../../architecture/data-model/04-d1-execution-profile.md), [history](../../architecture/data-model/05-application-history.md), [experience/acceptance](../../experience/README.md) and exact artifacts from the upstream WPs above. Later domain/AI fixtures are allowed only where explicitly named below and must be removed at their owning real integration gate.

## 3. Binding rules and decisions

Own-application composition and state, public binary gRPC-Web, helper-only local RPC, fixed D1 atomic plans, no hidden cross-product dependency. Use existing command/revision/permission/effect/format profiles. All necessary product behavior is fixed in the linked authorities; private helper implementation choices remain within those constraints.


## 4. Projects, directories, files and major types affected

Use the exact projects assigned to this WP in [architecture 27](../../architecture/27-platform-projects-and-application-assistants.md#2-desktopplatform-tree-and-actual-projects) and its product/Cloud/Mobile trees. Implement their owned named services, typed records, schema migrations and tests; do not introduce a new repository, generic SQL facade or shared runtime to connect them. Versioned generated schema definitions remain in Contracts.

## 5. Required implementation work

<a id="rule-wp-40.00"></a>
### WP-40.00 — Source ownership

**What must be fully done.** Admit own-product content, explicitly selected uploads and authorized web sources; preserve source origin/egress and consent.

**Testing requirements.** Other-product/realm/private resource rejected before snippets/context.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-40.01"></a>
### WP-40.01 — Scoped derived index production

**What must be fully done.** Implement D1 FTS scoped queries and Vectorize per-workspace namespaces with mandatory realm/product/model-generation filters per model 04 §8. Preserve source revision/policy checks and rebuild pointers.

**Testing requirements.** Cross-product/tenant isolation before topK, stale deletion, unavailable canonical owner, lexical fallback and [L-16](../../assurance/release-gates.md#rule-l-16) index/namespace footprint.

**Completion gate.** No global vector query followed only by UI filtering; measured index limits match the capacity profile.

<a id="rule-wp-40.02"></a>
### WP-40.02 — Hybrid retrieval and budgets

**What must be fully done.** Preserve ranking/retrieval/embedding limits and exact Notes scalar comparator; vector score never changes business ordering.

**Testing requirements.** Budget bounds, multilingual/no-match/partial and exact decimal vectors.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-40.03"></a>
### WP-40.03 — Current permission

**What must be fully done.** Recheck current source owner permission and revision after candidate retrieval, before counts/snippets/citations.

**Testing requirements.** Revocation during query and stale index cannot expose content.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-40.04"></a>
### WP-40.04 — Evidence and citations

**What must be fully done.** Retain source kind, immutable reference, anchor, uncertainty/completeness and measurement/media precision.

**Testing requirements.** Stale/missing source labels and no fabricated citation.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-40.05"></a>
### WP-40.05 — Privacy and caches

**What must be fully done.** Partition cache/history/context by product/profile; temporary/local Cloud-processing content never enters Cloud search.

**Testing requirements.** Marker test, cross-app/account leakage and purge.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-40.06"></a>
### WP-40.06 — Real Cloud query path

**What must be fully done.** Use Workers AI embeddings/reranker and actual D1/Vectorize with C# owner filtering; fixture joins remain named until real provider gate.

**Testing requirements.** Real compatible client/owner/index versions and explicit lexical-only degradation.

**Completion gate.** The stated behavior and oracle pass using the actual owned implementation. Evidence names source commit, artifact versions/hashes, environment and any later fixture replacement.

<a id="rule-wp-40.90"></a>
### WP-40.90 — Owned artifacts and real integration

**What must be fully done.** Complete every preceding substep, build/pack once, consume exact candidate bytes from a clean environment and record all applicable [UX acceptance groups](../../experience/03-state-and-acceptance.md). This is acceptance of implemented capabilities, not a deferred place to design them.

**Testing requirements.** Package/contract/owner/version compatibility, failure/recovery and the real boundaries required above. A named later-provider fixture cannot close that provider's real gate.

**Completion gate.** All owned actions, schemas, public interfaces and tests are complete; later external evidence remains named. Publish/promote only the tested immutable bytes in the producer CI sequence.

**Index capacity acceptance.** Consume model04 launch-capacity.v1 account/realm vector and namespace budgets. Test reservations, old/new index overlap, tombstone reconciliation, threshold refusal before new paid admission, rebuild pausing and recovery. An index count never substitutes for owner authorization or creates an undisclosed purchased quota.

## 6. Impacts

Changed application scope, storage, transport, UI and deployment behavior are governed by the authorities in §2. Preserve existing business rules and formats. Migration/compatibility manifests include source/schema/plan/ABI/runtime versions; current cross-product collaboration is deferred and contributes no release input.

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-40.90](#rule-wp-40.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

| Evidence | Produced by |
|---|---|
| Source ownership: Other-product/realm/private resource rejected before snippets/context. | [WP-40.00](#rule-wp-40.00) |
| Derived indexes: Delete/rebuild, tombstone, dimensional mismatch and generation switch. | [WP-40.01](#rule-wp-40.01) |
| Hybrid retrieval and budgets: Budget bounds, multilingual/no-match/partial and exact decimal vectors. | [WP-40.02](#rule-wp-40.02) |
| Current permission: Revocation during query and stale index cannot expose content. | [WP-40.03](#rule-wp-40.03) |
| Evidence and citations: Stale/missing source labels and no fabricated citation. | [WP-40.04](#rule-wp-40.04) |
| Privacy and caches: Marker test, cross-app/account leakage and purge. | [WP-40.05](#rule-wp-40.05) |
| Real Cloud query path: Real compatible client/owner/index versions and explicit lexical-only degradation. | [WP-40.06](#rule-wp-40.06) |
| Exact artifact/consumer and applicable UX acceptance ledger | [WP-40.90](#rule-wp-40.90) |

## 8. Completion gate

All §7 evidence is attached, failed cases are resolved, actual vs fixture/provider evidence is labelled, and no required interface/state/recovery decision is delegated to the next implementer. Runtime and commercial gates close only with their stated real environment evidence.

## 9. Dependency consequences

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [SRCH.00](../delivery/lanes/search.md#task-srch-00) | [WP-40.00](40-knowledge-search-and-retrieval.md#rule-wp-40.00) (full) | [CON.10](../delivery/lanes/contracts.md#task-con-10) (contract), [CLOUD.37](../delivery/lanes/cloud.md#task-cloud-37) (artifact) |
| [SRCH.01](../delivery/lanes/search.md#task-srch-01) | [WP-40.01](40-knowledge-search-and-retrieval.md#rule-wp-40.01) (full) | [CON.10](../delivery/lanes/contracts.md#task-con-10) (contract) |
| [SRCH.02](../delivery/lanes/search.md#task-srch-02) | [WP-40.02](40-knowledge-search-and-retrieval.md#rule-wp-40.02) (full) | none |
| [SRCH.03](../delivery/lanes/search.md#task-srch-03) | [WP-40.03](40-knowledge-search-and-retrieval.md#rule-wp-40.03) (full) | [CLOUD.11](../delivery/lanes/cloud.md#task-cloud-11) (artifact) |
| [SRCH.04](../delivery/lanes/search.md#task-srch-04) | [WP-40.04](40-knowledge-search-and-retrieval.md#rule-wp-40.04) (full) | none |
| [SRCH.05](../delivery/lanes/search.md#task-srch-05) | [WP-40.05](40-knowledge-search-and-retrieval.md#rule-wp-40.05) (full) | none |
| [SRCH.06](../delivery/lanes/search.md#task-srch-06) | [WP-40.06](40-knowledge-search-and-retrieval.md#rule-wp-40.06) (full) | [AIR.00](../delivery/lanes/ai-routing.md#task-air-00) (artifact), [POL.08](../delivery/lanes/policy.md#task-pol-08) (artifact), [AIR.06](../delivery/lanes/ai-routing.md#task-air-06) (artifact) |
| [SRCH.90](../delivery/lanes/search.md#task-srch-90) | [WP-40.90](40-knowledge-search-and-retrieval.md#rule-wp-40.90) (full, including index capacity acceptance) | none |

**Consumers outside this package:** [HAR.01](../delivery/lanes/harness.md#task-har-01), [REL.06](../delivery/lanes/release.md#task-rel-06).

<!-- delivery-graph:end -->

