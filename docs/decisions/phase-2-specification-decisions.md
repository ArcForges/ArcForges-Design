# Phase 2 Specification Decisions

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Decisions
> Governing authority: **[D-001](phase-1-foundation-decisions.md#rule-d-001)** (conflict-resolution rule), **[D-016](phase-1-foundation-decisions.md#rule-d-016)** (deferred-decision ownership), **[D-019](phase-1-foundation-decisions.md#rule-d-019)** (sequence status)
> Companions: [`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md), [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)

Phase 1 decisions remain binding except where subsequent explicit user direction amends them under D-001. **[P2-006](#rule-p2-006) records the user-directed requirements revision of 2026-09-06.**

The bar for entry is deliberately high. A conclusion already established by a current formal specification or an effective accepted decision is implemented in the appropriate layer with a citation — it does not become a duplicate decision record. The [deprecated input archive](../deprecated-inputs/README.md) supplies no new requirements or authority; its citations and original quotations are historical provenance only. [P2-001](#rule-p2-001) through [P2-009](#rule-p2-009) are recorded below. [P2-002](#rule-p2-002) is withdrawn; [P2-003](#rule-p2-003) is adopted under the Web redesign. [P2-009](#rule-p2-009) now amends repository ownership, proto, Cloud/AI and Mobile technology. Earlier runtime/transport outcomes are historical where that decision explicitly supersedes them; the accepted product and commercial scope remains binding.

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
| RC-02 | **A decision recorded here is cited inline wherever it is implemented**, exactly as Phase 1 decisions are. |
| RC-03 | **A deferred decision carries an owner, a trigger and the constraint every permitted option must satisfy** — never a bare "decide later". |
| RC-04 | **Adding to this register requires the same discipline as Phase 1**: a real decision, a stated consequence, and a named enforcement mechanism. |

---

<a id="rule-p2-001"></a>

## P2-001 — Install and update infrastructure baseline · `ADOPTED`

**Decision.** **Velopack** is the cross-platform install and update framework baseline for the four desktop products on Windows, macOS and Linux, as specified in the [current packaging architecture](../architecture/14-build-packaging-and-release.md#5-packaging). The baseline has three qualifications:

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

## P2-002 — Sequence derivation under [D-019](phase-1-foundation-decisions.md#rule-d-019) · `WITHDRAWN — SUPERSEDED BY P2-004`

> **This entry was wrong and is retained as the record of the error, not as authority.** Its normative content is withdrawn. The governing entry is [P2-004](#rule-p2-004).

**What it decided.** That the numbered work-package sequence would be derived **before** the per-product Reference Coverage Matrices and the item-level code inventory existed, with those audits scheduled inside the sequence and later packages rewritten if a finding invalidated them (the withdrawn derive-before-evidence rules).

**Why it was wrong.** **[D-019](phase-1-foundation-decisions.md#rule-d-019)** states that the implementation plan *must be derived after* requirements, architecture, licence matrices and current-code reconciliation are complete. **[D-012](phase-1-foundation-decisions.md#rule-d-012)** states that every product must receive a Reference Coverage Matrix *before implementation planning for that product is finalized*. Both are `USER_CONFIRMED` and binding.

[P2-002](#rule-p2-002) substituted a different process — derive first, audit during implementation, rewrite after findings — and presented that substitution as satisfying **[D-019](phase-1-foundation-decisions.md#rule-d-019)**. It did not. A Phase 2 decision may not alter a Phase 1 decision's ordering requirement, and [RC-01](#rule-rc-01) of this register already says so. The entry contradicted the rule under which it was recorded.

**What the substitution cost.** It was not a formality. Producing the prerequisite evidence afterwards surfaced findings that would have changed the plan:

| Finding | Where | What the sequence had assumed |
|---|---|---|
| Four of six accessible references are GPL-family, proprietary or AGPL; **no reuse is possible from any of them** | [`../assurance/reference-coverage/README.md`](../assurance/reference-coverage/README.md) `§Aggregate licence position` | That per-product licence audits might clear material for reuse, making `Copy`/`Port` dispositions plausible downstream |
| Neither ArcNotes reference implements slides | [`arcnotes-affine-siyuan.md`](../assurance/reference-coverage/arcnotes-affine-siyuan.md) `F-AN-2` | That [WP-29](../planning/work-packages/29-arcnotes-slides.md#rule-wp-29) would have reference oracles like its sibling packages |
| Serial-Studio's licence creates an **authorship boundary**, not only a reuse prohibition | [`arcscope-serial-studio.md`](../assurance/reference-coverage/arcscope-serial-studio.md) `F-AS-1` | That the whole reference was readable evidence |
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

**Current decision.** Under [P2-008](#rule-p2-008), browser authentication uses a same-origin C# session adapter inside the existing Cloud host. The edge routes the Account and Chat origins to that host; no new Node server or separate BFF deployment is needed. Each origin receives its own opaque Secure/HttpOnly host-only cookie; session authority, expiry, step-up and revocation stay in the PostgreSQL Identity store. Browser JavaScript receives no access/refresh credential.

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

- `DD-01`: **The sequence is derived, not provisional.** Every package's scope rests on evidence that existed before it was written.
- `DD-02`: **The baseline matrices and the inventory are versioned planning inputs.** Implementation packages consume them. No implementation package re-creates a baseline audit.
- `DD-03`: **Implementation packages retain drift checks only** — source drift against the recorded commit, changed scope, and newly introduced material. Baseline creation and later maintenance are different obligations and are not conflated.
- `DD-04`: **Where evidence changed a package, the change is recorded** with its evidence, the affected statement, the correction, downstream consumers and the verification needed — in [`../planning/evidence-driven-revisions.md`](../planning/evidence-driven-revisions.md).
- `DD-05`: **No unresolved determination remains.** The one that existed — [OC-01](../assurance/open-gates-register.md#rule-oc-01), the ArcSlate reference baseline — was closed by user decision on 2026-09-05 and is recorded as [P2-005](#rule-p2-005).
- `DD-06`: **The four derive-before-evidence rules are withdrawn with P2-002.** They described the substituted process.

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

- `RB-01`: **[D-012](phase-1-foundation-decisions.md#rule-d-012)'s reference map is amended.** The verbatim decision block is preserved per this register's supersession convention; the current effective ArcSlate line is *"ArcVideo and ArcVideoFoundation → ArcSlate references"* ([`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md) §[D-012](phase-1-foundation-decisions.md#rule-d-012) amendment; applied-disposition row 31).
- `RB-02`: **The Olive-direct audit scope is removed.** No obligation exists to obtain Olive's independent tests, fixtures, source or licence file. The missing-repository blocker is withdrawn.
- `RB-03`: **ArcSlate's reference coverage, planning and verification evidence rest on the actual ArcVideo and ArcVideoFoundation repositories**, at commits `caf5651` and `139eeca`.
- <a id="rule-rb-04"></a>`RB-04`: **Olive-origin provenance is preserved, not erased.** ArcVideo is a documented fork of Olive. Its **GPL-3.0 obligations, upstream copyright and attribution run to the Olive authors**, and every notice, licence header and provenance record that inherited material requires is retained (**[D-013](phase-1-foundation-decisions.md#rule-d-013)**). Removing Olive as an independent reference does not authorise removing its provenance, and no row in any matrix does so.
- `RB-05`: **Preserved raw inputs are unchanged.** `I2 §II` and `I4 §Stage 20` still discuss Olive as historical evidence; this decision is recorded outside them and does not rewrite them.
- `RB-06`: **[OC-01](../assurance/open-gates-register.md#rule-oc-01) is closed.** No unresolved determination remains in the Phase 2 register.

**What does not change.** ArcSlate remains an **original implementation**. Both references are **GPL-3.0-only**, so **[D-013](phase-1-foundation-decisions.md#rule-d-013)** still prohibits copying, translating or porting from either; every matrix row remains `Reference Only` or an accepted exclusion. Removing Olive narrows the *audit* scope, not the *reuse* prohibition.

**Authority.** Product Owner (this decision), with the Licensing and Provenance Owner for [RB-04](#rule-rb-04).

**Consumed by.** [`phase-1-foundation-decisions.md`](phase-1-foundation-decisions.md) §[D-012](phase-1-foundation-decisions.md#rule-d-012) amendment; [`../assurance/reference-coverage/arcslate-arcvideo.md`](../assurance/reference-coverage/arcslate-arcvideo.md); [`../assurance/reference-coverage-and-provenance.md`](../assurance/reference-coverage-and-provenance.md) §1.1, §2.2, §7; [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md) §6; [`../requirements/products/arcslate.md`](../requirements/products/arcslate.md) §1; [`../requirements/00-product-scope-and-portfolio.md`](../requirements/00-product-scope-and-portfolio.md) §9; [WP-36](../planning/work-packages/36-arcslate-project-and-timeline.md#rule-wp-36).

**Reversal cost.** Low. Should an Olive checkout later become available and be wanted, it is added to the reference map and the ArcSlate matrix is extended; nothing built on this decision would need to be undone.

---

<a id="rule-p2-006"></a>

## P2-006 — Cloud subscription product and requirements scope revision · ADOPTED

**Authority.** The user's explicit requirements discussion and instruction of **2026-09-06** to apply the changes directly in this worktree, design the remaining metering rules, and review the resulting requirements. This overrides conflicting preserved-input positions and affected portions of [D-006](phase-1-foundation-decisions.md#rule-d-006) and [D-020](phase-1-foundation-decisions.md#rule-d-020) under **[D-001](phase-1-foundation-decisions.md#rule-d-001)**. Preserved inputs remain unchanged.

**User-directed scope.** All AI inference, the single Harness, durable agent orchestration and AI automation are Cloud responsibilities. Official AI requires an active paid service term and uses subscription capacity plus explicitly authorised extra credits. No local AI, end-user BYOK (local or Cloud), agent teams, sub-agents or external-agent delegation. Ordinary bounded tool concurrency and non-agent background jobs remain. Workspaces are single-owner, multi-device boundaries; no organisations, membership, invitations, collaborative editing or collaboration-only schema hooks. Cloud has one ASP.NET Core JIT deployment host with bounded internal background services.

ArcNotes delivers the notebook core, cloud sync, block references/backlinks, properties, queries and views informed by AFFiNE and SiYuan. Full Edgeless, shapes/connectors/frames, slides/presentations, spaced repetition and DOCX import are excluded from the current complete scope, with no mandatory future hooks. Custom local encrypted stores, encrypted portable exports and E2EE are also excluded. ArcChat retains the lean preview scope; no code/Diff/Office workbench is added. ArcScope gains a real deterministic Cloud simulator. ArcSlate gains canonical .otio import/export.

**Design dispositions under the user's delegated requirement-design authority.** These make that direction implementable; they are not quotations of additional user confirmations:

- Cloud owns acknowledged versions of synchronised user data and all agent state. Native clients keep working caches and durable pending edits; cached note editing/search can survive outages, without promising a permanent account-free notebook product. Hardware acquisition and media editing/rendering retain product-local execution and resource ownership.
- Notes' required property depth is common scalar types plus saved list/table views with filtering and sorting. Formula, relation/rollup engines and further database layouts are excluded from current delivery. Basic Markdown/text import and a Cloud data export remain; a full-fidelity local package ecosystem is not required.
- A paid monthly/annual subscription or active prepaid Cloud Pass is the service term; the Pass remains the [D-023](phase-1-foundation-decisions.md#rule-d-023) non-recurring purchase route, not a credit-only AI bypass. Renewal grace protects data access but does not fund new AI calls after the paid term. Purchased credits are retained on expiry and usable again with an active service term.
- Actual provider usage, normalised into non-overlapping billing categories, is the metering basis. Supplier cost, customer usage units, subscription capacity, purchased credits and payment revenue remain separate. Customer tariff snapshots, fixed precision, reservation, idempotent settlement and immutable adjustments remain binding under D-020. Replenishing subscription capacity supplies the base service; extra credits require opt-in. Numeric prices and limits remain versioned deployment data.
- Complete pricing, entitlement and rate-control code runs against validated external configuration. Production values are mounted into Docker at deployment; no private repository, proprietary policy plug-in, separate policy service or authoring UI is required. Public sample configuration exercises the same implementation. Database snapshots and ledgers are real persisted facts, not alternate mutable price authorities.
- Independent self-hosting runs the same Cloud code with an operator-funded, deployment-configured remote model provider and realm policy. This is infrastructure credential provisioning, not end-user BYOK. It confers no official-service entitlement and does not run models in the desktop.
- Existing licensing boundaries remain. Deployment-specific operating values are private; covered implementation code is not hidden as configuration. Public schemas and runnable samples remain available.

**Consumed by.** The revised [requirements set](../requirements/README.md), especially [scope](../requirements/00-product-scope-and-portfolio.md), [commerce](../requirements/04-commerce-entitlement-and-credits.md), [AI execution](../requirements/05-ai-and-agent-execution.md), [configuration](../requirements/11-policy-and-configuration.md) and [product requirements](../requirements/products/README.md).

**Downstream reconciliation status.** This is a requirements revision within **Stage 2**, not a claim that Stage 2 or implementation is complete. Architecture, reference/invariant coverage accounting, work packages, traceability and assurance evidence were produced against earlier scope and require reconciliation before implementation. Their previous completion claims do not demonstrate coverage of P2-006. Detailed schemas, classes, deployment artifacts and implementation steps remain downstream work.

**Acceptance.** Current requirements neither grant an excluded mode nor leave required simulator, OTIO or metering behaviour as a placeholder. Requirements agree on authority, scope, lifecycle, failure behaviour and evidence. Existing identifiers remain traceable; excluded obligations are explicitly retired rather than silently reused.

---

<a id="rule-p2-007"></a>

## P2-007 — Stage 2 design closure corrections · ADOPTED

**Authority.** The user's explicit instruction in this session to repair all fourteen review groups against baseline `c5b95a7`, including the necessary detailed design and cross-document reconciliation. These are authorised design dispositions, not claims of additional user confirmations. The work remains Stage 2; it changes no product or reference source and preserves `docs/inputs/`.

**Effective choices.** Cloud Notes receives a canonical PostgreSQL model; local pending edits retain durable lineage. Publication guarantees per-aggregate revision order and safe cursor advancement, not a global business-commit order inferred from UUIDs. Shared transactions are enumerated for the actual operation families. Admission reserves operator exposure as well as customer funds. Capacity transitions first advance accrual under the previous hold state; a lowered ceiling preserves an already-issued excess balance but cannot increase it. Service terms and plan assignments retain immutable history. Provider dispatch and per-call settlement are separate from final Turn completion. Stream truncation is a presentation state. Migration completion requires version-guarded materialisation and a fenced cutover. C# helper processes isolate hostile parsers and extension executables using OS-enforced capabilities; they contain no product domain or agent loop. OTIO conversion has an explicit external floating-point boundary around the integer tick domain.

**Scope.** [P2-006](#rule-p2-006)'s product scope continues to govern. Native Scope/Slate working stores remain authoritative locally; Cloud acknowledges their synchronised metadata replicas. The helper-process design is the present, bounded application of [D-016](phase-1-foundation-decisions.md#rule-d-016)'s isolation exception, not a C++ worker or second Agent Host. Its operation allowlist, ownership and platform enforcement are specified in the architecture.

**Closure evidence.** The [Stage 2 closure review](../assurance/phase-2-design-closure-review.md) records the fourteen dispositions, design checks and remaining implementation obligations. Existing historical statements are not completion evidence for the revised baseline. A future runtime gate cannot substitute for resolving a contradiction in current specifications.

---

<a id="rule-p2-008"></a>

## P2-008 — React/TypeScript Web and C# generated API clients · ADOPTED

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

The following earlier-baseline tensions were recorded before P2-006. Their evidence remains historical; any affected architecture/coverage/plan must now be reconciled to the amended requirements:

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

**Authority/date.** Explicit user architecture direction and authorization to apply it, 2026-09-11. This is the coordinated amendment prepared in Plan/architecture-change-plan; the formal definitions linked here are the current implementation authority.

**Decisions.** Ten peer implementation/contract repositories under [solution ownership](../architecture/01-solution-and-project-layout.md); reuse existing implementation history for DesktopPlatform, with capability-specific managed/RID NuGet packages. Handwritten proto in Contracts governs business RPC and generated C#/TS clients. Desktop and the single C# Cloud business host publish Native AOT. Mobile is Apache React Native/TypeScript/Hermes Android companion; iOS stays build-deferred. React Web keeps static profiles and isolated origins.

The sole AI loop is a Cloudflare Workflow in ArcForges-AI, using selected Workers AI models directly. A Durable Object coordinates bounded live presentation. C# retains all 20 business owners and canonical PostgreSQL transactions; R2 holds primary bytes behind consumption-time authorization. No production Node/Deno/Bun AI sidecar, local AI, extra Harness or generic gateway. Independent immutable disaster copy remains mandatory.

**Precise authorities.** [Wire registry](../architecture/contracts/04-protobuf-wire-registry.md), [CF/state/object contract](../architecture/contracts/05-cloudflare-integration.md), [runtime/dependency matrix](../architecture/21-platform-and-dependency-matrix.md), [implementation sequence](../planning/implementation-sequence.md).

**Specific supersession.** Amend [D-007](phase-1-foundation-decisions.md#rule-d-007)/[P2-008](#rule-p2-008) C# wire-source rule to proto; [D-008](phase-1-foundation-decisions.md#rule-d-008)/[V-03](../assurance/phase-1-official-verification.md#rule-v-03)/[V-04](../assurance/phase-1-official-verification.md#rule-v-04) Cloud JIT and Mono-AOT mobile choices to the selected Cloud Native AOT and RN runtime; [D-009](phase-1-foundation-decisions.md#rule-d-009) contract authoring/transport to proto; [D-011](phase-1-foundation-decisions.md#rule-d-011) monorepo target to the ten-repository ownership graph. [P2-006](#rule-p2-006)'s single in-host C# Harness placement becomes sole CF Workflow with C# business authority. [P2-008](#rule-p2-008)'s prohibition on RN is replaced for Mobile. The preserved quotations/dated verification in those records describe their historical decision and are not current implementation instructions.

[D-004](phase-1-foundation-decisions.md#rule-d-004)/[D-013](phase-1-foundation-decisions.md#rule-d-013)/[D-021](phase-1-foundation-decisions.md#rule-d-021) license and reference boundaries, [D-010](phase-1-foundation-decisions.md#rule-d-010) direct professional-product access and in-process ArcChat Hub, [D-014](phase-1-foundation-decisions.md#rule-d-014)/015 origins, [D-016](phase-1-foundation-decisions.md#rule-d-016)/[P2-007](#rule-p2-007) isolation, [P2-006](#rule-p2-006) accepted commercial/product scope and all three repaired semantic profiles remain binding. No organizations, BYOK, extra agent, professional mobile editor, Notes canvas/slides/formulas/E2EE or mandatory prepayment is added.

**Implementation consequence.** WP02/03 establish exact producer artifacts; WP06 proves selected AOT/gRPC/RN/CF/R2 paths early. WP52 implements the sole CF loop after real business admission/bridge/retrieval, and WP50 joins real deployment/restore evidence. Documentation review does not satisfy those runtime gates.
