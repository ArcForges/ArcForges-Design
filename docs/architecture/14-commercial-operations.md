# 14 — Commercial operations

Decisions: [AD-0009](../decisions/AD-0009-cloud-relay-and-cost-controls.md) (cost controls), [AD-0010](../decisions/AD-0010-commerce-and-entitlements.md) (commerce). Requirements: R-COM-001..004, R-OPS-001..006, R-CLOUD-006.

## 1. Operating model

| Role | Who | Tools |
|---|---|---|
| Product owner | The user (human) | Decides prices, plans, legal texts, store listings and support targets. Holds provider accounts and signing custody. |
| Operator | The product owner or a delegate with an operator account | Operations profile (`ArcForges.Web.Operations`, Blazor WebAssembly on its own origin), backed by the existing `arcforges.operator.v1.OperatorService` contract |
| Automation | C# jobs in the Cloud host | Webhook processing, acknowledgement, dunning notices, budget checks, retention purges, alerting |

- **Contract.** `OperatorService` already defines the operator surface (Contracts internal, main `b774c322`): cases, consented diagnostic access, configuration staging, approval and activation, kill switches, break-glass, two-person actions, entitlement grant and revoke, compensation and refund decisions.
- **New work.** The Cloud implementation and the Operations profile pages are new. They are adapted to the flagship surfaces in [experience/web.md](../experience/web.md) (operations section).
- **Audit.** Every operator action is audited. Destructive or monetary actions (refund, revoke, break-glass, activating a configuration revision) need a second operator's approval when a second operator exists. A single-operator deployment records a self-approval with justification, and the audit trail marks it.

## 2. Plan catalogue (data)

Plans live in the Entitlement module's configuration revision ([AD-0010](../decisions/AD-0010-commerce-and-entitlements.md) §1). Launch configuration:

| Plan | Features | Limits | Offers |
|---|---|---|---|
| `free` | — | Relay nodes 0, viewers 0, push 0, support uploads 1/day | — |
| `pro` | `remote.view`, `remote.control`, `push` | [10](10-cloud.md) §5 Pro column | Paddle `pro_monthly`, `pro_annual`; Play product `arcforges.pro` with base plans `monthly` and `annual` |

- **Only cloud features are plan features.** Local and LAN capabilities are free and never appear in a plan ([AD-0015](../decisions/AD-0015-direction-editions-roadmap.md) §2).
- **Prices, currencies, trials and introductory offers** are product-owner decisions (human prerequisite H-07). The catalogue supports them without code changes: Paddle prices and Play base-plan offers are referenced by ID.
- **Default before the decision:** no trial, and the paid plans are disabled (configuration flag `commerce.sales_open=false`). The checkout surfaces show "Coming soon" while the flag is off.
- **Feature changes.** Changing a plan's features creates a new configuration revision. Existing subscriptions keep the features of their plan ID, and nodes receive updated entitlement tokens within 24 h, or immediately when online through the relay `EntitlementChanged` frame.

## 3. Subscription lifecycle → entitlement

### 3.1 Paddle (web)

| Paddle subscription status / event | Entitlement | User-visible state |
|---|---|---|
| `active` | Granted | Active, renews on date |
| `trialing` (only if trials are enabled) | Granted | Trial ends on date |
| `past_due` (payment failed; Paddle dunning retries) | Granted during Paddle's retry window | **Payment failed.** Update the payment method (link to the Paddle-hosted page) |
| `paused` | Not granted | Paused, resumes on date |
| `canceled` (scheduled at period end) | Granted until period end | Ends on date |
| `canceled` (effective) | Removed | Ended |
| Refund (`adjustment` with refund action, full) | Removed immediately | Refunded |
| Chargeback | Removed, account flagged for review | Payment disputed: contact support |

### 3.2 Google Play (Android)

| `subscriptionsv2` state / RTDN | Entitlement | User-visible state |
|---|---|---|
| `SUBSCRIPTION_STATE_ACTIVE` | Granted (after acknowledgement succeeds or is queued) | Active |
| `SUBSCRIPTION_STATE_IN_GRACE_PERIOD` | Granted | **Payment issue.** Fix it in Google Play (deep link to the Play subscription center) |
| `SUBSCRIPTION_STATE_ON_HOLD` | Removed | On hold: fix payment in Google Play |
| `SUBSCRIPTION_STATE_PAUSED` | Removed | Paused until date |
| `SUBSCRIPTION_STATE_CANCELED` | Granted until `expiryTime` | Ends on date |
| `SUBSCRIPTION_STATE_EXPIRED` | Removed | Ended |
| `SUBSCRIPTION_STATE_PENDING` | Not granted | Pending payment |
| `SUBSCRIPTION_STATE_PENDING_PURCHASE_CANCELED` | Not granted | Purchase cancelled |
| Revoked (RTDN `SUBSCRIPTION_REVOKED`) or voided purchase | Removed immediately | Refunded or revoked |

### 3.3 Both sources

- **Effective entitlement.** The entitlement snapshot is the union of the active sources.
- **Duplicate subscriptions.** With both a web and a Play subscription active, the Account and Android subscription pages show a duplicate-subscription warning with instructions for cancelling one. The operator can issue a prorated refund through `DecideRefund`.
- **Account deletion with an active subscription.**
  - **Web:** deletion cancels the Paddle subscription immediately, with no refund unless policy says otherwise.
  - **Play:** the flow tells the user that Play subscriptions must be cancelled in Google Play, links there, and blocks deletion until the user confirms it understands.

## 4. Customer communication

| Event | Channel | Content |
|---|---|---|
| Purchase confirmed | Paddle receipt e-mail (MoR) or Google Play receipt | Provider-owned |
| Payment failed, grace, hold | In-app banner (Desktop status bar, web, Android); Paddle dunning e-mails | Fix-payment link |
| Entitlement ended | In-app banner; nodes show which features stopped for new work | Running local work is unaffected (R-COM-004) |
| Node revoked, new device sign-in | Account security e-mail through the Identity e-mail adapter (AF-ID-01, AF-ID-02) | Device and time |
| Incident affecting cloud features | Status page (`status.arcforges.com`, static R2 page updated by the operator) | Affected features; local work unaffected |

The product sends no marketing e-mail. Transactional e-mail goes through the Identity e-mail adapter (Postmark, with Amazon SES as fallback; [10](10-cloud.md) §2). Its live delivery is deferred validation (acceptance register AR-14).

## 5. Support

| Item | Design |
|---|---|
| Intake | Web Support page and Desktop **Help → Contact support** create cases through the reused `SupportService`. The Desktop can attach a support bundle ([11](11-security-privacy.md) §5): the user reviews the files, then consents to the upload. |
| Targets | Free: community (documentation, public issue tracker). Pro: first response in 2 business days (product-owner decision H-08 confirms or changes it). |
| Operator access | Reading a bundle requires `RequestAccess` → user approval (`ApproveAccess`, scoped and time-limited) → `ReadDiagnostic`. Every read is audited. |
| Refunds and compensation | Paddle refunds through the Paddle API (the operator decides through `DecideRefund`). Play refunds are issued in Google Play Console by the product owner and arrive as `SUBSCRIPTION_REVOKED` or voided-purchase notifications. Goodwill extensions use `IssueCompensation` (an entitlement grant with an expiry). |
| Abuse | Rate and anomaly flags (§6) open trust-and-safety proposals (`ProposeEnforcement`), decided by an operator (web W-65), with appeals (`GetAppeal` / `ResolveAppeal`). The TrustSafety contracts and D1 schema are reused; the implementation is new (AF-OPS-01). |

## 6. Abuse prevention and limits (R-OPS-002)

| Surface | Limit (default; configuration) | Anomaly flag |
|---|---|---|
| Sign-in (Identity, AF-ID-01) | Rate limits per IP and per account | Repeated failures from one IP or against one account |
| Node sign-in flows and device codes | 10 flows per account per hour; 5 code-entry attempts per user code | More than 3 denied flows in an hour |
| Phone pairings | 10 per account per hour; single-use secrets | Repeated wrong secrets |
| Node enrollment | Plan node limit; 20 enrollments per account per day | Enrollment churn above 5 revoke-and-re-enroll cycles per day |
| Relay connections | Token-carried limits ([10](10-cloud.md) §5) | Sustained frames above 80% of limit for 1 h |
| Remote commands | 120 per hour (Pro) | More than 20 high-risk commands per hour |
| Push | 50 per account per day | — |
| Support | Free: 1 bundle upload per day; Pro: 5 per day; 10 cases per account per day | Bundle size near the cap repeatedly |

An exceeded limit returns `RESOURCE` with `retry_after` and never silently drops work. Anomaly flags are recorded as audit events of type `anomaly.<kind>` for operator review (web W-65). They never automatically lock an account.

## 7. Cost model and controls (R-CLOUD-006)

Cloudflare has no hard spending cap (V-C04), and subscription gating limits who uses the service, not how much it costs. Spending is therefore bounded by three things together: metering of every billable dimension, structural limits configured in the deployment, and a degradation ladder that stops new **and ongoing** billable activity. Whatever the ladder cannot stop is stated as residual exposure.

### 7.1 Billing dimensions and metering

Every billable dimension of the products in use (V-C02, V-C08) maps to an operating dimension (`OperatingDimension`, [cloud-store](../data/cloud-store.md) §3):

| Product | Billable dimension | Operating dimension | Metered how | Structural bound |
|---|---|---|---|---|
| Containers (C# host) | Provisioned memory (GiB-s) and disk (GB-s) **for as long as an instance runs**, 10 ms granularity | `CONTAINER_INSTANCE_SECONDS` | Measured: the host records each instance's run interval (start to sleep) and the instance type | `max_instances` and `instance_type` in `wrangler.json`, and the idle `sleepAfter`. Worst case per day = `max_instances × 86,400 s × (memory + disk + vCPU rates of the instance type)`. |
| Containers | CPU (vCPU-s), active only | `CONTAINER_CPU_SECONDS` | Measured: the host's process CPU time | Bounded by the worst case above |
| Containers | The container's own Durable Object: requests, and duration while the instance runs (V-C08) | `DO_REQUESTS`, `DO_DURATION_GB_SECONDS` | **Estimated** from the instance run intervals and the requests routed to the container | As the container worst case |
| Containers | Egress | `EGRESS_BYTES` | Measured: the host's outbound handler counts bytes (FCM, Paddle, Play, e-mail provider) | Allow-listed destinations only |
| Workers | Requests and CPU time | `WORKER_REQUESTS` | Measured: request counters batched from the Worker to the host | `limits.cpu_ms` per request; edge rate limits. Requests rejected by edge rules never invoke the Worker. |
| Durable Objects | Requests, including WebSocket opens, incoming messages at 20:1, and alarms | `DO_REQUESTS` | Measured: counters in `FleetHub`, batched to the host | Per-token frame limits, viewer and node limits, the wake guard |
| Durable Objects | Duration: 128 MB × wall time while active and not eligible to hibernate | `DO_DURATION_GB_SECONDS` | **Estimated**: `FleetHub` measures each awake interval (first event to last handler completion) and multiplies by 0.125 GB. Reconciled daily (§7.5). | Hibernation API only (no non-hibernating `accept()`); the alarm-loop guard |
| Durable Objects | SQLite rows written, storage | `DO_ROWS_WRITTEN` | Measured: counted by `FleetHub` | Fixed key layout (10 §4) |
| D1 | Rows read and written, storage | `D1_ROWS_READ`, `D1_ROWS_WRITTEN` | Measured: per-query row counts returned by D1 | Indexed queries only; retention purges |
| R2 | Class A and class B operations, storage (egress free) | `R2_CLASS_A`, `R2_CLASS_B`, `R2_BYTES` | Measured: counted per operation by the host; storage from object sizes | Per-account upload limits; lifecycle rules |
| Queues | Operations | `QUEUE_OPERATIONS` | Measured | One wake message per batch |
| FCM | Free | `PUSH_SENDS` | Measured | Per-account push limits |
| E-mail provider (Postmark, SES) | Messages | `EMAILS_SENT` | Measured by the Identity e-mail adapter | Rate limits on codes and notices |
| Workers Logs | Log events | — (residual) | Not metered | Head sampling 0.1 |

**Unit prices** per dimension are configuration data (`ops.unit_prices`), maintained by the operator from the providers' price lists. They feed the monthly report and the residual-exposure figure.

### 7.2 Budgets and thresholds

- **Daily operating budgets.** One budget per dimension and UTC day in `platform_operating_budget`. Every metered operation reserves against its dimension (`platform_operating_reservation`); estimated dimensions are recorded after the fact.
- **80%:** an operator alert.
- **100%:** the degradation ladder (§7.3) applies the step for that dimension. **120%** of any dimension, or the container worst case being reached, enters essential-only mode.
- **`EMAILS_SENT`** has no ladder step: the product sends only sign-in codes and account security notices, which stay available. It alerts at 80% and 100%, its rate limits bound it (§7.4), and it is excluded from the 120% rule because essential-only mode would not reduce it.
- **The job runner** (cron) runs only essential jobs in essential-only mode: Play purchase acknowledgements, webhook inbox processing and account-deletion purges. Retention sweeps, reports and reconciliation pause until the mode ends.
- **Never affected:** local execution and LAN features. LAN features keep working on cached entitlement tokens.

### 7.3 Degradation ladder (what actually stops spending)

| Step | Triggered by | What stops | What keeps costing |
|---|---|---|---|
| 1. Live streaming off | `DO_REQUESTS`, `DO_DURATION_GB_SECONDS`, `DO_ROWS_WRITTEN` | Delta frames and the DO wakes they cause; viewers get summaries only | Summary frames (at most 1 per minute per node) |
| 2. Relay closed | Step 1 persisting for 15 min, or `DO_*` at 110% | **Existing** relay sockets are closed (close code 4429 `budget`) and new ones refused. Nodes back off 15 min with jitter; viewers show "Live view paused". | Nodes' daily entitlement refresh |
| 3. Push batched, then off | `PUSH_SENDS`, `EGRESS_BYTES` | Push is batched hourly; at 120% it stops | — |
| 4. Uploads refused | `R2_*` | Support uploads | Storage of existing bundles until lifecycle expiry |
| 5. Essential-only mode (`cloud.essential_only`) | 120% of any dimension; `CONTAINER_*`, `WORKER_REQUESTS`, `D1_*` or `QUEUE_OPERATIONS` at 100% | Every route except sign-in, entitlement refresh, payment webhooks and operator calls is answered by the Worker with `RESOURCE/kill_switch_active` **without waking the container**. With essential traffic idle, instances sleep after `sleepAfter`. | The residual exposure (§7.4) |

Each step is a kill switch in configuration, applied automatically by the budget service and reversible by an operator. Steps take effect within one token lifetime (15 min), and step 2 at once for connected sockets.

### 7.4 Residual exposure

Essential-only mode cannot stop:
- **essential requests** (sign-in, entitlement refresh, payment webhooks, operator calls), which are bounded by their rate limits;
- **container run time** for those requests, at most the structural worst case;
- **storage at rest** (D1, R2, Durable Object storage), bounded by retention;
- **Workers Logs** events, bounded by head sampling;
- **unauthenticated internet traffic** that passes the edge rules, bounded by edge rate limiting and Cloudflare's network-level DDoS protection;
- **Worker requests** answered or refused in essential-only mode: refusing a request still bills it as a Worker request; they are bounded by the edge rate limits (`ResidualExposure.worker_requests_micros`).

`OperatorReadService.GetOperatingBudgets` returns `residual`: the container bound, storage at rest, essential requests and Worker requests at their rate limits, priced with `ops.unit_prices`, as a **daily worst case**. W-66 shows it.

**Monthly ceiling (product-owner input H-09).** The operator sets the daily budgets so that `31 × (Σ daily budgets + residual daily worst case) ≤ monthly ceiling`. Cloudflare budget alerts at 50%, 80% and 100% of the ceiling are a second, notification-only signal (V-C04).

### 7.5 Reconciliation

A daily job compares the metered values with the providers' billing data. For Cloudflare this uses the GraphQL Analytics API with a read-only token (optional prerequisite H-21). The job raises an operator alert when a dimension diverges by more than 20%, and recalibrates the estimated dimension (`DO_DURATION_GB_SECONDS`). Reconciliation is a check, never enforcement. Without the token, the job reports that reconciliation is off. `GetOperatingBudgets.reconciliation` carries the state (`OFF`, `OK`, `DIVERGED`), the last run and the diverging dimensions.

**Unit economics check.** The monthly operator report (`OperatorReadService.GetMonthlyReport`, computed on demand from budget use, unit prices and subscriptions) shows the cost per active Pro account, the cost per relay-connected node and the Free-tier cost. It is an input to price decisions.

## 8. Service operations (R-OPS-006)

| Item | Design |
|---|---|
| Health | `GET /healthz` (liveness) and `/readyz` (D1 reachable, configuration loaded, key material present) on the C# host. Relay Worker `GET /v1/health`. |
| Logs | Structured JSON with correlation IDs (reused observability). Personal data minimised. Command lines and outputs are never logged (R-OPS-003). |
| Metrics | [10](10-cloud.md) §7, plus commerce: webhook backlog, acknowledgement-pending count and age, entitlement-token issuance failures |
| Alerts | Acknowledgement pending > 12 h; webhook verification failures > 5/min; budget 80%; relay error rate > 2%; container ready failures; certificate-issuance errors; signing-key expiry < 30 days |
| Deploys | Main-push deployments through each repository's guarded scripts only (existing practice). No previews; `workers.dev` disabled. |
| Backups | D1 Time Travel (point-in-time restore within the retention window) and a weekly export of commerce and registry tables to R2 (encrypted, 90 days). |
| Incident runbooks | One per alert class, kept in the Cloud repository `docs/runbooks/`: relay degraded, container unavailable, D1 overloaded, webhook failures, Play acknowledgement backlog, key rotation, kill-switch activation, data-deletion request, security incident. Each states symptoms, checks, actions, the kill switches allowed and the user communication. |

## 9. Legal and compliance (human prerequisites)

| Item | Owner | Status in design |
|---|---|---|
| Terms of service, privacy policy, refund policy, subprocessor list | Product owner (legal review) | Pages are specified ([experience/web.md](../experience/web.md)); text is supplied by the owner (H-10) |
| Paddle seller account and product setup (MoR handles tax) | Product owner | H-01 |
| Google Play developer account, merchant profile, app listing, data-safety form | Product owner | H-02 |
| Firebase project and FCM service account | Product owner | H-03 |
| Code-signing certificate (Authenticode), ES256 release manifest key, apt GPG key, Android upload key | Product owner (custody) | H-04 |
| Domains (`arcforges.com`, `releases.`, `relay.`, `status.`), DNS | Product owner | H-05 |
| Cloudflare account settings: Containers enabled, budget alerts | Product owner | H-06 |

The H-numbered list with exact steps is in the Plan's `acceptance-register.md` (human prerequisites section).
