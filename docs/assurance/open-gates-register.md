# Open Gates Register

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: **D-003** (verification scope and the first-consumption rule), **D-016** (deferred-decision ownership)
> Companions: [`phase-1-official-verification.md`](phase-1-official-verification.md), [`phase-1-input-review-ledger.md`](phase-1-input-review-ledger.md), [`release-gates.md`](release-gates.md), [`../planning/README.md`](../planning/README.md)

Every gate that Phase 1 deferred, every gate the official verification record created, and every gate Phase 2 adds — in one register, each with an owner, a trigger, what it blocks, and the work package that must satisfy it.

**No gate in this register is closed by Phase 2.** Phase 2's obligation is to schedule each one against a specific work package so that none can be forgotten. That scheduling is complete here.

---

## 1. Register conventions

| Field | Meaning |
|---|---|
| **State** | `OPEN` — not yet triggered · `TRIGGERED` — its trigger has fired and it is now blocking · `CLOSED` — satisfied with recorded evidence |
| **Owner** | The accountable role, as recorded in Phase 1 or assigned here |
| **Trigger** | The event that makes the gate due; until then it is not overdue |
| **Blocks** | What cannot proceed while the gate is open after its trigger |
| **Scheduled in** | The work package that must satisfy it ([`../planning/work-packages/README.md`](../planning/work-packages/README.md)) |

| # | Rule |
|---|---|
| OG-01 | **A gate is closed only by recorded evidence**, never by assertion. |
| OG-02 | **A gate whose trigger has fired and which is not closed blocks the dependent work** — it does not become a warning. |
| OG-03 | **A gate may not be silently re-scoped.** Changing a gate requires a decision record. |
| OG-04 | **A new gate discovered during implementation is added here**, with the same fields, rather than living only in the document that discovered it. |

---

## 2. Deferred gates carried from Phase 1

| Gate | Subject | Owner | Trigger | Blocks | Scheduled in | State |
|---|---|---|---|---|---|---|
| **F-013** | Reference-repository licences and file-level SPDX evidence (**D-013**) | Licensing and Provenance Owner | The first step of a product's Reference Coverage Matrix and licence audit, before substantive reference source is used for planning or implementation | That product's implementation planning; `P-02` in the release gates | The per-product reference-audit work packages | `OPEN` |
| **F-023** | ArcChat Mobile provenance and complete direct and transitive dependency closure (**D-004**) | Release Engineering Owner **and** Licensing and Provenance Owner; Product Owner approves | Before the first store, test-flight, store-listing or sideloadable mobile artifact is produced | Any mobile artifact; `L-50` | The mobile release work package | `OPEN` |
| **F-026** | Typed HTTP client version pin, generated-only entry point, reflection-package prohibition, generator diagnostic treated as build-breaking | Owning platform work-package owner; Architecture Owner approves | Before accepting the typed HTTP client into an AOT deliverable | Any AOT deliverable consuming it; `R-03` | The platform skeleton and AOT proof work package | `OPEN` |

---

## 3. Gates created by the official verification record

| Gate | Source | Owner | Trigger | Blocks | Scheduled in | State |
|---|---|---|---|---|---|---|
| **VG-01** | **V-01** — confirm whether ArcForges adheres to the transparency code of practice for AI-generated content or relies on equivalently adequate alternative means, and record the marking mechanism per artifact type | Security and Privacy Owner, with Product Owner approval | First EU market availability | First EU-available release | The AI transparency and compliance work package | `OPEN` |
| **VG-02** | **V-02** — pin the exact MCP SDK version and record an explicit mapping between MCP extension concepts and the ArcForges execution vocabulary defined by the normative glossary (**D-018**) | Architecture Owner | Start of the MCP and extension work package | Finalising that work package | The extension and integration platform work package | `OPEN` |
| **VG-03** | **V-05a** — a real AOT publish proof of the desktop shell plus every third-party control actually used, with zero trim or AOT diagnostics | Owning platform work-package owner | Before accepting any third-party control into an AOT deliverable | Adoption of that control | The desktop shell and design system work package | `OPEN` |
| **VG-04** | **V-05b** — an AOT publish proof of the desktop host with the real local-RPC contract set, plus a repository-policy test asserting every RPC contract interface carries its generated-shape attribute | Architecture Owner | Before the first AOT desktop deliverable | That deliverable | The platform skeleton and AOT proof work package | `OPEN` |
| **VG-05** | **V-05c** — see **F-026**; recorded there | — | — | — | — | Merged into **F-026** |
| **VG-06** | **V-05e** — if any Cloud component is ever moved into an AOT deliverable, its full dependency closure requires an AOT publish proof at that time | Architecture Owner | Any decision to AOT-publish a Cloud component | That decision's implementation | Not scheduled — conditional on a decision that has not been taken (**D-008** makes Cloud JIT) | `OPEN — dormant` |
| **VG-07** | **V-04a** — before the first Android production build, confirm the runtime is Mono AOT and that the runtime selection is explicit in the project file rather than inherited from a default | Release Engineering Owner with Architecture Owner | First Android production build | That build; `L-53` | The mobile platform work package | `OPEN` |
| **VG-08** | **V-04b** — before any framework major-version upgrade, re-verify the Android runtime posture and re-run the mobile AOT and trim proof | Release Engineering Owner with Architecture Owner | Any framework major-version upgrade | That upgrade | The dependency and framework upgrade work package | `OPEN — recurring` |
| **VG-09** | **V-04c** — iOS release runtime re-verified against the then-current supported baseline before build activation | Release Engineering Owner with Architecture Owner | iOS build activation | iOS release | Deferred with the iOS build itself (**D-008**) | `OPEN — dormant` |
| **VG-10** | **V-06** — supplier onboarding and account approval; sanctions and export screening for the intended market set | Commercial Operations Owner | Before the first live transaction | Commercial go-live; `L-20`, `L-21` | The commerce go-live work package | `OPEN` |
| **VG-11** | **V-07** — payout account eligibility and receiving-currency confirmation for the chosen supplier jurisdiction | Commercial Operations Owner | First authoritative pricing specification, and again before launch | Commercial go-live; `L-22` | The commerce go-live work package | `OPEN` |
| **VG-12** | **V-08** — the additional regional gates: the separate payment-method application with its stated criteria; a local-currency product and tax configuration existing before approval can be sought; and a refund and dispute model validated against the absence of chargeback support | Commercial Operations Owner, with Product Owner approval on the pricing catalogue | Before enabling mainland-China sales | That market's enablement; `L-40` | The regional enablement work package | `OPEN — conditional` |
| **VG-13** | **V-09** — before the first store submission, confirm category fit with review and confirm that no build path can display a purchase call to action or accept a licence key; before the first alternative-store submission, confirm consumption-only conformance | Release Engineering Owner with Product Owner approval | First mobile store submission | That submission; `L-51`, `L-52` | The mobile release work package | `OPEN` |

---

## 4. Gates created by Phase 2

These are new obligations that follow from Phase 2 architecture rather than from Phase 1. Each is a scheduling obligation, not a reopened decision.

| Gate | Subject | Owner | Trigger | Blocks | Scheduled in | State |
|---|---|---|---|---|---|---|
| **PG-01** | The per-product **Reference Coverage Matrix** exists with a disposition for every item (**D-012**) | Product Owner with Architecture Owner | Start of that product's implementation planning | `P-01`; that product's first release | The per-product reference-audit work packages | `OPEN` |
| **PG-02** | The **implementation-state reconciliation inventory** exists before repository restructuring begins | Architecture Owner | Before the first restructuring change | All restructuring work | The repository reconciliation work package | `OPEN` |
| **PG-03** | The **native dependency licence review** per product, against that product's licence boundary (`LD-07` in the native architecture) | Licensing and Provenance Owner | First native dependency accepted into a product | That dependency's use | The native interoperability work package | `OPEN` |
| **PG-04** | **Runbook rehearsal evidence**: every required runbook executed at least once, with a dated record (`RB-04` in the observability architecture) | Operations Owner | Before paid cloud go-live | `L-12` | The operations readiness work package | `OPEN` |
| **PG-05** | **Redaction proof**: marker values injected as headers, tokens, prompts and document content never appear in exported telemetry (`TV-01` there) | Operations Owner | First telemetry export to an external backend | `R-16` | The observability work package | `OPEN` |
| **PG-06** | **Invariant coverage**: every glossary invariant maps to at least one architecture rule, one test and one work-package completion gate (**D-018**) | Architecture Owner | Continuous from the first implementation work package | Traceability completeness | The glossary enforcement work package | `OPEN` |
| **PG-07** | **Format fixture completeness**: every claimed import format version has a fixture (`ME-03` in the provenance document) | Product Owner per product | First public import claim for that product | That claim | The per-product import and export work packages | `OPEN` |
| **PG-08** | **Hardware lab inventory**: a maintained device, firmware and driver inventory exists before ArcScope or ArcSlate hardware results are accepted (`TE-03` in the testing strategy) | Quality Owner | First hardware-lab test run | `C-04` | The ArcScope and ArcSlate verification work packages | `OPEN` |
| **PG-09** | **Extension protocol conformance**: the reference-extension suite passes before the extension platform is opened to third parties | Architecture Owner | Before third-party extension enablement | `L-60` | The extension platform work package | `OPEN` |
| **PG-10** | **Provider test-environment coverage**: every provider integration is exercised against the provider's test environment and frozen as recorded contract fixtures (`TE-04` there) | Architecture Owner | First provider integration | `L-28`, `L-29` | The commerce and AI provider work packages | `OPEN` |

---

## 5. What is deliberately not verified

**D-003** established a verification scope and a first-consumption rule. This register preserves it.

| Category | Position |
|---|---|
| Prices, fees, quotas, rates and commercial figures | **Deliberately not verified.** Deferred under **D-003**'s first-consumption rule with a named owner and trigger; every figure is versioned commercial policy under **D-020** |
| Third-party pricing pages and plan tiers | Not verified; verified at first consumption by the owning work package |
| Vendor feature roadmaps | Not verified; only current, documented behaviour is relied upon |
| Reference-repository internals beyond behavioural evidence | Not verified; governed by **D-012** and **D-013** |

| # | Rule |
|---|---|
| NV-01 | **A figure quoted from the input corpus is recorded as a corpus proposal, never as a commitment** (**D-020**). |
| NV-02 | **Consuming an unverified external fact triggers its verification at that moment** (**D-003**), and the verification result is recorded in the assurance layer. |

---

## 6. Register summary

| State | Count |
|---|---|
| Deferred gates carried from Phase 1 | 3 |
| Gates created by the verification record | 12 active + 1 merged |
| Gates created by Phase 2 | 10 |
| Closed in Phase 2 | **0** — Phase 2 schedules gates; it does not close them |

---

## 7. Traceability

| Source | Consumed as |
|---|---|
| [`phase-1-official-verification.md`](phase-1-official-verification.md) | Every "Required gate" statement, transcribed with owner, trigger and scheduling |
| [`phase-1-input-review-ledger.md`](phase-1-input-review-ledger.md) | The deferred-gate register carried forward |
| **D-003** | Verification scope and the first-consumption rule |
| **D-016** | Deferred-decision ownership |
| **D-020** | Commercial figures as versioned policy, not verified constants |
