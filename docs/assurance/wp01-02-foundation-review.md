# WP01.02 shared-foundation boundary review

Scope: [WP01.02](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.02), under [shared-foundation boundaries](../architecture/00-architecture-overview.md#6-shared-foundation-boundary) and [current project ownership](../architecture/27-platform-projects-and-application-assistants.md). This closes the current content and reference review, not implementation of the future capabilities.

## Baseline and decisions

DesktopPlatform source `b7744f3ffdeae161d8a3e34243aad3b8e8b47978` matches the clean primary and remote main. All 11 current BuildingBlocks projects, their source, README files, project/lock files and inherited build inputs were reviewed. The [WP01.00 inventory](wp01-00-inventory-policy.md) remains the current source mapping; [WP01.01](wp01-01-implementation-evidence.md) and [WP00](wp00-stage-acceptance.md) retain their independently completed gates. No implementation source, package version, lock or licence was changed.

| Project | Classification | Disposition | Reviewed rationale |
|---|---|---|---|
| `ArcForges.Application.Abstractions` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |
| `ArcForges.Desktop.Experience` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |
| `ArcForges.Desktop.Graphics` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |
| `ArcForges.Desktop.Preview` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |
| `ArcForges.Desktop.RichContent` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |
| `ArcForges.Desktop.Text` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |
| `ArcForges.Foundation` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |
| `ArcForges.NativeInterop` | Mechanism-only | Keep | C ABI version/build-info/error probes only; legacy ArcSlate library identifiers preserve binary compatibility. Native surface migration remains WP01.03. |
| `ArcForges.Observability` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |
| `ArcForges.Persistence.Sqlite` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |
| `ArcForges.Security` | Mechanism-only | Keep | Only an assembly-name constant; no business state, rules, adapters or product dependency. |

No current project is product-aware, so there is no product-content move or split to execute. The five Desktop.* name-only scaffolds do not implement a UI or business view model. Their older historical Move recommendation described a previous baseline; WP01.00's current Keep disposition is confirmed by this content review. Eventual design-system/shell content belongs to WP10 under architecture 27, without duplicating product behavior. Foundation/Application behavior remains WP04, SQLite WP07, Security WP11 and Observability WP12. Existing scaffolds are excluded from package admission and are not accepted capabilities. Historical Persistence.Postgres and Testing projects remain absent/retired; they are not recreated.

## Actual verification

A clean isolated worktree restored `DesktopPlatform.slnx` with `--locked-mode`, built Release with zero warnings/errors and passed all four existing ArchitectureTests. The unchanged source's [main publication CI](https://github.com/ArcForges/DesktopPlatform/actions/runs/35539950237) is green; its prior package/runtime evidence is not misrepresented as a new runtime run.

For every current BuildingBlocks project, actual `dotnet msbuild` Release evaluation collected `ProjectReference`, `Reference`, `PackageReference`, `Compile`, `TargetFramework` and `IsPackable`. All 11 have zero project/assembly references, no product package dependencies, only owned compiled source paths, and `IsPackable=false`. The only package dependencies are build/analyzer tooling. This verifies the effective inherited graph, beyond searching project XML. [Microsoft documents these evaluated-item options](https://learn.microsoft.com/en-us/visualstudio/msbuild/evaluate-items-and-properties), checked 2026-09-20. The [machine-readable receipt](wp01-02-foundation-review.json) records per-project source hashes, reference results and log hashes.

The content decision is a manual review bound to exact source hashes, not a general semantic analyzer. Existing ownership/build/reference tests continue to apply. Future source changes require review under the same architectural boundary; this historical receipt does not automatically approve new code. No new package was necessary because no implementation changed, and no browser/device/provider behavior is claimed. No external prerequisite blocks this step. Worktrees and `codex/wp01-02-foundation-review` branches are retained in Design and DesktopPlatform.
