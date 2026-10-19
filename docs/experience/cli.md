# `arcforges` CLI

Architecture: [12](../architecture/12-client-applications.md) §3. Origin:
- `HUMAN` when attached to an interactive terminal and not descended from an agent root;
- `AGENT` under an agent root or with `ARCFORGES_SESSION`;
- `SCRIPT` otherwise ([11](../architecture/11-security-privacy.md) §1).

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

Each row lists the command, its main options, the RPCs it calls and its notes. All mutating commands send a fresh `command_id`. The CLI retries transport failures with the same ID, at most 3 times with jittered backoff.

### C-01 Run and tasks

| Command | Options | RPCs | Notes |
|---|---|---|---|
| `run -- <program> [args]` | `--cwd <dir>` (default: current directory), `--pool`, `--priority`, `--timeout`, `--cpu-limit-time`, `--env K=V` (repeatable), `--env-inherit caller\|node\|none`, `--unset K`, `--stdin none\|file:<path>\|stream`, `--label k=v`, `--title`, `--kind command\|service`, `--ready-regex/--ready-port/--ready-file`, `--side-effect pure\|idempotent\|side-effecting\|unknown`, `--retries n`, `--depends-on <id>[:succeeded\|finished\|ready]`, `--placement local\|any\|<node>`, `--inputs <glob>`, `--outputs <glob>`, `--output-conflict stage\|skip-existing\|fail\|overwrite`, `--exclusive <key>` and `--shared <key>` (repeatable), `--exclusive-workspace`, `--client-timeout <dur>` (hand-off before an AI client's timeout, exit 124), `--join-existing`, `--cpu <cores>`, `--mem <size>`, `--mem-max <size>`, `--require-enforcement cpu,memory`, `--detach`, `--wait <dur>`, `--session <id>`, `--agent <id>`, `--shell bash\|sh\|pwsh\|powershell\|cmd` | `SubmitTask`, then `AttachTask` (attached) or `WaitTask` | Attached by default. stdin is forwarded when `--stdin stream` is set (`WriteTaskInput`, `CloseTaskInput`). `Ctrl+C` once sends `CancelTask`; a second `Ctrl+C` detaches and leaves the task running, printing its ID. |
| `tasks list` | `--state`, `--session`, `--workspace`, `--pool`, `--label`, `--since`, `--mine`, `--limit` | `ListTasks` | — |
| `tasks show <id>` | `--full` | `GetTask` | — |
| `tasks wait <id>` | `--for terminal\|started\|ready`, `--timeout <dur>` (≤ 55 s per call; the CLI loops), `--output tail\|all\|none` (default `tail`) | `WaitTask`, `ReadTaskOutput` | When the task is terminal: prints its output (default the last 4 KiB) and exits with the task's exit code. Exit 9 when the target is not reached before `--timeout`, with the state and queue position on stderr. This is the wait command printed by a hand-off. |
| `tasks attach <id>` | `--from-start` | `AttachTask` | Detaching never stops the task |
| `tasks logs <id>` | `--attempt n`, `--stream stdout\|stderr\|merged`, `--follow`, `--tail <n>` | `ReadTaskOutput`, `WatchTaskOutput` | — |
| `tasks cancel <id>...` | `--reason`, `--grace <dur>` | `CancelTask` | Prompts on a TTY when the tasks belong to others |
| `tasks retry <id>` | `--mem <size>` | `RetryTask` | Warns for side-effecting or unknown classes |
| `tasks priority <id> <class>` | `--pool` | `SetTaskPriority` | — |
| `tasks pause <id>` / `resume <id>` | — | `PauseTask` / `ResumeTask` | Windows prints "pause is not supported on Windows" (exit 1) |
| `tasks pin <id>` / `unpin` | — | `PinTask` | — |
| `tasks purge <id>` | — | `PurgeTaskRecord` | HUMAN only; prompts |
| `tasks timeline <id>` | `--attempt n`, `--samples`, `--processes` | `GetTimeline` | — |
| `tasks attempts <id>` | — | `ListAttempts` | — |

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
| `guests` / `guests link <distro> [--disable]` | `ListGuestLinks` / `SetGuestLink` (host) |
| `guests host` / `guests trust-host <host-node-id>` | `GetHostLink` / `TrustHost` (inside a WSL guest; interactive only). The node refuses a link from a host other than the pinned one; `trust-host` accepts that host, and its next link is pinned as on first use (09 §9). |

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
| `coverage [--session <id>]` | `GetReleaseScope`, then `GetSessionCoverage` when a session is given: the release coverage statement (product definition §9), followed by the session's facts. `session coverage <id>` ends with a pointer to it. |
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
| `account status` | `GetAccountStatus` | — |
| `account login [--device]` | `BeginSignIn`, `GetSignInFlow` | Opens the browser, or prints the code, URL and a terminal QR in device mode |
| `account logout` | `SignOut` | — |
| `account pair-phone` | `CreatePhonePairing`, `GetPhonePairing`, `ConfirmPhonePairing` | Prints a terminal QR, then asks "Allow <model>?" |
| `account cloud-link on\|off` / `account refresh` | `SetCloudLink` / `RefreshEntitlement` | — |
| `lan status` / `lan enable [--port p] [--no-advertise]` / `lan disable` | `GetLanStatus` / `SetLanEnabled` | — |
| `lan peers` / `lan peer <id>` / `lan add <host[:port]>` | `ListPeers` / `GetPeer` / `AddPeerAddress` | — |
| `lan pair <peer>` | `BeginPairing`, `GetPairing`, `ConfirmPairing` | Shows the six digits and asks "Do both screens show 481 290? [y/N]" |
| `lan incoming` / `lan accept <pairing>` / `lan reject <pairing>` | `RespondToPairing` | — |
| `lan policy <peer> [--place-to] [--accept-from] [--cache-read] [--cache-write] [--cpu-share x] [--mem-share x] [--data-out source,outputs,logs] [--require-approval]` | `UpdatePeerPolicy` | — |
| `lan remove <peer> [--block]` | `RemovePeer` | — |
| `integrate <claude-code\|codex> [--scope user\|project\|local] [--project <dir>] [--mcp] [--hooks] [--routing observe\|guide\|rewrite]` | `PlanIntegration` | Prints the plan diff (default: plan only), with the routing statement for the client when the plan enables an MCP or hook route ([AD-0007](../decisions/AD-0007-ai-integration.md) §4; added 2026-10-19) |
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

**Internal roles**, hidden from help: `mcp serve`, `hook <client> <event>`, `bridge wsl`, `node exec-wrap`, `node signal`, `node exit-record`, `node update-rollback`.

## 5. Behaviour details

- **Auto-start.** Any command that needs the node starts it when it is absent ([02](../architecture/02-node-service.md) §3), except inside AI sandboxes or CI, where it prints `arcforges: node not running; start it with 'arcforges node run --background' or the Desktop` and exits 75.
- **Approvals.** On `approval_required` the CLI prints `Waiting for approval <id> (approve in ArcForges Desktop or with 'arcforges approvals approve <id>')` and exits 6. With `--wait-approval <dur>` it polls `GetApproval` and then prints the outcome.
- **Rewritten agent commands.** When the CLI was invoked by a hook rewrite (`--session` with `--attach`), it behaves exactly as the original command would: same stdout, stderr and exit code ([08](../architecture/08-ai-integration.md) §4.1).
- **Accessibility.** Human output never relies on colour alone: states carry words. Tables degrade to `key: value` lines when the terminal width is below 60 columns.
