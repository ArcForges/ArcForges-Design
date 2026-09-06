# Open Gates Register

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: **D-003** (verification scope and the first-consumption rule), **D-016** (deferred-decision ownership)
> Companions: [`phase-1-official-verification.md`](phase-1-official-verification.md), [`phase-1-input-review-ledger.md`](phase-1-input-review-ledger.md), [`release-gates.md`](release-gates.md), [`../planning/README.md`](../planning/README.md)

Every gate that Phase 1 deferred, every gate the official verification record created, and every gate Phase 2 adds — in one register, each with an owner, a trigger, what it blocks, and the work package that must satisfy it.

Gates fall into two classes, and the distinction is load-bearing:

| Class | Obligation | Can Phase 2 close it? |
|---|---|---|
| **Design-stage** | The obligation is design or planning evidence — a matrix, an inventory, a mapping | **Yes**, and where Phase 2 produced the evidence the gate is marked `CLOSED` with its artifact named |
| **Implementation-stage** | The obligation is execution evidence — an AOT publish, a hardware result, a received payout, a passing test | **No.** Phase 2 schedules it against a named package; only recorded execution evidence closes it |

A gate is never closed by registering a finding about it, and never closed by a weaker gate passing in its place.

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
| OG-05 | **Identifier disambiguation.** `PG-nn` in this register and in the assurance and planning layers means *Phase 2 gate*. [`../requirements/products/arcslate.md`](../requirements/products/arcslate.md) independently uses `PG-01`–`PG-14` for its *processing graph* rules. **The namespaces collide.** Every cross-document citation of an ArcSlate processing-graph rule is therefore qualified by its document — for example “`PG-08` in the ArcSlate requirements” — and an unqualified `PG-nn` always means a gate. This is a convention, not a structural guarantee; it is recorded as a known limitation rather than left implicit. |
| OG-06 | **`PG-14b` is deliberately suffixed.** `PG-14` is already an ArcSlate processing-graph rule in [`../requirements/products/arcslate.md`](../requirements/products/arcslate.md), and reusing the bare number would have made two unrelated obligations indistinguishable in citation. The suffix is the disambiguation `OG-05` requires. |

---

## 2. Deferred gates carried from Phase 1

| Gate | Subject | Owner | Trigger | Blocks | Scheduled in | State |
|---|---|---|---|---|---|---|
| **F-013** | Reference-repository licences and file-level SPDX evidence (**D-013**) | Licensing and Provenance Owner | The first step of a product's Reference Coverage Matrix and licence audit — **fired and satisfied 2026-09-05** | That product's implementation planning; `P-02` in the release gates | Design-stage evidence: the five matrices in [`reference-coverage/`](reference-coverage/README.md), 145 item-level rows with a licence position each | **`CLOSED` 2026-09-05** for every registered reference under the amended **D-012** map |
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
| **PG-01** | The per-product **Reference Coverage Matrix** exists with a disposition for every item (**D-012**) | Product Owner with Architecture Owner | Start of that product's implementation planning — **fired and satisfied 2026-09-05** | `P-01`; that product's first release | Design-stage evidence: [`reference-coverage/`](reference-coverage/README.md) — ArcChat 30 rows, ArcNotes 41, ArcScope 31, ArcSlate 31, distribution 12 | **`CLOSED` 2026-09-05** for all four products and the distribution oracle |
| **PG-02** | The **implementation-state reconciliation inventory** exists before repository restructuring begins | Architecture Owner | Before the first restructuring change — **fired and satisfied 2026-09-05** | All restructuring work | Design-stage evidence: [`implementation-state-reconciliation.md`](implementation-state-reconciliation.md) — 166 of 166 projects, 6 of 6 native shims, 28 test suites | **`CLOSED` 2026-09-05** |
| **PG-03** | The **native dependency licence review** per product, against that product's licence boundary (`LD-07` in the native architecture) | Licensing and Provenance Owner | First native dependency accepted into a product | That dependency's use | The native interoperability work package | `OPEN` |
| **PG-04** | **Runbook rehearsal evidence**: every required runbook executed at least once, with a dated record (`RB-04` in the observability architecture) | Operations Owner | Before paid cloud go-live | `L-12` | The operations readiness work package | `OPEN` |
| **PG-05** | **Redaction proof**: marker values injected as headers, tokens, prompts and document content never appear in exported telemetry (`TV-01` there) | Operations Owner | First telemetry export to an external backend | `R-16` | The observability work package | `OPEN` |
| **PG-06** | **Design-stage invariant traceability**: every catalogued invariant has an architecture home, an enforcement mechanism, a **planned** verification specification and an owning work-package completion gate (**D-018** obligation B) | Architecture Owner | On completion of the glossary catalogue | Finalising the design baseline | `WP-00.01`; evidence in [`invariant-coverage.md`](invariant-coverage.md) `§7` | **`CLOSED` 2026-09-05** — 421 of 421 mapped |
| **PG-11** | **Implementation-stage invariant enforcement**: every catalogued invariant has an **implemented** check and a **passing** result (**D-018** obligation C) | Each invariant's owning package owner, coordinated by the Architecture Owner | Each owning package reaching its completion gate | That package's completion gate; and `P-03` for the affected product | Distributed across the owning packages listed in [`invariant-coverage.md`](invariant-coverage.md) `§7` | `OPEN` |
| **PG-07** | **Format fixture completeness**: every claimed import format version has a fixture (`ME-03` in the provenance document) | Product Owner per product | First public import claim for that product | That claim | The per-product import and export work packages | `OPEN` |
| **PG-08** | **Hardware lab inventory**: a maintained device, firmware and driver inventory exists before ArcScope or ArcSlate hardware results are accepted (`TE-03` in the testing strategy) | Quality Owner | First hardware-lab test run | `C-04` | The ArcScope and ArcSlate verification work packages | `OPEN` |
| **PG-09** | **Extension protocol conformance**: the reference-extension suite passes before the extension platform is opened to third parties | Architecture Owner | Before third-party extension enablement | `L-60` | The extension platform work package | `OPEN` |
| **PG-10** | **Provider test-environment coverage**: every provider integration is exercised against the provider's test environment and frozen as recorded contract fixtures (`TE-04` there) | Architecture Owner | First provider integration | `L-28`, `L-29` | The commerce and AI provider work packages | `OPEN` |
| **PG-12** | **ArcNotes document-rendering dependency**: `AT-05` requires in-product PDF viewing with page-anchored annotation targets, which no managed-only path in the current stack delivers. The dependency's owner, substitute analysis, licence position and provenance record must exist **before adoption** (`DR-03`), and until then `AT-05` is not met | Architecture Owner with Licensing and Provenance Owner | First implementation of the ArcNotes attachment viewer | `AT-05`; ArcNotes' first release claim of PDF support | `WP-18.05`; scope in `§2.1` of the native interoperability architecture and `§8.2` of the editing architecture | `OPEN` |
| **PG-13** | **Real-provider metering evidence**: one real provider usage response and one real payment-provider event reconciled through the same code as the fixtures, plus the `§8.6` worked fixture asserted exactly. Interfaces, fixed responses and in-memory mock balances are **not** completion evidence (`MT-01`, `§10.6` of the configuration requirements) | Architecture Owner with Commercial Operations Owner | First paid AI dispatch in any environment | Paid AI go-live; `PG-10` | `WP-43.07`, `WP-42.11` | `OPEN` |
| **PG-14b** | **Simulator acceptance against the real host**: same-seed hashes, fault positions, killed host with fenced takeover, duplicate commands, malformed AST and CSV, quota exhaustion, cross-workspace denial, realtime-disabled reconnect, partial cancellation and a 24-hour bounded-resource soak. **A preview or test fake is insufficient** (`SIM-20`) | Quality Owner with Architecture Owner | First ArcScope Cloud simulation release claim | ArcScope release; `WP-34` verification that depends on a repeatable source | `WP-51.00`–`WP-51.05` | `OPEN` |
| **PG-15** | **OTIO bidirectional evidence**: real fixtures and the pinned official library exercising import and export, mixed and fractional rates with no frame shift, unsupported-feature reports, malicious paths, malformed input, cancellation and semantic round-trip. **Merely opening JSON is insufficient** (`OT-12`) | Quality Owner | First ArcSlate interchange release claim | ArcSlate release | `WP-39.05` | `OPEN` |
| **PG-16** | **Configuration activation evidence**: two example policies producing different future decisions and identical historical charges; malformed, partial and duplicate-version rejection; replacement during concurrent requests with no mixed-version evaluation, quota reset or duplicate grant; all replicas restarting with balances, holds and refill state preserved; and the client projection proven free of server-only parameters and credentials (`§10.6` there) | Operations Owner with Architecture Owner | Before the first paid production deployment | Paid production go-live | `WP-44.01`, `WP-42.11` | `OPEN` |
| **PG-17** | **Commit-order feed proof**: a change committed *after* a later one still receives a higher `publish_seq` and is delivered to a cursor that already advanced past it. The previous in-transaction sequence design could not provide this, and no monotonic-identifier argument substitutes for the test (`PB-01`, `PB-02`) | Architecture Owner | First multi-writer sync deployment | Sync go-live; every client cursor guarantee | `WP-21.05`, `WP-25.02` | `OPEN` |
| **PG-18** | **Uncertain-effect proof**: a crash after dispatch and before any outcome is classified `unknown`, is **not** retried automatically, and resolves only through declared idempotency, an owner status operation, the provider's record, the deadline or a user decision (`§6.4` of the harness). A capability declaring neither idempotency nor a status operation is proven **unregistrable** (`UR-02`) | Quality Owner with Architecture Owner | First device-tool or MCP invocation in a paid environment | Paid AI go-live; any external-effect capability | `WP-52.02`, `WP-52.04` | `OPEN` |
| **PG-19** | **Backfill catch-up and rollback-window proof**: a row updated by old code after its backfill is caught before the switch; a mode B converter maintains the new representation for a writer that does not know it exists; and the pre-rollback check refuses an unsafe rollback naming the mode and cutover that closed the window (`BF-05`, `BF-07`, `RW-05`) | Operations Owner | First expand/contract migration against production-shaped data | Any schema evolution in production | `WP-21.03`, `WP-50.04` | `OPEN` |
| **PG-20** | **Time-model proof**: frame↔tick and sample↔tick round-trip exactly for every supported rate; no stored position is a frame, a sample, a float or a duration type; and a long sequence at 30000/1001 fps with 48 kHz audio shows **no cumulative drift** (`TB-01`, `TV-01`, `TV-04`) | Quality Owner | First ArcSlate timeline release claim | ArcSlate release; OTIO round-trip claims | `WP-36.01`, `WP-37.02` | `OPEN` |

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

## 6. Unresolved determinations

**None.**

Distinct from a gate. A gate has a known obligation awaiting evidence; an **unresolved determination** is a question the accessible material cannot answer. One existed and is closed.

| # | Determination | Resolution | State |
|---|---|---|---|
| **OC-01** | **Olive was registered by D-012 as an ArcSlate reference but was not present** at the authorized reference-map location | **User decision, 2026-09-05** (`P2-005`): ArcSlate's direct reference repositories are **ArcVideo and ArcVideoFoundation**; there is no requirement to obtain or independently review an Olive repository. Olive could not be built in the user's environment, and ArcVideo carries the modifications made to get that codebase building. **D-012**'s reference map is amended accordingly | **`CLOSED` 2026-09-05** |

| # | Rule |
|---|---|
| UD-01 | **Closing OC-01 removed an audit obligation, not a provenance obligation.** ArcVideo is a documented Olive fork; its GPL-3.0 obligations, upstream copyright and attribution to the Olive authors are preserved wherever inherited material requires them (**D-013**; `§3.1` of the ArcSlate matrix). |
| UD-02 | **A future unresolved determination is recorded here** with the same fields, and blocks whatever depends on it until decided. |

---

## 7. Register summary

| Class | Count | Note |
|---|---|---|
| Deferred gates carried from Phase 1 | 3 | **F-013 closed**; F-023 and F-026 remain implementation-stage |
| Gates created by the verification record | 12 active + 1 merged | All implementation-stage; none closable by design work |
| Gates created by Phase 2 | 20 | `PG-06` split into `PG-06` (design) and `PG-11` (implementation); `PG-12` added by the editing pass; **`PG-13`, `PG-14b`, `PG-15`, `PG-16` added by the P2-006 reconciliation** |
| **Closed by design-stage evidence** | **4** | `F-013`, `PG-01`, `PG-02`, `PG-06` — each with a named artifact |
| **Open implementation-stage gates** | **31** | Legitimate future obligations; their triggers are listed per gate |
| Unresolved determinations | **0** | `OC-01` closed by user decision 2026-09-05 (`P2-005`) |

| # | Rule |
|---|---|
| RS-01 | **A design-stage gate closes on design evidence.** Four have. |
| RS-02 | **An implementation-stage gate never closes on design evidence**, however complete that evidence is. |
| RS-03 | **`PG-06` closing does not close `PG-11`.** They are different obligations with different evidence; the weaker one passing has no effect on the stronger one. |

---

## 8. Traceability

| Source | Consumed as |
|---|---|
| [`phase-1-official-verification.md`](phase-1-official-verification.md) | Every "Required gate" statement, transcribed with owner, trigger and scheduling |
| [`phase-1-input-review-ledger.md`](phase-1-input-review-ledger.md) | The deferred-gate register carried forward |
| **D-003** | Verification scope and the first-consumption rule |
| **D-016** | Deferred-decision ownership |
| **D-020** | Commercial figures as versioned policy, not verified constants |
