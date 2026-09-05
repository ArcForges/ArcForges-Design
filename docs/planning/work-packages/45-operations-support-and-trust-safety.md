# WP-45 — Operations, Support and Trust & Safety

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: J — Platform completion
> Upstream: `12`, `21`, `44` · Downstream: `46`

> **Goal.** Make the platform operable: alerting that is worth waking someone for, runbooks that have actually been executed, a status page that survives an outage, support access that never silently impersonates a user, and an enforcement ladder with appeals.

---

## 1. Scope and purpose

**In scope.** Alerting and severity; the incident process; runbook authoring and rehearsal; the independently hosted status page; service-level objectives and their computation; the operator console with its separate identity system; support cases and time-bounded support access; break-glass; community reports and the enforcement ladder; appeals; security advisories; and operational email adapters.

**Out of scope.** Backup and disaster recovery (`46`). Observability instrumentation (`12`).

**Why this package exists.** `I2 §III.11` places operations, support and trust and safety in cloud completion. The cloud go-live threshold is "failure behaves correctly", and that threshold cannot be met without this package.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/13-observability-and-operations.md`](../../architecture/13-observability-and-operations.md) | Alerting, incidents, status, operator surface, runbooks, dependency adapters |
| [`../../requirements/10-distribution-update-and-support.md`](../../requirements/10-distribution-update-and-support.md) Part II | Support, operators, recovery, incidents, enforcement, appeals, advisories |
| [`../../requirements/products/arcforges-cloud.md`](../../requirements/products/arcforges-cloud.md) `§9` | Service levels, incident severity and the required runbook set |
| `WP-12`, `WP-21`, `WP-44` output | Signals, the real cloud and the policy control plane |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Alerts are symptom-based.** A single unexpected exception is a defect signal, not a page. |
| BR-02 | **Every alert names its runbook.** An alert without a runbook is not deployed. |
| BR-03 | **A runbook is executable in an incident** and is exercised, not merely written. |
| BR-04 | **The status page is hosted independently of ArcForges Cloud**, with an emergency alternate URL published. |
| BR-05 | **Status components are user-facing capabilities**, never internal vendors or regions. |
| BR-06 | **An operator never silently becomes a user.** Support access is explicit, consented where required, time-bounded, scoped and audited. |
| BR-07 | **Break-glass is a distinct, alarmed path** with mandatory justification, automatic expiry and post-hoc review. |
| BR-08 | **Operator actions are audited to the audit system**, never only to telemetry. |
| BR-09 | **A possible personal-data breach is automatically the highest severity**, with the statutory notification clock as a hard deadline. |
| BR-10 | **The enforcement ladder is proportionate and appealable**, with every action recorded and communicated. |
| BR-11 | **Security advisories follow a defined disclosure process** coordinated with the expedited update path. |
| BR-12 | **Transactional and broadcast email are separated by stream and sending subdomain**, and security-critical email has a prepared secondary path. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Cloud/ArcForges.Cloud.Modules.Operations/` | Support cases, support access grants, break-glass, enforcement, appeals, advisories |
| `src/Cloud/ArcForges.Cloud.Modules.Notification/` | Transactional and broadcast email adapters with separated streams and a secondary path |
| `src/Web/ArcForges.Web.App/` (operator profile) | The operator console on its own origin and identity system |
| `deploy/monitoring/` | Alert definitions, service-level objective definitions, status component mapping |
| `docs/runbooks/` in the implementation repository | The required runbook set with rehearsal records |
| `tests/CloudIntegrationTests/Operations/` | Alert-to-runbook, support access, break-glass, enforcement and appeal suites |

**Major types introduced.** `AlertDefinition`, `Severity`, `Incident`, `IncidentState`, `Runbook`, `RunbookRehearsal`, `ServiceLevelObjective`, `ServiceLevelIndicator`, `StatusComponent`, `OperatorIdentity`, `OperatorScope`, `SupportCase`, `SupportAccessGrant`, `BreakGlassSession`, `EnforcementAction`, `AppealRequest`, `SecurityAdvisory`.

---

## 5. Required implementation work

### WP-45.00 — Service levels and alerting

**What must be fully done.** Service-level indicators measuring user-visible success, objectives per capability group with realtime and managed AI computed independently, error-budget visibility, and the enumerated page-worthy alert set with routing that distinguishes page, ticket and dashboard.

**Testing requirements.** Indicator correctness against synthetic failures; a dependency-attribution test asserting a provider outage does not read as full platform downtime; an alert-routing test; an alert-to-runbook completeness assertion.

**Completion gate.** Indicators measure user-visible success, a provider outage is attributed correctly, and **every deployed alert names an existing runbook**.

### WP-45.01 — Incident process

**What must be fully done.** The four-severity ladder shared by engineering, support and communication; incident state tracked in a system independent of production; a possible personal-data breach automatically the highest severity with the statutory clock treated as a hard deadline; post-incident review producing runbook updates.

**Testing requirements.** A severity-classification exercise; an independence assertion for the incident system; a breach-classification test.

**Completion gate.** Severity is shared and unambiguous, the incident system survives a production outage, and a possible breach classifies automatically at the highest severity.

### WP-45.02 — Runbooks and rehearsal

**What must be fully done.** Every required runbook written with preconditions, decision points, exact steps, verification and rollback. Each is executed at least once with a dated record. A runbook never executed is marked unproven.

**Testing requirements.** A completeness check against the required set; a dated rehearsal record per runbook.

**Completion gate.** **Every required runbook exists and has a dated rehearsal record** — satisfying `PG-04`.

### WP-45.03 — Status page

**What must be fully done.** An independently hosted status page with user-facing capability components, an emergency alternate URL published in the repository, support documentation and public profiles, and a mapping from internal capability health to published component state that is explicit and reviewed.

**Testing requirements.** A full-cloud-outage test asserting the status page remains available; a mapping test per capability health state; a vendor-name absence check.

**Completion gate.** The status page survives a full cloud outage, publishes only user-facing components, and its emergency alternate URL is published in at least three places.

### WP-45.04 — Operator console and support access

**What must be fully done.** The operator console on a separate origin with a separate identity system, never in public navigation. Support access is explicit, scoped, time-bounded, consented where required and audited. A destructive action affecting customer data or entitlement requires a second authorised operator. Operator tooling uses the same contracts as the product.

**Testing requirements.** A silent-impersonation negative test; scope and expiry tests; a two-operator requirement test; an audit-completeness test; a parallel-admin-API absence assertion.

**Completion gate.** **An operator can never silently become a user**, every access is scoped, expiring and audited, and no parallel unversioned admin API exists.

### WP-45.05 — Break-glass

**What must be fully done.** A distinct, alarmed emergency access path with mandatory justification, automatic expiry, immediate alerting and mandatory post-hoc review. Break-glass use is visible to the account owner where it touched their data.

**Testing requirements.** Activation alerting; expiry enforcement; a review-requirement test; an owner-visibility test.

**Completion gate.** Break-glass alerts immediately, expires automatically, requires review, and is visible to the affected account owner.

### WP-45.06 — Support cases and in-product reporting

**What must be fully done.** In-product problem reporting producing a support reference without attaching data by default; support cases linking to diagnostic references rather than content; the case lifecycle with response expectations.

**Testing requirements.** A no-data-by-default assertion; a reference-resolution test; a lifecycle test.

**Completion gate.** A problem report attaches no user data by default and produces a resolvable support reference.

### WP-45.07 — Trust and safety

**What must be fully done.** Community report intake; the proportionate enforcement ladder with every action recorded and communicated; account enforcement states integrated with the account model; an appeal process with a defined path and response expectation; copyright and public content handling.

**Testing requirements.** Ladder progression tests; a communication-completeness assertion; an appeal path test; an enforcement-audit test.

**Completion gate.** Every enforcement action is proportionate, recorded, communicated and appealable.

### WP-45.08 — Security advisories and email adapters

**What must be fully done.** A defined advisory process coordinated with the expedited update path and the kill-switch mechanism. Transactional and broadcast email separated by stream and sending subdomain, with a prepared secondary path for security-critical mail and delivery outcome observable.

**Testing requirements.** An advisory publication rehearsal; an email failover test asserting no duplicate one-time codes; a stream-separation assertion; a delivery-failure alert test.

**Completion gate.** An advisory can be published and coordinated with an expedited update, and **email failover produces no duplicate one-time codes**.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Support cases, access grants, enforcement actions and advisories |
| Protocol | Operator contracts reuse product contracts |
| UI | Operator console, support surfaces and status page |
| Security | Operator access is a major control surface; break-glass is alarmed |
| Platform | Status and incident systems independent of the platform they monitor |
| Migration | Operations schema versioning |
| Compatibility | Advisory and enforcement communication reaches every client version |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Indicator, attribution, routing and runbook-completeness results | `WP-45.00` |
| Severity, independence and breach-classification results | `WP-45.01` |
| Runbook completeness check and dated rehearsal records | `WP-45.02` |
| Outage-survival, mapping and vendor-absence results | `WP-45.03` |
| Impersonation negative, scope, two-operator and audit results | `WP-45.04` |
| Break-glass alert, expiry, review and visibility results | `WP-45.05` |
| No-data-by-default and reference resolution results | `WP-45.06` |
| Ladder, communication, appeal and audit results | `WP-45.07` |
| Advisory rehearsal and email failover results | `WP-45.08` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Indicators measure user-visible success; a provider outage is attributed correctly; **every deployed alert names an existing runbook**.
2. Severity is shared and unambiguous; the incident system survives a production outage; a possible breach classifies automatically at the highest severity.
3. **Every required runbook exists and has a dated rehearsal record** — satisfying `PG-04`.
4. The status page survives a full cloud outage, publishes only user-facing components, and its emergency alternate URL is published in at least three places.
5. **An operator can never silently become a user**; every support access is scoped, expiring and audited; no parallel unversioned admin API exists.
6. Break-glass alerts immediately, expires automatically, requires post-hoc review, and is visible to the affected account owner.
7. A problem report attaches no user data by default and produces a resolvable support reference.
8. Every enforcement action is proportionate, recorded, communicated and appealable.
9. An advisory can be published and coordinated with an expedited update; **email failover produces no duplicate one-time codes**.

---

## 9. Dependencies

**Upstream.** `12` (signals), `21` (the real cloud), `44` (policy and kill switches).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `46` — Backup and recovery | The incident and runbook framework its drills run inside |
| `50` — Production release | Operational readiness as a go-live gate |
