<a id="rule-wp-47"></a>

# WP-47 — Static Public Site

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: A — Freeze and foundation
> Scheduling: this package is an obligation set; its delivery tasks and their typed prerequisites are listed in section 9, generated from the [delivery graph](../delivery/delivery-graph.json) under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018).

> **Goal.** Ship the public face early and keep it independent: marketing, documentation, downloads and legal pages as static HTML and CSS generated from one source of truth, requiring no runtime, no account and no cloud.

> **Dependency note.** This package consumes [WP-00](00-specification-naming-and-rights-freeze.md#rule-wp-00)'s names/content authority and [WP-02](02-build-governance-and-analyzer-policy.md#rule-wp-02)'s Node workspace/toolchain. Its first static slice can be implemented after those gates in the one serial context; final public commercial content still depends on the release gates. It is not parallel implementation authorization.

> **[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) execution binding.** Repositories: Web. Inputs: only the applicable published producers available at this stage under [staged artifact integration](../README.md#staged-artifact-integration). Producer candidate records precede Cloud consolidation; no future package/manifest is an input. Source paths below resolve inside their assigned owner under [layout](../../architecture/01-solution-and-project-layout.md#root-and-logical-path-convention), never a shared checkout. Output: production React build and real C#/CF endpoints with source SHA, package/descriptor/image/Worker identity and evidence attached to that artifact.
> After WP03, unit mocks consume published Contracts fixtures; earlier stages verify their inventory/policy outputs. Acceptance consumes the actual providers scheduled for that stage. A mock cannot close AOT, native isolation, device, CF/R2 or commercial live-operation gates.

---

## 1. Scope and purpose

**In scope.** The static generator; content sourcing from one source of truth for product catalogue, release metadata, pricing and legal document versions; per-locale output; the documentation surface; the download and update surfaces; legal pages; performance and internationalisation obligations; and privacy-preserving analytics.

**Out of scope.** The account portal (`48`) and the web companion (`49`) — both are the React application, not the static site. Any interactive application feature.

**Why this package exists.** [the current dependency model](../implementation-sequence.md#2-phase-structure) permits early delivery of static public content. [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) adds the shared Node/toolchain dependency; public content remains usable before JavaScript runs.

---

## 2. Required inputs and dependencies

[Producer artifacts and real integration](../producer-artifacts-and-integration.md) is a required input. Use this WP's row to identify exact released artifacts, permitted fixtures and the owner that must replace each fixture; completion requires the stated evidence class.


**Frozen architecture inputs.** [P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009), [package registry](../../architecture/01-solution-and-project-layout.md#12-package-and-native-distribution-registry), [numbered wire profile](../../architecture/contracts/04-protobuf-wire-registry.md), and [CF/state/object contract](../../architecture/contracts/05-cloudflare-integration.md). All selected rules in these formal authorities apply before coding.

| Input | Why it matters |
|---|---|
| [`../../architecture/10-web-architecture.md`](../../architecture/10-web-architecture.md) `§1`, `§2` | Build outputs and static generation rules |
| [`../../requirements/products/arcforges-web.md`](../../requirements/products/arcforges-web.md) | Site scope, internationalisation, performance and analytics requirements |
| **[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)**, **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)** | The rendering boundary and the surface inventory |
| [WP-00](00-specification-naming-and-rights-freeze.md#rule-wp-00) output | Frozen product names and the content source of truth |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) as amended by [P2-012](../../decisions/phase-2-specification-decisions.md#rule-p2-012)/[P2-013](../../decisions/phase-2-specification-decisions.md#rule-p2-013) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| <a id="rule-br-01"></a>BR-01 | **Public pages render as static HTML and CSS before JavaScript runs**, with working ordinary navigation when scripting is disabled ([D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007), as amended). |
| <a id="rule-br-02"></a>BR-02 | **Node.js/npm, React/TypeScript, Vite and React Router generate the static site.** Runtime Node SSR, Blazor and a second business backend are outside [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008). |
| <a id="rule-br-03"></a>BR-03 | **Browser enhancements follow the owned design system and dependency/CSP/performance policy.** Initial content, links and downloads remain usable with JavaScript disabled. |
| <a id="rule-br-04"></a>BR-04 | **Product catalogue, release metadata and pricing come from one source of truth.** The generator consumes it and never re-states versions or prices. |
| <a id="rule-br-05"></a>BR-05 | **Above-the-fold content is present in the delivered HTML**; no client script is required to render it. |
| <a id="rule-br-06"></a>BR-06 | **Locale-scoped URLs with correct alternate-language annotations**; no client-only language switching and no trapping automatic redirect. |
| <a id="rule-br-07"></a>BR-07 | **No blocked third-party resource on the critical path** — fonts, script hosts, analytics and verification providers all chosen for global reachability. |
| <a id="rule-br-08"></a>BR-08 | **The generator is deterministic**: identical inputs produce byte-identical output. |
| <a id="rule-br-09"></a>BR-09 | **The site is entirely independent of Cloud** and remains available during any cloud incident. |
| <a id="rule-br-10"></a>BR-10 | **Analytics are minimal and privacy-preserving**, with no cross-site advertising profile and no data sale. |
| <a id="rule-br-11"></a>BR-11 | **Only the four current products appear.** Superseded product names never appear. |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/Web/ArcForges.Web.Site/` | The build-time generator |
| `src/Web/ArcForges.Web.Site/content/` | Marketing, documentation, legal and changelog content with locale variants |
| `src/Web/ArcForges.Web.Site/content/catalogue.json` | The single source of truth for products, releases and pricing references |
| `src/Web/ArcForges.Web.Site/react-router.config.ts` | Generator build configuration |
| `deploy/edge/` | Edge hosting configuration, cache policy, redirects |
| `src/Web/tests/site/` | Determinism, locale, link, performance and accessibility suites |

**Major types introduced.** `ContentSource`, `PageDefinition`, `LocaleVariant`, `SiteManifest`, `Sitemap`, `RedirectRule`, `AssetFingerprint`.

---

## 5. Required implementation work

<a id="rule-wp-47.00"></a>

### WP-47.00 — React static generation and determinism

**What must be fully done.** Use the shared Node/npm workspace and React Router build-time pre-rendering with runtime SSR disabled. Generate the full public locale/URL inventory, documentation versions, sitemap, metadata and redirects. Public output contains no Account/Chat route bundle or private runtime configuration; builds use pinned local content/pricing/release inputs.

**Testing requirements.** Two full builds with identical toolchain/inputs; no-script navigation/content tests; public route inventory and 404 checks; single-content-change diff; build with network disabled after approved restore.

**Completion gate.** Deterministic static artifacts render their meaningful content/navigation without JavaScript or Cloud, with complete locale/docs routes and no private application content.

<a id="rule-wp-47.01"></a>

### WP-47.01 — Versioned public content and pricing inputs

**What must be fully done.** Consume catalogue, release metadata, changelog, public offer projection and legal versions from declared versioned inputs. No live provider fetch during a build. Show the pricing projection's effective version/time; final checkout revalidates eligibility/tax/price through Cloud. Private candidate builds may use named test-only offer/release fixtures. Public builds use approved WP42/44 projections and released signed artifacts; that final join closes at WP50.

**Testing requirements.** Assert no independently hard-coded product version/private supplier price; compare public projection to the selected approved snapshot; changed/stale offer and unavailable-checkout presentation tests.

**Completion gate.** Public amounts/versions are traceable to approved inputs, no private commercial policy ships, and stale static content cannot authorize a charge.

<a id="rule-wp-47.02"></a>

### WP-47.02 — Rendering and performance

**What must be fully done.** Above-the-fold content present in the delivered HTML; content-hashed immutably cached assets with short-lived HTML; no blocked third-party resource on the critical path; performance measured at the 75th percentile against the product requirement.

**Testing requirements.** A no-script render test; a critical-path resource audit; performance measurement at the required percentile; a global-reachability check on every third-party host.

**Completion gate.** The page renders fully with scripting disabled, meets its performance requirement, and has no globally unreachable critical-path resource.

<a id="rule-wp-47.03"></a>

### WP-47.03 — Internationalisation

**What must be fully done.** Locale-scoped URLs with alternate-language annotations, no client-only switching, and no automatic redirect that traps a user in the wrong locale. Every user-visible string is localisable, including in generated pages.

**Testing requirements.** Locale routing and annotation tests; a no-trap assertion; a pseudo-localisation pass over generated output.

**Completion gate.** Locale routing is correct and annotated, no redirect traps a user, and pseudo-localisation reveals no hard-coded string.

<a id="rule-wp-47.04"></a>

### WP-47.04 — Documentation, downloads and legal

**What must be fully done.** Versioned per-product documentation; a download surface with no account gate serving signed artifacts with published hashes; the update feed surface; legal pages with versioning and effective dates.

**Testing requirements.** Documentation version routing; download integrity verification against published hashes; a no-account-gate assertion; legal version-history tests.

**Completion gate.** Downloads are verifiable against published hashes with no account gate, and legal documents carry versions and effective dates.

<a id="rule-wp-47.05"></a>

### WP-47.05 — Accessibility and analytics

**What must be fully done.** Accessibility semantics on every page with keyboard-only navigation. Analytics minimal and privacy-preserving, with no consent wall required because no consent-bearing tracking is used on the basic site.

**Testing requirements.** Automated accessibility checks plus a dated manual verification; an analytics payload audit asserting no cross-site identifier.

**Completion gate.** Accessibility checks pass with a dated manual record, and analytics carry no cross-site identifier.

<a id="rule-wp-47.06"></a>

### WP-47.06 — Independence and deployment

**What must be fully done.** The site is entirely independent of Cloud, deployed atomically per surface from a promoted artifact, with rollback restoring the previous artifact set.

**Testing requirements.** A cloud-outage test asserting the site is unaffected; an atomic deployment test; a rollback test.

**Completion gate.** **A full cloud outage leaves the site fully available**, deployment is atomic, and rollback restores the previous set.

---

<a id="rule-wp-47.07"></a>

### WP-47.07 — Owned consumer design system

**What must be fully done.** Create packages/ui with design tokens, responsive typography/spacing/color/themes, owned accessible primitives and optional Motion interactions. Establish a test-only component catalogue and approved visual baselines for home/product/pricing plus reusable account/usage/chat primitives. Implement localization, long labels, mobile-width navigation, focus/keyboard/reduced-motion and loading/error/empty variants. No extra public application or desktop Web UI is introduced.

**Testing requirements.** React Testing Library behavior tests, production-rendered Playwright visual snapshots for representative viewport/theme/locale combinations, automated accessibility and dated human visual/keyboard review; dependency/licence/provenance checks for incorporated components/assets.

**Completion gate.** The shared design system has approved consumer layouts and complete accessible states; [WP-48](48-account-portal.md#rule-wp-48), [WP-49](49-arcchat-web-companion.md#rule-wp-49) reuse it. Starter-template appearance alone is not acceptance.

---

<a id="rule-wp-47.90"></a>
### WP-47.90 — Verify the owned artifact and real integration

**What must be fully done.** Keep React-generated static Site, localization/SEO and no production Node server. Consume independently published product/version/download metadata through the fixed release contract.

**Execution order.** Follow [staged artifact integration](../README.md#staged-artifact-integration): consume only existing assigned producers, publish an owned capability candidate before its product consumer, and verify the declared stage against exact upstream artifacts. Record pending later owners and their closing gates; local mocks cover only that named test boundary.

**Testing requirements.** Static/no-script/accessibility/link and artifact-version checks; private candidate download fixtures are labelled; public promotion waits for signed published artifacts at WP50.

**Completion gate.** Static/no-script/accessibility/link and artifact-version checks; private candidate download fixtures are labelled; public promotion waits for signed published artifacts at WP50. Record exact artifacts and provider reality. The package is incomplete if an important contract/owner/recovery rule still requires design during coding.

---

**Browser matrix acceptance.** Use [browser-support.v1](../../requirements/12-quality-and-compatibility-contract.md#202-browser-supportv1) and the exact release artifact/OS/browser patches. For each output’s existing flows, verify supported/degraded/blocked browser behavior: delayed-stream polling where streaming exists, refusal of unavailable required authentication/step-up, safe-preview refusal and preserved pending work. Static site acceptance includes no-JavaScript readability; it does not invent interactive account/stream APIs. Operator step-up retains its separate Entra/MFA authority. WP23 proves generated transports; WP45/47/48/49 prove their respective operations/site/account/chat output; WP50 joins all four production hashes and real browser evidence. A Playwright WebKit run alone does not claim Safari/OS authenticator proof.

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | None |
| Protocol | Consumes release metadata; produces none |
| UI | The public web presence |
| Security | Strict content security policy; no secret in output; signed download verification |
| Platform | Edge hosting and cache policy |
| Migration | Content and locale structure versioning |
| Compatibility | The download and update surfaces installed clients depend on |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Determinism comparison and diff-minimality results | [WP-47.00](#rule-wp-47.00) |
| Hard-coded version and price scan | [WP-47.01](#rule-wp-47.01) |
| No-script render, critical-path audit and performance measurements | [WP-47.02](#rule-wp-47.02) |
| Locale routing, no-trap and pseudo-localisation results | [WP-47.03](#rule-wp-47.03) |
| Download integrity, no-gate and legal versioning results | [WP-47.04](#rule-wp-47.04) |
| Accessibility automated plus manual record; analytics audit | [WP-47.05](#rule-wp-47.05) |
| Cloud-outage independence, atomic deployment and rollback results | [WP-47.06](#rule-wp-47.06) |
| Owned artifact and real-integration receipt: source commit, producer version, candidate hashes, actual runtime/OS/device/provider, scenario, result, limitations and real-versus-fixture status; inapplicable fields explicitly marked | [WP-47.90](#rule-wp-47.90) |

---

**Visual-system evidence.** [WP-47.07](#rule-wp-47.07)'s component behavior, browser snapshots, licensed assets and dated human visual/accessibility review are required outputs, in addition to the static/content/deployment results above.

---

## 8. Completion gate

**[P2-009](../../decisions/phase-2-specification-decisions.md#rule-p2-009) gate:** [WP-47.90](#rule-wp-47.90) and all inherited domain-specific gates must pass on the same candidate closure. Static/no-script/accessibility/link and artifact-version checks; private candidate download fixtures are labelled; public promotion waits for signed published artifacts at WP50.

**[PG-23](../../assurance/open-gates-register.md#rule-pg-23) evidence:** [WP-47](#rule-wp-47) — Static production output, applicable accessibility/visual/performance and atomic release/rollback evidence. A scoped contribution does not close the shared gate until every required producer has recorded passing evidence at its trigger.

**All of the following, with recorded evidence:**

1. Two builds of unchanged content are byte-identical; a single content change produces a minimal diff.
2. No version or price is hard-coded anywhere in the site.
3. **The page renders fully with scripting disabled**, meets its performance requirement, and has no globally unreachable critical-path resource.
4. Locale routing is correct and annotated; no redirect traps a user; pseudo-localisation reveals no hard-coded string.
5. Candidate fixtures prove download hash/no-account behavior and legal version rendering. WP50 replaces them with actual signed release downloads and approved effective legal/price snapshots before public promotion.
6. Accessibility checks pass with a dated manual record; analytics carry no cross-site identifier.
7. **A full cloud outage leaves the site fully available**; deployment is atomic; rollback restores the previous artifact set.

---

## 9. Dependencies

<!-- delivery-graph:begin (generated by Plan tools/delivery.py; do not edit) -->

Scheduling is task-level under [P2-018](../../decisions/phase-2-specification-decisions.md#rule-p2-018). This package is an obligation set; it is satisfied when every task below is complete with its evidence. Prerequisites are typed task edges, never "all upstream packages complete".

| Delivery task | Satisfies | Start prerequisites outside this package |
|---|---|---|
| [WEB.01](../delivery/lanes/web.md#task-web-01) | [WP-47.00](47-static-public-site.md#rule-wp-47.00) (full) | [GOV.03](../delivery/lanes/governance.md#task-gov-03) (artifact) |
| [WEB.02](../delivery/lanes/web.md#task-web-02) | [WP-47.01](47-static-public-site.md#rule-wp-47.01) (full) | none |
| [WEB.03](../delivery/lanes/web.md#task-web-03) | [WP-47.02](47-static-public-site.md#rule-wp-47.02) (full) | none |
| [WEB.04](../delivery/lanes/web.md#task-web-04) | [WP-47.03](47-static-public-site.md#rule-wp-47.03) (full) | none |
| [WEB.05](../delivery/lanes/web.md#task-web-05) | [WP-47.04](47-static-public-site.md#rule-wp-47.04) (full) | none |
| [WEB.06](../delivery/lanes/web.md#task-web-06) | [WP-47.05](47-static-public-site.md#rule-wp-47.05) (full) | none |
| [WEB.07](../delivery/lanes/web.md#task-web-07) | [WP-47.06](47-static-public-site.md#rule-wp-47.06) (full) | none |
| [WEB.08](../delivery/lanes/web.md#task-web-08) | [WP-47.07](47-static-public-site.md#rule-wp-47.07) (full) | [GOV.03](../delivery/lanes/governance.md#task-gov-03) (artifact) |
| [WEB.09](../delivery/lanes/web.md#task-web-09) | [WP-47.90](47-static-public-site.md#rule-wp-47.90) (full)<br>[WP-47](47-static-public-site.md#rule-wp-47) Browser matrix acceptance paragraph (browser-support.v1 for the static site output) (package-level obligation contribution) | none |

**Consumers outside this package:** [REL.05](../delivery/lanes/release.md#task-rel-05), [WEB.10](../delivery/lanes/web.md#task-web-10), [WEB.19](../delivery/lanes/web.md#task-web-19), [WEB.30](../delivery/lanes/web.md#task-web-30), [WEB.31](../delivery/lanes/web.md#task-web-31).

<!-- delivery-graph:end -->

