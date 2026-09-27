# Family governance and policy tests — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Accepted freeze, reconciliation and build-governance baselines, and the per-repository architecture and policy test suites.

Tasks: 16 · Owning repositories: AI, ArcScope, Cloud, Contracts, DesktopPlatform, Mobile, Web · Integration owner(s): AI integration owner, ArcScope integration owner, Cloud integration owner, Contracts integration owner, DesktopPlatform integration owner, Mobile integration owner, Web integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [GOV.01](#task-gov-01) | Specification, naming, licence-boundary and provenance freeze (WP00, accepted) | governance | XL | none | accepted |
| [GOV.02](#task-gov-02) | Repository reconciliation and target layout (WP01, accepted) | governance | XL | [GOV.01](#task-gov-01) (artifact) | accepted |
| [GOV.03](#task-gov-03) | Build governance, packaging policy and analyzers (WP02, accepted) | governance | XL | [GOV.02](#task-gov-02) (artifact) | accepted |
| [GOV.04](#task-gov-04) | Shared architecture/repository policy-test engine and DesktopPlatform enforcement | governance | L | [GOV.03](#task-gov-03) (artifact), [GOV.01](#task-gov-01) (artifact), [GOV.18](#task-gov-18) (artifact), [CON.23](contracts.md#task-con-23) (artifact) | not-started |
| [GOV.05](#task-gov-05) | Contracts policy tests and contract/serialization policy engine | governance | L | [GOV.04](#task-gov-04) (artifact), [CON.90](contracts.md#task-con-90) (contract), [CON.23](contracts.md#task-con-23) (artifact) | not-started |
| [GOV.07](#task-gov-07) | ArcScope policy tests | governance | S | [GOV.04](#task-gov-04) (artifact), [GOV.05](#task-gov-05) (artifact) | not-started |
| [GOV.09](#task-gov-09) | Cloud policy tests | governance | M | [GOV.04](#task-gov-04) (artifact), [GOV.05](#task-gov-05) (artifact) | not-started |
| [GOV.10](#task-gov-10) | AI (Workflow Harness) policy tests | governance | S | [GOV.04](#task-gov-04) (artifact), [GOV.05](#task-gov-05) (artifact) | not-started |
| [GOV.11](#task-gov-11) | Web policy tests (Node/TS mechanism) | governance | M | [GOV.03](#task-gov-03) (artifact), [GOV.01](#task-gov-01) (artifact), [CON.23](contracts.md#task-con-23) (artifact) | not-started |
| [GOV.12](#task-gov-12) | Mobile policy tests (Gradle/Kotlin mechanism) | governance | M | [GOV.03](#task-gov-03) (artifact), [GOV.04](#task-gov-04) (artifact) | not-started |
| [GOV.13](#task-gov-13) | Invariant enforcement accounting report | governance | M | [GOV.04](#task-gov-04) (artifact), [GOV.18](#task-gov-18) (artifact) | not-started |
| [GOV.14](#task-gov-14) | Specification integrity checks over the Design repository | governance | M | [GOV.01](#task-gov-01) (artifact), [GOV.18](#task-gov-18) (artifact) | not-started |
| [GOV.15](#task-gov-15) | WP05 stage integration verification | integration | M | [GOV.04](#task-gov-04) (artifact), [GOV.05](#task-gov-05) (artifact), [GOV.07](#task-gov-07) (artifact), [GOV.09](#task-gov-09) (artifact), [GOV.10](#task-gov-10) (artifact), [GOV.11](#task-gov-11) (artifact), [GOV.12](#task-gov-12) (artifact), [GOV.13](#task-gov-13) (artifact), [GOV.14](#task-gov-14) (artifact) | not-started |
| [GOV.16](#task-gov-16) | Operation-catalogue authorization reachability matrix and identity boundary evidence | governance | M | [CON.18](contracts.md#task-con-18) (contract) | not-started |
| [GOV.17](#task-gov-17) | Retire the native families outside the product family and move the still-image shim | governance | M | none | not-started |
| [GOV.18](#task-gov-18) | Reduce the DesktopPlatform policy data and re-pin the design-policy export | governance | M | [CON.23](contracts.md#task-con-23) (artifact) | not-started |

## Tasks

<a id="task-gov-01"></a>

### GOV.01 — Specification, naming, licence-boundary and provenance freeze (WP00, accepted)

**Outcome.** WP00's naming/licence/provenance freeze is accepted across the seven implementation repositories: product-names.json, exported glossary/invariant policy data, per-project SPDX licence boundaries, a working provenance process and five registered Reference Coverage Matrices are in place, scanned clean, and enforced in CI.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/gov-01` and ledger record `ledger/tasks/gov-01.md` in the Plan repository; task branch `task/gov-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / XL · early risk proof |
| Obligations | [WP-00.00](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.00) — full<br>[WP-00.01](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.01) — full<br>[WP-00.02](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.02) — full<br>[WP-00.03](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.03) — full<br>[WP-00.04](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.04) — full<br>[WP-00.05](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.05) — full<br>[WP-00.90](../../work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.90) — full |
| Provides | product-names-policy-v1; glossary-invariant-policy-v1; licence-boundary-declarations; provenance-process-v1; reference-matrix-registrations |
| Start prerequisites | none |
| Completion prerequisites | none |
| Unblocks | [CON.23](contracts.md#task-con-23), [GOV.02](#task-gov-02), [GOV.04](#task-gov-04), [GOV.11](#task-gov-11), [GOV.14](#task-gov-14) |
| Write scope | `Contracts:eng/policy/product-names.json`<br>`DesktopPlatform:eng/policy/glossary-terms.json`<br>`DesktopPlatform:eng/policy/invariants.json`<br>`DesktopPlatform:eng/policy/reference-baselines.json`<br>`*:NOTICE.md`<br>`*:LICENSE`<br>`*:Directory.Build.props` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Design-repo-pinned exporter (DesktopPlatform/eng/design_policy.py) verified against an immutable, clean pinned Design commit; offline forbidden-term scanner over the implementation repositories in Contracts CI; no macOS/device/live-service runtime, per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | docs/assurance/wp00-03-implementation-evidence.md, wp00-04-implementation-evidence.md, wp00-05-implementation-evidence.md, wp00-stage-acceptance.md, wp00-stage-acceptance.json (file names only, via ls; bodies not read per assignment). |
| Baseline (unreviewed unless accepted) | accepted — Design receipts wp00-stage-acceptance.md/.json and the recorded executions in wp00-03, wp00-04 and wp00-05 implementation evidence. |
| Notes | Executed across the seven implementation repositories plus Contracts' product-names.json; represented as one accepted task for the whole closed package rather than one task per substep, per the assignment's 'small number of GOV tasks' instruction. |

<a id="task-gov-02"></a>

### GOV.02 — Repository reconciliation and target layout (WP01, accepted)

**Outcome.** WP01 reconciliation is accepted: seven-repository disposition inventory executed against ede43db, the Contracts public/internal Apache-2.0 split assigned, the shared-foundation boundary reviewed, native surface dispositions executed (MDF excluded), all eighteen test families mapped, bounded reconciliation applied, and Cloud's 19 domain owners recorded.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/gov-02` and ledger record `ledger/tasks/gov-02.md` in the Plan repository; task branch `task/gov-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / XL |
| Obligations | [WP-01.00](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.00) — full<br>[WP-01.01](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.01) — full<br>[WP-01.02](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.02) — full<br>[WP-01.03](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.03) — full<br>[WP-01.04](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.04) — full<br>[WP-01.05](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.05) — full<br>[WP-01.90](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.90) — full<br>[WP-01](../../work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01) Cloud module layout acceptance - map 17 historical scaffold names to the 21 declared domain owners in WP21; Cloud owns the Native AOT Container host and Worker bindings, AI owns the sole Workflow Harness; empty module projects are not created during reconciliation — package-level obligation contribution |
| Provides | contract-licence-split-assignment; shared-foundation-boundary-classification; native-admission-record; test-family-coverage-map; cloud-domain-owner-map |
| Start prerequisites | **artifact** [GOV.01](#task-gov-01) — WP00's naming/licence freeze closed (GOV.01). *Why:* reconciliation dispositions classify every project against the frozen naming/licence boundary; nothing can be dispositioned before that boundary is fixed |
| Completion prerequisites | none |
| Unblocks | [GOV.03](#task-gov-03) |
| Write scope | `*:every .csproj disposition`<br>`Contracts:src/Contracts/`<br>`*:native/`<br>`*:eng/policy/reconciliation/` |
| Validation | Clean-checkout builds with no sibling source, licence/reference-direction checks, offline; per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) no macOS/device runtime. |
| Completion evidence | docs/assurance/wp01-00-implementation-evidence.md/.json, wp01-00-inventory-policy.md, wp01-01-contract-access-policy.md, wp01-01-implementation-evidence.md/.json, wp01-02-foundation-review.md/.json, wp01-03-native-reconciliation-policy.md, wp01-03-native-reconciliation.md/.json, wp01-04-test-family-map.md/.json, wp01-05-bounded-reconciliation.md/.json, wp01-stage-acceptance.md/.json (file names only, via ls; bodies not read). |
| Baseline (unreviewed unless accepted) | accepted — Design receipts wp01-stage-acceptance.md/.json and the recorded executions of substeps 01.00 to 01.05. |
| Notes | Also closes the unlabeled 'Cloud module layout acceptance' package obligation (17 historical scaffold names -> 21 declared WP21 domain owners); see package_obligations. |

<a id="task-gov-03"></a>

### GOV.03 — Build governance, packaging policy and analyzers (WP02, accepted)

**Outcome.** WP02 build governance is accepted: pinned/locked toolchains in all seven owners, warnings-as-errors with an empty authored-code waiver list, a complete AOT/trim declaration sweep with zero unassigned diagnostics, verified runtime/directory boundaries, all nine version axes producible, and dependency-admission policy encoded as data.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/gov-03` and ledger record `ledger/tasks/gov-03.md` in the Plan repository; task branch `task/gov-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / XL · early risk proof |
| Obligations | [WP-02.00](../../work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.00) — full<br>[WP-02.01](../../work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.01) — full<br>[WP-02.02](../../work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.02) — full<br>[WP-02.03](../../work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.03) — full<br>[WP-02.04](../../work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.04) — full, under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)<br>[WP-02.05](../../work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.05) — full, under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)<br>[WP-02.90](../../work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.90) — full |
| Provides | locked-toolchain-pins; warnings-as-errors-build; aot-trim-diagnostic-posture; runtime-boundary-config; version-axis-plumbing; dependency-admission-policy |
| Start prerequisites | **artifact** [GOV.02](#task-gov-02) — WP01's settled project set and dispositions (GOV.02). *Why:* build properties and lock files are applied per-project; the project set must be settled first |
| Completion prerequisites | none |
| Unblocks | [GOV.04](#task-gov-04), [GOV.11](#task-gov-11), [GOV.12](#task-gov-12), [REL.06](release.md#task-rel-06), [WEB.01](web.md#task-web-01), [WEB.08](web.md#task-web-08) |
| Write scope | `*:global.json`<br>`*:Directory.Build.props/.targets`<br>`*:Directory.Packages.props`<br>`*:packages.lock.json`<br>`DesktopPlatform:eng/build/desktop-aot.props`<br>`Cloud:eng/build/cloud-aot.props`<br>`Mobile:gradle/*`<br>`Web:package.json,package-lock.json,.node-version,.npmrc,ArcForges.Web.esproj`<br>`Contracts:eng/build/contracts.props`<br>`*:.editorconfig`<br>`DesktopPlatform:eng/policy/dependency-policy.json` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Clean-machine locked restores, warnings-as-errors full-solution build, complete AOT/trim diagnostic sweep, per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) reduced CI for 02.04/02.05 (no new macOS/device/download runtime). |
| Completion evidence | docs/assurance/wp02-00-implementation-evidence.md/.json, wp02-00-toolchain-profile.md, wp02-01-diagnostic-profile.md, wp02-01-implementation-evidence.md/.json, wp02-02-aot-sweep-evidence.md/.json, wp02-03-runtime-boundary-evidence.md/.json, wp02-03-runtime-boundary-profile.md, wp02-04-implementation-evidence.md/.json, wp02-04-version-identity-profile.md, wp02-05-dependency-policy-profile.md, wp02-05-implementation-evidence.md/.json, wp02-stage-acceptance.md/.json (file names only, via ls; bodies not read). |
| Baseline (unreviewed unless accepted) | accepted — Design receipts wp02-stage-acceptance.md/.json and the recorded executions of substeps 02.00 to 02.05. |
| Notes | [VG-08](../../../assurance/open-gates-register.md#rule-vg-08) (framework upgrade re-verification) is explicitly recurring: WP02.05's evidence closes the first instance only; every future dependency/framework upgrade re-triggers [VG-08](../../../assurance/open-gates-register.md#rule-vg-08) outside this task's own closure. |

<a id="task-gov-04"></a>

### GOV.04 — Shared architecture/repository policy-test engine and DesktopPlatform enforcement

**Outcome.** A reusable [AT-01](../../../architecture/01-solution-and-project-layout.md#rule-at-01)..14/[RP-01](../../../architecture/01-solution-and-project-layout.md#rule-rp-01)..10 rule engine, project-graph reader, fixture compiler and banned-symbol scanner extend DesktopPlatform's existing 5-method RepositoryPolicyTests.cs baseline (WP01.04) to the full rule set, are published for the other six repositories to reuse, and DesktopPlatform's own project graph is fully enforced with one positive and one failing negative fixture per rule.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/gov-04` and ledger record `ledger/tasks/gov-04.md` in the Plan repository; task branch `task/gov-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / L · early risk proof |
| Obligations | [WP-05.00](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.00) — build the reusable [AT-01](../../../architecture/01-solution-and-project-layout.md#rule-at-01)..14/[RP-01](../../../architecture/01-solution-and-project-layout.md#rule-rp-01)..10 rule engine and project-graph reader; apply it to DesktopPlatform's own layering/reference-direction rules<br>[WP-05.01](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01) — licence-boundary rule implementation in the shared engine; DesktopPlatform's own licence-boundary enforcement<br>[WP-05.04](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.04) — banned-symbol scanner mechanism in the shared engine; DesktopPlatform's own banned-API fixtures<br>[WP-05.02](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.02) — wire the existing WP00.00 forbidden-term scanner into DesktopPlatform's own PR build as a failing policy test |
| Provides | architecture-policy-rule-engine-v1; project-graph-reader; fixture-compiler; banned-symbol-scanner |
| Start prerequisites | **artifact** [GOV.03](#task-gov-03) — a build that fails on warnings/AOT diagnostics (GOV.03). *Why:* WP05 [BR-02](../../../architecture/14-build-packaging-and-release.md#rule-br-02): a policy-test failure must be a build failure; without WP02's warnings-as-errors/AOT posture there is nothing for a new policy test to fail against<br>**artifact** [GOV.01](#task-gov-01) — exported glossary-terms.json/invariants.json policy data (GOV.01). *Why:* the layering/shared-foundation rules and forbidden-alias checks read this generated policy data directly rather than re-deriving it<br>**artifact** [GOV.18](#task-gov-18) — policy data reduced to the retained repositories. *Why:* the shared policy-test engine is built over the cleaned policy data<br>**artifact** [CON.23](contracts.md#task-con-23) — Immutable canonical naming policy/scanner build-time candidate asset. *Why:* The repository policy suite consumes Contracts-owned published naming authority without sibling source imports or copied rules. |
| Entry condition | [ADOPT.02.governance](adoption.md#task-adopt-02-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [GOV.05](#task-gov-05), [GOV.07](#task-gov-07), [GOV.09](#task-gov-09), [GOV.10](#task-gov-10), [GOV.12](#task-gov-12), [GOV.13](#task-gov-13), [GOV.15](#task-gov-15) |
| Write scope | `DesktopPlatform:src/Build/ArcForges.Build.Policy/Architecture/** (single shared C# policy engine, project graph, fixture compiler, banned-symbol scanner and explicit opt-in source-link props)`<br>`DesktopPlatform:src/Build/ArcForges.Build.Policy/ArcForges.Build.Policy.csproj (package the same engine source as tools/architecture build-only assets; preserve existing default behavior and package identity)`<br>`DesktopPlatform:src/Build/ArcForges.Build.Policy/README.md (owned opt-in test/build-only engine contract)`<br>`DesktopPlatform:tests/ArchitectureTests/**`<br>`DesktopPlatform:eng/policy/exceptions.json`<br>`DesktopPlatform:Directory.Packages.props (exact canonical naming-tool package pin)`<br>`DesktopPlatform:eng/policy/dependency-policy.json (canonical naming-tool admission)`<br>`DesktopPlatform:eng/policy/dependency-reviews/** (new immutable naming-tool admission receipt)`<br>`DesktopPlatform:eng/provenance/** (owned naming-tool inventory and new receipts; preserve historical records)` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline unit/analyzer-style project-graph assertions, one positive and one failing negative fixture per rule, runs in PR CI; no macOS/device/live runtime per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Full [AT-01](../../../architecture/01-solution-and-project-layout.md#rule-at-01)..14/[RP-01](../../../architecture/01-solution-and-project-layout.md#rule-rp-01)..10 rule table with pass/fail fixture pairs; banned-symbol detection results per category (reflection on AOT paths, dynamic codegen, blocking waits on async paths, direct provider SDK calls outside adapters, secret/content logging, float money arithmetic, raw pointer fields). |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: DesktopPlatform/eng/design_graph.py and eng/design_policy.py (read directly, full text) implement adjacent but distinct corpus/graph checks over the DESIGN repo, not this task's own ArchitectureTests (see GOV.14 for what those two files actually assert). tests/ArchitectureTests/RepositoryPolicyTests.cs itself was not read (out of the minimal-reading scope given); WP05 section 4 states it currently has five bounded methods per the WP01.04 baseline. |
| Notes | The existing ArcForges.Build.Policy package publishes one C# engine source under tools/architecture, linked explicitly into offline consumer policy tests through ArchitecturePolicy.props. DesktopPlatform ArchitectureTests exercise that same producer source; no copied Python engine, new package identity, implicit default hook or product runtime dependency. Preserve existing AGPL/build-only and PrivateAssets boundaries. The already pinned SDK Roslyn assemblies may serve the offline fixture compiler under existing dependency admission; do not introduce a new NuGet dependency or provision another SDK. Necessary existing project/packaging/lock/inventory/provenance bindings follow [ADP-07](../adoption.md#rule-adp-07) with exact paths and evidence recorded before editing. This is the shared-tooling half of WP05's own binding statement: 'Repositories: Each repository; shared tooling in Platform/Contracts.' |

<a id="task-gov-05"></a>

### GOV.05 — Contracts policy tests and contract/serialization policy engine

**Outcome.** Contracts enforces its own layering/licence/banned-API rules using GOV.04's shared engine, and implements the contract/serialization policy engine that makes [VG-04](../../../assurance/open-gates-register.md#rule-vg-04)'s policy-test half enforceable and that GOV.07 and GOV.09-GOV.12 reuse for their own generated-client checks.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/gov-05` and ledger record `ledger/tasks/gov-05.md` in the Plan repository; task branch `task/gov-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / L |
| Obligations | [WP-05.03](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.03) — full: build the contract/serialization policy engine (generated-from-proto DTO check, explicit JSON metadata for HTTP exceptions, no reflection-based serializer reachable, every local RPC contract interface carries the generated service/descriptor identity, generated artifacts match the committed baseline) and apply it to Contracts itself<br>[WP-05.00](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.00) — Contracts layering: contract projects reference only contract projects and the foundation<br>[WP-05.01](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01) — Contracts licence-boundary enforcement (public/internal Apache-2.0 split from WP01.01)<br>[WP-05.02](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.02) — wire the forbidden-term scanner into Contracts' own PR build as a failing policy test<br>[WP-05.04](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.04) — Contracts banned-API fixtures |
| Provides | contract-serialization-policy-engine; contract-generated-baseline-check |
| Start prerequisites | **artifact** [GOV.04](#task-gov-04) — published shared AT-*/RP-* rule engine, fixture compiler and project-graph reader. *Why:* 05.00/05.01/05.04 rule implementations must reuse one tested engine rather than reimplementing it per repository<br>**contract** [CON.90](contracts.md#task-con-90) — Contracts' public/internal Apache-2.0 project split and generated proto baseline. *Why:* 05.03 checks that generated artifacts match a committed baseline and that no public type transitively depends on an internal one; there is no generated baseline to check against before WP03 lands<br>**artifact** [CON.23](contracts.md#task-con-23) — retired Contracts elements removed and reserved. *Why:* the Contracts policy tests run over the cleaned naming data and record set |
| Entry condition | [ADOPT.03.governance](adoption.md#task-adopt-03-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [GOV.07](#task-gov-07), [GOV.09](#task-gov-09), [GOV.10](#task-gov-10), [GOV.15](#task-gov-15) |
| Write scope | `Contracts:tests/ArchitectureTests/**`<br>`Contracts:eng/policy/exceptions.json` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
| Validation | Offline unit tests, negative fixtures per assertion, PR CI; no live-service runtime per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Contract/serialization policy results with negative fixtures per assertion; Contracts' own layering/licence/banned-API results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | WP05's own §8 completion-gate text states this substep 'makes [VG-04](../../../assurance/open-gates-register.md#rule-vg-04)'s policy-test half enforceable' - a second [VG-04](../../../assurance/open-gates-register.md#rule-vg-04) contributor not listed in the README's deferred-gate table (which names only 03.04/06.01). |

<a id="task-gov-07"></a>

### GOV.07 — ArcScope policy tests

**Outcome.** ArcScope enforces its own layering/licence/naming/banned-API/contract-consumption rules independently.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/gov-07` and ledger record `ledger/tasks/gov-07.md` in the Plan repository; task branch `task/gov-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / S |
| Obligations | [WP-05.00](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.00) — ArcScope slice<br>[WP-05.01](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01) — ArcScope slice<br>[WP-05.02](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.02) — wire the forbidden-term scanner into ArcScope's own PR build<br>[WP-05.03](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.03) — ArcScope's generated-client consumption checks<br>[WP-05.04](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.04) — ArcScope banned-API fixtures |
| Provides | arcscope-policy-suite |
| Start prerequisites | **artifact** [GOV.04](#task-gov-04) — published shared rule engine. *Why:* reuse one tested engine rather than reimplementing per repository<br>**artifact** [GOV.05](#task-gov-05) — contract/serialization policy helpers. *Why:* ArcScope consumes generated Contracts clients; the 'local RPC contract interface carries the generated descriptor identity' check needs GOV.05's engine, not a reimplementation |
| Entry condition | [ADOPT.05.governance](adoption.md#task-adopt-05-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [GOV.15](#task-gov-15) |
| Write scope | `ArcScope:tests/ArchitectureTests/**`<br>`ArcScope:eng/policy/exceptions.json` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
| Validation | Offline unit tests, negative fixtures, PR CI; per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Per-rule pass/fail fixture table for ArcScope's project graph. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Fixture-driven; does not require ArcScope's own product work (WP33 to WP35) to have landed. |

<a id="task-gov-09"></a>

### GOV.09 — Cloud policy tests

**Outcome.** Cloud enforces its own layering/licence/naming/banned-API/contract-consumption rules independently, with extra weight on AOT-path banned APIs given [BR-07](../../../architecture/14-build-packaging-and-release.md#rule-br-07)'s zero-trim/AOT-diagnostic requirement.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/gov-09` and ledger record `ledger/tasks/gov-09.md` in the Plan repository; task branch `task/gov-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / M |
| Obligations | [WP-05.00](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.00) — Cloud slice<br>[WP-05.01](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01) — Cloud slice<br>[WP-05.02](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.02) — wire the forbidden-term scanner into Cloud's own PR build<br>[WP-05.03](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.03) — Cloud's own generated public API/RPC descriptor checks<br>[WP-05.04](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.04) — Cloud banned-API fixtures, weighted toward AOT-path reflection/dynamic-codegen since Cloud is the Native AOT host |
| Provides | cloud-policy-suite |
| Start prerequisites | **artifact** [GOV.04](#task-gov-04) — published shared rule engine. *Why:* reuse one tested engine rather than reimplementing per repository<br>**artifact** [GOV.05](#task-gov-05) — contract/serialization policy helpers. *Why:* Cloud hosts the generated public API surface that 05.03 validates |
| Entry condition | [ADOPT.07.governance](adoption.md#task-adopt-07-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [GOV.15](#task-gov-15) |
| Write scope | `Cloud:tests/ArchitectureTests/**`<br>`Cloud:eng/policy/exceptions.json` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
| Validation | Offline unit tests, negative fixtures, PR CI; per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (Cloud's real AOT publish proof is WP06/WP21, not claimed here). |
| Completion evidence | Per-rule pass/fail fixture table for Cloud's project graph. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Fixture-driven; does not require Cloud's own product work (WP21 to WP26) to have landed. |

<a id="task-gov-10"></a>

### GOV.10 — AI (Workflow Harness) policy tests

**Outcome.** AI enforces its own layering/licence/naming/banned-API/contract-consumption rules independently as the sole owner of the Workflow Harness (per WP01's Cloud/AI module split).

| Field | Value |
|---|---|
| Owning repository | AI (`C:\MyFile\Projects\ArcForges\AI`); integration owner: AI integration owner, the holder of `roles/integration-ai` |
| Claim, branch and ledger | `claims/gov-10` and ledger record `ledger/tasks/gov-10.md` in the Plan repository; task branch `task/gov-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / S |
| Obligations | [WP-05.00](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.00) — AI slice<br>[WP-05.01](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01) — AI slice<br>[WP-05.02](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.02) — wire the forbidden-term scanner into AI's own PR build<br>[WP-05.03](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.03) — AI's generated-client consumption checks<br>[WP-05.04](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.04) — AI banned-API fixtures |
| Provides | ai-policy-suite |
| Start prerequisites | **artifact** [GOV.04](#task-gov-04) — published shared rule engine. *Why:* reuse one tested engine rather than reimplementing per repository<br>**artifact** [GOV.05](#task-gov-05) — contract/serialization policy helpers. *Why:* the Workflow Harness consumes generated Contracts clients; its generated-client checks need GOV.05's engine, not a reimplementation |
| Entry condition | [ADOPT.08.governance](adoption.md#task-adopt-08-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [GOV.15](#task-gov-15) |
| Write scope | `AI:tests/ArchitectureTests/**`<br>`AI:eng/policy/exceptions.json` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
| Validation | Offline unit tests, negative fixtures, PR CI; per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Per-rule pass/fail fixture table for AI's project graph. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Fixture-driven; does not require AI's own product work (WP40 to WP43, WP52) to have landed. |

<a id="task-gov-11"></a>

### GOV.11 — Web policy tests (Node/TS mechanism)

**Outcome.** Node/TS import and dependency policy checks enforce one Web workspace/lock, exact Node/npm/generator pins, SDK-to-UI licence separation, generated wire types only, no private/server/local-RPC imports, desktop JS/DOM prohibition scoped to desktop graphs, no obsolete Blazor target in the active Web graph, no esproj in portable managed references, no implicit npm install or production dev/HMR server, and no TS fixtures/test helpers in the release route graph - each with a passing and a failing negative example.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/gov-11` and ledger record `ledger/tasks/gov-11.md` in the Plan repository; task branch `task/gov-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / M |
| Obligations | [WP-05.01](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01) — Web slice: SDK-to-UI licence separation<br>[WP-05.02](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.02) — wire the forbidden-term scanner into Web's own PR build<br>[WP-05.04](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.04) — Web banned dependency/route fixtures<br>[WP-05](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) Web repository and architecture assertions (unlabeled paragraph after [WP-05.06](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.06)): Node/TS import and dependency checks - one Web workspace/lock, exact Node/npm/generator pins, SDK-to-UI licence separation, generated wire types only, no private/server/local-RPC imports, desktop JS/DOM prohibition scoped to desktop graphs, no obsolete Blazor target, no esproj in portable managed references, no implicit npm install or production dev/HMR server, no TS fixtures/test helpers in the release route graph — package-level obligation contribution |
| Provides | web-policy-suite |
| Start prerequisites | **artifact** [GOV.03](#task-gov-03) — the one Node/npm workspace and Windows esproj adapter (GOV.03). *Why:* there is no Web toolchain to lint until WP02 creates package.json/package-lock/esproj<br>**artifact** [GOV.01](#task-gov-01) — licence boundary declarations (mobile-only/public-SDK Apache set). *Why:* the SDK-to-UI licence separation check needs the frozen Apache/AGPL boundary<br>**artifact** [CON.23](contracts.md#task-con-23) — Immutable canonical naming policy/scanner build-time candidate asset. *Why:* The repository policy suite consumes Contracts-owned published naming authority without sibling source imports or copied rules. |
| Entry condition | [ADOPT.09.governance](adoption.md#task-adopt-09-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [GOV.15](#task-gov-15) |
| Write scope | `Web:apps/site/app/cloud-hello.ts (remove obsolete explicit useBinaryFormat option for the pinned SDK that internally requires binary; no transport behavior change)`<br>`Web:tests/unit/contracts.test.ts (same pinned SDK option adaptation only; retain binary transport assertions)`<br>`Web:eng/policy/**`<br>`Web:.eslintrc*/lint-config for architecture rules`<br>`Web:tooling/project.ts (wire owned policy checks into existing PR gate)`<br>`Web:tests/unit/** (offline policy positive/negative fixtures)`<br>`Web:eng/provenance/** (owned policy source inventory and new receipts; preserve historical records)`<br>`Web:apps/site/package.json (exact published naming-tool candidate pin and required existing SDK lockstep)`<br>`Web:package-lock.json (regenerate exact naming-tool candidate lock)`<br>`Web:eng/policy/dependency-reviews/** (immutable naming-tool pin admission receipt)`<br>`Web:.gitleaks.toml (extend the existing anchored browser-resources-r1 through r6 path selection to r7 only for its eight actually observed public source-hash rows, reusing the unchanged five exact key/hash regexes, generic-api-key rule and AND condition; no new hash, rule, broad path or future receipt exemption)` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-web-build-config](../shared-resources.md#res-web-build-config) (append) |
| Validation | Node/npm-based static import-rule checks, offline, PR CI; no browser/E2E runtime here - that is [WP-06.05](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.05)/[WP-50.06](../../work-packages/50-full-platform-production-release.md#rule-wp-50.06), per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Per-rule pass/fail fixture table for the Web import/dependency graph. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Owns the unlabeled 'Web repository and architecture assertions' package obligation from WP05 (no [WP-05](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05).MM anchor); see package_obligations. Mechanism is necessarily separate code from GOV.04's.NET engine. The r7 public-digest support requires independently verifying all eight observed key/hash rows against r6 and their public inputs; six distinct digest values and all existing narrow matching conditions remain unchanged. This is explicit security-exception scope, not ADP.07 metadata support. A previously pushed exception change is not retroactive approval: preserve that history and require this authority, independent exact-head review and retained CI before merging the product PR. |

<a id="task-gov-12"></a>

### GOV.12 — Mobile policy tests (Gradle/Kotlin mechanism)

**Outcome.** Mobile enforces its own layering/licence/naming/banned-API rules independently via a Gradle-native mechanism (dependency verification plus lint/Detekt-style rules) that consumes the same rule DATA as the other repos, not GOV.04's.NET test library directly.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/gov-12` and ledger record `ledger/tasks/gov-12.md` in the Plan repository; task branch `task/gov-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / M |
| Obligations | [WP-05.00](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.00) — Mobile slice, via Gradle dependency-graph verification rather than the.NET engine<br>[WP-05.01](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01) — Mobile slice: licence boundary + dependency allowlist over Gradle dependencies<br>[WP-05.02](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.02) — wire the forbidden-term scanner into Mobile's own PR build<br>[WP-05.04](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.04) — Mobile banned-API fixtures |
| Provides | mobile-policy-suite |
| Start prerequisites | **artifact** [GOV.03](#task-gov-03) — pinned JDK 21/Kotlin/Compose/AGP toolchain (GOV.03). *Why:* there is nothing to lint until the Gradle toolchain is pinned<br>**artifact** [GOV.04](#task-gov-04) — the rule DATA (forbidden-term list, licence-boundary declarations, banned-API categories) as portable JSON, not the.NET engine itself. *Why:* Mobile's enforcement mechanism must be native to Gradle; only the rule definitions are shared, not the runtime |
| Entry condition | [ADOPT.10.governance](adoption.md#task-adopt-10-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [GOV.15](#task-gov-15) |
| Write scope | `Mobile:gradle/policy/**`<br>`Mobile:eng/policy/exceptions.json`<br>`Mobile:build.gradle.kts (apply owned Gradle-native policy and formatter target only)` |
| Shared resources | [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Offline Gradle-time checks, negative fixtures, PR CI; no device/emulator runtime here, per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (that is WP06.07/WP30/WP32). |
| Completion evidence | Per-rule pass/fail fixture table for Mobile's Gradle dependency graph. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [F-023](../../../assurance/open-gates-register.md#rule-f-023) (mobile provenance) and [VG-07](../../../assurance/open-gates-register.md#rule-vg-07) (Android runtime posture) are separately scheduled at WP06.07/WP30/WP32 and are not this task's concern. |

<a id="task-gov-13"></a>

### GOV.13 — Invariant enforcement accounting report

**Outcome.** A build-produced report classifies all current catalogued invariants (406 after reduced-family retirement) as enforced-and-passing / enforced-and-failing / not-yet-implemented, every classification derived from an actual test-run result, without re-deriving the design-stage mapping ([PG-06](../../../assurance/open-gates-register.md#rule-pg-06), already closed) and without itself closing [PG-11](../../../assurance/open-gates-register.md#rule-pg-11).

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/gov-13` and ledger record `ledger/tasks/gov-13.md` in the Plan repository; task branch `task/gov-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / M |
| Obligations | [WP-05.05](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.05) — full |
| Provides | invariant-accounting-report-v1 |
| Start prerequisites | **artifact** [GOV.04](#task-gov-04) — at least one owning package's real policy-test run to classify (DesktopPlatform's own AT-*/RP-* results). *Why:* the report's classifications must come from actual test-run results, not declared status; it needs at least one real producer before it can report anything besides 'not yet implemented' for every row<br>**artifact** [GOV.18](#task-gov-18) — the invariant export regenerated from this Design repository. *Why:* the accounting report reads the pinned invariant export, which must describe the reduced family |
| Entry condition | [ADOPT.02.governance](adoption.md#task-adopt-02-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [GOV.15](#task-gov-15) |
| Write scope | `DesktopPlatform:eng/accounting/invariant-report.py or equivalent`<br>`DesktopPlatform:artifacts/evidence/invariant-accounting.json` |
| Validation | Report generation reads real CI test-run results only; offline; re-run as each owning package lands enforcement (not a one-time close), per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)'s 'runtime checks local, affected-scope, once, existing environment only' spirit. |
| Completion evidence | Current-catalogue-complete accounting table, every row classified from a real result. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Will read as mostly 'not yet implemented' immediately after WP05 since most current invariants are owned by packages far downstream (WP06...WP53, per invariant-coverage.md's ownerCell). [PG-11](../../../assurance/open-gates-register.md#rule-pg-11) stays open per-invariant in its OWNING package; GOV.13 never closes [PG-11](../../../assurance/open-gates-register.md#rule-pg-11) or [PG-06](../../../assurance/open-gates-register.md#rule-pg-06) itself - it only reports. |

<a id="task-gov-14"></a>

### GOV.14 — Specification integrity checks over the Design repository

**Outcome.** Checks run against the current Design repository and produce zero findings: every internal link resolves; every cited requirement/architecture rule/decision/verification finding/gate identifier exists; no superseded name appears as current outside docs/deprecated-inputs/; every Phase 1 decision is cited by at least one Phase 2 document or its non-applicability is stated; the delivery graph has satisfiable prerequisites, current generated views and complete obligation coverage; and the decision-coverage check passes.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/gov-14` and ledger record `ledger/tasks/gov-14.md` in the Plan repository; task branch `task/gov-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / M |
| Obligations | [WP-05.06](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.06) — full: six checks over docs/ in ArcForges-Design, plus semantic coverage of the 22 retained Phase 1 rows, seven retained initial Phase 2 rows and twelve current closure groups; trace retired decisions through [P2-019](../../../decisions/phase-2-specification-decisions.md#rule-p2-019) without recreating removed obligations |
| Provides | spec-integrity-check-v1 |
| Start prerequisites | **artifact** [GOV.01](#task-gov-01) — the citation/anchor index and continuing drift check installed by GOV.01 ([PG-21](../../../assurance/open-gates-register.md#rule-pg-21)). *Why:* 05.06 extends the same corpus/citation machinery WP00.01 already established rather than building link-resolution from nothing<br>**artifact** [GOV.18](#task-gov-18) — the design-policy export re-pinned to this Design repository. *Why:* the integrity checks run against the pinned Design commit, which must be the reduced family |
| Entry condition | [ADOPT.02.governance](adoption.md#task-adopt-02-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [GOV.15](#task-gov-15) |
| Write scope | `DesktopPlatform:eng/design_policy.py`<br>`DesktopPlatform:eng/design_corpus.py`<br>`DesktopPlatform:eng/design_graph.py`<br>`DesktopPlatform:eng/test_design_policy.py`<br>`Contracts:eng/policy/product-names.json (GOV.14 supporting producer data only: update design.commit and the sole DesktopPlatform eng/policy/glossary-terms.json derivedDeclaration.designCommit from 7aa84e69ad6808461b34181de261fab03bede076 to ec1a1e7400683a6f971693cf84c8480183b4b6c5; retain sourceSha256 9041df86987324c25446dc3a5cfbfbabd6b6df1ea20381135a8caf84f98e44d4 and declarationSha256 bdbdfcdc7e77fec492890159747cfffe4996181090af8818322064ae897ee023 unchanged; no other policy or scanner change)`<br>`DesktopPlatform:eng/policy/naming-package.json (strictly pin the normally published immutable Contracts naming-tool candidate carrying this exact GOV.14 source-identity registration; retain package identity and exact content/source proof)`<br>`DesktopPlatform:eng/policy/dependency-policy.json (current input binding and admission of that exact existing naming-tool candidate only; no unrelated dependency change)`<br>`DesktopPlatform:eng/policy/dependency-reviews/gov-14-naming-r4.json (new immutable successor for that exact naming-tool candidate; preserve all prior receipts)` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline documentation-only checks against a pinned, clean Design commit fetched in isolation (no Design program or repository hook is run); zero findings required; PR CI. |
| Completion evidence | Zero-findings report across all six checks plus the decision-coverage check. |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: DesktopPlatform/eng/design_graph.py:graph() (read in full) already implements: cross-checking implementation-sequence.md section 9's forward-dependency table against README.md's phase tables and its 'Downstream dependency index' reverse table (all three must agree, and reverse must be the exact transpose of forward); rejecting a producer reference to an inactive/nonexistent package; requiring every active WP file to declare exactly sections 1-9 with no duplicate numbering; requiring exactly one #rule-wp-NN.90 evidence row in each WP's own section 7; requiring implementation-sequence.md to carry a 'Serial execution:...' line that is a valid topological order of every active package (every producer ordered before its consumer) plus three exact hardcoded sentences ('All N active packages...', 'Total active dependency edges: E.', 'WP42.11 precedes 42.10.'). DesktopPlatform/eng/design_policy.py:verify() (read in full) additionally pins the ENTIRE Design corpus by commit+per-file sha256 (glossary/coverage/classifications sources plus one corpusSha256 over every doc), calls corpus.audit() for citation/anchor integrity (design_corpus.py itself not read), calls graph() above, and validates a citation-classification register (docs/assurance/citation-classifications.json) so every non-linked occurrence of a standard ID-shaped token anywhere in the corpus is either a normal citation or an explicit, dated, owned exception. This already covers the acyclic-graph check and much of link/citation integrity. NOT confirmed from this reading: the specific 23+8-row decision-coverage check against traceability-matrix.md, and whether superseded-name-outside-deprecated-inputs is checked here versus by WP00.00/WP05.02's separate forbidden-term scanner. |
| Notes | Extends the corpus and decision-coverage checks after GOV.18 has migrated the retired graph validator and re-pinned the export. Reuse that migration evidence; this broader integrity task is not a prerequisite for the initial repin. Current coverage follows the effective reduced-family authority: 22 of the original 23 Phase 1 decisions, seven of the initial eight Phase 2 decisions and twelve current closure groups. Historical acceptance totals remain historical, later amendment records remain traceable, and retirement is accounted through [P2-019](../../../decisions/phase-2-specification-decisions.md#rule-p2-019). Test semantic row identity, successor and producer/consumer mappings, not count equality alone. The actual GOV.14 Design export remains pinned to ec1a1e7400683a6f971693cf84c8480183b4b6c5; this supporting scope change does not chase later Design commits. The existing 1.0.0-ci.129.1 naming candidate registers the old source identity and therefore cannot validate that export, even though the glossary source and declaration bytes are unchanged. Under the real GOV.14 claim, contribute the exact Contracts registration data change through its integration owner, independent review, retained CI and normal immutable package publication, then consume that same produced candidate in DesktopPlatform. Do not reopen completed CON.23, copy sibling sources, republish old versions, weaken exact registration, broaden exceptions or modify naming/scanner algorithms. The Contracts producer change needs only those two policy fields: existing package staging copies and verifies the policy bytes, and no access/dependency/provenance input binding changes are required. The explicit DesktopPlatform candidate upgrade is not inferred from ADP.07. |

<a id="task-gov-15"></a>

### GOV.15 — WP05 stage integration verification

**Outcome.** Each of the seven implementation repositories enforces its own boundary independently, and a cross-repository integration graph - reading each repository's published package/dependency metadata rather than cloning every reference or product repository - detects a forbidden transitive edge; both the architecture/repository-policy suite and the specification-integrity suite run in the pull-request pipeline and a violation fails the build.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/gov-15` and ledger record `ledger/tasks/gov-15.md` in the Plan repository; task branch `task/gov-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-05](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-05.90](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.90) — full |
| Provides | wp05-stage-acceptance; cross-repo-dependency-graph-check |
| Start prerequisites | **artifact** [GOV.04](#task-gov-04) — DesktopPlatform's own policy suite green. *Why:* the stage receipt joins every substep's real evidence<br>**artifact** [GOV.05](#task-gov-05) — Contracts' own policy suite green. *Why:* same<br>**artifact** [GOV.07](#task-gov-07) — ArcScope's own policy suite green. *Why:* same<br>**artifact** [GOV.09](#task-gov-09) — Cloud's own policy suite green. *Why:* same<br>**artifact** [GOV.10](#task-gov-10) — AI's own policy suite green. *Why:* same<br>**artifact** [GOV.11](#task-gov-11) — Web's own policy suite green. *Why:* same<br>**artifact** [GOV.12](#task-gov-12) — Mobile's own policy suite green. *Why:* same<br>**artifact** [GOV.13](#task-gov-13) — the invariant accounting report existing and complete. *Why:* 05.90 assembles all preceding substeps' real evidence into one receipt<br>**artifact** [GOV.14](#task-gov-14) — the specification-integrity suite green. *Why:* same |
| Entry condition | [ADOPT.02.governance](adoption.md#task-adopt-02-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `DesktopPlatform:eng/**`<br>`Design:docs/assurance/wp05-90-*.md, wp05-stage-acceptance.md/.json` |
| Shared resources | [RES-design-evidence](../shared-resources.md#res-design-evidence) (append) |
| Validation | Reads published package manifests only (no full clone of every repository); offline; PR CI. |
| Completion evidence | Stage-acceptance receipt joining all eleven preceding GOV.04-14 substeps' real results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Terminal task for WP05. WP06 and WP21 depend on this as their own external artifact prerequisite (README downstream index: 05 -> 06, 21). |

<a id="task-gov-16"></a>

### GOV.16 — Operation-catalogue authorization reachability matrix and identity boundary evidence

**Outcome.** A build-produced reachability matrix classifies every public/local/operator/CF/exception operation binding under catalogue 00 against all seven [AZ-04](../../../architecture/08-security-architecture.md#rule-az-04) authorization fields, failing on unclassified/ambiguous fields, impossible idempotency claims, public imports of local schema, and tool reachability of human-only approval/credential/commerce/policy methods, including hostile actor-chain fixtures; separately, the owner/deployment identity chain is asserted so automation loses authorization when its owner loses permission/service eligibility even with an otherwise-valid process credential, and no customer service-principal or Organization authority is introduced.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/gov-16` and ledger record `ledger/tasks/gov-16.md` in the Plan repository; task branch `task/gov-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / M |
| Obligations | [WP-05](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) Section 7 operation-by-actor [AZ-04](../../../architecture/08-security-architecture.md#rule-az-04) authorization reachability matrix (public/local/operator/CF/exception bindings, hostile actor-chain fixtures, resource/context/connector egress denials) and section 8 'Identity boundary evidence' (owner/deployment identity chain; automation loses authorization when its owner loses eligibility) - both unlabeled, no [WP-05](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05).MM anchor — package-level obligation contribution |
| Provides | authz-reachability-matrix-v1; identity-boundary-check |
| Start prerequisites | **contract** [CON.18](contracts.md#task-con-18) — generated catalogue 00 (operation-catalogue.md) [AZ-04](../../../architecture/08-security-architecture.md#rule-az-04) authorization-field descriptors. *Why:* the reachability matrix is generated FROM the catalogue's [AZ-04](../../../architecture/08-security-architecture.md#rule-az-04) fields; nothing to enumerate before WP03 generates them |
| Entry condition | [ADOPT.03.governance](adoption.md#task-adopt-03-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.11](cloud.md#task-cloud-11) — identity/workspace/device/session bindings. *Why:* operator/CF binding classification needs Cloud's actual session/identity model<br>**integration** [PLT.38](platform.md#task-plt-38) — the owner/deployment identity chain mechanism (the platform lane security foundation). *Why:* the identity-boundary check asserts against the real identity-chain implementation, not a description of it |
| Unblocks | none |
| Write scope | `Contracts:tests/AuthorizationPolicyTests/**` |
| Validation | Static/offline policy tests over each repository's DECLARED authorization metadata (generated attributes/descriptors), not live-system penetration testing, per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Reachability matrix with all seven [AZ-04](../../../architecture/08-security-architecture.md#rule-az-04) fields classified per binding, plus identity-boundary assertion results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Covers two WP05 package-level obligations that carry no [WP-05](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05).MM anchor (the section 7 paragraph before the evidence table, and the section 8 'Identity boundary evidence' paragraph); see package_obligations. Genuinely cross-repository in subject matter (Contracts defines the catalogue; Cloud/DesktopPlatform implement the actual bindings) but modeled as a Contracts-owned static check over declared metadata, consistent with [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |

<a id="task-gov-17"></a>

### GOV.17 — Retire the native families outside the product family and move the still-image shim

**Outcome.** The Media, Colour and Otio native families and the macOS Metal graphics probe leave DesktopPlatform - ABI directories, overlays, managed and runtime projects, oracle tests, solution entries and package registrations - and no further versions of them are published; the still-image shim moves to native/arcimage-abi under the logical library ArcImageNative while its published arc_image_* symbols stay unchanged; provenance records of reused files stay unchanged. Packaging guards, local opt-in consumer fixtures and examples use retained producers, preserving applicable integrity and RID checks.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/gov-17` and ledger record `ledger/tasks/gov-17.md` in the Plan repository; task branch `task/gov-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / M |
| Obligations | [P2-019](../../../decisions/phase-2-specification-decisions.md#rule-p2-019) — retirement of the accepted DesktopPlatform native families, projects, packages and tests whose only consumers left the family; the neutral identity of the still-image shim<br>[P2-020](../../../decisions/phase-2-specification-decisions.md#rule-p2-020) — source cleanup of the alignment sequence ([ADP-10](../adoption.md#rule-adp-10)); blocks only the tasks that edit the retired bindings |
| Provides | retired-native-families; still-image-shim-moved |
| Start prerequisites | none |
| Entry condition | [ADOPT.02.governance](adoption.md#task-adopt-02-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [NAT.06](native.md#task-nat-06), [NAT.11](native.md#task-nat-11), [NAT.13](native.md#task-nat-13), [NAT.14](native.md#task-nat-14), [NAT.30](native.md#task-nat-30) |
| Write scope | `DesktopPlatform:native/* (retired family directories and the moved still-image directory)`<br>`DesktopPlatform:native/CMakeLists.txt`<br>`DesktopPlatform:src/Native/* (retired family projects and the still-image logical library name)`<br>`DesktopPlatform:tests/NativeAbiTests/**`<br>`DesktopPlatform:win.slnx`<br>`DesktopPlatform:DesktopPlatform.slnx (retired native project entries only)`<br>`DesktopPlatform:eng/packaging/packages.json`<br>`DesktopPlatform:docs/native-reconciliation.md`<br>`DesktopPlatform:README.md`<br>`DesktopPlatform:docs/native-package-release.md`<br>`DesktopPlatform:src/BuildingBlocks/ArcForges.NativeInterop/README.md`<br>`DesktopPlatform:tests/ArchitectureTests/** (retired native library map)`<br>`DesktopPlatform:eng/packaging/test_packages.py`<br>`DesktopPlatform:eng/packaging/native_consumer.py`<br>`DesktopPlatform:eng/packaging/README.md`<br>`DesktopPlatform:.github/workflows/native-abi.yml (retired owned-family build inputs only; retain dependencies of retained image/PDF/instrument families)`<br>`DesktopPlatform:CMakePresets.json (retired build targets only)`<br>`DesktopPlatform:deploy/README.md (current retained-family build/install inventory)`<br>`DesktopPlatform:eng/packaging/native.py`<br>`DesktopPlatform:eng/native/vcpkg/ports/opentimelineio/** (retired overlay only)`<br>`DesktopPlatform:eng/native_provenance.py`<br>`DesktopPlatform:tests/tooling/test_native_provenance.py`<br>`DesktopPlatform:eng/provenance/files.json`<br>`DesktopPlatform:eng/provenance/NOTICE.txt`<br>`DesktopPlatform:eng/provenance/artifact-profiles/native-win-x64-r4.json (new immutable successor)`<br>`DesktopPlatform:eng/provenance/records/native-*-r4.json (new immutable successors; preserve historical records)`<br>`DesktopPlatform:eng/check_provenance.py (validate explicit retirement of previously registered artifact targets only)`<br>`DesktopPlatform:tests/tooling/test_provenance.py (retirement rejection fixtures)`<br>`DesktopPlatform:eng/provenance/retired-artifacts.json (exact former project/package/kind targets with retirement authority; reject active or unregistered targets)`<br>`DesktopPlatform:eng/provenance/records/contracts-provenance-tools-r2.json (new immutable tool successor; preserve previous record)`<br>`DesktopPlatform:CMakeLists.txt (reject retired native build profiles)`<br>`DesktopPlatform:docs/provenance.md (current retained native profile inventory; preserve historical evidence)` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append), [RES-desktopplatform-native-build](../shared-resources.md#res-desktopplatform-native-build) (append), [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append), [RES-workstation-build-slot](../shared-resources.md#res-workstation-build-slot) (exclusive), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append) |
| Validation | offline: native CMake/solution/package-inventory consistency, retained packaging guard tests and a scan for active retired-family bindings outside provenance history. Retain necessary Windows native compilation and packaging checks; run affected consumer behavior locally only when the existing environment supports it and the change requires it ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)), never as CI. Acceptance: source, solution, packaging, tests and current documentation contain only retained families, guards no longer select Media packages, and still-image consumers resolve ArcImageNative. |
| Completion evidence | Retirement diff; native build and package-consumer results for the retained families; the moved still-image shim with unchanged exported symbols. |
| Baseline (unreviewed unless accepted) | not-started Observed in the accepted WP00-WP02 implementation: the media, colour, OTIO and still-image shim directories, the Metal graphics probe source, and their managed/runtime projects and 1.0.0-ci.17.1 packages. |
| Notes | Independent of the retained native families; NAT.11 starts on the moved still-image directory and NAT.30 verifies the retained producer set. GOV.18 carries the policy-data half, so neither waits on the other. |

<a id="task-gov-18"></a>

### GOV.18 — Reduce the DesktopPlatform policy data and re-pin the design-policy export

**Outcome.** Runtime-ownership, licence-boundary and reconciliation policy data drop the retired repositories and families. In the same reviewed change, the retired serial-graph validator and exporter migrate to the delivery graph, including graph-derived active invariant owners, before the design-policy export is re-pinned to this Design repository and glossary-terms.json and invariants.json are regenerated. Provenance records of reused files stay unchanged.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/gov-18` and ledger record `ledger/tasks/gov-18.md` in the Plan repository; task branch `task/gov-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | governance / M |
| Obligations | [P2-019](../../../decisions/phase-2-specification-decisions.md#rule-p2-019) — retirement of the accepted DesktopPlatform policy data that names repositories or families outside the family; the design-policy export re-pinned to this Design repository<br>[P2-020](../../../decisions/phase-2-specification-decisions.md#rule-p2-020) — source cleanup of the alignment sequence ([ADP-10](../adoption.md#rule-adp-10)); blocks only the tasks that edit the retired bindings<br>[P2-018](../../../decisions/phase-2-specification-decisions.md#rule-p2-018) — delivery-graph validation replacing the retired package-level graph check |
| Provides | design-policy-export-repinned |
| Start prerequisites | **artifact** [CON.23](contracts.md#task-con-23) — Published canonical naming data/scanner build-time candidate. *Why:* The policy repin validates new exports through the canonical scanner rather than old Contracts source or duplicated naming authority. |
| Entry condition | [ADOPT.02.governance](adoption.md#task-adopt-02-governance) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CON.23](contracts.md#task-con-23), [GOV.04](#task-gov-04), [GOV.13](#task-gov-13), [GOV.14](#task-gov-14) |
| Write scope | `DesktopPlatform:eng/policy/**`<br>`DesktopPlatform:docs/design-policy.md`<br>`DesktopPlatform:eng/runtime_ownership.py`<br>`DesktopPlatform:eng/licence_boundary.py`<br>`DesktopPlatform:eng/reference_baselines.py`<br>`DesktopPlatform:eng/reconciliation.py`<br>`DesktopPlatform:eng/test_runtime_ownership.py`<br>`DesktopPlatform:eng/test_licence_boundary.py`<br>`DesktopPlatform:eng/test_design_policy.py`<br>`DesktopPlatform:tests/ArchitectureTests/** (retired repository owners)`<br>`DesktopPlatform:eng/design_graph.py`<br>`DesktopPlatform:eng/design_policy.py`<br>`DesktopPlatform:eng/provenance/** (new same-owner tool reuse receipt and source inventory only; existing reused-file provenance remains unchanged)`<br>`DesktopPlatform:NOTICE.md (generated provenance notice only)`<br>`DesktopPlatform:eng/test_reference_baselines.py`<br>`DesktopPlatform:eng/test_reconciliation.py`<br>`DesktopPlatform:AGENTS.md`<br>`DesktopPlatform:docs/runtime-ownership.md`<br>`DesktopPlatform:docs/licence-boundary.md`<br>`DesktopPlatform:docs/reference-baselines.md`<br>`DesktopPlatform:docs/reconciliation-inventory.md`<br>`DesktopPlatform:Directory.Packages.props (exact canonical naming-tool package pin)`<br>`DesktopPlatform:eng/policy/dependency-policy.json (canonical naming-tool admission)`<br>`DesktopPlatform:eng/policy/dependency-reviews/** (new immutable naming-tool admission receipt)`<br>`DesktopPlatform:eng/provenance/** (owned naming-tool inventory and new receipts; preserve historical records)` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | offline: delivery-graph and exporter tests, including invalid prerequisite/obligation/active-owner rejection fixtures; architecture and runtime-ownership tests; fresh exporter comparison against the reviewed repinned Design commit; no live retired bindings outside provenance. Acceptance: the graph-validator migration and repin pass together without waiting for GOV.14, policy tools name only the retained repositories and references, and the design-policy check passes against the new pin. |
| Completion evidence | Reviewed graph-validator/exporter migration and negative-fixture results; repinned Design commit and policy-source identities; exporter comparison and policy-test results. |
| Baseline (unreviewed unless accepted) | not-started Observed in the accepted WP00-WP02 implementation: policy data and the design-policy export pinned to the derivation-baseline Design commit. |
| Notes | Performs the narrow checker migration needed to repin within this cleanup task. GOV.13 and GOV.14 consume the resulting export; GOV.14 retains the broader specification-integrity audit. CON.23 completes after its forbidden-alias declaration is re-exported. |
