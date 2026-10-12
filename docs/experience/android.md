# ArcForges for Android

- **Architecture:** [12](../architecture/12-client-applications.md) §6. Template: [README](README.md).
- **Platform:** .NET MAUI, Android 8.0+; reference size 412×915 dp.
- **Origin:** `REMOTE` through a session on the phone's own installation (product `arcforges-mobile`). A browser sign-in gives an `account` session. A QR pairing gives a `mobile.limited` session (fleet view, push and low-risk commands) until the first step-up upgrades it ([AD-0011](../decisions/AD-0011-identity-and-login.md) §3).
- **Entitlements:** live views need `remote.view`, actions need `remote.control`, push needs `push`.

## Global behaviour

| Topic | Behaviour |
|---|---|
| Navigation | Bottom navigation: Fleet · Approvals · Notifications · Account. Node and task detail are pushed pages. |
| Live data | Foreground only: `OpenFleetWatch`, then the viewer WebSocket, resumed by cursors. Leaving the foreground closes the socket within 5 s. Returning re-opens it and reconciles from the snapshot. |
| Background | No sockets and no polling. FCM data messages raise local notifications with deep links (`https://arcforges.com/app/node/<id>`, `/task/<id>`, `/approval/<id>`). |
| Offline | Banner "Offline · last updated <time>"; cached last snapshot shown greyed; actions disabled with the reason |
| Permissions | **Camera:** requested only when scanning, with a manual code entry fallback when denied. **Notifications** (Android 13+): requested at the first opt-in; denial is shown in settings with a link to system settings. |
| Step-up | Medium and high actions, billing and account settings trigger the step-up (`IdentityService.BeginStepUp`/`CompleteStepUp`): a passkey through Credential Manager, or an e-mail code. On a `mobile.limited` session the step-up also upgrades it to `account`. Failure leaves the action unsent. |
| Accessibility | TalkBack labels on every control (`SemanticProperties`), 48-dp targets, dynamic type up to 200 % without truncation of primary actions, no colour-only status |

## A-01 Welcome and sign-in

- **Purpose.** Sign the phone in to the account.
- **Permissions.** None before sign-in.
- **Layout.** Product mark and one sentence; QR sign-in (primary); browser sign-in; the create-account hint.
- **Wireframe:**

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
- **Data:** none until sign-in.
- **Accessibility.** The two sign-in buttons are the first two focus stops, and the QR button's name says it uses the camera.
- **Local stack.** Debug builds also accept the callback `http://10.0.2.2:<port>/app/callback` (the emulator's loopback alias) when pointed at the local cloud stack ([16](../architecture/16-testing-strategy.md) §3.1); release builds accept only the verified `https` link.

## A-02 Scan pairing code

- **Purpose.** Sign in by scanning the QR shown by a signed-in computer (D-16), without typing a password.
- **Permissions.** No session yet. The camera permission is requested here only.
- **Layout.** The camera viewfinder with a frame; the instruction; **Enter code instead**; after the scan, the "Confirm on your computer" state.
- **Wireframe:**

```
┌ Scan code ───────────────────┐
│ ┌──────────────────────────┐ │
│ │      [ viewfinder ]      │ │
│ └──────────────────────────┘ │
│ Point at the QR code in      │
│ ArcForges on your computer.  │
│ [ Enter code instead ]       │
│ ──────────────────────────── │
│ ✔ Code found. Confirm on     │
│ "workstation" (06:12 left)   │
└──────────────────────────────┘
```

- **Data and actions:**
  1. Scanning `arcforges://pair?i=<pairing_id>&s=<secret>` calls `NodeEnrollmentService.ClaimPhonePairing(pairing_id, secret, phone)`, which returns a `claim_token`.
  2. The phone shows "Confirm on your computer" and polls `PollPhonePairing(pairing_id, claim_token)` every 2 s for up to 120 s.
  3. On CONFIRMED the app stores the returned credentials in the Keystore and opens A-03. The session scope is `mobile.limited`.
- **Fallback.** Manual entry of the pairing ID and secret, which the computer shows under the QR as text.
- **States:** camera denied (manual entry offered); expired; denied on the computer; already used ("Ask your computer for a new code"); network error.
- **Accessibility.** The scanner announces "Code found" with a haptic tick. Manual entry fields have labels, and the countdown is announced at 60 s and 10 s.

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

- **Purpose.** See every node at a glance and open one.
- **Permissions.** Session of either scope; live data needs `remote.view`.
- **Layout.** The live indicator; one card per node (guests inside their host's card).
- **Data:** `FleetService.ListNodes`, then the viewer socket (SUMMARY).
- **Actions:** open a node (A-04); pull to refresh re-reads `ListNodes`.
- **Accessibility.** Each card reads as one sentence ("workstation, online, 6 running, 4 queued, 1 finding, 1 approval").
- **States:** S-EMPTY ("No nodes yet. Install ArcForges on a computer and sign in."); S-NOT-ENTITLED (shows the node list without live data, with **Get Pro**); offline.

## A-04 Node detail

- **Purpose.** Watch one node and act on its tasks.
- **Permissions.** `remote.view` to watch, `remote.control` to act. Medium- and high-risk actions need a step-up (which also upgrades a `mobile.limited` session).
- **Layout.** A header (name, state, version, pressure, **⋯** actions menu); then sections: Running and Queued tasks, Approvals for this node, Open findings, Recent commands.
- **Wireframe:**

```
┌ ← workstation ─────────── ⋯ ┐
│ online · 1.2.0 · Normal     │
│ Running                     │
│  dotnet build   04:12  [⋮]  │
│ Queued                      │
│  npm test  #2 budget_memory │
│ Approvals                   │
│  Codex: cancel npm test [›] │
│ Findings                    │
│  ⚠ STALL dotnet test        │
│ Recent commands             │
│  Cancel npm test ✔ 10:44    │
└─────────────────────────────┘
```

- **Data:** the viewer socket with FULL detail; `FleetService.GetNode` (recent commands).
- **Actions** (`SendNodeCommand`):
  - Refresh, and pause or resume the queue (low).
  - Cancel a task and change its priority (medium, step-up).
  - Approve or deny (high, step-up; only when the node allows remote approvals).
  - Apply update and stop node (high, step-up), from the **⋯** menu.
- **Confirmation** for every action, as a bottom sheet: "Cancel 'npm test' on workstation? The node applies its own remote-control policy. Requires verification." Buttons: [Cancel] [Verify and send].
- **States:** command pending (a chip on the row), then succeeded, failed, rejected or expired (a snackbar with the reason); node offline (read-only, last-known data); S-NOT-ENTITLED for control without `remote.control`.
- **Accessibility.** Row menus are named per task ("Actions for dotnet build"). Command results are announced politely.

## A-05 Task detail

- **Purpose.** Understand one task: its state, timing, owner and result.
- **Permissions.** `remote.view`; the output tail also needs the node's privacy policy to allow it.
- **Layout.** A header (title, state); facts (owner, pool, priority, start, duration); timeline categories; result (exit code, termination reason); **Show output tail**; task actions.
- **Wireframe:**

```
┌ ← npm test ──────────────────┐
│ ● RUNNING · 2 m 10 s         │
│ Owner: Codex · session 7Q2…  │
│ Pool agents · priority NORMAL│
│ Time: CPU 61% · I/O 12% ·    │
│       waiting 27%            │
│ [ Show output tail ]         │
│ [ Cancel ] [ Priority ]      │
└──────────────────────────────┘
```

- **Data:** the viewer socket (task summary) for this task.
- **Actions:**
  - **Show output tail** sends `ReadOutputTailCommand` (low). The tail arrives as a relay `OutputTail` frame and is never stored. If the node's privacy policy forbids it, the screen says "Output stays on the node".
  - **Cancel** (medium) and **Priority** (medium) as in A-04. Retry is not a remote command, so the button is absent.
- **States:** task not found (purged on the node); tail denied by policy; node offline.
- **Accessibility.** The output tail is a monospace text view with selectable text, and TalkBack reads it by line.

## A-06 Approvals

- **Purpose.** Decide approval requests from agents and scripts across all nodes.
- **Permissions.** `remote.control`; approving is a high-risk command (step-up), offered only for nodes whose policy allows remote approvals (`remote.allow_approvals`).
- **Layout.** A list of pending approvals, newest first, each with node, requester, operation, risk and expiry; the detail sheet with the full request.
- **Wireframe:**

```
┌ Approvals ───────────────────┐
│ workstation · Codex          │
│ Cancel task "npm test"       │
│ medium · expires in 23 h  [›]│
├──────────────────────────────┤
│ buildbox · script            │
│ Change policy (pool agents)  │
│ high · expires in 2 h     [›]│
└──────────────────────────────┘
```

- **Data:** the SUMMARY stream gives each node's `approvals_pending` count. While this screen is open, the app opens `OpenFleetWatch(node_ids = nodes with pending approvals, detail = FULL)` to read their `ApprovalSummary` items, and closes that watch when the screen closes.
- **Actions:** **Approve** and **Deny** send `DecideApprovalCommand` (high, step-up), with a confirmation stating the operation. For nodes without remote approvals the sheet says "Approve on the computer".
- **States:** S-EMPTY ("Nothing to approve"); expired while open; decided elsewhere (the item disappears with a snackbar).
- **Accessibility.** Each item reads node, requester, operation, risk and expiry in that order. The decision buttons are in the order Deny, Approve.

## A-07 Notifications

- **Purpose.** See past notifications and choose which events notify this account.
- **Permissions.** Session of either scope; push needs entitlement `push`. Android 13+ needs the notification permission.
- **Layout.** Two tabs: History and Preferences.
- **Wireframe:**

```
┌ Notifications ───────────────┐
│ [History] [Preferences]      │
│ ● Task failed: npm test      │
│   workstation · 10:41        │
│   Approval needed: buildbox  │
│   yesterday                  │
│ ──────── Preferences ─────── │
│ Task failed        [on ]     │
│ Approval needed    [on ]     │
│ Node offline       [off]     │
│ Max 50 per day (plan limit)  │
└──────────────────────────────┘
```

- **Data:** reused `NotificationService.List`; `FleetService.GetPushPreferences`.
- **Actions:**
  - Opening an item calls `Acknowledge` and follows its deep link.
  - Preference changes save immediately through `UpdatePushPreferences` with the revision read.
  - **Registration.** FCM registration uses the reused `NotificationService.RegisterPush` after sign-in, and `UnregisterPush` on sign-out.
- **States:** S-EMPTY ("No notifications yet"); notification permission denied (a banner with **Open system settings**); S-NOT-ENTITLED for push; revision conflict (reload).
- **Accessibility.** Unread items say "unread" in text. Switches are named by event kind.

## A-08 Subscription

- **Purpose.** Subscribe to Pro through Google Play, restore purchases, or manage a subscription.
- **Permissions.** Session with step-up for billing actions; Google Play installed.
- **Layout.** The current plan; what Pro adds; the plan buttons; restore; manage.
- **Wireframe:**

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
- **Data:** `StoreBillingService.GetBillingStatus` and `GetPlayAccountReference`; Play product details from the Billing Library.
- **Accessibility.** Prices are announced with the billing period.

## A-09 Account

- **Purpose.** See the signed-in account, manage this phone, and sign out.
- **Permissions.** Session of either scope; revoking another device needs a step-up and happens on the web.
- **Layout.** Profile (name, masked e-mail, plan); This phone (session scope, signed in since); Other devices (read-only); Security (link); Sign out.
- **Wireframe:**

```
┌ Account ─────────────────────┐
│ Sam · s…@example.com · Pro   │
│ This phone                   │
│  Pixel 9 · limited access    │
│  [ Verify to unlock all ]    │
│  [ Remove this phone ]       │
│ Other devices                │
│  workstation, buildbox (2)   │
│ Security ↗ arcforges.com     │
│ [ Sign out ]                 │
└──────────────────────────────┘
```

- **Data:** reused `IdentityService.GetProfile`; reused `DeviceService.List` (read-only).
- **Actions:**
  - **Verify to unlock all** runs the step-up and upgrades a `mobile.limited` session to `account`.
  - **Remove this phone** revokes its own device (`DeviceService.Revoke`), deletes local credentials and unregisters push.
  - **Sign out** revokes the session (`IdentityService.RevokeSession`), deletes local credentials and unregisters push.
  - **Security** opens `https://arcforges.com/account/security` in a Custom Tab.
- **States:** offline (sign-out still deletes local credentials and retries the revocation later); step-up cancelled.
- **Accessibility.** The session scope is stated in text ("limited access: viewing and low-risk actions").

## A-10 Settings and about

- **Purpose.** Set the theme, check notification status, collect diagnostics for support, and read licences and legal texts.
- **Permissions.** None beyond the app.
- **Layout.** Appearance; Notifications; Diagnostics; About (version, licences, privacy policy, terms).
- **Wireframe:**

```
┌ Settings ────────────────────┐
│ Theme  (•) System ( ) Light  │
│        ( ) Dark              │
│ Notifications: allowed       │
│ Diagnostics                  │
│  App 1.2.0 · last sync 10:44 │
│  [ Copy diagnostic summary ] │
│ About · Licences · Privacy · │
│ Terms                        │
└──────────────────────────────┘
```

- **Data:** local only: app version, last sync time, the notification permission state, the FCM registration state.
- **Actions:** theme change (applies at once); **Copy diagnostic summary** copies app version, Android version, session scope, last sync and the last error codes, with no tokens or personal data; legal links open Custom Tabs.
- **States:** notification permission denied (with **Open system settings**).
- **Accessibility.** The theme radio group has a label. The copy action announces "Copied".
