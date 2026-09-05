# WP-30 — Mobile Shared Architecture and the Apache Boundary

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: G — Mobile
> Upstream: `03`, `23`, `24` · Downstream: `31`

> **Goal.** Establish the mobile foundation under a strictly enforced Apache-2.0 boundary: the shared contract and client layer, the mobile-owned presentation layer that shares no ViewModel patterns with desktop, and the Android runtime posture stated explicitly rather than inherited.

---

## 1. Scope and purpose

**In scope.** The mobile project structure and its licence boundary enforcement; the shared and not-shared split; source-generated serialization and generated-only typed clients; the realtime client on mobile; the durable offline outbox; secure storage; and the Android runtime posture with iOS architecture present but build-deferred.

**Out of scope.** The ArcChat companion features themselves (`31`). Store submission and release (`32`).

**Why this package exists.** `I2 §III.8` places mobile after the first real cloud contracts stabilise, precisely so the shared layer is built against real contracts. **D-004** makes the licence boundary a structural precondition — a violation discovered later blocks the artifact entirely (**F-023**).

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/11-mobile-architecture.md`](../../architecture/11-mobile-architecture.md) | Layering, licence boundary, runtime and build, clients, network, outbox, storage |
| **D-004**, **D-021** | The Apache boundary and the prohibition on shared ViewModel patterns |
| **D-008**, **V-04** | Android Mono AOT as the production baseline; iOS build-deferred |
| **F-023** | The provenance and dependency closure gate this package prepares for |
| `WP-03`, `WP-23`, `WP-24` output | Contracts, generated clients and the realtime client |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Everything in the mobile tree and the public contract and SDK projects it consumes is Apache-2.0** (**D-004**). |
| BR-02 | **No GPL-family or AGPL-only material may enter, directly or transitively** (**D-004**), and automated checks prevent it. |
| BR-03 | **Base ViewModel patterns are not shared with desktop** (**D-021**). Each UI stack owns its implementation. |
| BR-04 | **Product-domain behaviour, server orchestration, policy decisions, persistence behaviour and entitlement authority stay outside the shared boundary** (**D-021**). |
| BR-05 | **The mobile client never loads the desktop native stack and never connects to a local endpoint** (**D-010**). |
| BR-06 | **Android production uses the supported Mono AOT release path** (**D-008**, **V-04**), and the runtime selection is **explicit in the project file**, never inherited. |
| BR-07 | **Mono AOT is never conflated with CoreCLR Native AOT** in code, comments or documentation. |
| BR-08 | **iOS architecture is present and complete; its build is deferred** (**D-008**), and it must not be claimed as compiled or tested. |
| BR-09 | **Every public DTO uses a source-generated serialization context**, and the typed client uses the generated-only entry point with the reflection package absent (**F-026**). |
| BR-10 | **No desktop-local secret ever reaches a mobile device.** |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Mobile/ArcForges.Mobile.Core/` | Apache-2.0: application semantics with no UI |
| `src/Mobile/ArcChat.Mobile/` | Apache-2.0: the MAUI application host |
| `src/Mobile/ArcChat.Mobile.Presentation/` | Mobile-owned ViewModels, sharing nothing with desktop |
| `src/Mobile/ArcChat.Mobile.CloudClient/`, `.Realtime/` | Generated clients and the realtime client |
| `src/Mobile/ArcChat.Mobile.Persistence/` | Local cache and the durable offline outbox |
| `eng/build/android-aot.props` | Explicit runtime selection, verified from evaluated properties |
| `eng/policy/dependency-policy.json` | Mobile-boundary allowlist |
| `tests/MobileContractTests/` | Contract compatibility from the mobile client |

**Major types introduced.** `MobileSession`, `MobileOutbox`, `OutboxItem`, `SecureSessionStore`, `MobileRealtimeClient`, `ConnectivityState`, `CellularPolicy`.

---

## 5. Required implementation work

### WP-30.00 — Project structure and licence enforcement

**What must be fully done.** The mobile tree with every project declaring Apache-2.0 and its boundary. A repository policy test asserts no reference from a mobile project to an AGPL project, directly or transitively, and that every dependency's licence is on the mobile allowlist.

**Testing requirements.** A negative fixture introducing an AGPL reference must fail the build; a transitive-closure licence report.

**Completion gate.** A cross-boundary reference fails the build, and every mobile dependency's licence is on the allowlist.

### WP-30.01 — Shared and not-shared split

**What must be fully done.** The shared set is exactly: foundation, public API and realtime DTOs, contract-level validators expressing wire constraints, public protocol state semantics required for interoperability, and generated and handwritten public clients. The not-shared set — desktop XAML, window and dispatcher concepts, local RPC contracts, desktop IPC, native handles and base ViewModel patterns — is enforced by a policy test.

**Testing requirements.** A policy test asserting no desktop presentation type is referenced from mobile; a review record for each shared type.

**Completion gate.** The split is enforced by a policy test and every shared type is recorded.

### WP-30.02 — Runtime posture

**What must be fully done.** The Android project declares its runtime explicitly. A release build is produced and its runtime confirmed by inspecting the artifact, not by reading the project file. Documentation and code comments never conflate the two AOT technologies. The iOS project exists with complete architecture and is explicitly marked build-deferred.

**Testing requirements.** An evaluated-property assertion; an artifact-inspection record; a terminology scan; an iOS status assertion that no build or test claim is made.

**Completion gate.** The Android runtime is confirmed from the produced artifact, terminology is unambiguous, and iOS status is honestly stated.

### WP-30.03 — Serialization and clients

**What must be fully done.** Every DTO in a source-generated context; the typed client using the generated-only entry point with the reflection package absent; the realtime client using source-generated payload metadata; one client factory with a token handler and serialised refresh.

**Testing requirements.** A dependency assertion; a refresh-storm test; a contract compatibility run from the mobile client against the supported server window.

**Completion gate.** Clients work with no reflection package present, refresh never storms, and the compatibility matrix passes from mobile.

### WP-30.04 — Network behaviour and offline outbox

**What must be fully done.** All commands and queries over HTTP with realtime carrying only updates; exponential backoff with jitter on network change; sequence-gap backfill over HTTP after reconnection; a durable outbox surviving process termination with idempotency keys; cellular policy respected for large transfers.

**Testing requirements.** Network-transition tests; backfill after a long disconnect; outbox survival across process death; a cellular-policy test.

**Completion gate.** The client converges after any disconnection, and pending actions survive process termination.

### WP-30.05 — Secure storage and lifecycle

**What must be fully done.** Session material in platform secure storage; no sensitive token in ordinary preferences or logs; app lock as UI access protection only, never as authentication and never substituting for step-up; lifecycle transitions driving realtime session and outbox behaviour.

**Testing requirements.** A storage-location assertion per platform; a log-scan for token leakage; a negative test asserting app lock does not satisfy step-up; foreground and background transition tests.

**Completion gate.** Session material is in secure storage only, no token appears in logs, and app lock never satisfies step-up.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Mobile local cache and the outbox store |
| Protocol | Mobile becomes a contract consumer in the compatibility window |
| UI | Mobile presentation foundation, sharing nothing with desktop |
| Security | Licence boundary, secure storage and the no-desktop-secret rule |
| Platform | Android runtime posture; iOS architecture present, build deferred |
| Migration | Mobile cache schema versioning |
| Compatibility | Mobile enters the supported client window |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Cross-boundary negative fixture and transitive licence report | `WP-30.00` |
| Shared/not-shared policy test and shared-type record | `WP-30.01` |
| Evaluated-property assertion, artifact inspection, terminology scan | `WP-30.02` |
| Dependency assertion, refresh-storm and compatibility matrix results | `WP-30.03` |
| Network-transition, backfill, outbox-survival and cellular results | `WP-30.04` |
| Secure-storage, log-scan and step-up negative results | `WP-30.05` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. A cross-boundary reference fails the build; every mobile dependency's licence is on the mobile allowlist.
2. The shared and not-shared split is enforced by a policy test, with **no base ViewModel pattern shared with desktop**.
3. The Android runtime posture is confirmed by inspecting the produced release artifact; terminology never conflates the two AOT technologies; iOS is honestly marked build-deferred.
4. Clients work with the reflection package absent; refresh never storms; the compatibility matrix passes from the mobile client.
5. The client converges after any disconnection; pending actions survive process termination.
6. Session material lives only in platform secure storage; no token appears in logs; app lock never satisfies step-up.

---

## 9. Dependencies

**Upstream.** `03` (contracts), `23` (generated clients), `24` (realtime client).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `31` — ArcChat Mobile | The entire foundation |
| `32` — Mobile release | The boundary and runtime posture the release gates verify |
