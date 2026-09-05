# Shared Desktop Experience Requirements

> Status: **Authoritative** — Phase 2 (Detailed Specifications)
> Layer: Requirements
> Companions: [`01-normative-glossary-and-invariants.md`](01-normative-glossary-and-invariants.md), [`11-policy-and-configuration.md`](11-policy-and-configuration.md), [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md), [`../architecture/04-desktop-application-architecture.md`](../architecture/04-desktop-application-architecture.md)

The four desktop products are neither four independently designed applications nor one shared shell with swapped content. The pattern is:

> **One design language, four professional workspaces.**

Founding invariant: **Shared Experience ≠ Shared Shell ≠ Shared Domain** (`I-021`).

---

## 1. Design principles

| # | Principle | Meaning |
|---|---|---|
| DP-01 | **Professional-first** | The interface serves sustained work, not first-impression delight. Density, precision and predictability outrank novelty. |
| DP-02 | **Calm UI** | Nothing moves, flashes or interrupts without cause. Attention is a budget the product spends deliberately. |
| DP-03 | **Progressive complexity** | Easy to start, efficient at depth. Advanced capability is discoverable, not front-loaded. |
| DP-04 | **Keyboard and mouse are equally first-class** | Every meaningful action is reachable by both. A keyboard-only professional must not be a second-class user. |
| DP-05 | **Local-first status is genuinely visible** | The user can always tell what is saved locally and, separately, what has reached the cloud. |

---

## 2. Design system

| # | Requirement |
|---|---|
| DS-01 | **What is unified is semantic design tokens, not literal colours.** Products consume tokens with meaning (surface, elevated surface, accent, danger, warning, success, informational, disabled, focus ring), never raw hex values. |
| DS-02 | **Product code must not invent colour semantics.** A product needing a new semantic adds a token to the system; it does not hard-code a colour. |
| DS-03 | **Product state colours are a defined, closed semantic set**, shared across all four products, so a warning means the same thing everywhere. |
| DS-04 | **Typography establishes a semantic hierarchy** — not a list of sizes. Numeric and tabular presentation is a distinct, stable typographic role, because three of the four products display precise numbers. |
| DS-05 | **Density is a first-class design-system capability**, not a per-product hack. At minimum: Comfortable, Compact, and a professional-dense mode for panel-heavy products. |
| DS-06 | **Iconography is one visual language** across all four products. |
| DS-07 | **An icon is never the only carrier of information** (`I-393` family). Every icon-only control has a label, tooltip or accessible name. |
| DS-08 | **Motion is restrained and never load-bearing.** No state may be understandable *only* through animation. |

---

## 3. Windows and workspace

### 3.1 Window semantics

| Type | Role |
|---|---|
| **Main Workspace Window** | The product's primary working surface |
| **Secondary / Document Window** | An additional document, project or session in its own window |
| **Utility Window** | A floating tool, inspector or monitor |
| **Dialog** | A bounded, focused interaction |

| # | Requirement |
|---|---|
| WN-01 | **Not every operation becomes a modal dialog.** Modality is reserved for genuinely blocking, decision-requiring interactions. |
| WN-02 | **Multi-window is a first-class capability.** `MainWindow` singleton must not be an architectural prerequisite. |
| WN-03 | **Multi-window first, multi-process second.** Multi-process is an explicit extension capability, not the default user experience. |
| WN-04 | **The same resource must not have two independent writable owners** without an explicit coordination mechanism. A `DocumentSession` owns write authority; a second view is read-only, coordinated, or refused with an explanation. Two silently-diverging local writable copies are prohibited. |
| WN-05 | **Window and layout physical state is device-local by default** and is never synced as user data (`I-181`). |
| WN-06 | **Full-screen and presentation states are not permanently forced to restore.** A product does not reopen into an unexpected immersive mode. |

### 3.2 Panels, docking and layout

| # | Requirement |
|---|---|
| LY-01 | A shared **dock/panel foundation** supports: dockable panels, floating panels, tabbed panel groups, splitters, panel visibility toggles, panel reset, and **named saved layouts**. |
| LY-02 | **ArcScope and ArcSlate are panel-heavy professional workspaces**; ArcChat is conversation/task-centred; ArcNotes is document/knowledge-centred. All four use the same foundation with different compositions. |
| LY-03 | **What may sync later is a named Layout *definition*, never physical window coordinates.** Monitor geometry is device-specific. |
| LY-04 | The word for a panel arrangement is **Layout**. "Workspace" always means the cloud ownership boundary (`I-001`, glossary §8). |

---

## 4. Command system

**Command is the semantic identity of an action.** It is the single foundation under menus, toolbars, context menus, shortcuts and the command palette.

| # | Requirement |
|---|---|
| CM-01 | Every action has a **stable command identity**. |
| CM-02 | **Menu, toolbar, context menu, shortcut and palette must not implement behaviour separately.** They all invoke the same command, which calls the same application service. |
| CM-03 | **The same user operation must never produce different business logic because it was reached from a different entry point.** |
| CM-04 | **A command knows its own availability**: enabled, disabled with reason, hidden, or requiring elevation/approval. A disabled command explains why. |
| CM-05 | **Command scope is explicit** — application, window, document/session, panel, selection — and resolution priority is fixed and documented, from most specific to least. |
| CM-06 | **Undo/redo uses unified command identity, but undo state belongs to the owning product** (`I-201`). **There is no global ArcForges undo service.** |
| CM-07 | **A command palette is a shared capability of all four products**, with the same invocation gesture and behaviour. |
| CM-08 | **A quick-entry bar** (find, jump, run) is available in all four products with consistent semantics. |

### 4.1 Shortcuts

Four levels, resolved in a defined order:

| Level | Example |
|---|---|
| **Platform standard** | Copy, paste, save, close, undo |
| **ArcForges shared** | Command palette, settings, activity surface, quick jump |
| **Product-specific** | Timeline navigation, capture control, block formatting |
| **User custom** | Any rebinding |

| # | Requirement |
|---|---|
| SH-01 | **Shortcuts are a projection of the command system**, never an independent input map. |
| SH-02 | **Conflicts are detected and managed by the system**, with a visible resolution surface. |
| SH-03 | **Context-scoped conflicts are legal** where contexts cannot overlap; the system distinguishes a genuine conflict from a scoped coexistence. |
| SH-04 | **OS-reserved and unsafe shortcuts are never captured.** |
| SH-05 | User remapping is supported, persisted as a device setting, and resettable. |

---

## 5. Settings

**Settings is not a flat dictionary.**

### 5.1 Scopes

| Scope | Examples |
|---|---|
| **Account preference** | Locale, timezone, notification preferences |
| **Workspace setting** | Workspace-level defaults and organization-visible configuration |
| **Device setting** | Paths, hardware, GPU, local cache, remote-access consent, layout |
| **Product setting** | Per-application behaviour |
| **Project / document setting** | Per-project overrides |
| **Session setting** | Transient, this-session only |

| # | Requirement |
|---|---|
| SE-01 | **Each setting declares which scopes it may appear in, and its own resolution rule.** A single global override chain applied to all settings is prohibited. |
| SE-02 | **Every effective setting value exposes its source**: which scope supplied it, and whether it is overridden or locked. |
| SE-03 | **Settings ≠ Policy** (`I-340`). A user preference and an administratively enforced policy are separate systems; a policy-locked setting shows as locked with its reason. |
| SE-04 | **A secret is never an ordinary setting** (`SE-01` in the security requirements). Secret fields store a `SecretRef` and never display plaintext. |
| SE-05 | **Settings user experience is unified** across products: the same organisation, the same search, the same reset semantics, the same scope indicators. |
| SE-06 | **Reset never deletes business data.** "Reset ArcNotes settings" resets settings; it does not touch notebooks. The scope of a reset is stated before it runs. |

---

## 6. Attention, notification and status

### 6.1 The attention model

Five channels, chosen by **durability**, not only by severity:

| Channel | For |
|---|---|
| **Inline state** | Something visible where the user already is |
| **Toast** | Transient confirmation that needs no follow-up |
| **Persistent attention item** | Something the user must eventually act on |
| **OS notification** | The user is not looking at the application |
| **Email / push** | The user is not at the device |

| # | Requirement |
|---|---|
| AT-01 | **A toast must never carry attention that requires later action.** Anything needing follow-up becomes a persistent attention item. |
| AT-02 | Severity is a **unified, closed set**, and error red is not overused. Informational states are visually distinct from failure states. |
| AT-03 | **Notifications deduplicate**: a continuing condition updates one status item rather than emitting a stream. |
| AT-04 | **ArcChat may aggregate cross-application attention without taking ownership.** An ArcScope condition displayed in ArcChat is still owned, resolved and cleared by ArcScope. |
| AT-05 | Notification content respects the sensitivity rules in [`03-cloud-services-and-sync.md`](03-cloud-services-and-sync.md) §11. |

### 6.2 Save and sync status

| # | Requirement |
|---|---|
| ST-01 | **Local Saved and Cloud Synced are always two different states** (`I-199`). |
| ST-02 | **Cloud Pending ≠ Unsaved** (`I-200`). A locally durable document with a pending upload must not produce a "you have unsaved changes" prompt. |
| ST-03 | **A cloud failure must not put the whole application into a red offline mode.** The product is local-first; cloud state is a secondary indicator. |
| ST-04 | Cloud status is presented per the state vocabulary in [`03-cloud-services-and-sync.md`](03-cloud-services-and-sync.md) §4. |

### 6.3 Activity surface

| # | Requirement |
|---|---|
| AV-01 | Every product has one **Activity surface** listing background work: indexing, sync, import, export, render, capture, agent tasks. |
| AV-02 | Progress follows the unified model — determinate, milestone or indeterminate — and never fabricates a percentage. |
| AV-03 | **Cancel is accurate**: `Canceling` is shown while the operation reaches a safe point, and `Canceled` only when it has actually stopped. |
| AV-04 | **Cross-application progress must not be presented as a local operation.** The interface always shows the owning product actually performing the work. |

---

## 7. Errors

| # | Requirement |
|---|---|
| ER-01 | **Every error states the impact and the recovery path.** "Is my data safe?" must be answerable from the message. |
| ER-02 | **An exception stack is never the normal product error surface.** Details are available at a second level, on request. |
| ER-03 | Errors use a **unified classification**: validation, conflict, dependency unavailable, recoverable operation failure, partial success, document/project recovery problem, fatal application failure. |
| ER-04 | **"Retry" is not a universal button.** It appears only where retry is genuinely safe. A conflict offers *resolve*; an unknown external effect offers *reconcile*; a permission failure offers neither. |
| ER-05 | A conflict surfaces the conflicting versions and a resolution path (`CF-03`). |
| ER-06 | A **partial success** enumerates what succeeded and what did not (`PR-07`). |
| ER-07 | A **document or project recovery problem** is presented as a data-state matter with explicit options, never as a generic failure. |
| ER-08 | Error reason vocabularies are separated: security, policy, entitlement and operational reasons are distinct (`SR-03`). |

---

## 8. Deep links

One namespace for the whole family: `arcforges://`.

Four semantics:

| Semantics | Meaning |
|---|---|
| **Open Product** | Launch or focus a product |
| **Navigate** | Go to a place in that product |
| **Resource** | Open a specific resource by stable identity |
| **Handoff** | Carry an intent plus a reference from one product to another |

| # | Requirement |
|---|---|
| DL-01 | **A deep link must never become an invisible remote execution API** (`I-062`). It opens the corresponding interface with a pre-filled intent; it does not execute a side-effecting action. |
| DL-02 | **An externally originated deep link is always untrusted input**, validated and never trusted to name arbitrary local paths. |
| DL-03 | **A deep link never embeds a secret** and **is never a permission token** (`I-063`). |
| DL-04 | **Deep links address stable identity**, never absolute file paths (`SY-12`). |
| DL-05 | **A deep link degrades gracefully when the target product is not installed**, offering an explanation and a download route rather than failing silently. |

---

## 9. File associations, drag and drop, clipboard

### 9.1 File associations

| # | Requirement |
|---|---|
| FA-01 | **ArcForges registers only native formats it genuinely owns.** |
| FA-02 | **Common formats do not seize default associations** (`I-536` family). Support for opening or importing a common format is offered through "Open with", not by claiming the system default. |
| FA-03 | **Open and Import are different operations** with different outcomes and different user language (`I-209`). |
| FA-04 | Opening a native project routes to an existing instance where appropriate before creating a new one. |

### 9.2 Drag and drop

| # | Requirement |
|---|---|
| DD-01 | **Data transfer semantics are unified and explicit**: Open, Import, Copy, Reference, Move. |
| DD-02 | **Drop does not mean Copy by default.** The intended semantics depend on source, target and modifier, and are always shown. |
| DD-03 | **Cross-application drop is non-destructive by default** — reference or import, never a silent destructive move. |
| DD-04 | **Dragging a large file does not copy bytes.** A `ResourceRef` or controlled reference crosses the boundary. |
| DD-05 | **Dragging to a cloud surface never uploads silently.** Cloud transmission is always an explicit act (`AS-03`). |
| DD-06 | **The drop target displays the action that will occur** before the drop completes. |

### 9.3 Clipboard

| # | Requirement |
|---|---|
| CB-01 | Clipboard behaviour is part of the shared experience: consistent formats offered, consistent paste semantics, consistent handling of rich versus plain content. |
| CB-02 | **The clipboard must never carry a secret.** |
| CB-03 | Large content crosses by reference where the target supports it. |

---

## 10. Lifecycle

| # | Requirement |
|---|---|
| LF-01 | **Window close, application quit and background work are three different concepts.** "Close window = exit" must not be hard-coded. |
| LF-02 | **Ordinary professional products do not silently reside in the background** long-term. |
| LF-03 | **ArcChat is the stated background/tray exception**, and the user must know it is running. |
| LF-04 | **ArcScope and ArcSlate may continue in the background while genuinely working** — an active capture, an active render — and the interface makes that visible and stoppable. |
| LF-05 | **Closing a window must never destroy confirmed data.** Anything locally durable stays durable; there is no "save?" prompt for content already committed. |
| LF-06 | **The exit sequence is consistent across products**: stop accepting new work, drain in-flight work, flush critical transactions, release local RPC and cloud connections, shut down native runtimes, exit. |
| LF-07 | **A recovery surface appears uniformly on the first launch after a crash**, explaining what was recovered, what was quarantined, and what the user may do. |
| LF-08 | **Update is part of the lifecycle experience**, not an interruption: the user is informed, and the restart is scheduled rather than forced. |
| LF-09 | **A sudden restart must never be forced during critical work.** Pending updates defer. |
| LF-10 | **Startup behaviour is explicit.** No product enables launch-at-login by default. |

---

## 11. Menus and interaction conventions

| # | Requirement |
|---|---|
| MN-01 | A **shared menu architecture** gives the four products the same top-level organisation for shared concerns (application, file/project, edit, view, window, help), with product-specific menus in between. |
| MN-02 | **Platform desktop conventions are respected**, notably on macOS. The goal is **semantic consistency, not pixel-identical interfaces**. |
| MN-03 | **Context menus are built from the current selection** and the command system, never from a static list. |
| MN-04 | **A toolbar is not a command dump.** It carries the highest-frequency, most important commands for the current context. |
| MN-05 | **Selection has a unified visual and behavioural model** across products: single, range, multiple, and its relationship to keyboard navigation. |
| MN-06 | **Focus ≠ Selection** (`I-404`). They are separate states with separate visual treatments. |

---

## 12. Account and cloud surfaces

| # | Requirement |
|---|---|
| AC-01 | **Account is never a first-launch gate** (`ID-01`). There is no login screen before first use. |
| AC-02 | The **account surface is in the same place with the same behaviour in every product**: identity, realm, workspace, storage summary, and "Manage Account →". |
| AC-03 | **The workspace selector must clearly express that it changes cloud ownership context** — what is synced, where new cloud objects go, which knowledge scope applies. It is not a cosmetic filter. |
| AC-04 | **Cloud status presentation is unified** across products. |
| AC-05 | Contextual cloud prompts are permitted where they are genuinely contextual and non-intrusive; they must not become recurring upsell interruptions. |

---

## 13. Help, about and problem reporting

| # | Requirement |
|---|---|
| HP-01 | Help is a unified surface: documentation, keyboard reference, what's new, support entry. |
| HP-02 | **About displays**, consistently across products: product version, build id, contract set version, data schema version, native ABI version where applicable, licence and third-party notices. |
| HP-03 | **"Report a problem" does not upload logs automatically.** A diagnostic bundle is assembled, its contents are shown, it is redacted by default, and the user chooses whether to send it (`I-424`). |

---

## 14. Cross-application handoff experience

| # | Requirement |
|---|---|
| HO-01 | **Handoff shows the owning product** that will do the work (`I-020`). |
| HO-02 | **Target not installed** — explain and offer the download route; never fail silently. |
| HO-03 | **Target version too old** — state the required version specifically (`FL-05`), never "tool failed". |
| HO-04 | **Target not running** — launch on demand where permitted, with the launch visible to the user. |
| HO-05 | **Cross-application progress is attributed to the owner** (`AV-04`). |

---

## 15. Shared foundation boundary

| # | Requirement |
|---|---|
| SF-01 | **The shared foundation must not become a giant shared UI library.** It provides mechanism and experience primitives; product-specific composition stays in the product. |
| SF-02 | **Shared UI may never hold professional domain state** (`I-022`). |
| SF-03 | The judgement rule: something belongs in the shared foundation when it is (a) experienced identically by users across products, (b) free of domain semantics, and (c) stable enough that a change is a deliberate cross-product event. Anything else stays in the product. |
| SF-04 | **A shared business ViewModel is prohibited.** ViewModels are product-owned, and per **D-021** are not shared with mobile either. |

---

## 16. Accessibility and localisation hooks

Full accessibility and localisation requirements are specified in [`12-quality-and-compatibility-contract.md`](12-quality-and-compatibility-contract.md). This layer guarantees the hooks:

| # | Requirement |
|---|---|
| AX-01 | Every shared control exposes an accessible name, role, value and state. |
| AX-02 | **Keyboard accessibility is a foundation concern, not a per-product afterthought** (`I-394`). Focus order, focus visibility and keyboard traversal are provided by the foundation. |
| AX-03 | **Every user-visible string is localisable from the outset**, including in shared components. |
| AX-04 | **Locale-safe data handling is separate from a localised interface** (`I-395`). Numbers, dates, units and sorting are canonical in storage and localised only in presentation (`I-396`). |

---

## 17. Explicit non-responsibilities

Stage-14 shared experience does **not** own:

- Any product's domain model, editor semantics or professional workflows
- Undo state (owned by each product)
- Sync mechanics (specified in the cloud requirements)
- Policy (specified in the policy requirements)
- Security decisions (specified in the security requirements)
- Performance budgets and accessibility conformance targets (specified in the quality contract)

---

## 18. Architecture invariants

| # | Invariant |
|---|---|
| SI-01 | The four products share the design language, not a mandatory shell layout. |
| SI-02 | Professional products may differ in density and workspace composition. |
| SI-03 | Menu, toolbar, shortcut and palette revolve around unified command semantics. |
| SI-04 | The same user operation must not produce different business logic from a different entry point. |
| SI-05 | Commands carry context and scope; there is no global shortcut dumping ground. |
| SI-06 | User shortcuts support conflict detection and remapping. |
| SI-07 | Settings have explicit scope; a global dictionary is prohibited. |
| SI-08 | A secret is never an ordinary setting. |
| SI-09 | Settings are strictly separate from policy. |
| SI-10 | Local Saved and Cloud Synced are always two different states. |
| SI-11 | A toast never carries attention that requires later action. |
| SI-12 | Errors explain impact and recovery; the normal path never exposes an exception stack. |
| SI-13 | Deep links use the unified ArcForges namespace. |
| SI-14 | A deep link cannot bypass confirmation to perform a dangerous operation. |
| SI-15 | Common file formats do not seize system default associations. |
| SI-16 | Drag and drop specifies Open / Import / Copy / Reference / Move semantics. |
| SI-17 | Cross-application drop is non-destructive by default. |
| SI-18 | Drag and clipboard never move large payloads across applications. |
| SI-19 | Window close, application quit and background work are distinct. |
| SI-20 | No product silently resides in the background, except ArcChat or explicitly active work. |
| SI-21 | Multi-window is a formal capability; `MainWindow` singleton is not an architectural prerequisite. |
| SI-22 | Multi-window is the default; multi-process is an explicit extension. |
| SI-23 | The same resource cannot have two local writable owners without a coordination mechanism. |
| SI-24 | Window and layout physical state is device-local by default. |
| SI-25 | Account is not a first-launch gate. |
| SI-26 | A cloud failure cannot render a local-first product unusable. |
| SI-27 | Cross-application user interface always shows the owning product doing the work. |
| SI-28 | Shared UI shares mechanism and experience only, never professional domain state. |

---

## 19. Shared experience surface

```
ArcForges Desktop Experience
├── Design System          Semantic tokens · Typography · Icons · Density · Motion
├── Window / Workspace     Main windows · Panels · Docking · Layout · Multi-window
├── Command Foundation     Commands · Menu · Toolbar · Context menu · Shortcut · Palette
├── Settings Experience    Account · Workspace · Device · Product · Project/Document
├── Status & Attention     Local save · Cloud sync · Activities · Notifications · Errors
├── Navigation             Deep links · File associations · Drag & drop · Clipboard · Handoff
└── Lifecycle              Launch · Close · Quit · Background · Update · Crash recovery · Restore
```

---

## 20. Acceptance scenarios

**Consistency** — a user moving between the four products finds settings in the same place, invokes the command palette the same way, and encounters logically consistent shortcuts.

**Command parity** — the same action from menu, toolbar, context menu, shortcut and palette produces one identical domain command and one identical audit outcome.

**Disabled command** — a disabled command explains why, rather than being silently inert.

**Shortcut conflict** — a user rebinding onto an occupied key sees the conflict and resolves it; an OS-reserved combination is refused.

**Settings scope** — a setting overridden at device scope shows its source; a policy-locked setting shows as locked with its reason; resetting product settings leaves documents untouched.

**Save versus sync** — an offline edit shows locally saved and cloud pending, with no unsaved-changes prompt on close.

**Cloud outage** — every product remains fully usable; only cloud indicators degrade.

**Attention** — a completed background job produces a toast; a required approval produces a persistent attention item that survives restart.

**Error** — a conflict offers resolve, not retry; a permission failure offers neither; a partial success enumerates outcomes; every message answers whether data is safe.

**Deep link** — opens the target surface with a pre-filled intent; a link attempting a destructive action requires confirmation; a link to an uninstalled product explains and offers a download.

**Drag and drop** — a cross-application drop shows the semantics before dropping, defaults to non-destructive, and moves a large asset by reference.

**Lifecycle** — closing a window with a running capture keeps the capture running and says so; quitting drains and flushes; a crash produces a recovery surface on next launch; an update defers rather than interrupting critical work.

**Multi-window** — a second window on the same document does not create a second writable owner.

**Accessibility** — every command is keyboard-reachable, every icon-only control has an accessible name, and focus is always visible.

---

## 21. Traceability

| Source | Consumed as |
|---|---|
| `I4 §Stage 14` | The entire shared desktop experience contract: design principles, design system, windows and panels, commands and shortcuts, settings scopes, attention model, errors, deep links, file associations, drag and drop, clipboard, lifecycle, menus, account surfaces, handoff, the shared-foundation boundary, and the 28 architecture invariants |
| `I4 §Stage 13 §58`, `§74–75` | Account experience shared without an ArcChat dependency; shared foundation must not become a fifth product |
| `I3 §9` | Avalonia desktop architecture, MVVM boundaries, threading, multi-window and multi-instance rules |
| **D-021** | ViewModels are not shared across UI stacks |
