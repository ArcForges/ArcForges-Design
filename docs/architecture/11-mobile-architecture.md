# Mobile Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **D-004**/**D-021** (Apache-2.0 boundary), **D-008** (Android Mono AOT; iOS build-deferred), **D-022** (consumption-only), **V-04** (runtime evidence)
> Companions: [`../requirements/products/arcchat-mobile-and-web.md`](../requirements/products/arcchat-mobile-and-web.md), [`01-solution-and-project-layout.md`](01-solution-and-project-layout.md), [`08-security-architecture.md`](08-security-architecture.md)

---

## 1. Layering

```
MAUI Views / Handlers                     platform UI
        ↓
Mobile Presentation (ViewModels)          mobile-owned; NOT shared with desktop
        ↓
Mobile Application Services               mobile-only application behaviour
        ↓
Generated HTTP client  +  Realtime client
        ↓
Secure storage · Local cache · Offline outbox
```

| Shared with the rest of ArcForges | Not shared |
|---|---|
| Foundation, PublicApi and Realtime DTOs | Avalonia XAML |
| Contract-level validators expressing wire constraints | Desktop window and dispatcher concepts |
| Public protocol state semantics required for interoperability | Local RPC contracts |
| Generated and handwritten public clients | Desktop IPC |
| | Desktop native handles |
| | **Base ViewModel patterns** (**D-021**) |

| # | Rule |
|---|---|
| LY-01 | **Base ViewModel patterns are not shared between Avalonia desktop and MAUI mobile** (**D-021**). Each UI stack owns its implementation. |
| LY-02 | **Product-domain behaviour, server orchestration, policy decisions, persistence behaviour and entitlement authority stay outside the shared boundary** (**D-021**). |
| LY-03 | **Mobile-only application behaviour is implemented independently inside the Apache mobile boundary** (**D-021**). |
| LY-04 | **The mobile client never loads the desktop native media stack and never connects to a local Hub** (`I3 §17.1`). |

---

## 2. Licence boundary

Everything in `src/Mobile/` and the public contract and SDK projects it consumes is **Apache-2.0** (**D-004**).

| # | Rule |
|---|---|
| LB-01 | **ArcChat Mobile must not contain, link to, copy from, port from or reference any GPL-family or AGPL-only implementation**, directly or transitively. |
| LB-02 | **Automated architecture and dependency checks prevent GPL-family or AGPL-only source, project references, packages, generated artifacts and transitive dependencies from entering the distributable** (**D-004** obligation 7). |
| LB-03 | **The complete direct and transitive dependency closure is verified before the first artifact is produced** — the **F-023** gate. *Owners: Release Engineering Owner and Licensing and Provenance Owner; Product Owner approves.* |
| LB-04 | **On discovering a conflicting contribution or dependency, the issue is registered and returned for decision.** Silently adding an exception, changing the licence or dropping the mobile target is prohibited (**D-004**). |
| LB-05 | **No App Store exception, dual licensing, proprietary grant or CLA.** DCO continues with inbound-equals-outbound per scope. |
| LB-06 | **Protocol communication across an explicit process or network boundary does not change the client's licence** (**D-004**). |

---

## 3. Runtime and build

| # | Rule |
|---|---|
| RT-01 | **Android production uses the supported .NET 10 Mono AOT release path** (**D-008**, **V-04**). |
| RT-02 | **`UseMonoRuntime` is explicit in the project file**, never inherited from a default that changes in a later framework version (**V-04** gate). |
| RT-03 | **Android CoreCLR and Android Native AOT are experimental and are not production baselines** (**V-04**). |
| RT-04 | **Documentation must never conflate Mono AOT with CoreCLR Native AOT** (`§8` of the glossary). |
| RT-05 | **iOS architecture is present and complete; its build is deferred** (**D-008**). Its lifecycle, permissions, notifications, secure storage, signing, release and testing are fully planned. **It must not be claimed as compiled or tested.** |
| RT-06 | **Before any framework major upgrade, the Android runtime posture is re-verified and the mobile AOT and trim proof is re-run.** *Owner: Release Engineering Owner with Architecture Owner.* |
| RT-07 | **Before the first Android production build, the runtime is confirmed to be Mono AOT** by inspecting the produced artifact, not by reading the project file alone. |
| RT-08 | **CI genuinely builds the release artifact and runs on-device smoke tests.** A successful debug build is not a pass (`PM-03` in the quality contract). |
| RT-09 | **iOS release runtime is re-verified against the then-current supported baseline before build activation.** |

---

## 4. Serialization and clients

| # | Rule |
|---|---|
| SC-01 | **Every public DTO belongs to a source-generated serialization context.** |
| SC-02 | **The typed HTTP client uses the generated-only registration and entry point**; the reflection package is absent from the dependency graph; its diagnostic is build-breaking (**F-026**). |
| SC-03 | **Realtime uses the JSON protocol with source-generated payload metadata.** |
| SC-04 | **Reflection, dynamic assemblies and runtime code generation must not enter the iOS main path** (`I3 §17.4`) — a constraint the shared contract layer already satisfies for every platform. |
| SC-05 | **One HTTP client factory owns client construction**, with the access token injected by a delegating handler. |
| SC-06 | **Token refresh is serialised**, so concurrent requests never trigger a refresh storm. |

---

## 5. Network behaviour

| # | Rule |
|---|---|
| NW-01 | **All public commands and queries go over HTTP/JSON; realtime carries only realtime updates** (`§2.1` of the overview). |
| NW-02 | **Foreground and background transitions rebuild or restore the realtime session per platform policy.** |
| NW-03 | **Network changes use exponential backoff with jitter.** |
| NW-04 | **After reconnection, gaps are backfilled by querying sequence and revision over HTTP** (`RL-04` in the cloud architecture). |
| NW-05 | **The client never scans a LAN, never discovers a desktop Hub, and never addresses a named pipe or socket** (**D-010**). |
| NW-06 | **Cellular policy is respected** for downloads and large transfers (`AR-09` in the companion requirements). |

---

## 6. Offline outbox

```
User action while offline
 → validated locally
 → written to a durable outbox with an idempotency key
 → surfaced with an explicit pending state
 → on reconnection:
      ordinary chat drafts may send automatically
      a high-risk agent task requires explicit confirmation
```

| # | Rule |
|---|---|
| OB-01 | **The outbox is durable**, surviving process termination. |
| OB-02 | **Every write retry obeys `CommandId` idempotency** (`ID-01` in the AI requirements). |
| OB-03 | **A high-risk agent task is never automatically executed on reconnection** (`OF-02` in the companion requirements). |
| OB-03a | **An unrecognised Task state renders as an unknown non-terminal state with its reason text** (`TS-01` of the public API contract), never as failed and never as absent. Mobile ships on store timelines and is routinely older than the Cloud host, so this is the normal case, not an edge one. |
| OB-04 | **Offline caching is restrained and bounded**: recent task state, recent conversation summaries, pending attention items and small previews (`OF-01` there). |
| OB-05 | **Cached content is evictable and never authoritative.** |

---

## 7. Secure storage

| # | Rule |
|---|---|
| SS-01 | **Session material uses the platform secure storage** — keychain or keystore. |
| SS-02 | **Sensitive tokens never enter ordinary preferences or logs** (`I3 §17.3`). |
| SS-03 | **No provider credential exists on any client, desktop or mobile** (`BY-01`–`BY-04`). |
| SS-04 | **App lock is UI access protection, not authentication** (`I-277`); biometric unlock never substitutes for step-up (`I-278`). |
| SS-05 | **Provider credentials are deployment secrets held only by the Cloud host** (`DC-15`), used server-side and never projected to any client (`DC-14`). |

---

## 8. Push and deep links

| # | Rule |
|---|---|
| PD-01 | **A push registration is per device and per installation**, revocable with the device. |
| PD-02 | **A push notification is not durable attention state** (`NT-07` in the companion requirements). Missing a push never loses a pending approval. |
| PD-03 | **A push action opens the corresponding surface; it never carries authorization** (`AD-01` in the security requirements). |
| PD-04 | **Lock-screen content is non-sensitive by default** (`NT-03` there). |
| PD-05 | **Universal/app links are supported** so an HTTPS canonical URL opens the installed application (`LN-02` in the companion requirements). |
| PD-06 | **A deep link is treated as untrusted input** and never carries a secret (`DL-02`, `DL-03` in the shared desktop requirements). |

---

## 9. Commerce constraints in the build

**D-022**, confirmed by **V-09**, produces build-verifiable constraints.

| # | Rule |
|---|---|
| MC-01 | **No purchase surface exists in any build path.** |
| MC-02 | **No provider checkout is embedded.** |
| MC-03 | **No store billing integration for the initial release.** |
| MC-04 | **No external purchase button, link or call to action exists.** |
| MC-05 | **No licence-key or purchase-token unlock path exists** — the prohibition most likely to be violated by accident, since it is a natural engineering shortcut for offline entitlement. |
| MC-06 | **A build-time and CI check asserts MC-01 through MC-05** (`MB-03` in the commerce requirements). |
| MC-07 | **The entitlement architecture remains capable of accepting a future store-originated grant**, without implementing one (`MB-02` there). |

---

## 10. Placement constraints

| # | Rule |
|---|---|
| PL-01 | **Mobile never loads executable extensions** (`PL-01` in the extension requirements). |
| PL-02 | **Content packages — skills, templates, workflows — may sync; executable packages do not** (`PL-02` there). |
| PL-03 | **Mobile holds no professional product's writable domain state** (`OM-02` in the companion requirements). |
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

All platform integrations are **mobile-only libraries inside the Apache boundary** (**D-004**).

---

## 12. Testing and release gates

| # | Gate |
|---|---|
| MT-01 | Real-device verification, not emulator-only (`PM-03` in the quality contract) |
| MT-02 | The release AOT artifact built by CI and smoke-tested on device |
| MT-03 | Cold-start, memory and weak-network behaviour measured against budget |
| MT-04 | Background resume with realtime reconnection and sequence backfill |
| MT-05 | Offline queueing, pending state and controlled reconnection behaviour |
| MT-06 | The licence and dependency-closure audit — the **F-023** gate |
| MT-07 | Store category-fit and consumption-only conformance — the **V-09** gate |
| MT-08 | The commerce-prohibition build check (`MC-06`) |
| MT-09 | Accessibility verification with the platform's assistive technology |
| MT-10 | Contract compatibility against the supported client window |

---

## 13. Non-goals

Mobile is **not**: an ArcNotes, ArcScope or ArcSlate editor; a general screen-and-input remote desktop; a route that bypasses the ArcChat trust model; a way to perform R4 operations without local presence; a holder of desktop-local secrets; a commerce surface; or a host for executable extensions.

---

## 14. Traceability

| Source | Consumed as |
|---|---|
| `I3 §17` | Mobile scope, layering, network discipline, AOT and trimming rules |
| `I4 §Stage 18` | The companion product model this architecture serves |
| `I2 §III.8` | Implementation sequence, Android release path and the iOS deferred posture |
| **D-004**, **D-021**, **F-023** | The Apache boundary, no shared ViewModels, and the pre-distribution provenance gate |
| **D-008**, **V-04** | Android Mono AOT as the production baseline; iOS build-deferred; the framework-upgrade re-verification gate |
| **D-010** | Mobile connects only to Cloud |
| **D-022**, **V-09** | Consumption-only constraints made build-verifiable |
| **F-026** | Typed HTTP client entry point and reflection-package prohibition |
