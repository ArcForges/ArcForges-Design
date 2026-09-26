# Knowledge search and retrieval — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Application-scoped derived indexes, hybrid retrieval, permission and citations.

Tasks: 8 · Owning repositories: Cloud · Integration owner(s): Cloud integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [SRCH.00](#task-srch-00) | Source admission and registration for search | service | M | [CON.10](contracts.md#task-con-10) (contract), [CLOUD.37](cloud.md#task-cloud-37) (artifact) | not-started |
| [SRCH.01](#task-srch-01) | Scoped derived index production (D1 FTS + Vectorize) | service | L | [SRCH.00](#task-srch-00) (artifact), [CON.10](contracts.md#task-con-10) (contract) | not-started |
| [SRCH.02](#task-srch-02) | Hybrid retrieval, RRF fusion and budgets | service | L | [SRCH.01](#task-srch-01) (artifact) | not-started |
| [SRCH.03](#task-srch-03) | Current permission recheck at query time | service | S | [SRCH.02](#task-srch-02) (artifact), [CLOUD.11](cloud.md#task-cloud-11) (artifact) | not-started |
| [SRCH.04](#task-srch-04) | Evidence and citations | service | M | [SRCH.03](#task-srch-03) (artifact) | not-started |
| [SRCH.05](#task-srch-05) | Privacy partitioning and cache isolation | service | M | [SRCH.01](#task-srch-01) (artifact) | not-started |
| [SRCH.06](#task-srch-06) | Real Cloud query path (fixture-to-real swap) | integration | M | [AIR.00](ai-routing.md#task-air-00) (artifact), [POL.08](policy.md#task-pol-08) (artifact), [SRCH.01](#task-srch-01) (artifact), [SRCH.02](#task-srch-02) (artifact), [AIR.06](ai-routing.md#task-air-06) (artifact) | not-started |
| [SRCH.90](#task-srch-90) | Owned artifacts, real integration and index capacity acceptance | service | M | [SRCH.06](#task-srch-06) (artifact), [SRCH.03](#task-srch-03) (artifact), [SRCH.04](#task-srch-04) (artifact), [SRCH.05](#task-srch-05) (artifact) | not-started |

## Tasks

<a id="task-srch-00"></a>

### SRCH.00 — Source admission and registration for search

**Outcome.** Own-product content, explicitly selected uploads and authorized web sources are admitted into the search source registry with origin/egress and consent recorded; other-product, other-realm and private resources are rejected before any index write.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/srch-00` and ledger record `ledger/tasks/srch-00.md` in the Plan repository; task branch `task/srch-00` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-40.00](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.00) — full |
| Provides | search-source-registry |
| Start prerequisites | **contract** [CON.10](contracts.md#task-con-10) — published SourceRecord/ContentOrigin typed record (origin, consent, egress) in Contracts public schema. *Why:* admission must persist a typed, versioned origin/consent record before any content is queued for indexing; the exact CON substep that publishes this record was not determined from this area's WP files<br>**artifact** [CLOUD.37](cloud.md#task-cloud-37) — durable resource identity/revision for synced product content. *Why:* admitted sources need a stable resource id and revision to key the derived index against; [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) owns the sync engine and blob lifecycle that assigns these |
| Entry condition | [ADOPT.07.search](adoption.md#task-adopt-07-search) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [HAR.01](harness.md#task-har-01), [SRCH.01](#task-srch-01) |
| Permitted substitutes | [SUB-web-search-fixture](../substitutes.md#sub-web-search-fixture) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Retrieval/Sources/**`<br>`Cloud:tests/Cloud.Tests.Integration/Retrieval/Sources/**` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline unit + Cloud integration tests against the real D1 schema in an ephemeral test host; no live web fetch in CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) forbids live-service CI) -- the web-source path is exercised through the fixture web-search response only. |
| Completion evidence | Rejection-before-snippet test matrix (other-product/realm/private), consent/origin record contents, source registration receipt. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |
| Notes | [WP-40](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40) has no explicit section 4 project/file table (unlike [WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41), [WP-43](../../work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43) and [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52)); the Cloud module path above follows the Cloud module layout convention and is not stated in [WP-40](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40) itself. |

<a id="task-srch-01"></a>

### SRCH.01 — Scoped derived index production (D1 FTS + Vectorize)

**Outcome.** D1 FTS scoped queries and per-workspace Vectorize namespaces are produced with mandatory realm/product/model-generation filters, source revision/policy checks, rebuild pointers, tombstone reconciliation and dimensional-change isolation (separate index, atomic reader switch, rollback window).

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/srch-01` and ledger record `ledger/tasks/srch-01.md` in the Plan repository; task branch `task/srch-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-40.01](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.01) — full |
| Provides | scoped-derived-index |
| Start prerequisites | **artifact** [SRCH.00](#task-srch-00) — admitted source registry entries to index. *Why:* nothing to index before a source is admitted<br>**contract** [CON.10](contracts.md#task-con-10) — the data-model retrieval_chunk projection key (sourceId, sourceRev, embeddingModelId, embeddingProfileVersion, chunkHash) as a published schema. *Why:* the index writer must key rows on the exact published projection, not an ad hoc shape |
| Entry condition | [ADOPT.07.search](adoption.md#task-adopt-07-search) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SRCH.02](#task-srch-02), [SRCH.05](#task-srch-05), [SRCH.06](#task-srch-06) |
| Permitted substitutes | [SUB-embedding-rerank-fixture](../substitutes.md#sub-embedding-rerank-fixture) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Retrieval/Indexing/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append), [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline unit tests for index math with fixture vectors; D1/Vectorize behavior exercised against local/emulated CF bindings per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (no live CF in ordinary CI); [L-16](../../../assurance/release-gates.md#rule-l-16) index/namespace footprint measured locally. |
| Completion evidence | Cross-product/tenant isolation before topK, stale deletion, unavailable canonical owner, lexical fallback, [L-16](../../../assurance/release-gates.md#rule-l-16) footprint measurement. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

<a id="task-srch-02"></a>

### SRCH.02 — Hybrid retrieval, RRF fusion and budgets

**Outcome.** Lexical (D1 FTS) and semantic (Vectorize) candidates are fused with RRF(x)=sum(1/(60+rank_i(x))), exact-match priority preserved, the Notes scalar comparator never reordered by vector score, and RetrievalBudget defaults (candidates 200/500, evidence 20/100, contextTokens 8192/24000, perSource 5/20, graphDepth 1/3) enforced.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/srch-02` and ledger record `ledger/tasks/srch-02.md` in the Plan repository; task branch `task/srch-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-40.02](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.02) — full |
| Provides | hybrid-retrieval |
| Start prerequisites | **artifact** [SRCH.01](#task-srch-01) — scoped derived index to query against. *Why:* fusion has nothing to rank without the index |
| Entry condition | [ADOPT.07.search](adoption.md#task-adopt-07-search) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SRCH.03](#task-srch-03), [SRCH.06](#task-srch-06) |
| Permitted substitutes | [SUB-embedding-rerank-fixture](../substitutes.md#sub-embedding-rerank-fixture) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Retrieval/Ranking/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append), [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline unit tests: budget bounds, multilingual/no-match/partial queries, exact decimal vector comparison against fixture vectors. |
| Completion evidence | Budget-bound test matrix; multilingual/no-match/partial results; decimal-vector exactness. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

<a id="task-srch-03"></a>

### SRCH.03 — Current permission recheck at query time

**Outcome.** Source owner permission and revision are rechecked after candidate retrieval and before any count/snippet/citation is returned; revocation during a query and a stale index can never expose content.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/srch-03` and ledger record `ledger/tasks/srch-03.md` in the Plan repository; task branch `task/srch-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-40.03](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.03) — full |
| Provides | retrieval-permission-recheck |
| Start prerequisites | **artifact** [SRCH.02](#task-srch-02) — ranked candidate list to filter. *Why:* nothing to recheck before candidates exist<br>**artifact** [CLOUD.11](cloud.md#task-cloud-11) — live owner/grant permission check API. *Why:* the recheck must call the actual current-permission source of truth, not a cached copy; the Cloud lane [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) is presumed to own identity/grant checks (exact substep not read from this area) |
| Entry condition | [ADOPT.07.search](adoption.md#task-adopt-07-search) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SRCH.04](#task-srch-04), [SRCH.90](#task-srch-90) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Retrieval/PermissionRecheck/**` |
| Validation | Offline integration test with a revocation injected mid-query and a deliberately stale index row. |
| Completion evidence | Revocation-during-query and stale-index-cannot-expose-content test results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

<a id="task-srch-04"></a>

### SRCH.04 — Evidence and citations

**Outcome.** Retrieval results retain source kind, immutable reference, anchor, uncertainty/completeness and measurement/media precision; stale or missing sources are labelled and no citation is ever fabricated.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/srch-04` and ledger record `ledger/tasks/srch-04.md` in the Plan repository; task branch `task/srch-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-40.04](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.04) — full |
| Provides | retrieval-citations |
| Start prerequisites | **artifact** [SRCH.03](#task-srch-03) — permission-rechecked candidates. *Why:* citations are only built for content cleared to surface |
| Entry condition | [ADOPT.07.search](adoption.md#task-adopt-07-search) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SRCH.90](#task-srch-90) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Retrieval/Citations/**` |
| Validation | Offline unit tests for stale/missing source labelling and anti-fabrication assertions. |
| Completion evidence | Stale/missing source label tests; no-fabricated-citation assertion. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

<a id="task-srch-05"></a>

### SRCH.05 — Privacy partitioning and cache isolation

**Outcome.** Cache, history and context are partitioned by product/profile per [RI-01](../../../architecture/data-model/03-derived-stores.md#rule-ri-01)..03 (workspace+principal key, no cross-workspace reuse); temporary/local Cloud-processing content never enters Cloud search.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/srch-05` and ledger record `ledger/tasks/srch-05.md` in the Plan repository; task branch `task/srch-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-40.05](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.05) — full |
| Provides | retrieval-privacy-partitioning |
| Start prerequisites | **artifact** [SRCH.01](#task-srch-01) — index/cache tables to partition. *Why:* partitioning is enforced at the same storage SRCH.01 creates |
| Entry condition | [ADOPT.07.search](adoption.md#task-adopt-07-search) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [SRCH.90](#task-srch-90) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Retrieval/Privacy/**` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | Offline marker test, cross-app/account leakage test, purge test. |
| Completion evidence | Marker test, cross-app/account leakage and purge results. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

<a id="task-srch-06"></a>

### SRCH.06 — Real Cloud query path (fixture-to-real swap)

**Outcome.** The retrieval path runs against real Workers AI embeddings/reranker and real D1/Vectorize with C# owner filtering; SUB-embedding-rerank-fixture is retired from the query path, and explicit lexical-only degradation is proven when the semantic path is unavailable.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/srch-06` and ledger record `ledger/tasks/srch-06.md` in the Plan repository; task branch `task/srch-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-40.06](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.06) — full |
| Provides | real-cloud-retrieval |
| Start prerequisites | **artifact** [AIR.00](ai-routing.md#task-air-00) — deployed Workers AI embed/rerank adapter (real, not fixture). *Why:* this task's entire purpose is proving the real provider path; a fixture cannot satisfy it<br>**artifact** [POL.08](policy.md#task-pol-08) — active policy/config snapshot naming the admitted embedding/rerank model generation. *Why:* [WP-40.01](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.01)'s mandatory model-generation filter must read the currently activated model identity from policy, not a hardcoded string<br>**artifact** [SRCH.01](#task-srch-01) — scoped derived index production. *Why:* the real query path replaces fixture embeddings in the index<br>**artifact** [SRCH.02](#task-srch-02) — hybrid retrieval and budgets. *Why:* the real query path replaces fixture reranking<br>**artifact** [AIR.06](ai-routing.md#task-air-06) — the real operator-funded web-search dispatch capability. *Why:* the real query path replaces the web-search fixture and runs against the real dispatch |
| Entry condition | [ADOPT.07.search](adoption.md#task-adopt-07-search) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [SRCH.90](#task-srch-90) — index capacity acceptance evidence. *Why:* this task's real-path evidence feeds the package-level acceptance in SRCH.90 |
| Unblocks | [SRCH.90](#task-srch-90) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Retrieval/Indexing/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Retrieval/Ranking/**` |
| Shared resources | [RES-ai-workflow-and-routes](../shared-resources.md#res-ai-workflow-and-routes) (append), [RES-private-configuration](../shared-resources.md#res-private-configuration) (append) |
| Validation | Real compatible client/owner/index version test against deployed CF bindings (credentialed candidate gate, not ordinary CI, per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)'s 'no real AI inference in CI'); explicit lexical-only degradation test. |
| Completion evidence | Real compatible client/owner/index versions; explicit lexical-only degradation. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |

<a id="task-srch-90"></a>

### SRCH.90 — Owned artifacts, real integration and index capacity acceptance

**Outcome.** Every SRCH substep is built/packed once and consumed as exact candidate bytes from a clean environment; model04 launch-capacity.v1 account/realm vector and namespace budgets are enforced with reservation, old/new index overlap, tombstone reconciliation, threshold refusal before new paid admission, and rebuild pausing/recovery all proven.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/srch-90` and ledger record `ledger/tasks/srch-90.md` in the Plan repository; task branch `task/srch-90` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Package acceptance | Records the [WP-40](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-40.90](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40.90) — full, including index capacity acceptance |
| Provides | search-package-acceptance |
| Start prerequisites | **artifact** [SRCH.06](#task-srch-06) — real query path evidence. *Why:* acceptance cannot close on fixture-only evidence<br>**artifact** [SRCH.03](#task-srch-03) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SRCH.04](#task-srch-04) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SRCH.05](#task-srch-05) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.search](adoption.md#task-adopt-07-search) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [POL.02](policy.md#task-pol-02) — launch-capacity.v1 signed configuration snapshot. *Why:* capacity/threshold-refusal tests need the real signed budget document, not an invented number |
| Unblocks | [REL.06](release.md#task-rel-06), [SRCH.06](#task-srch-06) |
| Write scope | `Cloud:tests/Cloud.Tests.Integration/Retrieval/**` |
| Shared resources | [RES-private-configuration](../shared-resources.md#res-private-configuration) (append) |
| Validation | Package/contract/owner/version compatibility and failure/recovery tests; [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) proportionate (no live paid-provider CI loop; capacity thresholds tested against recorded/replayable fixtures where the real CF budget document is unavailable in CI). |
| Completion evidence | Index capacity acceptance ledger: reservations, overlap, tombstone reconciliation, threshold refusal, rebuild pause/recovery. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Cloud repo is Hello-World stage (src/ArcForges.Cloud only: Program.cs/HelloEndpoint.cs/BuildIdentity.cs/HealthStatus.cs); no Modules.* tree exists. |
| Notes | [WP-40](../../work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40) Sec.9 names 50/52 as downstream consumers of this released artifact; not a completion blocker for SRCH.90 itself. Contributes to [PG-26](../../../assurance/open-gates-register.md#rule-pg-26) (launch capacity envelope) as one of its producers. |
