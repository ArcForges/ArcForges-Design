# Testing and Verification Strategy

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (runtime and AOT matrix), **[V-03](phase-1-official-verification.md#rule-v-03)**/**[V-04](phase-1-official-verification.md#rule-v-04)**/**[V-05](phase-1-official-verification.md#rule-v-05)** (AOT evidence), **[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** (glossary and invariants), the Product Quality Contract
> Companions: [`../requirements/12-quality-and-compatibility-contract.md`](../requirements/12-quality-and-compatibility-contract.md), [`release-gates.md`](release-gates.md), [`traceability-matrix.md`](traceability-matrix.md), [`../architecture/01-solution-and-project-layout.md`](../architecture/01-solution-and-project-layout.md)

The quality contract states *what must be true*. This document states *how it is proved*: which test families exist, what each is uniquely responsible for catching, where each runs, what evidence it produces, and what it is not allowed to substitute for.

---

## 1. Strategy principles

| # | Principle |
|---|---|
| TS-01 | **Each test family exists to catch a failure class no other family catches.** A family that duplicates another is removed, not kept for comfort. |
| TS-02 | **A passing test in one execution mode is not evidence for another** ([QI-01](../requirements/12-quality-and-compatibility-contract.md#rule-qi-01), [QI-02](../requirements/12-quality-and-compatibility-contract.md#rule-qi-02), [QI-03](../requirements/12-quality-and-compatibility-contract.md#rule-qi-03)). Debug is not Production; JIT is not AOT; a successful build is not runtime compatibility. |
| TS-03 | **Every invariant in the glossary catalogue maps to a planned verification** (**[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)**, design obligation B, complete), and to an **implemented** check before its owning package closes (obligation C, open). A planned verification is not evidence that the invariant holds. |
| <a id="rule-ts-04"></a>TS-04 | **Structural rules are tested, not reviewed.** Architecture and repository-policy tests turn design rules into build failures. |
| TS-05 | **Evidence is produced and retained**, not asserted. A gate that cannot point at an artifact is not passed. |
| TS-06 | **Tests are deterministic.** A test that depends on wall-clock timing, network availability, machine speed or ordering is either made deterministic or moved to a family designed for non-determinism (soak, hardware lab). |
| TS-07 | **A flaky test is quarantined with an owner and an expiry** ([CI-06](../architecture/14-build-packaging-and-release.md#rule-ci-06) in the build architecture), never retried indefinitely. |
| TS-08 | **Test data is synthetic or licence-cleared** ([PR-04](reference-coverage-and-provenance.md#rule-pr-04) in the provenance document). Real user content never becomes a fixture. |
| TS-09 | **No test writes to a real customer-facing external service.** Providers are exercised through their test environments or through recorded contract fixtures. |

---

## 2. The eighteen test families

Each family below states its unique responsibility, where it runs, and its evidence.

### 2.1 Fast families — every pull request

| # | Family | Uniquely catches | Evidence |
|---|---|---|---|
| <a id="rule-f-01"></a>F-01 | **Domain unit tests** — pure, fast, no I/O | Logic defects in domain rules, state machines, invariant enforcement and value semantics | Test results with per-invariant mapping |
| <a id="rule-f-02"></a>F-02 | **Application tests with port doubles** | Orchestration defects: wrong sequencing, missing compensation, incorrect authorization call ordering | Test results |
| <a id="rule-f-04"></a>F-04 | **Serialization and type-shape compatibility tests** | A DTO that no longer round-trips, a missing source-generated context, a shape change that breaks an older client | Round-trip results plus a diff against the committed type-shape baseline |
| <a id="rule-f-17"></a>F-17 | **Architecture and repository-policy tests** | Layering violations, forbidden references, licence-boundary breaches, forbidden terms, banned APIs, prohibited patterns | The `AT-*` and `RP-*` result set (`§8` of the solution layout) |

### 2.2 Integration families — main branch

| # | Family | Uniquely catches | Evidence |
|---|---|---|---|
| <a id="rule-f-03"></a>F-03 | **Persistence tests against real stores** | Defects an in-memory double hides: transaction semantics, isolation, constraint behaviour, index behaviour, migration effects | Test results per supported store version |
| <a id="rule-f-05"></a>F-05 | **Local RPC integration tests over real named pipes and domain sockets** | Framing, concurrency, ordering, cancellation, disconnection and reconnection defects (`§3` of the local IPC architecture) | Test results per platform |
| <a id="rule-f-06"></a>F-06 | **Public API contract tests: generated client against a real server** | Divergence between the C# source of truth, the generated document and the running implementation (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**) | Contract diff plus test results |
| <a id="rule-f-07"></a>F-07 | **Realtime integration tests** | Connect, disconnect, reconnect, sequence-gap recovery and backfill defects (`§7` of the cloud architecture) | Test results including induced gap scenarios |
| <a id="rule-f-11"></a>F-11 | **Multi-process end-to-end tests** | Defects that only appear when the products, Hub, extension host and cloud all run together | Scenario results with process logs |
| <a id="rule-f-12"></a>F-12 | **Migration and golden-fixture tests** | Data loss, semantic drift and irreversible migration defects ([QI-07](../requirements/12-quality-and-compatibility-contract.md#rule-qi-07)) | Fixture set plus before/after comparison |
| <a id="rule-f-16"></a>F-16 | **Publish, install, update, downgrade-protection and rollback tests** | Packaging, staging, atomic switch, rollback and data-directory defects (`§10` of the build architecture) | Matrix results per platform |

### 2.3 Robustness families — main branch and scheduled

| # | Family | Uniquely catches | Evidence |
|---|---|---|---|
| <a id="rule-f-08"></a>F-08 | **Native ABI tests per runtime identifier, including every error path** | ABI mismatch, ownership defects, handle leaks, use-after-free and error-path omissions (`§9` of the native architecture) | Per-RID results plus sanitiser output |
| <a id="rule-f-13"></a>F-13 | **Crash, fault-injection and recovery tests** | Unrecoverable state after a crash; the difference between crash-free and recoverable ([QI-08](../requirements/12-quality-and-compatibility-contract.md#rule-qi-08)) | Recovery outcome per injected fault |
| <a id="rule-f-14"></a>F-14 | **Soak and scale tests** | Leaks, unbounded growth, handle exhaustion, degradation over time and at corpus scale ([QI-11](../requirements/12-quality-and-compatibility-contract.md#rule-qi-11)) | Duration, resource curves, final state |
| <a id="rule-f-15"></a>F-15 | **Performance benchmarks with regression gates** | Silent regression against startup, memory, responsiveness and bundle budgets (`§2` of the quality contract) | Measured values against budget and against the previous release |

### 2.4 Human-facing and physical families

| # | Family | Uniquely catches | Evidence |
|---|---|---|---|
| <a id="rule-f-09"></a>F-09 | **UI component and automation tests** | Binding, command availability, state presentation and navigation defects | Test results plus failure screenshots |
| <a id="rule-f-10"></a>F-10 | **Accessibility tests, automated and assistive-technology-verified** | Automated checks pass while the product is unusable with a screen reader ([QI-16](../requirements/12-quality-and-compatibility-contract.md#rule-qi-16), [QI-17](../requirements/12-quality-and-compatibility-contract.md#rule-qi-17)) | Automated results plus a dated manual verification record |
| <a id="rule-f-18"></a>F-18 | **Hardware-lab tests for ArcScope and ArcSlate** | Real device, real driver, real codec and real timing defects that no simulation reproduces ([QI-21](../requirements/12-quality-and-compatibility-contract.md#rule-qi-21)) | Device inventory, run records, captured artifacts |

---

### 2.5 React/TypeScript execution of the existing families

[P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) adds Node/browser runners, not a replacement for the eighteen evidence families. Vitest/React Testing Library cover TS state, components and generated validation; Playwright covers production browser assets, edge/session behavior, accessibility and visual scenarios. C# server/persistence/architecture tests retain their existing runner and real infrastructure obligations.

| Boundary | Required evidence | What does not substitute |
|---|---|---|
| C# → OpenAPI → TS SDK | Fresh C# export/baseline diff, deterministic TS generation, real-server C#/TS calls and exact-value/unknown-field/error/header vectors | TypeScript compilation or a hand-authored matching fixture |
| Browser session | Real cookie/CSRF/origin, concurrent logout/expiry, replica failover, step-up, passkey matrix and no-credential-leak tests | A unit test of a frontend auth state flag |
| Realtime/stream | Both language adapters, duplicate/gap/reconnect, byte-offset correctness, polling equivalence and revocation | A component playing pre-recorded chunks only |
| Consumer interface | Approved representative production-rendered visual baselines, responsive/locale/theme states, keyboard/assistive review and interaction checks | Installing a UI library or accepting screenshots alone |
| Independent workflows | Windows VS esproj command evidence and direct npm work on non-Windows, one locked dependency root | Successful dotnet or CMake build |
| Release | Promoted Node artifacts, real Cloud commercial/Chat flows, strict production CSP, old cached clients, edge routes and rollback | Vite dev server, MSW, a hosted prototype or .NET WASM publish |

MSW remains an explicit test-only developer mode; release route graphs exclude it. Failed required external prerequisites make an integration gate incomplete, not silently skipped. [PG-23](open-gates-register.md#rule-pg-23) aggregates the resulting Web release evidence.

---



## 3. Cross-cutting verification themes

These are not additional families; they are obligations distributed across the families above, each with a named owner.

| # | Theme | Where it is proved |
|---|---|---|
| CV-01 | **AOT correctness** | [F-16](#rule-f-16) and [F-17](#rule-f-17) publish AOT for every desktop product with zero trim or AOT diagnostics; [F-05](#rule-f-05), [F-06](#rule-f-06) and [F-08](#rule-f-08) run against AOT-published binaries, not JIT test hosts ([QI-02](../requirements/12-quality-and-compatibility-contract.md#rule-qi-02)) |
| CV-02 | **Mobile runtime posture** | The Android release artifact is built by CI, its runtime confirmed by inspecting the artifact, and smoke-tested on a real device ([RT-07](../architecture/11-mobile-architecture.md#rule-rt-07), [RT-08](../architecture/11-mobile-architecture.md#rule-rt-08) in the mobile architecture) |
| CV-03 | **Contract compatibility across the supported window** | [F-06](#rule-f-06) runs the current client against the previous and minimum supported server, and the reverse (`§15` of the quality contract) |
| CV-04 | **Idempotency** | [F-02](#rule-f-02), [F-03](#rule-f-03) and [F-11](#rule-f-11) assert that every command, event and settlement path is exactly-once in effect under duplication and retry |
| CV-05 | **Security enforcement** | [F-02](#rule-f-02) and [F-11](#rule-f-11) assert refusal paths: exceeded grant, missing approval, expired lease, egress without authorization, and owner-side final validation |
| CV-06 | **Redaction** | [F-11](#rule-f-11) asserts that marker values never appear in exported telemetry (`§14` of the observability architecture) |
| CV-07 | **Licence and provenance** | [F-17](#rule-f-17) asserts boundary compliance; the release pipeline asserts SBOM, NOTICE and dependency closure (`§4.2` of the provenance document) |
| CV-08 | **Glossary and invariant enforcement** | [F-17](#rule-f-17) runs the forbidden-term scan; [F-01](#rule-f-01) maps each `X ≠ Y` invariant to an assertion (**[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)**) |
| CV-09 | **Offline and degradation honesty** | [F-11](#rule-f-11) asserts that every product starts, works and saves with Cloud entirely unavailable, and that degraded capabilities are named rather than silently missing |
| CV-10 | **Localisation and locale-safe data** | [F-09](#rule-f-09) and [F-12](#rule-f-12) assert canonical storage with localised presentation, and that a locale change never alters stored data ([QI-18](../requirements/12-quality-and-compatibility-contract.md#rule-qi-18)) |

---

## 4. The invariant-to-test obligation

**[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** produces an invariant catalogue of **429** `X ≠ Y` statements — 421 at the original baseline plus 8 added by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) ([I-491](../requirements/01-normative-glossary-and-invariants.md#rule-i-491)–[I-498](../requirements/01-normative-glossary-and-invariants.md#rule-i-498)). That is the count, not the highest identifier, which reaches [I-498](../requirements/01-normative-glossary-and-invariants.md#rule-i-498) because each section reserves headroom. They are only useful if they are enforced.

**The obligation has two halves with two gates.** They were previously conflated, which let an owned open finding appear to satisfy a coverage gate.

| Half | Content | Gate | State |
|---|---|---|---|
| **Design traceability** | Architecture home, mechanism, **planned** verification, owning gate — per invariant | [PG-06](open-gates-register.md#rule-pg-06) | **Closed** — **429 of 429** in [`invariant-coverage.md`](invariant-coverage.md) `§7` |
| **Implementation enforcement** | An **implemented** check with a **passing** result | [PG-11](open-gates-register.md#rule-pg-11) | **Open** — distributed across owning packages |

| # | Rule |
|---|---|
| IV-01 | **Every invariant maps to an architecture rule, a planned verification and an owning work-package completion gate** — complete, in [`invariant-coverage.md`](invariant-coverage.md) `§7`. |
| IV-02 | **An invariant with no implemented test leaves [PG-11](open-gates-register.md#rule-pg-11) open.** Registering it as an open finding records who owes the work; it does not satisfy the gate, and it has no effect on [PG-06](open-gates-register.md#rule-pg-06). |
| IV-03 | **Invariants are enforced by the cheapest sufficient mechanism**: a type distinction where possible, a repository-policy test where a naming or reference rule expresses it, a unit test where it is behavioural, and an end-to-end test only where nothing smaller can observe it. |
| <a id="rule-iv-04"></a>IV-04 | **A test that enforces an invariant names it**, so a failure message identifies the violated rule rather than only the failed assertion. |
| IV-05 | **The forbidden-alias and obsolete-name scan runs over `src/` and `docs/` excluding `docs/inputs/`**, plus identifiers and resource strings (`§10` of the glossary requirements). |

---

## 5. Test environments

| Environment | Purpose | Constraints |
|---|---|---|
| **Developer machine** | Fast families, targeted integration | Must run without cloud credentials or a network |
| **CI ephemeral** | Fast and integration families | Real store instances, real pipes and sockets, no shared mutable state between runs |
| **CI platform matrix** | Per-platform families | Every supported platform and architecture on a matching runner ([CI-05](../architecture/14-build-packaging-and-release.md#rule-ci-05) in the build architecture) |
| **Long-run agent** | Soak, scale, fuzzing, sanitiser builds | Scheduled, with resource curves retained |
| **Hardware lab** | [F-18](#rule-f-18) | Physical devices with a maintained inventory, recorded firmware and driver versions |
| **Staging** | Release-candidate verification against provider test environments | Never customer data; provider test mode only |

| # | Rule |
|---|---|
| TE-01 | **A test that cannot run on a developer machine must state why**, and a local substitute must exist for the same failure class where one is possible. |
| TE-02 | **No test suite requires a production credential.** |
| <a id="rule-te-03"></a>TE-03 | **The hardware-lab inventory is a maintained artifact** with device, firmware and driver versions, because a result is only meaningful against a known configuration (`§3` of the quality contract). |
| <a id="rule-te-04"></a>TE-04 | **Provider integrations are exercised against provider test environments**, and their contract shape is additionally frozen as recorded fixtures so a provider outage does not block CI. |

---

## 6. Fixtures and corpora

| Corpus | Contents | Owner obligation |
|---|---|---|
| **Format fixtures** | Files in each supported format version, first-party and reference-produced | Versioned; an import claim without a fixture is withdrawn ([ME-03](reference-coverage-and-provenance.md#rule-me-03) in the provenance document) |
| **Migration fixtures** | A store at each historical schema version | Every migration is exercised forward, and backward where reversibility is claimed |
| **Contract fixtures** | Serialized payloads for each contract version in the supported window | Never regenerated in place; a new version adds a new fixture |
| **Scale corpus** | Large, realistic project, note, capture and timeline sets | Sized per the quality contract's scale definitions |
| **Fuzzing corpus** | Inputs for every parser reachable from untrusted content | Extended by every parser defect found ([SB-04](../architecture/12-native-interop-and-media.md#rule-sb-04) in the native architecture) |
| **Adversarial corpus** | Prompt-injection attempts, hostile catalog metadata, malformed manifests, oversized payloads | Extended by every security finding |
| **Accessibility scenarios** | Keyboard-only and screen-reader task scripts for every core workflow | Re-verified per release |

| # | Rule |
|---|---|
| FX-01 | **A fixture is immutable once released.** Changing a fixture invalidates the history it was proving. |
| FX-02 | **Every fixture carries provenance** ([VO-03](reference-coverage-and-provenance.md#rule-vo-03) there). |
| FX-03 | **A fixture set is complete for the compatibility window it claims**, and the window is stated. |

---

## 7. Verification of the specification itself

Design defects are cheaper to catch than implementation defects.

| # | Check | Mechanism |
|---|---|---|
| <a id="rule-sv-01"></a>SV-01 | Every normative citation resolves to its explicitly linked defining document and stable anchor ([OG-05](open-gates-register.md#rule-og-05)). Historical relocations and unused allocation ranges are classified explicitly and never counted as active implementation gates. | Complete corpus resolver: fail on a missing, duplicate or ambiguous definition; repeat after every normative change |
| <a id="rule-sv-02"></a>SV-02 | Every internal document link resolves | Link check over `docs/` |
| SV-03 | No superseded product name or superseded provider appears as current outside `docs/inputs/` | Forbidden-term scan |
| SV-04 | Every Phase 1 decision is cited by at least one Phase 2 document, or its non-applicability is stated | Traceability matrix coverage check |
| <a id="rule-sv-05"></a>SV-05 | Every deferred gate (**[F-013](open-gates-register.md#rule-f-013)**, **[F-023](open-gates-register.md#rule-f-023)**, **[F-026](open-gates-register.md#rule-f-026)**) is scheduled in a named work package | Open-gates register |
| SV-06 | Every work package's stated dependencies refer to existing work packages, the graph is acyclic, **and every declared edge is symmetric** — an upstream declaration without its matching downstream is a defect, in either direction | Planning consistency check over the package headers and the downstream index |
| SV-07 | **No work package sits in a phase its own header contradicts**, and no package depends on one whose phase is later than its own without the backward edge being stated and justified (`§3` of the implementation sequence) | Planning consistency check |
| SV-08 | **A capability the requirements retired has no live specification, work-package step or completion gate anywhere** — a retired delivery is asserted absent, not left unmentioned | Retired-claim scan over `docs/` outside `docs/inputs/` |

---

## 8. What each family is not allowed to substitute for

| Claim | Rejected because |
|---|---|
| "Unit tests pass, so the product works" | [QI-03](../requirements/12-quality-and-compatibility-contract.md#rule-qi-03) — build and unit success is not runtime compatibility |
| "JIT tests pass, so AOT is fine" | [QI-02](../requirements/12-quality-and-compatibility-contract.md#rule-qi-02) — AOT compatibility is a separate proof (**[V-03](phase-1-official-verification.md#rule-v-03)**, **[V-04](phase-1-official-verification.md#rule-v-04)**, **[V-05](phase-1-official-verification.md#rule-v-05)**) |
| "The debug build is fast" | [QI-01](../requirements/12-quality-and-compatibility-contract.md#rule-qi-01) — Debug performance is not Production performance |
| "Migration succeeded" | [QI-07](../requirements/12-quality-and-compatibility-contract.md#rule-qi-07) — success is not semantic preservation |
| "It did not crash" | [QI-08](../requirements/12-quality-and-compatibility-contract.md#rule-qi-08) — crash-free is not recoverable |
| "The benchmark is green" | [QI-11](../requirements/12-quality-and-compatibility-contract.md#rule-qi-11) — a small benchmark is not scale reliability |
| "Startup is within budget" | [QI-12](../requirements/12-quality-and-compatibility-contract.md#rule-qi-12) — startup time is not time to usable |
| "Colour contrast passes" | [QI-16](../requirements/12-quality-and-compatibility-contract.md#rule-qi-16), [QI-17](../requirements/12-quality-and-compatibility-contract.md#rule-qi-17) — automated checks are not an accessible product |
| "It works on this OS" | [QI-22](../requirements/12-quality-and-compatibility-contract.md#rule-qi-22) — one platform is not cross-platform support |
| "The simulator passes" | [QI-21](../requirements/12-quality-and-compatibility-contract.md#rule-qi-21) — automated tests are not real-hardware validation |
| "We have logs" | [QI-23](../requirements/12-quality-and-compatibility-contract.md#rule-qi-23) — a diagnostic log is not an audit record |

---

## 9. Reporting

| # | Rule |
|---|---|
| RP-01 | **Every release produces a quality report** (`§24` of the quality contract) containing measured budgets, family results, waivers, and the gate outcomes of [`release-gates.md`](release-gates.md). |
| RP-02 | **A waiver is explicit, owned and expiring** (`§21.1` there). An expired waiver blocks release. |
| RP-03 | **Trends are retained**, so a slow regression across releases is visible rather than only a single-release comparison. |
| RP-04 | **A gate result names its evidence artifact**, so a claim can be checked after the fact. |

---

## 10. Traceability

| Source | Consumed as |
|---|---|
| `§25` of the quality contract | The eighteen families, elaborated here with responsibility, placement and evidence |
| `§26` there | The quality invariants that define what each family may not substitute for |
| **[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** | The invariant-to-test obligation and the forbidden-term scan |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](phase-1-official-verification.md#rule-v-03)**, **[V-04](phase-1-official-verification.md#rule-v-04)**, **[V-05](phase-1-official-verification.md#rule-v-05)** | AOT and runtime verification obligations |
| **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** | Contract tests against the generated artifacts and the running implementation |
| **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**, **[F-013](open-gates-register.md#rule-f-013)**, **[F-023](open-gates-register.md#rule-f-023)** | Fixture provenance and licence verification obligations |
