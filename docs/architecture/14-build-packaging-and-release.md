# Build, Packaging and Release Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021)** (C#-first build, packaging and publication), **[P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)** (PDF retirement), **[P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)** (macOS out of scope), **[P2-024](../decisions/phase-2-specification-decisions.md#rule-p2-024)** (WSL2 Linux validation), **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (runtime and AOT matrix), **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** (seven-repository target under [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) and [P2-019](../decisions/phase-2-specification-decisions.md#rule-p2-019)), **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** (surface inventory, update and download domains), **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)** (mobile commerce posture), [distribution requirements](../requirements/10-distribution-update-and-support.md)
> Companions: [`../requirements/10-distribution-update-and-support.md`](../requirements/10-distribution-update-and-support.md), [`../requirements/12-quality-and-compatibility-contract.md`](../requirements/12-quality-and-compatibility-contract.md), [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md)

Seven independent implementation repositories (ArcForges-AI among them, kept as read-only history once its last deployment is retired, [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 5) plus the Design authority, versioned capability packages and immutable integration artifacts, and one rule that governs everything below: **promote the original built candidate with its source and signing identity.** Execution follows [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017) and the [CI/local policy](../assurance/ci-and-local-validation-policy.md); runtime scenarios are local opt-in. Linux runtime checks run once, affected-scope, in the local WSL2 Debian distribution ([P2-024](../decisions/phase-2-specification-decisions.md#rule-p2-024)). macOS is out of scope ([P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)): no macOS build, artifact, signing or CI exists, and macOS CI is prohibited.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Build once, promote the same artifact.** No environment or channel rebuilds from source; promotion moves artifacts and metadata, never triggers a new compile. |
| <a id="rule-br-02"></a>BR-02 | **Each product has an independent release lifecycle** ([DS-01](../requirements/10-distribution-update-and-support.md#rule-ds-01) in the distribution requirements). A repository release does not force the rest of the family to rebuild. |
| <a id="rule-br-03"></a>BR-03 | **A source-hosting platform is a build and release automation platform, not the primary distribution channel** ([DS-04](../requirements/10-distribution-update-and-support.md#rule-ds-04) there). Artifacts and update feeds are served from ArcForges-controlled infrastructure. |
| <a id="rule-br-04"></a>BR-04 | **Release artifacts are immutable** ([DS-05](../requirements/10-distribution-update-and-support.md#rule-ds-05) there). A published version's bytes never change; a defect produces a new version, never a replaced file. |
| <a id="rule-br-05"></a>BR-05 | **Every artifact is signed, hashed, attested and recorded** before it can be promoted ([RC-03](../requirements/10-distribution-update-and-support.md#rule-rc-03), [RC-04](../requirements/10-distribution-update-and-support.md#rule-rc-04) there). |
| <a id="rule-br-06"></a>BR-06 | **The build is deterministic to the extent the toolchain allows**, and every non-determinism that remains is identified, justified and recorded rather than ignored. |
| <a id="rule-br-07"></a>BR-07 | **Record the checks actually performed.** The reduced CI set is machine-checked; relevant local runtime evidence is recorded separately and never fabricated from build success. |
| <a id="rule-br-08"></a>BR-08 | **No secret required to produce a release is held by an individual.** Signing and publishing credentials live in the release credential store with scoped, audited access. |

---

## 2. Repository build model

### 2.1 Structure

The following files belong to each applicable repository root. DesktopPlatform publishes shared BuildPolicy; C# owners consume its pinned policy and retain their own SDK/package manifests. Contracts, Cloud and Web own independent NuGet lock files (`packages.lock.json`). The npm roots kept are: the Node build and deploy tooling for wrangler (Web and the Cloud Worker adapter); the Cloud D1 migration runner and generators, which move to C# under [CLOUD.84](../planning/delivery/lanes/cloud.md#task-cloud-84) and make no business decision until then ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021), items 1 and 6); and the retained `@arcforges/ai-internal` pipeline, which Contracts owns as its producer and Cloud's Worker binding adapters consume as a pinned package ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021), item 4; [CON.40](../planning/delivery/lanes/contracts.md#task-con-40)). Every retained npm root has its own committed lock. Mobile owns its NuGet locks. Only DesktopPlatform restores native toolchains; Contracts alone runs business proto generation. Python build tooling (provenance, licence, packaging and policy scripts) stays build tooling and is not product logic ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 1).

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
| <a id="rule-bm-02"></a>BM-02 | **NuGet uses central management and committed `packages.lock.json` locks in every repository.** Each retained npm root has its own committed lock: the wrangler tooling for Web and for the Cloud Worker adapter, the Cloud D1 migration runner and generators until [CLOUD.84](../planning/delivery/lanes/cloud.md#task-cloud-84) moves them to C#, and the Contracts-owned `@arcforges/ai-internal` pipeline consumed by Cloud's Worker binding adapters. Node/npm is pinned independently; no business project invents a package version. |
| <a id="rule-bm-03"></a>BM-03 | **Compiler/analyzer policy applies per language:** .NET warnings, AOT and trim diagnostics, Blazor and MAUI analyzer policy, and TypeScript strict typechecking, lint and the import/dependency-boundary rule for the retained thin Cloudflare adapters and `@arcforges/ai-internal`, with owned time-bounded exceptions. The boundary rule keeps business logic out of the TypeScript adapters ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 1). |
| <a id="rule-bm-04"></a>BM-04 | **Trim, AOT and single-file analyzers are enabled on every project that participates in an AOT publish** (`§12` of the quality contract), and their diagnostics are build-breaking. |
| <a id="rule-bm-05"></a>BM-05 | **A build must not depend on machine state** — no globally installed tool that is not restored by the repository, no environment variable that is not declared, no network fetch outside restore. |
| <a id="rule-bm-06"></a>BM-06 | Handwritten proto is committed in Contracts. Generated C# source is built and packaged (plus the retained `ai-internal` TypeScript codec); descriptor sets, HTTP-exception schema and independent vectors are committed compatibility fixtures. Consumers restore pinned packages and never regenerate business schemas from their own handlers. |
| <a id="rule-bm-07"></a>BM-07 | **The build works offline after restore**, so a transient registry outage does not stop a release. |

### 2.1.1 Web entry points and release artifacts

[Web toolchain and SDK](25-web-toolchain-and-sdk.md) defines the exact directory/command contract; its React-era text is a pending correction (WTS-01 and WTS-02 of the [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) pending-correction table) and is not cited as current for the Blazor build. Each repository has its own solution/build entry. Web `win.slnx` contains the Blazor profiles, the Razor Class Library, the C# static Site generator and the test projects. DesktopPlatform alone composes CMake/native builds. Web's managed graph is portable: `dotnet` restore, build and test run from the ArcForges-Web root independently of CMake. Restore uses the locked NuGet packages, and Build never silently fetches packages. Node runs only the wrangler deploy tooling; the `@arcforges/ai-internal` build is a Contracts pipeline and is not a Web input. Production assets are static artifacts (Blazor publish output and generated Site pages) served by the edge, and Cloud remains the C# host.

CI retains generated descriptor/schema fingerprints, .NET SDK and NuGet lock versions, Node/npm lock versions for every retained npm root, generated SDK provenance, and an npm-aware SBOM and licence closure covering the NuGet closure and the npm closure of the Worker bundles and `ai-internal`; relevant local browser/visual reports (Microsoft.Playwright for .NET, local opt-in) are separate evidence. Changed proto descriptors/HTTP exception schemas trigger the native and C# compatibility checks, and the `@arcforges/ai-internal` TypeScript codec check runs in Contracts while that package exists. The full solution's C# test pass is insufficient for Web, so the Blazor/bUnit and static Site determinism checks run as their own stages. Windows IDE/native runtime checks are explicit local opt-in; Git hooks do not trigger heavy builds. Required Windows/Linux CMake compilation remains separate.


### 2.2 Build stages

```
locked restores (.NET/native; npm only for retained tooling) → proto compilation and descriptor export
   → contract compatibility diff → C# SDK/event generation → language checks/tests (xUnit, bUnit)
   → architecture/policy → Windows/Linux production .NET/native builds (Cloud and desktop Native AOT, Blazor publish, Site generation, MAUI Android)
   → package → sign → verify → attest → record → promote
```

| # | Rule |
|---|---|
| <a id="rule-bs-01"></a>BS-01 | **Architecture tests and repository policy tests run as ordinary build stages** ([AT-01](01-solution-and-project-layout.md#rule-at-01)–[AT-14](01-solution-and-project-layout.md#rule-at-14), [RP-01](01-solution-and-project-layout.md#rule-rp-01)–[RP-10](01-solution-and-project-layout.md#rule-rp-10) in the solution layout), and a violation fails the build. |
| <a id="rule-bs-02"></a>BS-02 | **Contract artifacts — Proto descriptors, HTTP-exception schemas and capability descriptors — are generated from the handwritten proto source of truth** (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**) and compared against the committed baseline. An undeclared contract change fails the build (`§4`). |
| <a id="rule-bs-03"></a>BS-03 | **Publish is per runtime identifier**, and the produced output is the input to packaging; packaging never recompiles. |
| <a id="rule-bs-04"></a>BS-04 | **Check candidate identity at promotion.** Required signatures, source/version identity and licence provenance remain; no automated launch smoke or repeated public archive download. |

---

## 3. Runtime publish matrix

| Target | Publish mode | Verification obligation |
|---|---|---|
| ArcScope desktop with its embedded assistant | **Native AOT**, self-contained (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | AOT publish succeeds with zero trim/AOT warnings; the produced binary launches without a machine-installed runtime; Linux runtime evidence is local, in WSL2 Debian ([P2-024](../decisions/phase-2-specification-decisions.md#rule-p2-024)) |
| ArcForges Cloud | **ASP.NET Core Native AOT**, container image (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | Native AOT compilation is required, and the C# Harness is part of the same publish ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021)); real-adapter runtime verification is scoped local opt-in (**[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**); the image runs the same pipeline in every environment |
| ArcForges.Web.App | **Blazor WebAssembly static assets**, `dotnet publish` IL build (`RunAOTCompilation=false`; WASM AOT only on a measured benchmark) ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021)) | Account, Chat and Operations profile artifacts, generated C# SDK round trip, exact CSP token set, browser/visual/bundle evidence ([PRF.11](../planning/delivery/lanes/runtime-proofs.md#task-prf-11)) |
| ArcForges.Web.Site output | **C# static Site generator** (Razor `HtmlRenderer`; proof pending under [PRF.11](../planning/delivery/lanes/runtime-proofs.md#task-prf-11)) build-time static HTML artifacts | No-script content, deterministic build (not claimed until PRF.11 proves it), locale/SEO/accessibility and the public p75 performance targets |
| ArcChat Mobile — Android | **.NET MAUI `net10.0-android` release build** with Mono AOT, trimming and R8 ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021); the Android gate of **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)**) | The runtime posture is confirmed by inspecting the produced artifact ([RT-07](11-mobile-architecture.md#rule-rt-07) in the mobile architecture); CI builds the release artifact (APK and AAB); the release checks re-proven for the MAUI closure ([PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12), [AND.40](../planning/delivery/lanes/android.md#task-and-40)) are minified release (trimming plus R8), 16 KB page-size alignment of the release native libraries, signed APK and AAB, licence and provenance closure ([F-023](../assurance/open-gates-register.md#rule-f-023)) and the F-023-class closure checks ([11 Android publication](11-mobile-architecture.md#android-publication-and-rescue)); device/runtime checks are scoped local opt-in under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017) |

The desktop RID set is `win-x64`, `win-arm64` and `linux-x64` ([P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023) item 1). `linux-arm64` is not added and is not claimed, and no macOS RID exists.

| # | Rule |
|---|---|
| <a id="rule-pm-01"></a>PM-01 | **A debug build passing is never evidence for a release target.** Every AOT and mobile gate is evaluated against the release artifact ([PM-03](../requirements/12-quality-and-compatibility-contract.md#rule-pm-03) in the quality contract). |
| <a id="rule-pm-02"></a>PM-02 | The ArcScope desktop application and the Cloud business host continuously publish Native AOT against their actual changed dependency closure; a previous passing artifact cannot certify a new dependency. |
| <a id="rule-pm-03"></a>PM-03 | **A framework major upgrade re-runs the whole runtime matrix**, including the .NET MAUI Android Mono AOT, trimming/R8 and gRPC-Web transport proof ([RT-06](11-mobile-architecture.md#rule-rt-06) in the mobile architecture). |
| <a id="rule-pm-04"></a>PM-04 | The C# Cloud host must publish Native AOT with the full selected adapter closure. The CF Worker is a separate thin TypeScript platform-adapter deployment with no business logic; it creates no C# JIT exception ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021)). |

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
| `NativeAbiVersion` | Native library ABI constant | Verified by product load-time checks ([AB-12](12-native-interop-and-media.md#rule-ab-12)) and build-source/metadata checks; runtime probes are local opt-in |
| `PolicySchemaVersion` | Policy schema definition | Schema change without a version change fails validation |
| `ExtensionProtocolVersion` | Extension protocol definition | Same rule |
| `PackageVersion` | Package manifest | Validated at package build |

| # | Rule |
|---|---|
| <a id="rule-vr-01"></a>VR-01 | **Version axes are never collapsed** ([I-383](../requirements/01-normative-glossary-and-invariants.md#rule-i-383)). A build that stamps one axis from another fails a policy test. |
| <a id="rule-vr-02"></a>VR-02 | **Versioning is semantic**, and pre-release identifiers distinguish channel builds ([RC-02](../requirements/10-distribution-update-and-support.md#rule-rc-02) there). |
| <a id="rule-vr-03"></a>VR-03 | **A version is allocated once.** Re-publishing a version number with different bytes is prohibited by the artifact store and by the release record. |
| <a id="rule-vr-04"></a>VR-04 | **Build metadata — commit, build id, pipeline run, timestamp — is stamped into every artifact** and is retrievable from the running product for support (`§7.1` of the distribution requirements). |
| <a id="rule-vr-05"></a>VR-05 | **A version string presented to a store, a package manager, an update feed and a checksum file is the same string.** Divergence is a defect, because stores verify installer URLs, package managers verify hashes, and the updater must resolve historical versions. |

---

### 4.1 Foundation applicability and support identity

The [WP02.04 version identity profile](../assurance/wp02-04-version-identity-profile.md) defines the complete foundation report and ordered implementation. Every candidate reports all nine axes from independent source kinds. The PackageVersion axis is the exact dependency package inventory; an artifact's own distribution version is separately recorded. Contract/profile identity comes from its authored or restored descriptor provenance, never from a NuGet or npm release number.

An axis with no implementation at the current producer stage records not-applicable or not-produced, its reason and, for a later producer, the owning step. It must not invent version 1 or claim future capability/format/storage/policy/extension support. Independent source-resolution tests cover all nine axes; actual candidate values come only from actual inputs. This supplies build plumbing without replacing the later typed axes, business compatibility or complete integration manifest.

Owned assemblies and runtime artifacts retain source/build/pipeline identity. Third-party and already-published dependency bytes remain unchanged and are inventoried separately. The stamped timestamp is explicitly the source commit's UTC timestamp for deterministic reproduction; actual execution times remain in the referenced pipeline record. Runtime retrieval reads compiled/sealed metadata, never the current process environment. Publication rejects local, dirty, incomplete or mismatched identities.

---

## 5. Packaging

### 5.1 Install and update infrastructure

**Velopack is the baseline install and update infrastructure for the desktop application** under [P2-001](../decisions/phase-2-specification-decisions.md#rule-p2-001). It covers Windows and Linux with one framework (macOS is out of scope under [P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)), supports installers, automatic and delta updates, release channels, a self-hosted HTTP update source, downgrade and release notes.

| # | Rule |
|---|---|
| <a id="rule-pk-01"></a>PK-01 | **The packaging tool consumes the publish output directory**. There is no principle conflict with Native AOT, and the installed application does not require a machine-installed .NET runtime. |
| <a id="rule-pk-02"></a>PK-02 | **The installer never bootstraps a runtime.** Self-contained means self-contained. |
| <a id="rule-pk-03"></a>PK-03 | **Packaging is behind a thin build-script boundary**, so the tool can be replaced without changing product code. Product code never references the update framework's types outside one update-integration component. |
| <a id="rule-pk-04"></a>PK-04 | Desktop channels deliver the same signed installer under the product updater. Android follows the declared APK/Play distribution channel, stable signing lineage and monotonic versionCode in Mobile architecture; installer/feed rules cannot override Android package-manager/store authority. |

### 5.2 Per-platform packaging

| Platform | Format | Notes |
|---|---|---|
| Windows | Signed `Setup.exe`, **per-user install** to a per-user application directory, no elevation required | A machine-wide MSI may be produced later for enterprise need; a package-manager manifest points at the same signed installer |
| Windows store listing | **Unpackaged Win32**: the same signed installer, not a repackaged container | Distribution only, **never a commerce channel** (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**) |
| Linux | **A single self-contained portable format as the first official format** | Additional formats later; **do not maintain many packaging formats simultaneously in the first stage** |
| Android | Signed AAB from the .NET MAUI Android release build with Play App Signing, published to the official store; the separately signed APK is the direct channel | Consumption-only (**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**); a direct download may exist but is not the primary channel |

| # | Rule |
|---|---|
| <a id="rule-pp-01"></a>PP-01 | **The desktop installer is a packaging unit for one application** ([DS-02](../requirements/10-distribution-update-and-support.md#rule-ds-02) there). It never becomes a monolithic installer that bundles companions, services or other components with independent release lifecycles. |
| <a id="rule-pp-02"></a>PP-02 | **No macOS artifact exists.** macOS is out of scope ([P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)): there is no macOS build, package, signing, notarisation or release inventory row, and macOS CI is prohibited under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| <a id="rule-pp-03"></a>PP-03 | **Every product's package identity is stable and distinct**, and is never reused between products or channels. |
| <a id="rule-pp-04"></a>PP-04 | **The executable directory is never a user data directory** ([UP-05](../requirements/10-distribution-update-and-support.md#rule-up-05) there), and packaging must make that structurally impossible. |

---

## 6. Signing, provenance and supply chain

| # | Rule |
|---|---|
| <a id="rule-sp-01"></a>SP-01 | **All Windows executables and installers are signed and timestamped** ([PL-01](../requirements/10-distribution-update-and-support.md#rule-pl-01) there), so signatures remain valid after certificate expiry. |
| <a id="rule-sp-02"></a>SP-02 | **Linux artifacts carry published checksums, and repository signing where a repository is used.** macOS signing and notarisation do not exist ([P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)). |
| <a id="rule-sp-03"></a>SP-03 | **CI-produced artifacts are signed in their release pipeline against a scoped credential.** Release credentials are not copied into ordinary development builds. |
| <a id="rule-sp-04"></a>SP-04 | **The signing identity and the brand identity are distinct concerns** ([PL-04](../requirements/10-distribution-update-and-support.md#rule-pl-04) there). Where a certificate displays an individual name, the product surfaces and documentation still present the brand consistently, and the discrepancy is anticipated rather than discovered at first release. |
| <a id="rule-sp-05"></a>SP-05 | **Store developer accounts are established under the intended long-term owning identity** ([PL-05](../requirements/10-distribution-update-and-support.md#rule-pl-05) there). |
| <a id="rule-sp-06"></a>SP-06 | **An SBOM is produced for every artifact (managed, native and npm closures)**: a NuGet closure for managed artifacts, the native closure for DesktopPlatform native libraries and RID packages ([SP-09](#rule-sp-09)), and an npm closure for the Worker bundles and `ai-internal`, with licence closure, stored with the release record. |
| <a id="rule-sp-07"></a>SP-07 | **Build provenance attestation is produced and published**, so an artifact can be traced to its source commit and pipeline run. |
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
| <a id="rule-af-03"></a>AF-03 | **The feed can immediately stop offering a bad version** ([UP-10](../requirements/10-distribution-update-and-support.md#rule-up-10) there), and the compatibility policy can block a specific version range without blocking neighbouring versions. |
| <a id="rule-af-04"></a>AF-04 | **Feed changes are auditable** and carry an author, reason and timestamp. |
| <a id="rule-af-05"></a>AF-05 | **A public mirror of a release may exist**, but the authoritative feed is the ArcForges-owned one. |
| <a id="rule-af-06"></a>AF-06 | **Objects are immutable and content-addressed**; a delta package references exact source and target hashes. |
| <a id="rule-af-07"></a>AF-07 | **The download surface has no account gate** (`§4` of the web architecture) and remains available during a cloud incident. |

---

## 8. Update client architecture

| # | Rule |
|---|---|
| <a id="rule-uc-01"></a>UC-01 | **Update never blocks launch** ([UP-01](../requirements/10-distribution-update-and-support.md#rule-up-01) there): discover, download and stage in the background; apply at a safe moment. |
| <a id="rule-uc-02"></a>UC-02 | **The apply sequence is** download → verify signature and hash → stage → **atomic switch** → retain the previous launchable version ([UP-04](../requirements/10-distribution-update-and-support.md#rule-up-04) there). |
| <a id="rule-uc-03"></a>UC-03 | **A running task or unsaved work defers the apply step** ([UP-03](../requirements/10-distribution-update-and-support.md#rule-up-03) there) rather than interrupting it. |
| <a id="rule-uc-04"></a>UC-04 | **Rollback is reserved and tested** ([UP-06](../requirements/10-distribution-update-and-support.md#rule-up-06) there): the previous version stays launchable, subject to data-compatibility rules. |
| <a id="rule-uc-05"></a>UC-05 | **Migration is independent of the installer** ([UP-08](../requirements/10-distribution-update-and-support.md#rule-up-08) there): installer update → application start → data compatibility check → migration, with its own recovery path, and rollback compatibility considered. |
| <a id="rule-uc-06"></a>UC-06 | **A failed update never damages user data** ([UP-05](../requirements/10-distribution-update-and-support.md#rule-up-05) there). |
| <a id="rule-uc-07"></a>UC-07 | **Channel switching is a user action with stated consequences** ([RC-01](../requirements/10-distribution-update-and-support.md#rule-rc-01) there), including that moving down a channel may require a data compatibility check. |
| <a id="rule-uc-08"></a>UC-08 | **A critical security update has an expedited path** ([UP-09](../requirements/10-distribution-update-and-support.md#rule-up-09) there), coordinated with the advisory process and, where warranted, a policy kill switch — noting a kill switch reduces exposure but does not fix a local vulnerability. |
| <a id="rule-uc-09"></a>UC-09 | **Staged rollout is supported** using the deterministic rollout mechanism of the policy architecture (`§3` of the policy requirements), so a percentage rollout is stable per installation rather than re-randomised. |
| <a id="rule-uc-10"></a>UC-10 | **Update activity is observable**: check, download, verify, stage, apply, defer, fail and rollback are recorded with reason codes (`§2` of the observability architecture). |

### 8.1 Signed feed and update recovery profile

WP02 produces feed assets; [WP53](../planning/work-packages/53-desktop-distribution-and-update.md) produces ArcForges.Update and its Velopack integration; WP50 verifies production installers/feed. No product invents an independent updater. [Velopack's specific-version path](https://docs.velopack.io/integrating/specific-version) supplies mechanics; ArcForges still decides eligibility and data safety.

The owned HTTPS feed is `update.feed.v1`, a canonical JSON envelope `{payload,keyId,signature}`. Signature is ECDSA P-256/SHA-256 over RFC8785-canonical payload UTF-8 (exact numeric strings remain strings), IEEE-P1363 64-byte signature encoded unpadded base64url. Keys are release trust metadata installed with the client; rotations require a successor key signed by a currently trusted key, increasing trust generation and persisted revocations. Unknown/revoked keys refuse. OS package/code signatures remain separately mandatory. This signed static artifact is not a local RPC endpoint.

Payload fields are `schemaVersion` (update.feed.v1), `productId`, `channel` (existing stable/beta/nightly channel registry), `rid`, `sequence` (positive exact uint64 decimal string), `issuedAt`, `expiresAt` (UTC, validity at most 24h), `releases` (at most 200) and `blockedVersions` (exact SemVer strings, at most 200). Each release is `{version,full,delta?,minimumOs,minimumCloudVersion,contractMajors,dataReadMin,dataReadMax,dataWriteMin,dataWriteMax,rolloutKey,rolloutBasisPoints,securityUrgent,releaseNotes}`. `full` is `{url,size,sha256}`; delta adds `fromVersion,fromSha256` to the same shape. Sizes use exact uint64 strings; digests are lower-case SHA256; ranges inclusive; contractMajors is a sorted unique positive integer list; rolloutBasisPoints 0..10000; minimumOs is the RID's numeric OS version; releaseNotes is bounded plain text<=16 KiB. Max feed 1 MiB, unknown schema/duplicate version/invalid field rejects the whole feed. URLs and redirects must stay HTTPS on downloads.arcforges.com or updates.arcforges.com. Feed fields cannot carry code or arbitrary command lines.

Use the highest semantically eligible version for the selected product/RID/channel after all compatibility and signed-policy denies intersect. An explicit channel downgrade requires user consent and the same data horizon check. No feed entry can bypass a policy block. Persist highest verified sequence and sticky revocations per product/channel/RID; older sequence or expired feed cannot authorize a new apply. A same-sequence different hash refuses. Feed failure does not block launch or erase the last safe installation. Check on launch in the background, then every 6 hours with up to 10 percent jitter, and on explicit user check. Apply rechecks a current feed/policy; disconnected operation may continue locally with a staged candidate waiting.

Resume downloads only against the same URL/hash/size identity and correct Content-Range; otherwise restart. Verify source before delta, reconstructed full target after delta, and OS signature before execution; unsupported or failed delta falls back to the verified full target once. Disk-full/corruption retains the old installation. Velopack's signed updater executable and package layout are admitted WP02 artifacts, never a script fetched from feed text. Use its source adapter only after the wrapper validates this feed; framework defaults cannot replace SHA256 or trust checks.

The per-installation journal is versioned `update.journal.v1`: transactionId, product/installation/RID, channel, source/target version and hashes, feed sequence/hash, phase, prior package identity, observed store format/horizon and last reason. Phases are downloaded→verified→staged→awaitingExit→applying→pendingHealth→healthy, or failed/rolledBack. Flush each boundary before the corresponding irreversible action. Serialize updates by installation OS lock. Never acquire a domain lock while awaiting shutdown RPC; every running instance must report ready, then exit, before apply. Missing/refusing instances defer. Retain the previous verified full package outside updater cleanup until the new version reports successful local-store open and completed migration.

The selected Velopack per-RID switch must leave a valid launch path after kill at every boundary. On restart reconcile journal with actual signed active version; do not infer successful activation from a process exit code alone. A pre-migration launch failure may restore the previous verified package. After any migration write, automatic rollback is permitted only when the previous binary's declared read AND write horizon includes the recovered store format and the migration journal is clean; otherwise preserve data and enter the existing read-only/forward-repair recovery flow. The updater never runs a down migration or deletes a store. A security urgency flag offers an immediate safe update; it does not override unsaved-work deferral or authorize arbitrary termination. Staged rollouts use the existing installation-based policy algorithm. [UP-11](../requirements/10-distribution-update-and-support.md#rule-up-11) grace and compatibility denial come from WP44 policy, not a new hard-coded grace period.

---

## 9. Release gates

A release record states the applicable checks actually performed under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017). The retained build/static/signing gates control automated candidate publication. Runtime, hardware, browser, install and rehearsal rows below are scoped local product-acceptance scenarios, not CI or automatic publication prerequisites. Do not claim unobserved product coverage.

| # | Gate |
|---|---|
| <a id="rule-rg-01"></a>RG-01 | Build clean: zero errors, zero warnings-as-errors, zero suppressed AOT or trim diagnostics on the main path |
| <a id="rule-rg-02"></a>RG-02 | Architecture tests and repository policy tests pass ([BS-01](#rule-bs-01)) |
| <a id="rule-rg-03"></a>RG-03 | Contract baseline check passes, or the contract change is declared with a version bump and a compatibility note ([BS-02](#rule-bs-02)) |
| <a id="rule-rg-04"></a>RG-04 | Unit, integration, contract and migration test suites pass (`§25` of the quality contract) |
| <a id="rule-rg-05"></a>RG-05 | AOT publish succeeds for the desktop application and the artifact launches ([PM-01](#rule-pm-01), [PM-02](#rule-pm-02)) |
| <a id="rule-rg-06"></a>RG-06 | Performance budgets met: startup, memory, responsiveness, bundle size, with the regression gate applied (`§2`–`§6` there) |
| <a id="rule-rg-07"></a>RG-07 | Accessibility and localisation checks pass (`§10`, `§11` there) |
| <a id="rule-rg-08"></a>RG-08 | Windows and Android signing complete and verified on the packaged artifact ([SP-01](#rule-sp-01), [SP-03](#rule-sp-03)); no notarisation gate exists ([P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)) |
| <a id="rule-rg-09"></a>RG-09 | SBOM, provenance attestation and licence verification present ([SP-06](#rule-sp-06)–[SP-08](#rule-sp-08)) |
| <a id="rule-rg-10"></a>RG-10 | Update matrix verified: fresh install, upgrade, two-version upgrade, rollback, interrupted download, interrupted install, corrupted artifact rejection (`§5` of the distribution requirements) |
| <a id="rule-rg-11"></a>RG-11 | Compatibility manifest published: minimum OS, minimum cloud version, supported client window (`§15` of the quality contract). Include the signed browser-support.v1 artifact/hash, exact tested browser/OS versions and all four Web output hashes beside the minimum OS metadata. |
| <a id="rule-rg-12"></a>RG-12 | Release record complete and immutable ([RC-03](../requirements/10-distribution-update-and-support.md#rule-rc-03) there) |
| <a id="rule-rg-13"></a>RG-13 | Mobile only: **[F-023](../assurance/open-gates-register.md#rule-f-023)** dependency closure and provenance audit passed ([PL-06](../requirements/10-distribution-update-and-support.md#rule-pl-06) there) |
| <a id="rule-rg-14"></a>RG-14 | Mobile only: **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** store category fit and consumption-only conformance confirmed, and the commerce-prohibition build check passed ([MC-06](11-mobile-architecture.md#rule-mc-06) in the mobile architecture) |
| <a id="rule-rg-15"></a>RG-15 | Cloud migration and rollback rehearsal passes the selected modeA/B/C: compatible binary rollback only inside the proven write/schema horizon; outside it use verified forward repair or independent fresh-environment restore with safety-journal/generation fencing. No universal down-migration promise. |
| <a id="rule-rg-16"></a>RG-16 | No open severity-blocking quality issue and no expired quality waiver (`§21` there) |

---

## 10. Continuous integration topology

| # | Rule |
|---|---|
| <a id="rule-ci-01"></a>CI-01 | **Pull-request builds run the fast gates**: build, unit tests, architecture and policy tests, contract baseline check. |
| <a id="rule-ci-02"></a>CI-02 | **Main runs the retained build/offline/static/security gates for its changed owner.** No hosted runtime, installed-consumer or live-service execution is permitted; unrelated sources are not rebuilt. |
| <a id="rule-ci-03"></a>CI-03 | **Release builds additionally package, sign, attest and record.** |
| <a id="rule-ci-04"></a>CI-04 | **Scheduled jobs are limited to non-duplicated offline/static/security checks.** Long runtime, soak, hardware, browser and live-service jobs are not scheduled in CI. |
| <a id="rule-ci-05"></a>CI-05 | **CI uses only required Windows/Linux runners.** All macOS CI, including self-hosted/manual/scheduled variants, is prohibited, and macOS is out of scope ([P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)): no macOS runner, artifact or support claim exists. |
| <a id="rule-ci-06"></a>CI-06 | **A flaky test is quarantined with an owner and an expiry**, never silently retried forever. |
| <a id="rule-ci-07"></a>CI-07 | **Pipeline definitions are versioned in the repository** and reviewed like code. |
| <a id="rule-ci-08"></a>CI-08 | **Credentials are scoped per pipeline stage**; a test stage never holds a signing or publishing credential. |
| <a id="rule-ci-09"></a>CI-09 | **The pipeline is reproducible from the repository.** A rebuilt pipeline on a clean runner produces the same result from the same commit. |

---

## 11. Environments and promotion

| # | Rule |
|---|---|
| <a id="rule-ep-01"></a>EP-01 | **Environments are configuration, not builds** ([BR-01](#rule-br-01)). |
| <a id="rule-ep-02"></a>EP-02 | **Promotion order is fixed** — development → staging → production for Cloud; nightly → beta → stable for clients — and skipping a stage is an explicit, recorded exception. |
| <a id="rule-ep-03"></a>EP-03 | A production deployment has a verified recovery route appropriate to migration mode. ModeC pauses incompatible writes, fences cutover and ends old-binary rollback at its declared horizon. After that boundary forward repair or verified fresh-environment restore is required; expanding/contracting schemas cannot make incompatible persisted writes reversible by flag alone. |
| <a id="rule-ep-04"></a>EP-04 | **Client and cloud releases are decoupled**, and the compatibility window governs their interaction (`§15` of the quality contract). A cloud release must not require a client release on the same day. |
| <a id="rule-ep-05"></a>EP-05 | **A minimum-cloud-version requirement is imposed only after every channel has had a genuine opportunity to update**, with the grace period honoured ([UP-11](../requirements/10-distribution-update-and-support.md#rule-up-11) there). |

---

## 12. Non-goals

The build and release system is **not**: a monolithic installer; a second update mechanism layered on a store; a place where product code learns about the packaging tool; a route for an unsigned or unrecorded artifact to reach a user; a justification for rebuilding per environment; or a reason to collapse the nine version axes into one number.

---

## 13. Traceability

| Current document | Relationship |
|---|---|
| [Distribution, Update, Support and Trust & Safety Requirements](../requirements/10-distribution-update-and-support.md) | Owns signing, channels, release records, packaging and update behavior |
| [Product Quality and Compatibility Contract](../requirements/12-quality-and-compatibility-contract.md) | Owns the runtime and release evidence matrix |
| [Deployment and Release Execution](22-deployment-and-release-execution.md) | Defines publication, promotion, rollback and compatibility procedures |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)** | The publish matrix and its verification obligations |
| **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** | Seven independently built implementation repositories and the Design authority, integrated through versioned packages and immutable artifacts |
| **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** | Update and download domains as owned surfaces |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)**, **[F-023](../assurance/open-gates-register.md#rule-f-023)** | Mobile release gates |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**, **[F-013](../assurance/open-gates-register.md#rule-f-013)** | Licence and provenance verification in the supply chain |
| **[P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021)**, **[P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)**, **[P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)**, **[P2-024](../decisions/phase-2-specification-decisions.md#rule-p2-024)** | C#-first build, publication and channels; PDF retirement (report export kept); macOS out of scope; WSL2 Linux validation |

## 14. Independent producer and consumer artifact gates

The exact integration manifest is owned by [deployment 22](22-deployment-and-release-execution.md#p2-009-independent-artifact-deployment-and-restore); build outputs populate its real hashes, D1 schema/plan identity and deployed compatibility date.

Per-repo locked restore/build/offline tests → immutable producer candidate → consumer compile/AOT/package → original-candidate promotion/deployment with provider status. Runtime/browser/real-provider scenarios remain explicit local opt-in, never default CI or post-merge steps. Fork/untrusted PR code gets no deployment secrets; trusted CI promotes reviewed commit with short-lived credentials and dedicated test realm/service account, unique resources,24h cleanup TTL. Tests enter the isolated Worker TLS origin and reach the Container through its private binding; storage.internal stays private. A directly public C# origin or runner localhost cannot substitute for the production route/binding graph. Test artifacts use no real customer content. No submodules/latest/floating branch fixtures.

Rolling upgrade: expand DB/internal/public read schemas → backfill from watermark → deploy C# dual readers → deploy compatible Worker thin adapters (in-flight adapter invocations drain on their pinned Worker version; no Workflow instance state remains, [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 5) → canary/soak ≥24h → activate config reader head → clients independently update within supported window → contract only after all old executor leases and in-flight adapter invocations drained and rollback horizon closed. Incompatible Worker adapter code is a new deployment version under a migration tag; no hot reinterpretation of checkpoints. Rollback before contract restores prior image/Worker/config/assets; after destructive contraction use verified forward repair or fresh-environment restore, not blind old binary startup. Selfhost operator supplies own CF resources/AWS disaster copy/DB/secrets/origins/realm, same one-host architecture.

Use [the CF/object recovery contract](contracts/05-cloudflare-integration.md#6-r2-lifecycle-and-independent-recovery) for the independent S3 COMPLIANCE 30-day backup, D1 export/change archive/object manifests and recovery generation. Observability join request/task/run/attempt/outbox IDs over W3C traceparent across C#/Worker/device with redaction; expose CF dispatch lag/unknown attempts/R2 transfer failures/backup lag/lease conflicts. CF/R2 outage leaves hydrated ArcScope acquisition, analysis and annotation usable within its existing offline rules; AI pauses/fails with durable reasons and support/export stay truthful. Full recovery tested after WP46+52 and before 50.

## Producer bootstrap and candidate manifests

Before a complete Cloud exists, each producer publishes a candidate manifest with source commit, artifact hashes, exact Contracts/Platform dependencies, RID/runtime and evidence. WP02 supplies this format/pipeline, WP03 publishes schemas and WP06 composes the first foundation integration manifest in ArcForges-Cloud. Early packages may consume this manifest without depending on later business features. WP21 and later packages extend it with real owner behavior; WP50 requires the final complete manifest. No package is required to restore an artifact that its own current step has not yet produced.

## Immutable candidate publication

Allocate the actual NuGet or product version before compilation and signing. A candidate channel is an access/promotion state, not a version suffix that can later be renamed. Promoting version 1.0.0 moves the same 1.0.0 bytes and attestation from private candidate to the approved channel. An artifact compiled as 1.0.0-ci.42 retains that version permanently; a 1.0.0 build is a new candidate requiring its own checks. Mutable tags are pointers only; restore and integration manifests bind version plus hash. Bootstrap stages and partial versus full manifest closure are fixed in [planning](../planning/README.md#staged-artifact-integration).

## Complete producer candidate and promotion protocol

[Producer artifacts and integration](../planning/producer-artifacts-and-integration.md) owns the complete package/stage matrix. Contracts delivers every initial field/profile and C# NuGet artifact (and the retained `ai-internal` artifact) before consumer WPs; DesktopPlatform compiles the full required native RID closure before packing any wrapper/runtime candidate. A candidate is the actual immutable release input, not a dummy package. The same candidate bytes are packaged and published without hosted consumer execution, with package hashes, descriptors/ABI, SPDX/NOTICE/SBOM and source commit in its manifest.

The [Contracts publication channels profile](contracts-publication-channels.md) governs the NuGet channels and the retained npm package. Its Maven Central release rows and its npm channels for the stopped packages still describe the pre-P2-021 publication; that correction is pending as the row for `architecture/contracts-publication-channels.md` and `architecture/14-build-packaging-and-release.md` in the P2-021 pending-correction table. Until it merges, [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 4 governs the stopped channels: the Maven destination below and the other npm packages stop publication after their consumers migrate ([CON.40](../planning/delivery/lanes/contracts.md#task-con-40)); published versions stay immutable and resolvable.

PR CI validates/generates/builds/packs/tests but has no registry publish authority. Merge to main automatically allocates 1.0.0-ci.<run>.<attempt> (configured base version), creates the complete candidate, checks its required build outputs and publication identity, then promotes that version. Explicit stable version configuration/tag passes the same graph; no manual publish job is needed. Use a single non-canceling publication concurrency group and immutable version claim. NuGet prerelease remains explicit; the retained npm package's latest tag moves to the newest fully verified main candidate only after its artifacts are available. Consumers pin exact versions and committed locks, never float latest on each restore. Dependency update PRs refresh the whole compatible producer set, test and commit locks.

NuGet and npm registries are not one transaction. Persist release state allocated/built/verified/publishing/complete or partial, expected asset inventory and per-registry receipts. Publish only the already-verified bytes; resume only with a trustworthy existing publication receipt or registry identity metadata for the same candidate. Ambiguous existing versions fail for diagnosis; routine remote archive downloads are prohibited. On partial publication keep promotion manifest and dist-tag updates blocked, resume missing outputs from the preserved signed candidate; do not rebuild or delete/reuse versions. If unrecoverable, abandon that candidate and publish a new version while consumers remain on the last complete release. A deployment manifest can reference only complete producer releases. npm dist-tag rollback points to the prior complete version; it does not remove packages or rewrite consumer locks.

GitHub Environments and OIDC trust are repository-specific. NuGet policy binds exact repository/workflow/environment/package scope; npm trusted publisher binds each package and workflow/environment after its one-time bootstrap. Bootstrap granular token is revoked after successful OIDC verification and removed from CI; normal runs contain no npm static publish token. Maven Central publication stops only after its consumers migrate ([CON.40](../planning/delivery/lanes/contracts.md#task-con-40)). Until that stop, the Maven namespace-verification requirements, the publisher credential and signing requirements, and the immutable JAR, POM, signature and checksum output still bind. Stopped releases stay immutable, resolvable and signed. Nothing is unpublished, deleted or deprecated without explicit user approval ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 4). CI secrets remain environment-bound; namespace ownership and successful provider publication/status are implementation gates, not evidence established by this document. Signing identity and artifact provenance are checked before any registry accepts a candidate.

### Current automated platform coverage

[P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017) prohibits macOS CI, including scheduled/manual/self-hosted paths. macOS is out of scope ([P2-023](../decisions/phase-2-specification-decisions.md#rule-p2-023)): there is no macOS build, artifact, signing or release inventory row, and no macOS support or validation is claimed. Automated release inventories list only the produced Windows, Linux and Android (APK/AAB) artifacts. Product support claims still require actual evidence from the platform concerned. Post-merge confirmation is limited to commit and required job/publication/deployment status; no repeated public-byte or runtime verification.
