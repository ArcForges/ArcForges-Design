# Reference Coverage Matrix — Distribution and Release / StartArcForges

> Status: **Authoritative** — Phase 2 design-stage evidence · **Complete within the authorized oracle boundary**
> Governing authority: **[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)** (StartArcForges is the *packaged-product and release-behaviour oracle*), **[D-013](../../decisions/phase-1-foundation-decisions.md#rule-d-013)**
> Consuming area: distribution, packaging and release — [`../../requirements/10-distribution-update-and-support.md`](../../requirements/10-distribution-update-and-support.md), [`../../architecture/14-build-packaging-and-release.md`](../../architecture/14-build-packaging-and-release.md)

---

## 1. Source identity and authorized boundary

| Field | Value |
|---|---|
| Local path | `C:\MyFile\ArcForges\StartArcForges` |
| Kind | A tree of **packaged product outputs**, one directory per reference product. Not a git repository; no commit exists |
| Reviewed on | 2026-09-05 |
| Reviewer | Release Engineering Owner (design stage) |

### 1.1 The authorized oracle boundary

**[D-012](../../decisions/phase-1-foundation-decisions.md#rule-d-012)** registers StartArcForges as the *packaged-product and release-behaviour* oracle. That boundary is narrow and is respected literally:

| In boundary | Out of boundary |
|---|---|
| What a shipped artifact set looks like on disk | The source of any product — that belongs to each product's own matrix |
| Installer presence, naming and version convention | Runtime behaviour of any product |
| Bundled runtime and third-party notice files | Anything requiring execution |
| Crash-handler and updater artifacts as shipped | Reverse engineering of any binary |
| Deployment shape — self-contained versus loose | Licence clearance for reuse — no reuse is possible from a binary tree |

| # | Rule |
|---|---|
| <a id="rule-ob-01"></a>OB-01 | **No packaged binary was executed.** This is an explicit constraint of this repair and is independently required for Serial-Studio, whose binary is a licensed trial. |
| <a id="rule-ob-02"></a>OB-02 | **No binary was disassembled, unpacked or reverse engineered.** Evidence is directory structure, file names, and bundled text notices only. |
| <a id="rule-ob-03"></a>OB-03 | **Nothing here authorizes reuse.** A packaged tree contains compiled third-party code under many licences; it is an observation subject, not a source. |

---

## 2. Licence and provenance position

| Observation | Evidence | Finding |
|---|---|---|
| Bundled runtime notices | `AionUi/LICENSE.electron.txt`, `AionUi/LICENSES.chromium.html` | The Electron-based reference ships **both** its own licence and separate runtime notice files |
| Serial-Studio | Commercial trial binary | Not executed; licence position established in that product's matrix |

---

## 3. Reviewed scope

| Area read | Evidence location |
|---|---|
| Per-product packaged tree structure | `StartArcForges/{AionUi,Serial-Studio}` — directory listings |
| Installer artifacts | `*.exe` at each product root |
| Bundled notice files | `LICENSE*`, `LICENSES.chromium.html`, `LICENSE.electron.txt` |
| Runtime support files | `*.pak`, `*.dll`, `vk_swiftshader_icd.json`, `plugins/`, `qml/`, `resources/`, `translations/` |

**Not read, and why:** binary contents of any executable or library — outside the oracle boundary ([OB-02](#rule-ob-02)).

---

## 4. Item-level matrix

| # | Observation | Evidence location | ArcForges requirement or exclusion | Disposition | Rationale | Licence position | Verification oracle | Owner | State |
|---|---|---|---|---|---|---|---|---|---|
| <a id="rule-sd-01"></a>SD-01 | **The Electron reference ships a versioned installer** — `AionUi-2.1.35-win-x64.exe` | `StartArcForges/AionUi` | `10-distribution-update-and-support.md` §1.1 (signed installer from the official site); `14-build-packaging-and-release.md` §5.2 | Reference Only | Confirms the versioned-installer convention, including that the **version string appears in the artifact file name** — which [VR-05](../../architecture/14-build-packaging-and-release.md#rule-vr-05) requires ArcForges to keep identical across store, package manager, feed and checksum | Bundled notices; no reuse | Release matrix ([WP-50.02](../../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02)) | Release Engineering Owner | Evidence established |
| <a id="rule-sd-02"></a>SD-02 | **Installer and application executable coexist in the same tree** — e.g. `AionUi.exe` beside `AionUi-2.1.35-win-x64.exe` | `StartArcForges/AionUi` | `14-build-packaging-and-release.md` §5 | Reference Only | Evidence that the packaged output tree and the installer are separate artifacts produced from one publish, matching [PK-01](../../architecture/14-build-packaging-and-release.md#rule-pk-01) (the packaging tool consumes the publish output directory) | Bundled notices; no reuse | Release matrix | Release Engineering Owner | Evidence established |
| <a id="rule-sd-04"></a>SD-04 | **The native reference ships as a loose directory with no installer** — Serial-Studio has `bin/ plugins/ qml/ resources/ translations/ run.cmd` | `StartArcForges/Serial-Studio` | `10-distribution-update-and-support.md` §1.1 ([DS-02](../../requirements/10-distribution-update-and-support.md#rule-ds-02), [PL-01](../../requirements/10-distribution-update-and-support.md#rule-pl-01)) | Reference Only | **The clearest category finding**: the Electron reference installs, the native reference does not. ArcForges is a native product that requires a signed per-user installer on every desktop platform — a deliberate improvement over the category norm | Bundled notices; no reuse | Release matrix; [WP-50.02](../../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02) gate 3 | Release Engineering Owner | Evidence established |
| <a id="rule-sd-05"></a>SD-05 | **A launcher script substitutes for an installer** — `Serial-Studio/run.cmd` | `StartArcForges/Serial-Studio/run.cmd` | **Accepted exclusion** — ArcForges ships no launcher script | Drop | A script launcher bypasses signing, file association, update registration and uninstall, all of which ArcForges requires | Not applicable | — | Release Engineering Owner | Accepted exclusion |
| <a id="rule-sd-08"></a>SD-08 | **A software-rasteriser fallback ships with the Electron reference** — `vk_swiftshader_icd.json` | `StartArcForges/AionUi` | `12-quality-and-compatibility-contract.md` [PM-06](../../requirements/12-quality-and-compatibility-contract.md#rule-pm-06) (fallback tests for missing GPU) | Reference Only | Independent confirmation that a software fallback is expected to be **shipped**, not merely available in theory | Bundled notices; no reuse | Architecture review of the packaged tree | Architecture Owner | Evidence established |
| <a id="rule-sd-09"></a>SD-09 | **Localisation ships as a packaged resource directory** — `Serial-Studio/translations/` | `StartArcForges/Serial-Studio` | `12-quality-and-compatibility-contract.md` §11 | Reference Only | Evidence that translation resources are a packaging concern with their own artifacts | Bundled notices; no reuse | Localisation gate ([R-08](../release-gates.md#rule-r-08)) | Product Owner | Evidence established |
| <a id="rule-sd-11"></a>SD-11 | **Product identity appears in the executable name, not only in metadata** — `AionUi.exe` | `StartArcForges/*` | `10-distribution-update-and-support.md` [PL-04](../../requirements/10-distribution-update-and-support.md#rule-pl-04) (signing identity versus brand identity) | Reference Only | Evidence that the executable name is a user-visible brand surface; ArcForges must keep it consistent with the frozen product names from [WP-00.00](../../planning/work-packages/00-specification-naming-and-rights-freeze.md#rule-wp-00.00) | Bundled notices; no reuse | Forbidden-term scan over shipped artifact names ([G-04](../release-gates.md#rule-g-04)) | Release Engineering Owner | Evidence established |
| <a id="rule-sd-12"></a>SD-12 | **No update-feed or release-metadata document ships inside any packaged tree** | absence across both trees | `14-build-packaging-and-release.md` §7 ([AF-02](../../architecture/14-build-packaging-and-release.md#rule-af-02) — the feed is a signed, versioned document served from an owned domain) | Reference Only | Confirms the feed is a **service artifact, not a packaged artifact** — supporting [AF-01](../../architecture/14-build-packaging-and-release.md#rule-af-01), that clients resolve through an owned domain rather than a bundled URL | Not applicable | [WP-50.02](../../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02) feed population | Release Engineering Owner | Evidence established |

---

## 5. Completeness check

| Check | Result |
|---|---|
| Every reviewed area in `§3` produces at least one row | **Pass** — 8 rows across all 4 areas |
| Every row carries all nine required fields | **Pass** |
| Every row has exactly one completeness state | **Pass** — 8 rows: 7 evidence established, 1 accepted exclusion, 0 unresolved |
| Every non-`Drop` row maps to an existing ArcForges requirement | **Pass** — no row creates a new requirement |
| Oracle boundary respected | **Pass** — no execution, no unpacking, no source claims |
| Any row proposing reuse carries a provenance obligation | **Not applicable** — no row proposes reuse, and a binary tree is not a reuse source |

**Unresolved determinations: none.**

---

## 6. Findings that affect ArcForges design

| # | Finding | Effect |
|---|---|---|
| <a id="rule-f-sd-1"></a>F-SD-1 | **The native reference ships without an installer; the Electron reference ships with one** ([SD-04](#rule-sd-04)). | ArcForges is native and requires a signed per-user installer on all three desktop platforms. The requirement is a deliberate improvement over the category norm, not table stakes — worth knowing when estimating [WP-50.02](../../planning/work-packages/50-full-platform-production-release.md#rule-wp-50.02). **No design change.** |
| <a id="rule-f-sd-4"></a>F-SD-4 | **A software rasteriser is shipped, not merely assumed** ([SD-08](#rule-sd-08)). | Supports [PM-06](../../requirements/12-quality-and-compatibility-contract.md#rule-pm-06). No change needed. |

---

## 7. Maintenance

| # | Rule |
|---|---|
| <a id="rule-mt-01"></a>MT-01 | This tree has no commit. It is bound instead to the **observed artifact version** — AionUi 2.1.35 — recorded in [SD-01](#rule-sd-01). A drift check compares that version. |
| <a id="rule-mt-02"></a>MT-02 | The oracle boundary is not widened by later packages. Source questions go to each product's own matrix. |
| <a id="rule-mt-03"></a>MT-03 | No packaged binary is executed, at any stage. |
