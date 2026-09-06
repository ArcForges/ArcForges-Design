# WP-02 — Build Governance, Packaging Policy and Analyzers

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `01` · Downstream: `03`, `05`

> **Goal.** Make the build tell the truth. Until diagnostics are real, warnings are errors, versions are locked and the runtime split is expressed in the build itself, every later AOT proof and every later quality claim rests on unverified ground.

---

## 1. Scope and purpose

**In scope.** Repository-wide build properties, central package management with locked restore, analyzer and diagnostic policy, the AOT/trim/single-file diagnostic posture, the per-target runtime property sets, deterministic build configuration, and the build stage ordering.

**Out of scope.** Packaging artifacts and signing — those are `50`'s production concern and are specified in the build architecture; this package establishes the build *governance* they depend on. The policy test implementations themselves (`05`).

**Why this package exists.** The observed inventory found `IsAotCompatible` declared on zero projects and no committed lock file. Both are prerequisites for the AOT proof in `06` being meaningful rather than accidental.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/14-build-packaging-and-release.md`](../../architecture/14-build-packaging-and-release.md) | The build model, stages, publish matrix and versioning implementation |
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) | Project conventions `PJ-01`–`PJ-09` |
| [`../../requirements/12-quality-and-compatibility-contract.md`](../../requirements/12-quality-and-compatibility-contract.md) | The AOT contract, the nine version axes and the dependency upgrade gate |
| **D-008**, **V-03**, **V-04**, **V-05** | The runtime split and the evidence obligations attached to each target |
| `WP-01` output | The settled project set and dispositions |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The SDK version is pinned and upgrading it is a reviewed change** (`BM-01` in the build architecture). |
| BR-02 | **Central package management is mandatory**; a version number in a business project file is a defect (`PJ-04`). |
| BR-03 | **The lock file is committed and CI restores in locked mode** (`PJ-05`). |
| BR-04 | **Warnings are errors on the main path**; trim and AOT diagnostics are always errors on AOT deliverables (`PJ-08`). |
| BR-05 | **Every reusable library consumed by an AOT deliverable declares AOT compatibility; every AOT host declares AOT publish** (`PJ-02`). |
| BR-06 | **Desktop is Native AOT; Cloud is ASP.NET Core JIT; Android is Mono AOT; Web is WebAssembly without AOT compilation** (**D-008**). The build expresses this split; no target inherits another's posture. |
| BR-07 | **Cloud must not be packaged as Native AOT** for consistency's sake (**D-008**, **V-03**). |
| BR-08 | **Preview packages never enter a stable branch's core path** (`PJ-06`). |
| BR-09 | **The build must not depend on machine state** (`BM-05`) and must work offline after restore (`BM-07`). |
| BR-10 | **Generated code is generated at build time, not committed**, except deliberate compatibility fixtures (`BM-06`). |
| BR-11 | **A dependency addition is a reviewed change** with licence, provenance, maintenance status and transitive closure recorded (`SP-10`). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `global.json` | Verified pinned, roll-forward disabled, prerelease disallowed |
| `Directory.Build.props` / `.targets` | Language version, nullable, implicit usings, deterministic build, analysis level, SourceLink, licence boundary property, warnings-as-errors staging |
| `Directory.Packages.props` | Central management with transitive pinning verified; preview packages audited |
| `packages.lock.json` | **Created and committed** at every project; CI switched to locked restore |
| `eng/build/desktop-aot.props` | Verified: AOT publish, trim analysis, single-file diagnostics as errors, RID set |
| `eng/build/cloud-jit.props` | Verified: JIT posture explicit; AOT properties absent by design |
| `eng/build/android-aot.props` | Verified: explicit runtime selection, never inherited (`RT-02` in the mobile architecture) |
| `eng/build/web-wasm.props` | Created: WebAssembly publish with AOT compilation disabled (**D-007**) |
| `eng/build/contracts.props` | Verified: source-generated serialization and generator settings for contract projects |
| `.editorconfig` | Analyzer severities as build policy |
| `eng/policy/dependency-policy.json` | Created: allowlist per licence boundary, preview-package rules, upgrade evidence requirements |

**Major types introduced:** none.

---

## 5. Required implementation work

### WP-02.00 — Pin and lock

**What must be fully done.** The SDK pin is verified and its upgrade process recorded. Central package management with transitive pinning is verified. A lock file is generated and committed for every project, and CI restore is switched to locked mode. Preview packages in the core path are enumerated and either justified or removed.

**Testing requirements.** A restore on a clean machine with no package cache succeeds in locked mode; a check that no project declares its own version of a centrally managed package.

**Completion gate.** Locked restore succeeds from clean, and no project-level version override exists.

### WP-02.01 — Diagnostic posture

**What must be fully done.** Analysis level, nullable reference types, implicit usings and deterministic build are set repository-wide. Analyzer severities are expressed in the editor configuration as build policy. Warnings-as-errors is enabled on the main path; where staged debt prevents this for a specific project, the exception is time-bounded with an owner and recorded as a waiver.

**Testing requirements.** A build with warnings-as-errors on the full solution; the waiver list is enumerated with owners and expiry dates.

**Completion gate.** The solution builds with warnings-as-errors, and every waiver has an owner and an expiry.

### WP-02.02 — AOT and trim declaration sweep

**What must be fully done.** Every reusable library that an AOT deliverable consumes declares AOT compatibility; every AOT host declares AOT publish. The resulting diagnostics are treated as findings, triaged, and either fixed or recorded as blocking items against the package that owns the offending code. This is expected to surface real work — the observed inventory found zero declarations.

**Testing requirements.** A build producing the complete diagnostic set; a triage record for every diagnostic.

**Completion gate.** Every project on an AOT chain declares its posture, and every resulting diagnostic is fixed or assigned. **A suppressed diagnostic without an assignment fails this gate.**

### WP-02.03 — Runtime split in the build

**What must be fully done.** The per-target property files express **D-008** exactly: desktop Native AOT with the RID set; Cloud JIT with AOT properties deliberately absent; Android with explicit runtime selection that is never inherited from a framework default; Web with AOT compilation disabled. Each file carries a comment stating the governing decision and the verification finding behind it.

**Testing requirements.** A property-inspection test asserting each target's effective posture; a check that no target file sets a property belonging to another target's posture.

**Completion gate.** Each target's effective posture matches **D-008**, verified by inspection of evaluated properties rather than by reading the file.

### WP-02.04 — Version axis plumbing

**What must be fully done.** The nine version axes are produced by the build (`§4` of the build architecture): each axis has a declared source of truth and is stamped into the appropriate artifact. Build metadata — commit, build identifier, pipeline run — is stamped into every assembly and is retrievable at runtime for support.

**Testing requirements.** A test asserting every axis is present and that no axis is derived from another; a runtime test that build metadata is retrievable from a published binary.

**Completion gate.** All nine axes are produced independently, and build metadata is retrievable from a published artifact.

### WP-02.05 — Dependency policy

**What must be fully done.** A dependency policy exists as data: the allowlist per licence boundary, the preview-package rule, and the evidence required for an addition or an upgrade — licence, provenance, maintenance status, transitive closure, and for AOT chains an AOT compatibility statement. The framework-upgrade re-verification obligation (`VG-08`) is recorded as a recurring checklist attached to the policy.

**Testing requirements.** A policy check over the current dependency set; a dry run of the addition process for one new dependency.

**Completion gate.** The policy exists as machine-readable data, the current dependency set passes it, and the framework-upgrade checklist is recorded. **This schedules `VG-08`.**

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None |
| Protocol | Contract projects gain their generator and serialization settings |
| UI | None |
| Security | The dependency policy and locked restore are supply-chain controls |
| Platform | The runtime split becomes a build fact rather than an intention |
| Migration | None |
| Compatibility | The nine version axes become producible, which every later compatibility claim depends on |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Clean-machine locked restore log | `WP-02.00` |
| Warnings-as-errors build log plus the waiver list | `WP-02.01` |
| The full AOT/trim diagnostic set with triage records | `WP-02.02` |
| Evaluated-property report per target | `WP-02.03` |
| Version axis report and a runtime metadata retrieval test | `WP-02.04` |
| Dependency policy check report | `WP-02.05` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Locked restore succeeds from a clean machine and no project overrides a central version.
2. The solution builds with warnings-as-errors; every waiver has an owner and an expiry.
3. Every project on an AOT chain declares its posture, and every resulting diagnostic is fixed or assigned to a named package.
4. Each target's effective runtime posture matches **D-008**, verified from evaluated properties.
5. All nine version axes are produced independently and build metadata is retrievable from a published artifact.
6. The dependency policy exists as data, passes against the current set, and carries the framework-upgrade re-verification checklist.

---

## 9. Dependencies

**Upstream.**

| Package | What this needs from it |
|---|---|
| `01` | The settled project set and dispositions to apply conventions to |

**Downstream.**

| Package | What it needs from here |
|---|---|
| `03` — Contract foundation | Generator settings, serialization posture, locked packages |
| `05` — Policy tests | A build that can fail on policy violations |
| `06` — AOT proof | Real diagnostics, without which the proof is meaningless |
| `10` — Design system *(transitive, through `06`)* | The AOT diagnostic posture that third-party control adoption is judged against |
| Every later package | A build that enforces rather than reports |
