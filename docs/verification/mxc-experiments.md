# MXC native experiment protocol

Status on **2026-11-14 UTC: every experiment below is NOT_RUN**. Official release/source/package inspection is recorded in [MXC research](../research/mxc-research.md); it is not native runtime evidence. No designated Windows/Linux verification host was available for these experiments in this Design migration.

This protocol implements [02 — MXC integration](../architecture/02-mxc-integration.md). The selected profiles are `windows-process-executor-v1` and `linux-bubblewrap-sdk-v1`, initially pinned to official **1.0.1**, stable schema **1.0.0**. Windows uses the unchanged official executor, C# Native AOT ConPTY supervision and an outer ArcForges Job. Linux uses the official typed .NET SDK inside the established cgroup boundary. No private fork, custom MXC build, test-only forced tier, substitute backend, or plain-pipe terminal claim is acceptable.

## 1. Ownership and evidence rules

| Experiment set | Plan owner | Platform register | Current result |
|---|---|---|---|
| MXC-AOT-01 | AFV2-MXC-01 | F-AOT-01 | NOT_RUN |
| MXC-WIN-01 through MXC-WIN-06 | AFV2-MXC-02 | A-MXC-01 / F-MXC-01 | NOT_RUN; Windows combination UNPROVEN |
| MXC-LNX-01 through MXC-LNX-05 | AFV2-MXC-03 | A-MXC-02 / F-MXC-02 | NOT_RUN; Linux combination UNPROVEN |
| Cross-profile decision | AFV2-MXC-04 | Both combination facts plus F-AOT-01 | BLOCKED pending evidence, not a declared product impossibility |

Use the designated native Windows and native Linux verification hosts and the repository's normal exact-commit verification procedure. An agent sandbox, WSL, container imitation, source unit test, mocked SDK, or successful CI compilation is not native combination evidence. Do not post successful platform statuses by hand. If a host/dependency is unavailable, preserve `NOT_RUN` with its reason and owner; do not downgrade the acceptance criterion.

Each result bundle contains:

- Experiment ID, exact ArcForges/Design/Plan commits, official package/native/executor versions, runtime file hashes/signatures, selected profile revision, command/fixture hashes and redacted policy hash.
- Host architecture, Windows build/PSEC request probe or Linux kernel/cgroup/user-namespace/helper versions, service identity and inherited resource-scope description. Redact personal paths and secrets in exported records.
- Expected result and actual result for each case, native/API return values, trusted process/resource observations, terminal byte trace where useful, resource readback, cleanup proof, elapsed-time measurements and limitations.
- Run ID, boot identity, supervisor process-start identity, owner generation, scope identity, state transitions, exit-source/start-certainty/stop-reason fields, and any gap or cleanup failure.
- Separate labels for observed passes, observed failures, unavailable/not run cases, and inferences. An ordinary stdout assertion cannot establish isolation, start identity, resource membership or cleanup by itself.

Use disposable, uniquely owned fixture directories and synthetic data, never real credentials or another user's files. Test processes have modest bounded CPU, memory, child counts and lifetimes; a trusted external observer/cleanup owner is ready before starting them. No global firewall/namespace/sysctl changes, DACL host preparation, or broad host filesystem grant is part of this protocol. Prerequisites are explicitly provisioned through normal host administration, not silently repaired by the test harness. Capture pre/post state for every resource the experiment owns.

## 2. MXC-AOT-01 — Official package, AOT and distribution

**Owner:** AFV2-MXC-01. **Evidence basis:** V-MXC-01/02/07. **Purpose:** prove the exact official distribution works with a real ArcForges Native AOT owner, rather than treating the upstream JSON-only smoke sample as a native test.

1. Resolve the locked `Microsoft.Mxc.Sdk` 1.0.1 package and official v1.0.1 native unit. Check the current official release metadata before running; an upgrade is a new reviewed pin. Verify package contents and lock integrity, release ZIP digest, and Windows signatures on the actual host. Record every shipped native/sidecar hash and license/third-party notice. Confirm no unreviewed source rebuild, Node runtime or executable from ambient PATH is used.
2. Publish the bounded experiment supervisor with Native AOT for each candidate shipping RID. Run the published output from a clean installation location without an SDK/JIT dependency. Inspect trimming/AOT diagnostics and native dependency resolution; reject missing/unexpected files rather than masking it with development PATH or `MXC_FFI_DIR` overrides.
3. Call public `MxcPlatform.NativeVersion`, `GetPlatformSupport` and `GetAvailableBackends`. On Linux perform an actual pipe and PTY spawn/wait/cleanup through V1. On Windows load/probe the package where used and run the unchanged executor through the intended host launcher. Record process behavior, not just successful JSON serialization.
4. Validate mismatch detection with a deliberately incomplete private staging copy and an incompatible recorded manifest; no workload may run. The experiment never modifies a shared installed runtime. Check Unicode/space-containing installation and request paths, noninteractive service context, and absent global PATH helpers where the profile promises explicit resolution.
5. Apply per-request optional telemetry disabled for the selected stable version. Verify an offline local start and completion with no Center login/subscription. Inspect logs/process argv for synthetic secret sentinels; policy/environment contents must not leak there. Document any remaining official-runtime artifacts or required telemetry behavior before accepting a newer pin.

**Pass:** real published native execution and cleanup on each advertised RID, coherent verified official artifact set, license/distribution manifest and offline local behavior. Package metadata or the upstream reflection-free JSON smoke alone cannot pass. Unavailable architectures remain unqualified and must not be advertised.

## 3. Windows experiments

### MXC-WIN-01 — Exact policy admission and fail-closed tier

**Owner:** AFV2-MXC-02. **Purpose:** establish that the official binary can service the complete no-DACL-mutation ProcessContainer profile.

1. Record the actual Windows build, service token and inherited Job chain. Create an owner-only Run control directory, a writable fixture workspace and a separate denied fixture. Compile schema 1.0.0 JSON with explicit ProcessContainer, private-control deny, `fallback.allowDaclMutation=false`, filesystem/network/UI policy and exact clean environment. Keep the control directory outside all grants.
2. Probe this same file with the official executor. Require native BaseContainer selection, native deny capability, no DACL augmentation and all required policy capabilities. Follow with a real launch; a dry-run/probe alone is insufficient. Readback confirms the untrusted process cannot open the policy/control endpoint.
3. Exercise deterministic incompatible requests, including `processContainer.leastPrivilege=true` (not supported by native BaseContainer), malformed JSON, unknown schema, missing policy file, invalid environment, and an unsupported network combination. Confirm rejection before a synthetic payload-entry sentinel appears, no weaker backend runs, and host ACL snapshots remain unchanged.
4. Where a designated lower-capability host is available, rerun the identical deny plus fallback-false request and require rejection. If unavailable, label that host case not run; do not emulate it with a custom MXC testing build. Never enable `MXC_FORCE_TIER` or auto-run `wxc-host-prep`.
5. Attempt control-file replacement/reparse traversal from the test principal and access from the restricted workload. Verify atomic creation, ownership and failure behavior. Test Windows command-line quoting using spaces, quotes, trailing backslashes and Unicode; confirm argument values inside the contained process without a host shell.

**Pass:** actual native tier and policies established; incompatible request leaves no payload and no host DACL changes. Any successful fallback, readable control file, silent policy reduction, or injection is a failure.

### MXC-WIN-02 — ConPTY, real TUI and truthful exit

**Owner:** AFV2-MXC-02. **Purpose:** prove the unchanged executor preserves a full terminal through ProcessContainer.

1. Start the C# Native AOT supervisor with the profile's resource boundary, create ConPTY before executor launch, and concurrently pump input/output. Use a terminal fixture that calls the platform console APIs and a representative interactive shell/TUI. Require actual console/terminal detection; a pipe-only echo test does not qualify.
2. Exercise line editing, raw-mode keyboard input, ANSI cursor movement/alternate screen, Unicode output, prompt interaction, and sustained output larger than every pipe/buffer. Resize repeatedly from initial dimensions to both small and large valid dimensions; confirm the program sees and redraws for the actual new size. Reject zero/overflow dimensions before a native call.
3. Send Ctrl+C to a cooperative foreground program with child processes, then to a raw-mode program and an ignoring program. Record which operation is terminal input, which is graceful exit, and when the supervisor deadline escalates to tree kill. Do not assert that ETX universally means SIGINT or graceful stop on Windows.
4. Detach all clients during output and input wait, keep draining, and reattach to the same live owner. Verify output replay/gaps, unchanged Run and terminal identity, one writer lease and observer isolation. Repeated attach must not start new executors.
5. Run payload exits 0, 1 and a selected nonzero code, invalid executable, native launch failure, timeout, and forced stop. Include a workload that prints a fake JSON backend-error envelope and fake state records. Trusted state must not change because of those bytes. Validate raw `official_executor` exit provenance and unknown payload-start certainty where no trusted signal establishes more.

**Pass:** actual interactive console behavior, responsive resize/control, lossless-or-explicitly-gapped draining, detach persistence and honest outcomes under the same policy. Unsupported terminal behavior is a profile blocker, not a reason to return a pipe stream labeled PTY.

### MXC-WIN-03 — Before-execution resources and nested Job ownership

**Owner:** AFV2-MXC-02. **Purpose:** prove the existing ArcForges resource model composes with MXC's inner Job.

1. Configure/read back bounded CPU, memory and process-count policy on the intended outer scope. Start the trusted worker suspended, assign the valid ancestor chain before resume, and prove its membership from the external observer. No Job in the ArcForges chain may carry UI restrictions or breakaway.
2. Invoke the official executor, whose BaseContainer payload inherits the outer chain and gets MXC's own Job before resume. A burst fixture immediately creates children, allocates bounded memory and burns CPU before reporting readiness. Observe all descendants and resource charges from the OS, not solely from fixture messages. Include very short-lived children so late PID attachment would be detected.
3. Exceed each configured limit in an isolated case and verify enforcement and readback; then update limits during a live terminal run and verify desired/apply/readback state and actual behavior. Record helper/supervisor charges and distinguish aggregate ancestor totals from per-Run attribution.
4. Exercise expected parent Job assignment failures and invalid resource settings. Require no payload execution and reliable cleanup, with a concrete failure reason. Inspect the actual service's ancestor Jobs; success in an unconstrained developer console is not sufficient.
5. Hold/recover the outer owner across abrupt Node death while the supervisor/executor/payload continue. Confirm the same Job identity and limits remain, then stop through the recovered owner. Test supervisor loss separately and verify kill-on-close/retained guardian behavior removes descendants.

**Pass:** constraints exist before untrusted code, every descendant remains controlled, dynamic updates/readback are truthful, and Node death does not drop the last required owner. An inner-Job creation success without outer enforcement is insufficient.

### MXC-WIN-04 — Filesystem, network and terminal in combination

**Owner:** AFV2-MXC-02. **Purpose:** test exact policies with the real resource-limited terminal profile.

1. Present owned home/config/cache/tmp/work/data directories at their actual paths; grant only those needed writable and selected tool/input paths read-only. From the terminal run test intended persistence, read-only write denial, private-control and neighboring-Sandbox denial, hardcoded ungranted writes, reparse/link escape attempts, and explicit external writable grants. Confirm writes are denied rather than transparently redirected; verify external data is never marked owned for deletion.
2. Test clean environment and known-folder behavior using synthetic secrets. Document applications that ignore configured paths; do not grant the entire user profile or temp directory to hide incompatibility. Include a multiprocess build/test fixture and named-IPC use to expose practical CLI limitations.
3. Use controlled test endpoints to verify all-deny egress, selected IP/protocol/port egress, denied destinations, host-loopback policy and supported inbound behavior separately. If proxy mode is advertised, verify that only the configured cooperative proxy/peer is reachable and forbidden direct access remains denied. Record native capability prerequisites and unsupported combinations rather than broadening them.
4. Run the TUI/resize and bounded resource pressure while the filesystem/network checks are active. Snapshot relevant host DACLs before/after. Verify enforcement remains until the last workload descendant is gone.

**Pass:** policy effects on both allowed and denied cases match the advertised capability set while terminal and resources remain active. Domain-name semantics, unrestricted host services and arbitrary write redirection are not inferred from successful network/filesystem calls.

### MXC-WIN-05 — Owner loss, root exit and cleanup proof

**Owner:** AFV2-MXC-02. **Purpose:** prove persistent Sandbox data and bounded Run ownership across failure.

1. Start a root that creates a persistent background child, then let the root exit. Record native/executor exit and independently observe the child terminated. The run must not become a detached daemon outside the supervisor.
2. Terminate Node at each boundary: prepared record, resource scope created, supervisor ownership acknowledgement, executor created, active terminal, root exited/cleaning, final record. Recovery reconnects to the same authenticated supervisor or cleans the exact recorded scope; it never adopts a recycled PID.
3. Lose the supervisor separately, close the active client, and simulate unavailable Center separately. Client/Center loss leaves the run locally owned; supervisor loss triggers fail-closed cleanup. Test authentication failures and stale owner generation without affecting unrelated processes.
4. Verify complete workload/helper emptiness from the outer scope before terminal completion or deletion. When the supervisor itself is a member, enumerate its exact known identity separately; do not equate root exit, executor exit, or MXC's five-second drain warning with an empty scope. Inject an owned cleanup failure and require a retained unresolved state/owner and denied data deletion.
5. Restart a new Run in the same Sandbox data and prove persistence of intended state. Safely remove only test-owned control/native resources after all owners are reconciled. A stale private policy file is not a launch instruction on recovery.

**Pass:** precise recovery, no orphan/unowned workload, no unrelated termination, truthful cleanup-failure state and data persistence. There is no SDK handle reopening or persistent MXC ProcessContainer lifecycle assumption.

### MXC-WIN-06 — Combined qualification and measured overhead

**Owner:** AFV2-MXC-02; decision reviewed under AFV2-MXC-04.

Run one bounded long-lived multiprocess terminal workload with the accepted filesystem/network policies and live CPU/memory/process limits. Exercise resize, attach/detach, Node restart/reconnect, a limit update, then Stop and complete cleanup. Repeat with the required default-deny and selected-egress modes. Capture cold/warm startup time, idle supervisor/executor/native memory, bounded terminal throughput, descendant accounting, and stop/cleanup latency. Keep measurements attributable to this exact profile/build; report overhead rather than inventing performance targets from source code.

**Pass:** all mandatory combination cases from WIN-01–05 are demonstrated together and the supported host/profile matrix is explicit. If a mandatory feature cannot compose, record the minimal reproducer, unchanged official artifact hashes and upstream stable capability blocker. Pipes-only partial development is labeled partial and cannot pass this experiment.

## 4. Linux experiments

### MXC-LNX-01 — Namespace, helper and public SDK admission

**Owner:** AFV2-MXC-03. **Purpose:** validate the actual .NET Bubblewrap environment and refusal paths.

Record kernel, native RID, user namespace availability, `bwrap` version, systemd/delegation/controllers and service identity. Use public V1 discovery and a real bounded spawn. Require `bwrap >= 0.5.0`. Test denied/missing namespace and helper capabilities in an isolated controlled launch environment where feasible; do not change host-wide kernel or firewall settings. Test schema/API policy validation and unsupported ingress combinations before workload launch. For network-enabled modes record slirp, ip/unshare/nsenter, firewall/restore utilities, shell, connection tracking and firewall backend. No fallback may share host networking. The published package/native unit is the one accepted in AOT-01.

**Pass:** exact public API works; all required prerequisites are accurately reported; unavailable/unsupported requests fail without a payload or policy broadening.

### MXC-LNX-02 — PTY, input, resize and structured ownership

**Owner:** AFV2-MXC-03.

Use `SpawnWithPty` with an explicitly selected Bubblewrap request inside the resource scope. Test actual `isatty`/termios behavior, shell editing and raw-mode TUI, Unicode, alternate screen, repeated resize and a foreground-child Ctrl+C case. Compare with explicit pipe mode so terminal assertions cannot accidentally pass from stream forwarding. Exercise EOF in canonical and raw modes, large output, detach/reattach with continuous draining, stop escalation and invalid dimensions. Test executable/argv POSIX serialization with spaces, quotes, shell metacharacters and Unicode; injection must never reach the host. Record structured SDK errors separately from untrusted output. Cancel a client wait and prove the run remains supervised; the lifetime wait remains active until final native cleanup.

**Pass:** real terminal and tested signal semantics, no deadlock on full output, no client-owned lifetime, correct argument values and explicit exit provenance.

### MXC-LNX-03 — Cgroup entry, enforcement and all descendants

**Owner:** AFV2-MXC-03.

Apply and read back the resource policy before launching the RunSupervisor executable through the delegated service/cgroup path. Immediately-spawning fixtures must have every child in the intended subtree before useful work. Test CPU, memory and pids enforcement plus dynamic updates, including the Bubblewrap supervisor, slirp/firewall helpers and terminal mode. Collect OS cgroup membership/counters independently, avoid ancestor double counting, and record helper overhead. Test delegated-controller absence, failed setting writes/readback and creation failure: no unbounded payload may start. A process-group kill or moving an already-running PID is not a substitute. On completion require the workload/helper subtree empty, with only explicitly identified trusted controllers remaining before their own exit/removal.

**Pass:** pre-execution placement, real enforcement/readback, no escaping descendants, correct accounting and owned teardown. Unknown/missing controller state blocks required resource capability.

### MXC-LNX-04 — Filesystem and private-network effects

**Owner:** AFV2-MXC-03.

Use explicit same-absolute-path owned directories and HOME/XDG/temp values. Test system baseline reads, writable state persistence, ungranted home/neighbor/control paths, directory/file denies, symlink escape attempts and intentional host grants. Confirm no source→different-target remap or arbitrary write redirection is promised. Do not grant host `/tmp` or the whole data-root ancestor. Exercise all-deny networking without network helpers; then qualified selected-egress/proxy mode with its real private namespace and helper set. Observe allowed/denied endpoint traffic externally. Test rejection of host/public ingress; demonstrate that a listening long-running service is not automatically host reachable. Verify IPv6 remains unavailable in the selected stable slirp configuration even when a rule names an IPv6 address. Required routes are tested concurrently with TUI and resource pressure, not in an unrestricted companion run.

**Pass:** effects match the declared profile and negative cases fail closed. A blocked required product network mode must stay a documented capability blocker, not be implemented using a host-network exception.

### MXC-LNX-05 — Recovery, combination and measured overhead

**Owner:** AFV2-MXC-03; decision reviewed under AFV2-MXC-04.

Repeat Node crash and owner-identity recovery at the same prepared/start/active/cleaning boundaries as WIN-05. Test supervisor loss, root exit with background descendants, client detach and Center loss independently. Verify native process/PTY handles stay in the surviving supervisor and cgroup ownership is not reconstructed from PID alone. Require cgroup emptiness and no network helpers before terminal completion; retained unresolved cleanup blocks data deletion. Start another Run with the same persistent Sandbox files. Finally run the combined long-lived terminal/filesystem/network/resource scenario with resize, detach, Node restart, dynamic limit update and Stop. Capture cold/warm startup, idle helper/supervisor memory, throughput and cleanup latency with actual host metadata.

**Pass:** same-profile full combination, authentic reconnect/cleanup and bounded measured behavior. No individual Linux unit test substitutes for the combined native run.

## 5. AFV2-MXC-04 decision gate

The owner assembles the signed-off experiment bundles, records their exact source and runtime versions, and selects one of these outcomes:

| Outcome | Consequence |
|---|---|
| All mandatory requirements pass together on a qualified profile | Admit only that explicit profile/host/capability matrix for product implementation. Preserve unsupported requests as refusals. |
| A host prerequisite is unavailable | Keep the relevant experiment NOT_RUN and the profile UNPROVEN; arrange the designated host/prerequisite, without claiming a pass elsewhere. |
| An official stable public/adjunct capability cannot express or enforce the requirement | Record a concrete upstream stable capability blocker and a supported remedy/release dependency or explicit product decision. Do not invent an SDK method, privately patch MXC, or instruct a later task to perform an impossible pass. |
| Only pipes or a weaker policy works | Permit only clearly labeled partial development if authorized; final full V2 acceptance remains blocked. |
| Cleanup/resource-before-exec isolation fails | Keep existing necessary execution assets, reject normal profile admission, and fix/requalify the composition before replacement. |

All mandatory terminal, filesystem, network and resource properties must coexist for each shipping profile. Passing each on different backends, OS builds, shell paths or weakened policies is not acceptance. P2–P8 delivery may not convert these unknowns into presumed facts.
