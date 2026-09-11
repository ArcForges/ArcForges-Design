<a id="rule-wp-05"></a>

# WP-05 — Architecture and Repository Policy Test Suite

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `02`, `03` · Downstream: `06`, `21`

> **Goal.** Turn the architecture into build failures. Every structural rule that a reviewer would otherwise have to remember becomes a test, so that a violation is caught at the moment it is introduced rather than at a release gate months later.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Each repository; shared tooling in Platform/Contracts. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Extending the existing `ArchitectureTests` suite to the full [AT-01](../../architecture/01-solution-and-project-layout.md#rule-at-01)–[AT-14](../../architecture/01-solution-and-project-layout.md#rule-at-14) set, extending its `RepositoryPolicyTests.cs` to [RP-01](../../architecture/01-solution-and-project-layout.md#rule-rp-01)–[RP-10](../../architecture/01-solution-and-project-layout.md#rule-rp-10), the forbidden-term scan, the invariant **enforcement accounting** report, and the documentation integrity checks over this design repository.

**Out of scope.** Behavioural tests of any kind. Performance gates (`06` and each product package). The policy *data* these tests read, which `00` and `02` produce. **The invariant-to-architecture mapping**, which is completed design evidence ([PG-06](../../assurance/open-gates-register.md#rule-pg-06) closed). **Implementing every invariant's check**, which is distributed across owning packages under [PG-11](../../assurance/open-gates-register.md#rule-pg-11).

**Why this package exists.** Without it, every rule in the architecture layer is advice. With it, the rules are the build.

**Its scope is smaller than first planned.** The reconciliation evidence (`§5.4`) found the harness already exists: `tests/ArchitectureTests` holds **2,075 lines**, 28 test methods in `ArchitectureRuleTests.cs` and 19 in `RepositoryPolicyTests.cs`, a real project-graph loader and a negative-fixture compiler. The file header names *thirteen* rules against the accepted twenty-four. **This package reconciles rule-by-rule against a working harness; it does not build one.**

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) `§8` | The `AT-*` and `RP-*` rule sets to implement |
| [`../../architecture/00-architecture-overview.md`](../../architecture/00-architecture-overview.md) | Layering rules [LY-01](../../architecture/00-architecture-overview.md#rule-ly-01)–[LY-09](../../architecture/00-architecture-overview.md#rule-ly-09) |
| [`../../assurance/testing-and-verification-strategy.md`](../../assurance/testing-and-verification-strategy.md) `§4`, `§7` | The invariant-to-test obligation and the specification integrity checks |
| [WP-00](00-specification-naming-and-rights-freeze.md#rule-wp-00) output | Forbidden-term lists and the exported glossary policy data |
| [`../../assurance/invariant-coverage.md`](../../assurance/invariant-coverage.md) | **The completed item-level invariant mapping** — a versioned input, not work to be done |
| [`../../assurance/implementation-state-reconciliation.md`](../../assurance/implementation-state-reconciliation.md) `§5.4` | The measured state of the existing test harness this package extends |
| [WP-02](02-build-governance-and-analyzer-policy.md#rule-wp-02) output | A build that can fail; the dependency policy data |
| [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03) output | Contract projects and their licence declarations |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **A structural rule is tested, not reviewed** ([TS-04](../../assurance/testing-and-verification-strategy.md#rule-ts-04) in the testing strategy). |
| BR-02 | **A policy test failure is a build failure**, never a warning. |
| BR-03 | **Design-stage traceability is complete and is an input, not an output** (**[D-018](../../decisions/phase-1-foundation-decisions.md#rule-d-018)** obligation B; [PG-06](../../assurance/open-gates-register.md#rule-pg-06) closed). This package builds enforcement, and reports on it — it does not re-derive the mapping. |
| BR-04 | **The forbidden-term scan covers source, identifiers, resource strings and implementation documentation**, excluding preserved historical inputs. |
| BR-05 | **A test that enforces an invariant names it**, so a failure identifies the violated rule ([IV-04](../../assurance/testing-and-verification-strategy.md#rule-iv-04) there). |
| BR-06 | **An exception to a policy test is data, owned and expiring** — never a code comment that disables the check. |
| BR-07 | **Policy tests run in pull-request builds** ([CI-01](../../architecture/14-build-packaging-and-release.md#rule-ci-01) in the build architecture), so a violation never reaches the main branch. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `tests/ArchitectureTests/` | **Exists** — 2,075 lines, 13 rules implemented. Extended to the full [AT-01](../../architecture/01-solution-and-project-layout.md#rule-at-01)–[AT-14](../../architecture/01-solution-and-project-layout.md#rule-at-14) set |
| `tests/ArchitectureTests/RepositoryPolicyTests.cs` | **Exists** — 19 test methods. Extended to [RP-01](../../architecture/01-solution-and-project-layout.md#rule-rp-01)–[RP-10](../../architecture/01-solution-and-project-layout.md#rule-rp-10). Whether it becomes a separate project is a packaging choice, not a gap |
| `tests/ArchitectureTests/FixtureCompiler.cs`, `ProjectGraph.cs` | **Exist** — the negative-fixture and graph mechanism this package relies on |
| `tests/SpecificationIntegrityTests/` | Created: link, identifier and coverage checks over the design repository |
| `eng/policy/exceptions.json` | Created: the owned, expiring exception set |
| CI pull-request pipeline | Both suites added as required stages |

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

| Evidence | Produced by |
|---|---|
| Layering test results with negative fixtures | [WP-05.00](#rule-wp-05.00) |
| Licence boundary report | [WP-05.01](#rule-wp-05.01) |
| Forbidden-term scan, zero findings | [WP-05.02](#rule-wp-05.02) |
| Contract and serialization policy results | [WP-05.03](#rule-wp-05.03) |
| Banned-symbol detection results | [WP-05.04](#rule-wp-05.04) |
| Invariant enforcement accounting report, **429 of 429** classified from real results | [WP-05.05](#rule-wp-05.05) |
| Specification integrity report, zero findings | [WP-05.06](#rule-wp-05.06) |

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

**Upstream — all must be complete.**

- [WP-02](02-build-governance-and-analyzer-policy.md#rule-wp-02)
- [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03)

**Downstream — consumers of these released outputs.**

- [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)
- [WP-21](21-cloud-host-and-persistence.md#rule-wp-21)


---
