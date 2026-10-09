# Release readiness and family release — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Per-surface release readiness, production signing and feeds, commercial activation, disaster drill and the family release.

Tasks: 9 · Owning repositories: ArcScope, Cloud, Contracts, DesktopPlatform, Mobile, Web · Integration owner(s): ArcScope integration owner, Cloud integration owner, Contracts integration owner, DesktopPlatform integration owner, Mobile integration owner, Web integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [REL.02](#task-rel-02) | ArcScope desktop release readiness | release | L | [SCOPE.26](arcscope.md#task-scope-26) (release), [UPD.08](updater.md#task-upd-08) (artifact), [SCOPE.11](arcscope.md#task-scope-11) (release), [SCOPE.19](arcscope.md#task-scope-19) (release), [NAT.30](native.md#task-nat-30) (release) | not-started |
| [REL.04](#task-rel-04) | Android release readiness | release | M | [AND.23](android.md#task-and-23) (release), [AND.26](android.md#task-and-26) (artifact) | not-started |
| [REL.05](#task-rel-05) | Web outputs release readiness | release | L | [WEB.26](web.md#task-web-26) (release), [WEB.09](web.md#task-web-09) (release), [WEB.18](web.md#task-web-18) (release) | not-started |
| [REL.06](#task-rel-06) | Cloud/AI production readiness (deployment, migration, backup, self-host) | release | XL | [CLOUD.51](cloud.md#task-cloud-51) (release), [AIR.90](ai-routing.md#task-air-90) (release), [GOV.03](governance.md#task-gov-03) (artifact), [CLOUD.10](cloud.md#task-cloud-10) (release), [CLOUD.20](cloud.md#task-cloud-20) (release), [CLOUD.28](cloud.md#task-cloud-28) (release), [CLOUD.36](cloud.md#task-cloud-36) (release), [CLOUD.47](cloud.md#task-cloud-47) (release), [CLOUD.55](cloud.md#task-cloud-55) (release), [COM.15](commerce.md#task-com-15) (release), [POL.10](policy.md#task-pol-10) (release), [OPS.12](operations.md#task-ops-12) (release), [SRCH.90](search.md#task-srch-90) (release), [HAR.90](harness.md#task-har-90) (release), [SIM.08](simulator.md#task-sim-08) (release), [GOV.09](governance.md#task-gov-09) (release) | not-started |
| [REL.07](#task-rel-07) | Contracts/SDK release audit (licence, SBOM, provenance rollup) | acceptance | M | [REL.02](#task-rel-02) (artifact), [REL.04](#task-rel-04) (artifact), [REL.05](#task-rel-05) (artifact), [REL.06](#task-rel-06) (artifact), [REL.08](#task-rel-08) (artifact) | not-started |
| [REL.08](#task-rel-08) | Commercial activation | release | L | [COM.15](commerce.md#task-com-15) (release), [POL.10](policy.md#task-pol-10) (release) | not-started |
| [REL.09](#task-rel-09) | Combined disaster drill and operational readiness confirmation | release | L | [REL.06](#task-rel-06) (artifact), [OPS.12](operations.md#task-ops-12) (release) | not-started |
| [REL.10](#task-rel-10) | Production update feed and signing switch | release | M | [REL.02](#task-rel-02) (artifact), [UPD.01](updater.md#task-upd-01) (artifact), [UPD.07](updater.md#task-upd-07) (artifact) | not-started |
| [REL.11](#task-rel-11) | Family release readiness audit and honest statement | release | L | [REL.02](#task-rel-02) (release), [REL.04](#task-rel-04) (release), [REL.05](#task-rel-05) (release), [REL.06](#task-rel-06) (release), [REL.07](#task-rel-07) (release), [REL.08](#task-rel-08) (release), [REL.09](#task-rel-09) (release), [REL.10](#task-rel-10) (release) | not-started |

## Tasks

<a id="task-rel-02"></a>

### REL.02 — ArcScope desktop release readiness

**Outcome.** ArcScope's desktop release candidate passes the complete update matrix on both supported platforms (Windows and Linux) against a candidate/staging feed, and carries a complete licence/SBOM/provenance/NOTICE record for REL.07 to roll up.

| Field | Value |
|---|---|
| Owning repository | ArcScope (`C:\MyFile\Projects\ArcForges\ArcScope`); integration owner: ArcScope integration owner, the holder of `roles/integration-arcscope` |
| Claim, branch and ledger | `claims/rel-02` and ledger record `ledger/tasks/rel-02.md` in the Plan repository; task branch `task/rel-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / L |
| Obligations | [WP-50.02](../../work-packages/50-full-platform-production-release.md#rule-wp-50.02) — ArcScope's own complete update matrix on Windows/Linux (macOS is out of scope per [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023))<br>[WP-50.01](../../work-packages/50-full-platform-production-release.md#rule-wp-50.01) — ArcScope's own licence inventory, SBOM, provenance attestation and verified NOTICE |
| Provides | arcscope-release-candidate-proven |
| Start prerequisites | **release** [SCOPE.26](arcscope.md#task-scope-26) — ArcScope feature-complete release candidate. *Why:* no release candidate exists to run an update matrix against until ArcScope's own product work is accepted<br>**artifact** [UPD.08](updater.md#task-upd-08) — the published ArcForges.Update package/client (the platform lane UPD area). *Why:* WP50.02 explicitly consumes the actual Update package rather than first implementing an updater<br>**release** [SCOPE.11](arcscope.md#task-scope-11) — ArcScope acquisition package accepted. *Why:* release readiness requires every ArcScope obligation package accepted<br>**release** [SCOPE.19](arcscope.md#task-scope-19) — ArcScope analysis package accepted. *Why:* release readiness requires every ArcScope obligation package accepted<br>**release** [NAT.30](native.md#task-nat-30) — complete native producer set verified as one immutable candidate (reduced under [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026)). *Why:* [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S13: the desktop release verifies the reduced native producer set it ships (instrument and common-ABI legs) |
| Entry condition | [ADOPT.05.release](adoption.md#task-adopt-05-release) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [REL.10](#task-rel-10) — production feed/signing cutover pointing at this proven candidate. *Why:* the update matrix can be rehearsed against a candidate/staging feed, but the desktop release is not actually complete until the production feed and signing switch points at the proven artifact |
| Unblocks | [REL.07](#task-rel-07), [REL.10](#task-rel-10), [REL.11](#task-rel-11) |
| Permitted substitutes | [SUB-desktop-candidate-feed](../substitutes.md#sub-desktop-candidate-feed) |
| Write scope | `ArcScope:eng/release/**`<br>`Design:docs/assurance/wp50-02-arcscope-*.md` |
| Shared resources | [RES-production-release-trust](../shared-resources.md#res-production-release-trust) (append) |
| Validation | Local opt-in runtime observation per supported platform under [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (the Linux leg runs in local WSL2 per [P2-024](../../../decisions/phase-2-specification-decisions.md#rule-p2-024)); no macOS CI or macOS matrix row per [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023). |
| Completion evidence | Full update-matrix results table per platform; licence/SBOM/provenance/NOTICE closure report for the ArcScope artifact. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023)): the macOS platform leg of the ArcScope update matrix is removed; Windows and Linux are the matrix. No other acceptance changes. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): NAT.30 (reduced) is added as a release verification input; the still-image and image chain is out of scope. |

<a id="task-rel-04"></a>

### REL.04 — Android release readiness

**Outcome.** The signed MAUI Android artifact (applicationId com.arcforges.mobile) is published on the direct-APK channel with every mobile gate closed (Play publication and store listings are out of scope for V1, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026)); post-release install and update are verified from the direct-APK channel.

| Field | Value |
|---|---|
| Owning repository | Mobile (`C:\MyFile\Projects\ArcForges\Mobile`); integration owner: Mobile integration owner, the holder of `roles/integration-mobile` |
| Claim, branch and ledger | `claims/rel-04` and ledger record `ledger/tasks/rel-04.md` in the Plan repository; task branch `task/rel-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / M |
| Obligations | [WP-50.03](../../work-packages/50-full-platform-production-release.md#rule-wp-50.03) — full<br>[WP-50.01](../../work-packages/50-full-platform-production-release.md#rule-wp-50.01) — Android's own licence inventory, SBOM, provenance attestation and verified NOTICE |
| Provides | android-release-live |
| Start prerequisites | **release** [AND.23](android.md#task-and-23) — every mobile gate satisfied (the Web and Android lanes AND area: signing, distribution, store gates). *Why:* WP50.03's completion gate explicitly requires every mobile gate closed from WP32 before Android can be submitted<br>**artifact** [AND.26](android.md#task-and-26) — physical Android FCM receipt delivered. *Why:* [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S7: the physical-device receipt moved here from OPS.12, so Cloud production readiness (REL.06, REL.09) is not blocked on a phone |
| Entry condition | [ADOPT.10.release](adoption.md#task-adopt-10-release) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.07](#task-rel-07), [REL.11](#task-rel-11) |
| Write scope | `Mobile:eng/release/**`<br>`Design:docs/assurance/wp50-03-android-*.md` |
| Validation | Post-release direct-APK install/update verification; no emulator/device CI per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) (real device evidence is WP06.07/WP30/WP32). |
| Completion evidence | Direct-APK install/update verification results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [F-023](../../../assurance/open-gates-register.md#rule-f-023) final closure and [VG-13](../../../assurance/open-gates-register.md#rule-vg-13) (store category fit) are WP32's own gates, consumed here rather than produced. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Artifact name and identity change to the MAUI build; store, consumption-only and install/update criteria unchanged. Store activation remains gated by the existing README and releasing.md no-listing statement until a reviewed decision. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: Play submission, the store listing and store-channel verification are out of scope, not completed; Android V1 uses the direct-APK channel ([PL-03](../../../architecture/09-ai-and-agent-runtime-architecture.md#rule-pl-03)). |

<a id="task-rel-05"></a>

### REL.05 — Web outputs release readiness

**Outcome.** Site, Account and Chat build once through the pinned .NET 10 SDK and central package management (offline after an approved restore), after current released proto-descriptor and C# compatibility checks. The same static artifacts are promoted with a manifest and safe runtime-config schema, deployed atomically with per-origin edge routing, opaque cookie, CSRF policy and per-profile exact CSP token sets, old hashed assets are preserved for the compatibility window, and headers, assets and config roll back coherently. Production Node servers stay out of the Cloud runtime; Node remains wrangler build and deploy tooling and Playwright remains test-only. The full browser-support.v1 matrix passes for supported, degraded and blocked behaviour in the rows that remain after [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023) (no macOS or Safari row).

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/rel-05` and ledger record `ledger/tasks/rel-05.md` in the Plan repository; task branch `task/rel-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / L |
| Obligations | [WP-50.06](../../work-packages/50-full-platform-production-release.md#rule-wp-50.06) — full<br>[WP-50.01](../../work-packages/50-full-platform-production-release.md#rule-wp-50.01) — Web's own npm SBOM/provenance and CLI evidence<br>[WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) Browser matrix acceptance (unlabeled paragraph after [WP-50.90](../../work-packages/50-full-platform-production-release.md#rule-wp-50.90)): browser-support.v1 against the exact release artifact/OS/browser patches, supported/degraded/blocked flows including delayed-stream polling, refusal of unavailable required auth/step-up, safe-preview refusal, preserved pending work; no-JS static-site readability; joins WP23/45/47/48/49 production hashes with real browser evidence - a Playwright WebKit run alone does not claim Safari/OS authenticator proof — package-level obligation contribution |
| Provides | web-release-live; pg-23-web-contribution |
| Start prerequisites | **release** [WEB.26](web.md#task-web-26) — ArcChat Web Companion complete (the Web and Android lanes WEB area). *Why:* WP50.06 releases Site/Account/Chat together<br>**release** [WEB.09](web.md#task-web-09) — Static Public Site complete (the Web and Android lanes WEB area). *Why:* same joint-release reasoning<br>**release** [WEB.18](web.md#task-web-18) — Account Portal complete (the Web and Android lanes WEB area). *Why:* same joint-release reasoning |
| Entry condition | [ADOPT.09.release](adoption.md#task-adopt-09-release) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.07](#task-rel-07), [REL.11](#task-rel-11) |
| Write scope | `Web:eng/release/**`<br>`Design:docs/assurance/wp50-06-web-*.md` |
| Validation | Local opt-in only ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)) for the browser and integration rows: production static-asset and real C# integration in the supported browser matrix, covering public no-script content, auth/CSRF/expiry/replica revocation, paid-checkout return and Task recovery; visual, accessibility and performance budgets; atomic switch and rollback, cached-client and chunk failure, route-fallback and API-error separation; real-browser evidence per browser-support.v1 for the browser rows that remain (Chromium and Firefox as configured in playwright.config.ts; no Playwright-WebKit-only evidence for Safari or OS-authenticator claims, and no Safari row, [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023)). Static or offline checks, not part of the opt-in: NuGet closure SBOM and provenance with licence receipts, and a byte-for-byte publish reproducibility comparison (CI-eligible; ci.yml already runs the licence-evaluated and test:provenance checks). Windows and WSL2 Debian evidence for affected Linux checks ([P2-024](../../../decisions/phase-2-specification-decisions.md#rule-p2-024)). No fixture-only substitution in the integration rows. |
| Completion evidence | [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) combined production release and rollback evidence (local opt-in run receipt); browser-matrix acceptance results for the remaining rows; NuGet closure SBOM and provenance receipts; publish reproducibility comparison. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Owns the unlabeled 'Browser matrix acceptance' package obligation appended after [WP-50.90](../../work-packages/50-full-platform-production-release.md#rule-wp-50.90); see package_obligations. Joins WP23/45/47/48/49 production hashes with real browser evidence per that paragraph. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021), [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023)): The pinned Node/npm pipeline becomes the pinned .NET 10 build with central package management; esproj/npm installs and the npm SBOM become the NuGet closure SBOM and provenance; C#/TS compatibility becomes C# compatibility; Playwright-WebKit and Safari evidence is removed because macOS and Safari are outside delivery scope. Production Node servers stay out of the Cloud runtime, and Node remains wrangler tooling only. The release gate and its evidence intent are unchanged. |

<a id="task-rel-06"></a>

### REL.06 — Cloud/AI production readiness (deployment, migration, backup, self-host)

**Outcome.** Cloud is deployed from a promoted, never-rebuilt artifact with rehearsed migration/rollback, proven backup/restore, a live status page with emergency alternate URL, and the approved/measured capacity envelope plus independently operated self-host deployment evidence required for [L-16](../../../assurance/release-gates.md#rule-l-16)/[PG-25](../../../assurance/open-gates-register.md#rule-pg-25)/[PG-26](../../../assurance/open-gates-register.md#rule-pg-26), on a genuine Native AOT publish.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/rel-06` and ledger record `ledger/tasks/rel-06.md` in the Plan repository; task branch `task/rel-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / XL |
| Obligations | [WP-50.04](../../work-packages/50-full-platform-production-release.md#rule-wp-50.04) — production deployment from a promoted artifact; expand/contract migration and compatible rollback rehearsed; backup verified with proven restore; upgrade/rollback rehearsed; [L-01](../../../assurance/release-gates.md#rule-l-01)..[L-16](../../../assurance/release-gates.md#rule-l-16) evidence except the game-day exercise itself (REL.09); status page live with emergency alternate URL; approved/measured capacity envelope and independently operated self-host deployment ([PG-25](../../../assurance/open-gates-register.md#rule-pg-25)/26)<br>[WP-50.01](../../work-packages/50-full-platform-production-release.md#rule-wp-50.01) — Cloud/AI's own licence inventory, SBOM, provenance attestation and verified NOTICE |
| Provides | cloud-production-deployed; vg-06-wp50-contribution; pg-19-wp50-contribution |
| Start prerequisites | **release** [CLOUD.51](cloud.md#task-cloud-51) — D1/R2 disaster-recovery mechanism complete. *Why:* backup/restore rehearsal needs the actual recovery mechanism, not a description of it<br>**release** [AIR.90](ai-routing.md#task-air-90) — Workers AI routing/metering complete (the AI lanes AIR area). *Why:* AI is included in this production surface<br>**artifact** [GOV.03](governance.md#task-gov-03) — Cloud's Native AOT build posture (GOV.03). *Why:* [L-01](../../../assurance/release-gates.md#rule-l-01)..[L-16](../../../assurance/release-gates.md#rule-l-16) evidence requires the promoted candidate to already be a genuine Native AOT publish, not a JIT stand-in<br>**release** [CLOUD.10](cloud.md#task-cloud-10) — Cloud host closure and launch-capacity acceptance. *Why:* production readiness includes the real launch-capacity evidence<br>**release** [CLOUD.20](cloud.md#task-cloud-20) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [CLOUD.28](cloud.md#task-cloud-28) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [CLOUD.36](cloud.md#task-cloud-36) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [CLOUD.47](cloud.md#task-cloud-47) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [CLOUD.55](cloud.md#task-cloud-55) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [COM.15](commerce.md#task-com-15) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [POL.10](policy.md#task-pol-10) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [OPS.12](operations.md#task-ops-12) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [SRCH.90](search.md#task-srch-90) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [HAR.90](harness.md#task-har-90) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [SIM.08](simulator.md#task-sim-08) — obligation package accepted. *Why:* Cloud and AI production readiness requires every Cloud and AI obligation package accepted with its evidence<br>**release** [GOV.09](governance.md#task-gov-09) — Cloud policy tests delivered; the standing worker/ no-business-logic check is CLOUD.84 validation ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S16(b)). *Why:* [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S13: the Cloud production readiness release verifies the standing C# policy check it accepts |
| Entry condition | [ADOPT.07.release](adoption.md#task-adopt-07-release) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [REL.09](#task-rel-09) — the combined disaster drill actually exercised against this deployed production topology. *Why:* [L-16](../../../assurance/release-gates.md#rule-l-16) and the cloud go-live threshold require a completed game day; deployment alone does not prove 'failure behaves correctly' |
| Unblocks | [REL.07](#task-rel-07), [REL.09](#task-rel-09), [REL.11](#task-rel-11) |
| Write scope | `Cloud:eng/release/**`<br>`Cloud:deploy/production/**`<br>`Design:docs/assurance/wp50-04-cloud-*.md` |
| Validation | Production-shaped migration/rollback rehearsal against real Cloudflare topology; archived launch-capacity.v1 hash, actual standard-2 allocation/four global slots/ten-minute sleep, warm/cold/burst/fallback-read workload, D1/Vectorize/R2 dimensions and provider prices; explicit Product/Operations approval required for [L-16](../../../assurance/release-gates.md#rule-l-16)/[PG-26](../../../assurance/open-gates-register.md#rule-pg-26) - not markable complete from document checks alone. |
| Completion evidence | Per-gate go-live evidence [L-01](../../../assurance/release-gates.md#rule-l-01)..[L-16](../../../assurance/release-gates.md#rule-l-16) (except the drill); backup/restore proof; self-host deployment evidence. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | The game-day exercise itself is split out to REL.09 per the assignment's explicit 'combined disaster drill' bucket. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): the EXT.90 start edge is removed (extension platform out of scope); the GOV.09 Cloud policy tests are added as a release verification input (S13); the standing worker/ check is a CLOUD.84 validation item (S16(b)). |

<a id="task-rel-07"></a>

### REL.07 — Contracts/SDK release audit (licence, SBOM, provenance rollup)

**Outcome.** Every shipped artifact across every retained surface (the excluded public SDK, CLI and retired npm, Kotlin and Maven rows are out of scope, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026)) has a licence inventory, SBOM, provenance attestation and verified NOTICE, and every reused item has a completed provenance record, rolled into one closure report.

| Field | Value |
|---|---|
| Owning repository | Contracts (`C:\MyFile\Projects\ArcForges\Contracts`); integration owner: Contracts integration owner, the holder of `roles/integration-contracts` |
| Claim, branch and ledger | `claims/rel-07` and ledger record `ledger/tasks/rel-07.md` in the Plan repository; task branch `task/rel-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | acceptance / M |
| Obligations | [WP-50.01](../../work-packages/50-full-platform-production-release.md#rule-wp-50.01) — the audit mechanism (licence inventory, SBOM, provenance attestation, NOTICE-generation verification per artifact, copied-content audit) plus Contracts/public-SDK's own candidate audit and the cross-artifact provenance-completeness rollup |
| Provides | release-audit-rollup; sbom-provenance-closure-report |
| Start prerequisites | **artifact** [REL.02](#task-rel-02) — ArcScope's own licence/SBOM/provenance/NOTICE evidence row. *Why:* same<br>**artifact** [REL.04](#task-rel-04) — Android's own licence/SBOM/provenance/NOTICE evidence row. *Why:* same<br>**artifact** [REL.05](#task-rel-05) — Web's own licence/SBOM/provenance/NOTICE evidence row. *Why:* same<br>**artifact** [REL.06](#task-rel-06) — Cloud/AI's own licence/SBOM/provenance/NOTICE evidence row. *Why:* same<br>**artifact** [REL.08](#task-rel-08) — the commercial surface's own licence/SBOM/provenance/NOTICE evidence row. *Why:* same |
| Entry condition | [ADOPT.03.release](adoption.md#task-adopt-03-release) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.11](#task-rel-11) |
| Write scope | `Contracts:eng/release-audit/**`<br>`Design:docs/assurance/wp50-01-audit-*.md` |
| Validation | Offline document/metadata rollup; no new build or download beyond what each surface already produced, per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017). |
| Completion evidence | Closure report per artifact; NOTICE verification; provenance-completeness check across every recorded reuse. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Distributed-responsibility pattern: each surface task produces its OWN artifact's evidence as part of its own completion (WP50.01's per-artifact language); REL.07 owns the audit mechanism and the cross-artifact completeness rollup, mirroring GOV.13's role for [PG-11](../../../assurance/open-gates-register.md#rule-pg-11)/invariant accounting. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: the Contracts public SDK and CLI candidate audit, the npm TypeScript SDK audit rows, and the Kotlin and Maven audit rows are out of scope, not completed; the NuGet C# SDK packages are covered by the audit. |

<a id="task-rel-08"></a>

### REL.08 — Commercial activation

**Outcome.** Account portal and checkout run in production; official pricing is published only after entitlement, refunds, webhook idempotency and a RECEIVED payout are all proven - until then the public statement is 'technical integration complete'; the regional route remains disabled unless its own gates are met.

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/rel-08` and ledger record `ledger/tasks/rel-08.md` in the Plan repository; task branch `task/rel-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / L |
| Obligations | [WP-50.05](../../work-packages/50-full-platform-production-release.md#rule-wp-50.05) — full |
| Provides | commercial-launch-live; vg-10-vg-11-vg-12-wp50-contribution |
| Start prerequisites | **release** [COM.15](commerce.md#task-com-15) — Commerce, Entitlement and Credits complete (the commerce, policy and operations lanes COM area). *Why:* the full commercial gate evidence set WP50.05 requires comes from WP42<br>**release** [POL.10](policy.md#task-pol-10) — Dynamic Policy and Configuration Control Plane complete (the commerce, policy and operations lanes POL area). *Why:* the regional-route configuration assertion depends on WP44's control plane |
| Entry condition | [ADOPT.07.release](adoption.md#task-adopt-07-release) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.07](#task-rel-07), [REL.11](#task-rel-11) |
| Write scope | `Cloud:eng/release/commercial/**`<br>`Design:docs/assurance/wp50-05-commercial-*.md` |
| Validation | Full commercial gate evidence set from WP42; configuration assertion on the regional route; a received payout is required, not merely a successful test transaction, per [BR-05](../../../architecture/14-build-packaging-and-release.md#rule-br-05). |
| Completion evidence | Commercial gate evidence set including the received payout; regional-route configuration assertion. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | [VG-10](../../../assurance/open-gates-register.md#rule-vg-10)/[VG-11](../../../assurance/open-gates-register.md#rule-vg-11)/[VG-12](../../../assurance/open-gates-register.md#rule-vg-12) (supplier onboarding, payout eligibility, regional enablement) are WP42's own gates, consumed here rather than produced. |

<a id="task-rel-09"></a>

### REL.09 — Combined disaster drill and operational readiness confirmation

**Outcome.** A game-day exercise across the full severity ladder runs against the real deployed production topology with recorded evidence for every go-live gate; every alert maps to a rehearsed runbook, on-call is in place, and support paths and account-level enforcement and appeal paths are operable (community and public-ecosystem enforcement paths are out of scope, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026)).

| Field | Value |
|---|---|
| Owning repository | Cloud (`C:\MyFile\Projects\ArcForges\Cloud`); integration owner: Cloud integration owner, the holder of `roles/integration-cloud` |
| Claim, branch and ledger | `claims/rel-09` and ledger record `ledger/tasks/rel-09.md` in the Plan repository; task branch `task/rel-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / L |
| Obligations | [WP-50.04](../../work-packages/50-full-platform-production-release.md#rule-wp-50.04) — the game-day exercise across the severity ladder against the real production topology only (the rest of 50.04 is REL.06)<br>[WP-50.07](../../work-packages/50-full-platform-production-release.md#rule-wp-50.07) — full: alerting live and mapped to rehearsed runbooks, on-call arrangement in place, incident process exercised, support entry points live, enforcement/appeal paths operable, advisory process rehearsed |
| Provides | disaster-drill-complete; operational-readiness-confirmed |
| Start prerequisites | **artifact** [REL.06](#task-rel-06) — Cloud deployed to the real production topology. *Why:* a game day exercised against anything less than the real production topology does not satisfy the go-live threshold ('failure behaves correctly')<br>**release** [OPS.12](operations.md#task-ops-12) — rehearsed runbooks and [PG-04](../../../assurance/open-gates-register.md#rule-pg-04) closure (the commerce, policy and operations lanes OPS area). *Why:* WP50.07 confirms runbooks are LIVE at release; it does not author or first-rehearse them - that is WP45's job |
| Entry condition | [ADOPT.07.release](adoption.md#task-adopt-07-release) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.06](#task-rel-06), [REL.11](#task-rel-11) |
| Write scope | `Cloud:eng/release/game-day/**`<br>`Design:docs/assurance/wp50-04-gameday-*.md, wp50-07-operational-readiness-*.md` |
| Validation | A real exercise across the severity ladder against real production topology; alert-to-runbook completeness assertion; on-call verification; support-path end-to-end test; local/opt-in per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017), no synthetic-only substitution. |
| Completion evidence | Game-day record with per-gate go-live evidence; alert-to-runbook, on-call and support-path results. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Named explicitly in the assignment as its own bucket ('combined disaster drill'); folds WP50.07 in alongside WP50.04's game-day portion since both are evidence of the same severity-ladder incident-response exercise. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: rehearsal of community and public-ecosystem enforcement, appeal and support paths, and of publisher or third-party package advisories and package revocation, is out of scope, not completed; only the first-party advisory process is rehearsed. |

<a id="task-rel-10"></a>

### REL.10 — Production update feed and signing switch

**Outcome.** The production update feed is populated with hashes/compatibility ranges/minimum versions for the ArcScope desktop application across Windows and Linux (macOS is out of scope per [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023)), the corresponding signed installers are referenced by the feed (store and package-manager listings are out of scope for V1, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026)), and a blocked bad version is refused by both the feed and compatibility policy.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/rel-10` and ledger record `ledger/tasks/rel-10.md` in the Plan repository; task branch `task/rel-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / M |
| Obligations | [WP-50.02](../../work-packages/50-full-platform-production-release.md#rule-wp-50.02) — the shared production update-feed population (hashes, compatibility ranges, minimum versions) and code-signing/publication-pointer cutover only; ArcScope update-matrix testing is REL.02 |
| Provides | production-feed-live; signing-switch-complete |
| Start prerequisites | **artifact** [REL.02](#task-rel-02) — ArcScope's own update matrix proven. *Why:* same reasoning<br>**artifact** [UPD.01](updater.md#task-upd-01) — the update client/channel mechanism and feed schema (the platform lane UPD area). *Why:* WP50.02 explicitly does not first implement an updater; it consumes WP53's actual mechanism<br>**artifact** [UPD.07](updater.md#task-upd-07) — production desktop update-channel and Android distribution trust (catalog trust is out of scope, [P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026)). *Why:* the production switch installs the production trust roots produced by the updater lane |
| Entry condition | [ADOPT.02.release](adoption.md#task-adopt-02-release) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.02](#task-rel-02), [REL.11](#task-rel-11), [UPD.08](updater.md#task-upd-08) |
| Write scope | `DesktopPlatform:eng/packaging/release/**` |
| Shared resources | [RES-production-release-trust](../shared-resources.md#res-production-release-trust) (append) |
| Validation | Blocked-bad-version refusal test against both feed and compatibility policy; no rebuild - promotes the exact already-proven candidate per [BR-01](../../../architecture/14-build-packaging-and-release.md#rule-br-01); per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) local/opt-in observation only. |
| Completion evidence | Feed population record; signed-installer feed consistency; blocked-bad-version refusal evidence. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Production feed hosting and signing-key invocation follow the updater lane design; key custody is the Release Engineering Owner. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023)): the macOS feed, listing and signing leg is removed; Windows and Linux installers are the populated feed. No other acceptance changes. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: store and package-manager listings are out of scope, not completed; the production update feed and signed installers remain, and UPD.07 is narrowed to the desktop update-channel and Android distribution trust roots. |

<a id="task-rel-11"></a>

### REL.11 — Family release readiness audit and honest statement

**Outcome.** Every gate in release-gates.md is evaluated for every retained surface with a named, resolvable evidence artifact; every still-open gate's blocking consequence is stated; no cross-system failure row for a retained lifecycle in architecture/20-cross-system-lifecycles.md lacks a run test; every public claim is backed by gate evidence, iOS and macOS are explicitly stated as outside current scope, and nothing incomplete is presented as complete.

| Field | Value |
|---|---|
| Owning repository | DesktopPlatform (`C:\MyFile\Projects\ArcForges\DesktopPlatform`); integration owner: DesktopPlatform integration owner, the holder of `roles/integration-desktopplatform` |
| Claim, branch and ledger | `claims/rel-11` and ledger record `ledger/tasks/rel-11.md` in the Plan repository; task branch `task/rel-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / L |
| Package acceptance | Records the [WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-50.00](../../work-packages/50-full-platform-production-release.md#rule-wp-50.00) — full<br>[WP-50.08](../../work-packages/50-full-platform-production-release.md#rule-wp-50.08) — full<br>[WP-50.90](../../work-packages/50-full-platform-production-release.md#rule-wp-50.90) — full |
| Provides | wp50-family-release-complete; release-audit-final |
| Start prerequisites | **release** [REL.02](#task-rel-02) — ArcScope desktop release readiness complete. *Why:* same<br>**release** [REL.04](#task-rel-04) — Android release readiness complete. *Why:* same<br>**release** [REL.05](#task-rel-05) — Web outputs release readiness complete. *Why:* same<br>**release** [REL.06](#task-rel-06) — Cloud/AI production readiness complete. *Why:* same<br>**release** [REL.07](#task-rel-07) — Contracts/SDK release audit complete. *Why:* same<br>**release** [REL.08](#task-rel-08) — commercial activation complete. *Why:* same<br>**release** [REL.09](#task-rel-09) — combined disaster drill and operational readiness confirmed. *Why:* same<br>**release** [REL.10](#task-rel-10) — production feed/signing switch complete. *Why:* same |
| Entry condition | [ADOPT.02.release](adoption.md#task-adopt-02-release) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | none |
| Write scope | `Design:docs/assurance/wp50-00-readiness-audit.md, wp50-08-honest-statement.md, wp50-stage-acceptance.md/.json`<br>`DesktopPlatform:eng/release/**` |
| Shared resources | [RES-design-evidence](../shared-resources.md#res-design-evidence) (append) |
| Validation | Gate-coverage report asserting no gate is unevaluated; evidence-resolution check asserting every claimed evidence artifact exists; cross-system failure-row coverage check; claim audit comparing every required retained feature and owner WP to real gate receipts and public claims; per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) no new runtime beyond what each surface already produced. |
| Completion evidence | Gate-coverage report; claim audit; WP50 stage-acceptance receipt joining REL.02 and REL.04-REL.10. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Terminal task for the entire 51-package sequence (WP50 has no downstream). [BR-01](../../../architecture/14-build-packaging-and-release.md#rule-br-01)/[BR-02](../../../architecture/14-build-packaging-and-release.md#rule-br-02)/[BR-03](../../../architecture/14-build-packaging-and-release.md#rule-br-03)/[BR-04](../../../architecture/14-build-packaging-and-release.md#rule-br-04) (build once, no partial pass, no waiving integrity/security/licence/regulatory gates, nothing incomplete presented as complete) all bind here directly. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: gate coverage and claim audit for excluded products (ArcSlate, ArcNotes, excluded native families, the catalog and community ecosystem), macOS and Safari claims (except the statement that iOS and macOS are outside current scope), failure rows for excluded lifecycles, and requirement-to-gate accounting for excluded owner work packages ([WP-41](../../work-packages/41-extension-platform-and-integrations.md#rule-wp-41), [WP-45.10](../../work-packages/45-operations-support-and-trust-safety.md#rule-wp-45.10)) are out of scope, not completed. |
