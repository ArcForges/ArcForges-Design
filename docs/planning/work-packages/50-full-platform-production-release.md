# WP-50 — Full-Platform Production Release

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: K — Web and release
> Upstream: `20`, `29`, `32`, `35`, `39`, `43`, `46`, `49` · Downstream: —

> **Goal.** Ship everything together, once every gate is genuinely satisfied: four desktop products across three platforms, the Android companion, the cloud, the web surfaces, and the commercial loop — with the release audit, the production gates and the honest statement of what is and is not shipped.

---

## 1. Scope and purpose

**In scope.** The coordinated production release: official site entry points, downloads and documentation; account portal and checkout in production; Windows, macOS and Linux desktop releases; the Android release; cloud production with migration rehearsal, backup and restore, upgrade and rollback; the licence, SBOM and copied-content release audit; observability, alerting, runbook and incident closure; and the final production gates for the whole family.

**Out of scope.** iOS build activation, which remains deferred (**D-008**). Any capability whose gates are not satisfied — it ships disabled or not at all, never as a claim.

**Why this package exists.** `I2 §III.13` requires these to complete **together**. A release where the site is live but the payout path is unproven, or where downloads exist but rollback is untested, is not a release — it is an incident waiting for its first customer.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| `I2 §III.13` | The list of items that must complete together |
| [`../../assurance/release-gates.md`](../../assurance/release-gates.md) | Every gate class and its evidence |
| [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md) | Every open gate and whether it is now closed |
| [`../../architecture/14-build-packaging-and-release.md`](../../architecture/14-build-packaging-and-release.md) | Build, packaging, signing, feed and promotion |
| All upstream packages | Every product and platform capability being released |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Build once, promote the same artifact.** Production never rebuilds. |
| BR-02 | **A gate is passed with evidence or it is not passed.** There is no "passed with concerns". |
| BR-03 | **A gate protecting data integrity, security, licence compliance or a regulatory obligation cannot be waived.** |
| BR-04 | **Nothing incomplete is presented as complete.** A deferred capability is stated as deferred. |
| BR-05 | **Official pricing and checkout do not launch publicly before entitlement, refunds, webhook idempotency and a real payout path are complete** (`I2 §III.12`). |
| BR-06 | **iOS is not claimed as compiled or tested** (**D-008**). |
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

### WP-50.00 — Release readiness audit

**What must be fully done.** Every gate in [`release-gates.md`](../../assurance/release-gates.md) evaluated for every surface, with its evidence artifact named. Every gate in [`open-gates-register.md`](../../assurance/open-gates-register.md) either closed with evidence or explicitly recorded as still open with its blocking consequence stated.

**Testing requirements.** A gate-coverage report asserting no gate is unevaluated; an evidence-resolution check asserting every claimed evidence artifact exists; a **cross-system failure-row coverage check** asserting that every failure row in [`../../architecture/20-cross-system-lifecycles.md`](../../architecture/20-cross-system-lifecycles.md) names a test that exists and has run.

**Completion gate.** **Every gate is evaluated with a named, resolvable evidence artifact**, every open gate's blocking consequence is stated, and **no cross-system failure row lacks a run test**.

### WP-50.01 — Licence, SBOM and copied-content audit

**What must be fully done.** The full release audit: licence inventory per artifact, SBOM per artifact, provenance attestation, NOTICE generation verified against recorded attribution obligations, and a copied-content audit confirming every reused item has a completed provenance record.

**Testing requirements.** A closure report per artifact; a NOTICE verification; a provenance-completeness check across every recorded reuse.

**Completion gate.** Every shipped artifact has a licence inventory, SBOM, provenance attestation and verified NOTICE, and every reused item has a completed provenance record.

### WP-50.02 — Desktop release across three platforms

**What must be fully done.** Signed installers for Windows, macOS and Linux from the same CI-produced artifacts; the update feed populated with hashes, compatibility ranges and minimum versions; the full update matrix verified per platform; store and package-manager listings pointing at the same signed installer.

**Testing requirements.** The complete update matrix per platform — fresh install, upgrade, two-version upgrade, downgrade protection, rollback, interrupted download, interrupted install, corrupted artifact rejection, update during a long task, update with documents open, uninstall preserving user data, channel switch both ways, blocked bad version.

**Completion gate.** **The full update matrix passes on all three desktop platforms**, and a blocked bad version is refused by both the feed and compatibility policy.

### WP-50.03 — Android release

**What must be fully done.** The Android artifact submitted and released with every mobile gate satisfied from `32`, and the store listing consistent with the consumption-only posture.

**Testing requirements.** Post-release install and update verification from the store channel; a listing-consistency check.

**Completion gate.** The Android release is live with every mobile gate closed and the listing consistent with the consumption-only posture.

### WP-50.04 — Cloud production

**What must be fully done.** Production deployment from a promoted artifact; migration rehearsed forward and backward; backup verified with a proven restore; upgrade and rollback rehearsed; the full go-live gate set from `L-01` to `L-15` satisfied; the status page live with its emergency alternate URL published.

**Testing requirements.** A game-day exercise across the severity ladder against the real production topology; the recorded evidence for each go-live gate.

**Completion gate.** **The cloud go-live threshold is met — "failure behaves correctly"** — with a completed game day and evidence for every gate.

### WP-50.05 — Commercial launch

**What must be fully done.** Account portal and checkout in production; official pricing published only after entitlement, refunds, webhook idempotency and a **received payout** are all proven; the regional route disabled unless its own gates are met.

**Testing requirements.** The full commercial gate evidence set from `42`; a configuration assertion on the regional route.

**Completion gate.** **Pricing and checkout are public only after a payout has actually been received**; until then the statement is "technical integration complete". The regional route remains disabled unless its gates are met.

### WP-50.06 — Web surfaces

**What must be fully done.** The static site, account portal and web companion deployed atomically per surface from promoted artifacts, each with its own origin policy, with rollback restoring the previous artifact set and a cached-older-client path that refreshes with a grace period rather than breaking.

**Testing requirements.** Atomic deployment and rollback per surface; a cached-client compatibility test; a cross-surface isolation assertion.

**Completion gate.** Every web surface deploys atomically, rolls back cleanly, and handles a cached older client with a grace period.

### WP-50.07 — Operational readiness

**What must be fully done.** Alerting live with every alert mapped to a rehearsed runbook; on-call arrangement in place; incident process exercised; support entry points live; enforcement and appeal paths operable; advisory process rehearsed.

**Testing requirements.** An alert-to-runbook completeness assertion; an on-call verification; a support-path end-to-end test.

**Completion gate.** Every alert maps to a rehearsed runbook, on-call is in place, and support and appeal paths are operable.

### WP-50.08 — Honest release statement

**What must be fully done.** A published statement of what ships, what is deferred and what is disabled: iOS as planned and build-deferred; any capability whose gates are unmet as disabled rather than claimed; the supported platform, browser and device matrices; and the supported client window.

**Testing requirements.** A claim-audit comparing every public statement against the gate evidence.

**Completion gate.** **Every public claim is backed by gate evidence**, and every deferred or disabled capability is stated as such.

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
| Gate coverage report with resolvable evidence artifacts | `WP-50.00` |
| Licence inventory, SBOM, attestation, NOTICE and provenance closure | `WP-50.01` |
| Full update matrix results per desktop platform | `WP-50.02` |
| Store install and update verification | `WP-50.03` |
| Game-day record and per-gate go-live evidence | `WP-50.04` |
| Commercial gate evidence including the received payout | `WP-50.05` |
| Atomic deployment, rollback and cached-client results | `WP-50.06` |
| Alert-to-runbook, on-call and support-path results | `WP-50.07` |
| Claim audit against gate evidence | `WP-50.08` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. **Every gate in the release-gate set is evaluated with a named, resolvable evidence artifact**, and every still-open gate's blocking consequence is stated.
2. Every shipped artifact has a licence inventory, SBOM, provenance attestation and verified NOTICE; every reused item has a completed provenance record.
3. **The full update matrix passes on Windows, macOS and Linux**, and a blocked bad version is refused by both the feed and compatibility policy.
4. The Android release is live with every mobile gate closed and a listing consistent with the consumption-only posture.
5. **The cloud go-live threshold is met** — a completed game day across the severity ladder, proven restore, rehearsed rollback and region rebuild, and evidence for every gate from `L-01` to `L-15`.
6. **Pricing and checkout are public only after a payout has actually been received**; the regional route remains disabled unless its own gates are met.
7. Every web surface deploys atomically, rolls back cleanly, and handles a cached older client with a grace period.
8. Every alert maps to a rehearsed runbook; on-call is in place; support, enforcement and appeal paths are operable.
9. **Every public claim is backed by gate evidence**; iOS is stated as planned and build-deferred; nothing incomplete is presented as complete.

---

## 9. Dependencies

**Upstream.**

| Package | What this needs from it |
|---|---|
| `20` | The proven cross-product workflow as a must-pass scenario |
| `29` | ArcNotes complete per **D-006** |
| `32` | A shippable Android artifact with every mobile gate satisfied |
| `35` | ArcScope complete and integrated |
| `39` | ArcSlate complete and integrated |
| `43` | Managed AI metered and transparent |
| `46` | Proven backup and recovery |
| `49` | The web companion |

**Downstream.** None. This is the final package in the sequence.

---

## 10. After this package

The sequence ends here, but three obligations continue:

| # | Continuing obligation |
|---|---|
| CO-01 | **`VG-08` recurs on every framework major upgrade** — the Android runtime posture is re-verified and the mobile AOT and trim proof re-run. |
| CO-02 | **`VG-09` fires if and when iOS build activation is decided** — the release runtime is re-verified against the then-current supported baseline. |
| CO-03 | **`VG-06` remains dormant** unless a decision moves a cloud component into an AOT deliverable, at which point its full dependency closure requires an AOT publish proof. |
