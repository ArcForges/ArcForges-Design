# Traceability Matrix

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: **[D-001](../decisions/phase-1-foundation-decisions.md#rule-d-001)** (conflict-resolution rule), **[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** (glossary and invariant catalogue)
> Companions: [`../decisions/phase-1-foundation-decisions.md`](../decisions/phase-1-foundation-decisions.md), [`phase-1-official-verification.md`](phase-1-official-verification.md), [`open-gates-register.md`](open-gates-register.md), [`release-gates.md`](release-gates.md)

This matrix answers four questions with evidence rather than assertion:

1. **Is every Phase 1 decision carried into Phase 2?**
2. **Is every verification finding enforced somewhere, and gated where required?**
3. **Does every requirement have an architecture, a test family and a work package?**
4. **Is every invariant enforceable?**

Where coverage is incomplete, this document says so, with the package that closes it.

---

## 1. Decision coverage — [D-001](../decisions/phase-1-foundation-decisions.md#rule-d-001) … [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)

Every decision is carried. The **Primary home** column names where the decision is realised in most detail; the **Also enforced in** column names the other layers that depend on it.

| Decision | Subject | Primary home | Also enforced in | Enforced by |
|---|---|---|---|---|
| **[D-001](../decisions/phase-1-foundation-decisions.md#rule-d-001)** | Conflict-resolution rule | `../planning/implementation-sequence.md` `§6` ([WF-03](../planning/implementation-sequence.md#rule-wf-03)) | Every work package's conflict rule | Process; [WP-05.06](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.06) specification-integrity checks |
| **[D-002](../decisions/phase-1-foundation-decisions.md#rule-d-002)** | Product baseline — four products | `../requirements/00-product-scope-and-portfolio.md` | Every product document; the reference map | Forbidden-term scan ([WP-00.00](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.00), [G-04](release-gates.md#rule-g-04)) |
| **[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)** | Verification scope and first-consumption | `open-gates-register.md` `§5` | `reference-coverage-and-provenance.md` | Register review; [NV-02](open-gates-register.md#rule-nv-02) |
| **[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)** | ArcChat Mobile licensing boundary | `../architecture/11-mobile-architecture.md` `§2` | Solution layout `§4`; provenance `§4`; [WP-30](../planning/work-packages/30-mobile-shared-architecture.md#rule-wp-30), [WP-32](../planning/work-packages/32-mobile-release-and-store-gates.md#rule-wp-32) | Licence policy tests ([G-03](release-gates.md#rule-g-03)), **[F-023](open-gates-register.md#rule-f-023)** closure |
| **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)** | Payment provider baseline | `../architecture/16-billing-and-commerce-architecture.md` | Commerce requirements; [WP-42](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42) | Provider containment architecture test ([CT-09](../architecture/16-billing-and-commerce-architecture.md#rule-ct-09)) |
| **[D-006](../decisions/phase-1-foundation-decisions.md#rule-d-006)** *(as amended by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006))* | ArcNotes scope: notebook core, bounded properties, saved views | `../requirements/products/arcnotes.md` | [WP-18](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18), [WP-28](../planning/work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) — **`27` and `29` retired** | The migration chain gate ([WP-18.06](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.06)); the V4 stage is retired with `27` and `29` |
| **[D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007)** | Web technology and rendering boundary | `../architecture/10-web-architecture.md` | [WP-47](../planning/work-packages/47-static-public-site.md#rule-wp-47), [WP-48](../planning/work-packages/48-account-portal.md#rule-wp-48), [WP-49](../planning/work-packages/49-arcchat-web-companion.md#rule-wp-49) | Prohibited-technology policy test; no-script render test |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Runtime and AOT matrix | `../architecture/14-build-packaging-and-release.md` `§3` | Desktop, cloud, mobile, web architecture; [WP-02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02), [WP-06](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06), [WP-30](../planning/work-packages/30-mobile-shared-architecture.md#rule-wp-30) | Evaluated-property assertions; AOT publish proof ([R-03](release-gates.md#rule-r-03)) |
| **[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)** | Contract granularity | `../architecture/02-contracts-and-protocols.md` | Solution layout `§3`; [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-23](../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23) | Contract baseline diff gate ([G-05](release-gates.md#rule-g-05)) |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Cloud topology | `../architecture/00-architecture-overview.md` `§3` | Local IPC, cloud, mobile architecture; [WP-08](../planning/work-packages/08-local-ipc-and-registration.md#rule-wp-08), [WP-26](../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26), [WP-31](../planning/work-packages/31-arcchat-mobile-android.md#rule-wp-31) | No-inbound-connection assertions ([WP-26.01](../planning/work-packages/26-remote-action-and-tool-bridge.md#rule-wp-26.01), [WP-31.06](../planning/work-packages/31-arcchat-mobile-android.md#rule-wp-31.06)) |
| **[D-011](../decisions/phase-1-foundation-decisions.md#rule-d-011)** | Target monorepo | `implementation-state-reconciliation.md` — **item-level, 166 projects** | Solution layout `§1`; [WP-01](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01) | [PG-02](open-gates-register.md#rule-pg-02) **closed** by that evidence |
| **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** | Reference-repository roles — **amended 2026-09-05** by [P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005) (ArcSlate: ArcVideo and ArcVideoFoundation) | `reference-coverage-and-provenance.md` `§1` (method); [`reference-coverage/`](reference-coverage/README.md) (**the five completed matrices**) | Every product document's reference posture; [WP-00.04](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.04) | [PG-01](open-gates-register.md#rule-pg-01) **closed** by those matrices |
| **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** | Reuse policy | `reference-coverage-and-provenance.md` `§3`, `§4` | Solution layout [LB-07](../architecture/01-solution-and-project-layout.md#rule-lb-07); [WP-00.03](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.03) | Provenance-record check ([AE-06](reference-coverage-and-provenance.md#rule-ae-06)); **[F-013](open-gates-register.md#rule-f-013) closed** — 145 rows each carry a licence position and **no row proposes reuse** |
| **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** | Web and service surface inventory | `../architecture/10-web-architecture.md` `§4` | Observability `§8`, `§10`; build `§7`; [WP-47](../planning/work-packages/47-static-public-site.md#rule-wp-47) | Surface deployment matrix; origin policy tests |
| **[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)** | Account portal URL | `../architecture/10-web-architecture.md` `§4` | [WP-48](../planning/work-packages/48-account-portal.md#rule-wp-48), [WP-49](../planning/work-packages/49-arcchat-web-companion.md#rule-wp-49) | Redirect and profile-isolation tests ([WP-48.00](../planning/work-packages/48-account-portal.md#rule-wp-48.00)) |
| **[D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016)** | Deferred-decision ownership | `open-gates-register.md` | Native architecture [NI-10](../architecture/12-native-interop-and-media.md#rule-ni-10) | Register ownership fields |
| **[D-017](../decisions/phase-1-foundation-decisions.md#rule-d-017)** | Planning location and format | `../planning/README.md` | `../planning/work-packages/README.md` | Repository structure; [WP-05.06](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.06) |
| **[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** | Normative glossary | `../requirements/01-normative-glossary-and-invariants.md`; [`invariant-coverage.md`](invariant-coverage.md) | Every layer's vocabulary; [WP-00.01](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.01) | Forbidden-term scan; **[PG-06](open-gates-register.md#rule-pg-06) closed** (design traceability); [PG-11](open-gates-register.md#rule-pg-11) open (implementation enforcement) |
| **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** | Sequence status | `../planning/implementation-sequence.md` `§1.1` | `../planning/work-packages/README.md`; [`../planning/evidence-driven-revisions.md`](../planning/evidence-driven-revisions.md) | **Ordering followed**: the plan was derived after the matrices and the inventory. [P2-002](../decisions/phase-2-specification-decisions.md#rule-p2-002), which substituted a different ordering, is withdrawn; [P2-004](../decisions/phase-2-specification-decisions.md#rule-p2-004) records the re-derivation |
| **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** | AI and payment economic model | `../architecture/16-billing-and-commerce-architecture.md` | Commerce requirements; [WP-42](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42), [WP-43](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43) | Fixed-precision policy test ([CT-05](../architecture/16-billing-and-commerce-architecture.md#rule-ct-05)); no-compiled-figure scan ([WP-42.01](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.01)) |
| **[D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021)** | Apache boundary for validators and shared semantics | `../architecture/11-mobile-architecture.md` `§1` | Solution layout `§3`; extension SDK `§11`; [WP-30.01](../planning/work-packages/30-mobile-shared-architecture.md#rule-wp-30.01) | Shared/not-shared policy test |
| **[D-022](../decisions/phase-1-foundation-decisions.md#rule-d-022)** | Mobile-store commerce | `../architecture/11-mobile-architecture.md` `§9` | Commerce architecture `§10`; [WP-31](../planning/work-packages/31-arcchat-mobile-android.md#rule-wp-31), [WP-32](../planning/work-packages/32-mobile-release-and-store-gates.md#rule-wp-32) | Five commerce-prohibition build checks ([WP-32.03](../planning/work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.03)) |
| **[D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023)** | Mainland China payment route | `../architecture/16-billing-and-commerce-architecture.md` `§11` | Commerce requirements `§12`; [WP-42.10](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10) | Configuration assertion; gate [L-40](release-gates.md#rule-l-40) |

**Coverage: 23 of 23 decisions carried, each with a named enforcement mechanism.**

---

## 2. Verification finding coverage — [V-01](phase-1-official-verification.md#rule-v-01) … [V-09](phase-1-official-verification.md#rule-v-09)

| Finding | Subject | Architecture home | Gate | Scheduled in |
|---|---|---|---|---|
| **[V-01](phase-1-official-verification.md#rule-v-01)** | AI transparency obligations | `../requirements/07-security-privacy-and-trust.md`; `../architecture/09-ai-and-agent-runtime-architecture.md` | [VG-01](open-gates-register.md#rule-vg-01) — marking mechanism per artifact type before first EU availability | [WP-43.04](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.04) |
| **[V-02](phase-1-official-verification.md#rule-v-02)** | MCP specification status and vocabulary collision | `../architecture/15-extension-platform-architecture.md` `§5`; glossary `§9` | [VG-02](open-gates-register.md#rule-vg-02) — SDK pin and explicit vocabulary mapping | [WP-41.07](../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41.07) |
| **[V-03](phase-1-official-verification.md#rule-v-03)** | Cloud runtime posture | `../architecture/05-cloud-architecture.md` `§1` | No gate for cloud; the JIT decision removes it | [WP-06.04](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.04), [WP-21.00](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.00) |
| **[V-04](phase-1-official-verification.md#rule-v-04)** | Android runtime posture | `../architecture/11-mobile-architecture.md` `§3` | [VG-07](open-gates-register.md#rule-vg-07) artifact confirmation; [VG-08](open-gates-register.md#rule-vg-08) upgrade re-verification; [VG-09](open-gates-register.md#rule-vg-09) iOS activation | [WP-32.01](../planning/work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.01), [WP-02.05](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02.05), deferred |
| **[V-05a](phase-1-official-verification.md#rule-v-05a)** | Third-party control AOT | `../architecture/04-desktop-application-architecture.md` `§2` | [VG-03](open-gates-register.md#rule-vg-03) — publish proof per control | [WP-10.08](../planning/work-packages/10-design-system-and-desktop-shell.md#rule-wp-10.08) |
| **[V-05b](phase-1-official-verification.md#rule-v-05b)** | Local RPC generated shapes | `../architecture/02-contracts-and-protocols.md` `§12` | [VG-04](open-gates-register.md#rule-vg-04) — AOT proof plus policy test | [WP-03.04](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.04), [WP-06.01](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.01) |
| **[V-05c](phase-1-official-verification.md#rule-v-05c)** | Typed HTTP client AOT packaging | `../architecture/11-mobile-architecture.md` [SC-02](../architecture/11-mobile-architecture.md#rule-sc-02); build `§3` | **[F-026](open-gates-register.md#rule-f-026)** | [WP-03.02](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.02), [WP-06.02](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.02) |
| **[V-05d](phase-1-official-verification.md#rule-v-05d)** | Realtime under AOT | `../architecture/05-cloud-architecture.md` `§7` | Covered by the desktop AOT proof | [WP-06.03](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.03) |
| **[V-05e](phase-1-official-verification.md#rule-v-05e)** | Cloud dependency set under AOT | `../architecture/05-cloud-architecture.md` `§1` | [VG-06](open-gates-register.md#rule-vg-06) — dormant unless a cloud component becomes an AOT deliverable | Not scheduled; conditional |
| **[V-06](phase-1-official-verification.md#rule-v-06)** | Merchant-of-Record role | `../architecture/16-billing-and-commerce-architecture.md` `§1` | [VG-10](open-gates-register.md#rule-vg-10) — onboarding, approval and screening | [WP-42.10](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10) |
| **[V-07](phase-1-official-verification.md#rule-v-07)** | Payout relationship and settlement timing | `../architecture/16-billing-and-commerce-architecture.md` `§9` | [VG-11](open-gates-register.md#rule-vg-11) — eligibility and currency confirmation | [WP-42.10](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10) |
| **[V-08](phase-1-official-verification.md#rule-v-08)** | Regional payment route constraints | `../architecture/16-billing-and-commerce-architecture.md` `§11` | [VG-12](open-gates-register.md#rule-vg-12) — three sharpened regional gates | [WP-42.10](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10), conditional |
| **[V-09](phase-1-official-verification.md#rule-v-09)** | Mobile storefront commerce rules | `../architecture/11-mobile-architecture.md` `§9` | [VG-13](open-gates-register.md#rule-vg-13) — category fit and consumption-only by review | [WP-32.04](../planning/work-packages/32-mobile-release-and-store-gates.md#rule-wp-32.04) |

**Coverage: 9 of 9 findings enforced; 12 active gates scheduled, 2 dormant by design, 1 merged into F-026.**

---

## 3. Requirements → architecture → tests → work packages

| Requirement document | Primary architecture | Primary test families | Primary work packages |
|---|---|---|---|
| `00-product-scope-and-portfolio` | `00-architecture-overview` | [F-17](testing-and-verification-strategy.md#rule-f-17) | `00`, `01`, `02` |
| `01-normative-glossary-and-invariants` | All (vocabulary) | [F-01](testing-and-verification-strategy.md#rule-f-01), [F-17](testing-and-verification-strategy.md#rule-f-17) | `00`, `05` |
| `02-identity-account-and-workspace` | `08-security-architecture` | [F-02](testing-and-verification-strategy.md#rule-f-02), [F-03](testing-and-verification-strategy.md#rule-f-03), [F-11](testing-and-verification-strategy.md#rule-f-11) | `11`, `22`, `48` |
| `03-cloud-services-and-sync` | `07-sync-conflict-and-backup`; `20-cross-system-lifecycles`; `contracts/01`, `contracts/03`; `data-model/01` | [F-03](testing-and-verification-strategy.md#rule-f-03), [F-07](testing-and-verification-strategy.md#rule-f-07), [F-11](testing-and-verification-strategy.md#rule-f-11), [F-13](testing-and-verification-strategy.md#rule-f-13) | `21`, `24`, `25`, `46` |
| `04-commerce-entitlement-and-credits` | `16-billing-and-commerce-architecture` `§5.3`, `§7`; `20-cross-system-lifecycles` `§2`–`§4`; `data-model/01` `§8.1` | [F-02](testing-and-verification-strategy.md#rule-f-02), [F-03](testing-and-verification-strategy.md#rule-f-03), [F-06](testing-and-verification-strategy.md#rule-f-06) | `42`, `43`, `48` |
| `05-ai-and-agent-execution` | `09-ai-and-agent-runtime-architecture`; **`17-agent-harness`** (the Cloud loop); `16` `§7.3` (admission) | [F-02](testing-and-verification-strategy.md#rule-f-02), [F-11](testing-and-verification-strategy.md#rule-f-11), [F-13](testing-and-verification-strategy.md#rule-f-13) | 17, 26, 40, 41, 42, 43, 44, 52 |
| `06-knowledge-search-and-retrieval` | `09-ai-and-agent-runtime-architecture` `§5`; `17-agent-harness` `§4`; `data-model/03` | [F-03](testing-and-verification-strategy.md#rule-f-03), [F-11](testing-and-verification-strategy.md#rule-f-11) | `19`, `40` |
| `07-security-privacy-and-trust` | `08-security-architecture` | [F-02](testing-and-verification-strategy.md#rule-f-02), [F-11](testing-and-verification-strategy.md#rule-f-11), [F-17](testing-and-verification-strategy.md#rule-f-17) | `11`, `22`, `41`, `45` |
| `08-extensions-and-developer-platform` | `15-extension-platform-architecture` | [F-05](testing-and-verification-strategy.md#rule-f-05), [F-11](testing-and-verification-strategy.md#rule-f-11), [F-17](testing-and-verification-strategy.md#rule-f-17) | `41` |
| `09-shared-desktop-experience` | `04-desktop-application-architecture`; `18-editing-and-rich-content` `§8` (preview levels) | [F-09](testing-and-verification-strategy.md#rule-f-09), [F-10](testing-and-verification-strategy.md#rule-f-10), [F-15](testing-and-verification-strategy.md#rule-f-15) | `10` |
| `10-distribution-update-and-support` | `14-build-packaging-and-release`; `13-observability-and-operations`; **`22-deployment-and-release-execution`** | [F-16](testing-and-verification-strategy.md#rule-f-16), [F-11](testing-and-verification-strategy.md#rule-f-11) | `02`, `32`, `45`, `50` |
| `11-policy-and-configuration` | `16-billing-and-commerce-architecture` `§2.2`; `22-deployment-and-release-execution` `§3.1`; `data-model/01` `§8.2`; `05-cloud-architecture` `§12` | [F-02](testing-and-verification-strategy.md#rule-f-02), [F-06](testing-and-verification-strategy.md#rule-f-06), [F-11](testing-and-verification-strategy.md#rule-f-11) | `44`, `42` |
| `12-quality-and-compatibility-contract` | All (budgets and gates); `21-platform-and-dependency-matrix` `§2`; `22-deployment-and-release-execution` `§5` | Every family | `02`, `05`, `06`, and each product package |
| `13-data-formats-and-portability` | `06-data-persistence-and-formats`; `18-editing-and-rich-content` `§10`; `data-model/02` | [F-03](testing-and-verification-strategy.md#rule-f-03), [F-12](testing-and-verification-strategy.md#rule-f-12), [F-13](testing-and-verification-strategy.md#rule-f-13) | `07`, `19`, `35`, `39` |
| `products/arcchat` | `04`, `09`, **`17`**, `19` `§3` architecture; `contracts/02` `§4` | [F-02](testing-and-verification-strategy.md#rule-f-02), [F-05](testing-and-verification-strategy.md#rule-f-05), [F-11](testing-and-verification-strategy.md#rule-f-11) | 15, 17, 20, 25, 26, 52 |
| `products/arcnotes` | `04`, `06`, **`18`**, `19` `§4` architecture; `data-model/02` `§3` | [F-03](testing-and-verification-strategy.md#rule-f-03), [F-09](testing-and-verification-strategy.md#rule-f-09), [F-12](testing-and-verification-strategy.md#rule-f-12) | 18, 19, 25, 28; 27 and 29 are retired |
| `products/arcscope` | `12-native-interop-and-media` `§8`; **`23-simulator-and-interchange` `§1`**; `19` `§5`; `21` `§3`; `data-model/01` `§8.3`; `data-model/02` `§4` | [F-08](testing-and-verification-strategy.md#rule-f-08), [F-14](testing-and-verification-strategy.md#rule-f-14), [F-18](testing-and-verification-strategy.md#rule-f-18) | `33`, `34`, `35`, **`51`** |
| `products/arcslate` | `12-native-interop-and-media` `§7`; **`23-simulator-and-interchange` `§2`**; `19` `§6`; `21` `§3`; `data-model/02` `§5` | [F-08](testing-and-verification-strategy.md#rule-f-08), [F-15](testing-and-verification-strategy.md#rule-f-15), [F-18](testing-and-verification-strategy.md#rule-f-18) | `36`, `37`, `38`, `39` |
| `products/arcchat-mobile-and-web` | `11-mobile-architecture`; `10-web-architecture` | [F-04](testing-and-verification-strategy.md#rule-f-04), [F-06](testing-and-verification-strategy.md#rule-f-06), [F-16](testing-and-verification-strategy.md#rule-f-16) | `30`, `31`, `32`, `49` |
| `products/arcforges-web` | `10-web-architecture` | [F-09](testing-and-verification-strategy.md#rule-f-09), [F-10](testing-and-verification-strategy.md#rule-f-10), [F-15](testing-and-verification-strategy.md#rule-f-15) | `47`, `48`, `49` |
| `products/arcforges-cloud` | `05-cloud-architecture`; `13-observability-and-operations`; **`22-deployment-and-release-execution`**; `contracts/01`; `data-model/01` | [F-03](testing-and-verification-strategy.md#rule-f-03), [F-07](testing-and-verification-strategy.md#rule-f-07), [F-13](testing-and-verification-strategy.md#rule-f-13), [F-14](testing-and-verification-strategy.md#rule-f-14) | 21–26, 42–46, 51, 52 |

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
| `09-ai-and-agent-runtime-architecture` | 17 (client), 26, 40, 43, 52 (single Cloud runtime) |
| `10-web-architecture` | `47`, `48`, `49` |
| `11-mobile-architecture` | `30`, `31`, `32` |
| `12-native-interop-and-media` | `13`, `33`, `34`, `36`, `37`, `38` |
| `13-observability-and-operations` | `12`, `45` |
| `14-build-packaging-and-release` | `02`, `06`, `32`, `50` |
| `15-extension-platform-architecture` | `41` |
| `16-billing-and-commerce-architecture` | `42`, `43` |
| `17-agent-harness` | **`52`** (the Harness itself), `15`, `17`, `40`, `42`, `43` |
| `18-editing-and-rich-content` | 11, 18, 19, 25, 28 |
| `19-product-implementation-maps` | `01`, `05`, and each product package it maps |
| `20-cross-system-lifecycles` | `24`, `25`, `26`, `42`, `43`, `46`, `50` |
| `21-platform-and-dependency-matrix` | `06`, `13`, `33`, `37`, `50` |
| `22-deployment-and-release-execution` | `21`, `23`, `44`, `45`, `50` |
| `23-simulator-and-interchange` *(also the ArcSlate time model, `§3`)* | `33`, `36`, `37`, `38`, `39`, **`51`** |
| [24-content-and-extension-isolation](../architecture/24-content-and-extension-isolation.md) | 11.09, 18.04, 37.01, 41.00 |
| `contracts/00-operation-catalogue` | `03`, `04`, `09`, `23` |
| `contracts/01-public-api-operations` | `22`, `23`, `25`, `42` |
| `contracts/02-local-rpc-operations` | `08`, `09`, `14`, `17`, `18`, `20`, `33`, `36` |
| `contracts/03-realtime-and-bridge` | `24`, `26`, `31` |
| `data-model/00-data-model-overview` | `07`, `21`, `25` |
| `data-model/01-cloud-data-model` | `21`, `22`, `23`, `42` |
| `data-model/02-desktop-data-model` | `07`, `15`, `18`, `33`, `36` |
| `data-model/03-derived-stores` | `19`, `40` |

**Coverage: 33 of 33 architecture documents realised in at least one work package.**

> **Layer note.** Documents `00`–`24` state architecture: boundaries, ownership and rules. The `contracts/` and `data-model/` subdirectories state the concrete design those rules produce — the operations, signatures, events and schemas. Both are cited by work packages, because a rule without its concrete counterpart is not implementable.

---

## 5. Invariant enforcement

The catalogue in [`../requirements/01-normative-glossary-and-invariants.md`](../requirements/01-normative-glossary-and-invariants.md) contains **429 invariants** across twelve sections — 421 at the original baseline plus 8 added by P2-006. The full item-level mapping is [`invariant-coverage.md`](invariant-coverage.md) `§7`.

> **Corrected count.** Earlier documents said "approximately 490". That read the highest identifier as a count. The catalogue holds **429** rows; identifiers reach [I-498](../requirements/01-normative-glossary-and-invariants.md#rule-i-498) because each section reserves headroom, evidenced in `§2` of the coverage document. **421 is the superseded pre-P2-006 figure.**

| Mechanism | Applies to | Invariants |
|---|---|---|
| **Type distinction** | Identity, reference, capability and version-axis distinctions | 55 |
| **Repository policy test** | Boundary, naming, reference-direction and platform rules | 39 |
| **Unit test** | Behavioural distinctions within one component | 202 |
| **Integration test** | Distinctions observable only across a process, device or system boundary | 125 |

### 5.1 Three obligations, three states

| Obligation | Content | Gate | State |
|---|---|---|---|
| **A — design completeness** | Every corpus statement preserved or explicitly dispositioned | Part of [PG-06](open-gates-register.md#rule-pg-06) | **Complete** — 484 of 484 accounted for; four invariants added; one superseded statement correctly excluded |
| **B — design traceability** | Architecture home, mechanism, planned verification, owning gate, per invariant | [PG-06](open-gates-register.md#rule-pg-06) | **Complete** — **429 of 429** mapped; **[PG-06](open-gates-register.md#rule-pg-06) closed 2026-09-05 and re-verified after [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) added [I-491](../requirements/01-normative-glossary-and-invariants.md#rule-i-491)–[I-498](../requirements/01-normative-glossary-and-invariants.md#rule-i-498)** |
| **C — implementation evidence** | An implemented check with a passing result | [PG-11](open-gates-register.md#rule-pg-11) | **Open**, distributed across owning packages |

| # | Rule |
|---|---|
| IE-01 | **[PG-06](open-gates-register.md#rule-pg-06) and [PG-11](open-gates-register.md#rule-pg-11) are different gates with different evidence.** [PG-06](open-gates-register.md#rule-pg-06) closing has no effect on [PG-11](open-gates-register.md#rule-pg-11). |
| IE-02 | **An owned open finding never closes either.** [WP-05.05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.05) produces an accounting report; a faithful report of unimplemented checks is a complete report and a failing [PG-11](open-gates-register.md#rule-pg-11). |
| IE-03 | **A planned verification is not evidence that an invariant holds.** It is evidence that the invariant is verifiable and that someone owns proving it. |

---

## 6. Gate → work package

Every gate in [`open-gates-register.md`](open-gates-register.md) is scheduled.

| Gate | Scheduled in | Blocking |
|---|---|---|
| **[F-013](open-gates-register.md#rule-f-013)** | **Closed by design evidence 2026-09-05** — the five matrices. Registered in `00.04`; drift maintenance in `15.07`, `18.08`, `33.07`, `36.07` | [P-02](release-gates.md#rule-p-02) per product |
| **[F-023](open-gates-register.md#rule-f-023)** | `32.02` | [L-50](release-gates.md#rule-l-50), any mobile artifact |
| **[F-026](open-gates-register.md#rule-f-026)** | `03.02`, `06.02` | [R-03](release-gates.md#rule-r-03) on consuming targets |
| **[VG-01](open-gates-register.md#rule-vg-01)** | `43.04` | First EU-available release |
| **[VG-02](open-gates-register.md#rule-vg-02)** | `41.07` | Finalising the extension work package |
| **[VG-03](open-gates-register.md#rule-vg-03)** | `10.08` | Third-party control adoption |
| **[VG-04](open-gates-register.md#rule-vg-04)** | `03.04`, `06.01` | First AOT desktop deliverable |
| **[VG-06](open-gates-register.md#rule-vg-06)** | Not scheduled — dormant | Conditional on a decision not taken |
| **[VG-07](open-gates-register.md#rule-vg-07)** | `32.01` | First Android production build |
| **[VG-08](open-gates-register.md#rule-vg-08)** | `02.05`, recurring | Every framework major upgrade |
| **[VG-09](open-gates-register.md#rule-vg-09)** | Deferred with the iOS build | iOS release |
| **[VG-10](open-gates-register.md#rule-vg-10)**, **[VG-11](open-gates-register.md#rule-vg-11)** | `42.10` | Commercial go-live |
| **[VG-12](open-gates-register.md#rule-vg-12)** | `42.10`, conditional | Regional enablement |
| **[VG-13](open-gates-register.md#rule-vg-13)** | `32.04` | First store submission |
| **[PG-01](open-gates-register.md#rule-pg-01)** | **Closed by design evidence 2026-09-05.** Registered in `00.04`; drift maintenance per product | Product first release |
| **[PG-02](open-gates-register.md#rule-pg-02)** | **Closed by design evidence 2026-09-05** — the item-level inventory. Drift validation in `01.00`; execution in `01.01`–`01.05` | All restructuring |
| **[PG-03](open-gates-register.md#rule-pg-03)** | `13.04`, `33`, `37.00`; shim dispositions already assigned, two fenced pending `35.04` and `39.05` | Native dependency use |
| **[PG-04](open-gates-register.md#rule-pg-04)** | `45.02` | Paid cloud go-live |
| **[PG-05](open-gates-register.md#rule-pg-05)** | `12.02` | [R-16](release-gates.md#rule-r-16) |
| **[PG-06](open-gates-register.md#rule-pg-06)** | **Closed by design evidence 2026-09-05** — [`invariant-coverage.md`](invariant-coverage.md) `§7` | Finalising the design baseline |
| **[PG-11](open-gates-register.md#rule-pg-11)** | Distributed across the owning packages in that mapping; accounting reported by `05.05` | Each owning package's gate; [P-03](release-gates.md#rule-p-03) per product |
| **[PG-07](open-gates-register.md#rule-pg-07)** | 19.04, 35.04, 39.05 | Public import-format claims. Early export UI fixtures in 15.06/19.05 do not prove the real Cloud download; that gate is 25.08 |
| **[PG-08](open-gates-register.md#rule-pg-08)** | 13.04 establishes the inventory; 33/34 and 37/38 consume and maintain it | [C-04](release-gates.md#rule-c-04) |
| **[PG-09](open-gates-register.md#rule-pg-09)** | `41` | Third-party extension enablement |
| **[PG-10](open-gates-register.md#rule-pg-10)** | `42.10`, `43.06` | [L-28](release-gates.md#rule-l-28), [L-29](release-gates.md#rule-l-29) |
| **[PG-12](open-gates-register.md#rule-pg-12)** | 11.09, 18.04 | [ArcNotes PDF requirement](../requirements/products/arcnotes.md#rule-at-05); first PDF release claim |
| **[PG-13](open-gates-register.md#rule-pg-13)** | `43.07`, `42.11` | Paid AI go-live; [PG-10](open-gates-register.md#rule-pg-10) |
| **[PG-14b](open-gates-register.md#rule-pg-14b)** | `51.00`–`51.05` | Any ArcScope claim that Cloud simulation is delivered. **Not `34`**, whose repeatable source is file/replay from `33` |
| **[PG-15](open-gates-register.md#rule-pg-15)** | `39.05` | ArcSlate release |
| **[PG-16](open-gates-register.md#rule-pg-16)** | `44.01`, `42.11` | Paid production go-live |
| **[PG-17](open-gates-register.md#rule-pg-17)** | 21.05, 25.02, 25.07 | Sync publisher ordering, fairness and bootstrap convergence |
| **[PG-18](open-gates-register.md#rule-pg-18)** | `52.02`, `52.04` | Paid AI go-live; any external-effect capability |
| **[PG-19](open-gates-register.md#rule-pg-19)** | `21.03`, `50.04` | Any schema evolution in production |
| **[PG-20](open-gates-register.md#rule-pg-20)** | 36.01, 37.04, 39.05 | Source conform, per-track mixing and OTIO boundaries |
| **[PG-21](open-gates-register.md#rule-pg-21)** | Current corpus closed by [repair verification](design-repair-verification.md); continuing drift check in 00.01 | Every later normative edit re-runs the complete citation check |
| **[PG-22](open-gates-register.md#rule-pg-22)** | 11.09, 18.04, 37.01, 41.00 | Packaged OS containment and extension permissions on each supported RID |
| **[VG-05](open-gates-register.md#rule-vg-05)** | **Merged into [F-026](open-gates-register.md#rule-f-026)** and recorded there; no separate schedule | — |

**Coverage: 38 register entries** — 3 deferred Phase 1, 13 verification entries and 22 Phase 2 entries. Five are closed on design evidence; 32 remain open for implementation, including two dormant entries; one verification entry is merged into its deferred gate. There are zero unresolved owner determinations. Every entry has an owner, trigger and implementation or evidence location in the [gate register](open-gates-register.md).

> **This count is checked, not asserted.** [SV-05](testing-and-verification-strategy.md#rule-sv-05) of the verification strategy requires every gate to be scheduled in a named package; before 2026-09-08 this table stopped at [PG-10](open-gates-register.md#rule-pg-10) while the register held [PG-21](open-gates-register.md#rule-pg-21), so ten gates — including every gate created by the [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) reconciliation and the two review passes — were unscheduled here while the coverage line claimed completeness.

---

## 7. What this matrix does not claim

| # | Statement |
|---|---|
| NC-01 | **No gate is closed by this document.** Five gates are closed by the design-stage artifacts they name; this matrix records that, it does not effect it. |
| NC-02 | **Design traceability is complete; implementation enforcement is not.** [PG-06](open-gates-register.md#rule-pg-06) is closed on the mapping; [PG-11](open-gates-register.md#rule-pg-11) requires implemented, passing checks and is open. |
| NC-03 | **All five Reference Coverage Matrices exist**, with 145 item-level rows, and **no unresolved determination remains** — [OC-01](open-gates-register.md#rule-oc-01) was closed by user decision ([P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005)). |
| NC-04 | **The item-level code inventory exists** — 166 of 166 projects, measured. Its dispositions are **not executed**; that is [WP-01](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01)'s work. |
| NC-05 | **No test in this matrix has been run.** This is a specification repository; the test families and gates are defined here and executed in the implementation repository. |
| NC-06 | **A resolving citation is not a designed mechanism.** This matrix records that a requirement has an architecture home; whether that home specifies a mechanism rather than restating the requirement is checked by [`end-to-end-workflow-verification.md`](end-to-end-workflow-verification.md), with the complete fourteen-group repair recorded in [the closure review](phase-2-design-closure-review.md). |
| NC-07 | **Row counts prove nothing about completeness.** Every architecture document being realised in a work package says every document is claimed by someone, not that every subject is designed. |
| NC-08 | **This matrix was recomputed on 2026-09-06 against the revised requirements**, not carried forward. [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)'s downstream reconciliation statement is explicit that prior completion claims do not demonstrate coverage of the amended scope, so every count here is a fresh derivation. |
| NC-09 | **A retired package still appears.** `27` and `29` are listed as retired rather than deleted, so a reader following an older citation finds the retirement record instead of a broken reference. |
| NC-10 | **This matrix was rechecked on 2026-09-07** after the design-defect repair pass. [WP-52](../planning/work-packages/52-cloud-harness.md#rule-wp-52) was created at its real dependency position, and the sub-steps relocated into it ([WP-17.08](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.08), [WP-17.09](../planning/work-packages/17-arcchat-independent-core.md#rule-wp-17.09), [WP-20.03](../planning/work-packages/20-first-cross-product-workflow.md#rule-wp-20.03)) are retired at their old identifiers rather than left as dangling citations. |

---

## 8. Maintenance

| # | Rule |
|---|---|
| MT-01 | **This matrix is updated whenever a document, gate or work package is added, removed or renamed.** |
| MT-02 | **[WP-05.06](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.06) asserts its integrity**: every identifier cited here must exist, and every architecture document, requirement document and gate must appear. |
| MT-03 | **A decision added in Phase 2** ([`../decisions/`](../decisions/README.md)) is added to `§1` with its enforcement mechanism. |
| MT-04 | **A gate discovered during implementation** is added to the register and to `§6` with its scheduling. |
