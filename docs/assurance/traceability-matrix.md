# Traceability Matrix

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: **D-001** (conflict-resolution rule), **D-018** (glossary and invariant catalogue)
> Companions: [`../decisions/phase-1-foundation-decisions.md`](../decisions/phase-1-foundation-decisions.md), [`phase-1-official-verification.md`](phase-1-official-verification.md), [`open-gates-register.md`](open-gates-register.md), [`release-gates.md`](release-gates.md)

This matrix answers four questions with evidence rather than assertion:

1. **Is every Phase 1 decision carried into Phase 2?**
2. **Is every verification finding enforced somewhere, and gated where required?**
3. **Does every requirement have an architecture, a test family and a work package?**
4. **Is every invariant enforceable?**

Where coverage is incomplete, this document says so, with the package that closes it.

---

## 1. Decision coverage — D-001 … D-023

Every decision is carried. The **Primary home** column names where the decision is realised in most detail; the **Also enforced in** column names the other layers that depend on it.

| Decision | Subject | Primary home | Also enforced in | Enforced by |
|---|---|---|---|---|
| **D-001** | Conflict-resolution rule | `../planning/implementation-sequence.md` `§6` (`WF-03`) | Every work package's conflict rule | Process; `WP-05.06` specification-integrity checks |
| **D-002** | Product baseline — four products | `../requirements/00-product-scope-and-portfolio.md` | Every product document; the reference map | Forbidden-term scan (`WP-00.00`, `G-04`) |
| **D-003** | Verification scope and first-consumption | `open-gates-register.md` `§5` | `reference-coverage-and-provenance.md` | Register review; `NV-02` |
| **D-004** | ArcChat Mobile licensing boundary | `../architecture/11-mobile-architecture.md` `§2` | Solution layout `§4`; provenance `§4`; `WP-30`, `WP-32` | Licence policy tests (`G-03`), **F-023** closure |
| **D-005** | Payment provider baseline | `../architecture/16-billing-and-commerce-architecture.md` | Commerce requirements; `WP-42` | Provider containment architecture test (`CT-09`) |
| **D-006** | ArcNotes complete scope | `../requirements/products/arcnotes.md` | `WP-18`, `WP-27`, `WP-28`, `WP-29` | The V1→V4 migration chain gate (`WP-29.04`) |
| **D-007** | Web technology and rendering boundary | `../architecture/10-web-architecture.md` | `WP-47`, `WP-48`, `WP-49` | Prohibited-technology policy test; no-script render test |
| **D-008** | Runtime and AOT matrix | `../architecture/14-build-packaging-and-release.md` `§3` | Desktop, cloud, mobile, web architecture; `WP-02`, `WP-06`, `WP-30` | Evaluated-property assertions; AOT publish proof (`R-03`) |
| **D-009** | Contract granularity | `../architecture/02-contracts-and-protocols.md` | Solution layout `§3`; `WP-03`, `WP-23` | Contract baseline diff gate (`G-05`) |
| **D-010** | Cloud topology | `../architecture/00-architecture-overview.md` `§3` | Local IPC, cloud, mobile architecture; `WP-08`, `WP-26`, `WP-31` | No-inbound-connection assertions (`WP-26.01`, `WP-31.06`) |
| **D-011** | Target monorepo | `implementation-state-reconciliation.md` | Solution layout `§1`; `WP-01` | Inventory gate `PG-02` |
| **D-012** | Reference-repository roles | `reference-coverage-and-provenance.md` `§1` | Every product document's reference posture; `WP-00.04` | Matrix completion gate `PG-01` |
| **D-013** | Reuse policy | `reference-coverage-and-provenance.md` `§3`, `§4` | Solution layout `LB-07`; `WP-00.03` | Provenance-record check (`AE-06`), **F-013** |
| **D-014** | Web and service surface inventory | `../architecture/10-web-architecture.md` `§4` | Observability `§8`, `§10`; build `§7`; `WP-47` | Surface deployment matrix; origin policy tests |
| **D-015** | Account portal URL | `../architecture/10-web-architecture.md` `§4` | `WP-48`, `WP-49` | Redirect and profile-isolation tests (`WP-48.00`) |
| **D-016** | Deferred-decision ownership | `open-gates-register.md` | Native architecture `NI-10` | Register ownership fields |
| **D-017** | Planning location and format | `../planning/README.md` | `../planning/work-packages/README.md` | Repository structure; `WP-05.06` |
| **D-018** | Normative glossary | `../requirements/01-normative-glossary-and-invariants.md` | Every layer's vocabulary; `WP-00.01` | Forbidden-term scan; invariant coverage gate `PG-06` |
| **D-019** | Sequence status | `../planning/implementation-sequence.md` `§1.1` | `../planning/work-packages/README.md` | Derivation-condition rules `DC-01`–`DC-04` |
| **D-020** | AI and payment economic model | `../architecture/16-billing-and-commerce-architecture.md` | Commerce requirements; `WP-42`, `WP-43` | Fixed-precision policy test (`CT-05`); no-compiled-figure scan (`WP-42.01`) |
| **D-021** | Apache boundary for validators and shared semantics | `../architecture/11-mobile-architecture.md` `§1` | Solution layout `§3`; extension SDK `§11`; `WP-30.01` | Shared/not-shared policy test |
| **D-022** | Mobile-store commerce | `../architecture/11-mobile-architecture.md` `§9` | Commerce architecture `§10`; `WP-31`, `WP-32` | Five commerce-prohibition build checks (`WP-32.03`) |
| **D-023** | Mainland China payment route | `../architecture/16-billing-and-commerce-architecture.md` `§11` | Commerce requirements `§12`; `WP-42.10` | Configuration assertion; gate `L-40` |

**Coverage: 23 of 23 decisions carried, each with a named enforcement mechanism.**

---

## 2. Verification finding coverage — V-01 … V-09

| Finding | Subject | Architecture home | Gate | Scheduled in |
|---|---|---|---|---|
| **V-01** | AI transparency obligations | `../requirements/07-security-privacy-and-trust.md`; `../architecture/09-ai-and-agent-runtime-architecture.md` | `VG-01` — marking mechanism per artifact type before first EU availability | `WP-43.04` |
| **V-02** | MCP specification status and vocabulary collision | `../architecture/15-extension-platform-architecture.md` `§5`; glossary `§9` | `VG-02` — SDK pin and explicit vocabulary mapping | `WP-41.07` |
| **V-03** | Cloud runtime posture | `../architecture/05-cloud-architecture.md` `§1` | No gate for cloud; the JIT decision removes it | `WP-06.04`, `WP-21.00` |
| **V-04** | Android runtime posture | `../architecture/11-mobile-architecture.md` `§3` | `VG-07` artifact confirmation; `VG-08` upgrade re-verification; `VG-09` iOS activation | `WP-32.01`, `WP-02.05`, deferred |
| **V-05a** | Third-party control AOT | `../architecture/04-desktop-application-architecture.md` `§2` | `VG-03` — publish proof per control | `WP-10.08` |
| **V-05b** | Local RPC generated shapes | `../architecture/02-contracts-and-protocols.md` `§12` | `VG-04` — AOT proof plus policy test | `WP-03.04`, `WP-06.01` |
| **V-05c** | Typed HTTP client AOT packaging | `../architecture/11-mobile-architecture.md` `SC-02`; build `§3` | **F-026** | `WP-03.02`, `WP-06.02` |
| **V-05d** | Realtime under AOT | `../architecture/05-cloud-architecture.md` `§7` | Covered by the desktop AOT proof | `WP-06.03` |
| **V-05e** | Cloud dependency set under AOT | `../architecture/05-cloud-architecture.md` `§1` | `VG-06` — dormant unless a cloud component becomes an AOT deliverable | Not scheduled; conditional |
| **V-06** | Merchant-of-Record role | `../architecture/16-billing-and-commerce-architecture.md` `§1` | `VG-10` — onboarding, approval and screening | `WP-42.10` |
| **V-07** | Payout relationship and settlement timing | `../architecture/16-billing-and-commerce-architecture.md` `§9` | `VG-11` — eligibility and currency confirmation | `WP-42.10` |
| **V-08** | Regional payment route constraints | `../architecture/16-billing-and-commerce-architecture.md` `§11` | `VG-12` — three sharpened regional gates | `WP-42.10`, conditional |
| **V-09** | Mobile storefront commerce rules | `../architecture/11-mobile-architecture.md` `§9` | `VG-13` — category fit and consumption-only by review | `WP-32.04` |

**Coverage: 9 of 9 findings enforced; 12 active gates scheduled, 2 dormant by design, 1 merged into F-026.**

---

## 3. Requirements → architecture → tests → work packages

| Requirement document | Primary architecture | Primary test families | Primary work packages |
|---|---|---|---|
| `00-product-scope-and-portfolio` | `00-architecture-overview` | F-17 | `00`, `01`, `02` |
| `01-normative-glossary-and-invariants` | All (vocabulary) | F-01, F-17 | `00`, `05` |
| `02-identity-account-and-workspace` | `08-security-architecture` | F-02, F-03, F-11 | `11`, `22`, `48` |
| `03-cloud-services-and-sync` | `07-sync-conflict-and-backup` | F-03, F-07, F-11, F-13 | `21`, `24`, `25`, `46` |
| `04-commerce-entitlement-and-credits` | `16-billing-and-commerce-architecture` | F-02, F-03, F-06 | `42`, `43`, `48` |
| `05-ai-and-agent-execution` | `09-ai-and-agent-runtime-architecture` | F-02, F-11, F-13 | `16`, `17`, `43` |
| `06-knowledge-search-and-retrieval` | `09-ai-and-agent-runtime-architecture` `§5` | F-03, F-11 | `19`, `40` |
| `07-security-privacy-and-trust` | `08-security-architecture` | F-02, F-11, F-17 | `11`, `22`, `41`, `45` |
| `08-extensions-and-developer-platform` | `15-extension-platform-architecture` | F-05, F-11, F-17 | `41` |
| `09-shared-desktop-experience` | `04-desktop-application-architecture` | F-09, F-10, F-15 | `10` |
| `10-distribution-update-and-support` | `14-build-packaging-and-release`; `13-observability-and-operations` | F-16, F-11 | `02`, `32`, `45`, `50` |
| `11-policy-and-configuration` | `05-cloud-architecture` `§12`; policy client | F-02, F-06, F-11 | `44` |
| `12-quality-and-compatibility-contract` | All (budgets and gates) | Every family | `02`, `05`, `06`, and each product package |
| `13-data-formats-and-portability` | `06-data-persistence-and-formats` | F-03, F-12, F-13 | `07`, `19`, `35`, `39` |
| `products/arcchat` | `04`, `09` architecture | F-02, F-05, F-11 | `15`, `17`, `20` |
| `products/arcnotes` | `04`, `06` architecture | F-03, F-09, F-12 | `18`, `19`, `27`, `28`, `29` |
| `products/arcscope` | `12-native-interop-and-media` `§8` | F-08, F-14, F-18 | `33`, `34`, `35` |
| `products/arcslate` | `12-native-interop-and-media` `§7` | F-08, F-15, F-18 | `36`, `37`, `38`, `39` |
| `products/arcchat-mobile-and-web` | `11-mobile-architecture`; `10-web-architecture` | F-04, F-06, F-16 | `30`, `31`, `32`, `49` |
| `products/arcforges-web` | `10-web-architecture` | F-09, F-10, F-15 | `47`, `48`, `49` |
| `products/arcforges-cloud` | `05-cloud-architecture`; `13-observability-and-operations` | F-03, F-07, F-13, F-14 | `21`–`26`, `45`, `46` |

Test family identifiers are those of [`testing-and-verification-strategy.md`](testing-and-verification-strategy.md) `§2`.

---

## 4. Architecture → work package

| Architecture document | Realised in |
|---|---|
| `00-architecture-overview` | `00`–`07` collectively |
| `01-solution-and-project-layout` | `01`, `02`, `05` |
| `02-contracts-and-protocols` | `03`, `04`, `09`, `23` |
| `03-local-ipc-and-process-model` | `08`, `14` |
| `04-desktop-application-architecture` | `06`, `10`, and each desktop product package |
| `05-cloud-architecture` | `21`, `23`, `24`, `26` |
| `06-data-persistence-and-formats` | `07`, `18`, `19` |
| `07-sync-conflict-and-backup` | `25`, `46` |
| `08-security-architecture` | `11`, `22`, `41` |
| `09-ai-and-agent-runtime-architecture` | `16`, `17`, `40`, `43` |
| `10-web-architecture` | `47`, `48`, `49` |
| `11-mobile-architecture` | `30`, `31`, `32` |
| `12-native-interop-and-media` | `13`, `33`, `34`, `36`, `37`, `38` |
| `13-observability-and-operations` | `12`, `45` |
| `14-build-packaging-and-release` | `02`, `06`, `32`, `50` |
| `15-extension-platform-architecture` | `41` |
| `16-billing-and-commerce-architecture` | `42`, `43` |

**Coverage: 17 of 17 architecture documents realised in at least one work package.**

---

## 5. Invariant enforcement

The catalogue in [`../requirements/01-normative-glossary-and-invariants.md`](../requirements/01-normative-glossary-and-invariants.md) contains roughly 490 `X ≠ Y` invariants across twelve sections. Each is assigned an enforcement mechanism in `WP-00.01` and asserted in `WP-05.05`.

| Mechanism | Applies to | Where implemented |
|---|---|---|
| **Type distinction** — the wrong thing does not compile | Identity, revision, sequence, version-axis and secret invariants | `WP-04.00`, `WP-04.02`, `WP-04.05`, `WP-11.04` |
| **Repository policy test** — naming, reference and structural rules | Forbidden aliases, obsolete names, layering, licence boundary, banned APIs | `WP-05.00`–`WP-05.04` |
| **Unit test** — behavioural distinctions | Undo vs checkpoint vs journal, search vs retrieval, trust vs permission, progress vs outcome | Each owning product package |
| **Integration or end-to-end test** — only observable across a boundary | Cloud sync vs raw upload, isolation vs authorization, push vs durable attention | `WP-25`, `WP-35`, `WP-41`, `WP-31` |

| # | Rule |
|---|---|
| IE-01 | **Every invariant has exactly one assigned mechanism** and at least one concrete test (`IV-01` in the testing strategy). |
| IE-02 | **An invariant with no test is an open finding** with an owner and a closing package, reported by `WP-05.05`. |
| IE-03 | **A test enforcing an invariant names it**, so a failure identifies the violated rule. |

**Status: the assignment is produced by `WP-00.01`; the 100 % coverage assertion is the completion gate of `WP-05.05` (`PG-06`).** Until that gate passes, invariant coverage is *specified* but not yet *demonstrated* — this document does not claim otherwise.

---

## 6. Gate → work package

Every gate in [`open-gates-register.md`](open-gates-register.md) is scheduled.

| Gate | Scheduled in | Blocking |
|---|---|---|
| **F-013** | `00.04`; then `15`, `18`, `33`, `36` per product | `P-02` per product |
| **F-023** | `32.02` | `L-50`, any mobile artifact |
| **F-026** | `03.02`, `06.02` | `R-03` on consuming targets |
| **VG-01** | `43.04` | First EU-available release |
| **VG-02** | `41.07` | Finalising the extension work package |
| **VG-03** | `10.08` | Third-party control adoption |
| **VG-04** | `03.04`, `06.01` | First AOT desktop deliverable |
| **VG-06** | Not scheduled — dormant | Conditional on a decision not taken |
| **VG-07** | `32.01` | First Android production build |
| **VG-08** | `02.05`, recurring | Every framework major upgrade |
| **VG-09** | Deferred with the iOS build | iOS release |
| **VG-10**, **VG-11** | `42.10` | Commercial go-live |
| **VG-12** | `42.10`, conditional | Regional enablement |
| **VG-13** | `32.04` | First store submission |
| **PG-01** | `00.04`; then per product | Product first release |
| **PG-02** | `01.00` | All restructuring |
| **PG-03** | `13.04`, `33`, `37.00` | Native dependency use |
| **PG-04** | `45.02` | Paid cloud go-live |
| **PG-05** | `12.02` | `R-16` |
| **PG-06** | `05.05` | Traceability completeness |
| **PG-07** | `19.05`, `35.04`, `39.05` | Public import claims |
| **PG-08** | `13.04` | `C-04` |
| **PG-09** | `41` | Third-party extension enablement |
| **PG-10** | `42.10`, `43.06` | `L-28`, `L-29` |

**Coverage: 25 of 25 gates scheduled or explicitly dormant.**

---

## 7. What this matrix does not claim

| # | Statement |
|---|---|
| NC-01 | **No gate is closed by this document.** Phase 2 schedules gates; only recorded evidence closes them. |
| NC-02 | **Invariant coverage is specified, not demonstrated.** The 100 % assertion is `WP-05.05`'s gate, not a present fact. |
| NC-03 | **The per-product Reference Coverage Matrices do not yet exist** beyond the ArcChat calibration matrix produced in `WP-00.04`. |
| NC-04 | **The item-level code inventory does not yet exist.** `implementation-state-reconciliation.md` records an observed first-pass inventory and states plainly that the item-level version is `WP-01.00`'s deliverable. |
| NC-05 | **No test in this matrix has been run.** This is a specification repository; the test families and gates are defined here and executed in the implementation repository. |

---

## 8. Maintenance

| # | Rule |
|---|---|
| MT-01 | **This matrix is updated whenever a document, gate or work package is added, removed or renamed.** |
| MT-02 | **`WP-05.06` asserts its integrity**: every identifier cited here must exist, and every architecture document, requirement document and gate must appear. |
| MT-03 | **A decision added in Phase 2** ([`../decisions/`](../decisions/README.md)) is added to `§1` with its enforcement mechanism. |
| MT-04 | **A gate discovered during implementation** is added to the register and to `§6` with its scheduling.
