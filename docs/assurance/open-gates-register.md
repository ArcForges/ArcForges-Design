# Open Gates Register

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Assurance
> Governing authority: **[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)** (verification scope and the first-consumption rule), **[D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016)** (deferred-decision ownership)
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
| <a id="rule-og-02"></a>OG-02 | **A gate whose trigger has fired and which is not closed blocks the dependent work** — it does not become a warning. |
| OG-03 | **A gate may not be silently re-scoped.** Changing a gate requires a decision record. |
| OG-04 | **A new gate discovered during implementation is added here**, with the same fields, rather than living only in the document that discovered it. |
| <a id="rule-og-05"></a>OG-05 | Rule identifiers are document-scoped. Every active citation is a direct link to its defining document and stable rule anchor; the same spelling in a different document is a different rule. Retired identifiers link to an explicit historical relocation, and reserved allocation ranges are metadata, not requirements. No unresolved or silently guessed citation is permitted. The complete current-corpus check is the design evidence for [PG-21](#rule-pg-21); subsequent edits must repeat it. |
| OG-06 | **[PG-14b](#rule-pg-14b) is deliberately suffixed.** [PG-14](../requirements/products/arcslate.md#rule-pg-14) is already an ArcSlate processing-graph rule in [`../requirements/products/arcslate.md`](../requirements/products/arcslate.md), and reusing the bare number would have made two unrelated obligations indistinguishable in citation. The suffix is the disambiguation [OG-05](#rule-og-05) requires. |

---

## 2. Deferred gates carried from Phase 1

| Gate | Subject | Owner | Trigger | Blocks | Scheduled in | State |
|---|---|---|---|---|---|---|
| <a id="rule-f-013"></a>**F-013** | Reference-repository licences and file-level SPDX evidence (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**) | Licensing and Provenance Owner | The first step of a product's Reference Coverage Matrix and licence audit — **fired and satisfied 2026-09-05** | That product's implementation planning; [P-02](release-gates.md#rule-p-02) in the release gates | Design-stage evidence: the five matrices in [`reference-coverage/`](reference-coverage/README.md), 145 item-level rows with a licence position each | **`CLOSED` 2026-09-05** for every registered reference under the amended **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** map |
| <a id="rule-f-023"></a>**F-023** | ArcChat Mobile provenance and complete direct and transitive dependency closure (**[D-004](../decisions/phase-1-foundation-decisions.md#rule-d-004)**) | Release Engineering Owner **and** Licensing and Provenance Owner; Product Owner approves | Before the first store, test-flight, store-listing or sideloadable mobile artifact is produced | Any mobile artifact; [L-50](release-gates.md#rule-l-50) | The mobile release work package | `OPEN` |
| <a id="rule-f-026"></a>**F-026** | Typed HTTP client version pin, generated-only entry point, reflection-package prohibition, generator diagnostic treated as build-breaking | Owning platform work-package owner; Architecture Owner approves | Before accepting the typed HTTP client into an AOT deliverable | Any AOT deliverable consuming it; [R-03](release-gates.md#rule-r-03) | The platform skeleton and AOT proof work package | `OPEN` |

---

## 3. Gates created by the official verification record

| Gate | Source | Owner | Trigger | Blocks | Scheduled in | State |
|---|---|---|---|---|---|---|
| <a id="rule-vg-01"></a>**VG-01** | **[V-01](phase-1-official-verification.md#rule-v-01)** — confirm whether ArcForges adheres to the transparency code of practice for AI-generated content or relies on equivalently adequate alternative means, and record the marking mechanism per artifact type | Security and Privacy Owner, with Product Owner approval | First EU market availability | First EU-available release | The AI transparency and compliance work package | `OPEN` |
| <a id="rule-vg-02"></a>**VG-02** | **[V-02](phase-1-official-verification.md#rule-v-02)** — pin the exact MCP SDK version and record an explicit mapping between MCP extension concepts and the ArcForges execution vocabulary defined by the normative glossary (**[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)**) | Architecture Owner | Start of the MCP and extension work package | Finalising that work package | The extension and integration platform work package | `OPEN` |
| <a id="rule-vg-03"></a>**VG-03** | **[V-05a](phase-1-official-verification.md#rule-v-05a)** — a real AOT publish proof of the desktop shell plus every third-party control actually used, with zero trim or AOT diagnostics | Owning platform work-package owner | Before accepting any third-party control into an AOT deliverable | Adoption of that control | The desktop shell and design system work package | `OPEN` |
| <a id="rule-vg-04"></a>**VG-04** | **[V-05b](phase-1-official-verification.md#rule-v-05b)** — an AOT publish proof of the desktop host with the real local-RPC contract set, plus a repository-policy test asserting every RPC contract interface carries its generated-shape attribute | Architecture Owner | Before the first AOT desktop deliverable | That deliverable | The platform skeleton and AOT proof work package | `OPEN` |
| <a id="rule-vg-05"></a>**VG-05** | **[V-05c](phase-1-official-verification.md#rule-v-05c)** — see **[F-026](#rule-f-026)**; recorded there | — | — | — | — | Merged into **[F-026](#rule-f-026)** |
| <a id="rule-vg-06"></a>**VG-06** | **[V-05e](phase-1-official-verification.md#rule-v-05e)** — if any Cloud component is ever moved into an AOT deliverable, its full dependency closure requires an AOT publish proof at that time | Architecture Owner | Any decision to AOT-publish a Cloud component | That decision's implementation | Not scheduled — conditional on a decision that has not been taken (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** makes Cloud JIT) | `OPEN — dormant` |
| <a id="rule-vg-07"></a>**VG-07** | **[V-04](phase-1-official-verification.md#rule-v-04)** gate (a) — before the first Android production build, confirm the runtime is Mono AOT and that the runtime selection is explicit in the project file rather than inherited from a default | Release Engineering Owner with Architecture Owner | First Android production build | That build; [L-53](release-gates.md#rule-l-53) | The mobile platform work package | `OPEN` |
| <a id="rule-vg-08"></a>**VG-08** | **[V-04](phase-1-official-verification.md#rule-v-04)** gate (b) — before any framework major-version upgrade, re-verify the Android runtime posture and re-run the mobile AOT and trim proof | Release Engineering Owner with Architecture Owner | Any framework major-version upgrade | That upgrade | The dependency and framework upgrade work package | `OPEN — recurring` |
| <a id="rule-vg-09"></a>**VG-09** | **[V-04](phase-1-official-verification.md#rule-v-04)** gate (c) — iOS release runtime re-verified against the then-current supported baseline before build activation | Release Engineering Owner with Architecture Owner | iOS build activation | iOS release | Deferred with the iOS build itself (**[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)**) | `OPEN — dormant` |
| <a id="rule-vg-10"></a>**VG-10** | **[V-06](phase-1-official-verification.md#rule-v-06)** — supplier onboarding and account approval; sanctions and export screening for the intended market set | Commercial Operations Owner | Before the first live transaction | Commercial go-live; [L-20](release-gates.md#rule-l-20), [L-21](release-gates.md#rule-l-21) | The commerce go-live work package | `OPEN` |
| <a id="rule-vg-11"></a>**VG-11** | **[V-07](phase-1-official-verification.md#rule-v-07)** — payout account eligibility and receiving-currency confirmation for the chosen supplier jurisdiction | Commercial Operations Owner | First authoritative pricing specification, and again before launch | Commercial go-live; [L-22](release-gates.md#rule-l-22) | The commerce go-live work package | `OPEN` |
| <a id="rule-vg-12"></a>**VG-12** | **[V-08](phase-1-official-verification.md#rule-v-08)** — the additional regional gates: the separate payment-method application with its stated criteria; a local-currency product and tax configuration existing before approval can be sought; and a refund and dispute model validated against the absence of chargeback support | Commercial Operations Owner, with Product Owner approval on the pricing catalogue | Before enabling mainland-China sales | That market's enablement; [L-40](release-gates.md#rule-l-40) | The regional enablement work package | `OPEN — conditional` |
| <a id="rule-vg-13"></a>**VG-13** | **[V-09](phase-1-official-verification.md#rule-v-09)** — before the first store submission, confirm category fit with review and confirm that no build path can display a purchase call to action or accept a licence key; before the first alternative-store submission, confirm consumption-only conformance | Release Engineering Owner with Product Owner approval | First mobile store submission | That submission; [L-51](release-gates.md#rule-l-51), [L-52](release-gates.md#rule-l-52) | The mobile release work package | `OPEN` |

---

## 4. Gates created by Phase 2

These are new obligations that follow from Phase 2 architecture rather than from Phase 1. Each is a scheduling obligation, not a reopened decision.

| Gate | Subject | Owner | Trigger | Blocks | Scheduled in | State |
|---|---|---|---|---|---|---|
| <a id="rule-pg-01"></a>**PG-01** | The per-product **Reference Coverage Matrix** exists with a disposition for every item (**[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**) | Product Owner with Architecture Owner | Start of that product's implementation planning — **fired and satisfied 2026-09-05** | [P-01](release-gates.md#rule-p-01); that product's first release | Design-stage evidence: [`reference-coverage/`](reference-coverage/README.md) — ArcChat 30 rows, ArcNotes 41, ArcScope 31, ArcSlate 31, distribution 12 | **`CLOSED` 2026-09-05** for all four products and the distribution oracle |
| <a id="rule-pg-02"></a>**PG-02** | The **implementation-state reconciliation inventory** exists before repository restructuring begins | Architecture Owner | Before the first restructuring change — **fired and satisfied 2026-09-05** | All restructuring work | Design-stage evidence: [`implementation-state-reconciliation.md`](implementation-state-reconciliation.md) — 166 of 166 projects, 6 of 6 native shims, 28 test suites | **`CLOSED` 2026-09-05** |
| <a id="rule-pg-03"></a>**PG-03** | The **native dependency licence review** per product, against that product's licence boundary ([LD-07](../architecture/12-native-interop-and-media.md#rule-ld-07) in the native architecture) | Licensing and Provenance Owner | First native dependency accepted into a product | That dependency's use | The native interoperability work package | `OPEN` |
| <a id="rule-pg-04"></a>**PG-04** | **Runbook rehearsal evidence**: every required runbook executed at least once, with a dated record ([RB-04](../architecture/13-observability-and-operations.md#rule-rb-04) in the observability architecture) | Operations Owner | Before paid cloud go-live | [L-12](release-gates.md#rule-l-12) | The operations readiness work package | `OPEN` |
| <a id="rule-pg-05"></a>**PG-05** | **Redaction proof**: marker values injected as headers, tokens, prompts and document content never appear in exported telemetry ([TV-01](../architecture/13-observability-and-operations.md#rule-tv-01) there) | Operations Owner | First telemetry export to an external backend | [R-16](release-gates.md#rule-r-16) | The observability work package | `OPEN` |
| <a id="rule-pg-06"></a>**PG-06** | **Design-stage invariant traceability**: every catalogued invariant has an architecture home, an enforcement mechanism, a **planned** verification specification and an owning work-package completion gate (**[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** obligation B) | Architecture Owner | On completion of the glossary catalogue | Finalising the design baseline | [WP-00.01](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.01); evidence in [`invariant-coverage.md`](invariant-coverage.md) `§7` | **`CLOSED` 2026-09-05, re-verified against the revised catalogue** — **429 of 429 mapped**. The original closure was 421 of 421; [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006) added [I-491](../requirements/01-normative-glossary-and-invariants.md#rule-i-491)–[I-498](../requirements/01-normative-glossary-and-invariants.md#rule-i-498), and [PR-03](invariant-coverage.md#rule-pr-03) requires the count to be recomputed rather than carried forward, which `§7` does |
| <a id="rule-pg-11"></a>**PG-11** | **Implementation-stage invariant enforcement**: every catalogued invariant has an **implemented** check and a **passing** result (**[D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)** obligation C) | Each invariant's owning package owner, coordinated by the Architecture Owner | Each owning package reaching its completion gate | That package's completion gate; and [P-03](release-gates.md#rule-p-03) for the affected product | Distributed across the owning packages listed in [`invariant-coverage.md`](invariant-coverage.md) `§7` | `OPEN` |
| <a id="rule-pg-07"></a>**PG-07** | **Format fixture completeness**: every claimed import format version has a fixture ([ME-03](reference-coverage-and-provenance.md#rule-me-03) in the provenance document) | Product Owner per product | First public import claim for that product | That claim | The per-product import and export work packages | `OPEN` |
| <a id="rule-pg-08"></a>**PG-08** | **Hardware lab inventory**: a maintained device, firmware and driver inventory exists before ArcScope or ArcSlate hardware results are accepted ([TE-03](testing-and-verification-strategy.md#rule-te-03) in the testing strategy) | Quality Owner | First hardware-lab test run | [C-04](release-gates.md#rule-c-04) | The ArcScope and ArcSlate verification work packages | `OPEN` |
| <a id="rule-pg-09"></a>**PG-09** | **Extension protocol conformance**: the reference-extension suite passes before the extension platform is opened to third parties | Architecture Owner | Before third-party extension enablement | [L-60](release-gates.md#rule-l-60) | The extension platform work package | `OPEN` |
| <a id="rule-pg-10"></a>**PG-10** | **Provider test-environment coverage**: every provider integration is exercised against the provider's test environment and frozen as recorded contract fixtures ([TE-04](testing-and-verification-strategy.md#rule-te-04) there) | Architecture Owner | First provider integration | [L-28](release-gates.md#rule-l-28), [L-29](release-gates.md#rule-l-29) | The commerce and AI provider work packages | `OPEN` |
| <a id="rule-pg-12"></a>**PG-12** | ArcNotes PDF viewing dependency and actual ContentSandbox containment: provenance/licence/native binding and packaged RID evidence; malformed native input must not crash the parent | Architecture Owner with Licensing and Provenance Owner | First implementation of the ArcNotes attachment viewer | [AT-05](../requirements/products/arcnotes.md#rule-at-05); ArcNotes' first release claim of PDF support | [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04), [WP-11.09](../planning/work-packages/11-security-foundation.md#rule-wp-11.09); [isolation architecture](../architecture/24-content-and-extension-isolation.md) | `OPEN` |
| <a id="rule-pg-13"></a>**PG-13** | **Real-provider metering evidence**: one real provider usage response and one real payment-provider event reconciled through the same code as the fixtures, plus the `§8.6` worked fixture asserted exactly. Interfaces, fixed responses and in-memory mock balances are **not** completion evidence ([MT-01](../requirements/04-commerce-entitlement-and-credits.md#rule-mt-01), `§10.6` of the configuration requirements) | Architecture Owner with Commercial Operations Owner | First paid AI dispatch in any environment | Paid AI go-live; [PG-10](#rule-pg-10) | [WP-43.07](../planning/work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07), [WP-42.11](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) | `OPEN` |
| <a id="rule-pg-14b"></a>**PG-14b** | **Simulator acceptance against the real host**: same-seed hashes, fault positions, killed host with fenced takeover, duplicate commands, malformed AST and CSV, quota exhaustion, cross-workspace denial, realtime-disabled reconnect, partial cancellation and a 24-hour bounded-resource soak. **A preview or test fake is insufficient** ([SIM-20](../requirements/products/arcscope.md#rule-sim-20)) | Quality Owner with Architecture Owner | First ArcScope Cloud simulation release claim | Any ArcScope claim that Cloud simulation is a delivered capability. **It does not gate [WP-34](../planning/work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34)**, whose repeatable source is file/replay from [WP-33](../planning/work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) ([SD-09](../requirements/products/arcscope.md#rule-sd-09) of the ArcScope requirements) | [WP-51.00](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.00)–[WP-51.05](../planning/work-packages/51-arcscope-cloud-simulator.md#rule-wp-51.05) | `OPEN` |
| <a id="rule-pg-15"></a>**PG-15** | **OTIO bidirectional evidence**: real fixtures and the pinned official library exercising import and export, mixed and fractional rates with no frame shift, unsupported-feature reports, malicious paths, malformed input, cancellation and semantic round-trip. **Merely opening JSON is insufficient** ([OT-12](../requirements/products/arcslate.md#rule-ot-12)) | Quality Owner | First ArcSlate interchange release claim | ArcSlate release | [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) | `OPEN` |
| <a id="rule-pg-16"></a>**PG-16** | **Configuration activation evidence**: two example policies producing different future decisions and identical historical charges; malformed, partial and duplicate-version rejection; replacement during concurrent requests with no mixed-version evaluation, quota reset or duplicate grant; all replicas restarting with balances, holds and refill state preserved; and the client projection proven free of server-only parameters and credentials (`§10.6` there) | Operations Owner with Architecture Owner | Before the first paid production deployment | Paid production go-live | [WP-44.01](../planning/work-packages/44-dynamic-policy-and-configuration.md#rule-wp-44.01), [WP-42.11](../planning/work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) | `OPEN` |
| <a id="rule-pg-17"></a>**PG-17** | Published-feed and bootstrap proof: late commit remains above an advanced cursor; lowest revision per aggregate despite reversed same-millisecond UUIDs; round-robin fairness; bootstrap v2 followed by feed v1 cannot regress state; tombstones, own echoes and structural references reconcile | Architecture Owner | First multi-writer sync deployment | Sync go-live; every client cursor guarantee | [WP-21.05](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.05), [WP-25.02](../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.02), [WP-25.07](../planning/work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.07) | `OPEN` |
| <a id="rule-pg-18"></a>**PG-18** | **Uncertain-effect proof**: a crash after dispatch and before any outcome is classified `unknown`, is **not** retried automatically, and resolves only through declared idempotency, an owner status operation, the provider's record, the deadline or a user decision (`§6.4` of the harness). A capability declaring neither idempotency nor a status operation is proven **unregistrable** ([UR-02](../architecture/17-agent-harness.md#rule-ur-02)) | Quality Owner with Architecture Owner | First device-tool or MCP invocation in a paid environment | Paid AI go-live; any external-effect capability | [WP-52.02](../planning/work-packages/52-cloud-harness.md#rule-wp-52.02), [WP-52.04](../planning/work-packages/52-cloud-harness.md#rule-wp-52.04) | `OPEN` |
| <a id="rule-pg-19"></a>**PG-19** | Versioned backfill and fenced-cutover proof: delayed v1 cannot overwrite captured v2/tombstone; all old/new writers participate; exclusive cutover drains in-flight commits/capture and verifies every dirty range; A/B converter preserves rollback while C closes it explicitly | Operations Owner | First expand/contract migration against production-shaped data | Any schema evolution in production | [WP-21.03](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.03), [WP-50.04](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.04) | `OPEN` |
| <a id="rule-pg-20"></a>**PG-20** | Time model proof: exact supported output-grid projections, reported inexact-source conform, per-track cut ownership with one mixed sample across tracks/dissolves/gaps, and the official OTIO double boundary without silent frame/sample drift | Quality Owner | First ArcSlate timeline release claim | ArcSlate release; OTIO round-trip claims | [WP-36.01](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.01), [WP-37.04](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.04), [WP-39.05](../planning/work-packages/39-arcslate-integration-and-portability.md#rule-wp-39.05) | `OPEN` |
| <a id="rule-pg-21"></a>**PG-21** | Complete current-corpus citation proof: every active citation names one defining document and stable anchor; no missing, duplicate or unqualified reference remains ([OG-05](#rule-og-05)). Reserved headroom and explicit historical relocations are not implementation obligations. | Quality Owner with Architecture Owner | Current Stage 2 repair and every later normative edit | Acceptance criteria that cite design rules | [Executable corpus check and recorded evidence](design-repair-verification.md); [repair review](phase-2-design-closure-review.md). Continuing verification in [WP-00.01](../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.01) | **`CLOSED` on current design evidence; future edits recheck** |
| <a id="rule-pg-22"></a>**PG-22** | **OS isolation proof**: real packaged C# ContentSandbox and executable-extension profiles deny product-store/credential/network/process escape, contain native crash/hang/exhaustion and clean up after parent death; no unrestricted fallback | Security and Privacy Owner with Release Engineering Owner | Before any first-party hostile parser or executable extension ships on a RID | PDF/image/media parsing and executable extensions on that RID | [WP-11.09](../planning/work-packages/11-security-foundation.md#rule-wp-11.09), [WP-18.04](../planning/work-packages/18-arcnotes-document-core.md#rule-wp-18.04), [WP-37.01](../planning/work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.01), [WP-41.00](../planning/work-packages/41-extension-platform-and-integrations.md#rule-wp-41.00) | `OPEN` |

---

## 5. What is deliberately not verified

**[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)** established a verification scope and a first-consumption rule. This register preserves it.

| Category | Position |
|---|---|
| Prices, fees, quotas, rates and commercial figures | **Deliberately not verified.** Deferred under **[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)**'s first-consumption rule with a named owner and trigger; every figure is versioned commercial policy under **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** |
| Third-party pricing pages and plan tiers | Not verified; verified at first consumption by the owning work package |
| Vendor feature roadmaps | Not verified; only current, documented behaviour is relied upon |
| Reference-repository internals beyond behavioural evidence | Not verified; governed by **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** and **[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)** |

| # | Rule |
|---|---|
| NV-01 | **A figure quoted from the input corpus is recorded as a corpus proposal, never as a commitment** (**[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)**). |
| <a id="rule-nv-02"></a>NV-02 | **Consuming an unverified external fact triggers its verification at that moment** (**[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)**), and the verification result is recorded in the assurance layer. |

---

## 6. Unresolved determinations

**None.**

Distinct from a gate. A gate has a known obligation awaiting evidence; an **unresolved determination** is a question the accessible material cannot answer. One existed and is closed.

| # | Determination | Resolution | State |
|---|---|---|---|
| <a id="rule-oc-01"></a>**OC-01** | **Olive was registered by [D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012) as an ArcSlate reference but was not present** at the authorized reference-map location | **User decision, 2026-09-05** ([P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005)): ArcSlate's direct reference repositories are **ArcVideo and ArcVideoFoundation**; there is no requirement to obtain or independently review an Olive repository. Olive could not be built in the user's environment, and ArcVideo carries the modifications made to get that codebase building. **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**'s reference map is amended accordingly | **`CLOSED` 2026-09-05** |

| # | Rule |
|---|---|
| <a id="rule-ud-01"></a>UD-01 | **Closing [OC-01](#rule-oc-01) removed an audit obligation, not a provenance obligation.** ArcVideo is a documented Olive fork; its GPL-3.0 obligations, upstream copyright and attribution to the Olive authors are preserved wherever inherited material requires them (**[D-013](../decisions/phase-1-foundation-decisions.md#rule-d-013)**; `§3.1` of the ArcSlate matrix). |
| UD-02 | **A future unresolved determination is recorded here** with the same fields, and blocks whatever depends on it until decided. |

---

## 7. Register summary

| Class | Count | Note |
|---|---|---|
| Deferred gates carried from Phase 1 | 3 | **[F-013](#rule-f-013) closed**; [F-023](#rule-f-023) and [F-026](#rule-f-026) remain implementation-stage |
| Gates created by the verification record | 12 active + 1 merged | All implementation-stage; none closable by design work |
| Gates created by Phase 2 | 22 | Includes the current citation closure and the new packaged OS isolation gate |
| **Closed by design-stage evidence** | **5** | [F-013](#rule-f-013), [PG-01](#rule-pg-01), [PG-02](#rule-pg-02), [PG-06](#rule-pg-06), [PG-21](#rule-pg-21) |
| **Open implementation-stage gates** | **32** | Includes two dormant entries; the other 30 are current, conditional or recurring. One additional verification entry is merged, not counted twice as an open obligation |
| Unresolved determinations | **0** | [OC-01](#rule-oc-01) closed by user decision 2026-09-05 ([P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005)) |

| # | Rule |
|---|---|
| <a id="rule-rs-01"></a>RS-01 | **A design-stage gate closes on design evidence.** Five currently have. |
| RS-02 | **An implementation-stage gate never closes on design evidence**, however complete that evidence is. |
| <a id="rule-rs-03"></a>RS-03 | **[PG-06](#rule-pg-06) closing does not close [PG-11](#rule-pg-11).** They are different obligations with different evidence; the weaker one passing has no effect on the stronger one. |

---

## 8. Traceability

| Source | Consumed as |
|---|---|
| [`phase-1-official-verification.md`](phase-1-official-verification.md) | Every "Required gate" statement, transcribed with owner, trigger and scheduling |
| [`phase-1-input-review-ledger.md`](phase-1-input-review-ledger.md) | The deferred-gate register carried forward |
| **[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)** | Verification scope and the first-consumption rule |
| **[D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016)** | Deferred-decision ownership |
| **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)** | Commercial figures as versioned policy, not verified constants |
