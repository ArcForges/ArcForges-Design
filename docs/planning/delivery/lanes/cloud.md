# Cloud core — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Host and D1 persistence, identity and sessions, public APIs, realtime events, sync and objects, backup and recovery.

Tasks: 63 · Owning repositories: Cloud, DesktopPlatform · Integration owner(s): Cloud integration owner, DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [CLOUD.01](#task-cloud-01) | Ingress and host pipeline | service | M | [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [CLOUD.02](#task-cloud-02) | Nineteen module boundaries and D1 named-plan bridge | service | M | [CLOUD.01](#task-cloud-01) (artifact) | not-started |
| [CLOUD.03](#task-cloud-03) | D1 migration runner and exact physical mapping | service | L | [CLOUD.02](#task-cloud-02) (artifact) | not-started |
| [CLOUD.04](#task-cloud-04) | Receipts, outbox, inbox dedup and change archive | service | M | [CLOUD.02](#task-cloud-02) (artifact), [CLOUD.03](#task-cloud-03) (artifact) | not-started |
| [CLOUD.05](#task-cloud-05) | Finite durable jobs (Cron/Queue/Workflow-woken endpoints) | service | M | [CLOUD.01](#task-cloud-01) (artifact), [CLOUD.04](#task-cloud-04) (artifact), [CLOUD.69](#task-cloud-69) (artifact) | not-started |
| [CLOUD.06](#task-cloud-06) | Shared atomic family guarded-batch engine | service | M | [CLOUD.02](#task-cloud-02) (artifact) | not-started |
| [CLOUD.07](#task-cloud-07) | Capacity, Container/D1 integration producer and harness | service | L | [CLOUD.02](#task-cloud-02) (artifact), [CLOUD.03](#task-cloud-03) (artifact), [CLOUD.06](#task-cloud-06) (artifact) | not-started |
| [CLOUD.08](#task-cloud-08) | Failure isolation and readiness surface | service | S | [CLOUD.01](#task-cloud-01) (artifact), [CLOUD.02](#task-cloud-02) (artifact) | not-started |
| [CLOUD.09](#task-cloud-09) | Selfhost.v1 deployment profile | service | M | [CLOUD.01](#task-cloud-01) (artifact), [CLOUD.03](#task-cloud-03) (artifact) | not-started |
| [CLOUD.10](#task-cloud-10) | Owned-artifact closure and launch-capacity.v1 acceptance | integration | M | [CLOUD.39](#task-cloud-39) (artifact), [SIM.10](simulator.md#task-sim-10) (artifact) | not-started |
| [CLOUD.11](#task-cloud-11) | Core identity model (realm, user, authIdentity, single-owner workspace) | service | M | [CLOUD.02](#task-cloud-02) (artifact), [CLOUD.03](#task-cloud-03) (artifact), [CLOUD.06](#task-cloud-06) (artifact) | not-started |
| [CLOUD.12](#task-cloud-12) | Native and browser authentication with real Postmark/SES mail delivery | service | L | [CLOUD.11](#task-cloud-11) (artifact) | not-started |
| [CLOUD.13](#task-cloud-13) | Device, installation, instance and session (four distinct concepts) | service | M | [CLOUD.11](#task-cloud-11) (artifact), [CLOUD.06](#task-cloud-06) (artifact) | not-started |
| [CLOUD.14](#task-cloud-14) | Device trust and remote gating | service | S | [CLOUD.13](#task-cloud-13) (artifact) | not-started |
| [CLOUD.15](#task-cloud-15) | Step-up challenges for sensitive operations | service | M | [CLOUD.12](#task-cloud-12) (artifact), [CLOUD.13](#task-cloud-13) (artifact) | not-started |
| [CLOUD.16](#task-cloud-16) | PAT and actor authorization | service | M | [CLOUD.11](#task-cloud-11) (artifact) | not-started |
| [CLOUD.17](#task-cloud-17) | Recovery, account states and deletion | service | M | [CLOUD.12](#task-cloud-12) (artifact) | not-started |
| [CLOUD.18](#task-cloud-18) | Independent native session integration (Platform client primitives) | service | M | [CLOUD.12](#task-cloud-12) (artifact), [PLT.40](platform.md#task-plt-40) (artifact) | not-started |
| [CLOUD.19](#task-cloud-19) | Browser cookie-session adapter and full account-surface closure | service | L | [CLOUD.01](#task-cloud-01) (artifact), [CLOUD.11](#task-cloud-11) (artifact), [CLOUD.13](#task-cloud-13) (artifact) | not-started |
| [CLOUD.20](#task-cloud-20) | Owned-artifact closure and real integration | integration | M | [CON.07](contracts.md#task-con-07) (artifact), [CLOUD.11](#task-cloud-11) (artifact), [CLOUD.66](#task-cloud-66) (artifact) | not-started |
| [CLOUD.21](#task-cloud-21) | Public endpoint mapping and validation | service | M | [CON.91](contracts.md#task-con-91) (contract), [CLOUD.13](#task-cloud-13) (artifact) | not-started |
| [CLOUD.22](#task-cloud-22) | Typed protocol and error mapping | service | M | [CLOUD.21](#task-cloud-21) (artifact) | not-started |
| [CLOUD.23](#task-cloud-23) | Typed queries and revision preconditions | service | M | [CLOUD.21](#task-cloud-21) (artifact), [CON.91](contracts.md#task-con-91) (contract) | not-started |
| [CLOUD.24](#task-cloud-24) | Idempotency and rate limiting | service | M | [CLOUD.21](#task-cloud-21) (artifact) | not-started |
| [CLOUD.25](#task-cloud-25) | Resource transport schema and future-owner boundary | service | M | [CLOUD.21](#task-cloud-21) (artifact), [PRF.07](runtime-proofs.md#task-prf-07) (artifact) | not-started |
| [CLOUD.26](#task-cloud-26) | Generated C#/TypeScript/Kotlin clients against Identity/Workspace/Device | service | L | [CLOUD.19](#task-cloud-19) (artifact), [CLOUD.22](#task-cloud-22) (artifact), [PRF.10](runtime-proofs.md#task-prf-10) (artifact) | not-started |
| [CLOUD.27](#task-cloud-27) | Compatibility window and bidirectional matrix | service | M | [CLOUD.26](#task-cloud-26) (artifact) | not-started |
| [CLOUD.28](#task-cloud-28) | Owned-artifact closure and real integration | integration | L | [AND.07](android.md#task-and-07) (artifact), [WEB.30](web.md#task-web-30) (artifact) | not-started |
| [CLOUD.29](#task-cloud-29) | Stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells) | service | M | [CLOUD.21](#task-cloud-21) (artifact), [CLOUD.19](#task-cloud-19) (artifact), [CON.11](contracts.md#task-con-11) (contract) | not-started |
| [CLOUD.30](#task-cloud-30) | Scoped subscription (owner/product/filter/recovery-generation binding) | service | M | [CLOUD.29](#task-cloud-29) (artifact) | not-started |
| [CLOUD.31](#task-cloud-31) | Cursor and gap handling (DO projection backed by D1 outbox) | service | M | [CLOUD.30](#task-cloud-30) (artifact), [CLOUD.04](#task-cloud-04) (artifact) | not-started |
| [CLOUD.32](#task-cloud-32) | Durable unary fallback (Poll/readOutput) | service | S | [CLOUD.31](#task-cloud-31) (artifact) | not-started |
| [CLOUD.33](#task-cloud-33) | Publication and wake (D1 outbox to bounded DO feed via Queues) | service | M | [CLOUD.31](#task-cloud-31) (artifact), [CLOUD.05](#task-cloud-05) (artifact), [CLOUD.69](#task-cloud-69) (artifact) | not-started |
| [CLOUD.34](#task-cloud-34) | Bounded stream lifecycle | service | S | [CLOUD.29](#task-cloud-29) (artifact) | not-started |
| [CLOUD.35](#task-cloud-35) | Reusable stream consumer adapters | service | M | [CLOUD.33](#task-cloud-33) (artifact), [CLOUD.34](#task-cloud-34) (artifact) | not-started |
| [CLOUD.36](#task-cloud-36) | Owned-artifact closure and real integration (tool-result acceptance) | integration | M | [DEV.14](device-bridge.md#task-dev-14) (artifact) | not-started |
| [CLOUD.38](#task-cloud-38) | Client outbox and conflict lineage (desktop data model) | service | L | [PLT.01](platform.md#task-plt-01) (artifact) | not-started |
| [CLOUD.39](#task-cloud-39) | Guarded publication, convergent bootstrap and the Sync owner transaction | service | L | [CLOUD.04](#task-cloud-04) (artifact), [CLOUD.31](#task-cloud-31) (artifact), [CLOUD.03](#task-cloud-03) (artifact), [CLOUD.06](#task-cloud-06) (artifact), [CON.03](contracts.md#task-con-03) (artifact), [CON.09](contracts.md#task-con-09) (artifact), [CLOUD.01](#task-cloud-01) (artifact) | not-started |
| [CLOUD.40](#task-cloud-40) | Conflict detection and five resolution policies | service | M | [CLOUD.38](#task-cloud-38) (artifact), [CLOUD.39](#task-cloud-39) (artifact) | not-started |
| [CLOUD.41](#task-cloud-41) | Deletion and tombstones | service | M | [CLOUD.39](#task-cloud-39) (artifact) | not-started |
| [CLOUD.42](#task-cloud-42) | Blob lifecycle (real R2 staged/verified/committed) | service | L | [CLOUD.01](#task-cloud-01) (artifact), [CLOUD.06](#task-cloud-06) (artifact), [CLOUD.25](#task-cloud-25) (artifact) | not-started |
| [CLOUD.43](#task-cloud-43) | Availability, protection, data-health signals and realm-transfer workflow | service | L | [CLOUD.42](#task-cloud-42) (artifact), [CLOUD.39](#task-cloud-39) (artifact) | not-started |
| [CLOUD.44](#task-cloud-44) | Multi-device convergence harness | integration | L | none | not-started |
| [CLOUD.45](#task-cloud-45) | Real Cloud Chat export producer | service | L | [CLOUD.42](#task-cloud-42) (artifact), [CLOUD.05](#task-cloud-05) (artifact), [CON.22](contracts.md#task-con-22) (contract) | not-started |
| [CLOUD.46](#task-cloud-46) | Application Cloud history and restartable import | service | M | [CLOUD.42](#task-cloud-42) (artifact), [CLOUD.06](#task-cloud-06) (artifact) | not-started |
| [CLOUD.47](#task-cloud-47) | Owned-artifact closure and real integration | integration | M | [AST.21](assistant.md#task-ast-21) (artifact), [AST.22](assistant.md#task-ast-22) (artifact), [CLOUD.58](#task-cloud-58) (artifact), [SCOPE.27](arcscope.md#task-scope-27) (artifact) | not-started |
| [CLOUD.48](#task-cloud-48) | D1 and independent object backup | service | L | [CLOUD.03](#task-cloud-03) (artifact), [CLOUD.42](#task-cloud-42) (artifact) | not-started |
| [CLOUD.49](#task-cloud-49) | Point-in-time and fresh restore | service | M | [CLOUD.48](#task-cloud-48) (artifact) | not-started |
| [CLOUD.50](#task-cloud-50) | Fresh environment rebuild | service | M | [CLOUD.49](#task-cloud-49) (artifact), [CLOUD.17](#task-cloud-17) (artifact) | not-started |
| [CLOUD.51](#task-cloud-51) | Disaster-recovery drill programme | integration | M | [CLOUD.50](#task-cloud-50) (artifact) | not-started |
| [CLOUD.52](#task-cloud-52) | Data health read projection | service | S | [CLOUD.48](#task-cloud-48) (artifact) | not-started |
| [CLOUD.53](#task-cloud-53) | Export and realm migration | service | M | [CLOUD.48](#task-cloud-48) (artifact) | not-started |
| [CLOUD.54](#task-cloud-54) | Backup release gate | service | S | [CLOUD.48](#task-cloud-48) (artifact) | not-started |
| [CLOUD.55](#task-cloud-55) | Owned-artifact closure and real integration | integration | M | none | not-started |
| [CLOUD.58](#task-cloud-58) | Structural removal of the Chat export runtime fixture | integration | M | [CLOUD.45](#task-cloud-45) (artifact), [AST.21](assistant.md#task-ast-21) (artifact) | not-started |
| [CLOUD.63](#task-cloud-63) | Real Commerce/Entitlement participation in the shared atomic family engine | integration | M | [CLOUD.06](#task-cloud-06) (artifact), [CLOUD.16](#task-cloud-16) (artifact), [COM.09](commerce.md#task-com-09) (artifact), [COM.16](commerce.md#task-com-16) (artifact) | not-started |
| [CLOUD.64](#task-cloud-64) | Full operator contract closure across PublicApi, Commerce, Policy and Console | integration | M | [COM.13](commerce.md#task-com-13) (artifact), [POL.05](policy.md#task-pol-05) (artifact), [OPS.05](operations.md#task-ops-05) (artifact), [CLOUD.21](#task-cloud-21) (artifact), [CLOUD.22](#task-cloud-22) (artifact) | not-started |
| [CLOUD.66](#task-cloud-66) | Every enumerated sensitive operation wired to the step-up mechanism | integration | M | [CLOUD.15](#task-cloud-15) (artifact), [COM.10](commerce.md#task-com-10) (artifact), [CLOUD.21](#task-cloud-21) (artifact), [CLOUD.22](#task-cloud-22) (artifact) | not-started |
| [CLOUD.67](#task-cloud-67) | Combined AI reopen after Cloud disaster-recovery restore | integration | M | [CLOUD.51](#task-cloud-51) (artifact), [HAR.00](harness.md#task-har-00) (artifact), [HAR.02](harness.md#task-har-02) (artifact), [HAR.03](harness.md#task-har-03) (artifact), [AIR.00](ai-routing.md#task-air-00) (artifact) | not-started |
| [CLOUD.68](#task-cloud-68) | ArcScope library read model and companion notifications | service | M | [CON.24](contracts.md#task-con-24) (contract), [CLOUD.39](#task-cloud-39) (artifact), [CLOUD.21](#task-cloud-21) (artifact) | not-started |
| [CLOUD.69](#task-cloud-69) | Correlation acceptance and propagation across ingress, response meta and queue wake | service | M | [CLOUD.01](#task-cloud-01) (artifact) | not-started |
| [CLOUD.70](#task-cloud-70) | Gated D1 migration deployment step and compatible-rollback flow | service | S | [CLOUD.03](#task-cloud-03) (artifact), [CLOUD.01](#task-cloud-01) (artifact) | not-started |
| [CLOUD.71](#task-cloud-71) | Serve the built Web profiles from the proof origin | service | S | [PRF.07](runtime-proofs.md#task-prf-07) (artifact), [PRF.08](runtime-proofs.md#task-prf-08) (artifact) | not-started |

## Tasks

<a id="task-cloud-01"></a>

### CLOUD.01 — Ingress and host pipeline

**Outcome.** Worker /api routing plus the C# AOT gRPC-Web/auth/current-owner pipeline runs behind the Worker in the real Container image; no buffered stream, no direct public Container port.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-01` and ledger record `ledger/tasks/cloud-01.md` in the Plan repository; task branch `task/cloud-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M · early risk proof |
| Obligations | [WP-21.00](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.00) — all work except the parts mapped to CLOUD.39 |
| Provides | cloud-ingress-pipeline |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — published ArcForges.Contracts.PublicApi generated gRPC-Web service stubs to register the pipeline against. *Why:* the pipeline has nothing to route without at least one generated service surface |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.02](#task-cloud-02), [CLOUD.05](#task-cloud-05), [CLOUD.08](#task-cloud-08), [CLOUD.09](#task-cloud-09), [CLOUD.10](#task-cloud-10), [CLOUD.19](#task-cloud-19), [CLOUD.39](#task-cloud-39), [CLOUD.42](#task-cloud-42), [CLOUD.69](#task-cloud-69), [CLOUD.70](#task-cloud-70), [HAR.00](harness.md#task-har-00), [PLT.48](platform.md#task-plt-48) |
| Write scope | `Cloud:worker/index.ts`<br>`Cloud:worker/router.ts`<br>`Cloud:worker/ingress/** (new: the generalized /api route table, credential and CSRF edge checks and the frame-guarded streaming pass-through)`<br>`Cloud:worker/foundation/entry.ts, Cloud:worker/foundation/container-env.ts and Cloud:worker/foundation/types.ts (only to hand the ingress route table the proof-only probe route and to forward the allowed origin; no change to a proof route, queue consumer or private handler)`<br>`Cloud:wrangler.json`<br>`Cloud:Dockerfile`<br>`Cloud:.dockerignore (only admit the new nested C# source folder of the existing host project by the same append-only explicit directory rule and *.cs rule used for its other source folders; every other ignore rule is preserved)`<br>`Cloud:src/ArcForges.Cloud/** (the existing Native AOT host project, which is the real layout of the planned src/ArcForges.Cloud.Host/**; the adoption rules forbid renaming it or adding a parallel project)`<br>`Cloud:tests/ArcForges.Cloud.Tests/**`<br>`Cloud:tests/worker/**`<br>`Cloud:eng/verification/** (the local cross-process and explicit opt-in live scenarios of the pipeline)`<br>`Cloud:package.json (the explicit test file list and the pipeline scenario scripts only; no dependency or version change)`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/cloud-01-*.json (new immutable successor chained from the then-active receipt, only because the changed bundle, manifest and source inputs are hash-bound; no coordinate, integrity value or closure entry changes)`<br>`Cloud:eng/provenance/** (immutable successor release profile, Worker bundle and runtime-notice records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt)`<br>`Cloud:docs/cloud-ingress.md, Cloud:docs/deployment.md and Cloud:AGENTS.md (factual description of the ingress pipeline; the AGENTS.md Hello bullet is narrowed to what remains true)` |
| Shared resources | [RES-cloud-deployment](../shared-resources.md#res-cloud-deployment) (append), [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | offline unit tests for routing/validation logic; deployed-environment request/stream/cancel/CSRF/trailer path checks are opt-in local runtime evidence per docs/validation-policy.md, not hosted CI |
| Completion evidence | source commit, Worker/Container image hash, deployed request/stream/cancel/CSRF/trailer scenario results, confirmation no buffered stream or direct public Container port exists |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Cloud@ce0a32a has only a Hello World Worker (worker/router.ts handles exactly /api/arcforges.hello.v1.HelloService/SayHello + /api/healthz) and a Hello World C# host (src/ArcForges.Cloud: BuildIdentity/HealthStatus/HelloEndpoint/Program). No real routing, auth, or module dispatch exists. |
| Notes | Foundation task. The Hello World router.ts already proves the deadline/cancel/body-limit/trailer mechanics at small scale (see worker/router.ts); WP21.00 generalizes this to real dispatch. Early risk: every later public call depends on this boundary being correct. |

<a id="task-cloud-02"></a>

### CLOUD.02 — Nineteen module boundaries and D1 named-plan bridge

**Outcome.** The 19 module projects exist as boundaries and the D1 named-plan bridge mechanism works: C# decides business logic and asks the Worker to execute one exact named/versioned plan; the Worker executes only approved SQL, never ad hoc queries.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-02` and ledger record `ledger/tasks/cloud-02.md` in the Plan repository; task branch `task/cloud-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M · early risk proof |
| Obligations | [WP-21.02](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.02) — full |
| Provides | d1-plan-bridge; module-boundary-pattern |
| Start prerequisites | **artifact** [CLOUD.01](#task-cloud-01) — the deployed ingress/host pipeline to carry the private C#<->Worker plan-execution calls. *Why:* the plan bridge is an internal call made through the same Container/Worker boundary CLOUD.01 establishes |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.03](#task-cloud-03), [CLOUD.04](#task-cloud-04), [CLOUD.06](#task-cloud-06), [CLOUD.07](#task-cloud-07), [CLOUD.08](#task-cloud-08), [CLOUD.10](#task-cloud-10), [CLOUD.11](#task-cloud-11), [SIM.01](simulator.md#task-sim-01) |
| Write scope | `Cloud:src/ArcForges.Cloud.Modules.*/** (one project per module, named ArcForges.Cloud.Modules.<Name> for the 19 owners of the Cloud schema map, plus ArcForges.Cloud.Modules.Abstractions for the shared boundary types; the Domain, Application and Infrastructure layers are folders and namespaces inside each project, enforced by architecture tests, instead of three projects per module)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/** (new project that owns the named-plan binding mechanism; it receives, by move with namespaces preserved, the PRF.07 proof bridge now in Cloud:src/ArcForges.Cloud/Storage/** and Cloud:src/ArcForges.Cloud/Hmac/**: plan definitions, exact scalar values, executor, private request signing and the generated manifest)`<br>`Cloud:storage/plans/** (the plan root and owner registry; it receives, by move, the reviewed plans now in Cloud:src/ArcForges.Cloud/Storage/Plans/**)`<br>`Cloud:src/ArcForges.Cloud/** (the existing Native AOT host project, which is the real layout of the planned Cloud.Host; only the removal of the moved Storage and Hmac sources, the project references, the module catalog listing in Composition/HostModules.cs and the project file; no behavior change and no rename, per the adoption rules)`<br>`Cloud:Cloud.slnx, Cloud:Dockerfile, Cloud:.dockerignore and Cloud:eng/policy/licence-boundary.json (only project membership, the restore and publish context of the new projects by the same explicit directory and *.cs rules, and the licence boundary rows; every other rule is preserved)`<br>`Cloud:tests/ArcForges.Cloud.Tests/** and Cloud:tests/worker/**`<br>`Cloud:eng/verification/storage-plans.ts (the plan root, the owner and table ownership checks and the generated C# output path; the Worker dictionary format and the manifest hash algorithm are unchanged) and Cloud:package.json (the explicit test file list only; no dependency or version change)`<br>`Cloud:tooling/dependency-policy.ts and Cloud:tooling/dependency-policy.test.ts (only to admit src/ArcForges.Cloud.Storage.D1/ as the second consumer root of the private generated CloudInternal records, which moved with the bridge; no new package, owner or coordinate), and Cloud:tooling/release-provenance.ts only if an existing check enumerates the host source root`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/cloud-02-*.json (new immutable successor chained from the then-active receipt, only because the hash-bound project, lock and source inputs change; no coordinate, integrity value or closure entry changes)`<br>`Cloud:eng/provenance/** (immutable successor release profile, Worker bundle and runtime-notice records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt)`<br>`Cloud:docs/storage-plans.md (new), Cloud:docs/development.md, Cloud:docs/prf-07-foundation-proof.md (path references only) and Cloud:AGENTS.md (factual description of the module projects and the plan root)` |
| Shared resources | [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append), [RES-cloud-storage-plans](../shared-resources.md#res-cloud-storage-plans) (append) |
| Validation | offline architecture/import tests (no forbidden cross-module reference), plan-hash tests, wrong-container/public-access refusal tests, AOT compile |
| Completion evidence | architecture/import/plan-hash/wrong-container/public-access refusal test results, source commit and plan-manifest hash |
| Baseline (unreviewed unless accepted) | not-started Observed, unreviewed: PRF.07 (delivered) left a proof bridge in src/ArcForges.Cloud/Storage and src/ArcForges.Cloud/Hmac with its plans in src/ArcForges.Cloud/Storage/Plans; no module project, Storage.D1 project or storage/plans root exists yet |
| Notes | Foundation task and the security-model proof: if the C#-decides/Worker-executes-approved-SQL-only boundary is wrong, every module built on it inherits the defect. Every module task (Identity, Sync, Resource, etc.) in this and other areas starts against this. |

<a id="task-cloud-03"></a>

### CLOUD.03 — D1 migration runner and exact physical mapping

**Outcome.** Model-04's full physical manifest is implemented: migrations, typed exact bind/result adapters for D1's signed64/uint64/Decimal/JSON/FTS5 quirks, and expand/backfill/fenced-cutover migration mode support.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-03` and ledger record `ledger/tasks/cloud-03.md` in the Plan repository; task branch `task/cloud-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L · early risk proof |
| Obligations | [WP-21.03](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) — full<br>[WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21) §6 Impacts -- migration/compatibility manifests include source/schema/plan/ABI/runtime versions — package-level obligation contribution |
| Provides | d1-physical-schema; d1-migration-runner |
| Start prerequisites | **artifact** [CLOUD.02](#task-cloud-02) — module boundary projects to attach physical tables to (physical table name = <module>_<snake_case_entity>). *Why:* physical mapping is organized per module boundary; there is nothing to migrate schema for without the module projects existing |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.04](#task-cloud-04), [CLOUD.07](#task-cloud-07), [CLOUD.09](#task-cloud-09), [CLOUD.10](#task-cloud-10), [CLOUD.11](#task-cloud-11), [CLOUD.39](#task-cloud-39), [CLOUD.48](#task-cloud-48), [CLOUD.70](#task-cloud-70), [COM.16](commerce.md#task-com-16) |
| Write scope | `Cloud:src/ArcForges.Cloud.Storage.D1/Migrations/** (the numbered, checksum-locked D1 migrations and the append-only migration lock; RES-cloud-d1-migrations)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Physical/** (the checked-in physical manifest, its generated C# column maps, the typed exact bind/result adapters and their shared vectors)`<br>`Cloud:eng/migrations/** and Cloud:eng/verification/physical-schema.ts (the migration runner with its D1 clients and sequence assignment, and the manifest validator, baseline emitter and migration-to-manifest drift check; Node tooling like eng/verification/storage-plans.ts, because migrations run from the gated deployment job and never from the Container)`<br>`Cloud:tests/ArcForges.Cloud.Tests/Physical/** and Cloud:tests/ArcForges.Cloud.Tests/Vectors/physical-*.json and Cloud:tests/worker/d1-*.test.ts (adapter, manifest, migration and conformance tests, new files only)`<br>`Cloud:package.json (only the new npm scripts and the new test files in the test list), Cloud:tsconfig.json (only the include of eng/migrations) and Cloud:.dockerignore (only the admission rule of the new Physical source folder, so the image build context holds the sources that compile into the host)`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/cloud-03-*.json (new immutable successor chained from the then-active receipt, only because hash-bound project and release inputs change; no coordinate, integrity value or closure entry changes)`<br>`Cloud:eng/provenance/** (immutable successor release profile, Worker bundle and runtime-notice records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt)`<br>`Cloud:docs/d1-physical-schema.md (new, factual description of the manifest, the adapters, the migration runner and its modes) and Cloud:docs/storage-plans.md and Cloud:AGENTS.md (only factual pointers if the description of the storage layer changes)` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | offline unit tests for bind/result adapters; opt-in local runtime tests against a real D1 instance for signed64/uint64/Decimal/JSON/FTS5, interrupted migration, stale backfill and compatible rollback per docs/validation-policy.md |
| Completion evidence | actual D1 signed64/uint64/decimal/JSON/FTS5 conformance results, interrupted-migration/stale-backfill/rollback test results, source commit |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no migrations or physical mapping code exists |
| Notes | Early risk proof: D1's real type/SQL quirks (signed 64-bit only, no native uint64/Decimal, JSON1, FTS5 behavior) affect the physical design of all 19 modules' tables. Getting the bind/result adapters wrong here would force rework across every later module task in every area that stores data in D1. |

<a id="task-cloud-04"></a>

### CLOUD.04 — Receipts, outbox, inbox dedup and change archive

**Outcome.** Every atomic guarded write also produces its owner receipt, outbox entry and change-archive row in the same D1 batch; inbox dedup makes replay a no-op; publication is contiguous (no gaps).

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-04` and ledger record `ledger/tasks/cloud-04.md` in the Plan repository; task branch `task/cloud-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-21.04](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.04) — full |
| Provides | d1-receipts-outbox |
| Start prerequisites | **artifact** [CLOUD.02](#task-cloud-02) — the D1 named-plan bridge to add receipt/outbox/inbox writes inside. *Why:* receipts/outbox are written as part of the same guarded plan execution the bridge provides<br>**artifact** [CLOUD.03](#task-cloud-03) — physical platform.command/outbox/inbox tables (data-model/01 §2 platform infra tables). *Why:* there is no physical table to write receipts into before the migration runner defines it |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.05](#task-cloud-05), [CLOUD.10](#task-cloud-10), [CLOUD.31](#task-cloud-31), [CLOUD.39](#task-cloud-39), [COM.16](commerce.md#task-com-16), [SIM.04](simulator.md#task-sim-04) |
| Write scope | `Cloud:src/ArcForges.Cloud.Storage.D1/Receipts/** (the commit tail builder, the command receipt and its replay classification, the inbox dedup)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Outbox/** (outbox streams, the contiguous publisher with its guarded acknowledgement and reconciliation, attempts, dead letter and requeue) and Cloud:src/ArcForges.Cloud.Storage.D1/Archive/** (the change archive reader with its record-hash verification and the acknowledged watermark)`<br>`Cloud:storage/plans/platform/** and the generated plan manifest Cloud:worker/storage/plans.generated.ts and Cloud:src/ArcForges.Cloud.Storage.D1/PlanManifest.g.cs (the platform owner's named plans over platform_ tables only: receipt and inbox reads and writes, stream state, outbox select, acknowledgement, attempt, dead letter and requeue, archive select and acknowledgement; the manifest hash is regenerated by the author after rebase; RES-cloud-storage-plans)`<br>`Cloud:eng/verification/storage-plans.ts and the new Cloud:eng/verification/commit-tail.ts (only the commit-tail directive and its verification: a module write plan declares the canonical commit tail or the reason it has none, a plan that declares it starts with a commit-guard insert and ends with the exact canonical statements, and the one shared definition of that tail; no change to the table-ownership rule, the statement grammar or the generated output format)`<br>`Cloud:src/ArcForges.Cloud.Storage.D1/Physical/manifest/platform.json, Cloud:src/ArcForges.Cloud.Storage.D1/Physical/PhysicalSchema.g.cs and Cloud:src/ArcForges.Cloud.Storage.D1/Migrations/** (only the three new platform tables of model 01 section 2, platform.sequence_stream, platform.outbox_position and platform.change_archive, as one append-only expand migration numbered at merge by the integration owner; RES-cloud-d1-migrations; the guard table platform.command_guard is CLOUD.06's and is only consumed here; no existing table, column, trigger or locked migration changes)`<br>`Cloud:tests/ArcForges.Cloud.Tests/Receipts/**, Cloud:tests/ArcForges.Cloud.Tests/Outbox/**, Cloud:tests/ArcForges.Cloud.Tests/Archive/**, Cloud:tests/ArcForges.Cloud.Tests/Vectors/commit-tail*.json, Cloud:tests/worker/commit-tail*.test.ts, Cloud:tests/worker/d1-receipts*.test.ts, Cloud:tests/worker/support/** (new files only), Cloud:eng/verification/d1-receipts-local.ts (the explicit opt-in run against workerd's D1), and the minimal edits of existing tests that the new tables and plans require: the pinned table inventory counts and the per-table monotonic fixtures of Cloud:tests/ArcForges.Cloud.Tests/Physical/** and Cloud:tests/worker/d1-physical-schema.test.ts, the hard-coded next migration numbers of Cloud:tests/worker/d1-migration-runner.test.ts (now derived from the catalog), and the owner list and scope rule of Cloud:tests/worker/storage-plan-ownership.test.ts and Cloud:tests/worker/storage-plans-generator.test.ts for the platform owner's plans, and the pinned Worker bundle hash and size of Cloud:tests/worker/release-provenance.test.ts, which the regenerated plan dictionary changes`<br>`Cloud:package.json (only the new npm scripts and the new test files in the test list), Cloud:tsconfig.json (only includes of new Node files) and Cloud:.dockerignore (only the admission rule of any new Storage.D1 source folder, so the image build context holds the sources that compile into the host)`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/cloud-04-*.json (new immutable successor chained from the then-active receipt, only because hash-bound project and release inputs change; no coordinate, integrity value or closure entry changes)`<br>`Cloud:eng/provenance/** (immutable successor release profile, Worker bundle and runtime-notice records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt)`<br>`Cloud:docs/d1-receipts-outbox.md (new, factual description of the commit tail, the receipts, the outbox streams, the inbox and the change archive) and Cloud:docs/storage-plans.md, Cloud:docs/d1-physical-schema.md and Cloud:AGENTS.md (only factual pointers if the description of the storage layer changes)` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append), [RES-cloud-storage-plans](../shared-resources.md#res-cloud-storage-plans) (append) |
| Validation | offline unit tests plus opt-in local D1 runtime tests: constraint-guard failure rolls back all rows, zero-row CAS cannot publish, duplicate/lost ack reconciles |
| Completion evidence | constraint-guard rollback, zero-row-CAS and duplicate/lost-ack reconciliation results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no receipt/outbox/inbox code exists |
| Notes | This generic outbox mechanism is distinct from (a) [WP-24.04](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.04)'s DO wake/live-feed publisher and (b) [WP-25.02](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.02)'s sync.change publish_seq bootstrap publisher; both consume this task's committed outbox rows but each adds its own D1-batch publication logic.. Planning repair 2026-10-05: the write scope is bound to the real Cloud layout (the commit-tail directive in the plan generator, the three new platform tables as one expand migration, the platform owner's plans, tests and the factual document), as for CLOUD.01, CLOUD.02, CLOUD.03 and COM.05. The physical tables of model 01 had no sequence and no change-archive field list, so model 01 section 2 and model 04 sections 4 and 5 now define them; the guard table is defined by the CLOUD.06 repair (platform.command_guard) and CLOUD.04 follows its guards with the commit tail and the release, which that repair's generated family plans append the same way. The module-facing exposure of the commit tail (a port in ArcForges.Cloud.Modules.Abstractions) belongs to the generic plan-execution port of COM.16; this task delivers the mechanism inside Storage.D1. The finite-job lease and fence plans over platform.job_lease are not part of [WP-21.04](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.04) and are not delivered here. |

<a id="task-cloud-05"></a>

### CLOUD.05 — Finite durable jobs (Cron/Queue/Workflow-woken endpoints)

**Outcome.** Perpetual hosted loops are replaced by Cron/Queue/Workflow-woken C# endpoints bounded to <=100 items/20s per job with checkpoint/receipt/lease-then-yield semantics.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-05` and ledger record `ledger/tasks/cloud-05.md` in the Plan repository; task branch `task/cloud-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-21.01](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.01) — full |
| Provides | finite-job-runner |
| Start prerequisites | **artifact** [CLOUD.01](#task-cloud-01) — the deployed Worker/Container ingress to attach Cron/Queue/Workflow triggers to. *Why:* finite jobs are woken through the same Worker deployment<br>**artifact** [CLOUD.04](#task-cloud-04) — receipt/lease primitives to checkpoint job progress. *Why:* a finite job's checkpoint/receipt/lease-then-yield cycle reuses the same guarded receipt mechanism, not a second one<br>**artifact** [CLOUD.69](#task-cloud-69) — the Cloud-side correlation seam for wake messages and job-slice calls. *Why:* propagating correlation once is a Cloud seam ([CR-06](../../../architecture/13-observability-and-operations.md#rule-cr-06)); this task builds on it instead of adding per-module propagation |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.10](#task-cloud-10), [CLOUD.33](#task-cloud-33), [CLOUD.45](#task-cloud-45), [HAR.00](harness.md#task-har-00), [SIM.03](simulator.md#task-sim-03) |
| Write scope | `Cloud:src/ArcForges.Cloud.Jobs/**` |
| Shared resources | [RES-cloud-deployment](../shared-resources.md#res-cloud-deployment) (append) |
| Validation | opt-in local runtime tests: sleep/restart, duplicate wake, delayed delivery, stale lease, paused simulator continuation |
| Completion evidence | sleep/restart, duplicate-wake, delayed-delivery, stale-lease and paused-simulator-continuation results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no job runner exists |
| Notes | This is the generic mechanism later background jobs plug into: [WP-25.02](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.02)'s publisher, [WP-25.06](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.06) realm-transfer jobs, [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) backup jobs, notification delivery retries. Planning repair 2026-10-05: job wake messages and job-slice calls carry correlationId and causationId through the CLOUD.69 seam; this task keeps them when it replaces the proof queue consumer (no new write scope). |

<a id="task-cloud-06"></a>

### CLOUD.06 — Shared atomic family guarded-batch engine

**Outcome.** A reusable D1 guarded-batch executor exists that enforces the fixed [SU-04](../../../architecture/04-desktop-application-architecture.md#rule-su-04) module lock order (Config->Identity->Workspace->Device->Entitlement->Commerce->Policy->Agent->Chat->Scope->Task->Search->PackageCatalog->Notification->Resource->Sync->Audit) and provides authorization/revision/policy/balance/lease guard primitives that any shared-transaction family can compose.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-06` and ledger record `ledger/tasks/cloud-06.md` in the Plan repository; task branch `task/cloud-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-21.05](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05) — generic guarded-batch engine and fixed [SU-04](../../../architecture/04-desktop-application-architecture.md#rule-su-04) module lock-order enforcement only; each module's own family participant list is a separate obligation carried by that module's own task (see coverage) |
| Provides | shared-atomic-family-engine |
| Start prerequisites | **artifact** [CLOUD.02](#task-cloud-02) — the D1 named-plan bridge, since a guarded batch is executed as one named plan. *Why:* the family engine is built on top of the plan-execution mechanism, not a separate execution path |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.63](#task-cloud-63) — at least two real module family participants exercising the engine under contention (e.g. Identity's auth/enrollment family and Sync's synced-content-mutation family). *Why:* [WP-21.05](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05)'s own completion gate requires evidence of 'two Containers contend, stale holder cannot finalize, exact credits and sync cursor safety' -- 'exact credits' is Commerce and 'sync cursor safety' is this area's own [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25); the generic engine alone cannot demonstrate this |
| Unblocks | [CLOUD.07](#task-cloud-07), [CLOUD.10](#task-cloud-10), [CLOUD.11](#task-cloud-11), [CLOUD.13](#task-cloud-13), [CLOUD.39](#task-cloud-39), [CLOUD.42](#task-cloud-42), [CLOUD.46](#task-cloud-46), [CLOUD.63](#task-cloud-63), [COM.16](commerce.md#task-com-16), [SIM.03](simulator.md#task-sim-03) |
| Write scope | `Cloud:src/ArcForges.Cloud.Storage.D1/SharedFamilies/**` |
| Shared resources | [RES-shared-transaction-families](../shared-resources.md#res-shared-transaction-families) (append) |
| Validation | offline unit tests for the guard/lock-order primitives; opt-in local D1 runtime tests: two Containers contend, stale holder cannot finalize |
| Completion evidence | lock-order enforcement test results, contention/stale-holder test results, source commit |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no shared-family engine exists |
| Notes | Every module task that participates in a named shared-transaction family (CLOUD.11/13 Identity's auth-enrollment/device-revocation families, CLOUD.39 Sync's synced-content-mutation family, CLOUD.42 Resource's upload-lifecycle family, CLOUD.53 realm-transfer family) declares a start edge on this task and fills in its own participant logic; [WP-21.05](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05) substep coverage therefore spans CLOUD.06 plus those module tasks with differing `part` text. |

<a id="task-cloud-07"></a>

### CLOUD.07 — Capacity, Container/D1 integration producer and harness

**Outcome.** Model-04 named plans run through guarded-batch fixtures under measured load; the primary-authorization path, route/service-binding/outbound-handler matrix, job-slice and SimulationPacer infrastructure exist; the [L-16](../../../assurance/release-gates.md#rule-l-16) measurement harness and a proposed capacity report are produced.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-07` and ledger record `ledger/tasks/cloud-07.md` in the Plan repository; task branch `task/cloud-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-21.06](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.06) — all work except the parts mapped to SIM.10 |
| Provides | capacity-harness; simulation-pacer-do |
| Start prerequisites | **artifact** [CLOUD.02](#task-cloud-02) — module boundary + plan bridge to issue guarded-batch fixture plans against. *Why:* capacity measurement runs synthetic guarded batches through the real bridge, not a separate harness<br>**artifact** [CLOUD.03](#task-cloud-03) — physical D1 schema to measure real write/read latency against. *Why:* capacity numbers are meaningless without the real physical tables<br>**artifact** [CLOUD.06](#task-cloud-06) — the guarded-batch engine, since capacity fixtures are guarded batches. *Why:* measuring contention requires the real guard/lock-order engine, not a mock |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.70](#task-cloud-70) — the gated migration step that applies the locked migrations to the deployed D1 database. *Why:* the real D1 rollback, duplicate, competing-writer and cold-start measurements run against a deployed schema |
| Unblocks | [CLOUD.10](#task-cloud-10), [COM.07](commerce.md#task-com-07), [SIM.03](simulator.md#task-sim-03), [SIM.10](simulator.md#task-sim-10) |
| Permitted substitutes | [SUB-guarded-batch-capacity-fixtures](../substitutes.md#sub-guarded-batch-capacity-fixtures) |
| Write scope | `Cloud:src/ArcForges.Cloud.Capacity/**`<br>`Cloud:wrangler.json` |
| Shared resources | [RES-cloud-deployment](../shared-resources.md#res-cloud-deployment) (append) |
| Validation | opt-in local + real-deployed D1 rollback/duplicate/competing-writer/cold-start tests; public/internal denial, blocked egress, forged service headers, stream-limit and headroom measurement |
| Completion evidence | [L-16](../../../assurance/release-gates.md#rule-l-16) measurement harness output, proposed capacity report, real D1 rollback/duplicate/competing-writer/cold-start results, public/internal denial and forged-header refusal results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no capacity harness exists; wrangler.json today has a single lite/1-instance placeholder container |
| Notes | Can proceed in parallel with [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22)/23/24/25 module work once CLOUD.01-04/06 exist, because it uses its own guarded-batch fixtures rather than waiting for real module business logic. |

<a id="task-cloud-08"></a>

### CLOUD.08 — Failure isolation and readiness surface

**Outcome.** Ingress/Container/D1/DO/R2/Queue health are exposed separately, and a missing binding or plan-hash mismatch fails readiness rather than allowing partial execution to appear successful; logs remain no-content.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-08` and ledger record `ledger/tasks/cloud-08.md` in the Plan repository; task branch `task/cloud-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-21.07](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.07) — full |
| Provides | readiness-surface |
| Start prerequisites | **artifact** [CLOUD.01](#task-cloud-01) — the deployed ingress/Container to expose readiness for. *Why:* readiness reports on the pipeline CLOUD.01 builds<br>**artifact** [CLOUD.02](#task-cloud-02) — the plan-manifest hash to check for mismatch. *Why:* one of the required readiness failure modes is a plan-hash mismatch |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.10](#task-cloud-10), [PRF.08](runtime-proofs.md#task-prf-08) |
| Write scope | `Cloud:src/ArcForges.Cloud.Host/Readiness/**` |
| Validation | opt-in local runtime tests: missing binding/plan mismatch fails readiness, not successful partial execution |
| Completion evidence | missing-binding and plan-mismatch readiness-failure results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists; only a Hello /api/healthz stub |
| Notes | Can be built in parallel with [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22)/23/24/25 once CLOUD.01/02 exist; readiness for R2/Queue/DO bindings can be checked even while those bindings are still otherwise unused stubs. |

<a id="task-cloud-09"></a>

### CLOUD.09 — Selfhost.v1 deployment profile

**Outcome.** An operator-owned Cloudflare deployment/config/realm descriptor exists for self-hosting, with default payment disabled, separate keys/identity/providers from the official realm, immutable artifacts and independent backup requirements preserved.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-09` and ledger record `ledger/tasks/cloud-09.md` in the Plan repository; task branch `task/cloud-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-21.08](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.08) — full |
| Provides | selfhost-deployment-profile |
| Start prerequisites | **artifact** [CLOUD.01](#task-cloud-01) — a deployable Worker/Container image to define a second deployment profile for. *Why:* selfhost.v1 packages the same artifact under a different config, not a different build<br>**artifact** [CLOUD.03](#task-cloud-03) — the D1 physical schema/migration runner to provision a fresh realm's database. *Why:* fresh account/realm provisioning needs real migrations to run against |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.70](#task-cloud-70) — the gated migration step to provision a fresh realm's database. *Why:* fresh development account and realm provisioning applies the schema through the same step |
| Unblocks | [CLOUD.10](#task-cloud-10) |
| Write scope | `Cloud:docs/deployment.md`<br>`Cloud:eng/selfhost/**` |
| Shared resources | [RES-cloud-deployment](../shared-resources.md#res-cloud-deployment) (append) |
| Validation | opt-in local + real Cloudflare dev-account tests: fresh development account/realm provisioning, missing binding/secret/unsupported descriptor/redirect failures, no official token acceptance |
| Completion evidence | fresh provisioning, missing-binding/secret refusal, and no-official-token-acceptance results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no selfhost profile exists; wrangler.json has only the single official arcforges.com route/environment |
| Notes | [WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21)'s own completion gate states this task hands [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) 'a runnable deployment and complete configuration inventory'; production [PG-25](../../../assurance/open-gates-register.md#rule-pg-25) evidence stays external. Can run in parallel with [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22)/23/24/25 once CLOUD.01/03 exist. |

<a id="task-cloud-10"></a>

### CLOUD.10 — Owned-artifact closure and launch-capacity.v1 acceptance

**Outcome.** Every [WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21) substep is complete, built/packed once, and consumed as exact candidate bytes from a clean environment; launch-capacity.v1 is produced and tested (four fixed standard-2 slots, no per-account instance creation, idle sleep/wake, pre-dispatch refusal vs unknown dispatched outcome, control-slot reserve, Vectorize/R2 reservation thresholds at 60/70/80/90%).

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-10` and ledger record `ledger/tasks/cloud-10.md` in the Plan repository; task branch `task/cloud-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-21.90](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.90) — full, including the Launch configuration acceptance subsection (launch-capacity.v1, [PG-26](../../../assurance/open-gates-register.md#rule-pg-26))<br>[WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21) §6 Impacts -- migration/compatibility manifests include source/schema/plan/ABI/runtime versions — package-level obligation contribution |
| Provides | wp21-closure |
| Start prerequisites | **artifact** [CLOUD.39](#task-cloud-39) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SIM.10](simulator.md#task-sim-10) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.01](#task-cloud-01) — final candidate build. *Why:* closure requires every preceding substep complete<br>**integration** [CLOUD.02](#task-cloud-02) — final candidate build. *Why:* closure requires every preceding substep complete<br>**integration** [CLOUD.03](#task-cloud-03) — final candidate build. *Why:* closure requires every preceding substep complete<br>**integration** [CLOUD.04](#task-cloud-04) — final candidate build. *Why:* closure requires every preceding substep complete<br>**integration** [CLOUD.05](#task-cloud-05) — final candidate build. *Why:* closure requires every preceding substep complete<br>**integration** [CLOUD.06](#task-cloud-06) — final candidate build. *Why:* closure requires every preceding substep complete<br>**integration** [CLOUD.07](#task-cloud-07) — final candidate build. *Why:* closure requires every preceding substep complete<br>**integration** [CLOUD.08](#task-cloud-08) — final candidate build. *Why:* closure requires every preceding substep complete<br>**integration** [CLOUD.09](#task-cloud-09) — final candidate build. *Why:* closure requires every preceding substep complete<br>**integration** [CLOUD.70](#task-cloud-70) — final candidate build. *Why:* closure requires the deployment pipeline to apply the migrations it ships against |
| Unblocks | [REL.06](release.md#task-rel-06) |
| Write scope | `Cloud:artifacts/candidate/**` |
| Shared resources | [RES-cloud-deployment](../shared-resources.md#res-cloud-deployment) (append) |
| Validation | package/contract/owner/version compatibility, failure/recovery and the real boundaries above; publish/promote only the tested immutable bytes in the producer CI sequence (matches the existing candidate->verify->deploy CI job sequence) |
| Completion evidence | cold-start and measured cost inputs; [PG-26](../../../assurance/open-gates-register.md#rule-pg-26) explicitly cannot close on a localhost benchmark |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: n/a -- closure task |
| Notes | Gate: [PG-26](../../../assurance/open-gates-register.md#rule-pg-26). A localhost benchmark cannot close it per [WP-21.90](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.90)'s own text. |

<a id="task-cloud-11"></a>

### CLOUD.11 — Core identity model (realm, user, authIdentity, single-owner workspace)

**Outcome.** Realm, user, authentication identity and single-owner workspace exist with ownership as a direct workspace.owner_user_id check; no membership/role/seat table exists anywhere in schema, contracts or operations.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-11` and ledger record `ledger/tasks/cloud-11.md` in the Plan repository; task branch `task/cloud-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-22.00](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.00) — all work except the parts mapped to CLOUD.20 |
| Provides | identity-core-model |
| Start prerequisites | **artifact** [CLOUD.02](#task-cloud-02) — module boundary + D1 plan bridge to implement the Identity module against. *Why:* Identity is one of the 19 modules; it cannot be written before the module boundary/plan-bridge mechanism exists<br>**artifact** [CLOUD.03](#task-cloud-03) — physical D1 schema/migration runner for identity.* tables. *Why:* the identity schema needs real migrations, not an improvised table<br>**artifact** [CLOUD.06](#task-cloud-06) — the shared atomic family engine, since core identity operations (enrollment, workspace provisioning) are shared-transaction families. *Why:* [WO-01](../../../architecture/data-model/01-cloud-data-model.md#rule-wo-01)..05/no-membership rules are enforced as part of a guarded family write, not a plain CRUD write |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.12](#task-cloud-12), [CLOUD.13](#task-cloud-13), [CLOUD.16](#task-cloud-16), [CLOUD.19](#task-cloud-19), [CLOUD.20](#task-cloud-20), [GOV.16](governance.md#task-gov-16), [SRCH.03](search.md#task-srch-03) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Identity/Core/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append), [RES-cloud-storage-plans](../shared-resources.md#res-cloud-storage-plans) (append), [RES-shared-transaction-families](../shared-resources.md#res-shared-transaction-families) (append) |
| Validation | offline structural tests: identity-change continuity, no membership/role/invitation/seat concept anywhere, no capability treats an auth identity as a user; AOT compile |
| Completion evidence | identity-continuity and structural-separation test results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no identity module exists |
| Notes | First real module built on the [WP-21](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21) foundation; unlocks the rest of [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22). |

<a id="task-cloud-12"></a>

### CLOUD.12 — Native and browser authentication with real Postmark/SES mail delivery

**Outcome.** Native authorize/token PKCE ceremony and minimal browser login UI work with passkey/email and configured self-host OIDC/password; real Postmark-primary/SES-secondary delivery and outcome adapters exist and prove live delivery/recovery, not a stub.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-12` and ledger record `ledger/tasks/cloud-12.md` in the Plan repository; task branch `task/cloud-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-22.01](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.01) — full |
| Provides | real-email-delivery; native-browser-auth |
| Start prerequisites | **artifact** [CLOUD.11](#task-cloud-11) — the core identity/authIdentity model to attach auth methods to. *Why:* authentication ceremonies operate on the AuthIdentity/User records CLOUD.11 defines |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.15](#task-cloud-15), [CLOUD.17](#task-cloud-17), [CLOUD.18](#task-cloud-18), [CLOUD.20](#task-cloud-20), [CLOUD.68](#task-cloud-68), [OPS.09](operations.md#task-ops-09), [WEB.10](web.md#task-web-10) |
| Permitted substitutes | [SUB-postmark-ses-test-recordings](../substitutes.md#sub-postmark-ses-test-recordings) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Identity/Auth/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Notification/**` |
| Validation | actual email delivery/recovery and prepared-secondary tests; PKCE/state/redirect/code-replay, Credential Manager/RP origin fixtures, refresh contention and revocation -- real provider evidence, no CI hosted live-service run (per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), this stays local opt-in) |
| Completion evidence | real provider identity flow results; required accounts/DNS recorded as external inputs, never replaced by a stub acceptance |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: no auth ceremonies or mail adapters exist |
| Notes | Must-be-real-early per implementation-sequence §3 ('Identity, refresh/session contention and real email delivery/recovery at WP22' is explicitly listed as Must be real early, not Push-until-later). Keep this must-be-real-early placement; do not move it later. |

<a id="task-cloud-13"></a>

### CLOUD.13 — Device, installation, instance and session (four distinct concepts)

**Outcome.** Device, installation, instance and session are four distinct concepts with four lifecycles; device identity is stable but not a hardware fingerprint; device revocation cascades to sessions and push registrations.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-13` and ledger record `ledger/tasks/cloud-13.md` in the Plan repository; task branch `task/cloud-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-22.02](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.02) — full |
| Provides | device-session-model |
| Start prerequisites | **artifact** [CLOUD.11](#task-cloud-11) — the core identity model a device/session attaches to. *Why:* sessions belong to a user/device; there is nothing to attach to before CLOUD.11<br>**artifact** [CLOUD.06](#task-cloud-06) — the shared atomic family engine, since device revocation is a named shared-transaction family. *Why:* cascading revocation across sessions/registrations is guarded, not a plain cascade delete |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.07](android.md#task-and-07), [CLOUD.14](#task-cloud-14), [CLOUD.15](#task-cloud-15), [CLOUD.19](#task-cloud-19), [CLOUD.20](#task-cloud-20), [CLOUD.21](#task-cloud-21), [DEV.01](device-bridge.md#task-dev-01) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Identity/Device/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append), [RES-shared-transaction-families](../shared-resources.md#res-shared-transaction-families) (append) |
| Validation | offline structural distinction-matrix tests; revocation-cascade tests; hardware-change survival test |
| Completion evidence | four-concept distinction matrix and revocation cascade results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-14"></a>

### CLOUD.14 — Device trust and remote gating

**Outcome.** Trust levels per device exist with remote access defaulting to off; raising trust requires an explicit act with step-up; remote capability is derived from trust, never from mere session possession.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-14` and ledger record `ledger/tasks/cloud-14.md` in the Plan repository; task branch `task/cloud-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-22.03](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.03) — full |
| Provides | device-trust-gating |
| Start prerequisites | **artifact** [CLOUD.13](#task-cloud-13) — the device/session model to attach trust levels to. *Why:* trust is a property of the device record CLOUD.13 defines |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.20](#task-cloud-20) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Identity/Trust/**` |
| Validation | offline default-off assertion, trust-elevation-requires-step-up test, session-alone-insufficient test |
| Completion evidence | default-off and session-insufficiency results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-15"></a>

### CLOUD.15 — Step-up challenges for sensitive operations

**Outcome.** Step-up challenges exist for the enumerated sensitive operations, bounded validity window, no app-unlock substitution; step-up state is per session and per operation class.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-15` and ledger record `ledger/tasks/cloud-15.md` in the Plan repository; task branch `task/cloud-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-22.04](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.04) — the step-up mechanism itself and coverage for Cloud/Identity-owned sensitive operations (credential change, recovery, deletion, trust elevation); full coverage across every enumerated operation in every module is completed as each owning module wires it in -- see IM.step-up-cross-product-coverage |
| Provides | step-up-mechanism |
| Start prerequisites | **artifact** [CLOUD.12](#task-cloud-12) — real authentication methods to re-assert during a step-up challenge. *Why:* step-up reuses the same passkey/email/OIDC methods CLOUD.12 implements<br>**artifact** [CLOUD.13](#task-cloud-13) — the session model to scope step-up state to. *Why:* step-up state is per session and per operation class |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.16](#task-cloud-16), [CLOUD.20](#task-cloud-20), [CLOUD.66](#task-cloud-66) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Identity/StepUp/**` |
| Validation | offline coverage-enumeration test, window-expiry test, app-unlock-does-not-substitute negative test |
| Completion evidence | step-up coverage, expiry and non-substitution results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | Aggregate-gate risk: [WP-22.04](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.04)'s completion gate says 'every enumerated operation demands step-up', but the full enumeration spans Commerce ([WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42)), PublicApi ([WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23)) and client apps outside this area. This task delivers the mechanism plus Identity's own operations; see integration_proposals for the cross-product completion. |

<a id="task-cloud-16"></a>

### CLOUD.16 — PAT and actor authorization

**Outcome.** patEligible/scopes metadata, hash-only token storage, expiry/revocation and one-time display after step-up are implemented; the actor chain is preserved and customer tokens are denied on operator/internal/local boundaries.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-16` and ledger record `ledger/tasks/cloud-16.md` in the Plan repository; task branch `task/cloud-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-22.05](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.05) — full |
| Provides | pat-actor-authorization |
| Start prerequisites | **artifact** [CLOUD.11](#task-cloud-11) — the core identity model a token belongs to. *Why:* a PAT is issued to a user/workspace |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.15](#task-cloud-15) — the step-up mechanism, since one-time PAT display happens after step-up. *Why:* PAT issuance display is gated by step-up per the WP text |
| Unblocks | [CLOUD.19](#task-cloud-19), [CLOUD.20](#task-cloud-20), [CLOUD.63](#task-cloud-63), [EXT.06](extensions.md#task-ext-06), [EXT.08](extensions.md#task-ext-08) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Identity/Tokens/**` |
| Validation | offline enumeration of eligible/denied methods from the generated manifest; cookie+bearer conflict, scope escalation and agent-substitution negative vectors |
| Completion evidence | no missing/default PAT metadata, no generic token bypass |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-17"></a>

### CLOUD.17 — Recovery, account states and deletion

**Outcome.** Recovery flows resist modelled abuse; account states (active/restricted/suspended/pending-deletion) have defined capability; deletion has a grace period, explicit scope of what is/isn't deleted, and never touches local data.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-17` and ledger record `ledger/tasks/cloud-17.md` in the Plan repository; task branch `task/cloud-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-22.06](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.06) — full |
| Provides | recovery-account-states |
| Start prerequisites | **artifact** [CLOUD.12](#task-cloud-12) — real auth methods (passkey/email/OIDC) to build recovery flows on. *Why:* recovery re-establishes one of the real auth methods CLOUD.12 implements |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.19](#task-cloud-19), [CLOUD.20](#task-cloud-20), [CLOUD.50](#task-cloud-50) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Identity/Recovery/**` |
| Validation | offline recovery-abuse tests, state-transition capability matrix, deletion-preserves-local-data test |
| Completion evidence | recovery abuse-resistance, state matrix and deletion results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-18"></a>

### CLOUD.18 — Independent native session integration (Platform client primitives)

**Outcome.** System browser, per-product redirects, secure storage and installation-bound tokens are integrated into Platform client primitives; each client owns its own session, no token sharing/device SSO.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/cloud-18` and ledger record `ledger/tasks/cloud-18.md` in the Plan repository; task branch `task/cloud-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-22.07](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.07) — full |
| Provides | native-session-client-primitives |
| Start prerequisites | **artifact** [CLOUD.12](#task-cloud-12) — the real native PKCE ceremony endpoints to integrate against. *Why:* the client primitive drives the server-side PKCE flow CLOUD.12 implements<br>**artifact** [PLT.40](platform.md#task-plt-40) — the local security foundation's secure storage primitive. *Why:* installation-bound tokens are stored through the platform's existing secure-storage mechanism, not a new one |
| Entry condition | [ADOPT.02.cloud](adoption.md#task-adopt-02-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.07](android.md#task-and-07), [CLOUD.20](#task-cloud-20), [PLT.40](platform.md#task-plt-40) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Security/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | offline + opt-in local tests: separate product sign-in/sign-out, canceled/lost callback, wrong state/realm, expired code, device revoke, local history preservation |
| Completion evidence | per-client session isolation results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: ArcForges.Security building block not yet inspected in depth; |
| Notes | Cross-repo: owned by [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) but lives in DesktopPlatform. |

<a id="task-cloud-19"></a>

### CLOUD.19 — Browser cookie-session adapter and full account-surface closure

**Outcome.** The same-origin browser adapter runs in the AOT host with random hashed session/preauth/CSRF records, exact Origin checks, idle/absolute expiry, lowest-trust browser installation and one-use auth flow, with explicit cookie parsing/writing (no ASP.NET Data Protection/cookie-auth middleware); the full typed account surface is wired through the same owner ports.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-19` and ledger record `ledger/tasks/cloud-19.md` in the Plan repository; task branch `task/cloud-19` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-22.08](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.08) — full, including the 'Required implementation and closure from the final review' paragraph (complete typed account surface: profile/email, recovery-code set, scoped PAT, credential rename, session listing, four sign-out scopes, per-installation browser authorization, remote capability policy, restricted deletion-cancel reauthentication)<br>[WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) Browser-session evidence note ([WP-22.08](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.08) must pass before [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) consumes its contract; a written [P2-003](../../../decisions/phase-2-specification-decisions.md#rule-p2-003) decision alone is insufficient) — package-level obligation contribution |
| Provides | browser-session-adapter; account-surface |
| Start prerequisites | **artifact** [CLOUD.01](#task-cloud-01) — the AOT host pipeline to implement the /session/* routes in. *Why:* the browser adapter is implemented in the same fixed pipeline, with explicit cookie parsing, not a framework middleware<br>**artifact** [CLOUD.11](#task-cloud-11) — identity core model. *Why:* sessions authenticate against real user/authIdentity records<br>**artifact** [CLOUD.13](#task-cloud-13) — device/installation/session model, since browser sessions are the lowest-trust browser installation. *Why:* browser session records are installation-bound |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.16](#task-cloud-16) — PAT mechanism for the scoped-PAT account surface. *Why:* the account surface exposes scoped PAT creation, which needs CLOUD.16's token mechanism<br>**integration** [CLOUD.17](#task-cloud-17) — recovery/deletion mechanism for the deletion-cancel reauthentication surface. *Why:* the account surface's deletion-cancel path calls CLOUD.17's deletion mechanism |
| Unblocks | [AND.07](android.md#task-and-07), [CLOUD.20](#task-cloud-20), [CLOUD.21](#task-cloud-21), [CLOUD.26](#task-cloud-26), [CLOUD.29](#task-cloud-29), [WEB.11](web.md#task-web-11), [WEB.30](web.md#task-web-30) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Host/Session/**`<br>`Cloud:src/Contracts/Public/ArcForges.Contracts.PublicApi.Identity/**` |
| Validation | opt-in local + real D1 tests: one-use challenge, lost-login response, idle-vs-revoke race, expiry, replica failover, exact Origin/CSRF on unsafe RPC/session/stream/object operations, native-token route refusal, gRPC-Web stream authorization, two-products-one-OS-user isolation |
| Completion evidence | one server-owned session authority, no JS bearer, no cross-origin reuse or session resurrection; real database/concurrency, origin/CSRF/expiry and multi-replica results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | Gate: [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) (this task's contribution; [WP-23.05](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.05) contributes the other side). Feeds [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) and full portal acceptance -- [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) cannot consume this contract until it passes; a written [P2-003](../../../decisions/phase-2-specification-decisions.md#rule-p2-003) decision alone is insufficient per the WP text. |

<a id="task-cloud-20"></a>

### CLOUD.20 — Owned-artifact closure and real integration

**Outcome.** Native/Android bearer sessions, same-origin Web opaque sessions, passkeys/recovery, workspace/device rules and authenticated CF authorization ports work end-to-end using selected AOT-compatible components; real publish-mode auth/session/CSRF/origin/rotation/revocation tests pass including stale CF requests and browser credential secrecy.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-20` and ledger record `ledger/tasks/cloud-20.md` in the Plan repository; task branch `task/cloud-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-22.90](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.90) — full<br>[WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure appendix (initial enrollment/recovery/provider/account/SSO methods wired end-to-end in client journeys) — [P2-010](../../../decisions/phase-2-specification-decisions.md#rule-p2-010) required behavior and closure appendix (initial enrollment/recovery/provider/account/SSO methods wired end-to-end in client journeys)<br>[WP-22.00](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.00) — real identity/session implementation |
| Provides | wp22-closure |
| Start prerequisites | **artifact** [CON.07](contracts.md#task-con-07) — real, delivered outcome of CON.07 (Identity/session/device operation registry + native-auth and browser HTTP exceptions). *Why:* this integration exercises the real identity/session/device operation registry + native-auth and browser HTTP exceptions instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.11](#task-cloud-11) — real, delivered outcome of CLOUD.11 (Core identity model (realm, user, authIdentity, single-owner workspace)). *Why:* this integration exercises the real core identity model (realm, user, authIdentity, single-owner workspace) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.66](#task-cloud-66) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.12](#task-cloud-12) — final candidate. *Why:* closure requires every preceding [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) substep<br>**integration** [CLOUD.13](#task-cloud-13) — final candidate. *Why:* closure requires every preceding [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) substep<br>**integration** [CLOUD.14](#task-cloud-14) — final candidate. *Why:* closure requires every preceding [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) substep<br>**integration** [CLOUD.15](#task-cloud-15) — final candidate. *Why:* closure requires every preceding [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) substep<br>**integration** [CLOUD.16](#task-cloud-16) — final candidate. *Why:* closure requires every preceding [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) substep<br>**integration** [CLOUD.17](#task-cloud-17) — final candidate. *Why:* closure requires every preceding [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) substep<br>**integration** [CLOUD.18](#task-cloud-18) — final candidate. *Why:* closure requires every preceding [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) substep<br>**integration** [CLOUD.19](#task-cloud-19) — final candidate. *Why:* closure requires every preceding [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) substep |
| Unblocks | [REL.06](release.md#task-rel-06) |
| Write scope | `Cloud:artifacts/candidate/**` |
| Validation | real publish-mode auth/session/CSRF/origin/rotation/revocation tests including stale CF requests and browser credential secrecy |
| Completion evidence | owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations, real-vs-fixture status |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: n/a -- closure task |
| Notes | Merged duplicate integration or closure task formerly proposed as CON.94. |

<a id="task-cloud-21"></a>

### CLOUD.21 — Public endpoint mapping and validation

**Outcome.** Generated proto service methods are registered with exact request/reply/semantic validation from the registry; binary gRPC-Web unary calls and declared server streams go through the same owner handlers; owner mutations and the Sync allowlist are mapped exactly; no ad-hoc REST business API exists.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-21` and ledger record `ledger/tasks/cloud-21.md` in the Plan repository; task branch `task/cloud-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-23.00](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.00) — full<br>[WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) Browser-session evidence note ([WP-22.08](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.08) must pass before [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) consumes its contract; a written [P2-003](../../../decisions/phase-2-specification-decisions.md#rule-p2-003) decision alone is insufficient) — package-level obligation contribution |
| Provides | public-api-endpoints |
| Start prerequisites | **contract** [CON.91](contracts.md#task-con-91) — the handwritten-proto-generated service/method definitions to register ([D-009](../../../decisions/phase-1-foundation-decisions.md#rule-d-009) authority). *Why:* [BR-01](../../../architecture/14-build-packaging-and-release.md#rule-br-01) requires endpoints be mapped from the contract set, not hand-written<br>**artifact** [CLOUD.13](#task-cloud-13) — session model and native session validation. *Why:* handlers are registered behind authenticated, tenancy-scoped requests; native session validation is enough to start, browser sessions join at completion |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.19](#task-cloud-19) — the browser cookie-session adapter and native session validation to authenticate requests before they reach a handler. *Why:* [WP-23.00](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.00) registers handlers behind authenticated/tenancy-scoped requests; there is no caller identity without CLOUD.19/CLOUD.12 |
| Unblocks | [AND.04](android.md#task-and-04), [CLOUD.22](#task-cloud-22), [CLOUD.23](#task-cloud-23), [CLOUD.24](#task-cloud-24), [CLOUD.25](#task-cloud-25), [CLOUD.28](#task-cloud-28), [CLOUD.29](#task-cloud-29), [CLOUD.64](#task-cloud-64), [CLOUD.66](#task-cloud-66), [CLOUD.68](#task-cloud-68), [COM.13](commerce.md#task-com-13), [PRF.05](runtime-proofs.md#task-prf-05), [PRF.08](runtime-proofs.md#task-prf-08), [SIM.05](simulator.md#task-sim-05) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.PublicApi/Endpoints/**` |
| Validation | offline + opt-in tests: each method category through native and TS transport, malformed/unknown request values, denied scope before handler |
| Completion evidence | every selected operation has a concrete typed endpoint and owner; no ad-hoc REST business API |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists beyond the Hello World unary method |

<a id="task-cloud-22"></a>

### CLOUD.22 — Typed protocol and error mapping

**Outcome.** Generated ArcResult domain errors and gRPC-Web transport statuses/trailers are mapped exactly under registry 04; ProblemDetails is limited to documented HTTP exceptions.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-22` and ledger record `ledger/tasks/cloud-22.md` in the Plan repository; task branch `task/cloud-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-23.01](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.01) — full |
| Provides | typed-error-mapping |
| Start prerequisites | **artifact** [CLOUD.21](#task-cloud-21) — the endpoint registration to attach error mapping to. *Why:* error mapping wraps the handlers CLOUD.21 registers |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.26](#task-cloud-26), [CLOUD.28](#task-cloud-28), [CLOUD.64](#task-cloud-64), [CLOUD.66](#task-cloud-66), [PRF.05](runtime-proofs.md#task-prf-05), [PRF.08](runtime-proofs.md#task-prf-08) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.PublicApi/Errors/**` |
| Validation | offline + opt-in tests: HTTP200-with-error-trailers, partial frame, 64-bit values, deadline/cancel-after-dispatch, command-receipt reconciliation |
| Completion evidence | every C#/TS/Kotlin client distinguishes transport uncertainty from a domain refusal |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-23"></a>

### CLOUD.23 — Typed queries and revision preconditions

**Outcome.** Opaque scope-bound PageRequest cursors, registered typed filters and RequestMeta expected-owner-revision preconditions work; no ETag/If-Match for business RPC.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-23` and ledger record `ledger/tasks/cloud-23.md` in the Plan repository; task branch `task/cloud-23` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-23.02](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.02) — full |
| Provides | typed-query-cursors |
| Start prerequisites | **artifact** [CLOUD.21](#task-cloud-21) — endpoint registration to add query/cursor semantics to. *Why:* cursors are a property of the registered query endpoints<br>**contract** [CON.91](contracts.md#task-con-91) — the accepted foundation PageRequest/PageState and exact-value records. *Why:* [WP-23.02](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.02) implements scope-bound cursors, typed filters and exact scalar vectors against the accepted foundation contract records |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.28](#task-cloud-28), [COM.06](commerce.md#task-com-06) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.PublicApi/Queries/**` |
| Validation | offline + opt-in tests: wrong product/scope cursor, stale revision, page limits, unsupported filter/version, exact scalar vectors |
| Completion evidence | generated clients exercise the authoritative RPC query/revision rules without REST aliases |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-24"></a>

### CLOUD.24 — Idempotency and rate limiting

**Outcome.** State-changing requests accept a command identity and produce exactly one effect under retry; rate limits apply per identity and per capability class with typed refusals carrying retry guidance.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-24` and ledger record `ledger/tasks/cloud-24.md` in the Plan repository; task branch `task/cloud-24` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-23.03](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.03) — full |
| Provides | idempotency-rate-limiting |
| Start prerequisites | **artifact** [CLOUD.21](#task-cloud-21) — endpoint registration to enforce idempotency/rate limits on. *Why:* these are cross-cutting behaviors on the registered handlers |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.28](#task-cloud-28), [COM.03](commerce.md#task-com-03), [SIM.05](simulator.md#task-sim-05) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.PublicApi/Idempotency/**` |
| Validation | offline + opt-in tests: retry-produces-one-effect at the API boundary, rate-limit tests per class, actionable-guidance test |
| Completion evidence | one command produces one effect at the API boundary; rate limiting refuses with actionable guidance |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: the Hello World router already implements a simple per-IP rate limiter (HELLO_RATE_LIMITER) as a working precedent, not the real per-identity/per-capability-class mechanism |

<a id="task-cloud-25"></a>

### CLOUD.25 — Resource transport schema and future-owner boundary

**Outcome.** The complete generated upload/status/ticket/verification/owner-promotion schema and permission/error envelope is registered and exercised through declared protocol fixtures; every endpoint's real owner/fixture/replacement WP is recorded.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-25` and ledger record `ledger/tasks/cloud-25.md` in the Plan repository; task branch `task/cloud-25` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-23.04](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.04) — full (schema/transport/fixture boundary only; real R2 multipart behavior is [WP-25.05](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.05)) |
| Provides | resource-transport-schema |
| Start prerequisites | **artifact** [CLOUD.21](#task-cloud-21) — endpoint registration to add resource-transport endpoints to. *Why:* upload/status/ticket endpoints are registered the same way as other endpoints<br>**artifact** [PRF.07](runtime-proofs.md#task-prf-07) — the minimal real R2 transport probe already proved by [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06). *Why:* [WP-23.04](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.04)'s own text states 'the minimal actual R2 transport is already proved by WP06' -- this task builds the full schema on that proof, not from nothing |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.28](#task-cloud-28), [CLOUD.42](#task-cloud-42) |
| Permitted substitutes | [SUB-resource-transport-schema-fixtures](../substitutes.md#sub-resource-transport-schema-fixtures) |
| Write scope | `Cloud:src/Contracts/Public/ArcForges.Contracts.PublicApi.Resource/**`<br>`Cloud:fixtures/wire/publicapi/resource/**` |
| Validation | offline + opt-in tests: independent request/result/expiry/hash/denied-scope and encoded-body fixtures across C#/TS/Kotlin |
| Completion evidence | no missing resource schema; no claim that [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) alone delivered Resource/R2 owner behavior |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-26"></a>

### CLOUD.26 — Generated C#/TypeScript/Kotlin clients against Identity/Workspace/Device

**Outcome.** Released C# native, TypeScript gRPC-Web and Kotlin native clients work against actual Identity/Workspace/Device endpoints with native single-flight refresh, Web cookie/CSRF/Origin handling and generation-scoped callbacks outside generated code.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-26` and ledger record `ledger/tasks/cloud-26.md` in the Plan repository; task branch `task/cloud-26` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-23.05](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.05) — all work except the parts mapped to AND.07, WEB.30 |
| Provides | generated-clients-csharp-ts-kotlin |
| Start prerequisites | **artifact** [CLOUD.19](#task-cloud-19) — the real browser cookie-session adapter to test the TS client's cookie/CSRF/Origin handling against. *Why:* [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) requires this task's client evidence alongside CLOUD.19's server evidence on the same candidate closure<br>**artifact** [CLOUD.22](#task-cloud-22) — typed error mapping to test exact-value/error/header client conformance against. *Why:* client contract tests exercise the error mapping CLOUD.22 implements<br>**artifact** [PRF.10](runtime-proofs.md#task-prf-10) — the [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) Android probe artifact, explicitly named as the substitute for the future complete Android app. *Why:* [WP-23.05](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.05)'s own text: 'Use WP06 Android probe, not the future complete app' |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.07](android.md#task-and-07), [CLOUD.27](#task-cloud-27), [CLOUD.28](#task-cloud-28), [WEB.30](web.md#task-web-30) |
| Write scope | `Cloud:src/BuildingBlocks/ArcForges.CloudClient/**`<br>`Cloud:tests/PublicApiContractTests/**` |
| Validation | offline + opt-in tests: independent exact-value/current-previous-major vectors, actual [WP-22](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22) session expiry/revoke/refresh, public/internal leak rejection |
| Completion evidence | three ecosystem clients work against the actual host; owner implementations replaced by [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25)/42/52 before full release |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists; tests/ArcForges.Cloud.Consumer and tests/kotlin-consumer exist today only as Hello World consumer probes |
| Notes | Gate: [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) (this task's client-side contribution; CLOUD.19 contributes the server side). |

<a id="task-cloud-27"></a>

### CLOUD.27 — Compatibility window and bidirectional matrix

**Outcome.** The supported client window is declared with golden wire vectors per contract version; the compatibility matrix runs both directions (previous client vs current server, current client vs minimum supported server) and catches a deliberately breaking change.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-27` and ledger record `ledger/tasks/cloud-27.md` in the Plan repository; task branch `task/cloud-27` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-23.06](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.06) — full |
| Provides | compatibility-matrix |
| Start prerequisites | **artifact** [CLOUD.26](#task-cloud-26) — at least one generated client per language to build the matrix against. *Why:* the bidirectional matrix runs real generated clients from two contract versions |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.28](#task-cloud-28) |
| Write scope | `Cloud:fixtures/wire/publicapi/**`<br>`Cloud:tests/PublicApiContractTests/Compatibility/**` |
| Validation | the bidirectional matrix; a negative test asserting a breaking change fails the matrix |
| Completion evidence | bidirectional compatibility matrix passes and catches a deliberately breaking change |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-28"></a>

### CLOUD.28 — Owned-artifact closure and real integration

**Outcome.** Real C#/browser/Kotlin calls succeed against the AOT image with previous/current compatibility and complete operation mapping including auth, files and webhooks outside gRPC.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-28` and ledger record `ledger/tasks/cloud-28.md` in the Plan repository; task branch `task/cloud-28` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / L |
| Package acceptance | Records the [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-23.90](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.90) — full<br>[WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) Operator contract closure appendix -- Cloud's own share: generate/implement every operation with its eight authorization fields, operator scope and [OC-03](../../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role binding, refuse public customer/PAT/agent access, verify distinct approver/stale hash/revision/configuration/role revocation/expiry/concurrent consumption/lost receipt; the financial owners ([WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42)), configuration/policy owners ([WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44)) and console join ([WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45)) are NOT this task's obligation -- see IM.operator-contract-closure — Operator contract closure appendix -- Cloud's own share: generate/implement every operation with its eight authorization fields, operator scope and [OC-03](../../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role binding, refuse public customer/PAT/agent access, verify distinct approver/stale hash/revision/configuration/role revocation/expiry/concurrent consumption/lost receipt; the financial owners ([WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42)), configuration/policy owners ([WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44)) and console join ([WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45)) are NOT this task's obligation -- see IM.operator-contract-closure<br>[WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) Browser matrix acceptance appendix -- Cloud's own share: prove generated transports support delayed-stream polling, refusal of unavailable required auth/step-up, safe-preview refusal, preserved pending work; [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45)/47/48/49/50's own operations/site/account/chat/production-hash evidence is NOT this task's obligation -- see IM.browser-matrix-acceptance — Browser matrix acceptance appendix -- Cloud's own share: prove generated transports support delayed-stream polling, refusal of unavailable required auth/step-up, safe-preview refusal, preserved pending work; [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45)/47/48/49/50's own operations/site/account/chat/production-hash evidence is NOT this task's obligation -- see IM.browser-matrix-acceptance<br>[WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) Operator contract closure appendix (registry04 §9 + model01 operator state; eight authorization fields, operator scope, [OC-03](../../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role binding) — package-level obligation contribution<br>[WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) Browser matrix acceptance appendix (browser-support.v1, supported/degraded/blocked behavior for generated transports) — package-level obligation contribution |
| Provides | wp23-closure; public-api-transport-proven |
| Start prerequisites | **artifact** [AND.07](android.md#task-and-07) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [WEB.30](web.md#task-web-30) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.21](#task-cloud-21) — final candidate. *Why:* closure requires every preceding [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) substep<br>**integration** [CLOUD.22](#task-cloud-22) — final candidate. *Why:* closure requires every preceding [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) substep<br>**integration** [CLOUD.23](#task-cloud-23) — final candidate. *Why:* closure requires every preceding [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) substep<br>**integration** [CLOUD.24](#task-cloud-24) — final candidate. *Why:* closure requires every preceding [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) substep<br>**integration** [CLOUD.25](#task-cloud-25) — final candidate. *Why:* closure requires every preceding [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) substep<br>**integration** [CLOUD.26](#task-cloud-26) — final candidate. *Why:* closure requires every preceding [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) substep<br>**integration** [CLOUD.27](#task-cloud-27) — final candidate. *Why:* closure requires every preceding [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) substep |
| Unblocks | [CLOUD.64](#task-cloud-64), [REL.06](release.md#task-rel-06), [WEB.31](web.md#task-web-31) |
| Write scope | `Cloud:artifacts/candidate/**` |
| Validation | real C#/browser/Kotlin calls against the AOT image, previous/current compatibility, complete operation mapping including auth/files/webhooks outside gRPC |
| Completion evidence | owned artifact and real-integration receipt per [WP-23.90](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.90) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: n/a -- closure task |
| Notes | Gate: [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) (joint with CLOUD.19/CLOUD.26). |

<a id="task-cloud-29"></a>

### CLOUD.29 — Stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells)

**Outcome.** Public server-streaming shells for EventService.Watch and ExecutionService.WatchOutput exist with generated StreamFrame, re-authorizing current session/scope every 15s; real C#/browser/Kotlin binary streams work with trailers/cancel/expiry; no WebSocket path.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-29` and ledger record `ledger/tasks/cloud-29.md` in the Plan repository; task branch `task/cloud-29` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-24.00](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.00) — full |
| Provides | realtime-stream-transport |
| Start prerequisites | **artifact** [CLOUD.21](#task-cloud-21) — the endpoint-mapping pattern to register server-streaming methods alongside unary ones. *Why:* streams are registered through the same owner-handler mechanism CLOUD.21 establishes<br>**artifact** [CLOUD.19](#task-cloud-19) — session authorization to re-check every 15s on the open stream. *Why:* stream authorization reuses the same session/CSRF/Origin checks CLOUD.19 implements<br>**contract** [CON.11](contracts.md#task-con-11) — the StreamFrame/StreamPosition/ApplicationScope record definitions (contracts/10 §2). *Why:* the stream shells are typed against these generated records, not ad hoc JSON |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.07](android.md#task-and-07), [CLOUD.30](#task-cloud-30), [CLOUD.34](#task-cloud-34), [CLOUD.36](#task-cloud-36), [DEV.01](device-bridge.md#task-dev-01), [DEV.14](device-bridge.md#task-dev-14), [PRF.06](runtime-proofs.md#task-prf-06), [WEB.30](web.md#task-web-30) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.PublicApi/Streams/**` |
| Validation | opt-in real deployed C#/browser/Kotlin binary stream tests: trailers/cancel/expiry, no WebSocket path |
| Completion evidence | real binary stream trailer/cancel/expiry results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-30"></a>

### CLOUD.30 — Scoped subscription (owner/product/filter/recovery-generation binding)

**Outcome.** The feed is bound to owner/product/filter/recovery generation, one events stream plus two output streams per foreground profile; mixed-product/unauthorized feeds are refused; account-security identifiers stay separate.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-30` and ledger record `ledger/tasks/cloud-30.md` in the Plan repository; task branch `task/cloud-30` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-24.01](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.01) — all work except the parts mapped to DEV.14 |
| Provides | scoped-subscription |
| Start prerequisites | **artifact** [CLOUD.29](#task-cloud-29) — the stream connection/auth shell to bind scope onto. *Why:* subscription scoping is a property of the open stream CLOUD.29 establishes |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.31](#task-cloud-31), [CLOUD.36](#task-cloud-36), [DEV.14](device-bridge.md#task-dev-14) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.PublicApi/Streams/Scope/**` |
| Validation | opt-in tests: mixed-product/unauthorized feed refused |
| Completion evidence | mixed-product/unauthorized refusal and account-security-identifier separation results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-31"></a>

### CLOUD.31 — Cursor and gap handling (DO projection backed by D1 outbox)

**Outcome.** Sequence/hash/offset cursors and snapshot high-water recovery work per annex 10; the DO is a projection backed by the D1 outbox, never a second business authority.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-31` and ledger record `ledger/tasks/cloud-31.md` in the Plan repository; task branch `task/cloud-31` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-24.02](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.02) — full |
| Provides | stream-cursor-recovery |
| Start prerequisites | **artifact** [CLOUD.30](#task-cloud-30) — scoped subscription to attach cursor semantics to. *Why:* cursors are scoped to the subscription CLOUD.30 defines<br>**artifact** [CLOUD.04](#task-cloud-04) — the committed D1 outbox to project from. *Why:* the DO projection is explicitly backed by the D1 outbox, not an independent source of truth |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.32](#task-cloud-32), [CLOUD.33](#task-cloud-33), [CLOUD.36](#task-cloud-36), [CLOUD.39](#task-cloud-39), [DEV.14](device-bridge.md#task-dev-14) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.EventFeed/**` |
| Validation | opt-in tests: duplicate/conflicting frames, expired cursor, deleted DO, revision replay |
| Completion evidence | duplicate/conflicting-frame, expired-cursor, deleted-DO and revision-replay results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-32"></a>

### CLOUD.32 — Durable unary fallback (Poll/readOutput)

**Outcome.** Poll/readOutput works with the same owner/cursor profile as the stream, replacing the old HTTP task-stream endpoint; a blocked stream recovers through a real unary read without inventing completion.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-32` and ledger record `ledger/tasks/cloud-32.md` in the Plan repository; task branch `task/cloud-32` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-24.03](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.03) — full |
| Provides | durable-unary-fallback |
| Start prerequisites | **artifact** [CLOUD.31](#task-cloud-31) — cursor/gap handling to read from in the unary fallback. *Why:* Poll/readOutput shares the same cursor profile CLOUD.31 defines |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.36](#task-cloud-36), [PRF.06](runtime-proofs.md#task-prf-06) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.PublicApi/Streams/Fallback/**` |
| Validation | opt-in test: blocked stream recovers through real unary read without invented completion |
| Completion evidence | blocked-stream real-recovery result |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | AI terminal bodies (ChatTurn/Task execution output) arrive via [WP-52](../../work-packages/52-cloud-harness.md#rule-wp-52), not this task. |

<a id="task-cloud-33"></a>

### CLOUD.33 — Publication and wake (D1 outbox to bounded DO feed via Queues)

**Outcome.** The committed D1 outbox publishes into the bounded DO feed with wake hints delivered via Queues; contiguous watermark, no skipped commit, duplicate queue event is safe; no business ownership lives in the DO.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-33` and ledger record `ledger/tasks/cloud-33.md` in the Plan repository; task branch `task/cloud-33` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-24.04](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.04) — full |
| Provides | outbox-to-feed-publisher |
| Start prerequisites | **artifact** [CLOUD.31](#task-cloud-31) — the DO projection to publish into. *Why:* this task is the write side of the projection CLOUD.31 reads<br>**artifact** [CLOUD.05](#task-cloud-05) — the finite-durable-job/Queue wake mechanism. *Why:* wake hints are delivered via Queues using the same finite-job pattern CLOUD.05 establishes<br>**artifact** [CLOUD.69](#task-cloud-69) — the Cloud-side correlation seam for event publication. *Why:* propagating correlation once is a Cloud seam ([CR-06](../../../architecture/13-observability-and-operations.md#rule-cr-06)); this task builds on it instead of adding per-module propagation |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.35](#task-cloud-35), [CLOUD.36](#task-cloud-36), [DEV.14](device-bridge.md#task-dev-14) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.EventFeed/Publisher/**` |
| Shared resources | [RES-cloud-leased-singletons](../shared-resources.md#res-cloud-leased-singletons) (append) |
| Validation | opt-in tests: contiguous watermark, no skipped commit, duplicate queue event safe |
| Completion evidence | contiguous-watermark and duplicate-safety results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | Planning repair 2026-10-05: the bounded DO feed and the events it publishes carry the originating correlation (Event.correlationId, contracts 03) through the CLOUD.69 seam; this is part of this task's own acceptance and of the real realtime hop that PLT.48's correlation scenario names as a later owner (no new write scope). |

<a id="task-cloud-34"></a>

### CLOUD.34 — Bounded stream lifecycle

**Outcome.** 5-minute stream, 15s heartbeat, 45s silence and bounded jitter/queue limits are enforced; Android background closes streams and later refetches; slow-reader overflow resets rather than growing unbounded.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-34` and ledger record `ledger/tasks/cloud-34.md` in the Plan repository; task branch `task/cloud-34` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-24.05](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.05) — full |
| Provides | bounded-stream-lifecycle |
| Start prerequisites | **artifact** [CLOUD.29](#task-cloud-29) — the stream shell to bound the lifecycle of. *Why:* lifecycle limits wrap the stream CLOUD.29 opens |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.35](#task-cloud-35), [CLOUD.36](#task-cloud-36), [DEV.14](device-bridge.md#task-dev-14), [PRF.06](runtime-proofs.md#task-prf-06) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.PublicApi/Streams/Lifecycle/**` |
| Validation | opt-in test: slow reader overflow resets, no unbounded memory or hibernation-cost claim |
| Completion evidence | slow-reader overflow-reset result |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-35"></a>

### CLOUD.35 — Reusable stream consumer adapters

**Outcome.** Platform Cloud.Client and Contracts TS/Kotlin stream fixtures are published with typed lifecycle states and no UI-specific transport logic.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-35` and ledger record `ledger/tasks/cloud-35.md` in the Plan repository; task branch `task/cloud-35` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-24.06](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.06) — full |
| Provides | stream-consumer-adapters |
| Start prerequisites | **artifact** [CLOUD.33](#task-cloud-33) — the real publication/wake mechanism to expose through the reusable adapter. *Why:* adapters wrap the real deployed stream, not a placeholder<br>**artifact** [CLOUD.34](#task-cloud-34) — bounded lifecycle semantics to expose as typed lifecycle states. *Why:* the adapter's typed states mirror CLOUD.34's lifecycle bounds |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.36](#task-cloud-36) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.CloudClient/Streams/**`<br>`Cloud:fixtures/wire/streams/**` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append) |
| Validation | opt-in tests: clean generated-client consumers and real deployed C# ownership paths |
| Completion evidence | clean-consumer and real-ownership-path results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-36"></a>

### CLOUD.36 — Owned-artifact closure and real integration (tool-result acceptance)

**Outcome.** Every [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) substep is complete and packaged; two distinct toolRequestIds in one attempt both persist and replay correctly for both Task and ChatTurn owners; a changed result under the same (toolRequestId, attemptId, commandId) refuses.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-36` and ledger record `ledger/tasks/cloud-36.md` in the Plan repository; task branch `task/cloud-36` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-24.90](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.90) — full, including the Tool-result acceptance subsection (toolRequestId dedup for Task and ChatTurn owners, command.reused_identifier refusal, wire registry + [TK-05](../../../architecture/contracts/01-public-api-operations.md#rule-tk-05) + task.tool_result binding) |
| Provides | wp24-closure |
| Start prerequisites | **artifact** [DEV.14](device-bridge.md#task-dev-14) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.29](#task-cloud-29) — final candidate. *Why:* closure requires every preceding [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) substep<br>**integration** [CLOUD.30](#task-cloud-30) — final candidate. *Why:* closure requires every preceding [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) substep<br>**integration** [CLOUD.31](#task-cloud-31) — final candidate. *Why:* closure requires every preceding [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) substep<br>**integration** [CLOUD.32](#task-cloud-32) — final candidate. *Why:* closure requires every preceding [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) substep<br>**integration** [CLOUD.33](#task-cloud-33) — final candidate. *Why:* closure requires every preceding [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) substep<br>**integration** [CLOUD.34](#task-cloud-34) — final candidate. *Why:* closure requires every preceding [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) substep<br>**integration** [CLOUD.35](#task-cloud-35) — final candidate. *Why:* closure requires every preceding [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24) substep<br>**integration** [DEV.12](device-bridge.md#task-dev-12) — a real Task owner to exercise the tool-result dedup vector against. *Why:* the tool-result acceptance test needs both Task and ChatTurn owners exercised; the Task owner is built outside this area |
| Unblocks | [REL.06](release.md#task-rel-06) |
| Write scope | `Cloud:artifacts/candidate/**` |
| Validation | package/contract/owner/version compatibility, failure/recovery, real boundaries |
| Completion evidence | owned artifact and real-integration receipt per [WP-24.90](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24.90) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: n/a -- closure task |

<a id="task-cloud-38"></a>

### CLOUD.38 — Client outbox and conflict lineage (desktop data model)

**Outcome.** The single sync_outbox schema exists client-side: the existing store_content aggregate row holds its canonical acknowledged Cloud shadow in a dedicated nullable column while payload bytes remain opaque and byte-exact, alongside the pending journal, frozen batch hash/revision/range and explicit supersession lineage; a user conflict resolution appends a new local event and never edits the frozen failed batch.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/cloud-38` and ledger record `ledger/tasks/cloud-38.md` in the Plan repository; task branch `task/cloud-38` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-25.01](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.01) — full |
| Provides | client-sync-outbox |
| Start prerequisites | **artifact** [PLT.01](platform.md#task-plt-01) — the local store journal/single-writer persistence foundation. *Why:* the client outbox is built on the local journal, not a second local persistence mechanism |
| Entry condition | [ADOPT.02.cloud](adoption.md#task-adopt-02-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.39](#task-cloud-39) — the real guarded publication/bootstrap mechanism to submit batches against for a genuine end-to-end proof. *Why:* client-side outbox correctness (own-origin feed echo, late old receipt) can only be proven against the real server publisher, not assumed |
| Unblocks | [CLOUD.40](#task-cloud-40), [CLOUD.44](#task-cloud-44), [CLOUD.47](#task-cloud-47) |
| Write scope | `DesktopPlatform:src/BuildingBlocks/ArcForges.Sync/**`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.Persistence.Sqlite/** (only the existing single sync_outbox schema and one store_content.acknowledged_cloud_shadow BLOB NULL column under the fixed cloud-38-sync-outbox-v1 forward migration; atomic local edit/state/journal/outbox/shadow transaction; recovery and downgrade-refusal behavior; payload remains opaque and byte-exact; protected-table migration authorization is limited to this exact migration touching sync_outbox and store_content after legacy-shape validation)`<br>`DesktopPlatform:tests/PersistenceTests/** (sync_outbox regressions of the persistence work package only)` |
| Shared resources | [RES-assistant-store-schema](../shared-resources.md#res-assistant-store-schema) (append), [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | offline + opt-in tests: edit during dispatch, conflict followed by keep-local/keep-Cloud/merge, dependent undispatched batches, crash at each resolution write, late old receipt, own-origin feed echo; migration preserves legacy payload bytes, valid and malformed projection-marker prefixes remain opaque byte-exact payloads, acknowledged shadow round-trips only through its explicit nullable column, legacy store_content shape is validated, and unrelated protected-table access is refused |
| Completion evidence | every local edit has a durable outcome and exactly one live submission lineage; no conflict silently drops pending content |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: DesktopPlatform out of this area's primary research scope -- integration owner should verify no existing local-outbox scaffold |
| Notes | Cross-repo: [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) names this project explicitly in its own §4 table despite living in DesktopPlatform. Persistence.Sqlite scope is limited to the one existing sync_outbox schema plus one store_content.acknowledged_cloud_shadow BLOB NULL column on the existing store_content row, in the same database and atomic local edit/state/journal/outbox/shadow transaction, with the fixed cloud-38-sync-outbox-v1 forward migration, legacy-shape validation, recovery and downgrade-refusal tests; no second database, table or outbox and no unrelated Persistence changes. store_content.payload remains opaque application bytes and is never inspected for or decoded from a marker, magic prefix or hash wrapper. Only cloud-38-sync-outbox-v1 may touch the two exact protected tables sync_outbox and store_content; no generic protected-table authorization is added. PersistenceTests scope covers only [WP-25.01](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.01) outbox regressions. Project/solution/workflow/inventory/support changes are exact [ADP-07](../adoption.md#rule-adp-07) bindings only: append the required project/build/test and current policy/provenance inputs without new dependencies, package identities, policy algorithms or unrelated rows. Preserve RES-assistant-store-schema's serialized migration protocol. |

<a id="task-cloud-39"></a>

### CLOUD.39 — Guarded publication, convergent bootstrap and the Sync owner transaction

**Outcome.** Model-04's primary lower-bound W bootstrap, immutable-key pages, retention pin and replay-to-H work; the publisher guards watermark/fence/selected rows in one D1 batch; the real Sync owner transaction commits admitted ScopeProjectMetadata and ScopeMetadata owner bodies with publication, receipts and Resource/Entitlement enlistment in the same commit; real D1 clients converge without PostgreSQL snapshot/locks or lost pending work.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-39` and ledger record `ledger/tasks/cloud-39.md` in the Plan repository; task branch `task/cloud-39` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L · early risk proof |
| Obligations | [WP-25.02](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.02) — full<br>[WP-21.00](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.00) — real Sync owner transaction implementation for admitted ArcScope metadata owner bodies |
| Provides | sync-publication-bootstrap; sync-change-feed; sync-owner-transaction |
| Start prerequisites | **artifact** [CLOUD.04](#task-cloud-04) — the generic receipts/outbox mechanism this publisher reads committed-unpublished rows from. *Why:* the publisher batch reads <=100 committed-unpublished sync.change rows written with publish_seq=NULL by the business transaction, per data-model/01 §9<br>**artifact** [CLOUD.31](#task-cloud-31) — [WP-24](../../work-packages/24-realtime-and-reliable-events.md#rule-wp-24)'s cursor/gap-handling concept, since this publisher and the realtime DO feed are related but distinct publication mechanisms consumers must not conflate. *Why:* see shared_resources: this is a second, sync-specific leased singleton distinct from CLOUD.33's feed-wake publisher<br>**artifact** [CLOUD.03](#task-cloud-03) — D1 physical mapping/migration runner for the Sync owner tables. *Why:* the real Sync owner transaction needs real migrations<br>**artifact** [CLOUD.06](#task-cloud-06) — the shared atomic family engine, since synced content mutation is a named shared-transaction family. *Why:* publication, receipts and Resource enlistment share the commit<br>**artifact** [CON.03](contracts.md#task-con-03) — the closed Sync owner-body admission for ArcScope metadata. *Why:* the Sync owner transaction accepts only admitted owner bodies<br>**artifact** [CON.09](contracts.md#task-con-09) — the published SyncService operations. *Why:* the Sync owner transaction implements the generated Sync operations<br>**artifact** [CLOUD.01](#task-cloud-01) — real, delivered outcome of CLOUD.01 (Ingress and host pipeline). *Why:* the Sync owner transaction runs behind the real ingress and host pipeline |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.70](#task-cloud-70) — the gated migration step that applies the locked migrations to the deployed D1 database. *Why:* real D1 clients converge against a deployed schema |
| Unblocks | [AND.07](android.md#task-and-07), [CLOUD.10](#task-cloud-10), [CLOUD.38](#task-cloud-38), [CLOUD.40](#task-cloud-40), [CLOUD.41](#task-cloud-41), [CLOUD.43](#task-cloud-43), [CLOUD.47](#task-cloud-47), [CLOUD.68](#task-cloud-68), [SCOPE.27](arcscope.md#task-scope-27), [SRCH.00](search.md#task-srch-00) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Sync/Publisher/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Sync/Transactions/**` |
| Shared resources | [RES-cloud-leased-singletons](../shared-resources.md#res-cloud-leased-singletons) (append) |
| Validation | opt-in real-D1 tests: two-writer interleavings, commit between pages, insert below cursor, delete/tombstone, expired pin, lost acknowledgement, old/new revision application with pending edits; non-allowlisted owner body, stale sorted-root revision and cross-owner reference refusals |
| Completion evidence | real D1 clients converge without PostgreSQL snapshot/locks or lost pending work |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | Early risk proof: this is the two-writer D1 guarded-batch algorithm underlying [PG-17](../../../assurance/open-gates-register.md#rule-pg-17). Proving it under contention before WP-25.03-07 build on top avoids invalidating that downstream work. [PG-17](../../../assurance/open-gates-register.md#rule-pg-17) explicitly 'consumes the publisher from package 21' (CLOUD.04/CLOUD.06) -- this task is where that consumption happens for Sync specifically, together with the real Sync owner transaction. |

<a id="task-cloud-40"></a>

### CLOUD.40 — Conflict detection and five resolution policies

**Outcome.** Conflicts are detected by revision, never timestamp; five policies are implemented per the architecture, chosen per scope and object kind; discarded versions remain recoverable; user-facing conflicts present both versions intelligibly.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-40` and ledger record `ledger/tasks/cloud-40.md` in the Plan repository; task branch `task/cloud-40` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-25.03](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.03) — full |
| Provides | conflict-policies |
| Start prerequisites | **artifact** [CLOUD.38](#task-cloud-38) — the client outbox/conflict lineage to detect conflicts against. *Why:* conflict detection compares the client's pending lineage against the server's committed revision<br>**artifact** [CLOUD.39](#task-cloud-39) — the guarded publication mechanism, since conflicts are detected during publication. *Why:* revision comparison happens as part of the guarded publish batch |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.44](#task-cloud-44), [CLOUD.47](#task-cloud-47) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Sync/Conflict/**` |
| Validation | offline + opt-in tests: conflict matrix across object kinds and policies, recoverability test for every discard, user-facing presentation test |
| Completion evidence | every conflict path covered, every discarded version recoverable, user-facing conflicts present both versions |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-41"></a>

### CLOUD.41 — Deletion and tombstones

**Outcome.** Deletion propagates through tombstones with defined retention; an offline-beyond-retention device resolves deterministically rather than silently resurrecting content; local deletion, cloud deletion and unsync are distinguished.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-41` and ledger record `ledger/tasks/cloud-41.md` in the Plan repository; task branch `task/cloud-41` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-25.04](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.04) — full |
| Provides | deletion-tombstones |
| Start prerequisites | **artifact** [CLOUD.39](#task-cloud-39) — the change feed/publication mechanism to propagate tombstones through. *Why:* tombstones are change-feed entries like any other change |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.44](#task-cloud-44), [CLOUD.47](#task-cloud-47) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Sync/Tombstones/**` |
| Validation | offline + opt-in tests: offline-beyond-retention convergence, resurrection-prevention test, three-way delete-action distinction test |
| Completion evidence | deleted content never silently resurrects; the three delete-like actions are distinguishable |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-42"></a>

### CLOUD.42 — Blob lifecycle (real R2 staged/verified/committed)

**Outcome.** Upload happens through a server-issued session, chunked and checksummed, moving Staged -> Verified -> Committed; a reference is only published after commit; orphan cleanup removes uncommitted staging without touching committed data; storage accounting is computed from committed objects.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-42` and ledger record `ledger/tasks/cloud-42.md` in the Plan repository; task branch `task/cloud-42` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-25.05](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.05) — full |
| Provides | blob-lifecycle-r2 |
| Start prerequisites | **artifact** [CLOUD.01](#task-cloud-01) — the deployed Worker's R2 bucket binding and job-authorized object port (contracts/05 §9 job-grant/job-authorize). *Why:* real bytes move through the deployed Worker's R2 binding; there is no substitute since object storage is explicitly must-be-real-early<br>**artifact** [CLOUD.06](#task-cloud-06) — the shared atomic family engine, since resource upload lifecycle is a named shared-transaction family. *Why:* staged/verified/committed transitions are guarded D1 batch writes, not plain state flips<br>**artifact** [CLOUD.25](#task-cloud-25) — the resource transport schema this task replaces the fixture for. *Why:* CLOUD.42 is the real_producer named by CLOUD.25's SUB-resource-transport-schema-fixtures entry |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.07](android.md#task-and-07), [CLOUD.43](#task-cloud-43), [CLOUD.44](#task-cloud-44), [CLOUD.45](#task-cloud-45), [CLOUD.46](#task-cloud-46), [CLOUD.47](#task-cloud-47), [CLOUD.48](#task-cloud-48), [EXT.06](extensions.md#task-ext-06), [SCOPE.23](arcscope.md#task-scope-23), [SIM.04](simulator.md#task-sim-04), [WEB.13](web.md#task-web-13) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Resource/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append), [RES-cloud-storage-plans](../shared-resources.md#res-cloud-storage-plans) (append), [RES-shared-transaction-families](../shared-resources.md#res-shared-transaction-families) (append) |
| Validation | opt-in real-R2 tests: interrupted-upload resumption, verification-failure path, orphan-cleanup safety test, accounting comparison against actual committed storage |
| Completion evidence | no reference published before commit; orphan cleanup never touches committed data; accounting matches committed storage |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists; only the [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) minimal R2 transport probe exists upstream (the native and runtime-proof lanes, not this repo) |
| Notes | Must-be-real-early per implementation-sequence §3 ('Object storage adapters' may be mocked only at the schema/protocol layer -- 'Upload interruption, hashing, resumption and quota' must be real). Keep this must-be-real-early placement; do not defer real R2 behind fixture evidence. |

<a id="task-cloud-43"></a>

### CLOUD.43 — Availability, protection, data-health signals and realm-transfer workflow

**Outcome.** Hydration/cache pause is distinguished from explicit Cloud deletion; source-consent/transient inputs and health states exist; the full realm-transfer export/preview/commit/status/cancel workflow works from client journeys; missing-object outcomes are rebuilt or verified with irrecoverable data retaining evidence and recovery/export actions.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-43` and ledger record `ledger/tasks/cloud-43.md` in the Plan repository; task branch `task/cloud-43` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-25.06](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.06) — full |
| Provides | availability-protection-health |
| Start prerequisites | **artifact** [CLOUD.42](#task-cloud-42) — the real blob lifecycle to verify object availability against. *Why:* integrity/availability checks operate on real R2 objects, not fixtures<br>**artifact** [CLOUD.39](#task-cloud-39) — the sync change feed for the realm-transfer workflow's status/commit steps. *Why:* realm-transfer commit/status participates in the same guarded publication mechanism |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.47](#task-cloud-47) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Sync/Health/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Resource/RealmTransfer/**` |
| Validation | opt-in real-R2/D1 tests: resume after 100-root batch, repeated command, missing object, partial cancellation, denied current scope, transfer credential/ledger exclusion, restore generation |
| Completion evidence | no Unsync deletion of authoritative Cloud content, no empty success for irrecoverable data, no manual migration rule invented |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | POSSIBLE DESIGN OVERLAP: this task's 'full realm-transfer export/preview/commit/status/cancel workflow from client journeys' ([WP-25.06](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.06)) reads very close to [WP-46.05](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.05)'s 'existing explicit realm export/import semantics using compatible D1 physical/schema/plan manifests' (CLOUD.53). They may be genuinely different (user-facing personal-data export vs operator-level realm-to-realm database migration) or may be the same feature described twice. |

<a id="task-cloud-44"></a>

### CLOUD.44 — Multi-device convergence harness

**Outcome.** Three devices editing concurrently, one offline for an extended period, converge to verifiably identical state under concurrent edits, attachments, deletions and a mid-sync crash, verified by comparison not absence of errors.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-44` and ledger record `ledger/tasks/cloud-44.md` in the Plan repository; task branch `task/cloud-44` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / L |
| Obligations | [WP-25.07](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.07) — all work except the parts mapped to SCOPE.27 |
| Provides | multi-device-convergence-proof |
| Start prerequisites | none |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.38](#task-cloud-38) — real client outbox. *Why:* the harness drives three real client outboxes<br>**integration** [CLOUD.40](#task-cloud-40) — real conflict policies. *Why:* concurrent edits must resolve through the real policies<br>**integration** [CLOUD.41](#task-cloud-41) — real tombstones. *Why:* the harness includes deletions<br>**integration** [CLOUD.42](#task-cloud-42) — real blob lifecycle. *Why:* the harness includes attachments<br>**integration** [SCOPE.27](arcscope.md#task-scope-27) — a real ArcScope client syncing metadata against the deployed Cloud sync engine to run the three-device harness against. *Why:* ArcScope is the product proving the sync protocol ([WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25)); this task needs the real product, not just the Sync building block |
| Unblocks | [CLOUD.47](#task-cloud-47), [SCOPE.27](arcscope.md#task-scope-27) |
| Write scope | `Cloud:tests/SyncConflictTests/Convergence/**` |
| Validation | a three-device convergence harness with concurrent edits, an extended offline device, attachments, deletions and a mid-sync crash |
| Completion evidence | three devices converge to verifiably identical state |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | Gate: [PG-17](../../../assurance/open-gates-register.md#rule-pg-17) (joint with CLOUD.39). This is the full end-to-end demonstration; CLOUD.39 is where the underlying algorithm risk is retired early. |

<a id="task-cloud-45"></a>

### CLOUD.45 — Real Cloud Chat export producer

**Outcome.** Bounded leased Cloud export jobs freeze an acknowledged revision manifest, pin history/attachment objects, generate the declared Markdown/JSON/text outputs with metadata/link map and fidelity report, and publish a verified expiring download artifact; device-only pending edits are excluded.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-45` and ledger record `ledger/tasks/cloud-45.md` in the Plan repository; task branch `task/cloud-45` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) — all work except the parts mapped to AST.21, CLOUD.58 |
| Provides | real-chat-export |
| Start prerequisites | **artifact** [CLOUD.42](#task-cloud-42) — real R2 staging/verification for the export bundle. *Why:* the export bundle is staged and verified through the real blob lifecycle, not a fixture<br>**artifact** [CLOUD.05](#task-cloud-05) — the finite-durable-job mechanism, since exports are bounded leased jobs. *Why:* export jobs follow the same checkpoint/receipt/lease pattern<br>**contract** [CON.22](contracts.md#task-con-22) — published export and data operations. *Why:* export jobs expose the generated status, cancel and download operations |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.21](assistant.md#task-ast-21), [CLOUD.47](#task-cloud-47), [CLOUD.58](#task-cloud-58), [WEB.15](web.md#task-web-15) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Chat/Export/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Jobs/Export/**` |
| Validation | opt-in real host/database/object-store tests: concurrent history writes, branch edits, deleted attachments, quota limit, expiry, restart, cancellation, paid-term end; compare every delivered manifest/hash and omission; scan for secrets |
| Completion evidence | the Chat export path works against real Cloud authority, preserves a stable snapshot and honest fidelity, and releases pins/reservations on all terminal paths |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | This is the Cloud-side producer for [PG-07](../../../assurance/open-gates-register.md#rule-pg-07)'s Cloud Chat export portion; CLOUD.58 structurally removes the [WP-15.06](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15.06) runtime export fixture. |

<a id="task-cloud-46"></a>

### CLOUD.46 — Application Cloud history and restartable import

**Outcome.** HistoryService.BeginImport/FinalizeImport/GetImport/CancelImport work per annex 10 with fixed product scope, verified staged archive/typed rows and atomic visibility/receipt; local-only history bodies never enter Cloud Chat or search without explicit promotion.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-46` and ledger record `ledger/tasks/cloud-46.md` in the Plan repository; task branch `task/cloud-46` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-25.09](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.09) — all work except the parts mapped to AST.22 |
| Provides | cloud-history-import-service |
| Start prerequisites | **artifact** [CLOUD.42](#task-cloud-42) — real R2 staged-archive verification for imported history bodies. *Why:* history import stages and verifies an archive object through the real blob lifecycle<br>**artifact** [CLOUD.06](#task-cloud-06) — the shared atomic family engine for atomic visibility/receipt. *Why:* finalize import's atomic visibility/receipt is a guarded D1 batch |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AST.22](assistant.md#task-ast-22), [CLOUD.47](#task-cloud-47) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.*/History/**` |
| Validation | opt-in real tests: actual archive/manifest hashes, staged object authorization, parent/branch mapping, lost finalization acknowledgement, duplicate import, source edit during promotion, quota/permission loss, expiry |
| Completion evidence | clean published desktop/Kotlin/TS consumers recover a real interrupted import, see no partial visible conversation, keep local/Cloud/temporary retention distinct |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists; data-model/05-application-history.md defines the physical schema this implements on the Cloud side (import/promotion receiving) |
| Notes | Replaces the HistoryService fixture consumed by [WP-15](../../work-packages/15-arcchat-conversation-core.md#rule-wp-15)/[WP-17](../../work-packages/17-arcchat-independent-core.md#rule-wp-17). See integration_proposals: IM.assistant-history-real-integration. |

<a id="task-cloud-47"></a>

### CLOUD.47 — Owned-artifact closure and real integration

**Outcome.** R2 is used for the existing upload admission, multipart resume, Verified pin, owner promotion, quota and release lifecycle; outbox/inbox/tombstones/conflicts/bootstrap/unknown-field behavior and export protocol are retained; three-device convergence and interrupted-upload/failed-content-commit/orphan/delete cases run against actual provider adapters.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-47` and ledger record `ledger/tasks/cloud-47.md` in the Plan repository; task branch `task/cloud-47` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-25.90](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.90) — full<br>[WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) Required implementation and closure from the final review (01-cloud-data-model verification; real structural move/ack/conflict transactions, full native metadata replicas, job-authorized R2 staging/verification/promotion, quarantined old-generation client commands) — package-level obligation contribution |
| Provides | wp25-closure |
| Start prerequisites | **artifact** [AST.21](assistant.md#task-ast-21) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [AST.22](assistant.md#task-ast-22) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [CLOUD.58](#task-cloud-58) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [SCOPE.27](arcscope.md#task-scope-27) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.38](#task-cloud-38) — final candidate. *Why:* closure requires every preceding [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) substep<br>**integration** [CLOUD.39](#task-cloud-39) — final candidate. *Why:* closure requires every preceding [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) substep<br>**integration** [CLOUD.40](#task-cloud-40) — final candidate. *Why:* closure requires every preceding [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) substep<br>**integration** [CLOUD.41](#task-cloud-41) — final candidate. *Why:* closure requires every preceding [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) substep<br>**integration** [CLOUD.42](#task-cloud-42) — final candidate. *Why:* closure requires every preceding [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) substep<br>**integration** [CLOUD.43](#task-cloud-43) — final candidate. *Why:* closure requires every preceding [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) substep<br>**integration** [CLOUD.44](#task-cloud-44) — final candidate. *Why:* closure requires every preceding [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) substep<br>**integration** [CLOUD.45](#task-cloud-45) — final candidate; [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) must be represented in this task's own evidence and completion gate per the WP text, not treated as optional. *Why:* [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25)'s own §8 states [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) 'remains represented in its evidence and completion gate'<br>**integration** [CLOUD.46](#task-cloud-46) — final candidate. *Why:* closure requires every preceding [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) substep, and the.90 stage explicitly cannot leave HistoryService as a fixture per [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) §9<br>**integration** [CLOUD.68](#task-cloud-68) — package task complete. *Why:* the [WP-25](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25) closure verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Unblocks | [REL.06](release.md#task-rel-06) |
| Write scope | `Cloud:artifacts/candidate/**` |
| Validation | three-device convergence and interrupted-upload/failed-content-commit/orphan/delete cases against actual provider adapters |
| Completion evidence | owned artifact and real-integration receipt per [WP-25.90](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.90) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: n/a -- closure task |

<a id="task-cloud-48"></a>

### CLOUD.48 — D1 and independent object backup

**Outcome.** Model-04/backup-manifest-v1 works: matching D1 export/bookmark/base sequence, contiguous replay, verified R2 inventory and an independent S3-COMPLIANCE copy; no PostgreSQL WAL/LSN procedure; measured metadata/blob RPO and RTO pass; Time Travel alone cannot satisfy independent restore.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-48` and ledger record `ledger/tasks/cloud-48.md` in the Plan repository; task branch `task/cloud-48` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / L |
| Obligations | [WP-46.00](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.00) — full |
| Provides | d1-object-backup |
| Start prerequisites | **artifact** [CLOUD.03](#task-cloud-03) — the D1 physical schema/migration runner to export a matching bookmark/base sequence for. *Why:* backup format is defined against the exact physical mapping CLOUD.03 implements<br>**artifact** [CLOUD.42](#task-cloud-42) — real committed R2 objects to inventory and copy independently. *Why:* R2 inventory/independent copy operates on the real blob lifecycle, not a fixture |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.49](#task-cloud-49), [CLOUD.52](#task-cloud-52), [CLOUD.53](#task-cloud-53), [CLOUD.54](#task-cloud-54), [CLOUD.55](#task-cloud-55) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Backup/**` |
| Shared resources | [RES-cloud-d1-migrations](../shared-resources.md#res-cloud-d1-migrations) (append) |
| Validation | opt-in real tests: fresh database import, missing replay gap/hash/key, restrictive journal replay, session/generation reset, reconciled unknown effects; include selfhost.v1 account |
| Completion evidence | measured metadata/blob RPO and RTO; Time Travel alone cannot satisfy independent restore |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-49"></a>

### CLOUD.49 — Point-in-time and fresh restore

**Outcome.** Base bookmark/sequence and contiguous after-image archive are verified; in-place Time Travel and fresh import/replay both use generation fences.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-49` and ledger record `ledger/tasks/cloud-49.md` in the Plan repository; task branch `task/cloud-49` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-46.01](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.01) — full |
| Provides | point-in-time-restore |
| Start prerequisites | **artifact** [CLOUD.48](#task-cloud-48) — the backup manifest/archive to restore from. *Why:* restore reads the archive CLOUD.48 produces |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.50](#task-cloud-50), [CLOUD.55](#task-cloud-55) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Backup/Restore/**` |
| Validation | opt-in real tests: missing archive/object, partial export, unsafe reopen refusal |
| Completion evidence | missing-archive/object and unsafe-reopen refusal results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-50"></a>

### CLOUD.50 — Fresh environment rebuild

**Outcome.** Old ingress/keys are fenced, D1/R2 are restored, the independent restrictive safety journal replays, credentials/leases/cursors are invalidated, external effects are reconciled; a deleted/revoked account cannot reappear and an absent attempt cannot execute twice.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-50` and ledger record `ledger/tasks/cloud-50.md` in the Plan repository; task branch `task/cloud-50` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-46.02](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.02) — full |
| Provides | fresh-environment-rebuild |
| Start prerequisites | **artifact** [CLOUD.49](#task-cloud-49) — point-in-time restore to rebuild from. *Why:* environment rebuild composes restore plus fencing/reconciliation<br>**artifact** [CLOUD.17](#task-cloud-17) — the recovery/account-states/deletion model, since a deleted/revoked account must not reappear after rebuild. *Why:* the rebuild's negative test directly checks CLOUD.17's deletion semantics survive a restore |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.51](#task-cloud-51), [CLOUD.55](#task-cloud-55) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Backup/Rebuild/**` |
| Validation | opt-in real tests: deleted/revoked account cannot reappear, absent attempt cannot execute twice |
| Completion evidence | deleted-account and absent-attempt-no-double-execution results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-51"></a>

### CLOUD.51 — Disaster-recovery drill programme

**Outcome.** An actual Container/Worker/DO/R2/D1 restore runs using separate credentials and an immutable archive with RTO<=4h real evidence, not a SQLite/simulator-only restore.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-51` and ledger record `ledger/tasks/cloud-51.md` in the Plan repository; task branch `task/cloud-51` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-46.03](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.03) — Cloud-side drill: real Container/Worker/DO/R2/D1 restore using separate credentials and immutable archive, RTO<=4h. The combined AI reopen portion is a joint step with the AI lanes/the governance and release lanes -- see IM.dr-drill-combined-ai-reopen |
| Provides | dr-drill-evidence |
| Start prerequisites | **artifact** [CLOUD.50](#task-cloud-50) — the fresh environment rebuild mechanism to drill. *Why:* the drill exercises the real rebuild procedure CLOUD.50 implements |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.67](#task-cloud-67) — AI reopen after the Cloud-side restore, per [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46)'s own text 'then combined AI reopen at 50/52'. *Why:* the full drill is explicitly combined with AI and release ([WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50)); Cloud's own restore evidence is necessary but not sufficient for the combined drill |
| Unblocks | [CLOUD.55](#task-cloud-55), [CLOUD.67](#task-cloud-67), [OPS.03](operations.md#task-ops-03), [REL.06](release.md#task-rel-06) |
| Write scope | `Cloud:tests/DrillTests/**` |
| Validation | RTO<=4h with real evidence, not SQLite/simulator-only restore |
| Completion evidence | real RTO<=4h evidence |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-52"></a>

### CLOUD.52 — Data health read projection

**Outcome.** Archive watermark, capacity, canonical refs/hash/pins, derived-rebuild state and backup lag/admission state are exposed as a queryable read projection, with 4min/12min warning guards and exceeded-objective incidents made visible.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-52` and ledger record `ledger/tasks/cloud-52.md` in the Plan repository; task branch `task/cloud-52` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-46.04](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.04) — full |
| Provides | data-health-read-projection |
| Start prerequisites | **artifact** [CLOUD.48](#task-cloud-48) — the real D1/object backup mechanism producing watermark/lag/inventory numbers to project. *Why:* data health reports real backup state; it cannot report numbers from a system that does not yet run |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.55](#task-cloud-55), [WEB.13](web.md#task-web-13) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.*/DataHealth/**` |
| Validation | opt-in tests: 4min/12min warning guard, exceeded-objective incident visible |
| Completion evidence | warning-guard and exceeded-objective-visibility results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | DELIBERATELY separable from CLOUD.49/50/51 (point-in-time restore, fresh rebuild, drill programme): this task's start edge is only on CLOUD.48 (real backup producing real numbers), not on the full restore/rebuild/drill machinery. This lets the Account portal ([WP-48](../../work-packages/48-account-portal.md#rule-wp-48), the Web and Android lanes) consume the data-health projection without waiting for all of [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46)'s recovery work to close -- per this area's assignment, keep this separation explicit and do not fold CLOUD.52 into a bundled [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) restore task. |

<a id="task-cloud-53"></a>

### CLOUD.53 — Export and realm migration

**Outcome.** Explicit realm export/import semantics work using compatible D1 physical/schema/plan manifests; no automatic cross-DB transaction; identity/resource/history scope is preserved and unsupported mapping is refused.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-53` and ledger record `ledger/tasks/cloud-53.md` in the Plan repository; task branch `task/cloud-53` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-46.05](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.05) — full |
| Provides | realm-export-import |
| Start prerequisites | **artifact** [CLOUD.48](#task-cloud-48) — the backup manifest format to reuse for realm export/import. *Why:* realm export/import uses compatible D1 physical/schema/plan manifests, the same manifest family CLOUD.48 defines |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.55](#task-cloud-55) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Backup/RealmMigration/**` |
| Shared resources | [RES-shared-transaction-families](../shared-resources.md#res-shared-transaction-families) (append) |
| Validation | opt-in real tests: identity/resource/history scope preserved, unsupported mapping refused |
| Completion evidence | scope-preservation and unsupported-mapping-refusal results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |
| Notes | POSSIBLE DESIGN OVERLAP with CLOUD.43 ([WP-25.06](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.06) realm-transfer workflow) -- see that task's notes. |

<a id="task-cloud-54"></a>

### CLOUD.54 — Backup release gate

**Outcome.** Verified independent backup and safety journal are required before paid production admission; no unverified restore, private access or mutation reopens on incomplete inventory.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-54` and ledger record `ledger/tasks/cloud-54.md` in the Plan repository; task branch `task/cloud-54` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-46.06](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.06) — full |
| Provides | backup-release-gate |
| Start prerequisites | **artifact** [CLOUD.48](#task-cloud-48) — the independent backup/safety-journal mechanism this gate checks the completeness of. *Why:* the gate is a completeness check on CLOUD.48's inventory, not a new mechanism |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.55](#task-cloud-55) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Backup/ReleaseGate/**` |
| Validation | opt-in tests: no unverified restore, private access or mutation reopens on incomplete inventory |
| Completion evidence | incomplete-inventory refusal results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: none exists |

<a id="task-cloud-55"></a>

### CLOUD.55 — Owned-artifact closure and real integration

**Outcome.** Every [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) substep is complete, built/packed once, and consumed as exact candidate bytes from a clean environment with all applicable UX acceptance groups recorded.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-55` and ledger record `ledger/tasks/cloud-55.md` in the Plan repository; task branch `task/cloud-55` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-46.90](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.90) — full |
| Provides | wp46-closure |
| Start prerequisites | none |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.48](#task-cloud-48) — final candidate. *Why:* closure requires every preceding [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) substep<br>**integration** [CLOUD.49](#task-cloud-49) — final candidate. *Why:* closure requires every preceding [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) substep<br>**integration** [CLOUD.50](#task-cloud-50) — final candidate. *Why:* closure requires every preceding [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) substep<br>**integration** [CLOUD.51](#task-cloud-51) — final candidate. *Why:* closure requires every preceding [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) substep<br>**integration** [CLOUD.52](#task-cloud-52) — final candidate. *Why:* closure requires every preceding [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) substep<br>**integration** [CLOUD.53](#task-cloud-53) — final candidate. *Why:* closure requires every preceding [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) substep<br>**integration** [CLOUD.54](#task-cloud-54) — final candidate. *Why:* closure requires every preceding [WP-46](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46) substep |
| Unblocks | [REL.06](release.md#task-rel-06) |
| Write scope | `Cloud:artifacts/candidate/**` |
| Validation | package/contract/owner/version compatibility, failure/recovery, real boundaries |
| Completion evidence | owned artifact and real-integration receipt per [WP-46.90](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.90) |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: n/a -- closure task |

<a id="task-cloud-58"></a>

### CLOUD.58 — Structural removal of the Chat export runtime fixture

**Outcome.** The production clients run with no fixture export producer registered; real Cloud export jobs serve the Chat export path

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-58` and ledger record `ledger/tasks/cloud-58.md` in the Plan repository; task branch `task/cloud-58` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-25.08](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) — full, joint with consumer-side structural fixture-registration removal |
| Start prerequisites | **artifact** [CLOUD.45](#task-cloud-45) — real, delivered outcome of CLOUD.45 (Real Cloud Chat export producer). *Why:* this integration exercises the real Cloud Chat export producer instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [AST.21](assistant.md#task-ast-21) — assistant history export consuming the real Cloud export producer. *Why:* runtime export fixtures are removed only after every consumer uses the real producer |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.47](#task-cloud-47) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | The production clients run with no fixture export producer registered; real Cloud export jobs serve the Chat export path |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-cloud-63"></a>

### CLOUD.63 — Real Commerce/Entitlement participation in the shared atomic family engine

**Outcome.** The 'exact credits' half of [WP-21.05](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05)'s own completion gate ('Two Containers contend, stale holder cannot finalize, exact credits and sync cursor safety') -- Commerce's family participation, owned by the commerce, policy and operations lanes

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-63` and ledger record `ledger/tasks/cloud-63.md` in the Plan repository; task branch `task/cloud-63` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-21.05](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05) — Commerce/Entitlement family participant evidence for the shared completion gate |
| Start prerequisites | **artifact** [CLOUD.06](#task-cloud-06) — real, delivered outcome of CLOUD.06 (Shared atomic family guarded-batch engine). *Why:* this integration exercises the real shared atomic family guarded-batch engine instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.16](#task-cloud-16) — real, delivered outcome of CLOUD.16 (PAT and actor authorization). *Why:* this integration exercises the real pAT and actor authorization instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [COM.09](commerce.md#task-com-09) — real, delivered outcome of COM.09 (Ledgers and reconciliation). *Why:* this integration exercises the real ledgers and reconciliation instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [COM.16](commerce.md#task-com-16) — the real Entitlement D1 store and grant port as the Entitlement participant of the shared families. *Why:* this integration exercises the real Entitlement participation instead of an in-memory substitute, so it cannot start before the durable Entitlement store exists |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.06](#task-cloud-06) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | The 'exact credits' half of [WP-21.05](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05)'s own completion gate ('Two Containers contend, stale holder cannot finalize, exact credits and sync cursor safety') -- Commerce's family participation, owned by the commerce, policy and operations lanes |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-cloud-64"></a>

### CLOUD.64 — Full operator contract closure across PublicApi, Commerce, Policy and Console

**Outcome.** Every operator operation's eight authorization fields, operator scope and [OC-03](../../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role binding work end-to-end with the real financial owners ([WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42)), configuration/policy owners ([WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44)) and console join ([WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45))

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-64` and ledger record `ledger/tasks/cloud-64.md` in the Plan repository; task branch `task/cloud-64` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) Operator contract closure appendix, full cross-area join — Operator contract closure appendix, full cross-area join |
| Start prerequisites | **artifact** [COM.13](commerce.md#task-com-13) — real, delivered outcome of COM.13 (Operator financial-owner proposal/approval operations). *Why:* this integration exercises the real operator financial-owner proposal/approval operations instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [POL.05](policy.md#task-pol-05) — real, delivered outcome of POL.05 (Kill switches). *Why:* this integration exercises the real kill switches instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [OPS.05](operations.md#task-ops-05) — real, delivered outcome of OPS.05 (Operator console and support access). *Why:* this integration exercises the real operator console and support access instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.21](#task-cloud-21) — real public endpoint mapping for the operator operations. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [CLOUD.22](#task-cloud-22) — real typed protocol and error mapping. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.28](#task-cloud-28) — the [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) operator contract closure accepted. *Why:* the full operator closure includes the public-API part that the [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) closure accepts |
| Unblocks | none |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Every operator operation's eight authorization fields, operator scope and [OC-03](../../../architecture/contracts/00-operation-catalogue.md#rule-oc-03) role binding work end-to-end with the real financial owners ([WP-42](../../work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42)), configuration/policy owners ([WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44)) and console join ([WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45)) |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-cloud-66"></a>

### CLOUD.66 — Every enumerated sensitive operation wired to the step-up mechanism

**Outcome.** Full coverage of [WP-22.04](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.04)'s completion gate ('every enumerated operation demands step-up') across Commerce refund/purchase operations and any other module-owned sensitive operation, not just Identity's own

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-66` and ledger record `ledger/tasks/cloud-66.md` in the Plan repository; task branch `task/cloud-66` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-22.04](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.04) — cross-product operation coverage beyond Identity's own operations |
| Start prerequisites | **artifact** [CLOUD.15](#task-cloud-15) — real, delivered outcome of CLOUD.15 (Step-up challenges for sensitive operations). *Why:* this integration exercises the real step-up challenges for sensitive operations instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [COM.10](commerce.md#task-com-10) — real, delivered outcome of COM.10 (Refunds, disputes and evidence). *Why:* this integration exercises the real refunds, disputes and evidence instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.21](#task-cloud-21) — real public endpoint mapping for the sensitive operations. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [CLOUD.22](#task-cloud-22) — real typed protocol and error mapping that returns step-up challenges. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.20](#task-cloud-20) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Full coverage of [WP-22.04](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.04)'s completion gate ('every enumerated operation demands step-up') across Commerce refund/purchase operations and any other module-owned sensitive operation, not just Identity's own |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-cloud-67"></a>

### CLOUD.67 — Combined AI reopen after Cloud disaster-recovery restore

**Outcome.** AI services genuinely reopen and function after a real Cloud DR restore, per [WP-46.03](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.03)'s own 'then combined AI reopen at 50/52'

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-67` and ledger record `ledger/tasks/cloud-67.md` in the Plan repository; task branch `task/cloud-67` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-46.03](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.03) — combined AI-reopen portion |
| Start prerequisites | **artifact** [CLOUD.51](#task-cloud-51) — real, delivered outcome of CLOUD.51 (Disaster-recovery drill programme). *Why:* this integration exercises the real disaster-recovery drill programme instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [HAR.00](harness.md#task-har-00) — the real Harness turn loop to reopen. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [HAR.02](harness.md#task-har-02) — real approval, cancellation and crash recovery. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [HAR.03](harness.md#task-har-03) — real generated streaming and durable output. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AIR.00](ai-routing.md#task-air-00) — real Workers AI provider adapters. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.51](#task-cloud-51) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | AI services genuinely reopen and function after a real Cloud DR restore, per [WP-46.03](../../work-packages/46-backup-recovery-and-data-health.md#rule-wp-46.03)'s own 'then combined AI reopen at 50/52' |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-cloud-68"></a>

### CLOUD.68 — ArcScope library read model and companion notifications

**Outcome.** scope.listProjects, scope.listSessions and scope.getSession project authorized committed project/session rows from scope.synced_aggregate. Project names, revisions and commit times come from ScopeProjectMetadata; counts and paging bind a consistent authorized snapshot, with missing/deleted parents and empty projects excluded. Sync emits durable scope.reportSynced and sync.conflictNeedsDecision notifications through the existing owner transaction, idempotently on replay. No raw bytes or new authoritative table are introduced.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-68` and ledger record `ledger/tasks/cloud-68.md` in the Plan repository; task branch `task/cloud-68` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-25.10](../../work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.10) — full |
| Provides | scope-library-read-model |
| Start prerequisites | **contract** [CON.24](contracts.md#task-con-24) — the generated ScopeService and summary records. *Why:* the endpoints implement the generated library operations<br>**artifact** [CLOUD.39](#task-cloud-39) — the real Sync owner transaction committing ArcScope metadata. *Why:* the read model projects committed scope.synced_aggregate rows<br>**artifact** [CLOUD.21](#task-cloud-21) — public endpoint registration. *Why:* the library operations are registered public endpoints |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.12](#task-cloud-12) — the Notification module durable rows. *Why:* the emitted notifications are persisted and delivered by the Notification owner |
| Unblocks | [AND.27](android.md#task-and-27), [CLOUD.47](#task-cloud-47), [WEB.32](web.md#task-web-32) |
| Write scope | `Cloud:src/Cloud/ArcForges.Cloud.Modules.Scope/Library/**`<br>`Cloud:src/Cloud/ArcForges.Cloud.Modules.Sync/Notifications/**` |
| Validation | offline projection, authorization and notification tests covering project rename, parent tombstones, out-of-order project/session arrival, empty projects, count changes without a project revision change, paged reads across commits and cache invalidation on either root; optional affected-scope real-D1 checks using an existing environment for these cases, minRevision, large responses and durable notification replay ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Real D1 projection results, authorization refusals and notification receipts for a synced ArcScope workspace. |
| Baseline (unreviewed unless accepted) | not-started Observed none: the Cloud host has no Scope or Sync module code yet. |
| Notes | Builds as soon as the Sync owner transaction exists; durable notification rows come from the Notification module. |

<a id="task-cloud-69"></a>

### CLOUD.69 — Correlation acceptance and propagation across ingress, response meta and queue wake

**Outcome.** The deployed Cloud ingress and host carry one correlation identity per call ([CR-01](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cr-01), [CR-03](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cr-03), [CR-06](../../../architecture/13-observability-and-operations.md#rule-cr-06), [HP-06](../../../architecture/05-cloud-architecture.md#rule-hp-06)): a RequestMeta.correlationId is read, validated as a canonical lowercase UUID and bound to the call context without ever influencing authorization or the current-owner decision, an absent value is created at the edge, a malformed value is refused with the registered validation.invalid_request code, and the identity is returned in ResponseMeta.correlationId and ArcError.correlationId of every reply the host builds. The Worker and host join it to one W3C traceparent per call, and the job wake message and the private job-slice call carry correlationId and causationId (the originating request or the previous wake event), so one synthetic call is joined across HTTP, Worker, host and queue-wake by the identifier alone. The task provides the one Cloud-side seam (a call-scoped correlation context for the host and a correlation envelope for Worker-originated queue messages) that later hop owners reuse instead of re-implementing propagation per module. It adds no realtime or provider behavior and no new wire field, header or contract meaning: a need for one is raised to the Contracts owner under [PA-02](../../implementation-sequence.md#rule-pa-02).

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-69` and ledger record `ledger/tasks/cloud-69.md` in the Plan repository; task branch `task/cloud-69` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / M |
| Obligations | [WP-12.01](../../work-packages/12-observability-foundation.md#rule-wp-12.01) — the Cloud share: acceptance of a validated client correlation value or creation at the Cloud edge, and its propagation across the HTTP ingress, Worker, host, ResponseMeta/ArcError and queue-wake hops (the shared infrastructure and the desktop origin stay with PLT.48) |
| Provides | cloud-correlation-seam |
| Start prerequisites | **artifact** [CLOUD.01](#task-cloud-01) — the deployed ingress and host pipeline (RpcPolicy, RequestEnvelopeReader, IngressPipeline, Worker pipeline and the wake queue consumer) in which correlation is read, bound and returned. *Why:* correlation propagation is a change inside the pipeline CLOUD.01 establishes and cannot be written without that real seam |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AIR.04](ai-routing.md#task-air-04), [CLOUD.05](#task-cloud-05), [CLOUD.33](#task-cloud-33), [PLT.48](platform.md#task-plt-48) |
| Write scope | `Cloud:worker/ingress/** (read, validate or create the correlation identity at the edge, forward it to the host with one W3C traceparent, and return it on Worker-built refusals only through fields the wire registry already defines)`<br>`Cloud:worker/foundation/queue.ts, Cloud:worker/foundation/types.ts and Cloud:worker/foundation/container-client.ts (only the job wake message correlationId/causationId metadata, its closed-key parser and its forwarding in the private job-slice call; no change to lease, fence, retry or backoff semantics)`<br>`Cloud:src/ArcForges.Cloud/Ingress/** (the existing Native AOT host project, which is the real layout of the planned Cloud.Host; RequestEnvelopeReader, Caller, RpcPolicy, IngressPipeline and the proof-only PipelineProbe replies; the adoption rules forbid renaming it or adding a parallel project)`<br>`Cloud:src/ArcForges.Cloud/Foundation/JobSliceService.cs and the private job-slice request handling in Cloud:src/ArcForges.Cloud/Foundation/FoundationEndpoints.cs (only to accept the wake's correlation/causation and carry them in the call context)`<br>`Cloud:tests/ArcForges.Cloud.Tests/** and Cloud:tests/worker/**`<br>`Cloud:eng/verification/pipeline-scenarios.ts and Cloud:eng/verification/foundation-scenarios.ts (only added local cross-process and explicit opt-in deployed correlation scenarios: supplied, absent, malformed, error reply, queue wake; the deployed scenarios hold the lease leases/res-cloud-deployment for the live run only)`<br>`Cloud:package.json (the explicit test file list and the scenario scripts only; no dependency or version change)`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/cloud-69-*.json (new immutable successor chained from the then-active receipt, only because the changed bundle, manifest and source inputs are hash-bound; no coordinate, integrity value or closure entry changes)`<br>`Cloud:eng/provenance/** (immutable successor release profile, Worker bundle and runtime-notice records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt)`<br>`Cloud:docs/cloud-ingress.md and Cloud:AGENTS.md (factual description of correlation acceptance, the seam and what remains unobserved)` |
| Shared resources | [RES-cloud-deployment](../shared-resources.md#res-cloud-deployment) (append) |
| Validation | Offline unit and cross-process tests: a valid supplied identifier is echoed in ResponseMeta and ArcError and reaches the wake message and job-slice call; an absent one is created; a malformed one is refused with validation.invalid_request before any handler or authorization decision; a supplied value never changes the authorization outcome; the Worker and host share one traceparent. Explicit local opt-in deployed scenarios against the isolated proof environment, once, under the RES-cloud-deployment lease. No hosted live, device, GUI or browser run ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Source commit, Worker bundle and image identity, local and deployed correlation scenario results with the untested hops named (realtime and provider are not exercised), and confirmation that no new wire field or header was introduced. |
| Baseline (unreviewed unless accepted) | not-started Planning repair 2026-10-05: no Cloud code or document handles correlation (CLOUD.01 delivered the ingress without it); nothing exists. |
| Notes | Planning repair 2026-10-05 ([DLV-34](../README.md#rule-dlv-34): scope moves only; no obligation or acceptance is removed). PLT.48's completion follow-up found that its completion prerequisite CLOUD.01 delivers a pipeline that neither reads, validates, returns nor propagates a correlation identifier (no Cloud code or documentation handles RequestMeta.correlationId, ResponseMeta.correlationId, ArcError.correlationId or a traceparent; the wake message is a closed key set without correlation) and that no Cloud task owned [CR-01](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cr-01), [CR-03](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cr-03), [CR-06](../../../architecture/13-observability-and-operations.md#rule-cr-06) or [HP-06](../../../architecture/05-cloud-architecture.md#rule-hp-06) for the Cloud side. This task is that owner and is deliberately small: it uses only the fields already in wire registry 04 (RequestMeta tag 3, ResponseMeta tag 4, ArcError tag 6; the generated Contracts packages already carry them) and the existing private signed job-slice call. It does not add the realtime or provider hops: Event.correlationId is populated by the publication owners (CLOUD.33 and the stream owners) and a provider request identifier ([CR-05](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-cr-05)) by the provider owners (AIR.04), each of which starts from this task's seam and keeps its own acceptance. The C# origin that makes the connected trace is not a Cloud or DesktopPlatform delivery task: PLT.48's completion follow-up performs it as one local opt-in consumer run outside the repository (the PLT.53 precedent) using the published ArcForges.Observability package to create the typed origin and the published generated PublicApi client to send it to the isolated proof environment, under the RES-cloud-deployment lease, and records the connected trace. The write scope of CLOUD.01 is not reopened. CLOUD.02 changes different files of the same host project (moved Storage and Hmac sources, module projects, composition listing); rebase after it merges, append to RES-cloud-host-composition only if a registration is needed (none is planned), and regenerate hash-bound provenance after the rebase. |

<a id="task-cloud-70"></a>

### CLOUD.70 — Gated D1 migration deployment step and compatible-rollback flow

**Outcome.** Migrations reach a deployed D1 database only through one gated step of the deployment pipeline (Design D1 profile section 6: never from Container startup). The step runs the CLOUD.03 runner against the target environment's business database under the migrator lease and fence, applies the pending migrations in sequence, prints the receipts and compatibility record without any secret, applies a backfill, cutover or contract migration only when the release manifest names it for this deployment (contract only with the explicit consent flag and after its soak), and before promoting a Worker or image checks the compatible-rollback rule so that a build the read or write horizon excludes is never promoted. The step is exercised once against the proof environment under the RES-cloud-deployment lease and records its result; production receives the same step only through the existing gated main-push deployment job. It adds no schema, no runner behavior and no deployment secret to pull-request code.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-70` and ledger record `ledger/tasks/cloud-70.md` in the Plan repository; task branch `task/cloud-70` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-21.03](../../work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03) — the deployment-job application of the migration runner and its compatibility flow: a gated migration step in the existing deployment pipeline that holds the migrator lease and fence, applies the pending locked migrations in sequence with receipts, surfaces the receipts and the compatibility record in the job, orders expand, backfill, cutover and contract across deployments, and refuses an application build that the schema horizons exclude (the compatible-rollback rule); the manifest, the runner, the adapters and the conformance evidence stay with CLOUD.03 |
| Provides | d1-migration-deployment |
| Start prerequisites | **artifact** [CLOUD.03](#task-cloud-03) — the migration runner, its REST client, the locked migration catalog and the compatible-rollback rule to run from the deployment job. *Why:* the deployment step is a thin gated caller of the runner; there is nothing to run before CLOUD.03 delivers it<br>**artifact** [CLOUD.01](#task-cloud-01) — the existing gated deployment job and the proof environment the step is added to and exercised in. *Why:* the step extends the deployment pipeline CLOUD.01 established and is proven in its proof environment |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.07](#task-cloud-07), [CLOUD.09](#task-cloud-09), [CLOUD.10](#task-cloud-10), [CLOUD.39](#task-cloud-39) |
| Write scope | `Cloud:.github/workflows/ci.yml (only one gated migration step in the existing main-push deployment job and the proof deployment job, run before the Worker or image is promoted; the pull-request jobs gain no secret and no migration step; the workflow is shared build configuration and the Cloud integration owner resolves ordering conflicts at merge)`<br>`Cloud:tooling/cloudflare.ts and Cloud:eng/migrations/deploy.ts (the deployment-time caller of the runner: environment-to-database selection from the existing deployment configuration, the release manifest's migration plan, the compatible-rollback check and the receipt report; no change to the runner, the catalog, the manifest or the adapters)`<br>`Cloud:tests/worker/d1-migration-deploy*.test.ts (new files only: the step against the SQLite and fake-REST oracles, the refusal of an excluded build, no secret in any output)`<br>`Cloud:package.json (only the new test files in the test list and one script) and Cloud:tsconfig.json (only if a new folder needs the include)`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/cloud-70-*.json (new immutable successor chained from the then-active receipt, only because hash-bound inputs change; no coordinate, integrity value or closure entry changes)`<br>`Cloud:eng/provenance/** (immutable successor records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt)`<br>`Cloud:docs/d1-migration-deployment.md (new, factual description of the gated step, its environment variables by name only, the proof-environment run and the rollback flow; docs/deployment.md stays with CLOUD.09)` |
| Shared resources | [RES-cloud-deployment](../shared-resources.md#res-cloud-deployment) (append) |
| Validation | offline tests of the deployment caller against the SQLite oracle and a fake REST client (gated order, receipts printed, excluded build refused, no secret in any output, a contract refused without consent); one explicit proof-environment run under the RES-cloud-deployment lease per docs/validation-policy.md, recorded once; no pull-request job receives a secret and none runs a live service |
| Completion evidence | the proof-environment run's job result and receipt report (receipt and fence values, never a secret), the refusal test results and the source commit |
| Baseline (unreviewed unless accepted) | not-started Planning repair 2026-10-05: no workflow step, script or document applies migrations to a deployed D1 database; CLOUD.03's runner is run only locally and against workerd's D1. |
| Notes | Planning repair 2026-10-05 ([DLV-34](../README.md#rule-dlv-34): a new task gives work no existing scope could hold; no obligation or acceptance is removed). CLOUD.03 delivers the runner and states that no workflow step runs it; CLOUD.07 (wrangler.json and capacity), CLOUD.09 (docs/deployment.md and eng/selfhost) and CLOUD.10 (artifacts/candidate) cannot hold a .github/workflows/ci.yml edit, and only the completed PRF.07 listed it. Modules whose live acceptance runs against a deployed schema (CLOUD.07, CLOUD.09, CLOUD.10, CLOUD.39) complete after it; no task's start waits for it, so offline and local-oracle module work is not delayed. |

<a id="task-cloud-71"></a>

### CLOUD.71 — Serve the built Web profiles from the proof origin

**Outcome.** The two production profile builds of PRF.08 are served, byte for byte, by the proof Worker (custom domain proof.arcforges.com, workers.dev and previews stay disabled) as static assets on separate paths of the same origin that serves /api, /session/v1 and the operator-signed /proof/v1 surface, which keep going to the Worker first. The bytes come from one immutable digest-named bundle that the Web main-push build publishes; the Cloud proof deployment job (manual proof=deploy) downloads that exact asset, verifies its digest against the value pinned in the deployment manifest and binds it as the Worker's assets, so nothing is rebuilt and no Web source is read. Responses carry the profile Content-Security-Policy that PRF.08 derives. Production configuration and the Web apex Custom Domain are untouched. The result is exercised once with PRF.08's live script (apps/app/scripts/proof-run.ts) pointed at the served profiles under the RES-cloud-deployment lease and the run's result is recorded.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/cloud-71` and ledger record `ledger/tasks/cloud-71.md` in the Plan repository; task branch `task/cloud-71` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | service / S |
| Obligations | [WP-06.05](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.05) — the deployed same-origin hosting of the two built production profiles (Account and Chat) on the proof origin, so that the page, /api and /session/v1 share one origin, cookie and CSRF boundary on a deployed Cloudflare; the profile builds, their budgets and their offline proof stay with PRF.08 |
| Provides | proof-origin-web-hosting |
| Start prerequisites | **artifact** [PRF.07](runtime-proofs.md#task-prf-07) — the deployed proof environment, its custom domain, its operator-signed surface and its manual deployment job. *Why:* the profiles are served by the proof Worker and deployed by its existing job<br>**artifact** [PRF.08](runtime-proofs.md#task-prf-08) — the two production profile builds and their measured, deterministic output (npm run build:profiles) and the live script that exercises them. *Why:* there are no Web bytes to serve or live script to run before PRF.08 delivers them |
| Entry condition | [ADOPT.07.cloud](adoption.md#task-adopt-07-cloud) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [PRF.08](runtime-proofs.md#task-prf-08) |
| Write scope | `Cloud:wrangler.json (only env.proof: the static-assets binding and the routing so that /api, /session/v1 and /proof/v1 reach the Worker first; no production, no other environment and no binding change)`<br>`Cloud:worker/foundation/** (only the proof route fragment, and only if the assets configuration alone cannot keep the three route families on the Worker)`<br>`Cloud:.github/workflows/ci.yml and Cloud:eng/verification/proof-deploy.ts (only the manual proof deployment job: download the digest-named bundle asset, verify the pinned digest, stage it as the proof assets; no pull-request job gains a secret, a download or a live call)`<br>`Cloud:tests/worker/proof-assets*.test.ts (new files only: route precedence, digest refusal, headers)`<br>`Cloud:package.json (only the new test files in the test list)`<br>`Cloud:eng/policy/dependency-policy.json and Cloud:eng/policy/dependency-reviews/cloud-71-*.json (new immutable successor chained from the then-active receipt, only because hash-bound inputs change; no coordinate or closure entry changes)`<br>`Cloud:eng/provenance/** (immutable successor records only where an existing record binds an input this task changes, the first-party inventory files.json and the deterministic NOTICE.txt)`<br>`Cloud:docs/prf-07-foundation-proof.md and Cloud:docs/cloud-ingress.md (factual additions about the served profiles and the proof run)`<br>`Web:.github/workflows/ci.yml (only: one step of the existing main-push deployment job that publishes the two profile builds as one immutable digest-named release asset next to the existing candidate asset; no new job, runner, credential or pull-request step)`<br>`Web:apps/app/scripts/** and Web:docs/prf-08-*.md (only the bundling script for that asset and the factual record of the served-profile run, and the interaction-budgets.json that the live run produces)` |
| Shared resources | [RES-cloud-deployment](../shared-resources.md#res-cloud-deployment) (append), [RES-cloud-host-composition](../shared-resources.md#res-cloud-host-composition) (append) |
| Validation | offline tests of route precedence, digest verification and headers; one explicit proof-environment deployment and one live run under the RES-cloud-deployment lease per docs/validation-policy.md, recorded once; no pull-request job receives a secret and none runs a live service |
| Completion evidence | the proof deployment job result with the verified bundle digest, the live run's output (observations and interaction timings, never a secret or a session handle) and the source commits |
| Baseline (unreviewed unless accepted) | not-started Planning repair 2026-10-05: the proof Worker (arcforges-cloud-proof) serves /api, /session/v1 and /proof/v1 only; wrangler.json has no assets binding. |
| Notes | Planning repair 2026-10-05 ([DLV-34](../README.md#rule-dlv-34): a new task gives work no existing scope could hold; no obligation or acceptance is removed). PRF.08's completion needs the built profiles to share an origin with the deployed ingress; the proof Worker has no assets binding and no existing Cloud or Web task owns one. WEB.30 cannot hold it because it consumes PRF.08, so an edge from PRF.08 to it would be a cycle; this task starts after PRF.08 delivers the profiles and PRF.08 completes after it. No task's start waits for it. |
