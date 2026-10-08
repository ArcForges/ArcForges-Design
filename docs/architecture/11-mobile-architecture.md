# Mobile Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) (.NET MAUI Android; amends P2-010 in part, 2026-10-08), [P2-010](../decisions/phase-2-specification-decisions.md#rule-p2-010), [D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)/[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021) (Apache boundary), [D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022) (consumption-only companion).
> Companions: [`../requirements/products/arcchat-mobile-and-web.md`](../requirements/products/arcchat-mobile-and-web.md), [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md), [`08-security-architecture.md`](08-security-architecture.md)

---

## 1. Layering

```
.NET MAUI views / Android platform adapters                     platform UI
        ↓
Mobile Presentation (view-models with observable state)          mobile-owned; NOT shared with desktop
        ↓
Mobile Application Services               mobile-only application behaviour
        ↓
Generated C# proto unary/server-stream gRPC-Web client (Contracts NuGet SDK)
        ↓
Secure storage · Local cache · Offline outbox
```

| Shared with the rest of ArcForges | Not shared |
|---|---|
| Foundation, PublicApi and Realtime DTOs | Avalonia XAML |
| Contract-level validators expressing wire constraints | Desktop window and dispatcher concepts |
| Public protocol state semantics required for interoperability | Local RPC contracts |
| Generated public clients and handwritten bounded transport adapters | Desktop IPC |
| | Desktop native handles |
| | **Base ViewModel patterns** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**) |

| # | Rule |
|---|---|
| <a id="rule-ly-01"></a>LY-01 | **Base ViewModel patterns are not shared between Avalonia desktop and .NET MAUI Android mobile** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). Each UI stack owns its implementation. |
| <a id="rule-ly-02"></a>LY-02 | **Product-domain behaviour, server orchestration, policy decisions, persistence behaviour and entitlement authority stay outside the shared boundary** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| <a id="rule-ly-03"></a>LY-03 | **Mobile-only application behaviour is implemented independently inside the Apache mobile boundary** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| <a id="rule-ly-04"></a>LY-04 | **The mobile client never loads a desktop native library stack and never opens a desktop-local endpoint**. |

---

## 2. Licence boundary

Everything in ArcForges-Mobile and the public contract and SDK projects it consumes is **Apache-2.0** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**).

| # | Rule |
|---|---|
| <a id="rule-lb-01"></a>LB-01 | **Android companion must not contain, link to, copy from, port from or reference any GPL-family or AGPL-only implementation**, directly or transitively. The MAUI NuGet closure consumes only Apache-2.0 packages (such as the Contracts NuGet packages and the Microsoft and AndroidX bindings), verified by the [F-023](../assurance/open-gates-register.md#rule-f-023) gate, and never an AGPL DesktopPlatform package. The client layer `Communication/ArcForges.Cloud.Client` (AGPL DesktopPlatform tree) is not referenced by any MAUI build ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3). Naming an Apache-2.0 replacement, or re-homing the layer, is not decided by P2-021 and is open for [AND.40](../planning/delivery/lanes/android.md#task-and-40). The one time-limited exception is the build-only consumption of ArcForges.Build.Policy (AGPL) by this Apache-2.0 repository, which ends when AND.40 lands; AND.40's C# policy consumes no AGPL package. |
| <a id="rule-lb-02"></a>LB-02 | **Automated architecture and dependency checks prevent GPL-family or AGPL-only source, project references, packages, generated artifacts and transitive dependencies from entering the distributable** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** obligation 7). |
| <a id="rule-lb-03"></a>LB-03 | **The complete direct and transitive dependency closure is verified before the first artifact is produced** — the **[F-023](../assurance/open-gates-register.md#rule-f-023)** gate. *Owners: Release Engineering Owner and Licensing and Provenance Owner; Product Owner approves.* |
| <a id="rule-lb-04"></a>LB-04 | **On discovering a conflicting contribution or dependency, the issue is registered and returned for decision.** Silently adding an exception, changing the licence or dropping the mobile target is prohibited (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |
| <a id="rule-lb-05"></a>LB-05 | **No App Store exception, dual licensing, proprietary grant or CLA.** DCO continues with inbound-equals-outbound per scope. |
| <a id="rule-lb-06"></a>LB-06 | **Protocol communication across an explicit process or network boundary does not change the client's licence** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |

---

<a id="rule-rt-02"></a>
<a id="rule-rt-06"></a>
<a id="rule-rt-07"></a>
<a id="rule-rt-08"></a>
## 3. Runtime, libraries and lifecycle baseline

.NET MAUI on `net10.0-android` only implements the complete [companion requirements](../requirements/products/arcchat-mobile-and-web.md). The .NET 10 release runtime is Mono with AOT: `UseMonoRuntime=true` is explicit, and Android NativeAOT and CoreCLR stay experimental and unused until a later decision ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021), item 3). The .NET 11 runtime decision is open under [D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016) and is not settled here. Android arm64 is the delivered target, x64 emulator-only. The MAUI minimum API and compile/target API are deferred under [D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016) until [AND.40](../planning/delivery/lanes/android.md#task-and-40) records them from [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) evidence; the Kotlin-era values (minimum 26, compile and target 37) remain binding until AND.40 records a reviewed change under [D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016); [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3 records the owner, trigger, required evidence and failure consequence of that deferral. No iOS, macOS or other MAUI platform target, no KMP, no RN/Hermes/Node runtime and no shared desktop ViewModel is required. The target applicationId is `com.arcforges.mobile` ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3); the current development checkout still uses `io.github.arcforges.mobile`, and the reinstall from that development prerelease is described under Android identity below. The persistent android-release signing identity (certificate SHA-256 `7a8b3b14…`) is kept across the runtime replacement. versionCode strictly increases across the runtime replacement for the same applicationId and signing identity, and increases monotonically within each channel.

The Android producer selects one mutually compatible **stable** .NET toolchain: the .NET 10 SDK pinned in `global.json`, the .NET MAUI workload and the Android SDK platform pins, all committed with exact versions. The earlier stack's wrapper URL and SHA-256 pairing is not carried over. The integrity mechanism for these SDK, workload and platform installs is recorded by [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) in the immutable toolchain manifest; until PRF.12 records it, no install is claimed integrity-verified. Central package management (`Directory.Packages.props`) pins every direct NuGet dependency, and committed `packages.lock.json` locks pin the resolved graph. The Android adapters are AndroidX and .NET for Android bindings: WorkManager, Credential Manager, Biometric, Firebase Messaging (FCM), Android Keystore, storage access (SAF) and the local store binding, which [AND.40](../planning/delivery/lanes/android.md#task-and-40) owns (no engine is named by this document). Each is admitted as a dependency when its task needs it under [AND.40](../planning/delivery/lanes/android.md#task-and-40). Their exact compatible patch versions are recorded by [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) in the immutable toolchain manifest after a real release build; equivalent patch selection changes no product rule. An update PR changes the coherent toolchain, package and lock pins together and repeats affected tests. The earlier Kotlin/Gradle preview stack is historical input and is not a production approval.

Use async/await with structured cancellation (`CancellationToken`), immutable observable screen state, lifecycle-aware updates tied to the MAUI page lifecycle, repository-scoped background work and database transactions. A view-model owns presentation only. Losing a page or the Android activity does not allocate a second command or task. Foreground revalidates session/recoveryGeneration, reconciles durable owner state and then resumes authorized gRPC-Web streams. Background closes streams; bounded WorkManager work reconciles previously authorized uploads/messages under network constraints. It does not start model work, approve a proposal or run a desktop tool because the app resumed.

The intended mechanism is Mono AOT, trimming and R8 with `AndroidLinkTool=r8` ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3). The property name is snippet-sourced and the `AndroidR8ObfuscationMode` values are not yet verified; this is a provenance note only, and [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) owns the compatibility evidence. This candidate tuple has not been built by this documentation task; [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) and [AND.40](../planning/delivery/lanes/android.md#task-and-40) own actual compatibility evidence, and WP32 owns the signed artifact and store evidence.

<a id="rule-sc-02"></a>
## 4. Generated serialization and clients

Consume exactly the generated C# Contracts NuGet packages (protobuf messages and the gRPC-Web client SDK) from the same verified Contracts manifest. Generated C# messages and clients contain public schemas only. Mobile supplies the gRPC-Web handler, interceptors and bounded transport adapters; it never generates a private fork of proto or depends on adjacent Contracts source. Package consumption, trimming with R8 retention (`AndroidLinkTool=r8`) and release APK/AAB execution are tested, not inferred from unit tests. The Maven artifacts `contracts-proto` and `contracts-connect-client` retire after this consumer migrates ([CON.40](../planning/delivery/lanes/contracts.md#task-con-40)).

One generated C# client per authenticated application profile uses binary gRPC-Web (`application/grpc-web+proto`) over HTTPS through `Grpc.Net.Client.Web` on a `SocketsHttpHandler`, with system trust, bounded messages/deadlines and bearer metadata. This transport is intended and unverified: [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) observes the GrpcWebMode and media type for MAUI server streaming and records them with the fallback decision ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3). The Mobile loopback streaming fixtures are test-only characterisation and are not a substitute for the real producers [CON.11](../planning/delivery/lanes/contracts.md#task-con-11) and [CLOUD.29](../planning/delivery/lanes/cloud.md#task-cloud-29), which are completion edges. A custom Cloud realm uses an explicitly configured HTTPS origin; no trust-all callback. Refresh is single-flight and excluded from automatic business retries. Status/trailers map through ArcError; an HTTP failure does not prove an effect failed. The generated client implements gRPC-Web framing; there is no handwritten Android framing fork. Only file bytes, OAuth and provider adapters retain the [declared standard-protocol exceptions](contracts/05-cloudflare-integration.md). Event and AI output recovery use annex 10 RPCs.

Map signed 64-bit integers to `long` and protobuf `uint64` to `ulong` directly, with checked arithmetic at the application boundary. Preserve high-bit values and unsigned base10 JSON strings. Money decimals stay canonical strings with checked decimal arithmetic; UUID bytes are network order. Generated enums retain unknown values. Current/previous client vectors include uint64 max, negative ticks, absent/default fields, unknown enums, ArcError details, content origin, oversized/truncated bodies and canceled calls. The generated C# clients use the producer's generated protobuf messages and the explicit gRPC-Web protocol; no TypeScript or JavaScript runtime is embedded.

## 5. Network behaviour

| # | Rule |
|---|---|
| <a id="rule-nw-01"></a>NW-01 | Public gRPC-Web server streams use [the complete scope/stream contract](contracts/10-application-scope-and-streams.md); current authorization, CSRF/Origin, cursor recovery and bounded queues are required. |
| <a id="rule-nw-02"></a>NW-02 | **Foreground and background transitions rebuild or restore the realtime session per platform policy.** |
| <a id="rule-nw-03"></a>NW-03 | **Network changes use exponential backoff with jitter.** |
| <a id="rule-nw-04"></a>NW-04 | **After reconnecting, reread durable state with generated unary RPC and resume EventService.Watch/ExecutionService.WatchOutput at the last accepted cursor.** Expired retention takes the snapshot/reset path in [annex 10](contracts/10-application-scope-and-streams.md). |
| <a id="rule-nw-05"></a>NW-05 | **The client never scans a LAN, never discovers a desktop application runtime, and never addresses a named pipe or socket** (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |
| <a id="rule-nw-06"></a>NW-06 | **Cellular policy is respected** for downloads and large transfers ([AR-09](../requirements/products/arcchat-mobile-and-web.md#rule-ar-09) in the companion requirements). |

---

## 6. Offline outbox

```
User action while offline
 → validated locally
 → written to a durable outbox with an idempotency key
 → surfaced with an explicit pending state
 → on reconnection:
      ordinary messages explicitly queued by the user may send automatically; unqueued drafts remain drafts
      a high-risk agent task requires explicit confirmation
```

| # | Rule |
|---|---|
| <a id="rule-ob-01"></a>OB-01 | **The outbox is durable**, surviving process termination. |
| <a id="rule-ob-02"></a>OB-02 | **Every write retry obeys `CommandId` idempotency** ([ID-01](../requirements/05-ai-and-agent-execution.md#rule-id-01) in the AI requirements). |
| <a id="rule-ob-03"></a>OB-03 | **A high-risk agent task is never automatically executed on reconnection** ([OF-02](../requirements/products/arcchat-mobile-and-web.md#rule-of-02) in the companion requirements). |
| <a id="rule-ob-03a"></a>OB-03a | **An unrecognised Task state renders as an unknown non-terminal state with its reason text** ([TS-01](contracts/01-public-api-operations.md#rule-ts-01) of the public API contract), never as failed and never as absent. Mobile ships on store timelines and is routinely older than the Cloud host, so this is the normal case, not an edge one. |
| <a id="rule-ob-04"></a>OB-04 | **Offline caching is restrained and bounded**: recent task state, recent conversation summaries, pending attention items and small previews ([OF-01](../requirements/products/arcchat-mobile-and-web.md#rule-of-01) there). |
| <a id="rule-ob-05"></a>OB-05 | **Acknowledged projection/preview caches are evictable and never authoritative. Unsent drafts and pending/unknown commands are durable user work and are never cache-evicted.** |

---

## 7. Secure storage

| # | Rule |
|---|---|
| <a id="rule-ss-01"></a>SS-01 | **Session material uses the platform secure storage** — Android Keystore-backed encrypted storage. |
| <a id="rule-ss-02"></a>SS-02 | **Sensitive tokens never enter ordinary preferences or logs**. |
| <a id="rule-ss-03"></a>SS-03 | **No provider credential exists on any client, desktop or mobile** ([BY-01](../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)). |
| <a id="rule-ss-04"></a>SS-04 | **App lock is UI access protection, not authentication** ([I-277](../requirements/01-normative-glossary-and-invariants.md#rule-i-277)); biometric unlock never substitutes for step-up ([I-278](../requirements/01-normative-glossary-and-invariants.md#rule-i-278)). |
| <a id="rule-ss-05"></a>SS-05 | **Provider credentials are held only by their designated C# or CF service deployment** ([DC-15](../requirements/11-policy-and-configuration.md#rule-dc-15)), used server-side and never projected to any client ([DC-14](../requirements/11-policy-and-configuration.md#rule-dc-14)). |

---

## 8. Push and deep links

| # | Rule |
|---|---|
| <a id="rule-pd-01"></a>PD-01 | **A push registration is per device and per installation**, revocable with the device. |
| <a id="rule-pd-02"></a>PD-02 | **A push notification is not durable attention state** ([NT-07](../requirements/products/arcchat-mobile-and-web.md#rule-nt-07) in the companion requirements). Missing a push never loses a pending approval. |
| <a id="rule-pd-03"></a>PD-03 | **A push action opens the corresponding surface; it never carries authorization** ([AD-01](../requirements/07-security-privacy-and-trust.md#rule-ad-01) in the security requirements). |
| <a id="rule-pd-04"></a>PD-04 | **Lock-screen content is non-sensitive by default** ([NT-03](../requirements/products/arcchat-mobile-and-web.md#rule-nt-03) there). |
| <a id="rule-pd-05"></a>PD-05 | **Universal/app links are supported** so an HTTPS canonical URL opens the installed application ([LN-02](../requirements/products/arcchat-mobile-and-web.md#rule-ln-02) in the companion requirements). |
| <a id="rule-pd-06"></a>PD-06 | **A deep link is treated as untrusted input** and never carries a secret ([DL-02](../requirements/09-shared-desktop-experience.md#rule-dl-02), [DL-03](../requirements/09-shared-desktop-experience.md#rule-dl-03) in the shared desktop requirements). |

---

Use the [push.v1 profile](contracts/04-protobuf-wire-registry.md#android-push-provider-payload). Register only the current Android installation token; rotate on token changes, unregister on logout/permission loss. Deduplicate by realm/account/notificationId, display generic local HIGH-priority attention immediately, and fetch details through current authorization. No push supplies an approval credential. [PG-24](../assurance/open-gates-register.md#rule-pg-24) distinguishes provider acceptance, physical receipt and explicitly unavailable no-GMS/denied-permission background delivery.

## 9. Commerce constraints in the build

**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, confirmed by **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)**, produces build-verifiable constraints.

| # | Rule |
|---|---|
| <a id="rule-mc-01"></a>MC-01 | **No purchase surface exists in any build path.** |
| <a id="rule-mc-02"></a>MC-02 | **No provider checkout is embedded.** |
| <a id="rule-mc-03"></a>MC-03 | **No store billing integration for the initial release.** |
| <a id="rule-mc-04"></a>MC-04 | **No external purchase button, link or call to action exists.** |
| <a id="rule-mc-05"></a>MC-05 | **No licence-key or purchase-token unlock path exists** — the prohibition most likely to be violated by accident, since it is a natural engineering shortcut for offline entitlement. |
| <a id="rule-mc-06"></a>MC-06 | **A build-time and CI check asserts [MC-01](#rule-mc-01) through [MC-05](#rule-mc-05)** ([MB-03](../requirements/04-commerce-entitlement-and-credits.md#rule-mb-03) in the commerce requirements). |
| <a id="rule-mc-07"></a>MC-07 | **The entitlement architecture remains capable of accepting a future store-originated grant**, without implementing one ([MB-02](../requirements/04-commerce-entitlement-and-credits.md#rule-mb-02) there). |

---

## 10. Placement constraints

| # | Rule |
|---|---|
| <a id="rule-pl-01"></a>PL-01 | **Mobile never loads executable extensions** ([`PL-01`](../requirements/08-extensions-and-developer-platform.md#rule-pl-01) in the extension requirements). |
| <a id="rule-pl-02"></a>PL-02 | **Content packages — skills, templates, workflows — may sync; executable packages do not** ([`PL-02`](../requirements/08-extensions-and-developer-platform.md#rule-pl-02) there). |
| <a id="rule-pl-03"></a>PL-03 | **Mobile holds no professional product's writable domain state** ([OM-02](../requirements/products/arcchat-mobile-and-web.md#rule-om-02) in the companion requirements). |
| <a id="rule-pl-04"></a>PL-04 | **Complex configuration surfaces — advanced automation policy, MCP configuration, skill authoring — live on desktop and web** (`§13`, `§14` there). |

---

## 11. Platform integration surface

| Concern | Concrete Android behavior |
|---|---|
| Credential storage | AES-GCM key generated in Android Keystore; encrypted credential record in no-backup app-private storage with realm/user/installation as associated data. Rotation writes one atomic replacement; invalidated key requires reauthentication, never plaintext fallback. |
| Passkey | Credential Manager registration/authentication returns exact bounded WebAuthn records. Passkey behaviour through Credential Manager is unverified until [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) records passkey-on-MAUI evidence ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3). Unsupported device/provider offers the realm's email or other enabled method; never claims a passkey was registered. |
| OIDC | External browser/custom tab, PKCE and verified app link containing only a one-use flow receipt. Validate realm, state and original installation before redemption. |
| App lock | BiometricPrompt gates UI access; no session or step-up is minted. Background timeout locks sensitive views and screenshots in protected mode. |
| Push | FCM per installation registration via notification.registerPush. Logout/revoke unregisters when reachable and locally clears binding. No-GMS/permission denial uses durable notification polling and explicitly reports push unavailable. No sensitive lock-screen payload. |
| Links | Android App Links with verified assetlinks.json; typed route allowlist. Store pending route until authentication; requery permission, never auto-approve or cross-realm silently. |
| Sharing/attachments | ACTION_SEND/open-document grants are read once or explicitly persisted for an in-progress job. Stage an app-owned bounded copy, record hash/origin, and show upload purpose/maximum bytes. URI revocation leaves a recoverable attachment, not an invented Cloud resource. |
| Download/export | Storage Access Framework or MediaStore selected destination; authenticated download and full hash verification before atomic destination completion. FileProvider sharing grants read access only. Partial files retain job identity and never appear complete. |
| Permissions | Ask just in time for notification, microphone/camera or selected files when the user invokes that feature; refusal preserves text/file-picker alternatives. No broad storage permission for ordinary use. |
| Background/network | WorkManager unique work per owner/command, metered-network policy and bounded retry. No always-on foreground service or long-lived AI loop. Reboot resumes only eligible persisted work after session checks. |

All adapters are implemented within the Apache mobile boundary; dependency provenance is checked before distribution.

## 12. Testing and release gates

| # | Gate |
|---|---|
| <a id="rule-mt-01"></a>MT-01 | Real-device verification, not emulator-only ([PM-03](../requirements/12-quality-and-compatibility-contract.md#rule-pm-03) in the quality contract) |
| <a id="rule-mt-02"></a>MT-02 | The signed .NET MAUI Android release artifact (Mono AOT, trimmed and R8-shrunk) built by CI; relevant runtime/device observations are local opt-in and recorded separately under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| <a id="rule-mt-03"></a>MT-03 | Cold-start, memory and weak-network behaviour measured against budget |
| <a id="rule-mt-04"></a>MT-04 | Background resume with realtime reconnection and sequence backfill |
| <a id="rule-mt-05"></a>MT-05 | Offline queueing, pending state and controlled reconnection behaviour |
| <a id="rule-mt-06"></a>MT-06 | The licence and dependency-closure audit — the **[F-023](../assurance/open-gates-register.md#rule-f-023)** gate |
| <a id="rule-mt-07"></a>MT-07 | Store category-fit and consumption-only conformance — the **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** gate |
| <a id="rule-mt-08"></a>MT-08 | The commerce-prohibition build check ([MC-06](#rule-mc-06)) |
| <a id="rule-mt-09"></a>MT-09 | Accessibility verification with the platform's assistive technology |
| <a id="rule-mt-10"></a>MT-10 | Contract compatibility against the supported client window |

---

## 13. Non-goals

Mobile is **not**: an ArcScope editor; a general screen-and-input remote desktop; a route that bypasses the ArcChat trust model; a way to perform R4 operations without local presence; a holder of desktop-local secrets; a commerce surface; or a host for executable extensions.

---

## 14. Traceability

| Current document | Relationship |
|---|---|
| [Android companion and ArcChat Web — Product Requirements](../requirements/products/arcchat-mobile-and-web.md) | Owns mobile companion scope, continuity, remote controls and exclusions |
| [Realtime Events and the Durable Bridge](contracts/03-realtime-and-bridge.md) | Defines the Cloud-facing remote and realtime contract |
| [Product Quality and Compatibility Contract](../requirements/12-quality-and-compatibility-contract.md) | Owns platform, compatibility and runtime acceptance |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**, **[F-023](../assurance/open-gates-register.md#rule-f-023)** | The Apache boundary, no shared ViewModels, and the pre-distribution provenance gate |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)** | Android production baseline (the Kotlin/Jetpack Compose stack is replaced by .NET MAUI Android, [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021)); iOS and macOS outside scope; the framework-upgrade re-verification gate |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Mobile connects only to Cloud |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** | Consumption-only constraints made build-verifiable |
| **[F-026](../assurance/open-gates-register.md#rule-f-026)** | Generated public clients and the selected AOT/native and Android gRPC transport gates |

## 15. Mobile repository, screens and execution state

All paths are relative to Mobile. A `.slnx` solution, the .NET MAUI application project, `global.json` (pinned .NET 10 SDK), `Directory.Build.props`, `Directory.Packages.props` (central NuGet versions), `packages.lock.json` and the Android publish settings define the build. The application project's `Platforms/Android` folder and its feature, data and platform folders own boot/navigation, feature view-models and XAML pages, repositories, local database, network and Android adapters (AndroidX and .NET for Android bindings). The xUnit test projects contain deterministic domain, codec and client tests; device and emulator UI, storage and platform tests are local opt-in. `eng/` holds portable verification/release entry points. Hooks perform lightweight local checks; retained CI separately compiles/packages and runs applicable offline/static/security checks under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017). Hooks never silently invoke the full build or runtime tests. Git attributes/ignore, EditorConfig, licence/NOTICE/SECURITY/CONTRIBUTING/DCO, PR/issue templates, CODEOWNERS, Dependabot NuGet/Actions grouping, C# CodeQL, secret/dependency checks and branch-required verification are repository deliverables. The `.slnx` solution is required for this MAUI repository.

Navigation is authentication followed by **Home, Conversations, Tasks, Library, Settings**. Home is attention-first, including pending approvals, blocked/interrupted work and selected device status. Library contains projects, search, artifacts and simple automations; Settings contains devices/trust, account and preferences. Stable IDs identify nested routes; tab index never identifies an owner object. Every route has loading/empty/offline/denied/expired/missing/error states and localized recovery actions. Auth/realm/workspace change invalidates old callbacks before exposing a new partition.

| Surface / user action | Generated operation and required result |
|---|---|
| First run/server profile | Validate HTTPS realm and enabled identity providers; present sign-in/enrollment/recovery. No desktop is required for Cloud use. |
| Login/recovery/credential management | Purpose-bound flow in [client journeys](contracts/07-client-journeys-and-ports.md); passkey/email and advertised self-host methods. Session secret only in secure storage. Lost proof response requires fresh flow. |
| Home attention | notification.list and approval.list plus task.list filters; unread acknowledgement is independent from approval. Task/approval status is authoritative even when push was lost. |
| Conversation list/detail | chat.listConversations/getConversation/createConversation/createBranch; paged messages, project association, search/pin/archive/title controls through typed metadata operations. Branch ancestry and canonical final messages remain visible. |
| Ordinary/agent/temporary composer | chat.appendMessage with stable message/command IDs and explicit mode/profile/model/target/context. Result identifies ChatTurn or AgentTask. Temporary history is excluded, writes require explicit promotion to durable AgentTask. |
| Slash commands/context | Select from current descriptor/profile/model registries, materialize typed input and show unsupported/denied entries. A source selection pins owner revision and any explicit one-time consent; no implicit sync enrollment. |
| Stream/result | CF stream ID/UTF8-byte offset and catch-up; bounded 4 MiB live tail with virtualization. Reconcile final ChatTurn/task/message; partial text remains labelled and cannot become a success receipt. |
| Task detail/control | task.get and paged run/step/attempt/artifact details; cancel/pause/resume/retryAttempt/steer with expected revision. Show requested versus acknowledged control and unknown effect separately. Offline/high-risk control requires renewed foreground confirmation. |
| Approval | approval.decide only after current proposal/hash/revision/actor/target/risk/expiry/cost and device eligibility are shown. Changed preview refreshes; local-presence requirement opens instructions for the designated desktop. |
| Search | search.query with current source/authorization tokens and bounded pages. Results open permitted conversation/artifact/context previews; denied bodies do not leak through cached snippets. |
| Projects/memory | chat.listProjects/getProject/putProject/deleteProject and listMemories/getMemory/putMemory/deleteMemory. Simple project/context and inspect/delete memory are included; no advanced package authoring. |
| Simple automation | automation.list/get/create/update/setEnabled/delete/runNow/resolveMissed using accepted simple schedule and target/profile/context controls. Missed occurrence choices are explicit; background phone execution is not a scheduler. |
| Device status/selection | device.list and paged capability detail distinguish installed/running/ready/lastSeen. Phone is not a desktop tool host. Selected target enters the command; no silent device failover after dispatch. |
| Trust/grants | device.setTrust/setRemoteEnabled/getRemotePolicy/setRemotePolicy/revoke/signOut, scope grant operations from the journey registry, fresh step-up for authority expansion. Revocation invalidates pending work before any new dispatch. |
| Artifact previews | resource.getMetadata/getDownloadTicket and export.getStatus/getDownload; Scope chart/table/report, assistant image and text. Bounded read-only in-app viewers for images and text, no professional editing or executable attachment. An exported report PDF (`arcscope.report.pdf.v1`) is opened only through the Android system viewer (`ACTION_VIEW` intent). The handoff grant is not claimed here, because no authoritative rule at this commit defines a read-grant mechanism for it ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022) item 2); the origin sidecar travels with the PDF in the bundle; download and share of the full bundle follow the same containment ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022) item 2). Generic PDF attachments are opaque downloads with no parsing. The app contains no PDF parser, preview or renderer ([P2-022](../decisions/phase-2-specification-decisions.md#rule-p2-022)). |
| Handoff and transfer | Declared semantic handoff opens an owned target through Cloud/device policy; user-data export/realm transfer uses explicit preview/job status/download. Never screen/input remote control or silent copy of active task authority. |
| Capacity/credit consent | entitlement snapshot/usage/capacity, agent usage and existing extra-usage preference. Explain available/exhausted/unknown and the approved maximum. May authorize use of already-owned credits; no purchase, checkout link, billing SDK or unlock token. |
| Account/support | Profile/session/device management, deletion status/cancel flow, support cases/messages, data health and export. Purpose-restricted deletion session cannot operate ordinary content. |
| Preferences | Notification/cellular/app-lock/appearance/language/cache settings are mobile-local except explicitly shared user policy. Clear cache excludes unsent drafts and unknown commands. |

Local database tables (logical schema; [AND.40](../planning/delivery/lanes/android.md#task-and-40) owns the store binding): `local_schema(version)`, `scope_partition(realm,user,workspace,localGeneration,recoveryGeneration)`, `projection(ownerKind,ownerId,ownerRev,protoBytes,updatedAt,pinned)`, `draft(draftId,conversationId,mode,body,context,updatedAt)`, `outbox(commandId,requestHash,method,requestBytes,state,ownerIds,firstDispatchAt,reason)`, `transfer(jobId,resourceVersion,hash,parts,localUri,state)`, `cursor(streamId,offset,ownerRev)` and `preferences(key,typedValue)`. All scoped rows reference one partition. Secret credentials stay outside the database. Protect draft/outbox/transfer rows with app-private encryption at rest, exclude them from Android Auto Backup and offer the existing authenticated recovery/export route; no unsupported cross-device restore of refresh tokens.

Migration runs atomically before account services start. Failure preserves the prior database and offers diagnostics; cache rebuild never drops draft/outbox. Cache default 128 MiB, compiled maximum 512 MiB, LRU among acknowledged unpinned rows; actual memory budgets remain in the quality contract. Draft/outbox never silently evict: max 1000 queued items and 20 MiB text per partition, new work refuses visibly before transmission at capacity. Attachment bytes use the existing resource limits and explicit storage check.

Outbox states: draft (outside send queue), queued, sending, awaitingReconciliation, blocked. Send atomically writes commandId/exact request/hash/scoped identity before I/O. Receipt updates projection and removes queue item atomically. A lost response or process death marks awaitingReconciliation; query known owner then replay the identical command only within the declared idempotency window/current recoveryGeneration. Never allocate a new command to recover an unknown acknowledgement. Expired receipt/revision/policy requires owner reconciliation and explicit reapply. Ordinary queued messages may resume; approvals, high-risk task actions and steering need explicit foreground confirmation. Temporary chat drafts remain memory-only and are excluded from the local database, history and backup; closing temporary mode warns about loss and cancels its execution.

Refresh is single-flight per session generation. Invalidate local generation before canceling callbacks on logout/revoke/realm/workspace switch. Offline refresh failure does not erase a draft. Revocation clears accessible protected projections and quarantines pending work for the same owner after reauthentication. User sign-out offers explicit discard/export of pending work; it never silently sends it. UI expiry does not cancel a durable AgentTask.

Implementation is [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) MAUI transport/runtime proof (supersedes PRF.10) → [AND.40](../planning/delivery/lanes/android.md#task-and-40) complete MAUI foundation using the released Contracts NuGet SDK, current identity, events and R2 → WP31 full companion with WP52 CF and WP26 desktop → WP32 signed artifact/device/store/support. Every screen includes TalkBack labels/order, focus restoration, large text, keyboard where present and content-origin disclosure; physical low/mid-tier arm64 tests include 1000 messages,4 MiB answer, screen rotation, process kill during send/refresh/upload, denied push, airplane/reconnect, account switch, expired approval and revoked source.

## Release rescue and recovered realm

Android rollback follows the [forward rescue release](22-deployment-and-release-execution.md#partial-integration-manifests-and-mobile-rescue-release) with a greater versionCode and verified current-data compatibility. Session generation change quarantines queued commands before fresh bootstrap, using the same explicit recovery/reapply contract as Web and desktop. A transport retry never crosses a recovery generation automatically.

## Android publication and rescue

PR CI resolves locked dependencies, checks generated resources, runs targeted offline xUnit, .NET analyzer and C# CodeQL security checks and builds a release candidate. [P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 8 keeps the static and offline checks of the retired Kotlin app in substance, so the manifest and resource checks of the retired Kotlin release lint stay required in substance. This document names no MAUI tool for them. That replacement is an open item: owner, the Mobile lane responsible role of [AND.40](../planning/delivery/lanes/android.md#task-and-40); trigger, before AND.40 defines the Android PR CI gate; constraint, the check is static and offline, needs no device, emulator or hosted runtime ([P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017)), and covers the manifest and resource conditions that the retired release lint enforced, with warnings treated as errors. Until AND.40 records the replacement, no MAUI manifest or resource lint is claimed as retained. Emulator/device and live Cloud tests are local opt-in only under [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017). Main verifies the same gates, builds one signed APK/AAB pair from identical inputs, records APK/AAB hashes, signing-certificate digest, versionName/versionCode, toolchain and Contracts manifest, then publishes the immutable artifacts to the GitHub Releases archive and mirror automatically. GitHub Releases is not a distribution channel ([P2-013](../decisions/phase-2-specification-decisions.md#rule-ird-24) IRD-24). Store submission/promotion additionally requires WP32's account/listing/consumption-only and physical-device receipts; an uploaded artifact is not a Play-approved product.

The Android release checks that applied to the retired Kotlin app are re-proven for the MAUI closure ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021), item 3) by [PRF.12](../planning/delivery/lanes/runtime-proofs.md#task-prf-12) before the first release artifact, and are kept in the Android publication gate by [AND.40](../planning/delivery/lanes/android.md#task-and-40): (1) minified release through .NET trimming and R8 (`AndroidLinkTool=r8`), with the release build inspected for the runtime posture; (2) 16 KB page-size alignment of every native library in the MAUI release APK and AAB; (3) signed APK and AAB with the persistent android-release identity; (4) licence and provenance closure of the complete MAUI dependency graph, the [F-023](../assurance/open-gates-register.md#rule-f-023) gate; and (5) the F-023-class closure checks for the packaged artifact.

versionName follows the product release manifest; versionCode is an allocated monotonic integer in the repository release ledger, above every previously distributed code, including the historical React Native bootstrap release (a historical reference only). Re-run reuses the candidate or allocates a new code; no overwrite. CI signing keys live in protected repository environment secrets with backup/recovery ownership; they are not regenerated per build. Distribution signing identity and Play upload key are distinct when Play App Signing is used. A rescue release has a greater code, compatible current data and rollback-mode evidence. Never instruct users to downgrade database-bearing APKs in place.

## Complete native UX and application targeting

The [Android route/layout/action specification](../experience/02-android-companion.md) resolves the navigation inventory: Home, ArcScope, Chats, Tasks, Settings; Devices is nested under Home. It is normative for AN01–AN28 and native Back/IME/accessibility/lifecycle behavior. [Application scope](contracts/10-application-scope-and-streams.md) and [history modes](data-model/05-application-history.md) govern the local database, own chats, explicit desktop Cloud history and frozen one-application remote control. No local-only desktop history is remotely exposed.

## Android identity and release channels

Before the first production/Play upload, [AND.01](../planning/delivery/lanes/android.md#task-and-01) sets the application id, the namespace and the source namespace to `com.arcforges.mobile` (the IRD-23 / AND.01 target, consistent with IRC-30), and [AND.40](../planning/delivery/lanes/android.md#task-and-40) builds the MAUI project on that identifier. AND.01 also owns the reinstall guidance from the development prerelease. Until AND.01 changes the identifier, no release claims `com.arcforges.mobile`. Development prerelease installs under `io.github.arcforges.mobile` require reinstall; no same-package in-place migration from them is promised. Reinstalling under the new applicationId discards the previous installation's data, including its secure-storage data ([P2-021](../decisions/phase-2-specification-decisions.md#rule-p2-021) item 3). The coordinator disposition of 2026-10-08 is reinstall guidance with no data migration, because the development prereleases hold no production user data. The wording of that guidance is an AND.01 deliverable that is not yet written, and this document does not claim that pending local data is protected. Existing published prereleases stay as immutable history: their bytes, signatures and version codes are never replaced, re-signed or renumbered. The rename does not change the signing identity. Keep the exact .NET 10 SDK, MAUI workload and Android SDK pins in Mobile's committed `global.json`, central package file, lock and provenance manifests. No independent patch pins in Design. Android only; no iOS, macOS or Mac Catalyst deliverable, no KMP or Swift, and no RN/TS runtime.

Core modules own auth/system-browser PKCE, typed gRPC-Web transport, local database history/cache/outbox, secure storage, device/app targeting, notifications and signed update checks; feature modules own conversation/task/approval/target/settings UI. The same module map is in arch 27. Login and output-state tests use generated Contracts NuGet artifacts plus real Cloud; no TypeScript SDK implements the Android client.

Google Play is the primary production channel (AAB, Play App Signing). Direct distribution is a separately signed release APK from downloads.arcforges.com. Same package ID uses channel-specific signing policy; incompatible certificates cannot update one another. Switching channels requires explicit export/reinstall/import guidance and protects pending local data. Do not auto-uninstall or promise cross-signature migration. Each channel has a monotonically increasing versionCode, immutable artifacts and recorded signing fingerprint.

Direct APK checks updates at foreground start, at most once per 24h, against the signed android-update.v1 feed at updates.arcforges.com/android/stable.json. It notifies only; the user opens the verified HTTPS download and confirms Android's installer/source permission. No silent installation. Play uses store updates and never offers a direct APK as a bypass. Feed verification failure keeps the installed app usable and displays an actionable update error. WP03 owns format/fixtures, WP32 client/channel behavior, WP53 production feed/signing and WP50 actual integration.
