# WP-05 — Architecture and Repository Policy Test Suite

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `02`, `03` · Downstream: `06`, `21`

> **Goal.** Turn the architecture into build failures. Every structural rule that a reviewer would otherwise have to remember becomes a test, so that a violation is caught at the moment it is introduced rather than at a release gate months later.

---

## 1. Scope and purpose

**In scope.** The `ArchitectureTests` suite (`AT-01`–`AT-14`), the `RepositoryPolicyTests` suite (`RP-01`–`RP-10`), the forbidden-term scan, the invariant coverage assertion, and the documentation integrity checks over this design repository.

**Out of scope.** Behavioural tests of any kind. Performance gates (`06` and each product package). The policy *data* these tests read, which `00` and `02` produce.

**Why this package exists.** Without it, every rule in the architecture layer is advice. With it, the rules are the build. This is also the cheapest possible enforcement point for the invariant catalogue, which is otherwise 490 statements nobody can hold in mind.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) `§8` | The `AT-*` and `RP-*` rule sets to implement |
| [`../../architecture/00-architecture-overview.md`](../../architecture/00-architecture-overview.md) | Layering rules `LY-01`–`LY-09` |
| [`../../assurance/testing-and-verification-strategy.md`](../../assurance/testing-and-verification-strategy.md) `§4`, `§7` | The invariant-to-test obligation and the specification integrity checks |
| `WP-00` output | Forbidden-term lists, glossary policy data, invariant catalogue with mechanisms |
| `WP-02` output | A build that can fail; the dependency policy data |
| `WP-03` output | Contract projects and their licence declarations |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **A structural rule is tested, not reviewed** (`TS-04` in the testing strategy). |
| BR-02 | **A policy test failure is a build failure**, never a warning. |
| BR-03 | **Every invariant maps to at least one architecture rule, one test and one work-package completion gate** (**D-018**). |
| BR-04 | **The forbidden-term scan covers source, identifiers, resource strings and implementation documentation**, excluding preserved historical inputs. |
| BR-05 | **A test that enforces an invariant names it**, so a failure identifies the violated rule (`IV-04` there). |
| BR-06 | **An exception to a policy test is data, owned and expiring** — never a code comment that disables the check. |
| BR-07 | **Policy tests run in pull-request builds** (`CI-01` in the build architecture), so a violation never reaches the main branch. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `tests/ArchitectureTests/` | Extended to the full `AT-01`–`AT-14` set |
| `tests/RepositoryPolicyTests/` | **Created**, implementing `RP-01`–`RP-10` |
| `tests/SpecificationIntegrityTests/` | Created: link, identifier and coverage checks over the design repository |
| `eng/policy/exceptions.json` | Created: the owned, expiring exception set |
| CI pull-request pipeline | Both suites added as required stages |

**Major types introduced:** test infrastructure only.

---

## 5. Required implementation work

### WP-05.00 — Layering and reference direction

**What must be fully done.** Tests asserting: domain projects reference no infrastructure; application projects reference no UI; building blocks reference no product; no product references another product's internals; contract projects reference only contract projects and the foundation; the shared foundation contains no product knowledge; and no project reachable from an AOT deliverable references a fenced project.

**Testing requirements.** Each rule has a positive fixture and a negative fixture that must fail.

**Completion gate.** Every layering rule has a passing positive case and a failing negative case.

### WP-05.01 — Licence boundary enforcement

**What must be fully done.** Tests asserting: every project declares an SPDX identifier and a boundary; no Apache-boundary project references an AGPL project directly or transitively; the Apache set matches the enumerated list; and every dependency's licence is on the allowlist for its consuming boundary.

**Testing requirements.** A negative fixture introducing a cross-boundary reference must fail the build.

**Completion gate.** All four assertions pass, and the negative fixture fails as designed.

### WP-05.02 — Forbidden terms and naming

**What must be fully done.** The scan covers superseded product names, the superseded payment provider, forbidden aliases from the glossary, and obsolete architectural terms. Coverage includes type and member names, namespaces, resource strings, and implementation documentation. The preserved input corpus in this design repository is excluded.

**Testing requirements.** A negative fixture containing each forbidden term must be detected; the scan must produce zero findings on the current tree.

**Completion gate.** Zero findings, and every forbidden term is detectable.

### WP-05.03 — Contract and serialization policy

**What must be fully done.** Tests asserting: every public DTO belongs to a source-generated context; no reflection-based serializer is reachable; every local RPC contract interface carries the generated-shape attribute (**V-05b**); the typed HTTP client's reflection package is absent; and every contract project's generated artifacts match the committed baseline.

**Testing requirements.** Negative fixtures for each assertion.

**Completion gate.** All assertions pass with negative fixtures failing. **This makes `VG-04`'s policy-test half enforceable.**

### WP-05.04 — Banned APIs and patterns

**What must be fully done.** A banned-symbol list covering: reflection entry points on AOT paths, dynamic code generation, blocking waits on async paths, direct provider SDK calls outside adapters, direct logging of secret-bearing or content types, floating-point arithmetic in money and credit paths, and raw pointer fields where a safe handle is required.

**Testing requirements.** A negative fixture per banned category.

**Completion gate.** Every banned category is detected.

### WP-05.05 — Invariant coverage

**What must be fully done.** A coverage report mapping every invariant in the catalogue to its enforcement mechanism and to at least one concrete test. Invariants with no test are reported as open findings with an owner and the package that will close them.

**Testing requirements.** The coverage report itself is asserted: it must account for 100 % of invariants, either as covered or as an owned open finding.

**Completion gate.** 100 % of invariants are accounted for, and the open findings each have an owner and a target package. **This satisfies `PG-06`.**

### WP-05.06 — Specification integrity

**What must be fully done.** Checks over this design repository: every internal link resolves; every cited requirement, architecture rule, decision, verification finding and gate identifier exists; no superseded name appears outside the preserved inputs; every Phase 1 decision is cited by at least one Phase 2 document or its non-applicability is stated; and the work-package dependency graph is acyclic with every referenced package existing.

**Testing requirements.** The checks run against the current design repository and produce zero findings.

**Completion gate.** Zero findings across all six checks.

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
| Layering test results with negative fixtures | `WP-05.00` |
| Licence boundary report | `WP-05.01` |
| Forbidden-term scan, zero findings | `WP-05.02` |
| Contract and serialization policy results | `WP-05.03` |
| Banned-symbol detection results | `WP-05.04` |
| Invariant coverage report, 100 % accounted | `WP-05.05` |
| Specification integrity report, zero findings | `WP-05.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Every layering, reference-direction and licence rule has a passing positive case and a failing negative case.
2. The forbidden-term scan produces zero findings and detects every listed term.
3. Contract, serialization and RPC-attribute policy is enforced with negative fixtures failing.
4. Every banned API category is detected.
5. 100 % of glossary invariants are accounted for as covered or as an owned open finding — satisfying `PG-06`.
6. Specification integrity checks produce zero findings.
7. Both suites run in the pull-request pipeline and a violation fails the build.

---

## 9. Dependencies

**Upstream.** `02` (a failing build and policy data), `03` (contract projects to assert against).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `06` — AOT proof | Policy tests that prevent an AOT-breaking pattern from being reintroduced |
| `21` — Cloud host | Module boundary assertions |
| Every later package | A build that rejects architecture violations at the moment they are written |
