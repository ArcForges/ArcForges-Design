# Build, Packaging and Release Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (runtime and AOT matrix), **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** (target monorepo), **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** (surface inventory, update and download domains), **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)** (mobile commerce posture), `I4 §Stage 5`
> Companions: [`../requirements/10-distribution-update-and-support.md`](../requirements/10-distribution-update-and-support.md), [`../requirements/12-quality-and-compatibility-contract.md`](../requirements/12-quality-and-compatibility-contract.md), [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md)

One monorepo, many independently versioned products, one build system, and one rule that governs everything below: **the bytes a user runs are the bytes CI produced, verified end to end.**

---

## 1. Controlling rules

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Build once, promote the same artifact.** No environment or channel rebuilds from source; promotion moves artifacts and metadata, never triggers a new compile. |
| BR-02 | **Each product has an independent release lifecycle** ([DS-01](../requirements/10-distribution-update-and-support.md#rule-ds-01) in the distribution requirements). A monorepo is not a monolithic release. |
| BR-03 | **A source-hosting platform is a build and release automation platform, not the primary distribution channel** ([DS-04](../requirements/10-distribution-update-and-support.md#rule-ds-04) there). Artifacts and update feeds are served from ArcForges-controlled infrastructure. |
| BR-04 | **Release artifacts are immutable** ([DS-05](../requirements/10-distribution-update-and-support.md#rule-ds-05) there). A published version's bytes never change; a defect produces a new version, never a replaced file. |
| BR-05 | **Every artifact is signed, hashed, attested and recorded** before it can be promoted ([RC-03](../requirements/10-distribution-update-and-support.md#rule-rc-03), [RC-04](../requirements/10-distribution-update-and-support.md#rule-rc-04) there). |
| BR-06 | **The build is deterministic to the extent the toolchain allows**, and every non-determinism that remains is identified, justified and recorded rather than ignored. |
| BR-07 | **A release gate is a machine check, not a person's recollection.** Every gate in `§9` is evaluated by the pipeline and recorded in the release record. |
| BR-08 | **No secret required to produce a release is held by an individual.** Signing and publishing credentials live in the release credential store with scoped, audited access. |

---

## 2. Repository build model

### 2.1 Structure

```
Directory.Build.props / .targets      one place for language version, nullable,
                                      analysis level, deterministic build flags
Directory.Packages.props              central package version management
global.json                           pinned SDK
.editorconfig                         analyzer severity as build policy
build/                                the build orchestration entry points
```

| # | Rule |
|---|---|
| <a id="rule-bm-01"></a>BM-01 | **The SDK version is pinned** and upgrading it is a reviewed change with the full verification matrix re-run (`§22` of the quality contract). |
| BM-02 | **Central package management is mandatory.** A project never declares its own version of a shared dependency. |
| BM-03 | **Analyzer and warning policy is repository-wide**, with warnings as errors on the main path. A per-project suppression carries a justification comment and an owner. |
| BM-04 | **Trim, AOT and single-file analyzers are enabled on every project that participates in an AOT publish** (`§12` of the quality contract), and their diagnostics are build-breaking. |
| <a id="rule-bm-05"></a>BM-05 | **A build must not depend on machine state** — no globally installed tool that is not restored by the repository, no environment variable that is not declared, no network fetch outside restore. |
| <a id="rule-bm-06"></a>BM-06 | **Generated code is generated at build time, never committed**, except where a golden file is deliberately checked in as a compatibility fixture (`§6`). |
| <a id="rule-bm-07"></a>BM-07 | **The build works offline after restore**, so a transient registry outage does not stop a release. |

### 2.2 Build stages

```
restore → analyze → compile → unit test → generate contracts artifacts
   → architecture and policy tests → integration test → publish (per RID)
   → package → sign → verify → attest → record → promote
```

| # | Rule |
|---|---|
| <a id="rule-bs-01"></a>BS-01 | **Architecture tests and repository policy tests run as ordinary build stages** ([AT-01](01-solution-and-project-layout.md#rule-at-01)–[AT-14](01-solution-and-project-layout.md#rule-at-14), [RP-01](01-solution-and-project-layout.md#rule-rp-01)–[RP-10](01-solution-and-project-layout.md#rule-rp-10) in the solution layout), and a violation fails the build. |
| <a id="rule-bs-02"></a>BS-02 | **Contract artifacts — OpenAPI documents, JSON Schema, capability descriptors — are generated from the C# source of truth** (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**) and compared against the committed baseline. An undeclared contract change fails the build (`§4`). |
| BS-03 | **Publish is per runtime identifier**, and the produced output is the input to packaging; packaging never recompiles. |
| BS-04 | **Verification runs against the packaged artifact**, not against the build output directory: signature, hash, entry point, runtime posture and launch smoke test. |

---

## 3. Runtime publish matrix

| Target | Publish mode | Verification obligation |
|---|---|---|
| ArcChat, ArcNotes, ArcScope, ArcSlate desktop | **Native AOT**, self-contained (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | AOT publish succeeds with zero trim/AOT warnings; the produced binary launches without a machine-installed runtime |
| ArcForges Cloud | **ASP.NET Core JIT**, container image (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | Strict AOT is explicitly not required (**[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**); the image runs the same pipeline in every environment |
| ArcForges.Web.App | **Blazor WebAssembly**, `RunAOTCompilation=false` (**[D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007)**) | Publish succeeds; bundle size measured against budget |
| ArcForges.Web.StaticGen output | Static artifacts | Deterministic regeneration produces byte-identical output |
| ArcChat Mobile — Android | **.NET 10 Mono AOT** release build (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)**) | The runtime posture is confirmed by inspecting the produced artifact ([RT-07](11-mobile-architecture.md#rule-rt-07) in the mobile architecture); CI builds the release artifact and smoke-tests on a real device |
| ArcChat Mobile — iOS | **Architecture present, build deferred** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | Never claimed as compiled or tested; re-verified against the then-current supported baseline before activation |

| # | Rule |
|---|---|
| <a id="rule-pm-01"></a>PM-01 | **A debug build passing is never evidence for a release target.** Every AOT and mobile gate is evaluated against the release artifact ([PM-03](../requirements/12-quality-and-compatibility-contract.md#rule-pm-03) in the quality contract). |
| <a id="rule-pm-02"></a>PM-02 | **The AOT proof is continuous, not a one-off.** Every desktop product publishes AOT in CI on every main-branch build. |
| PM-03 | **A framework major upgrade re-runs the whole runtime matrix**, including the mobile AOT and trim proof ([RT-06](11-mobile-architecture.md#rule-rt-06) in the mobile architecture). |
| PM-04 | **Cloud must not be packaged as Native AOT** in an attempt to be consistent with desktop. The matrix is deliberate (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**). |

---

## 4. Versioning implementation

The nine version axes (`§14` of the quality contract) are produced by the build, not written by hand.

| Axis | Source of truth | Enforcement |
|---|---|---|
| `AppVersion` | Release input for that product | Stamped into the assembly, package and release record |
| `ContractVersion` / `ContractSet` | Contract project version files | A contract change without a version change fails [BS-02](#rule-bs-02) |
| `CapabilityVersion` | Capability descriptor declarations | Compared against the committed descriptor baseline |
| `NativeFormatVersion` | Format definition constant | A serializer change without a version change fails the format compatibility test |
| `StorageSchemaVersion` | Migration set head | Must equal the highest applied migration |
| `NativeAbiVersion` | Native library ABI constant | Verified at load ([AB-12](12-native-interop-and-media.md#rule-ab-12) in the native architecture) and asserted in CI |
| `PolicySchemaVersion` | Policy schema definition | Schema change without a version change fails validation |
| `ExtensionProtocolVersion` | Extension protocol definition | Same rule |
| `PackageVersion` | Package manifest | Validated at package build |

| # | Rule |
|---|---|
| VR-01 | **Version axes are never collapsed** ([I-383](../requirements/01-normative-glossary-and-invariants.md#rule-i-383)). A build that stamps one axis from another fails a policy test. |
| VR-02 | **Versioning is semantic**, and pre-release identifiers distinguish channel builds ([RC-02](../requirements/10-distribution-update-and-support.md#rule-rc-02) there). |
| VR-03 | **A version is allocated once.** Re-publishing a version number with different bytes is prohibited by the artifact store and by the release record. |
| VR-04 | **Build metadata — commit, build id, pipeline run, timestamp — is stamped into every artifact** and is retrievable from the running product for support (`§7.1` of the distribution requirements). |
| <a id="rule-vr-05"></a>VR-05 | **A version string presented to a store, a package manager, an update feed and a checksum file is the same string.** Divergence is a defect, because stores verify installer URLs, package managers verify hashes, and the updater must resolve historical versions (`I4 §Stage 5 §3`). |

---

## 5. Packaging

### 5.1 Install and update infrastructure

**Velopack is the baseline install and update infrastructure for the desktop products** (`I4 §Stage 5 §4`). It covers Windows, macOS and Linux with one framework, supports installers, automatic and delta updates, release channels, a self-hosted HTTP update source, downgrade and release notes.

| # | Rule |
|---|---|
| <a id="rule-pk-01"></a>PK-01 | **The packaging tool consumes the publish output directory** (`I4 §Stage 5 §5`). There is no principle conflict with Native AOT, and the installed application does not require a machine-installed .NET runtime. |
| PK-02 | **The installer never bootstraps a runtime.** Self-contained means self-contained. |
| PK-03 | **Packaging is behind a thin build-script boundary**, so the tool can be replaced without changing product code. Product code never references the update framework's types outside one update-integration component. |
| PK-04 | **The product's own update system remains authoritative across every channel** ([PL-03](../requirements/10-distribution-update-and-support.md#rule-pl-03), `UP-*` in the distribution requirements). A store or package manager delivers the same signed installer; it does not become the update mechanism (`I4 §Stage 5 §17`). |

### 5.2 Per-platform packaging

| Platform | Format | Notes |
|---|---|---|
| Windows | Signed `Setup.exe`, **per-user install** to a per-user application directory, no elevation required (`I4 §Stage 5 §7`) | A machine-wide MSI may be produced later for enterprise need; a package-manager manifest points at the same signed installer |
| Windows store listing | **Unpackaged Win32**: the same signed installer, not a repackaged container (`I4 §Stage 5 §8`) | Distribution only, **never a commerce channel** (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**) |
| macOS | Signed with a Developer ID, hardened runtime, notarised, stapled | Official-site distribution first; a store route is deferred because sandboxing conflicts with professional local-file and device workflows |
| Linux | **A single self-contained portable format as the first official format** (`I4 §Stage 5 §22`) | Additional formats later; **do not maintain many packaging formats simultaneously in the first stage** (`§24` there) |
| Android | App bundle with platform app signing, published to the official store | Consumption-only (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**); a direct download may exist but is not the primary channel |
| iOS | **Deferred** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | Packaging is designed, not built |

| # | Rule |
|---|---|
| PP-01 | **A "full suite" is an installation experience, not a packaging unit** ([DS-02](../requirements/10-distribution-update-and-support.md#rule-ds-02) there). A bootstrapper may install selected products; a single monolithic installer must never exist. |
| <a id="rule-pp-02"></a>PP-02 | **A macOS artifact is built and signed on a macOS runner** (`I4 §Stage 5 §26`). Cross-building and post-hoc signing are not substitutes. |
| PP-03 | **Every product's package identity is stable and distinct**, and is never reused between products or channels. |
| PP-04 | **The executable directory is never a user data directory** ([UP-05](../requirements/10-distribution-update-and-support.md#rule-up-05) there), and packaging must make that structurally impossible. |

---

## 6. Signing, provenance and supply chain

| # | Rule |
|---|---|
| <a id="rule-sp-01"></a>SP-01 | **All Windows executables and installers are signed and timestamped** ([PL-01](../requirements/10-distribution-update-and-support.md#rule-pl-01) there), so signatures remain valid after certificate expiry. |
| <a id="rule-sp-02"></a>SP-02 | **macOS artifacts are signed, hardened-runtime enabled, notarised and stapled** ([PL-02](../requirements/10-distribution-update-and-support.md#rule-pl-02) there); Linux artifacts carry published checksums, and repository signing where a repository is used. |
| SP-03 | **Signing happens in the pipeline against a scoped credential**, never on a developer machine. |
| SP-04 | **The signing identity and the brand identity are distinct concerns** ([PL-04](../requirements/10-distribution-update-and-support.md#rule-pl-04) there). Where a certificate displays an individual name, the product surfaces and documentation still present the brand consistently, and the discrepancy is anticipated rather than discovered at first release. |
| SP-05 | **Store developer accounts are established under the intended long-term owning identity** ([PL-05](../requirements/10-distribution-update-and-support.md#rule-pl-05) there). |
| <a id="rule-sp-06"></a>SP-06 | **An SBOM is produced for every artifact** and stored with the release record. |
| SP-07 | **Build provenance attestation is produced and published**, so an artifact can be traced to its source commit and pipeline run. |
| <a id="rule-sp-08"></a>SP-08 | **Third-party dependency licences are collected and verified against the licence boundary of the consuming project** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**), and the mobile dependency closure is verified before the first mobile artifact — the **[F-023](../assurance/open-gates-register.md#rule-f-023)** gate ([PL-06](../requirements/10-distribution-update-and-support.md#rule-pl-06) there). |
| <a id="rule-sp-09"></a>SP-09 | **Native assets are covered by the same signing, SBOM and provenance rules as managed assemblies** ([LD-05](12-native-interop-and-media.md#rule-ld-05)–[LD-07](12-native-interop-and-media.md#rule-ld-07) in the native architecture). |
| <a id="rule-sp-10"></a>SP-10 | **A dependency addition is a reviewed change** with licence, provenance, maintenance status and transitive closure recorded (`§22` of the quality contract). |

---

## 7. Artifact store, update feed and download surfaces

```
CI pipeline
   ↓ produces + signs + attests
Artifact store (immutable object storage)
   ↓ published through ArcForges-owned domains
downloads.arcforges.com      installers, checksums, signatures, SBOMs
updates.arcforges.com        update feed + delta packages
   ↓ consumed by
The product's own update system
```

| # | Rule |
|---|---|
| <a id="rule-af-01"></a>AF-01 | **Clients never hard-code an object-storage URL** ([DS-06](../requirements/10-distribution-update-and-support.md#rule-ds-06) there, **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)**). They resolve through the ArcForges-owned update domain, so storage can move without breaking installed clients. |
| <a id="rule-af-02"></a>AF-02 | **The update feed is data, not code**: a signed, versioned document describing available versions per channel, per platform, per architecture, with hashes, minimum OS versions, minimum cloud version and compatibility ranges. |
| AF-03 | **The feed can immediately stop offering a bad version** ([UP-10](../requirements/10-distribution-update-and-support.md#rule-up-10) there), and the compatibility policy can block a specific version range without blocking neighbouring versions. |
| AF-04 | **Feed changes are auditable** and carry an author, reason and timestamp. |
| AF-05 | **A public mirror of a release may exist**, but the authoritative feed is the ArcForges-owned one (`I4 §Stage 5 §2`, `§6`). |
| AF-06 | **Objects are immutable and content-addressed**; a delta package references exact source and target hashes. |
| AF-07 | **The download surface has no account gate** (`§4` of the web architecture) and remains available during a cloud incident. |

---

## 8. Update client architecture

| # | Rule |
|---|---|
| UC-01 | **Update never blocks launch** ([UP-01](../requirements/10-distribution-update-and-support.md#rule-up-01) there): discover, download and stage in the background; apply at a safe moment. |
| UC-02 | **The apply sequence is** download → verify signature and hash → stage → **atomic switch** → retain the previous launchable version ([UP-04](../requirements/10-distribution-update-and-support.md#rule-up-04) there). |
| UC-03 | **A running task or unsaved work defers the apply step** ([UP-03](../requirements/10-distribution-update-and-support.md#rule-up-03) there) rather than interrupting it. |
| UC-04 | **Rollback is reserved and tested** ([UP-06](../requirements/10-distribution-update-and-support.md#rule-up-06) there): the previous version stays launchable, subject to data-compatibility rules. |
| UC-05 | **Migration is independent of the installer** ([UP-08](../requirements/10-distribution-update-and-support.md#rule-up-08) there): installer update → application start → data compatibility check → migration, with its own recovery path, and rollback compatibility considered. |
| UC-06 | **A failed update never damages user data** ([UP-05](../requirements/10-distribution-update-and-support.md#rule-up-05) there). |
| UC-07 | **Channel switching is a user action with stated consequences** ([RC-01](../requirements/10-distribution-update-and-support.md#rule-rc-01) there), including that moving down a channel may require a data compatibility check. |
| UC-08 | **A critical security update has an expedited path** ([UP-09](../requirements/10-distribution-update-and-support.md#rule-up-09) there), coordinated with the advisory process and, where warranted, a policy kill switch — noting a kill switch reduces exposure but does not fix a local vulnerability. |
| UC-09 | **Staged rollout is supported** using the deterministic rollout mechanism of the policy architecture (`§3` of the policy requirements), so a percentage rollout is stable per installation rather than re-randomised. |
| UC-10 | **Update activity is observable**: check, download, verify, stage, apply, defer, fail and rollback are recorded with reason codes (`§2` of the observability architecture). |

---

## 9. Release gates

A release cannot be promoted to a channel until every applicable gate passes. Gate results are recorded in the release record.

| # | Gate |
|---|---|
| RG-01 | Build clean: zero errors, zero warnings-as-errors, zero suppressed AOT or trim diagnostics on the main path |
| RG-02 | Architecture tests and repository policy tests pass ([BS-01](#rule-bs-01)) |
| RG-03 | Contract baseline check passes, or the contract change is declared with a version bump and a compatibility note ([BS-02](#rule-bs-02)) |
| RG-04 | Unit, integration, contract and migration test suites pass (`§25` of the quality contract) |
| RG-05 | AOT publish succeeds for every desktop product and the artifact launches ([PM-01](#rule-pm-01), [PM-02](#rule-pm-02)) |
| RG-06 | Performance budgets met: startup, memory, responsiveness, bundle size, with the regression gate applied (`§2`–`§6` there) |
| RG-07 | Accessibility and localisation checks pass (`§10`, `§11` there) |
| RG-08 | Signing, notarisation and stapling complete and verified on the packaged artifact ([SP-01](#rule-sp-01), [SP-02](#rule-sp-02)) |
| RG-09 | SBOM, provenance attestation and licence verification present ([SP-06](#rule-sp-06)–[SP-08](#rule-sp-08)) |
| RG-10 | Update matrix verified: fresh install, upgrade, two-version upgrade, rollback, interrupted download, interrupted install, corrupted artifact rejection (`§5` of the distribution requirements) |
| RG-11 | Compatibility manifest published: minimum OS, minimum cloud version, supported client window (`§15` of the quality contract) |
| RG-12 | Release record complete and immutable ([RC-03](../requirements/10-distribution-update-and-support.md#rule-rc-03) there) |
| RG-13 | Mobile only: **[F-023](../assurance/open-gates-register.md#rule-f-023)** dependency closure and provenance audit passed ([PL-06](../requirements/10-distribution-update-and-support.md#rule-pl-06) there) |
| RG-14 | Mobile only: **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** store category fit and consumption-only conformance confirmed, and the commerce-prohibition build check passed ([MC-06](11-mobile-architecture.md#rule-mc-06) in the mobile architecture) |
| <a id="rule-rg-15"></a>RG-15 | Cloud only: migration forward and backward rehearsal passed, and the deployment is reversible (`§6.1` of the cloud product requirements) |
| RG-16 | No open severity-blocking quality issue and no expired quality waiver (`§21` there) |

---

## 10. Continuous integration topology

| # | Rule |
|---|---|
| <a id="rule-ci-01"></a>CI-01 | **Pull-request builds run the fast gates**: build, unit tests, architecture and policy tests, contract baseline check. |
| CI-02 | **Main-branch builds run the full gates** including AOT publish for every desktop product and the integration suites. |
| CI-03 | **Release builds additionally package, sign, attest and record.** |
| CI-04 | **Scheduled builds run the long gates**: soak, scale corpus, fuzzing, sanitiser builds, dependency audit, and the cross-platform matrix (`§20` there). |
| <a id="rule-ci-05"></a>CI-05 | **Platform-specific work runs on the matching platform runner** ([PP-02](#rule-pp-02)), and the matrix covers every supported platform and architecture. |
| <a id="rule-ci-06"></a>CI-06 | **A flaky test is quarantined with an owner and an expiry**, never silently retried forever. |
| CI-07 | **Pipeline definitions are versioned in the repository** and reviewed like code. |
| CI-08 | **Credentials are scoped per pipeline stage**; a test stage never holds a signing or publishing credential. |
| CI-09 | **The pipeline is reproducible from the repository.** A rebuilt pipeline on a clean runner produces the same result from the same commit. |

---

## 11. Environments and promotion

| # | Rule |
|---|---|
| <a id="rule-ep-01"></a>EP-01 | **Environments are configuration, not builds** ([BR-01](#rule-br-01)). |
| EP-02 | **Promotion order is fixed** — development → staging → production for Cloud; nightly → beta → stable for clients — and skipping a stage is an explicit, recorded exception. |
| EP-03 | **A production deployment is reversible.** A deployment whose database migration cannot be rolled back forward-only is separated into an expand phase, a deploy phase and a contract phase (`§6.1` of the cloud product requirements). |
| <a id="rule-ep-04"></a>EP-04 | **Client and cloud releases are decoupled**, and the compatibility window governs their interaction (`§15` of the quality contract). A cloud release must not require a client release on the same day. |
| <a id="rule-ep-05"></a>EP-05 | **A minimum-cloud-version requirement is imposed only after every channel has had a genuine opportunity to update**, with the grace period honoured ([UP-11](../requirements/10-distribution-update-and-support.md#rule-up-11) there). |

---

## 12. Non-goals

The build and release system is **not**: a monolithic suite installer; a second update mechanism layered on a store; a place where product code learns about the packaging tool; a route for an unsigned or unrecorded artifact to reach a user; a justification for rebuilding per environment; or a reason to collapse the nine version axes into one number.

---

## 13. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 5 §1`–`§52` | Distribution matrix, install and update infrastructure choice, per-platform packaging routes, signing obligations, channel model, version specification, release record, artifact verification, update-source ownership, update behaviour, rollback, data-migration independence and mobile distribution |
| `I3 §2`, `§19` | Runtime and AOT publish matrix, and the packaging consequences of self-contained AOT |
| `I2 §III.0`, `§III.1`, `§III.13` | Specification and rights freeze, the platform skeleton AOT proof, and the full-platform production release sequence |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)** | The publish matrix and its verification obligations |
| **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** | One monorepo with independently released products |
| **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** | Update and download domains as owned surfaces |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)**, **[F-023](../assurance/open-gates-register.md#rule-f-023)** | Mobile release gates |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**, **[F-013](../assurance/open-gates-register.md#rule-f-013)** | Licence and provenance verification in the supply chain |
