<a id="rule-wp-30"></a>
# WP-30 — Kotlin Android Foundation

> Status: Authoritative implementation plan under [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010)
> Phase: G — Kotlin Android foundation
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

## 1. Scope and purpose

Implement this stage of the complete Android ArcChat companion. [Mobile architecture](../../architecture/11-mobile-architecture.md), [client journeys](../../architecture/contracts/07-client-journeys-and-ports.md), [companion requirements](../../requirements/products/arcchat-mobile-and-web.md) and [producer stages](../producer-artifacts-and-integration.md) fix scope, behavior and evidence. Source repositories are implementation/reference evidence only; their hello scaffolds do not define completion.

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


Use the exact released Contracts Maven package/descriptor/fixture set, compatible Cloud/AI manifest and completed upstream owner outputs. Android toolchain and OS decisions come from Mobile architecture and WP06 proof; a blocking local toolchain/Android environment problem is reported before dependent execution. No producer source checkout or browser TS runtime is an input.

## 3. Binding rules and decisions

Android only, Kotlin/JVM/Jetpack Compose, Apache-2.0; no GPL-family implementation in the app. Command/owner/recovery identity, explicit permissions/consent, exact values, immutable producer artifacts, full accepted companion scope and consumption-only commercial restrictions are mandatory. [Wire registry](../../architecture/contracts/04-protobuf-wire-registry.md) owns the complete field and operation inventory. Equivalent internal classes/layout choices may vary only when observable behavior and acceptance remain identical.

## 4. Projects, directories, files and major types affected

Mobile adopts the exact module map in architecture 27 (app, core and feature modules), tests and Android build/release governance. The Hello World shared/preview host is not a second production module plan. No edits in other implementation repositories are required to bypass their published artifact boundary.

## 5. Required implementation work

<a id="rule-wp-30.00"></a>
### WP-30.00 — Android repository identity and toolchain

**What must be fully done.** Adopt com.arcforges.mobile applicationId/namespace/source packages before production. Follow-up F-1: on JDK 21 reconcile the Hello World compiler/AGP/Compose/Gradle stack to mutually compatible stable releases; commit exact producer pins, wrapper checksums, locks and generated-client compatibility evidence before any production upload. Document development prerelease reinstall; Apache boundary includes no GPL-family closure.

**Testing requirements.** Release build, dependency verification, package/certificate inspection, device install and fixture-key App Link tests.

**Completion gate.** Production identity and own Android module map match arch 11/27; no RN/TS or iOS obligation.

<a id="rule-wp-30.01"></a>
### WP-30.01 — Native module and route boundaries

**What must be fully done.** Implement architecture 27 concrete Kotlin app/core/feature modules and AN01–AN25 navigation/state contracts; features depend typed core ports, app composes them, no React Native/iOS or AGPL imports.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience 03; named later-provider fixtures cannot close real integration.

**Completion gate.** Transport records do not become mutable domain/UI owners; all module boundaries enforceable.

<a id="rule-wp-30.02"></a>
### WP-30.02 — Android runtime and OS adapters

**What must be fully done.** Use the exact API/RID/runtime profile in Mobile architecture: arm64 release, x64 emulator; Compose, Credential Manager/passkey fallback, Keystore, WorkManager, notifications/FCM with non-GMS fallback, SAF/MediaStore/FileProvider. OS callbacks use generation and account scope.

**Testing requirements.** Install real release build on physical Android, permission refusal, process death, missing Play services and callback after account switch.

**Completion gate.** Produced APK uses Kotlin/ART with complete supported adapters and no unsafe fallback.

<a id="rule-wp-30.03"></a>
### WP-30.03 — Published gRPC-Web contracts

**What must be fully done.** Consume pinned Maven messages/Connect Kotlin clients and fixtures. Select binary gRPC-Web explicitly; implement session/stream/retry/exact-value adapters and actual deployed foundation calls.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience 03; named later-provider fixtures cannot close real integration.

**Completion gate.** Real packaged Maven consumer and service/device evidence passes; missing TLS/transport support blocks.

<a id="rule-wp-30.04"></a>
### WP-30.04 — Room history, drafts and receipts

**What must be fully done.** Implement model 05 equivalent Room schemas and per-profile partitions, own local/cloud/temporary behavior, bounded outbox/transfers/cursors. Local canonical history is not evictable cache; temporary content never persists.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience 03; named later-provider fixtures cannot close real integration.

**Completion gate.** Drafts/pending work survive; retries reconcile exact owner command and never fabricate a completed side effect.

<a id="rule-wp-30.05"></a>
### WP-30.05 — Secure lifecycle and permissions

**What must be fully done.** Implement per-account Keystore encryption, no-backup secret/pending-store policy, session/logout/revoke purge versus unsent-work quarantine/export, same-generation deep link validation and current foreground consent. No credential in logs/crash/notification/analytics.

**Testing requirements.** Device restore without key, logout/switch while requests run, deep-link spoof, notification click after revocation, secret scan of release logs/backup.

**Completion gate.** Security/lifecycle behavior matches Mobile architecture and client journeys with recoverable local user work.

<a id="rule-wp-30.90"></a>
### WP-30.90 — Foundation integration evidence

**What must be fully done.** Publish/test the exact candidate APK against real 22/23/24/25 and released Maven packages. Future Task/AI fixtures must be named in evidence and compiled out of production at 31.

**Testing requirements.** Clean-cache restore/build/install and actual sign-in/hydration/upload/reconnect on device.

**Completion gate.** Foundation complete; full companion and AI are explicitly gated by 31/52, not counted here.

## 6. Impacts

Contracts delivers the complete public Kotlin package; Cloud/AI deliver the same owner behavior as desktop/Web. Mobile maintains its own lifecycle/storage/UI. Changes in package/signing/schema versions require an explicit compatible manifest and tested migration.

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-30.90](#rule-wp-30.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

Separate unit/schema/fixture tests, clean packaged consumers, actual Cloud/CF/desktop interactions, physical-device release evidence and distribution/store evidence. Record exact hashes/versions/device identity and limitations. A green build cannot substitute for a missing stage.


| Evidence | Produced by |
|---|---|
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-30.90](#rule-wp-30.90) |

## 8. Completion gate

Every numbered substep and applicable inherited requirement passes; the complete surface/action/state matrix is exercised. Unfinished required behavior blocks completion. Candidate and producer identities are immutable and all temporary fixtures have the named replacement stage. No scope reduction or design decision is deferred to consumer coding.

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [AND.01](../delivery/lanes/android.md#task-and-01) | [WP-30.00](30-mobile-shared-architecture.md#rule-wp-30.00) (all work except the parts mapped to AND.04)<br>[WP-30](30-mobile-shared-architecture.md#rule-wp-30) §3 binding rules: Apache-2.0 boundary, no GPL-family implementation, immutable producer artifacts (package-level obligation contribution) | [PRF.10](../delivery/lanes/runtime-proofs.md#task-prf-10) (artifact) |
| [AND.02](../delivery/lanes/android.md#task-and-02) | [WP-30.01](30-mobile-shared-architecture.md#rule-wp-30.01) (full) | none |
| [AND.03](../delivery/lanes/android.md#task-and-03) | [WP-30.02](30-mobile-shared-architecture.md#rule-wp-30.02) (full) | none |
| [AND.04](../delivery/lanes/android.md#task-and-04) | [WP-30.03](30-mobile-shared-architecture.md#rule-wp-30.03) (full)<br>[WP-30.00](30-mobile-shared-architecture.md#rule-wp-30.00) (Kotlin Android foundation real package consumption) | [CON.07](../delivery/lanes/contracts.md#task-con-07) (contract), [CON.11](../delivery/lanes/contracts.md#task-con-11) (contract) |
| [AND.05](../delivery/lanes/android.md#task-and-05) | [WP-30.04](30-mobile-shared-architecture.md#rule-wp-30.04) (full) | [CON.11](../delivery/lanes/contracts.md#task-con-11) (contract) |
| [AND.06](../delivery/lanes/android.md#task-and-06) | [WP-30.05](30-mobile-shared-architecture.md#rule-wp-30.05) (full) | none |
| [AND.07](../delivery/lanes/android.md#task-and-07) | [WP-30.90](30-mobile-shared-architecture.md#rule-wp-30.90) (full) | [CLOUD.13](../delivery/lanes/cloud.md#task-cloud-13) (artifact), [CLOUD.42](../delivery/lanes/cloud.md#task-cloud-42) (artifact), [CLOUD.39](../delivery/lanes/cloud.md#task-cloud-39) (artifact), [CLOUD.18](../delivery/lanes/cloud.md#task-cloud-18) (artifact), [CLOUD.19](../delivery/lanes/cloud.md#task-cloud-19) (artifact), [CLOUD.26](../delivery/lanes/cloud.md#task-cloud-26) (artifact), [CLOUD.29](../delivery/lanes/cloud.md#task-cloud-29) (artifact) |
| [AND.14](../delivery/lanes/android.md#task-and-14) | [WP-30](30-mobile-shared-architecture.md#rule-wp-30) §3 binding rules: Apache-2.0 boundary, no GPL-family implementation, immutable producer artifacts (package-level obligation contribution) | [AND.08](../delivery/lanes/android.md#task-and-08) (artifact), [AND.09](../delivery/lanes/android.md#task-and-09) (artifact), [AND.10](../delivery/lanes/android.md#task-and-10) (artifact) |

**Consumers outside this package:** [AND.08](../delivery/lanes/android.md#task-and-08), [AND.09](../delivery/lanes/android.md#task-and-09), [AND.10](../delivery/lanes/android.md#task-and-10), [AND.11](../delivery/lanes/android.md#task-and-11), [AND.12](../delivery/lanes/android.md#task-and-12), [AND.15](../delivery/lanes/android.md#task-and-15), [CLOUD.28](../delivery/lanes/cloud.md#task-cloud-28).

<!-- delivery-graph:end -->

