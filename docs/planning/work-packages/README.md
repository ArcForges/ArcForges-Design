# Work Packages

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning
> Governing authority: **D-017** (numbered implementation work packages belong here), **D-019** (one serial numbered sequence, no predetermined maximum)
> Companions: [`../implementation-sequence.md`](../implementation-sequence.md), [`../../assurance/release-gates.md`](../../assurance/release-gates.md), [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md)

**One continuous numbered sequence, `00` → `50`.** Shared foundation, cloud, mobile, web and cross-product capability interleave at their real dependency positions; there is no separate per-product plan (`I2 §VI`).

The number is an identity, not a schedule. Ordering is by dependency; parallelism is governed by `§4` of [`../implementation-sequence.md`](../implementation-sequence.md).

---

## The sequence

### Phase A — Freeze and foundation

| # | Work package | Depends on |
|---|---|---|
| 00 | [Specification, naming and rights freeze](00-specification-naming-and-rights-freeze.md) | — |
| 01 | [Repository reconciliation and target layout](01-repository-reconciliation-and-target-layout.md) | 00 |
| 02 | [Build governance, packaging policy and analyzers](02-build-governance-and-analyzer-policy.md) | 01 |
| 03 | [Contract foundation and the licence boundary split](03-contract-foundation-and-licence-split.md) | 02 |
| 04 | [Identity, error, revision and versioning primitives](04-identity-error-and-versioning-primitives.md) | 03 |
| 05 | [Architecture and repository policy test suite](05-architecture-and-repository-policy-tests.md) | 02, 03 |
| 06 | [AOT, JIT and WebAssembly publish proof](06-aot-jit-and-wasm-publish-proof.md) | 03, 04, 05 |
| 07 | [Local persistence foundation](07-local-persistence-foundation.md) | 04, 06 |

### Phase B — Shared platform

| # | Work package | Depends on |
|---|---|---|
| 08 | [Local IPC transport and registration lifecycle](08-local-ipc-and-registration.md) | 06, 07 |
| 09 | [Capability, contribution and resource model](09-capability-contribution-and-resource-model.md) | 03, 08 |
| 10 | [Design system and desktop shell foundation](10-design-system-and-desktop-shell.md) | 06 |
| 11 | [Security foundation](11-security-foundation.md) | 04, 08, 09 |
| 12 | [Observability foundation](12-observability-foundation.md) | 04, 06 |
| 13 | [Four high-risk technical probes](13-high-risk-technical-probes.md) | 06, 07, 08 |

### Phase C — First real slice

| # | Work package | Depends on |
|---|---|---|
| 14 | [ArcChat Hub and minimal ArcNotes cross-process slice](14-hub-and-minimal-provider-slice.md) | 08, 09, 10, 11, 13 |
| 15 | [ArcChat conversation and project core](15-arcchat-conversation-core.md) | 14 |
| 16 | [Unified execution engine](16-unified-execution-engine.md) | 09, 11, 14 |
| 17 | [ArcChat independent core V1A](17-arcchat-independent-core.md) | 15, 16 |

### Phase D — ArcNotes core

| # | Work package | Depends on |
|---|---|---|
| 18 | [ArcNotes document core](18-arcnotes-document-core.md) | 07, 10, 14 |
| 19 | [ArcNotes search, import, export and portability](19-arcnotes-search-and-portability.md) | 18 |
| 20 | [First real cross-product workflow](20-first-cross-product-workflow.md) | 17, 19 |

### Phase E — First real cloud

| # | Work package | Depends on |
|---|---|---|
| 21 | [Cloud host, modules, persistence and migrations](21-cloud-host-and-persistence.md) | 03, 05, 12 |
| 22 | [Identity, workspace, device and session](22-identity-workspace-and-device.md) | 11, 21 |
| 23 | [Public API surface and generated clients](23-public-api-and-generated-clients.md) | 03, 22 |
| 24 | [Realtime, reliable events and recovery](24-realtime-and-reliable-events.md) | 23 |
| 25 | [Sync engine and blob lifecycle](25-sync-engine-and-blob-lifecycle.md) | 19, 24 |
| 26 | [Device presence, remote action and the tool bridge](26-remote-action-and-tool-bridge.md) | 17, 24, 25 |

### Phase F — ArcNotes completion

| # | Work package | Depends on |
|---|---|---|
| ~~27~~ | [ArcNotes edgeless canvas](27-arcnotes-edgeless-canvas.md) — **RETIRED** by P2-006 | — |
| 28 | [ArcNotes bounded properties and saved views](28-arcnotes-properties-and-views.md) | 19, 25 |
| ~~29~~ | [ArcNotes slides and presentation](29-arcnotes-slides.md) — **RETIRED** by P2-006 | — |

### Phase G — Mobile

| # | Work package | Depends on |
|---|---|---|
| 30 | [Mobile shared architecture and Apache boundary](30-mobile-shared-architecture.md) | 03, 23, 24 |
| 31 | [ArcChat Mobile Android remote closed loop](31-arcchat-mobile-android.md) | 26, 30 |
| 32 | [Mobile release engineering and store gates](32-mobile-release-and-store-gates.md) | 31 |

### Phase H — ArcScope

| # | Work package | Depends on |
|---|---|---|
| 33 | [ArcScope acquisition and session core](33-arcscope-acquisition-and-session.md) | 07, 10, 13, 26 |
| 34 | [ArcScope analysis, visualisation and reporting](34-arcscope-analysis-and-reporting.md) | 33 |
| 35 | [ArcScope integration and metadata sync](35-arcscope-integration-and-sync.md) | 25, 34 |

### Phase I — ArcSlate

| # | Work package | Depends on |
|---|---|---|
| 36 | [ArcSlate project, timeline and media model](36-arcslate-project-and-timeline.md) | 07, 10, 13, 26 |
| 37 | [ArcSlate playback and processing runtime](37-arcslate-playback-and-processing.md) | 36 |
| 38 | [ArcSlate render, export and colour management](38-arcslate-render-and-colour.md) | 37 |
| 39 | [ArcSlate integration and portability](39-arcslate-integration-and-portability.md) | 25, 38 |

### Phase J — Platform completion

| # | Work package | Depends on |
|---|---|---|
| 40 | [Knowledge, search and retrieval](40-knowledge-search-and-retrieval.md) | 19, 25 |
| 41 | [Extension platform and integrations](41-extension-platform-and-integrations.md) | 09, 11, 17 |
| 42 | [Commerce, entitlement and credits](42-commerce-entitlement-and-credits.md) | 22, 23 |
| 43 | [Cloud AI routing, metering and settlement](43-managed-ai-routing-and-metering.md) | 16, 42 |
| 44 | [Dynamic policy and configuration control plane](44-dynamic-policy-and-configuration.md) | 23, 42 |
| 45 | [Operations, support and trust & safety](45-operations-support-and-trust-safety.md) | 12, 21, 44 |
| 46 | [Backup, disaster recovery and data health](46-backup-recovery-and-data-health.md) | 25, 45 |

### Phase K — Web and release

| # | Work package | Depends on |
|---|---|---|
| 47 | [Static public site](47-static-public-site.md) | 00 |
| 48 | [Account portal](48-account-portal.md) | 42, 44, 47 |
| 49 | [ArcChat Web companion](49-arcchat-web-companion.md) | 26, 48 |
| 50 | [Full-platform production release](50-full-platform-production-release.md) | 20, 28, 32, 35, 39, 43, 46, 49, 51, 52 |
| 51 | [ArcScope deterministic Cloud simulator](51-arcscope-cloud-simulator.md) | 21, 23, 25, 33 |
| 52 | [The Cloud Harness](52-cloud-harness.md) | 15, 17, 21, 23, 42, 43 |

---

## Downstream dependency index

Which packages are blocked by each package's completion gate.

| # | Blocks |
|---|---|
| 00 | 01, 47 |
| 01 | 02 |
| 02 | 03, 05, 10 |
| 03 | 04, 05, 06, 09, 21, 23, 30 |
| 04 | 06, 07, 11, 12 |
| 05 | 06, 21 |
| 06 | 07, 08, 10, 12, 13, 17 |
| 07 | 08, 13, 18, 33, 36 |
| 08 | 09, 11, 13, 14 |
| 09 | 11, 14, 16, 41 |
| 10 | 14, 18, 33, 36 |
| 11 | 14, 16, 22, 41 |
| 12 | 21, 45 |
| 13 | 14, 33, 36 |
| 14 | 15, 16, 18 |
| 15 | 17, 52 |
| 16 | 17, 43 |
| 17 | 20, 26, 41, 52 |
| 18 | 19 |
| 19 | 20, 25, 28, 40 |
| 20 | 50 |
| 21 | 22, 45 |
| 22 | 23, 42 |
| 23 | 24, 30, 42, 44 |
| 24 | 25, 26, 30 |
| 25 | 26, 28, 35, 39, 40, 46, 51 |
| 26 | 31, 33, 36, 49 |
| ~~27~~ | — (retired) |
| 28 | 50 |
| 29 | 50 |
| 30 | 31 |
| 31 | 32 |
| 32 | 50 |
| 33 | 34 |
| 34 | 35 |
| 35 | 50 |
| 36 | 37 |
| 37 | 38 |
| 38 | 39 |
| 39 | 50 |
| 40 | 50 |
| 41 | 50 |
| 42 | 43, 44, 48 |
| 43 | 50 |
| 44 | 45, 48 |
| 45 | 46 |
| 46 | 50 |
| 47 | 48 |
| 48 | 49 |
| 49 | 50 |
| 50 | — |

---

## Deferred-gate scheduling

Every gate in [`../../assurance/open-gates-register.md`](../../assurance/open-gates-register.md) is satisfied by a named package.

| Gate | Satisfied in |
|---|---|
| **F-013** — reference licence determinations | **Closed 2026-09-05 by design-stage evidence** — the five matrices in [`../../assurance/reference-coverage/`](../../assurance/reference-coverage/README.md). Drift maintenance only: `15.07`, `18.08`, `33.07`, `36.07` |
| **F-023** — mobile provenance and dependency closure | 32 |
| **F-026** — typed HTTP client AOT packaging | 06 |
| **VG-01** — AI transparency marking | 43 |
| **VG-02** — MCP SDK pin and vocabulary mapping | 41 |
| **VG-03** — third-party control AOT proof | 10 |
| **VG-04** — desktop host AOT proof with the real contract set | 06 |
| **VG-06** — cloud AOT closure (dormant) | not scheduled; conditional on a decision not taken |
| **VG-07** — Android runtime posture confirmed from the artifact | 32 |
| **VG-08** — framework upgrade re-verification (recurring) | 02, and re-run on each upgrade |
| **VG-09** — iOS runtime re-verification (dormant) | deferred with the iOS build |
| **VG-10** — supplier onboarding and screening | 42 |
| **VG-11** — payout eligibility and currency | 42 |
| **VG-12** — regional enablement gates (conditional) | 42 |
| **VG-13** — store category fit and consumption-only | 32 |
| **PG-01** — per-product Reference Coverage Matrix | **Closed 2026-09-05 by design-stage evidence.** Registered as versioned inputs in `00.04`; drift maintenance in `15.07`, `18.08`, `33.07`, `36.07` |
| **PG-02** — item-level reconciliation inventory | **Closed 2026-09-05 by design-stage evidence** — [`../../assurance/implementation-state-reconciliation.md`](../../assurance/implementation-state-reconciliation.md). Drift validation in `01.00`; disposition execution in `01.01`–`01.05` |
| **PG-03** — native dependency licence review | 13, then 33 and 37. Shim-level dispositions already assigned (`§5.2` of the reconciliation evidence); two shims fenced pending substitute analyses in `35.04` and `39.05` |
| **PG-04** — runbook rehearsal evidence | 45 |
| **PG-05** — telemetry redaction proof | 12 |
| **PG-06** — design-stage invariant traceability | **Closed 2026-09-05 by design-stage evidence** — [`../../assurance/invariant-coverage.md`](../../assurance/invariant-coverage.md) `§7`, 421 of 421 mapped |
| **PG-11** — implementation-stage invariant enforcement | **Open.** Distributed across the owning packages named in the coverage mapping; accounting reported by `05.05`, which closes neither gate |
| **PG-07** — format fixture completeness | 19, 35, 39 |
| **PG-08** — hardware lab inventory | 13 |
| **PG-09** — extension protocol conformance | 41 |
| **PG-10** — provider test-environment coverage | 42, 43 |

---

## Conventions

- Each package is one file, `NN-slug.md`, and contains numbered sub-steps `WP-NN.MM`, each with what must be fully done, its testing requirement, and its own completion gate.
- Every package states the nine mandatory fields listed in `§6` of [`../implementation-sequence.md`](../implementation-sequence.md).
- A package's completion gate is machine-evaluated wherever possible and always names its evidence artifact.
- A package that discovers a genuine architecture conflict stops and raises it (**D-001**); it does not resolve it locally.
- **A package never re-creates a completed baseline audit.** The reference matrices and the code inventory are versioned planning inputs; packages consume them and check for drift ([`../evidence-driven-revisions.md`](../evidence-driven-revisions.md)).
- One main context advances the sequence serially (**D-019**). Implementation ownership is not split across autonomous agent teams.
- **A package identifier is stable and never reused.** `27` and `29` are retired by P2-006; their files remain as retirement records so an older citation resolves to an explanation rather than a broken reference.
- **Numbering is allocation order, not execution order, above `50`.** `00`–`50` were allocated when the sequence was derived, and a retired identifier is never recycled, so a package added afterwards takes the next free number. **`51` executes in Phase H after `33`, and `52` executes in Phase J after `43`; both are therefore upstreams of `50` despite their higher numbers.** The dependency graph in this file and each package's own header are authoritative for order; the numeral is not.
