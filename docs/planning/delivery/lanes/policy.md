# Dynamic policy and configuration — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Configuration schemas, limits, flags, kill switches, resolution, compatibility and publication.

Tasks: 11 · Owning repositories: Cloud, DesktopPlatform · Integration owner(s): Cloud integration owner, DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [POL.01](#task-pol-01) | The four boundaries | service | S | none | not-started |
| [POL.02](#task-pol-02) | Schema-constrained configuration | service | L | [CON.12](contracts.md#task-con-12) (contract), [POL.01](#task-pol-01) (artifact) | not-started |
| [POL.03](#task-pol-03) | Compiled hard limits | service | M | [POL.02](#task-pol-02) (artifact) | not-started |
| [POL.04](#task-pol-04) | Features, flags and deterministic rollout | service | L | [POL.01](#task-pol-01) (artifact), [POL.02](#task-pol-02) (artifact), [COM.05](commerce.md#task-com-05) (artifact) | not-started |
| [POL.05](#task-pol-05) | Kill switches | service | M | [POL.02](#task-pol-02) (artifact), [CON.14](contracts.md#task-con-14) (contract) | not-started |
| [POL.06](#task-pol-06) | Scoped resolution and explainability (server side) | service | M | [POL.02](#task-pol-02) (artifact) | not-started |
| [POL.07](#task-pol-07) | Compatibility policy | service | M | [POL.02](#task-pol-02) (artifact) | not-started |
| [POL.08](#task-pol-08) | Publication, staleness and last-known-good (server side) | service | M | [POL.02](#task-pol-02) (artifact) | not-started |
| [POL.09](#task-pol-09) | Client-side policy resolution library (native/AOT) | service | L | [POL.04](#task-pol-04) (artifact), [CON.12](contracts.md#task-con-12) (contract), [CON.22](contracts.md#task-con-22) (contract) | not-started |
| [POL.10](#task-pol-10) | Owned-artifact receipt | service | S | [POL.09](#task-pol-09) (artifact), [POL.03](#task-pol-03) (artifact), [POL.05](#task-pol-05) (artifact), [POL.06](#task-pol-06) (artifact), [POL.07](#task-pol-07) (artifact) | not-started |
| [POL.11](#task-pol-11) | First real publish-then-resolve round trip from Cloud Policy authority to the DesktopPlatform client library | integration | M | [POL.08](#task-pol-08) (artifact), [POL.09](#task-pol-09) (artifact) | not-started |

## Tasks

<a id="task-pol-01"></a>

### POL.01 — The four boundaries

**Outcome.** Policy, entitlement, user settings, health and the data plane are kept structurally distinct with an architecture test asserting no policy type reaches an entitlement decision, each boundary backed by a failing negative fixture.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-01` and ledger record `ledger/tasks/pol-01.md` in the Plan repository; task branch `task/pol-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S · early risk proof |
| Obligations | [WP-44.00](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.00) — full |
| Provides | policy-boundary-markers; boundary-architecture-test |
| Start prerequisites | none |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [POL.02](#task-pol-02), [POL.04](#task-pol-04) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Policy/**/Boundaries/**` |
| Validation | Offline architecture test (assembly/namespace dependency scan) plus four negative fixtures. |
| Completion evidence | Four boundary negative-fixture results plus the architecture-test pass log. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Cheap structural invariant that every other Policy task must respect; wrong here silently corrupts POL.02-09. |

<a id="task-pol-02"></a>

### POL.02 — Schema-constrained configuration

**Outcome.** policy.body.v1 and configuration.v1 bundles validate exactly against their schema (key/type/scope/limit/cross-reference), an invalid bundle is rejected wholesale, and activation is a dry-run proposal with dual approval and compare-and-swap.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-02` and ledger record `ledger/tasks/pol-02.md` in the Plan repository; task branch `task/pol-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-44.01](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.01) — full<br>[WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) Operator contract closure — configuration/policy owners — operator contract closure; configuration/policy owner: dry-run proposal/dual-approval/activation CAS as the typed proposal protocol |
| Provides | configuration-schema-validation; activation-cas-pipeline |
| Start prerequisites | **contract** [CON.12](contracts.md#task-con-12) — policy.body.v1 and configuration.v1 published message schemas per architecture/contracts/08 §4/§6. *Why:* only tooling-level 'policy' files (dependency/licence policy) exist in Contracts at HEAD e6c4a77f; no PolicyBody or Configuration wire message was found, so there is nothing generated to validate against yet<br>**artifact** [POL.01](#task-pol-01) — boundary markers. *Why:* schema validation must reject a body that reaches into entitlement/settings/health/data-plane territory, which POL.01 defines |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.01](ai-routing.md#task-air-01), [POL.03](#task-pol-03), [POL.04](#task-pol-04), [POL.05](#task-pol-05), [POL.06](#task-pol-06), [POL.07](#task-pol-07), [POL.08](#task-pol-08), [SRCH.90](search.md#task-srch-90), [WEB.14](web.md#task-web-14) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Configuration/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Offline tests: unknown key/field/version, invalid commercial route, secret-in-body, conflicting rule priority, stale parent, mixed-replica version, rollback; AOT-publish check. |
| Completion evidence | Atomic-rejection test (no partial apply); AOT-clean publish result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-pol-03"></a>

### POL.03 — Compiled hard limits

**Outcome.** Safety-critical limits are compiled and authoritative; remote policy may only tighten them, and any attempt to loosen one is rejected and recorded.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-03` and ledger record `ledger/tasks/pol-03.md` in the Plan repository; task branch `task/pol-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M · early risk proof |
| Obligations | [WP-44.02](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.02) — full |
| Provides | compiled-hard-limits |
| Start prerequisites | **artifact** [POL.02](#task-pol-02) — the activation validation pipeline. *Why:* loosening-rejection is enforced as part of bundle activation validation |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [POL.10](#task-pol-10), [SIM.07](simulator.md#task-sim-07) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Policy/**/HardLimits/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Offline tests: per-hard-limit loosening-rejection, tightening-acceptance, audit assertion on rejection. |
| Completion evidence | Loosening-rejection test per compiled hard limit, with audit record. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Security-critical invariant ([BR-03](../../../architecture/14-build-packaging-and-release.md#rule-br-03)); cheap to verify in isolation before building rollout/kill-switch machinery that also touches these limits. |

<a id="task-pol-04"></a>

### POL.04 — Features, flags and deterministic rollout

**Outcome.** Deterministic target/percent hashing, exclusion groups and sticky experiment allocation select the same result for the same stable subject/version across languages, and rollout cannot grant commercial or security authority.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-04` and ledger record `ledger/tasks/pol-04.md` in the Plan repository; task branch `task/pol-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-44.03](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.03) — server-side flag/rollout definition, publication and byte/hash/bucket algorithm; on-device execution split to POL.09 |
| Provides | rollout-hashing-algorithm; flag-lifecycle |
| Start prerequisites | **artifact** [POL.01](#task-pol-01) — boundary enforcement. *Why:* rollout must not be able to grant commercial/security authority, which is exactly a boundary POL.01 defines<br>**artifact** [POL.02](#task-pol-02) — schema/activation pipeline. *Why:* flag/rollout definitions are published and activated as configuration bundles through POL.02's pipeline<br>**artifact** [COM.05](commerce.md#task-com-05) — explicit-setting/entitlement priority ordering. *Why:* annex 08 §5 requires explicit-setting and entitlement to take priority over rollout bucketing; the resolver is where entitlement is decided (same area, [WP-42.04](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.04)) |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [POL.09](#task-pol-09) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Policy/**/Rollout/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Offline tests: independent byte/hash/bucket vectors, boundary 0/9999, holdout, overlapping exclusion group, account/device change, cached signed bundle expiry. |
| Completion evidence | Cross-language hash/bucket vector match; boundary 0/9999 test. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-pol-05"></a>

### POL.05 — Kill switches

**Outcome.** All four kill-switch modes propagate promptly with a defined blast radius, a mandatory reason, a user-visible explanation and a complete audit record, and are reversible.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-05` and ledger record `ledger/tasks/pol-05.md` in the Plan repository; task branch `task/pol-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-44.04](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.04) — full<br>[WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) operator contract closure; the 'kill' typed operator RPC — operator contract closure; the 'kill' typed operator RPC<br>[WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) Operator contract closure — configuration/policy owners — package-level obligation contribution |
| Provides | kill-switch-modes |
| Start prerequisites | **artifact** [POL.02](#task-pol-02) — activation CAS pipeline. *Why:* kill-switch activation reuses the same schema/activation mechanism as any other policy bundle<br>**contract** [CON.14](contracts.md#task-con-14) — the 'kill' operator RPC shape per registry04 §9.2. *Why:* same gap as COM.13 — only OperatorCallContext exists at Contracts HEAD e6c4a77f, no per-domain operator RPC including kill is generated yet |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.64](cloud.md#task-cloud-64), [OPS.05](operations.md#task-ops-05), [OPS.13](operations.md#task-ops-13), [POL.10](#task-pol-10) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Policy/**/KillSwitch/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Offline tests: per-mode activation/propagation, user-visibility, audit-completeness, reversal. |
| Completion evidence | Per-mode propagation test with user-visible reason and complete audit record. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-pol-06"></a>

### POL.06 — Scoped resolution and explainability (server side)

**Outcome.** Policy resolves across application, workspace, device and installation scopes in a fixed order, and the server can state which scope and bundle produced any effective value.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-06` and ledger record `ledger/tasks/pol-06.md` in the Plan repository; task branch `task/pol-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-44.05](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.05) — server-side resolution across application/workspace/device/installation scopes with fixed order, and the explainability endpoint/data; client-side consumption split to POL.09 |
| Provides | scoped-resolution-server; explainability-data |
| Start prerequisites | **artifact** [POL.02](#task-pol-02) — published, validated bundles to resolve over. *Why:* resolution operates over activated configuration bundles |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [POL.10](#task-pol-10) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Policy/**/Resolution/**` |
| Validation | Offline tests: resolution-order matrix, explainability per scope, workspace-policy override. |
| Completion evidence | Resolution-order matrix result; explainability-per-scope result. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-pol-07"></a>

### POL.07 — Compatibility policy

**Outcome.** Compatibility rules express supported client windows and blocked version ranges; a bad version is blockable without affecting neighbours, and a minimum-version requirement is never enforced before its grace period elapses.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-07` and ledger record `ledger/tasks/pol-07.md` in the Plan repository; task branch `task/pol-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-44.06](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.06) — full |
| Provides | compatibility-policy-rules |
| Start prerequisites | **artifact** [POL.02](#task-pol-02) — schema/activation pipeline. *Why:* compatibility rules are published and activated as a policy bundle type |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [UPD.08](updater.md#task-upd-08) — the update feed actually stopping an offer for a blocked version. *Why:* [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44)'s own downstream list names 53 as a consumer; a compatibility rule is only proven real once the update feed enforces it, which POL.07 does not own |
| Unblocks | [POL.10](#task-pol-10) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Policy/**/Compatibility/**` |
| Validation | Offline tests: range-blocking precision, grace-period enforcement; update-feed integration test stays with the [WP-53](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53) consumer per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (no cross-repo E2E in this task's CI). |
| Completion evidence | Range-blocking precision test; grace-period enforcement test. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-pol-08"></a>

### POL.08 — Publication, staleness and last-known-good (server side)

**Outcome.** Bundles publish with versioning and audit, and the server-side staleness/application-timing contract is defined so a change is never applied in a way that produces inconsistent behaviour mid-operation.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-08` and ledger record `ledger/tasks/pol-08.md` in the Plan repository; task branch `task/pol-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-44.07](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.07) — bundle publication with versioning and audit; server-side staleness signalling; the application-timing contract clients must honour. Client caching/fallback/mid-operation behaviour split to POL.09 |
| Provides | bundle-publication; staleness-signal-contract |
| Start prerequisites | **artifact** [POL.02](#task-pol-02) — validated bundle to publish. *Why:* publication follows validation/activation |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.00](ai-routing.md#task-air-00), [POL.09](#task-pol-09), [POL.11](#task-pol-11), [SRCH.06](search.md#task-srch-06), [WEB.29](web.md#task-web-29) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Policy/**/Publication/**` |
| Validation | Offline tests: publication audit, staleness-signal correctness. |
| Completion evidence | Publication audit test. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-pol-09"></a>

### POL.09 — Client-side policy resolution library (native/AOT)

**Outcome.** A single ArcForges.Policy building block resolves, caches, and explains policy identically under Native AOT, falling back from staleness to last-known-good to compiled defaults with the staleness state always visible, and a change never takes effect mid-operation inconsistently.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/pol-09` and ledger record `ledger/tasks/pol-09.md` in the Plan repository; task branch `task/pol-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-44.05](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.05) — client-side consumption of scoped resolution/explainability<br>[WP-44.07](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.07) — client caching, staleness threshold, fallback to last-known-good then compiled defaults, staleness visible, mid-operation application timing<br>[WP-44.03](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.03) — client execution of the deterministic rollout hash so the same subject/version selects the same result on-device |
| Provides | client-policy-resolution-library |
| Start prerequisites | **artifact** [POL.04](#task-pol-04) — the deterministic rollout hashing algorithm specification. *Why:* the client must reproduce the exact same hash/bucket result as the server for the same subject/version<br>**contract** [CON.12](contracts.md#task-con-12) — policy.body.v1/configuration.v1 generated client-side (C#) types. *Why:* same schema gap as POL.02 — the client needs the generated DTOs to deserialize into<br>**contract** [CON.22](contracts.md#task-con-22) — published policy.getBundle. *Why:* the client resolution library fetches the generated policy bundle |
| Entry condition | [ADOPT.02.policy](adoption.md#task-adopt-02-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [POL.11](#task-pol-11) — a genuinely published bundle fetched and cached by this library, with staleness fallback proven against the deployed Cloud policy service. *Why:* this task's own tests can only prove the fallback chain mechanics in isolation; real staleness/LKG behavior needs a real publish-then-resolve round trip<br>**integration** [POL.08](#task-pol-08) — real server-side publication and staleness signal complete. *Why:* the client library starts from the published policy contract and the compiled last-known-good seed; its acceptance still resolves the real publication |
| Unblocks | [POL.10](#task-pol-10), [POL.11](#task-pol-11), [UPD.05](updater.md#task-upd-05), [UPD.08](updater.md#task-upd-08) |
| Permitted substitutes | [SUB-lkg-compiled-defaults-seed](../substitutes.md#sub-lkg-compiled-defaults-seed) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Policy/**` |
| Shared resources | [RES-contracts-schema-sources](../shared-resources.md#res-contracts-schema-sources) (append) |
| Validation | Offline unit tests: staleness-fallback-chain, mid-operation-application, offline-extended, AOT publish/trim check (this module must publish cleanly under Native AOT per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)'s AOT compile class). |
| Completion evidence | Fallback-chain-to-compiled-defaults test; AOT-clean publish result. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform HEAD fe8476d0 has BuildingBlocks/{Application.Abstractions,Desktop.Experience,Desktop.Graphics,Desktop.Preview,Desktop.RichContent,Desktop.Text,Foundation,NativeInterop,Observability,Persistence.Sqlite,Security} but no ArcForges.Policy yet. |
| Notes | Cross-repo: [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) is planned under the commerce, policy and operations lanes but this substep's implementation path lives in the DesktopPlatform repo per [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) §4's own file table. The React/Web browser binding is NOT built here — [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44)'s downstream list omits 47/49 and includes 48, so the browser-side resolver is expected to be built by the Web and Android lanes ([WP-48](../../work-packages/48-account-portal.md#rule-wp-48)) consuming this task's published algorithm/contract, not duplicated here. |

<a id="task-pol-10"></a>

### POL.10 — Owned-artifact receipt

**Outcome.** The package-level owned-artifact/real-integration receipt is recorded confirming every CF run and effect uses the required policy version and stale/disallowed models or revoked permission fail deterministically without client-side policy becoming authority.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-10` and ledger record `ledger/tasks/pol-10.md` in the Plan repository; task branch `task/pol-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Package acceptance | Records the [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-44.90](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.90) — full |
| Provides | wp44-closure-receipt |
| Start prerequisites | **artifact** [POL.09](#task-pol-09) — client resolution evidence to attach. *Why:* the receipt must show the client never treats stale/local policy as authoritative, which only POL.09's fallback tests demonstrate<br>**artifact** [POL.03](#task-pol-03) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [POL.05](#task-pol-05) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [POL.06](#task-pol-06) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [POL.07](#task-pol-07) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.06](release.md#task-rel-06), [REL.08](release.md#task-rel-08) |
| Write scope | `Cloud:eng/provenance/records/**` |
| Validation | Aggregation of POL.01-09 evidence at the candidate closure. |
| Completion evidence | The owned-artifact/real-integration receipt. |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-pol-11"></a>

### POL.11 — First real publish-then-resolve round trip from Cloud Policy authority to the DesktopPlatform client library

**Outcome.** a genuinely published bundle is fetched, cached, and correctly falls back to last-known-good on a later real staleness condition, not just against POL.09's local fixture

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/pol-11` and ledger record `ledger/tasks/pol-11.md` in the Plan repository; task branch `task/pol-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-44.07](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.07) — real fallback chain against a deployed publication endpoint |
| Start prerequisites | **artifact** [POL.08](#task-pol-08) — real, delivered outcome of POL.08 (Publication, staleness and last-known-good (server side)). *Why:* this integration exercises the real publication, staleness and last-known-good (server side) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [POL.09](#task-pol-09) — real, delivered outcome of POL.09 (Client-side policy resolution library (native/AOT)). *Why:* this integration exercises the real client-side policy resolution library (native/AOT) instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.07.policy](adoption.md#task-adopt-07-policy) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [POL.09](#task-pol-09) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | a genuinely published bundle is fetched, cached, and correctly falls back to last-known-good on a later real staleness condition, not just against POL.09's local fixture |
| Baseline (unreviewed unless accepted) | not-started |
