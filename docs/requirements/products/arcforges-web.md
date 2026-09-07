# ArcForges Web — Product Requirements
> Current scope amendment: **[P2-006](../../decisions/phase-2-specification-decisions.md#rule-p2-006)** (2026-09-06) governs cloud AI, single-user scope, product exclusions and configuration-driven metering. Earlier references apply only where consistent.

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements / Products
> Governing authority: **[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)** (web technology and rendering boundary), **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)** (surface inventory), **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)** (canonical account portal)
> Companions: [`arcchat-mobile-and-web.md`](arcchat-mobile-and-web.md), [`../02-identity-account-and-workspace.md`](../02-identity-account-and-workspace.md), [`../04-commerce-entitlement-and-credits.md`](../04-commerce-entitlement-and-credits.md), [`../../architecture/10-web-architecture.md`](../../architecture/10-web-architecture.md)

The web presence is ArcForges' **only official outward entrance system**. It is not "a website"; it carries discovery, download, documentation, status, account management, cloud control and commerce.

Three roles, and only three:

> **The marketing site discovers and downloads. The account portal manages the cloud. ArcChat Web is a product surface.**

---

## 1. Surface inventory

The twelve-entry inventory is fixed by **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)**.

| Surface | Role | Nature |
|---|---|---|
| `arcforges.com` | Canonical public marketing site | **Static artifacts** |
| `www.arcforges.com` | Permanent redirect to `arcforges.com` | Redirect |
| `account.arcforges.com` | **Canonical authenticated account portal** | `ArcForges.Web.App` deployment |
| `chat.arcforges.com` | ArcChat web companion | `ArcForges.Web.App` deployment |
| `api.arcforges.com` | Public Cloud API | Service |
| `docs.arcforges.com` | Public documentation | Static artifacts |
| `status.arcforges.com` | Public service status | **Independently hosted** |
| `downloads.arcforges.com` | Signed release downloads | Artifacts |
| `updates.arcforges.com` | Update metadata and release artifacts | Artifacts |
| `ops.arcforges.com` | Private operator-only surface | **Never in public navigation** |
| `notify.arcforges.com` | Transactional messaging and link domain | Not a separate application |
| `news.arcforges.com` | Optional marketing communication domain | Not a separate application |

| # | Requirement |
|---|---|
| SI-01 | **A hostname is not an application** (**[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)**). Account and Chat are separately deployed configurations of one `ArcForges.Web.App` codebase; static surfaces remain static artifacts. |
| SI-02 | **`account.arcforges.com` is canonical** (**[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**). `arcforges.com/account` is a **permanent redirect** and must never become a second account application. |
| SI-03 | **Explicit origin, cookie, OAuth redirect, CSP, CSRF and CORS boundaries** apply per surface. **No broad parent-domain authentication cookies** (**[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)**). |
| <a id="rule-si-04"></a>SI-04 | **`status.arcforges.com` is hosted independently of ArcForges Cloud**, so a cloud outage cannot take the status page down with it. |
| SI-05 | **`ops.arcforges.com` never appears in public navigation** and is reachable only by authorised operators (`§10` of the distribution requirements). |

---

## 2. Technology boundary

Fixed by **[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)** and not reopened.

| # | Requirement |
|---|---|
| <a id="rule-tb-01"></a>TB-01 | **Public marketing, legal, download and information pages render as static HTML and CSS before JavaScript runs.** Their content and ordinary navigation work with scripting disabled; they do not boot a client application merely to display initial content. |
| TB-02 | **`ArcForges.Web.App` is the only interactive browser application**, implemented in React and strict TypeScript as separate Account/Chat build profiles under [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008). |
| TB-03 | **Public pages are generated at build time using React/TypeScript and Node.js**, as static deployment artifacts. Their initial content and navigation work without JavaScript. |
| TB-04 | **The selected Web toolchain is Node.js/npm, Vite and React Router.** No Blazor browser host, React Native migration, runtime Node SSR or separate Node business backend is required. |
| TB-05 | **Web is checked against production browser assets, not .NET AOT properties.** Pin the Node/compiler/dependency toolchain, enforce browser compatibility and track initial and per-route transfer budgets. |
| TB-06 | **Browser JS/TS libraries are permitted under dependency, CSP, accessibility and performance policy.** This permission is confined to Web and does not relax pure-native Avalonia desktop requirements. |

---

## 3. `arcforges.com` — the marketing site

Its job is **Discover → Understand → Download**, then **Upgrade to Cloud**.

| # | Requirement |
|---|---|
| MS-01 | Discovery and direct download require no account. Product pages accurately separate native offline operations from Cloud account, service and AI requirements; download is never gated by purchase. |
| MS-02 | **Downloading never requires an account** ([C-05](../00-product-scope-and-portfolio.md#rule-c-05)). |
| MS-03 | First-level navigation is fixed: **Products · Cloud · Pricing · Download · Open Source · Docs**, with **Sign In** and a primary download action. |
| MS-04 | The home page states that product source is open, Cloud is authoritative for subscribed AI and synchronized content, and operator deployment values are private. It must not imply account-free local AI or a permanent standalone ArcNotes service. |
| MS-05 | **Every product has a page on a unified template**: what it is, who it is for, key capabilities, screenshots or demo, platform support, system requirements, download, documentation link, open-source link, and how the cloud enhances it. |
| MS-06 | **Product pages must never advertise a superseded product name.** `ArcCanvas`, `ArcMusic`, `ArcImage` and `ArcVideo` do not appear (**[D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002)**). |
| MS-07 | **A unified Download Center** presents every product, platform, architecture, package format, version, release channel, hash and signature information, and system requirements — from **one source of truth**. |
| MS-08 | Pricing is generated from the public projection of deployed offers, states that checkout determines final price/tax, and discloses AI recovery, burst/rate/concurrency and model limits. It never promises unbounded throughput, budget or storage. |
| MS-09 | **Open Source is a first-level official page**: licences (both boundaries per **[D-004](../../decisions/phase-1-foundation-decisions.md#rule-d-004)**), repositories, contribution guidance, third-party notices and the security policy. |
| MS-10 | **Self-hosting belongs in the documentation**, presented as a supported first-class deployment — not as a competing product line on the marketing site. |
| MS-11 | **A public roadmap commitment system is not built.** Direction may be communicated; dated feature promises are not ([OB-05](../10-distribution-update-and-support.md#rule-ob-05) in the distribution requirements). |
| MS-12 | **Support entry points are clear**: documentation, community, private support and security disclosure, each routing to the right object type (`§7` of the distribution requirements). |
| MS-13 | **A Security / Trust page** describes the security posture, the advisory feed, `security.txt` and the private disclosure route. |

### 3.1 Documentation, changelog and status

| # | Requirement |
|---|---|
| DS-01 | **`docs.arcforges.com` is independent from the first day**, covering every product, self-hosting and developer documentation, **versioned per product**. |
| DS-02 | **The changelog is a formal system**, generated from release metadata, per product and per version, and consistent with what the download page, updater and documentation state. |
| DS-03 | **`status.arcforges.com` reports per-capability state** — Identity, Sync, Storage, Search, Remote, Tasks, Managed AI, Billing ([CL-03](../03-cloud-services-and-sync.md#rule-cl-03)) — and **never contains customer-specific private data** ([IN-05](../10-distribution-update-and-support.md#rule-in-05) in the distribution requirements). |

### 3.2 One source of truth

| # | Requirement |
|---|---|
| <a id="rule-st-01"></a>ST-01 | **Product catalogue and release metadata have one source of truth.** A state where the home page, download page, documentation and release feed each show a different version is a defect, not a coordination problem. |
| <a id="rule-st-02"></a>ST-02 | **After a release is produced, the download page, product page, changelog, updater and documentation all work from the same version identity** ([RC-03](../10-distribution-update-and-support.md#rule-rc-03) in the distribution requirements). |
| <a id="rule-st-03"></a>ST-03 | **Pricing has one source of truth.** The marketing site and the account portal must never display different amounts. |

### 3.3 Internationalisation and access

| # | Requirement |
|---|---|
| <a id="rule-il-01"></a>IL-01 | **Multi-language is designed correctly from the first day**: locale-scoped URLs, correct alternate-language annotations, no client-side-only language switching, and no locale-based automatic redirect that traps a user. |
| <a id="rule-il-02"></a>IL-02 | **Mainland-China access must not depend on resources that are unreachable there.** No blocked fonts, script hosts, analytics or captcha providers on the public path. Region-specific infrastructure is a later, evidence-driven decision (**[D-023](../../decisions/phase-1-foundation-decisions.md#rule-d-023)** context). |
| <a id="rule-il-03"></a>IL-03 | **Public site performance is a formal product requirement**, not an aspiration: the above-the-fold content renders without waiting for a client runtime ([TB-01](#rule-tb-01)), and the site meets its stated web-vitals targets at the 75th percentile. |
| IL-04 | **Analytics are minimal and privacy-preserving** ([PV-05](../07-security-privacy-and-trust.md#rule-pv-05)). No cross-site advertising profile, no data sale, and no consent wall required for the basic site. |
| IL-05 | **Sharing and discovery metadata** — canonical URLs, structured metadata, social previews, sitemaps — is generated as part of the build. |

---

## 4. `account.arcforges.com` — the ArcForges Cloud Control Center

**Scope is strictly controlled: it manages the cloud. It never edits user content.**

| Section | Contents |
|---|---|
| **Overview** | Plan, cloud status, storage summary, AI usage summary, devices summary, attention items |
| **Workspace** | Single-owner personal workspace, data region and device association; no teams, members, invitations or protection-mode selector |
| **Storage** | Quota, usage by product, versions and trash, manage storage |
| **AI** | Included capacity/recovery, additional credits, service eligibility, usage history, Cloud model policy and extra-credit limits |
| **Devices** | Registered devices, presence, trust, revoke |
| **Remote Access** | Per-device remote enablement and per-capability grants |
| **Security** | Passkeys, recovery codes, sessions, security activity, API tokens, step-up |
| **Billing** | Plan, subscription state, renewal or end date, storage add-ons, credits, billing history summary, "Manage Billing →" |
| **Data & Privacy** | Export, cloud data deletion, account deletion, privacy controls, subprocessor link |

| # | Requirement |
|---|---|
| AP-01 | **The portal manages the cloud; it does not edit ArcNotes documents, ArcScope sessions or ArcSlate projects.** |
| AP-02 | **Every high-privilege operation lives here**: account, security, account deletion, billing, device revocation, remote-access grants (`§12` of the identity requirements). |
| AP-03 | **In-product account interfaces stay lightweight** and link here (`§12` there). |
| AP-04 | **Account deletion is available in the portal** and separately in every product, as required by store policy (`§10` there). |
| AP-05 | Included recoverable capacity and purchased credits are displayed separately, with recovery timing, active-term dependency, extra-credit consent and consumption history. |
| AP-06 | **Entitlement is shown with reasons**, not as a bare plan name ([ES-02](../04-commerce-entitlement-and-credits.md#rule-es-02) there). |
| AP-07 | **An Entitlement Explain view exists for support** ([ES-07](../04-commerce-entitlement-and-credits.md#rule-es-07) there). |
| AP-08 | **Invoices, receipts, payment details and billing-related refunds are handled by the Merchant of Record's portal** in V1; ArcForges does not reimplement an invoice engine or a tax-invoice editor (`§11` there). |
| AP-09 | **Storage-full and over-quota states are explained**, with the assurance that local work is safe ([ST-06](../03-cloud-services-and-sync.md#rule-st-06), [QU-03](../04-commerce-entitlement-and-credits.md#rule-qu-03) there). |
| AP-10 | **Remote access enablement in the portal cannot substitute for first-time enablement on the desktop** ([DP-07](arcchat-mobile-and-web.md#rule-dp-07) in the companion requirements). |

---

## 5. `chat.arcforges.com` — ArcChat Web

Specified in [`arcchat-mobile-and-web.md`](arcchat-mobile-and-web.md). Two boundaries repeated here because they are web-surface decisions:

| # | Requirement |
|---|---|
| CW-01 | **ArcChat Web and the account portal are strictly separate** ([WP-01](../../planning/work-packages/01-repository-reconciliation-and-target-layout.md#rule-wp-01) there), even though both are deployments of one codebase. Separate origins, separate cookies, separate authorization posture. |
| CW-02 | **ArcChat Web must not become an ArcNotes web editor** ([AR-02](arcchat-mobile-and-web.md#rule-ar-02) there). |

---

## 6. Security posture

| # | Requirement |
|---|---|
| SE-01 | **HTTPS only**, across every surface. |
| SE-02 | **Each deployment has its own CSP, host-only cookie, CSRF and explicit origin policy**, using the C# browser-session adapter adopted by [P2-003](../../decisions/phase-2-specification-decisions.md#rule-p2-003). |
| SE-03 | **Secrets are never compiled into the browser bundle.** |
| SE-04 | **Browser JavaScript receives no access/refresh credential.** Opaque Secure/HttpOnly cookie sessions are held and revoked server-side; cookie-authenticated writes require explicit antiforgery and origin checks. |
| SE-05 | **Cross-origin policy is an explicit allowlist.** Broad production CORS is prohibited. |
| SE-06 | **Uploads undergo content-type, size and format validation with a quarantine area**, and are never executed server-side ([EX-06](../03-cloud-services-and-sync.md#rule-ex-06) in the cloud requirements). |
| SE-07 | **Access tokens must be redacted from realtime transport logs.** |
| <a id="rule-se-08"></a>SE-08 | **Public share links do not exist in V1** (`§18` of the cloud requirements). Links are authenticated and private ([I-279](../01-normative-glossary-and-invariants.md#rule-i-279)). |
| SE-09 | **A web session is more conservative than a desktop session**, and an unknown browser does not immediately hold high-risk approval capability ([OF-07](arcchat-mobile-and-web.md#rule-of-07), [OF-08](arcchat-mobile-and-web.md#rule-of-08) in the companion requirements). |

---

### 6.1 Generated contracts and independent engineering

| # | Requirement |
|---|---|
| <a id="rule-web-01"></a>WEB-01 | **C# public DTOs/endpoints generate OpenAPI 3.1, JSON Schema and the TypeScript SDK.** No duplicate handwritten TS business contract or React-specific business backend; runtime response validation and version compatibility are required. |
| <a id="rule-web-02"></a>WEB-02 | **Exact values survive C# and JavaScript.** Int64 revisions/token counts/microcredits and decimal prices use the specified canonical string wire encoding; UI display never rounds accounting values through JS Number. |
| <a id="rule-web-03"></a>WEB-03 | **One Web npm workspace can be developed independently.** Windows win.slnx includes its esproj; non-Windows developers run Node/npm in the Web directory without loading the managed/native solution. |
| <a id="rule-web-04"></a>WEB-04 | **Fixture development and real integration are separate modes.** Tests of the generated SDK against real C# APIs, browser sessions, PostgreSQL state and approved provider test flows are release evidence; fixture success alone is not. |
| <a id="rule-web-05"></a>WEB-05 | **Realtime and streaming have generated event contracts and recovery tests**, including byte offsets, reconnect/gaps, duplicate delivery and loss of authorization. |
| <a id="rule-web-06"></a>WEB-06 | **The browser handles API uncertainty explicitly.** Idempotency keys, revision conflicts, rate limits, pending checkout confirmation and expired sessions cannot be replaced with unconditional optimistic success. |

### 6.2 Consumer visual and interaction quality

| # | Requirement |
|---|---|
| <a id="rule-uxw-01"></a>UXW-01 | **A shared owned design system governs Site, Account and Chat**: typography, spacing, color, iconography, light/dark themes, responsive layout and motion. React/shadcn components are adapted to this system; shipping an unreviewed starter theme is insufficient. |
| <a id="rule-uxw-02"></a>UXW-02 | **Core screens have approved visual baselines**: home/product/pricing, subscription/checkout return, account overview, usage/capacity, conversation and task approval. Validate desktop and narrow browser layouts and long translated text. |
| <a id="rule-uxw-03"></a>UXW-03 | **Loading, empty, error, pending, disabled, expired and recovery states are designed and tested.** Server truth controls subscription/credit/task status; animations and placeholders do not imply authority. |
| <a id="rule-uxw-04"></a>UXW-04 | **Motion supports comprehension**, honors reduced-motion preferences and never hides focus, delays primary actions or blocks initial content. Keyboard, screen reader and touch behavior are acceptance conditions. |
| <a id="rule-uxw-05"></a>UXW-05 | **Production artifacts meet the existing public Web Vitals target and committed application budgets.** Visual review, interaction/browser tests and performance evidence are all required. |

---


## 7. Content and data concepts

The web system must be able to express:

```
Product · ProductCategory · ProductStatus
Platform · Architecture
Release · ReleaseChannel · DownloadArtifact
ProductScreenshot · ProductDemo · Feature
CloudPlanDisplay · PricingDisplay
ChangelogEntry
DocumentationProduct · DocumentationVersion
Locale · Announcement · SupportCategory
LegalDocument · LegalDocumentVersion · SecurityNotice
ServiceComponent · StatusIncident
```

---

## 8. Key user paths

Each must be complete and testable:

1. **Discover → product page → download**, with no account.
2. **Download → install → native product entry**, with honest sign-in requirements; cached work and native capture/render operate under their product-specific offline contract.
3. **Sign up → create passkey → single-owner workspace → activate service → synchronized work**, with explicit native raw-media/capture upload choices.
4. **Pricing → sign in → checkout → confirming → entitlement active** (`§4` of the commerce requirements).
5. **Sign in → account portal → manage storage, AI, devices, remote access, security, billing.**
6. **Enable remote access on desktop → manage per-capability grants in the portal → approve from a companion surface.**
7. **Export workspace data → download.**
8. **Delete selected Cloud data**, or **delete account**, with a retention/propagation preview and protection of unsent work. Deletion semantics distinguish device caches from independent native capture/media files.
9. **Read documentation for a specific product version.**
10. **Check status during an incident**, on infrastructure independent of the cloud.
11. **Report a security issue** through the private route.
12. **Find and read the changelog for the version currently installed.**

---

## 9. Non-goals

The web presence is **not**: an ArcNotes, ArcScope or ArcSlate web editor; a second account application at a secondary path; a public content-sharing platform in V1; a public roadmap commitment system; a heavy client application on public marketing pages.

---

## 10. Acceptance scenarios

**Static rendering** — a public marketing page renders its above-the-fold content with the client runtime blocked entirely.

**Download without account** — every product, platform and architecture is downloadable with no sign-in, and hashes and signatures are published.

**One source of truth** — the home page, product page, download page, changelog, documentation and update feed all report the same current version.

**Pricing consistency** — the marketing site and the account portal display identical amounts, and both state that final price and tax are determined at checkout.

**Account portal boundaries** — the portal manages storage, AI, devices, remote access, security, billing and data; it offers no document, session or project editing.

**Redirect** — `arcforges.com/account` permanently redirects to the canonical origin, and no second account application exists behind it.

**Origin isolation** — the chat surface and the account surface do not share authentication cookies; no broad parent-domain cookie exists.

**Status independence** — a full cloud outage leaves the status page reachable and accurate.

**Mainland access** — the public site loads with no blocked third-party resources on the critical path.

**Localization** — a locale-scoped page carries correct alternate-language annotations, and no automatic redirect traps a user in the wrong locale.

**Security** — the browser bundle contains no secret; CORS is an explicit allowlist; an unknown browser cannot immediately perform a high-risk approval.

**Commerce** — checkout requires sign-in and a selected workspace; the success redirect shows a confirming state and grants nothing until verified provider events arrive.

---

**Generated-client interoperability** — C# emits the contract, TS regenerates without handwritten DTOs, exact large integers/decimals round-trip, and stale clients follow the compatibility window.

**Independent developer workflow** — Windows opens/builds the Web esproj in win.slnx; Linux/macOS run the same npm commands directly. Real-browser API and fixture modes are distinguishable.

**Visual acceptance** — approved Site, subscription and Chat layouts pass theme, narrow-screen, locale, asynchronous-state, keyboard and reduced-motion checks.

---

## 11. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 2` | The complete web presence: surface layout, marketing site positioning and navigation, product pages, download centre, account portal scope, pricing, open source, documentation, changelog, status, support, security, internationalisation, mainland access, performance, analytics, discovery metadata, key paths and content concepts |
| `I4 §Stage 7 §54–56` | ArcChat Web as a cloud surface, separate from the account portal |
| `I4 §Stage 5` | Download and release metadata as one source of truth |
| `I3 §18` | Historical Web input; current technology follows [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008), with origin/security principles retained |
| **[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)** | Static public pages and one application; technology amended by [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) |
| **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)** | The twelve-entry surface inventory and "a hostname is not an application" |
| **[D-015](../../decisions/phase-1-foundation-decisions.md#rule-d-015)** | Canonical account portal origin and boundary policy |
| **[D-002](../../decisions/phase-1-foundation-decisions.md#rule-d-002)** | Superseded product names never appear |
