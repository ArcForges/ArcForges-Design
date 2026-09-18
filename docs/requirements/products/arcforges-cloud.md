# ArcForges Cloud — Product and Platform Requirements
> Effective scope: [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012) and [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) amend the technology and application ownership below. **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements / Products
> Governing authority: **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)** (ASP.NET Core **Native AOT** modular monolith), **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** (cloud topology and local action), **[D-003](../../decisions/phase-1-foundation-decisions.md#rule-d-003)** (provider facts deferred with a first-consumption trigger)
> Companions: [`../03-cloud-services-and-sync.md`](../03-cloud-services-and-sync.md), [`../04-commerce-entitlement-and-credits.md`](../04-commerce-entitlement-and-credits.md), [`../10-distribution-update-and-support.md`](../10-distribution-update-and-support.md), [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md), [`../../architecture/13-observability-and-operations.md`](../../architecture/13-observability-and-operations.md)

> **ArcForges Cloud is the continuity and remote-execution layer of ArcForges — one logical platform, never four per-product backends.**

Product capability requirements are specified in [`../03-cloud-services-and-sync.md`](../03-cloud-services-and-sync.md). **This document specifies the platform: runtime roles, dependency posture, environments, deployment, operations, resilience and the go-live threshold.**

---

## 1. Platform posture

| # | Requirement |
|---|---|
| <a id="rule-pp-01"></a>PP-01 | ArcForges Cloud is one C# Native AOT modular monolith per Container instance under [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009)/[P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012). The 21 module owners are enumerated in architecture 05, including PackageCatalog. D1, Durable Objects, Queues, Workflow/Workers AI and R2 are bound managed resources; no Node sidecar or second business host. |
| <a id="rule-pp-02"></a>PP-02 | **It is one logical platform**, internally partitioned by module — never split into per-product backends. |
| <a id="rule-pp-03"></a>PP-03 | One deployable C# Native AOT host contains business APIs, admission, canonical Task/Agent stores, simulator and bounded leased jobs. The sole model/tool loop runs in the separate CF Worker deployment; identical C# replicas are allowed, no role-selected Worker/TaskRunner. |
| <a id="rule-pp-04"></a>PP-04 | The first deployment uses Cloudflare Workers and Containers. Kubernetes and an independently operated container platform are outside this profile. |
| <a id="rule-pp-05"></a>PP-05 | **Cloud never connects to localhost, a named pipe, a Unix socket or local stdio** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). Local action is a durable `ToolRequest` that the owning desktop application pulls, re-authorises locally, executes, and answers with an idempotent `ToolResult`. |
| <a id="rule-pp-06"></a>PP-06 | **Cloud never scans a LAN** and never addresses a desktop directly. |
| <a id="rule-pp-07"></a>PP-07 | **Professional products reach Cloud directly** for their own identity, sync, storage and product-domain APIs; ArcChat is not a mandatory data gateway (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |

### 1.1 One deployable host, bounded internal work

API ingress, webhook processing, sync, AI dispatch/admission and result recording, scheduling, outbox dispatch, indexing, reconciliation, simulation and maintenance are internal responsibilities of the same host. Replicas run the same deployable application. Module boundaries, leases, resource budgets and recovery protect correctness without adding independent deployment roles.

| # | Requirement |
|---|---|
| <a id="rule-rr-01"></a>RR-01 | User automations are Cloud domain objects with concurrency and missed-run policies, not per-user infrastructure cron entries. Their scheduler runs inside the host. |
| <a id="rule-rr-02"></a>RR-02 | The official host runs in Cloudflare Containers and may scale to zero; bounded cold-start/availability acceptance is required. Worker routing, durable wake sources and D1 checkpoints replace always-on process assumptions. |
| <a id="rule-rr-03"></a>RR-03 | Internal work has bounded concurrency, memory, time and temporary storage. Durable claims, fencing and idempotency prevent duplicate model dispatch, charge settlement, simulation publication and maintenance effects after host loss. No background loop depends on an HTTP connection staying open. |
| <a id="rule-rr-04"></a>RR-04 | Arbitrary untrusted server-side code execution is excluded. A bounded simulator expression interpreter or trusted tool adapter does not authorize general code execution in the host. |
| <a id="rule-rr-05"></a>RR-05 | Secrets and resource access are purpose-bound to the admitted operation; no user input obtains the host identity or arbitrary host file/network access. |
| <a id="rule-rr-06"></a>RR-06 | AI activity, sync and ordinary product jobs have separate capacity budgets within the host. Load shedding and graceful drain prevent an agent or simulator from starving identity, billing webhooks and sync. |

---

## 2. Dependency baseline

The current baseline selections. **Every provider fact — availability, region tables, pricing, quotas, limits and terms — is deferred under [D-003](../../decisions/phase-1-foundation-decisions.md#rule-d-003)'s first-consumption rule and must be re-verified before it is relied upon.** *Owner: Commercial Operations Owner for commercial facts; Architecture Owner for capability facts.*

| Concern | Baseline selection | Notes |
|---|---|---|
| Public edge | Cloudflare Worker, WAF and rate limits | Terminates public ingress; forwards only the closed routes in architecture 05 |
| Application platform | Cloudflare Containers, reached through Worker bindings | Restartable C# Native AOT instances; explicit scale caps, wake sources and D1 fences |
| Relational store | Managed D1 | One D1 database per realm, module-owned prefixes and fixed atomic plans |
| Event hints | D1 outbox and DO feed via gRPC-Web Watch/Poll | Bounded hints; durable owners recover state |
| Asynchronous effects | D1 transactional outbox/inbox plus Cloudflare Queues/Cron wakes | Bounded retries/dead-letter; consumers deduplicate |
| Live AI presentation | Cloudflare Durable Object | Presentation only; Workflow and C# retain their existing authorities |
| Mobile push | FCM HTTP v1 behind Notification adapter | Android data-only wake; durable attention survives provider loss |
| Object storage | R2 plus an independent encrypted second-provider disaster copy | Exact object-version inventory and restore manifest under model 04 and architecture 22 |
| Secrets | Cloudflare deployment secret bindings and operator secret references | Separate environment identities, audited rotation, no customer key submission |
| Observability | An external observability and incident platform | Plus the platform's native signals |
| Transactional email | Postmark primary; SES emergency secondary | Notification owns correlated delivery intents and ambiguity reconciliation under architecture 13 |
| Infrastructure as code | A declarative IaC tool with pinned providers | State stored securely, never in version control |
| CI/CD | The build platform with provider-supported deployment authentication under [EN-08](#rule-en-08) | Protected short-lived or expiring deployment credentials |

| # | Requirement |
|---|---|
| <a id="rule-db-01"></a>DB-01 | **No provider name may enter a domain contract.** Storage is `ObjectStorage`, not a vendor type; realtime is a transport, not a domain concept; the AI gateway is infrastructure, not a product model ([RT-01](../05-ai-and-agent-execution.md#rule-rt-01) in the AI requirements). |
| <a id="rule-db-02"></a>DB-02 | **Every external dependency has an adapter and a stated degradation behaviour** (`§7`). |
| <a id="rule-db-03"></a>DB-03 | **Redis is not a V1 dependency.** Caching that a single-region deployment can do without is not introduced pre-emptively. |
| <a id="rule-db-04"></a>DB-04 | **A dedicated search cluster is not a V1 dependency.** Search sits behind an abstraction so the backend can change without a domain change ([IX-10](../06-knowledge-search-and-retrieval.md#rule-ix-10)). |
| <a id="rule-db-05"></a>DB-05 | **Do not install expensive infrastructure in advance "for performance."** Capacity is added against measured need. |

### 2.1 Region

| # | Requirement |
|---|---|
| <a id="rule-rg-01"></a>RG-01 | A deployment declares its Cloudflare jurisdiction/location settings and any legally supported residency promises. D1 is a single primary authority per realm; Worker placement is not a region-pinned business assumption. |
| <a id="rule-rg-02"></a>RG-02 | Provisioning preflight verifies the actual account plan and availability of Workers, Containers, D1, Durable Objects, Queues, R2, Workflows, Workers AI and Vectorize; record current quotas, retention, jurisdiction and outbound restrictions. Missing required capabilities block provisioning rather than silently choosing another topology. |
| <a id="rule-rg-03"></a>RG-03 | Resilience uses the managed service guarantees and explicit application retry/fence/recovery design. Do not claim operator-configured availability zones or customer-controlled D1 failover. |
| <a id="rule-rg-04"></a>RG-04 | Jurisdiction and supported location hints are versioned IaC inputs. Disaster recovery provisions a fresh fenced realm/resource set from the independent manifest; it never assumes a SQL region switch or unchanged resource IDs. |
| <a id="rule-rg-05"></a>RG-05 | **Workspace `DataRegion` exists from day one** ([WS-09](../02-identity-account-and-workspace.md#rule-ws-09)), and **no public residency claim is made** unless infrastructure legally guaranteeing it is in use ([RG-02](../07-security-privacy-and-trust.md#rule-rg-02) in the security requirements). |

---

## 3. Network and ingress

| # | Requirement |
|---|---|
| <a id="rule-nw-01"></a>NW-01 | **The API origin is never directly exposed to the public internet.** It uses internal ingress, reached only through the edge. |
| <a id="rule-nw-02"></a>NW-02 | Only the bound Worker can route to the Container. A failed or restarting instance is replaced within the configured capacity; callers receive bounded unavailability and reconcile commands through D1. There is no cloudflared connector pair to operate. |
| <a id="rule-nw-03"></a>NW-03 | Worker origin routing and private Container/service bindings require no cloudflared tunnel host or separate relay VM. |
| <a id="rule-nw-04"></a>NW-04 | **Three protection layers coexist**: edge WAF, a human-verification challenge on abuse-prone endpoints only, and **application-level rate limiting**. |
| <a id="rule-nw-05"></a>NW-05 | **A human-verification challenge must not be applied everywhere.** It belongs on sign-up, sign-in, recovery, support submission and other abuse-prone endpoints — never on ordinary product API traffic. |
| <a id="rule-nw-06"></a>NW-06 | **Rate limiting is never IP-only.** It is dimensioned by identity, workspace, device, endpoint class and cost class, because IP alone punishes shared networks and fails against distributed abuse. |
| <a id="rule-nw-07"></a>NW-07 | D1 is accessible only through the private Worker execution adapter with its deployment binding. No public SQL endpoint or general SQL-over-HTTP route is admitted. |
| <a id="rule-nw-08"></a>NW-08 | Use the bounded registered D1 plans and service-binding adapter in model 04. There is no PostgreSQL connection pool, arbitrary SQL proxy or per-request interactive transaction. |
| <a id="rule-nw-09"></a>NW-09 | Provider callbacks are a separate allowlisted ingress class: verify each provider-specific authentication mechanism before durable idempotent acceptance. Payment signatures and SES SNS signatures are verified; Postmark uses its dedicated HTTPS credential/IP policy and correlation, not a fabricated signature. Callback payloads never authorize a user action. |
| <a id="rule-nw-10"></a>NW-10 | **Cloud tasks require SSRF protection**: outbound destinations are validated against an allow policy, internal address ranges and metadata endpoints are blocked, and redirects are re-validated. |

---

## 4. Data platform

| # | Requirement |
|---|---|
| <a id="rule-dp-01"></a>DP-01 | **One primary relational database, with module-owned schemas or explicit table ownership** — not one database per module. |
| <a id="rule-dp-02"></a>DP-02 | **A module never writes another module's tables**. Cross-module interaction is through module APIs and events. |
| <a id="rule-dp-03"></a>DP-03 | D1 service failure is explicit unavailability. Guarded batches, durable receipts and primary-read reconciliation prevent duplicate or partially accepted business effects after retry; no customer-controlled database failover is assumed. |
| <a id="rule-dp-04"></a>DP-04 | Provision and verify the selected plan's D1 Time Travel retention and record its bookmark in the backup manifest. Independently export the fenced logical database and referenced object versions under model 04; restore evidence, not configured retention alone, satisfies recovery. |
| <a id="rule-dp-05"></a>DP-05 | **Platform backup is not the whole backup story.** An independent, encrypted logical backup to a second provider is also required (`§14` of the cloud requirements). |
| <a id="rule-dp-06"></a>DP-06 | **The transactional outbox commits with the business transaction**, and an inbox/idempotency table guards duplicate delivery. |
| <a id="rule-dp-07"></a>DP-07 | **Outbox/inbox dispatch is never the business source of truth.** Lost or replayed delivery cannot lose or duplicate a business fact. |
| <a id="rule-dp-08"></a>DP-08 | **Every queue consumer is idempotent.** Re-delivery must be indistinguishable from single delivery in effect. |
| <a id="rule-dp-09"></a>DP-09 | **Per-owner ordered dispatch is used only where the owner requires it**, through the declared outbox/inbox sequence and fence. No broker session or global ordering is introduced. |
| <a id="rule-dp-10"></a>DP-10 | **D1 outbox/inbox dead-letter state is a first-class operational object**, monitored, inspectable and replayable with duplicate effects prevented. |
| <a id="rule-dp-11"></a>DP-11 | **Realtime is not a task state database** ([I-066](../01-normative-glossary-and-invariants.md#rule-i-066), [SN-01](../05-ai-and-agent-execution.md#rule-sn-01)). State is queried; realtime accelerates. |

---

## 5. Secrets and identity

| # | Requirement |
|---|---|
| <a id="rule-sc-01"></a>SC-01 | Production secrets are injected through deployment secret references or a managed secret store, with least privilege, rotation and audited access. Non-secret operational policy is the mounted versioned configuration in [DC-01](../11-policy-and-configuration.md#rule-dc-01)–[DC-17](../11-policy-and-configuration.md#rule-dc-17), not a secret-store entry per business value. |
| <a id="rule-sc-02"></a>SC-02 | **Service-to-service authentication uses workload identity, not secrets**, wherever the platform supports it. |
| <a id="rule-sc-03"></a>SC-03 | Provider credentials belong to the deployment operator and are resolved server-side. There is no customer Cloud BYOK submission, key vault or reveal API. Self-hosting uses operator-funded remote credentials with the same host implementation. |
| <a id="rule-sc-04"></a>SC-04 | **Operator identity is independent of customer identity.** The operator surface must not authenticate through the customer identity system (`§10` of the distribution requirements). |
| <a id="rule-sc-05"></a>SC-05 | **Break-glass administrative access exists with two independent recovery routes**, under the constraints in `§9` of the distribution requirements. |
| <a id="rule-sc-06"></a>SC-06 | **Support staff can never silently become a user** ([`SC-06`](../10-distribution-update-and-support.md#rule-sc-06) there). |

---

## 6. Environments and deployment

Four layers:

| Layer | Purpose |
|---|---|
| **Local development** | Developer machines, with local orchestration tooling |
| **CI integration** | Automated verification |
| **Staging** | **Topology-compatible** with production |
| **Production** | The real thing |

| # | Requirement |
|---|---|
| <a id="rule-en-01"></a>EN-01 | **Staging is topology-compatible with production** — same shapes, same boundaries, same deployment mechanism — even at smaller scale. |
| <a id="rule-en-02"></a>EN-02 | **Production and non-production live in separate cloud subscriptions or accounts.** |
| <a id="rule-en-03"></a>EN-03 | **Production data is never copied to staging.** Staging uses synthetic data. |
| <a id="rule-en-04"></a>EN-04 | **Infrastructure is defined as code**, with pinned provider versions. |
| <a id="rule-en-05"></a>EN-05 | **Local development orchestration is not replaced by, and does not replace, production IaC.** They serve different purposes and both exist. |
| <a id="rule-en-06"></a>EN-06 | **IaC state is a secret**: stored in a secured backend, never in version control, and separated per environment. |
| <a id="rule-en-07"></a>EN-07 | **Portal-driven infrastructure changes are prohibited in production.** An emergency manual change is reconciled back into IaC promptly, and drift detection runs regularly. |
| <a id="rule-en-08"></a>EN-08 | CI uses provider-supported workload identity; Cloudflare deployment uses an expiring, narrowly scoped API token from a protected environment under [CF-03](../../architecture/22-deployment-and-release-execution.md#rule-cf-03). Rotation and revocation are rehearsed; secrets never enter artifacts or logs. |
| <a id="rule-en-09"></a>EN-09 | **Staging and production use different deployment identities**, and neither holds subscription-owner rights. |
| <a id="rule-en-10"></a>EN-10 | **Container images are published to a private registry**, and **production never rebuilds**: the same digest built once is promoted through environments. |
| <a id="rule-en-11"></a>EN-11 | **Deployment references an image digest, never a mutable tag.** |
| <a id="rule-en-12"></a>EN-12 | **Server builds produce an SBOM and provenance attestation** ([PK-20](../08-extensions-and-developer-platform.md#rule-pk-20) in the extension requirements, applied to first-party builds). |
| <a id="rule-en-13"></a>EN-13 | **Production deployment passes through a gated environment approval.** |
| <a id="rule-en-14"></a>EN-14 | **Rollback is one action.** Platform revisions retain the previous release so a rollback is immediate. |

### 6.1 Database migration

| # | Requirement |
|---|---|
| <a id="rule-mg-01"></a>MG-01 | **Automatic migration on application startup is prohibited for all replicas**. Every replica racing to migrate is a defect. |
| <a id="rule-mg-02"></a>MG-02 | **Migration is an independent, gated deployment step.** |
| <a id="rule-mg-03"></a>MG-03 | **Schema change uses expand/contract**, so old and new application versions coexist during a rolling deployment. |
| <a id="rule-mg-04"></a>MG-04 | **"Migration down" is not the rollback strategy.** Rollback is an application rollback or a forward fix; a destructive down-migration is not run against production data ([MG-09](../13-data-formats-and-portability.md#rule-mg-09) in the data requirements). |

---

## 7. Resilience and degradation

**Every ordinary provider failure must degrade predictably. No single ordinary provider failure may cause data loss, entitlement corruption, or damage to the local product experience.**

| Failure | Required behaviour |
|---|---|
| **Object storage unavailable** | Metadata operations continue where possible; uploads and downloads queue or fail cleanly with a specific reason; no partial commit; existing local data unaffected |
| **Database unavailable** | The API returns an honest degraded state; nothing is silently accepted; native tools and cached editing/search continue; Cloud AI and fresh Cloud data remain unavailable, and pending edits are clearly unsynced |
| **Event hints unavailable** | Clients keep bounded authoritative reads; expired cursors reset and reread without presenting partial history as complete. AI presentation reconnect follows the CF frame/range profile; no separate realtime-service failover |
| **Push provider unavailable** | Pending attention remains durable and readable via notification.list; foreground/reconnect polling recovers it. Alert operations; bounded TTL retries. Background delivery without GMS/permission is unavailable and stated; never mark an approval resolved from a send result |
| **Workers AI unavailable** | Stop dispatch and show typed unavailability. Release customer reservations only when the accounting outcome permits; retain uncertain supplier exposure for reconciliation. No provider substitution or customer charge for platform-caused retry. |
| **AI telemetry path unavailable** | Core provider metering and durable receipts remain authoritative. No AI Gateway or direct-provider bypass is a launch dependency. |
| **Observability platform unavailable** | The product continues operating normally; only visibility is degraded |
| **Worker ingress unavailable** | Cloud is unreachable; native product jobs and cached work continue; Cloud AI pauses and unsynced changes stay durable — the edge provider was never written into the business domain |
| **Email provider unavailable** | An emergency secondary exists for critical mail; **failover must never deliver two one-time codes for one request** |

| # | Requirement |
|---|---|
| <a id="rule-rs-01"></a>RS-01 | **Capabilities degrade independently** ([CL-03](../03-cloud-services-and-sync.md#rule-cl-03)). An AI outage must never stop ArcNotes sync. |
| <a id="rule-rs-02"></a>RS-02 | **Passkey authentication means an email outage does not lock every user out** (`§2.2` of the identity requirements). |
| <a id="rule-rs-03"></a>RS-03 | **Every dependency has a documented degradation path and a runbook** (`§9`). |

---

## 8. Observability

| # | Requirement |
|---|---|
| <a id="rule-ob-01"></a>OB-01 | **OpenTelemetry is the unified standard** across every host, with traces, metrics and structured logs correlated. |
| <a id="rule-ob-02"></a>OB-02 | **The application retains its own standard instrumentation**; a platform-managed agent supplements it rather than replacing it. |
| <a id="rule-ob-03"></a>OB-03 | **Platform-native signals are retained alongside** the external platform, so a failure of one does not blind the other. |
| <a id="rule-ob-04"></a>OB-04 | Every request carries correlation across edge, Cloud host, internal job/agent operation, database, realtime and outbound calls. |
| <a id="rule-ob-05"></a>OB-05 | **Observability must never become a user-content database** ([I-273](../01-normative-glossary-and-invariants.md#rule-i-273)). Chat bodies, note bodies, file paths, tokens and raw prompts never enter telemetry by default. |
| <a id="rule-ob-06"></a>OB-06 | **Audit and observability logs are completely separate systems** ([I-272](../01-normative-glossary-and-invariants.md#rule-i-272), [I-273](../01-normative-glossary-and-invariants.md#rule-i-273)) with separate retention, access control and purpose. |
| <a id="rule-ob-07"></a>OB-07 | **Desktop telemetry is stricter than cloud telemetry**: minimal, opt-in, and never carrying user content ([PV-06](../07-security-privacy-and-trust.md#rule-pv-06)). |
| <a id="rule-ob-08"></a>OB-08 | Required signal dimensions include: application and instance identity, build id, de-identified actor, transport, service/interface/method, capability, redacted resource id, command/task ids, correlation and causation, expected and result revision, duration, queue time, result code, native ABI/build where applicable, and reconnect/sequence-gap counters. |

---

## 9. Service levels, incidents and runbooks

| # | Requirement |
|---|---|
| <a id="rule-sl-01"></a>SL-01 | **An internal SLO set exists and is defined by user experience, not by "the process is running"** ([I-391](../01-normative-glossary-and-invariants.md#rule-i-391)). A responding server that cannot serve a sync request is down. |
| <a id="rule-sl-02"></a>SL-02 | **SLO ≠ external SLA** ([I-403](../01-normative-glossary-and-invariants.md#rule-i-403)). Publishing a commitment requires a deliberate decision and demonstrated performance. |
| <a id="rule-sl-03"></a>SL-03 | **Alerts are symptom-based, not exception-based.** Waking someone for every exception destroys the alerting channel's value. |
| <a id="rule-sl-04"></a>SL-04 | Incident severity is fixed: **SEV0** security or potential data loss; **SEV1** major paid cloud outage; **SEV2** critical functionality degraded; **SEV3** limited impact. |
| <a id="rule-sl-05"></a>SL-05 | **A possible personal-data breach is automatically SEV0** with the statutory notification clock as a hard deadline ([IN-06](../10-distribution-update-and-support.md#rule-in-06) in the distribution requirements). |
| <a id="rule-sl-06"></a>SL-06 | **Every SEV1-capable dependency has a runbook.** |
| <a id="rule-sl-07"></a>SL-07 | **The status page is independently hosted** ([SI-04](arcforges-web.md#rule-si-04) in the web requirements), reports per-capability state, and carries an **emergency alternate URL** in case the primary domain path is itself affected. |

### 9.1 Required runbooks

D1 unavailability and guarded retry · Time Travel recovery · independent fresh-realm restore · R2 outage and cross-provider blob restore · event-hint degradation and cursor reset · outbox/inbox backlog and dead-letter replay · Workers AI outage and uncertain supplier reconciliation · Worker/Container cold-start or ingress outage · email delivery ambiguity and failover · secret compromise and rotation · deployment rollback · migration failure · entitlement reconciliation repair · webhook loss recovery · data-health anomaly · security advisory publication · package containment.

### 9.2 Disaster recovery

| # | Requirement |
|---|---|
| <a id="rule-dr-01"></a>DR-01 | Disaster recovery uses one authoritative D1 realm plus independent encrypted logical/object backup and a rehearsed fresh Cloudflare resource deployment. It is not active-active and cannot rely on the failed original database remaining accessible. |
| <a id="rule-dr-02"></a>DR-02 | Exercise fresh-resource restore from IaC, secrets recovery and independent backups in the quarterly drill. Validate schema/hash counts, object inventory, new recovery generation, invalidated sessions/leases and reconciliation before reopening traffic. |
| <a id="rule-dr-03"></a>DR-03 | **Internal recovery objectives** are those in `§14.2` of the cloud requirements, and remain internal engineering objectives until a drill justifies publishing anything. |
| <a id="rule-dr-04"></a>DR-04 | **`backup.zip` is not a backup strategy.** Backups are structured, verified, restorable and drilled (`§14` there). |

---

## 10. Cost control

| # | Requirement |
|---|---|
| <a id="rule-cc-01"></a>CC-01 | **Cost control is an infrastructure function, not a monthly surprise.** |
| <a id="rule-cc-02"></a>CC-02 | **Budget alerts and anomaly detection are configured** across cloud spend, AI spend and storage growth. |
| <a id="rule-cc-03"></a>CC-03 | **Autoscaling has a maximum cap.** An unbounded scale-out is an availability risk and a financial one. |
| <a id="rule-cc-04"></a>CC-04 | **Cloud tasks have maximum concurrency**, per workspace and globally ([LP-04](../05-ai-and-agent-execution.md#rule-lp-04)). |
| <a id="rule-cc-05"></a>CC-05 | The authoritative usage, capacity, credit and supplier-cost ledgers belong to ArcForges. Adapter/gateway caps are secondary guards. The mounted configuration supplies real model rates, plan terms, capacity recovery and bounded resource policies under the commerce and configuration requirements. |
| <a id="rule-cc-06"></a>CC-06 | **Provider prepaid balance is monitored and alerted** ([LG-09](../05-ai-and-agent-execution.md#rule-lg-09) there). |

---

## 11. Operator surface

| # | Requirement |
|---|---|
| <a id="rule-op-01"></a>OP-01 | **`ops.arcforges.com` is never as publicly reachable as the customer surface.** It is protected at the edge by an independent access layer in addition to application authorization. |
| <a id="rule-op-02"></a>OP-02 | **Operator authentication does not use the customer identity system** ([SC-04](#rule-sc-04)). |
| <a id="rule-op-03"></a>OP-03 | The operator console's capabilities, role separation, purpose binding, prohibition on arbitrary SQL and audit requirements are specified in `§10` of the distribution requirements. |

---

## 12. Go-live threshold

**The threshold is "failure behaves correctly", not "the happy path works."**

Before the paid cloud goes live:

1. A full **Game Day** exercising SEV0 through SEV2 scenarios against the real production topology.
2. D1 unavailability/retry and Time Travel recovery exercised; independent fresh-resource restore proven.
3. Cross-provider blob restore proven.
4. Outbox/inbox backlog and dead-letter replay proven.
5. Event-hint degradation with authoritative reread and cursor reset proven.
6. Workers AI outage with correct customer reservations and supplier liability, no hidden fallback, proven.
7. Worker ingress outage with durable cached work and native jobs preserved, Cloud AI correctly unavailable, and reconnection recovery verified.
8. Email failover proven **without duplicate one-time codes**.
9. Deployment rollback exercised, and a migration failure recovered.
10. A fresh Cloudflare realm/resource rebuild rehearsed from IaC plus independent backups.
11. Webhook loss recovered by reconciliation; entitlement repair verified ([RC-01](../04-commerce-entitlement-and-credits.md#rule-rc-01)–[RC-03](../04-commerce-entitlement-and-credits.md#rule-rc-03) in the commerce requirements).
12. Every runbook in `§9.1` written, assigned and rehearsed at least once.
13. Backup health dashboard green with a proven restore, not merely a green backup job ([BK-06](../../architecture/07-sync-conflict-and-backup.md#rule-bk-06), [BK-07](../03-cloud-services-and-sync.md#rule-bk-07)).
14. Commercial go-live gates satisfied (`§18` of the commerce requirements).
15. Regional and regulatory gates satisfied where a conditional market is enabled (**[D-023](../../decisions/phase-1-foundation-decisions.md#rule-d-023)**).

---

## 13. Modules

The cloud modular monolith is partitioned into modules, each owning an application/domain boundary, its own schema or explicit table ownership, a public module API and events, independent tests, and a prohibition on other modules writing its tables:

The 21 rows in architecture 05 §3 are the complete current module inventory. PackageCatalog owns its authoring, review, publication and revocation records; Notification owns delivery intents; Scope Simulation owns simulator state. This requirements document does not maintain a second differently grouped module list.

Scope Simulation owns the durable simulator state and manifests required by [SIM-01](arcscope.md#rule-sim-01)–[SIM-20](arcscope.md#rule-sim-20); it is an internal module, not another service.

Architecture boundaries must be reconciled to [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) in [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md).

---

## 14. Acceptance scenarios

**Topology** — Worker ingress is the only public business path; Container origin and internal service routes are inaccessible publicly. Kill an instance and prove bounded errors, replacement, fencing and command reconciliation without duplicate effects.

**Scaling** — Worker ingress and restartable Containers use [launch-capacity.v1](../../architecture/data-model/04-d1-execution-profile.md#launch-capacity-profile-v1): four fixed standard-2 slots per realm, ten-minute idle sleep, bounded readiness/first-response deadlines and explicit D1/Vectorize/R2 reservations and budgets. Cold starts and unavailable dependencies return bounded typed outcomes. Durable work never depends on an always-on replica.

**Migration** — a rolling deployment with an expand/contract migration succeeds with mixed application versions live; no replica attempts migration at startup.

**Deployment** — the same image digest built once is promoted through staging to production; rollback follows the verified migration-mode compatibility horizon; an incompatible persisted state requires forward repair or independent fenced restore, with the stated RPO/RTO.

**Event hints and live presentation** — disable hint delivery and verify bounded authoritative reads; expired cursors return an explicit reset followed by a fresh snapshot. Interrupt CF presentation separately and recover its retained byte range or authoritative Task state under contracts 05; no fabricated complete sequence backfill.

**Outbox/inbox** — a consumer receives a message five times and produces one effect; a poisoned message lands in the dead-letter queue, is inspectable and is replayable.

**Storage** — the primary object store is unavailable; uploads fail cleanly with a specific reason and no partial commit; a cross-provider restore recovers a blob.

**Database** — inject D1 unavailability and ambiguous batch replies; authoritative state and receipts reconcile. Prove Time Travel to a recorded bookmark and separately restore without the original D1 database.

**Email** — after primary failure/unknown acceptance, reconcile before secondary delivery; retain one authoritative challenge and stable logical notification/dedup key. Duplicate physical messages may occur but contain the same still-valid one-use proof; retry cannot create extra valid codes or misleading delivered status.

**Edge** — Cloud is unreachable; cached editing/search and native capture/render remain available, new Cloud AI cannot start, and pending changes synchronize safely after recovery.

**Secrets/configuration** — operator provider credentials never reach clients or logs. The real host uses a mounted validated policy; updating rates creates a new version without repricing prior usage or resetting capacity. A non-production sample runs without proprietary code; production rejects missing/invalid pricing.

**SSRF** — a cloud task attempting to reach an internal address or a metadata endpoint is blocked, including through a redirect.

**Observability** — a request is traceable end to end by correlation; no user content appears in telemetry; audit and observability remain separate systems.

**Operations** — the operator surface is unreachable without the independent access layer; operator identity is separate from customer identity; every high-value access is audited.

---

## 15. Traceability

| Current document | Relationship |
|---|---|
| [ArcForges Cloud Architecture](../../architecture/05-cloud-architecture.md) | Defines the single deployment host, modules and reliable background work |
| [Deployment and Release Execution](../../architecture/22-deployment-and-release-execution.md) | Defines provisioning, deployment, migration and recovery procedures |
| [Observability and Operations Architecture](../../architecture/13-observability-and-operations.md) | Implements observability, incident, support and operator obligations |
| **[D-003](../../decisions/phase-1-foundation-decisions.md#rule-d-003)** | Provider capability and pricing facts are deferred with a first-consumption trigger |
| **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)** | [D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008) is amended by [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009)/[P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012): Cloud is an ASP.NET Core Native AOT Container; real AOT integration is a required gate |
| **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Cloud never touches local IPC; durable `ToolRequest` / `ToolResult` model |
| **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)** | Surface inventory including the private operator surface |
| **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-05e](../../assurance/phase-1-official-verification.md#rule-v-05e)** | Historical evidence for the earlier runtime decision; [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009)/[P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012) supersede its runtime/dependency conclusions |

## Cloudflare deployment profile

Official and explicitly supported custom-realm deployments use the same C# image plus Cloudflare Worker/Container/D1/DO/Queues/R2 resources and declared AI bindings. Operator-owned Cloudflare accounts and signed deployment/configuration manifests replace a generic PostgreSQL host prerequisite. A non-Cloudflare local server is not a promised equivalent deployment. Independent disaster backup, authentication/payment/push/search suppliers retain their enumerated external protocols. The detailed D1 capacity, schema, migration and recovery profile is a required deployment input and acceptance gate.
