# ArcForges Cloud Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **D-008** (ASP.NET Core **JIT** modular monolith), **D-010** (topology), **V-03**/**V-05e** (the evidence)
> Companions: [`../requirements/products/arcforges-cloud.md`](../requirements/products/arcforges-cloud.md), [`02-contracts-and-protocols.md`](02-contracts-and-protocols.md), [`13-observability-and-operations.md`](13-observability-and-operations.md)

---

## 1. Runtime decision

**ArcForges Cloud is an ASP.NET Core JIT modular monolith. Strict Native AOT is not a Cloud requirement** (**D-008**).

**V-03** made this structural rather than preferential. Under .NET 10 Native AOT, ASP.NET Core marks **"Other Authentication", MVC, Blazor Server, OData, Session and Spa as Not supported**, with **Minimal APIs and SignalR at Partial support**; the slim host omits HTTPS endpoints, HTTP/3, several logging providers and various routing constraints; reflection is unsupported, so every body type must be registered on a source-generated serialization context; and **not all runtime libraries are fully annotated for AOT compatibility**. A Cloud requiring anything beyond bearer-token authentication would be blocked outright.

| # | Consequence |
|---|---|
| RD-01 | **Azure SDKs, the durable agent loop, provider adapters, realtime integration, billing, policy and operational infrastructure all run inside the JIT boundary** (**D-008**). |
| RD-02 | **No effort is spent proving cloud-dependency AOT compatibility** (**D-008**, honoured in **V-05e**). |
| RD-03 | **If any Cloud component is ever moved into an AOT deliverable, its full dependency closure requires a publish proof at that time.** *Owner: Architecture Owner.* |
| RD-04 | **JIT does not relax the conventions.** Source-generated serialization, explicit registration and no reflection scanning remain the Cloud style, because they are correctness and start-up-performance practices independent of AOT. |
| RD-05 | **The corpus statement that realtime is unsupported under AOT is stale** (a .NET 8 status). Under .NET 10 it has partial support (**V-03**). The stale statement must not be carried forward, and the decision is unaffected. |

---

## 2. Roles and topology

Three production roles (`§1.1` of the cloud product requirements):

```
                          Edge (TLS, WAF, rate limit)
                                     │
                          private ingress only
                                     ▼
┌────────────────────────── ArcForges.Cloud.Host (API) ──────────────────────────┐
│ forwarded headers → request limits → correlation → exception normalisation      │
│ → authentication → authorization → rate limiting → endpoints → realtime hubs    │
│ → health and management                                                         │
└──────┬─────────────────────────────────────────────────────────────────┬────────┘
       │                                                                 │
       │ module application services                                     │ outbox
       ▼                                                                 ▼
   PostgreSQL  ──────────────────────────────────────────────►  Outbox dispatcher
       ▲                                                                 │
       │                                          ┌──────────────────────┴───────┐
       │                                          ▼                              ▼
ArcForges.Cloud.Worker                     Message broker              Realtime broadcast
  outbox dispatch · reconciliation                │
  indexing · notification fan-out                 ▼
  deletion propagation · maintenance      ArcForges.Cloud.TaskRunner
                                            isolated, ephemeral, task-scoped credentials
```

| # | Rule |
|---|---|
| RT-01 | **The API role is stateless.** Any state that must survive a request lives in the database, the broker or object storage. |
| RT-02 | **The API never scales to zero and runs at least two replicas.** |
| RT-03 | **TaskRunner work is isolated** with ephemeral storage, task-scoped credentials, time and resource limits, and network policy (`RX-06`, `RX-07` in the cloud requirements). |
| RT-04 | **A user automation is never a platform scheduled job** (`RR-01` there). |
| RT-05 | **Untrusted code never holds a platform identity** (`RR-05` there). |
| RT-06 | **Roles are split into further deployment units only on demonstrated need** for independent scaling, isolation, security or ownership. |

---

## 3. Host pipeline

Fixed order:

1. Forwarded headers and trusted proxy configuration
2. Request limits (body size, header size, timeouts)
3. Correlation and trace establishment
4. Exception normalisation into the semantic error contract
5. Authentication
6. Authorization
7. Rate limiting
8. Endpoint routing (Minimal API)
9. Realtime hubs
10. Health, readiness and liveness endpoints

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

Sixteen modules, each owning an application and domain boundary, its schema or explicit table set, a public module API and published events, and independent tests.

| Module | Owns |
|---|---|
| **Identity** | Users, authentication identities, recovery, sessions, security activity |
| **Workspace** | Workspaces, memberships, data region, protection profile |
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

| # | Rule |
|---|---|
| MD-01 | **A module never writes another module's tables**, enforced by architecture test. |
| MD-02 | **Cross-module interaction is a module API call or a published event.** |
| MD-03 | **A module's public API is the only reachable surface**; internal types are not referenced across modules. |
| MD-04 | **Entitlement, Policy and Audit are consumed by nearly every module and depend on almost none**, which keeps the dependency graph acyclic. |
| MD-05 | **Commerce depends on Entitlement's grant interface, never the reverse.** Entitlement must remain usable with Commerce entirely absent — for example in a self-hosted realm. |

---

## 5. Persistence

| # | Rule |
|---|---|
| PS-01 | **One primary PostgreSQL database, partitioned by module-owned schemas.** |
| PS-02 | **Short-lived connection and transaction per request or unit of work.** |
| PS-03 | **Optimistic concurrency by revision token** on every mutable aggregate. |
| PS-04 | **The outbox commits inside the business transaction** — this is what makes "no lost business fact" true. |
| PS-05 | **An inbox and idempotency table guard duplicate inbound messages and duplicate provider events.** |
| PS-06 | **Hot queries have explicit indexes and query-plan monitoring.** |
| PS-07 | **Large content goes to object storage.** The database holds metadata, ownership and lifecycle — never large binary bodies. |
| PS-08 | **Vector retrieval is a replaceable module** and never bleeds into the core document model (`IX-10`). |
| PS-09 | **Migration is a separate, gated deployment step.** Automatic migration on replica start-up is prohibited (`MG-01` in the cloud product requirements). |
| PS-10 | **Schema change uses expand/contract**, so two application versions coexist during a rolling deployment. |
| PS-11 | **A mapping and SQL-generation enhancement layer may be adopted after benchmarking**; it is not a prerequisite. |
| PS-12 | **A heavyweight reflection-driven ORM runtime is not required by the JIT decision, and its adoption remains a deliberate, benchmarked choice** rather than a default. |

---

## 6. Public API surface

| # | Rule |
|---|---|
| AP-01 | **The server is an ordinary REST-ish HTTP/JSON Minimal API.** The typed client is a **client-side generation layer only** — the server never "implements the client interface" to imitate local RPC. |
| AP-02 | **Standard web semantics are preserved**: status codes, headers, cache control, ETag and conditional requests, so proxies, browsers and non-.NET clients all work. |
| AP-03 | **OpenAPI is generated from the C# contracts** for observation and third parties — never maintained as a parallel handwritten source (**D-009**). |
| AP-04 | **API drift is controlled by** shared DTO and route constants, generated description artifacts, server-client contract integration tests, and a compatibility matrix of the previous stable client against the current server. |
| AP-05 | **File upload and download use standard HTTP content and streams.** Large objects are never base64-encoded into JSON. |
| AP-06 | **Timeout, cancellation and retry are explicit client policies**; a write retry requires `CommandId` idempotency. |
| AP-07 | **Every public DTO belongs to a source-generated serialization context.** |
| AP-08 | **Route versioning is explicit**, and the supported client set is declared by compatibility policy (`§7` of the policy requirements). |

---

## 7. Realtime

| # | Rule |
|---|---|
| RL-01 | **Realtime carries presence, chat deltas, task progress, approval resolution, device and session state, remote wake intents, and low-latency notifications.** |
| RL-02 | **Realtime is never**: the sole durable command log, a transaction mechanism, a large-file channel, a media path, the only means of state recovery, or a replacement for the HTTP API. |
| RL-03 | **Every significant event carries** event kind, sequence and revision, correlation, occurrence time, and the relevant resource, document or task identity. |
| RL-04 | **After reconnection a client queries the current snapshot, revision and sequence over HTTP, then resumes deltas** (`SN-01`–`SN-03` in the AI requirements). |
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
Outbox dispatcher (Worker role)
        ↓
├── internal reliable processing and projections
├── message broker for cross-module and deferred work
└── realtime broadcast to online clients
```

| # | Rule |
|---|---|
| EV-01 | **A broker is never the business source of truth** (`I-066`). |
| EV-02 | **Every consumer is idempotent**, keyed by `EventId`. |
| EV-03 | **Ordered sessions are used only where order genuinely matters.** |
| EV-04 | **The dead-letter queue is a first-class operational object**: monitored, alerted, inspectable, replayable. |
| EV-05 | **There is no global event sequence** (`EV-09` in the contracts architecture). Sequences are per stream or per resource. |
| EV-06 | **Backplane or additional messaging infrastructure is added on empirical need**, not pre-emptively. |

---

## 9. Background work

| # | Rule |
|---|---|
| BG-01 | Background services run inside the Worker role, or as isolated jobs in the TaskRunner role. |
| BG-02 | **Critical background work persists leases, retry counts and idempotency keys.** |
| BG-03 | **A crashed worker does not lose a task.** Task authority lives in the database; a worker is only an executor (`RV-05` in the AI requirements). |
| BG-04 | Splitting a worker into its own deployment role is a scaling or isolation decision — still a cloud role, never a reintroduced desktop worker process. |

---

## 10. Remote action

The cloud half of the **D-010** model:

| # | Rule |
|---|---|
| RA-01 | **Cloud creates a durable `ToolRequest`** with target device, capability, typed input, actor chain, risk, approval reference, expiry and idempotency key. |
| RA-02 | **The desktop pulls it.** Cloud never pushes into a local endpoint and never opens an inbound connection. |
| RA-03 | **Realtime carries only a restricted wake or intent signal** to a bound device. |
| RA-04 | **The desktop re-authorises locally**, executes through the owning product, and returns an **idempotent `ToolResult`**. |
| RA-05 | **A `ToolRequest` whose result never arrives is re-adjudicated through durable task state**, never blindly re-issued (`FL-06`, `FL-07` there). |
| RA-06 | **Cloud re-validates independently on every request** — session, workspace, entitlement, permission, device trust and capability. **The client is never the security authority** (`RX-10` in the cloud requirements). |

---

## 11. Multi-tenancy and isolation

| # | Rule |
|---|---|
| MT-01 | **Every cloud object belongs to a workspace** (`WS-07` in the identity requirements). |
| MT-02 | **Authorization is always `Actor → Membership → Workspace → Resource`.** Knowledge of an identifier never grants access. |
| MT-03 | **Workspace scoping is enforced at the data access layer**, not only in handlers, so a missing filter is a structural impossibility rather than a review finding. |
| MT-04 | **Search indexes are partitioned by realm and workspace** (`PM-05` in the knowledge requirements). |
| MT-05 | **Realm is the outermost boundary.** A self-hosted realm is a separate deployment with its own identity, policy and data authority (`§17` of the cloud requirements). |

---

## 12. Configuration and secrets

| # | Rule |
|---|---|
| CS-01 | **Configuration files hold references, never long-lived plaintext secrets.** |
| CS-02 | **Production secrets live in a managed vault in RBAC mode with purge protection.** |
| CS-03 | **Service-to-service authentication uses workload identity where available.** |
| CS-04 | **User Cloud BYOK secrets use envelope encryption**, not one vault entry per user (`SC-03` in the cloud product requirements). |
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
| SP-04 | **Autoscaling has a maximum cap** (`CC-03` in the cloud product requirements). |

---

## 15. Traceability

| Source | Consumed as |
|---|---|
| `I3 §16` | Modular monolith, host pipeline, public API relationship, realtime rules, database, reliable events and background tasks |
| `I3 §19` | Cloud-to-desktop bridging security model |
| `I4 §Stage 7` | Cloud capability responsibilities and isolation |
| `I4 §Stage 10` | Runtime roles, deployment, migration, resilience and operations |
| `I4 §Stage 13 §36–44` | Direct product-to-Cloud data path; Cloud as one logical platform |
| **D-008** | Cloud is a JIT modular monolith; no strict AOT requirement |
| **D-010** | Cloud never reaches local IPC; the durable request/result model |
| **V-03** | The ASP.NET Core AOT support surface that made the JIT decision structural, and the stale-realtime correction |
| **V-05e** | The instruction not to spend effort proving cloud-dependency AOT compatibility |
