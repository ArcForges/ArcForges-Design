# Reference Coverage Matrix — Distribution and Release / StartArcForges

> Status: **Authoritative** — Phase 2 design-stage evidence · **Complete within the authorized oracle boundary**
> Governing authority: **D-012** (StartArcForges is the *packaged-product and release-behaviour oracle*), **D-013**
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

**D-012** registers StartArcForges as the *packaged-product and release-behaviour* oracle. That boundary is narrow and is respected literally:

| In boundary | Out of boundary |
|---|---|
| What a shipped artifact set looks like on disk | The source of any product — that belongs to each product's own matrix |
| Installer presence, naming and version convention | Runtime behaviour of any product |
| Bundled runtime and third-party notice files | Anything requiring execution |
| Crash-handler and updater artifacts as shipped | Reverse engineering of any binary |
| Deployment shape — self-contained versus loose | Licence clearance for reuse — no reuse is possible from a binary tree |

| # | Rule |
|---|---|
| OB-01 | **No packaged binary was executed.** This is an explicit constraint of this repair and is independently required for Serial-Studio, whose binary is a licensed trial. |
| OB-02 | **No binary was disassembled, unpacked or reverse engineered.** Evidence is directory structure, file names, and bundled text notices only. |
| OB-03 | **Nothing here authorizes reuse.** A packaged tree contains compiled third-party code under many licences; it is an observation subject, not a source. |

---

## 2. Licence and provenance position

| Observation | Evidence | Finding |
|---|---|---|
| Bundled runtime notices | `AFFiNE/LICENSES.chromium.html`, `AFFiNE/LICENSE`, `AionUi/LICENSE.electron.txt`, `AionUi/LICENSES.chromium.html`, `siyuan/LICENSE`, `siyuan/LICENSE.electron.txt`, `siyuan/LICENSES.chromium.html` | Every Electron-based product ships **both** its own licence and separate runtime notice files |
| Native product notices | `ArcVideo/` ships third-party DLLs (OpenColorIO, OpenEXR, OpenImageIO, Imath, Iex, IlmThread) **without** an accompanying aggregated notice file in the tree | **Finding recorded** — see `SD-06` |
| Serial-Studio | Commercial trial binary | Not executed; licence position established in that product's matrix |

---

## 3. Reviewed scope

| Area read | Evidence location |
|---|---|
| Per-product packaged tree structure | `StartArcForges/{AFFiNE,AionUi,ArcVideo,ArcVideoFoundation,Serial-Studio,siyuan}` — directory listings |
| Installer artifacts | `*.exe` at each product root |
| Update-framework artifacts | `AFFiNE/Squirrel.exe` |
| Crash-handling artifacts | `ArcVideo/{crashpad_handler.exe,arcvideo-crashhandler.exe}` |
| Bundled notice files | `LICENSE*`, `LICENSES.chromium.html`, `LICENSE.electron.txt` |
| Runtime support files | `*.pak`, `*.dll`, `vk_swiftshader_icd.json`, `plugins/`, `qml/`, `resources/`, `translations/` |
| Library-only output | `ArcVideoFoundation/{include,lib}` |

**Not read, and why:** binary contents of any executable or library — outside the oracle boundary (`OB-02`).

---

## 4. Item-level matrix

| # | Observation | Evidence location | ArcForges requirement or exclusion | Disposition | Rationale | Licence position | Verification oracle | Owner | State |
|---|---|---|---|---|---|---|---|---|---|
| SD-01 | **Electron products ship a versioned installer** — `affine-0.27.2-stable-windows-x64.nsis.exe`, `AionUi-2.1.35-win-x64.exe`, `siyuan-3.7.3-win.exe` | `StartArcForges/{AFFiNE,AionUi,siyuan}` | `10-distribution-update-and-support.md` §1.1 (signed installer from the official site); `14-build-packaging-and-release.md` §5.2 | Reference Only | Confirms the versioned-installer convention, including that the **version string appears in the artifact file name** — which `VR-05` requires ArcForges to keep identical across store, package manager, feed and checksum | Bundled notices; no reuse | Release matrix (`WP-50.02`) | Release Engineering Owner | Evidence established |
| SD-02 | **Installer and application executable coexist in the same tree** — e.g. `AFFiNE.exe` beside `affine-…nsis.exe` | `StartArcForges/{AFFiNE,AionUi,siyuan}` | `14-build-packaging-and-release.md` §5 | Reference Only | Evidence that the packaged output tree and the installer are separate artifacts produced from one publish, matching `PK-01` (the packaging tool consumes the publish output directory) | Bundled notices; no reuse | Release matrix | Release Engineering Owner | Evidence established |
| SD-03 | **A dedicated update framework binary ships with the product** — `Squirrel.exe` | `StartArcForges/AFFiNE/Squirrel.exe` | `10-distribution-update-and-support.md` §3; `P2-001` | Reference Only | **Contrast evidence for `P2-001`.** The reference category solves install-and-update with an Electron-specific framework. ArcForges' baseline is a cross-platform .NET framework behind an abstraction boundary; the requirement it satisfies is the same, the mechanism is not transferable | Bundled notices; no reuse | Update matrix (`WP-50.02`) | Release Engineering Owner | Evidence established |
| SD-04 | **Native products ship as a loose directory with no installer** — Serial-Studio has `bin/ plugins/ qml/ resources/ translations/ run.cmd`; ArcVideo has 47 loose entries including `arcvideo-editor.exe` | `StartArcForges/{Serial-Studio,ArcVideo}` | `10-distribution-update-and-support.md` §1.1 (`DS-02`, `PL-01`) | Reference Only | **The clearest category finding**: Electron products install, native products do not. ArcForges is a native product that requires a signed per-user installer on every desktop platform — a deliberate improvement over the category norm | Bundled notices; no reuse | Release matrix; `WP-50.02` gate 3 | Release Engineering Owner | Evidence established |
| SD-05 | **A launcher script substitutes for an installer** — `Serial-Studio/run.cmd` | `StartArcForges/Serial-Studio/run.cmd` | **Accepted exclusion** — ArcForges ships no launcher script | Drop | A script launcher bypasses signing, file association, update registration and uninstall, all of which ArcForges requires | Not applicable | — | Release Engineering Owner | Accepted exclusion |
| SD-06 | **Native third-party dependencies ship without an aggregated notice file** — ArcVideo bundles OpenColorIO, OpenEXR, OpenImageIO, Imath, Iex, IlmThread DLLs with no `NOTICE`/`THIRD-PARTY` file in the tree | `StartArcForges/ArcVideo` directory listing | `14-build-packaging-and-release.md` `SP-06`, `SP-10`; `WP-50.01` | Reference Only | **Compliance-gap evidence.** The Electron products ship runtime notices; the native product does not. ArcForges' native path carries the same dependency classes, so `WP-50.01`'s NOTICE verification must explicitly cover **native** assets, not only managed packages | Third-party licences apply to those DLLs regardless | `WP-50.01` NOTICE verification includes native assets | Licensing and Provenance Owner | Evidence established |
| SD-07 | **A separate crash-handler process ships with the native media product** — `crashpad_handler.exe` and `arcvideo-crashhandler.exe` | `StartArcForges/ArcVideo` | `12-native-interop-and-media.md` `SB-06`; `10-distribution-update-and-support.md` §7.1; `WP-12.05` | Reference Only | **Confirms `SB-06` is standard practice** for native media applications: crash capture is an out-of-process concern that must be packaged, signed and versioned with the product | Bundled notices; no reuse | `WP-50.02` packaging matrix includes the crash handler as a signed artifact | Release Engineering Owner | Evidence established |
| SD-08 | **A software-rasteriser fallback ships with Electron products** — `vk_swiftshader_icd.json` in all three | `StartArcForges/{AFFiNE,AionUi,siyuan}` | `12-native-interop-and-media.md` `GP-04` (software fallback for every GPU operation) | Reference Only | Independent confirmation that a software fallback is expected to be **shipped**, not merely available in theory | Bundled notices; no reuse | First-party test: forced-software-path equivalence (`WP-37.01`) | Architecture Owner | Evidence established |
| SD-09 | **Localisation ships as a packaged resource directory** — `Serial-Studio/translations/` | `StartArcForges/Serial-Studio` | `12-quality-and-compatibility-contract.md` §11 | Reference Only | Evidence that translation resources are a packaging concern with their own artifacts | Bundled notices; no reuse | Localisation gate (`R-08`) | Product Owner | Evidence established |
| SD-10 | **A library reference ships headers and a static/import library, not a product** — `ArcVideoFoundation/{include,lib}` only | `StartArcForges/ArcVideoFoundation` | Informs `../reference-coverage/arcslate-arcvideo.md` `AL-30` | Reference Only | Confirms from the packaged side that ArcVideoFoundation is a library, not an application — consistent with the source-side finding that it is a thin utility layer | GPL-3.0 library; not executed | — | Architecture Owner | Evidence established |
| SD-11 | **Product identity appears in the executable name, not only in metadata** — `AFFiNE.exe`, `AionUi.exe`, `SiYuan.exe`, `arcvideo-editor.exe` | `StartArcForges/*` | `10-distribution-update-and-support.md` `PL-04` (signing identity versus brand identity) | Reference Only | Evidence that the executable name is a user-visible brand surface; ArcForges must keep it consistent with the frozen product names from `WP-00.00` | Bundled notices; no reuse | Forbidden-term scan over shipped artifact names (`G-04`) | Release Engineering Owner | Evidence established |
| SD-12 | **No update-feed or release-metadata document ships inside any packaged tree** | absence across all six trees | `14-build-packaging-and-release.md` §7 (`AF-02` — the feed is a signed, versioned document served from an owned domain) | Reference Only | Confirms the feed is a **service artifact, not a packaged artifact** — supporting `AF-01`, that clients resolve through an owned domain rather than a bundled URL | Not applicable | `WP-50.02` feed population | Release Engineering Owner | Evidence established |

---

## 5. Completeness check

| Check | Result |
|---|---|
| Every reviewed area in `§3` produces at least one row | **Pass** — 12 rows across all 7 areas |
| Every row carries all nine required fields | **Pass** |
| Every row has exactly one completeness state | **Pass** — 12 rows: 11 evidence established, 1 accepted exclusion, 0 unresolved |
| Every non-`Drop` row maps to an existing ArcForges requirement | **Pass** — no row creates a new requirement |
| Oracle boundary respected | **Pass** — no execution, no unpacking, no source claims |
| Any row proposing reuse carries a provenance obligation | **Not applicable** — no row proposes reuse, and a binary tree is not a reuse source |

**Unresolved determinations: none.**

---

## 6. Findings that affect ArcForges design

| # | Finding | Effect |
|---|---|---|
| F-SD-1 | **Native reference products ship without installers; Electron ones ship with them** (`SD-04`). | ArcForges is native and requires a signed per-user installer on all three desktop platforms. The requirement is a deliberate improvement over the category norm, not table stakes — worth knowing when estimating `WP-50.02`. **No design change.** |
| F-SD-2 | **The native product bundles heavy third-party libraries with no aggregated notice file** (`SD-06`). | **Actionable**: `WP-50.01`'s NOTICE verification must explicitly cover **native** assets, since ArcSlate and ArcScope will bundle the same dependency classes. Recorded as a scope clarification in that package. |
| F-SD-3 | **A separate crash-handler process is standard for native media applications** (`SD-07`). | `WP-50.02`'s packaging matrix must treat the crash handler as its own signed, versioned artifact rather than an implementation detail. Recorded in that package. |
| F-SD-4 | **A software rasteriser is shipped, not merely assumed** (`SD-08`). | Supports `GP-04`. No change needed. |

---

## 7. Maintenance

| # | Rule |
|---|---|
| MT-01 | This tree has no commit. It is bound instead to the **observed artifact versions** — AFFiNE 0.27.2-stable, AionUi 2.1.35, SiYuan 3.7.3 — recorded in `SD-01`. A drift check compares those versions. |
| MT-02 | The oracle boundary is not widened by later packages. Source questions go to each product's own matrix. |
| MT-03 | No packaged binary is executed, at any stage. |
