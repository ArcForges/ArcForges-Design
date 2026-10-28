# 12 — Client applications

Page and screen specifications are in [experience/](../experience/README.md). This chapter fixes the client architectures.

**Amended 2026-10-28 (target; AF-CTR-04, AF-CTR-05) by [AD-0021](../decisions/AD-0021-central-access-go-center.md) §2, §5.** Ordinary client operations go through the configured center to an explicitly selected node; the shared client library's local connection serves node management, sign-in, diagnostics and recovery.

## 1. Shared client library (`ArcForges.Client`)

Used by the CLI, the Desktop and the MCP adapter.

| Component | Responsibility |
|---|---|
| `NodeEndpointResolver` | Endpoint descriptor, defaults and auto-start ([02](02-node-service.md) §3) |
| `NodeChannel` | LocalRpc client channel. `Hello` handshake with client kind, version and process hints. Compatibility check: a contract major mismatch → `INCOMPATIBLE` with guidance. |
| `NodeStreamCache` | Subscribes with `NodeEventService.Subscribe(topics, cursor)`. Applies the snapshot then events by `event_seq`. Detects gaps (sequence jump or generation change) → resubscribe without cursor (reset). Drops duplicates (seq ≤ last applied). Exposes observable collections per entity type. **Holds no authoritative state; every mutation goes through RPCs** (R-API-003). |
| `CommandIds` | UUIDv7 command IDs per user action. The same ID is reused on retry, so retries are idempotent (R-EXE-016). |
| `ConnectionState` | `CONNECTING`, `CONNECTED`, `RECONNECTING` (backoff 0.5 s → 10 s, jittered), `NODE_STOPPED`, `INCOMPATIBLE`, `ACCESS_DENIED` |

## 2. Desktop (`ArcForges.Desktop`, `ArcForges.Desktop.ViewModels`)

- **Stack:** Avalonia with compiled bindings only. View models use CommunityToolkit.Mvvm source generators, which keep them AOT-safe. Native AOT publish on Windows and Linux (V-N04; obligation in AD-0003).
- **Shell:**
  - DesktopPlatform `ArcForges.Desktop.Shell` models (surface catalogue, command palette, layout persistence, lifecycle coordinator, accessible node tree, error presenter, pseudo-localizer) are **reused unchanged**. ArcForges.Desktop provides their Avalonia view adapter.
  - Design tokens come from `ArcForges.DesignSystem` (reused).
  - Layout: left navigation (pages in [experience/desktop.md](../experience/desktop.md)), top status bar (node connection, enforcement summary, pressure level, account and plan), content area, and a notification drawer.
- **Single instance.** Named mutex `Local\ArcForges.Desktop.<user-hash>`. A second launch activates the first window through a local signal (`<data root>/run/desktop.sock` or pipe).
- **Tray.**
  - Where `TrayIcon` is supported (Windows; some Linux desktops, V-N04) it shows the node state colour, running and queued counts, and a menu: Open, Pause all pools, Resume all pools, Quit Desktop, Stop node (confirmation).
  - Without tray support, closing the window prompts once: "ArcForges keeps running in the background. Reopen it from the Start menu, or run `arcforges ui`."
  - Closing the window never stops the node (R-UX-002).
- **Notifications.** An in-app notification centre is fed by node events. OS notifications use Windows toast through WinRT projections where AOT-safe, otherwise tray balloons. Linux uses `org.freedesktop.Notifications` over D-Bus where available.
- **Accessibility.** Automation peers for every interactive control, full keyboard navigation (a focus order is defined per page) and a high-contrast token set. All specified pages target WCAG 2.2 AA. Automated checks run in headless Avalonia tests; the human screen-reader session is deferred (R-UX-006).
- **Localization.** English resources at launch. Pseudo-localization (reused) runs in tests to catch truncation and hard-coded strings.

## 3. CLI (`ArcForges.CommandLine`)

- **Parser.** System.CommandLine 2.x if its AOT publish is warning-free (A-N02, F-N02). Otherwise a small in-house parser covering the [command grammar](../experience/cli.md).
- **Output modes.**
  - Human: width-aware tables and colour only when stdout is a TTY and `NO_COLOR` is unset.
  - `--json`: one JSON document for results, JSON Lines for streams, using the canonical protobuf JSON mapping.
  - `--quiet`.
- **Behaviour.** Exit codes are defined in [experience/cli.md](../experience/cli.md) §3. `arcforges run` exits with the task's exit code (R-UX-003). Shell completion is available for bash, zsh, fish and PowerShell.
- **Auto-start.** If the node is absent, the CLI starts it ([02](02-node-service.md) §3). Inside AI-client sandboxes or CI jobs, where auto-start is refused, it prints guidance.

## 4. MCP adapter (`ArcForges.Mcp`)

See [08](08-ai-integration.md) §2 and [experience/mcp.md](../experience/mcp.md). It uses the official C# MCP SDK if A-N01 is confirmed, otherwise an in-house stdio JSON-RPC implementation with source-generated JSON.

## 5. Web (`ArcForges.Web.Site`, `ArcForges.Web.App`)

- **Public site.** The existing C# static generator, which publishes no JavaScript, adapted for ArcForges pages: home, features, pricing, download, documentation index, security, privacy, terms and status link. Downloads link to signed artifacts and manifests in R2.
- **Account profile** (Blazor WebAssembly, adapted from the existing Account profile):
  - account overview, security (passkeys, sessions), devices and nodes, subscription and billing;
  - support cases, privacy and data;
  - `/connect` (node sign-in approval) and `/activate` (device code);
  - existing cookie session with CSRF and Origin checks;
  - binary gRPC-Web for unary calls.
- **Fleet profile** (Blazor WebAssembly, new): fleet overview and node detail. Live updates use the viewer WebSocket with `relay.v1.ViewerFrame` protobuf messages decoded by the generated C# classes ([10](10-cloud.md) §1); there is no JavaScript business code. A fallback uses `WatchFleet` gRPC-Web streaming with `GrpcWebText` (V-N03).
- **Checkout.** Paddle **hosted checkout by redirect**, with the URL created through the reused `CommerceService.CreateCheckoutAttempt`, so the site needs no third-party JavaScript. Return pages poll the purchase state.

## 6. Android (`ArcForges.Mobile`)

- **Stack.** .NET MAUI Shell, Mono AOT release with R8 (existing), and gRPC-Web clients (existing transport).
- **Services:**

| Service | Implementation |
|---|---|
| `AuthService` | Custom Tabs with PKCE and a verified app link (`https://arcforges.com/app/callback`); QR pairing ([10](10-cloud.md) §3.3); refresh-token storage in the Keystore (reused `ArcForges.Mobile.Security`) |
| `FleetClient` | gRPC-Web `FleetService` and `NodeEnrollmentService` |
| `ViewerSocket` | `ClientWebSocket` to the relay, decoding `ViewerFrame`s. Foreground only. Reconnect backoff 1 s → 30 s. Resume by cursors. |
| `PushService` | Firebase Messaging binding (existing design). Data messages → local notifications with deep links; token registration through the reused `NotificationService.RegisterPush` |
| `BillingService` | `Xamarin.Android.Google.BillingClient` (V-C06, F-C01) → `StoreBillingService` |
| `QrScanner` | Camera barcode scanning with a C# library compatible with trimming and R8, verified by the Android task (A-C02, F-C02). Manual code entry as a fallback. |
| `SecureStore` | Reused Keystore wrapper |

- **Lifecycle.**
  - **Background:** no live connection is kept (Android background limits). Push data messages produce notifications.
  - **Foreground:** the app re-opens the viewer socket and reconciles from the snapshot.
  - **Offline:** a banner with the last-updated time; actions are disabled with the reason shown.
  - **Notifications:** on Android 13+ the `POST_NOTIFICATIONS` permission is requested at the first opt-in, and its denial is handled.
