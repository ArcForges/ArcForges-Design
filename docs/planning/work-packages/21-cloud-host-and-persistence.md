# WP-21 — Cloud Host, Modules, Persistence and Migrations

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `03`, `05`, `12` · Downstream: `22`, `45`, `51`, `52`

> **Goal.** Stand up the real cloud: a JIT modular monolith as **one deployable host** with lease-fenced internal services (**P2-006**), a fixed host pipeline order, module boundaries with owned schemas, a real database with a standalone migrator, reliable events, and background work — running against real infrastructure, not stubs.

---

## 1. Scope and purpose

**In scope.** The single cloud host and its pipeline; its bounded hosted services and their durable lease fencing; module structure with schema ownership and module-to-module rules; persistence with a standalone migrator; the outbox, inbox and idempotency infrastructure; background work; configuration and secrets; failure isolation; and instrumentation of the real pipeline.

**Out of scope.** Identity (`22`), the public API surface (`23`), realtime (`24`), sync (`25`), commerce (`42`), policy (`44`) and operations tooling (`45`) — this package is the substrate those land on.

**Why this package exists.** `I2 §III.6` requires the first real server version to use real infrastructure — real database, real HTTP, real realtime, real disconnected recovery. The substrate must exist before any module can be real.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) | The JIT decision, roles, pipeline order, modules, persistence, events, background work, isolation |
| [`../../requirements/products/arcforges-cloud.md`](../../requirements/products/arcforges-cloud.md) | Platform posture, dependency baseline, environments, resilience and the module list |
| **D-008**, **V-03** | Cloud is JIT; strict AOT is explicitly not required |
| `WP-03`, `WP-05`, `WP-12` output | Contracts, policy tests and instrumentation |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Cloud is an ASP.NET Core JIT modular monolith** (**D-008**). It must not be packaged as Native AOT for consistency (**V-03**). |
| BR-02 | **Cloud never connects to localhost, a named pipe, a domain socket or local standard I/O** (**D-010**). |
| BR-03 | **A module owns its schema or its explicit table set.** No module writes another module's tables. |
| BR-04 | **Modules communicate through a published module API or events**, never through direct data access. |
| BR-05 | **The host pipeline order is fixed** and asserted by a test — ordering defects here are security defects. |
| BR-06 | **Migrations run from a standalone migrator**, not from application start-up. |
| BR-07 | **A deployment is reversible**; a migration that cannot be rolled back is split into expand, deploy and contract phases. |
| BR-08 | **Every state-changing message is idempotent** through the outbox/inbox pattern. |
| BR-09 | **The database holds metadata, ownership and lifecycle — never large binary bodies** (`I3 §14.3`). |
| BR-10 | **Build once, promote the same artifact**; production never rebuilds. |
| BR-11 | **A failure in one capability degrades that capability, not the platform** (`§13` of the cloud architecture). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Host/` | The API role and its fixed pipeline |
| `src/Cloud/ArcForges.Cloud.BackgroundJobs/` | Hosted services — a **library** referenced by the host, not a deployable |
| `src/Cloud/ArcForges.Cloud.AgentRuntime/` | The single Harness — a **library** referenced by the host |
| `src/Cloud/ArcForges.Cloud.AppHost/` | Aspire orchestration for **local development only** (`EN-05`) |
| `src/Cloud/ArcForges.Cloud.Persistence/` | Store abstraction, unit of work, outbox and inbox |
| `src/Cloud/ArcForges.Cloud.Migrations/` | The standalone migrator and the numbered migration set |
| `src/Cloud/ArcForges.Cloud.Modules.*/` | Module skeletons with owned schemas, module APIs and events, reconciled against `WP-01` |
| `deploy/` | Environment definitions, infrastructure as code, and promotion configuration |
| `tests/CloudIntegrationTests/` | Pipeline order, module isolation, migration, outbox and failure-isolation suites |

**Major types introduced.** `ModuleDefinition`, `ModuleApi`, `ModuleEvent`, `UnitOfWork`, `OutboxMessage`, `InboxRecord`, `MigrationRunner`, `BackgroundJob`, `JobLease`, `CapabilityHealthReport`, `TenantScope`.

---

## 5. Required implementation work

### WP-21.00 — Host and pipeline

**What must be fully done.** The API host with the fixed pipeline order: correlation, request limits, authentication, tenancy resolution, authorization, validation, handling, and problem-detail mapping. The order is asserted by a test. The JIT posture is explicit and no AOT properties are set.

**Testing requirements.** A pipeline-order assertion test; a negative test asserting a request cannot reach a handler with tenancy unresolved; a posture inspection.

**Completion gate.** The pipeline order is asserted, no handler is reachable without tenancy resolution, and the JIT posture is explicit.

### WP-21.01 — One host and its bounded hosted services

**What must be fully done.** **One deployable host** — `ArcForges.Cloud.Host` — running the request pipeline, realtime hubs, the single Harness and every bounded background service as libraries (**P2-006**, `RT-03` of the cloud architecture). Every replica is identical: no role flag, no worker-only deployment, no leader chosen by configuration. Cross-replica concurrency is controlled by **durable leases with fencing** (`RT-04`), and every hosted service claims a bounded batch and yields — no unbounded loop exists in a request handler or a hosted service (`RT-05`). Scaling and failure characteristics differ per role.

**Testing requirements.** A structural test asserting exactly one web executable exists and no second deployable is produced; a multi-replica test proving two identical replicas do not both claim the same leased work; a fencing test proving a stale token cannot publish; a bounded-batch test asserting no hosted-service iteration exceeds its budget; a drain test proving a shutting-down replica completes or releases its in-flight work rather than abandoning a lease.

**Completion gate.** **N identical replicas run every hosted service safely under lease fencing**, no unbounded loop is reachable, and no second deployable exists.

### WP-21.02 — Module boundaries

**What must be fully done.** Each module owns its schema or explicit table set, publishes a module API and events, has independent tests, and is prevented from writing another module's tables. The module set is reconciled against the architecture's list using the `WP-01` inventory.

**Testing requirements.** A schema-ownership test asserting no cross-module write; a reference test asserting no module references another's internals; a reconciliation record against the architecture module list.

**Completion gate.** No module can write another module's tables or reference its internals, and the module set is reconciled and recorded.

### WP-21.03 — Persistence and the standalone migrator

**What must be fully done.** A real database with the numbered migration set applied by a standalone migrator. Migration is transactional per step, idempotent, resumable, and rehearsed forward and backward. The expand/deploy/contract pattern is implemented for any change that is not directly reversible.

**Testing requirements.** Forward migration on a clean database and on every historical fixture; interruption and resume; an expand/deploy/contract rehearsal; a rollback rehearsal.

**Completion gate.** Migration is resumable and rehearsed in both directions, and a non-reversible change is demonstrably handled by the three-phase pattern.

### WP-21.04 — Outbox, inbox and idempotency

**What must be fully done.** State changes and their outbound messages commit atomically through an outbox. Inbound messages deduplicate through an inbox keyed by message identity. A dead-letter path exists with replay. Message ordering guarantees are stated and enforced where required.

**Testing requirements.** Atomic commit test with an induced failure between state change and publish; duplicate-delivery test; dead-letter and replay test.

**Completion gate.** A failure between state change and publish never produces a lost or phantom message, and duplicate delivery has no additional effect.

### WP-21.05 — Background work

**What must be fully done.** Bounded hosted services inside the single host, each claiming work by **durable lease with a monotonic fence token**, at-least-once execution with idempotent handlers, visible queue depth and oldest-work age, and bounded retry with dead-lettering. Every replica runs every hosted service (`RT-03`); **a stale fence token cannot publish** (`RT-04`), and no hosted service runs an unbounded loop (`RT-05`). Also the **change-feed publisher** (`§9.1` of the cloud data model): commit-ordered `publish_seq` assignment under a per-workspace lease, with oldest-unpublished age as a monitored signal (`PB-05`).

**Testing requirements.** Lease expiry and takeover; a fencing test proving a stale token cannot publish; poison-message handling; a bounded-batch assertion that no hosted-service iteration exceeds its budget; a multi-replica test proving two identical replicas never both claim the same leased work; **a publisher test proving a change committed after a later one still receives a higher `publish_seq` and is never skipped by an advanced cursor** (`PB-01`, `PB-02`).

**Completion gate.** Leases expire and are taken over safely under fencing, poison messages dead-letter rather than looping, no unbounded loop is reachable, and **the change feed is provably commit-ordered** — a late-committing change is always delivered.

### WP-21.06 — Configuration, secrets and tenancy

**What must be fully done.** Configuration per environment with no secret in configuration files; secrets resolved through the platform secret service with managed identity. Tenancy scope is resolved once in the pipeline and enforced in every data access path.

**Testing requirements.** A secret-absence scan over configuration; a cross-tenant access test asserting refusal at the data layer even with a forged scope.

**Completion gate.** No secret exists in configuration, and cross-tenant access is refused at the data layer independently of the pipeline.

### WP-21.07 — Failure isolation and instrumentation

**What must be fully done.** A dependency failure degrades the capabilities that need it and no others, with capability health reflecting the degradation. The real pipeline is instrumented with correlation propagating into queues and workers.

**Testing requirements.** Per-dependency outage tests asserting scoped degradation; a correlation propagation test through queue and worker.

**Completion gate.** Each simulated dependency outage degrades only its dependent capabilities, and correlation survives every hop.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | The cloud schema, its ownership model and its migration baseline |
| Protocol | Problem-detail mapping and module events |
| UI | None directly; capability health becomes reportable |
| Security | Pipeline order, tenancy enforcement and secret handling are security controls |
| Platform | Container image, roles and environment promotion |
| Migration | The cloud migration mechanism and its rehearsal record |
| Compatibility | The cloud version axis and minimum-client relationship begin here |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Pipeline order and tenancy-required assertions | `WP-21.00` |
| Role composition results | `WP-21.01` |
| Schema ownership and module reference results, plus the reconciliation record | `WP-21.02` |
| Migration forward, backward, resume and three-phase rehearsal records | `WP-21.03` |
| Outbox atomicity, duplicate-delivery and dead-letter results | `WP-21.04` |
| Lease, poison-message and role-assertion results | `WP-21.05` |
| Configuration secret scan and cross-tenant refusal results | `WP-21.06` |
| Per-dependency degradation and correlation propagation results | `WP-21.07` |

---

## 8. Completion gate

**All of the following, with recorded evidence, against real infrastructure:**

1. The host pipeline order is asserted; no handler is reachable with tenancy unresolved; the JIT posture is explicit with no AOT properties.
2. Each runtime role starts only its declared components.
3. No module writes another module's tables or references its internals; the module set is reconciled and recorded.
4. Migration is transactional, idempotent, resumable, and rehearsed forward and backward, with the three-phase pattern demonstrated.
5. A failure between state change and publish never loses or invents a message; duplicate delivery has no additional effect; dead-letter replay works.
6. Background leases expire and are taken over safely; poison messages dead-letter; jobs never run on the API role.
7. No secret exists in configuration; cross-tenant access is refused at the data layer even with a forged scope.
8. Each simulated dependency outage degrades only its dependent capabilities, and correlation survives every hop.

---

## 9. Dependencies

**Upstream.** `03` (contracts), `05` (policy tests), `12` (instrumentation).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `22` — Identity | The host, modules and persistence to build identity into |
| `23`, `24`, `25`, `26` | The substrate every cloud capability sits on |
| `42`, `44` | Module boundaries and event infrastructure |
| `45` — Operations | A real host to operate, alert on and rehearse against |
