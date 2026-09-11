# Solution and Project Layout

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** (contract granularity), **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** (licence boundaries), **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** (implementation target)
> Companions: [`00-architecture-overview.md`](00-architecture-overview.md), [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`14-build-packaging-and-release.md`](14-build-packaging-and-release.md)

The implementation targets are the ten repositories selected by [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009). This document fixes source ownership and package boundaries before WP01 creates/reconciles those roots.

---

## 1. Repository ownership and dependency graph

The ten repositories are ArcForges-DesktopPlatform, ArcChat, ArcNotes, ArcScope, ArcSlate, ArcForges-Cloud, ArcForges-AI, ArcForges-Web, ArcForges-Mobile and ArcForges-Contracts. Keep Design and Plan separately. The existing implementation history becomes DesktopPlatform; other roots are new. Retire old monorepo application scaffolds after their disposition is recorded, without treating placeholders as missing design.

| Existing group | Sole target / disposition |
|---|---|
| native/, CMake, vcpkg overlay/toolchain, native tests | DesktopPlatform / retained foundation, selected packages below |
| BuildingBlocks Foundation/Application.Abstractions/Execution/Persistence/Observability/Security/Update; DesignSystem/Desktop.Shell | DesktopPlatform / mechanism-only managed packages; separate headless vs desktop closures |
| BuildingBlocks CloudClient and public value/validator types | Contracts / generated public C# and TS clients and Apache primitives |
| Public/Internal Contracts and Sdk/CLI/generators | Contracts / handwritten proto, explicit license directories, released tools/fixtures |
| ArcChat domain/application/adapters/Hub/Agent/LocalTools | ArcChat / product-owned rewrite or relocate; Hub stays in-process, Agent is a Cloud client |
| ArcNotes, ArcScope, ArcSlate groups | Matching product / no cross-product project reference; owned domain/storage/native consumer adapters |
| Cloud.Host/PublicApi/Persistence/Modules/BackgroundJobs/Migrations | Cloud / single AOT host, one-shot migrator, ordinary leased jobs; no role-selected Worker/AgentHost |
| Cloud.AgentRuntime | Retire the loop scaffold; AI owns the TS Workflow. Cloud may retain this C# library name for typed Agent/Task dispatch/control/reconciliation ports only |
| Cloud.Realtime | Cloud EventService bounded hint polling; AI stream DO in AI |
| Mobile.Core/ArcChat.Mobile | Mobile / RN application and Apache TS domain/client state; retire MAUI projects |
| Web apps/UI/testing/esproj | Web / Site, Account, Chat, operator and status build profiles, one npm lock |
| ContentSandbox/helper broker | DesktopPlatform / per-RID packaged restricted helper; product invocation stays in product |
| eng/build/packaging/policy | DesktopPlatform reusable tooling package/workflow, owner-specific thin invocation files |
| eng/terraform/deploy/migrations/integration E2E | Cloud / environment infra and integration manifest; AI owns wrangler config, Web owns asset build |
| Contract fixtures | Contracts / immutable public/internal wire/profile vectors |
| Product/native/format/performance fixtures and tests | Owning product or Platform; cross-provider integration orchestrated by Cloud manifest |
| StartArcForges outputs / ReactApp2 template references | Read-only evidence only, no build dependency or extra repository |

Within each C# product: Domain ← Application ← Infrastructure/LocalRpc/CloudClient/Desktop. Domain imports no transport/UI/native code. Across repositories only exact packages/artifacts/workflow commits; no ProjectReference, source-link import, submodule or sibling checkout build. Platform depends on Contracts, never on a product/Cloud/AI implementation; product/Cloud depends on selected Platform/Contracts packages; AI/Web/Mobile depend on allowed Contracts npm artifacts. Cloud never depends on native/UI/helper packages. An integration manifest is evidence about compatible independent versions, not a family release lockstep.

### Root and logical-path convention

Each .NET repository owns global.json, Directory.Build.props/targets, Directory.Packages.props, NuGet.config, committed per-project package locks, a managed .slnx, eng/, src/ and tests/. DesktopPlatform additionally owns native/, CMakePresets and vcpkg inputs; only its Windows IDE solution composes native builds. Each TS repository owns package.json/package-lock.json, .node-version, tooling/ and tests/. Web owns its esproj/win.slnx; no Cloud project references that esproj. Mobile owns android/ and deferred ios/; AI owns src/worker.ts, src/workflows/, src/streams/, src/providers/workers-ai/, src/inference/ and wrangler.jsonc. RunWorkflow is the sole agent loop; InferenceWorkflow and object verification are fixed-stage bounded job handlers in that same deployment.

Logical .NET suffixes such as src/ArcNotes/ArcNotes.Domain and src/Cloud/ArcForges.Cloud.Modules.Task are relative to the sole repository assigned in the table above. They do not identify a shared checkout. Contracts uses public/proto, internal/proto, public/http, internal/ai-http, src/public, src/internal and fixtures/public|internal; Web uses apps/site, apps/app and packages/ui. This convention applies to the remaining diagrams and work-package paths. Source suffix renaming inside an owner is an internal implementation choice; owner/package boundaries are fixed.

---

## 2. Project conventions

**Approved helper projects ([P2-007](../decisions/phase-2-specification-decisions.md#rule-p2-007)).** `src/DesktopHelpers/ArcForges.ContentSandbox` is a signed first-party C# Native AOT executable with no product-domain/Harness/store dependency. `ArcForges.ContentSandbox.Contracts` contains only generated bounded parent-child DTOs; `ArcForges.ContentSandbox.Broker` owns launch profiles and handle/resource budgets. Product-specific approved parser wrappers are loaded only in that helper. Native library adaptation remains narrow; no C++ business host or cross-product shared pool is introduced. [WP-11.09](../planning/work-packages/11-security-foundation.md#rule-wp-11.09) supplies this boundary before [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04) or media ingestion depends on it.

| # | Rule |
|---|---|
| <a id="rule-pj-01"></a>PJ-01 | **One responsibility per project.** A project that is both a domain and an adapter is a defect. |
| <a id="rule-pj-02"></a>PJ-02 | **Every .NET library consumed by an AOT deliverable sets IsAotCompatible; each AOT host sets PublishAot.** Node/TS packages and esproj never inherit .NET runtime properties. |
| PJ-03 | Local RPC uses generated protobuf/gRPC bindings and explicit service registration; no runtime attach/interceptor reflection path. |
| <a id="rule-pj-04"></a>PJ-04 | **NuGet versions use Directory.Packages.props; Web versions use exact npm manifest pins and the one workspace lock.** JavaScript SDK/Node versions have their own reviewed toolchain pins; no accidental inline NuGet override. |
| <a id="rule-pj-05"></a>PJ-05 | **Each .NET packages.lock.json and the Web package-lock.json are committed.** CI uses locked dotnet restore and npm ci; esproj disables implicit npm install. |
| <a id="rule-pj-06"></a>PJ-06 | **Preview packages never enter a stable branch's core path.** |
| <a id="rule-pj-07"></a>PJ-07 | **.NET code follows nullable/implicit-usings/analyzer/SourceLink policy; TypeScript follows strict compiler, import-boundary and lint policy.** Deterministic builds, UTF-8/LF formatting and reproducible provenance cover both. |
| <a id="rule-pj-08"></a>PJ-08 | **Warnings as errors**, enabled repository-wide once staged debt is cleared; trimming and AOT diagnostics are always errors on AOT deliverables. |
| <a id="rule-pj-09"></a>PJ-09 | **Every project/package declares its SPDX licence and boundary.** .NET uses project metadata, npm uses package metadata; public generated SDK and product UI dependency graphs are audited separately. |

---

## 3. Contract packages

Mobile and Contracts public/proto, public/http, src/public, public SDK/CLI and public fixtures are Apache-2.0. Internal proto/HTTP and implementation in Platform/Cloud/AI/Web/four desktop repositories retain AGPL-3.0-only; upstream dependencies keep their original notices. Public SDK extension protocol is Apache even though first-party product RPC is internal AGPL. Generated files inherit the authored schema boundary and generator's required runtime notices; tools do not relabel input expression. Mobile cannot import Web application/UI/testing expression; shared public tests originate in Contracts public fixtures. Internal tests may consume public fixtures, never the reverse.

Package metadata declares owner/SPDX/source commit, schema/package version, dependency closure, NOTICE and SBOM. Public npm access=public, NuGet public registry; AGPL packages may be publicly distributed with source/notice obligations. Per-RID native license closure includes static dependencies and optional codec features, not merely the wrapper's license. Six reference-source access/exclusion/provenance boundaries and all archive prohibitions stay unchanged. Source review and actual distributable license gate remain evidence obligations; this amendment does not claim third-party code has been copied or audited by a runtime test.

The [wire registry](contracts/04-protobuf-wire-registry.md) defines every service/message/field and the public/internal package split. Generated C# and TS output is not hand-edited. The [CF HTTP schema](contracts/05-cloudflare-integration.md) is the explicit AI/object exception. Contract validators validate shape/profile; business validation remains in the owner.

| # | Rule |
|---|---|
| CT-01 | Independent product changes cannot force unrelated product releases. |
| CT-02 | Handwritten proto in Contracts is the sole business wire source; C#/TS clients are generated. |
| CT-03 | Contracts contain no business implementation. |
| CT-04 | Contracts have no UI/ORM/native/host dependency. |
| CT-05 | C# contract libraries satisfy the Native AOT gate. |
| CT-06 | Cloud/public browser clients never import local product RPC packages. |
| CT-07 | Public business records expose no local IPC/native handles. |
| CT-08 | Foundation remains stable and bounded; domain services own their own types. |

---

## 4. Licence boundary enforcement

| # | Rule |
|---|---|
| LB-01 | Every .NET project declares PackageLicenseExpression/LicenceBoundary; npm packages declare license and the equivalent repository boundary metadata. The generated TS public SDK is Apache; Web product UI is AGPL. |
| LB-02 | **No AGPL source/package enters an Apache dependency closure.** Check .NET references and npm imports/dependencies, including generators and copied component provenance where applicable. |
| LB-03 | **A dependency test asserts that the mobile distributable's complete direct and transitive closure is compatible with Apache-2.0 application distribution and applicable store terms** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** obligation 7). |
| LB-04 | **`NOTICE` files are generated from the dependency graph**, per boundary, as part of packaging. |
| LB-05 | **SBOM generation runs per deliverable**, and its output is a release artifact. |
| LB-06 | **On discovery of a conflicting contribution or dependency in the mobile boundary, the issue is registered and returned for decision.** Silently adding an exception, changing the licence, or removing the mobile distribution target is prohibited (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |
| <a id="rule-lb-07"></a>LB-07 | **Reference-repository reuse requires the nine-field provenance record before any copy, translation, port or structural reuse** (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**), recorded in [`../assurance/reference-coverage-and-provenance.md`](../assurance/reference-coverage-and-provenance.md). |

---

## 5. Cloud module projects

The 20 domain owners in the [Cloud schema map](data-model/01-cloud-data-model.md#1-schema-map) are authoritative; `platform` is shared infrastructure, not a domain module. The usual project arrangement is a pair: `ArcForges.Cloud.Modules.<Name>` (application and domain) and `ArcForges.Cloud.Modules.<Name>.Infrastructure` (persistence and integrations), plus tests. An equivalent bounded project partition is permitted if ownership and reference rules remain enforceable; schema ownership does not require a fixed project count.

Modules: **Identity**, **Workspace**, **Devices**, **Entitlement**, **Commerce**, **Chat**, **Task**, **Agent**, **Sync**, **Resource**, **Search**, **Notification**, **Policy**, **Audit**, **Support**, **TrustSafety**, **Notes**, **Scope**, **Slate**, **Configuration**.

| # | Rule |
|---|---|
| CM-01 | **A module owns its schema or its explicit table set.** No other module writes those tables. |
| CM-02 | **Cross-module interaction is through a module's public API or its published events**, never through its persistence. |
| CM-03 | **An architecture test asserts module persistence ownership.** |
| CM-04 | **All modules ship inside the single Cloud Host.** A future change to deployment topology requires an accepted architecture decision; a project split is not permission to add deployment roles. |

---

## 6. Reference direction

```
Desktop / LocalRpc / Infrastructure / MinimalApi / React Native adapters
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
| RD-01 | Domain references neither Application, Infrastructure, UI nor Contracts. |
| RD-02 | Application depends only on Domain plus abstractions. |
| RD-03 | Infrastructure implements Application's ports. |
| RD-04 | A generated local/public wire DTO never becomes a domain entity. |
| RD-05 | A UI model never becomes a transport DTO. |
| RD-06 | Typed HTTP client interfaces exist only inside the public API client contract boundary. |
| RD-07 | Local RPC interfaces exist only inside the local RPC contract boundary. |
| RD-08 | Realtime DTOs are never the canonical persisted domain events. |
| RD-09 | Products never reference each other's Domain, Application or Infrastructure. |
| RD-10 | The design system and desktop shell reference no product domain. |

---

## 7. Architecture and repository-policy tests

These are release gates, not advisory checks (`§23` of the quality contract).

### 7.1 Architecture tests

| # | Assertion |
|---|---|
| <a id="rule-at-01"></a>AT-01 | Domain references no UI, infrastructure, transport or database provider assembly |
| AT-02 | A local RPC adapter references no view model or control type |
| AT-03 | A public API adapter references no UI type |
| AT-04 | Contracts reference no platform-specific type |
| AT-05 | Products do not reference each other's Domain, Application or Infrastructure |
| AT-06 | Native pointers and `SafeHandle` types do not cross the native adapter boundary |
| AT-07 | A Cloud module does not reach into another module's persistence |
| AT-08 | No catch-all string/object RPC entry point exists |
| AT-09 | No long-lived C++ worker executable project enters the release graph |
| AT-10 | The reflection-based typed-HTTP-client package is absent from C# production dependency graphs; browser HTTP uses generated TS SDK imports. |
| AT-11 | Every local service implements its generated proto contract and maps explicitly to its owner application port. |
| AT-12 | Every wire type is generated from the owned proto or exception JSON schema; runtime serializers/validators agree with the released descriptors. |
| AT-13 | Every module's public surface is reachable only through its declared API |
| <a id="rule-at-14"></a>AT-14 | The design system and shell reference no product domain assembly |

### 7.2 Repository-policy tests

| # | Assertion |
|---|---|
| <a id="rule-rp-01"></a>RP-01 | **No forbidden alias or obsolete product name** appears in `src/`, `tests/`, `eng/`, identifiers or resource strings — `ArcCanvas`, `ArcMusic`, `ArcImage`, `ArcVideo`, and the superseded payment provider (**[D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002)**, **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)**) |
| RP-02 | Every project declares an SPDX licence identifier and a licence boundary |
| RP-03 | No `AGPL` project is referenced from an `Apache` project |
| RP-04 | The mobile distributable's dependency closure passes the licence policy |
| RP-05 | NuGet versions obey central management; npm versions/lock and JavaScript SDK pins obey the declared Web policy. |
| RP-06 | Each toolchain lock is present/current; there is exactly one Web npm root and no nested lockfile. |
| RP-07 | No blanket suppression of trimming or AOT diagnostics exists |
| RP-08 | Every glossary-forbidden term is absent from new authoritative text |
| RP-09 | No secret-shaped literal is committed |
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
| FX-01 | **Golden fixtures are permanent and immutable.** A fixture is added, never edited. |
| FX-02 | **Every historical native format version has a fixture.** |
| FX-03 | **Serialized golden vectors exist for every wire contract** — exact bytes for representative messages. |
| FX-04 | **Fixtures come from several sources**: synthesised, captured with consent and redaction, and edge cases. **Unredacted real user data never enters the repository.** |
| FX-05 | **Scale corpora are declared by manifest**, generated deterministically rather than committed as large binaries where possible. |

---

## 10. Reconciliation and repository split

**[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)**: the existing repository's scaffolds and code are **implementation-state evidence, never design authority**, and may be retained, restructured, replaced or removed as the accepted design requires.

| # | Rule |
|---|---|
| MG-01 | **Migration proceeds one vertical slice at a time.** A slice is complete when its contract, application, infrastructure, adapter, tests and gates all conform. |
| MG-02 | **The architecture and policy tests are introduced early and grow**, so conformance is ratcheted rather than promised. |
| MG-03 | **Existing code that has not yet been migrated is fenced**, so it cannot be referenced from conforming projects. |
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

Publish the following package identities. Managed package versions and their compatible ABI range are independent from product versions. A native candidate has version 1.0.0-ci.<run>, stable starts1.0.0; never overwrite an existing package/version. Producer release manifests list SHA256 and exact dependencies.

| Package family | Dependencies / public C# capability | Native RID assets |
|---|---|---|
| ArcForges.Foundation, .Application.Abstractions | Contracts.Foundation; IDs are adapters, not duplicate wire types | None; headless |
| ArcForges.Observability | Foundation; bounded Activity/Meter/logging, no product telemetry schema | None; headless |
| ArcForges.Persistence | Foundation; desktop SQLite/journal mechanics, no product schema/Cloud Npgsql | None in managed package; SQLite runtime independently selected |
| ArcForges.Security, .Update, .Execution | Foundation; OS secret/approval adapters, signed updates, ProductJob mechanics | Explicit OS adapters; Cloud may consume only documented headless subpackages |
| ArcForges.DesignSystem, .Desktop.Shell | Foundation plus Avalonia; shell also DesignSystem | Avalonia asset closure; product apps own flows |
| ArcForges.Native.Media | Foundation + Native.Abstractions; Probe/Decode/Encode/Audio/Resample capabilities | .Native.Media.Runtime.<rid>: FFmpeg and miniaudio |
| ArcForges.Native.Colour | Native.Abstractions; bounded immutable colour transforms | .Native.Colour.Runtime.<rid>: OpenColorIO |
| ArcForges.Native.Image | Native.Abstractions; image probe/decode/encode | .Native.Image.Runtime.<rid>: OpenImageIO/OpenEXR/Imath |
| ArcForges.Native.Graphics | Native.Abstractions; optional GPU surface/Metal bridge | .Native.Graphics.Runtime.<rid>, Metal only macOS; CPU fallback explicit |
| ArcForges.Native.Instruments | Native.Abstractions; device transport buffers/USB | .Native.Instruments.Runtime.<rid>: libusb; serial OS adapter |
| ArcForges.Native.Otio | Native.Abstractions; parse/serialize official Timeline plus fidelity report | .Native.Otio.Runtime.<rid>: official OTIO0.18.1 |
| ArcForges.Native.Pdf | Native.Abstractions; render page and extract bounded text only | .Native.Pdf.Runtime.<rid>: PDFium chromium/8044 |
| ArcForges.ContentSandbox.Contracts, .Broker | Foundation + bounded helper DTOs; Broker references helper Contracts only; isolated helper references selected parser wrappers | .ContentSandbox.Runtime.<rid>: signed AOT helper + OS enforcement profile |
| ArcForges.Build.Policy | Build-only, source/pin/NOTICE checks | No runtime dependency |
| ArcForges.Contracts.Foundation/PublicApi/Events/Validation/LocalRpc.<owner>/CloudInternal; ArcForges.Sdk.* and ArcForges.Cli | Contracts-owned generated/public vs internal graph | No desktop native dependency |
| @arcforges/proto, @arcforges/api-client, @arcforges/rn-transport, @arcforges/contract-fixtures | Apache; protobuf-es + selected transport; no AGPL app import | No desktop native dependency |
| @arcforges/ai-internal | Internal HTTP generated types and validators | AGPL; AI/Cloud integration only |

Native.Abstractions holds status/ABI/build-manifest and safe lifetime wrappers, not media/domain entities. Consumers explicitly reference the managed package and exactly one matching .Runtime.<rid> package through RID-conditioned PackageReference; NuGet does not magically select a sibling RID package. Assets live runtimes/<rid>/native, signed in final app, load only app-owned read-only paths, with no PATH/user-writable fallback. RID set remains win-x64/win-arm64/osx-arm64/osx-x64/linux-x64/linux-arm64 under existing tiers. Normal consumer restore/build/publish never calls CMake/vcpkg; no “all desktop dependencies” metapackage.

Existing version/build-info/error ABI preambles stay compatible; capability ABI major1 adds functions under owned prefixes. C ABI uses fixed widths, explicit lengths, opaque handles, status+bounded error data, explicit allocation/free and callback deregistration before owner disposal. LibraryImport/SafeHandle wrappers own memory; no C++ exception, STL, native pointer or domain object crosses. Buffers may not outlive their handle unless explicitly copied; one handle is single-caller unless capability documents concurrent read. Existing native architecture remains the lifetime/concurrency/error authority.

**Admission dispositions resolved now.** OTIO selected as required official format interoperability, using upstream0.18.1 and the existing pinned overlay (Apache-2.0, Imath/RapidJSON notices). A first-party managed JSON reader could parse a subset but would duplicate official schema upgrade/fidelity behavior; it is not the selected interoperability engine. Hostile parsing remains isolated. MDF is not a V1 required interchange format: keep arcscope-mdf-abi fenced/excluded from all release/package closures, and implement accepted tabular/event/native formats with managed adapters. This is an explicit no-adoption disposition, not “decide during WP35”. No unrelated acquisition feature is removed.

Native build record native-build.v1 fixes vcpkg36677bbd0b3bf11da7376e62e14bffcc54d2eaeb (current CI input); deployREADME9e593... is superseded. CMake 4.3.3/Ninja 1.13.1, C++20/C17 ABI; classic vcpkg standard triplets, no new manifest/custom triplets/local installed tree. Pin gives FFmpeg 9.0.1, OpenColorIO 2.5.2, OpenImageIO 3.1.14.0, libusb1.0.30/miniaudio0.11.25; overlay OTIO0.18.1 includes existing source SHA512. FFmpeg core LGPL configuration disables GPL/nonfree components; no optional GPU SDK silently changes redistribution closure. PDFium uses verified chromium/8044 source/build identity and full BSD/third-party notices; build in Platform isolated profile, not a dependency downloaded by clients. The exact platform library closure/signatures/SBOM are candidate build outputs and release gates, not a claim already built here.

CI order: module tests/fuzz+ABI → produce candidate managed/RID packages → isolated feed restore into clean consumer → Native AOT publish/run per RID with sandbox on → compare ABI/NOTICE/SBOM → publish same tested bytes to nuget.org. ABI major change requires new package major and all affected consumers' compatibility proof; compatible patch retests all consumers of that capability, not unrelated products.
