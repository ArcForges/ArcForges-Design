# Embedded Application Assistant

Owner: DesktopPlatform `ArcForges.Assistant.Avalonia`, WP15/17. Composition and ports: [architecture 27](../architecture/27-platform-projects-and-application-assistants.md). History: [model 05](../architecture/data-model/05-application-history.md). All current assistant feature requirements remain; there is no standalone ArcChat executable.

## 1. Presentation and navigation

One session/store per application profile; any number of ordinary application windows may host a view, with one assistant surface per host window. All views show the app identity, active workspace and history mode. They never show another application's history by default. The app command `Assistant.Toggle` opens/focuses its own last surface. Default shortcut Ctrl+Shift+Space (Command+Shift+Space on macOS) is configurable through the existing conflict-aware command system; no system-wide global hotkey or separate launcher is required.

| Presentation | Layout and entry | Persistence / exit |
|---|---|---|
| Docked (default) | right panel, preferred 400 logical px, minimum 320; full host height. Header, message viewport, sticky composer; tabs/menus open over the panel. | Width/visibility device-local per app/window; Escape closes menus, then returns focus to host, not implicit task cancellation. |
| Floating | owned application window, initial 480×720, minimum 360×480; same conversation service, own draft. | Persists bounds within visible monitors; close returns to host and preserves draft. No independent process. |
| Expanded | owned window or full app panel, initial 1100×760, minimum 800×600; sidebar 240, central conversation≥360, optional preview 320. | Below 900px hide preview behind a tab; navigation state local; no editor layout or cross-product setting sync. |

```text
Expanded view
+--------------------+-----------------------------------+---------------------+
| ArcNotes Assistant | [workspace] [Local history] [•••] | Resource preview    |
| New conversation   | Conversation title / branch       | Source · permission |
| Search             |                                   |                     |
| Conversations      | You: frozen selection + question  | bounded content     |
| Tasks [2 attention]| Assistant: streamed answer        | / native fallback   |
| Projects           | [sources] [tool card] [result]     |                     |
| Library            |                                   | [Open in ArcNotes]  |
| Automations        | [context chips] [profile] [mode]  | [Save as…]          |
| Settings           | [multiline draft           ][Send]|                     |
+--------------------+-----------------------------------+---------------------+
```

Docked/floating modes replace the sidebar with a labelled navigation menu and conversation picker; no feature disappears because the window is small. Task/approval attention badge remains visible even while chat is closed. Header's app name is immutable; a workspace switch runs the profile-switch flow, never just changes a label.

## 2. Complete surface catalogue

| ID / surface | Controls and information | Actions, state and ownership |
|---|---|---|
| AS01 Home / conversation list | New chat, search, pinned/recent groups, title, last activity, local/cloud badge, overflow | create/rename/pin/archive/trash; empty state explains first local chat; keyset 50/page; unsent drafts badge per window; WP15 |
| AS02 Conversation | header title/branch breadcrumb, chronological messages, source labels/citations, tool cards, output status, composer | edit submitted message forks, retry preserves command semantics, branch picker, copy/export, stop, scroll-to-latest; immutable committed messages; WP15/17 |
| AS03 Context inspector | selected document/range/resources, owner/revision/size, source kind, egress destination | inspect/remove/freeze; explicit “Use current selection”; stale or missing resource blocks send until refreshed/removed; never follows live host selection after send; WP09/17 |
| AS04 Profile / mode | ordinary/agent/temporary choice, model profile, skills, project association | default ordinary; agent shows action/credit consequences; temporary visibly suppresses history/memory; unsupported choice has reason; WP15/17/52 |
| AS05 Task list/detail | state/reason, progress, current tool, target app/device, timeline, produced artifacts, usage/effect certainty | open, pause/resume/cancel/steer where allowed, fork/clone under existing semantics; failed/interrupted distinct from complete; WP16/17/52 |
| AS06 Approval | originator, exact operation/target/resources/revisions, egress, expected side effects/cost, expiry | approve once or deny; never generic persistent “allow all”; highest risk routes to local presence on target; stale approval refreshes; WP11/17/26 |
| AS07 Projects/profiles/skills | list/detail, scoped instructions/source disclosure, profile/skill version | create/edit/archive supported existing metadata; immutable instructions snapshot per execution; untrusted imported instructions cannot grant access; WP15 |
| AS08 Library / artifact preview | generated/uploaded artifacts with owner/status/hash/version, file kind, citations | preview, open own product resource, Save As/export with egress check, delete when owned; unsupported format downloads/opens only after safe native choice; WP17/25 |
| AS09 Search | query, current app/project scope, local/cloud source badges, completeness/index status | title/body/source results, branch jump, exact citations; local-only history stays local; no federation into other products; WP15/40 |
| AS10 Automations | existing rules list, enabled state, next occurrence/timezone, target, last run and budget | create/edit simple or full supported desktop rule, pause/delete, inspect occurrence; server authority, no local scheduler masquerading as always available; WP17/52 |
| AS11 App capabilities | this app's registered features/extensions, availability/version/risk/permission | inspect grant/revoke/settings, explain absent native/helper/device dependency; no discovery of installed peer products; WP09/17/41 |
| AS12 Settings/security | profile/account/workspace, history default, devices/grants, theme/density/shortcuts, diagnostics/support, storage/recovery | explicit profile switch, Cloud opt-in/import, local copy/delete/export, sign-out, permission review; account-wide commerce opens Account portal under existing desktop rules; WP10/11/15/17 |
| AS13 Trash/history/recovery | tombstone/retention, branch/history revision, interrupted runs/pending imports, unavailable objects | restore only where policy allows; verify imported/exported snapshot; no undo claim after destructive purge; WP15/25 |

## 3. Composer and message interaction

Composer persists a per-window draft after each debounced edit (≤500ms) and before navigation/shutdown; temporary draft stays memory-only. Enter sends, Shift+Enter newline; IME composition Enter never sends. Send button exposes keyboard/screen-reader state. After submit, clear only the snapshotted draft revision after the local transaction commits; a newly typed draft survives. “Queued locally”, “Sending”, “Accepted” and “Failed/unknown outcome” are visibly distinct. Offline does not pretend that an AI request was admitted. Stop targets the displayed execution, not unrelated tasks.

`@` opens explicitly permitted own-app resource/context search; `/` selects existing commands/skills. Suggestions are keyboard navigable and Escape preserves typed text. Attach via file picker, drag/drop or paste; inspect selected kind/size/count and upload status before admission. File selection grants access only to those files. Failed transfer remains a removable/retryable chip, not a vanished attachment. Host selection enters only on explicit context action or a visible invocation command that describes it. A locked chip shows frozen revision and source; replacing it creates a new draft snapshot.

Auto-scroll follows output only when already near the bottom (within 64px); reading earlier messages pauses follow and shows “New output”. No focus stealing on token updates. Select/copy text without live updates collapsing selection; code blocks have copy and wrap controls, links display destinations and cannot execute actions. Display concise tool progress and returned evidence, not hidden model reasoning. Citation opens the authorized resource/version/anchor, or explains missing/stale/permission state.

## 4. Tool, task and preview behavior

A tool card shows operation, app/device target, frozen inputs, state and effect certainty. Approval cards are durable attention items; dismissing the surface leaves them in Tasks. A lost response shows reconciliation before retry. Native render/export/capture are ProductJobs linked from a Cloud task when requested, not relabelled AI runs. The app can keep editing while Cloud work runs; shutdown confirms consequences of local work and makes remote device tools unavailable.

Preview supports plain/Markdown/code, inert sanitized HTML, bounded tables/measurement reports, images, PDF through restricted helper, audio/video through admitted host capability and exact timeline/frame references. No active HTML/script or arbitrary native parser inside the assistant package. Absent preview capability yields metadata plus safe Save As/Open action; content is not falsely reported missing. Captures remain bounded reports/selected ranges unless explicit raw upload. Video source precision, captions and render artifact identity retain Slate rules. An artifact's “Open in app” targets the current owning application only; future cross-product destinations are not shown.

## 5. History/privacy and lifecycle UI

Local/cloud/temporary badge is always visible beside the title and before first send. Local badge explains selected content is processed by Cloud AI but history remains on this installation. “Save to Cloud” opens an import review with counts/resources, destination workspace, retention and copy behavior. Progress survives restart; changed local history is retained as a separate copy. “Make local copy” does not delete the Cloud original. Changing the default affects new conversations only.

Deleting a conversation presents local vs Cloud consequences, pending task status and undo/retention availability. It does not silently cancel already effected work or reverse charges. Sign-out/profile switch stops subscriptions, seals drafts/pending commands, clears private previews and requires authentication for the old partition. Layout and public theme preferences may remain; conversation snippets never leak into another profile. Closing one assistant surface preserves shared task state and returns focus to its host.

## 6. Accessibility and acceptance

All controls have names/roles, focus order and keyboard paths; minimum target size follows shared desktop tokens, contrast/high-contrast/reduced-motion/text scaling are tested. Streaming announcements are throttled to meaningful sentence/status changes, with user pause. Color is never the only state cue. Restore windows onto available screens after monitor changes. Test Chinese/English IME, long localized labels,200% text scaling, RTL structure and screen reader navigation.

WP17 acceptance uses the published package from a clean sample host plus ArcNotes integration. WP35/39 independently compose the same package in Scope/Slate with their own store/context/action ports. Two apps must show unrelated conversations/drafts and independent connection loss; two windows in one app must show consistent commits without draft overwrite. WP52 completes actual model/tool/approval/usage/reconnect and WP50 tests installed signed applications. A screenshot or fixture-only UI does not close real integration.
