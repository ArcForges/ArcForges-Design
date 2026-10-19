# Journeys

Each journey lists its steps across surfaces with the APIs involved, its success criteria, its main failure branches and how it is verified. **Verification** names the closed-loop test that proves the journey at development stage and, where real-world validation is deferred, the acceptance-register entry (AR-…).

## J-01 Install and connect an AI client

- **Actor.** A developer on Windows with Claude Code (WSL Debian also present).
- **Preconditions.** None.

1. The user downloads the setup program from W-04 and installs it per user. The node starts (13 §3.1). Linux and WSL users use `install.sh`.
2. Desktop D-00 shows the capabilities. In WSL Debian, the guest node is installed by `install.sh` (user action) and linked automatically: SM-GUEST-LINK DISCOVERED → LINKED.
3. In D-14, the user plans the Claude Code integration at user scope (`PlanIntegration`), reviews the diff with the routing statement (routed commands run outside Claude Code's own sandbox; [AD-0007](../decisions/AD-0007-ai-integration.md) §4) and applies it (`ApplyIntegration`).
4. The user runs the probe (`StartProbe`) and pastes the instruction into Claude Code. `arcforges probe` reports PASS (`ReportProbe`).
5. The user selects routing `rewrite` (heavy commands) or `rewrite-all` (every shell command except passthrough patterns) for the workspace (policy). D-14 states that connecting MCP alone routes nothing. A new Claude Code session raises SessionStart (`ReportHookEvent`) and the session appears in D-06.

- **Success:**
  - MCP connected;
  - hooks seen;
  - rewrite active only where the probe passed;
  - coverage visible, with the managed share and what stays unmanaged ([08](../architecture/08-ai-integration.md) §4.4);
  - the release coverage statement on D-14, including its stated limits ([product definition](../product/product-definition.md) §9; added 2026-10-19).
- **Failures:**
  - hooks disabled by managed settings (DEGRADED, conflict shown, MCP-only);
  - the probe fails (rewrite stays off; guide or MCP);
  - no WSL systemd (guest DEGRADED with the remedy).
- **Verification:**
  - closed-loop `J01_IntegrationInstallTests`, using `ScriptedMcpClient` and hook fixtures against real config files in a temporary home directory;
  - real setup-program and `install.sh` tests (13 §9);
  - real Claude Code and Codex probe runs on the workstation (F-A01; recorded evidence);
  - fresh-machine install: AR-01.

## J-02 An agent builds through ArcForges

- **Actor.** Claude Code (agent). Several sessions in parallel, some in the same workspace.

1. The agent calls the MCP `run` tool with `dotnet build` (or a hook rewrites the Bash command into `arcforges run --session … --client-timeout <ms> --join-existing -- dotnet build`).
2. The node persists the task (`SubmitTask`). The adapter classifies `dotnet.build` (side effect `UNKNOWN` by default) and adds the workspace's .NET key. The estimate comes from memory or the adapter. Admission queues the task when budgets are full, or while another task holds a conflicting key: .NET builds in one workspace run one after the other, because each builds the referenced projects too, while a `dotnet test --no-build` runs beside another one. Sessions that build in parallel use separate managed worktrees ([03](../architecture/03-resource-control.md) §4).
3. The task starts in a job or transient unit with limits. NuGet caches are redirected to the shared managed caches, `-m:N` follows the grant, and node reuse is disabled.
4. The agent receives the result within 45 s, or a handle plus `task_wait` (bounded waits), with no retry loops. A rewritten command that is still queued or running shortly before the client's tool timeout hands off: it prints the task ID and `arcforges tasks wait <id>`, exits 124, and the task keeps its place. A resubmission of the same command joins the existing task ([08](../architecture/08-ai-integration.md) §4.1).
5. Records show the timeline (QUEUED_ADMISSION, RESTORE, BUILD), and the session coverage counts it as managed.

- **Success:**
  - admission keeps accounted memory within the budget while 3+ builds run, and the reserve holds under the 15 §4 load as far as the platform enforces it ([03](../architecture/03-resource-control.md) §5.4);
  - concurrent builds in one workspace never write the same project's outputs at the same time;
  - no duplicate package downloads across tasks;
  - exit codes and output are byte-identical to direct runs.
- **Failures:**
  - OOM: a retry with more memory only for tasks asserted PURE or IDEMPOTENT; an `UNKNOWN` build is reported, not retried (AD-0006 §4);
  - the client's tool timeout: hand-off, never cancellation or requeue;
  - a stall finding;
  - the node down: MCP reports `effect` honestly and the CLI exits 75.
- **Verification:**
  - closed-loop `J02_AgentBuildTests` (ScriptedMcpClient plus real `dotnet` and `cargo` builds on Windows and WSL);
  - real enforcement tests (F-W01, F-W02, F-L03);
  - performance tests (15 §4).

## J-03 Run, queue and limit commands without AI

- **Actor.** A developer or automation author.

1. `arcforges run --pool default --mem 4GiB -- npm test`, attached. A second terminal runs three more commands.
2. The queue shows positions and explanations (`queue explain`).
3. The user disables parallelism for the `default` pool (`queue parallelism pool:default off`). Admissions follow one by one.
4. The user cancels one task and retries another. `tasks logs --follow` shows the output.

- **Success:**
  - limits are enforced (or labelled unenforced with the reason);
  - the cancellation tree is cleaned up within the grace period;
  - the exit codes of §3 in [cli.md](cli.md) hold.
- **Verification:** closed-loop `J03_CliQueueTests` (real processes, Windows and WSL); `TestLoad` scenarios.

## J-04 Diagnose slow or stuck work

1. A `dotnet test` hangs with no output.
2. After the stall threshold, the node raises STALL with evidence and collects a tree snapshot automatically.
3. The user opens D-08 (or an agent calls `findings`) and sees the explanation. The user cancels (or approves the agent's cancel request).
4. The waste report (D-19, `report waste`) shows admission wait against execution, idle no-progress and repeated work for the last 7 days.

- **Verification:** closed-loop `J04_DiagnosisTests` with `TestLoad` hang, repeat and stale scenarios; doctor tests.

## J-05 Reclaim disk safely

1. A DISK_PRESSURE finding is raised (or the user opens D-11).
2. Analyze → plan (low-risk regenerable outputs, per-task restores, abandoned clean worktrees).
3. The user executes. Items are re-validated and quarantined. One item is IN_USE, so the plan ends PARTIAL.
4. The user restores one item from quarantine. The other items are purged after 24 h.

- **Failures:**
  - the volume reaches `LOW`: new tasks that write there wait (`disk_space`);
  - it reaches `CRITICAL`: running writers are frozen or stopped with `DISK_LIMIT`, and the store reserve keeps the node's records writable ([06](../architecture/06-storage-workspaces.md) §5);
  - a dirty worktree is archived and verified before removal, never removed with changes ([06](../architecture/06-storage-workspaces.md) §3).

- **Verification:** closed-loop `J05_CleanupTests` on real directory trees, with junctions and symlinks, open files and dirty worktrees (T-04). The bounds (10,000 items / 2 TiB) are tested with synthetic plans.

## J-06 Pair a machine on the LAN

- **Actors.** A user with a workstation and a build box.

1. Both nodes enable LAN (D-15). The build box is DISCOVERED through DNS-SD, or added by address.
2. Pair: SAS digits are shown on both, both users confirm, and the peer is PAIRED (pinned) with a status-only policy.
3. The user widens the policy: place-to on the workstation, accept-from on the build box. No account or subscription is involved.

- **Failures:** a digit mismatch, which aborts with MISMATCH; expiry; blocked after 5 failures; incompatible versions.
- **Verification:**
  - closed-loop `J06_PairingTests` with two or three real node processes on one machine (loopback, real TLS);
  - mDNS on a physical LAN with two physical machines: AR-03.

## J-07 Place work on another node

1. A task with `placement=ANY` is submitted on the workstation. Scoring prefers the build box (an idle queue and a warm sccache).
2. Offer, then accept. The executor pulls the inputs into a workspace slot leased by this attempt, runs the task and streams its output. The workstation shows a REMOTE attempt. A second placement from the same workspace gets its own slot.
3. The outputs return. The workstation applies the declared outputs against the digests recorded at submission. A file that changed locally meanwhile is staged beside it and raises `OUTPUT_CONFLICT` ([09](../architecture/09-lan.md) §6).
4. The workstation disconnects mid-run. The build box finishes and retains. On reconnect the origin collects the results.

- **Verification:**
  - closed-loop `J07_PlacementTests` (multi-node on one machine, real transfers, lease expiry, executor preemption, the node's compiler-cache store reading through to a peer, with a real sccache client);
  - a physical LAN: AR-03.

## J-08 Subscribe

1. Web: W-24, then Paddle-hosted checkout, then return. A webhook sets the subscription ACTIVE, and the nodes receive updated entitlement tokens within 60 s.
2. Android: A-08, then Play purchase, then `SubmitPlayPurchase`, verification and acknowledgement, then ACTIVE.
3. Lifecycle: payment failure (PAYMENT_ISSUE), recovery, cancellation (CANCELED_ACTIVE), expiry, refund (REVOKED).

- **Verification:**
  - closed-loop `J08_CommerceTests` with `FakePaddle` signed webhook fixtures, `FakePlayDeveloperApi` and RTDN fixtures, against the local Cloud host and D1;
  - real Paddle checkout: AR-05; real Play purchase: AR-06.

## J-09 Remote status and actions

1. Away from the desk, the user opens W-40 or A-03. Live summaries arrive through the relay.
2. A push reports "Approval needed: Codex wants to cancel npm test" (FCM).
3. The user opens it, steps up and approves (when the node allows remote approvals), or cancels the task (MEDIUM).
4. The node verifies the signature, expiry and local policy, executes, and returns a signed result. The cloud records the outcome.

- **Failures:**
  - the node offline (the command EXPIRES and never executes late);
  - the node rejects by policy (REJECTED_BY_NODE);
  - kill switch active (summaries only).
- **Verification:**
  - closed-loop `J09_RemoteTests`: real node and C# host, Worker and Durable Object in local workerd, a scripted viewer;
  - `FakeFcm`;
  - push delivery to a physical device: AR-07; Android on a physical phone: AR-08.

## J-10 Operate, support and enforce limits

1. A budget reaches 80%, raising an operator alert. The operator views W-66, including the residual daily exposure.
2. At 100% the degradation ladder applies the step for that dimension, for example live streaming off; if it persists, existing relay sockets are closed; at 120% the service enters essential-only mode. Summaries continue where the step allows, and local work is unaffected ([14](../architecture/14-commercial-operations.md) §7.3).
3. A support case arrives with a consented bundle. The operator requests access, the user allows it, the operator reads it, and the read is audited.
4. A refund is decided (Paddle) and the entitlement is revoked.

- **Verification:**
  - closed-loop `J10_OperationsTests` (budgets and kill switches against the local Cloud stack; operator flows through `OperatorService`);
  - runbook review;
  - production alerting configuration: AR-09.

## J-11 Agent worktrees, subagents and temporary files

- **Actor.** Claude Code (agent) with subagents.

1. The agent creates a managed worktree with the MCP `worktree_create` tool ([06](../architecture/06-storage-workspaces.md) §3).
2. A subagent builds and tests there through rewritten commands. Each task carries the subagent's agent ID, so the session's records separate its work from the agent's own.
3. Each attempt gets its own `tmp/<attempt>` as TMP, TEMP and TMPDIR, under the per-attempt limit ([06](../architecture/06-storage-workspaces.md) §4, §5). It is deleted when the attempt ends; a failed attempt's directory is kept 24 h when `keep_failed_tmp` is set.
4. The agent removes the worktree, which has uncommitted changes, with `worktree_remove` and `archive=true`. The user approves; the archive is verified before anything is removed ([06](../architecture/06-storage-workspaces.md) §3). Later the user restores it with `arcforges worktree restore <id>`.
5. The session report lists the subagent's tasks with its agent ID.

- **Success:**
  - subagent work runs under the same admission, keys, limits and records as the agent's own;
  - no temporary directory outlives its retention;
  - the restored worktree matches the archived state byte for byte.
- **Failures:**
  - Codex subagent work cannot be attributed and is labelled unknown;
  - archiving is refused while a merge or rebase is in progress;
  - ignored files such as `.env` are archived only when included, never discarded.
- **Verification:**
  - closed-loop `J11_WorktreeSubagentTests` (`HookPayloadFixtures` for subagent events, real git worktrees on Windows and WSL);
  - the archive round trip (L-19).
