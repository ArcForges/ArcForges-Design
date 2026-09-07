# Web Architecture

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Architecture
> Governing authority: [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) amends [D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007); [D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014) defines the surfaces and [D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015) the canonical account origin
> Companions: [Web requirements](../requirements/products/arcforges-web.md), [Web toolchain and SDK](25-web-toolchain-and-sdk.md), [security](08-security-architecture.md), [Cloud](05-cloud-architecture.md)

React/TypeScript implements the browser experiences. Node.js provides the shared build/development toolchain. One existing ASP.NET Core Cloud host owns the APIs, browser session adapter, billing, persistence and single agent Harness.

## 1. Build outputs

```text
src/Web — one npm workspace and one Windows esproj
├─ ArcForges.Web.Site — React/TS build-time pre-rendering
│     → public HTML/CSS + bounded enhancement assets
└─ ArcForges.Web.App — React/TS application
      ├─ Account build profile → account.arcforges.com
      └─ Chat build profile    → chat.arcforges.com
          ↓ generated TypeScript SDK / same-origin edge routes
       existing ASP.NET Core Cloud.Host
```

| # | Rule |
|---|---|
| <a id="rule-bo-01"></a>BO-01 | **Public content is present in static HTML/CSS before JavaScript runs.** Marketing, pricing information, legal, docs and downloads are usable with scripting disabled; enhancements do not hide initial content. |
| <a id="rule-bo-02"></a>BO-02 | **Static pages are deployment artifacts, not a second account/chat application.** |
| <a id="rule-bo-03"></a>BO-03 | **`ArcForges.Web.App` is the one interactive browser codebase**, built as Account and Chat profiles with their own route graphs. |
| <a id="rule-bo-04"></a>BO-04 | **React DOM runs browser JavaScript emitted from strict TypeScript.** Web has no .NET/WASM host or Web AOT setting. Desktop and mobile keep their separately specified C# runtime postures. |
| <a id="rule-bo-05"></a>BO-05 | **Use Node.js/npm, React Router and Vite as specified in the toolchain companion.** Build-time static rendering is allowed; runtime Node SSR, Blazor modes, React Native and an additional Node business service are outside this baseline. |
| <a id="rule-bo-06"></a>BO-06 | **Browser code may use the selected JS/TS ecosystem under dependency and bundle policy.** Browser capabilities do not authorize WebView, DOM or JavaScript UI inside native desktop applications. |

## 2. Static generation

Content, catalogue, release manifests, legal versions, locales and an approved public pricing snapshot feed the Node build. React Router pre-renders the complete public URL inventory. No build reads a live pricing endpoint, customer database or arbitrary provider API. Private pricing policy is reduced to an approved public offer projection before it becomes a build input.

| # | Rule |
|---|---|
| <a id="rule-sg-01"></a>SG-01 | **Product catalogue and release metadata have one source of truth.** The site consumes versioned content/artifacts and never invents a release. |
| <a id="rule-sg-02"></a>SG-02 | **Pricing consumes a versioned public offer projection.** Its version/effective time is visible; live checkout revalidates price and eligibility. Stale public HTML never authorizes a price, grant or debit. |
| <a id="rule-sg-03"></a>SG-03 | **Above-the-fold content and ordinary navigation work without scripts.** Optional animation respects reduced-motion settings and cannot delay meaningful paint. |
| <a id="rule-sg-04"></a>SG-04 | **Locale-scoped URLs, canonical/alternate-language metadata, sitemap and stable versioned docs** are generated together; no trapping automatic language redirect. |
| <a id="rule-sg-05"></a>SG-05 | **Self-host licensed fonts/icons and required assets where practical.** No globally unreachable third-party resource is on the critical path. |
| <a id="rule-sg-06"></a>SG-06 | **Assets are content-hashed; HTML has a short cache lifetime.** Old assets remain available for the supported client window. |
| <a id="rule-sg-07"></a>SG-07 | **Same inputs/toolchain yield the same output**, including deterministic timestamps/order and locale handling; record any toolchain nondeterminism explicitly. |

## 3. React application and design system

| # | Rule |
|---|---|
| <a id="rule-wa-01"></a>WA-01 | **One application codebase, two explicit build profiles.** Shared shell, error handling, locale and UI primitives have one implementation; account/chat feature route imports are selected at build time. Route exclusion is a bundle boundary, never authorization. |
| <a id="rule-wa-02"></a>WA-02 | **Origins have independent sessions, storage and in-memory state.** A workspace/user switch aborts old requests and clears scoped queries; late replies cannot contaminate the new context. |
| <a id="rule-wa-03"></a>WA-03 | **C# DTOs and endpoint metadata generate OpenAPI, then TS types, SDK and runtime validators.** No UI model or database entity becomes a wire contract. |
| <a id="rule-wa-04"></a>WA-04 | **React consumes the generated Fetch SDK through one transport wrapper.** C# clients retain generated Refit; its AOT entry-point rule does not describe JavaScript. |
| <a id="rule-wa-05"></a>WA-05 | **Realtime uses the official JS SignalR client with generated JSON payload validation.** Stream byte positions, sequence gaps and backfill follow the shared contracts. |
| <a id="rule-wa-06"></a>WA-06 | **Browser authentication is an opaque server-side cookie session**, resolved in §5. Browser JavaScript holds no bearer/refresh credential and performs no refresh-token loop. |
| <a id="rule-wa-07"></a>WA-07 | **TanStack Query caches projections and invalidates them on authoritative changes.** Entitlement events and optimistic presentation never approve a paid action or settle a charge. |
| <a id="rule-wa-08"></a>WA-08 | **Route chunks, initial transfer, first usable interaction and sustained chat memory have recorded budgets.** [WP-06](../planning/work-packages/06-aot-jit-and-wasm-publish-proof.md#rule-wp-06) establishes the production baseline; later releases enforce regressions. |
| <a id="rule-wa-09"></a>WA-09 | **Own a coherent ToC design system:** type scale, spacing, colors, contrast, icons, responsive layout, light/dark theme and restrained motion. Site, subscription and chat are designed together; a default component-library theme is not design acceptance. |
| <a id="rule-wa-10"></a>WA-10 | **Every major component specifies normal, loading, empty, error, disabled, pending and recovery states.** Account views distinguish active term, included capacity, purchased credits and rate limitation using server-provided reasons; skeletons never suggest a successful purchase. |
| <a id="rule-wa-11"></a>WA-11 | **A test-only UI catalogue and representative visual baselines precede page completion.** Cover pricing/checkout return, account overview, quota/capacity, conversation/streaming, task approval and mobile-width layouts, with human visual acceptance plus automated interaction checks. |

Shared components live in `packages/ui`. React state models navigation and presentation; the generated SDK and small language-specific clients own transport/recovery. No React component embeds supplier rates, provider keys, agent execution or payment authority.

## 4. Surface and routing matrix

| Surface | Output and route | Authority |
|---|---|---|
| `arcforges.com` | Static public pages | Versioned content; no login requirement |
| `www.arcforges.com` | Permanent redirect | Canonical public origin |
| `account.arcforges.com` | Account static JS/HTML assets; `/api/*`, `/session/*`, `/realtime/*` forwarded to Cloud | Canonical account surface |
| `chat.arcforges.com` | Chat static JS/HTML assets; same route categories forwarded to Cloud | Independent browser session, same Cloud business services |
| `docs.arcforges.com` | Static versioned documentation | Independent of Cloud availability |
| `status.arcforges.com` | Independently hosted status | Separate failure domain and emergency alternate URL |
| `downloads.arcforges.com` / `updates.arcforges.com` | Signed artifacts/manifests | Existing distribution authority |
| `api.arcforges.com` | Public Cloud HTTP API | Native/mobile/public clients use their declared auth schemes |
| `ops.arcforges.com` | Private operator surface | Separate operator identity and route allowlist; no consumer bundle access |
| `notify.arcforges.com` / optional `news.arcforges.com` | Message links / content | Not additional consumer applications |

| # | Rule |
|---|---|
| <a id="rule-sm-01"></a>SM-01 | **`arcforges.com/account` permanently redirects to the canonical account origin.** It does not serve a second account UI. |
| <a id="rule-sm-02"></a>SM-02 | **Each origin has explicit CSP, cookie, CORS, CSRF and edge route rules.** The edge forwards only declared routes to the configured Cloud service and preserves a validated external-origin identity. Untrusted forwarded headers cannot select a session realm. |
| <a id="rule-sm-03"></a>SM-03 | **No parent-domain auth cookie or cross-origin credential sharing.** Browser requests use same-origin allowlisted routes with fixed Cloud targets. The browser edge never exposes native bearer issuance/refresh routes; browser login/recovery returns the safe cookie-session projection. The native public API does not accept browser cookies as bearer credentials. |
| <a id="rule-sm-04"></a>SM-04 | **Static public and status surfaces survive Cloud failure.** Their already published content remains available; current checkout and live account state truthfully report unavailability. |
| <a id="rule-sm-05"></a>SM-05 | **SPA fallback applies only to declared UI navigation.** API/session errors keep their JSON/status, missing assets remain 404, protected responses are never cached as HTML, and direct account/chat deep links load the correct profile. |

## 5. Browser session architecture — P2-003 resolved

**Selected deployment.** A same-origin browser-session adapter (BFF boundary) runs as C# endpoint mapping/authentication inside the existing Cloud host. It invokes the same application services as the public API. It is not a new host, network hop to another business service, or proxy carrying stored user refresh tokens.

| # | Rule |
|---|---|
| <a id="rule-au-01"></a>AU-01 | **Desktop/mobile bearer sessions retain short access lifetimes and refresh rotation. Browser sessions instead use an opaque cookie handle**, with server-enforced idle and absolute expiry and immediate revocation checks. Expiry requires reauthentication; there is no browser refresh credential. |
| <a id="rule-au-02"></a>AU-02 | **No access/refresh/session secret is returned in browser JSON, persisted in Web Storage, embedded in HTML, or attached to URLs.** The browser session handle is delivered only by a Secure, HttpOnly, Path=/, host-only `__Host-` cookie with SameSite=Lax; cookie lifetime never exceeds server expiry. |
| <a id="rule-au-03"></a>AU-03 | **[P2-003](../decisions/phase-2-specification-decisions.md#rule-p2-003) is ADOPTED under [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008).** The implementation uses the cookie-session design here; [WP-22](../planning/work-packages/22-identity-workspace-and-device.md#rule-wp-22) builds the adapter and [WP-48](../planning/work-packages/48-account-portal.md#rule-wp-48) proves the full account experience. A change of deployment requires a new recorded decision. |
| <a id="rule-au-04"></a>AU-04 | **Web session lifetime/trust is more conservative than native-device sessions.** Idle and absolute bounds are versioned server policy; browser activity cannot extend absolute expiry or increase device trust. |
| <a id="rule-au-05"></a>AU-05 | **A new browser has the lowest applicable trust.** Creating a browser device/installation during successful authentication never grants desktop local-tool access or high-risk approval authority. |
| <a id="rule-au-06"></a>AU-06 | **Sensitive actions require the existing server-side step-up operation classes.** A biometric device unlock, visible confirmation dialog or frontend role flag is not step-up evidence. |
| <a id="rule-au-07"></a>AU-07 | **Passkeys remain primary, with existing email verification/recovery.** Use a server challenge tied to the pre-auth flow, expected origin and RP ID. Account and Chat authenticate independently; redirects carry no credentials and use an exact allowlist. |
| <a id="rule-au-08"></a>AU-08 | **CSRF checks are explicit for every cookie-authenticated unsafe operation**, including JSON, multipart, login/logout and SignalR negotiation. Require the ASP.NET antiforgery request header plus exact Origin validation; SameSite and CORS alone are insufficient. Refresh the antiforgery request token after login without rotating a session on every request. |
| <a id="rule-au-09"></a>AU-09 | **SignalR/WebSocket handshakes enforce the origin allowlist and live session.** Browser connections use WebSockets-only with skipNegotiation; blocked upgrades use bounded public HTTP recovery, not SignalR long polling. Disabled browser negotiation routes cannot bypass CSRF or issue credentials. Live connections revalidate expiry/revocation and close at the applicable deadline; reconnect cannot extend it. |
| <a id="rule-au-10"></a>AU-10 | **All Cloud replicas use the same authoritative session store and shared protected Data Protection key ring.** Authentication has no session-affinity or replica-local state requirement. The browser's WebSocket-only transport and HTTP fallback avoid a hidden negotiate/long-poll affinity requirement. Key retention covers live antiforgery/cookie material and follows deployment secret policy. |

**Storage and lifecycle.** [Cloud data model §identity.session](data-model/01-cloud-data-model.md#browser-session-storage) defines native/browser credential exclusivity, hashed handles, origin binding, idle/absolute expiry, browser-device creation, lookup indices and revocation. Public session/bootstrap/logout endpoint shapes are recorded in the [operation catalogue](contracts/01-public-api-operations.md#browser-session-operations). Cookies carry a cryptographically random handle; neither business state nor an authorization snapshot is trusted from the client.

Concurrent browser tabs share only their own origin's cookie session. No periodic credential rotation occurs per request, so ordinary requests cannot create a refresh race. Login invalidates the pre-auth flow; logout/revocation/expiry invalidates the server record before clearing the cookie. An already admitted command retains its normal command/result semantics; revocation does not pretend to undo a committed operation. A subsequent command fails authorization.

## 6. Content security

| # | Rule |
|---|---|
| <a id="rule-cs-01"></a>CS-01 | **Production CSP permits only the required hashed/self-hosted scripts and explicitly approved providers**, without unsafe-eval or a default unsafe-inline allowance. Vite HMR/development exceptions never reach production. Any build-injected inline bootstrap is externalized or has a build-generated exact hash. |
| <a id="rule-cs-02"></a>CS-02 | **Everything shipped to a browser is public.** Bundle, source maps, runtime config, static props and errors carry no private policy, supplier pricing or secrets. |
| <a id="rule-cs-03"></a>CS-03 | **Cross-origin permissions are explicit allowlists.** Cookie-authenticated business traffic is same-origin; native bearer endpoints retain separate policy. |
| <a id="rule-cs-04"></a>CS-04 | **Uploads use the existing size/type/quarantine/resource authorization flow.** Neither a React preview nor a generated validator establishes file safety. |
| <a id="rule-cs-05"></a>CS-05 | **Logs redact cookies, Authorization, antiforgery material, prompts and chat/tool contents.** Browser error telemetry uses sanitized identifiers and user consent rules. |
| <a id="rule-cs-06"></a>CS-06 | **User Markdown/content is rendered from a safe structured subset.** Raw user HTML is never passed to React unsafe HTML APIs. Active documents/HTML/SVG previews use an isolated authorized surface or a download flow, never script execution in Account/Chat origin. |
| <a id="rule-cs-07"></a>CS-07 | **No public share links in V1.** Private links and resource fetches authenticate and authorize at access. |
| <a id="rule-cs-08"></a>CS-08 | **Resource denials do not disclose forbidden existence.** Signed/object URLs remain short-lived, scoped and outside application logs. |

## 7. Offline and resilience

| # | Rule |
|---|---|
| <a id="rule-or-01"></a>OR-01 | **Web offline support is bounded.** Preserve the current unsent input through a transient connection loss in memory; show unavailable actions and require a live session before submission. No local model, autonomous browser agent, offline payment or authoritative offline mutation is added. |
| <a id="rule-or-02"></a>OR-02 | **Cloud failure leaves the loaded shell usable with honest unavailable states.** Successful server acknowledgement is distinguished from pending work; a retry preserves the command identity. |
| <a id="rule-or-03"></a>OR-03 | **Realtime failure falls back to bounded HTTP polling and sequence backfill.** Never resubmit an AI turn because its stream disconnected. |
| <a id="rule-or-04"></a>OR-04 | **Public static pages remain available during a Cloud outage.** |
| <a id="rule-or-05"></a>OR-05 | **Logout, revocation and user/workspace changes clear sensitive UI caches and abort requests.** No default persistent query cache or service worker stores authenticated data; background tabs cannot repopulate a cleared scope. |

## 8. Accessibility, localisation and visual performance

| # | Rule |
|---|---|
| <a id="rule-al-01"></a>AL-01 | **WCAG 2.2 AA on core static and application workflows**, with automated checks and assistive-technology verification. |
| <a id="rule-al-02"></a>AL-02 | **Keyboard-only completion of every core workflow**, visible focus and correct dialog focus restoration. |
| <a id="rule-al-03"></a>AL-03 | **All visible strings are localisable**, including server reason-code presentation, validation, streaming/status messages and generated pages. |
| <a id="rule-al-04"></a>AL-04 | **Canonical data, localised display.** No locale parsing of IDs, exact amounts or timestamps on the wire. |
| <a id="rule-al-05"></a>AL-05 | **Public pages meet the existing p75 LCP ≤2.5 s, INP ≤200 ms and CLS ≤0.1 requirement**, with a declared device/network profile for lab checks and production field verification. |
| <a id="rule-al-06"></a>AL-06 | **Application route/bundle/startup/memory budgets are committed and enforced**, measured on production assets and the supported browser/device matrix. A development server result is not evidence. |
| <a id="rule-al-07"></a>AL-07 | **Visual acceptance includes narrow screens, touch targets, long translated text, dark/light themes and reduced motion.** Do not trade readability, focus order or error clarity for animation. |

## 9. Analytics

| # | Rule |
|---|---|
| <a id="rule-an-01"></a>AN-01 | **Minimal privacy-preserving analytics** under the existing privacy requirements. |
| <a id="rule-an-02"></a>AN-02 | **No cross-site advertising profile or data sale.** |
| <a id="rule-an-03"></a>AN-03 | **Basic static use requires no consent wall**, because required page behavior does not depend on consent-bearing tracking. |
| <a id="rule-an-04"></a>AN-04 | **Application telemetry contains no user content** and follows the applicable consent setting. |

## 10. Build and deployment

| # | Rule |
|---|---|
| <a id="rule-bd-01"></a>BD-01 | **Build once, promote the same release set.** Node builds are deterministic jobs, not production request handlers. |
| <a id="rule-bd-02"></a>BD-02 | **Atomic deployment per surface with retained previous assets, manifests and compatible security headers.** |
| <a id="rule-bd-03"></a>BD-03 | **C# contracts → schema compatibility → TS SDK → Web build** is the enforced producer/consumer order. Old clients remain supported for the declared window; simultaneous frontend/backend deployment is not a compatibility strategy. |
| <a id="rule-bd-04"></a>BD-04 | **Cached old clients receive a supported upgrade path.** Chunk failure, API incompatibility and draft preservation have explicit UI behavior; no infinite reload loop. |
| <a id="rule-bd-05"></a>BD-05 | **Production Node-built assets and browser behavior are Web release evidence.** A .NET/WASM publish is neither required nor an alternative proof. |
| <a id="rule-bd-06"></a>BD-06 | **Windows uses win.slnx + one esproj; other platforms use npm in src/Web.** Cloud.csproj and the portable managed solution never depend on that esproj. See the [toolchain workflow](25-web-toolchain-and-sdk.md). |

## 11. Non-goals

No ArcNotes/ArcScope/ArcSlate browser editor, public sharing, React Native migration, desktop WebView, browser agent authority, supplier key handling, private policy bundle, or separate Node business backend is introduced. Private operator functions remain outside consumer deployment profiles.

## 12. Traceability

| Source | Consumed as |
|---|---|
| [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) and the dated [D-007](../decisions/phase-1-foundation-decisions.md#rule-d-007) amendment | React/TS, Node/npm, C# generated SDK, esproj/CLI split and supersession of Blazor-only Web requirements |
| [D-014](../decisions/phase-1-foundation-decisions.md#rule-d-014) / [D-015](../decisions/phase-1-foundation-decisions.md#rule-d-015) | Existing surface inventory, one account/chat codebase, canonical account origin and isolated browser sessions |
| [D-009](../decisions/phase-1-foundation-decisions.md#rule-d-009) / [D-021](../decisions/phase-1-foundation-decisions.md#rule-d-021) | C# authored public contracts; generated Apache SDK and wire validation separated from AGPL product UI |
| [P2-003](../decisions/phase-2-specification-decisions.md#rule-p2-003) resolution | Same-origin C# browser-session adapter, live server sessions, CSRF and revocation |
| Current product requirements | Account, paid subscription/capacity and Cloud ArcChat scope; static public content and quality requirements |

The preserved input descriptions of Blazor are historical input. They are superseded for Web by the user's [P2-008](../decisions/phase-2-specification-decisions.md#rule-p2-008) decision, not implementation requirements.
