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

Never encode state by color alone. Use a short state label, icon and explanation. Core Run states `Starting`, `Running`, `Stopping`, `Draining descendants`, `Exited`, `Failed` and `Recovery required` are distinct from transport/view states `Unknown`, `Offline`, `Stale`, `Unsupported`, `Unproven combination` and `Access denied`. A missing CPU/memory measurement renders “Unavailable” with its reason, not zero. A disconnected Node's last known Running badge is labeled “Last reported running” with its observation time.

`Draining descendants` means the root/executor exited but Core has not yet verified the managed group empty. Show raw executor exit status with its provenance separately from the workload outcome, which can remain unknown. A long-running service requires its foreground root to remain alive and does not imply public/host ingress is supported. Capability explanations come from the complete admitted profile; neither a subscription purchase nor a browser setting makes an unsupported/unproven combination safe.

Critical actions remain in stable positions during requests. Prevent double submission without dropping keyboard focus. A destructive confirmation includes the exact device and Sandbox name plus data consequence; the primary action does not move during async validation. Escape closes a cancellable dialog but never silently cancels an admitted remote operation.

## 3. Navigation and page contracts

Navigation: Overview, Devices, Sandboxes, Resources, Runs, Security, Account. Subscription appears within Account in official-hosted mode. Context is always visible: Center origin/name, device name and its online state; detail pages additionally show Sandbox/Run identity. No screen suggests that viewing an offline node constitutes a live read.

| Page/route | Data and API interaction | Actions | Required non-happy states |
|---|---|---|---|
| `/overview` | Device registry summary; bounded live Sandbox/Run counts and resource summaries for selected online devices | Open device, resume selected view, enroll device | Empty account; all offline; partial refresh; stale summaries; hosted entitlement unavailable |
| `/devices` | `management.v2` device/enrollment list; last seen, OS/arch, version, capability status, remote grant summary | Enroll instructions, inspect, revoke enrollment | Never connected; needs sign-in; old protocol; revoked; no subscription; local remote access disabled |
| `/devices/{node}` | Registry detail plus Node health and currently allowed actions; epoch/freshness shown | Open Sandboxes/Resources/Runs; show local re-enrollment instructions; revoke | Node unavailable, capability mismatch, policy denies, unknown live state |
| `/devices/{node}/sandboxes` | Paged `SandboxService` list; state, active-run count, usage, configuration revision | Create from permitted options, filter, inspect | No Sandboxes; permission denied; incomplete usage; unsupported backend profile |
| `/devices/{node}/sandboxes/{sandbox}` | Core configuration, permissions, resources, usage, Run summaries and audit-safe operation status | Start Run; configure including display-name rename within local grant; import/export owned regular files; plan/delete Sandbox | Revision conflict; active-run deletion refusal; path/permission refusal; partial resource application; deletion recovery pending |
| `/devices/{node}/resources` | `ResourceService` host reserve, policy budget, pressure and per-Sandbox/Run measurements | Change permitted budget/priority within local ceiling; inspect effective limit | Sampling unavailable; unverified backend limit; pressure intervention; stale data; partially applied update |
| `/devices/{node}/runs` | Paged Runs with Sandbox, executable display name, start/end, state, exit/signal and elapsed time | Filter, inspect, stop an allowed active Run | Unknown outcome, disconnected Node, output expired, stopped during refresh |
| `/devices/{node}/runs/{run}` | Run detail, safe redacted command display, bound configuration/profile revisions, bounded logs, resource samples, operation reconciliation | Stop, copy safe IDs, download allowed log range, reconcile pending operation | Output gap; transport interruption; permission revoked; lost output epoch; no exit status yet |
| `/security` | Own sessions/devices, enrollment keys' public metadata, remote-grant summary and security activity | Revoke sessions/devices/grants; display local grant-edit instructions; open step-up/remediation flow | Reauthentication required; stale policy; forbidden expansion; lost device |
| `/account` | Account profile, Center mode, current session and essential security links | Profile update, sign out, bounded recovery, account export and prepare/confirm deletion through `AFV2-ID-01` | Anonymous, expired/revoked session, mail provider unconfigured, restricted account, expiring proof/export, deletion pending |
| `/account/subscription` | Hosted catalog availability, service term, purchase/subscription state, billing history | Open hosted checkout or billing portal; cancel renewal; refresh receipt | Sales not configured; payment pending; grace/expired; canceled but valid until term end; provider unavailable |

The table is an implementation map, not evidence these routes exist. Exact wire methods are generated from [Contracts](../contracts/README.md). Browser code consumes typed clients with a closed route map; reflection, runtime method registries and arbitrary string dispatch are not permitted.

## 4. Shared view state and freshness

Every data region has explicit `initial-loading`, `ready`, `empty`, `refreshing-with-old-data`, `stale`, `unavailable`, `forbidden` and `incompatible` states. Initial loading uses appropriately sized placeholders. Refresh preserves readable data and its original timestamp. Failure never turns previously observed data into a new success or resets it to zero.

Lists use server-defined stable sort and opaque page cursors; filter changes cancel the prior read and reset the list cursor. Selection binds IDs rather than row position. A deleted/re-enrolled Node cannot inherit a stale detail route's control authority. Concurrent responses are ignored unless their view generation matches the currently selected account, Center and target.

Updates are demand-driven. An active visible overview requests summaries; Run detail requests that Run's output/samples. Hidden tabs suspend long polls after their current bounded request and refresh on return. Use one coalesced refresh per target, bounded cancellation-aware backoff, and at most the negotiated concurrency. Reconnect obtains an epoch snapshot before applying new deltas. An epoch mismatch discards buffered deltas and renders a resynchronization indication.

View models preserve integer counters, revisions and byte offsets as exact values; do not convert 64-bit IDs/offsets through JavaScript floating-point numbers. Format user-visible time in the selected locale/time zone while preserving an unambiguous UTC value for copying and audit detail. Server sequence/revision, not wall-clock sorting alone, resolves update order.

## 5. Principal user flows

### 5.1 First connection

The device page explains `arcforges center connect <configured-center>` and directs the user to the existing Center consent/device-code flow. Show the requesting device fingerprint/name before approving. Enrollment and local permission are separate: after sign-in the page shows which remote grants are enabled and the precise local CLI command to grant view/control. The browser cannot silently grant itself a broader host permission.

The self-hosted flow stays on the user's configured Center and has no official subscription check. Official mode explains when a hosted subscription is required for node connectivity. Signing in, managing account security and revoking a device still work when connectivity is not entitled.

### 5.2 Create/configure a Sandbox

Creation first selects an existing locally issued provisioning grant and its immutable template revision. If none is available, the page explains the required local grant action and disables remote creation. Enrollment alone does not enable a free-form creation form. The form collects display name and only the isolation profile, read/write mount choices, network permissions and resource limits permitted by that template. It displays backend capability reasons before submission. Host paths are selected from locally authorized descriptors; the UI must not invent a generic arbitrary-path field for remote callers. It shows which settings apply to new Runs and which can affect live Runs according to Core semantics.

Create sends `provision_grant_id`, template revision and the complete requested configuration. Core verifies exact or narrowed authority and creates the bounded child Sandbox grant atomically with the Sandbox. Template revision conflicts require local review or selection of the current allowed template; the browser cannot widen or mint a provisioning grant. Configuring an existing Sandbox instead uses its Sandbox-scoped grant and preserves that grant's limits.

Submit includes a fresh command identity, the admitted Node owner epoch and the current expected revision for updates. After a conflict, display the server's current revision and let the user review changed values; do not silently overwrite. A display-name change uses Configure and never changes the Sandbox ID or owned root. Backend rejection preserves the previous configuration or shows the Core-reported partial result. A configuration saved successfully is distinct from a resource policy verified as active by the OS. Device rename is not a V2 Dashboard action; the device API exposes List/Inspect/Revoke.

### 5.3 Start and stop

Run launch uses an existing Sandbox, executable and argument array, relative working directory, and permitted environment inputs. Argument boundaries are visible; the browser does not concatenate user data into an implicit host shell. A shell is a program explicitly requested inside the Sandbox. Secret environment values never enter URL parameters, analytics, browser persistent storage, ordinary audit rows or notifications. Credential input comes from a secure local mechanism where the contract requires one.

After admission, retain the command ID until its result is known. Show `Starting`, a Run ID when available, and the exact operation state. A timeout shows “The result is not yet known” and offers a read-only reconciliation action. It does not offer an automatic new Start button that would duplicate an uncertain Run.

Reconciliation retains the original owner epoch. Reload, reconnect, receipt-body compaction or a new Handshake cannot silently rebind a saved command to a different store epoch. Render a compacted receipt or retired epoch explicitly; neither condition automatically creates another Start. Safe command display and the bound config/profile revisions come from the typed Run result, not reconstruction from a secret-bearing launch form.

Stop shows the selected Run and the Core's graceful-stop/escalation policy. Navigation away never stops a Run. A stop response reports whether the tree was confirmed exited or remains uncertain; the UI does not infer success merely because the node disconnected.

### 5.4 Files and safe deletion

Each import/export transfer contains one regular file and bounded chunks under a Sandbox-relative path. Multiple selection creates separate transfers with individual progress and outcome; it does not promise an atomic directory snapshot. Show bytes transferred, cancellation and conflict state. No archive is implicitly expanded, no symlink/junction target is followed, and no remote host search/editor is introduced. Validate each destination path and final commit on the Node; browser validation only provides early feedback. Interrupted transfers are not reported as complete or silently applied to a later file revision.

Use the authorized `DataService.InspectTransfer` read for asynchronous progress, final manifest digest and `closed_at`. Do not repeat `BeginExport` to discover whether preparation finished. `COMPLETE` means the immutable export was materialized and verified; source Runs may resume, while the private snapshot remains readable until explicit `CloseTransfer` or expiry. A lost final read can request the same range again during that lifetime. Receiving the last byte does not release the snapshot or make Sandbox deletion safe; the UI shows retained versus released/expired state separately.

Sandbox deletion is plan then execute. Display the plan's Sandbox identity, affected data size/estimate, active-run refusal and expiry. Execute binds plan and current revision with a new command identity and required approval. If contents, ownership or running state changed, Core refuses and the UI requests a new plan. A lost execute reply is reconciled by operation ID; pressing delete again must not create a fresh effect. Do not add a generic disk-cleaner, cache classification or deduplication page.

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
| `AFV2-WEB-02` | Sandbox, Run, Resource and regular-file transfer screens against typed APIs. Verify conflict/unknown outcome/deletion safety/capability restrictions; no hidden host path override or mutation auto-retry. |
| `AFV2-WEB-03` | Security, account and subscription views after `AFV2-ID-01` and commerce; remove obsolete probe/account composition. Verify real recovery/deletion/export and revoked/expired/disabled-provider business states. |
| `AFV2-WEB-04` | Qualify responsive/accessibility, keyboard/focus, all page states, offline/reconnect and uncertain-operation behavior across the finished Dashboard. Record explicit local browser evidence against real Center/PostgreSQL and both native Node profiles. |

Keep existing platform-native build, unit, static, bundle-budget, provenance and locked dependency gates. Task-listed typed response/view-model fixtures may exercise loading, empty, error, stale, inaccessible and provider-unavailable rendering, cancellation and late-response ordering. They never prove account authorization, subscription correctness, persistence, filesystem isolation or resource limits. Completed control/account journeys use real Center/PostgreSQL and real Windows/Linux Nodes; only explicitly permitted external mail/payment transports may be fixture peers. Public activation still requires actual provider/domain/business qualification.

Source evidence: [Cloud/Web/Contracts audit](../research/cloud-audit.md).
