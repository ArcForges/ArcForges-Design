# WP-05 — Architecture and Repository Policy Test Suite

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `02`, `03` · Downstream: `06`, `21`

> **Goal.** Turn the architecture into build failures. Every structural rule that a reviewer would otherwise have to remember becomes a test, so that a violation is caught at the moment it is introduced rather than at a release gate months later.

---

## 1. Scope and purpose

**In scope.** Extending the existing `ArchitectureTests` suite to the full `AT-01`–`AT-14` set, extending its `RepositoryPolicyTests.cs` to `RP-01`–`RP-10`, the forbidden-term scan, the invariant **enforcement accounting** report, and the documentation integrity checks over this design repository.

**Out of scope.** Behavioural tests of any kind. Performance gates (`06` and each product package). The policy *data* these tests read, which `00` and `02` produce. **The invariant-to-architecture mapping**, which is completed design evidence (`PG-06` closed). **Implementing every invariant's check**, which is distributed across owning packages under `PG-11`.

**Why this package exists.** Without it, every rule in the architecture layer is advice. With it, the rules are the build.

**Its scope is smaller than first planned.** The reconciliation evidence (`§5.4`) found the harness already exists: `tests/ArchitectureTests` holds **2,075 lines**, 28 test methods in `ArchitectureRuleTests.cs` and 19 in `RepositoryPolicyTests.cs`, a real project-graph loader and a negative-fixture compiler. The file header names *thirteen* rules against the accepted twenty-four. **This package reconciles rule-by-rule against a working harness; it does not build one.**

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) `§8` | The `AT-*` and `RP-*` rule sets to implement |
| [`../../architecture/00-architecture-overview.md`](../../architecture/00-architecture-overview.md) | Layering rules `LY-01`–`LY-09` |
| [`../../assurance/testing-and-verification-strategy.md`](../../assurance/testing-and-verification-strategy.md) `§4`, `§7` | The invariant-to-test obligation and the specification integrity checks |
| `WP-00` output | Forbidden-term lists and the exported glossary policy data |
| [`../../assurance/invariant-coverage.md`](../../assurance/invariant-coverage.md) | **The completed item-level invariant mapping** — a versioned input, not work to be done |
| [`../../assurance/implementation-state-reconciliation.md`](../../assurance/implementation-state-reconciliation.md) `§5.4` | The measured state of the existing test harness this package extends |
| `WP-02` output | A build that can fail; the dependency policy data |
| `WP-03` output | Contract projects and their licence declarations |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **A structural rule is tested, not reviewed** (`TS-04` in the testing strategy). |
| BR-02 | **A policy test failure is a build failure**, never a warning. |
| BR-03 | **Design-stage traceability is complete and is an input, not an output** (**D-018** obligation B; `PG-06` closed). This package builds enforcement, and reports on it — it does not re-derive the mapping. |
| BR-04 | **The forbidden-term scan covers source, identifiers, resource strings and implementation documentation**, excluding preserved historical inputs. |
| BR-05 | **A test that enforces an invariant names it**, so a failure identifies the violated rule (`IV-04` there). |
| BR-06 | **An exception to a policy test is data, owned and expiring** — never a code comment that disables the check. |
| BR-07 | **Policy tests run in pull-request builds** (`CI-01` in the build architecture), so a violation never reaches the main branch. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `tests/ArchitectureTests/` | **Exists** — 2,075 lines, 13 rules implemented. Extended to the full `AT-01`–`AT-14` set |
| `tests/ArchitectureTests/RepositoryPolicyTests.cs` | **Exists** — 19 test methods. Extended to `RP-01`–`RP-10`. Whether it becomes a separate project is a packaging choice, not a gap |
| `tests/ArchitectureTests/FixtureCompiler.cs`, `ProjectGraph.cs` | **Exist** — the negative-fixture and graph mechanism this package relies on |
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

### WP-05.05 — Invariant enforcement accounting

> **Design-stage traceability already complete.** [`../../assurance/invariant-coverage.md`](../../assurance/invariant-coverage.md) `§7` maps all 421 catalogued invariants to an architecture home, a mechanism, a planned verification and an owning gate. **`PG-06` is closed.** This sub-step does **not** re-derive that mapping and cannot re-close that gate.

**What must be fully done.** A build-produced **accounting report** stating, for every invariant, whether an **implemented** check exists and whether it **passes**. The report is a status instrument. It classifies each invariant as: enforced and passing · enforced and failing · not yet implemented.

**Testing requirements.** The report is asserted for completeness — every one of the 421 invariants appears with exactly one classification, and every classification is derived from an actual test-run result rather than declared.

**Completion gate for this sub-step.** The accounting report exists, covers all 421 invariants, and derives every classification from a real result.

> **What this gate explicitly does not do.**
>
> | It does not | Because |
> |---|---|
> | Close `PG-06` | Already closed by design evidence; a weaker later check cannot re-close a satisfied gate |
> | Close `PG-11` | `PG-11` requires every invariant **enforced and passing**. A report that faithfully records 300 unimplemented invariants is a *complete report* and a *failing* `PG-11` |
> | Let an owned open finding substitute for enforcement | Registering a finding records who owes the work. It does not do the work. `PG-11` counts implementations, not findings |
>
> **Accounting and enforcement are separate obligations with separate gates.** This sub-step owns the accounting. `PG-11` is discharged per invariant by its owning package, at that package's completion gate, with a passing result.

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
| Invariant enforcement accounting report, 421 of 421 classified from real results | `WP-05.05` |
| Specification integrity report, zero findings | `WP-05.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Every layering, reference-direction and licence rule has a passing positive case and a failing negative case.
2. The forbidden-term scan produces zero findings and detects every listed term.
3. Contract, serialization and RPC-attribute policy is enforced with negative fixtures failing.
4. Every banned API category is detected.
5. The invariant enforcement accounting report covers all 421 invariants with every classification derived from a real result. **`PG-06` was closed by design evidence before this package; `PG-11` remains open until every invariant is enforced and passing in its owning package.**
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
