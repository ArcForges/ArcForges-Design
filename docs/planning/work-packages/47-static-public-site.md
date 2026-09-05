# WP-47 — Static Public Site

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: K — Web and release
> Upstream: `00` · Downstream: `48`

> **Goal.** Ship the public face early and keep it independent: marketing, documentation, downloads and legal pages as static HTML and CSS generated from one source of truth, requiring no runtime, no account and no cloud.

> **Parallelism note.** This package depends only on `00` and may run in parallel with the entire foundation and platform sequence (`§4` of the implementation sequence). It is numbered here because its *content* completes late, but its first version can exist very early.

---

## 1. Scope and purpose

**In scope.** The static generator; content sourcing from one source of truth for product catalogue, release metadata, pricing and legal document versions; per-locale output; the documentation surface; the download and update surfaces; legal pages; performance and internationalisation obligations; and privacy-preserving analytics.

**Out of scope.** The account portal (`48`) and the web companion (`49`) — both are the Blazor application, not the static site. Any interactive application feature.

**Why this package exists.** `I2 §III.12` states the static site can be built very early because it depends on nothing but content. **D-007** requires it to render without waiting for the runtime or WebAssembly.

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../architecture/10-web-architecture.md`](../../architecture/10-web-architecture.md) `§1`, `§2` | Build outputs and static generation rules |
| [`../../requirements/products/arcforges-web.md`](../../requirements/products/arcforges-web.md) | Site scope, internationalisation, performance and analytics requirements |
| **D-007**, **D-014** | The rendering boundary and the surface inventory |
| `WP-00` output | Frozen product names and the content source of truth |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **Public pages render as static HTML and CSS without waiting for the runtime or WebAssembly** (**D-007**). |
| BR-02 | **Prohibited**: server circuits, runtime server-side rendering, React, TypeScript, Node, any JavaScript package manager (**D-007**). |
| BR-03 | **Minimal audited JavaScript interop only**, each instance reviewed and listed. |
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
| `src/Web/ArcForges.Web.StaticGen/` | The build-time generator |
| `content/` | Marketing, documentation, legal and changelog content with locale variants |
| `content/catalogue.json` | The single source of truth for products, releases and pricing references |
| `eng/build/web-static.props` | Generator build configuration |
| `deploy/edge/` | Edge hosting configuration, cache policy, redirects |
| `tests/Web/StaticGenTests/` | Determinism, locale, link, performance and accessibility suites |

**Major types introduced.** `ContentSource`, `PageDefinition`, `LocaleVariant`, `SiteManifest`, `Sitemap`, `RedirectRule`, `AssetFingerprint`.

---

## 5. Required implementation work

### WP-47.00 — Generator and determinism

**What must be fully done.** A C# build-time generator producing per-locale, per-page static output plus sitemap, metadata and redirects. Two runs over unchanged input produce byte-identical output so a diff is meaningful.

**Testing requirements.** A determinism test comparing two full builds; a diff-meaningfulness check on a single content change.

**Completion gate.** Two builds of unchanged content are byte-identical, and a single content change produces a minimal diff.

### WP-47.01 — Content sourcing

**What must be fully done.** Product catalogue, release metadata, changelog, pricing references and legal document versions consumed from one source of truth. The generator never restates a version or a price independently.

**Testing requirements.** A source-of-truth assertion asserting no hard-coded version or price exists in content or templates; a release-metadata integration test.

**Completion gate.** No version or price is hard-coded anywhere in the site.

### WP-47.02 — Rendering and performance

**What must be fully done.** Above-the-fold content present in the delivered HTML; content-hashed immutably cached assets with short-lived HTML; no blocked third-party resource on the critical path; performance measured at the 75th percentile against the product requirement.

**Testing requirements.** A no-script render test; a critical-path resource audit; performance measurement at the required percentile; a global-reachability check on every third-party host.

**Completion gate.** The page renders fully with scripting disabled, meets its performance requirement, and has no globally unreachable critical-path resource.

### WP-47.03 — Internationalisation

**What must be fully done.** Locale-scoped URLs with alternate-language annotations, no client-only switching, and no automatic redirect that traps a user in the wrong locale. Every user-visible string is localisable, including in generated pages.

**Testing requirements.** Locale routing and annotation tests; a no-trap assertion; a pseudo-localisation pass over generated output.

**Completion gate.** Locale routing is correct and annotated, no redirect traps a user, and pseudo-localisation reveals no hard-coded string.

### WP-47.04 — Documentation, downloads and legal

**What must be fully done.** Versioned per-product documentation; a download surface with no account gate serving signed artifacts with published hashes; the update feed surface; legal pages with versioning and effective dates.

**Testing requirements.** Documentation version routing; download integrity verification against published hashes; a no-account-gate assertion; legal version-history tests.

**Completion gate.** Downloads are verifiable against published hashes with no account gate, and legal documents carry versions and effective dates.

### WP-47.05 — Accessibility and analytics

**What must be fully done.** Accessibility semantics on every page with keyboard-only navigation. Analytics minimal and privacy-preserving, with no consent wall required because no consent-bearing tracking is used on the basic site.

**Testing requirements.** Automated accessibility checks plus a dated manual verification; an analytics payload audit asserting no cross-site identifier.

**Completion gate.** Accessibility checks pass with a dated manual record, and analytics carry no cross-site identifier.

### WP-47.06 — Independence and deployment

**What must be fully done.** The site is entirely independent of Cloud, deployed atomically per surface from a promoted artifact, with rollback restoring the previous artifact set.

**Testing requirements.** A cloud-outage test asserting the site is unaffected; an atomic deployment test; a rollback test.

**Completion gate.** **A full cloud outage leaves the site fully available**, deployment is atomic, and rollback restores the previous set.

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
| Determinism comparison and diff-minimality results | `WP-47.00` |
| Hard-coded version and price scan | `WP-47.01` |
| No-script render, critical-path audit and performance measurements | `WP-47.02` |
| Locale routing, no-trap and pseudo-localisation results | `WP-47.03` |
| Download integrity, no-gate and legal versioning results | `WP-47.04` |
| Accessibility automated plus manual record; analytics audit | `WP-47.05` |
| Cloud-outage independence, atomic deployment and rollback results | `WP-47.06` |

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

**Upstream.** `00` (frozen names and the content source of truth).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `48` — Account portal | The surface boundary, redirects and shared visual language |
| `50` — Production release | The public entry points, downloads and documentation |
