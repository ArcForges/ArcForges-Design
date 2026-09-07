# Phase 1 Foundation Decision Register

> Status: **Foundation Freeze requested** — Phase 1 (Input Review and Foundation Decision Freeze)
> Branch: `design/phase-1-foundation`
> Companions: `docs/assurance/phase-1-input-review-ledger.md`, `docs/assurance/phase-1-official-verification.md`

This register holds every material issue found while reviewing the closed Phase 1 input corpus, together with the user decisions that resolve them. Nothing here is a specification. Only a decision the user has actually given is recorded as `USER_CONFIRMED`.

> **Current amendment (2026-09-06):** [P2-006](phase-2-specification-decisions.md#rule-p2-006) records subsequent explicit user direction and delegated requirements design. Original quotations below remain historical records and do not reinstate superseded obligations.

## Authority order

Confirmed by the user as **[D-001](#rule-d-001)**.

1. Current explicit user decisions.
2. The user-confirmed Phase 1 decision register.
3. Raw input documents as evidence of prior intent and exploration only.
4. Current official primary sources for externally verifiable facts.

**There is no automatic precedence among the raw input documents.** The sequencing notes, later stages, the architecture concept and the overview do not automatically override one another. A later or apparently more specific statement may be evidence of intended evolution, but it is not authoritative until reviewed.

Neither the existing implementation monorepo nor any undeclared historical plan is design authority. A statement is not correct merely because it appears later in a file, appears repeatedly, is written confidently, or is labelled "final", "frozen" or "recommended".

## Conflict handling procedure

Confirmed by the user as part of **[D-001](#rule-d-001)**. For every material conflict: register it; explain the likely evolution; provide the viable alternatives and a recommendation; obtain a user decision; record the disposition; apply that confirmed disposition consistently afterward without asking the same question again.

Every confirmed global disposition applies to all occurrences it covers without further asking. Only material conflicts **not** already covered by an existing user decision are brought back.

## Status vocabulary

`USER_CONFIRMED` · `REJECTED` · `SUPERSEDED` · `DEFERRED_WITH_OWNER_AND_TRIGGER`

`OPEN` and `PROPOSED` no longer appear in this register. Every registered issue is resolved or validly deferred.

## Source shorthand

`I1` overview · `I2` sequencing notes · `I3` architecture concept · `I4` discovery record (cited as `I4 §Stage N.item`) · `V-NN` a finding in `docs/assurance/phase-1-official-verification.md`.

---

# Issue index

| ID | Subject | Status | Resolved / governed by |
|---|---|---|---|
| <a id="rule-f-001"></a>F-001 | Conflict-resolution rule for the input corpus | `USER_CONFIRMED` | [D-001](#rule-d-001) |
| <a id="rule-f-002"></a>F-002 | Product portfolio; ArcCanvas, ArcMusic, ArcImage | `USER_CONFIRMED` | [D-002](#rule-d-002) |
| <a id="rule-f-003"></a>F-003 | ArcNotes complete scope | `USER_CONFIRMED` | [D-006](#rule-d-006) |
| <a id="rule-f-004"></a>F-004 | Verification policy for time-sensitive claims | `USER_CONFIRMED` | [D-003](#rule-d-003) |
| <a id="rule-f-005"></a>F-005 | Licensing boundary for ArcChat Mobile | `USER_CONFIRMED` | [D-004](#rule-d-004) |
| <a id="rule-f-006"></a>F-006 | Web technology and rendering boundary | `USER_CONFIRMED` | [D-007](#rule-d-007) |
| <a id="rule-f-007"></a>F-007 | Runtime and AOT matrix | `USER_CONFIRMED` | [D-008](#rule-d-008) |
| <a id="rule-f-008"></a>F-008 | Contract granularity | `USER_CONFIRMED` | [D-009](#rule-d-009) |
| <a id="rule-f-009"></a>F-009 | Cloud topology | `USER_CONFIRMED` | [D-010](#rule-d-010) |
| <a id="rule-f-010"></a>F-010 | Target monorepo | `USER_CONFIRMED` | [D-011](#rule-d-011) |
| <a id="rule-f-011"></a>F-011 | Reference-repository roles | `USER_CONFIRMED` | [D-012](#rule-d-012) |
| <a id="rule-f-012"></a>F-012 | Reuse policy | `USER_CONFIRMED` | [D-013](#rule-d-013) |
| [F-013](../assurance/open-gates-register.md#rule-f-013) | Reference-repository licences unknown | `DEFERRED_WITH_OWNER_AND_TRIGGER` | [D-013](#rule-d-013), [D-016](#rule-d-016) |
| <a id="rule-f-014"></a>F-014 | Payment provider baseline | `USER_CONFIRMED` | [D-005](#rule-d-005) |
| <a id="rule-f-015"></a>F-015 | Web and service surface inventory | `USER_CONFIRMED` | [D-014](#rule-d-014) |
| <a id="rule-f-016"></a>F-016 | Account portal URL | `USER_CONFIRMED` | [D-015](#rule-d-015) |
| <a id="rule-f-017"></a>F-017 | Deferred-decision ownership | `USER_CONFIRMED` | [D-016](#rule-d-016) |
| <a id="rule-f-018"></a>F-018 | Planning location and format | `USER_CONFIRMED` | [D-017](#rule-d-017) |
| <a id="rule-f-019"></a>F-019 | Normative glossary | `USER_CONFIRMED` | [D-018](#rule-d-018) |
| <a id="rule-f-020"></a>F-020 | Sequence status | `USER_CONFIRMED` | [D-019](#rule-d-019) |
| <a id="rule-f-021"></a>F-021 | AI and payment economic model | `USER_CONFIRMED` | [D-020](#rule-d-020) |
| <a id="rule-f-022"></a>F-022 | Apache boundary for validators and shared semantics | `USER_CONFIRMED` | [D-021](#rule-d-021) |
| [F-023](../assurance/open-gates-register.md#rule-f-023) | Mobile provenance and dependency closure | `DEFERRED_WITH_OWNER_AND_TRIGGER` | [D-004](#rule-d-004), [D-016](#rule-d-016) |
| <a id="rule-f-024"></a>F-024 | Mobile-store commerce | `USER_CONFIRMED` | [D-022](#rule-d-022) |
| <a id="rule-f-025"></a>F-025 | Mainland China payment route | `USER_CONFIRMED` | [D-023](#rule-d-023) |
| [F-026](../assurance/open-gates-register.md#rule-f-026) | Refit AOT packaging and entry-point change | `DEFERRED_WITH_OWNER_AND_TRIGGER` | [D-008](#rule-d-008), [D-016](#rule-d-016); discovered by [V-05c](../assurance/phase-1-official-verification.md#rule-v-05c) |

Totals: **26 registered** ([F-001](#rule-f-001) to [F-026](../assurance/open-gates-register.md#rule-f-026), every identifier used, none skipped) = **23 resolved** · **3 validly deferred** ([F-013](../assurance/open-gates-register.md#rule-f-013), [F-023](../assurance/open-gates-register.md#rule-f-023), [F-026](../assurance/open-gates-register.md#rule-f-026)) · **0 open** · **0 proposed**. One of the 26 was newly discovered during official verification ([F-026](../assurance/open-gates-register.md#rule-f-026)), deferred as an implementation gate rather than a foundation conflict.

---

# Resolved issues

## [F-001](#rule-f-001) — Conflict-resolution rule for the input corpus

**Type** `MISSING_DECISION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-001](#rule-d-001)

**Where** Not stated anywhere in `I1`–`I4`. Implied by `I2 §I` and by `I4 §Stage 13.93`.

**Input position** The corpus contains internal contradictions that later stages sometimes resolve silently. `I4 §Stage 2.1` reverses `§Stage 1.44` on the account-portal URL without saying so. `§Stage 13.36–41` amends `I3 §3.1` on cloud topology and says so explicitly. `I2 §I.2` declares `I3`'s product names obsolete. There was no stated rule for which wins.

**Outcome** The layered automatic precedence originally proposed here is `REJECTED`. Raw input documents carry no automatic precedence over one another and are evidence only. The confirmed rule and procedure are recorded at the head of this register.

## [F-002](#rule-f-002) — Product portfolio and the disposition of ArcCanvas, ArcMusic, ArcImage

**Type** `CONTRADICTION` + `MISSING_DECISION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-002](#rule-d-002)

**Where** `I4 §Stage 0.1`, `§0.14` list six-plus products; `§Stage 2.3` and `§2.20` place ArcCanvas and ArcMusic in navigation and docs; `§Stage 1.2` shows a six-product account diagram; `§Stage 13.1` freezes the portfolio to four and `§13.3` places ArcImage at "Not in Current Product Baseline"; `I3` line 5 and `§3` still describe ArcVideo and ArcImage as current.

**Outcome** Four desktop products only. ArcCanvas, ArcMusic and ArcImage are not current, future, reserved, alias or re-entry-candidate products.

## [F-003](#rule-f-003) — ArcNotes complete scope

**Type** `CONTRADICTION` (apparent) + `MISSING_DECISION` (depth) · **Status** `USER_CONFIRMED` · **Resolved by** [D-006](#rule-d-006)

**Where** `I4 §Stage 15` is titled "ArcNotes Complete Product Specification" and contains no Edgeless Canvas, no multi-view Database and no Slides; `§Stage 15.150` lists "Not complete Notion Database Platform" as a core non-goal; `§Stage 15.39` excludes relational database pages, formula engine, board engine, project management database and complex rollup. Stage 15 never mentions AFFiNE or SiYuan. `I2 §II` records the settled Option 5 decision, pre-empts the apparent contradiction ("'No Notion Database clone' means not replicating Notion's entire scope without limit"), and enumerates the V1 compatibility hooks.

**Original outcome — scope superseded by P2-006.** Option A was confirmed. Stage 15 was the V1 document-core baseline, not the ceiling. Canvas, typed multi-view Database and Slides are all in complete scope, phased after the document core stabilises, at ArcForges-decided depth via the Reference Coverage Matrix. The `I2 §II` V1 compatibility hooks are binding from the beginning. Slides defaults to a presentation view over document and canvas content.

## [F-004](#rule-f-004) — Verification policy for time-sensitive claims

**Type** `EXTERNAL_FACT` · **Status** `USER_CONFIRMED` · **Resolved by** [D-003](#rule-d-003), as amended by [D-005](#rule-d-005)

**Where** `I3` header line 4 carries a technical baseline verification date of **2026-07-20**; `I3 §32` requires updating ADRs, the AOT compatibility matrix and a real publish PoC before amending the baseline. `I4` was written around **2026-07-21**. This review is dated **2026-09-04**.

**Time-boxed claims identified**

| Claim | Source | Disposition |
|---|---|---|
| Claude Sonnet 5 promotional price reverts to $3/$15 per MTok on 2026-08-31 | `I4 §Stage 8.15` | Date passed. Invalidated as a frozen figure by **[D-020](#rule-d-020)**. |
| EU AI Act Article 50 applies from 2026-08-02 | `I4 §Stage 11.30` | **VERIFIED — V-01.** |
| MCP `2026-07-28` is a Release Candidate | `I4 §Stage 6.41` | **SUPERSEDED — V-02.** Now a stable release; the Stage 6 prohibition lapses on its own terms. |
| Waffo Pancake `Change Subscription Product` returns 501 | `I4 §Stage 3.17`, `§4.63` | Obsolete per **[D-005](#rule-d-005)**. Historical evidence only. Not verified and never to be verified. |
| Waffo WeChat Pay documented inconsistently | `I4 §Stage 3.5` | Obsolete per **[D-005](#rule-d-005)**. Historical evidence only. The `BillingProviderCapabilities` principle it motivated survives independently. |
| Azure Southeast Asia Zone-Redundant HA blocked for new deployments | `I4 §Stage 10.8` | Deferred. `§Stage 10.10` already mandates a Region Preflight re-check at provisioning time. |
| Pinned dependency versions | `I3 §2` | Partially re-verified — see **[V-05](../assurance/phase-1-official-verification.md#rule-v-05)**. Refit carries a material change (**[F-026](../assurance/open-gates-register.md#rule-f-026)**). |
| Android CoreCLR Native AOT not a stable production baseline; Mono AOT is production | `I3 §2.1`, `§29.6` | **VERIFIED — V-04.** |
| EF Core unsuitable as a strict-AOT production baseline | `I3 §2.1.4`, `§29.7` | **Moot for Cloud under [D-008](#rule-d-008)** — see V-05e. |
| ~30 pricing and quota figures | `I4 §Stages 0, 5, 8, 9, 10` | Deferred under [D-003](#rule-d-003)'s first-consumption rule; frozen figures invalidated by **[D-020](#rule-d-020)**. |

**Outcome** Foundation-critical verification only, executed and recorded in `docs/assurance/phase-1-official-verification.md`.

<a id="rule-d-003"></a>

### D-003 — current effective verification scope

This is the single active statement of [D-003](#rule-d-003)'s applied scope. It replaces the earlier applied-scope paragraph in full.

**Verified now against current official primary sources** (all complete — see the verification record):

1. EU AI Act Article 50 applicability and current Commission transparency guidance — **[V-01](../assurance/phase-1-official-verification.md#rule-v-01)**.
2. MCP `2026-07-28` specification status and the official C# SDK — **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)**.
3. .NET 10 ASP.NET Core Native AOT support and limitations — **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**.
4. .NET MAUI runtime and compilation status for Android and iOS — **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)**.
5. AOT evidence for Avalonia, StreamJsonRpc, Refit, SignalR and the dependency set consumed by an AOT deliverable — **[V-05](../assurance/phase-1-official-verification.md#rule-v-05)**.
6. **Paddle** — Merchant-of-Record role, supported regions, currencies, hosted checkout, subscriptions, webhooks, refunds and payment methods — **[V-06](../assurance/phase-1-official-verification.md#rule-v-06)**.
7. **Payoneer** — the supported Paddle-to-Payoneer payout relationship — **[V-07](../assurance/phase-1-official-verification.md#rule-v-07)**.
8. **Paddle mainland-China support**, including Alipay and WeChat Pay — **[V-08](../assurance/phase-1-official-verification.md#rule-v-08)**.
9. Current Apple App Store and Google Play rules for a free consumption-only companion application — **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)**.

**Deferred with a first-consumption trigger, not verified now:** all provider pricing, quotas, fee schedules, payout terms, storage and AI rates, exchange rates, tax rates, Azure regional availability tables, and store fee details. Consistent with `I3 §32` and `I4 §Stage 8.77`, which already forbid acting on an unreviewed price change. **Owner:** Commercial Operations Owner ([D-016](#rule-d-016)). **Trigger:** first authoritative pricing specification, and again before launch.

**Not a verification target.** Waffo Pancake is obsolete and `SUPERSEDED` under D-005. It must not be verified, recommended, integrated, or included in any new authoritative specification, roadmap, dependency, runtime component or implementation step. It survives in this register **only** in explicitly-labelled historical-evidence rows.

### Supersession history

**[D-005](#rule-d-005) replaced the Waffo Pancake item in [D-003](#rule-d-003)'s original applied verification worklist with Paddle and Payoneer.** The verbatim [D-003](#rule-d-003) decision block is unchanged, and every other part of [D-003](#rule-d-003) — its scope split, its deferral rule, and its first-consumption trigger — remains in force exactly as recorded. The scope statement above is the current effective form.

## [F-005](#rule-f-005) — Licensing boundary for ArcChat Mobile

**Type** `CONTRADICTION` — not raised anywhere in the corpus · **Status** `USER_CONFIRMED` · **Resolved by** [D-004](#rule-d-004)

**Where** `I4 §Stage 11.1` freezes a single `AGPL-3.0-only` licence for everything and explicitly rejects a "license platter"; `§Stage 11.11` chooses DCO over CLA on the stated grounds that there is no plan to relicense community contributions proprietarily; `§Stage 5.45` and `§5.48` ship ArcChat iOS through the App Store and TestFlight; `§Stage 12.91` plans App Store review prompts; `I2 §III.8` and `§III.13` keep iOS at `Planned / Build Deferred`.

**Why this mattered** GPL-family licences and the Apple App Store terms have a long-standing incompatibility: the store imposes usage and redistribution restrictions on the end user that the GPL family forbids adding. AGPLv3 is in the same family. Nothing in the corpus addresses this — Stage 11 was written about the server and desktop, Stage 5 about distribution channels, and the two were never checked against each other.

**Outcome** A two-boundary licensing rule replaces the single-licence statement.

**Register hygiene note** During drafting, a derived issue about shared-assembly licensing was prepared under the identifier [F-022](#rule-f-022) but **was never written to disk**. It is superseded in substance by D-004. It is recorded here only as a never-created draft; [F-022](#rule-f-022) below is a different, separately decided question.

## [F-006](#rule-f-006) — Web technology and rendering boundary

**Type** `CONTRADICTION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-007](#rule-d-007)

**Where** `I3 §18.1` and `§31` mandate Blazor WebAssembly with WASM AOT and rule out Blazor Server as a core mode. `I4 §Stage 2.27` requires the public marketing page to render above the fold *without JS/WASM fully started*, at LCP ≤2.5s / INP ≤200ms / CLS ≤0.1 (p75), and states that a marketing site must not require multi-MB WASM before Hero. Blazor WASM cannot satisfy that. `I2 §III.12` splits web into static site / account portal / chat companion and calls web a separate project, noting the static site "V0 can be built very early".

**Outcome** Static HTML/CSS for public pages; one interactive Blazor WebAssembly application; `RunAOTCompilation=false`; no Blazor Server circuits, no React/TypeScript/Node/JS package manager; minimal audited JS interop only where no adequate managed interface exists.

## [F-007](#rule-f-007) — Runtime and AOT matrix

**Type** `CONTRADICTION` / `NEEDS_OFFICIAL_VERIFICATION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-008](#rule-d-008)

**Where** `I3 §2.1`, `§16.2` and `§23.2` make Native AOT the Cloud baseline and forbid reflection-dependent paths; `I3 §24.1` and `I4 §Stage 27.54` make IL2026/IL3050 release-blocking. `I4 §Stage 10` then selects Azure SignalR Service, Azure Service Bus, Azure Key Vault, Managed Identity and OpenTelemetry exporters, none of which the corpus assesses for AOT or trimming compatibility. Azure SignalR Service is a different server code path from the in-box SignalR that `I3 §2.1.3` assessed.

**Verification** **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)** confirms the conflict is real and structural: under .NET 10, "Other Authentication", MVC, Blazor Server, OData, Session and Spa are **Not supported** under Native AOT; Minimal APIs and SignalR have only **Partial support**. **[V-04](../assurance/phase-1-official-verification.md#rule-v-04)** confirms Android CoreCLR is experimental and not intended for production in .NET 10.

**Outcome** Cloud is an ASP.NET Core **JIT** modular monolith; strict Native AOT is not a Cloud requirement. Desktop remains Native AOT. Android uses the supported .NET 10 Mono AOT path. Web uses Blazor WebAssembly with `RunAOTCompilation=false`. AOT release gates apply only to projects actually consumed by an AOT deliverable.

**Corpus correction recorded** `I3 §2.1.3`'s statement that SignalR is unsupported under AOT reflects the .NET 8 status. Under .NET 10 SignalR has Partial support ([V-03](../assurance/phase-1-official-verification.md#rule-v-03)). The decision is unaffected; the stale statement must not be carried forward unamended.

## [F-008](#rule-f-008) — Contract granularity

**Type** `CONTRADICTION` (mild) · **Status** `USER_CONFIRMED` · **Resolved by** [D-009](#rule-d-009)

**Where** `I3 §5.1` and `§5.3` define four shared Contracts projects with all LocalRpc interfaces in one assembly. `I3 §6.5` itself warns local contracts must stay small rather than becoming "one ever-expanding giant assembly". `I4 §Stage 21.122–123` requires per-product semantic ownership and versioning, so an ArcNotes contract change must not force an ArcSlate re-release. [D-004](#rule-d-004) adds the constraint that mobile-facing contracts must sit in clearly bounded Apache-2.0 packages.

**Outcome** Contracts split by communication boundary, product/domain ownership, release cadence and licence boundary. C# DTOs and endpoint metadata are the source of truth; OpenAPI and JSON Schema are generated from them. No business implementation in a contracts package.

**Verification consequence** **[V-05b](../assurance/phase-1-official-verification.md#rule-v-05b)** adds a contract-authoring obligation to this decision: every `[JsonRpcContract]` / `[RpcMarshalable]` interface must also carry `[GenerateShape(IncludeMethods = PublicInstance)]`, because that attribute — not the contract attribute alone — is what makes the proxy source-generated and therefore AOT- and trim-safe. Omitting it fails silently into a non-AOT-safe path.

## [F-009](#rule-f-009) — Cloud topology

**Type** `CONTRADICTION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-010](#rule-d-010)

**Where** `I3 §3.1` and `§3.2` route professional apps' cloud access through ArcChat; `I4 §Stage 13.36–41` amends this so professional apps reach Cloud directly and ArcChat is a control plane, not a data gateway. Under [D-001](#rule-d-001) internal corpus resolution is not self-authorising, so this required an explicit decision rather than automatic adoption of the later statement.

**Outcome** Direct product-to-Cloud communication. ArcChat is a control plane, never a mandatory data gateway. Cloud never connects to localhost, Named Pipes, Unix sockets or local stdio; it issues durable `ToolRequest`s that ArcChat Desktop pulls, re-authorizes locally, executes, and answers with an idempotent `ToolResult`. Same-machine first-party product-to-product communication remains StreamJsonRpc over Named Pipe/UDS.

## [F-010](#rule-f-010) — Target monorepo

**Type** `MISSING_DECISION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-011](#rule-d-011)

**Where** `I3 §5.1` proposes a repository layout containing `ArcVideo/` and `ArcImage/`, both `SUPERSEDED` by D-002. The Phase 1 brief states `C:\MyFile\ArcForges\ArcForges` already contains implementation code and must not dictate the design.

**Outcome** The implementation target is the existing monorepo. `ArcForges-Design` is the sole authoritative requirements, architecture and planning repository and contains no product source code. The implementation repository is inspected only in the later code-reading and reconciliation phase.

## [F-011](#rule-f-011) — Reference-repository roles

**Type** `UNSUPPORTED_ASSUMPTION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-012](#rule-d-012)

**Where** `I4 §Stage 15` never mentions AFFiNE or SiYuan; `§Stage 16` never mentions Serial Studio; `§Stage 20` mentions only Olive, never ArcVideo or ArcVideoFoundation. All reference-repository roles came solely from `I2 §II` and the Phase 1 brief's inventory.

**Outcome** The reference map is confirmed explicitly rather than inferred. Reference repositories are sources of features, behaviour, tests, migration evidence and possible reusable material — never architecture authorities, parity commitments, or reasons to import a runtime stack. Every product receives a Reference Coverage Matrix before its implementation planning is finalized.

## [F-012](#rule-f-012) — Reuse policy

**Type** `USER_INTENT` / `MISSING_DECISION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-013](#rule-d-013)

**Where** `I2 §II` states as user-confirmed that non-AGPL content from AFFiNE, Serial Studio, ArcVideo, ArcVideoFoundation and Olive may be copied — code, logic, tests and assets — then progressively replaced. Its interaction with the `I4 §Stage 11.5–7` licence traffic lights (GPL-2.0-only and unknown-origin code are `RED`) was unstated. [D-004](#rule-d-004) adds a hard constraint on the mobile side.

**Outcome** Copy First is retained only as a **licence-gated and provenance-gated** strategy; unconditional copying is rejected. A nine-field provenance record is required before any reuse.

## [F-014](#rule-f-014) — Payment provider baseline

**Type** `CANDIDATE_ARCHITECTURE` + `NEEDS_OFFICIAL_VERIFICATION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-005](#rule-d-005)

**Where** `I4 §Stage 3` selects Waffo Pancake as sole customer-facing Merchant of Record and builds the entire Stage 3 commercial surface on it. `§Stage 3.37` records the provider risk directly. `§Stage 3.5` records that its own documentation contradicted itself on WeChat Pay. `§Stage 3.38` and `§Stage 4.62` nevertheless design for provider replaceability from the outset.

**Outcome** Waffo Pancake is removed. Paddle is the sole customer-facing Merchant of Record for web and cloud commerce (**VERIFIED — [V-06](../assurance/phase-1-official-verification.md#rule-v-06)**); Payoneer is the payout and settlement destination (**VERIFIED — [V-07](../assurance/phase-1-official-verification.md#rule-v-07)**).

**What survives from `I4 §Stage 3` and `§Stage 4`** The provider-independent commercial domain model, which was designed to outlive any provider and does: `BillingProviderCapabilities`; Billing Account separate from User; Offer / Product Scope / Price Version / Regional Price; Purchase Intent → Checkout Attempt → Order → Payment; a stable internal billing identity used as buyer identity rather than email; checkout metadata carrying internal IDs; success-redirect never treated as payment authority; Provider Event Inbox with signature verification and `eventType + eventId` idempotency; periodic reconciliation as the second line of defence; normalised internal subscription states with `ExternalProviderStatus` retained for diagnostics; entitlement driven by `PaidThrough` rather than raw provider status; Grant plus Revocation rather than mutable flags; Credit Lots with refund holds; Commercial Evidence retention; and the rule that provider IDs never reach the client.

[V-08](../assurance/phase-1-official-verification.md#rule-v-08) makes `BillingProviderCapabilities` load-bearing rather than precautionary: Alipay and WeChat Pay differ from each other and from cards on subscription support, currency, platform, chargeback availability and transaction caps.

**Historical evidence only** Every Waffo-specific mechanic — its fee schedule and single-transaction caps, its WeChat Pay route and the USD-one-time-product constraint that came with it, its refund-ticket window and per-refund fee, its chargeback fee ladder, its merchant-review prerequisites, its mainland-China personal KYC path, its RMB payout to bank card or Alipay, its API signing scheme, its Consumer Portal, and its 501-returning plan-change endpoint — is obsolete and superseded.

## [F-015](#rule-f-015) — Web and service surface inventory

**Type** `MISSING_DECISION` (minor) · **Status** `USER_CONFIRMED` · **Resolved by** [D-014](#rule-d-014)

**Where** Ten surfaces accumulate across stages with no single list: `arcforges.com`, `account.`, `docs.`, `status.`, `api.` (`§Stage 2.51`); `chat.` (`§Stage 7.54`); `downloads.`, `updates.` (`§Stage 5`); `ops.` (internal), `notify.`, `news.` (`§Stage 10.127`). Additive, not contradictory.

**Outcome** A twelve-entry consolidated inventory, with the explicit rule that a hostname is not an application: Account and Chat may be separately deployed configurations of the same `ArcForges.Web.App` codebase, and static surfaces remain static artifacts.

## [F-016](#rule-f-016) — Account portal URL

**Type** `CONTRADICTION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-015](#rule-d-015)

**Where** `I4 §Stage 1.44` prefers `arcforges.com/account`; `§Stage 2.1` formally chooses `account.arcforges.com` with `arcforges.com/account` as a permanent redirect. Reopened under [D-001](#rule-d-001) because internal corpus resolution is not self-authorising.

**Outcome** `account.arcforges.com` is canonical; `arcforges.com/account` is a permanent redirect and must not become a second account application. Explicit origin, cookie, OAuth redirect, CSP, CSRF and CORS boundaries; no broad parent-domain authentication cookies.

## [F-017](#rule-f-017) — Deferred-decision ownership

**Type** `MISSING_DECISION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-016](#rule-d-016)

**Where** The corpus names no owners. The Phase 1 completion gate requires every deferred decision to carry a valid owner and trigger. [F-013](../assurance/open-gates-register.md#rule-f-013) and [F-023](../assurance/open-gates-register.md#rule-f-023) previously named the user as owner by default, which [D-016](#rule-d-016) explicitly rejects as an operational model.

**Outcome** Six durable responsibility roles, with the user/Product Owner as final approval authority where a product decision is required. Every deferred item carries a role, a trigger, an earliest consumer, required evidence, and a stated failure consequence.

## [F-018](#rule-f-018) — Planning location and format

**Type** `OBSOLETE` / `MISSING_DECISION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-017](#rule-d-017)

**Where** `I2` lines 5–6 and `§VI` name `ArchitectureDesign\ArcForgesReWrite-AllCsharp` as the output location and `ArchitectureDesign\AionUiReWrite-Kotlin` as the format reference. Neither is in the declared inventory. The format *contract* is self-contained: `I2 §VI` lists the required per-step fields directly.

**Outcome** Five fixed output directories inside `ArcForges-Design`. The old `ArchitectureDesign` locations are obsolete, must never be used as an output or authority, and must not be accessed or depended on. The `AionUiReWrite-Kotlin` material is not an input corpus or authority.

## [F-019](#rule-f-019) — Normative glossary

**Type** `MISSING_DECISION` · **Status** `USER_CONFIRMED` · **Resolved by** [D-018](#rule-d-018)

**Where** The corpus defines roughly 600 named domain concepts and asserts roughly 250 `X ≠ Y` invariants across Stages 13–28. These invariants are the corpus's highest-value content and cannot be enforced without a single normative glossary. Overloaded terms needing particular care: **Workspace** (cloud ownership boundary versus panel layout — `§Stage 14.95` and `§Stage 20.166` mandate "Layout" for the latter), **Project** (ArcChat / ArcScope / ArcSlate — namespaced `ResourceKind` in `§Stage 21.54`), and **Scope** (Knowledge, Sync, Permission, Policy, Product, Search, Egress, Resource — each defined separately, never consolidated).

**Outcome** A single normative glossary and invariant catalogue is a mandatory foundation-to-specification gate. Not generated in Phase 1.

**Verification consequence** **[V-02](../assurance/phase-1-official-verification.md#rule-v-02)** adds a term-collision risk from outside the corpus: MCP's extension framework defines **Tasks** and **Skills**, which overlap the ArcForges `Task / Run / Step / Attempt` vocabulary from `I4 §Stage 19`. The glossary must disambiguate MCP-`Task` from ArcForges-`Task` explicitly.

## [F-020](#rule-f-020) — Sequence status

**Type** `SEQUENCING_PROPOSAL` · **Status** `USER_CONFIRMED` · **Resolved by** [D-019](#rule-d-019)

**Where** `I2`'s 14-item "Final Recommended Sequence" and `I3 §28`'s Phase 0–8 are proposals. `I2 §I.1` states Stage 0–28 is decision order, not build order, and `I2 §I.2` declares `I3`'s legacy Phase 3 and Phase 4 inapplicable to the current portfolio. The Phase 1 brief forbids assuming an earlier plan's step count or structure is still valid.

**Outcome** All corpus sequences are planning evidence only. One serial numbered sequence `00 → 01 → … → NN` with no predetermined maximum. Interleaving by real dependency gates. One main context advances the sequence serially.

## [F-021](#rule-f-021) — AI and payment economic model

**Type** `EXTERNAL_FACT` · **Status** `USER_CONFIRMED` · **Resolved by** [D-020](#rule-d-020)

**Where** `I4 §Stage 8` derives the ~1.6× retail multiplier, the 1,000-credit monthly allowance and the $10/$25/$50 pack economics from provider prices captured on 2026-07-21, at least one of which — the Claude Sonnet 5 promotional rate — has already expired. `§Stage 8.10`'s net figures of $9.02 / $23.29 / $47.07 were computed from the removed provider's fee schedule and payout rate.

**Outcome** The provider-independent accounting model is preserved. Every frozen number derived from expired model pricing or the removed provider's fees is invalidated and removed from the authoritative baseline, and is **not** replaced with new frozen numbers in Phase 1. Prices, allowances, pack sizes, margins and regional amounts become versioned commercial policy requiring approval at first specification consumption and again before launch.

## [F-022](#rule-f-022) — Apache-2.0 boundary for validators, application semantics and base ViewModel patterns

**Type** `MISSING_DECISION`, arising from [D-004](#rule-d-004) · **Status** `USER_CONFIRMED` · **Resolved by** [D-021](#rule-d-021)

**Where** `I3 §17.2` states what the mobile client shares: "Shared: Foundation/PublicApi/Realtime DTOs, validators, pure application semantics, and base ViewModel patterns. Not shared: Avalonia XAML, desktop Window/Dispatcher, StreamJsonRpc LocalRpc Contracts, desktop IPC, and desktop native handles."

**Why this needed a decision** [D-004](#rule-d-004)'s Apache-2.0 boundary covers the mobile application, mobile-only libraries, public protocol specifications required for mobile interoperability, and the corresponding wire schemas, DTOs and client libraries. Validators, pure application semantics and base ViewModel patterns are none of those four categories obviously — they are shared implementation, not protocol. [D-004](#rule-d-004) also forbids any AGPL-only implementation entering ArcChat Mobile by any route, so their classification determines whether they may be shared with mobile at all.

**Outcome** Option C confirmed and refined. The boundary is drawn around **interoperability**: contract-level validation belongs with the schema it enforces; product and server business behaviour stays in its owning AGPL implementation; mobile-only application behaviour is implemented independently inside the Apache mobile boundary. **Base ViewModel patterns are not shared between Avalonia desktop and MAUI mobile at all** — each UI stack owns its implementation.

## [F-024](#rule-f-024) — Mobile-store commerce

**Type** `MISSING_DECISION`, arising from [D-005](#rule-d-005) · **Status** `USER_CONFIRMED` · **Resolved by** [D-022](#rule-d-022)

**Where** `I4 §Stage 3.44` positions ArcChat Mobile as a free companion that may log in, view plan, use existing Cloud entitlement and credits, and view remote agent and task state — but may not buy, present a checkout link, or steer to an external purchase. `§Stage 5.50` holds the Microsoft Store to distribution only. `§Stage 4.61` already models Apple and Google in-app purchases as producing ordinary Entitlement Grants.

**Verification** **[V-09](../assurance/phase-1-official-verification.md#rule-v-09)** confirms both storefronts permit the chosen posture. Apple 3.1.3(f) exempts free stand-alone companions to a paid web-based tool "provided there is no purchasing inside the app, or calls to action for purchase outside of the app". Google states verbatim: "Google Play allows any app to be consumption-only, even if it is part of a paid service. For example, a user could log in when the app opens and access content paid for somewhere else." Apple 3.1.1 additionally bans unlocking via licence keys, which independently confirms one of [D-022](#rule-d-022)'s prohibitions.

**Outcome** Option A globally for the initial product: free companion / consumption-only, all commerce on the web through Paddle, the same conservative behaviour across storefronts, and the entitlement architecture kept capable of accepting a future store-originated grant without implementing one.

## [F-025](#rule-f-025) — Mainland China payment route

**Type** `MISSING_DECISION`, newly exposed by [D-005](#rule-d-005) · **Status** `USER_CONFIRMED` · **Resolved by** [D-023](#rule-d-023)

**Where** `I4 §Stage 3` built the entire mainland-China commercial route on the removed provider: `§Stage 3.4` routed Chinese users to WeChat Pay for Cloud Pass and AI Credits as one-time USD products; `§Stage 3.6` forbade inventing a fixed CNY price because that provider offered no real CNY product pricing; `§Stage 3.32`–`§3.35` described mainland personal KYC and RMB payout to a bank card or Alipay; `§Stage 3.50` froze the arrangement. `§Stage 2.26` separately defers mainland-China network infrastructure.

**Verification** **[V-08](../assurance/phase-1-official-verification.md#rule-v-08)** establishes the real capability set. Alipay: one-time and subscriptions supported, CNY only, 1,600 CNY cap on renewals and charges, separate Paddle approval required, no chargebacks, no saved payment methods. WeChat Pay: one-time only — **no subscriptions** — CNY or USD, **desktop only**, no configuration required, no chargebacks, no saved payment methods. Neither requires a Chinese entity or a provider merchant account.

**Two corrections to the corpus, both absorbed by [D-023](#rule-d-023) without amendment**

1. **CNY pricing inverts from forbidden to required.** `§Stage 3.6` forbade a fixed CNY price. Paddle's Alipay route requires CNY-priced products and conditions approval on it. [D-023](#rule-d-023)'s "CNY product and tax configuration" gate already carries this.
2. **The cap changed shape.** The corpus recorded ~$140 / ¥1,000 single-transaction for the removed provider; Paddle's Alipay cap is 1,600 CNY on subscription renewals and charges. [D-023](#rule-d-023)'s instruction not to hard-code caps already carries this.

**Outcome** Mainland China is a conditional launch market. No second payment provider for V1. Paddle-hosted checkout with Alipay, WeChat Pay and available cards; Payoneer as payout only. Cloud Pass remains the non-recurring fixed-term product — a requirement made concrete by [V-08](../assurance/phase-1-official-verification.md#rule-v-08), since WeChat Pay users cannot subscribe at all and Alipay users hit a renewal ceiling. Eight pre-enablement gates; on failure, disable regional sales by explicit policy without blocking global launch and without silently substituting another provider.

---

# Deferred issues

Each carries a responsible role, a concrete trigger, the earliest consumer, required evidence, and the consequence if the gate fails — per **[D-016](#rule-d-016)**.

## [F-013](../assurance/open-gates-register.md#rule-f-013) — Reference-repository licences unknown

**Status** `DEFERRED_WITH_OWNER_AND_TRIGGER` · **Governed by** [D-013](#rule-d-013), [D-016](#rule-d-016)

**Where** AionUi is corrected to **Apache-2.0** in `I4 §Stage 6.77` (previously believed MIT) — one-way compatible into AGPL with attribution and NOTICE. Serial Studio's licence is stated nowhere in the corpus; `I2 §II` requires file-level SPDX verification against the local repository baseline, not the repository-root licence or an external page. AFFiNE's licence is stated nowhere. Olive is GPL-family. Phase 1 forbids inspecting these repositories.

| Field | Value |
|---|---|
| **Responsible role** | Licensing and Provenance Owner |
| **Final approval** | Product Owner, where a product decision is required |
| **Trigger** | Before any reference material is reused — the first step of the per-product Reference Coverage Matrix and licence audit |
| **Earliest consumer** | `I2 §III.0` "Specification and Rights Freeze" |
| **Required evidence** | File-level SPDX and licence evidence against the local repository baseline; exact commit; copyright and attribution obligations; NOTICE requirements |
| **Failure consequence** | The material is classified Reference Only or Drop. It must not be copied, translated or ported. Per [D-013](#rule-d-013), GPL-only, licence-unclear and unknown-origin material may be used only as controlled behavioral evidence until an explicit compatibility decision says otherwise. |

## [F-023](../assurance/open-gates-register.md#rule-f-023) — Mobile provenance and dependency-closure verification

**Status** `DEFERRED_WITH_OWNER_AND_TRIGGER` · **Governed by** [D-004](#rule-d-004), [D-016](#rule-d-016)

**Where** [D-004](#rule-d-004): "The current decision assumes that ArcChat Mobile and its required interoperability code are ArcForges-owned and contain no GPL-family code. Verify provenance and the complete dependency closure before distribution."

The audit is **not** complete and must not be described as complete.

| Field | Value |
|---|---|
| **Responsible roles** | Release Engineering Owner **and** Licensing and Provenance Owner |
| **Final approval** | Product Owner |
| **Trigger** | Before the first App Store, TestFlight, Google Play or sideloadable ArcChat Mobile artifact is produced |
| **Earliest consumer** | Mobile packaging and signing — `I2 §III.8`, and again at `§III.13` |
| **Required evidence** | Ownership or Apache-2.0-compatible licence for the application, mobile-only libraries, packaging and platform integrations, and every Apache-2.0 interoperability package consumed; complete **direct and transitive** dependency closure compatible with Apache-2.0 application distribution and applicable store terms; passing automated architecture and dependency checks per [D-004](#rule-d-004) obligation 7 |
| **Failure consequence** | Per [D-004](#rule-d-004), register that specific issue and return it for decision. **Never** silently add an exception, change the licence, or remove the mobile distribution target. |

## [F-026](../assurance/open-gates-register.md#rule-f-026) — Refit AOT packaging and entry-point change

**Status** `DEFERRED_WITH_OWNER_AND_TRIGGER` · **Governed by** [D-008](#rule-d-008), [D-016](#rule-d-016) · **Discovered by** [V-05c](../assurance/phase-1-official-verification.md#rule-v-05c)

**Newly discovered during official verification.** Not a foundation-critical conflict — it changes no decision above — but it is implementation-critical and the corpus does not record it.

**Finding** `I3 §2` pins Refit 13.1.0 and says nothing about how Refit is consumed under AOT. Since Refit 12.0 the source generator builds requests inline at compile time, and two consequences follow that a naive implementation would miss: the **reflection request builder has moved out of the main package** into `Refit.Reflection`, signalled by diagnostic **`RF006`** — adding that package reintroduces exactly the reflection dependency an AOT deliverable must avoid; and **`RestService.ForGenerated<T>`** is the AOT-safe entry point, not `RestService.For<T>`. Some hot-path async members now return `ValueTask` instead of `Task`. Refit 14 is a later line focused on request-generation correctness.

| Field | Value |
|---|---|
| **Responsible role** | Owning platform work-package owner |
| **Final approval** | Architecture Owner |
| **Trigger** | Before accepting Refit into an AOT deliverable |
| **Earliest consumer** | The first desktop work package that calls a public HTTP API |
| **Required evidence** | Deliberate version pin at first consumption; `RestService.ForGenerated<T>` used throughout; `Refit.Reflection` absent from every AOT deliverable; `RF006` treated as build-breaking in AOT projects; a clean AOT publish with zero IL2026/IL3050 warnings |
| **Failure consequence** | Refit is not accepted into that deliverable. Either the offending interface shapes are changed so the generator can handle them, or an alternative typed-client approach is chosen for that surface. Do not add `Refit.Reflection` to make the build pass. |

---

# Decision log

Decisions are recorded verbatim as given by the user. Each cites the issue it resolves.

---

<a id="rule-d-001"></a>

## D-001 — Conflict-resolution rule · resolves **[F-001](#rule-f-001)** · `USER_CONFIRMED`

> Do not establish automatic precedence among the raw input documents.
>
> The authority order is:
>
> 1. Current explicit user decisions.
> 2. The user-confirmed Phase 1 decision register.
> 3. Raw input documents as evidence of prior intent and exploration only.
> 4. Current official primary sources for externally verifiable facts.
>
> Sequencing notes, later stages, the architecture concept, and the overview do not automatically override one another. A later or apparently more specific statement may be evidence of intended evolution, but it is not authoritative until reviewed.
>
> For every material conflict:
>
> - register it;
> - explain the likely evolution;
> - provide the viable alternatives and recommendation;
> - obtain a user decision;
> - record the disposition;
> - apply that confirmed disposition consistently afterward without asking the same question again.
>
> Submitting this answer confirms this conflict-resolution rule. Apply every confirmed global disposition to all occurrences it covers without asking again. Bring back only new material conflicts that are not already covered by an existing user decision.

---

<a id="rule-d-002"></a>

## D-002 — Product baseline · resolves **[F-002](#rule-f-002)** · `USER_CONFIRMED`

> The current product baseline contains exactly four desktop products: ArcChat, ArcNotes, ArcScope, and ArcSlate.
>
> ArcCanvas, ArcMusic, and ArcImage are not current products, future products, reserved products, aliases, or re-entry candidates. Mark every occurrence in the raw inputs as obsolete and SUPERSEDED. Do not create any database, runtime component, dependency, navigation entry, contract, specification, roadmap item, or implementation step for them.
>
> Preserve the raw input files unchanged, but exclude these three product names from every new authoritative document.
>
> ArcScope is an independently defined product, not a rename or continuation of ArcImage. ArcNotes Edgeless Canvas is an ArcNotes capability, not a standalone ArcCanvas product.

---

## [D-003](#rule-d-003) — Verification scope · resolves **[F-004](#rule-f-004)** · `USER_CONFIRMED`

> Foundation-critical only (Recommended)

The current effective applied scope of this decision is recorded under **[F-004](#rule-f-004)**, together with the [D-005](#rule-d-005) supersession history. The verbatim decision block above is unchanged.

---

<a id="rule-d-004"></a>

## D-004 — ArcChat Mobile licensing boundary · resolves **[F-005](#rule-f-005)** · `USER_CONFIRMED`

> ArcChat Mobile shall be licensed under Apache-2.0, not AGPL-3.0-only.
>
> The Apache-2.0 boundary includes:
>
> - the ArcChat Mobile application;
> - mobile-only libraries, tests, packaging, and platform integrations;
> - the ArcForges-owned public protocol specifications required for mobile interoperability;
> - the corresponding wire schemas, DTOs, and generated or handwritten client libraries used by ArcChat Mobile.
>
> If the mobile-facing contracts currently reside inside a broader AGPL-only project, separate them into clearly bounded Apache-2.0 projects or packages. AGPL desktop and server components may consume these Apache-2.0 contracts without changing their own licences.
>
> ArcChat Mobile must not contain, link to, copy from, port from, or reference any GPL-family or AGPL-only implementation. Its complete direct and transitive dependency closure must be compatible with Apache-2.0 application distribution and the applicable mobile app stores.
>
> Communication with ArcForges Desktop or ArcForges Cloud through the independently defined ArcForges wire protocols and APIs does not change the mobile client’s licence. Desktop and server implementations remain separate works across explicit process or network boundaries.
>
> The following remain AGPL-3.0-only:
>
> - ArcChat Desktop;
> - ArcNotes;
> - ArcScope;
> - ArcSlate;
> - ArcForges Cloud and all server implementations;
> - all other components not explicitly assigned to the Apache-2.0 mobile/interoperability boundary.
>
> No App Store exception, dual licensing, proprietary grant, or CLA shall be introduced for ArcChat Mobile. Continue using DCO with inbound-equals-outbound licensing: Apache-2.0 for contributions to the Apache-2.0 scope and AGPL-3.0-only for contributions to the AGPL scope.
>
> Replace the previous global statement that the entire product family is AGPL-3.0-only with an explicit two-boundary licensing rule. Update all affected architecture invariants, licensing documentation, SPDX identifiers, package metadata, LICENSE/NOTICE handling, contribution guidance, dependency checks, SBOM rules, and repository-policy tests accordingly.
>
> Add automated architecture and dependency checks preventing GPL-family or AGPL-only source, project references, packages, generated artifacts, and transitive dependencies from entering the ArcChat Mobile distributable.
>
> The current decision assumes that ArcChat Mobile and its required interoperability code are ArcForges-owned and contain no GPL-family code. Verify provenance and the complete dependency closure before distribution. If a conflicting contribution or dependency is discovered, register that specific issue and return it for decision; do not silently add an exception, change the licence, or remove the mobile distribution target.
>
> This decision is final for Phase 1 and must be applied consistently to all later planning documents.

### [D-004](#rule-d-004) obligations carried into the specification phase

| # | Obligation | Surface |
|---|---|---|
| 1 | Replace the global "entire product family is AGPL-3.0-only" statement with an explicit two-boundary licensing rule | Licensing documentation; architecture invariants |
| 2 | Separate mobile-facing contracts out of any broader AGPL-only project into clearly bounded Apache-2.0 projects or packages | Solution and project layout; governed by [D-009](#rule-d-009) |
| 3 | Update SPDX identifiers and package metadata across both boundaries | Every project and package |
| 4 | Update LICENSE and NOTICE handling for the two-boundary model | Repository root; per-package |
| 5 | Update contribution guidance for DCO with inbound-equals-outbound per scope | `CONTRIBUTING.md` |
| 6 | Update dependency checks and SBOM rules for the two-boundary model | CI; release pipeline |
| 7 | Add automated architecture and dependency checks preventing GPL-family or AGPL-only source, project references, packages, generated artifacts and transitive dependencies from entering the ArcChat Mobile distributable | ArchitectureTests; repository-policy tests; CI gates |
| 8 | Verify provenance and the complete direct and transitive dependency closure before distribution | Tracked as **[F-023](../assurance/open-gates-register.md#rule-f-023)** |

---

<a id="rule-d-005"></a>

## D-005 — Payment provider baseline · resolves **[F-014](#rule-f-014)** · `USER_CONFIRMED`

> Waffo Pancake is not part of the current ArcForges payment architecture. It is obsolete and SUPERSEDED as a provider choice. Do not verify it, recommend it, create an integration for it, or include it in any new authoritative specification, roadmap, dependency, runtime component, or implementation step.
>
> Preserve the raw input files unchanged. Existing Waffo Pancake references in the raw corpus remain historical evidence only and must be classified as obsolete and superseded.
>
> The current payment-provider baseline is:
>
> 1. Paddle is the sole customer-facing Merchant of Record for ArcForges web and cloud commerce. It owns checkout, subscriptions, recurring billing, applicable sales-tax/VAT handling, compliant invoices, refunds, chargebacks, and payment webhooks.
>
> 2. Payoneer is the selected payout and settlement destination for receiving Paddle payouts. It is not a second Merchant of Record, not an interchangeable checkout provider, and not a customer-facing fallback payment processor.
>
> 3. Preserve the provider-abstraction principles already identified as sound: entitlement state remains independent of provider identifiers; provider IDs do not enter client authority contracts; webhooks are verified and idempotent; and the architecture must not depend irreversibly on one provider’s proprietary data model.
>
> Apply this as a global disposition. Mark [F-014](#rule-f-014) USER_CONFIRMED and resolved by D-005.
>
> Do not rewrite or alter the verbatim [D-003](#rule-d-003) decision block. Add a clear supersession note stating that [D-005](#rule-d-005) replaces only the Waffo Pancake part of [D-003](#rule-d-003)’s applied verification worklist. The current verification target is Paddle and Payoneer, using current official primary sources. Verify their current availability, onboarding eligibility, supported regions and currencies, payout relationship, API/webhook capabilities, and any implementation-critical restrictions. Pricing and fees remain time-sensitive and must follow [D-003](#rule-d-003)’s first-consumption rule.
>
> Register a separate open issue for the mobile-store commerce boundary. Paddle and Payoneer being selected for web/cloud commerce does not by itself decide whether ArcChat Mobile is a free companion with no in-app purchasing, uses Apple/Google in-app purchasing, or may expose an external purchase path in particular storefronts. Do not decide that issue silently and do not assume Paddle checkout may be embedded in every mobile-store build.

---

<a id="rule-d-006"></a>

## D-006 — ArcNotes complete scope · resolves **[F-003](#rule-f-003)** · `USER_CONFIRMED`

> Confirm Option A.
>
> Stage 15 is the ArcNotes V1 document-core baseline, not the ceiling of the complete ArcNotes product.
>
> ArcNotes Edgeless Canvas, typed multi-view Database and Slides are all part of the complete ArcNotes scope and must be delivered in phases after the document core stabilises.
>
> “Incorporate in full, in phases” means that all three capability families are in scope. It does not mean feature-for-feature parity with AFFiNE, SiYuan, Notion or any other external product.
>
> The depth of each feature is decided by the ArcNotes Reference Coverage Matrix using Copy, Rewrite, Improve, Replace, Reference Only or Drop.
>
> The V1 compatibility hooks listed in I2 are binding from the beginning. Do not create fake empty Canvas, Database or Slides implementations.
>
> Slides should default to a presentation view over document and canvas content rather than a third incompatible content model, unless a later confirmed specification demonstrates a real need otherwise.
>
> Mark [F-003](#rule-f-003) USER_CONFIRMED and resolved by D-006.

**V1 compatibility hooks made binding by this decision** (from `I2 §II`): stable Document/Space and Block IDs with revisions and unified reference semantics; a Block model that allows later addition of Surface/Canvas types; canvas spatial positions, connectors, groupings and layout data isolated from normal document layout; typed properties, queries and saved views as the multi-view Database foundation; no stuffing of future fields into the core Block; no fake empty Canvas, Database or Slides implementations; static registration or source generation for block and extension types under AOT; and `DocumentId/BlockId/Operation/Revision` preserving future collaboration compatibility from the start.

---

### [D-006](#rule-d-006) amendment — 2026-09-06

**Current effective scope:** [P2-006](phase-2-specification-decisions.md#rule-p2-006) removes Edgeless Canvas, Slides/Presentation and future-collaboration hooks from required ArcNotes delivery. Notebook core, bounded typed properties, saved list/table views, queries, references and multi-device cloud sync remain. No reference feature automatically expands scope. The original quotation above is preserved for provenance.

---

<a id="rule-d-007"></a>

## D-007 — Web technology and rendering boundary · resolves **[F-006](#rule-f-006)** · `USER_CONFIRMED`

> The public marketing experience must render as static HTML and CSS without waiting for the .NET runtime or WebAssembly to start. Marketing, legal, download and other public information pages must not boot Blazor merely to display their initial content.
>
> The only interactive browser application is ArcForges.Web.App, implemented as standalone Blazor WebAssembly for authenticated account and ArcChat companion experiences.
>
> Static public pages may be hand-authored or generated at build time by C#/.NET tooling. They are static deployment artifacts, not a second browser application.
>
> Do not use Blazor Server circuits, Interactive Server, runtime server-side rendering, React, TypeScript, Node or a JavaScript package manager.
>
> Set RunAOTCompilation=false for the Blazor WebAssembly application unless a future measured benchmark and explicit decision proves that WASM AOT’s larger download is justified.
>
> Minimal audited JavaScript interop remains allowed only where the browser or a required provider has no adequate managed interface.
>
> Mark [F-006](#rule-f-006) USER_CONFIRMED and resolved by D-007.

---

<a id="rule-d-008"></a>

## D-008 — Runtime and AOT matrix · resolves **[F-007](#rule-f-007)** · `USER_CONFIRMED`

> ArcForges Cloud is an ASP.NET Core JIT modular monolith. Strict Native AOT is not a Cloud requirement.
>
> Azure SDKs, the durable agent loop, provider adapters, SignalR integration, billing, policy and operational infrastructure run inside the JIT Cloud boundary.
>
> Desktop applications remain Native AOT deliverables and must retain trim/AOT-safe dependency rules.
>
> ArcChat Mobile Android uses the supported .NET 10 Mono AOT release path. Experimental Android CoreCLR and experimental Android NativeAOT are not production baselines.
>
> The iOS architecture remains present and complete but its build is deferred. Its eventual release runtime must be reverified against the then-current supported MAUI/iOS baseline.
>
> ArcForges Web uses standalone Blazor WebAssembly with RunAOTCompilation=false.
>
> Only projects actually consumed by an AOT deliverable must satisfy AOT release gates. Shared public contracts and client libraries consumed by desktop/mobile must remain trim-safe and source-generation friendly.
>
> Remove obsolete claims that Cloud must publish as Native AOT. Do not spend Phase 1 proving Azure SDK Native AOT compatibility for a server that is now explicitly JIT.
>
> Mark [F-007](#rule-f-007) USER_CONFIRMED and resolved by D-008.

**Instruction honoured.** No Azure SDK Native AOT verification was attempted ([V-05e](../assurance/phase-1-official-verification.md#rule-v-05e)).

---

<a id="rule-d-009"></a>

## D-009 — Contract granularity · resolves **[F-008](#rule-f-008)** · `USER_CONFIRMED`

> Reject a single ever-growing contracts assembly.
>
> Split contracts by communication boundary, product/domain ownership, release cadence and licence boundary.
>
> Use the following governing structure:
>
> - Apache-2.0 public/interoperability packages:
>   - stable serialized identifiers and primitives;
>   - mobile-facing Public API contracts;
>   - mobile-facing realtime contracts;
>   - wire schemas and generated clients;
>   - public SDK contracts and contract-level validators.
> - AGPL-3.0-only contracts:
>   - first-party LocalRpc contracts, split by owning product or independently versioned capability;
>   - Cloud-internal contracts;
>   - implementation-only interfaces and domain internals.
>
> A contract change owned by ArcNotes must not require an unrelated ArcSlate contract release.
>
> C# DTOs and endpoint metadata are the source of truth. Generate OpenAPI and JSON Schema compatibility artifacts from them. Do not maintain parallel handwritten schemas that can drift.
>
> No business implementation belongs in a contracts package.
>
> Mark [F-008](#rule-f-008) USER_CONFIRMED and resolved by D-009.

---

<a id="rule-d-010"></a>

## D-010 — Cloud topology · resolves **[F-009](#rule-f-009)** · `USER_CONFIRMED`

> Professional desktop products communicate directly with ArcForges Cloud for their own identity, sync, storage and product-domain APIs.
>
> ArcChat is a control plane and user-facing agent client. It is not a mandatory data gateway or proxy for ArcNotes, ArcScope or ArcSlate.
>
> Cloud must never connect directly to localhost, Named Pipes, Unix sockets or local stdio.
>
> When Cloud needs a local action, it creates a durable ToolRequest. ArcChat Desktop pulls it, re-authorizes it locally, executes the approved capability and returns an idempotent ToolResult.
>
> Same-machine first-party product-to-product communication remains StreamJsonRpc over Named Pipe/UDS. It is separate from Cloud and public HTTP APIs.
>
> Mark [F-009](#rule-f-009) USER_CONFIRMED and resolved by D-010.

---

<a id="rule-d-011"></a>

## D-011 — Target monorepo · resolves **[F-010](#rule-f-010)** · `USER_CONFIRMED`

> The implementation target is the existing monorepo:
>
> C:\MyFile\ArcForges\ArcForges
>
> Do not create a replacement implementation repository.
>
> ArcForges-Design is the sole authoritative requirements, architecture and implementation-planning repository. It contains no product source code.
>
> The existing ArcForges implementation will be inspected only in the later code-reading/reconciliation phase. Its current scaffolds and code are evidence of implementation state, not design authority. They may be retained, restructured, replaced or removed as required by the accepted design.

---

<a id="rule-d-012"></a>

## D-012 — Reference-repository roles · resolves **[F-011](#rule-f-011)** · `USER_CONFIRMED`

> Confirm this reference map:
>
> - AionUi → ArcChat reference.
> - AFFiNE and SiYuan → ArcNotes references.
> - Serial-Studio → ArcScope reference.
> - ArcVideo, ArcVideoFoundation and Olive → ArcSlate references.
> - StartArcForges → packaged-product and release-behavior oracle.
> - The existing ArcForges monorepo → implementation-state inventory and reconciliation target.
>
> Reference repositories are sources of features, behavior, tests, migration evidence and possible reusable material. They are not architecture authorities, parity commitments, or reasons to import their runtime stack.
>
> Every product must receive a Reference Coverage Matrix before implementation planning for that product is finalized.
>
> Mark [F-011](#rule-f-011) USER_CONFIRMED and resolved by D-012.

### Amendment 2026-09-05 — Olive removed as a separate required reference

**Amended by user decision, recorded as [P2-005](phase-2-specification-decisions.md#rule-p2-005) in [`phase-2-specification-decisions.md`](phase-2-specification-decisions.md).**

The verbatim decision block above is unchanged, following this register's supersession convention. The **current effective reference map** replaces its ArcSlate line:

> - **ArcVideo and ArcVideoFoundation → ArcSlate references.**

Every other line of the map, and every other part of [D-012](#rule-d-012) — the non-authority position, the not-a-parity-commitment position, the no-runtime-import position, and the per-product Reference Coverage Matrix requirement — remains in force exactly as recorded.

**Basis.** Olive could not be built in the user's environment. ArcVideo contains the modifications made to get that codebase building, and ArcVideo and ArcVideoFoundation are the intended concrete reference baselines. There is no requirement to obtain or independently review an Olive repository.

**What this amendment does not do.** It removes Olive as a *separate required reference*. It does **not** remove Olive's provenance. ArcVideo is a documented fork of Olive; its GPL-3.0 obligations, upstream copyright and attribution run to the Olive authors, and every notice, licence header and provenance record that inherited material requires is preserved unchanged (**[D-013](#rule-d-013)**).

---

<a id="rule-d-013"></a>

## D-013 — Reuse policy · resolves **[F-012](#rule-f-012)**, governs **[F-013](../assurance/open-gates-register.md#rule-f-013)** · `USER_CONFIRMED`

> Retain Copy First only as a licence-gated and provenance-gated strategy. Reject unconditional copying.
>
> Before any source, test, asset or generated artifact is copied, translated, ported or structurally reused, record:
>
> - exact source repository;
> - exact commit;
> - exact source path;
> - file-level licence and SPDX evidence;
> - copyright and attribution obligations;
> - target file/project;
> - intended Copy, Rewrite, Improve, Replace, Reference Only or Drop disposition;
> - verification oracle;
> - NOTICE requirement;
> - whether the reuse is temporary or permanent.
>
> Permissively licensed compatible material may be copied or ported into the AGPL boundary after this audit.
>
> AGPL-compatible material may be reused only inside the AGPL boundary after exact compatibility and provenance review.
>
> GPL-only, licence-unclear, unknown-origin or otherwise incompatible material must not be copied, translated or ported. It may be used only as controlled behavioral/reference evidence until an explicit compatibility decision says otherwise.
>
> No GPL-family or AGPL-only material may enter the Apache-2.0 mobile/public-client boundary.
>
> Tests and assets require their own licence checks; a repository-root licence must not be assumed to cover every file.
>
> Keep [F-013](../assurance/open-gates-register.md#rule-f-013) DEFERRED_WITH_OWNER_AND_TRIGGER. Its trigger is the first step of the per-product Reference Coverage Matrix and licence audit, before substantive reference source is used for planning or implementation.
>
> Mark [F-012](#rule-f-012) USER_CONFIRMED and resolved by D-013.

---

<a id="rule-d-014"></a>

## D-014 — Web and service surface inventory · resolves **[F-015](#rule-f-015)** · `USER_CONFIRMED`

> Adopt this consolidated inventory:
>
> - arcforges.com — canonical public marketing site.
> - [www.arcforges.com](https://www.arcforges.com) — permanent redirect to arcforges.com.
> - account.arcforges.com — canonical authenticated account portal.
> - chat.arcforges.com — ArcChat web companion.
> - api.arcforges.com — public Cloud API.
> - docs.arcforges.com — public documentation.
> - status.arcforges.com — public service status.
> - downloads.arcforges.com — signed release downloads.
> - updates.arcforges.com — update metadata and release artifacts.
> - ops.arcforges.com — private operator-only surface; never public navigation.
> - notify.arcforges.com — transactional messaging/link domain, not a separate product application.
> - news.arcforges.com — optional marketing communication/content domain, not a separate product application.
>
> Do not turn every hostname into an independently designed application. Account and Chat may be separately deployed configurations of the same ArcForges.Web.App codebase. Static surfaces remain static artifacts where appropriate.
>
> Mark [F-015](#rule-f-015) USER_CONFIRMED and resolved by D-014.

---

<a id="rule-d-015"></a>

## D-015 — Account portal URL · resolves **[F-016](#rule-f-016)** · `USER_CONFIRMED`

> account.arcforges.com is the canonical account portal.
>
> arcforges.com/account is a permanent redirect to the canonical account origin and must not become a second account application.
>
> Use explicit origin, cookie, OAuth redirect, CSP, CSRF and CORS boundaries. Do not share broad parent-domain authentication cookies.
>
> Mark [F-016](#rule-f-016) USER_CONFIRMED and resolved by D-015.

---

<a id="rule-d-016"></a>

## D-016 — Deferred-decision ownership · resolves **[F-017](#rule-f-017)** · `USER_CONFIRMED`

> Do not use “the user” as the operational owner of every deferred item.
>
> Every deferred item must name:
>
> - a responsible role;
> - the user/Product Owner as final approval authority where a product decision is required;
> - a concrete trigger;
> - the earliest consumer;
> - required evidence;
> - the consequence if the gate fails.
>
> Use durable responsibility roles such as Architecture Owner, Product Owner, Licensing and Provenance Owner, Security/Privacy Owner, Commercial Operations Owner and Release Engineering Owner. One person may hold multiple roles; the role remains stable even if the person changes.
>
> Update existing deferred entries accordingly:
>
> - [F-013](../assurance/open-gates-register.md#rule-f-013) → Licensing and Provenance Owner; trigger: before reference material is reused.
> - [F-023](../assurance/open-gates-register.md#rule-f-023) → Release Engineering plus Licensing and Provenance Owner; trigger: before the first mobile distributable.
> - pricing/fee verification → Commercial Operations Owner; trigger: first authoritative pricing specification and again before launch.
> - dependency AOT proof → owning platform work-package owner; trigger: before accepting the dependency into an AOT deliverable.
>
> Mark [F-017](#rule-f-017) USER_CONFIRMED and resolved by D-016.

**Applied.** [F-013](../assurance/open-gates-register.md#rule-f-013), [F-023](../assurance/open-gates-register.md#rule-f-023) and [F-026](../assurance/open-gates-register.md#rule-f-026) above carry role, approval authority, trigger, earliest consumer, required evidence and failure consequence. The pricing/fee deferral is recorded under F-004. The dependency AOT proofs are recorded in the verification record's deferred-gate table.

---

<a id="rule-d-017"></a>

## D-017 — Planning location and format · resolves **[F-018](#rule-f-018)** · `USER_CONFIRMED`

> All new authoritative design and planning output belongs in ArcForges-Design.
>
> Requirements:
> docs/requirements/
>
> Architecture:
> docs/architecture/
>
> Foundation decisions:
> docs/decisions/
>
> Assurance and verification:
> docs/assurance/
>
> Numbered implementation work packages:
> docs/planning/work-packages/
>
> The old ArchitectureDesign/ArcForgesReWrite-AllCsharp location is obsolete and must never be used as an output or authority.
>
> Do not access or depend on the moved historical ArchitectureDesign directory.
>
> The AionUiReWrite-Kotlin material is not an input corpus or authority. The self-contained per-step format contract in I2 is sufficient.
>
> Mark [F-018](#rule-f-018) USER_CONFIRMED and resolved by D-017.

---

<a id="rule-d-018"></a>

## D-018 — Normative glossary · resolves **[F-019](#rule-f-019)** · `USER_CONFIRMED`

> A single normative glossary and invariant catalogue is mandatory before detailed product specifications are finalized.
>
> It must:
>
> - define each canonical cross-product term once;
> - namespace product-specific meanings;
> - preserve every accepted X ≠ Y invariant;
> - distinguish wire terms, domain terms, UI terms, storage terms and commercial terms;
> - identify forbidden aliases and obsolete terms;
> - link each definition to requirements, contracts and later work packages;
> - prevent Workspace, Project, Scope, Task, Run, Step, Attempt, Revision, Approval, Permission, ResourceRef and Capability from being reused ambiguously.
>
> Record this as a mandatory foundation-to-specification gate. Do not generate the full glossary in this turn.
>
> Mark [F-019](#rule-f-019) USER_CONFIRMED and resolved by D-018.

**Gate recorded.** Not generated in this turn. **Owner:** Architecture Owner. **Trigger:** before any detailed product specification is finalized. **Additional input from [V-02](../assurance/phase-1-official-verification.md#rule-v-02):** MCP's extension framework defines Tasks and Skills, which collide with the ArcForges execution vocabulary and must be disambiguated explicitly.

---

<a id="rule-d-019"></a>

## D-019 — Sequence status · resolves **[F-020](#rule-f-020)** · `USER_CONFIRMED`

> Every sequence in the raw corpus is planning evidence only, not a frozen implementation plan.
>
> The new implementation plan must be derived after requirements, architecture, licence matrices and current-code reconciliation are complete.
>
> Use one serial numbered sequence:
>
> 00 → 01 → 02 → … → NN
>
> There is no predetermined maximum step count. The final count may substantially exceed every previous ArcForges plan.
>
> Allow shared foundations, Cloud, Web, Mobile and product work to interleave according to real dependency gates. Do not interpret ArcChat → ArcNotes → ArcScope → ArcSlate as requiring one product to be completely finished before dependent shared work begins.
>
> One main context advances the sequence serially. Do not split implementation ownership across autonomous agent teams.
>
> Mark [F-020](#rule-f-020) USER_CONFIRMED and resolved by D-019.

---

<a id="rule-d-020"></a>

## D-020 — AI and payment economic model · resolves **[F-021](#rule-f-021)** · `USER_CONFIRMED`

> Preserve the provider-independent accounting model:
>
> - fixed-precision internal credit accounting;
> - versioned retail tariffs;
> - per-run tariff snapshots;
> - separate provider-cost, user-credit and promotional/grant ledgers;
> - reserve before execution and settle afterward;
> - immutable historical financial records;
> - explicit hard-stop behavior when authorized balance is exhausted.
>
> Invalidate and remove from the authoritative baseline:
>
> - the old 1.6× retail multiplier;
> - the old 1,000-credit monthly allowance;
> - the old $10/$25/$50 pack economics;
> - the old $9.02/$23.29/$47.07 net-proceeds calculations;
> - every amount derived from expired model pricing or Waffo fees.
>
> Do not replace them with new frozen numbers in Phase 1.
>
> Prices, included allowances, pack sizes, margins and regional amounts are versioned commercial policy. They require current provider pricing, Paddle fees, Payoneer payout costs, taxes, refund exposure and target-margin approval at first specification consumption and again before launch.
>
> Mark [F-021](#rule-f-021) USER_CONFIRMED and resolved by D-020.

---

### [D-020](#rule-d-020) amendment — 2026-09-06

[P2-006](phase-2-specification-decisions.md#rule-p2-006) adopts subscription capacity that replenishes over time, actual-token metering and opt-in extra credits. Official AI requires an active paid service term. Fixed precision, distinct cost/customer/revenue records, customer tariff snapshots, pre-authorisation and immutable corrections remain. Exhausted capacity waits for recovery or explicitly authorised credits; no overdraft or unbounded compute is permitted. Production numbers are external deployment configuration. A $20 monthly offer is an illustrative target, not a verified tariff or profitability assertion.

---

<a id="rule-d-021"></a>

## D-021 — Apache boundary for validators and shared semantics · resolves **[F-022](#rule-f-022)** · `USER_CONFIRMED`

> Confirm and refine Option C.
>
> Inside the Apache-2.0 boundary:
>
> - public wire schemas;
> - public/mobile DTOs;
> - generated or handwritten public clients;
> - validation rules that express wire-format constraints;
> - public protocol state semantics required for independent interoperability;
> - the future public SDK surface.
>
> Outside that shared Apache boundary:
>
> - product-domain behavior;
> - server orchestration;
> - desktop application use cases;
> - policy decisions;
> - persistence behavior;
> - entitlement authority;
> - base ViewModel implementations and UI scaffolding.
>
> Pure application semantics must be classified by responsibility:
>
> - semantics required for an independent client to interpret or validate the public protocol belong in the Apache interoperability layer;
> - product or server business behavior remains in its owning AGPL implementation;
> - mobile-only application behavior is implemented independently inside the Apache mobile boundary.
>
> Base ViewModel patterns are not shared between Avalonia desktop and MAUI mobile. Each UI stack owns its implementation.
>
> Mark [F-022](#rule-f-022) USER_CONFIRMED and resolved by D-021.

---

<a id="rule-d-022"></a>

## D-022 — Mobile-store commerce · resolves **[F-024](#rule-f-024)** · `USER_CONFIRMED`

> Confirm Option A globally for the initial product.
>
> ArcChat Mobile is a free companion/consumption-only application.
>
> It may:
>
> - sign in;
> - display the user’s current plan and entitlement state;
> - consume Cloud capabilities and AI credits already acquired elsewhere;
> - display remote tasks, runs, approvals, notifications and results;
> - manage non-commercial account and security settings allowed by store policy.
>
> It must not:
>
> - sell subscriptions, Cloud access or AI credits in the app;
> - embed Paddle checkout;
> - integrate StoreKit or Google Play Billing for initial release;
> - display an external purchase button, link or purchase call to action;
> - unlock functionality using a locally entered licence key or purchase token.
>
> All initial commerce occurs on the web through Paddle.
>
> Use the same conservative behavior across storefronts even where a regional programme permits external links. This avoids region-specific commercial builds and continuously changing entitlement programmes.
>
> Keep the entitlement architecture capable of accepting a future store-originated grant, but do not implement that source until a new explicit decision authorizes mobile purchasing.
>
> Mark [F-024](#rule-f-024) USER_CONFIRMED and resolved by D-022.

---

<a id="rule-d-023"></a>

## D-023 — Mainland China payment route · resolves **[F-025](#rule-f-025)** · `USER_CONFIRMED`

> Mainland China remains a conditional launch market. Do not add another payment provider for V1.
>
> Use Paddle-hosted web checkout and the payment methods Paddle currently makes available for China.
>
> The intended route is:
>
> - Alipay for supported CNY one-time and recurring purchases, subject to Paddle approval and current provider limits;
> - WeChat Pay for supported one-time desktop-web purchases, subject to its current platform and currency limitations;
> - supported cards or other Paddle methods as available;
> - Payoneer only as the ArcForges payout and settlement destination.
>
> Do not hard-code current provider caps, currencies, approval rules or platform limitations into domain contracts. Represent them through BillingProviderCapabilities and verified commercial configuration.
>
> Cloud Pass remains the non-recurring fixed-term product for customers who cannot or do not want to use recurring payment methods.
>
> ArcChat Mobile remains consumption-only and contains no China-specific checkout.
>
> Before enabling mainland-China sales, require successful gates for:
>
> - Paddle supplier onboarding;
> - Alipay/WeChat Pay approval where required;
> - CNY product and tax configuration;
> - checkout and webhook reachability;
> - Payoneer payout eligibility;
> - refund and reconciliation behavior;
> - sanctions, export, privacy and applicable Chinese regulatory review;
> - production network preflight.
>
> If these gates fail, disable mainland-China sales through explicit regional policy without blocking the global launch. Do not silently substitute another provider.
>
> Mark [F-025](#rule-f-025) USER_CONFIRMED and resolved by D-023.

**Verified against V-08.** The intended route matches Paddle's documented capability set item for item. [V-08](../assurance/phase-1-official-verification.md#rule-v-08) adds three operational facts that sharpen but do not change the decision: Alipay requires a separate approval application conditioned on CNY pricing; the Alipay cap is 1,600 CNY on renewals and charges; and **neither** China method supports chargebacks, so the dispute and refund model must not assume the card pathway.

---

# Dispositions applied

Global rules now in force. Applied to all occurrences they cover without further asking, per D-001.

| # | Disposition | Authority | Scope |
|---|---|---|---|
| 1 | No automatic precedence among raw input documents; they are evidence only. Conflicts are registered, explained, decided, recorded, then applied globally. | [D-001](#rule-d-001) | All |
| 2 | Only material conflicts not already covered by an existing user decision are brought back. | [D-001](#rule-d-001) | All |
| 3 | The product baseline is exactly ArcChat, ArcNotes, ArcScope and ArcSlate. | [D-002](#rule-d-002) | All |
| 4 | `ArcCanvas`, `ArcMusic` and `ArcImage` are obsolete and `SUPERSEDED` wherever they appear, and are excluded from every new authoritative document. Not future, reserved, alias or re-entry-candidate products, so the `I4 §Stage 13.81` fifth-product contract does not apply to them; it remains available for a genuinely new product. | [D-002](#rule-d-002) | All |
| 5 | `ArcVideo` is likewise obsolete wherever it appears; ArcSlate is the current product. | [D-002](#rule-d-002) | T01, T03 |
| 6 | ArcScope is an independently defined product, not a rename or continuation of ArcImage. `I3 §3.5` ArcImage domain concepts must not be migrated into ArcScope. | [D-002](#rule-d-002) | T01, T03 |
| 7 | The former Canvas naming distinction does not require delivery. Canvas/whiteboard and presentation scope is excluded by [P2-006](phase-2-specification-decisions.md#rule-p2-006); no standalone product is introduced. | [D-002](#rule-d-002); [D-006](#rule-d-006) as amended by [P2-006](phase-2-specification-decisions.md#rule-p2-006) | T03 |
| 8 | Raw input files remain unmodified. Dispositions are recorded here, never applied to the inputs themselves. | [D-002](#rule-d-002), [D-005](#rule-d-005) | All |
| 9 | Foundation-critical external facts are verified now; all pricing, quota, fee, rate and regional-availability data is deferred with a first-consumption trigger. | [D-003](#rule-d-003) | All |
| 10 | Two-boundary licensing: ArcChat Mobile and its mobile-facing interoperability code are Apache-2.0; ArcChat Desktop, ArcNotes, ArcScope, ArcSlate, ArcForges Cloud and all server implementations, and everything not explicitly assigned to the Apache-2.0 boundary, remain `AGPL-3.0-only`. | [D-004](#rule-d-004) | T17, T20 |
| 11 | No App Store exception, dual licensing, proprietary grant or CLA for ArcChat Mobile. DCO continues with inbound-equals-outbound licensing per scope. | [D-004](#rule-d-004) | T20 |
| 12 | ArcChat Mobile must not contain, link to, copy from, port from or reference any GPL-family or AGPL-only implementation, directly or transitively. | [D-004](#rule-d-004) | T17, T20 |
| 13 | Protocol communication across explicit process or network boundaries does not change the mobile client's licence; desktop and server implementations remain separate works. | [D-004](#rule-d-004) | T07, T17, T20 |
| 14 | On discovery of a conflicting contribution or dependency in the mobile boundary: register that specific issue and return it for decision. Never silently add an exception, change the licence, or remove the mobile distribution target. | [D-004](#rule-d-004) | T20 |
| 15 | **Waffo Pancake is obsolete and `SUPERSEDED` as a provider choice.** It must not be verified, recommended, integrated, or included in any new authoritative specification, roadmap, dependency, runtime component or implementation step. Every reference to it in the raw corpus is historical evidence only. | [D-005](#rule-d-005) | T11, T12 |
| 16 | **Paddle is the sole customer-facing Merchant of Record for ArcForges web and cloud commerce**, owning checkout, subscriptions, recurring billing, applicable sales-tax and VAT handling, compliant invoices, refunds, chargebacks and payment webhooks. | [D-005](#rule-d-005) | T11 |
| 17 | **Payoneer is the payout and settlement destination for receiving Paddle payouts.** Not a second Merchant of Record, not an interchangeable checkout provider, not a customer-facing fallback processor. | [D-005](#rule-d-005) | T11 |
| 18 | Provider-abstraction principles preserved: entitlement state independent of provider identifiers; provider IDs never in client authority contracts; webhooks verified and idempotent; no irreversible dependence on one provider's proprietary data model. | [D-005](#rule-d-005) | T11 |
| 19 | The payment-provider verification target is Paddle and Payoneer. Their pricing and fees remain under [D-003](#rule-d-003)'s first-consumption rule. | [D-005](#rule-d-005) | T11 |
| 20 | Current ArcNotes scope is notebook core, bounded property/query views and cloud sync. Canvas, Slides and collaboration-only hooks are excluded by the dated [D-006](#rule-d-006) amendment; references do not imply parity. | [D-006](#rule-d-006) as amended by [P2-006](phase-2-specification-decisions.md#rule-p2-006) | T03, T13 |
| 21 | Public marketing, legal, download and other public information pages render as static HTML/CSS without booting the .NET runtime or WebAssembly. Static pages are deployment artifacts, not a second browser application. | [D-007](#rule-d-007) | T16 |
| 22 | `ArcForges.Web.App` is the only interactive browser application: standalone Blazor WebAssembly, `RunAOTCompilation=false`. No Blazor Server circuits, Interactive Server, runtime SSR, React, TypeScript, Node or JS package manager. Minimal audited JS interop only where no adequate managed interface exists. | [D-007](#rule-d-007) | T16 |
| 23 | **ArcForges Cloud is an ASP.NET Core JIT modular monolith.** Strict Native AOT is not a Cloud requirement, and every obsolete claim that Cloud must publish as Native AOT is removed. Azure SDKs, the durable agent loop, provider adapters, SignalR integration, billing, policy and operational infrastructure run inside the JIT boundary. | [D-008](#rule-d-008) | T18, T07 |
| 24 | Desktop remains a Native AOT deliverable with trim/AOT-safe dependency rules. **Only projects actually consumed by an AOT deliverable must satisfy AOT release gates.** Shared public contracts and client libraries stay trim-safe and source-generation friendly. | [D-008](#rule-d-008) | T07, T19 |
| 25 | ArcChat Mobile Android uses the supported .NET 10 Mono AOT release path. Experimental Android CoreCLR and experimental Android NativeAOT are not production baselines. iOS architecture stays present and complete with its build deferred; its release runtime is re-verified against the then-current supported MAUI/iOS baseline. | [D-008](#rule-d-008) | T17 |
| 26 | Contracts are split by communication boundary, product/domain ownership, release cadence and licence boundary. A single ever-growing contracts assembly is rejected, and an ArcNotes contract change must not force an unrelated ArcSlate release. | [D-009](#rule-d-009) | T07, T20 |
| 27 | C# DTOs and endpoint metadata are the source of truth; OpenAPI and JSON Schema compatibility artifacts are generated from them. No parallel handwritten schemas. No business implementation in a contracts package. | [D-009](#rule-d-009) | T07 |
| 28 | Professional desktop products talk directly to Cloud for their own identity, sync, storage and product-domain APIs. **ArcChat is a control plane, never a mandatory data gateway or proxy.** | [D-010](#rule-d-010) | T04, T07, T18 |
| 29 | **Cloud never connects directly to localhost, Named Pipes, Unix sockets or local stdio.** Local action flows as a durable `ToolRequest` that ArcChat Desktop pulls, re-authorizes locally, executes, and answers with an idempotent `ToolResult`. Same-machine first-party product-to-product communication remains StreamJsonRpc over Named Pipe/UDS. | [D-010](#rule-d-010) | T07, T08, T09 |
| 30 | The implementation target is the existing `ArcForges` monorepo; no replacement implementation repository is created. `ArcForges-Design` is the sole authoritative requirements, architecture and planning repository and contains no product source code. Existing scaffolds and code are implementation-state evidence, never design authority. | [D-011](#rule-d-011) | T23 |
| 31 | The reference map is fixed: AionUi → ArcChat; AFFiNE and SiYuan → ArcNotes; Serial-Studio → ArcScope; **ArcVideo and ArcVideoFoundation → ArcSlate** (amended 2026-09-05; see [D-012](#rule-d-012)'s amendment); StartArcForges → packaged-product and release-behaviour oracle; the ArcForges monorepo → implementation-state inventory and reconciliation target. References are never architecture authorities, parity commitments, or reasons to import a runtime stack. | [D-012](#rule-d-012) | T02, T03, T20 |
| 32 | Every product receives a Reference Coverage Matrix — Copy / Rewrite / Improve / Replace / Reference Only / Drop — before its implementation planning is finalized. | [D-012](#rule-d-012), [D-006](#rule-d-006) | T02, T03, T20 |
| 33 | Copy First is licence-gated and provenance-gated; unconditional copying is rejected. The nine-field provenance record in [D-013](#rule-d-013) is mandatory before any source, test, asset or generated artifact is copied, translated, ported or structurally reused. | [D-013](#rule-d-013) | T20 |
| 34 | GPL-only, licence-unclear, unknown-origin or otherwise incompatible material must not be copied, translated or ported; it may be used only as controlled behavioural evidence until an explicit compatibility decision says otherwise. Tests and assets require their own licence checks; a repository-root licence is never assumed to cover every file. | [D-013](#rule-d-013) | T20 |
| 35 | The twelve-entry web and service surface inventory in [D-014](#rule-d-014) is the consolidated list. A hostname is not an application: Account and Chat may be separate deployments of one `ArcForges.Web.App` codebase, and static surfaces stay static artifacts. | [D-014](#rule-d-014) | T16 |
| 36 | `account.arcforges.com` is the canonical account portal; `arcforges.com/account` is a permanent redirect and never a second account application. Explicit origin, cookie, OAuth redirect, CSP, CSRF and CORS boundaries; no broad parent-domain authentication cookies. | [D-015](#rule-d-015) | T16, T10 |
| 37 | **"The user" is not an operational owner.** Every deferred item names a responsible role, the Product Owner as final approval authority where a product decision is required, a concrete trigger, the earliest consumer, required evidence, and the consequence if the gate fails. Roles are durable: Architecture Owner, Product Owner, Licensing and Provenance Owner, Security/Privacy Owner, Commercial Operations Owner, Release Engineering Owner. | [D-016](#rule-d-016) | All |
| 38 | Authoritative output locations are fixed: `docs/requirements/`, `docs/architecture/`, `docs/decisions/`, `docs/assurance/`, `docs/planning/work-packages/`. The old `ArchitectureDesign` locations are obsolete, must never be used as an output or authority, and must not be accessed or depended on. `AionUiReWrite-Kotlin` is not an input corpus or authority. | [D-017](#rule-d-017) | T23 |
| 39 | A single normative glossary and invariant catalogue is a mandatory foundation-to-specification gate. It defines each canonical term once, namespaces product-specific meanings, preserves every accepted `X ≠ Y` invariant, separates wire/domain/UI/storage/commercial terms, names forbidden aliases, and links definitions to requirements, contracts and work packages. | [D-018](#rule-d-018) | T19, T23, All |
| 40 | Every corpus sequence is planning evidence only. The implementation plan is one serial numbered sequence `00 → 01 → … → NN` with no predetermined maximum, derived after requirements, architecture, licence matrices and current-code reconciliation. Work interleaves by real dependency gates. One main context advances it serially; implementation ownership is never split across autonomous agent teams. | [D-019](#rule-d-019) | T23 |
| 41 | The provider-independent accounting model is preserved: fixed-precision credit accounting, versioned retail tariffs, per-run tariff snapshots, three separate ledgers, reserve-then-settle, immutable historical financial records, explicit hard stop at exhausted balance. | [D-020](#rule-d-020) | T11, T12 |
| 42 | Every frozen economic figure derived from expired model pricing or the removed provider's fees is invalidated and removed from the authoritative baseline, and is **not** replaced with new frozen numbers in Phase 1. Prices, allowances, pack sizes, margins and regional amounts are versioned commercial policy requiring approval at first specification consumption and again before launch. | [D-020](#rule-d-020) | T11, T12 |
| 43 | The Apache-2.0 boundary is drawn around **interoperability**: public wire schemas, public/mobile DTOs, public clients, validation rules expressing wire-format constraints, public protocol state semantics, and the future public SDK. Product-domain behaviour, server orchestration, desktop use cases, policy decisions, persistence behaviour, entitlement authority and UI scaffolding stay outside it. | [D-021](#rule-d-021) | T17, T20, T07 |
| 44 | **Base ViewModel patterns are not shared between Avalonia desktop and MAUI mobile.** Each UI stack owns its implementation. | [D-021](#rule-d-021) | T17, T19 |
| 45 | **ArcChat Mobile is a free companion / consumption-only application.** It must not sell anything in-app, embed Paddle checkout, integrate StoreKit or Play Billing for initial release, display an external purchase button, link or call to action, or unlock functionality via a locally entered licence key or purchase token. All initial commerce occurs on the web through Paddle. | [D-022](#rule-d-022) | T11, T17 |
| 46 | The same conservative mobile-commerce behaviour applies across all storefronts, even where a regional programme permits external links. The entitlement architecture stays capable of accepting a future store-originated grant, but that source is not implemented until a new explicit decision authorizes mobile purchasing. | [D-022](#rule-d-022) | T11, T17 |
| 47 | Mainland China is a conditional launch market served through Paddle-hosted web checkout with the methods Paddle currently makes available. No second payment provider for V1, and no silent substitution if gates fail — regional sales are disabled by explicit policy without blocking global launch. | [D-023](#rule-d-023) | T11 |
| 48 | **Provider caps, currencies, approval rules and platform limitations must never be hard-coded into domain contracts.** They are represented through `BillingProviderCapabilities` and verified commercial configuration. Cloud Pass remains the non-recurring fixed-term product. | [D-023](#rule-d-023) | T11 |
| 49 | Absence of an official AOT guarantee is never treated as proof of AOT compatibility. Where documentation cannot prove a dependency's complete behaviour under an AOT deliverable, a real publish-and-test proof is registered as a deferred gate with an owner and trigger. | [D-003](#rule-d-003), [D-008](#rule-d-008) | T07, T19 |

---

# Consolidated verification findings

Per the decision package: any genuinely new material conflict uncovered by verification is recorded here rather than returned as a further questionnaire.

**No new foundation-critical conflict was uncovered.** All nine expected conclusions were checked against official evidence and all held. The verification produced one new registered issue and six consequences already absorbed by existing decisions.

| # | Finding | Source | Disposition |
|---|---|---|---|
| 1 | **Refit's reflection request builder moved to a separate package; `RestService.ForGenerated<T>` is the AOT-safe entry point; `RF006` signals a non-generable shape.** The corpus records none of this. | [V-05c](../assurance/phase-1-official-verification.md#rule-v-05c) | **New issue [F-026](../assurance/open-gates-register.md#rule-f-026)**, deferred as an implementation gate under [D-008](#rule-d-008) and D-016. Changes no decision. |
| 2 | MCP `2026-07-28` is stable, not a release candidate. `I4 §Stage 6.41`'s prohibition was conditioned on RC status and lapses on its own terms. | [V-02](../assurance/phase-1-official-verification.md#rule-v-02) | Recorded under F-004. No decision required — the corpus's own condition resolved it. |
| 3 | MCP's extension framework defines **Tasks** and **Skills**, colliding with the ArcForges `Task / Run / Step / Attempt` vocabulary. | [V-02](../assurance/phase-1-official-verification.md#rule-v-02) | Added as required input to the [D-018](#rule-d-018) glossary gate. |
| 4 | SignalR moved from Not supported (.NET 8) to **Partial support** (.NET 10) under Native AOT, making `I3 §2.1.3` stale. | [V-03](../assurance/phase-1-official-verification.md#rule-v-03) | Recorded as a corpus correction under F-007. Decision unaffected — Cloud is JIT under D-008. |
| 5 | **CNY pricing inverts from forbidden to required.** `I4 §Stage 3.6` forbade a fixed CNY price; Paddle's Alipay route requires CNY-priced products and conditions approval on it. | [V-08](../assurance/phase-1-official-verification.md#rule-v-08) | Absorbed by [D-023](#rule-d-023)'s existing "CNY product and tax configuration" gate. |
| 6 | Neither Alipay nor WeChat Pay supports chargebacks, and WeChat Pay supports neither subscriptions nor mobile. | [V-08](../assurance/phase-1-official-verification.md#rule-v-08) | Absorbed by [D-023](#rule-d-023)'s instruction not to hard-code provider limitations and by its retention of Cloud Pass. Sharpens the refund and dispute model. |
| 7 | Apple 3.1.3(f) category fit is decided by App Review, not by reading the guideline; ArcChat Mobile fits the category's shape but is not literally enumerated. | [V-09](../assurance/phase-1-official-verification.md#rule-v-09) | `PARTIALLY_VERIFIED`. Covered by the existing store-submission gate. Does not affect [D-022](#rule-d-022), which already chooses the most conservative posture available. |

---

# Foundation Freeze gate status

| # | Gate | Status |
|---|---|---|
| 1 | Every current issue resolved or validly deferred | **Pass** — 26 registered: 23 resolved, 3 deferred, 0 open, 0 proposed |
| 2 | Every deferred item has a responsible role and trigger | **Pass** — [F-013](../assurance/open-gates-register.md#rule-f-013), [F-023](../assurance/open-gates-register.md#rule-f-023), [F-026](../assurance/open-gates-register.md#rule-f-026) each carry role, approval authority, trigger, earliest consumer, evidence and failure consequence per [D-016](#rule-d-016) |
| 3 | Official verification artifact complete | **Pass** — `docs/assurance/phase-1-official-verification.md`, [V-01](../assurance/phase-1-official-verification.md#rule-v-01) to [V-09](../assurance/phase-1-official-verification.md#rule-v-09) |
| 4 | Decision register and ledger agree | **Pass** — see the ledger's status table |
| 5 | Four raw inputs byte-unchanged | **Pass** — verified by `git status`/`git diff` scoped to exactly those four paths |
| 6 | No genuinely new foundation-critical conflict blocking the freeze | **Pass** — none uncovered; see consolidated verification findings |

**Decisions recorded:** [D-001](#rule-d-001) through [D-023](#rule-d-023), verbatim.
