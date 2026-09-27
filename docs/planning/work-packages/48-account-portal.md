<a id="rule-wp-48"></a>

# WP-48 — Account Portal

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: K — Web and release
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Deliver the canonical account origin as one deployment profile of the single React/TypeScript application: account, security, devices, workspace, storage, entitlement, billing, AI and data — with no second account application anywhere.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Web + Cloud. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: production React build and real C#/CF endpoints with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The account deployment profile of `ArcForges.Web.App`: authentication in the browser with step-up; account and security management; device list and trust; single-owner workspace settings; storage and usage; entitlement, subscription, credits and billing history; data export and deletion; and the per-origin security posture.

**Out of scope.** The ArcChat web companion (`49`) — a different deployment profile. The static site (`47`). The operator console, which is a separate origin and identity system.

**Why this package exists.** **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)** makes `account.arcforges.com` the canonical account origin and forbids a second account application. [the current dependency model](../implementation-sequence.md#2-phase-structure) requires the portal to follow identity, workspace, device, entitlement and billing APIs — which is why it lands after `42` and `44`.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/10-web-architecture.md`](../../architecture/10-web-architecture.md) `§3`–`§6` | The application structure, surface matrix, browser authentication and content security |
| [`../../requirements/02-identity-account-and-workspace.md`](../../requirements/02-identity-account-and-workspace.md) `§12` | Portal scope |
| **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**, **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)** | Canonical account origin and the surface inventory |
| [WP-42](42-commerce-entitlement-and-credits.md#rule-wp-42), [WP-44](44-dynamic-policy-and-configuration.md#rule-wp-44), [WP-47](47-static-public-site.md#rule-wp-47) output | Commerce, policy and the public site boundary |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) as amended by [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **`ArcForges.Web.App` is the only interactive browser application** (**[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)**), deployed per surface profile. |
| <a id="rule-br-02"></a>BR-02 | **`arcforges.com/account` is a permanent redirect, never a second account application** (**[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**). |
| <a id="rule-br-03"></a>BR-03 | **Deployments do not share state, storage or cookies**, and no broad parent-domain authentication cookie exists (**[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**). |
| <a id="rule-br-04"></a>BR-04 | **React/TypeScript production assets use the pinned Node/npm build**, generated SDK and the shared design system; .NET WASM/AOT flags do not apply. |
| <a id="rule-br-05"></a>BR-05 | **No access/refresh credential is script-readable or delivered to browser JSON.** The adopted C# opaque-cookie session and CSRF/origin rules apply. |
| <a id="rule-br-06"></a>BR-06 | **A web session is shorter-lived and less trusted than a desktop session**, and a new browser does not immediately hold high-risk approval capability. |
| <a id="rule-br-07"></a>BR-07 | **Step-up is available in the browser** for the enumerated sensitive operations. |
| <a id="rule-br-08"></a>BR-08 | **No secret is compiled into the bundle.** Any value in the bundle is public. |
| <a id="rule-br-09"></a>BR-09 | **Bundle size is a tracked budget with a regression gate.** |
| <a id="rule-br-10"></a>BR-10 | **Losing entitlement never deletes local data**, and the portal states that plainly. |
| <a id="rule-br-11"></a>BR-11 | **Deletion is explicit about what is and is not deleted**, with a grace period. |

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

### WP-48.00 — Account profile and native ceremony integration

**What must be fully done.** Build account Web output using WP22 identity/browser/native endpoints and WP42 commerce. Integrate Android callback/assetlinks with actual production signing input and exact route map; minimal auth producer already exists in WP22. Compose the account route graph/shell using WP47 components/tokens, generated TS SDK and TanStack Query. Include responsive overview/navigation, safe public runtime config, error boundaries and loading/empty/pending/expired states; clear caches and abort requests on user/workspace changes.

**Testing requirements.** No cookie leakage, state/PKCE/origin mismatch, Android verified links, purchase/read-only expired-service/export and separate operator denial. Check production route/chunk isolation, both themes, keyboard/narrow layouts, long translations and scope-switch late responses; no private config or Chat-feature leakage.

**Completion gate.** Account profile is deployed with real identity/commerce producers and release gates retain their live evidence requirements. Approved account visuals and safe states use the real generated client.

<a id="rule-wp-48.01"></a>

### WP-48.01 — Real browser session and step-up acceptance

**What must be fully done.** Use the [P2-003](../../decisions/phase-2-specification-decisions.md#rule-p2-003) adapter implemented in [WP-22.08](22-identity-workspace-and-device.md#rule-wp-22.08), not a new auth choice. Complete passkey/email verification/recovery, live opaque cookie session, server-controlled expiry/revocation and sensitive-action step-up on the real account origin topology. Fetch CSRF state safely and never hold bearer/refresh tokens in the app. Coordinate tabs without rotating credentials per request; require fresh authentication after absolute expiry.

**Testing requirements.** Playwright against production assets/edge/real Cloud and D1: login/logout, two origins and two tabs, sibling-origin CSRF on JSON/multipart, passkey expected origin, replica restart, expiry/revoke races, no token in storage/URL/logs, no cookie leakage, step-up failure, no elevated new-browser trust. Manual passkey/browser matrix evidence supplements automation.

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

**Required implementation and closure from the final review.** Implement and independently verify [08-security-architecture](../../architecture/08-security-architecture.md#account-and-provider-closure). Deliver all account/security flows, scoped token creation display-once, email/passkey/recovery/session controls, remote policy, workspace data deletion/health and account cancellation restricted route. Consume real WP22/25/42/44/46 APIs, including export with lapsed term and no automatic old-generation replay. No browser-only business rule or fixture remains. Record exact artifact identities and real/fixture status with the existing substeps; these cases are part of this package's completion gate.

<a id="rule-wp-48.90"></a>
### WP-48.90 — Verify the owned artifact and real integration

**What must be fully done.** Assemble the owned deliverables from the preceding substeps under the selected repository, package, runtime and protocol authorities. Retain Account profile/session/step-up/privacy/commerce behavior. Implement routes using proto/gRPC-Web and the actual AOT session adapter; expose existing CF usage/storage status through owned APIs.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Real browser against the AOT release: cookie secrecy, CSRF, expiry/revocation, privacy/export and admission/usage display. No AGPL application import into Mobile.

**Completion gate.** Real browser against the AOT release: cookie secrecy, CSRF, expiry/revocation, privacy/export and admission/usage display. No AGPL application import into Mobile. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

**Browser matrix acceptance.** Use [browser-support.v1](../../requirements/12-quality-and-compatibility-contract.md#202-browser-supportv1) and the exact release artifact/OS/browser patches. For each output’s existing flows, verify supported/degraded/blocked browser behavior: delayed-stream polling where streaming exists, refusal of unavailable required authentication/step-up, safe-preview refusal and preserved pending work. Static site acceptance includes no-JavaScript readability; it does not invent interactive account/stream APIs. Operator step-up retains its separate Entra/MFA authority. WP23 proves generated transports; WP45/47/48/49 prove their respective operations/site/account/chat output; WP50 joins all four production hashes and real browser evidence. A Playwright WebKit run alone does not claim Safari/OS authenticator proof.

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None directly; consumes cloud APIs |
| Protocol | Consumes identity, entitlement, commerce and policy contracts |
| UI | The canonical account experience |
| Security | Browser token handling, step-up, origin isolation and content security |
| Platform | [browser-support.v1](../../requirements/12-quality-and-compatibility-contract.md#202-browser-supportv1) |
| Migration | Bundle and contract version compatibility for cached clients |
| Compatibility | A cached older client is told to refresh with a grace period, never silently broken |

---

## 7. Tests and verification evidence

Acceptance includes every amended §5 producer/consumer and [WP-48.90](#rule-wp-48.90) evidence. Current [P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) contracts/data/runtime rules are tested in the original owner implementation, not a detached explanatory sample.

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
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-48.90](#rule-wp-48.90) |

---

**React acceptance evidence.** In addition to the workflow results, retain generated-SDK input fingerprint, TypeScript/RTL checks, production Playwright API/session/visual results, private-config/route isolation scan and approved consumer layouts. [PG-23](../../assurance/open-gates-register.md#rule-pg-23) covers the resulting browser deployment proof.

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-48.90](#rule-wp-48.90) and all inherited domain-specific gates must pass on the same candidate closure. Real browser against the AOT release: cookie secrecy, CSRF, expiry/revocation, privacy/export and admission/usage display. No AGPL application import into Mobile.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-48](#rule-wp-48) — Real Account commercial/session workflows and approved visual/accessibility/performance evidence. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

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

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [WEB.10](../delivery/lanes/web.md#task-web-10) | [WP-48.00](48-account-portal.md#rule-wp-48.00) (full) | [WEB.08](../delivery/lanes/web.md#task-web-08) (artifact), [CON.07](../delivery/lanes/contracts.md#task-con-07) (contract) |
| [WEB.11](../delivery/lanes/web.md#task-web-11) | [WP-48.01](48-account-portal.md#rule-wp-48.01) (full) | [CLOUD.19](../delivery/lanes/cloud.md#task-cloud-19) (artifact) |
| [WEB.12](../delivery/lanes/web.md#task-web-12) | [WP-48.02](48-account-portal.md#rule-wp-48.02) (full) | none |
| [WEB.13](../delivery/lanes/web.md#task-web-13) | [WP-48.03](48-account-portal.md#rule-wp-48.03) (full) | none |
| [WEB.14](../delivery/lanes/web.md#task-web-14) | [WP-48.04](48-account-portal.md#rule-wp-48.04) (all work except the parts mapped to WEB.29) | [CON.08](../delivery/lanes/contracts.md#task-con-08) (contract) |
| [WEB.15](../delivery/lanes/web.md#task-web-15) | [WP-48.05](48-account-portal.md#rule-wp-48.05) (full) | [CON.22](../delivery/lanes/contracts.md#task-con-22) (contract) |
| [WEB.16](../delivery/lanes/web.md#task-web-16) | [WP-48.06](48-account-portal.md#rule-wp-48.06) (full) | none |
| [WEB.17](../delivery/lanes/web.md#task-web-17) | [WP-48.07](48-account-portal.md#rule-wp-48.07) (full) | none |
| [WEB.18](../delivery/lanes/web.md#task-web-18) | [WP-48.90](48-account-portal.md#rule-wp-48.90) (full; final-review closure: 08-security-architecture account/provider closure, scoped-token display-once, cancellation restricted route)<br>[WP-48](48-account-portal.md#rule-wp-48) Required implementation and closure from the final review: 08-security-architecture account/provider closure, scoped-token display-once, cancellation restricted route (package-level obligation contribution)<br>[WP-48](48-account-portal.md#rule-wp-48) Browser matrix acceptance paragraph (browser-support.v1 for the account output) (package-level obligation contribution) | none |
| [WEB.29](../delivery/lanes/web.md#task-web-29) | [WP-48.04](48-account-portal.md#rule-wp-48.04) (real-provider-evidence closure) | [COM.14](../delivery/lanes/commerce.md#task-com-14) (artifact), [POL.08](../delivery/lanes/policy.md#task-pol-08) (artifact) |

**Consumers outside this package:** [REL.05](../delivery/lanes/release.md#task-rel-05), [WEB.19](../delivery/lanes/web.md#task-web-19), [WEB.30](../delivery/lanes/web.md#task-web-30), [WEB.31](../delivery/lanes/web.md#task-web-31).

<!-- delivery-graph:end -->

