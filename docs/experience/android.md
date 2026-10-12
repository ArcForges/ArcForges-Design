# ArcForges for Android

- **Architecture:** [12](../architecture/12-client-applications.md) §6. Template: [README](README.md).
- **Platform:** .NET MAUI, Android 8.0+; reference size 412×915 dp.
- **Origin:** `REMOTE` through an `account` session on a `MOBILE` installation.
- **Entitlements:** live views need `remote.view`, actions need `remote.control`, push needs `push`.

## Global behaviour

| Topic | Behaviour |
|---|---|
| Navigation | Bottom navigation: Fleet · Approvals · Notifications · Account. Node and task detail are pushed pages. |
| Live data | Foreground only: `OpenFleetWatch`, then the viewer WebSocket, resumed by cursors. Leaving the foreground closes the socket within 5 s. Returning re-opens it and reconciles from the snapshot. |
| Background | No sockets and no polling. FCM data messages raise local notifications with deep links (`https://arcforges.com/app/node/<id>`, `/task/<id>`, `/approval/<id>`). |
| Offline | Banner "Offline · last updated <time>"; cached last snapshot shown greyed; actions disabled with the reason |
| Permissions | **Camera:** requested only when scanning, with a manual code entry fallback when denied. **Notifications** (Android 13+): requested at the first opt-in; denial is shown in settings with a link to system settings. |
| Step-up | Medium and high actions trigger the reused step-up (passkey through Credential Manager, or recent authentication). Failure leaves the action unsent. |
| Accessibility | TalkBack labels on every control (`SemanticProperties`), 48-dp targets, dynamic type up to 200 % without truncation of primary actions, no colour-only status |

## A-01 Welcome and sign-in

```
┌──────────────────────────────┐
│        ArcForges             │
│  See and control your        │
│  ArcForges machines.         │
│                              │
│ [ Sign in with QR from       │
│   your computer ]            │
│ [ Sign in with browser ]     │
│                              │
│ No account? Create one at    │
│ arcforges.com                │
└──────────────────────────────┘
```

- **Actions:**
  - QR leads to A-02.
  - Browser opens a Custom Tab with PKCE (reused native authorization) and returns through the verified app link `https://arcforges.com/app/callback`.
- **States:** cancelled in browser; network error; account pending deletion.

## A-02 Scan pairing code

- **Purpose.** Sign in by scanning the QR shown by a signed-in desktop (D-16).
- **Flow:**
  1. Scan `arcforges://pair?i=…&s=…`, which calls `ClaimPhonePairing`.
  2. The phone shows "Confirm on your computer" and polls `PollPhonePairing` every 2 s for up to 120 s.
  3. On CONFIRMED the app stores the credentials (Keystore) and opens A-03.
- **Fallback.** Manual entry of the pairing ID and secret, shown under the QR as a text code on the desktop.
- **States:** camera denied (manual entry offered); expired; denied on desktop; consumed (wrong code: "Ask your computer for a new code").
- **Accessibility.** The scanner announces "Code found" with a haptic tick. Manual entry fields have labels.

## A-03 Fleet

```
┌ Fleet ─────────────── ● live ┐
│ workstation        online    │
│ 6 running · 4 queued  ⚠1 ①1 │
│ CPU 74 %  Mem 33 %           │
├──────────────────────────────┤
│ buildbox           online    │
│ 2 running · 0 queued         │
├──────────────────────────────┤
│ laptop      offline (2 h)    │
└──────────────────────────────┘
```

- **Data:** `FleetService.ListNodes`, then the viewer socket (SUMMARY).
- **States:** S-EMPTY ("No nodes yet. Install ArcForges on a computer and sign in."); S-NOT-ENTITLED (shows the node list without live data, with **Get Pro**); offline.

## A-04 Node detail

- **Sections:** status summary; Running and Queued tasks; Approvals for this node; Open findings; Recent commands.
- **Data:** viewer FULL detail; `FleetService.GetNode`.
- **Actions** (`SendNodeCommand`): Refresh; Pause or resume the queue; Cancel task (medium, step-up); Priority (medium, step-up); Approve or deny (high, when the node allows it); Apply update (high).
- **Confirmation** for every action, as a bottom sheet: "Cancel 'npm test' on workstation? The node applies its own remote-control policy. Requires verification." Buttons: [Cancel] [Verify and send].
- **States:** command pending (spinner chip on the row) → succeeded, failed, rejected or expired (snackbar with the reason).

## A-05 Task detail

- **Shows:** title, state, owner (client and session), pool, priority, started time and duration, timeline summary categories, exit code and termination reason.
- **Output tail.** **Show output tail** sends `ReadOutputTailCommand` (LOW). It appears only when the node's privacy policy allows it, otherwise the screen says "Output stays on the node".
- **Accessibility.** The output tail is in a monospace text view with selectable text, and TalkBack reads it by line.

## A-06 Approvals

Pending approvals across nodes, newest first, each with node, requester, operation, risk and expiry. Approve and Deny are HIGH-risk commands: step-up is required and they are offered only for nodes whose policy allows remote approvals. States: S-EMPTY ("Nothing to approve").

## A-07 Notifications

- **History.** Reused `NotificationService.List` and `Acknowledge`.
- **Preferences** (`FleetService.GetPushPreferences`, `UpdatePushPreferences`): per kind, with per-node overrides, and the daily limit shown.
- **Registration.** FCM registration uses the reused `NotificationService.RegisterPush` after sign-in, and `UnregisterPush` on sign-out.

## A-08 Subscription

```
┌ Subscription ────────────────┐
│ Free                         │
│ Pro adds: LAN placement and  │
│ cache sharing, remote status │
│ and control, notifications.  │
│ [ Pro monthly – price ]      │
│ [ Pro annual – price ]       │
│ Restore purchases            │
└──────────────────────────────┘
```

- **Flow:**
  1. `StoreBillingService.GetPlayAccountReference`.
  2. Launch the Play billing flow with `obfuscatedAccountId`.
  3. On PURCHASED, `SubmitPlayPurchase` and show the result.
  4. PENDING purchases show "Waiting for payment".
- **Restore:** query purchases, then `RestorePlayPurchases`. NEEDS_CONFIRMATION shows "This purchase was made outside the app. Link it to sam@…?", which calls `ConfirmPurchaseLink` with step-up.
- **Manage:** deep link to the Google Play subscription center. A Paddle web subscription shows "Managed on arcforges.com".
- **States:** sales closed ("Coming soon"); region not supported (Play response); duplicate warning; payment issue or hold (fix-payment deep link).
- **Accessibility.** Prices are announced with the billing period.

## A-09 Account

Profile, this phone (revoke and sign out), other devices (read-only list), security (opens arcforges.com security pages), and sign out. Sign-out deletes local credentials and unregisters push.

## A-10 Settings and about

Theme (system, light, dark), notification permission status, diagnostics (app version, last sync, **Copy diagnostic summary**), licences, privacy policy and terms links.
