<a id="rule-wp-50"></a>

# WP-50 — Full-Platform Production Release

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: K — Web and release
> Upstream: `20`, `28`, `32`, `35`, `39`, `40`, `41`, `43`, `46`, `49`, `51`, `52` · Downstream: —

> **Goal.** Ship everything together, once every gate is genuinely satisfied: four desktop products across three platforms, the Android companion, the cloud, the web surfaces, and the commercial loop — with the release audit, the production gates and the honest statement of what is and is not shipped.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Each publisher; Cloud coordinated evidence. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The coordinated production release: official site entry points, downloads and documentation; account portal and checkout in production; Windows, macOS and Linux desktop releases; the Android release; cloud production with migration rehearsal, backup and restore, upgrade and rollback; the licence, SBOM and copied-content release audit; observability, alerting, runbook and incident closure; and the final production gates for the whole family.

**Out of scope.** iOS build activation, which remains deferred (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**). Any capability whose gates are not satisfied — it ships disabled or not at all, never as a claim.

**Why this package exists.** The [release gates](../../assurance/release-gates.md) and this package’s completion gate require these deliveries to be ready **together**. A release where the site is live but the payout path is unproven, or where downloads exist but rollback is untested, is not a release — it is an incident waiting for its first customer.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [Release gates](../../assurance/release-gates.md) | The production acceptance classes; this package’s §8 lists the deliveries that must be ready together |
| [`../../assurance/release-gates.md`](../../assurance/release-gates.md) | Every gate class and its evidence |
| [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md) | Every open gate and whether it is now closed |
| [`../../architecture/14-build-packaging-and-release.md`](../../architecture/14-build-packaging-and-release.md) | Build, packaging, signing, feed and promotion |
| All upstream packages | Every product and platform capability being released |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Build once, promote the same artifact.** Production never rebuilds. |
| BR-02 | **A gate is passed with evidence or it is not passed.** There is no "passed with concerns". |
| BR-03 | **A gate protecting data integrity, security, licence compliance or a regulatory obligation cannot be waived.** |
| BR-04 | **Nothing incomplete is presented as complete.** A deferred capability is stated as deferred. |
| BR-05 | **Official pricing and checkout do not launch publicly before entitlement, refunds, webhook idempotency and a real payout path are complete**. |
| BR-06 | **iOS is not claimed as compiled or tested** (**[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**). |
| BR-07 | **A bad version must be immediately haltable** through the update feed and compatibility policy. |
| BR-08 | **Rollback is reserved and tested** for every shipped surface. |
| BR-09 | **Release artifacts are immutable**; a defect produces a new version. |
| BR-10 | **The release record is complete and immutable**, and every gate result names its evidence artifact. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `eng/release/` | The coordinated release procedure across every surface |
| `eng/verification/release-audit/` | Licence, SBOM, provenance and copied-content audit output |
| `deploy/production/` | Production environment definitions and promotion configuration |
| `content/` | Launch content, documentation, changelog and legal versions |
| The release record store | One immutable record per released artifact |
| `docs/runbooks/` in the implementation repository | Final rehearsal records for every runbook |

---

## 5. Required implementation work

<a id="rule-wp-50.00"></a>

### WP-50.00 — Release readiness audit

**What must be fully done.** Every gate in [`release-gates.md`](../../assurance/release-gates.md) evaluated for every surface, with its evidence artifact named. Every gate in [`open-gates-register.md`](../../assurance/open-gates-register.md) either closed with evidence or explicitly recorded as still open with its blocking consequence stated.

**Testing requirements.** A gate-coverage report asserting no gate is unevaluated; an evidence-resolution check asserting every claimed evidence artifact exists; a **cross-system failure-row coverage check** asserting that every failure row in [`../../architecture/20-cross-system-lifecycles.md`](../../architecture/20-cross-system-lifecycles.md) names a test that exists and has run.

**Completion gate.** **Every gate is evaluated with a named, resolvable evidence artifact**, every open gate's blocking consequence is stated, and **no cross-system failure row lacks a run test**.

<a id="rule-wp-50.01"></a>

### WP-50.01 — Licence, SBOM and copied-content audit

**What must be fully done.** The full release audit: licence inventory per artifact, SBOM per artifact, provenance attestation, NOTICE generation verified against recorded attribution obligations, and a copied-content audit confirming every reused item has a completed provenance record.

**Testing requirements.** A closure report per artifact; a NOTICE verification; a provenance-completeness check across every recorded reuse.

**Completion gate.** Every shipped artifact has a licence inventory, SBOM, provenance attestation and verified NOTICE, and every reused item has a completed provenance record.

<a id="rule-wp-50.02"></a>

### WP-50.02 — Desktop release across three platforms

**What must be fully done.** Signed installers for Windows, macOS and Linux from the same CI-produced artifacts; the update feed populated with hashes, compatibility ranges and minimum versions; the full update matrix verified per platform; store and package-manager listings pointing at the same signed installer.

**Testing requirements.** The complete update matrix per platform — fresh install, upgrade, two-version upgrade, downgrade protection, rollback, interrupted download, interrupted install, corrupted artifact rejection, update during a long task, update with documents open, uninstall preserving user data, channel switch both ways, blocked bad version.

**Completion gate.** **The full update matrix passes on all three desktop platforms**, and a blocked bad version is refused by both the feed and compatibility policy.

<a id="rule-wp-50.03"></a>

### WP-50.03 — Android release

**What must be fully done.** The Android artifact submitted and released with every mobile gate satisfied from `32`, and the store listing consistent with the consumption-only posture.

**Testing requirements.** Post-release install and update verification from the store channel; a listing-consistency check.

**Completion gate.** The Android release is live with every mobile gate closed and the listing consistent with the consumption-only posture.

<a id="rule-wp-50.04"></a>

### WP-50.04 — Cloud production

**What must be fully done.** Production deployment from a promoted artifact; migration rehearsed forward and backward; backup verified with a proven restore; upgrade and rollback rehearsed; the full go-live gate set from [L-01](../../assurance/release-gates.md#rule-l-01) to [L-15](../../assurance/release-gates.md#rule-l-15) satisfied; the status page live with its emergency alternate URL published.

**Testing requirements.** A game-day exercise across the severity ladder against the real production topology; the recorded evidence for each go-live gate.

**Completion gate.** **The cloud go-live threshold is met — "failure behaves correctly"** — with a completed game day and evidence for every gate, including [VG-06](../../assurance/open-gates-register.md#rule-vg-06) on the promoted Native AOT host and real CF/R2/recovery closure.

<a id="rule-wp-50.05"></a>

### WP-50.05 — Commercial launch

**What must be fully done.** Account portal and checkout in production; official pricing published only after entitlement, refunds, webhook idempotency and a **received payout** are all proven; the regional route disabled unless its own gates are met.

**Testing requirements.** The full commercial gate evidence set from `42`; a configuration assertion on the regional route.

**Completion gate.** **Pricing and checkout are public only after a payout has actually been received**; until then the statement is "technical integration complete". The regional route remains disabled unless its gates are met.

<a id="rule-wp-50.06"></a>

### WP-50.06 — Node-built Web release set and real-browser verification

**What must be fully done.** Build Site/Account/Chat once through the pinned Node/npm pipeline after current released proto descriptor/C#/TS compatibility checks; promote the same artifacts with their manifest and safe runtime-config schema. Deploy per-origin edge routing, opaque cookie/CSRF policy, CSP and shared Cloud session prerequisites. Preserve old hashed chunks for the compatibility window; rollback headers/assets/config coherently. Keep production Node servers and esproj/npm installs out of Cloud runtime.

**Testing requirements.** Production asset/real C# integration in the supported browser matrix; public no-script content, auth/CSRF/expiry/replica revocation, paid checkout return and Task recovery; visual/accessibility/performance budgets; atomic switch/rollback, cached client/chunk failure, route fallback/API error separation; npm SBOM/provenance and Windows/CLI evidence. No fixture-only substitution.

**Completion gate.** All declared Web surfaces pass commercial/browser/session/contract/visual/deployment gates including [PG-23](../../assurance/open-gates-register.md#rule-pg-23), using promoted production artifacts with an auditable rollback and client-compatibility path.

<a id="rule-wp-50.07"></a>

### WP-50.07 — Operational readiness

**What must be fully done.** Alerting live with every alert mapped to a rehearsed runbook; on-call arrangement in place; incident process exercised; support entry points live; enforcement and appeal paths operable; advisory process rehearsed.

**Testing requirements.** An alert-to-runbook completeness assertion; an on-call verification; a support-path end-to-end test.

**Completion gate.** Every alert maps to a rehearsed runbook, on-call is in place, and support and appeal paths are operable.

<a id="rule-wp-50.08"></a>

### WP-50.08 — Honest release statement

**What must be fully done.** A published statement of what ships, what is deferred and what is disabled: iOS as planned and build-deferred; any capability whose gates are unmet as disabled rather than claimed; the supported platform, browser and device matrices; and the supported client window.

**Testing requirements.** A claim-audit comparing every public statement against the gate evidence.

**Completion gate.** **Every public claim is backed by gate evidence**, and every deferred or disabled capability is stated as such.

---

**Required implementation and closure from the final review.** Implement and independently verify [22-deployment-and-release-execution](../../architecture/22-deployment-and-release-execution.md#partial-integration-manifests-and-mobile-rescue-release). Require complete products[] and web[] plus source/package/descriptor/image/Worker/config/database identities in the family manifest, with no pending/mock release operation. Replace WP47 private metadata fixtures with approved offers and actual signed downloads. Join WP46+52 real running/waiting/unknown-effect restore, post-backup revocation/deletion and offline-client quarantine. Prove A/B/C-safe rollback, Android greater-versionCode rescue, all portable Slate output/subtitle/transcription and applicable commercial gates on the declared artifacts. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-50.90"></a>
### WP-50.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Implement release coordination using per-repository immutable artifacts and the compatible integration/deployment manifest. Assemble licences, signing, migrations, update/rollback, support, commercial and restore gates from actual owner evidence.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Clean install/update/rollback and mixed-version acceptance across supported products; real Cloud+CF+R2 paths; no mandatory lockstep product versions or invented iOS build evidence.

**Completion gate.** Clean install/update/rollback and mixed-version acceptance across supported products; real Cloud+CF+R2 paths; no mandatory lockstep product versions or invented iOS build evidence. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Production data becomes real user data; every recovery path becomes load-bearing |
| Protocol | The supported client window becomes a public commitment |
| UI | Every surface becomes publicly visible |
| Security | The threat model becomes live; advisory and expedited update paths become load-bearing |
| Platform | Every supported platform is now a maintenance obligation |
| Migration | Every future migration must carry real user data forward |
| Compatibility | The first public compatibility baseline for every axis |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Gate coverage report with resolvable evidence artifacts | [WP-50.00](#rule-wp-50.00) |
| Licence inventory, SBOM, attestation, NOTICE and provenance closure | [WP-50.01](#rule-wp-50.01) |
| Full update matrix results per desktop platform | [WP-50.02](#rule-wp-50.02) |
| Store install and update verification | [WP-50.03](#rule-wp-50.03) |
| Game-day record and per-gate go-live evidence | [WP-50.04](#rule-wp-50.04) |
| Commercial gate evidence including the received payout | [WP-50.05](#rule-wp-50.05) |
| Atomic deployment, rollback and cached-client results | [WP-50.06](#rule-wp-50.06) |
| Alert-to-runbook, on-call and support-path results | [WP-50.07](#rule-wp-50.07) |
| Claim audit against gate evidence | [WP-50.08](#rule-wp-50.08) |

---

## 8. Completion gate

**Runtime/closure producers.** [VG-06](../../assurance/open-gates-register.md#rule-vg-06) through [WP-50.04](#rule-wp-50.04). The named candidate must supply actual passing evidence; documentation does not close these gates.

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-50.90](#rule-wp-50.90) and all inherited domain-specific gates must pass on the same candidate closure. Clean install/update/rollback and mixed-version acceptance across supported products; real Cloud+CF+R2 paths; no mandatory lockstep product versions or invented iOS build evidence.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-50.06](#rule-wp-50.06) — Combine all contributing Web evidence into coherent production assets/config/edge release and rollback; no fixture-only release. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-19](../../assurance/open-gates-register.md#rule-pg-19) evidence:** [WP-50.04](#rule-wp-50.04) — Production-shaped migration/rollback rehearsal consumes the versioned backfill/cutover proof from package 21. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. **Every gate in the release-gate set is evaluated with a named, resolvable evidence artifact**, and every still-open gate's blocking consequence is stated.
2. Every shipped artifact has a licence inventory, SBOM, provenance attestation and verified NOTICE; every reused item has a completed provenance record.
3. **The full update matrix passes on Windows, macOS and Linux**, and a blocked bad version is refused by both the feed and compatibility policy.
4. The Android release is live with every mobile gate closed and a listing consistent with the consumption-only posture.
5. **The cloud go-live threshold is met** — a completed game day across the severity ladder, proven restore, rehearsed rollback and region rebuild, and evidence for every gate from [L-01](../../assurance/release-gates.md#rule-l-01) to [L-15](../../assurance/release-gates.md#rule-l-15).
6. **Pricing and checkout are public only after a payout has actually been received**; the regional route remains disabled unless its own gates are met.
7. Every web surface deploys atomically, rolls back cleanly, and handles a cached older client with a grace period.
8. Every alert maps to a rehearsed runbook; on-call is in place; support, enforcement and appeal paths are operable.
9. **Every public claim is backed by gate evidence**; iOS is stated as planned and build-deferred; nothing incomplete is presented as complete.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [WP-20](20-first-cross-product-workflow.md#rule-wp-20)
- [WP-28](28-arcnotes-properties-and-views.md#rule-wp-28)
- [WP-32](32-mobile-release-and-store-gates.md#rule-wp-32)
- [WP-35](35-arcscope-integration-and-sync.md#rule-wp-35)
- [WP-39](39-arcslate-integration-and-portability.md#rule-wp-39)
- [WP-40](40-knowledge-search-and-retrieval.md#rule-wp-40)
- [WP-41](41-extension-platform-and-integrations.md#rule-wp-41)
- [WP-43](43-managed-ai-routing-and-metering.md#rule-wp-43)
- [WP-46](46-backup-recovery-and-data-health.md#rule-wp-46)
- [WP-49](49-arcchat-web-companion.md#rule-wp-49)
- [WP-51](51-arcscope-cloud-simulator.md#rule-wp-51)
- [WP-52](52-cloud-harness.md#rule-wp-52)

**Downstream — consumers of these released outputs.**

None.


---
