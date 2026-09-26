# WP02 build and publication governance stage acceptance

Authority: [WP02.90 and the parent completion gate](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.90), [staged producer integration](../planning/README.md#staged-artifact-integration), [producer responsibilities](../planning/producer-artifacts-and-integration.md) and [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017). Result: the bounded WP02 stage passes. The [source and evidence index](wp02-stage-acceptance.json) identifies its exact owner sources, producer candidates, retained consumer pins and later closing gates. It is not the WP06 integration manifest or a commercial release manifest.

## Research, decisions and complete ordered plan

WP01 stage acceptance and all six WP02 substep receipts were inspected. WP02.05 supplies the latest nine reviewed implementation merges, successful applicable PR checks, required main publication/deployment results and clean primary fast-forwards. Current package manifests and consumer selections were read from those sources. The 43-project managed graph remains intact. Source comparison against the WP02.02 sweep found no changed managed AOT/trim/diagnostic posture; the intervening build-metadata target's Git-command stderr handling does not suppress compiler or AOT diagnostics.

No implementation, dependency upgrade or fresh producer publication is required to assemble these deliverables. Owner-specific SDK/JDK and bootstrap package pins are intentional; agreement means conformance to assigned runtime/licence profiles, not forcing every owner onto a new producer version. Historical runtime and artifact comparisons remain evidence at their recorded sources, not a mandate to repeat them. The planning reference to an exclusively private candidate feed is clarified to match the already accepted public-candidate publication protocol and restricted publisher credentials.

The ordered plan, established before this documentation change, is:

1. Bind the completed WP02.00–02.05 and WP01 receipts to the latest accepted owner sources and publication results. Inspect only relevant source drift and current package/consumer selections.
2. Write the six-condition acceptance matrix, actual artifact inventory, provider evidence and explicit later-owner/untested boundaries. Clarify candidate access without changing immutable promotion or stable-closure rules.
3. Review the complete documentation diff and validate local links, source identities, cross-document consistency and whitespace. Run no product build, runtime test, package download or hash audit.
4. Create `[WP02 · SubStep 02.90]` Design documentation PR, fix concrete review findings, merge without CI and fast-forward the clean Design primary. Retain the branch/worktree.
5. Update Plan Current task to WP03.00 in another retained worktree, review/merge its documentation PR without CI and fast-forward Plan. Begin the next step only through its own research and bounded plan.

## Parent completion conditions

| Condition | Accepted evidence | Current-stage result |
|---|---|---|
| Pinned toolchains and locked restore without central-version overrides | [WP02.00](wp02-00-implementation-evidence.md), current owner-local locks and [WP02.05 admission](wp02-05-implementation-evidence.md) | All 43 managed project locks and four npm roots remain governed; Kotlin/Gradle and Python tooling retain exact selected inputs. Historical isolated/offline restore evidence is retained. Current reduced CI restores the reviewed closure. |
| Warnings-as-errors with owned waivers | [WP02.01](wp02-01-implementation-evidence.md) and current affected PR/main CI | All 43 managed projects have evaluated policy; 17 historical rejection cases establish enforcement. Active authored diagnostic-debt waivers remain empty. Kotlin/Java/TypeScript checks retain their own fatal-warning policy. |
| Complete AOT/trim posture and diagnostic disposition | [WP02.02](wp02-02-aot-sweep-evidence.md), reviewed source drift and current AOT compilation jobs | 31 selected managed analysis postures; historical expanded diagnostic/suppression/blocking lists are empty. Remaining build/test tools are not invented AOT deliverables. This stage does not repeat the expanded runtime sweep. |
| Correct runtime and owner/IDE boundaries | [WP02.03](wp02-03-runtime-boundary-evidence.md), [WP02.04 reduction](wp02-04-implementation-evidence.md) | Independent owner builds, package-only consumer references and Web npm/esproj dispatch are established. No sibling producer checkout or CMake/vcpkg is required by ordinary application restore. |
| Independent version axes and observable build identity | [WP02.04](wp02-04-implementation-evidence.md) and latest provider jobs in [WP02.05](wp02-05-implementation-evidence.json) | Compiled support/source/run identity and candidate metadata exist. Each axis retains its actual value or explicit not-produced/not-applicable state; future business producers are not fabricated. Historical runtime readback is not relabelled as a new observation. |
| Executable dependency policy and recurring upgrade review | [WP02.05](wp02-05-implementation-evidence.md) | Nine owners enforce current admission, immutable coordinates, publisher/import scope and upgrade receipts. All 120 targeted offline cases passed across owners. Framework-major/runtime assessment remains recurring VG-08 work at its trigger. |

## Actual artifact and provider boundary

DesktopPlatform source `fe8476d0e137ab91af0a0a189419c7bd6cc68114` produced NuGet candidate **`1.0.0-ci.22.1`** in [the successful publication run](https://github.com/ArcForges/DesktopPlatform/actions/runs/35688808413). The current ten-package allowlist is Build.Policy, five managed native packages and four **win-x64** runtime packages. Native candidates carry headers, import libraries, dependency/source notices, SBOM and manifests; the pipeline checks the original candidate before authenticated publication. Existing ABI/version/error probes do not implement WP13 media/image/colour/timeline functions or additional runtime RIDs. Local vcpkg reuse remains the accepted WP02.00 policy.

Contracts source `48654ae3f2d37a98c949f1fa644f3da5c1642b58` produced NuGet/npm **`1.0.0-ci.78.1`** and its separate Maven **`1.0.0-SNAPSHOT`** channel in [the successful publication run](https://github.com/ArcForges/Contracts/actions/runs/35688812523). Its candidate inventory contains NuGet, two npm packages, a Maven bundle and a descriptor artifact with source/build/schema/lock metadata. The current Hello schema and generated bindings remain bootstrap compatibility inputs; complete production schemas, generated language packages and fixtures are WP03 work. The SNAPSHOT is development evidence with retention, not a permanent formal Central release.

The exact publication run and source identify each retained candidate manifest and its original hashes. Those manifests remain the producer hash authority; this documentation-only step does not redownload, re-extract or recompute public bytes. Required candidate identity, signatures, licence/source checks and upload/deployment results were already verified by the producing pipelines. The [WP02.05 source/result receipt](wp02-05-implementation-evidence.json) records all nine successful main results, including desktop portable releases, persistent-identity Android signing, Cloud Native AOT image/Worker publication, AI deployment and Web static deployment. Provider success is not a live application test.

Consumer selections remain explicit and independently versioned:

| Consumers | Retained first-party selection |
|---|---|
| ArcNotes, ArcScope, ArcSlate | Build.Policy `1.0.0-ci.20.1`; Contracts.PublicApi `1.0.0-ci.36.1` |
| Cloud | Build.Policy `1.0.0-ci.21.1`; NuGet PublicApi and npm proto/api-client `1.0.0-ci.74.1` |
| AI | npm proto `1.0.0-ci.44.1` |
| Web | npm proto/api-client `1.0.0-ci.44.1` |
| Mobile | Maven contracts `1.0.0-ci.60.1` |

These are the actual reviewed bootstrap locks, not claims that every application consumed the newest producer candidate. WP02.05 did not alter dependency versions. Source-free restore and the unchanged Build.Policy round trip retain their accepted historical proof; a forced consumer upgrade would add no stage requirement. WP03/04/06 will publish and join their actual required contract/value/runtime closures in dependency order.

## Remaining gates and coverage

No unresolved ownership, selected-toolchain or publication-mechanism decision blocks this stage. WP03 owns complete schemas and public/internal generated outputs; WP04 owns foundation values; WP05 owns the broader architecture/invariant policy suite; WP06 owns real foundation transport/native/runtime integration and its first joined manifest; WP11/13 own actual containment/parser/native capabilities; WP21 owns progressive Cloud consolidation; WP50 owns production signatures, full product/recovery and commercial acceptance. Recurring VG-08 is not permanently closed by one no-upgrade baseline.

No new build, runtime, device, browser, live service/inference, installed-consumer or public-release upgrade test ran for WP02.90. No macOS CI or macOS artifact is claimed. Desktop CI/release coverage is win-x64, win-arm64 and linux-x64; current DesktopPlatform native runtime publication is win-x64. Stable-tag publication remains deliberately unexecuted. Historical broader platform observations remain historical only. No artifact download, toolchain installation, replacement version, tag, signing operation or deployment was performed to create this acceptance receipt.
