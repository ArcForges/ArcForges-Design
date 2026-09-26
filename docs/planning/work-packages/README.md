# Work Packages

Execution follows [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018) and [P2-017](../../decisions/phase-2-specification-decisions.md#rule-p2-017) with the [CI/local policy](../../assurance/ci-and-local-validation-policy.md). Work packages are obligation sets; their delivery tasks run whenever their own prerequisites allow. Runtime scenarios are scoped local opt-in, not hosted CI or repeated post-merge gates; macOS CI is prohibited. Historical completion evidence is not a rerun requirement.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning
> Governing authority: **[D-017](../../decisions/phase-1-foundation-decisions.md#rule-d-017)** (numbered implementation work packages belong here), [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018) (task-level scheduling)
> Companions: [`../delivery/README.md`](../delivery/README.md), [`../implementation-sequence.md`](../implementation-sequence.md), [`../../assurance/release-gates.md`](../../assurance/release-gates.md), [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md)

**51 active obligation packages are identified in `00`–`53`; `20` is future-only; `27` and `29` are retired.** Each package defines what must be done, tested and accepted. Scheduling is task-level: each package's section 9 lists the delivery tasks that satisfy it, generated from the [delivery graph](../delivery/delivery-graph.json), and [traceability](../delivery/traceability.md) maps every substep to its tasks.

The number is an identity, not a schedule. No package waits for another package; a task waits only for the specific tasks named in its prerequisites.

---

## The packages

Phases group packages for reading only.

### Phase A — Freeze and foundation

| # | Work package |
|---|---|
| 00 | [Specification, Naming and Rights Freeze](00-specification-naming-and-rights-freeze.md) |
| 01 | [Repository Reconciliation and Target Layout](01-repository-reconciliation-and-target-layout.md) |
| 02 | [Build Governance, Packaging Policy and Analyzers](02-build-governance-and-analyzer-policy.md) |
| 03 | [Proto Contract Foundation and License Split](03-contract-foundation-and-licence-split.md) |
| 04 | [Identity, Error, Revision and Versioning Primitives](04-identity-error-and-versioning-primitives.md) |
| 05 | [Architecture and Repository Policy Test Suite](05-architecture-and-repository-policy-tests.md) |
| 06 | [AOT, Android, CF and Real Artifact Publish Proof](06-aot-jit-and-wasm-publish-proof.md) |
| 07 | [Local Persistence Foundation](07-local-persistence-foundation.md) |
| 47 | [Static Public Site](47-static-public-site.md) |

### Phase B — Shared platform

| # | Work package |
|---|---|
| 08 | [Private Helper gRPC and Parent Registration](08-local-ipc-and-registration.md) |
| 09 | [Capability, Contribution and Resource Model](09-capability-contribution-and-resource-model.md) |
| 10 | [Design System and Desktop Shell Foundation](10-design-system-and-desktop-shell.md) |
| 11 | [Security Foundation](11-security-foundation.md) |
| 12 | [Observability Foundation](12-observability-foundation.md) |
| 13 | [Complete Native Producers and Technical Probes](13-high-risk-technical-probes.md) |

### Phase C — First real slice

| # | Work package |
|---|---|
| 14 | [Independent Application Composition and Typed Host Ports](14-hub-and-minimal-provider-slice.md) |
| 15 | [Application Assistant Conversation, History and Project Packages](15-arcchat-conversation-core.md) |
| 16 | [Unified Execution Engine](16-unified-execution-engine.md) |
| 17 | [Complete Embedded Assistant and Cloud Client Surface](17-arcchat-independent-core.md) |

### Phase D — ArcNotes core

| # | Work package |
|---|---|
| 18 | [ArcNotes Document Core](18-arcnotes-document-core.md) |
| 19 | [ArcNotes Search, Import, Export and Portability](19-arcnotes-search-and-portability.md) |
| 20 | [Cross-Product Collaboration — FUTURE](20-first-cross-product-workflow.md) |

### Phase E — First real cloud

| # | Work package |
|---|---|
| 21 | [Cloudflare Container, D1 Authority and Binding Plans](21-cloud-host-and-persistence.md) |
| 22 | [Identity, Workspace, Device and Session](22-identity-workspace-and-device.md) |
| 23 | [Public Proto APIs and Generated Clients](23-public-api-and-generated-clients.md) |
| 24 | [gRPC-Web Streams and Durable Event Recovery](24-realtime-and-reliable-events.md) |
| 25 | [Sync Engine and Blob Lifecycle](25-sync-engine-and-blob-lifecycle.md) |
| 26 | [Application Presence and One-Application Tool Bridge](26-remote-action-and-tool-bridge.md) |

### Phase F — ArcNotes completion

| # | Work package |
|---|---|
| 28 | [ArcNotes Bounded Properties and Saved Views](28-arcnotes-properties-and-views.md) |

### Phase G — Mobile shared foundation

| # | Work package |
|---|---|
| 30 | [Kotlin Android Foundation](30-mobile-shared-architecture.md) |

### Phase H — ArcScope desktop

| # | Work package |
|---|---|
| 33 | [ArcScope Acquisition and Session Core](33-arcscope-acquisition-and-session.md) |
| 34 | [ArcScope Visualisation, Analysis and Reporting](34-arcscope-analysis-and-reporting.md) |
| 35 | [ArcScope Integration and Metadata Sync](35-arcscope-integration-and-sync.md) |

### Phase I — ArcSlate

| # | Work package |
|---|---|
| 36 | [ArcSlate Project, Timeline and Media Model](36-arcslate-project-and-timeline.md) |
| 37 | [ArcSlate Playback and Processing Runtime](37-arcslate-playback-and-processing.md) |
| 38 | [ArcSlate Render, Export and Colour Management](38-arcslate-render-and-colour.md) |
| 39 | [ArcSlate Integration and Portability](39-arcslate-integration-and-portability.md) |

### Phase J — Platform and client integration

| # | Work package |
|---|---|
| 42 | [Commerce, Entitlement and Credits](42-commerce-entitlement-and-credits.md) |
| 44 | [Dynamic Policy and Configuration Control Plane](44-dynamic-policy-and-configuration.md) |
| 43 | [Workers AI Routing and Metering](43-managed-ai-routing-and-metering.md) |
| 40 | [Application-Scoped Knowledge Search and Retrieval](40-knowledge-search-and-retrieval.md) |
| 41 | [Extension Platform and Integrations](41-extension-platform-and-integrations.md) |
| 45 | [Operations, Support and Trust & Safety](45-operations-support-and-trust-safety.md) |
| 53 | [Desktop Distribution, Update Client and Channels](53-desktop-distribution-and-update.md) |
| 46 | [D1, R2 and Independent Disaster Recovery](46-backup-recovery-and-data-health.md) |
| 51 | [ArcScope Deterministic Cloud Simulator](51-arcscope-cloud-simulator.md) |
| 52 | [Sole Cloudflare Workflow Harness](52-cloud-harness.md) |
| 31 | [Complete ArcChat Android Companion](31-arcchat-mobile-android.md) |
| 32 | [Android Signing, Distribution and Store Gates](32-mobile-release-and-store-gates.md) |

### Phase K — Web and release

| # | Work package |
|---|---|
| 48 | [Account Portal](48-account-portal.md) |
| 49 | [ArcChat Web Companion](49-arcchat-web-companion.md) |
| 50 | [Full-Platform Production Release](50-full-platform-production-release.md) |

`27` (canvas) and `29` (slides) are retired; their identifiers are not reused. [WP-20](20-first-cross-product-workflow.md#rule-wp-20) is future-only and has no delivery tasks.

---

## Downstream dependency index

Retired by [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). The package-level downstream index and its forward table described a serial package order; they remain in repository history as a record. Consumers of each package are now listed per task: each package's section 9 names the tasks outside the package that consume its tasks, and every lane catalogue lists what each task unblocks.

## Deferred-gate scheduling

Every gate in [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md) is satisfied by a named package.

| Gate | Satisfied in |
|---|---|
| **[F-013](../../assurance/open-gates-register.md#rule-f-013)** — reference licence determinations | **Closed 2026-09-05 by design-stage evidence** — the five matrices in [`../../assurance/reference-coverage/`](../../assurance/reference-coverage/README.md). Drift maintenance only: `15.07`, `18.08`, `33.07`, `36.07` |
| **[F-023](../../assurance/open-gates-register.md#rule-f-023)** — mobile provenance and dependency closure | 06.07 before first artifact; 30.00 on change; 32.02 final closure |
| **[F-026](../../assurance/open-gates-register.md#rule-f-026)** — typed HTTP client AOT packaging | 03.02, 06.02 |
| **[VG-01](../../assurance/open-gates-register.md#rule-vg-01)** — AI transparency marking | 43 |
| **[VG-02](../../assurance/open-gates-register.md#rule-vg-02)** — MCP SDK pin and vocabulary mapping | 41 |
| **[VG-03](../../assurance/open-gates-register.md#rule-vg-03)** — third-party control AOT proof | 10 |
| **[VG-04](../../assurance/open-gates-register.md#rule-vg-04)** — desktop host AOT proof with the real contract set | 03.04, 06.01 |
| **[VG-05](../../assurance/open-gates-register.md#rule-vg-05)** — typed client verification | Merged into [F-026](../../assurance/open-gates-register.md#rule-f-026); no separate closure |
| **[VG-06](../../assurance/open-gates-register.md#rule-vg-06)** — Cloud Native AOT closure (triggered) | 06.04, 21.00, 50.04 |
| **[VG-07](../../assurance/open-gates-register.md#rule-vg-07)** — Android runtime posture confirmed from the artifact | 06.07, 30.02, 32.01 |
| **[VG-08](../../assurance/open-gates-register.md#rule-vg-08)** — framework upgrade re-verification (recurring) | 02, and re-run on each upgrade |
| **[VG-09](../../assurance/open-gates-register.md#rule-vg-09)** — historical iOS gate (retired by [P2-010](../../decisions/phase-2-specification-decisions.md#rule-p2-010)) | outside current Android-only scope |
| **[VG-10](../../assurance/open-gates-register.md#rule-vg-10)** — supplier onboarding and screening | 42 |
| **[VG-11](../../assurance/open-gates-register.md#rule-vg-11)** — payout eligibility and currency | 42 |
| **[VG-12](../../assurance/open-gates-register.md#rule-vg-12)** — regional enablement gates (conditional) | 42 |
| **[VG-13](../../assurance/open-gates-register.md#rule-vg-13)** — store category fit and consumption-only | 32 |
| **[PG-01](../../assurance/open-gates-register.md#rule-pg-01)** — per-product Reference Coverage Matrix | **Closed 2026-09-05 by design-stage evidence.** Registered as versioned inputs in `00.04`; drift maintenance in `15.07`, `18.08`, `33.07`, `36.07` |
| **[PG-02](../../assurance/open-gates-register.md#rule-pg-02)** — item-level reconciliation inventory | **Closed 2026-09-05 by design-stage evidence** — [`../../assurance/implementation-state-reconciliation.md`](../../assurance/implementation-state-reconciliation.md). Drift validation in `01.00`; disposition execution in `01.01`–`01.05` |
| **[PG-03](../../assurance/open-gates-register.md#rule-pg-03)** — native dependency licence review | 13.04, 33, 35.04, 37.00, 39.05; each admitted native dependency has its licence/substitute-analysis evidence |
| **[PG-04](../../assurance/open-gates-register.md#rule-pg-04)** — runbook rehearsal evidence | 45 |
| **[PG-05](../../assurance/open-gates-register.md#rule-pg-05)** — telemetry redaction proof | 12 |
| **[PG-06](../../assurance/open-gates-register.md#rule-pg-06)** — design-stage invariant traceability | **Closed 2026-09-05 by design-stage evidence** — [`../../assurance/invariant-coverage.md`](../../assurance/invariant-coverage.md) `§7`, **429 of 429** mapped after [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) added [I-491](../../requirements/01-normative-glossary-and-invariants.md#rule-i-491)–[I-498](../../requirements/01-normative-glossary-and-invariants.md#rule-i-498) |
| **[PG-11](../../assurance/open-gates-register.md#rule-pg-11)** — implementation-stage invariant enforcement | **Open.** Distributed across the owning packages named in the coverage mapping; accounting reported by `05.05`, which closes neither gate |
| **[PG-07](../../assurance/open-gates-register.md#rule-pg-07)** — format fixture completeness | 19.04 (Notes import), 35.04, 39.05; real Cloud Notes/Chat export separately closes at 25.08 |
| **[PG-08](../../assurance/open-gates-register.md#rule-pg-08)** — hardware lab inventory | 13 establishes inventory; 33, 34, 37, 38 bind each hardware result to it |
| **[PG-09](../../assurance/open-gates-register.md#rule-pg-09)** — extension protocol conformance | 41 |
| **[PG-10](../../assurance/open-gates-register.md#rule-pg-10)** — provider test-environment coverage | 42, 43 |
| **[PG-12](../../assurance/open-gates-register.md#rule-pg-12)** — PDF dependency and containment | 11.09, 13.13, 18.04 |
| **[PG-13](../../assurance/open-gates-register.md#rule-pg-13)** — real-provider metering | 43.07, 42.11 |
| **[PG-14b](../../assurance/open-gates-register.md#rule-pg-14b)** — real Cloud simulator | 51 |
| **[PG-15](../../assurance/open-gates-register.md#rule-pg-15)** — bidirectional OTIO | 39.05 |
| **[PG-16](../../assurance/open-gates-register.md#rule-pg-16)** — configuration activation | 44.01, 42.11 |
| **[PG-17](../../assurance/open-gates-register.md#rule-pg-17)** — feed publication and bootstrap | 21.05, 25.02, 25.07 |
| **[PG-18](../../assurance/open-gates-register.md#rule-pg-18)** — uncertain-effect resolution | 52.02, 52.04 |
| **[PG-19](../../assurance/open-gates-register.md#rule-pg-19)** — versioned migration and cutover | 21.03, 50.04 |
| **[PG-20](../../assurance/open-gates-register.md#rule-pg-20)** — time model and official OTIO boundary | 36.01, 37.04, 39.05 |
| **[PG-21](../../assurance/open-gates-register.md#rule-pg-21)** — current design citation integrity | Current corpus closed by [repair verification](../../assurance/design-repair-verification.md); continuing drift check in 00.01 |
| **[PG-22](../../assurance/open-gates-register.md#rule-pg-22)** — OS-enforced content/extension isolation | 11.09, 13.13, 18.04, 37.01, 41.00 |
| **[PG-23](../../assurance/open-gates-register.md#rule-pg-23)** — commercial Web | 06.05, 22.08, 23.05, 24.06, 47, 48, 49, 50.06; combine all applicable producer evidence |
| **[PG-24](../../assurance/open-gates-register.md#rule-pg-24)** — real Android push | 45.09 live sender;32 physical receipt and fallback |

The contributing delivery tasks for each gate are listed in [gate traceability](../delivery/traceability.md#gates), which is the authoritative gate-to-task mapping. It also covers gates this table predates — [PG-25](../../assurance/open-gates-register.md#rule-pg-25), [PG-26](../../assurance/open-gates-register.md#rule-pg-26), [L-16](../../assurance/release-gates.md#rule-l-16) and [L-30](../../assurance/release-gates.md#rule-l-30) — the experience acceptance rows UX-A to UX-H, and the second [VG-04](../../assurance/open-gates-register.md#rule-vg-04) contribution from the Contracts policy tests ([WP-05.03](05-architecture-and-repository-policy-tests.md#rule-wp-05.03)). A gate closes only when every contributing task has recorded its evidence.

---

## Conventions

- Each package is one file, `NN-slug.md`, and contains numbered substeps `WP-NN.MM`, each with what must be fully done, its testing requirement and its own completion gate.
- Every package states the nine mandatory fields listed in `§6` of [`../implementation-sequence.md`](../implementation-sequence.md); field 9 is the generated delivery-task block.
- Section 2 of each package lists the documents and upstream outputs its obligations consume. They are information inputs, not scheduling prerequisites: a task's prerequisites are only its typed edges in the delivery graph.
- A package's completion gate is machine-evaluated wherever possible and always names its evidence artifact; the package is complete when every task mapped to it is complete.
- A task that discovers a genuine architecture conflict stops and raises it (**[D-001](../../decisions/phase-1-foundation-decisions.md#rule-d-001)**); it does not resolve it locally.
- **A package never re-creates a completed baseline audit.** The reference matrices and the code inventory are versioned planning inputs; tasks consume them and check for drift ([`../evidence-driven-revisions.md`](../evidence-driven-revisions.md)).
- Implementation ownership is per task: any number of workers may execute different ready tasks concurrently under atomic claims, with merges coordinated by each repository's integration owner ([DLV-26](../delivery/README.md#rule-dlv-26), [DLV-29](../delivery/README.md#rule-dlv-29)).
- **A package identifier is stable and never reused.** `27` and `29` are retired by [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006); their files remain as retirement records so an older citation resolves to an explanation rather than a broken reference.
- **Numbering is allocation order, not execution order.** `00`–`50` were allocated when the obligations were derived and `51`–`53` were added later.


## [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) package boundaries

The 51 active packages keep their accepted scope; WP20 is future-only; WP27/29 remain retired. Package numbering and anchors are stable; titles and runtime/contract responsibilities reflect [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009). The `.90` substeps are the explicit repository and integration acceptance attached to inherited domain work; each package's closure task depends on every other task mapped to the package.


[Producer artifacts and real integration](../producer-artifacts-and-integration.md) defines each package's producer outputs, permitted substitutes and real replacement evidence.
