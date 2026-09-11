# Commercial Figure Status

> Status: **Authoritative** — Phase 2 design-stage evidence
> Layer: Assurance
> Governing authority: **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** (AI and payment economic model — every figure is versioned commercial policy), **[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)** (verification scope and the first-consumption rule)
> Companions: [`../requirements/04-commerce-entitlement-and-credits.md`](../requirements/04-commerce-entitlement-and-credits.md), [`open-gates-register.md`](open-gates-register.md)

This document answers one question with evidence: **has any commercial figure been consumed as an authoritative specification without satisfying [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)'s verification and approval requirement?**

**Current status:** synthetic acceptance rates exist, and the seven recorded commercial-policy allowances remain proposals. Neither is an approved production tariff. This record distinguishes historical inventory, test arithmetic and live configuration; it does not claim a new market/pricing approval.

---

## 1. What [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020) requires

| # | Obligation |
|---|---|
| CF-01 | Every commercial figure is **versioned commercial policy**, never a frozen commitment and never a compiled constant. |
| <a id="rule-cf-02"></a>CF-02 | An illustrative commercial figure in the current design is a **proposal**. It requires Commercial Operations Owner specification and Product Owner approval **at first consumption and again before launch**. |
| CF-03 | **Financial history is immutable**; a price change never alters a settled charge. |
| CF-04 | Money and credit arithmetic is **fixed-precision**. |
| CF-05 | Exhaustion is a **hard stop at zero**; no post-paid overdraft. |

---

## 2. Historical inventory check

| Step | Method | Result |
|---|---|---|
| 1 | Scanned `docs/requirements/`, `docs/architecture/` and `docs/planning/` for currency amounts, storage quantities and percentages | 21 numeric occurrences found |
| 2 | Classified each by kind | See `§3` |
| 3 | For every commercial-policy figure, checked that it carries the proposal label and the approval requirement | See `§4` |
| 4 | Checked whether any figure is stated as a price, a rate or a commitment | See `§5` |

---

## 3. Classification of the historical 21 occurrences

| Kind | Count | Examples | [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020) applicable? |
|---|---|---|---|
| **Commercial policy — proposals** | 7 | Included workspace storage, version-history window, deleted-item recovery window, payment grace period, post-entitlement retention, backup retention, storage add-on tiers | **Yes** — all labelled |
| **Illustrative scenario quantities** | 6 | "a user with 2,000 local notes and 300 GB of local media"; "a 40 GB upload"; "a 200 GB external library"; "an 80 GB local capture" | No — these illustrate a behaviour requirement, not an allowance |
| **Test fixture sizes** | 1 | "1 KB · 100 MB · 20 GB" in an upload test matrix | No |
| **Quality budgets and thresholds** | 5 | ~10 % regression gate; memory ceilings; reference-hardware memory | No — engineering budgets, governed by the quality contract |
| **Progress and availability illustrations** | 2 | "80 % to 32 %" progress example; "99.9 % monthly availability" internal objective | No — the availability figure is an explicitly internal objective, and [SL-02](../architecture/13-observability-and-operations.md#rule-sl-02) states **SLO ≠ external SLA** |

---

### 3.1 Current synthetic accounting fixtures

The historical 21-occurrence inventory above predates the metering fixture and is not a current whole-corpus numeric count. [Commerce §8.6](../requirements/04-commerce-entitlement-and-credits.md#86-configuration-and-acceptance) defines six synthetic rates: supplier USD 2 / USD 0.20 / USD 8 per million uncached-input/cached-input/output tokens, and independent retail 4000 / 400 / 16000 credits per million. For 800 uncached + 200 cached + 100 output tokens, supplier cost is USD 0.00244 and customer consumption is 4.88 credits = 4,880,000 microcredits; a 6-credit hold releases 1.12. These are exact test inputs/outputs, not provider prices, launch offers or compiled production defaults. One credit =1,000,000 microcredits is the accounting unit definition, not a retail exchange rate.

The [BG-01](../requirements/05-ai-and-agent-execution.md#rule-bg-01) 30,000-credit workspace balance is an illustrative example separating available balance from Task spending authorization, not included subscription capacity. Real supplier/retail tariffs, burst/refill parameters and service policies remain independently versioned deployment configuration with required approval/activation. Missing required live rates fail closed; synthetic fixtures cannot populate a production fallback. Changing a fixture does not rewrite historical charges.

## 4. The seven commercial-policy figures

All seven appear in one place — [`../requirements/03-cloud-services-and-sync.md`](../requirements/03-cloud-services-and-sync.md) `§1` — under a heading that states the position before the table is read:

> *"Every numeric allowance below is **versioned commercial policy under [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)**, not a frozen figure. Each requires Commercial Operations Owner specification and Product Owner approval at first consumption and again before launch. The illustrative defaults in this table are *proposals* so that design work has a concrete shape; nothing here is a commitment."*

| Parameter | Recorded value | Column value | Conforms to [CF-02](#rule-cf-02)? |
|---|---|---|---|
| Included workspace shared storage | 50 GB | *Proposal; requires approval* | Yes |
| Version history window | 30 days | *Proposal; requires approval* | Yes |
| Deleted-item recovery window | 30 days | *Proposal; requires approval* | Yes |
| Payment grace period | 7 days | *Proposal; requires approval* | Yes |
| Post-entitlement cloud retention | 30 days | *Proposal; requires approval* | Yes |
| Infrastructure backup retention | ≈ 35 days | *Proposal; requires approval* | Yes |
| Storage add-on tiers | +100 GB / +500 GB / +1 TB | *Proposal; requires approval* | Yes |

**Two adjacent statements are structural, not policy, and are correctly marked binding**: storage is workspace-shared rather than per-product, and *"unlimited"* is never offered for storage or AI.

---

## 5. Prices, rates and tariffs

| Check | Result |
|---|---|
| Is any subscription price stated anywhere in the authoritative layers? | **No.** [`04-commerce-entitlement-and-credits.md`](../requirements/04-commerce-entitlement-and-credits.md) `§3` defines the price *model* — `Offer → PriceVersion → RegionalPrice` — and states no amount |
| Is any AI tariff or credit ratio stated? | **Yes, as synthetic acceptance data and the accounting unit definition**, listed in §3.1; no production tariff is approved by those examples |
| Is a synthetic rate a production constant? | **No.** Production configuration is versioned and approved; [WP-42.01](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.01) verifies no commercial rate is compiled into the product. A planned scan is not evidence that product code already passes |
| Does any document present a proposal as a commitment? | **No** — every one of the seven carries the *Proposal; requires approval* status in its own row |

---

## 6. Conclusion

| # | Statement |
|---|---|
| CN-01 | The seven recorded allowances remain proposals; the six metering rates and budget scenario are explicitly synthetic/illustrative. This record establishes their design status, not runtime or commercial approval. |
| CN-02 | Price/rate numbers do occur in authoritative documents as test data. Their arithmetic is normative for the fixture; their numeric prices are not production defaults or a launch offer. |
| CN-03 | First consumption as real commercial policy still requires the designated specification/approval under [D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020); synthetic testing does not satisfy or waive it. |
| CN-04 | **No figure was invented or frozen during this repair** to make the documents appear complete. |
| CN-05 | The approval obligation is carried as [VG-10](open-gates-register.md#rule-vg-10) and [VG-11](open-gates-register.md#rule-vg-11) in [`open-gates-register.md`](open-gates-register.md), and as gates [L-20](release-gates.md#rule-l-20)–[L-31](release-gates.md#rule-l-31) in [`release-gates.md`](release-gates.md). Those are legitimate future obligations whose trigger — first live transaction, and the first authoritative pricing specification — has not fired. |

---

## 7. Maintenance

| # | Rule |
|---|---|
| MT-01 | **A figure moving from proposal to specification fires [CF-02](#rule-cf-02).** It must gain Commercial Operations Owner specification and Product Owner approval at that moment, not at launch. |
| MT-02 | **A new numeric occurrence is classified before it is added.** If it is commercial policy, it enters `§4` with the proposal status. |
| MT-03 | Recheck the affected classification when allowance, tariff/capacity, budget or worked-fixture sections change; retain dated historical inventories without presenting them as current counts. |
