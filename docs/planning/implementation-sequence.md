# Implementation Sequence

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning
> Governing authority: **[D-017](../decisions/phase-1-foundation-decisions.md#rule-d-017)** (planning location and format), **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** (sequence status)
> Companions: [`work-packages/README.md`](work-packages/README.md), [`../assurance/release-gates.md`](../assurance/release-gates.md), [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)

This document states the dependency model that produces the work-package sequence: why the order is what it is, what may be parallelised, what may be mocked, and what may never be.

**The sequence is a dependency order, not a schedule.** It contains no dates, no durations and no resourcing assumptions.

---

## 1. The controlling ordering principles

| # | Principle |
|---|---|
| SQ-01 | **Freeze before build.** Naming, terminology, licence position and product scope are frozen first, because editors, data formats, capabilities and sync all rework if they change later. |
| SQ-02 | **Prove the risky mechanism before building on it.** AOT publish, local IPC, serialization and persistence recovery are proven on a skeleton before product work depends on them. |
| <a id="rule-sq-03"></a>SQ-03 | **External vendors may be mocked; your own architectural boundaries may not**. This single rule determines most of the ordering. |
| <a id="rule-sq-04"></a>SQ-04 | **The first cross-process slice is real, not simulated**. Two genuinely AOT-published processes must talk over a real transport before either product grows. |
| <a id="rule-sq-05"></a>SQ-05 | **ArcNotes proves sync**, because it is more complex than a toy and simpler than raw captures or large media. |
| SQ-06 | **The professional products come after the platform they depend on**, and ArcSlate comes last because it carries the highest complexity and performance risk. |
| SQ-07 | **Mobile architecture follows the first real Cloud contracts; runtime acceptance follows the actual Harness**. Deferring mobile design until every desktop product is finished would rework the contracts it depends on. |
| <a id="rule-sq-08"></a>SQ-08 | **Commercial primitives precede paid Cloud consumers; paid go-live remains gated at final release**, after entitlement, refunds, webhook idempotency and a real payout path are proven. |
| SQ-09 | **The static public site can start very early** after the shared Node toolchain is available; it does not need completed commercial or agent services. |
| SQ-10 | **Each professional product may connect directly to Cloud.** Nothing in this sequence may create a dependency in which a professional product must relay through ArcChat (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |

### 1.1 The [D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019) ordering, followed

**[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** requires the implementation plan to be derived **after** requirements, architecture, licence matrices and current-code reconciliation are complete. **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** requires each product's Reference Coverage Matrix before that product's implementation planning is finalized. That ordering is followed.

| Prerequisite | Artifact | State |
|---|---|---|
| Requirements | [`../requirements/`](../requirements/README.md) | Complete |
| Architecture | [`../architecture/`](../architecture/README.md) | Complete |
| Licence matrices, per product | [`../assurance/reference-coverage/`](../assurance/reference-coverage/README.md) — five matrices, 145 item-level rows | **Complete** |
| Current-code reconciliation | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) — 166 projects, item-level | **Complete** |

> **A correction is recorded here rather than hidden.** An earlier Phase 2 decision ([P2-002](../decisions/phase-2-specification-decisions.md#rule-p2-002)) substituted a different process — derive the plan first, perform the prerequisite audits during implementation, rewrite afterwards — and presented that substitution as satisfying **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)**. It did not. That entry is **withdrawn** and retained as the record of the error; [P2-004](../decisions/phase-2-specification-decisions.md#rule-p2-004) records the re-derivation from the completed evidence. The changes the evidence caused are in [`evidence-driven-revisions.md`](evidence-driven-revisions.md).

| # | Position |
|---|---|
| DD-01 | **The sequence is derived, not provisional.** Every package's scope rests on evidence that existed before the package was written. |
| DD-02 | **The matrices and the inventory are versioned planning inputs.** Implementation packages consume them; **no implementation package re-creates a baseline audit.** |
| DD-03 | **Implementation packages retain drift checks only** — source drift against the recorded commit, changed scope, and newly introduced material. Each has a named producing sub-step: [WP-15.07](work-packages/15-arcchat-conversation-core.md#rule-wp-15.07), [WP-18.08](work-packages/18-arcnotes-document-core.md#rule-wp-18.08), [WP-33.07](work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.07), [WP-36.07](work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.07) for references, and [WP-01.00](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.00) for the code inventory. |
| DD-04 | **Baseline creation and later maintenance are different obligations** and are never conflated in a gate. |
| DD-05 | **No unresolved determination remains.** [OC-01](../assurance/open-gates-register.md#rule-oc-01) — the ArcSlate reference baseline — was closed by user decision on 2026-09-05 ([P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005)), which amended **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**'s reference map to ArcVideo and ArcVideoFoundation. |

---

## 2. Phase structure

The sequence is one continuous numbered series. Phases are a reading aid, not a gate structure — the gates are per work package.

| Phase | Work packages | What becomes true at the end |
|---|---|---|
| **A — Freeze and foundation** | 00 – 07 | Terminology, licence position and layout are settled; the build enforces the architecture; AOT is proven; contracts, serialization and persistence primitives exist |
| **B — Shared platform** | 08 – 13 | Local IPC, the capability and resource model, the desktop shell, security, observability, and the four high-risk probes |
| **C — First real slice** | 14 – 17 | Two real processes talk; ArcChat has a domain, an execution engine and an independent core |
| **D — ArcNotes core** | 18 – 20 | ArcNotes native editor/recovery and non-agent cross-product commands work; acknowledged Cloud authority and real exports arrive in E, AI workflow in J |
| **E — First real cloud** | 21 – 26 | Identity, public API, realtime, sync and remote action exist against real infrastructure |
| **F — ArcNotes completion** | 28 | Bounded typed properties and saved list/table views land. **`27` and `29` are retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** — canvas and slides are excluded from delivery, not deferred |
| **G — Mobile shared foundation** | 30 | Early mobile contracts, Apache boundary and platform architecture; the real Android closed loop is delivered after the Harness in J |
| **H — ArcScope desktop** | 33 – 35 | Real acquisition, replay, analysis and metadata integration; the real Cloud simulator follows paid-term/quota/policy prerequisites in J |
| **I — ArcSlate** | 36 – 39 | Timeline, runtime, render and integration |
| **J — Platform and client integration** | 42, 44, 43, 40, 41, 45, 46, 51, 52, 31, 32 | Commercial/policy kernel, real provider metering and Cloud retrieval, extensions, operations, simulator, Harness/automation, then real Android Task/stream and signed-device acceptance |
| **K — Web and release** | 47 – 50 | Public site, account portal, web companion and the full-platform production release |

---

> **Numbering above `50`.** `00`–`50` were allocated when the sequence was first derived, and a retired identifier is never recycled (`27`, `29`). A package added afterwards therefore takes the next free number while executing at its real dependency position: **`51` and `52` run in Phase J; Android execution acceptance `31`/`32` follows `52`, and all gate `50`.** Where the numeral and the dependency graph disagree, **the dependency graph governs**.

---

### 2.1 Web redesign producers and consumers

[P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) preserves package identity while changing its Web implementation: [WP-01](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01), [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) produce the npm/esproj/toolchain boundary; [WP-03](work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-04](work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04) produce handwritten proto descriptors/generated C#/TS packages and exact values; [WP-06.05](work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.05) proves a production React call against the real foundation host. [WP-22.08](work-packages/22-identity-workspace-and-device.md#rule-wp-22.08) supplies the production cookie-session adapter before [WP-23](work-packages/23-public-api-and-generated-clients.md#rule-wp-23)'s generated clients and [WP-24](work-packages/24-realtime-and-reliable-events.md#rule-wp-24)'s TS realtime adapter. [WP-47](work-packages/47-static-public-site.md#rule-wp-47) now also depends on [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) and supplies the shared consumer design system before [WP-48](work-packages/48-account-portal.md#rule-wp-48), [WP-49](work-packages/49-arcchat-web-companion.md#rule-wp-49). Commercial/Chat release acceptance still consumes the real Cloud/Harness, then [WP-50](work-packages/50-full-platform-production-release.md#rule-wp-50). One new edge, [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) → [WP-47](work-packages/47-static-public-site.md#rule-wp-47), prevents the static site from assuming a Node toolchain that no package has built.

---

## 3. What may be mocked, and what may not

The policy in this section is the complete, binding definition for every work package. The table defines the permitted fixture boundaries; the rules and named replacement owners below govern their removal.

| May be mocked initially | Must be real early |
|---|---|
| AI providers, streaming responses, token billing | **The device tool path inside a real AOT release binary** — pull, local re-authorisation, generated decode, typed invocation, idempotent result. **The agent loop itself is the CF Workflow** ([LS-02](../architecture/17-agent-harness.md#rule-ls-02), **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**), so no AOT gate applies to it |
| Email delivery and one-time codes; push | **Identity, refresh and session contention** |
| Payment provider webhook payloads (as fixtures) | **The webhook inbox, idempotency and reconciliation** |
| Object storage adapters | **Upload interruption, hashing, resumption and quota** |
| Cloud policy distribution | **Permission re-validated at the final resource owner** |
| Cloud search | **Local full-text indexing and citation anchors** |
| ArcScope device simulators | **Real serial, TCP and UDP transports, disconnects and throughput** |
| ArcSlate test media | **Real decoding, audio/video synchronisation and long exports** |
| Application-port fakes | **The local store journal, crash recovery and migration** |
| Cloud API stubs and generated-contract MSW UI fixtures | **Real C#/TS generated clients, exact JSON values, browser sessions, serialization and realtime compatibility tests** |
| Capability test providers | **Real named pipes and domain sockets, generated proxies and the binary formatter** |

| # | Rule |
|---|---|
| <a id="rule-mk-01"></a>MK-01 | **A mock is temporary and named.** Every mock introduced by a work package is listed in that package, with the later package that replaces it. |
| MK-02 | **A mock never crosses a completion gate that the real thing is supposed to prove.** |
| MK-03 | **A test that only ever runs against a mock does not satisfy a gate for the real integration.** |
| MK-04 | **A package may not gate on a capability a later package builds.** Where an early package needs a Cloud behaviour that does not exist yet, it uses a named fixture and **states in its own gate that the real verification belongs to the later package**. [WP-17.01](work-packages/17-arcchat-independent-core.md#rule-wp-17.01) and [WP-52](work-packages/52-cloud-harness.md#rule-wp-52) are the worked case. |

### 3.1 Named temporary scaffolding

Every fixture that stands in for a later capability is listed here with the package that **deletes** it. [MK-01](#rule-mk-01) requires the naming; this table is where it lives.

| Scaffolding | Introduced by | Stands in for | Deleted by |
|---|---|---|---|
| **Fixture turn endpoint** — accepts a turn, returns scripted task and step transitions, scripted stream chunks and scripted `ToolRequest`s; runs no model, planner, admission or metering | [WP-17.01](work-packages/17-arcchat-independent-core.md#rule-wp-17.01) | The Cloud Harness | **[WP-52.05](work-packages/52-cloud-harness.md#rule-wp-52.05)**, which asserts structurally that it no longer exists |
| Stubbed managed provider path | [WP-17.05](work-packages/17-arcchat-independent-core.md#rule-wp-17.05) | Real provider routing and metering | [WP-43.00](work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.00), [WP-43.07](work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.07) |
| Notes/Chat export fixture endpoints | [WP-15.06](work-packages/15-arcchat-conversation-core.md#rule-wp-15.06), [WP-19.05](work-packages/19-arcnotes-search-and-portability.md#rule-wp-19.05) | Real Cloud snapshot/export jobs | [WP-25.08](work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08) |
| Automation fixture state transitions | [WP-17.04](work-packages/17-arcchat-independent-core.md#rule-wp-17.04) | Durable Cloud trigger scheduler and occurrence execution | [WP-52.06](work-packages/52-cloud-harness.md#rule-wp-52.06) |
| Payment-provider fixture adapter (recorded event fixtures remain regression inputs) | [WP-42.03](work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.03) | Live adapter/event ingestion | Remove runtime fixture registration at [WP-42.10](work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10); retain recorded test cases |
| Local device test-source substitution | [WP-33.00](work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.00) | Real hardware acceptance | [WP-33](work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33) hardware-lab gate ([PG-08](../assurance/open-gates-register.md#rule-pg-08)); replay and test sources remain explicitly labelled |
| No-op media adapter, if used during a unit test | [WP-37.01](work-packages/37-arcslate-playback-and-processing.md#rule-wp-37.01) | Real codec integration | [WP-37](work-packages/37-arcslate-playback-and-processing.md#rule-wp-37)/[WP-38](work-packages/38-arcslate-render-and-colour.md#rule-wp-38) use real decode/export; golden media inputs are retained, never deleted as scaffolding |

| # | Rule |
|---|---|
| TS-01 | **Scaffolding is deleted, never adapted.** A fixture that graduates into production code stops being visible as a fixture, which is how a mock ends up serving real traffic. |
| TS-02 | **The deleting package asserts the deletion structurally**, so the removal is verified rather than assumed. |

---

**Web fixtures.** [WP-06](work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) may use a labelled foundation endpoint and Web development may use MSW fixtures. MSW handlers remain test-only; they are excluded from release bundles. [WP-23](work-packages/23-public-api-and-generated-clients.md#rule-wp-23) replaces fixture evidence with real API/session conformance and [WP-48](work-packages/48-account-portal.md#rule-wp-48), [WP-49](work-packages/49-arcchat-web-companion.md#rule-wp-49) require the real commercial/Harness services. Retaining a regression fixture does not authorize a production mock registration.

---

### Frozen semantics before the first consumer

The reviewed repairs establish these definitions before implementation starts. Packages implement and test them; they do not select their product meaning during coding.

| Definition | Earliest implementation and downstream proof |
|---|---|
| [Content origin behavior](../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carriers](../requirements/13-data-formats-and-portability.md#content-origin-carriers) | Contract foundation freezes typed records/vectors; persistence commits origin with content; Chat/Notes/native report/media formats preserve it. Real Cloud export replaces runtime fixtures in [WP-25.08](work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08); real provider/Harness marking runs in [WP-43.04](work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.04) and [WP-52.03](work-packages/52-cloud-harness.md#rule-wp-52.03). Early fixtures cannot close these real-producer gates |
| [Notes scalar query](../requirements/products/arcnotes.md#notes-scalar-query-profile) | Foundation contracts and core values precede initial list filters, API/cursor and sync validation. [WP-28](work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) completes both query evaluators; [WP-40](work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40) directly depends on it for the Notes filter. The existing serial order already puts 28 before 40 |
| [Scope measurement](../requirements/products/arcscope.md#measurement-profile) | Contract/storage projection precedes [WP-34.02](work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.02) formulas/oracles and reports. Recorded acquisition/replay input is sufficient; the later Cloud simulator reuses this profile and does not gate earlier analysis |
| Service term and capacity | [WP-42.11](work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) executes before [WP-42.10](work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10) go-live despite numerical suffix order. AI-provider and configuration evidence complete their own shared gates later |

A shared gate closes only after every scheduled producer contributes its required execution evidence. An early package records its scoped contribution in §7/§8, never a substitute global pass. The [gate index](work-packages/README.md#deferred-gate-scheduling) and each named completion gate carry the same obligation. Design-only checks do not close provider, hardware, market, isolation or commercial runtime gates.

---

## 4. Serial execution and dependency freedom

Implementation is one main, serial context. Execute the topological order in the work-package index; numerical identity never overrides a dependency. Independent products may have focused solution views and isolated build/test entry points without splitting authority or bypassing shared gates.

| # | Rule |
|---|---|
| PA-01 | A package starts only after **all** direct upstream completion gates pass; the header, dependency section and index name the same edges. |
| PA-02 | A change to a shared contract follows its ownership/compatibility process before dependent work proceeds. |
| PA-03 | No delegated/background implementation agents or parallel package execution is required or authorised by this plan. Independent technical test cases can run concurrently inside a verification command where appropriate. |

---

## 5. Roles

Roles are functions. One person may hold several; a role always has exactly one accountable holder at a time.

| Role | Accountable for |
|---|---|
| **Product Owner** | Scope, product decisions, commercial policy versions, first-release approval |
| **Architecture Owner** | Architecture rules, contract changes, the glossary, technical gates |
| **Release Engineering Owner** | Build, packaging, signing, release gates, mobile artifacts |
| **Quality Owner** | The quality contract, test families, waivers, the quality report |
| **Security and Privacy Owner** | The security model, privacy obligations, advisories, transparency gates |
| **Operations Owner** | Cloud operation, runbooks, incidents, go-live readiness |
| **Commercial Operations Owner** | Provider onboarding, payouts, screening, regional gates |
| **Licensing and Provenance Owner** | Licence boundaries, provenance records, dependency closure |

---

## 6. Work-package format

Every work package states, without exception:

1. **Scope and purpose** — in scope and explicitly out of scope
2. **Required inputs and dependencies** — documents, upstream packages, external evidence
3. **Binding rules and decisions** — the decisions, invariants and architecture rules that constrain it
4. **Projects, directories, files and major types affected**
5. **Required implementation work** — as numbered sub-steps, each with what must be fully done, its tests, and its own completion gate
6. **Impacts** — database, protocol, UI, security, platform, migration and compatibility, where applicable
7. **Tests and verification evidence**
8. **Completion gate**
9. **Dependencies on earlier and later work packages**

Required design inputs are current formal definitions, accepted decisions, declared reference-source evidence and completed upstream outputs. An input table must link to the actual definition or evidence it consumes. A historical source label or an instruction to reconstruct a rule from an archived document is not a valid input. Where a rule is defined by this package itself, its behavior and acceptance belong in sections 3, 5, 7 and 8; they are not an external prerequisite.

| # | Rule |
|---|---|
| WF-01 | **A work package is not complete until its gate is satisfied with recorded evidence.** |
| WF-02 | **A work package may not silently absorb another's scope.** Moving scope between packages is a recorded change. |
| <a id="rule-wf-03"></a>WF-03 | **A work package that discovers a genuine architecture conflict stops and raises it** (**[D-001](../decisions/phase-1-foundation-decisions.md#rule-d-001)**), rather than resolving it locally. |
| WF-04 | **Sub-steps execute serially in dependency order.** Independent verification cases may run concurrently without dividing implementation ownership. |
| WF-05 | **Every deferred gate that a package is scheduled to satisfy is named in that package's gate section** ([`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)). |

---

## 7. What this sequence deliberately does not do

| # | Position |
|---|---|
| ND-01 | **It does not create separate multi-tier plans per product**. One continuous sequence interleaves shared foundation, cloud, mobile, web and cross-product capability at their real dependency positions. |
| ND-02 | **It does not schedule.** No dates, no durations, no capacity assumptions. |
| ND-03 | **It does not reopen Phase 1 decisions.** Where a package touches a decided area, it implements the decision. |
| ND-04 | **It does not defer risk to the end.** The four high-risk probes are early, precisely so that ArcSlate does not meet decoding, GPU, synchronisation and AOT problems for the first time at work package 36. |
| <a id="rule-nd-05"></a>ND-05 | **It does not treat probe code as production code.** Probe conclusions feed the formal steps; probe code is cleaned up or discarded. |

---

## 8. Traceability

| Current document | Relationship |
|---|---|
| [ArcForges Product Scope and Portfolio](../requirements/00-product-scope-and-portfolio.md) | Owns the accepted product scope and boundaries |
| [Testing and Verification Strategy](../assurance/testing-and-verification-strategy.md) | Assigns the verification evidence required by the sequence |
| [Release Gates](../assurance/release-gates.md) | Defines the release and implementation evidence gates |
| **[D-017](../decisions/phase-1-foundation-decisions.md#rule-d-017)** | Planning location and format |
| **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** | The status of the original stage sequence as discovery, not delivery order |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | The prohibition on making ArcChat a mandatory relay for professional products |

## 9. P2-009 complete artifact dependency graph

All 51 active packages retain their domain scope; WP27/29 stay retired. The dependency table below is the current complete directed graph. Header and dependency sections of each package are generated from this same frozen set. Source ownership and immutable inputs are in each package; no cross-repository source dependency is implied.

| WP | Required upstream |
|---|---|
| 00 | None |
| 01 | 00 |
| 02 | 01 |
| 03 | 02 |
| 04 | 03 |
| 05 | 02, 03 |
| 06 | 03, 04, 05 |
| 07 | 04, 06 |
| 08 | 06, 07 |
| 09 | 03, 08 |
| 10 | 06, 09 |
| 11 | 04, 08, 09 |
| 12 | 04, 06 |
| 13 | 06, 07, 08 |
| 14 | 08, 09, 10, 11, 13 |
| 15 | 14 |
| 16 | 09, 11, 14 |
| 17 | 06, 15, 16 |
| 18 | 07, 10, 14 |
| 19 | 18 |
| 20 | 17, 19 |
| 21 | 03, 05, 12 |
| 22 | 11, 21 |
| 23 | 03, 22 |
| 24 | 23 |
| 25 | 19, 24 |
| 26 | 17, 24, 25 |
| 28 | 19, 25 |
| 30 | 03, 06, 23, 24 |
| 33 | 07, 10, 13, 26 |
| 34 | 33 |
| 35 | 25, 34 |
| 36 | 07, 10, 13, 26 |
| 37 | 36 |
| 38 | 37 |
| 39 | 25, 38 |
| 42 | 22, 23 |
| 44 | 23, 42 |
| 43 | 25, 42, 44 |
| 40 | 19, 25, 28, 43, 44 |
| 41 | 09, 11, 17 |
| 45 | 12, 21, 44 |
| 46 | 25, 45 |
| 51 | 21, 23, 25, 33, 34, 35, 42, 44 |
| 52 | 15, 17, 20, 21, 23, 26, 39, 40, 41, 42, 43, 44 |
| 31 | 26, 30, 52 |
| 32 | 31 |
| 47 | 00, 02 |
| 48 | 25, 42, 44, 46, 47 |
| 49 | 26, 48, 52 |
| 50 | 20, 28, 32, 35, 39, 40, 41, 43, 46, 49, 51, 52 |

Serial execution: 00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 33, 34, 35, 36, 37, 38, 39, 42, 44, 43, 40, 41, 45, 46, 51, 52, 31, 32, 47, 48, 49, 50. WP42.11 precedes 42.10. WP02 supplies package pipelines, WP03 schema packages, WP06 actual candidate/AOT/RN/CF/R2 foundations before full features. WP17/20 use explicitly named AI fixtures; WP52 replaces them. WP46 establishes backup mechanics; WP50 tests combined recovery after 46 and52, avoiding a cycle. Independent package/product versions are joined by a tested manifest, not a suite-wide version.

## Final review execution bindings

[Staged artifact integration](README.md#staged-artifact-integration) is mandatory for the graph above. WP02 produces the pipeline/BuildPolicy, WP03 Contracts, WP04 values and WP06 the real native/runtime foundation; later packages never require a future Cloud manifest. The shell directly consumes WP09 contribution contracts. Account UI consumes WP25 exports and WP46 data health. Simulator acceptance consumes WP34 measurements and WP35 portability. WP52 additionally consumes WP39 for real Slate transcription/adoption; this does not move the media engine into Cloud. No full integration gate is satisfied by renaming a mock.
