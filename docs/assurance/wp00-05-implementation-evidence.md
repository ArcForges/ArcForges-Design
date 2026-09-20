# WP00.05 implementation evidence

> Status: Completed: source, review, CI, public-package and real deployment acceptance passed.
> Owning substep: [WP-00.05](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.05).
> Verified on: 2026-09-20 UTC.

## Authority and reviewed changes

[Design PR29](https://github.com/ArcForges/ArcForges-Design/pull/29), merged as
`e2dd78058ce2d4bd1a8434a34d049bbc1158eacb`, establishes the
[runtime and source ownership profile](../architecture/30-runtime-and-source-ownership-policy.md).
It corrects the stale ten-implementation-repository count to nine, records bounded
source checks and actual-build evidence separately, and preserves the already
assigned later product migrations. Design remains documentation authority. Earlier
[WP00.04 evidence](wp00-04-implementation-evidence.md) and its prerequisite stages
were verified before these changes; no future producer is demanded at this stage.

| Owner | Reviewed PR and merged revision | Latest-head PR checks |
|---|---|---|
| Contracts | [24](https://github.com/ArcForges/Contracts/pull/24), `d716045854e2e401a1a536ba2ee5c62ad1c4e8ab` | [CI](https://github.com/ArcForges/Contracts/actions/runs/35535424235) and [security](https://github.com/ArcForges/Contracts/actions/runs/35535424372) passed |
| Cloud | [5](https://github.com/ArcForges/Cloud/pull/5), `4571ec8692235485712d4c4e3ef4886c162f2574` | [CI](https://github.com/ArcForges/Cloud/actions/runs/35535430473) passed |
| AI | [10](https://github.com/ArcForges/AI/pull/10), `944edfe88718fc5f72a42ea0bed1c495307c22df` | [CI](https://github.com/ArcForges/AI/actions/runs/35535435971) passed |
| DesktopPlatform | [52](https://github.com/ArcForges/DesktopPlatform/pull/52), `08c46ab9fe955c60c28e7106df519eb55bd8e3ba` | [All 18 checks](https://github.com/ArcForges/DesktopPlatform/actions/runs/35536350533) passed |

Every complete PR diff was reviewed; findings were fixed before merging the checked
head. The [implementation claim table](https://github.com/ArcForges/DesktopPlatform/blob/08c46ab9fe955c60c28e7106df519eb55bd8e3ba/docs/runtime-ownership.md#reviewed-claim-corrections)
records each changed source path, previous claim, accepted replacement and validation.
Contracts corrects packaged TypeScript README targets and public business transport;
Cloud and AI correct obsolete database ownership claims. Historical bootstrap notes
retain their source-bound results and explicitly identify current authority.
DesktopPlatform corrects the desktop/helper comment and repository count, adds the
closed runtime registry/verifier/tests, registers its source provenance, and requires
the new Windows/Linux gate before package production. Runtime behavior, package IDs,
Hello compatibility and signing continuity are preserved.

## Runtime, source and review acceptance

The policy binds Design's exact revision and profile digest
`3be292a0fffc23dbdb0f7d1d0fe41ad250e03661d02fee79e4d4c58b8af33e2b`.
The runtime registry digest is
`66813be2a63b4f76c9f2fb0effd7661fd76e3a71b9bac07ea9177b88e56fc6ea`.
It assigns all 75 current projects across nine owners and requires their actual
source/provenance inventories. It does not copy the Contracts forbidden-name list
or import AGPL tooling into Apache owners. Ten former monorepo source groups have
explicit owner/disposition records verified against extraction revision
`99bfe7d695ed0d65a0d035af7d219fc9b86100f5`; absent old source is not recreated.

The 18 runtime test groups reject incomplete/duplicate owners, changed roles or
runtime identities, unsafe paths, unassigned projects/source, restored retired trees,
wrong/missing frameworks, conditional/false AOT overrides, escaped imports, obsolete
dependency aliases, extra runtime environments/hosts, invalid Workflow/AI bindings,
and unsupported Mobile targets. Review additionally tightened exact host assignment,
unversioned scoped npm alias detection and framework checks; all affected tests were
rerun. Existing 11 licence, 41 provenance/native, 15 Design and 12 reference groups
also passed: 97 local groups in total. The actual provenance scan, repository hooks,
whitespace check and complete-history secret scan passed without suppressions.

Both PR and merged-main Windows/Linux reports passed with nine source snapshots,
75 projects, 1,328 files and 34 actual Debug/Release MSBuild AOT property evaluations
using .NET SDK 10.0.400. Their policy identities match the reviewed registry. These
read-only declaration/property checks remain distinct from native package execution.
The fresh post-merge audit used all nine real local primary roots, not merely the
pinned snapshots; their source inventory and existing naming scan passed cleanly.
The current Design preview passed with 135 terms, 148 names, 429 invariants and
16 forbidden aliases.

| Owner | Actual clean merged/current main | Projects |
|---|---|---:|
| DesktopPlatform | `08c46ab9fe955c60c28e7106df519eb55bd8e3ba` | 35 |
| Contracts | `d716045854e2e401a1a536ba2ee5c62ad1c4e8ab` | 15 |
| ArcNotes | `e40423a1b14ce8341de35748cc2a093c7c9b77a7` | 4 |
| ArcScope | `d247dcff36fd1123a70e5e59967a9b2294a2eeac` | 4 |
| ArcSlate | `b0d255f54fb560a534cc493d5645ca4bc7b4bd0e` | 4 |
| Cloud | `4571ec8692235485712d4c4e3ef4886c162f2574` | 5 |
| AI | `944edfe88718fc5f72a42ea0bed1c495307c22df` | 1 |
| Web | `84939ca1fde0f0653d2cb4d8b8f9e5dd1057abb5` | 4 |
| Mobile | `5031d837d2e7bf9dd1b681c837c942d2b74dc65e` | 3 |

All nine primary HEADs were independently compared with remote main and were clean.
The unchanged product repositories needed no empty PRs. Source checks do not claim
that their Hello applications implement the full commercial requirements.

## Publication and real runtime evidence

Contracts main [CI/publication](https://github.com/ArcForges/Contracts/actions/runs/35536018400)
and [security](https://github.com/ArcForges/Contracts/actions/runs/35536018415) passed.
The owning archive verifier accepted `1.0.0-ci.58.1` at its merge revision. Independent
public downloads matched all 13 original NuGet members, both complete npm tarballs
and all 20 Maven candidate files. The public npm README bytes carry the corrected
Web/Kotlin distinction. The proto tarball SHA256 is
`5cc015e2c1f592bcaeff9a6fdc537b6fdda81fd61fa85c22ef230000e4d706d6`;
the API-client tarball SHA256 is
`e95cdf104ae8d146fb5715a1c87f85a8bfd1265dee67043dd35a8f1244e3fff1`.
Both main CI operating systems ran the isolated real candidate consumers.

DesktopPlatform main [CI/publication](https://github.com/ArcForges/DesktopPlatform/actions/runs/35536843264)
passed. Its ten-package `1.0.0-ci.15.1` candidate passed the owning archive/native
identity verifier at the merged revision. Both operating systems passed isolated
package consumption, and the actual Windows native build/ABI checks passed.
All ten public NuGet packages were independently downloaded; all 599 original
archive members match the verified candidate. Registry-added `.signature.p7s` is
the only excluded member. Initial 404 responses were retained; the last media
package was obtained through a cache-bypassing public request after its version
index listed the release. Upload success alone did not establish availability.

Cloud main [CI/deployment](https://github.com/ArcForges/Cloud/actions/runs/35535883611)
passed for candidate `0.1.0-ci.18.1`. The downloaded candidate passed its owning
verifier. The published container digest is
`sha256:447ef781549d707fa4e546fa98e0d33b290a1d067ae862e6221ef90d3e115ee0`;
the worker bundle SHA256 is
`37d36ff37803fd4dfc5fef623ddc4a1b5e607d50782c3bf7c949b1dbb4e8fa9c`.
Deployed Worker and Container revisions match the merge. CI exercised the real
published Kotlin client; an additional local public-HTTPS run independently verified
Native AOT health, ordinary/Unicode binary gRPC-Web greetings, invalid-argument and
resource-exhaustion statuses, and Worker routing boundaries. Its immutable client
version is `1.0.0-ci.36.1`. This is stateless Hello evidence, not D1 business behavior.

AI main [CI/deployment](https://github.com/ArcForges/AI/actions/runs/35535890121)
passed for candidate `0.1.0-ci.26.1`, worker version
`daae29e9-1712-4f86-9700-36a42cc87087`. The owning verifier accepted the downloaded
candidate at its actual merge; candidate JSON SHA256 is
`a48dcfd9f35b5c1972d2079606073b742681103f81ca74e966d44218a47c26ef`.
Live admission matched that candidate. The real Workflow used Workers AI
`@cf/openai/gpt-oss-20b`, made two model calls around `say_hello`, and returned the
expected Hello result. Local model mocks and 56 source/81 tooling tests are recorded
separately from this real provider evidence; no additional paid inference was needed.

## Retained evidence and boundaries

Each changed implementation owner retains branch
`codex/wp00-05-runtime-ownership` and `.worktree/wp00-05-runtime-ownership`.
DesktopPlatform's ignored `artifacts/evidence`, PR/main runtime reports, downloaded
candidate and public-package comparisons bind the review and source identities.
Contracts retains the candidate and public-registry attempt receipts; Cloud/AI retain
the downloaded candidates, deployment receipts and real runtime evidence. Design
retains its profile and completion-evidence branches/worktrees. Primary checkouts
were pulled after merges and post-merge checks used the actual merged code.

Microsoft Native AOT and Cloudflare Workflow/Workers AI declarations were checked
against the official sources on 2026-09-20, as recorded in the authority profile.
No SDK/provider upgrade was inferred. The shared placeholders and helper remain
explicit scaffolds; existing Hello/native-gRPC compatibility, Mobile prerelease
identity and JVM preview retain their named later owners. Full assistant/business
behavior, all Web surfaces, full RID/native families and commercial activation
remain required at their scheduled stages. This substep makes their current
assignments enforceable; it does not close those later acceptance gates.

No unavailable external prerequisite blocks this substep.
