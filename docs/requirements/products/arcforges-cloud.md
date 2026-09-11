# ArcForges Cloud — Product and Platform Requirements
> Current scope amendment: **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

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
| PP-01 | ArcForges Cloud is one C# Native AOT modular monolith per instance under P2-009. All 20 business modules and ordinary bounded jobs run in that process. PostgreSQL, CF Workflow/Workers AI and R2 are external managed services; no runtime Node sidecar. |
| PP-02 | **It is one logical platform**, internally partitioned by module — never split into per-product backends. |
| <a id="rule-pp-03"></a>PP-03 | One deployable C# Native AOT host contains business APIs, admission, canonical Task/Agent stores, simulator and bounded leased jobs. The sole model/tool loop runs in the separate CF Worker deployment; identical C# replicas are allowed, no role-selected Worker/TaskRunner. |
| PP-04 | **Kubernetes is not used in the first stage.** A managed container application platform is sufficient and materially cheaper to operate at this scale. |
| PP-05 | **Cloud never connects to localhost, a named pipe, a Unix socket or local stdio** (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). Local action is a durable `ToolRequest` that ArcChat Desktop pulls, re-authorises locally, executes, and answers with an idempotent `ToolResult`. |
| PP-06 | **Cloud never scans a LAN** and never addresses a desktop directly. |
| PP-07 | **Professional products reach Cloud directly** for their own identity, sync, storage and product-domain APIs; ArcChat is not a mandatory data gateway (**[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)**). |

### 1.1 One deployable host, bounded internal work

API ingress, webhook processing, sync, AI model execution, scheduling, outbox dispatch, indexing, reconciliation, simulation and maintenance are internal responsibilities of the same host. Replicas run the same deployable application. Module boundaries, leases, resource budgets and recovery protect correctness without adding independent deployment roles.

| # | Requirement |
|---|---|
| <a id="rule-rr-01"></a>RR-01 | User automations are Cloud domain objects with concurrency and missed-run policies, not per-user infrastructure cron entries. Their scheduler runs inside the host. |
| RR-02 | The official production host does not scale to zero and uses at least two replicas for its availability target. Replica count is not a separate service role; self-host/development may use one replica with an explicit availability limitation. |
| RR-03 | Internal work has bounded concurrency, memory, time and temporary storage. Durable claims, fencing and idempotency prevent duplicate model dispatch, charge settlement, simulation publication and maintenance effects after host loss. No background loop depends on an HTTP connection staying open. |
| RR-04 | Arbitrary untrusted server-side code execution is excluded. A bounded simulator expression interpreter or trusted tool adapter does not authorize general code execution in the host. |
| <a id="rule-rr-05"></a>RR-05 | Secrets and resource access are purpose-bound to the admitted operation; no user input obtains the host identity or arbitrary host file/network access. |
| RR-06 | AI activity, sync and ordinary product jobs have separate capacity budgets within the host. Load shedding and graceful drain prevent an agent or simulator from starving identity, billing webhooks and sync. |

---

## 2. Dependency baseline

The current baseline selections. **Every provider fact — availability, region tables, pricing, quotas, limits and terms — is deferred under [D-003](../../decisions/phase-1-foundation-decisions.md#rule-d-003)'s first-consumption rule and must be re-verified before it is relied upon.** *Owner: Commercial Operations Owner for commercial facts; Architecture Owner for capability facts.*

| Concern | Baseline selection | Notes |
|---|---|---|
| Public edge | A CDN/WAF edge provider | Terminates TLS, applies WAF and rate limiting, fronts every public surface |
| Application platform | A managed container application platform | Zone-redundant from creation |
| Relational store | Managed PostgreSQL | One primary database, module-owned schemas |
| Realtime | A managed realtime service | Delivery only; never a state store |
| Async messaging | A managed message broker | Never the business source of truth |
| Object storage | Primary object store plus an **independent second-provider** disaster copy | Per `§14` of the cloud requirements |
| Secrets | A managed key vault with RBAC and purge protection | Plus workload identity for service-to-service auth |
| Observability | An external observability and incident platform | Plus the platform's native signals |
| Transactional email | A transactional email provider, behind an adapter | With an emergency secondary |
| Infrastructure as code | A declarative IaC tool with pinned providers | State stored securely, never in version control |
| CI/CD | The build platform with federated identity to the cloud | No long-lived deployment secrets |

| # | Requirement |
|---|---|
| DB-01 | **No provider name may enter a domain contract.** Storage is `ObjectStorage`, not a vendor type; realtime is a transport, not a domain concept; the AI gateway is infrastructure, not a product model ([RT-01](../05-ai-and-agent-execution.md#rule-rt-01) in the AI requirements). |
| DB-02 | **Every external dependency has an adapter and a stated degradation behaviour** (`§7`). |
| DB-03 | **Redis is not a V1 dependency.** Caching that a single-region deployment can do without is not introduced pre-emptively. |
| DB-04 | **A dedicated search cluster is not a V1 dependency.** Search sits behind an abstraction so the backend can change without a domain change ([IX-10](../06-knowledge-search-and-retrieval.md#rule-ix-10)). |
| DB-05 | **Do not install expensive infrastructure in advance "for performance."** Capacity is added against measured need. |

### 2.1 Region

| # | Requirement |
|---|---|
| RG-01 | **A single primary region is chosen, and the choice is a deployment configuration, never a hard-coded business assumption.** |
| RG-02 | **A Region Preflight is mandatory at provisioning time**: the required capabilities — zone-redundant high availability, service tiers, private networking, backup features — must be confirmed **available in the chosen region at the time of provisioning**, because regional capability tables change. |
| RG-03 | **The production environment is zone-redundant from creation.** Retrofitting zone redundancy is frequently impossible without a rebuild. |
| RG-04 | **Region is a Terraform-level parameter from day one**, so a rebuild in another region is a configuration change rather than a redesign. |
| RG-05 | **Workspace `DataRegion` exists from day one** ([WS-09](../02-identity-account-and-workspace.md#rule-ws-09)), and **no public residency claim is made** unless infrastructure legally guaranteeing it is in use ([RG-02](../07-security-privacy-and-trust.md#rule-rg-02) in the security requirements). |

---

## 3. Network and ingress

| # | Requirement |
|---|---|
| <a id="rule-nw-01"></a>NW-01 | **The API origin is never directly exposed to the public internet.** It uses internal ingress, reached only through the edge. |
| NW-02 | **The edge-to-origin connection is redundant** — at least two connector instances — so a single connector failure is not an outage. |
| NW-03 | **No separate always-on virtual machine is provisioned merely to host the tunnel.** It runs as an ordinary workload on the application platform. |
| <a id="rule-nw-04"></a>NW-04 | **Three protection layers coexist**: edge WAF, a human-verification challenge on abuse-prone endpoints only, and **application-level rate limiting**. |
| NW-05 | **A human-verification challenge must not be applied everywhere.** It belongs on sign-up, sign-in, recovery, support submission and other abuse-prone endpoints — never on ordinary product API traffic. |
| <a id="rule-nw-06"></a>NW-06 | **Rate limiting is never IP-only.** It is dimensioned by identity, workspace, device, endpoint class and cost class, because IP alone punishes shared networks and fails against distributed abuse. |
| <a id="rule-nw-07"></a>NW-07 | **The production database is never open to the public internet.** Private networking only. |
| NW-08 | **Connection pooling is a platform feature, not a hand-rolled container**, wherever the managed service provides it. |
| <a id="rule-nw-09"></a>NW-09 | **A public webhook endpoint is a distinct ingress class**: signature-verified, fast-accept then queue, idempotent, and never trusted to carry authorization (`§4.1` of the commerce requirements). |
| <a id="rule-nw-10"></a>NW-10 | **Cloud tasks require SSRF protection**: outbound destinations are validated against an allow policy, internal address ranges and metadata endpoints are blocked, and redirects are re-validated. |

---

## 4. Data platform

| # | Requirement |
|---|---|
| DP-01 | **One primary relational database, with module-owned schemas or explicit table ownership** — not one database per module. |
| DP-02 | **A module never writes another module's tables**. Cross-module interaction is through module APIs and events. |
| DP-03 | **Zone-redundant high availability** on the production database. |
| DP-04 | **Point-in-time recovery with a retention window, plus geo-redundant backup**, is configured **at creation** — several backup options cannot be changed afterwards. |
| DP-05 | **Platform backup is not the whole backup story.** An independent, encrypted logical backup to a second provider is also required (`§14` of the cloud requirements). |
| DP-06 | **The transactional outbox commits with the business transaction**, and an inbox/idempotency table guards duplicate delivery. |
| DP-07 | **A message broker is never the business source of truth** ([I-066](../01-normative-glossary-and-invariants.md#rule-i-066)). Losing a message must never lose a business fact. |
| DP-08 | **Every queue consumer is idempotent.** Re-delivery must be indistinguishable from single delivery in effect. |
| DP-09 | **Ordered sessions are used only where order genuinely matters.** Global ordering is not imposed by default. |
| DP-10 | **The dead-letter queue is a first-class operational object**, monitored, alerted, inspectable and replayable. |
| DP-11 | **Realtime is not a task state database** ([I-066](../01-normative-glossary-and-invariants.md#rule-i-066), [SN-01](../05-ai-and-agent-execution.md#rule-sn-01)). State is queried; realtime accelerates. |

---

## 5. Secrets and identity

| # | Requirement |
|---|---|
| SC-01 | Production secrets are injected through deployment secret references or a managed secret store, with least privilege, rotation and audited access. Non-secret operational policy is the mounted versioned configuration in [DC-01](../11-policy-and-configuration.md#rule-dc-01)–[DC-17](../11-policy-and-configuration.md#rule-dc-17), not a secret-store entry per business value. |
| SC-02 | **Service-to-service authentication uses workload identity, not secrets**, wherever the platform supports it. |
| <a id="rule-sc-03"></a>SC-03 | Provider credentials belong to the deployment operator and are resolved server-side. There is no customer Cloud BYOK submission, key vault or reveal API. Self-hosting uses operator-funded remote credentials with the same host implementation. |
| <a id="rule-sc-04"></a>SC-04 | **Operator identity is independent of customer identity.** The operator surface must not authenticate through the customer identity system (`§10` of the distribution requirements). |
| SC-05 | **Break-glass administrative access exists with two independent recovery routes**, under the constraints in `§9` of the distribution requirements. |
| SC-06 | **Support staff can never silently become a user** (`SC-06` there). |

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
| EN-01 | **Staging is topology-compatible with production** — same shapes, same boundaries, same deployment mechanism — even at smaller scale. |
| EN-02 | **Production and non-production live in separate cloud subscriptions or accounts.** |
| EN-03 | **Production data is never copied to staging.** Staging uses synthetic data. |
| EN-04 | **Infrastructure is defined as code**, with pinned provider versions. |
| <a id="rule-en-05"></a>EN-05 | **Local development orchestration is not replaced by, and does not replace, production IaC.** They serve different purposes and both exist. |
| <a id="rule-en-06"></a>EN-06 | **IaC state is a secret**: stored in a secured backend, never in version control, and separated per environment. |
| <a id="rule-en-07"></a>EN-07 | **Portal-driven infrastructure changes are prohibited in production.** An emergency manual change is reconciled back into IaC promptly, and drift detection runs regularly. |
| <a id="rule-en-08"></a>EN-08 | **CI authenticates to the cloud with federated identity only** — no long-lived deployment credentials. |
| <a id="rule-en-09"></a>EN-09 | **Staging and production use different deployment identities**, and neither holds subscription-owner rights. |
| <a id="rule-en-10"></a>EN-10 | **Container images are published to a private registry**, and **production never rebuilds**: the same digest built once is promoted through environments. |
| <a id="rule-en-11"></a>EN-11 | **Deployment references an image digest, never a mutable tag.** |
| EN-12 | **Server builds produce an SBOM and provenance attestation** ([PK-20](../08-extensions-and-developer-platform.md#rule-pk-20) in the extension requirements, applied to first-party builds). |
| <a id="rule-en-13"></a>EN-13 | **Production deployment passes through a gated environment approval.** |
| <a id="rule-en-14"></a>EN-14 | **Rollback is one action.** Platform revisions retain the previous release so a rollback is immediate. |

### 6.1 Database migration

| # | Requirement |
|---|---|
| <a id="rule-mg-01"></a>MG-01 | **Automatic migration on application startup is prohibited for all replicas**. Every replica racing to migrate is a defect. |
| MG-02 | **Migration is an independent, gated deployment step.** |
| MG-03 | **Schema change uses expand/contract**, so old and new application versions coexist during a rolling deployment. |
| <a id="rule-mg-04"></a>MG-04 | **"Migration down" is not the rollback strategy.** Rollback is an application rollback or a forward fix; a destructive down-migration is not run against production data ([MG-09](../13-data-formats-and-portability.md#rule-mg-09) in the data requirements). |

---

## 7. Resilience and degradation

**Every ordinary provider failure must degrade predictably. No single ordinary provider failure may cause data loss, entitlement corruption, or damage to the local product experience.**

| Failure | Required behaviour |
|---|---|
| **Object storage unavailable** | Metadata operations continue where possible; uploads and downloads queue or fail cleanly with a specific reason; no partial commit; existing local data unaffected |
| **Database unavailable** | The API returns an honest degraded state; nothing is silently accepted; native tools and cached editing/search continue; Cloud AI and fresh Cloud data remain unavailable, and pending edits are clearly unsynced |
| **Realtime unavailable** | Clients fall back to polling the authoritative state; **no business fact is lost** ([SN-03](../05-ai-and-agent-execution.md#rule-sn-03)); reconnection backfills by sequence |
| **AI provider unavailable** | Reserved credits are released; routing falls back within the cost class or asks; **the user is not charged for platform-caused retries** ([CU-03](../05-ai-and-agent-execution.md#rule-cu-03)) |
| **AI gateway unavailable** | A direct-provider bypass path exists and is exercised, so the gateway is not a single point of failure |
| **Observability platform unavailable** | The product continues operating normally; only visibility is degraded |
| **Edge or tunnel unavailable** | Cloud is unreachable; native product jobs and cached work continue; Cloud AI pauses and unsynced changes stay durable — the edge provider was never written into the business domain |
| **Email provider unavailable** | An emergency secondary exists for critical mail; **failover must never deliver two one-time codes for one request** |

| # | Requirement |
|---|---|
| RS-01 | **Capabilities degrade independently** ([CL-03](../03-cloud-services-and-sync.md#rule-cl-03)). An AI outage must never stop ArcNotes sync. |
| RS-02 | **Passkey authentication means an email outage does not lock every user out** (`§2.2` of the identity requirements). |
| RS-03 | **Every dependency has a documented degradation path and a runbook** (`§9`). |

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
| SL-02 | **SLO ≠ external SLA** ([I-403](../01-normative-glossary-and-invariants.md#rule-i-403)). Publishing a commitment requires a deliberate decision and demonstrated performance. |
| SL-03 | **Alerts are symptom-based, not exception-based.** Waking someone for every exception destroys the alerting channel's value. |
| <a id="rule-sl-04"></a>SL-04 | Incident severity is fixed: **SEV0** security or potential data loss; **SEV1** major paid cloud outage; **SEV2** critical functionality degraded; **SEV3** limited impact. |
| <a id="rule-sl-05"></a>SL-05 | **A possible personal-data breach is automatically SEV0** with the statutory notification clock as a hard deadline ([IN-06](../10-distribution-update-and-support.md#rule-in-06) in the distribution requirements). |
| <a id="rule-sl-06"></a>SL-06 | **Every SEV1-capable dependency has a runbook.** |
| <a id="rule-sl-07"></a>SL-07 | **The status page is independently hosted** ([SI-04](arcforges-web.md#rule-si-04) in the web requirements), reports per-capability state, and carries an **emergency alternate URL** in case the primary domain path is itself affected. |

### 9.1 Required runbooks

Database failover and restore · point-in-time recovery · object-store outage · cross-provider blob restore · realtime outage · message-broker backlog and dead-letter replay · AI provider outage and gateway bypass · edge or tunnel outage · email provider failover · secret compromise and rotation · deployment rollback · migration failure · region rebuild · entitlement reconciliation repair · webhook loss recovery · data-health anomaly · security advisory publication · package containment.

### 9.2 Disaster recovery

| # | Requirement |
|---|---|
| DR-01 | **Disaster recovery is single-primary-region plus zone redundancy plus cross-region and cross-provider backup plus a tested rebuild** — **not** active-active. |
| DR-02 | **A region rebuild is a tested procedure**, exercised in a full quarterly disaster-recovery drill ([BK-06](../03-cloud-services-and-sync.md#rule-bk-06)). |
| DR-03 | **Internal recovery objectives** are those in `§14.2` of the cloud requirements, and remain internal engineering objectives until a drill justifies publishing anything. |
| <a id="rule-dr-04"></a>DR-04 | **`backup.zip` is not a backup strategy.** Backups are structured, verified, restorable and drilled (`§14` there). |

---

## 10. Cost control

| # | Requirement |
|---|---|
| CC-01 | **Cost control is an infrastructure function, not a monthly surprise.** |
| CC-02 | **Budget alerts and anomaly detection are configured** across cloud spend, AI spend and storage growth. |
| <a id="rule-cc-03"></a>CC-03 | **Autoscaling has a maximum cap.** An unbounded scale-out is an availability risk and a financial one. |
| CC-04 | **Cloud tasks have maximum concurrency**, per workspace and globally ([LP-04](../05-ai-and-agent-execution.md#rule-lp-04)). |
| CC-05 | The authoritative usage, capacity, credit and supplier-cost ledgers belong to ArcForges. Adapter/gateway caps are secondary guards. The mounted configuration supplies real model rates, plan terms, capacity recovery and bounded resource policies under the commerce and configuration requirements. |
| CC-06 | **Provider prepaid balance is monitored and alerted** ([LG-09](../05-ai-and-agent-execution.md#rule-lg-09) there). |

---

## 11. Operator surface

| # | Requirement |
|---|---|
| OP-01 | **`ops.arcforges.com` is never as publicly reachable as the customer surface.** It is protected at the edge by an independent access layer in addition to application authorization. |
| OP-02 | **Operator authentication does not use the customer identity system** ([SC-04](#rule-sc-04)). |
| OP-03 | The operator console's capabilities, role separation, purpose binding, prohibition on arbitrary SQL and audit requirements are specified in `§10` of the distribution requirements. |

---

## 12. Go-live threshold

**The threshold is "failure behaves correctly", not "the happy path works."**

Before the paid cloud goes live:

1. A full **Game Day** exercising SEV0 through SEV2 scenarios against the real production topology.
2. Database failover exercised; point-in-time restore proven.
3. Cross-provider blob restore proven.
4. Message-broker backlog and dead-letter replay proven.
5. Realtime outage with client fallback and sequence backfill proven.
6. AI provider outage with credit release and fallback proven.
7. Edge/tunnel outage with durable cached work and native jobs preserved, Cloud AI correctly unavailable, and reconnection recovery verified.
8. Email failover proven **without duplicate one-time codes**.
9. Deployment rollback exercised, and a migration failure recovered.
10. A region rebuild rehearsed from IaC plus backups.
11. Webhook loss recovered by reconciliation; entitlement repair verified ([RC-01](../04-commerce-entitlement-and-credits.md#rule-rc-01)–[RC-03](../04-commerce-entitlement-and-credits.md#rule-rc-03) in the commerce requirements).
12. Every runbook in `§9.1` written, assigned and rehearsed at least once.
13. Backup health dashboard green with a proven restore, not merely a green backup job ([BK-06](../../architecture/07-sync-conflict-and-backup.md#rule-bk-06), [BK-07](../03-cloud-services-and-sync.md#rule-bk-07)).
14. Commercial go-live gates satisfied (`§18` of the commerce requirements).
15. Regional and regulatory gates satisfied where a conditional market is enabled (**[D-023](../../decisions/phase-1-foundation-decisions.md#rule-d-023)**).

---

## 13. Modules

The cloud modular monolith is partitioned into modules, each owning an application/domain boundary, its own schema or explicit table ownership, a public module API and events, independent tests, and a prohibition on other modules writing its tables:

**Identity & Workspace · Devices & Sessions · Entitlement & Commerce · Chat & Conversation · Task & Execution · Agent & Provider · Sync & Conflict · Resource & Storage Metadata · Search & Knowledge Index · Notification · Policy Control Plane · Audit · Support & Operations · Trust & Safety · Scope Simulation**

Scope Simulation owns the durable simulator state and manifests required by [SIM-01](arcscope.md#rule-sim-01)–[SIM-20](arcscope.md#rule-sim-20); it is an internal module, not another service.

Architecture boundaries must be reconciled to [P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006) in [`../../architecture/05-cloud-architecture.md`](../../architecture/05-cloud-architecture.md).

---

## 14. Acceptance scenarios

**Topology** — the API is unreachable directly from the public internet; the edge is the only path; a single connector instance failure does not cause an outage.

**Scaling** — the production API never scales to zero; at least two replicas serve at all times; autoscale respects its cap.

**Migration** — a rolling deployment with an expand/contract migration succeeds with mixed application versions live; no replica attempts migration at startup.

**Deployment** — the same image digest built once is promoted through staging to production; rollback is one action and restores service.

**Realtime** — realtime is disabled entirely; clients continue by querying authoritative state; reconnection backfills the sequence gap exactly.

**Broker** — a consumer receives a message five times and produces one effect; a poisoned message lands in the dead-letter queue, is inspectable and is replayable.

**Storage** — the primary object store is unavailable; uploads fail cleanly with a specific reason and no partial commit; a cross-provider restore recovers a blob.

**Database** — a failover occurs and the service recovers; a point-in-time restore is proven to a specific timestamp.

**Email** — the primary provider fails, the secondary delivers, and the user receives exactly one one-time code.

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
| **[D-008](../../decisions/phase-1-foundation-decisions.md#rule-d-008)** | Cloud is an ASP.NET Core **Native AOT** modular monolith; no strict AOT requirement |
| **[D-010](../../decisions/phase-1-foundation-decisions.md#rule-d-010)** | Cloud never touches local IPC; durable `ToolRequest` / `ToolResult` model |
| **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)** | Surface inventory including the private operator surface |
| **[V-03](../../assurance/phase-1-official-verification.md#rule-v-03)**, **[V-05e](../../assurance/phase-1-official-verification.md#rule-v-05e)** | The AOT evidence that made the Native AOT decision structural, and the instruction not to spend effort proving Azure SDK AOT compatibility |
