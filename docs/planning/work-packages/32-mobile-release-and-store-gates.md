# WP-32 — Mobile Release Engineering and Store Gates

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: G — Mobile
> Upstream: `31` · Downstream: `50`

> **Goal.** Get a real Android release artifact through every gate: dependency closure and provenance (**F-023**), consumption-only conformance (**V-09**), the runtime posture confirmed from the artifact (**V-04**), and build-verifiable commerce prohibitions — none of which is satisfied by reading a document.

---

## 1. Scope and purpose

**In scope.** The Android release build and signing; the store listing and its category-fit confirmation; the **F-023** dependency closure and provenance audit; the **V-09** consumption-only conformance confirmation; the commerce-prohibition build check; on-device release verification; and the iOS position stated honestly.

**Out of scope.** Any in-app purchase or billing integration — prohibited (**D-022**). iOS build activation, which remains deferred (**D-008**).

**Why this package exists.** Three of the register's open gates converge on the first mobile artifact. They are not documentation tasks: **F-023** requires an audited transitive closure, **V-09** requires a review outcome, and **V-04** requires inspecting a produced binary.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md) | **F-023**, **VG-07**, **VG-13** and their owners and triggers |
| [`../../assurance/release-gates.md`](../../assurance/release-gates.md) `§6.4` | The mobile release gate set |
| [`../../requirements/10-distribution-update-and-support.md`](../../requirements/10-distribution-update-and-support.md) `§1.1` | The mobile platform matrix and its obligations |
| **D-022**, **V-09** | Consumption-only posture and its verification requirement |
| `WP-31` output | A complete application to release |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The complete direct and transitive dependency closure is verified before the first artifact is produced** — **F-023**. |
| BR-02 | **On discovering a conflicting contribution or dependency, the issue is registered and returned for decision** (**D-004**). Silently adding an exception, changing the licence or dropping the mobile target is prohibited. |
| BR-03 | **No purchase surface, embedded checkout, store billing integration, external purchase call to action, or licence-key or purchase-token unlock path exists in any build path** (**D-022**). |
| BR-04 | **A build-time and CI check asserts every prohibition** in `BR-03`. |
| BR-05 | **The runtime is confirmed by inspecting the produced release artifact**, not by reading the project file (**V-04**). |
| BR-06 | **CI builds the release artifact and runs on-device smoke tests.** A successful debug build is not a pass. |
| BR-07 | **The store developer account is established under the intended long-term owning identity**, not casually under a personal account. |
| BR-08 | **A store listing is distribution, never a commerce channel.** |
| BR-09 | **iOS is not claimed as compiled or tested** (**D-008**). |
| BR-10 | **The product's own update system is unaffected by store distribution** — mobile follows store update mechanics without that becoming the desktop model.

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `eng/build/android-aot.props` | Release configuration, verified from evaluated properties |
| `eng/signing/` | Android signing configuration with credentials held in the release credential store |
| `eng/release/mobile/` | Release procedure, store metadata and the submission checklist |
| `eng/policy/mobile-commerce-prohibitions.json` | The machine-checkable prohibition set |
| `tests/MobileReleaseTests/` | Commerce prohibition, artifact posture and on-device smoke suites |
| `eng/verification/mobile/` | The **F-023** closure report and the **V-09** confirmation record |

---

## 5. Required implementation work

### WP-32.00 — Release build and signing

**What must be fully done.** A CI-produced release artifact with platform app signing, reproducible from a commit, with its version stamped from the version-axis plumbing. Signing credentials are never on a developer machine.

**Testing requirements.** A CI release build from a clean checkout; a signature verification; a version-stamp assertion.

**Completion gate.** CI produces a signed release artifact reproducibly, with credentials held only in the release credential store.

### WP-32.01 — Runtime posture confirmation

**What must be fully done.** The produced release artifact is inspected to confirm the runtime is the supported Mono AOT path. The evidence is the artifact inspection, not the project file. A framework-upgrade re-verification checklist is attached.

**Testing requirements.** An artifact inspection record; an evaluated-property cross-check; the re-verification checklist recorded.

**Completion gate.** The runtime is confirmed from the artifact. **This satisfies `VG-07`** and links `VG-08` to the upgrade process.

### WP-32.02 — Dependency closure and provenance

**What must be fully done.** The complete direct and transitive dependency closure is enumerated with each dependency's licence, source and provenance. Any GPL-family or AGPL-only item is registered and returned for decision rather than excepted. An SBOM is produced for the artifact.

**Testing requirements.** A closure report covering 100 % of dependencies with a licence position each; a negative test asserting an introduced AGPL dependency fails the check.

**Completion gate.** 100 % of the closure has a licence position with no unresolved item. **This satisfies `F-023`.**

### WP-32.03 — Commerce prohibition check

**What must be fully done.** A machine check asserting no purchase surface, embedded checkout, store billing integration, external purchase call to action, or licence-key or purchase-token unlock path exists in any build path. The licence-key path is called out explicitly as the prohibition most likely to be violated by accident.

**Testing requirements.** Negative fixtures for each of the five prohibitions, each of which must fail the build.

**Completion gate.** All five prohibitions are machine-checked with negative fixtures failing the build.

### WP-32.04 — Store category fit and consumption-only conformance

**What must be fully done.** Category fit confirmed with the store's review process, and consumption-only conformance confirmed — by review outcome, not by reading a guideline. The confirmation and its date are recorded.

**Testing requirements.** A recorded review outcome; a checklist mapping each store requirement to its evidence.

**Completion gate.** Category fit and consumption-only conformance are confirmed by review outcome and recorded. **This satisfies `VG-13`.**

### WP-32.05 — On-device verification

**What must be fully done.** The release artifact is smoke-tested on real devices covering the supported version and form-factor range: cold start, sign-in, conversation, task, approval, background resume, weak network, push and deep link. Cold start, memory and weak-network behaviour are measured against budget.

**Testing requirements.** A device matrix run with recorded results; budget measurements; accessibility verification with the platform's assistive technology.

**Completion gate.** The release artifact passes on-device smoke tests across the device matrix, meets budgets, and passes accessibility verification.

### WP-32.06 — iOS position

**What must be fully done.** The iOS project's architecture is complete and its build status is stated as deferred, in the repository and in any public material. No claim of compilation or testing is made. The re-verification obligation before activation is recorded.

**Testing requirements.** A documentation scan asserting no compiled-or-tested claim exists.

**Completion gate.** No iOS build or test claim exists anywhere, and the activation re-verification obligation is recorded.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None |
| Protocol | The shipped mobile client version enters the supported window |
| UI | Store listing assets and metadata |
| Security | Signing, credential custody and the dependency closure |
| Platform | Android release path proven; iOS honestly deferred |
| Migration | Mobile cache migration across shipped versions |
| Compatibility | The minimum supported mobile client is declared |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| CI release build, signature verification and version stamp | `WP-32.00` |
| Artifact runtime inspection record | `WP-32.01` |
| Dependency closure report with licence positions and SBOM | `WP-32.02` |
| Five negative fixtures failing the build | `WP-32.03` |
| Recorded review outcome and requirement checklist | `WP-32.04` |
| Device matrix results, budget measurements, accessibility record | `WP-32.05` |
| Documentation scan for iOS claims | `WP-32.06` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. CI produces a signed release artifact reproducibly, with signing credentials held only in the release credential store.
2. The runtime is confirmed from the produced artifact — satisfying `VG-07`.
3. **100 % of the direct and transitive dependency closure has a licence position with no unresolved item** — satisfying `F-023`.
4. All five commerce prohibitions are machine-checked with negative fixtures failing the build.
5. Store category fit and consumption-only conformance are confirmed by review outcome — satisfying `VG-13`.
6. The release artifact passes on-device smoke tests across the device matrix, meets cold-start, memory and weak-network budgets, and passes accessibility verification.
7. No iOS build or test claim exists anywhere, and the activation re-verification obligation is recorded.

---

## 9. Dependencies

**Upstream.** `31` (a complete companion application).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `50` — Production release | A shippable mobile artifact with every mobile gate satisfied |
