<a id="rule-wp-30"></a>

# WP-30 — React Native Companion Foundation

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: G — Mobile
> Upstream: `03`, `06`, `23`, `24` · Downstream: `31`

> **Goal.** Establish the mobile foundation under a strictly enforced Apache-2.0 boundary: the shared contract and client layer, the mobile-owned presentation layer that shares no ViewModel patterns with desktop, and the Android runtime posture stated explicitly rather than inherited.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Mobile; Apache Contracts. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: RN/Hermes artifact and real generated service clients with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The mobile project structure and its licence boundary enforcement; the shared and not-shared split; generated TypeScript protobuf types and the selected RN unary gRPC-Web transport; the realtime client on mobile; the durable offline outbox; secure storage; and the Android runtime posture with iOS architecture present but build-deferred.

**Out of scope.** The ArcChat companion features themselves (`31`). Store submission and release (`32`).

**Why this package exists.** [the current dependency model](../implementation-sequence.md#2-phase-structure) places mobile after the first real cloud contracts stabilise, precisely so the shared layer is built against real contracts. **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)** makes the licence boundary a structural precondition — a violation discovered later blocks the artifact entirely (**[F-023](../../assurance/open-gates-register.md#rule-f-023)**).

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/11-mobile-architecture.md`](../../architecture/11-mobile-architecture.md) | Layering, licence boundary, runtime and build, clients, network, outbox, storage |
| **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**, **[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)** | The Apache boundary and the prohibition on shared ViewModel patterns |
| **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-04](../../assurance/phase-1-official-verification.md#rule-v-04)** | Android React Native/Hermes as the production baseline; iOS build-deferred |
| **[F-023](../../assurance/open-gates-register.md#rule-f-023)** | The provenance and dependency closure gate this package prepares for |
| [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-23](23-public-api-and-generated-clients.md#rule-wp-23), [WP-24](24-realtime-and-reliable-events.md#rule-wp-24) output | Contracts, generated clients and the realtime client |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Everything in the mobile tree and the public contract and SDK projects it consumes is Apache-2.0** (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**). |
| BR-02 | **No GPL-family or AGPL-only material may enter, directly or transitively** (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**), and automated checks prevent it. |
| BR-03 | **Base ViewModel patterns are not shared with desktop** (**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**). Each UI stack owns its implementation. |
| BR-04 | **Product-domain behaviour, server orchestration, policy decisions, persistence behaviour and entitlement authority stay outside the shared boundary** (**[D-021](../../decisions/phase-1-foundation-decisions.md#rule-d-021)**). |
| BR-05 | **The mobile client never loads the desktop native stack and never connects to a local endpoint** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |
| BR-06 | Android production pins the RN template, New Architecture and bundled Hermes in Gradle/npm lock files; release artifact inspection proves that selection. |
| BR-07 | Hermes bytecode/native modules are the mobile runtime. CoreCLR Native AOT governs C# desktop/Cloud only; no .NET mobile runtime settings enter this repository. |
| BR-08 | **iOS architecture is present and complete; its build is deferred** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**), and it must not be claimed as compiled or tested. |
| BR-09 | Consume only the released Apache public proto/SDK/RN transport closure; contract drift, trailer/status decoding, bigint and refresh behavior are tested on Hermes. |
| BR-10 | **No desktop-local secret ever reaches a mobile device.** |

---

## 4. Projects, directories, files and major types affected

Paths resolve in ArcForges-Mobile under [the selected repository and screen design](../../architecture/11-mobile-architecture.md#15-mobile-repository-screens-and-execution-state).

| Location | Deliverable |
|---|---|
| package.json, package-lock.json, android/, ios/ | Pinned RN template; Android release profile; deferred iOS source/adapters |
| src/app/, src/services/ | Boot/navigation/session generation, generated RPC composition and CF presentation |
| src/storage/ | Versioned SQLite migrations, durable drafts/outbox, bounded acknowledged projections |
| src/platform/ | Secure storage, passkey, push, links, pickers and lifecycle adapters |
| eng/policy/, tests/unit/, tests/contract/, tests/device/ | Apache import/closure controls, deterministic protocol/recovery tests and actual device proof |

Application types are TypeScript records/hooks/services: MobileSession, MobileOutbox, OutboxItem, SecureSessionStore, MobileRealtimeClient, ConnectivityState and CellularPolicy. Native adapters expose bounded typed values; no C# or desktop domain import is used.

---

## 5. Required implementation work

<a id="rule-wp-30.00"></a>

### WP-30.00 — Project structure and licence enforcement


**What must be fully done.** Create the Apache RN repository from the pinned template. Enforce the released public-only npm import boundary and enumerate npm/Gradle/native transitive source and licences before any artifact. Consume the first-artifact closure from WP06, rerunning it for changes; isolate policy negative fixtures from distributables.

**Testing requirements.** Reject direct/transitive AGPL imports, local sibling paths and unrecorded native binaries; verify exact lock/source hashes.

**Completion gate.** [F-023](../../assurance/open-gates-register.md#rule-f-023) has an actual complete closure for this candidate before build; no unresolved licence item enters the app.

<a id="rule-wp-30.01"></a>

### WP-30.01 — Shared and not-shared split


**What must be fully done.** Construct src/app, services, storage, platform and feature boundaries exactly as the mobile architecture specifies. Share only Apache generated public types/clients and wire validators; mobile presentation, session, persistence and application behavior are mobile-owned.

**Testing requirements.** Import-policy tests reject desktop IPC/native/domain/ViewModel and AGPL Web application imports.

**Completion gate.** Every module has its selected owner and generated/public boundary; the independent checkout builds without sibling source.

<a id="rule-wp-30.02"></a>

### WP-30.02 — Runtime posture


**What must be fully done.** Build Android arm64 release with RN 0.87.1 bundled Hermes/New Architecture and the selected Gradle template. Inspect packaged Hermes bytecode/runtime/native modules and exercise a native view, navigation, OP-SQLite transaction, secure storage and passkey adapter. Retain the iOS source/platform mapping with build jobs disabled.

**Testing requirements.** Use the first-artifact gated closure; run the exact artifact on a physical Android device, retain package/runtime inspection and measured launch/memory results.

**Completion gate.** Hermes and every selected native adapter load under the release build; iOS remains explicitly unbuilt.

<a id="rule-wp-30.03"></a>

### WP-30.03 — Serialization and clients


**What must be fully done.** Wire exact released public protobuf-es clients and the Apache RN unary gRPC-Web adapter: frame/trailer parsing, binary status/details, cancellation/deadline, uint64 bigint, exact decimals/origin, maximum bytes, opaque bearer handler and single-flight refresh. CF presentation uses the selected first-message nonce, byte offsets and catch-up.

**Testing requirements.** Against actual AOT Cloud, test success/domain/transport errors, trailers, malformed frames, clock/expiry, refresh storms and supported version window; test CF revocation and stream interruption.

**Completion gate.** Real RN transport passes the common C#/TS vectors and current/previous contract matrix without browser ReadableStream assumptions.

<a id="rule-wp-30.04"></a>

### WP-30.04 — Network behaviour and offline outbox


**What must be fully done.** Implement the specified SQLite tables/migrations and outbox transitions. Persist exact scoped command/input/IDs before sending; atomically acknowledge; preserve draft and unknown-command work across death, disk full and cache eviction. Read known chat/task identities and use the permitted same-ID replay to obtain the stored dedup receipt as fixed in the mobile architecture; high-risk work stays blocked for confirmation.

**Testing requirements.** Kill before send, after send/before acknowledgement and during migration; reopen offline then reconnect; verify one server effect and retained user work. Test cellular refusal and cache pressure.

**Completion gate.** No duplicate effect, silently lost draft or cross-account queued send; bounded projections can be discarded independently.

<a id="rule-wp-30.05"></a>

### WP-30.05 — Secure storage and lifecycle


**What must be fully done.** Implement session generation, secure token storage, passkey/platform lifecycle, notification permission, app links, picker and sharing adapters. Foreground reauthorizes/reconciles; background stops polling/live reads; notification actions navigate only. App lock never satisfies server step-up.

**Testing requirements.** Physical-device suspend/kill/refresh/revoke/sign-out/workspace-switch tests; late callbacks ignored; secrets absent from ordinary files/logs; permissions denied and push disabled still allow durable attention.

**Completion gate.** Each selected adapter and recovery state is implemented and independently tested with the real service boundary.

**Required implementation and closure from the final review.** Implement and independently verify [08-security-architecture](../../architecture/08-security-architecture.md#account-and-provider-closure). Use the generated complete account/session projection. A generation change stops outgoing commands before fresh bootstrap and preserves pending user input for explicit review; no token is copied into JS persistence. Deletion cancellation uses restricted fresh proof and cannot open ordinary data routes. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-30.90"></a>
### WP-30.90 — Verify the owned artifact and real integration


**What must be fully done.** Assemble the foundation from the preceding substeps against the pinned AOT Cloud/CF candidate. Record Contracts/npm, Cloud OCI and deployed Worker identities with the mobile commit.

**Testing requirements.** Run the foundation device/protocol/death scenarios with production RN transport and actual providers.

**Completion gate.** Foundation is ready for the feature work in WP31; no template, storage, auth or transport decision remains open.

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
| Cross-boundary negative fixture and transitive licence report | [WP-30.00](#rule-wp-30.00) |
| Shared/not-shared policy test and shared-type record | [WP-30.01](#rule-wp-30.01) |
| Evaluated-property assertion, artifact inspection, terminology scan | [WP-30.02](#rule-wp-30.02) |
| Dependency assertion, refresh-storm and compatibility matrix results | [WP-30.03](#rule-wp-30.03) |
| Network-transition, backfill, outbox-survival and cellular results | [WP-30.04](#rule-wp-30.04) |
| Secure-storage, log-scan and step-up negative results | [WP-30.05](#rule-wp-30.05) |

---

## 8. Completion gate

**Runtime/closure producers.** [F-023](../../assurance/open-gates-register.md#rule-f-023) through [WP-30.00](#rule-wp-30.00); [VG-07](../../assurance/open-gates-register.md#rule-vg-07) through [WP-30.02](#rule-wp-30.02). The named candidate must supply actual passing evidence; documentation does not close these gates.

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-30.90](#rule-wp-30.90) and all inherited domain-specific gates must pass on the same candidate closure. Real generated SDK/RN runtime, secure-storage and process-death/outbox proofs; no desktop native/AGPL dependency enters the app.

**All of the following, with recorded evidence:**

1. A cross-boundary reference fails the build; every mobile dependency's licence is on the mobile allowlist.
2. The shared and not-shared split is enforced by a policy test, with **no base ViewModel pattern shared with desktop**.
3. The Android runtime posture is confirmed by inspecting the produced release artifact; terminology never conflates the selected Hermes and C# runtime boundaries; iOS is honestly marked build-deferred.
4. Clients use the released generated public closure and selected RN transport; refresh never storms; the compatibility matrix passes from the mobile client.
5. The client converges after any disconnection; pending actions survive process termination.
6. Session material lives only in platform secure storage; no token appears in logs; app lock never satisfies step-up.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03)
- [WP-06](06-aot-jit-and-wasm-publish-proof.md#rule-wp-06)
- [WP-23](23-public-api-and-generated-clients.md#rule-wp-23)
- [WP-24](24-realtime-and-reliable-events.md#rule-wp-24)

**Downstream — consumers of these released outputs.**

- [WP-31](31-arcchat-mobile-android.md#rule-wp-31)


---
