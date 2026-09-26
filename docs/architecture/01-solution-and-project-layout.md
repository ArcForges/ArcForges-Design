# Solution and Project Layout

Authority: [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012). The [concrete project/package tree and host contracts](27-platform-projects-and-application-assistants.md) are the implementation directory authority for every repository, particularly DesktopPlatform.

<a id="1-repository-ownership-and-dependency-graph"></a>
## 1. Independent repository roots

DesktopPlatform, Contracts, ArcNotes, ArcScope, ArcSlate, Cloud, AI, Web and Mobile build independently. ArcChat is a reusable assistant feature family inside DesktopPlatform, not another desktop process/repository. Each product owns its domain/application/infrastructure/UI integration. Shared code never implies a shared database or live singleton across applications.

### Root and logical path convention

Use the exact repository/project trees in architecture 27. Remaining logical suffixes in older rule examples identify their single owning repository; they do not authorize adjacent-source references. Current work-package project sections select those concrete trees. Contracts produces generated clients; ArcForges.Cloud.Client implements reusable session/transport/recovery behavior above them. No product CloudClient implementation is duplicated into Contracts.

## 2. Project conventions

**Approved helper projects ([P2-007](../decisions/phase-2-specification-decisions.md#rule-p2-007)).** `src/DesktopHelpers/ArcForges.ContentSandbox` is a signed first-party C# Native AOT executable with no product-domain/Harness/store dependency. `ArcForges.ContentSandbox.Contracts` is a thin facade over Contracts-owned `.LocalRpc.Sandbox` generated messages/services; `ArcForges.ContentSandbox.Broker` owns launch profiles and handle/resource budgets. Product-specific approved parser wrappers are loaded only in that helper. Native library adaptation remains narrow; no C++ business host or cross-product shared pool is introduced. [WP-11.09](../planning/work-packages/11-security-foundation.md#rule-wp-11.09) supplies this boundary before [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04) or media ingestion depends on it.

| # | Rule |
|---|---|
| <a id="rule-pj-01"></a>PJ-01 | **One responsibility per project.** A project that is both a domain and an adapter is a defect. |
| <a id="rule-pj-02"></a>PJ-02 | **Every .NET library consumed by an AOT deliverable sets IsAotCompatible; each AOT host sets PublishAot.** Node/TS packages and esproj never inherit .NET runtime properties. |
| <a id="rule-pj-03"></a>PJ-03 | Local RPC uses generated protobuf/gRPC bindings and explicit service registration; no runtime attach/interceptor reflection path. |
| <a id="rule-pj-04"></a>PJ-04 | **NuGet versions use Directory.Packages.props; Web versions use exact npm manifest pins and the one workspace lock.** JavaScript SDK/Node versions have their own reviewed toolchain pins; no accidental inline NuGet override. |
| <a id="rule-pj-05"></a>PJ-05 | **Each .NET packages.lock.json and the Web package-lock.json are committed.** CI uses locked dotnet restore and npm ci; esproj disables implicit npm install. |
| <a id="rule-pj-06"></a>PJ-06 | **Preview packages never enter a stable branch's core path.** |
| <a id="rule-pj-07"></a>PJ-07 | **.NET code follows nullable/implicit-usings/analyzer/SourceLink policy; TypeScript follows strict compiler, import-boundary and lint policy.** Deterministic builds, UTF-8/LF formatting and reproducible provenance cover both. |
| <a id="rule-pj-08"></a>PJ-08 | **Warnings as errors**, enabled repository-wide once staged debt is cleared; trimming and AOT diagnostics are always errors on AOT deliverables. |
| <a id="rule-pj-09"></a>PJ-09 | **Every project/package declares its SPDX licence and boundary.** .NET uses project metadata, npm uses package metadata; public generated SDK and product UI dependency graphs are audited separately. |

---

## 3. Contract packages

Contracts also owns the Apache-2.0 machine-readable [naming policy](28-product-naming-policy.md) and its standalone inventory scanner. WP00 policy verification does not create a product source/build dependency or require a future package.

Mobile and the entire Contracts repository (public/internal proto, HTTP schemas, generators, SDK/CLI, validators and fixtures) are Apache-2.0 under [P2-010](../decisions/phase-2-specification-decisions.md#rule-p2-010). Public/internal remains an access and import-direction separation. Platform/Cloud/AI/Web/three professional desktop implementations retains its existing licence; dependencies keep their own notices. Generated files preserve authored-schema and generator/runtime notices. Mobile imports only public artifacts and public fixtures; it cannot import Web application expression or any GPL-family implementation.

Package metadata declares owner/SPDX/source commit, schema/package version, dependency closure, NOTICE and SBOM. Public npm access=public, NuGet public registry; AGPL packages may be publicly distributed with source/notice obligations. Per-RID native license closure includes static dependencies and optional codec features, not merely the wrapper's license. Six reference-source access/exclusion/provenance boundaries and all archive prohibitions stay unchanged. Source review and actual distributable license gate remain evidence obligations; this amendment does not claim third-party code has been copied or audited by a runtime test.

The [wire registry](contracts/04-protobuf-wire-registry.md) defines every service/message/field and the public/internal package split. Generated C#, TypeScript and Java/Kotlin output is not hand-edited. The [CF integration schema](contracts/05-cloudflare-integration.md) owns private Cloud/AI bindings and signed object transfers. Public AI operations remain generated gRPC-Web under annex 10. Contract validators validate shape/profile; business validation remains in the owner.

| # | Rule |
|---|---|
| <a id="rule-ct-01"></a>CT-01 | Independent product changes cannot force unrelated product releases. |
| <a id="rule-ct-02"></a>CT-02 | Handwritten proto in Contracts is the sole business wire source; C#/TS/Kotlin clients are generated. |
| <a id="rule-ct-03"></a>CT-03 | Contracts contain no business implementation. |
| <a id="rule-ct-04"></a>CT-04 | Contracts have no UI/ORM/native/host dependency. |
| <a id="rule-ct-05"></a>CT-05 | C# contract libraries satisfy the Native AOT gate; public clients all select gRPC-Web. |
| <a id="rule-ct-06"></a>CT-06 | Cloud/public browser clients never import local product RPC packages. |
| <a id="rule-ct-07"></a>CT-07 | Public business records expose no local IPC/native handles. |
| <a id="rule-ct-08"></a>CT-08 | Foundation remains stable and bounded; domain services own their own types. |

---

## 4. Licence boundary enforcement

| # | Rule |
|---|---|
| <a id="rule-lb-01"></a>LB-01 | Every .NET project declares PackageLicenseExpression/LicenceBoundary; npm packages declare license and the equivalent repository boundary metadata. The generated TS public SDK is Apache; Web product UI is AGPL. |
| <a id="rule-lb-02"></a>LB-02 | **No AGPL source/package enters an Apache dependency closure.** Check .NET references and npm imports/dependencies, including generators and copied component provenance where applicable. |
| <a id="rule-lb-03"></a>LB-03 | **A dependency test asserts that the mobile distributable's complete direct and transitive closure is compatible with Apache-2.0 application distribution and applicable store terms** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** obligation 7). |
| <a id="rule-lb-04"></a>LB-04 | **`NOTICE` files are generated from the dependency graph**, per boundary, as part of packaging. |
| <a id="rule-lb-05"></a>LB-05 | **SBOM generation runs per deliverable**, and its output is a release artifact. |
| <a id="rule-lb-06"></a>LB-06 | **On discovery of a conflicting contribution or dependency in the mobile boundary, the issue is registered and returned for decision.** Silently adding an exception, changing the licence, or removing the mobile distribution target is prohibited (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |
| <a id="rule-lb-07"></a>LB-07 | **Reference-repository reuse requires the ten-field provenance record before any copy, translation, port or structural reuse** (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**), recorded in [`../assurance/reference-coverage-and-provenance.md`](../assurance/reference-coverage-and-provenance.md). |

### 4.1 Project declaration and verification profile

[WP-00.02](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.02)
makes the existing two-boundary decision readable by each build system. The current
repository-wide assignment is closed: **Contracts and Mobile use `Apache` with
`Apache-2.0`; DesktopPlatform, ArcNotes, ArcScope, ArcSlate, Cloud, AI and Web use
`AGPL` with `AGPL-3.0-only`**. This covers original tooling, tests and internal
schemas as well as application/library projects. Public/internal contract access
restrictions remain separate from licensing. Third-party components retain their
own licences and are never relicensed by these declarations.

Each implementation owner maintains `eng/policy/licence-boundary.json`, schema
version 1, with `repository`, `spdxLicense`, `licenceBoundary` and `projects`.
Each project row names its repository-relative `path` and `kind` (`msbuild`,
`npm`, `gradle` or `cmake`). The inventory includes tooling, test, root/workspace
and IDE projects. It matches the actual tracked project/build manifests and
non-ignored new manifests during local validation; a missing, extra or duplicate
row fails. It is an inventory of existing projects, not permission to create
future scaffolds. Build declarations use these representations:

| Build system | Project declaration | Build verification |
|---|---|---|
| MSBuild, including native/JavaScript IDE projects | `PackageLicenseExpression` and `LicenceBoundary` properties | Inspect evaluated properties and references for supported build configurations; reject absent or changed values before build/pack. IDE-only adapters additionally receive source-inventory checks. |
| npm root/workspace packages | `license` and `arcforges.licenceBoundary` in each `package.json` | The existing build/policy command verifies every workspace manifest and its dependency graph. |
| Gradle root/subprojects and independent tooling/test builds | `spdxLicense` and `licenceBoundary` project extra properties | Verify evaluated project properties and project dependencies; published POM licences agree with the declared SPDX identifier. |
| CMake project | `ARCFORGES_SPDX_LICENSE` and `ARCFORGES_LICENCE_BOUNDARY` project variables and owned target properties | The configured owned target graph carries and verifies the declaration; imported third-party targets retain their own attribution. |

Declarations may be inherited through an owned build convention, but verification
uses their effective values and cannot accept a missing declaration merely because
the repository root has a LICENSE file. Reports retain the discovered project set,
source commit/dirty state, evaluated declarations, reference edges and findings.
The enumerated repository assignment is checked independently of editable project
metadata. Every Apache project rejects an AGPL project/package in its direct or
transitive closure; an unknown first-party package owner also fails review.
Generated bindings follow their existing generator and input provenance.

DesktopPlatform owns the standalone family inventory/reference verifier. It may
read explicitly supplied implementation roots for this audit, without building,
importing or executing adjacent product source. Each owner also verifies its own
declarations in its existing native build/CI toolchain. Apache owners do not copy
or import the AGPL verifier. This source-policy audit creates no product build
dependency and requires no future policy package. Distribution and the expanded
repository-policy suite remain with [WP-02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02)
and [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05).

The current reference-direction result is not a complete third-party licence
audit. Existing candidate pipelines and their licence/NOTICE checks still apply.
Before producing a new Android candidate, the Mobile owner must record and verify
the actual resolved direct/transitive distributable dependency closure, its
licence evidence and retained notices under [F-023](../assurance/open-gates-register.md#rule-f-023).
Unknown or conflicting entries fail; a project declaration cannot excuse them.
Evidence is bound to the inspected source, dependency locks and artifact, and does
not preapprove future dependencies or claim store/commercial readiness.

Review covers missing/overridden declarations, an unregistered project, inconsistent
boundary/SPDX pairs, an Apache-to-AGPL edge (including a transitive one), unknown
first-party ownership and references escaping the selected repository. Preserve
existing package/application identities, signing continuity and immutable producer
publication order. The declaration work changes no licence grant, architecture
layering rule or allowed reuse disposition.

### 4.2 Current Android dependency conflict and remediation

The WP00.02 collection on 2026-09-18 found Mobile commit
`15145a4b4139525aae4185f0d2d20c87ec91686a` enabling core-library desugaring and
locking `com.android.tools:desugar_jdk_libs:2.1.5`. Its
[published POM](https://dl.google.com/dl/android/maven2/com/android/tools/desugar_jdk_libs/2.1.5/desugar_jdk_libs-2.1.5.pom)
declares GPL version 2 with the Classpath Exception. The
[Android build documentation](https://developer.android.com/studio/write/java8-support#library-desugaring)
explains that this option can package library implementation in a separate DEX.
It is therefore a distributable input, not merely the build JDK. This concrete
conflict is registered under [F-023](../assurance/open-gates-register.md#rule-f-023);
the existing blanket exclusion in [D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)
is not waived by the upstream exception or an earlier successful build.

The selected resolution is to remove that optional core-library implementation
from Mobile's dependencies and packaging, while retaining Kotlin/Java target 21,
Android minimum API 26, application identity, signing continuity and all accepted
Android behavior. D8/R8 language-bytecode transformation remains enabled. Mobile
must verify the complete actual Android runtime closure and retained notices
before producing a new candidate, reject unknown/conflicting inputs, and bind
the result to source, locks and final APK/AAB hashes. Device/runtime checks must
exercise the published client and the minified release on the minimum supported
API as well as the current CI image; lint or compilation alone cannot prove
the removal is compatible. Any newly discovered unsupported API must be repaired
within the same Android requirements, without raising the minimum API or quietly
restoring an excluded dependency.

Mobile owns this remediation and its Apache-licensed checks. Development-only
JVM preview tools and build-host JDKs are identified separately from Android
packaging inputs. This decision records the issue and chosen repair;
[F-023](../assurance/open-gates-register.md#rule-f-023) is satisfied only by actual
dependency, notice and artifact evidence. Its [current candidate record](../assurance/open-gates-register.md#21-current-android-candidate-licence-evidence)
separates completed checks from pending or later gates. It changes
no licence grant, store-distribution target or future product acceptance gate.

---

## 5. Cloud module projects

The 21 domain owners in the [Cloud schema map](data-model/01-cloud-data-model.md#1-schema-map) are authoritative; `platform` is shared infrastructure, not a domain module. The concrete arrangement is `src/Modules/<Name>/<Name>.Domain`, `<Name>.Application`, `<Name>.Infrastructure` and module tests. Cloud.Host composes them; Cloud.Storage.D1 owns the named-plan binding mechanism, while module owners own their plans/tables. Private implementation folders within these projects remain implementation choices.

Modules: **Identity**, **Workspace**, **Devices**, **Entitlement**, **Commerce**, **Chat**, **Task**, **Agent**, **Sync**, **Resource**, **Search**, **Notification**, **Policy**, **Audit**, **Support**, **TrustSafety**, **Notes**, **Scope**, **Slate**, **Configuration**, **PackageCatalog**.

| # | Rule |
|---|---|
| <a id="rule-cm-01"></a>CM-01 | **A module owns its schema or its explicit table set.** No other module writes those tables. |
| <a id="rule-cm-02"></a>CM-02 | **Cross-module interaction is through a module's public API or its published events**, never through its persistence. |
| <a id="rule-cm-03"></a>CM-03 | **An architecture test asserts module persistence ownership.** |
| <a id="rule-cm-04"></a>CM-04 | **All modules ship inside the single Cloud Host.** A future change to deployment topology requires an accepted architecture decision; a project split is not permission to add deployment roles. |

---

## 6. Reference direction

```
Desktop / Infrastructure / public gRPC-Web / Kotlin Android adapters
Private helper transport adapters (no product listener)
                                 ↓
                          Application
                                 ↓
                             Domain

Contracts.Foundation  ←  Contracts.PublicApi
Contracts.Foundation  ←  Contracts.Events
Contracts.Foundation  ←  Contracts.LocalRpc.*
```

Hard rules, all enforced by architecture tests:

| # | Rule |
|---|---|
| <a id="rule-rd-01"></a>RD-01 | Domain references neither Application, Infrastructure, UI nor Contracts. |
| <a id="rule-rd-02"></a>RD-02 | Application depends only on Domain plus abstractions. |
| <a id="rule-rd-03"></a>RD-03 | Infrastructure implements Application's ports. |
| <a id="rule-rd-04"></a>RD-04 | A generated local/public wire DTO never becomes a domain entity. |
| <a id="rule-rd-05"></a>RD-05 | A UI model never becomes a transport DTO. |
| <a id="rule-rd-06"></a>RD-06 | Typed HTTP client interfaces exist only inside the public API client contract boundary. |
| <a id="rule-rd-07"></a>RD-07 | Local RPC interfaces exist only inside the local RPC contract boundary. |
| <a id="rule-rd-08"></a>RD-08 | Realtime DTOs are never the canonical persisted domain events. |
| <a id="rule-rd-09"></a>RD-09 | Products never reference each other's Domain, Application or Infrastructure. |
| <a id="rule-rd-10"></a>RD-10 | The design system and desktop shell reference no product domain. |

---

## 7. Architecture and repository-policy tests

These are release gates, not advisory checks (`§23` of the quality contract).

### 7.1 Architecture tests

| # | Assertion |
|---|---|
| <a id="rule-at-01"></a>AT-01 | Domain references no UI, infrastructure, transport or database provider assembly |
| <a id="rule-at-02"></a>AT-02 | A local RPC adapter references no view model or control type |
| <a id="rule-at-03"></a>AT-03 | A public API adapter references no UI type |
| <a id="rule-at-04"></a>AT-04 | Contracts reference no platform-specific type |
| <a id="rule-at-05"></a>AT-05 | Products do not reference each other's Domain, Application or Infrastructure |
| <a id="rule-at-06"></a>AT-06 | Native pointers and `SafeHandle` types do not cross the native adapter boundary |
| <a id="rule-at-07"></a>AT-07 | A Cloud module does not reach into another module's persistence |
| <a id="rule-at-08"></a>AT-08 | No catch-all string/object RPC entry point exists |
| <a id="rule-at-09"></a>AT-09 | No long-lived C++ worker executable project enters the release graph |
| <a id="rule-at-10"></a>AT-10 | The reflection-based typed-HTTP-client package is absent from C# production dependency graphs; browser HTTP uses generated TS SDK imports. |
| <a id="rule-at-11"></a>AT-11 | Every local service implements its generated proto contract and maps explicitly to its owner application port. |
| <a id="rule-at-12"></a>AT-12 | Every wire type is generated from the owned proto or exception JSON schema; runtime serializers/validators agree with the released descriptors. |
| <a id="rule-at-13"></a>AT-13 | Every module's public surface is reachable only through its declared API |
| <a id="rule-at-14"></a>AT-14 | The design system and shell reference no product domain assembly |

### 7.2 Repository-policy tests

| # | Assertion |
|---|---|
| <a id="rule-rp-01"></a>RP-01 | **No forbidden alias or obsolete product name** appears in `src/`, `tests/`, `eng/`, identifiers or resource strings — `ArcCanvas`, `ArcMusic`, `ArcImage`, `ArcVideo`, and the superseded payment provider (**[D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002)**, **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)**) |
| <a id="rule-rp-02"></a>RP-02 | Every project declares an SPDX licence identifier and a licence boundary |
| <a id="rule-rp-03"></a>RP-03 | No `AGPL` project is referenced from an `Apache` project |
| <a id="rule-rp-04"></a>RP-04 | The mobile distributable's dependency closure passes the licence policy |
| <a id="rule-rp-05"></a>RP-05 | NuGet versions obey central management; npm versions/lock and JavaScript SDK pins obey the declared Web policy. |
| <a id="rule-rp-06"></a>RP-06 | Each toolchain lock is present/current; there is exactly one Web npm root and no nested lockfile. |
| <a id="rule-rp-07"></a>RP-07 | No blanket suppression of trimming or AOT diagnostics exists |
| <a id="rule-rp-08"></a>RP-08 | Every glossary-forbidden term is absent from new authoritative text |
| <a id="rule-rp-09"></a>RP-09 | No secret-shaped literal is committed |
| <a id="rule-rp-10"></a>RP-10 | Every public API method has a corresponding contract test |

---

### 7.3 Web graph assertions

Assert portable managed projects have no esproj reference; win.slnx contains exactly the intended Web adapter; Web imports no private policy, database/entity or local-RPC contract; SDK imports no product UI; Account/Chat route graphs are selected explicitly; Authored proto changes trigger C#/TS generation and compatibility tests. Scope desktop DOM/JS bans to desktop build graphs, while prohibiting obsolete Blazor product dependencies in the current Web target.

---

## 8. Test project taxonomy

| Project | Purpose |
|---|---|
| `ArchitectureTests` | §7.1 |
| `RepositoryPolicyTests` | §7.2 |
| `ContractCompatibilityTests` | Previous stable client against current implementation, and the reverse, across the supported window |
| `PublicApiContractTests` | Generated client against a real server: route, verb, status, shape, ETag and revision semantics |
| `LocalRpcAotTests` | Real named pipe and domain socket round-trips against AOT-published artifacts |
| `RealtimeReconnectTests` | Connect, disconnect, reconnect, sequence-gap backfill |
| `MigrationTests` | The golden-fixture corpus, round-trip, failure injection, downgrade behaviour |
| `NativeAbiTests` | Per-RID ABI verification including every error path |
| `EndToEndTests` | Multi-process scenarios across products |
| `Performance` | Benchmarks with regression gates against reference hardware |

---

## 9. Fixtures

| # | Rule |
|---|---|
| <a id="rule-fx-01"></a>FX-01 | **Golden fixtures are permanent and immutable.** A fixture is added, never edited. |
| <a id="rule-fx-02"></a>FX-02 | **Every historical native format version has a fixture.** |
| <a id="rule-fx-03"></a>FX-03 | **Serialized golden vectors exist for every wire contract** — exact bytes for representative messages. |
| <a id="rule-fx-04"></a>FX-04 | **Fixtures come from several sources**: synthesised, captured with consent and redaction, and edge cases. **Unredacted real user data never enters the repository.** |
| <a id="rule-fx-05"></a>FX-05 | **Scale corpora are declared by manifest**, generated deterministically rather than committed as large binaries where possible. |

---

## 10. Reconciliation and repository split

**[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)**: the existing repository's scaffolds and code are **implementation-state evidence, never design authority**, and may be retained, restructured, replaced or removed as the accepted design requires.

| # | Rule |
|---|---|
| <a id="rule-mg-01"></a>MG-01 | **Migration proceeds one vertical slice at a time.** A slice is complete when its contract, application, infrastructure, adapter, tests and gates all conform. |
| <a id="rule-mg-02"></a>MG-02 | **The architecture and policy tests are introduced early and grow**, so conformance is ratcheted rather than promised. |
| <a id="rule-mg-03"></a>MG-03 | **Existing code that has not yet been migrated is fenced**, so it cannot be referenced from conforming projects. |
| <a id="rule-mg-04"></a>MG-04 | **The current-code reconciliation inventory is produced before restructuring begins**, and recorded in [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md). |

---

## 11. Traceability

| Current document | Relationship |
|---|---|
| [ArcForges Product Scope and Portfolio](../requirements/00-product-scope-and-portfolio.md) | Owns product independence, runtime boundaries and shared-foundation limits |
| [Build, Packaging and Release Architecture](14-build-packaging-and-release.md) | Defines build governance and packaging |
| [Web Toolchain, Generated SDK and Developer Workflow](25-web-toolchain-and-sdk.md) | Defines Node workspace, esproj integration and portable Web entry points |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** | Licence boundaries and provenance gating enforced structurally |
| **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** | The contract split |
| **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** | The implementation target and the treatment of existing code |

## 12. Package and native distribution registry

Publish the following package identities. Managed package versions and their compatible ABI range are independent from product versions. A producer candidate has version 1.0.0-ci.<run>.<attempt>, stable starts 1.0.0; never overwrite an existing package/version. Producer release manifests list SHA256 and exact dependencies. Contracts Maven development distribution uses the explicit [SNAPSHOT channel exception](contracts-publication-channels.md); formal tag releases remain immutable.

| Package family | Dependencies / public C# capability | Native RID assets |
|---|---|---|
| ArcForges.Foundation, .Application.Abstractions | Contracts.Foundation; IDs are adapters, not duplicate wire types | None; headless |
| ArcForges.LocalRpc, .Capabilities | Foundation and exact local Contracts; private-child IPC and in-process descriptor mechanisms from WP08/09 | No product implementation or native payload transport |
| ArcForges.Observability | Foundation; bounded Activity/Meter/logging, no product telemetry schema | None; headless |
| ArcForges.Persistence.Sqlite | Foundation; desktop SQLite/journal mechanics, no product schema/Cloud D1 binding adapter | None in managed package; SQLite runtime independently selected |
| ArcForges.Security, .Update, .Execution | Foundation; OS secret/approval adapters, signed updates, ProductJob mechanics | Explicit OS adapters; Cloud may consume only documented headless subpackages |
| ArcForges.DesignSystem, .Desktop.Shell | Foundation plus Avalonia; shell also DesignSystem | Avalonia asset closure; product apps own flows |
| ArcForges.Cloud.Client | Foundation/Security + exact public Contracts; sessions, gRPC-Web, streams and transfers | No desktop native closure; WP06 minimal, WP23–25 complete |
| ArcForges.Device.Runtime | Cloud.Client, Capabilities, Security, Execution; own-application registration/tool dispatch | No cross-app listener; WP17 fixture and WP26 real |
| ArcForges.Assistant.Abstractions | Foundation/Application.Abstractions; typed host ports and identities | None; WP14 |
| ArcForges.Assistant.Core | Assistant.Abstractions, Foundation, Capabilities; complete reusable assistant behavior | None; WP15 |
| ArcForges.Assistant.Persistence.Sqlite | Assistant.Core, Persistence.Sqlite; complete assistant schema/repositories/migrations | Existing SQLite runtime policy; WP15 |
| ArcForges.Assistant.Cloud | Assistant.Core, Cloud.Client, Device.Runtime; history/execution/recovery adapters | None; WP17, real WP26/52 |
| ArcForges.Assistant.Avalonia | Core, Cloud, Persistence.Sqlite, Desktop.Shell; complete embedded window | No implicit FFmpeg/OTIO dependency; WP17 |
| ArcForges.Native.Media | Foundation + Native.Abstractions; Probe/Decode/Encode/Audio/Resample capabilities | .Native.Media.Runtime.<rid>: FFmpeg and miniaudio |
| ArcForges.Native.Colour | Native.Abstractions; bounded immutable colour transforms | .Native.Colour.Runtime.<rid>: OpenColorIO |
| ArcForges.Native.Image | Native.Abstractions; image probe/decode/encode | .Native.Image.Runtime.<rid>: OpenImageIO/OpenEXR/Imath |
| ArcForges.Native.Graphics | Native.Abstractions; optional GPU surface/Metal bridge | .Native.Graphics.Runtime.<rid>, Metal only macOS; CPU fallback explicit |
| ArcForges.Native.Instruments | Native.Abstractions; device transport buffers/USB | .Native.Instruments.Runtime.<rid>: libusb; serial OS adapter |
| ArcForges.Native.Otio | Native.Abstractions; parse/serialize official Timeline plus fidelity report | .Native.Otio.Runtime.<rid>: official OTIO0.18.1 |
| ArcForges.Native.Pdf | Native.Abstractions; render page and extract bounded text only | .Native.Pdf.Runtime.<rid>: PDFium chromium/8044 |
| ArcForges.ContentSandbox.Contracts, .Broker | Exact ArcForges.Contracts.LocalRpc.Sandbox/Platform plus Foundation; Contracts facade has no duplicate authored/generated wire types. Broker owns restricted launch and buffer grants; helper loads selected parser wrappers | .ContentSandbox.Runtime.<rid>: signed AOT helper + OS enforcement profile, WP11 host/profile; WP13 production-parser composition |
| ArcForges.Build.Policy | Build-only, source/pin/NOTICE checks | No runtime dependency |
| ArcForges.Contracts.LocalRpc.Platform, .LocalRpc.Sandbox | Contracts-owned internal child records/services, launch/bootstrap/lease/hints/connector and complete parser controls; public clients cannot import | Generated C# messages/client/server bindings from authored proto, WP03 |
| ArcForges.Contracts.LocalRpc.Chat, .LocalRpc.Notes, .LocalRpc.Scope, .LocalRpc.Slate | Contracts-owned typed in-process product-port records; import shared public projections without duplicating them. No product listener, gRPC server registration or cross-product routing | Internal C# outputs; public clients and Cloud cannot import |
| ArcForges.Contracts.Foundation, .PublicApi, .Events, .Validation, .CloudInternal; ArcForges.Sdk.Contracts, ArcForges.Sdk.Client and ArcForges.Cli | Contracts-owned public versus internal graph; CloudInternal includes private Cloud and separately partitioned operator bindings. SDK/CLI cannot import internal protocols | No desktop native dependency |
| @arcforges/proto, @arcforges/api-client, @arcforges/contract-fixtures | Apache; protobuf-es + selected transport; no AGPL app import | No desktop native dependency |
| @arcforges/ai-internal | Internal HTTP generated types and validators | Apache-2.0; AI/Cloud import boundary only |
| @arcforges/operator-client | Internal operator proto messages, descriptors and selected client transport; separate from public and AI entry points | Apache-2.0; operator application only, never public Web, SDK or Android |
| io.github.arcforges:contracts-proto, :contracts-connect-client, :contract-fixtures | Public Java/Kotlin lite messages, Connect Kotlin gRPC-Web clients, independent fixtures respectively | Apache-2.0 JARs; Connect Kotlin gRPC-Web transport is selected by Android consumer, no desktop dependency |

Native.Abstractions holds status/ABI/build-manifest and safe lifetime wrappers, not media/domain entities. Consumers explicitly reference the managed package and exactly one matching .Runtime.<rid> package through RID-conditioned PackageReference; NuGet does not magically select a sibling RID package. Assets live runtimes/<rid>/native, signed in final app, load only app-owned read-only paths, with no PATH/user-writable fallback. RID set remains win-x64/win-arm64/osx-arm64/osx-x64/linux-x64/linux-arm64 under existing tiers. Normal consumer restore/build/publish never calls CMake/vcpkg; no “all desktop dependencies” metapackage.

Existing version/build-info/error ABI preambles stay compatible; functional ABI1.1 adds the complete typed functions under owned prefixes in [native ABI](contracts/06-native-functional-abi.md), preserving the published 1.0 probe/POD layout. C ABI uses fixed widths, explicit lengths, opaque handles, status+bounded error data, explicit allocation/free and callback deregistration before owner disposal. LibraryImport/SafeHandle wrappers own memory; no C++ exception, STL, native pointer or domain object crosses. Buffers may not outlive their handle unless explicitly copied; one handle is single-caller unless capability documents concurrent read. Existing native architecture remains the lifetime/concurrency/error authority.

**Admission dispositions resolved now.** OTIO selected as required official format interoperability, using upstream 0.18.1 and the existing pinned overlay (Apache-2.0, Imath/RapidJSON notices). A first-party managed JSON reader could parse a subset but would duplicate official schema upgrade/fidelity behavior; it is not the selected interoperability engine. Hostile parsing remains isolated. MDF is not a V1 required interchange format: keep arcscope-mdf-abi fenced/excluded from all release/package closures, and implement accepted tabular/event/native formats with managed adapters. This is an explicit no-adoption disposition, not “decide during WP35”. No unrelated acquisition feature is removed.

Native build record native-build.v1 fixes vcpkg36677bbd0b3bf11da7376e62e14bffcc54d2eaeb (current CI input); deployREADME9e593... is superseded. The owned wrappers use CMake 4.3.3/Ninja 1.13.1 and C++20/C17 ABI. Classic vcpkg retains the standard triplet names, architecture and linkage semantics, with no new manifest. The Windows producer uses its existing ignored `artifacts/vcpkg-installed` tree instead of a global installation. The narrow toolset pin described below supersedes the earlier blanket prohibition on triplet overlays. Pin gives FFmpeg 9.0.1, OpenColorIO 2.5.2, OpenImageIO 3.1.14.0, libusb1.0.30/miniaudio0.11.25; overlay OTIO0.18.1 includes existing source SHA512. FFmpeg core LGPL configuration disables GPL/nonfree components; no optional GPU SDK silently changes redistribution closure. PDFium uses verified chromium/8044 source/build identity and full BSD/third-party notices; build in Platform isolated profile, not a dependency downloaded by clients. The exact platform library closure/signatures/SBOM are candidate build outputs and release gates, not a claim already built here.

**Local development reuse (2026-09-20).** Follow the [WP02.00 toolchain profile](../assurance/wp02-00-toolchain-profile.md): prefer existing installed vcpkg and dependencies for successful local compilation, without a mandatory reinstall or global installation change. The following exact toolset requirements govern admitted producer candidates; local compatible-build evidence must retain its actual tool identity.

**Windows producer toolset pin (2026-09-19).** The current reviewed Windows closure uses MSVC toolset directory `14.51.36231` and the separately recorded Microsoft runtime DLL version `14.51.36247.0`. vcpkg otherwise selects the latest installed minor toolset, which can differ from the default selected by the owned wrapper build. DesktopPlatform owns two minimal triplet overlays that include the pinned standard `x64-windows` and `x64-windows-static-md` definitions and select that exact toolset. They preserve the upstream architecture/linkage/feature choices and hash the included standard definitions; they do not create product-specific dependency variants. Both dependency builds and owned wrappers must select the reviewed compiler. The vcpkg script/build generator is CMake 4.4.0 from its pinned tools manifest, distinct from the wrapper generator. Actual build caches and installed ABI records, including the overlay identity, accompany candidate verification. An unreviewed toolset or generator fails closed. A future toolset/runtime upgrade requires new provenance and compatibility evidence before distribution, under the [native and compiler-runtime profiles](../assurance/reference-coverage-and-provenance.md#33-existing-native-distribution-closure); no existing package/ABI identity changes here.

Under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017), CI order is necessary static/offline checks → Windows/Linux compilation and applicable AOT compilation → pack once → required licence/provenance/signing and candidate identity checks → publish those same bytes. CI does not run installed-package consumers, native/runtime probes, sandbox execution or macOS jobs. Relevant runtime/consumer diagnostics run locally only when the existing environment supports the affected behavior; missing coverage remains explicit. ABI major change requires a new package major and affected compatibility evidence; a compatible patch validates its affected capability without repeating unrelated passing checks.

Each functional native managed package includes its versioned C17 headers under build/native/include/arc and ABI fixture manifest; the matching RID runtime contains the actual shared libraries. A clean C17 consumer dynamically resolves only the declared exports from those packaged assets (no adjacent headers or source). Header/descriptor and binary ABI manifest versions must agree before load.
