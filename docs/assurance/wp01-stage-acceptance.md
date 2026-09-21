# WP01 repository reconciliation stage acceptance

Authority: [WP01.90](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.90), the parent WP01 completion gate and [staged producer integration](../planning/README.md#staged-artifact-integration). Result: the bounded reconciliation stage passes. The [machine-readable receipt](wp01-stage-acceptance.json) joins the exact sources, candidates, evidence hashes and retained limitations; it is not a commercial release manifest.

## Completed obligations

| Substep | Verified outcome |
|---|---|
| [WP01.00](wp01-00-implementation-evidence.md) | Nine independent owners, 75 current projects, 359 directory dispositions and seven native entries. All 166 historical project paths/blobs were checked again against the original Git tree; every row retains a target owner, disposition, producer and reason. |
| [WP01.01](wp01-01-implementation-evidence.md) | Current contract type/access assignments are complete and dependency-consistent; compiled checks reject public-to-internal references. Both source sets remain Apache-2.0. Full business schema generation belongs to WP03. |
| [WP01.02](wp01-02-foundation-review.md) | All eleven BuildingBlocks projects contain mechanisms or name-only scaffolds, with no product-domain references. Evaluated build references and architecture tests passed. WP01.03 subsequently moved the independent native oracle out of the production scaffold. |
| [WP01.03](wp01-03-native-reconciliation.md) | One production owner for admitted native bindings; test-only oracle, selected official OTIO, excluded MDF, no duplicate product copies. Current ABI probes and real packaged consumers passed without claiming functional parser or signed-helper completion. |
| [WP01.04](wp01-04-test-family-map.md) | All eighteen test families have current bounded suites or explicit gaps and future producers. Mapping covers 99 rows over 98 sources/entrypoints and all 28 historical test projects; ten families remain partial and eight remain gaps. |
| [WP01.05](wp01-05-bounded-reconciliation.md) | Current owned project/directory graphs agree with the inventory; retired Notes/monorepo roots are absent. Fresh licence/runtime audits pass. A new clean Notes worktree restores exact packages, builds and passes 89 tests plus formatting and provenance checks. |

No additional source migration, fence or package publication is necessary to assemble these unchanged deliverables. All nine exact source heads remain clean; their exact-head hosted CI was verified in WP01.05. Existing reviewed content drift is enumerated there instead of relabelling immutable snapshot pins as current heads.

## Candidate and runtime closure

| Owner | Candidate | Actual evidence and bounds |
|---|---|---|
| DesktopPlatform | `1.0.0-ci.17.1` | Ten public NuGet packages; verified Windows native build and independently restored JIT/AOT/C17 consumers, five cases and four negative loader fixtures. Metal remains source-only in this admission. |
| Contracts | `1.0.0-ci.65.1`; Maven `1.0.0-SNAPSHOT`, timestamp `20260921.014054-1` | Public NuGet/npm/Maven bytes and Windows/Linux isolated protocol consumers; subsequent actual Windows snapshot feed restore verifies C#/TS/Kotlin/Connect/AOT success/error calls. [Publication-channel receipt](contracts-publication-channels-evidence.md). |
| ArcNotes / ArcScope / ArcSlate | Each `0.1.0-ci.8.1` | Their own five native platform archives and UI/live-Hello checks, with exact source and observed historical Cloud revision retained in the upstream receipt. These runs are not a fresh current-provider test. |
| Cloud | `0.1.0-ci.18.1` | Existing actual Worker/Native AOT Container and binding/runtime evidence, not D1 production business-module acceptance. |
| AI | `0.1.0-ci.26.1` | Existing private Workflow and two real Workers AI model calls around the tool. No new paid model request is made for source reconciliation. |
| Web | `0.1.0-ci.22.1` | Existing public archive identity and real browser Hello proof; full Account/Chat/Operations business acceptance remains future work. |
| Mobile | `0.1.0-ci.14.1`, version code 1401 | Existing signed APK/AAB identities, emulator and public upgrade evidence; no physical-device or store admission claim. |

The seven unchanged owners retain their exact [WP00 candidate and runtime receipt](wp00-stage-acceptance.md). Producer and consumer identities are separate: applications retain their own compatible exact package locks, rather than silently adopting each new Platform or Contracts CI version. No sibling source is admitted to their package closure.

WP01.90 newly downloaded and hashed all ten Platform public NuGet archives and 23 Contracts files (one NuGet archive, two npm tarballs and twenty timestamped Maven files). All 33 match the independently verified public hashes retained by the producing substeps. This read-only check neither publishes nor overwrites a version. Maven snapshot identity is the timestamp plus exact hashes; it is a development channel with retention, not a permanent formal Central release.

## Stage boundary and remaining work

The six parent completion conditions are satisfied for this stage: explicit old-to-current dispositions, dependency-consistent contract assignment, product-free foundation, admitted current native ownership, complete test-family mapping, and retired blocking-path absence with a working retained Notes core. No unresolved ownership or substitute-native selection remains to be decided during this stage's implementation. Explicit Kotlin bootstrap compatibility and later Build.Policy/Cloud project producers remain as recorded by WP01.05.

WP02 supplies build governance; WP03 supplies complete production schemas; WP04/07–12 supply substantive shared mechanisms; WP05 completes architecture/invariant enforcement; WP13 supplies functional native ABI/RID/parser behavior; WP21.02 supplies the twenty-one Cloud module boundaries. Product/provider/recovery and commercial gates remain with their full producing work packages and WP50. Existing Hello/scaffold and package checks do not close these gates.

No external prerequisite blocks WP01 reconciliation. This documentation-only change is reviewed and checked with the Design policy preview, then merged and verified on pulled main. Branch `codex/wp01-90-stage-acceptance` and worktree `.worktree/wp01-90-stage-acceptance` are retained with all preceding implementation and evidence worktrees.
