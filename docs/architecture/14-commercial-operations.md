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
| `pro` | `lan.placement`, `lan.accept`, `lan.cache`, `remote.view`, `remote.control`, `push` | [10](10-cloud.md) §5 Pro column | Paddle `pro_monthly`, `pro_annual`; Play product `arcforges.pro` with base plans `monthly` and `annual` |

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

### 7.1 Cost drivers

| Driver | Unit | Shape | Main control |
|---|---|---|---|
| Container CPU and memory (C# host) | Active seconds × instance | Bursty, proportional to business calls | Sleep when idle; instance type `basic` by default (V-C02); request budgets |
| Durable Object requests and duration | Requests; GB-s while not hibernated | Proportional to frames processed | Hibernation; demand-driven telemetry; at most 1 summary per minute without viewers; alarm-loop guard |
| D1 | Rows read and written | Registry, commands, commerce, audit | Indexed queries only; no telemetry time series in D1 |
| R2 | Storage, class A/B operations, egress free | Releases and support bundles | Bundle retention 30 days; per-account upload limits |
| FCM | Free | — | Per-account push limits |
| Worker requests | Requests | Ingress and relay upgrades | Edge rate limits |

### 7.2 Budgets and kill switches

- **Daily operating budgets.** One budget per dimension and UTC day in `platform_operating_budget` (schema reused; the flagship dimensions are added by AF-PLAT-01, [cloud-store](../data/cloud-store.md) §3): container CPU-seconds, Durable Object requests, D1 rows read, D1 rows written, push sends, R2 class A and class B operations, and R2 bytes (support bundles). Every metered operation reserves against its dimension (`platform_operating_reservation`).
- **Unit prices** per dimension are configuration data (`ops.unit_prices`), maintained by the operator from the Cloudflare price list. They feed the monthly report.
- **Thresholds:**
  - **80%:** an operator alert.
  - **100%:** the kill switches apply in order ([10](10-cloud.md) §5):
    1. live streaming off;
    2. push batched hourly;
    3. new relay connections refused;
    4. support uploads refused.
- **Never affected:** local execution and LAN features. LAN features keep working on cached entitlement tokens.
- **Monthly ceiling (product-owner input H-09).** The operator sets the daily budgets so that 31 × daily ≤ the monthly ceiling. Cloudflare budget alerts are set at 50%, 80% and 100% of the ceiling as a second, notification-only signal (V-C04).
- **Unit economics check.** The monthly operator report (`OperatorReadService.GetMonthlyReport`, computed on demand from budget use, unit prices and subscriptions) shows the cost per active Pro account, the cost per relay-connected node and the Free-tier cost. It is an input to price decisions.

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
