# Observability and Operations Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: [Cloud requirements](../requirements/products/arcforges-cloud.md) (infrastructure and telemetry), [support requirements](../requirements/10-distribution-update-and-support.md) (incidents and operations), **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** (surface inventory, including the status and notification domains)
> Companions: [`../requirements/products/arcforges-cloud.md`](../requirements/products/arcforges-cloud.md), [`../requirements/10-distribution-update-and-support.md`](../requirements/10-distribution-update-and-support.md), [`05-cloud-architecture.md`](05-cloud-architecture.md), [`08-security-architecture.md`](08-security-architecture.md)

Observability answers *why is the system slow or failing*. It is a separate system, with separate retention and separate access control, from the audit log, which answers *who changed what security or business state, and when*. Conflating the two is the failure this architecture is designed to prevent.

---

## 1. Controlling rules

| # | Rule |
|---|---|
| OA-01 | **OpenTelemetry is the instrumentation standard** for logs, metrics and traces, from the first release ([OB-01](../requirements/products/arcforges-cloud.md#rule-ob-01) in the cloud requirements). |
| <a id="rule-oa-02"></a>OA-02 | **Business code never references a vendor logging type.** It uses the standard abstractions and OpenTelemetry semantics, so the backend can change without touching instrumentation. |
| OA-03 | **The application owns its own instrumentation.** A platform-managed collector agent is a convenience, never an architectural prerequisite ([OB-02](../requirements/products/arcforges-cloud.md#rule-ob-02) there). |
| OA-04 | **Platform-native signals are retained as a secondary channel**, so a failure of the observability vendor does not blind operations ([OB-03](../requirements/products/arcforges-cloud.md#rule-ob-03) there). |
| OA-05 | **Observability is never a user-content database** ([I-273](../requirements/01-normative-glossary-and-invariants.md#rule-i-273), [OB-05](../requirements/products/arcforges-cloud.md#rule-ob-05) there). |
| <a id="rule-oa-06"></a>OA-06 | **Audit and observability are completely separate systems** ([I-272](../requirements/01-normative-glossary-and-invariants.md#rule-i-272), [OB-06](../requirements/products/arcforges-cloud.md#rule-ob-06) there), with separate storage, retention, access control and export paths. |
| OA-07 | **Desktop telemetry is stricter than cloud telemetry** ([OB-07](../requirements/products/arcforges-cloud.md#rule-ob-07) there): minimal, opt-in, and never carrying user content. |
| OA-08 | **Telemetry is a cost centre with a budget.** Cardinality, sampling and retention are designed, measured and reviewed, not discovered from an invoice. |

---

## 2. Signal architecture

### 2.1 The three signal classes and what each is for

| Signal | Purpose | Retention posture | Cardinality posture |
|---|---|---|---|
| **Metrics** | Rates, saturation, latency distributions, queue depth, error ratios — the basis of SLI computation and alerting | Longest; aggregated | Strictly bounded label sets; no unbounded identifier as a label |
| **Traces** | Causal path of one request or task across services, queues and providers | Short; sampled | High-cardinality attributes permitted on spans, not on metrics |
| **Logs** | Structured events with context, for diagnosis of a specific occurrence | Short to medium | Structured fields only; no free-text dumps of payloads |

| # | Rule |
|---|---|
| SG-01 | **A structured log event is a typed record, not an interpolated sentence.** Fields are named and stable so they can be queried. |
| <a id="rule-sg-02"></a>SG-02 | **An identifier that can grow without bound is never a metric label** — no workspace id, actor id, task id, resource id or provider request id on a metric. Those live on spans and log records. |
| SG-03 | **Trace sampling is head-based with tail retention for errors and slow requests**: an error path or a request exceeding its latency objective is retained even when the sample rate would have dropped it. |
| SG-04 | **A task, sync operation or automation run is traceable end to end**, including across queue hops and provider calls (`§3`). |
| SG-05 | **Every signal carries the build identifier and instance identity**, so a regression can be attributed to a release. |

### 2.2 Required dimensions

Every emitted signal carries the applicable subset of ([OB-08](../requirements/products/arcforges-cloud.md#rule-ob-08) there):

```
application id · instance id · build id · environment
de-identified actor reference · workspace reference
transport · service · interface · method · capability
redacted resource id · command id · task id · run id · attempt id
correlation id · causation id
expected revision · result revision
duration · queue time · result code · reason code
native ABI version and build (where applicable)
reconnect count · sequence-gap count
```

| # | Rule |
|---|---|
| DM-01 | **"Bring whatever is there"**: a dimension that exists in the current context is always attached; a dimension that does not exist is omitted, never faked or defaulted. |
| DM-02 | **An actor is referenced by a stable de-identified reference**, not by email address or display name. |
| DM-03 | **A resource is referenced by identifier, never by name or path** (`§4`). |
| <a id="rule-dm-04"></a>DM-04 | **Reason codes in telemetry are the same enumerated reason codes the product uses** (`§16` of the security requirements), so a support conversation, a user-visible message and a trace all name the same cause. |

---

## 3. Correlation

```
User action (desktop / web / mobile)
   └── correlation id created at the originating edge, or accepted from the client
        ↓ HTTP
      Cloud API request            request id, correlation id, causation id
        ↓ enqueue
      Message                      correlation propagated in message metadata
        ↓ dequeue
      Worker / task runner         new span, same correlation, causation = enqueue span
        ↓ outbound
      AI provider / payment provider / email provider
                                   provider request id captured and attached
```

| # | Rule |
|---|---|
| <a id="rule-cr-01"></a>CR-01 | **One correlation identity spans the whole causal chain** across API, queue, worker, task runner, realtime and outbound provider calls ([OB-04](../requirements/products/arcforges-cloud.md#rule-ob-04) there). |
| CR-02 | **Causation is recorded as well as correlation**: which specific operation caused this one, so a fan-out can be reconstructed rather than flattened. |
| CR-03 | **A client-supplied correlation id is accepted but never trusted for authorization** and is length- and format-validated before use. |
| <a id="rule-cr-04"></a>CR-04 | **A user-visible task or run identifier resolves to its trace.** When a user reports "task 7PM3 failed", an operator reaches the API request, queue hop, worker attempt and provider call without guesswork. |
| CR-05 | **A provider request identifier is captured for every outbound provider call**, so a provider-side investigation is possible. |
| <a id="rule-cr-06"></a>CR-06 | **Correlation propagation is implemented once**, in the shared telemetry infrastructure, not per module. |
| CR-07 | **Realtime connections carry correlation** for connect, negotiate, subscribe and message-delivery events, including reconnection and sequence-gap events. |

---

## 4. Redaction architecture

Redaction is enforced by construction, not by reviewer diligence.

| # | Rule |
|---|---|
| <a id="rule-rd-01"></a>RD-01 | **Prohibited from telemetry by default**: authorization headers, cookies, passkey material, one-time codes, API keys, BYOK secrets, prompt content, model response content, note and document content, file contents, file paths, and raw sync payloads. |
| RD-02 | **The permitted substitute for a payload is its shape**: object identifier, size, duration, status, item count, and a hash prefix where a hash genuinely aids diagnosis. |
| <a id="rule-rd-03"></a>RD-03 | **A secret-bearing type cannot be logged.** `SecretRef` and equivalent types have a formatting implementation that emits only a reference, and the underlying value has no accessible string representation (`§6` of the security architecture). |
| <a id="rule-rd-04"></a>RD-04 | **A domain content type has no logging representation.** Message bodies, note blocks, capture buffers and media frames are not loggable objects. |
| RD-05 | **A scrubbing processor runs in the telemetry pipeline as a second line of defence**, removing known-sensitive header and field names before export. It is a safety net, never the primary control. |
| <a id="rule-rd-06"></a>RD-06 | **A test asserts redaction**: a suite exercises representative error and success paths and fails if a known-sensitive marker value appears anywhere in the exported signal (`§9`). |
| RD-07 | **An exception message is not assumed safe.** Exception messages that can embed user input are mapped to reason codes before export. |
| RD-08 | **URLs are recorded as route templates plus identifiers**, never as raw URLs that may contain a resource name or token in a query string (`§6` of the security architecture — no sensitive data in URLs). |

---

## 5. Audit architecture

Audit is a **product security record**, not a diagnostic aid.

| # | Rule |
|---|---|
| <a id="rule-au-01"></a>AU-01 | **Audit is append-only.** No update, no delete, no operator edit (`§13` of the security architecture). |
| AU-02 | **Audit retention is governed by policy and does not expire with the observability retention window**. |
| AU-03 | **Audit events are enumerated, not incidental**: device revoked, passkey added or removed, session revoked, step-up performed, administrative grant, entitlement change, refund, secret created, rotated or deleted, remote action approved, break-glass access, enforcement action, export requested, deletion requested. |
| AU-04 | **Every audit event records the full actor chain** — human principal, device, installation, session, and any agent acting on the principal's behalf (`§2` of the security architecture). |
| AU-05 | **An audit record is visible to the account owner** for events affecting their account, in the account portal and the security centre. |
| <a id="rule-au-06"></a>AU-06 | **Audit access by an operator is itself audited** (`§15` of the distribution requirements). |
| AU-07 | **Audit and observability are never joined in a query surface** that would let a diagnostic search read security history, or the reverse. Correlation between them is by identifier, deliberately. |

---

## 6. Health and service levels

### 6.1 Health

| # | Rule |
|---|---|
| HE-01 | **Health is reported per capability, not per process** ([SL-01](../requirements/products/arcforges-cloud.md#rule-sl-01) there). "The process is alive" is not health. |
| HE-02 | **Three probe kinds exist**: liveness (should this instance be restarted), readiness (should this instance receive traffic), and capability health (can this capability actually serve a request). |
| HE-03 | **A readiness probe checks the dependencies the instance needs to serve**, and fails closed when a required dependency is unavailable. |
| HE-04 | **Capability health is what feeds the status page and degradation decisions** (`§13` of the cloud architecture). |
| HE-05 | **The five health dimensions of the contract model** — reachable, ready, healthy, degraded, capacity — are the vocabulary used consistently across local IPC, cloud capability health and status reporting (`§9` of the contract architecture). |

### 6.2 SLI and SLO

| # | Rule |
|---|---|
| SL-01 | **An SLI measures user-visible success**, not infrastructure liveness: successful user requests, latency, sync completion, task execution, realtime negotiation, and one-time-code delivery. |
| <a id="rule-sl-02"></a>SL-02 | **SLOs are internal engineering objectives.** **SLO ≠ external SLA** ([I-403](../requirements/01-normative-glossary-and-invariants.md#rule-i-403)); publishing an external commitment is a separate, deliberate decision backed by demonstrated performance. |
| SL-03 | **Objectives are set per capability group** — core cloud API, identity, sync control plane — with realtime and managed AI computed independently. |
| SL-04 | **A dependency outage outside ArcForges' control is attributed to that dependency's objective**, so a provider outage does not make the whole platform read as down. |
| SL-05 | **Error budget consumption is visible** and is the input to release-pace decisions, not a report produced after the fact. |
| SL-06 | **Objective definitions live in configuration reviewed like code**, with a change history. |

---

## 7. Alerting and incident architecture

| # | Rule |
|---|---|
| AL-01 | **Alerts are symptom-based.** A single unexpected exception is a defect signal, not a page. |
| <a id="rule-al-02"></a>AL-02 | **Page-worthy conditions are enumerated**: external API unavailable, server-error rate spike, database unavailable, oldest-message age critical, dead-letter growth, one-time-code delivery failure spike, remote connection collapse, backup lag beyond objective, **payment provider webhook backlog**, all managed AI routes unavailable, and a data-integrity alarm. |
| <a id="rule-al-03"></a>AL-03 | **Every alert names its runbook.** An alert without a runbook is not deployed. |
| AL-04 | **Alert routing distinguishes page, ticket and dashboard**, and the distinction is part of the alert definition. |
| AL-05 | **Alert definitions are version-controlled and deployed with the same review as code.** |
| AL-06 | **Severity is fixed and shared** across engineering, support and communication: **SEV0** security or potential data loss; **SEV1** major paid cloud outage; **SEV2** critical functionality degraded; **SEV3** limited impact ([SL-04](../requirements/products/arcforges-cloud.md#rule-sl-04) there). |
| AL-07 | **A possible personal-data breach is automatically SEV0**, with the statutory notification clock treated as a hard deadline ([SL-05](../requirements/products/arcforges-cloud.md#rule-sl-05) there). |
| AL-08 | **Incident state is tracked in a system independent of the production platform**, so an outage does not disable incident management. |

---

## 8. Status page architecture

| # | Rule |
|---|---|
| ST-01 | **The status page is hosted independently of ArcForges Cloud**. A status page rendered by the API is worthless when the API is down. |
| ST-02 | **An emergency alternate status URL is published** in the repository README, support documentation and public profiles, so a DNS or edge failure affecting the primary hostname does not remove the only status channel. |
| ST-03 | **Components are user-facing capabilities, not internal vendors**: website; account and authentication; cloud API; sync and storage; remote and realtime; cloud tasks and automation; managed AI; billing and checkout; downloads and updates. |
| ST-04 | **Internal vendor and region names are never published as status components.** |
| ST-05 | **Capability health drives status**, and the mapping from internal capability health to published component state is explicit and reviewed. |
| ST-06 | **A degraded capability is reported as degraded**, with what still works stated — not as a binary up or down (`§13` of the cloud architecture). |
| ST-07 | **In-product degradation messaging and the status page agree.** A user seeing "sync unavailable" in the product must find the same statement on the status page. |

---

## 9. Desktop and client diagnostics

| # | Rule |
|---|---|
| DG-01 | **Desktop analytics are minimal and opt-in** ([OB-07](../requirements/products/arcforges-cloud.md#rule-ob-07) there, [PV-06](../requirements/07-security-privacy-and-trust.md#rule-pv-06) in the security requirements). A product whose native surfaces run without telemetry obligations does not report on the user by default. |
| DG-02 | **Local diagnostics are always available to the user without any upload.** A local log and a local diagnostic view exist regardless of telemetry consent. |
| DG-03 | **A crash or diagnostic report is generated, shown to the user, and uploaded only after approval**. The flow is: generate → show exactly what will be sent → user approves → send. |
| DG-04 | **A full memory dump is never uploaded by default**, because it may contain document content and secrets. |
| DG-05 | **Diagnostic tiers are explicit** (`§17` of the quality contract): a minimal always-on local tier, a user-approved report tier, and a temporary verbose tier enabled by the user for a bounded period. |
| DG-06 | **A verbose diagnostic session is time-bounded and self-disabling**, and its state is visible while active. |
| DG-07 | **A diagnostic report carries a support reference identifier**, so a user can quote it in a support case without attaching data (`§7.1` of the distribution requirements). |
| DG-08 | **Client telemetry consent is revocable**, and revocation stops collection immediately and locally. |

---

## 10. Operator surface architecture

| # | Rule |
|---|---|
| OP-01 | **The operator surface is a separate origin with a separate identity system** (**[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)**; `§10`, `§16` of the distribution requirements), never reachable from public navigation. |
| OP-02 | **An operator never silently becomes a user**. Support access is explicit, consented where required, time-bounded, scoped and audited. |
| OP-03 | **Break-glass access is a distinct, alarmed path** with mandatory justification, automatic expiry, and post-hoc review (`§9` there). |
| <a id="rule-op-04"></a>OP-04 | **Operator actions are audited to the audit system, not to observability** ([AU-06](#rule-au-06)). |
| OP-05 | **The operator surface reads through the same authorization model as the product**, with operator scopes as an additional constraint — never through a privileged path that bypasses tenancy isolation (`§11` of the cloud architecture). |
| OP-06 | **A destructive operator action requires a second authorised operator** where it affects customer data or entitlement. |
| OP-07 | **Operator tooling is built from the same contracts** as the product; there is no parallel, unversioned admin API. |

---

## 11. Operational dependency adapters

| # | Rule |
|---|---|
| OD-01 | **Every external operational provider sits behind an adapter interface** — transactional email, observability export, incident notification, status publication. A provider call is never scattered through business code. |
| OD-02 | **Transactional and broadcast email are separated by stream and by sending subdomain**, so marketing reputation can never affect delivery of one-time codes and security alerts. |
| OD-03 | **Security-critical email has a prepared secondary path**, because failure of a single email provider must not lock users out of their accounts. |
| OD-04 | **Email delivery outcome is observable** — accepted, delivered, bounced, complained — and a delivery-failure spike is a page-worthy condition ([AL-02](#rule-al-02)). |
| OD-05 | **Provider selection is configuration, not code**, and switching providers requires no instrumentation change ([OA-02](#rule-oa-02)). |

---

## 12. Runbooks as an architectural artifact

| # | Rule |
|---|---|
| RB-01 | **Every dependency capable of causing a SEV1 has a runbook before go-live** ([SL-06](../requirements/products/arcforges-cloud.md#rule-sl-06) there). |
| RB-02 | **A runbook is executable in an incident**: preconditions, decision points, exact commands or console steps, verification, and rollback. Searching the internet during an incident is a failure of preparation. |
| RB-03 | **The required runbook set is the list in `§9.1` of the cloud product requirements**, and it is a go-live gate. |
| <a id="rule-rb-04"></a>RB-04 | **A runbook is exercised, not merely written.** Restore, failover, replay and rebuild runbooks are executed in drills, and a runbook that has never been executed is marked as unproven. |
| RB-05 | **An incident that required an undocumented action produces a runbook update** as part of its closure. |

---

## 13. Cost and cardinality control

| # | Rule |
|---|---|
| CC-01 | **Metric cardinality is bounded by design** ([SG-02](#rule-sg-02)), and a cardinality budget per service is monitored. |
| CC-02 | **Sampling is configurable per signal and per route** without a code change. |
| CC-03 | **Retention differs by signal class and by environment**, with production and non-production budgeted separately. |
| CC-04 | **Duplicating the full log stream into a second permanent store is not the default**. Platform-native signals are a secondary channel, not a second copy of everything. |
| CC-05 | **Telemetry cost is reported alongside infrastructure cost** (`§10` of the cloud product requirements), so a change in instrumentation is visible economically. |

---

## 14. Verification

| # | Test obligation |
|---|---|
| <a id="rule-tv-01"></a>TV-01 | **Redaction tests**: marker values injected as headers, tokens, prompts and document content must never appear in exported signals ([RD-06](#rule-rd-06)). |
| TV-02 | **Correlation tests**: a synthetic user action produces one connected trace across API, queue, worker and provider stub. |
| TV-03 | **Cardinality tests**: metric label sets are asserted against an allowlist; an unbounded identifier used as a label fails the build. |
| TV-04 | **Audit-separation tests**: an audit event never lands in observability storage, and an observability event never lands in audit storage. |
| TV-05 | **Health-probe tests**: readiness fails closed on each required dependency; capability health reflects a simulated dependency outage. |
| TV-06 | **Alert-definition tests**: every deployed alert resolves to an existing runbook ([AL-03](#rule-al-03)). |
| TV-07 | **Status-mapping tests**: each capability health state maps to the published component state the degradation policy specifies. |
| TV-08 | **Diagnostic-consent tests**: with telemetry consent absent, no client signal leaves the device; a crash report is not sent without approval. |
| TV-09 | **Operator-audit tests**: every operator read and write of customer-scoped data produces an audit record naming the operator, scope and justification. |
| TV-10 | **Drill evidence**: each restore, failover and rebuild runbook has a dated execution record ([RB-04](#rule-rb-04)), and its absence blocks the go-live gate. |

---

## 15. Non-goals

Observability is **not**: a place to store user content; a substitute for the audit log; a product analytics platform for behavioural profiling; a billing source of truth; a debugging channel that bypasses user consent on the desktop; or a reason to add a dimension whose cardinality is unbounded.

---

## 16. Traceability

| Current document | Relationship |
|---|---|
| [ArcForges Cloud — Product and Platform Requirements](../requirements/products/arcforges-cloud.md) | Owns operational signals, region preflight and Cloud readiness |
| [Distribution, Update, Support and Trust & Safety Requirements](../requirements/10-distribution-update-and-support.md) | Owns incidents, support, status and operator access |
| [Security, Permission, Privacy and Trust Requirements](../requirements/07-security-privacy-and-trust.md) | Owns redaction, audit and privacy constraints |
| **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** | The status, notification and operator surfaces as distinct surfaces with distinct policy |
| [I-272](../requirements/01-normative-glossary-and-invariants.md#rule-i-272), [I-273](../requirements/01-normative-glossary-and-invariants.md#rule-i-273), [I-403](../requirements/01-normative-glossary-and-invariants.md#rule-i-403) | Audit ≠ observability; observability ≠ user content; SLO ≠ SLA |
