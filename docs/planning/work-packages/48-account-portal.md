<a id="rule-wp-48"></a>

# WP-48 — Account Portal

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: K — Web and release
> Upstream: `42`, `44`, `47` · Downstream: `49`

> **Goal.** Deliver the canonical account origin as one deployment profile of the single React/TypeScript application: account, security, devices, workspace, storage, entitlement, billing, AI and data — with no second account application anywhere.

---

## 1. Scope and purpose

**In scope.** The account deployment profile of `ArcForges.Web.App`: authentication in the browser with step-up; account and security management; device list and trust; single-owner workspace settings; storage and usage; entitlement, subscription, credits and billing history; data export and deletion; and the per-origin security posture.

**Out of scope.** The ArcChat web companion (`49`) — a different deployment profile. The static site (`47`). The operator console, which is a separate origin and identity system.

**Why this package exists.** **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)** makes `account.arcforges.com` the canonical account origin and forbids a second account application. [the current dependency model](../implementation-sequence.md#2-phase-structure) requires the portal to follow identity, workspace, device, entitlement and billing APIs — which is why it lands after `42` and `44`.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/10-web-architecture.md`](../../architecture/10-web-architecture.md) `§3`–`§6` | The application structure, surface matrix, browser authentication and content security |
| [`../../requirements/02-identity-account-and-workspace.md`](../../requirements/02-identity-account-and-workspace.md) `§12` | Portal scope |
| **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**, **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)** | Canonical account origin and the surface inventory |
| [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42), [WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44), [WP-47](47-static-public-site.md#rule-wp-47) output | Commerce, policy and the public site boundary |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **`ArcForges.Web.App` is the only interactive browser application** (**[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)**), deployed per surface profile. |
| BR-02 | **`arcforges.com/account` is a permanent redirect, never a second account application** (**[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**). |
| BR-03 | **Deployments do not share state, storage or cookies**, and no broad parent-domain authentication cookie exists (**[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**). |
| BR-04 | **React/TypeScript production assets use the pinned Node/npm build**, generated SDK and the shared design system; .NET WASM/AOT flags do not apply. |
| BR-05 | **No access/refresh credential is script-readable or delivered to browser JSON.** The adopted C# opaque-cookie session and CSRF/origin rules apply. |
| BR-06 | **A web session is shorter-lived and less trusted than a desktop session**, and a new browser does not immediately hold high-risk approval capability. |
| BR-07 | **Step-up is available in the browser** for the enumerated sensitive operations. |
| BR-08 | **No secret is compiled into the bundle.** Any value in the bundle is public. |
| BR-09 | **Bundle size is a tracked budget with a regression gate.** |
| BR-10 | **Losing entitlement never deletes local data**, and the portal states that plainly. |
| BR-11 | **Deletion is explicit about what is and is not deleted**, with a grace period. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Web/ArcForges.Web.App/` | Shell, deployment profile selection, navigation, theming, locale |
| `src/Web/ArcForges.Web.App/app/features/account/` | Account, security, devices, sessions, recovery |
| `src/Web/ArcForges.Web.App/app/features/workspace/` | Workspace settings, storage, usage, capacity and service term. **No membership surface** ([WO-01](../../architecture/data-model/01-cloud-data-model.md#rule-wo-01)) |
| `src/Web/ArcForges.Web.App/app/features/commerce/` | Entitlement, subscription, credits, billing history, invoices |
| `src/Web/ArcForges.Web.App/app/features/data/` | Export, deletion, data health visibility |
| `deploy/edge/account/` | Origin configuration: content security policy, cookie policy, CORS, CSRF posture |
| `src/Web/tests/` | Authentication, step-up, bundle budget, accessibility and profile-isolation suites |

**Major types introduced.** `DeploymentProfile`, `AccountSession`, `BrowserSessionTransport`, `StepUpFlow`, `DeviceListView`, `WorkspaceView`, `EntitlementView`, `CreditsView`, `BillingHistoryView`, `ExportRequestView`, `DeletionRequestView`.

---

## 5. Required implementation work

<a id="rule-wp-48.00"></a>

### WP-48.00 — React account profile and visual composition

**What must be fully done.** Compose the Account route graph and shell using [WP-47](47-static-public-site.md#rule-wp-47)'s owned components/tokens, generated TS SDK and TanStack Query. Account and Chat share source but produce separate route builds; no client storage/cookie/query scope crosses origins. Provide responsive account overview, navigation, safe runtime public config, error boundaries and complete loading/empty/pending/expired states. Clear caches/abort requests on user/workspace changes.

**Testing requirements.** Production per-profile route/chunk inspection; visual and keyboard tests in both themes and narrow layouts; long-translation and scope-switch late-response tests; no private config or Chat feature leakage.

**Completion gate.** One React codebase builds isolated profiles; approved account visuals and complete safe state transitions use real generated client contracts.

<a id="rule-wp-48.01"></a>

### WP-48.01 — Real browser session and step-up acceptance

**What must be fully done.** Use the [P2-003](../../decisions/phase-2-specification-decisions.md#rule-p2-003) adapter implemented in [WP-22.08](22-identity-workspace-and-device.md#rule-wp-22.08), not a new auth choice. Complete passkey/email verification/recovery, live opaque cookie session, server-controlled expiry/revocation and sensitive-action step-up on the real account origin topology. Fetch CSRF state safely and never hold bearer/refresh tokens in the app. Coordinate tabs without rotating credentials per request; require fresh authentication after absolute expiry.

**Testing requirements.** Playwright against production assets/edge/real Cloud and PostgreSQL: login/logout, two origins and two tabs, sibling-origin CSRF on JSON/multipart, passkey expected origin, replica restart, expiry/revoke races, no token in storage/URL/logs, no cookie leakage, step-up failure, no elevated new-browser trust. Manual passkey/browser matrix evidence supplements automation.

**Completion gate.** Browser authentication and sensitive actions work through the adopted server session authority with no credential leaks, session resurrection, CSRF bypass or high-risk trust shortcut.

<a id="rule-wp-48.02"></a>

### WP-48.02 — Account and security surfaces

**What must be fully done.** Profile, authentication methods, passkey management, sessions, device list with trust levels and revocation, recovery configuration, and the security event view from the audit store.

**Testing requirements.** Device revocation propagation; passkey add and remove; a security-event visibility test; a step-up-required assertion on each sensitive action.

**Completion gate.** Every sensitive account action requires step-up, and device revocation propagates promptly.

<a id="rule-wp-48.03"></a>

### WP-48.03 — Workspace, storage and usage

**What must be fully done.** Single-owner workspace settings — **no membership, invitation, role or seat surface** ([WO-01](../../architecture/data-model/01-cloud-data-model.md#rule-wo-01)–[WO-05](../../architecture/data-model/01-cloud-data-model.md#rule-wo-05)); **service term and included-capacity display with recovery timing and the extra-credit opt-in** ([EC-01](../../architecture/contracts/01-public-api-operations.md#rule-ec-01)–[EC-04](../../architecture/contracts/01-public-api-operations.md#rule-ec-04)); storage consumption computed from committed objects; usage against quota with reset boundaries visible; data health visibility.

**Testing requirements.** Accounting comparison against server-side figures; boundary display tests; **a structural test asserting no membership, invitation, role or seat operation is offered**; a projection test asserting the portal receives no supplier rate, route weight or other user's state ([DC-14](../../requirements/11-policy-and-configuration.md#rule-dc-14)); a display test asserting capacity and purchased credits are never summed into one figure ([CD-07](../../architecture/16-billing-and-commerce-architecture.md#rule-cd-07)).

**Completion gate.** Displayed storage and usage match server-side computed values exactly.

<a id="rule-wp-48.04"></a>

### WP-48.04 — Subscription, capacity, credits and hosted checkout

**What must be fully done.** Implement consumer subscription/management views using public server projections and generated operations. Display paid-term state, replenishing included capacity and purchased credits separately, with explicit credit opt-in and server-provided rate-limit/recovery reasons. Hosted checkout opens in the browser; returning shows confirming until verified Cloud state changes. Price/tax changes require renewed confirmation; no client/provider redirect grants entitlement.

**Testing requirements.** Real C# accounting/checkout-test-environment flows; exact amount display above JS safe-integer boundaries; duplicate click, cancelled/failed/late provider confirmation, refund, term expiry and stale-price tests; approved responsive/accessible pricing/status visuals; no card fields or supplier-policy exposure.

**Completion gate.** The real commercial state and exact values drive a complete purchase/manage/recovery UX, with no duplicate debit or frontend entitlement authority.

<a id="rule-wp-48.05"></a>

### WP-48.05 — Data export and deletion

**What must be fully done.** Export requests with progress and download; deletion requests with a grace period and an explicit statement of what is and is not deleted, including that local data is untouched.

**Testing requirements.** Export completeness; a deletion-statement accuracy test; a grace-period test; a local-data assertion.

**Completion gate.** Export is complete, and deletion states accurately what it does and does not remove — including that local data is untouched.

<a id="rule-wp-48.06"></a>

### WP-48.06 — Origin security and performance

**What must be fully done.** A strict content security policy with no inline script by default; per-origin cookie, CORS and CSRF posture; no secret in the bundle; sandboxed preview of any user content; bundle size and first-interactive budgets with regression gates.

**Testing requirements.** Policy header verification; a bundle secret scan; a sandbox escape test on hostile content; budget measurements with the regression gate applied.

**Completion gate.** The origin enforces its own strict policy, the bundle contains no secret, and bundle and interactivity budgets pass their regression gate.

<a id="rule-wp-48.07"></a>

### WP-48.07 — Offline, degradation and accessibility

**What must be fully done.** Honest offline behaviour that preserves unsent input and never pretends to work; a cloud outage reporting which capabilities are unavailable with reasons rather than blanking; accessibility on every major workflow with keyboard-only completion.

**Testing requirements.** Offline behaviour tests; a cloud-outage test asserting the application does not blank; accessibility automated and manual passes.

**Completion gate.** The application never blanks during an outage, states what is unavailable and why, and every core workflow completes by keyboard.

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None directly; consumes cloud APIs |
| Protocol | Consumes identity, entitlement, commerce and policy contracts |
| UI | The canonical account experience |
| Security | Browser token handling, step-up, origin isolation and content security |
| Platform | Browser support matrix |
| Migration | Bundle and contract version compatibility for cached clients |
| Compatibility | A cached older client is told to refresh with a grace period, never silently broken |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Profile isolation and composition results | [WP-48.00](#rule-wp-48.00) |
| Token storage, refresh, step-up and new-browser trust results | [WP-48.01](#rule-wp-48.01) |
| Device revocation, passkey and step-up coverage results | [WP-48.02](#rule-wp-48.02) |
| Storage and usage accounting comparison | [WP-48.03](#rule-wp-48.03) |
| Entitlement reason coverage, credit separation and no-payment-field scan | [WP-48.04](#rule-wp-48.04) |
| Export completeness and deletion statement accuracy | [WP-48.05](#rule-wp-48.05) |
| Policy headers, bundle secret scan and budget measurements | [WP-48.06](#rule-wp-48.06) |
| Offline, outage and accessibility results | [WP-48.07](#rule-wp-48.07) |

---

**React acceptance evidence.** In addition to the workflow results, retain generated-SDK input fingerprint, TypeScript/RTL checks, production Playwright API/session/visual results, private-config/route isolation scan and approved consumer layouts. [PG-23](../../assurance/open-gates-register.md#rule-pg-23) covers the resulting browser deployment proof.

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. One codebase produces both deployment profiles with provably isolated state, storage and cookies.
2. **Browser JavaScript receives no bearer/refresh credential**; opaque-cookie expiry/revocation and explicit CSRF/origin checks pass across replicas and tabs; a new browser holds no immediate high-risk approval capability.
3. Every sensitive account action requires step-up; device revocation propagates promptly.
4. Displayed storage and usage match server-side computed values exactly.
5. Entitlement shows a reason per capability; credit classes are never summed; **no payment instrument field exists anywhere in the application**.
6. Export is complete; deletion accurately states what it removes, including that local data is untouched.
7. The origin enforces a strict content security policy; the bundle contains no secret; bundle and interactivity budgets pass their regression gate.
8. The application never blanks during a cloud outage, states what is unavailable and why, and every core workflow completes by keyboard.
9. **`arcforges.com/account` is a permanent redirect and no second account application exists.**

---

## 9. Dependencies

**Upstream — all must be complete.**

- [42 — Commerce, Entitlement and Credits](42-commerce-entitlement-and-credits.md)
- [44 — Dynamic Policy and Configuration Control Plane](44-dynamic-policy-and-configuration.md)
- [47 — Static Public Site](47-static-public-site.md)

**Downstream — these consume this package’s completed output.**

- [49 — ArcChat Web Companion](49-arcchat-web-companion.md)
