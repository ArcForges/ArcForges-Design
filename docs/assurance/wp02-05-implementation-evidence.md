# WP02.05 dependency policy implementation evidence

Scope: [WP02.05](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.05), executed under [the researched ordered profile](wp02-05-dependency-policy-profile.md) and [P2-017 validation policy](../decisions/phase-2-specification-decisions.md#rule-p2-017). This is foundation dependency and publication governance, not product or commercial acceptance.

## Implemented behavior

All nine owners bind their actual dependency inputs to reviewed admission data. Existing exact lock versions are retained. Policy checks reject unadmitted dependencies, prohibited licence admissions, floating selectors, changed integrity under an already admitted coordinate, incorrect first-party publisher scope and missing upgrade evidence. Historical admission evidence cannot be replaced to authorize different bytes under an existing version. Existing native and source-provenance gates retain redistribution authority; a new policy declaration does not replace their file-level evidence.

DesktopPlatform admits 31 NuGet and 10 Python tooling coordinates and retains its reviewed native inventory. Contracts admits 166 NuGet/npm/Maven coordinates. Each desktop application admits 91 NuGet coordinates. Cloud, AI and Web admit 131, 195 and 351 external npm lock entries respectively, and bind their other existing toolchain/dependency inputs to review. Mobile reuses its existing 195-component Android inventory and validates its actual Gradle feeds, locks, source identities and public-client boundary. Entry counts are owner-local closure measures, not a cross-ecosystem package total.

Upgrade receipts bind actual inputs, owner/reviewer decisions, maintenance and licence/source evidence, and proportionate compilation/AOT, compatibility, security/SBOM and conditional local runtime/performance/migration assessments. Framework major changes require an explicit runtime-posture assessment; Android assessments use Kotlin/JVM/ART/R8 and the relevant native/transport implications. Recurring [VG-08](open-gates-register.md#rule-vg-08) remains an obligation at future upgrade triggers.

Candidate exceptions are exact existing foundation inputs. Stable core closures reject previews. DesktopPlatform now accepts deliberate canonical stable tags through its existing candidate chain, validating the peeled tag target and membership in main before publication. Its NuGet environment retains the main branch rule and adds only the reviewed `v*` tag rule. Publications share a serialized queue. Contracts keeps the accepted main npm candidate channel and Maven SNAPSHOT protocol. Existing OIDC, signing, allowlists and publication-candidate identity checks remain; no stable tag or test publication was created.

ArcScope and ArcSlate append their ArcNotes source-reuse successor records. AI and Web record the copied Cloud checker, tests and guide under their compatible AGPL boundary; Web retains the original record and its lint-fix successor. All source identities and existing notices remain explicit. Mobile's obsolete mandatory device and empty-cache upgrade instructions were repaired.

## Review and validation

Every owner received full PR review and concrete findings were repaired before merge. Findings included Linux-sensitive NuGet configuration casing, complete Git history for admission comparisons, historical-coordinate replacement, framework-baseline reset, duplicate npm coordinate integrity, actual Android feed enforcement, missing structural-reuse attribution, and source formatting/lint failures. Contracts secret scanning identified four public source hash rows repeated twelve times; the reviewed exception is limited to their exact path/hash lines in two receipt files and the `generic-api-key` rule. Scanner defaults and redaction remain enabled.

Targeted offline policy cases passed: DesktopPlatform 12, Contracts 13, each desktop application 12, each TypeScript owner 15, and Mobile 14. The desktop applications also passed cache-only locked restore, targeted managed compilation with zero warnings/errors, and full repository/provenance checks. Existing tools and caches were used. CI supplies the retained affected Windows/Linux compilation, Native AOT, packaging and security evidence. No runtime or end-to-end execution was required for these policy changes.

The unchanged Build.Policy publication/restore mechanism retains the round-trip evidence recorded by [WP02.00](wp02-00-implementation-evidence.md) and subsequent [WP02.04 receipts](wp02-04-implementation-evidence.md). New publication results are established by required provider jobs, without another public artifact download or installed-consumer cycle.

## Completion and evidence limits

All nine implementation PRs were merged after successful applicable latest-head checks. Required main build/publication/deployment jobs succeeded, expected merge commits were confirmed, and all primary checkouts were fast-forwarded cleanly. The [source/result receipt](wp02-05-implementation-evidence.json) records exact reviewed heads, merges, run identities, retained branches/worktrees and validation. This closes WP02.05 under P2-017; WP02.90 is the next stage acceptance step. The stable-tag path is source-reviewed and covered by offline refusal cases, but deliberately unexecuted. Historical runtime observations retain their original commits and are not new observations of these candidates.

No macOS CI, physical-device/emulator test, desktop GUI/browser E2E, live service/inference test, installed-package consumer or public-release upgrade test was added or executed. Removed platform coverage is not claimed. No SDK/vcpkg/emulator installation, dependency upgrade or WSL wrapper was used. Later schema/native capability and real consumer integration gates remain with WP03/WP06 and their assigned owners; production release remains WP50.

## Accepted owner results

| Owner | Reviewed and merged PR | Required main result |
|---|---|---|
| ArcNotes | [#9](https://github.com/ArcForges/ArcNotes/pull/9) | [Successful build/publication](https://github.com/ArcForges/ArcNotes/actions/runs/35688797135) |
| ArcScope | [#9](https://github.com/ArcForges/ArcScope/pull/9) | [Successful build/publication](https://github.com/ArcForges/ArcScope/actions/runs/35688248008) |
| ArcSlate | [#9](https://github.com/ArcForges/ArcSlate/pull/9) | [Successful build/publication](https://github.com/ArcForges/ArcSlate/actions/runs/35688252843) |
| Mobile | [#10](https://github.com/ArcForges/Mobile/pull/10) | [Successful build/publication](https://github.com/ArcForges/Mobile/actions/runs/35688243200) |
| Cloud | [#19](https://github.com/ArcForges/Cloud/pull/19) | [Successful build/publication](https://github.com/ArcForges/Cloud/actions/runs/35688528067) |
| AI | [#19](https://github.com/ArcForges/AI/pull/19) | [Successful build/publication](https://github.com/ArcForges/AI/actions/runs/35688532745) |
| Web | [#15](https://github.com/ArcForges/Web/pull/15) | [Successful build/publication](https://github.com/ArcForges/Web/actions/runs/35688537646) |
| DesktopPlatform | [#59](https://github.com/ArcForges/DesktopPlatform/pull/59) | [Successful build/publication](https://github.com/ArcForges/DesktopPlatform/actions/runs/35688808413) |
| Contracts | [#32](https://github.com/ArcForges/Contracts/pull/32) | [Successful build/publication](https://github.com/ArcForges/Contracts/actions/runs/35688812523) |

DesktopPlatform published candidate `1.0.0-ci.22.1`; Contracts published NuGet/npm `1.0.0-ci.78.1` and its separate Maven `1.0.0-SNAPSHOT` channel. Versions follow the committed main-channel selectors and successful provider run identities. ArcNotes experienced delayed push-event processing; its original merge subsequently produced a successful main publication without manual dispatch, replacement commits or extra versions.
