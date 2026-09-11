<a id="rule-wp-02"></a>

# WP-02 — Build Governance, Packaging Policy and Analyzers

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `01` · Downstream: `03`, `05`, `47`

> **Goal.** Make the build tell the truth. Until diagnostics are real, warnings are errors, versions are locked and the runtime split is expressed in the build itself, every later AOT proof and every later quality claim rests on unverified ground.

---

## 1. Scope and purpose

**In scope.** Repository-wide build properties, central package management with locked restore, analyzer and diagnostic policy, the AOT/trim/single-file diagnostic posture, the per-target runtime property sets, deterministic build configuration, and the build stage ordering.

**Out of scope.** Packaging artifacts and signing — those are `50`'s production concern and are specified in the build architecture; this package establishes the build *governance* they depend on. The policy test implementations themselves (`05`).

**Why this package exists.** The corrected inventory records central desktop/contracts AOT imports and 165 committed per-project NuGet lockfiles. Validate evaluated properties and locked restore, repair uncovered AOT chains, and establish the accepted Web toolchain; file-local absence is not an effective-property defect.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/14-build-packaging-and-release.md`](../../architecture/14-build-packaging-and-release.md) | The build model, stages, publish matrix and versioning implementation |
| [`../../architecture/01-solution-and-project-layout.md`](../../architecture/01-solution-and-project-layout.md) | Project conventions [PJ-01](../../architecture/01-solution-and-project-layout.md#rule-pj-01)–[PJ-09](../../architecture/01-solution-and-project-layout.md#rule-pj-09) |
| [`../../requirements/12-quality-and-compatibility-contract.md`](../../requirements/12-quality-and-compatibility-contract.md) | The AOT contract, the nine version axes and the dependency upgrade gate |
| **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-04](../../assurance/phase-1-official-verification.md#rule-v-04)**, **[V-05](../../assurance/phase-1-official-verification.md#rule-v-05)** | The runtime split and the evidence obligations attached to each target |
| [WP-01](01-repository-reconciliation-and-target-layout.md#rule-wp-01) output | The settled project set and dispositions |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The SDK version is pinned and upgrading it is a reviewed change** ([BM-01](../../architecture/14-build-packaging-and-release.md#rule-bm-01) in the build architecture). |
| BR-02 | **Central package management governs NuGet; exact npm manifests and one root lock govern Web.** Node/npm and the JavaScript SDK have reviewed pins. |
| BR-03 | **The lock file is committed and CI restores in locked mode** ([PJ-05](../../architecture/01-solution-and-project-layout.md#rule-pj-05)). |
| BR-04 | **Warnings are errors on the main path**; trim and AOT diagnostics are always errors on AOT deliverables ([PJ-08](../../architecture/01-solution-and-project-layout.md#rule-pj-08)). |
| BR-05 | **Every reusable library consumed by an AOT deliverable declares AOT compatibility; every AOT host declares AOT publish** ([PJ-02](../../architecture/01-solution-and-project-layout.md#rule-pj-02)). |
| BR-06 | **Desktop is Native AOT; Cloud is ASP.NET Core JIT; Android is Mono AOT; Web is React/TypeScript built by Node/npm.** No esproj or TS package inherits .NET runtime properties ([P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008)). |
| BR-07 | **Cloud must not be packaged as Native AOT** for consistency's sake (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**). |
| BR-08 | **Preview packages never enter a stable branch's core path** ([PJ-06](../../architecture/01-solution-and-project-layout.md#rule-pj-06)). |
| BR-09 | **The build must not depend on machine state** ([BM-05](../../architecture/14-build-packaging-and-release.md#rule-bm-05)) and must work offline after restore ([BM-07](../../architecture/14-build-packaging-and-release.md#rule-bm-07)). |
| BR-10 | **Generated code is generated at build time, not committed**, except deliberate compatibility fixtures ([BM-06](../../architecture/14-build-packaging-and-release.md#rule-bm-06)). |
| BR-11 | **A dependency addition is a reviewed change** with licence, provenance, maintenance status and transitive closure recorded ([SP-10](../../architecture/14-build-packaging-and-release.md#rule-sp-10)). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `global.json` | Verified pinned, roll-forward disabled, prerelease disallowed |
| `Directory.Build.props` / `.targets` | Language version, nullable, implicit usings, deterministic build, analysis level, SourceLink, licence boundary property, warnings-as-errors staging |
| `Directory.Packages.props` | Central management with transitive pinning verified; preview packages audited |
| `packages.lock.json` | Validate the 165 existing project locks and locked CI restore; create/update only for actual project/dependency changes. No root NuGet lock is required |
| `eng/build/desktop-aot.props` | Verified: AOT publish, trim analysis, single-file diagnostics as errors, RID set |
| `eng/build/cloud-jit.props` | Verified: JIT posture explicit; AOT properties absent by design |
| `eng/build/android-aot.props` | Verified: explicit runtime selection, never inherited ([RT-02](../../architecture/11-mobile-architecture.md#rule-rt-02) in the mobile architecture) |
| `src/Web/package.json`, `package-lock.json`, `.node-version`, `.npmrc`, `ArcForges.Web.esproj` | Create the one Node/npm workspace, exact toolchain/dependency pins, portable commands and Windows adapter; remove obsolete Web WASM property imports |
| `eng/build/contracts.props` | Verified: source-generated serialization and generator settings for contract projects |
| `.editorconfig` | Analyzer severities as build policy |
| `eng/policy/dependency-policy.json` | Created: allowlist per licence boundary, preview-package rules, upgrade evidence requirements |

**Major types introduced:** none.

---

## 5. Required implementation work

<a id="rule-wp-02.00"></a>

### WP-02.00 — Pin and lock each toolchain

**What must be fully done.** Verify the .NET SDK and central NuGet pins, locked project restores and stable dependency policy. Establish the Web root manifest/lock, exact supported Node 24 LTS patch and npm version, exact generator/framework pins and reviewed JavaScript SDK. Disable implicit npm install in esproj; its explicit restore calls root npm ci once.

**Testing requirements.** Clean-cache locked .NET restore and npm ci; reject lock drift, nested npm locks and wrong engine versions; verify no accidental package overrides.

**Completion gate.** Both restored graphs are reproducible and declared; changing a lock or toolchain requires review.

<a id="rule-wp-02.01"></a>

### WP-02.01 — Diagnostic posture

**What must be fully done.** Analysis level, nullable reference types, implicit usings and deterministic build are set repository-wide. Analyzer severities are expressed in the editor configuration as build policy. Warnings-as-errors is enabled on the main path; where staged debt prevents this for a specific project, the exception is time-bounded with an owner and recorded as a waiver.

**Testing requirements.** A build with warnings-as-errors on the full solution; the waiver list is enumerated with owners and expiry dates.

**Completion gate.** The solution builds with warnings-as-errors, and every waiver has an owner and an expiry.

<a id="rule-wp-02.02"></a>

### WP-02.02 — AOT and trim declaration sweep

**What must be fully done.** Every reusable library that an AOT deliverable consumes declares AOT compatibility; every AOT host declares AOT publish. The resulting diagnostics are treated as findings, triaged, and either fixed or recorded as blocking items against the package that owns the offending code. Evaluate imports before deciding whether a declaration is missing; the baseline already supplies desktop and contract AOT properties centrally.

**Testing requirements.** A build producing the complete diagnostic set; a triage record for every diagnostic.

**Completion gate.** Every project on an AOT chain declares its posture, and every resulting diagnostic is fixed or assigned. **A suppressed diagnostic without an assignment fails this gate.**

<a id="rule-wp-02.03"></a>

### WP-02.03 — Runtime and directory boundaries

**What must be fully done.** Express desktop Native AOT, Cloud JIT and Android Mono AOT in the managed build. Create the independent Node/TS workspace and thin esproj commands; win.slnx composes it, while Cloud.csproj/ArcForges.slnx have no esproj dependency. Implement typed portable orchestration, explicit restore/health-aware dev configuration and separate account/chat development hostnames. Initial commands may target foundation shells; real SDK/runtime proof belongs to [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06).

**Testing requirements.** Evaluated .NET property assertions; inspect project references/imports; Windows esproj load/restore/build command dispatch; direct npm invocation on non-Windows; assert no duplicate dev server, implicit install or production dev proxy.

**Completion gate.** Each build graph has the correct runtime/toolchain; Windows and CLI commands share one Web implementation and portable .NET build does not evaluate esproj.

<a id="rule-wp-02.04"></a>

### WP-02.04 — Version axis plumbing

**What must be fully done.** The nine version axes are produced by the build (`§4` of the build architecture): each axis has a declared source of truth and is stamped into the appropriate artifact. Build metadata — commit, build identifier, pipeline run — is stamped into every assembly and is retrievable at runtime for support.

**Testing requirements.** A test asserting every axis is present and that no axis is derived from another; a runtime test that build metadata is retrievable from a published binary.

**Completion gate.** All nine axes are produced independently, and build metadata is retrievable from a published artifact.

<a id="rule-wp-02.05"></a>

### WP-02.05 — Dependency policy

**What must be fully done.** A dependency policy exists as data: the allowlist per licence boundary, the preview-package rule, and the evidence required for an addition or an upgrade — licence, provenance, maintenance status, transitive closure, and for AOT chains an AOT compatibility statement. The framework-upgrade re-verification obligation ([VG-08](../../assurance/open-gates-register.md#rule-vg-08)) is recorded as a recurring checklist attached to the policy.

**Testing requirements.** A policy check over the current dependency set; a dry run of the addition process for one new dependency.

**Completion gate.** The policy exists as machine-readable data, the current dependency set passes it, and the framework-upgrade checklist is recorded. **This schedules [VG-08](../../assurance/open-gates-register.md#rule-vg-08).**

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
| Clean-machine locked restore log | [WP-02.00](#rule-wp-02.00) |
| Warnings-as-errors build log plus the waiver list | [WP-02.01](#rule-wp-02.01) |
| The full AOT/trim diagnostic set with triage records | [WP-02.02](#rule-wp-02.02) |
| Evaluated-property report per target | [WP-02.03](#rule-wp-02.03) |
| Version axis report and a runtime metadata retrieval test | [WP-02.04](#rule-wp-02.04) |
| Dependency policy check report | [WP-02.05](#rule-wp-02.05) |

---

**Web evidence.** Record Node/npm/JS SDK versions, npm ci output, portable command results, esproj solution load/dispatch, and scoped policy checks. The later real React/API proof remains [WP-06.05](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.05); it is not claimed by toolchain setup.

---

## 8. Completion gate

**[VG-08](../../assurance/open-gates-register.md#rule-vg-08) evidence:** [WP-02.05](#rule-wp-02.05) — Retained framework-upgrade record and Android runtime/AOT/trim re-verification whenever the recurring trigger fires. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. Locked restore succeeds from a clean machine and no project overrides a central version.
2. The solution builds with warnings-as-errors; every waiver has an owner and an expiry.
3. Every project on an AOT chain declares its posture, and every resulting diagnostic is fixed or assigned to a named package.
4. Each target's effective runtime posture matches **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, verified from evaluated properties.
5. All nine version axes are produced independently and build metadata is retrievable from a published artifact.
6. The dependency policy exists as data, passes against the current set, and carries the framework-upgrade re-verification checklist.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [01 — Repository Reconciliation and Target Layout](01-repository-reconciliation-and-target-layout.md)

**Downstream — these consume this package’s completed output.**

- [03 — Contract Foundation and the Licence Boundary Split](03-contract-foundation-and-licence-split.md)
- [05 — Architecture and Repository Policy Test Suite](05-architecture-and-repository-policy-tests.md)
- [47 — Static Public Site](47-static-public-site.md)
