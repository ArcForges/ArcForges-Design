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
| 27 | [ArcNotes edgeless canvas](27-arcnotes-edgeless-canvas.md) | 19, 25 |
| 28 | [ArcNotes typed properties and database views](28-arcnotes-properties-and-views.md) | 27 |
| 29 | [ArcNotes slides and presentation](29-arcnotes-slides.md) | 28 |

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
| 43 | [Managed AI, BYOK, routing and metering](43-managed-ai-routing-and-metering.md) | 16, 42 |
| 44 | [Dynamic policy and configuration control plane](44-dynamic-policy-and-configuration.md) | 23, 42 |
| 45 | [Operations, support and trust & safety](45-operations-support-and-trust-safety.md) | 12, 21, 44 |
| 46 | [Backup, disaster recovery and data health](46-backup-recovery-and-data-health.md) | 25, 45 |

### Phase K — Web and release

| # | Work package | Depends on |
|---|---|---|
| 47 | [Static public site](47-static-public-site.md) | 00 |
| 48 | [Account portal](48-account-portal.md) | 42, 44, 47 |
| 49 | [ArcChat Web companion](49-arcchat-web-companion.md) | 26, 48 |
| 50 | [Full-platform production release](50-full-platform-production-release.md) | 20, 29, 32, 35, 39, 43, 46, 49 |

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
| 06 | 07, 08, 10, 12, 13 |
| 07 | 08, 13, 18, 33, 36 |
| 08 | 09, 11, 13, 14 |
| 09 | 11, 14, 16, 41 |
| 10 | 14, 18, 33, 36 |
| 11 | 14, 16, 22, 41 |
| 12 | 21, 45 |
| 13 | 14, 33, 36 |
| 14 | 15, 16, 18 |
| 15 | 17 |
| 16 | 17, 43 |
| 17 | 20, 26, 41 |
| 18 | 19 |
| 19 | 20, 25, 27, 40 |
| 20 | 50 |
| 21 | 22, 45 |
| 22 | 23, 42 |
| 23 | 24, 30, 42, 44 |
| 24 | 25, 26, 30 |
| 25 | 26, 27, 35, 39, 40, 46 |
| 26 | 31, 33, 36, 49 |
| 27 | 28 |
| 28 | 29 |
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
| **F-013** — reference licence determinations | 00 (process and first product), then each product's own audit inside 18, 33, 36 and 15 |
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
| **PG-01** — per-product Reference Coverage Matrix | 00 (method), then 15, 18, 33, 36 |
| **PG-02** — item-level reconciliation inventory | 01 |
| **PG-03** — native dependency licence review | 13, then 33 and 36 |
| **PG-04** — runbook rehearsal evidence | 45 |
| **PG-05** — telemetry redaction proof | 12 |
| **PG-06** — invariant coverage | 05 |
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
- One main context advances the sequence serially (**D-019**). Implementation ownership is not split across autonomous agent teams.
