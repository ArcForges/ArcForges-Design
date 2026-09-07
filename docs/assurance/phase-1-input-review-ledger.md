# Phase 1 Input Review and Coverage Ledger

> Status: **Foundation Freeze requested** — Phase 1 (Input Review and Foundation Decision Freeze)
> Branch: `design/phase-1-foundation`
> Purpose: Record complete-reading coverage of the closed Phase 1 input corpus, the topic inventory derived from it, and the classification of material content. This ledger is evidence of review; it is not a specification and confers no authority on the material it describes.
> Companions: `docs/decisions/phase-1-foundation-decisions.md` (issues and decisions), `docs/assurance/phase-1-official-verification.md` (official verification record).

**Historical record:** This input review is complete. The four files are now [deprecated](../deprecated-inputs/README.md) and excluded from ongoing design and audit scope. The paths below identify their renamed archive locations; recorded reading ranges, counts and dispositions describe the original review, not a new review or a requirement to repeat it.

## 1. Closed input corpus

Phase 1 used exactly four input files. At that stage, no other file, repository, branch, history, or planning location was admitted as an input. This historical intake boundary does not define current reference-source or formal-design audit scope.

| # | File | Lines | Bytes | Read status |
|---|---|---:|---:|---|
| I1 | [product-discovery-overview-deprecated.md](../deprecated-inputs/product-discovery-overview-deprecated.md) | 91 | 7,746 | Complete |
| I2 | [implementation-sequencing-notes-deprecated.md](../deprecated-inputs/implementation-sequencing-notes-deprecated.md) | 646 | 30,042 | Complete |
| I3 | [platform-architecture-concept-deprecated.md](../deprecated-inputs/platform-architecture-concept-deprecated.md) | 2,522 | 121,737 | Complete |
| I4 | [product-discovery-record-deprecated.md](../deprecated-inputs/product-discovery-record-deprecated.md) | 112,228 | 1,528,926 | Complete |

Total: 115,487 lines / 1,688,451 bytes across the four files.

The four file bodies are preserved unmodified. Their original filenames in the historical coverage headings below identify the reviewed baseline. Accepted corrections and decisions were recorded in `docs/decisions/`, not applied to those bodies.

### 1.1 Reading method

Reading was performed sequentially over contiguous line ranges with no sampling, no heading-only traversal, and no summarisation substituted for reading. `I4` was segmented on its own `# stageN` markers so that every segment boundary is derived from the document's own structure rather than from an arbitrary offset.

## 2. Coverage map

### 2.1 I1 — `product-discovery-overview.md`

Read as a single unit, lines 1–91. Content: a stage-by-stage responsibility table for Stage 0–28 plus a five-part summary. It is an index of `I4`, not an independent source.

### 2.2 I2 — `implementation-sequencing-notes.md`

| Range | Section |
|---|---|
| 1–13 | Header, status, external path references, mainline sequence statement |
| 14–75 | §I Points requiring reconciliation (stage order, obsolete names, ArcChat AOT/JIT conflict) |
| 76–186 | §II Redefining secondary development for ArcNotes, ArcScope, ArcSlate |
| 187–508 | §III Concrete implementation sequence, steps 0–13 |
| 509–567 | §IV How far server interfaces should be designed now |
| 568–587 | §V What can be mocked and what cannot |
| 588–620 | Final recommended sequence |
| 621–646 | §VI Mapping to sequential planning documents |

### 2.3 I3 — `platform-architecture-concept.md`

| Range | Sections |
|---|---|
| 1–48 | Header (baseline verification date 2026-07-20), §0 conclusion, §0.1 full-AOT definition and boundaries |
| 49–116 | §1 Why rewrite this way (retained essentials, discarded approaches, goals, non-goals) |
| 117–212 | §2 2026 technology baseline, version strategy, §2.1 AOT boundaries incl. StreamJsonRpc / Refit / SignalR / data layer |
| 213–328 | §3 Product topology (ArcChat, ArcVideo, ArcNotes, ArcImage, Cloud, Mobile/Web) |
| 329–387 | §4 State ownership and consistency |
| 388–511 | §5 Solution and code boundaries, repository layout, reference direction, contract split |
| 512–841 | §6 StreamJsonRpc Interface Code First RPC (§6.1–§6.16) |
| 842–952 | §7 Local IPC, discovery, routing |
| 953–1034 | §8 Capability system and Agents |
| 1035–1110 | §9 Avalonia desktop application architecture |
| 1111–1174 | §10 Documents, revisions, concurrency; §11 Undo/Redo |
| 1175–1271 | §12 Journal, snapshot, crash recovery; §13 Long task model |
| 1272–1321 | §14 ResourceRef and the large-data path |
| 1322–1410 | §15 P/Invoke and the native ABI |
| 1411–1614 | §16 ArcForges Cloud server |
| 1615–1670 | §17 The .NET MAUI mobile client |
| 1671–1744 | §18 The Blazor web front end; §19 Cloud and desktop bridging |
| 1745–1803 | §20 Identity, security, permissions |
| 1804–1846 | §21 Observability |
| 1847–1890 | §22 Performance, memory, backpressure |
| 1891–1936 | §23 Release mode matrix |
| 1937–1996 | §24 Build and engineering governance |
| 1997–2086 | §25 Testing strategy |
| 2087–2128 | §26 CI/CD quality gates |
| 2129–2162 | §27 Installation, update, rollback |
| 2163–2269 | §28 Phased implementation plan (Phase 0–8) |
| 2270–2323 | §29 Principal risks and disciplines |
| 2324–2401 | §30 Architecture review checklist |
| 2402–2432 | §31 Final decision summary |
| 2433–2522 | §32 Official material and verification sources |

### 2.4 I4 — `product-discovery-record.md`

Segmented on the document's own `# stageN` markers. All 29 segments plus the trailing summary were read completely.

| Segment | Lines | Count | Topic |
|---|---|---:|---|
| Stage 0 | 1–1,227 | 1,227 | Portfolio, business model, pricing, AI economics baseline |
| Stage 1 | 1,228–3,399 | 2,172 | Identity, account, workspace, device, session |
| Stage 2 | 3,400–5,069 | 1,670 | Website, product portal, account portal |
| Stage 3 | 5,070–7,049 | 1,980 | Billing, payment, subscription |
| Stage 4 | 7,050–9,826 | 2,777 | Unified entitlement |
| Stage 5 | 9,827–11,690 | 1,864 | Distribution, installation, update |
| Stage 6 | 11,691–14,681 | 2,991 | ArcChat platform direction |
| Stage 7 | 14,682–17,699 | 3,018 | ArcForges Cloud capabilities |
| Stage 8 | 17,700–20,912 | 3,213 | AI economics, provider, cost |
| Stage 9 | 20,913–24,102 | 3,190 | Data, sync, backup, user assets |
| Stage 10 | 24,103–28,333 | 4,231 | Production operations infrastructure |
| Stage 11 | 28,334–29,996 | 1,663 | Legal, open source, privacy, compliance |
| Stage 12 | 29,997–33,702 | 3,706 | Growth, community, product UX direction |
| Stage 13 | 33,703–36,932 | 3,230 | Product topology and architecture baseline freeze |
| Stage 14 | 36,933–40,698 | 3,766 | Shared desktop experience foundation |
| Stage 15 | 40,699–44,866 | 4,168 | ArcNotes complete product specification |
| Stage 16 | 44,867–49,396 | 4,530 | ArcScope complete product specification |
| Stage 17 | 49,397–54,051 | 4,655 | ArcChat complete product specification |
| Stage 18 | 54,052–57,710 | 3,659 | ArcChat Mobile and Web companion |
| Stage 19 | 57,711–62,568 | 4,858 | Unified agent execution, task, automation model |
| Stage 20 | 62,569–67,893 | 5,325 | ArcSlate specification and Olive-to-C# rewrite |
| Stage 21 | 67,894–73,929 | 6,036 | Cross-app semantic capability and resource model |
| Stage 22 | 73,930–79,365 | 5,436 | Local data, project format, interoperability |
| Stage 23 | 79,366–84,971 | 5,606 | Knowledge, search, retrieval architecture |
| Stage 24 | 84,972–91,474 | 6,503 | Extension, integration, developer platform |
| Stage 25 | 91,475–97,295 | 5,821 | Dynamic configuration and product policy control plane |
| Stage 26 | 97,296–102,957 | 5,662 | Product security, permission, trust closure |
| Stage 27 | 102,958–107,379 | 4,422 | Product quality and compatibility contract |
| Stage 28 | 107,380–112,228 | 4,849 | Support, feedback, operator, trust and safety |

Nested `# Stage NN` headings appearing inside a segment (for example `# Stage 21` at line 38,872 inside the Stage 14 segment) are cross-references within the prose, not segment boundaries. They were read in place.

## 3. Topic inventory

Twenty-three review domains were derived from the corpus and mapped to their governing input locations.

| # | Domain | Primary source |
|---|---|---|
| T01 | Portfolio, names, positioning, product boundaries | I4 Stage 0, 13; I1; I2 §I.2 |
| T02 | ArcChat scope and the AionUi rewrite relationship | I4 Stage 6, 17; I2 §I.3 |
| T03 | ArcNotes, ArcScope, ArcSlate scope | I4 Stage 15, 16, 20; I2 §II |
| T04 | Desktop / Cloud / Mobile / Web responsibilities | I4 Stage 7, 13, 18; I3 §3, §17, §18 |
| T05 | Local-first behaviour and offline operation | I4 Stage 13, 22; I3 §1.1, §4 |
| T06 | State ownership, revisions, conflicts, sync, backup, recovery | I4 Stage 9, 22; I3 §4, §10, §12 |
| T07 | Process boundaries, IPC, public API, realtime, large data | I3 §6, §7, §14, §16; I4 Stage 21 |
| T08 | Agent placement, tasks, tools, approvals, automation, remote | I4 Stage 6, 17, 18, 19; I3 §8, §13 |
| T09 | Security, privacy, permission, trust, egress, sandbox, secrets, audit | I4 Stage 26; I3 §20 |
| T10 | Identity, account, workspace, device, session, realm, self-host | I4 Stage 1, 7 |
| T11 | Billing, payment, subscriptions, entitlements, refunds, reconciliation | I4 Stage 3, 4 |
| T12 | Managed AI, BYOK, provider selection, pricing, credits, quotas | I4 Stage 0, 8 |
| T13 | Persistence, schemas, formats, migration, import/export, portability | I4 Stage 22; I3 §12, §27.2 |
| T14 | Extensions, MCP, skills, integrations, packages, catalogs, publishers | I4 Stage 24 |
| T15 | Native interop, media, acquisition, rendering, performance, platforms | I3 §15; I4 Stage 16, 20 |
| T16 | Web architecture, hosting, security, account portal, checkout, website | I4 Stage 2, 10; I3 §18; I2 §III.12 |
| T17 | Mobile scope, remote control, background, notifications, weak network | I4 Stage 18; I3 §17; I2 §III.8 |
| T18 | Cloud topology, deployment, storage, observability, operations, support | I4 Stage 10, 28; I3 §16, §21 |
| T19 | Accessibility, localization, performance, testing, packaging, updates | I4 Stage 5, 14, 27; I3 §22–§27 |
| T20 | Licensing, copying, clean-room, provenance, NOTICE, verification | I4 Stage 11; I2 §II |
| T21 | Dynamic policy, feature flags, compatibility, provider availability | I4 Stage 25 |
| T22 | Knowledge, search, retrieval, evidence, citation | I4 Stage 23 |
| T23 | Dependency ordering, work packages, gates, traceability | I2 §III, §VI; I3 §28 |

## 4. Content classification

Every material statement in the corpus falls into one of the classes below. Classification affects what may be carried forward into specifications.

| Class | Meaning | Carried forward as |
|---|---|---|
| `USER_INTENT` | Product or commercial intent expressed by the user | Requirement input, subject to confirmation |
| `CANDIDATE_REQUIREMENT` | Proposed observable product behaviour | Requirement, after confirmation |
| `CANDIDATE_ARCHITECTURE` | Proposed structural or boundary decision | Architecture decision, after confirmation |
| `IMPLEMENTATION_PREFERENCE` | Proposed implementation technique | Non-binding unless it protects a boundary |
| `EXTERNAL_FACT` | Claim about a third party, product, price, law, or version | Requires current official verification |
| `SEQUENCING_PROPOSAL` | Proposed ordering of work | Planning input, not a freeze |
| `EXAMPLE` | Illustration, sample name, sample code | Never normative |
| `OBSOLETE` | Superseded by a later corpus statement or by the Phase 1 brief | Disposition recorded, not carried forward |
| `AMBIGUOUS_TRANSLATION` | Wording defect from the English translation | Restated before use |
| `UNSUPPORTED_ASSUMPTION` | Asserted without evidence in the corpus | Flagged for decision |
| `MISSING_DECISION` | Required decision the corpus does not make | Raised to the user |
| `IMPLEMENTATION_DEFINED` | Detail that should remain free | Explicitly left open |

### 4.1 Notable classification calls

- Every version number, price, fee, quota, rate, provider capability and regulatory date in the corpus is `EXTERNAL_FACT`. The corpus carries a verification date of **2026-07-20** (I3 header) with the record written around **2026-07-21**. Per **[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)**, the foundation-critical subset was verified against current official primary sources on **2026-09-04** and is recorded in `phase-1-official-verification.md` ([V-01](phase-1-official-verification.md#rule-v-01) to [V-09](phase-1-official-verification.md#rule-v-09)). All pricing, fee, quota, rate and regional-availability figures remain deliberately unverified and are deferred under [D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)'s first-consumption rule, with every frozen economic figure additionally invalidated by **[D-020](../decisions/phase-1-foundation-decisions.md#rule-d-020)**.
- All C# code blocks, JSON samples, capability identifier strings, file extensions and directory names in I3 and I4 are `EXAMPLE` unless a stage explicitly freezes them. I4 repeatedly states "the specific ID set will be designed by the product contract later".
- I3's `ArcVideo` and `ArcImage` product sections are `OBSOLETE`; I4 Stage 13 §93 lists the five amendments required.
- I3 §28 "Phased implementation plan" (Phase 0–8) is `OBSOLETE` as a sequence; I2 §I.2 states Legacy Phase 3 and Phase 4 cannot be applied to the current portfolio.
- I4's ~250 "inequality" invariant statements (`X ≠ Y`) are `CANDIDATE_ARCHITECTURE` and are the highest-value content in the corpus for preventing rework.

## 5. External references outside the corpus

Recorded per the Phase 1 brief. Not followed.

| Reference | Location | Self-contained? |
|---|---|---|
| `C:\MyFile\ArcForges\ArchitectureDesign\AionUiReWrite-Kotlin` | I2 line 5, §VI | No — cited as a planning-format template. However I2 §VI enumerates the required per-step fields directly, so the format *contract* is self-contained even though the *example* is not. |
| `C:\MyFile\ArcForges\ArchitectureDesign\ArcForgesReWrite-AllCsharp` | I2 lines 6, §VI | Superseded. The Phase 1 brief designates `ArcForges-Design` as the only writable repository. |
| `ArcForges-stages.md` | I2 §I.1 | Self-contained. Its content is `I1`/`I4`. |
| `FutureAllCSharp.md` | I2 §I.2 | Self-contained. Its content is `I3`. |
| ~180 external URLs | I3 §32; I4 stage footnotes | Not followed in this ledger. Each supports an `EXTERNAL_FACT` requiring current verification. |

## 6. Declared repository inventory

Existence verified. No contents read, enumerated, executed, or inspected.

| Path | Present | Phase 1 role |
|---|---|---|
| `C:\MyFile\ArcForges\ArcForges-Design` | Yes | Active, writable |
| `C:\MyFile\ArcForges\ArcForges` | Yes | Implementation monorepo — not read, not design authority |
| `C:\MyFile\ArcForges\AionUi` | Yes | Future ArcChat reference — not read |
| `C:\MyFile\ArcForges\AFFiNE` | Yes | Future ArcNotes reference — not read |
| `C:\MyFile\ArcForges\siyuan` | Yes | Future ArcNotes reference — not read |
| `C:\MyFile\ArcForges\Serial-Studio` | Yes | Future ArcScope reference — not read |
| `C:\MyFile\ArcForges\ArcVideo` | Yes | Future ArcSlate reference — not read |
| `C:\MyFile\ArcForges\ArcVideoFoundation` | Yes | Future ArcSlate reference — not read |
| `C:\MyFile\ArcForges\StartArcForges` | Yes | Packaged-product oracle — not inspected, not executed |

## 7. Official verification

The foundation-critical verification mandated by **[D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)**, as retargeted by **[D-005](../decisions/phase-1-foundation-decisions.md#rule-d-005)**, was executed on **2026-09-04** and is recorded in full at [`phase-1-official-verification.md`](phase-1-official-verification.md).

| ID | Subject | Result |
|---|---|---|
| [V-01](phase-1-official-verification.md#rule-v-01) | EU AI Act Article 50 and current Commission guidance | VERIFIED |
| [V-02](phase-1-official-verification.md#rule-v-02) | MCP `2026-07-28` specification and official C# SDK | SUPERSEDED — RC status no longer current; now stable |
| [V-03](phase-1-official-verification.md#rule-v-03) | ASP.NET Core Native AOT support in .NET 10 | VERIFIED |
| [V-04](phase-1-official-verification.md#rule-v-04) | .NET MAUI Android and iOS runtime and compilation status | VERIFIED |
| [V-05](phase-1-official-verification.md#rule-v-05) | AOT evidence for Avalonia, StreamJsonRpc, Refit, SignalR, Azure SDKs, EF Core | PARTIALLY_VERIFIED / DEFERRED per dependency |
| [V-06](phase-1-official-verification.md#rule-v-06) | Paddle Merchant-of-Record role | VERIFIED |
| [V-07](phase-1-official-verification.md#rule-v-07) | Paddle-to-Payoneer payout relationship | VERIFIED |
| [V-08](phase-1-official-verification.md#rule-v-08) | Paddle mainland-China support (Alipay, WeChat Pay) | VERIFIED |
| [V-09](phase-1-official-verification.md#rule-v-09) | Apple and Google rules for a free consumption-only companion app | Google VERIFIED; Apple PARTIALLY_VERIFIED |

All nine expected conclusions in the decision package were checked against official evidence rather than substituted for it, and all held. One new implementation-critical issue was discovered (**[F-026](open-gates-register.md#rule-f-026)**, Refit AOT packaging) and registered as a deferred gate. No new foundation-critical conflict was uncovered.

**Not verified, by decision:** all prices, fees, quotas, exchange rates, tax rates, provider rate cards, storage and AI rates, and store fee details. These remain deferred under [D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003)'s first-consumption rule.

## 8. Deferred gates

Every deferred item carries a durable responsibility role and a concrete trigger, per **[D-016](../decisions/phase-1-foundation-decisions.md#rule-d-016)**. "The user" is not used as an operational owner.

| Item | Responsible role | Trigger |
|---|---|---|
| **[F-013](open-gates-register.md#rule-f-013)** — reference-repository licences and file-level SPDX evidence | Licensing and Provenance Owner | Before any reference material is reused; first step of the per-product Reference Coverage Matrix |
| **[F-023](open-gates-register.md#rule-f-023)** — ArcChat Mobile provenance and complete transitive dependency closure | Release Engineering Owner **and** Licensing and Provenance Owner | Before the first App Store, TestFlight, Google Play or sideloadable mobile artifact |
| **[F-026](open-gates-register.md#rule-f-026)** — Refit version pin, `ForGenerated` policy, `Refit.Reflection` prohibition, `RF006` build-breaking | Owning platform work-package owner (Architecture Owner approves) | Before accepting Refit into an AOT deliverable |
| Pricing, fee, quota and rate verification | Commercial Operations Owner | First authoritative pricing specification; again before launch |
| EU AI-content marking mechanism and Code of Practice position | Security/Privacy Owner (Product Owner approves) | First EU market availability |
| MCP SDK version pin and extension-vocabulary mapping | Architecture Owner | Start of the MCP/extension work package |
| Avalonia + third-party control AOT publish proof | Owning platform work-package owner | Before accepting a third-party control into an AOT deliverable |
| StreamJsonRpc contract-attribute policy test and AOT publish proof | Architecture Owner | Before the first AOT desktop deliverable |
| Android runtime confirmation; re-verification on framework major upgrade; iOS baseline re-verification | Release Engineering Owner with Architecture Owner | First Android production build; framework upgrade; iOS build activation |
| Cloud component AOT proof, if any component is ever AOT-published | Architecture Owner | Any decision to AOT-publish a Cloud component |
| Paddle supplier onboarding; sanctions and export screening | Commercial Operations Owner | Before first live transaction |
| Payoneer eligibility and receiving-currency confirmation | Commercial Operations Owner | First authoritative pricing specification; again before launch |
| Mainland-China enablement gates per [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023), sharpened by [V-08](phase-1-official-verification.md#rule-v-08) | Commercial Operations Owner (Product Owner approves catalogue) | Before enabling mainland-China sales |
| Store category-fit and consumption-only conformance | Release Engineering Owner with Product Owner approval | First mobile store submission |
| Normative glossary and invariant catalogue ([D-018](../decisions/phase-1-foundation-decisions.md#rule-d-018)) | Architecture Owner | Before any detailed product specification is finalized |

## 9. Ledger status

| Gate item | Status |
|---|---|
| All four input files read completely | Done |
| Complete-reading coverage recorded | Done |
| Topic inventory established | Done |
| Content classification scheme established | Done |
| Material issues registered | Done — 26 issues, [F-001](../decisions/phase-1-foundation-decisions.md#rule-f-001) to [F-026](open-gates-register.md#rule-f-026), every identifier used and none skipped (an earlier never-written [F-022](../decisions/phase-1-foundation-decisions.md#rule-f-022) draft is recorded as such; see the register's hygiene note) |
| Every issue resolved or validly deferred | Done — 23 resolved, 3 deferred, 0 open, 0 proposed |
| Every deferred item has a responsible role and trigger | Done — section 8 |
| Time-sensitive claims verified or marked unresolved | Done — foundation-critical verified per [D-003](../decisions/phase-1-foundation-decisions.md#rule-d-003) (section 7); pricing and rates deferred with owner and trigger |
| Official verification artifact complete | Done — `phase-1-official-verification.md`, [V-01](phase-1-official-verification.md#rule-v-01) to [V-09](phase-1-official-verification.md#rule-v-09) |
| User decisions recorded | **[D-001](../decisions/phase-1-foundation-decisions.md#rule-d-001) to [D-023](../decisions/phase-1-foundation-decisions.md#rule-d-023) recorded verbatim** in `docs/decisions/phase-1-foundation-decisions.md` |
| Four raw input files byte-unchanged | Done — verified by `git status` and `git diff` scoped to exactly those four paths |
| Decision register and ledger agree | Done |
| New foundation-critical conflict blocking the freeze | None uncovered |
| Foundation Freeze | **Requested — all gates pass** |
