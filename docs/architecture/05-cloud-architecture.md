# ArcForges Cloud Architecture

[P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012) current implementation authorities: [Complete D1/Container transaction and recovery profile](data-model/04-d1-execution-profile.md); [Public gRPC-Web and application scopes](contracts/10-application-scope-and-streams.md).

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-008](../decisions/phase-1-foundation-decisions.md#rule-d-008)** (ASP.NET Core **Native AOT** modular monolith), **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** (topology), **[V-03](../assurance/phase-1-official-verification.md#rule-v-03)**/**[V-05e](../assurance/phase-1-official-verification.md#rule-v-05e)** (the evidence)
> Companions: [`../requirements/products/arcforges-cloud.md`](../requirements/products/arcforges-cloud.md), [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`13-observability-and-operations.md`](13-observability-and-operations.md)

---

## 1. Runtime decision

[P2-009](../decisions/phase-2-specification-decisions.md#rule-p2-009) requires Native AOT for the complete C# business host. The selected dependency/session/SQL/HTTP adapter closure is in [the platform matrix](21-platform-and-dependency-matrix.md#8-selected-p2-009-runtime-and-dependency-closure). Use explicit gRPC service/serializer registration, Minimal API exceptions, D1 binding adapter fixed SQL and supported cryptography. No automatic ASP.NET Session, dynamic ORM, runtime assembly scanning or JIT exception is allowed. WP06 publishes and exercises the real dependency closure; prose cannot satisfy that gate.

---

## 2. Deployment host and internal services

**One deployable host** (**[P2-006](../decisions/phase-2-specification-decisions.md#rule-p2-006)**; `§8` of the product scope). `ArcForges.Cloud.Host` is the single ASP.NET Core Native AOT executable. Business request handlers, bounded hint reads, canonical Task/Agent ports and ordinary leased background jobs run inside it as libraries. The sole model loop runs in CF Workflow, outside this process. Horizontal scale is **replicas of that one host**, never a second deployable with a different job.

```
Desktop gRPC-Web / Web gRPC-Web / Kotlin Android gRPC-Web
                   -> TLS ingress -> C# Native AOT Cloud (identical replicas)
                      explicit auth/tenancy/authorization/validation
                      business owners + leased bounded jobs
                      D1 + transactional outbox
                   -> generated RPC / object-byte exceptions -> Cloud Worker router
                      RunWorkflow: only model/tool loop -> Workers AI
                      RunStream DO: bounded disposable stream tail
                      R2: private immutable objects and staged transfers
C# <-> CF: authenticated typed HTTP ports, leases and idempotent receipts.
Cloud clients never connect inbound to a desktop; device tools pull from Cloud.
```

| # | Rule |
|---|---|
| <a id="rule-rt-01"></a>RT-01 | **The host is stateless between requests.** Anything that must survive a request lives in the database or object storage. |
| <a id="rule-rt-02"></a>RT-02 | **C# runs in restartable Cloudflare Containers that may sleep.** Worker ingress wakes ready instances; D1/DO/Queues preserve durable work. No minimum replica count is a correctness assumption. |
| <a id="rule-rt-03"></a>RT-03 | Every Container instance runs the same image and exposes the same bounded job entry points. Cron/Queues/DO alarms wake work; a perpetual hosted-service process is not a correctness assumption. |
| <a id="rule-rt-04"></a>RT-04 | Durable D1 leases and monotonic fences control concurrent job slices; a paused or replaced Container cannot publish after takeover. |
| <a id="rule-rt-05"></a>RT-05 | A job slice handles at most 100 items or 20 seconds then commits a checkpoint and reschedules. No unbounded generation loop or sleep-based real-time scheduler runs inside the Container. |
| <a id="rule-rt-06"></a>RT-06 | **A user automation is never a platform scheduled job** ([RR-01](../requirements/products/arcforges-cloud.md#rule-rr-01) in the cloud requirements). |
| <a id="rule-rt-07"></a>RT-07 | **Untrusted code never holds a platform identity** ([RR-05](../requirements/products/arcforges-cloud.md#rule-rr-05) there). |
| <a id="rule-rt-08"></a>RT-08 | **Splitting a hosted service into its own deployable is an architecture baseline change**, requiring demonstrated need for independent scaling, isolation, security or ownership. V1 does not require it and no design may assume it. |

> **Implementation evidence, 2026-09-06.** `ArcForges/src/Cloud` at commit `ede43db` contains exactly one web executable — `ArcForges.Cloud.Host` — referencing `ArcForges.Cloud.AgentRuntime`, `ArcForges.Cloud.BackgroundJobs`, `ArcForges.Cloud.PublicApi` and `ArcForges.Cloud.Realtime` as libraries. No `Worker` or `TaskRunner` executable exists. `ArcForges.Cloud.AppHost` is an Aspire orchestration host for local development only ([EN-05](../requirements/products/arcforges-cloud.md#rule-en-05)). Every cloud module is currently an `AssemblyPlaceholder.cs` scaffold with no implemented behaviour, so this topology correction is unblocked by existing code.

---

### Edge routes and binding graph

This is the authoritative routing table; arch 10 references it. All `/internal/*` paths are rejected before Container forwarding on every public hostname. Cloud's private exported handler is reachable only through service bindings. Retire the Hello World apex `/api/*` deployment at WP21.

| Host | Paths | Serving owner |
|---|---|---|
| api.arcforges.com | /api/*, /webhooks/*, documented /session/*, /objects/* and GET /.well-known/arcforges-realm.json only; other paths return 404 | Cloud Worker → C# business/auth/webhook owners or R2 byte facade |
| account.arcforges.com, chat.arcforges.com | /api/*, /session/*, /objects/*, /callbacks/* | Cloud Worker with exact host-bound cookie/CSRF rules |
| account.arcforges.com | /.well-known/assetlinks.json, /native/android/callback and remaining static paths | account Web profile; callback only hands one-use code/state to the verified Android app |
| chat.arcforges.com | remaining paths | chat Web profile |
| arcforges.com | all paths including /.well-known/assetlinks.json | site Web profile; RP association static file |
| www.arcforges.com | all paths | site Web edge → permanent HTTP 308 redirect to `https://arcforges.com`, preserving path and query before static asset handling; no independent API or session origin |
| ops.arcforges.com | operations assets and operator APIs | Cloud Worker plus operations static profile behind separate operator Access/OIDC identity; customer sessions rejected |
| docs.arcforges.com, downloads.arcforges.com, updates.arcforges.com | immutable documentation, packages/catalog, signed update feeds respectively | static artifact deployment; no customer cookies/business writes |
| status.arcforges.com | all | independently hosted status adapter, reachable during Cloud outage |
| notify.arcforges.com, news.arcforges.com | no Web routes | transactional and broadcast mail domains only |

Container port 8080 has no public ingress. Cloud Worker selects the Container; C# is the only business authority. Set `enableInternet=false`; configure the closed outbound host list and exported outbound proxy handler. `storage.internal` executes Cloud-owned named D1 plans, `objects.internal` accesses authorized R2 grants, `ai.internal` invokes the AI Worker service binding, and `feeds.internal` opens private DO projections. These virtual names have no public DNS fallback. AI Worker calls C# only through the Cloud Worker's private service binding. Per-direction HMAC/nonce/epoch checks in contracts 05 remain defense in depth. The handler routes exact host/path/method, strips client-forwarded private headers and rejects redirects to non-admitted destinations. No generic fetch proxy or arbitrary SQL endpoint exists.

Container external egress through the handler is restricted to configured Postmark/SES, FCM, Paddle, independent S3 backup and activated self-host/operator OIDC token/metadata origins. Provider paths and ports are 443 only; private/link-local addresses and unexpected redirects are refused. AI Worker uses the Workers AI binding, Brave Search and exact admitted Cloud connector/MCP HTTPS origins through its one tool adapter; there is no unrestricted model-driven URL fetch. Cloud bindings/secrets are never passed into extension code. Host/path allowlists and instance limits are versioned deployment config with validation and negative integration vectors.

Selected mechanism: [Containers outbound handlers](https://developers.cloudflare.com/containers/guides/outbound-traffic/) and [Worker connections](https://developers.cloudflare.com/containers/configuration/workers-connections/), checked 2026-09-17. Use the provider's outbound proxy export and certificate configuration only when HTTPS interception is actually configured. WP06/21 must prove the selected SDK/runtime wiring, blocked egress and public denial on a real deployment.

**Launch allocation authority.** [Model04 launch-capacity.v1](data-model/04-d1-execution-profile.md#launch-capacity-profile-v1) selects standard-2, four globally capped fixed realm slots and ten-minute idle sleep with bounded wake/readiness admission. Worker routing and Container configuration consume that same validated artifact; do not inherit the Hello World lite/one-slot configuration or assume provider autoscaling. The Vectorize/R2 reservation and alert budgets there complement, rather than replace, purchased entitlements and D1 constraints.

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

EventService.Poll uses the same pipeline. Generated output RPC and CF object routes are authenticated through the selected C# ports and never acquire an alternate business authorization path.

| # | Rule |
|---|---|
| <a id="rule-hp-01"></a>HP-01 | **All cloud communication is TLS.** |
| <a id="rule-hp-02"></a>HP-02 | **Startup, readiness and liveness are separate signals.** |
| <a id="rule-hp-03"></a>HP-03 | **HTTP, realtime and background work all drain gracefully.** |
| <a id="rule-hp-04"></a>HP-04 | **Endpoints are registered explicitly**, never by runtime assembly scanning. |
| <a id="rule-hp-05"></a>HP-05 | **Exception normalisation never leaks a stack trace, an internal type name or a storage detail** to a client. |
| <a id="rule-hp-06"></a>HP-06 | **Every response carries the correlation identity** so a user-reported problem is traceable. |

---

## 4. Modules

Twenty-one domain modules, following the [Cloud schema ownership map](data-model/01-cloud-data-model.md#1-schema-map), each owning an application and domain boundary, its schema or explicit table set, a public module API and published events, and independent tests.

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
| **PackageCatalog** | Publisher verification, package/version submission, review, publication and revocation; TrustSafety enforcement and Support reports remain separate owners |
| **Configuration** | Immutable deployment configuration revisions and atomic activation; Policy owns the governed policy projection and evaluation surface |

| # | Rule |
|---|---|
| <a id="rule-md-01"></a>MD-01 | **A module never writes another module's tables**, enforced by architecture test. |
| <a id="rule-md-02"></a>MD-02 | **Cross-module interaction is a module API call or a published event.** |
| <a id="rule-md-03"></a>MD-03 | **A module's public API is the only reachable surface**; internal types are not referenced across modules. |
| <a id="rule-md-04"></a>MD-04 | **Entitlement, Policy and Audit are consumed by nearly every module and depend on almost none**, which keeps the dependency graph acyclic. |
| <a id="rule-md-05"></a>MD-05 | **Commerce depends on Entitlement's grant interface, never the reverse.** Entitlement must remain usable with Commerce entirely absent — for example in a self-hosted realm. |

---

## 5. Persistence

| # | Rule |
|---|---|
| <a id="rule-ps-01"></a>PS-01 | **One primary D1 database per realm, partitioned by module-owned table prefixes; atomic families stay in that database.** |
| <a id="rule-ps-02"></a>PS-02 | **Short-lived connection and transaction per request or unit of work.** |
| <a id="rule-ps-03"></a>PS-03 | **Optimistic concurrency by revision token** on every mutable aggregate. |
| <a id="rule-ps-04"></a>PS-04 | **The outbox commits inside the business transaction** — this is what makes "no lost business fact" true. |
| <a id="rule-ps-05"></a>PS-05 | **An inbox and idempotency table guard duplicate inbound messages and duplicate provider events.** |
| <a id="rule-ps-06"></a>PS-06 | **Hot queries have explicit indexes and query-plan monitoring.** |
| <a id="rule-ps-07"></a>PS-07 | **Large content goes to object storage.** The database holds metadata, ownership and lifecycle — never large binary bodies. |
| <a id="rule-ps-08"></a>PS-08 | **Vector retrieval is a replaceable module** and never bleeds into the core document model ([IX-10](../requirements/06-knowledge-search-and-retrieval.md#rule-ix-10)). |
| <a id="rule-ps-09"></a>PS-09 | **Migration is a separate, gated deployment step.** Automatic migration on replica start-up is prohibited ([MG-01](../requirements/products/arcforges-cloud.md#rule-mg-01) in the cloud product requirements). |
| <a id="rule-ps-10"></a>PS-10 | **Schema change uses expand/contract**, so two application versions coexist during a rolling deployment. |
| <a id="rule-ps-11"></a>PS-11 | **A mapping and SQL-generation enhancement layer may be adopted after benchmarking**; it is not a prerequisite. |
| <a id="rule-ps-12"></a>PS-12 | Use the selected D1 binding adapter fixed-SQL mapping; no reflection-driven ORM enters the AOT host. |

---

## 6. Public API surface

| # | Rule |
|---|---|
| <a id="rule-ap-01"></a>AP-01 | Public business services implement handwritten proto through binary gRPC-Web unary methods and bounded server streams for all client platforms. Only the enumerated browser-auth/provider/object/AI/platform protocol exceptions use HTTP/JSON or their standard wire format. |
| <a id="rule-ap-02"></a>AP-02 | Business commands/queries use binary gRPC-Web with generated ArcResult and trailers. HTTP status/cache/ETag semantics apply only to the explicitly declared browser/object/provider/static exceptions; never expose a parallel REST CRUD surface. |
| <a id="rule-ap-03"></a>AP-03 | Handwritten proto is the business RPC authority. Descriptor sets generate C#/TS/Connect Kotlin records/clients and fixtures. JSON schemas document only the declared HTTP exceptions; OpenAPI is not a business generation stage. |
| <a id="rule-ap-04"></a>AP-04 | Descriptor compatibility, generated metadata/validation and real three-language package-consumer tests control drift. Published immutable artifacts are the integration boundary. |
| <a id="rule-ap-05"></a>AP-05 | **File upload and download use standard HTTP content and streams.** Large objects are never base64-encoded into JSON. |
| <a id="rule-ap-06"></a>AP-06 | **Timeout, cancellation and retry are explicit client policies**; a write retry requires `CommandId` idempotency. |
| <a id="rule-ap-07"></a>AP-07 | Public protobuf types use generated C#/TS serializers; declared HTTP exceptions use explicit source-generated JSON metadata. The same semantic validators apply before owner dispatch. |
| <a id="rule-ap-08"></a>AP-08 | **Route versioning is explicit**, and the supported client set is declared by compatibility policy (`§7` of the policy requirements). |

---

## 7. Event hints and live presentation

| # | Rule |
|---|---|
| <a id="rule-rl-01"></a>RL-01 | EventService.Poll/Watch carry the 17 existing typed hints. Live AI text uses ExecutionService.ReadOutput/WatchOutput over the same public gRPC-Web boundary; D1 task/message authority and transient-body rules remain separate. |
| <a id="rule-rl-02"></a>RL-02 | Hints and AI presentation never own durable commands, transactions, large objects, task outcomes or the only recovery path. |
| <a id="rule-rl-03"></a>RL-03 | Hints carry the numbered event envelope and the revision/identities declared by their payload; they never invent a global sequence. |
| <a id="rule-rl-04"></a>RL-04 | After loss or expired cursor, query current authoritative snapshots and resume from the returned cursor; no hidden partial backfill. |
| <a id="rule-rl-05"></a>RL-05 | Publish hints only after the owning transaction commits. Event delivery cannot commit domain state. |
| <a id="rule-rl-06"></a>RL-06 | A client acknowledgement is not a business commit. |
| <a id="rule-rl-07"></a>RL-07 | Losing hints never loses a business fact. |
| <a id="rule-rl-08"></a>RL-08 | EventService.Watch/Poll and ExecutionService.WatchOutput/ReadOutput use generated proto and durable owner/cursor recovery. |
| <a id="rule-rl-09"></a>RL-09 | Initial clients use bounded unary polling with the cadence/backoff in contracts 05; no required backplane, affinity or transport negotiation. |
| <a id="rule-rl-10"></a>RL-10 | C# gRPC-Web server streams expose authorized DO projections with finite lifetime and current authorization refresh under annex 10; no public AI WebSocket. |

---

## 8. Reliable events

```
Business transaction commits (state + outbox row, atomically)
        ↓
Outbox dispatcher (a hosted service in the host)
        ↓
├── module inbox consumers and versioned projections
├── CF dispatch/control and object-verification effects
├── Notification outbox → FCM adapter (wake only)
└── committed hint rows read by EventService.Poll
```

| # | Rule |
|---|---|
| <a id="rule-ev-01"></a>EV-01 | **Outbox/inbox delivery is never business authority**; owner state and the emitting outbox row commit atomically. |
| <a id="rule-ev-02"></a>EV-02 | **Every consumer is idempotent**, keyed by `EventId`. |
| <a id="rule-ev-03"></a>EV-03 | **Required ordering uses the owning outbox/inbox stream and fence**, never an undeclared broker session or global sequence. |
| <a id="rule-ev-04"></a>EV-04 | **D1 outbox/inbox dead-letter state** is monitored, inspectable and replayable. |
| <a id="rule-ev-05"></a>EV-05 | **There is no global event sequence** ([EV-09](02-contracts-and-protocols.md#rule-ev-09) in the contracts architecture). Sequences are per stream or per resource. |
| <a id="rule-ev-06"></a>EV-06 | **No separate broker or backplane is provisioned in V1.** A later addition requires measured need and an explicit design decision. |

---

## 9. Background work

| # | Rule |
|---|---|
| <a id="rule-bg-01"></a>BG-01 | **Background services are hosted services inside `ArcForges.Cloud.Host`** ([RT-03](#rule-rt-03)). There is no separate worker or task-runner deployable. |
| <a id="rule-bg-02"></a>BG-02 | **Critical background work persists leases, retry counts and idempotency keys.** |
| <a id="rule-bg-03"></a>BG-03 | **A crashed worker does not lose a task.** Task authority lives in the database; a worker is only an executor ([RV-05](../requirements/05-ai-and-agent-execution.md#rule-rv-05) in the AI requirements). |
| <a id="rule-bg-04"></a>BG-04 | Splitting a worker into its own deployment role is a scaling or isolation decision — still a cloud role, never a reintroduced desktop worker process. |

---

## 10. Remote action

The cloud half of the **[D-010](../decisions/phase-1-foundation-decisions.md#rule-d-010)** model:

| # | Rule |
|---|---|
| <a id="rule-ra-01"></a>RA-01 | **Cloud creates a durable `ToolRequest`** with target device, capability, typed input, actor chain, risk, approval reference, expiry and idempotency key. |
| <a id="rule-ra-02"></a>RA-02 | **The desktop pulls it.** Cloud never pushes into a local endpoint and never opens an inbound connection. |
| <a id="rule-ra-03"></a>RA-03 | **Realtime carries only a restricted wake or intent signal** to a bound device. |
| <a id="rule-ra-04"></a>RA-04 | **The desktop re-authorises locally**, executes through the owning product, and returns an **idempotent `ToolResult`**. |
| <a id="rule-ra-05"></a>RA-05 | **A `ToolRequest` whose result never arrives is re-adjudicated through durable task state**, never blindly re-issued ([FL-06](../requirements/05-ai-and-agent-execution.md#rule-fl-06), [FL-07](../requirements/05-ai-and-agent-execution.md#rule-fl-07) there). |
| <a id="rule-ra-06"></a>RA-06 | **Cloud re-validates independently on every request** — session, workspace, entitlement, permission, device trust and capability. **The client is never the security authority** ([RX-10](../requirements/03-cloud-services-and-sync.md#rule-rx-10) in the cloud requirements). |

---

## 11. Multi-tenancy and isolation

| # | Rule |
|---|---|
| <a id="rule-mt-01"></a>MT-01 | **Every cloud object belongs to a workspace** ([WS-07](../requirements/02-identity-account-and-workspace.md#rule-ws-07) in the identity requirements). |
| <a id="rule-mt-02"></a>MT-02 | **Authorization is always `Actor → owner/service grant → Workspace → Resource`.** Knowledge of an identifier never grants access. |
| <a id="rule-mt-03"></a>MT-03 | **Workspace scoping is enforced at the data access layer**, not only in handlers, so a missing filter is a structural impossibility rather than a review finding. |
| <a id="rule-mt-04"></a>MT-04 | **Search indexes are partitioned by realm and workspace** ([PM-05](../requirements/06-knowledge-search-and-retrieval.md#rule-pm-05) in the knowledge requirements). |
| <a id="rule-mt-05"></a>MT-05 | **Realm is the outermost boundary.** A self-hosted realm is a separate deployment with its own identity, policy and data authority (`§17` of the cloud requirements). |

---

## 12. Configuration and secrets

| # | Rule |
|---|---|
| <a id="rule-cs-01"></a>CS-01 | **Configuration files hold references, never long-lived plaintext secrets.** |
| <a id="rule-cs-02"></a>CS-02 | **Production secrets use Cloudflare Worker secrets or Secrets Store**, with environment-separated bindings, least privilege, audited access and rotation under [IRD-13](../decisions/phase-2-specification-decisions.md#rule-ird-13). |
| <a id="rule-cs-03"></a>CS-03 | **Service-to-service authentication uses workload identity where available.** |
| <a id="rule-cs-04"></a>CS-04 | **Envelope encryption is used for per-workspace secret material**, not one deployment-secret entry per workspace. **There are no user provider secrets** — end-user BYOK is excluded ([BY-01](../requirements/04-commerce-entitlement-and-credits.md#rule-by-01)–[BY-04](../requirements/04-commerce-entitlement-and-credits.md#rule-by-04), [I-015](../requirements/01-normative-glossary-and-invariants.md#rule-i-015) retired); provider credentials are deployment secrets ([DC-15](../requirements/11-policy-and-configuration.md#rule-dc-15)). |
| <a id="rule-cs-05"></a>CS-05 | **Logs, crash dumps and diagnostic bundles are redacted by default.** |
| <a id="rule-cs-06"></a>CS-06 | **Provider API keys are deployment-operator credentials isolated by provider and environment**, not customer workspace keys. Workspace authorization and data-key isolation remain separate controls. |

---

## 13. Failure isolation

Capabilities degrade independently. The full dependency-degradation matrix is in `§7` of the cloud product requirements. Structurally:

| # | Rule |
|---|---|
| <a id="rule-fi-01"></a>FI-01 | **A module's failure must not cascade.** Cross-module calls have timeouts, bulkheads and explicit fallbacks. |
| <a id="rule-fi-02"></a>FI-02 | **An AI provider outage must not affect sync**; a search outage must not affect writes; a notification outage must not affect task execution. |
| <a id="rule-fi-03"></a>FI-03 | **A degraded capability reports a specific, honest reason** (`§11` of the policy requirements). |
| <a id="rule-fi-04"></a>FI-04 | **Health endpoints report per-capability state**, which is what the public status page renders. |

---

## 14. Scaling posture

| # | Rule |
|---|---|
| <a id="rule-sp-01"></a>SP-01 | **Start as a modular monolith; split only on demonstrated need** for independent scaling, isolation, security or team ownership. |
| <a id="rule-sp-02"></a>SP-02 | **The seams are kept**: module boundaries, module APIs, published events and explicit persistence ownership make a later split mechanical rather than architectural. |
| <a id="rule-sp-03"></a>SP-03 | **Premature microservices and premature distributed messaging are prohibited.** |
| <a id="rule-sp-04"></a>SP-04 | **Autoscaling has a maximum cap** ([CC-03](../requirements/products/arcforges-cloud.md#rule-cc-03) in the cloud product requirements). |

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

[Platform runtime closure](21-platform-and-dependency-matrix.md#8-selected-p2-009-runtime-and-dependency-closure) owns the AOT/auth/SQL/HTTP adapter selection. [CF integration](contracts/05-cloudflare-integration.md) owns external execution/object ports and commit boundaries. This host implements those ports and canonical module operations; it runs no model loop.
