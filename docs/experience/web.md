# arcforges.com

Architecture: [12](../architecture/12-client-applications.md) §5, [10](../architecture/10-cloud.md), [14](../architecture/14-commercial-operations.md). Template: [README](README.md).

| Part | Technology | Origin and session |
|---|---|---|
| Public site | Static, generated in C#, no JavaScript | Anonymous |
| Account profile | Blazor WebAssembly; reused cookie session with CSRF and Origin checks; binary gRPC-Web | `account` session (reused Identity) |
| Fleet profile | Blazor WebAssembly; viewer WebSocket (`relay.v1.ViewerFrame`) plus gRPC-Web | `account` session; entitlements `remote.view` and `remote.control` |
| Operations profile | Blazor WebAssembly on its own origin (existing skeleton) | Operator session (reused operator access) |

The standard states S-LOADING, S-OFFLINE, S-FAILED and S-NOT-ENTITLED apply to every profile page. A missing session redirects to sign-in with a return URL.

## Public site

| ID | Page | Content | Data |
|---|---|---|---|
| W-01 | `/` Home | The problem and the product in one screen, the three main capabilities, screenshots, Download and Pricing calls to action | Static |
| W-02 | `/features` | Execution and queueing, resource control, caches and storage, records and diagnosis, AI integration, LAN, remote. Each feature states its platforms and honest limits (e.g. "Pause: Linux only"). | Static |
| W-03 | `/pricing` | Free and Pro feature table (product definition §5). Prices come from the build-time catalogue. While `commerce.sales_open=false` the page shows "Coming soon". | Catalogue snapshot at build time |
| W-04 | `/download` | Per-OS installers (MSI x64/arm64, `install.sh`, `.deb`, winget and Scoop commands), checksum and signature verification instructions, channel selector, AI-client plugin links. Android: Google Play badge. | Release manifest snapshot at build time |
| W-05 | `/docs` | Documentation index: install, first run, CLI, MCP, policies, LAN, troubleshooting | Static |
| W-06 | `/security` | Security model summary, vulnerability disclosure contact, signing keys and fingerprints | Static |
| W-07 | `/privacy`, `/terms`, `/refunds`, `/subprocessors` | Legal texts (supplied by the product owner, H-10) | Static |
| W-08 | `/releases` | Release notes per version and channel, revoked versions | Manifest snapshot |

- **Wireframe** (all public pages share one layout):

```
┌ ArcForges   Features  Pricing  Download  Docs                     [Sign in] ┐
│                                                                             │
│  One authority for every build, test and agent command on your machines.   │
│  [Download for Windows]  [Linux / WSL]          See how it works ↓         │
├─────────────────────────────────────────────────────────────────────────────┤
│ footer: Security · Privacy · Terms · Status · Releases                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

- **Accessibility.** The pages use landmark regions (`header`, `nav`, `main`, `footer`), a skip link and a logical heading order. Images have alternative text.

## Account profile

### W-20 Sign in

- **Purpose.** Authenticate with a passkey or an e-mail code (reused flows), and create an account.
- **Data and actions:** reused `IdentityService.BeginAuthentication`, `CompleteAuthentication`, `RequestEmailCode`, `RedeemEmailCode` and `CompleteEnrollment`.
- **States:** rate limited; code expired; account pending deletion ("Cancel deletion?" via `CancelAccountDeletion`).
- **Accessibility.** WebAuthn prompts are announced, and code fields use `autocomplete="one-time-code"`.

### W-21 Overview

```
┌ Account ─ Overview · Security · Devices & nodes · Subscription · Support · Privacy ┐
│ Hello Sam ─ Pro (renews 12 Nov)          Nodes: 3 (2 online)   Phones: 1         │
│ Needs attention: payment method expires in 9 days [Update]                       │
│ [Open Fleet ↗]                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `IdentityService.GetProfile`, `StoreBillingService.GetBillingStatus`, `FleetService.ListNodes`.

### W-22 Security

Passkeys (add, rename, remove), sessions (list, revoke one, revoke all), security activity, recovery codes and e-mail change. All operations reuse the existing `IdentityService` methods, and step-up is required for removal and revocation.

### W-23 Devices and nodes

```
┌ Devices & nodes ────────────────────────────────────────────────────────────────┐
│ Node        OS       Role   Version  Last seen   Relay   Actions                 │
│ workstation Windows  host   1.2.0    online      ✔       [Rename] [Revoke]       │
│  └ Debian   Linux    guest  1.2.0    online      ✔                               │
│ buildbox    Linux    host   1.1.4    2 h ago     ✔       [Rename] [Revoke]       │
│ Phone Pixel 9 · Android 16 · ArcForges 1.2.0 · last active today      [Revoke]   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `FleetService.ListNodes`; reused `DeviceService.List` for phones and browsers.
- **Actions:**
  - Rename (`FleetService.RenameNode`).
  - Revoke a node (`FleetService.RevokeNode`, step-up). Confirmation: "The node can no longer reach the cloud or use account LAN certificates. Local work is unaffected."
  - Revoke a phone (`DeviceService.Revoke`).

### W-24 Subscription and billing

```
┌ Subscription ─ Pro · Paddle · renews 12 Nov 2026 ───────────────────────────────┐
│ [Manage payment method ↗ Paddle] [Cancel subscription]                           │
│ Google Play: none        ⚠ Duplicate subscriptions shown here when both exist    │
│ Billing history: 12 Oct 2026  Pro monthly  paid  [Invoice ↗]                     │
│ No subscription? [Choose Pro monthly] [Choose Pro annual] → Paddle checkout      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `StoreBillingService.GetBillingStatus`; reused `CommerceService.GetSubscription`, `ListBillingHistory` and `GetCatalogue`.
- **Actions:**
  - Choose a plan: `CommerceService.CreateCheckoutAttempt`, then redirect to the Paddle-hosted checkout; the return page polls `GetPurchaseState`.
  - Cancel (`CancelSubscription`), with the confirmation "Pro features stay until 12 Nov 2026."
  - Reactivate (`ReactivateSubscription`).
  - Play subscriptions link to the Google Play subscription center.
- **States:** sales closed ("Coming soon"); payment issue; on hold; pending; refunded.

### W-25 Support

- **Content.** Cases list and detail, new case, messages, attached support bundles (name, size, upload date, expiry), and access requests from operators with **Allow for 24 h** or **Deny** (reused `SupportService.DecideAccess`).
- **Data:** reused `SupportService.ListCases`, `CreateCase` and `AppendMessage`.

### W-26 Privacy and data

Export (`DataService.RequestExport`, `GetExportState`) and account deletion (reused `RequestAccountDeletion`, with a 30-day grace period, step-up and a statement of what is deleted and kept). Active Play subscriptions block deletion until the user confirms they have cancelled in Google Play ([14](../architecture/14-commercial-operations.md) §3.3).

### W-27 `/connect` (node sign-in consent)

```
┌ Connect a node ─────────────────────────────────────────────────────────────────┐
│ "workstation" (Windows, x64, ArcForges 1.2.0) wants to connect to your account   │
│ sam@… It will be able to: appear in your fleet, receive your plan's features,   │
│ and (if you enable it on the node) be viewed and controlled remotely.            │
│ Requested 10:41 from this browser session. Expires in 08:12.                     │
│                                           [Deny]  [Connect node]                 │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data and actions:** `NodeEnrollmentService.GetNodeSignInFlow`; `ApproveNodeSignIn`, which then redirects to the loopback URI.
- **States:** expired; already used; plan node limit reached (S-NOT-ENTITLED with the limit); denied.
- **Accessibility.** The buttons are in the order Deny, Connect, and focus starts on the heading.

### W-28 `/activate` (device code)

- **Flow.** Code entry field (8 characters, `XXXX-XXXX`, case-insensitive, separators ignored), then the node details, then Approve or Deny.
- **Data and actions:** `LookupDeviceCode`, `ApproveDeviceCode`. The QR deep link pre-fills the code.
- **States:** invalid code (shows remaining attempts); expired; approved ("Return to your terminal").

### W-29 Notification preferences

Per kind (task failed, task finished, approval needed, node offline, finding) with per-node overrides, and the daily limit shown. Data: `FleetService.GetPushPreferences`, `UpdatePushPreferences`. Requires entitlement `push`.

## Fleet profile

### W-40 Fleet overview

```
┌ Fleet ─ live ● ─────────────────────────────────────────────────────────────────┐
│ workstation  online   Running 6  Queued 4  CPU 74 %  Mem 33 %  ⚠1  ①1           │
│ buildbox     online   Running 2  Queued 0  CPU 40 %  Mem 20 %                   │
│ laptop       offline  last seen 2 h ago                                          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `FleetService.ListNodes`, then `OpenFleetWatch(SUMMARY)`, then the viewer WebSocket (snapshot plus deltas). `WatchFleet` is the fallback.
- **States:** S-OFFLINE (reconnects with cursors); node offline; viewer limit reached; kill switch active ("Live updates paused; showing summaries").
- **Accessibility.** A polite live region announces state changes only for the focused node, at most every 10 s.

### W-41 Node detail

```
┌ workstation ─ online · 1.2.0 · Pressure Normal ──────────── [Refresh] [⋯ Actions] ┐
│ Tasks: dotnet build ✔ RUNNING 04:12 [Cancel] [Priority]   npm test ✖ FAILED [Tail]│
│ Approvals: Codex asks: cancel task npm test (medium) [Deny] [Approve]            │
│ Findings: ⚠ STALL dotnet test                                                    │
│ Recent commands: Cancel task npm test — SUCCEEDED 10:44                          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** viewer stream with `detail=FULL` (task summaries, findings, approvals, sessions); `FleetService.GetNode` (recent commands).
- **Actions:** each is `SendNodeCommand` with step-up for MEDIUM and HIGH, followed by command status through `command_update` frames.
  - Refresh (LOW).
  - Pause or resume the queue (LOW).
  - Cancel a task (MEDIUM).
  - Change priority (MEDIUM).
  - Approve or deny (HIGH; offered only when the node policy allows remote approvals, otherwise "Approve on the node").
  - Output tail (LOW; shown only when the node's privacy policy allows it, otherwise "Output stays on the node").
  - Run task (HIGH; argv form in a registered workspace, a dialog with explicit fields).
  - Apply update (HIGH), Stop node (HIGH).
- **Confirmations.** Each states the command, its risk, the step-up requirement and that the node applies its own policy: "The node may reject this command under its local remote-control policy."
- **States:** command EXPIRED ("The node did not receive the command within 5 minutes. It will not run later."); REJECTED_BY_NODE (shows the node's reason).

## Operations profile (operators)

| ID | Page | Content | API (reused `OperatorService` unless noted) |
|---|---|---|---|
| W-60 | Cases | Queue, filters, case detail, replies, state changes | `ListCases`, `GetCase`, `ReplyCase`, `SetCaseState` |
| W-61 | Diagnostic access | Request access to a bundle, see the user decision, read with audit | `RequestAccess`, `ReadDiagnostic`, `EndAccess` |
| W-62 | Configuration | Kill switches, limits, plan catalogue: stage, validate, approve (second operator), activate | `StageConfiguration`, `ValidateConfiguration`, `ApproveConfiguration`, `ActivateConfiguration`, `SetKillSwitch` |
| W-63 | Entitlements and compensation | Grant, revoke, goodwill extensions | `GrantEntitlement`, `RevokeEntitlement`, `IssueCompensation`, `AdjustCompensation` |
| W-64 | Refunds | Paddle refund decisions; Play refunds are issued in Play Console (link) | `DecideRefund` |
| W-65 | Trust and safety | Anomaly flags, enforcement proposals, appeals | `ProposeEnforcement`, `DecideEnforcement`, `GetAppeal`, `ResolveAppeal` |
| W-66 | Budgets | Operating budget consumption per resource class, thresholds, kill-switch state, monthly report | Read from configuration and platform budget tables through operator diagnostics (new read method added by AF-OPS-01) |
| W-67 | Break-glass and audit | Start and end break-glass, audit trail | `StartBreakGlass`, `EndBreakGlass`, audit read (existing) |

Operator pages require an operator session with step-up. Two-person approval applies where [14](../architecture/14-commercial-operations.md) §1 says so. Every page shows the audit reference of each action.
