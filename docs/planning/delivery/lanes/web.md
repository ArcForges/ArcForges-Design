# Web — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Static site, shared consumer design system, Account portal and the ArcScope Web companion (workspace, simulator console, assistant).

Tasks: 34 · Owning repositories: Web · Integration owner(s): Web integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [WEB.01](#task-web-01) | C# static Site generator (Razor HtmlRenderer) and determinism engine | producer | L | [WEB.40](#task-web-40) (artifact) | not-started |
| [WEB.02](#task-web-02) | Versioned public content and pricing inputs (catalogue.json) | feature | M | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.03](#task-web-03) | Rendering and performance | feature | M | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.04](#task-web-04) | Internationalisation | feature | M | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.05](#task-web-05) | Documentation, downloads and legal surfaces | feature | M | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.06](#task-web-06) | Accessibility and analytics | feature | S | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.07](#task-web-07) | Independence and atomic deployment | release | S | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.08](#task-web-08) | Owned consumer design system (Razor class library ArcForges.Web.Ui) | producer | L | [WEB.40](#task-web-40) (artifact) | not-started |
| [WEB.09](#task-web-09) | Verify the owned Site artifact and real integration | integration | S | [WEB.02](#task-web-02) (artifact), [WEB.03](#task-web-03) (artifact), [WEB.04](#task-web-04) (artifact), [WEB.05](#task-web-05) (artifact), [WEB.06](#task-web-06) (artifact), [WEB.07](#task-web-07) (artifact), [WEB.08](#task-web-08) (artifact) | not-started |
| [WEB.10](#task-web-10) | Account Blazor shell: route graph, deployment-profile selection, generated C# SDK wiring | producer | XL | [WEB.08](#task-web-08) (artifact), [CON.07](contracts.md#task-con-07) (contract), [WEB.40](#task-web-40) (artifact), [PRF.11](runtime-proofs.md#task-prf-11) (artifact) | not-started |
| [WEB.11](#task-web-11) | Real browser session and step-up acceptance | feature | L | [CLOUD.19](cloud.md#task-cloud-19) (artifact), [WEB.10](#task-web-10) (artifact) | not-started |
| [WEB.12](#task-web-12) | Account and security surfaces | feature | M | [WEB.11](#task-web-11) (artifact) | not-started |
| [WEB.13](#task-web-13) | Workspace, storage and usage | feature | M | [WEB.10](#task-web-10) (artifact) | not-started |
| [WEB.14](#task-web-14) | Subscription, capacity, credits and hosted checkout | feature | L | [WEB.10](#task-web-10) (artifact), [CON.08](contracts.md#task-con-08) (contract) | not-started |
| [WEB.15](#task-web-15) | Data export and deletion | feature | M | [WEB.10](#task-web-10) (artifact), [CON.22](contracts.md#task-con-22) (contract) | not-started |
| [WEB.16](#task-web-16) | Origin security and performance (account) | feature | M | [WEB.10](#task-web-10) (artifact) | not-started |
| [WEB.17](#task-web-17) | Offline, degradation and accessibility (account) | feature | M | [WEB.12](#task-web-12) (artifact), [WEB.13](#task-web-13) (artifact), [WEB.14](#task-web-14) (artifact), [WEB.15](#task-web-15) (artifact) | not-started |
| [WEB.18](#task-web-18) | Verify the owned Account artifact and real integration | integration | M | [WEB.11](#task-web-11) (artifact), [WEB.12](#task-web-12) (artifact), [WEB.13](#task-web-13) (artifact), [WEB.14](#task-web-14) (artifact), [WEB.15](#task-web-15) (artifact), [WEB.16](#task-web-16) (artifact), [WEB.17](#task-web-17) (artifact), [WEB.29](#task-web-29) (artifact) | not-started |
| [WEB.19](#task-web-19) | Chat shell: route composition and design-system integration | producer | L | [WEB.08](#task-web-08) (artifact), [WEB.10](#task-web-10) (artifact) | not-started |
| [WEB.20](#task-web-20) | Conversation and generated output streams | feature | L | [WEB.19](#task-web-19) (artifact), [PRF.11](runtime-proofs.md#task-prf-11) (artifact) | not-started |
| [WEB.21](#task-web-21) | Tasks, approval and steering | feature | L | [WEB.19](#task-web-19) (artifact) | not-started |
| [WEB.22](#task-web-22) | Artifacts and sandboxing | feature | M | [WEB.19](#task-web-19) (artifact) | not-started |
| [WEB.23](#task-web-23) | One-application remote control | feature | M | [WEB.19](#task-web-19) (artifact) | not-started |
| [WEB.24](#task-web-24) | Offline, degradation and accessibility (chat) | feature | M | [WEB.20](#task-web-20) (artifact), [WEB.21](#task-web-21) (artifact), [WEB.22](#task-web-22) (artifact), [WEB.23](#task-web-23) (artifact) | not-started |
| [WEB.25](#task-web-25) | Performance budgets (chat) | feature | S | [WEB.19](#task-web-19) (artifact), [PRF.11](runtime-proofs.md#task-prf-11) (artifact) | not-started |
| [WEB.26](#task-web-26) | Verify the owned Chat artifact and real integration | integration | M | [WEB.20](#task-web-20) (artifact), [WEB.21](#task-web-21) (artifact), [WEB.22](#task-web-22) (artifact), [WEB.23](#task-web-23) (artifact), [WEB.24](#task-web-24) (artifact), [WEB.25](#task-web-25) (artifact), [WEB.32](#task-web-32) (artifact), [WEB.33](#task-web-33) (artifact) | not-started |
| [WEB.27](#task-web-27) | Real CF Harness generation/tool loop observed end to end in the browser | integration | M | [WEB.20](#task-web-20) (artifact), [WEB.21](#task-web-21) (artifact), [HAR.00](harness.md#task-har-00) (artifact), [HAR.03](harness.md#task-har-03) (artifact) | not-started |
| [WEB.28](#task-web-28) | Real desktop tool dispatch from the browser companion | integration | M | [WEB.21](#task-web-21) (artifact), [WEB.23](#task-web-23) (artifact), [DEV.02](device-bridge.md#task-dev-02) (artifact), [DEV.03](device-bridge.md#task-dev-03) (artifact), [DEV.06](device-bridge.md#task-dev-06) (artifact), [DEV.07](device-bridge.md#task-dev-07) (artifact), [DEV.12](device-bridge.md#task-dev-12) (artifact) | not-started |
| [WEB.29](#task-web-29) | Real commerce/policy provider evidence for the account portal | integration | M | [WEB.14](#task-web-14) (artifact), [COM.14](commerce.md#task-com-14) (artifact), [POL.08](policy.md#task-pol-08) (artifact) | not-started |
| [WEB.30](#task-web-30) | Real Blazor WebAssembly Web client against deployed browser session/PublicApi/realtime | integration | M | [CLOUD.19](cloud.md#task-cloud-19) (artifact), [CLOUD.26](cloud.md#task-cloud-26) (artifact), [CLOUD.29](cloud.md#task-cloud-29) (artifact), [WEB.07](#task-web-07) (artifact), [WEB.14](#task-web-14) (artifact), [WEB.19](#task-web-19) (artifact), [PRF.11](runtime-proofs.md#task-prf-11) (artifact) | not-started |
| [WEB.31](#task-web-31) | Full browser-support.v1 matrix across all Web-facing outputs | integration | M | [OPS.05](operations.md#task-ops-05) (artifact), [WEB.07](#task-web-07) (artifact), [WEB.14](#task-web-14) (artifact), [WEB.19](#task-web-19) (artifact), [WEB.30](#task-web-30) (artifact) | not-started |
| [WEB.32](#task-web-32) | ArcScope workspace in the Web companion: library and reports | feature | L | [WEB.19](#task-web-19) (artifact), [CON.24](contracts.md#task-con-24) (contract) | not-started |
| [WEB.33](#task-web-33) | Cloud simulator console in the Web companion | feature | M | [WEB.19](#task-web-19) (artifact), [CON.21](contracts.md#task-con-21) (contract) | not-started |
| [WEB.40](#task-web-40) | Blazor migration of the existing Web (C# static Site, Blazor WebAssembly profiles, C# policy) | producer | XL | [GOV.03](governance.md#task-gov-03) (artifact), [CON.07](contracts.md#task-con-07) (contract) | not-started |

## Tasks

<a id="task-web-01"></a>

### WEB.01 — C# static Site generator (Razor HtmlRenderer) and determinism engine

**Outcome.** The C# static Site generator (ArcForges.Web.Site, first-party Razor HtmlRenderer, build time, with no WebAssembly or runtime JavaScript on public pages per [TB-01](../../../architecture/18-editing-and-rich-content.md#rule-tb-01)) generates the full public locale/URL inventory, documentation versions, sitemap, metadata and redirects, deterministically, with no Account/Chat profile bundle or private config leaking into the static output.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-01` and ledger record `ledger/tasks/web-01.md` in the Plan repository; task branch `task/web-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-47.00](../../work-packages/47-static-public-site.md#rule-wp-47.00) — full |
| Provides | web-static-generator |
| Start prerequisites | **artifact** [WEB.40](#task-web-40) — C# static Site generator and migrated public page inventory (WEB.40 parity port). *Why:* this task generalises the generator that the migration delivers; apps/site retires only after that parity port |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [OPS.04](operations.md#task-ops-04), [WEB.02](#task-web-02), [WEB.03](#task-web-03), [WEB.04](#task-web-04), [WEB.05](#task-web-05), [WEB.06](#task-web-06), [WEB.07](#task-web-07) |
| Write scope | `Web:src/ArcForges.Web.Site/**`<br>`Web:.gitleaks.toml (only exact path-and-digest generic-api-key exceptions re-derived for the C# static output, each change under the WEB.40 successor policy and the GOV.11 review standard)`<br>`Web:tests/ArcForges.Web.Site.Tests/** (incl. the xUnit successor of tests/provenance/candidate.test.ts: Gitleaks exception-boundary positive and negative tests)` |
| Shared resources | [RES-contract-consumer-pins](../shared-resources.md#res-contract-consumer-pins) (append) |
| Validation | Two full builds with identical inputs compared byte-for-byte; no-script navigation/content tests (xUnit over parsed HTML); single-content-change diff; build with network disabled after an approved NuGet restore (CI-eligible offline checks). Keep the pinned Gitleaks scan enabled. Its generic-api-key exception may match only an exact path-and-digest pair enumerated for the C# static output (each bound on the same line, AND). The enumerated set is not assumed: it is established only by observing the C# output and freezing the observed set by a reviewed change under the WEB.40 successor policy. The Web r8 counts (eight lines, six unique values) are not carried over as verified facts for the C# output. Until the reviewed set is frozen the scan fails closed on any generic-api-key match, and any later count outside the frozen set fails the scan. Freezing or changing the set is a security-exception change and needs the GOV.11 review standard (named authority, independent exact-head review and retained CI before merge). The xUnit policy tests must test the actual config and profile bindings with positive and negative cases for a changed digest, another path, an unrelated 64-hex value and credential-looking text. No generic 64-hex patterns, whole-file or commit suppressions, scanner/workflow/rule-algorithm changes, candidate-generation algorithm changes or new dependencies: the only dependency admission is the WEB.40 NuGet closure, which needs the same GOV.11 review standard (independent exact-head review and retained CI before merge). |
| Completion evidence | Determinism comparison and diff-minimality results; pinned Gitleaks results on the C# static output, with the observed generic-api-key line count and unique path-and-digest values recorded as to-be-observed evidence (not assumed from the r8 counts), the frozen exception set with its reviewed record reference, and negative path/digest-boundary evidence. |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: apps/site already has a working react-router static generator (react-router.config.ts prerenders /, /hello, /cloud-hello) with a working build/deploy pipeline; needs generalizing to the full catalogue-driven public inventory |
| Notes | Its only real start need (WP00/WP02) is already satisfied; the current serial plan defers WP47 until after WP40, but nothing blocks starting this immediately. The candidate provenance test reads the actual .gitleaks.toml and browser-resources-r8.json, verifies the six unique exact path/digest bindings for the eight observed findings, and rejects changed-digest, different-path, unrelated-64-hex and credential-text cases; it must not alter candidate generation. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): React Router build-time prerendering becomes the C# HtmlRenderer generator in src/ArcForges.Web.Site (apps/site retires after the WEB.40 parity port) per [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 2. Determinism, locale/URL inventory, the no-leak rule and the exact-exception discipline are kept. The Gitleaks generic-api-key exception set is fail-closed until observed on the C# output and frozen by a reviewed change; the r8 counts are an assumption for the C# output, not a verified fact, and are not used as the bound. Freezing or changing the set is a security-exception change under the GOV.11 review standard (named authority, independent exact-head review, retained CI). The one-for-one xUnit successor of tests/provenance/candidate.test.ts is listed in writes. Starts only after WEB.40 delivers. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): the GOV.11 start is removed because GOV.11 is out; the GOV.03 Node/npm start is removed because its pins are replaced by the .NET build governance of WEB.40, which this task already starts on. |

<a id="task-web-02"></a>

### WEB.02 — Versioned public content and pricing inputs (catalogue.json)

**Outcome.** Catalogue, release metadata, changelog and legal versions are consumed from declared versioned local inputs with no live provider fetch during build; the pricing projection shows its effective version/time.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-02` and ledger record `ledger/tasks/web-02.md` in the Plan repository; task branch `task/web-02` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-47.01](../../work-packages/47-static-public-site.md#rule-wp-47.01) — full |
| Provides | web-content-pricing-inputs |
| Start prerequisites | **artifact** [WEB.01](#task-web-01) — static generator. *Why:* content inputs feed the generator |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.09](#task-web-09) |
| Write scope | `Web:src/ArcForges.Web.Site/content/**`<br>`Web:src/ArcForges.Web.Site/catalogue.json` |
| Validation | Hard-coded-version/price scan; comparison of public projection to the selected approved snapshot — offline |
| Completion evidence | No independently hard-coded product version/private supplier price |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Private candidate builds may use named test-only offer/release fixtures per [WP-47.01](../../work-packages/47-static-public-site.md#rule-wp-47.01); the real WP42/44 numeric join for public promotion is explicitly deferred to WP50, not required to close this task's own gate. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The versioned catalogue and pricing data files are kept as data. Their loader moves from the React/Vite import to typed C# configuration. No live provider fetch during build, unchanged. Writes move to the C# site project. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: catalogue, pricing, release, changelog and legal rows for ArcSlate and ArcNotes, and the macOS download, signing, notarisation and Apple store rows, are out of scope, not completed. |

<a id="task-web-03"></a>

### WEB.03 — Rendering and performance

**Outcome.** Above-the-fold content ships in the HTML delivered by the C# static generator, so no JavaScript is needed to render public pages ([TB-01](../../../architecture/18-editing-and-rich-content.md#rule-tb-01)). Assets are content-hashed with short-lived HTML caching, no blocked third-party resource sits on the critical path, and the p75 LCP/INP/CLS budgets ([AL-05](../../../architecture/08-security-architecture.md#rule-al-05)) are met.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-03` and ledger record `ledger/tasks/web-03.md` in the Plan repository; task branch `task/web-03` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-47.02](../../work-packages/47-static-public-site.md#rule-wp-47.02) — full |
| Provides | web-site-performance |
| Start prerequisites | **artifact** [WEB.01](#task-web-01) — static generator. *Why:* measures its output |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.09](#task-web-09) |
| Write scope | `Web:src/ArcForges.Web.Site/**`<br>`Web:tools/ArcForges.Web.Tooling/**` |
| Shared resources | [RES-web-build-config](../shared-resources.md#res-web-build-config) (append) |
| Validation | No-script render test; critical-path resource audit; p75 performance measurement; global-reachability check on every third-party host — offline/lab Public-Site CSP assertion (xUnit over the generated headers and meta tags, [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 2): the static public pages carry exactly the strict token set script-src 'self' with no unsafe-eval, unsafe-inline or wasm-unsafe-eval token, style-src 'self', and no script element or Blazor _framework reference on any public route. |
| Completion evidence | No-script render, critical-path audit and performance measurements |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Public pages stay static HTML and CSS before JavaScript runs ([TB-01](../../../architecture/18-editing-and-rich-content.md#rule-tb-01) is a live rule). The generator emits no WebAssembly or _framework script on public routes. The React tooling/** scripts port to C# under tools/ArcForges.Web.Tooling. The [AL-05](../../../architecture/08-security-architecture.md#rule-al-05) public budgets are not re-baselined. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 2): The strict public-Site CSP token set (no wasm-unsafe-eval) is asserted in validation; the App profiles keep their own token set under WEB.16. |

<a id="task-web-04"></a>

### WEB.04 — Internationalisation

**Outcome.** Locale-scoped URLs with alternate-language annotations, no client-only switching and no trapping redirect; every user-visible string, including generated pages, is localisable through .NET localisation resources (.resx) with the same criteria as before.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-04` and ledger record `ledger/tasks/web-04.md` in the Plan repository; task branch `task/web-04` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-47.03](../../work-packages/47-static-public-site.md#rule-wp-47.03) — full |
| Provides | web-site-i18n |
| Start prerequisites | **artifact** [WEB.01](#task-web-01) — static generator. *Why:* i18n routing is generator-level |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.09](#task-web-09) |
| Write scope | `Web:src/ArcForges.Web.Site/**` |
| Validation | Locale routing/annotation tests, no-trap assertion, pseudo-localisation pass — offline |
| Completion evidence | Locale routing, no-trap and pseudo-localisation results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The mechanism moves from React i18n to .NET localisation (.resx) under the C# static generator. The locale routing, no-trap and pseudo-localisation criteria are unchanged. |

<a id="task-web-05"></a>

### WEB.05 — Documentation, downloads and legal surfaces

**Outcome.** Versioned per-product documentation, a no-account-gate download surface serving signed artifacts with published hashes, an update feed surface, and versioned legal pages with effective dates.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-05` and ledger record `ledger/tasks/web-05.md` in the Plan repository; task branch `task/web-05` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-47.04](../../work-packages/47-static-public-site.md#rule-wp-47.04) — full |
| Provides | web-docs-downloads-legal |
| Start prerequisites | **artifact** [WEB.01](#task-web-01) — static generator. *Why:* docs/downloads/legal are generated surfaces |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.09](#task-web-09) |
| Write scope | `Web:src/ArcForges.Web.Site/content/**`<br>`Web:src/ArcForges.Web.Site/Pages/**` |
| Validation | Documentation version routing; download integrity verification against published hashes; no-account-gate assertion; legal version-history tests — offline against labelled fixtures |
| Completion evidence | Download integrity, no-gate and legal versioning results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Private candidate download fixtures are labelled; public promotion with real signed Desktop/Android artifacts is joined at WP50, not required to close this task. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Versioned docs, downloads and legal pages become generated surfaces of the C# static generator. The download-integrity, no-gate and legal-versioning criteria are unchanged. Legal version-history tests run as xUnit tests against labelled fixtures. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: per-product documentation and download rows for ArcSlate and ArcNotes, the macOS and Apple store download rows, and any Play store download route are out of scope, not completed. The Android download is the direct APK channel only (S11). |

<a id="task-web-06"></a>

### WEB.06 — Accessibility and analytics

**Outcome.** Accessibility semantics and keyboard-only navigation on every page; minimal privacy-preserving analytics with no cross-site identifier and no consent wall.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-06` and ledger record `ledger/tasks/web-06.md` in the Plan repository; task branch `task/web-06` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / S |
| Obligations | [WP-47.05](../../work-packages/47-static-public-site.md#rule-wp-47.05) — full |
| Provides | web-site-a11y-analytics |
| Start prerequisites | **artifact** [WEB.01](#task-web-01) — static generator. *Why:* audits its output |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.09](#task-web-09) |
| Write scope | `Web:src/ArcForges.Web.Site/**`<br>`Web:tests/ArcForges.Web.Site.Tests/**` |
| Validation | CI-gated (offline) accessibility semantics in xUnit/bUnit over the generated static pages and rendered components: roles, accessible names, labels, focus order, live regions, landmarks, alt text, heading order, lang, focus-visible styles and keyboard-reachable controls; axe-core is local opt-in test-only tooling run through Microsoft.Playwright for .NET, injected only into the page under test and never shipped (browser E2E is never CI: playwright.config.ts CI guard, [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)), plus a dated manual verification; analytics payload audit (xUnit, offline). |
| Completion evidence | Offline xUnit/bUnit accessibility semantic results on the generated pages and components; local axe-core opt-in results; dated manual record; analytics payload audit with no cross-site identifier. |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: @axe-core/playwright is already a pinned devDependency in package.json though no pages exist to audit yet |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021), [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017); section 6 decision 3): Accessibility semantics and keyboard navigation are checked on the C# generated pages and components. The CI gate is the offline xUnit/bUnit semantic assertion set (roles, names, labels, focus order, live regions) in validation. axe-core is local opt-in test-only tooling run through Microsoft.Playwright for .NET, injected only into the page under test and never shipped. Baseline fact: axe-core tests already run only in tests/browser under the Playwright CI guard, so no CI-gated axe check is removed by this repair. The criteria are unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): no part of this task is out of scope: minimal privacy-preserving analytics and the analytics payload audit stay in scope ([PV-05](../../../architecture/18-editing-and-rich-content.md#rule-pv-05); S12). |

<a id="task-web-07"></a>

### WEB.07 — Independence and atomic deployment

**Outcome.** The site remains fully available during a full Cloud outage, deploys atomically per surface from a promoted artifact (static C# output on Cloudflare Static Assets, no production Node server), and rollback restores the previous artifact set. The Cloudflare worker/index.js stays a thin platform adapter with no business rule.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-07` and ledger record `ledger/tasks/web-07.md` in the Plan repository; task branch `task/web-07` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | release / S |
| Obligations | [WP-47.06](../../work-packages/47-static-public-site.md#rule-wp-47.06) — full |
| Provides | web-site-deployment |
| Start prerequisites | **artifact** [WEB.01](#task-web-01) — static generator. *Why:* deploys its output |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.09](#task-web-09), [WEB.30](#task-web-30), [WEB.31](#task-web-31) |
| Write scope | `Web:wrangler.json`<br>`Web:worker/**`<br>`Web:.github/workflows/ci.yml`<br>`Web:tools/ArcForges.Web.Tooling/Cloudflare/**` |
| Shared resources | [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append), [RES-web-build-config](../shared-resources.md#res-web-build-config) (append) |
| Validation | Cloud-outage independence, atomic-deployment and rollback tests: the offline checks (CI-eligible) exercise the deployment adapter against recorded Cloudflare API fixtures and a local wrangler dry-run, and compare the promoted artifact byte-for-byte with the build output. The live-account promotion and rollback check is a local opt-in run by an operator against the real Cloudflare account, recorded as an operator run receipt, not a hosted live-service CI check ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)); no live-service CI job is added. The existing main-push Cloudflare deploy job in .github/workflows/ci.yml is a deployment step outside validation and stays (section 6 decision 2); it is not counted as validation evidence. Rollback acceptance is a named gate ([PG-23](../../../assurance/open-gates-register.md#rule-pg-23), REL.05) recorded by the local operator run receipt. |
| Completion evidence | A full cloud outage leaves the site fully available; deployment is atomic; rollback restores the previous set. Rollback acceptance is the named gate evidence ([PG-23](../../../assurance/open-gates-register.md#rule-pg-23), REL.05) recorded by a local opt-in operator run receipt, not a CI job ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017); section 6 decision 2). |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: wrangler.json + worker/index.js (www redirect) + the CI deploy job already implement build-once/promote-same-bytes deployment to Cloudflare for the site; this task extends/validates it, not builds it fresh |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Stays a thin-adapter task ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 1). The Node/TypeScript tooling/cloudflare.ts deployment script ports to C# under tools/ArcForges.Web.Tooling. Node remains wrangler build/deploy tooling only. |

<a id="task-web-08"></a>

### WEB.08 — Owned consumer design system (Razor class library ArcForges.Web.Ui)

**Outcome.** src/ArcForges.Web.Ui (the Razor class library that replaces packages/ui) grows from a placeholder Shell/Button into a full design-token system (typography, spacing, colour, themes), owned accessible Blazor components, a test-only component catalogue, approved visual baselines and reusable account/usage/chat primitives, with localization/long-label/mobile-nav/focus/reduced-motion/loading-error-empty variants.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-08` and ledger record `ledger/tasks/web-08.md` in the Plan repository; task branch `task/web-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-47.07](../../work-packages/47-static-public-site.md#rule-wp-47.07) — full |
| Provides | web-design-system |
| Start prerequisites | **artifact** [WEB.40](#task-web-40) — the migrated Web repository baseline (Razor component port of the placeholder Shell/Button). *Why:* the design system is ported into the C# solution before its full token system is built |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.09](#task-web-09), [WEB.10](#task-web-10), [WEB.19](#task-web-19) |
| Write scope | `Web:src/ArcForges.Web.Ui/**`<br>`Web:tests/ArcForges.Web.Ui.Tests/**` |
| Shared resources | [RES-web-shared-ui](../shared-resources.md#res-web-shared-ui) (append) |
| Validation | bUnit component behaviour tests, including the CI-gated accessibility semantic assertions of WEB.06 on every component state; production-rendered Microsoft.Playwright for .NET visual snapshots for representative viewport/theme/locale combinations (local opt-in, per the Playwright CI guard); axe-core on the same states as local opt-in only, injected only into the page under test; dated human visual/keyboard review; NuGet licence and provenance checks. |
| Completion evidence | Approved consumer layouts and complete accessible states |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: packages/ui currently exports only Arrow/Button/Shell (a minimal site header/footer); needs the full token system and component catalogue |
| Notes | Has NO dependency on WEB.01-WEB.07 (different package, only needs WP02 which is already satisfied) and should be started in parallel with the site generator work, not after it — it is the critical-path input for both WEB.10 (account) and WEB.19 (chat). Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): packages/ui (React Shell/Button and 373 CSS lines) becomes the Razor class library ArcForges.Web.Ui. The token system, catalogue, visual baselines and variants are kept. Still no dependency on WEB.01-WEB.07, and it is still the critical-path input for WEB.10 and WEB.19. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): the GOV.03 Node/npm start is removed (S10); the .NET build governance comes from the WEB.40 start. |

<a id="task-web-09"></a>

### WEB.09 — Verify the owned Site artifact and real integration

**Outcome.** The C#-generated static Site with localization/SEO and no production Node server or runtime JavaScript is verified end to end; independently published product/version/download metadata is consumed through the fixed release contract, with pending later owners and their closing gates recorded.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-09` and ledger record `ledger/tasks/web-09.md` in the Plan repository; task branch `task/web-09` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / S |
| Package acceptance | Records the [WP-47](../../work-packages/47-static-public-site.md#rule-wp-47) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-47.90](../../work-packages/47-static-public-site.md#rule-wp-47.90) — full<br>[WP-47](../../work-packages/47-static-public-site.md#rule-wp-47) Browser matrix acceptance paragraph (browser-support.v1 for the static site output) — package-level obligation contribution |
| Provides | web-static-site-candidate |
| Start prerequisites | **artifact** [WEB.02](#task-web-02) — content/pricing inputs. *Why:* final join<br>**artifact** [WEB.03](#task-web-03) — performance. *Why:* final join<br>**artifact** [WEB.04](#task-web-04) — i18n. *Why:* final join<br>**artifact** [WEB.05](#task-web-05) — docs/downloads/legal. *Why:* final join<br>**artifact** [WEB.06](#task-web-06) — a11y/analytics. *Why:* final join<br>**artifact** [WEB.07](#task-web-07) — deployment. *Why:* final join<br>**artifact** [WEB.08](#task-web-08) — design system. *Why:* final join |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.05](release.md#task-rel-05) |
| Write scope | `Web:src/ArcForges.Web.Site/**` |
| Validation | Static, no-script, public-Site CSP token-set (WEB.03), localization, link and artifact-version checks (xUnit); accessibility through the CI-gated WEB.06 xUnit semantic checks, with axe-core only as local Microsoft.Playwright for .NET opt-in for browser rendering, injected only into the page under test; private candidate download fixtures labelled; public promotion waits for WP50. |
| Completion evidence | Owned-artifact-and-real-integration receipt including browser-support.v1 evidence for the site output |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Provides the tooling WP45's operations console needs ("47 tooling must precede 45" per producer-artifacts-and-integration.md); the commerce, policy and operations lanes should reference this task's 'web-static-generator'/'web-design-system' tokens as its own start need rather than waiting on all of WP47's numeral position in the old serial plan. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Verifies the C# generated Site artifact instead of the React build. The no-script, localization and release-contract criteria are unchanged. |

<a id="task-web-10"></a>

### WEB.10 — Account Blazor shell: route graph, deployment-profile selection, generated C# SDK wiring

**Outcome.** The ArcForges.Web.App Blazor WebAssembly project is created with the account deployment profile (standalone, RunAOTCompilation=false by default): route graph and shell composed from ArcForges.Web.Ui and the generated C# gRPC-Web client (Grpc.Net.Client.Web, binary framing); Android callback/assetlinks wiring; responsive overview/navigation; safe public runtime config; error boundaries; and loading/empty/pending/expired states with cache-clear-and-abort on user/workspace change (in-memory state only, no persistent account cache).

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-10` and ledger record `ledger/tasks/web-10.md` in the Plan repository; task branch `task/web-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / XL |
| Obligations | [WP-48.00](../../work-packages/48-account-portal.md#rule-wp-48.00) — full |
| Provides | web-app-shell |
| Start prerequisites | **artifact** [WEB.08](#task-web-08) — design system tokens/components. *Why:* the shell composes packages/ui directly<br>**contract** [CON.07](contracts.md#task-con-07) — generated C# gRPC-Web client from the published Contracts NuGet candidate, at the current release covering the account and chat wire surface (precondition: the NuGet identity is verified at start from the CON.07 publication record). *Why:* the shell calls the generated C# client; the TypeScript SDK pin retires with @arcforges/api-client ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 4)<br>**artifact** [WEB.40](#task-web-40) — the migrated Blazor WebAssembly project baseline and C# NuGet closure. *Why:* the shell is built in the migrated solution<br>**artifact** [PRF.11](runtime-proofs.md#task-prf-11) — Blazor WebAssembly production proof (real AOT probe, CSP, exact values, binary streaming decision). *Why:* bulk Web feature work follows the early Blazor proof (brief section 4.1) |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.12](cloud.md#task-cloud-12) — identity/browser/native endpoints. *Why:* per [WP-48.00](../../work-packages/48-account-portal.md#rule-wp-48.00)'s own text: "minimal auth producer already exists in WP22" |
| Unblocks | [WEB.11](#task-web-11), [WEB.13](#task-web-13), [WEB.14](#task-web-14), [WEB.15](#task-web-15), [WEB.16](#task-web-16), [WEB.19](#task-web-19) |
| Write scope | `Web:src/ArcForges.Web.App/**`<br>`Web:tests/ArcForges.Web.App.Tests/**`<br>`Web:win.slnx (register the profile projects only)`<br>`Web:Directory.Packages.props (NuGet pins needed by the shell only)` |
| Shared resources | [RES-contract-consumer-pins](../shared-resources.md#res-contract-consumer-pins) (append), [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append), [RES-web-build-config](../shared-resources.md#res-web-build-config) (append), [RES-web-shared-ui](../shared-resources.md#res-web-shared-ui) (append) |
| Validation | xUnit state/route tests and bUnit component tests (no-cookie-leakage, state, PKCE and origin-mismatch, Android-verified-links tests); production profile/chunk isolation, both themes, keyboard and narrow layouts (fixture-backed CI plus local opt-in real-browser evidence). |
| Completion evidence | Profile isolation and composition results |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08 (Web a469064): apps/app holds the React/Vite Account and Chat probe profiles delivered offline under PRF.08 (superseded by PRF.11), not an account shell. The account shell has no ledger record and is not started. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The apps/app workspace registration moves to the Blazor project. The chain of cookie/PKCE/origin/cache-clear rules is kept. The shell composes ArcForges.Web.Ui instead of packages/ui. The CON.07 need text names the generated C# client. |

<a id="task-web-11"></a>

### WEB.11 — Real browser session and step-up acceptance

**Outcome.** Passkey/email verification/recovery, live opaque cookie session, server-controlled expiry/revocation and sensitive-action step-up work on the real account origin topology; no bearer/refresh token ever enters the app.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-11` and ledger record `ledger/tasks/web-11.md` in the Plan repository; task branch `task/web-11` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-48.01](../../work-packages/48-account-portal.md#rule-wp-48.01) — full |
| Provides | web-browser-session |
| Start prerequisites | **artifact** [CLOUD.19](cloud.md#task-cloud-19) — the [P2-003](../../../decisions/phase-2-specification-decisions.md#rule-p2-003) same-origin cookie-session adapter. *Why:* [WP-48.01](../../work-packages/48-account-portal.md#rule-wp-48.01)'s own text: "Use the [P2-003](../../../decisions/phase-2-specification-decisions.md#rule-p2-003) adapter implemented in [WP-22.08](../../work-packages/22-identity-workspace-and-device.md#rule-wp-22.08), not a new auth choice" — a precise single-substep need, not all of WP22<br>**artifact** [WEB.10](#task-web-10) — account shell. *Why:* session UI lives in the shell |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.12](#task-web-12), [WEB.18](#task-web-18) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Account/**`<br>`Web:tests/ArcForges.Web.App.Tests/**` |
| Validation | Playwright against production assets, edge and real Cloud and D1 is local opt-in (login/logout, two origins and tabs, sibling-origin CSRF, passkey expected origin, replica restart, expiry/revoke races); manual passkey and browser matrix supplements automation; xUnit/bUnit fixture tests for session state, step-up and expiry handling. |
| Completion evidence | Token storage, refresh, step-up and new-browser trust results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The passkey WebAuthn call (navigator.credentials) and clipboard/download are the audited JavaScript interop points allowed by [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 2. No bearer or refresh token enters the app. Session, step-up and expiry criteria are unchanged. |

<a id="task-web-12"></a>

### WEB.12 — Account and security surfaces

**Outcome.** Profile, authentication methods, passkey management, sessions, device list with trust/revocation, recovery configuration, API token management ([AT-01](../../../architecture/01-solution-and-project-layout.md#rule-at-01): personal access tokens with scoped display-once creation and revocation), the sync status view and the security-event view are complete, with step-up required on every sensitive action.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-12` and ledger record `ledger/tasks/web-12.md` in the Plan repository; task branch `task/web-12` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-48.02](../../work-packages/48-account-portal.md#rule-wp-48.02) — full |
| Provides | web-account-security-ui |
| Start prerequisites | **artifact** [WEB.11](#task-web-11) — session/step-up. *Why:* every action here requires step-up |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.17](#task-web-17), [WEB.18](#task-web-18) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Account/**` |
| Validation | Device-revocation-propagation, passkey add/remove, security-event-visibility and step-up-required-per-action tests, API token display-once and revocation tests and sync status view tests — fixture CI plus local opt-in real-Cloud evidence |
| Completion evidence | Device revocation, passkey, step-up, API token and sync status coverage results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Account and security surfaces are Blazor components in the Account profile. The step-up-per-action and revocation-propagation criteria are unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): gains API token management ([AT-01](../../../architecture/01-solution-and-project-layout.md#rule-at-01)) and the sync status view from the requirements/02 section 12 minimum portal scope (S12), which no WEB outcome covered. |

<a id="task-web-13"></a>

### WEB.13 — Workspace, storage and usage

**Outcome.** Single-owner workspace settings (no membership/invitation/role/seat surface), service-term/included-capacity display with recovery timing and extra-credit opt-in, storage from committed objects, usage-against-quota with visible reset boundaries, and data-health visibility.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-13` and ledger record `ledger/tasks/web-13.md` in the Plan repository; task branch `task/web-13` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-48.03](../../work-packages/48-account-portal.md#rule-wp-48.03) — full |
| Provides | web-workspace-storage-ui |
| Start prerequisites | **artifact** [WEB.10](#task-web-10) — account shell. *Why:* lives in the shell |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.42](cloud.md#task-cloud-42) — R2/committed-object accounting. *Why:* displayed storage must match server-side computed values exactly<br>**integration** [CLOUD.52](cloud.md#task-cloud-52) — data-health status projection (read-only surface only). *Why:* the portal needs only WP46's read-only health/status projection, not backup/restore execution itself — must not block the whole portal on one recovery capability |
| Unblocks | [WEB.17](#task-web-17), [WEB.18](#task-web-18) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Workspace/**` |
| Validation | Accounting comparison against server-side figures; structural xUnit test over the generated C# operation catalogue and route table asserting no membership, invitation, role or seat operation; projection test asserting no supplier rate or route-weight leakage; capacity-vs-credits never-summed display test. |
| Completion evidence | Storage and usage accounting comparison |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The no-membership structural test becomes an xUnit assertion over the generated C# operation catalogue and route table, not a TypeScript source check. |

<a id="task-web-14"></a>

### WEB.14 — Subscription, capacity, credits and hosted checkout

**Outcome.** Consumer subscription and management views use public server projections and generated C# operations; paid-term state, replenishing capacity and purchased credits display separately; hosted checkout opens in-browser and shows confirming until verified Cloud state changes; no client or provider redirect grants entitlement.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-14` and ledger record `ledger/tasks/web-14.md` in the Plan repository; task branch `task/web-14` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-48.04](../../work-packages/48-account-portal.md#rule-wp-48.04) — all work except the parts mapped to WEB.29 |
| Provides | web-commerce-ui |
| Start prerequisites | **artifact** [WEB.10](#task-web-10) — account shell. *Why:* lives in the shell<br>**contract** [CON.08](contracts.md#task-con-08) — commerce/entitlement wire records. *Why:* already available for building/unit-testing against fixtures |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [COM.14](commerce.md#task-com-14) — real commerce ledger/test-mode checkout environment. *Why:* per the producer stage matrix, WP48 "activates only with required real provider evidence"; unlike WP47.01's pricing display, this gate cannot be closed with candidate fixtures alone — duplicate-click, cancelled/failed/late confirmation and refund scenarios need a real test-mode provider<br>**integration** [POL.02](policy.md#task-pol-02) — real policy projections for rate-limit/recovery reasons. *Why:* server-provided reasons must be real, not scripted |
| Unblocks | [WEB.17](#task-web-17), [WEB.18](#task-web-18), [WEB.29](#task-web-29), [WEB.30](#task-web-30), [WEB.31](#task-web-31) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Commerce/**` |
| Validation | Real C# accounting and checkout test-environment flows; exact-amount display using C# decimal and int64/uint64 values end to end (no double or JavaScript Number conversion), correct above the 2^53 JavaScript safe-integer boundary and across the full int64/uint64 range (xUnit/bUnit, offline); duplicate-click, cancelled, failed, late-confirmation, refund, term-expiry and stale-price tests (local opt-in against a real test-mode provider). |
| Completion evidence | Entitlement reason coverage, credit separation and no-payment-field scan |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The JS safe-integer display boundary is restated as a C# decimal and int64/uint64 boundary ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 1 exact-value rule). The acceptance is stronger: the boundary above 2^53 and the full wire range are both tested. Duplicate-click, refund and provider criteria are unchanged. |

<a id="task-web-15"></a>

### WEB.15 — Data export and deletion

**Outcome.** Export requests show progress and download; deletion requests show a grace period and an explicit, accurate statement of what is and is not deleted, including that local data is untouched.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-15` and ledger record `ledger/tasks/web-15.md` in the Plan repository; task branch `task/web-15` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-48.05](../../work-packages/48-account-portal.md#rule-wp-48.05) — full |
| Provides | web-data-export-deletion-ui |
| Start prerequisites | **artifact** [WEB.10](#task-web-10) — account shell. *Why:* lives in the shell<br>**contract** [CON.22](contracts.md#task-con-22) — published data and export operations. *Why:* the Account data export and deletion surfaces call the generated operations |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.45](cloud.md#task-cloud-45) — real export job mechanics. *Why:* export must be real, not a stub |
| Unblocks | [WEB.17](#task-web-17), [WEB.18](#task-web-18) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Data/**` |
| Validation | Export-completeness, deletion-statement-accuracy, grace-period and local-data-assertion tests |
| Completion evidence | Export completeness and deletion statement accuracy |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Export progress and download and deletion-statement accuracy are Blazor components calling the generated C# CON.22 operations. Criteria unchanged. |

<a id="task-web-16"></a>

### WEB.16 — Origin security and performance (account)

**Outcome.** A strict CSP on the Blazor WebAssembly profiles: script-src 'self' 'wasm-unsafe-eval' plus only the required framework hashes, never unsafe-eval or unsafe-inline; style-src 'self' with no component that needs inline styles (the exact token set is asserted on the built output; [CS-01](../../../architecture/05-cloud-architecture.md#rule-cs-01) is rewritten to it). Per-origin cookie, CORS and CSRF posture, no secret in the bundle, sandboxed preview of user content, and bundle-size and first-interactive budgets re-baselined for Blazor WebAssembly by a reviewed [AL-06](../../../architecture/10-web-architecture.md#rule-al-06) record owned by PRF.11, while the regression gate and its 10% regression threshold stay fixed: an [AL-06](../../../architecture/10-web-architecture.md#rule-al-06) record may change only the measured baseline values, never the threshold or the gate itself.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-16` and ledger record `ledger/tasks/web-16.md` in the Plan repository; task branch `task/web-16` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-48.06](../../work-packages/48-account-portal.md#rule-wp-48.06) — full |
| Provides | web-account-origin-security |
| Start prerequisites | **artifact** [WEB.10](#task-web-10) — account shell. *Why:* policy applies to the real bundle |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.18](#task-web-18) |
| Write scope | `Web:deploy/edge/account/**`<br>`Web:src/ArcForges.Web.App/** (CSP and budget configuration only)` |
| Shared resources | [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append), [RES-web-build-config](../shared-resources.md#res-web-build-config) (append) |
| Validation | Policy header verification against the published profile build, with an exact CSP token-set assertion; bundle secret scan; sandbox escape test on hostile content; budget measurements with regression gate (xUnit, offline and CI-eligible); in-browser CSP proof local opt-in under PRF.11. |
| Completion evidence | Policy headers, bundle secret scan and budget measurements |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The 'no default inline script' wording becomes the Blazor CSP rule of [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 2: wasm-unsafe-eval plus required hashes, never unsafe-eval or unsafe-inline. The React budgets (apps/app/budgets.json: initialJsGzip 116363 account, 144698 chat, regressionPercent 10) are re-baselined only by the reviewed [AL-06](../../../architecture/10-web-architecture.md#rule-al-06) record and never silently. |

<a id="task-web-17"></a>

### WEB.17 — Offline, degradation and accessibility (account)

**Outcome.** Honest offline behaviour in the Blazor Account profile, in memory only: no service worker and no persistent account cache ([WCI-05](../../../architecture/25-web-toolchain-and-sdk.md#rule-wci-05)). When the connection drops, the profile shows an honest offline state and keeps unsent input in live component state for the current page session; a cloud-outage state naming unavailable capabilities with reasons rather than blanking; and full keyboard-only accessibility on every major workflow.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-17` and ledger record `ledger/tasks/web-17.md` in the Plan repository; task branch `task/web-17` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-48.07](../../work-packages/48-account-portal.md#rule-wp-48.07) — full |
| Provides | web-account-resilience |
| Start prerequisites | **artifact** [WEB.12](#task-web-12) — account/security surfaces. *Why:* exercises real workflows<br>**artifact** [WEB.13](#task-web-13) — workspace/storage surfaces. *Why:* exercises real workflows<br>**artifact** [WEB.14](#task-web-14) — commerce surfaces. *Why:* exercises real workflows<br>**artifact** [WEB.15](#task-web-15) — data surfaces. *Why:* exercises real workflows |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.18](#task-web-18) |
| Write scope | `Web:src/ArcForges.Web.App/**`<br>`Web:tests/ArcForges.Web.App.Tests/**` |
| Validation | Offline-behaviour tests (bUnit/xUnit): offline state shown, unsent input kept across a simulated connection loss within the page session, no service worker registered and no browser-storage write asserted; cloud-outage-no-blank test; accessibility CI-gated semantic checks (WEB.06) and a manual pass. |
| Completion evidence | Offline, outage and accessibility results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021), [WCI-05](../../../architecture/25-web-toolchain-and-sdk.md#rule-wci-05)): The offline criterion is reconciled to the online-only decision. Offline behaviour in the Blazor profiles is in memory only (no service worker, no persistent cache), so unsent input survives a connection loss within the page session but not a reload; a draft that survives reload would need a reviewed [WCI-05](../../../architecture/25-web-toolchain-and-sdk.md#rule-wci-05) decision. The UI port targets the Blazor Account profile components. |

<a id="task-web-18"></a>

### WEB.18 — Verify the owned Account artifact and real integration

**Outcome.** Real browser evidence against the AOT release closes cookie secrecy, CSRF, expiry/revocation, privacy/export and admission/usage display; the account deployment profile is the sole account application with no AGPL import into Mobile.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-18` and ledger record `ledger/tasks/web-18.md` in the Plan repository; task branch `task/web-18` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-48](../../work-packages/48-account-portal.md#rule-wp-48) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-48.90](../../work-packages/48-account-portal.md#rule-wp-48.90) — full; final-review closure: 08-security-architecture account/provider closure, scoped-token display-once, cancellation restricted route<br>[WP-48](../../work-packages/48-account-portal.md#rule-wp-48) Required implementation and closure from the final review: 08-security-architecture account/provider closure, scoped-token display-once, cancellation restricted route — package-level obligation contribution<br>[WP-48](../../work-packages/48-account-portal.md#rule-wp-48) Browser matrix acceptance paragraph (browser-support.v1 for the account output) — package-level obligation contribution |
| Provides | web-account-candidate |
| Start prerequisites | **artifact** [WEB.11](#task-web-11) — session/step-up. *Why:* final join<br>**artifact** [WEB.12](#task-web-12) — security surfaces. *Why:* final join<br>**artifact** [WEB.13](#task-web-13) — workspace surfaces. *Why:* final join<br>**artifact** [WEB.14](#task-web-14) — commerce surfaces. *Why:* final join<br>**artifact** [WEB.15](#task-web-15) — data surfaces. *Why:* final join<br>**artifact** [WEB.16](#task-web-16) — origin security. *Why:* final join<br>**artifact** [WEB.17](#task-web-17) — resilience. *Why:* final join<br>**artifact** [WEB.29](#task-web-29) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [REL.05](release.md#task-rel-05) |
| Write scope | `Web:src/ArcForges.Web.App/**` |
| Validation | Real browser against the AOT release: cookie secrecy, CSRF, expiry/revocation, privacy/export and admission/usage display — local opt-in per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Owned-artifact-and-real-integration receipt; contributes its scoped evidence toward [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) (closed later at WP50, not here) |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The phrase AOT release refers to the Cloud Native AOT backend, not to Web, so it is unchanged. The Web profile is Blazor WebAssembly standalone with RunAOTCompilation=false by default; any WASM AOT adoption requires the PRF.11 benchmark record. |

<a id="task-web-19"></a>

### WEB.19 — Chat shell: route composition and design-system integration

**Outcome.** Chat routes are composed in the same ArcForges.Web.App Blazor WebAssembly codebase using owned ArcForges.Web.Ui components and the generated C# gRPC-Web client. Account and Chat assets, cookies, query scopes and public config are independently selected and validated (separate profile output; no chat code in the account profile). Responsive conversation navigation, composer and task panel, and native-product handoff work with keyboard and reduced-motion support.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-19` and ledger record `ledger/tasks/web-19.md` in the Plan repository; task branch `task/web-19` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-49.00](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.00) — full |
| Provides | web-chat-shell |
| Start prerequisites | **artifact** [WEB.08](#task-web-08) — design system tokens/components. *Why:* the chat shell composes packages/ui directly, same as the account shell<br>**artifact** [WEB.10](#task-web-10) — account shell and apps/app workspace registration. *Why:* chat is the second deployment profile of the same already-registered apps/app codebase; do not re-register the workspace |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.20](#task-web-20), [WEB.21](#task-web-21), [WEB.22](#task-web-22), [WEB.23](#task-web-23), [WEB.25](#task-web-25), [WEB.30](#task-web-30), [WEB.31](#task-web-31), [WEB.32](#task-web-32), [WEB.33](#task-web-33) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Chat/**` |
| Shared resources | [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append), [RES-web-build-config](../shared-resources.md#res-web-build-config) (append), [RES-web-shared-ui](../shared-resources.md#res-web-shared-ui) (append) |
| Validation | Production route and profile inspection; approved light, dark and narrow-screen visual baselines; keyboard, touch and long-text states; xUnit source and dependency assertion that no provider or Harness implementation enters the browser profile. |
| Completion evidence | Cross-profile isolation results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Chat is the second Blazor profile of the same ArcForges.Web.App codebase (not re-registered). The route-composition and design-system criteria are unchanged. |

<a id="task-web-20"></a>

### WEB.20 — Conversation and generated output streams

**Outcome.** The full Chat UI uses annex-10 gRPC-Web binary output and event streams (Grpc.Net.Client.Web; server streaming through the .NET 10 browser streaming client, with the grpc-web-text variant on server-stream routes only if the PRF.11 decision records it, and then its framing variant is recorded in the wire registry before the stream UI ships) with durable recovery. Cloud history is authoritative except memory-only temporary UI, and an interrupted stream is always shown as interrupted, never complete.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-20` and ledger record `ledger/tasks/web-20.md` in the Plan repository; task branch `task/web-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-49.01](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.01) — all work except the parts mapped to WEB.27 |
| Provides | web-chat-streaming-ui |
| Start prerequisites | **artifact** [WEB.19](#task-web-19) — chat shell + real deployed WP23/24 transport (inherited via WEB.10). *Why:* streaming UI needs the real deployed event/stream transport, already available once the account shell's WP22/23 chain is up<br>**artifact** [PRF.11](runtime-proofs.md#task-prf-11) — the binary-versus-text server-stream decision and the browser streaming proof. *Why:* the streaming UI is not built before the Blazor transport is observed to work ([P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 2); the transport is proven, not assumed |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [WEB.27](#task-web-27) — real CF Harness admission/generation/tool loop. *Why:* same pattern as AND.09: the streaming/cursor/reconnect UI can be fully built and tested against the server-side contract-bound fixture turn endpoint that already runs in the real deployed Cloud host; real generation quality requires WP52<br>**integration** [SRCH.90](search.md#task-srch-90) — the companion assistant answers that cite search, delivered search surface ([SW-06](../../../requirements/products/arcchat-mobile-and-web.md#rule-sw-06)). *Why:* companion answers must be verified against the delivered search, not a fixture ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026) S13) |
| Unblocks | [WEB.24](#task-web-24), [WEB.26](#task-web-26), [WEB.27](#task-web-27) |
| Permitted substitutes | [SUB-fixture-turn-endpoint](../substitutes.md#sub-fixture-turn-endpoint) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Chat/**`<br>`Web:tests/ArcForges.Web.App.Tests/**` |
| Validation | Generated event-contract and recovery tests (byte offsets, reconnect and gaps, duplicate delivery, loss of authorization) as xUnit and bUnit tests over the generated C# event contract; browser-support.v1 polling-fallback behaviour (EventService.Poll every 10s +/-20% jitter, ExecutionService.ReadOutput every 5s after the 45s stream-silence timeout), unchanged. |
| Completion evidence | Streaming, interruption and partial-message results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The polling constants are kept verbatim. Blazor browser server streaming is unverified in the research and is decided by PRF.11. The WEB.27 completion edge and the SUB-fixture-turn-endpoint substitute are unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): realtime server streaming is V1 (S3), and the SRCH.90 completion verifies companion answers (S13). |

<a id="task-web-21"></a>

### WEB.21 — Tasks, approval and steering

**Outcome.** Task/run/step/tool-call surfaces with progress; approve/reject/cancel/pause/retry/steer as idempotent commands; local-presence-required operations are clearly refused with an explanation; no missed notification loses a pending approval.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-21` and ledger record `ledger/tasks/web-21.md` in the Plan repository; task branch `task/web-21` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-49.02](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.02) — all work except the parts mapped to WEB.27, WEB.28 |
| Provides | web-chat-tasks-ui |
| Start prerequisites | **artifact** [WEB.19](#task-web-19) — chat shell. *Why:* lives in the shell |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [WEB.28](#task-web-28) — real device bridge. *Why:* local-presence-required refusal and real device dispatch need the real bridge; the approval/task UI itself only needs the contract shape<br>**integration** [WEB.27](#task-web-27) — real Harness planning/tool-proposal loop. *Why:* approval content must reflect real proposed effects to close the gate |
| Unblocks | [WEB.24](#task-web-24), [WEB.26](#task-web-26), [WEB.27](#task-web-27), [WEB.28](#task-web-28) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Tasks/**`<br>`Web:tests/ArcForges.Web.App.Tests/**` |
| Validation | Idempotency-per-control, local-presence-negative, approval-expiry and durable-attention tests |
| Completion evidence | Control idempotency, local-presence and attention-durability results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Task, approval and steering surfaces are Blazor components. The idempotency, local-presence and attention-durability criteria are unchanged. |

<a id="task-web-22"></a>

### WEB.22 — Artifacts and sandboxing

**Outcome.** Artifact preview runs inside an isolated sandbox (a sandboxed frame whose CSP is re-proven under PRF.11, with JavaScript interop only at that audited sandbox point) so untrusted content never executes in the application origin. Downloads verify permission at access, and no public share links exist in V1.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-22` and ledger record `ledger/tasks/web-22.md` in the Plan repository; task branch `task/web-22` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-49.03](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.03) — full |
| Provides | web-artifact-sandbox |
| Start prerequisites | **artifact** [WEB.19](#task-web-19) — chat shell. *Why:* lives in the shell |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.24](#task-web-24), [WEB.26](#task-web-26) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Artifacts/**` |
| Validation | Sandbox-escape attempt with hostile content; permission-at-access test (bUnit/xUnit); existence-disclosure test on a denied resource; public-share-link absence assertion. |
| Completion evidence | Sandbox escape, permission-at-access and share-link absence results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Self-contained: mostly a client-side iframe/CSP isolation mechanism plus WP25 resource tickets already inherited via the account shell; does not need WP26 or WP52. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The isolation mechanism moves from the React host to the Blazor host with a re-proven sandbox CSP. The sandbox-escape, permission-at-access and share-link criteria are unchanged. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): still-image attachments are shown as metadata cards (type, name and size by magic-byte sniffing) with no decoded still-image preview in V1 Web (S1); the sandboxed artifact preview is unchanged. |

<a id="task-web-23"></a>

### WEB.23 — One-application remote control

**Outcome.** Device applications are listed, an explicit authorized product/installation is selected and frozen per task target; no browser local connection, another-product tool or local-only desktop chat access exists; an offline target shows an honest queued state with expiry.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-23` and ledger record `ledger/tasks/web-23.md` in the Plan repository; task branch `task/web-23` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-49.04](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.04) — all work except the parts mapped to WEB.28 |
| Provides | web-remote-control-ui |
| Start prerequisites | **artifact** [WEB.19](#task-web-19) — chat shell + real device-presence API (inherited). *Why:* the device list itself can be built against the real deployed presence API |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [WEB.28](#task-web-28) — real device bridge dispatch. *Why:* actually reaching a desktop only through the cloud bridge needs the real bridge; the picker/freeze UI itself only needs the contract shape |
| Unblocks | [WEB.24](#task-web-24), [WEB.26](#task-web-26), [WEB.28](#task-web-28) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Devices/**` |
| Validation | Scope/permission, wrong-or-stale-target, loss/retry and expiry scenarios against the exact real artifact/owner boundary |
| Completion evidence | Offline-target queueing and no-local-connection results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Device list and picker are Blazor components. The scope, wrong-target and expiry criteria are unchanged. |

<a id="task-web-24"></a>

### WEB.24 — Offline, degradation and accessibility (chat)

**Outcome.** Honest offline messaging in the Blazor Chat profile, in memory only (no service worker, no persistent chat cache; [WCI-05](../../../architecture/25-web-toolchain-and-sdk.md#rule-wci-05)): unsent input is kept in live component state for the current page session; realtime loss degrades to polling with backfill using the WEB.20 constants; a cloud outage reports unavailable capabilities rather than blanking; every core workflow completes by keyboard.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-24` and ledger record `ledger/tasks/web-24.md` in the Plan repository; task branch `task/web-24` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-49.05](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.05) — full |
| Provides | web-chat-resilience |
| Start prerequisites | **artifact** [WEB.20](#task-web-20) — streaming UI. *Why:* exercises real workflows<br>**artifact** [WEB.21](#task-web-21) — tasks UI. *Why:* exercises real workflows<br>**artifact** [WEB.22](#task-web-22) — artifacts UI. *Why:* exercises real workflows<br>**artifact** [WEB.23](#task-web-23) — device UI. *Why:* exercises real workflows |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.26](#task-web-26) |
| Write scope | `Web:src/ArcForges.Web.App/**`<br>`Web:tests/ArcForges.Web.App.Tests/**` |
| Validation | Offline and reconnection tests (bUnit/xUnit: offline messaging, in-session unsent input kept, no service worker, no persistent chat cache written); polling-degradation test; cloud-outage test; accessibility CI-gated semantic checks (WEB.06) and a manual pass. |
| Completion evidence | Offline, degradation, convergence and accessibility results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021), [WCI-05](../../../architecture/25-web-toolchain-and-sdk.md#rule-wci-05)): The offline criterion is reconciled to in-memory offline behaviour as in WEB.17. Realtime-to-polling degradation keeps the WEB.20 polling constants. |

<a id="task-web-25"></a>

### WEB.25 — Performance budgets (chat)

**Outcome.** Bundle size (compressed Blazor WebAssembly download and startup), first-interactive and interaction-responsiveness budgets are measured per release candidate with a regression gate that catches a deliberate regression. The Blazor WebAssembly budgets are set by a reviewed [AL-06](../../../architecture/10-web-architecture.md#rule-al-06) re-baseline record (owner PRF.11); the React numbers are not carried over silently.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-25` and ledger record `ledger/tasks/web-25.md` in the Plan repository; task branch `task/web-25` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / S |
| Obligations | [WP-49.06](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.06) — full |
| Provides | web-chat-performance |
| Start prerequisites | **artifact** [WEB.19](#task-web-19) — chat shell. *Why:* measures its bundle<br>**artifact** [PRF.11](runtime-proofs.md#task-prf-11) — the measured Blazor WebAssembly profile size and startup and the [AL-06](../../../architecture/10-web-architecture.md#rule-al-06) re-baseline record. *Why:* the chat budgets cannot be set before the proof measures the real profile |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.26](#task-web-26) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Chat/**`<br>`Web:tools/ArcForges.Web.Tooling/Budgets/**` |
| Shared resources | [RES-web-build-config](../shared-resources.md#res-web-build-config) (append) |
| Validation | Budget measurements per release candidate; regression-gate negative test |
| Completion evidence | Budget measurements and regression-gate negative test |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): These are performance budgets, not the cost-control budgets. The regression-gate criterion is kept and the React baseline is re-baselined by reviewed record only. |

<a id="task-web-26"></a>

### WEB.26 — Verify the owned Chat artifact and real integration

**Outcome.** A full real admitted CF turn/tool/approval/reconnect sequence is exercised in a browser using the fixed same-origin session and generated AI gRPC-Web route; a blocked/expired live stream reconciles to the authoritative result without leaking session credentials.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-26` and ledger record `ledger/tasks/web-26.md` in the Plan repository; task branch `task/web-26` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Package acceptance | Records the [WP-49](../../work-packages/49-arcchat-web-companion.md#rule-wp-49) acceptance receipt after every task mapped to the package; tasks outside the package never start from it ([DLV-35](../README.md#rule-dlv-35)) |
| Obligations | [WP-49.90](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.90) — full<br>[WP-49](../../work-packages/49-arcchat-web-companion.md#rule-wp-49) Browser matrix acceptance paragraph (browser-support.v1 for the chat output) — package-level obligation contribution |
| Provides | web-chat-candidate |
| Start prerequisites | **artifact** [WEB.20](#task-web-20) — streaming. *Why:* final join<br>**artifact** [WEB.21](#task-web-21) — tasks/approval. *Why:* final join<br>**artifact** [WEB.22](#task-web-22) — artifacts. *Why:* final join<br>**artifact** [WEB.23](#task-web-23) — remote control. *Why:* final join<br>**artifact** [WEB.24](#task-web-24) — resilience. *Why:* final join<br>**artifact** [WEB.25](#task-web-25) — budgets. *Why:* final join<br>**artifact** [WEB.32](#task-web-32) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03))<br>**artifact** [WEB.33](#task-web-33) — package task delivered. *Why:* the package acceptance receipt verifies every task mapped to the package ([DLV-03](../README.md#rule-dlv-03)) |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [WEB.27](#task-web-27) — real Harness. *Why:* unlike WP47's deferrable numeric join, [WP-49](../../work-packages/49-arcchat-web-companion.md#rule-wp-49)'s own text states "49 consumes 52" as a hard requirement recorded at this task's own gate, not deferred to WP50 |
| Unblocks | [REL.05](release.md#task-rel-05) |
| Write scope | `Web:src/ArcForges.Web.App/**` |
| Validation | Full real admitted CF turn/tool/approval/reconnect in a browser — local opt-in per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Owned-artifact-and-real-integration receipt; contributes its scoped evidence toward [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) (closed later at WP50) |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The integration receipt is unchanged; the browser run is against the Blazor Chat profile and the generated C# AI gRPC-Web route. |

<a id="task-web-27"></a>

### WEB.27 — Real CF Harness generation/tool loop observed end to end in the browser

**Outcome.** real admitted generation and tool proposal replace the contract-bound fixture turn endpoint in Chat

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-27` and ledger record `ledger/tasks/web-27.md` in the Plan repository; task branch `task/web-27` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-49.01](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.01) — real-integration closure<br>[WP-49.02](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.02) — real-integration closure |
| Start prerequisites | **artifact** [WEB.20](#task-web-20) — real, delivered outcome of WEB.20 (Conversation and generated output streams). *Why:* this integration exercises the real conversation and generated output streams instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.21](#task-web-21) — real, delivered outcome of WEB.21 (Tasks, approval and steering). *Why:* this integration exercises the real tasks, approval and steering instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [HAR.00](harness.md#task-har-00) — real, delivered outcome of HAR.00 (Turn loop, tool batching and bounds (RunWorkflow core)). *Why:* this integration exercises the real turn loop, tool batching and bounds (RunWorkflow core) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [HAR.03](harness.md#task-har-03) — real generated streaming and durable output. *Why:* the browser end-to-end scenario reads real Harness output |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [HAR.05](harness.md#task-har-05), [WEB.20](#task-web-20), [WEB.21](#task-web-21), [WEB.26](#task-web-26) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | real admitted generation and tool proposal replace the contract-bound fixture turn endpoint in Chat |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Stack-neutral acceptance; no change to outcome, validation or evidence. The browser run is against the C# Chat profile (WEB.19/WEB.20) and the generated C# clients. |

<a id="task-web-28"></a>

### WEB.28 — Real desktop tool dispatch from the browser companion

**Outcome.** a browser-initiated remote task actually reaches a desktop through the durable bridge

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-28` and ledger record `ledger/tasks/web-28.md` in the Plan repository; task branch `task/web-28` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-49.02](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.02) — device-dispatch closure<br>[WP-49.04](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.04) — real-integration closure |
| Start prerequisites | **artifact** [WEB.21](#task-web-21) — real, delivered outcome of WEB.21 (Tasks, approval and steering). *Why:* this integration exercises the real tasks, approval and steering instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.23](#task-web-23) — real, delivered outcome of WEB.23 (One-application remote control). *Why:* this integration exercises the real one-application remote control instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [DEV.02](device-bridge.md#task-dev-02) — the real durable target queue. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.03](device-bridge.md#task-dev-03) — real owner reauthorization on the desktop. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.06](device-bridge.md#task-dev-06) — real remote approval and steering. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.07](device-bridge.md#task-dev-07) — real offline expiry and unknown-effect recovery. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier<br>**artifact** [DEV.12](device-bridge.md#task-dev-12) — the cross-repository (toolRequestId, attemptId, commandId) agreement. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.21](#task-web-21), [WEB.23](#task-web-23) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | a browser-initiated remote task actually reaches a desktop through the durable bridge |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Stack-neutral acceptance; no change to outcome, validation or evidence. The browser companion is the C# Blazor Chat profile. |

<a id="task-web-29"></a>

### WEB.29 — Real commerce/policy provider evidence for the account portal

**Outcome.** hosted checkout, entitlement reasons and rate-limit/recovery text reflect a real test-mode ledger and policy service, not contract fixtures

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-29` and ledger record `ledger/tasks/web-29.md` in the Plan repository; task branch `task/web-29` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-48.04](../../work-packages/48-account-portal.md#rule-wp-48.04) — real-provider-evidence closure |
| Start prerequisites | **artifact** [WEB.14](#task-web-14) — real, delivered outcome of WEB.14 (Subscription, capacity, credits and hosted checkout). *Why:* this integration exercises the real subscription, capacity, credits and hosted checkout instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [COM.14](commerce.md#task-com-14) — real, delivered outcome of COM.14 (Technical commerce closure and live-gate staging). *Why:* this integration exercises the real technical commerce closure and live-gate staging instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [POL.08](policy.md#task-pol-08) — real, delivered outcome of POL.08 (Publication, staleness and last-known-good (server side)). *Why:* this integration exercises the real publication, staleness and last-known-good (server side) instead of a substitute, so it cannot start before that outcome exists |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.18](#task-web-18) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | hosted checkout, entitlement reasons and rate-limit/recovery text reflect a real test-mode ledger and policy service, not contract fixtures |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Stack-neutral acceptance; no change to outcome, validation or evidence. The account portal under test is the Blazor Account profile. |

<a id="task-web-30"></a>

### WEB.30 — Real Blazor WebAssembly Web client against deployed browser session/PublicApi/realtime

**Outcome.** Real C# gRPC-Web client (Grpc.Net.Client.Web, generated from Contracts) with cookie, CSRF and Origin session behaviour and realtime streams against the deployed Cloud, beyond fixture-backed proofs (no fixture or test double stands in for the deployed ingress).

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web`; also touches Cloud |
| Claim, branch and ledger | `claims/web-30` and ledger record `ledger/tasks/web-30.md` in the Plan repository; task branch `task/web-30` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-23.05](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.05) — Web real-consumer integration |
| Start prerequisites | **artifact** [CLOUD.19](cloud.md#task-cloud-19) — real, delivered outcome of CLOUD.19 (Browser cookie-session adapter and full account-surface closure). *Why:* this integration exercises the real browser cookie-session adapter and full account-surface closure instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.26](cloud.md#task-cloud-26) — real, delivered outcome of CLOUD.26 (Generated C#/TypeScript/Kotlin clients against Identity/Workspace/Device). *Why:* this integration exercises the real generated C#/TypeScript/Kotlin clients against Identity/Workspace/Device instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.29](cloud.md#task-cloud-29) — real, delivered outcome of CLOUD.29 (Stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells)). *Why:* this integration exercises the real stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.07](#task-web-07) — real, delivered outcome of WEB.07 (Independence and atomic deployment). *Why:* this integration exercises the real independence and atomic deployment instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.14](#task-web-14) — real, delivered outcome of WEB.14 (Subscription, capacity, credits and hosted checkout). *Why:* this integration exercises the real subscription, capacity, credits and hosted checkout instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.19](#task-web-19) — real, delivered outcome of WEB.19 (Chat shell: route composition and design-system integration). *Why:* this integration exercises the real chat shell: route composition and design-system integration instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.11](runtime-proofs.md#task-prf-11) — the Blazor WebAssembly production proof (PRF.11, successor of the superseded React PRF.08). *Why:* the real-client integration builds on the proven Blazor transport, session and CSRF semantics |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.28](cloud.md#task-cloud-28), [WEB.31](#task-web-31) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Real C# gRPC-Web client, cookie/CSRF/Origin session behaviour and realtime streams against the deployed Cloud, beyond fixture-backed proofs. |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The React/MSW wording is replaced by the C# Blazor client: the same real deployed session, PublicApi and realtime criteria. SUB-web-msw-fixtures is restated for the C# client; its test-only rule is kept. PRF.08 is retargeted to PRF.11. |

<a id="task-web-31"></a>

### WEB.31 — Full browser-support.v1 matrix across all Web-facing outputs

**Outcome.** Supported/degraded/blocked behavior across every output's flows on real browser/OS patches; [WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) joins all production hashes and real browser evidence

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web`; also touches Cloud |
| Claim, branch and ledger | `claims/web-31` and ledger record `ledger/tasks/web-31.md` in the Plan repository; task branch `task/web-31` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) Browser matrix acceptance appendix, full cross-area join — Browser matrix acceptance appendix, full cross-area join |
| Start prerequisites | **artifact** [OPS.05](operations.md#task-ops-05) — real, delivered outcome of OPS.05 (Operator console and support access). *Why:* this integration exercises the real operator console and support access instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.07](#task-web-07) — real, delivered outcome of WEB.07 (Independence and atomic deployment). *Why:* this integration exercises the real independence and atomic deployment instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.14](#task-web-14) — real, delivered outcome of WEB.14 (Subscription, capacity, credits and hosted checkout). *Why:* this integration exercises the real subscription, capacity, credits and hosted checkout instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.19](#task-web-19) — real, delivered outcome of WEB.19 (Chat shell: route composition and design-system integration). *Why:* this integration exercises the real chat shell: route composition and design-system integration instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.30](#task-web-30) — the real Blazor WebAssembly client against the deployed browser session. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.28](cloud.md#task-cloud-28) — the [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) browser-matrix Cloud part accepted. *Why:* the full browser matrix includes the Cloud part that the [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) closure accepts |
| Unblocks | none |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Supported/degraded/blocked behavior across every output's flows on real browser/OS patches; [WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) joins all production hashes and real browser evidence |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): Stack-neutral acceptance; no change to outcome, validation or evidence. The browser matrix runs against the C# Web profiles. Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023)): The browser-support matrix has no macOS or Safari rows, because macOS is outside the delivery scope. Supported, degraded and blocked criteria are otherwise unchanged, and the matrix runs against the C# Blazor profiles. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: Safari rows, macOS OS entries and any macOS or iOS Safari claim or test are out of scope, not completed ([P2-023](../../../decisions/phase-2-specification-decisions.md#rule-p2-023)). |

<a id="task-web-32"></a>

### WEB.32 — ArcScope workspace in the Web companion: library and reports

**Outcome.** The Web ArcScope library: projects, sessions, findings and annotations, report reading with provenance and stored chart snapshots, exported-report download through resource tickets, sessions and reports attached to assistant conversations, and the ArcScope notification kinds. Under [P2-022](../../../decisions/phase-2-specification-decisions.md#rule-p2-022) the exported report PDF (arcscope.report.pdf.v1) is presented only through the browser's built-in PDF viewer (a sandboxed iframe with CSP isolation where it can be enforced, otherwise download or open; requirements/12 line 421) or downloaded as an opaque file; the Web companion has no app-side PDF parser, text extraction, tile rendering or PDF library, and no native PDF preview is kept.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-32` and ledger record `ledger/tasks/web-32.md` in the Plan repository; task branch `task/web-32` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-49.07](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.07) — full |
| Provides | web-arcscope-workspace |
| Start prerequisites | **artifact** [WEB.19](#task-web-19) — the companion route shell and design-system integration. *Why:* the workspace is a route set of the companion deployment<br>**contract** [CON.24](contracts.md#task-con-24) — the generated C# library operations. *Why:* the views call the library operations through the generated C# client |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.68](cloud.md#task-cloud-68) — the deployed library read model. *Why:* acceptance reads a real synced workspace<br>**integration** [SCOPE.22](arcscope.md#task-scope-22) — the delivered desktop project/session and report publication adapter. *Why:* acceptance must consume desktop-produced synced metadata and readable reports rather than a fixture; UI development remains parallel |
| Unblocks | [WEB.26](#task-web-26) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Scope/**` |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | A report synced from ArcScope desktop found, read with provenance (in the Web report reader or through the browser's built-in PDF viewer) and downloaded on Web with provenance; revocation, ticket expiry and accessibility results; a negative check that the Web App output references no PDF parser or renderer. |
| Baseline (unreviewed unless accepted) | not-started Observed none. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The ArcScope library views are Blazor components in the Web companion. The generated-operation dependency is now the C# client. Acceptance is unchanged. |

<a id="task-web-33"></a>

### WEB.33 — Cloud simulator console in the Web companion

**Outcome.** The simulator console: definitions, immutable scenario versions with validation errors, start, pause, resume and cancel with expectedRev and legal predecessor-state guards, run state with complete-or-partial extent, and the committed segment manifest with resumable, hash-verified downloads. Run history is discovered through simulation.listRuns on a fresh session.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-33` and ledger record `ledger/tasks/web-33.md` in the Plan repository; task branch `task/web-33` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / M |
| Obligations | [WP-49.08](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.08) — full |
| Provides | web-simulator-console |
| Start prerequisites | **artifact** [WEB.19](#task-web-19) — the companion route shell and design-system integration. *Why:* the console is a route set of the companion deployment<br>**contract** [CON.21](contracts.md#task-con-21) — the generated C# simulation operations. *Why:* the console calls the simulation operations through the generated C# client |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [SIM.05](simulator.md#task-sim-05) — the deployed simulation operations. *Why:* acceptance runs a real scenario |
| Unblocks | [WEB.26](#task-web-26) |
| Write scope | `Web:src/ArcForges.Web.App/Features/Simulation/**` |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | A scenario created and run from the browser with every desktop off, completed or cancelled with the correct extent, and its committed segments downloaded and verified. Authorized run discovery, filter paging and denied cross-workspace access. |
| Baseline (unreviewed unless accepted) | not-started Observed none. |
| Notes | Planning repair 2026-10-08 ([DLV-34](../README.md#rule-dlv-34); [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021)): The simulator console is a Blazor route set of the Web companion. Its run-control, extent and segment-download acceptance is unchanged. |

<a id="task-web-40"></a>

### WEB.40 — Blazor migration of the existing Web (C# static Site, Blazor WebAssembly profiles, C# policy)

**Outcome.** Migrates the existing Web repository to the C#-first stack with equal acceptance. (1) The C# static Site generator (ArcForges.Web.Site, first-party Razor HtmlRenderer) reproduces the current public pages (/, /hello, /cloud-hello and the documentation, legal and download inventory) with no runtime JavaScript ([TB-01](../../../architecture/18-editing-and-rich-content.md#rule-tb-01)) and replaces apps/site. (2) Blazor WebAssembly standalone Account and Chat deployment profiles (ArcForges.Web.App, RunAOTCompilation=false by default) replace apps/app with identical cookie-session, antiforgery/CSRF, Origin, exact-value and typed-failure semantics. The Operations console keeps its own standalone Blazor WebAssembly profile (ArcForges.Web.Operations) on a separate origin and identity: this task creates only its skeleton, and the operator features are built by OPS.05. (3) packages/ui becomes the Razor class library ArcForges.Web.Ui. (4) Every existing test whose subject stays in V1 is ported one-for-one to xUnit (contract, provenance, policy) or bUnit (components), with Microsoft.Playwright for .NET kept as local opt-in test-only tooling (axe-core injected only into the page under test; no npm-hosted test tooling remains). (5) CI and deploy build the C# outputs once and promote the same bytes to Cloudflare Static Assets through the unchanged thin worker/index.js. The existing main-push Cloudflare deploy job in .github/workflows/ci.yml stays as a deployment step outside validation (section 6 decision 2); its rollback acceptance is a named gate recorded by a local operator run receipt. (6) Every NuGet package in the closure is admitted with provenance and licence receipts under eng/policy. (7) The GOV.11 policy is re-implemented in C# as the successor, with one solution and central package management, an exact .NET SDK pin, SDK-to-UI licence separation, generated wire types only, no private, server or local-RPC imports, a desktop JS/DOM prohibition, Blazor WebAssembly standalone as the only allowed Blazor target, Blazor Server render modes and circuits forbidden, no esproj in portable references, no implicit restore or install and no production dev server, and no test helpers in the release route graph; each rule has a passing and a failing negative example; any exact-pattern or Gitleaks exception change needs the GOV.11 review standard (named authority, independent exact-head review, retained CI before merge). (8) JavaScript interop is limited to the listed audited points (WebAuthn, clipboard, download and share, sandboxed preview).

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-40` and ledger record `ledger/tasks/web-40.md` in the Plan repository; task branch `task/web-40` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / XL |
| Obligations | [WP-05.01](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.01) — Web slice: SDK-to-UI licence separation (carried from GOV.11)<br>[WP-05.02](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.02) — wire the forbidden-term scanner into Web's own PR build (carried from GOV.11)<br>[WP-05.04](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.04) — Web banned dependency and route fixtures (carried from GOV.11)<br>[WP-05](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05) Web repository and architecture assertions (unlabeled paragraph after [WP-05.06](../../work-packages/05-architecture-and-repository-policy-tests.md#rule-wp-05.06)): Node/TS import and dependency checks - one Web workspace/lock, exact Node/npm/generator pins, SDK-to-UI licence separation, generated wire types only, no private/server/local-RPC imports, desktop JS/DOM prohibition scoped to desktop graphs, no obsolete Blazor target, no esproj in portable managed references, no implicit npm install or production dev/HMR server, no TS fixtures/test helpers in the release route graph — package-level obligation contribution (carried from GOV.11; amended by [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) item 2: Blazor WebAssembly standalone is the allowed Blazor target, Blazor Server is forbidden, and the Node/TS mechanism is replaced by the C# policy) |
| Provides | web-csharp-migration-baseline; web-csharp-policy-suite; web-nuget-closure |
| Start prerequisites | **artifact** [GOV.03](governance.md#task-gov-03) — build governance, packaging policy and analyzers (inherited). *Why:* the C# solution, analyzers and packaging policy are the GOV.03 mechanism<br>**contract** [CON.07](contracts.md#task-con-07) — generated C# gRPC-Web session and device client and the BrowserSession HTTP exception codecs from the published Contracts NuGet candidate (precondition: the NuGet identity is verified at start from the CON.07 publication record). *Why:* the Account profile session and CSRF calls consume the generated C# records, not handwritten DTOs |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.85](cloud.md#task-cloud-85), [CON.40](contracts.md#task-con-40), [OPS.05](operations.md#task-ops-05), [PRF.11](runtime-proofs.md#task-prf-11), [WEB.01](#task-web-01), [WEB.08](#task-web-08), [WEB.10](#task-web-10) |
| Write scope | `Web:src/ArcForges.Web.Site/** (C# HtmlRenderer static generator replacing apps/site)`<br>`Web:src/ArcForges.Web.App/** (Blazor WebAssembly Account and Chat profiles replacing apps/app)`<br>`Web:src/ArcForges.Web.Ui/** (Razor class library replacing packages/ui)`<br>`Web:tests/ArcForges.Web.Site.Tests/**`<br>`Web:tests/ArcForges.Web.App.Tests/**`<br>`Web:tests/ArcForges.Web.Ui.Tests/**`<br>`Web:tests/ArcForges.Web.Policy.Tests/**`<br>`Web:tools/ArcForges.Web.Tooling/** (out of scope under S17(a): the C# replacement of tooling/*.ts is not created by WEB.40)`<br>`Web:Directory.Packages.props (new central NuGet pins)`<br>`Web:nuget.config (new locked package sources)`<br>`Web:src/**/packages.lock.json (per-project NuGet lock files)`<br>`Web:win.slnx (C# projects replace the esproj entry)`<br>`Web:ArcForges.Web.esproj (retired after parity, replaced by csproj references)`<br>`Web:Directory.Build.targets (keep the AGPL/Apache licence-boundary MSBuild targets)`<br>`Web:package.json and Web:package-lock.json (reduced to wrangler, Node build and deploy tooling only; no npm-hosted test tooling remains, brief section 5 item 8)`<br>`Web:apps/** and Web:packages/ui/** (React sources removed after the one-for-one port; history stays in git)`<br>`Web:tooling/*.ts, Web:tests/unit/*.ts, Web:tests/fixtures/*.ts, Web:vitest.config.ts, Web:tsconfig.json, Web:biome.json (retained where S17(a) takes their port out of scope; otherwise removed after the one-for-one port)`<br>`Web:tests/browser/** (Microsoft.Playwright for .NET, test-only local opt-in tooling)`<br>`Web:wrangler.json`<br>`Web:worker/** (thin adapter kept)`<br>`Web:.github/workflows/ci.yml`<br>`Web:eng/policy/** (dependency-policy.json NuGet admissions; successor architecture policy)`<br>`Web:eng/policy/dependency-reviews/** (immutable NuGet closure receipts)`<br>`Web:eng/provenance/** (new successor records; historical records kept)`<br>`Web:.gitleaks.toml`<br>`Web:docs/** (factual updates to development, deploying, provenance and validation)`<br>`Web:src/ArcForges.Web.Operations/** (Operations profile skeleton only: project, shell routes and separate-origin configuration; no operator feature code)`<br>`Web:tests/ArcForges.Web.Operations.Tests/** (skeleton tests only)`<br>`Web:tests/provenance/** (retained unchanged: the xUnit successor for every provenance test is out of scope under S17(a), not completed)`<br>`Web:.github/dependabot.yml (npm groups react-and-router, contracts, cloudflare and tooling retarget to the NuGet and wrangler closure in the same change; no open Dependabot pull request is touched)` |
| Shared resources | [RES-web-build-config](../shared-resources.md#res-web-build-config) (append), [RES-architecture-tests](../shared-resources.md#res-architecture-tests) (append), [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append), [RES-web-shared-ui](../shared-resources.md#res-web-shared-ui) (append) |
| Validation | Windows build and test of win.slnx with the pinned .NET 10 SDK and central package management (dotnet build and test, offline after an approved restore). One-for-one port table: every retired TS or React test whose subject stays in V1 has an xUnit or bUnit successor with the same positive and negative cases (tests/unit, tests/provenance, tests/fixtures). The migrated public page inventory is compared with the React output before apps/site is removed. Account and Chat profile tests for identical session, CSRF, exact-value and typed-failure semantics. The policy suite has positive and negative fixtures for every GOV.11 rule, with Blazor WebAssembly allowed and Blazor Server forbidden. NuGet closure licence and provenance receipts. Microsoft.Playwright for .NET only as local opt-in test tooling, with axe-core injected only into the page under test; the CI accessibility gate is the xUnit/bUnit semantic set (section 6 decision 3). The existing main-push Cloudflare deploy job is a deployment step outside validation (section 6 decision 2). No hosted browser, device or live-service CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). Linux-affected checks run once in WSL2 Debian on a Linux-native filesystem ([P2-024](../../../decisions/phase-2-specification-decisions.md#rule-p2-024)). The Operations profile skeleton is covered by the same exact CSP token-set assertion as the Account and Chat profiles (script-src 'self' 'wasm-unsafe-eval' plus required hashes; never unsafe-eval or unsafe-inline) and contains no operator feature code. Dependabot: .github/dependabot.yml ports its npm groups to NuGet and wrangler groups in the same change as the closure. Any Gitleaks generic-api-key exception change under the GOV.11 successor policy needs the GOV.11 review standard (named authority, independent exact-head review, retained CI before merge); the xUnit policy suite fails on any count other than the enumerated set. |
| Completion evidence | One-for-one port table with a successor for every retired test; byte comparison of the migrated public page inventory; CI run receipt for the C# build; policy negative-example results; NuGet closure provenance and licence receipts; coordination note with Cloud on CLOUD.71 bundle naming. |
| Baseline (unreviewed unless accepted) | not-started Observed 2026-10-08 at Web a469064: React Router apps/site generator; React/Vite apps/app probe profiles (PRF.08 delivered offline, superseded); packages/ui a 60-line React Shell/Button; Node/TS policy under eng/policy and tooling/; GOV.11 policy in eng/policy/architecture.ts that forbids Blazor at lines 71 and 185-187 (this task reverses that one rule). Not started; no ledger record. |
| Notes | Decisions this task depends on: [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) items 2 and 8 (Microsoft.Playwright for .NET stays test-only local tooling, and the Blazor-free public Site per [TB-01](../../../architecture/18-editing-and-rich-content.md#rule-tb-01)); brief section 5 item 8 (no npm-hosted test tooling remains); brief section 6 decision 3 (accessibility tooling: the CI gate is the bUnit/xUnit semantic assertion set, and axe-core is local opt-in only through Microsoft.Playwright for .NET, injected only into the page under test); section 6 decision 2 (the existing main-push Cloudflare deploy job stays as a deployment step). Under the same decision 3 no accessibility analyzer NuGet package is in the CI gate. The CON.07 NuGet identity is a start precondition verified from the CON.07 publication record. The port of tooling/*.ts to C# is out of scope under S17(a), not completed. It creates the Operations profile skeleton that OPS.05 builds on. Bundle naming coordinates with CLOUD.85 and CLOUD.71. CON.40 (Contracts consumer migration) starts after WEB.40 delivers, so this task does not start on CON.40. Decision basis: [P2-021](../../../decisions/phase-2-specification-decisions.md#rule-p2-021) (decision obligations are reserved for adoption and governance tasks, so the decision is cited here rather than as an obligation). Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction): reduced: OPS.11 package-review routes are out of scope, not completed. Tests whose only subject is retired React, Vite or npm tooling or an excluded product (ArcSlate, ArcNotes, macOS) retire with an explicit successor record, not a port. GOV.11 is out; its C# successor is item (7) of this task. Planning repair 2026-10-09 ([P2-026](../../../decisions/phase-2-specification-decisions.md#rule-p2-026); scope correction, brief section 11 S17(a)): reduced: the remaining Node TypeScript build, policy and provenance tooling port is out of scope, not completed. That covers dependency-policy.ts, provenance.ts, licence-boundary.ts, project.ts, build-identity.ts, cloudflare.ts and candidate.ts (tools/ArcForges.Web.Tooling is not created), the node:test provenance tests build-identity, legal-path, source, csharp-candidate, lock-provenance and cloudflare-delivery, and the xUnit successor for every provenance test. Node stays for wrangler and these build tools; product and business code stays C# (Blazor) and the Worker stays a thin adapter. The outcome and validation clauses that name that port are carved out by this note, not completed. |
