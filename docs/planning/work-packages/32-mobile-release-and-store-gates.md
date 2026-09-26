<a id="rule-wp-32"></a>
# WP-32 — Android Signing, Distribution and Store Gates

> Status: Authoritative implementation plan under [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010)
> Phase: J — Platform and client integration
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

## 1. Scope and purpose

Implement this stage of the complete Android ArcChat companion. [Mobile architecture](../../architecture/11-mobile-architecture.md), [client journeys](../../architecture/contracts/07-client-journeys-and-ports.md), [companion requirements](../../requirements/products/arcchat-mobile-and-web.md) and [producer stages](../producer-artifacts-and-integration.md) fix scope, behavior and evidence. Source repositories are implementation/reference evidence only; their hello scaffolds do not define completion.

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


Use the exact released Contracts Maven package/descriptor/fixture set, compatible Cloud/AI manifest and completed upstream owner outputs. Android toolchain and OS decisions come from Mobile architecture and WP06 proof; a blocking local toolchain/Android environment problem is reported before dependent execution. No producer source checkout or browser TS runtime is an input.

<a id="rule-br-03"></a>
## 3. Binding rules and decisions

Android only, Kotlin/JVM/Jetpack Compose, Apache-2.0; no GPL-family implementation in the app. Command/owner/recovery identity, explicit permissions/consent, exact values, immutable producer artifacts, full accepted companion scope and consumption-only commercial restrictions are mandatory. [Wire registry](../../architecture/contracts/04-protobuf-wire-registry.md) owns the complete field and operation inventory. Equivalent internal classes/layout choices may vary only when observable behavior and acceptance remain identical.

## 4. Projects, directories, files and major types affected

Mobile owns app/, core/domain, core/data, core/network, core/security, core/designsystem, feature/home, feature/chat, feature/tasks, feature/library and feature/settings, tests and Android build/release governance. An equivalent module partition may preserve the same boundaries. No edits in other implementation repositories are required to bypass their published artifact boundary.

## 5. Required implementation work

<a id="rule-wp-32.00"></a>
### WP-32.00 — Signed Android release artifacts

**What must be fully done.** Build AAB for Play and separately signed direct APK automatically from reviewed main, with monotonic versionCode and immutable provenance. Preserve signing custody/channel distinction and test against WP03 update schemas.

**Testing requirements.** Verify actual signature/package/R8/runtime, version monotonicity, no development key in production, clean device install/upgrade.

**Completion gate.** Actual signed artifacts are produced; store/production-account gates stay evidence-based.

<a id="rule-wp-32.01"></a>
### WP-32.01 — Release runtime inspection

**What must be fully done.** Verify Kotlin/ART, Compose/public grpc-lite closure, min/target API, arm64 assets, R8 rules and required permissions on actual APK/AAB.

**Testing requirements.** Install without development server/toolchain; startup/identity/RPC/R2/notifications and lifecycle release tests.

**Completion gate.** No debug-only success or source inspection counts as release runtime proof.

<a id="rule-wp-32.02"></a>
### WP-32.02 — Dependency and source rights

**What must be fully done.** Audit direct/transitive Gradle/plugin/runtime/asset closure, licences, provenance and reproducible SBOM/NOTICE. Verify public schema/tooling Apache origin; independently original app implementation.

**Testing requirements.** Forbidden licence fixture, unpinned/dynamic dependency and changed-checksum rejection; binary inventory matches candidate.

**Completion gate.** Apache distribution/store closure passes before publication.

<a id="rule-wp-32.03"></a>
### WP-32.03 — Consumption-only enforcement

**What must be fully done.** Enforce absence of purchase buttons/embedded checkout/store billing/external purchase calls to action/licence-key unlock. Show existing access, quota, service expiry and explicit consumption budget using admitted account APIs.

**Testing requirements.** Static route/dependency checks and all-state UX tests, including expired subscription and exhausted credits.

**Completion gate.** Consumption-only remains true in every release branch and remote-config state.

<a id="rule-wp-32.04"></a>
### WP-32.04 — Play and direct-channel updates

**What must be fully done.** Implement arch 11 channel behavior and notify-only signed update client. Consume WP03 format/fixture keys now; WP53 production feed/key replacement is verified at WP50, not a backwards input.

**Testing requirements.** Expired/rollback/wrong certificate/URL/hash, offline stale feed and explicit channel-switch export/reinstall guidance.

**Completion gate.** Play primary and direct APK flow are complete with no silent install or unsupported cross-signature upgrade.

<a id="rule-wp-32.05"></a>
### WP-32.05 — Physical device and recovery gates

**What must be fully done.** Run full companion on minimum supported and current Android physical-device profiles, weak/offline network, permission denial, no-GMS, key loss/backup restore, process kill and OS background limits. Test migration and forward-rescue release with a higher versionCode; Android cannot accept downgrade as the routine rollback.

**Testing requirements.** Actual local/server unknown-effect replay and encrypted draft/outbox retention through upgrade; signing-key recovery rehearsal with protected evidence.

**Completion gate.** All mandatory scenarios pass, material device limits disclosed and no pending user work lost.

<a id="rule-wp-32.06"></a>
### WP-32.06 — Android scope statement

**What must be fully done.** Document Android only; iOS, Swift, KMP and cross-platform UI are outside this delivery and contribute no completion gate. Keep app name/product identity separate from implementation language.

**Testing requirements.** Store/release/readme/platform matrices match signed Android artifact.

**Completion gate.** No false retained-iOS deliverable or unsupported platform claim.

<a id="rule-wp-32.90"></a>
### WP-32.90 — Distribution acceptance

**What must be fully done.** Archive exact signed APK/AAB, manifest/hash/versionCode/certificate identity, compatible server/Contracts release and all gate receipts; publish through the automatic main graph.

**Testing requirements.** Download public candidate in a clean device path, verify signature/hash and exercise actual services.

**Completion gate.** Distribution complete only with real receipts; document/CI fixtures alone do not establish store or commercial operation.

## 6. Impacts

Contracts delivers the complete public Kotlin package; Cloud/AI deliver the same owner behavior as desktop/Web. Mobile maintains its own lifecycle/storage/UI. Changes in package/signing/schema versions require an explicit compatible manifest and tested migration.

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-32.90](#rule-wp-32.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

Separate unit/schema/fixture tests, clean packaged consumers, actual Cloud/CF/desktop interactions, physical-device release evidence and distribution/store evidence. Record exact hashes/versions/device identity and limitations. A green build cannot substitute for a missing stage.


| Evidence | Produced by |
|---|---|
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-32.90](#rule-wp-32.90) |

## 8. Completion gate

[PG-24](../../assurance/open-gates-register.md#rule-pg-24): exercise the actual WP45.09 sender and push.v1 on a physical arm64 Android device, including Doze/background generic attention, authoritative detail/approval, duplicate suppression, rotation/revocation, no-GMS and denied-permission foreground recovery. Provider acceptance alone is insufficient.

Every numbered substep and applicable inherited requirement passes; the complete surface/action/state matrix is exercised. Unfinished required behavior blocks completion. Candidate and producer identities are immutable and all temporary fixtures have the named replacement stage. No scope reduction or design decision is deferred to consumer coding.

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [AND.16](../delivery/lanes/android.md#task-and-16) | [WP-32.00](32-mobile-release-and-store-gates.md#rule-wp-32.00) (full) | [AND.15](../delivery/lanes/android.md#task-and-15) (artifact) |
| [AND.17](../delivery/lanes/android.md#task-and-17) | [WP-32.01](32-mobile-release-and-store-gates.md#rule-wp-32.01) (full) | none |
| [AND.18](../delivery/lanes/android.md#task-and-18) | [WP-32.02](32-mobile-release-and-store-gates.md#rule-wp-32.02) (full) | none |
| [AND.19](../delivery/lanes/android.md#task-and-19) | [WP-32.03](32-mobile-release-and-store-gates.md#rule-wp-32.03) (full) | [AND.08](../delivery/lanes/android.md#task-and-08) (artifact), [AND.09](../delivery/lanes/android.md#task-and-09) (artifact), [AND.10](../delivery/lanes/android.md#task-and-10) (artifact), [AND.11](../delivery/lanes/android.md#task-and-11) (artifact), [AND.12](../delivery/lanes/android.md#task-and-12) (artifact) |
| [AND.20](../delivery/lanes/android.md#task-and-20) | [WP-32.04](32-mobile-release-and-store-gates.md#rule-wp-32.04) (full) | [CON.16](../delivery/lanes/contracts.md#task-con-16) (contract) |
| [AND.21](../delivery/lanes/android.md#task-and-21) | [WP-32.05](32-mobile-release-and-store-gates.md#rule-wp-32.05) (all work except the parts mapped to AND.26) | none |
| [AND.22](../delivery/lanes/android.md#task-and-22) | [WP-32.06](32-mobile-release-and-store-gates.md#rule-wp-32.06) (full) | none |
| [AND.23](../delivery/lanes/android.md#task-and-23) | [WP-32.90](32-mobile-release-and-store-gates.md#rule-wp-32.90) (full)<br>[WP-32](32-mobile-release-and-store-gates.md#rule-wp-32) [PG-24](../../assurance/open-gates-register.md#rule-pg-24) completion-gate paragraph (recheck on distributed artifact) (package-level obligation contribution) | none |
| [AND.26](../delivery/lanes/android.md#task-and-26) | [WP-32](32-mobile-release-and-store-gates.md#rule-wp-32) [PG-24](../../assurance/open-gates-register.md#rule-pg-24) completion-gate paragraph (recheck on distributed artifact) ([PG-24](../../assurance/open-gates-register.md#rule-pg-24) closure)<br>[WP-32.05](32-mobile-release-and-store-gates.md#rule-wp-32.05) (physical/no-GMS/permission evidence half) | [AND.12](../delivery/lanes/android.md#task-and-12) (artifact), [OPS.10](../delivery/lanes/operations.md#task-ops-10) (artifact) |

**Consumers outside this package:** [AND.12](../delivery/lanes/android.md#task-and-12), [OPS.10](../delivery/lanes/operations.md#task-ops-10), [OPS.12](../delivery/lanes/operations.md#task-ops-12), [REL.04](../delivery/lanes/release.md#task-rel-04).

<!-- delivery-graph:end -->

