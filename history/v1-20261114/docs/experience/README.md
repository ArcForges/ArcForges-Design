# Experience specifications

These specifications satisfy R-UX-001..006. Each page or screen is specified with the template in §2. Surfaces:

| Document | Surface | Page IDs |
|---|---|---|
| [desktop.md](desktop.md) | ArcForges Desktop (Avalonia) | D-00 … D-22 |
| [cli.md](cli.md) | `arcforges` CLI | C-01 … (command groups) |
| [mcp.md](mcp.md) | MCP adapter tools | M-01 … |
| [web.md](web.md) | arcforges.com: public site, Account, Fleet and Operations profiles | W-01 … |
| [android.md](android.md) | ArcForges for Android | A-01 … |
| [journeys.md](journeys.md) | End-to-end journeys J-01 … J-10 across surfaces | — |

## 1. Shared principles

- **The node is the authority.** Clients render node state from `NodeEventService.Subscribe` and act only through RPCs ([12](../architecture/12-client-applications.md) §1). Remote surfaces act only through `FleetService.SendNodeCommand`.
- **Honest labels.** Inferred values (`NETWORK_WAIT`, unattributed processes, coverage gaps) are shown as inferred. Enforcement states show the capability value and its reason. Values from fakes or simulations are never shown as real.
- **Confirmations.** Destructive or irreversible actions show a confirmation that states what will happen, its scope, and whether it can be undone, with the destructive button last. Medium- and high-risk remote actions also need a step-up.
- **Identifiers.** Shown as the first 8 characters of the Crockford base32 ID, with copy-full-ID on demand.
- **Time.** Relative time ("3 min ago"), with the absolute local time on hover or focus. Durations are shown as `1 h 04 m`.
- **Units.** CPU as cores with one decimal (millicores ÷ 1000); memory in GiB or MiB with binary prefixes.
- **Design system.** `ArcForges.DesignSystem` tokens (reused): light, dark and high-contrast themes; 8-px spacing grid; type scale; status colours, each paired with an icon and text, never colour alone.

## 2. Page template

Every page section in the surface documents contains:

| Item | Content |
|---|---|
| Purpose | What the user accomplishes |
| Permissions | Origin and role required. Desktop and interactive CLI are `HUMAN`, the MCP adapter is `AGENT`, web and Android are `REMOTE` through an account session. Entitlements where gated. |
| Layout | Regions and their order |
| Wireframe | ASCII wireframe at the reference size (Desktop 1280×800, web 1280 wide, Android 412×915) |
| Data | Read RPCs and subscribed event topics |
| Actions | Controls → RPCs, with confirmations |
| States | The standard states of §3 that apply, plus page-specific states |
| Accessibility | Focus order, accessible names, keyboard shortcuts, live regions |

## 3. Standard states

| Code | State | Behaviour |
|---|---|---|
| S-LOADING | First data not yet received | Skeleton placeholders; no spinner longer than 300 ms without a skeleton; the live region announces "Loading <page>" |
| S-EMPTY | No items | An explanation plus the primary next action (e.g. "No tasks yet. Run `arcforges run -- dotnet build` or use Run task.") |
| S-NODE-STOPPED | The local node is not running (`ConnectionState.NODE_STOPPED`) | Full-page banner "ArcForges node is not running", with **Start node** (Desktop) and the last-known data greyed out |
| S-RECONNECTING | Connection lost; retrying | Thin top banner "Reconnecting…"; data is kept but marked stale with the last-updated time; actions disabled |
| S-INCOMPATIBLE | Contract major mismatch | Blocking message naming both versions, with **Update** |
| S-DENIED | `AUTHORIZATION/permission_denied` | Inline message naming the policy rule; the action stays visible but disabled |
| S-APPROVAL | `AUTHORIZATION/approval_required` | Inline "Waiting for approval" chip linked to the approval; the action resolves when the approval is decided |
| S-FAILED | Any other `ArcError` | Inline error with the message, a **Retry** button (same `command_id`) when the retry mode allows, and copy-correlation-ID |
| S-EXPIRED | Plans, flows, offers or approvals that expired | Message plus **Start again** |
| S-OFFLINE | Cloud surfaces without connectivity | Banner with the last-updated time; actions disabled with the reason |
| S-NOT-ENTITLED | `ENTITLEMENT/feature_not_entitled` | Explanation of the plan feature, with **See plans** (web) or **Manage subscription** |

## 4. Accessibility baseline (WCAG 2.2 AA)

- **Keyboard.** Every interactive control is reachable in a logical focus order, with a visible focus indicator (2-px outline, 3:1 contrast). No keyboard traps.
- **Target size and names.** Targets are at least 24×24 CSS px (web and Desktop) or 48×48 dp (Android). Each control has an accessible name equal to its visible label plus context, e.g. "Cancel task dotnet build".
- **Live regions.**
  - *Polite:* task state changes on the page in view, new findings and reconnect banners.
  - *Assertive:* only for confirmation dialogs and errors after a user action.
- **Contrast and motion.** Text contrast is at least 4.5:1, or 3:1 for large text and UI components. Charts have tables as accessible alternatives. Motion respects reduced-motion settings.
- **Verification.** Automated checks (Avalonia headless tree assertions, bUnit plus axe-core-equivalent rules in C#, MAUI semantic properties) run in the UI tests. The human screen-reader session is deferred (acceptance register).
