# Implementation Sequence

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning
> Governing authority: **D-017** (planning location and format), **D-019** (sequence status), `I2 §III`, `I2 §V`, `I2 §VI`
> Companions: [`work-packages/README.md`](work-packages/README.md), [`../assurance/release-gates.md`](../assurance/release-gates.md), [`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)

This document states the dependency model that produces the work-package sequence: why the order is what it is, what may be parallelised, what may be mocked, and what may never be.

**The sequence is a dependency order, not a schedule.** It contains no dates, no durations and no resourcing assumptions.

---

## 1. The controlling ordering principles

| # | Principle |
|---|---|
| SQ-01 | **Freeze before build.** Naming, terminology, licence position and product scope are frozen first, because editors, data formats, capabilities and sync all rework if they change later (`I2 §III.0`). |
| SQ-02 | **Prove the risky mechanism before building on it.** AOT publish, local IPC, serialization and persistence recovery are proven on a skeleton before product work depends on them (`I2 §III.1`, `§III.2`). |
| SQ-03 | **External vendors may be mocked; your own architectural boundaries may not** (`I2 §V`). This single rule determines most of the ordering. |
| SQ-04 | **The first cross-process slice is real, not simulated** (`I2 §III.3`). Two genuinely AOT-published processes must talk over a real transport before either product grows. |
| SQ-05 | **ArcNotes proves sync**, because it is more complex than a toy and simpler than raw captures or large media (`I2 §III.6`). |
| SQ-06 | **The professional products come after the platform they depend on**, and ArcSlate comes last because it carries the highest complexity and performance risk (`I2 §III.10`). |
| SQ-07 | **Mobile follows the first real cloud contracts, not the last product** (`I2 §III.8`). Deferring mobile design until every desktop product is finished would rework the contracts it depends on. |
| SQ-08 | **Commerce goes live last among the cloud capabilities**, because entitlement, refunds, webhook idempotency and a real payout path must all exist first (`I2 §III.12`). |
| SQ-09 | **The static public site can start very early** (`I2 §III.12`) because it depends on nothing but content. |
| SQ-10 | **Each professional product may connect directly to Cloud.** Nothing in this sequence may create a dependency in which a professional product must relay through ArcChat (**D-010**, `I2 §III.11`). |

### 1.1 The D-019 ordering, followed

**D-019** requires the implementation plan to be derived **after** requirements, architecture, licence matrices and current-code reconciliation are complete. **D-012** requires each product's Reference Coverage Matrix before that product's implementation planning is finalized. That ordering is followed.

| Prerequisite | Artifact | State |
|---|---|---|
| Requirements | [`../requirements/`](../requirements/README.md) | Complete |
| Architecture | [`../architecture/`](../architecture/README.md) | Complete |
| Licence matrices, per product | [`../assurance/reference-coverage/`](../assurance/reference-coverage/README.md) — five matrices, 145 item-level rows | **Complete**, with one unresolved determination (`OC-01`, Olive) |
| Current-code reconciliation | [`../assurance/implementation-state-reconciliation.md`](../assurance/implementation-state-reconciliation.md) — 166 projects, item-level | **Complete** |

> **A correction is recorded here rather than hidden.** An earlier Phase 2 decision (`P2-002`) substituted a different process — derive the plan first, perform the prerequisite audits during implementation, rewrite afterwards — and presented that substitution as satisfying **D-019**. It did not. That entry is **withdrawn** and retained as the record of the error; `P2-004` records the re-derivation from the completed evidence. The changes the evidence caused are in [`evidence-driven-revisions.md`](evidence-driven-revisions.md).

| # | Position |
|---|---|
| DD-01 | **The sequence is derived, not provisional.** Every package's scope rests on evidence that existed before the package was written. |
| DD-02 | **The matrices and the inventory are versioned planning inputs.** Implementation packages consume them; **no implementation package re-creates a baseline audit.** |
| DD-03 | **Implementation packages retain drift checks only** — source drift against the recorded commit, changed scope, and newly introduced material. Each has a named producing sub-step: `WP-15.07`, `WP-18.08`, `WP-33.07`, `WP-36.07` for references, and `WP-01.00` for the code inventory. |
| DD-04 | **Baseline creation and later maintenance are different obligations** and are never conflated in a gate. |
| DD-05 | **One unresolved determination remains** — `OC-01`. It blocks only a claim of complete Olive coverage, which is made nowhere. |

---

## 2. Phase structure

The sequence is one continuous numbered series. Phases are a reading aid, not a gate structure — the gates are per work package.

| Phase | Work packages | What becomes true at the end |
|---|---|---|
| **A — Freeze and foundation** | 00 – 07 | Terminology, licence position and layout are settled; the build enforces the architecture; AOT is proven; contracts, serialization and persistence primitives exist |
| **B — Shared platform** | 08 – 13 | Local IPC, the capability and resource model, the desktop shell, security, observability, and the four high-risk probes |
| **C — First real slice** | 14 – 17 | Two real processes talk; ArcChat has a domain, an execution engine and an independent core |
| **D — ArcNotes core** | 18 – 20 | ArcNotes is a complete local product, and the first genuine cross-product workflow runs |
| **E — First real cloud** | 21 – 26 | Identity, public API, realtime, sync and remote action exist against real infrastructure |
| **F — ArcNotes completion** | 27 – 29 | Edgeless, database views and slides land on the V1 compatibility baseline |
| **G — Mobile** | 30 – 32 | The Android remote closed loop exists under the Apache boundary; iOS is planned, build-deferred |
| **H — ArcScope** | 33 – 35 | Acquisition, analysis and integration |
| **I — ArcSlate** | 36 – 39 | Timeline, runtime, render and integration |
| **J — Platform completion** | 40 – 46 | Knowledge, extensions, commerce, AI economics, policy, operations and resilience |
| **K — Web and release** | 47 – 50 | Public site, account portal, web companion and the full-platform production release |

---

## 3. What may be mocked, and what may not

Directly from `I2 §V`, which is binding on every work package.

| May be mocked initially | Must be real early |
|---|---|
| AI providers, streaming responses, token billing | **The agent running inside a real AOT release binary** |
| Email delivery and one-time codes; push | **Identity, refresh and session contention** |
| Payment provider webhook payloads (as fixtures) | **The webhook inbox, idempotency and reconciliation** |
| Object storage adapters | **Upload interruption, hashing, resumption and quota** |
| Cloud policy distribution | **Permission re-validated at the final resource owner** |
| Cloud search | **Local full-text indexing and citation anchors** |
| ArcScope device simulators | **Real serial, TCP and UDP transports, disconnects and throughput** |
| ArcSlate test media | **Real decoding, audio/video synchronisation and long exports** |
| Application-port fakes | **The local store journal, crash recovery and migration** |
| Cloud API stubs | **Real HTTP client, serialization and realtime protocol compatibility tests** |
| Capability test providers | **Real named pipes and domain sockets, generated proxies and the binary formatter** |

| # | Rule |
|---|---|
| MK-01 | **A mock is temporary and named.** Every mock introduced by a work package is listed in that package, with the later package that replaces it. |
| MK-02 | **A mock never crosses a completion gate that the real thing is supposed to prove.** |
| MK-03 | **A test that only ever runs against a mock does not satisfy a gate for the real integration.** |

---

## 4. Parallelisation

The sequence is serial by number, but the dependency graph permits genuine parallelism. A work package may begin when **all** its upstream dependencies are complete, regardless of number.

| Track | May proceed in parallel once its dependency is met |
|---|---|
| Static public site (47) | After 00; it depends only on frozen naming and content |
| Design system and shell (10) | After 02; parallel with contract and persistence work |
| Observability foundation (12) | After 02; parallel with security foundation |
| High-risk probes (13) | After 06; the four probes are parallel with one another |
| ArcScope (33 – 35) and ArcSlate (36 – 39) | Independent of each other once 26 is complete |
| Extension platform (41) | After 09 and 11; parallel with product work |
| Commerce (42) | After 22 and 23; parallel with product work |

| # | Rule |
|---|---|
| PA-01 | **Parallelism never bypasses a completion gate.** A downstream package still requires its upstream gates to have passed. |
| PA-02 | **A parallel track that changes a shared contract yields to the contract owner**, and the change goes through the contract-change process (`§4` of the contract architecture). |
| PA-03 | **A package with an unsatisfied upstream gate is blocked, not "started with a caveat".** |

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

| # | Rule |
|---|---|
| WF-01 | **A work package is not complete until its gate is satisfied with recorded evidence.** |
| WF-02 | **A work package may not silently absorb another's scope.** Moving scope between packages is a recorded change. |
| WF-03 | **A work package that discovers a genuine architecture conflict stops and raises it** (**D-001**), rather than resolving it locally. |
| WF-04 | **Sub-steps within a package are ordered but may be executed in parallel where they are genuinely independent.** |
| WF-05 | **Every deferred gate that a package is scheduled to satisfy is named in that package's gate section** ([`../assurance/open-gates-register.md`](../assurance/open-gates-register.md)). |

---

## 7. What this sequence deliberately does not do

| # | Position |
|---|---|
| ND-01 | **It does not create separate multi-tier plans per product** (`I2 §VI`). One continuous sequence interleaves shared foundation, cloud, mobile, web and cross-product capability at their real dependency positions. |
| ND-02 | **It does not schedule.** No dates, no durations, no capacity assumptions. |
| ND-03 | **It does not reopen Phase 1 decisions.** Where a package touches a decided area, it implements the decision. |
| ND-04 | **It does not defer risk to the end.** The four high-risk probes are early, precisely so that ArcSlate does not meet decoding, GPU, synchronisation and AOT problems for the first time at work package 36. |
| ND-05 | **It does not treat probe code as production code.** Probe conclusions feed the formal steps; probe code is cleaned up or discarded (`I2 §III.2`). |

---

## 8. Traceability

| Source | Consumed as |
|---|---|
| `I2 §III.0`–`§III.13` | The high-level dependency order decomposed into the numbered sequence |
| `I2 §V` | The mock policy, binding on every package |
| `I2 §VI` | The required per-step fields and the prohibition on separate per-product plans |
| **D-017** | Planning location and format |
| **D-019** | The status of the original stage sequence as discovery, not delivery order |
| **D-010** | The prohibition on making ArcChat a mandatory relay for professional products |
