# Web Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: **[D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007)** (technology and rendering boundary), **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** (surface inventory), **[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)** (canonical account origin)
> Companions: [`../requirements/products/arcforges-web.md`](../requirements/products/arcforges-web.md), [`08-security-architecture.md`](08-security-architecture.md), [`05-cloud-architecture.md`](05-cloud-architecture.md)

Two build outputs, several deployments, one shared contract layer.

---

## 1. Build outputs

```
ArcForges.Web.StaticGen          C#/.NET build-time generator
      ↓ produces
Static site artifacts            HTML + CSS + minimal assets
      → arcforges.com · docs.arcforges.com · legal and download pages

ArcForges.Web.App                standalone Blazor WebAssembly
      ↓ deployed as
account.arcforges.com            account and cloud control centre
chat.arcforges.com               ArcChat web companion
```

| # | Rule |
|---|---|
| BO-01 | **Public marketing, legal, download and information pages render as static HTML and CSS without waiting for the .NET runtime or WebAssembly** (**[D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007)**). |
| BO-02 | **Static pages are deployment artifacts, not a second browser application.** |
| BO-03 | **`ArcForges.Web.App` is the only interactive browser application.** |
| BO-04 | **`RunAOTCompilation=false`** unless a measured benchmark and an explicit decision prove otherwise (**[D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007)**). |
| BO-05 | **Prohibited**: Blazor Server circuits, Interactive Server, runtime server-side rendering, React, TypeScript, Node, any JavaScript package manager. |
| BO-06 | **Minimal audited JavaScript interop only**, where the browser or a required provider offers no adequate managed interface — each instance reviewed and listed. |

---

## 2. Static generation

```
Content sources (repository content, product catalogue, release metadata,
                 changelog, legal document versions, locale resources)
        ↓
StaticGen (C#, build time)
        ↓
Per-locale, per-page static output + sitemap + metadata + redirects
        ↓
Edge-hosted immutable artifacts with long cache lifetimes and content hashing
```

| # | Rule |
|---|---|
| SG-01 | **Product catalogue and release metadata come from one source of truth** ([ST-01](../requirements/products/arcforges-web.md#rule-st-01), [ST-02](../requirements/products/arcforges-web.md#rule-st-02) in the web requirements). The generator consumes it; it never re-states versions. |
| SG-02 | **Pricing comes from one source of truth** ([ST-03](../requirements/products/arcforges-web.md#rule-st-03) there). |
| SG-03 | **Above-the-fold content is present in the delivered HTML.** No client script is required to render it. |
| SG-04 | **Locale-scoped URLs with correct alternate-language annotations**; no client-only language switching and no trapping automatic redirect ([IL-01](../requirements/products/arcforges-web.md#rule-il-01) there). |
| SG-05 | **No blocked third-party resource on the critical path** — fonts, script hosts, analytics and verification providers all chosen for global reachability ([IL-02](../requirements/products/arcforges-web.md#rule-il-02) there). |
| SG-06 | **Assets are content-hashed and immutably cached**; HTML carries a short cache lifetime so a release is visible promptly. |
| SG-07 | **The generator is deterministic**, so the same inputs produce byte-identical output and a diff is meaningful. |

---

## 3. The Blazor WebAssembly application

```
ArcForges.Web.App
├── Shell                      navigation, layout, theming, locale
├── Deployment profile         Account | Chat — selected at build or configuration time
├── Feature modules            account · workspace · storage · AI · devices · remote
│                              · security · billing · data — and — chat · tasks
│                              · artifacts · projects · automations · search
├── Contract clients           generated typed HTTP clients + realtime client
├── Session and token handling short-lived tokens, refresh serialisation
└── State                      per-surface, never a cross-surface shared store
```

| # | Rule |
|---|---|
| WA-01 | **One codebase, several deployments** (**[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)**). A deployment profile selects the feature set, navigation and branding. |
| WA-02 | **Deployments do not share state, storage or cookies** ([WB-02](08-security-architecture.md#rule-wb-02) in the security architecture). |
| WA-03 | **Serialization uses source-generated contexts** for every DTO, matching the desktop and mobile clients. |
| WA-04 | **The typed HTTP client uses the generated-only entry point**; the reflection package is absent (**[F-026](../assurance/open-gates-register.md#rule-f-026)**). |
| WA-05 | **Realtime uses the JSON protocol with source-generated payload metadata.** |
| WA-06 | **Token refresh is serialised** so concurrent requests never trigger a refresh storm. |
| WA-07 | **On a realtime message the client re-reads authoritative state where it needs full fidelity** ([RL-04](05-cloud-architecture.md#rule-rl-04) in the cloud architecture). |
| WA-08 | **Bundle size is a tracked budget** with a regression gate (`§20` of the quality contract). |

---

## 4. Surface deployment matrix

| Surface | Output | Auth | Notes |
|---|---|---|---|
| `arcforges.com` | Static | None | Discovery and download; no account gate |
| `www.arcforges.com` | Redirect | — | Permanent redirect |
| `account.arcforges.com` | Web App (Account profile) | Required | **Canonical account origin** (**[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)**) |
| `chat.arcforges.com` | Web App (Chat profile) | Required | ArcChat companion |
| `docs.arcforges.com` | Static | None | Versioned per product |
| `status.arcforges.com` | **Independently hosted** | None | Survives a cloud outage |
| `downloads.arcforges.com` | Artifacts | None | Signed, hashed |
| `updates.arcforges.com` | Artifacts + metadata | None | Consumed by the updater |
| `api.arcforges.com` | Cloud API | Per endpoint | Not a browsable site |
| `ops.arcforges.com` | Operator surface | **Separate identity system** | Never in public navigation |
| `notify.arcforges.com` | Link and message domain | — | Not an application |
| `news.arcforges.com` | Optional content domain | — | Not an application |

| # | Rule |
|---|---|
| SM-01 | **`arcforges.com/account` is a permanent redirect and never a second account application** (**[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)**). |
| SM-02 | **Each origin has its own CSP, cookie policy, CORS policy and CSRF posture.** |
| SM-03 | **No broad parent-domain authentication cookie exists** (**[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)**). |
| SM-04 | **The status page is hosted independently of ArcForges Cloud**, with an emergency alternate URL ([SL-07](../requirements/products/arcforges-cloud.md#rule-sl-07) in the cloud product requirements). |

---

## 5. Authentication in the browser

| # | Rule |
|---|---|
| AU-01 | **Short-lived access tokens**, with refresh rotation and revocation. |
| <a id="rule-au-02"></a>AU-02 | **A long-lived access token is never held in storage readable by arbitrary scripts** ([WB-05](08-security-architecture.md#rule-wb-05) in the security architecture). |
| <a id="rule-au-03"></a>AU-03 | **The concrete token-handling deployment — cookie-based backend-for-frontend versus in-memory tokens — is settled by a decision record**, and both must satisfy [AU-02](#rule-au-02). |
| AU-04 | **A web session is shorter-lived and less trusted than a desktop session** ([OF-07](../requirements/products/arcchat-mobile-and-web.md#rule-of-07) in the companion requirements). |
| AU-05 | **A new browser does not immediately hold high-risk approval capability** ([OF-08](../requirements/products/arcchat-mobile-and-web.md#rule-of-08) there). |
| AU-06 | **Step-up authentication is available in the browser** for the enumerated sensitive operations (`§6` of the identity requirements). |
| AU-07 | **Passkey authentication is the primary browser method**, with email one-time codes for first verification and recovery. |

---

## 6. Content security

| # | Rule |
|---|---|
| CS-01 | **A strict Content Security Policy** with no inline script permitted by default; the WebAssembly application's requirements are met by explicit, reviewed directives. |
| CS-02 | **No secret is compiled into the bundle** ([WB-04](08-security-architecture.md#rule-wb-04) there). Any value in the bundle is public. |
| CS-03 | **Cross-origin policy is an explicit allowlist** ([WB-06](08-security-architecture.md#rule-wb-06) there). |
| CS-04 | **Uploads are content-type-, size- and format-validated with a quarantine area, and never executed server-side** ([WB-07](08-security-architecture.md#rule-wb-07) there). |
| CS-05 | **Realtime transport logs redact tokens** ([WB-08](08-security-architecture.md#rule-wb-08) there). |
| <a id="rule-cs-06"></a>CS-06 | **Preview rendering of user content is sandboxed** — untrusted HTML or documents never execute in the application origin ([EX-06](../requirements/03-cloud-services-and-sync.md#rule-ex-06) in the cloud requirements). |
| <a id="rule-cs-07"></a>CS-07 | **There are no public share links in V1** ([SE-08](../requirements/products/arcforges-web.md#rule-se-08) in the web requirements). Links are authenticated and private. |
| CS-08 | **A cloud resource URL verifies permission at access**, and a denial does not disclose existence where that would leak ([LN-04](../requirements/products/arcchat-mobile-and-web.md#rule-ln-04) in the companion requirements). |

---

## 7. Offline and resilience

| # | Rule |
|---|---|
| OR-01 | **Web offline is minimal and honest** ([OF-05](../requirements/products/arcchat-mobile-and-web.md#rule-of-05) in the companion requirements): the application states it is offline and preserves unsent input; it does not pretend to work. |
| <a id="rule-or-02"></a>OR-02 | **A cloud outage does not blank the application.** It reports which capabilities are unavailable, with reasons. |
| OR-03 | **Realtime loss degrades to polling authoritative state**, then backfills on reconnection ([RL-04](05-cloud-architecture.md#rule-rl-04) in the cloud architecture). |
| OR-04 | **The static site is entirely independent of Cloud** and remains available during any cloud incident. |

---

## 8. Accessibility, localisation and performance

| # | Rule |
|---|---|
| AL-01 | **WCAG 2.2 AA semantics on all major workflows**, in both the static site and the application (`§10` of the quality contract). |
| <a id="rule-al-02"></a>AL-02 | **Keyboard-only completion of every core workflow.** |
| AL-03 | **Every user-visible string is localisable**, including in generated static pages. |
| AL-04 | **Locale-safe data handling**: canonical storage, localised presentation ([LO-06](../requirements/12-quality-and-compatibility-contract.md#rule-lo-06)–[LO-09](../requirements/12-quality-and-compatibility-contract.md#rule-lo-09) there). |
| AL-05 | **Public site performance is a product requirement** measured at the 75th percentile, and the above-the-fold render does not depend on the client runtime ([IL-03](../requirements/products/arcforges-web.md#rule-il-03) in the web requirements). |
| AL-06 | **Application performance carries its own budgets**: bundle size, first interactive, and interaction responsiveness, each with a regression gate. |

---

## 9. Analytics

| # | Rule |
|---|---|
| AN-01 | **Minimal, privacy-preserving analytics** ([PV-05](../requirements/07-security-privacy-and-trust.md#rule-pv-05) in the security requirements). |
| AN-02 | **No cross-site advertising profile, no data sale.** |
| AN-03 | **No consent wall is required for the basic static site**, because the basic site does not require consent-bearing tracking. |
| AN-04 | **Application telemetry is consented and carries no user content** ([OB-05](../requirements/products/arcforges-cloud.md#rule-ob-05) in the cloud architecture). |

---

## 10. Build and deployment

```
CI build
 ├── StaticGen → static artifacts       → edge hosting (immutable, hashed)
 └── Web App publish → WebAssembly      → edge hosting per deployment profile
        ↓
Same artifact promoted through environments; production never rebuilds
        ↓
Rollback restores the previous artifact set
```

| # | Rule |
|---|---|
| BD-01 | **Build once, promote the same artifact** ([EN-10](../requirements/products/arcforges-cloud.md#rule-en-10) in the cloud product requirements). |
| BD-02 | **Deployment is atomic per surface**, so a partially updated site never exists. |
| BD-03 | **A release updates the static site and the application together where a shared contract changed**, and the compatibility policy governs older cached clients (`§7` of the policy requirements). |
| BD-04 | **A cached older client is handled by compatibility policy**, not by breaking it silently: it is told to refresh, with a grace period. |
| BD-05 | **The WebAssembly publish and its AOT-build verification are part of the release matrix** ([PM-04](../requirements/12-quality-and-compatibility-contract.md#rule-pm-04) in the quality contract). |

---

## 11. Non-goals

The web layer is **not**: an ArcNotes, ArcScope or ArcSlate editor; a second account application; a public sharing platform in V1; a JavaScript-framework application; a server-rendered application; or a heavy client on public marketing pages.

---

## 12. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 2` | Surface layout, marketing site positioning, account portal scope, documentation, status, internationalisation, performance and analytics |
| `I4 §Stage 7 §54–56` | ArcChat Web as a cloud surface, separate from the account portal |
| `I3 §18` | Blazor WebAssembly boundaries, communication rules and web security |
| **[D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007)** | Static public rendering; one WebAssembly application; prohibited technologies |
| **[D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014)** | The surface inventory and "a hostname is not an application" |
| **[D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015)** | Canonical account origin and per-origin boundary policy |
| **[F-026](../assurance/open-gates-register.md#rule-f-026)** | Typed HTTP client entry point and reflection-package prohibition |
