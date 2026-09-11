# Release Gates

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: the Product Quality Contract, **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)**, **[V-04](phase-1-official-verification.md#rule-v-04)**, **[V-09](phase-1-official-verification.md#rule-v-09)**, and the deferred gates **[F-013](open-gates-register.md#rule-f-013)**, **[F-023](open-gates-register.md#rule-f-023)**, **[F-026](open-gates-register.md#rule-f-026)**
> Companions: [`testing-and-verification-strategy.md`](testing-and-verification-strategy.md), [`../architecture/14-build-packaging-and-release.md`](../architecture/14-build-packaging-and-release.md), [`../requirements/12-quality-and-compatibility-contract.md`](../requirements/12-quality-and-compatibility-contract.md), [`open-gates-register.md`](open-gates-register.md)

This document consolidates every gate that stands between work and users, in one place, so no gate lives only inside the document that invented it.

**A gate is a machine-evaluated condition with a named evidence artifact.** A gate that depends on someone remembering is not a gate.

---

## 1. Gate classes

| Class | When evaluated | Blocks |
|---|---|---|
| **G — Continuous** | Every pull request and main build | Merge |
| **R — Per-release** | Every release build, per product | Promotion to any channel |
| **C — Channel promotion** | Moving a release between channels | That promotion |
| **P — Product first release** | The first public release of a product | That product's launch |
| **L — Go-live** | The first time a paid or externally exposed capability opens | That capability's launch |
| **D — Deferred-gate closure** | When a deferred gate's trigger fires | The work that depends on it |

| # | Rule |
|---|---|
| GA-01 | **A gate result is recorded with its evidence artifact** in the release record ([RC-03](../requirements/10-distribution-update-and-support.md#rule-rc-03) in the distribution requirements). |
| GA-02 | **A gate is either passed or blocked.** There is no "passed with concerns"; a concern is either a defect or a waiver. |
| GA-03 | **A waiver is explicit, owned and expiring** (`§21.1` of the quality contract). An expired waiver blocks release automatically. |
| GA-04 | **A gate may not be waived if it protects data integrity, security, licence compliance or a regulatory obligation.** |
| GA-05 | **Adding a gate is cheap; removing one requires a recorded decision.** |

---

## 2. G — Continuous gates

| # | Gate | Evidence |
|---|---|---|
| G-01 | Build clean: zero errors; zero warnings-as-errors; no suppressed AOT, trim or single-file diagnostic on the main path | Build log |
| G-02 | Architecture tests pass ([AT-01](../architecture/01-solution-and-project-layout.md#rule-at-01)–[AT-14](../architecture/01-solution-and-project-layout.md#rule-at-14)) | Test results |
| <a id="rule-g-03"></a>G-03 | Repository policy tests pass ([RP-01](../architecture/01-solution-and-project-layout.md#rule-rp-01)–[RP-10](../architecture/01-solution-and-project-layout.md#rule-rp-10)), including licence boundary, forbidden references and banned APIs | Test results |
| <a id="rule-g-04"></a>G-04 | Forbidden-term scan clean: no forbidden alias, no superseded product name, no superseded payment provider outside `docs/deprecated-inputs/` (**[D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002)**, **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)**, **[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)**) | Scan report |
| <a id="rule-g-05"></a>G-05 | Contract baseline check: any change to a generated contract artifact is accompanied by a version change and a compatibility note (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**) | Contract diff |
| G-06 | Domain, application and serialization test families pass ([F-01](testing-and-verification-strategy.md#rule-f-01), [F-02](testing-and-verification-strategy.md#rule-f-02), [F-04](testing-and-verification-strategy.md#rule-f-04)) | Test results |
| G-07 | Type-shape and serialization compatibility baseline unchanged, or changed with a declared version bump | Baseline diff |
| G-08 | No new dependency without a licence, provenance and closure record (`§4.2` of the provenance document) | Dependency report |
| G-09 | Documentation link and identifier integrity: every cross-reference resolves ([SV-01](testing-and-verification-strategy.md#rule-sv-01), [SV-02](testing-and-verification-strategy.md#rule-sv-02) in the testing strategy) | Link report |

---

## 3. R — Per-release gates

| # | Gate | Evidence |
|---|---|---|
| R-01 | All continuous gates pass on the release commit | Gate report |
| R-02 | Integration families pass: persistence, local RPC, public API contract, realtime, multi-process ([F-03](testing-and-verification-strategy.md#rule-f-03), [F-05](testing-and-verification-strategy.md#rule-f-05), [F-06](testing-and-verification-strategy.md#rule-f-06), [F-07](testing-and-verification-strategy.md#rule-f-07), [F-11](testing-and-verification-strategy.md#rule-f-11)) | Test results |
| <a id="rule-r-03"></a>R-03 | **AOT publish succeeds for every desktop product and the published artifact launches** (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-05](phase-1-official-verification.md#rule-v-05)**) | Publish log plus launch smoke result |
| R-04 | Migration and golden-fixture tests pass, forward and — where reversibility is claimed — backward ([F-12](testing-and-verification-strategy.md#rule-f-12)) | Fixture comparison |
| R-05 | Crash, fault-injection and recovery tests pass ([F-13](testing-and-verification-strategy.md#rule-f-13)) | Recovery outcomes |
| R-06 | Performance budgets met with the regression gate applied: startup, memory, responsiveness, bundle size (`§2`–`§6` of the quality contract) | Measured values versus budget and previous release |
| R-07 | Accessibility gates pass, automated and assistive-technology-verified ([F-10](testing-and-verification-strategy.md#rule-f-10)) | Automated results plus dated manual record |
| <a id="rule-r-08"></a>R-08 | Localisation gates pass: no hard-coded user-visible string, locale-safe data handling (`§11` there) | Scan plus test results |
| R-09 | Native ABI tests pass per runtime identifier, including error paths ([F-08](testing-and-verification-strategy.md#rule-f-08)) | Per-RID results |
| R-10 | Install, update, downgrade-protection and rollback matrix passes ([F-16](testing-and-verification-strategy.md#rule-f-16)) | Matrix results |
| R-11 | Signing complete and verified on the packaged artifact; macOS notarised and stapled | Verification output |
| R-12 | SBOM, provenance attestation, licence inventory and NOTICE produced and verified | Artifacts |
| R-13 | Compatibility manifest published: minimum OS, minimum cloud version, supported client window (`§15` there) | Manifest |
| R-14 | Release record complete and immutable ([RC-03](../requirements/10-distribution-update-and-support.md#rule-rc-03) there) | Release record |
| R-15 | No open severity-blocking quality issue; no expired waiver (`§21` there) | Quality report |
| <a id="rule-r-16"></a>R-16 | Telemetry redaction test passes: no marker value in exported signals (`§14` of the observability architecture) | Redaction report |

---

## 4. C — Channel promotion gates

| # | Gate | Applies to |
|---|---|---|
| C-01 | All per-release gates passed for this exact artifact — no rebuild ([BR-01](../architecture/14-build-packaging-and-release.md#rule-br-01) in the build architecture) | Every promotion |
| C-02 | Soak and scale results within budget for the promotion's duration requirement ([F-14](testing-and-verification-strategy.md#rule-f-14)) | Beta → Stable |
| C-03 | Cross-platform matrix complete for every supported platform and architecture (`§20` of the quality contract) | Beta → Stable |
| <a id="rule-c-04"></a>C-04 | Hardware-lab verification complete for ArcScope and ArcSlate ([F-18](testing-and-verification-strategy.md#rule-f-18)) | Beta → Stable for those products |
| C-05 | Update feed entry prepared with hashes, compatibility ranges and minimum versions (`§7` of the build architecture) | Every promotion |
| C-06 | Rollback path verified for this specific version pair | Every promotion |
| C-07 | Nightly and canary artifacts are never submitted to a platform store (`§2` of the distribution requirements) | Store submission |

---

## 5. P — Product first-release gates

| # | Gate | Evidence |
|---|---|---|
| <a id="rule-p-01"></a>P-01 | The product's **Reference Coverage Matrix** is complete, with a disposition for every item (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**; [CM-07](reference-coverage-and-provenance.md#rule-cm-07) in the provenance document) | Matrix |
| <a id="rule-p-02"></a>P-02 | The product's **licence audit** is complete — the **[F-013](open-gates-register.md#rule-f-013)** trigger has fired and been satisfied for this product (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) | Audit record |
| <a id="rule-p-03"></a>P-03 | The product's Quality Contract instance is populated with measured values, not targets (`§1` of the quality contract) | Quality report |
| P-04 | Must-pass release scenarios pass for this product, including every applicable initial-state row of the [offline acceptance matrix](testing-and-verification-strategy.md#offline-acceptance-matrix). Record enrollment/hydration/authorization and restart outcomes; no generic Cloud-authoritative editable-workspace assumption substitutes for the product behavior | Scenario results |
| P-05 | The product's **declared** exit path is met. **ArcScope and ArcSlate**: a portable package that re-imports completely and serialises deterministically ([WS-01](../requirements/13-data-formats-and-portability.md#rule-ws-01)–[WS-06](../requirements/13-data-formats-and-portability.md#rule-ws-06) of the data-format requirements; [WP-35.04](../planning/work-packages/35-arcscope-integration-and-sync.md#rule-wp-35.04), [WP-39.02](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.02)). **ArcNotes and ArcChat**: a Cloud-generated download over acknowledged revisions with an attachment manifest and a stated fidelity/exclusion report — **re-import is not an obligation for these two** ([EP-04](../requirements/products/arcnotes.md#rule-ep-04) of the ArcNotes requirements, [EX-01](../requirements/products/arcchat.md#rule-ex-01) of the ArcChat requirements), so a round-trip result is not the evidence and must not be demanded | Round-trip result, or export completeness and fidelity report, per the product's declared path |
| <a id="rule-p-06"></a>P-06 | The product's capability set, risk levels and approval postures are reviewed and recorded (`§4` of the security requirements) | Capability register |
| P-07 | Deep links, file associations and single-instance routing verified (`§7`, `§8` of the shared desktop requirements) | Test results |
| P-08 | Diagnostics, crash reporting and consent behaviour verified (`§9` of the observability architecture) | Test results |

---

## 6. L — Go-live gates

### 6.1 Paid cloud go-live

**The threshold is "failure behaves correctly", not "the happy path works."** (`§12` of the cloud product requirements)

| # | Gate |
|---|---|
| <a id="rule-l-01"></a>L-01 | A full **Game Day** exercising SEV0 through SEV2 scenarios against the real production topology |
| L-02 | Database failover exercised; point-in-time restore proven |
| L-03 | Cross-provider blob restore proven |
| L-04 | Message-broker backlog and dead-letter replay proven |
| L-05 | Realtime outage with client fallback and sequence backfill proven |
| L-06 | AI provider outage with credit release and fallback proven |
| L-07 | Edge or tunnel outage with local products fully unaffected, verified |
| L-08 | Email failover proven **without duplicate one-time codes** |
| L-09 | Deployment rollback exercised, and a migration failure recovered |
| L-10 | A region rebuild rehearsed from infrastructure-as-code plus backups |
| L-11 | Webhook loss recovered by reconciliation; entitlement repair verified |
| <a id="rule-l-12"></a>L-12 | Every required runbook written, assigned and rehearsed at least once (`§9.1` there) |
| <a id="rule-l-13"></a>L-13 | Backup health dashboard green **with a proven restore**, not merely a green backup job |
| L-14 | Status page live, independently hosted, with the emergency alternate URL published (`§8` of the observability architecture) |
| <a id="rule-l-15"></a>L-15 | Alert-to-runbook mapping complete; on-call responder arrangement in place (`§7` there) |

### 6.2 Commercial go-live

**Until funds are actually received, the correct statement is "technical integration complete" — not "the commercial loop is closed."** (`§18` of the commerce requirements)

| # | Gate |
|---|---|
| <a id="rule-l-20"></a>L-20 | Supplier onboarding and account approval complete |
| <a id="rule-l-21"></a>L-21 | Sanctions and export screening completed for the intended market set |
| <a id="rule-l-22"></a>L-22 | Payout eligibility and receiving-currency confirmed |
| L-23 | One real card payment completed |
| L-24 | One real subscription created |
| L-25 | One real renewal observed |
| L-26 | One cancellation and one reactivation completed |
| L-27 | One refund completed **with entitlement rollback verified** |
| <a id="rule-l-28"></a>L-28 | Webhook duplicate-and-loss recovery test passed |
| <a id="rule-l-29"></a>L-29 | Reconciliation repair test passed |
| L-30 | **A completed payout received** |
| <a id="rule-l-31"></a>L-31 | Credit lifecycle demonstrated end to end: reservation, settlement, release, expiry, refund hold (`§13` of the commerce architecture) |

### 6.3 Regional enablement

| # | Gate |
|---|---|
| <a id="rule-l-40"></a>L-40 | Every one of the eight Mainland China pre-enablement gates recorded as met before that route is enabled (**[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)**) |
| L-41 | The route remains disabled by configuration until [L-40](#rule-l-40) is satisfied, and the configuration state is verified in the release gate ([RG-04](../architecture/16-billing-and-commerce-architecture.md#rule-rg-04) in the commerce architecture) |

### 6.4 Mobile release

| # | Gate |
|---|---|
| <a id="rule-l-50"></a>L-50 | **[F-023](open-gates-register.md#rule-f-023)**: complete direct and transitive dependency closure verified before the first artifact is produced (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**; [PL-06](../requirements/10-distribution-update-and-support.md#rule-pl-06) in the distribution requirements) |
| <a id="rule-l-51"></a>L-51 | **[V-09](phase-1-official-verification.md#rule-v-09)**: store category fit and consumption-only conformance confirmed by review, not by reading the guideline ([PL-07](../requirements/10-distribution-update-and-support.md#rule-pl-07) there) |
| <a id="rule-l-52"></a>L-52 | Commerce-prohibition build check passes: no purchase surface, no embedded checkout, no store billing, no external purchase call to action, **no licence-key or purchase-token unlock path** ([MC-01](../architecture/11-mobile-architecture.md#rule-mc-01)–[MC-06](../architecture/11-mobile-architecture.md#rule-mc-06) in the mobile architecture) |
| <a id="rule-l-53"></a>L-53 | Android runtime posture confirmed by inspecting the produced release artifact, not the project file ([RT-07](../architecture/11-mobile-architecture.md#rule-rt-07) there) |
| L-54 | Release artifact built by CI and smoke-tested on a real device ([RT-08](../architecture/11-mobile-architecture.md#rule-rt-08) there) |
| L-55 | Store developer account established under the intended long-term owning identity ([PL-05](../requirements/10-distribution-update-and-support.md#rule-pl-05) in the distribution requirements) |

### 6.5 Extension platform opening

| # | Gate |
|---|---|
| <a id="rule-l-60"></a>L-60 | Extension protocol conformance suite passes against a reference extension covering every contribution kind ([XT-01](../architecture/15-extension-platform-architecture.md#rule-xt-01) in the extension architecture) |
| L-61 | Isolation suite passes: crash, hang, memory exhaustion and unbounded output each leave the host healthy |
| L-62 | Permission presentation, grant, re-consent and revocation verified end to end |
| L-63 | Catalog-as-untrusted suite passes |
| L-64 | Public SDK compatibility commitment published, with the protocol and SDK versions separated (`§10` there) |

---

## 7. D — Deferred-gate closure

| Gate | Trigger | Owner | Blocks |
|---|---|---|---|
| **[F-013](open-gates-register.md#rule-f-013)** — reference licence determinations | The first step of a product's Reference Coverage Matrix and licence audit, before substantive reference source is used for planning or implementation (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) | Licensing and Provenance Owner | [P-02](#rule-p-02) for that product |
| **[F-023](open-gates-register.md#rule-f-023)** — mobile provenance and dependency closure | Before the first mobile artifact is produced (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**) | Release Engineering Owner and Licensing and Provenance Owner; Product Owner approves | [L-50](#rule-l-50) |
| **[F-026](open-gates-register.md#rule-f-026)** — typed HTTP client AOT packaging | First use of the typed HTTP client on an AOT or trimmed target | Architecture Owner | [R-03](#rule-r-03) for any target consuming it |

Full state is tracked in [`open-gates-register.md`](open-gates-register.md).

---

## 8. Gate ownership

| Gate class | Accountable role |
|---|---|
| G | Architecture Owner |
| R | Release Engineering Owner |
| C | Release Engineering Owner |
| P | Product Owner, with the Architecture Owner for [P-01](#rule-p-01), [P-02](#rule-p-02), [P-06](#rule-p-06) |
| L (cloud) | Operations Owner |
| L (commercial) | Product Owner |
| L (regional) | Product Owner |
| L (mobile) | Release Engineering Owner |
| L (extension) | Architecture Owner |
| D | As recorded per gate |

| # | Rule |
|---|---|
| GO-01 | **A gate without a named accountable role is not deployed.** |
| GO-02 | **The accountable role approves the evidence, not the intention.** |
| GO-03 | **Roles are functions, not individuals**, and the current holder is recorded in the planning layer. |

---

## 9. Traceability

| Source | Consumed as |
|---|---|
| `§9` of the build architecture | The per-release gate set, consolidated here with evidence and ownership |
| `§12` of the cloud product requirements | The paid-cloud go-live threshold |
| `§18` of the commerce requirements | The commercial go-live threshold |
| `§1` of the distribution requirements | Mobile and store gates |
| `§21`, `§24`, `§27` of the quality contract | Waivers, the quality report, and must-pass release scenarios |
| **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**, **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**, **[F-013](open-gates-register.md#rule-f-013)** | Product first-release reference and licence gates |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)**, **[V-09](phase-1-official-verification.md#rule-v-09)**, **[F-023](open-gates-register.md#rule-f-023)** | Mobile release gates |
| **[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)** | Regional enablement gates |
| **[F-026](open-gates-register.md#rule-f-026)** | The typed HTTP client packaging gate |


## React/TypeScript Web release evidence

[P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) replaces the Web runtime proof with Node-built Site/Account/Chat artifacts. [PG-23](open-gates-register.md#rule-pg-23) requires real C#/TS SDK and session/realtime compatibility, consumer visual/accessibility/performance evidence, esproj/CLI workflow checks, exact-value correctness, npm provenance/SBOM and coherent edge/asset rollback. Existing native AOT and real commercial provider gates remain independent.
