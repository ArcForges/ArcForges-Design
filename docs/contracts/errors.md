# Error catalogue

Every failed call returns `arcforges.foundation.v1.ArcError` with:
- `category` (`ErrorCategory`) and `code` (the snake_case code below);
- `message_key` = `error.<category>.<code>`, for example `error.state.not_found`;
- `retry` (`RetryAdvice`) and `effect` (`EffectCertainty`);
- `correlation_id`;
- the `details` listed here.

Method annotations name codes as `CATEGORY/code` ([README](README.md) §4). `tools/check_design.py` fails when a method names a code that is missing here.

**Implicit codes.** These can be returned by any method and are not repeated in method annotations:
- `INTERNAL/internal`;
- `RESOURCE/overloaded`;
- for local node methods: `STATE/node_stopping`;
- for cloud methods: `AUTHENTICATION/unauthenticated`, `RESOURCE/rate_limited`, and `STATE/not_activated` while the method's surface is not activated in production ([10](../architecture/10-cloud.md) §8).

**Effect rule.** A mutation that fails before any durable change returns `DID_NOT_HAPPEN`. When the outcome is uncertain (for example a peer or cloud call timed out after sending), the method returns `UNKNOWN` with `retry.mode = RECONCILE` and the read operation to call. A retry with the same `command_id` is always safe (AD-0004).

| Category / code | Meaning | Retry advice | Effect | Details |
|---|---|---|---|---|
| `VALIDATION/invalid_argument` | A field violates its `validate:` rule | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = field path and rule |
| `VALIDATION/unsafe_batch_argument` | A batch-file argument cannot be quoted safely (CVE-2024-24576 class) | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = argument index |
| `VALIDATION/unsupported_shell` | The requested shell is unavailable on the executing node | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = shell kind |
| `VALIDATION/path_not_found` | A required path does not exist or is not a directory | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = path field |
| `VALIDATION/inputs_required` | Remote placement needs input selection, and none can be derived safely (for example a non-git working directory) | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = working directory |
| `VALIDATION/program_not_found` | `argv[0]` did not resolve through PATH/PATHEXT | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = program |
| `VALIDATION/invalid_dependency` | A dependency is missing or forms a cycle | `NEVER` | `DID_NOT_HAPPEN` | `state.resource` = dependency |
| `VALIDATION/invalid_policy` | The policy document has ERROR issues | `NEVER` | `DID_NOT_HAPPEN` | Issues in the method value |
| `VALIDATION/invalid_cursor` | A page or stream cursor is malformed or from another generation | `NEVER` (restart listing) | `DID_NOT_HAPPEN` | — |
| `VALIDATION/incompatible_version` | Contract or protocol major mismatch | `NEVER` | `DID_NOT_HAPPEN` | `upgrade` (`VersionFailure`) |
| `VALIDATION/code_invalid` | Unknown device user code | `NEVER` | `DID_NOT_HAPPEN` | Remaining attempts in `limit` |
| `VALIDATION/purchase_invalid` | Google Play rejected the purchase token | `NEVER` | `DID_NOT_HAPPEN` | — |
| `AUTHENTICATION/unauthenticated` | Missing or invalid credential | `NEVER` (sign in again) | `DID_NOT_HAPPEN` | — |
| `AUTHENTICATION/token_expired` | Access, relay or refresh token expired | `SAME_COMMAND` after refresh | `DID_NOT_HAPPEN` | — |
| `AUTHENTICATION/credential_revoked` | The device, node or session was revoked | `NEVER` | `DID_NOT_HAPPEN` | — |
| `AUTHENTICATION/step_up_required` | The operation needs a recent strong authentication | `SAME_COMMAND` after step-up | `DID_NOT_HAPPEN` | — |
| `AUTHENTICATION/signature_invalid` | A manifest, token or command signature failed verification | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = what failed |
| `AUTHORIZATION/permission_denied` | The origin is denied by the permission matrix or ownership | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = matrix operation |
| `AUTHORIZATION/approval_required` | An approval request was raised; the node executes the request once approved | `RECONCILE` via `ApprovalService.GetApproval` | `DID_NOT_HAPPEN` (yet) | `state.resource` = `{kind: "approval", id}` |
| `AUTHORIZATION/command_pattern_denied` | The command is outside the agent's or peer's allowed patterns | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = policy path |
| `AUTHORIZATION/peer_policy_denied` | The peer policy does not allow this operation | `NEVER` | `DID_NOT_HAPPEN` | — |
| `AUTHORIZATION/account_mismatch` | Play `obfuscatedAccountId` differs from the caller's account | `NEVER` | `DID_NOT_HAPPEN` | — |
| `ENTITLEMENT/feature_not_entitled` | The plan lacks the cloud feature (`remote.*`, `push`); local and LAN features are never gated | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = feature |
| `ENTITLEMENT/plan_limit_reached` | A per-plan count (nodes, viewers) is exhausted | `NEVER` | `DID_NOT_HAPPEN` | `limit` |
| `CONFLICT/revision_conflict` | `meta.expected_rev` differs from the current revision | `NEVER` (re-read, merge) | `DID_NOT_HAPPEN` | `revision` |
| `CONFLICT/already_exists` | The named object already exists | `NEVER` | `DID_NOT_HAPPEN` | `state.resource` |
| `CONFLICT/command_id_reused` | The same `command_id` arrived with a different payload digest | `NEVER` | `DID_NOT_HAPPEN` | — |
| `CONFLICT/digest_mismatch` | A plan digest differs from the presented one | `NEVER` (re-plan) | `DID_NOT_HAPPEN` | — |
| `CONFLICT/code_reused` | A sign-in code was presented twice; the flow is revoked | `NEVER` | `DID_NOT_HAPPEN` | — |
| `CONFLICT/purchase_already_linked` | The Play purchase is linked to another account | `NEVER` | `DID_NOT_HAPPEN` | — |
| `STATE/not_found` | The object does not exist (or is not visible to the caller) | `NEVER` | `DID_NOT_HAPPEN` | `state.resource` |
| `STATE/invalid_state` | The object's state does not allow the operation | `NEVER` | `DID_NOT_HAPPEN` | `state.state`, `state.reason` |
| `STATE/expired` | A flow, offer, pairing or approval expired | `NEVER` | `DID_NOT_HAPPEN` | — |
| `STATE/plan_expired` | A cleanup or integration plan expired | `NEVER` (re-plan) | `DID_NOT_HAPPEN` | — |
| `STATE/node_stopping` | The node is shutting down or switching versions | `AFTER_TIME` (2 s) | `DID_NOT_HAPPEN` | — |
| `STATE/pause_unsupported` | Pause is not supported on this platform (Windows) | `NEVER` | `DID_NOT_HAPPEN` | — |
| `STATE/not_attached` | A stdin call without the caller's current attach | `NEVER` | `DID_NOT_HAPPEN` | — |
| `STATE/secrets_unavailable` | A retry needs sealed secret environment values that were purged (terminal state + `storage.secret_retention_hours`), or that the node data key can no longer open because the key is missing or unreadable ([04](../architecture/04-execution.md) §2) | `NEVER` (submit again with the environment) | `DID_NOT_HAPPEN` | `state.reason` = purge time (absent when the key cannot open them) |
| `STATE/in_use` | Referenced by running work, a session or a lease | `AFTER_TIME` | `DID_NOT_HAPPEN` | `state.reason` = holder |
| `STATE/dirty_worktree` | A worktree has uncommitted changes | `NEVER` (archive or commit) | `DID_NOT_HAPPEN` | — |
| `STATE/sas_mismatch` | Pairing digits did not match, or the commitment failed | `NEVER` | `DID_NOT_HAPPEN` | — |
| `STATE/peer_incompatible` | The peer's protocol range does not overlap | `NEVER` | `DID_NOT_HAPPEN` | `upgrade` |
| `STATE/peer_unreachable` | The peer did not answer | `AFTER_TIME` | `DID_NOT_HAPPEN` or `UNKNOWN` | — |
| `STATE/peer_blocked` | Pairing from this node identity is blocked or rate limited | `AFTER_TIME` (1 h) | `DID_NOT_HAPPEN` | — |
| `STATE/link_down` | (retired, [AD-0018](../decisions/AD-0018-native-platforms-without-wsl-integration.md)) The WSL guest link is not connected; never returned | `AFTER_TIME` | `DID_NOT_HAPPEN` | — |
| `STATE/update_in_progress` | An update switch is running | `AFTER_TIME` | `DID_NOT_HAPPEN` | — |
| `STATE/managed_externally` | Updates are managed by a package manager | `NEVER` | `DID_NOT_HAPPEN` | — |
| `STATE/not_activated` | The feature is deployed but not yet activated in production ([10](../architecture/10-cloud.md) §8) | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = surface |
| `STATE/not_signed_in` | The node has no account link | `NEVER` (sign in) | `DID_NOT_HAPPEN` | — |
| `STATE/cloud_unreachable` | The node could not reach the cloud | `AFTER_TIME` | `DID_NOT_HAPPEN` or `UNKNOWN` | — |
| `STATE/purchase_pending` | A Play purchase is `PENDING` and not granted | `AFTER_TIME` | `DID_NOT_HAPPEN` | — |
| `RESOURCE/queue_full` | The admission queue or offer capacity is full (policy limit) | `AFTER_TIME` | `DID_NOT_HAPPEN` | `limit` |
| `RESOURCE/disk_space` | The data volume is below the free-space guard | `AFTER_TIME` | `DID_NOT_HAPPEN` | `limit` |
| `RESOURCE/quota_exceeded` | A hard quota is exceeded | `NEVER` (clean up or raise the quota) | `DID_NOT_HAPPEN` | `limit` |
| `RESOURCE/enforcement_unavailable` | The task requires enforcement the node cannot provide | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` = capability |
| `RESOURCE/rate_limited` | A rate limit applies | `AFTER_TIME` (`retry_at`) | `DID_NOT_HAPPEN` | `limit` |
| `RESOURCE/too_large` | A payload, manifest, plan or transfer exceeds its bound | `NEVER` | `DID_NOT_HAPPEN` | `limit` |
| `RESOURCE/kill_switch_active` | A cloud kill switch disables the feature | `AFTER_TIME` | `DID_NOT_HAPPEN` | `state.reason` = switch |
| `RESOURCE/overloaded` | Temporary overload (D1 overloaded, node command queue full) | `AFTER_TIME` with jitter | `DID_NOT_HAPPEN` | — |
| `EXECUTION/adopt_not_permitted` | The OS refused to place the process under management | `NEVER` | `DID_NOT_HAPPEN` | `state.reason` |
| `EXECUTION/operation_failed` | A node job or OS operation failed | Depends on `effect` | `HAPPENED` or `UNKNOWN` | `state.reason` |
| `EXECUTION/integration_write_failed` | Writing a client configuration file failed; earlier files of the plan were restored | `SAME_COMMAND` | `DID_NOT_HAPPEN` | `state.reason` = path |
| `EXECUTION/provider_error` | A provider API (Google Play, Paddle) failed | `AFTER_TIME` | `UNKNOWN` | — |
| `INTERNAL/internal` | Unexpected failure; the correlation ID is in the node or cloud log. For `PurgeTaskRecord`, a failed or busy post-commit WAL checkpoint reports `HAPPENED`; the logical purge is committed, and identical-command replay reattempts the checkpoint (node-store section 1, MR-14) | `AFTER_TIME` once | `UNKNOWN` unless known | — |
| `INTERNAL/store_corrupt` | The node store failed its integrity check | `NEVER` (doctor; restore from backup) | `DID_NOT_HAPPEN` | — |
