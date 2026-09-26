<a id="rule-wp-05"></a>

# WP-05 — Architecture and Repository Policy Test Suite

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Turn the architecture into build failures. Every structural rule that a reviewer would otherwise have to remember becomes a test, so that a violation is caught at the moment it is introduced rather than at a release gate months later.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Each repository; shared tooling in Platform/Contracts. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Extending the existing `ArchitectureTests` suite to the full [AT-01](../../architecture/01-solution-and-project-layout.md#rule-at-01)–[AT-14](../../architecture/01-solution-and-project-layout.md#rule-at-14) set, extending its `RepositoryPolicyTests.cs` to [RP-01](../../architecture/01-solution-and-project-layout.md#rule-rp-01)–[RP-10](../../architecture/01-solution-and-project-layout.md#rule-rp-10), the forbidden-term scan, the invariant **enforcement accounting** report, and the documentation integrity checks over this design repository.

**Out of scope.** Behavioural tests of any kind. Performance gates (`06` and each product package). The policy *data* these tests read, which `00` and `02` produce. **The invariant-to-architecture mapping**, which is completed design evidence ([PG-06](../../assurance/open-gates-register.md#rule-pg-06) closed). **Implementing every invariant's check**, which is distributed across owning packages under [PG-11](../../assurance/open-gates-register.md#rule-pg-11).

**Why this package exists.** Without it, every rule in the architecture layer is advice. With it, the rules are the build.

**Current reconciliation scope.** The earlier monorepo architecture-test inventory is historical evidence, not a current working harness. At the pinned repository baseline, retain useful surviving tests and implement the complete rule manifest in the owning repository; archived line/test counts cannot satisfy this package. Validate both allowed dependencies and deliberate negative fixtures against the actual multi-repository package graph.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) `§7` | The `AT-*` and `RP-*` rule sets to implement |
| [`../../architecture/00-architecture-overview.md`](../../architecture/00-architecture-overview.md) | Layering rules [LY-01](../../architecture/00-architecture-overview.md#rule-ly-01)–[LY-09](../../architecture/00-architecture-overview.md#rule-ly-09) |
| [`../../assurance/testing-and-verification-strategy.md`](../../assurance/testing-and-verification-strategy.md) `§4`, `§7` | The invariant-to-test obligation and the specification integrity checks |
| [WP-00](00-specification-naming-and-rights-freeze.md#rule-wp-00) output | Forbidden-term lists and the exported glossary policy data |
| [`../../assurance/invariant-coverage.md`](../../assurance/invariant-coverage.md) | **The completed item-level invariant mapping** — a versioned input, not work to be done |
| [Current test-family map](../../assurance/wp01-04-test-family-map.md) and [historical reconciliation](../../assurance/implementation-state-reconciliation.md) `§5.4` | Current exact-head suites and gaps; historical harness counts remain reference evidence only |
| [WP-02](02-build-governance-and-analyzer-policy.md#rule-wp-02) output | A build that can fail; the dependency policy data |
| [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) output | Contract projects and their licence declarations |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) as amended by [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **A structural rule is tested, not reviewed** ([TS-04](../../assurance/testing-and-verification-strategy.md#rule-ts-04) in the testing strategy). |
| <a id="rule-br-02"></a>BR-02 | **A policy test failure is a build failure**, never a warning. |
| <a id="rule-br-03"></a>BR-03 | **Design-stage traceability is complete and is an input, not an output** (**[D-018](../../decisions/phase-1-foundation-decisions.md#rule-d-018)** obligation B; [PG-06](../../assurance/open-gates-register.md#rule-pg-06) closed). This package builds enforcement, and reports on it — it does not re-derive the mapping. |
| <a id="rule-br-04"></a>BR-04 | **The forbidden-term scan covers source, identifiers, resource strings and implementation documentation**, excluding preserved historical inputs. |
| <a id="rule-br-05"></a>BR-05 | **A test that enforces an invariant names it**, so a failure identifies the violated rule ([IV-04](../../assurance/testing-and-verification-strategy.md#rule-iv-04) there). |
| <a id="rule-br-06"></a>BR-06 | **An exception to a policy test is data, owned and expiring** — never a code comment that disables the check. |
| <a id="rule-br-07"></a>BR-07 | **Policy tests run in pull-request builds** ([CI-01](../../architecture/14-build-packaging-and-release.md#rule-ci-01) in the build architecture), so a violation never reaches the main branch. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `tests/ArchitectureTests/` | **Current DesktopPlatform project exists** — the WP01.04 baseline has five bounded repository-policy methods. Extend to the full [AT-01](../../architecture/01-solution-and-project-layout.md#rule-at-01)–[AT-14](../../architecture/01-solution-and-project-layout.md#rule-at-14) set |
| `tests/ArchitectureTests/RepositoryPolicyTests.cs` | **Current file exists** — five methods at the WP01.04 baseline, not the historical nineteen. Extend to [RP-01](../../architecture/01-solution-and-project-layout.md#rule-rp-01)–[RP-10](../../architecture/01-solution-and-project-layout.md#rule-rp-10). Whether it becomes a separate project is a packaging choice, not a gap |
| `tests/ArchitectureTests/FixtureCompiler.cs`, `ProjectGraph.cs` | Historical files are absent from the current suite. Retain current owner-local negative fixtures and introduce the graph/fixture mechanism needed to enforce the complete rules; do not assume the old harness is present |
| DesktopPlatform `eng/design_policy.py`, `eng/design_corpus.py`, `eng/design_graph.py` and `eng/test_design_policy.py` | Existing link, identifier, glossary and graph tooling; extend missing specification checks and negative fixtures. A separate test project is optional, not a coverage requirement |
| `eng/policy/exceptions.json` | Created: the owned, expiring exception set |
| CI pull-request pipeline | Existing owner-local policy and Design checks remain required; add the remaining AT/RP and accounting gates |

**Major types introduced:** test infrastructure only.

---

## 5. Required implementation work

<a id="rule-wp-05.00"></a>

### WP-05.00 — Layering and reference direction

**What must be fully done.** Tests asserting: domain projects reference no infrastructure; application projects reference no UI; building blocks reference no product; no product references another product's internals; contract projects reference only contract projects and the foundation; the shared foundation contains no product knowledge; and no project reachable from an AOT deliverable references a fenced project.

**Testing requirements.** Each rule has a positive fixture and a negative fixture that must fail.

**Completion gate.** Every layering rule has a passing positive case and a failing negative case.

<a id="rule-wp-05.01"></a>

### WP-05.01 — Licence boundary enforcement

**What must be fully done.** Tests asserting: every project declares an SPDX identifier and a boundary; no Apache-boundary project references an AGPL project directly or transitively; the Apache set matches the enumerated list; and every dependency's licence is on the allowlist for its consuming boundary.

**Testing requirements.** A negative fixture introducing a cross-boundary reference must fail the build.

**Completion gate.** All four assertions pass, and the negative fixture fails as designed.

<a id="rule-wp-05.02"></a>

### WP-05.02 — Forbidden terms and naming

**What must be fully done.** The scan covers superseded product names, the superseded payment provider, forbidden aliases from the glossary, and obsolete architectural terms. Coverage includes type and member names, namespaces, resource strings, and implementation documentation. The deprecated input archive at `docs/deprecated-inputs/` in this design repository is excluded.

**Testing requirements.** A negative fixture containing each forbidden term must be detected; the scan must produce zero findings on the current tree.

**Completion gate.** Zero findings, and every forbidden term is detectable.

<a id="rule-wp-05.03"></a>

### WP-05.03 — Contract and serialization policy

**What must be fully done.** Tests asserting: every public business DTO is generated from proto and HTTP exceptions have explicit JSON metadata; no reflection-based serializer is reachable; every local RPC contract interface carries the generated service/descriptor identity (**[V-05b](../../assurance/phase-1-official-verification.md#rule-v-05b)**); unregistered dynamic/reflection serializer paths are absent; and every contract project's generated artifacts match the committed baseline.

**Testing requirements.** Negative fixtures for each assertion.

**Completion gate.** All assertions pass with negative fixtures failing. **This makes [VG-04](../../assurance/open-gates-register.md#rule-vg-04)'s policy-test half enforceable.**

<a id="rule-wp-05.04"></a>

### WP-05.04 — Banned APIs and patterns

**What must be fully done.** A banned-symbol list covering: reflection entry points on AOT paths, dynamic code generation, blocking waits on async paths, direct provider SDK calls outside adapters, direct logging of secret-bearing or content types, floating-point arithmetic in money and credit paths, and raw pointer fields where a safe handle is required.

**Testing requirements.** A negative fixture per banned category.

**Completion gate.** Every banned category is detected.

<a id="rule-wp-05.05"></a>

### WP-05.05 — Invariant enforcement accounting

> **Design-stage traceability already complete.** [`../../assurance/invariant-coverage.md`](../../assurance/invariant-coverage.md) `§7` maps all **429** catalogued invariants to an architecture home, a mechanism, a planned verification and an owning gate. **[PG-06](../../assurance/open-gates-register.md#rule-pg-06) is closed.** This sub-step does **not** re-derive that mapping and cannot re-close that gate.

**What must be fully done.** A build-produced **accounting report** stating, for every invariant, whether an **implemented** check exists and whether it **passes**. The report is a status instrument. It classifies each invariant as: enforced and passing · enforced and failing · not yet implemented.

**Testing requirements.** The report is asserted for completeness — every one of the **429** invariants appears with exactly one classification, and every classification is derived from an actual test-run result rather than declared.

**Completion gate for this sub-step.** The accounting report exists, covers all **429** invariants, and derives every classification from a real result.

> **What this gate explicitly does not do.**
>
> | It does not | Because |
> |---|---|
> | Close [PG-06](../../assurance/open-gates-register.md#rule-pg-06) | Already closed by design evidence; a weaker later check cannot re-close a satisfied gate |
> | Close [PG-11](../../assurance/open-gates-register.md#rule-pg-11) | [PG-11](../../assurance/open-gates-register.md#rule-pg-11) requires every invariant **enforced and passing**. A report that faithfully records 300 unimplemented invariants is a *complete report* and a *failing* [PG-11](../../assurance/open-gates-register.md#rule-pg-11) |
> | Let an owned open finding substitute for enforcement | Registering a finding records who owes the work. It does not do the work. [PG-11](../../assurance/open-gates-register.md#rule-pg-11) counts implementations, not findings |
>
> **Accounting and enforcement are separate obligations with separate gates.** This sub-step owns the accounting. [PG-11](../../assurance/open-gates-register.md#rule-pg-11) is discharged per invariant by its owning package, at that package's completion gate, with a passing result.

<a id="rule-wp-05.06"></a>

### WP-05.06 — Specification integrity

**Decision coverage check.** Verify 23 Phase 1 and eight Phase 2 decision rows against the [traceability matrix](../../assurance/traceability-matrix.md#11-phase-2-decisions), including the withdrawn ordering's effective successor and all fourteen closure groups. A valid anchor at the wrong decision is a semantic failure, not a pass.


**What must be fully done.** Checks over the current documentation and archive README in this design repository: every internal link resolves; every cited requirement, architecture rule, decision, verification finding and gate identifier exists; no superseded name appears as current outside `docs/deprecated-inputs/`; every Phase 1 decision is cited by at least one Phase 2 document or its non-applicability is stated; and the work-package dependency graph is acyclic with every referenced package existing. The four deprecated input bodies are excluded; their historical citations do not require a new input review or commitment mapping.

**Testing requirements.** The checks run against the current design repository and produce zero findings. Enforce [SV-09](../../assurance/testing-and-verification-strategy.md#rule-sv-09) over all current specification and planning files, including required-input tables and authority headers. Negative fixtures for an archived source shorthand, old Stage citation and archive-body path must fail; a valid current-rule reference must pass. Historical records and archive navigation remain distinguishable from active implementation inputs.

**Completion gate.** Zero findings across all six checks.

---

### Web repository and architecture assertions

Add Node/TS import and dependency checks to the existing policy suite: one Web workspace/lock; exact Node/npm/generator pins; SDK-to-UI licence separation; generated wire types; no private/server/local-RPC imports; desktop JS/DOM prohibition scoped to desktop graphs; no obsolete Blazor target in the active Web graph; no esproj in portable managed references; no implicit npm install or production dev/HMR server. TS fixtures and test helpers cannot enter a release route graph. Exercise negative examples and verify the policy fails for each prohibited dependency/route.

---

<a id="rule-wp-05.90"></a>
### WP-05.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Implement intra-repository rules and package/licence closure tests. Enforce no cross-repository project/source dependency, no Mobile import of AGPL implementation, no desktop native/UI assets in Cloud and one Harness owner.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Each repository can enforce its boundary independently; the integration graph detects a forbidden transitive edge without cloning every reference or product repository.

**Completion gate.** Each repository can enforce its boundary independently; the integration graph detects a forbidden transitive edge without cloning every reference or product repository. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None |
| Protocol | Contract policy becomes enforced rather than documented |
| UI | Naming and resource-string policy becomes enforced |
| Security | Licence boundary and banned-API enforcement are security controls |
| Platform | AOT-path banned APIs are caught before an AOT publish fails obscurely |
| Migration | None |
| Compatibility | The contract baseline gate becomes a test rather than a convention |

---

## 7. Tests and verification evidence

Generate an operation-by-actor reachability matrix for every public/local/operator/CF/exception binding under catalogue 00 [AZ-04](../../architecture/contracts/00-operation-catalogue.md#rule-az-04), with all seven effective authorization fields and source profile. Fail unclassified/ambiguous fields, nonexistent idempotency examples, public imports of local schema and tool reachability of human-only approval/credential/commerce/policy methods. Include resource/context/connector egress denials and hostile actor-chain cases.

| Evidence | Produced by |
|---|---|
| Layering test results with negative fixtures | [WP-05.00](#rule-wp-05.00) |
| Licence boundary report | [WP-05.01](#rule-wp-05.01) |
| Forbidden-term scan, zero findings | [WP-05.02](#rule-wp-05.02) |
| Contract and serialization policy results | [WP-05.03](#rule-wp-05.03) |
| Banned-symbol detection results | [WP-05.04](#rule-wp-05.04) |
| Invariant enforcement accounting report, **429 of 429** classified from real results | [WP-05.05](#rule-wp-05.05) |
| Specification integrity report, zero findings | [WP-05.06](#rule-wp-05.06) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-05.90](#rule-wp-05.90) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-05.90](#rule-wp-05.90) and all inherited domain-specific gates must pass on the same candidate closure. Each repository can enforce its boundary independently; the integration graph detects a forbidden transitive edge without cloning every reference or product repository.

**Identity boundary evidence.** Apply the [owner/deployment identity chain](../../architecture/08-security-architecture.md#1-identity-layering). Automation loses authorization when its owner loses permission/service eligibility even with a valid process credential; no customer service-principal or Organization authority is introduced.

**All of the following, with recorded evidence:**

1. Every layering, reference-direction and licence rule has a passing positive case and a failing negative case.
2. The forbidden-term scan produces zero findings and detects every listed term.
3. Contract, serialization and RPC-attribute policy is enforced with negative fixtures failing.
4. Every banned API category is detected.
5. The invariant enforcement accounting report covers all **429** invariants with every classification derived from a real result. **[PG-06](../../assurance/open-gates-register.md#rule-pg-06) was closed by design evidence before this package; [PG-11](../../assurance/open-gates-register.md#rule-pg-11) remains open until every invariant is enforced and passing in its owning package.**
6. Specification integrity checks produce zero findings.
7. Both suites run in the pull-request pipeline and a violation fails the build.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [GOV.04](../delivery/lanes/governance.md#task-gov-04) | [WP-05.00](05-architecture-and-repository-policy-tests.md#rule-wp-05.00) (build the reusable [AT-01](../../architecture/01-solution-and-project-layout.md#rule-at-01)..14/[RP-01](../../architecture/01-solution-and-project-layout.md#rule-rp-01)..10 rule engine and project-graph reader; apply it to DesktopPlatform's own layering/reference-direction rules)<br>[WP-05.01](05-architecture-and-repository-policy-tests.md#rule-wp-05.01) (licence-boundary rule implementation in the shared engine; DesktopPlatform's own licence-boundary enforcement)<br>[WP-05.04](05-architecture-and-repository-policy-tests.md#rule-wp-05.04) (banned-symbol scanner mechanism in the shared engine; DesktopPlatform's own banned-API fixtures)<br>[WP-05.02](05-architecture-and-repository-policy-tests.md#rule-wp-05.02) (wire the existing WP00.00 forbidden-term scanner into DesktopPlatform's own PR build as a failing policy test) | [GOV.03](../delivery/lanes/governance.md#task-gov-03) (artifact), [GOV.01](../delivery/lanes/governance.md#task-gov-01) (artifact) |
| [GOV.05](../delivery/lanes/governance.md#task-gov-05) | [WP-05.03](05-architecture-and-repository-policy-tests.md#rule-wp-05.03) (full: build the contract/serialization policy engine (generated-from-proto DTO check, explicit JSON metadata for HTTP exceptions, no reflection-based serializer reachable, every local RPC contract interface carries the generated service/descriptor identity, generated artifacts match the committed baseline) and apply it to Contracts itself)<br>[WP-05.00](05-architecture-and-repository-policy-tests.md#rule-wp-05.00) (Contracts layering: contract projects reference only contract projects and the foundation)<br>[WP-05.01](05-architecture-and-repository-policy-tests.md#rule-wp-05.01) (Contracts licence-boundary enforcement (public/internal Apache-2.0 split from WP01.01))<br>[WP-05.02](05-architecture-and-repository-policy-tests.md#rule-wp-05.02) (wire the forbidden-term scanner into Contracts' own PR build as a failing policy test)<br>[WP-05.04](05-architecture-and-repository-policy-tests.md#rule-wp-05.04) (Contracts banned-API fixtures) | [CON.90](../delivery/lanes/contracts.md#task-con-90) (contract) |
| [GOV.06](../delivery/lanes/governance.md#task-gov-06) | [WP-05.00](05-architecture-and-repository-policy-tests.md#rule-wp-05.00) (ArcNotes slice: layering/reference-direction fixtures)<br>[WP-05.01](05-architecture-and-repository-policy-tests.md#rule-wp-05.01) (ArcNotes slice: licence boundary + dependency allowlist)<br>[WP-05.02](05-architecture-and-repository-policy-tests.md#rule-wp-05.02) (wire the forbidden-term scanner into ArcNotes' own PR build)<br>[WP-05.03](05-architecture-and-repository-policy-tests.md#rule-wp-05.03) (ArcNotes' generated-client consumption checks (RPC interface carries generated descriptor identity))<br>[WP-05.04](05-architecture-and-repository-policy-tests.md#rule-wp-05.04) (ArcNotes banned-API fixtures) | none |
| [GOV.07](../delivery/lanes/governance.md#task-gov-07) | [WP-05.00](05-architecture-and-repository-policy-tests.md#rule-wp-05.00) (ArcScope slice)<br>[WP-05.01](05-architecture-and-repository-policy-tests.md#rule-wp-05.01) (ArcScope slice)<br>[WP-05.02](05-architecture-and-repository-policy-tests.md#rule-wp-05.02) (wire the forbidden-term scanner into ArcScope's own PR build)<br>[WP-05.03](05-architecture-and-repository-policy-tests.md#rule-wp-05.03) (ArcScope's generated-client consumption checks)<br>[WP-05.04](05-architecture-and-repository-policy-tests.md#rule-wp-05.04) (ArcScope banned-API fixtures) | none |
| [GOV.08](../delivery/lanes/governance.md#task-gov-08) | [WP-05.00](05-architecture-and-repository-policy-tests.md#rule-wp-05.00) (ArcSlate slice)<br>[WP-05.01](05-architecture-and-repository-policy-tests.md#rule-wp-05.01) (ArcSlate slice)<br>[WP-05.02](05-architecture-and-repository-policy-tests.md#rule-wp-05.02) (wire the forbidden-term scanner into ArcSlate's own PR build)<br>[WP-05.03](05-architecture-and-repository-policy-tests.md#rule-wp-05.03) (ArcSlate's generated-client consumption checks)<br>[WP-05.04](05-architecture-and-repository-policy-tests.md#rule-wp-05.04) (ArcSlate banned-API fixtures) | none |
| [GOV.09](../delivery/lanes/governance.md#task-gov-09) | [WP-05.00](05-architecture-and-repository-policy-tests.md#rule-wp-05.00) (Cloud slice)<br>[WP-05.01](05-architecture-and-repository-policy-tests.md#rule-wp-05.01) (Cloud slice)<br>[WP-05.02](05-architecture-and-repository-policy-tests.md#rule-wp-05.02) (wire the forbidden-term scanner into Cloud's own PR build)<br>[WP-05.03](05-architecture-and-repository-policy-tests.md#rule-wp-05.03) (Cloud's own generated public API/RPC descriptor checks)<br>[WP-05.04](05-architecture-and-repository-policy-tests.md#rule-wp-05.04) (Cloud banned-API fixtures, weighted toward AOT-path reflection/dynamic-codegen since Cloud is the Native AOT host) | none |
| [GOV.10](../delivery/lanes/governance.md#task-gov-10) | [WP-05.00](05-architecture-and-repository-policy-tests.md#rule-wp-05.00) (AI slice)<br>[WP-05.01](05-architecture-and-repository-policy-tests.md#rule-wp-05.01) (AI slice)<br>[WP-05.02](05-architecture-and-repository-policy-tests.md#rule-wp-05.02) (wire the forbidden-term scanner into AI's own PR build)<br>[WP-05.03](05-architecture-and-repository-policy-tests.md#rule-wp-05.03) (AI's generated-client consumption checks)<br>[WP-05.04](05-architecture-and-repository-policy-tests.md#rule-wp-05.04) (AI banned-API fixtures) | none |
| [GOV.11](../delivery/lanes/governance.md#task-gov-11) | [WP-05.01](05-architecture-and-repository-policy-tests.md#rule-wp-05.01) (Web slice: SDK-to-UI licence separation)<br>[WP-05.02](05-architecture-and-repository-policy-tests.md#rule-wp-05.02) (wire the forbidden-term scanner into Web's own PR build)<br>[WP-05.04](05-architecture-and-repository-policy-tests.md#rule-wp-05.04) (Web banned dependency/route fixtures)<br>[WP-05](05-architecture-and-repository-policy-tests.md#rule-wp-05) Web repository and architecture assertions (unlabeled paragraph after [WP-05.06](05-architecture-and-repository-policy-tests.md#rule-wp-05.06)): Node/TS import and dependency checks - one Web workspace/lock, exact Node/npm/generator pins, SDK-to-UI licence separation, generated wire types only, no private/server/local-RPC imports, desktop JS/DOM prohibition scoped to desktop graphs, no obsolete Blazor target, no esproj in portable managed references, no implicit npm install or production dev/HMR server, no TS fixtures/test helpers in the release route graph (package-level obligation contribution) | [GOV.03](../delivery/lanes/governance.md#task-gov-03) (artifact), [GOV.01](../delivery/lanes/governance.md#task-gov-01) (artifact) |
| [GOV.12](../delivery/lanes/governance.md#task-gov-12) | [WP-05.00](05-architecture-and-repository-policy-tests.md#rule-wp-05.00) (Mobile slice, via Gradle dependency-graph verification rather than the.NET engine)<br>[WP-05.01](05-architecture-and-repository-policy-tests.md#rule-wp-05.01) (Mobile slice: licence boundary + dependency allowlist over Gradle dependencies)<br>[WP-05.02](05-architecture-and-repository-policy-tests.md#rule-wp-05.02) (wire the forbidden-term scanner into Mobile's own PR build)<br>[WP-05.04](05-architecture-and-repository-policy-tests.md#rule-wp-05.04) (Mobile banned-API fixtures) | [GOV.03](../delivery/lanes/governance.md#task-gov-03) (artifact) |
| [GOV.13](../delivery/lanes/governance.md#task-gov-13) | [WP-05.05](05-architecture-and-repository-policy-tests.md#rule-wp-05.05) (full) | none |
| [GOV.14](../delivery/lanes/governance.md#task-gov-14) | [WP-05.06](05-architecture-and-repository-policy-tests.md#rule-wp-05.06) (full: six checks over docs/ in ArcForges-Design, plus the 23+8-row Phase-1/Phase-2 decision-coverage check against traceability-matrix.md) | [GOV.01](../delivery/lanes/governance.md#task-gov-01) (artifact) |
| [GOV.15](../delivery/lanes/governance.md#task-gov-15) | [WP-05.90](05-architecture-and-repository-policy-tests.md#rule-wp-05.90) (full) | none |
| [GOV.16](../delivery/lanes/governance.md#task-gov-16) | [WP-05](05-architecture-and-repository-policy-tests.md#rule-wp-05) Section 7 operation-by-actor [AZ-04](../../architecture/08-security-architecture.md#rule-az-04) authorization reachability matrix (public/local/operator/CF/exception bindings, hostile actor-chain fixtures, resource/context/connector egress denials) and section 8 'Identity boundary evidence' (owner/deployment identity chain; automation loses authorization when its owner loses eligibility) - both unlabeled, no [WP-05](05-architecture-and-repository-policy-tests.md#rule-wp-05).MM anchor (package-level obligation contribution) | [CON.18](../delivery/lanes/contracts.md#task-con-18) (contract) |

**Consumers outside this package:** none.

<!-- delivery-graph:end -->

## Current source baseline and migration input

The 166-project ede43db monorepo inventory is historical disposition evidence, not the current checkout shape. [Family completion review](../../assurance/family-design-completion-review.md) records the separate DesktopPlatform/Contracts/Mobile bootstrap evidence and scope. Before coding, verify each actual source HEAD/dirty state and map only retained required mechanisms to its owning repository/package; preserve existing published Hello/probe compatibility and Mobile app/signing/version identity. Do not recreate deleted scaffolds, copy every legacy project, or treat unpublished implementation as missing design. Generated protocol artifacts follow the tracked authored-schema/generator baseline and immutable producer manifest from WP03; generated outputs are not categorically forbidden from version control.
