# Android companion — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Kotlin/Compose foundation, companion features and Android release gates.

Tasks: 26 · Owning repositories: Mobile · Integration owner(s): Mobile integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [AND.01](#task-and-01) | Android production identity and stable toolchain reconciliation | producer | M | [PRF.10](runtime-proofs.md#task-prf-10) (artifact) | not-started |
| [AND.02](#task-and-02) | Real Android module graph and AN01-AN25 route/state contracts | producer | L | [AND.01](#task-and-01) (artifact) | not-started |
| [AND.03](#task-and-03) | Android runtime and OS adapters (Compose, Credential Manager, Keystore wrapper, WorkManager, FCM registration, SAF/MediaStore) | feature | L | [AND.02](#task-and-02) (artifact) | not-started |
| [AND.04](#task-and-04) | Published gRPC-Web contract consumption (Connect Kotlin client, binary framing, session/stream/retry adapters) | feature | M | [AND.02](#task-and-02) (artifact), [CON.07](contracts.md#task-con-07) (contract), [CON.11](contracts.md#task-con-11) (contract), [AND.01](#task-and-01) (artifact) | not-started |
| [AND.05](#task-and-05) | Room history, drafts, outbox and receipts | feature | L | [AND.02](#task-and-02) (artifact), [CON.11](contracts.md#task-con-11) (contract) | not-started |
| [AND.06](#task-and-06) | Secure per-account lifecycle: Keystore encryption, no-backup policy, purge/quarantine, deep-link validation | feature | M | [AND.03](#task-and-03) (artifact) | not-started |
| [AND.07](#task-and-07) | Foundation integration evidence: real candidate against deployed 22/23/24/25 | integration | M | [AND.03](#task-and-03) (artifact), [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact), [AND.06](#task-and-06) (artifact), [CLOUD.13](cloud.md#task-cloud-13) (artifact), [CLOUD.42](cloud.md#task-cloud-42) (artifact), [CLOUD.39](cloud.md#task-cloud-39) (artifact), [CLOUD.18](cloud.md#task-cloud-18) (artifact), [CLOUD.19](cloud.md#task-cloud-19) (artifact), [CLOUD.26](cloud.md#task-cloud-26) (artifact), [CLOUD.29](cloud.md#task-cloud-29) (artifact) | not-started |
| [AND.08](#task-and-08) | Authentication, Home and workspace (AN01-AN06) | feature | L | [AND.03](#task-and-03) (artifact), [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact), [AND.06](#task-and-06) (artifact) | not-started |
| [AND.09](#task-and-09) | Conversations and context (AN07-AN10/15/16) | feature | L | [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact) | not-started |
| [AND.10](#task-and-10) | Tasks, approvals and automation (AN11-AN13/19/25) | feature | L | [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact) | not-started |
| [AND.11](#task-and-11) | Library and resources (AN14-AN18/22) | feature | M | [AND.04](#task-and-04) (artifact), [AND.05](#task-and-05) (artifact) | not-started |
| [AND.12](#task-and-12) | Presence, push, links and settings (AN20-AN24) | feature | M | [CON.22](contracts.md#task-con-22) (contract), [AND.03](#task-and-03) (artifact), [AND.04](#task-and-04) (artifact), [AND.06](#task-and-06) (artifact) | not-started |
| [AND.13](#task-and-13) | Native interaction and recovery: full experience-02 device matrix | integration | L | [AND.08](#task-and-08) (artifact), [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact), [AND.11](#task-and-11) (artifact), [AND.12](#task-and-12) (artifact) | not-started |
| [AND.14](#task-and-14) | Scope and licence enforcement audit | acceptance | S | [AND.08](#task-and-08) (artifact), [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact) | not-started |
| [AND.15](#task-and-15) | Complete companion acceptance | integration | M | [AND.08](#task-and-08) (artifact), [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact), [AND.11](#task-and-11) (artifact), [AND.12](#task-and-12) (artifact), [AND.13](#task-and-13) (artifact), [AND.14](#task-and-14) (artifact) | not-started |
| [AND.16](#task-and-16) | Signed Android release artifacts (AAB + direct APK) | release | S | [AND.15](#task-and-15) (artifact) | not-started |
| [AND.17](#task-and-17) | Release runtime inspection | acceptance | S | [AND.16](#task-and-16) (artifact) | not-started |
| [AND.18](#task-and-18) | Dependency and source rights closure (final artifact) | acceptance | S | [AND.16](#task-and-16) (artifact) | not-started |
| [AND.19](#task-and-19) | Consumption-only enforcement | acceptance | M | [AND.08](#task-and-08) (artifact), [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact), [AND.11](#task-and-11) (artifact), [AND.12](#task-and-12) (artifact) | not-started |
| [AND.20](#task-and-20) | Play and direct-channel signed update client | feature | M | [CON.16](contracts.md#task-con-16) (contract) | not-started |
| [AND.21](#task-and-21) | Physical device and recovery gates | integration | L | [AND.16](#task-and-16) (artifact) | not-started |
| [AND.22](#task-and-22) | Android scope statement | acceptance | S | none | not-started |
| [AND.23](#task-and-23) | Distribution acceptance | release | M | [AND.17](#task-and-17) (artifact), [AND.18](#task-and-18) (artifact), [AND.19](#task-and-19) (artifact), [AND.20](#task-and-20) (artifact), [AND.21](#task-and-21) (artifact), [AND.22](#task-and-22) (artifact) | not-started |
| [AND.24](#task-and-24) | Real CF Harness generation/tool loop observed end to end on Android | integration | M | [AND.09](#task-and-09) (artifact), [AND.10](#task-and-10) (artifact), [HAR.00](harness.md#task-har-00) (artifact), [HAR.03](harness.md#task-har-03) (artifact) | not-started |
| [AND.25](#task-and-25) | Real desktop tool dispatch and unknown-effect reconciliation from Android | integration | M | [AND.10](#task-and-10) (artifact), [AND.13](#task-and-13) (artifact), [DEV.02](device-bridge.md#task-dev-02) (artifact), [DEV.03](device-bridge.md#task-dev-03) (artifact), [DEV.06](device-bridge.md#task-dev-06) (artifact), [DEV.07](device-bridge.md#task-dev-07) (artifact), [DEV.12](device-bridge.md#task-dev-12) (artifact) | not-started |
| [AND.26](#task-and-26) | Real FCM sending and physical Android receipt | integration | M | [AND.12](#task-and-12) (artifact), [AND.23](#task-and-23) (artifact), [OPS.10](operations.md#task-ops-10) (artifact), [AND.21](#task-and-21) (artifact) | not-started |

## Tasks

<a id="task-and-01"></a>

### AND.01 — Android production identity and stable toolchain reconciliation

**Outcome.** com.arcforges.mobile applicationId/namespace/source packages adopted, and a mutually compatible stable JDK21/AGP/Kotlin/Compose/Gradle tuple is pinned with wrapper checksums, version-catalog locks and generated-client compatibility evidence.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-01` and ledger record `ledger/tasks/and-01.md` in the Plan repository; task branch `task/and-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M · early risk proof |
| Obligations | [WP-30.00](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.00) — all work except the parts mapped to AND.04<br>[WP-30](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30) §3 binding rules: Apache-2.0 boundary, no GPL-family implementation, immutable producer artifacts — package-level obligation contribution |
| Provides | android-app-identity; android-stable-toolchain |
| Start prerequisites | **artifact** [PRF.10](runtime-proofs.md#task-prf-10) — immutable toolchain compatibility manifest (exact AGP/Kotlin/Compose/Gradle versions proven together on a real release build). *Why:* WP30.00 Follow-up F-1 must commit exact producer pins against a proven-compatible stack; the transport probe already runs in this repo's own CI (CloudHelloClient, F-023-evidenced candidates), so this is a recorded-manifest join, not a functional blocker |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.02](#task-and-02), [AND.04](#task-and-04) |
| Write scope | `Mobile:app/build.gradle.kts`<br>`Mobile:app/src/main/AndroidManifest.xml`<br>`Mobile:app/src/main/kotlin/**`<br>`Mobile:gradle/libs.versions.toml`<br>`Mobile:gradle/locks/**`<br>`Mobile:gradle/verification-metadata.xml`<br>`Mobile:gradle/wrapper/gradle-wrapper.properties`<br>`Mobile:eng/policy/**`<br>`Mobile:eng/provenance/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Windows/Linux full build, dependency-verification metadata check, package/certificate inspection under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017); device install and App Link fixture-key tests are local opt-in, not CI gates |
| Completion evidence | Exact pinned tuple + wrapper checksums + regenerated locks; [F-023](../../../assurance/open-gates-register.md#rule-f-023) re-run showing closure holds after the identity change |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: app/ is a Hello World module with applicationId io.github.arcforges.mobile (dev-prerelease id); shared/ is a Kotlin-Multiplatform module (android+desktop jvm targets) used only for a Compose Hot Reload preview per AGENTS.md, not a production target; CI already builds/signs/publishes real signed candidates (android-0.1.0-ci.14.1, [F-023](../../../assurance/open-gates-register.md#rule-f-023) closed for that candidate) which is de facto WP06 evidence |
| Notes | Must also decide the KMP shared/ preview module's fate: arch-27's module map (core/*, feature/*) has no KMP target, so shared/ stays a dev-only convenience outside the shipped app graph, never a second production plan (per WP30 §4). |

<a id="task-and-02"></a>

### AND.02 — Real Android module graph and AN01-AN25 route/state contracts

**Outcome.** The arch-27 module set (app, core/domain, core/data, core/network, core/security, core/designsystem, feature/home, feature/chat, feature/tasks, feature/library, feature/settings) exists as enforced Gradle modules with typed AN01-AN25 navigation/state contracts; features depend only on typed core ports.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-02` and ledger record `ledger/tasks/and-02.md` in the Plan repository; task branch `task/and-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-30.01](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.01) — full |
| Provides | android-module-boundaries; android-nav-contracts |
| Start prerequisites | **artifact** [AND.01](#task-and-01) — renamed applicationId/namespace and pinned toolchain. *Why:* new modules must be created under the production package identity, not the Hello dev id |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.03](#task-and-03), [AND.04](#task-and-04), [AND.05](#task-and-05) |
| Write scope | `Mobile:settings.gradle.kts`<br>`Mobile:build.gradle.kts`<br>`Mobile:core/domain/**`<br>`Mobile:core/data/**`<br>`Mobile:core/network/**`<br>`Mobile:core/security/**`<br>`Mobile:core/designsystem/**`<br>`Mobile:feature/home/**`<br>`Mobile:feature/chat/**`<br>`Mobile:feature/tasks/**`<br>`Mobile:feature/library/**`<br>`Mobile:feature/settings/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (exclusive) |
| Validation | Architecture/import boundary tests (no React Native/iOS/AGPL imports, no cross-module leakage) as offline static checks; targeted offline unit tests per module |
| Completion evidence | Module dependency graph report showing one-way core<-feature<-app dependencies; route ID inventory matching AN01-AN25 |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: Only app/ and the KMP shared/ preview module exist today; none of the arch-27 core/* or feature/* modules exist |

<a id="task-and-03"></a>

### AND.03 — Android runtime and OS adapters (Compose, Credential Manager, Keystore wrapper, WorkManager, FCM registration, SAF/MediaStore)

**Outcome.** arm64 release / x64 emulator adapters for Compose, Credential Manager/passkey fallback, Keystore, WorkManager, FCM with non-GMS fallback, and SAF/MediaStore/FileProvider exist in core/security, core/data and core/network, with no unsafe fallback path.

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
| Write scope | `Mobile:core/security/**`<br>`Mobile:core/data/**`<br>`Mobile:core/network/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Targeted offline unit tests for adapter contracts; install-on-real-device, permission-refusal, process-death and missing-Play-services scenarios are local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), not CI |
| Completion evidence | Adapter test matrix (permission refusal, process death, missing Play services, callback after account switch) with device identity recorded for local runs |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No Credential Manager/Keystore/WorkManager/FCM/SAF integration exists yet; only plain OkHttp networking in the Hello probe |
| Notes | Can proceed in parallel with AND.04 (core/network gRPC client) and AND.05 (Room, core/data) once AND.02's skeleton lands; they touch different files within shared modules so should be sequenced as short-lived parallel PRs, not serialized. |

<a id="task-and-04"></a>

### AND.04 — Published gRPC-Web contract consumption (Connect Kotlin client, binary framing, session/stream/retry adapters)

**Outcome.** core/network wraps the pinned contracts-proto/contracts-connect-client Maven artifacts behind typed session/stream/retry/exact-value adapters, explicitly selecting binary gRPC-Web.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-04` and ledger record `ledger/tasks/and-04.md` in the Plan repository; task branch `task/and-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-30.03](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.03) — full<br>[WP-30.00](../../work-packages/30-mobile-shared-architecture.md#rule-wp-30.00) — Kotlin Android foundation real package consumption |
| Provides | android-grpc-web-client |
| Start prerequisites | **artifact** [AND.02](#task-and-02) — core/network module shell. *Why:* client wiring lives in this module<br>**contract** [CON.07](contracts.md#task-con-07) — io.github.arcforges:contracts-proto / contracts-connect-client Maven coordinates. *Why:* the generated client is the only legal way to speak the wire protocol; this is already published and pinned in gradle/libs.versions.toml (contracts=1.0.0-ci.60.1) so this is a real, already-available start input<br>**contract** [CON.11](contracts.md#task-con-11) — published ApplicationService/HistoryService/EventService Kotlin Connect clients. *Why:* the Android gRPC-Web contract layer consumes the application, history and event operations<br>**artifact** [AND.01](#task-and-01) — real, delivered outcome of AND.01 (Android production identity and stable toolchain reconciliation). *Why:* this integration exercises the real android production identity and stable toolchain reconciliation instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.21](cloud.md#task-cloud-21) — publicly deployed Cloud host serving the generated business RPC surface. *Why:* the completion gate requires real packaged-Maven-consumer-and-service/device evidence, i.e. a live endpoint; the client code itself only needs the published Maven package to be written and unit-tested |
| Unblocks | [AND.07](#task-and-07), [AND.08](#task-and-08), [AND.09](#task-and-09), [AND.10](#task-and-10), [AND.11](#task-and-11), [AND.12](#task-and-12) |
| Write scope | `Mobile:core/network/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Targeted offline codec/adapter unit tests; real device/service calls against a deployed Cloud host are local opt-in evidence, not a CI gate (matches CloudHelloClient's existing pattern) |
| Completion evidence | Real packaged Maven consumer + service/device call evidence with exact hashes/versions/device identity |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: CloudHelloClient.kt already demonstrates this exact pattern (ProtocolClient, GRPC_WEB, OkHttp transport, error-code mapping) for the single Hello RPC; needs generalizing to the full session/stream/retry surface |
| Notes | Merged duplicate integration or closure task formerly proposed as CON.97. |

<a id="task-and-05"></a>

### AND.05 — Room history, drafts, outbox and receipts

**Outcome.** Room schemas (local_schema, scope_partition, projection, draft, outbox, transfer, cursor, preferences) implement per-profile partitions with a durable, bounded, never-silently-evicted outbox; local canonical history is not evictable cache.

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
| Write scope | `Mobile:core/data/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Offline Room migration/instrumented-on-emulator-or-device tests for crash recovery, capacity refusal and atomic outbox writes; local opt-in for real-device runs under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Migration test results; outbox capacity-refusal and awaitingReconciliation replay tests; no silent eviction of draft/outbox rows |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: No Room dependency or schema exists in the repo yet |
| Notes | Fully local; remote Task/AI content reconciled through this store may use named fixtures until WP31/52 per the producer matrix ("Task/AI fixture allowed only until 31+52"), but the store/journal/outbox mechanics themselves must be real now. |

<a id="task-and-06"></a>

### AND.06 — Secure per-account lifecycle: Keystore encryption, no-backup policy, purge/quarantine, deep-link validation

**Outcome.** Per-account Keystore-encrypted secret/pending-store policy, session/logout/revoke purge vs unsent-work quarantine/export, same-generation deep-link validation and current-foreground consent are implemented in core/security.

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
| Write scope | `Mobile:core/security/**` |
| Validation | Offline unit tests for encryption/purge/quarantine logic; device-restore-without-key, logout-while-requests-run, deep-link-spoof and secret-scan-of-release-logs are local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Secret scan of release logs/backup showing no credential leakage; device restore and logout-while-in-flight scenario results |
| Baseline (unreviewed unless accepted) | not-started |

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
| Start prerequisites | **artifact** [AND.03](#task-and-03) — OS adapters complete. *Why:* candidate needs full local capability set<br>**artifact** [AND.04](#task-and-04) — gRPC-Web client complete. *Why:* candidate needs real network layer<br>**artifact** [AND.05](#task-and-05) — Room store complete. *Why:* candidate needs real local persistence<br>**artifact** [AND.06](#task-and-06) — secure lifecycle complete. *Why:* candidate needs real session/secret handling<br>**artifact** [CLOUD.13](cloud.md#task-cloud-13) — deployed identity/session service. *Why:* sign-in must be real<br>**artifact** [CLOUD.42](cloud.md#task-cloud-42) — deployed R2/sync/hydration. *Why:* upload/reconnect must be real<br>**artifact** [CLOUD.39](cloud.md#task-cloud-39) — deployed guarded publication and convergent bootstrap. *Why:* the Android foundation integration evidence exercises real hydration and sync against deployed Cloud authority<br>**artifact** [CLOUD.18](cloud.md#task-cloud-18) — real, delivered outcome of CLOUD.18 (Independent native session integration (Platform client primitives)). *Why:* this integration exercises the real independent native session integration (Platform client primitives) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.19](cloud.md#task-cloud-19) — real, delivered outcome of CLOUD.19 (Browser cookie-session adapter and full account-surface closure). *Why:* this integration exercises the real browser cookie-session adapter and full account-surface closure instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.26](cloud.md#task-cloud-26) — real, delivered outcome of CLOUD.26 (Generated C#/TypeScript/Kotlin clients against Identity/Workspace/Device). *Why:* this integration exercises the real generated C#/TypeScript/Kotlin clients against Identity/Workspace/Device instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.29](cloud.md#task-cloud-29) — real, delivered outcome of CLOUD.29 (Stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells)). *Why:* this integration exercises the real stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells) instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.08](#task-and-08), [AND.09](#task-and-09), [AND.10](#task-and-10), [AND.11](#task-and-11), [AND.12](#task-and-12), [CLOUD.28](cloud.md#task-cloud-28) |
| Write scope | `Mobile:app/**` |
| Validation | Clean-cache restore/build/install on a real device is local opt-in evidence per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017); CI only runs the offline/static portion |
| Completion evidence | Owned-artifact-and-real-integration receipt: source commit, producer versions, candidate hashes, actual device identity, scenario, result, real-vs-fixture status per field |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as CLOUD.60. |

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
| Completion prerequisites | **integration** [AND.07](#task-and-07) — foundation candidate proven against the deployed Cloud services. *Why:* the feature can be built on the foundation modules, but its acceptance runs against the deployed services AND.07 proves and requires any remaining Task/AI fixtures compiled out |
| Unblocks | [AND.13](#task-and-13), [AND.14](#task-and-14), [AND.15](#task-and-15), [AND.19](#task-and-19) |
| Write scope | `Mobile:feature/home/**`<br>`Mobile:app/**` |
| Validation | Instrumented UI tests offline where feasible; scope/permission, wrong/stale target, loss/retry and expiry scenarios against real WP22/23 are local opt-in |
| Completion evidence | Full account/attention path walkthrough against real Cloud endpoints |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Does not need WP26 (remote bridge), WP45 (push sender) or WP52 (Harness) to start or complete — only WP30's own foundation and the already-deployed WP22/23. Demonstrates that not all Android features wait on the complete Harness. |

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
| Completion prerequisites | **integration** [AND.24](#task-and-24) — real CF Harness admission/generation/tool loop. *Why:* the completion gate requires every conversation/project/retrieval row to work with actual WP52 outputs; the streaming/cursor/reconnect UI itself can be fully built and tested against the server-side contract-bound fixture turn endpoint (introduced WP17.01, deleted WP52.05) that already runs in the real deployed Cloud host<br>**integration** [AND.07](#task-and-07) — foundation candidate proven against the deployed Cloud services. *Why:* the feature can be built on the foundation modules, but its acceptance runs against the deployed services AND.07 proves and requires any remaining Task/AI fixtures compiled out |
| Unblocks | [AND.13](#task-and-13), [AND.14](#task-and-14), [AND.15](#task-and-15), [AND.19](#task-and-19), [AND.24](#task-and-24) |
| Permitted substitutes | [SUB-fixture-turn-endpoint](../substitutes.md#sub-fixture-turn-endpoint) |
| Write scope | `Mobile:feature/chat/**` |
| Validation | Offline stream-codec/cursor unit tests; real-device streaming/reconnect scenarios against the deployed (fixture-backed until WP52.05) endpoint are local opt-in |
| Completion evidence | History/pending-input/stream/final-message consistency under every declared recovery outcome |
| Baseline (unreviewed unless accepted) | not-started |

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
| Write scope | `Mobile:feature/tasks/**` |
| Validation | Offline idempotency/state-machine unit tests; real bridge/Harness/commerce scenarios are local opt-in against deployed services |
| Completion evidence | One real owner outcome/settlement per command; no broad implicit grant or hidden background write |
| Baseline (unreviewed unless accepted) | not-started |

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
| Unblocks | [AND.13](#task-and-13), [AND.15](#task-and-15), [AND.19](#task-and-19) |
| Write scope | `Mobile:feature/library/**` |
| Validation | Offline transfer-journal unit tests; resumable-upload/hash-mismatch/process-death-during-transfer scenarios are local opt-in on real devices |
| Completion evidence | No unavailable bytes represented as empty success; resumable journal survives process death |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Independent of WP26/WP45/WP52 — can complete in parallel with AND.09/AND.10 once the foundation (AND.07) lands. |

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
| Write scope | `Mobile:feature/settings/**`<br>`Mobile:core/network/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Offline notification-dedup/registration unit tests; physical-device push receipt, Doze/background behavior and no-GMS fallback are local opt-in per [PG-24](../../../assurance/open-gates-register.md#rule-pg-24) |
| Completion evidence | Physical device receipt of a real push; denied-permission and no-GMS durable-polling fallback observed |
| Baseline (unreviewed unless accepted) | not-started |

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
| Unblocks | [AND.15](#task-and-15), [AND.25](#task-and-25) |
| Write scope | `Mobile:app/src/androidTest/**` |
| Validation | Physical low/mid-tier arm64 device matrix (1000 messages, 4 MiB answer, rotation, process kill during send/refresh/upload, denied push, airplane/reconnect, account switch, expired approval, revoked source) is local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Per-scenario pass/fail with device identity and TalkBack/IME/large-text results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-and-14"></a>

### AND.14 — Scope and licence enforcement audit

**Outcome.** Full companion requirements, consumption-only restrictions, public-Maven-only imports, and absence of desktop secrets/device-local paths/excluded professional-editing surfaces are verified with complete provenance.

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
| Start prerequisites | **artifact** [AND.08](#task-and-08) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.09](#task-and-09) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.10](#task-and-10) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.11](#task-and-11) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.12](#task-and-12) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.13](#task-and-13) — all WP31 substep tasks complete. *Why:* final join<br>**artifact** [AND.14](#task-and-14) — all WP31 substep tasks complete. *Why:* final join |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.16](#task-and-16) |
| Write scope | `Mobile:app/**` |
| Validation | Full physical-device release scenarios and injected failure matrix, local opt-in under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Owned-artifact-and-real-integration receipt joining all producer manifests; distribution/store activation explicitly deferred to WP32 |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-and-16"></a>

### AND.16 — Signed Android release artifacts (AAB + direct APK)

**Outcome.** AAB (Play) and a separately signed direct APK build automatically from reviewed main with monotonic versionCode, immutable provenance and tested WP03 update-schema compatibility.

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
| Write scope | `Mobile:.github/workflows/ci.yml`<br>`Mobile:eng/mobile.py` |
| Shared resources | [RES-android-signing-and-store](../shared-resources.md#res-android-signing-and-store) (append) |
| Validation | Actual signature/package/R8/runtime and version-monotonicity checks; clean device install/upgrade is local opt-in |
| Completion evidence | Signed AAB/APK with recorded provenance and monotonic versionCode |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: The full candidate-build-sign-publish pipeline already exists and runs on every merge to main (see.github/workflows/ci.yml build/publish jobs, eng/mobile.py sign/stage); this task extends it to the real companion and confirms WP03 update-schema compatibility, it does not build the pipeline from scratch |

<a id="task-and-17"></a>

### AND.17 — Release runtime inspection

**Outcome.** Kotlin/ART, Compose/public grpc-lite closure, min/target API, arm64 assets, R8 rules and required permissions are verified on the actual signed APK/AAB, not source inspection.

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
| Completion evidence | [VG-07](../../../assurance/open-gates-register.md#rule-vg-07) evidence: real Kotlin/ART release artifact inspection, not debug-only or source-only proof |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-and-18"></a>

### AND.18 — Dependency and source rights closure (final artifact)

**Outcome.** Direct/transitive Gradle/plugin/runtime/asset closure, licences, provenance and reproducible SBOM/NOTICE are audited against the final companion candidate; public schema/tooling Apache origin and independently original app implementation are verified.

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
| Validation | Forbidden-licence fixture, unpinned/dynamic dependency and changed-checksum rejection tests, offline |
| Completion evidence | [F-023](../../../assurance/open-gates-register.md#rule-f-023) re-closure for the final companion candidate (binary inventory matches candidate) |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: eng/licences.py, eng/check_provenance.py and the provenance-record set already implement this machinery and have closed [F-023](../../../assurance/open-gates-register.md#rule-f-023) twice for Hello-stage candidates; this task re-runs it against the real companion's larger dependency closure |

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
| Completion prerequisites | none |
| Unblocks | [AND.23](#task-and-23) |
| Write scope | `Mobile:eng/policy/**` |
| Validation | Static route/dependency checks ([MC-01](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-mc-01)..[MC-06](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-mc-06) build-time/CI assertions) plus all-state UX tests, offline where feasible |
| Completion evidence | [VG-13](../../../assurance/open-gates-register.md#rule-vg-13) evidence: no build path can display a purchase CTA or accept a licence key |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-and-20"></a>

### AND.20 — Play and direct-channel signed update client

**Outcome.** arch-11 channel behavior and a notify-only signed update client are complete, consuming WP03's format/fixture keys now; channel-switch export/reinstall guidance is explicit.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/and-20` and ledger record `ledger/tasks/and-20.md` in the Plan repository; task branch `task/and-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-32.04](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.04) — full |
| Provides | android-update-channels |
| Start prerequisites | **contract** [CON.16](contracts.md#task-con-16) — android-update.v1 feed format and fixture signing keys. *Why:* already available per the producer matrix ("No production key prerequisite; WP32/WP41 consume fixture roots") |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.23](#task-and-23) |
| Write scope | `Mobile:core/network/**`<br>`Mobile:feature/settings/**` |
| Shared resources | [RES-mobile-build-config](../shared-resources.md#res-mobile-build-config) (append) |
| Validation | Expired/rollback/wrong-certificate/URL/hash and offline-stale-feed tests, offline where feasible |
| Completion evidence | Play primary + direct APK flow complete with no silent install |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Explicitly does NOT wait on WP53 (production feed/signing) — [WP-32.04](../../work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.04)'s own text states WP53's replacement is verified at WP50, not a backward input to this task. |

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
| Start prerequisites | none |
| Entry condition | [ADOPT.10.android](adoption.md#task-adopt-10-android) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [AND.23](#task-and-23) |
| Write scope | `Mobile:README.md`<br>`Mobile:docs/**` |
| Validation | Store/release/readme/platform matrix cross-check against the signed Android artifact, offline |
| Completion evidence | No false retained-iOS deliverable or unsupported platform claim |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Small and independent; can land in the same PR series as AND.18 or AND.19 for convenience without being merged into them as one task. |

<a id="task-and-23"></a>

### AND.23 — Distribution acceptance

**Outcome.** The exact signed APK/AAB, manifest/hash/versionCode/certificate identity, compatible server/Contracts release and all gate receipts are archived and published through the automatic main graph; a clean-device download verifies signature/hash and exercises actual services.

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
| Completion evidence | Distribution complete only with real receipts; [VG-13](../../../assurance/open-gates-register.md#rule-vg-13) store-submission confirmation |
| Baseline (unreviewed unless accepted) | not-started |

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
| Completion prerequisites | none |
| Unblocks | [AND.10](#task-and-10), [AND.13](#task-and-13) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | an Android-initiated remote task actually reaches a desktop through the durable bridge with correct lease/grant/reconciliation semantics |
| Baseline (unreviewed unless accepted) | not-started |

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
| Unblocks | [AND.12](#task-and-12), [AND.23](#task-and-23), [OPS.10](operations.md#task-ops-10), [OPS.12](operations.md#task-ops-12) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | [PG-24](../../../assurance/open-gates-register.md#rule-pg-24): a project-bound FCM credential actually sends and a physical arm64 device actually receives, including duplicate/rotation/revocation and denied-permission/no-GMS recovery |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Merged duplicate integration or closure task formerly proposed as COM.17. |
