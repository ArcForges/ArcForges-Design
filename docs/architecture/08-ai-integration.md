# 08 — AI client integration

Decision: [AD-0007](../decisions/AD-0007-ai-integration.md). Tool catalogue and schemas: [experience/mcp.md](../experience/mcp.md).

## 1. Components

| Component | Role |
|---|---|
| `arcforges mcp serve` | MCP server (stdio; optionally Streamable HTTP on `127.0.0.1` with a bearer token). It connects to the local node as client kind `MCP_ADAPTER` and serves tools that map one-to-one onto node RPCs. |
| `arcforges hook <client> <event>` | Reads the client's hook JSON from stdin, calls `SessionService`, and writes the client's expected JSON to stdout. Latency target: p95 ≤ 50 ms ([15](15-performance-targets.md)). |
| `arcforges integrate <client>` | Plans, applies and removes client configuration (`IntegrationService`) |
| Node `SessionService` | Session and subagent registry, process roots, routing decisions, coverage |

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
- **Tasks extension.** When the client declares `io.modelcontextprotocol/tasks` in its capabilities extensions, `run` with `async=true` returns a task handle per the extension, mapped to the same node task. `tasks/get` maps to `GetTask` and `WaitTask(0)`, and `tasks/update` maps to `WriteTaskInput` for STREAM stdin.
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
| SessionStart hook (Claude Code, Codex) | `session_id`, `cwd`, `transcript_path`, `model` (Codex), source; the hook process's parent PID and start time = **agent process root** | Client-asserted; the agent root is verified by the node (the PID exists, the same user owns it, and its start time matches) |
| SubagentStart/Stop hooks | `agent_id`, `agent_type`, parent `session_id` | Client-asserted |
| PreToolUse/PostToolUse hooks | `tool_name`, `tool_input` (commands), `tool_use_id`, `agent_id` when inside a subagent | Client-asserted |
| WorktreeCreate/Remove (Claude Code) | Worktree paths | Client-asserted; matched to workspaces |
| MCP adapter hello | Adapter PID, parent PID (the AI client process), `clientInfo` (name, version) from `initialize` or `_meta` | Verified PIDs; `clientInfo` client-asserted |
| `ARCFORGES_SESSION` environment variable (Claude Code through `CLAUDE_ENV_FILE`) | Session ID on CLI calls made by Bash commands | Client-carried |

### 3.2 Correlation rules

1. A session is created by SessionStart, or by the first MCP call whose adapter parent PID matches no session. The latter gets `source=MCP_ONLY` with a synthetic session ID and the client name.
2. MCP calls are attributed to the session whose agent root PID equals the adapter's parent PID (and start time). Several concurrent sessions of the same client therefore stay separate, because each spawns its own stdio server.
3. Subagent attribution:
   - Hook-routed commands carry `--agent <agent_id>`.
   - MCP calls cannot be attributed to subagents unless the client sends an agent identifier in `_meta`, which no supported client does at design time. MCP work is then attributed to the session with `agent=UNKNOWN`, and coverage says so (R-AI-007).
4. Process-tree attribution: descendants of a session's agent root belong to the session. Descendants of a subagent cannot be separated by ancestry, because subagents run in-process, so they are attributed to the session only.
5. The session ends on SessionEnd, when the agent root process exits, or after 24 h of inactivity. Services with `stop_with_session` stop then.

## 4. Routing

### 4.1 Decision procedure (PreToolUse on shell tools)

`SessionService.ClassifyCommand(session, agent, command, cwd)` returns `{decision, rewritten_command?, reason}`:

1. Unless the workspace's routing policy enables routing, the decision is `ALLOW_UNCHANGED` (observe).
2. The adapter classification matches heavy patterns, which are policy data. Defaults:
   - `dotnet (build|test|publish|pack|restore)`, `msbuild`;
   - `cargo (build|test|check|clippy|bench|doc)`;
   - `cmake --build`, `ninja`, `make`, `ctest`;
   - `npm (ci|install|test|run build)`, `pnpm (install|test|build)`;
   - `pytest`, `gradle`.

   Non-matching commands are `ALLOW_UNCHANGED`.
3. Rewrite, when the mode is `rewrite` and the client's reachability probe is `PASS` for this environment (§4.2). The command becomes:

   `arcforges run --session <sid> [--agent <aid>] --attach --title "<summary>" --cwd "<cwd>" --shell <client-shell> -- <original command string>`

   The original string is passed verbatim as one argument to the client's own shell (bash on Linux and Git Bash on Windows for Claude Code; the Codex shell), so quoting and semantics are preserved. Output and exit code are byte-identical in attached mode ([04](04-execution.md) §5). The hook returns `permissionDecision: "allow"` with `updatedInput.command` (V-A02, V-A04).
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

## 5. Coverage

`SessionCoverage` per session:
- `routes`: MCP connected (yes/no); hooks seen per event kind; rewrite mode active; probe result;
- `managed_tasks`: count, CPU-seconds, wall time;
- `bypassed`: commands seen through PostToolUse, plus heavy processes by ancestry, with CPU-seconds and peak memory;
- `unattributed_heavy`: node-wide heavy unmanaged processes with no session ancestry;
- `unknowns`: subagent attribution of MCP work, model and thinking state (never available), hooks failed or disabled;
- `client_events`: the last client-reported events (session start and end, subagent start and stop, stop).

The UI and MCP present coverage as observed facts with these labels, never as completeness (R-AI-007).

## 6. Configuration management

### 6.1 Files written (with consent; R-AI-008)

**Claude Code**
- *MCP server:* user scope via `claude mcp add --scope user arcforges -- arcforges mcp serve` when the CLI is available; otherwise the user-scope configuration file entry. Project scope (`.mcp.json`) only when the user selects it.
- *Hooks:* `~/.claude/settings.json` (user) or `.claude/settings.local.json` (local), hook entries for the events in [AD-0007](../decisions/AD-0007-ai-integration.md) §2 with command `arcforges hook claude-code <event>`.
- *Never written:* managed settings.
- *Plugin alternative:* a marketplace plugin with `hooks/hooks.json`, `.mcp.json` and a skill describing ArcForges usage.

**Codex**
- *MCP server:* `~/.codex/config.toml` `[mcp_servers.arcforges]`, `command = "arcforges"`, `args = ["mcp","serve"]`, or the project `.codex/config.toml` when the user selects it (it loads only for trusted projects).
- *Hooks:* `~/.codex/hooks.json` or the project hooks file, plus the trust step shown to the user ("run `/hooks` in Codex to trust ArcForges hooks").
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

The integration offers an optional snippet for the user to add to project instructions, never written automatically:

> Builds and tests in this repository run through ArcForges. Use the `arcforges` MCP tools `run`, `task_wait` and `task_output` for build, test and restore commands. Do not start them directly. ArcForges queues them under shared CPU and memory limits and keeps the logs. Do not modify ArcForges itself.

## 7. Non-goals and limits

- **Session scope.** ArcForges does not intercept commands of clients it is not configured for, or of sessions started before the hooks were installed.
- **No transcripts.** It never reads transcripts by default. The `transcript_path` is stored only as a pointer for the user's own navigation.
- **No hidden state.** It does not claim the model's internal state, plan or completion. A client's Stop event is shown as "client reported stop".
