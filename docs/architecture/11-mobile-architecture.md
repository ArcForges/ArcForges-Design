# Mobile Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**/**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** (Apache-2.0 boundary), **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (Android React Native/Hermes; iOS build-deferred), **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)** (consumption-only), **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)** (runtime evidence)
> Companions: [`../requirements/products/arcchat-mobile-and-web.md`](../requirements/products/arcchat-mobile-and-web.md), [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md), [`08-security-architecture.md`](08-security-architecture.md)

---

## 1. Layering

```
RN native components / TurboModules                     platform UI
        ↓
Mobile Presentation (React hooks/state)          mobile-owned; NOT shared with desktop
        ↓
Mobile Application Services               mobile-only application behaviour
        ↓
Generated proto unary client + CF presentation adapter
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
| LY-01 | **Base ViewModel patterns are not shared between Avalonia desktop and React Native mobile** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). Each UI stack owns its implementation. |
| LY-02 | **Product-domain behaviour, server orchestration, policy decisions, persistence behaviour and entitlement authority stay outside the shared boundary** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| LY-03 | **Mobile-only application behaviour is implemented independently inside the Apache mobile boundary** (**[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| LY-04 | **The mobile client never loads the desktop native media stack and never connects to a local Hub**. |

---

## 2. Licence boundary

Everything in ArcForges-Mobile and the public contract and SDK projects it consumes is **Apache-2.0** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**).

| # | Rule |
|---|---|
| LB-01 | **ArcChat Mobile must not contain, link to, copy from, port from or reference any GPL-family or AGPL-only implementation**, directly or transitively. |
| LB-02 | **Automated architecture and dependency checks prevent GPL-family or AGPL-only source, project references, packages, generated artifacts and transitive dependencies from entering the distributable** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** obligation 7). |
| LB-03 | **The complete direct and transitive dependency closure is verified before the first artifact is produced** — the **[F-023](../assurance/open-gates-register.md#rule-f-023)** gate. *Owners: Release Engineering Owner and Licensing and Provenance Owner; Product Owner approves.* |
| LB-04 | **On discovering a conflicting contribution or dependency, the issue is registered and returned for decision.** Silently adding an exception, changing the licence or dropping the mobile target is prohibited (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |
| LB-05 | **No App Store exception, dual licensing, proprietary grant or CLA.** DCO continues with inbound-equals-outbound per scope. |
| LB-06 | **Protocol communication across an explicit process or network boundary does not change the client's licence** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |

---

## 3. Runtime, libraries and lifecycle baseline

Mobile is bare React Native 0.87.1 + React 19.3.0 + TypeScript 7.0.2 and bundled Hermes, New Architecture, no Expo baseline/MAUI/.NET mobile runtime. Node 24.21.0/npm 11.19.0 build only; one lock per TS repository. Android Gradle/Kotlin/SDK versions use the exact RN 0.87.1 template (SDK 37/Kotlin 2.2.0, AGP 9 opt-outs prescribed by RN); Android arm64 delivery, x64 emulator only; iOS source/profile present, build/store still deferred.

Select React Navigation native7.3.18/native-stack7.18.10, screens4.27.0/safe-area-context5.9.1; OP-SQLite18.2.1 for bounded account/realm cache/drafts/outbox; keychain10.0.0 for native token secure storage; passkey3.6.2 for Credential Manager/AuthenticationServices binding; RN Firebase app/messaging26.4.0 for Android push; native standard OS pickers/deep links. All license MIT/Apache-compatible. Foundation proof checks these exact packages under RN/Hermes and Android lifecycle before product work; no performance superiority claim.

Mobile tables: profile(realm,workspace,user), draft(conversationId,body,updatedAt), outbox(commandId PK,requestHash,typedProtoBytes,state,retryAt), acknowledged_message(messageId,rev,typedProtoBytes), sync_cursor(scope,cursor), app_meta(schemaVersion,sessionGeneration). One SQLite transaction records draft→queued command before sending; acknowledgment updates cache/removes outbox atomically; pending/unknown sends retain command identity. On process death restore pending queue then reconcile before resend; approval-expired decisions never auto-replay. Partition by realm/user; clear authorized views on signout/revoke, retain pending recovery only under explicit recovery flow. Credentials only Keychain/Keystore; no token in SQLite/AsyncStorage/logs. No custom encrypted notebook store.

Foreground: validate session/current generation → bounded unary Task/chat reconciliation → stream tail; background suspended, push carries opaque IDs only, never performs AI/tool work. Deep links parse allowlisted realm/route/IDs, no automatic approval or credential in URL. Long AI output virtualized, capped4 MiB live tail; Unicode byte offsets from wire profile. Explicit drafts survive connectivity loss and restart; synced messages replace presentation. Android acceptance on physical low/mid-tier arm64: cold/warm launch,1000-message list,4 MiB streamed answer, process kill during send/refresh, push disabled, airplane/reconnect, expired approval, permission revoke; retain existing numeric quality budgets and record measured RAM/frame/startup, no invented benchmark result.


**Preserved rule anchors.** These identifiers now resolve to the selected rules in this section: <a id="rule-rt-02"></a>RT-02 <a id="rule-rt-06"></a>RT-06 <a id="rule-rt-07"></a>RT-07 <a id="rule-rt-08"></a>RT-08.

---

## 4. Generated serialization and clients

Consume Apache @arcforges/proto/api-client/rn-transport from exact released npm artifacts. [The wire registry](contracts/04-protobuf-wire-registry.md) supplies protobuf fields, bigint/decimal/origin vectors and the selected unary binary gRPC-Web arrayBuffer adapter. Standard React Native fetch need not expose browser ReadableStream. [CF presentation](contracts/05-cloudflare-integration.md#5-live-presentation-and-client-recovery) supplies native WebSocket frames and HTTP catch-up. Credential headers use native secure storage; no C# assembly, desktop native package or AGPL Web application import enters Mobile.


**Preserved rule anchors.** These identifiers now resolve to the selected rules in this section: <a id="rule-sc-02"></a>SC-02.

---

## 5. Network behaviour

| # | Rule |
|---|---|
| <a id="rule-nw-01"></a>NW-01 | All business commands and queries use generated binary unary gRPC-Web. CF WebSocket/HTTP stream reads carry presentation; file/auth/provider exceptions retain their declared HTTP protocol. |
| NW-02 | **Foreground and background transitions rebuild or restore the realtime session per platform policy.** |
| NW-03 | **Network changes use exponential backoff with jitter.** |
| NW-04 | **After reconnection, durable state is backfilled by generated unary RPC; CF presentation gaps use the declared HTTP catch-up** ([RL-04](05-cloud-architecture.md#rule-rl-04) in the cloud architecture). |
| NW-05 | **The client never scans a LAN, never discovers a desktop Hub, and never addresses a named pipe or socket** (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |
| NW-06 | **Cellular policy is respected** for downloads and large transfers ([AR-09](../requirements/products/arcchat-mobile-and-web.md#rule-ar-09) in the companion requirements). |

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
| OB-01 | **The outbox is durable**, surviving process termination. |
| OB-02 | **Every write retry obeys `CommandId` idempotency** ([ID-01](../requirements/05-ai-and-agent-execution.md#rule-id-01) in the AI requirements). |
| OB-03 | **A high-risk agent task is never automatically executed on reconnection** ([OF-02](../requirements/products/arcchat-mobile-and-web.md#rule-of-02) in the companion requirements). |
| OB-03a | **An unrecognised Task state renders as an unknown non-terminal state with its reason text** ([TS-01](contracts/01-public-api-operations.md#rule-ts-01) of the public API contract), never as failed and never as absent. Mobile ships on store timelines and is routinely older than the Cloud host, so this is the normal case, not an edge one. |
| OB-04 | **Offline caching is restrained and bounded**: recent task state, recent conversation summaries, pending attention items and small previews ([OF-01](../requirements/products/arcchat-mobile-and-web.md#rule-of-01) there). |
| OB-05 | **Acknowledged projection/preview caches are evictable and never authoritative. Unsent drafts and pending/unknown commands are durable user work and are never cache-evicted.** |

---

## 7. Secure storage

| # | Rule |
|---|---|
| SS-01 | **Session material uses the platform secure storage** — keychain or keystore. |
| SS-02 | **Sensitive tokens never enter ordinary preferences or logs**. |
| SS-03 | **No provider credential exists on any client, desktop or mobile** ([BY-01](../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04)). |
| SS-04 | **App lock is UI access protection, not authentication** ([I-277](../requirements/01-normative-glossary-and-invariants.md#rule-i-277)); biometric unlock never substitutes for step-up ([I-278](../requirements/01-normative-glossary-and-invariants.md#rule-i-278)). |
| SS-05 | **Provider credentials are held only by their designated C# or CF service deployment** ([DC-15](../requirements/11-policy-and-configuration.md#rule-dc-15)), used server-side and never projected to any client ([DC-14](../requirements/11-policy-and-configuration.md#rule-dc-14)). |

---

## 8. Push and deep links

| # | Rule |
|---|---|
| <a id="rule-pd-01"></a>PD-01 | **A push registration is per device and per installation**, revocable with the device. |
| <a id="rule-pd-02"></a>PD-02 | **A push notification is not durable attention state** ([NT-07](../requirements/products/arcchat-mobile-and-web.md#rule-nt-07) in the companion requirements). Missing a push never loses a pending approval. |
| <a id="rule-pd-03"></a>PD-03 | **A push action opens the corresponding surface; it never carries authorization** ([AD-01](../requirements/07-security-privacy-and-trust.md#rule-ad-01) in the security requirements). |
| PD-04 | **Lock-screen content is non-sensitive by default** ([NT-03](../requirements/products/arcchat-mobile-and-web.md#rule-nt-03) there). |
| PD-05 | **Universal/app links are supported** so an HTTPS canonical URL opens the installed application ([LN-02](../requirements/products/arcchat-mobile-and-web.md#rule-ln-02) in the companion requirements). |
| PD-06 | **A deep link is treated as untrusted input** and never carries a secret ([DL-02](../requirements/09-shared-desktop-experience.md#rule-dl-02), [DL-03](../requirements/09-shared-desktop-experience.md#rule-dl-03) in the shared desktop requirements). |

---

## 9. Commerce constraints in the build

**[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, confirmed by **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)**, produces build-verifiable constraints.

| # | Rule |
|---|---|
| <a id="rule-mc-01"></a>MC-01 | **No purchase surface exists in any build path.** |
| MC-02 | **No provider checkout is embedded.** |
| MC-03 | **No store billing integration for the initial release.** |
| MC-04 | **No external purchase button, link or call to action exists.** |
| <a id="rule-mc-05"></a>MC-05 | **No licence-key or purchase-token unlock path exists** — the prohibition most likely to be violated by accident, since it is a natural engineering shortcut for offline entitlement. |
| <a id="rule-mc-06"></a>MC-06 | **A build-time and CI check asserts [MC-01](#rule-mc-01) through [MC-05](#rule-mc-05)** ([MB-03](../requirements/04-commerce-entitlement-and-credits.md#rule-mb-03) in the commerce requirements). |
| MC-07 | **The entitlement architecture remains capable of accepting a future store-originated grant**, without implementing one ([MB-02](../requirements/04-commerce-entitlement-and-credits.md#rule-mb-02) there). |

---

## 10. Placement constraints

| # | Rule |
|---|---|
| PL-01 | **Mobile never loads executable extensions** (`PL-01` in the extension requirements). |
| PL-02 | **Content packages — skills, templates, workflows — may sync; executable packages do not** (`PL-02` there). |
| PL-03 | **Mobile holds no professional product's writable domain state** ([OM-02](../requirements/products/arcchat-mobile-and-web.md#rule-om-02) in the companion requirements). |
| PL-04 | **Complex configuration surfaces — advanced automation policy, MCP configuration, skill authoring — live on desktop and web** (`§13`, `§14` there). |

---

## 11. Platform integration surface

| Concern | Handling |
|---|---|
| Lifecycle | Foreground, background, suspended and resumed states drive realtime session and outbox behaviour |
| Permissions | Requested just-in-time with clear purpose; declined permissions degrade gracefully |
| Notifications | Registered on sign-in, revoked on sign-out and on device revocation |
| Background work | Bounded to platform allowances; no attempt at long-running background execution |
| Secure storage | Platform-native |
| Biometrics | App lock only |
| Sharing | Receiving shared content creates ordinary attachments or context references |
| Files | Downloads and exports use platform-appropriate file handling |

All platform integrations are **mobile-only libraries inside the Apache boundary** (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**).

---

## 12. Testing and release gates

| # | Gate |
|---|---|
| MT-01 | Real-device verification, not emulator-only ([PM-03](../requirements/12-quality-and-compatibility-contract.md#rule-pm-03) in the quality contract) |
| MT-02 | The signed RN/Hermes release artifact built by CI and smoke-tested on device |
| MT-03 | Cold-start, memory and weak-network behaviour measured against budget |
| MT-04 | Background resume with realtime reconnection and sequence backfill |
| MT-05 | Offline queueing, pending state and controlled reconnection behaviour |
| MT-06 | The licence and dependency-closure audit — the **[F-023](../assurance/open-gates-register.md#rule-f-023)** gate |
| MT-07 | Store category-fit and consumption-only conformance — the **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** gate |
| MT-08 | The commerce-prohibition build check ([MC-06](#rule-mc-06)) |
| MT-09 | Accessibility verification with the platform's assistive technology |
| MT-10 | Contract compatibility against the supported client window |

---

## 13. Non-goals

Mobile is **not**: an ArcNotes, ArcScope or ArcSlate editor; a general screen-and-input remote desktop; a route that bypasses the ArcChat trust model; a way to perform R4 operations without local presence; a holder of desktop-local secrets; a commerce surface; or a host for executable extensions.

---

## 14. Traceability

| Current document | Relationship |
|---|---|
| [ArcChat Mobile and ArcChat Web — Product Requirements](../requirements/products/arcchat-mobile-and-web.md) | Owns mobile companion scope, continuity, remote controls and exclusions |
| [Realtime Events and the Durable Bridge](contracts/03-realtime-and-bridge.md) | Defines the Cloud-facing remote and realtime contract |
| [Product Quality and Compatibility Contract](../requirements/12-quality-and-compatibility-contract.md) | Owns platform, compatibility and runtime acceptance |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)**, **[F-023](../assurance/open-gates-register.md#rule-f-023)** | The Apache boundary, no shared ViewModels, and the pre-distribution provenance gate |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)** | Android React Native/Hermes as the production baseline; iOS build-deferred; the framework-upgrade re-verification gate |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Mobile connects only to Cloud |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** | Consumption-only constraints made build-verifiable |
| **[F-026](../assurance/open-gates-register.md#rule-f-026)** | Generated public clients and the selected AOT/native and RN transport gates |

## 15. Mobile repository, screens and execution state

All following paths are relative to ArcForges-Mobile. package.json/package-lock.json pin the selected public npm artifacts and RN template; android/ owns the Gradle app and Kotlin adapters; ios/ contains the matching iOS template/adapter sources with build and distribution disabled. src/app/ owns boot, account/realm gate, typed navigation and dependency construction; src/features/{auth,conversations,tasks,approvals,artifacts,devices,settings}/ own React screens and mobile application behavior; src/services/ owns generated RPC composition, session refresh, CF presentation and reconciliation; src/storage/ owns SQL migrations, drafts/outbox and bounded projections; src/platform/ owns secure storage, passkey, push, links, pickers and lifecycle adapters. tests/{unit,contract,device}/ and eng/{policy,release,verification}/ belong to this repository. There are no mobile csproj/XAML/handlers/Mono properties, shared desktop ViewModels or DesktopPlatform package dependencies.

Navigation has an authentication stack followed by four tabs: Conversations, Tasks, Devices, Settings. Conversation detail, task detail, approval and artifact preview are nested routes with stable IDs; tab state never defines a server identity. Resume/deep-link first resolves the account/realm gate, then queries current permission before opening the target. An unavailable target renders a recoverable reason, not an empty successful view.

| Surface | Required behavior and selected boundary |
|---|---|
| Server profile, sign-in, recovery | Validate an HTTPS realm profile; passkey/email flows use identity.beginAuthentication/completeAuthentication, requestEmailCode/redeemEmailCode and recovery operations. Platform passkey adapter returns the exact WebAuthn fields; native opaque session handles are stored only in secure storage. No CF login identity. |
| Workspace and installation binding | workspace.list/get; device.register/list and heartbeat bind the installation. Switching workspace increments the session generation, clears old visible projections and reopens its own partition; previous pending commands cannot be sent into the new scope. |
| Conversation list and detail | chat.listConversations/getConversation/createConversation/createBranch, paginated virtualized messages, branch selection, Markdown/code and typed attachments with content-origin display. Composer supports slash commands, context references and model/mode/profile choices from agent.listModels/listProfiles plus current public policy. No mobile skill/MCP authoring. |
| Send and live output | chat.appendMessage carries the stable message ID, command ID, typed draft and optional turn options. Render the returned Task identity immediately; display CF live/catch-up by stream ID/byte offset, then replace the tail from canonical chat/task reads. Partial model text is visibly partial until a committed final message exists. |
| Task list/detail | task.list/get display run, step, tool, progress and blocking reason; cancel/pause/resume/retryAttempt/steer carry the current revision, command ID and required reconciliation/approval state. Unknown future nonterminal states keep their server reason and disable unsupported mutations. |
| Approvals and attention | approval.list/decide and notification.list/acknowledge show proposal, scope, target, risk, expiry and budget impact before confirmation. Stale proposal/revision reopens current approval; local-presence-required actions explain the required desktop step. A push never decides approval. |
| Artifacts | resource.getMetadata/getDownloadTicket and export.getStatus/getDownload lead to the authenticated CF object facade. Show accepted Notes excerpts/PDF, Scope chart/table/measurement and Slate image/audio/video/result previews in bounded read-only viewers. No professional editing or executable content. Verify resource version and authorized range; cellular policy and OS file picker/share sheet control downloads. |
| Devices | device.list plus durable polling shows honest last-known/offline/presence and remote eligibility. Select a desktop target in turn input; phone device registration never makes it a desktop tool host. |
| Settings and account | Show identity, workspace, entitlement.getSnapshot/getUsage/getCapacity and agent.getUsage; notification, cellular, app-lock, appearance/language and bounded cache controls are mobile settings. Approved account/security/support link-outs use the canonical portal routes and the consumption-only allowlist; no checkout, purchase CTA or hidden unlock. Sign-out invokes revokeSession/unregisterPush when reachable and always clears local credentials/generation. |

Every screen implements loading, empty, denied, expired, offline, unavailable-content and recoverable-error states where applicable, showing server reason/recovery actions in localized user terms. Accessibility labels, focus restoration, dynamic text and screen-reader navigation are part of every slice, not a final styling task. Account-free boot shows the shell/server profile; a hydrated offline session shows bounded cached conversations/tasks and durable drafts without pretending Cloud actions succeeded.

SQLite stores exactly the selected public proto bytes and explicit local metadata, not desktop domain tables. Migrations run atomically with schemaVersion before account services start; failure leaves the prior database intact and offers diagnostics/recovery. Cache-only rows may be rebuilt, but migration never drops a draft/outbox as repair. Projection/preview cache capacity follows the signed client policy and remains bounded by its existing quality envelope; eviction uses LRU among acknowledged unpinned rows only. Storage full refuses a new queued send before transmission and preserves existing work.

Outbox state is draft (not in send queue), queued, sending, awaitingReconciliation or blocked. User Send atomically persists commandId, exact proto input, requestHash, messageId/taskId when known, realm/user/workspace and session generation before network I/O. A successful receipt updates acknowledged projections and removes the item in one transaction. Timeout, process death or lost response moves sending to awaitingReconciliation; use chat.getConversation and task.get for known identities, then replay the exact command ID/input only where the public idempotency class permits. That replay returns the stored dedup result if already committed; no invented generic command-status endpoint is required. Never allocate a new ID merely to recover a lost acknowledgement. A stale revision or changed policy blocks the item for explicit user action. Ordinary already-queued messages may resume; high-risk Task/approval/steering decisions require renewed explicit foreground confirmation. Drafts stay drafts until Send.

Refresh is single-flight per session generation. Expiry, sign-out, revoke, realm/workspace switch increment generation before cancelling in-flight callbacks; late results cannot populate or mutate the replacement session. Offline inability to refresh does not itself erase an authorized cache/draft; explicit revocation clears accessible protected projections and isolates pending recovery for the same owner after reauthentication. UI session expiry does not cancel a server-owned durable Task. Background stops polling/live delivery; foreground revalidates and reconciles before joining a new one-use CF stream nonce. Push payloads contain opaque IDs only; notification permission denial remains fully functional through durable attention.

Implementation sequence is fixed: foundation dependency closure/import gate → RN template and native runtime proof → generated transport/session → SQL/outbox → lifecycle/adapters → complete feature slices → real Cloud/CF/desktop loop → signed release, device/store/support/update gates. The first artifact proof in WP06 and all later dependency changes obey [F-023](../assurance/open-gates-register.md#rule-f-023); WP30 consumes that proof and WP32 repeats the final distributable closure. iOS has the same app/service/storage interfaces, AuthenticationServices/Keychain/APNs/app-link and file adapters, Apple signing/entitlements/store metadata and device matrix specified for future activation; no iOS build, submission or success is claimed now.
