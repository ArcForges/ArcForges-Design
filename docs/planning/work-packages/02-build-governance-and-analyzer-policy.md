<a id="rule-wp-02"></a>

# WP-02 — Build Governance, Packaging Policy and Analyzers

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Upstream: `01` · Downstream: `03`, `05`, `47`

> **Goal.** Make the build tell the truth. Until diagnostics are real, warnings are errors, versions are locked and the runtime split is expressed in the build itself, every later AOT proof and every later quality claim rests on unverified ground.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Platform, Contracts, each consumer. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** Repository-wide build properties, central package management with locked restore, analyzer and diagnostic policy, the AOT/trim/single-file diagnostic posture, the per-target runtime property sets, deterministic build configuration, and the build stage ordering.

**Out of scope.** Final product/store signing and public promotion belong to WP50. This package implements candidate publication/signing metadata mechanisms and BuildPolicy packaging; actual Contracts/native capability producers are WP03/06. Policy test implementations belong to WP05.

**Why this package exists.** The corrected inventory records central desktop/contracts AOT imports and 165 committed per-project NuGet lockfiles. Validate evaluated properties and locked restore, repair uncovered AOT chains, and establish the accepted Web toolchain; file-local absence is not an effective-property defect.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

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
| BR-06 | **Desktop is Native AOT; Cloud is ASP.NET Core Native AOT; Android is RN/Hermes; Web is React/TypeScript built by Node/npm.** No esproj or TS package inherits .NET runtime properties ([P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008)). |
| BR-07 | The Cloud host must publish Native AOT using the complete selected adapter/dependency closure; zero trim/AOT diagnostics and the activated [VG-06](../../assurance/open-gates-register.md#rule-vg-06) gate apply. |
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
| `eng/build/cloud-aot.props` | Create: PublishAot enabled and AOT/trim diagnostics treated as errors |
| `ArcForges-Mobile/android/gradle.properties` | Selected RN/Hermes/New Architecture settings plus native template locks ([RT-02](../../architecture/11-mobile-architecture.md#rule-rt-02) in the mobile architecture) |
| `src/Web/package.json`, `package-lock.json`, `.node-version`, `.npmrc`, `ArcForges.Web.esproj` | Create the one Node/npm workspace, exact toolchain/dependency pins, portable commands and Windows adapter; remove obsolete Web WASM property imports |
| `eng/build/contracts.props` | Verified: source-generated serialization and generator settings for contract projects |
| `.editorconfig` | Analyzer severities as build policy |
| `eng/policy/dependency-policy.json` | Created: allowlist per licence boundary, preview-package rules, upgrade evidence requirements |

**Major types introduced:** none.

---

## 5. Required implementation work

<a id="rule-wp-02.00"></a>

### WP-02.00 — Pin and lock each toolchain


**What must be fully done.** Pin the exact toolchain/package versions in the platform matrix: each .NET owner has SDK/central NuGet/locked restore; each TS owner has Node/npm and one root package-lock; DesktopPlatform has the same vcpkg baseline/overlays in local and CI. Contracts owns protoc/generator pins and generated package metadata. Web esproj delegates to its own npm commands without implicit restore.

**Testing requirements.** Clean isolated restores and offline repeat from fetched caches; altered lock/baseline or floating dependency fails.

**Completion gate.** Every selected toolchain is reproducible from committed pins with no dependency on sibling checkout state.

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


**What must be fully done.** Apply Native AOT/analyzer settings to desktop and the Cloud host. Build Web and AI with their selected TS commands and Mobile through its RN/Gradle template; mobile runtime settings never enter MSBuild. Use owner-local solution/IDE entry points and typed portable tooling; local orchestration consumes exact producer artifacts in the integration manifest.

**Testing requirements.** Run Windows IDE delegation and supported non-Windows CLI commands; verify Cloud never builds Web/Mobile/native targets and each product builds without another product source.

**Completion gate.** Runtime and build entry points match the fixed repository graph and produce foundation candidates for WP06.

<a id="rule-wp-02.04"></a>

### WP-02.04 — Version axis plumbing

**What must be fully done.** The nine version axes are produced by the build (`§4` of the build architecture): each axis has a declared source of truth and is stamped into the appropriate artifact. Build metadata — commit, build identifier, pipeline run — is stamped into every assembly and is retrievable at runtime for support.

**Testing requirements.** A test asserting every axis is present and that no axis is derived from another; a runtime test that build metadata is retrievable from a published binary.

**Completion gate.** All nine axes are produced independently, and build metadata is retrievable from a published artifact.

<a id="rule-wp-02.05"></a>

### WP-02.05 — Dependency policy


**What must be fully done.** Encode the selected licence/import and dependency-admission rules as owner policy data, including exact source hashes, generated public/internal separation, native gates and the framework-upgrade re-verification obligation. Configure candidate/stable package feeds and restricted publisher credentials, immutable versions and checksum/signature verification.

**Testing requirements.** Negative forbidden-license, floating-tag, mutable-version and wrong-publisher fixtures; actual tooling-package publication/restore round trip. Generated Contracts and runtime consumers follow WP03/WP06.

**Completion gate.** Publication mechanisms and dependency policies are usable before consumer work; production release remains WP50.

<a id="rule-wp-02.90"></a>
### WP-02.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Apply pinned per-toolchain build/lock/analyzer settings, shared workflow/tooling consumption, native module build/pack pipeline and candidate feeds, npm schema publication pipeline and OCI/Worker artifact metadata. Align local/CI vcpkg inputs. Publication mechanisms arrive here; final product release remains WP-50.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Selected pins and licence/AOT policy agree across owners; the BuildPolicy produces an identifiable candidate and the native pack pipeline is configured; real native capability proof is WP06; consumers need no CMake/vcpkg for ordinary restore.

**Completion gate.** Selected pins and licence/AOT policy agree across owners; the BuildPolicy produces an identifiable candidate and the native pack pipeline is configured; real native capability proof is WP06; consumers need no CMake/vcpkg for ordinary restore. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-02.90](#rule-wp-02.90) and all inherited domain-specific gates must pass on the same candidate closure. Selected pins and licence/AOT policy agree across owners; the BuildPolicy produces an identifiable candidate and the native pack pipeline is configured; real native capability proof is WP06; consumers need no CMake/vcpkg for ordinary restore.

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

- [WP-01](01-repository-reconciliation-and-target-layout.md#rule-wp-01)

**Downstream — consumers of these released outputs.**

- [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03)
- [WP-05](05-architecture-and-repository-policy-tests.md#rule-wp-05)
- [WP-47](47-static-public-site.md#rule-wp-47)


---
