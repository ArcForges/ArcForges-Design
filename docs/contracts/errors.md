# V2 error vocabulary

Foundation `ArcError`, effect certainty and retry advice remain immutable. Implicit authentication, overload, node-stopping, rate-limit and dark-surface errors apply to every method. An `UNKNOWN` effect never pairs with `AFTER_TIME`; reconcile the original durable command instead; transient terminal uncertainty follows the live-lease rule and never triggers automatic input replay.

| Category / code | Meaning | Retry advice | Effect | Details |
|---|---|---|---|---|
| `VALIDATION/invalid_argument` | Malformed or out-of-bounds typed input | NEVER | DID_NOT_HAPPEN | Field and safe reason |
| `VALIDATION/invalid_cursor` | Cursor owner, filter or epoch mismatch | NEVER; start a fresh read | DID_NOT_HAPPEN | Current epoch |
| `VALIDATION/path_rejected` | Unsafe, unauthorized or unsupported path form | NEVER | DID_NOT_HAPPEN | Redacted relative path reason |
| `AUTHENTICATION/unauthenticated` | Missing/expired local or Center identity | NEVER; authenticate | DID_NOT_HAPPEN | No sensitive resource information |
| `AUTHORIZATION/permission_denied` | Local or remote grant does not allow this operation | NEVER | DID_NOT_HAPPEN | Required scope |
| `ENTITLEMENT/hosted_access_required` | Official-hosted access is inactive | NEVER; update hosted subscription | DID_NOT_HAPPEN | Hosted mode only; never a local error |
| `CONFLICT/revision_mismatch` | Expected aggregate revision changed | NEVER; inspect and explicitly reissue | DID_NOT_HAPPEN | Expected/actual revision |
| `CONFLICT/command_id_reused` | One command ID is reused with a different canonical payload | NEVER | DID_NOT_HAPPEN | Command ID |
| `CONFLICT/owner_epoch_retired` | Durable mutation carries a retired or different owner epoch | NEVER; inspect original authority | DID_NOT_HAPPEN | New attempt refused; no claim about a previous effect |
| `STATE/receipt_compacted` | Known original response body was compacted but non-executable command identity remains | NEVER; inspect retained operation/aggregate | DID_NOT_HAPPEN or HAPPENED | Original known effect, original aggregate and command identity; never reexecute |
| `EXECUTION/terminal_ack_unavailable` | A live terminal acknowledgment was lost/evicted or a consumed native input effect is uncertain | NEVER; inspect terminal state and take a new explicit user action | UNKNOWN | No durable GetOperation receipt; no automatic byte replay |
| `CONFLICT/identity_changed` | Native file/root/grant identity changed since preview | NEVER; inspect and plan again | DID_NOT_HAPPEN | Safe identity reason |
| `CONFLICT/lease_stale` | Terminal lease expired or generation/epoch changed | NEVER; reacquire locally | DID_NOT_HAPPEN | Current lease generation without credential |
| `STATE/not_found` | No visible aggregate or durable receipt for this query | NEVER | DID_NOT_HAPPEN | Query only; absence does not prove an earlier terminal input had no effect |
| `STATE/busy` | Conflicting admission/configure/delete operation is holding ownership | AFTER_TIME only when DID_NOT_HAPPEN | DID_NOT_HAPPEN | Blocking operation ID if visible |
| `STATE/managed_use` | A nonterminal owned Run or transfer holds data | NEVER; stop or close explicitly | DID_NOT_HAPPEN | Visible managed use IDs |
| `STATE/terminal_unavailable` | Requested profile/mode has no qualified terminal | NEVER | DID_NOT_HAPPEN | Capability requirement |
| `STATE/node_stopping` | Node is draining or reconciling | AFTER_TIME only when DID_NOT_HAPPEN | DID_NOT_HAPPEN | Readiness reason |
| `STATE/not_activated` | Configured remote surface remains dark | NEVER | DID_NOT_HAPPEN | Deployment mode |
| `RESOURCE/budget_unavailable` | Immediate Run admission lacks capacity | AFTER_TIME only when DID_NOT_HAPPEN | DID_NOT_HAPPEN | Needed versus available budget; no queue |
| `RESOURCE/enforcement_failed` | OS limit apply/readback cannot prove required control | RECONCILE for UNKNOWN; NEVER for DID_NOT_HAPPEN | DID_NOT_HAPPEN or UNKNOWN | Dimension and boundary identity |
| `RESOURCE/disk_space` | Journal/data/output reservation cannot be honored | AFTER_TIME only when DID_NOT_HAPPEN | DID_NOT_HAPPEN | Required and available bytes |
| `RESOURCE/overloaded` | Bounded server work or stream capacity exceeded | AFTER_TIME only when DID_NOT_HAPPEN | DID_NOT_HAPPEN | Retry time if known |
| `RESOURCE/rate_limited` | Local/operator or hosted connection/request rate exceeded | AFTER_TIME only when DID_NOT_HAPPEN | DID_NOT_HAPPEN | Rate scope; no local paid gate |
| `EXECUTION/unsupported_combination` | Backend cannot enforce all requested requirements | NEVER | DID_NOT_HAPPEN | Profile and missing capability |
| `EXECUTION/outcome_unknown` | Accepted native or routed effect lacks authoritative completion | RECONCILE | UNKNOWN | Original command ID and GetOperation route |
| `EXECUTION/launch_failed` | Definite pre-execution/launch failure with empty boundary | NEVER | DID_NOT_HAPPEN | Exit provenance and reason |
| `INTERNAL/store_corrupt` | Store integrity or migration receipt failed | NEVER; recover using approved backup | UNKNOWN | Safe diagnostic correlation |
| `INTERNAL/internal` | Unexpected service failure without a safe outcome claim | RECONCILE for UNKNOWN; NEVER for DID_NOT_HAPPEN | DID_NOT_HAPPEN or UNKNOWN | Correlation ID only |
