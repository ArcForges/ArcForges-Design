# ArcForges requirements

Each requirement has a stable ID, a statement and an acceptance criterion. [traceability/model.json](../traceability/model.json) maps every requirement to the specification elements that satisfy it, and the Plan graph maps those elements to delivery tasks. `tools/check_design.py` fails when a requirement has no specification element or no task.

The keywords MUST and MUST NOT are binding. "Real test" means a test that runs real processes and real operating-system mechanisms in the named environment ([testing strategy](../architecture/16-testing-strategy.md)). "Closed-loop test" means an automated test of complete behaviour in which only the named unavailable external dependency is simulated.

## R-EXE — Execution

| ID | Requirement | Acceptance |
|---|---|---|
| R-EXE-001 | A caller submits a task once. The node persists it before acknowledging and starts it when dependencies, policy and capacity allow, without the caller polling or retrying for capacity. | Real test: 20 tasks submitted at once on an 18-thread host run to completion with no client retry, in the order the admission rules give. |
| R-EXE-002 | A task carries a command as an argument vector or as a shell command line with an explicit shell kind, a working directory, environment additions/removals with an inheritance mode, stdin mode, timeout, priority, pool, labels, placement constraints and a side-effect class. | Contract and schema include each field; validation tests reject malformed specs with `ERROR_CATEGORY_VALIDATION`. |
| R-EXE-003 | The node launches commands as the requesting user with the exact argument vector, working directory and resolved environment, and captures stdout and stderr separately with timestamps, plus exit code, signal and termination reason. | Real tests on Windows and WSL2 compare captured output, exit codes and environment against direct execution for argv, quoting edge cases, Unicode, long command lines (>32 KiB) and large output (>1 GiB streamed). |
| R-EXE-004 | stdin supports none, inline bytes (≤1 MiB), a file and an interactive stream while the caller is attached. | Real tests for each mode. |
| R-EXE-005 | Long-running processes (servers, watchers) run without a default timeout, can declare a readiness condition (output pattern or listening TCP port), and are stopped explicitly or with their owning session. | Real test starts a server task, waits for readiness, runs a dependent task and stops the server. |
| R-EXE-006 | Cancellation terminates the whole managed process tree. It first sends a graceful signal (CTRL_BREAK or SIGTERM), then forcibly terminates after a configurable grace period (default 10 s). No managed descendant survives. | Real tests with a process tree that ignores graceful signals, on both OSes. |
| R-EXE-007 | Timeouts (wall clock) and optional CPU-time limits terminate the tree with the termination reason recorded. | Real tests. |
| R-EXE-008 | Managed processes survive a node service restart or crash. On restart the node re-attaches to every live execution, continues log capture and accounting, and records the gap. | Real test kills the service during a build and verifies the build completes and is recorded. |
| R-EXE-009 | After a machine reboot or loss of the process tree, affected attempts become `LOST` with evidence (boot identity or job/cgroup absence). They are retried automatically only if the task is retryable. | Real test (simulated reboot by destroying the tree outside the node) plus a unit test of boot-identity comparison. |
| R-EXE-010 | Retries are automatic only for tasks classed `pure` or `idempotent`, or for infrastructure failures before the process started. A `side_effecting` or `unknown` task is never retried automatically, and an `unknown` effect is reported as such. | Unit tests of the retry policy table; real test that a side-effecting task is not retried after node loss. |
| R-EXE-011 | Pause and resume are offered only where the platform can stop a whole tree reliably. Linux pauses through the user manager's `FreezeUnit` (cgroup.freeze). Windows reports pause as unsupported. | Capability reported per node; real Linux test freezes and thaws a tree. |
| R-EXE-012 | Tasks may depend on other tasks (after success, after completion). A cycle or a dependency on an unknown task is rejected. | Unit and real tests. |
| R-EXE-013 | Pools (named queues) have a parallelism limit (auto or fixed) and a share weight. A policy can disable parallelism (limit 1) globally, per pool, per workspace or per session. | Real test: with parallelism disabled, at most one task in the scope runs at a time. |
| R-EXE-014 | Ordering inside a pool is priority first, then fair share across owners, then submission time. No waiting task starves longer than the configured starvation bound (default 10 min) while lower-priority tasks are admitted in the same pool. | Simulation and real tests of starvation bounds. |
| R-EXE-015 | Every task and attempt has one authoritative owner node. Remote attempts are owned by the executing node, and the task by the origin node. | Contract and state machine; LAN closed-loop test. |
| R-EXE-016 | Operations (submit, cancel, retry, priority change) are idempotent by caller-supplied command id within a 24 h window. | Unit test returns the original receipt on replay. |
| R-EXE-017 | The working directory and environment captured at submission are recorded with secrets redacted by policy: in records, exports and bundles, variables matching secret patterns appear as presence only. For execution, their values are kept sealed (encrypted under a key in the OS secret store) until the task is terminal and the retry window has passed, so queued tasks, restarts and retries run with the submitted environment. | Unit tests of redaction; record inspection; sealed-store tests (restart and retry keep values; purge after the window; `secrets_unavailable` afterwards). |
| R-EXE-018 | Output capture survives restarts because processes write to node-owned files. Callers read history and live tails through the API. | Real test reads output written while the service was down. |

## R-RES — Resource observation and control

| ID | Requirement | Acceptance |
|---|---|---|
| R-RES-001 | The node observes machine CPU, memory, commit/swap, disk space per volume and I/O. On Linux it also observes per-cgroup pressure (PSI). It samples at 1 s for managed executions and 5 s for the machine, with downsampled retention. | Real tests compare samples to OS tools within tolerance (CPU ±5 percentage points, memory ±2%). |
| R-RES-002 | The node distinguishes **observed** processes (all visible processes) from **controlled** processes (launched or explicitly adopted). It never claims control of observed-only processes. | API marks `control_state`; test lists unmanaged processes as observed only. |
| R-RES-003 | Budgets come from host capacity, current unmanaged load (smoothed), user-reserved headroom (default: 1 logical CPU + 10% of CPUs, and 2 GiB + 10% of memory) and policy. Callers need not provide CPU or memory figures. | Unit tests of the budget formula; real load test keeps reserved headroom free. |
| R-RES-004 | Each attempt has a resource request estimated from the toolchain profile, operational memory or conservative defaults. An explicit hint overrides it within policy bounds. | Unit tests; records show the source of each estimate. |
| R-RES-005 | Admission control starts an attempt only when its memory estimate fits available memory and pool/global concurrency allows. Memory is never overcommitted beyond policy. | Real test: memory-heavy tasks queue instead of running together. |
| R-RES-006 | Windows enforcement places each execution in a job object under a per-node root job. It applies CPU rate control (weights for sharing, a hard cap on the root job protecting reserved headroom), a commit limit and an active-process limit, and kills the tree on demand. | Real Windows tests prove each limit takes effect without elevation (F-W01, F-W02). |
| R-RES-007 | Linux enforcement runs each execution as its own transient systemd user unit in `arcforges.slice`, created through the user manager. Limits: `CPUWeight`; a slice-level `CPUQuota`, `MemoryHigh` and `MemoryMax`; per-unit `MemoryHigh`, `MemoryMax`, `OOMPolicy=kill` and `TasksMax`. It kills with `KillUnit`. Executions are never children of the node process, so they survive node restarts with a durable exit record. | Real WSL2 tests prove each limit and survival across a node restart (L-07, L-13). |
| R-RES-008 | When enforcement is unavailable (no delegation, no systemd, a missing privilege), the node reports `enforcement=OBSERVE_ONLY` or `PARTIAL` per resource. It refuses tasks whose policy requires enforcement, and runs others only if policy allows unenforced execution, labelling them as such. | Real test on a guest without systemd user delegation (simulated by withholding delegation) shows refusal or labelling. |
| R-RES-009 | The controller adapts to unmanaged load: it shrinks the managed root's CPU cap and memory budget with hysteresis, stops admissions, and applies the configured memory-pressure action (pause where supported, preempt preemptible tasks, or notify). | Real test raises unmanaged load and observes the reactions. |
| R-RES-010 | Windows and WSL2 are separate environments on one physical host. The host node accounts the WSL VM as a guest consumer, and the guest node reports its managed and unmanaged usage. No resource is counted twice. | Real test runs load in the guest and checks host accounting. |
| R-RES-011 | Limiting `wsl.exe` or any Windows launcher is never presented as limiting the Linux processes it starts. Linux work is controlled by the guest node or reported as unmanaged. | Contract and UI labelling; test that a Windows-side task invoking `wsl.exe` is flagged `crosses_vm_boundary`. |
| R-RES-012 | Process-tree termination includes orphan handling: descendants that escaped by breakaway or WMI are detected by ancestry scan and reported as escaped, not silently left running. | Real Windows test with a WMI-created child. |
| R-RES-013 | Explicit adoption of an existing process is opt-in, same-user only, and recorded. A failure to adopt (for example a process already in a non-nestable job) is reported, never forced. | Real test. |

## R-TOOL — Toolchains

| ID | Requirement | Acceptance |
|---|---|---|
| R-TOOL-001 | The node detects installed toolchains (.NET SDKs, MSBuild, Rust/Cargo, CMake, Ninja, MSVC/clang/gcc, Node/npm, Python), with versions and paths, per environment (Windows, each WSL guest). | Real detection test on the workstation (L-10, L-11). |
| R-TOOL-002 | Toolchain adapters for .NET, Cargo, CMake/Ninja and Node classify commands, inject tool-level concurrency consistent with the CPU grant (`-m:N`, `-j N`, `CMAKE_BUILD_PARALLEL_LEVEL`), direct caches and temporary files to managed locations, and detect phases. Unknown commands use the generic adapter. | Real tests per adapter (F-T01). |
| R-TOOL-003 | Adapters never present tool flags as hard limits. Hard limits come only from OS enforcement, and records state both. | UI and record review; unit tests of labels. |
| R-TOOL-004 | Each adapter declares which redirections are best-effort (tools that may ignore variables) and which are contained. | Adapter manifest field; documentation test. |
| R-TOOL-005 | MSBuild node reuse and similar daemons are managed explicitly. Within a managed execution, node reuse is disabled by default, or a shared daemon is accounted as a shared service with an owner. | Real test shows no MSBuild node outlives its execution unless policy keeps a shared daemon. |
| R-TOOL-006 | FASTBuild is supported: detection, a managed cache (`FASTBUILD_CACHE_PATH`, read and write modes, trimming with `-cachetrim`), local worker concurrency from the CPU grant (`-j`), and records. FASTBuild distributed compilation (`-dist`, brokerage and FBuildWorker) is observed and recorded but not managed in this scope ([05](../architecture/05-toolchains-caches.md) §3.8). | Real test when FASTBuild is installed (F-T02); otherwise recorded as missing tool. |

## R-CACHE — Caches

| ID | Requirement | Acceptance |
|---|---|---|
| R-CACHE-001 | Every cache the node manages is registered with kind, location, owner, compatibility key (toolchain family, version band, OS, architecture, configuration), size, quota and state. | Schema and API; registry test. |
| R-CACHE-002 | Shared caches are used only by executions with a matching compatibility key. Mutable build outputs (bin/obj/target) are never shared between unrelated workspaces. | Unit tests of key matching; real test that two worktrees get separate output directories and a shared package cache. |
| R-CACHE-003 | For NuGet, all managed executions on a node share one global-packages folder, one http cache and one scratch folder per compatibility key (V-T01). Per-task restores into fresh folders are detected and reported. | Real test; diagnosis finding for per-task restores. |
| R-CACHE-004 | sccache and ccache are integrated as optional compiler caches with managed directories and size limits. Their hit/miss statistics are collected. | Real tests where the tools are installed (sccache on Windows L-10). |
| R-CACHE-005 | Quotas and eviction (LRU by last use) keep each cache within its limit without evicting entries in use by running executions. | Unit and real tests. |
| R-CACHE-006 | Integrity: content-addressed stores verify digests on read. Tool caches are verified with the tool's own verification where one exists. A corrupt entry is quarantined and rebuilt. | Corruption-injection test. |
| R-CACHE-007 | A node can serve its compiler caches to trusted LAN peers through an authenticated WebDAV-compatible endpoint (sccache WebDAV, ccache HTTP), with read-only or read-write per peer policy and quota enforcement. | Closed-loop LAN test with two nodes on one machine (separate users or ports); real cross-machine run is deferred validation. |
| R-CACHE-008 | Cache effectiveness is reported: hits, misses, bytes saved, duplicate downloads and duplicate cache copies. | Report test with seeded statistics. |

## R-STOR — Storage, workspaces and cleanup

| ID | Requirement | Acceptance |
|---|---|---|
| R-STOR-001 | One configurable data root per node has managed sub-roots: work, tmp, cache, out, logs, records, downloads and staging. A sub-root may be placed on another volume. | Settings API and schema; real relocation test. |
| R-STOR-002 | Every managed directory has an ownership record (owner kind and id, created, last used, pinned, size, state). | Schema; test that no managed directory exists without a record. |
| R-STOR-003 | Workspaces are registered checkouts or node-managed git worktrees. Managed worktrees are created and removed through the node with branch, base and owner recorded. | Real git worktree tests. |
| R-STOR-004 | Managed executions get per-attempt temporary directories (TMP, TEMP and TMPDIR), removed after the attempt unless retained by policy for diagnosis. | Real test. |
| R-STOR-005 | Quotas per sub-root, and retention for logs and records, are enforced. Exceeding a hard quota blocks new allocations with a typed error. | Unit and real tests. |
| R-STOR-006 | Cleanup is two-phase: plan (dry run with exact paths, sizes and reasons), then execute after approval. It never touches directories in use by running or queued attempts, pinned items, or paths outside managed roots unless the user explicitly selects them in that plan. Deletion first moves items to a quarantine on the same volume with a delayed purge (default 24 h). Items on a volume with no quarantine root (managed roots or a configured `storage.quarantine_roots` entry) can only be deleted after an explicit per-item delete-without-quarantine confirmation. | Real tests, including active-use protection, quarantine restore and the cross-volume confirmation. |
| R-STOR-007 | Disk analysis reports usage by sub-root, workspace and cache, duplicated caches, abandoned worktrees (no recent activity, no live owner, merged or deleted branch) and per-task restore copies, with reclaimable estimates. | Real test on a seeded tree. |
| R-STOR-008 | Cleanup is bounded: one cleanup execution removes at most the planned set. No wildcard or unbounded deletion API exists. | API review and negative tests. |

## R-REC — Execution records

| ID | Requirement | Acceptance |
|---|---|---|
| R-REC-001 | Each attempt records a timeline of categorized segments: queued-admission, queued-dependency, workspace-preparation, transfer, restore/download, build/compile, test, link/package, run, network-wait, disk-wait, idle-no-progress, paused, throttled, finalizing and unknown. Each segment carries evidence and a confidence. | Real tests for .NET and Cargo builds show restore and build segments. |
| R-REC-002 | Progress is never inferred from process existence. It is inferred from CPU time, I/O, output, child-process activity and adapter phase markers. Elapsed time is never reported as model thinking time. | Unit tests of the classifier; review of labels. |
| R-REC-003 | Records expose tables, timelines and machine-readable exports (JSON Lines and protobuf) per task, session, workspace and period. | Export tests. |
| R-REC-004 | Repeated work is detected: the same command fingerprint and input fingerprint re-executed without an input change is flagged `repeat`, and work whose inputs changed while it was queued or running is flagged `stale`. | Unit tests; real repeat test. |
| R-REC-005 | Retention keeps records within configured size and time bounds, and downsamples resource samples. | Unit tests. |

## R-DIAG — Diagnosis and recovery

| ID | Requirement | Acceptance |
|---|---|---|
| R-DIAG-001 | Periodic progress checks (default every 15 s per running attempt) detect no-progress intervals from evidence. A stall finding needs both no CPU and no I/O progress and no output beyond the threshold (default 5 min, adapter-specific). | Real test with a deliberately hung process. |
| R-DIAG-002 | Findings cover at least: stall, queue starvation, memory-pressure kill or OOM, repeated work, stale work, per-task restore, cache miss storm, disk pressure, unmanaged heavy process in an agent session, bypassed command, dead or orphaned execution, and over-subscription. | One test per finding kind with seeded evidence. |
| R-DIAG-003 | Each finding lists recommended actions. Policy states which actions are automatic, which need approval and which are notify-only. Destructive or side-effecting actions always need approval unless explicitly configured. | Policy tests. |
| R-DIAG-004 | `arcforges doctor` and the Diagnosis page check service health, enforcement capabilities, WSL guest links, integrations, storage and caches, with remedies. | Real test on the workstation. |

## R-MEM — Operational memory

| ID | Requirement | Acceptance |
|---|---|---|
| R-MEM-001 | The node keeps learned facts (duration and peak-memory distributions, typical phases, failure signatures, required environment) scoped by project identity, environment, toolchain version and command fingerprint. | Schema; learning test. |
| R-MEM-002 | A fact is invalidated or expires when its scope key changes (toolchain version, lockfile digest) or after its TTL (default 30 days without observation). A stale fact is never used without revalidation and is labelled when shown. | Unit tests. |
| R-MEM-003 | Users can list, inspect and forget facts. AI clients can query facts through MCP. | API and MCP tests. |

## R-AI — AI client integration

| ID | Requirement | Acceptance |
|---|---|---|
| R-AI-001 | The MCP adapter exposes managed execution and inspection tools over stdio. It supports MCP revisions 2025-11-25 and 2026-07-28, uses explicit server-minted task handles, and offers the official tasks extension where the client supports it (V-A01). | MCP conformance tests for both revisions. |
| R-AI-002 | Long operations never block a tool call beyond its bounded wait (default 45 s). The call returns the task handle, current state and an output tail, and the agent continues with wait, status or output tools. | Closed-loop MCP tests. |
| R-AI-003 | Claude Code integration installs, with consent, an MCP server entry, hooks (SessionStart, SessionEnd, SubagentStart, SubagentStop, PreToolUse and PostToolUse for Bash) and optional plugin packaging. It records the session, subagent, working directory and agent process identity (V-A02). | Closed-loop test with recorded hook payloads; real configuration validation against the installed client. |
| R-AI-004 | Codex integration installs, with consent, an MCP server entry and hooks (SessionStart, SessionEnd, SubagentStart, SubagentStop, PreToolUse and PostToolUse). Because Codex hooks fail open, the integration reports hooks as guardrails, not enforcement (V-A04). | Same as R-AI-003. |
| R-AI-005 | Routing modes are MCP tool (always available), command rewrite through `arcforges run` (only after a passing in-client reachability probe), deny-with-guidance, and observe-only. The active mode per client and session is visible. | Closed-loop tests per mode; probe tests (F-A01). |
| R-AI-006 | Bypassed heavy work (processes under a registered agent process tree that are not managed) is detected, attributed to the session where ancestry allows, and reported. Unattributable work is reported as unattributed, never guessed. | Real test runs a heavy command outside ArcForges under a registered fake agent process. |
| R-AI-007 | Coverage per session reports routes, managed and bypassed counts, and unknowns. The node never claims to know model, thinking state or internal completion status beyond events the client exposes. | Contract fields and UI labels; review. |
| R-AI-008 | Integration never edits managed or enterprise settings, never silently overrides user or repository instructions, shows a diff before writing, and reports conflicts (hooks disabled, untrusted, sandbox denies IPC). | Tests with fixture settings files, including managed-only policies. |
| R-AI-009 | Guardrails keep managed tasks from accidentally replacing or reconfiguring the ArcForges installation. These are read-only version directories with digest checks at startup, tamper findings for out-of-band edits, and optional Linux unit hardening. Configuration changes from AI clients go through policy-gated APIs that may require approval. Same-user bypasses are documented, never claimed impossible. | Policy tests; read-only and digest checks; tamper-finding test. |

## R-API — Contracts and state

| ID | Requirement | Acceptance |
|---|---|---|
| R-API-001 | `.proto` files are the canonical first-party contracts, published from the Contracts repository. | Contracts CI; spec check. |
| R-API-002 | GUI, CLI, MCP adapter and WSL bridge talk to the local node with gRPC over a Windows named pipe or Unix domain socket restricted to the same user. | Real tests including wrong-user denial on Linux (second uid; deferred where unavailable) and pipe ACL verification on Windows. |
| R-API-003 | The node is the only writer of its execution and resource state. Clients hold caches only and reconcile from streams. | Architecture tests forbid client-side state writes. |
| R-API-004 | Event streams start with a snapshot at a cursor followed by ordered incremental events. Clients resume from a cursor, and a cursor outside retention yields a reset with a new snapshot. Duplicates are identified by sequence number. | Closed-loop stream tests with disconnects. |
| R-API-005 | An action from any surface (CLI, MCP, GUI, mobile through relay) appears in all connected surfaces within 1 s locally and 5 s remotely (p95). | Closed-loop multi-client test. |
| R-API-006 | Deadlines are required on unary calls (default 10 s, maximum 120 s). Streams are long-lived with heartbeats every 15 s. Cancellation propagates. | Tests. |
| R-API-007 | Versions are negotiated: a client reports its contract version, the node refuses incompatible majors with a typed error, and minor additions are compatible. | Compatibility tests across N−1 minor versions. |
| R-API-008 | Errors use `arcforges.foundation.v1.ArcError` with category, retry advice and effect certainty. | Contract check. |

## R-LAN — LAN

| ID | Requirement | Acceptance |
|---|---|---|
| R-LAN-001 | Nodes discover peers through DNS-SD (`_arcforges._tcp.local`), manual address entry and account-assisted hints. Discovery never implies trust. | Unit tests; real single-host test with two nodes; physical LAN deferred. |
| R-LAN-002 | Trust comes from pairing: either both nodes belong to the same account (cloud-issued node certificates), or a local short-authentication-string comparison confirmed on both nodes. | Closed-loop pairing tests. |
| R-LAN-003 | Peer traffic uses mutually authenticated TLS 1.3 with pinned or account-issued node certificates. Unpaired identities may reach only the handshake and pairing services. | Tests: revoked or invalid account certificates fail the TLS handshake; unpaired identities are refused every service except handshake and pairing; pinned and same-account identities pass. |
| R-LAN-004 | Peers report capabilities, toolchains, enforcement state and resource offers. Placement requires a per-peer policy allowing it. | Contract tests. |
| R-LAN-005 | Placement chooses among local and peer nodes by constraints, available resources, cache locality, transfer cost and policy, and falls back to local queueing. | Unit tests of scoring; closed-loop placement tests. |
| R-LAN-006 | Workspace inputs transfer as content-addressed manifests with blob deduplication. Outputs and artifacts return the same way. LAN data never routes through the cloud. | Closed-loop transfer tests; network capture shows no cloud egress. |
| R-LAN-007 | Disconnects keep remote attempts running. The origin resumes streams by cursor, and an executor lost beyond its lease makes the attempt `LOST`, retried elsewhere only if retryable. | Closed-loop fault-injection tests. |
| R-LAN-008 | Cancellation and ownership work across nodes, and an executor's local policy may refuse or preempt remote work. | Tests. |
| R-LAN-009 | Peer protocol versions are negotiated, and incompatible peers are shown as such. | Tests. |
| R-LAN-010 | The product distinguishes separate-task placement, toolchain distributed compilation, and cache or artifact sharing. It never implies one process runs across machines. | Documentation and UI review. |

## R-CLOUD — Cloud

| ID | Requirement | Acceptance |
|---|---|---|
| R-CLOUD-001 | Local and LAN-internal operation never requires continuous cloud connectivity. Entitlements are cached as signed tokens with an offline grace period (default 14 days). | Test with the cloud unreachable. |
| R-CLOUD-002 | Nodes connect to the cloud relay with short-lived node tokens through hibernating Durable Object WebSockets. Business decisions stay in C# (V-C01). | Closed-loop relay tests with a local Workers runtime (wrangler dev / workerd) where available; deployment evidence separately. |
| R-CLOUD-003 | Status telemetry to the cloud is demand-driven. Full snapshots flow only while an authorized viewer watches, otherwise only presence and summary changes, within per-account rate limits. | Relay tests count frames. |
| R-CLOUD-004 | Remote commands are authorized in C#, signed, checked again by the node's local remote-control policy, audited and idempotent. High-risk commands need confirmation on the requesting device and are allowed only if the node's policy permits them remotely. | Tests. |
| R-CLOUD-005 | Push notifications (FCM HTTP v1) are sent for user-selected events, deduplicated and rate-limited. | Closed-loop test with an FCM fake; physical device deferred. |
| R-CLOUD-006 | Application-enforced quotas and operating budgets bound every metered cloud path, with kill switches. Budget alerts are never counted as enforcement (V-C04). | Tests that exceed quotas and trip kill switches. |

## R-UX — User surfaces

| ID | Requirement | Acceptance |
|---|---|---|
| R-UX-001 | Desktop pages in [experience/desktop.md](../experience/desktop.md) each specify purpose, permissions, layout, data, actions, all states (loading, empty, offline, reconnecting, denied, failed, expired), confirmations, accessibility and APIs. | Spec check; implementation UI tests per page. |
| R-UX-002 | Closing the Desktop window never stops the node or running tasks. The tray (where supported) shows node status. | Real test. |
| R-UX-003 | The CLI ([experience/cli.md](../experience/cli.md)) supports human output, `--json` machine output, stable exit codes and shell completion. It auto-starts a stopped node. | Real tests. |
| R-UX-004 | Web pages in [experience/web.md](../experience/web.md) are specified like desktop pages. | Spec check. |
| R-UX-005 | Android screens in [experience/android.md](../experience/android.md) are specified like desktop pages, including reconnect, offline and background behaviour. | Spec check. |
| R-UX-006 | All surfaces meet WCAG 2.2 AA for the specified pages: keyboard access, screen-reader names, contrast and target sizes. Human screen-reader validation is deferred. | Automated accessibility checks; manual session deferred. |

## R-AUTH — Identity and access

| ID | Requirement | Acceptance |
|---|---|---|
| R-AUTH-001 | Desktop and CLI sign in through the system browser with PKCE and a loopback redirect. Headless contexts use the device authorization grant (code plus URL plus QR). Token copy-paste is never the normal path. | Closed-loop tests against the cloud identity service with a scripted browser fake. |
| R-AUTH-002 | Android signs in through a Custom Tab with PKCE, or by scanning a QR shown by a signed-in desktop node and confirming on that desktop. | Closed-loop tests. |
| R-AUTH-003 | Device and node credentials are stored in the OS secret store (Windows Credential Manager, Android Keystore). Linux uses a 0600 file in the node data root when no secret service exists, and reports that weaker protection. | Tests. |
| R-AUTH-004 | Credentials are scoped (node uplink, user session, push) and revocable per device and session from web, desktop and mobile. | Tests. |
| R-AUTH-005 | Account authentication is separate from OS privileges. No account action grants OS privileges, and privileged installation steps are explicit OS prompts. | Review; UI labels. |

## R-COM — Commerce

| ID | Requirement | Acceptance |
|---|---|---|
| R-COM-001 | Web subscriptions use Paddle as Merchant of Record (reused design V-C07). Checkout, renewal, cancellation, refund, payment failure and dunning update entitlements through verified webhooks. | Closed-loop tests with recorded signed webhook fixtures; live checkout deferred. |
| R-COM-002 | Android subscriptions use Google Play Billing. The backend verifies purchases with `purchases.subscriptionsv2`, acknowledges within the window, links with `obfuscatedAccountId`, processes RTDN, and handles restore, cancellation, grace period, account hold, pause, expiry, revocation and refund (V-C05). | Closed-loop tests with a Play Developer API fake and RTDN fixtures; real purchase deferred. |
| R-COM-003 | One entitlement snapshot per account combines web and Play sources without double-granting. Changes reach relay-connected nodes within 60 s (`EntitlementChanged` frame). Other online nodes receive them at their next refresh (at most 24 h), or immediately when the user refreshes or opens the account page. | Tests. |
| R-COM-004 | Entitlement enforcement on nodes uses signed tokens with offline grace. Expiry degrades only the gated features and never interrupts running local tasks. | Tests. |

## R-DIST — Distribution and updates

| ID | Requirement | Acceptance |
|---|---|---|
| R-DIST-001 | A per-user Windows setup program (no administrator rights needed) installs the `arcforges` binary, the supervisor, node autostart, PATH entry, an uninstall entry that the updater keeps current, and the optional Desktop. A Linux user-level install script and a `.deb` package install the binary and the systemd user unit. | Real install/uninstall tests on the workstation and in WSL2 (fresh user profile or container). |
| R-DIST-002 | Release artifacts are signed (Authenticode on Windows; signed manifests for all artifacts). The node verifies signatures before applying updates. | Tests with test keys; production signing deferred. |
| R-DIST-003 | Updates are staged side by side, switched atomically when safe, health-checked and rolled back automatically on failure. Running executions survive the switch (R-EXE-008). | Real update and rollback tests with locally built versions. |
| R-DIST-004 | `arcforges integrate` configures AI clients. The product does not assume that installing a plugin or MCP configuration installs or authorizes the native service. | Tests. |
| R-DIST-005 | Package-manager routes (winget, Scoop, apt repository) and AI-client plugin discovery (Claude Code marketplace, Codex plugins) are prepared with manifests. Their publication is a release task. | Manifest validation; publication deferred to release. |

## R-OPS — Commercial operation

| ID | Requirement | Acceptance |
|---|---|---|
| R-OPS-001 | Onboarding, account recovery, device enrollment and revocation reuse the existing identity and device contracts, D1 schema and domain stores. Their service endpoints and flows are implemented for the flagship (AF-ID-01, AF-ID-02). | Tests. |
| R-OPS-002 | Usage limits and abuse prevention cover sign-in, pairing, relay connections, viewers, commands, push and support, with rate limits and anomaly flags. | Tests. |
| R-OPS-003 | Privacy: command lines, environment values and output never leave a node unless a user explicitly requests them for a remote view or a support bundle. Telemetry is opt-in. | Tests and data-flow review. |
| R-OPS-004 | Retention and deletion: account deletion removes cloud data per the retention schedule. Nodes provide a local data wipe. Exports are available. | Tests. |
| R-OPS-005 | Support diagnostics: locally generated, redacted support bundles, uploaded only with consent and linked to support cases. | Tests. |
| R-OPS-006 | Service operations: health endpoints, structured logs, metrics, operating budgets, alerting and incident runbooks exist for each cloud component. | Review and tests. |

## R-PERF — Performance and footprint

| ID | Requirement | Acceptance |
|---|---|---|
| R-PERF-001 | The node, CLI, Desktop and MCP adapter meet the measurable targets in [performance targets](../architecture/15-performance-targets.md) (idle CPU and memory, startup latency, binary size, scheduling overhead). | Benchmarks in CI (size, startup) and on the workstation (idle footprint). |

## R-SEC — Security

| ID | Requirement | Acceptance |
|---|---|---|
| R-SEC-001 | Local IPC accepts only same-user peers: pipe DACL on Windows, socket directory permissions and SO_PEERCRED on Linux. | Real tests; second-account checks deferred where unavailable. |
| R-SEC-002 | Every privileged or remote action is audited locally, and in the cloud for cloud-originated actions. | Tests. |
| R-SEC-003 | Secrets are never logged. Redaction applies to records, exports and support bundles. | Tests with seeded secrets. |
| R-SEC-004 | Threat model ([security](../architecture/11-security-privacy.md)) items have mitigations with tests. | Review. |

## R-TEST — Development-stage verification

| ID | Requirement | Acceptance |
|---|---|---|
| R-TEST-001 | Every delivery task ships automated tests. Mocks and fakes are allowed only for unavailable external dependencies (other machines, cloud providers, app stores, payment providers, AI clients' internals), never for the behaviour under test. | Review of each task's evidence. |
| R-TEST-002 | Real Windows and WSL2 tests run the node's process control on the workstation, including concurrent workloads and resource sharing. | Test reports. |
| R-TEST-003 | Deferred real-world validations (physical multi-machine LAN, real stores and payments, physical devices, production signing reputation, second OS accounts, human accessibility sessions) are recorded in the Plan's acceptance register with prerequisites and owner, and are never reported as proven. | Register exists and is referenced. |
