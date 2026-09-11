# ArcForges Cloud Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (ASP.NET Core **Native AOT** modular monolith), **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** (topology), **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**/**[V-05e](../assurance/phase-1-official-verification.md#rule-v-05e)** (the evidence)
> Companions: [`../requirements/products/arcforges-cloud.md`](../requirements/products/arcforges-cloud.md), [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`13-observability-and-operations.md`](13-observability-and-operations.md)

---

## 1. Runtime decision

[P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) requires Native AOT for the complete C# business host. The selected dependency/session/SQL/HTTP adapter closure is in [the platform matrix](21-platform-and-dependency-matrix.md#7-selected-p2-009-runtime-and-dependency-closure). Use explicit gRPC service/serializer registration, Minimal API exceptions, Npgsql fixed SQL and supported cryptography. No automatic ASP.NET Session, dynamic ORM, runtime assembly scanning or JIT exception is allowed. WP06 publishes and exercises the real dependency closure; prose cannot satisfy that gate.

---

## 2. Deployment host and internal services

**One deployable host** (**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**; `§8` of the product scope). `ArcForges.Cloud.Host` is the single ASP.NET Core Native AOT executable. Business request handlers, bounded hint reads, canonical Task/Agent ports and ordinary leased background jobs run inside it as libraries. The sole model loop runs in CF Workflow, outside this process. Horizontal scale is **replicas of that one host**, never a second deployable with a different job.

```
Desktop native gRPC / Web and RN gRPC-Web
                   -> TLS ingress -> C# Native AOT Cloud (identical replicas)
                      explicit auth/tenancy/authorization/validation
                      business owners + leased bounded jobs
                      PostgreSQL + transactional outbox
                   -> same-origin /ai, /objects -> CF Worker router
                      RunWorkflow: only model/tool loop -> Workers AI
                      RunStream DO: bounded disposable stream tail
                      R2: private immutable objects and staged transfers
C# <-> CF: authenticated typed HTTP ports, leases and idempotent receipts.
Cloud clients never connect inbound to a desktop; device tools pull from Cloud.
```

| # | Rule |
|---|---|
| RT-01 | **The host is stateless between requests.** Anything that must survive a request lives in the database or object storage. |
| RT-02 | **The host never scales to zero and runs at least two replicas**, so a single instance is never a correctness assumption. |
| <a id="rule-rt-03"></a>RT-03 | **Every replica is identical and runs the same hosted services.** There is no role flag, no worker-only deployment and no leader instance chosen by configuration. |
| <a id="rule-rt-04"></a>RT-04 | **Concurrency across replicas is controlled by durable leases with fencing**, not by deploying exactly one instance. A hosted service claims work by lease, renews while working, and loses it cleanly on expiry (`§9`). |
| <a id="rule-rt-05"></a>RT-05 | **A hosted service is bounded.** It claims a batch, processes it and yields. An unbounded generation loop inside a request handler or a hosted service is prohibited ([SIM-10](../requirements/products/arcscope.md#rule-sim-10) of the ArcScope requirements). |
| RT-06 | **A user automation is never a platform scheduled job** ([RR-01](../requirements/products/arcforges-cloud.md#rule-rr-01) in the cloud requirements). |
| RT-07 | **Untrusted code never holds a platform identity** ([RR-05](../requirements/products/arcforges-cloud.md#rule-rr-05) there). |
| RT-08 | **Splitting a hosted service into its own deployable is an architecture baseline change**, requiring demonstrated need for independent scaling, isolation, security or ownership. V1 does not require it and no design may assume it. |

> **Implementation evidence, 2026-09-06.** `ArcForges/src/Cloud` at commit `ede43db` contains exactly one web executable — `ArcForges.Cloud.Host` — referencing `ArcForges.Cloud.AgentRuntime`, `ArcForges.Cloud.BackgroundJobs`, `ArcForges.Cloud.PublicApi` and `ArcForges.Cloud.Realtime` as libraries. No `Worker` or `TaskRunner` executable exists. `ArcForges.Cloud.AppHost` is an Aspire orchestration host for local development only ([EN-05](../requirements/products/arcforges-cloud.md#rule-en-05)). Every cloud module is currently an `AssemblyPlaceholder.cs` scaffold with no implemented behaviour, so this topology correction is unblocked by existing code.

---

## 3. Host pipeline

Fixed request order (service registration remains explicit at startup):

1. Trusted forwarded headers/TLS context and bounded request/header/deadline limits.
2. Correlation and exception/status normalization wrapping all later work.
3. Routing and the declared gRPC-Web/CORS protocol adapter, with exact allowed Origin.
4. Native/browser/operator or CF service authentication; browser unsafe calls validate session-bound CSRF.
5. Realm/workspace/device scope resolution from authenticated identity and request metadata.
6. Current authorization, entitlement/capability admission and per-identity/capability rate limiting.
7. Generated contract validation, conditional revision/idempotency and the owning handler/transaction.
8. Typed reply/status and audit/trace completion. Health/readiness have their explicit minimal allowlist.

EventService.Poll uses the same pipeline. CF public presentation/object routes are authenticated through the selected C# ports and never acquire an alternate business authorization path.

| # | Rule |
|---|---|
| HP-01 | **All cloud communication is TLS.** |
| HP-02 | **Startup, readiness and liveness are separate signals.** |
| HP-03 | **HTTP, realtime and background work all drain gracefully.** |
| HP-04 | **Endpoints are registered explicitly**, never by runtime assembly scanning. |
| HP-05 | **Exception normalisation never leaks a stack trace, an internal type name or a storage detail** to a client. |
| HP-06 | **Every response carries the correlation identity** so a user-reported problem is traceable. |

---

## 4. Modules

Twenty domain modules, following the [Cloud schema ownership map](data-model/01-cloud-data-model.md#1-schema-map), each owning an application and domain boundary, its schema or explicit table set, a public module API and published events, and independent tests.

| Module | Owns |
|---|---|
| **Identity** | Users, authentication identities, recovery, sessions, security activity |
| **Workspace** | Single-owner workspaces, data region and data-access policy |
| **Devices** | Devices, installations, presence, trust, remote grants |
| **Entitlement** | Definitions, bundles, grants, revocations, resolver, snapshots, quotas |
| **Commerce** | Billing accounts, offers, price versions, purchase intents, orders, payments, subscriptions, provider events, reconciliation, credit ledger |
| **Chat** | Conversations, messages, branches, projects, personal memory |
| **Task** | Tasks, runs, plans, steps, attempts, approvals, steering, budgets, automations, triggers |
| **Agent** | Agent profiles, skills, provider and model catalogue, routing policy, AI usage and cost records |
| **Sync** | Sync scopes, cursors, changes, conflicts, tombstones, revisions |
| **Resource** | Cloud objects, blobs, upload sessions, integrity, storage usage, deletion propagation |
| **Search** | Search documents, index state, retrieval, evidence assembly |
| **Notification** | Notifications, preferences, push registrations, delivery |
| **Policy** | Features, flags, rollouts, kill switches, remote config, compatibility, provider and model availability, experiments, bundles |
| **Audit** | Security and high-value audit events |
| **Support** | Feedback, bug reports, support cases, access grants, diagnostic bundles, recovery cases |
| **TrustSafety** | Community reports, investigations, enforcement actions, appeals, security reports, advisories |
| **Notes** | Canonical notebooks, documents/blocks, properties, saved views and immutable history |
| **Scope** | Cloud simulator state and authorized metadata replicas; native capture/analysis authority remains in ArcScope |
| **Slate** | Authorized metadata replicas; native project/edit/render authority remains in ArcSlate |
| **Configuration** | Immutable deployment configuration revisions and atomic activation; Policy owns the governed policy projection and evaluation surface |

| # | Rule |
|---|---|
| MD-01 | **A module never writes another module's tables**, enforced by architecture test. |
| <a id="rule-md-02"></a>MD-02 | **Cross-module interaction is a module API call or a published event.** |
| <a id="rule-md-03"></a>MD-03 | **A module's public API is the only reachable surface**; internal types are not referenced across modules. |
| MD-04 | **Entitlement, Policy and Audit are consumed by nearly every module and depend on almost none**, which keeps the dependency graph acyclic. |
| <a id="rule-md-05"></a>MD-05 | **Commerce depends on Entitlement's grant interface, never the reverse.** Entitlement must remain usable with Commerce entirely absent — for example in a self-hosted realm. |

---

## 5. Persistence

| # | Rule |
|---|---|
| <a id="rule-ps-01"></a>PS-01 | **One primary PostgreSQL database, partitioned by module-owned schemas.** |
| PS-02 | **Short-lived connection and transaction per request or unit of work.** |
| PS-03 | **Optimistic concurrency by revision token** on every mutable aggregate. |
| <a id="rule-ps-04"></a>PS-04 | **The outbox commits inside the business transaction** — this is what makes "no lost business fact" true. |
| PS-05 | **An inbox and idempotency table guard duplicate inbound messages and duplicate provider events.** |
| PS-06 | **Hot queries have explicit indexes and query-plan monitoring.** |
| <a id="rule-ps-07"></a>PS-07 | **Large content goes to object storage.** The database holds metadata, ownership and lifecycle — never large binary bodies. |
| <a id="rule-ps-08"></a>PS-08 | **Vector retrieval is a replaceable module** and never bleeds into the core document model ([IX-10](../requirements/06-knowledge-search-and-retrieval.md#rule-ix-10)). |
| PS-09 | **Migration is a separate, gated deployment step.** Automatic migration on replica start-up is prohibited ([MG-01](../requirements/products/arcforges-cloud.md#rule-mg-01) in the cloud product requirements). |
| <a id="rule-ps-10"></a>PS-10 | **Schema change uses expand/contract**, so two application versions coexist during a rolling deployment. |
| PS-11 | **A mapping and SQL-generation enhancement layer may be adopted after benchmarking**; it is not a prerequisite. |
| PS-12 | Use the selected Npgsql fixed-SQL mapping; no reflection-driven ORM enters the AOT host. |

---

## 6. Public API surface

| # | Rule |
|---|---|
| AP-01 | Public business services implement the handwritten proto service definitions using native gRPC and unary gRPC-Web. Only the enumerated browser-auth/provider/object/AI/platform protocol exceptions use HTTP/JSON or their standard wire format. |
| AP-02 | **Standard web semantics are preserved**: status codes, headers, cache control, ETag and conditional requests, so proxies, browsers and non-.NET clients all work. |
| AP-03 | **OpenAPI is generated from the proto descriptors** for observation and third parties — never maintained as a parallel handwritten source (**[D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009)**). |
| AP-04 | **API drift is controlled by** shared DTO and route constants, generated description artifacts, server-client contract integration tests, and a compatibility matrix of the previous stable client against the current server. |
| AP-05 | **File upload and download use standard HTTP content and streams.** Large objects are never base64-encoded into JSON. |
| AP-06 | **Timeout, cancellation and retry are explicit client policies**; a write retry requires `CommandId` idempotency. |
| AP-07 | Public protobuf types use generated C#/TS serializers; declared HTTP exceptions use explicit source-generated JSON metadata. The same semantic validators apply before owner dispatch. |
| AP-08 | **Route versioning is explicit**, and the supported client set is declared by compatibility policy (`§7` of the policy requirements). |

---

## 7. Realtime

| # | Rule |
|---|---|
| RL-01 | **Realtime carries presence, chat deltas, task progress, approval resolution, device and session state, remote wake intents, and low-latency notifications.** |
| RL-02 | **Realtime is never**: the sole durable command log, a transaction mechanism, a large-file channel, a media path, the only means of state recovery, or a replacement for the HTTP API. |
| RL-03 | **Every significant event carries** event kind, sequence and revision, correlation, occurrence time, and the relevant resource, document or task identity. |
| <a id="rule-rl-04"></a>RL-04 | **After reconnection a client queries the current snapshot, revision and sequence over HTTP, then resumes deltas** ([SN-01](../requirements/05-ai-and-agent-execution.md#rule-sn-01)–[SN-03](../requirements/05-ai-and-agent-execution.md#rule-sn-03) in the AI requirements). |
| RL-05 | **Realtime is fed from the post-commit outbox and application notifications** (`§8`), never from a pre-commit path. |
| RL-06 | **A client acknowledgement is not a business commit.** |
| RL-07 | **Losing realtime never loses a business fact.** |
| RL-08 | **Realtime payloads use source-generated serialization** and centralised method-name constants — no scattered magic strings. |
| RL-09 | **Transport negotiation and fallback are permitted; the application layer's consistency semantics never change as a result.** |
| RL-10 | **Realtime connections and hub methods use the same identity model and explicit authorization** as HTTP endpoints. |

---

## 8. Reliable events

```
Business transaction commits (state + outbox row, atomically)
        ↓
Outbox dispatcher (a hosted service in the host)
        ↓
├── internal reliable processing and projections
├── message broker for cross-module and deferred work
└── realtime broadcast to online clients
```

| # | Rule |
|---|---|
| EV-01 | **A broker is never the business source of truth** ([I-066](../requirements/01-normative-glossary-and-invariants.md#rule-i-066)). |
| EV-02 | **Every consumer is idempotent**, keyed by `EventId`. |
| EV-03 | **Ordered sessions are used only where order genuinely matters.** |
| EV-04 | **The dead-letter queue is a first-class operational object**: monitored, alerted, inspectable, replayable. |
| EV-05 | **There is no global event sequence** ([EV-09](02-contracts-and-protocols.md#rule-ev-09) in the contracts architecture). Sequences are per stream or per resource. |
| EV-06 | **Backplane or additional messaging infrastructure is added on empirical need**, not pre-emptively. |

---

## 9. Background work

| # | Rule |
|---|---|
| BG-01 | **Background services are hosted services inside `ArcForges.Cloud.Host`** ([RT-03](#rule-rt-03)). There is no separate worker or task-runner deployable. |
| <a id="rule-bg-02"></a>BG-02 | **Critical background work persists leases, retry counts and idempotency keys.** |
| <a id="rule-bg-03"></a>BG-03 | **A crashed worker does not lose a task.** Task authority lives in the database; a worker is only an executor ([RV-05](../requirements/05-ai-and-agent-execution.md#rule-rv-05) in the AI requirements). |
| BG-04 | Splitting a worker into its own deployment role is a scaling or isolation decision — still a cloud role, never a reintroduced desktop worker process. |

---

## 10. Remote action

The cloud half of the **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** model:

| # | Rule |
|---|---|
| RA-01 | **Cloud creates a durable `ToolRequest`** with target device, capability, typed input, actor chain, risk, approval reference, expiry and idempotency key. |
| RA-02 | **The desktop pulls it.** Cloud never pushes into a local endpoint and never opens an inbound connection. |
| RA-03 | **Realtime carries only a restricted wake or intent signal** to a bound device. |
| RA-04 | **The desktop re-authorises locally**, executes through the owning product, and returns an **idempotent `ToolResult`**. |
| RA-05 | **A `ToolRequest` whose result never arrives is re-adjudicated through durable task state**, never blindly re-issued ([FL-06](../requirements/05-ai-and-agent-execution.md#rule-fl-06), [FL-07](../requirements/05-ai-and-agent-execution.md#rule-fl-07) there). |
| RA-06 | **Cloud re-validates independently on every request** — session, workspace, entitlement, permission, device trust and capability. **The client is never the security authority** ([RX-10](../requirements/03-cloud-services-and-sync.md#rule-rx-10) in the cloud requirements). |

---

## 11. Multi-tenancy and isolation

| # | Rule |
|---|---|
| MT-01 | **Every cloud object belongs to a workspace** ([WS-07](../requirements/02-identity-account-and-workspace.md#rule-ws-07) in the identity requirements). |
| MT-02 | **Authorization is always `Actor → owner/service grant → Workspace → Resource`.** Knowledge of an identifier never grants access. |
| <a id="rule-mt-03"></a>MT-03 | **Workspace scoping is enforced at the data access layer**, not only in handlers, so a missing filter is a structural impossibility rather than a review finding. |
| MT-04 | **Search indexes are partitioned by realm and workspace** ([PM-05](../requirements/06-knowledge-search-and-retrieval.md#rule-pm-05) in the knowledge requirements). |
| MT-05 | **Realm is the outermost boundary.** A self-hosted realm is a separate deployment with its own identity, policy and data authority (`§17` of the cloud requirements). |

---

## 12. Configuration and secrets

| # | Rule |
|---|---|
| <a id="rule-cs-01"></a>CS-01 | **Configuration files hold references, never long-lived plaintext secrets.** |
| <a id="rule-cs-02"></a>CS-02 | **Production secrets live in a managed vault in RBAC mode with purge protection.** |
| CS-03 | **Service-to-service authentication uses workload identity where available.** |
| CS-04 | **Envelope encryption is used for per-workspace secret material**, not one vault entry per workspace. **There are no user provider secrets** — end-user BYOK is excluded ([BY-01](../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [I-015](../requirements/01-normative-glossary-and-invariants.md#rule-i-015) retired); provider credentials are deployment secrets ([DC-15](../requirements/11-policy-and-configuration.md#rule-dc-15)). |
| CS-05 | **Logs, crash dumps and diagnostic bundles are redacted by default.** |
| CS-06 | **Provider API keys are isolated by provider, workspace and environment.** |

---

## 13. Failure isolation

Capabilities degrade independently. The full dependency-degradation matrix is in `§7` of the cloud product requirements. Structurally:

| # | Rule |
|---|---|
| FI-01 | **A module's failure must not cascade.** Cross-module calls have timeouts, bulkheads and explicit fallbacks. |
| FI-02 | **An AI provider outage must not affect sync**; a search outage must not affect writes; a notification outage must not affect task execution. |
| FI-03 | **A degraded capability reports a specific, honest reason** (`§11` of the policy requirements). |
| FI-04 | **Health endpoints report per-capability state**, which is what the public status page renders. |

---

## 14. Scaling posture

| # | Rule |
|---|---|
| SP-01 | **Start as a modular monolith; split only on demonstrated need** for independent scaling, isolation, security or team ownership. |
| SP-02 | **The seams are kept**: module boundaries, module APIs, published events and explicit persistence ownership make a later split mechanical rather than architectural. |
| SP-03 | **Premature microservices and premature distributed messaging are prohibited.** |
| SP-04 | **Autoscaling has a maximum cap** ([CC-03](../requirements/products/arcforges-cloud.md#rule-cc-03) in the cloud product requirements). |

---

## 15. Traceability

| Current document | Relationship |
|---|---|
| [ArcForges Cloud — Product and Platform Requirements](../requirements/products/arcforges-cloud.md) | Owns runtime, deployment and operational obligations |
| [Cloud Services, Sync, Assets and Data Integrity Requirements](../requirements/03-cloud-services-and-sync.md) | Owns Cloud capabilities, sync and continuity |
| [Cloud Data Model](data-model/01-cloud-data-model.md) | Defines module data, transactions and reliable-event persistence |
| **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Cloud is the Native AOT modular monolith under [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) |
| **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Cloud never reaches local IPC; the durable request/result model |
| **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)** | The ASP.NET Core AOT support surface that made the Native AOT decision structural, and the stale-realtime correction |
| **[V-05e](../assurance/phase-1-official-verification.md#rule-v-05e)** | Historical non-AOT evidence, superseded by the activated Cloud AOT proof under [P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) |

## Selected host dependencies and integration

[Platform runtime closure](21-platform-and-dependency-matrix.md#7-selected-p2-009-runtime-and-dependency-closure) owns the AOT/auth/SQL/HTTP adapter selection. [CF integration](contracts/05-cloudflare-integration.md) owns external execution/object ports and commit boundaries. This host implements those ports and canonical module operations; it runs no model loop.
