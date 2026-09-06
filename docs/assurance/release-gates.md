# Release Gates

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: the Product Quality Contract, **D-008**, **D-022**, **D-023**, **V-04**, **V-09**, and the deferred gates **F-013**, **F-023**, **F-026**
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
| GA-01 | **A gate result is recorded with its evidence artifact** in the release record (`RC-03` in the distribution requirements). |
| GA-02 | **A gate is either passed or blocked.** There is no "passed with concerns"; a concern is either a defect or a waiver. |
| GA-03 | **A waiver is explicit, owned and expiring** (`§21.1` of the quality contract). An expired waiver blocks release automatically. |
| GA-04 | **A gate may not be waived if it protects data integrity, security, licence compliance or a regulatory obligation.** |
| GA-05 | **Adding a gate is cheap; removing one requires a recorded decision.** |

---

## 2. G — Continuous gates

| # | Gate | Evidence |
|---|---|---|
| G-01 | Build clean: zero errors; zero warnings-as-errors; no suppressed AOT, trim or single-file diagnostic on the main path | Build log |
| G-02 | Architecture tests pass (`AT-01`–`AT-14`) | Test results |
| G-03 | Repository policy tests pass (`RP-01`–`RP-10`), including licence boundary, forbidden references and banned APIs | Test results |
| G-04 | Forbidden-term scan clean: no forbidden alias, no superseded product name, no superseded payment provider outside `docs/inputs/` (**D-002**, **D-005**, **D-018**) | Scan report |
| G-05 | Contract baseline check: any change to a generated contract artifact is accompanied by a version change and a compatibility note (**D-009**) | Contract diff |
| G-06 | Domain, application and serialization test families pass (`F-01`, `F-02`, `F-04`) | Test results |
| G-07 | Type-shape and serialization compatibility baseline unchanged, or changed with a declared version bump | Baseline diff |
| G-08 | No new dependency without a licence, provenance and closure record (`§4.2` of the provenance document) | Dependency report |
| G-09 | Documentation link and identifier integrity: every cross-reference resolves (`SV-01`, `SV-02` in the testing strategy) | Link report |

---

## 3. R — Per-release gates

| # | Gate | Evidence |
|---|---|---|
| R-01 | All continuous gates pass on the release commit | Gate report |
| R-02 | Integration families pass: persistence, local RPC, public API contract, realtime, multi-process (`F-03`, `F-05`, `F-06`, `F-07`, `F-11`) | Test results |
| R-03 | **AOT publish succeeds for every desktop product and the published artifact launches** (**D-008**, **V-05**) | Publish log plus launch smoke result |
| R-04 | Migration and golden-fixture tests pass, forward and — where reversibility is claimed — backward (`F-12`) | Fixture comparison |
| R-05 | Crash, fault-injection and recovery tests pass (`F-13`) | Recovery outcomes |
| R-06 | Performance budgets met with the regression gate applied: startup, memory, responsiveness, bundle size (`§2`–`§6` of the quality contract) | Measured values versus budget and previous release |
| R-07 | Accessibility gates pass, automated and assistive-technology-verified (`F-10`) | Automated results plus dated manual record |
| R-08 | Localisation gates pass: no hard-coded user-visible string, locale-safe data handling (`§11` there) | Scan plus test results |
| R-09 | Native ABI tests pass per runtime identifier, including error paths (`F-08`) | Per-RID results |
| R-10 | Install, update, downgrade-protection and rollback matrix passes (`F-16`) | Matrix results |
| R-11 | Signing complete and verified on the packaged artifact; macOS notarised and stapled | Verification output |
| R-12 | SBOM, provenance attestation, licence inventory and NOTICE produced and verified | Artifacts |
| R-13 | Compatibility manifest published: minimum OS, minimum cloud version, supported client window (`§15` there) | Manifest |
| R-14 | Release record complete and immutable (`RC-03` there) | Release record |
| R-15 | No open severity-blocking quality issue; no expired waiver (`§21` there) | Quality report |
| R-16 | Telemetry redaction test passes: no marker value in exported signals (`§14` of the observability architecture) | Redaction report |

---

## 4. C — Channel promotion gates

| # | Gate | Applies to |
|---|---|---|
| C-01 | All per-release gates passed for this exact artifact — no rebuild (`BR-01` in the build architecture) | Every promotion |
| C-02 | Soak and scale results within budget for the promotion's duration requirement (`F-14`) | Beta → Stable |
| C-03 | Cross-platform matrix complete for every supported platform and architecture (`§20` of the quality contract) | Beta → Stable |
| C-04 | Hardware-lab verification complete for ArcScope and ArcSlate (`F-18`) | Beta → Stable for those products |
| C-05 | Update feed entry prepared with hashes, compatibility ranges and minimum versions (`§7` of the build architecture) | Every promotion |
| C-06 | Rollback path verified for this specific version pair | Every promotion |
| C-07 | Nightly and canary artifacts are never submitted to a platform store (`§2` of the distribution requirements) | Store submission |

---

## 5. P — Product first-release gates

| # | Gate | Evidence |
|---|---|---|
| P-01 | The product's **Reference Coverage Matrix** is complete, with a disposition for every item (**D-012**; `CM-07` in the provenance document) | Matrix |
| P-02 | The product's **licence audit** is complete — the **F-013** trigger has fired and been satisfied for this product (**D-013**) | Audit record |
| P-03 | The product's Quality Contract instance is populated with measured values, not targets (`§1` of the quality contract) | Quality report |
| P-04 | Must-pass release scenarios pass for this product (`§27` there), including the **product's own** offline-start scenario: launch never requires an account (`ID-01` of the identity requirements); for a Cloud-authoritative product, an **enrolled, hydrated** workspace opens editable with Cloud unreachable and **without an interactive re-authentication prompt**, pending edits visibly unsynchronised | Scenario results |
| P-05 | The product's **declared** exit path is met. **ArcScope and ArcSlate**: a portable package that re-imports completely and serialises deterministically (`WS-01`–`WS-06` of the data-format requirements; `WP-35.04`, `WP-39.02`). **ArcNotes and ArcChat**: a Cloud-generated download over acknowledged revisions with an attachment manifest and a stated fidelity/exclusion report — **re-import is not an obligation for these two** (`EP-04` of the ArcNotes requirements, `EX-01` of the ArcChat requirements), so a round-trip result is not the evidence and must not be demanded | Round-trip result, or export completeness and fidelity report, per the product's declared path |
| P-06 | The product's capability set, risk levels and approval postures are reviewed and recorded (`§4` of the security requirements) | Capability register |
| P-07 | Deep links, file associations and single-instance routing verified (`§7`, `§8` of the shared desktop requirements) | Test results |
| P-08 | Diagnostics, crash reporting and consent behaviour verified (`§9` of the observability architecture) | Test results |

---

## 6. L — Go-live gates

### 6.1 Paid cloud go-live

**The threshold is "failure behaves correctly", not "the happy path works."** (`§12` of the cloud product requirements)

| # | Gate |
|---|---|
| L-01 | A full **Game Day** exercising SEV0 through SEV2 scenarios against the real production topology |
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
| L-12 | Every required runbook written, assigned and rehearsed at least once (`§9.1` there) |
| L-13 | Backup health dashboard green **with a proven restore**, not merely a green backup job |
| L-14 | Status page live, independently hosted, with the emergency alternate URL published (`§8` of the observability architecture) |
| L-15 | Alert-to-runbook mapping complete; on-call responder arrangement in place (`§7` there) |

### 6.2 Commercial go-live

**Until funds are actually received, the correct statement is "technical integration complete" — not "the commercial loop is closed."** (`§18` of the commerce requirements)

| # | Gate |
|---|---|
| L-20 | Supplier onboarding and account approval complete |
| L-21 | Sanctions and export screening completed for the intended market set |
| L-22 | Payout eligibility and receiving-currency confirmed |
| L-23 | One real card payment completed |
| L-24 | One real subscription created |
| L-25 | One real renewal observed |
| L-26 | One cancellation and one reactivation completed |
| L-27 | One refund completed **with entitlement rollback verified** |
| L-28 | Webhook duplicate-and-loss recovery test passed |
| L-29 | Reconciliation repair test passed |
| L-30 | **A completed payout received** |
| L-31 | Credit lifecycle demonstrated end to end: reservation, settlement, release, expiry, refund hold (`§13` of the commerce architecture) |

### 6.3 Regional enablement

| # | Gate |
|---|---|
| L-40 | Every one of the eight Mainland China pre-enablement gates recorded as met before that route is enabled (**D-023**) |
| L-41 | The route remains disabled by configuration until `L-40` is satisfied, and the configuration state is verified in the release gate (`RG-04` in the commerce architecture) |

### 6.4 Mobile release

| # | Gate |
|---|---|
| L-50 | **F-023**: complete direct and transitive dependency closure verified before the first artifact is produced (**D-004**; `PL-06` in the distribution requirements) |
| L-51 | **V-09**: store category fit and consumption-only conformance confirmed by review, not by reading the guideline (`PL-07` there) |
| L-52 | Commerce-prohibition build check passes: no purchase surface, no embedded checkout, no store billing, no external purchase call to action, **no licence-key or purchase-token unlock path** (`MC-01`–`MC-06` in the mobile architecture) |
| L-53 | Android runtime posture confirmed by inspecting the produced release artifact, not the project file (`RT-07` there) |
| L-54 | Release artifact built by CI and smoke-tested on a real device (`RT-08` there) |
| L-55 | Store developer account established under the intended long-term owning identity (`PL-05` in the distribution requirements) |

### 6.5 Extension platform opening

| # | Gate |
|---|---|
| L-60 | Extension protocol conformance suite passes against a reference extension covering every contribution kind (`XT-01` in the extension architecture) |
| L-61 | Isolation suite passes: crash, hang, memory exhaustion and unbounded output each leave the host healthy |
| L-62 | Permission presentation, grant, re-consent and revocation verified end to end |
| L-63 | Catalog-as-untrusted suite passes |
| L-64 | Public SDK compatibility commitment published, with the protocol and SDK versions separated (`§10` there) |

---

## 7. D — Deferred-gate closure

| Gate | Trigger | Owner | Blocks |
|---|---|---|---|
| **F-013** — reference licence determinations | The first step of a product's Reference Coverage Matrix and licence audit, before substantive reference source is used for planning or implementation (**D-013**) | Licensing and Provenance Owner | `P-02` for that product |
| **F-023** — mobile provenance and dependency closure | Before the first mobile artifact is produced (**D-004**) | Release Engineering Owner and Licensing and Provenance Owner; Product Owner approves | `L-50` |
| **F-026** — typed HTTP client AOT packaging | First use of the typed HTTP client on an AOT or trimmed target | Architecture Owner | `R-03` for any target consuming it |

Full state is tracked in [`open-gates-register.md`](open-gates-register.md).

---

## 8. Gate ownership

| Gate class | Accountable role |
|---|---|
| G | Architecture Owner |
| R | Release Engineering Owner |
| C | Release Engineering Owner |
| P | Product Owner, with the Architecture Owner for `P-01`, `P-02`, `P-06` |
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
| **D-012**, **D-013**, **F-013** | Product first-release reference and licence gates |
| **D-022**, **V-09**, **F-023** | Mobile release gates |
| **D-023** | Regional enablement gates |
| **F-026** | The typed HTTP client packaging gate |
