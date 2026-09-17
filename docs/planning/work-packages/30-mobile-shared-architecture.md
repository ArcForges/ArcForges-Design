<a id="rule-wp-30"></a>
# WP-30 — Kotlin Android Foundation

> Status: Authoritative implementation plan under P2-010
> Phase: G — Kotlin Android foundation
> Upstream: `03` · `06` · `23` · `24` · `25` · Downstream: `31`

## 1. Scope and purpose

Implement this stage of the complete Android ArcChat companion. [Mobile architecture](../../architecture/11-mobile-architecture.md), [client journeys](../../architecture/contracts/07-client-journeys-and-ports.md), [companion requirements](../../requirements/products/arcchat-mobile-and-web.md) and [producer stages](../producer-artifacts-and-integration.md) fix scope, behavior and evidence. Source repositories are implementation/reference evidence only; their hello scaffolds do not define completion.

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


Use the exact released Contracts Maven package/descriptor/fixture set, compatible Cloud/AI manifest and completed upstream owner outputs. Android toolchain and OS decisions come from Mobile architecture and WP06 proof; a blocking local toolchain/Android environment problem is reported before dependent execution. No producer source checkout or browser TS runtime is an input.

## 3. Binding rules and decisions

Android only, Kotlin/JVM/Jetpack Compose, Apache-2.0; no GPL-family implementation in the app. Command/owner/recovery identity, explicit permissions/consent, exact values, immutable producer artifacts, full accepted companion scope and consumption-only commercial restrictions are mandatory. [Wire registry](../../architecture/contracts/04-protobuf-wire-registry.md) owns the complete field and operation inventory. Equivalent internal classes/layout choices may vary only when observable behavior and acceptance remain identical.

## 4. Projects, directories, files and major types affected

Mobile owns app/, core/domain, core/data, core/network, core/security, core/designsystem, feature/home, feature/chat, feature/tasks, feature/library and feature/settings, tests and Android build/release governance. An equivalent module partition may preserve the same boundaries. No edits in other implementation repositories are required to bypass their published artifact boundary.

## 5. Required implementation work

<a id="rule-wp-30.00"></a>
### WP-30.00 — Repository, build and Apache boundary

**What must be fully done.** Create Android Kotlin/JVM/Compose app/, core/ and feature/ modules with Gradle Kotlin DSL, version catalog, verified wrapper, exact dependency locks/checksums, .gitignore/.gitattributes/.editorconfig, Apache LICENSE/NOTICE/SPDX, SECURITY/CONTRIBUTING/CODEOWNERS, issue/PR templates, local hooks and CI parity. Pin the proven toolchain from WP06; signed app identity remains com.arcforges.mobile. No implementation repo is a source dependency.

**Testing requirements.** Fresh checkout, hook bypass in CI, LF/binary attributes, Gradle locked restore and negative GPL-family/import fixtures.

**Completion gate.** Complete reproducible Android repository and compatible direct/transitive closure; no RN/npm runtime or iOS deliverable.

<a id="rule-wp-30.01"></a>
### WP-30.01 — Native module and route boundaries

**What must be fully done.** Implement architecture27 concrete Kotlin app/core/feature modules and AN01–AN25 navigation/state contracts; features depend typed core ports, app composes them, no React Native/iOS or AGPL imports.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience03; named later-provider fixtures cannot close real integration.

**Completion gate.** Transport records do not become mutable domain/UI owners; all module boundaries enforceable.

<a id="rule-wp-30.02"></a>
### WP-30.02 — Android runtime and OS adapters

**What must be fully done.** Use the exact API/RID/runtime profile in Mobile architecture: arm64 release, x64 emulator; Compose, Credential Manager/passkey fallback, Keystore, WorkManager, notifications/FCM with non-GMS fallback, SAF/MediaStore/FileProvider. OS callbacks use generation and account scope.

**Testing requirements.** Install real release build on physical Android, permission refusal, process death, missing Play services and callback after account switch.

**Completion gate.** Produced APK uses Kotlin/ART with complete supported adapters and no unsafe fallback.

<a id="rule-wp-30.03"></a>
### WP-30.03 — Published gRPC-Web contracts

**What must be fully done.** Consume pinned Maven messages/Connect Kotlin clients and fixtures. Select binary gRPC-Web explicitly; implement session/stream/retry/exact-value adapters and actual deployed foundation calls.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience03; named later-provider fixtures cannot close real integration.

**Completion gate.** Real packaged Maven consumer and service/device evidence passes; missing TLS/transport support blocks.

<a id="rule-wp-30.04"></a>
### WP-30.04 — Room history, drafts and receipts

**What must be fully done.** Implement model05 equivalent Room schemas and per-profile partitions, own local/cloud/temporary behavior, bounded outbox/transfers/cursors. Local canonical history is not evictable cache; temporary content never persists.

**Testing requirements.** Verify the stated behavior against the exact real artifact/owner boundary. Include scope/permission, wrong or stale target, loss/retry, expiry and applicable native UI cases from experience03; named later-provider fixtures cannot close real integration.

**Completion gate.** Drafts/pending work survive; retries reconcile exact owner command and never fabricate a completed side effect.

<a id="rule-wp-30.05"></a>
### WP-30.05 — Secure lifecycle and permissions

**What must be fully done.** Implement per-account Keystore encryption, no-backup secret/pending-store policy, session/logout/revoke purge versus unsent-work quarantine/export, same-generation deep link validation and current foreground consent. No credential in logs/crash/notification/analytics.

**Testing requirements.** Device restore without key, logout/switch while requests run, deep-link spoof, notification click after revocation, secret scan of release logs/backup.

**Completion gate.** Security/lifecycle behavior matches Mobile architecture and client journeys with recoverable local user work.

<a id="rule-wp-30.90"></a>
### WP-30.90 — Foundation integration evidence

**What must be fully done.** Publish/test the exact candidate APK against real22/23/24/25 and released Maven packages. Future Task/AI fixtures must be named in evidence and compiled out of production at31.

**Testing requirements.** Clean-cache restore/build/install and actual sign-in/hydration/upload/reconnect on device.

**Completion gate.** Foundation complete; full companion and AI are explicitly gated by31/52, not counted here.

## 6. Impacts

Contracts delivers the complete public Kotlin package; Cloud/AI deliver the same owner behavior as desktop/Web. Mobile maintains its own lifecycle/storage/UI. Changes in package/signing/schema versions require an explicit compatible manifest and tested migration.

## 7. Tests and verification evidence

Separate unit/schema/fixture tests, clean packaged consumers, actual Cloud/CF/desktop interactions, physical-device release evidence and distribution/store evidence. Record exact hashes/versions/device identity and limitations. A green build cannot substitute for a missing stage.


| Evidence | Produced by |
|---|---|
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-30.90](#rule-wp-30.90) |

## 8. Completion gate

Every numbered substep and applicable inherited requirement passes; the complete surface/action/state matrix is exercised. Unfinished required behavior blocks completion. Candidate and producer identities are immutable and all temporary fixtures have the named replacement stage. No scope reduction or design decision is deferred to consumer coding.

## 9. Dependencies

**Upstream:** `03` · `06` · `23` · `24` · `25`. Consume completed stage outputs.

**Downstream:** `31`. Consumers use exact released artifacts.
