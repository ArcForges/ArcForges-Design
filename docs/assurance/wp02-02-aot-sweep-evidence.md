# WP02.02 AOT and trim declaration sweep

Scope: [WP02.02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.02), [BR-04/05](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-br-04), [PJ-02](../architecture/01-solution-and-project-layout.md#rule-pj-02), [BM-04](../architecture/14-build-packaging-and-release.md#rule-bm-04) and the [AOT contract](../requirements/12-quality-and-compatibility-contract.md#rule-ao-01). The [prior diagnostic-posture receipt](wp02-01-implementation-evidence.md) supplies the exact unchanged published baseline. This step closes the declaration and diagnostic sweep, not the later functional AOT proof or complete product acceptance.

## Research, decision and ordered execution

Research on 2026-09-21 evaluated all 43 restored managed projects in six owners, inspected the authored suppression surface and pinned SDK/ILLink/ILC imports, and ran expanded full-solution builds and real Native AOT publishes before changing documentation. Every existing AOT chain already declares its posture through effective imports; no source repair, dependency update, empty implementation PR or replacement publication is justified. No authored trim/AOT suppression or resulting diagnostic requires a waiver or blocking assignment.

The complete order selected before documentation edits was:

1. Record existing declarations, SDK defaults, expanded diagnostic logs and runtime receipts, preserving conforming source and its published identities.
2. Write this bounded evidence record and the parent completion link; validate all evidence identities, diagnostic results and formal Design references, then review the complete diff.
3. Create and review one documentation PR. Merge after applicable checks; when no CI is configured, merge after the documented review. Retain the branch and worktree.
4. Pull primary, verify the merged documentation and unchanged owner main identities, and only then enter the next numbered substep.

This is an acceptance-only change in Design. Research uses retained `wp02-01-diagnostic-posture` source worktrees whose Git trees equal their current clean merged mains. No source, package, generated output, provenance profile, release trigger or native installation changed. The new Design branch/worktree is `codex/wp02-02-aot-sweep` / `.worktree/wp02-02-aot-sweep`.

## Evaluated declarations and diagnostic coverage

The [machine-readable evidence](wp02-02-aot-sweep-evidence.json) records every project, effective properties, project references, main/source-tree identities, commands, complete diagnostic logs, compiler response arguments and runtime results.

| Owner | Managed projects | Projects with AOT analysis | Declaration source |
|---|---:|---:|---|
| DesktopPlatform | 24 | 22 | `src/Directory.Build.props` declares reusable library compatibility; the ContentSandbox host imports `eng/build/desktop-aot.props` |
| Contracts | 4 | 2 | PublicApi declares compatibility; HelloClient is an AOT-compatible verification client published AOT by its consumer command |
| ArcNotes | 4 | 2 | Core declares compatibility; the product host declares Native AOT |
| ArcScope | 4 | 2 | Core declares compatibility; the product host declares Native AOT |
| ArcSlate | 4 | 2 | Core declares compatibility; the product host declares Native AOT |
| Cloud | 3 | 1 | The service host declares Native AOT; effective imports enable all three analyzers |

All 31 selected projects evaluate AOT, trim and single-file analyzers enabled, with compiler warnings treated as errors. The remaining 12 are build/code-generation/test tools or JIT test hosts, not reusable runtime libraries on the deliverable chain. None needs a fictitious AOT-host declaration. Kotlin Android, browser assets and AI TypeScript retain their separate runtime policies.

The pinned SDK supplies ordinary compiler exclusions `1701;1702`. On trimmed projects its ILLink targets additionally hide `IL2121`, which reports redundant suppression attributes. The complete sweep explicitly used `_TrimmerShowRedundantSuppressions=true`, `TrimmerSingleWarn=false` and `SuppressTrimAnalysisWarnings=false`. This exposes redundant-suppression diagnostics and individual dependency warnings while retaining warnings-as-errors. Actual captured ILC arguments contain `--warnaserror`, no `IL2121`, no global `--singlewarn`, and no trim/AOT analysis disable switch. Compiler codes `1701;1702;8002` in the response files are recorded separately from IL diagnostics. No owner-authored suppression is introduced or excused by an SDK default.

The installed ILLink targets and ILC response files, not file-local absence or an assumed SDK default, establish these results. Microsoft documents the [AOT compatibility analyzer defaults](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/) and [detailed trimming warnings](https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/trimming-options). The pinned 10.0.11/10.0.12 targets additionally establish the redundant-suppression switch and warnings-as-errors fallback. Re-evaluate these defaults when the pinned SDK/runtime changes; this receipt is not an exemption from that upgrade review.

## Observed verification and triage

- Six complete Release solutions built successfully with expanded reporting and zero warnings/errors.
- DesktopPlatform ContentSandbox and all three desktop products published real Windows x64 Native AOT binaries with no expanded diagnostic. The helper executed; each product's actual native UI action reached the deployed Cloud revision `8942437a5e42c01ae7595b64a220efd60f33b4f0`, verifying greetings, Unicode boundaries and invalid/oversized input failures.
- An isolated Contracts consumer restored `ArcForges.Contracts.PublicApi` `1.0.0-ci.69.1` from public NuGet into its own empty package cache, replacing the producer ProjectReference with a PackageReference. Its native client published with expanded diagnostics and passed the existing authored success/error vectors against a real local gRPC host. No sibling producer source was compiled by that consumer.
- Cloud published the pinned Linux x64 Native AOT Docker closure using the same source and base images plus diagnostic-only command-line overrides in an untracked research recipe. The resulting image ran successfully; its actual native health and published binary gRPC-Web client passed greeting, Unicode, InvalidArgument and ResourceExhausted checks. This local image was not deployed or promoted as a new release.

**Resulting AOT/trim/single-file diagnostic list: empty. Authored suppression list: empty. Blocking assignments: empty.** There is no finding to suppress or leave unowned. SDK-default reporting was expanded rather than accepted as evidence of an absent finding. Existing declaration coverage plus these actual builds satisfies WP02.02 without a source change.

The unchanged [WP02.01 receipt](wp02-01-implementation-evidence.md) retains public package/archive comparisons, all five desktop RID runtime receipts, native package-only consumers and deployed Cloud evidence. Its JSON hash is bound in this receipt. Those normal-policy runs are distinct from this fresh expanded sweep: fresh desktop/helper expanded publishes ran on Windows x64, and Cloud ran Linux x64. Do not describe other RIDs as freshly rebuilt with the reporting overrides. Research desktop binaries report `sourceRevision=local` and `version=1.0.0`; their clean source-tree identity is recorded independently, and they are not public release candidates.

No vcpkg reinstall or package publication was performed. No external prerequisite is unavailable for this substep. The ContentSandbox scaffold is still not the WP11/13 containment/parser implementation. WP03/06 functional protocol/native proof, WP02.03 runtime/IDE boundaries and the remaining commercial gates remain separate obligations.
