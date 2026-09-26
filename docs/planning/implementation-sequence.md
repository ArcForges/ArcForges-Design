# Implementation Dependency Model

Execution follows [P2-018](../decisions/phase-2-specification-decisions.md#rule-p2-018) and [P2-017](../decisions/phase-2-specification-decisions.md#rule-p2-017) with the [CI/local policy](../assurance/ci-and-local-validation-policy.md). Work is scheduled as delivery tasks with typed prerequisites in the [delivery graph](delivery/README.md); any number of ready tasks may run concurrently while CPU-heavy local work stays serialized per workstation. Runtime scenarios are scoped local opt-in, not hosted CI or repeated post-merge gates; macOS CI is prohibited. Historical completion evidence is not a rerun requirement.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning
> Governing authority: **[D-017](../decisions/phase-1-foundation-decisions.md#rule-d-017)** (planning location and format), **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** (derivation after evidence), [P2-018](../decisions/phase-2-specification-decisions.md#rule-p2-018) (task-level scheduling)
> Companions: [`delivery/README.md`](delivery/README.md), [`work-packages/README.md`](work-packages/README.md), [`../assurance/release-gates.md`](../assurance/release-gates.md), [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)

This document states the principles that shape the dependency model: why prerequisites are what they are, what may be substituted, what must be real, and which semantics are frozen before their first consumer. The scheduling itself — tasks, typed edges, readiness and claims — is defined by the [delivery model](delivery/README.md) and its [graph](delivery/delivery-graph.json).

**The model is a dependency structure, not a schedule.** It contains no dates, no durations and no resourcing assumptions; the relative task sizes exist only for the [schedule analysis](delivery/schedule-analysis.md).

---

## 1. The controlling ordering principles

| # | Principle |
|---|---|
| <a id="rule-sq-01"></a>SQ-01 | **Freeze before build.** Naming, terminology, licence position and product scope are frozen first, because editors, data formats, capabilities and sync all rework if they change later. This freeze is complete and accepted. |
| <a id="rule-sq-02"></a>SQ-02 | **Prove the risky mechanism before building on it.** AOT publish, local IPC, serialization, persistence recovery, native decode and acquisition throughput are proven by tasks with few prerequisites; each proof gates only the work that depends on its conclusion ([DLV-21](delivery/README.md#rule-dlv-21)). |
| <a id="rule-sq-03"></a>SQ-03 | **External vendors may be mocked; your own architectural boundaries may be substituted only to start work.** A contract-bound substitute generated from the authoritative schema may unblock a consumer's start, but every gate that proves a boundary requires the real boundary, and the must-be-real-early list in §3 is unchanged ([DLV-18](delivery/README.md#rule-dlv-18), [DLV-19](delivery/README.md#rule-dlv-19)). |
| <a id="rule-sq-04"></a>SQ-04 | **Prove each real boundary before the consumers that depend on it complete.** Parent/helper AOT gRPC over OS streams, independent product hosts with typed in-process calls, and each Cloud transport are proven by named proof or integration tasks; consumers may start against the published contract. Product-to-product IPC is not a prerequisite. |
| <a id="rule-sq-05"></a>SQ-05 | **ArcNotes proves sync**, because it is more complex than a toy and simpler than raw captures or large media. Other products' sync integration tasks follow the real Notes convergence evidence of the sync engine. |
| <a id="rule-sq-06"></a>SQ-06 | **Products depend on the platform capabilities they use, not on the whole platform.** Each product task depends on the specific persistence, shell, security, native-family or assistant tasks it consumes. ArcSlate's high performance and media risk is retired early by the native decode and synchronisation probe and the media family tasks, not by scheduling ArcSlate last. |
| <a id="rule-sq-07"></a>SQ-07 | **Android foundation work starts from the published contracts; Android runtime acceptance follows the real Cloud and Harness integration tasks.** Deferring mobile design until every desktop product is finished would rework the contracts it depends on. |
| <a id="rule-sq-08"></a>SQ-08 | **Commercial primitives precede the completion of paid Cloud consumers; paid go-live remains gated at release**, after entitlement, refunds, webhook idempotency and a real payout path are proven. |
| <a id="rule-sq-09"></a>SQ-09 | **The static public site can start very early** after the shared Node toolchain is available; it does not need completed commercial or agent services. |
| <a id="rule-sq-10"></a>SQ-10 | **Each professional product may connect directly to Cloud.** Nothing in this model may create a dependency in which a professional product must relay through ArcChat (**[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |

### 1.1 The [D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019) ordering, followed

**[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)** requires the implementation plan to be derived **after** requirements, architecture, licence matrices and current-code reconciliation are complete, and **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)** requires each product's Reference Coverage Matrix before that product's implementation planning is finalized. That derivation requirement remains in force; [P2-018](../decisions/phase-2-specification-decisions.md#rule-p2-018) replaced only its serial single-context execution rule.

| Prerequisite | Artifact | State |
|---|---|---|
| Requirements | [`../requirements/`](../requirements/README.md) | Complete |
| Architecture | [`../architecture/`](../architecture/README.md) | Complete |
| Licence matrices, per product | [`../assurance/reference-coverage/`](../assurance/reference-coverage/README.md) — five matrices, 145 item-level rows | **Complete** |
| Current-code reconciliation | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) — historical 166-project inventory at ede43db; current repository snapshot in family completion review | **Historical evidence; revalidated per current source** |

> **A correction is recorded here rather than hidden.** An earlier Phase 2 decision ([P2-002](../decisions/phase-2-specification-decisions.md#rule-p2-002)) substituted a different process — derive the plan first, perform the prerequisite audits during implementation, rewrite afterwards — and presented that substitution as satisfying **[D-019](../decisions/phase-1-foundation-decisions.md#rule-d-019)**. It did not. That entry is **withdrawn** and retained as the record of the error; [P2-004](../decisions/phase-2-specification-decisions.md#rule-p2-004) records the re-derivation from the completed evidence. The changes the evidence caused are in [`evidence-driven-revisions.md`](evidence-driven-revisions.md).

| # | Position |
|---|---|
| <a id="rule-dd-01"></a>DD-01 | **The sequence is derived, not provisional.** Every package's scope rests on evidence that existed before the package was written. |
| <a id="rule-dd-02"></a>DD-02 | **The matrices and the inventory are versioned planning inputs.** Implementation packages consume them; **no implementation package re-creates a baseline audit.** |
| <a id="rule-dd-03"></a>DD-03 | **Implementation packages retain drift checks only** — source drift against the recorded commit, changed scope, and newly introduced material. Each has a named producing sub-step: [WP-15.07](work-packages/15-arcchat-conversation-core.md#rule-wp-15.07), [WP-18.08](work-packages/18-arcnotes-document-core.md#rule-wp-18.08), [WP-33.07](work-packages/33-arcscope-acquisition-and-session.md#rule-wp-33.07), [WP-36.07](work-packages/36-arcslate-project-and-timeline.md#rule-wp-36.07) for references, and [WP-01.00](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01.00) for the code inventory. |
| <a id="rule-dd-04"></a>DD-04 | **Baseline creation and later maintenance are different obligations** and are never conflated in a gate. |
| <a id="rule-dd-05"></a>DD-05 | **No unresolved determination remains.** [OC-01](../assurance/open-gates-register.md#rule-oc-01) — the ArcSlate reference baseline — was closed by user decision on 2026-09-05 ([P2-005](../decisions/phase-2-specification-decisions.md#rule-p2-005)), which amended **[D-012](../decisions/phase-1-foundation-decisions.md#rule-d-012)**'s reference map to ArcVideo and ArcVideoFoundation. |

---

## 2. Phase structure

Phases group obligation packages for reading; they are not a schedule and carry no ordering. Each package belongs to exactly one phase. Scheduling is defined only by task prerequisites in the [delivery graph](delivery/README.md).

| Phase | Work packages | What becomes true at the end |
|---|---|---|
| **A — Freeze and foundation** | 00 – 07, 47 | Terminology, licence position and layout are settled; the build enforces the architecture; AOT is proven; contracts, serialization and persistence primitives exist |
| **B — Shared platform** | 08 – 13 | Local IPC, capability/resource model, desktop shell, security, observability and complete functional native producers with technical probes |
| **C — Independent applications and assistant** | 14 – 17 | Real independent application composition, assistant SQLite/core, execution mechanisms and the complete reusable Avalonia assistant exist; Cloud fixture replacement has named later producers |
| **D — ArcNotes core** | 18 – 19 | ArcNotes native editor/recovery and own-product search/export work; acknowledged Cloud authority and real exports arrive in E, AI workflow in J. WP20 is future-only |
| **E — First real cloud** | 21 – 26 | Identity, public API, realtime, sync and remote action exist against real infrastructure |
| **F — ArcNotes completion** | 28 | Bounded typed properties and saved list/table views land. **`27` and `29` are retired by [P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)** — canvas and slides are excluded from delivery, not deferred |
| **G — Kotlin Android foundation** | 30 | Early mobile contracts, Apache boundary and platform architecture; the real Android closed loop is delivered after the Harness in J |
| **H — ArcScope desktop** | 33 – 35 | Real acquisition, replay, analysis and metadata integration; the real Cloud simulator follows paid-term/quota/policy prerequisites in J |
| **I — ArcSlate** | 36 – 39 | Timeline, runtime, render and integration |
| **J — Platform and client integration** | 41, 42, 44, 43, 40, 45, 53, 46, 51, 52, 31, 32 | Commercial/policy kernel, providers/retrieval, extensions, operations, desktop updater, simulator, Harness and actual Android acceptance |
| **K — Web and release** | 48 – 50 | Account portal, web companion and the full-platform production release |

---

> **Numbering.** `00`–`50` were allocated when the obligations were first derived and `51`–`53` were added later; a retired identifier is never recycled (`27`, `29`). Numbers are identities only. Whether any task of a package can run depends solely on that task's prerequisites.

---

### 2.1 Web redesign producers and consumers

[P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) preserves package identity while changing its Web implementation: [WP-01](work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01), [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) produce the npm/esproj/toolchain boundary; [WP-03](work-packages/03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-04](work-packages/04-identity-error-and-versioning-primitives.md#rule-wp-04) produce handwritten proto descriptors/generated C#/TS packages and exact values; [WP-06.05](work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06.05) proves a production React call against the real foundation host. [WP-22.08](work-packages/22-identity-workspace-and-device.md#rule-wp-22.08) supplies the production cookie-session adapter before [WP-23](work-packages/23-public-api-and-generated-clients.md#rule-wp-23)'s generated clients and [WP-24](work-packages/24-realtime-and-reliable-events.md#rule-wp-24)'s TS realtime adapter. [WP-47](work-packages/47-static-public-site.md#rule-wp-47) now also depends on [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02) and supplies the shared consumer design system before [WP-48](work-packages/48-account-portal.md#rule-wp-48), [WP-49](work-packages/49-arcchat-web-companion.md#rule-wp-49). Commercial/Chat release acceptance still consumes the real Cloud/Harness, then [WP-50](work-packages/50-full-platform-production-release.md#rule-wp-50). The static site depends only on the accepted Node toolchain of [WP-02](work-packages/02-build-governance-and-analyzer-policy.md#rule-wp-02), so its tasks are among the first to become ready.

---

## 3. What may be mocked, and what may not

The policy in this section is the complete, binding definition for every task. The table defines the permitted substitute boundaries; the rules below and the [substitute registry](delivery/substitutes.md) govern their removal.

| May be mocked initially | Must be real early |
|---|---|
| AI providers, streaming responses, token billing | **The device tool path inside a real AOT release binary** — pull, local re-authorisation, generated decode, typed invocation, idempotent result. **The agent loop itself is the CF Workflow** ([LS-02](../architecture/17-agent-harness.md#rule-ls-02), **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**), so no AOT gate applies to it |
| Push until its named producer; test-only recorded email responses | **Identity, refresh/session contention and real email delivery/recovery at WP22** |
| Payment provider webhook payloads (as fixtures) | **The webhook inbox, idempotency and reconciliation** |
| Object storage adapters | **Upload interruption, hashing, resumption and quota** |
| Cloud policy distribution | **Permission re-validated at the final resource owner** |
| Cloud search | **Local full-text indexing and citation anchors** |
| ArcScope device simulators | **Real serial, TCP and UDP transports, disconnects and throughput** |
| ArcSlate test media | **Real decoding, audio/video synchronisation and long exports** |
| Application-port fakes | **The local store journal, crash recovery and migration** |
| Cloud API stubs and generated-contract MSW UI fixtures | **Real C#/TS generated clients, exact JSON values, browser sessions, serialization and realtime compatibility tests** |
| Capability test providers | **Real typed in-process product ports, isolated application stores and parent/helper Named Pipe/UDS gRPC** |

| # | Rule |
|---|---|
| <a id="rule-mk-01"></a>MK-01 | **A substitute is temporary and named.** Every substitute is registered in the [substitute registry](delivery/substitutes.md) with the contract it implements, what it proves, its real producer and the task that removes its runtime use. |
| <a id="rule-mk-02"></a>MK-02 | **A substitute never crosses a completion gate that the real thing is supposed to prove.** |
| <a id="rule-mk-03"></a>MK-03 | **A test that only ever runs against a substitute does not satisfy a gate for the real integration.** |
| <a id="rule-mk-04"></a>MK-04 | **A task's own gate never requires a capability produced by a task that depends on it.** Where early work needs a Cloud behaviour that does not exist yet, it uses a registered substitute, and the real verification belongs to a named integration or acceptance task. The fixture turn endpoint, removed only after every assistant, Android and Web consumer runs against the real Harness, is the worked case. |

### 3.1 Named temporary scaffolding

Every piece of named scaffolding from the retired scaffolding table — the fixture turn endpoint, the stubbed managed provider path, the Notes and assistant export fixtures, automation fixture state transitions, the payment-provider fixture adapter and recorded events, local device test sources, the no-op media adapter, the test-signed desktop update feed, the hostile test parser, recorded Postmark/SES responses and recorded FCM sender responses — is registered in the [substitute registry](delivery/substitutes.md) with its real producer and removing task. The registry is the only list; it also records substitutes introduced by task decomposition.

| # | Rule |
|---|---|
| <a id="rule-ts-01"></a>TS-01 | **Scaffolding is deleted, never adapted.** A fixture that graduates into production code stops being visible as a fixture, which is how a mock ends up serving real traffic. |
| <a id="rule-ts-02"></a>TS-02 | **The removing task asserts the deletion structurally**, so the removal is verified rather than assumed. |

---

**Web fixtures.** [WP-06](work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) may use a labelled foundation endpoint and Web development may use MSW fixtures. MSW handlers remain test-only; they are excluded from release bundles. [WP-23](work-packages/23-public-api-and-generated-clients.md#rule-wp-23) replaces fixture evidence with real API/session conformance and [WP-48](work-packages/48-account-portal.md#rule-wp-48), [WP-49](work-packages/49-arcchat-web-companion.md#rule-wp-49) require the real commercial/Harness services. Retaining a regression fixture does not authorize a production mock registration.

---

### Frozen semantics before the first consumer

The reviewed repairs establish these definitions before implementation starts. Tasks implement and test them; they do not select their product meaning during coding.

| Definition | Earliest implementation and downstream proof |
|---|---|
| [Content origin behavior](../requirements/07-security-privacy-and-trust.md#content-origin-profile) and [carriers](../requirements/13-data-formats-and-portability.md#content-origin-carriers) | Contract foundation freezes typed records/vectors; persistence commits origin with content; Chat/Notes/native report/media formats preserve it. Real Cloud export replaces runtime fixtures in [WP-25.08](work-packages/25-sync-engine-and-blob-lifecycle.md#rule-wp-25.08); real provider/Harness marking runs in [WP-43.04](work-packages/43-managed-ai-routing-and-metering.md#rule-wp-43.04) and [WP-52.03](work-packages/52-cloud-harness.md#rule-wp-52.03). Early fixtures cannot close these real-producer gates |
| [Notes scalar query](../requirements/products/arcnotes.md#notes-scalar-query-profile) | Foundation contracts and core values precede initial list filters, API/cursor and sync validation. [WP-28](work-packages/28-arcnotes-properties-and-views.md#rule-wp-28) completes both query evaluators; [WP-40](work-packages/40-knowledge-search-and-retrieval.md#rule-wp-40) directly depends on it for the Notes filter. In the delivery graph the Notes filter in search depends on the query-model task |
| [Scope measurement](../requirements/products/arcscope.md#measurement-profile) | Contract/storage projection precedes [WP-34.02](work-packages/34-arcscope-analysis-and-reporting.md#rule-wp-34.02) formulas/oracles and reports. Recorded acquisition/replay input is sufficient; the later Cloud simulator reuses this profile and does not gate earlier analysis |
| Service term and capacity | [WP-42.11](work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.11) executes before [WP-42.10](work-packages/42-commerce-entitlement-and-credits.md#rule-wp-42.10) go-live despite numerical suffix order. AI-provider and configuration evidence complete their own shared gates later |

A shared gate closes only after every contributing task records its required execution evidence. An early task records its scoped contribution, never a substitute global pass. The [gate traceability](delivery/traceability.md#gates) and each named completion gate carry the same obligation. Design-only checks do not close provider, hardware, market, isolation or commercial runtime gates.

---

## 4. Parallel execution and dependency freedom

| # | Rule |
|---|---|
| <a id="rule-pa-01"></a>PA-01 | **A task starts when its own start prerequisites are satisfied** ([DLV-24](delivery/README.md#rule-dlv-24)) and the adoption slice for its repository and lane is complete ([DLV-22](delivery/README.md#rule-dlv-22)). There is no package-level start rule: a package's other tasks, its numeric neighbours and unrelated lanes never gate it. |
| <a id="rule-pa-02"></a>PA-02 | **A change to a shared contract follows its ownership/compatibility process before dependent work proceeds.** The Architecture Owner accepts the change; consumers move to the new closure through reviewed pin updates. |
| <a id="rule-pa-03"></a>PA-03 | **Independent tasks run concurrently** in the same or different repositories under atomic claims ([DLV-26](delivery/README.md#rule-dlv-26)); merges follow each repository's integration owner ([DLV-29](delivery/README.md#rule-dlv-29)); at most one CPU-heavy local build or test runs per workstation ([DLV-31](delivery/README.md#rule-dlv-31)). |

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
| **Repository integration owner** (one per repository) | Merge order and main health, shared-resource protocols, generated baselines, candidate publication of that repository |

---

## 6. Work-package format

Every work package states, without exception:

1. **Scope and purpose** — in scope and explicitly out of scope
2. **Required inputs and dependencies** — documents, upstream packages, external evidence
3. **Binding rules and decisions** — the decisions, invariants and architecture rules that constrain it
4. **Projects, directories, files and major types affected**
5. **Required implementation work** — as numbered sub-steps, each with what must be fully done, its tests, and its own completion gate
6. **Impacts** — database, protocol, UI, security, platform, migration and compatibility, where applicable
7. **Tests and verification evidence**, including the .90 owned-artifact and real-integration receipt
8. **Completion gate**
9. **Delivery tasks** — generated from the delivery graph: the tasks that satisfy the package, their prerequisites outside it and their consumers

Required design inputs are current formal definitions, accepted decisions, declared reference-source evidence and completed upstream outputs. An input table must link to the actual definition or evidence it consumes. A historical source label or an instruction to reconstruct a rule from an archived document is not a valid input. Where a rule is defined by this package itself, its behavior and acceptance belong in sections 3, 5, 7 and 8; they are not an external prerequisite.

| # | Rule |
|---|---|
| <a id="rule-wf-01"></a>WF-01 | **A work package is not complete until its gate is satisfied with recorded evidence.** |
| <a id="rule-wf-02"></a>WF-02 | **A work package may not silently absorb another's scope.** Moving scope between packages or tasks is a recorded planning change. |
| <a id="rule-wf-03"></a>WF-03 | **A task that discovers a genuine architecture conflict stops and raises it** (**[D-001](../decisions/phase-1-foundation-decisions.md#rule-d-001)**), rather than resolving it locally. |
| <a id="rule-wf-04"></a>WF-04 | **Substeps are obligations, not a sequence.** Their tasks run whenever their prerequisites allow; tasks of one package may run concurrently, and independent verification cases may run concurrently without dividing implementation ownership. |
| <a id="rule-wf-05"></a>WF-05 | **Every deferred gate that a package is scheduled to satisfy is named in that package's gate section** ([`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)) and mapped to its contributing tasks in [traceability](delivery/traceability.md#gates). |

---

## 7. What this model deliberately does not do

| # | Position |
|---|---|
| <a id="rule-nd-01"></a>ND-01 | **It does not create separate multi-tier plans per product.** One delivery graph interleaves shared foundation, Cloud, mobile, Web and application-owned capabilities at their real dependency positions. |
| <a id="rule-nd-02"></a>ND-02 | **It does not schedule by calendar.** No dates, no durations, no capacity assumptions; relative sizes serve only the schedule analysis. |
| <a id="rule-nd-03"></a>ND-03 | **It does not reopen Phase 1 decisions.** Where a task touches a decided area, it implements the decision. |
| <a id="rule-nd-04"></a>ND-04 | **It does not defer risk to the end.** The four high-risk probes are tasks with few prerequisites, precisely so that ArcSlate does not meet decoding, GPU, synchronisation and AOT problems for the first time late. |
| <a id="rule-nd-05"></a>ND-05 | **Probe scaffolding does not become production by relabeling.** Probe conclusions feed implementation; scaffolds are cleaned up or discarded. Explicitly assigned functional producer code (WP13.05–13.16) is production code, retained and maintained. |

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
| [Delivery traceability](delivery/traceability.md) | Maps every substep, package obligation and gate to its delivery tasks |

## 9. [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) complete artifact dependency graph

[P2-018](../decisions/phase-2-specification-decisions.md#rule-p2-018) replaced the package-level dependency table and its serial execution list with the task-level [delivery graph](delivery/delivery-graph.json). The graph is the complete artifact dependency structure: every start prerequisite names the published closure or artifact a task needs, every completion prerequisite names the real scenario its acceptance includes, and release prerequisites apply only to release tasks. The retired table (51 active packages, 158 package edges) remains in repository history as a record; it is not an execution rule. All 51 active packages retain their accepted scope; WP20 is future-only and WP27/WP29 remain retired.

Package relationships are now derived views: each package's section 9 lists the tasks that satisfy it, their prerequisites outside the package and the tasks that consume them. The explicit service-term-before-go-live constraint is a task edge: the live-gate staging task starts only after the service-term and replenishing-capacity task is delivered.

## Final review execution bindings

[Staged artifact integration](README.md#staged-artifact-integration) is mandatory for every task. Contracts closures, Foundation values, platform packages and the runtime proofs are produced before the tasks that consume them; no task requires a future Cloud manifest. The shell directly consumes the capability contribution contracts. Account UI consumes the Cloud export producer and the data-health read projection. Simulator acceptance consumes ArcScope measurements and portability. The Slate transcription adoption scenario consumes the Harness and ArcSlate subtitles without moving the media engine into Cloud. No full integration gate is satisfied by renaming a mock. [P2-013](../decisions/phase-2-specification-decisions.md#rule-p2-013) PackageCatalog production precedes the package review console; native login and mail originate in the identity tasks, fixture signing formats in Contracts, and production trust in the updater and release tasks.
