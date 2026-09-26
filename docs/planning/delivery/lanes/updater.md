# Desktop distribution and update — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

ArcForges.Update: signed feed, staging, atomic apply, rollback, channels and diagnostics.

Tasks: 8 · Owning repositories: DesktopPlatform · Integration owner(s): DesktopPlatform integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [UPD.01](#task-upd-01) | Signed feed and applicable-target selection | producer | M | [PLT.40](platform.md#task-plt-40) (artifact), [FND.05](foundation.md#task-fnd-05) (artifact) | not-started |
| [UPD.02](#task-upd-02) | Background download and staging | producer | L | [UPD.01](#task-upd-01) (artifact) | not-started |
| [UPD.03](#task-upd-03) | Safe apply and atomic activation | producer | L | [UPD.02](#task-upd-02) (artifact), [PLT.32](platform.md#task-plt-32) (artifact) | not-started |
| [UPD.04](#task-upd-04) | Rollback and migration interlock | producer | L | [UPD.03](#task-upd-03) (artifact), [PLT.04](platform.md#task-plt-04) (artifact) | not-started |
| [UPD.05](#task-upd-05) | Channels, staged rollout and security updates | producer | M | [UPD.01](#task-upd-01) (artifact) | not-started |
| [UPD.06](#task-upd-06) | Diagnostics and preserving data on uninstall | producer | S | [PLT.47](platform.md#task-plt-47) (artifact), [FND.05](foundation.md#task-fnd-05) (artifact) | not-started |
| [UPD.07](#task-upd-07) | Production catalog and Android distribution trust | producer | M | [UPD.01](#task-upd-01) (artifact), [CON.16](contracts.md#task-con-16) (contract) | not-started |
| [UPD.08](#task-upd-08) | Publish ArcForges.Update and verify the complete lifecycle | acceptance | M | [UPD.01](#task-upd-01) (artifact), [UPD.02](#task-upd-02) (artifact), [UPD.03](#task-upd-03) (artifact), [UPD.04](#task-upd-04) (artifact), [UPD.05](#task-upd-05) (artifact), [UPD.06](#task-upd-06) (artifact), [UPD.07](#task-upd-07) (artifact), [PRF.01](runtime-proofs.md#task-prf-01) (artifact), [POL.09](policy.md#task-pol-09) (artifact) | not-started |

## Tasks

<a id="task-upd-01"></a>

### UPD.01 — Signed feed and applicable-target selection

**Outcome.** update.feed.v1 canonical JSON envelope validation, trust (ECDSA P256/SHA256 over RFC8785-canonical payload), product/RID/channel selection, compatibility and anti-replay per architecture 14 SS8.1; only an admitted target from a current trusted feed can enter download.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/upd-01` and ledger record `ledger/tasks/upd-01.md` in the Plan repository; task branch `task/upd-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-53.00](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.00) — full |
| Provides | signed-feed |
| Start prerequisites | **artifact** [PLT.40](platform.md#task-plt-40) — secure key-handling/signature-verification patterns from Security. *Why:* verifying the feed signature and managing trusted key rotation reuses the same secure-storage/crypto discipline Security establishes, applied to a public trust-key set rather than user secrets.<br>**artifact** [FND.05](foundation.md#task-fnd-05) — reason-code registry. *Why:* every feed refusal (unsigned/expired/duplicate/hash-invalid/wrong product/RID) returns a registered reason code. |
| Entry condition | [ADOPT.02.updater](adoption.md#task-adopt-02-updater) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.10](release.md#task-rel-10), [UPD.02](#task-upd-02), [UPD.05](#task-upd-05), [UPD.07](#task-upd-07), [UPD.08](#task-upd-08) |
| Permitted substitutes | [SUB-test-signed-update-feed](../substitutes.md#sub-test-signed-update-feed) |
| Write scope | `DesktopPlatform:src/Update/ArcForges.Update/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline tests: unsigned/expired/duplicate/hash-invalid feed, removed and policy-blocked version independently, wrong product/RID, older signed feed - all against a test-signed fixture feed, no live update.feed.v1 server. |
| Completion evidence | Signed feed schema, replay and blocked-version cases. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: src/Update/ does not exist anywhere in the repository yet. |

<a id="task-upd-02"></a>

### UPD.02 — Background download and staging

**Outcome.** Background check, range resume, delta reconstruct with verified full fallback, bounded staging and final hash/signature checks; a complete verified candidate is staged without changing the active installation.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/upd-02` and ledger record `ledger/tasks/upd-02.md` in the Plan repository; task branch `task/upd-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-53.01](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.01) — full |
| Provides | download-staging |
| Start prerequisites | **artifact** [UPD.01](#task-upd-01) — signed feed/target selection. *Why:* download operates on the admitted target the feed task resolves. |
| Entry condition | [ADOPT.02.updater](adoption.md#task-adopt-02-updater) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [UPD.03](#task-upd-03), [UPD.08](#task-upd-08) |
| Write scope | `DesktopPlatform:src/Update/ArcForges.Update/**` |
| Validation | Offline tests: interrupt every transfer boundary, tamper base/delta/target, storage exhaustion - against a local test HTTP fixture server, not a live download surface; launch-remains-available assertion. |
| Completion evidence | Actual resumed download, delta/full reconstruction and tamper refusal. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-upd-03"></a>

### UPD.03 — Safe apply and atomic activation

**Outcome.** The real lifecycle shutdown handshake (await all affected instances exiting without holding domain locks) plus the selected Velopack adapter drive download->verify->stage->atomic-switch->retain-previous-launchable-version; busy work defers apply; restart sees either the previous or the new verified installation, never a partial one.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/upd-03` and ledger record `ledger/tasks/upd-03.md` in the Plan repository; task branch `task/upd-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-53.02](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.02) — full |
| Provides | safe-apply |
| Start prerequisites | **artifact** [UPD.02](#task-upd-02) — staged verified candidate. *Why:* apply activates what staging produced.<br>**artifact** [PLT.32](platform.md#task-plt-32) — lifecycle/shutdown handshake ([WP-10.06](../../work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.06)). *Why:* [UC-02](../../../architecture/14-build-packaging-and-release.md#rule-uc-02)/[UP-03](../../../requirements/10-distribution-update-and-support.md#rule-up-03) explicitly require coordinating with 'the real lifecycle shutdown handshake' - this is a genuine Shell->Updater dependency within the DesktopPlatform repository, not an external one. |
| Entry condition | [ADOPT.02.updater](adoption.md#task-adopt-02-updater) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [UPD.04](#task-upd-04), [UPD.08](#task-upd-08) |
| Write scope | `DesktopPlatform:src/Update/ArcForges.Update/**` |
| Shared resources | [RES-desktopplatform-build-config](../shared-resources.md#res-desktopplatform-build-config) (append) |
| Validation | Offline/local tests: long render/capture, unsaved edit, peer unavailable, canceled restart and kill at each activation boundary - simulated process-level, not a real installed multi-instance product (that is UPD.08's job). |
| Completion evidence | Busy/unsaved work deferral and interrupted apply. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists; Velopack is not yet a dependency anywhere in Directory.Packages.props. |

<a id="task-upd-04"></a>

### UPD.04 — Rollback and migration interlock

**Outcome.** The update journal is persisted outside install/data files; uses the existing data-store migration read/write compatibility horizon before rollback; user data survives; an incompatible automatic rollback refuses with a recovery reason instead of opening data with the old binary.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/upd-04` and ledger record `ledger/tasks/upd-04.md` in the Plan repository; task branch `task/upd-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-53.03](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.03) — full<br>[WP-53](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53) Versioned installation update journal persisted outside install/data files; the updater never writes product data or implements schema migration (SS6 impacts, [BR-05](../../../architecture/14-build-packaging-and-release.md#rule-br-05)) — package-level obligation contribution |
| Provides | rollback-migration-interlock |
| Start prerequisites | **artifact** [UPD.03](#task-upd-03) — safe apply/activation. *Why:* rollback is the inverse of apply, built on the same activation mechanism.<br>**artifact** [PLT.04](platform.md#task-plt-04) — migration runner's read/write compatibility-horizon concept ([WP-07.03](../../work-packages/07-local-persistence-foundation.md#rule-wp-07.03)). *Why:* [BR-05](../../../architecture/14-build-packaging-and-release.md#rule-br-05) says explicitly: 'use the existing data-store migration read/write compatibility horizon before rollback' - this is a direct, real Persistence->Updater contract dependency within the DesktopPlatform repository, not invented by the updater. |
| Entry condition | [ADOPT.02.updater](adoption.md#task-adopt-02-updater) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [UPD.08](#task-upd-08) |
| Write scope | `DesktopPlatform:src/Update/ArcForges.Update/**` |
| Validation | Offline tests: fail pre-migration startup, fail during migration, current store outside previous reader/writer horizon, interrupted rollback. |
| Completion evidence | Compatible rollback, incompatible migration refusal and launch recovery. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-upd-05"></a>

### UPD.05 — Channels, staged rollout and security updates

**Outcome.** Explicit channel selection, stable installation-based rollout assignment, halting bad versions and respecting minimum-version grace, using activated [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44) policy and the [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) advisory process; urgency cannot force unsafe restart.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/upd-05` and ledger record `ledger/tasks/upd-05.md` in the Plan repository; task branch `task/upd-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-53.04](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.04) — full |
| Provides | channels-rollout |
| Start prerequisites | **artifact** [UPD.01](#task-upd-01) — signed feed. *Why:* channel/rollout data rides in the same feed envelope. |
| Entry condition | [ADOPT.02.updater](adoption.md#task-adopt-02-updater) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [POL.09](policy.md#task-pol-09) — real activated Cloud policy distribution and the [WP-45](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45) advisory process. *Why:* under the substitute rules, a contract-bound fixture of the policy shape unblocks the start; real cross-area integration with the commerce, policy and operations lanes policy/advisory pipeline is deferred to a real scenario, not a start blocker. |
| Unblocks | [UPD.08](#task-upd-08) |
| Permitted substitutes | [SUB-updater-policy-fixture](../substitutes.md#sub-updater-policy-fixture) |
| Write scope | `DesktopPlatform:src/Update/ArcForges.Update/**` |
| Validation | Offline tests: both channel directions, unchanged rollout assignment across restart, blocked target after download, emergency offer during critical work, expired grace - all against the fixture policy document above. |
| Completion evidence | Stable rollout, channels and expedited security/grace behavior. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists; the commerce, policy and operations lanes [WP-44](../../work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44)/45 are equally unstarted per the family-wide WP02 baseline, so the fixture substitute is presently the ONLY way to make progress here at all. |

<a id="task-upd-06"></a>

### UPD.06 — Diagnostics and preserving data on uninstall

**Outcome.** check/download/verify/stage/apply/defer/fail/rollback recorded with stable reasons and correlation, no user content; uninstall never implicitly removes user data or the recovery journal.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/upd-06` and ledger record `ledger/tasks/upd-06.md` in the Plan repository; task branch `task/upd-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / S |
| Obligations | [WP-53.05](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.05) — full |
| Provides | update-diagnostics |
| Start prerequisites | **artifact** [PLT.47](platform.md#task-plt-47) — emission/dimension surface ([WP-12.00](../../work-packages/12-observability-foundation.md#rule-wp-12.00)). *Why:* update activity is emitted through the shared Observability surface, not a bespoke logging path.<br>**artifact** [FND.05](foundation.md#task-fnd-05) — reason-code registry. *Why:* every recorded outcome uses a registered reason code. |
| Entry condition | [ADOPT.02.updater](adoption.md#task-adopt-02-updater) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [UPD.08](#task-upd-08) |
| Write scope | `DesktopPlatform:src/Update/ArcForges.Update/**` |
| Shared resources | [RES-desktopplatform-policy-data](../shared-resources.md#res-desktopplatform-policy-data) (append) |
| Validation | Offline tests: independent expected activity sequence; uninstall/reinstall preserving product data and recovery journal (simulated file-system scenario). |
| Completion evidence | Update reason-code sequence and data-preserving uninstall. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Nothing exists. |

<a id="task-upd-07"></a>

### UPD.07 — Production catalog and Android distribution trust

**Outcome.** Production catalog/revocation and Android direct-update feeds using WP03 formats, with signing custody/rotation and artifact URI/certificate inventory; registers per-product desktop auth URI schemes in signed installers.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/upd-07` and ledger record `ledger/tasks/upd-07.md` in the Plan repository; task branch `task/upd-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / M |
| Obligations | [WP-53.07](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.07) — full |
| Provides | production-catalog-trust |
| Start prerequisites | **artifact** [UPD.01](#task-upd-01) — signed feed mechanics. *Why:* this substep is where the test-signed feed's real production counterpart is built.<br>**contract** [CON.16](contracts.md#task-con-16) — native auth exceptions, catalog/index/revocation/update/realm schemas and independent signed vectors. *Why:* the producer-artifacts matrix names [WP-03.07](../../work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.07) as the exact source for these formats; fixture keys are WP02/06, no production key prerequisite for starting. |
| Entry condition | [ADOPT.02.updater](adoption.md#task-adopt-02-updater) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.10](release.md#task-rel-10), [UPD.08](#task-upd-08) |
| Write scope | `DesktopPlatform:src/Update/ArcForges.Update/**`<br>`DesktopPlatform:eng/packaging/**` |
| Validation | Offline tests: real signatures/shards/monotonic revision, current/previous trust, Android certificate match and desktop callback registration from installed packages - against test key material; production key custody itself is an operational/local-opt-in concern, not a CI-testable behavior. |
| Completion evidence | WP50 can replace WP32/WP41 fixture keys with production feeds without changing schemas. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: eng/packaging/release_channels.py already exists (confirmed, used by the current publish-nuget.yml workflow) but only handles the existing NuGet publisher identity, not update-feed production signing. |

<a id="task-upd-08"></a>

### UPD.08 — Publish ArcForges.Update and verify the complete lifecycle

**Outcome.** ArcForges.Update is packed with its verified closure, restored into clean consumer applications, and exercised through a real Tier 1 install->staged update->restart->rollback cycle against a test-signed feed, including interrupted download/apply, blocked versions, signature corruption and wrong data horizon.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/upd-08` and ledger record `ledger/tasks/upd-08.md` in the Plan repository; task branch `task/upd-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Package acceptance | Records the [WP-53](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-53.90](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.90) — full |
| Provides | update-package |
| Start prerequisites | **artifact** [UPD.01](#task-upd-01) — signed feed. *Why:* publish needs the complete substep set.<br>**artifact** [UPD.02](#task-upd-02) — download/staging. *Why:* same.<br>**artifact** [UPD.03](#task-upd-03) — safe apply. *Why:* same.<br>**artifact** [UPD.04](#task-upd-04) — rollback/migration interlock. *Why:* same.<br>**artifact** [UPD.05](#task-upd-05) — channels/rollout. *Why:* same.<br>**artifact** [UPD.06](#task-upd-06) — diagnostics/uninstall. *Why:* same.<br>**artifact** [UPD.07](#task-upd-07) — production catalog/trust. *Why:* same.<br>**artifact** [PRF.01](runtime-proofs.md#task-prf-01) — a real signed candidate AOT application to install/update. *Why:* WP53's own SS2 lists WP02/06 as supplying 'signed candidate pipeline and real AOT applications to install' - the full lifecycle test genuinely needs an installable product, which only exists once the early platform runtime proofs and at least one product's own AOT publish exist; this is a real integration-time (not code-start) need, consistent with implementation-sequence.md listing WP53 after 45 and before 46 in the serial schedule.<br>**artifact** [POL.09](policy.md#task-pol-09) — client policy resolution library. *Why:* the updater verifies real policy distribution before its acceptance |
| Entry condition | [ADOPT.02.updater](adoption.md#task-adopt-02-updater) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [REL.10](release.md#task-rel-10) — production installers, production domains/signing and the full release matrix. *Why:* [WP-53.90](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.90)'s own gate explicitly leaves this to WP50.02; no placeholder producer is admitted at WP50 but WP53 itself only proves mechanics on a test-signed feed. |
| Unblocks | [POL.07](policy.md#task-pol-07), [REL.01](release.md#task-rel-01), [REL.02](release.md#task-rel-02), [REL.03](release.md#task-rel-03) |
| Write scope | `DesktopPlatform:eng/packaging/packages.json` |
| Shared resources | [RES-desktopplatform-package-inventory](../shared-resources.md#res-desktopplatform-package-inventory) (append) |
| Validation | [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017): Tier 1 (Windows/Linux) real install/apply/rollback cycle is the kind of local, affected-scope, once, existing-environment runtime check [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) permits and expects to be recorded, distinct from hosted CI; Tier 2 (macOS) follows the existing recorded waiver process, never macOS CI. |
| Completion evidence | Owned artifact and real-integration receipt per [WP-53.90](../../work-packages/53-desktop-distribution-and-update.md#rule-wp-53.90). |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: Not in packages.json; no product anywhere in the family is yet installable/updatable to test against. |
