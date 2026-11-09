# `arcforges` CLI

Architecture: [12](../architecture/12-client-applications.md) §3. Origin:
- `HUMAN` when attached to an interactive terminal and not descended from an agent root;
- `AGENT` under an agent root or with `ARCFORGES_SESSION`;
- `SCRIPT` otherwise ([11](../architecture/11-security-privacy.md) §1).

**Delivered and bounded by [AD-0021](../decisions/AD-0021-central-access-go-center.md) §4–§5.** AF-CTR-04 delivered `login [--device-code]`, `logout [--local]`, `center show`, `center set <url> | --default` and `account status` (ArcForges #69). AF-CTR-05 N3 (ArcForges #75) routes `run`, `tasks` list/show/wait/cancel and `output` through the local Fleet proxy and configured center; `--node` defaults to this installation's node. `run --local` is a labelled HUMAN diagnostic. Other task commands remain local unless separately delivered. LAN commands remain out of current delivery.

## 1. Grammar and global options

```
arcforges [global options] <group> <command> [arguments] [options]
arcforges run [run options] -- <program> [args...]
arcforges run [run options] --shell <kind> -- "<script>"
```

| Global option | Meaning |
|---|---|
| `--json` | Machine output: one JSON document (protobuf JSON mapping), or JSON Lines for streams |
| `--quiet`, `-q` | Only essential output (IDs, the task's own output for `run`) |
| `--no-color` | Disable colour (also when `NO_COLOR` is set or stdout is not a TTY) |
| `--yes`, `-y` | Answer yes to local confirmation prompts. Node permissions and approvals still apply. |
| `--timeout <dur>` | Client deadline for unary calls (default: the method deadline) |
| `--verbose`, `-v` | Show correlation IDs and timings |
| `--help`, `-h` / `--version` | Help / version |

- **Durations** use `90s`, `5m`, `2h` or `1d`. **Sizes** use `512MiB` or `4GiB`. **CPU** values like `2` or `1.5` are cores, converted to millicores.
- **IDs** accept the full base32 ID or any unique prefix of at least 6 characters.

## 2. Output

| Mode | Behaviour |
|---|---|
| Human | Width-aware tables, colour only on a TTY, relative times. Errors go to stderr as `error: <message> (<CATEGORY>/<code>, correlation <id>)`. |
| `--json` | stdout carries only JSON. Errors print as `{"error": <ArcError JSON>}` on stdout, with the exit code of §3. |
| `run` (attached) | The task's stdout and stderr are mirrored byte-exactly to the CLI's stdout and stderr. ArcForges messages go to stderr prefixed `arcforges:`, and only when `--verbose` is set or something fails. |

## 3. Exit codes

| Code | Meaning | Applies to |
|---|---|---|
| 0 | Success | All |
| 1 | Operation failed (error printed) | All except `run` |
| 2 | Usage error (invalid arguments) | All |
| 3 | Node already running | `node run` |
| 4 | Not found | Lookups |
| 5 | Permission denied | All |
| 6 | Approval pending (approval ID printed; `--wait-approval` waits) | Mutations |
| 7 | Conflict (revision, already exists, digest) | Mutations |
| 8 | Entitlement required | Gated features |
| 9 | Wait ended without reaching the target state | `tasks wait`, `run --detach --wait <dur>` |
| 124 | `run --client-timeout`: the run handed off before the client's timeout; the task continues (task ID, wait command and cancel command on stderr). A task that itself exits with 124 prints no hand-off line. | `run` (attached) |
| 75 | Node unreachable and nothing was submitted (`EX_TEMPFAIL`, effect `DID_NOT_HAPPEN`) | All |
| `run` only: task exit code 0–255 | The task's exit code; signals map to 128 + n on Linux | `run` (attached) |
| `run` only: 125 | Not started: validation, permission, approval or queue refusal (message on stderr) | `run` |
| `run` only: 126 | Spawn failed: the program could not be executed | `run` |
| `run` only: 127 | Program not found | `run` |

## 4. Commands

Each row lists the command, its main options, the RPCs it calls and its notes. Mutating commands use a fresh `command_id` for the user action. The local command retry policy allows at most three transport retries; routed mutations have the distinct bounded same-command policy below.

### C-01 Run and tasks

| Command | Options | RPCs | Notes |
|---|---|---|---|
| `run -- <program> [args]` | `--cwd <dir>` (default: current directory), `--pool`, `--priority`, `--timeout`, `--cpu-limit-time`, `--env K=V` (repeatable), `--env-inherit caller\|node\|none`, `--unset K`, `--stdin none\|file:<path>\|stream`, `--label k=v`, `--title`, `--kind command\|service`, `--ready-regex/--ready-port/--ready-file`, `--side-effect pure\|idempotent\|side-effecting\|unknown`, `--retries n`, `--depends-on <id>[:succeeded\|finished\|ready]`, `--placement local\|any\|<node>`, `--inputs <glob>`, `--outputs <glob>`, `--output-conflict stage\|skip-existing\|fail\|overwrite`, `--exclusive <key>` and `--shared <key>` (repeatable), `--exclusive-workspace`, `--client-timeout <dur>` (hand-off before an AI client's timeout, exit 124), `--join-existing`, `--cpu <cores>`, `--mem <size>`, `--mem-max <size>`, `--require-enforcement cpu,memory`, `--detach`, `--wait <dur>`, `--session <id>`, `--agent <id>`, `--shell bash\|sh\|pwsh\|powershell\|cmd` | `SubmitTask`, then `AttachTask` (attached) or `WaitTask` | Attached by default. stdin is forwarded when `--stdin stream` is set (`WriteTaskInput`, `CloseTaskInput`). `Ctrl+C` once sends `CancelTask`; a second `Ctrl+C` detaches and leaves the task running, printing its ID. |
| `tasks list` | `--state`, `--session`, `--workspace`, `--pool`, `--label`, `--since`, `--mine`, `--limit` | `ListTasks` | — |
| `tasks show <id>` | `--full` | `GetTask` | — |
| `tasks wait <id>` | `--for terminal\|started\|ready`, `--timeout <dur>` (≤ 55 s per call; the CLI loops), `--output tail\|all\|none` (default `tail`) | `WaitTask`, `ReadTaskOutput` | When the task is terminal: prints its output (default the last 4 KiB) and exits with the task's exit code. Exit 9 when the target is not reached before `--timeout`, with the state and queue position on stderr. This is the wait command printed by a hand-off. |
| `tasks attach <id>` | `--from-start` | `AttachTask` | Detaching never stops the task |
| `tasks logs <id>` | `--attempt n`, `--stream stdout\|stderr\|merged`, `--follow`, `--tail <n>` | `ReadTaskOutput`, `WatchTaskOutput` | — |
| `output <id>` | `--node <name-or-uuid>`, `--local`, `--stream stdout\|stderr\|merged`, `--from-offset <n>`, `--follow` | local `ReadTaskOutput` or routed `ReadNodeTaskOutput` | Reads from a resumable byte offset; `--json` emits JSON Lines |
| `tasks cancel <id>...` | `--reason`, `--grace <dur>` | `CancelTask` | Prompts on a TTY when the tasks belong to others |
| `tasks retry <id>` | `--mem <size>` | `RetryTask` | Warns for side-effecting or unknown classes |
| `tasks priority <id> <class>` | `--pool` | `SetTaskPriority` | — |
| `tasks pause <id>` / `resume <id>` | — | `PauseTask` / `ResumeTask` | Windows prints "pause is not supported on Windows" (exit 1) |
| `tasks pin <id>` / `unpin` | — | `PinTask` | — |
| `tasks purge <id>` | — | `PurgeTaskRecord` | HUMAN only; prompts |
| `tasks timeline <id>` | `--attempt n`, `--samples`, `--processes` | `GetTimeline` | — |
| `tasks attempts <id>` | — | `ListAttempts` | — |

**Routed execution details (AF-CTR-05 N3).** `run`, `tasks` list/show/wait/cancel and `output` accept `--node <name-or-uuid>` or `--local`, never both. A canonical nonzero UUID is taken directly; a name must exactly and uniquely match the account's node name. Without either option the target is this node, reached through the center. `tasks attach`, `tasks logs` and the other task controls in the table remain local; routed `run` follows output by offset instead of a local attach stream. For another node, `--cwd` is required and it, `--stdin file:` and `--ready-file` must be absolute target paths; POSIX, Windows drive-absolute and UNC forms are passed unchanged for validation on the target. Routed `--stdin stream` is not available.

The CLI sets `EnvironmentSpec.inherit` to NODE by default for routed `run`, and to CALLER for `--local`; an explicit choice is honored, not silently filtered. This CLI override is separate from the unchanged Contracts comment on `EnvironmentSpec.inherit`. Before requesting a relay nonce or sending a Submit, the local proxy examines the original environment wire fields. For this node it refuses carried values whose names match either default or current local secret-name patterns; it fails closed if the policy cannot be read or interpreted. For another node it refuses all caller/set environment values because the target's custom patterns are unknown; NODE or NONE without carried values remains available. Unknown environment or map-entry fields are refused; unrelated protobuf fields keep normal pass-through. These guarantees concern environment values, not an exhaustive classifier for argv, output or other payloads.

A routed mutation retries at most five times within two minutes using the original command ID and inner request bytes. An explicit `--wait-approval` is a separate human wait; an approval on this node restarts that transport clock. When a mutation may have run, the CLI retains and prints its command ID and warns against a new submission; an interrupted in-flight mutation or pending approval receives the same uncertainty warning as delivered in [ArcForges #76](https://github.com/ArcForges/ArcForges/pull/76). `replay_window_passed` also means an earlier attempt may have run, even though the current delivery did not; `replay_digest_differs` is a defect and is not retried as a new command. A local proxy that is not signed in or whose center/channel is unavailable before a routed call reports exit 4; a target `node_offline` with DID_NOT_HAPPEN reports 75. Failure to reach the local node itself has its own connection-error mapping. Owner-device and hosted routed acceptance remains NOT PROVEN; local and synthetic test results do not prove it.

### C-02 Queue

| Command | RPCs |
|---|---|
| `queue show [--pool p]` | `GetQueue` |
| `queue explain <task>` | `ExplainTask` |
| `queue pools` | `ListPools` |
| `queue pool create <name> [--weight n] [--max auto\|n] [--priority c]` / `update` / `delete` | `CreatePool` / `UpdatePool` / `DeletePool` |
| `queue pause [<pool>\|--all]` / `queue resume ...` | `PausePool` / `ResumePool` |
| `queue parallelism <global\|pool:p\|workspace:w\|session:s> <auto\|n\|off>` | `SetParallelism` |

### C-03 Resources and processes

| Command | RPCs |
|---|---|
| `resources [--watch [--interval 5s]]` | `GetResourceSnapshot` / `WatchResources` |
| `ps [--label managed,escaped,bypassed,unmanaged,guest,shared] [--session s] [--top n]` | `ListProcesses` |
| `samples [--attempt id] [--range 1h]` | `GetSamples` |
| `adopt <pid> [--title t] [--pool p]` | `AdoptProcess` (HUMAN only) |
| `terminate <pid> [--reason r]` | `TerminateProcess` |

### C-04 Policy

| Command | RPCs | Notes |
|---|---|---|
| `policy show [--section s]` | `GetPolicy` | JSON in `--json` |
| `policy edit` | `GetPolicy`, `ValidatePolicy`, `UpdatePolicy` | Opens `$EDITOR` on the protobuf JSON, validates and applies with expected_rev |
| `policy apply <file.json>` / `policy validate <file.json>` | `UpdatePolicy` / `ValidatePolicy` | — |
| `policy revisions` / `policy restore <rev>` | `ListPolicyRevisions` / `RestorePolicyRevision` | — |
| `policy explain <operation> --origin agent\|script\|remote` | `ExplainPermission` | — |
| `policy defaults` | `GetDefaultPolicy` | — |

### C-05 Workspaces

| Command | RPCs |
|---|---|
| `workspace list` / `show <id\|path>` | `ListWorkspaces` / `GetWorkspace` |
| `workspace register <path> [--name n]` / `unregister <id>` | `RegisterWorkspace` / `UnregisterWorkspace` |
| `workspace routing <id> <inherit\|observe\|guide\|rewrite\|rewrite-all>` | `UpdateWorkspaceSettings` |
| `workspace concurrency <id> <inherit\|adapter-keys\|serial\|shared>` | `UpdateWorkspaceSettings` |
| `worktree create <workspace> [--branch b] [--base ref] [--name n]` | `CreateWorktree` (prints the path when ready) |
| `worktree remove <id> [--archive] [--ignored include\|discard]` | `PlanWorktreeRemoval`, then `RemoveWorktree`. With `--archive`: snapshot, bundle and verification before removal. Ignored files outside regenerable outputs are listed and need `--ignored include`, or `--ignored discard` with a typed confirmation (HUMAN only). Unmerged entries or dirty submodules refuse the removal. |
| `worktree archives [--workspace <id>]` / `worktree restore <archive-id> [--branch b]` | `ListWorktreeArchives` / `RestoreWorktree` |

### C-06 Storage and caches

| Command | RPCs |
|---|---|
| `storage summary` / `storage dirs [--root r]` | `GetStorageSummary` / `ListManagedDirectories` |
| `storage analyze [--root r] [--workspace w] [--wait]` / `storage analysis <id>` | `AnalyzeStorage` / `GetStorageAnalysis` |
| `storage plan [--analysis id] [--class c] [--max-risk low] [--item id...]` | `PlanCleanup` (prints the plan and its digest) |
| `storage add-path <plan> <path>` | `AddExternalPath` (HUMAN; prompts twice) |
| `storage execute <plan> [--item id...]` | `ExecuteCleanup` (shows the plan and prompts) |
| `storage cancel <plan>` | `CancelCleanupPlan` |
| `storage quarantine` / `storage restore <plan> <item>` | `ListQuarantine` / `RestoreQuarantine` |
| `storage relocate <root> <path>` | `UpdateRoot` |
| `storage pin <dir-id>` / `unpin` | `SetDirectoryPinned` |
| `cache list` / `cache report [--days n]` / `cache verify <id>` / `cache set <id> [--quota s] [--lan on\|off]` | `ListCaches` / `GetCacheReport` / `VerifyCache` / `UpdateCacheSettings` |

### C-07 Toolchains, sessions, findings, approvals, memory

| Command | RPCs |
|---|---|
| `toolchain list [--kind k]` / `detect` / `adapters` / `preview -- <cmd>` | `ListToolchains` / `DetectToolchains` / `ListAdapters` / `PreviewInvocation` |
| `session list` / `show <id>` / `coverage <id>` / `end <id>` | `ListSessions` / `GetSession` / `GetSessionCoverage` / `EndSession` |
| `coverage [--session <id>]` | `GetReleaseScope`, then `GetSession` and `GetSessionCoverage` when a session is given (`GetSession` names the session's client): the release coverage statement (product definition §9), whose routing rows carry each client's routing statement and, when a session is given, mark the row of the session's client (added 2026-10-19), followed by the session's facts. `session coverage <id>` ends with a pointer to it. |
| `findings list` / `show <id>` / `ack <id>` / `mute <id> [--for 7d]` / `remedy <id> <action>` | `ListFindings` / `GetFinding` / `AcknowledgeFinding` / `MuteFinding` / `ApplyRemedy` |
| `approvals list` / `show <id>` / `approve <id>` / `deny <id> [--comment c]` / `withdraw <id>` | `ListApprovals` / `GetApproval` / `DecideApproval` / `CancelApproval` |
| `memory list` / `show <id>` / `query -- <cmd>` / `forget <id>... \| --project p` | `ListFacts` / `GetFact` / `QueryFacts` / `ForgetFacts` |

### C-08 Diagnostics, support, events, jobs

| Command | RPCs |
|---|---|
| `doctor [--area a]` | `RunDoctor` (exit 1 when any check fails) |
| `report waste\|capacity\|cache\|disk\|session <id> [--days n]` | `GetReport` |
| `export [--days n] [--types t] [--task id...] [--session s] [--include-output]` | `ExportRecords` |
| `support bundle create [--days n] [--task id] [--include-output]` / `show <id>` / `list` / `upload <id> --case c\|--new "subject"` / `delete <id>` | `CreateSupportBundle` / `GetSupportBundle` / `ListSupportBundles` / `UploadSupportBundle` (prints the file list and asks for consent) / `DeleteSupportBundle` |
| `events [--topic t...] [--since cursor]` | `Subscribe` (JSON Lines) |
| `jobs list` / `show <id>` / `cancel <id>` | `ListJobs` / `GetJob` / `CancelJob` |

### C-09 Account, LAN, integrations, updates

| Command | RPCs | Notes |
|---|---|---|
| `login [--device-code]` (hidden alias `account login [--device]`) | `BeginSignIn`, `GetSignInFlow`, `CancelSignIn` | Delivered (AF-CTR-04, ArcForges #69). The browser method asks the node to open the browser on its computer and prints the URL to open there if it does not; the device-code method (`--device-code`, and by default over SSH or on Linux without a graphical session) prints the URL, the code and the complete URL. Both print the center's host and the node key's full fingerprint: the browser method asks to compare it with the page, and the device-code method also names its last group, which the `/activate` page asks for. No terminal QR (decision Q19). Success prints "Signed in as <name> (<masked e-mail>) at <host>." Exit 0 when signed in; 1 when denied, expired, failed or cancelled elsewhere; 5 for a caller without an interactive terminal; 130 on Ctrl+C or SIGTERM, which cancel the flow at the node. `--json` prints JSON Lines |
| `logout [--local]` (hidden alias `account logout`) | `SignOut` | Delivered (ArcForges #69). Ends the credential at the center, then on the node; `--local` forgets it on this node only (the center keeps it until it expires or the device is revoked on the web). `logout --local --json` abandons a stranded link only with `--yes` |
| `account status` | `GetAccountStatus` | Delivered (ArcForges #69) |
| `center show` | `GetNodeSettings`, `GetAccountStatus` | Delivered (ArcForges #69). Prints the configured center (or that none is set) and, when the node is signed in at another center, that one too. It shows no "is default" flag: the contract has no field for it |
| `center set <url> \| --default` | `GetNodeSettings`, `UpdateNodeSettings` (`center_url`) | Delivered (ArcForges #63 for the setting, #69 for the command). HUMAN only, with no approval path. The URL is https, or http only for `localhost`, `127.0.0.1` or `[::1]`, accepted only as written. Refused while the node is signed in or signing in (`STATE/invalid_state`, exit 1). `--default` returns to the official center (refused under `--test-mode`) |
| `account pair-phone` | `CreatePhonePairing`, `GetPhonePairing`, `ConfirmPhonePairing` | Prints a terminal QR, then asks "Allow <model>?" |
| `account cloud-link on\|off` / `account refresh` | `SetCloudLink` / `RefreshEntitlement` | — |
| `lan status` / `lan enable [--port p] [--no-advertise]` / `lan disable` | `GetLanStatus` / `SetLanEnabled` | — |
| `lan peers` / `lan peer <id>` / `lan add <host[:port]>` | `ListPeers` / `GetPeer` / `AddPeerAddress` | — |
| `lan pair <peer>` | `BeginPairing`, `GetPairing`, `ConfirmPairing` | Shows the six digits and asks "Do both screens show 481 290? [y/N]" |
| `lan incoming` / `lan accept <pairing>` / `lan reject <pairing>` | `RespondToPairing` | — |
| `lan policy <peer> [--place-to] [--accept-from] [--cache-read] [--cache-write] [--cpu-share x] [--mem-share x] [--data-out source,outputs,logs] [--require-approval]` | `UpdatePeerPolicy` | — |
| `lan remove <peer> [--block]` | `RemovePeer` | — |
| `integrate <claude-code\|codex> [--scope user\|project\|local] [--project <dir>] [--mcp] [--hooks] [--routing observe\|guide\|rewrite]` | `PlanIntegration` | Prints the plan diff (default: plan only), with the client's routing statement (the Stated limit text of its routing row, product definition §9) when the plan enables an MCP or hook route ([AD-0007](../decisions/AD-0007-ai-integration.md) §4; added 2026-10-19) |
| `integrate <client> --apply` | `PlanIntegration`, `ApplyIntegration` | HUMAN only; shows the diff and prompts |
| `integrate <client> --remove [--apply]` | `PlanRemoval`, `ApplyIntegration` | — |
| `integrate <client> --probe` / `integrate status` / `integrate <client> --snippet` | `StartProbe`, `ListProbeResults` / `ListClients` / `GetInstructionSnippet` | — |
| `probe --token <t>` | `ReportProbe` | Run inside the AI client (prints the observations) |
| `update status` / `check` / `apply` / `postpone <dur>` / `rollback` | `GetUpdateStatus` / `CheckNow` / `ApplyNow` / `Postpone` / `Rollback` | — |

### C-10 Node and configuration

| Command | RPCs / behaviour |
|---|---|
| `status` | `Hello`, `GetNodeInfo`, `GetResourceSnapshot` summary |
| `node run [--background] [--systemd]` | Runs the node role (exit 3 if already running) |
| `node stop [--cancel-running] [--timeout d]` / `node wait-ready [--timeout d]` | `StopNode` / polls the endpoint |
| `node info` / `node health` / `node capabilities [--reevaluate]` / `node rename <name>` | `GetNodeInfo` / `GetHealth` / `GetCapabilities` / `RenameNode` |
| `node wipe --scope records\|caches\|all` | `WipeNode` (HUMAN; asks for the node name) |
| `node self-test [--staged] [--demo]` | Local platform self-test without the endpoint (installer and updater use) |
| `config list` / `config get <key>` / `config set <key> <value>` | `GetNodeSettings` / `UpdateNodeSettings` |
| `ui` | Starts or activates ArcForges Desktop |
| `completion bash\|zsh\|fish\|pwsh` | Prints a completion script |
| `version` | Client and node versions, contract versions |

**Internal roles**, hidden from help: `mcp serve`, `hook <client> <event>`, `node exec-wrap`, `node signal`, `node exit-record`, `node update-rollback`.

## 5. Behaviour details

- **Auto-start.** Any command that needs the node starts it when it is absent ([02](../architecture/02-node-service.md) §3), except inside AI sandboxes or CI, where it prints `arcforges: node not running; start it with 'arcforges node run --background' or the Desktop` and exits 75.
- **Approvals.** On `approval_required` the CLI prints `Waiting for approval <id> (approve in ArcForges Desktop or with 'arcforges approvals approve <id>')` and exits 6. With `--wait-approval <dur>` it polls `GetApproval` and then prints the outcome.
- **Rewritten agent commands.** When the CLI was invoked by a hook rewrite (`--session` with `--attach`), it behaves exactly as the original command would: same stdout, stderr and exit code ([08](../architecture/08-ai-integration.md) §4.1).
- **Sign-in with an unreadable secret store** (AF-CTR-04, ArcForges #69). While the node's secret store or its link file cannot be read, `login` and both `logout` forms refuse and change nothing (`STATE/invalid_state`, `signed_out`, `credential_store_unavailable`). They name the way out for a store that stays unreadable: revoke this node on the account's devices page (`/account/devices` on the center), then stop the node and remove `run/cloud-link.json` from its data root.
- **The browser the node opens.** On Linux the node starts it with `xdg-open`, so that browser runs inside the node's systemd unit, and a node restart or update closes it (a residual; NOT PROVEN by any test, ArcForges #69). Under `--test-mode` the node starts no OS handler.
- **Text from the center** (errors, flow failures, the account's name and e-mail address) reaches the terminal only as plain text: control and format characters are replaced.
- **Accessibility.** Human output never relies on colour alone: states carry words. Tables degrade to `key: value` lines when the terminal width is below 60 columns.
