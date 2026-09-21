# WP02.01 diagnostic posture implementation evidence

Scope: [WP02.01](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.01), under the [reviewed diagnostic profile and ordered plan](wp02-01-diagnostic-profile.md). [Design PR47](https://github.com/ArcForges/ArcForges-Design/pull/47) merged before dependent implementation. This receipt closes diagnostic posture only; the AOT declaration sweep and the remaining WP02 obligations retain their separate gates.

## Accepted result

All eight implementation PRs received complete diff review and merged after every applicable PR check passed. Their main publication and real runtime checks passed. Primary checkouts match remote main, and branches/worktrees are retained. The [machine-readable receipt](wp02-01-implementation-evidence.json) records exact source/file hashes, all 43 evaluated managed projects, 17 warning-rejection cases, local logs, PR/main checks and public/runtime identities.

| Owner | Reviewed PR | Merged commit | Main run |
|---|---|---|---|
| DesktopPlatform | [56](https://github.com/ArcForges/DesktopPlatform/pull/56) | `b1c6d18467ec8b6b3b12d4b42018a1c991098292` | [35577992705](https://github.com/ArcForges/DesktopPlatform/actions/runs/35577992705) |
| Contracts | [29](https://github.com/ArcForges/Contracts/pull/29) | `2ad370e9c6e503c9491fc82485fa34bce53ecefa` | [35578998388](https://github.com/ArcForges/Contracts/actions/runs/35578998388) |
| ArcNotes | [6](https://github.com/ArcForges/ArcNotes/pull/6) | `885289e54e123bb1e2fa7ae2884f35306863c35a` | [35579012604](https://github.com/ArcForges/ArcNotes/actions/runs/35579012604) |
| ArcScope | [6](https://github.com/ArcForges/ArcScope/pull/6) | `cacab2a0305064018de505e704267ba8936cc5a4` | [35579025945](https://github.com/ArcForges/ArcScope/actions/runs/35579025945) |
| ArcSlate | [6](https://github.com/ArcForges/ArcSlate/pull/6) | `48abba0ce7a7cb83b35a0c6e20e0df1fb1af5e5e` | [35579040862](https://github.com/ArcForges/ArcSlate/actions/runs/35579040862) |
| Cloud | [7](https://github.com/ArcForges/Cloud/pull/7) | `8942437a5e42c01ae7595b64a220efd60f33b4f0` | [35579055371](https://github.com/ArcForges/Cloud/actions/runs/35579055371) |
| AI | [16](https://github.com/ArcForges/AI/pull/16) | `48837287694b825f727448430fccab72e172ed3c` | [35579070273](https://github.com/ArcForges/AI/actions/runs/35579070273) |
| Mobile | [8](https://github.com/ArcForges/Mobile/pull/8) | `9d0ca5b13ac45cf762de7441ed654fa6af85f7cc` | [35579086244](https://github.com/ArcForges/Mobile/actions/runs/35579086244) |

Web remains at `84939ca1fde0f0653d2cb4d8b8f9e5dd1057abb5`; current npm checks and 18 Chromium/Firefox/WebKit production-browser tests passed. No empty Web PR was created.

## Policy and waivers

All 43 managed projects evaluate nullable references and implicit usings enabled, deterministic compilation, compiler/analyzer warnings-as-errors and build-time code-style enforcement. DesktopPlatform retains `latest-all`; the other five managed roots explicitly retain `latest`. Each managed `.editorconfig` makes `IDE0161` an error. Full solutions built with zero warnings/errors. Existing SDKs, dependencies, targets and generated bindings remain unchanged.

Contracts' Kotlin producers/isolated consumers and Mobile app/shared compilations now fail warnings; Contracts javac uses `-Werror`. Selected Gradle roots fail deprecations. Two owned Contracts deprecations were repaired: delegated configuration creation and task-time Project access in documentation packaging. AI's ordinary Biome command now fails warnings; Cloud/Web already did. Strict TypeScript checks remain enabled.

**Active authored-code diagnostic debt waivers: none (`[]`).** No owner or expiry entries are needed because no exception is admitted. SDK `NoWarn=1701;1702`, the ILLink default for `IL2121`, generator-emitted pragmas/markers, vendor headers and declaration-library boundaries remain explicitly inventoried in the profile. WP02.02 owns the complete trim/AOT diagnostic sweep; this receipt does not close it.

Contracts, Cloud and Mobile retain their old provenance records and introduce reviewed successors for changed build inputs. Complete semantic comparisons preserve documentation golden outputs, resource hashes, dependency closures and legal expectations. Contracts' existing access-policy inventory also updates the three changed build-input hashes without changing package assignments. Mobile's active documentation now names its already selected Contracts `ci.60.1` dependency.

## Verification

The six managed owners rejected real compiler warnings (`CS1030`) and the declared namespace violation (`IDE0161`) through ordinary builds. Contracts rejected Kotlin/Java deprecated-call warnings; Mobile rejected them in both shared and app compilations; AI rejected an unused-variable warning through `npm run lint`. All 17 intended diagnostic cases were verified, temporary mutations restored and affected builds/lint rerun successfully. An initial unclassified Mobile fixture failed provenance before compilation and is not counted as compiler evidence.

Local verification includes full managed builds/format/source checks, 89 tests in each desktop product, DesktopPlatform engineering/architecture/native ABI checks, 92 Contracts tooling tests plus immutable package consumers, Mobile's 49 tooling tests/unit tests/release lint/APK/AAB/resource checks, Cloud's real Linux Native AOT Docker/protocol checks, AI's complete checks and explicitly mocked local bundle test, and Web's browser checks. Hosted CI supplies the full native/device/provider gates. The existing vcpkg installation and dependency tree compiled successfully with `VcpkgManifestInstall=false`; no vcpkg reinstall or dependency rebuild occurred.

- **DesktopPlatform `1.0.0-ci.19.1`:** all ten public NuGet packages match every original candidate ZIP member, allowing only the registry-added signature. Five isolated JIT/AOT cases, C17 and four loader rejection cases passed on the exact main candidate.
- **Contracts `1.0.0-ci.69.1`:** public NuGet members, both npm tarballs and all twenty Maven files match the candidate. Maven is `1.0.0-SNAPSHOT`, timestamp `20260921.084730-3`; no formal tag was created. An independent merged-candidate consumer restored Kotlin from the live Snapshot repository and passed C#, TS, Kotlin gRPC/Connect and Native AOT success/error calls. NuGet/npm in that consumer use verified candidate archives; their public availability is proved separately by byte comparison.
- **ArcNotes/ArcScope/ArcSlate `0.1.0-ci.12.1`:** all fifteen public five-RID archives match candidate receipts, with real native UI/Cloud/failure-path checks. Receipts preserve the Cloud revision actually observed.
- **Cloud `0.1.0-ci.22.1`:** the deployed Native AOT image and Worker passed actual public binary gRPC-Web/Kotlin protocol checks against the merged revision.
- **AI `0.1.0-ci.34.1`:** the deployed Workflow made two actual Workers AI calls to `@cf/openai/gpt-oss-20b` and executed `say_hello`.
- **Mobile `0.1.0-ci.19.1`, code `1901`:** API 26 and 36 verified the actual public signed artifacts, upgraded baseline code `901` with the same certificate, UID and first-install time, and called real Cloud from the minified APK.

Initial NuGet downloads returned 404 during registry synchronization; final complete comparisons passed without republishing. A local Cloud Java PATH setup failure was corrected before successful real container verification. Failed attempts are retained separately from accepted results. No external prerequisite remains unavailable for WP02.01. These foundation probes do not establish later business workflows, production/store promotion or complete commercial readiness.
