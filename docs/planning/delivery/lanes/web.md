# Web — delivery tasks

> Generated from [the delivery graph](../delivery-graph.json) by Plan `tools/delivery.py`; do not edit by hand. Rules and definitions: [delivery model](../README.md).

Static site, shared consumer design system, Account portal and ArcChat Web companion.

Tasks: 31 · Owning repositories: Web · Integration owner(s): Web integration owner

| Task | Title | Kind | Size | Start prerequisites | Baseline |
|---|---|---|---|---|---|
| [WEB.01](#task-web-01) | React static generation and determinism engine | producer | L | [GOV.03](governance.md#task-gov-03) (artifact) | not-started |
| [WEB.02](#task-web-02) | Versioned public content and pricing inputs (catalogue.json) | feature | M | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.03](#task-web-03) | Rendering and performance | feature | M | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.04](#task-web-04) | Internationalisation | feature | M | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.05](#task-web-05) | Documentation, downloads and legal surfaces | feature | M | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.06](#task-web-06) | Accessibility and analytics | feature | S | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.07](#task-web-07) | Independence and atomic deployment | release | S | [WEB.01](#task-web-01) (artifact) | not-started |
| [WEB.08](#task-web-08) | Owned consumer design system (packages/ui) | producer | L | [GOV.03](governance.md#task-gov-03) (artifact) | not-started |
| [WEB.09](#task-web-09) | Verify the owned Site artifact and real integration | integration | S | [WEB.02](#task-web-02) (artifact), [WEB.03](#task-web-03) (artifact), [WEB.04](#task-web-04) (artifact), [WEB.05](#task-web-05) (artifact), [WEB.06](#task-web-06) (artifact), [WEB.07](#task-web-07) (artifact), [WEB.08](#task-web-08) (artifact) | not-started |
| [WEB.10](#task-web-10) | Account shell: route graph, deployment-profile selection, generated-SDK wiring | producer | XL | [WEB.08](#task-web-08) (artifact), [CON.07](contracts.md#task-con-07) (contract) | not-started |
| [WEB.11](#task-web-11) | Real browser session and step-up acceptance | feature | L | [CLOUD.19](cloud.md#task-cloud-19) (artifact), [WEB.10](#task-web-10) (artifact) | not-started |
| [WEB.12](#task-web-12) | Account and security surfaces | feature | M | [WEB.11](#task-web-11) (artifact) | not-started |
| [WEB.13](#task-web-13) | Workspace, storage and usage | feature | M | [WEB.10](#task-web-10) (artifact) | not-started |
| [WEB.14](#task-web-14) | Subscription, capacity, credits and hosted checkout | feature | L | [WEB.10](#task-web-10) (artifact), [CON.08](contracts.md#task-con-08) (contract) | not-started |
| [WEB.15](#task-web-15) | Data export and deletion | feature | M | [WEB.10](#task-web-10) (artifact), [CON.22](contracts.md#task-con-22) (contract) | not-started |
| [WEB.16](#task-web-16) | Origin security and performance (account) | feature | M | [WEB.10](#task-web-10) (artifact) | not-started |
| [WEB.17](#task-web-17) | Offline, degradation and accessibility (account) | feature | M | [WEB.12](#task-web-12) (artifact), [WEB.13](#task-web-13) (artifact), [WEB.14](#task-web-14) (artifact), [WEB.15](#task-web-15) (artifact) | not-started |
| [WEB.18](#task-web-18) | Verify the owned Account artifact and real integration | integration | M | [WEB.11](#task-web-11) (artifact), [WEB.12](#task-web-12) (artifact), [WEB.13](#task-web-13) (artifact), [WEB.14](#task-web-14) (artifact), [WEB.15](#task-web-15) (artifact), [WEB.16](#task-web-16) (artifact), [WEB.17](#task-web-17) (artifact), [WEB.29](#task-web-29) (artifact) | not-started |
| [WEB.19](#task-web-19) | Chat shell: route composition and design-system integration | producer | L | [WEB.08](#task-web-08) (artifact), [WEB.10](#task-web-10) (artifact) | not-started |
| [WEB.20](#task-web-20) | Conversation and generated output streams | feature | L | [WEB.19](#task-web-19) (artifact) | not-started |
| [WEB.21](#task-web-21) | Tasks, approval and steering | feature | L | [WEB.19](#task-web-19) (artifact) | not-started |
| [WEB.22](#task-web-22) | Artifacts and sandboxing | feature | M | [WEB.19](#task-web-19) (artifact) | not-started |
| [WEB.23](#task-web-23) | One-application remote control | feature | M | [WEB.19](#task-web-19) (artifact) | not-started |
| [WEB.24](#task-web-24) | Offline, degradation and accessibility (chat) | feature | M | [WEB.20](#task-web-20) (artifact), [WEB.21](#task-web-21) (artifact), [WEB.22](#task-web-22) (artifact), [WEB.23](#task-web-23) (artifact) | not-started |
| [WEB.25](#task-web-25) | Performance budgets (chat) | feature | S | [WEB.19](#task-web-19) (artifact) | not-started |
| [WEB.26](#task-web-26) | Verify the owned Chat artifact and real integration | integration | M | [WEB.20](#task-web-20) (artifact), [WEB.21](#task-web-21) (artifact), [WEB.22](#task-web-22) (artifact), [WEB.23](#task-web-23) (artifact), [WEB.24](#task-web-24) (artifact), [WEB.25](#task-web-25) (artifact) | not-started |
| [WEB.27](#task-web-27) | Real CF Harness generation/tool loop observed end to end in the browser | integration | M | [WEB.20](#task-web-20) (artifact), [WEB.21](#task-web-21) (artifact), [HAR.00](harness.md#task-har-00) (artifact), [HAR.03](harness.md#task-har-03) (artifact) | not-started |
| [WEB.28](#task-web-28) | Real desktop tool dispatch from the browser companion | integration | M | [WEB.21](#task-web-21) (artifact), [WEB.23](#task-web-23) (artifact), [DEV.02](device-bridge.md#task-dev-02) (artifact), [DEV.03](device-bridge.md#task-dev-03) (artifact), [DEV.06](device-bridge.md#task-dev-06) (artifact), [DEV.07](device-bridge.md#task-dev-07) (artifact), [DEV.12](device-bridge.md#task-dev-12) (artifact) | not-started |
| [WEB.29](#task-web-29) | Real commerce/policy provider evidence for the account portal | integration | M | [WEB.14](#task-web-14) (artifact), [COM.14](commerce.md#task-com-14) (artifact), [POL.08](policy.md#task-pol-08) (artifact) | not-started |
| [WEB.30](#task-web-30) | Real React Web client against deployed browser session/PublicApi/realtime | integration | M | [CLOUD.19](cloud.md#task-cloud-19) (artifact), [CLOUD.26](cloud.md#task-cloud-26) (artifact), [CLOUD.29](cloud.md#task-cloud-29) (artifact), [WEB.07](#task-web-07) (artifact), [WEB.14](#task-web-14) (artifact), [WEB.19](#task-web-19) (artifact), [PRF.08](runtime-proofs.md#task-prf-08) (artifact) | not-started |
| [WEB.31](#task-web-31) | Full browser-support.v1 matrix across all Web-facing outputs | integration | M | [OPS.05](operations.md#task-ops-05) (artifact), [WEB.07](#task-web-07) (artifact), [WEB.14](#task-web-14) (artifact), [WEB.19](#task-web-19) (artifact), [WEB.30](#task-web-30) (artifact) | not-started |

## Tasks

<a id="task-web-01"></a>

### WEB.01 — React static generation and determinism engine

**Outcome.** React Router build-time pre-rendering (SSR disabled) generates the full public locale/URL inventory, documentation versions, sitemap, metadata and redirects, deterministically, with no Account/Chat route bundle or private config leaking into the static output.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-01` and ledger record `ledger/tasks/web-01.md` in the Plan repository; task branch `task/web-01` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-47.00](../../work-packages/47-static-public-site.md#rule-wp-47.00) — full |
| Provides | web-static-generator |
| Start prerequisites | **artifact** [GOV.03](governance.md#task-gov-03) — Node/npm workspace and toolchain pins. *Why:* already satisfied — the repo's root package.json/workspaces/.node-version already implement this |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.02](#task-web-02), [WEB.03](#task-web-03), [WEB.04](#task-web-04), [WEB.05](#task-web-05), [WEB.06](#task-web-06), [WEB.07](#task-web-07) |
| Write scope | `Web:apps/site/**` |
| Shared resources | [RES-contract-consumer-pins](../shared-resources.md#res-contract-consumer-pins) (append) |
| Validation | Two full builds with identical inputs compared byte-for-byte; no-script navigation/content tests; single-content-change diff; build with network disabled after approved restore — CI-eligible offline checks |
| Completion evidence | Determinism comparison and diff-minimality results |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: apps/site already has a working react-router static generator (react-router.config.ts prerenders /, /hello, /cloud-hello) with a working build/deploy pipeline; needs generalizing to the full catalogue-driven public inventory |
| Notes | Its only real start need (WP00/WP02) is already satisfied; the current serial plan defers WP47 until after WP40, but nothing blocks starting this immediately. |

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
| Write scope | `Web:apps/site/content/**`<br>`Web:apps/site/app/catalogue.json` |
| Validation | Hard-coded-version/price scan; comparison of public projection to the selected approved snapshot — offline |
| Completion evidence | No independently hard-coded product version/private supplier price |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Private candidate builds may use named test-only offer/release fixtures per [WP-47.01](../../work-packages/47-static-public-site.md#rule-wp-47.01); the real WP42/44 numeric join for public promotion is explicitly deferred to WP50, not required to close this task's own gate. |

<a id="task-web-03"></a>

### WEB.03 — Rendering and performance

**Outcome.** Above-the-fold content ships in delivered HTML, assets are content-hashed with short-lived HTML caching, no blocked third-party resource sits on the critical path, and p75 LCP/INP/CLS budgets are met.

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
| Write scope | `Web:apps/site/**`<br>`Web:tooling/**` |
| Shared resources | [RES-web-build-config](../shared-resources.md#res-web-build-config) (append) |
| Validation | No-script render test; critical-path resource audit; p75 performance measurement; global-reachability check on every third-party host — offline/lab |
| Completion evidence | No-script render, critical-path audit and performance measurements |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-04"></a>

### WEB.04 — Internationalisation

**Outcome.** Locale-scoped URLs with alternate-language annotations, no client-only switching and no trapping redirect; every user-visible string, including generated pages, is localisable.

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
| Write scope | `Web:apps/site/**` |
| Validation | Locale routing/annotation tests, no-trap assertion, pseudo-localisation pass — offline |
| Completion evidence | Locale routing, no-trap and pseudo-localisation results |
| Baseline (unreviewed unless accepted) | not-started |

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
| Write scope | `Web:apps/site/content/**`<br>`Web:apps/site/app/routes/**` |
| Validation | Documentation version routing; download integrity verification against published hashes; no-account-gate assertion; legal version-history tests — offline against labelled fixtures |
| Completion evidence | Download integrity, no-gate and legal versioning results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Private candidate download fixtures are labelled; public promotion with real signed Desktop/Android artifacts is joined at WP50, not required to close this task. |

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
| Write scope | `Web:apps/site/**` |
| Validation | Automated accessibility checks (axe-core, already a pinned devDependency) plus a dated manual verification; analytics payload audit — offline |
| Completion evidence | Accessibility checks pass with a dated manual record; analytics carry no cross-site identifier |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: @axe-core/playwright is already a pinned devDependency in package.json though no pages exist to audit yet |

<a id="task-web-07"></a>

### WEB.07 — Independence and atomic deployment

**Outcome.** The site remains fully available during a full Cloud outage, deploys atomically per surface from a promoted artifact, and rollback restores the previous artifact set.

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
| Write scope | `Web:wrangler.json`<br>`Web:worker/**`<br>`Web:.github/workflows/ci.yml`<br>`Web:tooling/cloudflare.ts` |
| Shared resources | [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append), [RES-web-build-config](../shared-resources.md#res-web-build-config) (append) |
| Validation | Cloud-outage independence test, atomic deployment test, rollback test — offline/local against the real Cloudflare account under existing CI secrets |
| Completion evidence | A full cloud outage leaves the site fully available; deployment is atomic; rollback restores the previous set |
| Baseline (unreviewed unless accepted) | not-started Observed partial, unreviewed: wrangler.json + worker/index.js (www redirect) + the CI deploy job already implement build-once/promote-same-bytes deployment to Cloudflare for the site; this task extends/validates it, not builds it fresh |

<a id="task-web-08"></a>

### WEB.08 — Owned consumer design system (packages/ui)

**Outcome.** packages/ui grows from a placeholder Shell/Button into a full design-token system (typography, spacing, color, themes), owned accessible primitives, a test-only component catalogue, approved visual baselines and reusable account/usage/chat primitives, with localization/long-label/mobile-nav/focus/reduced-motion/loading-error-empty variants.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-08` and ledger record `ledger/tasks/web-08.md` in the Plan repository; task branch `task/web-08` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / L |
| Obligations | [WP-47.07](../../work-packages/47-static-public-site.md#rule-wp-47.07) — full |
| Provides | web-design-system |
| Start prerequisites | **artifact** [GOV.03](governance.md#task-gov-03) — Node/npm workspace. *Why:* already satisfied; packages/ui already exists as a workspace member |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.09](#task-web-09), [WEB.10](#task-web-10), [WEB.19](#task-web-19) |
| Write scope | `Web:packages/ui/**` |
| Shared resources | [RES-web-shared-ui](../shared-resources.md#res-web-shared-ui) (append) |
| Validation | React Testing Library behavior tests; production-rendered Playwright visual snapshots for representative viewport/theme/locale combinations (local opt-in per playwright.config.ts's CI guard); automated accessibility and dated human visual/keyboard review; dependency/licence/provenance checks |
| Completion evidence | Approved consumer layouts and complete accessible states |
| Baseline (unreviewed unless accepted) | not-started Observed scaffold, unreviewed: packages/ui currently exports only Arrow/Button/Shell (a minimal site header/footer); needs the full token system and component catalogue |
| Notes | Has NO dependency on WEB.01-WEB.07 (different package, only needs WP02 which is already satisfied) and should be started in parallel with the site generator work, not after it — it is the critical-path input for both WEB.10 (account) and WEB.19 (chat). |

<a id="task-web-09"></a>

### WEB.09 — Verify the owned Site artifact and real integration

**Outcome.** The React-generated static Site with localization/SEO and no production Node server is verified end to end; independently published product/version/download metadata is consumed through the fixed release contract, with pending later owners and their closing gates recorded.

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
| Write scope | `Web:apps/site/**` |
| Validation | Static/no-script/accessibility/link and artifact-version checks; private candidate download fixtures labelled; public promotion waits for WP50 |
| Completion evidence | Owned-artifact-and-real-integration receipt including browser-support.v1 evidence for the site output |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Provides the tooling WP45's operations console needs ("47 tooling must precede 45" per producer-artifacts-and-integration.md); the commerce, policy and operations lanes should reference this task's 'web-static-generator'/'web-design-system' tokens as its own start need rather than waiting on all of WP47's numeral position in the old serial plan. |

<a id="task-web-10"></a>

### WEB.10 — Account shell: route graph, deployment-profile selection, generated-SDK wiring

**Outcome.** The apps/app workspace member is created with the account deployment profile: route graph/shell composed from packages/ui + generated TS SDK + TanStack Query, Android callback/assetlinks wiring, responsive overview/navigation, safe public runtime config, error boundaries, and loading/empty/pending/expired states with cache-clear-and-abort on user/workspace change.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-10` and ledger record `ledger/tasks/web-10.md` in the Plan repository; task branch `task/web-10` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | producer / XL |
| Obligations | [WP-48.00](../../work-packages/48-account-portal.md#rule-wp-48.00) — full |
| Provides | web-app-shell |
| Start prerequisites | **artifact** [WEB.08](#task-web-08) — design system tokens/components. *Why:* the shell composes packages/ui directly<br>**contract** [CON.07](contracts.md#task-con-07) — generated TS SDK (@arcforges/api-client/@arcforges/proto). *Why:* already published and consumed at 1.0.0-ci.44.1 in apps/site; needs bumping to the current release to cover the account/chat wire surface |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.12](cloud.md#task-cloud-12) — identity/browser/native endpoints. *Why:* per [WP-48.00](../../work-packages/48-account-portal.md#rule-wp-48.00)'s own text: "minimal auth producer already exists in WP22" |
| Unblocks | [WEB.11](#task-web-11), [WEB.13](#task-web-13), [WEB.14](#task-web-14), [WEB.15](#task-web-15), [WEB.16](#task-web-16), [WEB.19](#task-web-19) |
| Write scope | `Web:apps/app/**`<br>`Web:package.json` |
| Shared resources | [RES-contract-consumer-pins](../shared-resources.md#res-contract-consumer-pins) (append), [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append), [RES-web-build-config](../shared-resources.md#res-web-build-config) (append), [RES-web-shared-ui](../shared-resources.md#res-web-shared-ui) (append) |
| Validation | TypeScript/RTL checks; no-cookie-leakage/state/PKCE/origin-mismatch and Android-verified-links tests; production route/chunk isolation, both themes, keyboard/narrow layouts — fixture-backed CI plus local opt-in real-browser evidence |
| Completion evidence | Profile isolation and composition results |
| Baseline (unreviewed unless accepted) | not-started Observed none, unreviewed: apps/app currently contains only a README stating the design is not yet implemented |

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
| Write scope | `Web:apps/app/app/features/account/**` |
| Validation | Playwright against production assets/edge/real Cloud and D1 is local opt-in (login/logout, two origins/tabs, sibling-origin CSRF, passkey expected origin, replica restart, expiry/revoke races); manual passkey/browser matrix supplements automation |
| Completion evidence | Token storage, refresh, step-up and new-browser trust results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-12"></a>

### WEB.12 — Account and security surfaces

**Outcome.** Profile, authentication methods, passkey management, sessions, device list with trust/revocation, recovery configuration and the security-event view are complete, with step-up required on every sensitive action.

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
| Write scope | `Web:apps/app/app/features/account/**` |
| Validation | Device-revocation-propagation, passkey add/remove, security-event-visibility and step-up-required-per-action tests — fixture CI plus local opt-in real-Cloud evidence |
| Completion evidence | Device revocation, passkey and step-up coverage results |
| Baseline (unreviewed unless accepted) | not-started |

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
| Write scope | `Web:apps/app/app/features/workspace/**` |
| Validation | Accounting comparison against server-side figures; structural test asserting no membership/invitation/role/seat operation; projection test asserting no supplier rate/route-weight leakage; capacity-vs-credits never-summed display test |
| Completion evidence | Storage and usage accounting comparison |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-14"></a>

### WEB.14 — Subscription, capacity, credits and hosted checkout

**Outcome.** Consumer subscription/management views use public server projections and generated operations; paid-term state, replenishing capacity and purchased credits display separately; hosted checkout opens in-browser and shows confirming until verified Cloud state changes; no client/provider redirect grants entitlement.

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
| Write scope | `Web:apps/app/app/features/commerce/**` |
| Validation | Real C# accounting/checkout-test-environment flows; exact-amount display above JS safe-integer boundaries; duplicate-click/cancelled/failed/late-confirmation/refund/term-expiry/stale-price tests — local opt-in against a real test-mode provider |
| Completion evidence | Entitlement reason coverage, credit separation and no-payment-field scan |
| Baseline (unreviewed unless accepted) | not-started |

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
| Write scope | `Web:apps/app/app/features/data/**` |
| Validation | Export-completeness, deletion-statement-accuracy, grace-period and local-data-assertion tests |
| Completion evidence | Export completeness and deletion statement accuracy |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-16"></a>

### WEB.16 — Origin security and performance (account)

**Outcome.** A strict CSP with no default inline script, per-origin cookie/CORS/CSRF posture, no secret in the bundle, sandboxed preview of user content, and bundle-size/first-interactive budgets with regression gates.

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
| Write scope | `Web:deploy/edge/account/**` |
| Shared resources | [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append), [RES-web-build-config](../shared-resources.md#res-web-build-config) (append) |
| Validation | Policy header verification; bundle secret scan; sandbox escape test on hostile content; budget measurements with regression gate — offline/CI-eligible |
| Completion evidence | Policy headers, bundle secret scan and budget measurements |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-17"></a>

### WEB.17 — Offline, degradation and accessibility (account)

**Outcome.** Honest offline behaviour preserving unsent input, a cloud-outage state naming unavailable capabilities with reasons rather than blanking, and full keyboard-only accessibility on every major workflow.

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
| Write scope | `Web:apps/app/**`<br>`Web:tests/**` |
| Validation | Offline-behaviour tests; cloud-outage-no-blank test; accessibility automated and manual passes |
| Completion evidence | Offline, outage and accessibility results |
| Baseline (unreviewed unless accepted) | not-started |

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
| Write scope | `Web:apps/app/**` |
| Validation | Real browser against the AOT release: cookie secrecy, CSRF, expiry/revocation, privacy/export and admission/usage display — local opt-in per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Owned-artifact-and-real-integration receipt; contributes its scoped evidence toward [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) (closed later at WP50, not here) |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-19"></a>

### WEB.19 — Chat shell: route composition and design-system integration

**Outcome.** Chat routes are composed in the same ArcForges.Web.App codebase using owned UI tokens/components and the generated TS SDK; Account/Chat assets, cookies, query scopes and public config are independently selected and validated; responsive conversation navigation/composer/task panel and native-product handoff work with keyboard/reduced-motion support.

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
| Unblocks | [WEB.20](#task-web-20), [WEB.21](#task-web-21), [WEB.22](#task-web-22), [WEB.23](#task-web-23), [WEB.25](#task-web-25), [WEB.30](#task-web-30), [WEB.31](#task-web-31) |
| Write scope | `Web:apps/app/app/features/chat/**` |
| Shared resources | [RES-web-app-routing](../shared-resources.md#res-web-app-routing) (append), [RES-web-build-config](../shared-resources.md#res-web-build-config) (append), [RES-web-shared-ui](../shared-resources.md#res-web-shared-ui) (append) |
| Validation | Production route/profile inspection; approved light/dark/narrow-screen visual baselines; keyboard/touch/long-text states; source/dependency assertion that no provider or Harness implementation enters the browser |
| Completion evidence | Cross-profile isolation results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-20"></a>

### WEB.20 — Conversation and generated output streams

**Outcome.** The full Chat UI uses annex-10 gRPC-Web binary output/event streams with durable recovery; Cloud history is authoritative except memory-only temporary UI; an interrupted stream is always shown as interrupted, never complete.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-20` and ledger record `ledger/tasks/web-20.md` in the Plan repository; task branch `task/web-20` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / L |
| Obligations | [WP-49.01](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.01) — all work except the parts mapped to WEB.27 |
| Provides | web-chat-streaming-ui |
| Start prerequisites | **artifact** [WEB.19](#task-web-19) — chat shell + real deployed WP23/24 transport (inherited via WEB.10). *Why:* streaming UI needs the real deployed event/stream transport, already available once the account shell's WP22/23 chain is up |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [WEB.27](#task-web-27) — real CF Harness admission/generation/tool loop. *Why:* same pattern as AND.09: the streaming/cursor/reconnect UI can be fully built and tested against the server-side contract-bound fixture turn endpoint that already runs in the real deployed Cloud host; real generation quality requires WP52 |
| Unblocks | [WEB.24](#task-web-24), [WEB.26](#task-web-26), [WEB.27](#task-web-27) |
| Permitted substitutes | [SUB-fixture-turn-endpoint](../substitutes.md#sub-fixture-turn-endpoint) |
| Write scope | `Web:apps/app/app/features/chat/**`<br>`Web:tests/chat/**` |
| Validation | Generated event-contract and recovery tests (byte offsets, reconnect/gaps, duplicate delivery, loss of authorization); browser-support.v1 polling-fallback behavior (EventService.Poll every 10s +/-20% jitter, ExecutionService.ReadOutput every 5s after the 45s stream-silence timeout) |
| Completion evidence | Streaming, interruption and partial-message results |
| Baseline (unreviewed unless accepted) | not-started |

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
| Write scope | `Web:apps/app/app/features/tasks/**`<br>`Web:tests/chat/**` |
| Validation | Idempotency-per-control, local-presence-negative, approval-expiry and durable-attention tests |
| Completion evidence | Control idempotency, local-presence and attention-durability results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-22"></a>

### WEB.22 — Artifacts and sandboxing

**Outcome.** Artifact preview runs inside an isolated sandbox so untrusted content never executes in the application origin; downloads verify permission at access; no public share links exist in V1.

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
| Write scope | `Web:apps/app/app/features/artifacts/**` |
| Validation | Sandbox-escape attempt with hostile content; permission-at-access test; existence-disclosure test on a denied resource; public-share-link absence assertion |
| Completion evidence | Sandbox escape, permission-at-access and share-link absence results |
| Baseline (unreviewed unless accepted) | not-started |
| Notes | Self-contained: mostly a client-side iframe/CSP isolation mechanism plus WP25 resource tickets already inherited via the account shell; does not need WP26 or WP52. |

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
| Write scope | `Web:apps/app/app/features/devices/**` |
| Validation | Scope/permission, wrong-or-stale-target, loss/retry and expiry scenarios against the exact real artifact/owner boundary |
| Completion evidence | Offline-target queueing and no-local-connection results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-24"></a>

### WEB.24 — Offline, degradation and accessibility (chat)

**Outcome.** Honest offline messaging preserving unsent input; realtime loss degrades to polling with backfill; a cloud outage reports unavailable capabilities rather than blanking; every core workflow completes by keyboard.

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
| Write scope | `Web:apps/app/**`<br>`Web:tests/chat/**` |
| Validation | Offline/reconnection tests; polling-degradation test; cloud-outage test; accessibility automated and manual passes |
| Completion evidence | Offline, degradation, convergence and accessibility results |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-25"></a>

### WEB.25 — Performance budgets (chat)

**Outcome.** Bundle size, first-interactive and interaction-responsiveness budgets are measured per release candidate with a regression gate that catches a deliberate regression.

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web` |
| Claim, branch and ledger | `claims/web-25` and ledger record `ledger/tasks/web-25.md` in the Plan repository; task branch `task/web-25` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | feature / S |
| Obligations | [WP-49.06](../../work-packages/49-arcchat-web-companion.md#rule-wp-49.06) — full |
| Provides | web-chat-performance |
| Start prerequisites | **artifact** [WEB.19](#task-web-19) — chat shell. *Why:* measures its bundle |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [WEB.26](#task-web-26) |
| Write scope | `Web:apps/app/app/features/chat/**` |
| Shared resources | [RES-web-build-config](../shared-resources.md#res-web-build-config) (append) |
| Validation | Budget measurements per release candidate; regression-gate negative test |
| Completion evidence | Budget measurements and regression-gate negative test |
| Baseline (unreviewed unless accepted) | not-started |

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
| Start prerequisites | **artifact** [WEB.20](#task-web-20) — streaming. *Why:* final join<br>**artifact** [WEB.21](#task-web-21) — tasks/approval. *Why:* final join<br>**artifact** [WEB.22](#task-web-22) — artifacts. *Why:* final join<br>**artifact** [WEB.23](#task-web-23) — remote control. *Why:* final join<br>**artifact** [WEB.24](#task-web-24) — resilience. *Why:* final join<br>**artifact** [WEB.25](#task-web-25) — budgets. *Why:* final join |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [WEB.27](#task-web-27) — real Harness. *Why:* unlike WP47's deferrable numeric join, [WP-49](../../work-packages/49-arcchat-web-companion.md#rule-wp-49)'s own text states "49 consumes 52" as a hard requirement recorded at this task's own gate, not deferred to WP50 |
| Unblocks | [REL.05](release.md#task-rel-05) |
| Write scope | `Web:apps/app/**` |
| Validation | Full real admitted CF turn/tool/approval/reconnect in a browser — local opt-in per [P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017) |
| Completion evidence | Owned-artifact-and-real-integration receipt; contributes its scoped evidence toward [PG-23](../../../assurance/open-gates-register.md#rule-pg-23) (closed later at WP50) |
| Baseline (unreviewed unless accepted) | not-started |

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

<a id="task-web-30"></a>

### WEB.30 — Real React Web client against deployed browser session/PublicApi/realtime

**Outcome.** Real TS gRPC-Web client, cookie/CSRF/Origin session behavior and realtime streams against the deployed Cloud, beyond MSW fixtures

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web`; also touches Cloud |
| Claim, branch and ledger | `claims/web-30` and ledger record `ledger/tasks/web-30.md` in the Plan repository; task branch `task/web-30` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-23.05](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23.05) — Web real-consumer integration |
| Start prerequisites | **artifact** [CLOUD.19](cloud.md#task-cloud-19) — real, delivered outcome of CLOUD.19 (Browser cookie-session adapter and full account-surface closure). *Why:* this integration exercises the real browser cookie-session adapter and full account-surface closure instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.26](cloud.md#task-cloud-26) — real, delivered outcome of CLOUD.26 (Generated C#/TypeScript/Kotlin clients against Identity/Workspace/Device). *Why:* this integration exercises the real generated C#/TypeScript/Kotlin clients against Identity/Workspace/Device instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [CLOUD.29](cloud.md#task-cloud-29) — real, delivered outcome of CLOUD.29 (Stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells)). *Why:* this integration exercises the real stream connection and authentication (EventService.Watch/ExecutionService.WatchOutput shells) instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.07](#task-web-07) — real, delivered outcome of WEB.07 (Independence and atomic deployment). *Why:* this integration exercises the real independence and atomic deployment instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.14](#task-web-14) — real, delivered outcome of WEB.14 (Subscription, capacity, credits and hosted checkout). *Why:* this integration exercises the real subscription, capacity, credits and hosted checkout instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.19](#task-web-19) — real, delivered outcome of WEB.19 (Chat shell: route composition and design-system integration). *Why:* this integration exercises the real chat shell: route composition and design-system integration instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [PRF.08](runtime-proofs.md#task-prf-08) — React production build and generated SDK proof using MSW fixtures. *Why:* the real-client integration replaces the fixture-backed proof path |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | none |
| Unblocks | [CLOUD.28](cloud.md#task-cloud-28), [WEB.31](#task-web-31) |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Real TS gRPC-Web client, cookie/CSRF/Origin session behavior and realtime streams against the deployed Cloud, beyond MSW fixtures |
| Baseline (unreviewed unless accepted) | not-started |

<a id="task-web-31"></a>

### WEB.31 — Full browser-support.v1 matrix across all Web-facing outputs

**Outcome.** Supported/degraded/blocked behavior across every output's flows on real browser/OS patches; [WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) joins all production hashes and real browser evidence

| Field | Value |
|---|---|
| Owning repository | Web (`C:\MyFile\Projects\ArcForges\Web`); integration owner: Web integration owner, the holder of `roles/integration-web`; also touches Cloud |
| Claim, branch and ledger | `claims/web-31` and ledger record `ledger/tasks/web-31.md` in the Plan repository; task branch `task/web-31` ([DLV-26](../README.md#rule-dlv-26)) |
| Kind / size | integration / M |
| Obligations | [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) Browser matrix acceptance appendix, full cross-area join — Browser matrix acceptance appendix, full cross-area join |
| Start prerequisites | **artifact** [OPS.05](operations.md#task-ops-05) — real, delivered outcome of OPS.05 (Operator console and support access). *Why:* this integration exercises the real operator console and support access instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.07](#task-web-07) — real, delivered outcome of WEB.07 (Independence and atomic deployment). *Why:* this integration exercises the real independence and atomic deployment instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.14](#task-web-14) — real, delivered outcome of WEB.14 (Subscription, capacity, credits and hosted checkout). *Why:* this integration exercises the real subscription, capacity, credits and hosted checkout instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.19](#task-web-19) — real, delivered outcome of WEB.19 (Chat shell: route composition and design-system integration). *Why:* this integration exercises the real chat shell: route composition and design-system integration instead of a substitute, so it cannot start before that outcome exists<br>**artifact** [WEB.30](#task-web-30) — the real React Web client against the deployed browser session. *Why:* the consumer builds on these delivered producers; the package acceptance receipt is a roll-up, never a start barrier |
| Entry condition | [ADOPT.09.web](adoption.md#task-adopt-09-web) — the adoption slice for this repository and lane is complete ([DLV-22](../README.md#rule-dlv-22)) |
| Completion prerequisites | **integration** [CLOUD.28](cloud.md#task-cloud-28) — the [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) browser-matrix Cloud part accepted. *Why:* the full browser matrix includes the Cloud part that the [WP-23](../../work-packages/23-public-api-and-generated-clients.md#rule-wp-23) closure accepts |
| Unblocks | none |
| Write scope |  |
| Validation | Local real-integration run of the affected scenario in an existing environment, recorded once; offline and static checks in CI; no hosted runtime, device, browser, live-service or inference CI ([P2-017](../../../decisions/phase-2-specification-decisions.md#rule-p2-017)). |
| Completion evidence | Supported/degraded/blocked behavior across every output's flows on real browser/OS patches; [WP-50](../../work-packages/50-full-platform-production-release.md#rule-wp-50) joins all production hashes and real browser evidence |
| Baseline (unreviewed unless accepted) | not-started |
