<a id="rule-wp-21"></a>

# WP-21 — Native AOT Cloud Host and Persistence

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: E — First real cloud
> Upstream: `03`, `05`, `12` · Downstream: `22`, `45`, `51`, `52`

> **Goal.** Stand up the real cloud: a Native AOT modular business host as **one deployable host** with lease-fenced internal services (**[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)**), a fixed host pipeline order, module boundaries with owned schemas, a real database with a standalone migrator, reliable events, and background work — running against real infrastructure, not stubs.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Cloud. Inputs: the assigned exact Contracts packages/descriptors and actual provider artifacts; upstream artifacts are selected by Cloud's integration manifest. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: owned candidate artifacts and generated contracts with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> Unit mocks use released Contracts fixtures; acceptance consumes actual pinned candidate providers. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The single cloud host and its pipeline; its bounded hosted services and their durable lease fencing; module structure with schema ownership and module-to-module rules; persistence with a standalone migrator; the outbox, inbox and idempotency infrastructure; background work; configuration and secrets; failure isolation; and instrumentation of the real pipeline.

**Out of scope.** Identity (`22`), the public API surface (`23`), realtime (`24`), sync (`25`), commerce (`42`), policy (`44`) and operations tooling (`45`) — this package is the substrate those land on.

**Why this package exists.** The [Cloud architecture](../../architecture/05-cloud-architecture.md) and [the mock policy](../implementation-sequence.md#3-what-may-be-mocked-and-what-may-not) require the first real server version to use real infrastructure — real database, real HTTP, real realtime, real disconnected recovery. The substrate must exist before any module can be real.

---

## 2. Required inputs and dependencies

**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md) | The Native AOT decision, roles, pipeline order, modules, persistence, events, background work, isolation |
| [`../../requirements/products/arcforges-cloud.md`](../../requirements/products/arcforges-cloud.md) | Platform posture, dependency baseline, environments, resilience and the module list |
| **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)**, **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)** | Cloud requires Native AOT across the selected production dependency closure |
| [WP-03](03-contract-foundation-and-licence-split.md#rule-wp-03), [WP-05](05-architecture-and-repository-policy-tests.md#rule-wp-05), [WP-12](12-observability-foundation.md#rule-wp-12) output | Contracts, policy tests and instrumentation |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | Cloud is one ASP.NET Core Native AOT business executable per replica, with the selected explicit auth/SQL/gRPC/HTTP adapter closure and zero trim/AOT diagnostics. CF owns the separate managed AI loop. |
| BR-02 | **Cloud never connects to localhost, a named pipe, a domain socket or local standard I/O** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |
| BR-03 | **A module owns its schema or its explicit table set.** No module writes another module's tables. |
| BR-04 | **Modules communicate through a published module API or events**, never through direct data access. |
| BR-05 | **The host pipeline order is fixed** and asserted by a test — ordering defects here are security defects. |
| BR-06 | **Migrations run from a standalone migrator**, not from application start-up. |
| BR-07 | **A deployment is reversible**; a migration that cannot be rolled back is split into expand, deploy and contract phases. |
| BR-08 | **Every state-changing message is idempotent** through the outbox/inbox pattern. |
| BR-09 | **The database holds metadata, ownership and lifecycle — never large binary bodies**. |
| BR-10 | **Build once, promote the same artifact**; production never rebuilds. |
| BR-11 | **A failure in one capability degrades that capability, not the platform** (`§13` of the cloud architecture). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Host/` | The API role and its fixed pipeline |
| `src/Cloud/ArcForges.Cloud.BackgroundJobs/` | Hosted services — a **library** referenced by the host, not a deployable |
| `src/Cloud/ArcForges.Cloud.AgentRuntime/` | Canonical Agent/Task integration ports, dispatch and reconciliation only; no loop. The AI repository owns RunWorkflow. |
| `src/Cloud/ArcForges.Cloud.AppHost/` | Aspire orchestration for **local development only** ([EN-05](../../requirements/products/arcforges-cloud.md#rule-en-05)) |
| `src/Cloud/ArcForges.Cloud.Persistence/` | Store abstraction, unit of work, outbox and inbox |
| `src/Cloud/ArcForges.Cloud.Migrations/` | The standalone migrator and the numbered migration set |
| `src/Cloud/ArcForges.Cloud.Modules.*/` | Module skeletons with owned schemas, module APIs and events, reconciled against [WP-01](01-repository-reconciliation-and-target-layout.md#rule-wp-01) |
| `deploy/` | Environment definitions, infrastructure as code, and promotion configuration |
| `tests/CloudIntegrationTests/` | Pipeline order, module isolation, migration, outbox and failure-isolation suites |

**Major types introduced.** `ModuleDefinition`, `ModuleApi`, `ModuleEvent`, `UnitOfWork`, `OutboxMessage`, `InboxRecord`, `MigrationRunner`, `BackgroundJob`, `JobLease`, `CapabilityHealthReport`, `TenantScope`.

---

## 5. Required implementation work

<a id="rule-wp-21.00"></a>

### WP-21.00 — Host and pipeline


**What must be fully done.** Implement the exact host pipeline in Cloud architecture: bounded trusted ingress, correlation/error wrapper, routing/gRPC-Web/CORS, authentication/CSRF, realm/workspace/device scope, authorization/admission/rate limit, validation/revision/idempotency and owner handler. Explicitly register all selected source-generated serializers/services and session/WebAuthn/OIDC adapters.

**Testing requirements.** AOT image inspection with zero diagnostics; ordered middleware/handler probes and missing/wrong-scope/CSRF/service-auth negative tests.

**Completion gate.** No business handler executes without its declared scope/authorization; the production closure contributes [VG-06](../../assurance/open-gates-register.md#rule-vg-06) proof.

<a id="rule-wp-21.01"></a>

### WP-21.01 — One host and its bounded hosted services


**What must be fully done.** Run request handlers, unary hints, canonical Agent/Task control ports and bounded DB-leased jobs inside the one C# host. CF RunWorkflow alone plans/invokes models/tools; no C# loop, Node sidecar or separate C# worker deployment. Replicas are identical; claim, renewal and fence checks occur at each selected transaction barrier.

**Testing requirements.** Two identical replicas contend and drain; stale holder cannot publish; actual CF dispatch/reconcile receipts deduplicate; bounded jobs yield.

**Completion gate.** Single C# process topology and fenced concurrency hold across replica loss without creating a second Harness.

<a id="rule-wp-21.02"></a>

### WP-21.02 — Module boundaries

**Fixed ownership input.** The [Cloud schema map](../../architecture/data-model/01-cloud-data-model.md#1-schema-map) declares 20 domain owners plus platform infrastructure. Map every table to that owner, including Notes, Scope, Slate and Configuration; preserve native Scope/Slate content authority. Existing scaffold names may be split/merged internally to enforce these owners, but cannot invent a second owner or deployment role. The shared-transaction participant list remains its own explicitly narrower contract.

**What must be fully done.** Each module owns its schema or explicit table set, publishes a module API and events, has independent tests, and is prevented from writing another module's tables. The module set is reconciled against the architecture's list using the [WP-01](01-repository-reconciliation-and-target-layout.md#rule-wp-01) inventory.

**Testing requirements.** A schema-ownership test asserting no cross-module write; a reference test asserting no module references another's internals; a reconciliation record against the architecture module list.

**Completion gate.** No module can write another module's tables or reference its internals, and the module set is reconciled and recorded.

<a id="rule-wp-21.03"></a>

### WP-21.03 — Versioned SQL migration and fenced cutover


**What must be fully done.** Implement the selected fixed SQL/Npgsql typed mappings, per-owner schemas/indexes, shared transaction families and standalone one-shot migrator. Use explicit column/type maps and revision predicates; no dynamic ORM/reflection mapping. Follow expand/contract and record restore-compatible schema/checkpoint versions.

**Testing requirements.** Real PostgreSQL integration, clean/upgrade/rollback-or-forward-repair migration corpus, concurrent revision conflicts and query plans.

**Completion gate.** Owned persistence and the migrator run from actual AOT artifacts with the defined consistency boundaries.

<a id="rule-wp-21.04"></a>

### WP-21.04 — Outbox, inbox and idempotency


**What must be fully done.** Implement transactional outbox/inbox and command dedup. Publish hint rows and CF dispatch/control intents only after commit; each consumer has immutable message/input identity, bounded retries/dead-letter and typed reconciliation. Replay only operations whose declared effect certainty permits it.

**Testing requirements.** Kill around commit/publish/ack, duplicate deliveries and ambiguous CF outcomes; verify one durable effect and visible dead-letter state.

**Completion gate.** Business state, notifications, dispatch and receipts cannot diverge through loss or duplicate delivery.

<a id="rule-wp-21.05"></a>

### WP-21.05 — Leases, publication and transaction ownership

**What must be fully done.** Implement the monotonic lease fence and the closed shared-unit-of-work participant list from the data-model overview. A stale holder cannot publish an effect. Sync publication serialises on the workspace watermark, chooses the lowest unpublished revision per aggregate with a durable round-robin key, and assigns cursor sequence only in the committed publication transaction; UUID is identity only.

**Testing requirements.** Use two replicas and real PostgreSQL: stale worker after takeover, same-millisecond UUIDs in reverse revision order, paused business transaction committing after a cursor advances, rollback, heavy and sparse aggregates competing, and bounded deadlock retries. Assert permitted write sets and optional Resource/Entitlement/Sync enlistment.

**Completion gate.** Every committed change remains publishable above the acknowledged cursor, each aggregate is ordered and sparse work is not starved. Lease loss prevents stale effects; [PG-17](../../assurance/open-gates-register.md#rule-pg-17) is actual database evidence, not an identifier-order argument.

<a id="rule-wp-21.06"></a>

### WP-21.06 — Configuration, secrets and resource-admission foundation

**What must be fully done.** Implement immutable validated mounted configuration snapshots and activation head, secret references and realm isolation. Provide the real Entitlement quota-budget/reservation/event repository and shared transaction ports required by uploads in [WP-23](23-public-api-and-generated-clients.md#rule-wp-23), including workspace and deployment staging limits. This is the production accounting kernel; [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42) adds commercial grants/paid-term resolution and [WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44) adds full policy distribution/activation controls. Early integration tests seed explicit test-realm grants and exercise real SQL, never in-memory mock balances.

**Testing requirements.** Restart with outstanding reservations; race two upload admissions against one quota; reject mixed/invalid configuration and secret leakage; verify grant provenance in the test realm and no implicit official entitlement.

**Completion gate.** Cloud endpoints can atomically reserve measured resources before the commercial UI/provider flows exist. Later work extends this kernel instead of replacing a fake quota implementation.

<a id="rule-wp-21.07"></a>

### WP-21.07 — Failure isolation and instrumentation

**What must be fully done.** A dependency failure degrades the capabilities that need it and no others, with capability health reflecting the degradation. The real pipeline is instrumented with correlation propagating into queues and workers.

**Testing requirements.** Per-dependency outage tests asserting scoped degradation; a correlation propagation test through queue and worker.

**Completion gate.** Each simulated dependency outage degrades only its dependent capabilities, and correlation survives every hop.

---

<a id="rule-wp-21.90"></a>
### WP-21.90 — Verify the owned artifact and real integration

**What must be fully done.** Implement the one AOT host, 20 module-owner topology, explicit PostgreSQL/SQL, migrations, transactional outbox, leases and CF integration-port foundations. Canonical Task/Chat/Commerce state remains here; the loop does not.

**Execution order.** Restore the pinned producer outputs assigned above, implement the preceding substeps using the fixed formal contracts, then verify this candidate against the actual upstream artifacts. Local mocks cover only the declared test boundary.

**Testing requirements.** Real AOT image plus database tests demonstrate module ownership, transaction/idempotency/fencing boundaries, restart and one-shot migrations.

**Completion gate.** Real AOT image plus database tests demonstrate module ownership, transaction/idempotency/fencing boundaries, restart and one-shot migrations. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

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
| Pipeline order and tenancy-required assertions | [WP-21.00](#rule-wp-21.00) |
| Single-deployable assertion, multi-replica lease exclusivity, stale-token fencing, bounded-batch and drain results | [WP-21.01](#rule-wp-21.01) |
| Schema ownership and module reference results, plus the reconciliation record | [WP-21.02](#rule-wp-21.02) |
| Migration forward, backward, resume and three-phase rehearsal records | [WP-21.03](#rule-wp-21.03) |
| Outbox atomicity, duplicate-delivery and dead-letter results | [WP-21.04](#rule-wp-21.04) |
| Lease takeover, fencing, poison-message dead-letter, no-unbounded-loop and commit-ordered-feed results | [WP-21.05](#rule-wp-21.05) |
| Configuration secret scan and cross-tenant refusal results | [WP-21.06](#rule-wp-21.06) |
| Per-dependency degradation and correlation propagation results | [WP-21.07](#rule-wp-21.07) |

---

## 8. Completion gate

**Runtime/closure producers.** [VG-06](../../assurance/open-gates-register.md#rule-vg-06) through [WP-21.00](#rule-wp-21.00). The named candidate must supply actual passing evidence; documentation does not close these gates.

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-21.90](#rule-wp-21.90) and all inherited domain-specific gates must pass on the same candidate closure. Real AOT image plus database tests demonstrate module ownership, transaction/idempotency/fencing boundaries, restart and one-shot migrations.

**[PG-19](../../assurance/open-gates-register.md#rule-pg-19) evidence:** [WP-21.03](#rule-wp-21.03) — Real version-guarded backfill, all-writer participation and fenced cutover; combine with release rehearsal. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**[PG-17](../../assurance/open-gates-register.md#rule-pg-17) evidence:** [WP-21.05](#rule-wp-21.05) — Real commit-ordered feed, per-aggregate revision order and fairness; combine with sync/bootstrap consumer evidence. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence, against real infrastructure:**

1. The host pipeline order is asserted; no handler is reachable with tenancy unresolved; Native AOT publish and the selected dependency closure pass.
2. **One deployable host runs every bounded hosted service** ([RT-03](../../architecture/05-cloud-architecture.md#rule-rt-03)); every replica is identical, with no role flag and no leader chosen by configuration.
3. No module writes another module's tables or references its internals; the module set is reconciled and recorded.
4. Migration is transactional, idempotent, resumable, and rehearsed forward and backward, with the three-phase pattern demonstrated.
5. A failure between state change and publish never loses or invents a message; duplicate delivery has no additional effect; dead-letter replay works.
6. Leases expire and are taken over safely under fencing; a stale token cannot publish; poison messages dead-letter; no hosted service runs an unbounded loop ([RT-05](../../architecture/05-cloud-architecture.md#rule-rt-05)); and **the change feed is provably commit-ordered** ([PB-01](../../architecture/data-model/01-cloud-data-model.md#rule-pb-01)).
7. No secret exists in configuration; cross-tenant access is refused at the data layer even with a forged scope.
8. Each simulated dependency outage degrades only its dependent capabilities, and correlation survives every hop.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [03 contract foundation and licence split](03-contract-foundation-and-licence-split.md#rule-wp-03)
- [05 architecture and repository policy tests](05-architecture-and-repository-policy-tests.md#rule-wp-05)
- [12 observability foundation](12-observability-foundation.md#rule-wp-12)

**Downstream — consumers of these released outputs.**

- [22 identity workspace and device](22-identity-workspace-and-device.md#rule-wp-22)
- [45 operations support and trust safety](45-operations-support-and-trust-safety.md#rule-wp-45)
- [51 arcscope cloud simulator](51-arcscope-cloud-simulator.md#rule-wp-51)
- [52 cloud harness](52-cloud-harness.md#rule-wp-52)

---
