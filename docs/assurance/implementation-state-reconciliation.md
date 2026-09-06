# Implementation-State Reconciliation

> Status: **Authoritative** — Phase 2 design-stage evidence · **Complete**
> Layer: Assurance
> Governing authority: **D-011** (the existing monorepo is the implementation target and is inspected in the reconciliation phase), **D-012** (it is an implementation-state inventory and reconciliation target)
> Companions: [`../architecture/01-solution-and-project-layout.md`](../architecture/01-solution-and-project-layout.md), [`reference-coverage/README.md`](reference-coverage/README.md), [`../planning/work-packages/README.md`](../planning/work-packages/README.md)

This is the **item-level reconciliation evidence** required before implementation planning is finalized. It replaces the earlier first-pass structural inventory, which read directory shape as if it were implementation state and drew several conclusions the evidence does not support. Those corrections are recorded in `§3`.

> **Scope note.** The design repository is documentation-only. Everything below was produced by **reading** the implementation repository. Nothing in it was modified, restructured, relabelled, relicensed, deleted, formatted or regenerated. No build was run and no test was executed.

---

## 1. Source identity and method

| Field | Value |
|---|---|
| Repository | `C:\MyFile\ArcForges\ArcForges` (**D-011** target) |
| Remote | `github.com/ArcForges/ArcForges` |
| Head commit | `ede43db` — *"Merge pull request #34 … dependabot/nuget/multi-5e6b40012e"* |
| Reviewed on | 2026-09-05 |
| Reviewer | Architecture Owner (design stage) |

### 1.1 Method

| Step | What was done |
|---|---|
| 1 | Enumerated every `.csproj` outside build output, **excluding the nested `.worktree/af02-01-contracts-localrpc` tree** so no project is counted twice |
| 2 | For each project: read the project file for target framework, AOT properties, package and project references; counted `.cs` files and lines under the project directory, excluding `bin` and `obj` |
| 3 | Read the effective build configuration — `Directory.Build.props`, `Directory.Packages.props`, `global.json`, `eng/build/*.props` — rather than inferring from per-project files |
| 4 | Read licence declarations at file level across all 273 `.cs` files, not only at the repository root |
| 5 | Read the contents of the substantive projects and of every native shim, rather than treating their directory names as evidence |
| 6 | Compared each finding against the earlier first-pass claim and recorded every correction |

### 1.2 The measurement that changes the picture

| Measure | Value |
|---|---|
| Projects (main tree) | **166** |
| Total C# lines across the whole repository | **8,638** |
| Projects with 12 or fewer C# lines | **111 of 166** |
| Projects with 60 or fewer C# lines | **151 of 166** |
| Projects with more than 250 C# lines | **4** |
| Test projects | 28, totalling **4,148** lines — of which three projects hold **3,396** |

**The repository is a near-complete structural skeleton with four substantive components.** Its directory shape closely anticipates the target layout; its behaviour does not yet exist. Both halves of that sentence matter: the shape is a genuine asset, and reading it as implementation would have produced a badly wrong plan.

---

## 2. Reconciliation method and dispositions

| # | Rule |
|---|---|
| RM-01 | **The inventory precedes restructuring.** This document is that inventory. |
| RM-02 | **Reconciliation is per project, per test suite and per native shim** — not per directory. |
| RM-03 | **Dispositions**: `Keep` · `Rename` · `Move` · `Split` · `Merge` · `Rewrite` · `Fence` · `Delete`. |
| RM-04 | **`Keep` means the item conforms to the accepted design or has a scheduled change that will make it conform** — never merely that it exists. |
| RM-05 | **Existing code is evidence of present state, not a competing design authority** (**D-011**). Where existing code and the accepted design disagree, the design governs. |
| RM-06 | **A scaffold is not an implementation.** A project with a namespace declaration and no behaviour is `Keep` on structure and carries its full implementation work in its owning package. |
| RM-07 | **Deleting existing work requires an explicit disposition with a reason.** |
| RM-08 | **A reconciliation change is separate from a behaviour change**, and no step leaves the repository unbuildable at a commit boundary. |
| RM-09 | **Completing this inventory is not executing it.** Physical migration and build-time enforcement remain implementation work in `WP-01` and `WP-02`. |

---

## 3. Corrections to the earlier first-pass inventory

The first-pass inventory made six claims the evidence does not support. Each is corrected here, with the check that establishes the correction.

| # | Earlier claim | Evidence | Corrected finding |
|---|---|---|---|
| C-01 | "**332** projects" | Enumeration excluding the nested worktree | **166 projects.** The earlier count double-counted `.worktree/af02-01-contracts-localrpc`, a working branch checkout inside the repository. Every count derived from 332 was inflated by roughly half |
| C-02 | Per-area alignment described as "**Close**", implying substance | 8,638 C# lines total; 151 of 166 projects at or under 60 lines | **Alignment is structural only.** The directory shape anticipates the target layout; the behaviour does not exist. "Close" was a statement about names, presented as if it were about implementation |
| C-03 | "`IsAotCompatible` present in **0** project files → does not satisfy `PJ-02`" | `eng/build/desktop-aot.props` sets `IsAotCompatible`, `PublishAot`, `PublishTrimmed`, `TrimMode=full`; `eng/build/contracts.props` sets `IsAotCompatible` and `EnableTrimAnalyzer` | **False finding.** The property is set **centrally** for the projects that need it. A per-`csproj` grep cannot see central imports. `PJ-02` is substantially satisfied for the AOT chain already |
| C-04 | "No committed `packages.lock.json` → does not satisfy `PJ-05`" | **165 lock files** present, one per project | **False finding.** Locked restore is already in place. Only the root-level absence was observed, and the wrong conclusion drawn from it |
| C-05 | "The repository-policy suite is **not separately identifiable**" | `tests/ArchitectureTests/RepositoryPolicyTests.cs` — **19 test methods**, alongside `ArchitectureRuleTests.cs` with **28** | **False finding.** The suite exists as a file within the ArchitectureTests project rather than as a separate project. That is a packaging difference, not an absence |
| C-06 | "Every project declares its SPDX identifier and its licence boundary" (stated as target, read as near-conformance) | 0 `.csproj` carry SPDX; **all 273 `.cs` files carry `SPDX-License-Identifier: AGPL-3.0-only`** | **Both halves wrong, in opposite directions.** SPDX *is* declared — at file level, universally. But the *boundary* is not declared anywhere, and the single blanket identifier is itself a defect (`§5.1`) |

**What this pattern shows.** Four of the six errors came from treating a `grep` count over project files as a conformance measurement. Presence of a token is weak evidence; absence of a token is weaker still. The corrected method reads effective configuration and file contents.

---

## 4. Item-level inventory

Every project in the main tree, with its measured content and state. **State** is a measurement, not a judgement:

| State | Definition |
|---|---|
| **Empty** | No `.cs` file |
| **Stub** | 1–12 C# lines — typically a namespace or a single placeholder type |
| **Skeleton** | 13–60 C# lines — a few types, no behaviour |
| **Partial** | 61–250 C# lines |
| **Substantive** | More than 250 C# lines |

#### `src/Contracts` — 7 projects, 1916 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcForges.Contracts.Foundation` | 30 | 1868 | Substantive | — |
| `ArcForges.Contracts.Agent` | 1 | 8 | Stub | — |
| `ArcForges.Contracts.LocalRpc` | 1 | 8 | Stub | — |
| `ArcForges.Contracts.PublicApi` | 1 | 8 | Stub | — |
| `ArcForges.Contracts.Realtime` | 1 | 8 | Stub | — |
| `ArcForges.Contracts.Serialization` | 1 | 8 | Stub | — |
| `ArcForges.Contracts.Sync` | 1 | 8 | Stub | — |

#### `src/BuildingBlocks` — 13 projects, 391 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcForges.NativeInterop` | 4 | 220 | Partial | — |
| `ArcForges.Testing` | 2 | 83 | Partial | — |
| `ArcForges.Application.Abstractions` | 1 | 8 | Stub | — |
| `ArcForges.Desktop.Experience` | 1 | 8 | Stub | — |
| `ArcForges.Desktop.Graphics` | 1 | 8 | Stub | — |
| `ArcForges.Desktop.Preview` | 1 | 8 | Stub | — |
| `ArcForges.Desktop.RichContent` | 1 | 8 | Stub | — |
| `ArcForges.Desktop.Text` | 1 | 8 | Stub | — |
| `ArcForges.Foundation` | 1 | 8 | Stub | — |
| `ArcForges.Observability` | 1 | 8 | Stub | — |
| `ArcForges.Persistence.Postgres` | 1 | 8 | Stub | — |
| `ArcForges.Persistence.Sqlite` | 1 | 8 | Stub | — |
| `ArcForges.Security` | 1 | 8 | Stub | — |

#### `src/ArcChat` — 13 projects, 388 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcChat.Desktop` | 5 | 210 | Partial | yes |
| `ArcChat.Tests.Ui` | 2 | 78 | Partial | — |
| `ArcChat.Tests.Integration` | 1 | 14 | Skeleton | — |
| `ArcChat.Tests.Unit` | 1 | 14 | Skeleton | — |
| `ArcChat.Application` | 1 | 8 | Stub | — |
| `ArcChat.CloudClient` | 1 | 8 | Stub | — |
| `ArcChat.Domain` | 1 | 8 | Stub | — |
| `ArcChat.Infrastructure` | 1 | 8 | Stub | — |
| `ArcChat.LocalHub` | 1 | 8 | Stub | — |
| `ArcChat.LocalRpc` | 1 | 8 | Stub | — |
| `ArcChat.LocalTools` | 1 | 8 | Stub | — |
| `ArcChat.McpClient` | 1 | 8 | Stub | — |
| `ArcChat.Presentation` | 1 | 8 | Stub | — |

#### `src/ArcNotes` — 16 projects, 412 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcNotes.Desktop` | 5 | 210 | Partial | yes |
| `ArcNotes.Tests.Ui` | 2 | 78 | Partial | — |
| `ArcNotes.Tests.Integration` | 1 | 14 | Skeleton | — |
| `ArcNotes.Tests.Unit` | 1 | 14 | Skeleton | — |
| `ArcNotes.Application` | 1 | 8 | Stub | — |
| `ArcNotes.CloudClient` | 1 | 8 | Stub | — |
| `ArcNotes.Database` | 1 | 8 | Stub | — |
| `ArcNotes.Domain` | 1 | 8 | Stub | — |
| `ArcNotes.Edgeless` | 1 | 8 | Stub | — |
| `ArcNotes.Editor` | 1 | 8 | Stub | — |
| `ArcNotes.ImportExport` | 1 | 8 | Stub | — |
| `ArcNotes.Infrastructure` | 1 | 8 | Stub | — |
| `ArcNotes.LocalRpc` | 1 | 8 | Stub | — |
| `ArcNotes.Presentation` | 1 | 8 | Stub | — |
| `ArcNotes.Search` | 1 | 8 | Stub | — |
| `ArcNotes.Slides` | 1 | 8 | Stub | — |

#### `src/ArcScope` — 17 projects, 435 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcScope.Desktop` | 5 | 210 | Partial | yes |
| `ArcScope.Tests.Ui` | 2 | 78 | Partial | — |
| `ArcScope.Native` | 3 | 23 | Skeleton | — |
| `ArcScope.Tests.Integration` | 1 | 14 | Skeleton | — |
| `ArcScope.Tests.Unit` | 1 | 14 | Skeleton | — |
| `ArcScope.Acquisition` | 1 | 8 | Stub | — |
| `ArcScope.Analysis` | 1 | 8 | Stub | — |
| `ArcScope.Application` | 1 | 8 | Stub | — |
| `ArcScope.CloudClient` | 1 | 8 | Stub | — |
| `ArcScope.Decoders` | 1 | 8 | Stub | — |
| `ArcScope.Domain` | 1 | 8 | Stub | — |
| `ArcScope.Infrastructure` | 1 | 8 | Stub | — |
| `ArcScope.LocalRpc` | 1 | 8 | Stub | — |
| `ArcScope.Presentation` | 1 | 8 | Stub | — |
| `ArcScope.Recording` | 1 | 8 | Stub | — |
| `ArcScope.Reporting` | 1 | 8 | Stub | — |
| `ArcScope.Visualization` | 1 | 8 | Stub | — |

#### `src/ArcSlate` — 20 projects, 460 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcSlate.Desktop` | 5 | 210 | Partial | yes |
| `ArcSlate.Tests.Ui` | 2 | 78 | Partial | — |
| `ArcSlate.Native` | 3 | 24 | Skeleton | — |
| `ArcSlate.Tests.Integration` | 1 | 14 | Skeleton | — |
| `ArcSlate.Tests.Unit` | 1 | 14 | Skeleton | — |
| `ArcSlate.Application` | 1 | 8 | Stub | — |
| `ArcSlate.Audio` | 1 | 8 | Stub | — |
| `ArcSlate.CloudClient` | 1 | 8 | Stub | — |
| `ArcSlate.Color` | 1 | 8 | Stub | — |
| `ArcSlate.Domain` | 1 | 8 | Stub | — |
| `ArcSlate.ImportExport` | 1 | 8 | Stub | — |
| `ArcSlate.Infrastructure` | 1 | 8 | Stub | — |
| `ArcSlate.LocalRpc` | 1 | 8 | Stub | — |
| `ArcSlate.Media` | 1 | 8 | Stub | — |
| `ArcSlate.Playback` | 1 | 8 | Stub | — |
| `ArcSlate.Presentation` | 1 | 8 | Stub | — |
| `ArcSlate.Processing` | 1 | 8 | Stub | — |
| `ArcSlate.Rendering` | 1 | 8 | Stub | — |
| `ArcSlate.Subtitles` | 1 | 8 | Stub | — |
| `ArcSlate.Timeline` | 1 | 8 | Stub | — |

#### `src/Cloud` — 27 projects, 233 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcForges.Cloud.Host` | 3 | 27 | Skeleton | yes |
| `ArcForges.Cloud.Tests` | 1 | 14 | Skeleton | — |
| `ArcForges.Cloud.AgentRuntime` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.BackgroundJobs` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Infrastructure` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.AI` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Agent` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Billing` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Catalog` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Chat` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Configuration` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Entitlement` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Identity` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Notes` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Notification` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Operations` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Policy` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Resource` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Scope` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Search` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Slate` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Modules.Sync` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.PublicApi` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.Realtime` | 1 | 8 | Stub | — |
| `ArcForges.ServiceDefaults` | 1 | 8 | Stub | — |
| `ArcForges.Cloud.AppHost` | 1 | 5 | Stub | — |
| `ArcForges.Cloud.Migrations` | 1 | 3 | Stub | — |

#### `src/Mobile` — 11 projects, 166 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcChat.Mobile` | 5 | 68 | Partial | — |
| `ArcChat.Mobile.ContractTests` | 1 | 14 | Skeleton | — |
| `ArcChat.Mobile.Tests` | 1 | 14 | Skeleton | — |
| `ArcChat.Mobile.UiTests` | 1 | 14 | Skeleton | — |
| `ArcChat.Mobile.Application` | 1 | 8 | Stub | — |
| `ArcChat.Mobile.CloudClient` | 1 | 8 | Stub | — |
| `ArcChat.Mobile.Contracts` | 1 | 8 | Stub | — |
| `ArcChat.Mobile.Domain` | 1 | 8 | Stub | — |
| `ArcChat.Mobile.Persistence` | 1 | 8 | Stub | — |
| `ArcChat.Mobile.Presentation` | 1 | 8 | Stub | — |
| `ArcChat.Mobile.Realtime` | 1 | 8 | Stub | — |

#### `src/Web` — 5 projects, 27 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcForges.Web.App` | 1 | 8 | Stub | — |
| `ArcForges.Web.Application` | 1 | 8 | Stub | — |
| `ArcForges.Web.Infrastructure` | 1 | 8 | Stub | — |
| `ArcForges.Web.SiteGenerator` | 1 | 3 | Stub | — |
| `ArcForges.Web.Components` | 0 | 0 | Empty | — |

#### `src/SDK` — 4 projects, 27 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcForges.SDK.Foundation` | 1 | 8 | Stub | — |
| `ArcForges.SDK.SourceGenerators` | 1 | 8 | Stub | — |
| `ArcForges.SDK.Testing` | 1 | 8 | Stub | — |
| `ArcForges.Cli` | 1 | 3 | Stub | — |

#### `src/Extensions` — 4 projects, 32 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcForges.Extensions.Contracts` | 1 | 8 | Stub | — |
| `ArcForges.Extensions.Packaging` | 1 | 8 | Stub | — |
| `ArcForges.Extensions.Registry` | 1 | 8 | Stub | — |
| `ArcForges.Extensions.Runtime` | 1 | 8 | Stub | — |

#### `src/DesktopHelpers` — 1 projects, 3 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcForges.ContentSandbox` | 1 | 3 | Stub | — |

#### `tests` — 28 projects, 4148 C# lines

| Project | .cs files | C# lines | State | AOT publish |
|---|---|---|---|---|
| `ArcForges.Tests.ArchitectureTests` | 18 | 2075 | Substantive | — |
| `ArcForges.Tests.ContractCompatibilityTests` | 7 | 987 | Substantive | — |
| `ArcForges.Tests.ContractSchemaTests` | 1 | 334 | Substantive | — |
| `ArcForges.Tests.CloudIntegrationTests` | 2 | 53 | Skeleton | — |
| `ArcForges.Web.BrowserTests` | 1 | 45 | Skeleton | — |
| `ArcForges.Tests.NativeAbiTests` | 2 | 39 | Skeleton | — |
| `ArcForges.Web.ComponentTests` | 2 | 36 | Skeleton | — |
| `ArcForges.Tests.AndroidUiTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.ArcScopePipelineTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.ArcSlateMediaTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.DesktopExperienceGallery` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.DesktopExperienceTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.DesktopUiTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.EndToEndTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.GraphicsInteropTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.LocalRpcAotTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.McpAotTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.MobileContractTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.NativeContentTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.PersistenceRecoveryTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.PublicApiContractTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.RealtimeReconnectTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.ReleaseArtifactTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.RemoteToolBridgeTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.SyncConflictTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Tests.VirtualizationTests` | 2 | 29 | Skeleton | — |
| `ArcForges.Web.ContractTests` | 1 | 14 | Skeleton | — |
| `ArcForges.Web.UnitTests` | 1 | 14 | Skeleton | — |

---

## 5. Findings and dispositions

### 5.1 Licence boundary — three live defects, not merely absent work

All 273 `.cs` files declare `SPDX-License-Identifier: AGPL-3.0-only`, and `NOTICE.md` states the repository is AGPL-3.0-only. Three subtrees are **required by Phase 1 to be Apache-2.0**:

| Subtree | Files declaring AGPL-3.0-only | Required position | Authority |
|---|---|---|---|
| `src/Mobile/**` | **15** | Apache-2.0 | **D-004** — ArcChat Mobile and its mobile-only libraries |
| `src/SDK/**` | **4** | Apache-2.0 | **D-021** — the public SDK |
| `src/Contracts/**` | **36** | Apache-2.0 for the public interoperability set | **D-004**, **D-021** — public protocol specs, wire schemas, DTOs, public clients, contract-level validators |

| # | Finding |
|---|---|
| LB-01 | **This is a declared-wrong condition, not an undone task.** The files assert a licence that Phase 1 forbids for their boundary. |
| LB-02 | **It is also cheap to fix now and expensive later.** The material is 55 files totalling a small fraction of the repository; after external contribution it would require contributor agreement. |
| LB-03 | **`src/Contracts` has no `Public`/`Internal` split** — verified: no such directories exist. The split decision therefore governs both the physical layout and the licence header of each type. |
| LB-04 | **Disposition: `Split` for `src/Contracts`, `Relicense-in-place` for `src/Mobile` and `src/SDK`** — the latter recorded as a `Rewrite` of the header only, executed by the owning packages, never by a bulk automated pass without per-file review. |
| LB-05 | **`NOTICE.md` must gain the boundary statement** so the repository's own declaration matches **D-004**. |

**This is the highest-priority reconciliation item**, and it is why `WP-01` precedes every product package.

### 5.2 Native shims — six ABI skeletons, not six implementations

| Shim | Source files | Lines | Exported functions found |
|---|---|---|---|
| `arcmedia-ffmpeg-abi` | 3 | 120 | `arc_media_get_abi_version`, `arc_media_get_build_info`, `arc_media_get_last_error` |
| `arcscope-mdf-abi` | 3 | 92 | version / build-info / last-error triple |
| `arcslate-color-abi` | 3 | 93 | version / build-info / last-error triple |
| `arcslate-image-abi` | 3 | 90 | version / build-info / last-error triple |
| `arcslate-otio-abi` | 3 | 91 | version / build-info / last-error triple |
| `arcgraphics-metal-abi` | 2 | 28 | version / build-info / last-error triple |
| `shared` | 4 | — | `arc/arc_native_abi.h` preamble, implementation, internal header, and a fuzzer |

**Every shim exposes only the three-function ABI preamble.** None contains decode, colour, image, interchange, MDF4 or Metal functionality. Total across all six plus shared: roughly 514 lines.

| # | Finding | Disposition |
|---|---|---|
| NS-01 | **The earlier framing — "a broader native surface than the architecture illustrates" — was wrong.** These are six *named placeholders* sharing one ABI convention, not six implemented surfaces | Corrected here |
| NS-02 | The shared preamble already implements version negotiation, build info and last-error — exactly what `AB-02`, `AB-08` and `AB-12` require | `Keep` — the convention conforms |
| NS-03 | Each shim carries `exports/{linux.map,macos.exports,windows.def}`, an `include/`, `src/`, `generated/`, `tests/` and `fuzz/` layout | `Keep` — the layout anticipates `NT-01`–`NT-05` |
| NS-04 | `arcmedia-ffmpeg-abi` → ArcSlate decode/encode. Permitted under `§2` of the native architecture | `Keep`; substantive work in `WP-37.00` |
| NS-05 | `arcslate-color-abi` → ArcSlate colour management. Permitted | `Keep`; work in `WP-38.00` |
| NS-06 | `arcslate-image-abi` → ArcSlate still-image I/O. Permitted | `Keep`; work in `WP-37.01` |
| NS-07 | `arcslate-otio-abi` → ArcSlate timeline interchange. **Permitted-surface question**: interchange parsing is a *format* concern, and the native architecture permits native code only where no reasonable managed substitute exists. A managed interchange reader is plausible | **`Fence` pending a substitute analysis in `WP-39.05`.** Not deleted — the exports and layout are reusable if the analysis favours native |
| NS-08 | `arcscope-mdf-abi` → ArcScope measurement-format I/O. Same question as `NS-07`, same treatment | **`Fence` pending a substitute analysis in `WP-35.04`** |
| NS-09 | `arcgraphics-metal-abi` → GPU surface access on one platform. Permitted under `§2` (GPU device and surface access) | `Keep`; work in `WP-37.02` |
| NS-10 | Every shim's `.h` declares `SPDX-License-Identifier: AGPL-3.0-only`. Native shims sit inside the AGPL boundary and are not consumed by mobile or the public SDK | **Conforms** — no change |
| NS-11 | **No third-party native dependency is vendored into any shim.** The FFmpeg, OpenColorIO and image dependencies named in `NOTICE.md` are external | Licence review of those externals remains `PG-03`, per product |

### 5.3 Build governance — better than the first pass claimed

| Item | Evidence | Finding | Disposition |
|---|---|---|---|
| SDK pin | `global.json`: `10.0.400`, `rollForward: disable`, `allowPrerelease: false` | Conforms to `BM-01` | `Keep` |
| Central package management | `Directory.Packages.props`: `ManagePackageVersionsCentrally`, `CentralPackageTransitivePinningEnabled` | Conforms to `PJ-04`, and transitive pinning exceeds the stated requirement | `Keep` |
| Lock files | 165 `packages.lock.json` | Conforms to `PJ-05` | `Keep`; `WP-02.00` verifies locked-mode restore rather than creating them |
| Warnings as errors | `Directory.Build.props`: `TreatWarningsAsErrors=true` | Conforms to `PJ-08` repository-wide | `Keep` |
| Language and nullability | `LangVersion=14`, `Nullable=enable` | Conforms to `PJ-07` | `Keep` |
| Desktop AOT posture | `eng/build/desktop-aot.props`: `PublishAot`, `PublishTrimmed`, `TrimMode=full`, `IsAotCompatible` | Conforms to **D-008** desktop row | `Keep` |
| Contract AOT posture | `eng/build/contracts.props`: `IsAotCompatible`, `EnableTrimAnalyzer`, `TreatWarningsAsErrors` | Conforms | `Keep` |
| Cloud JIT posture | `eng/build/cloud-jit.props` present as a distinct file | Structurally conforms to **D-008**; effective properties to be asserted in `WP-02.03` | `Keep` |
| Android AOT posture | `eng/build/android-aot.props` present | Structurally conforms; explicit runtime selection to be asserted in `WP-30.02` | `Keep` |
| Web WebAssembly posture | **No `web-wasm.props` found** | **Gap** — the fourth **D-008** row has no build-property file | `WP-02.03` creates it |
| Test runner | `global.json` selects a modern test platform | Conforms | `Keep` |

**Revised conclusion.** Build governance is close to conformant. `WP-02`'s remaining work is narrower than planned: the Web posture file, the `IsAotCompatible` sweep for libraries **outside** the two central imports, effective-property assertion, and the version-axis plumbing.

### 5.4 Existing tests — three real suites, twenty-five scaffolds

| Suite | Lines | Assessment |
|---|---|---|
| `ArchitectureTests` (incl. `RepositoryPolicyTests.cs`) | **2,075** | **Substantive.** 28 + 19 test methods; a real `ProjectGraph` loader; a `FixtureCompiler` for negative fixtures; the file header states *"the thirteen rules"* |
| `ContractCompatibilityTests` | **987** | **Substantive** |
| `ContractSchemaTests` | **334** | **Substantive** |
| `CloudIntegrationTests` | 53 | Skeleton |
| The remaining 24 suites | ≈ 700 combined | Stubs and skeletons — directory presence only |

| # | Finding | Disposition |
|---|---|---|
| TS-01 | The architecture-test approach is real and already uses negative fixtures — the mechanism `WP-05` specifies | `Keep` and extend. **`WP-05` is materially smaller than planned**: the harness exists |
| TS-02 | The file header names **thirteen** rules; the accepted design specifies **fourteen** architecture rules and **ten** repository-policy rules | `Keep`; `WP-05.00`–`WP-05.04` reconcile rule-by-rule rather than starting from nothing |
| TS-03 | **Twenty-five test-suite directories exist with no meaningful content.** Directory presence was previously read as coverage | **Corrected.** Each maps to a required family in `WP-01.04`, and its implementation stays with the owning package |
| TS-04 | **No test result, pass rate or execution record was observed**, and none is claimed | Test execution is implementation evidence, not design evidence |

### 5.5 Cloud module set

| Item | Evidence | Finding | Disposition |
|---|---|---|---|
| Modules present | 17: AI, Agent, Billing, Catalog, Chat, Configuration, Entitlement, Identity, Notes, Notification, Operations, Policy, Resource, Scope, Search, Slate, Sync | Close to the accepted 16-module set; the difference is a partitioning question, not a missing capability | `Keep`; reconciled item-by-item in `WP-21.02` |
| Runtime roles | `ArcForges.Cloud.Host`, `.AppHost`, `.BackgroundJobs`, `.ServiceDefaults` — **no `Worker`, no `TaskRunner`** | The accepted design's three deployable roles do not exist. `AppHost` and `ServiceDefaults` indicate an orchestration-framework pattern rather than role separation | **`Split` required** — recorded for `WP-21.01` |
| Content | 27 projects, **233 C# lines total** | Scaffolding | `Keep` on structure; all behaviour is `WP-21`+ |

### 5.6 Shared boundary and remaining areas

| Item | Evidence | Finding | Disposition |
|---|---|---|---|
| `src/BuildingBlocks` | 13 projects, 391 lines. Includes `ArcForges.Desktop.{Experience,Graphics,Preview,RichContent,Text}` | Those five are UI-facing and belong to the design-system and shell boundary, not to mechanism-only building blocks | **`Move`** to the design-system tree — `WP-01.02` |
| `src/DesktopHelpers/ArcForges.ContentSandbox` | 1 project, **3 lines** | A stub whose name implies a security boundary. Sandboxed preview is a real requirement (`CS-06`) | **`Move`** into the security or shell boundary with its owner named — `WP-01.02` |
| `src/Contracts` | 7 projects, 1,916 lines, of which `Contracts.Foundation` is **1,868** | The only substantive product-side implementation in the repository | `Keep`, then `Split` by licence boundary (`§5.1`) |
| `src/Extensions` | 4 projects, 32 lines | Names match the accepted extension architecture | `Keep`; behaviour in `WP-41` |
| `src/Web` | 5 projects, 27 lines; `ArcForges.Web.Components` is **empty**; generator is named `SiteGenerator` not `StaticGen` | Structure conforms; naming differs | `Keep` + `Rename` — `WP-01.05` |
| `src/Mobile` | 11 projects, 166 lines | Structure conforms; **licence declaration does not** (`§5.1`) | `Keep` + relicense |
| `fixtures/` | **Absent** | The golden-fixture root does not exist | `WP-01.05` creates it |

---

## 6. Priority order

Derived from what blocks the most downstream work, and revised by the corrected evidence.

| Priority | Item | Why | Changed by this evidence? |
|---|---|---|---|
| 1 | **Licence boundary correction** (`§5.1`) | 55 files actively declare a licence Phase 1 forbids for their boundary; **F-023** depends on it | **Raised** — it is a defect, not pending work |
| 2 | **Contract `Public`/`Internal` split** | Governs both layout and licence header; `Contracts.Foundation` is the only substantive code to move | Unchanged |
| 3 | **Cloud runtime-role separation** (`§5.5`) | Three roles do not exist; retrofitting after modules gain behaviour is expensive | **New** — not previously identified |
| 4 | **Shared-boundary moves** (`§5.6`) | Five UI-facing projects sit in mechanism-only building blocks | Unchanged |
| 5 | **Native shim substitute analyses** (`NS-07`, `NS-08`) | Two shims may not belong in the permitted native surface | **Narrowed** — from six shims to two questions |
| 6 | **Build governance completion** (`§5.3`) | Only the Web posture file, the library `IsAotCompatible` sweep and version-axis plumbing remain | **Lowered** — most of it already conforms |
| 7 | **Architecture-rule reconciliation** (`§5.4`) | Thirteen existing rules versus the accepted twenty-four | **Lowered** — the harness exists |
| 8 | **Fixtures root and naming** | Cheap, and unblocks compatibility claims | Unchanged |

---

## 7. Completeness check

| Check | Result |
|---|---|
| Every `.csproj` in the main tree appears in `§4` | **Pass** — 166 of 166 |
| Every area has a disposition in `§5` | **Pass** — 13 areas |
| Every native shim has a role, consuming product, permitted-surface assessment and disposition | **Pass** — 6 of 6, plus `shared` |
| Substitute analysis recorded where the permitted-surface assessment is open | **Pass** — `NS-07`, `NS-08`, both scheduled |
| Every earlier conformance claim re-checked against evidence | **Pass** — 6 corrections in `§3` |
| Effective build configuration read rather than inferred | **Pass** — `§5.3` |
| Licence position read at file level | **Pass** — all 273 `.cs` files |
| Test suites assessed by content, not directory presence | **Pass** — `§5.4` |
| Nothing in the implementation repository modified | **Pass** — read-only; no build or test executed |

**Unresolved determinations: none.** Two open *questions* (`NS-07`, `NS-08`) are scheduled substitute analyses with named owners, not unresolved determinations — the disposition (`Fence`) is decided; only the eventual destination is open.

---

## 8. What this inventory does not do

| # | Statement |
|---|---|
| ND-01 | **It does not execute the dispositions.** Physical migration is `WP-01`; build-time enforcement is `WP-02` and `WP-05`. |
| ND-02 | **It does not claim any behaviour works.** No build was run, no test executed, no artifact produced. |
| ND-03 | **It does not treat existing code as design authority** (**D-011**). |
| ND-04 | **It does not measure quality.** Line counts measure presence, not correctness. |
| ND-05 | **It is bound to commit `ede43db`.** `WP-01` re-checks for drift before executing. |
