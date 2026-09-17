# Shared Client States and Acceptance

Applies to the embedded assistant, Android and Web Chat, with native/browser-specific authentication and storage from their authorities. Existing professional editor offline rules remain intact.

| State / transition | Required presentation and available action | Durable rule / independent oracle |
|---|---|---|
| No account | local desktop/Android history/drafts can open; AI prompts sign-in on Send | no accidental upload or online capability claim |
| Authenticating / expired | identity form or reauthenticate sheet, preserve nonsensitive input/draft | challenge/session expiry and scope checked by server; no secret in UI store |
| Profile/workspace change | name target, seal pending work, clear private content before new load | old outbox cannot execute under new session |
| Loading / empty / partial | distinct spinner/empty action/index completeness with last updated time | stale result cannot overwrite newer route/query |
| Offline | persistent unobtrusive banner, own hydrated read/edit/draft/export available | AI send remains pending/explicit; product save/acquisition/render remain usable |
| Sending / unknown acknowledgement | show sending or reconciling, disable duplicate new-send action for same intent | receipt lookup with same command/hash before retry |
| Streaming / backfill | partial output label, stop and reconnect status; keep scroll position | ordered hash/cursor checks, terminal commit required for success |
| Approval pending / expired | durable attention, exact target/effects/expiry; approve/deny or refresh | stale grant/epoch/revision cannot authorize a new effect |
| Tool offline / incompatible | identify app/device and reason; inspect expiry/cancel/retry | never reroute to another product/device silently |
| Budget/admission denied | exact allowed/required quantities and retry/consent alternatives | no speculative debit; mobile has no purchase CTA |
| Task canceled / failed / interrupted | distinct state, effect certainty, result availability, safe follow-up | canceled does not imply an already performed effect was reversed |
| Resource downloading / verifying / ready | progress and stage, cancel/retry, destination | content invisible as ready until integrity/permission verify |
| Resource missing / denied / unsupported | separate reason, refresh/relink/safe-download only where permitted | no stale content leak and no false missing-file claim for unsupported preview |
| History promotion | explicit counts/destination/retention, restartable progress | idempotent manifest visibility commit; changed local source retained |
| Deletion / retention | scope, active task consequence, undo availability and retained-record disclosure | tombstone/index/purge fences survive reconnect/restore |
| Storage pressure / corruption | name affected local/cloud/derived store; export/recovery action | never evict canonical history or pending edits as cache |
| App/window close | preserve draft; show local running-job consequences when required | closing a view only disposes subscriptions; explicit stop command is separate |
| Upgrade / rollback | version compatibility reason, safe restart/forward-fix path | schema horizon and package hash interlock prevents destructive downgrade |

## Acceptance ledger

| Acceptance group | Surfaces / owners | Required real join |
|---|---|---|
| UX-A ownership | AS01–13, AN03–25; WP14/15/17/30/31 | two products, two windows in one product, two installations; no history/draft/channel crossover |
| UX-B composition | AS01–13; WP10/14/17/35/39 | exact Platform candidate consumed by product-specific host adapters; no adjacent source |
| UX-C history | AS01/02/07/09/12/13, AN07–10/15/22; WP15/25/31/49/52 | local/Cloud/temporary CRUD, promotion lost ack, account switch, export/deletion and terminal output ack |
| UX-D target/tool | AS03/05/06/11, AN05/06/09/11–13; WP09/11/26/31/52 | current same-product action, stale context/epoch/approval refusal, no second product involved |
| UX-E protocol | all async surfaces; WP03/06/23/24/26/31/49/52 | actual binary gRPC-Web unary and server streams in AOT C#, browser and Android, no named fixture retained |
| UX-F resources/search | AS03/08/09, AN14–18; WP13/18/19/25/35/39/40 | native/helper or Android-safe previews, current owner permissions, index completeness and exact scientific/media values |
| UX-G operations | AS10/12/13, AN19–25; WP42/44/45/46/48/50/52/53 | admission/usage, notifications, support/export/deletion, signed update, outage and fenced restore |
| UX-H native usability | all surfaces; WP10/17/30/31/32/49/50 | keyboard/IME/screen reader/large text, denied permissions, resize and process-death evidence |

WP17/30 may use explicitly named future-owner fixtures while producing real local stores/UI. Their receipts must name the replacing producer and method. WP31/49/52 and final release cannot close these groups on a fixture, source screenshot or mock API. Reference assets reused during implementation are listed with source path/hash/license and any changes in the owning repository's NOTICE inventory.
