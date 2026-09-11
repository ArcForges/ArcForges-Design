# Build, Packaging and Release Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (runtime and AOT matrix), **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** (ten-repository target under [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009)), **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** (surface inventory, update and download domains), **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)** (mobile commerce posture), [distribution requirements](../requirements/10-distribution-update-and-support.md)
> Companions: [`../requirements/10-distribution-update-and-support.md`](../requirements/10-distribution-update-and-support.md), [`../requirements/12-quality-and-compatibility-contract.md`](../requirements/12-quality-and-compatibility-contract.md), [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md)

Ten independently built repositories, versioned capability packages and immutable integration artifacts, and one rule that governs everything below: **the bytes a user runs are the bytes CI produced, verified end to end.**

---

## 1. Controlling rules

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Build once, promote the same artifact.** No environment or channel rebuilds from source; promotion moves artifacts and metadata, never triggers a new compile. |
| BR-02 | **Each product has an independent release lifecycle** ([DS-01](../requirements/10-distribution-update-and-support.md#rule-ds-01) in the distribution requirements). A repository release does not force the rest of the family to rebuild. |
| BR-03 | **A source-hosting platform is a build and release automation platform, not the primary distribution channel** ([DS-04](../requirements/10-distribution-update-and-support.md#rule-ds-04) there). Artifacts and update feeds are served from ArcForges-controlled infrastructure. |
| BR-04 | **Release artifacts are immutable** ([DS-05](../requirements/10-distribution-update-and-support.md#rule-ds-05) there). A published version's bytes never change; a defect produces a new version, never a replaced file. |
| BR-05 | **Every artifact is signed, hashed, attested and recorded** before it can be promoted ([RC-03](../requirements/10-distribution-update-and-support.md#rule-rc-03), [RC-04](../requirements/10-distribution-update-and-support.md#rule-rc-04) there). |
| BR-06 | **The build is deterministic to the extent the toolchain allows**, and every non-determinism that remains is identified, justified and recorded rather than ignored. |
| BR-07 | **A release gate is a machine check, not a person's recollection.** Every gate in `§9` is evaluated by the pipeline and recorded in the release record. |
| BR-08 | **No secret required to produce a release is held by an individual.** Signing and publishing credentials live in the release credential store with scoped, audited access. |

---

## 2. Repository build model

### 2.1 Structure

The following files belong to each applicable repository root. DesktopPlatform publishes shared BuildPolicy; C# owners consume its pinned policy and retain their own SDK/package manifests. Web, AI and Mobile own independent locked npm roots. Only DesktopPlatform restores native toolchains; Contracts alone runs business proto generation.

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
| BM-02 | **NuGet uses central management; Web uses exact npm pins and one package-lock.json.** Node/npm and the JavaScript SDK are independently pinned; no business project invents a package version. |
| BM-03 | **Compiler/analyzer policy applies per language:** .NET warnings/AOT diagnostics and TS strict typechecking/lint/import boundaries, with owned time-bounded exceptions. |
| BM-04 | **Trim, AOT and single-file analyzers are enabled on every project that participates in an AOT publish** (`§12` of the quality contract), and their diagnostics are build-breaking. |
| <a id="rule-bm-05"></a>BM-05 | **A build must not depend on machine state** — no globally installed tool that is not restored by the repository, no environment variable that is not declared, no network fetch outside restore. |
| <a id="rule-bm-06"></a>BM-06 | Handwritten proto is committed in Contracts. Generated C#/TS source is built and packaged; descriptor sets, HTTP-exception schema and independent vectors are committed compatibility fixtures. Consumers restore pinned packages and never regenerate business schemas from their own handlers. |
| <a id="rule-bm-07"></a>BM-07 | **The build works offline after restore**, so a transient registry outage does not stop a release. |

### 2.1.1 Web entry points and release artifacts

[Web toolchain and SDK](25-web-toolchain-and-sdk.md) defines the exact directory/command contract. Each repository has its own solution/build entry. Web win.slnx contains its esproj; DesktopPlatform alone composes CMake/native builds. The portable managed graph excludes esproj; non-Windows Web work runs npm from ArcForges-Web root, independently of CMake. JS SDK restore invokes root npm ci explicitly and Build never silently installs. Node runs only build/dev/test work; production assets are static artifacts served by the edge, and Cloud remains the C# host.

CI retains generated descriptor/schema fingerprints, Node/npm and lock versions, generated SDK provenance, browser/visual reports and an npm-aware SBOM. Changed proto descriptors/HTTP exception schemas trigger both native and TS compatibility checks. The full solution's C# test pass is insufficient for Web. Existing Windows VS/native hooks and cross-platform CMake jobs retain separate obligations.


### 2.2 Build stages

```
locked restores (.NET/native/npm) → proto compilation and descriptor export
   → contract compatibility diff → TS SDK/event generation → language checks/tests
   → architecture/policy → production .NET/native/Web builds → integration/browser tests
   → package → sign → verify → attest → record → promote
```

| # | Rule |
|---|---|
| <a id="rule-bs-01"></a>BS-01 | **Architecture tests and repository policy tests run as ordinary build stages** ([AT-01](01-solution-and-project-layout.md#rule-at-01)–[AT-14](01-solution-and-project-layout.md#rule-at-14), [RP-01](01-solution-and-project-layout.md#rule-rp-01)–[RP-10](01-solution-and-project-layout.md#rule-rp-10) in the solution layout), and a violation fails the build. |
| <a id="rule-bs-02"></a>BS-02 | **Contract artifacts — Proto descriptors, HTTP-exception schemas and capability descriptors — are generated from the handwritten proto source of truth** (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**) and compared against the committed baseline. An undeclared contract change fails the build (`§4`). |
| BS-03 | **Publish is per runtime identifier**, and the produced output is the input to packaging; packaging never recompiles. |
| BS-04 | **Verification runs against the packaged artifact**, not against the build output directory: signature, hash, entry point, runtime posture and launch smoke test. |

---

## 3. Runtime publish matrix

| Target | Publish mode | Verification obligation |
|---|---|---|
| ArcChat, ArcNotes, ArcScope, ArcSlate desktop | **Native AOT**, self-contained (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | AOT publish succeeds with zero trim/AOT warnings; the produced binary launches without a machine-installed runtime |
| ArcForges Cloud | **ASP.NET Core Native AOT**, container image (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | Native AOT publish and real-adapter verification are mandatory (**[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**); the image runs the same pipeline in every environment |
| ArcForges.Web.App | **React/TypeScript browser assets**, Node/npm production build ([P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008)) | Account/Chat profile artifacts, generated SDK round trip, browser/CSP/visual/bundle evidence |
| ArcForges.Web.Site output | React/TS build-time pre-rendered static artifacts | No-script content, deterministic build, locale/SEO/accessibility and performance |
| ArcChat Mobile — Android | **React Native/Hermes** release build (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)**) | The runtime posture is confirmed by inspecting the produced artifact ([RT-07](11-mobile-architecture.md#rule-rt-07) in the mobile architecture); CI builds the release artifact and smoke-tests on a real device |
| ArcChat Mobile — iOS | **Architecture present, build deferred** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | Never claimed as compiled or tested; re-verified against the then-current supported baseline before activation |

| # | Rule |
|---|---|
| <a id="rule-pm-01"></a>PM-01 | **A debug build passing is never evidence for a release target.** Every AOT and mobile gate is evaluated against the release artifact ([PM-03](../requirements/12-quality-and-compatibility-contract.md#rule-pm-03) in the quality contract). |
| <a id="rule-pm-02"></a>PM-02 | Every desktop product and the Cloud business host continuously publish Native AOT against their actual changed dependency closure; a previous passing artifact cannot certify a new dependency. |
| PM-03 | **A framework major upgrade re-runs the whole runtime matrix**, including the RN/Hermes native-module and transport proof ([RT-06](11-mobile-architecture.md#rule-rt-06) in the mobile architecture). |
| PM-04 | The C# Cloud host must publish Native AOT with the full selected adapter closure. The CF Worker is a separate TypeScript deployment; it creates no C# JIT exception. |

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
| <a id="rule-vr-05"></a>VR-05 | **A version string presented to a store, a package manager, an update feed and a checksum file is the same string.** Divergence is a defect, because stores verify installer URLs, package managers verify hashes, and the updater must resolve historical versions. |

---

## 5. Packaging

### 5.1 Install and update infrastructure

**Velopack is the baseline install and update infrastructure for the desktop products** under [P2-001](../decisions/phase-2-specification-decisions.md#rule-p2-001). It covers Windows, macOS and Linux with one framework, supports installers, automatic and delta updates, release channels, a self-hosted HTTP update source, downgrade and release notes.

| # | Rule |
|---|---|
| <a id="rule-pk-01"></a>PK-01 | **The packaging tool consumes the publish output directory**. There is no principle conflict with Native AOT, and the installed application does not require a machine-installed.NET runtime. |
| PK-02 | **The installer never bootstraps a runtime.** Self-contained means self-contained. |
| PK-03 | **Packaging is behind a thin build-script boundary**, so the tool can be replaced without changing product code. Product code never references the update framework's types outside one update-integration component. |
| PK-04 | **The product's own update system remains authoritative across every channel** ([PL-03](../requirements/10-distribution-update-and-support.md#rule-pl-03), `UP-*` in the distribution requirements). A store or package manager delivers the same signed installer; it does not become the update mechanism. |

### 5.2 Per-platform packaging

| Platform | Format | Notes |
|---|---|---|
| Windows | Signed `Setup.exe`, **per-user install** to a per-user application directory, no elevation required | A machine-wide MSI may be produced later for enterprise need; a package-manager manifest points at the same signed installer |
| Windows store listing | **Unpackaged Win32**: the same signed installer, not a repackaged container | Distribution only, **never a commerce channel** (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**) |
| macOS | Signed with a Developer ID, hardened runtime, notarised, stapled | Official-site distribution first; a store route is deferred because sandboxing conflicts with professional local-file and device workflows |
| Linux | **A single self-contained portable format as the first official format** | Additional formats later; **do not maintain many packaging formats simultaneously in the first stage** |
| Android | App bundle with platform app signing, published to the official store | Consumption-only (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**); a direct download may exist but is not the primary channel |
| iOS | **Deferred** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | Packaging is designed, not built |

| # | Rule |
|---|---|
| PP-01 | **A "full suite" is an installation experience, not a packaging unit** ([DS-02](../requirements/10-distribution-update-and-support.md#rule-ds-02) there). A bootstrapper may install selected products; a single monolithic installer must never exist. |
| <a id="rule-pp-02"></a>PP-02 | **A macOS artifact is built and signed on a macOS runner**. Cross-building and post-hoc signing are not substitutes. |
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
| AF-05 | **A public mirror of a release may exist**, but the authoritative feed is the ArcForges-owned one. |
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
| CI-02 | **Each main build runs the full gates for its owned artifact and changed dependency closure.** Cross-repository CI restores published candidates by immutable identity; the family integration manifest records downstream checks without rebuilding unrelated sources. WP50 closes the full product matrix. |
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

| Current document | Relationship |
|---|---|
| [Distribution, Update, Support and Trust & Safety Requirements](../requirements/10-distribution-update-and-support.md) | Owns signing, channels, release records, packaging and update behavior |
| [Product Quality and Compatibility Contract](../requirements/12-quality-and-compatibility-contract.md) | Owns the runtime and release evidence matrix |
| [Deployment and Release Execution](22-deployment-and-release-execution.md) | Defines publication, promotion, rollback and compatibility procedures |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)** | The publish matrix and its verification obligations |
| **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** | Ten independently built repositories integrated through versioned packages and immutable artifacts |
| **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** | Update and download domains as owned surfaces |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)**, **[F-023](../assurance/open-gates-register.md#rule-f-023)** | Mobile release gates |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**, **[F-013](../assurance/open-gates-register.md#rule-f-013)** | Licence and provenance verification in the supply chain |

## 14. Independent producer and consumer artifact gates

Cloud owns deploy/integration-manifest.v1.json with schemaVersion1, manifestId, sourceCommits{repo:sha}, packages[{id,version,sha256,license,rid?}], contracts[{package,major,descriptorSha256}], cloudImage:{registry:"ghcr.io/arcforges/cloud",digest,rid:"linux-x64"}, worker:{name,versionId,sourceSha,compatibilityDate:"2026-09-11",migrationTag}, web:{profile,artifactHash,configSchema}, database:{engine:"18.6",migrationFrom,migrationTo,rollbackFloor}, configVersion, testEvidence[{scenario,artifactHash,result}], createdAt, signer, signature. Cloud OCI and release executables published on GHCR/GitHub releases; Worker4.131.0 Wrangler, fixed compatibility date. IDs/digests come from actual build/deploy, never placeholders considered proof.

Per-repo locked restore/build/mock tests → immutable producer candidate → consumer candidate restore/AOT/Hermes/browser tests → isolated real C#/PG/CF/R2 deployment → exact manifest integration suite → approve/promote same bytes. Fork/untrusted PR code gets no deployment secrets; trusted CI promotes reviewed commit with short-lived credentials and dedicated test realm/service account, unique resources,24h cleanup TTL. Workers require a public TLS test C# endpoint reachable from CF, not runnerlocalhost. Test artifacts use no real customer content. No submodules/latest/floating branch fixtures.

Rolling upgrade: expand DB/internal/public read schemas → backfill from watermark → deploy C# dual readers → deploy compatible Worker (old workflows drain on their pinned worker version) → canary/soak ≥24h → activate config reader head → clients independently update within supported window → contract only after all old workflows drained and rollback horizon closed. Incompatible Worker code is a new workflow class/migration tag; no hot reinterpretation of checkpoints. Rollback before contract restores prior image/Worker/config/assets; after destructive contraction use verified forward repair or fresh-environment restore, not blind old binary startup. Selfhost operator supplies own CF resources/AWS disaster copy/DB/secrets/origins/realm, same one-host architecture.

Use [the CF/object recovery contract](contracts/05-cloudflare-integration.md#6-r2-lifecycle-and-independent-recovery) for the independent S3 COMPLIANCE 30-day backup, WAL/base backup/object manifests and recovery generation. Observability join request/task/run/attempt/outbox IDs over W3C traceparent across C#/Worker/device with redaction; expose CF dispatch lag/unknown attempts/R2 transfer failures/backup lag/lease conflicts. CF/R2 outage leaves hydrated desktop editing/acquisition/rendering usable within existing per-product offline rules; AI pauses/fails with durable reasons and support/export stay truthful. Full recovery tested after WP46+52 and before 50.

## Producer bootstrap and candidate manifests

Before a complete Cloud exists, each producer publishes a candidate manifest with source commit, artifact hashes, exact Contracts/Platform dependencies, RID/runtime and evidence. WP02 supplies this format/pipeline, WP03 publishes schemas and WP06 composes the first foundation integration manifest in ArcForges-Cloud. Early packages may consume this manifest without depending on later business features. WP21 and later packages extend it with real owner behavior; WP50 requires the final complete manifest. No package is required to restore an artifact that its own current step has not yet produced.

## Immutable candidate publication

Allocate the actual NuGet/npm/product version before compilation and signing. A candidate channel is an access/promotion state, not a version suffix that can later be renamed. Promoting version 1.0.0 moves the same 1.0.0 bytes and attestation from private candidate to the approved channel. An artifact compiled as 1.0.0-ci.42 retains that version permanently; a 1.0.0 build is a new candidate requiring its own checks. Mutable tags are pointers only; restore and integration manifests bind version plus hash. Bootstrap stages and partial versus full manifest closure are fixed in [planning](../planning/README.md#staged-artifact-integration).
