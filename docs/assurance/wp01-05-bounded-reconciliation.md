# WP01.05 bounded repository reconciliation

Authority: [WP01.05](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.05), [current inventory profile](wp01-00-inventory-policy.md), [repository composition](../architecture/27-platform-projects-and-application-assistants.md) and [staged integration](../planning/producer-artifacts-and-integration.md). The [machine-readable receipt](wp01-05-bounded-reconciliation.json) binds this observation to the exact nine clean source commits and their successful main CI runs.

## Current disposition and decisions

All 75 current build projects retain their registered owner and Keep disposition: DesktopPlatform 35, Contracts 15, ArcNotes/ArcScope/ArcSlate four each, Cloud five, AI one, Web four and Mobile three. Every project's current Git blob is recorded. All 359 planned/current directory presence observations still match the inventory. No blocking source move, duplicate owner or conflicting retained implementation was found. This step verifies already completed physical separation; it does not recreate the historical 166-project monorepo or make empty source commits.

Three project files changed since the original snapshot: the NativeAbiTests project under reviewed DesktopPlatform PR 54, and two Gradle build files under the reviewed Contracts snapshot publication transition (PRs 26 and 27). Their original and current blobs are enumerated. The original immutable inventory remains unchanged. The fresh licence/runtime audits and explicit project-set/directory comparison establish current source state; this receipt does not claim that passing the old pinned-snapshot checker alone establishes current family state.

| Inventory disposition | Current result and remaining owner |
|---|---|
| Old DesktopPlatform product, ArcChat, Cloud, Contracts, Extensions, SDK, Web and Mobile roots | Absent. Independent owners already compose their actual hosts and consume package references. No monorepo host/Harness is restored. |
| ArcNotes.Edgeless and ArcNotes.Slides | Absent from tracked paths and live source/project/solution/lock/workflow inputs. Matches in the scan are historical policy data or negative assertions only. Retained Notes core builds and tests successfully. |
| MDF ABI and retired shared Persistence.Postgres/Testing roots | Absent. Existing native admissions and test-only oracle relocation remain those verified in WP01.03. |
| Contracts `src/public/csharp` | Absent legacy spelling; current C# owner is `src/public/dotnet`. Architecture 27 now uses the actual approved name. No package identity changes. |
| Contracts native-grpc-only Kotlin client | Still present under explicit bootstrap compatibility. Retirement belongs to the first business release in WP03; deleting it here would break the supported bootstrap closure. |
| Build.Policy target `eng/ArcForges.Build.Policy` | Still a planned WP02 move. Its current owned source remains valid; absence of the future target is not missing WP01 implementation. |
| Cloud 21 module owners | Ownership is recorded now; substantive module projects and schema-boundary implementation belong to WP21.02. The contradictory WP01 instruction to create them immediately is corrected without reducing the 21-module requirement. |
| Historical Web generator and missing fixture-root actions | Current Web uses four TypeScript outputs. Neither old generator remains to rename. Fixtures are created with substantive content at their named producer, never as empty placeholders. |

## Validation and package closure

Fresh read-only first-party licence/reference audits pass for all nine owners and 75 projects. Runtime/ownership and canonical naming audits pass for all nine. The source audit rejects outside-owner project/source references and submodules; no sibling source is admitted as a build dependency. The retired-name scan records its exact text-input scope and every historical/assertion match.

Every source commit still equals its remote main and has a successful exact-head CI run. The receipt records each job conclusion, including platform-native builds, isolated package consumers, publication and deployed checks where that owner's workflow runs them. These are existing hosted runs, not newly executed tests. Workflow execution at a historical date is not a fresh live-provider availability assertion.

A new clean ArcNotes worktree uses the already installed .NET SDK 10.0.401. Locked restore, Release build, repository/provenance/licence checks, formatting and all 89 deterministic tests pass. Its exact public Contracts 1.0.0-ci.36.1 and Build.Policy 1.0.0-ci.7.1 dependencies remain unchanged. Logs are hashed in the receipt. No vcpkg installation or native dependency version change occurred.

Existing verified candidate and package-notice evidence remains bound to the [WP00 stage receipt](wp00-stage-acceptance.md), [WP01.01 contract receipt](wp01-01-implementation-evidence.md), [Contracts snapshot verification](contracts-publication-channels-evidence.md) and [WP01.03 native receipt](wp01-03-native-reconciliation.md). The latter verifies every public payload for ten DesktopPlatform 1.0.0-ci.17.1 packages and real independent JIT/AOT/C17 consumers. Consumers retain their own compatible exact locks; no latest-version upgrade or new package publication is needed for this unchanged source graph.

## Completion boundary

WP01.05's current owner map, blocking retired-path absence, licence/reference boundary, clean builds and existing package closure are verified. No new source move needs a new consumer path. Full product workflows, future module implementations, physical-device/store/signing and commercial acceptance remain with their named producing steps. No external prerequisite blocked this bounded reconciliation.

The Design branch/worktree `codex/wp01-05-bounded-reconciliation` / `.worktree/wp01-05-bounded-reconciliation` and the unchanged ArcNotes validation branch/worktree `codex/wp01-05-core-validation` / `.worktree/wp01-05-core-validation` are retained. Complete diff review, Design policy preview and post-merge verification govern this documentation-only PR.
