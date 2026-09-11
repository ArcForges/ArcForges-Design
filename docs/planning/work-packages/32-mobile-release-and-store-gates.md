<a id="rule-wp-32"></a>

# WP-32 — Mobile Release Engineering and Store Gates

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Integration after real Cloud prerequisites
> Upstream: `31` · Downstream: `50`

> **Goal.** Get a real Android release artifact through every gate: dependency closure and provenance (**[F-023](../../assurance/open-gates-register.md#rule-f-023)**), consumption-only conformance (**[V-09](../../assurance/phase-1-official-verification.md#rule-v-09)**), the runtime posture confirmed from the artifact (**[V-04](../../assurance/phase-1-official-verification.md#rule-v-04)**), and build-verifiable commerce prohibitions — none of which is satisfied by reading a document.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Mobile. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: RN/Hermes artifact and real generated service clients with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The Android release build and signing; the store listing and its category-fit confirmation; the **[F-023](../../assurance/open-gates-register.md#rule-f-023)** dependency closure and provenance audit; the **[V-09](../../assurance/phase-1-official-verification.md#rule-v-09)** consumption-only conformance confirmation; the commerce-prohibition build check; on-device release verification; and the iOS position stated honestly.

**Out of scope.** Any in-app purchase or billing integration — prohibited (**[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**). iOS build activation, which remains deferred (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**).

**Why this package exists.** The initial closure gate executes before the first mobile artifact in WP06, repeats for dependency changes in WP30, and converges here with runtime/store gates for the final distributable. They are not documentation tasks: **[F-023](../../assurance/open-gates-register.md#rule-f-023)** requires an audited transitive closure, **[V-09](../../assurance/phase-1-official-verification.md#rule-v-09)** requires a review outcome, and **[V-04](../../assurance/phase-1-official-verification.md#rule-v-04)** requires inspecting a produced binary.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md) | **[F-023](../../assurance/open-gates-register.md#rule-f-023)**, **[VG-07](../../assurance/open-gates-register.md#rule-vg-07)**, **[VG-13](../../assurance/open-gates-register.md#rule-vg-13)** and their owners and triggers |
| [`../../assurance/release-gates.md`](../../assurance/release-gates.md) `§6.4` | The mobile release gate set |
| [`../../requirements/10-distribution-update-and-support.md`](../../requirements/10-distribution-update-and-support.md) `§1.1` | The mobile platform matrix and its obligations |
| **[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](../../assurance/phase-1-official-verification.md#rule-v-09)** | Consumption-only posture and its verification requirement |
| [WP-31](31-arcchat-mobile-android.md#rule-wp-31) output | A complete application to release |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The complete direct and transitive dependency closure is verified before the first artifact is produced** — **[F-023](../../assurance/open-gates-register.md#rule-f-023)**. |
| BR-02 | **On discovering a conflicting contribution or dependency, the issue is registered and returned for decision** (**[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**). Silently adding an exception, changing the licence or dropping the mobile target is prohibited. |
| <a id="rule-br-03"></a>BR-03 | **No purchase surface, embedded checkout, store billing integration, external purchase call to action, or licence-key or purchase-token unlock path exists in any build path** (**[D-022](../../decisions/phase-1-foundation-decisions.md#rule-d-022)**). |
| BR-04 | **A build-time and CI check asserts every prohibition** in [BR-03](#rule-br-03). |
| BR-05 | **The runtime is confirmed by inspecting the produced release artifact**, not by reading the project file (**[V-04](../../assurance/phase-1-official-verification.md#rule-v-04)**). |
| BR-06 | **CI builds the release artifact and runs on-device smoke tests.** A successful debug build is not a pass. |
| BR-07 | **The store developer account is established under the intended long-term owning identity**, not casually under a personal account. |
| BR-08 | **A store listing is distribution, never a commerce channel.** |
| BR-09 | **iOS is not claimed as compiled or tested** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**). |
| BR-10 | **The product's own update system is unaffected by store distribution** — mobile follows store update mechanics without that becoming the desktop model. |

---

## 4. Projects, directories, files and major types affected

All paths are relative to ArcForges-Mobile.

| Location | Deliverable |
|---|---|
| android/, package.json, package-lock.json | Locked release variant, version code/name, Hermes and native module closure |
| eng/signing/, eng/release/ | CI-only signing, signed AAB and device-test APK, store metadata/privacy/support/update/rollback procedure |
| eng/policy/ | Consumption-only route/import checks and source/licence closure |
| tests/device/, tests/contract/ | Release-artifact runtime, migration, recovery and full provider loop |
| eng/verification/ | NOTICE/SBOM/provenance, device measurements, store review and exact artifact receipts |
| ios/ | Deferred Apple adapter/entitlement/signing/store/device activation specification |

---

## 5. Required implementation work

**Order:** [WP-32.02](#rule-wp-32.02) validates the final locked closure before [WP-32.00](#rule-wp-32.00) produces its artifact; run [WP-32.01](#rule-wp-32.01)/03/05 on that artifact, then [WP-32.04](#rule-wp-32.04) submission and [WP-32.06](#rule-wp-32.06) status verification. The earlier first-artifact gate in WP06 is not deferred until this package.

<a id="rule-wp-32.00"></a>

### WP-32.00 — Release build and signing


**What must be fully done.** After final closure approval, build the pinned RN Android release in clean CI. Produce signed AAB for store and signed release APK for device tests with identical JS/native dependency closure; stamp app/protocol/config/artifact identities. Signing keys stay in the release credential store. Attach NOTICE, source/SBOM and hashes.

**Testing requirements.** Verify signatures, version stamps, reproducible dependency/asset closure and installation/upgrade from the supported previous version; record any nondeterministic signing envelope separately.

**Completion gate.** Signed installable release artifacts have exact source/lock/build provenance and pass the prior closure gate.

<a id="rule-wp-32.01"></a>

### WP-32.01 — Runtime posture confirmation


**What must be fully done.** Inspect the packaged Hermes bytecode, Hermes/native libraries, arm64 ABI and release/debug settings; run the exact release APK on physical devices. Record RN/New Architecture/native template identities and the framework-upgrade re-verification trigger.

**Testing requirements.** Artifact inspection plus device navigation/storage/passkey/transport/push exercise; no Mono/.NET mobile runtime or desktop native package; iOS remains unbuilt.

**Completion gate.** The real RN/Hermes artifact closes [VG-07](../../assurance/open-gates-register.md#rule-vg-07) and records the [VG-08](../../assurance/open-gates-register.md#rule-vg-08) upgrade obligation.

<a id="rule-wp-32.02"></a>

### WP-32.02 — Dependency closure and provenance


**What must be fully done.** Before [WP-32.00](#rule-wp-32.00), revalidate the final npm/Gradle/native/generated public closure including source and NOTICE. Compare with WP06/WP30 evidence, review all differences and produce the final SBOM; reject unresolved licence/provenance items.

**Testing requirements.** Complete transitive closure with licence/source positions and negative AGPL/unknown-native import fixtures.

**Completion gate.** [F-023](../../assurance/open-gates-register.md#rule-f-023) is passed for the exact final closure before its first build and any changed closure is gated again.

<a id="rule-wp-32.03"></a>

### WP-32.03 — Commerce prohibition check


**What must be fully done.** Enforce all five existing consumption-only prohibitions in native routes, deep links, bundles, dependencies and store metadata: purchase surface, embedded checkout, store billing, external purchase CTA and licence/purchase-token unlock. Allow only the designated non-commerce account/security/support routes.

**Testing requirements.** One negative fixture per prohibition, including remote-config/link attempts and hidden route navigation.

**Completion gate.** All prohibited paths fail policy checks and are absent from the actual release artifact.

<a id="rule-wp-32.04"></a>

### WP-32.04 — Store category fit and consumption-only conformance


**What must be fully done.** Submit under the intended long-term owning store identity with category, privacy/data collection, deletion/support, notification/file permissions and consumption-only metadata matched to behavior. Record actual review outcome. Establish staged rollout, supported-version communication and a forward rescue release restoring prior behavior with a greater versionCode and verified current-data compatibility; server compatibility preserves the public client window and pending commands.

**Testing requirements.** Store review evidence, privacy/support links, staged rollout/rollback exercise and previous-version migration/device result.

**Completion gate.** Actual category-fit and consumption-only review closes [VG-13](../../assurance/open-gates-register.md#rule-vg-13); no guideline reading is reported as store approval.

<a id="rule-wp-32.05"></a>

### WP-32.05 — On-device verification


**What must be fully done.** Run the full WP31 product/CF/desktop loop and all mobile initial-state/recovery scenarios on supported physical low/mid-tier arm64 devices using the release APK. Measure launch/RAM/frame behavior, long lists/streams, weak network, storage pressure and screen-reader/dynamic-text behavior against the existing quality contract.

**Testing requirements.** Record exact devices/OS/artifact and real providers; exercise kill during send/refresh/migration, expiry/revoke, missed push, hostile links, pending approvals and rollback upgrade.

**Completion gate.** Every applicable quality, accessibility, compatibility and commercial companion gate passes on the release closure.

<a id="rule-wp-32.06"></a>

### WP-32.06 — iOS position


**What must be fully done.** Keep the selected iOS template, app/service/storage interfaces, AuthenticationServices/Keychain/APNs/app-link/file adapter mapping, signing/entitlements/store metadata and physical-device activation matrix documented. CI build/submission remain disabled until the existing activation gates run.

**Testing requirements.** Check repository/release metadata claims and gate triggers; no successful iOS compile or test is asserted.

**Completion gate.** iOS is architecture-present/build-deferred with a concrete activation procedure and truthful status.

<a id="rule-wp-32.90"></a>
### WP-32.90 — Verify the owned artifact and real integration


**What must be fully done.** Collect the exact signed RN artifact and all preceding release, provider, store and support/rollback receipts in the candidate manifest.

**Testing requirements.** Verify receipts identify that same closure and no gate is satisfied by a mock or a debug build.

**Completion gate.** Android is deliverable only when every applicable runtime, licence, device, commerce and store gate is actually passed; iOS remains deferred.

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None |
| Protocol | The shipped mobile client version enters the supported window |
| UI | Store listing assets and metadata |
| Security | Signing, credential custody and the dependency closure |
| Platform | Android release path proven; iOS honestly deferred |
| Migration | Mobile cache migration across shipped versions |
| Compatibility | The minimum supported mobile client is declared |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| CI release build, signature verification and version stamp | [WP-32.00](#rule-wp-32.00) |
| Artifact runtime inspection record | [WP-32.01](#rule-wp-32.01) |
| Dependency closure report with licence positions and SBOM | [WP-32.02](#rule-wp-32.02) |
| Five negative fixtures failing the build | [WP-32.03](#rule-wp-32.03) |
| Recorded review outcome and requirement checklist | [WP-32.04](#rule-wp-32.04) |
| Device matrix results, budget measurements, accessibility record | [WP-32.05](#rule-wp-32.05) |
| Documentation scan for iOS claims | [WP-32.06](#rule-wp-32.06) |

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-32.90](#rule-wp-32.90) and all inherited domain-specific gates must pass on the same candidate closure. Inspect and run the real signed Android artifact; verify compiled JS bytecode/runtime and platform behavior without claiming machine-code AOT equivalence or iOS delivery.

**All of the following, with recorded evidence:**

1. CI produces a signed release artifact reproducibly, with signing credentials held only in the release credential store.
2. The runtime is confirmed from the produced artifact — satisfying [VG-07](../../assurance/open-gates-register.md#rule-vg-07).
3. **100 % of the direct and transitive dependency closure has a licence position with no unresolved item** — satisfying [F-023](../../assurance/open-gates-register.md#rule-f-023).
4. All five commerce prohibitions are machine-checked with negative fixtures failing the build.
5. Store category fit and consumption-only conformance are confirmed by review outcome — satisfying [VG-13](../../assurance/open-gates-register.md#rule-vg-13).
6. The release artifact passes on-device smoke tests across the device matrix, meets cold-start, memory and weak-network budgets, and passes accessibility verification.
7. No iOS build or test claim exists anywhere, and the activation re-verification obligation is recorded.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-31](31-arcchat-mobile-android.md#rule-wp-31)

**Downstream — consumers of these released outputs.**

- [WP-50](50-full-platform-production-release.md#rule-wp-50)


---
