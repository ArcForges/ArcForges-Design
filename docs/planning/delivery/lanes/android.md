# Android companion — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Kotlin/Compose foundation, the Android ArcScope companion (workspace, assistant, approvals) and Android release gates.

Tasks: 28 · Owning repositories: Mobile · Integration owner(s): Mobile integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [AND.01](#task-and-01) | Android production identity and .NET MAUI toolchain pins | producer | M | none | not-started |
| [AND.02](#task-and-02) | Real MAUI module graph and AN01-AN28 route/state contracts | producer | L | [AND.01](#task-and-01) (artifact), [AND.40](#task-and-40) (artifact), [PRF.12](runtime-proofs.md#task-prf-12) (artifact) | not-started |
| [AND.03](#task-and-03) | Android runtime and OS adapters (MAUI, Credential Manager, Keystore wrapper, WorkManager, FCM registration, SAF/MediaStore) | feature | L | [AND.02](#task-and-02) (artifact) | not-started |
| [AND.04](#task-and-04) | Published gRPC-Web contract consumption (Grpc.Net.Client.Web C# client from the NuGet Contracts packages, binary framing, session/stream/retry adapters) | feature | M | [AND.02](#task-and-02) (artifact), [CON.07](contracts.md#task-con-07) (contract), [CON.11](contracts.md#task-con-11) (contract), [AND.01](#task-and-01) (artifact), [AND.40](#task-and-40) (artifact) | not-started |
| [AND.05](#task-and-05) | SQLite history, drafts, outbox and receipts (versioned migrations through an admitted Apache-2.0 SQLite binding) | feature | L | [AND.02](#task-and-02) (artifact), [CON.11](contracts.md#task-con-11) (contract) | not-started |
| [AND.06](#task-and-06) | Secure per-account lifecycle: Keystore encryption, no-backup policy, purge/quarantine, deep-link validation | feature | M | [AND.03](#task-and-03) (artifact) | not-started |
| [AND.07](#task-and-07) | Foundation integration evidence: real candidate against deployed 22/23/24/25 | integration | M | [AND.03](#task-and-03) (artifact), [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact), [AND.06](#task-and-06) (artifact), [CLOUD.13](cloud.md#task-cloud-13) (artifact), [CLOUD.42](cloud.md#task-cloud-42) (artifact), [CLOUD.39](cloud.md#task-cloud-39) (artifact), [CLOUD.19](cloud.md#task-cloud-19) (artifact), [CLOUD.26](cloud.md#task-cloud-26) (artifact), [CLOUD.29](cloud.md#task-cloud-29) (artifact) | not-started |
| [AND.08](#task-and-08) | Authentication, Home and workspace (AN01-AN06) | feature | L | [AND.03](#task-and-03) (artifact), [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact), [AND.06](#task-and-06) (artifact) | not-started |
| [AND.09](#task-and-09) | Conversations and context (AN07-AN10/15/16) | feature | L | [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact) | not-started |
| [AND.10](#task-and-10) | Tasks, approvals and automation (AN11-AN13/19/25) | feature | L | [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact) | not-started |
| [AND.11](#task-and-11) | Library and resources (AN14-AN18/22) | feature | M | [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact) | not-started |
| [AND.12](#task-and-12) | Presence, push, links and settings (AN20-AN24) | feature | M | [CON.22](contracts.md#task-con-22) (contract), [AND.03](#task-and-03) (artifact), [AND.04](#task-and-04) (artifact), [AND.06](#task-and-06) (artifact) | not-started |
| [AND.13](#task-and-13) | Native interaction and recovery: full experience-02 device matrix | integration | L | [AND.08](#task-and-08) (artifact), [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact), [AND.11](#task-and-11) (artifact), [AND.12](#task-and-12) (artifact) | not-started |
| [AND.14](#task-and-14) | Scope and licence enforcement audit | acceptance | S | [AND.08](#task-and-08) (artifact), [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact) | not-started |
| [AND.15](#task-and-15) | Complete companion acceptance | integration | M | [AND.08](#task-and-08) (artifact), [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact), [AND.11](#task-and-11) (artifact), [AND.12](#task-and-12) (artifact), [AND.13](#task-and-13) (artifact), [AND.14](#task-and-14) (artifact), [AND.27](#task-and-27) (artifact) | not-started |
| [AND.16](#task-and-16) | Signed Android release artifacts (direct APK) | release | S | [AND.15](#task-and-15) (artifact) | not-started |
| [AND.17](#task-and-17) | Release runtime inspection | acceptance | S | [AND.16](#task-and-16) (artifact) | not-started |
| [AND.18](#task-and-18) | Dependency and source rights closure (final artifact) | acceptance | S | [AND.16](#task-and-16) (artifact) | not-started |
| [AND.19](#task-and-19) | Consumption-only enforcement | acceptance | M | [AND.08](#task-and-08) (artifact), [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact), [AND.11](#task-and-11) (artifact), [AND.12](#task-and-12) (artifact) | not-started |
| [AND.20](#task-and-20) | Direct-channel signed update client | feature | M | [CON.16](contracts.md#task-con-16) (contract), [AND.02](#task-and-02) (artifact) | not-started |
| [AND.21](#task-and-21) | Physical device and recovery gates | integration | L | [AND.16](#task-and-16) (artifact) | not-started |
| [AND.22](#task-and-22) | Android scope statement | acceptance | S | [AND.01](#task-and-01) (artifact) | not-started |
| [AND.23](#task-and-23) | Distribution acceptance | release | M | [AND.17](#task-and-17) (artifact), [AND.18](#task-and-18) (artifact), [AND.19](#task-and-19) (artifact), [AND.20](#task-and-20) (artifact), [AND.21](#task-and-21) (artifact), [AND.22](#task-and-22) (artifact) | not-started |
| [AND.24](#task-and-24) | Real CF Harness generation/tool loop observed end to end on Android | integration | M | [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact), [HAR.00](harness.md#task-har-00) (artifact), [HAR.03](harness.md#task-har-03) (artifact) | not-started |
| [AND.25](#task-and-25) | Real desktop tool dispatch and unknown-effect reconciliation from Android | integration | M | [AND.10](#task-and-10) (artifact), [AND.13](#task-and-13) (artifact), [DEV.02](device-bridge.md#task-dev-02) (artifact), [DEV.03](device-bridge.md#task-dev-03) (artifact), [DEV.06](device-bridge.md#task-dev-06) (artifact), [DEV.07](device-bridge.md#task-dev-07) (artifact), [DEV.12](device-bridge.md#task-dev-12) (artifact) | not-started |
| [AND.26](#task-and-26) | Real FCM sending and physical Android receipt | integration | M | [AND.12](#task-and-12) (artifact), [AND.23](#task-and-23) (artifact), [OPS.10](operations.md#task-ops-10) (artifact), [AND.21](#task-and-21) (artifact) | not-started |
| [AND.27](#task-and-27) | ArcScope library, reports and simulation runs on Android | feature | L | [AND.11](#task-and-11) (artifact), [CON.24](contracts.md#task-con-24) (contract), [CON.21](contracts.md#task-con-21) (contract) | not-started |
| [AND.40](#task-and-40) | MAUI migration of the existing Mobile app: Hello client, streaming consumer rules, Keystore probe, CI, signing and C# policy (Kotlin, KMP and Gradle retired) | producer | L | [AND.01](#task-and-01) (artifact) | not-started |

## Tasks

<a id="task-and-01"></a>

### AND.01 — Android production identity and .NET MAUI toolchain pins

**Outcome.** com.arcforges.mobile applicationId, namespace and source packages adopted, with reinstall guidance from the development prerelease io.github.arcforges.mobile recorded in docs/releasing.md (reinstall with no data migration; the prerelease holds no production user data); the persistent android-release signing identity is kept (cert SHA256 7a8b3b14...); and a mutually compatible .NET 10 LTS SDK, Android workload, MAUI and NuGet tuple is pinned as candidate pins with global.json, central package versions (Directory.Packages.props), packages.lock.json locks, SDK and workload integrity pins and dependency-admission records, plus generated-client compatibility evidence (the NuGet Contracts client restores and builds against the candidate tuple). Every shipped Mobile project targets net10.0-android only (P2-021.3), with UseMonoRuntime=true set explicitly; host-run test, policy and architecture-test projects (executed by the .NET test host on a Windows or Linux machine, never on an Android device or emulator) target net10.0 so that they run on hosted Windows and Linux runners without an emulator ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)), Android device test projects (AND.13) target net10.0-android, and platform-neutral libraries may add net10.0 as a second target used only by the host-run tests; platform-neutral domain and feature projects (AND.02) contain no Android or platform API references, and their shipped target is net10.0-android. The exact tuple is not proven by this task: the first release-build proof is AND.40's CI gate, and PRF.12 proves the tuple on the device before this task completes.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-01` and ledger record `ledger/tasks/and-01.md` in the Plan repository; task branch `task/and-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M · early risk proof |
| Obligations | [WP-30.00](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.00) — all work except the parts mapped to AND.04<br>[WP-30](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30) §3 binding rules: Apache-2.0 boundary, no GPL-family implementation, immutable producer artifacts — package-level obligation contribution |
| Provides | android-app-identity; android-stable-toolchain |
| Start prerequisites | none |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [PRF.12](runtime-proofs.md#task-prf-12) — the MAUI Android release proof recording the exact compatible .NET 10 / Android workload / NuGet tuple. *Why:* AND.01 is delivered on candidate pins, so AND.40 starts on that candidate tuple. The completion edge keeps AND.01 open until the MAUI Android release proof of the exact tuple exists. A start gate on PRF.12 would be a cycle, because PRF.12 starts on AND.40, which starts on this task; so the first release-build proof is AND.40's own CI gate (net10.0-android Release build with Mono AOT and R8). A failed proof or any later pin change reopens AND.01, AND.40 and PRF.12. The former start edge on PRF.10 is removed because PRF.10 is superseded (retargeting it to PRF.12 would be a cycle). |
| Unblocks | [AND.02](#task-and-02), [AND.04](#task-and-04), [AND.22](#task-and-22), [AND.40](#task-and-40) |
| Write scope | `Mobile:global.json`<br>`Mobile:Directory.Build.props`<br>`Mobile:Directory.Packages.props`<br>`Mobile:NuGet.config`<br>`Mobile:eng/policy/**`<br>`Mobile:eng/provenance/**`<br>`Mobile:eng/build_identity.py`<br>`Mobile:eng/version-sources.json`<br>`Mobile:src/ArcForges.Mobile/** (the identity-only project: its csproj, packages.lock.json, the Android manifest with no permission and no launchable activity, and only the compile-only sources the identity build and the generated-client compatibility evidence need; no runtime behaviour, because AND.40 owns the app)`<br>`Mobile:docs/releasing.md (the reinstall guidance from io.github.arcforges.mobile only)`<br>`Mobile:docs/maui-toolchain.md (new: the pinned tuple, the integrity pins and the identity-build evidence)`<br>`Mobile:docs/licence-boundary.md (the Contracts NuGet admission entry and the MAUI-closure licence notes only)`<br>`Mobile:eng/maui_identity.py (new identity, tuple and admission gate) and Mobile:eng/tests/test_maui_identity.py (its offline tests)`<br>`Mobile:eng/mobile.py (wire the identity gate, and the exact-path final-newline exemption of the identity project lock, only)`<br>`Mobile:eng/licences.py (extend the existing licence audit to the identity project csproj only)`<br>`Mobile:.gitignore (bin/ and obj/ of the identity project only)` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Windows full build of the identity-only project with locked restore (packages.lock.json content hashes), NuGet audit and dependency-verification check, and the same Linux full build in the hosted Linux CI job that AND.40 adds ([P2-024](../../../decisions/phase-2-specification-decisions.md#rule-p2-024) limitation: the local WSL2 Debian distribution has no JDK or Android SDK and installing them needs the user; owner AND.40, trigger its Linux CI job; AND.01 is not complete before that Linux build passes); F-023-class licence and provenance closure re-run for the pinned MAUI closure; package-identity and certificate inspection of the built manifest under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). The MAUI app release build and its Mono AOT, trimming, R8 and 16 KB checks are an explicit transfer to AND.40 (CI) and PRF.12 (candidate proof), so the Windows and Linux build acceptance is not narrowed here; device install and App Link fixture-key tests are local opt-in, not CI gates. |
| Completion evidence | Exact pinned tuple in global.json, Directory.Packages.props and packages.lock.json; SDK and workload integrity pins (exact SDK version with rollForward pinned, exact workload manifest versions, packages.lock.json content hashes in place of the former Gradle wrapper checksum); admission records for each new NuGet or workload dependency; built manifest showing applicationId com.arcforges.mobile; reinstall guidance recorded in docs/releasing.md; [F-023](../../../assurance/open-gates-register.md#rule-f-023) re-run showing the closure holds for the MAUI dependency set (the android-0.1.0-ci.14.1 closure does not carry over and reopens on this dependency change); no AGPL DesktopPlatform package in the closure; the hosted Linux CI run (run identifier) of the identity-only build that AND.40 adds, which closes the [P2-024](../../../decisions/phase-2-specification-decisions.md#rule-p2-024) deferral. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: app/ is a Hello World module with applicationId io.github.arcforges.mobile (dev-prerelease id); shared/ is a Kotlin-Multiplatform module (android+desktop jvm targets) used only for a Compose Hot Reload preview per AGENTS.md, not a production target; CI already builds/signs/publishes real signed candidates (android-0.1.0-ci.14.1, [F-023](../../../assurance/open-gates-register.md#rule-f-023) closed for that candidate) which is de facto WP06 evidence |
| Notes | Must also decide the KMP shared/ preview module's fate: arch-27's module map (core/*, feature/*) has no KMP target, so shared/ stays a dev-only convenience outside the shipped app graph, never a second production plan (per WP30 §4). Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Kotlin/AGP/Compose/Gradle tuple replaced by the .NET 10 LTS SDK, Android workload and NuGet candidate pins (P2-021.3); applicationId decision taken from P2-021.3 and [IRD-23](../../../decisions/phase-2-specification-decisions.md#rule-ird-23) (com.arcforges.mobile, reinstall from io.github.arcforges.mobile documented in docs/releasing.md with no data migration). Source packages are adopted as well as applicationId and namespace. Identity-only Windows and Linux build acceptance restored; the MAUI release-build proof transfers explicitly to AND.40 (CI) and PRF.12 (device proof). Start edge on the superseded PRF.10 removed; the exact-tuple proof is a completion edge on PRF.12, not a start gate. Dropped on purpose: the optional development preview in the KMP shared/ module (desktopMain, labelled development-only; AGENTS.md:3) retires with the Kotlin/KMP modules under AND.40, with no replacement preview; the development-only status is restated in AND.22. No acceptance removed. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); coordinator adjudication, brief section 10): the write scope is completed with the paths the outcome already requires (docs/releasing.md for the reinstall guidance; the identity-only project sources, manifest and lock; the identity gate and its tests; the toolchain and licence documentation; the bin/obj ignore). The identity project carries no runtime behaviour: no permission, no launchable activity, only compile-only sources. First-party Contracts packages are admitted only from a candidate published from a commit on the current Contracts main (Contracts main 330e46bd, which the 2026-10-07 baseline rollback kept, published 1.0.0-ci.324.1 on 2026-10-05); 1.0.0-ci.350.1 was published from rolled-back commit 74c298c9 and is not admitted. No obligation or acceptance changes. Planning repair 2026-10-09 ([DLV-34](../README.md#rule-dlv-34); coordinator adjudication, brief section 10 AND.40 decisions): the single-target wording is scoped to the shipped projects (host test targets). Planning repair 2026-10-09 ([DLV-34](../README.md#rule-dlv-34); fix4 review follow-up, non-blocking items): "host-run" is defined in place; no acceptance or evidence changes. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: the Gradle 9.8.1, Kotlin 2.4.21 and Spotless 8.10.4 admissions, the Gradle wrapper, gradle/libs.versions.toml, gradle/locks, verification metadata, the JDK 21 pin and the Kotlin lint gates are out of scope, not completed; completion cites only the .NET identity build and the PRF.12 tuple proof. |

<a id="task-and-02"></a>

### AND.02 — Real MAUI module graph and AN01-AN28 route/state contracts

**Outcome.** The arch-27 module set (app, core/domain, core/data, core/network, core/security, core/designsystem, feature/home, feature/chat, feature/tasks, feature/library, feature/scope, feature/settings) exists as enforced .NET projects, each shipped project targeting net10.0-android only (P2-021.3), the app being the MAUI project; host-run test, policy and architecture-test projects (executed by the .NET test host on a Windows or Linux machine, never on an Android device or emulator) target net10.0 so that they run on hosted Windows and Linux runners without an emulator ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)), Android device test projects (AND.13) target net10.0-android, and platform-neutral libraries may add net10.0 as a second target used only by the host-run tests; the domain and feature projects are platform-neutral in code (no Android or platform API reference, enforced by architecture tests) and ship with net10.0-android as their target. Typed AN01-AN28 Shell/navigation and state contracts exist, and features depend only on typed core ports. No iOS, Mac Catalyst, macOS or other platform target exists.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-02` and ledger record `ledger/tasks/and-02.md` in the Plan repository; task branch `task/and-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-30.01](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.01) — full |
| Provides | android-module-boundaries; android-nav-contracts |
| Start prerequisites | **artifact** [AND.01](#task-and-01) — renamed applicationId/namespace and pinned toolchain. *Why:* new modules must be created under the production package identity, not the Hello dev id<br>**artifact** [AND.40](#task-and-40) — the MAUI app project, Hello transport and CI created by AND.40. *Why:* the module projects are created inside the MAUI app solution and the Kotlin module graph retires in AND.40<br>**artifact** [PRF.12](runtime-proofs.md#task-prf-12) — the MAUI Android release proof of the candidate app, Hello transport and release pipeline on the device or emulator. *Why:* the MAUI proof is an early risk proof that precedes the bulk Android module and feature work; PRF.12 starts only on AND.40 and PRF.07, neither of which starts on AND.02, so the edge is acyclic |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.03](#task-and-03), [AND.04](#task-and-04), [AND.05](#task-and-05), [AND.20](#task-and-20) |
| Write scope | `Mobile:src/ArcForges.Mobile/**`<br>`Mobile:src/core/ArcForges.Mobile.Domain/**`<br>`Mobile:src/core/ArcForges.Mobile.Data/**`<br>`Mobile:src/core/ArcForges.Mobile.Network/**`<br>`Mobile:src/core/ArcForges.Mobile.Security/**`<br>`Mobile:src/core/ArcForges.Mobile.DesignSystem/**`<br>`Mobile:src/features/ArcForges.Mobile.Home/**`<br>`Mobile:src/features/ArcForges.Mobile.Chat/**`<br>`Mobile:src/features/ArcForges.Mobile.Tasks/**`<br>`Mobile:src/features/ArcForges.Mobile.Library/**`<br>`Mobile:src/features/ArcForges.Mobile.Scope/**`<br>`Mobile:src/features/ArcForges.Mobile.Settings/**`<br>`Mobile:ArcForges.Mobile.slnx`<br>`Mobile:tests/ArcForges.Mobile.Tests/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (exclusive) |
| Validation | Architecture and import-boundary tests (no React Native, iOS, macOS or AGPL package references, no cross-module leakage, one-way core<-feature<-app) as offline xUnit architecture tests run in CI; targeted offline unit tests per project. |
| Completion evidence | Project reference graph report showing one-way core<-feature<-app dependencies; route ID inventory matching AN01-AN28; zero iOS or macOS target frameworks. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Only app/ and the KMP shared/ preview module exist today; none of the arch-27 core/* or feature/* modules exist |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): arch-27 Gradle module set becomes .NET project set with the same one-way rule; KMP shared/ dev module retires with AND.40. Acceptance unchanged. Planning repair 2026-10-09 ([DLV-34](../README.md#rule-dlv-34); coordinator adjudication, brief section 10 AND.40 decisions): the single-target wording is scoped to the shipped projects (host test targets). Planning repair 2026-10-09 ([DLV-34](../README.md#rule-dlv-34); fix4 review follow-up, non-blocking items): "host-run" is defined in place; no acceptance changes. |

<a id="task-and-03"></a>

### AND.03 — Android runtime and OS adapters (MAUI, Credential Manager, Keystore wrapper, WorkManager, FCM registration, SAF/MediaStore)

**Outcome.** arm64 release and x64 emulator adapters for Credential Manager/passkey fallback, Keystore, WorkManager, FCM with non-GMS fallback, and SAF/MediaStore/FileProvider exist in ArcForges.Mobile.Security, ArcForges.Mobile.Data and ArcForges.Mobile.Network, bound through admitted .NET for Android (AndroidX and Google/OS) bindings, with no unsafe fallback path.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-03` and ledger record `ledger/tasks/and-03.md` in the Plan repository; task branch `task/and-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-30.02](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.02) — full |
| Provides | android-os-adapters; android-keystore-wrapper; android-workmanager |
| Start prerequisites | **artifact** [AND.02](#task-and-02) — core/security, core/data, core/network module shells. *Why:* adapters live inside these modules; cannot be written before the module boundary exists |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.06](#task-and-06), [AND.07](#task-and-07), [AND.08](#task-and-08), [AND.12](#task-and-12) |
| Write scope | `Mobile:src/core/ArcForges.Mobile.Security/**`<br>`Mobile:src/core/ArcForges.Mobile.Data/**`<br>`Mobile:src/core/ArcForges.Mobile.Network/**`<br>`Mobile:tests/ArcForges.Mobile.Tests/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Targeted offline xUnit tests for adapter contracts in CI; install-on-real-device, permission-refusal, process-death and missing-Play-services scenarios are local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), not CI. |
| Completion evidence | Adapter test matrix (permission refusal, process death, missing Play services, callback after account switch) with device identity recorded for local runs |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No Credential Manager/Keystore/WorkManager/FCM/SAF integration exists yet; only plain OkHttp networking in the Hello probe |
| Notes | Can proceed in parallel with AND.04 (core/network gRPC client) and AND.05 (Room, core/data) once AND.02's skeleton lands; they touch different files within shared modules so should be sequenced as short-lived parallel PRs, not serialized. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Compose and Kotlin references replaced by MAUI and .NET Android bindings (admitted per binding); paths moved to the C# projects; the xUnit adapter tests land in tests/ArcForges.Mobile.Tests, which is added to writes. Acceptance unchanged. |

<a id="task-and-04"></a>

### AND.04 — Published gRPC-Web contract consumption (Grpc.Net.Client.Web C# client from the NuGet Contracts packages, binary framing, session/stream/retry adapters)

**Outcome.** ArcForges.Mobile.Network wraps the NuGet Contracts client surface behind typed session/stream/retry/exact-value adapters, explicitly selecting binary gRPC-Web through Grpc.Net.Client.Web; the observed GrpcWebMode and server-stream media type are recorded by PRF.12 together with the fallback decision. Exact values stay exact: int64 and uint64 use C# long and ulong, decimal values use decimal, and no value passes through floating point.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-04` and ledger record `ledger/tasks/and-04.md` in the Plan repository; task branch `task/and-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-30.03](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.03) — full contract consumption through the NuGet Grpc.Net.Client.Web client (Connect-Kotlin client retired)<br>[WP-30.00](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.00) — MAUI real package consumption of the NuGet Contracts clients |
| Provides | android-grpc-web-client |
| Start prerequisites | **artifact** [AND.02](#task-and-02) — core/network module shell. *Why:* client wiring lives in this module<br>**contract** [CON.07](contracts.md#task-con-07) — the NuGet Contracts packages (ArcForges.Contracts.PublicApi and the Contracts generated C# client surface) for identity, session and native-auth types. *Why:* the Maven coordinates are retired under P2-021.4; the consumed C# client surface is the NuGet package<br>**contract** [CON.11](contracts.md#task-con-11) — the generated C# ApplicationService, HistoryService and EventService clients in the NuGet Contracts packages. *Why:* the Android contract layer consumes these operations through the NuGet client, not the retired Kotlin Connect clients<br>**artifact** [AND.01](#task-and-01) — delivered AND.01 identity and candidate .NET MAUI toolchain pins (the exact tuple is proven by PRF.12 before AND.01 completes). *Why:* this integration exercises the real identity and pinned MAUI toolchain instead of a substitute<br>**artifact** [AND.40](#task-and-40) — the MAUI Hello transport and streaming consumer rules built by AND.40. *Why:* the generalised session/stream/retry adapters extend the transport that AND.40 proves first |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.21](cloud.md#task-cloud-21) — publicly deployed Cloud host serving the generated business RPC surface. *Why:* the completion gate requires real packaged-Maven-consumer-and-service/device evidence, i.e. a live endpoint; the client code itself only needs the published Maven package to be written and unit-tested |
| Unblocks | [AND.07](#task-and-07), [AND.08](#task-and-08), [AND.09](#task-and-09), [AND.10](#task-and-10), [AND.11](#task-and-11), [AND.12](#task-and-12) |
| Write scope | `Mobile:src/core/ArcForges.Mobile.Network/**`<br>`Mobile:tests/ArcForges.Mobile.Tests/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Targeted offline xUnit codec and adapter tests in CI (binary framing, exact int64/uint64/decimal values, grpc-timeout header format, no cookies, no redirects, no connection retry); real device or service calls against a deployed Cloud host are local opt-in evidence, not a CI gate (same pattern as the MAUI Hello client built by AND.40). |
| Completion evidence | Real NuGet-package consumer and service/device call evidence with exact package versions, hashes and device identity. |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: CloudHelloClient.kt already demonstrates this exact pattern (ProtocolClient, GRPC_WEB, OkHttp transport, error-code mapping) for the single Hello RPC; needs generalizing to the full session/stream/retry surface |
| Notes | Merged duplicate integration or closure task formerly proposed as CON.97. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Connect-Kotlin client replaced by Grpc.Net.Client.Web (C#, binary gRPC-Web selected explicitly). Maven edges replaced by NuGet Contracts edges. Open items on the NuGet streaming methods are recorded in PRF.12. Acceptance unchanged; exact-value rule stated explicitly. |

<a id="task-and-05"></a>

### AND.05 — SQLite history, drafts, outbox and receipts (versioned migrations through an admitted Apache-2.0 SQLite binding)

**Outcome.** SQLite schemas (local_schema, scope_partition, projection, draft, outbox, transfer, cursor, preferences), versioned with forward-only SQLite migrations through an admitted Apache-2.0 .NET SQLite binding, implement per-profile partitions with a durable, bounded, never-silently-evicted outbox; local canonical history is not evictable cache.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-05` and ledger record `ledger/tasks/and-05.md` in the Plan repository; task branch `task/and-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-30.04](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.04) — full |
| Provides | android-room-store; android-outbox |
| Start prerequisites | **artifact** [AND.02](#task-and-02) — core/data module shell. *Why:* Room lives in this module<br>**contract** [CON.11](contracts.md#task-con-11) — model-05-equivalent typed records for projections/receipts. *Why:* table shapes mirror the published wire records |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.07](#task-and-07), [AND.08](#task-and-08), [AND.09](#task-and-09), [AND.10](#task-and-10), [AND.11](#task-and-11) |
| Write scope | `Mobile:src/core/ArcForges.Mobile.Data/**`<br>`Mobile:tests/ArcForges.Mobile.Tests/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Offline SQLite migration tests in CI: every schema version migrates forward; crash-recovery, capacity-refusal and atomic outbox writes run against a file-backed database; the SQLite binding is admitted under dependency admission with its licence and native-library provenance closure (Apache-2.0 required by P2-021.3). Instrumented runs on the emulator or a device are local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Migration test results for every schema version; outbox capacity-refusal and awaitingReconciliation replay tests; no silent eviction of draft or outbox rows. |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No Room dependency or schema exists in the repo yet |
| Notes | Fully local; remote Task/AI content reconciled through this store may use named fixtures until WP31/52 per the producer matrix ("Task/AI fixture allowed only until 31+52"), but the store/journal/outbox mechanics themselves must be real now. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Room is replaced by SQLite with versioned migrations (the coordinator translation for the MAUI stack). The binding must be Apache-2.0 under P2-021.3 and is admitted by dependency admission; if no Apache-2.0 SQLite binding is admitted, the AndroidX Room binding is the fallback and needs a coordinator decision (openQuestions). Durability, bounds and no-eviction rules unchanged. |

<a id="task-and-06"></a>

### AND.06 — Secure per-account lifecycle: Keystore encryption, no-backup policy, purge/quarantine, deep-link validation

**Outcome.** Per-account Keystore-encrypted secret and pending-store policy (Android Keystore through the .NET binding), session, logout and revoke purge vs unsent-work quarantine or export, same-generation deep-link validation and current-foreground consent are implemented in ArcForges.Mobile.Security. Reinstall path: the io.github.arcforges.mobile development prerelease (Kotlin-era Keystore data) has no MAUI migration helper and holds no production user data, so the path to com.arcforges.mobile is reinstall guidance in docs/releasing.md with no data migration. Upgrades within com.arcforges.mobile keep the migration, quarantine and retention rules of AND.21, including no pending user work lost.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-06` and ledger record `ledger/tasks/and-06.md` in the Plan repository; task branch `task/and-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-30.05](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.05) — full |
| Provides | android-secure-lifecycle |
| Start prerequisites | **artifact** [AND.03](#task-and-03) — Keystore/Credential Manager adapter wrapper. *Why:* per-account encryption is built on top of the raw OS adapter, not a second implementation of it |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.07](#task-and-07), [AND.08](#task-and-08), [AND.12](#task-and-12) |
| Write scope | `Mobile:src/core/ArcForges.Mobile.Security/**` |
| Validation | Offline unit tests for encryption/purge/quarantine logic; device-restore-without-key, logout-while-requests-run, deep-link-spoof and secret-scan-of-release-logs are local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). The io.github reinstall guidance in docs/releasing.md (no data migration) is checked offline in CI by the AND.40 policy suite. |
| Completion evidence | Secret scan of release logs/backup showing no credential leakage; device restore and logout-while-in-flight scenario results; the docs/releasing.md reinstall-guidance check result for io.github.arcforges.mobile (no data migration). |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Paths moved to ArcForges.Mobile.Security. The io.github reinstall guidance (no data migration; development prerelease, no production user data) is recorded by AND.40 in docs/releasing.md; see the outcome, validation and evidence. Acceptance otherwise unchanged. |

<a id="task-and-07"></a>

### AND.07 — Foundation integration evidence: real candidate against deployed 22/23/24/25

**Outcome.** A candidate APK is built, installed clean and exercises real sign-in/hydration/upload/reconnect on a physical device against actually deployed Cloud identity/API/realtime/sync; any Task/AI fixtures still present are named and confirmed compiled out of production before WP31.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-07` and ledger record `ledger/tasks/and-07.md` in the Plan repository; task branch `task/and-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-30](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-30.90](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.90) — full<br>[WP-23.05](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.05) — Android real-consumer integration beyond the [WP-06](../../work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) probe |
| Provides | android-foundation-candidate |
| Start prerequisites | **artifact** [AND.03](#task-and-03) — OS adapters complete. *Why:* candidate needs full local capability set<br>**artifact** [AND.04](#task-and-04) — gRPC-Web client complete. *Why:* candidate needs real network layer<br>**artifact** [AND.05](#task-and-05) — Room store complete. *Why:* candidate needs real local persistence<br>**artifact** [AND.06](#task-and-06) — secure lifecycle complete. *Why:* candidate needs real session/secret handling<br>**artifact** [CLOUD.13](cloud.md#task-cloud-13) — deployed identity/session service. *Why:* sign-in must be real<br>**artifact** [CLOUD.42](cloud.md#task-cloud-42) — deployed R2/sync/hydration. *Why:* upload/reconnect must be real<br>**artifact** [CLOUD.39](cloud.md#task-cloud-39) — deployed guarded publication and convergent bootstrap. *Why:* the Android foundation integration evidence exercises real hydration and sync against deployed Cloud authority<br>**artifact** [CLOUD.19](cloud.md#task-cloud-19) — real, delivered outcome of CLOUD.19 (Browser cookie-session adapter and full account-surface closure). *Why:* this integration exercises the real browser cookie-session adapter and full account-surface closure instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.26](cloud.md#task-cloud-26) — real, delivered outcome of CLOUD.26 (generated NuGet C# clients against Identity/Workspace/Device). *Why:* this integration exercises the real generated client as a NuGet package, not a substitute; the Kotlin client wording is retired under P2-021.4<br>**artifact** [CLOUD.29](cloud.md#task-cloud-29) — real, delivered outcome of CLOUD.29 (Stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells)). *Why:* this integration exercises the real stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells) instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.08](#task-and-08), [AND.09](#task-and-09), [AND.10](#task-and-10), [AND.11](#task-and-11), [AND.12](#task-and-12), [CLOUD.28](cloud.md#task-cloud-28) |
| Write scope | `Mobile:src/ArcForges.Mobile/**` |
| Validation | Clean-cache restore/build/install on a real device is local opt-in evidence per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017); CI only runs the offline/static portion |
| Completion evidence | Owned-artifact-and-real-integration receipt: source commit, producer versions, candidate hashes, actual device identity, scenario, result, real-vs-fixture status per field |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as CLOUD.60. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Writes moved to the MAUI app project; the Kotlin candidate becomes a MAUI candidate under AND.40. Real-device and fixture-retirement acceptance unchanged. Planning repair fix8 2026-10-10 ([DLV-34](../README.md#rule-dlv-34); coordinator ruling S57(11)): the start edge on CLOUD.18 is removed. CLOUD.18 delivers an AGPL DesktopPlatform package (ArcForges.Security.Sessions) that the Apache-2.0 MAUI app never consumes ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3); the Android native session is AND.06 and AND.08, on which this task already depends through AND.06. The real sign-in against deployed Cloud identity is unchanged and still rests on the CLOUD.13 and CLOUD.19 edges. No acceptance changes. |

<a id="task-and-08"></a>

### AND.08 — Authentication, Home and workspace (AN01-AN06)

**Outcome.** System authentication, five-destination navigation and per-device application selection are complete with real Cloud identity/presence and explicit history disclosure.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-08` and ledger record `ledger/tasks/and-08.md` in the Plan repository; task branch `task/and-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-31.00](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.00) — full |
| Provides | android-auth-home |
| Start prerequisites | **artifact** [AND.03](#task-and-03) — the real Android foundation module AND.03 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap<br>**artifact** [AND.04](#task-and-04) — the real Android foundation module AND.04 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap<br>**artifact** [AND.05](#task-and-05) — the real Android foundation module AND.05 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap<br>**artifact** [AND.06](#task-and-06) — the real Android foundation module AND.06 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AND.07](#task-and-07) — foundation candidate proven against the deployed Cloud services. *Why:* the feature can be built on the foundation modules, but its acceptance runs against the deployed services AND.07 proves and requires any remaining Task/AI fixtures compiled out<br>**integration** [AND.13](#task-and-13) — the UI-level suite (five-destination Shell navigation, back and state restore, UI assertions) in the net10.0-android device test project. *Why:* the suite AND.08 validation relies on is owned by AND.13; completing on it means the UI-level coverage cannot be claimed without the suite existing and running (local opt-in) |
| Unblocks | [AND.13](#task-and-13), [AND.14](#task-and-14), [AND.15](#task-and-15), [AND.19](#task-and-19) |
| Write scope | `Mobile:src/features/ArcForges.Mobile.Home/**`<br>`Mobile:src/ArcForges.Mobile/**`<br>`Mobile:tests/ArcForges.Mobile.Tests/**` |
| Validation | Offline xUnit view-model and Shell navigation tests in CI where feasible; the UI-level suite the instrumented tests covered (five-destination Shell navigation, back and state restore, UI assertions) runs in the net10.0-android device test project owned by AND.13 as local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017); scope/permission, wrong or stale target, loss/retry and expiry scenarios against real WP22/23 are local opt-in. |
| Completion evidence | Full account/attention path walkthrough against real Cloud endpoints |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Does not need WP26 (remote bridge), WP45 (push sender) or WP52 (Harness) to start or complete — only WP30's own foundation and the already-deployed WP22/23. Demonstrates that not all Android features wait on the complete Harness. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Five-destination navigation is MAUI Shell instead of Compose navigation. Instrumented UI tests become offline view-model and Shell navigation tests in tests/ArcForges.Mobile.Tests (added to writes) where feasible, and the UI-level suite moves to the AND.13 net10.0-android device test project. AND.08 completes on AND.13 (typed edge), so no UI-level coverage is removed. Acceptance unchanged. |

<a id="task-and-09"></a>

### AND.09 — Conversations and context (AN07-AN10/15/16)

**Outcome.** Native composer/IME/branch/context, history modes/promotion and real binary output streams work end-to-end for own-application scope, with no desktop local-history access.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-09` and ledger record `ledger/tasks/and-09.md` in the Plan repository; task branch `task/and-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-31.01](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.01) — all work except the parts mapped to AND.24 |
| Provides | android-chat-ui |
| Start prerequisites | **artifact** [AND.04](#task-and-04) — the real Android foundation module AND.04 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap<br>**artifact** [AND.05](#task-and-05) — the real Android foundation module AND.05 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AND.24](#task-and-24) — real CF Harness admission/generation/tool loop. *Why:* the completion gate requires every conversation/project/retrieval row to work with actual WP52 outputs; the streaming/cursor/reconnect UI itself can be fully built and tested against the server-side contract-bound fixture turn endpoint (introduced WP17.01, deleted WP52.05) that already runs in the real deployed Cloud host<br>**integration** [AND.07](#task-and-07) — foundation candidate proven against the deployed Cloud services. *Why:* the feature can be built on the foundation modules, but its acceptance runs against the deployed services AND.07 proves and requires any remaining Task/AI fixtures compiled out<br>**integration** [SRCH.90](search.md#task-srch-90) — the owned search artifacts and index capacity acceptance. *Why:* companion conversation search and [SW-06](../../../requirements/products/arcchat-mobile-and-web.md#rule-sw-06) companion answers run against the owned search facade, so their acceptance needs SRCH.90 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S13) |
| Unblocks | [AND.13](#task-and-13), [AND.14](#task-and-14), [AND.15](#task-and-15), [AND.19](#task-and-19), [AND.24](#task-and-24) |
| Permitted substitutes | [SUB-fixture-turn-endpoint](../substitutes.md#sub-fixture-turn-endpoint) |
| Write scope | `Mobile:src/features/ArcForges.Mobile.Chat/**` |
| Validation | Offline stream-codec/cursor unit tests; real-device streaming/reconnect scenarios against the deployed (fixture-backed until WP52.05) endpoint are local opt-in |
| Completion evidence | History/pending-input/stream/final-message consistency under every declared recovery outcome |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Composer, IME and stream surfaces become MAUI controls on the same stream and cursor semantics; writes moved to the C# feature project. Acceptance unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): added: start edge on SRCH.90 (S13; companion answers and search). |

<a id="task-and-10"></a>

### AND.10 — Tasks, approvals and automation (AN11-AN13/19/25)

**Outcome.** Task/approval/automation surfaces enforce action, risk, credit-consent and consumption-only rules with one real owner outcome/settlement per command.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-10` and ledger record `ledger/tasks/and-10.md` in the Plan repository; task branch `task/and-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-31.02](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.02) — all work except the parts mapped to AND.24, AND.25 |
| Provides | android-tasks-ui |
| Start prerequisites | **artifact** [AND.04](#task-and-04) — the real Android foundation module AND.04 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap<br>**artifact** [AND.05](#task-and-05) — the real Android foundation module AND.05 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AND.25](#task-and-25) — real device bridge with lease/current-grant/unknown-effect reconciliation. *Why:* dispatching an actual tool call to a desktop and observing durable reconciliation needs the real bridge; the task/approval card UI itself only needs the contract shape and can be tested against fixtures<br>**integration** [AND.24](#task-and-24) — real Harness planning/tool-proposal loop. *Why:* approval content must reflect real proposed effects, not scripted ones, to close the gate<br>**integration** [AND.07](#task-and-07) — foundation candidate proven against the deployed Cloud services. *Why:* the feature can be built on the foundation modules, but its acceptance runs against the deployed services AND.07 proves and requires any remaining Task/AI fixtures compiled out |
| Unblocks | [AND.13](#task-and-13), [AND.14](#task-and-14), [AND.15](#task-and-15), [AND.19](#task-and-19), [AND.24](#task-and-24), [AND.25](#task-and-25) |
| Permitted substitutes | [SUB-automation-fixture](../substitutes.md#sub-automation-fixture) |
| Write scope | `Mobile:src/features/ArcForges.Mobile.Tasks/**` |
| Validation | Offline idempotency/state-machine unit tests; real bridge/Harness/commerce scenarios are local opt-in against deployed services |
| Completion evidence | One real owner outcome/settlement per command; no broad implicit grant or hidden background write |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Task, approval and automation UI port to MAUI; idempotency state machine unchanged. Writes moved to the C# feature project. Acceptance unchanged. |

<a id="task-and-11"></a>

### AND.11 — Library and resources (AN14-AN18/22)

**Outcome.** Native preview/import/export/transfer flows handle missing/denied/unsupported states with correct local/cloud copy and deletion semantics.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-11` and ledger record `ledger/tasks/and-11.md` in the Plan repository; task branch `task/and-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-31.03](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.03) — full |
| Provides | android-library-ui |
| Start prerequisites | **artifact** [AND.04](#task-and-04) — the real Android foundation module AND.04 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap<br>**artifact** [AND.05](#task-and-05) — the real Android foundation module AND.05 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AND.07](#task-and-07) — foundation candidate proven against the deployed Cloud services. *Why:* the feature can be built on the foundation modules, but its acceptance runs against the deployed services AND.07 proves and requires any remaining Task/AI fixtures compiled out |
| Unblocks | [AND.13](#task-and-13), [AND.15](#task-and-15), [AND.19](#task-and-19), [AND.27](#task-and-27) |
| Write scope | `Mobile:src/features/ArcForges.Mobile.Library/**` |
| Validation | Offline transfer-journal unit tests; resumable-upload/hash-mismatch/process-death-during-transfer scenarios are local opt-in on real devices |
| Completion evidence | No unavailable bytes represented as empty success; resumable journal survives process death |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Independent of WP26/WP45/WP52 — can complete in parallel with AND.09/AND.10 once the foundation (AND.07) lands. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Library preview, import, export and transfer flows port to MAUI with SAF/MediaStore equivalents. Writes moved to the C# feature project. Acceptance unchanged. |

<a id="task-and-12"></a>

### AND.12 — Presence, push, links and settings (AN20-AN24)

**Outcome.** Presence/push/deep-link/settings surfaces stay usable through declared polling/notification fallback, with no purchase/store billing surface and no exposure of a revoked resource on background reconnect.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-12` and ledger record `ledger/tasks/and-12.md` in the Plan repository; task branch `task/and-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-31.04](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.04) — all work except the parts mapped to AND.26<br>[WP-31](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31) [PG-24](../../../assurance/open-gates-register.md#rule-pg-24) completion-gate paragraph: physical arm64 push/Doze/background evidence — package-level obligation contribution |
| Provides | android-push-settings |
| Start prerequisites | **contract** [CON.22](contracts.md#task-con-22) — published notification.registerPush and unregisterPush. *Why:* Android push registration uses the generated operations<br>**artifact** [AND.03](#task-and-03) — the real Android foundation module AND.03 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap<br>**artifact** [AND.04](#task-and-04) — the real Android foundation module AND.04 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap<br>**artifact** [AND.06](#task-and-06) — the real Android foundation module AND.06 this feature is built on. *Why:* the feature uses the real foundation modules, not a fresh bootstrap |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AND.26](#task-and-26) — live FCM sender adapter with a project-bound credential. *Why:* [PG-24](../../../assurance/open-gates-register.md#rule-pg-24) requires physical arm64 receipt of an actually-sent push; Android only owns registration/receipt, not the sending path, which is WP45's named scaffolding replacement (recorded FCM sender responses -> WP45.09 proves live sending, this task and WP32 prove real device receipt)<br>**integration** [AND.07](#task-and-07) — foundation candidate proven against the deployed Cloud services. *Why:* the feature can be built on the foundation modules, but its acceptance runs against the deployed services AND.07 proves and requires any remaining Task/AI fixtures compiled out |
| Unblocks | [AND.13](#task-and-13), [AND.15](#task-and-15), [AND.19](#task-and-19), [AND.26](#task-and-26) |
| Write scope | `Mobile:src/features/ArcForges.Mobile.Settings/**`<br>`Mobile:src/core/ArcForges.Mobile.Network/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Offline notification-dedup/registration unit tests; physical-device push receipt, Doze/background behavior and no-GMS fallback are local opt-in per [PG-24](../../../assurance/open-gates-register.md#rule-pg-24) |
| Completion evidence | Physical device receipt of a real push; denied-permission and no-GMS durable-polling fallback observed |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Push registration uses the .NET Firebase binding and the no-GMS polling fallback is retained; writes moved to the C# projects. Acceptance unchanged. |

<a id="task-and-13"></a>

### AND.13 — Native interaction and recovery: full experience-02 device matrix

**Outcome.** The complete phone/tablet/back/IME/TalkBack/large-text/process-death/account-switch/denied-permission/no-GMS matrix from experience 02 passes against real services on a release APK, preserving typed effect uncertainty and drafts.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-13` and ledger record `ledger/tasks/and-13.md` in the Plan repository; task branch `task/and-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / L |
| Obligations | [WP-31.05](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.05) — all work except the parts mapped to AND.25 |
| Provides | android-native-interaction-verified |
| Start prerequisites | **artifact** [AND.08](#task-and-08) — auth/home built. *Why:* matrix exercises the real surfaces<br>**artifact** [AND.09](#task-and-09) — chat built. *Why:* matrix exercises the real surfaces<br>**artifact** [AND.10](#task-and-10) — tasks built. *Why:* matrix exercises the real surfaces<br>**artifact** [AND.11](#task-and-11) — library built. *Why:* matrix exercises the real surfaces<br>**artifact** [AND.12](#task-and-12) — settings/push built. *Why:* matrix exercises the real surfaces |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AND.24](#task-and-24) — real Harness evidence. *Why:* WP31.05's own completion gate names "real 52/26/25 evidence passes on release APK; mocks do not close any required journey"<br>**integration** [AND.25](#task-and-25) — real bridge evidence. *Why:* same gate text |
| Unblocks | [AND.08](#task-and-08), [AND.15](#task-and-15), [AND.19](#task-and-19), [AND.25](#task-and-25) |
| Write scope | `Mobile:tests/ArcForges.Mobile.DeviceTests/**` |
| Validation | Physical low/mid-tier arm64 device matrix (1000 messages, 4 MiB answer, rotation, process kill during send/refresh/upload, denied push, airplane/reconnect, account switch, expired approval, revoked source) is local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Per-scenario pass/fail with device identity and TalkBack/IME/large-text results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The androidTest Kotlin matrix moves to a net10.0-android device test project (local opt-in). The matrix itself and TalkBack, IME and large-text criteria are unchanged. |

<a id="task-and-14"></a>

### AND.14 — Scope and licence enforcement audit

**Outcome.** Full companion requirements, consumption-only restrictions, public-NuGet-only imports, and absence of desktop secrets, device-local paths and excluded professional-editing surfaces are verified with complete provenance.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-14` and ledger record `ledger/tasks/and-14.md` in the Plan repository; task branch `task/and-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Obligations | [WP-31.06](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.06) — full<br>[WP-30](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30) §3 binding rules: Apache-2.0 boundary, no GPL-family implementation, immutable producer artifacts — package-level obligation contribution |
| Provides | android-scope-enforced |
| Start prerequisites | **artifact** [AND.08](#task-and-08) — features exist to audit. *Why:* surface-action inventory cross-check needs the real surfaces<br>**artifact** [AND.09](#task-and-09) — features exist to audit. *Why:* same<br>**artifact** [AND.10](#task-and-10) — features exist to audit. *Why:* same |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.15](#task-and-15) |
| Write scope | `Mobile:eng/policy/**`<br>`Mobile:eng/provenance/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Package content/dependency/privacy static checks plus full surface-action inventory cross-check, offline |
| Completion evidence | Complete surface/action inventory cross-check with no unaccepted third-party provenance |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: eng/policy and eng/provenance machinery already exists and is exercised for the Hello candidate ([F-023](../../../assurance/open-gates-register.md#rule-f-023) closed 2026-09-19); this task extends it to the full companion surface |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Gradle-based inventory becomes NuGet/MSBuild inventory; the public-Maven-only import criterion becomes public-NuGet-only. Acceptance unchanged. |

<a id="task-and-15"></a>

### AND.15 — Complete companion acceptance

**Outcome.** A signed candidate joins real 31.00-31.06 evidence with producer manifests and the full compatible 52/26/25/42/45 integration manifest, verified through injected-failure scenarios with exact device/OS/server/worker/package identities.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-15` and ledger record `ledger/tasks/and-15.md` in the Plan repository; task branch `task/and-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-31](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-31.90](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.90) — full<br>[WP-31](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31) [PG-24](../../../assurance/open-gates-register.md#rule-pg-24) completion-gate paragraph: physical arm64 push/Doze/background evidence — package-level obligation contribution |
| Provides | android-companion-candidate |
| Start prerequisites | **artifact** [AND.08](#task-and-08) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.09](#task-and-09) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.10](#task-and-10) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.11](#task-and-11) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.12](#task-and-12) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.13](#task-and-13) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.14](#task-and-14) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.27](#task-and-27) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.16](#task-and-16) |
| Write scope | `Mobile:src/ArcForges.Mobile/**` |
| Validation | Full physical-device release scenarios and injected failure matrix, local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Owned-artifact-and-real-integration receipt joining all producer manifests; distribution/store activation explicitly deferred to WP32 |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Final join of the MAUI companion; writes moved to the MAUI app project. Acceptance unchanged. |

<a id="task-and-16"></a>

### AND.16 — Signed Android release artifacts (direct APK)

**Outcome.** A signed direct APK build automatically from reviewed main as MAUI outputs, with monotonic versionCode within applicationId com.arcforges.mobile, immutable provenance and tested WP03 update-schema compatibility.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-16` and ledger record `ledger/tasks/and-16.md` in the Plan repository; task branch `task/and-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / S |
| Obligations | [WP-32.00](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.00) — full |
| Provides | android-signed-artifacts |
| Start prerequisites | **artifact** [AND.15](#task-and-15) — companion acceptance complete. *Why:* signs the real companion, not the Hello candidate |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.17](#task-and-17), [AND.18](#task-and-18), [AND.21](#task-and-21) |
| Write scope | `Mobile:.github/workflows/ci.yml`<br>`Mobile:eng/mobile.py`<br>`Mobile:eng/published.py` |
| Shared resources | [RES-android-signing-and-store](../shared-resources.md#res-android-signing-and-store) (append) |
| Validation | Actual signature/package/R8/runtime and version-monotonicity checks; clean device install/upgrade is local opt-in |
| Completion evidence | Signed APK with recorded provenance; monotonic versionCode for com.arcforges.mobile; reinstall guidance from io.github.arcforges.mobile recorded in docs/releasing.md with no data migration. |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: The full candidate-build-sign-publish pipeline already exists and runs on every merge to main (see.github/workflows/ci.yml build/publish jobs, eng/mobile.py sign/stage); this task extends it to the real companion and confirms WP03 update-schema compatibility, it does not build the pipeline from scratch |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The signing pipeline and persistent certificate are kept. The upgrade check in eng/published.py is re-based on the com.arcforges.mobile identity; the io.github line stays immutable history. Acceptance unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: the signed AAB for the Play channel is out of scope, not completed (Play publication is out of V1, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S11); the signed direct APK channel is unchanged. |

<a id="task-and-17"></a>

### AND.17 — Release runtime inspection

**Outcome.** Mono and ART runtime, the .NET for Android closure (no Kotlin, Compose or Connect-Kotlin residue), min and target API (26 and 37), arm64 assets with 16 KB alignment, trimming and R8 rules (AndroidLinkTool=r8), and required permissions are verified on the actual signed APK, not source inspection.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-17` and ledger record `ledger/tasks/and-17.md` in the Plan repository; task branch `task/and-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Obligations | [WP-32.01](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.01) — full |
| Provides | android-release-runtime-verified |
| Start prerequisites | **artifact** [AND.16](#task-and-16) — signed candidate. *Why:* inspects the real artifact |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.23](#task-and-23) |
| Write scope | `Mobile:eng/mobile.py` |
| Validation | Install without development server/toolchain; startup/identity/RPC/notifications/lifecycle release tests are local opt-in |
| Completion evidence | [VG-07](../../../assurance/open-gates-register.md#rule-vg-07) evidence: real Mono and ART release artifact inspection, not debug-only or source-only proof. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Kotlin/ART and Compose/grpc-lite inspection rewritten to the Mono/AOT and .NET closure with the same release checks (min/target API, arm64, R8, permissions, no debug-only proof). Rewording, not weakening. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: release inspection of the AAB is out of scope, not completed (Play publication is out of V1, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S11); inspection of the signed direct APK is unchanged. |

<a id="task-and-18"></a>

### AND.18 — Dependency and source rights closure (final artifact)

**Outcome.** Direct and transitive NuGet, MSBuild, workload, runtime and asset closure, licences, provenance and reproducible SBOM and NOTICE are audited against the final companion candidate, including F-023-class re-closure of the MAUI closure (the android-0.1.0-ci.14.1 closure does not carry over); public schema and tooling Apache origin and independently original app implementation are verified.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-18` and ledger record `ledger/tasks/and-18.md` in the Plan repository; task branch `task/and-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Obligations | [WP-32.02](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.02) — full |
| Provides | android-dependency-rights-verified |
| Start prerequisites | **artifact** [AND.16](#task-and-16) — signed candidate. *Why:* audits the real final artifact |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.23](#task-and-23) |
| Write scope | `Mobile:eng/policy/**`<br>`Mobile:eng/provenance/**`<br>`Mobile:third-party/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Forbidden-licence fixture, unpinned or dynamic dependency and changed-checksum rejection tests, plus a fixture that rejects any AGPL DesktopPlatform package in the app closure and any PDF parser or renderer package (PDFium or a PDF rendering binding) under [P2-022](../../../decisions/phase-2-specification-decisions.md#rule-p2-022); offline. |
| Completion evidence | [F-023](../../../assurance/open-gates-register.md#rule-f-023) re-closure for the final MAUI companion candidate (NuGet and MSBuild binary inventory matches the candidate; the closure reopened by the dependency change and is re-proven). |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: eng/licences.py, eng/check_provenance.py and the provenance-record set already implement this machinery and have closed [F-023](../../../assurance/open-gates-register.md#rule-f-023) twice for Hello-stage candidates; this task re-runs it against the real companion's larger dependency closure |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Gradle and plugin closure becomes NuGet/MSBuild closure; the AGPL exclusion (P2-021.3) is an explicit fixture, and the PDF parser and renderer exclusion ([P2-022](../../../decisions/phase-2-specification-decisions.md#rule-p2-022)) is added to the same fixture. Acceptance unchanged. |

<a id="task-and-19"></a>

### AND.19 — Consumption-only enforcement

**Outcome.** Absence of purchase buttons/embedded checkout/store billing/external purchase CTAs/licence-key unlock is enforced by static route/dependency checks and exercised across every state including expired subscription and exhausted credits.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-19` and ledger record `ledger/tasks/and-19.md` in the Plan repository; task branch `task/and-19` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Obligations | [WP-32.03](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.03) — full |
| Provides | android-consumption-only-verified |
| Start prerequisites | **artifact** [AND.08](#task-and-08) — every authentication and Home state to audit. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AND.09](#task-and-09) — every conversation state to audit. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AND.10](#task-and-10) — every task, approval and automation state to audit. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AND.11](#task-and-11) — every library and resource state to audit. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [AND.12](#task-and-12) — every presence, push, link and settings state to audit. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AND.13](#task-and-13) — the rendered-state UX tests run in the net10.0-android device test project. *Why:* UX states that need a rendered MAUI page are executed there (local opt-in); completing on that project means the all-state coverage is not claimed before the suite exists |
| Unblocks | [AND.23](#task-and-23) |
| Write scope | `Mobile:eng/policy/**`<br>`Mobile:tests/ArcForges.Mobile.Tests/**` |
| Validation | Static route and dependency checks ([MC-01](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-mc-01)..[MC-06](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-mc-06) build-time and CI assertions, as C# analyzers or xUnit architecture tests) plus all-state UX tests, offline where feasible; UX states that need a rendered MAUI page run in the AND.13 device test project as local opt-in. |
| Completion evidence | [VG-13](../../../assurance/open-gates-register.md#rule-vg-13) evidence: no build path can display a purchase CTA or accept a licence key |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Static checks move from Gradle to C# analyzers or architecture tests in tests/ArcForges.Mobile.Tests (added to writes); rendered-state UX tests run in the AND.13 device test project, and AND.19 completes on AND.13 (typed edge). Acceptance unchanged. |

<a id="task-and-20"></a>

### AND.20 — Direct-channel signed update client

**Outcome.** arch-11 channel behavior and a notify-only signed update client are complete, consuming WP03's format/fixture keys now; channel-switch export/reinstall guidance is explicit.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-20` and ledger record `ledger/tasks/and-20.md` in the Plan repository; task branch `task/and-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-32.04](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.04) — full |
| Provides | android-update-channels |
| Start prerequisites | **contract** [CON.16](contracts.md#task-con-16) — android-update.v1 feed format and fixture signing keys. *Why:* already available per the producer matrix ("No production key prerequisite; WP32/WP41 consume fixture roots")<br>**artifact** [AND.02](#task-and-02) — registered core/network and feature/settings module shells from android-module-boundaries. *Why:* AND.02 owns creation and one-time Gradle registration of the architecture-27 module set; the update client cannot be compiled or tested in these production modules until that delivered boundary exists |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.23](#task-and-23) |
| Write scope | `Mobile:src/core/ArcForges.Mobile.Network/**`<br>`Mobile:src/features/ArcForges.Mobile.Settings/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Expired/rollback/wrong-certificate/URL/hash and offline-stale-feed tests, offline where feasible |
| Completion evidence | Direct APK flow complete with no silent install |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Explicitly does NOT wait on WP53 (production feed/signing) — [WP-32.04](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.04)'s own text states WP53's replacement is verified at WP50, not a backward input to this task. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Notify-only update client ported to C# on the same android-update.v1 feed rules. Writes moved to the C# projects. Acceptance unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: the Play-primary update flow is out of scope, not completed (Play publication is out of V1, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S11); the direct-APK notify-only update client is unchanged. |

<a id="task-and-21"></a>

### AND.21 — Physical device and recovery gates

**Outcome.** Full companion runs on minimum-supported and current physical-device profiles across weak/offline network, permission denial, no-GMS, key-loss/backup-restore, process kill and OS background limits; forward-rescue release with a higher versionCode is proven (Android never downgrades as routine rollback).

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-21` and ledger record `ledger/tasks/and-21.md` in the Plan repository; task branch `task/and-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / L |
| Obligations | [WP-32.05](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.05) — all work except the parts mapped to AND.26 |
| Provides | android-device-recovery-verified |
| Start prerequisites | **artifact** [AND.16](#task-and-16) — signed candidate. *Why:* tests the real signed artifact |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.23](#task-and-23), [AND.26](#task-and-26) |
| Write scope | `Mobile:eng/mobile.py` |
| Validation | Actual local/server unknown-effect replay, encrypted draft/outbox retention through upgrade, signing-key recovery rehearsal — all local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | All mandatory scenarios pass; material device limits disclosed; no pending user work lost |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Device and recovery gates unchanged; they run against the MAUI signed candidate instead of the Kotlin candidate. |

<a id="task-and-22"></a>

### AND.22 — Android scope statement

**Outcome.** Documentation and store/release/readme/platform matrices state Android-only scope; iOS/Swift/KMP/cross-platform UI are recorded as outside this delivery with no false retained-iOS claim.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-22` and ledger record `ledger/tasks/and-22.md` in the Plan repository; task branch `task/and-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / S |
| Obligations | [WP-32.06](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.06) — full |
| Provides | android-scope-statement |
| Start prerequisites | **artifact** [AND.01](#task-and-01) — the AND.01 Mobile documentation (docs/releasing.md reinstall guidance, docs/maui-toolchain.md, docs/licence-boundary.md) merged. *Why:* both tasks write Mobile docs/**; AND.22 edits the merged AND.01 text instead of racing it |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.23](#task-and-23) |
| Write scope | `Mobile:README.md`<br>`Mobile:docs/**` |
| Validation | Store/release/readme/platform matrix cross-check against the signed Android artifact, offline |
| Completion evidence | No false retained-iOS deliverable or unsupported platform claim |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Small and independent; can land in the same PR series as AND.18 or AND.19 for convenience without being merged into them as one task. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Successor AND.40 retires the Kotlin wording in README.md and docs (README KMP row, docs/development.md, docs/releasing.md). The development-only desktop preview in shared/ (desktopMain; AGENTS.md:3 forbids any desktop product) retires with the KMP module. The AND.40 README and AGENTS.md restate the Android-only scope, the no-desktop, no-iOS and no-macOS product statement, and the development-only qualifier for any local tooling; none of these is dropped. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); coordinator adjudication, brief section 10): start edge on AND.01 orders the shared Mobile docs writes. |

<a id="task-and-23"></a>

### AND.23 — Distribution acceptance

**Outcome.** The exact signed APK, manifest/hash/versionCode/certificate identity, compatible server/Contracts release and all gate receipts are archived and published through the automatic main graph; a clean-device download verifies signature/hash and exercises actual services.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-23` and ledger record `ledger/tasks/and-23.md` in the Plan repository; task branch `task/and-23` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / M |
| Package acceptance | Records the [WP-32](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-32.90](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.90) — full<br>[WP-32](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32) [PG-24](../../../assurance/open-gates-register.md#rule-pg-24) completion-gate paragraph (recheck on distributed artifact) — package-level obligation contribution |
| Provides | android-distribution-candidate |
| Start prerequisites | **artifact** [AND.17](#task-and-17) — release runtime inspection passed. *Why:* final join<br>**artifact** [AND.18](#task-and-18) — dependency rights closed. *Why:* final join<br>**artifact** [AND.19](#task-and-19) — consumption-only verified. *Why:* final join<br>**artifact** [AND.20](#task-and-20) — update client complete. *Why:* final join<br>**artifact** [AND.21](#task-and-21) — device/recovery gates passed. *Why:* final join<br>**artifact** [AND.22](#task-and-22) — scope statement complete. *Why:* final join |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [AND.26](#task-and-26) — live FCM sender + physical receipt rechecked on the distributed artifact. *Why:* producer matrix: "WP32 inherits it through 31 and rechecks the distributed artifact" ([PG-24](../../../assurance/open-gates-register.md#rule-pg-24)) |
| Unblocks | [AND.26](#task-and-26), [REL.04](release.md#task-rel-04) |
| Write scope | `Mobile:eng/mobile.py` |
| Shared resources | [RES-android-signing-and-store](../shared-resources.md#res-android-signing-and-store) (append) |
| Validation | Download public candidate in a clean device path, verify signature/hash, exercise actual services — local opt-in |
| Completion evidence | Distribution complete only with real receipts |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Distribution receipts bind to the MAUI signed APK and AAB (com.arcforges.mobile). Acceptance unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: the signed AAB and the store-submission receipt are out of scope, not completed (Play publication and store listings are out of V1, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S11); the signed APK distribution receipts are unchanged. |

<a id="task-and-24"></a>

### AND.24 — Real CF Harness generation/tool loop observed end to end on Android

**Outcome.** real admitted generation, tool proposal and automation execution replace the contract-bound fixture turn endpoint on a physical device

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-24` and ledger record `ledger/tasks/and-24.md` in the Plan repository; task branch `task/and-24` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-31.01](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.01) — real-integration closure<br>[WP-31.02](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.02) — real-integration closure |
| Start prerequisites | **artifact** [AND.09](#task-and-09) — real, delivered outcome of AND.09 (Conversations and context (AN07-AN10/15/16)). *Why:* this integration exercises the real conversations and context (AN07-AN10/15/16) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [AND.10](#task-and-10) — real, delivered outcome of AND.10 (Tasks, approvals and automation (AN11-AN13/19/25)). *Why:* this integration exercises the real tasks, approvals and automation (AN11-AN13/19/25) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [HAR.00](harness.md#task-har-00) — real, delivered outcome of HAR.00 (Turn loop, tool batching and bounds (RunWorkflow core)). *Why:* this integration exercises the real turn loop, tool batching and bounds (RunWorkflow core) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [HAR.03](harness.md#task-har-03) — real generated streaming and durable output. *Why:* the Android end-to-end scenario reads real Harness output |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.09](#task-and-09), [AND.10](#task-and-10), [AND.13](#task-and-13), [HAR.05](harness.md#task-har-05), [HAR.06](harness.md#task-har-06) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | real admitted generation, tool proposal and automation execution replace the contract-bound fixture turn endpoint on a physical device |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Real Harness integration unchanged; the Android client is the MAUI app. Start edges to AI-lane tasks are re-homed to Cloud under P2-021.5, not renumbered here. |

<a id="task-and-25"></a>

### AND.25 — Real desktop tool dispatch and unknown-effect reconciliation from Android

**Outcome.** an Android-initiated remote task actually reaches a desktop through the durable bridge with correct lease/grant/reconciliation semantics

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-25` and ledger record `ledger/tasks/and-25.md` in the Plan repository; task branch `task/and-25` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-31.02](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.02) — device-dispatch closure<br>[WP-31.05](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.05) — real-52/26 evidence |
| Start prerequisites | **artifact** [AND.10](#task-and-10) — real, delivered outcome of AND.10 (Tasks, approvals and automation (AN11-AN13/19/25)). *Why:* this integration exercises the real tasks, approvals and automation (AN11-AN13/19/25) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [AND.13](#task-and-13) — real, delivered outcome of AND.13 (Native interaction and recovery: full experience-02 device matrix). *Why:* this integration exercises the real native interaction and recovery: full experience-02 device matrix instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [DEV.02](device-bridge.md#task-dev-02) — the real durable target queue. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.03](device-bridge.md#task-dev-03) — real owner reauthorization on the desktop. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.06](device-bridge.md#task-dev-06) — real remote approval and steering. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.07](device-bridge.md#task-dev-07) — real offline expiry and unknown-effect recovery. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.12](device-bridge.md#task-dev-12) — the cross-repository (toolRequestId, attemptId, commandId) agreement. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [DEV.14](device-bridge.md#task-dev-14) — the real device tool bridge over the deployed realtime transport. *Why:* real desktop dispatch from Android cannot be proven without the real device tool bridge ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S13) |
| Unblocks | [AND.10](#task-and-10), [AND.13](#task-and-13) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | an Android-initiated remote task actually reaches a desktop through the durable bridge with correct lease/grant/reconciliation semantics |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Real desktop dispatch unchanged; stack-neutral. Acceptance unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): added: complete edge on DEV.14 (S13; real desktop dispatch needs the real device tool bridge). |

<a id="task-and-26"></a>

### AND.26 — Real FCM sending and physical Android receipt

**Outcome.** [PG-24](../../../assurance/open-gates-register.md#rule-pg-24): a project-bound FCM credential actually sends and a physical arm64 device actually receives, including duplicate/rotation/revocation and denied-permission/no-GMS recovery

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-26` and ledger record `ledger/tasks/and-26.md` in the Plan repository; task branch `task/and-26` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-31.04](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.04) — physical receipt closure<br>[WP-32](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32) [PG-24](../../../assurance/open-gates-register.md#rule-pg-24) completion-gate paragraph (recheck on distributed artifact) — [PG-24](../../../assurance/open-gates-register.md#rule-pg-24) closure<br>[WP-45.09](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.09) — device-delivery half<br>[WP-32.05](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.05) — physical/no-GMS/permission evidence half |
| Start prerequisites | **artifact** [AND.12](#task-and-12) — real, delivered outcome of AND.12 (Presence, push, links and settings (AN20-AN24)). *Why:* this integration exercises the real presence, push, links and settings (AN20-AN24) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [AND.23](#task-and-23) — real, delivered outcome of AND.23 (Distribution acceptance). *Why:* this integration exercises the real distribution acceptance instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [OPS.10](operations.md#task-ops-10) — real, delivered outcome of OPS.10 (Customer push delivery and registration lifecycle). *Why:* this integration exercises the real customer push delivery and registration lifecycle instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [AND.21](#task-and-21) — real, delivered outcome of AND.21 (Physical device and recovery gates). *Why:* this integration exercises the real physical device and recovery gates instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.12](#task-and-12), [AND.23](#task-and-23), [OPS.10](operations.md#task-ops-10), [REL.04](release.md#task-rel-04) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | [PG-24](../../../assurance/open-gates-register.md#rule-pg-24): a project-bound FCM credential actually sends and a physical arm64 device actually receives, including duplicate/rotation/revocation and denied-permission/no-GMS recovery |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as COM.17. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Physical FCM receipt unchanged; the receipt side uses the .NET Firebase binding. Acceptance unchanged. |

<a id="task-and-27"></a>

### AND.27 — ArcScope library, reports and simulation runs on Android

**Outcome.** AN14 and AN26-AN28: the read-only ArcScope library, session and report views with provenance and stored chart snapshots, report sharing through the system share sheet, simulation run status with cancel, and the ArcScope notification kinds opening their objects. A fresh installation discovers runs with simulation.listRuns before reading details or cancelling. The AN27 static PDF preview is retired under [P2-022](../../../decisions/phase-2-specification-decisions.md#rule-p2-022) and replaced by download or share of the exported bundle and an Android ACTION_VIEW intent to the system PDF viewer for arcscope.report.pdf.v1. The app embeds no PDF parser or renderer, and generic PDF attachments remain opaque files.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-27` and ledger record `ledger/tasks/and-27.md` in the Plan repository; task branch `task/and-27` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-31.07](../../work-packages/31-arcchat-mobile-android.md#rule-wp-31.07) — full |
| Provides | android-arcscope-workspace |
| Start prerequisites | **artifact** [AND.11](#task-and-11) — the Library route and resource preview surfaces. *Why:* the ArcScope library is built into the Library destination and reuses its preview and transfer paths<br>**contract** [CON.24](contracts.md#task-con-24) — the generated library operations. *Why:* the views call scope.listProjects, scope.listSessions and scope.getSession<br>**contract** [CON.21](contracts.md#task-con-21) — the generated simulation operations. *Why:* run status and cancel use simulation.getRun and simulation.cancelRun |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.68](cloud.md#task-cloud-68) — the deployed library read model. *Why:* acceptance reads a real synced workspace<br>**integration** [SIM.05](simulator.md#task-sim-05) — the deployed simulation operations. *Why:* acceptance follows a real run to its terminal state<br>**integration** [SCOPE.22](arcscope.md#task-scope-22) — the delivered desktop project/session and report publication adapter. *Why:* acceptance must consume desktop-produced synced metadata and readable reports rather than a fixture; UI development remains parallel<br>**integration** [SCOPE.18](arcscope.md#task-scope-18) — a desktop-produced report from the reports and reproducibility task. *Why:* report sharing acceptance needs a desktop-produced report to read and share on Android ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S13) |
| Unblocks | [AND.15](#task-and-15) |
| Write scope | `Mobile:src/features/ArcForges.Mobile.Scope/**` |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). PDF disposition check ([P2-022](../../../decisions/phase-2-specification-decisions.md#rule-p2-022)): the ACTION_VIEW hand-off of arcscope.report.pdf.v1 to the system viewer is exercised in the local run, and the AND.18 closure fixture and AND.19 architecture tests reject any PDF parser or renderer package in the app closure. |
| Completion evidence | A report synced from ArcScope desktop found, read and shared on Android; a Cloud simulation run followed to its terminal state; revocation, unavailable-artifact and raw-data-local cases. Run discovery after reinstall or on another authorized device; no remembered run ID required. PDF disposition evidence: the exported report opened through ACTION_VIEW in a system viewer on the device, and the closure listing shows no PDF renderer. |
| Baseline (unreviewed unless accepted) | not-started Observed none. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): ArcScope library, report and simulation views port to MAUI; system share sheet and notification behaviours use MAUI platform equivalents. Writes moved to the C# feature project. The AN27 static PDF preview is retired under P2-022.2 (download or share of the bundle, and an Android ACTION_VIEW hand-off to the system viewer); the other acceptance is unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): added: complete edge on SCOPE.18 (S13; acceptance needs a desktop-produced report). |

<a id="task-and-40"></a>

### AND.40 — MAUI migration of the existing Mobile app: Hello client, streaming consumer rules, Keystore probe, CI, signing and C# policy (Kotlin, KMP and Gradle retired)

**Outcome.** The shipped Mobile app is a .NET MAUI Android app (its shipped projects target net10.0-android only, and its host-run test, policy and architecture-test projects target net10.0 as the validation states; Mono runtime with AOT for release, UseMonoRuntime=true explicit, applicationId com.arcforges.mobile, persistent android-release signing identity cert SHA256 7a8b3b14...). Its Hello client uses Grpc.Net.Client.Web selecting binary gRPC-Web, with the transport rules carried over from the retired Kotlin client (the GrpcWebMode and server-stream media type are not settled here: they are observed and recorded by PRF.12 together with the fallback decision): no cookies, no redirects, no connection retry, deadline no more than 5 s, 10 s call timeout, the grpc-timeout header in the same format, and the 1..256 name rule. Its streaming consumer keeps frames in order, requires exactly one OK trailer (a missing trailer is DATA_LOSS), stays bounded, and closes the stream on cancellation even when the caller is cancelled (NonCancellable close). A Keystore probe reports the platform security level without claiming hardware backing. CI on Windows and Linux compiles and executes the offline unit tests; the signed candidate and prerelease pipeline use the persistent identity in the protected android-release environment only. GOV.12's Gradle policy is replaced by a C# policy suite that keeps its layering, licence, naming and banned-API categories: the seven canonical BAN-* categories are enforced by Mobile-owned Apache-2.0 rules with negative fixtures, authored from the Design requirement text. Under P2-021.3 Mobile never consumes an AGPL-3.0-only DesktopPlatform package: no copy, port or consumption of the DesktopPlatform banned-symbol catalog and no ArcForges.Build.Policy package is part of the MAUI closure. Mobile's build-only consumption of ArcForges.Build.Policy 1.0.0-ci.40.1 recorded under GOV.12 (PR17, merged 34c64e0) ends in this task, which reverses, for Mobile, the GOV.12 single-canonical-producer receipt (history retained). The Kotlin app, KMP shared module and Gradle build retire in a second pull request of this task, after the first pull request has made the MAUI candidate pass the offline checks and a signed MAUI prerelease (tag namespace android-maui-VERSION) is published from main; the second pull request then switches the MAUI publish to android-VERSION.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-40` and ledger record `ledger/tasks/and-40.md` in the Plan repository; task branch `task/and-40` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-30.03](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.03) — Hello client transport and streaming consumer rules only (binary gRPC-Web, deadlines, no cookies, no redirects, no retry, exactly one OK trailer); full contract consumption stays in AND.04<br>[WP-05.00](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.00) — GOV.12 successor: Mobile policy suite in C#<br>[WP-05.01](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01) — GOV.12 successor: licence boundary and dependency allowlist over NuGet<br>[WP-05.02](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.02) — GOV.12 successor: forbidden-term scanner in the Mobile PR build<br>[WP-05.04](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.04) — GOV.12 successor: Mobile banned-API fixtures |
| Provides | android-maui-app-project; android-hello-transport; android-streaming-consumer; android-keystore-probe; android-maui-release-pipeline; android-csharp-policy-suite |
| Start prerequisites | **artifact** [AND.01](#task-and-01) — the com.arcforges.mobile identity and the pinned .NET 10 / Android workload / NuGet tuple. *Why:* the MAUI app project, its package identity and its toolchain pins must exist before the migration code lands |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CON.11](contracts.md#task-con-11) — the generated C# EventService Watch and Poll operations and the ApplicationService operations that CON.11 publishes in the NuGet Contracts packages (events.proto and application.proto). *Why:* the streaming consumer rules (one OK trailer, DATA_LOSS on a missing trailer, bounded, NonCancellable close) are defined against the EventService stream shape; the CI loopback fixtures are test-only characterisation of that shape, not a substitute, so AND.40 may be delivered first and completes only when the published generated client confirms the shape<br>**integration** [CLOUD.29](cloud.md#task-cloud-29) — the deployed stream connection and authentication (EventService.Watch shell) that the streaming consumer rules are checked against. *Why:* the streaming consumer rules (one OK trailer, DATA_LOSS on a missing trailer, bounded, NonCancellable close) are characterised by test-only loopback fixtures; the real stream producer confirms them before AND.40 completes. CLOUD.29 starts on CON.11, CLOUD.19 and CLOUD.21 only, so the edge is acyclic |
| Unblocks | [AND.02](#task-and-02), [AND.04](#task-and-04), [CLOUD.29](cloud.md#task-cloud-29), [CLOUD.84](cloud.md#task-cloud-84), [CON.40](contracts.md#task-con-40), [PRF.12](runtime-proofs.md#task-prf-12) |
| Write scope | `Mobile:src/ArcForges.Mobile/**`<br>`Mobile:src/core/ArcForges.Mobile.Network/**`<br>`Mobile:src/core/ArcForges.Mobile.Security/**`<br>`Mobile:tests/ArcForges.Mobile.Tests/**`<br>`Mobile:tests/ArcForges.Mobile.Policy/**`<br>`Mobile:ArcForges.Mobile.slnx`<br>`Mobile:global.json`<br>`Mobile:Directory.Build.props`<br>`Mobile:Directory.Packages.props`<br>`Mobile:NuGet.config`<br>`Mobile:.github/workflows/ci.yml`<br>`Mobile:.github/workflows/security.yml`<br>`Mobile:.gitleaks.toml`<br>`Mobile:eng/mobile.py`<br>`Mobile:eng/published.py`<br>`Mobile:eng/policy/**`<br>`Mobile:README.md`<br>`Mobile:AGENTS.md`<br>`Mobile:docs/**`<br>`Mobile:app/**`<br>`Mobile:shared/**`<br>`Mobile:gradle/**`<br>`Mobile:build.gradle.kts`<br>`Mobile:settings.gradle.kts`<br>`Mobile:settings-gradle.lockfile`<br>`Mobile:gradle.properties`<br>`Mobile:gradlew`<br>`Mobile:gradlew.bat`<br>`Mobile:.java-version`<br>`Mobile:eng/licences.gradle.kts`<br>`Mobile:eng/licences.py, Mobile:eng/resources.py, Mobile:eng/build_identity.py, Mobile:eng/dependency_policy.py, Mobile:eng/maui_identity.py, Mobile:eng/device-smoke.py and Mobile:eng/verify_published_fixture.py (the MAUI paths, and the retirement of their Gradle and Kotlin parts in the second pull request)`<br>`Mobile:eng/check_provenance.py (inventory classification of the new .NET projects and of the retired Gradle and Kotlin paths only)`<br>`Mobile:eng/tests/** (tests of the eng tools above)`<br>`Mobile:eng/provenance/** (successor records, inventory rows and the retirement receipt)`<br>`Mobile:eng/version-sources.json`<br>`Mobile:third-party/** and Mobile:THIRD_PARTY_NOTICES.md (the MAUI closure notices, and the Kotlin-only entries retired after review)`<br>`Mobile:.github/dependabot.yml (the gradle ecosystem replaced by nuget in the second pull request)`<br>`Mobile:.gitignore (the bin/ and obj/ of the new projects)`<br>`Mobile:CONTRIBUTING.md and Mobile:.gitattributes (the Gradle and JDK instructions and the gradlew attribute replaced by the .NET workflow in the second pull request)` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (exclusive), [RES-android-signing-and-store](../shared-resources.md#res-android-signing-and-store) (append) |
| Validation | Offline on Windows and Linux CI only (compile, offline xUnit and policy tests, actionlint, gitleaks, existing eng/*.py tests): restore with locked packages (packages.lock.json), NuGet audit and dependency-admission and provenance records for every package in the closure (Apache-2.0 only; no AGPL DesktopPlatform package and no ArcForges.Build.Policy reference); net10.0-android Release build with Mono AOT, trimming and R8 (AndroidLinkTool=r8), which is the first proof of the AND.01 candidate tuple (a failure reopens AND.01); the Hello transport suite (no cookies, no redirects, no retry, deadline cap 5 s, call timeout 10 s, grpc-timeout format, binary gRPC-Web selected through the configured GrpcWebMode with the configured media type asserted, the observed unary and server-stream mode left to PRF.12, 1..256 name rule) and the streaming suite (ordered frames then one OK trailer; an error trailer after frames keeps the frames and status; a missing trailer is DATA_LOSS; deadline mid-stream keeps frames and gives DEADLINE_EXCEEDED; cancel releases the stream) against loopback fixtures; C# policy tests (layering, licence boundary, forbidden terms, the seven BAN-* categories as Mobile-owned rules) with negative fixtures; F-023-class closure re-proof (licence, provenance, SBOM and NOTICE) for the MAUI closure on the candidate; a NuGet closure check that rejects an unadmitted or unpinned package. Signing and prerelease publication run only in the protected android-release environment on main. Emulator and device runs are local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), not CI. The Gradle, Kotlin and KMP retirement lands only after a candidate passes these offline checks and its signed MAUI prerelease is published from main. Every shipped project targets net10.0-android only; host-run test, policy and architecture-test projects (executed by the .NET test host on a Windows or Linux machine, never on an Android device or emulator) target net10.0 so that they run on hosted Windows and Linux runners without an emulator ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)), Android device test projects (AND.13) target net10.0-android, and platform-neutral libraries may add net10.0 as a second target used only by the host-run tests; a policy test proves that the resolved closure of the MAUI app targets net10.0-android only. |
| Completion evidence | Offline CI run identifiers for the Windows and Linux builds with executed test counts; transport and streaming test matrix results (including the configured media-type assertion; observed unary and server-stream values are PRF.12 evidence); Keystore probe output recording the reported security level (software level is not hardware evidence); policy suite results with negative fixtures; NuGet admission and provenance records for the closure; a closure listing showing no ArcForges.Build.Policy and no AGPL DesktopPlatform package; F-023-class closure re-proof for the MAUI candidate (licence, provenance, SBOM and NOTICE); a retirement receipt listing every removed Kotlin, KMP, Gradle and ArcForges.Build.Policy consumer path; signed candidate hash and applicationId and certificate SHA256 verification (7a8b3b14...); reinstall guidance from io.github.arcforges.mobile recorded in docs/releasing.md with no data migration. |
| Baseline (unreviewed unless accepted) | not-started Observed (2026-10-08): the Kotlin pipeline in .github/workflows/ci.yml already signs and publishes prereleases on main through eng/mobile.py sign_candidate and eng/published.py; this task re-hosts those steps on .NET outputs. The MAUI signing properties were taken from Microsoft Learn search snippets and must be verified by a local non-publishing build before use. The Kotlin CloudHelloClient defines the transport rules this task keeps. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): new C#-first successor of the Kotlin Android foundation, of GOV.12 (Gradle policy) and of the Android CI and signing surfaces. Published Kotlin prereleases stay immutable history; nothing here unpublishes, deletes or re-signs them. No start edge on CON.07: the Hello.V1 surface the transport uses is already published in the ArcForges.Contracts.PublicApi NuGet package (Contracts repo evidence), and the transport, streaming consumer and Keystore probe use none of CON.07's identity, session or native-auth types; AND.04 keeps its CON.07 edge for those. CON.11 and CLOUD.29 are completion edges, not start edges: the loopback fixtures are test-only characterisation of the EventService stream shape, not a substitute, and the published client and the real stream producer confirm it before AND.40 completes. Planning repair 2026-10-09 ([DLV-34](../README.md#rule-dlv-34); coordinator adjudication, brief section 10 AND.40 decisions): decision 1 (host test targets), decision 2 (write scope for the eng tools, tests, provenance, notices, dependabot, .gitignore, CONTRIBUTING.md and .gitattributes) and decision 5 (two pull requests: MAUI beside Kotlin under android-maui-VERSION, then the retirement and the switch to android-VERSION). Recorded here as well: global.json stays at SDK 10.0.400 with rollForward disable (decision 3), and the API target is targetSdk 36 with compile 36.1 under [D-016](../../../decisions/phase-1-foundation-decisions.md#rule-d-016) (decision 4). The other decisions are recorded in the brief and stated in the pull requests; they change no acceptance. Planning repair 2026-10-09 ([DLV-34](../README.md#rule-dlv-34); fix4 review follow-up, non-blocking items): "host-run" is defined in place (executed by the .NET test host on a Windows or Linux machine, never on an Android device or emulator) and the opening sentence names the shipped app; no acceptance changes. Planning repair fix8 2026-10-10 ([DLV-34](../README.md#rule-dlv-34); coordinator ruling S57(13)): note only; no edge is added to this delivered task (S16(a)/(f)). Its completion follow-up observes the streaming consumer rules (frames, exactly one OK trailer, cancel) against the deployed route after CLOUD.34 delivers the heartbeat frames and the five-minute close, because CLOUD.29's shell alone produces no data frame or normal close. CLOUD.29 now takes an artifact start edge on this task for its MAUI Android leg, which runs this task's ServerStreamConsumer through the PRF.12 emulator harness. |
