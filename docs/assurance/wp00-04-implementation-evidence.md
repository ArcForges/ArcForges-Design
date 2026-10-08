# WP00.04 implementation evidence

> **SUPERSEDED IN PART (2026-10-08, [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021))**: the React/TypeScript, Node/npm and Kotlin/Maven/Gradle toolchain statements and the statements that rejected Blazor WebAssembly or .NET MAUI. The recorded result is retained as dated history and is not rewritten.

> Status: Completed: source, CI, publication and post-merge acceptance passed.
> Owning substep: [WP-00.04](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.04).
> Verified on: 2026-09-20 UTC.

## Accepted changes and prerequisites

[Design PR 27](https://github.com/ArcForges/ArcForges-Design/pull/27), merged as
`f5ef5d56dba6e7ecbe49a4ff47163bc548b94c8c`, defines the
[registration profile](reference-baseline-registration.md). It repairs the impossible
Git-commit requirement for a packaged tree and explicitly assigns the registry,
source verification, drift assessment and narrow packaged-observation boundary.
The three completed matrices retain their dispositions and source commits.

The earlier naming, glossary, licence and provenance stages remain prerequisites.
All seven primary implementation revisions matched the
[previous execution receipt](wp00-03-implementation-evidence.md), and their seven linked
main CI/publication runs were independently queried and confirmed successful.
Fresh verification retained the exact glossary/invariant pin, passed its 15 test
groups and immutable export check, and passed the current Design corpus preview.
The 35 effective DesktopPlatform project declarations and 11 licence test groups
passed; the 41 source/native provenance test groups, actual inventories and native
closure registration passed. No future producer package is required at this stage.

| Owner | Reviewed PR and merge | Latest-head PR CI |
|---|---|---|
| Contracts | [23](https://github.com/ArcForges/Contracts/pull/23), `7cfc2005b4d91eea28ffe073927b945a3a0d766a` | [package/consumer CI](https://github.com/ArcForges/Contracts/actions/runs/35532886579) and [security](https://github.com/ArcForges/Contracts/actions/runs/35532886555) passed |
| DesktopPlatform | [51](https://github.com/ArcForges/DesktopPlatform/pull/51), `76b40214fe018fc663dd393f812f1ecf89249cdd` | [all 16 checks](https://github.com/ArcForges/DesktopPlatform/actions/runs/35533138970) passed |

Contracts adds one exact provenance-file naming registration and updates the narrow
expected-path test. DesktopPlatform adds `eng/policy/reference-baselines.json`,
`eng/provenance/reference-inputs.json`, the portable verifier, 12 test groups,
implementation notes and Windows/Linux CI. Its existing provenance inventory admits
these authored identity facts. No reference source or matrix prose is copied; no
runtime package API, product identity or glossary declaration changes.

## Registration and real drift acceptance

The registration binds Design commit `f5ef5d56dba6e7ecbe49a4ff47163bc548b94c8c` and
metadata digest `4d06afa72af2deeff860288b96644a63b3b1ce814ab2bf8cb7992cd3b005edd5`.
Both hosted CI platforms independently fetched the registered immutable objects and
verified the same metadata, three document digests and the 69 matrix rows.

| Matrix | Rows | Source identity |
|---|---:|---|
| Assistant | 30 | AionUi `29c9271a59484e4696778cb80164f705245a6186` |
| Scope | 31 | Serial-Studio `639daafb2fe7d324c3b2d5583d2514c8c470676f` |
| Distribution | 8 | Non-Git observation dated 2026-09-20; installer version 2.1.35, two directory listings and two bundled text-notice hashes |

The actual local packaged tree matched after merge. Only immediate directory-entry
names/kinds and the two registered text notices were read; no binary was read,
executed, unpacked or reverse engineered. Hosted CI reports this observation as
registered but not locally re-observed. The registration date cannot prove the
packaged bytes present at the historical 2026-09-05 matrix review.

Independent disposable Git fixtures
proved added, modified and removed paths are detected. Both historical commits
resolved against their registered origins. AionUi
had a pre-existing local modification; this was reported separately, remains
unreviewed and is excluded from the fixed inputs. No reference checkout was changed.
Later source/scope maintenance and rights assessment keep their named consumer owners.

The 12 test groups additionally reject missing/duplicate/misassigned matrices,
invalid source/digest/path identities, changed matrix rows, missing packaged versions,
changed/missing notices, binary-as-notice entries and Windows reparse points. A real
observer test verifies that executable contents are never read. A generic-key secret
scan false positive on a Python diagnostic was removed by renaming the local variable;
no scan suppression or protection change was introduced. The final complete-history
scan passed. The superseded failed/cancelled CI remains historical evidence.

Post-merge naming verification scanned all 1,171 tracked files in the seven clean
implementation repositories with zero findings; the two exact DesktopPlatform
provenance paths were used. Local locked restore and Release build with the required
.NET 10.0.400 passed without warnings/errors, as did all four architecture tests.
The machine's installed 10.0.401 was not substituted: the exact SDK was downloaded
from official release metadata, its SHA512 verified, and retained in the task worktree.

## Automatic publication and runtime evidence

Contracts main [CI/publication](https://github.com/ArcForges/Contracts/actions/runs/35533334820)
and [security](https://github.com/ArcForges/Contracts/actions/runs/35533334825) passed at
its merged commit. Published `1.0.0-ci.56.1` was independently downloaded: all 13
original NuGet members match the candidate (the registry adds its signature), both
npm tarballs are byte-identical, and all 20 Maven candidate files match public
Central bytes. Both main CI platforms ran isolated real candidate consumers,
including the existing Native AOT transport/codec probes. These remain bootstrap
contract tests, not a claim that production business handlers exist.

DesktopPlatform main [CI/publication](https://github.com/ArcForges/DesktopPlatform/actions/runs/35533676317)
passed at its merged commit. Its ten-package `1.0.0-ci.14.1` candidate was downloaded
and passed the owning archive/native-identity verifier. Main CI repeated the actual
native build/ABI checks, package verification and Windows/Linux isolated consumers.
All ten public NuGet packages were independently downloaded. Their 599 original
archive members match the verified candidate; only registry-added signatures are
excluded from the comparison.

The initial public NuGet downloads returned 404 immediately after successful upload.
Propagation subsequently completed for both owners and all comparisons passed. The
attempt receipts are retained; an upload success alone did not close acceptance.

## Retained receipts and boundaries

DesktopPlatform retains local, remote, CI, review and post-merge records under
`.worktree/wp00-04-reference-baselines/artifacts/evidence/`. Contracts retains its
scan, review inputs and candidate evidence under
`.worktree/wp00-04-reference-naming/artifacts/`. Both implementation task branches,
the Design profile/evidence branches and their worktrees are retained. Primary
checkouts were pulled after merge; post-merge checks used the merged source.

This stage establishes fixed planning inputs and an exercised maintenance procedure.
It does not establish complete application behavior, live commercial operation or
later release gates. The completed design-stage matrix gates remain closed on their
original evidence; this registration does not claim to close them again.

No unavailable external prerequisite blocks this substep.
