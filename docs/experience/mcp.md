# MCP adapter tools

Architecture: [08](../architecture/08-ai-integration.md) §2; decision [AD-0007](../decisions/AD-0007-ai-integration.md).

- **Server.** `arcforges mcp serve` (stdio), server name `arcforges` (or `arcforges-node` on a name conflict).
- **Protocol revisions.** 2025-11-25 and 2026-07-28.
- **Origin.** `AGENT`. The session is correlated by the adapter's parent process ([08](../architecture/08-ai-integration.md) §3.2).

## 1. Server metadata

- **`serverInfo`:** `{name: "arcforges", title: "ArcForges", version: <product version>}`.
- **Capabilities:**
  - `tools` with `listChanged: false`;
  - no resources, prompts, sampling, roots or elicitation;
  - the `io.modelcontextprotocol/tasks` extension, advertised only when the client declares it.
- **`instructions`** (returned at initialize or discover):

  > ArcForges runs build, test and other heavy commands under shared CPU and memory limits on this machine and keeps their logs. Use `run` instead of starting such commands directly. `run` waits up to 45 seconds. If the task is still running, call `task_wait` with the returned `task_id`, and never start the same command again. Use `explain_wait` when a task is queued.

## 2. Conventions

- **IDs.** Task, attempt, approval, plan and workspace IDs are lower-case Crockford base32 strings (26 characters).
- **Results.**
  - Every result has `content` (a short text summary for the model) and `structuredContent` (the JSON object below).
  - `outputSchema` is declared for every tool.
  - On 2026-07-28, results carry `resultType: "complete"`.
- **Errors** follow [08](../architecture/08-ai-integration.md) §2.3: `isError: true`, `structuredContent.error` = the `ArcError` JSON, and the content states `effect`.
  - `approval_required` is not an error. The tool returns `state: "WAITING_APPROVAL"` with `approval_id` and `next_actions: ["approval_status"]`.
- **Bounded waits.** `wait_seconds` is at most 55 (default 45), so a tool call never approaches client timeouts. Progress notifications are sent at most every 2 s when the client supplied a `progressToken`.
- **Annotations** per tool (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) are listed below.

## 3. Tools

### M-01 `run`

Submit a command and wait (bounded) for its completion. The tool's description says that commands it runs execute outside the client's own sandbox, with resource control and records ([08](../architecture/08-ai-integration.md) §1; added 2026-10-19).

Input schema:

```json
{
  "type": "object",
  "properties": {
    "command": {"type": "string", "description": "Shell command line, run with the client's shell semantics"},
    "argv": {"type": "array", "items": {"type": "string"}, "minItems": 1, "description": "Program and arguments (alternative to command)"},
    "cwd": {"type": "string", "description": "Absolute working directory"},
    "shell": {"type": "string", "enum": ["bash", "sh", "pwsh", "powershell", "cmd"]},
    "wait_seconds": {"type": "integer", "minimum": 0, "maximum": 55, "default": 45},
    "title": {"type": "string", "maxLength": 200},
    "priority": {"type": "string", "enum": ["high", "normal", "low", "background"], "default": "normal"},
    "pool": {"type": "string"},
    "timeout_seconds": {"type": "integer", "minimum": 1, "maximum": 2592000},
    "env": {"type": "object", "additionalProperties": {"type": "string"}},
    "kind": {"type": "string", "enum": ["command", "service"], "default": "command"},
    "ready": {"type": "object", "properties": {"regex": {"type": "string"}, "port": {"type": "integer"}, "file": {"type": "string"}}},
    "side_effect": {"type": "string", "enum": ["pure", "idempotent", "side_effecting", "unknown"], "default": "unknown"},
    "depends_on": {"type": "array", "items": {"type": "string"}, "maxItems": 64},
    "placement": {"type": "string", "enum": ["local", "any"], "default": "local"},
    "inputs": {"type": "object", "properties": {"include": {"type": "array", "items": {"type": "string"}, "maxItems": 256}, "exclude": {"type": "array", "items": {"type": "string"}, "maxItems": 256}}, "description": "Workspace-relative globs sent to a remote node (placement any)"},
    "outputs": {"type": "array", "items": {"type": "string"}, "maxItems": 256, "description": "Workspace-relative paths or globs returned from a remote node"},
    "output_conflict": {"type": "string", "enum": ["stage", "skip_existing", "fail"], "default": "stage"},
    "async": {"type": "boolean", "default": false, "description": "Return immediately (tasks extension when supported)"}
  },
  "required": ["cwd"],
  "oneOf": [{"required": ["command"]}, {"required": ["argv"]}]
}
```

Output (`structuredContent`):

```json
{
  "task_id": "01j9…", "attempt_id": "01j9…",
  "state": "SUCCEEDED | FAILED | CANCELLED | LOST | RUNNING | QUEUED | WAITING_DEPENDENCY | PLACING | PAUSED | RETRY_WAIT | WAITING_APPROVAL",
  "exit_code": 0, "termination_reason": "EXITED",
  "tail": "last 4 KiB of merged output", "tail_truncated": true,
  "elapsed_seconds": 251,
  "timeline_summary": [{"category": "QUEUED_ADMISSION", "seconds": 12}, {"category": "BUILD", "seconds": 230}],
  "queue": {"position": 2, "blocking_reason": "budget_memory", "eta_seconds": 180},
  "approval_id": null,
  "next_actions": ["task_wait", "task_output", "task_cancel"],
  "warnings": ["Pause is not supported on Windows"]
}
```

- **Mapping:** `TaskService.SubmitTask`, then `WaitTask(wait_seconds, tail_bytes = 4096)`.
- **Command form.** `command` uses the `SHELL` form with the client's shell; `argv` uses the `ARGV` form.
- **Environment.** `inherit=CALLER` with the adapter's environment, which is the client's environment.
- **Placement `any`.** `PlacementSpec.inputs` is required for remote execution. The adapter derives it safely when `inputs` is omitted:
  - In a **git workspace**, `inputs = {include: ["**"]}` under the manifest rule of [09](../architecture/09-lan.md) §6, which takes only tracked files and untracked files that are not ignored.
  - In a **non-git directory**, the call fails with `VALIDATION/inputs_required`, because a walk of everything could send secrets or huge trees.
  - **Outputs** default to none: a remote run then returns its exit code, records and logs, and writes no local files. Declared outputs return with `output_conflict` (default `stage`). `overwrite` is not offered to agents.
- **Side-effect assertions.** `side_effect` values `pure` and `idempotent` from an agent take effect only when the policy `retry_safety.accept_agent_assertions` is true. Otherwise the task records `unknown` and the result carries a warning ([AD-0006](../decisions/AD-0006-execution-semantics.md) §4).
- **Annotations:** `readOnlyHint: false`, `destructiveHint: true`, `idempotentHint: false`, `openWorldHint: true`.

### M-02 … M-19

| ID | Tool | Input (required **bold**) | Output | RPCs | Hints (RO / destr. / idem.) |
|---|---|---|---|---|---|
| M-02 | `task_status` | **task_id** | Task summary: state, exit code, timeline summary, queue, approval | `GetTask` | RO |
| M-03 | `task_wait` | **task_id**, `wait_seconds` ≤ 55, `for` = terminal\|started\|ready, `tail_bytes` ≤ 65,536 | As `run` | `WaitTask` | RO |
| M-04 | `task_output` | **task_id** or **attempt_id**, `stream` = merged\|stdout\|stderr, `from_offset`, `max_bytes` ≤ 65,536, `tail` (bool), `raw` (bool: keep ANSI escapes) | `{text, next_offset, eof, truncated, encoding: "utf-8 (invalid bytes replaced)"}` | `ReadTaskOutput` | RO |
| M-05 | `task_cancel` | **task_id**, `reason` | `{state, approval_id?}` | `CancelTask` | destructive, idempotent |
| M-06 | `task_list` | `state[]`, `mine` (default true), `limit` ≤ 100 | Task summaries | `ListTasks` | RO |
| M-07 | `task_retry` | **task_id**, `reason` | `{state, warnings, approval_id?}` | `RetryTask` | destructive |
| M-08 | `queue_status` | — | Pools, budget summary, waiting count, positions of the session's tasks | `GetQueue` | RO |
| M-09 | `explain_wait` | **task_id** | AdmissionExplanation (text plus numbers) | `ExplainTask` | RO |
| M-10 | `resources` | — | Capacity, budgets, pressure, enforcement capabilities with reasons | `GetResourceSnapshot` | RO |
| M-11 | `memory_query` | **command** or **argv**, **cwd** | Facts (duration, peak memory, failure signatures) and the admission estimate | `QueryFacts` | RO |
| M-12 | `findings` | `task_id`, `scope` = session\|node (default session), `include_resolved` | Findings with explanations and available actions | `ListFindings` | RO |
| M-13 | `session_coverage` | — | The current session's coverage, labelled as observed facts, plus `release_scope`: the release coverage statement (product definition §9), whose rows include the routing statement for the session's client: commands routed through ArcForges execute outside the client's own sandbox, with resource control and records (added 2026-10-19) | `GetSessionCoverage`, `GetReleaseScope` | RO |
| M-14 | `worktree_create` | **workspace** (path or ID), `branch`, `base_ref`, `name` | `{workspace_id, path, state}`; waits up to 55 s for ACTIVE | `CreateWorktree`, `GetJob` | not RO, not destructive |
| M-15 | `worktree_remove` | **workspace_id**, `archive` (bool), `include_ignored` (bool; agents can include ignored files such as `.env` in the archive, never discard them) | `{state, approval_id?}` | `RemoveWorktree` | destructive |
| M-16 | `cleanup_plan` | `classes[]`, `max_risk` (default low), `workspace` | Plan: items, sizes, risks, digest, expiry | `AnalyzeStorage` (if no recent analysis), `PlanCleanup` | not RO, not destructive |
| M-17 | `cleanup_execute` | **plan_id**, **digest**, `item_ids[]` | `{state, outcomes[], approval_id?}`. Approval is required unless policy `cleanup.agent_execute=LOW_RISK_ONLY` and every item is low risk. | `ExecuteCleanup` | destructive |
| M-18 | `doctor` | `areas[]` | Checks with status and remedies. The HUMAN-only host-posture check is listed without status or values ([07](../architecture/07-records-diagnosis-memory.md) §2.4): the tool returns no host-posture value (added 2026-10-19) | `RunDoctor` | RO |
| M-19 | `approval_status` | **approval_id**, `wait_seconds` ≤ 55 | `{state, outcome?}` | `GetApproval` (polled within the bound) | RO |

The adapter exposes **no** tools for policy changes, integration changes, pairing, account, update or adoption. Those operations are HUMAN-only or approval-gated and remain in the Desktop and CLI. This keeps agent capabilities explicit (R-AI-009).

## 4. Tasks extension mapping

When the client declares `io.modelcontextprotocol/tasks`:

| Request | Mapping |
|---|---|
| `run` with `async: true` | Returns a task handle per the extension, with the ArcForges `task_id` as the handle ID |
| `tasks/get` | `GetTask` and `WaitTask(0)`, mapped to the extension's status values: running, completed, failed, cancelled. For a terminal task the response carries the final `run` output; the 2026-07-28 extension has no `tasks/result` (V-A01). |
| `tasks/cancel` | `CancelTask` |
| `tasks/update` (input) | `WriteTaskInput` for STREAM stdin, through the adapter's own attach (below) |

**Stdin for async runs.** When `run` starts a STREAM-stdin task with `async: true`, the adapter opens `AttachTask(task_id, want_stdin=true)` and keeps that attach, and its `attach_id`, for the life of the MCP session. `tasks/update` then calls `WriteTaskInput(task_id, attach_id, data, offset)`, where the adapter tracks the offset. When the MCP session ends, the attach drops and the task sees end-of-file on stdin, as with any detach (AD-0006 §7).

Without the extension, `async: true` returns at once with `state` and `next_actions`.

## 5. Accessibility of results

Model-facing text is plain, with no ANSI colour and no tables wider than 100 characters. Output tails strip ANSI escape sequences in `content` but keep them in `task_output` when `raw: true` is requested.
