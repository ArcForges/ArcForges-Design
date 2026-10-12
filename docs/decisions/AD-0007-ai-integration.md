# AD-0007 — AI client integration: MCP first, hooks for identity and routing, honest coverage

- Status: Accepted (2026-10-12)
- Evidence: V-A01–V-A05, A-A01 ([platform verification](../verification/platform-capabilities.md))

## Decision

1. **Primary route: MCP.**
   - `arcforges mcp serve` (stdio) is configured in each AI client and translates MCP tool calls into node gRPC calls ([experience/mcp.md](../experience/mcp.md)). AI clients run MCP servers outside their command sandboxes (V-A03, and Codex's MCP launch), so this route reaches the node even when shell commands cannot.
   - It supports MCP revisions **2025-11-25** (initialize handshake) and **2026-07-28** (stateless, `server/discover`), chosen per request by the client's declared version. Task handles are explicit, server-minted tool arguments.
   - Long work returns within a bounded wait (default 45 s, maximum 55 s) with state, an output tail and the handle. Where a client declares the `io.modelcontextprotocol/tasks` extension, the adapter returns task handles as the extension defines.
2. **Identity through hooks.** The `arcforges hook <client> <event>` handler is configured for:
   - Claude Code: SessionStart, SessionEnd, SubagentStart, SubagentStop, PreToolUse and PostToolUse (Bash), WorktreeCreate and WorktreeRemove;
   - Codex: SessionStart, SessionEnd, SubagentStart, SubagentStop, PreToolUse and PostToolUse.

   It registers the session (`session_id`), subagents (`agent_id`, `agent_type`), the working directory, the transcript path where given, and the **agent process identity** (the hook process's parent PID and start time). On Claude Code it writes `ARCFORGES_SESSION=<id>` to `CLAUDE_ENV_FILE`, so later commands carry the session.
3. **Command routing (opt-in per workspace or client):**

| Mode | Mechanism | Enabled when |
|---|---|---|
| `mcp` | Agent uses `run` and related MCP tools | Always available |
| `rewrite` | PreToolUse returns `allow` with `updatedInput` replacing a matching shell command with `arcforges run --session … --agent … --attach -- <original>` | Only if the per-client **reachability probe** passes inside that client's command environment (A-A01), and policy allows |
| `guide` | PreToolUse denies matching heavy commands with a reason directing the agent to the MCP `run` tool | When rewrite is unavailable and policy prefers guidance |
| `observe` | No routing; heavy unmanaged descendants are recorded and reported | Default for unmatched commands, or when hooks are disabled |

   Matching rules (heavy-command patterns per toolchain adapter) are policy data, editable by the user and per workspace.
4. **Honesty.**
   - Codex hooks fail open, and Claude Code hooks can be disabled by managed settings. The node therefore reports routing as **guardrails**, never as enforcement.
   - Per session it reports which routes were active, the managed and bypassed counts, and unknowns.
   - It never claims the model, thinking state or internal completion status. It shows only client-reported events (session start and end, subagent start and stop, stop events) and its own observations.
5. **Bypass detection.** The node watches descendants of registered agent processes. Heavy unmanaged processes (CPU or memory above the policy threshold, or matching heavy-command patterns) are recorded as `BYPASSED`, with resource usage, as a diagnosis finding. Processes with no attributable ancestry are reported as unattributed.
6. **Configuration consent.**
   - `arcforges integrate <client>` shows the exact file diff before writing. It writes only user-level, project-level or local-level settings that the user selects, never managed or enterprise settings.
   - It preserves unrelated settings and records what it wrote, so it can remove it.
   - It reports conflicts: hooks disabled (`disableAllHooks`, `allowManagedHooksOnly`, `allow_managed_hooks_only`), hooks untrusted (Codex `/hooks`), a sandbox denying IPC, or project instructions that prescribe other build entry points.
   - It never edits a repository's instruction files (AGENTS.md, CLAUDE.md). It offers a snippet the user may add.
7. **Packaging.** Claude Code and Codex plugin packages bundle the MCP configuration, hooks and skills. Installing a plugin never installs or authorizes the native node. The plugin's SessionStart hook detects a missing node and prints install guidance (R-DIST-004).
8. **No self-modification.** Managed tasks cannot write the ArcForges installation directory: Windows uses an ACL deny for the user's own write access on the versioned app directory, inherited by managed jobs; Linux installs files read-only. Policy and configuration changes requested through MCP go through `PolicyService` with approval where the policy demands it (R-AI-009).
