# MXC native experiment protocol

Status on **2026-11-14 UTC: every experiment below is NOT_RUN**. Official release/source/package inspection is recorded in [MXC research](../research/mxc-research.md); it is not native runtime evidence. No designated Windows/Linux verification host was available for these experiments in this Design migration.

This protocol implements [02 — MXC integration](../architecture/02-mxc-integration.md). The selected profiles are `windows-process-executor-v1` and `linux-bubblewrap-sdk-v1`, initially pinned to official **1.0.1**, stable schema **1.0.0**. Windows uses the unchanged official executor, C# Native AOT ConPTY supervision and an outer ArcForges Job. Linux uses the official typed .NET SDK inside the established cgroup boundary. No private fork, custom MXC build, test-only forced tier, substitute backend, or plain-pipe terminal claim is acceptable.

**Historical update 2026-11-16 UTC:** MXC-AOT-01 ran and **FAILED** the then-selected Linux 1.0.1 request-environment argv privacy check. Pipe/PTY execution passed and the owned scope was cleaned. That report is unchanged. **Owner decision 2026-11-17 UTC:** trusted local host visibility of explicitly requested environment values is not a standalone blocker; F-AOT-01 has a fresh **bounded Windows/Linux native cohort PASS**. Node PR93 merged after Windows15/Linux20 required checks and independent review. See the [dated revalidation checkpoint](#mxc-aot-01-revalidation-checkpoint--2026-11-17-utc). The [Linux full-profile checkpoint](#linux-full-profile-native-checkpoint--2026-11-17-utc) records native72/72 at50e602a8.

The [2026-11-18 amendment](../decisions/AD-0022-cli-sandbox-platform-pivot.md#official-mxc-wrapper-boundary--2026-11-18-amendment) defines the Windows MVP qualification below. The [Windows local wrapper checkpoint](#windows-local-wrapper-native-checkpoint--2026-11-18-utc) records 60/60 required native cases at Node `fac982f`, including WIN-06 against a calibrated local peer. The [earlier Plan evidence record](https://github.com/ArcForges/Plan/blob/f4767f08176526ec309de45ca10b0b361fd82e1a/docs/afv2-mxc-02-progress.md) retains the diagnostic 59/59 at `cb0396b`, the original external selected-egress attempts and the unrun external combined cases. External selected egress remains unverified on the designated host. The [AFV2-MXC-04 profile admission](#afv2-mxc-04-profile-admission) uses the final Windows and Linux source receipts.

## 1. Ownership and evidence rules

| Experiment set | Plan owner | Platform register | Current result |
|---|---|---|---|
| MXC-AOT-01 | AFV2-MXC-01 | F-AOT-01 | COHORT NATIVE PASS — fresh Windows/Linux 9a evidence under the amended criterion; Node93 merged after exact-head required checks; original825 FAILED report retained |
| MXC-WIN-01 through MXC-WIN-06 | AFV2-MXC-02 | A-MXC-01 / F-MXC-01 | NATIVE PASS — 60/60 required workstation cases in the final `da7f5bf` [admission receipt](#afv2-mxc-04-profile-admission). External selected TCP/UDP and its dependent combinations remain unverified. |
| MXC-LNX-01 through MXC-LNX-05 | AFV2-MXC-03 | A-MXC-02 / F-MXC-02 | NATIVE PASS — H-22 full profile `50e602a8`, six groups and 72/72. See the [scoped admission receipt](#afv2-mxc-04-profile-admission). |
| Profile decision | AFV2-MXC-04 | Required matrix for each profile plus F-AOT-01 | [Scoped official profile admission](#afv2-mxc-04-profile-admission) with exact evidence, predicates and limitations. |

Use the designated native Windows and native Linux verification hosts and the repository's normal exact-commit verification procedure. An agent sandbox, WSL, container imitation, source unit test, mocked SDK, or successful CI compilation is not native combination evidence. Do not post successful platform statuses by hand. If a host/dependency is unavailable, preserve `NOT_RUN` with its reason and owner; do not downgrade the acceptance criterion.

Each result bundle contains:

- Experiment ID, exact ArcForges/Design/Plan commits, official package/native/executor versions, runtime file hashes/signatures, selected profile revision, command/fixture hashes and redacted policy hash.
- Host architecture, Windows build/PSEC request probe or Linux kernel/cgroup/user-namespace/helper versions, service identity and inherited resource-scope description. Redact personal paths and secrets in exported records.
- Expected result and actual result for each case, native/API return values, trusted process/resource observations, terminal byte trace where useful, resource readback, cleanup proof, elapsed-time measurements and limitations.
- Run ID, boot identity, supervisor process-start identity, owner generation, scope identity, state transitions, exit-source/start-certainty/stop-reason fields, and any gap or cleanup failure.
- Separate labels for official source support, observed passes and failures, unverified behavior and unavailable or unrun cases. Trusted host observations establish isolation, start identity, resource membership and cleanup.

Use disposable, uniquely owned fixture directories and synthetic data, never real credentials or another user's files. Test processes have modest bounded CPU, memory, child counts and lifetimes; a trusted external observer/cleanup owner is ready before starting them. No global firewall/namespace/sysctl changes, DACL host preparation, or broad host filesystem grant is part of this protocol. Prerequisites are explicitly provisioned through normal host administration, not silently repaired by the test harness. Capture pre/post state for every resource the experiment owns.

## 2. MXC-AOT-01 — Official package, AOT and distribution

**Owner:** AFV2-MXC-01. **Evidence basis:** V-MXC-01/02/07. **Purpose:** prove the exact official distribution works with a real ArcForges Native AOT owner, rather than treating the upstream JSON-only smoke sample as a native test.

1. Resolve the locked `Microsoft.Mxc.Sdk` 1.0.1 package and official v1.0.1 native unit. Check the current official release metadata before running; an upgrade is a new reviewed pin. Verify package contents and lock integrity, release ZIP digest, and Windows signatures on the actual host. Record every shipped native/sidecar hash and license/third-party notice. Confirm no unreviewed source rebuild, Node runtime or executable from ambient PATH is used.
2. Publish the bounded experiment supervisor with Native AOT for each candidate shipping RID. Run the published output from a clean installation location without an SDK/JIT dependency. Inspect trimming/AOT diagnostics and native dependency resolution; reject missing/unexpected files rather than masking it with development PATH or `MXC_FFI_DIR` overrides.
3. Call public `MxcPlatform.NativeVersion`, `GetPlatformSupport` and `GetAvailableBackends`. On Linux perform an actual pipe and PTY spawn/wait/cleanup through V1. On Windows load/probe the package where used and run the unchanged executor through the intended host launcher. Record process behavior, not just successful JSON serialization.
4. Validate mismatch detection with a deliberately incomplete private staging copy and an incompatible recorded manifest; no workload may run. The experiment never modifies a shared installed runtime. Check Unicode/space-containing installation and request paths, noninteractive service context, and absent global PATH helpers where the profile promises explicit resolution.
5. Apply per-request optional telemetry disabled for the selected stable version. Verify an offline local start and completion with no Center login/subscription. Use synthetic secret sentinels to inspect ordinary logs and native process visibility, recording only redacted observations and observer authority. Explicitly requested inputs visible to trusted host user/administrator inspection are permitted by the [local process boundary](../architecture/08-security-trust.md#trusted-local-process-inspection) and do not alone fail admission. Unexpected host credential inheritance, unauthorized payload/cross-boundary access and raw secret disclosure in ordinary logs or exported/public records remain failures. Document any remaining official-runtime artifacts or required telemetry behavior before accepting a newer pin.

**Pass:** real published native execution and cleanup on each advertised RID, coherent verified official artifact set, license/distribution manifest and offline local behavior. Package metadata or the upstream reflection-free JSON smoke alone cannot pass. Unavailable architectures remain unqualified and must not be advertised.

### Admission progress — 2026-11-16 UTC

AFV2-MXC-01 is active. H-22 independently downloaded the exact official 1.0.1
release ZIP and NuGet package; the ZIP matches freshly checked official metadata,
and all five x64 native files match between those two distributions. Exact
hashes and the same-host receipt location are in
[mxc-sources.json](../research/mxc-sources.json), `admission_progress`.
The bundled x64 SPDX 2.2 manifest digest matches, but its package licenses are
`NOASSERTION`; this is an inventory observation, not license closure approval.
User namespaces and Bubblewrap 0.12.0 are available on the actual native venue.

At this artifact-only checkpoint the probe had not been published or executed.
The following dated result records the subsequent real execution and rejection.
Every complete profile-composition experiment remains NOT_RUN.
Official 1.1.0 was published after the original research baseline; it is recorded
as a separate observation and is not selected by this 1.0.1 probe task. Any new
pin still requires its own coherent artifact, privacy and native review.

### Native negative result — 2026-11-16 UTC

The designated H-22 host independently fetched candidate
`8252c8fc13d5973b27ab76bc18726eab8f21cb96` from GitHub
([Node draft93](https://github.com/ArcForges/ArcForges/pull/93)). Locked restore
and linux-x64 Native AOT publish with the retained LLVM/binutils selector passed
with **0 warnings/0 errors**. Its probe SHA256 is
`d2465732a29fff4edd0d20b8017d3ed9f665254b67fa0af7005f0452d8b45663`;
the official native payload remains the pinned hash above.

A fresh Unicode/space installation was staged from the exact official ZIP and
NuGet. The native executable ran without invoking dotnet, Center or a login,
inside owned systemd user unit `arcforges-mxc-aot-825-26b98458`, with Delegate,
45s runtime, 256MiB memory, 64 tasks and 100% CPU quota bounds. These are experiment
bounds, not product resource qualification. The same-host evidence directory is
`ArcForges/.worktree/afv2-mxc-01-8252c8f/artifacts/mxc-01/`.

| Observation | Actual result |
|---|---|
| Public native version/support/backends |1.0.1 / supported / Bubblewrap |
| Pipe/stdout/stderr | PASS; PID3026303, exit0, native wait and PID absent |
| Real PTY `test -t` | PASS; PID3026310, exit0, native wait and PID absent |
| Owned argv privacy under the 2026-11-16 criterion | **FAILED** in the original report; actual native PID3026318 observed the synthetic request-environment sentinel in argv; only the boolean is exported. The 2026-11-17 decision supersedes its argv-only blocking interpretation. |
| Kill/wait and cleanup | Kill/native wait completed, PID3026318 absent; all recorded PIDs absent; unit inactive/not-found, empty ControlGroup |
| Invalid private stages |4/4 PASS: missing native file, incompatible manifest, unexpected member and loader override all reject before fixture/native work |
| Probe owner idle |1s observation: 0.949ms CPU, 14897152 bytes working set; no product target claim |

`linux-report-825.json` SHA256 is
`2d9fbd329c481e77912a9df5b566a96590eba1aa8c8591f196d9c3664310eafe`.
The context, publish/staging/unit/cleanup logs and negative reports stay on the
originating host; `mxc-sources.json` records their identities. Initial candidate
676 produced the same native privacy refusal and is preserved separately.

Windows native observations at the same exact 825 source are also preserved:
zero-warning win-x64 AOT; all five official native signatures valid; five actual
executor/Job-zero/argv-readback cases and four invalid-stage refusals passed.
The process ran with only System32 on parent PATH and an absent DOTNET_ROOT;
the PE has no CLR directory and actual module observations contain no
CoreCLR/JIT/hostfxr/hostpolicy. The exact same-host summary is
`ArcForges/.worktree/afv2-mxc-01/artifacts/mxc-01/windows-author-8252c8f-summary.json`,
SHA256 `18bb697dd27f4ae5afce757a2dd19ddb49dd32c6c21ed2afb175b9dec31dc5d7`.
The native probe SHA256 is
`23b9bae909c4bbaa638b5c1985d202e1e22ac6dc9aa28191b0bcc77d6b3a5370`.
First sequential fresh-process launch-to-Main was 66.632ms; the next four had
p50 10.818ms, with discovery p50 2185.811ms. No OS caches were cleared, so this
is not a cold-cache or product-performance claim. Per-case idle CPU/RSS and
all signatures/reports remain in the originating artifacts. This **nonterminal**
launcher does not qualify ConPTY or a complete Windows profile.

The preserved Node draft head is now
`4382988ce5b5ea40f4eb4583534a18bb135d371a`, only whitespace formatting after 825;
native observations remain bound to 825 and are not relabelled as 438 results.
Independent review and documentation repository gates record a failed admission;
they cannot turn the rejected Node candidate into a delivered product task.

Under the criterion applied on 2026-11-16, this actual observation rejected the
selected cohort. It was not a host-connectivity or helper-availability failure.
The later official 1.1.0 source also constructs request environment entries as
`--setenv key value`; that bounded source check did not admit or execute 1.1.0.
The original rejection and reports remain historical evidence, with their
interpretation superseded only as described below. Preserve the Node draft and
necessary old runtime until the applicable replacement checks pass; pipe/PTY
success alone still does not admit a full profile.

### Owner decision and resumption — 2026-11-17 UTC

The [AD-0022 amendment](../decisions/AD-0022-cli-sandbox-platform-pivot.md#local-process-visibility--2026-11-17-amendment)
records the owner's explicit decision to permit trusted local user/administrator
process inspection of intentionally supplied request environment values. The
observed boolean remains true; the old native report remains FAILED under its
original assertion. That argv-only assertion is no longer a product admission
requirement. Do not suppress the observation, silently inherit host credentials,
permit unauthorized payload access, or copy raw secrets into logs, public Plan/
GitHub records or evidence.

AFV2-MXC-01 may resume with F-AOT-01 pending revalidation under the amended
criterion, the retained official 1.0.1 pin and its existing package/license/AOT/
offline/cleanup requirements. Record a fresh candidate and actual validation
results; this decision does not relabel 825 or formatted 438 as a passed run.
Full Windows/Linux profile experiments and warm performance qualification remain
pending under their existing owners. Other authorized tasks remain governed by
their actual dependencies, not by the superseded trusted-local argv blocker.

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
3. Use disposable local controls to exercise the default-deny policy and the applicable host-loopback and ingress behavior. Record the exact official request, native preflight, launch/result and observed local effects. Verify a concrete refusal for an incompatible policy. A denial observation requires a local positive control and an independent outcome observation. Preserve the original external selected TCP/UDP attempts and unrun cases as evidence. A reachable external peer, proxy or route change is outside the Windows MVP matrix.
4. Run the TUI, resize and bounded resource pressure while exercising the filesystem and applicable local policy checks. Snapshot relevant host DACLs before and after. Verify enforcement remains until the last workload descendant is gone.

**Pass:** allowed and denied filesystem effects and the required local policy controls match the declared profile while terminal and resources remain active. The receipt states the scope of the observations, including the unverified external network cases.

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

Run one bounded long-lived multiprocess terminal workload with the required local filesystem and default-deny network policy and live CPU/memory/process limits. Observe the default-deny network effect in that Run using a calibrated disposable local peer and independent observations. Exercise resize, attach/detach, Node restart/reconnect, a limit update, then Stop and complete cleanup. Retain the external selected-egress variant as unverified when no qualifying receipt exists. Capture cold/warm startup time, idle supervisor/executor/native memory, bounded terminal throughput, descendant accounting, and stop/cleanup latency. Attribute measurements to the exact profile/build.

**Pass:** the same native Run demonstrates terminal behavior, filesystem/control isolation, the default-deny network effect against the local peer, resource limits/readback, ownership, recovery and cleanup. Record the scope of the network observation and the exact host/profile matrix. If a required property fails, retain its original observations and artifact identity. Record an upstream stable capability blocker only when established by the evidence.

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
| All mandatory requirements pass together on a qualified profile | Admit the exact profile/host/capability matrix. Record actual unsupported requests as refusals. |
| A prerequisite for required local/native behavior is unavailable | Keep the affected required cases NOT_RUN and the corresponding profile UNVERIFIED. |
| A Windows external selected-egress case or dependent combination has no qualifying native evidence | Retain the observations and mark the affected capability UNVERIFIED. The local MVP matrix and dependent delivery can proceed when their applicable required evidence passes. |
| The official contract cannot express or enforce a required property | Record the concrete refusal or capability failure and the supported remedy, release dependency or explicit product decision. |
| A mandatory terminal, confinement, resource-before-execution or cleanup property fails | Keep the affected profile unadmitted and retain existing necessary execution assets until the required replacement passes. |

Each shipping profile needs its mandatory properties together on the same backend, host and applicable policy. The optional Windows external result stays separate throughout P2–P8, including release acceptance.

## MXC-AOT-01 revalidation checkpoint — 2026-11-17 UTC

The fresh bounded Windows/Linux native AOT cohort **passes** under the amended
criterion at Node `9a9378bc3a6bc8190d896ca7ef0e43eee5abd886` (tree
`4b8785f999505582558c85019bdceb7b4952cf7e`) and Design policy
`4bc1d2be8916a961d167b4965e30e45bc3023ef1`. At that native checkpoint the Node source had not merged. The subsequent final
source checks, review and actual merge are recorded below.
The original 825 failed observations and every historical report hash are unchanged.

DEKU native Windows 10.0.26300 published win-x64 Native AOT with **0 warnings/
0 errors** (9.85s). Probe SHA256 is
`ab9486fd2dd58cf8e6c9bc328f802aff66f64bdbd997c7012400e6065e7bf1ad`;
stage manifest SHA256 is
`dc0bfb3708e1994f1ddf5714a5bd30f8f7d0149af6ecf519d96c06271040a34c`.
All ten staged file hashes and the actual **5/5 Valid Microsoft Corporation**
signature receipt were checked. The PE has no CLR directory, with only System32
on parent PATH and an absent DOTNET_ROOT fixture. Five fresh owners discovered
native 1.0.1/BaseContainer and each ran the unchanged official executor to exit0,
with Job assignment/readback before resume and zero active Job processes after
wait. All five executor argv observations were sentinel-free. Four invalid-stage
cases rejected before stage verification or fixture/workload creation.
The same-host Windows summary is
`ArcForges/.worktree/afv2-mxc-01/artifacts/mxc-01/windows-author-9a9378bc3a6b-revalidated-summary.json`,
SHA256 `9e1676addeedbbb465a4a0e0f1544220fc76a095db815075907167fd6355f12e`.

H-22 published linux-x64 Native AOT with **0 warnings/0 errors** (10.89s).
Probe SHA256 is
`d3ff0a71a3a9614e360dbeb4011c8fee88268a74dfdf581bd8cc6b3e4218557c`;
stage manifest SHA256 is
`2a9df34d5e78d232ee81f5f4f7ed7b55052428eca61dc746281eddb7849ecf2a`.
Five staged members retain the pinned official 1.0.1 unit. Five owned user-service
processes each passed real pipe/stdout/stderr, PTY and kill/native-wait cases;
all five owner exits were 0. Native library mappings were observed and no JIT
runtime mapping or exported sentinel hit was recorded. Four invalid-stage cases
rejected before stage verification or fixture/workload creation. The Linux
same-host summary is
`ArcForges/.worktree/afv2-mxc-01-9a9378b-native/artifacts/mxc-01-native-9a9378b/summary.json`,
SHA256 `e499109bd69dd5476522c0fd1996a999e5dfdad745941c3aeea37a461dc9781b`.

PID cleanup evidence uses the probe's internal `/proc` assertions with the actual
`processId` values and independent originating-host read-back of all15 recorded
PIDs. Pipe/PTY reports have a null supplemental `processAbsentAfterWait` field;
the five kill/wait reports record it true. The driver's auxiliary `casePidsAbsent`
check used a nonexistent `pid` key and supplies no independent cleanup evidence.
Trusted host-user argv inspection recorded the requested-environment sentinel in
four kill/wait observations and not in the fifth; only these booleans are
exported. This observation is permitted by the amended boundary and is retained.

Originating-host reports, negative summaries, signature receipt and publish logs
are identified by hash in [mxc-sources.json](../research/mxc-sources.json),
`admission_progress.revalidation_2026_11_17`. Independent native evidence review
passed; the separate final exact-head required Node profiles are recorded below.

Windows first fresh-process launch-to-Main was44.269ms; the next four had
p50 10.824ms and native-discovery p50 2177.940ms. Linux first whole-process wall time
was 1125.462ms; the next four had p50 1117.151ms, including discovery, the one-second
idle observation and all three workloads. No OS cache was flushed. Per-run
owner-idle CPU/working-set observations remain in the reports. These bounded
measurements establish no cold-cache claim or product performance target.
Windows ConPTY, Linux resource composition and complete shipping profiles remain
with AFV2-MXC-02/03 and are **UNPROVEN** here.

### Final repository verification checkpoint — 2026-11-17 UTC

The final Node source candidate is
`d460524d7fa23e1558fc7ddd5e4a3c31e66e71d6`, tree
`14c754b7da091eb4e0630fa2350d0a1dcde322bc`. Its native Windows **full profile
passed 15/15 steps in 2102s**, with all 15 recorded log hashes verified by the
coordinator against the original same-host files. The summary is
`ArcForges/.git/arcforges-verify/logs/20261117-123248-d460524d7fa2-win/summary.json`,
SHA256 `ec87c1c6b9413d6303993e663f4272782667ca8ca127ed89eea4f1f048fbe438`.
Linux R2 passed **20/20 steps in 1950s**, with all20 original step-log hashes
verified by the coordinator and independent reviewer. Its summary is
`ArcForges/.git/arcforges-verify/logs/20261117-125046-d460524d7fa2-linux/summary.json`,
SHA256 `089e7ca23191e06df55bc240ac10f06c547ad6411b42c511c57e96490b4ea8f1`.
[Node PR93](https://github.com/ArcForges/ArcForges/pull/93) merged as
`b2ebace5c15a130b13a7dbd02fd9900e4983c6e8`, with the identical verified tree.
[Independent final review](https://github.com/ArcForges/ArcForges/pull/93#issuecomment-6939445328)
accepted the full source and original evidence. No main-push workflow run or
public distribution/deployment occurred; complete profiles remain unqualified.
These repository results do not change the earlier 9a native probe, stage or
report identities.

The first Windows attempt at the same source remains **FAILED**: `win-publish`
refused its localized Chinese zero-warning/zero-error summary because the warning
count parser expected English. Its original summary is
`ArcForges/.git/arcforges-verify/logs/20261117-122129-d460524d7fa2-win/summary.json`,
SHA256 `4833c841042bccaaea2f4c184190eeaac5ce4c236580e03a0b74f950c4b4207e`.
The failed attempt and its publish log are retained separately from the later
15/15 pass. The first Linux full leg also remains FAILED: its pressure fixture
waited90s for a fourth Normal task before allocation, and the aggregate exclusive
suite reached900s. The original fixture was disposed, so the original admission
cause is unknown. A bounded unchanged single case and both JIT/native cases in
full R2 passed; no source, assertion, timeout or CPU override was changed.
Original failure, diagnostic and final receipt identities are in
`admission_progress.revalidation_2026_11_17.final_repository_verification` in
[mxc-sources.json](../research/mxc-sources.json).

## Linux full-profile native checkpoint — 2026-11-17 UTC

The `linux-bubblewrap-sdk-v1` full invocation **passed 72/72 recorded cases** on
the designated native H-22 (`v2202601329473427941`, UID1000), exit0 with
`qualificationPassed=true`, `cleanupConfirmed=true` and no unrun group. The
whole invocation took 87.749s; its original receipt covers
2026-11-17T16:55:36.2679558Z–16:57:04.0021302Z. This is the native experiment
checkpoint at the source below. It does not assert completed Node repository
checks, a merge, publication, product runtime cutover, or the AFV2-MXC-04
profile-admission decision. Final integration source
`022946a305e505e5817162c79a956c7816b99b12` differs only by initializer formatting;
independent review confirmed unchanged C# tokens and non-whitespace bytes.
That integration does not change the source/artifact identity of this original
native evidence or substitute for final-head repository checks.

| Identity | Exact value |
|---|---|
| Node native source / embedded AOT source | `50e602a83ece2c4de75d8dbd32777c7833a6eaf7` / `0.1.0-dev+50e602a83ece2c4de75d8dbd32777c7833a6eaf7` |
| Design / Plan invocation baselines | `af28dc6378d91d678870abc628362476611efa32` / `cf937ddc1c52778007bdc0980a1ae139c809d25f` |
| Full Run ID | `7eb7b9726a6a4b5d974d20fdadd3df8d` |
| Full receipt SHA256 | `57f41658b57c18ff350fde2a9afc428c9434946b1aa829735325336019288fcf` |
| Full driver events SHA256 | `3b85f0b9475972bcdd6bb8bf6508ff7113f657493b79185556cfd3eb0bfe2d48` |
| AOT executable SHA256 | `eda60f8c071559985f88d17e1d6722f1be1f6b48a87b0845befc425496d99e7c` |
| Stage manifest SHA256 | `5eedcd1733c25a38545d77f9f1d9f2d9aae1bee04d07b71584272c08f3f02616` |
| Official SDK / schema / native source | `1.0.1` / `1.0.0` / `fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2` |
| Official package / release ZIP SHA256 | `d47b1f70c3fcaaed1705a0c3872807e2878fe8c1b778c0dd9eb9325bf421a672` / `0e832239454ba7fcd338ff56218a287eef4c0a01c1484084b869f55feff8abe9` |
| Official `libmxc_ffi.so` SHA256 | `18a1cba8f2980af79570141c4eec9cd3982872162ae6b63634d45862913002bc` |

The original H-22 repository-relative evidence directory is
`ArcForges/.worktree/mxc03-author-50e602a83ece/artifacts/mxc-03/`: retain
`full-native-01.json`, its `.events.jsonl`, `full-native.log`,
`author-summary.json`, toolchain/restore/build/publish/stage logs and
`full fixture 01/`. The full receipt binds each group's report/event-log hashes,
official stage members and actual case results. Owner/control evidence stays
private; publish summaries and identities rather than whole control records.
The Native AOT publish log has 0 warnings/0 errors; its SHA256 is
`007ef021d5b7e5ada0ce97e1e03385978076ecfcce4ae4ad7d4f470ebc21749f`.
The launcher's generic `author-summary.json` purpose text is not the full result;
the explicit full receipt above is authoritative for the native combination.

H-22 was Debian 13 x64, kernel `6.12.63+deb13-amd64`
(`#1 SMP PREEMPT_DYNAMIC Debian 6.12.63-1 (2025-12-30)`), with actual user-manager
version `257.9-1~deb13u1`. Actual helper observations include Bubblewrap 0.12.0,
slirp4netns 1.2.1, iproute2-6.15.0, util-linux 2.41, and iptables/ip6tables/restore
1.8.11 using `nf_tables`; shell identity is the resolved dash executable/hash
and successful POSIX probe, not an invented `sh --version`. The admission log
records exact helper paths, hashes and banners; `nf_conntrack` was listed, which
alone is not a functional connection-tracking test. Real selected-network
effects supply the runtime evidence.

| Group | Recorded pass count | Observed scope |
|---|---:|---|
| admission |4/4| Public SDK discovery; helper identities; actual user/pid/mount/net/ipc/uts namespace differences; independently gated child with missing bwrap refused by SDK BackendError12 without payload/fallback |
| terminal |17/17| Native PTY/pipe distinction, canonical/raw input, Unicode/resize, actual foreground-child SIGINT, EOF/escalation, 2MiB output/replay gaps, client cancellation, POSIX argv, shell editing and explicit exit provenance |
| policy |12/12| System baseline reads; owned RW/RO/denied paths, symlink escape refusal, explicit host grant, clean environment/HOME/XDG, persistent second Run, invalid environment and unsupported ingress refusal |
| network |10/10| Default-deny TCP/UDP without helpers; selected literal IPv4 TCP/UDP; denied address/port/protocol and DNS; private listener not host reachable; IPv6 remains unavailable even with an allow rule |
| resource |13/13| Pre-execution membership/readback; CPU comparison and dynamic update; real pids-max/OOM enforcement; bounds/existing-unit/readback/native setter/controller-absence/pre-exec creation refusals |
| lifecycle |16/16| Seven Node crash boundaries; authentication/generation/writer rules; independent client/Center loss; supervisor loss; root-exit descendants; retained cleanup/deletion refusal; two persistent Runs; default-deny and selected combined scenarios |

Ordinary owners had actual pre-SDK readback `cpu.max=50000 100000`,
`memory.max=536870912`, `pids.max=128`, with memory swap disabled. Resource cases
used separately owned services: 250/1000millicore CPU comparison, 32 tasks for
pids pressure and 96MiB for memory pressure. The OS recorded six pids-max events
with the real process-creation refusal and one `oom_kill`; the identity-bound owner reports
also completed successfully. The CPU comparison measured 248.534 versus
1001.267 CPU microseconds per elapsed millisecond. Dynamic readback and the
combined 500→250millicore update were observed. The controller-absence negative
used only a fresh private slice, observed missing child `cpu.max`, and refused
before owner admission; its trusted pre-exec process had memory/tasks guards
and a 5s deadline. The native creation negative recorded systemd 200/CHDIR.
No shared slice, host firewall/sysctl, credentials or host network setting was
changed. All six groups confirmed owned cleanup; held cgroup identity and
emptiness, not PID disappearance or workload text alone, establish that result.

The same-source full invocation includes the long-lived raw-terminal/owned-files/
network/resource scenarios under both default-deny and selected-egress policies.
An internal ready gate starts network/filesystem operations only after actual
memory touches and children are ready; the observer checks the recorded ordering
against the load lifetime as well as native cgroup/namespace identities and
external peer counters. Resize, detach, Node replacement, dynamic limits and Stop
preserved the same authenticated native/PTY owner until cleanup. The controlled
network peer is outside the payload's private network namespace on H-22, in the
same bounded owner cgroup; no Windows-to-VPS data channel is part of this proof.

### Measured overhead and limits of interpretation

The following values come from the original lifecycle receipt's
`LNX05-combined_default_deny` and `LNX05-combined_selected` facts. They are
descriptive bounded observations, not new performance thresholds.

| Measurement | Default deny | Selected IPv4 TCP |
|---|---:|---:|
| Owner service ready (`serviceReadyMs`) |155.681ms|157.376ms|
| Official native spawn (`nativeSpawnMs`) |4.958ms|79.285ms|
| Actual idle measurement window |1010.809ms|1013.665ms|
| Owner RSS snapshot |21,471,232bytes|21,540,864bytes|
| Aggregate cgroup `memory.current` snapshot |10,719,232bytes|11,395,072bytes|
| Aggregate idle CPU delta / native members |15,278µs /4|16,822µs /6|
| Observed terminal bytes / actual window |4,150bytes /3109.251ms|4,046bytes /3157.394ms|
| Window terminal throughput |1334.721bytes/s|1281.428bytes/s|
| Stop, native/helper drain and owner-final report |276.700ms|405.198ms|

`serviceReadyMs` runs from before manager service creation through verified
owner-ready identity/scope, before payload admission. `nativeSpawnMs` measures
the official SDK spawn through native PID validation, before stream acquisition;
each lifecycle case uses a fresh owner and its first spawn. The terminal owner's
first spawn-to-stream-ready event envelope was 10.0591ms; its next 16, across the
different fixed cases, ranged 4.7185–17.7631ms. Those envelopes include stream/
drain setup and logging boundaries. This defines first/subsequent-owner-process
observations explicitly; no OS cache was flushed, and these are not matched
cold-cache/warm-cache benchmarks.

The idle window rejects a workload-start event during measurement. Per-member
RSS snapshots remain in the receipt and must not be summed as unique memory or
equated with cgroup charges. Terminal throughput uses the output-cursor delta
over a window that includes idle, restart/reconnect, resize and fixture startup;
it is not peak throughput. Stop timing ends at validated owner-final reporting;
the later outside-driver service Stop/empty-scope verification is separate.
The supervisor-loss case observed original held-cgroup emptiness 11.094ms after
the main-process kill operation returned. Original cleanup proofs remain in the
driver events independently of these latency observations.

The namespace-denial fault remains **NOT_RUN** under LNX-01's where-feasible
clause: no safe independent denial injection was available without host policy/
credential changes or adding a seccomp framework. Actual positive namespaces and
the isolated missing-helper refusal passed; they do not fabricate a denial pass.
DNS evidence is a single real bounded UDP53 query through the sandbox's configured
resolver that produced native refusal or no response under the selected denying
policy. There is no independent upstream packet count or delivery assertion.
Allowed DNS, domain-name policy semantics, proxy mode and public ingress are not
qualified. IPv6 had no routable address in the selected stable private namespace
and the allow-rule request remained unreachable. The receipt qualifies only this
official 1.0.1/cohort/H-22 experiment; Windows, other Linux hosts, reboot recovery
and later product acceptance retain their separately owned evidence obligations.
All earlier failed or partial receipts and their original hashes remain intact.

## Windows local wrapper native checkpoint — 2026-11-18 UTC

The exact-source `windows-process-executor-v1` wrapper invocation passed
**60/60 required cases** on DEKU, Microsoft Windows build `10.0.26300`,
x64. Exit was 0 with `wrapperQualificationPassed=true`, confirmed owned
cleanup, verified stage and final identity, and an observed driver Job
context. All six protocols were complete. The report lists zero missing,
duplicate, unexpected or failing cases. The elapsed time was 62.912 seconds.
The original report covers 05:24:31.0808091–05:25:33.9240778 UTC.

| Identity | Exact value |
|---|---|
| Node source and embedded AOT source | `fac982f628799c8905ea911bd949355072a4d2a7` and `0.1.0-dev+fac982f628799c8905ea911bd949355072a4d2a7` |
| Design / Plan invocation baselines | `529d3154317178fb7eed50f2a9192281bb2f4b2d` / `6a7ecc46c47c27fc9673b75b4023023bdebd6946` |
| Run ID / profile revision | `af8b9d5949f541f78397a1264119c2a7` / `win-wrapper-local-v1` |
| Wrapper receipt SHA-256 | `d822ef2c65d8f6c12bb57d1d2b1f638a5be88b4d8de5618fbb614bd6c1dcbca4` |
| Driver events SHA-256 | `94f7aa7ff27f0ab52678d762d5a3f9f5a8639b9334dcd62fdda2c038721735dd` |
| Driver Job context SHA-256 | `3fff96853b8b35abb198cb40d4730797cd6f4d5f636b7187a0abbd2c5ca202c4` |
| AOT executable / stage manifest SHA-256 | `79ca3c1e4f107dd96ac2f2a0a7f41965a4f9a92115c32d11fccb4d725a9f891f` / `9eec347151404510831bc05d5c67c522c17da608c52831b1164527fc9e8ea60e` |
| Official MXC version / schema / RID | `1.0.1` / `1.0.0` / `win-x64` |
| Official native source | `fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2` |
| Official package / release ZIP SHA-256 | `d47b1f70c3fcaaed1705a0c3872807e2878fe8c1b778c0dd9eb9325bf421a672` / `0e832239454ba7fcd338ff56218a287eef4c0a01c1484084b869f55feff8abe9` |
| Official `wxc-exec.exe` SHA-256 | `090f5d1f7bb93104ab08dcd4e8034ef954aeefcdaf6658dde5f7dff4cfc12f3a` |
| Combined policy / observation SHA-256 | `136052983aa167c3a3c9162376952451e8080d3b417e7702ff2c48917e4567f0` / `9e00538979494621f53b42304253897bfa82ffb1e82d6987e108de22e255302f` |

The original repository-relative evidence directory is
`ArcForges/.worktree/m02-wrapper-fac982f/artifacts/native-fac982f/`.
Retain `wrapper.json`, the driver events and Job context, `wrapper.launch.json`,
`wrapper.log`, verified staged artifacts and the owned fixture receipts.
The wrapper used `--windows-profile --manifest <manifest> --work <fresh-dir>
--report <fresh-file> --source <Node> --design <Design> --plan <Plan>`.
The worktree's `wrapper.audit.json` verifies the combined policy and observation
against the original report. Publish hashes and bounded observations from the
private controls.

| Protocol | Cases passed | Observed scope |
|---|---:|---|
| WIN-01 | 7/7 | Official request, policy and tier refusal cases and argv roundtrip |
| WIN-02 | 15/15 | ConPTY and interactive shell, resize, input, detach/replay and exit/control observations |
| WIN-03 | 9/9 | Pre-execution Job assignment, limit/readback, child burst, measured enforcement, live update and refusal |
| WIN-04 | 13/13 | Filesystem/control isolation, owned and granted data, local CLI and six loopback/ingress cases |
| WIN-05 | 15/15 | Owner/client loss, child drain, cleanup and persistent data |
| WIN-06 | 1/1 | Same-Run ConPTY, file/control effects, default-deny against a local peer, resources, recovery and confirmed cleanup |

`combined-local-host-loopback-deny` used egress default deny, ingress default
deny, host loopback deny and `fallback.allowDaclMutation=false`. Ordinary
Windows calibration advanced the local TCP peer's receive and matching
counters from 0 to 1. Both remained at 1 after the contained attempt.
The workload performed the network attempt and ten filesystem checks
after the pressure fixture was ready, with the same payload's native Job
membership independently observed. Six processes and 70,258,688 bytes of peak
aggregate commit were observed at readiness. All 16 recorded DACL snapshots
were unchanged. The same owner was rebound, ConPTY resize and Unicode output
were observed, and resource readback recorded CPU rate 2500, memory 805,306,368
bytes and process limit 12 after the update. The official executor exit was
125 for this Stop path, and the held Job was observed empty at cleanup.

The first and subsequent executor spawn-through-resume observations were
4.340 and 3.2825 ms on separate ordered cases. In the combined case, admission
through console readiness was 393.2202 ms. The idle sample window was 1,021.6485
ms, the terminal replay window recorded 171 bytes in 81.6838 ms, and Stop
through cleanup took 59.7187 ms. These observations describe this run and
measurement windows. The driver recorded immediate inherited Job context.
Ancestor Jobs were not enumerated by that snapshot. Cases with an owned
Job use its native handles to verify assignment, enforcement and cleanup.
The missing-policy case records the official executor's configuration
rejection, identity, exit and cleanup.

The report retains `qualificationPassed=false` and
`externalNetworkStatus=unverified` for the separate external mode. The
local peer result covers host loopback only. Original external attempts and
unrun combinations remain separate. The lower-capability-host case remains
NOT_RUN because a designated host was unavailable. Deterministic official
refusal cases passed. Repository checks and review, merge, publication and
AFV2-MXC-04 product admission are separately recorded delivery steps.

## AFV2-MXC-04 profile admission

The admission decision uses the original composed native evidence in AR-01 and AR-02, with the isolated native AOT and distribution evidence from AR-03 / F-AOT-01. The [profile register](platform-capabilities.md#qualified-official-profiles) states the conditions under which these receipts qualify the Windows local wrapper and Linux Bubblewrap.

| Qualified profile and evidence | Exact source and original receipt | Artifact identifiers in the receipt |
|---|---|---|
| `windows-process-executor-v1`, revision `win-wrapper-local-v1`. DEKU, Windows NT 10.0.26300.0, win-x64. 60/60 with owned cleanup. | Node `da7f5bfcfe497a35cece41f0e97b5863481bcc56`, Run `423f8c4c5456443da4b9c10be3d744c4`, receipt SHA-256 `f7f9914550d3f9cbf0933735e8703a36e8b16312ac9c6521f1f9dd3dedceb1ef`. | Stage manifest SHA-256 `e410036bce3097242d2daa07236dbf7b36b553b71b99a8f4a95e1d2c625a1e06`, AOT probe SHA-256 `ff573694e4aeae1b9577e11b574fab23ffae6853be79f839422dcfc6de42df0b`. |
| `linux-bubblewrap-sdk-v1`. H-22, Debian 13, kernel `6.12.63+deb13-amd64`, linux-x64. 72/72 with owned cleanup. | Node `50e602a83ece2c4de75d8dbd32777c7833a6eaf7`, Run `7eb7b9726a6a4b5d974d20fdadd3df8d`, receipt SHA-256 `57f41658b57c18ff350fde2a9afc428c9434946b1aa829735325336019288fcf`. | Stage manifest SHA-256 `5eedcd1733c25a38545d77f9f1d9f2d9aae1bee04d07b71584272c08f3f02616`, AOT probe SHA-256 `eda60f8c071559985f88d17e1d6722f1be1f6b48a87b0845befc425496d99e7c`. |

Both composed receipts use the official MXC 1.0.1 pin, schema 1.0.0 and native source `fda29ac63bc306b7f97f3b86b4b63d44f7f40cf2`. The historical stage hashes identify the exact experimental bundles. Runtime admission independently checks the protected official artifacts and the native prerequisites. The source checkpoints retain the exact artifact inventories and observations. [AOT revalidation](#mxc-aot-01-revalidation-checkpoint--2026-11-17-utc) · [Final Windows delivery](https://github.com/ArcForges/Plan/blob/e0ab253debdcb17c67029f6101c59b021a73667b/docs/afv2-mxc-02-progress.md#final-candidate-native-windows-receipts--2026-11-18) · [Linux full-profile qualification](#linux-full-profile-native-checkpoint--2026-11-17-utc)

In the final Windows Run, Winsock reported 10013 and the calibrated local peer saw no additional request. The same payload performed the recorded filesystem checks under real memory and child-process pressure. The receipt confirms ConPTY, owner recovery, an empty Job after Stop and persistent private data across Runs. It records `wrapperQualificationPassed=true` and `qualificationPassed=false` with external selected egress unverified. The prior same-source timeout and the earlier external attempts remain in the delivery evidence. The Windows `reject-missing-policy` case reported official executor exit 1 with `official_executor_config_rejection`, unknown payload start certainty and confirmed cleanup. The lower-capability-host case remains NOT_RUN.

On H-22, the gated missing-Bubblewrap case returned official `BackendError12` before payload execution. The separate controller-absence case observed missing child `cpu.max` and refused owner admission. The native combination included default-deny and selected literal IPv4 TCP/UDP egress. The DNS measurement covers denial. Stable Bubblewrap lacks IPv6 connectivity and host/public ingress, and namespace-denial injection remains NOT_RUN under the where-feasible clause.

The gate refuses missing, stale or mismatched qualification, unavailable required native prerequisites and unsupported constraints before user code runs. The Windows external selected TCP/UDP request retains its policy for the supported mode and returns the actual native outcome. A requirement for locally verified external selected egress fails the assurance check.
