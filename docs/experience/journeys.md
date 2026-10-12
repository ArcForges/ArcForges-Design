# Journeys

Each journey lists its steps across surfaces with the APIs involved, its success criteria, its main failure branches and how it is verified. **Verification** names the closed-loop test that proves the journey at development stage and, where real-world validation is deferred, the acceptance-register entry (AR-…).

## J-01 Install and connect an AI client

- **Actor.** A developer on Windows with Claude Code (WSL Debian also present).
- **Preconditions.** None.

1. The user downloads the setup program from W-04 and installs it per user. The node starts (13 §3.1). Linux and WSL users use `install.sh`.
2. Desktop D-00 shows the capabilities. In WSL Debian, the guest node is installed by `install.sh` (user action) and linked automatically: SM-GUEST-LINK DISCOVERED → LINKED.
3. In D-14, the user plans the Claude Code integration at user scope (`PlanIntegration`), reviews the diff and applies it (`ApplyIntegration`).
4. The user runs the probe (`StartProbe`) and pastes the instruction into Claude Code. `arcforges probe` reports PASS (`ReportProbe`).
5. The user selects routing REWRITE for the workspace (policy). A new Claude Code session raises SessionStart (`ReportHookEvent`) and the session appears in D-06.

- **Success:**
  - MCP connected;
  - hooks seen;
  - rewrite active only where the probe passed;
  - coverage visible.
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

- **Actor.** Claude Code (agent). Several sessions in parallel.

1. The agent calls the MCP `run` tool with `dotnet build` (or a hook rewrites the Bash command into `arcforges run --session … -- dotnet build`).
2. The node persists the task (`SubmitTask`). The adapter classifies `dotnet.build`, the estimate comes from memory or the adapter, and admission queues it when budgets are full.
3. The task starts in a job or transient unit with limits. NuGet caches are redirected to the shared managed caches, `-m:N` follows the grant, and node reuse is disabled.
4. The agent receives the result within 45 s, or a handle plus `task_wait` (bounded waits), with no retry loops.
5. Records show the timeline (QUEUED_ADMISSION, RESTORE, BUILD), and the session coverage counts it as managed.

- **Success:**
  - the user's reserved headroom holds while 3+ builds run (15 §4);
  - no duplicate package downloads across tasks;
  - exit codes and output are byte-identical to direct runs.
- **Failures:**
  - OOM, with a retry using more memory for PURE or IDEMPOTENT tasks;
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

- **Verification:** closed-loop `J05_CleanupTests` on real directory trees, with junctions and symlinks, open files and dirty worktrees (T-04). The bounds (10,000 items / 2 TiB) are tested with synthetic plans.

## J-06 Pair a machine on the LAN

- **Actors.** A user with a workstation and a build box.

1. Both nodes enable LAN (D-15). The build box is DISCOVERED through DNS-SD, or added by address.
2. Pair: SAS digits are shown on both, both users confirm, and the peer is PAIRED (pinned) with a status-only policy.
3. The user widens the policy: place-to on the workstation, accept-from on the build box (Pro).

- **Failures:** a digit mismatch, which aborts with MISMATCH; expiry; blocked after 5 failures; incompatible versions.
- **Verification:**
  - closed-loop `J06_PairingTests` with two or three real node processes on one machine (loopback, real TLS);
  - mDNS on a physical LAN with two physical machines: AR-03.

## J-07 Place work on another node

1. A task with `placement=ANY` is submitted on the workstation. Scoring prefers the build box (an idle queue and a warm sccache).
2. Offer, then accept. The executor pulls the inputs, runs the task and streams its output. The workstation shows a REMOTE attempt.
3. The outputs return. The workstation materializes the declared outputs.
4. The workstation disconnects mid-run. The build box finishes and retains. On reconnect the origin collects the results.

- **Verification:**
  - closed-loop `J07_PlacementTests` (multi-node on one machine, real transfers, lease expiry, executor preemption, cache proxy with a real sccache WebDAV client);
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

1. A budget reaches 80%, raising an operator alert. The operator views W-66.
2. At 100% the kill switch disables live streaming automatically. Summaries continue and local work is unaffected.
3. A support case arrives with a consented bundle. The operator requests access, the user allows it, the operator reads it, and the read is audited.
4. A refund is decided (Paddle) and the entitlement is revoked.

- **Verification:**
  - closed-loop `J10_OperationsTests` (budgets and kill switches against the local Cloud stack; operator flows through `OperatorService`);
  - runbook review;
  - production alerting configuration: AR-09.
