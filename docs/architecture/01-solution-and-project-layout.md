# Solution and Project Layout

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** (contract granularity), **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** (licence boundaries), **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** (implementation target)
> Companions: [`00-architecture-overview.md`](00-architecture-overview.md), [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`14-build-packaging-and-release.md`](14-build-packaging-and-release.md)

The implementation target is the existing monorepo at `C:\MyFile\ArcForges\ArcForges` (**[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)**). This document specifies the **target layout**. It is a logical structure: migration lands one vertical slice at a time and does not require moving every directory at once.

---

## 1. Repository layout

```
ArcForges/
├─ global.json                       pinned SDK feature band
├─ Directory.Build.props             shared build properties
├─ Directory.Build.targets           shared targets
├─ Directory.Packages.props          central package management
├─ NuGet.config
├─ packages.lock.json                committed; CI restores in locked mode
├─ ArcForges.slnx                     managed-only portable solution
├─ win.slnx                           Windows IDE: managed + native + Web esproj
│
├─ eng/
│  ├─ build/                         build scripts and shared MSBuild logic
│  ├─ packaging/                     installers, bundles, store packaging
│  ├─ versioning/                    version axes, release manifest generation
│  ├─ policy/                        licence policy, banned-symbol lists, forbidden-term lists
│  └─ terraform/                     cloud infrastructure as code, per environment
│
├─ src/
│  ├─ BuildingBlocks/                mechanism only — never domain
│  │  ├─ ArcForges.Foundation/
│  │  ├─ ArcForges.Application.Abstractions/
│  │  ├─ ArcForges.Persistence/
│  │  ├─ ArcForges.Observability/
│  │  ├─ ArcForges.Security/
│  │  ├─ ArcForges.CloudClient/
│  │  ├─ ArcForges.Update/
│  │  └─ ArcForges.NativeInterop/
│  │
│  ├─ Contracts/                     see §3 for the full split
│  │  ├─ Public/                     Apache-2.0 interoperability boundary
│  │  └─ Internal/                   AGPL-3.0-only
│  │
│  ├─ DesignSystem/
│  │  ├─ ArcForges.DesignSystem/                 tokens, typography, icons, density, motion
│  │  └─ ArcForges.Desktop.Shell/                windows, panels, commands, settings, attention
│  │
│  ├─ ArcChat/
│  │  ├─ ArcChat.Domain/
│  │  ├─ ArcChat.Application/
│  │  ├─ ArcChat.Infrastructure/
│  │  ├─ ArcChat.LocalRpc/                       adapter: hosts + consumes local contracts
│  │  ├─ ArcChat.Hub/                            platform coordination plane
│  │  ├─ ArcChat.Agent/                          agent runtime, turn loop, capability registry
│  │  ├─ ArcChat.LocalTools/                     first-party local capabilities ArcChat owns
│  │  ├─ ArcChat.CloudClient/
│  │  ├─ ArcChat.Desktop/                        Avalonia host — PublishAot
│  │  └─ ArcChat.Tests.*/
│  │
│  ├─ ArcNotes/          Domain · Application · Infrastructure · LocalRpc · CloudClient · Desktop · Tests
│  ├─ ArcScope/          Domain · Application · Infrastructure · Acquisition · LocalRpc · CloudClient · Desktop · Tests
│  ├─ ArcSlate/          Domain · Application · Infrastructure · Media · LocalRpc · CloudClient · Desktop · Tests
│  │
│  ├─ Cloud/
│  │  ├─ ArcForges.Cloud.Host/                   the single deployable host (§2 of the cloud architecture)
│  │  ├─ ArcForges.Cloud.AgentRuntime/           the single Harness — a library
│  │  ├─ ArcForges.Cloud.BackgroundJobs/         hosted services — a library
│  │  ├─ ArcForges.Cloud.AppHost/                Aspire local-development orchestration only
│  │  ├─ ArcForges.Cloud.PublicApi/              endpoint mapping
│  │  ├─ ArcForges.Cloud.Realtime/               hubs
│  │  ├─ ArcForges.Cloud.Persistence/
│  │  ├─ ArcForges.Cloud.Migrations/             standalone migrator
│  │  └─ ArcForges.Cloud.Modules.*/              one project pair per module (§5)
│  │
│  ├─ Mobile/
│  │  ├─ ArcForges.Mobile.Core/                  Apache-2.0 — application semantics, no UI
│  │  └─ ArcChat.Mobile/                         Apache-2.0 — MAUI application
│  │
│  ├─ Web/
│  │  ├─ package.json / package-lock.json        one private npm workspace and lock
│  │  ├─ ArcForges.Web.esproj                    win.slnx integration only
│  │  ├─ ArcForges.Web.App/                      React/TypeScript Account + Chat profiles
│  │  ├─ ArcForges.Web.Site/                     React/TypeScript static generation
│  │  ├─ packages/sdk/                          generated Apache TS SDK + wire validators
│  │  ├─ packages/ui/                           owned AGPL Web design system
│  │  └─ tooling/ · tests/                      typed Node commands and browser tests
│  │
│  ├─ Sdk/                                       Apache-2.0 public SDK
│  │  ├─ ArcForges.Sdk.Foundation/
│  │  ├─ ArcForges.Sdk.Extensions/
│  │  ├─ ArcForges.Sdk.Generators/
│  │  └─ ArcForges.Cli/                          the developer CLI
│  │
│  └─ Tools/                                     build/migration tooling (Technical Exception D)
│
├─ native/
│  ├─ media-abi/                                 thin extern "C" shim for ArcSlate
│  └─ acquisition-abi/                           thin extern "C" shim for ArcScope where required
│
├─ tests/
│  ├─ ArchitectureTests/
│  ├─ RepositoryPolicyTests/
│  ├─ ContractCompatibilityTests/
│  ├─ PublicApiContractTests/
│  ├─ LocalRpcAotTests/
│  ├─ RealtimeReconnectTests/
│  ├─ MigrationTests/
│  ├─ NativeAbiTests/
│  ├─ EndToEndTests/
│  └─ Performance/
│
├─ fixtures/                                     golden fixtures — permanent, immutable
│  ├─ formats/                                   one directory per historical format version
│  ├─ wire/                                      serialized golden vectors
│  └─ corpora/                                   scale corpora manifests
│
└─ docs/                                         implementation-facing notes only; design lives in ArcForges-Design
```

---

### 1.1 Web toolchain boundary

[P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) adds the Node/npm workspace defined in [Web toolchain and SDK](25-web-toolchain-and-sdk.md). Windows win.slnx includes one esproj; focused solution filters select the same projects. Portable .NET projects/ArcForges.slnx never reference esproj, and Cloud publish never bundles or builds Web. Non-Windows development opens src/Web and runs npm independently, alongside the existing dotnet and CMake entry points. CI joins artifact dependencies explicitly.

---

## 2. Project conventions

**Approved helper projects ([P2-007](../decisions/phase-2-specification-decisions.md#rule-p2-007)).** `src/DesktopHelpers/ArcForges.ContentSandbox` is a signed first-party C# Native AOT executable with no product-domain/Harness/store dependency. `ArcForges.ContentSandbox.Contracts` contains only generated bounded parent-child DTOs; `ArcForges.ContentSandbox.Broker` owns launch profiles and handle/resource budgets. Product-specific approved parser wrappers are loaded only in that helper. Native library adaptation remains narrow; no C++ business host or cross-product shared pool is introduced. [WP-11.09](../planning/work-packages/11-security-foundation.md#rule-wp-11.09) supplies this boundary before [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04) or media ingestion depends on it.

| # | Rule |
|---|---|
| <a id="rule-pj-01"></a>PJ-01 | **One responsibility per project.** A project that is both a domain and an adapter is a defect. |
| <a id="rule-pj-02"></a>PJ-02 | **Every .NET library consumed by an AOT deliverable sets IsAotCompatible; each AOT host sets PublishAot.** Node/TS packages and esproj never inherit .NET runtime properties. |
| PJ-03 | **Every project on a local-RPC attach chain enables the StreamJsonRpc interceptors property.** |
| <a id="rule-pj-04"></a>PJ-04 | **NuGet versions use Directory.Packages.props; Web versions use exact npm manifest pins and the one workspace lock.** JavaScript SDK/Node versions have their own reviewed toolchain pins; no accidental inline NuGet override. |
| <a id="rule-pj-05"></a>PJ-05 | **Each .NET packages.lock.json and the Web package-lock.json are committed.** CI uses locked dotnet restore and npm ci; esproj disables implicit npm install. |
| <a id="rule-pj-06"></a>PJ-06 | **Preview packages never enter a stable branch's core path.** |
| <a id="rule-pj-07"></a>PJ-07 | **.NET code follows nullable/implicit-usings/analyzer/SourceLink policy; TypeScript follows strict compiler, import-boundary and lint policy.** Deterministic builds, UTF-8/LF formatting and reproducible provenance cover both. |
| <a id="rule-pj-08"></a>PJ-08 | **Warnings as errors**, enabled repository-wide once staged debt is cleared; trimming and AOT diagnostics are always errors on AOT deliverables. |
| <a id="rule-pj-09"></a>PJ-09 | **Every project/package declares its SPDX licence and boundary.** .NET uses project metadata, npm uses package metadata; public generated SDK and product UI dependency graphs are audited separately. |

---

## 3. Contract projects

**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** rejects a single ever-growing contracts assembly. Contracts split by **communication boundary**, **product/domain ownership**, **release cadence** and **licence boundary**.

### 3.1 Apache-2.0 — public interoperability

| Project | Contents |
|---|---|
| `ArcForges.Contracts.Foundation` | Stable serialized identifiers and primitives: `AppId`, `InstanceId`, `WorkspaceId`, `ResourceId`, `CommandId`, `TaskId`, `RunId`, `StepId`, `AttemptId`, `InvocationId`; revision and sequence base types; `ArcResult<T>` and `ArcError`; `ResourceRef`, `ArtifactRef`, `TaskHandle`, `TaskSnapshot`; pagination, time and base enumerations |
| `ArcForges.Contracts.PublicApi` | Public request/response DTOs, route and version constants, typed client interfaces, source-generated serialization contexts |
| `ArcForges.Contracts.Realtime` | Realtime method-name constants, event envelopes, sequence and revision recovery information, source-generated serialization contexts |
| `ArcForges.Contracts.Validation` | Contract-level validators expressing **wire-format constraints only** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**) |
| `ArcForges.Sdk.*` | The public SDK surface (see [`15-extension-platform-architecture.md`](15-extension-platform-architecture.md)) |

### 3.2 AGPL-3.0-only — internal

| Project | Contents |
|---|---|
| `ArcForges.Contracts.LocalRpc.Hub` | Registration, discovery, lease, heartbeat, approval coordination, local routing, local connection events |
| `ArcForges.Contracts.LocalRpc.ArcNotes` | `INotesLocalRpc` and its DTOs |
| `ArcForges.Contracts.LocalRpc.ArcScope` | `IScopeLocalRpc` and its DTOs |
| `ArcForges.Contracts.LocalRpc.ArcSlate` | `ISlateLocalRpc` and its DTOs |
| `ArcForges.Contracts.LocalRpc.ArcChat` | ArcChat's own outward local contract |
| `ArcForges.Contracts.CloudInternal` | Cloud-internal module contracts and events |

| # | Rule |
|---|---|
| CT-01 | **A contract change owned by one product must not force an unrelated product to re-release** (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**). This is why local RPC contracts are split per owning product. |
| CT-02 | **C# DTOs and endpoint metadata are the source of truth.** OpenAPI and JSON Schema artifacts are **generated** from them; parallel handwritten schemas that can drift are prohibited (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**). |
| CT-03 | **No business implementation in a contracts package** (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**). |
| CT-04 | **Contracts reference no UI type, no ORM, no database provider, no native library and no specific host.** |
| CT-05 | **Every contracts project treats trimming and AOT compatibility as a hard gate.** |
| CT-06 | **Local RPC contracts are never referenced by the browser or by the Cloud host.** |
| CT-07 | **Public API contracts never expose local IPC concepts, native handles or desktop implementation details.** |
| CT-08 | **The foundation contract package is small and stable by policy.** Adding to it requires a decision record, because everything depends on it. |

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

Each Cloud module is a pair: `ArcForges.Cloud.Modules.<Name>` (application and domain) and `ArcForges.Cloud.Modules.<Name>.Infrastructure` (persistence and integrations), plus tests.

Modules: **Identity**, **Workspace**, **Devices**, **Entitlement**, **Commerce**, **Chat**, **Task**, **Agent**, **Sync**, **Resource**, **Search**, **Notification**, **Policy**, **Audit**, **Support**, **TrustSafety**.

| # | Rule |
|---|---|
| CM-01 | **A module owns its schema or its explicit table set.** No other module writes those tables. |
| CM-02 | **Cross-module interaction is through a module's public API or its published events**, never through its persistence. |
| CM-03 | **An architecture test asserts module persistence ownership.** |
| CM-04 | Modules are split into separate deployment roles only when there is demonstrated need for independent scaling, isolation, security or ownership. |

---

## 6. Reference direction

```
Desktop / LocalRpc / Infrastructure / MinimalApi / MAUI adapters
                                 ↓
                          Application
                                 ↓
                             Domain

Contracts.Foundation  ←  Contracts.PublicApi
Contracts.Foundation  ←  Contracts.Realtime
Contracts.Foundation  ←  Contracts.LocalRpc.*
```

Hard rules, all enforced by architecture tests:

| # | Rule |
|---|---|
| RD-01 | Domain references neither Application, Infrastructure, UI nor Contracts. |
| RD-02 | Application depends only on Domain plus abstractions. |
| RD-03 | Infrastructure implements Application's ports. |
| RD-04 | A local RPC DTO or a public API DTO never becomes a domain entity. |
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
| AT-11 | Every local RPC contract interface carries the required generated-proxy attributes |
| AT-12 | Every C# serialized DTO has a source-generated context; every consumed TS wire shape/validator is generated from C#-exported contracts. |
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

Assert portable managed projects have no esproj reference; win.slnx contains exactly the intended Web adapter; Web imports no private policy, database/entity or local-RPC contract; SDK imports no product UI; Account/Chat route graphs are selected explicitly; C# serializer/endpoint changes trigger TS generation and compatibility tests. Scope desktop DOM/JS bans to desktop build graphs, while prohibiting obsolete Blazor product dependencies in the current Web target.

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

## 10. Migration from the existing monorepo

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
