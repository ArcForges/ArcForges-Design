# WP02.04 version identity and CI reduction

Scope: [WP02.04](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.04), the [version identity profile](wp02-04-version-identity-profile.md), and the explicitly authorized [P2-017 CI/local policy](../decisions/phase-2-specification-decisions.md#rule-p2-017). This receipt covers foundation identity plumbing and the repository-wide execution-policy change. It does not establish complete business applications, future compatibility producers or commercial acceptance.

## Authority and execution

[Design PR 53](https://github.com/ArcForges/ArcForges-Design/pull/53), merged as `47db6670a727317939b91245e8c0b288834acf99`, established the researched inventory and complete ordered reduction plan before implementation. [Plan PR 3](https://github.com/ArcForges/Plan/pull/3), merged as `5b0563423555c8787385c01087c0ade5559d878d`, synchronized both execution profiles, AGENTS and the reusable single-task command. The current task remains WP02.04; no WP02.05 work was started.

Independent agents owned DesktopPlatform/Contracts, the three desktop products, and Cloud/AI/Web. The coordinator owned Mobile, authoritative documentation, dependency order and final review. Heavy local desktop builds ran sequentially using existing caches. No local toolchain, vcpkg, SDK or emulator was installed or reinstalled. Normal networking was used without WSL wrappers.

Mobile work was appended to its existing PR 9. Every other changed source owner received a new retained worktree and PR. Unrelated dependency PRs were left unchanged. Every complete PR received review, findings were corrected, and source merges required successful applicable checks on the latest reviewed head. Documentation-only PRs had no CI and merged after consistency review.

## Independent version sources and retained observations

All nine owners retain an explicit source catalog and an `arcforges.build-identity.v1` report. AppVersion, ContractSet, CapabilityVersion, NativeFormatVersion, StorageSchemaVersion, NativeAbiVersion, PolicySchemaVersion, ExtensionProtocolVersion and PackageVersion remain independent entries. Values originate in allocated release inputs, schema/descriptor identity, owned definitions or exact dependency locks; unavailable future producers have explicit states and owners. An absent implementation is not assigned a fabricated version. Source commit, dirty/local/CI state, run/attempt and source timestamp form a separate build identity.

The prior eight-owner implementation and runtime observations remain historical evidence at their original commits:

| Owner | Identity implementation | Accepted source | Main run |
|---|---|---|---|
| DesktopPlatform | [PR 57](https://github.com/ArcForges/DesktopPlatform/pull/57) | `96d1acebc74e7dcc7dbff7652763084b1cd95908` | [35590450948](https://github.com/ArcForges/DesktopPlatform/actions/runs/35590450948) |
| Contracts | [PR 30](https://github.com/ArcForges/Contracts/pull/30) | `e8b3e123b258fdf6f0b77268c60ea4d9e915e74b` | [35594600655](https://github.com/ArcForges/Contracts/actions/runs/35594600655) |
| ArcNotes | [PR 7](https://github.com/ArcForges/ArcNotes/pull/7) | `0c797e30690a10d8798ddca19ca7f37b16cecf01` | [35610729653](https://github.com/ArcForges/ArcNotes/actions/runs/35610729653) |
| ArcScope | [PR 7](https://github.com/ArcForges/ArcScope/pull/7) | `a26c2c91db49d1ac95d339b7988d215ed9b520e8` | [35613699865](https://github.com/ArcForges/ArcScope/actions/runs/35613699865), attempt 2 |
| ArcSlate | [PR 7](https://github.com/ArcForges/ArcSlate/pull/7) | `807ac12a86036dbd48b5a6bdf8fbeaa0a6f48430` | [35616616925](https://github.com/ArcForges/ArcSlate/actions/runs/35616616925) |
| Cloud | [PR 8](https://github.com/ArcForges/Cloud/pull/8) | `749de4b702a0de86859b8ae4a5f22ac90f856ffa` | [35620774565](https://github.com/ArcForges/Cloud/actions/runs/35620774565) |
| AI | [PR 17](https://github.com/ArcForges/AI/pull/17) | `dc6b8402d0885f1d7e33f3c1b3d3f86e26a80750` | [35623427130](https://github.com/ArcForges/AI/actions/runs/35623427130) |
| Web | [PR 13](https://github.com/ArcForges/Web/pull/13) | `1560ab754ccdeb71fe6fa994de488daa5c257376` | [35625293952](https://github.com/ArcForges/Web/actions/runs/35625293952) |

Those observations covered the existing library/ABI consumers, desktop metadata, Cloud compiled health identity, AI candidate/Workflow identity and Web browser readback. They were not repeated or relabelled as tests of the CI-reduction commits. Retained owner receipts identify their exact source, build and publication versions.

Before the policy change, Mobile's installed minified app exposed its packaged identity through the native build-information view on local API 26 and 36 emulators at clean source `97ef9d15ebdf4cacbefcfe8f407a1af4b9fffac2`. The receipt reports a local build, all nine axis states and the original runtime package inventory. Production `app/src/main` and `shared/src/commonMain` are unchanged between that observation and the reviewed reduction. Later packaging metadata and CI source identities are new; the old observation is not public-release or upgrade evidence. The task-owned emulators were stopped, and no device cycle followed this reduction.

## Final automated boundaries

| Owner | Removed | Retained |
|---|---|---|
| DesktopPlatform | Installed C17/managed/AOT consumers, CTest/PInvoke/owned-DLL execution, duplicate policy matrices, heavy push hook | Windows native compilation, Linux managed packaging, offline policy/security checks, narrow legal metadata inspection |
| Contracts | Consumer matrices, default real transport/disposable-signing fixtures, duplicate restoration and public archive polling | Generation/compilation, offline checks, candidate handoff integrity, main SNAPSHOT and deliberate-tag formal publication |
| ArcNotes / ArcScope / ArcSlate | Six macOS matrix entries, GUI/live smoke, implicit AOT execution, mandatory screenshots/smoke fields, repeated aggregate archive checks | Windows x64/ARM64 and Linux x64 AOT builds, one offline/static check set, security and three-candidate publication |
| Cloud | App/container startup, RPC/Worker/live deployment tests, hidden Kotlin loopback consumer and WSL fallback | Native AOT/image and Worker compilation, stopped-image legal extraction, original candidate deployment |
| AI | Default Workflow runtime, inference/live checks and required live-evidence release asset | Pure Node/offline tooling tests, sealed Worker candidate, deployment receipt |
| Web | Candidate/live Playwright, public asset comparisons and repeated full IDE/candidate build | Offline tests, static IDE declaration checks, one production build and deployment |
| Mobile | Both emulator matrices, public upgrade/download checks, disposable signing and debug/test candidate APKs | Windows/Linux compilation, shared/tooling offline tests, release APK/AAB, permanent signing and publication |

Runtime tools are explicit local opt-in, not hidden default CI prerequisites. Package IDs, product behavior, dependency versions, immutable releases and signing continuity are preserved. Historical macOS source support remains available where present; new automated desktop releases do not advertise nonexistent macOS assets. Scope/Slate append provenance r3, and Mobile appends resource profile r6 while retaining every prior admission unchanged.

Contracts publication now completes at provider upload/deployment status. The serialized SNAPSHOT publisher checks the latest main reference and skips a superseded commit instead of rewinding the channel. Formal Central publication still requires an intentional tag, signatures and matching deployment identity/coordinates at `PUBLISHED`; no formal tag was created for this reduction. Routine public archive downloads and hash/member/consumer cycles are removed.

## Review and validation

Local checks were scoped to the changed orchestration. Each desktop owner compiled with zero warnings/errors and passed 97 offline unit tests; loopback integration was excluded. Mobile passed 56 Python tests, and the specific licence-inventory repair passed its 12 relevant tests. DesktopPlatform/Contracts ran targeted Python publication/identity checks. Cloud, AI and Web ran their affected static/offline checks using installed dependencies. Hosted CI supplies the clean producer/package results; local checks are not described as hosted execution.

Review and CI exposed concrete omissions that were fixed: Contracts' new test required a source-inventory entry; Cloud's Gradle `check` still invoked a real loopback client and was detached from it; Mobile's licence staging still enumerated removed debug/test APKs and now uses the release archive set. Mobile's three obsolete standalone CodeQL baselines were retired after fresh checks confirmed exact category/ref and zero results; current CI categories and PR analysis history were preserved. These repairs do not waive retained compilation, security or signing checks.

Post-merge verification is limited to the expected merge commit, required main build/publication/deployment job result and clean primary fast-forward. No public release archive/image/site was downloaded for acceptance, no checksum comparison cycle was added, and no browser/device/service/inference test was restarted. Provider deployment success is not a live-service test.

## Completed source merges and publication

All applicable latest-head PR checks and the required main publication/deployment jobs succeeded. Primary checkouts are clean at the recorded merges; branches and worktrees remain retained. The [machine-readable receipt](wp02-04-implementation-evidence.json) records reviewed heads, all relevant workflow links and scoped local checks.

| Owner | Reviewed PR | Merge commit | Successful main run | Publication |
|---|---|---|---|---|
| DesktopPlatform | [PR 58](https://github.com/ArcForges/DesktopPlatform/pull/58) | `940532d91c64d65d3d654ab031ad1985c466f91c` | [35641624352](https://github.com/ArcForges/DesktopPlatform/actions/runs/35641624352) | NuGet `1.0.0-ci.21.1` |
| Contracts | [PR 31](https://github.com/ArcForges/Contracts/pull/31) | `9f0e90f65d57f405fcee311d467a57a255dfd644` | [35642372095](https://github.com/ArcForges/Contracts/actions/runs/35642372095) | NuGet/npm `1.0.0-ci.74.1`; Maven `1.0.0-SNAPSHOT` |
| ArcNotes | [PR 8](https://github.com/ArcForges/ArcNotes/pull/8) | `2dee20b0c1d9acaf3d83b20dfd045e1e070e082c` | [35642212929](https://github.com/ArcForges/ArcNotes/actions/runs/35642212929) | `v0.1.0-ci.17.1` |
| ArcScope | [PR 8](https://github.com/ArcForges/ArcScope/pull/8) | `8316d0bded118b0a76223c35cd42d7b1096b6104` | [35642226807](https://github.com/ArcForges/ArcScope/actions/runs/35642226807) | `v0.1.0-ci.16.1` |
| ArcSlate | [PR 8](https://github.com/ArcForges/ArcSlate/pull/8) | `26331c3b240a95603d2f9d25949f47899ac484e0` | [35642242698](https://github.com/ArcForges/ArcSlate/actions/runs/35642242698) | `v0.1.0-ci.16.1` |
| Cloud | [PR 9](https://github.com/ArcForges/Cloud/pull/9) | `9910c8bbc8485f206aaa8e88fe4b490073661078` | [35642540451](https://github.com/ArcForges/Cloud/actions/runs/35642540451) | `cloud-0.1.0-ci.28.1` |
| AI | [PR 18](https://github.com/ArcForges/AI/pull/18) | `3525611ec7b19a242dc275bbd093777f25355def` | [35642380942](https://github.com/ArcForges/AI/actions/runs/35642380942) | `ai-0.1.0-ci.44.1` |
| Web | [PR 14](https://github.com/ArcForges/Web/pull/14) | `165278c585c14560667cfb67a50d87907b755b28` | [35642441506](https://github.com/ArcForges/Web/actions/runs/35642441506) | `web-0.1.0-ci.35.1` |
| Mobile | [PR 9](https://github.com/ArcForges/Mobile/pull/9) | `56f815a80dc960a6e03c370891735d55b6a7cc24` | [35643331581](https://github.com/ArcForges/Mobile/actions/runs/35643331581) | `android-0.1.0-ci.28.1` |

Mobile publication used its permanent signing identity for the release APK/AAB; it did not submit a store release. Contracts uploaded four Maven SNAPSHOT modules in 1 minute 8 seconds, without formal-release validation or public-byte polling.

No external prerequisite was unavailable for this substep. Optional runtime/macOS coverage was not executed or reported as passed. Existing product/commercial go-live obligations and later version-axis producers remain outside this closure. WP02.04 is complete under the amended execution policy; WP02.05 was not started.
