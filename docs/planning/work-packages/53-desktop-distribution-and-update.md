<a id="rule-wp-53"></a>

# WP-53 — Desktop Distribution, Update Client and Channels

> Status: **Authoritative** — Phase 2
> Layer: Planning · Work package
> Phase: J — Platform and client integration
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Deliver ArcForges.Update as a real shared producer for all three professional desktop products before final release verification.

## 1. Scope and purpose

Own desktop update discovery, verified download/delta, staging, safe application, rollback interlock, channels, rollout and update diagnostics. Use the selected Velopack adapter; Android/Play remains Mobile-owned. Product UI/domain state and Cloud policy production stay with their existing owners. WP50 consumes this implementation and proves the production release matrix.

## 2. Required inputs and dependencies

| Input | Why |
|---|---|
| [Distribution requirements](../../requirements/10-distribution-update-and-support.md), [UP-01](../../requirements/10-distribution-update-and-support.md#rule-up-01)–[UP-11](../../requirements/10-distribution-update-and-support.md#rule-up-11) | All accepted update, recovery and support behavior |
| [Build/update architecture](../../architecture/14-build-packaging-and-release.md#8-update-client-architecture), [UC-01](../../architecture/14-build-packaging-and-release.md#rule-uc-01)–[UC-10](../../architecture/14-build-packaging-and-release.md#rule-uc-10) and §8.1 | Fixed client, signed-feed and recovery profile |
| [Producer matrix](../producer-artifacts-and-integration.md) | Exact packages, fixture scope and real replacement |
| WP02/06 | Signed candidate pipeline and real AOT applications to install |
| WP07/10/11/12 | Migration journal, lifecycle shell, signature/security mechanisms and reason-code registry |
| WP44/45 | Activated compatibility/rollout policy and security advisory process |

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | Build/pack once; install only the immutable tested bytes. |
| <a id="rule-br-02"></a>BR-02 | Launch/local saves are not blocked by a failed update check. Apply never forces loss of work. |
| <a id="rule-br-03"></a>BR-03 | Recheck product/RID/signatures/policy and data-compatibility immediately before apply or rollback. |
| <a id="rule-br-04"></a>BR-04 | A test feed proves updater mechanics; it does not prove production signing or commercial activation. |
| <a id="rule-br-05"></a>BR-05 | The updater never writes product data or implements schema migration. |

## 4. Projects, directories, files and major types affected

| Owner-relative location | Output |
|---|---|
| DesktopPlatform `src/Update/ArcForges.Update/` | Domain-free feed, staged update and Velopack adapter; fixed update-state and reason projections |
| DesktopPlatform `eng/packaging/`, `tests/UpdateConsumers/` | Package admission, signed test-feed fixtures, actual install/apply/rollback receipts |
| Each desktop product `*.Infrastructure/`, `*.Desktop/` | Consume exact Update package, expose pending/deferred update and channel selection through its native shell |
| Existing WP02 release metadata and WP44 policy | Feed signing/configuration inputs; no new Cloud update daemon |

## 5. Required implementation work

<a id="rule-wp-53.00"></a>

### WP-53.00 — Signed feed and applicable target

**What must be fully done.** Implement architecture 14 §8.1 feed validation, trust, product/RID/channel selection, compatibility and anti-replay. [AF-01](../../architecture/14-build-packaging-and-release.md#rule-af-01)–[AF-07](../../architecture/14-build-packaging-and-release.md#rule-af-07) and [UC-07](../../architecture/14-build-packaging-and-release.md#rule-uc-07) apply.

**Testing requirements.** Unsigned/expired/duplicate/hash-invalid feed, removed and policy-blocked version independently, wrong product/RID and older signed feed.

**Completion gate.** Only an admitted target from a current trusted feed can enter download.

<a id="rule-wp-53.01"></a>

### WP-53.01 — Background download and staging

**What must be fully done.** Implement [UP-01](../../requirements/10-distribution-update-and-support.md#rule-up-01)/02 and [UC-01](../../architecture/14-build-packaging-and-release.md#rule-uc-01): background check, range resume, delta reconstruct with verified full fallback, bounded staging and final hash/signature checks.

**Testing requirements.** Interrupt every transfer boundary, tamper base/delta/target, storage exhaustion; ensure launch remains available.

**Completion gate.** A complete verified candidate is staged without changing the active installation.

<a id="rule-wp-53.02"></a>

### WP-53.02 — Safe apply and atomic activation

**What must be fully done.** Implement [UC-02](../../architecture/14-build-packaging-and-release.md#rule-uc-02)/03, [UP-03](../../requirements/10-distribution-update-and-support.md#rule-up-03)/04 and [LF-08](../../requirements/09-shared-desktop-experience.md#rule-lf-08)/09 via the real lifecycle shutdown handshake and selected Velopack adapter. Await all affected instances exiting; do not wait while holding domain locks.

**Testing requirements.** Long render/capture, unsaved edit, peer unavailable, canceled restart and kill at each activation boundary.

**Completion gate.** Busy work defers apply; restart sees either previous verified installation or new verified installation, never a partial one.

<a id="rule-wp-53.03"></a>

### WP-53.03 — Rollback and migration interlock

**What must be fully done.** Implement [UC-04](../../architecture/14-build-packaging-and-release.md#rule-uc-04)/05/06 and [UP-05](../../requirements/10-distribution-update-and-support.md#rule-up-05)/06/08. Persist the update journal outside install/data files; use the existing data-store migration read/write compatibility horizon before rollback.

**Testing requirements.** Fail pre-migration startup, fail during migration, current store outside previous reader/writer horizon and interrupted rollback.

**Completion gate.** User data survives; incompatible automatic rollback refuses with a recovery reason instead of opening data with the old binary.

<a id="rule-wp-53.04"></a>

### WP-53.04 — Channels, staged rollout and security updates

**What must be fully done.** Implement [UC-07](../../architecture/14-build-packaging-and-release.md#rule-uc-07)/08/09, [RC-01](../../requirements/10-distribution-update-and-support.md#rule-rc-01) and [UP-09](../../requirements/10-distribution-update-and-support.md#rule-up-09)/10/11 using actual 44 policy and 45 advisory process. Explicit channel selection, stable installation assignment, halt bad versions and respect minimum-version grace.

**Testing requirements.** Both channel directions, unchanged rollout assignment across restart, blocked target after download, emergency offer during critical work and expired grace.

**Completion gate.** Urgency cannot force unsafe restart; denied Cloud operations explain the update/grace requirement while permitted local work remains available.

<a id="rule-wp-53.05"></a>

### WP-53.05 — Diagnostics and preserving data on uninstall

**What must be fully done.** Implement [UC-10](../../architecture/14-build-packaging-and-release.md#rule-uc-10), [UP-07](../../requirements/10-distribution-update-and-support.md#rule-up-07) and existing support activity policy. Record check/download/verify/stage/apply/defer/fail/rollback with stable reasons and correlation; no user content.

**Testing requirements.** Independent expected activity sequence and uninstall/reinstall preserving product data and recovery journal.

**Completion gate.** Every outcome is diagnosable and uninstall never removes user data implicitly.

<a id="rule-wp-53.07"></a>

### WP-53.07 — Production catalog and Android distribution trust

**What must be fully done.** Produce production catalog/revocation and Android direct-update feeds using WP03 formats. Keep signing custody/rotation and artifact URI/certificate inventory; register per-product desktop auth URI schemes in signed installers.

**Testing requirements.** Real signatures/shards/monotonic revision, current/previous trust, Android certificate match and desktop callback registration from installed packages.

**Completion gate.** WP50 can replace WP32/WP41 fixture keys with production feeds without changing schemas; no backwards dependency on this step.

<a id="rule-wp-53.90"></a>

### WP-53.90 — Verify the owned artifact and real integration

**What must be fully done.** Pack ArcForges.Update with its verified closure, restore it into clean consumer applications and exercise the complete update lifecycle through the actual installed artifacts. Record exact producer/consumer identities and all UC/UP rule evidence.

**Testing requirements.** Real Tier 1 install→staged update→restart→rollback against test-signed feed, with interrupted download/apply, blocked versions, signature corruption and wrong data horizon. Tier 2 follows the existing recorded waiver process.

**Completion gate.** All numbered substeps and package-only updater consumers pass. WP50.02 remains responsible for real product installers, production domains/signing and the full release matrix; no placeholder producer is admitted.

## 6. Impacts

| Dimension | Impact |
|---|---|
| Persistence | Versioned installation update journal and existing migration compatibility interlock; no product-data mutation by updater |
| Protocol | Signed immutable feed profile in architecture 14; lifecycle coordination uses existing local proto |
| Security | Verify trust, hashes, anti-replay and artifact identity before executing any updater action |
| UI | Background update/pending/deferred/failure/channel consequences with native shell |
| Recovery | Keep previous verified package and stable launch path until healthy startup; no blind rollback after incompatible migration |

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-53.90](#rule-wp-53.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

| Evidence | Produced by |
|---|---|
| Signed feed schema, replay and blocked-version cases | [WP-53.00](#rule-wp-53.00) |
| Actual resumed download, delta/full reconstruction and tamper refusal | [WP-53.01](#rule-wp-53.01) |
| Busy/unsaved work deferral and interrupted apply | [WP-53.02](#rule-wp-53.02) |
| Compatible rollback, incompatible migration refusal and launch recovery | [WP-53.03](#rule-wp-53.03) |
| Stable rollout, channels and expedited security/grace behavior | [WP-53.04](#rule-wp-53.04) |
| Update reason-code sequence and data-preserving uninstall | [WP-53.05](#rule-wp-53.05) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-53.90](#rule-wp-53.90) |



## 8. Completion gate

Every 53.00–53.05 and 53.90 gate passes with recorded evidence on the admitted platform set. [UP-01](../../requirements/10-distribution-update-and-support.md#rule-up-01)–[UP-11](../../requirements/10-distribution-update-and-support.md#rule-up-11) and [UC-01](../../architecture/14-build-packaging-and-release.md#rule-uc-01)–[UC-10](../../architecture/14-build-packaging-and-release.md#rule-uc-10) each resolve to the tests above. Required product/data behavior cannot remain an implementation-time design decision. Production release evidence remains WP50-owned.

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [UPD.01](../delivery/lanes/updater.md#task-upd-01) | [WP-53.00](53-desktop-distribution-and-update.md#rule-wp-53.00) (full) | [PLT.40](../delivery/lanes/platform.md#task-plt-40) (artifact), [FND.05](../delivery/lanes/foundation.md#task-fnd-05) (artifact) |
| [UPD.02](../delivery/lanes/updater.md#task-upd-02) | [WP-53.01](53-desktop-distribution-and-update.md#rule-wp-53.01) (full) | none |
| [UPD.03](../delivery/lanes/updater.md#task-upd-03) | [WP-53.02](53-desktop-distribution-and-update.md#rule-wp-53.02) (full) | [PLT.32](../delivery/lanes/platform.md#task-plt-32) (artifact) |
| [UPD.04](../delivery/lanes/updater.md#task-upd-04) | [WP-53.03](53-desktop-distribution-and-update.md#rule-wp-53.03) (full)<br>[WP-53](53-desktop-distribution-and-update.md#rule-wp-53) Versioned installation update journal persisted outside install/data files; the updater never writes product data or implements schema migration (SS6 impacts, [BR-05](../../architecture/14-build-packaging-and-release.md#rule-br-05)) (package-level obligation contribution) | [PLT.04](../delivery/lanes/platform.md#task-plt-04) (artifact) |
| [UPD.05](../delivery/lanes/updater.md#task-upd-05) | [WP-53.04](53-desktop-distribution-and-update.md#rule-wp-53.04) (full) | none |
| [UPD.06](../delivery/lanes/updater.md#task-upd-06) | [WP-53.05](53-desktop-distribution-and-update.md#rule-wp-53.05) (full) | [PLT.47](../delivery/lanes/platform.md#task-plt-47) (artifact), [FND.05](../delivery/lanes/foundation.md#task-fnd-05) (artifact) |
| [UPD.07](../delivery/lanes/updater.md#task-upd-07) | [WP-53.07](53-desktop-distribution-and-update.md#rule-wp-53.07) (full) | [CON.16](../delivery/lanes/contracts.md#task-con-16) (contract) |
| [UPD.08](../delivery/lanes/updater.md#task-upd-08) | [WP-53.90](53-desktop-distribution-and-update.md#rule-wp-53.90) (full) | [PRF.01](../delivery/lanes/runtime-proofs.md#task-prf-01) (artifact), [POL.09](../delivery/lanes/policy.md#task-pol-09) (artifact) |

**Consumers outside this package:** [POL.07](../delivery/lanes/policy.md#task-pol-07), [REL.01](../delivery/lanes/release.md#task-rel-01), [REL.02](../delivery/lanes/release.md#task-rel-02), [REL.03](../delivery/lanes/release.md#task-rel-03), [REL.10](../delivery/lanes/release.md#task-rel-10).

<!-- delivery-graph:end -->

