# Blazor management Dashboard

Status: V2 target design; no Dashboard is implemented at the audited Web baseline. Owners: `AFV2-WEB-01` through `AFV2-WEB-04`. This is a browser management product, not a desktop client or GUI-application sandbox. `AFV2-HOST-03` supplies deployment infrastructure; `AFV2-DIST-01` assembles the complete qualified Dashboard with Go/PostgreSQL after final consumer cutover.

## 1. Implementation choice and reusable assets

Use the existing `ArcForges.Web.App` Blazor WebAssembly application and `ArcForges.Web.Ui` Razor class library. Retain the static Site generator, profile bundle/budget tooling, exact Contracts packages and Cloudflare static-asset adapter. Go remains the only product API server. Do not introduce Blazor Server circuits, an ASP.NET BFF or a second identity/authorization store.

The present Account page is a session probe, Chat is a Hello probe, and Operations is a skeleton. They prove useful transport, focus-management and build patterns; they are not finished account, chat, billing or device-management features. Replace the App's probe pages with the Dashboard. Keep Operations as a separate operator-origin surface only to the extent required for the basic hosting controls in [Identity and commerce](11-identity-commerce.md); do not make an operator a default remote device administrator.

The Dashboard is distributable with a self-hosted Center. Its same-origin API base and configured Center identity come from a public deployment configuration, containing no private credentials. The official hosting mode may show subscription status; self-hosted mode shows operator-supplied limits and never redirects the user to official checkout. A Center switch is an explicit origin change, not a client-controlled URL injected into arbitrary fetches.

## 2. Visual system and responsive structure

The visual target is a calm operations workspace with clear hierarchy, compact but readable data tables, generous spacing around primary actions, and consistent terminology. Use semantic tokens for surfaces, typography, spacing, borders, focus and status. Provide light/dark themes, system preference, reduced motion and responsive layouts. Charts supplement exact numbers, timestamps and labels rather than replacing them.

| Width/context | Layout |
|---|---|
| Wide desktop | Fixed navigation rail, bounded content width, two-column detail when useful, sticky page-level action bar |
| Medium/tablet | Collapsible navigation; detail and charts stack before tables become unreadable |
| Narrow phone browser | Drawer navigation, single-column cards, key columns prioritized, full detail accessible through each row |
| Keyboard/screen reader | Skip link; semantic headings; table headers; visible focus; dialog focus trap/return; live regions for action result only |

Never encode state by color alone. Use a short state label, icon and explanation. Core Run states `Starting`, `Running`, `Stopping`, `Draining descendants`, `Exited`, `Failed` and `Recovery required` are distinct from transport/view states `Unknown`, `Offline`, `Stale`, `Unsupported`, `Unverified` and `Access denied`. A missing CPU/memory measurement renders “Unavailable” with its reason. A disconnected Node's last known Running badge is labeled “Last reported running” with its observation time.

`Draining descendants` means the root/executor exited and Core is still verifying that the managed group is empty. Show the provenance of raw executor exit status and the workload outcome, which can remain unknown. A long-running service requires its foreground root to remain alive. Show network limitations from the Node capability report. An unverified optional mode carries its evidence status and actual request result, while an unsupported mode shows the Node's refusal reason.

Critical actions remain in stable positions during requests. Prevent double submission without dropping keyboard focus. A destructive confirmation includes the exact device and Sandbox name plus data consequence; the primary action does not move during async validation. Escape closes a cancellable dialog but never silently cancels an admitted remote operation.

## 3. Navigation and page contracts

Navigation: Overview, Devices, Sandboxes, Resources, Runs, Security, Account. Subscription appears within Account in official-hosted mode. Context is always visible: Center origin/name, device name and its online state; detail pages additionally show Sandbox/Run identity. No screen suggests that viewing an offline node constitutes a live read.

| Page/route | Data and API interaction | Actions | Required non-happy states |
|---|---|---|---|
| `/overview` | Device registry summary; bounded live Sandbox/Run counts and resource summaries for selected online devices | Open device, resume selected view, enroll device | Empty account; all offline; partial refresh; stale summaries; hosted entitlement unavailable |
| `/devices` | `management.v2` device/enrollment list; last seen, OS/arch, version, capability status, remote grant summary | Enroll instructions, inspect, revoke enrollment | Never connected; needs sign-in; old protocol; revoked; no subscription; local remote access disabled |
| `/devices/{node}` | Registry detail plus Node health and currently allowed actions; epoch/freshness shown | Open Sandboxes/Resources/Runs; show local re-enrollment instructions; revoke | Node unavailable, capability mismatch, policy denies, unknown live state |
| `/devices/{node}/sandboxes` | Authorized grant selection, with zero or one Sandbox per scoped `SandboxService.List` response and no further page | Select an authorized Sandbox, inspect, create from a permitted template | No visible Sandbox, permission denied, unsupported backend profile |
| `/devices/{node}/sandboxes/{sandbox}` | Redacted configuration, permissions, granted resource observations, Run summaries and audit-safe operation status | Start an admitted Run, submit a complete authorized configuration, import/export owned regular files, show owner-local rename, usage and deletion guidance | Revision conflict, incomplete policy, path/permission refusal, retained export, deletion recovery pending |
| `/devices/{node}/resources` | `ResourceService` budgets and measurements for a granted Sandbox or its Runs | Inspect effective limits and, when the complete authorized policy is available, submit a revision-bound replacement | Scope unavailable, missing or stale sample, unverified or partially applied limit |
| `/devices/{node}/runs` | Runs for the granted Sandbox, with the returned page cursor when present and reported start/end, state, exit/signal and elapsed time | Filter, inspect, stop an allowed active Run | Unknown outcome, disconnected Node, output expired, stopped during refresh |
| `/devices/{node}/runs/{run}` | Run detail, safe redacted command display, bound configuration/profile revisions, bounded logs, resource samples, operation reconciliation | Stop, copy safe IDs, download allowed log range, reconcile pending operation | Output gap; transport interruption; permission revoked; lost output epoch; no exit status yet |
| `/security` | Own session and device summaries, admitted passkey metadata and the selected grant's redacted summary | Revoke authorized sessions, devices or the selected remote grant. Open the Center's passkey/session pages or show local grant instructions. | Reauthentication required, stale policy, access lost, unsupported operation |
| `/account` | Account profile, Center mode, current session and account deletion status when available | Update admitted profile fields, sign out, and open the Center's recovery and account lifecycle pages | Anonymous, expired/revoked session, mail unavailable, restricted account, proof or export expired, deletion pending |
| `/account/subscription` | Official-mode catalog, purchase and subscription state, entitlement snapshot and bounded billing history | Open an admitted checkout, change renewal, read the original purchase or current subscription after an uncertain response | Sales closed, pending or unknown purchase, grace/expired, cancellation scheduled, provider unavailable |

The table is an implementation map, not evidence these routes exist. Exact wire methods are generated from [Contracts](../contracts/README.md). Browser code consumes typed clients with a closed route map; reflection, runtime method registries and arbitrary string dispatch are not permitted.

## 4. Shared view state and freshness

Every data region has explicit `initial-loading`, `ready`, `empty`, `refreshing-with-old-data`, `stale`, `unavailable`, `forbidden` and `incompatible` states. Initial loading uses appropriately sized placeholders. Refresh preserves readable data and its original timestamp. Failure never turns previously observed data into a new success or resets it to zero.

Use the server-defined order and opaque cursors on routes that provide them. A new filter cancels the prior read and resets its cursor. A grant-scoped Sandbox list starts with an empty cursor and has no next page. Route selection binds IDs to the current account, Center, device and grant. Ignore late responses from an earlier selection or enrollment. [Node scoped list](https://github.com/ArcForges/ArcForges/blob/237e5cccbbdc8d01eff4579b29d2882214cbdad9/src/ArcForges.Node.Core/Security/SandboxCenterCalls.cs)

Updates are demand-driven. An active visible overview requests summaries; Run detail requests that Run's output/samples. Hidden tabs suspend long polls after their current bounded request and refresh on return. Use one coalesced refresh per target, bounded cancellation-aware backoff, and at most the negotiated concurrency. Reconnect obtains an epoch snapshot before applying new deltas. An epoch mismatch discards buffered deltas and renders a resynchronization indication.

View models preserve integer counters, revisions and byte offsets as exact values; do not convert 64-bit IDs/offsets through JavaScript floating-point numbers. Format user-visible time in the selected locale/time zone while preserving an unambiguous UTC value for copying and audit detail. Server sequence/revision, not wall-clock sorting alone, resolves update order.

For durable mutations, bind the owner epoch and original command ID to the same Center, device, enrollment and grant. Device presence `node_epoch`, event and sample epochs, and channel epochs describe their own scopes. Current device routes expose presence `node_epoch`, and the closed Center allowlist has no browser `Handshake` route. For a new browser intent, obtain the current owner epoch from an authorized typed source when available. The local owner can copy `handshake.ownerEpoch` from `arcforges --json node status` on the selected device. If the owner epoch is unavailable, leave the mutation unavailable and explain the local action. For reconciliation, use the original command ID and owner epoch from its receipt or owner-local command metadata. A new observation never replaces that original epoch. [Center device presence](https://github.com/ArcForges/Cloud/blob/9b8796eac760982d9814f371b820b736ddd945c4/center/internal/fleetapi/management_devices.go), [Node status](https://github.com/ArcForges/ArcForges/blob/237e5cccbbdc8d01eff4579b29d2882214cbdad9/src/ArcForges.CommandLine/V2NodeCommands.cs)

## 5. Principal user flows

### 5.1 First connection

The device page explains `arcforges center connect <configured-center>` and directs the user to the existing Center consent/device-code flow. Show the requesting device fingerprint/name before approving. Enrollment and local permission are separate: after sign-in the page shows which remote grants are enabled and the precise local CLI command to grant view/control. The browser cannot silently grant itself a broader host permission.

The self-hosted flow stays on the user's configured Center and has no official subscription check. Official mode explains when a hosted subscription is required for node connectivity. Signing in, managing account security and revoking a device still work when connectivity is not entitled.

### 5.2 Create/configure a Sandbox

Creation first selects an existing locally issued provisioning grant and its immutable template revision. If none is available, the page explains the required local grant action and disables remote creation. The form collects display name and settings that can be explicitly and safely requested within that template. It displays backend capability reasons before submission and offers mount choices only through available authorized descriptors. A redacted template displays only disclosed values. When those values are insufficient for the intended complete request, direct the owner to the local CLI.

Create sends `provision_grant_id`, template revision and the complete requested configuration. Core verifies exact or narrowed authority and creates the bounded child Sandbox grant atomically with the Sandbox. Template revision conflicts require local review or selection of the current allowed template; the browser cannot widen or mint a provisioning grant. Configuring an existing Sandbox instead uses its Sandbox-scoped grant and preserves that grant's limits.

Submit includes a fresh command identity, the current owner epoch and the exact expected revision for updates. After a conflict, display the server's current revision and let the user review changed values. `SandboxService.Configure` replaces the complete configuration. Remote Inspect omits host grants, environment and the default work directory, so building Configure by cloning it can discard policy. Expose Configure only for an explicitly reviewed, complete, grant-bounded replacement supported by the selected profile. For a name-only edit or an incomplete policy, show `arcforges sandbox rename <id> <name> --expected-revision <n>` or the applicable owner-local configuration command. Local rename uses the unchanged complete configuration and keeps the Sandbox ID and owned root. DeviceService exposes List, Inspect and Revoke. [Node Sandbox redaction](https://github.com/ArcForges/ArcForges/blob/237e5cccbbdc8d01eff4579b29d2882214cbdad9/src/ArcForges.Node.Core/Security/SandboxRemoteProvision.cs), [Local command mapping](06-local-node-cli.md#4-command-surface)

### 5.3 Start and stop

Run launch uses an existing authorized Sandbox, an executable and exact argument array, and a permitted relative working directory. Keep launch inputs within the local grant and admitted profile. Preserve argument boundaries and use an explicit shell only when the user names it as the program. The remote Start request cannot supply secret references. Any supported unsealed environment input stays out of URL parameters, analytics, browser persistent storage and ordinary audit rows. The browser offers admitted Start and Stop controls and bounded output reads. Terminal input and other live terminal controls remain local.

After admission, retain the command ID until its result is known. Show `Starting`, a Run ID when available, and the exact operation state. A timeout shows “The result is not yet known” and offers a read-only reconciliation action. It does not offer an automatic new Start button that would duplicate an uncertain Run.

Reconciliation retains the original owner epoch. Reload, reconnect, receipt-body compaction or a new Handshake cannot silently rebind a saved command to a different store epoch. Render a compacted receipt or retired epoch explicitly; neither condition automatically creates another Start. Safe command display and the bound config/profile revisions come from the typed Run result, not reconstruction from a secret-bearing launch form.

Stop shows the selected Run and the Core's graceful-stop/escalation policy. Navigation away never stops a Run. A stop response reports whether the tree was confirmed exited or remains uncertain; the UI does not infer success merely because the node disconnected.

### 5.4 Resource readings and policy edits

`ResourceService.GetBudget` and `WatchUsage` read the Sandbox named by the selected grant or a Run belonging to it. Keep host-wide Node readings and reserve changes in the local CLI. Display only returned measurements, with units, observation time, pressure and requested, applied and read-back limit states when supplied. A missing observation stays unavailable. Reconnect starts a fresh `WatchUsage` series and explicitly shows gaps in observation.

`SetPolicy` replaces the policy at its exact `policy_revision`. Allow only fields accepted for the target scope and within the local grant. A Run cap omitted from a replacement can restore its launch cap. Keep Run resource controls read-only until both the complete authorized overlay and its current revision are available. Use owner-local `arcforges resources show` and `resources set` when necessary. A saved policy and verified native application are separate states. [Node remote resource scopes](https://github.com/ArcForges/ArcForges/blob/237e5cccbbdc8d01eff4579b29d2882214cbdad9/src/ArcForges.Node.Core/Security/SandboxCenterCalls.cs), [Node resource policy replacement](https://github.com/ArcForges/ArcForges/blob/237e5cccbbdc8d01eff4579b29d2882214cbdad9/src/ArcForges.Node.Core/Resources/SandboxManager.ResourcePolicy.cs)

### 5.5 Files and owner-local deletion

Each import/export transfer contains one regular file and bounded chunks under a Sandbox-relative path. Multiple selection creates separate transfers with individual progress and outcome; it does not promise an atomic directory snapshot. Show bytes transferred, cancellation and conflict state. No archive is implicitly expanded, no symlink/junction target is followed, and no remote host search/editor is introduced. Validate each destination path and final commit on the Node; browser validation only provides early feedback. Interrupted transfers are not reported as complete or silently applied to a later file revision.

Use the authorized `DataService.InspectTransfer` read for asynchronous progress, final manifest digest and `closed_at`. Do not repeat `BeginExport` to discover whether preparation finished. `COMPLETE` means the immutable export was materialized and verified; source Runs may resume, while the private snapshot remains readable until explicit `CloseTransfer` or expiry. A lost final read can request the same range again during that lifetime. Receiving the last byte does not release the snapshot or make Sandbox deletion safe; the UI shows retained versus released/expired state separately.

In the browser, byte counts describe the individual transfer. Read owned-data usage on the selected Node with `arcforges --json sandbox usage <id>`. The Center transfers regular files without offering `DataService.GetUsage` or `ListEntries`. [Center route allowlist](https://github.com/ArcForges/Cloud/blob/9b8796eac760982d9814f371b820b736ddd945c4/center/internal/routes/management.go), [Node usage command](https://github.com/ArcForges/ArcForges/blob/237e5cccbbdc8d01eff4579b29d2882214cbdad9/src/ArcForges.CommandLine/DataCommands.cs)

The closed Center allowlist excludes `SandboxService.PlanDelete` and `Delete`. The Dashboard identifies the selected Sandbox and directs the owner to `arcforges --json sandbox delete <id> --plan-only` on its Node. The real local preview shows its revision, owned-size estimate when available, excluded host grants, managed-use blockers and expiry. Visible Runs and transfer observations may explain known blockers. The owner uses the local CLI to confirm, execute or resume Delete, and Core revalidates the safeguards when accepting the request. A missing size estimate remains unavailable. [Local deletion workflow](05-filesystem-data.md#7-safe-whole-sandbox-deletion)

### 5.6 Security, account lifecycle and subscription

Read own sessions and passkey metadata through the admitted PublicApi v1 identity methods or the Center's existing account pages. Device management uses V2 List/Inspect/Revoke. Retrieve a remote grant summary using the selected live Node, enrollment, grant and grant revision. Revocation uses the appropriate typed method with its exact target, command identity, revision and step-up evidence when required. Node grant revocation also requires the Node owner epoch described above. The current routes provide neither a general security activity feed nor public enrollment-key listings. To create a grant, the owner runs `arcforges grant set --file <policy>` on the Node. To replace an existing grant, include its `grantId` in the JSON and run `arcforges grant set --file <policy> --expected-revision <current>`. [Center identity methods](https://github.com/ArcForges/Cloud/blob/9b8796eac760982d9814f371b820b736ddd945c4/center/internal/routes/identity.go), [Node grant scope](https://github.com/ArcForges/ArcForges/blob/237e5cccbbdc8d01eff4579b29d2882214cbdad9/src/ArcForges.Node.Core/Security/SandboxRemoteGrants.cs), [CLI grant command](https://github.com/ArcForges/ArcForges/blob/237e5cccbbdc8d01eff4579b29d2882214cbdad9/src/ArcForges.CommandLine/SandboxGrantCommands.cs#L23-L47)

Use the existing same-origin Center pages reached through the configured `/api` proxy for the human ceremonies. The fixed paths are `/api/account/recovery`, `/api/account/lifecycle`, `/api/account/passkeys` and `/api/account/sessions`. They keep proof, cookie/session handling, expiring export and account deletion within the already admitted Center boundary. The Dashboard may read typed deletion status and explain pending, blocked, expired and renewed-sign-in states. A pending operation is not a purge promise. Preserve the operation or original command identity during reconciliation. [Center browser routes](https://github.com/ArcForges/Cloud/blob/9b8796eac760982d9814f371b820b736ddd945c4/center/internal/routes/pages.go), [Account lifecycle rules](11-identity-commerce.md#21-minimal-account-lifecycle)

In official mode, read the actual catalog and price version for the selected region before offering purchase. Keep the original purchase, checkout and command identities through uncertainty and use `GetPurchaseState` after checkout or loss of a reply. Only a current server response can establish payment and entitlement state. Cancel or reactivate using the current subscription revision and the proof required by the exact operation. A billing portal may be offered when the existing same-origin, subscription-bound route is available. In self-host mode, omit purchase controls and explain operator-configured limits using available facts. [Center commerce routes](https://github.com/ArcForges/Cloud/blob/9b8796eac760982d9814f371b820b736ddd945c4/center/internal/routes/commerce.go), [Subscription and purchase state](11-identity-commerce.md#6-subscription-and-purchase-state)

## 6. Authentication, browser security and accessible errors

Reuse strict same-origin session bootstrap, `SameOrigin` credentials, no-store responses, explicit CSRF and non-followed script redirects. Use the Center's existing passkey/email-code pages for sign-in/step-up. The UI holds CSRF only as needed; it never copies a Node token, refresh token, private key or operator credential into a bundle or local storage. A fully signed-out transition cancels subscriptions, clears account/target caches and erases unsent sensitive forms.

Render output, arguments, names and error detail as escaped text. The ordinary log view does not execute ANSI control streams or embedded links. Clipboard/download actions are explicit; output may contain application secrets, so exports require the same `logs` grant and have no default third-party upload. Content-security headers and origin policy remain part of the existing static/profile build.

Map errors to actionable text without exposing another account's objects: offline → wait/reconnect; grant denied → explain required local authority; unsupported combination → display OS/backend restriction; revision conflict → reload/review; uncertainty → query original command; subscription unavailable → keep essential account/security routes and show service state. Include a copyable correlation ID without dumping stack traces.

Target WCAG 2.2 AA for the delivered screens and verify keyboard operation, focus preservation, labels, contrast, reduced motion, responsive reflow and announcements. Graphs include a readable recent-sample table and current numerical summary. These are product acceptance criteria; accessibility conformance is not claimed until the screen checks run.

## 7. Scope exclusions

No desktop client, Android/iOS application, AI chat panel, MCP configuration, task DAG editor, cache analytics, toolchain registry, LAN placement, browser terminal, GUI sandbox or plugin marketplace is delivered. Existing unrelated Chat profile code can be removed from the ArcForges V2 bundle and build composition; shared public contract artifacts consumed by independent products stay resolvable.

## 8. Task and acceptance boundaries

| Owner | Concrete delivery and verification |
|---|---|
| `AFV2-WEB-01` | Replace probe navigation with responsive shell; account/session handling; device enrollment and Overview. Verify same-origin no-secret bundle, empty/offline/stale states, stable keyboard focus, account switch/cancellation, self-host configuration. |
| `AFV2-WEB-02` | Sandbox, Run, resource and regular-file transfer screens wired to the shipped typed APIs, with owner-local guidance where required. Verify deterministic control, error and reconciliation behavior using component and transport fixtures. |
| `AFV2-WEB-03` | Security, account and subscription views built on the admitted typed routes and existing Center ceremonies. Replace obsolete probe/account composition and verify the production route, view and failure behavior with deterministic component and transport fixtures. |
| `AFV2-WEB-04` | Qualify responsive layout, accessibility and keyboard/focus in explicit local browser checks. Exercise view states, offline/reconnect, stale and slow streams, and presentation of uncertain operations without duplicate requests. Record this browser evidence against real Center/PostgreSQL and both native Node profiles. |
| `AFV2-ACC-02` | Verify integrated control and account journeys and their real effects across the Dashboard, Center/PostgreSQL and both native Node profiles. |

The owner's 2026-11-21 instruction stages WEB-02 with component and transport tests and defers its live end-to-end run. Exercise the production typed client and state transitions with deterministic typed responses or controlled transport failures. Cover grant- and revision-bound requests, exact command and owner epoch, accepted versus uncertain effects, read-only reconciliation, stale and out-of-order responses, offline and access loss, bounded output and gaps, missing samples, retained export, and local-only actions sending no remote mutation. Fixtures remain test-only and establish component behavior. The integrated effect evidence belongs to ACC-02. Record unrun live cases as unverified. Public activation still requires actual provider, domain and business qualification.

Apply the owner's mock-first staging to WEB-03 development. Exercise the shipped request encodings, same-origin page handoffs and typed response handling with deterministic account/session, proof-expiry, grant conflict/revocation, pending deletion, export refusal, sales-closed, pending purchase, reconciliation, provider-unavailable and self-host cases. Cover cancellation and late responses after account or target changes, stale revisions, and preservation of command identities across uncertain writes. Keep fixtures in tests. ID-01 and HOST-02 retain their genuine server-side evidence. WEB-04 retains browser accessibility and reconnect checks, and ACC-02 owns the integrated effects. A component result leaves an unrun integrated case unverified.

Keep the current platform-native build, unit, static, bundle-budget, provenance and locked dependency gates. Previously recorded native and live evidence retains its original scope.

When the full trimmed Dashboard exceeds the earlier probe measurements, WEB-01 records a separately reviewed baseline from the exact current application and pinned release toolchain. Use the existing profile budget validator and 10% regression policy. Preserve the historical Account/Chat baseline, proof readers, static-origin limits and the ceilings the current publish already meets. Record all initial resource and total byte metrics from the designated native build. Complete self-host distribution and its Dashboard route admission remain with DIST-01.

Source evidence: [Cloud/Web/Contracts audit](../research/cloud-audit.md).
