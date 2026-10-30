# arcforges.com

Architecture: [12](../architecture/12-client-applications.md) §5, [10](../architecture/10-cloud.md), [14](../architecture/14-commercial-operations.md). Template: [README](README.md).

**Amended 2026-10-28 by [AD-0021](../decisions/AD-0021-central-access-go-center.md) (target until each AF-CTR task is delivered).** W-03's statement that everything local and on the LAN is free is withdrawn: the page states the editions and hosting distinction of AD-0021 §13, with plan contents from the owner's decision (H-07). The center serves its own sign-in, `/connect` and `/activate` pages so that self-hosted centers need no Web deployment; the official site's profiles use the same API. LAN mentions are out of current delivery.

| Part | Technology | Origin and session |
|---|---|---|
| Public site | Static, generated in C#, no JavaScript | Anonymous |
| Account profile | Blazor WebAssembly; cookie session with CSRF and Origin checks (AF-ID-01); binary gRPC-Web | `account` session (Identity) |
| Fleet profile | Blazor WebAssembly; viewer WebSocket (`relay.v1.ViewerFrame`) plus gRPC-Web | `account` session; entitlements `remote.view` and `remote.control` |
| Operations profile | Blazor WebAssembly on its own origin (existing skeleton) | Operator session with step-up (AF-OPS-01) |

The standard states S-LOADING, S-OFFLINE, S-FAILED and S-NOT-ENTITLED apply to every profile page. A missing session redirects to sign-in with a return URL.

## Center pages (AD-0021; delivered by AF-CTR-03 part A2, Cloud #121)

The center serves its own minimal account pages, so that a self-hosted or acceptance center works without any Web deployment. They are not the Account profile above (the Blazor pages W-20 to W-29 stay the product's web UI); they decide nothing the API does not, and every change goes through the same operation table, step-up evidence, rate limits and audit events as the API method it stands for.

| Page (below the public base URL) | Purpose | Credential |
|---|---|---|
| `/account/sign-in`, `/account/bootstrap` | Passkey sign-in; the owner bootstrap of an acceptance or self-hosted center | none |
| `/account/passkeys`, `/account/sessions`, `/account/devices`, `/account/sign-out` | List, add, rename and remove passkeys; end sessions; rename and revoke devices; sign out | cookie session |
| `/connect`, `/activate` | Node sign-in consent and device code (W-27, W-28; AF-CTR-04) | cookie session |

- **Browser sessions.** The pages' JSON calls use the WebBrowserSession document (`public/http/v1/web-browser.schema.json`, routes `/session/v1/web/*`), which admits the product `arcforges-web`. The cookie is `__Host-af_session` (Secure, HttpOnly, SameSite=Strict, no Domain), idle 30 minutes and absolute 12 hours, renewed only by a page load or the bootstrap read. CSRF is derived from the cookie handle (never stored); before a session exists the sign-in steps use a public constant of the origin and rest on the flow, the challenge, the WebAuthn origin binding and the rate limits. Every POST needs exactly one `Origin` equal to the public origin; a query string is refused; a return path travels in the URL fragment and is followed only when it is a path of the page's own origin.
- **Constraints.** No external asset; one script (`account.js`, text only through `textContent`, so Trusted Types can be required); exactly seven security headers on every reply of the center (CSP with `default-src 'none'` and `trusted-types 'none'`, `X-Frame-Options`, `Referrer-Policy: same-origin`, COOP, Permissions-Policy for publickey credentials, `Cache-Control: no-store`, `nosniff`); a page that needs its script says so. A page lists at most 30 items and says when there are more. The hosted Worker forwards only the exact paths and rejects a reply that lacks a header.
- **Passkeys only for now.** E-mail sign-in is `not_offered` on the browser channel until the live mail sender (the last AF-CTR-03 PR).
- **Contract gap.** The WebBrowserSession document defines no error body. The center answers a refusal of a JSON route with the ArcError as JSON (`{"error": {category, code, messageKey, retry, effect, correlationId, details}}`) and a page with a fixed text of its code. Routed to the next Contracts window.
- **Dark in production.** The `pages` surface needs `identity`; production enables none (`center.surfaces` `none`, the Worker answers every page path 404 without waking the Container); the acceptance environment enables `identity,pages`. Activation is AF-PROD-01.
- **Evidence.** The real-browser acceptance (Chromium 153 with a virtual authenticator, MOCKED hardware in a real browser) enrolls the owner through the bootstrap, signs in, steps up, registers a second passkey, lists sessions and devices, ends a second browser's session, removes the second passkey and signs out. The AR-23 procedure (a real Windows Hello passkey) is the owner's.

## Public site

| ID | Page | Content | Data |
|---|---|---|---|
| W-01 | `/` Home | The problem and the product in one screen, the three main capabilities, screenshots, Download and Pricing calls to action | Static |
| W-02 | `/features` | Execution and queueing, resource control, caches and storage, records and diagnosis, AI integration, LAN, remote. Each feature states its platforms and honest limits (e.g. "Pause: Linux only"). | Static |
| W-03 | `/pricing` | Free and Pro feature table (product definition §5): everything local and on the LAN is free; Pro is the cloud services. Prices come from the build-time catalogue. While `commerce.sales_open=false` the page shows "Coming soon". | Catalogue snapshot at build time |
| W-04 | `/download` | Per-OS installers (setup program x64/arm64, `install.sh`, `.deb`, winget and Scoop commands), checksum and signature verification instructions, channel selector, AI-client plugin links. Android: Google Play badge. | Release manifest snapshot at build time |
| W-05 | `/docs` | Documentation index: install, first run, CLI, MCP, policies, LAN, troubleshooting | Static |
| W-06 | `/security` | Security model summary, vulnerability disclosure contact, signing keys and fingerprints | Static |
| W-07 | `/privacy`, `/terms`, `/refunds`, `/subprocessors` | Legal texts (supplied by the product owner, H-10) | Static |
| W-08 | `/releases` | Release notes per version and channel, revoked versions | Manifest snapshot |

- **Wireframe** (all public pages share one layout):

```
┌ ArcForges   Features  Pricing  Download  Docs                     [Sign in] ┐
│                                                                             │
│  One authority for every build, test and agent command on your machines.   │
│  [Download for Windows]  [Linux]                See how it works ↓         │
├─────────────────────────────────────────────────────────────────────────────┤
│ footer: Security · Privacy · Terms · Status · Releases                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

- **Accessibility.** The pages use landmark regions (`header`, `nav`, `main`, `footer`), a skip link and a logical heading order. Images have alternative text.

## Account profile

### W-20 Sign in

- **Purpose.** Sign in with a passkey or an e-mail code, create an account, or cancel a pending account deletion.
- **Permissions.** Anonymous. Success creates an `account` cookie session (AF-ID-01). Rate limits apply per IP and per account.
- **Layout.** A centred card: heading; the passkey button; the e-mail code form (e-mail, then code); the create-account link; footer links.
- **Wireframe:**

```
┌ ArcForges ─────────────────────────────────────────────────────────────────────┐
│                           Sign in to ArcForges                                  │
│                     [ Sign in with a passkey ]                                  │
│                     ──────────── or ────────────                                │
│                     E-mail [________________________] [Send code]               │
│                     Code   [__________]  sent to s…@example.com · expires 09:42 │
│                     New to ArcForges? Create an account                         │
│  Privacy · Terms                                                                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** reused `IdentityService.ListAuthProviders` (which methods are offered).
- **Actions:**
  - Passkey: `BeginAuthentication`, the browser WebAuthn prompt, then `CompleteAuthentication`.
  - E-mail code: `RequestEmailCode`, then `RedeemEmailCode`.
  - Create an account: an e-mail code, then `CompleteEnrollment`, then an offer to add a passkey (`BeginPasskeyRegistration`, `CompletePasskeyRegistration`).
  - Pending deletion: "Your account will be deleted on 12 Nov 2026." with **Cancel deletion** (`CancelAccountDeletion`).
  - On success the page returns to the same-origin return URL (for example `/connect` or `/activate`), otherwise to W-21.
- **States:** S-LOADING, S-OFFLINE and S-FAILED; rate limited (with the retry time); code wrong (attempts left) or expired (**Send a new code**); passkey prompt cancelled (the page stays, without an error); no passkey on this device ("Use an e-mail code"); account pending deletion.
- **Accessibility.**
  - Focus starts on the heading, and the passkey button comes first.
  - A polite live region announces "Waiting for your passkey" while the browser prompt is open.
  - The code field uses `autocomplete="one-time-code"`.
  - Errors are announced assertively and linked to their field with `aria-describedby`.

### W-21 Overview

- **Purpose.** See the account, plan and fleet at a glance, with anything that needs attention.
- **Permissions.** Account session.
- **Layout.** The profile navigation; a greeting with plan and renewal; fleet counts; the needs-attention list; **Open Fleet**.
- **Wireframe:**

```
┌ Account ─ Overview · Security · Devices & nodes · Subscription · Support · Privacy ┐
│ Hello Sam ─ Pro (renews 12 Nov)          Nodes: 3 (2 online)   Phones: 1         │
│ Needs attention: payment method expires in 9 days [Update]                       │
│ [Open Fleet ↗]                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `IdentityService.GetProfile`, `StoreBillingService.GetBillingStatus`, `FleetService.ListNodes`.
- **Actions:** each needs-attention item links to its page (W-24 payment, W-22 security, W-23 a revoked or offline node); **Open Fleet** goes to W-40.
- **States:** S-LOADING, S-OFFLINE and S-FAILED; no nodes yet ("Install ArcForges on a computer, then sign in from it", linking to W-04).
- **Accessibility.** The navigation is a landmark with the current page marked `aria-current`. The needs-attention list is a list whose items read as one sentence each.

### W-22 Security

- **Purpose.** Manage passkeys, sessions, recovery codes and the account e-mail, and review security activity.
- **Permissions.** Account session. Removing a passkey, revoking sessions, generating recovery codes and changing the e-mail need a step-up (`BeginStepUp`, `CompleteStepUp`).
- **Layout.** Sections in order: Passkeys, Sessions, Recovery codes, E-mail, Security activity.
- **Wireframe:**

```
┌ Account ─ Overview · Security · Devices & nodes · Subscription · Support · Privacy ┐
│ Passkeys                                                     [Add a passkey]      │
│  Work laptop (Windows Hello)   added 3 Sep   last used today   [Rename] [Remove]  │
│ Sessions (browsers and phones; nodes are under Devices & nodes)                   │
│  Edge on Windows · this session · Berlin                                          │
│  ArcForges for Android · Pixel 9 · 2 h ago                    [Revoke]            │
│                                                   [Sign out all other sessions]   │
│ Recovery codes: generated 3 Sep, 8 of 10 unused               [Generate new codes]│
│ E-mail: s…@example.com                                        [Change]            │
│ Security activity: 12 Oct 10:41 New node "workstation" connected · Berlin         │
└───────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** reused `IdentityService.ListAuthIdentities`, `ListSessions`, `ListSecurityActivity` and `GetProfile`.
- **Actions:**
  - Add a passkey: `BeginPasskeyRegistration`, then `CompletePasskeyRegistration`. Rename: `RenameAuthIdentity`.
  - Remove a passkey: `RemoveAuthIdentity` (step-up). The last sign-in method cannot be removed.
  - Revoke a session: `RevokeSession` (step-up). Sign out all other sessions: `RevokeAllSessions` (step-up). The confirmation names the sessions affected.
  - Generate recovery codes: `GenerateRecoveryCodes` (step-up). The codes are shown once, with **Copy** and **Download**, and the old codes stop working.
  - Change the e-mail: `BeginEmailChange`, then `CompleteEmailChange` with the code sent to the new address (step-up).
- **States:** S-LOADING and S-FAILED; step-up required, cancelled or failed; last-method guard; recovery codes shown once ("These codes will not be shown again").
- **Accessibility.**
  - Tables have column headers, and each action's accessible name includes its item, for example "Remove passkey Work laptop".
  - The recovery codes are in a labelled, focusable region.
  - The step-up dialog keeps focus inside while open and returns it to the triggering button.

### W-23 Devices and nodes

- **Purpose.** See every node, phone and signed-in browser on the account, rename nodes, and revoke anything lost or retired.
- **Permissions.** Account session; step-up for revocation.
- **Layout.** The node table, then phones and browsers.
- **Wireframe:**

```
┌ Devices & nodes ────────────────────────────────────────────────────────────────┐
│ Node        OS       Role   Version  Last seen   Relay   Actions                 │
│ workstation Windows  host   1.2.0    online      ✔       [Rename] [Revoke]       │
│ buildbox    Linux    host   1.1.4    2 h ago     ✔       [Rename] [Revoke]       │
│ Phone Pixel 9 · Android 16 · ArcForges 1.2.0 · last active today      [Revoke]   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `FleetService.ListNodes`; reused `DeviceService.List` for phones and browsers.
- **Actions:**
  - Rename (`FleetService.RenameNode`).
  - Revoke a node (`FleetService.RevokeNode`, step-up). Confirmation: "The node can no longer reach the cloud. Local and LAN work is unaffected. If the machine is lost, also remove or block it on your other machines (LAN pairing is not revoked from here)."
  - Revoke a phone (`DeviceService.Revoke`, step-up).
- **States:** S-LOADING, S-OFFLINE and S-FAILED; S-EMPTY ("No nodes yet"); a node revoked (kept greyed out for 30 days, with the revocation time); plan node limit reached (S-NOT-ENTITLED on the next sign-in).
- **Accessibility.** The table has row headers (node names).

### W-24 Subscription and billing

- **Purpose.** See the plan and its source, start or change a subscription, fix payment problems, and find invoices.
- **Permissions.** Account session; step-up for cancellation. Checkout is closed while `commerce.sales_open=false`.
- **Layout.** The current subscription with its provider; payment and cancellation actions; the Play subscription notice; billing history; plan choice when there is no subscription.
- **Wireframe:**

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
- **Accessibility.** External links (Paddle, Google Play) say that they open another site. Amounts are read with their currency, and the renewal date in full.

### W-25 Support

- **Purpose.** Open and follow support cases, see support bundles uploaded from a node, and decide operator requests to read them.
- **Permissions.** Account session. Case and bundle limits per plan ([14](../architecture/14-commercial-operations.md) §6).
- **Layout.** A banner for pending access requests; the case list (left); the case detail with messages and attached bundles (right); **New case**.
- **Wireframe:**

```
┌ Support ─────────────────────────────────────────────────────────── [New case] ┐
│ ⓘ ArcForges support asks to read bundle "workstation-1012.zip" until 13 Oct     │
│   10:00 for case "Builds stall". [Review request]                              │
├──────────────────────────┬─────────────────────────────────────────────────────┤
│ ● Builds stall    open   │ Builds stall · open · updated 10 min ago            │
│   Billing question closed│ You: dotnet build hangs at restore…                 │
│                          │ Support: Could you upload a bundle?                 │
│                          │ 📎 workstation-1012.zip · 4.1 MB · expires 11 Nov   │
│                          │ [Reply ___________________________________] [Send]  │
└──────────────────────────┴─────────────────────────────────────────────────────┘
```

- **Data:**
  - reused `publicapi.v1.SupportService.ListCases`, whose cases include their messages; implemented by AF-SUP-01.
  - `publicapi.v1.SupportAccessService.ListAccessRequests` and `GetAccessRequest` (new, AF-SUP-01).
  - Bundles appear as messages whose `diagnostic` reference names the uploaded object (name, size, upload date, expiry).

  This is the cloud support service, not the node's `node.v1.SupportService`, which only builds bundles. Bundles are uploaded from the node (Desktop or `arcforges support upload`), never from the browser.
- **Actions:**
  - New case: `CreateCase` (subject, category, message, optional bundle reference).
  - Reply: `AppendMessage`.
  - Review an access request: the dialog shows the purpose, the resources, the access end and the requester. **Allow for 24 h** or **Deny** call reused `SupportService.DecideAccess(access_id, proposal_hash, approve)`. The Allow confirmation: "ArcForges support can read workstation-1012.zip until 13 Oct 10:00. Access ends automatically."
- **States:** S-EMPTY ("No cases yet. Describe the problem, and attach a bundle from your node if you can."), S-LOADING and S-FAILED; case limit reached (`RESOURCE/rate_limited`); case closed (read-only, with **Open a new case**); access request expired or already decided.
- **Accessibility.**
  - The banner is a polite live region.
  - The case list is a listbox whose items name the subject and state.
  - Messages are a list of articles labelled with author and time.
  - The access dialog states the scope in text before its buttons, in the order Deny, Allow.

### W-26 Privacy and data

- **Purpose.** Export the account's data, or delete the account.
- **Permissions.** Account session with step-up for both actions.
- **Layout.** Sections: Export your data; Delete your account; a link to the privacy policy.
- **Wireframe:**

```
┌ Privacy & data ──────────────────────────────────────────────────────────────────┐
│ Export your data                                                                  │
│  Last export: 2 Oct · ready · expires 9 Oct   [Download ↓]   [Request new export] │
│ Delete your account                                                               │
│  Deletion revokes every node, phone and browser, cancels a web subscription immediately    │
│  and erases your data after 30 days. Billing records are kept for 7 years.        │
│  ⚠ You have an active Google Play subscription. Cancel it in Google Play first.   │
│                                                        [Delete my account…]       │
└───────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** reused `DataService.GetExportState`, `IdentityService.GetAccountDeletion`, `CommerceService.GetSubscription`; `StoreBillingService.GetBillingStatus` (Play subscriptions).
- **Actions:**
  - Request an export: `DataService.RequestExport` (step-up). The page polls `GetExportState` every 5 s while it is open, then offers the download until `expires_at`.
  - Delete the account: `RequestAccountDeletion` (step-up). The confirmation lists what is deleted, what is kept and when, and asks for the account e-mail to be typed.
  - An active Play subscription blocks deletion until the user confirms they cancelled it in Google Play ([14](../architecture/14-commercial-operations.md) §3.3).
  - Cancel a pending deletion: `CancelAccountDeletion`.
- **States:** S-LOADING and S-FAILED; export running (progress); export expired; deletion pending (date, with **Cancel deletion**); Play subscription active.
- **Accessibility.** Export progress is a polite live region. The deletion dialog's confirm button stays disabled, with a stated reason, until the e-mail matches.

### W-27 `/connect` (node sign-in consent)

- **Purpose.** Approve or deny a node's sign-in, started by Desktop or `arcforges account login` on that node.
- **Permissions.** Account session; without one, W-20 runs first and returns here. The plan's node limit applies.
- **Layout.** One card: the node's details, what connecting allows, the request time and expiry, then Deny and Connect.
- **Wireframe:**

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

- **Purpose.** Approve a node's sign-in from a browser when the node cannot open one (device-code flow).
- **Permissions.** Account session; without one, W-20 runs first and returns here with the code kept. The plan's node limit applies.
- **Layout.** Three steps on one page: enter the code; check the node; the result.
- **Wireframe:**

```
┌ Activate a node ──────────────────────────────────────────────────────────────────┐
│ Enter the code shown by `arcforges account login --device`                         │
│                    [ K7QD - 9XWM ]   [Continue]                                    │
│ ──────────────────────────────────────────────────────────────────────────────    │
│ "buildbox" · Linux · x64 · ArcForges 1.2.0 wants to connect to s…@example.com      │
│                                               [Deny]  [Approve]                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `NodeEnrollmentService.LookupDeviceCode(user_code)` returns the node details. The QR deep link pre-fills the code.
- **Actions:** **Approve** or **Deny** call `ApproveDeviceCode(user_code, approve)`. The code is 8 characters (`XXXX-XXXX`), case-insensitive, and separators are ignored.
- **States:** invalid code (attempts left); expired ("Start again on the node"); plan node limit (S-NOT-ENTITLED, with the limit); approved ("Return to your terminal"); denied.
- **Accessibility.** The code field has one accessible name, "Activation code", and accepts pasting with or without the separator. The result is announced politely, and the button order is Deny, Approve.

### W-29 Notification preferences

- **Purpose.** Choose which node events reach the user's phones as push notifications.
- **Permissions.** Account session; entitlement `push` (S-NOT-ENTITLED otherwise).
- **Layout.** A grid of event kinds by scope (all nodes, then one column per node), the daily limit, and **Save**.
- **Wireframe:**

```
┌ Notifications ───────────────────────────────────────────────────────────────────┐
│ Event               All nodes   workstation   buildbox                            │
│ Task failed            ☑            ·             ☐ (override)                    │
│ Task finished          ☐            ·             ·                               │
│ Approval needed        ☑            ·             ·                               │
│ Node offline           ☑            ·             ·                               │
│ Finding                ☐            ☑ (override)  ·                               │
│ At most 50 notifications per day (plan limit).                       [Save]       │
└───────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `FleetService.GetPushPreferences`, `ListNodes`.
- **Actions:** toggling marks the page as changed. **Save** calls `UpdatePushPreferences` with the revision read. A per-node cell left at `·` follows the all-nodes value.
- **States:** S-NOT-ENTITLED; no phone registered ("Install ArcForges for Android to receive notifications"); revision conflict (reload, with the user's changes re-applied for review); S-FAILED.
- **Accessibility.** The grid is a table with row and column headers. Each checkbox is named by event and scope, for example "Task failed, buildbox". Override cells say "override" in text, not only by style.

## Fleet profile

### W-40 Fleet overview

- **Purpose.** See every node's live state and open one for detail or control.
- **Permissions.** Account session; entitlement `remote.view`.
- **Layout.** The live indicator; one row per node with counts, load and attention badges.
- **Wireframe:**

```
┌ Fleet ─ live ● ─────────────────────────────────────────────────────────────────┐
│ workstation  online  Running 6 Queued 4  CPU 74% Mem 33% Disk 61% ⚠1 ①1         │
│              Agents 2 (3 subagents)                                              │
│ buildbox     online  Running 2 Queued 0  CPU 40% Mem 20% Disk 12% (low space ⚠)  │
│ laptop       offline last seen 2 h ago                                           │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `FleetService.ListNodes`, then `OpenFleetWatch(SUMMARY)`, then the viewer WebSocket (snapshot plus deltas). `WatchFleet` is the fallback. Each row uses `StatusSummary`: running and queued counts, CPU and memory, findings and approvals, and the active sessions and subagents. **Disk** is the data-root volume's use (`disk_free_bytes`, `disk_total_bytes`); a separate "low space" mark shows when `disk_level` is `LOW` or `CRITICAL` on any volume holding managed roots.
- **Actions:** open a node (W-41). No commands are sent from this page.
- **States:** S-OFFLINE (reconnects with cursors); node offline; viewer limit reached; kill switch active ("Live updates paused; showing summaries").
- **Accessibility.** A polite live region announces state changes only for the focused node, at most every 10 s.

### W-41 Node detail

- **Purpose.** Watch one node in detail and send it remote commands.
- **Permissions.** Account session; `remote.view` to watch and `remote.control` to command. Step-up for medium and high risk. A `mobile.limited` session never reaches this page's commands (web sessions are `account`).
- **Layout.** A header with state, version, pressure and the actions menu; then tasks, approvals, findings and recent commands.
- **Wireframe:**

```
┌ workstation ─ online · 1.2.0 · Pressure Normal ──────────── [Refresh] [⋯ Actions] ┐
│ CPU 74% · Mem 33% · Disk 61% (412 GiB free) · managed storage 38 GiB              │
│ Tasks: dotnet build ● RUNNING 04:12 (build 70%, restore 20%) [Cancel] [Priority]  │
│        npm test ⏸ QUEUED #2 · budget_memory · ETA 3 min                            │
│        cargo test ✖ FAILED exit 101 · EXITED [Tail]                               │
│ Agents: Claude Code · ArcForges-Design · active · 2 subagents · managed 92%       │
│         last event PreToolUse 10:41 · model state: unknown (never reported)       │
│ Approvals: Codex asks: cancel task npm test (medium) [Deny] [Approve]             │
│ Findings: ⚠ STALL dotnet test                                                     │
│ Recent commands: Cancel task npm test — SUCCEEDED 10:44                           │
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** viewer stream with `detail=FULL`; `FleetService.GetNode` (recent commands).
  - Tasks (`TaskSummary`): state, elapsed time, the top timeline categories, queue position, blocking reason and ETA, exit code and termination reason, owner client and session, and the subagent when attribution is known.
  - Agents (`SessionSummary`): client, workspace name, state, active subagents with their types, the last client-reported event, the routing mode and the managed share.
  - Disk from `StatusSummary`.
  - **What the node knows** is shown. **What no client reports** is labelled, not hidden: `unknowns` on sessions (for example "model state (never available)") and `attribution=UNKNOWN` on tasks (for example MCP work of a subagent).
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
- **Accessibility.** Each command button's accessible name includes its task ("Cancel task npm test"). Command progress is a polite live region. Risk levels are text, not only colour.

## Operations profile (operators)

- **Permissions (all pages).** An operator session with step-up (AF-OPS-01) on the profile's own origin. Two-person approval applies where [14](../architecture/14-commercial-operations.md) §1 requires it (`ProposeAction`, `ApproveAction`, `GetProposal`). Every page shows the audit reference of each action.
- **Shared layout.** A left navigation (Cases, Access, Configuration, Entitlements, Refunds, Trust & safety, Budgets, Audit), the page body, and a right panel with the active proposal or access context.
- **Shared states.** S-LOADING, S-OFFLINE and S-FAILED; S-DENIED for a missing operator role; step-up required; a proposal awaiting a second operator.
- **Shared accessibility.** Landmark regions, tables with headers, accessible names that include the subject ("Reply to case Builds stall"), and confirmation dialogs that state the effect, its scope and whether it can be undone.

| ID | Page | API (reused `OperatorService` unless noted) |
|---|---|---|
| W-60 | Cases | `ListCases`, `GetCase`, `ReplyCase`, `SetCaseState` |
| W-61 | Diagnostic access | `RequestAccess`, `ApproveAccess`, `ReadDiagnostic`, `EndAccess` |
| W-62 | Configuration and kill switches | `GetConfiguration`, `StageConfiguration`, `ValidateConfiguration`, `ApproveConfiguration`, `ActivateConfiguration`, `SetKillSwitch` |
| W-63 | Entitlements and compensation | `GrantEntitlement`, `RevokeEntitlement`, `IssueCompensation`, `AdjustCompensation` |
| W-64 | Refunds | `DecideRefund` |
| W-65 | Trust and safety | `ProposeEnforcement`, `DecideEnforcement`, `GetAppeal`, `ResolveAppeal`; anomaly flags through `OperatorReadService.ListAuditEvents` (new) |
| W-66 | Budgets | `OperatorReadService.GetOperatingBudgets`, `GetMonthlyReport` (new); `GetConfiguration`; `SetKillSwitch` |
| W-67 | Break-glass and audit | `StartBreakGlass`, `EndBreakGlass`; `OperatorReadService.ListAuditEvents` (new) |

### W-60 Cases

- **Purpose.** Work the support queue: triage, reply and close cases.
- **Layout.** Filters (state, category, age); the queue table; the case detail with messages and bundle references.
- **Wireframe:**

```
┌ Cases ─ state: open ▾  category: all ▾  older than: any ▾ ───────────────────────┐
│ Subject          Account     Plan  Age    State     │ Builds stall · open        │
│ Builds stall     a1b2c3d4    Pro   2 h    open      │ User: dotnet build hangs…  │
│ Refund request   f9e8d7c6    Pro   1 d    waiting   │ [Reply ____________] [Send]│
│                                                     │ [Set state ▾] [Request access]│
└──────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `ListCases` (filters, paging) and `GetCase`.
- **Actions:** Reply (`ReplyCase`); change state (`SetCaseState`: open, waiting on user, resolved, closed); **Request access** opens W-61 with the case.
- **States:** S-EMPTY ("No open cases"); a case changed by another operator (revision conflict, reload).
- **Accessibility.** The queue is a sortable table; sort changes are announced politely.

### W-61 Diagnostic access

- **Purpose.** Ask a user for time-boxed access to a support bundle, and read it under audit once allowed.
- **Layout.** The request form (case, resources, reason, end time); the list of requests with state; the reader for allowed bundles.
- **Wireframe:**

```
┌ Diagnostic access ───────────────────────────────────────────────────────────────┐
│ New request: case [Builds stall ▾]  bundle [workstation-1012.zip ▾]               │
│              reason [read logs for the stall_____]  until [+24 h ▾]  [Request]    │
│ Requests:  workstation-1012.zip · pending user decision · requested 10:02         │
│            buildbox-0930.zip   · allowed until 13 Oct 10:00  [Open] [End access]  │
└───────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `GetCase` (the case's bundles); the access state from `RequestAccess` and `ReadDiagnostic` responses.
- **Actions:** `RequestAccess` (at most 24 h); `ApproveAccess` (second operator, where two-person approval applies); `ReadDiagnostic` (audited per read); `EndAccess`. The user decides in W-25.
- **States:** pending user decision; denied; expired; ended.
- **Accessibility.** The reader announces the remaining access time politely once a minute during the last 10 minutes.

### W-62 Configuration and kill switches

- **Purpose.** Change limits, the plan catalogue and kill switches through staged, validated and approved configuration revisions.
- **Layout.** The current revision; a staged draft with a diff; the validation result; approval and activation; the kill-switch panel.
- **Wireframe:**

```
┌ Configuration ─ active r41 ───────────────────────────────────────────────────────┐
│ Draft r42 (staged by you)                                                          │
│  - relay.viewer_limit: 3 → 5                                                       │
│  Validation: ✔ valid       Approval: waiting for a second operator                 │
│                                         [Validate] [Request approval] [Activate]   │
│ Kill switches: live streaming ON · push ON · new relay connections ON · uploads ON │
│                [Turn off live streaming…]                                          │
└────────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `GetConfiguration`.
- **Actions:** `StageConfiguration`, `ValidateConfiguration`, `ApproveConfiguration` (second operator), `ActivateConfiguration`; `SetKillSwitch` (mode, scope, reason, until). The kill-switch confirmation states the user-visible effect, for example "Live views fall back to summaries for every account."
- **States:** validation failed (issues listed by path); approval pending; activation conflict (another revision activated first).
- **Accessibility.** The diff is a table (key, old, new), so changes are not shown by colour alone.

### W-63 Entitlements and compensation

- **Purpose.** Grant or revoke entitlements, and issue goodwill extensions.
- **Layout.** Account lookup by ID; current entitlements; grant and compensation forms; the history.
- **Wireframe:**

```
┌ Entitlements ─ account a1b2c3d4 ──────────────────────────────────────────────────┐
│ Snapshot: pro (Paddle, renews 12 Nov) · remote.* push                              │
│ Grants:   compensation +14 days (issued 2 Oct, case Billing question)  [Adjust]    │
│ [Grant entitlement…]  [Revoke…]  [Issue compensation…]                            │
└────────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** the entitlement snapshot in the responses of these methods; the history from `OperatorReadService.ListAuditEvents` filtered by the account.
- **Actions:** `GrantEntitlement`, `RevokeEntitlement` (two-person), `IssueCompensation`, `AdjustCompensation`. Each requires a case or a reason.
- **States:** two-person proposal pending; the account has no subscription.
- **Accessibility.** Forms name every field, and the effect summary is read before the confirm button.

### W-64 Refunds

- **Purpose.** Decide Paddle refund requests. Play refunds are issued in Google Play Console by the product owner.
- **Layout.** The refund request list; the request detail (transaction, amount, reason, the case); the decision form.
- **Wireframe:**

```
┌ Refunds ──────────────────────────────────────────────────────────────────────────┐
│ Request          Account    Amount     Requested   State                            │
│ Pro annual 2026  f9e8d7c6   €96.00     1 d ago     pending   [Decide…]              │
│ Play purchases: refunds are issued in Google Play Console ↗                        │
└────────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** pending refunds from the cases and commerce records of `GetCase`.
- **Actions:** `DecideRefund` (approve full or partial, or deny, with a reason; two-person for approval).
- **States:** already refunded at Paddle (shown as reconciled); proposal pending.
- **Accessibility.** Amounts are read with their currency.

### W-65 Trust and safety

- **Purpose.** Review anomaly flags, propose and decide enforcement, and resolve appeals. Flags never lock an account automatically ([14](../architecture/14-commercial-operations.md) §6).
- **Layout.** The anomaly flag list; the enforcement proposal form; appeals.
- **Wireframe:**

```
┌ Trust & safety ───────────────────────────────────────────────────────────────────┐
│ Flags (audit events anomaly.*):  12 Oct 09:10  relay viewer flood  a1b2c3d4 [Review]│
│ Proposals: limit remote control for a1b2c3d4 (7 days) · waiting for decision       │
│ Appeals:   f9e8d7c6 · submitted 11 Oct · [Open]                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** anomaly flags are audit events of type `anomaly.*`, read through `OperatorReadService.ListAuditEvents`; `GetAppeal`.
- **Actions:** `ProposeEnforcement`, `DecideEnforcement` (second operator), `ResolveAppeal`.
- **States:** no flags (S-EMPTY); proposal pending; appeal resolved.
- **Accessibility.** Each flag's accessible name includes its kind, account and time.

### W-66 Budgets

- **Purpose.** Watch daily cloud cost budgets for every billable dimension, their thresholds, the degradation ladder and kill-switch state, the residual exposure, and the monthly unit-economics report ([14](../architecture/14-commercial-operations.md) §7).
- **Layout.** Today's budgets by dimension (bars plus a table); the kill-switch state; the monthly report.
- **Wireframe:**

```
┌ Budgets ─ 12 Oct 2026 (UTC) ─ ◀ day ▶ ────────────────────────────────────────────┐
│ Dimension            Used / ceiling          %     State                           │
│ Container CPU-s      41,200 / 60,000         69    normal                          │
│ DO requests          1.9 M / 2.0 M           95    ⚠ alert                         │
│ D1 rows read         3.1 M / 10 M            31    normal                          │
│ Push sends           880 / 5,000             18    normal                          │
│ Container instance-s 61,000 / 86,400        71    normal (worst case 2 × basic)     │
│ DO duration GB-s     9,800 / 40,000 (est.)  25    normal                          │
│ Ladder: step 0 · essential-only: off · Residual worst case: $1.10/day             │
│ Kill switches: all on                                    [Change in Configuration] │
│ October (partial, 12 days): est. $41.20 of $150 ceiling · $0.37 per Pro account     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `OperatorReadService.GetOperatingBudgets(day)` (budgets with `estimated` flags, `residual`, `essential_only`, `reconciliation`) and `GetMonthlyReport(month)` (new, AF-OPS-01); `GetConfiguration` (kill switches, unit prices, monthly ceiling).
- **Actions:** move the day or month; **Change in Configuration** opens W-62 (kill switches change only there).
- **States:** no budgets configured (S-EMPTY, with a link to W-62); a dimension at alert or exhausted (the ladder step and the triggered kill switches are named); essential-only mode active (banner); reconciliation off (no H-21 token) or diverging by more than 20%; partial month.
- **Accessibility.** Bars have the same values in the table. Threshold states are text plus an icon.

### W-67 Break-glass and audit

- **Purpose.** Start and end break-glass access, and search the audit trail.
- **Layout.** The break-glass panel; audit filters; the audit table with chain verification.
- **Wireframe:**

```
┌ Audit ─ last 24 h ▾  type: [config.____]  actor: [________]  [Search] ─────────────┐
│ ✔ chain verified for this page                                                     │
│ 12 Oct 10:44  operator:o1  config.activate  r42  reason: viewer limit              │
│ 12 Oct 10:02  operator:o1  support.access.request  case Builds stall               │
│ Break-glass: inactive                                   [Start break-glass…]       │
└────────────────────────────────────────────────────────────────────────────────────┘
```

- **Data:** `OperatorReadService.ListAuditEvents` (new): filters, paging, and `chain_verified`.
- **Actions:** `StartBreakGlass` (reason, scope, at most 1 h; two-person where available, otherwise a recorded self-approval) and `EndBreakGlass`.
- **States:** chain verification failed (an alert banner that names the first event that failed); break-glass active (a persistent banner on every operations page with the remaining time).
- **Accessibility.** The break-glass banner is a polite live region, and its countdown is announced at 10 minutes and 1 minute.
