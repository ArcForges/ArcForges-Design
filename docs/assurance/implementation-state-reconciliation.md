# Implementation-State Reconciliation

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: **D-011** (the existing monorepo is the implementation target), **D-012** (the monorepo is an implementation-state inventory and reconciliation target)
> Companions: [`../architecture/01-solution-and-project-layout.md`](../architecture/01-solution-and-project-layout.md), [`reference-coverage-and-provenance.md`](reference-coverage-and-provenance.md), [`../planning/README.md`](../planning/README.md)

**D-011** makes the existing monorepo at `C:\MyFile\ArcForges\ArcForges` the implementation target. **D-012** additionally makes it an *inventory and reconciliation target*: the design does not start on empty ground, and the gap between what exists and what this specification requires must be known before restructuring begins.

This document defines the reconciliation method, records the **observed first-pass inventory** taken during Phase 2, and states the gate that must be satisfied before restructuring starts.

> **Scope note.** The design repository is documentation-only. Nothing here modifies the implementation repository; the observations below were taken by reading it.

---

## 1. Reconciliation method

| # | Rule |
|---|---|
| RM-01 | **The inventory is produced before restructuring begins** (`MG-04` in the solution layout). Restructuring without it risks discarding work that already conforms. |
| RM-02 | **Reconciliation is per project, not per repository.** Each existing project receives one disposition. |
| RM-03 | **The dispositions are: Keep · Rename · Move · Split · Merge · Rewrite · Fence · Delete.** |
| RM-04 | **"Fence" means retained but unreferenceable**: existing code that has not yet been migrated is isolated so a conforming project cannot depend on it (`MG-03` there). |
| RM-05 | **Migration lands one vertical slice at a time** (`§1` there). The target layout is a logical structure, not a single restructuring event. |
| RM-06 | **A project is only Kept if it satisfies the project conventions** (`PJ-01`–`PJ-09` there) or has a scheduled change that will make it satisfy them. |
| RM-07 | **Existing behaviour is evidence, not authority.** Where existing code disagrees with this specification, the specification governs, and the divergence is recorded as a disposition rather than adopted. |
| RM-08 | **A disposition change is recorded with its reason**, so a decision is not silently revisited. |

### 1.1 Required fields per inventory item

| Field | Content |
|---|---|
| `ItemId` | Stable identifier |
| Existing path | Project or directory as it exists today |
| Target path | Where it lands in the target layout, or `NONE` |
| Disposition | One of `RM-03` |
| Licence boundary | Apache-2.0 or AGPL-3.0-only, per **D-004**/**D-021** |
| Conformance findings | Which project conventions it currently violates |
| Migration slice | Which work package moves it |
| Owner | Named owner |
| Risk | What breaks if this item is moved incorrectly |

---

## 2. Observed first-pass inventory

Taken 2026-09-04 by reading the implementation repository. It establishes scale and shape; the item-level inventory with dispositions is the work package deliverable (`§6`).

### 2.1 Repository shape

| Observation | Value |
|---|---|
| Solution files | `ArcForges.slnx`, `win.slnx` |
| Project count | **332** `.csproj` outside build artifacts |
| Top-level directories | `src`, `tests`, `contracts`, `native`, `eng`, `deploy`, `benchmarks`, `docs`, `artifacts` |
| SDK pin | `10.0.400`, `rollForward: disable`, `allowPrerelease: false` |
| Central package management | Enabled, **with transitive pinning** |
| Licence declaration | `AGPL-3.0-only` declared at the top of the central package file |
| Recent history | Active, with automated dependency updates and an SBOM step already present in CI |

### 2.2 Source areas that exist

| Area | Contents observed | Alignment with the target layout |
|---|---|---|
| `src/BuildingBlocks/` | Foundation, Application.Abstractions, Persistence (Postgres and SQLite), Observability, Security, NativeInterop, Testing, and several `Desktop.*` libraries | **Close.** The target expects mechanism-only building blocks; the `Desktop.*` set needs review against the shared-foundation boundary (`§7` of the overview) |
| `src/Contracts/` | Foundation, LocalRpc, PublicApi, Realtime, Sync, Agent, Serialization | **Close in shape.** Needs the explicit **Apache/AGPL split** the target requires (**D-004**, **D-021**) |
| `src/ArcChat/` | Domain, Application, Infrastructure, Presentation, Desktop, LocalRpc, LocalHub, LocalTools, McpClient, CloudClient, three test projects | **Close.** Hub and agent-runtime naming to reconcile with the target |
| `src/ArcNotes/` | Domain, Application, Infrastructure, Presentation, Desktop, Editor, Edgeless, Database, Slides, Search, ImportExport, LocalRpc, CloudClient, tests | **Close**, and broader than the target's summary line — the extra projects map onto ArcNotes V1 scope |
| `src/ArcScope/` | Domain, Application, Infrastructure, Presentation, Desktop, Acquisition, Recording, Decoders, Analysis, Visualization, Reporting, Native, LocalRpc, CloudClient, tests | **Close** |
| `src/ArcSlate/` | Domain, Application, Infrastructure, Presentation, Desktop, Timeline, Media, Playback, Processing, Rendering, Color, Audio, Subtitles, ImportExport, Native, LocalRpc, CloudClient, tests | **Close** |
| `src/Cloud/` | Host, AppHost, PublicApi, Realtime, Infrastructure, Migrations, BackgroundJobs, AgentRuntime, and modules for Identity, Catalog, Billing, Entitlement, Sync, Resource, Search, Notification, Configuration, Policy, Operations, AI, Agent, Chat, Notes, Scope, Slate | **Close.** Module set to be reconciled against the sixteen modules of the cloud architecture; role separation (API / Worker / TaskRunner) to be confirmed |
| `src/Mobile/` | ArcChat.Mobile plus Application, Domain, Presentation, Persistence, Realtime, CloudClient, Contracts, and test projects | **Close.** Requires the **Apache-2.0 boundary declaration and enforcement**, and the **F-023** closure before any artifact |
| `src/Web/` | `ArcForges.Web.App`, Application, Components, Infrastructure, `ArcForges.Web.SiteGenerator` | **Close.** Naming differs from the target's `StaticGen`; the two-output model matches |
| `src/SDK/` | `ArcForges.SDK.Foundation`, SourceGenerators, Testing, and `ArcForges.Cli` | **Close.** Requires the **Apache-2.0** licence boundary declaration |
| `src/Extensions/` | Contracts, Registry, Runtime, Packaging | **Close** to the extension platform architecture |
| `src/DesktopHelpers/` | `ArcForges.ContentSandbox` | To be reconciled — its placement relative to the shared foundation and the security boundary needs a disposition |
| `native/` | `arcmedia-ffmpeg-abi`, `arcscope-mdf-abi`, `arcslate-color-abi`, `arcslate-image-abi`, `arcslate-otio-abi`, `arcgraphics-metal-abi`, plus `shared` and `windows`, driven by CMake | **Broader than the target's two shims.** Each requires the `§2` permitted-surface test and a licence review (`PG-03` in the open-gates register) |
| `eng/` | `build` (with per-target property files for desktop AOT, desktop RIDs, Android AOT, cloud JIT and contracts), `native`, `packaging`, `release`, `signing`, `verification`, `versioning` | **Close**, and already encodes the **D-008** runtime split |
| `tests/` | 25 suites including ArchitectureTests, ContractCompatibilityTests, ContractSchemaTests, PublicApiContractTests, LocalRpcAotTests, RealtimeReconnectTests, NativeAbiTests, McpAotTests, MobileContractTests, PersistenceRecoveryTests, SyncConflictTests, ReleaseArtifactTests, RemoteToolBridgeTests, EndToEndTests, accessibility- and UI-oriented suites, and product pipeline suites | **Strong.** Most required families have a home already |

### 2.3 Conformance observations

| Observation | Finding | Consequence |
|---|---|---|
| No occurrence of `ArcCanvas`, `ArcMusic` or `ArcImage` in `src`, `contracts` or `tests` | **Conforms to D-002** | No product-name migration is needed in source |
| No occurrence of the superseded payment provider | **Conforms to D-005** | No commerce-provider migration is needed in source |
| `PublishAot` present in **5** project files | Consistent with four desktop hosts plus one additional AOT deliverable | To be confirmed item by item against the publish matrix (`§3` of the build architecture) |
| `IsAotCompatible` present in **0** project files | **Does not yet satisfy `PJ-02`**, which requires every reusable library consumed by an AOT deliverable to declare it | A scheduled, mechanical change across the library set, with the resulting diagnostics treated as findings |
| No committed `packages.lock.json` at the repository root | **Does not yet satisfy `PJ-05`** | Scheduled with the build-governance work package |
| No `fixtures/` directory | The golden-fixture root of the target layout does not exist | Scheduled with the compatibility-testing work package |
| `tests/RepositoryPolicyTests` not present as a distinct suite | `ArchitectureTests` exists; the repository-policy suite (`RP-01`–`RP-10`) is not separately identifiable | Scheduled with the repository-policy work package |
| Contracts are not split by licence boundary | **Does not yet satisfy `LB-01`–`LB-07`** | The single highest-priority structural reconciliation, because the mobile boundary depends on it |

> These are findings about conformance to this specification. They are not defects in the existing work, which predates this specification.

---

## 3. Priority order for reconciliation

Derived from what blocks the most downstream work.

| Priority | Item | Why first |
|---|---|---|
| 1 | **Contract licence-boundary split** | **D-004**/**D-021** and the **F-023** gate depend on it; every mobile and public-client decision is downstream |
| 2 | **Build governance**: `IsAotCompatible`, lock file, warnings-as-errors, analyzer policy | Every subsequent AOT proof depends on the diagnostics being real |
| 3 | **Repository-policy test suite** | Turns the rules of this specification into build failures rather than review burden |
| 4 | **Cloud module reconciliation** | Module boundaries determine schema ownership, which is expensive to change later |
| 5 | **Native surface reconciliation** | Each shim needs a permitted-surface and licence decision before it can ship |
| 6 | **Shared-foundation boundary review** (`BuildingBlocks`, `DesktopHelpers`) | Determines what may be shared, which affects every product |
| 7 | **Fixtures and golden corpora** | Required before compatibility claims can be made |
| 8 | **Per-product project reconciliation** | Largest volume, but least blocking once the above are settled |

---

## 4. Reconciliation rules that constrain outcomes

| # | Rule |
|---|---|
| RC-01 | **An existing project name that conflicts with the normative glossary is renamed** (**D-018**), not preserved for familiarity. |
| RC-02 | **An existing project that spans two licence boundaries is split**, never granted an exception (**D-004**). |
| RC-03 | **An existing project that is both domain and adapter is split** (`PJ-01`). |
| RC-04 | **An existing test suite that covers a required family is Kept and extended**, not replaced, unless it fails `RM-06`. |
| RC-05 | **An existing native shim outside the permitted surface (`§2` of the native architecture) is removed from the product path**, or its scope is narrowed with a recorded decision. |
| RC-06 | **Deleting existing work requires an explicit disposition with a reason.** Silent deletion is prohibited. |
| RC-07 | **No reconciliation step may leave the repository unbuildable at a commit boundary.** Fencing exists precisely so that partial migration remains green. |
| RC-08 | **A reconciliation change is separate from a behaviour change.** A commit either moves code or changes what it does, never both. |

---

## 5. Relationship to the reference audit

The existing monorepo is *both* the implementation target and a reference (**D-012**). Those roles must not be conflated.

| # | Rule |
|---|---|
| RF-01 | **Code already in the monorepo does not require a provenance record to keep**, because it is already ArcForges' own work under its declared licence. |
| RF-02 | **Code in the monorepo that originated elsewhere does require a provenance record** (**D-013**), and the inventory must identify it. |
| RF-03 | **A file with an unclear origin is treated as unknown-origin material** (**D-013**) until resolved, and cannot enter the Apache-2.0 boundary. |
| RF-04 | **The monorepo's own NOTICE and licence declarations are verified against the inventory**, not assumed correct. |

---

## 6. The gate

| Aspect | Position |
|---|---|
| Gate | **PG-02** in [`open-gates-register.md`](open-gates-register.md) |
| Requirement | The item-level inventory, with a disposition for every existing project and every native shim, exists and is approved |
| Owner | Architecture Owner |
| Trigger | Before the first restructuring change |
| Blocks | All restructuring work |
| Scheduled in | The repository reconciliation work package ([`../planning/work-packages/README.md`](../planning/work-packages/README.md)) |

> The observed inventory in `§2` is a first pass at repository scale, sufficient to plan the work and to set priority order. It is deliberately not presented as the item-level inventory the gate requires — producing that requires opening 332 project files and is assigned to a named work package.

---

## 7. Traceability

| Source | Consumed as |
|---|---|
| **D-011** | The existing monorepo as the implementation target |
| **D-012** | The monorepo as an implementation-state inventory and reconciliation target |
| **D-013** | Provenance obligations for material of external origin already present |
| **D-004**, **D-021** | The licence-boundary split as the highest-priority reconciliation |
| **D-018** | Renaming obligations where existing names conflict with the glossary |
| `§1`, `§2`, `§8` of the solution layout | The target layout, project conventions and policy tests that dispositions are measured against |
