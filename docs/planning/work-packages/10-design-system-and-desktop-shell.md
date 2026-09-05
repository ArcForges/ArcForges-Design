# WP-10 — Design System and Desktop Shell Foundation

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Planning · Work package
> Phase: B — Shared platform
> Upstream: `06` · Downstream: `14`, `18`, `33`, `36`

> **Goal.** Build the shared desktop foundation once — tokens, windows, panels, commands, settings, attention, errors, lifecycle — so that four products feel like one family without any of them depending on another, and so that every control in it survives Native AOT.

---

## 1. Scope and purpose

**In scope.** The semantic token system, typography, density and motion; the window, panel and layout model; the command system and shortcut resolution; scoped settings; the attention and notification model; the error presentation model; application lifecycle and shutdown prompts; menus; and the shared-foundation boundary enforcement.

**Out of scope.** Any product's own screens. Account surfaces beyond the shared placeholder (`22`, `48`). Deep-link routing behaviour, which is `09`'s model rendered here.

**Why this package exists.** `SI-01`–`SI-28` describe a shared experience contract. Building it per product would produce four divergent shells and four sets of accessibility defects. It is placed after the AOT proof because every third-party control admitted here must pass the AOT gate (**V-05a**).

---

## 2. Required inputs and dependencies

| Input | Why it matters |
|---|---|
| [`../../requirements/09-shared-desktop-experience.md`](../../requirements/09-shared-desktop-experience.md) | The full shared experience contract and invariants `SI-01`–`SI-28` |
| [`../../architecture/04-desktop-application-architecture.md`](../../architecture/04-desktop-application-architecture.md) | Host structure, MVVM, threading, windows, shell composition, start-up and shutdown |
| [`../../requirements/12-quality-and-compatibility-contract.md`](../../requirements/12-quality-and-compatibility-contract.md) `§4`, `§5`, `§10`, `§11` | Responsiveness, startup, accessibility and localisation contracts |
| **V-05a** | The third-party control AOT gate |
| `WP-06` output | The AOT proof and the control admission process |

---

## 3. Binding rules and decisions

| # | Rule |
|---|---|
| BR-01 | **The shared foundation contains mechanism, never product knowledge** (`§7` of the architecture overview). |
| BR-02 | **No product depends on another product** to render its own UI. |
| BR-03 | **Base ViewModel patterns are not shared with mobile** (**D-021**). |
| BR-04 | **Every third-party control requires its own AOT publish proof with zero diagnostics before adoption** (**V-05a**). |
| BR-05 | **Colour is never the only carrier of meaning**, and contrast, focus order and assistive-technology semantics are contract, not polish (`§10` of the quality contract). |
| BR-06 | **Every core workflow is completable by keyboard alone** (`AL-02` in the web architecture; the desktop equivalent in `§10` there). |
| BR-07 | **Every user-visible string is localisable**, and no string is composed by concatenation that breaks under translation. |
| BR-08 | **Notifications are classified by durability, not severity alone.** A missed transient notification never loses durable attention state. |
| BR-09 | **Settings are scoped** — application, workspace, device, instance — and resolution order is fixed and explainable. |
| BR-10 | **Startup never blocks on the network or on sign-in** (`§27` of the quality contract). |
| BR-11 | **UI work happens on the UI thread; everything else does not** (`§3` of the desktop architecture). |

---

## 4. Projects, directories, files and major types affected

| Location | Change |
|---|---|
| `src/DesignSystem/ArcForges.DesignSystem/` | Created: semantic tokens, typography scale, density, motion, iconography, theming |
| `src/DesignSystem/ArcForges.Desktop.Shell/` | Created: windows, panels, layout, commands, settings, attention, errors, menus, lifecycle |
| `src/BuildingBlocks/ArcForges.Desktop.*` | Reconciled per `WP-01.02`: mechanism-only survivors fold into the shell or the design system |
| `tests/DesktopExperienceTests/`, `tests/DesktopExperienceGallery/` | Extended: token coverage, command availability, shortcut conflicts, attention lifecycle |
| `tests/DesktopUiTests/` | Extended: keyboard-only workflow completion and assistive-technology semantics |

**Major types introduced.** `SemanticToken`, `ThemeDefinition`, `DensityMode`, `ShellWindow`, `PanelHost`, `LayoutState`, `CommandDefinition`, `CommandRegistry`, `ShortcutBinding`, `SettingScope`, `SettingResolver`, `AttentionItem`, `AttentionDurability`, `ErrorPresentation`, `LifecyclePrompt`, `MenuContribution`.

---

## 5. Required implementation work

### WP-10.00 — Token system and theming

**What must be fully done.** Semantic tokens for colour, typography, spacing, radius, elevation and motion, with light and dark themes and a high-contrast mode. No component references a raw value. Density modes are supported as a first-class capability rather than a scale factor.

**Testing requirements.** A policy test asserting no raw colour or size literal in component code; contrast tests across every theme; a density snapshot suite.

**Completion gate.** No raw literal survives, contrast passes in all themes, and density modes render correctly.

### WP-10.01 — Windows, panels and layout

**What must be fully done.** The window model with multiple windows per instance, the panel host with dockable, collapsible regions, and layout persistence that is device-local rather than synced work content. Layout restoration is resilient to a missing panel or a changed screen configuration.

**Testing requirements.** Restore tests across missing panel, changed display arrangement and corrupted layout state; a test asserting layout is device-local.

**Completion gate.** Layout restores safely in every degraded case and is never treated as synced work content.

### WP-10.02 — Command system

**What must be fully done.** A command registry with availability, shortcut binding, a command palette, and conflict detection. Availability is computed from the same evaluation the capability model uses (`WP-09.03`), so a command and a capability never disagree.

**Testing requirements.** Shortcut conflict detection; availability agreement tests against the capability model; palette search relevance tests.

**Completion gate.** No undetected shortcut conflict exists, and command availability agrees with capability availability.

### WP-10.03 — Scoped settings

**What must be fully done.** Settings with fixed scope resolution, typed schemas, migration on schema change, and an explainable effective value — the user can see which scope supplied a value. A device-scoped setting never syncs.

**Testing requirements.** Resolution order tests across every scope combination; explainability tests; a migration test.

**Completion gate.** Resolution order is correct and every effective value is explainable.

### WP-10.04 — Attention and notification model

**What must be fully done.** Attention items classified by durability. A durable item — a pending approval, a failed task — persists until resolved regardless of whether a transient notification was seen. Transient notifications are best-effort. Lock-screen and system-notification content is non-sensitive by default.

**Testing requirements.** A missed-notification test asserting durable state survives; a sensitivity test on notification content.

**Completion gate.** Missing every transient notification never loses a durable attention item.

### WP-10.05 — Error presentation

**What must be fully done.** Errors presented from the reason-code registry with a human-readable statement, what happened, whether it can be retried, and what the user can do. A raw exception message never reaches the user. A support reference identifier is available for every error.

**Testing requirements.** A test asserting no raw exception text is displayed; coverage that every registered reason code has a message.

**Completion gate.** No raw exception reaches the UI and every reason code has a presentation.

### WP-10.06 — Lifecycle, menus and shutdown

**What must be fully done.** Start-up sequence within the startup budget; single-instance routing; shutdown prompts that state consequences when work is running or unsaved; and menu contribution from the command registry.

**Testing requirements.** Startup budget measurement per product host; a shutdown-during-work test; a single-instance routing test.

**Completion gate.** Startup meets budget on reference hardware and shutdown never silently discards work.

### WP-10.07 — Accessibility and localisation baseline

**What must be fully done.** Every shell surface carries assistive-technology semantics, a correct focus order, and keyboard reachability. All strings are externalised. Right-to-left layout is supported structurally even if no such locale ships initially.

**Testing requirements.** Automated accessibility checks plus a dated manual assistive-technology verification; a pseudo-localisation pass; a right-to-left layout pass.

**Completion gate.** Automated checks pass, manual verification is recorded, and pseudo-localisation reveals no hard-coded or concatenated string.

### WP-10.08 — Third-party control admission

**What must be fully done.** Every third-party control the shell uses passes the AOT publish proof with zero diagnostics, and its licence position is recorded against the consuming boundary.

**Testing requirements.** A publish proof per control; a licence record per control.

**Completion gate.** Every admitted control has a zero-diagnostic AOT proof and a recorded licence position. **This satisfies `VG-03`.**

---

## 6. Impacts

| Dimension | Impact |
|---|---|
| Database | Device-local layout and settings storage |
| Protocol | Command availability consumes the capability model |
| UI | This package *is* the shared UI foundation |
| Security | Notification sensitivity defaults; no secret in shell state |
| Platform | Per-platform window, menu, notification and shortcut conventions |
| Migration | Settings schema migration |
| Compatibility | Token and command contracts that product packages build against |

---

## 7. Tests and verification evidence

| Evidence | Produced by |
|---|---|
| Raw-literal policy result and contrast reports per theme | `WP-10.00` |
| Layout restore matrix | `WP-10.01` |
| Shortcut conflict and availability agreement results | `WP-10.02` |
| Settings resolution and explainability results | `WP-10.03` |
| Missed-notification durability result | `WP-10.04` |
| Raw-exception prohibition and reason-code coverage | `WP-10.05` |
| Startup budget measurements and shutdown-during-work result | `WP-10.06` |
| Accessibility automated plus dated manual record; pseudo-localisation report | `WP-10.07` |
| Per-control AOT proofs and licence records | `WP-10.08` |

---

## 8. Completion gate

**All of the following, with recorded evidence:**

1. No raw colour or size literal exists in component code; contrast passes in every theme including high contrast.
2. Layout restores safely under a missing panel, a changed display arrangement and corrupted state, and is device-local.
3. Shortcut conflicts are detected, and command availability agrees with capability availability.
4. Setting resolution order is correct and every effective value is explainable.
5. Missing every transient notification never loses a durable attention item.
6. No raw exception text reaches the UI, and every reason code has a presentation.
7. Startup meets budget on reference hardware; shutdown never silently discards work.
8. Accessibility checks pass with a dated manual verification, and pseudo-localisation reveals no hard-coded or concatenated string.
9. Every third-party control has a zero-diagnostic AOT proof and a recorded licence position — satisfying `VG-03`.

---

## 9. Dependencies

**Upstream.** `06` (the AOT proof and control admission process).

**Downstream.**

| Package | What it needs from here |
|---|---|
| `14` — First slice | A shell to run the slice inside |
| `18`, `33`, `36` — product cores | The shared shell, tokens, commands, settings and attention model |
| `48`, `49` — web surfaces | The token vocabulary the web surfaces mirror |
