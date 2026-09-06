# Commercial Figure Status

> Status: **Authoritative** — Phase 2 design-stage evidence
> Layer: Assurance
> Governing authority: **D-020** (AI and payment economic model — every figure is versioned commercial policy), **D-003** (verification scope and the first-consumption rule)
> Companions: [`../requirements/04-commerce-entitlement-and-credits.md`](../requirements/04-commerce-entitlement-and-credits.md), [`open-gates-register.md`](open-gates-register.md)

This document answers one question with evidence: **has any commercial figure been consumed as an authoritative specification without satisfying D-020's verification and approval requirement?**

**Answer: no.** The check and its basis are below.

---

## 1. What D-020 requires

| # | Obligation |
|---|---|
| CF-01 | Every commercial figure is **versioned commercial policy**, never a frozen commitment and never a compiled constant. |
| CF-02 | A corpus-proposed figure is a **proposal**. It requires Commercial Operations Owner specification and Product Owner approval **at first consumption and again before launch**. |
| CF-03 | **Financial history is immutable**; a price change never alters a settled charge. |
| CF-04 | Money and credit arithmetic is **fixed-precision**. |
| CF-05 | Exhaustion is a **hard stop at zero**; no post-paid overdraft. |

---

## 2. The check performed

| Step | Method | Result |
|---|---|---|
| 1 | Scanned `docs/requirements/`, `docs/architecture/` and `docs/planning/` for currency amounts, storage quantities and percentages | 21 numeric occurrences found |
| 2 | Classified each by kind | See `§3` |
| 3 | For every commercial-policy figure, checked that it carries the proposal label and the approval requirement | See `§4` |
| 4 | Checked whether any figure is stated as a price, a rate or a commitment | See `§5` |

---

## 3. Classification of every numeric occurrence

| Kind | Count | Examples | D-020 applicable? |
|---|---|---|---|
| **Commercial policy — proposals** | 7 | Included workspace storage, version-history window, deleted-item recovery window, payment grace period, post-entitlement retention, backup retention, storage add-on tiers | **Yes** — all labelled |
| **Illustrative scenario quantities** | 6 | "a user with 2,000 local notes and 300 GB of local media"; "a 40 GB upload"; "a 200 GB external library"; "an 80 GB local capture" | No — these illustrate a behaviour requirement, not an allowance |
| **Test fixture sizes** | 1 | "1 KB · 100 MB · 20 GB" in an upload test matrix | No |
| **Quality budgets and thresholds** | 5 | ~10 % regression gate; memory ceilings; reference-hardware memory | No — engineering budgets, governed by the quality contract |
| **Progress and availability illustrations** | 2 | "80 % to 32 %" progress example; "99.9 % monthly availability" internal objective | No — the availability figure is an explicitly internal objective, and `SL-02` states **SLO ≠ external SLA** |

---

## 4. The seven commercial-policy figures

All seven appear in one place — [`../requirements/03-cloud-services-and-sync.md`](../requirements/03-cloud-services-and-sync.md) `§1` — under a heading that states the position before the table is read:

> *"Every numeric allowance below is **versioned commercial policy under D-020**, not a frozen figure. Each requires Commercial Operations Owner specification and Product Owner approval at first consumption and again before launch. The corpus-proposed defaults are recorded as *proposals* so that design work has a concrete shape; nothing here is a commitment."*

| Parameter | Recorded value | Column value | Conforms to `CF-02`? |
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
| Is any AI tariff or credit ratio stated? | **No.** The credit model defines lot classes, consumption order and reserve-then-settle; it states no rate |
| Is any figure compiled into a specification as a constant? | **No.** `WP-42.01`'s completion gate is a scan asserting no commercial constant is compiled into code, and `BR-02` of that package forbids it |
| Does any document present a proposal as a commitment? | **No** — every one of the seven carries the *Proposal; requires approval* status in its own row |

---

## 6. Conclusion

| # | Statement |
|---|---|
| CN-01 | **No commercial figure has been consumed as an authoritative specification.** All seven policy figures remain proposals with an explicit approval requirement. |
| CN-02 | **No price, rate or tariff exists in the authoritative layers at all.** The models exist; the numbers do not. |
| CN-03 | **D-020's verification and approval requirement is therefore not yet triggered** for any figure, consistent with **D-003**'s first-consumption rule. |
| CN-04 | **No figure was invented or frozen during this repair** to make the documents appear complete. |
| CN-05 | The approval obligation is carried as `VG-10` and `VG-11` in [`open-gates-register.md`](open-gates-register.md), and as gates `L-20`–`L-31` in [`release-gates.md`](release-gates.md). Those are legitimate future obligations whose trigger — first live transaction, and the first authoritative pricing specification — has not fired. |

---

## 7. Maintenance

| # | Rule |
|---|---|
| MT-01 | **A figure moving from proposal to specification fires `CF-02`.** It must gain Commercial Operations Owner specification and Product Owner approval at that moment, not at launch. |
| MT-02 | **A new numeric occurrence is classified before it is added.** If it is commercial policy, it enters `§4` with the proposal status. |
| MT-03 | This check is re-run whenever `03-cloud-services-and-sync.md` `§1` or `04-commerce-entitlement-and-credits.md` `§3` changes. |
