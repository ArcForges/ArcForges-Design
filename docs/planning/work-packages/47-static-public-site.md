<a id="rule-wp-47"></a>

# WP-47 — Static Public Site

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: K — Web and release
> Upstream: `00`, `02` · Downstream: `48`

> **Goal.** Ship the public face early and keep it independent: marketing, documentation, downloads and legal pages as static HTML and CSS generated from one source of truth, requiring no runtime, no account and no cloud.

> **Dependency note.** This package consumes [WP-00](00-specification-naming-and-rights-freeze.md#rule-wp-00)'s names/content authority and [WP-02](02-build-governance-and-analyzer-policy.md#rule-wp-02)'s Node workspace/toolchain. Its first static slice can be implemented after those gates in the one serial context; final public commercial content still depends on the release gates. It is not parallel implementation authorization.

---

## 1. Scope and purpose

**In scope.** The static generator; content sourcing from one source of truth for product catalogue, release metadata, pricing and legal document versions; per-locale output; the documentation surface; the download and update surfaces; legal pages; performance and internationalisation obligations; and privacy-preserving analytics.

**Out of scope.** The account portal (`48`) and the web companion (`49`) — both are the React application, not the static site. Any interactive application feature.

**Why this package exists.** `I2 §III.12` permits early delivery of static public content. [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) adds the shared Node/toolchain dependency; public content remains usable before JavaScript runs.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/10-web-architecture.md`](../../architecture/10-web-architecture.md) `§1`, `§2` | Build outputs and static generation rules |
| [`../../requirements/products/arcforges-web.md`](../../requirements/products/arcforges-web.md) | Site scope, internationalisation, performance and analytics requirements |
| **[D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007)**, **[D-014](../../decisions/phase-1-foundation-decisions.md#rule-d-014)** | The rendering boundary and the surface inventory |
| [WP-00](00-specification-naming-and-rights-freeze.md#rule-wp-00) output | Frozen product names and the content source of truth |

---

**Web redesign input.** [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008) and [Web toolchain and SDK](../../architecture/25-web-toolchain-and-sdk.md) are binding for this package's Web, generated-contract, toolchain and test responsibilities. The existing desktop/mobile runtime and product-scope decisions remain separately governed.

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Public pages render as static HTML and CSS before JavaScript runs**, with working ordinary navigation when scripting is disabled ([D-007](../../decisions/phase-1-foundation-decisions.md#rule-d-007), as amended). |
| BR-02 | **Node.js/npm, React/TypeScript, Vite and React Router generate the static site.** Runtime Node SSR, Blazor and a second business backend are outside [P2-008](../../decisions/phase-2-specification-decisions.md#rule-p2-008). |
| BR-03 | **Browser enhancements follow the owned design system and dependency/CSP/performance policy.** Initial content, links and downloads remain usable with JavaScript disabled. |
| BR-04 | **Product catalogue, release metadata and pricing come from one source of truth.** The generator consumes it and never re-states versions or prices. |
| BR-05 | **Above-the-fold content is present in the delivered HTML**; no client script is required to render it. |
| BR-06 | **Locale-scoped URLs with correct alternate-language annotations**; no client-only language switching and no trapping automatic redirect. |
| BR-07 | **No blocked third-party resource on the critical path** — fonts, script hosts, analytics and verification providers all chosen for global reachability. |
| BR-08 | **The generator is deterministic**: identical inputs produce byte-identical output. |
| BR-09 | **The site is entirely independent of Cloud** and remains available during any cloud incident. |
| BR-10 | **Analytics are minimal and privacy-preserving**, with no cross-site advertising profile and no data sale. |
| BR-11 | **Only the four current products appear.** Superseded product names never appear. |

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

**What must be fully done.** Consume catalogue, release metadata, changelog, public offer projection and legal versions from declared versioned inputs. No live provider fetch during a build. Show the pricing projection's effective version/time; final checkout revalidates eligibility/tax/price through Cloud. Content can refer to released signed artifacts only.

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

---

**Visual-system evidence.** [WP-47.07](#rule-wp-47.07)'s component behavior, browser snapshots, licensed assets and dated human visual/accessibility review are required outputs, in addition to the static/content/deployment results above.

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. Two builds of unchanged content are byte-identical; a single content change produces a minimal diff.
2. No version or price is hard-coded anywhere in the site.
3. **The page renders fully with scripting disabled**, meets its performance requirement, and has no globally unreachable critical-path resource.
4. Locale routing is correct and annotated; no redirect traps a user; pseudo-localisation reveals no hard-coded string.
5. Downloads are verifiable against published hashes with no account gate; legal documents carry versions and effective dates.
6. Accessibility checks pass with a dated manual record; analytics carry no cross-site identifier.
7. **A full cloud outage leaves the site fully available**; deployment is atomic; rollback restores the previous artifact set.

---

## 9. Dependencies

**Upstream — all must be complete.**

- [00 — Specification, Naming and Rights Freeze](00-specification-naming-and-rights-freeze.md)
- [02 — Build Governance, Packaging Policy and Analyzers](02-build-governance-and-analyzer-policy.md)

**Downstream — these consume this package’s completed output.**

- [48 — Account Portal](48-account-portal.md)
