# WP00 stage acceptance

> **SUPERSEDED IN PART (2026-10-08, [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021))**: the React/TypeScript, Node/npm and Kotlin/Maven/Gradle toolchain statements and the statements that rejected Blazor WebAssembly or .NET MAUI, and the sole Cloudflare Workflow model/tool loop of the AI row (P2-021 item 5). The Contracts, AI, Web and Mobile rows of the stage table below are kept unedited as recorded on 2026-09-20; their current replacement rows follow the table under the same dated marker (P2-021 items 1 to 5 and 8). The stage result, its status line and its evidence are retained as dated history and are not rewritten.

> Status: Completed for the authority, rights, runtime and source-inventory stage.
> Owning substep: [WP-00.90](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.90).
> Verified on: 2026-09-20 UTC, against Design `f8ef5561f5ff55dbecec1b01bc186427273520ef`.

The [machine-readable acceptance receipt](wp00-stage-acceptance.json) records all seven
actual source revisions, original licence assignments, instruction/policy hashes,
inventory counts, exact candidate identities and main CI links. This is a bounded
stage receipt, not a Cloud release manifest or a claim of completed applications.
It consumes the [stage matrix](../planning/producer-artifacts-and-integration.md#2-stage-and-fixture-replacement-matrix)
and requires no future Contracts/Foundation package. No implementation source or
published package changed during this substep.

## Authority, licence, runtime and instruction derivation

Current accepted Design governs every row. The [portfolio](../requirements/00-product-scope-and-portfolio.md),
[project authority](../architecture/27-platform-projects-and-application-assistants.md),
[licence declaration profile](../architecture/01-solution-and-project-layout.md#41-project-declaration-and-verification-profile)
and [runtime profile](../architecture/30-runtime-and-source-ownership-policy.md) are
shared inputs. Each repository's actual `AGENTS.md` was read completely and compared
with these definitions; its exact Git-blob SHA256 is recorded in the receipt.
DesktopPlatform's `CLAUDE.md` delegates to `AGENTS.md`. Existing contributor checks
remain owner-specific. These instructions are implementation guidance derived from
Design; historical bootstrap instructions cannot amend Design.

| Owner | Original licence | Runtime and owned boundary | Instruction derivation and retained limit |
|---|---|---|---|
| DesktopPlatform | AGPL-3.0-only | AOT-compatible C# mechanisms, native C ABI producers, parent-owned AOT helper | Architecture 27 shared/package boundaries; pinned locked tools, explicit package admission, no placeholder publication or sibling-source consumer. Eleven shared placeholders and the helper remain scaffolds. |
| Contracts | Apache-2.0 | Authored proto and generated C#/TypeScript/Kotlin artifacts; separate build/test tools | Architecture 27 and wire registry: generator-owned outputs, exact published consumers, no credentials or adjacent-source build. Hello/native-gRPC fixtures are compatibility evidence; business clients use binary gRPC-Web. |
| ArcScope | AGPL-3.0-only | Independent Avalonia/C# Native AOT acquisition/measurement application | Same product/runtime authority; no sibling-product coupling, preserved TLS/deadlines/cancellation and native evidence. Acquisition/measurement behavior remains at its producers. |
| Cloud | AGPL-3.0-only | C# Native AOT Container behind Worker; D1 business authority, R2 objects, DO coordination | Architecture 27 and CF contract: exact Contracts, one business owner, no AI loop, tested image/Worker promotion. Current anonymous stateless Hello does not implement D1 transactions or production recovery. |
| AI | AGPL-3.0-only | Sole Cloudflare Workflow model/tool loop with direct Workers AI | Runtime profile: no local/production Node agent, no Cloud business transactions, private deployment, mocks distinguished from real inference. Full Harness and recovery remain WP52. |
| Web | AGPL-3.0-only | React/TypeScript static browser outputs; Node is build tooling | Web/project authority: separate site/account/chat/operations, exact npm, public bundles without secrets, candidate promotion. Current Site Hello does not establish the other production surfaces. |
| Mobile | Apache-2.0 | Kotlin/Jetpack Compose Android; development JVM preview only | Mobile/project authority: exact Maven, protected signing and actual dependency notices, no iOS/desktop distribution. Existing prerelease identity and JVM target remain until WP30's already assigned migration. |

(**SUPERSEDED IN PART (2026-10-08, [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021))**: the Contracts, AI, Web and Mobile rows above are the 2026-09-20 text, kept unedited as dated history. The current replacement rows are below; each keeps the same columns and carries its own dated marker.)

| Owner | Original licence | Runtime and owned boundary | Instruction derivation and retained limit |
|---|---|---|---|
| Contracts | Apache-2.0 | Authored proto and generated C# artifacts; separate build/test tools. The TypeScript and Kotlin generated artifacts are superseded (2026-10-08, [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 4: stopped channels under CON.40 after consumers migrate; `@arcforges/ai-internal` retained) | Architecture 27 and wire registry: generator-owned outputs, exact published consumers, no credentials or adjacent-source build. Hello/native-gRPC fixtures are compatibility evidence; business clients use binary gRPC-Web. |
| AI | AGPL-3.0-only | C# Harness model/tool loop in the Cloud host, with Workers AI invoked only through the `env.AI` binding by the thin TypeScript outbound handler (superseded 2026-10-08 by [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 5: the sole Cloudflare Workflow loop no longer applies; the AI runtime role ends and the Harness is HAR.40 under Cloud) | Runtime profile: no local/production Node agent, no Cloud business transactions, private deployment, mocks distinguished from real inference. Full Harness and recovery remain WP52. |
| Web | AGPL-3.0-only | Blazor WebAssembly application and C# static Site outputs (superseded 2026-10-08 by [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 2: the React/TypeScript outputs are retired); Node is build tooling that only invokes wrangler (P2-021 item 1) | Web/project authority: separate site/account/chat/operations, exact .NET SDK and NuGet versions admitted under WP02.05 (superseded 2026-10-08 by P2-021 item 8; the only npm pin that remains is for wrangler, and `@arcforges/ai-internal` is retained for the Cloud Worker under P2-021 item 4, not as a Web pin), public bundles without secrets, candidate promotion. Current Site Hello does not establish the other production surfaces. |
| Mobile | Apache-2.0 | .NET MAUI Android for `net10.0-android` with Mono AOT for release (superseded 2026-10-08 by [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3 and IRD-23: the Kotlin/Jetpack Compose Android runtime and the development JVM preview are retired; the migration is owned by AND.40) | Mobile/project authority: exact NuGet, protected signing and actual dependency notices, no iOS/desktop distribution. The existing prerelease identity `io.github.arcforges.mobile` remains until AND.01 changes the applicationId (target `com.arcforges.mobile`). |

ArcScope's instruction file's merge-authorization clause was respected by
the user's explicit automatic-merge instruction. No permission or licence grant is
inferred from that authorization. Contracts and Mobile do not import AGPL checks.
No old monorepo document, reference feature or deprecated-input body was promoted to
authority; archived bodies were excluded before corpus reading.

## Six prerequisite substeps on the current closure

| Substep | Current acceptance evidence |
|---|---|
| 00.00 naming | Single Contracts naming policy and its closed declaration/provenance registrations; fresh seven-root scan of all 1,175 source files passes with no findings. Published identities and exact exceptions remain preserved. |
| 00.01 vocabulary/invariants | Immutable export verification and fresh current-Design preview both pass: 135 term rows, 148 names, 429 invariants and 16 contextual aliases. Citation/anchor/dependency checks pass. Existing 15 independent negative groups pass in current DesktopPlatform CI. |
| 00.02 licences | Fresh family audit covers all 67 projects and reference directions. Actual owner build declarations pass in current CI; the desktop C# check was freshly run in an isolated worktree and verifies four evaluated projects. |
| 00.03 provenance | Every owner-specific source checker passes at its actual clean revision: 1,166 files, 184 reused files, 267 retained records. The last count includes superseded records. Existing actual packaging/notice acceptance remains bound to each unchanged or newly verified candidate. |
| 00.04 reference inputs | All three matrices and their 69 rows match registration; two exact Git identities resolve; the packaged observation matches. A fresh real drift check passes. Only permitted directory entries and two text notices are read, never packaged binaries. |
| 00.05 current claims | Seven-owner runtime/ownership registry, 67 projects and all source assignments pass; reviewed stale-claim replacements and historical dispositions match current Design. Windows/Linux source gates and 34 effective AOT-property checks pass in merged-main CI. |

The current-stage runs use the actual owner implementations: C# desktop tooling,
TypeScript Cloud/Web, JavaScript AI and Python Contracts/Platform/Mobile. An initial
attempt to use a different owner's Python provenance schema was rejected; no policy
was relaxed. The correct C# owner check then passed in a retained isolated
worktree. The existing 97 Platform negative/positive groups and Contracts naming
negative tests were verified through the latest passing CI at the same source
revisions; unchanged tests were not represented as newly authored tests.

[WP00.03](wp00-03-implementation-evidence.md), [WP00.04](wp00-04-implementation-evidence.md)
and [WP00.05](wp00-05-implementation-evidence.md) retain their exact review,
publication and real-integration evidence. Earlier implementation notes that mark
CI as pending describe their original pre-merge observation; the current main run
links and downloaded candidate evidence in this receipt resolve that status without
rewriting history. No important current-stage owner or recovery decision remains
unassigned. Later mechanisms retain the already defined owners below.

## Exact candidates and actual runtime reality

| Owner | Exact accepted candidate | Evidence class and observed runtime |
|---|---|---|
| DesktopPlatform | `1.0.0-ci.15.1` | Ten public NuGet packages; 599 original members match the verified candidate. Actual Windows native build/ABI and Windows/Linux isolated consumers pass. Policy/data checks are separate from native probe execution. |
| Contracts | `1.0.0-ci.58.1` | Public NuGet, both npm tarballs and all 20 Maven files match the verified candidate; Windows/Linux isolated C#/TS/Kotlin/AOT consumers pass. These are Hello contract probes. |
| ArcScope | `0.1.0-ci.8.1` | Same independent five-host checks against its own source/candidate; original UI, Unicode and protocol error scenarios pass. |
| Cloud | `0.1.0-ci.18.1` | Real deployed Worker/Native AOT Container, published TypeScript/Kotlin clients and independent public HTTPS checks at the merge; ordinary/Unicode/invalid-argument/resource-exhaustion/routing cases pass. |
| AI | `0.1.0-ci.26.1` | Real private Workflow admission matches the candidate; two Workers AI model calls around the tool pass. Local mocks are a separate evidence class. |
| Web | `0.1.0-ci.22.1` | Public archive re-downloaded; all 49 listed members plus the manifest verified. Recorded real Chromium/Firefox/WebKit Cloud-button checks and static-delivery CI pass. |
| Mobile | `0.1.0-ci.14.1`, version code 1401 | Public release/signing/provenance receipts re-downloaded and hashed; all signed artifact digests match release metadata. Recorded API26/API36 emulator and signed public upgrade checks pass; no physical-device/store proof inferred. |

All linked main workflows were queried and confirmed successful at the recorded
commits. The receipt includes producer manifest/verification-archive SHA256 values,
Android signed APK/AAB hashes, desktop per-RID archive/smoke hashes and original
observed provider revisions. Unchanged desktop/Android binaries were not rebuilt
or relabelled as new device runs. Prior public binary comparisons remain recorded
at WP00.03; this substep freshly verifies public metadata and acceptance attachments.

The desktop native runs observed Cloud
`2cf5a58633a7e09db05ebc1741f1cab83547a832`. They are not evidence that those same UI
runs were repeated against current Cloud
`4571ec8692235485712d4c4e3ef4886c162f2574`. Current Cloud and AI real runs are recorded
separately in WP00.05. This closure joins the current authority/inventory stage;
it is not a new family-wide production end-to-end execution.

Consumer pins remain explicit: ArcScope uses Contracts `1.0.0-ci.36.1`
and Build.Policy `1.0.0-ci.7.1`; Cloud uses Contracts `1.0.0-ci.36.1`; AI/Web use
`1.0.0-ci.25.1`; Mobile uses `1.0.0-ci.54.1`. New producer publication does not silently
upgrade running consumers. Exact lockfiles and candidate provenance remain the
version authority, not an invented family-wide latest-version requirement.

## Remaining stage owners and disposition

- WP01 owns physical reconciliation; WP02/WP05 own policy distribution and expanded enforcement; WP03 owns complete generated business contracts. Current inventory checks cannot satisfy those later capabilities.
- WP06 owns the full transport/runtime foundation, including real Android/browser/CF/R2 paths; WP11/WP13 own real hostile-parser containment and complete functional native families/RIDs.
- WP14–17 and each product owner implement the full embedded assistant/product behavior; WP21–26 own actual D1/business/object/device integration and recovery. WP52 owns the full sole Harness and its failure/recovery proof.
- WP30 owns Android identity/stable-toolchain migration; WP31/WP32 require physical device, push, signing and store evidence. WP47–49 own the required complete Web surfaces.
- WP45/WP46/WP50 own operational drills, independent restore, joined production recovery and commercial activation. Invariant implementation remains with its assigned owners under [PG-11](open-gates-register.md#rule-pg-11); current corpus verification preserves [PG-21](open-gates-register.md#rule-pg-21), without closing runtime gates.

For the owned policy/inventory artifact, device, billing account, signing key, paid
inference and R2 object lifecycle are **not applicable** prerequisites. Their actual
later gates remain open; no unavailable external prerequisite blocks WP00.90.
The stage neither claims paid activation nor requests production secrets.

The Design acceptance branch/worktree and ArcScope's unchanged desktop verification
branch/worktree are retained as `codex/wp00-90-stage-acceptance` and
`.worktree/wp00-90-stage-acceptance`. Local reports and downloaded public receipts
are under the Design worktree's ignored `.worktree/evidence/`. Documentation review,
full corpus preview and post-merge verification apply before advancing to WP01.
