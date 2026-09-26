# Phase 2 Specification Decisions

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Decisions
> Governing authority: **[D-001](phase-1-foundation-decisions.md#rule-d-001)** (conflict-resolution rule), **[D-016](phase-1-foundation-decisions.md#rule-d-016)** (deferred-decision ownership), **[D-019](phase-1-foundation-decisions.md#rule-d-019)** (sequence status)
> Companions: [`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md), [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)

Phase 1 decisions remain binding except where subsequent explicit user direction amends them under [D-001](phase-1-foundation-decisions.md#rule-d-001). **[P2-006](#rule-p2-006) records the user-directed requirements revision of 2026-09-06.**

The bar for entry is deliberately high. A conclusion already established by a current formal specification or an effective accepted decision is implemented in the appropriate layer with a citation — it does not become a duplicate decision record. The [deprecated input archive](../deprecated-inputs/README.md) supplies no new requirements or authority; its citations and original quotations are historical provenance only. [P2-001](#rule-p2-001) through [P2-010](#rule-p2-010) are recorded below. [P2-002](#rule-p2-002) is withdrawn; [P2-003](#rule-p2-003) is adopted under the Web redesign. [P2-009](#rule-p2-009) now amends repository ownership, proto, Cloud/AI and Mobile technology. [P2-010](#rule-p2-010) further replaces Mobile with Kotlin/Compose Android only, licenses all Contracts as Apache-2.0 and completes the initial producer surface. Earlier runtime/transport outcomes are historical where these decisions explicitly supersede them; the accepted product and commercial scope remains binding.

---

## Register conventions

| Field | Meaning |
|---|---|
| **Status** | `ADOPTED` — decided and in force · `DEFERRED` — deliberately left open with an owner, a trigger and a binding constraint · `WITHDRAWN` — recorded in error, normative content removed, entry retained so the correction is auditable |
| **Authority** | Who may change it |
| **Consumed by** | Where it is implemented and enforced |

| # | Rule |
|---|---|
| <a id="rule-rc-01"></a>RC-01 | An author may not silently contradict Phase 1. Subsequent explicit user decisions take precedence under **[D-001](phase-1-foundation-decisions.md#rule-d-001)** and require a dated amendment recording the affected scope; **[P2-006](#rule-p2-006)** is such an amendment. |
| <a id="rule-rc-02"></a>RC-02 | **A decision recorded here is cited inline wherever it is implemented**, exactly as Phase 1 decisions are. |
| <a id="rule-rc-03"></a>RC-03 | **A deferred decision carries an owner, a trigger and the constraint every permitted option must satisfy** — never a bare "decide later". |
| <a id="rule-rc-04"></a>RC-04 | **Adding to this register requires the same discipline as Phase 1**: a real decision, a stated consequence, and a named enforcement mechanism. |

---

<a id="rule-p2-001"></a>

## P2-001 — Install and update infrastructure baseline · `ADOPTED`

**Decision.** **Velopack** is the cross-platform install and update framework baseline for the three professional desktop products on Windows, macOS and Linux, as specified in the [current packaging architecture](../architecture/14-build-packaging-and-release.md#5-packaging). The baseline has three qualifications:

1. **It sits behind a thin build-script and integration boundary.** Product code never references the framework's types outside one update-integration component, so the framework can be replaced without touching product code.
2. **The product's own update system remains authoritative across every distribution channel.** A platform store or package manager delivers the same signed installer; it does not become the update mechanism.
3. **It consumes the publish output directory and requires no machine-installed runtime.** This is what makes it compatible with the Native AOT desktop posture (**[D-008](phase-1-foundation-decisions.md#rule-d-008)**).

**Why this is a Phase 2 decision.** Phase 1 decided the runtime matrix (**[D-008](phase-1-foundation-decisions.md#rule-d-008)**), the distribution surfaces (**[D-014](phase-1-foundation-decisions.md#rule-d-014)**) and the mobile commerce posture (**[D-022](phase-1-foundation-decisions.md#rule-d-022)**), but never the desktop install and update mechanism. Implementation cannot proceed without it, and the choice constrains packaging, signing, the update feed, delta updates, channel switching and rollback across three platforms.

**Consequences.**

- Windows uses a per-user installer requiring no elevation; a machine-wide package may be added later for enterprise need.
- A store listing carries the **same signed installer**, not a repackaged container.
- Linux ships **one** self-contained portable format first; multiple packaging formats are not maintained simultaneously in the first stage.
- Delta updates, three release channels, self-hosted update sources and downgrade are available from the framework rather than built.

**Authority.** Architecture Owner, with the Release Engineering Owner.

**Consumed by.** [`../architecture/14-build-packaging-and-release.md`](../architecture/14-build-packaging-and-release.md) `§5`; [`../requirements/10-distribution-update-and-support.md`](../requirements/10-distribution-update-and-support.md) `§1`–`§3`; work packages `02`, `50`.

**Reversal cost.** Moderate before the first public release, high afterwards — an installed base's update path is not easily migrated. The abstraction boundary in qualification 1 exists specifically to keep this cost bounded.

---

<a id="rule-p2-002"></a>

## P2-002 — Sequence derivation under [D-019](phase-1-foundation-decisions.md#rule-d-019) · `WITHDRAWN` — superseded by [P2-004](#rule-p2-004)

> **This entry was wrong and is retained as the record of the error, not as authority.** Its normative content is withdrawn. The governing entry is [P2-004](#rule-p2-004).

**What it decided.** That the numbered work-package sequence would be derived **before** the per-product Reference Coverage Matrices and the item-level code inventory existed, with those audits scheduled inside the sequence and later packages rewritten if a finding invalidated them (the withdrawn derive-before-evidence rules).

**Why it was wrong.** **[D-019](phase-1-foundation-decisions.md#rule-d-019)** states that the implementation plan *must be derived after* requirements, architecture, licence matrices and current-code reconciliation are complete. **[D-012](phase-1-foundation-decisions.md#rule-d-012)** states that every product must receive a Reference Coverage Matrix *before implementation planning for that product is finalized*. Both are `USER_CONFIRMED` and binding.

[P2-002](#rule-p2-002) substituted a different process — derive first, audit during implementation, rewrite after findings — and presented that substitution as satisfying **[D-019](phase-1-foundation-decisions.md#rule-d-019)**. It did not. A Phase 2 decision may not alter a Phase 1 decision's ordering requirement, and [RC-01](#rule-rc-01) of this register already says so. The entry contradicted the rule under which it was recorded.

**What the substitution cost.** It was not a formality. Producing the prerequisite evidence afterwards surfaced findings that would have changed the plan:

| Finding | Where | What the sequence had assumed |
|---|---|---|
| Four of six accessible references are GPL-family, proprietary or AGPL; **no reuse is possible from any of them** | [`../assurance/reference-coverage/README.md`](../assurance/reference-coverage/README.md) `§Aggregate licence position` | That per-product licence audits might clear material for reuse, making `Copy`/`Port` dispositions plausible downstream |
| Neither ArcNotes reference implements slides | [`arcnotes-affine-siyuan.md`](../assurance/reference-coverage/arcnotes-affine-siyuan.md) [F-AN-2](../assurance/reference-coverage/arcnotes-affine-siyuan.md#rule-f-an-2) | That [WP-29](../planning/work-packages/29-arcnotes-slides.md#rule-wp-29) would have reference oracles like its sibling packages |
| Serial-Studio's licence creates an **authorship boundary**, not only a reuse prohibition | [`arcscope-serial-studio.md`](../assurance/reference-coverage/arcscope-serial-studio.md) [F-AS-1](../assurance/reference-coverage/arcscope-serial-studio.md#rule-f-as-1) | That the whole reference was readable evidence |
| The implementation repository has **166 projects and 8,638 C# lines**, not 332 projects of substance | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) `§3` [C-01](../assurance/implementation-state-reconciliation.md#rule-c-01), [C-02](../assurance/implementation-state-reconciliation.md#rule-c-02) | A materially different starting position |
| Four of six recorded conformance findings were false | there, [C-03](../assurance/implementation-state-reconciliation.md#rule-c-03)–[C-06](../assurance/implementation-state-reconciliation.md#rule-c-06) | [WP-02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) and [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) scoped larger than the evidence supports |
| The cloud three-role separation does not exist | there, `§5.5` | Not identified at all — a new priority-3 item |
| Olive was **not present** at the authorized location, which the plan had assumed | [`arcslate-arcvideo.md`](../assurance/reference-coverage/arcslate-arcvideo.md) | That all registered ArcSlate references were available. **Resolved by [P2-005](#rule-p2-005)**: the reference map is amended and ArcVideo plus ArcVideoFoundation are the baselines |

The withdrawn rule anticipated rewriting "a package"; the evidence in fact changed package scope, priority order and one open question requiring the user's decision. Deriving first did not make the dependency structure visible — it made a **provisional** structure look settled.

**Status of everything it produced.** The sequence derived under [P2-002](#rule-p2-002) was **provisional**, not a validly derived implementation plan. [P2-004](#rule-p2-004) records its re-derivation from the completed evidence and the specific changes that followed.

**Withdrawn on.** 2026-09-05, during the Stage 2 repair and closure pass.

---

<a id="rule-p2-003"></a>

## P2-003 — Browser session deployment · `ADOPTED 2026-09-06`

**Current decision.** Under [P2-008](#rule-p2-008), browser authentication uses a same-origin C# session adapter inside the existing Cloud host. The edge routes the Account and Chat origins to that host; no new Node server or separate BFF deployment is needed. Each origin receives its own opaque Secure/HttpOnly host-only cookie; session authority, expiry, step-up and revocation stay in the D1 Identity store. Browser JavaScript receives no access/refresh credential.

**Why it can now be resolved.** The Web redesign fixes the edge/API topology and the shared Cloud deployment. The previously unknown extra-host question no longer applies. The adapter calls the same C# application services as native/public API endpoints rather than storing bearer tokens to proxy into a second backend.

**Binding requirements.** Exact origin checks, explicit antiforgery on all unsafe cookie-authenticated operations, no parent-domain cookie, no credentials in bundles or URLs, bounded idle/absolute expiry, conservative browser trust and revocation across replicas. Native/mobile bearer refresh semantics remain separately specified.

**Owner and verification.** Architecture Owner with Security and Privacy Owner. [WP-22.08](../planning/work-packages/22-identity-workspace-and-device.md#rule-wp-22.08) implements the server adapter; [WP-23.05](../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23.05) proves generated clients; [WP-48.01](../planning/work-packages/48-account-portal.md#rule-wp-48.01) verifies real browser authentication. [PG-23](../assurance/open-gates-register.md#rule-pg-23) remains open for implementation evidence.

**Consumed by.** [Web architecture §5](../architecture/10-web-architecture.md#5-browser-session-architecture--p2-003-resolved), [Cloud session storage](../architecture/data-model/01-cloud-data-model.md#browser-session-storage), [browser-session operations](../architecture/contracts/01-public-api-operations.md#browser-session-operations).

**History.** Originally deferred to [WP-48.01](../planning/work-packages/48-account-portal.md#rule-wp-48.01) between cookie-based BFF and in-memory access tokens. The 2026-09-06 redesign adopts the cookie-session form. The historical deferral is not an outstanding design choice, and this decision is not evidence that browser authentication has been implemented.

---

<a id="rule-p2-004"></a>

## [P2-004](#rule-p2-004) — Sequence derivation from completed prerequisite evidence · `ADOPTED`

**Decision.** The implementation sequence is derived from the completed prerequisite evidence, in the ordering **[D-019](phase-1-foundation-decisions.md#rule-d-019)** and **[D-012](phase-1-foundation-decisions.md#rule-d-012)** require. The prerequisite evidence is:

| Prerequisite | Artifact | State |
|---|---|---|
| Requirements | [`../requirements/`](../requirements/README.md) | Complete |
| Architecture | [`../architecture/`](../architecture/README.md) | Complete |
| Licence matrices — per product, per **[D-012](phase-1-foundation-decisions.md#rule-d-012)** | [`../assurance/reference-coverage/`](../assurance/reference-coverage/README.md) — five matrices, 145 item-level rows | **Complete.** The one unresolved determination it carried was closed by [P2-005](#rule-p2-005) |
| Current-code reconciliation | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) — 166 projects, item-level | **Complete** |

**Ordering, stated plainly.** Requirements and architecture, then licence matrices and code reconciliation, **then** the plan. That is **[D-019](phase-1-foundation-decisions.md#rule-d-019)**'s ordering and it is now followed rather than substituted.

**Consequences.**

<a id="rule-dd-01"></a>
- `DD-01`: **The sequence is derived, not provisional.** Every package's scope rests on evidence that existed before it was written.
<a id="rule-dd-02"></a>
- `DD-02`: **The baseline matrices and the inventory are versioned planning inputs.** Implementation packages consume them. No implementation package re-creates a baseline audit.
<a id="rule-dd-03"></a>
- `DD-03`: **Implementation packages retain drift checks only** — source drift against the recorded commit, changed scope, and newly introduced material. Baseline creation and later maintenance are different obligations and are not conflated.
<a id="rule-dd-04"></a>
- `DD-04`: **Where evidence changed a package, the change is recorded** with its evidence, the affected statement, the correction, downstream consumers and the verification needed — in [`../planning/evidence-driven-revisions.md`](../planning/evidence-driven-revisions.md).
<a id="rule-dd-05"></a>
- `DD-05`: **No unresolved determination remains.** The one that existed — [OC-01](../assurance/open-gates-register.md#rule-oc-01), the ArcSlate reference baseline — was closed by user decision on 2026-09-05 and is recorded as [P2-005](#rule-p2-005).
<a id="rule-dd-06"></a>
- `DD-06`: **The four derive-before-evidence rules are withdrawn with [P2-002](#rule-p2-002).** They described the substituted process.

**Authority.** Product Owner, with the Architecture Owner and the Licensing and Provenance Owner.

**Consumed by.** [`../planning/implementation-sequence.md`](../planning/implementation-sequence.md) `§1.1`; [`../planning/work-packages/README.md`](../planning/work-packages/README.md); [`../planning/evidence-driven-revisions.md`](../planning/evidence-driven-revisions.md); every work package's Required Inputs.

**Reversal cost.** Not applicable — this is the ordering Phase 1 already confirmed. It is followed, not chosen.

---

<a id="rule-p2-005"></a>

## P2-005 — ArcSlate reference baseline: ArcVideo and ArcVideoFoundation · `ADOPTED`

**Decision (user, 2026-09-05).** **ArcSlate's direct reference repositories are ArcVideo and ArcVideoFoundation. There is no requirement to obtain or independently review an Olive repository.**

**Basis.** Olive could not be built in the user's environment. ArcVideo contains the modifications made to get that codebase building, and ArcVideo and ArcVideoFoundation are the intended concrete reference baselines. The concrete, buildable fork is the reference of record; the unbuildable upstream is not.

**Why this is a decision and not an inference.** **[D-012](phase-1-foundation-decisions.md#rule-d-012)** registered Olive explicitly. Dropping it is a scope decision that only the Product Owner can take — which is why the Stage 2 repair recorded it as [OC-01](../assurance/open-gates-register.md#rule-oc-01) and did not resolve it locally.

**Consequences.**

<a id="rule-rb-01"></a>
- `RB-01`: **[D-012](phase-1-foundation-decisions.md#rule-d-012)'s reference map is amended.** The verbatim decision block is preserved per this register's supersession convention; the current effective ArcSlate line is *"ArcVideo and ArcVideoFoundation → ArcSlate references"* ([`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md) §[D-012](phase-1-foundation-decisions.md#rule-d-012) amendment; applied-disposition row 31).
<a id="rule-rb-02"></a>
- `RB-02`: **The Olive-direct audit scope is removed.** No obligation exists to obtain Olive's independent tests, fixtures, source or licence file. The missing-repository blocker is withdrawn.
<a id="rule-rb-03"></a>
- `RB-03`: **ArcSlate's reference coverage, planning and verification evidence rest on the actual ArcVideo and ArcVideoFoundation repositories**, at commits `caf5651` and `139eeca`.
- <a id="rule-rb-04"></a>`RB-04`: **Olive-origin provenance is preserved, not erased.** ArcVideo is a documented fork of Olive. Its **GPL-3.0 obligations, upstream copyright and attribution run to the Olive authors**, and every notice, licence header and provenance record that inherited material requires is retained (**[D-013](phase-1-foundation-decisions.md#rule-d-013)**). Removing Olive as an independent reference does not authorise removing its provenance, and no row in any matrix does so.
<a id="rule-rb-05"></a>
- `RB-05`: **Preserved raw inputs are unchanged.** `I2 §II` and `I4 §Stage 20` still discuss Olive as historical evidence; this decision is recorded outside them and does not rewrite them.
<a id="rule-rb-06"></a>
- `RB-06`: **[OC-01](../assurance/open-gates-register.md#rule-oc-01) is closed.** No unresolved determination remains in the Phase 2 register.

**What does not change.** ArcSlate remains an **original implementation**. Both references are **GPL-3.0-only**, so **[D-013](phase-1-foundation-decisions.md#rule-d-013)** still prohibits copying, translating or porting from either; every matrix row remains `Reference Only` or an accepted exclusion. Removing Olive narrows the *audit* scope, not the *reuse* prohibition.

**Authority.** Product Owner (this decision), with the Licensing and Provenance Owner for [RB-04](#rule-rb-04).

**Consumed by.** [`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md) §[D-012](phase-1-foundation-decisions.md#rule-d-012) amendment; [`../assurance/reference-coverage/arcslate-arcvideo.md`](../assurance/reference-coverage/arcslate-arcvideo.md); [`../assurance/reference-coverage-and-provenance.md`](../assurance/reference-coverage-and-provenance.md) §1.1, §2.2, §7; [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md) §6; [`../requirements/products/arcslate.md`](../requirements/products/arcslate.md) §1; [`../requirements/00-product-scope-and-portfolio.md`](../requirements/00-product-scope-and-portfolio.md) §9; [WP-36](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36).

**Reversal cost.** Low. Should an Olive checkout later become available and be wanted, it is added to the reference map and the ArcSlate matrix is extended; nothing built on this decision would need to be undone.

---

<a id="rule-p2-006"></a>

## P2-006 — Cloud subscription product and requirements scope revision · ADOPTED

**SUPERSEDED IN PART (2026-09-17):** C# host/runtime placement, Docker-mounted configuration and provider topology are superseded by [P2-009](#rule-p2-009)/[P2-012](#rule-p2-012)/[P2-013](#rule-p2-013). Paid-service, single-owner and product-scope rules remain binding. See [P2-013](#rule-p2-013).

**Authority.** The user's explicit requirements discussion and instruction of **2026-09-06** to apply the changes directly in this worktree, design the remaining metering rules, and review the resulting requirements. This overrides conflicting preserved-input positions and affected portions of [D-006](phase-1-foundation-decisions.md#rule-d-006) and [D-020](phase-1-foundation-decisions.md#rule-d-020) under **[D-001](phase-1-foundation-decisions.md#rule-d-001)**. Preserved inputs remain unchanged.

**User-directed scope.** All AI inference, the single Harness, durable agent orchestration and AI automation are Cloud responsibilities. Official AI requires an active paid service term and uses subscription capacity plus explicitly authorised extra credits. No local AI, end-user BYOK (local or Cloud), agent teams, sub-agents or external-agent delegation. Ordinary bounded tool concurrency and non-agent background jobs remain. Workspaces are single-owner, multi-device boundaries; no organisations, membership, invitations, collaborative editing or collaboration-only schema hooks. Cloud has one ASP.NET Core JIT deployment host with bounded internal background services.

ArcNotes delivers the notebook core, cloud sync, block references/backlinks, properties, queries and views informed by AFFiNE and SiYuan. Full Edgeless, shapes/connectors/frames, slides/presentations, spaced repetition and DOCX import are excluded from the current complete scope, with no mandatory future hooks. Custom local encrypted stores, encrypted portable exports and E2EE are also excluded. ArcChat retains the lean preview scope; no code/Diff/Office workbench is added. ArcScope gains a real deterministic Cloud simulator. ArcSlate gains canonical .otio import/export.

**Design dispositions under the user's delegated requirement-design authority.** These make that direction implementable; they are not quotations of additional user confirmations:

- Cloud owns acknowledged versions of synchronised user data and all agent state. Native clients keep working caches and durable pending edits; cached note editing/search can survive outages, without promising a permanent account-free notebook product. Hardware acquisition and media editing/rendering retain product-local execution and resource ownership.
- Notes' required property depth is common scalar types plus saved list/table views with filtering and sorting. Formula, relation/rollup engines and further database layouts are excluded from current delivery. Basic Markdown/text import and a Cloud data export remain; a full-fidelity local package ecosystem is not required.
- A paid monthly/annual subscription or active prepaid Cloud Pass is the service term; the Pass remains the [D-023](phase-1-foundation-decisions.md#rule-d-023) non-recurring purchase route, not a credit-only AI bypass. Renewal grace protects data access but does not fund new AI calls after the paid term. Purchased credits are retained on expiry and usable again with an active service term.
- Actual provider usage, normalised into non-overlapping billing categories, is the metering basis. Supplier cost, customer usage units, subscription capacity, purchased credits and payment revenue remain separate. Customer tariff snapshots, fixed precision, reservation, idempotent settlement and immutable adjustments remain binding under [D-020](phase-1-foundation-decisions.md#rule-d-020). Replenishing subscription capacity supplies the base service; extra credits require opt-in. Numeric prices and limits remain versioned deployment data.
- Complete pricing, entitlement and rate-control code runs against validated external configuration. Production values are mounted into Docker at deployment; no private repository, proprietary policy plug-in, separate policy service or authoring UI is required. Public sample configuration exercises the same implementation. Database snapshots and ledgers are real persisted facts, not alternate mutable price authorities.
- Independent self-hosting runs the same Cloud code with an operator-funded, deployment-configured remote model provider and realm policy. This is infrastructure credential provisioning, not end-user BYOK. It confers no official-service entitlement and does not run models in the desktop.
- Existing licensing boundaries remain. Deployment-specific operating values are private; covered implementation code is not hidden as configuration. Public schemas and runnable samples remain available.

**Consumed by.** The revised [requirements set](../requirements/README.md), especially [scope](../requirements/00-product-scope-and-portfolio.md), [commerce](../requirements/04-commerce-entitlement-and-credits.md), [AI execution](../requirements/05-ai-and-agent-execution.md), [configuration](../requirements/11-policy-and-configuration.md) and [product requirements](../requirements/products/README.md).

**Downstream reconciliation status.** This is a requirements revision within **Stage 2**, not a claim that Stage 2 or implementation is complete. Architecture, reference/invariant coverage accounting, work packages, traceability and assurance evidence were produced against earlier scope and require reconciliation before implementation. Their previous completion claims do not demonstrate coverage of [P2-006](#rule-p2-006). Detailed schemas, classes, deployment artifacts and implementation steps remain downstream work.

**Acceptance.** Current requirements neither grant an excluded mode nor leave required simulator, OTIO or metering behaviour as a placeholder. Requirements agree on authority, scope, lifecycle, failure behaviour and evidence. Existing identifiers remain traceable; excluded obligations are explicitly retired rather than silently reused.

---

<a id="rule-p2-007"></a>

## P2-007 — Stage 2 design closure corrections · ADOPTED

**Authority.** The user's explicit instruction in this session to repair all fourteen review groups against baseline `c5b95a7`, including the necessary detailed design and cross-document reconciliation. These are authorised design dispositions, not claims of additional user confirmations. The work remains Stage 2; it changes no product or reference source and preserves `docs/inputs/`.

**Effective choices.** Cloud Notes receives a canonical D1 model; local pending edits retain durable lineage. Publication guarantees per-aggregate revision order and safe cursor advancement, not a global business-commit order inferred from UUIDs. Shared transactions are enumerated for the actual operation families. Admission reserves operator exposure as well as customer funds. Capacity transitions first advance accrual under the previous hold state; a lowered ceiling preserves an already-issued excess balance but cannot increase it. Service terms and plan assignments retain immutable history. Provider dispatch and per-call settlement are separate from final Turn completion. Stream truncation is a presentation state. Migration completion requires version-guarded materialisation and a fenced cutover. C# helper processes isolate hostile parsers and extension executables using OS-enforced capabilities; they contain no product domain or agent loop. OTIO conversion has an explicit external floating-point boundary around the integer tick domain.

**Scope.** [P2-006](#rule-p2-006)'s product scope continues to govern. Native Scope/Slate working stores remain authoritative locally; Cloud acknowledges their synchronised metadata replicas. The helper-process design is the present, bounded application of [D-016](phase-1-foundation-decisions.md#rule-d-016)'s isolation exception, not a C++ worker or second Agent Host. Its operation allowlist, ownership and platform enforcement are specified in the architecture.

**Closure evidence.** The [Stage 2 closure review](../assurance/phase-2-design-closure-review.md) records the fourteen dispositions, design checks and remaining implementation obligations. Existing historical statements are not completion evidence for the revised baseline. A future runtime gate cannot substitute for resolving a contradiction in current specifications.

---

<a id="rule-p2-008"></a>

## P2-008 — React/TypeScript Web and C# generated API clients · ADOPTED

**SUPERSEDED IN PART (2026-09-17):** The C#-generated OpenAPI/JSON business authority, JIT Harness host, shared src/Web/esproj layout and two-profile limit are superseded by [P2-009](#rule-p2-009)/[P2-012](#rule-p2-012)/[P2-013](#rule-p2-013). React/TypeScript and browser cookie isolation remain binding. See [P2-013](#rule-p2-013).

**Authority and date.** Explicit user direction, 2026-09-06: redesign the Web frontend in TypeScript using Node.js and C# → OpenAPI → TS SDK; include an esproj in Windows win.slnx, while non-Windows platforms use their own toolchain directories, analogous to CMake. The user-supplied ReactApp2 template is an IDE-integration reference.

**Decision.**

1. Replace the Blazor-only Web boundary with React/React DOM, strict TypeScript, Vite and React Router; npm workspaces on pinned Node.js 24 LTS. The Site pre-renders public HTML at build time; Account/Chat are separate build profiles of one React application.
2. C# public DTOs, serializer metadata and endpoints remain authoritative. Generate OpenAPI 3.1 / JSON Schema 2020-12, then the TypeScript Fetch SDK, validators and query integrations. C# clients continue using the generated C# route; browser code uses the generated TypeScript route.
3. The existing ASP.NET Core JIT Cloud remains the single business backend and Harness host. Node is build/development/test/static-generation infrastructure; no production Node business service or runtime SSR is required.
4. One Web npm root and lockfile reside under src/Web. Windows win.slnx includes one esproj for that workspace; portable .NET projects do not depend on esproj. Non-Windows and CI run npm, dotnet and CMake in their respective boundaries.
5. Resolve [P2-003](#rule-p2-003) to the same-origin C# cookie-session adapter. Share business handlers, not browser credentials or duplicated billing/authorization logic.
6. Consumer visual quality is an explicit acceptance obligation: owned design tokens/components, representative approved layouts, complete asynchronous/failure states, responsive behavior, accessibility, production performance and browser evidence.

**Supersession.** The original [D-007](phase-1-foundation-decisions.md#rule-d-007) Blazor/RunAOTCompilation and React/TS/Node/npm prohibition is superseded for Web only. Any [D-008](phase-1-foundation-decisions.md#rule-d-008) interpretation that applies .NET/WASM flags to Web is superseded. [D-009](phase-1-foundation-decisions.md#rule-d-009)'s C# source-of-truth rule, [D-014](phase-1-foundation-decisions.md#rule-d-014)/[D-015](phase-1-foundation-decisions.md#rule-d-015)'s surface/origin rules, [D-021](phase-1-foundation-decisions.md#rule-d-021)'s licence boundary and [P2-006](#rule-p2-006)'s product scope remain effective. The Web tooling exception does not permit desktop WebViews/DOM, local AI, mobile React Native, teams, BYOK or a second agent. Public HTTP stays JSON; this is not a Fory/TypeSpec/tRPC protocol decision.

**Implementation consequence.** Reconcile obsolete Blazor Web projects, .NET Web component tests and static C# generator targets in the implementation inventory. Introduce Node/TS restore, generation, diagnostics, tests, licences/SBOM and release artifacts. Retain package identifiers and amend real dependencies rather than inventing an unrelated implementation sequence.

**Selected mechanisms and verification.** [Web architecture](../architecture/10-web-architecture.md), [Web toolchain and SDK](../architecture/25-web-toolchain-and-sdk.md), the updated Web requirements, [WP-01](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01), [WP-02](../planning/work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02), [WP-03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-05](../planning/work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05), [WP-06](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06), [WP-22](../planning/work-packages/22-identity-workspace-and-device.md#rule-wp-22), [WP-23](../planning/work-packages/23-public-api-and-generated-clients.md#rule-wp-23), [WP-24](../planning/work-packages/24-realtime-and-reliable-events.md#rule-wp-24), [WP-47](../planning/work-packages/47-static-public-site.md#rule-wp-47), [WP-48](../planning/work-packages/48-account-portal.md#rule-wp-48), [WP-49](../planning/work-packages/49-arcchat-web-companion.md#rule-wp-49), [WP-50](../planning/work-packages/50-full-platform-production-release.md#rule-wp-50) and [PG-23](../assurance/open-gates-register.md#rule-pg-23) specify producers, consumers and real execution evidence.

**Cost accepted.** A TypeScript/Node dependency and testing toolchain in return for the React design/interaction ecosystem. A monorepo remains one source tree with several toolchains, not one universal compiler. No change to desktop/mobile business scope is inferred.

---


## What was considered and deliberately not recorded

Recording a non-decision as a decision is as harmful as leaving a decision unrecorded. These were considered and rejected for entry, with the reason:

| Considered | Why it is not a Phase 2 decision |
|---|---|
| The dual capability boundary for extensions | Defined by [`../architecture/15-extension-platform-architecture.md`](../architecture/15-extension-platform-architecture.md) `§4`; it requires no additional decision or archived-source lookup |
| Three cloud runtime roles | **Historical, superseded by [P2-006](#rule-p2-006):** the current requirement is one deployable host with bounded internal services. The prior three-role interpretation remains in [`../architecture/05-cloud-architecture.md`](../architecture/05-cloud-architecture.md) `§2` |
| The eighteen test families | A design output of the quality contract, not a choice between alternatives |
| Native shims beyond the architecture's illustrative two | Governed by the permitted-surface rule ([NP-01](../architecture/12-native-interop-and-media.md#rule-np-01)) and resolved per shim in [WP-01.03](../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.03); not a global decision |
| An isolated extension host | Already governed by **[D-016](phase-1-foundation-decisions.md#rule-d-016)** and the closed technical exception list; raising one is a future decision, not a present one |
| The eleven-phase reading structure of the sequence | Presentation of a dependency graph, not a decision |
| Cloud module count reconciliation | A reconciliation finding for [WP-21.02](../planning/work-packages/21-cloud-host-and-persistence.md#rule-wp-21.02), resolved with evidence rather than by decree |

---

## Open material conflicts requiring a user decision

**None.**

### [OC-01](../assurance/open-gates-register.md#rule-oc-01) — ArcSlate reference baseline · `CLOSED 2026-09-05`

| Field | Position |
|---|---|
| **Was** | **[D-012](phase-1-foundation-decisions.md#rule-d-012)** registered Olive as an ArcSlate reference; no Olive repository existed at the authorized reference-map location |
| **Resolution** | **User decision, 2026-09-05**: ArcSlate's direct reference repositories are **ArcVideo and ArcVideoFoundation**; there is no requirement to obtain or independently review an Olive repository. Recorded as [P2-005](#rule-p2-005), and applied to **[D-012](phase-1-foundation-decisions.md#rule-d-012)** as a dated amendment |
| **Effect** | The Olive-direct audit scope and the missing-repository blocker are removed. ArcSlate's evidence rests on the two actual repositories at commits `caf5651` and `139eeca` |
| **Not removed** | **Olive-origin provenance.** ArcVideo is a documented fork; GPL-3.0 obligations, upstream copyright and attribution to the Olive authors are preserved wherever inherited material requires them ([RB-04](#rule-rb-04)) |
| **State** | **Closed.** No unresolved determination remains in the Phase 2 register |

---

### Tensions resolved without escalation

The following earlier-baseline tensions were recorded before [P2-006](#rule-p2-006). Their evidence remains historical; any affected architecture/coverage/plan must now be reconciled to the amended requirements:

| Tension | Resolution | Recorded in |
|---|---|---|
| **[D-019](phase-1-foundation-decisions.md#rule-d-019)** requires the plan to follow audits that did not exist | **Not resolvable by substitution** — the earlier attempt is withdrawn. The audits were produced, then the plan was re-derived | [P2-002](#rule-p2-002) (withdrawn) and [P2-004](#rule-p2-004) above |
| The existing monorepo's state differs materially from any assumption | Item-level reconciliation with per-project dispositions; the plan adapts to measured evidence | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) |
| Two native shims may fall outside the permitted native surface | `Fence` with a scheduled substitute analysis per shim, rather than a global judgement | there, `§5.2` [NS-07](../assurance/implementation-state-reconciliation.md#rule-ns-07), [NS-08](../assurance/implementation-state-reconciliation.md#rule-ns-08) |
| Every commercial figure in the corpus is a proposal, not a commitment | Recorded as versioned commercial policy with corpus defaults labelled proposals (**[D-020](phase-1-foundation-decisions.md#rule-d-020)**); no figure has been consumed as an authoritative specification | [`../requirements/04-commerce-entitlement-and-credits.md`](../requirements/04-commerce-entitlement-and-credits.md); [`../assurance/commercial-figure-status.md`](../assurance/commercial-figure-status.md) |

Should implementation surface a further material conflict, **[D-001](phase-1-foundation-decisions.md#rule-d-001)** governs: the work stops, the conflict is registered, and it is returned for decision rather than resolved locally.

<!-- Architecture amendment 2026-09-11 -->

<a id="rule-p2-009"></a>
## P2-009 — Independent repositories, proto, Native AOT and Cloudflare execution · ADOPTED

**SUPERSEDED IN PART (2026-09-17):** Repository count and Mobile runtime are amended by [P2-010](#rule-p2-010)/[P2-012](#rule-p2-012); current count is nine. Public native gRPC and self-managed database placement are superseded by [P2-012](#rule-p2-012). Historical RN selection is retired. See [P2-013](#rule-p2-013).

**Authority/date.** Explicit user architecture direction and authorization to apply it, 2026-09-11. This is the coordinated amendment prepared in Plan/architecture-change-plan; the formal definitions linked here are the current implementation authority.

**Decisions.** Nine peer implementation/contract repositories (count corrected 2026-09-17 under [P2-012](#rule-p2-012)) under [solution ownership](../architecture/01-solution-and-project-layout.md); reuse existing implementation history for DesktopPlatform, with capability-specific managed/RID NuGet packages. Handwritten proto in Contracts governs business RPC and generated C#/TS clients. Desktop and the single C# Cloud business host publish Native AOT. Mobile is Apache React Native/TypeScript/Hermes Android companion; iOS stays build-deferred. React Web keeps static profiles and isolated origins.

The sole AI loop is a Cloudflare Workflow in ArcForges-AI, using selected Workers AI models directly. A Durable Object coordinates bounded live presentation. C# retains all 20 business owners and canonical D1 transactions; R2 holds primary bytes behind consumption-time authorization. No production Node/Deno/Bun AI sidecar, local AI, extra Harness or generic gateway. Independent immutable disaster copy remains mandatory.

**Precise authorities.** [Wire registry](../architecture/contracts/04-protobuf-wire-registry.md), [CF/state/object contract](../architecture/contracts/05-cloudflare-integration.md), [runtime/dependency matrix](../architecture/21-platform-and-dependency-matrix.md), [implementation sequence](../planning/implementation-sequence.md).

**Specific supersession.** Amend [D-007](phase-1-foundation-decisions.md#rule-d-007)/[P2-008](#rule-p2-008) C# wire-source rule to proto; [D-008](phase-1-foundation-decisions.md#rule-d-008)/[V-03](../assurance/phase-1-official-verification.md#rule-v-03)/[V-04](../assurance/phase-1-official-verification.md#rule-v-04) Cloud JIT and Mono-AOT mobile choices to the selected Cloud Native AOT and RN runtime; [D-009](phase-1-foundation-decisions.md#rule-d-009) contract authoring/transport to proto; [D-011](phase-1-foundation-decisions.md#rule-d-011) monorepo target to the nine-repository ownership graph. [P2-006](#rule-p2-006)'s single in-host C# Harness placement becomes sole CF Workflow with C# business authority. [P2-008](#rule-p2-008)'s prohibition on RN is replaced for Mobile. The preserved quotations/dated verification in those records describe their historical decision and are not current implementation instructions.

[D-004](phase-1-foundation-decisions.md#rule-d-004)/[D-013](phase-1-foundation-decisions.md#rule-d-013)/[D-021](phase-1-foundation-decisions.md#rule-d-021) license and reference boundaries, [D-010](phase-1-foundation-decisions.md#rule-d-010) direct professional-product access and in-process application-scoped capability registry, [D-014](phase-1-foundation-decisions.md#rule-d-014)/015 origins, [D-016](phase-1-foundation-decisions.md#rule-d-016)/[P2-007](#rule-p2-007) isolation, [P2-006](#rule-p2-006) accepted commercial/product scope and all three repaired semantic profiles remain binding. No organizations, BYOK, extra agent, professional mobile editor, Notes canvas/slides/formulas/E2EE or mandatory prepayment is added.

**Implementation consequence.** WP02/03 establish exact producer artifacts; WP06 proves selected AOT/gRPC/RN/CF/R2 paths early. WP52 implements the sole CF loop after real business admission/bridge/retrieval, and WP50 joins real deployment/restore evidence. Documentation review does not satisfy those runtime gates.

<a id="rule-p2-010"></a>
## P2-010 — Android and Complete Producer Contracts

**SUPERSEDED IN PART (2026-09-17):** The public C#/Kotlin native-gRPC clause is superseded by [P2-012](#rule-p2-012): all public clients use binary gRPC-Web. The Android/native ABI/product scope remains binding. See [P2-013](#rule-p2-013).

Accepted 2026-09-13 by the product owner's current direction. Mobile uses Kotlin/JVM and Jetpack Compose for Android only, replacing the Mobile runtime/retained-iOS portions of [P2-009](#rule-p2-009) and [D-008](phase-1-foundation-decisions.md#rule-d-008). Its complete ArcChat companion scope and Apache-2.0 boundary remain. iOS/KMP is outside this delivery, not a required dormant implementation.

Contracts is Apache-2.0 throughout, including internal schemas and tooling. Access control and import direction still separate public clients from operator/local/internal protocols; they are not licence differences. C# and Kotlin use native gRPC; TypeScript Web uses gRPC-Web. Contracts adds generated Java/Kotlin-lite messages and coroutine clients on Maven Central. No shared or adjacent source dependency is introduced.

The complete initial native ABI, generated wire/journey profiles, product behavior, extension/policy schemas and artifact-stage plan are specified before consumer work. [Native ABI](../architecture/contracts/06-native-functional-abi.md), [client journeys](../architecture/contracts/07-client-journeys-and-ports.md), [extension/policy profiles](../architecture/contracts/08-extension-and-policy-profiles.md) and [product profiles](../architecture/26-product-behavior-profiles.md) supplement their existing authorities. Active contradictory bodies are corrected; historical reviews remain dated evidence.

[P2-006](#rule-p2-006) product exclusions, the nine repositories, sole CF Harness, C# business authority, R2, all accepted product capabilities, exact-value/provenance/accounting/recovery constraints remain. No promise of immutable forever APIs is made: compatible evolution and tested consumer pin updates remain required. [Stage ownership](../planning/producer-artifacts-and-integration.md) distinguishes initial protocol/native probes from full real-product integration and commercial activation. Documentary verification is not product runtime evidence.

[P2-010](#rule-p2-010) device/transient protection clarification: Android OS-Keystore-bound application values and the separately expiring temporary-chat body store are implementation protection for the declared session/privacy lifecycle. They do not introduce a user-managed encrypted notebook/archive format, E2EE sync, key-sharing product or encrypted export, which remain excluded by [P2-006](#rule-p2-006). Existing exclusion wording is read with that explicit distinction.


<a id="rule-p2-011"></a>
## P2-011 — Producer closure and uniform local gRPC · ADOPTED

**SUPERSEDED IN PART (2026-09-17):** Independent peer discovery, leases, reverse endpoints and Device SSO are superseded by [P2-012](#rule-p2-012). Only parent-owned helper/extension controls use private generated gRPC; typed product ports are in-process. See [P2-013](#rule-p2-013).

**Authority/date.** User authorization on2026-09-14 to validate the independent findings, apply justified repairs and use port-free proto/gRPC for all local first-party control. Collection and unified adoption were committed in the local Plan repository before formal edits. This is a documentation amendment, not implemented-product evidence.

**Decisions.** [WP13](../planning/work-packages/13-high-risk-technical-probes.md) explicitly produces all seven native functional families, while WP11 solely produces restricted helper/Broker/Contracts. [WP53](../planning/work-packages/53-desktop-distribution-and-update.md) produces the shared desktop updater using the already selected Velopack integration. WP45.09 produces Android FCM sending; PG24 binds live sending and physical Mobile receipt. D1 outbox/inbox, EventService.Poll and CF presentation replace residual managed broker/realtime deployment claims. Catalogue00 exports closed effective authorization/egress/actor profiles; human-only decisions never become model tools.

All first-party same-machine application/control RPC, including ContentSandbox, uses authored proto and native gRPC over Windows Named Pipes or Linux/macOS Unix streams. The [local profile](../architecture/contracts/09-local-grpc-and-sandbox.md) fixes complete numbered services, discovery, OS/launch identity, bootstrap proof, independent peer lease, call bounds, reverse endpoint roles, local hints, connector/SSO and helper buffer/recovery behavior. It supersedes the [P2-009](#rule-p2-009) private-helper/XPC application-protocol exception. OS launch/finite handle provisioning and same-process C ABI are not RPC; standard external MCP/device/provider adapters retain their accepted protocols. No TCP fallback or unspecified serializer is allowed.

**Preserved scope.** All accepted products and desktop tiers, Android-only Kotlin/Compose companion, Cloud authority/transactions, one CF Harness, source/permission/commercial/time/measurement/recovery invariants remain binding. No iOS work, new agent host, native business worker or reduced release scope is introduced. Independent package-only consumers precede promotion; later product and external gates cannot be satisfied with schemas or mocks.

**Evidence and implementation.** The [current closure review](../assurance/producer-and-local-grpc-closure-review.md) records source snapshots, concrete repairs and mechanical verification. The corrected graph has51 active WPs and157 edges; PG24 adds one external runtime obligation. Actual AOT, native behavior, OS containment, CF/provider/device and commercial evidence remains at the named producers and consumers. Historical dated reviews retain their original baseline and counts.

<a id="rule-p2-012"></a>
## P2-012 — Cloudflare Runtime and Independent Application Assistants · ADOPTED

Date: 2026-09-16. Source: current user direction. Supersedes the remaining application runtime/standalone ArcChat, PostgreSQL, native-public-gRPC/AI-WebSocket and current cross-product collaboration portions of [P2-009](#rule-p2-009)/[P2-011](#rule-p2-011). Native functional ABI, Kotlin Android, exact contracts, product correctness, permissions and commercial rules remain binding.

The current family has nine delivery repositories and three professional desktop executables. DesktopPlatform publishes complete reusable assistant/core/store/Cloud/Avalonia packages; each application owns its own instances, windows, database and Cloud connection. Product domain/application/infrastructure libraries remain product-owned. Local history defaults on desktop; explicit Cloud history and bounded transient AI processing follow the application-history profile. Android is the sole mobile target with complete native UI, own conversations and authorized one-app device control.

All first-party public business clients use binary gRPC-Web unary methods and bounded server streams. C# Native AOT runs in Cloudflare Containers; Worker bindings expose D1/R2/DO, Queues/Cron wake bounded work, and the sole Harness remains the AI Workflow with Workers AI. D1 guarded atomic plans retain the existing business transaction families. Derived search uses D1 FTS5/Vectorize. Independent immutable S3 disaster backup remains an explicit existing exception; primary runtime/storage uses Cloudflare. No runtime-equivalence or capacity claim is inferred from documentation.

Ordinary applications have no local peer-discovery/RPC or shared application runtime. In-process typed product ports and Cloud-targeted device actions replace them. Parent-owned parser/extension gRPC over Named Pipe/UDS remains required. Cross-product collaboration is FUTURE only; WP20 has no active dependencies. Video-summary/report-to-Notes examples are separately recorded and do not enter current release gates.

Authorities: [projects/packages](../architecture/27-platform-projects-and-application-assistants.md), [D1](../architecture/data-model/04-d1-execution-profile.md), [history](../architecture/data-model/05-application-history.md), [protocol/scope](../architecture/contracts/10-application-scope-and-streams.md), [experience](../experience/README.md), [future](../future/cross-product-collaboration/README.md). The corresponding current requirements, main-body work steps and acceptance are updated together. Real AOT, deployed CF, Android devices and commercial operation remain open implementation evidence.


---

<a id="rule-p2-013"></a>

## P2-013 — Independent review remediation · ADOPTED

**Authority/date.** 2026-09-17, the user's instruction to carry out the complete review repair, with bounded design discretion already delegated for accepted scope. Baseline: Design `8b60426`; reviewed findings: Plan `9771885`. This records design dispositions, not additional user signatures, approved numeric prices or runtime evidence.

**Commercial reconciliation.** IRQ-1 default A is adopted: no free official Cloud service tier, no trial or promotion source. New official notebook enrolment, sync writes, Cloud history/search, remote agent work, simulator and AI require an active paid term. Account management, purchase, retained-data read/export and pending-work recovery remain available subject to retention/security. IRQ-2 default A is adopted: web-search requests are operator-funded; model tokens processing results use customer AI capacity. Existing requirements and metering architecture support these choices.

**Acceptance figures.** New capacity, playback and simulator-latency values are proposed acceptance targets under [D-020](phase-1-foundation-decisions.md#rule-d-020); approval and measurement remain release prerequisites. No implementation or commercial gate is passed by this record.

**Editing rule.** Repair conflicting authoritative bodies in place. Keep historical quotations and dated evidence, with explicit supersession. A new annex cannot leave contradictory active requirements, tables or work steps in force.

**Adopted dispositions and authoritative destinations.** Shorthand: registry04 = contracts/04; annexNN = contracts/NN; modelNN = data-model/NN; archNN = architecture/NN; reqNN = requirements/NN.

| ID | Decision | Resolves | Authoritative destination | Replaces or retires |
|---|---|---|---|---|
| <a id="rule-ird-01"></a>IRD-01 | Repairs rewrite conflicting text in place; historical quotations get dated supersession markers; appended override/addition sections are prohibited. | IRF-01, IRF-02, IRF-13, IRF-35 (all repairs) | Decision README; model01 rule; [P2-013](#rule-p2-013) | "Override banner" and "additions" pattern |
| <a id="rule-ird-02"></a>IRD-02 | Closed `productId` = `arcnotes`, `arcscope`, `arcslate`, `companion`. Platform is a separate field. `assistant` is a feature-family namespace. | IRF-04, IRF-13 | Glossary; registry04; annex10; model01 §5 | `arcchat`, `arcchat-mobile`, `mobile`, `web` product values; `ios` platform value (number reserved) |
| <a id="rule-ird-03"></a>IRD-03 | Durable presence facts are the D1 `device.installation` row plus trust/remote policy. Volatile presence lives only in the `ApplicationPresence` DO, and `application.heartbeat` is the only heartbeat. The `application.presenceChanged` hint replaces `device.presenceChanged` (17 hints in total). | IRF-04 | registry04 §4–§7; annex10; model01 §5; model04 §1 | `device.heartbeat`, `InstancePresence`, `PresenceLease`, `device.presence` table |
| <a id="rule-ird-04"></a>IRD-04 | The only public AI output path is binary gRPC-Web `ExecutionService.ReadOutput`/`WatchOutput`; `task.readStream` is a semantic alias. arch17 §7.2 fields map onto `StreamPosition`/`OutputChunk`/`StreamReset`/`ExecutionOutput`. | IRF-05 | annex10; arch17 §7.2 | `/ai/v1/*` public routes, connect nonce, WebSocket frames, JSON read object |
| <a id="rule-ird-05"></a>IRD-05 | `TaskState` is the registry enum (`queued, running, waiting, paused, interrupted, succeeded, partiallySucceeded, failed, canceled`) plus a closed `reasonFacet` registry (`waiting.approval/device/capacity/promotion/control`). Uncertainty is expressed as `hasUnknownEffect`. The spelling is `canceled` everywhere. | IRF-06 | registry04 §3; contracts01 §7.1 (presentation mapping) | `created`, `waitingApproval/Device/Capacity`, `unknownEffect` as states; `cancelled` |
| <a id="rule-ird-06"></a>IRD-06 | No Device SSO in this release. Native sign-in runs through the system browser (authorization code + PKCE) with per-client redirects: desktop `com.arcforges.<product>:/auth/callback`; Android App Link `https://account.arcforges.com/native/android/callback`. Two new exceptions, `GET /session/v1/native/authorize` and `POST /session/v1/native/token`. Email-code sign-in stays native. Android may use Credential Manager passkeys (RP ID `arcforges.com`, official realm only). PATs are sent as `authorization: Bearer` on gRPC-Web, only for `patEligible` operations within their scopes. | IRF-08 (also IRF-21, IRF-30) | registry04; manifest11; contracts07 §1; arch08; catalogue00 | `identity.begin/completeDeviceSso`, `DeviceSsoChallenge/Account`, broker rows, SSO `security_flow` kind |
| <a id="rule-ird-07"></a>IRD-07 | Exactly three local child kinds exist: ContentSandbox, executable extension, and connector/MCP-stdio. Each is launched by its owning application with the HMAC launch-secret bootstrap. Product ports are in-process typed records. `ILocalEvents` and `IResourceAccess` exist only on the extension/connector boundary. `Handoff` becomes `OpenArtifact`. Hub-era records move to a future package. | IRF-09 (also IRF-35) | annex09; contracts02; registry04 §4/§6; manifest11 | Discovery manifests, OS-peer bootstrap for independent peers, peer leases, `BeginTransfer`/`TransferRequest`, `IChatOperations.Handoff` |
| <a id="rule-ird-08"></a>IRD-08 | D1-feasible mechanics: guarded batches in [SU-04](../architecture/data-model/00-data-model-overview.md#rule-su-04) statement order; bootstrap with a lower-bound cursor, followed by replay from W; a read-then-guard publisher. The release manifest records the Cloudflare registry digest, the deployed compatibility date and the D1 schema/plan hashes. The backup manifest records the export bookmark and replay sequence range. The configuration field becomes `metadataRpoSeconds`. JSON `TEXT` replaces array and `jsonb` types. | IRF-12 | model04 §5; model00; model01; contracts05; annex08; arch14; arch22 | Locks, deadlock retry, REPEATABLE READ, PostgreSQL pseudo-code, WAL fields, GHCR, engine `18.6`, fixed compatibility date |
| <a id="rule-ird-09"></a>IRD-09 | model05 is the only assistant store schema. model02 §2 content moves into typed `assistant_*` tables. Message parts are protobuf `body_proto`. Room mirrors the same logical schema. | IRF-14 | model05 §3 | model02 §2 ArcChat local store |
| <a id="rule-ird-10"></a>IRD-10 | The typed local-history window preserves message roles, IDs, ordering and trust; it contains the applicable compaction record plus committed branch messages after it, with the new message in parts. Large windows use a verified transient input object. Compaction is requested with `compactionRequested` and performed by the Harness under [HC-08](../architecture/17-agent-harness.md#rule-hc-08). Summaries are stored in `assistant_compaction` (local), `chat.compaction_record` (Cloud), or memory only (temporary). There is one protected set and one refusal, `validation.invalid_request` / `context.protected_overflow`. | IRF-15 | annex10 §2; model05; model03; arch17 [HC-09](../architecture/17-agent-harness.md#rule-hc-09) | Unstated window; contracts07 duplicate protected list and code |
| <a id="rule-ird-11"></a>IRD-11 | D1 placement thresholds apply: bodies over 16 KiB and exported audit older than 90 days go to R2. A capacity profile is added (a proposal needing approval). New release gate [L-16](../assurance/release-gates.md#rule-l-16) is a production-shaped capacity test. A growth trigger at a 60 % forecast within 180 days requires a partitioning decision; until then onboarding stops at 80 %. | IRF-16 | model04 §6; model01 §8.4; release gates; open-gates register | Undefined "large eligible bodies"; unquantified launch readiness |
| <a id="rule-ird-12"></a>IRD-12 | Public route table (`api.*`, `account.*`, `chat.*`, apex, `ops.*`, `/webhooks/*` on `api.*`). The Cloud Worker is the only Container ingress. Container egress goes only through outbound-handler hosts (`storage.internal`, `objects.internal`, `ai.internal`, `feeds.internal`) and the listed providers. The AI Worker reaches C# only through a service binding, and its egress is limited to Workers AI, Brave and admitted connector/MCP origins. HMAC stays as defense in depth. | IRF-17 (also IRF-29) | arch05; arch10; contracts05 §2; model04 §1 | "TLS peer binding and ingress allowlist"; the Hello route `arcforges.com/api/*` (retired at WP21) |
| <a id="rule-ird-13"></a>IRD-13 | Cloudflare operational equivalents: Worker secrets/Secrets Store; signed configuration activation; versioned Wrangler rollouts. [L-02](../assurance/release-gates.md#rule-l-02) becomes D1 Time Travel plus fresh-environment import; [L-07](../assurance/release-gates.md#rule-l-07) becomes a Cloudflare edge outage; [L-10](../assurance/release-gates.md#rule-l-10) and WP50 gate 5 become a fresh-environment rebuild. Provider keys are held per environment. | IRF-19 | arcforges-cloud; req11 DC; arch05; arch16 [CG-06](../architecture/16-billing-and-commerce-architecture.md#rule-cg-06); arch22; release gates; WP50 | Zone redundancy, Terraform regions, connectors, pooling, key vault, Docker secrets/mounts, database failover, region rebuild |
| <a id="rule-ird-14"></a>IRD-14 | Postmark is primary and SES v2 secondary, subject to [D-003](phase-1-foundation-decisions.md#rule-d-003). Postmark callbacks use authenticated HTTPS, not a nonexistent signature; ambiguous sends are reconciled before any retry. The `notify.` and `news.` subdomains carry SPF, DKIM and DMARC `p=reject`. The Operations Owner selects status, incident, telemetry and analytics services before WP45. `configuration.v1` gains `email`, `push`, `operatorIdentity`, `serviceKeys`, `origins`, `observability` and `status` sections. An email fixture row is added to the scaffolding table. | IRF-20 | arch13; annex08 §6; implementation sequence §3.1; WP22; WP45 | "Provider selection is configuration" without a selection |
| <a id="rule-ird-15"></a>IRD-15 | `selfhost.v1`: the same artifacts deployed into the operator's Cloudflare account, with payments disabled, a configurable OIDC issuer and operator-credentialed adapters. A signed `/.well-known/arcforges-realm.json` descriptor is pinned on first use. Declared differences: no official-app background push; Android sign-in uses the private-use redirect; native Android passkeys only where the operator publishes Digital Asset Links for the official app. Plan steps are added to WP21/WP46/WP50, and gate [PG-25](../assurance/open-gates-register.md#rule-pg-25) is created. | IRF-21 | req03 §17; arch22; arch08; registry04 exceptions; open-gates register | Docker-era self-host wording; unstated feature differences |
| <a id="rule-ird-16"></a>IRD-16 | A coordination-only `SimulationPacer` DO alarm drives real-time segments (default 1 s, bounded 0.25–10 s). The latency target of 5 s is a proposal. Accelerated runs use back-to-back job slices. [SIM-10](../requirements/products/arcscope.md#rule-sim-10) reads "bounded job slices in the Cloud Container". | IRF-22 | arch23 §1; model04 §1/§5; arcscope [SIM-10](../requirements/products/arcscope.md#rule-sim-10); WP51 | "Single ASP.NET Core host", hosted-service generation loop |
| <a id="rule-ird-17"></a>IRD-17 | **IRQ-1 default A.** No free official Cloud tier; enrolment, sync, history, search, remote work, the simulator and AI require an active paid term. One grant-source vocabulary ([GR-02](../requirements/04-commerce-entitlement-and-credits.md#rule-gr-02)). `grant.kind ∈ {capability, quota, allowance}`. `SubscriptionState {pending, active, grace, cancelScheduled, ended, suspended}`. | IRF-24 | req00 [C-05](../requirements/00-product-scope-and-portfolio.md#rule-c-05); req04; arch16 [EO-04](../architecture/16-billing-and-commerce-architecture.md#rule-eo-04)/[EO-05](../architecture/16-billing-and-commerce-architecture.md#rule-eo-05); model01; registry04; [P2-013](#rule-p2-013) | `promotional`, `trial`, `store`, `free` sources; `trialing` and other model01 states; `credit`/`feature` kinds |
| <a id="rule-ird-18"></a>IRD-18 | **IRQ-2 default A.** A web-search request is operator-funded within `search.operatorBudget`; the tokens that process search results are customer-metered. The disclosure copy is fixed. | IRF-25 | req05; req06; arcchat [SE-08](../requirements/products/arcchat.md#rule-se-08); arch16; [P2-013](#rule-p2-013) | "Web search costs credits" statements |
| <a id="rule-ird-19"></a>IRD-19 | Workers AI is the only V1 supplier. Cost classes map to configured model profiles (`fast` = gpt-oss-20b, `balanced` = gpt-oss-120b). There is no automatic model fallback, and outages return a named unavailability reason. Unknown-effect step 3 is not applicable to Workers AI. Multi-provider pricing vectors are synthetic unit tests only. | IRF-26 | req05 §11.5; req04; arch09; arch17 §6.4; arcforges-cloud; release gate [L-06](../assurance/release-gates.md#rule-l-06); WP43 | Gateway → direct providers → aggregator; direct-provider bypass; "selected fallback policy" |
| <a id="rule-ird-20"></a>IRD-20 | ArcNotes export is the Cloud export job. Offline safety is the [DL-01](../requirements/02-identity-account-and-workspace.md#rule-dl-01) recovery view with Markdown copy/save. Local assistant history exports as `assistant-history.v1` with an optional Markdown transcript. Cloud assistant history uses the owned Cloud export. | IRF-27 | WP19; arcchat [EX-01](../requirements/products/arcchat.md#rule-ex-01); model05 §4; model02 §6 | WP19.05 offline native export; [BR-07](../planning/work-packages/19-arcnotes-search-and-portability.md#rule-br-07) re-import claim; "no local conversation archive" |
| <a id="rule-ird-21"></a>IRD-21 | New twenty-first Cloud module `PackageCatalog` (publisher, package, version, review, revocation) with catalog operations and operator review. A signed static `catalog-index.v1` and `catalog-revocations.v1` are served from `downloads.`. No community ratings in V1. | IRF-28 | arch15 §9; registry04; manifest11; model01; arch05; WP41; WP45 | Unowned "Cloud catalog"; the WP42 `Modules.Catalog` name |
| <a id="rule-ird-22"></a>IRD-22 | The extension wire protocol is authored proto; the SDK generator covers only `ValueSchema`/`StructuredValue` payloads and manifests. Third-party Arc Apps integrate through the public API, file formats and OS open/share. MCP `stdio` runs on the desktop only. MCP `streamableHttp` runs as a local connection or as a Cloud connection through the AI Worker tool adapter. | IRF-29 | req08; arch15; annex08; WP41 | C#-record wire generation; "same-application contribution model" for third-party apps |
| <a id="rule-ird-23"></a>IRD-23 | The permanent Android package name is `com.arcforges.mobile`, adopted before any Play or production distribution. Exact toolchain pins live in per-repository manifests (as for Contracts, IRF-11). JDK 21 and stable releases only. The arch27 module layout applies; `shared` KMP is kept as a preview host only. | IRF-30 (with IRF-11) | arch11; arch27; WP30; WP32; registry04 §8; WP02 | The "preserve" premise; patch pins in arch11 and registry04 |
| <a id="rule-ird-24"></a>IRD-24 | Play is the primary Android channel. The direct APK is served from `downloads.` with a signed notify-only update manifest on `updates.`. GitHub Releases are an archive and mirror only. Switching channels requires a reinstall. | IRF-31 | arch11; arch14; WP32; WP53 | GitHub Releases as a distribution channel |
| <a id="rule-ird-25"></a>IRD-25 | The listed work-package bodies are rebaselined to nine repositories, three professional products, parent/child local RPC, gRPC-Web business RPC and current Cloud mechanisms. The WP42 payout gate moves to WP50. Evidence-driven revisions get supersession markers. | IRF-35 | WP files; implementation sequence §3.1; contracts01 [CH-03](../architecture/contracts/01-public-api-operations.md#rule-ch-03); evidence-driven revisions | Monorepo, four-product, peer-RPC, OpenAPI-authority and hosted-service premises |
| <a id="rule-ird-26"></a>IRD-26 | Assurance oracles are regenerated after the content repairs. End-to-end §6.1 becomes two own-application scenarios. New trace rows cover native sign-in, promotion/export, catalog revocation, self-host, [L-16](../assurance/release-gates.md#rule-l-16) and simulator pacing. | IRF-36 | Assurance files | Cross-product §6.1 oracle; pre-P2-012 matrices |

**Execution corrections.** Native login and transactional-mail adapters are produced by WP22, including the minimal system-browser ceremony; later WP45/WP48 operational/full-account surfaces are not prerequisites. Signed catalog/update schemas are defined by WP03, test identities by WP02/06, consumers by WP41/32, production keys/feeds by WP53 and live end-to-end distribution by WP50. Local-history transcript roles are context only and never authority. An oversized context uses the existing verified transient object channel. MCP stdio remains its explicit third-party protocol exception. DO alarms provide at-least-once scheduling; checkpoints, fences and Cron rescue handle duplicate/lost wakes. CI uses workload federation where supported; Cloudflare Wrangler deployment uses a protected, narrowly scoped, expiring API token under its documented authentication model.

**Bounded repairs.** IRF-03 restores historical vocabulary, CI identity and Pearson cross-products. IRF-07 unifies tool-result identity. IRF-10/11 unify transport and toolchain ownership. IRF-13/14 consolidate schemas. IRF-18 scopes search before candidate generation. IRF-23 fixes proration and uncertain reservations. IRF-32/33 align directories and outputs. IRF-34 fixes isolation budgets, math, undo and PDF adoption. IRF-37 repairs navigation and derived-store terminology. Each is applied in its existing owner, not a competing replacement specification.

**Specific supersession.** [P2-006](#rule-p2-006) host placement; [P2-008](#rule-p2-008) generated OpenAPI/JSON business authority; [P2-009](#rule-p2-009) RN and historical ten-repository count; [P2-010](#rule-p2-010) public native gRPC; [P2-011](#rule-p2-011) independent peers and SSO; all phase-1 disposition rows marked amended/superseded. Unchanged scope, permissions, accounting, measurement, media time, provenance, recovery and licence obligations remain binding.

**Preserved scope.** Three independent professional desktops, embedded assistants, Android and Web companions, self-hosting, deterministic simulator, developer platform/catalog and complete commercial operations. Cross-product collaboration remains future-only; iOS, local AI, BYOK and agent teams are not introduced.


<a id="rule-p2-014"></a>
## P2-014 — Final independent findings closure

**Status: accepted design selection, 2026-09-18.** Applies the bounded final review of merged `70a04d4` (Plan review `1f5e560` / `fee5e4c`) and execution plan `eb6e7dd`. It completes [P2-012](#rule-p2-012)/[P2-013](#rule-p2-013) without changing the accepted product portfolio. The original conflicting normative text is replaced at its owner; dated verification records remain historical evidence.

| Decision | Authority and implementation consequence |
|---|---|
| No application Device SSO | Each application performs its own browser ceremony and stores its own session. Remove sibling bootstrap/signing/broker requirements from security, contracts and WP22. Only independently specified parent/child isolation remains local IPC. |
| Tool-result identity | `(toolRequestId, attemptId, commandId)` plus canonical result hash; Task and ChatTurn owners accept multiple results per attempt and reconcile identical retries. |
| Complete operator surface | Registry04 §9 owns every internal method, [OC-03](../requirements/10-distribution-update-and-support.md#rule-oc-03) role binding, eight-field authorization profile, typed dual-approval/financial/case behavior and owner commit. Manifest11 includes all 31 operator methods. Customer/PAT/agent credentials are excluded. |
| Module versus repository count | 21 Cloud domain modules include PackageCatalog; there are nine independent implementation repositories. Audit owns operator proposals; domain owners execute effects. No Operations data module or extra business host is created. |
| Bounded Cloud execution | SimulationPacer/Cron wake bounded C# slices; verified segment, checkpoint and continuation outbox commit in one guarded D1 batch. Restore uses D1 export/bookmark/replay, R2 inventory and independent safety journal. |
| Concrete launch profile | Model04 selects standard-2, four global fixed realm slots, ten-minute idle sleep, explicit first-response deadlines and Vectorize/R2 allocations/reservations. These are implementation/load targets, not hidden purchased quotas or achieved capacity. Real [L-16](../assurance/release-gates.md#rule-l-16)/[PG-26](../assurance/open-gates-register.md#rule-pg-26) cost/performance approval remains mandatory. |
| Concrete browser policy | Requirements12 browser-support.v1 defines engines/OS, build floors, deterministic current/previous release selection, exact versioned artifact, polling fallback and fail-closed step-up/preview. All four Web outputs consume it. |
| Real email and accurate portability | WP22 proves actual delivery/recovery before completion; recorded failures are regression-only. Notes exports retain the specified Cloud Markdown/attachments/manifest/fidelity path, not an excluded native archive importer. |
| Verifiable propagation | Exact operation counts, table schemas and vocabulary, rule links, graph and affected consumer gates are checked; the five-column dispositions register is restored. |

See the [final findings verification](../assurance/final-findings-remediation-verification.md). Documentation/source/SQLite example checks do not close real AOT, Cloudflare, browser, Android, native, provider, payment or commercial gates. [D-020](phase-1-foundation-decisions.md#rule-d-020) approval requirements for cost/performance remain effective.


<a id="rule-p2-015"></a>
## P2-015 — Executable naming freeze under the current portfolio

**Status: accepted bounded implementation clarification, 2026-09-18.** Authority: the user's delegated planning-repair discretion for WP00.00. Collection used Design `575ba9f` and all nine current origin/main implementation snapshots. This resolves residual four-product wording, an incorrect legacy-to-Scope mapping and the previously unassigned naming-data owner before implementation.

The current desktop products remain ArcNotes, ArcScope and ArcSlate. `companion` is the fourth wire ProductId; `assistant` is a feature namespace and ArcChat is not an executable/product ID. Contracts owns one Apache-2.0 naming JSON and a portable scanner under the [naming policy](../architecture/28-product-naming-policy.md). Closed-schema forbidden-name declarations are data to validate; exact hash-bound reference provenance is the only scan exception. No blanket source, generated, test or documentation exclusion is permitted in implementation repositories.

Reserve identifiers only for the already required Scope/Slate native projects; Notes and assistant history gain no native archive or default association. Preserve desktop bundle/assembly/package identities. The accepted WP30 development-prerelease Android rename remains at its owner; no production migration or signing continuity is claimed by WP00.00. WP02/WP05 consume this policy for continuing family enforcement; WP33/WP36/WP53 implement and test native associations. Existing package consumers and wire tags are unchanged.

Inventory refinement on 2026-09-18: the actual Git scan includes the tracked-but-ignored DesktopPlatform traceability seed, missed by an ignore-aware text search. Its 50 matching values are reference repository names plus exact commits, all under `sourceBaselines`. The naming policy admits that one unchanged, hash-bound provenance artifact alongside normal provenance records; no source or artifact directory exemption is introduced.

Verification: schema/identity checks, positive and adversarial scanner tests, nine actual Git inventories, Contracts CI and post-merge rescan. Documentation review and a clean naming scan do not establish product, installer, AOT, device, payment or commercial readiness.

<a id="rule-p2-016"></a>
## P2-016 — Reproducible glossary and invariant policy exports

**Status: accepted bounded implementation clarification, 2026-09-18.** Authority: the user's delegated planning-repair discretion for WP00.01. Collection used Design `4382eec`, the merged naming policy, all nine current implementation roots and the existing historical checkers.

DesktopPlatform owns the AGPL Design-derived vocabulary/invariant exports and portable continuing corpus check under the [export profile](../architecture/29-design-policy-export.md). Product term rows receive explicit spaces and complete namespace spellings; the already specified simulator objects become table rows. Retired rows remain retired. No domain scope, wire tag, stored format or runtime alias is added. The coverage mechanism totals are recomputed from the 429 mapped rows, including the two existing exclusion/architecture checks.

The current document corpus, graph and source-to-export round trip are checked from one pinned Design commit. Historical programs, reserved identifiers and exact historical review occurrences are classified separately; they cannot hide current citations or create current gates. Contracts can validate the exact generated forbidden-alias declaration digest at its one assigned location without admitting arbitrary source or documentation exceptions. This refines [P2-015](#rule-p2-015)'s declaration handling while preserving its authored naming authority and provenance constraints.

Verification requires complete citation/definition and dependency reports, exact two-way export equality and meaningful negative drift fixtures in CI. WP02/WP05 distribute and extend build policy; invariant owners still owe implemented checks under [PG-11](../assurance/open-gates-register.md#rule-pg-11). Policy data and documentation checks are not product runtime evidence.

<a id="rule-p2-017"></a>
## P2-017 — Bounded CI and local verification

**AMENDED IN PART (2026-09-23):** [P2-018](#rule-p2-018) replaces this record's coordinator and numbered-substep wording with task-level coordination: independent delivery tasks run concurrently, each repository's integration owner merges and publishes, and CPU-heavy local work stays serialized per workstation. The validation substance below is unchanged.

**Status: accepted explicit user change, 2026-09-21.** All nine owners, Design and Plan follow the [CI and local validation policy](../assurance/ci-and-local-validation-policy.md). It prohibits all macOS CI and hosted device/emulator, GUI/browser E2E, live service/inference, installed-consumer and public-release upgrade tests. Runtime checks are affected-scope local opt-in using the existing environment, not repeated pipeline or post-merge gates. Necessary Windows/Linux compile/AOT/package, offline unit/static/security and signing/licence/lock integrity remain. Publication uses the original candidate and provider status, without routine public downloads or repeated hashes.

The coordinator may delegate independent repositories while serializing CPU-heavy local work. Active pipeline, candidate inventories, AGENTS and execution profiles must match; old receipts remain historical. macOS product intent is unchanged, but no macOS CI artifact or runtime support is inferred. This amends the execution venue/cadence of earlier test and producer gates, not the product behavior, security boundaries or immutable release rules. It does not authorize beginning another numbered substep.

**Accepted user clarification, 2026-09-22.** Documentation-only PRs in documentation repositories with no configured CI merge after review. Repositories with CI retain all applicable required checks even when the diff contains only documentation; skip-CI directives, workflow disabling and bypasses are not substitutes for those checks. Documentation changes need no additional ad-hoc local product builds or runtime tests. The [policy](../assurance/ci-and-local-validation-policy.md) and repository instructions apply this distinction.

<a id="rule-p2-018"></a>
## P2-018 — Parallel delivery graph and multi-worker execution

**Status: accepted explicit user change, 2026-09-23.** The user directed that ArcForges implementation planning be rebuilt for maximum practical parallel execution across the family and within each application, with the accepted product, requirements, business semantics, user journeys, data ownership, security boundaries, compatibility, recovery, licensing and commercial acceptance preserved, and with existing implementation carried forward through an explicit adoption stage rather than discarded. This record amends [D-019](phase-1-foundation-decisions.md#rule-d-019) under [D-001](phase-1-foundation-decisions.md#rule-d-001) and [RC-01](#rule-rc-01).

**Decisions.**

1. The numbered work packages and their substeps remain the obligation catalogue: identity, required outcome, tests, completion gates and deferred-gate scheduling are unchanged. They are no longer scheduling units, and their numbering implies no execution order.
2. The [delivery graph](../planning/delivery/delivery-graph.json) is the single scheduling authority. Its delivery tasks each have one owning repository, the obligations or named obligation parts they satisfy, typed start prerequisites (contract, artifact, design), completion prerequisites (integration), release prerequisites for release tasks only, declared shared resources, permitted contract-bound substitutes, validation and evidence. All other planning representations are generated from it. The rules are in the [delivery model](../planning/delivery/README.md).
3. Any number of workers may execute ready tasks concurrently. A task is ready when the adoption slice for its repository and lane is complete and its start prerequisites are satisfied: a contract, artifact or design prerequisite by the producer's delivered outcome, a release prerequisite only by completion. It is claimed through an atomic claim branch with a lease in the Plan repository; interrupted work resumes from its retained worktree and pull request, and re-claiming a released task or taking over an expired lease is an atomic append to the same claim.
4. Coordination moves to the narrowest boundary: a per-repository integration owner for merges, shared files, generated baselines and publication; the Architecture Owner for contract and design changes; the Release Engineering Owner for release tasks. No family-wide merge order, single Current task or wave boundary exists.
5. Contract-bound substitutes may unblock the start of work. They never satisfy a real-integration, runtime, device, provider or commercial gate; each names its real producer and the integration task that removes it. The binding mock policy, must-be-real-early list and scaffolding deletion rules are unchanged.
6. One adoption stage reviews existing implementation and accepted evidence against the graph in independently claimable slices, one per repository and lane; each slice classifies its tasks as inherited, adjusted, gap or conflicting, records the result in the Plan ledger and opens only its own tasks. This decision certifies no existing implementation. The accepted baseline is complete through [WP-03.02](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.02); [WP-03.03](../planning/work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03.03) has not started.

**Specific supersession.** The [D-019](phase-1-foundation-decisions.md#rule-d-019) requirements that one serial numbered sequence be advanced serially by one main context and that implementation ownership never be split across autonomous agent teams are superseded; its requirement that the plan be derived only after requirements, architecture, licence matrices and current-code reconciliation remains, and [P2-004](#rule-p2-004) remains its record. The serial-execution rules previously stated as [PA-01](../planning/implementation-sequence.md#rule-pa-01), [PA-03](../planning/implementation-sequence.md#rule-pa-03), [WF-04](../planning/implementation-sequence.md#rule-wf-04) and [ND-01](../planning/implementation-sequence.md#rule-nd-01), the "one main context" work-package convention, the work-package level dependency table, its serial execution list and the single Current task of the Plan repository are replaced in place by task-level rules. [P2-017](#rule-p2-017) is unchanged in validation substance; its coordinator wording now reads through the per-repository coordination above, and CPU-heavy local work remains serialized per workstation.

**Preserved scope.** All 51 active work packages and 447 substeps with their gates, the retired status of WP27/WP29, future-only WP20, the nine repositories, three independent professional desktops with embedded assistants, the Android and Web companions, Cloudflare hosting with C# business authority, the sole Cloud Harness, self-hosting, the deterministic simulator, the developer platform and catalog, and complete commercial operation remain required. No requirement is deferred out of scope, no acceptance is weakened, and no product or technology strategy changes.

**Enforcement.** The Plan repository's `tools/delivery.py check` validates references, acyclic prerequisites, complete substep and package-obligation coverage, substitute replacement, shared-resource declarations and generated-view currency. DesktopPlatform's design-policy graph check still validates the retired work-package graph at its pinned Design commit; its replacement is a scheduled delivery task and a precondition for moving that pin. This record is a planning amendment, not implementation, runtime or commercial evidence.
