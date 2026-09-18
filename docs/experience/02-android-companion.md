# Kotlin Android Companion Experience

Authority: [P2-012](../decisions/phase-2-specification-decisions.md#rule-p2-012). Native Kotlin/Jetpack Compose, Android only. Production module plan is in [architecture 27](../architecture/27-platform-projects-and-application-assistants.md); wire/target behavior in [annex 10](../architecture/contracts/10-application-scope-and-streams.md). Preserve the complete companion capabilities and consumption-only commerce boundary.

## 1. Navigation and top-level layout

Five bottom destinations: **Home, Chats, Tasks, Library, Settings**. Devices is a Home card and `Home → Devices` route, not a sixth bottom tab. Current workspace is in the app bar; own-chat vs selected desktop application is an explicit scope chip below it. Switching target opens/selects a separate scoped destination; it never retargets an existing chat, request, draft or approval.

```text
+-------------------------------------+
| Workspace v                  Account|
| [My chats v] / [ArcNotes · PC-A v]   |
|                                     |
| Needs attention: approval / failure  |
| Continue chat                       |
| Connected applications              |
|   PC-A · ArcNotes      Online        |
|   PC-A · ArcSlate      Offline       |
| Recent tasks / saved artifacts       |
|                                     |
| Home | Chats | Tasks | Library | ⚙  |
+-------------------------------------+

Chat destination
+-------------------------------------+
| < Title / branch           [•••]    |
| [Cloud history] [My chats]           |
| user + authorized context chips     |
| assistant output / citations        |
| tool status / approval / result     |
|                         [New output]|
| [+] [multiline message…]     [Send] |
+-------------------------------------+
```

Compact width<600dp uses a single pane and bottom navigation.600–839dp uses a navigation rail with list/detail when both fit;≥840dp can show chat plus preview. These layouts support Android tablets/foldables/resizable windows, not iOS. State is keyed by route+profile+product+object ID. Bottom-tab switching preserves each tab's back stack; switching workspace clears old private stacks after sealing drafts. Back closes IME, then sheet/dialog, then detail, then returns to previous route; at root follows Android system exit behavior. Predictive Back must not submit, delete or cancel work.

## 2. Route and action catalogue

| Route ID / module | Layout / primary controls | Required actions and data | Empty/error/recovery |
|---|---|---|---|
| AN01 Welcome / auth | service/realm name, sign-in/create/recover, privacy links | configured official Cloud URL; custom realm only through existing allowed settings, HTTPS validation; no local host/token QR login | offline explanation; no fake signed-in state |
| AN02 Login / auth | email/passkey/provider, bounded proof entry, resend countdown | existing flow IDs/challenges/expiry; Credential Manager/system browser callbacks, exact redirect validation | wrong/expired/used proof preserves identity input, never token logs |
| AN03 Workspace / auth | owned-workspace list, role/storage/service status | choose authorized workspace; first-use Cloud-history disclosure; recheck current ownership | removed workspace locks content, return to list |
| AN04 Home / home | attention cards, continue chat, app presence, recent tasks | fetch durable attention first, reconnect indicator, open object route | no attention is positive empty state; unavailable service shows last-update timestamp |
| AN05 Devices / devices | grouped devices with separate installed app rows, last seen/version/trust | select one app, details, trust/revoke own device via step-up, capability availability | offline target visible with expiry implications; no switch to another app automatically |
| AN06 Target detail / devices | product/device/installation identity, capabilities/grants and attention | explicit authorized control entry; no arbitrary keyboard/mouse/desktop-screen remote control added | incompatible/revoked/expired grants explain required action |
| AN07 Chats / chat | search/new, pinned/recent, local/cloud badge, row menu | list/rename/pin/archive/trash, choose local/cloud/temporary new chat, app-specific Cloud history | no local-only desktop history shown; empty list offers creation |
| AN08 Conversation / chat | title/branch, messages, context chips, composer | ordinary/agent/temporary, profile/skill selection, send/stop, branch/retry/copy/citations; typed gRPC-Web output | draft persisted, partial output marked, resume uses cursor/receipt |
| AN09 Context / chat | bottom sheet with app/project/source/revision/size | inspect/remove/freeze sources, picker/upload, no live-follow selection | unavailable/stale/too-large source blocks affected send with remedy |
| AN10 Branch/history / chat | ancestry list and message preview | open/fork at selected immutable message; history mode/change summary | unsupported revision read-only, no silent overwrite |
| AN11 Tasks / tasks | filters state/target, attention first, progress and usage | list/open/cancel/pause/resume only when allowed | stale state refreshes before action, unknown effect reconciles |
| AN12 Task detail / tasks | timeline, step/tool/target, reasons, artifacts, budget | inspect, steering form, cancel confirmation, clone/fork existing actions | expired/offline target shows durable wait/retry state |
| AN13 Approval / tasks | full-screen sensitive operation, target/source/egress/effects/cost/expiry | approve once/deny with idempotency; step-up where required | expired approval read-only; local-presence action instructs target desktop, no biometric substitution |
| AN14 Library / library | projects, resources, saved search, simple automation sections | list/open/filter within current product scope | no cross-product merged library |
| AN15 Project/profile/skill / library | metadata, instruction/source disclosure and version | supported create/edit/archive/attach behavior; preserve existing bounded mobile scope | concurrent change offers reload/copy; no untrusted content granted authority |
| AN16 Search / library | query/scope/source kind, index/completeness badge | permission-aware results/citations; exact Notes scalar projections where admitted | lexical-only and unavailable are distinguished; query change cancels obsolete result |
| AN17 Resource detail / library | metadata/status/provenance/version, preview pane, safe actions | view text/code/Markdown/image/PDF, bounded table/report, audio/video; download/export via Storage Access Framework | unsupported preview shows metadata/download, missing or unauthorized differs |
| AN18 Transfers / library | item-level progress/hash/stage/retry/cancel | resumable upload/download, metered-network confirmation, explicit local file destination | process death resumes bounded journal; hash mismatch discards unsafe partial file |
| AN19 Automation / library | rule list, schedule/timezone/next occurrence, target/budget | existing simple-rule create/edit/pause/delete, run history; Cloud scheduling authority | offline edit remains draft; no local timer guarantee |
| AN20 Settings / settings | account/workspace, appearance, history, privacy, storage, notifications, help | navigate subsection, sign out, diagnostics consent, app version/update destination | consent defaults safe; no key-entry or purchase CTA |
| AN21 Account/security / settings | sessions, credentials, device trust, recovery, deletion status | existing generated operations and system auth; export/delete explanations | reauthentication locks private UI and seals pending operations |
| AN22 History/storage / settings | own local cache/history, Cloud default, pending imports, quotas | Save to Cloud/local copy/export/trash management; Cloud/local difference explicit | clearing cache cannot delete canonical local history or pending work |
| AN23 Notifications / settings | system permission/status, categories, privacy preview | ask permission only after contextual explanation; system settings shortcut | denied/non-GMS keeps in-app attention; no promise of background immediacy |
| AN24 Support/diagnostics / settings | problem category, full redacted report preview, consent | create support case/report, status/help/security advisory | offline draft, explicit upload retry, no automatic content dump |
| AN25 Admission/usage / tasks | allowance/credits/status and exact requested consequence | accept allowed credit use or cancel under existing policy; consumed-only info | no buy button, external checkout CTA, license-key entry or hidden web purchase page |

## 3. Android interaction details

Touch targets≥48dp; semantic names/state descriptions and TalkBack order for every action. Large text up to 200% reflows; accessibility actions expose menus otherwise shown by long press. Long press selects/copies text or opens a row menu; destructive swipe is not the only path. Pull-to-refresh requests a snapshot without discarding pending drafts. Destructive actions use explicit dialogs naming local/cloud scope; snackbars offer undo only where a real reversible operation exists.

Composer is multiline with a visible Send button. IME action inserts newline by default; hardware Ctrl+Enter sends, and composition Enter never does. Keyboard/insets move the composer above the IME; the message list preserves position. Draft is sealed within 500ms and before route switch; submit clears only the committed draft revision. Gallery Photo Picker/SAF selects attachments without broad storage permission; share-in opens a review sheet and target conversation selection, never immediately uploads. Persist only granted URI access, copy bounded content into app-private staging when necessary, and revoke unused grants. Camera/microphone permissions are requested only by an already accepted feature needing them; no voice-recording product scope is added by the presence of a microphone icon in a reference.

Auto-scroll follows near-bottom output only; reading earlier messages shows a New output button. Streaming updates announce meaningful states, not every token. Backgrounding closes streams and saves position/drafts; FCM hints trigger durable object fetch after authentication. Use WorkManager for eligible deferred transfers/cleanup with constraints, not a permanent chat-service process. Force-stop/reboot/offline/background restrictions are shown honestly. Initial launch needs no notification permission to chat.

## 4. Authentication, target and privacy flows

Native bearer credentials are held by the network/security module and OS Keystore-backed storage, never Compose state, SavedStateHandle or navigation arguments. Deep links/push carry only opaque object IDs and intended product scope; resolve session/workspace/current permission before rendering. A route to a revoked device/resource shows denial even if the notification text was previously received. Lock-screen notifications show a generic attention summary by default.

Changing target from ArcNotes/PC-A to ArcSlate/PC-A opens that application's scoped surface; pending Notes approvals remain bound to Notes. Own companion chats remain their own history. Creating a remote tool task explicitly shows the target before submit and freezes it; changing the header later cannot redirect the task. Local-only desktop conversations remain inaccessible. Choosing a Cloud desktop conversation is an explicit read/write of that application's authorized Cloud history, not joining a local assistant window.

Room owns per-profile drafts, local-history canonical rows, Cloud projection/pending receipts, transfer journal and cursors. Existing bounded outbox 1000 items/20 MiB and cache 128 MiB default/512 MiB cap remain; canonical local history/pending work is not evictable cache. Logout/profile switch seals the old partition, cancels subscriptions, removes private previews and prevents queued work from sending under a different identity. Temporary mode never writes content to Room/saved state/crash logs. Process death cannot claim a temporary conversation was restored.

## 5. Integration and independent acceptance

WP30 produces core modules, real generated Maven client, Room/Keystore/lifecycle and route shell with named Task fixtures. WP31 completes all AN01–AN25 actions against real Cloud25/26/42/45/52, including binary stream recovery, actual same-app remote tools, history modes/import and permission expiry. WP32 produces signed APK/AAB and physical-device/store evidence. Tests include phone/tablet, rotation/fold/resizing, background/force-stop, denied notification/file access, no-GMS, slow network, lost acknowledgement, two applications on one device, TalkBack/IME/large text and account switch.

The AionUi mobile reference supplies interaction/layout ideas; it is not a React Native implementation dependency. Kotlin modules consume published Contracts packages by exact version with dependency locks; platform NuGets are not imported or translated into Android code. Shipping uses the existing automatic main CI sequence and signing gates; a Hello World APK does not satisfy this complete UI acceptance.
