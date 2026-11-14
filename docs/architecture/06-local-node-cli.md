# Local Node, CLI and terminal sessions

Status: current V2 design. AFV2-CORE-01 through AFV2-CORE-03 implement the common core and Run owner; AFV2-CLI-01 and AFV2-CLI-02 deliver local commands and terminal behavior. SDK/profile qualification is a prerequisite, not an assertion of present terminal compatibility. [Resource](04-resource-management.md), [filesystem](05-filesystem-data.md) and [lifecycle](07-lifecycle-recovery.md) define the shared behavior.

## 1. First-class local use

The local CLI is the normal product entry point. The default target is the current user's local Node. Listing/creating/configuring Sandboxes, starting/stopping Runs, terminal interaction, resource observation and owned-data operations require local authorization but no account, subscription, Center connection or remote token. Signing out, an expired official subscription and an unreachable Center do not stop local Runs or disable local commands.

Center connectivity is an optional Node subsystem. Remote requests and local requests enter the same typed command dispatcher and Sandbox Core. The remote transport performs its own authentication/authorization and attaches a verified principal; it does not bypass local policy or call a raw host command runner. A remote command may execute arbitrary argv **inside an already authorized Sandbox profile**, which is distinct from an unrestricted host shell.

Remove current HUMAN-only diagnostic submit restrictions and the old Task/Attempt route. Do not expose `--test-mode`, fake HUMAN classification or `ARCFORGES_TEST_ALLOW_LOCAL_SCRIPT_SUBMIT` as ways to use the product. Generic scripts, interactive terminals and AI CLIs are ordinary local callers with the same user-granted Sandbox boundary; the core does not infer AI session identity.

Current contrary behavior is source-backed: [LocalSubmission](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/LocalSubmission.cs) and [RunCommand](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.CommandLine/RunCommand.cs) at the audited baseline.

## 2. Composition and dependencies

The product retains one `arcforges` CLI/Node host and the necessary platform service bootstrap. A durable internal RunSupervisor process owns each Run's official backend, terminal master/pipes, resource-scope identity and finalization record. It is a trusted implementation detail launched by the Node through a fixed executable and a private capability-bound handshake, not a second public CLI or arbitrary remote helper. Windows' existing service supervisor may remain as infrastructure; it is not a desktop client.

The Node owns Sandbox configuration/storage metadata, the single-writer command processor, operation receipts, recovery, Resource Manager, local API and optional Center link. It holds no exclusive terminal handle whose loss would kill a Run merely because the Node restarts. The RunSupervisor persists only the bounded facts needed for Node rebind and recovery; the Node remains authoritative for product state and permissions.

The local endpoint reuses DesktopPlatform LocalRpc service mode: current-user Windows named pipe or Unix-domain socket in an owner-only directory. Verify the OS peer identity; no unauthenticated loopback TCP fallback. Preserve bounded control lanes so stop, detach and health cannot wait behind large file transfers or terminal viewers. The Node exposes V2 Node/Sandbox/Run/Resource/Data operations only; delete old task/queue/workspace/Fleet method registrations after the compatibility cutoff.

Useful existing composition sources:

- [Host role dispatcher](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Host/Program.cs)
- [NodeHost](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Api/NodeHost.cs)
- [NodeRuntime](https://github.com/ArcForges/ArcForges/blob/10f692224f94916cfc93fbad971f80ec340c5edf/src/ArcForges.Node.Core/NodeRuntime.cs)
- [LocalRpcEndpoint](https://github.com/ArcForges/DesktopPlatform/blob/e02ebe455d4fe2c06b19dabc0f3179a43ab21aa6/src/BuildingBlocks/ArcForges.LocalRpc/LocalRpcEndpoint.cs)

Do not add Desktop shell, Avalonia, Mobile, MCP, AI adapter, compiler-cache or plugin infrastructure to this closure. Shared package deletion is not implied by removing a consumer.

## 3. Node startup and stop

Startup resolves and validates the owner configuration/data root, obtains the per-user singleton, opens the store with its existing backup/forward-migration checks, compares boot identity, reconciles persistent Sandbox and Run ownership, then publishes readiness. While recovery is in progress, read-only health/state calls may respond with `recovering`; new Starts and destructive mutations remain refused. Independent healthy Sandboxes may become available once their own reconciliation is complete; an unresolved Run keeps its Sandbox blocked from deletion.

Autostart reuses the installed user-service/supervisor mechanism. If OS/session policy prevents safe autostart, return `node_unavailable` with the explicit manual `arcforges node start` remedy. Do not bypass a foreign Job, impersonate another user, elevate silently or install services without the normal installer path.

`node stop` requests Node shutdown while allowing durable supervisors to continue under their existing immutable policies by default. `node stop --stop-runs` is a distinct explicit operation that requests orderly Run stops and reports any unresolved scope; it is not silently performed on sign-out. Host reboot does not restart Runs automatically. Upgrades drain old binaries and negotiate ownership/rebind as defined in the lifecycle and migration design.

## 4. Command surface

The command hierarchy exposes the same objects as the public contracts. Exact short aliases may be added only where unambiguous; examples below are the canonical spelling. Every mutation prints its operation ID on diagnostic/JSON output so interrupted clients can inspect the durable result.

| Command | Behavior |
|---|---|
| `arcforges node start`, `status`, `stop` | Manage/inspect the local Node |
| `arcforges sandbox create <name>` | Create a new owned root with an explicit/default reviewed profile; print Sandbox ID |
| `arcforges sandbox list` / `inspect <id>` | Show state, revision, data paths, grants and capability status |
| `arcforges sandbox configure <id> --file <path> --expected-revision <n>` | Validate and atomically commit a full configuration revision |
| `arcforges sandbox usage <id>` | Start/read a bounded owned-data usage scan |
| `arcforges sandbox import <id> <source> --to <relative-path>` | Explicit bounded local file copy into owned data |
| `arcforges sandbox export <id> <relative-path> --to <destination>` | Export one owned regular file after a quiescent verified snapshot; explicit host-destination overwrite |
| `arcforges sandbox delete <id>` | Display/create a concrete deletion plan, then apply with explicit confirmation or supplied reviewed plan/confirmation flag |
| `arcforges run start <sandbox-id> -- <program> [args...]` | Immediate Start; attach by default, or print Run ID with `--detach` |
| `arcforges run list [--sandbox <id>]` / `inspect <run-id>` | Read Run state, snapshot, outcome and effective resources |
| `arcforges run attach <run-id>` | Attach as input writer when authorized and available, or `--read-only` observer |
| `arcforges run detach <run-id> --lease <id>` | Release this caller's terminal attachment; never stop the Run |
| `arcforges run stop <run-id>` | Idempotent graceful stop then bounded forced cleanup under recorded policy |
| `arcforges run logs <run-id> [--follow]` | Bounded output with offsets and explicit gaps |
| `arcforges resources show` / `watch` | Host/Sandbox/Run budgets, pressure and desired/applied/readback limits |
| `arcforges center add` / `select` / `remove`, `login`, `logout`, `devices` | Optional remote management setup and identity |

Global `--json` selects versioned machine-readable results; command data goes to stdout and diagnostics to stderr. Terminal raw output and JSON control output are never mixed on one stream: `run start --json` returns the start receipt/Run ID, and a separate attach command owns the terminal. Commands accept explicit timeout/cancellation, with unknown-effect results when the deadline passes after dispatch. A caller can query the operation; it must not blindly mint a new Start ID after a network timeout.

The default is local. A global `--device <id>` selects a remote registered device through a selected/configured Center; `--center <alias>` chooses that Center explicitly. The CLI displays the remote target before destructive confirmation. A remote target never silently falls back to local if offline. Remote device status and authorization failures are distinct from local Node health. These options route typed operations, not SSH or a raw command tunnel. Node process/service startup and shutdown commands are local-only; specifying a remote device for them is a validation error.

Remove old `tasks`, `queue`, `jobs`, session/agent, dependency, retry, toolchain, compiler-cache, worktree and placement options from help/completions and code. Do not leave deprecated commands as permanent no-op shells. The compatibility document gives the one-time migration mapping.

## 5. Start snapshot and effects

`RunService.Start` requires Sandbox ID and expected configuration revision; argv (or an explicit shell program and script), working directory relative to an allowed directory, validated environment overrides, terminal mode/initial dimensions and resource request including preemptibility. Attach/detach is a client decision after the Start result, not a different execution policy or lifetime. The default working directory is owned `work/`. Executable lookup uses the validated Sandbox environment/profile, not arbitrary Center environment or Node secret-bearing process variables.

Persist the final redacted argv/environment/profile/grants/resource snapshot and its digest before user code may execute. Explicit secret injections are referenced by protected local secret identity/version and delivered only to the owner launch handoff; do not store plaintext secret environment in the snapshot. Sensitive values are excluded from ordinary audit/telemetry; the API returns redacted display fields. The snapshot includes official SDK/executor version, backend/profile identity and capability evidence reference. One Run cannot switch profiles mid-execution to bypass an unsupported capability.

Start returns an operation receipt and Run ID. `payload_started` is `unknown`, `no` or `confirmed` according to trusted evidence; an official executor's existence does not by itself confirm that the sandbox payload reached execution. All errors include effect certainty. A definite pre-launch refusal becomes FAILED and releases reservations after confirmed no effect; uncertainty becomes RECOVERY_REQUIRED until ownership reconciliation. Nonzero payload exit after confirmed execution is still EXITED, not a launch failure.

## 6. Genuine terminal modes

`--terminal auto|on|off` selects terminal behavior. Auto uses an actual terminal only when the initiating CLI has an interactive terminal and the selected profile supports the qualified terminal mechanism. If an interactive terminal is requested but unavailable, refuse with `terminal_unsupported`; do not silently claim a pipe is a terminal. Off uses ordinary stdin/stdout/stderr pipes, useful for redirection and machine scripts. Terminal mode emits one PTY output byte stream; stderr is not falsely separated after the terminal merged it.

The Windows qualified candidate uses C# Native AOT RunSupervisor plus unchanged official `wxc-exec.exe` under ConPTY, with explicit published configuration and fail-closed fallback policy. Linux uses the official published profile's supported terminal composition. These candidates become supported profiles only after AFV2-MXC native tests. Do not invent .NET SDK PTY/startup-attribute APIs or fork MXC. The official executor's stdout may contain workload bytes or backend messages; **never parse it as a trusted lifecycle/control channel**.

The RunSupervisor owns the PTY master for the full Run. CLI disconnect, loss of a viewer, Center outage or input-lease expiry must not close that owner handle. The program may block awaiting further input while detached. Reattach binds to the same live terminal and current output cursor. A terminal cannot be recreated around an already-running process after its real owner died; record that loss honestly.

Long-running services must keep their foreground root alive. The stable one-shot ProcessContainer backend finalizes when the root exits and stops remaining descendants. Background child processes are managed while the root runs, but daemonization/double-fork is not a promise of survival after root exit. Use `--detach` to detach the CLI while leaving the foreground program under its durable Run owner.

## 7. Terminal leases, input and resize

There is at most one write lease per Run terminal, with a caller identity, opaque lease ID, generation, monotonic expiry and expected next input sequence. Read-only observers have independent bounded output cursors and no input/signal/resize authority. A fresh attachment can observe current writer identity in privacy-preserving form; it cannot steal control automatically. Explicit takeover requires the authenticated local owner permission, revokes the old lease, increments generation and produces an audit event.

Input frames are bounded bytes with lease ID/generation and sequence. Repeated sequence/data is duplicate-safe within the lease's retained acknowledgment window; a sequence reused with different bytes is a conflict. A gap is refused and asks the client to resynchronize. Input is not retained as a transcript or logged. After an unknown input acknowledgment, do not replay beyond the deduplication window as if exactly-once input were assured; notify the user that input delivery is uncertain. Terminal input is not a persistent command queue.

Resize requires a valid writer lease, positive bounded rows/columns and a monotonic resize sequence. The owner applies the native terminal resize and reports the result; a read-only observer cannot resize the application. On platforms that cannot resize a particular profile, report unsupported and keep prior dimensions.

Ctrl+C in attached terminal mode is delivered to the terminal's foreground application using the qualified native terminal mechanism. It is not automatically translated to a whole-Run cancel command. In pipes mode, the CLI's interrupt can request the explicitly documented Stop operation. The default local detach escape is Ctrl+] followed by `d`; document how to send a literal escape and allow disabling the escape handling for raw workflows. An explicit `run stop` always remains available through the reserved control lane.

For pipe mode, EOF is an explicit stdin-close operation owned by the input lease. Detach and network loss do not implicitly mean EOF unless the start policy explicitly selected close-on-detach. Terminal mode preserves the PTY; an EOF character is input interpreted by the terminal/application, not a fabricated transport close.

## 8. Output retention and backpressure

Frames carry Run ID, stream kind, byte offset, length and generation; retained terminal bytes and piped stdout/stderr have documented independent cursor spaces. The transport uses bounded frames and per-subscriber queues. When a viewer falls behind, discard that viewer's queued copy and emit GAP with the earliest available offset; do not block a running application forever because one remote browser stopped reading. File-backed retention has an explicit per-Run byte cap and rotation policy. Reaching the cap emits a retention event and advances the earliest cursor; it never silently claims a complete log.

Raw output is untrusted. Web renders plain escaped text or a constrained terminal emulator, never raw HTML. Terminal escape sequences may influence a terminal display but cannot become trusted Node control messages. Binary bytes are permitted in pipe logs; text decoding errors must not corrupt byte offsets. File transfer and telemetry channels are separate from terminal bytes.

A terminal byte transcript is not a full screen-state snapshot. A reconnecting TUI receives recent bytes plus a resize/redraw request when supported, and the user can request redraw; do not claim perfect screen reconstruction from a truncated tail. The V2 remote surface watches output and controls Run lifecycle but exposes no terminal input/resize or browser terminal. A remote CLI attach request is refused as unsupported; it may explicitly watch read-only output instead. No secret-bearing terminal screen state is automatically recorded remotely. Output read/stream access requires the same Run authorization as inspection and is audited at the operation level without logging the content.

## 9. Exit and error presentation

Run state and raw exit observation are separate. Record `exit_source` (`payload`, `official_executor`, `supervisor`, `unknown`), raw exit code/signal when observed, `payload_started`, termination reason, timestamps and effect certainty. The CLI mirrors a trustworthy payload/executor exit according to its provenance and OS shell range; it prints a clear message when only wrapper failure or cleanup uncertainty is known. An unknown result is not success merely because a wrapper returned zero.

Control-command exit mapping is stable and documented: 0 confirmed successful requested control effect; 2 usage/validation; 3 conflict/revision or in-use refusal; 4 authorization; 5 unsupported capability; 6 resource unavailable; 7 transport/Node unavailable; 8 operation effect or cleanup uncertain. An attached Run's process-exit mapping is a separate channel and does not reuse these values as product control semantics. A detached Start exits 0 only for confirmed acceptance and prints the Run/operation ID; the Run can later fail and must be inspected.

## 10. Acceptance

AFV2-CLI-01 proves all local management paths while signed out, without a Center, and with expired official entitlement; all must reach the same Sandbox Core and respect filesystem/resource policy. Include JSON stability, help/completion removal, target disambiguation, duplicate Start handling, immediate resource refusal and recoverable timeout effects.

AFV2-CLI-02 proves genuine native terminal behavior: shell and full-screen TUI, raw input and Unicode, foreground Ctrl+C, window resize, stdin EOF in pipe mode, byte-exact piped output, detach/reattach, writer contention/takeover, stale lease refusal, slow viewer backpressure, GAP recovery, canceled attach, Node restart with the same live owner, root exit with background descendants drained, and offline Center while a local terminal remains usable. Use actual PTY/ConPTY on the designated native hosts; tests that use only ordinary pipes do not close terminal acceptance.
