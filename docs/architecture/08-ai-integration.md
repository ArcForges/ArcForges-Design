# 08 — AI client integration

Decision: [AD-0007](../decisions/AD-0007-ai-integration.md). Tool catalogue and schemas: [experience/mcp.md](../experience/mcp.md).

## 1. Components

| Component | Role |
|---|---|
| `arcforges mcp serve` | MCP server over stdio (a local HTTP transport is roadmap RM-05). It connects to the local node as client kind `MCP_ADAPTER` and serves tools that map one-to-one onto node RPCs. |
| `arcforges hook <client> <event>` | Reads the client's hook JSON from stdin, calls `SessionService`, and writes the client's expected JSON to stdout. Latency target: p95 ≤ 50 ms ([15](15-performance-targets.md)). |
| `arcforges integrate <client>` | Plans, applies and removes client configuration (`IntegrationService`) |
| Node `SessionService` | Session and subagent registry, process roots, routing decisions, coverage |

**What connecting does.** Adding the MCP server only *offers* tools; it intercepts nothing. Shell commands an agent runs are managed only when hooks route them (`rewrite` or `rewrite-all`, §4.1) or when the agent chooses the `run` tool. §4.4 lists what each route covers, and coverage (§5) measures the rest.

## 2. MCP adapter

### 2.1 Protocol handling

- **2025-11-25 clients:** the `initialize` handshake stores the negotiated version and capabilities for the connection.
- **2026-07-28 clients** (V-A01): every request carries its `_meta` protocol version and capabilities, and the adapter answers `server/discover` with supported versions `["2026-07-28", "2025-11-25"]`, capabilities and `serverInfo`.
- Tool results always carry `resultType: "complete"` (2026-07-28). The adapter never uses server-initiated requests (sampling, roots, elicitation), so the Multi Round-Trip Request pattern is not needed.
- `tools/list` is deterministic and returns `ttlMs` = 300,000 with `cacheScope: "private"`.
- If the client supports `notifications/progress` (it sent a `progressToken`), progress notifications are sent on the request's response stream at most every 2 s.

### 2.2 Task handles and bounded waits

- `run` submits with `owner=session`, then waits through `TaskService.WaitTask` for `wait_seconds` (default 45, maximum 55). It returns `{task_id, attempt_id, state, exit_code?, tail (last 4 KiB merged), timeline_summary, next_actions}`.
- If the task is still running, `next_actions` lists `task_wait`, `task_output` and `task_cancel` with the handle. Handles are server-minted IDs (Crockford base32 of the 16-byte UUIDv7).
- **Tasks extension.** When the client declares `io.modelcontextprotocol/tasks` in its capabilities extensions, `run` with `async=true` returns a task handle per the extension, mapped to the same node task. `tasks/get` maps to `GetTask` and `WaitTask(0)` and carries the final output once the task is terminal. `tasks/update` maps to `WriteTaskInput` for STREAM stdin, through an attach the adapter holds ([MCP](../experience/mcp.md) §4).
- A broken response stream (2026-07-28 has no resumability) loses only the response. The node task continues, and the agent re-queries by handle.

### 2.3 Error mapping

| Node `ArcError` | MCP response |
|---|---|
| `VALIDATION`, `AUTHORIZATION`, `STATE`, `CONFLICT` | Tool result `isError: true`. Content holds the message key, a human message and `effect`. `structuredContent.error` holds the `ArcError` JSON. |
| `RESOURCE` (admission queue full, quota) | Same, with retry advice |
| Transport failure to the node (node down) | Tool result `isError: true`, `effect: "DID_NOT_HAPPEN"` when nothing was submitted, with guidance to start the node. If the submission's command ID may have been accepted, the adapter re-queries by command ID before answering, so it never reports a false "did not happen" |

## 3. Session identity

### 3.1 Sources

| Source | Data | Trust |
|---|---|---|
| SessionStart hook (Claude Code, Codex) | `session_id`, `cwd`, `transcript_path`, `model` (Codex), source, `permission_mode`; the **agent process root** is the nearest ancestor of the hook process that is a known client executable: hooks run in exec form, and the handler walks up past any shell (A-A02) | Client-asserted fields; the agent root is verified by the node (it exists, the same user owns it, and its start time matches) |
| SubagentStart/Stop hooks | `agent_id`, `agent_type`, parent `session_id` | Client-asserted |
| PreToolUse/PostToolUse hooks | `tool_name`, `tool_input` (command, `timeout`), `tool_use_id`, `permission_mode`; `agent_id` inside a Claude Code subagent (Codex sends `agent_id` only on Subagent events) | Client-asserted |
| Worktrees | Session `cwd` and `git worktree list` of registered workspaces. WorktreeCreate/Remove hooks are never configured, because they replace the client's own worktree handling (V-A02). | Observed |
| MCP adapter hello | Adapter PID and its nearest client-executable ancestor (the AI client process; usually the direct parent), `clientInfo` (name, version) from `initialize` or `_meta` | Verified PIDs; `clientInfo` client-asserted |
| `ARCFORGES_SESSION` environment variable (Claude Code through `CLAUDE_ENV_FILE`) | Session ID on CLI calls made by Bash commands | Client-carried |

### 3.2 Correlation rules

1. A session is created by SessionStart, or by the first MCP call whose adapter's client ancestor matches no session. The latter gets `source=MCP_ONLY` with a synthetic session ID and the client name.
2. MCP calls are attributed to the session whose agent root equals the adapter's client ancestor (PID and start time). Several concurrent sessions of the same client therefore stay separate, because each spawns its own stdio server.
3. Subagent attribution:
   - Claude Code hook-routed commands carry `--agent <agent_id>`. Codex commands cannot be attributed to subagents (its PreToolUse carries no `agent_id`), and coverage says so.
   - MCP calls cannot be attributed to subagents unless the client sends an agent identifier in `_meta`, which no supported client does at design time. MCP work is then attributed to the session with `agent=UNKNOWN`, and coverage says so (R-AI-007).
4. Process-tree attribution: descendants of a session's agent root belong to the session. Descendants of a subagent cannot be separated by ancestry, because subagents run in-process, so they are attributed to the session only.
5. The session ends on SessionEnd, when the agent root process exits, or after 24 h of inactivity. Services with `stop_with_session` stop then.

## 4. Routing

### 4.1 Decision procedure (PreToolUse on shell tools)

`SessionService.ClassifyCommand(session, agent, command, cwd)` returns `{decision, rewritten_command?, reason}`:

1. Unless the workspace's routing policy enables routing, the decision is `ALLOW_UNCHANGED` (observe).
2. **Which commands are routed** depends on the mode (patterns are policy data):
   - **`rewrite` (heavy commands).** Heavy patterns, by default:
     - `dotnet (build|test|publish|pack|restore)`, `msbuild`;
     - `cargo (build|test|check|clippy|bench|doc)`;
     - `cmake --build`, `ninja`, `make`, `ctest`;
     - `npm (ci|install|test|run build)`, `pnpm (install|test|build)`;
     - `pytest`, `gradle`.
   - **`rewrite-all` (managed-command mode).** Every shell command, including scripts and data-processing pipelines, except the **passthrough patterns** (`routing.passthrough_patterns`). By default these are:
     - navigation and reads: `cd`, `pwd`, `ls`, `dir`, `cat`, `type`, `head`, `tail`, `echo`, `which`, `where`, `env`;
     - read-only git: `status`, `diff`, `log`, `show`, `branch`, `rev-parse`;
     - searches: `rg`, `grep`, `find` without `-exec` or `-delete`;
     - `arcforges` itself;
     - interactive programs that need a terminal (editors, pagers, REPLs, `top`).

     A compound command line (pipes, `&&`, loops) is routed whole, as one shell script, unless every part is passthrough, with these rules:
     - **Shell state stays with the client.** A leading chain of `cd`, `pushd`, `export`, `set`, `unset` and `source` segments is kept outside the routed part, so the client's shell changes directory and environment as before (`cd src && make` becomes `cd src && arcforges run … -- make`). State changes inside the routed part affect only that part, as in a subshell.
     - **Background processes are not routed.** A line that starts a process in the background (a trailing `&`, `nohup`, `disown`, `setsid`, `start /b`) runs unchanged and is observed, because a task's processes end with the task. Long-running services use the MCP `run` tool with `kind=service`.
     - **Light commands.** A routed command that no adapter classifies and no operational-memory fact describes is admitted with the light estimate (`source=LIGHT`: `routing.light_cpu_millicores`, default 250, and `routing.light_mem_bytes`, default 128 MiB) instead of the generic default, outside pool parallelism limits and reservations (memory admission and the global running limit still apply). Its memory ceiling is not derived from the light guess ([03](03-resource-control.md) §3), so a script that needs gigabytes is not killed for exceeding a guess. Its observed peak counts at once (accounted memory), and operational memory learns it.

   Commands that are not routed are `ALLOW_UNCHANGED`.
3. Rewrite, when the mode is `rewrite` or `rewrite-all` and the client's reachability probe is `PASS` for this environment (§4.2). The command becomes:

   `arcforges run --session <sid> [--agent <aid>] --attach --cancel-when-gone --client-timeout <ms> --join-existing --title "<summary>" --shell <client-shell> -- <original command string>`

   The rewrite passes no `--cwd`: the CLI runs in the client's shell and uses that shell's current directory, which is the client's working directory, or the directory a kept `cd` prefix moved to.

   `--client-timeout` is the client's tool timeout for this call: `tool_input.timeout` (Claude Code) or `timeout_ms` (Codex) when present, else the client default, which the integration probe records per client version (F-A01; 120,000 ms for Claude Code Bash). A call that runs in the background (Claude Code `run_in_background`) has no tool timeout: the rewrite then omits `--client-timeout`, the run stays attached until the task ends, and stopping the background shell cancels the task.

   - **Quoting.** The original string is passed verbatim as one argument to the client's own shell (bash on Linux and Git Bash on Windows for Claude Code; the Codex shell), so quoting and semantics are preserved. Output and exit code are byte-identical in attached mode ([04](04-execution.md) §5).
   - **Permission.** The hook returns `updatedInput.command` with `permissionDecision: "ask"` by default. The client shows the rewritten command, and the user's deny and ask rules are evaluated against it (V-A02). `"allow"` is used only when the session runs in `bypassPermissions`, or when a HUMAN sets `routing.rewrite_permission=ALLOW`. That setting pre-approves every routed command, and the integration page warns that deny rules written for the original command no longer match the rewritten form.
     - In `rewrite-all` mode the default `ask` means a confirmation for every routed command. D-14 says so when the mode is chosen; unattended managed-command mode needs `routing.rewrite_permission=ALLOW` (with the warning) or a `bypassPermissions` session.
     - Codex has no `ask` decision (V-A04). Codex rewrites therefore happen only with `routing.rewrite_permission=ALLOW`; otherwise the Codex integration uses `guide`, which denies the heavy patterns only, while other commands run unchanged and are observed. The coverage report says which applies.
   - **Hand-off before the client's timeout.** A task may wait in the queue or run longer than the tool call allows, and first runs have no duration estimate. The rewritten run therefore never relies on finishing in time:
     1. `--cancel-when-gone` binds the task to the CLI process (`SubmitTaskRequest.cancel_when_caller_gone`).
     2. At `client-timeout − min(routing.handoff_margin_ms, client-timeout / 2)` (margin default 15 s), if the task is not finished, the CLI calls `TaskService.ReleaseCallerBinding` and prints, on stderr: `arcforges: task <id> is <queued at position n | running>; it continues. Get the result with: arcforges tasks wait <id> --timeout <s> (or the MCP task_wait tool). Cancel it with: arcforges tasks cancel <id>`, where `<s>` is the same budget in seconds. It exits with code 124.
     - A task that admission classes `exceeds_capacity` can never start on this node, so the CLI does not wait for the hand-off: it cancels the task at once, prints the explanation, and exits with 125 (not started).
     3. The task keeps its queue position and keeps running. Each later `tasks wait` call stays within the tool timeout, and returns the task's output tail and exit code once it is terminal.
   - **Interrupts and explicit cancellation.** If the client kills the CLI *before* the hand-off (the user interrupted it), the binding is still in force and the node cancels the task within 5 s, as the original command would have stopped. After the hand-off the task is a persistent handle: interrupting a later `tasks wait` stops the waiting, not the task. The user cancels it explicitly with `arcforges tasks cancel <id>`, on D-03, or by asking the agent, whose `task_cancel` call cancels its own session's task.
   - **No duplicate requeues.** `--join-existing` lets a resubmission by the same session join an existing task instead of queueing a second copy (`SubmitTaskResponse.joined`; `routing.join_existing_rewrites`, default true). The match is exact: the same command digest (program and arguments, or the shell string), working directory, environment digest and stdin. Only a task that has **not started** is joined, because it has read no input yet and cannot return stale results. A resubmission while the identical task is already running starts a new task, so an agent that edited files after the hand-off always gets a run that includes its changes; the CLI says that the identical task is still running and names it.
     - The CLI prints `arcforges: joined task <id> (queued at position n | running since <time>)`, replays the task's output from the start, and follows it.
     - A joined submission binds its caller like a new one: an interrupt before its own hand-off cancels the task.
   - **Known long work.** If operational memory expects the command to run longer than the client's tool timeout, the decision is `DENY_WITH_GUIDANCE` towards the MCP `run` tool with `async` (`routing.guide_when_longer_than_client_timeout`, default true). The hand-off covers everything the estimate cannot know: first runs and queue waits.
4. `DENY_WITH_GUIDANCE`, when the mode is `guide`: deny with the reason text "This command is resource-managed. Use the `run` tool of the `arcforges` MCP server with the same command and working directory." The model sees the reason, and the decision is recorded.
5. Hook failures fail open: the client proceeds unchanged (Codex documents this; Claude Code proceeds on hook errors other than exit code 2). Coverage counts them as `ROUTE_FAILED`.

### 4.2 Reachability probe (A-A01)

`arcforges integrate <client> --probe` and Desktop "Test integration":
1. Write a one-shot probe instruction file, then ask the user to run, inside the client, the documented probe prompt "Run `arcforges probe --token <t>` and report the output". Alternatively, run the client non-interactively where it supports it, with the user's consent.
2. `arcforges probe` connects to the node and reports the sandbox signals it observes (environment markers, a failed connection with its errno).
3. The node stores `probe_result{client, environment (OS, WSL distro, sandbox mode), result PASS|FAIL_CONNECT|FAIL_NOT_FOUND, at}`.

Rewrite is enabled only for environments with `PASS`, and the probe is re-run after client version changes or settings changes detected by `IntegrationService` (file watchers on the client's settings files).

### 4.3 Observe mode and bypass detection

PostToolUse hooks record executed heavy commands that were not routed (`BYPASSED_COMMAND`). The resource monitor flags heavy unmanaged descendants of agent roots (`UNMANAGED_HEAVY`). Both feed coverage and findings (R-AI-006).

### 4.4 What each route covers

| Operation | How it can be managed | What remains unmanaged (observed and reported) |
|---|---|---|
| Shell-tool commands (Claude Code Bash, Codex shell) | Hooks in `rewrite` (heavy patterns) or `rewrite-all` (everything except passthrough); for Codex only with `routing.rewrite_permission=ALLOW`, otherwise `guide` | Commands when hooks are disabled, untrusted or failed (`ROUTE_FAILED`); passthrough commands by design |
| Scripts and data-processing commands (`python`, `node`, shell scripts, `ffmpeg`, `jq`) | `rewrite-all`, or the agent's `run` tool (argv or shell form), or `arcforges run` in the script | In `rewrite` mode they are not heavy patterns: observed, and flagged when they cross the bypass thresholds |
| Long, queued or unknown-duration work | `run` with `async`; rewritten runs hand off (§4.1) | — |
| Worktrees | `worktree_create` / `worktree_remove` (MCP), `arcforges worktree` (CLI): managed, with locks and archives | Worktrees the client creates itself (Claude Code `--worktree`, subagent isolation): observed through the session's `cwd` and `git worktree list`, registered as workspaces when `auto_register` is on |
| Directories | Every session's working directory inside a git repository is registered as a workspace (`auto_register`), so keys, caches and records apply to routed work there | Writes by unmanaged processes |
| Client-internal tools (file read, edit, search, web fetch) | Not processes; outside ArcForges' scope | Not counted as bypass |
| Processes the client starts itself (MCP servers, IDE tasks, language servers) | Not routed | Observed as unmanaged descendants of the agent root; heavy ones are flagged |
| Processes started inside a managed task | Managed (same container) | Escapes through WMI or breakaway are detected (`ESCAPED`) |

**Non-shell operation adapters** are the MCP tools of [mcp.md](../experience/mcp.md) (M-01 to M-19): `run` in argv form (no shell), task status, waits, output, cancellation and retries, queue explanations, operational-memory queries, worktree creation and removal, cleanup plans and the doctor. Each calls the same node services as the CLI, so permissions, keys and records apply equally.

ArcForges never claims that connecting MCP, or any single route, manages everything. The session coverage report (§5) shows the managed share. The operations release 1 manages are listed in the [product definition](../product/product-definition.md) §9; routing operations that clients start outside their shell tool is roadmap RM-12.

## 5. Coverage

`SessionCoverage` per session:
- `routes`: MCP connected (yes/no); hooks seen per event kind; rewrite mode active; probe result;
- `managed_tasks`: count, CPU-seconds, wall time;
- `managed_share`: managed CPU-seconds as a share of all CPU-seconds attributed to the session (managed, bypassed and attributed unmanaged), so the effect of the chosen mode is visible;
- `handoffs` and `joined`: rewritten runs that handed off before the client's timeout, and submissions that joined an existing task;
- `bypassed`: commands seen through PostToolUse, plus heavy processes by ancestry, with CPU-seconds and peak memory;
- `unattributed_heavy`: node-wide heavy unmanaged processes with no session ancestry;
- `unknowns`: subagent attribution of MCP work, model and thinking state (never available), hooks failed or disabled;
- `client_events`: the last client-reported events (session start and end, subagent start and stop, stop).

The UI and MCP present coverage as observed facts with these labels, never as completeness (R-AI-007).

## 6. Configuration management

### 6.1 Files written (with consent; R-AI-008)

**Claude Code**
- *MCP server:* user scope via `claude mcp add --scope user arcforges -- arcforges mcp serve` when the CLI is available; otherwise the user-scope configuration file entry. Project scope (`.mcp.json`) only when the user selects it.
- *Hooks:* `~/.claude/settings.json` (user) or `.claude/settings.local.json` (local), hook entries for the events in [AD-0007](../decisions/AD-0007-ai-integration.md) §2 in exec form: `{"type": "command", "command": "<absolute path to arcforges>", "args": ["hook", "claude-code", "<event>"]}` (no shell; the minimum Claude Code version supporting `args` is recorded by AF-AI-02). Never WorktreeCreate or WorktreeRemove.
- *Never written:* managed settings.
- *Plugin alternative:* a marketplace plugin with `hooks/hooks.json`, `.mcp.json` and a skill describing ArcForges usage.

**Codex**
- *MCP server:* `~/.codex/config.toml` `[mcp_servers.arcforges]`, `command = "arcforges"`, `args = ["mcp","serve"]`, or the project `.codex/config.toml` when the user selects it (it loads only for trusted projects).
- *Hooks:* `~/.codex/hooks.json` or the project hooks file, plus the trust step shown to the user ("run `/hooks` in Codex to trust ArcForges hooks"). Codex SessionEnd and interrupt hooks run with short default timeouts (about 1 s), so the handler only records and returns.
- *Never written:* `requirements.toml` (managed).

### 6.2 Conflicts detected and reported (never auto-resolved)

| Conflict | Detection | Consequence shown |
|---|---|---|
| Hooks disabled | Claude `disableAllHooks`; managed `allowManagedHooksOnly`; Codex `[features] hooks=false`; `allow_managed_hooks_only` | Routing unavailable; MCP-only |
| Hooks untrusted (Codex) | Trust state not readable; inferred when no SessionStart is ever received after configuration | Prompt to trust; MCP-only until then |
| Sandbox denies IPC | Probe FAIL_CONNECT | Rewrite disabled; guide or MCP |
| Project instructions prescribe other entry points | Text scan of AGENTS.md/CLAUDE.md for build-command directives (report only) | Note shown; ArcForges does not override |
| Another MCP server named `arcforges` | Configuration parse | Plan proposes `arcforges-node` as the name |
| Existing hook entries for the same events | Configuration parse | Plan appends; never removes the user's hooks |

### 6.3 Instruction snippet

The integration offers an optional snippet for the user to add to project instructions, never written automatically. Its text follows the routing mode:

- **`rewrite` or `guide`:**
  > Builds, tests and restores in this repository run through ArcForges. Use the `arcforges` MCP tools `run`, `task_wait` and `task_output` for them, or let the hooks route them. Do not start them in the background yourself. ArcForges queues them under shared CPU and memory limits and keeps the logs. Do not modify ArcForges itself.
- **`rewrite-all`:**
  > Commands in this repository run through ArcForges: the hooks route every shell command except simple reads. If a command reports that its task continues, wait for it with `arcforges tasks wait <id>` or the MCP `task_wait` tool; never start it again. For long work, use the MCP `run` tool with `async`. Do not modify ArcForges itself.
- **MCP only (hooks unavailable):**
  > Run builds, tests, scripts and other heavy commands with the `arcforges` MCP `run` tool instead of the shell. ArcForges cannot see commands started directly.

## 7. Non-goals and limits

- **Session scope.** ArcForges does not intercept commands of clients it is not configured for, or of sessions started before the hooks were installed.
- **No transcripts.** It never reads transcripts by default. The `transcript_path` is stored only as a pointer for the user's own navigation.
- **No hidden state.** It does not claim the model's internal state, plan or completion. A client's Stop event is shown as "client reported stop".
